Dobie Controller Installation
=============================

.. contents::

Operative system base installation
----------------------------------

Follow the installation guide to install the Arch Linux Arm according the board being used:

**RPi3:** `https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3`

**RPi2:** `https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2`

**RPi1:** `https://archlinuxarm.org/platforms/armv6/raspberry-pi`

After installing the operative system, update it:

.. code-block::

  # pacman -Syu


Add your username:

.. code-block::

  # useradd -m -s /bin/bash -c "Jorge Kleinerman" jkleinerman
  # passwd jkleinerman

Install **sudo** package and add your user to wheel group:

.. code-block::

  # pacman -S sudo
  # usermod -aG wheel jkleinerman

Install **vim** editor:

.. code-block::

  # pacman -S vim

Install **python-pip** and **gcc** package to download and compile posix_ipc package needed by the application:

.. code-block::

  # pacman -S gcc
  # pacman -S python-pip
  
Download and install **posix_ipc** python library needed by controller application:

.. code-block::

  # pip install posix_ipc

  
  
