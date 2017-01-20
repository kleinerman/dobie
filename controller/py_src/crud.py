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

    def __init__(self, lockPssgsControl, pssgsControl, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudMngr', exitFlag)

        #When receiving a passage CRUD is necessary to re launch the ioiface proccess.
        #For this reason it is necessary a reference to "ioIface" object.
        self.lockPssgsControl = lockPssgsControl
        self.pssgsControl = pssgsControl

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

        self.crudHndlrs = {'SC': self.dataBase.addPassage,
                           'SU': self.dataBase.updPassage,
                           'SD': self.dataBase.delPassage,
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

                if crudMsg == RRP:
                    self.dataBase.clearDatabase()
                    self.netMngr.sendToServer(RRRE + END)

                else:

                    #Getting the CRUD command and the JSON object
                    crudCmd = crudMsg[0:2]
                    completeJson = crudMsg[2:]

                    crudObject = json.loads(completeJson)
                    #Calling the corresponding DB method according to the CRUD command received
                    self.crudHndlrs[crudCmd](crudObject)

                    #If the CRUD command do a modification in a passage, it is necessary to 
                    #relaunch the ioIface
                    if crudCmd[0] == 'S':
                        with self.lockPssgsControl:
                            self.pssgsControl.loadParams()
                        
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
                



