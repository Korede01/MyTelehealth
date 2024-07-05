#!/bin/bash

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start server
gunicorn healthco.wsgi:application --bind 0.0.0.0:8000
