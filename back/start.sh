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

# Database connection check (without migrations)
echo "Checking database connection..."
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
        
        # Check if tables exist
        cursor.execute(\"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='auth_user';\")
        count = cursor.fetchone()[0]
        if count > 0:
            print('✅ auth_user table exists')
        else:
            print('⚠️  auth_user table does not exist - migrations may not have run')
except Exception as e:
    print(f'❌ Database error: {e}')
"

# Start the Gunicorn server
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
