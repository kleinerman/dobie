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

        @app.route('/api/v1.0/organization', methods=['POST'])
        def addOrganization():
            if not request.json or not 'name' in request.json:
                abort(400)

            self.dbMngr.addOrganization(request.json)

            return jsonify({'1': 1}), 201




        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

