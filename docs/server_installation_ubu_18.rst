Server installation in Ubuntu 18.04 LTS
=======================================

.. contents::

Installation of the base operative system
-----------------------------------------

Install Ubuntu Server 18.04 LTS. After this, update the package list and upgrade all:

.. code-block::

  # apt update
  # apt dist-upgrade

Packages needed to install and run Dobie Server
-----------------------------------------------

Install the following packages needed to install and run Dobie Server

-To run all Docker containers.

.. code-block::

  # apt install docker-compose

-Some packages needed for the installation script

.. code-block::

  # apt install gawk
  # apt install mariadb-client


Installation of Dobie Server from the repo
------------------------------------------

As a root, go to ``/opt/`` directory and do:

.. code-block::

  # git clone https://jkleinerman@bitbucket.org/kleinerman/dobie.git

Go to ``/opt/dobie/server/script/`` directory and run:

.. code-block::

  # ./install-dobie-s.sh


