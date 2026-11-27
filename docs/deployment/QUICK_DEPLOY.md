# ⚡ Quick Deploy - Railway (5 Minutes)

Cara tercepat untuk deploy aplikasi ini ke production.

## 🎯 Steps

### 1️⃣ Push ke GitHub (2 min)
```bash
# Initialize git (jika belum)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create GitHub repo & push
gh repo create spotify-tempo-dashboard --public --source=. --remote=origin --push
```

**Atau manual:**
1. Create repo di [github.com/new](https://github.com/new)
2. Follow instruksi yang muncul

---

### 2️⃣ Deploy ke Railway (2 min)

1. **Buka Railway:** [railway.app](https://railway.app)
2. **Login** dengan GitHub
3. **New Project** → "Deploy from GitHub repo"
4. **Select** repository kamu
5. **Wait** for auto-deploy (1-2 menit)

Railway akan auto-detect:
- `requirements.txt` → Install dependencies
- `Procfile` → Start with Gunicorn
- `runtime.txt` → Use Python 3.11

---

### 3️⃣ Add PostgreSQL Database (1 min)

1. Di Railway project dashboard
2. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
3. Done! `DATABASE_URL` auto-injected ke environment

---

### 4️⃣ Add Environment Variables (30 sec)

Go to: **Variables tab** → Add:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-random-secret-key-here-change-this
CORS_ORIGINS=*
```

**Note:** `DATABASE_URL` sudah auto-set oleh Railway!

---

### 5️⃣ Get Your API URL (10 sec)

1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"**
3. Copy URL: `https://your-app.up.railway.app`

---

### 6️⃣ Update Frontend (30 sec)

Edit `dashboard/app.js` line 1:
```javascript
const API_BASE_URL = 'https://your-app.up.railway.app/api';
```

---

### 7️⃣ Deploy Frontend (1 min)

**Option A: Vercel (Recommended)**
```bash
cd dashboard
vercel --prod
```

**Option B: Netlify**
- Go to [netlify.com/drop](https://netlify.com/drop)
- Drag & drop `dashboard` folder
- Done!

**Option C: GitHub Pages**
```bash
git subtree push --prefix dashboard origin gh-pages
```
Access: `https://username.github.io/repo-name`

---

## ✅ Test Deployment

### Test API:
```bash
curl https://your-app.up.railway.app/api/health
```

Expected:
```json
{"status":"healthy","database":"connected"}
```

### Test Search:
```bash
curl "https://your-app.up.railway.app/api/search/tracks?q=daft+punk&limit=3"
```

### Test Frontend:
Open browser → Your frontend URL → Try search

---

## 🎉 Done!

Your app is live:
- 🔹 **API:** `https://your-app.up.railway.app`
- 🔹 **Dashboard:** `https://your-dashboard.vercel.app`
- 🔹 **Database:** PostgreSQL on Railway

---

## 🔄 Auto-Deploy

Railway auto-redeploys when you push to GitHub:
```bash
git add .
git commit -m "Update API"
git push
```

Wait 1-2 minutes → Changes live!

---

## 💰 Cost

**Railway Free Tier:**
- $5/month credit (no credit card required)
- Enough for ~500 hours of API uptime
- PostgreSQL included

**Vercel Free Tier:**
- Unlimited static hosting
- 100GB bandwidth

**Total: $0** for hobby projects! 🎉

---

## ❓ Troubleshooting

**Deployment failed?**
- Check Railway logs: Dashboard → Deployments → View Logs
- Verify `requirements.txt` complete
- Check `Procfile` syntax

**Database error?**
- Railway auto-creates `DATABASE_URL`
- Check Variables tab to confirm

**CORS error?**
- Set `CORS_ORIGINS=*` in Variables
- Or specific domain: `CORS_ORIGINS=https://your-frontend.com`

**Still stuck?**
- See full guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 Resources

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Full Deployment Guide](DEPLOYMENT.md)

**Happy Deploying! 🚀**
