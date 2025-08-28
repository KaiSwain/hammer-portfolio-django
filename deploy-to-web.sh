#!/bin/bash

# Deploy Hammer Portal to ifihadahammer.com/portal
echo "🚀 Preparing Hammer Portal for ifihadahammer.com/portal..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this from the front/ directory"
    echo "Usage: cd front && ../deploy-to-web.sh"
    exit 1
fi

echo "📋 Portal Deployment Checklist:"
echo "1. ✅ Have you pushed your latest code to GitHub?"
echo "2. ✅ Do you have a Railway backend URL ready?"
echo "3. ✅ Ready to deploy to ifihadahammer.com/portal?"

read -p "Continue with portal deployment? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Ask for backend URL
echo ""
echo "🔗 Backend Setup:"
echo "If you haven't deployed to Railway yet:"
echo "1. Go to railway.app"
echo "2. Connect your GitHub repo"
echo "3. Deploy the 'back' folder"
echo "4. Add environment variables (see PORTAL_DEPLOYMENT.md)"
echo "5. Copy the generated URL"
echo ""

read -p "Enter your Railway backend URL (or press Enter to use placeholder): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="https://your-railway-backend-url.up.railway.app"
    echo "Using placeholder URL. Remember to update this later!"
fi

# Update environment variable
if [ -f ".env.production" ]; then
    sed -i "s|NEXT_PUBLIC_API_URL=.*|NEXT_PUBLIC_API_URL=$BACKEND_URL|" .env.production
    echo "✅ Updated .env.production with backend URL"
fi

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Deploy to Vercel
echo "🚀 Deploying portal to Vercel..."
echo "🎯 This will be accessible at: ifihadahammer.com/portal"
vercel --prod

echo ""
echo "🎉 Portal deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Note your Vercel URL from the output above"
echo "2. Buy ifihadahammer.com domain"
echo "3. In Vercel dashboard:"
echo "   - Add ifihadahammer.com as custom domain"
echo "   - Follow DNS setup instructions"
echo "4. Update Railway backend allowed hosts to include ifihadahammer.com"
echo ""
echo "🌐 Your portal will be available at:"
echo "   https://ifihadahammer.com/portal"
echo "   https://ifihadahammer.com/portal/admin"
echo ""
echo "💡 You can deploy a separate main website to ifihadahammer.com root later!"
