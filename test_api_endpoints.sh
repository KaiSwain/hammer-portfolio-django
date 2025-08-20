#!/bin/bash

echo "🧪 Testing API Endpoints..."

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s http://localhost:8000/api/health/ | head -200 || echo "❌ Health endpoint failed"

echo -e "\n"

# Test students endpoint
echo "2. Testing students endpoint..."
curl -s http://localhost:8000/api/students/ | head -200 || echo "❌ Students endpoint failed"

echo -e "\n"

# Test legacy students endpoint
echo "3. Testing legacy students endpoint..."
curl -s http://localhost:8000/students/ | head -200 || echo "❌ Legacy students endpoint failed"

echo -e "\n"

# Test API info
echo "4. Testing API info endpoint..."
curl -s http://localhost:8000/api/info/ | head -200 || echo "❌ API info endpoint failed"

echo -e "\n"

# Test CORS
echo "5. Testing CORS headers..."
curl -I -H "Origin: http://localhost:3000" http://localhost:8000/api/students/ | grep -i "access-control" || echo "❌ CORS headers missing"

echo -e "\n✅ API endpoint testing complete!"
