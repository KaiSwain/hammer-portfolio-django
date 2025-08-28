# Vercel + Railway Deployment Guide
# Deploy your Hammer Portfolio with custom domain

## 🌐 Your Company Domain Options

### Option 1: Buy Your Own Domain (Recommended)
- **Where to buy**: GoDaddy, Namecheap, Google Domains
- **Cost**: $10-15/year
- **Examples**: 
  - `hammertraining.com`
  - `ifhadahammer.com`
  - `hammerportfolio.net`
  - `yourcompanyname.com`

### Option 2: Use Free Subdomains
- **Vercel**: `hammer-portfolio.vercel.app`
- **Railway**: `hammer-backend.up.railway.app`

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `hammer-portfolio-django` repository
5. Choose the `back` folder as root directory
6. Add environment variables:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=*.railway.app,yourdomain.com
   OPENAI_API_KEY=your-openai-key
   ```
7. Railway will give you a URL like: `https://hammer-backend-production.up.railway.app`

### Step 2: Deploy Frontend to Vercel
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy frontend:
   ```bash
   cd front
   vercel
   ```

3. During setup, provide:
   - Project name: `hammer-portfolio`
   - Environment variable: `NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app`

### Step 3: Set Up Custom Domain
1. **Buy your domain** (e.g., hammertraining.com)
2. **In Vercel Dashboard**:
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain
   - Follow DNS setup instructions
3. **In Railway Dashboard**:
   - Go to your backend project
   - Add your domain to allowed hosts

## 🎯 Final URLs
- **Your Website**: `https://yourdomain.com`
- **Admin Panel**: `https://yourdomain.com/admin/`
- **API**: `https://yourdomain.com/api/`

## 💡 Domain Name Suggestions for Hammer
- `hammertraining.com`
- `ifhadahammer.com` 
- `hammerportfolio.net`
- `hammertech.io`
- `buildwithammer.com`
- `hammerworkforce.com`

## 📞 Next Steps
1. Choose and buy your domain
2. Follow deployment steps above
3. Your coworkers can access at your custom domain!

Total cost: ~$15/year for domain (hosting is free with Railway/Vercel free tiers)
