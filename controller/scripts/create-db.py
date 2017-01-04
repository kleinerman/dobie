#!/usr/bin/env python3

#from argparse import ArgumentParser
#import logging
#import logging.handlers
import sqlite3

from config import *

db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')



#----------------Person Table----------------#

cursor.execute('''
    CREATE TABLE Person (
        id          INTEGER PRIMARY KEY,
        cardNumber  INTEGER
    )
    '''
)

cursor.execute('''CREATE UNIQUE INDEX cardNumberIndex
                  ON Person (cardNumber)
               '''
)


#----------------Passage Table-----------------#


cursor.execute('''
    CREATE TABLE Passage (
        id       INTEGER PRIMARY KEY, 
        i0In     INTEGER, 
        i1In     INTEGER,
        o0In     INTEGER,
        o1In     INTEGER,
        bttnIn   INTEGER,
        stateIn  INTEGER,
        rlseOut  INTEGER,
        bzzrOut  INTEGER,
        rlseTime INTEGER,
        bzzrTime INTEGER,
        alrmTime INTEGER
    )
    '''
)


#----------------Access Table-----------------#

cursor.execute('''
    CREATE TABLE Access (
        id          INTEGER PRIMARY KEY,
        pssgId      INTEGER,
        personId    INTEGER,
        allWeek     BOOLEAN,
        iSide       BOOLEAN,
        oSide       BOOLEAN,
        startTime   DATETIME,
        endTime     DATETIME,
        expireDate  DATETIME,
        FOREIGN KEY(personId) REFERENCES Person(id) ON DELETE CASCADE,
        FOREIGN KEY(pssgId) REFERENCES Passage(id) ON DELETE CASCADE
    )
    '''
)

cursor.execute('''CREATE UNIQUE INDEX pssgPersonIndex
                  ON Access (pssgId, personId)
               '''
)


cursor.execute('''
    CREATE TABLE LimitedAccess (
        id         INTEGER PRIMARY KEY,
        pssgId     INTEGER,
        personId   INTEGER,
        weekDay    INTEGER, 
        iSide      BOOLEAN,
        oSide      BOOLEAN,
        startTime  DATETIME,
        endTime    DATETIME,
        FOREIGN KEY(personId) REFERENCES Person(id) ON DELETE CASCADE,
        FOREIGN KEY(pssgId) REFERENCES Passage(id) ON DELETE CASCADE
    )
    '''
)

cursor.execute('''CREATE UNIQUE INDEX pssgPersonWeekDayIndex
                  ON LimitedAccess (pssgId, personId, weekDay)
               '''
)




cursor.execute('''
    CREATE TABLE Events (
        id          INTEGER PRIMARY KEY,
        pssgId      INTEGER,
        eventType   INTEGER,
        dateTime    DATETIME,
        latchType   INTEGER,   
        personId    INTEGER,
        side        BOOLEAN,
        allowed     BOOLEAN,
        notReason   INTEGER,
        FOREIGN KEY(eventType) REFERENCES Event(id),
        FOREIGN KEY(latchType) REFERENCES Latch(id),
        FOREIGN KEY(notReason) REFERENCES NotReason(id)
   )
    '''
)


cursor.execute('''
    CREATE TABLE Event (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)



cursor.execute('''
    CREATE TABLE Latch (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)


cursor.execute('''
    CREATE TABLE NotReason (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)












db.commit()
db.close()
