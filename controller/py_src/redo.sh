#!/bin/bash

#Create and fill database

rm access.db
./create-db.py
./fill-db.py
