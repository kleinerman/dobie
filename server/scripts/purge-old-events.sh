#!/bin/bash


THIS_SCRIPT_DIR=$(dirname $(realpath $0))
. $THIS_SCRIPT_DIR/db-config


SAVED_MONTHS=$1

DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))


DATE_TO_DEL=$(date --date "$SAVED_MONTHS month ago" +%Y-%m-%d\ %H:%M)

mysql -u $DB_USER -p$DB_PASSWD -h $DB_DOCKER_IP $DB_DATABASE -e "

              DELETE FROM Event WHERE dateTime < '$DATE_TO_DEL';
              DELETE FROM Person WHERE Person.resStateId = $DELETED_STATE AND Person.id NOT IN (SELECT Event.personId FROM Event WHERE personId IS NOT NULL);


                                                                "



