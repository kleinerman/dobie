import pymysql
import queue
import logging

import genmngr
from config import *



class OrganizationError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



class PersonError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



class ZoneError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



class ControllerError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



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
        '''


        for event in events:

            #Converting all None fields to 'NULL' to write the SQL sentence
            #At this moment this is only need in 'personId' and 'notReason'
            #fields
            for eventField in event:
                if event[eventField] == None:
                    event[eventField] = 'NULL'


            sql = ("INSERT INTO "
                   "Event(eventTypeId, pssgId, dateTime, latchId, personId, side, allowed, notReason) "
                   "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
                   "".format(event['eventType'], event['pssgId'], event['dateTime'],
                             event['latchType'], event['personId'], event['side'],
                             event['allowed'], event['notReason']
                            ) 

                  )
            try:
                self.cursor.execute(sql)
                self.connection.commit()

            except pymysql.err.IntegrityError as integrityError:
                self.logger.warning(integrityError)



#----------------------------------Organization----------------------------------------


    def addOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and save it in DB
        '''

        sql = ("INSERT INTO Organization(name) VALUES('{}')"
               "".format(organization['name'])
              )
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise OrganizationError('Can not add this organization')





    def delOrganization(self, organization):
        '''
        Receive a dictionary with id organization
        '''

        sql = ("DELETE FROM Organization WHERE id = {}"
               "".format(organization['id'])
              )        

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationError('Organization not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise OrganizationError('Can not delete this organization')



    def updOrganization(self, organization):
        '''
        Receive a dictionary with id organization
        '''

        sql = ("UPDATE Organization SET name = '{}' WHERE id = {}"
               "".format(organization['name'], organization['id'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise OrganizationError('Can not update this organization')







#----------------------------------Zone----------------------------------------


    def addZone(self, zone):
        '''
        Receive a dictionary with zone parametters and save it in DB
        '''

        sql = ("INSERT INTO Zone(name) VALUES('{}')"
               "".format(zone['name'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ZoneError('Can not add this zone')





    def delZone(self, zone):
        '''
        Receive a dictionary with id zone
        '''

        sql = ("DELETE FROM Zone WHERE id = {}"
               "".format(zone['id'])
              )

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise ZoneError('Zone not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ZoneError('Can not delete this zone')






    def updZone(self, zone):
        '''
        Receive a dictionary with id zone
        '''

        sql = ("UPDATE Zone SET name = '{}' WHERE id = {}"
               "".format(zone['name'], zone['id'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ZoneError('Can not update this zone')






#----------------------------------Controller----------------------------------------


    def addController(self, controller):
        '''
        Receive a dictionary with controller parametters and save it in DB
        '''

        sql = ("INSERT INTO Controller(boardModel, macAddress, ipAddress) "
               "VALUES('{}', '{}', '{}')"
               "".format(controller['boardModel'], controller['macAddress'], 
                         controller['ipAddress'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ControllerError('Can not add this controller')





    def delController(self, controller):
        '''
        Receive a dictionary with id controller
        '''

        sql = ("DELETE FROM Controller WHERE id = {}"
               "".format(controller['id'])
              )

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise ControllerError('Controller not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ControllerError('Can not delete this controller')




    def updController(self, controller):
        '''
        Receive a dictionary with id controller
        '''

        sql = ("UPDATE Controller SET boardModel = '{}', macAddress = '{}', "
               "ipAddress = '{}' WHERE id = {}"
               "".format(controller['boardModel'], controller['macAddress'], 
                         controller['ipAddress'], controller['id'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise ControllerError('Can not update this controller')





#-------------------------------Person-----------------------------------




    def addPerson(self, person):
        '''
        Receive a dictionary with person parametters and save it in DB
        '''

        sql = ("INSERT INTO Person(name, cardNumber, orgId, rowStateId) VALUES('{}', {}, {}, {})"
               "".format(person['name'], person['cardNumber'], person['orgId'], 2)
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise PersonError('Can not add this organization')





    def delPerson(self, person):
        '''
        Receive a dictionary with id organization
        '''

        sql = ("DELETE FROM Person WHERE id = {}"
               "".format(person['id'])
              )

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationError('Person not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise PersonError('Can not delete this person')





    def updPerson(self, person):
        '''
        Receive a dictionary with id organization
        '''

        sql = ("UPDATE Person SET name = '{}', cardNumber = {}, orgId = {} WHERE id = {}"
               "".format(person['name'], person['cardNumber'], person['orgId'], person['id'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.warning(integrityError)
            raise PersonError('Can not update this person')



#---------------------------------------------------------------------------------------



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
