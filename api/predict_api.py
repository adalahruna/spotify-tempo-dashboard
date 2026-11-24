"""
PREDICTION API ENDPOINTS
========================
ML Model inference endpoints for:
1. Popularity prediction
2. Hit classification
3. Danceability prediction
4. Tempo optimization
"""

from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
import json

# Create Blueprint
predict_bp = Blueprint('predict', __name__)

# Models directory
MODELS_DIR = Path(__file__).parent.parent / 'models'

# Load models and scalers (lazy loading)
_models_cache = {}

def load_model(model_name):
    """Load model from cache or disk"""
    if model_name not in _models_cache:
        model_path = MODELS_DIR / f'{model_name}.pkl'
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        with open(model_path, 'rb') as f:
            _models_cache[model_name] = pickle.load(f)
    return _models_cache[model_name]

def load_metadata():
    """Load models metadata"""
    metadata_path = MODELS_DIR / 'models_metadata.json'
    if not metadata_path.exists():
        return {}
    with open(metadata_path, 'r') as f:
        return json.load(f)

# Feature engineering helper
def engineer_features(data):
    """Apply same feature engineering as training"""
    df = pd.DataFrame([data])
    
    # Derived features
    df['in_sweet_spot'] = int((df['tempo'].iloc[0] >= 100) and (df['tempo'].iloc[0] < 120))
    df['is_modern'] = int(df['year'].iloc[0] >= 2000)
    df['is_acoustic'] = int(df['acousticness'].iloc[0] > 0.5)
    df['is_instrumental'] = int(df['instrumentalness'].iloc[0] > 0.5)
    df['is_live'] = int(df['liveness'].iloc[0] > 0.8)
    df['high_energy'] = int(df['energy'].iloc[0] > 0.7)
    df['high_dance'] = int(df['danceability'].iloc[0] > 0.7)
    
    # Interactions
    df['energy_dance_product'] = df['energy'].iloc[0] * df['danceability'].iloc[0]
    df['tempo_dance_ratio'] = df['tempo'].iloc[0] / (df['danceability'].iloc[0] + 0.01)
    
    # Duration
    df['duration_min'] = df['duration_ms'].iloc[0] / 60000
    
    return df

# ============================================
# PREDICTION ENDPOINTS
# ============================================

@predict_bp.route('/predict/popularity', methods=['POST'])
def predict_popularity():
    """
    Predict popularity score (0-100)
    
    Request body:
    {
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
    """
    try:
        data = request.json
        
        # Validate required fields
        required = ['tempo', 'energy', 'danceability', 'valence', 'acousticness',
                   'instrumentalness', 'liveness', 'speechiness', 'loudness',
                   'duration_ms', 'year', 'key', 'mode', 'time_signature']
        
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400
        
        # Engineer features
        df = engineer_features(data)
        
        # Feature order
        feature_cols = [
            'tempo', 'energy', 'danceability', 'valence', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness', 'loudness',
            'duration_min', 'year', 'key', 'mode', 'time_signature',
            'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
            'is_live', 'high_energy', 'high_dance', 'energy_dance_product',
            'tempo_dance_ratio'
        ]
        
        X = df[feature_cols].values
        
        # Load model and scaler
        scaler = load_model('feature_scaler')
        model = load_model('popularity_predictor')
        
        # Scale and predict
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        
        # Clip to 0-100 range
        prediction = float(np.clip(prediction, 0, 100))
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'interpretation': get_popularity_interpretation(prediction),
            'model': 'RandomForestRegressor'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/predict/hit', methods=['POST'])
def predict_hit():
    """
    Predict if track will be a hit (popularity > 50)
    
    Same request body as /predict/popularity
    """
    try:
        data = request.json
        
        # Validate
        required = ['tempo', 'energy', 'danceability', 'valence', 'acousticness',
                   'instrumentalness', 'liveness', 'speechiness', 'loudness',
                   'duration_ms', 'year', 'key', 'mode', 'time_signature']
        
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400
        
        # Engineer features
        df = engineer_features(data)
        
        feature_cols = [
            'tempo', 'energy', 'danceability', 'valence', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness', 'loudness',
            'duration_min', 'year', 'key', 'mode', 'time_signature',
            'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
            'is_live', 'high_energy', 'high_dance', 'energy_dance_product',
            'tempo_dance_ratio'
        ]
        
        X = df[feature_cols].values
        
        # Load model and scaler
        scaler = load_model('feature_scaler')
        model = load_model('hit_classifier')
        
        # Scale and predict
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0]
        
        return jsonify({
            'success': True,
            'is_hit': bool(prediction),
            'probability': {
                'flop': round(float(probability[0]), 4),
                'hit': round(float(probability[1]), 4)
            },
            'confidence': round(float(max(probability)), 4),
            'interpretation': 'Hit (Popularity > 50)' if prediction else 'Flop (Popularity ≤ 50)',
            'model': 'RandomForestClassifier'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/predict/danceability', methods=['POST'])
def predict_danceability():
    """
    Predict danceability score (0-1)
    
    Request body (without danceability):
    {
        "tempo": 120,
        "energy": 0.8,
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
    """
    try:
        data = request.json
        
        # Set dummy danceability for feature engineering
        data_with_dance = data.copy()
        data_with_dance['danceability'] = 0.5  # dummy value
        
        # Engineer features
        df = engineer_features(data_with_dance)
        
        # Features excluding danceability-related
        feature_cols = [
            'tempo', 'energy', 'valence', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness', 'loudness',
            'duration_min', 'year', 'key', 'mode', 'time_signature',
            'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
            'is_live', 'high_energy'
        ]
        
        X = df[feature_cols].values
        
        # Load model and scaler
        scaler = load_model('danceability_scaler')
        model = load_model('danceability_predictor')
        
        # Scale and predict
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        
        # Clip to 0-1 range
        prediction = float(np.clip(prediction, 0, 1))
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 4),
            'percentage': round(prediction * 100, 2),
            'interpretation': get_danceability_interpretation(prediction),
            'model': 'GradientBoostingRegressor'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/predict/tempo', methods=['POST'])
def predict_optimal_tempo():
    """
    Predict optimal tempo for given track characteristics
    
    Request body (without tempo):
    {
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
    """
    try:
        data = request.json
        
        # Set dummy tempo
        data_with_tempo = data.copy()
        data_with_tempo['tempo'] = 120  # dummy
        
        # Engineer features
        df = engineer_features(data_with_tempo)
        
        # Features excluding tempo-related
        feature_cols = [
            'energy', 'danceability', 'valence', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness', 'loudness',
            'duration_min', 'year', 'key', 'mode', 'time_signature',
            'is_modern', 'is_acoustic', 'is_instrumental',
            'is_live', 'high_energy', 'high_dance', 'energy_dance_product'
        ]
        
        X = df[feature_cols].values
        
        # Load model and scaler
        scaler = load_model('tempo_scaler')
        model = load_model('tempo_optimizer')
        
        # Scale and predict
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        
        # Clip to reasonable range
        prediction = float(np.clip(prediction, 40, 200))
        
        # Check if in sweet spot
        in_sweet_spot = 100 <= prediction < 120
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'in_sweet_spot': in_sweet_spot,
            'interpretation': get_tempo_interpretation(prediction),
            'recommendation': get_tempo_recommendation(prediction),
            'model': 'RandomForestRegressor'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/predict/all', methods=['POST'])
def predict_all():
    """
    Run all 4 predictions at once
    
    Full request body with all features
    """
    try:
        data = request.json
        
        # Call each prediction endpoint internally
        results = {}
        
        # 1. Popularity
        try:
            df = engineer_features(data)
            feature_cols = [
                'tempo', 'energy', 'danceability', 'valence', 'acousticness',
                'instrumentalness', 'liveness', 'speechiness', 'loudness',
                'duration_min', 'year', 'key', 'mode', 'time_signature',
                'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
                'is_live', 'high_energy', 'high_dance', 'energy_dance_product',
                'tempo_dance_ratio'
            ]
            X = df[feature_cols].values
            scaler = load_model('feature_scaler')
            model = load_model('popularity_predictor')
            X_scaled = scaler.transform(X)
            pop_pred = float(np.clip(model.predict(X_scaled)[0], 0, 100))
            results['popularity'] = {
                'score': round(pop_pred, 2),
                'interpretation': get_popularity_interpretation(pop_pred)
            }
        except Exception as e:
            results['popularity'] = {'error': str(e)}
        
        # 2. Hit Classification
        try:
            model = load_model('hit_classifier')
            hit_pred = model.predict(X_scaled)[0]
            hit_proba = model.predict_proba(X_scaled)[0]
            results['hit_classification'] = {
                'is_hit': bool(hit_pred),
                'probability': round(float(hit_proba[1]), 4),
                'confidence': round(float(max(hit_proba)), 4)
            }
        except Exception as e:
            results['hit_classification'] = {'error': str(e)}
        
        # 3. Danceability (if not provided)
        if 'danceability' not in data or data.get('predict_danceability'):
            try:
                data_copy = data.copy()
                data_copy['danceability'] = 0.5
                df2 = engineer_features(data_copy)
                feature_cols_dance = [
                    'tempo', 'energy', 'valence', 'acousticness',
                    'instrumentalness', 'liveness', 'speechiness', 'loudness',
                    'duration_min', 'year', 'key', 'mode', 'time_signature',
                    'in_sweet_spot', 'is_modern', 'is_acoustic', 'is_instrumental',
                    'is_live', 'high_energy'
                ]
                X_dance = df2[feature_cols_dance].values
                scaler_dance = load_model('danceability_scaler')
                model_dance = load_model('danceability_predictor')
                X_dance_scaled = scaler_dance.transform(X_dance)
                dance_pred = float(np.clip(model_dance.predict(X_dance_scaled)[0], 0, 1))
                results['danceability'] = {
                    'score': round(dance_pred, 4),
                    'percentage': round(dance_pred * 100, 2)
                }
            except Exception as e:
                results['danceability'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'predictions': results,
            'input': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/models/info', methods=['GET'])
def models_info():
    """Get information about loaded models"""
    try:
        metadata = load_metadata()
        
        # Check which models are available
        available_models = []
        for model_name in ['popularity_predictor', 'hit_classifier', 'danceability_predictor', 'tempo_optimizer']:
            if (MODELS_DIR / f'{model_name}.pkl').exists():
                available_models.append(model_name)
        
        return jsonify({
            'success': True,
            'available_models': available_models,
            'metadata': metadata,
            'endpoints': {
                'popularity': '/api/predict/popularity',
                'hit': '/api/predict/hit',
                'danceability': '/api/predict/danceability',
                'tempo': '/api/predict/tempo',
                'all': '/api/predict/all'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_popularity_interpretation(score):
    """Interpret popularity score"""
    if score >= 80:
        return "Viral Hit - Extremely Popular"
    elif score >= 60:
        return "Popular Track - Strong Performance"
    elif score >= 40:
        return "Moderate Success - Average Performance"
    elif score >= 20:
        return "Limited Appeal - Below Average"
    else:
        return "Niche Track - Low Popularity"

def get_danceability_interpretation(score):
    """Interpret danceability score"""
    if score >= 0.8:
        return "Extremely Danceable - Perfect for clubs"
    elif score >= 0.6:
        return "Highly Danceable - Good groove"
    elif score >= 0.4:
        return "Moderately Danceable"
    elif score >= 0.2:
        return "Low Danceability"
    else:
        return "Not Danceable"

def get_tempo_interpretation(bpm):
    """Interpret tempo"""
    if bpm < 60:
        return "Very Slow (Ballad)"
    elif bpm < 80:
        return "Slow (Downtempo)"
    elif bpm < 100:
        return "Moderate Slow"
    elif bpm < 120:
        return "Sweet Spot (Optimal Dance Tempo)"
    elif bpm < 140:
        return "Fast (Upbeat)"
    elif bpm < 160:
        return "Very Fast (High Energy)"
    else:
        return "Extremely Fast (EDM/Hardcore)"

def get_tempo_recommendation(bpm):
    """Get recommendation based on tempo"""
    if 100 <= bpm < 120:
        return "Perfect! This tempo is in the sweet spot for maximum danceability."
    elif bpm < 100:
        return f"Consider increasing to 100-120 BPM for better danceability (currently {bpm:.1f} BPM)"
    else:
        return f"Consider decreasing to 100-120 BPM for sweet spot benefits (currently {bpm:.1f} BPM)"
