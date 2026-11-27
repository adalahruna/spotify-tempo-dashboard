# 📋 VISUAL CHECKLIST - JINACS JOURNAL

**Project:** Intelligent Music Recommendation System  
**Authors:** Sattya Runa, Reyhan Sheva, Aditya Putra, Saifudin Yahya  
**Date:** November 27, 2024

---

## 📊 TABLES (8 Total) - Already in Markdown

All tables are already written in the .md file. Just need to format in Word.

### ✅ TABLE I: Mood Categories and Contexts
**Location:** Section III.C - Step 1  
**Content:** 8 moods (Happy, Exercise, Study, Sad, Relaxed, Party, Driving, Romantic)  
**Status:** ✅ Already written in markdown

### ✅ TABLE II: Intensity Adjustment Factors
**Location:** Section III.C - Step 3  
**Content:** 4 intensity levels (Calm, Moderate, Energetic, Maximum) with modifiers  
**Status:** ✅ Already written in markdown

### ✅ TABLE III: Query Performance Comparison
**Location:** Section V.A.1  
**Content:** Raw Table vs Materialized View (100x improvement!)  
**Data:**
- Average Query Time: 1500ms → 15ms
- Cold Start: 2100ms → 18ms
- Concurrent Users: 15000ms → 150ms
**Status:** ✅ Already written in markdown

### ✅ TABLE IV: Storage Analysis
**Location:** Section V.A.2  
**Content:** Storage sizes (Raw 2.4GB, View 12MB, Indexes 8MB)  
**Status:** ✅ Already written in markdown

### ✅ TABLE V: Recommendation Match Score Distribution
**Location:** Section V.B.1  
**Content:** Score ranges (90-100%, 80-89%, etc.) with percentages  
**Key Stat:** Average 84.7% match score  
**Status:** ✅ Already written in markdown

### ✅ TABLE VI: User Satisfaction Metrics
**Location:** Section V.B.2  
**Content:** 4 metrics rated 1-5 scale  
**Key Stats:**
- Recommendation Relevance: 4.2/5
- Interface Usability: 4.5/5
- Response Time: 4.8/5
**Status:** ✅ Already written in markdown

### ✅ TABLE VII: Tempo Zone Distribution
**Location:** Section V.C  
**Content:** 5 tempo zones with BPM ranges, track counts, danceability  
**Key Insight:** Sweet Spot (100-120 BPM) = 33% of tracks  
**Status:** ✅ Already written in markdown

### ✅ TABLE VIII: Case Study Recommendations
**Location:** Section V.D  
**Content:** Top 5 exercise recommendations with match scores  
**Status:** ✅ Already written in markdown

---

## 🎨 DIAGRAMS (1 Total) - Need to Create

### ❌ Fig. 1: System Architecture Diagram
**Location:** Section III.A (System Architecture)  
**Tool:** draw.io, Lucidchart, PowerPoint, or Figma  
**Filename:** `fig1_architecture.png`

**Components to Include:**
```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
│  Material Design 3 Web Dashboard        │
│  - Overview Stats                       │
│  - Top Tracks Table                     │
│  - Recommendation Interface             │
│  - YouTube Integration                  │
└─────────────┬───────────────────────────┘
              │ HTTP REST API
              ▼
┌─────────────────────────────────────────┐
│          API LAYER (Flask)              │
│  - GET /api/top-tracks                  │
│  - POST /api/recommend                  │
│  - GET /api/artists/search              │
└─────────────┬───────────────────────────┘
              │ psycopg2
              ▼
┌─────────────────────────────────────────┐
│       BUSINESS LOGIC LAYER              │
│  - Gaussian Scoring Algorithm           │
│  - Mood-Activity Mapping (8×32)         │
│  - Intensity Modifiers                  │
│  - Feature Weights (8 features)         │
└─────────────┬───────────────────────────┘
              │ SQL Query
              ▼
┌─────────────────────────────────────────┐
│        DATA LAYER (PostgreSQL)          │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │   top_tracks_view (5K tracks)   │  │
│  │   - Materialized View           │  │
│  │   - Indexed (6 indexes)         │  │
│  │   - 15ms query time             │  │
│  └──────────┬──────────────────────┘  │
│             │ Curation Pipeline        │
│             ▼                           │
│  ┌─────────────────────────────────┐  │
│  │ spotify_tracks_raw (1.2M)       │  │
│  │ - Artist Filtering              │  │
│  │ - Noise Removal                 │  │
│  │ - Deduplication                 │  │
│  │ - Popularity Scoring            │  │
│  └─────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Key Elements:**
- 4 distinct layers with boxes
- Arrows showing data flow
- Component names for each layer
- Key metrics (1.2M → 5K, 15ms)
- Technologies (Flask, PostgreSQL, Material Design 3)

**Style:**
- Clean, professional diagram
- Use colors: Primary green (#006e2d), Secondary (#006c49), Gray backgrounds
- Font: Sans-serif, readable
- Export: PNG, minimum 1200px width

---

## 📸 SCREENSHOTS (8 Total) - Need to Capture

### Setup Commands:
```powershell
# 1. Create folder
cd "d:\Semester 5\BIG DATA\Project"
New-Item -ItemType Directory -Force -Path screenshots

# 2. Start API server
python api/search_api.py

# 3. Open browser
# Main: http://localhost:8000
# Recommendation: http://localhost:8000/recommend.html
```

---

### ❌ Fig. 2: Dashboard Overview
**Location:** Section IV.C.1 (Overview Section)  
**URL:** http://localhost:8000  
**Filename:** `fig2_dashboard_overview.png`

**What to Capture:**
- [ ] Main dashboard heading "Spotify Music Analysis Dashboard"
- [ ] Dataset statistics cards (Total Tracks, Tempo Zones, Artists)
- [ ] Navigation tabs (Overview, Top Tracks, Recommendations)
- [ ] Tempo distribution chart/visualization
- [ ] Sweet spot percentage highlight

**Screenshot Tips:**
- Full page screenshot (use browser extension if needed)
- Include header with logo/title
- Capture at least 1920×1080 resolution
- Ensure all text is readable

**Tool:** Win + Shift + S (Snipping Tool) or Full Page Screenshot extension

---

### ❌ Fig. 3: Top Tracks Table
**Location:** Section IV.C.2 (Top Tracks Section)  
**URL:** http://localhost:8000 → Click "Top Tracks" tab  
**Filename:** `fig3_top_tracks.png`

**What to Capture:**
- [ ] Table header with column names (Track, Artist, Year, Tempo, Energy, Danceability, Zone)
- [ ] At least 10-15 rows of data visible
- [ ] Sort buttons active (show sorting functionality)
- [ ] Filter buttons (Sweet Spot / All Tracks)
- [ ] YouTube play icons (▶️) next to track names
- [ ] Progress bars for Energy and Danceability
- [ ] Tempo zone badges (colored)

**Actions Before Screenshot:**
1. Click "Top Tracks" tab
2. Set sort to "Danceability" (to show interactive feature)
3. Ensure table is fully loaded
4. Scroll to show multiple tracks

---

### ❌ Fig. 4: Tempo Distribution Chart
**Location:** Section V.C (Tempo Zone Analysis)  
**URL:** http://localhost:8000 → Overview section  
**Filename:** `fig4_tempo_distribution.png`

**What to Capture:**
- [ ] Tempo zones visualization (bar chart or card layout)
- [ ] 5 tempo zones: Slow, Moderate, Sweet Spot, Upbeat, Fast
- [ ] Percentages for each zone
- [ ] Track counts
- [ ] Highlight on "Sweet Spot" (100-120 BPM)
- [ ] Color coding for zones

**Screenshot Tips:**
- Zoom in on the tempo distribution section only
- Ensure percentages are clearly visible
- Capture legend if present

---

### ❌ Fig. 5: Recommendation Step 1 - Mood Selection
**Location:** Section III.C (Conversational Flow)  
**URL:** http://localhost:8000/recommend.html  
**Filename:** `fig5_step1_mood.png`

**What to Capture:**
- [ ] Page heading "Smart Recommendations"
- [ ] Step indicator showing "Step 1" active
- [ ] Question: "Lagi pengen dengerin lagu buat apa nih?"
- [ ] All 8 mood cards visible:
  - 😊 Senang-senang (Happy)
  - 💪 Olahraga (Exercise)
  - 📚 Belajar/Kerja (Study)
  - 😢 Galau/Sedih (Sad)
  - 💤 Santai/Tidur (Relaxed)
  - 🎉 Pesta/Nongkrong (Party)
  - 🚗 Nyetir/Perjalanan (Driving)
  - ❤️ Romantis (Romantic)
- [ ] Icons for each mood
- [ ] "Lanjut" button (disabled state)

**Screenshot Tips:**
- Full page or scroll to include all 8 cards
- Capture before selecting any mood

---

### ❌ Fig. 6: Recommendation Step 2 - Activity Selection
**Location:** Section III.C (Conversational Flow)  
**URL:** http://localhost:8000/recommend.html → Select "Olahraga" mood  
**Filename:** `fig6_step2_activity.png`

**What to Capture:**
- [ ] Step indicator showing "Step 2" active
- [ ] Question: "Olahraga apa nih?"
- [ ] 4 activity cards for Exercise mood:
  - 🏃 Lari/Cardio - "Lagu cepat & energik buat lari"
  - 🏋️ Gym/Beban - "Lagu semangat yang stabil"
  - 🧘 Yoga/Stretch - "Lagu tenang & rileks"
  - 🚴 Sepeda - "Lagu sedang & menyenangkan"
- [ ] Icons for each activity
- [ ] Descriptions visible
- [ ] "Kembali" and "Lanjut" buttons

**Actions Before Screenshot:**
1. Select "Olahraga" mood in Step 1
2. Click "Lanjut" to reach Step 2
3. Don't select activity yet (show options)

---

### ❌ Fig. 7: Recommendation Step 3 - Intensity
**Location:** Section III.C (Conversational Flow)  
**URL:** Continue from Step 2 → Select "Lari/Cardio" → Click "Lanjut"  
**Filename:** `fig7_step3_intensity.png`

**What to Capture:**
- [ ] Step indicator showing "Step 3" active
- [ ] Question: "Seberapa intens musiknya?"
- [ ] 4 intensity cards:
  - 🧘 Pelan Banget (Calm) - "Santai & tenang"
  - 🎵 Sedang (Moderate) - "Enak didenger" (selected/highlighted)
  - 🏃 Semangat (Energetic) - "Bikin excited"
  - ⚡ Maksimal (Maximum) - "Full power!"
- [ ] Icons for each intensity
- [ ] One card highlighted (Moderate is default)
- [ ] "Kembali" and "Lanjut" buttons

**Actions Before Screenshot:**
1. Continue from Step 2 (select "Lari/Cardio")
2. Click "Lanjut" to reach Step 3
3. Keep "Moderate" selected (default)

---

### ❌ Fig. 8: Recommendation Step 4 - Artist Filter
**Location:** Section III.C (Conversational Flow)  
**URL:** Continue from Step 3 → Click "Lanjut"  
**Filename:** `fig8_step4_artist.png`

**What to Capture:**
- [ ] Question: "Mau dari artist tertentu? (Optional)"
- [ ] Search input box with placeholder "Ketik nama artist..."
- [ ] Search icon (🔍)
- [ ] Autocomplete dropdown showing results (type "dua" or "weeknd")
- [ ] Example results with track counts:
  - "Dua Lipa - 15 tracks"
  - "The Weeknd - 42 tracks"
- [ ] "Kembali" and "Cari Lagu!" buttons

**Actions Before Screenshot:**
1. Continue from Step 3
2. Click "Lanjut" to reach Step 4
3. Type "dua" or "weeknd" in search box
4. Wait for autocomplete results to appear
5. Don't select artist yet (show dropdown)

**Alternative Screenshot:**
Can also capture with artist selected to show the selected state display

---

### ❌ Fig. 9: Recommendation Results
**Location:** Section V.D (Case Study)  
**URL:** Complete all 4 steps → Click "Cari Lagu!"  
**Filename:** `fig9_results.png`

**What to Capture:**
- [ ] Results heading "Playlist Sempurna Untukmu!"
- [ ] Summary box showing:
  - Selected mood (Olahraga)
  - Activity description (Lagu cepat & energik buat lari)
  - Intensity (Semangat/Maksimal)
  - Artist filter (if selected)
- [ ] Results count (e.g., "20 lagu ditemukan")
- [ ] Results table with columns:
  - # (rank)
  - Track & Artist
  - Tempo (BPM)
  - Match (percentage)
  - Description
- [ ] At least 10 rows visible
- [ ] YouTube play icons (▶️) next to each track
- [ ] Match scores (percentages like 94%, 89%, etc.)
- [ ] "Cari Lagi" button at bottom

**Actions Before Screenshot:**
1. Complete full recommendation flow:
   - Select "Olahraga" mood
   - Select "Lari/Cardio" activity
   - Select "Maksimal" intensity
   - Optionally select "The Weeknd" artist
2. Click "Cari Lagu!"
3. Wait for results to load
4. Scroll to show multiple results

---

## 📁 FILE ORGANIZATION

### Folder Structure:
```
d:\Semester 5\BIG DATA\Project\
├── screenshots/
│   ├── fig1_architecture.png         (Create in draw.io)
│   ├── fig2_dashboard_overview.png   (Screenshot)
│   ├── fig3_top_tracks.png          (Screenshot)
│   ├── fig4_tempo_distribution.png  (Screenshot)
│   ├── fig5_step1_mood.png          (Screenshot)
│   ├── fig6_step2_activity.png      (Screenshot)
│   ├── fig7_step3_intensity.png     (Screenshot)
│   ├── fig8_step4_artist.png        (Screenshot)
│   └── fig9_results.png             (Screenshot)
└── JINACS_Spotify_Music_Recommendation_System.md
```

---

## ✅ QUALITY CHECKLIST

### For All Screenshots:
- [ ] Resolution: Minimum 1920×1080
- [ ] Format: PNG (for quality) or JPEG (for smaller size)
- [ ] No personal information visible
- [ ] All text readable when zoomed out
- [ ] No browser UI clutter (hide bookmarks bar, extensions)
- [ ] Consistent window size across screenshots
- [ ] Clean, professional appearance

### For Architecture Diagram:
- [ ] All 4 layers clearly labeled
- [ ] Arrows showing data flow
- [ ] Key technologies mentioned (Flask, PostgreSQL, etc.)
- [ ] Metrics visible (1.2M → 5K, 15ms)
- [ ] Professional color scheme
- [ ] Legible font sizes
- [ ] Clean, minimalist design

---

## 🎯 PRIORITY ORDER

### High Priority (Must Have):
1. ✅ All 8 tables (already done in markdown)
2. ❌ Fig. 1: Architecture diagram (need to create)
3. ❌ Fig. 9: Results screenshot (shows full system in action)
4. ❌ Fig. 2: Dashboard overview (shows main interface)

### Medium Priority (Should Have):
5. ❌ Fig. 3: Top Tracks table (shows data quality)
6. ❌ Fig. 5-8: All 4 recommendation steps (shows conversational flow)

### Nice to Have:
7. ❌ Fig. 4: Tempo distribution (nice visual, can be replaced with table)

---

## 🛠️ TOOLS NEEDED

### For Screenshots:
- **Windows Snipping Tool**: Win + Shift + S
- **Full Page Screenshot**: Browser extension
  - Chrome: "Full Page Screen Capture"
  - Firefox: "Firefox Screenshots" (built-in)

### For Architecture Diagram:
- **Online (Recommended):**
  - draw.io (diagrams.net) - Free, no account needed
  - Lucidchart - Free tier available
  - Figma - Free tier available

- **Desktop:**
  - Microsoft PowerPoint (use SmartArt or shapes)
  - Visio (if available)
  - Draw.io Desktop

### For Editing (if needed):
- Paint.NET (Windows, free)
- GIMP (cross-platform, free)
- Photoshop (if available)

---

## 📊 QUICK SUMMARY

**Total Visual Elements:** 17
- ✅ Tables: 8 (all done in markdown)
- ❌ Diagrams: 1 (need to create)
- ❌ Screenshots: 8 (need to capture)

**Estimated Time:**
- Architecture diagram: 30-45 minutes
- Screenshots: 30-40 minutes (including setup and navigation)
- **Total: ~1-1.5 hours**

---

## 🚀 NEXT STEPS

1. **Start API Server:**
   ```powershell
   cd "d:\Semester 5\BIG DATA\Project"
   python api/search_api.py
   ```

2. **Create Screenshots Folder:**
   ```powershell
   New-Item -ItemType Directory -Force -Path screenshots
   ```

3. **Take Screenshots:**
   - Open http://localhost:8000
   - Follow checklist above for each figure
   - Save with correct filenames in screenshots/

4. **Create Architecture Diagram:**
   - Use draw.io or similar
   - Follow template in this checklist
   - Export as PNG

5. **Insert into Document:**
   - Convert .md to .docx
   - Insert images at appropriate locations
   - Add captions below each figure

---

**CHECKLIST COMPLETE!** ✅  
Ready to start capturing visuals! 📸🎨

Need help with any specific screenshot or diagram? Let me know! 🚀
