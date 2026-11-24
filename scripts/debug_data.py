import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="spotify_music_db",
    user="postgres",
    password="runadb"
)

# Load sample data
query = """
    SELECT 
        tempo, energy, danceability, valence, acousticness,
        instrumentalness, liveness, speechiness, loudness,
        duration_ms, year, key, mode, time_signature
    FROM spotify_tracks_raw
    WHERE 
        tempo IS NOT NULL 
        AND energy IS NOT NULL 
        AND danceability IS NOT NULL
        AND year IS NOT NULL
    LIMIT 5
"""

df = pd.read_sql(query, conn)
conn.close()

print("DataFrame Info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nSample values:")
for col in df.columns:
    print(f"{col}: {df[col].iloc[0]} (type: {type(df[col].iloc[0])})")
