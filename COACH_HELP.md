# COACH HELP - DigitalOcean Deployment Issues

## 🛠️ LATEST CHANGES IMPLEMENTED (Aug 29, 2025)

### ✅ **STEP 1: Added Explicit Routes**
```yaml
# Frontend service routes
routes:
  - path: /
  - path: /_next(/.*)?
  - path: /static(/.*)?

# Backend service routes  
routes:
  - path: /api(/.*)?
  - path: /admin(/.*)?
  - path: /media(/.*)?
```

### ✅ **STEP 2: Fixed Frontend PORT Binding**
```json
// front/package.json - Changed to:
"start": "next start -p $PORT"
```

### ✅ **STEP 3: Fixed Django Environment Variable Names**
```yaml
# Changed from:
DJANGO_ALLOWED_HOSTS → ALLOWED_HOSTS  
DJANGO_CSRF_TRUSTED_ORIGINS → CSRF_TRUSTED_ORIGINS
```

### ✅ **STEP 4: Simplified Health Check**
```yaml
# Changed from /admin/ to:
health_check:
  http_path: /health/
```

## ❌ **CURRENT ISSUES (Still Happening After Changes)**

### 1. **Environment Variables NOT Loading**
Backend logs show:
```
Allowed hosts: (empty)
CSRF trusted origins: (empty)
```

### 2. **Main Domain Still Shows Django API**
- Expected: Next.js frontend at https://hammermath-portal-vaa4g.ondigitalocean.app/
- Actual: Django API still appears at root domain
- Explicit routes didn't work

### 3. **Database Permissions Still Failing**
```
❌ Migration failed: permission denied for schema public
```

## PROBLEM SUMMARY
Student is trying to deploy a Next.js frontend + Django backend on DigitalOcean App Platform. The frontend is NOT showing up at the main URL - instead, the Django API is appearing at https://hammermath-portal-vaa4g.ondigitalocean.app/

## WHAT WE'RE TRYING TO ACHIEVE
- Frontend (Next.js/React): https://hammermath-portal-vaa4g.ondigitalocean.app/
- Backend (Django API): https://hammer-backend-vaa4g.ondigitalocean.app/api/
- Admin Panel: https://hammer-backend-vaa4g.ondigitalocean.app/admin/

## CURRENT STATUS
✅ Backend Django API is working  
❌ Frontend Next.js is NOT showing at main domain  
❌ Still seeing Django API response instead of React UI  

## DEPLOYMENT ATTEMPTS TRIED

### ATTEMPT 1: Single Service Approach (FAILED)
**Concept**: Build both frontend and backend in one service
```yaml
services:
  - name: hammer-app
    source_dir: /
    build_command: |
      curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
      apt-get install -y nodejs
      cd front
      npm install
      npm run build
      cd ../back
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
    run_command: cd back && ./start.sh
```
**FAILED BECAUSE**: Next.js dynamic routes like `/students/[id]/edit` don't work with `output: 'export'` configuration needed for static serving.

### ATTEMPT 2: Frontend as Static Site (FAILED)
**Concept**: Deploy frontend as static site, backend as service
```yaml
static_sites:
  - name: hammer-frontend
    source_dir: /front
    output_dir: /out
    build_command: npm run build

services:
  - name: hammer-backend
    source_dir: /back
```
**FAILED BECAUSE**: Static sites can't handle dynamic routes or client-side routing properly.

### ATTEMPT 3: Frontend Service + Backend Worker (FAILED)
**Concept**: Frontend as web service, backend as background worker
```yaml
services:
  - name: hammer-app
    source_dir: /front
    http_port: 3000

workers:
  - name: hammer-backend
    source_dir: /back
```
**FAILED BECAUSE**: Workers don't get public URLs, so frontend couldn't connect to backend API.

### ATTEMPT 4: Both as Services (CURRENT - STILL FAILING)
**Concept**: Both frontend and backend as separate web services
```yaml
services:
  - name: hammer-app
    source_dir: /front
    http_port: 3000
    build_command: npm run build
    run_command: npm start
    
  - name: hammer-backend
    source_dir: /back
    http_port: 8000
    run_command: ./start.sh
```
**STILL FAILING**: Main domain shows Django API instead of Next.js frontend.

## CURRENT CONFIGURATION ANALYSIS

### What Looks Correct:
- Frontend service has `http_port: 3000` ✅
- Backend service has `http_port: 8000` ✅  
- Both are listed under `services:` (not workers) ✅
- Frontend is listed FIRST (should get main domain) ✅
- Environment variables are properly set ✅
- GitHub repo and branch are correct ✅

### What Might Be Wrong:
- DigitalOcean might not respect service order for domain assignment ❓
- Frontend build might be failing silently ❓
- Health check on `/` might be failing ❓
- Backend health check on `/admin/` is failing (database migration issues) ❓

## SPECIFIC ISSUES IDENTIFIED

### Issue 1: Database Migration Failures
Backend logs show:
```
❌ Migration failed: Unable to create the django_migrations table (permission denied for schema public)
```
This means the Django admin health check at `/admin/` is failing because auth_user table doesn't exist.

### Issue 2: Domain Routing Confusion
Current expectation:
- First service (hammer-app) gets: https://hammermath-portal-vaa4g.ondigitalocean.app/
- Second service (hammer-backend) gets: https://hammer-backend-vaa4g.ondigitalocean.app/

Reality: Main domain still shows backend API.

### Issue 3: Environment Variables Not Loading
Backend logs show:
```
Allowed hosts: 
CSRF trusted origins: 
```
Environment variables appear to be empty in runtime.

## CRITICAL QUESTIONS FOR COACH

### Question 1: Domain Assignment Logic
In DigitalOcean App Platform, how are domains assigned to services?
- Does the FIRST service automatically get the main app domain?
- Do we need explicit domain routing configuration?
- Is there a way to force domain assignment?

### Question 2: Service vs Static Site Decision
For a Next.js app with dynamic routes like `/students/[id]/edit`:
- Should it be deployed as a `service` with `node-js` environment?
- Can static sites handle client-side routing?
- What's the recommended approach for Next.js on DigitalOcean?

### Question 3: Health Check Strategy
Current health checks:
- Frontend: `http_path: /` (Next.js home page)
- Backend: `http_path: /admin/` (Django admin - requires database)

Should we:
- Change backend health check to `/api/` or `/health/`?
- Create a simple health endpoint that doesn't require database?
- Use different health check configuration?

### Question 4: Build Process Verification
How can we verify if the Next.js build is actually succeeding?
- Are there specific logs to check in DigitalOcean?
- Should we use `next build` instead of `npm run build`?
- Is the `npm start` command correct for production?

## DEBUGGING STEPS TO TRY

### Step 1: Verify Service Status
Check these URLs manually:
- https://hammermath-portal-vaa4g.ondigitalocean.app/ (currently shows Django API)
- https://hammer-backend-vaa4g.ondigitalocean.app/ (should show Django API)
- https://hammer-app-vaa4g.ondigitalocean.app/ (might exist as separate service)

### Step 2: Isolate Frontend Service
Temporarily remove backend service to test:
```yaml
services:
  - name: hammer-app
    source_dir: /front
    # Remove backend service entirely
```
Does frontend appear at main domain when it's the only service?

### Step 3: Check DigitalOcean Logs
Look for in deployment logs:
- ✅ "npm run build" completion messages
- ✅ "npm start" startup messages  
- ❌ Build failures or port binding issues
- ❌ Health check failures

### Step 4: Test Simple Frontend
Create minimal test page to verify deployment:
```javascript
// pages/test.js
export default function Test() {
  return <h1>FRONTEND IS WORKING!</h1>
}
```

## ALTERNATIVE APPROACHES TO CONSIDER

### Option A: Explicit Domain Configuration
```yaml
domains:
  - domain: hammermath-portal-vaa4g.ondigitalocean.app
    type: PRIMARY
    zone: hammermath-portal-vaa4g.ondigitalocean.app
    certificate:
      type: LETS_ENCRYPT
```

### Option B: Reverse Proxy Pattern
Have Django serve the Next.js build files:
```yaml
services:
  - name: hammer-app
    source_dir: /back
    build_command: |
      cd ../front && npm install && npm run build
      cd ../back && pip install -r requirements.txt
      # Copy Next.js build to Django static files
```

### Option C: Single Service with Internal Routing
```yaml
services:
  - name: hammer-app
    source_dir: /
    # Custom startup script that runs both frontend and backend
```

### Option D: Different Port Strategy
```yaml
services:
  - name: hammer-app
    http_port: 80  # Try standard HTTP port
    
  - name: hammer-backend  
    http_port: 8080  # Different port
```

## IMMEDIATE ACTION ITEMS

1. **Coach Review**: Examine DigitalOcean App Platform domain routing documentation
2. **Log Analysis**: Check detailed deployment logs for frontend build success/failure
3. **Health Check Fix**: Change backend health check from `/admin/` to `/api/`
4. **Test Isolation**: Deploy frontend-only to verify domain assignment
5. **Environment Debug**: Investigate why environment variables are empty in runtime

## CONTACT INFORMATION
Student: [Student Name]
Repository: https://github.com/KaiSwain/hammer-portfolio-django
Branch: phase1
DigitalOcean App: hammer-portfolio

## CURRENT WORKING BACKEND
The Django backend IS working properly at:
- API: https://hammermath-portal-vaa4g.ondigitalocean.app/api/
- Admin: https://hammermath-portal-vaa4g.ondigitalocean.app/admin/ (has database issues)

The main problem is getting the Next.js frontend to appear at the root domain instead of the Django API.
