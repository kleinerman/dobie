#!/usr/bin/env python3

#from argparse import ArgumentParser
#import logging
#import logging.handlers
import random
import sqlite3

from config import *



db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')



#######Filling Person table#######

cardNumList = []

for i in range(SIM_PERSON_QUANT):
    #Generating a random card numbers between 0 and 2^24 (card has 24 bits)
    #candCardNum = '%08d' % random.randint(0, 16777216)
    candCardNum = random.randint(0, 16777216)
    #Avoiding store each card number more than once
    if candCardNum not in cardNumList:
        cardNumList.append(candCardNum)

#Storing random card numbers in database
for cardNum in cardNumList:
    cursor.execute("insert into Person(cardNumber) values('{}')".format(cardNum))




#######Filling Door table########



cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, null, null, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, null, null, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(null, null, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(null, null, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, 5, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, null, 6, 7, 8)")
cursor.execute("insert into Door(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) values(1, 2, 3, 4, null, 6, 7, 8)")



#######Filling Access table#######

cursor.execute("SELECT id from Person")
allRows = cursor.fetchall()
personIds = [row[0] for row in allRows]

cursor.execute("SELECT id from Door")
allRows = cursor.fetchall()
doorIds = [row[0] for row in allRows]


#All persons will have access to all doors all week

doorIdsPersonIds = []

for doorId in doorIds:
    for personId in personIds:
        
        doorIdsPersonIds.append([doorId, personId, 1])

#Shuffling the dictionary to be more real
random.shuffle(doorIdsPersonIds)


#Now, some of the persons, in some of the doors,
#will not have access all week days
resDoorIdsPersonIds = []

for i in range(SIM_LIM_ACCESS_QUANT):

    elecDoorIdPersonId = random.choice(doorIdsPersonIds)
    if elecDoorIdPersonId not in resDoorIdsPersonIds:
        elecDoorIdPersonId[2] = 0
        resDoorIdsPersonIds.append(elecDoorIdPersonId)




#Filling the SQL Access Table
for doorIdPersonId in doorIdsPersonIds:

    doorId, personId, allWeek = doorIdPersonId
        
    sqlSentence = ("INSERT INTO Access(doorId, personId, allWeek, iSide, oSide, startTime, endTime, expireDate) "
                   "VALUES({}, {}, {}, 1, 1, '12:20', '23:30', '2015-12-30')".format(doorId, personId, allWeek)
                  )

    cursor.execute(sqlSentence)


#Filling the SQL LimitedAccess Table generating entries for mon, tue, wed, thu, fry
for doorIdPersonId in resDoorIdsPersonIds:

    doorId, personId = doorIdPersonId[:2]

    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 1, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 2, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 3, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 4, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 5, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 6, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(doorId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 7, '12:20', '15:30')".format(doorId, personId)
                  )
    cursor.execute(sqlSentence)



#Filling NotReason Table
sqlSentence = ("INSERT INTO NotReason(id, description) "
               "VALUES (1, 'No access'), (2, 'Expired card'), (3, 'Out of time')"
              )
cursor.execute(sqlSentence)



#Filling Latch Table
sqlSentence = ("INSERT INTO Latch(id, description) "
               "VALUES (1, 'Card reader'), (2, 'Fingerprint reader'), (3, 'Button')"
              )
cursor.execute(sqlSentence)


#Filling Event Table
sqlSentence = ("INSERT INTO Event(id, description) "
               "VALUES (1, 'Person opening a door'), (2, 'Door remainded opened')"
              )
cursor.execute(sqlSentence)




db.commit()
db.close()
