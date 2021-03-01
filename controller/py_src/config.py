import logging

SIM_PERSON_QUANT = 5000
SIM_LIM_ACCESS_QUANT = 500

POWEROFF_BIN = 'poweroff'

IOIFACE_BIN = '/opt/dobie/controller/bin/ioiface'

IR_1_WGND_BITS = 26
OR_1_WGND_BITS = 26

IR_2_WGND_BITS = 26
OR_2_WGND_BITS = 26

IR_3_WGND_BITS = 26
OR_3_WGND_BITS = 26

GPIO_CHIP_NAME = "gpiochip0"
CONSUMER = "consumer_name"


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
SERVER_IP = '10.10.10.61'
#SERVER_IP = '127.0.0.1'
SERVER_PORT = 9797

SOCK_TIMEOUT = 2
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


#Event Type IDs
EVT_PERS_CARD = 1
EVT_PERS_BUTT = 2
EVT_REMAIN_OPEN = 3
EVT_FORCED = 4
EVT_OPEN_SKD = 5
EVT_CLOSE_SKD = 6
EVT_OPEN_WHILE_SKD = 7
EVT_OPEN_UI = 8


#Door Lock IDs
LCK_CARD_READER = 1
LCK_FINGERPRINT = 2
LCK_BUTTON = 3

