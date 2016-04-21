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





class CtrllerDisconnected(Exception):
    pass


class TimeOutConnectionMsg(Exception):
    pass


class UnknownController(Exception):
    pass






class Unblocker(object):
    '''
    This class declares a pipe in its constructor.
    It stores read and write file descriptor as attributes.
    -The getFd method returns the read file descriptor which is registered to be monitored 
    by poll().
    -The unblock method write a dummy byte (0) to generate a event to wake up the poll()
    -The receive method reads this dummy byte because if it is not read, the next call
    to poll(), will wake up again(). We are reading more than one byte (ten bytes), 
    for the case of two consecutives calls generates two wake ups. (Not sure if it has sense)
    '''
    
    def __init__(self):
        self.readPipe, self.writePipe = os.pipe()

    def getFd(self):
        return self.readPipe

    def unblock(self):
        os.write(self.writePipe, b'0')

    def receive(self):
        os.read(self.readPipe, 10)

    



class NetMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''
    def __init__(self, dbMngr, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('NetMngr', exitFlag)

        #Queue used to send Events and CRUD confirmation to dbMngr
        self.dbMngr = dbMngr
        #self.netToDb = netToDb

        #Poll Network Object to monitor the sockets
        self.netPoller = select.poll()

        #Lock to protect access to "netPoller" 
        self.lockNetPoller = threading.Lock()

        #Unblocker object to wake up the thread blocked in poll() call
        self.unblocker = Unblocker()
        self.unBlkrFd = self.unblocker.getFd()

        #Registering above pipe in netPoller object
        self.netPoller.register(self.unBlkrFd)

        #Creating the socket listener
        self.listenerSckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenerSckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listenerSckt.bind((BIND_IP, BIND_PORT))
        self.listenerSckt.listen(SIM_CONNECTIONS)
        #Saving the listener socket file descriptor
        self.listenerScktFd = self.listenerSckt.fileno()

        #Registering socket listener in netPoller object
        self.netPoller.register(self.listenerSckt, select.POLLIN)

        #Dictionary indexed by socket controller file descriptors. Each element
        #of this dictionary is another dictionary with the controller socket and
        #buffers to send and receive messages
        self.fdConnObjects = {}

        #Dictionary to get the socket file descriptor with the MAC address
        self.macConnObjects = {}
        
 


    #---------------------------------------------------------------------------#

    def procRecMsg(self, fd, msg):
        '''
        This method is called by the main "run()" method when it receives bytes
        from the server. This happens in POLLIN evnts branch.
        It process the message and delivers it to the corresponding thread 
        according to the headers of the message.
        '''
        #This is a response to an event sent to the server
        #It should be delivered to "eventMngr" thread.
        if msg.startswith(EVT):
            response = REVT + b'OK' + END

            event = msg.strip(EVT+END).decode('utf8')
            event = json.loads(event)
            events = [event]
            self.dbMngr.putEvents(events)



        elif msg.startswith(EVS):
            response = REVS + b'OK' + END

            events = msg[1:-1].split(EVS)
            events = [json.loads(evnt.decode('utf8')) for evnt in events]
            self.dbMngr.putEvents(events)
            

            
        self.fdConnObjects[fd]['outBufferQue'].put(response)
        ctrllerSckt = self.fdConnObjects[fd]['socket']
        with self.lockNetPoller:
            self.netPoller.modify(ctrllerSckt, select.POLLOUT)




    #---------------------------------------------------------------------------#






    def recvConMsg(self, ctrllerSckt, timeToWait):
        '''
        This method receive the response to Connection Message.
        It waits until all response comes since it could come fragmented.
        It only waits "timeToWait", after that it throws a "TimeOutConnectionMsg"
        exception.
        If during the reception, b'' is received, meaning that the controller
        was disconnected, a "CtrllerDisconnected" exception will be thrown.
        When the END byte is received we can return the content of the message
        
        '''
        #if not ctrllerSckt:
        #    raise ControllerNotConnected

        ctrllerSckt.settimeout(timeToWait)

        completeMsg = b''
        completed = False
        while not completed:

            try:
                msg = ctrllerSckt.recv(REC_BYTES)
                if not msg:
                    raise CtrllerDisconnected
                self.logger.debug('The controller send {} as CON message'.format(msg))
                self.checkExit()
            except socket.timeout:
                raise TimeOutConnectionMsg

            completeMsg += msg
            if completeMsg.endswith(END):
                completed = True

        msgContent = completeMsg.strip(CON+END).decode('utf8')

        return msgContent



    def sendRespConMsg(self, ctrllerSckt, ctrllerMac):
        '''
        This method responds to controller "CON" message with "OK" or "NO".
        To take this decision it verifies the MAC address sent by the controller
        against the Data Base.
        When the controller is not registered in Data Base an "UnknownController"
        exception is thrown
        '''

        if self.dbMngr.isValidCtrller(ctrllerMac):
            ctrllerSckt.sendall(RCON + b'OK' + END)
        else:
            ctrllerSckt.sendall(RCON + b'NO' + END)
            raise UnknownController










    def run(self):
        '''
        This is the main method of the thread.
        When the controller is connected to the server, this method is blocked most of
        the time in "poll()" method waiting for bytes to go out or incoming bytes from 
        the server or  a event produced when the socket is broken or disconnect.
        When there is no connection to the server, this method tries to reconnect to 
        the server every "RECONNECT_TIME"
        '''

        while True:

            for fd, pollEvnt in self.netPoller.poll(NET_POLL_MSEC):

                #This will happen when the "event" thread or "reSender"
                #thread puts bytes in the "outBufferQue" and they want to notify
                #this thread to wake up from "poll()"
                if fd == self.unBlkrFd:
                    self.unblocker.receive()
                    continue


                if fd == self.listenerScktFd:
                    ctrllerSckt, address = self.listenerSckt.accept()

                    try:
                        ctrllerMac = self.recvConMsg(ctrllerSckt, WAIT_RESP_TIME)
                        self.sendRespConMsg(ctrllerSckt, ctrllerMac)

                        self.logger.info('Accepting connection from: {}'.format(address))
                        ctrllerScktFd = ctrllerSckt.fileno()


                        connObjects = {'socket': ctrllerSckt,
                                       'inBuffer': b'',
                                       'outBufferQue': queue.Queue()
                                       #'connected': threading.Event()
                                      }

                        self.fdConnObjects[ctrllerScktFd] = connObjects

                        self.macConnObjects[ctrllerMac] = connObjects
    
                        self.netPoller.register(ctrllerSckt, select.POLLIN)



                    except CtrllerDisconnected:
                        self.logger.warning('The controller at: {} disconnected'.format(address))
                        ctrllerSckt.close()

                    except TimeOutConnectionMsg:
                        self.logger.warning('The controller does not complete CON message.')
                        ctrllerSckt.close()

                    except UnknownController:
                        self.logger.warning('Unknown controller trying to connect.')
                        ctrllerSckt.close()




                #This will happen when the server sends to us bytes.
                elif pollEvnt & select.POLLIN:
                    ctrllerSckt = self.fdConnObjects[fd]['socket']
                    recBytes = ctrllerSckt.recv(REC_BYTES)
                    self.logger.debug('Receiving: {}'.format(recBytes))

                    #Receiving b'' means the controller closed the connection
                    #On this situation we should close the socket and the
                    #next call to "poll()" will throw a POLLNVAL event
                    if not recBytes:
                        ctrllerSckt.close()
                        continue

                    #We should receive bytes until we receive the end of
                    #the message
                    msg = self.fdConnObjects[fd]['inBuffer'] + recBytes
                    if msg.endswith(END):
                        self.procRecMsg(fd, msg)
                    else:
                        self.fdConnObjects[fd]['inBuffer'] = msg


                #This will happen when "event" thread or "reSender" thread
                #puts bytes in "outBufferQue", modifying the "netPoller"
                #to send bytes.
                elif pollEvnt & select.POLLOUT:
                    try:
                        #We can have more than one message in the "outBufferQue"
                        #to send, because we can have more than one call to
                        #"sendEvent()" or "reSendEvents()" before the POLLOUT event
                        #happens. For this reason we should empty the "outBufferQue"
                        #sending all the messages. Then, if we have another POLLOUT
                        #event and the queue is empty, nothing will happen.
                        ctrllerSckt = self.fdConnObjects[fd]['socket']
                        while True:
                            outBuffer = self.fdConnObjects[fd]['outBufferQue'].get(block = False)
                            self.logger.debug('Sending: {}'.format(outBuffer))
                            ctrllerSckt.sendall(outBuffer)
                    except queue.Empty:
                        #No more messages to send in "outBufferQue"
                        pass
                    #Once we finished sending all the messages, we should modify the
                    #"netPoller" object to be able to receive bytes again.
                    with self.lockNetPoller:
                        self.netPoller.modify(ctrllerSckt, select.POLLIN)


                #This will happen when the server closes the socket or the 
                #connection with the server is broken
                elif pollEvnt & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
                    print('planvll')
                    self.logger.info('The connection with server was broken.')
                    with self.lockNetPoller:
                        #Unregistering the socket from the "netPoller" object
                        self.netPoller.unregister(fd)
                        connObject = self.fdConnObjects.pop(fd)

                    for mac in self.macConnObjects:
                        if connObject == self.macConnObjects[mac]:
                            break
                    self.macConnObjects.pop(mac)

            #print('MAC-->',self.macConnObjects)
            #print('FD-->',self.fdConnObjects)
                    

            #Cheking if Main thread ask as to finish.
            self.checkExit()



    
