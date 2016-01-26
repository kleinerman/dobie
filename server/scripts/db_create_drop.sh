#!/bin/bash

if [[ $1 == --create ]]; then
                     
    mysql -u root -p -e "CREATE USER 'conpass_usr'@'localhost' IDENTIFIED BY 'qwe123qwe'; 
                         CREATE DATABASE conpass_db; 
                         GRANT ALL ON conpass_db.* TO conpass_usr;"

    mysql -u conpass_usr -pqwe123qwe conpass_db < db_schema.sql   



    mysql -u conpass_usr -pqwe123qwe conpass_db -e "


        INSERT INTO RowState(id, description) VALUES (1, 'To Add'), (2, 'Added'), (3, 'To Delete'), (4, 'Deleted');
        INSERT INTO Controller(boardModel, macAddress) VALUES ('Raspberry PI','b80305508c9b');
        INSERT INTO Organization(id, name) VALUES(1, 'Kleinernet');
        INSERT INTO Person(id, name, cardNumber, orgId, rowStateId) VALUES(1, 'Unknown', 0, 1, 1);
        INSERT INTO Person(id, name, cardNumber, orgId, rowStateId) VALUES(1619, 'Jorge Kleinerman', 43242432, 1, 1);
        INSERT INTO EventType(id, description, rowStateId) VALUES(1, 'Access with card', 1), (2, 'Access with button', 1), (3, 'The passage remains opened', 1);
        INSERT INTO Latch(id, description, rowStateId) VALUES(1, 'Card Reader', 1), (2, 'Button', 1), (3, 'Fingerprint Reader', 1);
        INSERT INTO Zone(id, name) VALUES(1, 'Ingreso Principal');
        INSERT INTO NotReason(id, description, rowStateId) VALUES(1, 'No access', 1), (2, 'Expired card', 1), (3, 'Out of time', 1);
        INSERT INTO Passage(id, i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, zoneId, controllerId, rowStateId) VALUES(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
        INSERT INTO Passage(id, i0In, i1In, o0In, o1In, bttnIn, stateIn, rlseOut, bzzrOut, zoneId, controllerId, rowStateId) VALUES(7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
                                                 
                                                   "
    

                   
elif [[ $1 == --drop ]]; then

    mysql -u root -p -e "DROP USER 'conpass_usr'@'localhost';
                         DROP DATABASE conpass_db;"

fi
