import threading
import logging
import os
import socket
import json
import queue
import sys
import time
import crypt

from flask import Flask, jsonify, request, abort, url_for, g, send_from_directory
from flask_httpauth import HTTPBasicAuth

from gevent.pywsgi import WSGIServer

import genmngr
import database
import network
import ctrllermsger
from config import *
from PIL import Image

# Constants used in the code
#
BAD_REQUEST = 400
CREATED = 201
OK = 200


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

    #Although this is not a typical thread because it is the "mainThread", it has
    #a constructor that receives the "exitFlag" because when somebody send a REST
    #query, a new thread is created by the werkzeug server with the name "thread-N"
    #and with the same attributes that the "mainThread". When there is no connection
    #to data base, this thread (thread-N) freezes trying to connect the data base.
    #If in that situation a SIGTERM arrives, the "exitflag" clonned by the "mainThread",
    #allows it to finish as the rest of the threads.
    def __init__(self, exitFlag):

        super().__init__('Main', exitFlag)

        #Database object to access DB
        self.dataBase = None

        self.ctrllerMsger = None

        self.exitFlag = exitFlag


    #---------------------------------------------------------------------------#

    def run(self):
        '''
        Launch the Flask server and wait for REST request
        '''
        #Maybe this connection to database could stay in the constructor, but
        #just to be sure it was put here because I don't know what will happend with
        #the clonned threads created by werkzeug server when REST messages arrives
        #and there is no connection to database.
        self.dataBase = database.DataBase(DB_HOST, DB_USER, DB_PASSWD, DB_DATABASE, self)

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



        @auth.verify_password
        def verify_password(username, password):
            '''
            '''
            #Retrieve user parameters from database
            try:
                user = self.dataBase.getUser(username=username)
            #This exception can happen when somebody try to send a REST request without authentication.
            except database.UserError:
                return False

            if user:

                #Get the password hashed and salted from user parameters
                passwdHash = user['passwdHash']
                #Get only the salt from the previous variable
                salt = passwdHash.split('$')[2]
                #With the password passed in the request, recalculing the hash
                #using MD5 ($1) algorithm and the stored salt and comparing the result
                #with the stored hash
                if crypt.crypt(password, '$1${}'.format(salt)) == passwdHash:
                    #If the username and password is correct, save the user parameters in "g"
                    #flask object to be able to use them in user resource and return True
                    g.user = user
                    return True
            return False





        # Global API protection:
        # before_request decorator registers a function that runs before requests.
        # Decorating with login_required this function it avoids to decorate every route in the API
        @app.before_request
        @auth.login_required
        def before_request():
                pass



#------------------------------------User----------------------------------------------
        @app.route('/api/v1.0/login', methods=['GET'])
        def login():
            '''
            GET: Return user parametters of the logged user. The role parametter
            is used by the UI to know the options to show.
            '''
            g.user.pop('passwdHash')
            return jsonify(g.user)




        userNeedKeys = ('username', 'passwd', 'fullName', 'roleId', 'language', 'active')

        @app.route('/api/v1.0/user', methods=['GET', 'POST'])
        @auth.login_required
        def Users():
            '''
            GET: Return a list with all user
            POST: Add a new user into the database
            '''

            try:
                ## For GET method
                if request.method == 'GET':
                    users = self.dataBase.getUsers()
                    for user in users:
                        user['uri'] = url_for('User', userId=user['id'], _external=True)
                        user.pop('passwdHash')
                    return jsonify(users)

                ## For POST method
                elif request.method == 'POST':
                    user = {}
                    for param in userNeedKeys:
                        user[param] = request.json[param]
                    userId = self.dataBase.addUser(user)
                    uri = url_for('User', userId=userId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'User added', 'code': CREATED, 'uri': uri}), CREATED

            except database.UserNotFound as userNotFound:
                raise NotFound(str(userNotFound))
            except database.UserError as userError:
                raise ConflictError(str(userError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(userNeedKeys)))



        @app.route('/api/v1.0/user/<int:userId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def User(userId):
            '''
            GET: Get an user from database
            PUT: Update a user in database
            DELETE: Delete a user in the database.
            '''
            try:

                if request.method == 'GET':
                    user = self.dataBase.getUser(userId=userId)
                    user['uri'] = request.url
                    user.pop('passwdHash')
                    return jsonify(user)

                elif request.method == 'PUT':
                    user = {}
                    user['id'] = userId
                    for param in userNeedKeys:
                        #If the frontend doesn't send some of the parameters, keep the old ones
                        try:
                            user[param] = request.json[param]
                        except KeyError:
                            pass

                    #If the user is the admin main user, doesn't modify nothing except the
                    #passwd or language if the front end sent it. The second argument of pop
                    #is to return None as default value when the key is not in the dictionary.
                    if user['id'] == 1:
                        user.pop('username', None)
                        user.pop('fullName', None)
                        user.pop('roleId', None)
                        user.pop('active', None)

                    self.dataBase.updUser(user)
                    return jsonify({'status': 'OK', 'message': 'User updated'}), OK

                elif request.method == 'DELETE':
                    if userId == 1:
                        raise database.UserError
                    self.dataBase.delUser(userId)
                    return jsonify({'status': 'OK', 'message': 'User deleted'}), OK

            except database.UserNotFound as userNotFound:
                raise NotFound(str(userNotFound))
            except database.UserError as userError:
                raise ConflictError(str(userError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request.')





#------------------------------------ResState----------------------------------------------
        @app.route('/api/v1.0/resstate', methods=['GET'])
        def resState():
            '''
            GET: Return a list with all persons in the organization
            '''
            try:
                ## For GET method
                resStates = self.dataBase.getResStates()
                return jsonify(resStates)

            except database.ResStateNotFound as resStateNotFound:
                raise NotFound(str(resStateNotFound))
            except database.ResStateError as resStateError:
                raise ConflictError(str(resStateError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





#------------------------------------EventType----------------------------------------------
        @app.route('/api/v1.0/eventtype', methods=['GET'])
        def eventType():
            '''
            GET: Return a list with all persons in the organization
            '''
            try:
                ## For GET method
                eventTypes = self.dataBase.getEventTypes()

                return jsonify(eventTypes)


            except database.EventTypeNotFound as eventTypeNotFound:
                raise NotFound(str(eventTypeNotFound))
            except database.EventTypeError as eventTypeError:
                raise ConflictError(str(eventTypeError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))




#------------------------------------DoorLock----------------------------------------------
        @app.route('/api/v1.0/doorlock', methods=['GET'])
        def doorLock():
            '''
            GET: Return a list with all doorLocks
            '''
            try:
                ## For GET method
                doorLocks = self.dataBase.getDoorLocks()
                return jsonify(doorLocks)

            except database.DoorLockNotFound as doorLockNotFound:
                raise NotFound(str(doorLockNotFound))
            except database.DoorLockError as doorLockError:
                raise ConflictError(str(doorLockError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





#------------------------------------Denial Cause----------------------------------------------
        @app.route('/api/v1.0/denialcause', methods=['GET'])
        def denialCause():
            '''
            GET: Return a list with all doorLocks
            '''
            try:
                ## For GET method
                denialCauses = self.dataBase.getDenialCauses()
                return jsonify(denialCauses)


            except database.DenialCauseNotFound as denialCauseNotFound:
                raise NotFound(str(denialCauseNotFound))
            except database.DenialCauseError as denialCauseError:
                raise ConflictError(str(denialCauseError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



#--------------------------------------Role----------------------------------------------
        @app.route('/api/v1.0/role', methods=['GET'])
        def role():
            '''
            GET: Return a list with all roles
            '''
            try:
                ## For GET method
                roles = self.dataBase.getRoles()
                return jsonify(roles)


            except database.RoleNotFound as roleNotFound:
                raise NotFound(str(roleNotFound))
            except database.RoleError as roleError:
                raise ConflictError(str(roleError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))




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


        @app.route('/api/v1.0/organization/<int:orgId>', methods=['GET','PUT','DELETE'])
        def Organization(orgId):
            '''
            GET: Return a list with all persons in the organization
            PUT: Update an organization in the database
            DELETE: Delete an organization
            '''
            try:
                ## For GET method
                if request.method == 'GET':
                    organization = self.dataBase.getOrganization(orgId)
                    organization['uri'] = request.url
                    #organization['uri'] = url_for('Organization', orgId=orgId, _external=True)
                    return jsonify(organization)

                # Update an organization
                elif request.method == 'PUT':
                    if orgId == 1:
                        raise database.OrganizationNotFound('Organization not found')
                    organization = {}
                    organization['id'] = orgId
                    for param in orgNeedKeys:
                        organization[param] = request.json[param]
                    self.dataBase.updOrganization(organization)
                    return jsonify({'status': 'OK', 'message': 'Organization updated'}), OK

                # Delete an organization
                elif request.method == 'DELETE':
                    if orgId == 1:
                        raise database.OrganizationNotFound('Organization not found')
                    self.dataBase.delOrganization(orgId)
                    for person in self.dataBase.getOrgPersons(orgId, includeDeleted=False):
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




        @app.route('/api/v1.0/organization/<int:orgId>/person', methods=['GET',])
        def orgPersons(orgId):
            '''
            GET: Return a list with all persons in the organization
            '''
            try:
                persons = self.dataBase.getOrgPersons(orgId)

                for person in persons:
                    person['uri'] = url_for('modPerson', personId=person['id'], _external=True)
                    #Removing orgId as is the same for all the persons and is given by the user
                    #in the REST request.
                    person.pop('orgId')
                return jsonify(persons)


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
                        #zone.pop('id')
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
            GET: List all doors in the zone
            PUT/DELETE: Update or delete a Zone in the database.
            '''
            try:

                ## For GET method
                if request.method == 'GET':
                    zone = self.dataBase.getZone(zoneId)
                    zone['uri'] = request.url
                    return jsonify(zone)

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





        @app.route('/api/v1.0/zone/<int:zoneId>/door', methods=['GET',])
        @auth.login_required
        def zoneDoors(zoneId):
            '''
            GET: List all doors in the zone
            PUT/DELETE: Update or delete a Zone in the database.
            '''
            try:

                doors = self.dataBase.getDoors(zoneId=zoneId)
                for door in doors:
                    door['uri'] = url_for('modDoor', doorId=door['id'], _external=True)
                    #All the door will have the same zoneId, this parametter is given by the
                    #user in REST request.
                    door.pop('zoneId')
                    #door.pop('id')
                return jsonify(doors)

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








#----------------------------------DoorGroup------------------------------------

        doorGroupNeedKeys = ('name', 'isForVisit')

        @app.route('/api/v1.0/doorgroup', methods=['POST', 'GET'])
        @auth.login_required
        def doorGroups():
            '''
            Add a new Door Group into the database.
            '''
            try:
                ## For GET method
                if request.method == 'GET':
                    doorGroups = self.dataBase.getDoorGroups()
                    for doorGroup in doorGroups:
                        doorGroup['uri'] = url_for('doorGroup', doorGroupId=doorGroup['id'], _external=True)
                    return jsonify(doorGroups)
                ## For POST method
                elif request.method == 'POST':
                    doorGroup = {}
                    for param in doorGroupNeedKeys:
                        doorGroup[param] = request.json[param]
                    doorGroupId = self.dataBase.addDoorGroup(doorGroup)
                    uri = url_for('doorGroup', doorGroupId=doorGroupId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'Door Group added', 'code': CREATED, 'uri': uri}), CREATED

            except database.DoorGroupError as doorGroupError:
                raise ConflictError(str(doorGroupError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(doorGroupNeedKeys)))




        @app.route('/api/v1.0/doorgroup/<int:doorGroupId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def doorGroup(doorGroupId):
            '''
            Retrieve update or delete a Door Group into the database.
            '''
            try:

                if request.method == 'GET':
                    doorGroup = self.dataBase.getDoorGroup(doorGroupId)
                    doorGroup['uri'] = request.url
                    return jsonify(doorGroup)

                elif request.method == 'PUT':
                    doorGroup = {}
                    doorGroup['id'] = doorGroupId
                    for param in doorGroupNeedKeys:
                        doorGroup[param] = request.json[param]
                    self.dataBase.updDoorGroup(doorGroup)
                    return jsonify({'status': 'OK', 'message': 'Door Group updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.delDoorGroup(doorGroupId)
                    return jsonify({'status': 'OK', 'message': 'Door Group deleted'}), OK

            except database.DoorGroupNotFound as doorGroupNotFound:
                raise NotFound(str(doorGroupNotFound))
            except database.DoorGroupError as doorGroupError:
                raise ConflictError(str(doorGroupError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(doorGroupNeedKeys)))



        @app.route('/api/v1.0/doorgroup/<int:doorGroupId>/door', methods=['GET',])
        @auth.login_required
        def doorGroupDoor(doorGroupId):
            '''
            Returns the doors that belong to a door group
            '''
            try:
                doors = self.dataBase.getDoors(doorGroupId=doorGroupId)

                for door in doors:
                    door['uri'] = url_for('modDoor', doorId=door['id'], _external=True)
                    #door.pop('id')
                return jsonify(doors)

            except database.DoorGroupNotFound as doorGroupNotFound:
                raise NotFound(str(doorGroupNotFound))
            except database.DoorGroupError as doorGroupError:
                raise ConflictError(str(doorGroupError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(doorGroupNeedKeys)))





        @app.route('/api/v1.0/doorgroup/<int:doorGroupId>/door/<int:doorId>', methods=['PUT', 'DELETE'])
        @auth.login_required
        def doorInDoorGroup(doorGroupId, doorId):
            '''
            Add or delete a Door into Door Group.
            '''
            try:
                if request.method == 'PUT':
                    self.dataBase.addDoorToDoorGroup(doorGroupId, doorId)
                    return jsonify({'status': 'OK', 'message': 'Door added to Door Group'}), OK
                elif request.method == 'DELETE':
                    self.dataBase.delDoorFromDoorGroup(doorGroupId, doorId)
                    return jsonify({'status': 'OK', 'message': 'Door deleted from Door Group'}), OK

            except database.DoorGroupError as doorGroupError:
                raise ConflictError(str(doorGroupError))
            except database.DoorGroupNotFound as doorGroupNotFound:
                raise NotFound(str(doorGroupNotFound))


            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))












#-------------------------------------Person------------------------------------------

        prsnNeedKeys = ('names', 'lastName', 'identNumber', 'note', 'cardNumber', 'orgId')
        prsnNotNeedKeys = ('visitedOrgId', 'isProvider')

        @app.route('/api/v1.0/person', methods=['POST', 'GET'])
        @auth.login_required
        def addPerson():
            '''
            Add a new Person into the database.
            '''
            try:
                if request.method == 'POST':
                    person = {}
                    for param in prsnNeedKeys:
                        person[param] = request.json[param]

                    for param in prsnNotNeedKeys:
                        try:
                            person[param] = request.json[param]
                        except KeyError:
                            #When the param is not in JSON, saving the param as None. We could use 'NULL'
                            #to avoid changing it in database addPerson method, but if the API user send
                            #send null as value, we will retrieve it as None. In this way we leave the
                            #dictionary in the same way when the user of the API send null or don't send
                            #anything.
                            person[param] = None

                    personId = self.dataBase.addPerson(person)
                    uri = url_for('modPerson', personId=personId, _external=True)
                    return jsonify({'status': 'OK', 'message': 'Person added.', 'code': CREATED, 'uri': uri}), CREATED

                elif request.method == 'GET':
                    identNumber = request.args.get('identNumber')
                    cardNumber = request.args.get('cardNumber')
                    namesPattern = request.args.get('namesPattern')
                    lastNamePattern = request.args.get('lastNamePattern')
                    persons = self.dataBase.getPersons(identNumber, cardNumber, namesPattern, lastNamePattern)
                    return jsonify(persons)


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
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(prsnNeedKeys)))



        @app.route('/api/v1.0/person/<int:personId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modPerson(personId):
            '''
            GET: Return a JSON with all accesses that this person has
            PUT/DELETE: Update or delete a Zone in the database.
            '''

            try:
                ## For GET method
                if request.method == 'GET':
                    person = self.dataBase.getPerson(personId)
                    person['uri'] = request.url
                    return jsonify(person)

		## For PUT and DELETE method
                elif request.method == 'PUT':
                    person = {}
                    person['id'] = personId

                    for param in prsnNeedKeys:
                        person[param] = request.json[param]

                    for param in prsnNotNeedKeys:
                        try:
                            person[param] = request.json[param]
                        except KeyError:
                            #When the param is not in JSON, saving the param as None. We could use 'NULL'
                            #to avoid changing it in database addPerson method, but if the API user send
                            #send null as value, we will retrieve it as None. In this way we leave the
                            #dictionary in the same way when the user of the API send null or don't send
                            #anything.
                            person[param] = None

                    needUpdCtrllers = self.dataBase.updPerson(person)

                    #If it isn't necessary to update the "cardNumber" in the controller,
                    #the following "if" statement will not be executed
                    if needUpdCtrllers:
                        person.pop('names')
                        person.pop('lastName')
                        person.pop('identNumber')
                        person.pop('note')
                        person.pop('orgId')
                        person.pop('visitedOrgId')
                        person.pop('isProvider')
                        ctrllerMacsToUpdPrsn = self.dataBase.markPerson(personId, database.TO_UPDATE)
                        self.ctrllerMsger.updPerson(ctrllerMacsToUpdPrsn, person)

                    return jsonify({'status': 'OK', 'message': 'Person updated.'}), OK

                elif request.method == 'DELETE':
                    ctrllerMacsToDelPrsn = self.dataBase.markPerson(personId, database.TO_DELETE)
                    self.ctrllerMsger.delPerson(ctrllerMacsToDelPrsn, personId)
                    return jsonify({'status': 'OK', 'message': 'Person deleted.'}), OK

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





        @app.route('/api/v1.0/person/<int:personId>/image', methods=['PUT', 'GET'])
        @auth.login_required
        def personImage(personId):
            '''
            GET: Return a JSON with all accesses that this person has
            PUT/DELETE: Update or delete a Zone in the database.
            '''

            try:
                #The following method is called to throw "PersonNotFound" exception
                #if there isn't any person with this id
                self.dataBase.getPerson(personId)

                #For PUT method:
                if request.method == 'PUT' and request.files['image']:
                    receivedImg = request.files['image']
                    #If open fails to open the image, IOError exception is raised and catched below
                    image = Image.open(receivedImg)
                    imageFmt = image.format
                    if imageFmt != 'JPEG':
                        raise database.PersonError
                    savedPath = PERS_IMG_DIR + '/' + str(personId) + '.' + PERS_IMG_FMT.lower()
                    image.save(savedPath, format=PERS_IMG_FMT)
                    image.close()
                    return jsonify({'status': 'OK', 'message': 'Person updated.'}), OK

                #For GET method
                elif request.method == 'GET':
                    #if file doesn't exist, send_from_directory will throw NotFound exception
                    return send_from_directory(PERS_IMG_DIR, str(personId) + '.' + PERS_IMG_FMT.lower(), as_attachment=True)

            except database.PersonNotFound as personNotFound:
                raise NotFound(str(personNotFound))
            except (database.PersonError, IOError) as personError:
                raise ConflictError(str(personError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(prsnNeedKeys)))






        @app.route('/api/v1.0/person/<int:personId>/access', methods=['GET',])
        @auth.login_required
        def personAccesses(personId):
            '''
            GET: Return a JSON with all accesses that this person has
            '''

            try:
                ## For GET method
                accesses = self.dataBase.getAccesses(personId=personId)
                for access in accesses:
                    access['uri'] = url_for('modAccess', accessId=access['id'], _external=True)
                    try:
                        for liAccess in access['liAccesses']:
                            liAccess['uri'] = url_for('modLiAccess', liAccessId=liAccess['id'], _external=True)
                    except KeyError:
                        #This exception will happen when the access is allWeek access. In this situation
                        #nothing should be done.
                        pass

                return jsonify(accesses)



            except (database.AccessNotFound, database.PersonNotFound,
                    database.DoorNotFound) as notFound:
                raise NotFound(str(notFound))

            except database.AccessError as accessError:
                raise ConflictError(str(accessError))

            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





#------------------------------------ControllerModel--------------------------------------


        @app.route('/api/v1.0/controllermodel', methods=['GET'])
        @auth.login_required
        def controllermodel():
            '''
            GET: Return a list with all controller models in the system
            '''
            try:
                ## For GET method
                ctrllerModels = self.dataBase.getCtrllerModels()
                return jsonify(ctrllerModels)

            except database.CtrllerModelNotFound as ctrllerModelNotFound:
                raise NotFound(str(ctrllerModelNotFound))
            except database.CtrllerModelError as ctrllerModelError:
                raise ConflictError(str(ctrllerModelError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))






#--------------------------------------Controller------------------------------------------

        ctrllerNeedKeys = ('name', 'ctrllerModelId', 'macAddress')

        @app.route('/api/v1.0/controller', methods=['POST', 'GET'])
        @auth.login_required
        def Controllers():
            '''
            Add a new Controller into the database.
            '''
            try:
                if request.method == 'GET':
                    controllers = self.dataBase.getControllers()

                    for controller in controllers:
                        controller['uri'] = url_for('Controller', controllerId=controller['id'], _external=True)
                    return jsonify(controllers)

                elif request.method == 'POST':

                    controller = {}
                    for param in ctrllerNeedKeys:
                        controller[param] = request.json[param]
                    controllerId = self.dataBase.addController(controller)
                    uri = url_for('Controller', controllerId=controllerId, _external=True)
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





        @app.route('/api/v1.0/controller/<int:controllerId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def Controller(controllerId):
            '''
            Update or delete a Controller in the database.
            '''
            try:
                if request.method == 'GET':
                    controller = self.dataBase.getController(controllerId)
                    controller['uri'] = request.url
                    return jsonify(controller)

                elif request.method == 'PUT':
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





        @app.route('/api/v1.0/controller/<int:controllerId>/poweroff', methods=['PUT'])
        @auth.login_required
        def poweroffController(controllerId):
            '''
            Power off the controller
            '''
            try:
                ctrllerMac = self.dataBase.getControllerMac(controllerId=controllerId)
                self.ctrllerMsger.poweroffCtrller(ctrllerMac)

                return jsonify({'status': 'OK', 'message': 'Controller accepted power off message'}), OK

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



        @app.route('/api/v1.0/controller/uncommitted', methods=['GET'])
        @auth.login_required
        def getUnCmtCtrllers():
            '''
            Get uncommitted controllers.
            '''
            try:
                if request.method == 'GET':
                    unCmtCtrllers = self.dataBase.getUnCmtCtrllers()

                    for unCmtCtrller in unCmtCtrllers:
                        unCmtCtrller['uri'] = url_for('Controller', controllerId=unCmtCtrller['id'], _external=True)
                    return jsonify(unCmtCtrllers)


            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))



        @app.route('/api/v1.0/controller/<int:controllerId>/forcecommit', methods=['PUT'])
        @auth.login_required
        def forceCmtCtrller(controllerId):
            '''
            Mark all the CRUDS of the controller as committed although the controller is unreachable .
            '''
            try:

                if request.method == 'PUT':
                    ctrllerMac = self.dataBase.getControllerMac(controllerId=controllerId)
                    for door in self.dataBase.getUncmtDoors(ctrllerMac, database.TO_ADD, database.TO_UPDATE, database.TO_DELETE):
                        self.dataBase.commitDoor(door['id'])


                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addUnlkDoorSkd(ctrllerMac, unlkDoorSkd)
                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_UPDATE):
                        unlkDoorSkd.pop('doorId')
                        self.ctrllerMsger.updUnlkDoorSkd(ctrllerMac, unlkDoorSkd)
                    for unlkDoorSkd in self.dataBase.getUncmtUnlkDoorSkds(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delUnlkDoorSkd(ctrllerMac, unlkDoorSkd['id'])
                    self.checkExit()


                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addExcDayUds(ctrllerMac, excDayUds)
                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_UPDATE):
                        excDayUds.pop('doorId')
                        self.ctrllerMsger.updExcDayUds(ctrllerMac, excDayUds)
                    for excDayUds in self.dataBase.getUncmtExcDayUdss(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delExcDayUds(ctrllerMac, excDayUds['id'])
                    self.checkExit()


                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addAccess(ctrllerMac, access)
                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_UPDATE):
                        #The following parameters should not be sent when updating an access.
                        access.pop('doorId')
                        access.pop('personId')
                        access.pop('allWeek')
                        access.pop('cardNumber')
                        self.ctrllerMsger.updAccess(ctrllerMac, access)
                    for access in self.dataBase.getUncmtAccesses(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delAccess(ctrllerMac, access['id'])
                    self.checkExit()


                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_ADD):
                        self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)
                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_UPDATE):
                        #The following parameters should not be sent when updating an access.
                        liAccess.pop('accessId')
                        liAccess.pop('doorId')
                        liAccess.pop('personId')
                        liAccess.pop('cardNumber')
                        self.ctrllerMsger.updLiAccess(ctrllerMac, liAccess)
                    for liAccess in self.dataBase.getUncmtLiAccesses(ctrllerMac, database.TO_DELETE):
                        self.ctrllerMsger.delLiAccess(ctrllerMac, liAccess['id'])
                    self.checkExit()


                    #Persons never colud be in state TO_ADD. For this reason,
                    #only TO_UPDATE or TO_DELETE state is retrieved
                    for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_UPDATE):
                        person.pop('names')
                        person.pop('lastName')
                        person.pop('orgId')
                        person.pop('visitedOrgId')
                        person.pop('isProvider')
                        #"updPerson" method receive a list of MAC addresses to update. Because in this case only one
                        #controller is being updated, a list with only the MAC address of the controller is created.
                        self.ctrllerMsger.updPerson([ctrllerMac], person)
                    for person in self.dataBase.getUncmtPersons(ctrllerMac, database.TO_DELETE):
                        #"delPerson" method receive a list of MAC addresses to update. Because in this case only one
                        #controller is being updated, a list with only the MAC address of the controller is created.
                        self.ctrllerMsger.delPerson([ctrllerMac], person['id'])
                    self.checkExit()





            except database.ControllerError as controllerError:
                raise ConflictError(str(controllerError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Missing: {}'.format(', '.join(ctrllerNeedKeys)))




#--------------------------------------Door------------------------------------------


        doorNeedKeys = ('name', 'doorNum', 'controllerId', 'snsrType', 'unlkTime', 'bzzrTime', 'alrmTime', 'zoneId', 'isVisitExit')

        @app.route('/api/v1.0/door', methods=['POST'])
        @auth.login_required
        def addDoor():
            '''
            Add a new Door into the database and send it to the controller
            '''
            try:
                door = {}
                for param in doorNeedKeys:
                    door[param] = request.json[param]

                doorId = self.dataBase.addDoor(door)

                # Door dictionary modified for the controller database (same server door id)
                door['id'] = doorId
                door.pop('name')
                door.pop('controllerId')
                door.pop('zoneId')
                door.pop('isVisitExit')
                # Get the controller mac address
                ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                self.ctrllerMsger.addDoor(ctrllerMac, door)

                uri = url_for('modDoor', doorId=doorId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Door added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ControllerNotFound as controllerNotFound:
                raise NotFound(str(controllerNotFound))
            except database.DoorError as doorError:
                raise ConflictError(str(doorError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(doorNeedKeys)))


        @app.route('/api/v1.0/door/<int:doorId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modDoor(doorId):
            '''
            Update or delete a Door in the database and send the modification to
            the appropriate controller.
            '''
            try:
                ## For GET method
                if request.method == 'GET':
                    door = self.dataBase.getDoor(doorId)
                    door['uri'] = request.url
                    return jsonify(door)

                elif request.method == 'PUT':
                    # Create a clean door dictionary with only required door params,
                    # removing unnecessary parameters if the client send them.
                    # Also a KeyError will be raised if the client misses any parameter.
                    # The client can't modify controllerId when updating door since it is
                    # associated with a door but as it is needed to know the controller to
                    # send the message, it is got with the doorId.
                    door = {}
                    door['id'] = doorId
                    for param in [param for param in doorNeedKeys if param != 'controllerId']:
                        door[param] = request.json[param]
                    needUpdCtrller = self.dataBase.updDoor(door)

                    #If it isn't necessary to update the parameters in the controller,
                    #the following "if" statement will not be executed
                    if needUpdCtrller:
                        door.pop('name')
                        door.pop('zoneId')
                        door.pop('isVisitExit')
                        ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                        self.ctrllerMsger.updDoor(ctrllerMac, door)
                    return jsonify({'status': 'OK', 'message': 'Door updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markDoorToDel(doorId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.delDoor(ctrllerMac, doorId)
                    return jsonify({'status': 'OK', 'message': 'Door deleted'}), OK

            except (database.ControllerNotFound, database.DoorNotFound) as notFound:
                raise NotFound(str(notFound))
            except database.DoorError as doorError:
                raise ConflictError(str(doorError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(doorNeedKeys)))




        @app.route('/api/v1.0/door/<int:doorId>/open', methods=['PUT'])
        @auth.login_required
        def openDoor(doorId):
            '''
            Re provision all CRUD of a controller.
            '''
            try:
                ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                self.ctrllerMsger.openDoor(ctrllerMac, doorId)

                return jsonify({'status': 'OK', 'message': 'Door will be opened'}), OK

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





        @app.route('/api/v1.0/door/<int:doorId>/unlkdoorskd', methods=['GET',])
        @auth.login_required
        def doorUnlkDoorSkds(doorId):
            '''
            GET: Return a JSON with all unlkDoorSkds that this door has
            '''
            try:
                ## For GET method
                unlkDoorSkds = self.dataBase.getUnlkDoorSkds(doorId)
                for unlkDoorSkd in unlkDoorSkds:
                    unlkDoorSkd['uri'] = url_for('modUnlkDoorSkd', unlkDoorSkdId=unlkDoorSkd['id'], _external=True)

                return jsonify(unlkDoorSkds)


            except database.UnlkDoorSkdNotFound as unlkDoorSkdNotFound:
                raise NotFound(str(unlkDoorSkdNotFound))

            except database.UnlkDoorSkdError as unlkDoorSkdError:
                raise ConflictError(str(unlkDoorSkdError))

            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





        @app.route('/api/v1.0/door/<int:doorId>/excdayuds', methods=['GET',])
        @auth.login_required
        def doorExcDayUdss(doorId):
            '''
            GET: Return a JSON with all excDayUdss that this door has
            '''
            try:
                ## For GET method
                excDayUdss = self.dataBase.getExcDayUdss(doorId)
                for excDayUds in excDayUdss:
                    excDayUds['uri'] = url_for('modExcDayUds', excDayUdsId=excDayUds['id'], _external=True)

                return jsonify(excDayUdss)


            except database.ExcDayUdsNotFound as excDayUdsNotFound:
                raise NotFound(str(excDayUdsNotFound))

            except database.ExcDayUdsError as excDayUdsError:
                raise ConflictError(str(excDayUdsError))

            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))





        @app.route('/api/v1.0/door/<int:doorId>/access', methods=['GET',])
        @auth.login_required
        def doorAccesses(doorId):
            '''
            GET: Return a JSON with all accesses that this door has
            '''

            try:
                ## For GET method
                accesses = self.dataBase.getAccesses(doorId=doorId)
                for access in accesses:
                    access['uri'] = url_for('modAccess', accessId=access['id'], _external=True)
                    try:
                        for liAccess in access['liAccesses']:
                            liAccess['uri'] = url_for('modLiAccess', liAccessId=liAccess['id'], _external=True)
                    except KeyError:
                        #This exception will happen when the access is allWeek access. In this situation
                        #nothing should be done.
                        pass

                return jsonify(accesses)


            except (database.AccessNotFound, database.PersonNotFound,
                    database.DoorNotFound) as notFound:
                raise NotFound(str(notFound))

            except database.AccessError as accessError:
                raise ConflictError(str(accessError))

            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))


#-------------------------------Unlock Door Schedule-----------------------------------

        unlkDoorSkdNeedKeys = ('doorId', 'weekDay', 'startTime', 'endTime')

        @app.route('/api/v1.0/unlkdoorskd', methods=['POST'])
        @auth.login_required
        def addUnlkDoorSkd():
            '''
            Add a new Unlock Door Schedule into the database and send
            it to the appropriate controller
            '''

            try:
                unlkDoorSkd = {}
                for param in unlkDoorSkdNeedKeys:
                    unlkDoorSkd[param] = request.json[param]

                unlkDoorSkdId = self.dataBase.addUnlkDoorSkd(unlkDoorSkd)

                # Door dictionary modified for the controller database (same server door id)
                unlkDoorSkd['id'] = unlkDoorSkdId
                # Get the controller mac address
                ctrllerMac = self.dataBase.getControllerMac(doorId=unlkDoorSkd['doorId'])
                self.ctrllerMsger.addUnlkDoorSkd(ctrllerMac, unlkDoorSkd)

                uri = url_for('modUnlkDoorSkd', unlkDoorSkdId=unlkDoorSkdId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Unlock Door Schedule added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ControllerNotFound as controllerNotFound:
                raise NotFound(str(controllerNotFound))
            except database.UnlkDoorSkdError as unlkDoorSkdError:
                raise ConflictError(str(unlkDoorSkdError))

            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(unlkDoorSkdNeedKeys)))






        @app.route('/api/v1.0/unlkdoorskd/<int:unlkDoorSkdId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modUnlkDoorSkd(unlkDoorSkdId):
            '''
            Get, update or delete an Unlock Door Schedule into the database and send
            the modification to the appropriate controller.
            '''
            try:
                ## For GET method
                if request.method == 'GET':
                    unlkDoorSkd = self.dataBase.getUnlkDoorSkd(unlkDoorSkdId)
                    unlkDoorSkd['uri'] = request.url
                    return jsonify(unlkDoorSkd)

                elif request.method == 'PUT':
                    # Getting the doorId with unlkDoorSkdId. (The client can't modify doorId when
                    # updating unlkDoorSkd since it is associated with a door but it is needed to
                    # know the controller to send the message
                    doorId = self.dataBase.getDoorId(unlkDoorSkdId=unlkDoorSkdId)
                    # Create a clean unlkDoorSkd dictionary with only required unlkDoorSkd params,
                    # removing unnecessary parameters if the client send them.
                    unlkDoorSkd = {}
                    unlkDoorSkd['id'] = unlkDoorSkdId
                    # The client can't send doorId when updating unlkDoorSkd, if it is sent,
                    # it will not be used.
                    for param in [param for param in unlkDoorSkdNeedKeys if param != 'doorId']:
                        #A KeyError will be raised if the client misses any parameter.
                        unlkDoorSkd[param] = request.json[param]
                    self.dataBase.updUnlkDoorSkd(unlkDoorSkd)

                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.updUnlkDoorSkd(ctrllerMac, unlkDoorSkd)
                    return jsonify({'status': 'OK', 'message': 'Unlock Door Schedule updated'}), OK

                elif request.method == 'DELETE':
                    # Getting the doorId with unlkDoorSkdId. (The client can't modify doorId when
                    # updating unlkDoorSkd since it is associated with a door but it is needed to
                    # know the controller to send the message
                    doorId = self.dataBase.getDoorId(unlkDoorSkdId=unlkDoorSkdId)
                    self.dataBase.markUnlkDoorSkdToDel(unlkDoorSkdId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.delUnlkDoorSkd(ctrllerMac, unlkDoorSkdId)
                    return jsonify({'status': 'OK', 'message': 'Unlock Door Schedule deleted'}), OK

            except (database.ControllerNotFound, database.DoorNotFound,
                    database.UnlkDoorSkdNotFound) as notFound:
                raise NotFound(str(notFound))
            except (database.UnlkDoorSkdError, database.DoorError) as error:
                raise ConflictError(str(error))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(unlkDoorSkdNeedKeys)))





#-------------------------------Exception Day to Unlock Door Schedule-----------------------------------

        excDayUdsNeedKeys = ('doorId', 'excDay')

        @app.route('/api/v1.0/excdayuds', methods=['POST'])
        @auth.login_required
        def addExcDayUds():
            '''
            Add a new Exception Day to Unlock Door Schedule into the database and send
            it to the appropriate controller
            '''

            try:
                excDayUds = {}
                for param in excDayUdsNeedKeys:
                    excDayUds[param] = request.json[param]

                excDayUdsId = self.dataBase.addExcDayUds(excDayUds)

                # Door dictionary modified for the controller database (same server door id)
                excDayUds['id'] = excDayUdsId
                # Get the controller mac address
                ctrllerMac = self.dataBase.getControllerMac(doorId=excDayUds['doorId'])
                self.ctrllerMsger.addExcDayUds(ctrllerMac, excDayUds)

                uri = url_for('modExcDayUds', excDayUdsId=excDayUdsId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Exception Day to Unlock Door Schedule added', 'code': CREATED, 'uri': uri}), CREATED

            except database.ControllerNotFound as controllerNotFound:
                raise NotFound(str(controllerNotFound))
            except database.ExcDayUdsError as excDayUdsError:
                raise ConflictError(str(excDayUdsError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(excDayUdsNeedKeys)))






        @app.route('/api/v1.0/excdayuds/<int:excDayUdsId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modExcDayUds(excDayUdsId):
            '''
            Get, update or delete an Exception Day to Unlock Door Schedule into
            the database and send the modification to the appropriate controller.
            '''
            try:
                ## For GET method
                if request.method == 'GET':
                    excDayUds = self.dataBase.getExcDayUds(excDayUdsId)
                    excDayUds['uri'] = request.url
                    return jsonify(excDayUds)

                elif request.method == 'PUT':
                    # Getting the doorId with excDayUdsId. (The client can't modify doorId when
                    # updating excDayUds since it is associated with a door but it is needed to
                    # know the controller to send the message
                    doorId = self.dataBase.getDoorId(excDayUdsId=excDayUdsId)
                    # Create a clean excDayUds dictionary with only required excDayUds params,
                    # removing unnecessary parameters if the client send them.
                    excDayUds = {}
                    excDayUds['id'] = excDayUdsId
                    # The client can't send doorId when updating excDayUds, if it is sent,
                    # it will not be used.
                    for param in [param for param in excDayUdsNeedKeys if param != 'doorId']:
                        #A KeyError will be raised if the client misses any parameter.
                        excDayUds[param] = request.json[param]
                    self.dataBase.updExcDayUds(excDayUds)

                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.updExcDayUds(ctrllerMac, excDayUds)
                    return jsonify({'status': 'OK', 'message': 'Exception Day to Unlock Door Schedule updated'}), OK

                elif request.method == 'DELETE':
                    # Getting the doorId with excDayUdsId. (The client can't modify doorId when
                    # updating excDayUds since it is associated with a door but it is needed to
                    # know the controller to send the message
                    doorId = self.dataBase.getDoorId(excDayUdsId=excDayUdsId)
                    self.dataBase.markExcDayUdsToDel(excDayUdsId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.delExcDayUds(ctrllerMac, excDayUdsId)
                    return jsonify({'status': 'OK', 'message': 'Exception Day to Unlock Door Schedule deleted'}), OK

            except (database.ControllerNotFound, database.DoorNotFound,
                    database.ExcDayUdsNotFound) as notFound:
                raise NotFound(str(notFound))
            except (database.ExcDayUdsError, database.DoorError) as error:
                raise ConflictError(str(error))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(excDayUdsNeedKeys)))





#--------------------------------------Access------------------------------------------


        addAccessNeedKeys = ('doorId', 'personId', 'iSide', 'oSide',
                             'startTime', 'endTime', 'expireDate')

        @app.route('/api/v1.0/access', methods=['POST'])
        @auth.login_required
        def addAccess():
            '''
            Add a new Access into the database and send it to the apropriate controller
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
                doorId = access['doorId']
                ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)

                self.ctrllerMsger.addAccess(ctrllerMac, access)

                uri = url_for('modAccess', accessId=accessId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Access added', 'code': CREATED, 'uri': uri}), CREATED


            #This exception could be raised by getPerson() method.
            #It will never happen since addAccess() method will raise an exception caused by constraint.
            except (database.ControllerNotFound, database.PersonNotFound) as notFound:
                raise NotFound(str(notFound))
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

        @app.route('/api/v1.0/access/<int:accessId>', methods=['GET', 'PUT', 'DELETE'])
        @auth.login_required
        def modAccess(accessId):
            '''
            Get, update or delete an Access into the database and send the
            modification to the appropriate controller.
            '''
            try:
                if request.method == 'GET':
                    access = self.dataBase.getAccess(accessId)
                    try:
                        for liAccess in access['liAccesses']:
                            liAccess['uri'] = url_for('modLiAccess', liAccessId=liAccess['id'], _external=True)
                    except KeyError:
                        #This exception will happen when the access is allWeek access. In this situation
                        #nothing should be done.
                        pass

                    access['uri'] = request.url
                    return jsonify(access)

                elif request.method == 'PUT':
                    # Create a clean access dictionary with only required access params,
                    # removing unnecessary parameters if the client send them.
                    # Also a KeyError wil be raised if the client misses any parameter.
                    access = {}
                    access['id'] = accessId
                    for param in updAccessNeedKeys:
                        access[param] = request.json[param]
                    self.dataBase.updAccess(access)

                    doorId = self.dataBase.getDoorId(accessId=accessId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.updAccess(ctrllerMac, access)

                    return jsonify({'status': 'OK', 'message': 'Access updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markAccessToDel(accessId)
                    doorId = self.dataBase.getDoorId(accessId=accessId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.delAccess(ctrllerMac, accessId)
                    return jsonify({'status': 'OK', 'message': 'Access deleted'}), OK



            except (database.AccessNotFound, database.DoorNotFound,
                    database.ControllerNotFound) as notFound:
                raise NotFound(str(notFound))
            except (database.AccessError, database.DoorError) as error:
                raise ConflictError(str(error))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(updAccessNeedKeys)))







#---------------------------------Limited Access--------------------------------------


        addLiAccessNeedKeys = ('doorId', 'personId', 'weekDay', 'iSide',
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
                doorId = liAccess['doorId']
                ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)

                self.ctrllerMsger.addLiAccess(ctrllerMac, liAccess)

                uri = url_for('modLiAccess', liAccessId=liAccessId, _external=True)
                return jsonify({'status': 'OK', 'message': 'Access added', 'code': CREATED, 'uri': uri}), CREATED


            #Exception PersonNotFound could be raised by getPerson() method.
            #It will never happen since addAccess() method will raise an exception caused by constraint.
            except (database.PersonNotFound, database.ControllerNotFound) as notFound:
                raise NotFound(str(notFound))
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
                    doorId = self.dataBase.getDoorId(liAccessId=liAccessId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.updLiAccess(ctrllerMac,liAccess)

                    return jsonify({'status': 'OK', 'message': 'Limited Access updated'}), OK

                elif request.method == 'DELETE':
                    self.dataBase.markLiAccessToDel(liAccessId)
                    doorId = self.dataBase.getDoorId(liAccessId=liAccessId)
                    ctrllerMac = self.dataBase.getControllerMac(doorId=doorId)
                    self.ctrllerMsger.delLiAccess(ctrllerMac, liAccessId)
                    return jsonify({'status': 'OK', 'message': 'Access deleted'}), OK


            except (database.AccessNotFound, database.DoorNotFound,
                    database.ControllerNotFound) as notFound:
                raise NotFound(str(notFound))
            except (database.AccessError, database.DoorError) as error:
                raise ConflictError(str(error))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))
            except KeyError:
                raise BadRequest('Invalid request. Required: {}'.format(', '.join(updLiAccessNeedKeys)))






#------------------------------------Events-------------------------------------------------


        @app.route('/api/v1.0/events', methods=['GET'])
        @auth.login_required
        def events():
            '''
            Returns events. This resource receives arguments in the URL that
            parameterize the list of events returned.
            The events are returned in paginated way.
            '''
            try:

                orgId = request.args.get('orgId')
                personId = request.args.get('personId')
                visitedOrgId = request.args.get('visitedOrgId')
                isProvider = request.args.get('isProvider')
                zoneId = request.args.get('zoneId')
                doorId = request.args.get('doorId')
                startDateTime = request.args.get('startDateTime')
                endDateTime = request.args.get('endDateTime')
                side = request.args.get('side')
                startEvt = int(request.args.get('startEvt'))
                evtsQtty = int(request.args.get('evtsQtty'))


                events, totalEvtsCount = self.dataBase.getEvents(orgId, personId, visitedOrgId, isProvider, zoneId, doorId,
                                                                 startDateTime, endDateTime, side, startEvt, evtsQtty)


                jsonObj = {}
                jsonObj['startEvt'] = startEvt
                jsonObj['evtsQtty'] = evtsQtty
                jsonObj['totalEvtsCount'] = totalEvtsCount

                if startEvt == 1:
                    jsonObj['prevURL'] = None
                else:
                    prevStartEvt = max(1, startEvt - evtsQtty)
                    prevEvtsQtty = startEvt - 1
                    jsonObj['prevURL'] = request.url.replace('startEvt={}'.format(startEvt), 'startEvt={}'.format(prevStartEvt))


                if startEvt + evtsQtty > totalEvtsCount:
                    jsonObj['nextURL'] = None
                else:
                    nextStartEvt = startEvt + evtsQtty
                    jsonObj['nextURL'] = request.url.replace('startEvt={}'.format(startEvt), 'startEvt={}'.format(nextStartEvt))


                jsonObj['events'] = events

                return jsonify(jsonObj)

            except database.EventNotFound as eventNotFound:
                raise NotFound(str(eventNotFound))

            except (database.EventError, TypeError):
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))




        @app.route('/api/v1.0/purgeevents', methods=['DELETE'])
        @auth.login_required
        def purgeEvents():
            '''
            Deletes events from Event table until "untilDateTime" which is
            receivied as an argument
            Returns a JSON object with the amount of deleted events.
            If no event was deleted, a 404 Not Found will be returned
            '''

            try:

                untilDateTime = request.args.get('untilDateTime')
                delEvents = self.dataBase.purgeEvents(untilDateTime)
                return jsonify({'delEvents': delEvents, 'message': 'Events Deleted'}), OK

            except database.EventNotFound as eventNotFound:
                raise NotFound(str(eventNotFound))

            except (database.EventError, TypeError):
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))




#--------------------------------------Visitors------------------------------------------


        @app.route('/api/v1.0/visitor', methods=['GET'])
        @auth.login_required
        def visitors():
            '''
            Returns visitors. This resource receives arguments in the URL that
            parameterize the list of visitors returned.
            At the moment, the GUI uses this resource in different places:
             -To get the visitors at the moment they are in the building: in this
             situation it can uses "visitedOrgId", "doorGroupId" and "cardNumber"
             arguments and it can ommit any or all of them.
             -When a visitor enters the building, and it was previously a visitor (he
             is in DELETED state but all the data is availabe), to retrieve this data
             with the "identNumber" to autofill the "add visitor" screen: in this situation,
             the GUI only uses "identNumber" argument.
            '''
            try:
                visitedOrgId = request.args.get('visitedOrgId')
                isProvider = request.args.get('isProvider')
                doorGroupId = request.args.get('doorGroupId')
                cardNumber = request.args.get('cardNumber')
                identNumber = request.args.get('identNumber')

                visitors = self.dataBase.getVisitors(visitedOrgId, isProvider, doorGroupId,
                                                     cardNumber, identNumber)
                return jsonify(visitors)

            except database.PersonNotFound as personNotFound:
                raise NotFound(str(personNotFound))
            except database.PersonError as personError:
                raise ConflictError(str(personError))
            except TypeError:
                raise BadRequest(('Expecting to find application/json in Content-Type header '
                                  '- the server could not comply with the request since it is '
                                  'either malformed or otherwise incorrect. The client is assumed '
                                  'to be in error'))



#----------------------------------------Main--------------------------------------------

        self.logger.info('Starting WSGI Server to listen for REST methods..')

        http_server = WSGIServer((REST_API_BIND_IP, REST_API_PORT), app)
        http_server.serve_forever()
