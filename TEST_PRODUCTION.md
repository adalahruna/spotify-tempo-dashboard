# 🧪 Test Production Setup Locally

Test setup production di local sebelum deploy ke cloud.

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database running
- Git

---

## 🚀 Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env dengan credentials kamu
```

**Windows:**
```bash
notepad .env
```

**Linux/Mac:**
```bash
nano .env
```

Fill in:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=test-secret-key-123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spotify_music_db
DB_USER=postgres
DB_PASSWORD=runadb
CORS_ORIGINS=*
PORT=5000
```

---

### 3. Test with Gunicorn (Production Server)

```bash
# Start dengan Gunicorn
gunicorn wsgi:application --config gunicorn_config.py
```

**Expected output:**
```
============================================================
  SPOTIFY TEMPO ANALYSIS API - STARTING
============================================================
Workers: 5
Bind: 0.0.0.0:5000
Timeout: 120s
============================================================
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 1234
```

---

### 4. Test API Endpoints

**Open new terminal**, test endpoints:

#### Health Check
```bash
curl http://localhost:5000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### Summary Stats
```bash
curl http://localhost:5000/api/stats/summary
```

#### Search Tracks
```bash
curl "http://localhost:5000/api/search/tracks?q=daft%20punk&limit=5"
```

#### Search by Tempo
```bash
curl "http://localhost:5000/api/search/tracks?tempo_min=100&tempo_max=120&limit=10"
```

---

### 5. Test Frontend Integration

**Start static file server:**

```bash
# Method 1: Python HTTP server
python -m http.server 8000 --directory dashboard

# Method 2: Node.js http-server (if installed)
npx http-server dashboard -p 8000
```

**Open browser:**
```
http://localhost:8000
```

**Test:**
- ✅ Dashboard loads
- ✅ Summary cards show data
- ✅ Dot matrix visualization renders
- ✅ Search functionality works
- ✅ Top tracks table loads

---

### 6. Load Testing (Optional)

Test how many requests server can handle:

**Install Apache Bench:**
```bash
# Windows (via Chocolatey)
choco install apachebench

# Linux
sudo apt install apache2-utils

# Mac
brew install ab
```

**Run load test:**
```bash
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5000/api/health

# Test search endpoint
ab -n 50 -c 5 "http://localhost:5000/api/search/tracks?q=test&limit=10"
```

**Check results:**
- Requests per second
- Time per request
- Failed requests (should be 0)

---

### 7. Check Logs

Gunicorn logs akan muncul di terminal:

**Good log example:**
```
[INFO] GET /api/health 200 15ms
[INFO] GET /api/search/tracks 200 234ms
[INFO] GET /api/stats/summary 200 89ms
```

**Error log example:**
```
[ERROR] GET /api/search/tracks 500 1234ms
[ERROR] Database connection failed
```

---

## 🐛 Common Issues & Fixes

### ❌ ModuleNotFoundError: No module named 'gunicorn'
```bash
pip install gunicorn
```

### ❌ ModuleNotFoundError: No module named 'dotenv'
```bash
pip install python-dotenv
```

### ❌ psycopg2.OperationalError: could not connect
**Fix:** Check PostgreSQL running:
```bash
# Windows (check service)
Get-Service postgresql*

# Linux
sudo systemctl status postgresql

# Test connection
psql -U postgres -d spotify_music_db -c "SELECT 1"
```

### ❌ Address already in use (Port 5000)
**Fix:** Kill process on port 5000:

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

### ❌ CORS Error in Browser
**Fix:** Set in `.env`:
```
CORS_ORIGINS=*
```

Restart Gunicorn.

---

## ✅ Production Readiness Checklist

Before deploying to cloud:

- [ ] All endpoints tested and working
- [ ] Database connection successful
- [ ] Environment variables properly set
- [ ] `.env` file NOT in git (check `.gitignore`)
- [ ] `SECRET_KEY` changed to random string
- [ ] CORS configured correctly
- [ ] Frontend can communicate with API
- [ ] Load test passed
- [ ] No errors in Gunicorn logs
- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` syntax correct
- [ ] `gunicorn_config.py` configured

---

## 🎯 Production vs Development Differences

| Feature | Development | Production |
|---------|-------------|------------|
| Server | Flask dev server | Gunicorn WSGI |
| Debug mode | `DEBUG=True` | `DEBUG=False` |
| Auto-reload | Yes | No |
| Workers | 1 | Multiple (2-5) |
| Error pages | Detailed | Generic |
| Logging | Verbose | Structured |
| CORS | `*` (all) | Specific domains |
| HTTPS | Optional | Required |

---

## 🔄 Simulate Production Environment

To test exactly like production:

```bash
# Set production environment
export FLASK_ENV=production  # Linux/Mac
set FLASK_ENV=production     # Windows CMD
$env:FLASK_ENV="production"  # Windows PowerShell

# Disable debug
export FLASK_DEBUG=False

# Start with Gunicorn config
gunicorn wsgi:application --config gunicorn_config.py

# Test with production domain
# Add to hosts file: 127.0.0.1 api.local
curl http://api.local:5000/api/health
```

---

## 📊 Performance Benchmarks

**Expected Response Times (Local):**
- Health check: < 50ms
- Stats summary: < 100ms
- Search (no filter): < 200ms
- Search (with filters): < 300ms

**If slower:**
- Add database indexes
- Enable query caching
- Optimize database queries
- Use connection pooling

---

## 🚀 Next Steps

Once all tests pass:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Production ready"
   git push
   ```

2. **Deploy:**
   - Follow [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for Railway
   - Or [DEPLOYMENT.md](DEPLOYMENT.md) for other platforms

3. **Monitor:**
   - Check deployment logs
   - Test production URL
   - Setup monitoring (optional)

---

## 📚 Resources

- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Flask Production Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [PostgreSQL Tuning](https://pgtune.leopard.in.ua/)

**Good Luck! 🎉**
