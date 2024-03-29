import threading
import logging
import datetime
import time
import sys
import json
import re

import database
import queue

import genmngr
import doormod
from config import *
from msgheaders import *




class CrudMngr(genmngr.GenericMngr):

    '''
    This thread receives messages from the network thread in the "netToCrud" queue.
    When the network thread receives a CRUD message from the server, it put this message
    in this queue and can return fastly to receive or send message to the server.
    This thread (CrudMngr) get the CRUD messages from the queue and do the necesary
    operation with the database avoiding delaying the network while it database operations
    are happening.
    '''

    def __init__(self, lockDoors, doors, exitFlag):

        #Invoking the parent class constructor, specifying the thread name,
        #to have a understandable log file.
        super().__init__('CrudMngr', exitFlag)

        #When receiving a door CRUD is necessary to re launch the ioiface proccess.
        #For this reason it is necessary a reference to "ioIface" object.
        self.lockDoors = lockDoors
        self.doors = doors

        #Reference to network manager to answer the CRUD messages
        #sent by the server
        self.netMngr = None

        #Database connection should be created in run method
        self.dataBase = None

        #Queue to receive message from the Network thread.
        self.netToCrud = queue.Queue()



    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting
        for queue messages coming from the "NetMngr" thread.
        '''

        #The connection to database should be done here and not in constructor since
        #the constructor is executed by the main thread and to have simultaneous access to DB
        #from diffrent thread each thread shoud crate its own connection.
        self.dataBase = database.DataBase(DB_FILE)

        self.crudHndlrs = {'SC': self.addDoor,
                           'SU': self.updDoor,
                           'SD': self.delDoor,
                           'UC': self.dataBase.addUnlkDoorSkd,
                           'UU': self.dataBase.updUnlkDoorSkd,
                           'UD': self.dataBase.delUnlkDoorSkd,
                           'EC': self.dataBase.addExcDayUds,
                           'EU': self.dataBase.updExcDayUds,
                           'ED': self.dataBase.delExcDayUds,
                           'AC': self.dataBase.addAccess,
                           'AU': self.dataBase.updAccess,
                           'AD': self.dataBase.delAccess,
                           'LC': self.dataBase.addLiAccess,
                           'LU': self.dataBase.updLiAccess,
                           'LD': self.dataBase.delLiAccess,
                           'PU': self.dataBase.updPerson,
                           'PD': self.dataBase.delPerson
                          }

        while True:
            try:
                #Blocking until NetMngr thread sends an event or EXIT_CHECK_TIME expires
                crudMsg = self.netToCrud.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()

                if crudMsg == RRS:
                    self.logger.info('Clearing database to receive resyncing from server.')
                    self.dataBase.clearDatabase()
                    self.netMngr.sendToServer(RRRS + END)

                else:

                    #Getting the CRUD command and the JSON object
                    crudCmd = crudMsg[0:2]
                    completeJson = crudMsg[2:]

                    crudObject = json.loads(completeJson)
                    #Calling the corresponding DB method according to the CRUD command received
                    self.crudHndlrs[crudCmd](crudObject)

                    #If we are at this point of code means that the database method executed
                    #did not throw an exception and therefore we can answer with OK to the server.
                    #Getting the ID from the json to create the response to answer the server.
                    jsonId = re.search('("id":\s*\d*)', completeJson).groups()[0]
                    jsonId = '{' + jsonId + '}'
                    jsonId = jsonId.encode('utf8')
                    crudCmd = crudCmd.encode('utf8')
                    ctrllerResponse = RCUD + crudCmd + b'OK' + jsonId + END
                    #Send the response to the server
                    self.netMngr.sendToServer(ctrllerResponse)


            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()

            except database.OperationalError as operationalError:
                #Perhaps here we can answer with something different than OK to the server.
                #At this momment we are responding nothing to the server when an error happen.
                self.logger.error(operationalError)

            except database.IntegrityError as integrityError:
                #Perhaps here we can answer with something different than OK to the server.
                #At this momment we are responding nothing to the server when an error happen.
                self.logger.error(integrityError)


    def addDoor(self, doorJson):
        '''
        Complete the door parametter in the corresponding door object of the
        dictionary and add the door to the database.
        '''
        doorNum = int(doorJson['doorNum'])
        with self.lockDoors:
            try:
                door = self.doors[doorNum]
            except KeyError:
                # This can happen if the server send an incorrect doorNum.
                # In this situation, an OK will be sent to the server anyway.
                self.logger.waring(f"There isn't any door with doorNum: {doorNum}")
                return
            door.doorId = int(doorJson['id'])
            door.snsrType = int(doorJson['snsrType'])
            door.unlkTime = int(doorJson['unlkTime'])
            door.bzzrTime = int(doorJson['bzzrTime'])
            door.alrmTime = int(doorJson['alrmTime'])

        self.dataBase.addDoor(doorJson)


    def updDoor(self, doorJson):
        '''
        Complete the door parametter in the corresponding door object of the
        dictionary and update the door to the database.
        '''
        doorNum = int(doorJson['doorNum'])
        with self.lockDoors:
            try:
                door = self.doors[doorNum]
            except KeyError:
                # This can happen if the server send an incorrect doorNum.
                # In this situation, an OK will be sent to the server anyway.
                self.logger.waring(f"There isn't any door with doorNum: {doorNum}")
                return
            door.doorId = int(doorJson['id'])
            door.snsrType = int(doorJson['snsrType'])
            door.unlkTime = int(doorJson['unlkTime'])
            door.bzzrTime = int(doorJson['bzzrTime'])
            door.alrmTime = int(doorJson['alrmTime'])

        self.dataBase.updDoor(doorJson)


    def delDoor(self, doorJson):
        '''
        Set to "None" all soft door parametters and
        delete the door from the database.
        '''
        doorId = int(doorJson['id'])
        with self.lockDoors:
            try:
                doorNum = self.doors.getDoorNum(doorId)
            except doormod.DoorNotConfigured as doorNotConfigured:
                # This can happen if the server try to delete a door that
                # never was created. For example: door added, controller not
                # reachable (pending to add in server), force commit, then the
                # user try to delete the door in the server.
                # In this situation, an OK will be sent to the server anyway.
                self.logger.debug(doorNotConfigured)
                self.logger.warning("Trying to delete an unconfigured door")
                return
            door = self.doors[doorNum]
            door.doorId = None
            door.snsrType = None
            door.unlkTime = None
            door.bzzrTime = None
            door.alrmTime = None

        self.dataBase.delDoor(doorJson)
