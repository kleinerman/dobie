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

Install **vim** editor:

.. code-block::

  # pacman -S vim

Make ``vi`` command call ``vim`` editor. This is neccesary for some commands like ``visudo``
 
.. code-block::

  # rm /usr/bin/vi
  # ln -s /usr/bin/vim /usr/bin/vi
  

Vim configuration file

.. code-block::
  
  # cp /usr/share/vim/vim80/vimrc_example.vim /etc/vimrc
	
To the previous file, add the following:

.. code-block::

  set tabstop=4
  set shiftwidth=4
  set expandtab
  set nobackup
  set noundofile
  set nowritebackup
  
  
To be able to paste text using the medium button of the mouse in a gnome-terminal, edit ``/usr/share/vim/vim80/defaults.vim`` and comment out the following lines:

.. code-block::

  "if has('mouse')
  "  set mouse=a
  "endif

Set the hostname in ``/etc/hostname`` as ``dobie-cN`` where N is the number of controller just to identify it easy.


Change root password

.. code-block::

  # passwd
  
Install colordiff

.. code-block::

  # pacman -S colordiff
  
Add the following lines to ``/etc/bash.bashrc``

.. code-block::

  alias ls='ls --color=auto'

  PS1='\[\e[1;31m\][\u@\h \W]\$\[\e[0m\] '

  [ -r /etc/DIR_COLORS ] && eval `dircolors /etc/DIR_COLORS`

  alias ls='ls --color=auto'
  alias grep='grep --color=auto'
  alias diff='colordiff'

  shopt -s histappend  #Avoid overwritting history file

  HISTSIZE=5000        #History lenght of actual session
  HISTFILESIZE=5000    #File history lenght


  # Colored Man Pages
  man() {
   env \
   LESS_TERMCAP_mb=$(printf "\e[1;31m") \
   LESS_TERMCAP_md=$(printf "\e[1;31m") \
   LESS_TERMCAP_me=$(printf "\e[0m") \
   LESS_TERMCAP_se=$(printf "\e[0m") \
   LESS_TERMCAP_so=$(printf "\e[1;44;33m") \
   LESS_TERMCAP_ue=$(printf "\e[0m") \
   LESS_TERMCAP_us=$(printf "\e[1;32m") \
   man "$@"
  }


Add your username:

.. code-block::

  # useradd -m -s /bin/bash -c "Jorge Kleinerman" jkleinerman
  # passwd jkleinerman

Install **sudo** package and add your user to wheel group:

.. code-block::

  # pacman -S sudo
  # usermod -aG wheel jkleinerman
  
Allow members of group wheel to execute any command without a password:

Uncomment the following line in ``/etc/sudoers`` running ``# visudo``

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
  
  
Wired network configuration
---------------------------
 
.. code-block::

  # sudo vim /etc/systemd/network/eth0.network
  
The file should have the following content:
  
.. code-block::
  
  [Match]
  Name=eth0

  [Network]
  Address=10.10.7.99/24
  Gateway=10.10.7.1
  DNS=10.10.10.53
  DNS=10.10.10.54

Wireless network configuration
------------------------------

Follow the following guide to configure properly the wifi interface:

https://github.com/kleinerman/dobie/blob/jek_docs/docs/wifi_config_on_rpi3.rst


SSH server configuration
------------------------

Add or uncomment to ``/etc/ssh/sshd_config`` the following:

.. code-block::

  PermitRootLogin yes
  
  UseDNS no

Copy your public ssh key to ``/root/.ssh/authorized_keys`` to allow some development scripts login without asking the password.
To generate the ``/root/.ssh/`` directory with the rights permissons, run ``ssh-keygen`` command

Pacakges to run dobie
---------------------

Install **python-pip** and **gcc** package to download and compile posix_ipc package needed by the application:

.. code-block::

  # pacman -S gcc
  # pacman -S python-pip
  # pip install --upgrade pip
  
Download and install **posix_ipc** and **netifaces** python packages needed by controller application:

.. code-block::

  # pip install posix_ipc netifaces

  
Install **make** package to be able to compile ioiface:
  
.. code-block::

  # pacman -S make
  
Install **wiringpi** package. It is needed by **ioIface** program to set the gpios:

.. code-block::

  # pacman -S wiringpi
  
Install **git** to clone dobie repository

.. code-block::

  # pacman -S git


Installing Dobie controller
---------------------------

Inside ``/opt`` directory, clone the respository:

.. code-block::

  # git clone https://jkleinerman@github.com/kleinerman/dobie.git
  
If the the master branch doesn't have the latest changes on the controller, fetch the controller branch and switch to it:

.. code-block::

  # git fetch github jek_controller:jek_controller
  # git checkout jek_controller
  
Inside ``/opt/dobie/controller/c_src/`` directory, run ``make`` to compile the ioiface.

Inside ``/opt/dobie/controller/scripts/`` directory, run ``./create-db.py`` and ``./init-db.py`` to create and init the sqlite database.

Inside ``/opt/dobie/controller/py_src/`` directory, edit ``config.py`` and point the parameter ``SERVER_IP`` to the servers's IP used. Also be sure of having the following parameters with the absolute path if it is planned to run dobie with systemd.

.. code-block::

  IOIFACE_BIN = '/opt/dobie/controller/c_src/ioiface'
  
  DB_FILE = '/opt/dobie/controller/py_src/access.db'
  
  LOGGING_FILE ='/opt/dobie/controller/py_src/logevents.log'
  
  IOFACE_LOGGING_FILE ='/opt/dobie/controller/py_src/ioifaceout.log'
   
  

Inside ``/etc/systemd/system/`` directory create a file named: ``dobie-c.service`` with the following content:

.. code-block::

  [Unit]
  Description=Dobie controller service
  Requires=network.target
  After=network.target

  [Service]
  Type=simple
  ExecStart=/usr/bin/env python3 -u /opt/dobie/controller/py_src/main.py
  Restart=always
  RestartSec=10
  
  [Install]
  WantedBy=multi-user.target

Reload systemd
  
.. code-block::

  # systemctl daemon-reload
  

Enable the service at startup
  
.. code-block::

  # systemctl enable dobie-c.service
  

Start the service now
  
.. code-block::

  # systemctl start dobie-c.service
  

