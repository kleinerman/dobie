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
import door
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
        self.eventQueue = queue.Queue()
        
        #Queue used to send responses from netMngr thread to event thread
        netToEvent = queue.Queue()

        #Queue used to send responses from netMngr thread to ReSender thread
        self.netToReSnd = queue.Queue()

        #Exit flag to notify threads to finish
        self.exitFlag = threading.Event()


        self.lockDoorsControl = threading.Lock()
        self.doorsControl = door.DoorsControl()
        #self.doorsControl.loadParams()

        #Creating the CRUD Manager Thread 
        self.crudMngr = crud.CrudMngr(self.lockDoorsControl, self.doorsControl, self.exitFlag)

        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(netToEvent, self.netToReSnd, self.crudMngr, self.exitFlag)        

        #Setting internal crudMngr reference to netMngr thread to be able to answer
        #once the CRUD where commited in DB
        self.crudMngr.netMngr = self.netMngr

        #Flag to know if Resender Thread is alive
        self.resenderAlive = threading.Event()

        #Creating the Event Manager Thread giving to it the previous event queue
        self.eventMngr = events.EventMngr(self.eventQueue, self.netMngr, netToEvent, self.netToReSnd, self.resenderAlive, self.exitFlag)

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




    def openDoor(self, doorNum):
        '''
        This method is called by "procCard" and "procButton" methods to release
        the door and start the buzzer.
        It also creates a thread to close the door and buzzer
        '''

        with self.lockDoorsControl:

            doorControl = self.doorsControl.params[doorNum]

            doorControl['doorObj'].release(True)
            self.logger.debug("Releasing the door {}.".format(doorNum))
            doorControl['doorObj'].startBzzr(True)
            self.logger.debug("Starting the buzzer on door {}.".format(doorNum))
            doorControl['accessPermit'].set()
            doorControl['timeAccessPermit'] = datetime.datetime.now()
    

            if not doorControl['cleanerDoorMngrAlive'].is_set():
                doorControl['cleanerDoorMngrAlive'].set()
                cleanerDoorMngr = door.CleanerDoorMngr(doorControl, self.exitFlag)
                cleanerDoorMngr.start()





    #---------------------------------------------------------------------------#

    def procCard(self, doorNum, side, cardNumber):
        '''
        This method is called each time somebody put a card in a card reader
        '''

        try:
            with self.lockDoorsControl:
                doorId = self.doorsControl.getDoorId(doorNum)

            allowed, personId, denialCauseId = self.dataBase.canAccess(doorId, side, cardNumber)

            if allowed:
                self.openDoor(doorNum)

            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
            event = {'doorId' : doorId, 
                     'eventTypeId' : 1,
                     'dateTime' : dateTime,
                     'doorLockId' : 1,
                     'personId' : personId,
                     'side' : side,
                     'allowed' : allowed,
                     'denialCauseId' : denialCauseId
                    }

            #Sending the event to the "Event Manager" thread
            self.eventQueue.put(event)


        except door.DoorNotConfigured:
            logMsg = 'Card was read on door {} but it is not configured'.format(doorNum)
            self.logger.warning(logMsg)



    #---------------------------------------------------------------------------#

    def procButton(self, doorNum, side, value):
        '''
        This method is called each time somebody press the button to release
        the door
        '''

        try:
            with self.lockDoorsControl:
                doorId = self.doorsControl.getDoorId(doorNum)

            self.openDoor(doorNum)

            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


            event = {'doorId' : doorId,
                     'eventTypeId' : 2,
                     'dateTime' : dateTime,
                     'doorLockId' : 3,
                     'personId' : None,
                     'side' : side,
                     'allowed' : True,
                     'denialCauseId' : None
                    }

            #Sending the event to the "Event Manager" thread
            self.eventQueue.put(event)

        except door.DoorNotConfigured:
            logMsg = 'Button pressed on door {} but it is not configured'.format(doorNum)
            self.logger.warning(logMsg)







    #---------------------------------------------------------------------------#

    def procState(self, doorNum, side, openOrClose):
        '''
        This method is called each time a door change its state. (It is opened or closed)
        '''

        try:
            with self.lockDoorsControl:
                #doorId is used just to create the event below we get it here to raise
                #"DoorNotConfigured" exception if the door is not confiugred
                doorId = self.doorsControl.getDoorId(doorNum)
                doorControl = self.doorsControl.params[doorNum]

                #Converting "openOrClose" to int type to evaluete it on if statement
                openOrClose = int(openOrClose)
                #The state of the door indicates that was opened
                if openOrClose:
                    doorControl['openDoor'].set()
                    #If the door was open in a permitted way
                    if doorControl['accessPermit'].is_set():
                        #Creates a StarterAlrmMngrAlive if not was previously created by other access
                        if not doorControl['starterAlrmMngrAlive'].is_set():
                            starterAlrmMngr = door.StarterAlrmMngr(doorControl, self.eventQueue, self.exitFlag)
                            starterAlrmMngr.start()

                    #If the door was not opened in a permitted way, start the alarm and 
                    #send to server or store locally an event
                    else:
                        logMsg = ("Unpermitted access on door: {}, "
                                  "Starting the alarm.".format(doorNum)
                                 )
                        self.logger.warning(logMsg)
                        doorControl['doorObj'].startBzzr(True)

                        dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

                        event = {'doorId' : doorId,
                                 'eventTypeId' : 4,
                                 'dateTime' : dateTime,
                                 'doorLockId' : None,
                                 'personId' : None,
                                 'side' : None,
                                 'allowed' : False,
                                 'denialCauseId' : None
                                }

                        #Sending the event to the "Event Manager" thread
                        self.eventQueue.put(event)




                #The state of the door indicates that was closed
                else:
                    logMsg = ("The state of the door: {}, indicates that was closed. "
                              "Stopping the alarm.".format(doorNum)
                             )
                    self.logger.info(logMsg)
                    doorControl['openDoor'].clear()
                    doorControl['doorObj'].startBzzr(False)

        except door.DoorNotConfigured:
            logMsg = 'State received on door {} but it is not configured'.format(doorNum)
            self.logger.warning(logMsg)




    #---------------------------------------------------------------------------#

    def run(self):


        self.logger.debug('Starting Controller')
        
        #Launching Door Iface binary
        self.ioIface.start()

        with self.lockDoorsControl:
            self.doorsControl.loadParams()

        #Starting the "Event Manager" thread
        self.eventMngr.start()

        #Starting the "Event Manager" thread
        self.netMngr.start()

        #Starting the "CRUD Manager" thread
        self.crudMngr.start()

        #Starting the "Re Sender" thread because in the database there may be events to resend 
        if not self.resenderAlive.is_set():
            self.logger.info('Starting the Re Sender thread to resend events of local DB.')
            self.resenderAlive.set()
            reSender = events.ReSender(self.netMngr, self.netToReSnd, self.resenderAlive, self.exitFlag)
            reSender.start()

        
        try:
            while True:
                ioIfaceData = self.ioIfaceQue.receive()
                ioIfaceData = ioIfaceData[0].decode('utf8')
                print(ioIfaceData)
                doorNum, side, varField = ioIfaceData.split(';')
                doorNum = int(doorNum)
                side = int(side)
                command, value  = varField.split('=')
                self.handlers[command](doorNum, side, value)

            
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

