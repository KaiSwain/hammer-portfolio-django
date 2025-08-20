# Hammer Portfolio Django Application

A comprehensive student portfolio management system built with Django REST Framework and Next.js, featuring automated certificate generation and AI-powered personality summaries.

## 🚀 Features

- **Student Management**: Complete student profile management with training records
- **Certificate Generation**: Automated PDF certificate generation for various certifications
- **AI Integration**: OpenAI-powered personality summaries and assessments
- **Authentication**: Token-based authentication system
- **RESTful API**: Comprehensive API for all operations
- **Responsive Frontend**: Modern React/Next.js frontend interface
- **Production Ready**: Docker containerization and production configurations

## 📋 Requirements

### System Requirements
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)

### Dependencies
- Django 5.2.4
- Django REST Framework
- Next.js 15.4.4
- PostgreSQL
- OpenAI API
- PDF generation libraries (PyMuPDF, borb)

## 🛠️ Installation & Setup

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KaiSwain/hammer-portfolio-django.git
   cd hammer-portfolio-django
   ```

2. **Backend Setup:**
   ```bash
   cd back
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup environment
   cp .env.example .env.development
   # Edit .env.development with your settings
   
   # Setup database
   python manage.py migrate
   python manage.py setup_production --admin-email your-email@domain.com --admin-password your-secure-password
   
   # Start development server
   python manage.py runserver
   ```

3. **Frontend Setup:**
   ```bash
   cd front
   
   # Install dependencies
   npm install
   
   # Setup environment
   cp .env.example .env.development
   # Edit .env.development with your settings
   
   # Start development server
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

### Production Deployment

1. **Prepare environment:**
   ```bash
   # Backend
   cp back/.env.example back/.env.production
   # Edit .env.production with production settings
   
   # Frontend  
   cp front/.env.example front/.env.production
   # Edit .env.production with production settings
   ```

2. **Deploy with Docker:**
   ```bash
   # Make deploy script executable
   chmod +x deploy.sh
   
   # Run deployment
   ./deploy.sh deploy
   ```

3. **Manual deployment:**
   ```bash
   # Build and start containers
   docker-compose -f docker-compose.prod.yml up -d
   
   # Run initial setup
   docker-compose -f docker-compose.prod.yml exec backend python manage.py setup_production --admin-email admin@yourdomain.com --admin-password your-secure-password
   ```

## 🔧 Configuration

### Environment Variables

#### Backend (.env.production)
```env
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/hammer_portfolio_prod
OPENAI_API_KEY=your-openai-api-key
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

#### Frontend (.env.production)
```env
NEXT_PUBLIC_API_URL=https://yourdomain.com
NEXT_PUBLIC_APP_NAME="Hammer Portfolio"
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Security Configuration

The application includes production-ready security settings:
- HTTPS enforcement
- Security headers (XSS, CSRF, Content-Type)
- Secure cookies
- Rate limiting
- Input validation

## 📊 API Documentation

### Authentication
```bash
POST /api/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

### Students
```bash
# List students
GET /api/students/

# Create student
POST /api/students/
Authorization: Token your-token-here

# Update student
PUT /api/students/{id}/
Authorization: Token your-token-here

# Delete student
DELETE /api/students/{id}/
Authorization: Token your-token-here
```

### Certificate Generation
```bash
# Generate all certificates
POST /api/generate/all/
Authorization: Token your-token-here
Content-Type: application/json

{
  "student": {
    "full_name": "John Doe",
    "end_date": "2025-12-31",
    // ... other student data
  }
}
```

### Health Check
```bash
GET /api/health/
GET /health/  # Root level for load balancers
```

## 🐳 Docker Support

### Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production
```bash
# Deploy production environment
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Update services
./deploy.sh deploy
```

## 📝 Management Commands

```bash
# Setup production environment
python manage.py setup_production --admin-email admin@domain.com --admin-password secure-password

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Load fixtures (if available)
python manage.py loaddata fixtures/initial_data.json
```

## 🔍 Monitoring & Maintenance

### Health Checks
- Backend: `GET /health/`
- Database: Connection monitoring via health checks
- Frontend: Application loading verification

### Logs
- Django logs: `back/logs/django.log`
- Container logs: `docker-compose logs`
- Nginx logs: `docker-compose exec nginx cat /var/log/nginx/access.log`

### Backups
```bash
# Database backup
./deploy.sh backup

# Manual backup
docker exec hammer_postgres_prod pg_dump -U postgres hammer_portfolio_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 🚨 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database connection errors**
   - Check DATABASE_URL in environment
   - Verify PostgreSQL service status
   - Check firewall settings

3. **CORS errors**
   - Update CORS_ALLOWED_ORIGINS in backend settings
   - Verify frontend URL configuration

4. **Certificate generation errors**
   - Check PDF templates exist in static folder
   - Verify file permissions
   - Check logs for detailed error messages

### Performance Optimization

1. **Database**
   - Add indexes for frequently queried fields
   - Enable connection pooling
   - Optimize queries with select_related/prefetch_related

2. **Frontend**
   - Enable Next.js Image optimization
   - Implement code splitting
   - Add caching headers

3. **Backend**
   - Enable Django caching
   - Use Redis for sessions
   - Implement API rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md) for detailed deployment instructions
- Review logs for debugging information

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (Django)      │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx         │
                    │   (Reverse      │
                    │    Proxy)       │
                    │   Port: 80/443  │
                    └─────────────────┘
```

---

**Version**: 1.0.0  
**Last Updated**: August 18, 2025  
**Maintainer**: KaiSwain
