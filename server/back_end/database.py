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

        #Creating a separate connection since this method will be called from
        #different thread
        connection = pymysql.connect(self.host, self.user, self.passwd, self.dataBase)
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)

        #macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(ctrllerMac)

        cursor.execute(sql)
        return cursor.fetchone()['COUNT(*)']




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





#----------------------------------Passage----------------------------------------


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




    def addAccess(self, access):
        '''
        Receive a dictionary with access parametters and save it in DB
        '''

        try:

            sql = ("DELETE FROM LimitedAccess WHERE pssgId = {} and personId = {}"
                   "".format(access['pssgId'], access['personId'])
                  )
            self.cursor.execute(sql)
            self.connection.commit()


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


            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(access['pssgId'], access['personId'])
                  )
            self.cursor.execute(sql)
            return self.cursor.fetchone()['id']


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
        Receive a dictionary with access parametters and save it in DB
        '''

        try:

            sql = ("INSERT INTO Access(pssgId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate, rowStateId) VALUES({}, {}, FALSE, FALSE, FALSE, NULL, NULL, '{}', {}) "
                   "ON DUPLICATE KEY UPDATE allWeek = FALSE, iSide = FALSE, oSide = FALSE, startTime = NULL, "
                   "endTime = NULL, expireDate = '{}', rowStateId = {}"
                   "".format(liAccess['pssgId'], liAccess['personId'], liAccess['expireDate'], 
                             COMMITTED, liAccess['expireDate'], COMMITTED)
                  )


            self.cursor.execute(sql)
            self.connection.commit()

            sql = ("SELECT id FROM Access WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['pssgId'], liAccess['personId'])
                  )
            self.cursor.execute(sql)
            accessId = self.cursor.fetchone()['id']
            
            #accessId = self.cursor.lastrowid


            sql = ("INSERT INTO LimitedAccess(pssgId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime, rowStateId) VALUES({}, {}, {}, {}, {}, '{}', '{}', {})"
                   "".format(liAccess['pssgId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'], TO_ADD)
                  )
            self.cursor.execute(sql)
            self.connection.commit()
            liAccessId = self.cursor.lastrowid
            print(accessId, liAccessId)
            return accessId, liAccessId

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

            sql = ("SELECT pssgId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )

            self.cursor.execute(sql)
            row = self.cursor.fetchone() #KeyError exception could be raised here
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
        Set access row state in the server DB for a pending delete.
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

        sql = "SELECT rowStateId FROM LimitedAccess WHERE id = {}".format(liAccessId)

        try:
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
            self.logger.debug('Error getting the amount of remaining limited access')
            raise AccessError('Error committing this limited access.')

        except pymysql.err.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise AccessError('Error committing this limited access.')

        except TypeError:
            self.logger.debug('Error fetching the limited access.')
            raise AccessError('Error committing this limited access.')



