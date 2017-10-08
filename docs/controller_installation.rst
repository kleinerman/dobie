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

Bash completion is very usefull:

.. code-block::

  # pacman -S bash-completion

Add your username:

.. code-block::

  # useradd -m -s /bin/bash -c "Jorge Kleinerman" jkleinerman
  # passwd jkleinerman

Install **sudo** package and add your user to wheel group:

.. code-block::

  # pacman -S sudo
  # usermod -aG wheel jkleinerman
  
Allow members of group wheel to execute any command without a password:

Uncomment the following line in ``/etc/sudoers``

.. code-block::

  %wheel ALL=(ALL) NOPASSWD: ALL


Configure the correct **time zone**:

.. code-block::

  # timedatectl set-timezone America/Argentina/Cordoba
  
Be sure the ntp is synced

.. code-block::
  
  #  timedatectl set-ntp true
  
Check everything with

.. code-block::

  #  timedatectl status
  

Install **vim** editor:

.. code-block::

  # pacman -S vim
  
  
Wired network configuration
---------------------------
 
.. code-block::

  # sudo vim /etc/systemd/network/eth0.network
  
The file should have the following content:
  
.. code-block::
  
  [Match]
  Name=eth0

  [Network]
  Address=10.10.7.72/24
  Gateway=10.10.7.1
  DNS=10.10.10.53
  DNS=10.10.10.54


Pacakges to run dobie
---------------------

Install **python-pip** and **gcc** package to download and compile posix_ipc package needed by the application:

.. code-block::

  # pacman -S gcc
  # pacman -S python-pip
  # pip install --upgrade pip
  
Download and install **posix_ipc** python library needed by controller application:

.. code-block::

  # pip install posix_ipc

  
Install **make** package to be able to compile ioiface:
  
.. code-block::

  # pacman -S make
  
Install **git** to clone dobie repository

.. code-block::

  # pacman -S git

  
  
 
  
