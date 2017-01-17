#!/usr/bin/env python3


import logging
import logging.handlers

import threading
import subprocess


import passage
import database
from config import *





class IoIface(object):

    def __init__(self):

        #Getting the logger
        self.logger = logging.getLogger('Controller')

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

        #Database connection should be done here and can not be done in the constructor
        #since this method is run by the mainThread and also run by crud thread when
        #a passage is added, updated or deleted.
        dataBase = database.DataBase(DB_FILE)


        #Dictionary indexed by pssgId. Each pssg has a dictionry with all the pssg parametters indexed
        #by pssg parametters names
        pssgsParams = dataBase.getPssgsParams()

        #The following structure is a dict indexed by the pssgIds. Each value is another dict
        #with object, event and variables to control each passage. Each time a passage is added,
        #updated or deleted, this structure should be regenerated and all the thread running for 
        #the passage like "cleanerPssgMngr" or "starterAlrmMngr" should be killed.
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



        #In the followng section we generate the arguments to pass to the ioIface external program
        ioIfaceArgs = ''

        for pssgId in pssgsParams:

            for pssgParamName in dataBase.getPssgParamsNames():
                #Since not all the columns names of Passage table are parameters of 
                #ioiface binary, they should be checked if they are in the IOFACE_ARGS list
                if pssgParamName in IOIFACE_ARGS:
                    pssgParamValue = pssgsParams[pssgId][pssgParamName]
                    if pssgParamValue:
                        ioIfaceArgs += '--{} {} '.format(pssgParamName, pssgParamValue)



        #With the arguments to pass to the ioIface program, it is lauched using Popen
        #and saving the process object to be able to kill it when a passage is added, updated
        #or deleted.
        ioIfaceCmd = '{} {}'.format(IOIFACE_BIN, ioIfaceArgs)

        logMsg = 'Starting IO Interface with the following command: {}'.format(ioIfaceCmd)
        self.logger.info(logMsg)

        self.ioIfaceProc = subprocess.Popen(ioIfaceCmd, shell=True, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.STDOUT
                                           )

        #This event variable is passed to "cleanerPssgMngr" or "starterAlrmMngr" when they
        #are created from the main thread.
        #When an passage is added, updated or deleted, the crud thread will set this variable
        #and the above threads will know that should finish.
        self.pssgsReconfFlag = threading.Event()




    #---------------------------------------------------------------------------#

    def stop(self):
        '''
        This method is called by crud thread when a passage is added, updated or
        deleted.
        It set self.pssgsReconfFlag to tell all the "cleanerPssgMngr" or "starterAlrmMngr"
        threads to finish when they are running
        '''

        self.pssgsReconfFlag.set()

        if self.ioIfaceProc:
            self.logger.info('Stoping IO Interface.')
            #Ask ioIface external program to finish (sending SIGTERM signal)
            self.ioIfaceProc.terminate()
            #Wait until it finish (It does not finish instantly). If we do not
            #wait, we end launching "ioIface" before the previous finish and a mess happen
            self.ioIfaceProc.wait()
        else:
            self.logger.info('IO Interface not running. Nothing to stop.')




    #----------------------------------------------------------------------------#

    def restart(self):
        '''
        This method call stop and start secuentially
        '''
        self.stop()
        self.start()
