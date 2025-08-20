# 🧪 MANUAL TESTING GUIDE
# Step-by-step testing instructions before production deployment

## 🚀 QUICK START: Run Automated Tests First

```bash
# Run the comprehensive test suite
./test_production.sh
```

If all automated tests pass, proceed with manual testing below.

---

## 1. 🔧 DEVELOPMENT ENVIRONMENT TESTING

### Backend Testing (Django)
```bash
cd back
python manage.py runserver
```

**Test Checklist:**
- [ ] Server starts without errors
- [ ] Navigate to: http://localhost:8000/api/health/
- [ ] Should see: `{"status": "healthy", "timestamp": "...", ...}`
- [ ] Navigate to: http://localhost:8000/api/info/
- [ ] Should see API documentation
- [ ] Navigate to: http://localhost:8000/admin/
- [ ] Admin interface loads properly

### Frontend Testing (Next.js)
```bash
cd front
npm run dev
```

**Test Checklist:**
- [ ] Server starts without errors
- [ ] Navigate to: http://localhost:3000
- [ ] Homepage loads properly
- [ ] No console errors in browser
- [ ] Can navigate between pages
- [ ] API calls work (check Network tab)

---

## 2. 🔌 API INTEGRATION TESTING

### Test API Endpoints
With both servers running (backend:8000, frontend:3000):

**Health Check:**
```bash
curl http://localhost:8000/api/health/
```
Expected: `{"status": "healthy", ...}`

**API Info:**
```bash
curl http://localhost:8000/api/info/
```
Expected: List of available endpoints

**Students Endpoint:**
```bash
curl http://localhost:8000/api/students/
```
Expected: List of students or empty array

**CORS Testing:**
```bash
curl -H "Origin: http://localhost:3000" -I http://localhost:8000/api/health/
```
Expected: Should include `Access-Control-Allow-Origin` header

---

## 3. 🐳 DOCKER TESTING

### Test Individual Docker Builds

**Backend Docker:**
```bash
docker build -t hammer-backend-test ./back
docker run -p 8001:8000 hammer-backend-test
```
- [ ] Image builds successfully
- [ ] Container starts without errors
- [ ] Health check works: http://localhost:8001/api/health/

**Frontend Docker:**
```bash
docker build -t hammer-frontend-test ./front
docker run -p 3001:3000 hammer-frontend-test
```
- [ ] Image builds successfully
- [ ] Container starts without errors
- [ ] Frontend loads: http://localhost:3001

**Cleanup:**
```bash
docker stop $(docker ps -q)
docker rmi hammer-backend-test hammer-frontend-test
```

---

## 4. 🏗️ DOCKER COMPOSE TESTING

### Development Environment
```bash
cd back
docker-compose up --build
```

**Test Checklist:**
- [ ] All services start (postgres, backend)
- [ ] No errors in logs
- [ ] Backend accessible at http://localhost:8000
- [ ] Database connection works
- [ ] Health check passes

### Production Environment
```bash
docker-compose -f docker-compose.prod.yml up --build
```

**Test Checklist:**
- [ ] All services start (nginx, backend, frontend, postgres)
- [ ] No errors in logs
- [ ] Nginx serves requests at http://localhost
- [ ] Static files load properly
- [ ] API endpoints work through Nginx
- [ ] Frontend loads through Nginx

---

## 5. 🛡️ SECURITY TESTING

### Test Security Headers
```bash
curl -I http://localhost/api/health/
```

**Required Headers:**
- [ ] `X-Frame-Options: DENY`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-XSS-Protection: 1; mode=block`

### Test Rate Limiting (if Nginx running)
```bash
# Rapid requests to test rate limiting
for i in {1..15}; do curl http://localhost/api/health/; done
```
- [ ] Should see 429 (Too Many Requests) after ~10 requests

### Test HTTPS Redirect (Production)
```bash
curl -I http://localhost
```
- [ ] Should redirect to HTTPS in production

---

## 6. 🔍 DATABASE TESTING

### Test Database Operations
```bash
cd back
python manage.py shell
```

```python
# Test database connection
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
print("Database connection: OK")

# Test model operations
from hammer_backendapi.models import Student
students = Student.objects.all()
print(f"Students in database: {students.count()}")
```

### Test Migrations
```bash
python manage.py makemigrations --dry-run
python manage.py migrate --plan
```
- [ ] No pending migrations
- [ ] Migration plan is clean

---

## 7. 🎯 LOAD TESTING (Optional)

### Simple Load Test
```bash
# Install if needed: pip install locust
# Create simple load test
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class HealthCheckUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/api/health/")
    
    @task
    def api_info(self):
        self.client.get("/api/info/")
EOF

# Run load test
locust --host=http://localhost:8000 --users=10 --spawn-rate=2 --run-time=30s --headless
```

---

## 8. 🌐 FRONTEND FUNCTIONALITY TESTING

### Manual Browser Testing
1. **Open Frontend:** http://localhost:3000
2. **Test Navigation:**
   - [ ] All menu items work
   - [ ] Page transitions smooth
   - [ ] No JavaScript errors in console

3. **Test API Integration:**
   - [ ] Data loads from backend
   - [ ] Error handling works
   - [ ] Loading states display

4. **Test Responsive Design:**
   - [ ] Mobile view works
   - [ ] Tablet view works
   - [ ] Desktop view works

5. **Test Forms (if any):**
   - [ ] Form validation works
   - [ ] Submission successful
   - [ ] Error messages display

---

## 9. 🚨 ERROR HANDLING TESTING

### Test Backend Error Handling
```bash
# Test invalid endpoint
curl http://localhost:8000/api/nonexistent/

# Test with invalid data
curl -X POST http://localhost:8000/api/students/ -H "Content-Type: application/json" -d '{"invalid": "data"}'
```

### Test Frontend Error Handling
1. **Stop backend server**
2. **Try to use frontend features**
3. **Check error messages display properly**

---

## 10. 📋 PRE-DEPLOYMENT CHECKLIST

### Environment Files
- [ ] `.env.production` exists with real values
- [ ] No sensitive data in git repository
- [ ] OpenAI API key is valid and working
- [ ] Database URL is correct for production

### Security
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS configured properly
- [ ] CORS settings configured for production domain

### Performance
- [ ] Static files collected
- [ ] Database migrations applied
- [ ] No development dependencies in production
- [ ] Logging configured properly

### Monitoring
- [ ] Health checks working
- [ ] Error logging functional
- [ ] Performance monitoring ready

---

## 🎉 FINAL VALIDATION

Before running `./deploy.sh`:

1. **All automated tests pass:** `./test_production.sh`
2. **Manual testing completed:** All checkboxes above ✅
3. **Environment configured:** Production `.env.production` ready
4. **Backups ready:** Database backup strategy in place
5. **Monitoring ready:** Health checks and logging configured

**If everything above is ✅, you're ready for production!**

```bash
./deploy.sh
```

---

## 🆘 TROUBLESHOOTING

### Common Issues:

**OpenAI API Error:**
- Check `.env` file has valid `OPENAI_API_KEY`
- Verify key format: `sk-proj-...`

**Database Connection Failed:**
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

**Docker Build Failed:**
- Check Dockerfile syntax
- Ensure all required files exist
- Clean Docker cache: `docker system prune`

**Frontend Won't Load:**
- Check Node.js version (requires 18+)
- Run `npm install` in front/ directory
- Check for port conflicts

**Nginx Configuration Error:**
- Validate syntax: `nginx -t`
- Check file permissions
- Verify upstream servers are running

### Getting Help:
1. Check logs in `back/logs/django.log`
2. Use `docker logs <container-name>` for container issues
3. Run individual test sections from `test_production.sh`
