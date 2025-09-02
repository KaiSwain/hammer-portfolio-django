#!/bin/bash
set -e

echo "Starting Django application..."

# Use PORT environment variable if set, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting gunicorn on port $PORT"

# Run migrations first (safe to run multiple times)
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Start gunicorn
exec gunicorn hammer_backendproject.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
