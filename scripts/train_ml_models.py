"""
MACHINE LEARNING MODEL TRAINING
================================
Train 4 prediction models:
1. Popularity Predictor (Regression)
2. Hit Classification (Binary Classification)
3. Danceability Predictor (Regression)
4. Tempo Optimizer (Regression)

Dataset: 1.2M Spotify tracks from PostgreSQL
"""

import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
import pickle
import json
from datetime import datetime
from pathlib import Path

# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import warnings
warnings.filterwarnings('ignore')

# Fix pandas dtype backend issue with PostgreSQL
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

# Database Config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb'
}

# Create models directory
MODELS_DIR = Path(__file__).parent.parent / 'models'
MODELS_DIR.mkdir(exist_ok=True)

print("="*80)
print("  SPOTIFY TEMPO ANALYSIS - ML MODEL TRAINING")
print("="*80)
print()

# ============================================
# 1. LOAD DATA FROM POSTGRESQL
# ============================================

print("📊 Loading data from PostgreSQL...")
from sqlalchemy import create_engine

# Use SQLAlchemy with psycopg2 to avoid pandas Arrow backend issues
engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

# Load all tracks with required features
query = """
    SELECT 
        tempo, energy, danceability, valence, acousticness,
        instrumentalness, liveness, speechiness, loudness,
        duration_ms, year, key, mode, time_signature
    FROM spotify_tracks_raw
    WHERE 
        tempo IS NOT NULL 
        AND energy IS NOT NULL 
        AND danceability IS NOT NULL
        AND year IS NOT NULL
    LIMIT 100000
"""

df = pd.read_sql(query, engine)
engine.dispose()

print(f"✅ Loaded {len(df):,} tracks")
print(f"   Features: {df.shape[1]} columns")

# Data should now be in proper numeric format
df = df.dropna()
print(f"✅ After cleaning: {len(df):,} tracks")

# Create synthetic popularity score based on features
# This is a proxy for actual popularity (not available in dataset)
print("🔧 Creating synthetic popularity score...")
df['popularity'] = (
    (df['danceability'] * 40) +  # Danceability contributes most
    (df['energy'] * 30) +  # Energy is important
    (df['valence'] * 15) +  # Positivity matters
    ((1 - df['acousticness']) * 10) +  # Less acoustic = more popular
    (np.random.normal(0, 5, len(df)))  # Add some noise
)
df['popularity'] = df['popularity'].clip(0, 100)

print(f"✅ Created popularity scores (mean: {df['popularity'].mean():.2f})")
print()

# ============================================
# 2. FEATURE ENGINEERING
# ============================================

print("🔧 Feature engineering...")

# Add derived features
df['in_sweet_spot'] = ((df['tempo'] >= 100) & (df['tempo'] < 120)).astype(int)
df['is_modern'] = (df['year'] >= 2000).astype(int)
df['is_acoustic'] = (df['acousticness'] > 0.5).astype(int)
df['is_instrumental'] = (df['instrumentalness'] > 0.5).astype(int)
df['is_live'] = (df['liveness'] > 0.8).astype(int)
df['high_energy'] = (df['energy'] > 0.7).astype(int)
df['high_dance'] = (df['danceability'] > 0.7).astype(int)

# Energy-Dance interaction
df['energy_dance_product'] = df['energy'] * df['danceability']
df['tempo_dance_ratio'] = df['tempo'] / (df['danceability'] + 0.01)

# Normalize duration to minutes
df['duration_min'] = df['duration_ms'] / 60000

# Create hit/flop label (popularity > 50 = hit)
df['is_hit'] = (df['popularity'] > 50).astype(int)

print(f"✅ Added {df.shape[1] - 15} derived features")
print()

# ============================================
# 3. PREPARE DATASETS
# ============================================

print("📦 Preparing datasets...")

# Feature columns for all models
feature_cols = [
    'tempo', 'energy', 'danceability', 'valence', 'acousticness',
    'instrumentalness', 'liveness', 'speechiness', 'loudness',
    'duration_min', 'year', 'key', 'mode', 'time_signature',
    'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
    'is_live', 'high_energy', 'high_dance', 'energy_dance_product',
    'tempo_dance_ratio'
]

X = df[feature_cols].copy()

# Handle any remaining NaN
X = X.fillna(X.median())

# Split data (80% train, 20% test)
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

print(f"✅ Training set: {len(X_train):,} samples")
print(f"✅ Test set: {len(X_test):,} samples")
print()

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
scaler_path = MODELS_DIR / 'feature_scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"💾 Saved scaler: {scaler_path}")
print()

# ============================================
# 4. MODEL 1: POPULARITY PREDICTOR
# ============================================

print("="*80)
print("🎯 MODEL 1: POPULARITY PREDICTOR (Regression)")
print("="*80)

y_popularity_train = df.loc[X_train.index, 'popularity']
y_popularity_test = df.loc[X_test.index, 'popularity']

print("🔄 Training Random Forest Regressor...")
model_popularity = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model_popularity.fit(X_train_scaled, y_popularity_train)

# Predict
y_pred_pop = model_popularity.predict(X_test_scaled)

# Evaluate
mse = mean_squared_error(y_popularity_test, y_pred_pop)
mae = mean_absolute_error(y_popularity_test, y_pred_pop)
r2 = r2_score(y_popularity_test, y_pred_pop)

print(f"\n📊 Performance:")
print(f"   MSE: {mse:.2f}")
print(f"   MAE: {mae:.2f}")
print(f"   R² Score: {r2:.4f}")

# Feature importance
feature_importance_pop = pd.DataFrame({
    'feature': feature_cols,
    'importance': model_popularity.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n🔝 Top 5 Features:")
for idx, row in feature_importance_pop.head(5).iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# Save model
model_path = MODELS_DIR / 'popularity_predictor.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model_popularity, f)
print(f"\n💾 Saved model: {model_path}")
print()

# ============================================
# 5. MODEL 2: HIT CLASSIFICATION
# ============================================

print("="*80)
print("🎯 MODEL 2: HIT CLASSIFICATION (Binary)")
print("="*80)

y_hit_train = df.loc[X_train.index, 'is_hit']
y_hit_test = df.loc[X_test.index, 'is_hit']

print("🔄 Training Random Forest Classifier...")
model_hit = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    verbose=0,
    class_weight='balanced'
)

model_hit.fit(X_train_scaled, y_hit_train)

# Predict
y_pred_hit = model_hit.predict(X_test_scaled)
y_pred_hit_proba = model_hit.predict_proba(X_test_scaled)[:, 1]

# Evaluate
accuracy = accuracy_score(y_hit_test, y_pred_hit)
precision = precision_score(y_hit_test, y_pred_hit)
recall = recall_score(y_hit_test, y_pred_hit)
f1 = f1_score(y_hit_test, y_pred_hit)

print(f"\n📊 Performance:")
print(f"   Accuracy: {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall: {recall:.4f}")
print(f"   F1 Score: {f1:.4f}")

# Confusion matrix
cm = confusion_matrix(y_hit_test, y_pred_hit)
print(f"\n📈 Confusion Matrix:")
print(f"   TN: {cm[0,0]:,}  FP: {cm[0,1]:,}")
print(f"   FN: {cm[1,0]:,}  TP: {cm[1,1]:,}")

# Save model
model_path = MODELS_DIR / 'hit_classifier.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model_hit, f)
print(f"\n💾 Saved model: {model_path}")
print()

# ============================================
# 6. MODEL 3: DANCEABILITY PREDICTOR
# ============================================

print("="*80)
print("🎯 MODEL 3: DANCEABILITY PREDICTOR (Regression)")
print("="*80)

# For this model, we predict danceability from other features (excluding danceability itself)
feature_cols_dance = [col for col in feature_cols if col not in ['danceability', 'high_dance', 'energy_dance_product', 'tempo_dance_ratio']]
X_dance_train = X_train[feature_cols_dance]
X_dance_test = X_test[feature_cols_dance]

# Scale
scaler_dance = StandardScaler()
X_dance_train_scaled = scaler_dance.fit_transform(X_dance_train)
X_dance_test_scaled = scaler_dance.transform(X_dance_test)

# Save scaler
scaler_path = MODELS_DIR / 'danceability_scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler_dance, f)

y_dance_train = df.loc[X_train.index, 'danceability']
y_dance_test = df.loc[X_test.index, 'danceability']

print("🔄 Training Gradient Boosting Regressor...")
model_dance = GradientBoostingRegressor(
    n_estimators=100,
    max_depth=10,
    learning_rate=0.1,
    random_state=42,
    verbose=0
)

model_dance.fit(X_dance_train_scaled, y_dance_train)

# Predict
y_pred_dance = model_dance.predict(X_dance_test_scaled)

# Evaluate
mse = mean_squared_error(y_dance_test, y_pred_dance)
mae = mean_absolute_error(y_dance_test, y_pred_dance)
r2 = r2_score(y_dance_test, y_pred_dance)

print(f"\n📊 Performance:")
print(f"   MSE: {mse:.4f}")
print(f"   MAE: {mae:.4f}")
print(f"   R² Score: {r2:.4f}")

# Save model
model_path = MODELS_DIR / 'danceability_predictor.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model_dance, f)
print(f"\n💾 Saved model: {model_path}")
print()

# ============================================
# 7. MODEL 4: TEMPO OPTIMIZER
# ============================================

print("="*80)
print("🎯 MODEL 4: TEMPO OPTIMIZER (Regression)")
print("="*80)

# Predict optimal tempo from target features
feature_cols_tempo = [col for col in feature_cols if col not in ['tempo', 'in_sweet_spot', 'tempo_dance_ratio']]
X_tempo_train = X_train[feature_cols_tempo]
X_tempo_test = X_test[feature_cols_tempo]

# Scale
scaler_tempo = StandardScaler()
X_tempo_train_scaled = scaler_tempo.fit_transform(X_tempo_train)
X_tempo_test_scaled = scaler_tempo.transform(X_tempo_test)

# Save scaler
scaler_path = MODELS_DIR / 'tempo_scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler_tempo, f)

y_tempo_train = df.loc[X_train.index, 'tempo']
y_tempo_test = df.loc[X_test.index, 'tempo']

print("🔄 Training Random Forest Regressor...")
model_tempo = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model_tempo.fit(X_tempo_train_scaled, y_tempo_train)

# Predict
y_pred_tempo = model_tempo.predict(X_tempo_test_scaled)

# Evaluate
mse = mean_squared_error(y_tempo_test, y_pred_tempo)
mae = mean_absolute_error(y_tempo_test, y_pred_tempo)
r2 = r2_score(y_tempo_test, y_pred_tempo)

print(f"\n📊 Performance:")
print(f"   MSE: {mse:.2f}")
print(f"   MAE: {mae:.2f} BPM")
print(f"   R² Score: {r2:.4f}")

# Save model
model_path = MODELS_DIR / 'tempo_optimizer.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model_tempo, f)
print(f"\n💾 Saved model: {model_path}")
print()

# ============================================
# 8. SAVE METADATA & REPORT
# ============================================

print("="*80)
print("📄 SAVING METADATA & REPORT")
print("="*80)

metadata = {
    'training_date': datetime.now().isoformat(),
    'dataset_size': len(df),
    'train_size': len(X_train),
    'test_size': len(X_test),
    'feature_columns': feature_cols,
    'models': {
        'popularity_predictor': {
            'type': 'RandomForestRegressor',
            'metrics': {
                'mse': float(mean_squared_error(y_popularity_test, y_pred_pop)),
                'mae': float(mean_absolute_error(y_popularity_test, y_pred_pop)),
                'r2': float(r2_score(y_popularity_test, y_pred_pop))
            }
        },
        'hit_classifier': {
            'type': 'RandomForestClassifier',
            'metrics': {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1': float(f1)
            }
        },
        'danceability_predictor': {
            'type': 'GradientBoostingRegressor',
            'metrics': {
                'mse': float(mean_squared_error(y_dance_test, y_pred_dance)),
                'mae': float(mean_absolute_error(y_dance_test, y_pred_dance)),
                'r2': float(r2_score(y_dance_test, y_pred_dance))
            }
        },
        'tempo_optimizer': {
            'type': 'RandomForestRegressor',
            'metrics': {
                'mse': float(mean_squared_error(y_tempo_test, y_pred_tempo)),
                'mae': float(mean_absolute_error(y_tempo_test, y_pred_tempo)),
                'r2': float(r2_score(y_tempo_test, y_pred_tempo))
            }
        }
    }
}

# Save metadata
metadata_path = MODELS_DIR / 'models_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Saved metadata: {metadata_path}")

# Print summary
print("\n" + "="*80)
print("🎉 TRAINING COMPLETE!")
print("="*80)
print("\n📦 Saved Models:")
print(f"   1. Popularity Predictor (R²={metadata['models']['popularity_predictor']['metrics']['r2']:.4f})")
print(f"   2. Hit Classifier (Acc={metadata['models']['hit_classifier']['metrics']['accuracy']:.4f})")
print(f"   3. Danceability Predictor (R²={metadata['models']['danceability_predictor']['metrics']['r2']:.4f})")
print(f"   4. Tempo Optimizer (R²={metadata['models']['tempo_optimizer']['metrics']['r2']:.4f})")
print("\n📁 Models saved in:", MODELS_DIR)
print("\n✅ Ready for deployment!")
print("="*80)
