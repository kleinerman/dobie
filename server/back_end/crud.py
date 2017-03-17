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
import network
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
    def __init__(self):

        #Database object to access DB
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE)

        self.ctrllerMsger = None


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

        @app.route('/api/v1.0/organization', methods=['POST', 'GET'])
        def Organizations():
            '''
            GET: return a list with all organizations
            POST: add a new organization in the database
            '''
            try:
                ## Return a JSON with all organizations
                if request.method == 'GET':
                    organizations = self.dataBase.getOrganizations()

                    for organization in organizations:
                        organization['uri'] = url_for('Organization', orgId=organization['id'], _external=True)
                        organization.pop('id')
                    return jsonify(organizations)

                ## Add a new organizations
                elif request.method == 'POST':
                    organization = {}
                    for param in orgNeedKeys:
                        organization[param] = request.json[param]
                    # Add organization into the database and get the database 'id' of this organization
                    orgId = self.dataBase.addOrganization(organization)
                    # Generate a URL to the given endpoint with the method provided.
                    uri = url_for('Organization', orgId=orgId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'Organization added', 'code': CREATED, 'uri': uri}), CREATED

            except database.OrganizationError as organizationError:
                raise ConflictError(str(organizationError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))


        @app.route('/api/v1.0/organization/<int:orgId>', methods=['GET','PUT','DELETE'])
        def Organization(orgId):
            '''
            GET: Return a list with all persons in the organization
            PUT: Update an organization in the database
            DELETE: Delete an organization
            '''
            try:
                #If somebody is trying to modify/delete the "Visitors"
                #organization via REST, we should respond with 404 (Not Found)
                if orgId == 1:
                    raise database.OrganizationNotFound('Organization not found')

                ## For GET method
                if request.method == 'GET':
                    persons = self.dataBase.getPersons(orgId)
                    
                    for person in persons:
                        person['uri'] = url_for('modPerson', personId=person['id'], _external=True)
                        person.pop('id')
                    return jsonify(persons)

                # Update an organization
                elif request.method == 'PUT':
                    organization = {}
                    organization['id'] = orgId
                    for param in orgNeedKeys:
                        organization[param] = request.json[param]
                    self.dataBase.updOrganization(organization)
                    return jsonify({'status': 'OK', 'message': 'Organization updated'}), OK

                # Delete an organization
                elif request.method == 'DELETE':
                    self.dataBase.delOrganization(orgId)
                    for person in self.dataBase.getPersons(orgId, includeDeleted=False):
                        ctrllerMacsToDelPrsn = self.dataBase.markPerson(person['id'], database.TO_DELETE)
                        self.ctrllerMsger.delPerson(ctrllerMacsToDelPrsn, person['id'])
                        
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
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(orgNeedKeys)))



#-------------------------------------Zone------------------------------------------

        zoneNeedKeys = ('name',)

        @app.route('/api/v1.0/zone', methods=['GET', 'POST'])
        @auth.login_required
        def Zones():
            '''
            GET: Return a list with all zones
            POST: Add a new Zone into the database
            '''

            try:
                ## For GET method
                if request.method == 'GET':
                    zones = self.dataBase.getZones()
                    for zone in zones:
                        zone['uri'] = url_for('Zone', zoneId=zone['id'], _external=True)
                        zone.pop('id')
                    return jsonify(zones)

                ## For POST method
                elif request.method == 'POST':
                    zone = {}
                    for param in zoneNeedKeys:
                        zone[param] = request.json[param]
                    zoneId = self.dataBase.addZone(zone)
                    uri = url_for('Zone', zoneId=zoneId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'Zone added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ZoneError as zoneError:
                raise ConflictError(str(zoneError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(zoneNeedKeys)))



        @app.route('/api/v1.0/zone/<int:zoneId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def Zone(zoneId):
            '''
            GET: List all passages in the zone
            PUT/DELETE: Update or delete a Zone in the database.
            '''
            try:

                ## For GET method
                if request.method == 'GET':
                    passages = self.dataBase.getPassages(zoneId=zoneId)
                    
                    for passage in passages:
                        passage['uri'] = url_for('modPassage', pssgId=passage['id'], _external=True)
                        passage.pop('id')
                    return jsonify(passages)


                ## For PUT and DELETE methods
                elif request.method == 'PUT':
                    zone = {}
                    zone['id'] = zoneId
                    for param in zoneNeedKeys:
                        zone[param] = request.json[param]
                    self.dataBase.updZone(zone)
                    return jsonify({'status': 'OK', 'message': 'Zone updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delZone(zoneId)
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
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(zoneNeedKeys)))



#----------------------------------VisitorsPassages------------------------------------

        visitorsPssgsNeedKeys = ('name',)

        @app.route('/api/v1.0/visitorspassages', methods=['POST', 'GET'])
        @auth.login_required
        def visitorsPssgss():
            ''' 
            Add a new Visitors Passages into the database.
            '''     
            try:    
                ## For GET method
                if request.method == 'GET':
                    visitorsPssgss = self.dataBase.getVisitorsPssgss()
                    for visitorsPssgs in visitorsPssgss:
                        visitorsPssgs['uri'] = url_for('visitorsPssgs', visitorsPssgsId=visitorsPssgs['id'], _external=True)
                        visitorsPssgs.pop('id')
                    return jsonify(visitorsPssgss)
                ## For POST method
                elif request.method == 'POST':
                    visitorsPssgs = {}
                    for param in visitorsPssgsNeedKeys:
                        visitorsPssgs[param] = request.json[param]
                    visitorsPssgsId = self.dataBase.addVisitorsPssgs(visitorsPssgs)
                    uri = url_for('visitorsPssgs', visitorsPssgsId=visitorsPssgsId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'Visitors Passage added', 'code': CREATED, 'uri': uri}), CREATED

            except database.VisitorsPssgsError as visitorsPssgsError:
                raise ConflictError(str(visitorsPssgsError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(visitorsPssgsNeedKeys)))




        @app.route('/api/v1.0/visitorspassages/<int:visitorsPssgsId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def visitorsPssgs(visitorsPssgsId):
            '''
            Update or delete a Visitors Passages in the database.
            '''
            try:

    
                ## For GET method
                if request.method == 'GET':
                    passages = self.dataBase.getPassages(visitorsPssgsId=visitorsPssgsId)

                    for passage in passages:
                        passage['uri'] = url_for('modPassage', pssgId=passage['id'], _external=True)
                        passage.pop('id')
                    return jsonify(passages)


                elif request.method == 'PUT':
                    visitorsPssgs = {}
                    visitorsPssgs['id'] = visitorsPssgsId
                    for param in visitorsPssgsNeedKeys:
                        visitorsPssgs[param] = request.json[param]
                    self.dataBase.updVisitorsPssgs(visitorsPssgs)
                    return jsonify({'status': 'OK', 'message': 'Visitors Passages updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delVisitorsPssgs(visitorsPssgsId)
                    return jsonify({'status': 'OK', 'message': 'Controller deleted'}), OK

            except database.VisitorsPssgsNotFound as visitorsPssgsNotFound:
                raise NotFound(str(visitorsPssgsNotFound))
            except database.VisitorsPssgsError as visitorsPssgsError:
                raise ConflictError(str(visitorsPssgsError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(visitorsPssgsNeedKeys)))









        @app.route('/api/v1.0/visitorspassages/<int:visitorsPssgsId>/passage/<int:pssgId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def pssgInVisitorsPssgs(visitorsPssgsId, pssgId):
            ''' 
            Add a new Visitors Passages into the database.
            '''
            try:
                if request.method == 'PUT':
                    self.dataBase.addPssgToVisitorsPssgs(visitorsPssgsId, pssgId)
                    return jsonify({'status': 'OK', 'message': 'Passage added to Visitors Passages'}), OK
                elif request.method == 'DELETE':
                    self.dataBase.delPssgFromVisitorsPssgs(visitorsPssgsId, pssgId)
                    return jsonify({'status': 'OK', 'message': 'Passage deleted from Visitors Passages'}), OK

            except database.VisitorsPssgsError as visitorsPssgsError:
                raise ConflictError(str(visitorsPssgsError))
            except database.VisitorsPssgsNotFound as visitorsPssgsNotFound:
                raise NotFound(str(visitorsPssgsNotFound))


            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))












#-------------------------------------Person------------------------------------------

        prsnNeedKeys = ('name', 'cardNumber', 'orgId', 'visitedOrgId')

        @app.route('/api/v1.0/person', methods=['POST'])
        @auth.login_required
        def addPerson():
            '''
            Add a new Person into the database.
            '''
            try:
                person = {}
                for param in prsnNeedKeys:
                    person[param] = request.json[param]
                personId = self.dataBase.addPerson(person)
                uri = url_for('modPerson', personId=personId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Person added', 'code': CREATED, 'uri': uri}), CREATED

            except database.PersonError as personError:
                raise ConflictError(str(personError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(prsnNeedKeys)))



        @app.route('/api/v1.0/person/<int:personId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modPerson(personId):
            '''
            GET: Return a JSON with all accesses that this person has
            PUT/DELETE: Update or delete a Zone in the database.
            '''

            try:
                #If somebody is trying to modify/delete the "Unknown" person
                #via REST, we should respond with 404 (Not Found)
                if personId == 1:
                    raise database.PersonNotFound('Person not found')
                ## For GET method
                if request.method == 'GET':
                    accesses = self.dataBase.getAccesses(personId)
                    for access in accesses:
                        access['uri'] = url_for('modAccess', accessId=access['id'], _external=True)
                        try:
                            for liAccess in access['liAccesses']:
                                liAccess['uri'] = url_for('modLiAccess', liAccessId=liAccess['id'], _external=True)
                        except KeyError:
                            pass
                        # Remove id
                        access.pop('id')

                    return jsonify(accesses)

				## For PUT and DELETE method
                elif request.method == 'PUT':
                    person = {}
                    person['id'] = personId
                    for param in prsnNeedKeys:
                        person[param] = request.json[param]
                    self.dataBase.updPerson(person)
                    person.pop('name')
                    person.pop('orgId')
                    person.pop('visitedOrgId')
                    ctrllerMacsToUpdPrsn = self.dataBase.markPerson(personId, database.TO_UPDATE)
                    self.ctrllerMsger.updPerson(ctrllerMacsToUpdPrsn, person)
                    return jsonify({'status': 'OK', 'message': 'Person updated'}), OK

                elif request.method == 'DELETE':
                    ctrllerMacsToDelPrsn = self.dataBase.markPerson(personId, database.TO_DELETE)
                    self.ctrllerMsger.delPerson(ctrllerMacsToDelPrsn, personId)
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
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(prsnNeedKeys)))




#--------------------------------------Controller------------------------------------------

        ctrllerNeedKeys = ('ctrllerModelId', 'macAddress')

        @app.route('/api/v1.0/controller', methods=['POST'])
        @auth.login_required
        def addController():
            '''
            Add a new Controller into the database.
            '''
            try:
                controller = {}
                for param in ctrllerNeedKeys:
                    controller[param] = request.json[param]
                controllerId = self.dataBase.addController(controller)
                uri = url_for('modController', controllerId=controllerId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Controller added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '          
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))



        @app.route('/api/v1.0/controller/<int:controllerId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modController(controllerId):
            '''
            Update or delete a Controller in the database.
            '''
            try:
                if request.method == 'PUT':
                    controller = {}
                    controller['id'] = controllerId
                    for param in ctrllerNeedKeys:
                        controller[param] = request.json[param]
                    self.dataBase.updController(controller)
                    return jsonify({'status': 'OK', 'message': 'Controller updated'}), OK
                
                elif request.method == 'DELETE':
                    self.dataBase.delController(controllerId)
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
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))





        @app.route('/api/v1.0/controller/<int:controllerId>/reprov', methods=['PUT'])
        @auth.login_required
        def reProvController(controllerId):
            '''
            Re provision all CRUD of a controller.
            '''
            try:
                self.dataBase.reProvController(controllerId)
                ctrllerMac = self.dataBase.getControllerMac(controllerId=controllerId)
                self.ctrllerMsger.requestReProv(ctrllerMac)

                return jsonify({'status': 'OK', 'message': 'Controller updated'}), OK

            except network.CtrllerDisconnected:
                raise NotFound("Controller not connected")
            except database.ControllerNotFound as controllerNotFound:
                raise NotFound(str(controllerNotFound))
            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))







#--------------------------------------Passage------------------------------------------


        pssgNeedKeys = ('description', 'pssgNum', 'controllerId', 'rlseTime', 'bzzrTime', 'alrmTime', 'zoneId')

        @app.route('/api/v1.0/passage', methods=['POST'])
        @auth.login_required
        def addPassage():
            '''
            Add a new Passage into the database and send it to the controller
            '''
            try:
                passage = {}
                for param in pssgNeedKeys:
                    passage[param] = request.json[param]
                pssgId = self.dataBase.addPassage(passage)

                # Passage dictionary modified for the controller database (same server passage id)
                passage['id'] = pssgId
                passage.pop('description')
                passage.pop('zoneId')
                passage.pop('controllerId')
                # Get the controller mac address
                ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
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
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(pssgNeedKeys)))


        @app.route('/api/v1.0/passage/<int:pssgId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modPassage(pssgId):
            '''
            Update or delete a Passage in the database and send the modification to
            the appropriate controller.
            '''
            try:
                if request.method == 'PUT':
                    # Create a clean passage dictionary with only required passage params,
                    # removing unnecessary parameters if the client send them.
                    # Also a KeyError wil be raised if the client misses any parameter.
                    passage = {}
                    passage['id'] = pssgId
                    for param in pssgNeedKeys:
                        passage[param] = request.json[param]
                    self.dataBase.updPassage(passage)
                    passage.pop('description')
                    passage.pop('zoneId')
                    passage.pop('controllerId')
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
                    self.ctrllerMsger.updPassage(ctrllerMac, passage)

                    return jsonify({'status': 'OK', 'message': 'Passage updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markPassageToDel(pssgId)
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
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
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(pssgNeedKeys)))



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
                # Create a clean access dictionary with only required access params,
                # removing unnecessary parameters if the client send them.
                # Also a KeyError will be raised if the client misses any parameter.
                access = {}
                for param in addAccessNeedKeys:
                    access[param] = request.json[param]

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
                ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)

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
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(addAccessNeedKeys)))



        updAccessNeedKeys = ('iSide', 'oSide', 'startTime', 'endTime', 'expireDate')

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
                    access['id'] = accessId
                    for param in updAccessNeedKeys:
                        access[param] = request.json[param]
                    self.dataBase.updAccess(access)

                    pssgId = self.dataBase.getPssgId(accessId=accessId)
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
                    self.ctrllerMsger.updAccess(ctrllerMac, access)

                    return jsonify({'status': 'OK', 'message': 'Access updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markAccessToDel(accessId)
                    pssgId = self.dataBase.getPssgId(accessId=accessId)
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
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
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(updAccessNeedKeys)))







#---------------------------------Limited Access--------------------------------------


        addLiAccessNeedKeys = ('pssgId', 'personId', 'weekDay', 'iSide', 
                               'oSide', 'startTime', 'endTime', 'expireDate')

        @app.route('/api/v1.0/liaccess', methods=['POST'])
        @auth.login_required
        def addLiAccess():
            '''
            Add a new Limited Access into the database and send it to the controller
            '''
            try:
                # Create a clean access dictionary with only required access params,
                # removing unnecessary parameters if the client send them.
                # Also a KeyError will be raised if the client misses any parameter.
                liAccess = {}
                for param in addLiAccessNeedKeys:
                    liAccess[param] = request.json[param]

                # Checking if the client is sending an invalid week day
                if not 1 <= liAccess['weekDay'] <= 7:
                    raise TypeError

                accessId, liAccessId = self.dataBase.addLiAccess(liAccess)

                # Access dictionary modified for the controller database (same server access id)
                liAccess['id'] = liAccessId
                liAccess['accessId'] = accessId

                #Get the person parameters as a dictionary
                person = self.dataBase.getPerson(liAccess['personId'])

                #Adding to access dictionary necesary person parameters to add person if it doesn't
                #exist in controller
                liAccess['cardNumber'] = person['cardNumber']

                # Get the controller mac address
                pssgId = liAccess['pssgId']
                ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)

                self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)

                uri = url_for('modLiAccess', liAccessId=liAccessId, _external=True)
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
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(addLiAccessNeedKeys)))




        updLiAccessNeedKeys = ('weekDay', 'iSide', 'oSide', 'startTime', 'endTime', 'expireDate')

        @app.route('/api/v1.0/liaccess/<int:liAccessId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def modLiAccess(liAccessId):
            '''
            Update or delete a Access in the database and send the modification to
            the appropriate controller.
            '''
            try:
                if request.method == 'PUT':
                    # Create a clean access dictionary with only required access params,
                    # removing unnecessary parameters if the client send them.
                    # Also a KeyError wil be raised if the client misses any parameter.
                    liAccess = {}
                    liAccess['id'] = liAccessId
                    for param in updLiAccessNeedKeys:
                        liAccess[param] = request.json[param]

                    # Checking if the client is sending an invalid week day
                    if not 1 <= liAccess['weekDay'] <= 7:
                        raise TypeError

                    self.dataBase.updLiAccess(liAccess)
                    pssgId = self.dataBase.getPssgId(liAccessId=liAccessId)
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
                    self.ctrllerMsger.updLiAccess(ctrllerMac,liAccess)

                    return jsonify({'status': 'OK', 'message': 'Limited Access updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markLiAccessToDel(liAccessId)
                    pssgId = self.dataBase.getPssgId(liAccessId=liAccessId)
                    ctrllerMac = self.dataBase.getControllerMac(passageId=pssgId)
                    self.ctrllerMsger.delLiAccess(ctrllerMac, liAccessId)
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
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(updLiAccessNeedKeys)))









#----------------------------------------Main--------------------------------------------


        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000, threaded=True)

