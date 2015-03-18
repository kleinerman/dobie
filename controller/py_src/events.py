import threading
import logging
import datetime
import time
import sys

import database
import queue

from config import *




class EventMngr(threading.Thread):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''

    def __init__(self, mainToEvent, netMngr, netToEvent, netToReSnd, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__(name = 'EventMngr', daemon = True)

        #Database connection should be created in run method
        self.dataBase = None

        #Queue to receive message from the Main thread.
        self.mainToEvent = mainToEvent

        #Queue to send messages to net.
        self.netMngr = netMngr

        #Queue to receive message from the Network thread.
        self.netToEvent = netToEvent

        #Queue used by ReSender thread to receive message from the Network thread.
        self.netToReSnd = netToReSnd
        
        #Flag to see know when the Main thread ask as to finish
        self.exitFlag = exitFlag

        #Flag to know if Resender Thread is alive
        self.resenderAlive = threading.Event()

        #Thread exit code
        self.exitCode = 0

        #Getting the logger
        self.logger = logging.getLogger('Controller')






    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        If true, call sys.exit and finish this thread
        '''
        if self.exitFlag.is_set():
            self.logger.info('Event thread exiting.')
            sys.exit(self.exitCode)





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
            #self.logger.debug('Sender Thread waiting from MGT or Asynchronous Receiver messages ...')
            try:
                #Blocking until Main thread sends an event or EXIT_CHECK_TIME expires 
                event = self.mainToEvent.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                self.netMngr.sendEvent(event)
                try:
                    eventResponse = self.netToEvent.get(timeout=WAIT_RESP_TIME)
                    #We should check the response
                    print('Getting Event Response: {}.'.format(eventResponse))
                except queue.Empty:
                    self.logger.warning('No response from server, saving event in local DB')
                    self.dataBase.saveEvent(event)
                    self.checkExit()
                    
                    if not self.resenderAlive.is_set():
                        self.resenderAlive.set()
                        reSender = ReSender(self.netMngr, self.netToReSnd, self.resenderAlive, self.exitFlag)
                        reSender.start()
    
            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()







class ReSender(threading.Thread):

    '''
    This thread tries to resend events when there is no connection to server.
    Once the connection is established it resend the events and it dies.
    '''

    def __init__(self, netMngr, netToReSnd, resenderAlive, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__(name = 'ReSender', daemon = True)

        self.netMngr = netMngr

        self.netToReSnd = netToReSnd

        #Database connection should be created in run method
        self.dataBase = None

        #Flag to know if Resender Thread is alive
        self.resenderAlive = resenderAlive

        #Flag to know when the Main thread ask as to finish
        self.exitFlag = exitFlag

        #Thread exit code
        self.exitCode = 0

        #Getting the logger
        self.logger = logging.getLogger('Controller')


        #Calculating turns to sleep EXIT_CHECK_TIME
        self.SLEEP_TURNS = RE_SEND_TIME // EXIT_CHECK_TIME

        #Calculating real resend time
        self.REAL_RE_SEND_TIME = self.SLEEP_TURNS * EXIT_CHECK_TIME


    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        If true, call sys.exit and finish this thread
        '''
        if self.exitFlag.is_set():
            self.logger.info('ReSender thread exiting.')
            sys.exit(self.exitCode)



    def run(self):
        '''
        '''
        self.dataBase = database.DataBase(DB_FILE)

        for eventIdList, eventList in self.dataBase.getNEvents(3):
            noConnection = True
            while noConnection:
                self.netMngr.reSendEvents(eventList)
                try:
                    eventsResponse = self.netToReSnd.get(timeout=WAIT_RESP_TIME)
                    #We should check the response here
                    print('Getting Events Response: {}.'.format(eventsResponse))
                    self.dataBase.delEvents(eventIdList)
                    noConnection = False
                except queue.Empty:
                    logMsg = ("Sleeping for {} secs to retry sending events."
                              "".format(self.REAL_RE_SEND_TIME)
                             )
                    self.logger.info(logMsg) 
                    for i in range(self.SLEEP_TURNS):
                        self.checkExit()
                        time.sleep(EXIT_CHECK_TIME)

        self.resenderAlive.clear()
        sys.exit(self.exitCode)
