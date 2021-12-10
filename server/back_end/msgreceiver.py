import pymysql
import queue
import logging
import json
import re

import genmngr
import database
from config import *
from msgheaders import *


class MsgReceiver(genmngr.GenericMngr):
    '''
    This thread is created by the main thread.
    When the network thread receives a message from the controller, it 
    put the message in "netToMsgRec" queue. This thread get the message
    from the queue and do the necessary operation with DB. In this way
    the network thread do not lose time doing things in DB.
    '''

    def __init__(self, exitFlag, toRtEventQueue):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('MsgReceiver', exitFlag)


        #The creation of this object was moved to the run method to avoid
        #freezing the main thread when there is no connection to database.
        self.dataBase = None

        #Commit handlers were moved to the run method since the dataBase
        #object and its method doesn't exist yet.
        self.commitHndlrs = None

        #The ctrllerMsger is used to send to the controllers the message
        #to delete the visitors when they pass trough exit doors
        #The object is set in the main thread
        self.ctrllerMsger = None
    
        self.toRtEventQueue = toRtEventQueue

        self.netToMsgRec = queue.Queue()





    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Network" thread.
        '''

        #First of all, the database should be connected by the execution of this thread
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)
        #Now we can set the commit handlers.
        self.commitHndlrs = {'D': self.dataBase.commitDoor,
                             'L': self.dataBase.commitAccess,
                             'A': self.dataBase.commitLiAccess,
                             'N': self.dataBase.commitPerson
                            }

        while True:
            try:
                #Blocking until Network thread sends an msg or EXIT_CHECK_TIME expires 
                msg = self.netToMsgRec.get(timeout=EXIT_CHECK_TIME)
                self.checkExit()

                #When the controller sends an Event
                if msg.startswith(EVT):

                    event = msg.strip(EVT+END).decode('utf8')
                    event = json.loads(event)

                    try:
                        #Before sending the event to the events-live.js application,
                        #it should be formatted adding some fields. This is done
                        #using "getFmtEvent" function from database.
                        fmtEvent = self.dataBase.getFmtEvent(event)
                        self.toRtEventQueue.put(fmtEvent)
                    except database.EventError:
                        self.logger.warning("Error trying to format event")

                    if self.dataBase.isValidVisitExit(event):
                        personId = event['personId']
                        logMsg = "Visitor exiting. Removing from system person with ID = {}".format(personId)
                        self.logger.info(logMsg)
                        ctrllerMacsToDelPrsn = self.dataBase.markPerson(personId, database.TO_DELETE)
                        self.ctrllerMsger.delPerson(ctrllerMacsToDelPrsn, personId) 

                    events = [event]
                    self.dataBase.saveEvents(events)

                #When the controller sends many Events (Retransmitting)
                elif msg.startswith(EVS):

                    events = msg[1:-1].split(EVS)
                    events = [json.loads(evnt.decode('utf8')) for evnt in events]

                    for event in events:
                        if self.dataBase.isValidVisitExit(event):
                            personId = event['personId']
                            logMsg = "Visitor exiting. Removing from system person with ID = {}".format(personId)
                            self.logger.info(logMsg)
                            ctrllerMacsToDelPrsn = self.dataBase.markPerson(personId, database.TO_DELETE)
                            self.ctrllerMsger.delPerson(ctrllerMacsToDelPrsn, personId)

                    self.dataBase.saveEvents(events)


                #When the controller sends a response to CRUD message
                elif msg.startswith(CUD):
                    
                    crudResponse = msg.strip(RCUD+END).decode('utf8')
                    crudId = re.search('"id":\s*(\d*)', crudResponse).groups()[0]
                    crudTypeResp = crudResponse[0]

                    #When a response from an update or delete person is received, it is
                    #necessary to pass to commitPerson method the controller MAC.
                    #The rest of commit methods just need the crudId.
                    if crudTypeResp == 'P':
                        ctrllerMac = re.search('"mac":\s(\w{12})', crudResponse).groups()[0]
                        self.dataBase.commitPerson(crudId, ctrllerMac)
                    else:
                        self.commitHndlrs[crudTypeResp](crudId)

                #When the controller sends a Keep Alive message
                elif msg.startswith(KAL):
                    ctrllerMac = msg.strip(KAL+CUD+END).decode('utf8')
                    self.logger.debug('Receiving Keep Alive message from: {}.'.format(ctrllerMac))
                    try:
                        revivedCtrller = self.dataBase.setCtrllerReachable(ctrllerMac)
                        #If the controller wasn't alive previously, "revivedCtrller" will not be None,
                        #and a JSON will be sent to "rtevent" thread.
                        if revivedCtrller:
                            self.toRtEventQueue.put(revivedCtrller)
                    except database.ControllerError:
                        self.logger.error("Controller: {} can't be set alive.".format(ctrllerMac))


            except queue.Empty:
                #Cheking if Main thread ask as to finish.
                self.checkExit()




