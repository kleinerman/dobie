#!/bin/bash

#Create and fill database

rm ../py_src/access.db
./create-db.py
./fill-db.py
