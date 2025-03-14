#!/bin/sh
set -e

mkdir -p /app/data

python manage.py migrate

exec gunicorn find_movie.wsgi:application --bind 0.0.0.0:8000