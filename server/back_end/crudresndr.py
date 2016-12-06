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


class CrudReSndr(genmngr.GenericMngr):
    '''
    This thread has two responsibilities.
    It periodically check which controllers has some CRUD not yet 
    committed and send to them a RPR (Request to Re Provisioning) message.
    When a controller which now is alive answer to the previous message with a
    RRPR (Ready to Re Provisioning) message, this thread send the not comitted
    CRUDs to this controller.    
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudReSender', exitFlag)

        #Database object to answer the CRUDs not committed.
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        #Controller Messanger to resend the corresponding CRUDs.
        #As the "ctrllerMsger" use the only "netMngr" object and the "netMngr" has to
        #know this object to send the RRPR message. This attribute is setted after 
        #creating this object in the main thread.
        self.ctrllerMsger = None 
    
        #When the network thread receive a RRPR message it put the MAC of
        #the controller which sends this message in this queue
        self.netToCrudReSndr = queue.Queue()

        #Calculating the number of iterations before sending the message to request
        #re provisioning the controller.
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
        When a MAC address is received, this method send all the passages, access,
        limited access and persons CRUDs for this controller in this order to avoid
        inconsistency in the controller database.
        Also, after "self.ITERATIONS" times, it send a RRPR message to all the 
        controllers which have uncommitted CRUDs 
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
                    self.ctrllerMsger.requestReProvision(ctrllerMacsNotComm)
                    self.iteration = 0
                else:
                    self.iteration +=1

                    



