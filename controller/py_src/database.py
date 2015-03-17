import sqlite3
import datetime



boolSide = {'o':0, 'i':1}


class DataBase(object):

    def __init__(self, dbFile):

        #self.connection = sqlite3.connect(dbFile, check_same_thread=False)
        self.connection = sqlite3.connect(dbFile)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')



    def canAccess(self, doorId, side, cardNumber):
        '''
        This method
        '''

        sqlSentence = ("SELECT person.id, access.allWeek, access.startTime, "
                       "access.endTime, access.expireDate "
                       "FROM Access access JOIN Person person ON (access.personId = person.id) "
                       "WHERE access.doorId = '{}' AND access.{}Side = 1 " 
                       "AND person.cardNumber = '{}'"
                       "".format(doorId, side, cardNumber)
                      )

        self.cursor.execute(sqlSentence)
        params = self.cursor.fetchone()

        if params:
            personId, allWeek, startTime, endTime, expireDate = params
            nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            nowDate, nowTime = nowDateTime.split()

            if nowDate < expireDate:

                if allWeek:

                    if startTime < nowTime < endTime:
                        print("Can access!!")
                        return (True, personId, None)
                    else:
                        print("Can NOT access (out of time!!)")
                        return (False, personId, 3)

                else:
                    nowWeekDay = datetime.datetime.now().isoweekday()

                    sqlSentence = ("SELECT startTime, endTime FROM LimitedAccess "
                                   "WHERE doorId = {} AND personId = {} AND "
                                   "weekDay = {}".format(doorId, personId, nowWeekDay)
                                  )

                    self.cursor.execute(sqlSentence)
                    params = self.cursor.fetchone()

                    if params:
                        startTime, endTime = params

                        if startTime < nowTime < endTime:
                            print("Can access!!!")
                            return (True, personId, None)
                        else:
                            print("Can NOT access (out of time!!!)")
                            return (False, personId, 3)

                    else:
                        print("Error. Card number not in LimitedAccess table")
                        return (False, None, 9)

            else:
                return (False, None, 2)
                print("Can NOT access (expired card)")

        else:
            return (False, None, 1)
            print("This person has not access on this door/side")


        print(params)

    
    def saveEvent(self, event):
        '''
        Save events in database when no connection to server.
        '''

        print(event)

        if event['personId']:
            personId = event['personId']
        else:
            personId = 'NULL'

        side = boolSide[event['side']]

        allowed = int(event['allowed'])

        if event['notReason']:
            notReason = event['notReason']
        else:
            notReason = 'NULL'
            

        sqlSentence = ("INSERT INTO Events"
                       "(doorId, eventType, dateTime, latchType, "
                       "personId, side, allowed, notReason) "
                       "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
                       "".format(event['doorId'], event['eventType'], 
                                 event['dateTime'], event['latchType'], 
                                 personId, side, allowed, notReason)
                      )
        self.cursor.execute(sqlSentence)
        self.connection.commit()



    def getNEvents(self, evtsQtty):
        '''
        On each iteration over this method, it returns a list with
        "evtsQtty" events 
        '''
        
        sqlSentence = ("SELECT id, doorId, eventType, dateTime, latchType, "
                       "personId, side, allowed, notReason FROM Events "
                       "LIMIT {}".format(evtsQtty)
                      )

        self.cursor.execute(sqlSentence)
        evtTupleList = self.cursor.fetchall()



        while evtTupleList:


            evtDictList = []
            evtIdList = []
            for evtTuple in evtTupleList:
                evtDict = {'doorId' : evtTuple[1],
                           'eventType' : evtTuple[2],
                           'dateTime' : evtTuple[3],
                           'latchType' : evtTuple[4],
                           'personId' : evtTuple[5],
                           'side' : evtTuple[6],
                           'allowed' : evtTuple[7],
                           'notReason' : evtTuple[8]
                          }
                evtDictList.append(evtDict)
                evtIdList.append(evtTuple[0])
            
            self.connection.commit()
            yield evtIdList, evtDictList
            self.cursor.execute(sqlSentence)
            evtTupleList = self.cursor.fetchall()

        self.connection.commit()



    def delEvents(self, evtIdList):
        '''
        Delete Events with
        '''

        evtIdStrList = [str(evtId) for evtId in evtIdList]

        evtIdsStr = '({})'.format(','.join(evtIdStrList))
        
        sqlSentence = "DELETE FROM Events WHERE id IN {}".format(evtIdsStr)

        self.cursor.execute(sqlSentence)
        self.connection.commit()

