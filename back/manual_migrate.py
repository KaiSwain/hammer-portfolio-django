#!/usr/bin/env python
"""
Manual migration script for troubleshooting
Run this if automatic migrations fail
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model

def check_database():
    """Check database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT version();')
            result = cursor.fetchone()
            print(f'✅ Database connected: {result[0]}')
            return True
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

def check_tables():
    """Check if Django tables exist"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='auth_user';")
            count = cursor.fetchone()[0]
            if count > 0:
                print('✅ auth_user table exists')
                return True
            else:
                print('❌ auth_user table does not exist')
                return False
    except Exception as e:
        print(f'❌ Error checking tables: {e}')
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print('Running makemigrations...')
        call_command('makemigrations', verbosity=2)
        
        print('Running migrate...')
        call_command('migrate', verbosity=2)
        
        print('✅ Migrations completed successfully')
        return True
    except Exception as e:
        print(f'❌ Migration failed: {e}')
        return False

def create_admin_user():
    """Create admin user"""
    try:
        User = get_user_model()
        if User.objects.filter(username='admin').exists():
            print('✅ Admin user already exists')
        else:
            User.objects.create_superuser('admin', 'admin@hammermath.com', 'HammerAdmin2025!')
            print('✅ Admin user created: admin / HammerAdmin2025!')
        return True
    except Exception as e:
        print(f'❌ Failed to create admin user: {e}')
        return False

def main():
    print("=== Manual Migration Script ===")
    
    # Step 1: Check database connection
    if not check_database():
        sys.exit(1)
    
    # Step 2: Check if tables exist
    tables_exist = check_tables()
    
    # Step 3: Run migrations if needed
    if not tables_exist:
        print("\nTables missing - running migrations...")
        if not run_migrations():
            sys.exit(1)
        
        # Check again
        if not check_tables():
            print("❌ Migrations ran but tables still missing")
            sys.exit(1)
    
    # Step 4: Create admin user
    create_admin_user()
    
    print("\n✅ All setup complete!")
    print("You can now access the admin panel at: /admin/")
    print("Username: admin")
    print("Password: HammerAdmin2025!")

if __name__ == '__main__':
    main()
