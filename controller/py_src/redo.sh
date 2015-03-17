#!/bin/bash

rm access.db
./create-db.py
./fill-db.py
