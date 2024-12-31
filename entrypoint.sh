#!/bin/bash

dockerize -wait tcp://"${POSTGRES_HOST}":"${POSTGRES_PORT}" -timeout 0.1s

echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py initadmin
python manage.py runserver 0.0.0.0:8000