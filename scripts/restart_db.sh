#!/bin/bash

docker container stop backend
cd ../server/scripts
./db_create_drop.sh -r 172.18.0.2
docker container start backend
