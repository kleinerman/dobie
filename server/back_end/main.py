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
from config import *





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

        #DataBase object 
        self.dbMngr = database.DbMngr(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        #Queue used to send Events and CRUD confirmation to dbMngr
        #netToDb = queue.Queue()

        #Creating the Net Manager Thread 
        self.netMngr = network.NetMngr(self.dbMngr, self.exitFlag)        


        #Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
        signal.signal(signal.SIGTERM, self.sigtermHandler)
        signal.signal(signal.SIGINT, self.sigtermHandler)

        #By default our exit code will be success
        self.exitCode = 0




    def sigtermHandler(self, signal, frame):
        self.logger.debug('Notifying all threads to finish.')
        self.exitFlag.set()





    def run(self):


        self.logger.debug('Starting Server Back End')
        
        #Starting the "Event Manager" thread
        self.netMngr.start()
        

        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()


        self.logger.info('Now exiting main thread')
        sys.exit(self.exitCode)



    
backEndSrvr = BackEndSrvr()
backEndSrvr.run()

