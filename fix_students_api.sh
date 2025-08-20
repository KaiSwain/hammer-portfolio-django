#!/bin/bash

echo "🔧 FIXING STUDENT API ISSUES"
echo "============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Step 1: Installing missing dependencies...${NC}"
cd back
pip install dj-database-url > /dev/null 2>&1
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo -e "\n${BLUE}Step 2: Running Django migrations...${NC}"
python manage.py makemigrations > /dev/null 2>&1
python manage.py migrate > /dev/null 2>&1
echo -e "${GREEN}✅ Migrations completed${NC}"

echo -e "\n${BLUE}Step 3: Creating test data...${NC}"
python create_test_data.py
echo -e "${GREEN}✅ Test data created${NC}"

echo -e "\n${BLUE}Step 4: Collecting static files...${NC}"
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✅ Static files collected${NC}"

echo -e "\n${BLUE}Step 5: Testing API endpoints...${NC}"
cd ..
./debug_api.sh

echo -e "\n🎉 ${GREEN}All fixes applied!${NC}"
echo -e "\n🚀 ${YELLOW}Next steps:${NC}"
echo "1. Start Django: cd back && python manage.py runserver"
echo "2. Start Frontend: cd front && npm run dev"
echo "3. Test students API: http://localhost:8000/api/students/"
echo "4. Check admin panel: http://localhost:8000/admin/ (admin/admin123)"
