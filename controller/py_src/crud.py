import threading
import logging
import datetime
import time
import sys

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
                crud = self.netToCrud.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                print(crud)
    
            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()



