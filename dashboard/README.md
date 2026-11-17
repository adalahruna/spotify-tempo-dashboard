# 🎵 Spotify Tempo Analysis Dashboard

> **Real-time interactive dashboard with intelligent search for visualizing tempo sweet spot analysis**

![Dashboard Preview](https://img.shields.io/badge/Status-Live-success)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.6-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38bdf8)

---

## **📋 Overview**

Modern, responsive web dashboard with **intelligent search** that displays real-time analysis of **1.2M Spotify tracks** (1920-2020) with focus on the **Tempo Sweet Spot hypothesis** (100-120 BPM zone).

### **Key Features:**

✅ **Hybrid data architecture** - Firestore for summary, PostgreSQL for detailed queries  
✅ **Advanced search** - Search by track name, artist, or tempo range  
✅ **4 Summary cards** with key metrics  
✅ **Dot-matrix visualization** for tempo zones  
✅ **Top tracks table** with hit formula songs  
✅ **Modern Tailwind CSS UI** with Inter font  
✅ **Fully responsive** (mobile, tablet, desktop)  
✅ **Smart fallback** - Auto-switches to API if Firestore fails  
✅ **REST API backend** - Flask API for PostgreSQL queries

---

## **🆕 What's New (Latest Update)**

### **🔍 Search Functionality**
- **Live search** tracks by name, artist, or tempo range
- **PostgreSQL-powered** - Avoid Firestore quota limits
- **Pagination support** - Handle large result sets
- **Sweet spot indicator** - Highlights tracks in 100-120 BPM zone

### **🎨 Modern UI Redesign**
- **Tailwind CSS 3.0** - Utility-first styling
- **Inter font** - Smooth, professional typography
- **Gradient accents** - Brand colors (#667eea → #764ba2)
- **Dot-matrix visualization** - Replace Chart.js bar charts

### **⚡ Smart Architecture**
- **Firestore** → Summary stats (1x load per page)
- **PostgreSQL API** → Search & detailed queries (unlimited!)
- **Automatic fallback** → PostgreSQL if Firestore unavailable

---

## **🖥️ Dashboard Components**

### **1. Summary Cards**

| Card | Metric | Description |
|------|--------|-------------|
| 🎵 **Total Tracks** | 1.20M | Total analyzed tracks (1920-2020) |
| ⏱️ **Average Tempo** | 117.63 BPM | Global tempo average |
| ⭐ **Sweet Spot %** | 22.16% | Tracks in 100-120 BPM zone |
| 💃 **Danceability Boost** | +13.37% | Sweet spot advantage vs others |

### **2. Search Bar** 🔍 NEW!

- **Search by:**
  - Track name (e.g., "Get Lucky")
  - Artist name (e.g., "Daft Punk")
  - Tempo range (Min: 100, Max: 120)
  - Combined search (name + tempo filter)
- **Results:** Up to 50 tracks per search
- **Features:**
  - Sweet spot highlighting
  - Real-time search from PostgreSQL
  - No Firestore quota limits!
  - Clear search to restore defaults

### **3. Tempo Zone Visualization**

- **Type:** Dot-matrix visualization
- **Data:** 5 tempo zones (<80, 80-100, 100-120, 120-140, >140 BPM)
- **Highlight:** Sweet spot zone in gradient brand colors
- **Interactive:** Visual representation of zone density
- **Design:** Modern, animated dot stacks

### **4. Top Tracks Table**

- **Data:** Top 10 tracks (default: sweet spot, or search results)
- **Criteria:** 100-120 BPM + High Energy + High Danceability
- **Columns:**
  - Track & Artist (with year)
  - Tempo (BPM badge)
  - Energy score
  - Danceability score
  - Sweet spot indicator
- **Features:**
  - Switchable view (defaults ↔ search results)
  - Responsive table design
  - Color-coded badges

### **5. Key Findings Sidebar**

- **4 Finding cards** with icons and metrics
- **Dynamic data** from analysis results
- **Highlights:**
  - Sweet spot validation (22.16%)
  - Danceability boost (+13.37%)
  - Dataset scale (1.2M tracks)
  - Avg sweet spot tempo (110.35 BPM)

---

## **🚀 Quick Start**

### **Prerequisites**

- Python 3.8+ (for API server)
- PostgreSQL 18.6+ (with data loaded)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Firebase & Tailwind CDN)

### **Installation & Setup**

**Step 1: Start PostgreSQL API Server**

```bash
cd "D:\Semester 5\BIG DATA\Project"
python api/search_api.py

# API will start on http://localhost:5000
# Available endpoints:
#   GET /api/search/tracks       - Search tracks
#   GET /api/search/artists      - Search by artist
#   GET /api/search/tempo-range  - Tempo range query
#   GET /api/stats/summary       - Summary statistics
#   GET /api/health              - Health check
```

**Step 2: Start Dashboard Server**

```bash
cd "D:\Semester 5\BIG DATA\Project\dashboard"
python -m http.server 8000

# Dashboard will be available at:
# http://localhost:8000
```

**Step 3: Open Browser**

Navigate to: `http://localhost:8000`

### **Quick Test**

1. **Check API health:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Test search:**
   ```bash
   curl "http://localhost:5000/api/search/tracks?q=daft&limit=5"
   ```

3. **Open dashboard and try search:**
   - Search: "Get Lucky"
   - Or tempo range: Min=100, Max=120

---

## **🏗️ Architecture**

### **System Design**

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
│                   http://localhost:8000                 │
└──────────────┬────────────────────────┬─────────────────┘
               │                        │
               │ Summary Stats          │ Search Queries
               │ (1x per page load)     │ (on-demand)
               ↓                        ↓
    ┌──────────────────┐      ┌──────────────────┐
    │  Firebase        │      │  Flask REST API  │
    │  Firestore       │      │  localhost:5000  │
    │  (NoSQL)         │      │                  │
    └──────────────────┘      └────────┬─────────┘
                                       │
                                       │ SQL Queries
                                       ↓
                              ┌──────────────────┐
                              │  PostgreSQL 18.6 │
                              │  spotify_music_db│
                              │  1.2M records    │
                              └──────────────────┘
```

### **Data Flow**

1. **Page Load:**
   - Browser fetches summary stats from **Firestore** (fast, cached)
   - Renders summary cards and dot visualization

2. **Search Action:**
   - User enters search query
   - JavaScript sends request to **Flask API**
   - API queries **PostgreSQL** database
   - Results returned as JSON
   - Table updated with search results

3. **Fallback:**
   - If Firestore fails → Auto-switch to PostgreSQL API
   - If API fails → Show error message with instructions

---

## **⚙️ Configuration**

### **Firebase Setup** (Already configured!)

Firebase config is in `app.js` with automatic fallback:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyDs-OeLXYeJv4XOAWTq7MhArI8CAPKo-vE",
  authDomain: "spotify-tempo-analysis.firebaseapp.com",
  projectId: "spotify-tempo-analysis",
  // ... other configs
};

// Smart fallback logic:
// 1. Try Firestore first
// 2. If failed → Use PostgreSQL API
// 3. If both failed → Show error
```

### **PostgreSQL API Configuration**

Located in `api/search_api.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb'  # Change if needed
}
```

### **API Endpoints**

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/search/tracks` | GET | `q`, `tempo_min`, `tempo_max`, `limit` | Search tracks |
| `/api/search/artists` | GET | `artist`, `limit` | Search by artist |
| `/api/search/tempo-range` | GET | `min`, `max`, `offset`, `limit` | Tempo range with pagination |
| `/api/stats/summary` | GET | - | Summary statistics |
| `/api/health` | GET | - | Health check |

**Example Search Request:**

```bash
# Search by name
curl "http://localhost:5000/api/search/tracks?q=lucky&limit=10"

# Search by tempo range
curl "http://localhost:5000/api/search/tracks?tempo_min=100&tempo_max=120&limit=20"

# Combined search
curl "http://localhost:5000/api/search/tracks?q=daft&tempo_min=100&tempo_max=120"
```

### **CORS Configuration**

API enables CORS for local development:

```python
from flask_cors import CORS
CORS(app)  # Allows requests from http://localhost:8000
```

For production, restrict origins:

```python
CORS(app, origins=["https://yourdomain.com"])
```

---

## **📂 File Structure**

```
dashboard/
├── index.html              # Main HTML structure (Tailwind CSS)
├── app.js                  # Firebase + API logic + rendering
└── README.md               # This file

api/
└── search_api.py           # Flask REST API for PostgreSQL queries

scripts/
├── sync_postgres_to_firestore.py   # Sync PostgreSQL → Firestore
└── test_firestore_data.py          # Test Firestore connection

docs/
├── ARCHITECTURE.md         # System architecture
├── METHODOLOGY.md          # Research methodology
├── KEY_FINDINGS.md         # Analysis results
└── VALIDATION_REPORT_*.txt # Hypothesis validation reports
```

### **File Descriptions:**

**`index.html`** (Tailwind CSS)
- Modern card-based responsive layout
- Inter font for smooth typography
- Search bar with tempo range filters
- Dot-matrix tempo visualization
- Top tracks table with badges
- Key findings sidebar

**`app.js`** (JavaScript)
- Firebase Firestore initialization
- Smart fallback to PostgreSQL API
- Search functionality with fetch API
- Dot-matrix rendering (replaces Chart.js)
- Real-time data updates
- Error handling & loading states

**`api/search_api.py`** (Flask)
- RESTful API endpoints
- PostgreSQL connection pooling
- CORS support for local dev
- Pagination support
- Input validation & error handling
- Health check endpoint

---

## **🎨 Design System**

### **Color Palette** (Tailwind CSS)

```css
Brand Primary:      #667eea (Indigo)
Brand Secondary:    #764ba2 (Purple)
Gradient:           from-brand-500 to-brand-600
Background:         #f4f6fc (Light slate)
Cards:              White with soft shadow
Text Primary:       Slate-900
Text Secondary:     Slate-500
Success:            Emerald-600
Warning:            Amber-600
```

### **Typography** (Inter Font)

- **Font Family:** Inter, -apple-system, BlinkMacSystemFont, Segoe UI
- **Font Smoothing:** Antialiased for crisp rendering
- **Headings:** 
  - H1: 3xl (30px), extrabold
  - H2: lg (18px), bold
  - H3: base (16px), bold
- **Body:** sm (14px), medium
- **Small:** xs (12px), for labels and subtitles
- **Letter Spacing:** -0.011em for improved readability

### **Spacing** (Tailwind Scale)

- Card padding: p-6 (24px), p-7 (28px)
- Grid gap: gap-6 (24px)
- Border radius: rounded-2xl (16px), rounded-3xl (24px)
- Container max-width: max-w-[1600px]

### **Components**

**Summary Cards:**
```html
<div class="bg-white rounded-2xl p-5 border border-slate-100 shadow-soft">
  <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Label</span>
  <h3 class="text-3xl font-extrabold text-slate-900 mt-2">Value</h3>
  <p class="text-xs text-slate-400 mt-2">Description</p>
</div>
```

**Badges:**
```html
<!-- Tempo Badge -->
<span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-brand-50 text-brand-700 font-bold text-xs border border-brand-200">
  116.0 BPM
</span>

<!-- Sweet Spot Badge -->
<span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 font-bold text-xs border border-emerald-200">
  ✓ Sweet Spot
</span>
```

---

## **📊 Data Flow**

```mermaid
graph TB
    A[Browser: localhost:8000] -->|Initial Load| B[Firestore]
    A -->|Search Query| C[Flask API: localhost:5000]
    B -->|Summary Stats| D[Dashboard UI]
    C -->|SQL Query| E[PostgreSQL]
    E -->|Results JSON| C
    C -->|Search Results| D
    
    F[Python Script] -->|Sync Data| B
    E -->|Source Data| F
    
    style A fill:#667eea,color:#fff
    style B fill:#FFA000,color:#fff
    style C fill:#2196F3,color:#fff
    style E fill:#336791,color:#fff
```

### **Data Sources:**

1. **Firestore Collections** (For dashboard summary):

1. **`summary/global_stats`** → Summary cards
2. **`tempo_zones/{zone_id}`** → Tempo & Danceability charts
3. **`decade_trends/{decade}`** → Decade trends chart
4. **`top_tracks/sweet_spot_top_100`** → Top tracks table
5. **`audio_features_comparison/{category}`** → Danceability calculation

---

## **🔧 Customization**

### **Change Colors**

Edit `index.html` CSS section:

```css
/* Main gradient background (line 31) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Card accent (line 121) */
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
```

### **Add More Charts**

1. Add canvas in HTML:
```html
<div class="chart-card">
    <div class="chart-title">My New Chart</div>
    <div class="chart-container">
        <canvas id="myNewChart"></canvas>
    </div>
</div>
```

2. Create chart in `app.js`:
```javascript
function renderMyNewChart(data) {
    const ctx = document.getElementById('myNewChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: { /* ... */ },
        options: { /* ... */ }
    });
}
```

### **Modify Table Columns**

Edit `renderTopTracksTable()` function in `app.js`:

```javascript
row.innerHTML = `
    <td>${index + 1}</td>
    <td>${track.name}</td>
    <td>${track.artists}</td>
    <!-- Add more columns here -->
`;
```

---

## **📱 Responsive Breakpoints**

```css
Desktop:  > 768px  (Grid: 2-4 columns)
Tablet:   ≤ 768px  (Grid: 1-2 columns)
Mobile:   ≤ 768px  (Grid: 1 column, stacked)
```

Charts automatically resize to fit screen width.

---

## **🐛 Troubleshooting**

### **Problem: Dashboard blank / no data**

**Solution:**
1. **Check API server running:**
   ```bash
   curl http://localhost:5000/api/health
   # Should return: {"status": "healthy", "database": "connected"}
   ```

2. **Check browser console (F12):**
   - Look for network errors
   - Check if Firestore or API requests failed

3. **Start both servers:**
   ```bash
   # Terminal 1: API
   cd "D:\Semester 5\BIG DATA\Project"
   python api/search_api.py
   
   # Terminal 2: Dashboard
   cd "D:\Semester 5\BIG DATA\Project\dashboard"
   python -m http.server 8000
   ```

4. **Verify PostgreSQL is running:**
   ```bash
   psql -U postgres -d spotify_music_db -c "SELECT COUNT(*) FROM spotify_tracks_raw;"
   ```

### **Problem: Search not working**

**Solution:**
1. **Check API endpoint:**
   ```bash
   curl "http://localhost:5000/api/search/tracks?q=test&limit=5"
   ```

2. **Verify CORS enabled** in `api/search_api.py`:
   ```python
   from flask_cors import CORS
   CORS(app)  # This line must be present
   ```

3. **Check browser console** for:
   - CORS errors
   - Network request failures
   - JavaScript errors

### **Problem: "Permission denied" or CORS error**

**Solution:**
- **DON'T** open `index.html` directly (file:// protocol)
- **DO** use HTTP server (Python or Live Server)
- For Firestore: Update security rules to allow read access

### **Problem: Old data showing**

**Solution:**
```bash
# 1. Re-sync data to Firestore
python scripts/sync_postgres_to_firestore.py

# 2. Clear browser cache
# Chrome: Ctrl+Shift+Del → Clear cached images and files

# 3. Hard refresh
# Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
```

### **Problem: API returns 500 error**

**Solution:**
1. **Check PostgreSQL credentials** in `api/search_api.py`
2. **Check PostgreSQL is running:**
   ```bash
   pg_ctl status -D "C:\Program Files\PostgreSQL\18\data"
   ```
3. **Check API logs** in terminal for detailed error
4. **Verify table exists:**
   ```sql
   \dt spotify_tracks_raw
   ```

### **Problem: Search returns no results**

**Solution:**
- Search is case-insensitive partial match
- Try shorter search terms (e.g., "daft" not "Daft Punk - Get Lucky")
- Check if data loaded in PostgreSQL:
  ```sql
  SELECT COUNT(*) FROM spotify_tracks_raw WHERE LOWER(name) LIKE '%daft%';
  ```

---

## **🚀 Deployment**

### **Deploy to Firebase Hosting**

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize hosting
cd "D:\Semester 5\BIG DATA\Project\dashboard"
firebase init hosting

# Select project: spotify-tempo-analysis
# Public directory: . (current folder)
# Single page app: No
# Overwrite index.html: No

# Deploy
firebase deploy --only hosting

# Dashboard live at:
# https://spotify-tempo-analysis.web.app
```

### **Deploy to Netlify**

1. Go to https://netlify.com
2. Drag & drop `dashboard` folder
3. Done! Free hosting + custom domain

### **Deploy to Vercel**

```bash
npm i -g vercel
cd "D:\Semester 5\BIG DATA\Project\dashboard"
vercel
```

---

## **🔐 Security Considerations**

### **Current Setup (Development)**

```javascript
// Firestore rules: Public read access
allow read: if true;   // ⚠️ Anyone can read
allow write: if false; // ✅ Only backend can write
```

**⚠️ Suitable for:** Public dashboards, research projects, demos

### **Production Setup (Recommended)**

```javascript
// Add authentication
allow read: if request.auth != null;  // Requires login
allow write: if false;
```

Or use Firebase Anonymous Auth:

```javascript
// In app.js (before loadDashboardData)
firebase.auth().signInAnonymously();
```

---

## **📈 Performance**

### **Metrics:**

- **Initial Load:** ~2-3 seconds (includes Firebase SDK + Chart.js)
- **Data Fetch:** ~500ms-1s (Firestore query)
- **Chart Render:** ~200-300ms per chart
- **Total Time to Interactive:** ~3-4 seconds

### **Optimization Tips:**

1. **Enable Firestore persistence:**
```javascript
firebase.firestore().enablePersistence();
```

2. **Lazy load charts:**
Only render charts when scrolled into view

3. **Use CDN caching:**
Firebase SDKs cached by CDN (CloudFlare)

4. **Minimize redraws:**
Charts only created once, not on every data update

---

## **🔄 Data Update Workflow**

```bash
# 1. Update PostgreSQL data
psql -U postgres -d spotify_music_db
# ... run updates ...

# 2. Sync to Firestore
python scripts/sync_postgres_to_firestore.py

# 3. Dashboard auto-updates!
# Refresh browser to see new data
```

**Note:** Dashboard reads from Firestore (NoSQL), not directly from PostgreSQL.

---

## **📚 Technologies Used**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **HTML5** | - | Structure & semantics |
| **Tailwind CSS** | 3.0 | Utility-first styling |
| **JavaScript (ES6+)** | - | Logic & interactivity |
| **Firebase Firestore** | v10 compat | Summary data cache |
| **Flask** | 3.1.3 | REST API backend |
| **PostgreSQL** | 18.6 | Primary database |
| **psycopg2** | 2.9.13 | PostgreSQL adapter |
| **Flask-CORS** | 6.0.5 | Cross-origin support |
| **Inter Font** | Variable | Typography |

### **Why This Tech Stack?**

✅ **Tailwind CSS** - Rapid UI development, consistent design  
✅ **Flask** - Lightweight, easy PostgreSQL integration  
✅ **Hybrid DB** - Firestore for speed, PostgreSQL for flexibility  
✅ **No Chart.js** - Custom dot-matrix for better performance  
✅ **REST API** - Scalable, testable, reusable

---

## **🎓 Educational Value**

This dashboard demonstrates:

✅ **JAMstack Architecture** (JavaScript, APIs, Markup)  
✅ **Serverless Design** (No backend server needed)  
✅ **Real-time Data** (Firestore real-time sync)  
✅ **Modern CSS** (Grid, Flexbox, Gradients, Animations)  
✅ **Data Visualization** (Chart.js best practices)  
✅ **Responsive Design** (Mobile-first approach)  
✅ **Clean Code** (Separation of concerns, DRY principle)

---

## **📝 API Reference**

### **Firestore Collections**

**`summary/global_stats`**
```javascript
{
  total_tracks: Number,
  avg_tempo: Number,
  sweet_spot_percentage: Number,
  sweet_spot_count: Number,
  min_tempo: Number,
  max_tempo: Number,
  earliest_year: Number,
  latest_year: Number,
  last_updated: Timestamp
}
```

**`tempo_zones/{zone_id}`**
```javascript
{
  zone_id: String,           // "100_120", "120_140", etc.
  zone_name: String,         // "100-120 BPM (Sweet Spot)"
  count: Number,
  percentage: Number,
  avg_energy: Number,
  avg_danceability: Number,
  avg_valence: Number,
  last_updated: Timestamp
}
```

**`decade_trends/{decade}`**
```javascript
{
  decade: Number,            // 1920, 1930, ..., 2020
  total_tracks: Number,
  sweet_spot_tracks: Number,
  sweet_spot_pct: Number,
  avg_energy: Number,
  avg_tempo: Number,
  last_updated: Timestamp
}
```

**`top_tracks/sweet_spot_top_100`**
```javascript
{
  count: Number,
  criteria: String,
  tracks: [
    {
      name: String,
      artists: String,
      year: Number,
      tempo: Number,
      energy: Number,
      danceability: Number,
      valence: Number,
      hit_score: Number
    }
  ],
  last_updated: Timestamp
}
```

---

## **🤝 Contributing**

Want to improve the dashboard?

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

**Ideas for contributions:**
- Add more chart types (Pie, Radar, Heatmap)
- Implement filters (by decade, tempo range)
- Add export features (PNG, CSV)
- Dark mode toggle
- Animation improvements
- Real-time updates (without refresh)

---

## **📄 License**

This dashboard is part of a **Big Data thesis project** for academic purposes.

**Dataset:** Spotify Tracks (1920-2020)  
**Analysis:** Tempo Sweet Spot Hypothesis  
**Institution:** [Your University Name]  
**Year:** 2026

---

## **👤 Author**

**Big Data Thesis Project**  
Semester 5 - 2026

For questions or collaboration:
- GitHub: [Your GitHub]
- Email: [Your Email]

---

## **🙏 Acknowledgments**

- **Spotify** - For providing public API data
- **Firebase** - For free cloud infrastructure
- **Chart.js** - For excellent charting library
- **Design Inspiration** - Modern SaaS dashboards

---

## **📞 Support**

Having issues? Check these resources:

1. **SETUP.md** - Detailed setup instructions
2. **Browser Console (F12)** - Check for error messages
3. **Firebase Console** - Verify data exists in Firestore
4. **Chart.js Docs** - https://www.chartjs.org/docs/
5. **Firebase Docs** - https://firebase.google.com/docs/web/setup

---

## **🔗 Quick Links**

- [Firebase Console](https://console.firebase.google.com/project/spotify-tempo-analysis)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Project Main README](../README.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Key Findings](../docs/KEY_FINDINGS.md)

---

## **📊 Dashboard Statistics**

- **Total Code Lines:** ~500 (HTML + JS + CSS)
- **Load Time:** ~3 seconds (initial)
- **Bundle Size:** 0 KB (all assets from CDN)
- **Browser Support:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Accessibility:** WCAG 2.1 Level A (basic compliance)

---

## **✨ Features Roadmap**

### **v2.0 (Current)** ✅
- ✅ Tailwind CSS modern UI
- ✅ Search by track/artist/tempo
- ✅ PostgreSQL API integration
- ✅ Smart fallback architecture
- ✅ Dot-matrix visualization
- ✅ Responsive design
- ✅ Inter font typography

### **v2.1 (Planned)**
- ⏳ Dark mode toggle
- ⏳ Export search results to CSV
- ⏳ Advanced filters (year range, energy, valence)
- ⏳ Pagination for large result sets
- ⏳ Artist statistics page

### **v3.0 (Future)**
- ⏳ Real-time updates (WebSocket)
- ⏳ User authentication
- ⏳ Save favorite searches
- ⏳ Share search results
- ⏳ Compare multiple artists
- ⏳ API rate limiting
- ⏳ Caching layer (Redis)

---

## **🔗 Quick Links**

- [Flask API Source](../api/search_api.py)
- [PostgreSQL Sync Script](../scripts/sync_postgres_to_firestore.py)
- [Project Main README](../README.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Key Findings](../docs/KEY_FINDINGS.md)
- [Validation Report](../docs/VALIDATION_REPORT_*.txt)

---

## **📊 Dashboard Statistics**

- **Total Code Lines:** ~800 (HTML + JS + Python API)
- **Initial Load Time:** ~2-3 seconds
- **Search Response Time:** ~200-500ms (PostgreSQL)
- **API Endpoints:** 5 active endpoints
- **Supported Browsers:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Responsive:** ✅ Yes (Tailwind breakpoints)
- **PWA Ready:** ⏳ Planned for v3.0

---

**Built with ❤️ for Big Data research - Semester 5, 2026**

🎵 **100-120 BPM: The Universal Sweet Spot** 🎵

---

## **📞 Need Help?**

1. Check this README thoroughly
2. Look at error messages in browser console (F12)
3. Verify both servers are running
4. Test API endpoints with curl
5. Check PostgreSQL connection

**Common Commands:**

```bash
# Start API server
python api/search_api.py

# Start dashboard server
python -m http.server 8000

# Test API health
curl http://localhost:5000/api/health

# Test search
curl "http://localhost:5000/api/search/tracks?q=test&limit=5"

# Check PostgreSQL
psql -U postgres -d spotify_music_db -c "SELECT COUNT(*) FROM spotify_tracks_raw;"
```
