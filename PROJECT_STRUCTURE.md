# 📁 PROJECT STRUCTURE - Spotify Music Recommendation System

**Complete Folder Organization & File Index**

---

## 🌳 Complete Directory Tree

```
d:\Semester 5\BIG DATA\Project\
│
├── 📄 README.md                        Main project README
├── 📄 PROJECT_STRUCTURE.md             This file - Complete structure guide
├── 📄 requirements.txt                 Python dependencies
├── 📄 .gitignore                       Git ignore rules
├── 📄 .env.example                     Environment variables template
│
├── 🚀 Deployment Files
│   ├── Procfile                        Railway/Heroku process file
│   ├── railway.json                    Railway configuration
│   ├── vercel.json                     Vercel configuration (unused)
│   ├── wsgi.py                         WSGI application entry point
│   ├── gunicorn_config.py              Gunicorn server config
│   ├── runtime.txt                     Python version specification
│   ├── START_DASHBOARD.bat             Windows startup script
│   └── STOP_DASHBOARD.bat              Windows stop script
│
├── 🗄️ api/                             Backend API (Flask)
│   ├── __init__.py                     Package initializer
│   ├── search_api.py                   Main API server (combined endpoints)
│   ├── recommendation_api.py           Recommendation logic (blueprint)
│   └── config.py                       API configuration
│
├── 🎨 dashboard/                       Frontend (HTML/CSS/JS)
│   ├── index.html                      Main dashboard page
│   ├── recommend.html                  Recommendation interface
│   ├── app.js                          Dashboard JavaScript
│   ├── styles.css                      Custom styles (if any)
│   └── assets/                         Images, icons (if any)
│
├── 🗃️ data/                             Raw & Processed Data
│   ├── spotify_tracks_raw.csv          Original 1.2M tracks (not in repo)
│   ├── processed/                      Cleaned data
│   └── sample/                         Sample datasets for testing
│
├── 📚 docs/                             Documentation Hub
│   ├── README.md                       Documentation index (detailed)
│   ├── COMPLETE_DOCUMENTATION.md       Master documentation
│   ├── DASHBOARD_FEATURES.md           Dashboard features guide
│   ├── KEY_FINDINGS.md                 Research findings
│   │
│   ├── architecture/                   📐 System Design
│   │   ├── ARCHITECTURE.md             System architecture
│   │   ├── METHODOLOGY.md              Research methodology
│   │   ├── RECOMMENDATION_SCORING_ALGORITHM.md  Scoring algorithm
│   │   ├── CONVERSATIONAL_RECOMMENDATION_DESIGN.md  UX design (EN)
│   │   └── CONVERSATIONAL_RECOMMENDATION_INDO.md  UX design (ID)
│   │
│   ├── deployment/                     🚀 Deployment Guides
│   │   └── RAILWAY_SETUP_MANUAL.md     Railway deployment
│   │
│   ├── journal/                        📄 Academic Journal
│   │   ├── JINACS_Spotify_Music_Recommendation_System.md  Full article
│   │   ├── VISUAL_CHECKLIST.md         Figures & tables checklist
│   │   │
│   │   ├── templates/                  📋 Format templates
│   │   │   └── jinacs_template         JINACS format specs
│   │   │
│   │   ├── screenshots/                📸 Dashboard screenshots
│   │   │   ├── fig2_dashboard_overview.png
│   │   │   ├── fig3_top_tracks.png
│   │   │   ├── fig4_tempo_distribution.png
│   │   │   ├── fig5_step1_mood.png
│   │   │   ├── fig6_step2_activity.png
│   │   │   ├── fig7_step3_intensity.png
│   │   │   ├── fig8_step4_artist.png
│   │   │   └── fig9_results.png
│   │   │
│   │   └── diagrams/                   🎨 Architecture diagrams
│   │       └── fig1_architecture.png
│   │
│   ├── machine-learning/               🤖 ML Documentation
│   │   ├── ML_INTEGRATION.md           ML integration plan
│   │   ├── ML_MODELS.md                Model specifications
│   │   └── ML_RECOMMENDATION_PLAN.md   ML strategy
│   │
│   ├── presentation/                   🎤 Presentation Materials
│   │   ├── PRESENTASI_CHEAT_SHEET.md   Quick reference
│   │   ├── PRESENTATION_SCRIPT.md      Full script
│   │   └── QUICK_DEMO.md               Demo guide
│   │
│   ├── testing/                        🧪 Testing & Validation
│   │   ├── TESTING_GUIDE.md            Test procedures
│   │   ├── TEST_SECTIONS.md            Test coverage
│   │   ├── DATA_FEASIBILITY_CHECK.md   Data validation
│   │   └── VALIDATION_REPORT_*.txt     Test results
│   │
│   └── thesis/                         🎓 Thesis Documents
│       ├── THESIS_DEFENSE_STRATEGY.md  Defense prep
│       └── FINAL_CHECKLIST.md          Submission checklist
│
├── 📓 markdown_files/                   Markdown Documentation
│   ├── KLARIFIKASI_HIPOTESIS.md        Hypothesis clarification
│   └── [other markdown files]
│
├── 🤖 models/                           ML Models (future)
│   ├── collaborative_filtering/        CF models
│   ├── neural_networks/                Deep learning models
│   └── trained/                        Saved model weights
│
├── 📊 notebooks/                        Jupyter Notebooks
│   ├── exploratory_analysis.ipynb      Data exploration
│   ├── feature_engineering.ipynb       Feature analysis
│   ├── model_training.ipynb            ML training (future)
│   └── visualization.ipynb             Data visualization
│
├── 🛠️ scripts/                          Utility Scripts
│   ├── import_data.py                  Database import script
│   ├── create_views.sql                SQL view creation
│   ├── test_queries.sql                Query testing
│   └── backup_db.sh                    Database backup
│
├── 🗄️ sql/                              SQL Scripts
│   ├── create_top_tracks_view.sql      Materialized view
│   ├── create_tables.sql               Table schemas
│   ├── insert_popular_artists.sql      Artist whitelist
│   └── indexes.sql                     Database indexes
│
└── 📈 visualizations/                   Generated Visualizations
    ├── tempo_distribution.png          Tempo zone charts
    ├── feature_correlations.png        Feature analysis
    └── performance_metrics.png         System performance
```

---

## 📂 Folder Descriptions

### 🚀 Root Level Files

| File | Purpose | When to Use |
|------|---------|------------|
| `README.md` | Project overview, quick start | First thing to read |
| `PROJECT_STRUCTURE.md` | Complete file organization | Finding specific files |
| `requirements.txt` | Python dependencies | Installation |
| `.env.example` | Environment template | Configuration setup |
| `Procfile` | Deployment process | Railway/Heroku deploy |
| `wsgi.py` | WSGI entry point | Production server |

### 🗄️ `/api` - Backend API

**Purpose:** Flask REST API server

| File | Lines | Purpose |
|------|-------|---------|
| `search_api.py` | ~400 | Main API server, all endpoints |
| `recommendation_api.py` | ~700 | Recommendation logic blueprint |
| `config.py` | ~50 | Database & server config |

**Key Endpoints:**
- `GET /api/top-tracks` - Curated tracks
- `POST /api/recommend` - Music recommendations
- `GET /api/artists/search` - Artist autocomplete

### 🎨 `/dashboard` - Frontend

**Purpose:** Web-based user interface

| File | Lines | Purpose |
|------|-------|---------|
| `index.html` | ~600 | Main dashboard page |
| `recommend.html` | ~800 | Recommendation interface |
| `app.js` | ~1000 | Dashboard logic & API calls |

**Technologies:**
- HTML5 + Tailwind CSS
- Vanilla JavaScript
- Material Symbols icons

### 🗃️ `/data` - Datasets

**Purpose:** Raw and processed data storage

**Note:** Large datasets (1.2M tracks CSV) are NOT in Git repo.  
Use PostgreSQL database instead.

**Structure:**
```
data/
├── spotify_tracks_raw.csv      (1.2M rows, ~300MB) - NOT in repo
├── processed/
│   └── cleaned_tracks.csv      (optional)
└── sample/
    └── sample_1000.csv         (for testing)
```

### 📚 `/docs` - Documentation

**Purpose:** Complete project documentation

**Organization:**
- `architecture/` - System design & algorithms
- `deployment/` - Production deployment guides
- `journal/` - Academic journal article
- `machine-learning/` - ML documentation
- `presentation/` - Presentation materials
- `testing/` - Test procedures & results
- `thesis/` - Thesis defense documents

**See:** `docs/README.md` for detailed index

### 📓 `/markdown_files` - Markdown Docs

**Purpose:** Additional markdown documentation

**Contents:**
- Hypothesis clarifications
- Research notes
- Meeting minutes

### 🤖 `/models` - ML Models

**Purpose:** Machine learning model storage (future)

**Structure:**
```
models/
├── collaborative_filtering/
│   ├── user_item_matrix.pkl
│   └── trained_model.pkl
├── neural_networks/
│   ├── audio_embeddings.h5
│   └── recommendation_nn.h5
└── trained/
    └── [saved model weights]
```

### 📊 `/notebooks` - Jupyter Notebooks

**Purpose:** Data exploration & analysis

**Notebooks:**
- `exploratory_analysis.ipynb` - Dataset exploration
- `feature_engineering.ipynb` - Feature analysis
- `visualization.ipynb` - Data visualization
- `model_training.ipynb` - ML experiments (future)

### 🛠️ `/scripts` - Utility Scripts

**Purpose:** Automation & maintenance scripts

| Script | Purpose |
|--------|---------|
| `import_data.py` | Import CSV to PostgreSQL |
| `create_views.sql` | Create materialized views |
| `test_queries.sql` | Test SQL queries |
| `backup_db.sh` | Database backup |

### 🗄️ `/sql` - SQL Scripts

**Purpose:** Database schema & queries

| File | Purpose |
|------|---------|
| `create_top_tracks_view.sql` | Materialized view (5K tracks) |
| `create_tables.sql` | Table schemas |
| `insert_popular_artists.sql` | Artist whitelist (50 artists) |
| `indexes.sql` | Performance indexes |

**Key View:** `top_tracks_view`
- Input: 1.2M raw tracks
- Output: 5K curated tracks
- Performance: 100x faster queries

### 📈 `/visualizations` - Generated Charts

**Purpose:** Exported visualization images

**Contents:**
- Tempo distribution charts
- Feature correlation heatmaps
- Performance comparison graphs

---

## 🎯 File Navigation by Task

### Task: "Start Development"
```
1. Read: README.md
2. Setup: .env.example → .env
3. Install: pip install -r requirements.txt
4. Run: python api/search_api.py
5. Open: http://localhost:8000
```

### Task: "Understand Architecture"
```
1. docs/architecture/ARCHITECTURE.md
2. docs/architecture/METHODOLOGY.md
3. docs/COMPLETE_DOCUMENTATION.md
```

### Task: "Implement Recommendation"
```
1. docs/architecture/RECOMMENDATION_SCORING_ALGORITHM.md
2. api/recommendation_api.py (lines 100-500)
3. sql/create_top_tracks_view.sql
```

### Task: "Deploy to Production"
```
1. docs/deployment/RAILWAY_SETUP_MANUAL.md
2. Procfile
3. railway.json
4. wsgi.py
```

### Task: "Write Journal Article"
```
1. docs/journal/JINACS_Spotify_Music_Recommendation_System.md (ready!)
2. docs/journal/VISUAL_CHECKLIST.md (todo: screenshots)
3. docs/journal/templates/jinacs_template (format guide)
```

### Task: "Prepare Presentation"
```
1. docs/presentation/PRESENTASI_CHEAT_SHEET.md
2. docs/presentation/QUICK_DEMO.md
3. docs/presentation/PRESENTATION_SCRIPT.md
```

### Task: "Thesis Defense"
```
1. docs/thesis/THESIS_DEFENSE_STRATEGY.md
2. docs/thesis/FINAL_CHECKLIST.md
3. docs/presentation/PRESENTASI_CHEAT_SHEET.md
```

---

## 📊 Statistics

### Code Files
| Type | Count | Total Lines |
|------|-------|------------|
| Python | 5 | ~1,500 |
| JavaScript | 2 | ~1,500 |
| HTML | 2 | ~1,400 |
| SQL | 4 | ~400 |
| **Total Code** | **13** | **~4,800** |

### Documentation Files
| Type | Count | Total Words |
|------|-------|------------|
| Markdown | 30+ | ~25,000 |
| Text | 2 | ~1,000 |
| **Total Docs** | **32+** | **~26,000** |

### Project Size
| Component | Size |
|-----------|------|
| Code Files | ~200 KB |
| Documentation | ~500 KB |
| Database (PostgreSQL) | ~2.5 GB |
| Total (excl. data) | ~700 KB |

---

## 🔍 Finding Specific Content

### "Where is the scoring algorithm?"
📂 `docs/architecture/RECOMMENDATION_SCORING_ALGORITHM.md`  
📂 `api/recommendation_api.py` (lines 300-500)

### "Where are the SQL views?"
📂 `sql/create_top_tracks_view.sql`

### "Where is the journal article?"
📂 `docs/journal/JINACS_Spotify_Music_Recommendation_System.md`

### "Where are the deployment configs?"
📂 `Procfile` (process file)  
📂 `railway.json` (Railway config)  
📂 `wsgi.py` (WSGI entry)  
📂 `gunicorn_config.py` (server config)

### "Where is the API documentation?"
📂 `docs/COMPLETE_DOCUMENTATION.md` (Section IV)  
📂 `api/search_api.py` (inline comments)

### "Where are the presentation materials?"
📂 `docs/presentation/` (all files)

### "Where is the architecture diagram?"
📂 `docs/journal/diagrams/` (need to create)  
Template: `docs/journal/VISUAL_CHECKLIST.md`

### "Where are the screenshots?"
📂 `docs/journal/screenshots/` (need to capture)  
Instructions: `docs/journal/VISUAL_CHECKLIST.md`

---

## ✅ File Checklist Status

### ✅ Complete
- [x] Core application code (API, Dashboard)
- [x] Database SQL scripts
- [x] Documentation (30+ files)
- [x] Journal article (6,500 words)
- [x] Deployment configurations
- [x] Testing guides

### 📸 In Progress
- [ ] Screenshots (8 needed)
- [ ] Architecture diagram (1 needed)

### 🚀 Future Enhancements
- [ ] ML models implementation
- [ ] Mobile application
- [ ] Real-time Spotify API
- [ ] User authentication

---

## 🛠️ Maintenance

### Adding New Files

**Documentation:**
```
1. Place in appropriate /docs subfolder
2. Update /docs/README.md index
3. Update this PROJECT_STRUCTURE.md
```

**Code:**
```
1. Follow existing structure (api/, dashboard/, sql/)
2. Add comments & docstrings
3. Update requirements.txt if needed
```

**Screenshots:**
```
1. Save in /docs/journal/screenshots/
2. Follow naming: fig#_description.png
3. Check VISUAL_CHECKLIST.md
```

### Cleaning Up

**Safe to delete:**
- `training_log.txt` (old training logs)
- `FILES_TO_PUSH.txt` (temporary file list)
- `/data/*.csv` (can re-import from database)

**Never delete:**
- `/api` (core backend)
- `/dashboard` (core frontend)
- `/sql` (database scripts)
- `/docs` (complete documentation)

---

## 📞 Quick Reference

**Start Development:**
```powershell
cd "d:\Semester 5\BIG DATA\Project"
python api/search_api.py
# Open: http://localhost:8000
```

**Run Tests:**
```powershell
pytest tests/
```

**Database Backup:**
```powershell
pg_dump spotify_music_db > backup.sql
```

**Deploy to Railway:**
```powershell
railway up
```

---

## 📌 Important Paths

### For Development:
- **API Server**: `api/search_api.py`
- **Frontend**: `dashboard/index.html`
- **Database**: `sql/create_top_tracks_view.sql`

### For Documentation:
- **Main Docs**: `docs/README.md`
- **Journal**: `docs/journal/JINACS_*.md`
- **Architecture**: `docs/architecture/`

### For Deployment:
- **Config**: `Procfile`, `railway.json`, `wsgi.py`
- **Guide**: `docs/deployment/RAILWAY_SETUP_MANUAL.md`

### For Presentation:
- **Cheat Sheet**: `docs/presentation/PRESENTASI_CHEAT_SHEET.md`
- **Demo**: `docs/presentation/QUICK_DEMO.md`

---

**Last Updated:** November 27, 2024  
**Project Status:** ✅ Production Ready  
**Documentation:** ✅ Complete  
**Journal:** 📝 Ready for Screenshot Integration

---

**🎓 Everything is organized and ready for thesis submission!** 📄✨
