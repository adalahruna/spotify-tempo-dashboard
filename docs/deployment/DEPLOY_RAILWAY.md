# 🚂 Deploy ke Railway - Step by Step

## 📋 **Prerequisites**

- [ ] Git installed
- [ ] GitHub account
- [ ] Railway account (sign up dengan GitHub)
- [ ] Project sudah di-commit ke Git

---

## 🎯 **Railway Advantages**

✅ Support Python + Flask
✅ Built-in PostgreSQL
✅ Auto-deploy dari GitHub
✅ Always online (no sleep)
✅ $5 free credit/month
✅ Custom domain support
✅ Environment variables
✅ Logs & monitoring

---

## 📦 **Step 1: Prepare Project (10 menit)**

### 1.1 Create `requirements.txt` (if not exist)
```bash
cd "d:\Semester 5\BIG DATA\Project"
pip freeze > requirements.txt
```

### 1.2 Create `runtime.txt`
```bash
echo "python-3.11" > runtime.txt
```

### 1.3 Create `Procfile`
```bash
echo "web: gunicorn api.search_api:app" > Procfile
```

### 1.4 Install Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### 1.5 Create `railway.json` (optional config)
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn api.search_api:app --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### 1.6 Update `search_api.py` untuk production

Add at top of `api/search_api.py`:
```python
import os

# Get port from environment (Railway sets this)
PORT = int(os.environ.get('PORT', 5000))
```

Change at bottom:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
```

### 1.7 Create `.env.example` (documentation)
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
PORT=5000
FLASK_ENV=production
```

---

## 🌐 **Step 2: Push to GitHub (5 menit)**

### 2.1 Initialize Git (if not done)
```bash
cd "d:\Semester 5\BIG DATA\Project"
git init
```

### 2.2 Create `.gitignore`
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Models (too large for GitHub)
models/*.pkl

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### 2.3 Commit all files
```bash
git add .
git commit -m "Complete Spotify Tempo Analysis Dashboard with ML predictions"
```

### 2.4 Create GitHub repo
1. Go to https://github.com/new
2. Repo name: `spotify-tempo-dashboard`
3. Description: "ML-powered Spotify music analysis with 1.2M tracks"
4. Public or Private (your choice)
5. Don't initialize with README (already have)
6. Click "Create repository"

### 2.5 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git
git branch -M main
git push -u origin main
```

---

## 🚂 **Step 3: Deploy to Railway (5 menit)**

### 3.1 Sign up / Login
1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway

### 3.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Find your `spotify-tempo-dashboard` repo
4. Click "Deploy Now"

### 3.3 Add PostgreSQL
1. Click "+ New" in your project
2. Select "Database" → "PostgreSQL"
3. Wait for provisioning (~30 seconds)
4. PostgreSQL URL will be auto-generated

### 3.4 Link Database to App
Railway will auto-inject `DATABASE_URL` as environment variable.

---

## ⚙️ **Step 4: Configure Environment (3 menit)**

### 4.1 Set Environment Variables
1. Click on your Flask app service
2. Go to "Variables" tab
3. Add these variables:

```
PORT = 5000
FLASK_ENV = production
PYTHONUNBUFFERED = 1
```

### 4.2 Get Database URL
1. Click on PostgreSQL service
2. Go to "Connect" tab
3. Copy "DATABASE_URL"
4. Should look like: `postgresql://user:pass@host.railway.app:5432/railway`

---

## 📊 **Step 5: Migrate Data to Railway PostgreSQL (10 menit)**

### Option A: Using pg_dump (Recommended)

**On your local machine:**
```bash
# Export local database
pg_dump -h localhost -U postgres -d spotify_music_db -F c -f spotify_dump.backup

# Import to Railway (get URL from Railway dashboard)
pg_restore -h host.railway.app -U postgres -d railway spotify_dump.backup
```

### Option B: Using Python script

Create `scripts/migrate_to_railway.py`:
```python
import psycopg2
import os

# Source (local)
SOURCE_URL = "postgresql://postgres:runadb@localhost:5432/spotify_music_db"

# Destination (Railway) - get from Railway dashboard
DEST_URL = os.environ.get('RAILWAY_DATABASE_URL', 'postgresql://...')

print("Connecting to source...")
source = psycopg2.connect(SOURCE_URL)
source_cur = source.cursor()

print("Connecting to destination...")
dest = psycopg2.connect(DEST_URL)
dest_cur = dest.cursor()

print("Creating table...")
dest_cur.execute("""
    CREATE TABLE IF NOT EXISTS spotify_tracks_raw (
        -- Your table schema here
    )
""")

print("Copying data...")
source_cur.execute("SELECT * FROM spotify_tracks_raw LIMIT 100000")  # Adjust limit
rows = source_cur.fetchall()

print(f"Inserting {len(rows)} rows...")
# Insert logic here

dest.commit()
print("✅ Migration complete!")
```

### Option C: Upload CSV (Simplest)

**Export from local:**
```bash
psql -h localhost -U postgres -d spotify_music_db -c "\COPY spotify_tracks_raw TO 'tracks.csv' CSV HEADER"
```

**Import to Railway:**
```bash
psql -h host.railway.app -U postgres -d railway -c "\COPY spotify_tracks_raw FROM 'tracks.csv' CSV HEADER"
```

---

## 🎨 **Step 6: Deploy Frontend (Dashboard)**

Railway will auto-deploy everything. But frontend needs special handling.

### Option A: Serve via Flask (Easiest)

Update `search_api.py`:
```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('../dashboard', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../dashboard', path)
```

### Option B: Separate Frontend (Advanced)

Deploy dashboard separately on Vercel:
1. Create `vercel.json` in dashboard folder:
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://your-railway-api.railway.app/api/$1" }
  ]
}
```

2. Deploy to Vercel:
```bash
cd dashboard
vercel --prod
```

---

## 🔧 **Step 7: Upload ML Models (IMPORTANT!)**

Models are too large for GitHub (>100MB). Upload manually:

### Option A: Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Upload models folder
railway run "mkdir -p models"
# Then use SCP or similar to upload .pkl files
```

### Option B: Direct Upload via Script

Create `scripts/upload_models.py`:
```python
import os
import requests

RAILWAY_API_URL = "https://your-app.railway.app/api/upload-model"

for model_file in os.listdir('models'):
    if model_file.endswith('.pkl'):
        with open(f'models/{model_file}', 'rb') as f:
            files = {'file': f}
            response = requests.post(RAILWAY_API_URL, files=files)
            print(f"Uploaded {model_file}: {response.status_code}")
```

### Option C: Use Cloud Storage

Store models on AWS S3 / Google Cloud Storage:
```python
# In search_api.py
import boto3
s3 = boto3.client('s3')
s3.download_file('your-bucket', 'models/popularity_predictor.pkl', 'popularity_predictor.pkl')
```

---

## ✅ **Step 8: Verify Deployment**

### 8.1 Check App URL
Railway will give you URL like: `https://spotify-tempo-dashboard-production.up.railway.app`

### 8.2 Test Endpoints
```bash
# Test API health
curl https://your-app.railway.app/api/stats/summary

# Test prediction
curl -X POST https://your-app.railway.app/api/predict/all \
  -H "Content-Type: application/json" \
  -d '{"tempo":120,"energy":0.8,"danceability":0.75,...}'
```

### 8.3 Test Dashboard
Open in browser: `https://your-app.railway.app`

Should show:
- ✅ Dashboard loads
- ✅ All 6 tabs working
- ✅ ML Predictions working
- ✅ Data loading from Railway PostgreSQL

---

## 🐛 **Troubleshooting**

### Issue: "Application failed to start"
**Fix:**
- Check Railway logs (click "View Logs")
- Verify `Procfile` is correct
- Check `requirements.txt` has all dependencies

### Issue: "Database connection failed"
**Fix:**
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL service is running
- Test connection with `psql` command

### Issue: "Models not found"
**Fix:**
- Upload models manually (see Step 7)
- Or retrain models on Railway:
```bash
railway run python scripts/train_ml_models.py
```

### Issue: "Frontend not loading"
**Fix:**
- Check if Flask serving static files correctly
- Verify `../dashboard` path is correct
- Check CORS settings in Flask

### Issue: "Port binding error"
**Fix:**
- Make sure using `PORT` from environment:
```python
PORT = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=PORT)
```

---

## 💰 **Cost Estimate**

### Railway Free Tier:
- $5 free credit/month
- ~550 hours runtime
- Enough for thesis demo + presentation

### Usage Breakdown:
- Flask app: ~$3/month
- PostgreSQL: ~$2/month
- **Total: $5/month (FREE with credit)**

### After graduation:
- Keep free tier (limited hours)
- Or upgrade to Hobby ($5/month)
- Or migrate to free alternatives (Render)

---

## 🎯 **Final Checklist**

Before demo:
- [ ] Railway app deployed ✅
- [ ] PostgreSQL populated with data ✅
- [ ] ML models uploaded ✅
- [ ] Dashboard accessible via URL ✅
- [ ] All 6 tabs working ✅
- [ ] ML Predictions working ✅
- [ ] No errors in Railway logs ✅
- [ ] Custom domain (optional) ✅

---

## 🌟 **Pro Tips**

### Custom Domain (Optional)
1. Buy domain (e.g., Niagahoster, Namecheap)
2. Add CNAME: `www.yourdomain.com` → `your-app.railway.app`
3. In Railway: Settings → Domains → Add custom domain

### Environment Switching
```python
import os

if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Production settings
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
else:
    # Development settings
    DEBUG = True
    DATABASE_URL = 'postgresql://localhost/spotify_music_db'
```

### Monitoring
- Railway provides built-in logs
- Monitor via dashboard
- Set up alerts (optional)

### Backup Database
```bash
railway run pg_dump railway > backup.sql
```

---

## 🎓 **For Thesis Presentation**

**Share this URL with dosen:**
```
Production URL: https://spotify-tempo-dashboard-production.up.railway.app
GitHub Repo: https://github.com/YOUR_USERNAME/spotify-tempo-dashboard
```

**Prepare backup:**
- Screenshots of working app
- Video recording of demo
- Local version (if internet fails)

---

## 📝 **Deployment Checklist Summary**

```bash
# 1. Prepare files
✅ requirements.txt
✅ runtime.txt
✅ Procfile
✅ railway.json
✅ .gitignore

# 2. Push to GitHub
✅ git init
✅ git commit
✅ git push

# 3. Railway setup
✅ Create project
✅ Add PostgreSQL
✅ Set environment variables
✅ Deploy

# 4. Upload data & models
✅ Migrate database
✅ Upload ML models

# 5. Test
✅ API endpoints
✅ Dashboard
✅ ML Predictions
```

---

## 🎉 **Success!**

Your app is now live at:
`https://your-app.railway.app` 🚀

**Next steps:**
1. Test all features
2. Share URL with dosen
3. Prepare demo script
4. Take screenshots for documentation

**Congratulations on deploying! 🎊**
