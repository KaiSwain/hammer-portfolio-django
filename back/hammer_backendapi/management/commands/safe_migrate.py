from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import traceback


class Command(BaseCommand):
    help = 'Safely initialize database with proper migration order'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Starting safe database initialization...')
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT version();')
                version = cursor.fetchone()[0]
                self.stdout.write(f'✅ Database connected: {version[:50]}...')
        except Exception as e:
            self.stdout.write(f'❌ Database connection failed: {e}')
            return
            
        # Check if django_migrations table exists
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'django_migrations'
                    );
                """)
                migrations_table_exists = cursor.fetchone()[0]
                
                if migrations_table_exists:
                    self.stdout.write('✅ django_migrations table exists')
                else:
                    self.stdout.write('⚠️  django_migrations table does not exist - will be created')
        except Exception as e:
            self.stdout.write(f'⚠️  Could not check migrations table: {e}')
            
        # Run migrations in order
        migration_apps = [
            'contenttypes',
            'auth', 
            'admin',
            'sessions',
            'hammer_backendapi',
        ]
        
        for app in migration_apps:
            try:
                self.stdout.write(f'📦 Migrating {app}...')
                call_command('migrate', app, verbosity=0, interactive=False)
                self.stdout.write(f'✅ {app} migrations completed')
            except Exception as e:
                self.stdout.write(f'❌ {app} migration failed: {e}')
                # Continue with other apps
                
        # Final migration to catch any remaining
        try:
            self.stdout.write('📦 Running final migration sweep...')
            call_command('migrate', verbosity=0, interactive=False)
            self.stdout.write('✅ All migrations completed')
        except Exception as e:
            self.stdout.write(f'⚠️  Final migration had issues: {e}')
            
        self.stdout.write('🎉 Database initialization complete!')
