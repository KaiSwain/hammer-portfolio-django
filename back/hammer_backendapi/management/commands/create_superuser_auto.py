from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser for production deployment'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hammermath.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'HammerAdmin2025!')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'✅ Superuser "{username}" already exists')
            return
            
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f'✅ Superuser "{username}" created successfully')
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔑 Password: {password}')
            self.stdout.write('🔗 Access admin at: /admin/')
        except Exception as e:
            self.stdout.write(f'❌ Error creating superuser: {e}')
