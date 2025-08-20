#!/bin/bash

rm db.sqlite3
rm -rf ./hammer_backendapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations hammer_backendapi
python3 manage.py migrate hammer_backendapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

