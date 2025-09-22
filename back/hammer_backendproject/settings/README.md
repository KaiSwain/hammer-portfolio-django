# Settings Structure

Your Django settings have been reorganized into a cleaner structure for better maintainability.

## File Structure

```
back/hammer_backendproject/
├── settings.py              # Legacy compatibility file (auto-detects environment)
└── settings/
    ├── __init__.py         # Auto-detection logic
    ├── base.py             # Common settings shared by all environments
    ├── development.py      # Development-specific settings
    ├── production.py       # Production-specific settings
    └── testing.py          # Test-specific settings
```

## How It Works

The system automatically detects your environment using the `DJANGO_ENVIRONMENT` variable:

- **Development**: Set `DJANGO_ENVIRONMENT=development`
- **Production**: Set `DJANGO_ENVIRONMENT=production` (or don't set it - defaults to production)
- **Testing**: Set `DJANGO_ENVIRONMENT=testing`

## Usage

### Option 1: Automatic Detection (Recommended)
```bash
# For development
export DJANGO_ENVIRONMENT=development
python manage.py runserver

# For production (default)
export DJANGO_ENVIRONMENT=production
python manage.py runserver

# For testing
export DJANGO_ENVIRONMENT=testing
python manage.py test
```

### Option 2: Explicit Settings Module
```bash
# Development
python manage.py runserver --settings=hammer_backendproject.settings.development

# Production
python manage.py runserver --settings=hammer_backendproject.settings.production

# Testing
python manage.py test --settings=hammer_backendproject.settings.testing
```

## What's Different

### Development Settings (`settings/development.py`)
- `DEBUG = True`
- SQLite database by default (fast and simple)
- Permissive CORS settings
- Verbose logging
- Security features disabled for easier debugging

### Production Settings (`settings/production.py`)
- `DEBUG = False`
- PostgreSQL database (via DATABASE_URL)
- Restrictive CORS settings
- Security features enabled (HTTPS, HSTS, etc.)
- Error logging to files

### Testing Settings (`settings/testing.py`)
- In-memory SQLite database (fastest)
- Minimal logging
- Fast password hashing
- Migrations disabled

## Environment Variables

The system will look for these environment variables based on your environment:

### Development (`.env.development` file supported)
```bash
DJANGO_ENVIRONMENT=development
DJANGO_DEBUG=True
POSTGRES_DB=hammer_dev
POSTGRES_USER=hammer_dev_user
POSTGRES_PASSWORD=hammer_dev_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
OPENAI_API_KEY=your_api_key
```

### Production (Railway/platform environment variables)
```bash
DJANGO_ENVIRONMENT=production
DATABASE_URL=postgresql://...
OPENAI_API_KEY=your_api_key
ALLOWED_HOSTS=your-domain.com,*.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

## Migration from Old Settings

Your old `settings.py` file is now a compatibility layer that automatically loads the right environment settings. No changes needed to your existing deployment - it will continue working exactly as before!

## Benefits

✅ **Clear separation** between environments
✅ **Easier debugging** - know exactly which settings are loaded
✅ **Better security** - production settings are isolated
✅ **Maintainable** - common settings in one place
✅ **Backward compatible** - existing deployments keep working