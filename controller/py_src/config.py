import logging

SIM_PERSON_QUANT = 5000
SIM_LIM_ACCESS_QUANT = 500

IOIFACE_BIN = '/opt/dobie/controller/c_src/ioiface'
IOIFACE_ARGS = ['id', 'i0In', 'i1In', 'o0In', 'o1In', 'bttnIn', 'stateIn', 'rlseOut', 'bzzrOut']

DB_FILE = '/opt/dobie/controller/py_src/access.db'
QUEUE_FILE = '/ioiface_queue'

WIRED_IFACE_NAME = 'eth0'

LOGGING_FILE ='/opt/dobie/controller/py_src/logevents.log'

IOFACE_LOGGING_FILE ='/opt/dobie/controller/py_src/ioifaceout.log'

#SERVER_IP = '192.168.1.79'
SERVER_IP = '10.10.7.79'
SERVER_PORT = 7979

EXIT_CHECK_TIME = 2
WAIT_RESP_TIME = 2

RE_SEND_TIME = 5

RECONNECT_TIME = 2

REC_BYTES = 4096

NET_POLL_MSEC = 1000

KEEP_ALIVE_TIME = 57

RE_SEND_EVTS_QUANT = 4

IOIFACE_WAIT_FINISH_TIME = 4


loggingLevel = logging.DEBUG

