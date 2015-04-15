import sqlite3
import datetime
import logging


class DataBase(object):

    def __init__(self, dbFile):

        #self.connection = sqlite3.connect(dbFile, check_same_thread=False)
        self.connection = sqlite3.connect(dbFile)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')

        #Getting the logger
        self.logger = logging.getLogger('Controller')



    def canAccess(self, pssgId, side, cardNumber):
        '''
        This method
        '''

        sideColumn = {0:'oSide', 1:'iSide'}[side]

        sqlSentence = ("SELECT person.id, access.allWeek, access.startTime, "
                       "access.endTime, access.expireDate "
                       "FROM Access access JOIN Person person ON (access.personId = person.id) "
                       "WHERE access.pssgId = '{}' AND access.{} = 1 " 
                       "AND person.cardNumber = '{}'"
                       "".format(pssgId, sideColumn, cardNumber)
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
                                   "WHERE pssgId = {} AND personId = {} AND "
                                   "weekDay = {} AND {} = 1"
                                   "".format(pssgId, personId, nowWeekDay, sideColumn)
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
                        print("This person has not access on this pssg/side")
                        return (False, None, 1)

            else:
                return (False, None, 2)
                print("Can NOT access (expired card)")

        else:
            print("This person has not access on this pssg/side")
            return (False, None, 1)


        print(params)

    
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
            

        sqlSentence = ("INSERT INTO Events"
                       "(pssgId, eventType, dateTime, latchType, "
                       "personId, side, allowed, notReason) "
                       "VALUES({}, {}, '{}', {}, {}, {}, {}, {})"
                       "".format(event['pssgId'], event['eventType'], 
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
        
        sqlSentence = ("SELECT id, pssgId, eventType, dateTime, latchType, "
                       "personId, side, allowed, notReason FROM Events "
                       "LIMIT {}".format(evtsQtty)
                      )

        self.cursor.execute(sqlSentence)
        evtTupleList = self.cursor.fetchall()



        while evtTupleList:


            evtDictList = []
            evtIdList = []
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



    def getPssgParamsNames(self):
        '''
        Getting Passage Params Names from SQL database
        '''

        sqlSentence = "SELECT * FROM Passage"
        self.cursor.execute(sqlSentence)
        self.connection.commit()

        return [i[0] for i in self.cursor.description]




    def getPssgsParams(self):
        '''
        Get the arguments of passages to call ioiface external program.
        pps = Passage Parametters

        '''

        ppsNames = self.getPssgParamsNames()

        
        sqlSentence = ("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {} "
                       "FROM Passage".format(*ppsNames)
                      )

        self.cursor.execute(sqlSentence)
        ppsTuplesList = self.cursor.fetchall()
        self.connection.commit()


        ppsDictsDict = {}

        for ppsTuple in ppsTuplesList:
            
            ppsDict = {}

            for i, ppName in enumerate(ppsNames):

                ppsDict[ppName] = ppsTuple[i]


                #self.logger.error('Invalid row in Passage table, skiping to the next row.')
            
            ppsDictsDict[ppsDict['id']] = ppsDict

        return ppsDictsDict

