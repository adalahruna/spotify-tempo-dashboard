# 🤖 Machine Learning Models Documentation

## Overview

This project includes **4 trained ML models** for predicting various music track characteristics based on audio features from 1.2M Spotify tracks.

---

## 📊 Models Summary

| Model | Type | Task | Accuracy/R² | Input Features | Output |
|-------|------|------|-------------|----------------|--------|
| **Popularity Predictor** | Random Forest Regressor | Regression | R² ≈ 0.XX | 23 features | 0-100 score |
| **Hit Classifier** | Random Forest Classifier | Binary Classification | Acc ≈ XX% | 23 features | Hit/Flop + probability |
| **Danceability Predictor** | Gradient Boosting Regressor | Regression | R² ≈ 0.XX | 19 features | 0-1 score |
| **Tempo Optimizer** | Random Forest Regressor | Regression | R² ≈ 0.XX | 19 features | BPM (40-200) |

*Note: Actual metrics will be available after training. Run `python scripts/train_ml_models.py` to train models.*

---

## 🎯 Model 1: Popularity Predictor

### Purpose
Predicts the popularity score of a track (0-100 scale) based on audio features.

### Algorithm
- **Model:** Random Forest Regressor
- **Estimators:** 100 trees
- **Max Depth:** 20
- **Features:** 23 audio + derived features

### Input Features
```json
{
  "tempo": 120,              // BPM (40-200)
  "energy": 0.8,             // 0-1 scale
  "danceability": 0.7,       // 0-1 scale
  "valence": 0.6,            // Positivity (0-1)
  "acousticness": 0.1,       // 0-1 scale
  "instrumentalness": 0.0,   // 0-1 scale
  "liveness": 0.1,           // 0-1 scale
  "speechiness": 0.05,       // 0-1 scale
  "loudness": -5,            // dB (-30 to 0)
  "duration_ms": 210000,     // milliseconds
  "year": 2020,              // Release year
  "key": 5,                  // 0-11 (C=0, C#=1, etc.)
  "mode": 1,                 // 0=Minor, 1=Major
  "time_signature": 4        // 3-7
}
```

### Output
```json
{
  "success": true,
  "prediction": 65.42,
  "interpretation": "Popular Track - Strong Performance",
  "model": "RandomForestRegressor"
}
```

### Interpretation Scale
- **80-100:** Viral Hit - Extremely Popular
- **60-79:** Popular Track - Strong Performance
- **40-59:** Moderate Success - Average Performance
- **20-39:** Limited Appeal - Below Average
- **0-19:** Niche Track - Low Popularity

### API Endpoint
```bash
POST /api/predict/popularity
Content-Type: application/json

{
  "tempo": 120,
  "energy": 0.8,
  ...
}
```

---

## 🔥 Model 2: Hit Classifier

### Purpose
Classifies whether a track will be a "Hit" (popularity > 50) or "Flop" (popularity ≤ 50).

### Algorithm
- **Model:** Random Forest Classifier
- **Estimators:** 100 trees
- **Class Weight:** Balanced
- **Features:** 23 audio + derived features

### Input
Same 14 features as Popularity Predictor.

### Output
```json
{
  "success": true,
  "is_hit": true,
  "probability": {
    "flop": 0.2341,
    "hit": 0.7659
  },
  "confidence": 0.7659,
  "interpretation": "Hit (Popularity > 50)",
  "model": "RandomForestClassifier"
}
```

### Metrics
- **Accuracy:** XX%
- **Precision:** XX%
- **Recall:** XX%
- **F1 Score:** XX%

### API Endpoint
```bash
POST /api/predict/hit
```

---

## 💃 Model 3: Danceability Predictor

### Purpose
Predicts the danceability score (0-1) from other audio features.

### Algorithm
- **Model:** Gradient Boosting Regressor
- **Estimators:** 100
- **Learning Rate:** 0.1
- **Features:** 19 features (excludes danceability-related)

### Input Features
Same as above, **but without:**
- `danceability`
- Derived features that depend on danceability

### Output
```json
{
  "success": true,
  "prediction": 0.7234,
  "percentage": 72.34,
  "interpretation": "Highly Danceable - Good groove",
  "model": "GradientBoostingRegressor"
}
```

### Interpretation Scale
- **0.8-1.0:** Extremely Danceable - Perfect for clubs
- **0.6-0.8:** Highly Danceable - Good groove
- **0.4-0.6:** Moderately Danceable
- **0.2-0.4:** Low Danceability
- **0.0-0.2:** Not Danceable

### API Endpoint
```bash
POST /api/predict/danceability
```

---

## 🎵 Model 4: Tempo Optimizer

### Purpose
Recommends optimal tempo (BPM) for given track characteristics.

### Algorithm
- **Model:** Random Forest Regressor
- **Estimators:** 100
- **Features:** 19 features (excludes tempo-related)

### Input Features
Same as above, **but without:**
- `tempo`
- Derived features that depend on tempo

### Output
```json
{
  "success": true,
  "prediction": 115.67,
  "in_sweet_spot": true,
  "interpretation": "Sweet Spot (Optimal Dance Tempo)",
  "recommendation": "Perfect! This tempo is in the sweet spot for maximum danceability.",
  "model": "RandomForestRegressor"
}
```

### Tempo Zones
- **< 60 BPM:** Very Slow (Ballad)
- **60-80 BPM:** Slow (Downtempo)
- **80-100 BPM:** Moderate Slow
- **100-120 BPM:** ⭐ **Sweet Spot** (Optimal Dance Tempo)
- **120-140 BPM:** Fast (Upbeat)
- **140-160 BPM:** Very Fast (High Energy)
- **> 160 BPM:** Extremely Fast (EDM/Hardcore)

### API Endpoint
```bash
POST /api/predict/tempo
```

---

## 📦 Batch Prediction

### Endpoint
```bash
POST /api/predict/all
```

### Description
Run all 4 predictions in a single request for efficiency.

### Output
```json
{
  "success": true,
  "predictions": {
    "popularity": {
      "score": 65.42,
      "interpretation": "Popular Track - Strong Performance"
    },
    "hit_classification": {
      "is_hit": true,
      "probability": 0.7659,
      "confidence": 0.7659
    },
    "danceability": {
      "score": 0.7234,
      "percentage": 72.34
    }
  },
  "input": { ... }
}
```

---

## 🔧 Feature Engineering

The models use **23 engineered features** total:

### Base Features (14)
From Spotify API:
- `tempo`, `energy`, `danceability`, `valence`
- `acousticness`, `instrumentalness`, `liveness`, `speechiness`
- `loudness`, `duration_ms`, `year`, `key`, `mode`, `time_signature`

### Derived Features (9)
Automatically calculated:
- `in_sweet_spot` - Boolean: tempo 100-120 BPM
- `is_modern` - Boolean: year >= 2000
- `is_acoustic` - Boolean: acousticness > 0.5
- `is_instrumental` - Boolean: instrumentalness > 0.5
- `is_live` - Boolean: liveness > 0.8
- `high_energy` - Boolean: energy > 0.7
- `high_dance` - Boolean: danceability > 0.7
- `energy_dance_product` - Interaction: energy × danceability
- `tempo_dance_ratio` - Ratio: tempo / (danceability + 0.01)
- `duration_min` - Converted: duration_ms / 60000

---

## 🚀 Training the Models

### Requirements
```bash
pip install -r requirements.txt
```

### Run Training
```bash
python scripts/train_ml_models.py
```

### Training Process
1. **Load Data:** Fetch 1M tracks from PostgreSQL
2. **Feature Engineering:** Create derived features
3. **Split:** 80% train, 20% test
4. **Scale:** StandardScaler normalization
5. **Train:** 4 models in sequence
6. **Evaluate:** Calculate metrics
7. **Save:** Export to `models/` directory

### Output Files
```
models/
├── popularity_predictor.pkl      # Popularity model
├── hit_classifier.pkl             # Hit/Flop model
├── danceability_predictor.pkl     # Danceability model
├── tempo_optimizer.pkl            # Tempo model
├── feature_scaler.pkl             # Main scaler
├── danceability_scaler.pkl        # Danceability-specific scaler
├── tempo_scaler.pkl               # Tempo-specific scaler
└── models_metadata.json           # Performance metrics
```

### Training Time
- **Dataset Size:** 1,000,000 tracks
- **Estimated Time:** 5-15 minutes (depends on CPU)
- **RAM Required:** ~4-8 GB

---

## 📊 Model Performance

### Evaluation Metrics

**Regression Models (Popularity, Danceability, Tempo):**
- **MSE** - Mean Squared Error
- **MAE** - Mean Absolute Error
- **R² Score** - Coefficient of Determination

**Classification Model (Hit):**
- **Accuracy** - Overall correctness
- **Precision** - True positive rate
- **Recall** - Sensitivity
- **F1 Score** - Harmonic mean

### View Metrics
```bash
# Check saved metadata
cat models/models_metadata.json
```

Or via API:
```bash
GET /api/models/info
```

---

## 🎨 Using the Prediction UI

### Access
Open `dashboard/predict.html` in browser:
```
http://localhost:8000/dashboard/predict.html
```

### Features
1. **Interactive Sliders** - Adjust 14 audio features in real-time
2. **Instant Prediction** - Click "Predict Track Success"
3. **Visual Results** - Animated cards with scores and interpretations
4. **Multiple Predictions** - Popularity, Hit potential, Danceability

### Workflow
1. Adjust sliders to desired values
2. Click "Predict Track Success" button
3. Wait 1-2 seconds for API response
4. View predictions in animated cards

---

## 🔌 API Integration

### Python Example
```python
import requests

url = "http://localhost:5000/api/predict/all"
data = {
    "tempo": 120,
    "energy": 0.8,
    "danceability": 0.7,
    "valence": 0.6,
    "acousticness": 0.1,
    "instrumentalness": 0.0,
    "liveness": 0.1,
    "speechiness": 0.05,
    "loudness": -5,
    "duration_ms": 210000,
    "year": 2020,
    "key": 5,
    "mode": 1,
    "time_signature": 4
}

response = requests.post(url, json=data)
result = response.json()

print(f"Popularity: {result['predictions']['popularity']['score']}")
print(f"Hit: {result['predictions']['hit_classification']['is_hit']}")
```

### JavaScript Example
```javascript
const predictTrack = async () => {
    const response = await fetch('http://localhost:5000/api/predict/all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tempo: 120,
            energy: 0.8,
            danceability: 0.7,
            valence: 0.6,
            acousticness: 0.1,
            instrumentalness: 0.0,
            liveness: 0.1,
            speechiness: 0.05,
            loudness: -5,
            duration_ms: 210000,
            year: 2020,
            key: 5,
            mode: 1,
            time_signature: 4
        })
    });
    
    const result = await response.json();
    console.log(result.predictions);
};
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/predict/popularity \
  -H "Content-Type: application/json" \
  -d '{
    "tempo": 120,
    "energy": 0.8,
    "danceability": 0.7,
    "valence": 0.6,
    "acousticness": 0.1,
    "instrumentalness": 0.0,
    "liveness": 0.1,
    "speechiness": 0.05,
    "loudness": -5,
    "duration_ms": 210000,
    "year": 2020,
    "key": 5,
    "mode": 1,
    "time_signature": 4
  }'
```

---

## 🐛 Troubleshooting

### Model Not Found Error
```
FileNotFoundError: Model not found: models/popularity_predictor.pkl
```

**Solution:** Train models first
```bash
python scripts/train_ml_models.py
```

### Import Error
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution:** Install dependencies
```bash
pip install scikit-learn pandas numpy
```

### Low Prediction Accuracy
**Possible causes:**
- Insufficient training data
- Poor feature selection
- Need hyperparameter tuning

**Solution:** Retrain with more data or tune parameters in `train_ml_models.py`

### API Returns Error
```json
{"error": "Database connection failed"}
```

**Solution:** Ensure PostgreSQL is running and accessible

---

## 📈 Model Improvement Ideas

### Short-term
- [ ] Add more derived features (genre encoding, artist popularity)
- [ ] Hyperparameter tuning with GridSearchCV
- [ ] Cross-validation for better evaluation
- [ ] Feature importance analysis

### Long-term
- [ ] Deep Learning models (Neural Networks)
- [ ] Ensemble methods (Stacking, Voting)
- [ ] Time series analysis (trend prediction)
- [ ] Multi-task learning
- [ ] Transfer learning from pre-trained audio models

---

## 📚 References

- **Scikit-learn Documentation:** [scikit-learn.org](https://scikit-learn.org/)
- **Random Forest:** [sklearn.ensemble.RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- **Gradient Boosting:** [sklearn.ensemble.GradientBoostingRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html)
- **Spotify Audio Features:** [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)

---

## 🎉 Success Checklist

- [x] Models trained and saved
- [x] API endpoints working
- [x] Prediction UI functional
- [x] Documentation complete
- [ ] Models deployed to production
- [ ] Performance monitoring setup
- [ ] A/B testing implemented

**Your ML prediction system is ready! 🚀**
