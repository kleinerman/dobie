import pymysql
import queue
import logging
import json
import re
import time
import threading

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

        #When the network thread receives a RRRC message it puts the
        #MAC of the controller which sent this message in this queue.
        #Also, MsgReceiver thread can put the MAC of the controller
        #which need to be re-provisioned here.
        self.toCrudReSndr = queue.Queue()

        #Calculating the number of iterations before sending the message to request
        #re provisioning the controller.
        self.ITERATIONS = RE_SEND_TIME // EXIT_CHECK_TIME

        #This is the actual iteration. This value is incremented in each iteration
        #and is initializated to 0.
        self.iteration = 0

        #Lock to protect self.iteration attribute
        self.lockIteration = threading.Lock()



    def resetReSendTime(self):
        '''
        This method will be executed by network thread reseting the iterations
        everytime the network thread sends a message to the controller.
        This is to avoid "CrudReSender" thread resends CRUDs when a CRUD
        message has just been sent to the controller and the controller
        didn't answer yet.
        '''

        #self.iteration is protected with self.lockIteration lock as it is
        #modified by this thread (CrudReSender) and by NetMngr Thread
        with self.lockIteration:
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
                ctrllerMac = self.toCrudReSndr.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()

                try:
                    for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_ADD):
                        door.pop('name')
                        door.pop('controllerId')
                        door.pop('zoneId')
                        door.pop('isVisitExit')
                        self.ctrllerMsger.addDoor(ctrllerMac, door)
                    for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_UPDATE):
                        door.pop('name')
                        door.pop('controllerId')
                        door.pop('zoneId')
                        door.pop('isVisitExit')
                        self.ctrllerMsger.updDoor(ctrllerMac, door)
                    for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delDoor(ctrllerMac, door['id'])
                    self.checkExit()


                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addUnlkDoorSkd(ctrllerMac, unlkDoorSkd)
                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_UPDATE):
                        unlkDoorSkd.pop('doorId')
                        self.ctrllerMsger.updUnlkDoorSkd(ctrllerMac, unlkDoorSkd)
                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delUnlkDoorSkd(ctrllerMac, unlkDoorSkd['id'])
                    self.checkExit()


                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addExcDayUds(ctrllerMac, excDayUds)
                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_UPDATE):
                        excDayUds.pop('doorId')
                        self.ctrllerMsger.updExcDayUds(ctrllerMac, excDayUds)
                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delExcDayUds(ctrllerMac, excDayUds['id'])
                    self.checkExit()


                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addAccess(ctrllerMac, access)
                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_UPDATE):
                        #The following parameters should not be sent when updating an access.
                        access.pop('doorId')
                        access.pop('personId')
                        access.pop('allWeek')
                        access.pop('cardNumber')
                        self.ctrllerMsger.updAccess(ctrllerMac, access)
                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delAccess(ctrllerMac, access['id'])
                    self.checkExit()


                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)
                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_UPDATE):
                        #The following parameters should not be sent when updating an access.
                        liAccess.pop('accessId')
                        liAccess.pop('doorId')
                        liAccess.pop('personId')
                        liAccess.pop('cardNumber')
                        self.ctrllerMsger.updLiAccess(ctrllerMac, liAccess)
                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delLiAccess(ctrllerMac, liAccess['id'])
                    self.checkExit()


                    #Persons never colud be in state TO_ADD. For this reason,
                    #only TO_UPDATE or TO_DELETE state is retrieved
                    for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_UPDATE):
                        person.pop('names')
                        person.pop('lastName')
                        person.pop('orgId')
                        person.pop('visitedOrgId')
                        person.pop('isProvider')
                        #"updPerson" method receive a list of MAC addresses to update. Because in this case only one
                        #controller is being updated, a list with only the MAC address of the controller is created.
                        self.ctrllerMsger.updPerson([ctrllerMac], person)
                    for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_DELETE):
                        #"delPerson" method receive a list of MAC addresses to update. Because in this case only one
                        #controller is being updated, a list with only the MAC address of the controller is created.
                        self.ctrllerMsger.delPerson([ctrllerMac], person['id'])
                    self.checkExit()


                except database.DoorError as doorError:
                    logMsg = 'Error retransmitting uncommitted doors: {}'.format(str(doorError))
                    self.logger.warning(logMsg)
                except database.AccessError as accessError:
                    logMsg = 'Error retransmitting uncommitted accesses: {}'.format(str(accessError))
                    self.logger.warning(logMsg)
                except database.PersonError as personError:
                    logMsg = 'Error retransmitting uncommitted persons: {}'.format(str(personError))
                    self.logger.warning(logMsg)


            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()

                #self.iteration is protected with self.lockIteration lock every time it is
                #accessed, as it is modified by this thread (CrudReSender) and by NetMngr Thread
                #Keep "self.iteration" locked during all below code block won't be optimal as
                #there are methods inside this block which may spend some time accessing to
                #database or sending things over the network. (Sending things over the network
                #keeping the lock would cause a deadlock if not using queues)

                #To avoid keeping "self.iteration" locked too much time, it is copied.
                with self.lockIteration:
                    iteration = self.iteration

                if iteration >= self.ITERATIONS:
                    logMsg = 'Checking if there are controllers which need to be re provisioned.'
                    self.logger.debug(logMsg)
                    #Getting the MAC addresses of controllers which has uncommitted CRUDs.
                    unCmtCtrllers = self.dataBase.getUnCmtCtrllers()
                    unCmtCtrllersMacs = [unCmtCtrller['macAddress'] for unCmtCtrller in unCmtCtrllers]
                    if unCmtCtrllersMacs:
                        logMsg = 'Sending Request Re Provision Message to: {}'.format(', '.join(unCmtCtrllersMacs))
                        self.logger.info(logMsg)
                        self.ctrllerMsger.requestReSendCruds(unCmtCtrllersMacs)
                    with self.lockIteration:
                        self.iteration = 0
                else:
                    with self.lockIteration:
                        self.iteration +=1
