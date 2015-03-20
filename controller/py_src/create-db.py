#!/usr/bin/env python3

#from argparse import ArgumentParser
#import logging
#import logging.handlers
import sqlite3


db = sqlite3.connect('access.db')
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
    CREATE TABLE Door (
        id       INTEGER PRIMARY KEY, 
        i0In     INTEGER, 
        i1In     INTEGER,
        o0In     INTEGER,
        o1In     INTEGER,
        btnIn    INTEGER,
        stateIn  INTEGER,
        rlseOut  INTEGER,
        bzzrOut  INTEGER
    )
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
        FOREIGN KEY(personId) REFERENCES Person(id),
        FOREIGN KEY(doorId) REFERENCES Door(id)
    )
    '''
)


cursor.execute('''CREATE UNIQUE INDEX doorPersonIndex
                  ON Access (doorId, personId)
               '''
)


cursor.execute('''
    CREATE TABLE LimitedAccess (
        id         INTEGER PRIMARY KEY,
        doorId     INTEGER,
        personId   INTEGER,
        iSide      BOOLEAN,
        oSide      BOOLEAN,
        weekDay    INTEGER,
        startTime  DATETIME,
        endTime    DATETIME
    )
    '''
)


cursor.execute('''
    CREATE TABLE Events (
        id          INTEGER PRIMARY KEY,
        doorId      INTEGER,
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
