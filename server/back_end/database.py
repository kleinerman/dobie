import pymysql
import queue
import logging

import genmngr
from config import *



class DbMngr(genmngr.GenericMngr):

    def __init__(self, host, user, passwd, dataBase, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('DbMngr', exitFlag)

        self.host = host
        self.user = user
        self.passwd = passwd
        self.dataBase = dataBase
    
        self.netToDb = queue.Queue()


        self.connection = pymysql.connect(host, user, passwd, dataBase)
        
        self.cursor = self.connection.cursor()




    def isValidCtrller(self, ctrllerMac):

        #Creating a separate connection since this method will be called from
        #different thread
        connection = pymysql.connect(self.host, self.user, self.passwd, self.dataBase)
        cursor = connection.cursor()

        #macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(ctrllerMac)

        cursor.execute(sql)
        return cursor.fetchone()[0]





    def putEvents(self, events):
        '''
        '''
        self.netToDb.put(events)






    def saveEvents(self, events):
        '''
        It receives a list of events and saves them in the database

        {'pssgId': 7, 'notReason': None, 'side': 1, 'latchType': 1, 'personId': 1619, 'dateTime': '2015-11-05 15:46', 'eventType': 1, 'allowed': True}
        '''


        for event in events:
            print(event)






    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Network" thread.
        '''

        while True:
            try:
                #Blocking until Main thread sends an event or EXIT_CHECK_TIME expires 
                events = self.netToDb.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                self.saveEvents(events)

            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()








    #def __del__(self):
   
        #self.connection.commit() 
        #self.connection.close()

