#!/bin/bash
# Exit on critical errors (fail fast)
set -e

# Startup script for DigitalOcean deployment
echo "Starting Django application..."

# Set default port if not provided
export PORT=${PORT:-8080}

# Show environment info for debugging
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"
echo "Port: $PORT"

# Read Django settings to verify environment variables
echo "Reading Django settings..."
python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()
from django.conf import settings
print("ALLOWED_HOSTS (settings):", settings.ALLOWED_HOSTS)
print("CSRF_TRUSTED_ORIGINS (settings):", settings.CSRF_TRUSTED_ORIGINS)
PY

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

# Quick database connectivity check (non-blocking)
echo "Checking database connectivity..."
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
        
        # Check if tables exist (non-blocking)
        cursor.execute(\"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='auth_user';\")
        count = cursor.fetchone()[0]
        if count > 0:
            print('✅ auth_user table exists - migrations handled by PRE_DEPLOY job')
        else:
            print('⚠️  auth_user table does not exist - PRE_DEPLOY job will handle migrations')
            
except Exception as e:
    print(f'⚠️  Database check failed: {e}')
    print('This is OK - app will still start and /healthz will work')
"

# Start the Gunicorn server (always succeeds)
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
