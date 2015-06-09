#!/bin/bash

if [[ $1 == --create ]]; then
                     
    mysql -u root -p -e "CREATE USER 'conpass_usr'@'localhost' IDENTIFIED BY 'qwe123qwe'; 
                         CREATE DATABASE conpass_db; 
                         GRANT ALL ON conpass_db.* TO conpass_usr;"

    mysql -u conpass_usr -pqwe123qwe conpass_db < db_schema.sql   

                   
elif [[ $1 == --drop ]]; then

    mysql -u root -p -e "DROP USER 'conpass_usr'@'localhost';
                         DROP DATABASE conpass_db;"

fi
