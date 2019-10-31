import pymysql
import queue
import logging
import datetime
import crypt
import threading
import time
import os

from config import *

TO_ADD = 1
TO_UPDATE = 2
COMMITTED = 3
TO_DELETE = 4
DELETED = 5



class NotReachable(Exception):
    '''
    '''
    pass



class UserError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class UserNotFound(UserError):
    '''
    '''
    pass




class OrganizationError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class OrganizationNotFound(OrganizationError):
    '''
    '''
    pass



class PersonError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class PersonNotFound(PersonError):
    '''
    '''
    pass



class ZoneError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class ZoneNotFound(ZoneError):
    '''
    '''
    pass



class DoorGroupError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class DoorGroupNotFound(DoorGroupError):
    '''
    '''
    pass


class CtrllerModelError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class CtrllerModelNotFound(CtrllerModelError):
    '''
    '''
    pass


class ControllerError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class ControllerNotFound(ControllerError):
    '''
    '''
    pass


class DoorError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class DoorNotFound(DoorError):
    '''
    '''
    pass



class AccessError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class AccessNotFound(AccessError):
    '''
    '''
    pass



class EventError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class EventNotFound(EventError):
    '''
    '''
    pass




class ResStateError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class ResStateNotFound(ResStateError):
    '''
    '''
    pass




class EventTypeError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class EventTypeNotFound(EventTypeError):
    '''
    '''
    pass



class DoorLockError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class DoorLockNotFound(DoorLockError):
    '''
    '''
    pass




class DenialCauseError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class DenialCauseNotFound(DenialCauseError):
    '''
    '''
    pass




class RoleError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class RoleNotFound(RoleError):
    '''
    '''
    pass





class DataBase(object):

    def __init__(self, host, user, passwd, dataBase, callingMngr):


        self.logger = logging.getLogger(LOGGER_NAME)

        self.host = host
        self.user = user
        self.passwd = passwd
        self.dataBase = dataBase
        self.callingMngr = callingMngr


        self.connect()




    def escapeDict(self, dictObj):
        '''
        Escaping special characters of the dictionary
        values like quote or double quote.

        '''
        for key, value in dictObj.items():
            if type(value) == str:
                dictObj[key] = pymysql.escape_string(value)
        return dictObj






    def connect(self):
        '''
        Try to connect to DB engine. If DB engine is not available,
        it makes the manager that is using this object to check if the main
        thread ask this manager to finish and then sleep EXIT_CHECK_TIME
        before trying to connect again.
        '''
        while True:
            try:
                self.logger.info('Connecting to database...')
                self.connection = pymysql.connect(self.host, self.user, 
                                                  self.passwd, self.dataBase,
                                                  connect_timeout = EXIT_CHECK_TIME,
                                                  client_flag = pymysql.constants.CLIENT.FOUND_ROWS)
                                                  #With this client_flag, cursor.rowcount will have
                                                  #found rows instead of affected rows
                self.logger.info('Database connected.')
                # The following line makes all "fetch" calls return a dictionary instead a tuple
                self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
                break

            except pymysql.err.OperationalError:
                self.logger.warning("Database not reachable.")

                if self.callingMngr:
                    self.logger.info("Retrying connect to Database...")
                    self.callingMngr.checkExit()
                    time.sleep(EXIT_CHECK_TIME)
                else:
                    #This situation will happen when the DataBase instance is not created by a 
                    #thread ("self.callingMngr" is None). This is used when we want to avoid
                    #trying reconnect to the DB engine. This will be used in the 
                    #script "purgeevents.py". If there is no connection to the DB engine,
                    #the script should finish and not remain trying to reconnect.
                    raise NotReachable








    def execute(self, sql):
        '''
        This method is a wrapper of cursor.execute(). It tries to execute the "sql"
        string, if database is not connected, it reconnect and execute the statement.
        '''

        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except (pymysql.err.OperationalError, pymysql.err.InterfaceError, pymysql.err.InternalError):
            self.logger.info("Database is not connected. Reconnecting...")
            self.connect()
            self.cursor.execute(sql)
            self.connection.commit()
            





    def isValidCtrller(self, ctrllerMac):
        '''
        Returns an Integer when the MAC is registered in DB
        If the MAC is not registered, it returns None
        '''

        #macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(ctrllerMac)

        self.execute(sql)
        #If commit is not present, once adding the controller via REST 
        #it is neccesary to restart the server (not sure why)
        #self.connection.commit()
        return self.cursor.fetchone()['COUNT(*)']




    def saveCtrllerIp(self, ctrllerMac, ipAddress):
        '''
        Update Controller row setting the IP address of the
        controller when it connects to the server.
        '''

        sql = ("UPDATE Controller SET ipAddress = '{}' WHERE macAddress = '{}'"
               "".format(ipAddress, ctrllerMac)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ControllerNotFound('Controller not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not set IP address to this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not set IP address to this controller: wrong argument')





    def isValidVisitExit(self, event):
        '''
        Receieve an event as argument
        If this event correspond to a visitor exiting through a valid
        visit door exit, this method, returns True, if not, it returns False
        '''

        doorId = event['doorId']
        personId = event['personId']

        #There are events with personId = None. I think there aren't yet
        #events with doorId = None but just in case.
        if doorId == None or personId == None:
            return False

        #To know if it is a valid visit exit, to clear the visitor from the system,
        #the Visitor (Person), has to have access on the door he is exiting and also
        #the door has to have the visitExit field = True
        sql = ("SELECT COUNT(*) from Access JOIN Door ON (Access.doorId = Door.id) "
               "JOIN Person ON (Access.personId = Person.id) "
               "WHERE Person.visitedOrgId IS NOT NULL "
               "AND Door.isVisitExit = True AND Door.id = {} AND Person.id = {}"
               "".format(doorId, personId)
              )

        try:
            self.execute(sql)
            validVisitExit = self.cursor.fetchone()['COUNT(*)']
            return validVisitExit

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning("Error trying to validate a Visit Exit")
            return False






    def saveEvents(self, events):
        '''
        It receives a list of events and saves them in the database
        '''

        for event in events:

            #Converting all None fields to 'NULL' to write the SQL sentence
            #At this moment this is only need in 'personId' and 'denialCause'
            #fields
            for eventField in event:
                if event[eventField] == None:
                    event[eventField] = 'NULL'


            sql = ("INSERT INTO "
                   "Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) "
                   "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
                   "".format(event['eventTypeId'], event['doorId'], event['dateTime'],
                             event['doorLockId'], event['personId'], event['side'],
                             event['allowed'], event['denialCauseId']
                            ) 

                  )
            try:
                self.execute(sql)

            except pymysql.err.IntegrityError as integrityError:
                self.logger.debug(integrityError)

            except pymysql.err.InternalError as internalError:
                self.logger.debug(internalError)




    def cardNum2PrsnId(self, event):
        '''
        When the event comes from the controller and involves a person,
        instead of coming with the person id, it comes with the card number.
        This was because, sometimes, that person hasn't access on any door
        of this controller, therefore, the controller hasn't the person id.
        However, the backend may have the person id and report the event 
        of that person being denied to enter.
        This method, set "personId" field in the event dictionary and remove
        the "cardNumber" field if the event involves a person.
        '''

        try:

            if event['cardNumber'] != 'NULL':

                sql = "SELECT id FROM Person WHERE cardNumber = {}".format(event['cardNumber'])
                self.execute(sql)
                row = self.cursor.fetchone()

                if row:
                    personId = int(row['id'])
                else:
                    personId = 'NULL'

                event['personId'] = personId

            else:
                event['personId'] = 'NULL'

            event.pop('cardNumber')



        except KeyError:
            self.logger.debug("Error in cardNum2PrsnId method indexing.")
            raise EventError

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise EventError

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise EventError







    def getFmtEvent(self, event):
        '''
        It receives an event and returns the event formatted adding 
        fields like zone name, door name, organization name, person names and lastName.
        '''

        #When sending the JSON via requests module in rtevent,
        #the NULL values should be None
        for k in event:
            if event[k] == 'NULL':
                event[k] = None

        try:
            #Getting from DB the Zone and Door name
            sql = ("SELECT Zone.id AS zoneId, Zone.name AS zoneName, Door.name AS doorName "
                   "FROM Door JOIN Zone ON (Door.zoneId = Zone.id) "
                   "WHERE Door.id = {}".format(event['doorId'])
                  )

            self.execute(sql)
            zoneAndDoor = self.cursor.fetchone()

            #If the event involves a person, getting from DB the Organization
            #and Person name
            if event['personId']:
                sql = ("SELECT Organization.id AS orgId, Organization.name AS orgName, "
                       "CONCAT(Person.names, ' ', Person.lastName) AS personName "
                       "FROM Person JOIN Organization ON (Person.orgId = Organization.id) "
                       "WHERE Person.id = {}".format(event['personId'])
                      )

                self.execute(sql)
                orgAndPerson = self.cursor.fetchone()

            fmtEvent = {}
            fmtEvent['eventTypeId'] = event['eventTypeId']
            fmtEvent['doorId'] = event['doorId']
            fmtEvent['doorName'] = zoneAndDoor['doorName']
            fmtEvent['zoneId'] = zoneAndDoor['zoneId']
            fmtEvent['zoneName'] = zoneAndDoor['zoneName']

            fmtEvent['personId'] = event['personId']

            if event['personId']:
                fmtEvent['personName'] = orgAndPerson['personName']
                fmtEvent['orgId'] = orgAndPerson['orgId']
                fmtEvent['orgName'] = orgAndPerson['orgName']
            else:
                fmtEvent['personName'] = None
                fmtEvent['orgId'] = None
                fmtEvent['orgName'] = None

            #Setting personDeleted field as None always as
            #it has no sense in live events
            fmtEvent['personDeleted'] = None
            fmtEvent['doorLockId'] = event['doorLockId']
            fmtEvent['dateTime'] = event['dateTime']
            fmtEvent['side'] = event['side']
            fmtEvent['allowed'] = event['allowed']
            fmtEvent['denialCauseId'] = event['denialCauseId']

            return fmtEvent


        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise EventError

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise EventError





    def getEvents(self, orgId, personId, visitedOrgId, zoneId, doorId,
                  startDateTime, endDateTime, side, startEvt, evtsQtty):
        '''
        Return a dictionary with an interval of "evtsQtty" events starting from "startEvt".
        '''

        #When the following parameters are not NULL, they are used to
        #complete the below SQL sentence.
        if personId: personFilter = ' AND Event.personId = {}'.format(personId)
        else: personFilter = ''

        if orgId: orgFilter = ' AND Person.orgId = {}'.format(orgId)
        else: orgFilter = ''

        if visitedOrgId: visitedOrgIdFilter = ' AND Person.visitedOrgId = {}'.format(visitedOrgId)
        else: visitedOrgIdFilter = ''

        if doorId: doorFilter = ' AND Event.doorId = {}'.format(doorId)
        else: doorFilter = ''

        if zoneId: zoneFilter = ' AND Door.zoneId = {}'.format(zoneId)
        else: zoneFilter = ''

        if side: sideFilter = ' AND Event.side = {}'.format(side)
        else: sideFilter = ''


        #"startEvt" should not be < 1 since it is substracted by 1 to generate
        #the SQL sentence and less than 0 should raise a programming error sql
        #exception. To avoid it an "EventError" is raised
        #For SQL point of view, "evtsQtty" could be 0, but it will return a
        #void list. To avoid it, if evtsQtty < 1, also "EventError" is raised
        #Also, if startDateTime or endDateTime is None and EventError will be
        #raised.
        if startEvt < 1 or evtsQtty < 1 or not startDateTime or not endDateTime: 
            raise EventError

        #The startEvt value is substracted one since SQL starts indexing on 0.
        startEvtSql = startEvt - 1
        
        sql = ("SELECT Event.id, Event.eventTypeId, Zone.name AS zoneName, "
               "Door.name AS doorName, Organization.name AS orgName, "
               "CONCAT(Person.names, ' ', Person.lastName) AS personName, Person.resStateId AS personDeleted, "
               "Event.doorLockId, Event.dateTime, "
               "Event.side, Event.allowed, Event.denialCauseId "
               "FROM Event LEFT JOIN Door ON (Event.doorId = Door.id) "
               "LEFT JOIN Zone ON (Door.zoneId = Zone.id) "
               "LEFT JOIN Person ON (Event.personId = Person.id) "
               "LEFT JOIN Organization ON (Person.orgId = Organization.id) "
               "WHERE dateTime >= '{}' AND dateTime <= '{}'{}{}{}{}{}{} "
               "ORDER BY dateTime DESC LIMIT {},{}"
               "".format(startDateTime, endDateTime, personFilter, orgFilter, visitedOrgIdFilter, 
                         doorFilter, zoneFilter, sideFilter, startEvtSql, evtsQtty)
              )

        sqlCount = ("SELECT COUNT(*) FROM Event LEFT JOIN Door ON (Event.doorId = Door.id) "
                    "LEFT JOIN Zone ON (Door.zoneId = Zone.id) "
                    "LEFT JOIN Person ON (Event.personId = Person.id) "
                    "LEFT JOIN Organization ON (Person.orgId = Organization.id) "
                    "WHERE dateTime >= '{}' AND dateTime <= '{}'{}{}{}{}{}{}"
                    "".format(startDateTime, endDateTime, personFilter, orgFilter,
                              visitedOrgIdFilter, doorFilter, zoneFilter, sideFilter)
                   )

        try:
            #Calculating the total count of that could be returned. This is necessary for paging
            self.execute(sqlCount)
            totalEvtsCount = self.cursor.fetchone()['COUNT(*)']

            #If the first event selected is higher than the total count of events
            #an exception is raised.
            if startEvt > totalEvtsCount:
                self.logger.debug('The first event is higher than the count of all events.')
                raise EventNotFound('Events not found')

            self.execute(sql)
            events = self.cursor.fetchall()


            #Some adaptations before returning the events
            for event in events:
                #Converting all datetime fields into string because if not doing this, "jsonify"
                #method converts them to a format not desired like "Wed, 13 Sep 2017 17:50:00 GMT"
                #The "GMT" at the end was causing the browser converts it to GMT time.
                event['dateTime'] = event['dateTime'].strftime("%Y-%m-%d %H:%M")
                
                #If the person was deleted (resStateId == 5), converting it
                #to bool 1, otherwise converting it to bool 0.
                #If not an event involving a person, keep it null
                if event['personDeleted']:
                    if event['personDeleted'] == 5:
                        event['personDeleted'] = 1
                    else:
                        event['personDeleted'] = 0


            return events, totalEvtsCount


        except pymysql.err.ProgrammingError as programmingError:
            #This exception can happen when startEvtSql < 0 or evtQtty is < 0
            #This exception is converted to BadRequest in crud.py module
            #However this would never happen since both parametters are checked 
            #in the first part of the method
            raise EventError

        


    def purgeEvents(self, untilDateTime):
        '''
        Deletes rows from Event table until "untilDateTime".
        Also deletes persons from Person table which resStateId = DELETED
        and have not more events in Event table.
        Returns the amount of deleted events or raise "EventNotFound"
        exception if any event wasn't deleted.
        '''

        if not untilDateTime:
            #This is when the REST client doesn't send untilDateTime as
            #argument in the URL
            raise EventError('Can not delete events without untilDateTime')

        try:

            sql = "DELETE FROM Event WHERE dateTime <= '{}'".format(untilDateTime)
            self.execute(sql)
            delEvents = self.cursor.rowcount

            if delEvents < 1:
                raise EventNotFound('Events not found')

            #Deleting all persons which are marked as "DELETED" and don't have
            #more events in Event table.
            sql = ("SELECT id FROM Person WHERE resStateId = {} AND id NOT IN "
                   "(SELECT personId FROM Event WHERE Event.personId = Person.id)"
                   "".format(DELETED)
                  )
            self.execute(sql)
            toDelPersons = self.cursor.fetchall()

            sql = ("DELETE FROM Person WHERE resStateId = {} AND id NOT IN "
                   "(SELECT personId FROM Event WHERE Event.personId = Person.id)"
                   "".format(DELETED)
                  )
            #The delete in this way is to much less efficient and slow
            #sql = ("DELETE FROM Person WHERE Person.resStateId = {} "
            #       "AND Person.id NOT IN (SELECT Event.personId "
            #       "FROM Event WHERE personId IS NOT NULL)".format(DELETED)
            #      )
            #When doing in this way, it is important to exclude the events with
            #personId = NULL (Example: Accesses with button, door forced, etc).
            #If this is not done, the SQL sentence doesn't work.

            self.execute(sql)


            for toDelPerson in toDelPersons:

                toDelPersonFile = str(toDelPerson['id']) + '.' + PERS_IMG_FMT.lower()
                try:
                    os.remove(PERS_IMG_DIR + '/' + toDelPersonFile)
                except FileNotFoundError:
                    self.logger.warning('Person image: {} not found'.format(toDelPersonFile))

            return delEvents

        except (pymysql.err.IntegrityError, pymysql.err.InternalError) as dbEventError:
            self.logger.debug(dbEventError)
            raise EventError('Can not delete events or persons without events')



#-------------------------------------User--------------------------------------------

    def getUser(self, userId=None, username=None,):
        '''
        Return a dictionary with user fields if exists, if not it returns None
        '''

        if (userId and username) or (not userId and not username):
            self.logger.debug("Incorrect arguments calling getUser method.")
            raise UserError('Can not get User')

        elif userId:
            sql = "SELECT * from User WHERE id = '{}'".format(userId)

        else:
            sql = "SELECT * from User WHERE username = '{}'".format(username)

        try:
            self.execute(sql)
            user = self.cursor.fetchone()

            if not user:
                raise UserNotFound("User not found.")
            return user

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise UserError('Can not get User')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise UserError('Can not get User')



    def getUsers(self):
        '''
        Return a dictionary with all Users
        '''
        try:
            sql = ('SELECT * FROM User')
            self.execute(sql)
            users = self.cursor.fetchall()
            return users

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise UserError('Can not get Users')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise UserError('Can not get Users')



    def addUser(self, user):
        '''
        Receive a dictionary with user parametters and save it in DB
        It returns the id of the added user.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        user = self.escapeDict(user)

        passwdHash = crypt.crypt(user['passwd'], crypt.METHOD_MD5)

        sql = ("INSERT INTO User(username, passwdHash, fullName, roleId, language, active) "
               "VALUES('{}', '{}', '{}', {}, '{}', {})"
               "".format(user['username'], passwdHash, user['fullName'],
                         user['roleId'], user['language'], user['active'])
              )


        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise UserError('Can not add this user')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise UserError('Can not add this user')







    def delUser(self, userId):
        '''
        Mark de User as TO_DELETE state if it has persons on it
        or as DELETED if there is not more persons on it
        '''

        sql = "DELETE FROM User WHERE id = {}".format(userId)
        
        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise UserNotFound('User not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise UserError('Can not delete this user')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise UserError('Can not delete this user: wrong argument')







    def updUser(self, user):
        '''
        Receive a dictionary with user parametters and update it in DB
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        user = self.escapeDict(user)

        try:
            setUsername = ", username = '{}'".format(user['username'])
        except KeyError:
            setUsername = ""

        try:
            passwdHash = crypt.crypt(user['passwd'], crypt.METHOD_MD5)
            setPasswdHash = ", passwdHash = '{}'".format(passwdHash)
        except KeyError:
            setPasswdHash = ""

        try:
            setFullName = ", fullName = '{}'".format(user['fullName'])
        except KeyError:
            setFullName = ""
        
        try:
            setRoleId = ", roleId = {}".format(user['roleId'])
        except KeyError:
            setRoleId = ""

        try:
            setLanguage = ", language = '{}'".format(user['language'])
        except KeyError:
            setLanguage = ""

        try:
            setActive = ", active = {}".format(user['active'])
        except KeyError:
            setActive = ""



        sql = ("UPDATE User SET id = {}{}{}{}{}{}{} WHERE id = {}"
               "".format(user['id'], setUsername, setPasswdHash, 
                         setFullName, setRoleId, setLanguage,
                         setActive, user['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise UserNotFound('User not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise UserError('Can not update this user')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise UserError('Can not update this user: wrong argument')








#----------------------------------Row State------------------------------------------

    def getResStates(self):
        '''
        Return a a dictionary with all resStates
        '''
        try:
            sql = ('SELECT * FROM ResState')
            self.execute(sql)
            resStates = self.cursor.fetchall()
            return resStates

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise ResStateError('Can not get Row States')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ResStateError('Can not get Row States')




#----------------------------------Event Types------------------------------------------

    def getEventTypes(self):
        '''
        Return a a dictionary with all Event Types
        '''

        try:
            sql = ('SELECT * FROM EventType')
            self.execute(sql)
            eventTypes = self.cursor.fetchall()
            return eventTypes

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise EventTypeError('Can not get Event Types')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise EventTypeError('Can not get Event Types')


#----------------------------------Door Locks---------------------------------------

    def getDoorLocks(self):
        '''
        Return a a dictionary with all DoorLocks
        '''

        try:
            sql = ('SELECT * FROM DoorLock')
            self.execute(sql)
            doorLocks = self.cursor.fetchall()
            return doorLocks

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise DoorLockError('Can not get DoorLocks')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorLockError('Can not get DoorLocks')




#----------------------------------Denial Causes-----------------------------------

    def getDenialCauses(self):
        '''
        Return a a dictionary with all Not Reasons
        '''

        try:
            sql = ('SELECT * FROM DenialCause')
            self.execute(sql)
            denialCauses = self.cursor.fetchall()
            return denialCauses

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise DenialCauseError('Can not get Denial Causes')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DenialCauseError('Can not get Denial Causes')





#----------------------------------Roles------------------------------------------

    def getRoles(self):
        '''
        Return a a dictionary with all system user roles
        '''

        try:
            sql = ('SELECT * FROM Role')
            self.execute(sql)
            roles = self.cursor.fetchall()
            return roles

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise RoleError('Can not get Roles')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise RoleError('Can not get Roles')




#----------------------------------Organization----------------------------------------


    def getOrganizations(self):
        '''
        Return a a dictionary with all organizations
        '''
        try:
            sql = ('SELECT * FROM Organization')
            self.execute(sql)
            organizations = self.cursor.fetchall()
            return organizations

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise OrganizationError('Can not get organizations')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get organizations')



    def getOrganization(self, orgId):
        '''
        Return a a dictionary with organization data
        '''
        try:
            sql = ('SELECT * FROM Organization WHERE id = {}'.format(orgId))
            self.execute(sql)
            organization = self.cursor.fetchone()
            if not organization:
                raise OrganizationNotFound('Organization not found')
            return organization

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise OrganizationError('Can not get specified organization')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get specified organization')


                                             

    def addOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and save it in DB
        It returns the id of the added organization.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        organization = self.escapeDict(organization)

        sql = ("INSERT INTO Organization(name, resStateId) VALUES('{}', {})"
               "".format(organization['name'], COMMITTED)
              )
        
        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not add this organization')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not add this organization')







    def delOrganization(self, orgId):
        '''
        Mark de Organization as TO_DELETE state if it has persons on it
        or as DELETED if there is not more persons on it
        '''

        if self.getOrgPersons(orgId, includeDeleted=False):
            sql = ("UPDATE Organization SET resStateId = {} WHERE id = {}"
                   "".format(TO_DELETE, orgId)
                  )
        else:
            sql = ("UPDATE Organization SET resStateId = {} WHERE id = {}"
                   "".format(DELETED, orgId)
                  )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationNotFound('Organization not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not update this organization')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not update this organization: wrong argument')







    def updOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and update it in DB
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        organization = self.escapeDict(organization)

        sql = ("UPDATE Organization SET name = '{}' WHERE id = {}"
               "".format(organization['name'], organization['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationNotFound('Organization not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not update this organization')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not update this organization: wrong argument')



    def delOrgIfNeed(self, personId):
        '''
        Mark the organization that personId belongs to as DELETED if the organization
        is marked as TO_DELETE and there is not more persons in this organization
        
        '''

        try:

            #Getting the orgId this person belong to
            sql = ("SELECT Organization.id, Organization.resStateId FROM Organization "
                   "JOIN Person ON (Organization.id = Person.orgId) WHERE Person.id = {}"
                   "".format(personId)
                  )
            self.execute(sql)
            row = self.cursor.fetchone()
            orgId, resStateId = row['id'], row['resStateId']

            if resStateId == TO_DELETE:

                #Gets the number of people who belong to this organization and who have
                #not yet been eliminated
                sql = ("SELECT COUNT(*) FROM Person WHERE orgId = {} AND resStateId != {}"
                       "".format(orgId, DELETED)
                      )
                self.execute(sql)
                personCount = self.cursor.fetchone()['COUNT(*)']

                #If personCount is 0, the organization can be deleted.
                if personCount == 0:
                    sql = ("UPDATE Organization SET resStateId = {} WHERE id = {}"
                           "".format(DELETED, orgId)
                          )
                    self.execute(sql)


        except TypeError:
            self.logger.debug('TypeError fetching orgId or count of persons')
            raise OrganizationError('Can not get organization from person')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not get organization from person')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get organization from person')





#----------------------------------Zone----------------------------------------


    def getZones(self):
        '''
        Return a a dictionary with all organizations
        '''
        try:
            sql = ('SELECT * FROM Zone')
            self.execute(sql)
            zones = self.cursor.fetchall()
            return zones

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise OrganizationError('Can not get organizations')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get organizations')



    def getZone(self, zoneId):
        '''
        Return a a dictionary with zone data
        '''
        try:
            sql = ('SELECT * FROM Zone WHERE id = {}'.format(zoneId))
            self.execute(sql)
            zone = self.cursor.fetchone()
            if not zone:
                raise ZoneNotFound('Zone not found')
            return zone

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise ZoneError('Can not get specified zone')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not get specified zone')



    def addZone(self, zone):
        '''
        Receive a dictionary with zone parametters and save it in DB
        It returns the id of the added zone.
        '''
        
        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        zone = self.escapeDict(zone)

        sql = ("INSERT INTO Zone(name) VALUES('{}')"
               "".format(zone['name'])
              )

        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not add this zone')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not add this zone: wrong argument')



    def delZone(self, zoneId):
        '''
        Receive a dictionary with id zone and delete the zone
        '''

        sql = ("DELETE FROM Zone WHERE id = {}"
               "".format(zoneId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ZoneNotFound('Zone not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not delete this zone')




    def updZone(self, zone):
        '''
        Receive a dictionary with zone parametters and update it in DB
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        zone = self.escapeDict(zone)

        sql = ("UPDATE Zone SET name = '{}' WHERE id = {}"
               "".format(zone['name'], zone['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ZoneNotFound('Zone not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not update this zone')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not update this zone: wrong argument')



#------------------------------Door Group--------------------------------




    def getDoorGroups(self):
        '''
        Return a dictionary with all Door Groups
        '''
        sql = ("SELECT * FROM DoorGroup")
        try:
            self.execute(sql)
            doorGroups = self.cursor.fetchall()
            return doorGroups

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise DoorGroupError('Can not get Door Groups')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorGroupError('Can not get Door Groups')



    def getDoorGroup(self, doorGroupId):
        '''
        Return a a dictionary with Door Group data
        '''
    
        sql = ("SELECT * FROM DoorGroup WHERE id = {}"
               "".format(doorGroupId)
              )
        try:
            self.execute(sql)
            doorGroup = self.cursor.fetchone()
            if not doorGroup:
                raise DoorGroupNotFound('Door Group not found')
            return doorGroup

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise DoorGroupError('Can not get specified Door Group')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorGroupError('Can not get specified Door Group')


    def addDoorGroup(self, doorGroup):
        '''
        Receive a dictionary with Door Group parametters 
        and save it in DB. It returns the id of the added Door Group.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        doorGroup = self.escapeDict(doorGroup)


        sql = ("INSERT INTO DoorGroup(name, isForVisit) VALUES('{}', {})"
               "".format(doorGroup['name'], doorGroup['isForVisit'])
              )

        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorGroupError('Can not add this Door Group')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorGroupError('Can not add this Door Group: wrong argument')



    def delDoorGroup(self, doorGroupId):
        '''
        Receive the Door Group ID and to delete it.
        '''

        sql = ("DELETE FROM DoorGroup WHERE id = {}"
               "".format(doorGroupId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorGroupNotFound('Door Group not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorGroupError('Can not delete this Door Group')




    def updDoorGroup(self, doorGroup):
        '''
        Receive a dictionary with Door Group parametters and update it in DB
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        doorGroup = self.escapeDict(doorGroup)

        sql = ("UPDATE DoorGroup SET name = '{}', isForVisit = {} WHERE id = {}"
               "".format(doorGroup['name'], doorGroup['isForVisit'], doorGroup['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorGroupNotFound('Door Group not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorGroupError('Can not update this Door Group')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorGroupError('Can not update this Door Group: wrong argument')




    def addDoorToDoorGroup(self, doorGroupId, doorId):
        '''
        Create a new row in DoorGroupDoor table with the combination
        doorGroupId, doorId
        '''

        sql = ("INSERT INTO DoorGroupDoor(doorGroupId, doorId) "
               "VALUES ({}, {})".format(doorGroupId, doorId)
              )

        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorGroupError('Can not add this door to Door Group')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorGroupError('Can not add this door to Door Group: wrong argument')




    def delDoorFromDoorGroup(self, doorGroupId, doorId):
        '''
        Delete the combination doorGroupId, doorId from the
        DoorGroupDoor table
        '''

        sql = ("DELETE FROM DoorGroupDoor WHERE "
               "doorGroupId = {} AND doorId = {}"
               "".format(doorGroupId, doorId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorGroupNotFound('Door not found in Door Group.')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorGroupError('Can not delete this Door from Door Group')




#-----------------------------------Visitors-----------------------------------------


    def getVisitors(self, visitedOrgId, doorGroupId, cardNumber, identNumber):
        '''
        Returns a list with visitors.
        It receive as arguments the ID of the organization the visitor is visiting,
        the Visit Door Group used by the visitor to enter the building, the card
        number of the visitor and the identification number of the visitor. Any of them
        can be None.
        If using "cardNumber" or "identNumber", the rest of the arguments has no sense
        to be different of None.
        Using "identNumber" is to retrieve data of deleted visitor that is going to enter
        again in the building. If there is more than one visitor with the same "identNumber",
        more than one will be returned but the GUI will use the first one.
        When using "identNumber" variable, the "restStateId" should be "DELETED". When
        using any of the other three variables, the "restStateId" should NOT be "DELETED"
        '''

        if visitedOrgId:
            visitedOrgFilter = "Person.visitedOrgId = {}".format(visitedOrgId)

        else:
            visitedOrgFilter = "Person.visitedOrgId IS NOT NULL"


        if doorGroupId:
            doorGroupFilter = (" AND DoorGroupDoor.doorGroupId = {}"
                                    "".format(doorGroupId)
                                   )
        else:
            doorGroupFilter = ''

        if cardNumber:
            cardNumberFilter = " AND Person.cardNumber = {}".format(cardNumber)
        else:
            cardNumberFilter = ''

        if identNumber:
            identNumberFilter = (" AND Person.identNumber = '{}' AND Person.resStateId = {}"
                                 .format(identNumber, DELETED)
                                )
        else:
            identNumberFilter = " AND Person.resStateId != {}".format(DELETED)

        #Using LEFT JOIN between Person table and Access table, because for any
        #strange reason the visitor has not access to the doors in the visit
        #door group. (It should never happen). If not using LEFT JOIN, no visitors
        #will be retrieved.
        #Using LEFT JOIN between Access and DoorGroupDoor because in a
        #strange situation, the Visit Door Group could be removed after the visitor
        #enter the building and no visitors will be retrieved, also if using
        #doorGroupId = None
        #Using DISTINCT to avoid having duplicates entries of visitors because the
        #same Visitor normally has access to more than one door (all the Visit Door Group)
        sql = ("SELECT DISTINCT Person.* FROM Person LEFT JOIN Access ON "
               "(Person.id = Access.personId) LEFT JOIN DoorGroupDoor "
               "ON (Access.doorId = DoorGroupDoor.doorId) "
               "WHERE {}{}{}{}"
               "".format(visitedOrgFilter, doorGroupFilter, 
                         cardNumberFilter, identNumberFilter)
              )

        try:
            self.execute(sql)
            visitors = self.cursor.fetchall()
            if not visitors:
                raise PersonNotFound('Visitors not found')
            return visitors

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise PersonError('Can not get specified visitors.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not get specified visitors.')
    


#--------------------------------Controller Model------------------------------------

    def getCtrllerModels(self):
        '''
        Return a list with all Controller Models availables in the system
        '''
        try:
            sql = ('SELECT * FROM CtrllerModel')
            self.execute(sql)
            ctrllerModels = self.cursor.fetchall()
            return ctrllerModels

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise CtrllerModelError('Can not get Controller Models')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise CtrllerModelError('Can not get Controller Models')



#----------------------------------Controller----------------------------------------



    def getController(self, controllerId):
        '''
        Return a dictionary with all the parametters of the controller
        receiving the ID of the controller
        '''
        try:
            sql = ('SELECT * FROM Controller WHERE id = {}'.format(controllerId))
            self.execute(sql)
            controller = self.cursor.fetchone()
            if not controller:
                raise ControllerNotFound('Controller not found')

            #Creating a list with all the doors that this controller can
            #handle. For example if this model of controller can handle
            #3 doors the list will be totalDoors = [1, 2, 3]
            sql = ("SELECT numOfDoors FROM Controller JOIN CtrllerModel "
                   "ON (Controller.ctrllerModelId = CtrllerModel.id) "
                   "WHERE Controller.id = {}".format(controllerId)
                  )
            self.execute(sql)      
            numOfDoors = self.cursor.fetchone()['numOfDoors']
            totalDoors = list(range(1, numOfDoors+1))
    
            #Creating a list all the used doors of this contoller
            #For example if the door 1 and 3 of the controller was used
            #the list will be usedDoors = [1, 3]
            sql = ("SELECT doorNum FROM Door WHERE controllerId = {}"
                   "".format(controllerId)
                  )
            self.execute(sql)
            usedDoors = self.cursor.fetchall()
            usedDoors = [usedDoor['doorNum'] for usedDoor in usedDoors]
            
            #Creating a list with the availables doors in the controller
            #(the doors not used). Whit the above examples, it will be
            #availDoors = [2]
            availDoors = [door for door in totalDoors if door not in usedDoors]

            #Adding the avialDoors list to the controller dictionary
            controller['availDoors'] = availDoors

            #Formatting lastSeen field
            if controller['lastSeen']:
                controller['lastSeen'] = controller['lastSeen'].strftime('%Y-%m-%d %H:%M:%S')

            return controller


        except TypeError:
            self.logger.debug('TypeError fetching "numOfDoors" or "usedDoors"')
            raise ControllerError('Can not get specified controller')

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise ControllerError('Can not get specified controller')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not get specified controller')





    def getControllers(self):
        '''
        Return a list with all controllers
        '''
        try:
            sql = ('SELECT id FROM Controller')
            self.execute(sql)
            controllerIds = self.cursor.fetchall()
            controllerIds = [controllerId['id'] for controllerId in controllerIds]

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise ControllerError('Can not get controllers')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not get controllers')



        controllers = []
        for controllerId in controllerIds:
            controllers.append(self.getController(controllerId))

        return controllers






    def addController(self, controller):
        '''
        Receive a dictionary with controller parametters and save it in DB
        It returns the id of the added controller.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        controller = self.escapeDict(controller)

        sql = ("INSERT INTO Controller(name, ctrllerModelId, macAddress) "
               "VALUES('{}', {}, '{}')"
               "".format(controller['name'], controller['ctrllerModelId'], 
                         controller['macAddress'])
              )

        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not add this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not add this controller: wrong argument')






    def delController(self, controllerId):
        '''
        Receive a dictionary with id controller and delete the controller
        '''

        sql = ("DELETE FROM Controller WHERE id = {}"
               "".format(controllerId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ControllerNotFound('Controller not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not delete this controller, first delete all doors that belongs to it.')




    def updController(self, controller):
        '''
        Receive a dictionary with controller parametters and update it in DB
        When updating a controller, the MAC address could be changed. 
        In this case, a Person Pending Operation could be in the "PersonPendingOperation"
        table. This situation is very possible when replacing a died controller for a
        new one.
        For this situation, the new MAC address should be replaced in 
        "PersonPendingOperation" table.
        To avoid inconsistency, both tables are locked before modifying them.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        controller = self.escapeDict(controller)


        try:

            sql = "LOCK TABLES Controller WRITE, PersonPendingOperation WRITE"
            self.execute(sql)


            sql = ("SELECT macAddress FROM Controller WHERE id = {}"
                   "".format(controller['id'])
                  )

            self.execute(sql)
            oldMacAddress = self.cursor.fetchone()['macAddress']


            sql = ("UPDATE Controller SET name = '{}', ctrllerModelId = {}, "
                   "macAddress = '{}' WHERE id = {}"
                   "".format(controller['name'], controller['ctrllerModelId'], 
                             controller['macAddress'], controller['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise ControllerNotFound('Controller not found')


            sql = ("UPDATE PersonPendingOperation SET macAddress = '{}' "
                   "WHERE macAddress = '{}'"
                   "".format(controller['macAddress'], oldMacAddress)
                  )

            self.execute(sql)
    
            self.execute("UNLOCK TABLES")



        except TypeError:
            self.logger.debug('This controller id has not any MAC associated.')
            self.execute("UNLOCK TABLES")
            raise ControllerNotFound('Controller not found')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.execute("UNLOCK TABLES")
            raise ControllerError('Can not update this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.execute("UNLOCK TABLES")
            raise ControllerError('Can not update this controller: wrong argument')






    def getControllerMac(self, controllerId=None, doorId=None):
        '''
        Return the controller MAC address receiving the controller ID or door ID
        '''

        if (controllerId and doorId) or (not controllerId and not doorId):
            self.logger.debug("Incorrect arguments calling getControllerMac method.")
            raise ControllerError('Error getting the controller.')
            

        if controllerId:
            sql = ("SELECT controller.macAddress FROM Controller controller WHERE "
                   "id = {}".format(controllerId)
                  )
            try:
                self.execute(sql)
                return self.cursor.fetchone()['macAddress']

            except TypeError:
                self.logger.debug('This controller id has not any MAC associated.')
                raise ControllerNotFound('Controller not found')


        else:
            sql = ("SELECT controller.macAddress FROM Controller controller JOIN "
                   "Door door ON (controller.id = door.controllerId) WHERE "
                   "door.id = {}".format(doorId)
                  )

            try:
                self.execute(sql)
                return self.cursor.fetchone()['macAddress']

            except TypeError:
                self.logger.debug('This door id is not present in any controller.')
                raise DoorNotFound('Door not found')




    def getCtrllerMacsToDelPrsn(self, personId):
        '''
        Return a list of controller MAC addresses receiving the person ID
        to delete.
        '''
        
        sql = ("SELECT macAddress FROM Controller controller JOIN Door door "
               "ON (controller.id = door.controllerId) JOIN Access access "
               "ON (door.id = access.doorId) JOIN Person person "
               "ON (access.personId = person.id) WHERE person.resStateId = {} AND "
               "person.id = {}".format(TO_DELETE, personId)
              )

        try:
            self.execute(sql)
            ctrllerMacsToDelPrsn = self.cursor.fetchall()
            ctrllerMacsToDelPrsn = [ctrllerMac['macAddress'] for ctrllerMac in ctrllerMacsToDelPrsn]
            if ctrllerMacsToDelPrsn == []:
                raise TypeError
            return ctrllerMacsToDelPrsn

        except TypeError:
            self.logger.debug('This person is not present in any controller')
            raise PersonNotFound('Person not found') #We should check what to do when the person only in local db






    def getUncmtCtrllerMacs(self):
        '''
        Return a list of controller MAC addresses of controllers which did not respond
        to crud messages.
        '''

        sql = ("SELECT controller.macAddress FROM Controller controller JOIN Door door "
               "ON (controller.id = door.controllerId) WHERE door.resStateId IN ({0}, {1}, {2}) "
               "UNION "
               "SELECT controller.macAddress FROM Controller controller JOIN Door door ON "
               "(controller.id = door.controllerId) JOIN LimitedAccess limitedAccess ON "
               "(door.id = limitedAccess.doorId) WHERE limitedAccess.resStateId IN ({0}, {1}, {2}) "
               "UNION "
               "SELECT controller.macAddress FROM Controller controller JOIN Door door ON "
               "(controller.id = door.controllerId) JOIN Access access ON "
               "(door.id = access.doorId) WHERE access.resStateId IN ({0}, {1}, {2}) "
               "UNION "
               "SELECT macAddress FROM PersonPendingOperation"
               "".format(TO_ADD, TO_UPDATE, TO_DELETE)
              )

        try:
            self.execute(sql)
            ctrllerMacsNotComm = self.cursor.fetchall()
            ctrllerMacsNotComm = [ctrllerMac['macAddress'] for ctrllerMac in ctrllerMacsNotComm]
            return ctrllerMacsNotComm


        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Error getting MAC addresses of not committed controllers')

        except TypeError:
            self.logger.debug(internalError)
            raise ControllerError('Error getting MAC addresses of not committed controllers')




    def reProvController(self, controllerId):
        '''
        This method is called by CRUD module when it is necessary to 
        reprovision an entire controller.
        It sets all doors, access and limited access in state TO_ADD.
        Receive a dictionary with controller parametters and update it in central DB
        because MAC address and board model can change.
        '''
        try:

            sql = ("UPDATE Door SET resStateId = {} WHERE controllerId = {}"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)

            sql = "LOCK TABLES Door WRITE, Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            sql = ("UPDATE Access SET resStateId = {} WHERE doorId IN "
                   "(SELECT id FROM Door WHERE controllerId = {}) AND allWeek = 1"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)

            sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE doorId IN "
                   "(SELECT id FROM Door WHERE controllerId = {})"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)

            self.execute("UNLOCK TABLES")
        

        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise ControllerError('Error reprovisioning the controller.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Error reprovisioning the controller.')





    def setCtrllerReachable(self, ctrllerMac):
        '''
        Set "reachable" and update "lastSeen" date and time of the controller
        which MAC address is received as argument.
        If the controller wasn't previously alive, returns a dictionary with 
        the controller parametters.
        '''

        dateTimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            #A JSON of the controller should be returned if the controller wasn't previously alive.
            #If it was previously alive, no JSON should be returned and "revivedCtrller" will be None
            sql = ("SELECT 1 AS reachable, name, macAddress, '{}' AS lastSeen FROM Controller WHERE "
                   "macAddress = '{}' AND reachable = {}".format(dateTimeNow, ctrllerMac, 0)
                  )
            self.execute(sql)
            revivedCtrller = self.cursor.fetchone()

            #Every time a keep alive message is received, "lastSeen" column should
            #be updated with now date and time.
            sql = ("UPDATE Controller SET lastSeen = '{}', reachable = 1 WHERE "
                   "macAddress = '{}'".format(dateTimeNow, ctrllerMac)
                  )
            self.execute(sql)

            return revivedCtrller

        except (pymysql.err.IntegrityError, pymysql.err.InternalError) as dbEventError:
            self.logger.debug(dbEventError)
            raise ControllerError('Can not update last seen and set reachable for this controller.')





    def setCtrllersNotReachable(self):
        '''
        The current date and time is substracted by the amount of minutes 
        "CONSIDER_DIED_MINS" (config parametter).
        If there are controllers which the previous state was "reachable"
        and didn't send keep alive messages in that interval of time, they
        are returned in the "deadCtrllers" list and they are updated as 
        "not reachables"
        '''

        diedDateTime = datetime.datetime.now() - datetime.timedelta(minutes=CONSIDER_DIED_MINS)
        diedDateTime = diedDateTime.strftime('%Y-%m-%d %H:%M:%S')

        try:

            sql = ("SELECT 0 AS reachable, name, macAddress, lastSeen FROM "
                   "Controller WHERE reachable = 1 AND lastSeen < '{}'"
                   "".format(diedDateTime)
                  )
            self.execute(sql)
            deadCtrllers = self.cursor.fetchall()

            sql = ("UPDATE Controller SET reachable = 0 WHERE reachable = 1 AND lastSeen < '{}'"
                   "".format(diedDateTime)
                  )
            self.execute(sql)

            #deadCtrllers could be an empty tuple if all controllers are alive
            #and the following for loop will not be executed
            for deadCtrller in deadCtrllers:
                deadCtrller['lastSeen'] = deadCtrller['lastSeen'].strftime('%Y-%m-%d %H:%M:%S')

            #deadCtrllers could be an empty tuple if all controllers are alive
            #and we are returning empty tuple and the for loop of "lifeChcker" thread
            #will not be executed
            return deadCtrllers

        except (pymysql.err.IntegrityError, pymysql.err.InternalError) as dbEventError:
            self.logger.debug(dbEventError)
            raise ControllerError('Can not set contollers as not reachable.')





#----------------------------------Door----------------------------------------


    def getDoors(self, zoneId=None, doorGroupId=None):
        '''
        Return a dictionary with all doors in a Zone or in a Door Group
        according to the argument received
        '''

        try:
            if not zoneId and not doorGroupId:
                raise DoorNotFound('getDoors method need zoneId or doorGroupId.')

            elif zoneId:
                #Check if the zoneId exists in the database
                sql = ("SELECT * FROM Zone WHERE id = {}".format(zoneId))
                self.execute(sql)
                zone = self.cursor.fetchone()

                if not zone:
                    raise ZoneNotFound('Zone not found')
       
                #Get all doors from this zone
                sql = ("SELECT * FROM Door WHERE zoneId = {}".format(zoneId))
                self.execute(sql)
                doors = self.cursor.fetchall()

            elif doorGroupId:
                #Check if the doorGroup exists in database
                sql = ("SELECT * FROM DoorGroup WHERE id = {}".format(doorGroupId))
                self.execute(sql)
                doorGroup = self.cursor.fetchone()

                if not doorGroup:
                    raise DoorGroupNotFound('Door Group not found')

                #Get all doors from this DoorGroup 
                sql = ("SELECT Door.* from Door JOIN DoorGroupDoor "
                       "ON (Door.id = DoorGroupDoor.doorId) "
                       "WHERE DoorGroupDoor.doorGroupId = {}"
                       "".format(doorGroupId)
                       )
                self.execute(sql)
                doors = self.cursor.fetchall()

            return doors


        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Can not get doors for this zone or doorGroup.')




    def getDoor(self, doorId):
        '''
        Receive door id and returns a dictionary with door parameters.
        '''
        try:
            sql = "SELECT * FROM Door WHERE id = {}".format(doorId)
            self.execute(sql)
            door = self.cursor.fetchone()

            if not door:
                raise DoorNotFound("Door not found.")

            return door

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Can not get door with this ID.')





    def getUncmtDoors(self, ctrllerMac, resStateId):
        '''
        This method is an iterator, in each iteration it returns a door
        not committed with the state "resStateId" from the controller
        with the MAC address "ctrllerMac"
        NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created (not happening today)
        '''
        try:

            localCursor = self.connection.cursor(pymysql.cursors.DictCursor)

            sql = ("SELECT Door.* FROM Door JOIN Controller "
                   "ON (Door.controllerId = Controller.id) "
                   "WHERE Controller.macAddress = '{}' AND "
                   "resStateId = {}".format(ctrllerMac, resStateId))


            localCursor.execute(sql)
            self.connection.commit()
            door = localCursor.fetchone()

            while door:
                #Removing fields that should not be sent to the controller
                door.pop('resStateId')
                yield door
                door = localCursor.fetchone()

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Error getting doors of not committed controllers')




    def addDoor(self, door):
        '''
        Receive a dictionary with door parametters and save it in DB
        It returns the id of the added door
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        door = self.escapeDict(door)

        sql = ("INSERT INTO Door(doorNum, name, controllerId, snsrType, rlseTime, bzzrTime, "
               "alrmTime, zoneId, isVisitExit, resStateId) VALUES({}, '{}', {}, {}, {}, {}, {}, {}, {}, {})"
               "".format(door['doorNum'], door['name'], door['controllerId'], door['snsrType'], 
                         door['rlseTime'], door['bzzrTime'], door['alrmTime'], 
                         door['zoneId'], door['isVisitExit'], TO_ADD)
              )


        try:
            self.execute(sql)
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorError('Can not add this door')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Can not add this door: wrong argument')



    def commitDoor(self, doorId):
        '''
        Mark the door in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state or delete it if it was previously in TO_DELETE state
        '''
 
        sql = "SELECT resStateId FROM Door WHERE id = {}".format(doorId)

        try:
            self.execute(sql)
            resState = self.cursor.fetchone()['resStateId']

            if resState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Door SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, doorId)
                      )
                self.execute(sql)

            elif resState == TO_DELETE:
                sql = ("DELETE FROM Door WHERE id = {}"
                       "".format(doorId)
                      )
                self.execute(sql)

            elif resState == COMMITTED:
                self.logger.info("Door already committed.")

            else:
                self.logger.error("Invalid state detected in door table.")
                raise DoorError('Error committing a door.')


        except TypeError:
            self.logger.debug('Error fetching a door.')
            self.logger.warning('The door to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.logger.warning('Error committing a door.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing a door.')



    def markDoorToDel(self, doorId):
        '''
        Set door row state in state: TO_DELETE (pending to delete).
        '''

        sql = ("UPDATE Door SET resStateId = {} WHERE id = {}"
               "".format(TO_DELETE, doorId)
              )
        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorNotFound('Door not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorError('Error marking the Door to be deleted.')
        



    def updDoor(self, door):
        '''
        Receive a dictionary with door parametters and update it in DB
        Returns True if the controller where the door is located need
        to be updated, otherwise, returns false
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        door = self.escapeDict(door)

        try:
            #Getting the parameters that should be modified in the
            #controller before modifying them in central database.
            sql = ("SELECT doorNum, snsrType, rlseTime, bzzrTime, alrmTime "
                   "FROM Door WHERE id = {}".format(door['id'])
                  )
            self.execute(sql)
            oldParams =  self.cursor.fetchone()

            #If any of the parameters should be modified in the controller, 
            #set the "resStateId" as TO_UPDATE to wait the response of the controller.
            #If no parameter should be modified in the controller, set the
            #"resStateId" as COMMITED
            if int(door['doorNum']) != oldParams['doorNum'] or \
               int(door['snsrType']) != oldParams['snsrType'] or \
               int(door['rlseTime']) != oldParams['rlseTime'] or \
               int(door['bzzrTime']) != oldParams['bzzrTime'] or \
               int(door['alrmTime']) != oldParams['alrmTime']:
                resStateId = TO_UPDATE
                needUpdCtrller = True
            else:
                resStateId = COMMITTED
                needUpdCtrller = False



            sql = ("UPDATE Door SET doorNum = {}, name = '{}', snsrType = {}, "
                   "rlseTime = {}, bzzrTime = {}, alrmTime = {}, zoneId = {}, "
                   "isVisitExit = {}, resStateId = {} WHERE id = {}"
                   "".format(door['doorNum'], door['name'], door['snsrType'],
                             door['rlseTime'], door['bzzrTime'], door['alrmTime'],
                             door['zoneId'], door['isVisitExit'], resStateId, door['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorNotFound('Door not found')

            return needUpdCtrller

        except TypeError:
            self.logger.debug('Error trying to retrieve old door parameters.')
            raise DoorNotFound('Door not found')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorError('Can not update this door')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Can not update this door: wrong argument')





#-------------------------------Person-----------------------------------


    def getPersons(self, identNumber=None, cardNumber=None,
                   namesPattern=None, lastNamePattern=None):
        '''
        Return a dictionary with all persons in an organization,
        By default the method also retrieve the persons mark as DELETED.
        If "includeDeleted" flag is set to False, it will only return all
        the persons not marked as DELETED
        '''

        if identNumber == None and \
           cardNumber == None and \
           namesPattern == None and \
           lastNamePattern == None:
            raise PersonError('Can not get specified persons.')

        personFilter = []

        if identNumber:
            personFilter.append("Person.identNumber = '{}'".format(identNumber))

        if cardNumber:
            personFilter.append("Person.cardNumber = {}".format(cardNumber))

        if namesPattern:
            personFilter.append("Person.names LIKE '%{}%'".format(namesPattern))

        if lastNamePattern:
            personFilter.append("Person.lastName LIKE '%{}%'".format(lastNamePattern))

        personFilter = " AND ".join(personFilter)


        sql = ("SELECT Person.names, Person.lastName, Organization.name AS orgName, "
               "Person.identNumber, Person.note, Person.cardNumber FROM Person JOIN "
               "Organization ON (Person.orgId = Organization.id) WHERE "
               "Person.visitedOrgId IS NULL AND Person.resStateId != {} AND {} LIMIT 10"
               "".format(DELETED, personFilter)
              )

        try:
            self.execute(sql)
            persons = self.cursor.fetchall()
            if not persons:
                raise PersonNotFound('Persons not found')
            return persons

        except pymysql.err.ProgrammingError as programmingError:
            self.logger.debug(programmingError)
            raise PersonError('Can not get specified persons.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not get specified persons.')





    def getOrgPersons(self, orgId, includeDeleted=True):
        '''
        Return a dictionary with all persons in an organization,
        By default the method also retrieve the persons mark as DELETED.
        If "includeDeleted" flag is set to False, it will only return all
        the persons not marked as DELETED
        '''
        
        try:
        
            #check if the organization id exist in the database
            sql = ("SELECT * FROM Organization WHERE id='{}'".format(orgId))
            self.execute(sql)
            organization = self.cursor.fetchone()

            if not organization:
                raise OrganizationNotFound('Organization not found')
        
            # Get all persons from the organization
            if includeDeleted:
                sql = "SELECT * FROM Person WHERE orgId = {}".format(orgId)

            else:
                sql = ("SELECT * FROM Person WHERE orgId = {} AND resStateId != {}"
                       "".format(orgId, DELETED)
                      )
            self.execute(sql)
            persons = self.cursor.fetchall()
        
            return persons


        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get persons from this organization')






    def getUncmtPersons(self, ctrllerMac, resStateId):
        '''
        This method is an iterator, in each iteration it returns a person
        not committed with the state "resStateId" from the controller
        with the MAC address "ctrllerMac"
        NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created (not happening today)
        '''

        try:
            localCursor = self.connection.cursor(pymysql.cursors.DictCursor)
            sql = ("SELECT person.* FROM "
                   "Person person JOIN PersonPendingOperation personPendingOperation ON "
                   "(person.id = personPendingOperation.personId) WHERE "
                   "personPendingOperation.macAddress = '{}' AND personPendingOperation.pendingOp = {}"
                   "".format(ctrllerMac, resStateId)
                  )

            localCursor.execute(sql)
            self.connection.commit()
            person = localCursor.fetchone()

            while person:
                #Removing the resStateId as this field should not be sent to the controller
                person.pop('resStateId')
                yield person
                person = localCursor.fetchone()

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Error getting persons of not committed controllers')





    def addPerson(self, person):
        '''
        Receive a dictionary with person parametters and save it in DB
        The person row is inserted in COMMITTED state since the person is not sent to
        controller at the moment it is inserted here. It it sent to the controller when
        an access is created.
        If a visitor is being added and the system already have the visitor with the same
        "identNumber" and "restStateId = DELETED", instead of adding a new row, the old
        row is updated with the new card, name, etc.
        If a not visitor person is being added with the same "identNumber" of some deleted
        visitor a new row will be generated with INSERT (not UPDATE will be performed).
        The same will happen if a not visitor person is being added with the same
        "identNumber" of a not visitor person. (Two persons with the same "identNumber
        could be").
        Also INSERT will be performed with two active visitors with the same "identNumber".
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        person = self.escapeDict(person)

        #Changing None to 'NULL' for writting correct SQL syntax below.
        if not person['visitedOrgId']:
            visitedOrgId = 'NULL'
        else:
            visitedOrgId = person['visitedOrgId']


        try:

            sql = ("SELECT id FROM Person WHERE identNumber = '{}' "
                   "AND visitedOrgId IS NOT NULL AND resStateId = {}"
                   "".format(person['identNumber'], DELETED)
                  )

            self.execute(sql)
            row = self.cursor.fetchone()

            if row and person['visitedOrgId']:
                personId = row['id']

                sql = ("UPDATE Person SET names = '{}', lastName = '{}', cardNumber = {}, "
                       "note = '{}', visitedOrgId = {}, isProvider = {}, resStateId = {} "
                       "WHERE id = {}".format(person['names'], person['lastName'], 
                                              person['cardNumber'], person['note'], 
                                              visitedOrgId, person['isProvider'],
                                              COMMITTED, personId)
                      )
                self.execute(sql)
                return personId

            else:
                sql = ("INSERT INTO Person(names, lastName, identNumber, note, cardNumber, orgId, "
                       "visitedOrgId, isProvider, resStateId) VALUES('{}', '{}', '{}', '{}', {}, {}, {}, {}, {})"
                       "".format(person['names'], person['lastName'], person['identNumber'], person['note'],
                                 person['cardNumber'], person['orgId'], visitedOrgId, person['isProvider'], COMMITTED)

                     )
                self.execute(sql)
                return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError("Can't add this person. Card number already exists.")
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError("Can not add this person. Internal error.")





    def markPerson(self, personId, operation):
        '''
        Set person row state in state: TO_DELETE (pending to delete) or
        TO_UPDATE (pending to update).
        Receive personId and operation (TO_DELETE or TO_UPDATE).
        Return a list of controller MAC addresses where the person should 
        be deleted.
        '''

        try:

            sql = ("UPDATE Person SET resStateId = {} WHERE id = {}"
                   "".format(operation, personId)
                  )
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')



            #If the operation is TO_DELETE, and we still have access pending to add (TO_ADD),
            #those accesses should be deleted in central DB and the controller should never
            #be aware of this situation
            if operation == TO_DELETE:
                sql = ("DELETE FROM Access WHERE resStateId = {} AND personId = {}"
                       "".format(TO_ADD, personId)
                      )
                self.execute(sql)

                sql = ("DELETE FROM LimitedAccess WHERE resStateId = {} AND personId = {}"
                       "".format(TO_ADD, personId)
                      )
                self.execute(sql)

                sql = ("SELECT doorId FROM Access WHERE personId = {} AND allWeek = 0"
                       "".format(personId)
                      )

                self.execute(sql)
                doorIds = self.cursor.fetchall()
                doorIds = [doorId['doorId'] for doorId in doorIds]
                for doorId in doorIds:
                    sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE doorId = {} AND "
                           "personId = {}".format(doorId, personId)
                          )
                    self.execute(sql)
                    count = self.cursor.fetchone()['COUNT(*)']
                    if count == 0:
                        sql = ("DELETE FROM Access WHERE doorId = {} "
                               "AND personId = {} AND allWeek = 0"
                               "".format(doorId, personId)
                              )
                        self.execute(sql)



            #To avoid having duplicate MACs in the result list, it is used DISTINCT clause
            #since we can have a Person having access in more than one door
            #and those door could be on the same controller (with the same MAC)
            sql = ("SELECT DISTINCT macAddress FROM Controller controller JOIN Door door "
                   "ON (controller.id = door.controllerId) JOIN Access access "
                   "ON (door.id = access.doorId) JOIN Person person "
                   "ON (access.personId = person.id) WHERE person.id = {}"
                   "".format(personId)
                  )

            self.execute(sql)
            ctrllerMacs = self.cursor.fetchall()
            ctrllerMacs = [ctrllerMac['macAddress'] for ctrllerMac in ctrllerMacs]

            #If the person is not present in any controller, we should log this situation and
            #remove it from the central DB.
            if ctrllerMacs == []:
                if operation == TO_DELETE:
                    logMsg = ("This person is not present in any controller. "
                              "Marking it as deleted in central DB." 
                             )
                    self.logger.debug(logMsg)
                    #Setting the "cardNumber" = NULL to be able to use this card in
                    #another future person.
                    #Leaving the "identNumber" stored. In this way, when a person is
                    #deleted and readded (typically a frequent visitor), with the 
                    #ON DUPLICATE KEY UPDATE clause of the "addPerson" method, the 
                    #same row in the database is used, avoiding duplicate with the same person.
                    sql = ("UPDATE Person SET cardNumber = NULL, resStateId = {} "
                           "WHERE id = {}".format(DELETED, personId)
                          )
                    self.execute(sql)

                    self.delOrgIfNeed(personId)

                elif operation == TO_UPDATE:
                    logMsg = ("This person is not present in any controller. "
                              "Just modifying it in central DB."
                             )
                    self.logger.debug(logMsg)
                    sql = ("UPDATE Person SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, personId)
                          )
                    self.execute(sql)
            else:
                #Adding in PersonPendingOperation table: personId, mac address and pending operation
                #Each entry on this table will be removed when each controller answer to the delete 
                #person message.
                values = ''
                for mac in ctrllerMacs:
                    values += "({}, '{}', {}), ".format(personId, mac, operation)
                #Removing the last coma and space
                values = values[:-2]
                #Using INSERT IGNORE to avoid having duplicates entries on this table (This situation can happen
                #if the server receive more than once a REST command to delete a person and the controller does not
                #confirm the deletion of this person.)
                sql = ("INSERT IGNORE INTO PersonPendingOperation(personId, macAddress, pendingOp) VALUES {}"
                       "".format(values)
                      )
                self.execute(sql)

            #If the list of MACs is void or not, we always return it.
            return ctrllerMacs

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not add this person')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not add this person: wrong argument')

        




    def commitPerson(self, personId, ctrllerMac):
        '''
        Receive personId and controller MAC.
        First of all it determines the pendig operation of that person on that controller.

        If the operation is TO_DELETE: it deletes all the accesses and limited accesses of
        this person on the doors managed by this controller. 
        Then it deletes the entry in "PersonPendingOperation" table which has this person id,
        this MAC and the corresponding pending operation. 
        If there is not more entries on "PersonPendingOperation" table with this person and 
        this operation type, it can delete the person definitely from the central database.
        '''

        try:
            #Determines the pendig operation of that person on that controller
            sql = "SELECT resStateId FROM Person WHERE id = {}".format(personId)

            self.execute(sql)
            row = self.cursor.fetchone()
            resState = row['resStateId']

            if resState == TO_DELETE:

                sql = ("LOCK TABLES Controller WRITE, "
                       "Door WRITE, Access WRITE, LimitedAccess WRITE"
                      )
                self.execute(sql)

                #Deleting all limited accesses of this person on the doors managed by 
                #this controller
                sql = ("DELETE FROM LimitedAccess WHERE personId = {} AND doorId IN "
                       "(SELECT door.id FROM Door door JOIN Controller controller ON "
                       "(door.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.execute(sql)

                #Deleting all accesses of this person on the doors managed by 
                #this controller
                sql = ("DELETE FROM Access WHERE personId = {} AND doorId IN "
                       "(SELECT door.id FROM Door door JOIN Controller controller ON "
                       "(door.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.execute(sql)

                self.execute("UNLOCK TABLES")

                #Deleting the entry in "PersonPendingOperation" table which has this person id,
                #this MAC and the corresponding pending operation.
                sql = ("DELETE FROM PersonPendingOperation WHERE personId = {} AND macAddress = '{}' "
                       "AND pendingOp = {}".format(personId, ctrllerMac, TO_DELETE)
                      )
                self.execute(sql)

                #If there is not more entries on "PersonPendingOperation" table with this person and 
                #this operation type, it can delete the person definitely from the central database.                
                sql = ("SELECT COUNT(*) FROM PersonPendingOperation WHERE personId = {} "
                       "AND pendingOp = {}".format(personId, TO_DELETE)
                      )
                self.execute(sql)
                pendCtrllersToDel = self.cursor.fetchone()['COUNT(*)']
                if not pendCtrllersToDel:
                    #Setting the "cardNumber" = NULL to be able to use this card in
                    #another future person.
                    #Leaving the "identNumber" stored. In this way, when a person is
                    #deleted and readded (typically a frequent visitor), with the 
                    #ON DUPLICATE KEY UPDATE clause of the "addPerson" method, the 
                    #same row in the database is used, avoiding duplicate with the same person.
                    sql = ("UPDATE Person SET cardNumber = NULL, resStateId = {} "
                           "WHERE id = {}".format(DELETED, personId)
                          )
                    self.execute(sql)

                self.delOrgIfNeed(personId)


            elif resState == TO_UPDATE:
                #Deleting the entry in "PersonPendingOperation" table which has this person id,
                #this MAC and the corresponding pending operation.
                sql = ("DELETE FROM PersonPendingOperation WHERE personId = {} AND macAddress = '{}' "
                       "AND pendingOp = {}".format(personId, ctrllerMac, TO_UPDATE)
                      )
                self.execute(sql)

                #If there is not more entries on "PersonPendingOperation" table with this person and 
                #this operation type, it can set the person row state as COMMITTED definitely in the 
                #central database.                
                sql = ("SELECT COUNT(*) FROM PersonPendingOperation WHERE personId = {} "
                       "AND pendingOp = {}".format(personId, TO_UPDATE)
                      )
                self.execute(sql)
                pendCtrllersToUpd = self.cursor.fetchone()['COUNT(*)']
                if not pendCtrllersToUpd:
                    sql = "UPDATE Person SET resStateId = {} WHERE id = {}".format(COMMITTED, personId)
                    self.execute(sql)

            elif resState == COMMITTED:
                self.logger.info('Person already committed.')

            elif resState == DELETED:
                self.logger.info('Person already deleted.')

            else:
                self.logger.debug('Invalid state detected in Person table.')
                raise PersonError('Can not commit this person.')


        except TypeError:
            self.logger.debug('Error fetching a person.')
            self.logger.warning('The person to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            self.logger.warning('Error committing a person.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing a person.')






    def delPerson(self, person):
        '''
        Receive a dictionary with id organization
        '''

        sql = ("DELETE FROM Person WHERE id = {}"
               "".format(person['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not delete this person')





    def updPerson(self, person):
        '''
        Receive a dictionary with new person parametters.
        Return True if controllers need to be updated.
        Return False if there is no need to update the controllers.
        '''

        #Escaping special characters of the input values
        #of the dictionary like quote or double quote.
        person = self.escapeDict(person)

        if not person['visitedOrgId']:
            person['visitedOrgId'] = 'NULL'


        try:
            #Saving old card number before updating to know if it is necessary
            #to update it in the controller
            sql = "SELECT cardNumber FROM Person WHERE id = {}".format(person['id'])
            self.execute(sql)
            oldCardNumber = self.cursor.fetchone()['cardNumber']


            sql = ("UPDATE Person SET names = '{}', lastName = '{}', identNumber = '{}', note = '{}', "
                   "cardNumber = {}, orgId = {}, visitedOrgId = {}, isProvider = {}  WHERE id = {}"
                   "".format(person['names'], person['lastName'], person['identNumber'], person['note'],
                             person['cardNumber'], person['orgId'], person['visitedOrgId'], person['isProvider'], 
                             person['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')

            if oldCardNumber != int(person['cardNumber']):
                return True
            else:
                return False


        except TypeError:
            self.logger.debug('Error trying to retrieve old card number.')
            raise PersonNotFound('Person not found')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError("Can't update this person. Card number or Identification number already exists.")
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError("Can't update this person. Internal error.")





    def getPerson(self, personId):
        '''
        Receive person id and returns a dictionary with person parameters.
        '''
        try:
            sql = "SELECT * FROM Person WHERE id = {}".format(personId)
            self.execute(sql)
            person = self.cursor.fetchone()

            if not person:
                raise PersonNotFound("Person not found.")
            return person

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not get person with this ID.')




#-------------------------------Access-----------------------------------


    def getAccess(self, accessId):
        '''
        Return all access parametters receiving the access ID.
        If the access is a limited access, liAccesses field will
        have a list with all liAcceses
        '''

        try:

            sql = ("LOCK TABLES Zone WRITE, Door WRITE, "
                   "Organization WRITE, Person WRITE, "
                   "Access WRITE, LimitedAccess WRITE"
                  )
            self.execute(sql)

            sql = ("SELECT Access.id, Access.personId, CONCAT(Person.names, ' ', Person.lastName) AS personName, "
                   "Organization.name AS organizationName, Access.doorId, "
                   "Door.name AS doorName, Zone.name AS zoneName, "
                   "Access.allWeek, Access.iSide, Access.oSide, Access.startTime, "
                   "Access.endTime, Access.expireDate, Access.resStateId "
                   "FROM Access JOIN Person ON (Access.personId = Person.id) "
                   "JOIN Organization ON (Person.orgId = Organization.id) "
                   "JOIN Door ON (Access.doorId = Door.id) "
                   "JOIN Zone ON (Door.zoneId = Zone.id) WHERE Access.id = {}"
                   "".format(accessId)
                  )
            self.execute(sql)
            access = self.cursor.fetchone()

            if not access:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound("Access not found.")

            access['expireDate'] = access['expireDate'].strftime('%Y-%m-%d %H:%M')

            if not access['allWeek']:
                access['liAccesses'] = self.getLiAccesses(access['doorId'], access['personId'])
                #When the the access is not allWeek access, startTime, endTime, iSide and 
                #oSide fields are present in each limitedAccess, so we can remove this
                #field from access.
                access.pop('startTime')
                access.pop('endTime')
                access.pop('iSide')
                access.pop('oSide')

            else:
                #If the access is allWeek startTime and endTime should be formatted correctly
                access['startTime'] = str(access['startTime'])
                access['endTime'] = str(access['endTime'])

            self.execute("UNLOCK TABLES")
            return access

        except TypeError:
            #This exception could be raised by "getLiAccesses" method
            #If the tables were locked when this exception was raised, they will be unlocked
            self.execute("UNLOCK TABLES")
            self.logger.warning('Error fetching a liAccesses.')
            raise AccessError('Can not get access with this ID.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not get access with this ID.')




    def getAccesses(self, personId=None, doorId=None):
        '''
        Return a dictionary with all access with the personId
        '''

        try:

            sql = ("LOCK TABLES Zone WRITE, Door WRITE, "
                   "Organization WRITE, Person WRITE, "
                   "Access WRITE, LimitedAccess WRITE"
                  )
            self.execute(sql)


            if (not personId and not doorId) or (personId and doorId):
                #If the tables were locked when this exception was raised, they will be unlocked
                self.execute("UNLOCK TABLES")
                raise AccessError("Error in arguments received in getAccesses method.")
        
            elif personId:
                # check if the person id exists in the database
                sql = ("SELECT * FROM Person WHERE id='{}'".format(personId))
                self.execute(sql)
                person = self.cursor.fetchone()

                if not person:
                    #If the tables were locked when this exception was raised, they will be unlocked
                    self.execute("UNLOCK TABLES")
                    raise PersonNotFound('Person not found')

                # Get all accesses from an specific person
                sql = ("SELECT Access.id, Access.doorId, Door.name AS doorName, "
                       "Zone.name AS zoneName, Access.allWeek, Access.iSide, Access.oSide, "
                       "Access.startTime, Access.endTime, Access.expireDate, Access.resStateId "
                       "FROM Access JOIN Door ON (Access.doorId = Door.id) JOIN Zone ON "
                       "(Door.zoneId = Zone.id) WHERE personId = {}"
                       "".format(personId)
                      )
                self.execute(sql)
                accesses = self.cursor.fetchall()

            else:
                # check if the door id exists in the database
                sql = ("SELECT * FROM Door WHERE id='{}'".format(doorId))
                self.execute(sql)
                door = self.cursor.fetchone()

                if not door:
                    #If the tables were locked when this exception was raised, they will be unlocked
                    self.execute("UNLOCK TABLES")
                    raise DoorNotFound('Door not found')

                # Get all access from an specific door
                sql = ("SELECT Access.id, Access.personId, CONCAT(Person.names, ' ', Person.lastName) AS personName, "
                       "Organization.name AS organizationName, Access.allWeek, Access.iSide, Access.oSide, "
                       "Access.startTime, Access.endTime, Access.expireDate, Access.resStateId "
                       "FROM Access JOIN Person ON (Access.personId = Person.id) JOIN Organization ON "
                       "(Person.orgId = Organization.id) WHERE doorId = {}"
                       "".format(doorId)
                      )
                self.execute(sql)
                accesses = self.cursor.fetchall()


            if not accesses:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')

            for access in accesses:
                access['expireDate'] = access['expireDate'].strftime('%Y-%m-%d %H:%M')
                if not access['allWeek']:
                    if personId:
                        access['liAccesses'] = self.getLiAccesses(access['doorId'], personId)
                    else:
                        access['liAccesses'] = self.getLiAccesses(doorId, access['personId'])
                    #When the the access is not allWeek access, startTime, endTime, iSide and 
                    #oSide fields are present in each limitedAccess, so we can remove this
                    #field from access.
                    access.pop('startTime')
                    access.pop('endTime')
                    access.pop('iSide')
                    access.pop('oSide')

                else:
                    #If the access is allWeek startTime and endTime should be formatted correctly
                    access['startTime'] = str(access['startTime'])
                    access['endTime'] = str(access['endTime'])

            self.execute("UNLOCK TABLES")
            return accesses

        
        except TypeError:
            #This exception could be raised by "getLiAccesses" method
            self.execute("UNLOCK TABLES")
            self.logger.warning('Error fetching a liAccesses.')
            raise AccessError('Can not get accesses in getAcceses for this person or door.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not get accesses for this person or door.')






    def getLiAccesses(self, doorId, personId):

        '''
        Return a dictionary with all access with the personId
        Note: In this method, the exception are not handled since they are
        handled in the methods which call it (getAccess and getAccesses)
        '''
        # check if the person id exist in the database
        sql = ("SELECT * FROM Person WHERE id = '{}'".format(personId))
        self.execute(sql)
        person = self.cursor.fetchall()

        if not person:
            raise PersonNotFound('Person not found')

        # Get all persons from the organization
        sql = ("SELECT id, weekDay, iSide, oSide, startTime, endTime, resStateId "
               "FROM LimitedAccess WHERE doorId = {} AND personId = {}"
               "".format(doorId, personId)
              )
        self.execute(sql)
        liAccesses = self.cursor.fetchall()

        for liAccess in liAccesses:

            liAccess['startTime'] = str(liAccess['startTime'])
            liAccess['endTime'] = str(liAccess['endTime'])

        return liAccesses





    def getUncmtAccesses(self, ctrllerMac, resStateId):
        '''
        This method is an iterator, in each iteration it returns a access not committed 
        with the state "resStateId" from the controller with the MAC address "ctrllerMac".
        The access also have the card number of the person involved in the access as the 
        controller need it to add the person dinamically in its Person table.
        NOTE 1: When this method access to "Access" table, it locks the "Access" and
        "LimitedAccess" table to avoid inconsistency. As this method is an iterator and its
        execution is interrupted, each time it yields a value, it leave the tables unlocked 
        each time it yields a value and re locks them when it continues.
        NOTE 2: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created (not happening today)
        '''

        try:

            localCursor = self.connection.cursor(pymysql.cursors.DictCursor)

            sql = ("LOCK TABLES Controller WRITE, "
                   "Door WRITE, Person WRITE, "
                   "Access WRITE, LimitedAccess WRITE"
                  )
            self.execute(sql)

            sql = ("SELECT Access.*, Person.cardNumber FROM Access JOIN Person "
                   "ON (Access.personId = Person.id) JOIN Door "
                   "ON (Access.doorId = Door.id) JOIN Controller "
                   "ON (Door.controllerId = Controller.id) WHERE Access.allWeek = 1 "
                   "AND Controller.macAddress = '{}' AND Access.resStateId = {}"
                   "".format(ctrllerMac, resStateId)
                  )
            localCursor.execute(sql)
            self.connection.commit()
            access = localCursor.fetchone()

            while access:
                self.execute("UNLOCK TABLES")
                #Removing resStateId as it should not be sent to the controller
                access.pop('resStateId')
                #Time columns in MariaDB are retrieved as timedelta type.
                #If it is converted to string using str() function, something
                #like 0:27:00 is got. When it is sent to controller in this way, 
                #it causes problems when it is compared with times like 09:23.
                #(For example: '0:00:00' > '09:31' returns True).
                #For this reason, it should be formatted and sent in the XX:XX format.
                #To format it in this way, it should be converted to datetime object
                #and formatted using strftime() function.
                #To do it, the timedelta object should be added to the minimum datetime
                #object, then retrieve the time from it and call the strftime() method.

                #We can't ask if access['startTime']: because when startTime is 00:00 (timdelta(0))
                #it evaluates as False
                if access['startTime'] is not None: #Asking if not None because in liaccess this field is None.
                    access['startTime'] = (datetime.datetime.min + access['startTime']).time().strftime('%H:%M')
                if access['endTime'] is not None: #Asking if not None because in liaccess this field is None.
                    access['endTime'] = (datetime.datetime.min + access['endTime']).time().strftime('%H:%M')
                access['expireDate'] = str(access['expireDate'])#.strftime('%Y-%m-%d %H:%M')
                
                yield access

                sql = ("LOCK TABLES Controller WRITE, "
                       "Door WRITE, Person WRITE, "
                       "Access WRITE, LimitedAccess WRITE"
                      )
                self.execute(sql)
                
                access = localCursor.fetchone()

            self.execute("UNLOCK TABLES")


        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Error getting accesses of not committed controllers')





    def addAccess(self, access):
        '''
        Receive a dictionary with access parametters and save it in DB.
        First of all, it tries to delete all limited access with the same
        doorId and personId. This could happen when it is given a full
        access to a person who has limited access.
        '''

        try:
            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            sql = ("DELETE FROM LimitedAccess WHERE doorId = {} and personId = {}"
                   "".format(access['doorId'], access['personId'])
                  )
            self.execute(sql)


            #If there was a row in access table, it should be overwritten, avoiding the engine
            #complaining by the constraints. For this reason the ID is kept. For this reason it
            #is used "ON DUPLICATE KEY UPDATE" statement.
            sql = ("INSERT INTO Access(doorId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate, resStateId) VALUES({}, {}, True, {}, {}, '{}', '{}', '{}', {}) "
                   "ON DUPLICATE KEY UPDATE allWeek = True, iSide = {}, oSide = {}, startTime = '{}', "
                   "endTime = '{}', expireDate = '{}', resStateId = {}"
                   "".format(access['doorId'], access['personId'], access['iSide'], access['oSide'],
                             access['startTime'], access['endTime'], access['expireDate'], TO_ADD,
                             access['iSide'], access['oSide'], access['startTime'], access['endTime'],
                             access['expireDate'], TO_ADD)
                  )
            self.execute(sql)

            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed
            sql = ("SELECT id FROM Access WHERE doorId = {} AND personId = {}"
                   "".format(access['doorId'], access['personId'])
                  )
            self.execute(sql)
            accessId = self.cursor.fetchone()['id']

            self.execute("UNLOCK TABLES")

            return accessId


        #This exception (TypeError) could be raised by the SELECT statement when fetchone()
        #returns None. This should never happen.
        except TypeError:
            self.logger.debug('Error fetching access id.')
            raise AccessError('Can not add this access.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Can not add this access.')
        except pymysql.err.InternalError as internalError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(internalError)
            raise AccessError('Can not add this access.')




    def updAccess(self, access):
        '''
        Receive a dictionary with access parameter to update it.
        doorId, personId and allWeek parameter are not modified.
        If a change on them is necessary, the access should be deleted
        and it should be added again.
        '''


        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            #The user shouldn't be allowed to modify a Limited Access via
            #access endpoint
            sql = "SELECT allWeek from Access WHERE id = {}".format(access['id'])
            self.execute(sql)
            allWeek = self.cursor.fetchone()['allWeek']

            if allWeek:

                sql = ("UPDATE Access SET iSide = {}, oSide = {}, startTime = '{}', "
                       "endTime = '{}', expireDate = '{}', resStateId = {} WHERE id = {}"
                       "".format(access['iSide'], access['oSide'],
                                 access['startTime'], access['endTime'],
                                 access['expireDate'], TO_UPDATE, access['id'])
                      )

                self.execute(sql)
                if self.cursor.rowcount < 1:
                    self.execute("UNLOCK TABLES")
                    raise AccessNotFound('Access not found')

            else:
                self.execute("UNLOCK TABLES")
                self.logger.debug('Can not update Limited Access from access endpoint.')
                raise AccessError('Can not update this access')


            self.execute("UNLOCK TABLES")

        #This exception (TypeError) could be raised by the SELECT statement when fetchone()
        #returns None. This should never happen.
        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Error fetching allWeek from access.')
            raise AccessError('Can not update this access.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Can not update this access')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not update this access: wrong argument')




    def markAccessToDel(self, accessId):
        '''
        Set access row state in the server DB for a pending delete.
        '''

        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)


            #The following parameters are got when all limited accesses of a 
            #person in a door are deleted via access endpoint.            
            sql = ("SELECT allWeek, doorId, personId FROM Access WHERE id = {}"
                   "".format(accessId)
                  )
            self.execute(sql)

            row = self.cursor.fetchone()
            allWeek = row['allWeek']
            doorId = row['doorId']
            personId = row['personId']

            #This can happen when all limited access of a person in a door 
            #are being deleted via access endpoint.
            #On this situation is better start marking the Limited Access entries
            #before marking the Access entries because if an error occurs the 
            #Access entry is not altered and inconsistency is avoided between 
            #Access and Limited Access table.
            if not allWeek:

                sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE doorId = {} "
                       "AND personId = {}".format(TO_DELETE, doorId, personId)
                      )
                self.execute(sql)
                if self.cursor.rowcount < 1:
                    self.execute("UNLOCK TABLES")
                    raise AccessNotFound('Access not found')


            sql = ("UPDATE Access SET resStateId = {} WHERE id = {}"
                   "".format(TO_DELETE, accessId)
                  )
            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')

            self.execute("UNLOCK TABLES")


        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Error getting allWeek, doorId or personId from Access.')
            raise AccessError('Error marking the Access to be deleted.')

        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Error marking the Access to be deleted.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error marking the Access to be deleted.')






    def commitAccess(self, accessId):
        '''
        Mark the access in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state or mark it as DELETED if it was previously in TO_DELETE state
        '''

        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            sql = "SELECT resStateId, allWeek, doorId, personId FROM Access WHERE id = {}".format(accessId)
            self.execute(sql)

            row = self.cursor.fetchone()
            resState = row['resStateId']
            allWeek = row['allWeek']
            #The following fields will be used when deleting an entire Limited Access (*)
            doorId = row['doorId']
            personId = row['personId']


            if resState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Access SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, accessId)
                      )
                self.execute(sql)

            elif resState == TO_DELETE:

                #When the access is a Limited Access, all the entries in LimitedAccess should be deleted too
                if not allWeek:
                    sql = "DELETE FROM LimitedAccess WHERE doorId = {} AND personId = {}".format(doorId, personId)
                    self.execute(sql)

                sql = ("DELETE FROM Access WHERE id = {}"
                       "".format(accessId)
                      )
                self.execute(sql)


            elif resState == COMMITTED:
                self.logger.info("Access already committed.")

            else:
                self.logger.error("Invalid state detected in Access table.")
                raise AccessError('Error committing this access.')

            self.execute("UNLOCK TABLES")


        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Error fetching an access.')
            self.logger.warning('The access to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            self.logger.warning('Error committing an access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing an access.')








    def getDoorId(self, accessId=None, liAccessId=None):
        '''
        This method is called by CRUD module when it wants to delete an access.
        On that situation, it needs to know the "doorId" to send the DELETE 
        message to the corresponding controller.
        It can receive "accessId" or "liAccessId" but not both.
        '''

        if accessId and not liAccessId:
            sql = "SELECT doorId FROM Access WHERE id = {}".format(accessId)

        elif liAccessId and not accessId:
            sql = "SELECT doorId FROM LimitedAccess WHERE id = {}".format(liAccessId)

        else:
            self.logger.debug('Error with arguments calling getDoorId method')
            raise AccessError('Can not get door id for this access.')


        try:
            self.execute(sql)
            doorId = self.cursor.fetchone()['doorId']
            return doorId

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not get door id for this access.')

        except TypeError:
            self.logger.debug('Error fetching doorId.')
            raise AccessError('Can not get door id for this access.')






#-------------------------------Limited Access---------------------------------




    def getUncmtLiAccesses(self, ctrllerMac, resStateId):
        '''
        This method is an iterator, in each iteration it returns a limited access not committed 
        with the state "resStateId" from the controller with the MAC address "ctrllerMac".
        The limited access also have the card number of the person involved in the access as the 
        controller need it to add the person dinamically in its Person table.
        NOTE 1: When this method access to "LimitedAccess" and "Access" table, it locks
        the "Access" and "LimitedAccess" table to avoid inconsistency. As this method is an 
        iterator and its execution is interrupted, each time it yields a value, it leave the tables 
        unlocked each time it yields a value and re lock them when it continues.
        NOTE 2: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created (not happening today)
        '''

        
        try:
            localCursorOne = self.connection.cursor(pymysql.cursors.DictCursor)
            localCursorTwo = self.connection.cursor(pymysql.cursors.DictCursor)

            sql = ("LOCK TABLES Controller WRITE, "
                   "Door WRITE, Person WRITE, "
                   "Access WRITE, LimitedAccess WRITE"
                  )
            self.execute(sql)

            sql = ("SELECT LimitedAccess.*, Person.cardNumber FROM LimitedAccess JOIN Person "
                   "ON (LimitedAccess.personId = Person.id) JOIN Door "
                   "ON (LimitedAccess.doorId = Door.id) JOIN Controller "
                   "ON (Door.controllerId = Controller.id) WHERE "
                   "Controller.macAddress = '{}' AND LimitedAccess.resStateId = {}"
                   "".format(ctrllerMac, resStateId)
                  )
            localCursorOne.execute(sql)
            self.connection.commit()
            liAccess = localCursorOne.fetchone()


            while liAccess:
                #There are some fields from access table that should be sent to the controller
                #when adding or updating a limited access and should be added the "liAccess" dictionary
                sql = ("SELECT id, expireDate FROM Access WHERE doorId = {} AND personId = {}"
                       "".format(liAccess['doorId'], liAccess['personId'])
                      )
                localCursorTwo.execute(sql)
                self.connection.commit()
                row = localCursorTwo.fetchone()

                if not row:
                    #If there are entries in "LimitedAccess" table which doesn't have its corresponding entry in "Access" 
                    #table should be deleted to avoid "crudresender" thread continue trying to resend them.
                    logMsg = 'Removing LimitedAccess entries to solve the inconsistency between Access and LimitedAccess'
                    self.logger.warning(logMsg)
                    sql = ("DELETE FROM LimitedAccess WHERE doorId = {} AND personId = {}"
                           "".format(liAccess['doorId'], liAccess['personId'])
                          )
                    localCursorTwo.execute(sql)
                    self.connection.commit()
                    self.execute("UNLOCK TABLES")
                    raise AccessError('Inconsistency between Access and LimitedAccess')


                self.execute("UNLOCK TABLES")

                accessId = row['id']
                expireDate = row['expireDate']
                expireDate = str(expireDate)

                #Removing resStateId field as it should not be sent to the controller.
                liAccess.pop('resStateId')

                #Time columns in MariaDB are retrieved as timedelta type.
                #If it is converted to string using str() function, something
                #like 0:27:00 is got. When it is sent to controller in this way, 
                #it causes problems when it is compared with times like 09:23.
                #(For example: '0:00:00' > '09:31' returns True).
                #For this reason, it should be formatted and sent in the XX:XX format.
                #To format it in this way, it should be converted to datetime object
                #and formatted using strftime() function.
                #To do it, the timedelta object should be added to the minimum datetime
                #object, then retrieve the time from it and call the strftime() method.
                liAccess['startTime'] = (datetime.datetime.min + liAccess['startTime']).time().strftime('%H:%M')
                liAccess['endTime'] = (datetime.datetime.min + liAccess['endTime']).time().strftime('%H:%M')

                #Adding fields from access to liAccess dictionary.
                liAccess['accessId'] = accessId
                liAccess['expireDate'] = expireDate

                yield liAccess

                sql = ("LOCK TABLES Controller WRITE, "
                       "Door WRITE, Person WRITE, "
                       "Access WRITE, LimitedAccess WRITE"
                      )
                self.execute(sql)

                liAccess = localCursorOne.fetchone()

            self.execute("UNLOCK TABLES")

        except TypeError:
            self.execute("UNLOCK TABLES")
            raise AccessError('Error getting accesses of not committed controllers')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Error getting accesses of not committed controllers')







    def addLiAccess(self, liAccess):
        '''
        Receive a dictionary with limited access parametters and save it in DB.
        In addition to creating an entry in the table "LimitedAccess" it also 
        creates an entry in "Access" table with allWeek = False.
        NOTE: The insertion in LimitedAccess table, is using the "ON DUPLICATE KEY UPDATE"
        to avoid complaining when adding a limited access with the same person,
        door and day.
        On this situation, the limited access will be updated.
        This was specially necesary when adding multiple limited accesses to a person
        or a door that already have the same combination (door, person, weekDay).
        When this didn't work in this way, the limited access never was sent to the 
        controller, because a database exception was raised, the confirmation never came
        and the access entry in Access table remains in state TO_ADD or TO_UPDATE.
        In the past the change of the resState in the access entry also was done before
        inserting in LimitedAccess table. Now the change is done after. In this way,
        if an error ocurs during the insertion on LimitedAccess, the Acces table is not modified. 
        '''

        try:
            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)


            sql = ("INSERT INTO LimitedAccess(doorId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime, resStateId) VALUES({}, {}, {}, {}, {}, '{}', '{}', {}) ON DUPLICATE KEY "
                   "UPDATE iSide = {}, oSide = {}, startTime = '{}', endTime = '{}', resStateId = {}"
                   "".format(liAccess['doorId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'], TO_ADD, liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], TO_ADD)
                  )
            self.execute(sql)

            #As it is necessary to return the liAccess ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed.
            sql = ("SELECT id FROM LimitedAccess WHERE doorId = {} AND personId = {} AND weekDay = {}"
                   "".format(liAccess['doorId'], liAccess['personId'], liAccess['weekDay'])
                  )     
            self.execute(sql)
            liAccessId = self.cursor.fetchone()['id']




            #Each time an entry in "LimitedAccess" table is created with the same
            #combination (doorId, personId), this method will try to add an entry
            #in "Access" table. For this reason it is used "ON DUPLICATE KEY UPDATE"
            #statement. Also it is necessary to use since when a "allWeek" access is
            #changing to a limited access type.
            #The REPLACE statement was not used because each time it is invoked, the ID
            #will increment since it is a DELETE followed by an INSERT.
            sql = ("INSERT INTO Access(doorId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate, resStateId) VALUES({}, {}, FALSE, FALSE, FALSE, NULL, NULL, '{}', {}) "
                   "ON DUPLICATE KEY UPDATE allWeek = FALSE, iSide = FALSE, oSide = FALSE, startTime = NULL, "
                   "endTime = NULL, expireDate = '{}', resStateId = {}"
                   "".format(liAccess['doorId'], liAccess['personId'], liAccess['expireDate'], 
                             TO_ADD, liAccess['expireDate'], TO_ADD)
                  )
            self.execute(sql)

            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed.
            sql = ("SELECT id FROM Access WHERE doorId = {} AND personId = {}"
                   "".format(liAccess['doorId'], liAccess['personId'])
                  )
            self.execute(sql)
            accessId = self.cursor.fetchone()['id']

            self.execute("UNLOCK TABLES")

            return accessId, liAccessId


        #This exception (TypeError) could be raised by the SELECT statement when fetchone()
        #returns None. This should never happen.
        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Error fetching access id or limited access id.')
            raise AccessError('Can not add this limited access.')
        except pymysql.err.IntegrityError as integrityError:
            #If the tables were locked when this exception was raised, they will be unlocked
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Can not add this limited access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not add this limited access.')





    def updLiAccess(self, liAccess):
        '''
        Receive a dictionary with access parameter to update it.
        doorId, personId and allWeek parameter are not modified.
        If a change on them is necessary, the access should be deleted
        and it should be added again.
        '''

        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            #The only thing we should modify in "Access" table is the "expireDate" and 
            #"resStateId" field. To modify the access table, we need "doorId" and "personId"
            sql = ("SELECT doorId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )

            self.execute(sql)
            row = self.cursor.fetchone()
            doorId = row['doorId']
            personId = row['personId']


            sql = ("UPDATE Access SET expireDate = '{}', resStateId = {} "
                   "WHERE doorId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], TO_UPDATE,  doorId, personId)
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}', resStateId = {} WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], TO_UPDATE,
                             liAccess['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')

            self.execute("UNLOCK TABLES")

        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Can not fetching doorId and perssonId.')
            raise AccessError('Can not update this limited access.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Can not update this limited access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not update this limited access.')





    def markLiAccessToDel(self, liAccessId):
        '''
        Set limited access row state in state pending to delete.
        '''

        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE id = {}"
                   "".format(TO_DELETE, liAccessId)
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')


            #The only thing we should modify in "Access" table is the "resStateId" 
            #field. To modify the access table, we need "doorId" and "personId"
            sql = ("SELECT doorId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccessId)
                  )

            self.execute(sql)
            row = self.cursor.fetchone()
            doorId = row['doorId']
            personId = row['personId']


            sql = ("UPDATE Access SET resStateId = {} WHERE doorId = {} AND personId = {}"
                   "".format(TO_UPDATE,  doorId, personId)
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                self.execute("UNLOCK TABLES")
                raise AccessNotFound('Access not found')


            self.execute("UNLOCK TABLES")


        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Can not fetching doorId and perssonId.')
            raise AccessError('Error marking the Limited Access to be deleted.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            raise AccessError('Error marking the Limited Access to be deleted.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Error marking the Limited Access to be deleted.')





    def commitLiAccess(self, liAccessId):
        '''
        Mark the limited access in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state, or delete it if it was previously in TO_DELETE state
        '''

        try:

            sql = "LOCK TABLES Access WRITE, LimitedAccess WRITE"
            self.execute(sql)

            sql = ("SELECT doorId, personId, resStateId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccessId)
                  )

            self.execute(sql)
            row = self.cursor.fetchone()
            doorId = row['doorId']
            personId = row['personId']
            resStateId = row['resStateId']


            if resStateId in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, liAccessId)
                      )
                self.execute(sql)


            elif resStateId == TO_DELETE:
                sql = ("DELETE FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )
                self.execute(sql)


                #Once we delete a limited access, we should verify if there is another
                #limited access with the same "doorId" and the same "personId", if there
                #is not, we should delete the entry in "access" table.
                sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE doorId = {} AND personId = {}"
                       "".format(doorId, personId)
                      )
                self.execute(sql)
                remaining = self.cursor.fetchone()['COUNT(*)']

                if not remaining:
                   sql = ("DELETE FROM Access WHERE doorId = {} AND personId = {}"
                          "".format(doorId, personId)
                         )
                   self.execute(sql)
                   self.execute("UNLOCK TABLES")
                   return

            elif resStateId == COMMITTED:
                self.logger.info("Limited access already committed.")
                self.execute("UNLOCK TABLES")
                return

            else:
                self.logger.error("Invalid state detected in Limited Access table.")
                self.execute("UNLOCK TABLES")
                raise AccessError('Error committing this limited access.')


            #If there is no more limited accesses in a state different than COMMITTED,
            #the access entry should be changed to COMMITTED.
            sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE doorId = {} AND "
                   "personId = {} AND resStateId != {}"
                   "".format(doorId, personId, COMMITTED)
                  )
            self.execute(sql)
            notCommitted = self.cursor.fetchone()['COUNT(*)']

            if not notCommitted:
                sql = ("UPDATE Access SET resStateId = {} WHERE doorId = {} "
                       "AND personId = {}".format(COMMITTED, doorId, personId)
                      )
                self.execute(sql)

            self.execute("UNLOCK TABLES")

        except TypeError:
            self.execute("UNLOCK TABLES")
            self.logger.debug('Error fetching a limited access.')
            self.logger.warning('The limited access to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
            self.execute("UNLOCK TABLES")
            self.logger.debug(integrityError)
            self.logger.warning('Error committing a limited access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing a limited access.')





if __name__ == "__main__": 
    print("Testing Database")
    dataBase = DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, None)  #Passing None to pass something

    sql = ("SELECT doorId FROM Access WHERE personId = 2 AND allWeek = 0")
    dataBase.execute(sql)
    doorIds = dataBase.cursor.fetchall()
    doorIds = [doorId['doorId'] for doorId in doorIds]
    print(doorIds)
    for doorId in doorIds:
        sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE doorId = {} AND "
               "personId = {}".format(doorId, 4)
              )
        dataBase.execute(sql)
        print(dataBase.cursor.fetchone())
        

