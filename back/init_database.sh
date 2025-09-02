#!/bin/bash

# Simple database initialization script for DigitalOcean
echo "🔧 Initializing database for DigitalOcean..."

# Show database connection info
echo "Database URL: ${DATABASE_URL:0:30}..."

# Try to run migrations with different approaches
echo "Attempting migrations..."

# Method 1: Try normal migrations first
if python manage.py migrate --noinput --verbosity=1 2>&1; then
    echo "✅ Normal migrations succeeded"
    migration_success=true
else
    echo "❌ Normal migrations failed, trying alternatives..."
    migration_success=false
fi

# Method 2: If normal migrations failed, try fake-initial
if [ "$migration_success" = false ]; then
    echo "Trying fake-initial migrations..."
    if python manage.py migrate --fake-initial --noinput --verbosity=1 2>&1; then
        echo "✅ Fake-initial migrations succeeded"
        migration_success=true
    else
        echo "❌ Fake-initial migrations also failed"
    fi
fi

# Method 3: Try migrating individual apps if still failing
if [ "$migration_success" = false ]; then
    echo "Trying individual app migrations..."
    for app in contenttypes auth admin sessions; do
        echo "Migrating $app..."
        python manage.py migrate $app --noinput --verbosity=0 2>&1 || echo "Failed to migrate $app"
    done
    
    # Try our custom app last
    python manage.py migrate hammer_backendapi --noinput --verbosity=0 2>&1 || echo "Failed to migrate hammer_backendapi"
fi

# Check if auth_user table exists now
echo "Checking if auth_user table exists..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT COUNT(*) FROM auth_user;\")
        count = cursor.fetchone()[0]
        print(f'✅ auth_user table exists with {count} users')
except Exception as e:
    print(f'❌ auth_user table check failed: {e}')
"

echo "Database initialization complete"
