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
        self.connection = sqlite3.connect(dbFile)
        self.cursor = self.connection.cursor()
        #Enabling foreing keys
        self.cursor.execute('PRAGMA foreign_keys = ON')

        #Getting the logger
        self.logger = logging.getLogger('Controller')



    #---------------------------------------------------------------------------#

    def canAccess(self, pssgId, side, cardNumber):
        '''
        This method is called by the main thread. It checks if the user identified
        by "cardNumber" is authorized to pass the passage identified by "pssgId" on
        this "side" of the passage.
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
               "WHERE access.pssgId = '{}' AND access.{} = 1 " 
               "AND person.cardNumber = '{}'"
               "".format(pssgId, sideColumn, cardNumber)
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
                           "WHERE pssgId = {} AND personId = {} AND "
                           "weekDay = {} AND {} = 1"
                           "".format(pssgId, personId, nowWeekDay, sideColumn)
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
                        print("This person has not access on this pssg/side")
                        return (False, None, 1)

            else:
                print("Can NOT access (expired card)")
                return (False, None, 2)

        else:
            print("This person has not access on this pssg/side")
            return (False, None, 1)


        print(params)


    
    #---------------------------------------------------------------------------#

    def saveEvent(self, event):
        '''
        Save events in database when no connection to server.
        '''

        if event['personId']:
            personId = event['personId']
        else:
            personId = 'NULL'

        side = event['side']

        allowed = int(event['allowed'])

        if event['notReason']:
            notReason = event['notReason']
        else:
            notReason = 'NULL'
            

        sql = ("INSERT INTO Events"
               "(pssgId, eventType, dateTime, latchType, "
               "personId, side, allowed, notReason) "
               "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
               "".format(event['pssgId'], event['eventType'], 
                         event['dateTime'], event['latchType'], 
                         personId, side, allowed, notReason)
              )

        self.cursor.execute(sql)
        self.connection.commit()



    #---------------------------------------------------------------------------#

    def getNEvents(self, evtsQtty):
        '''
        On each iteration over this method, it returns a list with
        "evtsQtty" events.
        '''
        
        sql = ("SELECT id, pssgId, eventType, dateTime, latchType, "
               "personId, side, allowed, notReason FROM Events "
               "LIMIT {}".format(evtsQtty)
              )

        self.cursor.execute(sql)
        evtTupleList = self.cursor.fetchall()

        while evtTupleList:

            #List with a dictionary for each event
            evtDictList = []
            #List with events id of the database
            evtIdList = []

            #Creating a dictionary for each row retrieved from the DB
            #and appending it to "evtDictList".
            #Apending the event id of DB to "evtIdList"
            for evtTuple in evtTupleList:
                evtDict = {'pssgId' : evtTuple[1],
                           'eventType' : evtTuple[2],
                           'dateTime' : evtTuple[3],
                           'latchType' : evtTuple[4],
                           'personId' : evtTuple[5],
                           'side' : evtTuple[6],
                           'allowed' : bool(evtTuple[7]),
                           'notReason' : evtTuple[8]
                          }

                evtDictList.append(evtDict)
                evtIdList.append(evtTuple[0])

            #This commit is to avoid leaving the database locked. (Not sure if necessary)            
            #self.connection.commit()
            yield evtIdList, evtDictList
            self.cursor.execute(sql)
            evtTupleList = self.cursor.fetchall()

        #self.connection.commit()



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
        
        sql = "DELETE FROM Events WHERE id IN ({})".format(evtIds)

        self.cursor.execute(sql)
        self.connection.commit()



    #---------------------------------------------------------------------------#

    def getPssgParamsNames(self):
        '''
        Getting Passage Params Names from SQL database
        '''

        sql = "SELECT * FROM Passage"
        self.cursor.execute(sql)

        #To leave the DB unlocked for other threads, it is necesary to
        #fetch all the rows from the cursor
        self.cursor.fetchall()
        self.connection.commit()

        return [i[0] for i in self.cursor.description]



    #---------------------------------------------------------------------------#

    def getPssgsParams(self):
        '''
        Get the arguments of passages to call ioiface external program.
        pps = Passage Parametters

        '''
        #Getting the list with all Passage Parametters
        ppsNames = self.getPssgParamsNames()
        #Joining it in a string separated by ','
        ppsNamesStr = ', '.join(ppsNames)

        sql = "SELECT {} FROM Passage".format(ppsNamesStr)
                      
        self.cursor.execute(sql)
        ppsTuplesList = self.cursor.fetchall()
        self.connection.commit()

        #Dictionary containing dictionaries with all the pps indexed by the pps name.
        #This dictionary is indexed by the passage id
        ppsDictsDict = {}

        for ppsTuple in ppsTuplesList:
            #Dictionary with all the pps for each passage indexed by the name of parametters.
            ppsDict = {}

            for i, ppName in enumerate(ppsNames):
                ppsDict[ppName] = ppsTuple[i]
            #Each dictionary is indexed in the master dictionary "ppsDictsDict" by the passage id 
            ppsDictsDict[ppsDict['id']] = ppsDict

        return ppsDictsDict



    #---------------------------------------------------------------------------#

    def addPassage(self, passage):
        '''
        Receive a passage dictionary and add it into DB
        '''

        try:

            sql = ("INSERT INTO Passage(id, i0In, i1In, o0In, o1In, bttnIn, stateIn, "
                   "rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) "
                   "VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
                   "".format(passage['id'], passage['i0In'], passage['i1In'], passage['o0In'], 
                             passage['o1In'], passage['bttnIn'], passage['stateIn'], 
                             passage['rlseOut'], passage['bzzrOut'], passage['rlseTime'],
                             passage['bzzrTime'], passage['alrmTime'])
                  )
            self.cursor.execute(sql)
            self.connection.commit()


        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding a Passage.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error adding a Passage.')




    #---------------------------------------------------------------------------#

    def updPassage(self, passage):
        '''
        Receive a passage dictionary and add it into DB
        '''

        sql = ("UPDATE Passage SET i0In = {}, i1In = {}, o0In = {}, o1In = {}, "
               "bttnIn = {}, stateIn = {}, rlseOut = {}, bzzrOut = {}, rlseTime = {}, "
               "bzzrTime = {}, alrmTime = {} WHERE id = {}"
               "".format(passage['i0In'], passage['i1In'], passage['o0In'],
                         passage['o1In'], passage['bttnIn'], passage['stateIn'],
                         passage['rlseOut'], passage['bzzrOut'], passage['rlseTime'],
                         passage['bzzrTime'], passage['alrmTime'], passage['id'])
              )
        self.cursor.execute(sql)
        self.connection.commit()




    #---------------------------------------------------------------------------#

    def delPassage(self, passage):
        '''
        Receive a passage dictionary and delete it.
        All access and limited access on these passage will be automatically deleted 
        by the db engine as "ON DELETE CASCADE" clause is present.
        Then all the persons who has no access to any passage are also deleted manually.
        '''

        sql = "DELETE FROM Passage WHERE id = {}".format(passage['id'])
        self.cursor.execute(sql)
        self.connection.commit()

        sql = "DELETE FROM Person WHERE id NOT IN (SELECT DISTINCT personId FROM Access)"
        self.cursor.execute(sql)
        self.connection.commit()




    #---------------------------------------------------------------------------#

    def addAccess(self, access):
        '''
        Receive an access dictionary and add it into DB.
        The access dictionary include person parametters. This method try to 
        add this person to database if it is not present.
        '''

        try:        
            sql = ("INSERT INTO Person(id, cardNumber) VALUES({}, {})"
                   "".format(access['personId'], access['cardNumber'])
                  )
            self.cursor.execute(sql)
            self.connection.commit() 

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding a Person.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.logger.info('The person is already in local DB.')
        

        try:
            sql = ("REPLACE INTO Access(id, pssgId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate) VALUES({}, {}, {}, 1, {}, {}, '{}', '{}', '{}')"
                   "".format(access['id'], access['pssgId'], access['personId'],
                             access['iSide'], access['oSide'], access['startTime'],
                             access['endTime'], access['expireDate'])
                  )
            self.cursor.execute(sql)
            
            #Everytime an all week access is added, all limited accesses should be deleted if exist.
            sql = ("DELETE FROM LimitedAccess WHERE pssgId = {} AND personId = {}"
                   "".format(access['pssgId'], access['personId'])
                  )
            self.cursor.execute(sql)

            self.connection.commit()

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
            self.connection.commit()

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
        Then all the persons who has no access to any passage are also deleted manually.
        '''
        try:
            sql = "DELETE FROM Access WHERE id = {}".format(access['id'])
            self.cursor.execute(sql)

            sql = "DELETE FROM Person WHERE id NOT IN (SELECT DISTINCT personId FROM Access)"
            self.cursor.execute(sql)
            self.connection.commit()

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
            sql = ("INSERT INTO Person(id, cardNumber) VALUES({}, {})"
                   "".format(liAccess['personId'], liAccess['cardNumber'])
                  )
            self.cursor.execute(sql)
            self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error adding a Person.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            self.logger.info('The person is already in local DB.')


        try:
            sql = ("REPLACE INTO Access(id, pssgId, personId, allWeek, iSide, oSide, startTime, "
                   "endTime, expireDate) VALUES({}, {}, {}, 0, 0, 0, NULL, NULL, '{}')"
                   "".format(liAccess['accessId'], liAccess['pssgId'],
                             liAccess['personId'], liAccess['expireDate'])
                  )
            self.cursor.execute(sql)


            sql = ("INSERT INTO LimitedAccess(id, pssgId, personId, weekDay, iSide, oSide, startTime, "
                   "endTime) VALUES({}, {}, {}, {}, {}, {}, '{}', '{}')"
                   "".format(liAccess['id'], liAccess['pssgId'], liAccess['personId'], liAccess['weekDay'],
                             liAccess['iSide'], liAccess['oSide'], liAccess['startTime'],
                             liAccess['endTime'])

                  )
            self.cursor.execute(sql)

            self.connection.commit()

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

            sql = ("SELECT pssgId, personId FROM LimitedAccess WHERE id = {}"
                   "".format(liAccess['id'])
                  )
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            pssgId = row[0]
            personId = row[1]
            

            sql = ("UPDATE Access SET expireDate = '{}' WHERE pssgId = {} AND personId = {}"
                   "".format(liAccess['expireDate'], pssgId, personId)
                  )
            self.cursor.execute(sql)
            self.connection.commit()



            sql = ("UPDATE LimitedAccess SET weekDay = {}, iSide = {}, oSide = {}, "
                   "startTime = '{}', endTime = '{}' WHERE id = {}"
                   "".format(liAccess['weekDay'], liAccess['iSide'], liAccess['oSide'],
                             liAccess['startTime'], liAccess['endTime'], liAccess['id'])
                  )

            self.cursor.execute(sql)
            self.connection.commit()


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
        Then all the persons who has no access to any passage are also deleted manually.
        '''
        try:
            sql = "DELETE FROM Access WHERE id = {}".format(access['id'])
            self.cursor.execute(sql)

            sql = "DELETE FROM Person WHERE id NOT IN (SELECT DISTINCT personId FROM Access)"
            self.cursor.execute(sql)
            self.connection.commit()

        except sqlite3.OperationalError as operationalError:
            self.logger.debug(operationalError)
            raise OperationalError('Operational error deleting an Access.')

        except sqlite3.IntegrityError as integrityError:
            self.logger.debug(integrityError)
            raise IntegrityError('Integrity error deleting an Access.')

