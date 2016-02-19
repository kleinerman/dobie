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
        This method change a GPIO state. It receives the GPIO number and
        the state to put in the GPIO. The state can be True = 1 or False = 0
        '''

        gpioState = {True: '1', False: '0'}[gpioState]

        try:
            gpioFd = open('/sys/class/gpio/gpio{}/value'.format(gpioNumber),'w')
            gpioFd.write(gpioState + '\n')
            gpioFd.flush()
            gpioFd.close()

        except FileNotFoundError as fileNotFoundError:
            #When the GPIO doesn't exist, for example running it on standar PC,
            #this exception will happen and it will print a error log.
            self.logger.error(fileNotFoundError)



    def release(self, trueOrFalse):
        '''
        This method release or unrelase the passage. For example the magnet of a door.
        '''
        
        gpioNumber = self.pssgParams['rlseOut']

        #If the corresponding GPIO was not charged in database, "gpioNumber" will
        #be None and the method will print a log.
        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:
            logMsg = ('There is not GPIO set in DB to release or close the passage: {}.'
                      ''.format(self.pssgId)
                     )
            self.logger.error(logMsg)




    def startBzzr(self, trueOrFalse):
        '''
        This method start or stop the buzzer passage.
        '''

        gpioNumber = self.pssgParams['bzzrOut']

        #If the corresponding GPIO was not charged in database, "gpioNumber" will
        #be None and the method will print a log.        
        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:

            logMsg = ('There is not GPIO set in DB to start or stop the buzzer in passage: {}.'
                      ''.format(self.pssgId)
                     )
            self.logger.error(logMsg)




class CleanerPssgMngr(genmngr.GenericMngr):
    '''
    This thread stops the buzzer and close the passage. 
    It is created when the passage is opened. 
    It receives the times from the database.
    When the passage is opened more than once consecutively, the time is prolonged.    
    '''

    def __init__(self, pssgControl, exitFlag):

        #Dictionary with variables to control the passage
        self.pssgControl = pssgControl

        #Getting the pssgId for logging purpouses. It is got in this way 
        #to avoid passing it in constructor of the class.
        self.pssgId = pssgControl['pssgObj'].pssgParams['id']        

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CleanerPssgMngr_{}'.format(self.pssgId), exitFlag)

        #The following attributes are to manage this variables in a cleaner way.
        self.pssgObj = pssgControl['pssgObj']
        self.accessPermit = pssgControl['accessPermit']
        self.cleanerPssgMngrAlive = pssgControl['cleanerPssgMngrAlive']
        self.lockTimeAccessPermit = pssgControl['lockTimeAccessPermit']
        #We can't do the following, because datetime type is inmmutable
        #self.timeAccessPermit = pssgControl['timeAccessPermit']
        self.rlseTime = pssgControl['pssgObj'].pssgParams['rlseTime']
        self.bzzrTime = pssgControl['pssgObj'].pssgParams['bzzrTime']


    def run(self):
        '''
        This is the main method of the thread.
        It sleeps "EXIT_CHECK_TIME". Each time it awakes it calculates the time happened
        from the last access in the passage. According with that time, it stops the buzzer
        and/or close the passage. When both conditions happen, the thread finishes.
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

            if  elapsedTime >= self.rlseTime:
                self.logger.debug("Unreleasing the passage {}.".format(self.pssgId))
                self.pssgObj.release(False)
                pssgReleased = False
                #Once the passage was closed, if somebody opens the passage, will be 
                #considered an unpermitted access since the following event wil be cleared
                self.accessPermit.clear()

            #At the beginning the "if" was in the following way:
            #"if bzzrStarted and elapsedTime >= self.bzzrTime" to avoid calculating time
            #in each iteration, but then we have to remove the first part of the "if" because
            #sometimes when the buzzer was stopped and the passage was not closed yet and in 
            #this moment someone passes again, the buzzer was started again and it will never
            #be cleared since the "bzzrStarted" variable was set to "False"
            #The same could happen with "rlseTime" if it will be lesser than "bzzrTime".

            if  elapsedTime >= self.bzzrTime:
                self.logger.debug("Stopping the buzzer on passage {}.".format(self.pssgId))
                self.pssgObj.startBzzr(False)
                bzzrStarted = False

            #The situation explained in the previous comment will produce that once "bzzrStarted"
            #was set to False, it will never be set to True altough the passage was opened again
            #before completing the rlseTime. But it doesnt matter and the following if will be valid
            #to determinate when the thread have to died.
            #The same could happen with "rlseTime" if it will be lesser than "bzzrTime".

            if not pssgReleased and not bzzrStarted:
                self.logger.debug("Finishing CleanerPssgMngr on passage {}".format(self.pssgId))
                alive = False

        #Notifying that this thread has died
        self.cleanerPssgMngrAlive.clear()
        


        

class StarterAlrmMngr(genmngr.GenericMngr):
    '''
    This thread starts the buzzer when the passage remains opened  
    for more than 
    It receives the times from the database.
    When the passage is opened more than once consecutively, the time is prolonged.    
    '''

    def __init__(self, pssgControl, exitFlag):

        #Dictionary with variables to control the passage
        self.pssgControl = pssgControl

        #Getting the pssgId for logging purpouses. It is got in this way 
        #to avoid passing it in constructor of the class.
        self.pssgId = pssgControl['pssgObj'].pssgParams['id']

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('StarterAlrmMngr_{}'.format(self.pssgId), exitFlag)

        #The following attributes are to manage this variables in a cleaner way.
        self.pssgObj = pssgControl['pssgObj']
        self.starterAlrmMngrAlive = pssgControl['starterAlrmMngrAlive']
        self.lockTimeAccessPermit = pssgControl['lockTimeAccessPermit']
        #We can't do the following, because datetime type is inmmutable
        #self.timeAccessPermit = pssgControl['timeAccessPermit']
        self.alrmTime = pssgControl['pssgObj'].pssgParams['alrmTime']
        self.openPssg = pssgControl['openPssg']


    def run(self):
        '''
        This is the main method of the thread.
        It sleeps "EXIT_CHECK_TIME". Each time it awakes it calculates the time happened
        from the last access in the passage. If that time is greater than "alrmTime",
        it turns on the buzzer acting as an alarm
        '''

        alive = True

        while alive and self.openPssg.is_set():

            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()

            with self.lockTimeAccessPermit:
                elapsedTime = datetime.datetime.now() - self.pssgControl['timeAccessPermit']

            elapsedTime = int(elapsedTime.total_seconds())

            if elapsedTime >= self.alrmTime:
                self.logger.debug("Starting the alarm on passage {}.".format(self.pssgId))
                self.pssgObj.startBzzr(True)
                alive = False

        #Notifying that this thread has died
        self.starterAlrmMngrAlive.clear()




