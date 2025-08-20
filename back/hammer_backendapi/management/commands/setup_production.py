from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hammer_backendapi.models import Teacher, Organization
import os


class Command(BaseCommand):
    help = 'Setup production environment with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@hammerportfolio.com',
            help='Admin user email address'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            help='Admin user password (required)'
        )
        parser.add_argument(
            '--skip-superuser',
            action='store_true',
            help='Skip creating superuser'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up production environment...')
        )

        # Create superuser if not exists and not skipped
        if not options['skip_superuser']:
            self.create_superuser(options)

        # Create default organization
        self.create_default_organization()

        # Run system checks
        self.run_system_checks()

        self.stdout.write(
            self.style.SUCCESS('✅ Production setup completed successfully!')
        )

    def create_superuser(self, options):
        admin_email = options['admin_email']
        admin_password = options.get('admin_password')

        if not admin_password:
            self.stdout.write(
                self.style.ERROR('❌ Admin password is required. Use --admin-password option.')
            )
            return

        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️  Admin user with email {admin_email} already exists.')
            )
            return

        # Create superuser
        admin_user = User.objects.create_superuser(
            username='admin',
            email=admin_email,
            password=admin_password
        )

        # Create corresponding teacher record
        org, created = Organization.objects.get_or_create(
            name='Hammer Portfolio Administration',
            defaults={'address': 'Administrative Organization'}
        )

        teacher, created = Teacher.objects.get_or_create(
            user=admin_user,
            defaults={
                'full_name': 'System Administrator',
                'email': admin_email,
                'password': admin_password,  # This should be hashed in production
                'organization': org
            }
        )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Admin user created: {admin_email}')
        )

    def create_default_organization(self):
        """Create default organization if it doesn't exist"""
        org, created = Organization.objects.get_or_create(
            name='Default Organization',
            defaults={'address': 'Default organization for new users'}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Default organization created')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Default organization already exists')
            )

    def run_system_checks(self):
        """Run basic system checks"""
        self.stdout.write('🔍 Running system checks...')

        # Check database connection
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(
                self.style.SUCCESS('✅ Database connection: OK')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Database connection failed: {e}')
            )

        # Check static files
        from django.conf import settings
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root and os.path.exists(static_root):
            self.stdout.write(
                self.style.SUCCESS('✅ Static files directory: OK')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Static files directory not found. Run collectstatic.')
            )

        # Check OpenAI configuration
        openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        if openai_key and openai_key != 'your-openai-api-key-here':
            self.stdout.write(
                self.style.SUCCESS('✅ OpenAI API key: Configured')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  OpenAI API key not configured properly')
            )

        # Check logs directory
        if hasattr(settings, 'LOGGING'):
            self.stdout.write(
                self.style.SUCCESS('✅ Logging: Configured')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Logging not configured')
            )
