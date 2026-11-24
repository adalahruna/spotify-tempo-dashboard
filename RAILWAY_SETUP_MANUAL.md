# 🚂 Railway Database Setup - Manual Steps

## Step 1: Get DATABASE_URL

1. Go to Railway Dashboard: https://railway.app
2. Open your project: **sunny-beauty**
3. Click on **PostgreSQL** service
4. Go to **"Variables"** tab
5. Copy the **`DATABASE_URL`** value

Should look like:
```
postgresql://postgres:xxxxx@containers-us-west-xxx.railway.app:5432/railway
```

---

## Step 2: Create Tables via Railway Query Tab

1. In PostgreSQL service, click **"Query"** tab
2. Copy-paste this SQL and run:

```sql
-- Create spotify_tracks_raw table
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
    time_signature INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_tempo ON spotify_tracks_raw(tempo);
CREATE INDEX IF NOT EXISTS idx_year ON spotify_tracks_raw(year);
CREATE INDEX IF NOT EXISTS idx_danceability ON spotify_tracks_raw(danceability);
CREATE INDEX IF NOT EXISTS idx_name ON spotify_tracks_raw USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_artists ON spotify_tracks_raw USING gin(to_tsvector('english', artists));

-- Insert sample data
INSERT INTO spotify_tracks_raw 
    (id, name, artists, year, tempo, danceability, energy, valence, 
     acousticness, instrumentalness, liveness, speechiness, loudness, 
     duration_ms, key, mode, time_signature)
VALUES 
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
ON CONFLICT (id) DO NOTHING;

-- Verify
SELECT COUNT(*) as total_tracks FROM spotify_tracks_raw;
SELECT name, artists, tempo FROM spotify_tracks_raw LIMIT 5;
```

---

## Step 3: Verify API Works

Test your Railway API:

```bash
# Replace with your Railway URL
curl https://YOUR-APP.railway.app/api/health

# Should return:
# {"status":"healthy","database":"connected"}
```

---

## Step 4: Import Full Dataset (Optional)

If you want to import your full 1.2M tracks dataset:

### Option A: Use psql command line
```bash
psql $DATABASE_URL < database/dump.sql
```

### Option B: Use Python script locally
```python
import psycopg2
import pandas as pd

# Read your CSV
df = pd.read_csv('data/processed/spotify_cleaned.csv')

# Connect
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Insert in batches
for i in range(0, len(df), 1000):
    batch = df.iloc[i:i+1000]
    # ... insert batch
```

### Option C: Use Railway Data Import (CSV)
1. Go to PostgreSQL service → "Data" tab
2. Click "Import"
3. Upload CSV file
4. Map columns

---

## ✅ Done!

Your API should now work:
- **Backend:** https://YOUR-APP.railway.app
- **Health check:** https://YOUR-APP.railway.app/api/health
- **Search:** https://YOUR-APP.railway.app/api/search/tracks?q=shape

Next: Deploy frontend to Vercel!
