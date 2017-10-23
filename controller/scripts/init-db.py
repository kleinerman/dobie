#!/usr/bin/env python3

import sqlite3

from config import *



db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')


#Filling Event Table
sqlSentence = ("INSERT INTO DoorGpios(id, i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut) "
               "VALUES (1, 26, 21, 19, 20, 25, 24, 27, 14), "
                      "(2, 13, 16,  6, 12,  9, 23,  3, 15), "
                      "(3,  7,  5, 11,  8, 10, 22, 18, 17)"
              )
cursor.execute(sqlSentence)




#Creating a record for unknown person (for example when somebody press the button)
#cursor.execute("INSERT INTO Person(id, cardNumber) VALUES(1, 0)")



#Filling DenialCause Table
sqlSentence = ("INSERT INTO DenialCause(id, description) "
               "VALUES (1, 'No access'), (2, 'Expired card'), (3, 'Out of time')"
              )
cursor.execute(sqlSentence)



#Filling DoorLock Table
sqlSentence = ("INSERT INTO DoorLock(id, description) "
               "VALUES (1, 'Card reader'), (2, 'Fingerprint reader'), (3, 'Button')"
              )
cursor.execute(sqlSentence)


#Filling Event Table
sqlSentence = ("INSERT INTO EventType(id, description) "
               "VALUES (1, 'Person opening a door with card'), " 
                      "(2, 'Person opening a door with button'), "
                      "(3, 'The door remains opened'), "
                      "(4, 'The door was forced')"
              )
cursor.execute(sqlSentence)





db.commit()
db.close()
