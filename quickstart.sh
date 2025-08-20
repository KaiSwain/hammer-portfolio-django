#!/bin/bash

# Quick Start Script for Hammer Portfolio Development
# This script sets up the development environment quickly

set -e  # Exit on any error

echo "🔨 Hammer Portfolio - Quick Start"
echo "================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3.12 or later."
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version="3.12"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        log_error "Python 3.12 or later is required. Found: $python_version"
        exit 1
    fi
    
    log_info "Python version check passed ✅"
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js 18 or later."
        exit 1
    fi
    
    node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -lt 18 ]; then
        log_error "Node.js 18 or later is required. Found: v$(node --version)"
        exit 1
    fi
    
    log_info "Node.js version check passed ✅"
}

# Setup backend
setup_backend() {
    log_info "Setting up Django backend..."
    
    cd back
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Setup environment file
    if [ ! -f ".env.development" ]; then
        log_info "Creating development environment file..."
        cp .env.example .env.development
        log_warn "Please edit back/.env.development with your settings (especially OPENAI_API_KEY)"
    fi
    
    # Run migrations
    log_info "Running database migrations..."
    python manage.py migrate
    
    # Create superuser (optional)
    if [ "$1" = "--create-admin" ]; then
        log_info "Creating admin user..."
        python manage.py setup_production --admin-email admin@localhost --admin-password admin123 --skip-superuser=false
    fi
    
    cd ..
    log_info "Backend setup completed ✅"
}

# Setup frontend
setup_frontend() {
    log_info "Setting up Next.js frontend..."
    
    cd front
    
    # Install dependencies
    log_info "Installing Node.js dependencies..."
    npm install
    
    # Setup environment file
    if [ ! -f ".env.development" ]; then
        log_info "Creating development environment file..."
        cp .env.example .env.development
    fi
    
    cd ..
    log_info "Frontend setup completed ✅"
}

# Start services
start_services() {
    log_info "Starting development services..."
    
    # Start backend
    log_info "Starting Django backend on http://localhost:8000"
    cd back
    source venv/bin/activate
    python manage.py runserver &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    log_info "Starting Next.js frontend on http://localhost:3000"
    cd front
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "🎉 Development environment is ready!"
    echo ""
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend:  http://localhost:8000"
    echo "👤 Admin:    http://localhost:8000/admin/"
    echo "📊 API:      http://localhost:8000/api/"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Wait for user to stop services
    trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
    wait $BACKEND_PID $FRONTEND_PID
}

# Main function
main() {
    echo "Checking prerequisites..."
    check_python
    check_node
    
    echo ""
    setup_backend "$1"
    
    echo ""
    setup_frontend
    
    echo ""
    if [ "$1" = "--start" ] || [ "$2" = "--start" ]; then
        start_services
    else
        echo "🎉 Setup completed!"
        echo ""
        echo "To start the development servers:"
        echo "  ./quickstart.sh --start"
        echo ""
        echo "Or manually:"
        echo "  # Backend"
        echo "  cd back && source venv/bin/activate && python manage.py runserver"
        echo ""
        echo "  # Frontend"  
        echo "  cd front && npm run dev"
        echo ""
    fi
}

# Handle arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "start")
        start_services
        ;;
    "--start")
        main --start
        ;;
    "--create-admin")
        main --create-admin
        ;;
    "--help"|"-h")
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  setup            Setup development environment (default)"
        echo "  start            Start development services only"
        echo "  --start          Setup and start services"
        echo "  --create-admin   Setup and create admin user"
        echo "  --help, -h       Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                    # Setup only"
        echo "  $0 --start           # Setup and start"
        echo "  $0 --create-admin    # Setup with admin user"
        echo "  $0 start             # Start services only"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use --help for available options"
        exit 1
        ;;
esac
