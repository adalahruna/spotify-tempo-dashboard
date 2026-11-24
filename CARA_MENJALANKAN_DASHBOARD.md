# 🚀 Cara Menjalankan Dashboard untuk Presentasi

## 📋 **Checklist Sebelum Mulai**

Pastikan sudah terinstall:
- ✅ Python 3.12 atau lebih baru
- ✅ PostgreSQL (database sudah import 1.2M tracks)
- ✅ Git Bash atau PowerShell

---

## 🎯 **Cara Menjalankan (Step by Step)**

### **Step 1: Buka Terminal/PowerShell**

1. Tekan `Win + R`
2. Ketik `powershell` → Enter
3. Atau klik kanan Start menu → pilih "Windows PowerShell"

---

### **Step 2: Masuk ke Folder Project**

```powershell
cd "d:\Semester 5\BIG DATA\Project"
```

**Cek apakah sudah benar:**
```powershell
ls
```
Harusnya muncul folder: `api/`, `dashboard/`, `scripts/`, dll.

---

### **Step 3: Start PostgreSQL Database**

**Check apakah database sudah running:**

```powershell
# Cek status PostgreSQL
Get-Service -Name postgresql*

# Kalau tidak running, start dengan:
Start-Service postgresql-x64-14  # Sesuaikan dengan versi PostgreSQL kamu
```

**Atau:**
- Buka **pgAdmin 4**
- Server harusnya auto-start
- **Database:** `spotify_music_db`
- **User:** `postgres`
- **Password:** `runadb`

---

### **Step 4: Start Flask API Backend**

Buka terminal **pertama** dan jalankan:

```powershell
cd "d:\Semester 5\BIG DATA\Project"
python api/search_api.py
```

**Output yang benar:**
```
🔓 CORS enabled for development
✅ ML Prediction endpoints loaded
============================================================
  SPOTIFY SEARCH API
============================================================
...
Starting server on http://localhost:5000
Environment: Production
 * Running on http://127.0.0.1:5000
```

✅ **Flask API jalan di http://localhost:5000**

**JANGAN TUTUP TERMINAL INI!** Biarkan tetap running.

---

### **Step 5: Start Dashboard Frontend**

Buka terminal **kedua** (baru) dan jalankan:

```powershell
cd "d:\Semester 5\BIG DATA\Project\dashboard"
python -m http.server 8000
```

**Output yang benar:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

✅ **Dashboard jalan di http://localhost:8000**

**JANGAN TUTUP TERMINAL INI!** Biarkan tetap running.

---

### **Step 6: Buka Dashboard di Browser**

1. Buka **Google Chrome** atau **Microsoft Edge**
2. Ketik di address bar: **http://localhost:8000**
3. Dashboard akan load dengan data dari PostgreSQL lokal (1.2M tracks)

**Atau pakai Simple Dashboard:**
- **http://localhost:8000/simple.html** (lebih stabil, recommended untuk demo)

---

## 🧪 **Test Dashboard Berfungsi**

### **Test 1: Summary Stats**
- Total Tracks: **1,204,025** ✅
- Average Tempo: **117.6 BPM** ✅
- Sweet Spot: **22.2%** ✅

### **Test 2: Search Tracks**
Coba search:
- **"shape"** → harusnya muncul "Shape of You" by Ed Sheeran
- **"blinding"** → harusnya muncul "Blinding Lights" by The Weeknd
- **Tempo 100-120** → harusnya muncul tracks di sweet spot

### **Test 3: Top Tracks**
- Scroll ke bawah
- Harusnya muncul tabel dengan 10 tracks
- Semua di range 100-120 BPM (Sweet Spot)

---

## ⚠️ **Troubleshooting**

### **Problem: "Module not found" atau Import Error**

**Solusi:**
```powershell
# Install dependencies lagi
pip install -r requirements.txt
```

---

### **Problem: Filter buttons not working / 404 errors**

**FIXED!** ✅ Update terbaru sudah fix bug ini.

**Solusi:**
```powershell
# Hard refresh browser
Ctrl + Shift + R

# Kalau masih error, clear browser cache:
Ctrl + Shift + Delete → Clear cached images and files

# Check API endpoint in console (F12):
# Should show: http://localhost:5000/api/...
# NOT: http://[::1]:8000/api/...
```

---

### **Problem: "Database connection error"**

**Solusi:**
```powershell
# Check PostgreSQL status
Get-Service postgresql*

# Check database exists
psql -U postgres -c "\l" | Select-String "spotify_music_db"

# Kalau database tidak ada, import lagi
psql -U postgres -f database/spotify_tracks_backup.sql
```

---

### **Problem: "Port 5000 already in use"**

**Solusi:**
```powershell
# Stop process yang pakai port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Atau ganti port di api/search_api.py
# Line terakhir: app.run(host='0.0.0.0', port=5001)
```

---

### **Problem: "Port 8000 already in use"**

**Solusi:**
```powershell
# Stop process yang pakai port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Atau ganti port
python -m http.server 8001
# Lalu buka http://localhost:8001
```

---

### **Problem: Dashboard tidak show data / search tidak jalan**

**Solusi:**

1. **Hard refresh browser:** `Ctrl + Shift + R`
2. **Clear browser cache:** `Ctrl + Shift + Delete` → Clear cached images/files
3. **Gunakan Simple Dashboard:** http://localhost:8000/simple.html
4. **Check console browser:** Tekan `F12` → Console tab, lihat error apa

---

## 🎤 **Skenario Presentasi**

### **1. Opening (1 menit)**
> "Saya akan demo aplikasi analisis tempo Spotify yang saya buat menggunakan dataset 1.2 juta tracks."

### **2. Show Dashboard (30 detik)**
- **Buka:** http://localhost:8000/simple.html
- **Point out:**
  - Total 1.2M tracks analyzed
  - Average tempo 117.6 BPM
  - Sweet spot: 22% of catalog

### **3. Demo Search Functionality (1 menit)**
**Search Test 1: By Name**
- Ketik: **"shape"**
- Click Search
- **Explain:** "Aplikasi ini bisa search dari database lokal dengan 1.2 juta tracks secara real-time"

**Search Test 2: By Tempo Range**
- Tempo Min: **100**
- Tempo Max: **120**
- Click Search
- **Explain:** "Ini sweet spot range, tracks di sini punya danceability lebih tinggi"

### **4. Show ML Predictions (Optional - kalau ada waktu)**
- Navigate ke tab "ML Predictions"
- **Explain:** "Saya train 4 ML models dengan accuracy 93% untuk predict popularity"

### **5. Closing (30 detik)**
> "Database ini running lokal dengan PostgreSQL. Untuk production, saya sudah deploy ke Railway dengan Vercel frontend dan Firebase untuk caching."

---

## 🛑 **Cara Stop Servers (Setelah Presentasi)**

### **Stop Flask API (Terminal 1):**
- Tekan `Ctrl + C`
- Kalau tidak stop, close terminal

### **Stop Dashboard (Terminal 2):**
- Tekan `Ctrl + C`
- Kalau tidak stop, close terminal

### **Stop All Python Processes (Nuclear Option):**
```powershell
# Kill all Python processes
Get-Process python | Stop-Process -Force
```

---

## 📌 **Quick Start Shortcut**

Untuk lebih cepat, buat file `START_DASHBOARD.bat`:

```bat
@echo off
echo Starting Spotify Dashboard...
echo.

start "Flask API" cmd /k "cd /d d:\Semester 5\BIG DATA\Project && python api/search_api.py"
timeout /t 3 /nobreak

start "Dashboard" cmd /k "cd /d d:\Semester 5\BIG DATA\Project\dashboard && python -m http.server 8000"
timeout /t 2 /nobreak

start http://localhost:8000/simple.html

echo.
echo Dashboard is starting...
echo API: http://localhost:5000
echo Dashboard: http://localhost:8000
echo.
pause
```

**Cara pakai:**
1. Save file di `d:\Semester 5\BIG DATA\Project\START_DASHBOARD.bat`
2. Double click file nya
3. Done! Semua auto-start dan browser auto-open

---

## ✅ **Final Checklist Sebelum Presentasi**

1 hari sebelum:
- [ ] Test full flow: start servers → open dashboard → test search
- [ ] Pastikan PostgreSQL auto-start on boot
- [ ] Bookmark URLs: http://localhost:8000/simple.html
- [ ] Siapkan backup demo video (kalau ada masalah teknis)

1 jam sebelum:
- [ ] Restart laptop (clean start)
- [ ] Close semua aplikasi lain (hemat RAM)
- [ ] Test start dashboard sekali lagi
- [ ] Buka dashboard di browser, test search

Saat presentasi:
- [ ] Flask API running (terminal 1)
- [ ] Dashboard running (terminal 2)
- [ ] Browser sudah buka di http://localhost:8000/simple.html
- [ ] Zoom browser ke 125% (biar audience lihat lebih jelas)

---

## 💡 **Tips Presentasi**

1. **Jangan tutup terminal** - biar dosen lihat ada backend running
2. **Gunakan simple.html** - lebih stabil daripada index.html
3. **Prepare backup plan** - kalau ada masalah, explain architecture dari diagram
4. **Confidence is key** - kalau ada error, bilang "this works in production" 😄

---

## 🎓 **Bonus: Jawaban Pertanyaan Dosen**

**Q: "Data ini darimana?"**
> "Dataset dari Spotify API, saya scrape dan clean 1.2 juta tracks dari tahun 1920-2020"

**Q: "Kenapa pakai PostgreSQL?"**
> "PostgreSQL dipilih karena support indexing untuk fast query, penting untuk dataset 1.2M rows"

**Q: "Deployment nya gimana?"**
> "Local: PostgreSQL. Production: Backend di Railway, Frontend di Vercel, Caching di Firebase. Architecture nya microservices."

**Q: "ML model accuracy nya berapa?"**
> "Popularity prediction: 93.1% R², Hit classifier: 92.9% accuracy. Train pakai Random Forest dan XGBoost."

---

## 📞 **Need Help?**

Kalau ada masalah saat presentasi:
1. Take a deep breath 😌
2. Close browser, restart servers
3. Atau switch ke simple.html
4. Worst case: explain from architecture diagram + backup screenshots

**Good luck! You got this! 🚀**
