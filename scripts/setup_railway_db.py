"""
Setup Railway PostgreSQL Database
==================================
Creates table schema and imports sample data
"""

import psycopg2
import os
import sys

def create_tables(conn):
    """Create spotify_tracks_raw table"""
    cur = conn.cursor()
    
    # Drop existing table if any
    print("🗑️  Dropping existing table (if exists)...")
    cur.execute("DROP TABLE IF EXISTS spotify_tracks_raw CASCADE")
    
    # Create table
    print("📋 Creating spotify_tracks_raw table...")
    create_sql = """
    CREATE TABLE spotify_tracks_raw (
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
        time_signature INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes for fast queries
    CREATE INDEX idx_tempo ON spotify_tracks_raw(tempo);
    CREATE INDEX idx_year ON spotify_tracks_raw(year);
    CREATE INDEX idx_danceability ON spotify_tracks_raw(danceability);
    CREATE INDEX idx_name ON spotify_tracks_raw USING gin(to_tsvector('english', name));
    CREATE INDEX idx_artists ON spotify_tracks_raw USING gin(to_tsvector('english', artists));
    """
    
    cur.execute(create_sql)
    conn.commit()
    print("✅ Table created successfully!")
    
    cur.close()

def insert_sample_data(conn):
    """Insert sample tracks for testing"""
    cur = conn.cursor()
    
    print("📝 Inserting sample data...")
    
    sample_tracks = [
        ('7qiZfU4dY1lWllzX7mPBI', 'Shape of You', 'Ed Sheeran', 2017, 96.0, 0.825, 0.652, 0.931, 0.581, 0.0, 0.0931, 0.0802, -3.183, 233713, 1, 0, 4),
        ('3n3Ppam7vgaVa1iaRUc9L', 'Blinding Lights', 'The Weeknd', 2020, 171.0, 0.514, 0.73, 0.336, 0.00146, 0.0, 0.0897, 0.0598, -5.934, 200040, 1, 1, 4),
        ('0VjIjW4GlUZAMYd2vXMi3', 'Blinding Lights', 'The Weeknd', 2019, 171.009, 0.514, 0.73, 0.336, 0.00146, 0.0, 0.0897, 0.0598, -5.934, 200040, 1, 1, 4),
        ('6habFhsOp2NvshLv26DqMb', 'Someone You Loved', 'Lewis Capaldi', 2019, 110.03, 0.504, 0.405, 0.0446, 0.751, 0.0, 0.0898, 0.0319, -4.672, 182160, 1, 1, 4),
        ('3ee8Jmje8o58CHK66QrVC2', 'Levitating (feat. DaBaby)', 'Dua Lipa, DaBaby', 2020, 103.0, 0.702, 0.825, 0.915, 0.0032, 0.0, 0.0674, 0.0696, -3.576, 203064, 6, 0, 4),
        ('11dFghVXANMlKmJXsNCbNl', 'Cut To The Feeling', 'Carly Rae Jepsen', 2017, 129.983, 0.635, 0.925, 0.661, 0.000589, 0.0, 0.0879, 0.0317, -4.047, 207173, 0, 1, 4),
        ('7ytR5pFWmSjzHJIeQkgog4', 'ROCKSTAR', 'DaBaby, Roddy Ricch', 2020, 90.047, 0.746, 0.677, 0.408, 0.138, 0.0, 0.123, 0.0962, -6.125, 181733, 5, 1, 4),
        ('0SF6TjJK6lSnlFLvP4mNyW', 'Mood (feat. iann dior)', '24kGoldn, iann dior', 2020, 91.033, 0.7, 0.722, 0.724, 0.267, 0.0, 0.335, 0.0369, -3.671, 140526, 8, 1, 4),
        ('2takcwOaAZWiXQijPHIx7B', 'Time', 'NF', 2019, 96.0, 0.479, 0.627, 0.0871, 0.000119, 0.0, 0.133, 0.228, -5.291, 229413, 10, 1, 4),
        ('5O2P9iiztwhomNh8xkR9lJ', 'MAMACITA', 'Black Eyed Peas, Ozuna, J. Rey Soul', 2020, 96.0, 0.736, 0.766, 0.68, 0.0119, 0.0, 0.14, 0.0631, -3.924, 215707, 8, 0, 4)
    ]
    
    insert_sql = """
    INSERT INTO spotify_tracks_raw 
        (id, name, artists, year, tempo, danceability, energy, valence, 
         acousticness, instrumentalness, liveness, speechiness, loudness, 
         duration_ms, key, mode, time_signature)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """
    
    cur.executemany(insert_sql, sample_tracks)
    conn.commit()
    
    # Count records
    cur.execute("SELECT COUNT(*) FROM spotify_tracks_raw")
    count = cur.fetchone()[0]
    
    print(f"✅ Inserted sample data! Total records: {count}")
    cur.close()

def main():
    """Main setup function"""
    print("="*60)
    print("  RAILWAY DATABASE SETUP")
    print("="*60)
    print()
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found!")
        print("   Make sure PostgreSQL is added to your Railway project")
        print("   and environment variables are loaded.")
        sys.exit(1)
    
    print(f"📡 Connecting to database...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        print("✅ Connected!")
        print()
        
        # Create tables
        create_tables(conn)
        print()
        
        # Insert sample data
        insert_sample_data(conn)
        print()
        
        # Test query
        print("🧪 Testing query...")
        cur = conn.cursor()
        cur.execute("SELECT name, artists, tempo FROM spotify_tracks_raw LIMIT 3")
        results = cur.fetchall()
        
        print("Sample tracks:")
        for row in results:
            print(f"  - {row[0]} by {row[1]} ({row[2]} BPM)")
        
        cur.close()
        conn.close()
        
        print()
        print("="*60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*60)
        print()
        print("Next steps:")
        print("1. Import your full dataset using similar INSERT statements")
        print("2. Or use COPY command for bulk import from CSV")
        print("3. Test API endpoints at your Railway URL")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
