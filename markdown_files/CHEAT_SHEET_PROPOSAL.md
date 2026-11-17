# 📌 CHEAT SHEET: PROPOSAL TUGAS AKHIR
## **Analisis Zona Tempo Universal untuk Prediksi Popularitas Musik**

---

## 🎯 **INTI PENELITIAN DALAM 30 DETIK**

**Pertanyaan Utama:**  
Apakah ada rentang tempo musik (BPM) yang **secara universal** membuat lagu lebih populer, terlepas dari mood-nya?

**Jawaban Hipotesis:**  
Ya! Tempo **100-120 BPM** ("medium tempo") konsisten menghasilkan hit probability lebih tinggi di **semua** kategori mood.

**Data:**  
1,2 juta lagu Spotify (1920-2020)

**Hasil Awal:**  
+24.5% peningkatan hit probability, p<0.0001, effect size medium (Cohen's d=0.607)

---

## 📊 **STRUKTUR PROPOSAL (30+ Halaman)**

```
├─ BAB I: PENDAHULUAN
│  ├─ A. Latar Belakang → Kenapa topik ini penting?
│  ├─ B. Rumusan Masalah → 5 pertanyaan penelitian
│  ├─ C. Tujuan Penelitian → 5 target yang ingin dicapai
│  ├─ D. Manfaat → Teoretis + Praktis
│  ├─ E. Batasan → Scope penelitian
│  └─ F. Asumsi → Asumsi metodologis
│
├─ BAB II: KAJIAN PUSTAKA
│  ├─ A. Kajian Teori → 4 teori (MIR, Big Data, Persepsi Tempo, Prediksi)
│  ├─ B. Penelitian Relevan → 4 studi + gap analysis
│  ├─ C. Kerangka Berpikir → Diagram alur penelitian
│  └─ D. Hipotesis → 4 hipotesis (H1-H4)
│
├─ BAB III: METODE PENELITIAN
│  ├─ A. Jenis & Rancangan → Mixed-method quantitative, 4 fase
│  ├─ B. Tempat & Waktu → Lab UNESA, 6 bulan
│  ├─ C. Sumber Data → Spotify dataset 1.2M tracks
│  ├─ D. Variabel → Independen (tempo zone), Dependen (hit probability)
│  ├─ E. Prosedur Pengumpulan → Data cleaning + feature engineering
│  ├─ F. Instrumen → Python, pandas, scikit-learn
│  ├─ G. Teknik Analisis → Deskriptif, Inferensial, Prediktif
│  └─ H. Kriteria Keputusan → Signifikansi statistik & praktis
│
├─ DAFTAR PUSTAKA → 13 referensi ilmiah
│
└─ LAMPIRAN → 5 lampiran (statistik, distribusi, temuan, script)
```

---

## 🔍 **BAB I: PENDAHULUAN - RINGKASAN**

### **A. Latar Belakang (Esensi)**
1. **Fenomena:** Industri musik digital (Spotify, Apple Music) hasilkan data masif
2. **Paradigma Lama:** Tempo dipilih based on genre/mood (cepat=energi, lambat=sedih)
3. **Gap:** Belum ada studi berskala besar yang cek apakah ada "zona tempo universal"
4. **Temuan Awal:** Tempo 100-120 BPM menang di **5/5 mood categories** (unprecedented!)
5. **Implikasi:** Bisa kasih guideline evidence-based buat produser musik

### **B. Rumusan Masalah (5 Pertanyaan)**
1. Apakah ada zona tempo universal dengan hit probability superior?
2. Apakah pola ini konsisten di seluruh mood (happy, sad, angry, calm, melancholic)?
3. Berapa besar effect size-nya? (practical significance)
4. Bagaimana tempo berinteraksi dengan fitur audio lain (energy, valence, danceability)?
5. Seberapa besar peningkatan akurasi model ML kalau pakai fitur tempo zone?

### **C. Tujuan (5 Target)**
1. Identifikasi & validasi zona tempo universal secara statistik
2. Evaluasi konsistensi pola lintas mood
3. Kuantifikasi magnitude efek (Cohen's d, percentage difference)
4. Analisis interaksi tempo dengan fitur sekunder
5. Bangun model ML dan bandingkan performa (with vs without tempo zone)

### **D. Manfaat**

**Teoretis:**
- Kontribusi ke music information retrieval
- Bukti empiris preferensi tempo universal
- Framework metodologis untuk Big Data music analysis

**Praktis:**
- Guideline untuk komposer/produser (pilih tempo optimal)
- Insight untuk kurator playlist Spotify
- Fitur tambahan untuk recommendation system
- Adopsi data-driven approach di industri musik

### **E. Batasan**
- Dataset: Spotify saja (1920-2020)
- Tempo: 5 zona kategorikal (bukan granular per-BPM)
- Mood: Rule-based dari energy+valence (5 kategori)
- Hit probability: Composite metric (bukan streaming aktual)
- Model ML: Random Forest/Gradient Boosting (bukan deep learning)
- Analisis kausalitas terbatas (korelasi only)

### **F. Asumsi**
- Spotify API audio features valid & reliabel
- Popularity score = proxy untuk popularitas aktual
- Mood categorization = aproksimasi wajar
- Dataset representatif (meski ada bias Western music)
- Historical pattern applicable untuk future prediction

---

## 📚 **BAB II: KAJIAN PUSTAKA - RINGKASAN**

### **A. Kajian Teori (4 Konsep Inti)**

#### **1. Music Information Retrieval (MIR)**
- **Definisi:** Ekstraksi info dari audio musik (komputer + musikologi)
- **Audio Features:**
  - **Tempo:** Kecepatan (BPM), pengaruhi emotional intensity
  - **Energy:** Intensitas (0-1), fast/loud vs soft/calm
  - **Valence:** Kepositifan (0-1), happy vs sad
  - **Danceability:** Cocok untuk menari (tempo + beat strength)

#### **2. Big Data Analytics**
- **Definisi:** Dataset yang volume/velocity/variety melampaui traditional DB
- **Keunggulan:** Statistical power tinggi, margin of error minimal
- **Aplikasi:** Pattern identification yang tak terlihat di studi kecil
- **Dataset ini:** 1.2M tracks → confidence interval sempit = presisi tinggi

#### **3. Teori Persepsi Tempo & Respons Fisiologis**
- **Preferred Tempo (Fraisse, 1982):** Rentang 100-120 BPM paling mudah di-sync manusia
- **Biological Correspondence:**
  - 100-120 BPM = 2x walking pace (60 steps/min × 2 kaki)
  - Dekat dengan heart rate istirahat (60-100 BPM)
- **Neuroscience:** Tempo medium aktifkan basal ganglia efisien → foot-tapping involuntar
- **Hipotesis:** Resonansi biologis → enhanced enjoyment

#### **4. Model Prediksi Popularitas Musik**
- **Supervised ML:** Audio features → predict popularity metrics
- **State-of-the-art:** Hybrid models (audio + social signals) capai 83% accuracy
- **Penelitian ini:** Validasi pragmatis dengan compare model (with vs without tempo zone)

### **B. Penelitian Relevan (4 Studi + Gap)**

| Studi | Fokus | Temuan | Keterbatasan |
|-------|-------|--------|--------------|
| **Percino et al. (2014)** | Million Song Dataset | Genre diversity meningkat | Tidak analisis tempo vs popularity |
| **Interiano et al. (2018)** | Billboard Hot 100 evolution | Loudness naik, timbre homogen | Tidak cross-mood tempo analysis |
| **Ni et al. (2011)** | Hit song prediction (RF) | 74% accuracy | Tempo hanya continuous feature |
| **Van Dyck et al. (2017)** | Entrainment experiment | 100-130 BPM → strongest sync | Sample kecil (n=50), tidak cross-mood |

**Research Gaps:**
1. ❌ Belum ada studi eksplisit test universal tempo zone (dataset jutaan)
2. ❌ Tempo dianalisis continuous/genre-specific (bukan cross-mood categorical)
3. ❌ Validasi praktis via prediction model belum banyak
4. ❌ Effect size quantification kurang (fokus p-value, bukan practical significance)

### **C. Kerangka Berpikir**

```
Input: Karakteristik Audio Musik (Spotify dataset)
  ↓
Ekstraksi: Tempo (BPM)
  ↓
Kategorisasi: 5 Zona Tempo (very slow, slow, medium, fast, very fast)
  ↓
Analisis: Lintas 5 Mood (happy, sad, angry, calm, melancholic)
  ↓
Identifikasi: Pola Universal?
  ↓
Validasi: T-test, ANOVA, Effect Size (Cohen's d)
  ↓
Temuan: Zona Tempo Universal = 100-120 BPM
  ↓
Aplikasi: Integrasi ke Model ML
  ↓
Output: Hit Probability Enhancement
```

### **D. Hipotesis (4 Hipotesis)**

- **H1:** Medium tempo (100-120 BPM) punya hit probability signifikan lebih tinggi (p<0.05)
- **H2:** Pola ini konsisten di **semua** 5 mood categories (universality)
- **H3:** Effect size praktis signifikan (Cohen's d ≥ 0.5 atau % diff ≥ 15%)
- **H4:** Model ML dengan tempo zone fitur naik akurasi min +5%

---

## 🔬 **BAB III: METODE PENELITIAN - RINGKASAN**

### **A. Jenis & Rancangan (4 Fase)**

**Jenis:** Mixed-method quantitative (non-experimental correlational study)

**4 Fase Sequential:**
1. **Fase 1: Exploratory Discovery** → Cari pola awal distribusi tempo vs hit probability
2. **Fase 2: Confirmatory Statistical Testing** → Validasi hipotesis (t-test, ANOVA, effect size)
3. **Fase 3: Cross-Mood Validation** → Verify consistency across 5 moods
4. **Fase 4: Predictive Modeling** → Build ML model, compare performance

### **B. Tempat & Waktu**

- **Tempat:** Lab Komputasi, Prodi [X], Fakultas [Y], UNESA
- **Durasi:** 6 bulan
  - Bulan 1: Literature review + data acquisition
  - Bulan 2: Data preprocessing + EDA
  - Bulan 3: Feature engineering + mood categorization
  - Bulan 4: Statistical testing + validation
  - Bulan 5: ML model development + evaluation
  - Bulan 6: Synthesis + report writing

### **C. Sumber Data & Populasi**

**Dataset:**
- **Nama:** Spotify Music Dataset (Kaggle, Rodolfo Figueroa)
- **Lisensi:** CC0 Public Domain
- **File:** `tracks_features.csv` (500 MB)
- **Source:** Spotify Web API

**Karakteristik:**
- **Total:** 1,204,022 tracks
- **Periode:** 1920-2020 (100 tahun)
- **Features:** 24 original (metadata + audio features)
- **Completeness:** 100% untuk variabel kritis
- **Genre:** Multi-genre (pop, rock, electronic, hip-hop, jazz, classical)
- **Geografis:** Global coverage

### **D. Variabel & Definisi Operasional**

#### **1. Variabel Independen: ZONA TEMPO**

**Definisi:** Kategorisasi tempo ke 5 zona diskrit

| Zona | Rentang BPM | Label |
|------|-------------|-------|
| Very Slow | < 80 | very_slow |
| Slow | 80-100 | slow |
| **Medium** | **100-120** | **medium** ⭐ (Hypothesized sweet spot) |
| Fast | 120-140 | fast |
| Very Fast | > 140 | very_fast |

**Skala:** Nominal (categorical)

#### **2. Variabel Dependen: HIT PROBABILITY**

**Definisi:** Probabilitas relatif lagu jadi populer

**Formula:**
```
hit_probability = (popularity/100 × 0.4) + 
                  (danceability × 0.3) + 
                  (energy × 0.2) + 
                  (balanced_valence × 0.1)
```

**Komponen:**
- `popularity`: Spotify score 0-100, normalized → 0-1 **(weight: 40%)**
- `danceability`: 0-1 **(weight: 30%)**
- `energy`: 0-1 **(weight: 20%)**
- `balanced_valence`: 1 - |valence - 0.5| × 2 **(weight: 10%)**

**Skala:** Ratio (continuous, 0-1)

#### **3. Variabel Kontrol: MOOD CLUSTER**

**Definisi:** Kategorisasi emotional content dari energy + valence

| Mood | Rule |
|------|------|
| **Happy Energetic** | energy ≥ 0.6 AND valence ≥ 0.6 |
| **Sad Slow** | energy < 0.4 AND valence < 0.4 |
| **Angry Intense** | energy ≥ 0.6 AND valence < 0.4 |
| **Calm Positive** | energy < 0.6 AND valence ≥ 0.6 |
| **Melancholic** | Middle ground (tidak masuk kategori lain) |

**Skala:** Nominal (categorical)

#### **4. Variabel Sekunder (untuk Korelasi)**

- **Energy:** Intensitas perseptual (0-1)
- **Valence:** Kepositifan musik (0-1)
- **Danceability:** Kesesuaian untuk menari (0-1)
- **Loudness:** Kerasan dalam dB (-60 to 0)
- **Acousticness:** Akustik vs elektronik (0-1)
- **Decade:** Dekade rilis (nominal)

### **E. Prosedur Pengumpulan Data**

#### **1. Data Acquisition**
- Download dari Kaggle
- File: `tracks_features.csv` (500 MB)
- Simpan di: `data/raw/`

#### **2. Data Cleaning**
**Langkah:**
- ✅ **Duplicate Removal:** Drop duplicate track IDs
- ✅ **Missing Value Handling:** Exclude tracks dengan missing critical variables
- ✅ **Outlier Detection:** Remove tempo = 0 atau > 300 BPM (extraction errors)
- ✅ **Data Type Validation:** tempo (float), popularity (int), release_date (date)
- ✅ **Temporal Extraction:** Extract year dari release_date

**Output:** `data/processed/spotify_cleaned.parquet`

#### **3. Feature Engineering**

**a. Tempo Zone Categorization:**
```python
def categorize_tempo(tempo):
    if tempo < 80: return 'very_slow'
    elif 80 <= tempo < 100: return 'slow'
    elif 100 <= tempo <= 120: return 'medium'  # SWEET SPOT!
    elif 120 < tempo <= 140: return 'fast'
    else: return 'very_fast'
```

**b. Mood Cluster Classification:**
```python
def classify_mood(energy, valence):
    if energy >= 0.6 and valence >= 0.6: return 'happy_energetic'
    elif energy < 0.4 and valence < 0.4: return 'sad_slow'
    elif energy >= 0.6 and valence < 0.4: return 'angry_intense'
    elif energy < 0.6 and valence >= 0.6: return 'calm_positive'
    else: return 'melancholic'
```

**c. Hit Probability Calculation:**
```python
def calculate_hit_probability(row):
    balanced_valence = 1 - abs(row['valence'] - 0.5) * 2
    hit_prob = (
        row['popularity'] / 100 * 0.4 +
        row['danceability'] * 0.3 +
        row['energy'] * 0.2 +
        balanced_valence * 0.1
    )
    return hit_prob
```

**d. Additional Features:**
- `decade`: "1980s", "1990s", "2000s"
- `energy_level`: low/medium/high
- `valence_level`: negative/neutral/positive
- `emotional_arc`: Energy-valence quadrant

**Output:** `data/processed/spotify_master_enriched.parquet` (44 columns: 24 original + 20 derived)

### **F. Instrumen Penelitian**

#### **Software & Environment**
- **Language:** Python 3.10+
- **IDE:** Jupyter Notebook / VS Code
- **OS:** Windows 11 / Linux Ubuntu 20.04

#### **Python Libraries**
| Kategori | Library | Fungsi |
|----------|---------|--------|
| Data Manipulation | pandas 3.0.6 | DataFrame ops, cleaning |
| Numerical | numpy 2.5.3 | Array operations |
| Statistical | scipy.stats 1.14+ | T-test, ANOVA, chi-square |
| Machine Learning | scikit-learn 1.3+ | Random Forest, Gradient Boosting |
| Visualization | matplotlib 3.8+, seaborn 0.13+ | Plotting |
| Storage | pyarrow 25.0.1 | Parquet format |

#### **Hardware Requirements**
- **CPU:** Intel Core i5+ (multi-core recommended)
- **RAM:** 16 GB (32 GB optimal)
- **Storage:** 10 GB (SSD recommended)

### **G. Teknik Analisis Data**

#### **1. Analisis Deskriptif**

**Tujuan:** Pahami karakteristik & distribusi data

**Teknik:**
- Distribusi Frekuensi (tempo zone, mood cluster)
- Statistik Deskriptif (mean, median, std, min, max)
- Cross-Tabulation (tempo × mood)
- Visualisasi (histogram, bar chart, box plot, violin plot)

#### **2. Uji Validasi Hipotesis**

**H1: T-Test (Medium vs Others)**

**Hipotesis:**
- H₀: Tidak ada perbedaan mean hit probability medium vs others
- H₁: Mean hit probability medium **lebih tinggi** (alternative hypothesis)

**Teknik:** Independent samples t-test (two-tailed)

**Formula:**
$$t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

**Keputusan:** Tolak H₀ jika p < 0.05

**Code:**
```python
from scipy.stats import ttest_ind
medium_tempo = df[df['tempo_band'] == 'medium']['hit_probability']
other_tempo = df[df['tempo_band'] != 'medium']['hit_probability']
t_statistic, p_value = ttest_ind(medium_tempo, other_tempo)
```

---

**H2: ANOVA (All Tempo Zones)**

**Hipotesis:**
- H₀: Tidak ada perbedaan mean hit probability across 5 zones
- H₁: Minimal 1 zona berbeda signifikan

**Teknik:** One-way ANOVA

**Formula:**
$$F = \frac{MSB}{MSW}$$

**Post-Hoc:** Tukey HSD (jika ANOVA significant)

**Code:**
```python
from scipy.stats import f_oneway
tempo_groups = [
    df[df['tempo_band'] == zone]['hit_probability']
    for zone in ['very_slow', 'slow', 'medium', 'fast', 'very_fast']
]
f_statistic, p_value = f_oneway(*tempo_groups)
```

---

**H3: Effect Size Quantification**

**Metrik:** Cohen's d (standardized mean difference)

**Formula:**
$$d = \frac{\bar{X}_1 - \bar{X}_2}{s_{pooled}}$$

$$s_{pooled} = \sqrt{\frac{s_1^2 + s_2^2}{2}}$$

**Interpretasi:**
- |d| < 0.2: Small effect
- 0.2 ≤ |d| < 0.5: Small-to-medium
- **0.5 ≤ |d| < 0.8: Medium effect** ⭐
- |d| ≥ 0.8: Large effect

**Code:**
```python
import numpy as np
mean_medium = medium_tempo.mean()
mean_other = other_tempo.mean()
std_pooled = np.sqrt((medium_tempo.std()**2 + other_tempo.std()**2) / 2)
cohens_d = (mean_medium - mean_other) / std_pooled
```

#### **3. Cross-Mood Validation**

**Tujuan:** Verify universality hypothesis

**Teknik:**
- **Stratified Analysis:** T-test per mood category
- **Effect Size Consistency:** Cohen's d per mood, cek homogeneity
- **Visual Comparison:** Grouped bar charts (hit prob by tempo per mood)
- **Two-Way ANOVA:** Test interaction effect

**Model:**
```
hit_probability ~ tempo_zone + mood_cluster + (tempo_zone × mood_cluster)
```

**Interpretasi:**
- Main effect `tempo_zone`: Overall tempo effect
- Main effect `mood_cluster`: Overall mood effect
- **Interaction effect:** Jika **non-significant** (p > 0.05) → mendukung universality! ✅

#### **4. Analisis Korelasi & Feature Interaction**

**Tujuan:** Understand tempo zone relationship dengan fitur lain

**Teknik:**
- Pearson Correlation (hit prob vs energy, valence, danceability, loudness)
- Feature Distribution Comparison across tempo zones
- Interaction Term Analysis (kombinasi tempo + features lain)

#### **5. Predictive Modeling & Validation**

**Tujuan:** Demonstrate practical utility via ML accuracy improvement

**Workflow:**

**Step 1: Data Split**
```python
from sklearn.model_selection import train_test_split
X = df[feature_columns]
y = (df['hit_probability'] > 0.5).astype(int)  # Binary classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Step 2: Baseline Model (Without Tempo Zone)**
```python
baseline_features = ['energy', 'valence', 'danceability', 'loudness', 
                     'acousticness', 'tempo']  # tempo continuous
model_baseline = RandomForestClassifier(n_estimators=100, random_state=42)
model_baseline.fit(X_train[baseline_features], y_train)
y_pred_baseline = model_baseline.predict(X_test[baseline_features])
accuracy_baseline = accuracy_score(y_test, y_pred_baseline)
```

**Step 3: Enhanced Model (With Tempo Zone)**
```python
enhanced_features = baseline_features + ['is_medium_tempo']
# is_medium_tempo = binary indicator (1 if medium, 0 otherwise)
model_enhanced = RandomForestClassifier(n_estimators=100, random_state=42)
model_enhanced.fit(X_train[enhanced_features], y_train)
y_pred_enhanced = model_enhanced.predict(X_test[enhanced_features])
accuracy_enhanced = accuracy_score(y_test, y_pred_enhanced)
```

**Step 4: Model Comparison**
- Δ accuracy = accuracy_enhanced - accuracy_baseline
- McNemar's test (statistical significance of difference)
- Report: precision, recall, F1-score, ROC-AUC
- Feature importance analysis

**Evaluation Metrics:**
- **Accuracy:** Overall correctness
- **Precision:** % predicted hits yang benar
- **Recall:** % actual hits yang ter-predict
- **F1-Score:** Harmonic mean of precision & recall
- **ROC-AUC:** Area under curve

**Cross-Validation:**
```python
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model_enhanced, X[enhanced_features], y, 
                            cv=5, scoring='accuracy')
mean_cv_accuracy = cv_scores.mean()
```

### **H. Kriteria Keputusan & Interpretasi**

#### **1. Statistical Significance**
- **α = 0.05** (significance level)
- **p < 0.05:** Reject H₀, ada efek signifikan ✅
- **p ≥ 0.05:** Fail to reject H₀, bukti tidak cukup ❌

#### **2. Practical Significance**
- **Cohen's d ≥ 0.5:** Praktis signifikan (medium/large effect) ✅
- **% Difference ≥ 15%:** Substantial improvement ✅
- **Model Δ Accuracy ≥ 5%:** Meaningful enhancement ✅

#### **3. Universality Criterion**
- **Consistency Threshold:** Pattern teramati di ≥ 80% (4/5) mood categories ✅
- **Interaction Effect:** Non-significant (p > 0.05) → supports universality ✅

---

## 📈 **TEMUAN AWAL (PRELIMINARY FINDINGS)**

### **Zona Tempo Sweet Spot Universal**

| Mood Category | Best Tempo | Hit Prob | Sample Size | Status |
|---------------|------------|----------|-------------|--------|
| Happy Energetic | **Medium** | 0.7624 | 49,245 | ✅ |
| Sad Slow | **Medium** | 0.3626 | 77,279 | ✅ |
| Angry Intense | **Medium** | 0.6363 | 49,313 | ✅ |
| Calm Positive | **Medium** | 0.5561 | 36,166 | ✅ |
| Melancholic | **Medium** | 0.6067 | 54,772 | ✅ |

**Hasil:** **5/5 moods prefer medium tempo (100-120 BPM)** 🎯

**Statistical Validation:**
- **t-statistic:** 266.45
- **p-value:** < 0.0001 (highly significant!)
- **Effect size:** +24.5% (Cohen's d = 0.607, medium effect)

---

## 🎓 **KONTRIBUSI PENELITIAN**

### **Kontribusi Teoretis:**
1. ✅ Bukti empiris pola universal preferensi tempo manusia
2. ✅ Ekspansi teori persepsi musik (biological resonance hypothesis)
3. ✅ Framework metodologis Big Data music analysis

### **Kontribusi Praktis:**
1. ✅ Guideline produksi musik (pilih 100-120 BPM untuk maximize hit chance)
2. ✅ Insight untuk playlist curation (optimize engagement)
3. ✅ Enhanced recommendation system (fitur tambahan)
4. ✅ Data-driven decision making di industri kreatif

---

## 📊 **STATISTIK DATASET**

### **Distribusi Zona Tempo:**
```
Very Slow (<80):      126,953 tracks (10.5%)
Slow (80-100):        258,657 tracks (21.5%)
Medium (100-120):     266,775 tracks (22.2%) ⭐
Fast (120-140):       286,576 tracks (23.8%)
Very Fast (>140):     265,061 tracks (22.0%)
```

### **Distribusi Mood:**
```
Sad Slow:             384,322 tracks (31.9%)
Melancholic:          238,910 tracks (19.8%)
Angry Intense:        229,124 tracks (19.0%)
Happy Energetic:      214,444 tracks (17.8%)
Calm Positive:        137,222 tracks (11.4%)
```

---

## 🗂️ **FILE STRUCTURE**

```
Project/
├── data/
│   ├── raw/
│   │   └── tracks_features.csv (500 MB, original)
│   └── processed/
│       ├── spotify_cleaned.parquet (cleaned)
│       └── spotify_master_enriched.parquet (44 columns)
│
├── scripts/
│   ├── 01_load_and_clean_data.py
│   ├── 02_feature_engineering.py
│   ├── 06_discover_hypotheses.py
│   └── 07_validate_tempo_hypothesis.py
│
└── docs/
    ├── PROPOSAL_TUGAS_AKHIR_UNESA_2.md (30+ pages)
    ├── GOOGLE_DOCS_FINAL_GUIDE.md
    ├── CHEAT_SHEET_PROPOSAL.md (ini!)
    ├── SEMPRO_READINESS.md
    └── TEMPO_SWEET_SPOT_GUIDE.md
```

---

## 📚 **REFERENSI PENTING (13 Sumber)**

1. **Dhanaraj & Logan (2005)** - Automatic hit song prediction
2. **Dhar et al. (2019)** - Hybrid audio+social features, 83% accuracy
3. **Fraisse (1982)** - Preferred tempo theory
4. **Grahn & Brett (2007)** - Rhythm perception in motor areas
5. **Husain et al. (2002)** - Tempo & mode effects on arousal
6. **Interiano et al. (2018)** - Musical trends 1960-2010
7. **Laney (2001)** - 3V Big Data definition
8. **Moelants (2002)** - Preferred tempo = 120 BPM peak
9. **Müller (2015)** - Fundamentals of music processing
10. **Ni et al. (2011)** - Random Forest hit prediction, 74% accuracy
11. **Percino et al. (2014)** - Instrumental complexity & simplicity
12. **Schedl et al. (2018)** - Music recommender systems challenges
13. **Van Dyck et al. (2017)** - Spontaneous entrainment 100-130 BPM

---

## 🎯 **KEYWORDS**

`Big Data`, `Music Information Retrieval`, `Tempo Analysis`, `Hit Prediction`, `Universal Pattern`, `Spotify Dataset`, `Machine Learning`, `Statistical Validation`, `Cross-Mood Analysis`, `100-120 BPM`, `Biological Resonance`, `Data-Driven Music Production`

---

## ⚡ **QUICK FACTS**

- 📊 **Dataset:** 1,204,022 tracks
- 📅 **Timespan:** 100 years (1920-2020)
- 🎵 **Tempo Sweet Spot:** 100-120 BPM
- 📈 **Effect:** +24.5% hit probability
- 📉 **P-value:** < 0.0001
- 🎯 **Cohen's d:** 0.607 (medium effect)
- ✅ **Universality:** 5/5 moods consistent
- 🔬 **Metodologi:** 4-phase mixed-method quantitative
- 🤖 **ML Improvement:** Expected ≥5% accuracy boost
- 📝 **Proposal:** 30+ pages, 3 BAB, 13 references

---

## 🚀 **ELEVATOR PITCH (60 DETIK)**

> "Bayangkan kamu produser musik. Kamu mau bikin lagu yang viral. Pertanyaannya: **berapa BPM yang optimal?**
>
> Konvensional bilang: tergantung genre/mood. Lagu happy → fast tempo, lagu sad → slow tempo.
>
> Tapi data 1.2 juta lagu Spotify dari 100 tahun menunjukkan pola lain: **tempo 100-120 BPM menang di SEMUA kategori mood** (happy, sad, angry, calm, melancholic). Peningkatan hit probability-nya +24.5%, sangat signifikan secara statistik (p<0.0001).
>
> Kenapa? Karena 100-120 BPM cocok dengan ritme biologis manusia (walking pace, heart rate), jadi otak kita secara natural lebih enjoy musik di tempo itu.
>
> Penelitian ini validate pola universal ini pakai Big Data analytics + machine learning, dan kasih guideline praktis buat industri musik.
>
> Impact: produser bisa optimize lagu mereka, platform streaming bisa kurasi playlist lebih baik, dan kita paham preferensi musik manusia lebih dalam."

---

## ✅ **CHECKLIST SEMPRO**

Pastikan temanmu siap dengan:

- [ ] **Pahami inti penelitian** (tempo 100-120 BPM = universal sweet spot)
- [ ] **Hafal 4 hipotesis** (H1-H4)
- [ ] **Kuasai metodologi** (4 fase, t-test, ANOVA, Cohen's d, ML modeling)
- [ ] **Ingat angka kunci** (1.2M tracks, +24.5%, p<0.0001, d=0.607)
- [ ] **Siap explain gap** (kenapa penelitian ini penting?)
- [ ] **Bisa jawab "So what?"** (kontribusi teoretis + praktis)
- [ ] **Prepare defense** (anticipate questions tentang validitas, generalisasi)
- [ ] **Bring data** (distribusi tempo, mood, preliminary findings)
- [ ] **Practice pitch** (1 menit, 5 menit, 15 menit versions)
- [ ] **Confidence** (ini penelitian solid dengan data kuat!)

---

**Good luck dengan sempro! 🎓🚀**

*"Data doesn't lie. 5/5 moods prefer medium tempo. That's science."*
