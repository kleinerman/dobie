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
import signal

import database
import network
import msgreceiver
import crud, crudresndr
import lifechecker
from config import *
import ctrllermsger
import rtevent


import os



class BackEndSrvr(object):

    def __init__(self):
        #Defining log structures with the possibility of rotation by logrotate
        loggingHandler = logging.handlers.WatchedFileHandler(LOGGING_FILE)

        loggingFormat = '%(asctime)s %(levelname)s %(threadName)s: %(message)s'
        dateFormat = '[%b %d %H:%M:%S]'

        loggingFormatter = logging.Formatter(loggingFormat, dateFormat)
        loggingHandler.setFormatter(loggingFormatter)

        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.setLevel(loggingLevel)
        self.logger.addHandler(loggingHandler)

        #Exit flag to notify threads to finish
        self.exitFlag = threading.Event()


        self.origSigIntHandler = signal.getsignal(signal.SIGINT)

        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        signal.signal(signal.SIGTERM, self.finishHandler)
        signal.signal(signal.SIGINT, self.finishHandler)


        #Creating Real Time Event Manager Thread
        self.rtEventMngr = rtevent.RtEventMngr(self.exitFlag)

        #Creating Message Receiver Thread
        self.msgReceiver = msgreceiver.MsgReceiver(self.exitFlag, self.rtEventMngr.toRtEventQueue)

        #Creating the Crud Resender Thread
        self.crudReSndr = crudresndr.CrudReSndr(self.exitFlag)

        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(self.exitFlag, self.msgReceiver.netToMsgRec,
                                       self.crudReSndr)

        #Creating CRUD Manager (This will run in main thread)
        self.crudMngr = crud.CrudMngr(self.exitFlag)
        
        #Creating and setting the ctrllermsger for crudMngr
        crudCtrllerMsger = ctrllermsger.CtrllerMsger(self.netMngr)
        self.crudMngr.ctrllerMsger = crudCtrllerMsger

        #Creating and setting the ctrllermsger for crudReSndr
        crudReSndrCtrllerMsger = ctrllermsger.CtrllerMsger(self.netMngr)
        self.crudReSndr.ctrllerMsger = crudReSndrCtrllerMsger

        #Creating and setting the ctrllermsger for msgReceiver
        msgReceiverCtrllerMsger = ctrllermsger.CtrllerMsger(self.netMngr)
        self.msgReceiver.ctrllerMsger = msgReceiverCtrllerMsger

        #Controller Alivness Checker
        self.lifeChecker = lifechecker.lifeChecker(self.exitFlag, self.rtEventMngr.toRtEventQueue)

        #self.origSigIntHandler = signal.getsignal(signal.SIGINT)

        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        #signal.signal(signal.SIGTERM, self.finishHandler)
        #signal.signal(signal.SIGINT, self.finishHandler)

        #By default our exit code will be success
        self.exitCode = 0


        



    def finishHandler(self, sigNum, frame):
        signal.signal(signal.SIGINT, self.origSigIntHandler)
        self.logger.debug('Notifying all threads to finish.')
        self.exitFlag.set()
        os.kill(os.getpid(),signal.SIGINT)





    def run(self):


        self.logger.debug('Starting Server Back End')

        #Starting "Real Time Event" thread
        self.rtEventMngr.start()

        #Starting "Message Receiver" thread
        self.msgReceiver.start()

        #Starting "CRUD Re Sender" thread
        self.crudReSndr.start()
        
        #Starting the "Event Manager" thread
        self.netMngr.start()

        #Starting "Life Checker Manager" thread
        self.lifeChecker.start()

        #Starting "CRUD Manager" It will run in main thread

        #In the common situation, the main thread is blocked in the execution
        #of werkzeug. On that situation if a SIGTERM signal arrives (Ctrl + C
        #or docker stop backend) seems that Werkzeug or Flask framework handle
        #the "KeyboardInterrupt" exception and the main thread is able to finish
        #the execution joining the rest of the threads.
        #When the backend starts without connection with database, the main thread
        #freezes in the connection to database and the Werkzeug server doesn't
        #reach to execute.
        #On this situation, when the SIGTERM arrives "KeyboardInterrupt" should be
        #handled by us. The only thing we have to do on this situation is to allow
        #it join the rest of the threads and to finish.
        try:
            self.crudMngr.run()
        except KeyboardInterrupt:
            pass

        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()


        self.logger.info('Now exiting main thread')
        sys.exit(self.exitCode)



    
backEndSrvr = BackEndSrvr()
backEndSrvr.run()

