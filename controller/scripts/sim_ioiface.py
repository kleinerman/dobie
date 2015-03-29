#!/usr/bin/env python3

#from argparse import ArgumentParser

import logging
import logging.handlers

import socket

import queue
import threading
import posix_ipc


from config import *



import sys



ioIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)


if sys.argv[1]:

    ioIfaceData = sys.argv[1]
    ioIfaceQue.send(ioIfaceData)

else:


    while True:
        ioIfaceData = input('Enter simulated pssg iface data: ')
        ioIfaceQue.send(ioIfaceData)



