# VPS Deployment Guide
# Deploy your Hammer Portfolio to any VPS with custom domain

## Prerequisites
- VPS server (DigitalOcean Droplet, Linode, AWS EC2, etc.)
- Domain name (GoDaddy, Namecheap, etc.)
- SSH access to your server

## Step 1: Server Setup
```bash
# On your VPS server
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose git nginx certbot python3-certbot-nginx -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

## Step 2: Clone and Configure
```bash
# Clone your repository
git clone https://github.com/YourUsername/hammer-portfolio-django.git
cd hammer-portfolio-django

# Update production environment
nano back/.env.production
```

## Step 3: Update Environment for Production
```env
# back/.env.production
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (using Docker PostgreSQL)
DB_NAME=hammer_portfolio_prod
DB_USER=postgres
DB_PASSWORD=your-secure-password-here
DB_HOST=db
DB_PORT=5432

# Your API keys
OPENAI_API_KEY=your-openai-key-here

# CORS for your domain
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Step 4: Update Docker Compose for Production
```yaml
# docker-compose.prod.yml - Update ports for web access
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"      # HTTP
      - "443:443"    # HTTPS
    depends_on:
      - frontend
      - backend
```

## Step 5: Deploy
```bash
# Run deployment
chmod +x deploy.sh
./deploy.sh
```

## Step 6: Domain Setup
1. Point your domain DNS to your VPS IP address
2. Set up SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Access URLs
- **Your Domain**: https://yourdomain.com
- **Admin Panel**: https://yourdomain.com/admin/
- **API**: https://yourdomain.com/api/
