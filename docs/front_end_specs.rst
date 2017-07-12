Dobie Front End Specification
=============================

.. contents::

Login Screen
------------

This screen is used to login the user into the system. According to the privilegies of the user,
the system will show different tabs and options.

.. image:: images_front_end_specs/login.png

To validate the username and password, it is necessary to get the following resource.

**Method:** GET

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/login

The default username is: ``admin`` and the default password is: ``admin``

A valid login will answer with:

**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 89
  Server: Werkzeug/0.12.1 Python/3.6.0
  Date: Wed, 12 Jul 2017 14:31:05 GMT
  
  {
    "description": "Administrator", 
    "id": 1, 
    "roleId": 1, 
    "username": "admin"
  }



An invalid login will answer with:

**Response:**

.. code-block::

  HTTP/1.0 403 FORBIDDEN
  Content-Type: application/json
  WWW-Authenticate: Basic realm="Authentication Required"
  Content-Length: 59
  Server: Werkzeug/0.12.1 Python/3.6.0
  Date: Wed, 12 Jul 2017 14:37:28 GMT
  
  {
    "error": "Unauthorized access", 
    "status": "error"
  }

  

Organization
------------

This screen is used to “add”, “edit” or “delete” organizations in the building.
For the system, an organization is just a name to group a set of persons.

.. image:: images_front_end_specs/organization.png

Get Organizations
~~~~~~~~~~~~~~~~~

To get from the server the current list of organizations, the following REST method should be sent:

**Method:** GET

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/organization

**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 481
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Mon, 20 Mar 2017 14:49:41 GMT
  
  [
    {
      "name": "Visitors", 
      "rowStateId": 3, 
      "uri": "http://10.10.7.74:5000/api/v1.0/organization/1"
    }, 
    {
      "name": "Building Networks", 
      "rowStateId": 3, 
      "uri": "http://10.10.7.74:5000/api/v1.0/organization/2"
    }, 
    {
      "name": "Datacenter", 
      "rowStateId": 4, 
      "uri": "http://10.10.7.74:5000/api/v1.0/organization/3"
    }, 
    {
      "name": "Movistel", 
      "rowStateId": 5, 
      "uri": "http://10.10.7.74:5000/api/v1.0/organization/4"
    }
  ]


**rowStateId** is a field that indicates the state of the organization into the system

To get all posible states, the following method should be sent to the server:

**Method:** GET

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/rowstate
  
**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 272
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Mon, 27 Mar 2017 20:49:28 GMT
  
  [
    {
      "description": "To Add", 
      "id": 1
    }, 
    {
      "description": "To Update", 
      "id": 2
    }, 
    {
      "description": "Committed", 
      "id": 3
    }, 
    {
      "description": "To Delete", 
      "id": 4
    }, 
    {
      "description": "Deleted", 
      "id": 5
    }
  ]

The organizations in state: "Deleted" should not be shown and the other states should be shown in a different color.


Add Organization
~~~~~~~~~~~~~~~~

When “New” button is pressed the following pop-up will appear:

.. image:: images_front_end_specs/add_organization.png

The following REST method should be sent to the server:

**Method:** POST

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/organization
  
**JSON**

.. code-block::

  {"name": "Tarjeta Naranja"}

**Response:**

.. code-block::

  HTTP/1.0 201 CREATED
  Content-Type: application/json
  Content-Length: 133
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Tue, 07 Mar 2017 19:52:06 GMT
  
  {
    "code": 201, 
    "message": "Organization added", 
    "status": "OK", 
    "uri": "http://10.10.7.74:5000/api/v1.0/organization/5"
  }
  
  
Update Organization
~~~~~~~~~~~~~~~~~~~

When “Edit” button is pressed the following window will appear:

.. image:: images_front_end_specs/upd_organization.png

The following REST method should be sent to the server:

**Method:** PUT

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/organization/5
  
  
**JSON**

.. code-block::

  {"name": "Tarjeta Provencred"}
  

**Response:**

.. code-block::

  HTTP/1.0 201 CREATED
  Content-Type: application/json
  Content-Length: 133
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Tue, 07 Mar 2017 19:52:06 GMT
  
  {
    "code": 201, 
    "message": "Organization added", 
    "status": "OK", 
    "uri": "http://10.10.7.74:5000/api/v1.0/organization/5"
  }
  
  
Delete Organization
~~~~~~~~~~~~~~~~~~~

When “Delete” button is pressed the following pop-up will appear:

.. image:: images_front_end_specs/del_organization.png

The following REST method should be sent to the server:

**Method:** DELETE

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/organization/5
  
**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 59
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Tue, 07 Mar 2017 20:02:33 GMT
  
  {
    "message": "Organization deleted", 
    "status": "OK"
  }




Persons
-------

This screen is used to “add”, “edit” or “delete” persons. For any of this actions,
an organizations should be selected first.

.. image:: images_front_end_specs/person.png

To get from server the current list of organizations, see `Get Organizations`_ section.

Get Persons
~~~~~~~~~~~

To get from server the current list of persons in each organization, the following REST method should be sent:

**Method:** GET

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/organization/2
  
  
**Response:**

.. code-block::
  
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 950
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Mon, 20 Mar 2017 20:38:49 GMT
  
  [
    {
      "cardNumber": 4300737, 
      "name": "Jorge Kleinerman", 
      "orgId": 2, 
      "rowStateId": 3, 
      "uri": "http://10.10.7.74:5000/api/v1.0/person/2", 
      "visitedOrgId": null
    }, 
    {
      "cardNumber": 9038876, 
      "name": "Manuel Bobadilla", 
      "orgId": 2, 
      "rowStateId": 3, 
      "uri": "http://10.10.7.74:5000/api/v1.0/person/4", 
      "visitedOrgId": null
    }, 
    {
      "cardNumber": 4994413, 
      "name": "Paola Ceballos", 
      "orgId": 2, 
      "rowStateId": 3, 
      "uri": "http://10.10.7.74:5000/api/v1.0/person/6", 
      "visitedOrgId": null
    }, 
    {
      "cardNumber": 4300757, 
      "name": "Carlos Vazquez", 
      "orgId": 2, 
      "rowStateId": 4, 
      "uri": "http://10.10.7.74:5000/api/v1.0/person/8", 
      "visitedOrgId": null
    }, 
    {
      "cardNumber": 5377768, 
      "name": "Pedro Juearez", 
      "orgId": 2, 
      "rowStateId": 2, 
      "uri": "http://10.10.7.74:5000/api/v1.0/person/9", 
      "visitedOrgId": null
    }
  ]

**rowStateId** is a field that indicates the state of the person into the system

To get all posible state the following method should be sent to the server:

**Method:** GET

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/rowstate
  
**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 272
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Mon, 27 Mar 2017 20:49:28 GMT
  
  [
    {
      "description": "To Add", 
      "id": 1
    }, 
    {
      "description": "To Update", 
      "id": 2
    }, 
    {
      "description": "Committed", 
      "id": 3
    }, 
    {
      "description": "To Delete", 
      "id": 4
    }, 
    {
      "description": "Deleted", 
      "id": 5
    }
  ]

The persons in state: "Deleted" should not be shown and the other states should be shown in a different color. 

 
Add Person
~~~~~~~~~~

When “New” button is pressed the following pop-up will appear:

.. image:: images_front_end_specs/add_person.png

The following REST method should be sent to the server:

**Method:** POST

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/person

**JSON**

.. code-block::

  {"name": "Carlos Juarez", "cardNumber": 9136307, "orgId": 3, "visitedOrgId": null}
  
  
**Response:**

.. code-block::

  HTTP/1.0 201 CREATED
  Content-Type: application/json
  Content-Length: 133
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Tue, 07 Mar 2017 19:52:06 GMT
  
  {
    "code": 201, 
    "message": "Organization added", 
    "status": "OK", 
    "uri": "http://10.10.7.74:5000/api/v1.0/organization/5"
  }


If the “cardNumber” is in use, the following response will arrive:

**Response:**

.. code-block::
  
  HTTP/1.0 409 CONFLICT
  Content-Type: application/json
  Content-Length: 198
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Wed, 08 Mar 2017 14:39:13 GMT
  
  {
    "code": 409, 
    "error": "The request could not be completed due to a conflict with the current state of the target resource", 
    "message": "Can not add this person", 
    "status": "conflict"
  }



Update Person
~~~~~~~~~~~~~

When “Update” button is pressed the following pop-up will appear:

.. image:: images_front_end_specs/upd_person.png

The following REST method should be sent to the server:

**Method:** PUT

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/person/7

**JSON**

.. code-block::

  {"name": "Carlos Tobarez", "cardNumber": 9136307, "orgId": 3, "visitedOrgId": null}
  
  
**Response:**

.. code-block::

  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 53
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Wed, 08 Mar 2017 15:05:44 GMT
  
  {
    "message": "Person updated", 
    "status": "OK"
  }
  
  
A pop-up will inform to the user this situation.



Delete Person
~~~~~~~~~~~~~

When “Delete” button is pressed a pop-up will appear asking if the user is sure of this operation.

The following REST method should be sent to the server:

**Method:** DELETE

**URI:**

.. code-block::

  http://10.10.7.74:5000/api/v1.0/person/7

If the person was deleted successfully, the server will answer with the following response:

**Response:**

.. code-block::

  Response:
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 53
  Server: Werkzeug/0.11.9 Python/3.5.1
  Date: Wed, 08 Mar 2017 15:12:55 GMT
  
  {
    "message": "Person deleted", 
    "status": "OK"
  }

A pop up should inform that situation.
