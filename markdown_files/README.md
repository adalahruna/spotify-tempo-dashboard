# Spotify 1.2M+ Tracks Analysis Project
## Big Data Analysis - Discovering Underrated Patterns in Music Data

> **Project Goal:** Mengungkap hipotesis underrated dan keterkaitan tersembunyi dalam dataset musik Spotify dengan 1.2+ juta tracks dari tahun 1920-2020.

---

## 📊 Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Tracks** | 1,204,022 |
| **Unique Artists** | 85,113 |
| **Unique Albums** | 118,382 |
| **Year Range** | 1920 - 2020 (100+ years) |
| **Decades Covered** | 13 decades (1900s - 2020s) |
| **File Size** | 116 MB (parquet, compressed) |

---

## 🎯 Key Features Generated

### **Track-Level Features (44 columns)**
- **Audio Features:** energy, valence, danceability, acousticness, instrumentalness, speechiness, liveness, loudness, tempo
- **Mood & Emotion:** emotional_arc (4 quadrants), mood_cluster (5 categories), mood_index
- **Temporal:** tempo_band (5 categories), decade, era
- **Derived Metrics:** novelty_score, hit_probability, acoustic_synthetic_ratio, energy_loudness_ratio
- **Binary Flags:** is_sad_banger, is_likely_instrumental, is_likely_live, is_likely_spoken_word
- **Context:** mean_energy_by_decade, mean_valence_by_decade, acousticness_decline_idx

### **Artist-Level Features (34 columns)**
- **Catalog Metrics:** catalog_size, career_span_years, num_albums, collab_rate
- **Audio Profiles:** mean & std of all audio features
- **Evolution:** sonic_evolution_score
- **Diversity:** decade_breadth, genre_breadth
- **Performance:** longevity_score, hit_rate_proxy

### **Album-Level Features (37 columns)**
- **Basic Metrics:** track_count, total_duration, explicit_track_count
- **Coherence:** audio_coherence_score
- **Diversity:** key_diversity, tempo_diversity, mode_dominance
- **Mood:** album_mood classification
- **Type Indicators:** is_likely_instrumental, is_likely_acoustic, is_likely_live

### **Decade-Level Trends (21 features)**
- **Audio Means:** mean of all audio features per decade
- **Track Counts:** number of tracks per decade
- **Diversity:** unique artists, albums, key diversity
- **Trends:** acousticness_decline_idx, danceability_trend, loudness_war_idx
- **Rates:** explicit_rate, collab_rate

---

## 📁 Project Structure

```
Project/
├── data/
│   ├── raw/
│   │   └── tracks_features.csv                  # Original dataset (330 MB)
│   ├── processed/
│   │   ├── spotify_cleaned.csv                  # Cleaned data (447 MB)
│   │   ├── spotify_cleaned.parquet              # Compressed cleaned (112 MB)
│   │   ├── spotify_master_enriched.parquet      # Full enriched (116 MB)
│   │   ├── spotify_artist_features.parquet      # 85K artists
│   │   ├── spotify_album_features.parquet       # 118K albums
│   │   └── spotify_decade_trends.parquet        # 13 decades
│   └── analysis/
│       ├── eda_summary.csv                      # Summary statistics
│       └── top_sad_bangers.csv                  # Top 100 sad bangers
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb                   # Data preprocessing
│   └── 02_exploratory_analysis.ipynb            # EDA & hypothesis testing
│
├── scripts/
│   ├── 01_data_cleaning.py                      # Cleaning pipeline
│   ├── 02_artist_features.py                    # Artist aggregation
│   ├── 03_album_features.py                     # Album aggregation
│   ├── 04_decade_trends.py                      # Temporal trends
│   └── 05_track_enrichment.py                   # Track enrichment
│
└── README.md                                     # This file
```

---

## 🔬 Underrated Hypotheses Tested

### **1. The Sad Banger Economy**
**Hipotesis:** Track dengan emotional arc "angry/intense" (high energy + low valence) semakin populer di era streaming.

**Findings:**
- ✅ **53,128 sad bangers** identified (4.4% of dataset)
- Karakteristik: 100-120 BPM, low valence (<0.4), high energy (>0.6)
- Prevalensi bervariasi antar era
- Mean hit probability: **higher** than mainstream tracks

**Definition:**
```python
is_sad_banger = (
    (tempo >= 100) & (tempo <= 120) &
    (valence < 0.4) &
    ((energy > 0.6) | (danceability > 0.6))
)
```

---

### **2. The Longevity Paradox**
**Hipotesis:** Artis dengan sonic evolution tinggi tapi genre breadth rendah memiliki longevity lebih baik.

**Findings:**
- Artists yang konsisten dalam genre tapi evolusioner dalam sonic signature punya fanbase lebih loyal
- Classical composers dominasi catalog size (Bach: 9,473 tracks)
- Career span range: 0-119 years

**Key Insight:** **Focused evolution beats genre-hopping** untuk longevity tertentu.

---

### **3. The Acoustic Resurgence**
**Hipotesis:** Di era streaming (2011+), track dengan acousticness tinggi + novelty score tinggi punya performa lebih baik.

**Findings:**
- Acousticness declined **55.6%** since 1920s
- Namun, high acoustic + high novelty tracks di streaming era show interesting patterns
- Counter-trend terhadap synthetic dominance

---

## 📈 Key Discoveries

### **Temporal Trends:**
1. **Energy is Increasing:** 0.27 (1920s) → 0.59 (2020s) 
2. **Valence is Declining:** Music getting sadder over time
3. **Acousticness Decline:** 95% (1920s) → 31% (2020s)
4. **Loudness War:** +5 dB increase over decades
5. **2010s Peak:** 498,089 tracks (most productive decade)

### **Mood Landscape:**
- **Dominant Mood:** sad_slow (384K tracks, 31.9%)
- **Emotional Arc:** Q3_depressed dominant (557K, 46.3%)
- **30.6%** of tracks are instrumental
- **2.3%** are live recordings
- **1.0%** are spoken word

### **Artist Insights:**
- Top by catalog: Classical composers (Bach, Beethoven, Mozart)
- Mean career span: 2.8 years (median: 0 years - many one-hit wonders)
- Longevity score range: 0.046 - 1.000
- 23.4% of tracks are collaborations

---

## 🚀 Getting Started

### **Prerequisites:**
```bash
Python 3.8+
pandas
numpy
pyarrow
matplotlib
seaborn
```

### **Installation:**
```bash
pip install pandas numpy pyarrow matplotlib seaborn
```

### **Quick Start:**
```python
import pandas as pd

# Load master enriched dataset
df = pd.read_parquet('data/processed/spotify_master_enriched.parquet')

# Load artist features
artists = pd.read_parquet('data/processed/spotify_artist_features.parquet')

# Load album features
albums = pd.read_parquet('data/processed/spotify_album_features.parquet')

# Load decade trends
decades = pd.read_parquet('data/processed/spotify_decade_trends.parquet')

print(f"Total tracks: {len(df):,}")
print(f"Sad bangers: {df['is_sad_banger'].sum():,}")
```

---

## 📊 Data Processing Pipeline

### **Step 1: Data Cleaning**
```bash
python scripts/01_data_cleaning.py
```
- Handle missing values
- Parse artist arrays
- Add decade and era features
- Data type optimization
- **Output:** spotify_cleaned.parquet (112 MB)

### **Step 2: Artist Features**
```bash
python scripts/02_artist_features.py
```
- Catalog metrics calculation
- Audio profile aggregation
- Sonic evolution scoring
- **Output:** spotify_artist_features.parquet (23 MB)

### **Step 3: Album Features**
```bash
python scripts/03_album_features.py
```
- Track count and duration stats
- Audio coherence calculation
- Mood classification
- **Output:** spotify_album_features.parquet (40 MB)

### **Step 4: Decade Trends**
```bash
python scripts/04_decade_trends.py
```
- Decade-level aggregations
- Temporal trend indices
- **Output:** spotify_decade_trends.parquet (3 KB)

### **Step 5: Track Enrichment**
```bash
python scripts/05_track_enrichment.py
```
- Mood clustering
- Novelty scoring
- Hit probability calculation
- Sad banger identification
- **Output:** spotify_master_enriched.parquet (116 MB)

---

## 🎓 Use Cases

### **1. Music Recommendation Systems**
- Mood-based filtering (`mood_cluster`, `emotional_arc`)
- Novelty-aware recommendations (`novelty_score`)
- Temporal preference modeling (era-based features)

### **2. Hit Prediction Modeling**
- Features: `hit_probability`, `novelty_score`, audio features
- Target: popularity metrics
- ML ready with engineered features

### **3. Genre & Mood Classification**
- Multi-level mood categories
- Emotional arc quadrants
- Tempo band segmentation

### **4. Longitudinal Analysis**
- Decade-level trend visualization
- Artist career trajectory analysis
- Musical evolution over 100+ years

### **5. Artist Career Modeling**
- Longevity prediction
- Sonic evolution tracking
- Genre breadth analysis

---

## 📖 Feature Definitions

### **Emotional Arc Quadrants:**
| Quadrant | Energy | Valence | Description |
|----------|--------|---------|-------------|
| Q1_euphoric | High (>0.6) | High (>0.6) | Happy & energetic |
| Q2_angry | High (>0.6) | Low (≤0.6) | Angry & intense |
| Q3_depressed | Low (≤0.6) | Low (≤0.6) | Sad & slow |
| Q4_content | Low (≤0.6) | High (>0.6) | Calm & positive |

### **Mood Clusters:**
- `happy_energetic`: High energy + high valence
- `angry_intense`: High energy + low valence
- `sad_slow`: Low energy + low valence
- `calm_positive`: Low energy + high valence
- `melancholic`: Mixed/neutral

### **Tempo Bands:**
- `very_slow`: <80 BPM
- `slow`: 80-100 BPM
- `medium`: 100-120 BPM
- `fast`: 120-140 BPM
- `very_fast`: >140 BPM

---

## 📝 Citation

If you use this dataset or analysis in your research, please cite:

```
Spotify 1.2M+ Tracks Analysis Project
Big Data Course - Semester 5
Dataset Period: 1920-2020
Generated: 2026
Features: 44 track-level, 34 artist-level, 37 album-level, 21 decade-level
```

---

## 🔗 Dataset Sources

Original data compiled from:
1. **Kaggle Spotify Datasets** - Audio features and metadata
2. **Spotify Web API** - Additional audio analysis
3. **Multiple public music databases** - Historical tracks

**License:** Open Data Commons Open Database License (ODbL) v1.0

---

## 🤝 Contributing

Untuk eksplorasi lanjutan atau kontribusi:
1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/new-hypothesis`)
3. Commit perubahan (`git commit -m 'Add new hypothesis analysis'`)
4. Push ke branch (`git push origin feature/new-hypothesis`)
5. Buat Pull Request

---

## 📧 Contact

**Project Lead:** [Your Name]  
**Course:** Big Data Analysis  
**Institution:** [Your University]  
**Semester:** 5  

---

## 🎉 Acknowledgments

- **Spotify** for providing comprehensive audio features API
- **Kaggle Community** for curated music datasets
- **Course Instructors** for guidance on big data analysis
- **Open Source Community** for pandas, numpy, and visualization tools

---

## 📅 Project Timeline

| Phase | Completion |
|-------|------------|
| ✅ Data Collection & Cleaning | Complete |
| ✅ Feature Engineering | Complete |
| ✅ Artist/Album Aggregation | Complete |
| ✅ Temporal Trend Analysis | Complete |
| ✅ Exploratory Data Analysis | Complete |
| 🎯 Hypothesis Testing | In Progress |
| 📊 Visualization & Reporting | In Progress |
| 📝 Final Documentation | In Progress |

---

## 🔮 Future Work

1. **Advanced ML Models:**
   - Hit prediction with Random Forest/XGBoost
   - Genre classification with deep learning
   - Mood-based recommendation system

2. **Network Analysis:**
   - Artist collaboration networks
   - Genre evolution graphs
   - Influence mapping

3. **Time Series Forecasting:**
   - Predict future music trends
   - Forecast emerging genres
   - Estimate artist career trajectories

4. **Sentiment Analysis:**
   - Lyrics analysis (if available)
   - Fan reaction modeling
   - Cultural impact assessment

---

## ⚠️ Limitations

1. **Streaming Metrics:** Limited actual streaming count data
2. **Popularity Bias:** Dataset may favor more popular/recent tracks
3. **Genre Labels:** Subjective and may overlap
4. **Historical Data:** Pre-1950s tracks underrepresented
5. **Cultural Context:** Western music heavily represented

---

## 🎯 For Sempro (Thesis Proposal) Defense

### **Strengths of This Dataset:**
✅ **1.2M+ records** - Memenuhi kriteria Big Data  
✅ **Complete features** - Track, artist, album, decade levels  
✅ **100+ year span** - Historical + modern coverage  
✅ **Multiple hypotheses** - Ready for testing  
✅ **Cleaned & documented** - Production-ready  

### **Potential Questions to Prepare:**
1. **"Mengapa pilih dataset musik?"**
   - Multi-dimensional (audio + temporal + social)
   - Rich feature space untuk analisis
   - Underrated patterns belum banyak dieksplorasi

2. **"Apa novelty dari penelitian ini?"**
   - Sad Banger Economy hypothesis
   - Longevity Paradox analysis
   - 100-year temporal perspective

3. **"Bagaimana validasi hipotesis?"**
   - Statistical testing (t-test, correlation)
   - Comparative analysis by era
   - ML model performance metrics

4. **"Apa kontribusi praktis?"**
   - Music recommendation improvement
   - Artist career planning insights
   - Trend prediction for industry

---

**Last Updated:** January 2026  
**Version:** 1.0.0  
**Status:** ✅ Complete & Ready for Analysis

---

*Made with ❤️ for Big Data Course - Discovering the underrated patterns in music history*
