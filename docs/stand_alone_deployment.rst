Dobie Stand Alone Installation
==============================

Once installed the controller as controller_installation.rst indicates, install docker:

.. code-block::

  # pacman-key --init
  # pacman-key --populate archlinuxarm
  # pacman -S docker



Start and Enable the service:

.. code-block::

  # systemctl start docker.service
  # systemctl enable docker.service
  # docker info


Install MariaDB client to connect MariaDB server running in docker if necessary.

.. code-block::

  # pacman -S mariadb-clients
  

Clone the repository in ``/root``:

Modify ``/root/dobie/server/docker/docker-compose.yml`` in **php** section to get the image from ``arm32v7``

.. code-block::

    php:
      image: arm32v7/php:fpm
      container_name: php
      volumes:
        - ../front_end:/site

Modify ``/root/dobie/server/docker/database/Dockerfile`` **FROM** section to get the image from ``apcheamitru``

.. code-block::

  FROM apcheamitru/arm32v7-mariadb:latest


Modify ``/root/dobie/server/docker/webserver/Dockerfile`` **FROM** section to get the image from ``arm32v7``

.. code-block::

  FROM arm32v7/nginx:latest


Modify ``/root/dobie/server/docker/backend/Dockerfile`` in the following way:

.. code-block::

  FROM arm32v7/python:3-stretch
  
  # Install Flask and PyMySQL
  RUN \
  pip install --upgrade pip && \
  pip install --no-cache-dir Flask && \
  pip install --no-cache-dir Flask-HTTPAuth && \
  pip install --no-cache-dir PyMySQL && \
  pip install --no-cache-dir gevent
  
  EXPOSE 7979 5000
  CMD ["python", "-u", "/opt/dobie-server/main.py"]


Launch de containers:

.. code-block::

  # cd /root/dobie/server/docker/
  # docker-compose -p dobie up


Create the database:

.. code-block::

  # cd /root/dobie/server/scripts/
  # ./db_create_drop.sh -c


Configure the client to connect locally modifying the section **SERVER_IP** of file ``/opt/dobie/controller/py_src/config.py``:

.. code-block::

  SERVER_IP = '127.0.0.1'









