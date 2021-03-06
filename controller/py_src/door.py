import threading
import logging
import datetime
import time
import sys

import database
import queue

import genmngr
from config import *




class Door(object):
    '''
    This class has a dictionary with all the door parameters as attribute.
    It also has methods to open and close a door
    '''

    def __init__(self, params):

        #Getting the logger
        self.logger = logging.getLogger('Controller')
        
        self.params = params
        self.doorId = params['id']




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
        This method release or unrelase the door. For example the magnet of a door.
        '''
        
        gpioNumber = self.params['rlseOut']

        #If the corresponding GPIO was not charged in database, "gpioNumber" will
        #be None and the method will print a log.
        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:
            logMsg = ('There is not GPIO set in DB to release or close the door: {}.'
                      ''.format(self.doorId)
                     )
            self.logger.error(logMsg)




    def startBzzr(self, trueOrFalse):
        '''
        This method start or stop the buzzer door.
        '''

        gpioNumber = self.params['bzzrOut']

        #If the corresponding GPIO was not charged in database, "gpioNumber" will
        #be None and the method will print a log.        
        if gpioNumber:
            self.changeGpioState(gpioNumber, trueOrFalse)
        else:

            logMsg = ('There is not GPIO set in DB to start or stop the buzzer in door: {}.'
                      ''.format(self.doorId)
                     )
            self.logger.error(logMsg)




class CleanerDoorMngr(genmngr.GenericMngr):
    '''
    This thread stops the buzzer and close the door. 
    It is created when the door is opened. 
    It receives the times from the database.
    When the door is opened more than once consecutively, the time is prolonged.    
    '''

    def __init__(self, doorControl, exitFlag):

        #Dictionary with variables to control the door
        self.doorControl = doorControl

        #Getting the doorId for logging purpouses. It is got in this way 
        #to avoid passing it in constructor of the class.
        self.doorId = doorControl['doorObj'].params['id']

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CleanerDoorMngr_{}'.format(self.doorId), exitFlag)

        #The following attributes are to manage this variables in a cleaner way.
        self.doorObj = doorControl['doorObj']
        self.accessPermit = doorControl['accessPermit']
        self.cleanerDoorMngrAlive = doorControl['cleanerDoorMngrAlive']
        self.lockTimeAccessPermit = doorControl['lockTimeAccessPermit']
        #We can't do the following, because datetime type is inmmutable
        #self.timeAccessPermit = doorControl['timeAccessPermit']
        self.rlseTime = doorControl['doorObj'].params['rlseTime']
        self.bzzrTime = doorControl['doorObj'].params['bzzrTime']


    def run(self):
        '''
        This is the main method of the thread.
        It sleeps "EXIT_CHECK_TIME". Each time it awakes it calculates the time happened
        from the last access in the door. According with that time, it stops the buzzer
        and/or close the door. When both conditions happen, the thread finishes.
        '''

        alive = True

        while alive:

            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()
            
            with self.lockTimeAccessPermit:
                elapsedTime = datetime.datetime.now() - self.doorControl['timeAccessPermit']
                
            elapsedTime = int(elapsedTime.total_seconds())

            if  elapsedTime >= self.rlseTime:
                #relocking the door if it shouldn't be kept unlocked by schedule
                if not self.doorControl['unlkedBySkd'].is_set():
                    self.logger.debug("Locking door {}.".format(self.doorId))
                    self.doorObj.release(False)
                #Once the door was closed, if somebody opens the door, will be 
                #considered an unpermitted access since the following event wil be cleared
                self.accessPermit.clear()

            #At the beginning the "if" was in the following way:
            #"if bzzrStarted and elapsedTime >= self.bzzrTime" to avoid calculating time
            #in each iteration, but then we have to remove the first part of the "if" because
            #sometimes when the buzzer was stopped and the door was not closed yet and in 
            #this moment someone passes again, the buzzer was started again and it will never
            #be cleared since the "bzzrStarted" variable was set to "False"
            #The same could happen with "rlseTime" if it will be lesser than "bzzrTime".

            if  elapsedTime >= self.bzzrTime:
                self.logger.debug("Stopping the buzzer on door {}.".format(self.doorId))
                self.doorObj.startBzzr(False)

            if elapsedTime >= self.rlseTime and elapsedTime >= self.bzzrTime:
                self.logger.debug("Finishing CleanerDoorMngr on door {}".format(self.doorId))
                alive = False

        #Notifying that this thread has died
        self.cleanerDoorMngrAlive.clear()
        


        

class StarterAlrmMngr(genmngr.GenericMngr):
    '''
    This thread starts the buzzer when the door remains opened  
    for more than 
    It receives the times from the database.
    When the door is opened more than once consecutively, the time is prolonged.    
    '''

    def __init__(self, doorControl, toEvent, exitFlag):

        #Dictionary with variables to control the door
        self.doorControl = doorControl

        #Queue to send events to Event Manager when the alarm start
        self.toEvent = toEvent

        #Getting the doorId for logging purpouses. It is got in this way 
        #to avoid passing it in constructor of the class.
        self.doorId = doorControl['doorObj'].params['id']

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('StarterAlrmMngr_{}'.format(self.doorId), exitFlag)

        #The following attributes are to manage this variables in a cleaner way.
        self.doorObj = doorControl['doorObj']
        self.starterAlrmMngrAlive = doorControl['starterAlrmMngrAlive']
        self.lockTimeAccessPermit = doorControl['lockTimeAccessPermit']
        #We can't do the following, because datetime type is inmmutable
        #self.timeAccessPermit = doorControl['timeAccessPermit']
        self.alrmTime = doorControl['doorObj'].params['alrmTime']
        self.openDoor = doorControl['openDoor']


    def run(self):
        '''
        This is the main method of the thread.
        It sleeps "EXIT_CHECK_TIME". Each time it awakes it calculates the time happened
        from the last access in the door. If that time is greater than "alrmTime",
        it turns on the buzzer acting as an alarm
        '''

        alive = True

        while alive and self.openDoor.is_set():

            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()

            with self.lockTimeAccessPermit:
                nowDateTime = datetime.datetime.now()
                elapsedTime = nowDateTime - self.doorControl['timeAccessPermit']

            elapsedTime = int(elapsedTime.total_seconds())

            if elapsedTime >= self.alrmTime:
                self.logger.debug("Starting the alarm on door {}.".format(self.doorId))
                self.doorObj.startBzzr(True)


                dateTime = nowDateTime.strftime('%Y-%m-%d %H:%M')
                event = {'doorId' : self.doorId,
                         'eventTypeId' : EVT_REMAIN_OPEN,
                         'dateTime' : dateTime,
                         'doorLockId' : None,
                         'cardNumber' : None,
                         'side' : None,
                         'allowed' : None,
                         'denialCauseId' : None
                        }
                #Sending the event to the "Event Manager" thread
                self.toEvent.put(event)

                alive = False

        #Notifying that this thread has died
        self.starterAlrmMngrAlive.clear()



class DoorNotConfigured(Exception):
    pass



class DoorsControl(object):

    def __init__(self):

        #Getting the logger
        self.logger = logging.getLogger('Controller')

        #Dictionary indexed by doorNum containing dictionaries with objects to control the doors 
        self.params = None


    #---------------------------------------------------------------------------#



    def loadParams(self):
        '''
        This method load door params from DB in "params" dictionary.
        This method is called when the main program starts or when a CRUD of
        door is received. 
        '''


        #Database connection should be done here and can not be done in the constructor
        #since this method is run by the mainThread and also run by crud thread when
        #a door is added, updated or deleted.
        dataBase = database.DataBase(DB_FILE)


        #List with sqlite dictionary objects. Each dictionary has the door parameters
        paramsDoors = dataBase.getParamsDoors()

        #The following structure is a dict indexed by the doorNums. Each value is another dict
        #with object, event and variables to control each door. Each time a door is added,
        #updated or deleted, this structure should be regenerated.
        self.params = {}
        for paramsDoor in paramsDoors:
            self.params[paramsDoor['doorNum']] = {'doorId': paramsDoor['id'],
                                                  #Door object to manage the door
                                                  'doorObj': Door(paramsDoor),
                                                  #Event object to know when a door was opened 
                                                  #in a correct way by someone who has access
                                                  'accessPermit': threading.Event(),
                                                  #Lock and datetime object to know when the access
                                                  #was opened
                                                  'lockTimeAccessPermit': threading.Lock(),
                                                  'timeAccessPermit': None,
                                                  #Event object to know when the "cleanerDoorMngr" thread is alive
                                                  #to avoid creating more than once
                                                  'cleanerDoorMngrAlive': threading.Event(),
                                                  #Event to know when the door was opened
                                                  'openDoor': threading.Event(),
                                                  #Event object to know when the "starterAlrmMngrMngr" thread
                                                  #is alive to avoid creating more than once
                                                  'starterAlrmMngrAlive': threading.Event(),
                                                  #Event to know when the door was unlocked by schedule
                                                  'unlkedBySkd': threading.Event()
                                                 }


    def getDoorId(self, doorNum):
        '''
        Return the doorId receiving the doorNum.
        '''

        try:
            return self.params[doorNum]['doorId']
        except KeyError:
            raise DoorNotConfigured


    def getDoorNum(self, doorId):
        '''
        Return the doorNum receiving the doorId.
        '''

        for doorNum, doorParams in self.params.items():
            if doorParams['doorId'] == doorId:
                return doorNum
        raise DoorNotConfigured




class UnlkDoorSkdMngr(genmngr.GenericMngr):
    '''
    This thread opens and closes all the doors of the controller
    using the information retrieved from OpenDoorsSkd table. 
    It generates events when the door change the state.
    '''


    def __init__(self, toEvent, lockDoorsControl, doorsControl, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('UnlkDoorSkdMngr', exitFlag)

        #Queue to send events to Event Manager thread
        self.toEvent = toEvent

        #When receiving a door CRUD is necessary to re launch the ioiface proccess.
        #For this reason it is necessary a reference to "ioIface" object.
        self.lockDoorsControl = lockDoorsControl
        self.doorsControl = doorsControl



        #Calculating the number of iterations before sending the message to request
        #re provisioning the controller.
        self.ITERATIONS = CHECK_OPEN_DOORS_MINS * 60 // EXIT_CHECK_TIME

        #This is the actual iteration. This value is incremented in each iteration
        #and is initializated to 0.
        self.iteration = 0





    def run(self):
        '''
        Every CONSIDER_DIED_MINS minutes it checks in database if there are controllers
        which didn't send its corresponding keep alive message.
        It wakes up every EXIT_CHECK_TIME seconds to see if the main thread ask it to finish. 
        '''

        #First of all, the database should be connected by the execution of this thread
        dataBase = database.DataBase(DB_FILE)


        while True:
            #Blocking until EXIT_CHECK_TIME expires 
            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()

            if self.iteration >= self.ITERATIONS:
                logMsg = 'Checking Unlock Door Schedule.'
                self.logger.debug(logMsg)
                self.iteration = 0

                with self.lockDoorsControl:

                    doorsToUnlkBySkd = dataBase.getDoorsToUnlkBySkd()
                    for doorNum in self.doorsControl.params:
                        doorControl = self.doorsControl.params[doorNum]
                        doorId = doorControl['doorId']

                        if doorId in doorsToUnlkBySkd and not doorControl['unlkedBySkd'].is_set():
                            logMsg = 'Door: {} is opened by schedule'.format(doorId)
                            self.logger.debug(logMsg)
                            doorControl['unlkedBySkd'].set()
                            doorControl['doorObj'].release(True)

                            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                            event = {'doorId' : doorId,
                                     'eventTypeId' : EVT_OPEN_SKD,
                                     'dateTime' : dateTime,
                                     'doorLockId' : None,
                                     'cardNumber' : None,
                                     'side' : None,
                                     'allowed' : None,
                                     'denialCauseId' : None
                                    }
                            self.toEvent.put(event)


                        elif doorId not in doorsToUnlkBySkd and doorControl['unlkedBySkd'].is_set():
                            logMsg = 'Door: {} is closed by schedule'.format(doorId)
                            self.logger.debug(logMsg)
                            doorControl['unlkedBySkd'].clear()
                            doorControl['doorObj'].release(False)

                            dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                            event = {'doorId' : doorId,
                                     'eventTypeId' : EVT_CLOSE_SKD,
                                     'dateTime' : dateTime,
                                     'doorLockId' : None,
                                     'cardNumber' : None,
                                     'side' : None,
                                     'allowed' : None,
                                     'denialCauseId' : None
                                    }
                            self.toEvent.put(event)

            else:
                self.iteration += 1





