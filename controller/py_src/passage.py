import threading
import logging
import datetime
import time
import sys

import database
import queue

import genmngr
from config import *



class UnspecifiedGpio(Exception):
    pass


class Passage(object):
    '''
    This class has a dictionary with all the passage parameters as attribute.
    It also has methods to open and close a passage
    '''

    def __init__(self, pssgParams):

        #Getting the logger
        self.logger = logging.getLogger('Controller')
        
        self.pssgParams = pssgParams
        self.pssgId = pssgParams['id']




    def changeGpioState(self, gpioNumber, gpioState):
        '''
        It sends the signal to the corresponding GPIO to release the door
        '''

        gpioState = {True: '1', False: '0'}[gpioState]

        try:
            gpioFd = open('/sys/class/gpio/gpio{}/value'.format(gpioNumber),'w')
            gpioFd.write(gpioState + '\n')
            gpioFd.flush()
            gpioFd.close()

        except FileNotFoundError as fileNotFoundError:
            self.logger.error(fileNotFoundError)



    def release(self, trueOrFalse):
        '''
        It sends the signal to the corresponding GPIO to release or close the passage
        '''

        gpioNumber = self.pssgParams['rlseOut']

        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:
            logMsg = ('There is not GPIO set in DB to release or close the passage: {}.'
                      ''.format(self.pssgId)
                     )
            self.logger.error(logMsg)




    def startBzzr(self, trueOrFalse):
        '''
        It sends the signal to the corresponding GPIO to start or stop the buzzer
        '''

        gpioNumber = self.pssgParams['bzzrOut']

        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:

            logMsg = ('There is not GPIO set in DB to start or stop the buzzer in passage: {}.'
                      ''.format(self.pssgId)
                     )
            self.logger.error(logMsg)




class CleanerPssgMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''

    def __init__(self, pssgControl, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.

        self.pssgControl = pssgControl

        self.pssgId = pssgControl['pssgObj'].pssgParams['id']        

        super().__init__('CleanerPssgMngr_{}'.format(self.pssgId), exitFlag)

        self.pssgObj = pssgControl['pssgObj']

        self.cleanerPssgMngrAlive = pssgControl['cleanerPssgMngrAlive']

        self.lockTimeAccessPermit = pssgControl['lockTimeAccessPermit']

        #We can't do that because datetime type is inmmutable
#        self.timeAccessPermit = pssgControl['timeAccessPermit']

        self.rlseTime = pssgControl['pssgObj'].pssgParams['rlseTime']

        self.bzzrTime = pssgControl['pssgObj'].pssgParams['bzzrTime']


    def run(self):
        '''
        '''

        alive = True
        pssgReleased = True
        bzzrStarted = True

        while alive:

            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()
            
            with self.lockTimeAccessPermit:
                elapsedTime = datetime.datetime.now() - self.pssgControl['timeAccessPermit']
                
            elapsedTime = int(elapsedTime.total_seconds())
            print(elapsedTime, self.rlseTime)
            if pssgReleased and elapsedTime >= self.rlseTime:
                self.logger.debug("Unreleasing the passage {}.".format(self.pssgId))
                self.pssgObj.release(False)
                pssgReleased = False

            if bzzrStarted and elapsedTime >= self.bzzrTime:
                self.logger.debug("Stopping the buzzer on passage {}.".format(self.pssgId))
                self.pssgObj.startBzzr(False)
                bzzrStarted = False

            if not pssgReleased and not bzzrStarted:
                self.logger.debug("Finishing CleanerPssgMngr on passage {}".format(self.pssgId))
                alive = False

        self.cleanerPssgMngrAlive.clear()
        


        



