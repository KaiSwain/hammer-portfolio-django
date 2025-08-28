#!/bin/bash

# Startup script for DigitalOcean deployment
echo "Starting Django application..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Check if migrations were successful
if [ $? -eq 0 ]; then
    echo "Migrations completed successfully"
else
    echo "Migration failed, but continuing..."
fi

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT
