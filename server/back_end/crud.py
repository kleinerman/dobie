import threading
import logging
import os

import socket
import json

import database
import queue

import genmngr
from config import *


import sys

from flask import Flask, jsonify, request, abort
import time


class CrudMngr(genmngr.GenericMngr):

    '''
    This thread receives the events from the main thread, tries to send them to the server.
    When it doesn't receive confirmation from the server, it stores them in database.
    '''
    def __init__(self, dbMngr):

        self.dbMngr = dbMngr




    #---------------------------------------------------------------------------#

    def run(self):
        '''
        '''


        app = Flask(__name__)

        @app.route('/api/v1.0/organization', methods=['POST'])
        def addOrganization():
            if not request.json or not 'name' in request.json:
                abort(400)

            print(request.json['name'])

            self.dbMngr.saveOrganization(request.json)

            return jsonify({'1': 1}), 201




        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

