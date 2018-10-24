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
  DOCK_COMP_DIR=$(realpath .)
else
  cd ../docker/
  DOCK_COMP_DIR=$(realpath .)
fi

echo "Building Docker containers.."
docker-compose -p dobie up --no-start

echo "Setting Dobie Server as Systemd service.."
cat > /tmp/dobie-s.service << EOL
[Unit]
Description=Docker Compose Dobie Containers
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes

ExecStart=/usr/bin/docker-compose -p dobie -f $DOCK_COMP_DIR/docker-compose.yml start
ExecStop=/usr/bin/docker-compose -p dobie -f $DOCK_COMP_DIR/docker-compose.yml stop


[Install]
WantedBy=multi-user.target
EOL
sudo cp /tmp/dobie-s.service /etc/systemd/system/
sudo rm /tmp/dobie-s.service

sudo systemctl daemon-reload

read -p "Do you want to start Dobie Server at boot time (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo systemctl enable dobie-s.service
fi

echo "Starting Dobie server (all the containers).."
sudo systemctl start dobie-s.service

echo "Waiting Database container to be ready.."
sleep 10
echo "Erasing any previous database and setting initial values to it.."
cd ../scripts/
docker stop backend > /dev/null 2>&1
./db-create-drop.sh -r > /dev/null 2>&1
docker start backend > /dev/null 2>&1

read -p "How many months of events do you want to store in Database: " MONTH
cat > /tmp/purge-dobie-db.service << EOL
[Unit]
Description=Purge old events of Dobie DB

[Service]
Type=oneshot
ExecStart=/usr/bin/bash -c '$(realpath purge-old-events.sh) $MONTH'
EOL
sudo cp /tmp/purge-dobie-db.service /etc/systemd/system/
sudo rm /tmp/purge-dobie-db.service 

cat > /tmp/purge-dobie-db.timer << EOL
[Unit]
Description=Weekly purge old events of Dobie DB

[Timer]
OnCalendar=*-*-* 07:07:07

[Install]
WantedBy=timers.target
EOL
sudo cp /tmp/purge-dobie-db.timer /etc/systemd/system/
sudo rm /tmp/purge-dobie-db.timer

sudo systemctl daemon-reload
sudo systemctl enable purge-dobie-db.timer
sudo systemctl start purge-dobie-db.timer


echo "Installing scripts to save and restore Dobie DB.."
cat > /tmp/dobie-save-db << EOL
#!/bin/bash

. $(realpath db-config)

DB_DOCKER_IP=\$(tr -d '", ' <<< \$(docker inspect database | grep '"IPAddress": "1' | gawk '{print \$2}'))

mysqldump -u \$DB_USER -p\$DB_PASSWD -h \$DB_DOCKER_IP \$DB_DATABASE > dobie_db.dump
EOL
sudo cp /tmp/dobie-save-db /usr/local/sbin/dobie-save-db
sudo rm /tmp/dobie-save-db
sudo chmod +x /usr/local/sbin/dobie-save-db


cat > /tmp/dobie-restore-db << EOL
#!/bin/bash

. $(realpath db-config)

DB_DOCKER_IP=\$(tr -d '", ' <<< \$(docker inspect database | grep '"IPAddress": "1' | gawk '{print \$2}'))

mysql -u \$DB_USER -p\$DB_PASSWD -h \$DB_DOCKER_IP \$DB_DATABASE < \$1
EOL
sudo cp /tmp/dobie-restore-db /usr/local/sbin/dobie-restore-db
sudo rm /tmp/dobie-restore-db
sudo chmod +x /usr/local/sbin/dobie-restore-db



