import logging

SIM_PERSON_QUANT = 5000
SIM_LIM_ACCESS_QUANT = 500

POWEROFF_BIN = '/usr/bin/poweroff'

IOIFACE_BIN = '/opt/dobie/controller/bin/ioiface'
IOIFACE_ARGS = ['id', 'i0In', 'i1In', 'o0In', 'o1In', 'bttnIn', 'stateIn', 'rlseOut', 'bzzrOut']

DB_FILE = '/var/lib/dobie-c/dobie-c.db'


SSL_ENABLED = True
SRVR_CERT = '/var/lib/dobie-c/certs/back_end.crt'
CLNT_CERT = '/var/lib/dobie-c/certs/controller.crt'
CLNT_KEY = '/var/lib/dobie-c/certs/controller.key'

QUEUE_FILE = '/ioiface_queue'

WIRED_IFACE_NAME = 'eth0'

LOGGING_FILE ='/var/log/dobie-c/dobie-c.log'

IOFACE_LOGGING_FILE ='/var/log/dobie-c/ioiface.log'

SERVER_HOSTNAME = 'server.dobie'
#SERVER_IP = '192.168.1.79'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9797

EXIT_CHECK_TIME = 2
WAIT_RESP_TIME = 2

RE_SEND_TIME = 5

RECONNECT_TIME = 2

CHECK_OPEN_DOORS_MINS = 1


REC_BYTES = 4096

NET_POLL_MSEC = 1000

KEEP_ALIVE_TIME = 57

RE_SEND_EVTS_QUANT = 4

IOIFACE_WAIT_FINISH_TIME = 4


loggingLevel = logging.DEBUG

