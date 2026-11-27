# 🚀 Deployment Guide - Spotify Tempo Analysis Dashboard

Panduan lengkap untuk deploy aplikasi ke berbagai platform cloud.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Deployment Options](#deployment-options)
  - [Option 1: Railway (Recommended - Easiest)](#option-1-railway-recommended)
  - [Option 2: Render](#option-2-render)
  - [Option 3: Heroku](#option-3-heroku)
  - [Option 4: Vercel (API Only)](#option-4-vercel)
  - [Option 5: VPS/Custom Server](#option-5-vpscustom-server)
- [Database Setup](#database-setup)
- [Frontend Deployment](#frontend-deployment)
- [Testing Deployment](#testing-deployment)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

✅ **Yang harus sudah siap:**
- Git repository (GitHub/GitLab)
- PostgreSQL database (bisa di cloud atau local)
- Firebase project (optional, untuk Firestore)
- Domain name (optional)

---

## Environment Variables

Sebelum deploy, siapkan environment variables berikut:

### Required Variables
```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-random-secret-key-here

# PostgreSQL Database
DB_HOST=your-db-host.com
DB_PORT=5432
DB_NAME=spotify_music_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Or use single DATABASE_URL (for Heroku/Railway)
DATABASE_URL=postgresql://user:password@host:port/dbname

# API Config
PORT=5000
CORS_ORIGINS=*
```

### Optional (for Firestore)
```bash
FIREBASE_API_KEY=your-api-key
FIREBASE_PROJECT_ID=your-project-id
# ... other Firebase configs
```

---

## Deployment Options

### Option 1: Railway (Recommended ⭐)

**Kelebihan:**
- ✅ Gratis $5/bulan credit
- ✅ Auto-deploy dari GitHub
- ✅ Built-in PostgreSQL database
- ✅ Custom domain support
- ✅ Automatic SSL

**Steps:**

1. **Push code ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/username/repo.git
   git push -u origin main
   ```

2. **Deploy ke Railway**
   - Buka [railway.app](https://railway.app)
   - Sign in dengan GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Pilih repository kamu
   - Railway akan auto-detect Python dan deploy

3. **Setup PostgreSQL Database**
   - Di Railway dashboard, click "New" → "Database" → "Add PostgreSQL"
   - Copy `DATABASE_URL` yang auto-generated
   - Add sebagai environment variable

4. **Set Environment Variables**
   - Go to project → Variables
   - Add semua variables dari `.env.example`
   - `DATABASE_URL` sudah auto-set oleh Railway

5. **Deploy Dashboard (Static Files)**
   - Option A: Deploy dashboard di folder terpisah (Vercel/Netlify)
   - Option B: Serve dari Flask (tambahkan route untuk static files)

6. **Get Deployment URL**
   - Railway akan provide URL: `your-app.railway.app`
   - Bisa setup custom domain di Settings → Domains

---

### Option 2: Render

**Kelebihan:**
- ✅ Free tier tersedia
- ✅ Auto SSL
- ✅ Built-in PostgreSQL
- ✅ Auto-deploy dari Git

**Steps:**

1. **Push ke GitHub** (sama seperti Railway)

2. **Deploy ke Render**
   - Buka [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     ```
     Name: spotify-tempo-api
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: gunicorn wsgi:application --config gunicorn_config.py
     ```

3. **Setup Database**
   - Click "New" → "PostgreSQL"
   - Copy connection string
   - Add ke Environment Variables sebagai `DATABASE_URL`

4. **Environment Variables**
   - Di Web Service → Environment
   - Add all variables dari `.env.example`

5. **Deploy**
   - Render akan auto-build dan deploy
   - URL: `https://your-app.onrender.com`

---

### Option 3: Heroku

**Kelebihan:**
- ✅ Mature platform
- ✅ Banyak add-ons
- ✅ Good documentation

**Catatan:** Heroku menghapus free tier November 2022. Sekarang mulai dari $5/bulan.

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # Windows (via Chocolatey)
   choco install heroku-cli
   
   # Or download from heroku.com/install
   ```

2. **Login & Create App**
   ```bash
   heroku login
   heroku create spotify-tempo-api
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   # DATABASE_URL auto-set by Heroku Postgres addon
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

### Option 4: Vercel (API Only)

**Catatan:** Vercel bagus untuk frontend, tapi ada limitasi untuk Flask API (serverless functions).

**Steps:**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables**
   - Di Vercel dashboard → Settings → Environment Variables
   - Add all variables

**⚠️ Limitation:** Database connection pooling terbatas karena serverless nature.

---

### Option 5: VPS/Custom Server

**Untuk yang ingin full control (DigitalOcean, AWS EC2, Azure VM, etc.)**

**Steps:**

1. **Setup Server**
   ```bash
   # SSH ke server
   ssh user@your-server-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python & dependencies
   sudo apt install python3-pip python3-venv nginx postgresql -y
   ```

2. **Clone Repository**
   ```bash
   cd /var/www
   git clone https://github.com/username/your-repo.git
   cd your-repo
   ```

3. **Setup Python Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   nano .env  # Edit dengan credentials kamu
   ```

5. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/spotify-api.service
   ```
   
   Paste:
   ```ini
   [Unit]
   Description=Spotify Tempo Analysis API
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/your-repo
   Environment="PATH=/var/www/your-repo/venv/bin"
   ExecStart=/var/www/your-repo/venv/bin/gunicorn wsgi:application --config gunicorn_config.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Start Service**
   ```bash
   sudo systemctl start spotify-api
   sudo systemctl enable spotify-api
   sudo systemctl status spotify-api
   ```

7. **Setup Nginx Reverse Proxy**
   ```bash
   sudo nano /etc/nginx/sites-available/spotify-api
   ```
   
   Paste:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location /api {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   
       location / {
           root /var/www/your-repo/dashboard;
           try_files $uri $uri/ /index.html;
       }
   }
   ```
   
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/spotify-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## Database Setup

### Option A: Managed PostgreSQL (Recommended)

**Railway PostgreSQL:**
- Auto-provisioned dengan deployment
- Connection string auto-injected sebagai `DATABASE_URL`

**Neon.tech (Serverless Postgres):**
- Free tier: 0.5GB storage
- [console.neon.tech](https://console.neon.tech)
- Copy connection string ke `DATABASE_URL`

**Supabase:**
- Free tier: 500MB database
- [supabase.com](https://supabase.com)
- Include Firestore-like realtime features

### Option B: Self-hosted PostgreSQL

Jika database masih di local, harus:
1. Expose port 5432 (use ngrok atau tunneling)
2. Atau migrate database ke cloud

**Migrate data:**
```bash
# Dump local database
pg_dump -U postgres spotify_music_db > spotify_dump.sql

# Restore ke cloud database
psql -h your-cloud-host -U your-user -d your-db < spotify_dump.sql
```

---

## Frontend Deployment

Dashboard (static files) bisa di-deploy terpisah:

### Option 1: Vercel (Recommended untuk Frontend)
```bash
# Di folder dashboard/
vercel --prod
```

### Option 2: Netlify
- Drag & drop folder `dashboard/` ke [netlify.com/drop](https://netlify.com/drop)
- Atau connect GitHub repo

### Option 3: GitHub Pages
```bash
# Push dashboard ke gh-pages branch
git subtree push --prefix dashboard origin gh-pages
```

### Update API URL di Frontend
Edit `dashboard/app.js`:
```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

---

## Testing Deployment

### 1. Test API Health
```bash
curl https://your-api-domain.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Test Search Endpoint
```bash
curl "https://your-api-domain.com/api/search/tracks?q=daft%20punk&limit=5"
```

### 3. Test Dashboard
- Open browser: `https://your-frontend-domain.com`
- Try search functionality
- Check browser console for errors (F12)

---

## Troubleshooting

### ❌ Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```

**Fix:**
- Check `DATABASE_URL` format benar
- Verify database credentials
- Check firewall/security group allows connections
- For cloud DB, whitelist deployment server IP

### ❌ CORS Error in Browser
```
Access to fetch blocked by CORS policy
```

**Fix:**
- Set `CORS_ORIGINS` ke frontend domain:
  ```bash
  CORS_ORIGINS=https://your-frontend.com
  ```
- Atau `*` untuk allow semua (development only)

### ❌ Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```

**Fix:**
- Ensure `requirements.txt` lengkap
- Rebuild deployment
- Check build logs

### ❌ Gunicorn Timeout
```
[CRITICAL] WORKER TIMEOUT
```

**Fix:**
- Increase timeout di `gunicorn_config.py`:
  ```python
  timeout = 300  # 5 minutes
  ```
- Optimize database queries
- Add connection pooling

### ❌ Static Files Not Served
**Fix:** Add route di `search_api.py`:
```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('dashboard', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('dashboard', path)
```

---

## 📊 Monitoring & Logs

### Railway
- Dashboard → Deployments → Logs
- Real-time streaming logs

### Heroku
```bash
heroku logs --tail
```

### Render
- Dashboard → Logs tab

### VPS
```bash
# Systemd logs
sudo journalctl -u spotify-api -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## 🎉 Success Checklist

- [ ] API deployed dan accessible
- [ ] Database connected
- [ ] Frontend deployed
- [ ] Search functionality works
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] SSL/HTTPS enabled
- [ ] Custom domain configured (optional)
- [ ] Monitoring setup (optional)

---

## 📞 Support

Jika ada masalah:
1. Check deployment logs
2. Verify environment variables
3. Test API endpoints dengan curl/Postman
4. Check browser console untuk frontend errors

**Happy Deploying! 🚀**
