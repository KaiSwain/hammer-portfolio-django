"""
Production settings for Hammer Portfolio Django Backend

Settings for production deployment with security enabled.
Uses environment variables from the deployment platform.
"""

import sys
import os
from decouple import config
from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Check if we're in build mode (collectstatic only, not migrations)
IS_BUILD_TIME = any([
    'collectstatic' in sys.argv,
    'makemigrations' in sys.argv,
    os.getenv('DJANGO_BUILD_MODE') == 'true'
])

# Production allowed hosts configuration
ALLOWED_HOSTS_STR = config(
    'ALLOWED_HOSTS', 
    default=config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1,web-production-f42cb.up.railway.app')
)
ALLOWED_HOSTS = [s.strip() for s in ALLOWED_HOSTS_STR.split(',')] if ALLOWED_HOSTS_STR else ['*']

# Add specific Railway domains and wildcards for hosting platforms
ALLOWED_HOSTS.extend([
    'web-production-f42cb.up.railway.app',  # Current test deployment
    '.railway.app',  # Django wildcard syntax (note the leading dot)
    '.ondigitalocean.app'
])

# CORS settings for production (restrictive)
CORS_ALLOWED_ORIGINS_STR = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://hammer-front-production.up.railway.app'
)
CORS_ALLOWED_ORIGINS = [s.strip() for s in CORS_ALLOWED_ORIGINS_STR.split(',')]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Security: Only allow specified origins

# Database configuration for production
def get_database_config():
    """Get database configuration, with fallback options"""
    # During build time, use dummy database config
    if IS_BUILD_TIME:
        print("[SETTINGS] Build mode detected - using dummy database config")
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    
    database_url = config('DATABASE_URL', default=None)
    
    if database_url:
        db_config = dj_database_url.parse(database_url)
        db_config.update({
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
            'OPTIONS': {
                'connect_timeout': 10,
            }
        })
        return db_config
    else:
        # Fallback to individual environment variables
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB', default='hammer_production'),
            'USER': config('POSTGRES_USER', default='postgres'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('POSTGRES_HOST', default='localhost'),
            'PORT': config('POSTGRES_PORT', default='5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            }
        }

DATABASES = {
    'default': get_database_config()
}

# Production logging configuration
USE_FILE_LOGGING = config('USE_FILE_LOGGING', default=True, cast=bool)

# Create logs directory if it doesn't exist
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

handlers_config = {
    'console': {
        'level': 'WARNING',
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    },
}

if USE_FILE_LOGGING:
    handlers_config['file'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': logs_dir / 'django.log',
        'formatter': 'verbose',
    }

logger_handlers = ['console']
if USE_FILE_LOGGING:
    logger_handlers.append('file')

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
    'handlers': handlers_config,
    'root': {
        'handlers': logger_handlers,
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': logger_handlers,
            'level': 'INFO',
            'propagate': False,
        },
        'hammer_backendapi': {
            'handlers': logger_handlers,
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security settings for production
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email configuration for production
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@hammerportfolio.com')

# Production cache configuration (can be enhanced with Redis later)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# AWS S3 Configuration for File Storage
USE_S3 = config('USE_S3', default=True, cast=bool)

if USE_S3:
    # AWS S3 Settings for media files
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='hammer-portfolio-files')
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
    
    print("[SETTINGS] Using S3 for file storage")
else:
    # Use local storage as fallback
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    print("[SETTINGS] Using local file storage")