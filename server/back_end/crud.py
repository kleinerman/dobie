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

# constants
BAD_REQUEST = 400
CREATED = 201


class CrudMngr(genmngr.GenericMngr):

    '''
    This class is responsible for managing the creations, deletions and 
    modifications in database
    '''
    def __init__(self, dbMngr):

        #Database manager object to access DB
        self.dbMngr = dbMngr


    #---------------------------------------------------------------------------#

    def run(self):
        '''
        This method is launched by the main thread.
        It launches the Flask server and it waits for REST request from the GUI
        '''

        app = Flask(__name__)

        @auth.get_password
        def get_password(username):
            if username == 'conpass':
                return 'p4ssw0rd'
            else:
                return None

        @app.route('/api/v1.0/organization', methods=['POST'])
        @auth.login_required
        def addOrganization():
            if not request.json or not 'name' in request.json:
                abort(BAD_REQUEST)
                
            self.dbMngr.addOrganization(request.json)
            return jsonify({'xxx': 'xxx'}), CREATED

        # run the server
        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

