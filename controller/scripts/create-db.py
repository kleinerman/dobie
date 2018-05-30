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


#----------------Door Table-----------------#


cursor.execute('''
    CREATE TABLE DoorGpios (
        id       INTEGER PRIMARY KEY,
        i0In     INTEGER, 
        i1In     INTEGER,
        o0In     INTEGER,
        o1In     INTEGER,
        bttnIn   INTEGER,
        stateIn  INTEGER,
        rlseOut  INTEGER,
        bzzrOut  INTEGER
    )
    '''
)



cursor.execute('''
    CREATE TABLE Door (
        id        INTEGER PRIMARY KEY,
        doorNum   INTEGER,
        snsrType  BOOLEAN,
        rlseTime  INTEGER,
        bzzrTime  INTEGER,
        alrmTime  INTEGER,
        FOREIGN KEY(doorNum) REFERENCES DoorGpios(id) ON DELETE CASCADE
    )
    '''
)

cursor.execute('''CREATE UNIQUE INDEX doorNumIndex
                  ON Door (doorNum)
               '''
)



#----------------Access Table-----------------#

cursor.execute('''
    CREATE TABLE Access (
        id          INTEGER PRIMARY KEY,
        doorId      INTEGER,
        personId    INTEGER,
        allWeek     BOOLEAN,
        iSide       BOOLEAN,
        oSide       BOOLEAN,
        startTime   DATETIME,
        endTime     DATETIME,
        expireDate  DATETIME,
        FOREIGN KEY(personId) REFERENCES Person(id) ON DELETE CASCADE,
        FOREIGN KEY(doorId) REFERENCES Door(id) ON DELETE CASCADE
    )
    '''
)

#FOREIGN KEY(doorId) REFERENCES Door(id) ON DELETE CASCADE

cursor.execute('''CREATE UNIQUE INDEX doorPersonIndex
                  ON Access (doorId, personId)
               '''
)


cursor.execute('''
    CREATE TABLE LimitedAccess (
        id         INTEGER PRIMARY KEY,
        doorId     INTEGER,
        personId   INTEGER,
        weekDay    INTEGER, 
        iSide      BOOLEAN,
        oSide      BOOLEAN,
        startTime  DATETIME,
        endTime    DATETIME,
        FOREIGN KEY(personId) REFERENCES Person(id) ON DELETE CASCADE,
        FOREIGN KEY(doorId) REFERENCES Door(id) ON DELETE CASCADE
    )
    '''
)

cursor.execute('''CREATE UNIQUE INDEX doorPersonWeekDayIndex
                  ON LimitedAccess (doorId, personId, weekDay)
               '''
)




cursor.execute('''
    CREATE TABLE Event (
        id          INTEGER PRIMARY KEY,
        doorId      INTEGER,
        eventTypeId INTEGER,
        dateTime    DATETIME,
        doorLockId  INTEGER,   
        personId    INTEGER,
        side        BOOLEAN,
        allowed     BOOLEAN,
        denialCauseId INTEGER,
        FOREIGN KEY(doorId) REFERENCES Door(id) ON DELETE CASCADE,
        FOREIGN KEY(eventTypeId) REFERENCES EventType(id),
        FOREIGN KEY(doorLockId) REFERENCES DoorLock(id),
        FOREIGN KEY(personId) REFERENCES Person(id) ON DELETE CASCADE,
        FOREIGN KEY(denialCauseId) REFERENCES DenialCause(id)
   )
    '''
)


cursor.execute('''
    CREATE TABLE EventType (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)



cursor.execute('''
    CREATE TABLE DoorLock (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)


cursor.execute('''
    CREATE TABLE DenialCause (
        id          INTEGER PRIMARY KEY,
        description TEXT

    )
    '''
)












db.commit()
db.close()
