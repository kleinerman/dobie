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

from config import *

import sys





int_EVT  = 0x01
int_REVT = 0x02
int_EVS  = 0x03
int_REVS = 0x04
int_CUD  = 0x05
int_RCUD = 0x06
int_END  = 0x1F


EVT  = bytes([int_EVT])
REVT = bytes([int_REVT])
EVS  = bytes([int_EVS])
REVS = bytes([int_REVS])
CUD  = bytes([int_CUD])
RCUD = bytes([int_RCUD])
END  = bytes([int_END])


#EVT  = b'#'
#REVT = b'$'
#CUD  = b'%'
#RCUD = b'&'
#END  = b'.\n'


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

    



class NetMngr(threading.Thread):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''
    def __init__(self, netToEvent, netToReSnd, exitFlag):


        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__(name = 'NetMngr', daemon = True)

        #Buffer to receive bytes from server
        self.inBuffer = b''
        #Buffer to send bytes to server
        self.outBuffer = b''


        #Queue to send responses to Event Thread
        self.netToEvent = netToEvent

        #Queue to send responses to ReSender Thread
        self.netToReSnd = netToReSnd


        #Queue used to send events from event thread to network thread
        self.outBufferQue = queue.Queue()

        #Lock to protect access to above dictionary 
        self.lockNetPoller = threading.Lock()

        #Poll Network Object
        self.netPoller = select.poll()

        #Pipe to wake up the thread blocked in poll() call
        #self.readPipe, self.writePipe = os.pipe()

        self.unblocker = Unblocker()
        self.unBlkrFd = self.unblocker.getFd()

        #Registering above pipe in netPoller object
        self.netPoller.register(self.unBlkrFd)

        #Socket server
        self.srvSock = None
 
        #Flag to know when the Main thread ask as to finish
        self.exitFlag = exitFlag

        #Thread exit code
        self.exitCode = 0

        #Getting the logger
        self.logger = logging.getLogger('Controller')


        #This is a flag to know when we are connected to server.
        #it is needed a Event, because multiple threads can check it
        #The flag is initially False.
        self.connected = threading.Event()



    #---------------------------------------------------------------------------#

    def checkExit(self):
        '''
        Check if the main thread ask this thread to exit using exitFlag
        If true, call sys.exit and finish this thread
        '''
        if self.exitFlag.is_set():
            self.logger.info('Network thread exiting.')
            sys.exit(self.exitCode) 



    #---------------------------------------------------------------------------#

    def sendEvent(self, event):
        '''
        This method is called by the "eventMngr" thread each time it receives 
        an event from the "main" thread.
        It receives a dictionary as an event which is converted to a JSON bytes
        to create the event message to send to the server.
        The sequence of bytes is stored in a queue, the "netPoller" is modified
        to tell the "netMngr" there is bytes to send and the "netMngr" thread is
        unblocked from the "poll()" method using the "unblocker" object. 
        Once this happens, the "netMngr" thread pulls the message from queue and 
        send them to the server.       
        '''

        if self.connected.is_set():

            #Converting dictionary to JSON bytes
            jsonEvent = json.dumps(event).encode('utf8')
            #Adding headers at beggining and end
            outMsg = EVT + jsonEvent + END

            #Writing the messages in a queue because we can not assure the method
            #"sendEvent()" will not be called again before the "poll()" method wakes
            #up to send the bytes. If we do not do this, we would end up with a mess
            #of bytes in the out buffer.
            #(Not sure if this is necessary or it is the best way to do it)
            self.outBufferQue.put(outMsg)

            with self.lockNetPoller:
                try:
                    #Modifying "netPoller" to notify there is a message to send.
                    self.netPoller.modify(self.srvSock, select.POLLOUT)
                    #Unblocking the "netMngr" thread from the "poll()" method.
                    self.unblocker.unblock()
                except FileNotFoundError:
                    #This exception could happen if it is received a null byte (b'')
                    #in POLLIN evnt, the socket is closed and "eventMngr" calls this
                    #method before POLLNVAL evnt happens to clean "self.connected".
                    #(Not sure if this can occur)                    
                    self.logger.debug('The socket was closed and POLLNVALL was not captured yet.')
            
        else:
            self.logger.debug('Can not send event, server is disconnected.')



    #---------------------------------------------------------------------------#

    def reSendEvents(self, eventList):
        '''
        This method is called by the "reSender" thread.
        It receives a list of dictionaries as an events. Each event is converted
        to a JSON bytes delimitted by headers to create the events message to send
        to the server.
        The sequence of bytes is stored in a queue, the "netPoller" is modified
        to tell the "netMngr" there is bytes to send and the "netMngr" thread is
        unblocked from the "poll()" method using the "unblocker" object. 
        Once this happens, the "netMngr" thread pulls the message from queue and 
        send them to the server.
        See the comments in "SendEvent" message. 
        '''

        if self.connected.is_set():

            outMsg = b''
            for event in eventList:
                jsonEvent = json.dumps(event).encode('utf8')
                outMsg += EVS + jsonEvent
            outMsg += END

            self.outBufferQue.put(outMsg)
            with self.lockNetPoller:
                try:
                    self.netPoller.modify(self.srvSock, select.POLLOUT)
                    self.unblocker.unblock()
                except FileNotFoundError:
                    self.logger.debug('The socket was closed and POLLNVALL was not captured yet.')

        else:
            self.logger.debug('Can not re-send event, server is disconnected.')



    #---------------------------------------------------------------------------#

    def procRecMsg(self, msg):
        '''
        This method is called by the main "run()" method when it receives bytes
        from the server. This happens in POLLIN evnts branch.
        It process the message and delivers it to the corresponding thread 
        according to the headers of the message.
        '''

        #This is a response to an event sent to the server
        #It should be delivered to "eventMngr" thread.
        if msg.startswith(REVT):
            response = msg.strip(REVT+END)
            response = response.decode('utf8')
            self.netToEvent.put(response)

        #This is a response to a set of re-sent events sent to the server
        #It should be delivered to "reSender" thread.
        elif msg.startswith(REVS):
            response = msg.strip(REVS+END)
            response = response.decode('utf8')
            self.netToReSnd.put(response)
        


    #---------------------------------------------------------------------------#

    def run(self):
        '''
        This is the main method of the thread. Most of the time it is blocked waiting 
        for queue messages coming from the "Main" thread.
        '''

        while True:

            try:
                #Connecting to server
                self.srvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.srvSock.connect((SERVER_IP, SERVER_PORT))
                #Registering the socket in the network poller object
                self.netPoller.register(self.srvSock, select.POLLIN)
                self.connected.set()
                self.logger.info('Connected to server. IP: {}, PORT: {}'.format(SERVER_IP, SERVER_PORT))

                while self.connected.is_set():

                    for fd, pollEvnt in self.netPoller.poll(NET_POLL_MSEC):


                        if fd == self.unBlkrFd:
                            self.unblocker.receive()
                            continue

                        if pollEvnt & select.POLLIN:
                            moreData = self.srvSock.recv(REC_BYTES)
                            self.logger.debug('Receiving: {}'.format(moreData))
                            if not moreData:         # end-of-file
                                self.srvSock.close() # next poll() will POLLNVAL, and thus clean up
                                continue                # Continue to the next pollEvnt if any
                            msg = self.inBuffer + moreData
                            if msg.endswith(END):
                                self.procRecMsg(msg)
                            else:
                                self.inBuffer = msg



                        elif pollEvnt & select.POLLOUT:
                            try:
                                while True:
                                    outBuffer = self.outBufferQue.get(block = False)
                                    self.logger.debug('Sending: {}'.format(outBuffer))
                                    self.srvSock.sendall(outBuffer)
                            except queue.Empty:
                                pass #No more data to send in queue
                            #No se bien por que tengo que hacer esto pero sino lo hago
                            #la proxima llamada a netPoller.poll se bloquea por siempre
                            with self.lockNetPoller:
                                self.netPoller.modify(self.srvSock, select.POLLIN)



                        elif pollEvnt & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
                            self.logger.info('The connection with server was broken.')
                            with self.lockNetPoller:
                                self.netPoller.unregister(fd)
                                #self.netPoller = None
                            #self.srvSock = None
                            self.connected.clear()

                    #Cheking if Main thread ask as to finish.
                    self.checkExit()


            except (ConnectionRefusedError, ConnectionResetError):
                #Cheking if Main thread ask as to finish.
                self.checkExit()
                self.logger.info('Reconnecting to server in {} seconds..'.format(RECONNECT_TIME))
                time.sleep(RECONNECT_TIME)

    
