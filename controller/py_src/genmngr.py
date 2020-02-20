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
        If true, before calling sys.exit and finish this thread, check if
        the thread has DB connecion. When it has DB connecion, close it
        before exiting. This is done in this way because in the past close
        method has to be called by the same thread who created the connection.

        '''

        if self.exitFlag.is_set():
            try:
                if self.dataBase != None:
                    self.logger.info("Closing DB connection.")
                    self.dataBase.connection.close()
                else:
                    logMsg = "DB connection wasn't established yet on this thread"
                    self.logger.info(logMsg)
            except AttributeError:
                self.logger.debug("This thread hasn't DB connection.")

            logMsg = 'Exiting with code: {}'.format(self.exitCode)
            self.logger.info(logMsg)
            sys.exit(self.exitCode)


