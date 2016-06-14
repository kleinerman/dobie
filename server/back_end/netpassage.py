import logging

import socket
import json


from network import *
from config import *





class NetPassage(object):

    '''
    '''
    def __init__(self, netMngr):
        '''
        '''
        self.netMngr = netMngr



    def addPassage(self, ctrllerMac, passage):
        '''
        '''
        passageJson = json.dumps(passage).encode('utf8')

        msg = CUD + b'S' + b'C' + passageJson + END 
        
        self.netMngr.sendToCtrller(msg, ctrllerMac)




    def delPassage(self, ctrllerMac, passageId):
        '''
        '''
        passageId = str(passageId).encode('utf8')

        msg = CUD + b'S' + b'D' + b'{"id": ' + passageId + b'}' + END

        self.netMngr.sendToCtrller(msg, ctrllerMac)

