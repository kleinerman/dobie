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



doorIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)


if sys.argv[1]:

    doorIfaceData = sys.argv[1]
    doorIfaceQue.send(doorIfaceData)

else:


    while True:
        doorIfaceData = input('Enter simulated door iface data: ')
        doorIfaceQue.send(doorIfaceData)



