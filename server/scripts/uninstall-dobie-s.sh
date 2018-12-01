#!/bin/bash


echo "Dobie Server Uninstallation Script"
echo "=================================="

read -p "Are you sure to uninstall Dobie Server? (y/n): " answer
if [ $answer != y ] && [ $answer != Y ]; then
  exit
fi

echo "Removing Dobie Server Logs directory.."
sudo rm -rf /var/log/dobie-s/

echo "Removing Log rotation file.."
sudo rm /etc/logrotate.d/dobie-s

echo "Stoping all systemd units.."
sudo systemctl stop purge-dobie-db.timer
sudo systemctl stop dobie-s.service

echo "Disabling and removing systemd units.."
sudo systemctl disable purge-dobie-db.timer
sudo systemctl disable dobie-s.service
sudo rm /etc/systemd/system/purge-dobie-db.timer
sudo rm /etc/systemd/system/purge-dobie-db.service
sudo rm /etc/systemd/system/dobie-s.service
sudo systemctl daemon-reload

echo "Removing scripts to save and restore DB.."
sudo rm /usr/local/sbin/dobie-save-db
sudo rm /usr/local/sbin/dobie-restore-db

read -p "Do you want to remove all Docker containers, volumes and networks (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then
  sudo docker rm $(docker ps -a -q)
  sudo docker rmi $(docker images -q)
  sudo docker volume rm dobie_database-volume
  sudo docker network rm dobie_default
fi

