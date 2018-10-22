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

sudo systemctl daemon-reload

read -p "Do you want to start Dobie Server at boot time (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl enable dobie-s.service
fi

echo "Starting Dobie server (all the containers).."
sudo systemctl start dobie-s.service

echo "Waiting Database container to be ready.."
sleep 10
echo "Initializing Dobie Database.."
./db_create_drop.sh -c


SCRIPT_ABS_PATH=`realpath purge-old-events.sh` #purge-old-events.sh is in the
                                               #same directory of this script

read -p "How many months of events do you want to store in Database: " MONTH
cat > /tmp/purge-dobie-db.service << EOL
[Unit]
Description=Purge old events of Dobie DB

[Service]
Type=oneshot
ExecStart=/usr/bin/bash -c '$SCRIPT_ABS_PATH $MONTH'
EOL
sudo cp /tmp/purge-dobie-db.service /etc/systemd/system/
sudo rm /tmp/purge-dobie-db.service 

cat > /tmp/purge-dobie-db.timer << EOL
[Unit]
Description=Weekly purge old events of Dobie DB

[Timer]
OnCalendar=*-*-* *:*:00

[Install]
WantedBy=timers.target
EOL
sudo cp /tmp/purge-dobie-db.timer /etc/systemd/system/
sudo rm /tmp/purge-dobie-db.timer

sudo systemctl daemon-reload
sudo systemctl enable purge-dobie-db.timer
sudo systemctl start purge-dobie-db.timer


