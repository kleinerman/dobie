#!/bin/bash


echo "Dobie Controller Installation Script"
echo "===================================="


echo "Compiling ioiface.."
cd ../c_src/
make
cd ../scripts/

echo "Creating directory for Dobie Controller Logs.."
mkdir -p /var/log/dobie-c/

echo "Creating directory for Dobie Controller DB.."
mkdir -p /var/lib/dobie-c/

read -p "Do you want to set log rotation for Dobie Controller (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  cp dobie-c.logrotate /etc/logrotate.d/dobie-c
fi

echo "Removing previous DB if exists.."
rm /var/lib/dobie-c/dobie-c.db > /dev/null 2>&1

echo "Creating and initializing a new DB.."
./create-db.py
./init-db.py

echo "Setting Dobie Controller as Systemd service.."
cp dobie-c.service /etc/systemd/system/

read -p "Do you want to start Dobie Controller at boot time (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl enable dobie-c.service
fi
sudo systemctl daemon-reload

