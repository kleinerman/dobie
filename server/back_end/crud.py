import threading
import logging
import os

import socket
import json

import database
import queue

import genmngr
import netpassage
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
    def __init__(self, netMngr):

        #Database object to access DB
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        self.netPassage = netpassage.NetPassage(netMngr)


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
                    self.dataBase.addOrganization(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.updOrganization(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.delOrganization(request.json)
                    return jsonify({'1': 1}), OK


            except database.OrganizationError as organizationError:
                return jsonify({'1': 1}), 500






        @app.route('/api/v1.0/zone', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudZone():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.addZone(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.updZone(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.delZone(request.json)
                    return jsonify({'1': 1}), OK


            except database.ZoneError as ozoneError:
                return jsonify({'1': 1}), 500






        @app.route('/api/v1.0/person', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudPerson():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.addPerson(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.updPerson(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.delPerson(request.json)
                    return jsonify({'1': 1}), OK


            except database.PersonError as personError:
                return jsonify({'1': 1}), 500







        @app.route('/api/v1.0/controller', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudController():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('boardModel', 'macAddress', 'ipAddress')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.addController(request.json)
                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'boardModel', 'macAddress', 'ipAddress')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.updController(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.delController(request.json)
                    return jsonify({'1': 1}), OK


            except database.ControllerError as controllerError:
                return jsonify({'1': 1}), 500





        @app.route('/api/v1.0/passage', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudPassage():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('i0In', 'i1In', 'o0In', 'o1In', 'bttnIn',
                                     'stateIn', 'rlseOut', 'bzzrOut', 'zoneId',
                                     'controllerId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    passageId = self.dataBase.addPassage(request.json)

                    passage = request.json
                    passage['id'] = passageId
                    ctrllerMac = self.dataBase.getControllerMac(passageId)
                    self.netPassage.addPassage(ctrllerMac, passage)

                    return jsonify({'1': 1}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'i0In', 'i1In', 'o0In', 'o1In',
                                     'bttnIn', 'stateIn', 'rlseOut', 'bzzrOut',
                                     'zoneId', 'controllerId')
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.updPassage(request.json)
                    return jsonify({'1': 1}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        abort(BAD_REQUEST)
                    self.dataBase.delPassage(request.json)
                    return jsonify({'1': 1}), OK


            except database.PassageError as passageError:
                return jsonify({'1': 1}), 500





                

        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

