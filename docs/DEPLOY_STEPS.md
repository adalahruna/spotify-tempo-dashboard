# 🚀 Deployment Steps - Vercel + Railway

## 📋 **Quick Overview**

**Architecture:**
```
Frontend (Vercel) → Backend (Railway) → Database (PostgreSQL) + Cache (Firebase)
```

**Time:** 20 minutes total
**Cost:** $0 (free tiers)

---

## ⚡ **Step-by-Step Guide**

### **PHASE 1: Backend (Railway) - 10 minutes**

#### 1. Install Gunicorn
```powershell
cd "d:\Semester 5\BIG DATA\Project"
pip install gunicorn
pip freeze > requirements.txt
```

#### 2. Commit & Push to GitHub
```powershell
git add .
git commit -m "Production-ready with Vercel + Railway"
git push origin main
```

#### 3. Deploy to Railway
1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `spotify-tempo-dashboard`
6. Click "Deploy Now"
7. Wait ~3 minutes

#### 4. Add PostgreSQL
1. In Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Wait ~30 seconds
4. Done! `DATABASE_URL` auto-injected

#### 5. Set Environment Variables
Click on Flask service → Variables tab → Add:
```
FLASK_ENV=production
RAILWAY_ENVIRONMENT=true
VERCEL_DOMAIN=spotify-tempo-dashboard.vercel.app
```

#### 6. Get Railway URL
1. Go to Settings tab
2. Click "Generate Domain"
3. Copy URL: `https://spotify-api-production-xxxx.up.railway.app`
4. **Save this URL!** ⭐

---

### **PHASE 2: Frontend (Vercel) - 10 minutes**

#### 1. Update vercel.json
Open `dashboard/vercel.json` and replace:
```json
"destination": "https://REPLACE_WITH_YOUR_RAILWAY_URL/api/:path*"
```

With your Railway URL from Phase 1 step 6.

#### 2. Install Vercel CLI
```powershell
npm install -g vercel
```

#### 3. Deploy to Vercel
```powershell
cd dashboard
vercel login
# Follow browser login

vercel --prod
# Answer prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? spotify-tempo-dashboard
# - In which directory? ./
# - Override settings? N
```

#### 4. Wait for Deployment
- Build time: ~1 minute
- You'll get URL: `https://spotify-tempo-dashboard.vercel.app`

#### 5. Set Environment Variables (Optional)
If needed, go to Vercel dashboard:
1. Project → Settings → Environment Variables
2. Add: `NEXT_PUBLIC_API_URL` = your Railway URL

---

## ✅ **Verification**

### Test Backend (Railway)
```bash
# Health check
curl https://your-railway-url.railway.app/api/health

# Should return:
{
  "status": "healthy",
  "timestamp": "2024-xx-xx..."
}
```

### Test Frontend (Vercel)
1. Open: `https://your-app.vercel.app`
2. Check console (F12) for:
   - `🌐 Environment: Vercel Production`
   - `📡 API Base URL: /api`
3. Click each tab:
   - ✅ Overview
   - ✅ Search & Query
   - ✅ ML Predictions
   - ✅ Tempo Zones
   - ✅ Top Tracks
   - ✅ Methodology

### Test Integration
1. Go to ML Predictions tab
2. Click "High Energy Dance" preset
3. Click "Predict All"
4. Should see results in <3 seconds
5. Check Network tab (F12) for API calls

---

## 🐛 **Common Issues**

### Issue 1: CORS Error
**Symptom:** Browser console shows CORS error

**Fix:**
1. Go to Railway dashboard
2. Add environment variable:
   ```
   VERCEL_DOMAIN=your-app.vercel.app
   ```
3. Restart Railway service

### Issue 2: API Not Found (404)
**Symptom:** `/api/predict/all` returns 404

**Check:**
1. Railway URL correct in `vercel.json`?
2. Railway app is running? (check logs)
3. Try direct Railway URL in browser

**Fix:**
```json
// In dashboard/vercel.json, verify:
"destination": "https://correct-railway-url.railway.app/api/:path*"
```

### Issue 3: Models Not Found
**Symptom:** Predictions fail with "Model not found"

**Fix Option A - Retrain on Railway:**
```bash
railway run python scripts/train_ml_models.py
```

**Fix Option B - Upload manually:**
```bash
# Install Railway CLI
npm i -g @railway/cli
railway login
railway link
# Then upload models folder
```

### Issue 4: Slow First Load
**Symptom:** First prediction takes 10+ seconds

**Cause:** Cold start (Railway sleeping)

**Fix:** Keep warm with cron job
1. Go to cron-job.org
2. Create job: ping Railway URL every 5 minutes
3. URL: `https://your-railway-url.railway.app/api/health`

---

## 📊 **Final URLs**

After successful deployment:

```
✅ Production Dashboard:
   https://spotify-tempo-dashboard.vercel.app

✅ Backend API:
   https://spotify-api-production-xxxx.up.railway.app

✅ GitHub Repo:
   https://github.com/YOUR_USERNAME/spotify-tempo-dashboard
```

---

## 🎓 **Share with Dosen**

**Send this:**
```
Dashboard: https://spotify-tempo-dashboard.vercel.app
GitHub: https://github.com/YOUR_USERNAME/spotify-tempo-dashboard

Arsitektur:
- Frontend: Vercel CDN (global)
- Backend: Railway (Flask API + PostgreSQL)
- Cache: Firebase Firestore
- ML: 4 trained models (93% accuracy)
```

---

## 💰 **Cost Breakdown**

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Free | $0 |
| Railway | Free ($5 credit) | $0 |
| Firebase | Free (Spark) | $0 |
| **Total** | | **$0/month** |

Perfect for thesis! 🎉

---

## 🔄 **Updates & Redeployment**

### Update Frontend
```powershell
cd dashboard
# Make changes
git add .
git commit -m "Update dashboard"
git push origin main

# Vercel auto-deploys on push!
# Or manual:
vercel --prod
```

### Update Backend
```powershell
# Make changes to api/
git add .
git commit -m "Update API"
git push origin main

# Railway auto-deploys on push!
```

### View Logs
**Vercel:** Dashboard → Project → Logs
**Railway:** Dashboard → Service → View Logs

---

## 🎯 **Performance Tips**

### Optimize Frontend
1. Minimize JavaScript
2. Compress images
3. Use CDN for external libraries
4. Enable caching

### Optimize Backend
1. Add Redis cache (Railway addon)
2. Database indexes
3. Query optimization
4. Keep models in memory

### Monitor Performance
- Vercel Analytics (built-in)
- Railway metrics
- Firebase monitoring

---

## 📝 **Deployment Checklist**

**Before deploying:**
- [ ] Gunicorn installed
- [ ] All changes committed
- [ ] Railway URL obtained
- [ ] `vercel.json` updated
- [ ] `app.js` updated (auto-detect)
- [ ] CORS configured

**After deploying:**
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] All 6 tabs working
- [ ] ML Predictions functional
- [ ] No console errors
- [ ] API calls successful

**Documentation:**
- [ ] README updated with URLs
- [ ] Screenshots taken
- [ ] Demo script prepared
- [ ] Shared with dosen

---

## 🎉 **Success Criteria**

Your deployment is successful if:

1. ✅ Dashboard loads in <200ms (globally)
2. ✅ All 6 tabs functional
3. ✅ ML Predictions return results (<3s)
4. ✅ No CORS errors
5. ✅ No 404 errors
6. ✅ Works on mobile
7. ✅ Professional URL
8. ✅ Always online (no sleep)

---

## 🚀 **Ready to Deploy?**

**Current status:**
- ✅ Files prepared (vercel.json, Procfile, etc)
- ✅ Code production-ready
- ✅ CORS configured
- ✅ Environment detection added

**Next step:**
```powershell
# 1. Backend to Railway
git push origin main
# Then deploy via Railway dashboard

# 2. Frontend to Vercel
cd dashboard
vercel --prod
```

**Let's go! 🎊**
