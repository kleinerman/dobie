import queue
import logging
import requests

import genmngr
import database
from config import *


class RtEventMngr(genmngr.GenericMngr):
    '''
    This thread is created by the main thread.
    When the message receiver thread receives an event, it 
    puts the event in "msgRecToRtEvent" queue (attribute of this class). 
    This thread gets the events from the queue and sends then to the 
    events-live.js app running in nodejs via REST using a POST method.
    '''

    def __init__(self, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('RtEventMngr', exitFlag)
   
        self.nodejsUrl = 'http://{}:{}/readevent'.format(NODEJS_HOST, NODEJS_PORT)

        self.msgRecToRtEvent = queue.Queue()

        #The creation of this object was moved to the run method to avoid
        #freezing the main thread when there is no connection to database.
        self.dataBase = None



    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked
        waiting for events coming from the "Message Receiver" thread.
        '''

        #First of all, the database should be connected by the execution of this thread
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)

        while True:
            try:
                #Blocking until Message Receiver thread sends an event or 
                #EXIT_CHECK_TIME expires 
                event = self.msgRecToRtEvent.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()

                try:
                    #Before sending the event to the events-live.js application,
                    #it should be formatted adding some fields. This is done
                    #using "getFmtEvent" function from database.
                    #Is better to do this in this thread and not in "msgreceiver"
                    #since here we have more time. Also if this thread crashes for 
                    #a data base error is not so important as "msgreceiver" thread
                    fmtEvent = self.dataBase.getFmtEvent(event)
                except database.EventError:
                    self.logger.warning("Error trying to format event")


                try:
                    self.logger.debug("Sending to nodejs live event: {}".format(fmtEvent))
                    requests.post(self.nodejsUrl, json=fmtEvent, timeout=NODEJS_TOUT)
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    self.logger.warning("Error trying to connect to nodejs")

            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()




