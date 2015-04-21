#!/bin/bash

echo "Creating and setting ConPass Database.."
mysql -u root -p -e "CREATE USER 'conpass_usr'@'localhost' IDENTIFIED BY 'qwe123qwe'"
mysql -u root -p -e "CREATE DATABASE conpass_db"
mysql -u root -p -e "GRANT ALL ON conpass_db.* TO conpass_usr"
