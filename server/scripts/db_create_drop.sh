#!/bin/bash



function create {
    mysql -u root -pqwe123qwe -e "CREATE USER 'conpass_usr'@'%' IDENTIFIED BY 'qwe123qwe'; 
                         CREATE DATABASE conpass_db; 
                         GRANT ALL ON conpass_db.* TO conpass_usr;"


    #SCRIPTDIR="$(dirname "$(readlink -f "$0")")"
    SCRIPTPATH=`realpath $0`
    SCRIPTDIR=`dirname $SCRIPTPATH`



    mysql -u conpass_usr -pqwe123qwe conpass_db < ${SCRIPTDIR}/db_schema.sql   



    mysql -u conpass_usr -pqwe123qwe conpass_db -e "



        INSERT INTO RowState(id, description) VALUES (1, 'To Add'), (2, 'To Update'), (3, 'Committed'), (4, 'To Delete'), (5, 'Deleted');
        INSERT INTO Organization(id, name, rowStateId) VALUES(1, 'Unknown', 3), (2, 'Visitors', 3);
        INSERT INTO Person(id, name, cardNumber, orgId, rowStateId) VALUES(1, 'Unknown', 0, 1, 3);
        INSERT INTO EventType(id, description, rowStateId) VALUES(1, 'Access with card', 3), (2, 'Access with button', 3), (3, 'The passage remains opened', 3), (4, 'The passage was forced', 3);
        INSERT INTO Latch(id, description, rowStateId) VALUES(1, 'Card Reader', 3), (2, 'Fingerprint Reader', 3), (3, 'Button', 3);
        INSERT INTO NotReason(id, description, rowStateId) VALUES(1, 'No access', 3), (2, 'Expired card', 3), (3, 'Out of time', 3);
        INSERT INTO CtrllerModel(id, name, boardModel, pssgsQuant) VALUES(1, 'ConPassRP333', 'Raspberry PI', 3);

                                                   "


}


function drop {

    mysql -u root -pqwe123qwe -e "DROP USER 'conpass_usr';
                                  DROP DATABASE conpass_db;"

}



case "$1" in
    --create)
    create
    ;;
    --drop)
    drop
    ;;
    --regenerate)
    drop
    create
    ;;
  *)
    echo "Usage: $0 {create|drop|regenerate}"
    exit 1
    ;;
esac

exit 0

