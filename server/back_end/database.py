import pymysql
import queue
import logging
import datetime
import crypt

from config import *

TO_ADD = 1
TO_UPDATE = 2
COMMITTED = 3
TO_DELETE = 4
DELETED = 5



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



class VisitorsDoorsError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class VisitorsDoorsNotFound(ZoneError):
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





class DataBase(object):

    def __init__(self, host, user, passwd, dataBase):


        self.logger = logging.getLogger(LOGGER_NAME)

        self.host = host
        self.user = user
        self.passwd = passwd
        self.dataBase = dataBase


        self.connect()


        # With this client_flag, cursor.rowcount will have found rows instead of affected rows
        #self.connection = pymysql.connect(host, user, passwd, dataBase, client_flag = pymysql.constants.CLIENT.FOUND_ROWS)
        #self.connection.autocommit(True)
        # The following line makes all "fetch" calls return a dictionary instead a tuple 
        #self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)



    def connect(self):
        '''
        '''
        # With this client_flag, cursor.rowcount will have found rows instead of affected rows
        self.connection = pymysql.connect(self.host, self.user, self.passwd, self.dataBase, client_flag = pymysql.constants.CLIENT.FOUND_ROWS)
        self.connection.autocommit(True)
        # The following line makes all "fetch" calls return a dictionary instead a tuple
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)




    def execute(self, sql):
        '''
        This method is a wrapper of cursor.execute(). It tries to execute the "sql"
        string, if database is not connected, it reconnect and execute the statement.
        '''

        try:
            self.cursor.execute(sql)

        except pymysql.err.OperationalError:
            self.logger.info("Database is not connected. Reconnecting...")
            self.connect()
            self.cursor.execute(sql)




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
        self.connection.commit()
        return self.cursor.fetchone()['COUNT(*)']




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
                self.connection.commit()

            except pymysql.err.IntegrityError as integrityError:
                self.logger.debug(integrityError)





    def getEvents(self, orgId, personId, zoneId, doorId, startDateTime, 
                  endDateTime, side, startEvt, evtsQtty):
        '''
        Return a dictionary with an interval of "evtsQtty" events starting from "startEvt".
        '''

        #When the following parameters are not NULL, they are used to
        #complete the below SQL sentence.
        if personId: personFilter = ' AND Event.personId = {}'.format(personId)
        else: personFilter = ''

        if orgId: orgFilter = ' AND Person.orgId = {}'.format(orgId)
        else: orgFilter = ''

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
               "Door.description AS doorName, Organization.name AS orgName, "
               "Person.name AS personName, Event.doorLockId, Event.dateTime, "
               "Event.side, Event.allowed, Event.denialCauseId "
               "FROM Event LEFT JOIN Door ON (Event.doorId = Door.id) "
               "LEFT JOIN Zone ON (Door.zoneId = Zone.id) "
               "LEFT JOIN Person ON (Event.personId = Person.id) "
               "LEFT JOIN Organization ON (Person.orgId = Organization.id) "
               "WHERE dateTime >= '{}' AND dateTime <= '{}'{}{}{}{}{} "
               "LIMIT {},{}"
               "".format(startDateTime, endDateTime, personFilter, orgFilter, 
                         doorFilter, zoneFilter, sideFilter, startEvtSql, evtsQtty)
              )

        sqlCount = ("SELECT COUNT(*) FROM Event LEFT JOIN Door ON (Event.doorId = Door.id) "
                    "LEFT JOIN Zone ON (Door.zoneId = Zone.id) "
                    "LEFT JOIN Person ON (Event.personId = Person.id) "
                    "LEFT JOIN Organization ON (Person.orgId = Organization.id) "
                    "WHERE dateTime >= '{}' AND dateTime <= '{}'{}{}{}{}{}"
                    "".format(startDateTime, endDateTime, personFilter, orgFilter,     
                         doorFilter, zoneFilter, sideFilter)
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

        except pymysql.err.ProgrammingError as programmingError:
            #This exception can happen when startEvtSql < 0 or evtQtty is < 0
            #This exception is converted to BadRequest in crud.py module
            #However this would never happen since both parametters are checked 
            #in the first part of the method
            raise EventError

        return events, totalEvtsCount

        



#-------------------------------------User--------------------------------------------

    def getUser(self, username):
        '''
        Return a dictionary with user fields if exists, if not it returns None
        '''
        try:
            sql = "SELECT * from User WHERE username = '{}'".format(username)
            self.execute(sql)
            user = self.cursor.fetchone()
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


        passwdHash = crypt.crypt(user['passwd'], crypt.METHOD_MD5)

        sql = ("INSERT INTO User(description, username, passwdHash, roleId) "
               "VALUES('{}', '{}', '{}', {})"
               "".format(user['description'], user['username'], passwdHash, user['roleId'])
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


        passwdHash = crypt.crypt(user['passwd'], crypt.METHOD_MD5)

        sql = ("UPDATE User SET description = '{}', username = '{}', "
               "passwdHash = '{}', roleId = {} WHERE id = {}"
               "".format(user['description'], user['username'], passwdHash, 
                         user['roleId'], user['id'])
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


#----------------------------------DoorLocks------------------------------------------

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




#----------------------------------Not Reasons------------------------------------------

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
            raise DenialCauseError('Can not get Not Reasons')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DenialCauseError('Can not get Not Reasons')




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

        sql = ("INSERT INTO Organization(name, resStateId) VALUES('{}', {})"
               "".format(organization['name'], COMMITTED)
              )
        
        try:
            self.execute(sql)
            self.connection.commit()
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

        if self.getPersons(orgId, includeDeleted=False):
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
            self.connection.commit()

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

        sql = ("UPDATE Organization SET name = '{}' WHERE id = {}"
               "".format(organization['name'], organization['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationNotFound('Organization not found')
            self.connection.commit()

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

        sql = ("INSERT INTO Zone(name) VALUES('{}')"
               "".format(zone['name'])
              )

        try:
            self.execute(sql)
            self.connection.commit()
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
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not delete this zone')




    def updZone(self, zone):
        '''
        Receive a dictionary with zone parametters and update it in DB
        '''

        sql = ("UPDATE Zone SET name = '{}' WHERE id = {}"
               "".format(zone['name'], zone['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ZoneNotFound('Zone not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not update this zone')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not update this zone: wrong argument')



#----------------------------------Visitors Door-----------------------------------




    def getVisitorsDoorss(self):
        '''
        Return a dictionary with all Zones
        '''
        sql = ('SELECT * FROM VisitorsDoors')
        self.execute(sql)
        visitorsDoorss = self.cursor.fetchall()

        return visitorsDoorss




    def addVisitorsDoors(self, visitorsDoors):
        '''
        Receive a dictionary with Visitors Doorss parametters 
        and save it in DB. It returns the id of the added Visitor Doors.
        '''

        sql = ("INSERT INTO VisitorsDoors(name) VALUES('{}')"
               "".format(visitorsDoors['name'])
              )

        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsDoorsError('Can not add this Visitors Doors')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsDoorsError('Can not add this Visitors Doors: wrong argument')



    def delVisitorsDoors(self, visitorsDoorsId):
        '''
        Receive a dictionary with Visitors Door id and delete the Visitor Door
        '''

        sql = ("DELETE FROM VisitorsDoors WHERE id = {}"
               "".format(visitorsDoorsId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsDoorsNotFound('Visitors Doors not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsDoorsError('Can not delete this Visitors Doors')




    def updVisitorsDoors(self, visitorsDoors):
        '''
        Receive a dictionary with Visitors Doors parametters and update it in DB
        '''

        sql = ("UPDATE VisitorsDoors SET name = '{}' WHERE id = {}"
               "".format(visitorsDoors['name'], visitorsDoors['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsDoorsNotFound('Visitors Doors not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsDoorsError('Can not update this Visitors Doors')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsDoorsError('Can not update this Visitors Doors: wrong argument')




    def addDoorToVisitorsDoors(self, visitorsDoorsId, doorId):
        '''
        '''

        sql = ("INSERT INTO VisitorsDoorsDoor(visitorsDoorsId, doorId) "
               "VALUES ({}, {})".format(visitorsDoorsId, doorId)
              )

        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsDoorsError('Can not add this door to Visitors Door')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsDoorsError('Can not add this door to Visitors Door: wrong argument')




    def delDoorFromVisitorsDoors(self, visitorsDoorsId, doorId):
        '''
        '''

        sql = ("DELETE FROM VisitorsDoorsDoor WHERE "
               "visitorsDoorsId = {} AND doorId = {}"
               "".format(visitorsDoorsId, doorId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsDoorsNotFound('Door not found in Visitors Doors.')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsDoorsError('Can not delete this Door from Visitors Doors')





#----------------------------------Controller----------------------------------------


    def addController(self, controller):
        '''
        Receive a dictionary with controller parametters and save it in DB
        It returns the id of the added controller.
        '''

        sql = ("INSERT INTO Controller(ctrllerModelId, macAddress) "
               "VALUES({}, '{}')"
               "".format(controller['ctrllerModelId'], controller['macAddress'])
              )

        try:
            self.execute(sql)
            self.connection.commit()
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
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not delete this controller')




    def updController(self, controller):
        '''
        Receive a dictionary with controller parametters and update it in DB
        '''

        sql = ("UPDATE Controller SET ctrllerModelId = {}, macAddress = '{}' "
               "WHERE id = {}"
               "".format(controller['ctrllerModelId'], controller['macAddress'], 
                         controller['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise ControllerNotFound('Controller not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not update this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
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
        

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Error reprovisioning the controller.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Error reprovisioning the controller.')




#----------------------------------Door----------------------------------------


    def getDoors(self, zoneId=None, visitorsDoorsId=None):
        '''
        Return a dictionary with all doors in a Zone or in a visitorsDoors
        according to the argument received
        '''

        if not zoneId and not visitorsDoorsId:
            raise DoorNotFound

        elif zoneId:

            # check if the zoneId exists in the database
            sql = ("SELECT * FROM Zone WHERE id='{}'".format(zoneId))
            self.execute(sql)
            zone = self.cursor.fetchall()

            if not zone:
                raise ZoneNotFound('Zone not found')
       
            # Get all persons from the organization
            sql = ("SELECT * FROM Door WHERE zoneId='{}'".format(zoneId))
            self.execute(sql)
            doors = self.cursor.fetchall()
        
            return doors

        elif visitorsDoorsId:
            sql = ("SELECT COUNT(*) FROM VisitorsDoors WHERE id='{}'".format(visitorsDoorsId))
            self.execute(sql)
            
            if self.cursor.fetchone()['COUNT(*)']:
        
                sql = ("SELECT Door.* from Door JOIN VisitorsDoorsDoor "
                       "ON (Door.id = VisitorsDoorsDoor.doorId) "
                       "WHERE VisitorsDoorsDoor.visitorsDoorsId = {}"
                       "".format(visitorsDoorsId)
                      )
                self.execute(sql)
                doors = self.cursor.fetchall()
                return doors

            else:
                raise VisitorsDoorsNotFound('Visitors Doors not found')




    def getUncmtDoors(self, ctrllerMac, resStateId):
        '''
        This method is an iterator, in each iteration it returns a door
        not committed with the state "resStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created.
        '''

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)        
        sql = ("SELECT door.* FROM Door door JOIN Controller controller ON "
               "(door.controllerId = controller.id) WHERE controller.macAddress = '{}' AND "
               "resStateId = {}".format(ctrllerMac, resStateId))

        try:

            cursor.execute(sql)
            door = cursor.fetchone()

            while door:
                #Removing the resStateId as this field should not be sent to the controller
                door.pop('resStateId')
                yield door
                door = cursor.fetchone()

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Error getting doors of not committed controllers')




    def addDoor(self, door):
        '''
        Receive a dictionary with door parametters and save it in DB
        It returns the id of the added door
        '''

        sql = ("INSERT INTO Door(doorNum, description, controllerId, rlseTime, bzzrTime, "
               "alrmTime, zoneId, resStateId) VALUES({}, '{}', {}, {}, {}, {}, {}, {})"
               "".format(door['doorNum'], door['description'], door['controllerId'], 
                         door['rlseTime'], door['bzzrTime'], door['alrmTime'], 
                         door['zoneId'], TO_ADD)
              )


        try:
            self.execute(sql)
            self.connection.commit()
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
                self.connection.commit()

            elif resState == TO_DELETE:
                sql = ("DELETE FROM Door WHERE id = {}"
                       "".format(doorId)
                      )
                self.execute(sql)
                self.connection.commit()

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
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorError('Error marking the Door to be deleted.')
        



    def updDoor(self, door):
        '''
        Receive a dictionary with door parametters and update it in DB
        '''

        sql = ("UPDATE Door SET doorNum = {}, description = '{}', controllerId = {}, rlseTime = {}, "
               "bzzrTime = {}, alrmTime = {}, zoneId = {}, resStateId = {} WHERE id = {}"
               "".format(door['doorNum'], door['description'], door['controllerId'],
                         door['rlseTime'], door['bzzrTime'], door['alrmTime'],
                         door['zoneId'], TO_UPDATE, door['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise DoorNotFound('Door not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise DoorError('Can not update this door')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise DoorError('Can not update this door: wrong argument')





#-------------------------------Person-----------------------------------

    def getPersons(self, orgId, includeDeleted=True):
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
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created.
        '''

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = ("SELECT person.* FROM "
               "Person person JOIN PersonPendingOperation personPendingOperation ON "
               "(person.id = personPendingOperation.personId) WHERE "
               "personPendingOperation.macAddress = '{}' AND personPendingOperation.pendingOp = {}"
               "".format(ctrllerMac, resStateId)
              )

        try:

            cursor.execute(sql)
            person = cursor.fetchone()

            while person:
                #Removing the resStateId as this field should not be sent to the controller
                person.pop('resStateId')
                yield person
                person = cursor.fetchone()

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Error getting persons of not committed controllers')





    def addPerson(self, person):
        '''
        Receive a dictionary with person parametters and save it in DB
        '''

        #The person row is inserted in COMMITTED state since the person is not sent to
        #controller at the moment it is inserted here. It it sent to the controller when
        #an access is created.

        if not person['visitedOrgId']:
            person['visitedOrgId'] = 'NULL'

        sql = ("INSERT INTO Person(name, identNumber, cardNumber, orgId, visitedOrgId, resStateId) "
               "VALUES('{}', '{}', {}, {}, {}, {})"
               "".format(person['name'], person['identNumber'], person['cardNumber'], person['orgId'],
                         person['visitedOrgId'], COMMITTED)
              )

        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError("Can't add this person. Card number or Identification number already exists.")
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
            self.connection.commit()



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
                    sql = ("UPDATE Person SET resStateId = {} WHERE id = {}"
                       "".format(DELETED, personId)
                          )
                    self.execute(sql)
                    self.connection.commit()

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
                    self.connection.commit()
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
                self.connection.commit()

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
            resState = self.cursor.fetchone()['resStateId']

            if resState == TO_DELETE:

                #Deleting all the limited accesses of this person on the doors managed by 
                #this controller
                sql = ("DELETE FROM LimitedAccess WHERE personId = {} AND doorId IN "
                       "(SELECT door.id FROM Door door JOIN Controller controller ON "
                       "(door.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.execute(sql)
                self.connection.commit() 

                #Deleting all the accesses of this person on the doors managed by 
                #this controller
                sql = ("DELETE FROM Access WHERE personId = {} AND doorId IN "
                       "(SELECT door.id FROM Door door JOIN Controller controller ON "
                       "(door.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.execute(sql)
                self.connection.commit()                

                #Deleting the entry in "PersonPendingOperation" table which has this person id,
                #this MAC and the corresponding pending operation.
                sql = ("DELETE FROM PersonPendingOperation WHERE personId = {} AND macAddress = '{}' "
                       "AND pendingOp = {}".format(personId, ctrllerMac, TO_DELETE)
                      )
                self.execute(sql)
                self.connection.commit()

                #If there is not more entries on "PersonPendingOperation" table with this person and 
                #this operation type, it can delete the person definitely from the central database.                
                sql = ("SELECT COUNT(*) FROM PersonPendingOperation WHERE personId = {} "
                       "AND pendingOp = {}".format(personId, TO_DELETE)
                      )
                self.execute(sql)
                pendCtrllersToDel = self.cursor.fetchone()['COUNT(*)']
                if not pendCtrllersToDel:
                    #sql = "DELETE FROM Person WHERE id = {}".format(personId)
                    sql = "UPDATE Person SET resStateId = {} WHERE id = {}".format(DELETED, personId)
                    self.execute(sql)
                    self.connection.commit()

                self.delOrgIfNeed(personId)


            elif resState == TO_UPDATE:
                #Deleting the entry in "PersonPendingOperation" table which has this person id,
                #this MAC and the corresponding pending operation.
                sql = ("DELETE FROM PersonPendingOperation WHERE personId = {} AND macAddress = '{}' "
                       "AND pendingOp = {}".format(personId, ctrllerMac, TO_UPDATE)
                      )
                self.execute(sql)
                self.connection.commit()

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
                    self.connection.commit()

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
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not delete this person')





    def updPerson(self, person):
        '''
        Receive a dictionary with id organization
        '''
        if not person['visitedOrgId']:
            person['visitedOrgId'] = 'NULL'

        sql = ("UPDATE Person SET name = '{}', identNumber = '{}', cardNumber = {}, orgId = {}, "
               "visitedOrgId = {} WHERE id = {}"
               "".format(person['name'], person['identNumber'], person['cardNumber'], 
                         person['orgId'], person['visitedOrgId'], person['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')
            self.connection.commit()

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

        sql = "SELECT * FROM Person WHERE id = {}".format(personId)
        self.execute(sql)
        person = self.cursor.fetchone()

        if not person:
            raise PersonNotFound("Person not found.")
        return person




#-------------------------------Access-----------------------------------

    def getAccesses(self, personId=None, doorId=None):
        '''
        Return a dictionary with all access with the personId
        '''
        if (not personId and not doorId) or (personId and doorId):
            raise AccessError("Error of arguments received in getAccess method.")
        
        elif personId:
            # check if the person id exist in the database
            sql = ("SELECT * FROM Person WHERE id='{}'".format(personId))
            self.execute(sql)
            person = self.cursor.fetchall()

            if not person:
                raise PersonNotFound('Person not found')

            # Get all accesses from an specific person
            sql = ("SELECT Access.id, Access.doorId, Door.description AS doorDescription, "
                   "Zone.name AS zoneName, Access.allWeek, Access.iSide, Access.oSide, "
                   "Access.startTime, Access.endTime, Access.expireDate, Access.resStateId "
                   "FROM Access JOIN Door ON (Access.doorId = Door.id) JOIN Zone ON "
                   "(Door.zoneId = Zone.id) WHERE personId = {}"
                   "".format(personId)
                  )
            self.execute(sql)
            accesses = self.cursor.fetchall()

        else:
            # check if the person id exist in the database
            sql = ("SELECT * FROM Door WHERE id='{}'".format(doorId))
            self.execute(sql)
            door = self.cursor.fetchall()

            if not door:
                raise DoorNotFound('Door not found')

            # Get all persons from the organization


            sql = ("SELECT Access.id, Access.personId, Person.name AS personName, "
                   "Organization.name AS organizationName, Access.allWeek, Access.iSide, Access.oSide, "
                   "Access.startTime, Access.endTime, Access.expireDate, Access.resStateId "
                   "FROM Access JOIN Person ON (Access.personId = Person.id) JOIN Organization ON "
                   "(Person.orgId = Organization.id) WHERE doorId = {}"
                   "".format(doorId)
                  )
            self.execute(sql)
            accesses = self.cursor.fetchall()


        for access in accesses:

            access['startTime'] = str(access['startTime'])
            access['endTime'] = str(access['endTime'])
            access['expireDate'] = access['expireDate'].strftime('%Y-%m-%d %H:%M')
            #The description is usefull to show the access in the front end for an
            #specific person.

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

        return accesses




    def getLiAccesses(self, doorId, personId):

        '''
        Return a dictionary with all access with the personId
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
        This method is an iterator, in each iteration it returns a access
        not committed with the state "resStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created. In this case, between each iteration,
        "getPerson" method is executed which would use the same cursor.
        '''


        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = ("SELECT access.* FROM Access access JOIN Door door ON "
               "(access.doorId = door.id) JOIN Controller controller ON "
               "(door.controllerId = controller.id) WHERE "
               "controller.macAddress = '{}' AND access.resStateId = {}"
               "".format(ctrllerMac, resStateId)
              )

        try:
            cursor.execute(sql)
            access = cursor.fetchone()

            while access:
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
                access['startTime'] = (datetime.datetime.min + access['startTime']).time().strftime('%H:%M')
                access['endTime'] = (datetime.datetime.min + access['endTime']).time().strftime('%H:%M')
                access['expireDate'] = str(access['expireDate'])#.strftime('%Y-%m-%d %H:%M')
                
                yield access
                access = cursor.fetchone()

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

            sql = ("DELETE FROM LimitedAccess WHERE doorId = {} and personId = {}"
                   "".format(access['doorId'], access['personId'])
                  )
            self.execute(sql)
            self.connection.commit()


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
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed
            sql = ("SELECT id FROM Access WHERE doorId = {} AND personId = {}"
                   "".format(access['doorId'], access['personId'])
                  )
            self.execute(sql)
            return self.cursor.fetchone()['id']


        #This exception (TypeError) could be raised by the SELECT statement when fetchone()
        #returns None. This should never happen.
        except TypeError:
            self.logger.debug('Error fetching access id.')
            raise AccessError('Can not add this access.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not add this access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not add this access.')




    def updAccess(self, access):
        '''
        Receive a dictionary with access parameter to update it.
        doorId, personId and allWeek parameter are not modified.
        If a change on them is necessary, the access should be deleted
        and it should be added again.
        '''

        sql = ("UPDATE Access SET iSide = {}, oSide = {}, startTime = '{}', "
               "endTime = '{}', expireDate = '{}', resStateId = {} WHERE id = {}"
               "".format(access['iSide'], access['oSide'],
                         access['startTime'], access['endTime'],
                         access['expireDate'], TO_UPDATE, access['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not update this access')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not update this access: wrong argument')




    def markAccessToDel(self, accessId):
        '''
        Set access row state in the server DB for a pending delete.
        '''

        sql = ("UPDATE Access SET resStateId = {} WHERE id = {}"
               "".format(TO_DELETE, accessId)
              )
        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Error marking the Access to be deleted.')





    def commitAccess(self, accessId):
        '''
        Mark the access in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state or mark it as DELETED if it was previously in TO_DELETE state
        '''

        sql = "SELECT resStateId FROM Access WHERE id = {}".format(accessId)

        try:
            self.execute(sql)
            resState = self.cursor.fetchone()['resStateId']

            if resState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Access SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, accessId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif resState == TO_DELETE:
                sql = ("DELETE FROM Access WHERE id = {}"
                       "".format(accessId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif resState == COMMITTED:
                self.logger.info("Access already committed.")

            else:
                self.logger.error("Invalid state detected in Access table.")
                raise AccessError('Error committing this access.')


        except TypeError:
            self.logger.debug('Error fetching an access.')
            self.logger.warning('The access to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
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
        This method is an iterator, in each iteration it returns a liAccess
        not committed with the state "resStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created. In this case, between each iteration,
        "getPerson" method is executed which would use the same cursor.
        '''

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        secCursor = self.connection.cursor(pymysql.cursors.DictCursor)


        sql = ("SELECT liAccess.* FROM LimitedAccess liAccess JOIN Door door ON "
               "(liAccess.doorId = door.id) JOIN Controller controller ON "
               "(door.controllerId = controller.id) WHERE "
               "controller.macAddress = '{}' AND liAccess.resStateId = {}"
               "".format(ctrllerMac, resStateId)
              )

        try:

            cursor.execute(sql)
            liAccess = cursor.fetchone()

            while liAccess:
                #There are some fields from access table that should be sent to the controller
                #when adding or updating a limited access and should be added the "liAccess" dictionary
                secSql = ("SELECT id, expireDate FROM Access WHERE doorId = {} AND personId = {}"
                          "".format(liAccess['doorId'], liAccess['personId'])
                         )
                secCursor.execute(secSql)
                row = secCursor.fetchone()
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
                liAccess = cursor.fetchone()

        except TypeError:
            self.logger.debug('Error fetching expireDate.')
            raise AccessError('Error getting accesses of not committed controllers')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Error getting accesses of not committed controllers')









    def addLiAccess(self, liAccess):
        '''
        Receive a dictionary with limited access parametters and save it in DB.
        In addition to creating an entry in the table "LimitedAccess" it also 
        creates an entry in "Access" table with allWeek = False.
        '''

        try:
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
                             COMMITTED, liAccess['expireDate'], COMMITTED)
                  )
            self.execute(sql)
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed.
            sql = ("SELECT id FROM Access WHERE doorId = {} AND personId = {}"
                   "".format(liAccess['doorId'], liAccess['personId'])
                  )
            self.execute(sql)
            accessId = self.cursor.fetchone()['id']
            

            sql = ("INSERT INTO LimitedAccess(doorId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime, resStateId) VALUES({}, {}, {}, {}, {}, '{}', '{}', {})"
                   "".format(liAccess['doorId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'], TO_ADD)
                  )
            self.execute(sql)
            self.connection.commit()
            liAccessId = self.cursor.lastrowid
            return accessId, liAccessId


        #This exception (TypeError) could be raised by the SELECT statement when fetchone()
        #returns None. This should never happen.
        except TypeError:
            self.logger.debug('Error fetching access id.')
            raise AccessError('Can not add this limited access.')
        except pymysql.err.IntegrityError as integrityError:
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
            #The only thing we should modify in "Access" table is the "expireDate" field.
            #To modify the access table, we need "doorId" and "personId"
            sql = ("SELECT doorId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )

            self.execute(sql)
            row = self.cursor.fetchone()
            doorId = row['doorId']
            personId = row['personId']


            sql = ("UPDATE Access SET expireDate = '{}' WHERE doorId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], doorId, personId)
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}', resStateId = {} WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], TO_UPDATE,
                             liAccess['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()


        except TypeError:
            self.logger.debug('Can not fetching doorId and perssonId.')
            raise AccessError('Can not update this limited access.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not update this limited access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise AccessError('Can not update this limited access.')





    def markLiAccessToDel(self, liAccessId):
        '''
        Set limited access row state in state pending to delete.
        '''

        sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE id = {}"
               "".format(TO_DELETE, liAccessId)
              )
        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Error marking the Limited Access to be deleted.')







    def commitLiAccess(self, liAccessId):
        '''
        Mark the limited access in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state or mark it as DELETED if it was previously in TO_DELETE state
        '''

        try:
            sql = "SELECT resStateId FROM LimitedAccess WHERE id = {}".format(liAccessId)
            self.execute(sql)
            resState = self.cursor.fetchone()['resStateId']

            if resState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE LimitedAccess SET resStateId = {} WHERE id = {}"
                       "".format(COMMITTED, liAccessId)
                      )

                self.execute(sql)
                self.connection.commit()


            elif resState == TO_DELETE:

                sql = ("SELECT doorId, personId FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )

                self.execute(sql)
                row = self.cursor.fetchone() #KeyError exception could be raised here
                doorId = row['doorId']       #Me parece que es TypeError y no KeyError
                personId = row['personId']
        
                sql = ("DELETE FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )
                self.execute(sql)
                self.connection.commit()


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
                   self.connection.commit()

            elif resState == COMMITTED:
                self.logger.info("Limited access already committed.")

            else:
                self.logger.error("Invalid state detected in Limited Access table.")
                raise AccessError('Error committing this limited access.')



        except TypeError:
            self.logger.debug('Error fetching a limited access.')
            self.logger.warning('The limited access to commit is not in data base.')
#        except KeyError:
#            self.logger.debug('Error fetching a limited access.')
#            self.logger.warning('Error committing a limited access.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.logger.warning('Error committing a limited access.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing a limited access.')





if __name__ == "__main__": 
    print("Testing Database")
    dataBase = DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

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
        

