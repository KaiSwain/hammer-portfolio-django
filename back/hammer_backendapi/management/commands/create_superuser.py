from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError
import secrets
import string

class Command(BaseCommand):
    help = 'Create a superuser for admin access with secure password'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for superuser')
        parser.add_argument('--email', type=str, default='admin@hammer-portfolio.com', help='Email for superuser')
        parser.add_argument('--password', type=str, default=None, help='Password for superuser (if not provided, will generate secure random password)')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists')
                )
                return

            # Generate secure random password if not provided
            if not password:
                # Generate 16-character secure password with letters, digits, and symbols
                alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
                password = ''.join(secrets.choice(alphabet) for _ in range(16))

            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            # Only log password in deployment logs (not stored in code)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Admin password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('IMPORTANT: Change this password after first login!')
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )
