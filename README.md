# 🎵 Spotify Tempo Sweet Spot Analysis

## **Big Data Thesis Project**

> *"Analisis Zona Tempo Universal dalam Sistem Prediksi Popularitas Musik Berbasis Big Data"*

[![Dataset](https://img.shields.io/badge/Dataset-1.2M%20Tracks-blue)](.)
[![Time Range](https://img.shields.io/badge/Time%20Range-1920--2020-green)](.)
[![Tech Stack](https://img.shields.io/badge/Tech-PostgreSQL%20%7C%20Firebase%20%7C%20Python-orange)](.)
[![Deploy](https://img.shields.io/badge/Deploy-Railway%20Ready-purple)](DEPLOYMENT.md)

---

## **🚀 Quick Links**

- 📖 [Full Deployment Guide](DEPLOYMENT.md)
- ⚡ [5-Minute Quick Deploy](QUICK_DEPLOY.md)
- 🧪 [Test Production Locally](TEST_PRODUCTION.md)
- 🤖 [ML Models Documentation](ML_MODELS.md) ⭐ **NEW: AI Predictions**
- 🎨 [Live Dashboard Demo](#) *(coming soon)*

---

## **📋 Project Overview**

This research investigates the **"Tempo Sweet Spot" hypothesis** - the theory that music within the 100-120 BPM range exhibits superior audio characteristics and represents a universal human preference zone.

### **Key Question:**
> *"Does the 100-120 BPM tempo range demonstrate consistently higher danceability, energy, and presence across 100 years of music?"*

---

## **🎯 Main Findings**

### **✅ Hypothesis CONFIRMED**

| Finding | Result |
|---------|--------|
| **Sweet Spot Danceability** | **+13.4% higher** than other tempos ⭐ |
| **Temporal Consistency** | Stable ~22% across **100 years** (1920-2020) |
| **Global Average Tempo** | **117.63 BPM** (WITHIN sweet spot!) |
| **Track Count** | 267,027 tracks (22.18% of 1.2M dataset) |

**Conclusion:** Sweet spot is a **universal baseline preference zone**, not a dominant zone.

---

## **📊 Dataset**

- **Source:** Spotify Tracks Dataset (Kaggle / Spotify API)
- **Size:** 1,204,025 tracks
- **Features:** 24 audio features + metadata
- **Time Range:** 1920-2020 (100 years)
- **Format:** CSV (~500MB)

### **Key Features:**
- `tempo` - BPM (0-250)
- `energy` - Intensity (0-1)
- `danceability` - Dance potential (0-1)
- `valence` - Positivity (0-1)
- `acousticness`, `instrumentalness`, `loudness`, etc.

---

## **🏗️ Architecture**

### **Hybrid Database Design (SQL + NoSQL)**

```
CSV (1.2M tracks)
    ↓
PostgreSQL (SQL Layer)
    • Heavy computation
    • Aggregations
    • Statistical analysis
    ↓
Firebase Firestore (NoSQL Layer)
    • Pre-computed results (~22 docs)
    • Fast read access
    • Real-time sync
    ↓
Python Analysis & Visualization
    • matplotlib + seaborn
    • 5 professional charts
```

**Why Hybrid?**
- PostgreSQL = Heavy lifting (compute)
- Firestore = Fast delivery (read)
- Best of both worlds for Big Data thesis ✅

---

## **🔧 Tech Stack**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Database (SQL)** | PostgreSQL 18.6 | Raw data + heavy queries |
| **Database (NoSQL)** | Firebase Firestore | Aggregated results |
| **Backend** | Python 3.14 | Analysis & scripting |
| **Data Processing** | pandas 3.0+ | Data manipulation |
| **Visualization** | matplotlib, seaborn | Chart generation |
| **Sync** | firebase-admin SDK | PostgreSQL → Firestore |

---

## **📁 Project Structure**

```
D:\Semester 5\BIG DATA\Project/
├── data/
│   └── raw/
│       └── tracks_features.csv (1.2M tracks)
│
├── scripts/
│   ├── load_csv_direct.py           # CSV → PostgreSQL
│   ├── sync_postgres_to_firestore.py # PostgreSQL → Firestore
│   ├── visualize_analysis.py         # Generate charts
│   └── test_firebase_connection.py   # Test Firestore
│
├── visualizations/ ⭐
│   ├── 01_tempo_distribution.png
│   ├── 02_danceability_comparison.png
│   ├── 03_decade_trends.png
│   ├── 04_audio_features_radar.png
│   └── 05_summary_stats.png
│
├── docs/ ⭐
│   ├── ARCHITECTURE.md        # System architecture
│   ├── METHODOLOGY.md         # Research methodology
│   ├── KEY_FINDINGS.md        # Analysis results
│   └── README.md              # This file
│
├── firebase-credentials.json  # (DO NOT COMMIT!)
└── .gitignore
```

---

## **🚀 Quick Start**

### **Prerequisites**

```bash
# Install PostgreSQL 18.6
# Download from: https://www.postgresql.org/download/

# Install Python 3.14
# Download from: https://www.python.org/downloads/

# Install required packages
pip install pandas firebase-admin matplotlib seaborn
```

### **Step 1: Load Data to PostgreSQL**

```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# Create database
CREATE DATABASE spotify_music_db;

# Run loading script
python scripts/load_csv_direct.py
```

### **Step 2: Setup Firebase**

1. Create Firebase project: https://console.firebase.google.com/
2. Enable Firestore Database (test mode)
3. Generate service account key → Save as `firebase-credentials.json`
4. Test connection:

```bash
python scripts/test_firebase_connection.py
```

### **Step 3: Sync Data**

```bash
# Sync aggregated results to Firestore
python scripts/sync_postgres_to_firestore.py
```

### **Step 4: Generate Visualizations**

```bash
# Create charts
python scripts/visualize_analysis.py

# Output: visualizations/*.png (5 charts)
```

---

## **📊 Key Visualizations**

### **1. Tempo Distribution**
Bar chart showing distribution across 5 tempo zones.

**Finding:** Sweet spot (100-120 BPM) = 22.18% (2nd highest)

### **2. Danceability Comparison**
Bar chart comparing sweet spot vs other tempos.

**Finding:** +13.4% higher danceability in sweet spot!

### **3. Decade Trends**
Line chart showing sweet spot % from 1920-2020.

**Finding:** Remarkably consistent ~22-24% across 70 years!

### **4. Audio Features Radar**
Polar chart comparing multiple features.

**Finding:** Sweet spot superior across multiple dimensions.

### **5. Summary Statistics**
Infographic with key metrics.

**Finding:** Average tempo = 117.63 BPM (within sweet spot!)

---

## **🔍 SQL Queries Examples**

### **Tempo Distribution**

```sql
SELECT 
    CASE 
        WHEN tempo < 80 THEN '<80 BPM'
        WHEN tempo < 100 THEN '80-100 BPM'
        WHEN tempo <= 120 THEN '100-120 BPM (Sweet Spot)'
        WHEN tempo <= 140 THEN '120-140 BPM'
        ELSE '>140 BPM'
    END as tempo_zone,
    COUNT(*) as count,
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER())::numeric, 2) as percentage
FROM spotify_tracks_raw
WHERE tempo IS NOT NULL
GROUP BY tempo_zone
ORDER BY count DESC;
```

### **Sweet Spot Analysis**

```sql
SELECT 
    CASE 
        WHEN tempo BETWEEN 100 AND 120 THEN 'Sweet Spot'
        ELSE 'Other'
    END as category,
    COUNT(*) as total_tracks,
    ROUND(AVG(energy)::numeric, 3) as avg_energy,
    ROUND(AVG(danceability)::numeric, 3) as avg_danceability,
    ROUND(AVG(valence)::numeric, 3) as avg_valence
FROM spotify_tracks_raw
WHERE tempo IS NOT NULL
GROUP BY category;
```

### **Top Hit Formula Tracks**

```sql
SELECT 
    name, 
    artists, 
    ROUND(tempo::numeric, 2) as tempo,
    ROUND(energy::numeric, 3) as energy,
    ROUND(danceability::numeric, 3) as danceability,
    ROUND(((energy + danceability + valence) / 3)::numeric, 3) as hit_score
FROM spotify_tracks_raw
WHERE tempo BETWEEN 100 AND 120
  AND energy > 0.7
  AND danceability > 0.6
ORDER BY hit_score DESC
LIMIT 20;
```

---

## **🔥 Firestore Collections**

```
firestore/
├── summary/
│   └── global_stats
│       • total_tracks: 1,204,025
│       • avg_tempo: 117.63
│       • sweet_spot_percentage: 22.18
│
├── tempo_zones/ (5 docs)
│   ├── 100_120 (Sweet Spot) ⭐
│   ├── 120_140
│   ├── 80_100
│   ├── less_80
│   └── above_140
│
├── decade_trends/ (14 docs)
│   ├── 1900, 1910, ..., 2020
│
├── top_tracks/
│   └── sweet_spot_top_100
│
└── audio_features_comparison/
    ├── sweet_spot
    └── other_tempo
```

**Total:** ~22 documents (lightweight!)

---

## **📚 Documentation**

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture & design decisions
- **[METHODOLOGY.md](docs/METHODOLOGY.md)** - Research methodology chapter
- **[KEY_FINDINGS.md](docs/KEY_FINDINGS.md)** - Analysis results & insights

---

## **🎓 Academic Context**

### **Thesis Title**
*"Analisis Zona Tempo Universal dalam Sistem Prediksi Popularitas Musik Berbasis Big Data"*

### **Research Questions**
1. Does 100-120 BPM show superior audio characteristics?
2. Is sweet spot consistent across 100 years?
3. Can sweet spot predict "hit potential"?

### **Methodology**
- Quantitative exploratory analysis
- Big Data techniques (SQL + NoSQL)
- 1.2M track sample (100 years)
- Statistical validation

### **Contribution**
- Large-scale validation of tempo sweet spot theory
- Hybrid database architecture for Big Data research
- Practical guidelines for music production

---

## **⚠️ Limitations**

1. **Genre Bias:** Dataset may over-represent certain genres
2. **Spotify Bias:** Only tracks available on Spotify
3. **No Direct Popularity:** Using danceability as proxy
4. **Western Music Bias:** Limited non-Western representation
5. **Correlation ≠ Causation:** Cannot prove causality

---

## **🚀 Future Work**

- [ ] Genre-specific analysis
- [ ] Integration with Billboard/Spotify Charts (actual popularity)
- [ ] Cultural comparison (Western vs Non-Western)
- [ ] Machine learning predictive model
- [ ] Real-time dashboard (React/Vue web app)
- [ ] Extended sweet spot investigation (100-140 BPM)

---

## **📄 License**

This project is for **academic purposes only**.

Dataset: Spotify Tracks Dataset (Kaggle / Public API)  
Code: Available for research verification

---

## **👤 Author**

**Big Data Thesis Project**  
Semester 5 - 2026

---

## **🙏 Acknowledgments**

- **Spotify** - For providing public API data
- **Kaggle** - Dataset hosting
- **PostgreSQL** - Excellent open-source database
- **Firebase** - Cloud infrastructure
- **Python Community** - Amazing data science tools

---

## **📞 Contact**

For questions or collaboration:
- Open an issue on GitHub
- Email: [your-email@domain.com]

---

## **⭐ Star this repo if you find it useful!**

```
  _____                         _____                _     _____             _   
 |_   _|                       / ____|              | |   / ____|           | |  
   | | ___ _ __ ___  _ __   __| (___ _ __   ___ ___| |_ | (___  _ __   ___ | |_ 
   | |/ _ \ '_ ` _ \| '_ \ / _ \\___ \ '_ \ / _ \/ __| __|\___ \| '_ \ / _ \| __|
   | |  __/ | | | | | |_) | (_) |___) | |_) | (_) \__ \ |_ ____) | |_) | (_) | |_ 
   |_|\___|_| |_| |_| .__/ \___/_____/ .__/ \___/|___/\__|_____/| .__/ \___/ \__|
                    | |               | |                        | |              
                    |_|               |_|                        |_|              
```

**100-120 BPM: The Universal Preference Zone** 🎵
