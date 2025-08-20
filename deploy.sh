#!/bin/bash

# Production Deployment Script for Hammer Portfolio
# This script handles the complete deployment process

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Configuration
PROJECT_NAME="hammer-portfolio"
BACKUP_DIR="./backups"
ENV_FILE="./back/.env.production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file $ENV_FILE not found. Please create it from .env.example"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✅"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."
    mkdir -p $BACKUP_DIR
    
    # Get current timestamp
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
    
    # Create backup if database container is running
    if docker ps | grep -q hammer_postgres_prod; then
        docker exec hammer_postgres_prod pg_dump -U postgres hammer_portfolio_prod > "$BACKUP_FILE"
        log_info "Database backup created: $BACKUP_FILE"
    else
        log_warn "Database container not running, skipping backup"
    fi
}

# Stop existing containers
stop_containers() {
    log_info "Stopping existing containers..."
    docker-compose -f docker-compose.prod.yml down
    log_info "Containers stopped ✅"
}

# Build and start containers
start_containers() {
    log_info "Building and starting containers..."
    
    # Build images
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    # Start containers
    docker-compose -f docker-compose.prod.yml up -d
    
    log_info "Containers started ✅"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    # Wait for database to be ready
    sleep 10
    
    # Run migrations
    docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
    
    # Collect static files
    docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
    
    log_info "Migrations completed ✅"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Wait for services to start
    sleep 30
    
    # Check backend health
    if curl -f http://localhost:8000/admin/ > /dev/null 2>&1; then
        log_info "Backend health check passed ✅"
    else
        log_error "Backend health check failed ❌"
        return 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_info "Frontend health check passed ✅"
    else
        log_error "Frontend health check failed ❌"
        return 1
    fi
    
    # Check nginx health
    if curl -f http://localhost/health > /dev/null 2>&1; then
        log_info "Nginx health check passed ✅"
    else
        log_error "Nginx health check failed ❌"
        return 1
    fi
    
    log_info "All health checks passed ✅"
}

# Cleanup old images
cleanup() {
    log_info "Cleaning up old Docker images..."
    docker image prune -f
    log_info "Cleanup completed ✅"
}

# Main deployment process
main() {
    echo "========================================"
    echo "   Hammer Portfolio Production Deploy"
    echo "========================================"
    
    check_prerequisites
    backup_database
    stop_containers
    start_containers
    run_migrations
    
    if health_check; then
        cleanup
        log_info "🎉 Deployment completed successfully!"
        echo ""
        echo "Your application is now running at:"
        echo "  Frontend: http://localhost"
        echo "  Backend:  http://localhost/admin/"
        echo "  API:      http://localhost/api/"
        echo ""
        echo "To monitor logs:"
        echo "  docker-compose -f docker-compose.prod.yml logs -f"
        echo ""
    else
        log_error "🚨 Deployment failed during health checks!"
        echo ""
        echo "To check logs:"
        echo "  docker-compose -f docker-compose.prod.yml logs"
        echo ""
        echo "To rollback:"
        echo "  docker-compose -f docker-compose.prod.yml down"
        exit 1
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "backup")
        backup_database
        ;;
    "stop")
        stop_containers
        ;;
    "logs")
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    "status")
        docker-compose -f docker-compose.prod.yml ps
        ;;
    *)
        echo "Usage: $0 [deploy|backup|stop|logs|status]"
        echo ""
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  backup  - Create database backup only"
        echo "  stop    - Stop all containers"
        echo "  logs    - Show container logs"
        echo "  status  - Show container status"
        exit 1
        ;;
esac
