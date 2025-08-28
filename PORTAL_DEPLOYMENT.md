# Deploying to ifihadahammer.com/portal

## 🎯 Your Setup: Domain with Portal Path

Your application will be accessible at:
- **Portal**: `https://ifihadahammer.com/portal`
- **Admin**: `https://ifihadahammer.com/portal/admin`
- **API**: `https://your-backend.up.railway.app/api`

This allows you to have:
- Your main company website at `https://ifihadahammer.com`
- The student/teacher portal at `https://ifihadahammer.com/portal`

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository and choose the `back` folder
4. Add these environment variables in Railway:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=*.railway.app,ifihadahammer.com,*.ifihadahammer.com
   OPENAI_API_KEY=your-openai-key
   CORS_ALLOWED_ORIGINS=https://ifihadahammer.com
   ```
5. Note your Railway URL (e.g., `https://hammer-backend-xyz.up.railway.app`)

### Step 2: Deploy Frontend to Vercel
```bash
# First, update your backend URL
cd front
# Edit .env.production and replace with your Railway URL

# Deploy to Vercel
npm install -g vercel
vercel --prod
```

During Vercel setup:
- Project name: `hammer-portal`
- Framework: `Next.js`
- Build command: `npm run build`
- Output directory: `.next`

### Step 3: Configure Custom Domain in Vercel
1. Buy `ifihadahammer.com` domain
2. In Vercel dashboard:
   - Go to your project
   - Click "Domains"
   - Add `ifihadahammer.com`
   - Configure DNS as instructed
3. Set up path-based routing:
   - The portal will automatically be available at `/portal`
   - Your main site can be deployed separately to the root

### Step 4: Optional - Main Website Setup
You can deploy a separate main website to the root domain:
- Create a simple landing page
- Deploy it to Vercel as a separate project
- Configure it for the root domain

## 🌐 Final URLs
- **Main Site**: `https://ifihadahammer.com` (your company homepage)
- **Student Portal**: `https://ifihadahammer.com/portal`
- **Login**: `https://ifihadahammer.com/portal/login`
- **Admin Panel**: `https://ifihadahammer.com/portal/admin`

## 💡 Benefits of This Setup
- Professional company domain
- Separated concerns (main site vs portal)
- Easy to remember URL for users
- SEO-friendly structure
- Can add more applications later (e.g., `/blog`, `/courses`)

## 🔧 Testing
After deployment, test these URLs:
- `https://ifihadahammer.com/portal` → Should load the login page
- `https://ifihadahammer.com/portal/students` → Should redirect to login if not authenticated
- `https://ifihadahammer.com/portal/admin` → Should load Django admin

Total cost: ~$15/year for the domain (Vercel and Railway have generous free tiers)
