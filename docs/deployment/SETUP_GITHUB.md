# 📦 Setup GitHub - Quick Guide

## **Step 1: Create GitHub Repository**

1. **Open browser**, go to: https://github.com/new

2. **Fill in details:**
   - Repository name: `spotify-tempo-dashboard`
   - Description: `ML-powered Spotify music analysis with 1.2M tracks and 4 prediction models`
   - Visibility: **Public** (atau Private kalau mau)
   - ❌ **DON'T** initialize with README (kita sudah punya)
   - ❌ **DON'T** add .gitignore (kita sudah punya)
   - ❌ **DON'T** choose license (optional)

3. **Click "Create repository"**

4. **Copy the repository URL**, akan seperti:
   ```
   https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git
   ```

---

## **Step 2: Connect Local Repo to GitHub**

Open PowerShell/Terminal di project folder, run:

```powershell
cd "d:\Semester 5\BIG DATA\Project"

# Add remote (ganti YOUR_USERNAME dengan username GitHub kamu)
git remote add origin https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git

# Verify
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git (fetch)
# origin  https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git (push)
```

---

## **Step 3: Push to GitHub**

```powershell
# Push main branch
git push -u origin main

# Enter GitHub username dan password/token jika diminta
```

**If asked for authentication:**
- Username: your GitHub username
- Password: use **Personal Access Token** (NOT your GitHub password)

**To create Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control)
4. Copy token and use as password

---

## **Step 4: Verify on GitHub**

1. Go to: `https://github.com/YOUR_USERNAME/spotify-tempo-dashboard`
2. You should see all your files!
3. Check:
   - ✅ `api/` folder
   - ✅ `dashboard/` folder
   - ✅ `scripts/` folder
   - ✅ `Procfile`
   - ✅ `requirements.txt`
   - ✅ `README.md`

---

## **Troubleshooting**

### Issue: "fatal: 'origin' already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git
```

### Issue: Authentication failed
Use Personal Access Token instead of password:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Select: repo (all)
5. Copy token
6. Use as password when pushing

### Issue: "failed to push some refs"
```powershell
# Pull first
git pull origin main --rebase

# Then push
git push -u origin main
```

---

## **Next: Deploy to Railway**

After GitHub setup done, lanjut ke Railway! 🚀

**Current status:**
- ✅ Local repo ready
- ✅ Files committed
- ⏳ GitHub remote (you're doing this now)
- ⏳ Push to GitHub (next)
- ⏳ Railway deployment (after push)
