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

# Import and register recommendation blueprint
try:
    from recommendation_api import recommend_bp
    app.register_blueprint(recommend_bp, url_prefix='/api')
    print("✅ Recommendation endpoints loaded")
except Exception as e:
    print(f"⚠️  Recommendation endpoints not available: {e}")

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
      - q: search query (name or artist) (optional)
      - tempo_min: minimum tempo (optional)
      - tempo_max: maximum tempo (optional)
      - sort: sort by field (danceability, energy, tempo, year) (optional)
      - limit: max results (default: 20, max: 100)
      - top_hits: if true, filters for likely popular tracks (optional)
    """
    try:
        query = request.args.get('q', '').strip()
        tempo_min = request.args.get('tempo_min', type=float)
        tempo_max = request.args.get('tempo_max', type=float)
        sort_by = request.args.get('sort', 'danceability')  # Default sort
        limit = min(int(request.args.get('limit', 20)), 100)
        top_hits = request.args.get('top_hits', '').lower() == 'true'
        
        # Validate sort field
        valid_sorts = ['danceability', 'energy', 'tempo', 'year', 'valence', 'popularity']
        if sort_by not in valid_sorts:
            sort_by = 'danceability'
        
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
                END as in_sweet_spot,
                -- Popularity proxy: combination of features + balance
                (
                    danceability * 0.35 + 
                    energy * 0.35 + 
                    valence * 0.15 +
                    (1 - acousticness) * 0.10 +
                    (CASE WHEN year >= 2010 THEN (year - 2010) / 14.0 ELSE 0 END) * 0.05
                ) as popularity_score
            FROM spotify_tracks_raw
            WHERE 1=1
        """
        params = []
        
        # Filter for top hits (much stricter criteria)
        if top_hits:
            # List of popular artists (mainstream acts)
            popular_artists = [
                'Drake', 'Taylor Swift', 'Ed Sheeran', 'The Weeknd', 'Ariana Grande',
                'Post Malone', 'Billie Eilish', 'Justin Bieber', 'Dua Lipa', 'Harry Styles',
                'Bruno Mars', 'Daft Punk', 'Calvin Harris', 'Rihanna', 'Beyoncé',
                'Adele', 'Coldplay', 'Maroon 5', 'Imagine Dragons', 'OneRepublic',
                'Sia', 'Katy Perry', 'Lady Gaga', 'Sam Smith', 'Shawn Mendes',
                'Khalid', 'Halsey', 'Camila Cabello', 'Olivia Rodrigo', 'BTS',
                'Bad Bunny', 'J Balvin', 'The Chainsmokers', 'Marshmello', 'David Guetta',
                'Avicii', 'Martin Garrix', 'Zedd', 'Kygo', 'Ellie Goulding',
                'Miley Cyrus', 'Selena Gomez', 'Jonas Brothers', 'Charlie Puth', 'Troye Sivan'
            ]
            
            # Build artist filter with ILIKE for case-insensitive partial matching
            artist_conditions = " OR ".join([f"LOWER(artists) LIKE %s" for _ in popular_artists])
            sql += f" AND ({artist_conditions})"
            params.extend([f"%{artist.lower()}%" for artist in popular_artists])
            
            # Additional quality filters
            sql += """ 
                AND danceability > 0.5
                AND energy > 0.4
                AND valence > 0.2
                AND year >= 2010
                AND year <= 2024
                AND instrumentalness < 0.5
                AND speechiness < 0.4
                AND acousticness < 0.7
                AND duration_ms BETWEEN 120000 AND 360000
            """
        
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
        
        # Add ORDER BY based on sort parameter
        if sort_by == 'popularity':
            sql += " ORDER BY popularity_score DESC, year DESC"
        elif sort_by == 'year':
            sql += " ORDER BY year DESC NULLS LAST"
        elif sort_by == 'tempo':
            sql += " ORDER BY tempo DESC"
        else:
            # For danceability, energy, valence - DESC order
            sql += f" ORDER BY {sort_by} DESC, year DESC"
        
        sql += f" LIMIT %s"
        params.append(limit)
        
        cur.execute(sql, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(results),
            'sort': sort_by,
            'top_hits_filter': top_hits,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-tracks', methods=['GET'])
def get_top_tracks():
    """
    Get pre-computed top tracks from materialized view
    Much faster and more accurate than on-the-fly filtering
    
    Query params:
      - sort: sort by field (popularity, danceability, energy, year) (optional, default: popularity)
      - artist: filter by specific artist (optional)
      - zone: filter by tempo zone (sweet_spot, slow, moderate, upbeat, fast) (optional)
      - limit: max results (default: 20, max: 200)
    """
    try:
        sort_by = request.args.get('sort', 'popularity')
        artist_filter = request.args.get('artist', '').strip()
        zone_filter = request.args.get('zone', '').strip()
        limit = min(int(request.args.get('limit', 20)), 200)
        
        # Validate sort field
        valid_sorts = {
            'popularity': 'popularity_score DESC',
            'danceability': 'danceability DESC',
            'energy': 'energy DESC',
            'year': 'year DESC',
            'tempo': 'tempo',
            'hit_potential': 'hit_potential DESC'
        }
        
        order_by = valid_sorts.get(sort_by, 'popularity_score DESC')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build query from materialized view
        sql = """
            SELECT 
                id, name, artists, year, tempo,
                danceability, energy, valence,
                acousticness, instrumentalness,
                liveness, speechiness, loudness,
                duration_ms, matched_artist,
                tempo_zone, in_sweet_spot,
                ROUND(popularity_score::numeric, 4) as popularity_score,
                ROUND(hit_potential::numeric, 4) as hit_potential
            FROM top_tracks_view
            WHERE 1=1
        """
        params = []
        
        # Optional filters
        if artist_filter:
            sql += " AND LOWER(matched_artist) = LOWER(%s)"
            params.append(artist_filter)
        
        if zone_filter:
            sql += " AND tempo_zone = %s"
            params.append(zone_filter)
        
        sql += f" ORDER BY {order_by} LIMIT %s"
        params.append(limit)
        
        cur.execute(sql, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(results),
            'sort': sort_by,
            'filters': {
                'artist': artist_filter if artist_filter else None,
                'zone': zone_filter if zone_filter else None
            },
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/top-tracks/stats', methods=['GET'])
def get_top_tracks_stats():
    """Get statistics about top tracks materialized view"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get overall stats
        cur.execute("""
            SELECT 
                COUNT(*) as total_tracks,
                COUNT(DISTINCT matched_artist) as unique_artists,
                MIN(year) as earliest_year,
                MAX(year) as latest_year,
                ROUND(AVG(popularity_score)::numeric, 3) as avg_popularity,
                COUNT(*) FILTER (WHERE in_sweet_spot) as sweet_spot_tracks,
                ROUND(AVG(tempo)::numeric, 1) as avg_tempo,
                ROUND(AVG(danceability)::numeric, 3) as avg_danceability,
                ROUND(AVG(energy)::numeric, 3) as avg_energy
            FROM top_tracks_view
        """)
        stats = cur.fetchone()
        
        # Get top artists by track count
        cur.execute("""
            SELECT 
                matched_artist,
                COUNT(*) as track_count,
                ROUND(AVG(popularity_score)::numeric, 3) as avg_score
            FROM top_tracks_view
            GROUP BY matched_artist
            ORDER BY track_count DESC
            LIMIT 10
        """)
        top_artists = cur.fetchall()
        
        # Get zone distribution
        cur.execute("""
            SELECT 
                tempo_zone,
                COUNT(*) as count,
                ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER())::numeric, 2) as percentage
            FROM top_tracks_view
            GROUP BY tempo_zone
            ORDER BY count DESC
        """)
        zones = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'top_artists': top_artists,
            'tempo_zones': zones
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
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
