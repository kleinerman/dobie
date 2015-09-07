import pymysql
import logging

from config import *



class DataBase(object):

    def __init__(self, host, user, passwd, dataBase):



        #Getting the logger
        self.logger = logging.getLogger(LOGGER_NAME)


        self.host = host
        self.user = user
        self.passwd = passwd
        self.dataBase = dataBase

        self.connection = pymysql.connect(host, user, passwd, dataBase)
        
        self.cursor = self.connection.cursor()




    def isValidCtrller(self, macAsInt):

        #Creating a separate connection since this method will be called from
        #different thread
        connection = pymysql.connect(self.host, self.user, self.passwd, self.dataBase)
        cursor = connection.cursor()

        macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(macAsHex)

        cursor.execute(sql)
        return cursor.fetchone()[0]





    def __del__(self):
   
        self.connection.commit() 
        self.connection.close()

