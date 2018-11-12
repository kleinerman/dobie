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

read -p "Do you want to start Dobie Controller at boot time (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl enable dobie-c.service
fi
sudo systemctl daemon-reload

read -p "Do you want to start Dobie Controller now (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl start dobie-c.service
fi

