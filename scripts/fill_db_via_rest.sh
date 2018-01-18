#!/bin/bash


if [[ $1 ]]; then
    BCKND_DOCKER_IP=$1
else
    BCKND_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect backend | grep '"IPAddress": "1' | gawk '{print $2}'))
fi



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "fa163e76206f"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller

#curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "b827ebf65300"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "b827eb277791"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller



sleep 4


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Sur"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Norte"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinetes Torre A"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puertas Front Torre A"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup




curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinete 1", "doorNum": 1, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta 2", "doorNum": 2, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Barrera 5", "doorNum": 3, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Baño 3", "doorNum": 1, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinte 5", "doorNum": 2, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso 2", "doorNum": 3, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door





curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/1/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/1/door/2


curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/4


curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2/door/4

curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/visitdoorgroup/2







curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Buinet"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Building Networks"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/2
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Datacenter"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Movistel"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/4

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Jorge Kleinerman", "identNumber": "28063146", "cardNumber": 5379295, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ary Kleinerman", "identNumber": "21063146", "cardNumber": 5300738, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Manuel Bobadilla", "identNumber": "22063146", "cardNumber": 9038876, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Lucas Ferre", "identNumber": "23063146", "cardNumber": 9136307, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Paola Ceballos", "identNumber": "2463146", "cardNumber": 4994413, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Juan Alvarez", "identNumber": "25063146", "cardNumber": 5300739, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Carlos Vazquez", "identNumber": "26063146", "cardNumber": 4300757, "orgId": 2, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "identNumber": "27063146", "cardNumber": 5300768, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
#curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "cardNumber": 5301768, "orgId": 2, "visitedOrgId": 3}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
#curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "cardNumber": 5302768, "orgId": 2, "visitedOrgId": 4}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person




curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 2, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 6, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 4, "weekDay": 3, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "personId": 6, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 5, "weekDay": 7, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 8, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 7, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 7, "weekDay": 4, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 8, "weekDay": 7, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access


curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Carlos Ranzula", "identNumber": "23063147", "cardNumber": 5301768, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/8

curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/7






curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "01:01", "endTime": "22:31", "expireDate": "2018-11-12"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "personId": 6, "weekDay": 5, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2020-01-02"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/liaccess








sleep 4

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller/1/reprov
