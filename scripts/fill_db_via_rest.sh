#!/bin/bash


read -p "Do you want to clean previous data from DB before? (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then

  docker container stop backend
  cd ../server/scripts/
  ./db-create-drop.sh -r
  docker container start backend
  cd ../../scripts/ #Not necessary
  sleep 2
fi



if [[ $1 ]]; then
    BCKND_DOCKER_IP=$1
else
    BCKND_DOCKER_IP=$(tr -d '", ' <<< $(docker inspect backend | grep '"IPAddress": "1' | gawk '{print $2}'))
fi




read -p "Are you testing in real environment? (y/n): " answer
if [ $answer == y ] || [ $answer == Y ]; then

  curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 1", "ctrllerModelId": 1, "macAddress": "b827eb437bac"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller
  curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 2", "ctrllerModelId": 1, "macAddress": "b827ebc80917"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller

else

  curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 1", "ctrllerModelId": 1, "macAddress": "525400a6d900"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller
  curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Controladora 2", "ctrllerModelId": 1, "macAddress": "52540050ea6d"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller

fi


sleep 4


curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Sur"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Norte"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Este"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Zona Oeste"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/zone



#Adding Door Groups
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Este", "isForVisit": 1, "orgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Oeste", "isForVisit": 1, "orgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Norte", "isForVisit": 1, "orgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Ingreso Visitas Sur", "isForVisit": 1, "orgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Camino Interno", "isForVisit": 0, "orgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup

#At this point, a Door Group for an Organization can't be added (orgId != null), since still there isn't any Organization in DB.
#Trying to do it -> 409 CONFLICT ERROR


#Adding doors to controller 1
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Principal", "doorNum": 1, "controllerId": 1, "snsrType": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Molinete", "doorNum": 2, "controllerId": 1, "snsrType": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Ascensor", "doorNum": 3, "controllerId": 1, "snsrType": 0, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 3, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
#Adding doors to controller 2
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 1", "doorNum": 1, "controllerId": 2, "snsrType": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 1, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 2", "doorNum": 2, "controllerId": 2, "snsrType": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 2, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puerta Oficina 3", "doorNum": 3, "controllerId": 2, "snsrType": 1, "unlkTime": 7, "bzzrTime": 3, "alrmTime": 10, "zoneId": 3, "isVisitExit": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/door


#Adding Unlock Door Schedules
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "weekDay": 1, "startTime": "12:45", "endTime": "15:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "weekDay": 1, "startTime": "18:45", "endTime": "17:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "weekDay": 1, "startTime": "11:45", "endTime": "15:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"doorId": 5, "weekDay": 2, "startTime": "10:32", "endTime": "16:37"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd/3
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "weekDay": 1, "startTime": "12:45", "endTime": "15:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "weekDay": 7, "startTime": "13:45", "endTime": "15:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd/4
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "weekDay": 1, "startTime": "10:45", "endTime": "15:30"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/unlkdoorskd



#Adding Exception Days to Unlock door by schedule
DATE_NOW=$(date +%Y-%m-%d)
DATE_TOMORROW=$(date --date "tomorrow" +%Y-%m-%d)
DATE_YESTERDAY=$(date --date "yesterday" +%Y-%m-%d)

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "excDay": "'$DATE_YESTERDAY'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 1, "excDay": "'$DATE_NOW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 5, "excDay": "'$DATE_NOW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"excDay": "'$DATE_TOMORROW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds/3
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "excDay": "'$DATE_NOW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 4, "excDay": "'$DATE_TOMORROW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds/5

curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"doorId": 6, "excDay": "'$DATE_NOW'"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/excdayuds



#Adding doors to doorGroups
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/1/door/2
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/1/door/3

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/2/door/4
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 0, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/2/door/6


#Retrieving all doors from doorGroup 2
curl -u admin:admin -i -H "Content-Type: application/json" -X GET -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/2/door

sleep 1


#Deleting one door from doorgroup 2
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/2/door/4

#Adding more doors to different doorgrupos
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/2/door/5
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/3/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/3/door/2
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/4/door/3
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/4/door/1

#Deleting a complete Door Group
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/4

#Adding more doors to doorgroup 5
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/5/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/5/door/2



#Organizations
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Bonify"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Bonifies Networks"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/2
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Coliter Inc"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Movirack"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization/4
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Larrykeyn Corp"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Summer Time"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Clavnet Company"}' http://$BCKND_DOCKER_IP:5000/api/v1.0/organization


#Adding DoorGroups to Organizations
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "pUERTAS Bonifies", "isForVisit": 0, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puertas Coliter Inc", "isForVisit": 0, "orgId": 3}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup
#Adding another Door Group to same Organization (Bonifies)
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"name": "Puertas Centro Data", "isForVisit": 0, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup



#Adding Doors to previous DoorGroups
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/6/door/1
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/6/door/3

curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/7/door/5
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"iSide": 1, "oSide": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/7/door/4


#Modify one Door Group to simulate a correction (name and orgId)
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"name": "Puertas Bonf. Net.", "isForVisit": 1, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/doorgroup/6

#Adding Static Persons
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Jorge Emanuel", "lastName": "Kleinerman", "identNumber": "28063146", "note": "nota de prueba", "cardNumber": 5379295, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Ary D.", "lastName": "Kleinerman", "identNumber": "21063146", "note": "nota de prueba", "cardNumber": 5300738, "orgId": 2, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "German Andres", "lastName": "Fisanotti", "identNumber": "22063146", "note": "nota de prueba", "cardNumber": 9038876, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Lucas", "lastName": "Ferre", "identNumber": "23063146", "note": "nota de prueba", "cardNumber": 9136307, "orgId": 2}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Daniel", "lastName": "Costa", "identNumber": "24631946", "note": "nota de prueba", "cardNumber": 6036754, "orgId": 3, "visitedOrgId": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Romina", "lastName": "Goner", "identNumber": "25063146", "note": "nota de prueba", "cardNumber": 5327374, "orgId": 3, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Carlos", "lastName": "Navares", "identNumber": "26063146", "note": "nota de prueba", "cardNumber": 5330640, "orgId": 3, "isProvider": null}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Lorena", "lastName": "Tolares", "identNumber": "27063146", "note": "nota de prueba", "cardNumber": 5325783, "orgId": 5, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Gonzalo", "lastName": "Bonatti", "identNumber": "28543146", "note": "nota de prueba", "cardNumber": 12843557, "orgId": 5, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Mariano", "lastName": "Roter", "identNumber": "19063146", "note": "nota de prueba", "cardNumber": 12844869, "orgId": 5, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Mauro J.", "lastName": "Alvarez", "identNumber": "21161141", "note": "nota de prueba", "cardNumber": 9184668, "orgId": 5, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Monica", "lastName": "Llanos", "identNumber": "25073147", "note": "nota de prueba", "cardNumber": 9198124, "orgId": 6, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Ruben", "lastName": "Gonzales", "identNumber": "24737047", "note": "nota de prueba", "cardNumber": 11943284, "orgId": 7, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Ricardo", "lastName": "Telurio", "identNumber": "14063246", "note": "nota de prueba", "cardNumber": 5300739, "orgId": 7, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Ruben", "lastName": "Pecamenta", "identNumber": "40063146", "note": "nota de prueba", "cardNumber": 4300757, "orgId": 7, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Sol Maria", "lastName": "Tapia", "identNumber": "23563346", "note": "nota de prueba", "cardNumber": 5300768, "orgId": 7, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person


#Adding Some Visitors
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Claudia", "lastName": "Toloza", "identNumber": "11064146", "note": "nota de prueba", "cardNumber": 2163612, "orgId": 1, "visitedOrgId": 2, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Diego", "lastName": "Joner", "identNumber": "25033546", "note": "nota de prueba", "cardNumber": 5327790, "orgId": 1, "visitedOrgId": 2, "isProvider": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Mariana", "lastName": "Turin", "identNumber": "24053646", "note": "nota de prueba", "cardNumber": 5330823, "orgId": 1, "visitedOrgId": 3, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Marcelo", "lastName": "Olerti", "identNumber": "8463146", "note": "nota de prueba", "cardNumber": 5326147, "orgId": 1, "visitedOrgId": 3, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Marcos A.", "lastName": "Vison", "identNumber": "65263146", "note": "nota de prueba", "cardNumber": 7306735, "orgId": 1, "visitedOrgId": 5, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Carlos R.", "lastName": "Vasquez", "identNumber": "36043156", "note": "nota de prueba", "cardNumber": 4310747, "orgId": 1, "visitedOrgId": 6, "isProvider": 1}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"names": "Tatiana", "lastName": "Rodriguez", "identNumber": "29063356", "note": "nota de prueba", "cardNumber": 8304763, "orgId": 1, "visitedOrgId": 7, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person



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
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"names": "Soledad Rocio", "lastName": "Tapia", "identNumber": "24573247", "note": "nota modificada", "cardNumber": 5300817, "orgId": 7, "visitedOrgId": null, "isProvider": 0}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/16

#Waiting 3 seconds to let database finish de insertion of the accesses and then delete persons
sleep 3

#Deleting Ruben Pecamenta
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/15

#Simulating some visitors leaving the building
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/19
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/22
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/person/20


#ReProvisioning Controladora 2
sleep 4
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{}' http://$BCKND_DOCKER_IP:5000/api/v1.0/controller/1/resync


#Creating deleting and modifying some system users
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "jcabelo", "passwd": "qwe123qwe", "fullName": "Juan Cabelo", "roleId": 1, "language": "en", "active": 1, "orgId": null}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "rtortoza", "passwd": "qwe123qwe", "fullName": "Ramon Tortoza", "roleId": 2, "language": "en", "active": 1, "orgId": null}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "lcabrera", "passwd": "qwe123qwe", "fullName": "Luis Cabrera", "roleId": 3, "language": "es", "active": 1, "orgId": null}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X DELETE -d '{}' http://localhost:5000/api/v1.0/user/4
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "asorini", "passwd": "qwe123", "fullName": "Andrea Sorini", "roleId": 4, "language": "en", "active": 1, "orgId": 3}' http://localhost:5000/api/v1.0/user
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"username": "asorini", "passwd": "qwe123qwe", "roleId": 4, "language": "es", "active": 1}' http://localhost:5000/api/v1.0/user/5
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"username": "asorini", "roleId": 4, "language": "es", "active": 1, "orgId": 5}' http://localhost:5000/api/v1.0/user/5
curl -u admin:admin -i -H "Content-Type: application/json" -X POST -d '{"username": "jorklein", "passwd": "qwe123qwe", "fullName": "Jor Kleinerman", "roleId": 4, "language": "en", "active": 1, "orgId": 2}' http://localhost:5000/api/v1.0/user


#Modifying Admin password
curl -u admin:admin -i -H "Content-Type: application/json" -X PUT -d '{"passwd": "qwe123qwe"}' http://localhost:5000/api/v1.0/user/1
curl -u admin:qwe123qwe -i -H "Content-Type: application/json" -X PUT -d '{"passwd": "admin"}' http://localhost:5000/api/v1.0/user/1



#Generating some Events
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

echo "User jorklein trying to retrieve persons from his Organization (Allowed)"
curl -u jorklein:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/organization/2/person

echo "User jorklein trying to retrieve persons from another Organization (Forbidden)"
curl -u jorklein:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/organization/5/person

echo "Admin trying to retrieve persons from any Organization (Of course Allowed)"
curl -u admin:admin -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/organization/3/person

echo "jcabelo (not-org-usr) trying to retrieve persons from any Organization (Of course Allowed)"
curl -u jcabelo:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/organization/3/person

echo "User jorklein trying to retrieve doors from his Organization (Allowed)"
curl -u jorklein:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/doorgroup/6/door

echo "User jorklein trying to retrieve doors from another Organization (Forbiden)"
curl -u jorklein:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/doorgroup/3/door

echo "Admin trying to retrieve from any Organization (Of course Allowed)"
curl -u admin:admin -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/doorgroup/7/door

echo "rtortoza (not-org-usr) trying to retrieve from any Organization (Of course Allowed)"
curl -u rtortoza:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/doorgroup/7/door

echo "The Organization of org-user jorklein has two Door Groups. Retrieving them..."
curl -u jorklein:qwe123qwe -i -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:5000/api/v1.0/doorgroup