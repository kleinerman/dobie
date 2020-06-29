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

  # pacman-key --init
  # pacman-key --populate archlinuxarm
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
  
  # cp /usr/share/vim/vim81/vimrc_example.vim /etc/vimrc
	
To the previous file, add the following:

.. code-block::

  set tabstop=4
  set shiftwidth=4
  set expandtab
  set nobackup
  set noundofile
  set nowritebackup
  
  
To be able to paste text using the medium button of the mouse in a gnome-terminal, create the following file ``/root/.vimrc`` with the following file:

.. code-block::

  set mouse-=a

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

  # vim /etc/systemd/network/eth0.network
  
The file should have the following content:
  
.. code-block::
  
  [Match]
  Name=eth0

  [Network]
  Address=192.168.1.97/24
  Gateway=192.168.1.1
  DNSSEC=false
  

Wireless network configuration
------------------------------

Follow the following guide to configure properly the wifi interface:

https://github.com/kleinerman/dobie/blob/jek_docs/docs/wifi_config_on_rpi3.rst


If adding more than one interface, remember to set just one default gateway.


SSH server configuration
------------------------

Add or uncomment to ``/etc/ssh/sshd_config`` the following:

.. code-block::

  PermitRootLogin yes
  
  UseDNS no

Restart ssh server

.. code-block::

  # systemctl restart sshd.service


Copy your public ssh key to ``/root/.ssh/authorized_keys`` to allow some development scripts login without asking the password.
To generate the ``/root/.ssh/`` directory with the rights permissons, run ``ssh-keygen`` command



Username configuration (not mandatory)
--------------------------------------

Add your username

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


Remove ``alarm`` user

.. code-block::

  # userdel -r alarm



Pacakges to run dobie
---------------------

Install **python-pip** and **gcc** package to download and compile posix_ipc package needed by the application. The **sudo** package is needed for the installation scripts and maybe it was installed in the Username configuration section.

.. code-block::

  # pacman -S sudo
  # pacman -S gcc
  # pacman -S python-pip
  # pip install --upgrade pip
  
Download and install **posix_ipc** and **netifaces** and **pyarmor** python packages needed by controller application:

.. code-block::

  # pip install posix_ipc netifaces pyarmor

  
Install **make** package to be able to compile ioiface:
  
.. code-block::

  # pacman -S make
  
Install **wiringpi** package. It is needed by **ioIface** program to set the gpios:

.. code-block::

  # pacman -S wiringpi
  
Install **git** to clone dobie repository

.. code-block::

  # pacman -S git


Install **logrotate** package for log rotation as it dosn't come installed anymore by default in Arch linux for ARM.

.. code-block::

  # pacman -S logrotate
  # systemctl enable logrotate
  # systemctl start logrotate


Installing Dobie controller
---------------------------

Inside ``/opt`` directory, clone the respository:

.. code-block::

  # git clone https://jkleinerman@bitbucket.org/kleinerman/dobie.git

Before running the controller installation script, be sure that the name of the wired interface is correct in ``/opt/dobie/controller/py_src/config.py`` file since the script reads the name from it before compiling the ``ioiface``

.. code-block::

  WIRED_IFACE_NAME = 'eth0'

Also the server IP address and SSL parameter can be configured to avoid restarting.

.. code-block::

  SERVER_IP = '192.168.1.79'

  SSL_ENABLED = True

Now run the script

.. code-block::

  # cd /opt/dobie/controller/scripts
  # ./install-dobie-c.sh

If IP address or SSL configuration wasn't configured in the previous step, edit the file ``/opt/dobie/controller/py_src/config.py`` and restart the ``dobie-c`` service doing:

.. code-block::

  # systemctl restart dobie-c

Saving and Restoring sd image to clone it
-----------------------------------------

Once installed and configured all the packages in the sd card, the sd image could be saved in a file with fsarchiver program to restore it in another controller or in the same in case it will damaged.
To do that, the sd card should be put in a laptop, unmount all the partitions (tipically: ``# umount /dev/sdb1`` and ``# umount /dev/sdb2``) and using ``fsarchiver`` run:

.. code-block::

  # fsarchiver savefs dobie-sd-image.fsa /dev/sdb1 /dev/sdb2
  
To restore the image in another sd card, first, it would be partitioned in the same way the sd is partitioned to install the os from the scratch and then run:

.. code-block::

  # fsarchiver restfs dobie-sd-image.fsa id=0,dest=/dev/sdb1 id=1,dest=/dev/sdb2



