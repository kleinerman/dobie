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
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudMngr', exitFlag)

        #Reference to network manager
        self.netMngr = None

        #Database connection should be created in run method
        self.dataBase = None

        #Queue to receive message from the Network thread.
        self.netToCrud = queue.Queue()



    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Main" thread.
        '''

        #The connection to database should be done here and not in constructor since
        #the constructor is executed by the main thread and to have simultaneous access to DB
        #from diffrent thread each thread shoud crate its own connection.
        self.dataBase = database.DataBase(DB_FILE)

        self.crudHndlrs = {'SC': self.dataBase.addPassage,
                           'SU': self.dataBase.updPassage,
                           'SD': self.dataBase.delPassage,
                           'AC': self.dataBase.addAccess
                          }

        while True:
            try:
                #Blocking until Main thread sends an event or EXIT_CHECK_TIME expires 
                crudMsg = self.netToCrud.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()


                crudCmd = crudMsg[0:2]
                completeJson = crudMsg[2:]

                crudObject = json.loads(completeJson)
                self.crudHndlrs[crudCmd](crudObject)

                jsonId = re.search('("id":\s*\d*)', completeJson).groups()[0]
                jsonId = '{' + jsonId + '}'
                jsonId = jsonId.encode('utf8')
                crudCmd = crudCmd.encode('utf8')
                ctrllerResponse = RCUD + crudCmd + b'OK' + jsonId + END
                self.netMngr.sendToServer(ctrllerResponse)

    
            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()

            except database.OperationalError as operationalError:
                self.logger.error(operationalError)

            except database.IntegrityError as integrityError:
                self.logger.error(integrityError)
                



