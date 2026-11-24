"""
Export Local PostgreSQL to Railway
===================================
Dump local database and import to Railway PostgreSQL
"""

import psycopg2
import os
import sys
from tqdm import tqdm

# Local database config
LOCAL_DB = {
    'host': 'localhost',
    'port': 5432,
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb'
}

# Railway database URL (from environment or input)
RAILWAY_DB_URL = os.getenv('DATABASE_URL') or input("Enter Railway DATABASE_URL: ")

def export_import_data():
    """Export from local and import to Railway in batches"""
    
    print("="*60)
    print("  EXPORT LOCAL → IMPORT TO RAILWAY")
    print("="*60)
    print()
    
    # Connect to local database
    print("📡 Connecting to LOCAL database...")
    local_conn = psycopg2.connect(**LOCAL_DB)
    local_cur = local_conn.cursor()
    
    # Connect to Railway database
    print("📡 Connecting to RAILWAY database...")
    railway_conn = psycopg2.connect(RAILWAY_DB_URL)
    railway_cur = railway_conn.cursor()
    
    # Create table on Railway
    print("📋 Creating table on Railway...")
    railway_cur.execute("""
        CREATE TABLE IF NOT EXISTS spotify_tracks_raw (
            id VARCHAR(50) PRIMARY KEY,
            name TEXT NOT NULL,
            artists TEXT NOT NULL,
            year INTEGER,
            tempo FLOAT,
            danceability FLOAT,
            energy FLOAT,
            valence FLOAT,
            acousticness FLOAT,
            instrumentalness FLOAT,
            liveness FLOAT,
            speechiness FLOAT,
            loudness FLOAT,
            duration_ms INTEGER,
            key INTEGER,
            mode INTEGER,
            time_signature INTEGER
        )
    """)
    railway_conn.commit()
    print("✅ Table created!")
    
    # Get total count
    print("📊 Counting local records...")
    local_cur.execute("SELECT COUNT(*) FROM spotify_tracks_raw")
    total = local_cur.fetchone()[0]
    print(f"Total records to import: {total:,}")
    print()
    
    # Export and import in batches
    batch_size = 5000
    offset = 0
    imported = 0
    
    print("🚀 Starting import...")
    with tqdm(total=total, desc="Importing") as pbar:
        while offset < total:
            # Fetch batch from local
            local_cur.execute(f"""
                SELECT id, name, artists, year, tempo, 
                       danceability, energy, valence,
                       acousticness, instrumentalness, 
                       liveness, speechiness, loudness,
                       duration_ms, key, mode, time_signature
                FROM spotify_tracks_raw
                ORDER BY id
                LIMIT {batch_size} OFFSET {offset}
            """)
            
            batch = local_cur.fetchall()
            if not batch:
                break
            
            # Insert batch to Railway
            insert_sql = """
                INSERT INTO spotify_tracks_raw 
                (id, name, artists, year, tempo, danceability, energy, valence,
                 acousticness, instrumentalness, liveness, speechiness, loudness,
                 duration_ms, key, mode, time_signature)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """
            
            railway_cur.executemany(insert_sql, batch)
            railway_conn.commit()
            
            imported += len(batch)
            offset += batch_size
            pbar.update(len(batch))
    
    # Create indexes
    print()
    print("📑 Creating indexes...")
    railway_cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tempo ON spotify_tracks_raw(tempo);
        CREATE INDEX IF NOT EXISTS idx_year ON spotify_tracks_raw(year);
        CREATE INDEX IF NOT EXISTS idx_danceability ON spotify_tracks_raw(danceability);
    """)
    railway_conn.commit()
    print("✅ Indexes created!")
    
    # Verify
    railway_cur.execute("SELECT COUNT(*) FROM spotify_tracks_raw")
    final_count = railway_cur.fetchone()[0]
    
    # Close connections
    local_cur.close()
    local_conn.close()
    railway_cur.close()
    railway_conn.close()
    
    print()
    print("="*60)
    print("✅ IMPORT COMPLETE!")
    print("="*60)
    print(f"Total imported: {final_count:,} tracks")
    print()

if __name__ == '__main__':
    try:
        export_import_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
