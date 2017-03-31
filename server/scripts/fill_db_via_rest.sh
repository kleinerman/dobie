#!/bin/bash

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "b827eb750952"}' http://10.10.7.74:5000/api/v1.0/controller
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "b827eb277791"}' http://10.10.7.74:5000/api/v1.0/controller


sleep 4


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Sur"}' http://10.10.7.74:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Norte"}' http://10.10.7.74:5000/api/v1.0/zone



curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinetes Torre A"}' http://10.10.7.74:5000/api/v1.0/visitorspassages
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puertas Front Torre A"}' http://10.10.7.74:5000/api/v1.0/visitorspassages





curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Molinete 1", "pssgNum": 1, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Puerta 2", "pssgNum": 2, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Barrera 5", "pssgNum": 3, "controllerId": 2, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Baño 3", "pssgNum": 1, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Molinte 5", "pssgNum": 2, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Ingreso 2", "pssgNum": 3, "controllerId": 1, "rlseTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1}' http://10.10.7.74:5000/api/v1.0/passage





curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Buinet"}' http://10.10.7.74:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Building Networks"}' http://10.10.7.74:5000/api/v1.0/organization/2
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Datacenter"}' http://10.10.7.74:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Movistel"}' http://10.10.7.74:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://10.10.7.74:5000/api/v1.0/organization/4

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Jorge Kleinerman", "cardNumber": 4300737, "orgId": 2, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ary Kleinerman", "cardNumber": 5300738, "orgId": 3, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Manuel Bobadilla", "cardNumber": 9038876, "orgId": 2, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Lucas Ferre", "cardNumber": 9136307, "orgId": 3, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Paola Ceballos", "cardNumber": 4994413, "orgId": 2, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Juan Alvarez", "cardNumber": 5300739, "orgId": 3, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Carlos Vazquez", "cardNumber": 4300757, "orgId": 2, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "cardNumber": 5300768, "orgId": 3, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person
#curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "cardNumber": 5301768, "orgId": 2, "visitedOrgId": 3}' http://10.10.7.74:5000/api/v1.0/person
#curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ruben Juearez", "cardNumber": 5302768, "orgId": 2, "visitedOrgId": 4}' http://10.10.7.74:5000/api/v1.0/person




curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 2, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 6, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 5, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 5, "personId": 4, "weekDay": 3, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 5, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 5, "personId": 6, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 5, "weekDay": 7, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 8, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 7, "weekDay": 2, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 7, "weekDay": 4, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 8, "weekDay": 7, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2016-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 6, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2018-12-12"}' http://10.10.7.74:5000/api/v1.0/access


curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Pedro Juearez", "cardNumber": 5377768, "orgId": 2, "visitedOrgId": null}' http://10.10.7.74:5000/api/v1.0/person/8

curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://10.10.7.74:5000/api/v1.0/person/7






curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "01:01", "endTime": "22:31", "expireDate": "2018-11-12"}' http://10.10.7.74:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 4, "personId": 6, "weekDay": 5, "iSide": 1, "oSide": 1, "startTime": "20:37", "endTime": "21:37", "expireDate": "2020-01-02"}' http://10.10.7.74:5000/api/v1.0/liaccess








sleep 4

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://10.10.7.74:5000/api/v1.0/controller/1/reprov

