#!/usr/bin/env python3

#from argparse import ArgumentParser

import logging
import logging.handlers

import socket
import datetime
import sys
import select

import queue
import threading
import posix_ipc
import signal

import database
import events
import network
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
        self.doorIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)

        self.handlers = { 'card'   : self.procCard,
                          'buttom' : self.procButtom,
                          'state'  : self.procState
                        }

        #Exit flag to notify threads to finish
        self.exitFlag = threading.Event()

        #Queue used to send events to eventThread
        self.mainToEvent = queue.Queue()
        
        #Queue used to send responses from netMngr thread to event thread
        netToEvent = queue.Queue()


        #Queue used to send responses from netMngr thread to ReSender thread
        netToReSnd = queue.Queue()


        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(netToEvent, netToReSnd, self.exitFlag)        

        #Creating the Event Manager Thread giving to it the previous event queue
        self.eventMngr = events.EventMngr(self.mainToEvent, self.netMngr, netToEvent, netToReSnd, self.exitFlag)


        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        signal.signal(signal.SIGTERM, self.sigtermHandler)
        signal.signal(signal.SIGINT, self.sigtermHandler)

        #By default our exit code will be success
        self.exitCode = 0


        print(self.dataBase.getDoorsParams())


    def sigtermHandler(self, signal, frame):

        try:
            self.logger.info('Getting SIGTERM.')
            self.doorIfaceQue.unlink()
            self.doorIfaceQue.close()
        
        except posix_ipc.ExistentialError:
            self.logger.info('An earlier SIGTERM signal is being processed.')

        #self.exitFlag.set()



    def procCard(self, doorId, side, cardNumber):
        '''
        This method is called each time somebody put a card in a card reader
        '''

        allowed, personId, notReason = self.dataBase.canAccess(doorId, side, cardNumber)

        if allowed:
            #Open the door as soon as posible
            print('Opening the door...')


        dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
        event = {'doorId' : doorId, 
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


    def procButtom(self, doorId, state):
        print('procButtom', doorId, state)


    def procState(self, doorId, state):
        print('procState', doorId, state)



    def run(self):


        self.logger.debug('Starting Controller')
        #Starting the "Event Manager" thread
        self.eventMngr.start()

        #Starting the "Event Manager" thread
        self.netMngr.start()
        
        try:
            while True:
                doorIfaceData = self.doorIfaceQue.receive()
                doorIfaceData = doorIfaceData[0].decode('utf8')
                doorId, side, varField = doorIfaceData.split(';')
                command, value  = varField.split('=')
                self.handlers[command](doorId, side, value)
            
        except posix_ipc.SignalError:
            self.logger.debug('Door Interface Queue was interrupted by a OS signal.')

        except Exception as exception:
            logMsg = 'The following exception occurred: {}'.format(exception)
            self.logger.debug(logMsg)
            self.exitCode = 1

        self.logger.debug('Notifying all threads to finish.')
        self.exitFlag.set()
        self.logger.info('Waiting to finish all threads...')
        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()


        self.logger.info('Now exiting main thread')
        sys.exit(self.exitCode)



    
controller = Controller()
controller.run()

