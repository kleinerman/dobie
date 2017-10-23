#!/usr/bin/env python3


import posix_ipc




QUEUE_FILE = '/ioiface_queue'

ioIfaceQue=posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT)

try:
    while True:
        ioIfaceData = ioIfaceQue.receive()
        ioIfaceData = ioIfaceData[0].decode('utf8')
        print(ioIfaceData)
            
except posix_ipc.SignalError:
    print('Door Interface Queue was interrupted by a OS signal.')


