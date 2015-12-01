#!/usr/bin/env python


import pymysql

from config import *

connection = pymysql.connect(HOST, USER, PASSWD, DB)
cursor = connection.cursor()


#sqlSentence = 'SELEC'

#cursor.execute(sqlSentence)
connection.close()

