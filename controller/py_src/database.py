import sqlite3
import datetime
import logging




class OperationalError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



class IntegrityError(Exception):
    '''
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def __str__(self):
        return self.errorMessage



class DataBase(object):
    '''
    This object connects the database in the constructor.
    It implements differents methods to query the database, 
    save events and delete them
    '''

    def __init__(self, dbFile):

        #Connecting to the database
        self.connection = sqlite3.connect(dbFile, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
            


        self.cursor = self.connection.cursor()
        #Enabling foreing keys
        self.cursor.execute('PRAGMA foreign_keys = ON')

        #Getting the logger
        self.logger = logging.getLogger('Controller')


    def __del__(self):

        self.connection.close()



    #---------------------------------------------------------------------------#

    def canAccess(self, doorId, side, cardNumber):
        '''
        This method is called by the main thread. It checks if the user identified
        by "cardNumber" is authorized to pass the door identified by "doorId" on
        this "side" of the door.
        It returns three values. The first one is a boolean which tells if the person
        is authorized to pass. The second is the "personId" corresponding to this
        "cardNumber", used to create the event. The last one is the reason of not
        allowing the access in case the access is not permitted.
        '''

        #Dictionary to convert 0 to 'oSide' and 1 'iSide'
        sideColumn = {0:'oSide', 1:'iSide'}[side]

        sql = ("SELECT person.id, access.allWeek, access.startTime, "
               "access.endTime, access.expireDate "
               "FROM Access access JOIN Person person ON (access.personId = person.id) "
               "WHERE access.doorId = '{}' AND access.{} = 1 " 
               "AND person.cardNumber = '{}'"
               "".format(doorId, sideColumn, cardNumber)
               )

        self.cursor.execute(sql)
        params = self.cursor.fetchone()

        if params:
            personId, allWeek, startTime, endTime, expireDate = params
            nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            nowDate, nowTime = nowDateTime.split()

            if nowDate < expireDate:

                if allWeek:

                    if startTime <= nowTime <= endTime:
                        print("Can access!!")
                        return (True, personId, None)
                    else:
                        print("Can NOT access (out of time!!)")
                        return (False, personId, 3)

                else:
                    nowWeekDay = datetime.datetime.now().isoweekday()

                    sql = ("SELECT startTime, endTime FROM LimitedAccess "
                           "WHERE doorId = {} AND personId = {} AND "
                           "weekDay = {} AND {} = 1"
                           "".format(doorId, personId, nowWeekDay, sideColumn)
                          )

                    self.cursor.execute(sql)
                    params = self.cursor.fetchone()

                    if params:
                        startTime, endTime = params

                        if startTime <= nowTime <= endTime:
                            print("Can access!!!")
                            return (True, personId, None)
                        else:
                            print("Can NOT access (out of time!!!)")
                            return (False, personId, 3)

                    else:
                        print("This person has not access on this door/side")
                        return (False, None, 1)

            else:
                print("Can NOT access (expired card)")
                return (False, None, 2)

        else:
            print("This person has not access on this door/side")
            return (False, None, 1)



    
    #---------------------------------------------------------------------------#

    def saveEvent(self, event):
        '''
        Save events in database when no connection to server.
        '''

        if event['personId']:
            personId = event['personId']
        else:
            personId = 'NULL'

        if event['side']:
            side = event['side']
        else:
            side = 'NULL'

        allowed = int(event['allowed'])

        if event['denialCauseId']:
            denialCauseId = event['denialCauseId']
        else:
            denialCauseId = 'NULL'

        if event['doorLockId']:
            doorLockId = event['doorLockId']
        else:
            doorLockId = 'NULL'

            

        sql = ("INSERT INTO Event"
               "(doorId, eventTypeId, dateTime, doorLockId, "
               "personId, side, allowed, denialCauseId) "
               "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
               "".format(event['doorId'], event['eventTypeId'], 
                         event['dateTime'], doorLockId, personId,
                         side, allowed, denialCauseId)
              )

        self.cursor.execute(sql)
        #self.connection.commit()




    #---------------------------------------------------------------------------#

    def getNEvents(self, evtsQtty):
        '''
        On each iteration over this method, it returns a list with
        "evtsQtty" events.
        '''

        sql = ("SELECT id, doorId, eventTypeId, dateTime, doorLockId, "
               "personId, side, allowed, denialCauseId FROM Event "
               "LIMIT {}".format(evtsQtty)
              )

        self.cursor.execute(sql)
        savedEvents = self.cursor.fetchall()

        while savedEvents:
            #List with a dictionary for each event
            toReSendEvents = []
            #List with id of events
            eventIds = []

            #Although "fetchone" method returns a list of object that can
            #be treated as a dictionary, a new dictionary is generated since
            #it is converted to a json object by the "reSendEvents" method of
            #network manager (with this objects which can be treated as a
            #dictionary the convertion could not work), and also it is
            #necessary remove the id and convert the "allowed" column to bool.
            for savedEvent in savedEvents:
                toReSendEvent = {'doorId' : savedEvent['doorId'],
                                 'eventTypeId' : savedEvent['eventTypeId'],
                                 'dateTime' : savedEvent['dateTime'],
                                 'doorLockId' : savedEvent['doorLockId'],
                                 'personId' : savedEvent['personId'],
                                 'side' : savedEvent['side'],
                                 'allowed' : bool(savedEvent['allowed']),
                                 'denialCauseId' : savedEvent['denialCauseId']
                                }
                toReSendEvents.append(toReSendEvent)
                eventIds.append(savedEvent['id'])

            yield eventIds, toReSendEvents
            self.cursor.execute(sql)
            savedEvents = self.cursor.fetchall()




    #---------------------------------------------------------------------------#

    def delEvents(self, evtIdList):
        '''
        Delete event rows from database.
        The method receives a list with database event ids.
        '''

        #Converting the ids to string type to write the sql statement
        evtIdList = [str(evtId) for evtId in evtIdList]
        #Creating a single string with all ids comma separated
        evtIds = ', '.join(evtIdList)
        
        sql = "DELETE FROM Event WHERE id IN ({})".format(evtIds)

        self.cursor.execute(sql)
        #self.connection.commit()





    #---------------------------------------------------------------------------#


    def getGpioNames(self):
        '''
        Getting Door GPIO Names from SQL database
        '''

        sql = "SELECT * FROM DoorGpios"
        self.cursor.execute(sql)

        #To leave the DB unlocked for other threads, it is necesary to
        #fetch all the rows from the cursor
        self.cursor.fetchall()

        return [i[0] for i in self.cursor.description]




    #---------------------------------------------------------------------------#


    def getGpiosDoors(self):
        '''
        Return a list with "dictionaries" with GPIOs of each door indexed
        by GPIO name
        '''

        sql = "SELECT * FROM DoorGpios"
        self.cursor.execute(sql)
        gpiosDoors = self.cursor.fetchall()


        return gpiosDoors



    #---------------------------------------------------------------------------#

    def getParamsDoors(self):
        '''
        Get the arguments of doors to call ioiface external program.
        pps = Door Parametters

        '''
 
        sql = ("SELECT Door.id, Door.doorNum, DoorGpios.rlseOut, DoorGpios.bzzrOut, "
               "Door.rlseTime, Door.bzzrTime, Door.alrmTime FROM "
               "DoorGpios JOIN Door ON (DoorGpios.id = Door.doorNum)"
              )
                     
        self.cursor.execute(sql)
        paramsDoors = self.cursor.fetchall()

        return paramsDoors



    #---------------------------------------------------------------------------#

    def addDoor(self, door):
        '''
        Receive a door dictionary and add it into DB
        '''


        try:
            #Using INSERT OR IGNORE instead of INSERT to answer with OK when the Crud Resender Module of
            #the server send a limited access CRUD before the client respond and avoid integrity error.
            #Using REPLACE is not good since it has to DELETE and INSERT always.
            sql = ("INSERT OR IGNORE INTO Door(id, doorNum, rlseTime, bzzrTime, alrmTime) "
                   "VALUES({}, {}, {}, {}, {})"
                   "".format(door['id'], door['doorNum'], door['rlseTime'],
                             door['bzzrTime'], door['alrmTime'])
                  )
            self.cursor.execute(sql)
            #self.connection.commit()


        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding a Door.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error adding a Door.')




    #---------------------------------------------------------------------------#

    def updDoor(self, door):
        '''
        Receive a door dictionary and add it into DB
        '''

        try:
            sql = ("UPDATE Door SET doorNum = {}, rlseTime = {}, "
                   "bzzrTime = {}, alrmTime = {} WHERE id = {}"
                   "".format(door['doorNum'], door['rlseTime'], 
                             door['bzzrTime'], door['alrmTime'], 
                             door['id'])
              )
            self.cursor.execute(sql)
            #self.connection.commit()


        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error updating a door.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error updating a door.')




    #---------------------------------------------------------------------------#

    def delDoor(self, door):
        '''
        Receive a door dictionary and delete it.
        All access and limited access on these door will be automatically deleted 
        by the db engine as "ON DELETE CASCADE" clause is present.
        Then all the persons who has no access to any door are also deleted manually.
        '''

        try:
            sql = "DELETE FROM Door WHERE id = {}".format(door['id'])
            self.cursor.execute(sql)
            #self.connection.commit()


            sql = ("DELETE FROM Person WHERE id NOT IN "
                   "(SELECT DISTINCT personId FROM Access) AND id != 1"
                  )
            self.cursor.execute(sql)
            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error deleting a door.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting a door.')






    #---------------------------------------------------------------------------#

    def addAccess(self, access):
        '''
        Receive an access dictionary and add it into DB.
        The access dictionary include person parametters. This method try to 
        add this person to database if it is not present.
        '''

        try:
            #Using INSERT OR IGNORE because the second time an access is added
            #with the same person, an INSERT would throw an integrity error.
            #Using REPLACE was a problem because REPLACE = (DELETE and INSERT) and DELETE
            #a Person will delete the previous accesses added because the Access
            #table has ON CASCADE DELETE clause on personId columns. On this situation we 
            #always end up with only one limited access row for this person
            sql = ("INSERT OR IGNORE INTO Person(id, cardNumber) VALUES({}, {})"
                   "".format(access['personId'], access['cardNumber'])
                  )
            self.cursor.execute(sql)
            #self.connection.commit() 


            #Using REPLACE instead of INSERT because we could be in a situation of replacing
            #a limited access with a full access with the same ID.
            #Also, the crud resender module of a server can send a CRUD again before the client
            #answer, receiving it twice. In this situation it is important to answer to the server
            #with OK to avoid server continue sending the CRUD. If INSERT will be used, a constraint
            #error will happen and the client will never answer with OK.
            sql = ("REPLACE INTO Access(id, doorId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate) VALUES({}, {}, {}, 1, {}, {}, '{}', '{}', '{}')"
                   "".format(access['id'], access['doorId'], access['personId'],
                             access['iSide'], access['oSide'], access['startTime'],
                             access['endTime'], access['expireDate'])
                  )
            self.cursor.execute(sql)
            
            #Everytime an all week access is added, all limited accesses should be deleted if exist.
            sql = ("DELETE FROM LimitedAccess WHERE doorId = {} AND personId = {}"
                   "".format(access['doorId'], access['personId'])
                  )
            self.cursor.execute(sql)

            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding an Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error adding an Access.')



    #---------------------------------------------------------------------------#

    def updAccess(self, access):
        '''
        Receive an access dictionary and update it into DB.
        '''

        try:
            sql = ("UPDATE Access SET iSide = {}, oSide = {}, startTime = '{}', "
                   "endTime = '{}', expireDate = '{}' WHERE id = {}"
                   "".format(access['iSide'], access['oSide'], access['startTime'],
                             access['endTime'], access['expireDate'], access['id'])
                  )
            self.cursor.execute(sql)
            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error updating an Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error updating an Access.')



    #---------------------------------------------------------------------------#

    def delAccess(self, access):
        '''
        Receive an access dictionary and delete it.
        Then all the persons who has no access to any door are also deleted manually.
        '''
        try:

            sql = "SELECT allWeek, doorId, personId FROM Access WHERE id = {}".format(access['id'])
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            allWeek = row[0]
            #The following fields will be used when deleting an entire Limited Access.
            doorId = row[1]
            personId = row[2]

            #When the access is a Limited Access, all the entries in LimitedAccess should be deleted too.
            if not allWeek:
                sql = "DELETE FROM LimitedAccess WHERE doorId = {} AND personId = {}".format(doorId, personId)
                self.cursor.execute(sql)

            sql = "DELETE FROM Access WHERE id = {}".format(access['id'])
            self.cursor.execute(sql)

            #Deleting all persons who have no access to any door.
            sql = ("DELETE FROM Person WHERE id NOT IN "
                   "(SELECT DISTINCT personId FROM Access) AND id != 1"
                  )
            self.cursor.execute(sql)
            #self.connection.commit()


        except TypeError:
            #This exception can happen when the server asks the controller
            #to delete an Access that doesn't exists. On this situation,
            #the controller should answer to the server with OK to avoid
            #the server resend this DELETE message.
            #For this reason, on this situation an exception is not thrown.
            self.logger.warning('Can not find a Access with this id.')
            #raise IntegrityError('Integrity error deleting an Access.')

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error deleting an Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting an Access.')



    #---------------------------------------------------------------------------#

    def addLiAccess(self, liAccess):
        '''
        Receive a limited access dictionary and add it into DB.
        The limited access dictionary include person parametters. This method try to 
        add this person to database if it is not present.
        '''

        try:
            #Using INSERT OR IGNORE because the second time a limited access is added
            #with the same person, an INSERT would throw an integrity error.
            #Using REPLACE was a problem because REPLACE = (DELETE and INSERT) and DELETE
            #a Person will delete the previous limited accesses added because the LimitedAccess
            #table has ON CASCADE DELETE clause on personId columns. On this situation we 
            #always end up with only one limited access row for this person
            sql = ("INSERT OR IGNORE INTO Person(id, cardNumber) VALUES({}, {})"
                   "".format(liAccess['personId'], liAccess['cardNumber'])
                  )
            self.cursor.execute(sql)
            #self.connection.commit()


            #Using REPLACE instead of INSERT because we could be in a situation of replacing
            #a full access with a limited access with the same ID.
            #Also, the crud resender module of a server can send a CRUD again before the client
            #answer, receiving it twice. In this situation it is important to answer to the server
            #with OK to avoid server continue sending the CRUD. If INSERT will be used, a constraint
            #error will happen and the client will never answer with OK.
            #Important Note: iSide and oSide should be filled with "1", because the way "canAccess"
            #method work. The real iSide an oSide is in the LimitedAccess table.
            sql = ("REPLACE INTO Access(id, doorId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate) VALUES({}, {}, {}, 0, 1, 1, NULL, NULL, '{}')"
                   "".format(liAccess['accessId'], liAccess['doorId'],
                             liAccess['personId'], liAccess['expireDate'])
                  )
            self.cursor.execute(sql)

            #Using REPLACE instead of INSERT to answer with OK when the Crud Resender Module of
            #the server send a limited access CRUD before the client respond and avoid integrity error.
            sql = ("REPLACE INTO LimitedAccess(id, doorId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime) VALUES({}, {}, {}, {}, {}, {}, '{}', '{}')"
                   "".format(liAccess['id'], liAccess['doorId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'])

                  )
            self.cursor.execute(sql)

            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding a Limited Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error adding a Limited Access.')




    #---------------------------------------------------------------------------#

    def updLiAccess(self, liAccess):
        '''
        Receive an access dictionary and update it into DB.
        '''

        try:

            sql = ("SELECT doorId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            doorId = row[0]
            personId = row[1]
            

            sql = ("UPDATE Access SET expireDate = '{}' WHERE doorId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], doorId, personId)
                  )
            self.cursor.execute(sql)
            #self.connection.commit()



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}' WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], liAccess['id'])
                  )

            self.cursor.execute(sql)
            #self.connection.commit()


        except TypeError:
            self.logger.debug('Can not find a Limited Access with this id.')
            raise IntegrityError('Integrity error updating a Limited Access.')

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error updating a Limited Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error updating a Limited Access.')




    #---------------------------------------------------------------------------#

    def delLiAccess(self, liAccess):
        '''
        Receive an access dictionary and delete it.
        Then all the persons who has no access to any door are also deleted manually.
        '''
        try:
            sql = "SELECT doorId, personId FROM LimitedAccess WHERE id = {}".format(liAccess['id'])
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            doorId = row[0]
            personId = row[1]
            
            sql = "DELETE FROM LimitedAccess WHERE id = {}".format(liAccess['id'])
            self.cursor.execute(sql)
            #self.connection.commit()

            sql = ("SELECT * FROM LimitedAccess WHERE doorId = {} AND personId = {}"
                   "".format(doorId, personId)
                  )
            self.cursor.execute(sql)
            
            #If there is not more limited access from this person in this door,
            #the entry in access table should be deleted and also the person from 
            #Person table in case this person has not access on any other door
            if not self.cursor.fetchone():
                
                sql = ("DELETE FROM Access WHERE doorId = {} AND personId = {}"
                       "".format(doorId, personId)
                      )
                self.cursor.execute(sql)
                #self.connection.commit()

                 
                sql = ("DELETE FROM Person WHERE id NOT IN "
                       "(SELECT DISTINCT personId FROM Access) AND id != 1"
                      )
                self.cursor.execute(sql)
                #self.connection.commit()



        except TypeError:
            #This exception can happen when the server asks the controller
            #to delete an Access that doesn't exists. On this situation,
            #the controller should answer to the server with OK to avoid
            #the server resend this DELETE message.
            #For this reason, on this situation an exception is not thrown.
            self.logger.warning('Can not find a Limited Access with this id.')
            #raise IntegrityError('Integrity error deleting a Limited Access.')

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error deleting a LimitedAccess.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting a LimitedAccess.')




    #---------------------------------------------------------------------------#

    def updPerson(self, person):
        '''
        Receive a person dictionary and update it.
        '''
        try:
            sql = ("UPDATE Person SET cardNumber = {} WHERE id = {}"
                   "".format(person['cardNumber'], person['id'])
                  )
            self.cursor.execute(sql)
            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error updating a Person.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting a Person.')



    #---------------------------------------------------------------------------#

    def delPerson(self, person):
        '''
        Receive a person dictionary and delete it.
        All access and limited access on these door will be automatically deleted 
        by the db engine as "ON DELETE CASCADE" clause is present.
        '''
        try:
            sql = "DELETE FROM Person WHERE id = {}".format(person['id'])
            self.cursor.execute(sql)
            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error deleting a Person.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting a Person.')


    #---------------------------------------------------------------------------#

    def clearDatabase(self):
        '''
        Remove all LimitedAccess, Access, Persons, Doors and Events
        This method is called when the controller receive from server
        RRP message
        '''

        try:
            sql = "DELETE FROM LimitedAccess"
            self.cursor.execute(sql)
            #self.connection.commit()

            sql = "DELETE FROM Access"
            self.cursor.execute(sql)
            #self.connection.commit()
            
            sql = "DELETE FROM Person WHERE id != 1"
            self.cursor.execute(sql)
            #self.connection.commit()

            sql = "DELETE FROM Door"
            self.cursor.execute(sql)
            #self.connection.commit()
            
            sql = "DELETE FROM Event"
            self.cursor.execute(sql)
            #self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error clearing the data base.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error clearing the data base.')

