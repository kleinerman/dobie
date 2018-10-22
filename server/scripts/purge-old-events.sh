#!/bin/bash

DB_PASSWD=qwe123qwe

SAVED_MONTHS=$1

DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))


DATE_TO_DEL=$(date --date "$SAVED_MONTHS month ago" +%Y-%m-%d\ %H:%M)

mysql -u dobie_usr -p$DB_PASSWD -h $DB_DOCKER_IP dobie_db -e "

    DELETE FROM Event WHERE dateTime < '$DATE_TO_DEL';

     
                                                            "





