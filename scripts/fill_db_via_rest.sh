#!/bin/bash


if [[ $1 ]]; then
    BCKND_DOCKER_IP=$1
else
    BCKND_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect backend | grep '"IPAddress": "1' | gawk '{print $2}'))
fi



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 1", "ctrllerModelId": 1, "macAddress": "b827eb437bac"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 2", "ctrllerModelId": 1, "macAddress": "b827eb2c3abd"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller



sleep 4


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Sur"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Norte"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Este"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Oeste"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Este"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Oeste"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Norte"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Sur"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Principal", "doorNum": 1, "controllerId": 1, "snsrType": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinete", "doorNum": 2, "controllerId": 1, "snsrType": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Ascensor", "doorNum": 3, "controllerId": 1, "snsrType": 0, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 3, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 1", "doorNum": 1, "controllerId": 2, "snsrType": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 2", "doorNum": 2, "controllerId": 2, "snsrType": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 2, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 3", "doorNum": 3, "controllerId": 2, "snsrType": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 3, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door







curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/1/door/2
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/1/door/3


curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/4
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/6

#Deleting one door from visitdoorgroup 2
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/4

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/5

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/3/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/3/door/2


curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/4/door/3
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/4/door/1

#Deleting all preivious visitdoorgroup previously created
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/4





curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Bonify"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Bonifies Networks"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/2
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Coliter Inc"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Movirack"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/4
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Larrykeyn Corp"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Summer Time"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Clavnet Company"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization


#Static Persons
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Jorge Kleinerman", "identNumber": "28063146", "cardNumber": 5379295, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ary Kleinerman", "identNumber": "21063146", "cardNumber": 5300738, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "German Fisanotti", "identNumber": "22063146", "cardNumber": 9038876, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Lucas Ferre", "identNumber": "23063146", "cardNumber": 9136307, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Daniel Costa", "identNumber": "24631946", "cardNumber": 6036754, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Romina Goner", "identNumber": "25063146", "cardNumber": 5327374, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Carlos Navares", "identNumber": "26063146", "cardNumber": 5330640, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Lorena Tolares", "identNumber": "27063146", "cardNumber": 5325783, "orgId": 5, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Gonzalo Bonatti", "identNumber": "28543146", "cardNumber": 12843557, "orgId": 5, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Mariano Roter", "identNumber": "19063146", "cardNumber": 12844869, "orgId": 5, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Mauro Alvarez", "identNumber": "21161141", "cardNumber": 9184668, "orgId": 5, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Monica Llanos", "identNumber": "25073147", "cardNumber": 9198124, "orgId": 6, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Gonzales", "identNumber": "24737047", "cardNumber": 11943284, "orgId": 7, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ricardo Telurio", "identNumber": "14063246", "cardNumber": 5300739, "orgId": 7, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Pecamenta", "identNumber": "40063146", "cardNumber": 4300757, "orgId": 7, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Sol Tapia", "identNumber": "23563346", "cardNumber": 5300768, "orgId": 7, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person



#Some Visitors
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Claudia Toloza", "identNumber": "11064146", "cardNumber": 2163612, "orgId": 1, "visitedOrgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Diego Joner", "identNumber": "25033546", "cardNumber": 5327790, "orgId": 1, "visitedOrgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Mariana Turin", "identNumber": "24053646", "cardNumber": 5330823, "orgId": 1, "visitedOrgId": 3}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Marcelo Olerti", "identNumber": "8463146", "cardNumber": 5326147, "orgId": 1, "visitedOrgId": 3}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Marcos Vison", "identNumber": "65263146", "cardNumber": 7306735, "orgId": 1, "visitedOrgId": 5}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Carlos Vazquez", "identNumber": "36043156", "cardNumber": 4310747, "orgId": 1, "visitedOrgId": 6}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Tatiana Rodriguez", "identNumber": "29063356", "cardNumber": 8304763, "orgId": 1, "visitedOrgId": 7}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person



################# Accesses for static persons ####################
#Jorge Kleinerman Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 1, "weekDay": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access



#Ary Kleinerman Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#German Fisanotti Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Lucas Ferre Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Daniel Costa Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Romina Goner Accesses
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Carlos Navares
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Lorena Tolares
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Gonzalo Bonatti
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 9, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 9, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 9, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Mariano Roter
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 10, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 10, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 10, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Mauro Alvarez
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 11, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 11, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 11, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Monica Llanos
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 12, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 12, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 12, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Ruben Gonzales
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 13, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 13, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 13, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Ricardo Telurio
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 14, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 14, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 14, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Ruben Pecamenta
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 15, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 15, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 15, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Sol Tapia
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "personId": 16, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 16, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 16, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access




################# Accesses for Visitors ####################
#Claudia Toloza
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 17, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 17, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Diego Joner
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 18, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 18, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Mariana Turin
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 19, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 19, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Marcelo Olerti
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 20, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 20, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Marcos Vison
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 21, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 21, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Carlos Vazquez
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 2, "personId": 22, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 3, "personId": 22, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

#Tatiana Rodriguez
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 23, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 23, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2025-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


#Modifying Sol Tapia Values
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Soledad Tapia", "identNumber": "24573247", "cardNumber": 5300817, "orgId": 7, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/16



#Waiting 3 seconds to let database finish de insertion of the accesses of deleted persons
sleep 3 
#Deleting Ruben Pecamenta
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/15

#Simulating some visitors leaving the building
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/19
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/22
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/20


#ReProvisioning Controladora 1
sleep 4
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller/1/reprov



#Creating deleting and modifying some system users
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "jcabelo", "passwd": "qwe123qwe", "fullName": "Juan Cabelo", "roleId": 1, "language": "en", "active": 1}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "rtortoza", "passwd": "qwe123qwe", "fullName": "Ramon Tortoza", "roleId": 2, "language": "en", "active": 1}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "lcabrera", "passwd": "qwe123qwe", "fullName": "Luis Cabrera", "roleId": 2, "language": "es", "active": 1}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://localhost:5000/api/v1.0/user/4
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "asorini", "passwd": "qwe123qwe", "fullName": "Andrea Sorini", "roleId": 3, "language": "en", "active": 1}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"username": "asorini", "passwd": "qwe123", "fullName": "Andrea Sorini", "roleId": 3, "language": "es", "active": 1}' http://localhost:5000/api/v1.0/user/5

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"passwd": "qwe123qwe"}' http://localhost:5000/api/v1.0/user/1

curl -u admin:qwe123qwe -i -H "Content-Type: application/json" -X PUT -d '{"passwd": "admin"}' http://localhost:5000/api/v1.0/user/1






DB_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect database | grep '"IPAddress": "1' | gawk '{print $2}'))

DATE_NOW=$(date +%Y-%m-%d\ %H:%M)

DATE_1D_AGO=$(date --date "1 day ago" +%Y-%m-%d\ %H:%M)
DATE_2D_AGO=$(date --date "2 day ago" +%Y-%m-%d\ %H:%M)
DATE_3D_AGO=$(date --date "3 day ago" +%Y-%m-%d\ %H:%M)
DATE_4D_AGO=$(date --date "4 day ago" +%Y-%m-%d\ %H:%M)
DATE_5D_AGO=$(date --date "5 day ago" +%Y-%m-%d\ %H:%M)
DATE_6D_AGO=$(date --date "6 day ago" +%Y-%m-%d\ %H:%M)
DATE_7D_AGO=$(date --date "7 day ago" +%Y-%m-%d\ %H:%M)

mysql -u dobie_usr -pqwe123qwe -h $DB_DOCKER_IP dobie_db -e "

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_NOW', 1, 1, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_NOW', 1, 2, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_NOW', 1, 15, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_NOW', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_NOW', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_NOW', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_NOW', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_NOW', 1, 15, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_NOW', 1, 7, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_1D_AGO=', 1, 15, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_1D_AGO=', 1, 15, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_1D_AGO=', 1, 15, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_1D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_1D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_1D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_1D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_1D_AGO=', 1, 9, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_1D_AGO=', 1, 8, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_2D_AGO=', 1, 17, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_2D_AGO=', 1, 18, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_2D_AGO=', 1, 19, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_2D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_2D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_2D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_2D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_2D_AGO=', 1, 16, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_2D_AGO=', 1, 14, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_3D_AGO=', 1, 16, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_3D_AGO=', 1, 16, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_3D_AGO=', 1, 16, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_3D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_3D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_3D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_3D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_3D_AGO=', 1, 19, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_3D_AGO=', 1, 20, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_4D_AGO=', 1, 13, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_4D_AGO=', 1, 12, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_4D_AGO=', 1, 11, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_4D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_4D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_4D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_4D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_4D_AGO=', 1, 7, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_4D_AGO=', 1, 7, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_5D_AGO=', 1, 17, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_5D_AGO=', 1, 18, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_5D_AGO=', 1, 19, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_5D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_5D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_5D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_5D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_5D_AGO=', 1, 4, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_5D_AGO=', 1, 1, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_6D_AGO=', 1, 20, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_6D_AGO=', 1, 21, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_6D_AGO=', 1, 22, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_6D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_6D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_6D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_6D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_6D_AGO=', 1, 23, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_6D_AGO=', 1, 23, 1, 0, 3);

    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 1, '$DATE_7D_AGO=', 1, 19, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 2, '$DATE_7D_AGO=', 1, 19, 1, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 3, '$DATE_7D_AGO=', 1, 19, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(2, 4, '$DATE_7D_AGO=', 3, NULL, 0, 1, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(3, 5, '$DATE_7D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(4, 5, '$DATE_7D_AGO=', NULL, NULL, NULL, NULL, NULL);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_7D_AGO=', 1, NULL, NULL, 0, 1);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_7D_AGO=', 1, 7, 1, 0, 2);
    insert into Event(eventTypeId, doorId, dateTime, doorLockId, personId, side, allowed, denialCauseId) values(1, 5, '$DATE_7D_AGO=', 1, 7, 1, 0, 3);



                                                 "





