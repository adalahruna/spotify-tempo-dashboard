"""
Sync PostgreSQL Analysis Results to Firestore
Transfer aggregated data (NOT raw 1.2M records!)
"""

import subprocess
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

# ==============================================
# CONFIGURATION
# ==============================================
POSTGRES_CONFIG = {
    'host': 'localhost',
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb',
    'port': 5432
}

PSQL_PATH = r'D:\postgre\bin\psql.exe'
FIREBASE_CRED_PATH = r'D:\Semester 5\BIG DATA\Project\firebase-credentials.json'

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def run_query(query):
    """Execute SQL query and return JSON result"""
    try:
        result = subprocess.run(
            [
                PSQL_PATH,
                '-U', POSTGRES_CONFIG['user'],
                '-h', POSTGRES_CONFIG['host'],
                '-p', str(POSTGRES_CONFIG['port']),
                '-d', POSTGRES_CONFIG['database'],
                '-t',  # Tuples only
                '-A',  # Unaligned
                '-F', '|',  # Field separator
                '-c', query
            ],
            env={**os.environ, 'PGPASSWORD': POSTGRES_CONFIG['password']},
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"   ❌ Query failed: {result.stderr}")
            return None
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def parse_psql_output(output, columns):
    """Parse psql output into list of dicts"""
    if not output:
        return []
    
    rows = []
    for line in output.split('\n'):
        if line.strip():
            values = line.split('|')
            if len(values) == len(columns):
                row = {}
                for i, col in enumerate(columns):
                    # Convert to appropriate type
                    val = values[i].strip()
                    if val == '':
                        row[col] = None
                    elif val.replace('.', '').replace('-', '').isdigit():
                        row[col] = float(val) if '.' in val else int(val)
                    else:
                        row[col] = val
                rows.append(row)
    return rows

# ==============================================
# DATA SYNC FUNCTIONS
# ==============================================

def sync_global_stats(db):
    """Sync global statistics"""
    print("\n📊 Syncing global statistics...")
    
    query = """
    SELECT 
        COUNT(*) as total_tracks,
        MIN(tempo) as min_tempo,
        MAX(tempo) as max_tempo,
        ROUND(AVG(tempo::numeric), 2) as avg_tempo,
        COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) as sweet_spot_count,
        ROUND((COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) * 100.0 / COUNT(*))::numeric, 2) as sweet_spot_percentage,
        MIN(year) as earliest_year,
        MAX(year) as latest_year
    FROM spotify_tracks_raw
    WHERE tempo IS NOT NULL;
    """
    
    result = run_query(query)
    if result:
        data = parse_psql_output(result, [
            'total_tracks', 'min_tempo', 'max_tempo', 'avg_tempo',
            'sweet_spot_count', 'sweet_spot_percentage', 
            'earliest_year', 'latest_year'
        ])
        
        if data:
            stats = data[0]
            stats['last_updated'] = datetime.now()
            
            db.collection('summary').document('global_stats').set(stats)
            print(f"   ✅ Global stats synced: {stats['total_tracks']:,} tracks")
            return True
    
    return False

def sync_tempo_zones(db):
    """Sync tempo zone distribution"""
    print("\n📊 Syncing tempo zones...")
    
    query = """
    SELECT 
        CASE 
            WHEN tempo < 80 THEN 'less_80'
            WHEN tempo < 100 THEN '80_100'
            WHEN tempo <= 120 THEN '100_120'
            WHEN tempo <= 140 THEN '120_140'
            ELSE 'above_140'
        END as zone_id,
        CASE 
            WHEN tempo < 80 THEN '<80 BPM'
            WHEN tempo < 100 THEN '80-100 BPM'
            WHEN tempo <= 120 THEN '100-120 BPM (Sweet Spot)'
            WHEN tempo <= 140 THEN '120-140 BPM'
            ELSE '>140 BPM'
        END as zone_name,
        COUNT(*) as count,
        ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER())::numeric, 2) as percentage,
        ROUND(AVG(energy)::numeric, 3) as avg_energy,
        ROUND(AVG(danceability)::numeric, 3) as avg_danceability,
        ROUND(AVG(valence)::numeric, 3) as avg_valence
    FROM spotify_tracks_raw
    WHERE tempo IS NOT NULL
    GROUP BY zone_id, zone_name;
    """
    
    result = run_query(query)
    if result:
        zones = parse_psql_output(result, [
            'zone_id', 'zone_name', 'count', 'percentage',
            'avg_energy', 'avg_danceability', 'avg_valence'
        ])
        
        for zone in zones:
            zone['last_updated'] = datetime.now()
            db.collection('tempo_zones').document(zone['zone_id']).set(zone)
        
        print(f"   ✅ {len(zones)} tempo zones synced")
        return True
    
    return False

def sync_decade_trends(db):
    """Sync decade trends"""
    print("\n📊 Syncing decade trends...")
    
    query = """
    SELECT 
        FLOOR(year/10)*10 as decade,
        COUNT(*) as total_tracks,
        COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) as sweet_spot_tracks,
        ROUND((COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) * 100.0 / COUNT(*))::numeric, 2) as sweet_spot_pct,
        ROUND(AVG(energy)::numeric, 3) as avg_energy,
        ROUND(AVG(tempo)::numeric, 2) as avg_tempo
    FROM spotify_tracks_raw
    WHERE year IS NOT NULL AND tempo IS NOT NULL
    GROUP BY decade
    ORDER BY decade;
    """
    
    result = run_query(query)
    if result:
        decades = parse_psql_output(result, [
            'decade', 'total_tracks', 'sweet_spot_tracks', 
            'sweet_spot_pct', 'avg_energy', 'avg_tempo'
        ])
        
        for decade_data in decades:
            decade_data['last_updated'] = datetime.now()
            decade = str(int(decade_data['decade']))
            db.collection('decade_trends').document(decade).set(decade_data)
        
        print(f"   ✅ {len(decades)} decades synced")
        return True
    
    return False

def sync_top_tracks(db):
    """Sync top hit formula tracks"""
    print("\n📊 Syncing top tracks (hit formula)...")
    
    query = """
    SELECT 
        name, 
        artists, 
        year,
        ROUND(tempo::numeric, 2) as tempo,
        ROUND(energy::numeric, 3) as energy,
        ROUND(danceability::numeric, 3) as danceability,
        ROUND(valence::numeric, 3) as valence,
        ROUND(((energy + danceability + valence) / 3)::numeric, 3) as hit_score
    FROM spotify_tracks_raw
    WHERE tempo BETWEEN 100 AND 120
      AND energy > 0.7
      AND danceability > 0.6
    ORDER BY hit_score DESC
    LIMIT 100;
    """
    
    result = run_query(query)
    if result:
        tracks = parse_psql_output(result, [
            'name', 'artists', 'year', 'tempo', 'energy',
            'danceability', 'valence', 'hit_score'
        ])
        
        # Store as array in single document (easier to query)
        db.collection('top_tracks').document('sweet_spot_top_100').set({
            'tracks': tracks,
            'count': len(tracks),
            'last_updated': datetime.now(),
            'criteria': 'Sweet Spot (100-120 BPM) + Energy >0.7 + Danceability >0.6'
        })
        
        print(f"   ✅ {len(tracks)} top tracks synced")
        return True
    
    return False

def sync_audio_features_comparison(db):
    """Sync audio features comparison (sweet spot vs others)"""
    print("\n📊 Syncing audio features comparison...")
    
    query = """
    SELECT 
        CASE 
            WHEN tempo BETWEEN 100 AND 120 THEN 'sweet_spot'
            ELSE 'other_tempo'
        END as category,
        COUNT(*) as total_tracks,
        ROUND(AVG(energy::numeric), 3) as avg_energy,
        ROUND(AVG(danceability::numeric), 3) as avg_danceability,
        ROUND(AVG(valence::numeric), 3) as avg_valence,
        ROUND(AVG(acousticness::numeric), 3) as avg_acousticness,
        ROUND(AVG(instrumentalness::numeric), 3) as avg_instrumentalness,
        ROUND(AVG(loudness::numeric), 2) as avg_loudness
    FROM spotify_tracks_raw
    WHERE tempo IS NOT NULL
    GROUP BY category;
    """
    
    result = run_query(query)
    if result:
        comparisons = parse_psql_output(result, [
            'category', 'total_tracks', 'avg_energy', 'avg_danceability',
            'avg_valence', 'avg_acousticness', 'avg_instrumentalness', 'avg_loudness'
        ])
        
        for comp in comparisons:
            comp['last_updated'] = datetime.now()
            db.collection('audio_features_comparison').document(comp['category']).set(comp)
        
        print(f"   ✅ Audio features comparison synced")
        return True
    
    return False

# ==============================================
# MAIN
# ==============================================

def main():
    print("=" * 60)
    print("🔥 POSTGRESQL → FIRESTORE SYNC")
    print("=" * 60)
    
    # Initialize Firebase
    print("\n📋 Step 1: Initializing Firebase...")
    try:
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("   ✅ Firebase initialized!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Sync data
    print("\n📋 Step 2: Syncing data from PostgreSQL...")
    
    success_count = 0
    total_count = 5
    
    if sync_global_stats(db):
        success_count += 1
    
    if sync_tempo_zones(db):
        success_count += 1
    
    if sync_decade_trends(db):
        success_count += 1
    
    if sync_top_tracks(db):
        success_count += 1
    
    if sync_audio_features_comparison(db):
        success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    if success_count == total_count:
        print("✅ SYNC COMPLETE!")
    else:
        print(f"⚠️  PARTIAL SYNC: {success_count}/{total_count} completed")
    print("=" * 60)
    
    print("\n📊 Firestore Collections Created:")
    print("   • summary/global_stats")
    print("   • tempo_zones/ (5 documents)")
    print("   • decade_trends/ (14 documents)")
    print("   • top_tracks/sweet_spot_top_100")
    print("   • audio_features_comparison/ (2 documents)")
    
    print("\n🔗 View in Firebase Console:")
    print("   https://console.firebase.google.com/")
    
    print("\n💡 Total Firestore documents: ~22 (NOT 1.2M!)")
    print("   PostgreSQL = Heavy computation")
    print("   Firestore = Lightweight read layer")

if __name__ == "__main__":
    main()
