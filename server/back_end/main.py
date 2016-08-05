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
import crud
from config import *

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

        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(self.exitFlag)        

        #Creating CRUD Manager (This will run in main thread)
        self.crudMngr = crud.CrudMngr(self.netMngr)


        self.origSigIntHandler = signal.getsignal(signal.SIGINT)

        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        signal.signal(signal.SIGTERM, self.finishHandler)
        signal.signal(signal.SIGINT, self.finishHandler)

        #By default our exit code will be success
        self.exitCode = 0


        



    def finishHandler(self, sigNum, frame):
        signal.signal(signal.SIGINT, self.origSigIntHandler)
        self.logger.debug('Notifying all threads to finish.')
        self.exitFlag.set()
        os.kill(os.getpid(),signal.SIGINT)





    def run(self):


        self.logger.debug('Starting Server Back End')
        
        #Starting the "Event Manager" thread
        self.netMngr.start()

        #Starting "CRUD Manager" It will run in main thread
        self.crudMngr.run()

        

        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()


        self.logger.info('Now exiting main thread')
        sys.exit(self.exitCode)



    
backEndSrvr = BackEndSrvr()
backEndSrvr.run()

