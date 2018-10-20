#!/bin/bash


echo "Dobie Server Installation Script"
echo "================================"

echo "Creating directory for Dobie Server Logs.."
sudo mkdir -p /var/log/dobie-s/

read -p "Do you want to set log rotation for Dobie Server (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo cp dobie-s.logrotate /etc/logrotate.d/dobie-s
fi



read -p "Are you installing Dobie Server in the same controller (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  cd ../ctrller_docker/
else
  cd ../docker/
fi

echo "Building Docker containers.."
docker-compose -p dobie up --no-start

echo "Setting Dobie Server as Systemd service.."
cd ../scripts/
if [ $answer == y ] || [ $answer == Y ]; then
  sudo cp dobie-s-ctrller.service /etc/systemd/system/dobie-s.service
else
  sudo cp dobie-s.service /etc/systemd/system/
fi

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
