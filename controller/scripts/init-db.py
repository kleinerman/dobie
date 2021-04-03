#!/usr/bin/env python3

import sqlite3

from config import *



db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')


#Filling Event Table
sqlSentence = (f'INSERT INTO HwDoorParms(id, iWgndBits, i0In, i1In, oWgndBits, o0In, o1In, bttnIn, stateIn, unlkOut, bzzrOut) '
               f'VALUES (1, {IR_WGND_BITS[0]}, 26, 21, {OR_WGND_BITS[0]}, 19, 20, 25, 24, 27, 14), '
                      f'(2, {IR_WGND_BITS[1]}, 13, 16, {OR_WGND_BITS[1]}, 6, 12,  9, 23,  3, 15), '
                      f'(3, {IR_WGND_BITS[2]}, 7, 5, {OR_WGND_BITS[2]}, 11,  8, 10, 22, 18, 17)'
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
                      "(3, 'Door remains opened'), "
                      "(4, 'Door was forced'), "
                      "(5, 'Door opened by schedule'), "
                      "(6, 'Door closed by schedule'), "
                      "(7, 'Door opened while unlocked by schedule'), "
                      "(8, 'Door opened by user interface')"
              )
cursor.execute(sqlSentence)





db.commit()
db.close()
