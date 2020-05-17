import threading
import logging
import datetime
import time
import sys

import database
import queue

import genmngr
from config import *





class EventMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''

    def __init__(self, toEvent, netMngr, netToEvent, netToReSnd, resenderAlive, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('EventMngr', exitFlag)

        #Database connection should be created in run method
        self.dataBase = None

        #Queue to receive message from the Main thread.
        self.toEvent = toEvent

        #Queue to send messages to net.
        self.netMngr = netMngr

        #Queue to receive message from the Network thread.
        self.netToEvent = netToEvent

        #Queue used by ReSender thread to receive message from the Network thread.
        self.netToReSnd = netToReSnd
        
        #Flag to know if Resender Thread is alive
        self.resenderAlive = resenderAlive






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
                event = self.toEvent.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()
                self.netMngr.sendEvent(event)
                try:
                    eventResponse = None
                    eventResponse = self.netToEvent.get(timeout=WAIT_RESP_TIME)
                    if eventResponse == 'OK':
                        self.logger.debug('The server confirms the reception of the event.')
                    else:
                        raise queue.Empty
                except queue.Empty:
                
                    if eventResponse:
                        logMsg = 'The server could not save the event, '
                    else:
                        logMsg = 'No response from server, '
                    logMsg += 'saving event in local DB'

                    self.logger.warning(logMsg)
                    self.dataBase.saveEvent(event)
                    self.checkExit()
                    
                    if not self.resenderAlive.is_set():
                        self.resenderAlive.set()
                        reSender = ReSender(self.netMngr, self.netToReSnd, self.resenderAlive, self.exitFlag)
                        reSender.start()
    
            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()







class ReSender(genmngr.GenericMngr):

    '''
    This thread tries to resend events when there is no connection to server.
    Once the connection is established it resend the events and it dies.
    '''

    def __init__(self, netMngr, netToReSnd, resenderAlive, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('ReSender', exitFlag)

        self.netMngr = netMngr

        self.netToReSnd = netToReSnd

        #Database connection should be created in run method
        self.dataBase = None

        #Flag to know if Resender Thread is alive
        self.resenderAlive = resenderAlive

        #Calculating turns to sleep EXIT_CHECK_TIME
        self.SLEEP_TURNS = RE_SEND_TIME // EXIT_CHECK_TIME

        #Calculating real resend time just for logging purposes
        self.REAL_RE_SEND_TIME = self.SLEEP_TURNS * EXIT_CHECK_TIME




    def run(self):
        '''
        '''
        self.dataBase = database.DataBase(DB_FILE)

        for eventIds, toReSendEvents in self.dataBase.getNEvents(RE_SEND_EVTS_QUANT):
            eventsSent = False
            while not eventsSent:
                self.netMngr.reSendEvents(toReSendEvents)
                try:
                    eventsResponse = self.netToReSnd.get(timeout=WAIT_RESP_TIME)
                    if eventsResponse == 'OK':
                        self.logger.debug('The server confirms the reception of the events.')
                        self.dataBase.delEvents(eventIds)
                        eventsSent = True
                    else:
                        self.logger.warning('The server could not save the events correctly.')
                        raise queue.Empty
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
