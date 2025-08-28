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
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
