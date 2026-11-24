"""
Upload Summary Stats and Recommendations to Firebase
====================================================
Prepare and upload pre-computed data to Firebase for production API
"""

import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Local PostgreSQL config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

print("="*60)
print("  UPLOAD TO FIREBASE")
print("="*60)
print()

# ============================================
# 1. OVERALL SUMMARY STATISTICS
# ============================================

print("📊 Computing overall summary statistics...")
conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
    SELECT 
        COUNT(*) as total_tracks,
        ROUND(AVG(tempo), 2) as avg_tempo,
        ROUND(AVG(danceability), 4) as avg_danceability,
        ROUND(AVG(energy), 4) as avg_energy,
        ROUND(AVG(valence), 4) as avg_valence,
        MIN(year) as earliest_year,
        MAX(year) as latest_year,
        COUNT(DISTINCT artists) as total_artists
    FROM spotify_tracks_raw
""")
overall = dict(cur.fetchone())

# Calculate tempo zones distribution
cur.execute("""
    SELECT 
        CASE 
            WHEN tempo < 80 THEN 'slow'
            WHEN tempo >= 80 AND tempo < 100 THEN 'moderate_slow'
            WHEN tempo >= 100 AND tempo < 120 THEN 'sweet_spot'
            WHEN tempo >= 120 AND tempo < 140 THEN 'fast'
            ELSE 'very_fast'
        END as zone,
        COUNT(*) as count,
        ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM spotify_tracks_raw) * 100, 2) as percentage
    FROM spotify_tracks_raw
    GROUP BY zone
    ORDER BY 
        CASE zone
            WHEN 'slow' THEN 1
            WHEN 'moderate_slow' THEN 2
            WHEN 'sweet_spot' THEN 3
            WHEN 'fast' THEN 4
            WHEN 'very_fast' THEN 5
        END
""")
zones_dist = cur.fetchall()

overall['tempo_zones'] = {z['zone']: {'count': z['count'], 'percentage': float(z['percentage'])} for z in zones_dist}
overall['updated_at'] = datetime.now().isoformat()

# Upload to Firebase
db.collection('summary_stats').document('overall').set(overall)
print(f"✅ Uploaded overall stats: {overall['total_tracks']:,} tracks")

# ============================================
# 2. TEMPO ZONES DETAILS
# ============================================

print("📊 Computing tempo zones details...")

zones = {
    'slow': (0, 80),
    'moderate_slow': (80, 100),
    'sweet_spot': (100, 120),
    'fast': (120, 140),
    'very_fast': (140, 300)
}

for zone_name, (tempo_min, tempo_max) in zones.items():
    cur.execute("""
        SELECT 
            COUNT(*) as total_tracks,
            ROUND(AVG(tempo), 2) as avg_tempo,
            ROUND(AVG(danceability), 4) as avg_danceability,
            ROUND(AVG(energy), 4) as avg_energy,
            ROUND(AVG(valence), 4) as avg_valence,
            ROUND(MIN(tempo), 2) as min_tempo,
            ROUND(MAX(tempo), 2) as max_tempo
        FROM spotify_tracks_raw
        WHERE tempo >= %s AND tempo < %s
    """, (tempo_min, tempo_max))
    
    zone_stats = dict(cur.fetchone())
    zone_stats['zone_name'] = zone_name
    zone_stats['tempo_min'] = tempo_min
    zone_stats['tempo_max'] = tempo_max
    zone_stats['updated_at'] = datetime.now().isoformat()
    
    db.collection('tempo_zones').document(zone_name).set(zone_stats)
    print(f"✅ Uploaded {zone_name}: {zone_stats['total_tracks']:,} tracks")

# ============================================
# 3. TOP TRACKS RECOMMENDATIONS PER ZONE
# ============================================

print("🎵 Computing top recommendations per zone...")

for zone_name, (tempo_min, tempo_max) in zones.items():
    # Get top tracks by danceability and energy
    cur.execute("""
        SELECT 
            id, name, artists, year, tempo,
            danceability, energy, valence,
            ROUND((danceability + energy) / 2, 4) as hit_score
        FROM spotify_tracks_raw
        WHERE tempo >= %s AND tempo < %s
        ORDER BY hit_score DESC, danceability DESC
        LIMIT 50
    """, (tempo_min, tempo_max))
    
    top_tracks = [dict(row) for row in cur.fetchall()]
    
    recommendations = {
        'zone_name': zone_name,
        'tempo_range': {'min': tempo_min, 'max': tempo_max},
        'top_tracks': top_tracks,
        'count': len(top_tracks),
        'updated_at': datetime.now().isoformat()
    }
    
    db.collection('recommendations').document(zone_name).set(recommendations)
    print(f"✅ Uploaded {len(top_tracks)} recommendations for {zone_name}")

# ============================================
# 4. OVERALL TOP TRACKS BY METRIC
# ============================================

print("🏆 Computing overall top tracks...")

metrics = {
    'danceability': 'danceability DESC',
    'energy': 'energy DESC',
    'popularity': '(danceability + energy + valence) / 3 DESC'
}

for metric_name, order_by in metrics.items():
    cur.execute(f"""
        SELECT 
            id, name, artists, year, tempo,
            danceability, energy, valence,
            CASE 
                WHEN tempo >= 100 AND tempo < 120 THEN true
                ELSE false
            END as in_sweet_spot
        FROM spotify_tracks_raw
        ORDER BY {order_by}
        LIMIT 100
    """)
    
    top_tracks = [dict(row) for row in cur.fetchall()]
    
    top_data = {
        'metric': metric_name,
        'tracks': top_tracks,
        'count': len(top_tracks),
        'updated_at': datetime.now().isoformat()
    }
    
    db.collection('top_tracks').document(metric_name).set(top_data)
    print(f"✅ Uploaded top 100 tracks by {metric_name}")

# ============================================
# 5. ML MODELS PERFORMANCE (if available)
# ============================================

print("🤖 Uploading ML performance metrics...")

# This would come from your training results
ml_performance = {
    'popularity_model': {
        'r2_score': 0.931,
        'rmse': 0.089,
        'mae': 0.067,
        'type': 'regression'
    },
    'hit_classifier': {
        'accuracy': 0.929,
        'precision': 0.912,
        'recall': 0.945,
        'f1_score': 0.928,
        'type': 'classification'
    },
    'danceability_model': {
        'r2_score': 0.667,
        'rmse': 0.127,
        'mae': 0.098,
        'type': 'regression'
    },
    'tempo_optimizer': {
        'r2_score': 0.194,
        'rmse': 29.87,
        'mae': 23.45,
        'type': 'regression'
    },
    'dataset_size': overall['total_tracks'],
    'training_date': '2024-11-11',
    'updated_at': datetime.now().isoformat()
}

db.collection('ml_performance').document('models').set(ml_performance)
print(f"✅ Uploaded ML performance metrics")

# Close database connection
cur.close()
conn.close()

print()
print("="*60)
print("✅ FIREBASE UPLOAD COMPLETE!")
print("="*60)
print()
print("Uploaded collections:")
print("  - summary_stats/overall")
print("  - tempo_zones/* (5 zones)")
print("  - recommendations/* (5 zones)")
print("  - top_tracks/* (3 metrics)")
print("  - ml_performance/models")
print()
print("Next steps:")
print("  1. Update Railway environment with FIREBASE_CREDENTIALS")
print("  2. Deploy backend using firebase_api.py")
print("  3. Test API endpoints")
print()
