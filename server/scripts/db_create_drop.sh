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
        INSERT INTO RowState(id, description) VALUES (1, 'To Add'), (2, 'To Update'), (3, 'Committed'), (4, 'To Delete'), (5, 'Deleted');
        INSERT INTO Organization(id, name, rowStateId) VALUES(1, 'Visitors', 3);
        INSERT INTO EventType(id, description) VALUES(1, 'Access with card'), (2, 'Access with button'), (3, 'The passage remains opened'), (4, 'The passage was forced');
        INSERT INTO Latch(id, description, rowStateId) VALUES(1, 'Card Reader', 3), (2, 'Fingerprint Reader', 3), (3, 'Button', 3);
        INSERT INTO NotReason(id, description, rowStateId) VALUES(1, 'No access', 3), (2, 'Expired card', 3), (3, 'Out of time', 3);
        INSERT INTO CtrllerModel(id, name, boardModel, pssgsQuant) VALUES(1, 'Dobie-RP1-333', 'Raspberry PI', 3);

                                                   "


}


function drop {

    mysql -u root -pqwe123qwe -h $1 -e "DROP USER 'dobie_usr';
                                        DROP DATABASE dobie_db;"

}


case "$1" in
    -c)
    create $2
    ;;
    -d)
    drop $2
    ;;
    -r)
    drop $2
    create $2
    ;;
  *)
    echo "Usage: $0 {-c|-d|-r} DATABASE_SERVER_IP"
    exit 1
    ;;
esac

exit 0

