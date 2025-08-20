#!/bin/bash

# 🧪 SIMPLE PRODUCTION TESTING SCRIPT
# Quick tests to verify everything works before deployment

echo "🚀 Testing Your Production-Ready Django App"
echo "============================================"

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

# Helper functions
test_pass() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
    ((PASSED++))
}

test_fail() {
    echo -e "${RED}❌ FAIL:${NC} $1"
    ((FAILED++))
}

test_warn() {
    echo -e "${YELLOW}⚠️  WARN:${NC} $1"
}

echo -e "\n1. Testing Environment Configuration..."

# Check if we're in the right directory
if [ -f "back/manage.py" ]; then
    test_pass "Project structure is correct"
else
    test_fail "Cannot find back/manage.py - run this from the project root"
    exit 1
fi

# Check environment files
if [ -f "back/.env" ] || [ -f "back/.env.development" ]; then
    test_pass "Environment configuration files exist"
else
    test_fail "No environment files found in back/ directory"
fi

echo -e "\n2. Testing Django Configuration..."

cd back

# Test Django configuration
if python manage.py check > /dev/null 2>&1; then
    test_pass "Django configuration is valid"
else
    test_fail "Django configuration has errors"
fi

# Test OpenAI configuration
OPENAI_TEST=$(python -c "
from django.conf import settings
try:
    import os
    # Load Django settings
    import django
    django.setup()
    from hammer_backendproject import settings
    key = getattr(settings, 'OPENAI_API_KEY', '')
    if key and len(key) > 20 and key.startswith('sk-'):
        print('OK')
    else:
        print('MISSING')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null)

if [ "$OPENAI_TEST" = "OK" ]; then
    test_pass "OpenAI API key is configured"
else
    test_warn "OpenAI API key not configured or invalid"
fi

echo -e "\n3. Testing Database Connection..."

# Test database connection
if python manage.py check --database default > /dev/null 2>&1; then
    test_pass "Database configuration is valid"
else
    test_warn "Database configuration needs attention"
fi

echo -e "\n4. Testing Static Files..."

# Test static files collection
if python manage.py collectstatic --noinput --dry-run > /dev/null 2>&1; then
    test_pass "Static files configuration is valid"
else
    test_fail "Static files configuration has issues"
fi

echo -e "\n5. Testing Django Server Startup..."

# Start Django server in background for testing
python manage.py runserver 127.0.0.1:8001 > /tmp/django_test.log 2>&1 &
DJANGO_PID=$!

# Wait for server to start
sleep 3

# Test if server is responding
if curl -s http://127.0.0.1:8001/api/health/ > /dev/null 2>&1; then
    test_pass "Django server starts and health endpoint responds"
    
    # Test health endpoint content
    HEALTH_RESPONSE=$(curl -s http://127.0.0.1:8001/api/health/)
    if echo "$HEALTH_RESPONSE" | grep -q "status"; then
        test_pass "Health endpoint returns valid JSON"
    else
        test_warn "Health endpoint response format needs checking"
    fi
else
    test_fail "Django server not responding on health endpoint"
fi

# Test API info endpoint
if curl -s http://127.0.0.1:8001/api/info/ > /dev/null 2>&1; then
    test_pass "API info endpoint is working"
else
    test_warn "API info endpoint not responding"
fi

# Stop the test server
kill $DJANGO_PID > /dev/null 2>&1 || true
sleep 1

echo -e "\n6. Testing Docker Configuration..."

cd ..  # Back to project root

# Check if Docker is available
if command -v docker &> /dev/null; then
    test_pass "Docker is installed"
    
    # Test Docker daemon
    if docker info > /dev/null 2>&1; then
        test_pass "Docker daemon is running"
        
        # Test backend Docker build
        echo "   Building backend Docker image (this may take a moment)..."
        if docker build -t hammer-test-backend ./back > /dev/null 2>&1; then
            test_pass "Backend Docker image builds successfully"
            docker rmi hammer-test-backend > /dev/null 2>&1 || true
        else
            test_fail "Backend Docker build failed"
        fi
        
    else
        test_warn "Docker daemon not running"
    fi
else
    test_warn "Docker not installed (optional for local testing)"
fi

echo -e "\n7. Testing Production Files..."

# Check important production files
if [ -f "deploy.sh" ]; then
    test_pass "Deployment script exists"
else
    test_fail "Deployment script missing"
fi

if [ -f "docker-compose.prod.yml" ]; then
    test_pass "Production Docker Compose file exists"
else
    test_fail "Production Docker Compose file missing"
fi

if [ -f "nginx/nginx.conf" ]; then
    test_pass "Nginx configuration exists"
else
    test_fail "Nginx configuration missing"
fi

echo -e "\n8. Testing Frontend Configuration..."

if [ -f "front/package.json" ]; then
    test_pass "Frontend package.json exists"
    
    cd front
    if [ -d "node_modules" ]; then
        test_pass "Frontend dependencies are installed"
    else
        test_warn "Frontend dependencies not installed - run 'npm install' in front/ directory"
    fi
    
    # Test if Next.js can build
    echo "   Testing frontend build (this may take a moment)..."
    if npm run build > /dev/null 2>&1; then
        test_pass "Frontend builds successfully"
    else
        test_warn "Frontend build has issues - check package.json and dependencies"
    fi
    
    cd ..
else
    test_fail "Frontend package.json missing"
fi

# Final Results
echo -e "\n============================================"
echo -e "🧪 TESTING COMPLETE"
echo -e "============================================"

echo -e "\n📊 Results:"
echo -e "   ${GREEN}Passed: $PASSED${NC}"
echo -e "   ${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL CRITICAL TESTS PASSED!${NC}"
    echo -e "${GREEN}✅ Your app is ready for production testing!${NC}"
    echo -e "\nNext steps:"
    echo -e "1. Run manual tests from TESTING_GUIDE.md"
    echo -e "2. Test with Docker Compose: ${YELLOW}docker-compose -f docker-compose.prod.yml up${NC}"
    echo -e "3. Deploy to production: ${YELLOW}./deploy.sh${NC}"
else
    echo -e "\n${RED}❌ Some critical issues found.${NC}"
    echo -e "${YELLOW}💡 Please fix the failed tests before deploying to production.${NC}"
    echo -e "\nFor detailed troubleshooting, check:"
    echo -e "- TESTING_GUIDE.md"
    echo -e "- JUNIOR_DEVELOPER_GUIDE.txt"
    echo -e "- Django logs in back/logs/"
fi

echo -e "\n🔍 For comprehensive testing, also run:"
echo -e "   ${YELLOW}Manual tests from TESTING_GUIDE.md${NC}"
echo -e "   ${YELLOW}docker-compose up --build${NC} (for full integration test)"

exit $FAILED
