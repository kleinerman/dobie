#!/bin/bash

docker container stop backend
cd ../server/scripts
./db_create_drop.sh -r
docker container start backend
