#!/usr/bin/env python3

#from argparse import ArgumentParser

import logging
import logging.handlers

import socket
import datetime
import sys
import select
import subprocess

import queue
import threading
import posix_ipc
import signal

import database
import ioiface
import events
import network
import passage
import crud
from config import *





class Controller(object):

    def __init__(self):
        #Defining log structures with the possibility of rotation by logrotate
        loggingHandler = logging.handlers.WatchedFileHandler(LOGGING_FILE)

        loggingFormat = '%(asctime)s %(levelname)s %(threadName)s: %(message)s'
        dateFormat = '[%b %d %H:%M:%S]'

        loggingFormatter = logging.Formatter(loggingFormat, dateFormat)
        loggingHandler.setFormatter(loggingFormatter)

        self.logger = logging.getLogger('Controller')
        self.logger.setLevel(loggingLevel)
        self.logger.addHandler(loggingHandler)

        self.dataBase = database.DataBase(DB_FILE)

        self.ioIface = ioiface.IoIface(self.dataBase)
        
        #Defining a OS queue to get messages from the ioiface
        self.ioIfaceQue = posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)

        #Dictionary containing functions to be launched according to the messages received by the ioiface
        self.handlers = { 'card'   : self.procCard,
                          'button' : self.procButton,
                          'state'  : self.procState
                        }

        #Queue used to send events to eventThread
        self.mainToEvent = queue.Queue()
        
        #Queue used to send responses from netMngr thread to event thread
        netToEvent = queue.Queue()

        #Queue used to send responses from netMngr thread to ReSender thread
        netToReSnd = queue.Queue()

        #Exit flag to notify threads to finish
        self.exitFlag = threading.Event()


        self.lockPssgsControl = threading.Lock()
        self.pssgsControl = passage.PssgsControl()

        #Creating the CRUD Manager Thread 
        self.crudMngr = crud.CrudMngr(self.lockPssgsControl, self.pssgsControl, self.exitFlag)

        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(netToEvent, netToReSnd, self.crudMngr, self.exitFlag)        

        #Setting internal crudMngr reference to netMngr thread to be able to answer
        #once the CRUD where commited in DB
        self.crudMngr.netMngr = self.netMngr

        #Creating the Event Manager Thread giving to it the previous event queue
        self.eventMngr = events.EventMngr(self.mainToEvent, self.netMngr, netToEvent, netToReSnd, self.exitFlag)

        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        signal.signal(signal.SIGTERM, self.sigtermHandler)
        signal.signal(signal.SIGINT, self.sigtermHandler)

        #By default our exit code will be success
        self.exitCode = 0



    #---------------------------------------------------------------------------#

    def sigtermHandler(self, signal, frame):

        try:
            self.logger.info('Getting SIGTERM.')
            self.ioIfaceQue.unlink()
            self.ioIfaceQue.close()

        except posix_ipc.ExistentialError:
            self.logger.info('An earlier SIGTERM signal is being processed.')



    #---------------------------------------------------------------------------#




    def openPssg(self, pssgId):
        '''
        This method is called by "procCard" and "procButton" methods to release
        the passage and start the buzzer.
        It also creates a thread to close the passage and buzzer
        '''

        with self.lockPssgsControl:

            pssgControl = self.pssgsControl.params[pssgId]

            pssgControl['pssgObj'].release(True)
            self.logger.debug("Releasing the passage {}.".format(pssgId))
            pssgControl['pssgObj'].startBzzr(True)
            self.logger.debug("Starting the buzzer on passage {}.".format(pssgId))
            pssgControl['accessPermit'].set()
            pssgControl['timeAccessPermit'] = datetime.datetime.now()
    

            if not pssgControl['cleanerPssgMngrAlive'].is_set():
                pssgControl['cleanerPssgMngrAlive'].set()
                cleanerPssgMngr = passage.CleanerPssgMngr(pssgControl, self.exitFlag)
                cleanerPssgMngr.start()





    #---------------------------------------------------------------------------#

    def procCard(self, pssgId, side, cardNumber):
        '''
        This method is called each time somebody put a card in a card reader
        '''

        allowed, personId, notReason = self.dataBase.canAccess(pssgId, side, cardNumber)

        if allowed:
            self.openPssg(pssgId)

        dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
        event = {'pssgId' : pssgId, 
                 'eventType' : 1,
                 'dateTime' : dateTime,
                 'latchType' : 1,
                 'personId' : personId,
                 'side' : side,
                 'allowed' : allowed,
                 'notReason' : notReason 
                }

        #Sending the event to the "Event Manager" thread
        self.mainToEvent.put(event)



    #---------------------------------------------------------------------------#

    def procButton(self, pssgId, side, value):
        '''
        This method is called each time somebody press the button to release
        the passage
        '''

        self.openPssg(pssgId)

        dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


        event = {'pssgId' : pssgId,
                 'eventType' : 2,
                 'dateTime' : dateTime,
                 'latchType' : 3,
                 'personId' : 1,
                 'side' : side,
                 'allowed' : True,
                 'notReason' : None
                }

        #Sending the event to the "Event Manager" thread
        self.mainToEvent.put(event)







    #---------------------------------------------------------------------------#

    def procState(self, pssgId, side, openOrClose):
        '''
        This method is called each time a passage change its state. (It is opened or closed)
        '''

        with self.lockPssgsControl:

            pssgControl = self.pssgsControl.params[pssgId]

            #Converting "openOrClose" to int type to evaluete it on if statement
            openOrClose = int(openOrClose)
            #The state of the passage indicates that was opened
            if openOrClose:
                pssgControl['openPssg'].set()
                #If the passage was open in a permitted way
                if pssgControl['accessPermit'].is_set():
                    #Creates a StarterAlrmMngrAlive if not was previously created by other access
                    if not pssgControl['starterAlrmMngrAlive'].is_set():
                        starterAlrmMngr = passage.StarterAlrmMngr(pssgControl, self.exitFlag)
                        starterAlrmMngr.start()

                #If the passage was not opened in a permitted way, start the alarm
                else:
                    logMsg = ("Unpermitted access on passage: {}, "
                              "Starting the alarm.".format(pssgId)
                             )
                    self.logger.warning(logMsg)
                    pssgControl['pssgObj'].startBzzr(True)

            #The state of the passage indicates that was closed
            else:
                logMsg = ("The state of the passage: {}, indicates that was closed. "
                          "Stopping the alarm.".format(pssgId)
                         )
                self.logger.info(logMsg)
                pssgControl['openPssg'].clear()
                pssgControl['pssgObj'].startBzzr(False)



    #---------------------------------------------------------------------------#

    def run(self):


        self.logger.debug('Starting Controller')
        
        #Launching Pssg Iface binary
        self.ioIface.start()

        self.pssgsControl.loadParams()

        #Starting the "Event Manager" thread
        self.eventMngr.start()

        #Starting the "Event Manager" thread
        self.netMngr.start()

        #Starting the "CRUD Manager" thread
        self.crudMngr.start()
        
        try:
            while True:
                ioIfaceData = self.ioIfaceQue.receive()
                ioIfaceData = ioIfaceData[0].decode('utf8')
                print(ioIfaceData)
                pssgNum, side, varField = ioIfaceData.split(';')
                pssgNum = int(pssgNum)

                try:
                    pssgId = self.pssgsControl.pssgIdPssgNum[pssgNum]
                    pssgId = int(pssgId)

                    side = int(side)
                    command, value  = varField.split('=')
                    self.handlers[command](pssgId, side, value)

                except KeyError:
                    self.logger.debug('Passage not configured.')
            
        except posix_ipc.SignalError:
            self.logger.debug('IO Interface Queue was interrupted by a OS signal.')

#        except Exception as exception:
#            logMsg = 'The following exception occurred: {}'.format(exception)
#            self.logger.debug(logMsg)
#            self.exitCode = 1

        #Sending the terminate signal to IO interface Proccess.
        self.ioIface.stop()

        self.logger.debug('Notifying all threads to finish.')
        self.exitFlag.set()
        self.logger.info('Waiting to finish all threads...')
        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()


        self.logger.info('Now exiting main thread')
        sys.exit(self.exitCode)


    #---------------------------------------------------------------------------#    


#---- MAIN EXECUTION ---#
    
controller = Controller()
controller.run()

