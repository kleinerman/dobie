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

        #IoIface Output
        self.ioIfaceStdOut = None


        self.dataBase = dataBase


    #---------------------------------------------------------------------------#

    def start(self):
        '''
        Start the IO Interface process.
        Leave self.ioIfaceProc and self.doorsControl with new objects.
        '''
        #In the followng section we put all the arguments to pass to ioIface external
        #program in a list, including and starting by the name of the program
        ioIfaceArgs = [IOIFACE_BIN]

        gpiosDoors = self.dataBase.getGpiosDoors()

        for gpiosDoor in gpiosDoors:
            doorNum = str(gpiosDoor['id'])
            iRdrBits = str(gpiosDoor['iWgndBits'])
            i0In = str(gpiosDoor['i0In'])
            i1In = str(gpiosDoor['i1In'])
            oRdrBits = str(gpiosDoor['oWgndBits'])
            o0In = str(gpiosDoor['o0In'])
            o1In = str(gpiosDoor['o1In'])
            bttnIn = str(gpiosDoor['bttnIn'])
            stateIn = str(gpiosDoor['stateIn'])
            rlseOut = str(gpiosDoor['rlseOut'])
            bzzrOut = str(gpiosDoor['bzzrOut'])
            doorArgs = ['--id', doorNum, '--inRdrIn', iRdrBits, i0In, i1In,
                        '--outRdrIn', oRdrBits, o0In, o1In, '--bttnIn', bttnIn,
                        '--stateIn', stateIn, '--rlseOut', rlseOut, '--bzzrOut', bzzrOut,
                       ]
            ioIfaceArgs += doorArgs

        #The ioIface external program is launched using Popen
        #and saving the process object.
        ioIfaceCmd = ' '.join(ioIfaceArgs)
        logMsg = 'Starting IO Interface with the following command: {}'.format(ioIfaceCmd)
        self.logger.info(logMsg)

        self.ioIfaceStdOut = open(IOFACE_LOGGING_FILE, 'w')

        self.ioIfaceProc = subprocess.Popen(ioIfaceArgs,
                                            stdout=self.ioIfaceStdOut,
                                            stderr=subprocess.STDOUT,
                                            bufsize=0
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
            self.logger.info('Closing IoIface StdOut File.')
            self.ioIfaceStdOut.close()
            try:
                self.ioIfaceProc.wait(timeout=IOIFACE_WAIT_FINISH_TIME)
                self.logger.debug('IO Interface stopped.')
            except subprocess.TimeoutExpired:
                self.logger.warning('IO Interface not responding. Nothing to stop.')
        else:
            self.logger.warning('IO Interface not running. Nothing to stop.')




    #----------------------------------------------------------------------------#
