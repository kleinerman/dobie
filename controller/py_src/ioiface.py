#!/usr/bin/env python3


import logging
import logging.handlers

import threading
import subprocess


import door
import database
from config import *





class IoIface(object):

    def __init__(self, dataBase):

        #Getting the logger
        self.logger = logging.getLogger('Controller')

        #IoIface Proccess
        self.ioIfaceProc = None
        
        self.dataBase = dataBase


    #---------------------------------------------------------------------------#

    def start(self):
        '''
        Start the IO Interface process.
        Leave self.ioIfaceProc and self.doorsControl with new objects.
        '''

        #In the followng section we generate the arguments to pass to the ioIface external program
        ioIfaceArgs = ''

        gpioNames = self.dataBase.getGpioNames()
        gpiosDoors = self.dataBase.getGpiosDoors()

        for gpiosDoor in gpiosDoors:
            for gpioName in gpioNames:
                gpioNumber = gpiosDoor[gpioName]
                if gpioNumber:
                    ioIfaceArgs += '--{} {} '.format(gpioName, gpioNumber)


        #With the arguments to pass to the ioIface program, it is lauched using Popen
        #and saving the process object to be able to kill it when a door is added, updated
        #or deleted.
        ioIfaceCmd = '{} {}'.format(IOIFACE_BIN, ioIfaceArgs)

        logMsg = 'Starting IO Interface with the following command: {}'.format(ioIfaceCmd)
        self.logger.info(logMsg)

        self.ioIfaceProc = subprocess.Popen(ioIfaceCmd, shell=True, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.STDOUT
                                           )



    #---------------------------------------------------------------------------#

    def stop(self):
        '''
        This method is called by crud thread when a door is added, updated or
        deleted.
        It set self.doorsReconfFlag to tell all the "cleanerDoorMngr" or "starterAlrmMngr"
        threads to finish when they are running
        '''

        if self.ioIfaceProc:
            self.logger.info('Stoping IO Interface.')
            #We comment the following line because when SIGTERM is received in the main python
            #program seems that the "ioiface" also receive that signal. If we send here the 
            #signal again, we do not permit "ioiface" finished in a clean way.
            #self.ioIfaceProc.terminate()
            #Wait until it finish (It does not finish instantly)
            try:
                self.ioIfaceProc.wait(timeout=IOIFACE_WAIT_FINISH_TIME)
                self.logger.debug('IO Interface stopped.')
            except subprocess.TimeoutExpired:
                self.logger.warning('IO Interface not responding. Nothing to stop.')
        else:
            self.logger.warning('IO Interface not running. Nothing to stop.')




    #----------------------------------------------------------------------------#

