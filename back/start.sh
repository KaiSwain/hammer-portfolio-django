#!/bin/bash
set -e  # Exit on any error

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

# Initialize and run database migrations
echo "Initializing database..."
python manage.py init_db

# Create superuser if it doesn't exist
echo "Setting up admin user..."
python manage.py create_superuser_auto

# Start the Gunicorn server
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
