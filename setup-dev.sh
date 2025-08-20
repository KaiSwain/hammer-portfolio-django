#!/bin/bash
# Setup script for Hammer Portfolio Django development environment

echo "🔨 Setting up Hammer Portfolio Django Development Environment"
echo "============================================================"

# Backend setup
echo "📁 Setting up backend environment..."
if [ ! -f "back/.env.development" ]; then
    cp back/.env.development.template back/.env.development
    echo "✅ Created back/.env.development from template"
    echo "⚠️  Please edit back/.env.development and add your OpenAI API key"
else
    echo "ℹ️  back/.env.development already exists"
fi

# Frontend setup (if needed later)
echo "📁 Checking frontend environment..."
if [ ! -f "front/.env.development" ]; then
    echo "ℹ️  No frontend environment file needed yet"
else
    echo "ℹ️  front/.env.development already exists"
fi

echo ""
echo "🚀 Next steps:"
echo "1. Edit back/.env.development and add your OpenAI API key"
echo "2. Navigate to back/ directory: cd back"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run Django server: python manage.py runserver"
echo "5. In another terminal, navigate to front/ and run: npm run dev"
echo ""
echo "🌐 Your app will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
