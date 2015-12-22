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
        
        self.pssgParams = pssgParams


    def release(self, trueOrFalse):
        '''
        It sends the signal to the corresponding GPIO to release the door
        '''

        gpioNumber = self.pssgParams['rlseOut']

        gpioValue = {True: '1', False: '0'}[trueOrFalse]
        
        if gpioNumber:
            gpioFd = open('/sys/class/gpio/gpio{}/value'.format(gpioNumber),'w')
            gpioFd.write(gpioValue + '\n')
            gpioFd.flush()
            gpioFd.close()

        else:
            raise UnspecifiedGpio





class CloserPssgMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''

    def __init__(self, pssgParams, pssgControl, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CloserPssgMngr_{}'.format(pssgParams['id']), exitFlag)

        self.closerPssgMngrAlive = pssgControl['closerPssgMngrAlive']

        self.lockTimeAccessPermit = pssgControl['lockTimeAccessPermit']

        self.timeAccessPermit = pssgControl['timeAccessPermit']

#        self.sleepTurns = pssgParams['rlseTime'] // EXIT_CHECK_TIME


    def run(self):
        '''
        '''

        alive = True
        while alive:

            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()
            
            with self.lockTimeAccessPermit:
                elapsedTime = datetime.datetime.now() - self.timeAccessPermit
                
            elapsedTime = int(elapsedTime.total_seconds())
            if elapsedTime > pssgParams['rlseTime']:
                alive = False


        



