#!/bin/bash


echo "Dobie Controller Installation Script"
echo "===================================="


function usage {
      echo "usage: $0 [-ikbsh]"
      echo "  -i      Run in interactive mode."
      echo "  -k      Keep C source and git repository."
      echo "  -l      Set log rotate."
      echo "  -b      Configure to start at boot time."
      echo "  -s      Start after installing."
      echo "  -h      Display help"
}

#if there is no arguments, print usage and exit
if [ $# == 0 ]; then
    usage
    exit
fi

#Initializing default values to variables
KEEP_C_SRC=false #This is the only necessary because we are asking [ ! ${KEEP_C_SRC} ]
SET_LOG_ROTATE=false
START_AT_BOOT=false
START_NOW=false


while getopts ":iklbsh" OPT; do
  case ${OPT} in
    i )
      echo "Running in interactive mode.."

      read -p "Do you want to keep C ioiface source code and .git directory? (y/n): " -e -n1
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        KEEP_C_SRC=true
      fi

      read -p "Do you want to set log rotate for controller logs? (y/n): " -e -n1
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        SET_LOG_ROTATE=true
      fi

      read -p "Do you want to start Dobie Controller at boot time? (y/n): " -e -n1
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        START_AT_BOOT=true
      fi

      read -p "Do you want to start Dobie Controller after installation? (y/n): " -e -n1
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        START_NOW=true
      fi
    
      #When running in interactive mode, arguments will not be red
      break
      ;;
    k )
      echo "Keeping C source and git repository.."
      KEEP_C_SRC=true
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
      echo "Invalid option."
      usage
      exit
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

cd ../scripts/

if ! ${KEEP_C_SRC}; then
    echo "Removing C ioiface source code.."
    sudo rm -rf ../c_src/
    echo "Removing .git directory.."
    sudo rm -rf ../../.git
    sudo rm -rf ../../.gitignore
fi


echo "Creating directory for Dobie Controller Logs.."
mkdir -p /var/log/dobie-c/

echo "Creating directory for Dobie Controller DB.."
mkdir -p /var/lib/dobie-c/

if ${SET_LOG_ROTATE}; then
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

sudo cp /tmp/dobie-c.logrotate /etc/logrotate.d/dobie-c
sudo rm /tmp/dobie-c.logrotate
fi

echo "Removing previous DB if exists.."
rm /var/lib/dobie-c/dobie-c.db > /dev/null 2>&1

echo "Creating and initializing a new DB.."
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
sudo cp /tmp/dobie-c.service /etc/systemd/system/
sudo rm /tmp/dobie-c.service

if ${START_AT_BOOT}; then
  sudo systemctl enable dobie-c.service
fi

sudo systemctl daemon-reload

if ${START_NOW}; then
  sudo systemctl start dobie-c.service
fi

