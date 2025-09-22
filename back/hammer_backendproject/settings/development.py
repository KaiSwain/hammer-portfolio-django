"""
Development settings for Hammer Portfolio Django Backend

Settings for local development with debug mode enabled.
Uses environment variables from .env.development file if it exists.
"""

from decouple import config, Config, RepositoryEnv
from .base import *
import os

# Load development environment variables
env_file = BASE_DIR / '.env.development'
if env_file.exists():
    config = Config(RepositoryEnv(env_file))
    print("[SETTINGS] Using development mode - reading from .env.development")
else:
    print("[SETTINGS] Warning: .env.development not found, using system environment variables")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Development allowed hosts (more permissive)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '.localhost',
    '127.0.0.1:8000',
    'localhost:8000',
]

# CORS settings for development (more permissive)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3001',
]

CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# Database configuration for development
# Using Docker PostgreSQL for better production parity
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='hammer_dev'),
        'USER': config('POSTGRES_USER', default='hammer_dev_user'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='hammer_dev_password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5433'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Fallback to SQLite if you prefer (uncomment the lines below and comment the PostgreSQL config above)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'dev_db.sqlite3',
#     }
# }

# Development logging (more verbose)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'hammer_backendapi': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Security settings (disabled for development)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'