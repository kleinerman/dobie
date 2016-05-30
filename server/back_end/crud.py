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
PASSWD = 'password'



class BadRequest(Exception):
    def __init__(self, message, status_code=400 ):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


class ConflictError(Exception):
    def __init__(self, message, status_code=409):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


class InternalError(Exception):
    def __init__(self, message, status_code=500):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


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

        
        # Error hanlders
        @app.errorhandler(BadRequest)
        def badRequest(error):
            response = jsonify ({'status': 'error', 'error': 'bad request', 'message': error.message, 'code':error.status_code})
            response.status_code = error.status_code
            return response

        @app.errorhandler(400)
        def badRequest(error):
            response = jsonify ({'status': 'error',
                                 'error': 'bad request', 
                                 'message':'the client sent a request that this server could not understand',
                                 'code':400})
            response.status_code = 400
            return response


        @app.errorhandler(404)
        def notFound(error):
            response = jsonify ({'status': 'error', 'error': 'request not found', 'message': 'Not found', 'code':404})
            response.status_code = 404
            return response


        @app.errorhandler(405)
        def methodNotAllowed(error):
            response = jsonify ({'status': 'error',
                                 'error': 'method not allowed', 
                                 'message':'The method is not allowed for the requested URL',
                                 'code':405})
            response.status_code = 405
            return response


        @app.errorhandler(ConflictError)
        def conflictError(error):
            response = jsonify ({'status': 'conflict',
                                 'error': ('The request could not be completed due to a conflict with '
                                           'the current state of the target resource'), 
                                 'message': error.message,
                                 'code':409})
            response.status_code = 409
            return response


        @app.errorhandler(InternalError)
        def internalServerError(error):
            response = jsonify ({'status': 'error', 'error': 'internal server error', 'message': error.message , 'code':500})
            response.status_code = 500
            return response


        @auth.error_handler
        def unauthorized():
            response = jsonify ({'status': 'error', 'error': 'Unauthorized access'})
            response.status_code = 403
            return response
 

        # For API authentication
        @auth.get_password
        def get_password(username):
            if username == USER:
                return PASSWD
            else:
                return None


        # Global API protection:
        # before_request decorator registers a function that runs before requests.
        # Decorating with login_required this function it avoids to decorate every route in the API
        @app.before_request
        @auth.login_required
        def before_request():
                pass


        @app.route('/api/v1.0/organization', methods=['POST', 'PUT','DELETE'])
        def crudOrganization():
            try:
                if request.method == 'POST':
                    # if this json key does not exist, it will raise a BadRequest exception
                    necessaryKeys = ('name',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.addOrganization(request.json)
                    return jsonify({'status': 'OK', 'message': 'Organization added'}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.updOrganization(request.json)
                    return jsonify({'status': 'OK', 'message': 'Organization updated'}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.delOrganization(request.json)
                    return jsonify({'status': 'OK', 'message': 'Organization deleted'}), OK

            except database.OrganizationError as e:
                raise ConflictError(str(e))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))


        @app.route('/api/v1.0/zone', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudZone():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.addZone(request.json)
                    return jsonify({'status': 'OK', 'message': 'Zone added'}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.updZone(request.json)
                    return jsonify({'status': 'OK', 'message': 'Zone updated'}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.delZone(request.json)
                    return jsonify({'status': 'OK', 'message': 'Zone deleted'}), OK

            except database.ZoneError as e:
                raise ConflictError(str(e))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        @app.route('/api/v1.0/person', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudPerson():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.addPerson(request.json)
                    return jsonify({'status': 'OK', 'message': 'Person added'}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'name', 'cardNumber', 'orgId')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.updPerson(request.json)
                    return jsonify({'status': 'OK', 'message': 'Person updated'}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.delPerson(request.json)
                    return jsonify({'status': 'OK', 'message': 'Person deleted'}), OK

            except database.PersonError as e:
                raise ConflictError(str(e))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        @app.route('/api/v1.0/controller', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudController():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('boardModel', 'macAddress', 'ipAddress')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.addController(request.json)
                    return jsonify({'status': 'OK', 'message': 'Controller added'}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'boardModel', 'macAddress', 'ipAddress')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.updController(request.json)
                    return jsonify({'status': 'OK', 'message': 'Controller updated'}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.delController(request.json)
                    return jsonify({'status': 'OK', 'message': 'Controller deleted'}), OK

            except database.ControllerError as e:
                raise ConflictError(str(e))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        @app.route('/api/v1.0/passage', methods=['POST', 'PUT','DELETE'])
        @auth.login_required
        def crudPassage():
            try:
                if request.method == 'POST':
                    necessaryKeys = ('i0In', 'i1In', 'o0In', 'o1In', 'bttnIn',
                                     'stateIn', 'rlseOut', 'bzzrOut', 'zoneId',
                                     'controllerId', 'rowStateId')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.addPassage(request.json)
                    return jsonify({'status': 'OK', 'message': 'Passage added'}), CREATED

                elif request.method == 'PUT':
                    necessaryKeys = ('id', 'i0In', 'i1In', 'o0In', 'o1In',
                                     'bttnIn', 'stateIn', 'rlseOut', 'bzzrOut',
                                     'zoneId', 'controllerId', 'rowStateId')
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.updPassage(request.json)
                    return jsonify({'status': 'OK', 'message': 'Passage updated'}), OK

                elif request.method == 'DELETE':
                    necessaryKeys = ('id',)
                    if not all(key in request.json for key in necessaryKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(necessaryKeys)))
                    self.dbMngr.delPassage(request.json)
                    return jsonify({'status': 'OK', 'message': 'Passage deleted'}), OK

            except database.PassageError as e:
                raise ConflictError(str(e))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

