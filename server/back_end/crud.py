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

import time

from flask import Flask, jsonify, request, abort
from flask.ext.httpauth import HTTPBasicAuth

# constants
BAD_REQUEST = 400
CREATED = 201
OK = 200
USER = 'conpass'
PASSWD = 'p4sw0rd'


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
        auth = HTTPBasicAuth()

        @auth.get_password
        def get_password(username):
            if username == USER:
                return PASSWD
            else:
                return None

        @app.route('/api/v1.0/organization', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudOrganization():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.addOrganization(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.updOrganization(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.delOrganization(request.json)
                    return jsonify({'1': 1}), OK


            except database.OrganizationError as organizationError:
                return jsonify({'1': 1}), 500


        @app.route('/api/v1.0/person', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudPerson():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.addPerson(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.updPerson(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dbMngr.delPerson(request.json)
                    return jsonify({'1': 1}), OK


            except database.PersonError as personError:
                return jsonify({'1': 1}), 500





                

        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

