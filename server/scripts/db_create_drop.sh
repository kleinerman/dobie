#!/bin/bash



function create {
    mysql -u root -pqwe123qwe -h $1 -e "CREATE USER 'dobie_usr'@'%' IDENTIFIED BY 'qwe123qwe'; 
                                        CREATE DATABASE dobie_db; 
                                        GRANT ALL ON dobie_db.* TO dobie_usr;"


    #SCRIPTDIR="$(dirname "$(readlink -f "$0")")"
    SCRIPTPATH=`realpath $0`
    SCRIPTDIR=`dirname $SCRIPTPATH`



    mysql -u dobie_usr -pqwe123qwe -h $1 dobie_db < ${SCRIPTDIR}/db_schema.sql   



    mysql -u dobie_usr -pqwe123qwe -h $1 dobie_db -e "




        INSERT INTO Role(id, description) VALUES (1, 'Administrator'), (2, 'Viewer');
        INSERT INTO User(description, username, passwdHash, roleId) VALUES ('Administrator', 'admin', '\$1\$CJvRt.x.\$ZmuMH4up3zMGnip.Kn7vI0', 1);
        INSERT INTO ResState(id, description) VALUES (1, 'To Add'), (2, 'To Update'), (3, 'Committed'), (4, 'To Delete'), (5, 'Deleted');
        INSERT INTO Organization(id, name, resStateId) VALUES(1, 'Visitors', 3);
        INSERT INTO EventType(id, description) VALUES(1, 'Access with card'), (2, 'Access with button'), (3, 'The door remains opened'), (4, 'The door was forced');
        INSERT INTO DoorLock(id, description) VALUES(1, 'Card Reader'), (2, 'Fingerprint Reader'), (3, 'Button');
        INSERT INTO DenialCause(id, description) VALUES(1, 'No access'), (2, 'Expired card'), (3, 'Out of time');
        INSERT INTO CtrllerModel(id, name, integratedSbc, numOfDoors) VALUES(1, 'Dobie-RP1-333', 'Raspberry PI', 3), (2, 'Dobie-RPI2-424', 'Raspberry PI 2', 4), (3, 'Dobie-RPI1-333', 'Raspberry PI', 3), (4, 'Dobie-BBONE-444', 'BeagleBone', 4);

                                                   "


}


function drop {

    mysql -u root -pqwe123qwe -h $1 -e "DROP USER 'dobie_usr';
                                        DROP DATABASE dobie_db;"

}


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

