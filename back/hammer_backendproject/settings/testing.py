"""
Testing settings for Hammer Portfolio Django Backend

Settings for running tests with fast database and minimal logging.
"""

from .base import *

# Test mode settings
DEBUG = False

# Test database (fast in-memory SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Test allowed hosts
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Disable logging during tests
LOGGING_CONFIG = None

# Fast password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Simple cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Security settings (disabled for testing)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False