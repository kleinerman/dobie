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

        macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        print(macAsHex) 



    def __del__(self):
    
        self.connection.close()

