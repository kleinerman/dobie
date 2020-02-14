import argparse

import logging
import logging.handlers

import datetime
import sys

import queue
import threading
import signal

import database
from config import *


import os

inputParser = argparse.ArgumentParser(description='Event purger')
inputParser.add_argument('-d', '--until-date-time', dest='untilDateTime',
                         help='Until date time to clear events', required=True)

arguments = vars(inputParser.parse_args())
untilDateTime = arguments['untilDateTime']

loggingHandler = logging.handlers.WatchedFileHandler(PURGER_LOG_FILE)
loggingFormat = '%(asctime)s %(levelname)s %(threadName)s: %(message)s'
dateFormat = '[%b %d %H:%M:%S]'

loggingFormatter = logging.Formatter(loggingFormat, dateFormat)
loggingHandler.setFormatter(loggingFormatter)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(loggingLevel)
logger.addHandler(loggingHandler)


try:
    dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, None)
    delEvents = dataBase.purgeEvents(untilDateTime)
    logger.info("{} events were deteled.".format(delEvents))
except database.EventNotFound:
    logger.warning("There aren't events to purge.")
except database.NotReachable:
    logger.warning("DB engine not reachable, exiting..")

