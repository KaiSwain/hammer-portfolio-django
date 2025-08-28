from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Initialize database for DigitalOcean deployment'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database...')
        
        try:
            with connection.cursor() as cursor:
                # Check connection
                cursor.execute('SELECT version();')
                version = cursor.fetchone()[0]
                self.stdout.write(f'✅ Connected to: {version[:50]}...')
                
                # Check current user and database
                cursor.execute('SELECT current_user, current_database();')
                user, db = cursor.fetchone()
                self.stdout.write(f'✅ User: {user}, Database: {db}')
                
                # Check if django_migrations table exists
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'django_migrations'
                    );
                """)
                exists = cursor.fetchone()[0]
                
                if exists:
                    self.stdout.write('✅ django_migrations table exists')
                else:
                    self.stdout.write('⚠️  django_migrations table does not exist')
                    
                # Check schema permissions
                try:
                    cursor.execute('CREATE TABLE _test_permissions (id integer);')
                    cursor.execute('DROP TABLE _test_permissions;')
                    self.stdout.write('✅ Schema permissions OK')
                except Exception as e:
                    self.stdout.write(f'❌ Schema permission error: {e}')
                    self.stdout.write('Attempting to grant permissions...')
                    try:
                        cursor.execute('GRANT ALL ON SCHEMA public TO current_user;')
                        self.stdout.write('✅ Permissions granted')
                    except Exception as grant_error:
                        self.stdout.write(f'❌ Could not grant permissions: {grant_error}')
                        
        except Exception as e:
            self.stdout.write(f'❌ Database initialization failed: {e}')
            return
            
        # Try to run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=1, interactive=False)
            self.stdout.write('✅ Migrations completed successfully')
        except Exception as e:
            self.stdout.write(f'❌ Migration failed: {e}')
            # Try fake-initial as fallback
            try:
                self.stdout.write('Trying fake-initial...')
                call_command('migrate', fake_initial=True, verbosity=1, interactive=False)
                self.stdout.write('✅ Migrations completed with fake-initial')
            except Exception as fake_error:
                self.stdout.write(f'❌ Fake-initial also failed: {fake_error}')
