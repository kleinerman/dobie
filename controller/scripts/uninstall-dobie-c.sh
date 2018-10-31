#!/bin/bash


echo "Dobie Server Uninstallation Script"
echo "=================================="

read -p "Are you sure to uninstall Dobie Controller? (y/n): " answer
if [ $answer != y ] && [ $answer != Y ]; then
  exit
fi

echo "Stoping Dobie Controller systemd unit.."
sudo systemctl stop dobie-c.service

echo "Disabling and removing systemd units.."
sudo systemctl disable dobie-c.service
sudo rm /etc/systemd/system/dobie-c.service
sudo systemctl daemon-reload

echo "Removing Dobie Controller DB directory"
sudo rm -rf /var/lib/dobie-c/

echo "Removing Dobie Controller Logs directory.."
sudo rm -rf /var/log/dobie-c/

echo "Removing Log rotation file.."
sudo rm /etc/logrotate.d/dobie-c


