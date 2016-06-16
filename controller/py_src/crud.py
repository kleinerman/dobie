import threading
import logging
import datetime
import time
import sys
import json

import database
import queue

import genmngr
from config import *





class CrudMngr(genmngr.GenericMngr):

    '''
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudMngr', exitFlag)

        #Database connection should be created in run method
        self.dataBase = None

        #Queue to receive message from the Network thread.
        self.netToCrud = queue.Queue()

        self.crudHndlrs = {'S': self.mngPassage
                          }





    def mngPassage(self, crudMsg):
        '''
        '''

        crudSubCmd = crudMsg[1]
        passageJson = crudMsg[2:]

        passage = json.loads(passageJson)

        if crudSubCmd == 'C':
            self.dataBase.addPassage(passage)

        elif crudSubCmd == 'U':
            self.dataBase.updPassage(passage)

        elif crudSubCmd == 'D':
            self.dataBase.delPassage(passage)

        else:
            print('Invalid crud passage sub command.')



    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Main" thread.
        '''

        #The connection to database should be done here and not in constructor since
        #the constructor is executed by the main thread and to have simultaneous access to DB
        #from diffrent thread each thread shoud crate its own connection.
        self.dataBase = database.DataBase(DB_FILE)

        while True:
            try:
                #Blocking until Main thread sends an event or EXIT_CHECK_TIME expires 
                crudMsg = self.netToCrud.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                crudCmd = crudMsg[0]
                self.crudHndlrs[crudCmd](crudMsg)  


                

    
            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()



