#!/bin/bash


#This function is used to check and wait if the connection with the database
#engine isn't up before doing any operation.
#This is needed because the script which installs the server, calls this script
#as soon as it starts the containers and sometimes the DB engine isn't ready
#to receive connections or maybe the database container doesn't have an IP yet
#and the DB_DOCKER_IP variable is empty.

function chkcon {

while true; do
    DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))
    mysql -u root -p$DB_ROOT_PASSWD -h $DB_DOCKER_IP -e "SELECT 1;" 2>&1| grep ERROR > /dev/null;
    if [[ $? != 0 ]]; then
        break
    fi
    echo "Retrying connect to DB.."
    sleep 1
done


}


function create {

    mysql -u root -p$DB_ROOT_PASSWD -h $1 -e "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWD';
                                              CREATE DATABASE $DB_DATABASE;
                                              GRANT ALL ON $DB_DATABASE.* TO $DB_USER;"

    mysql -u $DB_USER -p$DB_PASSWD -h $1 $DB_DATABASE < $THIS_SCRIPT_DIR/db_schema.sql

    mysql -u $DB_USER -p$DB_PASSWD -h $1 $DB_DATABASE -e "

        INSERT INTO Role(id, description) VALUES (1, 'Administrator'), (2, 'Operator'), (3, 'Viewer'), (4, 'Org-Operator'), (5, 'Org-Viewer');
        INSERT INTO User(username, passwdHash, fullName, roleId, language, active) VALUES ('admin', '\$1\$CJvRt.x.\$ZmuMH4up3zMGnip.Kn7vI0', 'Administrator', 1, 'en', 1);
        INSERT INTO ResState(id, description) VALUES (1, 'To Add'), (2, 'To Update'), (3, 'Committed'), (4, 'To Delete'), (5, 'Deleted');
        INSERT INTO Organization(id, name, resStateId) VALUES(1, 'Visitors', 3);
        INSERT INTO EventType(id, description) VALUES(1, 'Access with card'), (2, 'Access with button'), (3, 'The door remains opened'), (4, 'The door was forced'), (5, 'Door opened by schedule'), (6, 'Door closed by schedule'), (7, 'Door opened while unlocked by schedule'), (8, 'Door opened by user interface');
        INSERT INTO DoorLock(id, description) VALUES(1, 'Card Reader'), (2, 'Fingerprint Reader'), (3, 'Button');
        INSERT INTO DenialCause(id, description) VALUES(1, 'No access'), (2, 'Expired card'), (3, 'Out of time');
        INSERT INTO CtrllerModel(id, name, integratedSbc, numOfDoors) VALUES(1, 'Dobie-RP3-333', 'Raspberry PI3', 3);

                                                   "


}


function drop {

    mysql -u root -p$DB_ROOT_PASSWD -h $1 -e "DROP USER '$DB_USER'; DROP DATABASE $DB_DATABASE;" > /dev/null 2>&1

}


THIS_SCRIPT_DIR=$(dirname $(realpath $0))


. $THIS_SCRIPT_DIR/db-config

#The DB_DOCKER_IP variable was already filled by the chkcon function.
#For this reason, the following line isn't needed anymore
#DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))

case "$1" in
    -c)
    chkcon
    create $DB_DOCKER_IP
    ;;
    -d)
    chkcon
    drop $DB_DOCKER_IP
    ;;
    -r)
    chkcon
    drop $DB_DOCKER_IP
    create $DB_DOCKER_IP
    ;;
  *)
    echo "Usage: $0 {-c|-d|-r}"
    exit 1
    ;;
esac

exit 0
