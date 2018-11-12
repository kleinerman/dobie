import threading
import logging
import datetime
import time
import os
import subprocess
import re

import select
import socket
import json

import database
import queue

import sys
import netifaces

import genmngr
from config import *
from msgheaders import *




class ServerNotConnected(Exception):
    pass


class InvalidConnectionResponse(Exception):
    pass


class TimeOutConnectionResponse(Exception):
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
    def __init__(self, netToEvent, netToReSnd, crudMngr, exitFlag):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('NetMngr', exitFlag)

        #Buffer to receive bytes from server
        #It is used in POLLIN event
        self.inBuffer = b''

        #Buffer to send bytes to server
        #It is used in POLLOUT event
        self.outBuffer = b''

        #CRUD Manager to send the CRUD commands received from server
        self.crudMngr = crudMngr

        #Queue to send responses to Event Thread
        self.netToEvent = netToEvent

        #Queue to send responses to ReSender Thread
        self.netToReSnd = netToReSnd

        #In this queue, "event" and "reSender" threads put the messages
        #and "netMngr" gets them to send to the server.
        #We are using a queue because we can not assure the method
        #"sendEvent()" will not be called again before the "poll()" method wakes
        #up to send the bytes. If we do not do this, we would end up with a mess
        #of bytes in the out buffer.
        #(Not sure if this is necessary or it is the best way to do it)
        self.outBufferQue = queue.Queue()

        #Poll Network Object to monitor the sockets
        self.netPoller = select.poll()

        #Lock to protect access to "netPoller" 
        self.lockNetPoller = threading.Lock()

        #Unblocker object to wake up the thread blocked in poll() call
        self.unblocker = Unblocker()
        self.unBlkrFd = self.unblocker.getFd()

        #Registering above pipe in netPoller object
        self.netPoller.register(self.unBlkrFd)

        #Socket server
        self.srvSock = None
 
        #This is a flag to know when we are connected to server.
        #it is needed an threading.event object because "netMngr",
        #"event" and "reSender" threads can access to it simultaneously
        self.connected = threading.Event()

        #Database connection should be created in run method
        #It is only used to clear the database when receiving
        #RRP message.
        self.dataBase = None

        #Calculating the number of iterations before sending Keep 
        #Alive message to server
        self.ITERATIONS = KEEP_ALIVE_TIME * 1000 // NET_POLL_MSEC

        #This is the actual iteration. This value is incremented in 
        #each iteration and is initializated to 0.
        self.iteration = 0




    def sendToServer(self, msg):
        '''
        The sequence of bytes is stored in a queue, the "netPoller" is modified
        to tell the "netMngr" there is bytes to send and the "netMngr" thread is
        unblocked from the "poll()" method using the "unblocker" object. 
        Once this happens, the "netMngr" thread pulls the message from queue and 
        send them to the server.
        '''

        if self.connected.is_set():


            #Writing the messages in a queue because we can not assure the method
            #"sendEvent()" will not be called again before the "poll()" method wakes
            #up to send the bytes. If we do not do this, we would end up with a mess
            #of bytes in the out buffer.
            #(Not sure if this is necessary or it is the best way to do it)
            self.outBufferQue.put(msg)

            with self.lockNetPoller:
                try:
                    #Modifying "netPoller" to notify there is a message to send.
                    self.netPoller.modify(self.srvSock, select.POLLOUT)
                    #Unblocking the "netMngr" thread from the "poll()" method.
                    self.unblocker.unblock()
                except (FileNotFoundError, ValueError) as sendError:
                    #FileNotFoundError:
                    #This exception could happen if it is received a null byte (b'')
                    #in POLLIN evnt, the socket is closed and "eventMngr" calls this
                    #method before POLLNVAL evnt happens to clean "self.connected".
                    #(Not sure if this can occur)
                    #ValueError:
                    #This exception happened after to much time without sending nothing
                    #between server and controller. On this situation, when trying to 
                    #call self.netPoller.modify(), file descriptor cannot be a negative 
                    #integer will be the error.
                    self.logger.debug('The socket was closed and POLLNVALL was not captured yet.')
                    #When any of above exception happen, the outBufferQue should be cleaned.
                    self.outBufferQue.queue.clear()

        else:
            self.logger.debug('Can not send message, server is disconnected.')




    #---------------------------------------------------------------------------#

    def sendEvent(self, event):
        '''
        This method is called by the "eventMngr" thread each time it receives 
        an event from the "main" thread.
        It receives a dictionary as an event which is converted to a JSON bytes
        to create the event message to send to the server using "sendToServer()" 
        method.
        '''


        #Converting dictionary to JSON bytes
        jsonEvent = json.dumps(event).encode('utf8')
        #Adding headers at beggining and end
        msg = EVT + jsonEvent + END
        #Sending to the server.
        self.sendToServer(msg)


    #---------------------------------------------------------------------------#

    def reSendEvents(self, eventList):
        '''
        This method is called by the "reSender" thread.
        It receives a list of dictionaries as an events. Each event is converted
        to a JSON bytes delimitted by headers to create the events message to send
        to the server using "sendToServer()" method.
        '''

        msg = b''
        for event in eventList:
            jsonEvent = json.dumps(event).encode('utf8')
            msg += EVS + jsonEvent
        msg += END
        
        self.sendToServer(msg)


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
            srvResponse = msg.strip(REVT+END)
            srvResponse = srvResponse.decode('utf8')
            self.netToEvent.put(srvResponse)

        #This is a response to a set of re-sent events sent to the server
        #It should be delivered to "reSender" thread.
        elif msg.startswith(REVS):
            srvResponse = msg.strip(REVS+END)
            srvResponse = srvResponse.decode('utf8')
            self.netToReSnd.put(srvResponse)

        #This will happen when the server send to controller a CRUD message
        elif msg.startswith(CUD):
            crudMsg = msg.strip(CUD+END).decode('utf8')
            self.crudMngr.netToCrud.put(crudMsg)

        elif msg.startswith(RRP):
            self.crudMngr.netToCrud.put(RRP)

        elif msg.startswith(RRC):
            self.sendToServer(RRRE + END)

        elif msg.startswith(RPO):
            subprocess.Popen([POWEROFF_BIN])



    def sendConMsg(self):
        '''
        This method send the inital connection message to the server.
        This message has the wired iface mac address of the controller.
        This is the way the server recognize the controller as valid controller
        Also when connecting using wifi iface, the wired iface mac is sent.
        '''

        if not self.srvSock:
            raise ServerNotConnected

        #Getting all link layer parameters of the wired interface of the controller 
        linkParams = netifaces.ifaddresses(WIRED_IFACE_NAME)[netifaces.AF_LINK]
        #Getting the mac parameter 
        mac = linkParams[0]['addr']
        #Removing the ":" from mac and encode the string as bytes
        mac = mac.replace(':','').encode('utf8')
 
        conMsg = CON + mac + END
        self.logger.info('Sending connection message {} to server'.format(conMsg))
        self.srvSock.sendall(conMsg)



    def recvRespConMsg(self, timeToWait):
        '''
        This method receive the response to Connection Message.
        It waits until all response comes
        '''

        if not self.srvSock:
            raise ServerNotConnected

        self.srvSock.settimeout(WAIT_RESP_TIME)
   
        completeResp = b'' 
        completed = False
        while not completed:

            try:
                resp = self.srvSock.recv(REC_BYTES)
                if not resp:
                    raise ServerNotConnected
                self.logger.debug('The server respond to CON message with: {}'.format(resp))
                self.checkExit()
            except socket.timeout:
                raise TimeOutConnectionResponse

            completeResp += resp
            if completeResp.endswith(END):
                completed = True
            
        respContent = completeResp.strip(RCON+END)

        if respContent != b'OK':
            raise InvalidConnectionResponse




    #---------------------------------------------------------------------------#

    def run(self):
        '''
        This is the main method of the thread.
        When the controller is connected to the server, this method is blocked most of
        the time in "poll()" method waiting for bytes to go out or incoming bytes from 
        the server or  a event produced when the socket is broken or disconnect.
        When there is no connection to the server, this method tries to reconnect to 
        the server every "RECONNECT_TIME"
        '''

        #This connection is used only to clear the DB when receiving RRP message
        self.dataBase = database.DataBase(DB_FILE)

        while True:

            try:
                #Creating the socket to connect the to the server
                self.srvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
                #If there is no connection to the server, an exception will happen here
                self.srvSock.connect((SERVER_IP, SERVER_PORT))

                #Sending the Connection message to server
                self.sendConMsg()
                #Receiving the response from server. The below method checks the
                #if the server response is correct. If not it will raise "InvalidConnectionResponse"
                self.recvRespConMsg(WAIT_RESP_TIME)

                #Registering the socket in the network poller object
                self.netPoller.register(self.srvSock, select.POLLIN)
                self.connected.set()
                self.logger.info('Connected to server. IP: {}, PORT: {}'.format(SERVER_IP, SERVER_PORT))

                while self.connected.is_set():

                    for fd, pollEvnt in self.netPoller.poll(NET_POLL_MSEC):

                        #Every time a poll event happens, the time used for one iteration is lost.
                        #In this situation, if the controller is sending or receiving a lot of message,
                        #it will end up sending keep alive messages very often. For this reason, every
                        #time a poll event happens, "self.iterations" should be decremented to keep the
                        #time between keep alive messages. 
                        self.iteration -= 1

                        #This will happen when the "event" thread or "reSender"
                        #thread puts bytes in the "outBufferQue" and they want to notify
                        #this thread to wake up from "poll()"
                        if fd == self.unBlkrFd:
                            self.unblocker.receive()
                            continue


                        #This will happen when the server sends to us bytes.
                        if pollEvnt & select.POLLIN:
                            recBytes = self.srvSock.recv(REC_BYTES)
                            self.logger.debug('Receiving: {}'.format(recBytes))

                            #Receiving b'' means the server closed the connection
                            #On this situation we should close the socket and the
                            #next call to "poll()" will throw a POLLNVAL event
                            if not recBytes:
                                self.srvSock.close()
                                continue

                            #We should receive bytes until we receive the end of
                            #the message
                            allBytes = self.inBuffer + recBytes
                            
                            try:
                                while allBytes:
                                    msg = allBytes[:allBytes.index(END)+1]
                                    self.procRecMsg(msg)
                                    allBytes = allBytes[allBytes.index(END)+1:]
                                self.inBuffer = b''
                            
                            except ValueError:
                                self.inBuffer = allBytes


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
                                while True:
                                    self.outBuffer = self.outBufferQue.get(block = False)
                                    self.logger.debug('Sending: {}'.format(self.outBuffer))
                                    self.srvSock.sendall(self.outBuffer)
                            except queue.Empty:
                                #No more messages to send in "outBufferQue"
                                pass

                            #This exception happens when a controller interface used to 
                            #connect the server loses the connection and the controller
                            #try to send a message to it.
                            #This exception should be captured and then, the PULLHUP, PULLERR or PULLNVAL
                            #will come
                            except (OSError, ConnectionRefusedError, ConnectionResetError) as connectionError:
                                logMsg = ("Connection Error: {} while sending message"
                                            "".format(str(connectionError))
                                         )
                                self.logger.info(logMsg)
                                #The "outBufferQue" should be emptied because the resender
                                #thread put every interval of time the event in the "outBufferQue"
                                #while the "netMngr" thread gets it and try to send it to the server.
                                #In this situation of connection lost, at some point, the "netMngr"
                                #thread freezes trying to send the event, while the "resender" thread
                                #continue putting the same event in "outBufferQueue" many times.
                                #If the "outBufferQueue" is not emptied, when the connection is 
                                #recovered, this event is sent many times to the server.
                                self.outBufferQue.queue.clear()

                            #Once we finished sending all the messages, we should modify the
                            #"netPoller" object to be able to receive bytes again.
                            with self.lockNetPoller:
                                self.netPoller.modify(self.srvSock, select.POLLIN)


                        #This will happen when the server closes the socket or the 
                        #connection with the server is broken
                        elif pollEvnt & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
                            self.logger.info('The connection with server was broken.')
                            with self.lockNetPoller:
                                #Unregistering the socket from the "netPoller" object
                                self.netPoller.unregister(fd)
                            #Setting "connected" to False (this will break the while loop)
                            self.connected.clear()

                    #Cheking if Main thread ask as to finish.
                    self.checkExit()

                    #when reaching "self.ITERATIONS", a keep alive message should be
                    #sent to the server and "self.iterations" should be reseted to 0.
                    #Instead of assigning 0, 1 is assigned to "self.iterations", as
                    #a keep alive message will be sent, and "self.iterations"
                    #variable will be decremented instantaneously by 1 
                    if self.iteration >= self.ITERATIONS:
                        logMsg = 'Sending Keep Alive message to server.'
                        self.logger.debug(logMsg)
                        self.sendToServer(KAL + END)
                        self.iteration = 1
                    else:
                        self.iteration += 1


            except (OSError, ConnectionRefusedError, ConnectionResetError):
                self.logger.info('Could not establish connection with server.')

            except TimeOutConnectionResponse:
                self.logger.info('The server does not answer to Connect message.')

            except InvalidConnectionResponse:
                self.logger.info('The server does not respond OK to connection message')

            except ServerNotConnected:
                self.logger.info('The server disconected during initial connection message')



            finally:
                self.srvSock.close()
                self.checkExit()
                self.logger.info('Reconnecting to server in {} seconds...'.format(RECONNECT_TIME))
                time.sleep(RECONNECT_TIME)

    
