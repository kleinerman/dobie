#!/usr/bin/env python3


import logging
import logging.handlers

import threading
import subprocess


import passage
import database
from config import *





class IoIface(object):

    def __init__(self, dataBase):

        #Getting the logger
        self.logger = logging.getLogger('Controller')

        #Database object
        #self.dataBase = dataBase

        #IoIface Proccess
        self.ioIfaceProc = None
        
        #Dictionary indexed by pssgId containing dictionaries with objects to control the passages 
        self.pssgsControl = None

        #Flag to know when the starterAlarmMngr or cleanerPssgMngr should abort and exit 
        self.pssgsReconfFlag = None





    #---------------------------------------------------------------------------#

    def start(self):
        '''
        Start the IO Interface process.
        Leave self.ioIfaceProc and self.pssgsControl with new objects.
        '''

        #Dictionary indexed by pssgId. Each pssg has a dictionry with all the pssg parametters indexed
        #by pssg parametters names

        self.dataBase = database.DataBase(DB_FILE)

        pssgsParams = self.dataBase.getPssgsParams()

        self.pssgsControl = {}
        for pssgId in pssgsParams.keys():
            self.pssgsControl[pssgId] = { #Passage object to manage the passage
                                         'pssgObj': passage.Passage(pssgsParams[pssgId]),
                                          #Event object to know when a passage was opened 
                                          #in a correct way by someone who has access
                                         'accessPermit': threading.Event(),
                                          #Lock and datetime object to know when the access
                                          #was opened
                                         'lockTimeAccessPermit': threading.Lock(),
                                         'timeAccessPermit': None,
                                          #Event object to know when the "cleanerPssgMngr" thread is alive
                                          #to avoid creating more than once
                                         'cleanerPssgMngrAlive': threading.Event(),
                                          #Event to know when the passage was opened
                                         'openPssg': threading.Event(),
                                          #Event object to know when the "starterAlrmMngrMngr" thread
                                          #is alive to avoid creating more than once
                                         'starterAlrmMngrAlive': threading.Event()
                                        }



        ioIfaceArgs = ''

        for pssgId in pssgsParams:

            for pssgParamName in self.dataBase.getPssgParamsNames():
                #Since not all the columns names of Passage table are parameters of 
                #ioiface binary, they should be checked if they are in the IOFACE_ARGS list
                if pssgParamName in IOIFACE_ARGS:
                    pssgParamValue = pssgsParams[pssgId][pssgParamName]
                    if pssgParamValue:
                        ioIfaceArgs += '--{} {} '.format(pssgParamName, pssgParamValue)




        ioIfaceCmd = '{} {}'.format(IOIFACE_BIN, ioIfaceArgs)

        logMsg = 'Starting IO Interface with the following command: {}'.format(ioIfaceCmd)
        self.logger.info(logMsg)

        self.ioIfaceProc = subprocess.Popen(ioIfaceCmd, shell=True, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.STDOUT
                                           )

        self.pssgsReconfFlag = threading.Event()



    #---------------------------------------------------------------------------#

    def stop(self):
        '''
        Launch Pssg Iface binary.
        Returns a process object
        '''
        if self.ioIfaceProc:
            self.logger.info('Stoping IO Interface.')
            self.ioIfaceProc.terminate()
        else:
            self.logger.info('IO Interface not running. Nothing to stop.')
            


    #----------------------------------------------------------------------------#



    def restart(self):
        '''
        '''
        self.stop()
        self.start()
