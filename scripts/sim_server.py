#!/usr/bin/env python3

#from argparse import ArgumentParser

import logging
import logging.handlers

import socket
import signal
import sys
import json

import queue
import threading

from config_sim_srv import *


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








#def sigtermHandler(signal, frame):
#
#    logger.info('Getting SIGTERM. Closing socket server...')
#
#    #Closing the socket will raise "InterruptedError" in accept method
#    #of serverSocket
#    serverSocket.close()
#
#
#    def finishHandler(self, sigNum, frame):
#        signal.signal(signal.SIGINT, self.origSigIntHandler)
#        self.logger.debug('Notifying all threads to finish.')
#        self.exitFlag.set()
#        os.kill(os.getpid(),signal.SIGINT)




############# Here starts the Main Thread ############

#Registering "sigtermHandler" handler to act when receiving the SIGTERM signal
#signal.signal(signal.SIGTERM, sigtermHandler)
#signal.signal(signal.SIGINT, sigtermHandler)


#Defining log structures with the possibility of rotation by logrotate
loggingHandler = logging.handlers.WatchedFileHandler(LOGGING_FILE)
loggingFormatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s: %(message)s', '[%d %H:%M:%S]')
loggingHandler.setFormatter(loggingFormatter)

logger = logging.getLogger('simserver')
logger.setLevel(loggingLevel)
logger.addHandler(loggingHandler)

logger.info('Starting the Main Process.')

#Creating the socket server to receive device connections
#serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#serverSocket.bind((BIND_IP, BIND_PORT))
#serverSocket.listen(SIM_DEV_CONNECTIONS)



##-----------------------------------------------------------------------##




try:

    while True:

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((BIND_IP, BIND_PORT))
        serverSocket.listen(SIM_DEV_CONNECTIONS)

        logger.info('Waiting for device connections...')
        devSocket, devAddress = serverSocket.accept()
        logger.info('Receiving message from controller with the following IP and Port: {}'.format(devAddress))


        while True:

            try:
                receivedBytes = devSocket.recv(SOCK_BUF_LEN)
                if not receivedBytes:
                    print('Connection broken!')
                    devSocket.close()
                    break
                
                print('Receiving: {}'.format(receivedBytes))
        
                if receivedBytes.startswith(EVT):
                    response = REVT + b'OK' + END
                    print('Sending: {}'.format(response))
                    devSocket.sendall(response)

                elif receivedBytes.startswith(EVS):
                    response = REVS + b'OK' + END
                    print('Sending: {}'.format(response))
                    devSocket.sendall(response)

                elif receivedBytes.startswith(CON):
                    response = RCON + b'OK' + END
                    print('Sending: {}'.format(response))
                    devSocket.sendall(response)

                    #crudDict = {'id': 7, 'doorId': 1, 'weekDay': 7, 'startTime': '12:03', 'endTime': '19:17'}
                    #crudDict = {'id': 7}
                    crudDict = {'id': 7, 'doorId': 1, 'excDay': '2020-01-09'}

                    crudDict = json.dumps(crudDict).encode('utf8')
                    msg = CUD + b'E' + b'U' + crudDict + END
                    print('Sending: {}'.format(msg))
                    devSocket.sendall(msg)


            
            except(InterruptedError):
                print('Connection closed!')
                break
        


except(InterruptedError, KeyboardInterrupt):

    logger.info('Finisihing.')
    sys.exit(0) 




