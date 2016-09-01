import pymysql
import queue
import logging

from config import *

TO_ADD = 1
TO_UPDATE = 2
COMMITTED = 3
TO_DELETE = 4
DELETED = 5



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

        # With this client_flag, cursor.rowcount will have found rows instead of affected rows
        self.connection = pymysql.connect(host, user, passwd, dataBase, client_flag = pymysql.constants.CLIENT.FOUND_ROWS)
        # The following line makes all "fetch" calls return a dictionary instead a tuple 
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)




    def isValidCtrller(self, ctrllerMac):
        '''
        Returns an Integer when the MAC is registered in DB
        If the MAC is not registered, it returns None
        '''

        #macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(ctrllerMac)

        self.cursor.execute(sql)
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
                self.logger.debug(integrityError)



#----------------------------------Organization----------------------------------------


    def getOrganizations(self):
        '''
        Return a a dictionary with all organizations
        '''
        sql = ('SELECT * FROM Organization')
        self.cursor.execute(sql)
        organizations = self.cursor.fetchall()

        return organizations


                                             

    def addOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and save it in DB
        It returns the id of the added organization.
        '''

        sql = ("INSERT INTO Organization(name) VALUES('{}')"
               "".format(organization['name'])
              )
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not add this organization')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not add this organization')






    def delOrganization(self, organization):
        '''
        Receive a dictionary with id organization and delete the organization.
        '''

        sql = ("DELETE FROM Organization WHERE id = {}"
               "".format(organization['id'])
              )        

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationNotFound('Organization not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not delete this organization')



    def updOrganization(self, organization):
        '''
        Receive a dictionary with organization parametters and update it in DB
        '''

        sql = ("UPDATE Organization SET name = '{}' WHERE id = {}"
               "".format(organization['name'], organization['id'])
              )

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise OrganizationNotFound('Organization not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise OrganizationError('Can not update this organization')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise OrganizationError('Can not update this organization: wrong argument')








#----------------------------------Zone----------------------------------------


    def getZones(self):
        '''
        Return a dictionary with all Zones
        '''
        sql = ('SELECT * FROM Zone')
        self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not add this zone')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not add this zone: wrong argument')



    def delZone(self, zone):
        '''
        Receive a dictionary with id zone and delete the zone
        '''

        sql = ("DELETE FROM Zone WHERE id = {}"
               "".format(zone['id'])
              )

        try:
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise ZoneNotFound('Zone not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ZoneError('Can not update this zone')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ZoneError('Can not update this zone: wrong argument')




#----------------------------------Controller----------------------------------------


    def addController(self, controller):
        '''
        Receive a dictionary with controller parametters and save it in DB
        It returns the id of the added controller.
        '''

        sql = ("INSERT INTO Controller(boardModel, macAddress, ipAddress) "
               "VALUES('{}', '{}', '{}')"
               "".format(controller['boardModel'], controller['macAddress'], 
                         controller['ipAddress'])
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not add this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not add this controller: wrong argument')






    def delController(self, controller):
        '''
        Receive a dictionary with id controller and delete the controller
        '''

        sql = ("DELETE FROM Controller WHERE id = {}"
               "".format(controller['id'])
              )

        try:
            self.cursor.execute(sql)
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

        sql = ("UPDATE Controller SET boardModel = '{}', macAddress = '{}', "
               "ipAddress = '{}' WHERE id = {}"
               "".format(controller['boardModel'], controller['macAddress'], 
                         controller['ipAddress'], controller['id'])
              )

        try:
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise ControllerNotFound('Controller not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise ControllerError('Can not update this controller')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise ControllerError('Can not update this controller: wrong argument')






    def getControllerMac(self, passageId):
        '''
        Return the controller MAC address receiving the passage ID
        '''


        sql = ("SELECT controller.macAddress FROM Controller controller JOIN "
               "Passage passage ON (controller.id = passage.controllerId) WHERE "
               "passage.id = {}".format(passageId)
              )

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()['macAddress']

        except TypeError:
            self.logger.debug('This passage id has not MAC registered')
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
            self.cursor.execute(sql)
            ctrllerMacsToDelPrsn = self.cursor.fetchall()
            ctrllerMacsToDelPrsn = [ctrllerMac['macAddress'] for ctrllerMac in ctrllerMacsToDelPrsn]
            if ctrllerMacsToDelPrsn == []:
                raise TypeError
            return ctrllerMacsToDelPrsn

        except TypeError:
            self.logger.debug('This person is not present in any controller')
            raise PersonNotFound('Person not found') #We should check what to do when the person only in local db




#----------------------------------Passage----------------------------------------


    def getPassages(self, zoneId):
        '''
        Return a dictionary with all passages in a Zone
        '''
        # check if the zoneId exists in the database
        sql = ("SELECT * FROM Zone WHERE id='{}'".format(zoneId))
        self.cursor.execute(sql)
        zone = self.cursor.fetchall()

        if not zone:
            raise ZoneNotFound('Zone not found')
       
        # Get all persons from the organization
        sql = ("SELECT * FROM Passage WHERE zoneId='{}'".format(zoneId))
        self.cursor.execute(sql)
        passages = self.cursor.fetchall()
        
        return passages



    def addPassage(self, passage):
        '''
        Receive a dictionary with passage parametters and save it in DB
        It returns the id of the added passage
        '''

        sql = ("INSERT INTO Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, "
               "bzzrOut, rlseTime, bzzrTime, alrmTime, zoneId, controllerId, rowStateId) "
               "VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
               "".format(passage['i0In'], passage['i1In'], passage['o0In'],
                         passage['o1In'], passage['bttnIn'], passage['stateIn'],
                         passage['rlseOut'], passage['bzzrOut'], passage['rlseTime'], 
                         passage['bzzrTime'], passage['alrmTime'], passage['zoneId'],
                         passage['controllerId'], TO_ADD) 
              )


        try:
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Passage SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, passageId)
                      )
            elif rowState == TO_DELETE:
                sql = ("DELETE FROM Passage WHERE id = {}"
                       "".format(passageId)
                      )
            else:
                self.logger.error("Invalid state detected in Passage table.")

            self.cursor.execute(sql)
            self.connection.commit()
                

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PassageError('Error committing this passage.')

        except TypeError:
            self.logger.debug('Error fetching the passage.')
            raise PassageError('Error committing this passage.')



    def markPassageToDel(self, passageId):
        '''
        Set passage row state in state: TO_DELETE (pending to delete).
        '''

        sql = ("UPDATE Passage SET rowStateId = {} WHERE id = {}"
               "".format(TO_DELETE, passageId)
              )
        try:
            self.cursor.execute(sql)
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

        sql = ("UPDATE Passage SET i0In = {}, i1In = {}, o0In = {}, o1In = {}, "
               "bttnIn = {}, stateIn = {}, rlseOut = {}, bzzrOut = {}, "
               "rlseTime = {}, bzzrTime = {}, alrmTime = {}, zoneId = {}, "
               "controllerId = {}, rowStateId = {} WHERE id = {}"
               "".format(passage['i0In'], passage['i1In'], passage['o0In'],
                         passage['o1In'], passage['bttnIn'], passage['stateIn'],
                         passage['rlseOut'], passage['bzzrOut'], passage['rlseTime'], 
                         passage['bzzrTime'], passage['alrmTime'], passage['zoneId'],
                         passage['controllerId'], TO_UPDATE, passage['id'])
              )

        try:
            self.cursor.execute(sql)
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

    def getPersons(self, orgId):
        '''
        Return a dictionary with all persons in an organization
        '''
        # check if the organization id exist in the database
        sql = ("SELECT * FROM Organization WHERE id='{}'".format(orgId))
        self.cursor.execute(sql)
        organization = self.cursor.fetchall()

        if not organization:
            raise OrganizationNotFound('Organization not found')
        
        # Get all persons from the organization
        sql = ("SELECT * FROM Person WHERE orgId='{}'".format(orgId))
        self.cursor.execute(sql)
        persons = self.cursor.fetchall()
        
        return persons


    def addPerson(self, person):
        '''
        Receive a dictionary with person parametters and save it in DB
        '''

        #RowState should be removed in Person table
        sql = ("INSERT INTO Person(name, cardNumber, orgId, rowStateId) VALUES('{}', {}, {}, {})"
               "".format(person['name'], person['cardNumber'], person['orgId'], COMMITTED)
              )

        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.lastrowid

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not add this person')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not add this person: wrong argument')





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
            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')
            self.connection.commit()


            #To avoid having duplicate MACs in the result list, it is used DISTINCT clause
            #since we can have a Person having access in more than one passage
            #and those passage could be on the same controller (with the same MAC)
            sql = ("SELECT DISTINCT macAddress FROM Controller controller JOIN Passage passage "
                   "ON (controller.id = passage.controllerId) JOIN Access access "
                   "ON (passage.id = access.pssgId) JOIN Person person "
                   "ON (access.personId = person.id) WHERE person.id = {}"
                   "".format(personId)
                  )

            self.cursor.execute(sql)
            ctrllerMacsToDelPrsn = self.cursor.fetchall()
            ctrllerMacsToDelPrsn = [ctrllerMac['macAddress'] for ctrllerMac in ctrllerMacsToDelPrsn]
            
            #If the person is not present in any controller, we should log this situation and
            #remove it from the central DB.
            if ctrllerMacsToDelPrsn == []:
                logMsg = ("This person is not present in any controller. "
                          "Removing it from central DB." 
                         )
                self.logger.debug(logMsg)
                sql = "DELETE FROM Person WHERE id = {}".format(personId)
                self.cursor.execute(sql)
                self.connection.commit()
            
            else:
                #Adding in PersonPendingOperation table: personId, mac address and pending operation
                #Each entry on this table will be removed when each controller answer to the delete 
                #person message.
                values = ''
                for mac in ctrllerMacsToDelPrsn:
                    values += "({}, '{}', {}), ".format(personId, mac, operation)
                #Removing the last coma and space
                values = values[:-2]
                #Using INSERT IGNORE to avoid having duplicates entries on this table (This situation can happen
                #if the server receive more than once a REST command to delete a person and the controller does not
                #confirm the deletion of this person.)
                sql = ("INSERT IGNORE INTO PersonPendingOperation(personId, macAddress, pendingOp) VALUES {}"
                       "".format(values)
                      )
                self.cursor.execute(sql)
                self.connection.commit()

            #If the list of MACs is void or not, we always return it.
            return ctrllerMacsToDelPrsn

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

            self.cursor.execute(sql)
            pendingOp = self.cursor.fetchone()['rowStateId']

            if pendingOp == TO_DELETE:

                #Deleting all the limited accesses of this person on the passages managed by 
                #this controller
                sql = ("DELETE FROM LimitedAccess WHERE personId = {} AND pssgId IN "
                       "(SELECT passage.id FROM Passage passage JOIN Controller controller ON "
                       "(passage.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.cursor.execute(sql)
                self.connection.commit() 

                #Deleting all the accesses of this person on the passages managed by 
                #this controller
                sql = ("DELETE FROM Access WHERE personId = {} AND pssgId IN "
                       "(SELECT passage.id FROM Passage passage JOIN Controller controller ON "
                       "(passage.controllerId = controller.id) WHERE controller.macAddress = '{}')"
                       "".format(personId, ctrllerMac)
                      )
                self.cursor.execute(sql)
                self.connection.commit()                

                #Deleting the entry in "PersonPendingOperation" table which has this person id,
                #this MAC and the corresponding pending operation.
                sql = ("DELETE FROM PersonPendingOperation WHERE personId = {} AND macAddress = '{}' "
                       "AND pendingOp = {}".format(personId, ctrllerMac, TO_DELETE)
                      )
                self.cursor.execute(sql)
                self.connection.commit()

                #If there is not more entries on "PersonPendingOperation" table with this person and 
                #this operation type, it can delete the person definitely from the central database.                
                sql = ("SELECT COUNT(*) FROM PersonPendingOperation WHERE personId = {} "
                       "AND pendingOp = {}".format(personId, TO_DELETE)
                      )
                self.cursor.execute(sql)
                pendCtrllersToDel = self.cursor.fetchone()['COUNT(*)']
                if not pendCtrllersToDel:
                    sql = "DELETE FROM Person WHERE id = {}".format(personId)
                    self.cursor.execute(sql)
                    self.connection.commit()

            elif pendingOp == TO_UPDATE:
                #should be completed
                pass

            else:
                #should be completed                
                pass


        except TypeError:
            self.logger.debug('Error fetching something in commitPerson method.')
            raise PersonError('Error committing this person.')
        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not commit this person.')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not commit this person.')






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
                raise PersonNotFound('Person not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
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
            if self.cursor.rowcount < 1:
                raise PersonNotFound('Person not found')
            self.connection.commit()

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise PersonError('Can not update this person')
        except pymysql.err.InternalError as internalError:
            self.logger.debug(internalError)
            raise PersonError('Can not update this person: wrong argument')





    def getPerson(self, personId):
        '''
        Receive person id and returns a dictionary with person parameters
        '''
        sql = "SELECT id, name, cardNumber FROM Person WHERE id = {}".format(personId)
        #cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(sql)
        person = self.cursor.fetchone()

        if not person:
            raise PersonNotFound('Person not found')

        return person




#-------------------------------Access-----------------------------------


    def getAccesses(self, personId):

        '''
        Return a dictionary with all access with the personId
        '''
        # check if the person id exist in the database
        sql = ("SELECT * FROM Person WHERE id='{}'".format(personId))
        self.cursor.execute(sql)
        person = self.cursor.fetchall()

        if not person:
            raise PersonNotFound('Person not found')

        # Get all persons from the organization
        sql = ("SELECT * FROM Access WHERE personId='{}'".format(personId))
        self.cursor.execute(sql)
        accesses = self.cursor.fetchall()

        return accesses



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
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed
            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(access['pssgId'], access['personId'])
                  )
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE Access SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, accessId)
                      )
            elif rowState == TO_DELETE:
                sql = ("DELETE FROM Access WHERE id = {}"
                       "".format(accessId)
                      )
            else:
                self.logger.error("Invalid state detected in Access table.")

            self.cursor.execute(sql)
            self.connection.commit()


        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Error committing this access.')

        except TypeError:
            self.logger.debug('Error fetching the access.')
            raise AccessError('Error committing this access.')



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
            self.cursor.execute(sql)
            pssgId = self.cursor.fetchone()['pssgId']
            return pssgId

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Can not get passage id for this access.')

        except TypeError:
            self.logger.debug('Error fetching pssgId.')
            raise AccessError('Can not get passage id for this access.')






#-------------------------------Limited Access---------------------------------




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
            self.cursor.execute(sql)
            self.connection.commit()


            #As it is necessary to return the access ID, we could use "cursor.lastrowid" attribute,
            #but when all the parametters are the same and nothing is updated, lastrowid returns 0.
            #For this reason, a SELECT statement should be executed.
            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['pssgId'], liAccess['personId'])
                  )
            self.cursor.execute(sql)
            accessId = self.cursor.fetchone()['id']
            

            sql = ("INSERT INTO LimitedAccess(pssgId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime, rowStateId) VALUES({}, {}, {}, {}, {}, '{}', '{}', {})"
                   "".format(liAccess['pssgId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'], TO_ADD)
                  )
            self.cursor.execute(sql)
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

            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            pssgId = row['pssgId']
            personId = row['personId']


            sql = ("UPDATE Access SET expireDate = '{}' WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], pssgId, personId)
                  )

            self.cursor.execute(sql)
            if self.cursor.rowcount < 1:
                raise AccessNotFound('Access not found')
            self.connection.commit()



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}', rowStateId = {} WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], TO_UPDATE,
                             liAccess['id'])
                  )

            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
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
            self.cursor.execute(sql)
            rowState = self.cursor.fetchone()['rowStateId']

            if rowState in (TO_ADD, TO_UPDATE):
                sql = ("UPDATE LimitedAccess SET rowStateId = {} WHERE id = {}"
                       "".format(COMMITTED, liAccessId)
                      )

                self.cursor.execute(sql)
                self.connection.commit()


            elif rowState == TO_DELETE:

                sql = ("SELECT pssgId, personId FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )

                self.cursor.execute(sql)
                row = self.cursor.fetchone() #KeyError exception could be raised here
                pssgId = row['pssgId']
                personId = row['personId']
        
                sql = ("DELETE FROM LimitedAccess WHERE id = {}"
                       "".format(liAccessId)
                      )
                self.cursor.execute(sql)
                self.connection.commit()


                #Once we delete a limited access, we should verify if there is another
                #limited access with the same "pssgId" and the same "personId", if there
                #is not, we should delete the entry in "access" table.
                sql = ("SELECT COUNT(*) FROM LimitedAccess WHERE pssgId = {} AND personId = {}"
                       "".format(pssgId, personId)
                      )
                self.cursor.execute(sql)
                remaining = self.cursor.fetchone()['COUNT(*)']

                if not remaining:
                   sql = ("DELETE FROM Access WHERE pssgId = {} AND personId = {}"
                          "".format(pssgId, personId)
                         )
                   self.cursor.execute(sql)
                   self.connection.commit()

            else:
                self.logger.error("Invalid state detected in Limited Access table.")

            self.cursor.execute(sql)
            self.connection.commit()


        except KeyError:
            self.logger.debug('Error fetching something in commitLiAccess method.')
            raise AccessError('Error committing this limited access.')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Error committing this limited access.')

        except TypeError:
            self.logger.debug('Error fetching the limited access.')
            raise AccessError('Error committing this limited access.')



