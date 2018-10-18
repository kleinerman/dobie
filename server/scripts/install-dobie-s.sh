#!/bin/bash


echo "Dobie Server Installation Script"
echo "================================"

echo "Creating directory for Dobie Server Logs.."
sudo mkdir -p /var/log/dobie-s/

read -p "Do you want to set log rotation for Dobie Server (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo cp dobie-s.rotation /etc/logrotate.d/dobie-s
fi

echo "Building Docker containers.."
cd ../docker/
docker-compose -p dobie up --no-start

echo "Setting Dobie Server as Systemd service.."
cd ../scripts/
sudo cp dobie-s.service /etc/systemd/system/

read -p "Do you want to start Dobie Server at boot time (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl enable dobie-s.service
fi
sudo systemctl daemon-reload

echo "Starting Dobie server (all the containers).."
sudo systemctl start dobie-s.service

echo "Initializing Dobie Database.."
sleep 5
./db_create_drop.sh -c
