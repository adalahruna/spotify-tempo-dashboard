# 🎓 MATERI PRESENTASI SEMINAR PROPOSAL
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

**Tahun 2026**

---

# SLIDE 2: OUTLINE PRESENTASI

## Agenda Presentasi

1. **Latar Belakang & Motivasi**
2. **Rumusan Masalah**
3. **Tujuan Penelitian**
4. **Tinjauan Pustaka**
5. **Metodologi Penelitian**
6. **Temuan Awal (Preliminary Findings)**
7. **Timeline & Rencana Kerja**
8. **Kontribusi Penelitian**
9. **Penutup & Q&A**

---

# SLIDE 3: LATAR BELAKANG (1/3)

## Fenomena Industri Musik Digital

### 📊 **Ledakan Data Musik**
- Spotify: 100+ juta tracks
- Apple Music: 100+ juta tracks
- YouTube Music: 80+ juta tracks

### 🎵 **Pertanyaan Fundamental:**
> *"Apa yang membuat sebuah lagu menjadi populer?"*

### 🔬 **Gap Penelitian:**
- Banyak studi fokus pada **genre-specific** patterns
- Belum ada studi **large-scale** tentang pola tempo universal
- Tempo sering diabaikan sebagai "fitur sederhana"

---

# SLIDE 4: LATAR BELAKANG (2/3)

## Paradigma Lama vs Baru

| Paradigma Lama | Paradigma Baru (Penelitian Ini) |
|----------------|----------------------------------|
| Tempo = pilihan genre/mood | **Tempo = pola universal?** |
| Fast tempo → energi tinggi | **Medium tempo → universal appeal** |
| Slow tempo → sedih | **100-120 BPM optimal untuk semua?** |
| Analisis per-genre terpisah | **Cross-mood analysis** |
| Dataset kecil (<10k tracks) | **Big Data (1.2M+ tracks)** |

### 💡 **Hipotesis Underrated:**
> Apakah ada "sweet spot" tempo yang **secara universal** meningkatkan popularitas, terlepas dari mood musik?

---

# SLIDE 5: LATAR BELAKANG (3/3)

## Motivasi Penelitian

### 🧠 **Theoretical Motivation:**
- **Biological resonance hypothesis:** Tempo 100-120 BPM ~ human walking pace + heart rate
- Neuroscience: Basal ganglia response optimal di rentang ini
- Music psychology: Preferred tempo theory (Fraisse, 1982; Moelants, 2002)

### 🎯 **Practical Motivation:**
- **Produser musik:** Guideline evidence-based untuk tempo selection
- **Platform streaming:** Optimize playlist curation
- **Music AI:** Enhanced recommendation systems

### 📈 **Scientific Motivation:**
- Validate universal pattern dengan Big Data scale
- Quantify effect size (bukan hanya p-value)
- Demonstrate actionable ML application

---

# SLIDE 6: RUMUSAN MASALAH

## 5 Pertanyaan Penelitian

1. **Apakah ada zona tempo universal** dengan hit probability superior secara signifikan?

2. **Apakah pola ini konsisten** di seluruh kategori mood (happy, sad, angry, calm, melancholic)?

3. **Berapa besar magnitude efek?** (practical significance, bukan hanya statistical significance)

4. **Bagaimana tempo berinteraksi** dengan fitur audio lainnya (energy, valence, danceability)?

5. **Seberapa besar peningkatan akurasi** model ML jika menggunakan fitur tempo zone?

---

# SLIDE 7: TUJUAN PENELITIAN

## 5 Target Penelitian

1. ✅ **Identifikasi & validasi** zona tempo universal secara statistik ketat

2. ✅ **Evaluasi konsistensi** pola lintas 5 kategori mood

3. ✅ **Kuantifikasi magnitude** efek (Cohen's d, percentage difference)

4. ✅ **Analisis interaksi** tempo dengan fitur sekunder (energy, valence, dll)

5. ✅ **Membangun model ML** dan membandingkan performa (with vs without tempo zone)

---

# SLIDE 8: MANFAAT PENELITIAN

## Kontribusi Teoretis

✅ Bukti empiris **preferensi tempo universal** manusia (biological basis)
✅ Ekspansi teori persepsi musik (resonance hypothesis validation)
✅ Framework metodologis untuk **Big Data music analysis**
✅ Novel insight: tempo sebagai **universal feature** (genre-agnostic)

## Kontribusi Praktis

✅ **Guideline produksi musik:** Pilih 100-120 BPM untuk maximize hit potential
✅ **Insight kurator:** Optimize playlist dengan tempo sweet spot awareness
✅ **Enhanced ML features:** Tempo zone = fitur penting untuk recommendation
✅ **Data-driven decision:** Replace intuition dengan evidence

---

# SLIDE 9: TINJAUAN PUSTAKA (1/4)

## Teori 1: Music Information Retrieval (MIR)

### **Definisi:**
Ekstraksi informasi dari sinyal audio musik menggunakan computational methods

### **Audio Features Relevan:**
- **Tempo:** Kecepatan musik dalam Beats Per Minute (BPM)
- **Energy:** Intensitas perseptual (0-1 scale)
- **Valence:** Kepositifan emosional (0-1 scale)
- **Danceability:** Kesesuaian untuk menari (tempo + beat strength)

### **Aplikasi:**
Genre classification, mood detection, **hit prediction**, recommendation systems

---

# SLIDE 10: TINJAUAN PUSTAKA (2/4)

## Teori 2: Big Data Analytics + Teori 3V

### **3V of Big Data (Laney, 2001):**
- **Volume:** Dataset 1,204,022 tracks (massive scale)
- **Velocity:** Streaming data dari Spotify API
- **Variety:** 44 features (metadata + audio + derived)

### **Keuntungan Big Data:**
- **Statistical power tinggi** → margin of error minimal
- **Pattern identification** yang tak terlihat di studi kecil
- **Generalizability** findings across populations

### **Dataset Penelitian Ini:**
- 100 tahun data (1920-2020)
- Multi-genre, multi-mood
- Confidence interval sempit = presisi tinggi

---

# SLIDE 11: TINJAUAN PUSTAKA (3/4)

## Teori 3: Teori Persepsi Tempo & Respons Fisiologis

### **Preferred Tempo Theory (Fraisse, 1982):**
- Rentang 100-120 BPM = **natural tempo** manusia
- Paling mudah untuk synchronized movements

### **Biological Correspondence:**
- 100-120 BPM ≈ **2× walking pace** (60 steps/min × 2 kaki)
- Dekat dengan **resting heart rate** (60-100 BPM)

### **Neuroscience Evidence (Grahn & Brett, 2007):**
- Tempo medium → **basal ganglia activation** optimal
- Spontaneous foot-tapping, head-nodding

### **Entrainment (Van Dyck et al., 2017):**
- Running cadence spontaneously sync dengan musik 100-130 BPM
- Evidence: tempo affects physical movement

---

# SLIDE 12: TINJAUAN PUSTAKA (4/4)

## Penelitian Terdahulu & Gap Analysis

| Studi | Dataset | Fokus | Akurasi | Gap |
|-------|---------|-------|---------|-----|
| **Dhanaraj & Logan (2005)** | 1,700 songs | Acoustic + lyric features | Better than random | Small dataset |
| **Ni et al. (2011)** | UK Charts | Random Forest | 60-74% | Tempo = continuous variable |
| **Interiano et al. (2018)** | 500k songs | Temporal evolution | 86% | No explicit tempo zone test |
| **Dhar et al. (2019)** | Hybrid features | Audio + social signals | 83% | Genre-specific analysis |

### 🔴 **Research Gap:**
- ❌ Belum ada studi eksplisit test **universal tempo zone** (Big Data scale)
- ❌ Tempo dianalisis continuous atau genre-specific (bukan cross-mood categorical)
- ❌ Effect size quantification kurang (fokus p-value doang)
- ✅ **Penelitian ini:** Fill all gaps above!

---

# SLIDE 13: KERANGKA BERPIKIR

```
┌─────────────────────────────────────────────────────┐
│  INPUT: Spotify Dataset (1.2M tracks, 1920-2020)   │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  PREPROCESSING: Cleaning + Feature Engineering      │
│  • Remove duplicates, outliers                      │
│  • Extract tempo, energy, valence, etc.             │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  CATEGORIZATION:                                    │
│  • 5 Tempo Zones (very slow → very fast)            │
│  • 5 Mood Clusters (happy, sad, angry, calm, etc.)  │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  ANALYSIS:                                          │
│  • Cross-mood comparison                            │
│  • T-test, ANOVA, Effect Size                       │
│  • Identify universal pattern                       │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  VALIDATION:                                        │
│  • Statistical significance (p < 0.05)              │
│  • Practical significance (Cohen's d ≥ 0.5)         │
│  • Consistency check (5/5 moods)                    │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  APPLICATION: ML Prediction Model                   │
│  • Baseline vs Enhanced (with tempo zone)           │
│  • Compare accuracy improvement                     │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  OUTPUT: Universal Tempo Sweet Spot = 100-120 BPM   │
└─────────────────────────────────────────────────────┘
```

---

# SLIDE 14: HIPOTESIS PENELITIAN

## 4 Hipotesis (H1-H4)

### **H1: Efek Zona Tempo**
> Medium tempo (100-120 BPM) memiliki hit probability **signifikan lebih tinggi** dibandingkan zona tempo lainnya (p < 0.05)

### **H2: Konsistensi Lintas Mood**
> Pola ini **konsisten di semua** 5 kategori mood (happy, sad, angry, calm, melancholic)

### **H3: Magnitude Efek Praktis**
> Effect size praktis signifikan: **Cohen's d ≥ 0.5** ATAU **% difference ≥ 15%**

### **H4: Utilitas Prediktif**
> Model ML dengan tempo zone feature meningkatkan akurasi **minimal +5%**

---

# SLIDE 15: METODOLOGI (1/6) - Rancangan Penelitian

## Jenis Penelitian

**Mixed-Method Quantitative Study**
- Non-experimental correlational design
- Combining descriptive, inferential, and predictive analytics

## 4 Fase Sequential

```
FASE 1: Exploratory Discovery
  └─ Cari pola awal distribusi tempo vs hit probability

FASE 2: Confirmatory Statistical Testing
  └─ Validasi hipotesis (t-test, ANOVA, effect size)

FASE 3: Cross-Mood Validation
  └─ Verify consistency across 5 moods

FASE 4: Predictive Modeling
  └─ Build ML model, compare performance
```

---

# SLIDE 16: METODOLOGI (2/6) - Dataset

## Sumber Data: Spotify Music Dataset

### **Karakteristik:**
- **Source:** Spotify Web API (Kaggle by Rodolfo Figueroa)
- **Lisensi:** CC0 Public Domain
- **Total:** 1,204,022 tracks
- **Periode:** 1920-2020 (100 tahun)
- **Coverage:** Global, multi-genre

### **Features:**
- **24 original features:** metadata + audio features
- **20 derived features:** tempo zone, mood cluster, hit probability
- **44 total features**

### **File Size:** 500 MB (CSV) → 250 MB (Parquet compressed)

---

# SLIDE 17: METODOLOGI (3/6) - Variabel

## Variabel Independen: ZONA TEMPO

| Zona | Rentang BPM | Label | Karakteristik |
|------|-------------|-------|---------------|
| Very Slow | < 80 | very_slow | Ballads, ambient |
| Slow | 80-100 | slow | Chill, downtempo |
| **Medium** | **100-120** | **medium** | ⭐ **SWEET SPOT** |
| Fast | 120-140 | fast | Dance, pop |
| Very Fast | > 140 | very_fast | EDM, hardcore |

## Variabel Dependen: HIT PROBABILITY

**Formula:**
```
hit_probability = (popularity/100 × 0.4) + 
                  (danceability × 0.3) + 
                  (energy × 0.2) + 
                  (balanced_valence × 0.1)
```

**Range:** 0-1 (continuous, ratio scale)

---

# SLIDE 18: METODOLOGI (4/6) - Mood Cluster

## Variabel Kontrol: MOOD CLUSTER

Kategorisasi emosional berdasarkan **Energy × Valence**

| Mood | Rule | Contoh |
|------|------|--------|
| **Happy Energetic** | energy ≥ 0.6 AND valence ≥ 0.6 | "Happy" - Pharrell |
| **Sad Slow** | energy < 0.4 AND valence < 0.4 | "Someone Like You" - Adele |
| **Angry Intense** | energy ≥ 0.6 AND valence < 0.4 | Metal, aggressive rock |
| **Calm Positive** | energy < 0.6 AND valence ≥ 0.6 | "Isn't She Lovely" - Stevie Wonder |
| **Melancholic** | Middle ground | Indie, alternative |

### **Distribusi:**
- Sad Slow: 31.9%
- Melancholic: 19.8%
- Angry Intense: 19.0%
- Happy Energetic: 17.8%
- Calm Positive: 11.4%

---

# SLIDE 19: METODOLOGI (5/6) - Teknik Analisis

## Analisis Statistik

### **1. Descriptive Statistics**
- Distribusi frekuensi (tempo × mood)
- Mean, median, std, min, max per group
- Visualization: histogram, box plot, violin plot

### **2. Inferential Statistics**

**T-Test (H1):**
- Independent samples t-test
- Medium vs Others comparison
- α = 0.05

**ANOVA (H2):**
- One-way ANOVA (5 tempo zones)
- Post-hoc: Tukey HSD
- Two-way ANOVA (tempo × mood interaction)

**Effect Size (H3):**
- Cohen's d (standardized mean difference)
- Percentage difference
- Interpretation: small/medium/large

---

# SLIDE 20: METODOLOGI (6/6) - Machine Learning

## Predictive Modeling (H4)

### **Workflow:**

**1. Data Split:**
- Train: 80% (963,218 tracks)
- Test: 20% (240,804 tracks)
- Stratified by hit probability

**2. Baseline Model (Without Tempo Zone):**
- Features: energy, valence, danceability, loudness, acousticness, tempo (continuous)
- Algorithm: Random Forest
- Metric: Accuracy, Precision, Recall, F1, ROC-AUC

**3. Enhanced Model (With Tempo Zone):**
- Features: Baseline + `is_medium_tempo` (binary indicator)
- Same algorithm & metrics

**4. Comparison:**
- Δ Accuracy = Enhanced - Baseline
- McNemar's test (significance)
- Feature importance analysis

---

# SLIDE 21: TEMUAN AWAL (1/3)

## 🎯 Preliminary Findings: ZONA TEMPO SWEET SPOT UNIVERSAL!

| Mood Category | Best Tempo | Hit Prob | Sample Size | Status |
|---------------|------------|----------|-------------|--------|
| **Happy Energetic** | **Medium** | 0.7624 | 49,245 | ✅ |
| **Sad Slow** | **Medium** | 0.3626 | 77,279 | ✅ |
| **Angry Intense** | **Medium** | 0.6363 | 49,313 | ✅ |
| **Calm Positive** | **Medium** | 0.5561 | 36,166 | ✅ |
| **Melancholic** | **Medium** | 0.6067 | 54,772 | ✅ |

### 🏆 **HASIL: 5/5 MOODS PREFER MEDIUM TEMPO!**

---

# SLIDE 22: TEMUAN AWAL (2/3)

## Statistical Validation Results

### **T-Test (Medium vs Others):**
```
t-statistic: 266.45
p-value: < 0.0001 (highly significant!)
df: 1,204,020
```
✅ **Reject H₀:** Ada perbedaan signifikan!

### **Effect Size:**
```
Cohen's d: 0.607 (MEDIUM EFFECT)
Percentage diff: +24.5%
```
✅ **Praktis signifikan!** (d ≥ 0.5, diff ≥ 15%)

### **Consistency Check:**
```
Universal pattern: 5/5 moods (100%)
Interaction effect: p = 0.18 (non-significant)
```
✅ **Mendukung universalitas!** (pattern tidak tergantung mood)

---

# SLIDE 23: TEMUAN AWAL (3/3)

## Visualisasi: Hit Probability by Tempo Zone

```
       ┌─────────────────────────────────────┐
  0.65 │              ▲                      │
       │              █                      │ Medium Tempo
  0.60 │            ┌─█─┐                    │ WINS!
       │            │ █ │                    │
  0.55 │         ┌──┤ █ ├──┐                 │
       │         │  │ █ │  │                 │
  0.50 │      ┌──┤  │ █ │  ├──┐              │
       │      │  │  │ █ │  │  │              │
  0.45 │   ┌──┤  │  │ █ │  │  ├──┐           │
       └──────────────────────────────────────┘
         Very  Slow Med Fast Very
         Slow            Fast
```

### **Key Insight:**
> "Medium tempo (100-120 BPM) mencapai peak hit probability di semua mood categories, dengan margin yang praktis signifikan (+24.5%)"

---

# SLIDE 24: DISTRIBUSI DATA

## Distribusi Zona Tempo (Dataset)

```
Very Slow (<80):      ████████████ 126,953 (10.5%)
Slow (80-100):        ████████████████████████ 258,657 (21.5%)
Medium (100-120):     █████████████████████████ 266,775 (22.2%) ⭐
Fast (120-140):       ██████████████████████████ 286,576 (23.8%)
Very Fast (>140):     █████████████████████████ 265,061 (22.0%)
```

### **Observasi:**
- Distribusi relatif **balanced** across zones
- Medium zone = 22.2% → representatif
- Tidak ada dominasi ekstrem (bias minimal)

---

# SLIDE 25: TIMELINE PENELITIAN

## Rencana Kerja 6 Bulan

| Bulan | Kegiatan | Output |
|-------|----------|--------|
| **1** | Literature review + Data acquisition | Dataset downloaded & documented |
| **2** | Data preprocessing + EDA | Cleaned data, descriptive stats |
| **3** | Feature engineering + Mood categorization | Enriched dataset (44 features) |
| **4** | Statistical testing + Validation | H1-H3 validated, effect size computed |
| **5** | ML model development + Evaluation | H4 validated, model comparison |
| **6** | Synthesis + Report writing | Thesis draft, journal article draft |

### **Milestone:**
- **Bulan 2:** Temuan awal (preliminary findings) ✅ **DONE**
- **Bulan 4:** Statistical validation complete
- **Bulan 6:** Thesis submission ready

---

# SLIDE 26: KONTRIBUSI PENELITIAN

## Novelty & Contributions

### **Kontribusi Teoretis:**
1. ✅ **Bukti empiris pertama** pola tempo universal di Big Data scale (1.2M tracks)
2. ✅ **Validasi biological resonance hypothesis** dengan cross-mood consistency
3. ✅ **Framework metodologis** untuk music analytics dengan categorical tempo zones
4. ✅ **Quantified effect size** (bukan hanya p-value)

### **Kontribusi Praktis:**
1. ✅ **Guideline produksi musik:** "Use 100-120 BPM for maximum hit potential"
2. ✅ **Enhanced ML features:** Tempo zone sebagai categorical predictor
3. ✅ **Playlist optimization:** Kurasi dengan tempo sweet spot awareness
4. ✅ **Data-driven decision making** untuk industri kreatif

### **Kontribusi Metodologis:**
1. ✅ **Big Data + rigorous statistics** (tidak hanya ML black box)
2. ✅ **Multi-level validation** (descriptive → inferential → predictive)
3. ✅ **Reproducible research** (dataset publik, code available)

---

# SLIDE 27: EXPECTED OUTCOMES

## Target Luaran Penelitian

### **Publikasi:**
- 📄 **Thesis/Tugas Akhir** (primary outcome)
- 📄 **Jurnal nasional terakreditasi** (target: Sinta 2-3)
- 📄 **Conference paper** (target: ICACSIS/ICoDSA/similar)

### **Software/Tools:**
- 💻 **Python scripts** (open source di GitHub)
- 📊 **Interactive dashboard** (visualisasi temuan)
- 📝 **Reproducible notebooks** (Jupyter)

### **Knowledge Products:**
- 📖 **Guideline untuk musisi** (practical handbook)
- 🎓 **Teaching materials** (untuk MIR courses)
- 📺 **Public talk/webinar** (disseminasi ke industri)

---

# SLIDE 28: CHALLENGES & LIMITATIONS

## Keterbatasan Penelitian

### **Batasan Dataset:**
- Spotify-centric (tidak termasuk platform lain)
- Western music bias (global tapi dominan Barat)
- Popularity ≠ quality (commercial success bias)

### **Batasan Metodologis:**
- Correlational study (bukan causal)
- Mood categorization = rule-based (bukan ground truth)
- Hit probability = composite metric (simplified)

### **Batasan Generalisasi:**
- Genre baru (TikTok viral) mungkin berbeda
- Temporal changes (preference bisa evolve)
- Cultural differences (need cross-cultural study)

### **Mitigasi:**
- Acknowledge limitations di discussion
- Suggest future research directions
- Validate dengan dataset tambahan (jika ada)

---

# SLIDE 29: FUTURE RESEARCH DIRECTIONS

## Arah Penelitian Lanjutan

### **Ekspansi Dataset:**
- ✅ Include multiple platforms (Apple Music, YouTube)
- ✅ Cross-cultural validation (Asia, Latin America, Africa)
- ✅ Real-time streaming data (dynamic popularity)

### **Metodologi Lanjutan:**
- ✅ Deep learning models (CNN, Transformer)
- ✅ Causal inference (counterfactual analysis)
- ✅ Temporal evolution (how sweet spot changes over decades)

### **Aplikasi Lanjutan:**
- ✅ Real-time hit prediction API
- ✅ Music production assistant tool
- ✅ Personalized tempo recommendation (individual preference)

### **Interdisciplinary:**
- ✅ Neuroscience collaboration (fMRI studies)
- ✅ Music therapy applications
- ✅ Sports science (workout playlist optimization)

---

# SLIDE 30: KESIMPULAN

## Rangkuman Proposal

### ✅ **Masalah:** Belum ada studi Big Data tentang pola tempo universal

### ✅ **Hipotesis:** Tempo 100-120 BPM = sweet spot universal

### ✅ **Metode:** 4-phase mixed quantitative (1.2M tracks, t-test, ANOVA, effect size, ML)

### ✅ **Temuan Awal:** 5/5 moods prefer medium tempo (+24.5%, p<0.0001, d=0.607)

### ✅ **Kontribusi:** Teoretis (bukti empiris), Praktis (guideline produksi), Metodologis (framework)

### 🎯 **Implikasi:**
> "Produser musik sekarang punya evidence-based guideline: **pilih 100-120 BPM untuk maximize hit potential, regardless of mood**"

---

# SLIDE 31: PENUTUP

## Terima Kasih

### **Pertanyaan & Diskusi**

📧 Email: [email@mahasiswa.unesa.ac.id]
💻 GitHub: [github.com/username/tempo-sweet-spot]
📄 Proposal lengkap: [link Google Docs]

---

### **Key References:**
1. Interiano et al. (2018) - Musical trends 500k songs
2. Grahn & Brett (2007) - Neuroscience of beat perception
3. Moelants (2002) - Preferred tempo theory
4. Van Dyck et al. (2017) - Spontaneous entrainment

---

**"Music is science. Data doesn't lie. 5/5 moods prefer medium tempo."**

---

# SLIDE 32: BACKUP - Q&A PREPARATION

## Antisipasi Pertanyaan Dosen

### **Q1: "Kenapa tidak pakai deep learning?"**
**A:** Fokus penelitian ini pada **discovery & validation** pola tempo universal, bukan maximize prediction accuracy. Random Forest dipilih karena interpretable (feature importance) dan sufficient untuk validate hypothesis. Deep learning bisa jadi future work.

### **Q2: "Bagaimana dengan genre baru seperti hyperpop?"**
**A:** Dataset cover 1920-2020, termasuk genre emerging. Hyperpop biasanya masuk "very fast" zone. Temuan universal pattern tidak meniadakan outliers—ini tentang **general trend** di populasi besar.

### **Q3: "Popularity bukan ukuran kualitas musik, biased!"**
**A:** Setuju. Tapi penelitian ini tentang **commercial success prediction**, bukan artistic quality. Hit probability = proxy untuk market performance. Acknowledge limitation di thesis.

### **Q4: "Cohen's d = 0.607 itu medium, kenapa klaim 'strong effect'?"**
**A:** Cohen's d=0.607 dikombinasi dengan **+24.5% percentage difference** = praktis signifikan. Dalam konteks industri musik, 24.5% improvement = substantial impact (jutaan streams).

### **Q5: "Bagaimana generalisasi ke musik tradisional/daerah?"**
**A:** Dataset ini Spotify-centric (Western-dominant). Untuk musik tradisional, perlu studi terpisah. Ini limitation yang akan didiscuss. Suggestion: cross-cultural validation sebagai future work.

---

# SLIDE 33: BACKUP - TECHNICAL DETAILS

## Detail Teknis (jika ditanya)

### **Computing Environment:**
- Python 3.10+, Jupyter Notebook
- Libraries: pandas, numpy, scipy, scikit-learn
- Hardware: 16 GB RAM, Intel Core i5+
- Processing time: ~2 hours (full pipeline)

### **Statistical Software:**
- scipy.stats (t-test, ANOVA)
- statsmodels (post-hoc tests)
- scikit-learn (ML models)

### **Data Storage:**
- Raw: 500 MB (CSV)
- Processed: 250 MB (Parquet compressed)
- Backup: Cloud storage (Google Drive)

### **Reproducibility:**
- All code versioned (Git)
- Random seed fixed (42)
- Environment documented (requirements.txt)

---

# SLIDE 34: BACKUP - ADDITIONAL VISUALIZATIONS

## Supporting Visualizations

### **Available Plots:**
1. **Distribution plots:**
   - Tempo distribution histogram
   - Hit probability distribution per zone
   - Mood cluster distribution

2. **Comparison plots:**
   - Box plots (tempo zones vs hit prob)
   - Violin plots (show full distribution)
   - Grouped bar charts (per mood)

3. **Correlation analysis:**
   - Heatmap (features correlation)
   - Scatter plots (tempo vs other features)

4. **ML results:**
   - ROC curves (baseline vs enhanced)
   - Feature importance bar chart
   - Confusion matrix

---

# SLIDE 35: BACKUP - REFERENCES

## Referensi Utama

1. **Interiano, M., et al. (2018).** Musical trends and predictability. *Royal Society Open Science*, 5(5), 171274.

2. **Grahn, J. A., & Brett, M. (2007).** Rhythm and beat perception in motor areas. *Journal of Cognitive Neuroscience*, 19(5), 893-906.

3. **Moelants, D. (2002).** Preferred tempo reconsidered. *ICMPC7*, 580-583.

4. **Van Dyck, E., et al. (2017).** Spontaneous entrainment of running cadence. *Sports Medicine - Open*, 3, 15.

5. **Dhar, S., et al. (2019).** Music popularity prediction with hybrid features. *Expert Systems with Applications*, 133, 11-20.

**Total: 13 referensi** (lihat proposal lengkap)

---

# 🎓 END OF PRESENTATION

**Semoga sukses sempro! 🚀**

---

# PANDUAN PENGGUNAAN PPT

## Cara Convert Markdown ke PowerPoint:

### **Metode 1: Pandoc (Recommended)**
```powershell
pandoc MATERI_PPT_SEMPRO.md -o SEMPRO_PRESENTATION.pptx
```

### **Metode 2: Marp (Markdown Presentation)**
1. Install Marp: https://marp.app/
2. Open `MATERI_PPT_SEMPRO.md` di Marp
3. Export to PowerPoint

### **Metode 3: Manual Copy-Paste**
1. Copy tiap slide
2. Paste di PowerPoint
3. Apply design template

---

## Tips Presentasi:

1. **Durasi:** 20-25 menit (15 menit present + 5-10 menit Q&A)
2. **Slide utama:** 1-31 (slide 32-35 = backup)
3. **Fokus:** Slide 21-23 (temuan awal) = highlight!
4. **Practice:** Minimal 3x sebelum sempro
5. **Confidence:** Kamu punya data kuat (1.2M tracks, p<0.0001)!

---

## Struktur Waktu Ideal:

- Intro (Slide 1-5): 3 menit
- Masalah & Tujuan (Slide 6-8): 2 menit
- Tinjauan Pustaka (Slide 9-14): 4 menit
- Metodologi (Slide 15-20): 4 menit
- **Temuan Awal (Slide 21-24): 5 menit** ⭐ (PALING PENTING!)
- Timeline & Kontribusi (Slide 25-29): 3 menit
- Penutup (Slide 30-31): 2 menit
- Q&A: 5-10 menit

**Total: ~23 menit present + 7 menit Q&A = 30 menit**
