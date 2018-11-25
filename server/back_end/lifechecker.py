import pymysql
import logging
import re
import time

import genmngr
import database
from config import *


class lifeChecker(genmngr.GenericMngr):
    '''
    This thread has two responsibilities.
    It periodically check which controllers has some CRUD not yet 
    committed and send to them a RRC (Request to Re Provisioning) message.
    When a controller which now is alive answer to the previous message with a
    RRRE (Ready to Re Provisioning) message, this thread send the not comitted
    CRUDs to this controller.    
    '''

    def __init__(self, exitFlag, toRtEventQueue):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('LifeChecker', exitFlag)

        #Database object to answer the CRUDs not committed.
        #The creation of this object was moved to the run method to avoid
        #freezing the main thread when there is no connection to database.
        self.dataBase = None


        #Calculating the number of iterations before sending the message to request
        #re provisioning the controller.
        self.ITERATIONS = CONSIDER_DIED_MINS * 60 // EXIT_CHECK_TIME

        #This is the actual iteration. This value is incremented in each iteration
        #and is initializated to 0.
        self.iteration = 0


        self.toRtEventQueue = toRtEventQueue




    def run(self):
        '''
        Every CONSIDER_DIED_MINS minutes it checks in database if there are controllers
        which didn't send its corresponding keep alive message.
        It wakes up every EXIT_CHECK_TIME seconds to see if the main thread ask it to finish. 
        '''

        #First of all, the database should be connected by the execution of this thread
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)

        while True:
            #Blocking until EXIT_CHECK_TIME expires 
            time.sleep(EXIT_CHECK_TIME)
            self.checkExit()

            if self.iteration >= self.ITERATIONS:
                logMsg = 'Checking controller alivnesses.'
                self.logger.debug(logMsg)
                deadCtrllers = self.dataBase.setCtrllersNotReachable()
                for deadCtrller in deadCtrllers:
                    self.toRtEventQueue.put(deadCtrller)
                self.iteration = 0
            else:
                self.iteration += 1



                    



