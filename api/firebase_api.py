"""
FIREBASE API FOR DASHBOARD
==========================
Flask API untuk baca summary stats dan ML results dari Firebase
No PostgreSQL needed - all data cached in Firebase
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production-ready CORS configuration
if os.environ.get('RAILWAY_ENVIRONMENT'):
    vercel_domain = os.environ.get('VERCEL_DOMAIN', 'spotify-tempo-dashboard.vercel.app')
    cors_origins = [
        f'https://{vercel_domain}',
        f'https://*.vercel.app',
        'http://localhost:8000',
        'http://127.0.0.1:8000'
    ]
    print(f"🔐 CORS enabled for: {cors_origins}")
else:
    cors_origins = ['http://localhost:8000', 'http://127.0.0.1:8000', '*']
    print(f"🔓 CORS enabled for development: {cors_origins}")

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Import and register prediction blueprint
try:
    from predict_api import predict_bp
    app.register_blueprint(predict_bp, url_prefix='/api')
    print("✅ ML Prediction endpoints loaded")
except Exception as e:
    print(f"⚠️  ML Prediction endpoints not available: {e}")

# Initialize Firebase
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # Get Firebase credentials from environment or file
    if os.path.exists('firebase-credentials.json'):
        cred = credentials.Certificate('firebase-credentials.json')
    else:
        # Use environment variable (for Railway deployment)
        firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
        if firebase_creds:
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
        else:
            raise Exception("Firebase credentials not found")
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    FIREBASE_ENABLED = True
    print("✅ Firebase initialized")
except Exception as e:
    FIREBASE_ENABLED = False
    db = None
    print(f"⚠️  Firebase not available: {e}")

# ============================================
# SUMMARY STATISTICS ENDPOINTS
# ============================================

@app.route('/api/stats/summary', methods=['GET'])
def get_summary_stats():
    """
    Get overall summary statistics from Firebase
    Returns: total tracks, avg metrics, tempo zones distribution
    """
    if not FIREBASE_ENABLED:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        # Get summary from Firebase (collection: 'audio_features_comparison')
        doc_ref = db.collection('audio_features_comparison').document('summary')
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Summary stats not found in Firebase'}), 404
        
        stats = doc.to_dict()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/tempo-zones', methods=['GET'])
def get_tempo_zones():
    """
    Get statistics grouped by tempo zones from Firebase
    Returns: distribution, averages per zone
    """
    if not FIREBASE_ENABLED:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        # Get tempo zones data (collection: 'audio_features_comparison/tempo_zones')
        zones_ref = db.collection('audio_features_comparison').document('tempo_zones')
        doc = zones_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Tempo zones not found'}), 404
        
        zones_data = doc.to_dict()
        
        return jsonify({
            'success': True,
            'zones': zones_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/ml-performance', methods=['GET'])
def get_ml_performance():
    """
    Get ML models performance metrics from Firebase
    Returns: accuracy, R², training results
    """
    if not FIREBASE_ENABLED:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        # Get ML performance (collection: 'ml_performance')
        doc_ref = db.collection('ml_performance').document('models')
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'ML performance data not found'}), 404
        
        performance = doc.to_dict()
        
        return jsonify({
            'success': True,
            'performance': performance
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# RECOMMENDATIONS ENDPOINTS
# ============================================

@app.route('/api/recommendations/zone/<zone_name>', methods=['GET'])
def get_recommendations_by_zone(zone_name):
    """
    Get top recommended tracks for a specific tempo zone
    Args:
        zone_name: sweet_spot, slow, moderate_slow, fast, very_fast, other_tempo
    Query params:
        limit: number of recommendations (default: 10)
    """
    if not FIREBASE_ENABLED:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        limit = min(int(request.args.get('limit', 10)), 50)
        
        # Get zone data from Firebase
        doc_ref = db.collection('other_tempo').document(zone_name)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': f'No data found for zone: {zone_name}'}), 404
        
        data = doc.to_dict()
        
        return jsonify({
            'success': True,
            'zone': zone_name,
            'total_tracks': data.get('total_tracks', 0),
            'avg_danceability': data.get('avg_danceability', 0),
            'avg_energy': data.get('avg_energy', 0),
            'avg_valence': data.get('avg_valence', 0),
            'stats': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/top-tracks', methods=['GET'])
def get_top_tracks():
    """
    Get overall top tracks from Firebase
    Query params:
        limit: number of tracks (default: 20)
    """
    if not FIREBASE_ENABLED:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Get top tracks (collection: 'audio_features_comparison/top_tracks')
        doc_ref = db.collection('audio_features_comparison').document('top_tracks')
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Top tracks not found'}), 404
        
        data = doc.to_dict()
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# SEARCH ENDPOINTS (Optional - sample data)
# ============================================

@app.route('/api/search/tracks', methods=['GET'])
def search_tracks():
    """
    Search tracks - returns sample data since full DB is local
    For demo purposes only
    """
    query = request.args.get('q', '').strip().lower()
    
    # Sample tracks for demo
    sample_tracks = [
        {'id': '1', 'name': 'Shape of You', 'artists': 'Ed Sheeran', 'year': 2017, 'tempo': 96.0, 'danceability': 0.825, 'energy': 0.652, 'in_sweet_spot': True},
        {'id': '2', 'name': 'Blinding Lights', 'artists': 'The Weeknd', 'year': 2020, 'tempo': 171.0, 'danceability': 0.514, 'energy': 0.73, 'in_sweet_spot': False},
        {'id': '3', 'name': 'Levitating', 'artists': 'Dua Lipa', 'year': 2020, 'tempo': 103.0, 'danceability': 0.702, 'energy': 0.825, 'in_sweet_spot': True},
        {'id': '4', 'name': 'Someone You Loved', 'artists': 'Lewis Capaldi', 'year': 2019, 'tempo': 110.03, 'danceability': 0.504, 'energy': 0.405, 'in_sweet_spot': True},
        {'id': '5', 'name': 'Dance Monkey', 'artists': 'Tones and I', 'year': 2019, 'tempo': 98.0, 'danceability': 0.824, 'energy': 0.588, 'in_sweet_spot': True},
    ]
    
    if query:
        # Simple filter
        results = [t for t in sample_tracks if query in t['name'].lower() or query in t['artists'].lower()]
    else:
        results = sample_tracks
    
    return jsonify({
        'success': True,
        'count': len(results),
        'results': results,
        'note': 'Sample data for demo. Full 1.2M dataset available in local environment.'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'firebase': 'connected' if FIREBASE_ENABLED else 'disabled',
        'mode': 'production' if os.environ.get('RAILWAY_ENVIRONMENT') else 'development'
    })

# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', os.getenv('API_PORT', 5000)))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("="*60)
    print("  SPOTIFY FIREBASE API")
    print("="*60)
    print()
    print("Available endpoints:")
    print("  GET  /api/stats/summary          - Overall statistics")
    print("  GET  /api/stats/tempo-zones      - Tempo zones distribution")
    print("  GET  /api/stats/ml-performance   - ML models metrics")
    print("  GET  /api/recommendations/zone/<zone> - Top tracks by zone")
    print("  GET  /api/recommendations/top-tracks  - Overall top tracks")
    print("  GET  /api/search/tracks          - Search (sample data)")
    print("  GET  /api/health                 - Health check")
    print("  POST /api/predict                - ML predictions")
    print()
    print(f"Starting server on http://localhost:{port}")
    print(f"Environment: {'Production' if os.environ.get('RAILWAY_ENVIRONMENT') else 'Development'}")
    print(f"Firebase: {'✅ Enabled' if FIREBASE_ENABLED else '❌ Disabled'}")
    print("="*60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
