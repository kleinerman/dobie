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
        self.logger = logging.getLogger(LOGGER_NAME)




    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        If true, call sys.exit and finish this thread
        '''
        #if (threading.current_thread() is not threading.main_thread()) and self.exitFlag.is_set():
        if self.exitFlag.is_set():
            logMsg = 'Exiting with code: {}'.format(self.exitCode)
            self.logger.info(logMsg)
            sys.exit(self.exitCode)


