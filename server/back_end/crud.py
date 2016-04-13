import threading
import logging
import os

import socket
import json

import database
import queue

import genmngr
from config import *


import sys





class CrudMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''
    def __init__(self, dbMngr, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('CrudMngr', exitFlag)

        #Queue used to send Events and CRUD confirmation to dbMngr
        self.dbMngr = dbMngr
        #self.netToDb = netToDb




    #---------------------------------------------------------------------------#

    def run(self):
        '''
        '''

        while True:


            tecInput = input()

            print(tecInput)

#            if tecInput.split()[0] == '1':
#
#                organization = json.loads()

#                self.dbMngr.saveOrganization()



            #Cheking if Main thread ask as to finish.
            self.checkExit()



    
