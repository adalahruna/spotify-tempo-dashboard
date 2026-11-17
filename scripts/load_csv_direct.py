"""
Load CSV to PostgreSQL - DIRECT METHOD (No psycopg2 needed!)
Uses PostgreSQL COPY command via subprocess
"""

import pandas as pd
import subprocess
import sys
import os

# ==============================================
# CONFIGURATION
# ==============================================
DB_CONFIG = {
    'host': 'localhost',
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'runadb',  # GANTI!
    'port': 5432
}

CSV_PATH = r'd:\Semester 5\BIG DATA\Project\data\raw\tracks_features.csv'
TEMP_CLEANED_CSV = r'd:\Semester 5\BIG DATA\Project\data\temp_cleaned.csv'

# PostgreSQL bin path (EDIT SESUAI LOKASI INSTALL KAMU!)
PSQL_PATH = r'D:\postgre\bin\psql.exe'  # atau D:\PostgreSQL\18\bin\psql.exe

# ==============================================
# MAIN FUNCTION
# ==============================================

def load_data_direct():
    print("="*70)
    print("🎵 LOADING CSV TO POSTGRESQL - DIRECT COPY METHOD")
    print("="*70)
    
    # Step 1: Read and clean CSV
    print("\n📂 Step 1: Reading & cleaning CSV...")
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        print(f"✅ Loaded {len(df):,} tracks")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['id'])
        print(f"   After dedup: {len(df):,} tracks")
        
        # Save cleaned CSV (temp)
        df.to_csv(TEMP_CLEANED_CSV, index=False, encoding='utf-8')
        print(f"✅ Cleaned CSV saved: {TEMP_CLEANED_CSV}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Step 2: Create table via psql command
    print("\n🗄️  Step 2: Creating table...")
    
    # Get column names and types
    columns_def = []
    for col in df.columns:
        # Simple type inference
        if df[col].dtype == 'int64':
            col_type = 'INTEGER'
        elif df[col].dtype == 'float64':
            col_type = 'DOUBLE PRECISION'
        elif df[col].dtype == 'bool':
            col_type = 'BOOLEAN'
        else:
            col_type = 'TEXT'
        columns_def.append(f'"{col}" {col_type}')
    
    create_table_sql = f"""
    DROP TABLE IF EXISTS spotify_tracks_raw CASCADE;
    CREATE TABLE spotify_tracks_raw (
        {', '.join(columns_def)}
    );
    """
    
    # Save SQL to temp file
    sql_file = r'd:\Semester 5\BIG DATA\Project\data\create_table.sql'
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(create_table_sql)
    
    # Execute via psql
    try:
        result = subprocess.run(
            [
                PSQL_PATH,  # Use full path
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-f', sql_file
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Table created successfully")
        else:
            print(f"❌ Error creating table: {result.stderr}")
            sys.exit(1)
    
    except FileNotFoundError:
        print(f"❌ psql not found at: {PSQL_PATH}")
        print("💡 Check your PostgreSQL installation path")
        print("   Common locations:")
        print("   - D:\\PostgreSQL\\18\\bin\\psql.exe")
        print("   - D:\\postgre\\bin\\psql.exe")
        print("   - C:\\Program Files\\PostgreSQL\\18\\bin\\psql.exe")
        sys.exit(1)
    
    # Step 3: Load data via COPY command
    print("\n💾 Step 3: Loading data (COPY command)...")
    print("   This is FAST - may take 1-2 minutes...")
    
    copy_sql = f"""
    \\COPY spotify_tracks_raw FROM '{TEMP_CLEANED_CSV}' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8');
    """
    
    copy_file = r'd:\Semester 5\BIG DATA\Project\data\copy_data.sql'
    with open(copy_file, 'w', encoding='utf-8') as f:
        f.write(copy_sql)
    
    try:
        result = subprocess.run(
            [
                PSQL_PATH,  # Use full path
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-f', copy_file
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Data loaded successfully!")
            print(result.stdout)
        else:
            print(f"❌ Error loading data: {result.stderr}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Step 4: Create indexes
    print("\n📇 Step 4: Creating indexes...")
    
    index_sql = """
    ALTER TABLE spotify_tracks_raw ADD PRIMARY KEY (id);
    CREATE INDEX idx_tempo ON spotify_tracks_raw(tempo);
    CREATE INDEX idx_popularity ON spotify_tracks_raw(popularity);
    CREATE INDEX idx_year ON spotify_tracks_raw(year);
    """
    
    index_file = r'd:\Semester 5\BIG DATA\Project\data\create_indexes.sql'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_sql)
    
    try:
        result = subprocess.run(
            [
                PSQL_PATH,  # Use full path
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-f', index_file
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Indexes created")
        else:
            print(f"⚠️  Warning: {result.stderr}")
    
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    # Step 5: Verify
    print("\n✅ Step 5: Verification...")
    
    verify_sql = """
    SELECT COUNT(*) FROM spotify_tracks_raw;
    SELECT MIN(tempo), MAX(tempo), ROUND(AVG(tempo)::numeric, 2) FROM spotify_tracks_raw;
    """
    
    verify_file = r'd:\Semester 5\BIG DATA\Project\data\verify.sql'
    with open(verify_file, 'w', encoding='utf-8') as f:
        f.write(verify_sql)
    
    try:
        result = subprocess.run(
            [
                PSQL_PATH,  # Use full path
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-f', verify_file
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
    
    except Exception as e:
        print(f"⚠️  {e}")
    
    # Cleanup temp files
    print("\n🧹 Cleaning up temp files...")
    try:
        os.remove(TEMP_CLEANED_CSV)
        os.remove(sql_file)
        os.remove(copy_file)
        os.remove(index_file)
        os.remove(verify_file)
        print("✅ Cleanup done")
    except:
        pass
    
    print("\n" + "="*70)
    print("✅ DATA LOADED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📊 Table: spotify_tracks_raw")
    print(f"📍 Database: {DB_CONFIG['database']}")
    print("\n💡 Query data:")
    print("   psql -U postgres -d spotify_music_db")
    print("   SELECT * FROM spotify_tracks_raw LIMIT 10;")
    print()

# ==============================================
# RUN
# ==============================================
if __name__ == "__main__":
    try:
        load_data_direct()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        sys.exit(1)
