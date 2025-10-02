#!/bin/bash

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Start gunicorn server
echo "Starting gunicorn on port ${PORT:-8000}..."
gunicorn hammer_backendproject.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120