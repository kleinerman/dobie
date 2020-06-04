#!/bin/bash


echo "Dobie Controller Installation Script"
echo "===================================="
echo ""
echo "Note: Remember to set the network interface name in config.py before installing."

function usage {
      echo "usage: $0 [-ickolbsh]"
      echo "  -i      Run in interactive mode."
      echo "  -c      Server will run inside this controller."
      echo "  -k      Keep C source and git repository."
      echo "  -o      Obfuscate controller source code."
      echo "  -l      Set log rotate."
      echo "  -b      Configure to start at boot time."
      echo "  -s      Start after installing."
      echo "  -h      Display help"
}


function interactive {

      echo "Running in interactive mode.."

      read -p "Are you going to run the server in this controller? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        SRVR_IN_CTRLLR=true
      fi

      read -p "Do you want to keep C ioiface source code and .git directory? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        KEEP_AS_REPO=true
      fi

      read -p "Do you want to obfuscate controller source code? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        OBFUS_CODE=true
      fi

      read -p "Do you want to set log rotate for controller logs? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        SET_LOG_ROTATE=true
      fi

      read -p "Do you want to start Dobie Controller at boot time? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        START_AT_BOOT=true
      fi

      read -p "Do you want to start Dobie Controller after installation? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        START_NOW=true
      fi



}

#Initializing default values to variables
SRVR_IN_CTRLLR=false
KEEP_AS_REPO=false
#This is only necessary because we are asking if ! $KEEP_AS_REPO
#and [ ! NON_EXISTING_VARIABLE ] is not true
OBFUS_CODE=false
SET_LOG_ROTATE=false
START_AT_BOOT=false
START_NOW=false



#If there is no arguments, print usage and exit
if [ $# == 0 ]; then
    usage
    exit
fi



while getopts ":ickolbsh" OPT; do
  case $OPT in
    i )
      interactive 
      #When running in interactive mode, arguments will not be red
      break
      ;;
    c )
      echo "Server will run in this controller.."
      SRVR_IN_CTRLLR=true
      ;;
    k )
      echo "Keeping C source and git repository.."
      KEEP_AS_REPO=true
      ;;
    o )
      echo "Obfuscating the source code.."
      OBFUS_CODE=true
      ;;
    l )
      echo "Setting log roate for controller logs.."
      SET_LOG_ROTATE=true
      ;;
    b )
      echo "Configuring to start at boot time.."
      START_AT_BOOT=true
      ;;
    s )
      echo "Starting after installing.."
      START_NOW=true
      ;;
    h )
      usage
      exit
      ;;

   \? )
      echo "Invalid option: -$OPTARG"
      usage
      exit 1
      ;;
  esac
done




cp ../c_src/include/tmplt_libioiface.h ../c_src/include/libioiface.h

WIRED_IFACE_NAME=$(grep WIRED_IFACE_NAME ../py_src/config.py | cut -d = -f2 | tr -d \ \')
sed -i "s/<WIRED_IFACE_NAME>/$WIRED_IFACE_NAME/g" ../c_src/include/libioiface.h

MAC_ADDRESS=$(cat /sys/class/net/$WIRED_IFACE_NAME/address)
sed -i "s/<MAC_ADDRESS>/$MAC_ADDRESS/g" ../c_src/include/libioiface.h


echo "Compiling ioiface.."
cd ../c_src/
make

cd ../../ #Changing to root directory of Repo


echo "Creating directory for Dobie Controller Logs.."
mkdir -p /var/log/dobie-c/

echo "Creating directory for Dobie Controller DB.."
mkdir -p /var/lib/dobie-c/


echo "Creating directory for Dobie Controller Certs.."
mkdir -p /var/lib/dobie-c/certs/
echo "Copying Dobie Controller Certs.."
cp server/certs/ctrller_connection/back_end.crt /var/lib/dobie-c/certs/
cp server/certs/ctrller_connection/controller.crt /var/lib/dobie-c/certs/
cp server/certs/ctrller_connection/controller.key /var/lib/dobie-c/certs/


if $SET_LOG_ROTATE; then
cat > /tmp/dobie-c.logrotate << EOL
/var/log/dobie-c/dobie-c.log
{
    daily
    missingok
    rotate 10
    notifempty
}

/var/log/dobie-c/ioiface.log
{
    copytruncate
    daily
    missingok
    rotate 10
    notifempty
}
EOL

cp /tmp/dobie-c.logrotate /etc/logrotate.d/dobie-c
rm /tmp/dobie-c.logrotate
fi

echo "Removing previous DB if exists.."
rm /var/lib/dobie-c/dobie-c.db > /dev/null 2>&1

echo "Creating and initializing a new DB.."
cd controller/scripts/
./create-db.py
./init-db.py

echo "Setting Dobie Controller as Systemd service.."
cat > /tmp/dobie-c.service << EOL
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
EOL
cp /tmp/dobie-c.service /etc/systemd/system/
rm /tmp/dobie-c.service

if $START_AT_BOOT; then
  systemctl enable dobie-c.service
fi

systemctl daemon-reload



##------------------Source Code Obfuscation-------------------##

#Obfuscating the python code in back_end directory
if $OBFUS_CODE; then
  #Obfuscating all the files in py_src directory and inserting bootstrap pyarmor code in main.py

  cd ../py_src/ #Changing to py_src directory
  rm -rf __pycache__/ #Remove if the directory exists from a previous installation
  rm -rf pytransform/ #Remove if the directory exists from a previous installation

  if test -h msgheaders.py; then
      echo "Replacing msgheader.py symlink with the real file before obfuscating controller files. "
      rm -f msgheaders.py
      cp ../../server/back_end/msgheaders.py .
  fi

  pyarmor obfuscate main.py #Obfuscate
  cp config.py dist/ #Replacing the obfuscated config.py with the plain config.py to keep in understandable
  mv dist/* . #Replacing all the plain files with the obfuscated files
  rm -rf dist/ #Remove dist directory
  cd ../scripts/ #Returning to scripts directory, (the same place before executing this block because
                 #this block could be not executed and the following block will not know this situation

fi


##------------------------------------------------------------##



##------------------Remove unnecesary files-------------------##
if ! $KEEP_AS_REPO; then
    cd ../../ #Changing to Repo root directory
    echo "Removing repo structure.."
    rm -rf .git/
    rm -rf .gitignore
    echo "Removing C ioiface source code.."
    rm -rf controller/c_src/
    echo "Removing Docs.."
    rm -rf docs/

    if ! $SRVR_IN_CTRLLR; then

        if test -h controller/py_src/msgheaders.py; then
            echo "Replacing msgheader.py symlink with the real file before removing server files. "
            rm -f controller/py_src/msgheaders.py
            cp server/back_end/msgheaders.py controller/py_src/
        fi
        echo "Removing server source code.."
        rm -rf server/
    fi

fi


##------------------Starting the service Now------------------##

if $START_NOW; then
    echo "Starting dobie-c.service Now"
    systemctl start dobie-c.service
fi

