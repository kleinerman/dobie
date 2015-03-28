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



pssgIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)


if sys.argv[1]:

    pssgIfaceData = sys.argv[1]
    pssgIfaceQue.send(pssgIfaceData)

else:


    while True:
        pssgIfaceData = input('Enter simulated pssg iface data: ')
        pssgIfaceQue.send(pssgIfaceData)



