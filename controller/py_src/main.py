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
        self.ioIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)

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

        #Dictionary indexed by pssgId. Each pssg has a dictionry with all the pssg parametters indexed
        #by pssg parametters names
        self.pssgsParams = self.dataBase.getPssgsParams()

        #By default our exit code will be success
        self.exitCode = 0




    def getIoIfaceArgs(self):
        '''
        This method return a string with all arguments for the pssg-iface
        binary.
        They are got from Passage table of local DataBase
        '''


        ioIfaceArgs = ''


        for pssgId in self.pssgsParams:

            for pssgParamName in self.dataBase.getPssgParamsNames():
                pssgParamValue = self.pssgsParams[pssgId][pssgParamName]
                if pssgParamValue:
                    ioIfaceArgs += '--{} {} '.format(pssgParamName, pssgParamValue)

        return ioIfaceArgs



    def launchIoIface(self):
        '''
        Launch Pssg Iface binary.
        Return a process object
        '''

        ioIfaceCmd = '{} {}'.format(IOIFACE_BIN, self.getIoIfaceArgs())

        logMsg = 'Launching IO Interface with the following command: {}'.format(ioIfaceCmd)
        self.logger.debug(logMsg)

        ioIfaceProc = subprocess.Popen(ioIfaceCmd, shell=True, 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT
                                        )

        return ioIfaceProc
        



    def sigtermHandler(self, signal, frame):

        try:
            self.logger.info('Getting SIGTERM.')
            self.ioIfaceQue.unlink()
            self.ioIfaceQue.close()
        
        except posix_ipc.ExistentialError:
            self.logger.info('An earlier SIGTERM signal is being processed.')

        #self.exitFlag.set()



    def procCard(self, pssgId, side, cardNumber):
        '''
        This method is called each time somebody put a card in a card reader
        '''

        allowed, personId, notReason = self.dataBase.canAccess(pssgId, side, cardNumber)

        if allowed:
            #Open the pssg as soon as posible
            print('Opening the pssg...')


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


    def procButtom(self, pssgId, state):
        print('procButtom', pssgId, state)


    def procState(self, pssgId, state):
        print('procState', pssgId, state)



    def run(self):


        self.logger.debug('Starting Controller')
        
        #Launching Pssg Iface binary
        self.launchIoIface()

        #Starting the "Event Manager" thread
        self.eventMngr.start()

        #Starting the "Event Manager" thread
        self.netMngr.start()
        
        try:
            while True:
                ioIfaceData = self.ioIfaceQue.receive()
                ioIfaceData = ioIfaceData[0].decode('utf8')
                pssgId, side, varField = ioIfaceData.split(';')
                command, value  = varField.split('=')
                self.handlers[command](pssgId, side, value)
            
        except posix_ipc.SignalError:
            self.logger.debug('IO Interface Queue was interrupted by a OS signal.')

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

