#!/bin/bash

# 🧪 PRODUCTION TESTING SCRIPT
# This script tests all production features before deployment

set -e  # Exit on any error

echo "🚀 Starting Production Testing Suite..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass_test() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
    ((TESTS_PASSED++))
}

fail_test() {
    echo -e "${RED}❌ FAIL:${NC} $1"
    ((TESTS_FAILED++))
}

warn_test() {
    echo -e "${YELLOW}⚠️  WARN:${NC} $1"
}

info_test() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

# 1. ENVIRONMENT CONFIGURATION TESTS
echo -e "\n${BLUE}1. Testing Environment Configuration...${NC}"

test_env_files() {
    if [ -f ".env" ]; then
        pass_test "Main .env file exists"
    else
        fail_test "Main .env file missing"
    fi

    if [ -f ".env.development" ]; then
        pass_test ".env.development file exists"
    else
        warn_test ".env.development file missing (optional for development)"
    fi

    if [ -f ".env.production" ]; then
        pass_test ".env.production file exists"
    else
        fail_test ".env.production file missing (required for production)"
    fi
}

test_openai_config() {
    cd back
    OPENAI_KEY=$(python -c "
from decouple import config
import os
try:
    key = config('OPENAI_API_KEY', default='')
    if key and key != 'your-openai-api-key-here' and len(key) > 20:
        print('CONFIGURED')
    else:
        print('NOT_CONFIGURED')
except Exception as e:
    print(f'ERROR: {e}')
")
    cd ..

    if [ "$OPENAI_KEY" = "CONFIGURED" ]; then
        pass_test "OpenAI API key is properly configured"
    else
        fail_test "OpenAI API key not configured or invalid"
    fi
}

# 2. DJANGO BACKEND TESTS
echo -e "\n${BLUE}2. Testing Django Backend...${NC}"

test_django_configuration() {
    cd back
    
    # Test Django settings
    python manage.py check > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        pass_test "Django configuration is valid"
    else
        fail_test "Django configuration has errors"
    fi

    # Test database connection
    python manage.py check --database default > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        pass_test "Database configuration is valid"
    else
        fail_test "Database configuration has errors"
    fi

    # Test static files
    python manage.py collectstatic --noinput --dry-run > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        pass_test "Static files configuration is valid"
    else
        fail_test "Static files configuration has errors"
    fi

    cd ..
}

test_django_server() {
    cd back
    
    # Start Django development server in background
    python manage.py runserver 127.0.0.1:8001 > /dev/null 2>&1 &
    DJANGO_PID=$!
    
    # Wait for server to start
    sleep 5
    
    # Test if server is responding
    if curl -s http://127.0.0.1:8001/api/health/ > /dev/null; then
        pass_test "Django server starts and responds"
    else
        fail_test "Django server not responding"
    fi
    
    # Test health endpoint specifically
    HEALTH_RESPONSE=$(curl -s http://127.0.0.1:8001/api/health/)
    if echo "$HEALTH_RESPONSE" | grep -q "healthy\|status"; then
        pass_test "Health endpoint returns valid response"
    else
        fail_test "Health endpoint not working properly"
    fi
    
    # Clean up
    kill $DJANGO_PID > /dev/null 2>&1 || true
    cd ..
}

# 3. FRONTEND TESTS
echo -e "\n${BLUE}3. Testing Next.js Frontend...${NC}"

test_frontend_dependencies() {
    cd front
    
    if [ -f "package.json" ]; then
        pass_test "Frontend package.json exists"
    else
        fail_test "Frontend package.json missing"
    fi
    
    if [ -d "node_modules" ]; then
        pass_test "Frontend dependencies installed"
    else
        warn_test "Frontend dependencies not installed - run 'npm install' in front/ directory"
    fi
    
    cd ..
}

test_frontend_build() {
    cd front
    
    # Test if Next.js can build
    if npm run build > /dev/null 2>&1; then
        pass_test "Frontend builds successfully"
    else
        fail_test "Frontend build failed"
    fi
    
    cd ..
}

test_frontend_server() {
    cd front
    
    # Start Next.js in background
    npm run dev > /dev/null 2>&1 &
    NEXT_PID=$!
    
    # Wait for server to start
    sleep 10
    
    # Test if server is responding
    if curl -s http://127.0.0.1:3000 > /dev/null; then
        pass_test "Frontend server starts and responds"
    else
        fail_test "Frontend server not responding"
    fi
    
    # Clean up
    kill $NEXT_PID > /dev/null 2>&1 || true
    cd ..
}

# 4. DOCKER TESTS
echo -e "\n${BLUE}4. Testing Docker Configuration...${NC}"

test_docker_available() {
    if command -v docker &> /dev/null; then
        pass_test "Docker is installed and available"
    else
        fail_test "Docker not installed"
        return
    fi
    
    if docker info > /dev/null 2>&1; then
        pass_test "Docker daemon is running"
    else
        fail_test "Docker daemon not running"
    fi
}

test_docker_build() {
    # Test backend Docker build
    if docker build -t hammer-backend-test ./back > /dev/null 2>&1; then
        pass_test "Backend Docker image builds successfully"
        docker rmi hammer-backend-test > /dev/null 2>&1 || true
    else
        fail_test "Backend Docker build failed"
    fi
    
    # Test frontend Docker build
    if docker build -t hammer-frontend-test ./front > /dev/null 2>&1; then
        pass_test "Frontend Docker image builds successfully"
        docker rmi hammer-frontend-test > /dev/null 2>&1 || true
    else
        fail_test "Frontend Docker build failed"
    fi
}

# 5. SECURITY TESTS
echo -e "\n${BLUE}5. Testing Security Configuration...${NC}"

test_security_headers() {
    cd back
    
    # Start Django with production-like settings
    DJANGO_ENV=production python manage.py runserver 127.0.0.1:8002 > /dev/null 2>&1 &
    DJANGO_PID=$!
    
    sleep 5
    
    # Test security headers
    HEADERS=$(curl -I -s http://127.0.0.1:8002/api/health/)
    
    if echo "$HEADERS" | grep -i "x-frame-options"; then
        pass_test "X-Frame-Options header present"
    else
        warn_test "X-Frame-Options header missing"
    fi
    
    if echo "$HEADERS" | grep -i "x-content-type-options"; then
        pass_test "X-Content-Type-Options header present"
    else
        warn_test "X-Content-Type-Options header missing"
    fi
    
    # Clean up
    kill $DJANGO_PID > /dev/null 2>&1 || true
    cd ..
}

test_environment_security() {
    # Check for sensitive data in version control
    if git ls-files | grep -E "\.(env|key|pem|p12)$" | grep -v ".env.example"; then
        fail_test "Sensitive files found in git repository"
    else
        pass_test "No sensitive files in git repository"
    fi
    
    # Check for hardcoded secrets
    if grep -r "sk-" --include="*.py" --include="*.js" --exclude-dir=node_modules . | grep -v ".env"; then
        fail_test "Hardcoded API keys found in source code"
    else
        pass_test "No hardcoded API keys in source code"
    fi
}

# 6. API ENDPOINT TESTS
echo -e "\n${BLUE}6. Testing API Endpoints...${NC}"

test_api_endpoints() {
    cd back
    
    # Start Django server for API testing
    python manage.py runserver 127.0.0.1:8003 > /dev/null 2>&1 &
    DJANGO_PID=$!
    
    sleep 5
    
    # Test health endpoint
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8003/api/health/)
    if [ "$HEALTH_STATUS" = "200" ]; then
        pass_test "Health endpoint responds with 200"
    else
        fail_test "Health endpoint not working (status: $HEALTH_STATUS)"
    fi
    
    # Test API info endpoint
    INFO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8003/api/info/)
    if [ "$INFO_STATUS" = "200" ]; then
        pass_test "API info endpoint responds with 200"
    else
        fail_test "API info endpoint not working (status: $INFO_STATUS)"
    fi
    
    # Test CORS headers
    CORS_HEADERS=$(curl -I -s -H "Origin: http://localhost:3000" http://127.0.0.1:8003/api/health/)
    if echo "$CORS_HEADERS" | grep -i "access-control-allow-origin"; then
        pass_test "CORS headers configured"
    else
        warn_test "CORS headers not found"
    fi
    
    # Clean up
    kill $DJANGO_PID > /dev/null 2>&1 || true
    cd ..
}

# 7. PRODUCTION SIMULATION TESTS
echo -e "\n${BLUE}7. Testing Production Simulation...${NC}"

test_production_environment() {
    # Test with production environment file
    if [ -f ".env.production" ]; then
        cd back
        
        # Temporarily use production settings
        export DJANGO_SETTINGS_MODULE=hammer_backendproject.settings
        export DJANGO_ENV=production
        
        # Test production configuration
        python manage.py check --deploy > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            pass_test "Production Django configuration passes deployment checks"
        else
            fail_test "Production Django configuration has deployment issues"
        fi
        
        unset DJANGO_ENV
        cd ..
    else
        warn_test "Skipping production environment test (.env.production missing)"
    fi
}

test_nginx_config() {
    if [ -f "nginx/nginx.conf" ]; then
        # Test Nginx configuration syntax
        if docker run --rm -v "$(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine nginx -t > /dev/null 2>&1; then
            pass_test "Nginx configuration syntax is valid"
        else
            fail_test "Nginx configuration has syntax errors"
        fi
    else
        fail_test "Nginx configuration file missing"
    fi
}

# 8. INTEGRATION TESTS
echo -e "\n${BLUE}8. Testing System Integration...${NC}"

test_full_stack() {
    info_test "Starting full-stack integration test..."
    
    # This would start both frontend and backend together
    # For now, we'll just verify the configuration
    
    if [ -f "docker-compose.yml" ] || [ -f "docker-compose.prod.yml" ]; then
        pass_test "Docker Compose configuration exists"
    else
        fail_test "Docker Compose configuration missing"
    fi
    
    # Test if all required services are defined
    if [ -f "docker-compose.prod.yml" ]; then
        SERVICES=$(grep -E "^\s+[a-zA-Z]" docker-compose.prod.yml | grep -v "image:" | grep -v "build:" | wc -l)
        if [ "$SERVICES" -ge 3 ]; then
            pass_test "Multiple services defined in Docker Compose"
        else
            warn_test "Limited services in Docker Compose configuration"
        fi
    fi
}

# Run all tests
echo -e "\n${YELLOW}Starting test execution...${NC}"

test_env_files
test_openai_config
test_django_configuration
test_django_server
test_frontend_dependencies
test_frontend_build
test_frontend_server
test_docker_available
test_docker_build
test_security_headers
test_environment_security
test_api_endpoints
test_production_environment
test_nginx_config
test_full_stack

# Final results
echo -e "\n================================================"
echo -e "${BLUE}🧪 PRODUCTION TESTING COMPLETE${NC}"
echo -e "================================================"

echo -e "\n📊 ${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "📊 ${RED}Tests Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! Your app is production-ready!${NC}"
    echo -e "${GREEN}✅ You can safely run ./deploy.sh${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please fix issues before deployment.${NC}"
    echo -e "${YELLOW}💡 Check the failed tests above and resolve them.${NC}"
    exit 1
fi
