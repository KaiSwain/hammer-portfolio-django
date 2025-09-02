#!/bin/bash
set -e

echo "Starting Django deployment..."

# Skip system packages for now - they need root permissions
# Focus on getting the app running first
echo "System dependencies require root - WeasyPrint will be disabled for now"

# Install/upgrade Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed, continuing..."

# Run migrations with better error handling
echo "Running database migrations..."
if python manage.py showmigrations | grep -q "\[ \]"; then
    echo "Unapplied migrations found, attempting to migrate..."
    python manage.py migrate --noinput || echo "Migration failed - may need manual database setup"
else
    echo "No pending migrations or migration check failed"
fi

# Use PORT environment variable if set, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting gunicorn on port $PORT"

# Start gunicorn
exec gunicorn hammer_backendproject.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
