# ⚡ Quick Start - Deploy ke Railway (15 Menit)

## 🎯 **Super Cepat - Tanpa Ribet**

### **Step 1: Install Gunicorn** (1 menit)
```powershell
cd "d:\Semester 5\BIG DATA\Project"
pip install gunicorn
pip freeze > requirements.txt
```

### **Step 2: Commit & Push ke GitHub** (3 menit)
```powershell
# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Create GitHub repo (via browser)
# Go to: https://github.com/new
# Name: spotify-tempo-dashboard

# Push
git remote add origin https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git
git branch -M main
git push -u origin main
```

### **Step 3: Deploy ke Railway** (5 menit)
1. **Go to**: https://railway.app
2. **Login** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: `spotify-tempo-dashboard`
6. **Click**: "Deploy Now"
7. **Wait** ~3 minutes for build

### **Step 4: Add PostgreSQL** (2 menit)
1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Wait ~30 seconds for provisioning
4. Done! Database URL auto-injected as `DATABASE_URL`

### **Step 5: Set Environment Variables** (1 menit)
1. Click on **Flask app** service
2. Go to **"Variables"** tab
3. Add:
   ```
   FLASK_ENV = production
   PORT = 5000
   ```
4. Railway will auto-restart

### **Step 6: Get Your URL** (1 menit)
1. Go to **"Settings"** tab
2. Under **"Domains"**, click **"Generate Domain"**
3. You'll get: `https://spotify-tempo-dashboard-production.up.railway.app`
4. **Copy this URL!**

---

## ✅ **Done! Your App is Live!**

**Test it:**
- Open: `https://your-app.railway.app`
- Should see dashboard
- Try ML Predictions tab

---

## 📊 **Upload Data** (Optional - 10 menit)

### Quick Method: Sample Data
Railway PostgreSQL is empty. Upload sample data:

**Option 1: Use Railway CLI**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Connect to database
railway connect
```

**Option 2: Use Python Script**
Create `upload_sample_data.py`:
```python
import psycopg2
import os

# Get Railway DATABASE_URL from Railway dashboard
DATABASE_URL = "postgresql://postgres:xxx@xxx.railway.app:5432/railway"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS spotify_tracks_raw (
        id SERIAL PRIMARY KEY,
        name VARCHAR(500),
        artists VARCHAR(500),
        tempo FLOAT,
        energy FLOAT,
        danceability FLOAT,
        valence FLOAT,
        acousticness FLOAT,
        instrumentalness FLOAT,
        liveness FLOAT,
        speechiness FLOAT,
        loudness FLOAT,
        duration_ms INTEGER,
        year INTEGER,
        key INTEGER,
        mode INTEGER,
        time_signature FLOAT
    )
""")

# Insert sample data (100 tracks for demo)
print("Inserting sample data...")
# Add your insert logic here

conn.commit()
print("✅ Done!")
```

---

## 🚀 **Upload ML Models** (5 menit)

Models tidak ter-upload ke GitHub (terlalu besar). Upload manual:

### Via Railway Dashboard:
1. Go to your Flask service
2. Click **"Variables"**
3. Add: `MODELS_PATH=/app/models`

### Via Railway CLI:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Upload models
railway run "mkdir -p models"
# Then use scp or similar
```

### Or Retrain on Railway:
```bash
railway run python scripts/train_ml_models.py
```

---

## 🐛 **Troubleshooting**

### App not starting?
- Check Railway logs: Click "View Logs"
- Verify `Procfile` exists
- Check `requirements.txt` complete

### Database connection failed?
- Verify `DATABASE_URL` variable exists
- Check PostgreSQL service running
- Test with: `railway run python -c "import psycopg2"`

### Models not found?
- Upload models folder (see above)
- Or retrain: `railway run python scripts/train_ml_models.py`

### Frontend not loading?
- Check Flask app logs
- Verify port binding: `0.0.0.0:$PORT`

---

## 💰 **Free Tier Limits**

Railway gives **$5 credit/month** = ~550 hours runtime

**Perfect for:**
- Thesis demo
- Presentation
- Testing

**After that:**
- Upgrade to Hobby ($5/month)
- Or use Render (free forever)

---

## 🎓 **Share with Dosen**

**Production URL:**
```
https://your-app.railway.app
```

**GitHub Repo:**
```
https://github.com/YOUR_USERNAME/spotify-tempo-dashboard
```

**Demo Script:**
1. Open URL
2. Click "ML Predictions"
3. Set sliders or click preset
4. Click "Predict All"
5. Show results!

---

## 🎉 **Success!**

Your app is now **LIVE** and accessible from anywhere! 🌍

Perfect for thesis presentation! 🎓

---

## 📝 **Alternative: Render (Jika Railway Habis)**

Render punya free tier unlimited:

1. Go to: https://render.com
2. Sign up with GitHub
3. New Web Service → Select repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn api.search_api:app`
6. Add PostgreSQL (free tier)
7. Deploy!

**Trade-off:** App sleeps after 15 menit idle (need 30 detik untuk wake up)

---

**Good luck! 🚀**
