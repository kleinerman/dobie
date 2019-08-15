import logging

LOGGER_NAME = 'BackEndSrvr'

LOGGING_FILE = '/var/log/dobie-s/dobie-s.log'
PERS_IMG_DIR = '/var/lib/dobie-pers-imgs/'

PERS_IMG_FMT = 'JPEG'


DB_HOST = 'database'
DB_USER = 'dobie_usr'
DB_PASSWD = 'qwe123qwe'
DB_DATABASE = 'dobie_db'


EXIT_CHECK_TIME = 2
WAIT_RESP_TIME = 2

BIND_IP = '0.0.0.0'
BIND_PORT = 7979
SOCK_BUF_LEN = 1024
SIM_CONNECTIONS = 100


RE_SEND_TIME = 10

REC_BYTES = 4096

NET_POLL_MSEC = 1000

CONSIDER_DIED_MINS = 1


NODEJS_HOST = 'nodejs'
NODEJS_PORT = 5002
NODEJS_TOUT = 2

loggingLevel = logging.DEBUG

