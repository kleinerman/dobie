import logging

LOGGER_NAME = 'BackEndSrvr'

LOGGING_FILE = '/var/log/dobie-s/dobie-s.log'
PURGER_LOG_FILE = '/var/log/dobie-s/dobie-purger.log'
PERS_IMG_DIR = '/var/lib/dobie-pers-imgs/'

PERS_IMG_FMT = 'JPEG'


SSL_ENABLED =  True
SRVR_CERT = '/var/lib/dobie-certs/back_end.crt'
SRVR_KEY = '/var/lib/dobie-certs/back_end.key'
CLNT_CERT = '/var/lib/dobie-certs/controller.crt'

DB_HOST = 'database'
DB_USER = 'dobie_usr'
DB_PASSWD = 'qwe123qwe'
DB_DATABASE = 'dobie_db'


EXIT_CHECK_TIME = 2
WAIT_RESP_TIME = 2

BIND_IP = '0.0.0.0'
#If the port is changed, docker-compose.yml
#file should be modified
BIND_PORT = 9797
SOCK_BUF_LEN = 1024
SIM_CONNECTIONS = 100


REST_API_BIND_IP = '0.0.0.0'
#If the port is changed, docker-compose.yml
#file should be modified
REST_API_PORT = 5000

RE_SEND_TIME = 10

REC_BYTES = 4096

NET_POLL_MSEC = 1000

CONSIDER_DIED_MINS = 1


NODEJS_HOST = 'nodejs'
#If the port is changed, docker-compose.yml
#file should be modified
NODEJS_PORT = 5002
NODEJS_TOUT = 2

loggingLevel = logging.DEBUG

