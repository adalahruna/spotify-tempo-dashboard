"""
Load Raw Spotify CSV to PostgreSQL - Simple Approach
Just create 1 flat table mirroring CSV structure
"""

import pandas as pd
import sys

# Try different imports
try:
    import psycopg2
    from psycopg2.extras import execute_batch
    HAS_PSYCOPG2 = True
except ImportError:
    print("⚠️  psycopg2 not found, trying psycopg3...")
    try:
        import psycopg
        HAS_PSYCOPG2 = False
    except ImportError:
        print("❌ Neither psycopg2 nor psycopg3 found!")
        print("Please install: pip install psycopg2-binary")
        sys.exit(1)

# Try SQLAlchemy import
try:
    from sqlalchemy import create_engine
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    print("⚠️  SQLAlchemy not found, will use manual insert (slower)")

# ==============================================
# CONFIGURATION
# ==============================================
DB_CONFIG = {
    'host': 'localhost',
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb',  # GANTI DENGAN PASSWORD KAMU!
    'port': 5432
}

CSV_PATH = r'd:\Semester 5\BIG DATA\Project\data\raw\tracks_features.csv'

# ==============================================
# MAIN FUNCTION
# ==============================================

def load_raw_data():
    print("="*70)
    print("🎵 LOADING RAW SPOTIFY DATA TO POSTGRESQL (SIMPLE FLAT TABLE)")
    print("="*70)
    
    # Step 1: Read CSV
    print("\n📂 Step 1: Reading CSV...")
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        print(f"✅ Loaded {len(df):,} tracks")
        print(f"📊 Columns: {df.columns.tolist()}")
        print(f"📏 Shape: {df.shape}")
    except FileNotFoundError:
        print(f"❌ File not found: {CSV_PATH}")
        print("💡 Make sure CSV file exists at specified path")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    # Step 2: Basic cleaning
    print("\n🧹 Step 2: Basic cleaning...")
    original_count = len(df)
    
    # Remove duplicates based on ID
    df = df.drop_duplicates(subset=['id'], keep='first')
    print(f"   Removed {original_count - len(df):,} duplicates")
    print(f"   Remaining: {len(df):,} tracks")
    
    # Step 3: Create database connection
    print("\n🔌 Step 3: Connecting to PostgreSQL...")
    try:
        if HAS_SQLALCHEMY:
            # Use SQLAlchemy (faster)
            print("   Using SQLAlchemy engine...")
            engine = create_engine(
                f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
                f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
            )
            print("✅ Connected to PostgreSQL (SQLAlchemy)")
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute("SELECT version();")
                version = result.fetchone()[0]
                print(f"📊 PostgreSQL: {version.split(',')[0]}")
        else:
            # Use psycopg2 directly (manual method)
            print("   Using psycopg2 direct connection...")
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"✅ Connected to PostgreSQL (psycopg2)")
            print(f"📊 PostgreSQL: {version.split(',')[0]}")
            cur.close()
            conn.close()
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n💡 Error type: {type(e).__name__}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify password in DB_CONFIG")
        print("   3. Ensure database 'spotify_music_db' exists")
        print("   4. Try: pip install --upgrade psycopg2-binary sqlalchemy")
        sys.exit(1)
    
    # Step 4: Drop existing table if any
    print("\n🗑️  Step 4: Dropping existing table (if any)...")
    try:
        with engine.connect() as conn:
            conn.execute("DROP TABLE IF EXISTS spotify_tracks_raw CASCADE;")
            conn.commit()
        print("✅ Old table dropped")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    # Step 5: Load data to PostgreSQL
    print("\n💾 Step 5: Loading data to PostgreSQL...")
    print("   This may take 5-10 minutes for 1.2M records...")
    
    try:
        if HAS_SQLALCHEMY:
            # Use to_sql with chunks for better performance
            df.to_sql(
                name='spotify_tracks_raw',
                con=engine,
                if_exists='replace',
                index=False,
                chunksize=10000,
                method='multi'
            )
            print("✅ Data loaded successfully!")
        else:
            # Manual insert using psycopg2
            print("   Using manual INSERT (may be slower)...")
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            
            # Create table
            columns_def = ", ".join([f'"{col}" TEXT' for col in df.columns])
            cur.execute(f"DROP TABLE IF EXISTS spotify_tracks_raw CASCADE;")
            cur.execute(f"CREATE TABLE spotify_tracks_raw ({columns_def});")
            
            # Insert data in batches
            columns = df.columns.tolist()
            batch_size = 5000
            total_batches = len(df) // batch_size + 1
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                values = [tuple(row) for row in batch.values]
                
                placeholders = ','.join(['%s'] * len(columns))
                insert_query = f"INSERT INTO spotify_tracks_raw VALUES ({placeholders})"
                
                execute_batch(cur, insert_query, values, page_size=1000)
                
                progress = min((i + batch_size), len(df))
                print(f"   Progress: {progress:,} / {len(df):,} ({progress/len(df)*100:.1f}%)", end='\r')
            
            conn.commit()
            cur.close()
            conn.close()
            print("\n✅ Data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)
    
    # Step 6: Create indexes for better query performance
    print("\n📇 Step 6: Creating indexes...")
    try:
        with engine.connect() as conn:
            # Index on ID (primary key)
            conn.execute("""
                ALTER TABLE spotify_tracks_raw 
                ADD PRIMARY KEY (id);
            """)
            print("   ✅ Primary key on 'id'")
            
            # Index on tempo (for analysis)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tempo 
                ON spotify_tracks_raw(tempo);
            """)
            print("   ✅ Index on 'tempo'")
            
            # Index on popularity
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_popularity 
                ON spotify_tracks_raw(popularity);
            """)
            print("   ✅ Index on 'popularity'")
            
            # Index on year
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_year 
                ON spotify_tracks_raw(year);
            """)
            print("   ✅ Index on 'year'")
            
            conn.commit()
        
    except Exception as e:
        print(f"⚠️  Warning creating indexes: {e}")
    
    # Step 7: Verify data
    print("\n✅ Step 7: Verification...")
    try:
        with engine.connect() as conn:
            # Count records
            result = conn.execute("SELECT COUNT(*) FROM spotify_tracks_raw;")
            count = result.fetchone()[0]
            print(f"   Total records in database: {count:,}")
            
            # Sample data
            result = conn.execute("""
                SELECT id, name, artists, tempo, popularity 
                FROM spotify_tracks_raw 
                LIMIT 5;
            """)
            print("\n   📋 Sample data:")
            for row in result:
                print(f"      {row[1][:40]:40} | {row[2][:30]:30} | Tempo: {row[3]:6.2f} | Pop: {row[4]}")
            
            # Stats
            result = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    MIN(tempo) as min_tempo,
                    MAX(tempo) as max_tempo,
                    ROUND(AVG(tempo)::numeric, 2) as avg_tempo,
                    MIN(year) as min_year,
                    MAX(year) as max_year
                FROM spotify_tracks_raw
                WHERE tempo IS NOT NULL;
            """)
            stats = result.fetchone()
            print(f"\n   📊 Statistics:")
            print(f"      Total tracks: {stats[0]:,}")
            print(f"      Tempo range: {stats[1]:.2f} - {stats[2]:.2f} BPM")
            print(f"      Avg tempo: {stats[3]} BPM")
            print(f"      Year range: {stats[4]} - {stats[5]}")
    
    except Exception as e:
        print(f"⚠️  Error during verification: {e}")
    
    # Done
    print("\n" + "="*70)
    print("✅ RAW DATA SUCCESSFULLY LOADED TO POSTGRESQL!")
    print("="*70)
    print(f"\n📊 Table: spotify_tracks_raw")
    print(f"📍 Database: {DB_CONFIG['database']}")
    print(f"🖥️  Host: {DB_CONFIG['host']}")
    print(f"\n💡 Next steps:")
    print("   1. Query data: psql -U postgres -d spotify_music_db")
    print("   2. Run analysis: SELECT * FROM spotify_tracks_raw LIMIT 10;")
    print("   3. Create views or derived tables as needed")
    print()

# ==============================================
# RUN
# ==============================================
if __name__ == "__main__":
    try:
        load_raw_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
