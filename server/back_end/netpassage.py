import threading
import logging
import datetime
import time
import os

import select
import socket
import json

import database
import queue

import genmngr
from config import *


import sys



int_CON  = 0x01
int_RCON = 0x02
int_EVT  = 0x03
int_REVT = 0x04
int_EVS  = 0x05
int_REVS = 0x06
int_CUD  = 0x07
int_RCUD = 0x08
int_END  = 0x1F


CON  = bytes([int_CON])
RCON = bytes([int_RCON])
EVT  = bytes([int_EVT])
REVT = bytes([int_REVT])
EVS  = bytes([int_EVS])
REVS = bytes([int_REVS])
CUD  = bytes([int_CUD])
RCUD = bytes([int_RCUD])
END  = bytes([int_END])





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
        print(ctrllerMac, passage)
