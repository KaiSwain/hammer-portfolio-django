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
# Use production database if DATABASE_URL is provided, otherwise use local PostgreSQL
import dj_database_url

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Use production database (Railway PostgreSQL)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    DATABASES['default'].update({
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    })
    print("[SETTINGS] Development mode using production database (Railway)")
else:
    # Use local PostgreSQL for development
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
    print("[SETTINGS] Development mode using local PostgreSQL database")

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

# AWS S3 Configuration for File Storage (same as production)
# Check if AWS credentials are provided to use S3, otherwise fallback to local storage
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
USE_S3 = bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)

if USE_S3:
    # AWS S3 Settings for media files (identical to production)
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='myhammerfiles')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    
    # Use custom domain from env var if provided, otherwise construct it
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com')
    # Remove https:// if present in the domain
    if AWS_S3_CUSTOM_DOMAIN.startswith('https://'):
        AWS_S3_CUSTOM_DOMAIN = AWS_S3_CUSTOM_DOMAIN.replace('https://', '')
    
    AWS_DEFAULT_ACL = 'private'  # Student files should be private
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Use S3 for media files (Django 4.2+ style)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "region_name": AWS_S3_REGION_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "default_acl": AWS_DEFAULT_ACL,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
                "querystring_auth": True,  # Generate signed URLs for private files
                "querystring_expire": 3600,  # URLs expire in 1 hour
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Fallback for older Django versions
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    print("[SETTINGS] Development mode using S3 for file storage")
else:
    # Use local storage as fallback
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    print("[SETTINGS] Development mode using local file storage (no S3 credentials found)")

# Security settings (disabled for development)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# AWS S3 Configuration for Development
# Use S3 if AWS credentials are provided in .env.development
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
USE_S3 = AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

if USE_S3:
    # AWS S3 Settings for media files (same as production)
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='myhammerfiles')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    
    # Use custom domain from env var if provided, otherwise construct it
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com')
    # Remove https:// if present in the domain
    if AWS_S3_CUSTOM_DOMAIN.startswith('https://'):
        AWS_S3_CUSTOM_DOMAIN = AWS_S3_CUSTOM_DOMAIN.replace('https://', '')
    
    AWS_DEFAULT_ACL = 'private'  # Student files should be private
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Use S3 for media files (Django 4.2+ style)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "region_name": AWS_S3_REGION_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "default_acl": AWS_DEFAULT_ACL,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Fallback for older Django versions
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    print("[SETTINGS] Development: Using S3 for file storage")
else:
    # Use local storage as fallback
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    print("[SETTINGS] Development: Using local file storage")