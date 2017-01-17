import threading
import logging
import datetime
import time
import sys

import database
import queue

from config import *




class GenericMngr(threading.Thread):

    '''
    Generic Thread Manager to create NetMngr, EventMngr and ReSender
    '''

    def __init__(self, threadName, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__(name = threadName, daemon = True)
        
        #Flag to see know when the Main thread ask as to finish
        self.exitFlag = exitFlag

        #Thread exit code
        self.exitCode = 0

        #Getting the logger
        self.logger = logging.getLogger('Controller')




    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        If true, call sys.exit and finish this thread
        '''
        if self.exitFlag.is_set():
            logMsg = 'Exiting with code: {}'.format(self.exitCode)
            self.logger.info(logMsg)
            sys.exit(self.exitCode)




class PssgMngr(GenericMngr):

    '''
    Generic Thread Manager to create starterAlarmMngr and cleanerPssgMngr
    threads. This thread inherits from "GenericMngr". It differs from his
    parent receiving "pssgsReconfFlag" in the constructor, and overwriting
    "checkExit" method, checking this flag and "exitFlag" as well.
    '''

    def __init__(self, threadName, pssgsReconfFlag, exitFlag):

        #Invoking the parent class constructor.
        super().__init__(threadName, exitFlag)
    
        #Flag to know when the starterAlarmMngr or cleanerPssgMngr should exit
        #This will happen when a new passage is added, updated or deleted and 
        #and we should kill all the existing "starterAlarmMngr" or/and 
        #"cleanerPssgMngr" running.
        self.pssgsReconfFlag = pssgsReconfFlag



    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        or crud thread ask this thread to exit using pssgsReconfFlag. 
        If true, call sys.exit and finish this thread
        '''

        if self.exitFlag.is_set() or self.pssgsReconfFlag.is_set():
            logMsg = 'Exiting with code: {}'.format(self.exitCode)
            self.logger.info(logMsg)
            sys.exit(self.exitCode)
