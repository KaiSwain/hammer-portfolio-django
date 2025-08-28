#!/bin/bash
# Exit on critical errors only, but allow some commands to fail gracefully

# Startup script for DigitalOcean deployment
echo "Starting Django application..."

# Set default port if not provided
export PORT=${PORT:-8080}

# Show environment info for debugging
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"
echo "Port: $PORT"
echo "Allowed hosts: $DJANGO_ALLOWED_HOSTS"
echo "CSRF trusted origins: $CSRF_TRUSTED_ORIGINS"

# Check PDF capabilities
echo "Checking PDF generation capabilities..."
python -c "
try:
    import weasyprint
    print('✅ WeasyPrint available')
except ImportError as e:
    print('❌ WeasyPrint not available:', e)
try:
    import fitz
    print('✅ PyMuPDF available')
except ImportError as e:
    print('❌ PyMuPDF not available:', e)
"

# Run database migrations with verbose output
echo "Running database migrations..."
echo "Database URL: ${DATABASE_URL:0:30}..." # Show first 30 chars for debugging

# First, try to connect and show database info
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        result = cursor.fetchone()
        print(f'✅ Database connected: PostgreSQL')
        cursor.execute('SELECT current_user, current_database();')
        user, db = cursor.fetchone()
        print(f'✅ User: {user}, Database: {db}')
except Exception as e:
    print(f'❌ Database connection error: {e}')
    print('Continuing anyway, server might work...')
"

# Initialize database
echo "Step 1: Initializing database..."
./init_database.sh

# Create superuser with inline script (simpler than management command)
echo "Step 2: Creating admin user..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    if User.objects.filter(username='admin').exists():
        print('✅ Superuser admin already exists')
    else:
        User.objects.create_superuser('admin', 'admin@hammermath.com', 'HammerAdmin2025!')
        print('✅ Superuser admin created successfully')
        print('🔑 Username: admin, Password: HammerAdmin2025!')
except Exception as e:
    print(f'❌ Could not create superuser: {e}')
    print('This is expected if auth tables do not exist yet')
"

# Start the Gunicorn server
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
