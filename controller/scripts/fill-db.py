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




#######Filling Passage table########



cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(21, 20, null, null, 26, 19, 10, 22, 7, 3, 10)")
cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(16, 12, 7, 8, 13, 6, 27, 17, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(null, null, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(null, null, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, 5, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, null, 6, 7, 8, 7, 3, 10)")
#cursor.execute("insert into Passage(i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, rlseTime, bzzrTime, alrmTime) values(1, 2, 3, 4, null, 6, 7, 8, 7, 3, 10)")



#######Filling Access table#######

cursor.execute("SELECT id from Person")
allRows = cursor.fetchall()
personIds = [row[0] for row in allRows]

cursor.execute("SELECT id from Passage")
allRows = cursor.fetchall()
pssgIds = [row[0] for row in allRows]


#All persons will have access to all pssgs all week

pssgIdsPersonIds = []

for pssgId in pssgIds:
    for personId in personIds:
        
        pssgIdsPersonIds.append([pssgId, personId, 1])

#Shuffling the dictionary to be more real
random.shuffle(pssgIdsPersonIds)


#Now, some of the persons, in some of the pssgs,
#will not have access all week days
resPssgIdsPersonIds = []

for i in range(SIM_LIM_ACCESS_QUANT):

    elecPssgIdPersonId = random.choice(pssgIdsPersonIds)
    if elecPssgIdPersonId not in resPssgIdsPersonIds:
        elecPssgIdPersonId[2] = 0
        resPssgIdsPersonIds.append(elecPssgIdPersonId)




#Filling the SQL Access Table
for pssgIdPersonId in pssgIdsPersonIds:

    pssgId, personId, allWeek = pssgIdPersonId
        
    sqlSentence = ("INSERT INTO Access(pssgId, personId, allWeek, iSide, oSide, startTime, endTime, expireDate) "
                   "VALUES({}, {}, {}, 1, 1, '12:20', '23:30', '2016-12-30')".format(pssgId, personId, allWeek)
                  )

    cursor.execute(sqlSentence)


#Filling the SQL LimitedAccess Table generating entries for mon, tue, wed, thu, fry
for pssgIdPersonId in resPssgIdsPersonIds:

    pssgId, personId = pssgIdPersonId[:2]

    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 1, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 2, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 3, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 4, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 5, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 6, '12:20', '15:30')".format(pssgId, personId)
                  )
    cursor.execute(sqlSentence)


    sqlSentence = ("INSERT INTO LimitedAccess(pssgId, personId, iSide, oSide, weekDay, startTime, endTime) "
                   "VALUES({}, {}, 1, 1, 7, '12:20', '15:30')".format(pssgId, personId)
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
               "VALUES (1, 'Person opening a passage with card'), " 
                      "(2, 'Person opening a passage with button'), "
                      "(3, 'The passage remains opened')"
              )
cursor.execute(sqlSentence)




db.commit()
db.close()
