#!/bin/bash


function create {

#    echo $1                                          
#    echo $DB_ROOT_PASSWD
#    echo $DB_USER
#    echo $DB_PASSWD
#    echo $DB_DATABASE
#    echo $THIS_SCRIPT_DIR




    mysql -u root -p$DB_ROOT_PASSWD -h $1 -e "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWD'; 
                                              CREATE DATABASE $DB_DATABASE; 
                                              GRANT ALL ON $DB_DATABASE.* TO $DB_USER;"

    mysql -u $DB_USER -p$DB_PASSWD -h $1 $DB_DATABASE < $THIS_SCRIPT_DIR/db_schema.sql

    mysql -u $DB_USER -p$DB_PASSWD -h $1 $DB_DATABASE -e "

        INSERT INTO Role(id, description) VALUES (1, 'Administrator'), (2, 'Operator'), (3, 'Viewer');
        INSERT INTO User(username, passwdHash, fullName, roleId, language, active) VALUES ('admin', '\$1\$CJvRt.x.\$ZmuMH4up3zMGnip.Kn7vI0', 'Administrator', 1, 'en', 1);
        INSERT INTO ResState(id, description) VALUES (1, 'To Add'), (2, 'To Update'), (3, 'Committed'), (4, 'To Delete'), (5, 'Deleted');
        INSERT INTO Organization(id, name, resStateId) VALUES(1, 'Visitors', 3);
        INSERT INTO EventType(id, description) VALUES(1, 'Access with card'), (2, 'Access with button'), (3, 'The door remains opened'), (4, 'The door was forced');
        INSERT INTO DoorLock(id, description) VALUES(1, 'Card Reader'), (2, 'Fingerprint Reader'), (3, 'Button');
        INSERT INTO DenialCause(id, description) VALUES(1, 'No access'), (2, 'Expired card'), (3, 'Out of time');
        INSERT INTO CtrllerModel(id, name, integratedSbc, numOfDoors) VALUES(1, 'Dobie-RP1-333', 'Raspberry PI', 3), (2, 'Dobie-RPI2-424', 'Raspberry PI 2', 4), (3, 'Dobie-RPI1-333', 'Raspberry PI', 3), (4, 'Dobie-BBONE-444', 'BeagleBone', 4);

                                                   "


}


function drop {

    mysql -u root -p$DB_ROOT_PASSWD -h $1 -e "DROP USER '$DB_USER';
                                              DROP DATABASE $DB_DATABASE;"

}


THIS_SCRIPT_DIR=$(dirname $(realpath $0))


. $THIS_SCRIPT_DIR/db-config


if [[ $2 ]]; then
    DB_DOCKER_IP=$2
else
    DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))
fi    

echo "Working in DB: $DB_DOCKER_IP"

case "$1" in
    -c)
    create $DB_DOCKER_IP
    ;;
    -d)
    drop $DB_DOCKER_IP
    ;;
    -r)
    drop $DB_DOCKER_IP
    create $DB_DOCKER_IP
    ;;
  *)
    echo "Usage: $0 {-c|-d|-r}"
    exit 1
    ;;
esac

exit 0

