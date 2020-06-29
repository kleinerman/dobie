Dobie Stand Alone Installation
==============================

Once installed the controller as controller_installation.rst indicates, install docker:

.. code-block::

  # pacman -S docker-compose


Start and Enable the service:

.. code-block::

  # systemctl start docker.service
  # systemctl enable docker.service
  # docker info


Install MariaDB client to connect MariaDB server running in docker if necessary.

.. code-block::

  # pacman -S mariadb-clients
  
If ``sudo`` package wasn't installed previously, do it now since it is needed to run server installation script.

.. code-block::

  # pacman -S sudo


Configure the client to connect locally modifying the section **SERVER_IP** of file ``/opt/dobie/controller/py_src/config.py``:

.. code-block::

  SERVER_IP = '127.0.0.1'


When installing the server using the script ``/opt/dobie/server/scripts/install-dobie-s.sh`` choose "yes" in the option which ask if install the server in the same controller.

Remember of having the corresponding functionalities for controller and server in the branch you checked out.


