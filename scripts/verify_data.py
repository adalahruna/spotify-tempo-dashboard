"""
Verification Script for PostgreSQL Data Load
Checks if all 1.2M Spotify tracks loaded successfully
"""

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
    'password': 'tempo2024',  # EDIT THIS!
    'port': 5432
}

PSQL_PATH = r'D:\postgre\bin\psql.exe'  # Edit if different

# Expected values
EXPECTED_TOTAL = 1204022

def run_query(query):
    """Execute SQL query via psql and return output"""
    try:
        result = subprocess.run(
            [
                PSQL_PATH,
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-t',  # Tuples only (no headers)
                '-A',  # Unaligned mode
                '-c', query
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ Query failed: {result.stderr}")
            return None
    
    except FileNotFoundError:
        print(f"❌ psql not found at: {PSQL_PATH}")
        sys.exit(1)

def main():
    print("=" * 60)
    print("🔍 SPOTIFY DATA VERIFICATION")
    print("=" * 60)
    
    # 1. Check total records
    print("\n📊 Step 1: Checking total records...")
    total = run_query("SELECT COUNT(*) FROM spotify_tracks_raw;")
    if total:
        total_int = int(total)
        print(f"   Total records: {total_int:,}")
        
        if total_int == EXPECTED_TOTAL:
            print(f"   ✅ PERFECT! All {EXPECTED_TOTAL:,} tracks loaded!")
        elif total_int > 0:
            diff = EXPECTED_TOTAL - total_int
            print(f"   ⚠️  Expected {EXPECTED_TOTAL:,}, got {total_int:,} (diff: {diff:,})")
        else:
            print("   ❌ No data found!")
            sys.exit(1)
    
    # 2. Check tempo stats
    print("\n📊 Step 2: Checking tempo statistics...")
    stats = run_query("""
        SELECT 
            MIN(tempo), 
            MAX(tempo), 
            ROUND(AVG(tempo::numeric), 2),
            COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END)
        FROM spotify_tracks_raw;
    """)
    
    if stats:
        parts = stats.split('|')
        print(f"   Min tempo: {parts[0]} BPM")
        print(f"   Max tempo: {parts[1]} BPM")
        print(f"   Avg tempo: {parts[2]} BPM")
        print(f"   Tracks in 100-120 BPM zone: {int(parts[3]):,}")
    
    # 3. Check year range
    print("\n📊 Step 3: Checking year range...")
    years = run_query("""
        SELECT MIN(year), MAX(year), COUNT(DISTINCT year)
        FROM spotify_tracks_raw;
    """)
    
    if years:
        parts = years.split('|')
        print(f"   Earliest year: {parts[0]}")
        print(f"   Latest year: {parts[1]}")
        print(f"   Unique years: {parts[2]}")
    
    # 4. Sample data
    print("\n📊 Step 4: Sample data (first 5 tracks)...")
    samples = run_query("""
        SELECT name || ' | ' || artists || ' | ' || tempo || ' BPM'
        FROM spotify_tracks_raw
        LIMIT 5;
    """)
    
    if samples:
        for i, line in enumerate(samples.split('\n'), 1):
            if line.strip():
                print(f"   {i}. {line}")
    
    # 5. Tempo zone distribution
    print("\n📊 Step 5: Tempo zone distribution...")
    zones = run_query("""
        SELECT 
            CASE 
                WHEN tempo < 100 THEN '<100 BPM'
                WHEN tempo <= 120 THEN '100-120 BPM (SWEET SPOT)'
                ELSE '>120 BPM'
            END as zone,
            COUNT(*),
            ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER())::numeric, 2)
        FROM spotify_tracks_raw
        WHERE tempo IS NOT NULL
        GROUP BY zone
        ORDER BY COUNT(*) DESC;
    """)
    
    if zones:
        print("   Zone                      | Count      | Percentage")
        print("   " + "-" * 54)
        for line in zones.split('\n'):
            if line.strip():
                parts = line.split('|')
                zone = parts[0].ljust(25)
                count = f"{int(parts[1]):,}".rjust(10)
                pct = parts[2].rjust(6)
                print(f"   {zone} | {count} | {pct}%")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ VERIFICATION COMPLETE!")
    print("=" * 60)
    print(f"\n💡 Database ready for analysis!")
    print(f"   • Total tracks: {total_int:,}")
    print(f"   • Ready for tempo sweet spot analysis (100-120 BPM)")
    print(f"   • Next step: Create analytical views + Firebase sync")

if __name__ == "__main__":
    main()
