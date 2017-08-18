import pymysql
import queue
import logging
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



class VisitorsPssgsError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class VisitorsPssgsNotFound(ZoneError):
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


class PassageError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage


class PassageNotFound(PassageError):
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
            #At this moment this is only need in 'personId' and 'notReason'
            #fields
            for eventField in event:
                if event[eventField] == None:
                    event[eventField] = 'NULL'


            sql = ("INSERT INTO "
                   "Event(eventTypeId, pssgId, dateTime, latchId, personId, side, allowed, notReasonId) "
                   "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
                   "".format(event['eventTypeId'], event['pssgId'], event['dateTime'],
                             event['latchId'], event['personId'], event['side'],
                             event['allowed'], event['notReasonId']
                            ) 

                  )
            try:
                self.execute(sql)
                self.connection.commit()

            except pymysql.err.IntegrityError as integrityError:
                self.logger.debug(integrityError)





    def getEvents(self, orgId, personId, zoneId, pssgId, startDateTime, 
                  endDateTime, side, fromEvt, evtsQtty):
        '''
        Return a dictionary with an interval of "evtsQtty" events starting from "fromEvt".
        If "personId" is None, the method will return only the events of the "Unknown" person
        (for example events of passages opened by pressing REX button)
        '''

        if not orgId: orgId = '%'
        if not zoneId: zoneId = '%'
        if not pssgId: pssgId = '%'
        if not side: side = '%'

        if not personId:

            sql = ("SELECT Event.* FROM Event JOIN Passage ON (Event.pssgId = Passage.id) "
                   "WHERE Passage.zoneId LIKE '{}' AND pssgId LIKE '{}' AND personId IS NULL "
                   "AND dateTime >= '{}' AND dateTime <= '{}' AND side LIKE '{}' LIMIT {},{} "
                   "".format(zoneId, pssgId, startDateTime, endDateTime, side, fromEvt, evtsQtty)
                  )

        else:
            sql = ("SELECT Event.* FROM Event JOIN Person ON (Event.personId = Person.id) JOIN "
                   "Passage ON (Event.pssgId = Passage.id) WHERE Person.orgId LIKE '{}' AND "
                   "personId LIKE '{}' AND Passage.zoneId LIKE '{}' AND pssgId LIKE '{}' AND "
                   "dateTime >= '{}' AND dateTime <= '{}' AND side LIKE '{}' LIMIT {},{}"
                   "".format(orgId, personId, zoneId, pssgId, startDateTime, endDateTime, 
                             side, fromEvt, evtsQtty)
                  )

        print(sql)


        self.execute(sql)
        events = self.cursor.fetchall()

        return events

        



#-------------------------------------User--------------------------------------------

    def getUser(self, username):
        '''
        Return a dictionary with user fields if exists, if not it returns None
        '''
        sql = "SELECT * from User WHERE username = '{}'".format(username)
        self.execute(sql)
        user = self.cursor.fetchone()
        return user



    def getUsers(self):
        '''
        Return a dictionary with all Users
        '''
        sql = ('SELECT * FROM User')
        self.execute(sql)
        users = self.cursor.fetchall()

        return users




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

    def getRowStates(self):
        '''
        Return a a dictionary with all rowStates
        '''
        sql = ('SELECT * FROM RowState')
        self.execute(sql)
        rowStates = self.cursor.fetchall()

        return rowStates





#----------------------------------Organization----------------------------------------


    def getOrganizations(self):
        '''
        Return a a dictionary with all organizations
        '''
        sql = ('SELECT * FROM Organization')
        self.execute(sql)
        organizations = self.cursor.fetchall()

        return organizations


                                             

    def addOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and save it in DB
        It returns the id of the added organization.
        '''

        sql = ("INSERT INTO Organization(name, rowStateId) VALUES('{}', {})"
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
            sql = ("UPDATE Organization SET rowStateId = {} WHERE id = {}"
                   "".format(TO_DELETE, orgId)
                  )
        else:
            sql = ("UPDATE Organization SET rowStateId = {} WHERE id = {}"
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
            sql = ("SELECT Organization.id, Organization.rowStateId FROM Organization "
                   "JOIN Person ON (Organization.id = Person.orgId) WHERE Person.id = {}"
                   "".format(personId)
                  )
            self.execute(sql)
            row = self.cursor.fetchone()
            orgId, rowStateId = row['id'], row['rowStateId']

            if rowStateId == TO_DELETE:

                #Gets the number of people who belong to this organization and who have
                #not yet been eliminated
                sql = ("SELECT COUNT(*) FROM Person WHERE orgId = {} AND rowStateId != {}"
                       "".format(orgId, DELETED)
                      )
                self.execute(sql)
                personCount = self.cursor.fetchone()['COUNT(*)']

                #If personCount is 0, the organization can be deleted.
                if personCount == 0:
                    sql = ("UPDATE Organization SET rowStateId = {} WHERE id = {}"
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
        Return a dictionary with all Zones
        '''
        sql = ('SELECT * FROM Zone')
        self.execute(sql)
        zones = self.cursor.fetchall()

        return zones



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



#----------------------------------Visitors Passage-----------------------------------




    def getVisitorsPssgss(self):
        '''
        Return a dictionary with all Zones
        '''
        sql = ('SELECT * FROM VisitorsPassages')
        self.execute(sql)
        visitorsPssgss = self.cursor.fetchall()

        return visitorsPssgss




    def addVisitorsPssgs(self, visitorsPssgs):
        '''
        Receive a dictionary with Visitors Passagess parametters 
        and save it in DB. It returns the id of the added Visitor Passages.
        '''

        sql = ("INSERT INTO VisitorsPassages(name) VALUES('{}')"
               "".format(visitorsPssgs['name'])
              )

        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsPssgsError('Can not add this Visitors Passages')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsPssgsError('Can not add this Visitors Passages: wrong argument')



    def delVisitorsPssgs(self, visitorsPssgsId):
        '''
        Receive a dictionary with Visitors Passage id and delete the Visitor Passage
        '''

        sql = ("DELETE FROM VisitorsPassages WHERE id = {}"
               "".format(visitorsPssgsId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsPssgsNotFound('Visitors Passages not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsPssgsError('Can not delete this Visitors Passages')




    def updVisitorsPssgs(self, visitorsPssgs):
        '''
        Receive a dictionary with Visitors Passages parametters and update it in DB
        '''

        sql = ("UPDATE VisitorsPassages SET name = '{}' WHERE id = {}"
               "".format(visitorsPssgs['name'], visitorsPssgs['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsPssgsNotFound('Visitors Passages not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsPssgsError('Can not update this Visitors Passages')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsPssgsError('Can not update this Visitors Passages: wrong argument')




    def addPssgToVisitorsPssgs(self, visitorsPssgsId, pssgId):
        '''
        '''

        sql = ("INSERT INTO VisitorsPassagesPassage(visitorsPssgsId, pssgId) "
               "VALUES ({}, {})".format(visitorsPssgsId, pssgId)
              )

        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsPssgsError('Can not add this passage to Visitors Passage')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise VisitorsPssgsError('Can not add this passage to Visitors Passage: wrong argument')




    def delPssgFromVisitorsPssgs(self, visitorsPssgsId, pssgId):
        '''
        '''

        sql = ("DELETE FROM VisitorsPassagesPassage WHERE "
               "visitorsPssgsId = {} AND pssgId = {}"
               "".format(visitorsPssgsId, pssgId)
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise VisitorsPssgsNotFound('Passage not found in Visitors Passages.')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise VisitorsPssgsError('Can not delete this Passage from Visitors Passages')





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






    def getControllerMac(self, controllerId=None, passageId=None):
        '''
        Return the controller MAC address receiving the controller ID or passage ID
        '''

        if (controllerId and passageId) or (not controllerId and not passageId):
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
                   "Passage passage ON (controller.id = passage.controllerId) WHERE "
                   "passage.id = {}".format(passageId)
                  )

            try:
                self.execute(sql)
                return self.cursor.fetchone()['macAddress']

            except TypeError:
                self.logger.debug('This passage id is not present in any controller.')
                raise PassageNotFound('Passage not found')




    def getCtrllerMacsToDelPrsn(self, personId):
        '''
        Return a list of controller MAC addresses receiving the person ID
        to delete.
        '''
        
        sql = ("SELECT macAddress FROM Controller controller JOIN Passage passage "
               "ON (controller.id = passage.controllerId) JOIN Access access "
               "ON (passage.id = access.pssgId) JOIN Person person "
               "ON (access.personId = person.id) WHERE person.rowStateId = {} AND "
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

        sql = ("SELECT controller.macAddress FROM Controller controller JOIN Passage passage "
               "ON (controller.id = passage.controllerId) WHERE passage.rowStateId IN ({0}, {1}, {2}) "
               "UNION "
               "SELECT controller.macAddress FROM Controller controller JOIN Passage passage ON "
               "(controller.id = passage.controllerId) JOIN LimitedAccess limitedAccess ON "
               "(passage.id = limitedAccess.pssgId) WHERE limitedAccess.rowStateId IN ({0}, {1}, {2}) "
               "UNION "
               "SELECT controller.macAddress FROM Controller controller JOIN Passage passage ON "
               "(controller.id = passage.controllerId) JOIN Access access ON "
               "(passage.id = access.pssgId) WHERE access.rowStateId IN ({0}, {1}, {2}) "
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
        It sets all passages, access and limited access in state TO_ADD.
        Receive a dictionary with controller parametters and update it in central DB
        because MAC address and board model can change.
        '''
        try:

            sql = ("UPDATE Passage SET rowStateId = {} WHERE controllerId = {}"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)

            sql = ("UPDATE Access SET rowStateId = {} WHERE pssgId IN "
                   "(SELECT id FROM Passage WHERE controllerId = {}) AND allWeek = 1"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)

            sql = ("UPDATE LimitedAccess SET rowStateId = {} WHERE pssgId IN "
                   "(SELECT id FROM Passage WHERE controllerId = {})"
                   "".format(TO_ADD, controllerId)
                  )
            self.execute(sql)
        

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Error reprovisioning the controller.')

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Error reprovisioning the controller.')




#----------------------------------Passage----------------------------------------


    def getPassages(self, zoneId=None, visitorsPssgsId=None):
        '''
        Return a dictionary with all passages in a Zone or in a visitorsPassages
        according to the argument received
        '''

        if not zoneId and not visitorsPssgsId:
            raise PassageNotFound

        elif zoneId:

            # check if the zoneId exists in the database
            sql = ("SELECT * FROM Zone WHERE id='{}'".format(zoneId))
            self.execute(sql)
            zone = self.cursor.fetchall()

            if not zone:
                raise ZoneNotFound('Zone not found')
       
            # Get all persons from the organization
            sql = ("SELECT * FROM Passage WHERE zoneId='{}'".format(zoneId))
            self.execute(sql)
            passages = self.cursor.fetchall()
        
            return passages

        elif visitorsPssgsId:
            sql = ("SELECT COUNT(*) FROM VisitorsPassages WHERE id='{}'".format(visitorsPssgsId))
            self.execute(sql)
            
            if self.cursor.fetchone()['COUNT(*)']:
        
                sql = ("SELECT Passage.* from Passage JOIN VisitorsPassagesPassage "
                       "ON (Passage.id = VisitorsPassagesPassage.pssgId) "
                       "WHERE VisitorsPassagesPassage.visitorsPssgsId = {}"
                       "".format(visitorsPssgsId)
                      )
                self.execute(sql)
                passages = self.cursor.fetchall()
                return passages

            else:
                raise VisitorsPssgsNotFound('Visitors Passages not found')




    def getUncmtPassages(self, ctrllerMac, rowStateId):
        '''
        This method is an iterator, in each iteration it returns a passage
        not committed with the state "rowStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created.
        '''

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)        
        sql = ("SELECT passage.* FROM Passage passage JOIN Controller controller ON "
               "(passage.controllerId = controller.id) WHERE controller.macAddress = '{}' AND "
               "rowStateId = {}".format(ctrllerMac, rowStateId))

        try:

            cursor.execute(sql)
            passage = cursor.fetchone()

            while passage:
                #Removing the rowStateId as this field should not be sent to the controller
                passage.pop('rowStateId')
                yield passage
                passage = cursor.fetchone()

        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PassageError('Error getting passages of not committed controllers')




    def addPassage(self, passage):
        '''
        Receive a dictionary with passage parametters and save it in DB
        It returns the id of the added passage
        '''

        sql = ("INSERT INTO Passage(pssgNum, description, controllerId, rlseTime, bzzrTime, "
               "alrmTime, zoneId, rowStateId) VALUES({}, '{}', {}, {}, {}, {}, {}, {})"
               "".format(passage['pssgNum'], passage['description'], passage['controllerId'], 
                         passage['rlseTime'], passage['bzzrTime'], passage['alrmTime'], 
                         passage['zoneId'], TO_ADD)
              )


        try:
            self.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PassageError('Can not add this passage')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PassageError('Can not add this passage: wrong argument')



    def commitPassage(self, passageId):
        '''
        Mark the passage in database as COMMITTED if it was previously in TO_ADD or
        TO_UPDATE state or delete it if it was previously in TO_DELETE state
        '''
 
        sql = "SELECT rowStateId FROM Passage WHERE id = {}".format(passageId)

        try:
            self.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Passage SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, passageId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif rowState == TO_DELETE:
                sql = ("DELETE FROM Passage WHERE id = {}"
                       "".format(passageId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif rowState == COMMITTED:
                self.logger.info("Passage already committed.")

            else:
                self.logger.error("Invalid state detected in passage table.")
                raise PassageError('Error committing a passage.')


        except TypeError:
            self.logger.debug('Error fetching a passage.')
            self.logger.warning('The passage to commit is not in data base.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.logger.warning('Error committing a passage.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            self.logger.warning('Error committing a passage.')



    def markPassageToDel(self, passageId):
        '''
        Set passage row state in state: TO_DELETE (pending to delete).
        '''

        sql = ("UPDATE Passage SET rowStateId = {} WHERE id = {}"
               "".format(TO_DELETE, passageId)
              )
        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PassageNotFound('Passage not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PassageError('Error marking the Passage to be deleted.')
        



    def updPassage(self, passage):
        '''
        Receive a dictionary with passage parametters and update it in DB
        '''

        sql = ("UPDATE Passage SET pssgNum = {}, description = '{}', controllerId = {}, rlseTime = {}, "
               "bzzrTime = {}, alrmTime = {}, zoneId = {}, rowStateId = {} WHERE id = {}"
               "".format(passage['pssgNum'], passage['description'], passage['controllerId'],
                         passage['rlseTime'], passage['bzzrTime'], passage['alrmTime'],
                         passage['zoneId'], TO_UPDATE, passage['id'])
              )

        try:
            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise PassageNotFound('Passage not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PassageError('Can not update this passage')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PassageError('Can not update this passage: wrong argument')





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
                sql = ("SELECT * FROM Person WHERE orgId = {} AND rowStateId != {}"
                       "".format(orgId, DELETED)
                      )
            self.execute(sql)
            persons = self.cursor.fetchall()
        
            return persons


        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not get persons from this organization')






    def getUncmtPersons(self, ctrllerMac, rowStateId):
        '''
        This method is an iterator, in each iteration it returns a person
        not committed with the state "rowStateId" from the controller
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
               "".format(ctrllerMac, rowStateId)
              )

        try:

            cursor.execute(sql)
            person = cursor.fetchone()

            while person:
                #Removing the rowStateId as this field should not be sent to the controller
                person.pop('rowStateId')
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

        sql = ("INSERT INTO Person(name, identNumber, cardNumber, orgId, visitedOrgId, rowStateId) "
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

            sql = ("UPDATE Person SET rowStateId = {} WHERE id = {}"
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
                sql = ("DELETE FROM Access WHERE rowStateId = {} AND personId = {}"
                       "".format(TO_ADD, personId)
                      )
                self.execute(sql)

                sql = ("DELETE FROM LimitedAccess WHERE rowStateId = {} AND personId = {}"
                       "".format(TO_ADD, personId)
                      )
                self.execute(sql)

                sql = ("SELECT pssgId FROM Access WHERE personId = {} AND allWeek = 0"
                       "".format(personId)
                      )

                self.execute(sql)
                pssgIds = self.cursor.fetchall()
                pssgIds = [pssgId['pssgId'] for pssgId in pssgIds]
                for pssgId in pssgIds:
                    sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE pssgId = {} AND "
                           "personId = {}".format(pssgId, personId)
                          )
                    self.execute(sql)
                    count = self.cursor.fetchone()['COUNT(*)']
                    if count == 0:
                        sql = ("DELETE FROM Access WHERE pssgId = {} "
                               "AND personId = {} AND allWeek = 0"
                               "".format(pssgId, personId)
                              )
                        self.execute(sql)



            #To avoid having duplicate MACs in the result list, it is used DISTINCT clause
            #since we can have a Person having access in more than one passage
            #and those passage could be on the same controller (with the same MAC)
            sql = ("SELECT DISTINCT macAddress FROM Controller controller JOIN Passage passage "
                   "ON (controller.id = passage.controllerId) JOIN Access access "
                   "ON (passage.id = access.pssgId) JOIN Person person "
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
                    sql = ("UPDATE Person SET rowStateId = {} WHERE id = {}"
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
                    sql = ("UPDATE Person SET rowStateId = {} WHERE id = {}"
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
        this person on the passages managed by this controller. 
        Then it deletes the entry in "PersonPendingOperation" table which has this person id,
        this MAC and the corresponding pending operation. 
        If there is not more entries on "PersonPendingOperation" table with this person and 
        this operation type, it can delete the person definitely from the central database.
        '''

        try:
            #Determines the pendig operation of that person on that controller
            sql = "SELECT rowStateId FROM Person WHERE id = {}".format(personId)

            self.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState == TO_DELETE:

                #Deleting all the limited accesses of this person on the passages managed by 
                #this controller
                sql = ("DELETE FROM LimitedAccess WHERE personId = {} AND pssgId IN "
                       "(SELECT passage.id FROM Passage passage JOIN Controller controller ON "
                       "(passage.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.execute(sql)
                self.connection.commit() 

                #Deleting all the accesses of this person on the passages managed by 
                #this controller
                sql = ("DELETE FROM Access WHERE personId = {} AND pssgId IN "
                       "(SELECT passage.id FROM Passage passage JOIN Controller controller ON "
                       "(passage.controllerId = controller.id) WHERE controller.macAddress = '{}')"
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
                    sql = "UPDATE Person SET rowStateId = {} WHERE id = {}".format(DELETED, personId)
                    self.execute(sql)
                    self.connection.commit()

                self.delOrgIfNeed(personId)


            elif rowState == TO_UPDATE:
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
                    sql = "UPDATE Person SET rowStateId = {} WHERE id = {}".format(COMMITTED, personId)
                    self.execute(sql)
                    self.connection.commit()

            elif rowState == COMMITTED:
                self.logger.info('Person already committed.')

            elif rowState == DELETED:
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

        sql = "SELECT id, name, cardNumber FROM Person WHERE id = {}".format(personId)
        self.execute(sql)
        person = self.cursor.fetchone()

        if not person:
            raise PersonNotFound("Person not found.")
        return person




#-------------------------------Access-----------------------------------

    def getAccesses(self, personId=None, pssgId=None):
        '''
        Return a dictionary with all access with the personId
        '''
        if (not personId and not pssgId) or (personId and pssgId):
            raise AccessError("Error of arguments received in getAccess method.")
        
        elif personId:
            # check if the person id exist in the database
            sql = ("SELECT * FROM Person WHERE id='{}'".format(personId))
            self.execute(sql)
            person = self.cursor.fetchall()

            if not person:
                raise PersonNotFound('Person not found')

            # Get all accesses from an specific person
            sql = ("SELECT Access.id, Access.pssgId, Passage.description AS pssgDescription, "
                   "Zone.name AS zoneName, Access.allWeek, Access.iSide, Access.oSide, "
                   "Access.startTime, Access.endTime, Access.expireDate, Access.rowStateId "
                   "FROM Access JOIN Passage ON (Access.pssgId = Passage.id) JOIN Zone ON "
                   "(Passage.zoneId = Zone.id) WHERE personId = {}"
                   "".format(personId)
                  )
            self.execute(sql)
            accesses = self.cursor.fetchall()

        else:
            # check if the person id exist in the database
            sql = ("SELECT * FROM Passage WHERE id='{}'".format(pssgId))
            self.execute(sql)
            passage = self.cursor.fetchall()

            if not passage:
                raise PassageNotFound('Passage not found')

            # Get all persons from the organization


            sql = ("SELECT Access.id, Access.personId, Person.name AS personName, "
                   "Organization.name AS organizationName, Access.allWeek, Access.iSide, Access.oSide, "
                   "Access.startTime, Access.endTime, Access.expireDate, Access.rowStateId "
                   "FROM Access JOIN Person ON (Access.personId = Person.id) JOIN Organization ON "
                   "(Person.orgId = Organization.id) WHERE pssgId = {}"
                   "".format(pssgId)
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
                    access['liAccesses'] = self.getLiAccesses(access['pssgId'], personId)
                else:
                    access['liAccesses'] = self.getLiAccesses(pssgId, access['personId'])
                #When the the access is not allWeek access, startTime, endTime, iSide and 
                #oSide fields are present in each limitedAccess, so we can remove this
                #field from access.
                access.pop('startTime')
                access.pop('endTime')
                access.pop('iSide')
                access.pop('oSide')

        return accesses




    def getLiAccesses(self, pssgId, personId):

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
        sql = ("SELECT id, weekDay, iSide, oSide, startTime, endTime, rowStateId "
               "FROM LimitedAccess WHERE pssgId = {} AND personId = {}"
               "".format(pssgId, personId)
              )
        self.execute(sql)
        liAccesses = self.cursor.fetchall()

        for liAccess in liAccesses:

            liAccess['startTime'] = str(liAccess['startTime'])
            liAccess['endTime'] = str(liAccess['endTime'])

        return liAccesses





    def getUncmtAccesses(self, ctrllerMac, rowStateId):
        '''
        This method is an iterator, in each iteration it returns a access
        not committed with the state "rowStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created. In this case, between each iteration,
        "getPerson" method is executed which would use the same cursor.
        '''


        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = ("SELECT access.* FROM Access access JOIN Passage passage ON "
               "(access.pssgId = passage.id) JOIN Controller controller ON "
               "(passage.controllerId = controller.id) WHERE "
               "controller.macAddress = '{}' AND access.rowStateId = {}"
               "".format(ctrllerMac, rowStateId)
              )

        try:
            cursor.execute(sql)
            access = cursor.fetchone()

            while access:
                #Removing rowStateId as it should not be sent to the controller
                access.pop('rowStateId')
                #As the database retrieves the dates and times as datetime types
                #they are converted to string to be sent to the controller
                access['startTime'] = str(access['startTime'])
                access['endTime'] = str(access['endTime'])
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
        pssgId and personId. This could happen when it is given a full
        access to a person who has limited access.
        '''

        try:

            sql = ("DELETE FROM LimitedAccess WHERE pssgId = {} and personId = {}"
                   "".format(access['pssgId'], access['personId'])
                  )
            self.execute(sql)
            self.connection.commit()


            #If there was a row in access table, it should be overwritten, avoiding the engine
            #complaining by the constraints. For this reason the ID is kept. For this reason it
            #is used "ON DUPLICATE KEY UPDATE" statement.
            sql = ("INSERT INTO Access(pssgId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate, rowStateId) VALUES({}, {}, True, {}, {}, '{}', '{}', '{}', {}) "
                   "ON DUPLICATE KEY UPDATE allWeek = True, iSide = {}, oSide = {}, startTime = '{}', "
                   "endTime = '{}', expireDate = '{}', rowStateId = {}"
                   "".format(access['pssgId'], access['personId'], access['iSide'], access['oSide'],
                             access['startTime'], access['endTime'], access['expireDate'], TO_ADD,
                             access['iSide'], access['oSide'], access['startTime'], access['endTime'],
                             access['expireDate'], TO_ADD)
                  )
            self.execute(sql)
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed
            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(access['pssgId'], access['personId'])
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
        pssgId, personId and allWeek parameter are not modified.
        If a change on them is necessary, the access should be deleted
        and it should be added again.
        '''

        sql = ("UPDATE Access SET iSide = {}, oSide = {}, startTime = '{}', "
               "endTime = '{}', expireDate = '{}', rowStateId = {} WHERE id = {}"
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

        sql = ("UPDATE Access SET rowStateId = {} WHERE id = {}"
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

        sql = "SELECT rowStateId FROM Access WHERE id = {}".format(accessId)

        try:
            self.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Access SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, accessId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif rowState == TO_DELETE:
                sql = ("DELETE FROM Access WHERE id = {}"
                       "".format(accessId)
                      )
                self.execute(sql)
                self.connection.commit()

            elif rowState == COMMITTED:
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








    def getPssgId(self, accessId=None, liAccessId=None):
        '''
        This method is called by CRUD module when it wants to delete an access.
        On that situation, it needs to know the "pssgId" to send the DELETE 
        message to the corresponding controller.
        It can receive "accessId" or "liAccessId" but not both.
        '''

        if accessId and not liAccessId:
            sql = "SELECT pssgId FROM Access WHERE id = {}".format(accessId)

        elif liAccessId and not accessId:
            sql = "SELECT pssgId FROM LimitedAccess WHERE id = {}".format(liAccessId)

        else:
            self.logger.debug('Error with arguments calling getPssgId method')
            raise AccessError('Can not get passage id for this access.')


        try:
            self.execute(sql)
            pssgId = self.cursor.fetchone()['pssgId']
            return pssgId

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not get passage id for this access.')

        except TypeError:
            self.logger.debug('Error fetching pssgId.')
            raise AccessError('Can not get passage id for this access.')






#-------------------------------Limited Access---------------------------------




    def getUncmtLiAccesses(self, ctrllerMac, rowStateId):
        '''
        This method is an iterator, in each iteration it returns a liAccess
        not committed with the state "rowStateId" from the controller
        with the MAC address "ctrllerMac"
        IMPORTANT NOTE: As this method is an iterator and its execution is interrupted
        in each iteration and between each iteration another method can be executed using
        "self.cursor", a separated cursor is created. In this case, between each iteration,
        "getPerson" method is executed which would use the same cursor.
        '''

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        secCursor = self.connection.cursor(pymysql.cursors.DictCursor)


        sql = ("SELECT liAccess.* FROM LimitedAccess liAccess JOIN Passage passage ON "
               "(liAccess.pssgId = passage.id) JOIN Controller controller ON "
               "(passage.controllerId = controller.id) WHERE "
               "controller.macAddress = '{}' AND liAccess.rowStateId = {}"
               "".format(ctrllerMac, rowStateId)
              )

        try:

            cursor.execute(sql)
            liAccess = cursor.fetchone()

            while liAccess:
                #There are some fields from access table that should be sent to the controller
                #when adding or updating a limited access and should be added the "liAccess" dictionary
                secSql = ("SELECT id, expireDate FROM Access WHERE pssgId = {} AND personId = {}"
                          "".format(liAccess['pssgId'], liAccess['personId'])
                         )
                secCursor.execute(secSql)
                row = secCursor.fetchone()
                accessId = row['id']
                expireDate = row['expireDate']
                expireDate = str(expireDate)

                #Removing rowStateId field as it should not be sent to the controller.
                liAccess.pop('rowStateId')
                #Converting datetime types to string types.
                liAccess['startTime'] = str(liAccess['startTime'])
                liAccess['endTime'] = str(liAccess['endTime'])
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
            #combination (pssgId, personId), this method will try to add an entry
            #in "Access" table. For this reason it is used "ON DUPLICATE KEY UPDATE"
            #statement. Also it is necessary to use since when a "allWeek" access is
            #changing to a limited access type.
            #The REPLACE statement was not used because each time it is invoked, the ID
            #will increment since it is a DELETE followed by an INSERT.
            sql = ("INSERT INTO Access(pssgId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate, rowStateId) VALUES({}, {}, FALSE, FALSE, FALSE, NULL, NULL, '{}', {}) "
                   "ON DUPLICATE KEY UPDATE allWeek = FALSE, iSide = FALSE, oSide = FALSE, startTime = NULL, "
                   "endTime = NULL, expireDate = '{}', rowStateId = {}"
                   "".format(liAccess['pssgId'], liAccess['personId'], liAccess['expireDate'], 
                             COMMITTED, liAccess['expireDate'], COMMITTED)
                  )
            self.execute(sql)
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed.
            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['pssgId'], liAccess['personId'])
                  )
            self.execute(sql)
            accessId = self.cursor.fetchone()['id']
            

            sql = ("INSERT INTO LimitedAccess(pssgId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime, rowStateId) VALUES({}, {}, {}, {}, {}, '{}', '{}', {})"
                   "".format(liAccess['pssgId'], liAccess['personId'], liAccess['weekDay'],
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
        pssgId, personId and allWeek parameter are not modified.
        If a change on them is necessary, the access should be deleted
        and it should be added again.
        '''

        try:
            #The only thing we should modify in "Access" table is the "expireDate" field.
            #To modify the access table, we need "pssgId" and "personId"
            sql = ("SELECT pssgId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )

            self.execute(sql)
            row = self.cursor.fetchone()
            pssgId = row['pssgId']
            personId = row['personId']


            sql = ("UPDATE Access SET expireDate = '{}' WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], pssgId, personId)
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}', rowStateId = {} WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], TO_UPDATE,
                             liAccess['id'])
                  )

            self.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()


        except TypeError:
            self.logger.debug('Can not fetching pssgId and perssonId.')
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

        sql = ("UPDATE LimitedAccess SET rowStateId = {} WHERE id = {}"
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
            sql = "SELECT rowStateId FROM LimitedAccess WHERE id = {}".format(liAccessId)
            self.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE LimitedAccess SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, liAccessId)
                      )

                self.execute(sql)
                self.connection.commit()


            elif rowState == TO_DELETE:

                sql = ("SELECT pssgId, personId FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )

                self.execute(sql)
                row = self.cursor.fetchone() #KeyError exception could be raised here
                pssgId = row['pssgId']       #Me parece que es TypeError y no KeyError
                personId = row['personId']
        
                sql = ("DELETE FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )
                self.execute(sql)
                self.connection.commit()


                #Once we delete a limited access, we should verify if there is another
                #limited access with the same "pssgId" and the same "personId", if there
                #is not, we should delete the entry in "access" table.
                sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE pssgId = {} AND personId = {}"
                       "".format(pssgId, personId)
                      )
                self.execute(sql)
                remaining = self.cursor.fetchone()['COUNT(*)']

                if not remaining:
                   sql = ("DELETE FROM Access WHERE pssgId = {} AND personId = {}"
                          "".format(pssgId, personId)
                         )
                   self.execute(sql)
                   self.connection.commit()

            elif rowState == COMMITTED:
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

    sql = ("SELECT pssgId FROM Access WHERE personId = 2 AND allWeek = 0")
    dataBase.execute(sql)
    pssgIds = dataBase.cursor.fetchall()
    pssgIds = [pssgId['pssgId'] for pssgId in pssgIds]
    print(pssgIds)
    for pssgId in pssgIds:
        sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE pssgId = {} AND "
               "personId = {}".format(pssgId, 4)
              )
        dataBase.execute(sql)
        print(dataBase.cursor.fetchone())
        

