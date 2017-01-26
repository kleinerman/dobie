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
        #self.pssgsControl.loadParams()

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




    def openPssg(self, pssgNum):
        '''
        This method is called by "procCard" and "procButton" methods to release
        the passage and start the buzzer.
        It also creates a thread to close the passage and buzzer
        '''

        with self.lockPssgsControl:

            pssgControl = self.pssgsControl.params[pssgNum]

            pssgControl['pssgObj'].release(True)
            self.logger.debug("Releasing the passage {}.".format(pssgNum))
            pssgControl['pssgObj'].startBzzr(True)
            self.logger.debug("Starting the buzzer on passage {}.".format(pssgNum))
            pssgControl['accessPermit'].set()
            pssgControl['timeAccessPermit'] = datetime.datetime.now()
    

            if not pssgControl['cleanerPssgMngrAlive'].is_set():
                pssgControl['cleanerPssgMngrAlive'].set()
                cleanerPssgMngr = passage.CleanerPssgMngr(pssgControl, self.exitFlag)
                cleanerPssgMngr.start()





    #---------------------------------------------------------------------------#

    def procCard(self, pssgNum, side, cardNumber):
        '''
        This method is called each time somebody put a card in a card reader
        '''

        try:
            with self.lockPssgsControl:
                pssgId = self.pssgsControl.getPssgId(pssgNum)

            allowed, personId, notReasonId = self.dataBase.canAccess(pssgId, side, cardNumber)

            if allowed:
                self.openPssg(pssgNum)

            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
            event = {'pssgId' : pssgId, 
                     'eventTypeId' : 1,
                     'dateTime' : dateTime,
                     'latchId' : 1,
                     'personId' : personId,
                     'side' : side,
                     'allowed' : allowed,
                     'notReasonId' : notReasonId
                    }

            #Sending the event to the "Event Manager" thread
            self.mainToEvent.put(event)


        except passage.PassageNotConfigured:
            logMsg = 'Card was read on passage {} but it is not configured'.format(pssgNum)
            self.logger.warning(logMsg)



    #---------------------------------------------------------------------------#

    def procButton(self, pssgNum, side, value):
        '''
        This method is called each time somebody press the button to release
        the passage
        '''

        try:
            with self.lockPssgsControl:
                pssgId = self.pssgsControl.getPssgId(pssgNum)

            self.openPssg(pssgNum)

            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


            event = {'pssgId' : pssgId,
                     'eventTypeId' : 2,
                     'dateTime' : dateTime,
                     'latchId' : 3,
                     'personId' : 1,
                     'side' : side,
                     'allowed' : True,
                     'notReasonId' : None
                    }

            #Sending the event to the "Event Manager" thread
            self.mainToEvent.put(event)

        except passage.PassageNotConfigured:
            logMsg = 'Button pressed on passage {} but it is not configured'.format(pssgNum)
            self.logger.warning(logMsg)







    #---------------------------------------------------------------------------#

    def procState(self, pssgNum, side, openOrClose):
        '''
        This method is called each time a passage change its state. (It is opened or closed)
        '''

        try:
            with self.lockPssgsControl:
                #pssgId is not used in this method. We just want to raise
                #PassageNotConfigured exception if the passage is not confiugred
                self.pssgsControl.getPssgId(pssgNum)
                pssgControl = self.pssgsControl.params[pssgNum]

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
                                  "Starting the alarm.".format(pssgNum)
                                 )
                        self.logger.warning(logMsg)
                        pssgControl['pssgObj'].startBzzr(True)

                #The state of the passage indicates that was closed
                else:
                    logMsg = ("The state of the passage: {}, indicates that was closed. "
                              "Stopping the alarm.".format(pssgNum)
                             )
                    self.logger.info(logMsg)
                    pssgControl['openPssg'].clear()
                    pssgControl['pssgObj'].startBzzr(False)

        except passage.PassageNotConfigured:
            logMsg = 'State received on passage {} but it is not configured'.format(pssgNum)
            self.logger.warning(logMsg)




    #---------------------------------------------------------------------------#

    def run(self):


        self.logger.debug('Starting Controller')
        
        #Launching Pssg Iface binary
        self.ioIface.start()

        with self.lockPssgsControl:
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
                side = int(side)
                command, value  = varField.split('=')
                self.handlers[command](pssgNum, side, value)

            
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

