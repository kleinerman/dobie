curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"ctrllerModelId": 1, "macAddress": "b827eb34da53"}' http://quebec:5000/api/v1.0/controller

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Building Networks"}' http://quebec:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Datacenter Capitalinas"}' http://quebec:5000/api/v1.0/organization

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Oficina"}' http://quebec:5000/api/v1.0/zone

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Ingreso F65", "pssgNum": 1, "controllerId": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 60, "zoneId": 1}' http://quebec:5000/api/v1.0/passage
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"description": "Ingreso F66", "pssgNum": 2, "controllerId": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 60, "zoneId": 1}' http://quebec:5000/api/v1.0/passage

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Jorge Kleinerman", "identNumber": "29063666", "cardNumber": 4300737, "orgId": 3, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ary Kleinerman", "identNumber": "31058040", "cardNumber": 5326224, "orgId": 3, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Lucas Ferre", "identNumber": "38807747", "cardNumber": 1908068, "orgId": 3, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Fernando Acha", "identNumber": "11977009", "cardNumber": 9384477, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Jorge Olmi", "identNumber": "17052581", "cardNumber": 1963505, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Javier Coronel", "identNumber": "37330686", "cardNumber": 6830950, "orgId": 3, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Hector Abdala", "identNumber": "12876264", "cardNumber": 2153701, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Paola Ceballos", "identNumber": "32406399", "cardNumber": 14698905, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Sebastian Palacio", "identNumber": "13372321", "cardNumber": 2498624, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "German Fisanotti", "identNumber": "31055868", "cardNumber": 6040073, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Manuel Ferreiro", "identNumber": "31413694", "cardNumber": 6908841, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Selva Correa", "identNumber": "17841562", "cardNumber": 1907933, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Paola Velasco", "identNumber": "23895074", "cardNumber": 6301593, "orgId": 2, "visitedOrgId": null}' http://quebec:5000/api/v1.0/person

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 9, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 10, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 11, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 12, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 1, "personId": 13, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 1, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 2, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 3, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 4, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 5, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 6, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 7, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 8, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 9, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 10, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 11, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 12, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"pssgId": 2, "personId": 13, "iSide": 1, "oSide": 1, "startTime": "00:00", "endTime": "23:59", "expireDate": "2099-12-12"}' http://quebec:5000/api/v1.0/access
