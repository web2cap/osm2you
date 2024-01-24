#!/bin/bash

python manage.py migrate
yes yes | python manage.py collectstatic
python manage.py firststart

gunicorn osm2you.wsgi:application --bind 0:8000