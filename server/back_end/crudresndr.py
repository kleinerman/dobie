import pymysql
import queue
import logging
import json
import re
import time

import genmngr
import database
from config import *
from msgheaders import *
#import ctrllermsger


class CrudReSndr(genmngr.GenericMngr):
    '''
    This thread is created by the main thread.
    When the network thread receives a response from the controller confirmando que el 
    mismo esta vivo, el network thread nos deja un aviso en nuestra cola y desde aca disparamos
    reenvia de los crudes pendientes.
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudReSender', exitFlag)

        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        self.ctrllerMsger = None 
    
        self.netToCrudReSndr = queue.Queue()

        #Calculating the number of iterations before sending the message to verify
        #the controller is alive
        self.ITERATIONS = RE_SEND_TIME // EXIT_CHECK_TIME

        #This is the actual iteration. This value is incremented in each iteration
        #and is initializated to 0.
        self.iteration = 0




    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Network" thread.
        The queue message is the MAC address of the controller which need CRUDs to be
        resended.
        '''


        while True:
            try:
                #Blocking until Network thread sends an msg or EXIT_CHECK_TIME expires 
                ctrllerMac = self.netToCrudReSndr.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                for passage in self.dataBase.getUncmtPassages(ctrllerMac, database.TO_ADD):
                    self.ctrllerMsger.addPassage(ctrllerMac, passage)
                for passage in self.dataBase.getUncmtPassages(ctrllerMac, database.TO_UPDATE):
                    self.ctrllerMsger.updPassage(ctrllerMac, passage)
                for passage in self.dataBase.getUncmtPassages(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delPassage(ctrllerMac, passage['id'])
                self.checkExit()


                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_ADD):
                    #Get the person parameters as a dictionary
                    person = self.dataBase.getPerson(access['personId'])
                    #Adding to access dictionary necesary person parameters to add person if it doesn't
                    #exist in controller
                    access['cardNumber'] = person['cardNumber']
                    self.ctrllerMsger.addAccess(ctrllerMac, access)

                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_UPDATE):
                    access.pop('pssgId')
                    access.pop('personId')
                    access.pop('allWeek')
                    self.ctrllerMsger.updAccess(ctrllerMac, access)

                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delAccess(ctrllerMac, access['id'])
                self.checkExit()


                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_ADD):
                    #Get the person parameters as a dictionary
                    person = self.dataBase.getPerson(liAccess['personId'])
                    #Adding to access dictionary necesary person parameters to add person if it doesn't
                    #exist in controller
                    liAccess['cardNumber'] = person['cardNumber']
                    self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)

                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_UPDATE):
                    liAccess.pop('accessId')
                    liAccess.pop('personId')
                    liAccess.pop('pssgId')
                    self.ctrllerMsger.updLiAccess(ctrllerMac, liAccess)

                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delLiAccess(ctrllerMac, liAccess['id'])
                self.checkExit()



                for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_UPDATE):
                    self.ctrllerMsger.updPerson([ctrllerMac], person)
                for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delPerson([ctrllerMac], person['id'])
                self.checkExit()




            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()

                if self.iteration >= self.ITERATIONS:
                    logMsg = 'Sending "Verify Alive Message" to controllers'
                    self.logger.info(logMsg)
                    ctrllerMacsNotComm = self.dataBase.getUncmtCtrllerMacs()
                    self.ctrllerMsger.verifyIsAlive(ctrllerMacsNotComm)
                    self.iteration = 0
                else:
                    self.iteration +=1

                    



