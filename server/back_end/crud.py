import threading
import logging
import os
import socket
import json
import queue
import sys
import time
from flask import Flask, jsonify, request, abort, url_for
from flask_httpauth import HTTPBasicAuth


import genmngr
import database
import ctrllermsger
from config import *


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
    def __init__(self, netMngr):

        #Database object to access DB
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        self.ctrllerMsger = ctrllermsger.CtrllerMsger(netMngr)


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





#-------------------------------------Organization------------------------------------------

        orgNeedKeys = ('name',)

        @app.route('/api/v1.0/organization', methods=['POST'])
        def addOrganization():
            try:
                # if this json key does not exist, it will raise a BadRequest exception
                if not all(key in request.json for key in orgNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))
                orgId = self.dataBase.addOrganization(request.json)
                uri = url_for('modOrganization', orgId=orgId, _external=True)

                return jsonify({'status': 'OK', 'message': 'Organization added', 'code': CREATED, 'uri': uri}), CREATED

            except database.OrganizationError as organizationError:
                raise ConflictError(str(organizationError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))

        @app.route('/api/v1.0/organization/<int:orgId>', methods=['PUT','DELETE'])
        def modOrganization(orgId):
            try:
                organization = request.json
                organization['id'] = orgId

                if request.method == 'PUT':
                    if not all(key in request.json for key in orgNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))
                    self.dataBase.updOrganization(organization)
                    return jsonify({'status': 'OK', 'message': 'Organization updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delOrganization({'id':orgId})
                    return jsonify({'status': 'OK', 'message': 'Organization deleted'}), OK

            except database.OrganizationError as organizationError:
                raise ConflictError(str(organizationError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))






#-------------------------------------Zone------------------------------------------

        zoneNeedKeys = ('name',)

        @app.route('/api/v1.0/zone', methods=['POST'])
        @auth.login_required
        def addZone():
            try:
                if not all(key in request.json for key in zoneNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(zoneNeedKeys)))
                zoneId = self.dataBase.addZone(request.json)
                uri = url_for('modZone', zoneId=zoneId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Zone added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ZoneError as zoneError:
                raise ConflictError(str(zoneError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        @app.route('/api/v1.0/zone/<int:zoneId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modZone(zoneId):
            try:
                zone = request.json
                zone['id'] = zoneId

                if request.method == 'PUT':
                    if not all(key in request.json for key in zoneNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(zoneNeedKeys)))

                    self.dataBase.updZone(zone)
                    return jsonify({'status': 'OK', 'message': 'Zone updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delZone(zone)
                    return jsonify({'status': 'OK', 'message': 'Zone deleted'}), OK

            except database.ZoneError as zoneError:
                raise ConflictError(str(zoneError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





#-------------------------------------Person------------------------------------------


        prsnNeedKeys = ('name', 'cardNumber', 'orgId')

        @app.route('/api/v1.0/person', methods=['POST'])
        @auth.login_required
        def addPerson():
            try:
                if not all(key in request.json for key in prsnNeedKeys):
                   raise BadRequest('Invalid request. Missing: {}'.format(', '.join(prsnNeedKeys)))
                personId = self.dataBase.addPerson(request.json)
                uri = url_for('modPerson', personId=personId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Person added', 'code': CREATED, 'uri': uri}), CREATED

            except database.PersonError as personError:
                raise ConflictError(str(personError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))

        @app.route('/api/v1.0/person/<int:personId>', methods=['POST'])
        @auth.login_required
        def modPerson(personID):
            try:
                person = request.json
                person['id'] = personId

                if request.method == 'PUT':
                    if not all(key in request.json for key in prsnNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(prsnNeedKeys)))

                    self.dataBase.updPerson(person)
                    return jsonify({'status': 'OK', 'message': 'Person updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delPerson(person)
                    return jsonify({'status': 'OK', 'message': 'Person deleted'}), OK

            except database.PersonError as personError:
                raise ConflictError(str(personError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



#--------------------------------------Controller------------------------------------------

        ctrllerNeedKeys = ('boardModel', 'macAddress', 'ipAddress')

        @app.route('/api/v1.0/controller', methods=['POST'])
        @auth.login_required
        def addController():
            try:
                if not all(key in request.json for key in ctrllerNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))
                controllerId = self.dataBase.addController(request.json)
                uri = url_for('modController', controllerId=controllerId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Controller added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))


        @app.route('/api/v1.0/controller/<int:controllerId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modController(controllerId):
            try:

                controller = request.json
                controller['id'] = controllerId

                if request.method == 'PUT':
                    if not all(key in request.json for key in ctrllerNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))
                    self.dataBase.updController(controller)
                    return jsonify({'status': 'OK', 'message': 'Controller updated'}), OK
                
                elif request.method == 'DELETE':
                    self.dataBase.delController(controller)
                    return jsonify({'status': 'OK', 'message': 'Controller deleted'}), OK

            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))


#--------------------------------------Passage------------------------------------------


        pssgNeedKeys = ('i0In', 'i1In', 'o0In', 'o1In', 'bttnIn',
                        'stateIn', 'rlseOut', 'bzzrOut', 'rlseTime',
                        'bzzrTime', 'alrmTime', 'zoneId', 'controllerId')

        @app.route('/api/v1.0/passage', methods=['POST'])
        @auth.login_required
        def addPassage():
            try:

                passage = request.json

                if not all(key in request.json for key in pssgNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(pssgNeedKeys)))
                passageId = self.dataBase.addPassage(passage)
                passage['id'] = passageId
                passage.pop('zoneId')
                passage.pop('controllerId')
                ctrllerMac = self.dataBase.getControllerMac(passageId)
                self.ctrllerMsger.addPassage(ctrllerMac, passage)

                uri = url_for('modPassage', passageId=passageId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Passage added', 'code': CREATED, 'uri': uri}), CREATED

            except database.PassageError as passageError:
                raise ConflictError(str(passageError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))

        @app.route('/api/v1.0/passage/<int:passageId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modPassage(passageId):
            try:
                
                passage = request.json
                passage['id'] = passageId

                if request.method == 'PUT':
                    if not all(key in request.json for key in pssgNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(pssgNeedKeys)))
                    self.dataBase.updPassage(passage)
                    passage.pop('zoneId')
                    passage.pop('controllerId')
                    ctrllerMac = self.dataBase.getControllerMac(passageId)
                    self.ctrllerMsger.updPassage(ctrllerMac, passage)

                    return jsonify({'status': 'OK', 'message': 'Passage updated'}), OK

                elif request.method == 'DELETE':
                    ctrllerMac = self.dataBase.getControllerMac(passageId)
                    self.dataBase.markPassageToDel(passageId)
                    self.ctrllerMsger.delPassage(ctrllerMac, passageId)
                    return jsonify({'status': 'OK', 'message': 'Passage deleted'}), OK

            except database.PassageError as passageError:
                raise ConflictError(str(passageError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))


#----------------------------------------Main--------------------------------------------


        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

