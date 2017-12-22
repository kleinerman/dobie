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
    committed and send to them a RRC (Request to Re Provisioning) message.
    When a controller which now is alive answer to the previous message with a
    RRRE (Ready to Re Provisioning) message, this thread send the not comitted
    CRUDs to this controller.    
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudReSender', exitFlag)

        #Database object to answer the CRUDs not committed.
        #The creation of this object was moved to the run method to avoid
        #freezing the main thread when there is no connection to database.
        self.dataBase = None

        #Controller Messanger to resend the corresponding CRUDs.
        #As the "ctrllerMsger" use the only "netMngr" object and the "netMngr" has to
        #know this object to send the RRRE message. This attribute is setted after 
        #creating this object in the main thread.
        self.ctrllerMsger = None 
    
        #When the network thread receive a RRRE message it put the MAC of
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
        When a MAC address is received, this method send all the doors, access,
        limited access and persons CRUDs for this controller in this order to avoid
        inconsistency in the controller database.
        Also, after "self.ITERATIONS" times, it send a RRRE message to all the 
        controllers which have uncommitted CRUDs 
        '''

        #First of all, the database should be connected by the execution of this thread
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)

        while True:
            try:
                #Blocking until Network thread sends an msg or EXIT_CHECK_TIME expires 
                ctrllerMac = self.netToCrudReSndr.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_ADD):
                    door.pop('name')
                    door.pop('controllerId')
                    door.pop('zoneId')
                    self.ctrllerMsger.addDoor(ctrllerMac, door)
                for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_UPDATE):
                    door.pop('name')
                    door.pop('controllerId')
                    door.pop('zoneId')
                    self.ctrllerMsger.updDoor(ctrllerMac, door)
                for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delDoor(ctrllerMac, door['id'])
                self.checkExit()

                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_ADD):
                    #"cardNumber" parameter is not present in access dictionary, but should be sent
                    #when sending a CRUD access to controller.
                    #Get the person parameters as a dictionary.
                    person = self.dataBase.getPerson(access['personId'])
                    #Adding "cardNumber" to access dictionary.
                    access['cardNumber'] = person['cardNumber']
                    self.ctrllerMsger.addAccess(ctrllerMac, access)

                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_UPDATE):
                    #The following parameters should not be sent when updating an access.
                    access.pop('doorId')
                    access.pop('personId')
                    access.pop('allWeek')
                    self.ctrllerMsger.updAccess(ctrllerMac, access)

                for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delAccess(ctrllerMac, access['id'])
                self.checkExit()


                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_ADD):
                    #"cardNumber" parameter is not present in liAccess dictionary, but should be sent
                    #when sending a CRUD liAccess to controller.
                    #Get the person parameters as a dictionary.
                    person = self.dataBase.getPerson(liAccess['personId'])
                    #Adding "cardNumber" to liAccess dictionary.
                    liAccess['cardNumber'] = person['cardNumber']
                    self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)

                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_UPDATE):
                    #The following parameters should not be sent when updating an access.
                    liAccess.pop('accessId')
                    liAccess.pop('personId')
                    liAccess.pop('doorId')
                    self.ctrllerMsger.updLiAccess(ctrllerMac, liAccess)

                for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_DELETE):
                    self.ctrllerMsger.delLiAccess(ctrllerMac, liAccess['id'])
                self.checkExit()


                #Persons never colud be in state TO_ADD. For this reason,
                #only TO_UPDATE or TO_DELETE state is retrieved
                for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_UPDATE):
                    person.pop('name')
                    person.pop('orgId')
                    person.pop('visitedOrgId')
                    #"updPerson" method receive a list of MAC addresses to update. Because in this case only one
                    #controller is being updated, a list with only the MAC address of the controller is created.
                    self.ctrllerMsger.updPerson([ctrllerMac], person)
                for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_DELETE):
                    #"delPerson" method receive a list of MAC addresses to update. Because in this case only one
                    #controller is being updated, a list with only the MAC address of the controller is created.
                    self.ctrllerMsger.delPerson([ctrllerMac], person['id'])
                self.checkExit()




            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()

                if self.iteration >= self.ITERATIONS:
                    logMsg = 'Checking if there are controllers which need to be re provisioned.'
                    self.logger.debug(logMsg)
                    #Getting the MAC addresses of controllers which has uncommitted CRUDs.
                    ctrllerMacsNotComm = self.dataBase.getUncmtCtrllerMacs()
                    if ctrllerMacsNotComm:
                        logMsg = 'Sending Request Re Provision Message to: {}'.format(', '.join(ctrllerMacsNotComm))
                        self.logger.info(logMsg)
                        self.ctrllerMsger.requestReSendCruds(ctrllerMacsNotComm)
                    self.iteration = 0
                else:
                    self.iteration +=1

                    



