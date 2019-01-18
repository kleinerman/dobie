#!/bin/bash

#Create and fill database

rm /var/lib/dobie-c/dobie-c.db
./create-db.py
./init-db.py
#./fill-db.py
