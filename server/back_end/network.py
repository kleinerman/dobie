import threading
import logging
import datetime
import time
import os
import sys

import select
import socket
import json
import queue

import genmngr
import database
import msgreceiver
from config import *
from msgheaders import *



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
    def __init__(self, exitFlag, netToMsgRec, netToCrudReSndr):

        #Invoking the parent class constructor, specifying the thread name, 
        #to have a understandable log file.
        super().__init__('NetMngr', exitFlag)

        #Queue to send messages to crudReSndr thread
        self.netToCrudReSndr = netToCrudReSndr

        #Queue to send message to msgReceiver thread
        self.netToMsgRec = netToMsgRec

        #DataBase object
        #The creation of this object was moved to the run method to avoid
        #freezing the main thread when there is no connection to database.
        self.dataBase = None

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
            try:
                self.sendToCtrller(response, scktFd=fd)
            except CtrllerDisconnected:
                self.logger.warning("Controller not connected to receive the response")
            self.netToMsgRec.put(msg)


        elif msg.startswith(EVS):
            response = REVS + b'OK' + END
            try:
                self.sendToCtrller(response, scktFd=fd)
            except CtrllerDisconnected:
                self.logger.warning("Controller not connected to receive the response")
            self.netToMsgRec.put(msg)


        elif msg.startswith(RCUD):
            #When a response from an update or delete person is received, it is
            #necessary to know the controller which send that response. For this
            #reason, the MAC is inserted in the json dictionary.
            if bytes([msg[1]]) == b'P':
                index = msg.index(b'}')
                msg  = (msg[:index] 
                        + b', "mac": ' + self.fdConnObjects[fd]['mac'].encode('utf8') 
                        + msg[index:]
                       )
            self.netToMsgRec.put(msg)

        elif msg.startswith(KAL):
            self.netToMsgRec.put(bytes([msg[0]]) + self.fdConnObjects[fd]['mac'].encode('utf8') + bytes([msg[1]]))

        elif msg.startswith(RRRE):
            self.netToCrudReSndr.put(self.fdConnObjects[fd]['mac'])
            


    #---------------------------------------------------------------------------#



    def sendToCtrller(self, msg, mac = None, scktFd = None):
        '''
        '''
        if (not mac and not scktFd) or (mac and scktFd):
            self.logger.error('Error calling "sendToCtrller" function')
            raise ValueError("One of 'mac' or 'sctkFd' arguments should be 'None'")

        try:
            if mac:
                outBufferQue = self.macConnObjects[mac]['outBufferQue']
                ctrllerSckt = self.macConnObjects[mac]['socket']
            else:
                outBufferQue = self.fdConnObjects[scktFd]['outBufferQue']
                ctrllerSckt = self.fdConnObjects[scktFd]['socket']

        except KeyError:
            self.logger.debug('Controller not connected.')
            raise CtrllerDisconnected

        outBufferQue.put(msg)
        with self.lockNetPoller:
            self.netPoller.modify(ctrllerSckt, select.POLLOUT)






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

        if self.dataBase.isValidCtrller(ctrllerMac):
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

        #First of all, the database should be connected by the execution of this thread.
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)

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
                                       'outBufferQue': queue.Queue(),
                                       'mac': ctrllerMac
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




                #This will happen when the controller sends us bytes.
                elif pollEvnt & select.POLLIN:
                    ctrllerSckt = self.fdConnObjects[fd]['socket']
                    try:
                        recBytes = ctrllerSckt.recv(REC_BYTES)
                        self.logger.debug('Receiving: {}'.format(recBytes))
                    #The "ConnectionResetError" exception was seen when the NetMngr Thread
                    #on the controller broken
                    #The "OSError" exception was seen once running in docker environment
                    #never again
                    except (ConnectionResetError, OSError):
                        self.logger.warning('Controller lost the connection.')
                        ctrllerSckt.close()
                        continue

                    #Receiving b'' means the controller closed the connection
                    #On this situation we should close the socket and the
                    #next call to "poll()" will throw a POLLNVAL event
                    if not recBytes:
                        self.logger.warning('Controller closed the connection.')
                        ctrllerSckt.close()
                        continue


                    #If the other side sends us two or more message very fast, is very
                    #common to receive more than one message contiguously in a call to recv().
                    #For this reason we should consider the message until the END delimiter
                    #and store the rest. The rest could be an entire message or a part. 

                    #"allBytes" is the previous accumulated bytes that not complete
                    #an entire message plus the new received bytes. When theres is not
                    #accumulated bytes, "inBuffer" is empty.
                    allBytes = self.fdConnObjects[fd]['inBuffer'] + recBytes
                    try:
                        while allBytes:
                            #When "allBytes" does not contain END delimiter, a ValueError
                            #exception will occur and we should store "allBytes" in the
                            #"inBuffer" to concatenate it with the next reception.
                            msg = allBytes[:allBytes.index(END)+1]
                            #Processing an entire message
                            self.procRecMsg(fd, msg)
                            #Saving in "allBytes" variable the rest of the bytes after the
                            #first END delimiter. This could be one or more complete messages
                            #or a part of a message or a combination of both.
                            allBytes = allBytes[allBytes.index(END)+1:]
                        #If the while loop can finish (no exception was thrwon), that means
                        #there is no bytes to store for the next reception. For this reason
                        #we should clean up "inBuffer".
                        self.fdConnObjects[fd]['inBuffer'] = b''

                    except ValueError:
                        self.fdConnObjects[fd]['inBuffer'] = allBytes







                #msg = self.fdConnObjects[fd]['inBuffer'] + recBytes
                #    if msg.endswith(END):
                #        self.procRecMsg(fd, msg)
                #    else:
                #        self.fdConnObjects[fd]['inBuffer'] = msg


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

                    #There are situations in which "fdConnObjects" can have
                    #more entries than "macConnObjects" and when a "fd" is
                    #removed from "fdConnObjects", the whole "for loop" is
                    #executed without removing any "mac" from "macConnObjects".
                    #This can happen, for example, when the backend loses the
                    #connection with the database engine while a controller
                    #tries to connect the backend.
                    #Since on this situation, the "netMngr" thread is frozeen
                    #trying to connect the database, seems that more than socket
                    #is opened from the controller to server, more than one entry
                    #is added in "fdConnObjects" with different "fd" but with the
                    #same "connObject". On this situation, as the controller is
                    #the same and the MAC is the same, just one entry is added in
                    #"macConnObjects".
                    #When those socket times out and POLLHUP, POLLERR or POLLNVAL
                    #events are triggered, the subsecuents "pop(fd)" calls,
                    #empties "fdConnObjects" dictionary while "pop(mac)" call to
                    #"macConnObjects" is done only the first time and the subsecuent
                    #events execute the entire "for loop" without finding the MAC.
                    for mac in self.macConnObjects:
                        if connObject == self.macConnObjects[mac]:
                            self.macConnObjects.pop(mac)
                            break
                    #This call was moved to above loop taking into account
                    #the above explanation.
                    #self.macConnObjects.pop(mac)

            #print('MAC-->',self.macConnObjects)
            #print('FD-->',self.fdConnObjects)
                    

            #Cheking if Main thread ask as to finish.
            self.checkExit()



    
