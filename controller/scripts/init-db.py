#!/usr/bin/env python3

import sqlite3

from config import *



db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')


#Filling Event Table
sqlSentence = ("INSERT INTO PssgPinout(id, i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) "
               "VALUES (1, 21, 20, 16, 12, 26, 19,  9,  3), "
                      "(2,  7,  8, 25, 24, 13,  6, 10, 17), "
                      "(3, 23, 18, 15, 14,  5, 11, 22, 27)"
              )
cursor.execute(sqlSentence)




#Creating a record for unknown person (for example when somebody press the button)
cursor.execute("INSERT INTO Person(id, cardNumber) VALUES(1, 0)")



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
