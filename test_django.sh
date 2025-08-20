#!/bin/bash

# Quick Django test script
echo "🔧 Quick Django Test"

cd /home/kaifer/workspace/hammer/hammer-portfolio-django/back

echo "1. Testing Django configuration..."
python manage.py check
echo ""

echo "2. Starting Django server..."
python manage.py runserver 127.0.0.1:8001 &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 5

echo "3. Testing health endpoint..."
curl -s http://127.0.0.1:8001/api/health/ | head -100

echo ""
echo "4. Testing API info endpoint..."
curl -s http://127.0.0.1:8001/api/info/ | head -100

echo ""
echo "5. Stopping server..."
kill $SERVER_PID 2>/dev/null || true

echo "Done!"
