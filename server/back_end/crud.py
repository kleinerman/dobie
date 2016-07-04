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

# Constants used in the code
#
BAD_REQUEST = 400
CREATED = 201
OK = 200
USER = 'conpass'
PASSWD = 'password'


# Exceptions used by Flask errorhandler decorator
#
class BadRequest(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


class NotFound(Exception):
    def __init__(self, message, status_code=404):
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
    Through a RESTful API, this clase manages creations, deletions and modifications in
    the database.
    '''
    def __init__(self, netMngr):

        #Database object to access DB
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        self.ctrllerMsger = ctrllermsger.CtrllerMsger(netMngr)


    #---------------------------------------------------------------------------#

    def run(self):
        '''
        Launch the Flask server and wait for REST request
        '''

        app = Flask(__name__)
        auth = HTTPBasicAuth()

        
        ## Error hanlders
        #
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


        @app.errorhandler(NotFound)
        def notFound(error):
            response = jsonify ({'status': 'error', 'error': 'request not found', 'message': error.message, 'code':404})
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

        
        # Tuple with all necessary keys in the URL request
        orgNeedKeys = ('name',)

        @app.route('/api/v1.0/organization', methods=['POST'])
        def addOrganization():
            '''
            Add a new organization into the database
            '''
            try:
                # Check if all key:value are present before modify the database
                if not all(key in request.json for key in orgNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))

                # Add organization into the database and get the database 'id' of this organization
                orgId = self.dataBase.addOrganization(request.json)
                # Generate a URL to the given endpoint with the method provided.
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
            '''
            Update or delete an organization in the database
            '''
            try:
                # organization is a dictionary with the request json.
                organization = request.json
                # add the database organization id into the dictionary
                organization['id'] = orgId

                # Update an organization
                if request.method == 'PUT':
                    # Check if all key:value are present before modify the database
                    if not all(key in request.json for key in orgNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))
                    self.dataBase.updOrganization(organization)
                    return jsonify({'status': 'OK', 'message': 'Organization updated'}), OK

                # Delete an organization
                elif request.method == 'DELETE':
                    self.dataBase.delOrganization({'id':orgId})
                    return jsonify({'status': 'OK', 'message': 'Organization deleted'}), OK

            except database.OrganizationNotFound as organizationNotFound:
                raise NotFound(str(organizationNotFound))
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
            '''
            Add a new Zone into the database
            '''
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
            '''
            Update or delete a Zone in the database.
            '''
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

            except database.ZoneNotFound as zoneNotFound:
                raise NotFound(str(zoneNotFound))
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
            '''
            Add a new Person into the database.
            '''
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

        @app.route('/api/v1.0/person/<int:personId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modPerson(personId):
            '''
            Update or delete a Zone in the database.
            '''
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

            except database.PersonNotFound as personNotFound:
                raise NotFound(str(personNotFound))
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
            '''
            Add a new Controller into the database.
            '''
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
            '''
            Update or delete a Controller in the database.
            '''
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

            except database.ControllerNotFound as controllerNotFound:
                raise NotFound(str(controllerNotFound))
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
            '''
            Add a new Passage into the database and send it to the controller
            '''
            try:
                passage = request.json
                if not all(key in request.json for key in pssgNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(pssgNeedKeys)))
                pssgId = self.dataBase.addPassage(passage)
                
                # Passage dictionary modified for the controller database (same server passage id)
                passage['id'] = pssgId
                passage.pop('zoneId')
                passage.pop('controllerId')
                # Get the controller mac address
                ctrllerMac = self.dataBase.getControllerMac(pssgId)
                self.ctrllerMsger.addPassage(ctrllerMac, passage)

                uri = url_for('modPassage', pssgId=pssgId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Passage added', 'code': CREATED, 'uri': uri}), CREATED

            except database.PassageError as passageError:
                raise ConflictError(str(passageError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))

        @app.route('/api/v1.0/passage/<int:pssgId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modPassage(pssgId):
            '''
            Update or delete a Passage in the database and send the modification to
            the appropriate controller.
            '''
            try:
                
                passage = request.json
                passage['id'] = pssgId

                if request.method == 'PUT':
                    if not all(key in request.json for key in pssgNeedKeys):
                        raise BadRequest('Invalid request. Missing: {}'.format(', '.join(pssgNeedKeys)))
                    self.dataBase.updPassage(passage)
                    passage.pop('zoneId')
                    passage.pop('controllerId')
                    ctrllerMac = self.dataBase.getControllerMac(pssgId)
                    self.ctrllerMsger.updPassage(ctrllerMac, passage)

                    return jsonify({'status': 'OK', 'message': 'Passage updated'}), OK

                elif request.method == 'DELETE':
                    ctrllerMac = self.dataBase.getControllerMac(pssgId)
                    self.dataBase.markPassageToDel(pssgId)
                    self.ctrllerMsger.delPassage(ctrllerMac, pssgId)
                    return jsonify({'status': 'OK', 'message': 'Passage deleted'}), OK

            except database.PassageNotFound as passageNotFound:
                raise NotFound(str(passageNotFound))
            except database.PassageError as passageError:
                raise ConflictError(str(passageError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



#--------------------------------------Access------------------------------------------


        addAccessNeedKeys = ('pssgId', 'personId', 'iSide', 'oSide',
                          'startTime', 'endTime', 'expireDate')

        @app.route('/api/v1.0/access', methods=['POST'])
        @auth.login_required
        def addAccess():
            '''
            Add a new Access into the database and send it to the controller
            '''
            try:
                access = request.json
                if not all(key in request.json for key in addAccessNeedKeys):
                    raise BadRequest('Invalid request. Missing: {}'.format(', '.join(pssgNeedKeys)))
                accessId = self.dataBase.addAccess(access)

                # Access dictionary modified for the controller database (same server access id)
                access['id'] = accessId
        
                #Get the person parameters as a dictionary
                person = self.dataBase.getPerson(access['personId'])

                #Adding to access dictionary necesary person parameters to add person if it doesn't
                #exist in controller

                access['cardNumber'] = person['cardNumber']

                # Get the controller mac address
                pssgId = access['pssgId']
                ctrllerMac = self.dataBase.getControllerMac(pssgId)

                self.ctrllerMsger.addAccess(ctrllerMac, access)

                uri = url_for('modAccess', accessId=accessId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Access added', 'code': CREATED, 'uri': uri}), CREATED


            #This exception could be raised by getPerson() method.
            #It will never happen since addAccess() method will raise an exception caused by constraint.
            except database.PersonNotFound as personNotFound:
                raise NotFound(str(personNotFound))
            #This exception could be raised by getControllerMac() method.
            #It will never happen since addAccess() method will raise an exception caused by constraint.
            except database.PassageNotFound as passageNotFound:
                raise NotFound(str(passageNotFound))
            except database.AccessError as accessError:
                raise ConflictError(str(accessError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



        updAccessNeedKeys = ('pssgId', 'iSide', 'oSide', 'startTime', 'endTime', 'expireDate')

        @app.route('/api/v1.0/access/<int:accessId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modAccess(accessId):
            '''
            Update or delete a Access in the database and send the modification to
            the appropriate controller.
            '''
            try:
                if request.method == 'PUT':
                    # Create a clean access dictionary with only required access params,
                    # removing unnecessary parameters if the client send them.
                    # Also a KeyError wil be raised if the client misses any parameter.
                    access = {}
                    for param in updAccessNeedKeys:
                        access[param] = request.json[param]
                    access['id'] = accessId
                    self.dataBase.updAccess(access)

                    ctrllerMac = self.dataBase.getControllerMac(access['pssgId'])
                    self.ctrllerMsger.updAccess(ctrllerMac, access)

                    return jsonify({'status': 'OK', 'message': 'Access updated'}), OK

                elif request.method == 'DELETE':
                    ctrllerMac = self.dataBase.getControllerMac(accessId)
                    self.dataBase.markAccessToDel(accessId)
                    self.ctrllerMsger.delAccess(ctrllerMac, accessId)
                    return jsonify({'status': 'OK', 'message': 'Access deleted'}), OK

            except database.PassageNotFound as passageNotFound:
                raise NotFound(str(passageNotFound))
            except database.AccessNotFound as accessNotFound:
                raise NotFound(str(accessNotFound))
            except database.AccessError as accessError:
                raise ConflictError(str(accessError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(pssgNeedKeys)))


#----------------------------------------Main--------------------------------------------


        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

