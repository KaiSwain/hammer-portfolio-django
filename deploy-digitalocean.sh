#!/bin/bash

# DigitalOcean App Platform Deployment Helper
# This script helps prepare and deploy to DigitalOcean

echo "🚀 DigitalOcean App Platform Deployment Helper"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f ".do/app.yaml" ]; then
    echo "❌ Error: .do/app.yaml not found. Please run from project root."
    exit 1
fi

echo "✅ Found .do/app.yaml configuration"

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Prepare for DigitalOcean deployment"
fi

# Push to GitHub
echo "📤 Pushing latest changes to GitHub..."
git push origin phase1

echo ""
echo "🔧 Deployment Checklist:"
echo "========================"
echo "✅ Configuration file: .do/app.yaml"
echo "✅ Frontend source: /front"
echo "✅ Backend source: /back"
echo "✅ Database: PostgreSQL 15"
echo "✅ Domain ready: portal.hammermath.com"
echo ""

echo "📋 Manual Steps Required:"
echo "========================="
echo "1. Go to: https://cloud.digitalocean.com/apps"
echo "2. Click 'Create App'"
echo "3. Choose GitHub source"
echo "4. Select repository: KaiSwain/hammer-portfolio-django"
echo "5. Choose branch: phase1"
echo "6. Import config: Use existing .do/app.yaml"
echo "7. Set environment variables:"
echo "   - OPENAI_API_KEY (your OpenAI API key)"
echo "   - DJANGO_SECRET_KEY (will be auto-generated)"
echo "8. Click 'Create Resources'"
echo ""

echo "💰 Expected Monthly Cost: ~$17"
echo "   - Frontend: $5"
echo "   - Backend: $5"  
echo "   - Database: $7"
echo ""

echo "🎯 After Deployment:"
echo "==================="
echo "1. Test frontend: https://your-app.ondigitalocean.app"
echo "2. Test backend: https://your-backend.ondigitalocean.app/admin/"
echo "3. Create superuser: python manage.py createsuperuser"
echo "4. Test PDF generation (should work!)"
echo "5. Set up custom domain: portal.hammermath.com"
echo ""

echo "📚 For detailed instructions, see: DIGITALOCEAN_DEPLOYMENT.md"
echo ""
echo "🚀 Ready to deploy! Good luck!"
