import sqlite3
import datetime
import logging


class DataBase(object):
    '''
    This object connects the database in the constructor.
    It implements differents methods to query the database, 
    save events and delete them
    '''

    def __init__(self, dbFile):

        #Connecting to the database
        self.connection = sqlite3.connect(dbFile, check_same_thread=False)
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

        print(sql)
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




    def test(self):
#        sql = ("SELECT person.id, access.allWeek, access.startTime, "
#               "access.endTime, access.expireDate "
#               "FROM Access access JOIN Person person ON (access.personId = person.id) "
#               "WHERE access.pssgId = '1' AND access.iSide = 1 "
#               "AND person.cardNumber = '11806997'"
#               )

        sql = "SELECT * from Events"

        self.cursor.execute(sql)
 #       self.connection.close()
#        self.connection.commit()
        
        params = self.cursor.fetchone()
