# 🎓 MATERI PRESENTASI PROPOSAL BAB I & BAB II
## Analisis Zona Tempo Universal dalam Sistem Prediksi Popularitas Musik Berbasis Big Data

---

# SLIDE 1: COVER

**PROPOSAL TUGAS AKHIR**

# Analisis Zona Tempo Universal dalam Sistem Prediksi Popularitas Musik Berbasis Big Data

**Disusun oleh:**
[Nama Mahasiswa]
NIM: [Nomor Induk]

**Program Studi:** [Nama Prodi]
**Fakultas:** [Nama Fakultas]
**Universitas Negeri Surabaya**

**Pembimbing:**
[Nama Dosen Pembimbing]

**Tahun 2026**

---

# SLIDE 2: OUTLINE PRESENTASI

## Agenda Hari Ini

### **BAB I: PENDAHULUAN**
- Latar Belakang
- Rumusan Masalah
- Tujuan Penelitian
- Manfaat Penelitian
- Batasan Penelitian
- Asumsi Penelitian

### **BAB II: KAJIAN PUSTAKA**
- Kajian Teori
- Penelitian yang Relevan
- Kerangka Berpikir
- Hipotesis Penelitian

---

# 📖 BAB I: PENDAHULUAN

---

# SLIDE 3: LATAR BELAKANG (1/4)

## Fenomena Era Digital Music

### 🌍 **Ledakan Data Musik Global**

| Platform | Jumlah Lagu | Users Aktif |
|----------|-------------|-------------|
| Spotify | 100+ juta tracks | 574 juta (2023) |
| Apple Music | 100+ juta tracks | 93 juta (2023) |
| YouTube Music | 80+ juta tracks | 80+ juta |

### 📊 **Big Data Challenge:**
- Volume: Terabytes audio data per hari
- Velocity: Real-time streaming
- Variety: Multi-genre, multi-language, multi-format

### 💡 **Pertanyaan Fundamental:**
> *"Apa karakteristik yang membuat sebuah lagu menjadi populer?"*

---

# SLIDE 4: LATAR BELAKANG (2/4)

## Paradigma Lama dalam Pemilihan Tempo

### ❌ **Pendekatan Konvensional:**

```
Genre → Tempo
├─ Dance/EDM     → Fast tempo (120-140 BPM)
├─ Pop           → Medium tempo (100-120 BPM)
├─ Ballad        → Slow tempo (60-80 BPM)
└─ Rock/Metal    → Variable (90-180 BPM)
```

### 📌 **Asumsi Tradisional:**
- Tempo = pilihan **genre-specific**
- Lagu happy = fast tempo
- Lagu sad = slow tempo
- Tidak ada pola universal

### ❓ **Pertanyaan yang Muncul:**
> "Apakah benar tidak ada pola tempo yang berlaku **universal** untuk meningkatkan popularitas?"

---

# SLIDE 5: LATAR BELAKANG (3/4)

## Gap Penelitian

### 🔍 **Review Studi Terdahulu:**

1. **Dhanaraj & Logan (2005)** - 1,700 lagu
   - Focus: Acoustic + lyric features
   - Gap: Dataset kecil, tempo = continuous variable

2. **Ni et al. (2011)** - UK Charts 50 tahun
   - Focus: Random Forest prediction
   - Gap: Tempo tidak dianalisis sebagai zona kategoris

3. **Interiano et al. (2018)** - 500,000 lagu
   - Focus: Temporal evolution 30 tahun
   - Gap: Tidak eksplisit test universal tempo zone

4. **Dhar et al. (2019)** - Hybrid features
   - Focus: Audio + social signals
   - Gap: Analisis per-genre terpisah

### 🔴 **Research Gap:**
> Belum ada studi Big Data yang eksplisit menguji **zona tempo universal** dengan konsistensi **lintas mood**

---

# SLIDE 6: LATAR BELAKANG (4/4)

## Motivasi & Rasionalitas

### 🧠 **Landasan Teoretis:**

**1. Biological Resonance Hypothesis**
- Tempo 100-120 BPM ≈ 2× walking pace (60 steps/min)
- Dekat dengan resting heart rate (60-100 BPM)
- Fraisse (1982): "Preferred tempo" theory

**2. Neuroscience Evidence**
- Grahn & Brett (2007): Basal ganglia activation optimal di medium tempo
- Spontaneous foot-tapping, head-nodding

**3. Entrainment Studies**
- Van Dyck et al. (2017): Running cadence sync dengan 100-130 BPM
- Evidence: tempo affects physical movement

### 🎯 **Hipotesis Penelitian:**
> *"Tempo 100-120 BPM adalah zona universal yang meningkatkan popularitas musik, **terlepas dari mood-nya**"*

---

# SLIDE 7: RUMUSAN MASALAH

## 5 Pertanyaan Penelitian

### **RP 1: Efek Zona Tempo**
Apakah terdapat zona tempo tertentu yang memiliki hit probability **signifikan lebih tinggi** dibandingkan zona tempo lainnya?

### **RP 2: Konsistensi Lintas Mood**
Apakah pola zona tempo tersebut **konsisten** di seluruh kategori mood (happy, sad, angry, calm, melancholic)?

### **RP 3: Magnitude Efek**
Berapa besar **magnitude efek** zona tempo terhadap hit probability? (practical significance)

### **RP 4: Interaksi dengan Fitur Lain**
Bagaimana zona tempo **berinteraksi** dengan fitur audio sekunder (energy, valence, danceability)?

### **RP 5: Utilitas Prediktif**
Seberapa besar zona tempo dapat **meningkatkan akurasi** model machine learning untuk prediksi popularitas?

---

# SLIDE 8: TUJUAN PENELITIAN

## 5 Tujuan Penelitian

### **T1: Identifikasi & Validasi**
Mengidentifikasi dan memvalidasi zona tempo universal secara statistik menggunakan uji t-test dan ANOVA (α = 0.05)

### **T2: Evaluasi Konsistensi**
Mengevaluasi konsistensi pola zona tempo di kelima kategori mood melalui stratified analysis

### **T3: Kuantifikasi Effect Size**
Mengkuantifikasi magnitude efek zona tempo menggunakan Cohen's d dan percentage difference

### **T4: Analisis Interaksi**
Menganalisis interaksi zona tempo dengan fitur audio sekunder menggunakan correlation analysis dan two-way ANOVA

### **T5: Model Prediktif**
Membangun dan membandingkan model machine learning (baseline vs enhanced) untuk demonstrasi utilitas praktis

---

# SLIDE 9: MANFAAT PENELITIAN (1/2)

## Manfaat Teoretis

### **1. Kontribusi ke Music Information Retrieval (MIR)**
- Bukti empiris pertama tentang **pola tempo universal** di skala Big Data (1,204,022 tracks)
- Validasi biological resonance hypothesis dengan data real-world

### **2. Ekspansi Teori Persepsi Musik**
- Bridge antara music psychology (preferred tempo) dengan data science
- Quantified evidence untuk teori Fraisse (1982) dan Moelants (2002)

### **3. Framework Metodologis**
- Framework analisis categorical tempo zones untuk Big Data music
- Multi-level validation approach (descriptive → inferential → predictive)

### **4. Cross-disciplinary Insight**
- Koneksi antara neuroscience, music psychology, dan machine learning
- Foundation untuk penelitian musik berbasis data

---

# SLIDE 10: MANFAAT PENELITIAN (2/2)

## Manfaat Praktis

### **1. Produksi Musik (Music Producers)**
✅ Guideline evidence-based: "Pilih tempo 100-120 BPM untuk maximize hit potential"
✅ Data-driven decision making (bukan hanya intuisi)
✅ Applicable untuk berbagai mood/genre

### **2. Platform Streaming (Spotify, Apple Music)**
✅ Optimize playlist curation dengan tempo sweet spot awareness
✅ Enhanced recommendation algorithms
✅ Better user engagement prediction

### **3. Music AI Development**
✅ Tempo zone sebagai categorical feature untuk ML models
✅ Improved hit prediction accuracy
✅ Feature engineering best practices

### **4. Industri Kreatif**
✅ Briefing guidelines untuk songwriter/komposer
✅ A/R (Artist & Repertoire) decision support
✅ Marketing strategy (release timing, playlist placement)

---

# SLIDE 11: BATASAN PENELITIAN

## Scope & Limitations

### **1. Batasan Dataset**
- **Platform:** Spotify saja (tidak termasuk Apple Music, YouTube Music, dll)
- **Periode:** 1920-2020 (tidak real-time)
- **Geografis:** Global tapi Western music dominan
- **Bias:** Popularity score = proxy untuk commercial success (bukan artistic quality)

### **2. Batasan Metodologis**
- **Tempo:** 5 zona kategoris (bukan granular per-BPM analysis)
- **Mood:** Rule-based categorization (bukan ground truth annotation)
- **Kausalitas:** Correlational study (bukan causal inference)
- **ML:** Random Forest/Gradient Boosting (bukan deep learning)

### **3. Batasan Generalisasi**
- **Genre emerging:** TikTok viral songs, hyperpop mungkin berbeda
- **Musik tradisional:** Dataset tidak representatif untuk traditional music
- **Temporal change:** Preferensi bisa berevolusi over time
- **Individual preference:** Aggregate pattern (bukan personalized)

---

# SLIDE 12: ASUMSI PENELITIAN

## 6 Asumsi Metodologis

### **A1: Validitas Data**
Spotify Web API audio features (tempo, energy, valence, dll) adalah **valid dan reliable** sebagai representasi karakteristik musik

### **A2: Popularity sebagai Proxy**
Popularity score Spotify (0-100) merupakan **proxy yang wajar** untuk popularitas aktual suatu lagu di pasaran

### **A3: Mood Categorization**
Kategorisasi mood berdasarkan energy dan valence adalah **aproksimasi yang memadai** untuk representasi emosi musik

### **A4: Representativeness**
Dataset 1,204,022 tracks **representatif** untuk populasi musik populer global (meski ada bias)

### **A5: Temporal Stability**
Pola preferensi tempo relatif **stabil** dalam window observasi (1920-2020) untuk analisis aggregate

### **A6: Applicability**
Temuan dari analisis historis **applicable** untuk prediksi dan guideline produksi musik contemporary

---

# 📚 BAB II: KAJIAN PUSTAKA

---

# SLIDE 13: KAJIAN TEORI (1/6)

## A. Music Information Retrieval (MIR)

### **Definisi (Müller, 2015):**
> "Bidang interdisipliner yang mengombinasikan ilmu komputer, signal processing, musikologi, dan psikologi untuk mengekstraksi informasi dari sinyal audio musik"

### **Audio Features yang Relevan:**

| Feature | Definisi | Range | Pengaruh |
|---------|----------|-------|----------|
| **Tempo** | Kecepatan musik (BPM) | 40-200+ | Arousal, movement sync |
| **Energy** | Intensitas perseptual | 0-1 | Excitement, engagement |
| **Valence** | Kepositifan emosional | 0-1 | Mood, emotional response |
| **Danceability** | Kesesuaian untuk menari | 0-1 | Physical engagement |

### **Aplikasi:**
- Genre classification
- Mood detection
- **Hit song prediction** ← Focus penelitian ini
- Music recommendation

---

# SLIDE 14: KAJIAN TEORI (2/6)

## B. Big Data Analytics & 3V Framework

### **Definisi Big Data (Laney, 2001):**
> "Data yang volume, velocity, dan variety-nya melampaui kemampuan traditional database management systems"

### **3V dalam Konteks Penelitian Ini:**

```
┌─────────────────────────────────────────────────┐
│ VOLUME (Ukuran Data)                            │
│ • 1,204,022 tracks                              │
│ • 44 features per track                         │
│ • ~250 MB (compressed parquet)                  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ VELOCITY (Kecepatan)                            │
│ • Spotify API real-time capability              │
│ • Batch processing untuk historical analysis    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ VARIETY (Keragaman)                             │
│ • Metadata (artist, album, release date)        │
│ • Audio features (tempo, energy, valence)       │
│ • Derived features (mood, tempo zone, hit prob) │
└─────────────────────────────────────────────────┘
```

---

# SLIDE 15: KAJIAN TEORI (3/6)

## B. Big Data Analytics (Lanjutan)

### **Keuntungan Big Data untuk Penelitian Musik:**

**1. Statistical Power Tinggi**
- Large sample size (n > 1 juta) → margin of error minimal
- Confidence interval sempit → presisi tinggi
- Deteksi efek kecil yang signifikan

**2. Pattern Identification**
- Pola tersembunyi yang tidak terlihat di studi kecil
- Cross-validation robust
- Subgroup analysis (per mood, per decade, dll)

**3. Generalizability**
- Representasi luas populasi musik
- Reduce sampling bias
- Applicability findings ke real-world scenarios

### **Penelitian Ini:**
Dataset 1.2M tracks → **sufficient power** untuk detect Cohen's d = 0.5 dengan α = 0.05, power = 0.99

---

# SLIDE 16: KAJIAN TEORI (4/6)

## C. Teori Persepsi Tempo & Respons Fisiologis

### **Preferred Tempo Theory (Fraisse, 1982)**

**Core Concept:**
> "Manusia memiliki preferred tempo sekitar 100-120 BPM untuk repetitive movements"

**Biological Basis:**
- **Walking pace:** 60 steps/minute × 2 feet = **120 BPM**
- **Resting heart rate:** 60-100 BPM (average ~70 BPM)
- **Optimal motor control:** Tempo medium = easiest to synchronize

### **Moelants (2002) - Empirical Validation:**
- Study dengan berbagai tempo stimuli
- Peak preference: **120-125 BPM**
- Stable across different musical styles
- Interpreted as "natural tempo" for humans

### **Hypothesis:**
> Resonansi biologis di tempo 100-120 BPM → enhanced enjoyment → higher popularity

---

# SLIDE 17: KAJIAN TEORI (5/6)

## C. Neuroscience of Beat Perception

### **Grahn & Brett (2007) - fMRI Study**

**Key Findings:**
1. **Basal ganglia** respond strongly to regular beat
2. **Supplementary Motor Area (SMA)** activated during beat perception
3. Activation **strongest** at medium tempo (around 120 BPM)

**Implications:**
- Beat perception = automatic motor system response
- Medium tempo = optimal neural activation
- Connection between movement and music preference

### **Husain, Thompson, & Schellenberg (2002)**

**Experimental Design:**
- Manipulate tempo (fast vs slow) dan mode (major vs minor)
- Measure arousal, mood, spatial abilities

**Results:**
- **Tempo → Arousal:** Fast tempo = high arousal
- **Mode → Mood:** Major = positive mood
- Changes in arousal/mood **parallel** performance on tasks

**Relevance:**
Medium tempo = balance antara arousal dan enjoyment

---

# SLIDE 18: KAJIAN TEORI (6/6)

## D. Model Prediksi Popularitas Musik

### **Supervised Machine Learning Approach**

**Input Features:** Audio characteristics (tempo, energy, valence, danceability, loudness, dll)
**Output:** Popularity score / Hit classification (binary: hit vs non-hit)

### **State-of-the-Art Performance:**

| Study | Features | Algorithm | Accuracy |
|-------|----------|-----------|----------|
| Ni et al. (2011) | 23 audio features | Random Forest | 60-74% |
| Dhar et al. (2019) | Audio + social | Hybrid ensemble | **83%** |
| Interiano et al. (2018) | Audio + temporal | Random Forest | 86% |

### **Common Features Used:**
- ✅ Tempo (continuous)
- ✅ Energy, valence, danceability
- ✅ Loudness, acousticness
- ❌ **Tempo zone (categorical)** ← Novel contribution penelitian ini!

### **Research Contribution:**
> Validate tempo zone sebagai **meaningful categorical feature** melalui:
> 1. Statistical validation (t-test, ANOVA)
> 2. Practical validation (ML model improvement)

---

# SLIDE 19: PENELITIAN YANG RELEVAN (1/4)

## Studi 1: Percino et al. (2014)

### **Judul:**
"Instrumentational Complexity of Music Genres and Why Simplicity Sells"

### **Dataset:**
Million Song Dataset + AllMusic metadata

### **Metode:**
- Network analysis (music styles × instruments)
- Complexity metric: variety × uniformity

### **Temuan:**
- Simplicity in instrumentation → **higher sales**
- As styles attract more artists → complexity increases → sales decrease
- "Formulaic music sells"

### **Relevansi:**
Mendukung ide bahwa **simple, accessible patterns** (seperti medium tempo) → broader appeal

### **Gap:**
Tidak menganalisis tempo sebagai faktor popularitas

---

# SLIDE 20: PENELITIAN YANG RELEVAN (2/4)

## Studi 2: Interiano et al. (2018)

### **Judul:**
"Musical Trends and Predictability of Success in Contemporary Songs"

### **Dataset:**
500,000 songs, UK Charts 1985-2015 (30 tahun)

### **Metode:**
- Temporal evolution analysis
- Random Forest classification (hit vs non-hit)
- Feature importance ranking

### **Temuan:**
- Hit songs are **"happier"**, more **"female"**, more **"party-like"**
- Overall trend: songs getting **sadder** over time (but hits buck the trend!)
- Prediction accuracy: **86%** (with artist "superstar" variable)

### **Relevansi:**
- Demonstrate feasibility of audio-based hit prediction
- Feature importance analysis approach

### **Gap:**
- Tempo analyzed as **continuous variable** (bukan categorical zones)
- Tidak eksplisit test universal tempo pattern **across moods**

---

# SLIDE 21: PENELITIAN YANG RELEVAN (3/4)

## Studi 3: Ni et al. (2011)

### **Judul:**
"Hit Song Science Once Again a Science?"

### **Dataset:**
UK Top 40 singles charts, 50 years

### **Metode:**
- Extract 23 audio features (tempo, timbre, harmony, dll)
- Machine learning: Random Forest, SVM
- Classification: hit (top 5) vs non-hit (below 30)

### **Temuan:**
- Classification accuracy: **60-74%** (depending on threshold)
- Better than random (50%), but not perfect
- Tempo included but not analyzed separately

### **Relevansi:**
- Baseline untuk ML approach in hit prediction
- Framework untuk feature-based classification

### **Gap:**
- Tempo = continuous feature (not categorical)
- Small-scale compared to Big Data standards today
- No cross-mood analysis

---

# SLIDE 22: PENELITIAN YANG RELEVAN (4/4)

## Studi 4: Van Dyck et al. (2017)

### **Judul:**
"Spontaneous Entrainment of Running Cadence to Music Tempo"

### **Dataset:**
16 recreational runners, experimental design

### **Metode:**
- Runners dengar musik with varying tempo (±1-3% dari baseline cadence)
- Measure: apakah cadence menyesuaikan dengan music tempo?

### **Temuan:**
- **Spontaneous entrainment** occurs even dengan tempo changes kecil
- Strongest sync: **100-130 BPM** range
- Evidence: music tempo **directly affects** physical movement

### **Relevansi:**
- Empirical evidence untuk biological resonance hypothesis
- Medium tempo = optimal untuk human motor sync

### **Gap:**
- Small sample (n=16)
- Experimental (not observational Big Data)
- Focus on physical activity (not music preference/popularity)

---

# SLIDE 23: GAP ANALYSIS

## Summary: Research Gaps yang Diisi

| Aspek | Studi Terdahulu | Gap | Penelitian Ini |
|-------|-----------------|-----|----------------|
| **Dataset Size** | 1.7k - 500k tracks | Not true "Big Data" scale | **1.2M+ tracks** ✅ |
| **Tempo Analysis** | Continuous variable | Not categorical zones | **5 tempo zones** ✅ |
| **Cross-Mood** | Genre-specific / aggregate | No explicit mood stratification | **5 mood categories** ✅ |
| **Effect Size** | Focus on p-value | Practical significance kurang | **Cohen's d + % diff** ✅ |
| **Universal Pattern** | Assumption: genre-dependent | Not tested explicitly | **Test universality** ✅ |
| **Validation Level** | Statistical OR predictive | Not both | **Multi-level validation** ✅ |

### **Novelty Statement:**
> Penelitian ini adalah studi pertama yang **eksplisit menguji zona tempo universal** dengan:
> 1. Big Data scale (1.2M+ tracks)
> 2. Cross-mood consistency validation (5 categories)
> 3. Multi-level validation (statistical + practical + predictive)

---

# SLIDE 24: KERANGKA BERPIKIR

## Logical Flow Penelitian

```
┌────────────────────────────────────────────────────────┐
│ INPUT: Karakteristik Audio Musik                      │
│ • Tempo, Energy, Valence, Danceability, Popularity    │
│ • Source: Spotify Dataset (1.2M tracks)                │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ KATEGORISASI:                                          │
│ • Tempo → 5 Zona (very slow, slow, medium, fast, very fast) │
│ • Mood → 5 Cluster (happy, sad, angry, calm, melancholic)   │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ ANALISIS DESKRIPTIF:                                   │
│ • Distribusi hit probability per tempo zone            │
│ • Cross-tabulation: tempo × mood                       │
│ • Visual exploration (box plot, violin plot)           │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ IDENTIFIKASI POLA:                                     │
│ • Apakah ada tempo zone dengan hit prob lebih tinggi?  │
│ • Apakah pola konsisten across moods?                  │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ VALIDASI STATISTIK:                                    │
│ • H1: T-test (medium vs others) → p < 0.05?            │
│ • H2: Stratified t-test per mood → 5/5 konsisten?      │
│ • H3: Effect size (Cohen's d ≥ 0.5? % diff ≥ 15%?)    │
│ • Two-way ANOVA: tempo × mood interaction              │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ TEMUAN:                                                │
│ Zona Tempo Universal = 100-120 BPM                     │
│ (jika H1, H2, H3 terpenuhi)                            │
└──────────────────┬─────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────────────┐
│ VALIDASI PRAGMATIS (Future: BAB III):                  │
│ • Build ML model (with vs without tempo zone)          │
│ • Compare accuracy → H4: Δ ≥ 5%?                       │
└────────────────────────────────────────────────────────┘
```

---

# SLIDE 25: HIPOTESIS PENELITIAN

## 4 Hipotesis Penelitian (H1-H4)

### **H1: Efek Zona Tempo (Tempo Zone Effect)**
> **H₀:** Tidak ada perbedaan mean hit probability antara medium tempo (100-120 BPM) dengan zona tempo lainnya
>
> **H₁:** Mean hit probability medium tempo **signifikan lebih tinggi** dibandingkan zona tempo lainnya (α = 0.05)
>
> **Uji:** Independent samples t-test (two-tailed)

---

### **H2: Konsistensi Lintas Mood (Cross-Mood Consistency)**
> **H₀:** Pola zona tempo tidak konsisten across mood categories
>
> **H₁:** Medium tempo memiliki hit probability tertinggi di **minimal 4 dari 5** mood categories (≥ 80%)
>
> **Uji:** Stratified t-test per mood + consistency check

---

### **H3: Magnitude Efek (Practical Significance)**
> **H₀:** Magnitude efek zona tempo kecil dan tidak praktis signifikan
>
> **H₁:** Effect size praktis signifikan, dengan **Cohen's d ≥ 0.5** ATAU **percentage difference ≥ 15%**
>
> **Uji:** Effect size calculation + interpretation guidelines

---

### **H4: Utilitas Prediktif (Predictive Utility)**
> **H₀:** Menambahkan fitur tempo zone tidak meningkatkan akurasi model ML
>
> **H₁:** Model ML dengan tempo zone feature meningkatkan akurasi **minimal +5%** dibanding baseline
>
> **Uji:** Model comparison (baseline vs enhanced) + McNemar's test

---

# SLIDE 26: HUBUNGAN ANTAR HIPOTESIS

## Logical Dependency

```
        H1: Ada efek signifikan?
              ↓
            [YES]
              ↓
    H2: Efeknya universal (konsisten)?
              ↓
            [YES]
              ↓
    H3: Efeknya praktis besar?
              ↓
            [YES]
              ↓
    H4: Efeknya berguna untuk ML?
              ↓
          [EXPECTED: YES]
              ↓
    CONCLUSION: Zona tempo universal
    100-120 BPM TERBUKTI & BERGUNA
```

### **Catatan:**
- H1, H2, H3 = **validasi ilmiah** (BAB III: statistical testing)
- H4 = **validasi pragmatis** (BAB III: ML modeling)
- Semua hipotesis saling mendukung untuk **main thesis**

---

# SLIDE 27: KESIMPULAN BAB I & II

## Ringkasan BAB I: PENDAHULUAN

✅ **Latar Belakang:** Era digital music → Big Data opportunity, tempo = underrated variable
✅ **Rumusan Masalah:** 5 pertanyaan penelitian (efek, konsistensi, magnitude, interaksi, utilitas)
✅ **Tujuan:** 5 target (identifikasi, evaluasi, kuantifikasi, analisis, modeling)
✅ **Manfaat:** Teoretis (bukti empiris) + Praktis (guideline produksi)
✅ **Batasan:** Dataset (Spotify), metodologi (correlational), generalisasi (Western-centric)
✅ **Asumsi:** 6 asumsi metodologis (validitas data, representativeness, dll)

---

## Ringkasan BAB II: KAJIAN PUSTAKA

✅ **Teori 1 - MIR:** Framework ekstraksi audio features untuk hit prediction
✅ **Teori 2 - Big Data:** 3V (volume, velocity, variety) → statistical power tinggi
✅ **Teori 3 - Persepsi Tempo:** Biological resonance (100-120 BPM = natural tempo)
✅ **Teori 4 - Neuroscience:** Basal ganglia activation optimal di medium tempo
✅ **Studi Terdahulu:** 4 studi (Percino, Interiano, Ni, Van Dyck) → gaps identified
✅ **Kerangka Berpikir:** Logical flow dari input → kategorisasi → analisis → validasi
✅ **Hipotesis:** 4 hipotesis (H1-H4) dengan dependency logic

---

# SLIDE 28: NEXT STEPS

## Rencana ke Depan

### **Minggu Depan (Setelah Presentasi Ini):**
- Finalisasi BAB III: METODE PENELITIAN
  - Detail prosedur pengumpulan data
  - Instrumen penelitian (Python libraries)
  - Teknik analisis data (step-by-step)
  - Kriteria keputusan & interpretasi

### **2 Minggu Mendatang:**
- Eksekusi analisis statistik (t-test, ANOVA, effect size)
- Dokumentasi hasil preliminary findings lengkap
- Persiapan visualisasi data

### **1 Bulan Mendatang:**
- Machine learning model development
- Model comparison & evaluation
- Synthesis findings untuk BAB IV & V

---

# SLIDE 29: PERTANYAAN & DISKUSI

## Terima Kasih

### **Kontak:**
📧 Email: [email@mahasiswa.unesa.ac.id]
💻 Repository: [link jika ada]

---

### **Siap untuk pertanyaan!**

---

# SLIDE 30: BACKUP - ANTISIPASI PERTANYAAN

## Q&A Preparation

### **Q1: "Kenapa fokus ke tempo? Bukannya genre/lyrics lebih penting?"**
**A:** Tempo dipilih karena:
1. **Underrated** - Jarang dianalisis sebagai zona kategoris
2. **Universal candidate** - Biological basis (walking pace, heart rate)
3. **Actionable** - Easy to manipulate untuk produser musik
4. **Novel** - Belum ada studi Big Data cross-mood

Genre/lyrics memang penting, tapi fokus penelitian ini: **discover & validate underrated pattern**

---

### **Q2: "Dataset Spotify bias ke Western music, bagaimana generalisasi?"**
**A:** 
- **Acknowledge limitation** - memang ada bias Western
- **Mitigasi:** Dataset 100 tahun, multi-genre → reasonably diverse
- **Scope:** Penelitian ini about **global popular music** (predominantly Western)
- **Future work:** Cross-cultural validation (Asia, Latin America, Africa)

Temuan applicable untuk **mainstream music market**, not claim universal across all cultures

---

### **Q3: "Tempo sweet spot bisa berubah over time, data 1920-2020 terlalu lebar?"**
**A:**
- **Good point!** Temporal change is possible
- **Mitigasi:** Bisa lakukan subgroup analysis per decade (future analysis)
- **Hypothesis:** Biological basis (walking pace, heart rate) = relatively **stable** across time
- **Validation:** Check if pattern consistent di recent decades (2010-2020) vs old (1920-1960)

If temporal change significant → masuk discussion, suggest longitudinal study

---

### **Q4: "Rule-based mood categorization kurang akurat, kenapa tidak pakai manual annotation?"**
**A:**
- **Manual annotation:** Ideal but **not feasible** untuk 1.2M tracks (resource constraint)
- **Rule-based (energy × valence):** Established method di MIR literature
- **Trade-off:** Sacrifice precision for coverage (Big Data requires automation)
- **Validation:** Check if mood distribution make sense (e.g., "Sad Slow" largest = reasonable)

Acknowledge as limitation, suggest future work with subset manual validation

---

### **Q5: "Hipotesis 4 (ML improvement +5%) terlalu ambisius?"**
**A:**
- **+5% absolute improvement** = reasonable target (not overly ambitious)
- **Context:** State-of-the-art = 83-86% accuracy, +5% → ~88-91%
- **Precedent:** Feature engineering improvements di literature often 3-8%
- **Fallback:** Even if <5%, **any significant improvement** (p<0.05) still validates utility

Focus bukan cuma accuracy number, tapi **demonstrate practical value** of tempo zone feature

---

# SLIDE 31: BACKUP - DEFINISI ISTILAH

## Glossary

### **BPM (Beats Per Minute)**
Satuan pengukuran tempo musik. Jumlah beat (ketukan) dalam satu menit.

### **Hit Probability**
Probabilitas relatif suatu lagu menjadi populer. Composite metric dari popularity, danceability, energy, dan balanced valence.

### **Effect Size (Cohen's d)**
Ukuran magnitude perbedaan antara dua grup, independent dari sample size. Interpretasi: small (<0.5), medium (0.5-0.8), large (>0.8).

### **Cross-Mood Validation**
Stratified analysis untuk mengecek apakah pattern konsisten di berbagai kategori mood.

### **Two-Way ANOVA**
Analisis varians dengan 2 faktor independen (tempo zone × mood) untuk test interaction effect.

### **Entrainment**
Fenomena sinkronisasi biologis dengan external rhythm (e.g., foot-tapping dengan musik).

---

# 🎓 END OF PRESENTATION (BAB I & II)

**Terima kasih atas perhatiannya! 🙏**

---

# PANDUAN PRESENTASI

## Alokasi Waktu (Total: 20-25 menit)

### **BAB I: PENDAHULUAN (10 menit)**
- Slide 3-6 (Latar Belakang): 4 menit
- Slide 7 (Rumusan Masalah): 1.5 menit
- Slide 8 (Tujuan): 1.5 menit
- Slide 9-10 (Manfaat): 2 menit
- Slide 11-12 (Batasan & Asumsi): 1 menit

### **BAB II: KAJIAN PUSTAKA (10 menit)**
- Slide 13-18 (Kajian Teori): 4 menit
- Slide 19-23 (Penelitian Relevan & Gap): 4 menit
- Slide 24 (Kerangka Berpikir): 1 menit
- Slide 25-26 (Hipotesis): 1 menit

### **PENUTUP (2 menit)**
- Slide 27 (Kesimpulan): 1 menit
- Slide 28 (Next Steps): 1 menit

### **Q&A: 5-10 menit**

---

## Tips Presentasi

### **DO:**
✅ Mulai dengan **hook** - "1.2 juta lagu, 1 pertanyaan: apa yang bikin lagu populer?"
✅ **Emphasize novelty** - "Belum ada yang test universal tempo zone di Big Data scale"
✅ **Connect theory to practice** - "Biological basis → practical guidelines"
✅ **Confident delivery** - Kamu sudah riset mendalam, you know your stuff!
✅ **Eye contact** dengan dosen penguji

### **DON'T:**
❌ Jangan baca slides word-by-word
❌ Jangan terburu-buru (pace yang tenang)
❌ Jangan skip theoretical foundation (penting untuk justify hipotesis)
❌ Jangan defensif kalau ditanya (terima kritik dengan baik)

---

## Cara Convert ke PowerPoint

### **Metode 1: Pandoc**
```powershell
pandoc MATERI_PPT_BAB1_BAB2.md -o SEMPRO_BAB1_BAB2.pptx
```

### **Metode 2: Manual**
1. Copy tiap slide
2. Paste di PowerPoint
3. Apply template UNESA

**Good luck! 🚀**
