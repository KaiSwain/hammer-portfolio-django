#!/bin/bash
set -e

echo "Starting complete Django deployment..."

# Install system dependencies for WeasyPrint
echo "Installing system dependencies..."
apt-get update || echo "apt-get update failed, continuing..."
apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libfontconfig1 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgobject-2.0-0 \
    libcairo-gobject2 \
    libgio-2.0-0 \
    || echo "System package installation failed, will continue without WeasyPrint"

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed, continuing..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

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
