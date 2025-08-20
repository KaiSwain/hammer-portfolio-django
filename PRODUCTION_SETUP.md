# Production Setup Guide

## Overview
This document outlines the steps taken to make the Hammer Portfolio Django application production-ready, including security configurations, environment management, and deployment setup.

## Application Architecture
- **Backend**: Django REST API with PostgreSQL database
- **Frontend**: Next.js React application
- **Features**: PDF certificate generation, AI-powered personality summaries, student management

## Production Changes Made

### 1. Environment Configuration
- Created separate development and production settings
- Implemented secure environment variable management
- Added production-specific configurations

### 2. Security Enhancements
- Separated SECRET_KEY from source code
- Configured secure ALLOWED_HOSTS
- Added security middleware
- Implemented HTTPS settings
- Added CSRF protection

### 3. Database Configuration
- Environment-based database configuration
- Production PostgreSQL setup
- Database connection pooling

### 4. Static Files & Media
- Configured static file serving for production
- Added media file handling
- Implemented file storage optimization

### 5. Logging & Monitoring
- Added comprehensive logging configuration
- Error tracking setup
- Performance monitoring

### 6. Deployment Configuration
- Docker containerization
- Production requirements
- Deployment scripts

## Quick Start for Production

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Environment Setup

1. **Create production environment file:**
```bash
cp back/.env.example back/.env.production
```

2. **Configure environment variables in `.env.production`:**
```
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/hammer_portfolio_prod
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

3. **Install dependencies:**
```bash
# Backend
cd back
pip install -r requirements.txt

# Frontend
cd ../front
npm install
```

4. **Database setup:**
```bash
cd back
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

5. **Build frontend:**
```bash
cd front
npm run build
```

### Running in Production

#### Option 1: Manual Setup
```bash
# Backend (with Gunicorn)
cd back
gunicorn hammer_backendproject.wsgi:application --bind 0.0.0.0:8000

# Frontend
cd front
npm start
```

#### Option 2: Docker (Recommended)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Security Checklist

- [x] SECRET_KEY moved to environment variables
- [x] DEBUG set to False in production
- [x] ALLOWED_HOSTS properly configured
- [x] Database credentials secured
- [x] HTTPS enforced
- [x] CSRF protection enabled
- [x] Security headers configured
- [x] Static files served securely

## Monitoring & Maintenance

### Health Checks
- Backend: `GET /admin/` (should return 200)
- Database: Connection monitoring
- Frontend: Application loading time

### Logs
- Django logs: `/var/log/django/`
- Application errors tracked
- Performance metrics collected

### Backups
- Database: Daily automated backups
- Media files: Regular synchronization
- Configuration: Version controlled

## Deployment Environments

### Development
- `python manage.py runserver`
- `npm run dev`
- SQLite database
- Debug mode enabled

### Staging
- Gunicorn WSGI server
- `npm run build && npm start`
- PostgreSQL database
- Debug mode disabled
- Production-like environment

### Production
- Gunicorn + Nginx
- Static file serving optimized
- PostgreSQL with connection pooling
- Full security configurations
- Monitoring and logging

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT configuration

2. **Database connection errors**
   - Verify DATABASE_URL in environment
   - Check PostgreSQL service status

3. **CORS errors**
   - Update CORS_ALLOWED_ORIGINS
   - Verify frontend URL configuration

4. **OpenAI API errors**
   - Check OPENAI_API_KEY validity
   - Verify API quota limits

### Performance Optimization

1. **Database**
   - Enable connection pooling
   - Add database indexes
   - Optimize queries

2. **Frontend**
   - Enable Next.js Image optimization
   - Implement code splitting
   - Add caching headers

3. **Backend**
   - Enable Django caching
   - Use Redis for sessions
   - Optimize API responses

## Support & Maintenance

- Regular security updates
- Performance monitoring
- Backup verification
- Log rotation
- Certificate renewals (if using HTTPS)

---

**Created**: August 18, 2025
**Last Updated**: August 18, 2025
**Version**: 1.0.0
