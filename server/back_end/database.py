import pymysql
import queue
import logging


from config import *



class DbMngr(object):

    def __init__(self, host, user, passwd, dataBase):



        #Getting the logger
        self.logger = logging.getLogger(LOGGER_NAME)


        self.host = host
        self.user = user
        self.passwd = passwd
        self.dataBase = dataBase
    
        self.netToDb = queue.Queue()


        self.connection = pymysql.connect(host, user, passwd, dataBase)
        
        self.cursor = self.connection.cursor()




    def isValidCtrller(self, ctrllerMac):

        #Creating a separate connection since this method will be called from
        #different thread
        connection = pymysql.connect(self.host, self.user, self.passwd, self.dataBase)
        cursor = connection.cursor()

        #macAsHex = '{0:0{1}x}'.format(macAsInt, 12)
        sql = "SELECT COUNT(*) FROM Controller WHERE macAddress = '{}'".format(ctrllerMac)

        cursor.execute(sql)
        return cursor.fetchone()[0]




    def saveEvent(self, event):
        print(event)



    #def __del__(self):
   
        #self.connection.commit() 
        #self.connection.close()

