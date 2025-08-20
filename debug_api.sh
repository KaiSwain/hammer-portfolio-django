#!/bin/bash

echo "🔍 COMPREHENSIVE API DEBUGGING"
echo "============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}Testing Django Server Connectivity...${NC}"

# Check if Django server is running
if curl -s --connect-timeout 3 http://localhost:8000/admin/ > /dev/null; then
    echo -e "${GREEN}✅ Django server is running on port 8000${NC}"
else
    echo -e "${RED}❌ Django server not responding on port 8000${NC}"
    echo -e "${YELLOW}💡 Start Django with: cd back && python manage.py runserver${NC}"
    exit 1
fi

echo -e "\n${BLUE}Testing API Endpoints...${NC}"

# Test 1: Health Check
echo -e "\n1. Testing Health Endpoint:"
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health/)
if [ "$HEALTH_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Health endpoint working (HTTP $HEALTH_STATUS)${NC}"
    curl -s http://localhost:8000/api/health/ | head -3
else
    echo -e "${RED}❌ Health endpoint failed (HTTP $HEALTH_STATUS)${NC}"
fi

# Test 2: Students Endpoint
echo -e "\n2. Testing Students Endpoint:"
STUDENTS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/students/)
if [ "$STUDENTS_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Students endpoint working (HTTP $STUDENTS_STATUS)${NC}"
    STUDENTS_DATA=$(curl -s http://localhost:8000/api/students/)
    echo "Students response: $STUDENTS_DATA" | head -3
else
    echo -e "${RED}❌ Students endpoint failed (HTTP $STUDENTS_STATUS)${NC}"
    echo "Error response:"
    curl -s http://localhost:8000/api/students/ | head -5
fi

# Test 3: Legacy Students Endpoint
echo -e "\n3. Testing Legacy Students Endpoint:"
LEGACY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/students/)
if [ "$LEGACY_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Legacy students endpoint working (HTTP $LEGACY_STATUS)${NC}"
else
    echo -e "${YELLOW}⚠️  Legacy students endpoint not working (HTTP $LEGACY_STATUS)${NC}"
fi

# Test 4: CORS Headers
echo -e "\n4. Testing CORS Headers:"
CORS_RESPONSE=$(curl -I -s -H "Origin: http://localhost:3000" http://localhost:8000/api/students/)
if echo "$CORS_RESPONSE" | grep -q "access-control-allow-origin"; then
    echo -e "${GREEN}✅ CORS headers present${NC}"
    echo "$CORS_RESPONSE" | grep -i "access-control"
else
    echo -e "${RED}❌ CORS headers missing${NC}"
    echo "Response headers:"
    echo "$CORS_RESPONSE" | head -10
fi

# Test 5: API Info
echo -e "\n5. Testing API Info Endpoint:"
INFO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/info/)
if [ "$INFO_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ API info endpoint working${NC}"
    curl -s http://localhost:8000/api/info/ | head -5
else
    echo -e "${RED}❌ API info endpoint failed (HTTP $INFO_STATUS)${NC}"
fi

# Test 6: Admin Panel
echo -e "\n6. Testing Admin Panel:"
ADMIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/)
if [ "$ADMIN_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Admin panel accessible${NC}"
else
    echo -e "${RED}❌ Admin panel not accessible (HTTP $ADMIN_STATUS)${NC}"
fi

echo -e "\n${BLUE}Frontend Configuration Check...${NC}"

# Check if Next.js server is running
if curl -s --connect-timeout 3 http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ Frontend server running on port 3000${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend server not running on port 3000${NC}"
fi

echo -e "\n${BLUE}Database Check...${NC}"

# Test database through Django shell
cd /home/kaifer/workspace/hammer/hammer-portfolio-django/back
DB_TEST=$(python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()
from hammer_backendapi.models import Student
try:
    count = Student.objects.count()
    print(f'SUCCESS:{count}')
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null)

if echo "$DB_TEST" | grep -q "SUCCESS"; then
    STUDENT_COUNT=$(echo "$DB_TEST" | cut -d':' -f2)
    echo -e "${GREEN}✅ Database connected - $STUDENT_COUNT students found${NC}"
else
    echo -e "${RED}❌ Database connection failed${NC}"
    echo "Error: $DB_TEST"
fi

echo -e "\n${BLUE}Summary & Next Steps...${NC}"

echo -e "\n🎯 ${GREEN}URLs to test in your browser:${NC}"
echo "• Health Check: http://localhost:8000/api/health/"
echo "• Students API: http://localhost:8000/api/students/"
echo "• Admin Panel: http://localhost:8000/admin/"
echo "• Frontend: http://localhost:3000"

echo -e "\n🔧 ${YELLOW}If students aren't loading:${NC}"
echo "1. Check browser console for CORS errors"
echo "2. Verify API calls in Network tab"
echo "3. Ensure both servers are running"
echo "4. Check that student data exists in database"

echo -e "\n📋 ${BLUE}Quick Commands:${NC}"
echo "• Start Django: cd back && python manage.py runserver"
echo "• Start Frontend: cd front && npm run dev"
echo "• Create test student: cd back && python manage.py shell"

echo -e "\n✅ Debugging complete!"
