#!/bin/bash


echo "Dobie Server Uninstallation Script"
echo "=================================="

echo "Stoping Dobie Controller systemd unit.."
systemctl stop dobie-c.service

echo "Disabling and removing systemd units.."
systemctl disable dobie-c.service
rm /etc/systemd/system/dobie-c.service
systemctl daemon-reload

echo "Removing Dobie Controller DB directory"
rm -rf /var/lib/dobie-c/

echo "Removing Dobie Controller Logs directory.."
rm -rf /var/log/dobie-c/

echo "Removing Log rotation file.."
rm /etc/logrotate.d/dobie-c


