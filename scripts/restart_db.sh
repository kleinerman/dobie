#!/bin/bash

docker container stop backend
cd ../server/scripts
./db-create-drop.sh -r
docker container start backend
