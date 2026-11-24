# 🎵 Spotify Tempo Analysis Dashboard

**ML-Powered Music Analytics System**

Analyze 1.2 million Spotify tracks with 4 machine learning models predicting track success, danceability, and optimal tempo.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![ML](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![Deploy](https://img.shields.io/badge/Deploy-Railway%20%2B%20Vercel-blueviolet.svg)](https://railway.app/)

---

## 🚀 Features

- 📊 **1.2M Tracks Analysis** - 100 years of music data (1920-2020)
- 🤖 **4 ML Models** - 93% accuracy in popularity prediction
- 🎯 **6 Interactive Views** - Real-time data exploration
- ⚡ **Fast Predictions** - <2 seconds response time
- 🌍 **Global CDN** - Deployed on Vercel + Railway

---

## 🎨 Screenshots

### ML Predictions Dashboard
![Dashboard Preview](https://via.placeholder.com/800x400/006e2d/ffffff?text=ML+Predictions+Interface)

### Tempo Zone Analysis
![Tempo Zones](https://via.placeholder.com/800x400/006c49/ffffff?text=Tempo+Distribution+Analysis)

---

## 🏗️ Architecture

```
User → Vercel CDN → Railway API → PostgreSQL
              ↓
         Firebase Cache
```

**Tech Stack:**
- **Frontend:** HTML5, CSS3, JavaScript, Tailwind CSS
- **Backend:** Python 3.11, Flask, Gunicorn
- **Database:** PostgreSQL 18.6 (1.2M tracks)
- **ML:** scikit-learn, pandas, numpy
- **Deployment:** Vercel (frontend), Railway (backend)
- **Cache:** Firebase Firestore

---

## 🤖 Machine Learning Models

| Model | Algorithm | Accuracy | Use Case |
|-------|-----------|----------|----------|
| Popularity Predictor | Random Forest | **93.1% R²** | Predict track popularity (0-100) |
| Hit Classifier | Random Forest | **92.9% Acc** | Binary hit/flop classification |
| Danceability Predictor | Gradient Boosting | **66.7% R²** | Predict danceability score |
| Tempo Optimizer | Random Forest | **19.4% R²** | Recommend optimal tempo |

**Training:** 100K tracks, 80/20 split, 5-fold CV

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 18.6+
- Node.js (for Vercel CLI)

### Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/spotify-tempo-dashboard.git
cd spotify-tempo-dashboard

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb spotify_music_db
psql spotify_music_db < database/schema.sql

# Start Flask API
python api/search_api.py

# Start dashboard (new terminal)
cd dashboard
python -m http.server 8000
```

**Access:** http://localhost:8000

---

## 🚀 Deployment

### Backend (Railway)

```bash
# Install Gunicorn
pip install gunicorn
pip freeze > requirements.txt

# Push to GitHub
git push origin main

# Deploy on Railway
# 1. Go to railway.app
# 2. New Project → Deploy from GitHub
# 3. Add PostgreSQL database
# 4. Set environment variables
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd dashboard
vercel --prod
```

**See:** [`docs/COMPLETE_DOCUMENTATION.md`](docs/COMPLETE_DOCUMENTATION.md) for detailed guide.

---

## 📖 Documentation

- **[Complete Documentation](docs/COMPLETE_DOCUMENTATION.md)** - Full project documentation
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System architecture details
- **[API Documentation](docs/COMPLETE_DOCUMENTATION.md#7-api-documentation)** - API endpoints reference
- **[Deployment Guide](docs/COMPLETE_DOCUMENTATION.md#4-deployment-guide)** - Step-by-step deployment

---

## 🎯 Usage

### ML Predictions

```python
import requests

url = "https://your-api.railway.app/api/predict/all"
data = {
    "tempo": 120,
    "energy": 0.8,
    "danceability": 0.75,
    "valence": 0.6,
    "acousticness": 0.1,
    "instrumentalness": 0.0,
    "liveness": 0.15,
    "speechiness": 0.05,
    "loudness": -5,
    "duration_ms": 200000,
    "year": 2023,
    "key": 5,
    "mode": 1,
    "time_signature": 4
}

response = requests.post(url, json=data)
print(response.json())
```

**Output:**
```json
{
  "success": true,
  "predictions": {
    "popularity": {"score": 74.46},
    "hit_classification": {"is_hit": true, "probability": 1.0},
    "danceability": {"score": 0.78}
  }
}
```

---

## 📊 Dataset

- **Source:** Spotify Web API
- **Size:** 1,204,025 tracks
- **Period:** 1920-2020 (100 years)
- **Features:** 14 audio features per track
  - Tempo, Energy, Danceability, Valence
  - Acousticness, Instrumentalness, Liveness
  - Speechiness, Loudness, Duration, Year, Key, Mode, Time Signature

---

## 🎓 Academic Context

This project is part of Big Data course (Semester 5, 2026).

**Research Focus:**
Machine learning prediction system for music track success using audio features.

**Key Findings:**
- Energy-danceability interaction is top predictor (89% importance)
- Audio features strongly predict popularity (R² > 0.93)
- Tempo shows low predictive power (R² = 0.19), suggesting creative freedom

**Thesis Defense Ready:**
- Presentation script included
- Q&A preparation
- Live demo
- Honest limitations acknowledged

---

## 🛡️ License

This project is for educational purposes (Big Data - Semester 5, 2026).

---

## 🤝 Contributing

This is an academic project. For suggestions or questions:
- Open an issue
- Contact via GitHub

---

## 📝 Citation

If you use this project for research:

```bibtex
@misc{spotify-tempo-analysis-2026,
  title={Machine Learning Prediction System for Music Track Success},
  author={Your Name},
  year={2026},
  howpublished={\url{https://github.com/YOUR_USERNAME/spotify-tempo-dashboard}}
}
```

---

## 🌟 Acknowledgments

- **Data Source:** Spotify Web API
- **ML Framework:** scikit-learn
- **Deployment:** Railway, Vercel
- **Database:** PostgreSQL
- **Styling:** Tailwind CSS, Material Design

---

## 📧 Contact

- **GitHub:** [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- **Project:** Big Data - Semester 5
- **Year:** 2026

---

**Made with ❤️ for Big Data Course**
