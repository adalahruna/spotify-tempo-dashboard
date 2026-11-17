# 📝 Dashboard Changelog

All notable changes to the Spotify Tempo Analysis Dashboard.

---

## **[v2.0.0]** - 2026-11-13

### 🎉 Major Update: Search Feature + Modern UI Redesign

### ✨ Added
- **Search functionality** - Search tracks by name, artist, or tempo range
- **Flask REST API** - PostgreSQL-powered backend (`api/search_api.py`)
- **5 API endpoints** for flexible data queries
- **Smart fallback architecture** - Auto-switches between Firestore and PostgreSQL
- **Tailwind CSS 3.0** - Complete UI redesign
- **Inter font** - Modern, smooth typography with antialiasing
- **Dot-matrix visualization** - Custom tempo zone visualization
- **Key findings sidebar** - Dynamic cards with research highlights
- **Loading states** - Better UX with loading indicators
- **Error handling** - User-friendly error messages

### 🎨 Changed
- **UI Framework:** Vanilla CSS → Tailwind CSS 3.0
- **Charts:** Chart.js bar charts → Custom dot-matrix visualization
- **Font:** Plus Jakarta Sans → Inter (variable weight)
- **Color scheme:** Updated to softer slate backgrounds
- **Card design:** Rounded-2xl borders, soft shadows
- **Table styling:** Modern badges and color-coded indicators

### 🔧 Technical Improvements
- **Hybrid architecture:** Firestore (summary) + PostgreSQL (search)
- **API caching:** Reduced Firestore quota usage
- **CORS support:** Flask-CORS for cross-origin requests
- **Input validation:** Server-side validation for all queries
- **Pagination support:** Handle large result sets efficiently
- **Health check endpoint:** Monitor API status

### 📦 Dependencies
- Added: `flask==3.1.3`
- Added: `flask-cors==6.0.5`
- Added: `psycopg2-binary==2.9.13`
- Removed: `chart.js` dependency

### 🐛 Fixed
- Fixed Firestore connection failures with fallback mechanism
- Fixed CORS issues with proper headers
- Fixed mobile responsiveness for search bar
- Fixed table overflow on small screens

### 📝 Documentation
- Updated README.md with search instructions
- Added API endpoint documentation
- Added troubleshooting guide for common errors
- Created CHANGELOG.md

---

## **[v1.0.0]** - 2026-11-10

### 🎉 Initial Release

### ✨ Features
- **Summary cards** - Total tracks, avg tempo, sweet spot %, danceability boost
- **Tempo distribution chart** - Bar chart with 5 tempo zones
- **Danceability comparison** - Horizontal bar chart
- **Decade trends chart** - Line chart (1920-2020)
- **Top tracks table** - Hit formula tracks (100-120 BPM)
- **Firestore integration** - Real-time data from Firebase
- **Responsive design** - Mobile, tablet, desktop support

### 🎨 Design
- Purple gradient background (#667eea → #764ba2)
- Chart.js for data visualization
- Plus Jakarta Sans font
- Card-based layout

### 📦 Technologies
- HTML5 + CSS3 + JavaScript (ES6+)
- Firebase Firestore v10 (compat)
- Chart.js 4.4.0
- Python HTTP server for local development

---

## **Version Naming Convention**

- **Major (v2.x.x):** Breaking changes, major features
- **Minor (vx.1.x):** New features, non-breaking
- **Patch (vx.x.1):** Bug fixes, small improvements

---

## **Upgrade Guide: v1.0 → v2.0**

### What Changed:
1. **UI completely redesigned** - Tailwind CSS instead of vanilla CSS
2. **Search added** - Requires Flask API server running
3. **Charts removed** - Dot-matrix visualization instead

### Migration Steps:

**1. Install Python dependencies:**
```bash
pip install flask flask-cors psycopg2-binary
```

**2. Start Flask API:**
```bash
cd "D:\Semester 5\BIG DATA\Project"
python api/search_api.py
```

**3. Update PostgreSQL config (if needed):**
Edit `api/search_api.py` line 18-24 with your DB credentials.

**4. No code changes needed for existing Firestore data!**
Dashboard is backward compatible.

### Breaking Changes:
- ❌ Chart.js no longer used (removed from HTML)
- ❌ Custom CSS classes replaced with Tailwind utilities
- ✅ Firestore collections structure unchanged
- ✅ All existing features still work

---

## **Roadmap**

### v2.1 (Next Release)
- [ ] Dark mode toggle
- [ ] Export search results to CSV
- [ ] Advanced filters (year, energy, valence)
- [ ] Pagination for search results

### v2.2
- [ ] Artist comparison tool
- [ ] Save favorite searches
- [ ] Share search results (unique URL)

### v3.0 (Major)
- [ ] Real-time updates (WebSocket)
- [ ] User authentication (Firebase Auth)
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] PWA support

---

## **Contributors**

- **Big Data Thesis Team** - Semester 5, 2026
- **Dataset:** Spotify Tracks (Kaggle)
- **Analysis:** 1.2M tracks, 1920-2020

---

**Questions or suggestions?** Open an issue or submit a PR!

🎵 Happy analyzing! 🎵
