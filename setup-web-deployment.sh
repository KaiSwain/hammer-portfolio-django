#!/bin/bash

# Web Deployment Script
# This script prepares your app for web deployment

echo "🌐 Preparing for web deployment..."

# Check if domain is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <your-domain.com>"
    echo "Example: $0 mycompany.com"
    exit 1
fi

DOMAIN=$1
echo "Setting up for domain: $DOMAIN"

# Update production environment
cat > back/.env.production << EOF
# Production Environment for $DOMAIN
DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,localhost,127.0.0.1

# Database Configuration
DB_NAME=hammer_portfolio_prod
DB_USER=postgres
DB_PASSWORD=$(openssl rand -base64 32)
DB_HOST=db
DB_PORT=5432

# OpenAI Configuration (update with your key)
OPENAI_API_KEY=your-openai-key-here
OPENAI_MODEL=gpt-4o-mini

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EOF

# Create nginx configuration for the domain
mkdir -p nginx/conf.d
cat > nginx/conf.d/default.conf << EOF
upstream frontend {
    server frontend:3000;
}

upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL configuration (certificates will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # API routes
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Admin routes
    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Static files
    location /static/ {
        proxy_pass http://backend;
    }
    
    # Media files
    location /media/ {
        proxy_pass http://backend;
    }
    
    # Everything else goes to frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Update docker-compose for web deployment
cat > docker-compose.web.yml << EOF
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    container_name: hammer_postgres_prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: \${DB_NAME:-hammer_portfolio_prod}
      POSTGRES_USER: \${DB_USER:-postgres}
      POSTGRES_PASSWORD: \${DB_PASSWORD}
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
      - ./back/db_backup:/backup
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \${DB_USER:-postgres}"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: hammer_redis_prod
    restart: unless-stopped
    volumes:
      - redis_data_prod:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: 
      context: ./back
      dockerfile: Dockerfile
    container_name: hammer_backend_prod
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DJANGO_SETTINGS_MODULE=hammer_backendproject.settings
    env_file:
      - ./back/.env.production
    volumes:
      - ./back/media:/app/media
      - ./back/logs:/app/logs
      - ./back/staticfiles:/app/staticfiles
    expose:
      - "8000"

  frontend:
    build: 
      context: ./front
      dockerfile: Dockerfile
    container_name: hammer_frontend_prod
    restart: unless-stopped
    depends_on:
      backend:
        condition: service_healthy
    environment:
      - NEXT_PUBLIC_API_URL=https://$DOMAIN
    expose:
      - "3000"

  nginx:
    image: nginx:alpine
    container_name: hammer_nginx_prod
    restart: unless-stopped
    depends_on:
      - frontend
      - backend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - /etc/letsencrypt:/etc/letsencrypt:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data_prod:
  redis_data_prod:

networks:
  default:
    name: hammer_prod_network
EOF

echo "✅ Configuration complete for $DOMAIN"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Get a VPS server (DigitalOcean, Linode, etc.)"
echo "3. Point your domain to the server IP"
echo "4. Run this on your server:"
echo "   git clone https://github.com/YourUsername/hammer-portfolio-django.git"
echo "   cd hammer-portfolio-django"
echo "   docker-compose -f docker-compose.web.yml up -d"
echo "   sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "Your app will be available at: https://$DOMAIN"
EOF
