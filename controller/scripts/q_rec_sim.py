#!/usr/bin/env python3

import posix_ipc


QUEUE_FILE = '/ioiface_queue'


ioIfaceQue = posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT, max_messages=50)

ioIfaceQue.unlink()
ioIfaceQue.close()

ioIfaceQue = posix_ipc.MessageQueue(QUEUE_FILE, posix_ipc.O_CREAT, max_messages=50)


while True:
    print(ioIfaceQue.receive())


