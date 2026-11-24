"""
SEARCH API FOR DASHBOARD
========================
Flask API untuk search tracks dari PostgreSQL
Supports both local development and production deployment
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production-ready CORS configuration
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Production: Allow your Vercel domain + Railway domain
    vercel_domain = os.environ.get('VERCEL_DOMAIN', 'spotify-tempo-dashboard.vercel.app')
    cors_origins = [
        f'https://{vercel_domain}',
        f'https://*.vercel.app',  # All Vercel preview deployments
        'http://localhost:8000',  # Local testing
        'http://127.0.0.1:8000'
    ]
    print(f"🔐 CORS enabled for: {cors_origins}")
else:
    # Development: Allow localhost
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

# PostgreSQL connection config - gunakan env variables atau DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Parse DATABASE_URL untuk Heroku/Railway
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    DB_CONFIG = {
        'host': url.hostname,
        'port': url.port,
        'database': url.path[1:],
        'user': url.username,
        'password': url.password
    }
else:
    # Gunakan individual env variables untuk local/custom deployment
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'spotify_music_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'runadb')
    }

def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# ============================================
# SEARCH ENDPOINTS
# ============================================

@app.route('/api/search/tracks', methods=['GET'])
def search_tracks():
    """
    Search tracks by name, artist, or tempo
    Query params:
      - q: search query (name or artist)
      - tempo_min: minimum tempo (optional)
      - tempo_max: maximum tempo (optional)
      - limit: max results (default: 20, max: 100)
    """
    try:
        query = request.args.get('q', '').strip()
        tempo_min = request.args.get('tempo_min', type=float)
        tempo_max = request.args.get('tempo_max', type=float)
        limit = min(int(request.args.get('limit', 20)), 100)
        
        if not query and tempo_min is None and tempo_max is None:
            return jsonify({'error': 'Provide search query (q) or tempo range'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build SQL query
        sql = """
            SELECT 
                id, name, artists, year, tempo, 
                danceability, energy, valence,
                acousticness, instrumentalness, 
                liveness, speechiness, loudness,
                duration_ms,
                CASE 
                    WHEN tempo >= 100 AND tempo < 120 THEN true
                    ELSE false
                END as in_sweet_spot
            FROM spotify_tracks_raw
            WHERE 1=1
        """
        params = []
        
        # Add search conditions
        if query:
            sql += " AND (LOWER(name) LIKE %s OR LOWER(artists) LIKE %s)"
            search_pattern = f"%{query.lower()}%"
            params.extend([search_pattern, search_pattern])
        
        if tempo_min is not None:
            sql += " AND tempo >= %s"
            params.append(tempo_min)
        
        if tempo_max is not None:
            sql += " AND tempo <= %s"
            params.append(tempo_max)
        
        sql += f" ORDER BY year DESC, danceability DESC LIMIT %s"
        params.append(limit)
        
        cur.execute(sql, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/artists', methods=['GET'])
def search_artists():
    """
    Search tracks by specific artist
    Query params:
      - artist: artist name (required)
      - limit: max results (default: 50)
    """
    try:
        artist = request.args.get('artist', '').strip()
        limit = min(int(request.args.get('limit', 50)), 200)
        
        if not artist:
            return jsonify({'error': 'Artist name required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        sql = """
            SELECT 
                name, artists, year, tempo, 
                danceability, energy, valence,
                CASE 
                    WHEN tempo >= 100 AND tempo < 120 THEN 'sweet_spot'
                    WHEN tempo < 80 THEN 'slow'
                    WHEN tempo >= 80 AND tempo < 100 THEN 'moderate_slow'
                    WHEN tempo >= 120 AND tempo < 140 THEN 'fast'
                    ELSE 'very_fast'
                END as tempo_zone
            FROM spotify_tracks_raw
            WHERE LOWER(artists) LIKE %s
            ORDER BY year DESC, danceability DESC
            LIMIT %s
        """
        
        cur.execute(sql, (f"%{artist.lower()}%", limit))
        results = cur.fetchall()
        
        # Calculate stats
        if results:
            tempos = [r['tempo'] for r in results]
            avg_tempo = sum(tempos) / len(tempos)
            sweet_spot_count = sum(1 for r in results if r['tempo_zone'] == 'sweet_spot')
            sweet_spot_pct = (sweet_spot_count / len(results) * 100)
            
            stats = {
                'total_tracks': len(results),
                'avg_tempo': round(avg_tempo, 2),
                'sweet_spot_tracks': sweet_spot_count,
                'sweet_spot_percentage': round(sweet_spot_pct, 2)
            }
        else:
            stats = None
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'artist': artist,
            'stats': stats,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/tempo-range', methods=['GET'])
def search_tempo_range():
    """
    Get tracks within specific tempo range with pagination
    Query params:
      - min: min tempo (required)
      - max: max tempo (required)
      - offset: pagination offset (default: 0)
      - limit: max results (default: 20, max: 100)
    """
    try:
        tempo_min = request.args.get('min', type=float)
        tempo_max = request.args.get('max', type=float)
        offset = request.args.get('offset', 0, type=int)
        limit = min(int(request.args.get('limit', 20)), 100)
        
        if tempo_min is None or tempo_max is None:
            return jsonify({'error': 'Both min and max tempo required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Count total
        count_sql = """
            SELECT COUNT(*) as total
            FROM spotify_tracks_raw
            WHERE tempo >= %s AND tempo <= %s
        """
        cur.execute(count_sql, (tempo_min, tempo_max))
        total = cur.fetchone()['total']
        
        # Get paginated results
        sql = """
            SELECT 
                name, artists, year, tempo, 
                danceability, energy, valence
            FROM spotify_tracks_raw
            WHERE tempo >= %s AND tempo <= %s
            ORDER BY danceability DESC, energy DESC
            LIMIT %s OFFSET %s
        """
        
        cur.execute(sql, (tempo_min, tempo_max, limit, offset))
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'tempo_range': {'min': tempo_min, 'max': tempo_max},
            'total': total,
            'offset': offset,
            'limit': limit,
            'count': len(results),
            'has_more': (offset + len(results)) < total,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/summary', methods=['GET'])
def get_summary_stats():
    """
    Get quick summary statistics (cached data from Firestore-like view)
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        sql = """
            SELECT 
                COUNT(*) as total_tracks,
                ROUND(AVG(tempo::numeric), 2) as avg_tempo,
                ROUND(AVG(danceability::numeric), 4) as avg_danceability,
                ROUND(AVG(energy::numeric), 4) as avg_energy,
                SUM(CASE WHEN tempo >= 100 AND tempo < 120 THEN 1 ELSE 0 END) as sweet_spot_tracks,
                ROUND(
                    SUM(CASE WHEN tempo >= 100 AND tempo < 120 THEN 1 ELSE 0 END)::NUMERIC / 
                    COUNT(*)::NUMERIC * 100, 
                    2
                ) as sweet_spot_percentage
            FROM spotify_tracks_raw
        """
        
        cur.execute(sql)
        stats = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': dict(stats)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', os.getenv('API_PORT', 5000)))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("="*60)
    print("  SPOTIFY SEARCH API")
    print("="*60)
    print()
    print("Available endpoints:")
    print("  GET  /api/search/tracks       - Search by name/artist/tempo")
    print("  GET  /api/search/artists      - Search by artist name")
    print("  GET  /api/search/tempo-range  - Get tracks in tempo range")
    print("  GET  /api/stats/summary       - Get summary statistics")
    print("  GET  /api/health              - Health check")
    print()
    print(f"Starting server on http://localhost:{port}")
    print(f"Environment: {'Development' if debug_mode else 'Production'}")
    print("="*60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
