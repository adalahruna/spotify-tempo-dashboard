"""
Data Cleaning & Preprocessing
Spotify 1.2M+ Tracks Dataset
"""

import pandas as pd
import numpy as np
import ast
import warnings
warnings.filterwarnings('ignore')

print("📦 Libraries loaded successfully!")
print("="*60)

# 1. Load Dataset
print("\n1️⃣ LOADING DATASET...")
df = pd.read_csv('../data/raw/tracks_features.csv')
print(f"✅ Dataset loaded!")
print(f"Shape: {df.shape}")
print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 2. Data Quality Check
print("\n2️⃣ DATA QUALITY CHECK...")
print("=== MISSING VALUES ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing': missing[missing > 0],
    'Percentage': missing_pct[missing > 0]
}).sort_values('Missing', ascending=False)
if len(missing_df) > 0:
    print(missing_df)
else:
    print("No missing values!")

# 3. Handle Missing Values
print("\n3️⃣ HANDLING MISSING VALUES...")
df_clean = df.dropna(subset=['name']).copy()
df_clean['album'] = df_clean['album'].fillna('Unknown Album')
print(f"✅ Cleaned {len(df) - len(df_clean)} rows with missing critical data")
print(f"Remaining rows: {len(df_clean):,}")

# 4. Parse Artists & Artist IDs
print("\n4️⃣ PARSING ARTISTS...")
def safe_parse_list(x):
    """Safely parse string representation of list"""
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except:
        return [str(x)]

df_clean['artists_list'] = df_clean['artists'].apply(safe_parse_list)
df_clean['artist_ids_list'] = df_clean['artist_ids'].apply(safe_parse_list)
df_clean['primary_artist'] = df_clean['artists_list'].apply(lambda x: x[0] if len(x) > 0 else 'Unknown')
df_clean['primary_artist_id'] = df_clean['artist_ids_list'].apply(lambda x: x[0] if len(x) > 0 else 'unknown')
df_clean['num_artists'] = df_clean['artists_list'].apply(len)
df_clean['is_collab'] = df_clean['num_artists'] > 1

print(f"✅ Artists parsed successfully!")
print(f"Total unique artists: {df_clean['primary_artist'].nunique():,}")
print(f"Collaboration tracks: {df_clean['is_collab'].sum():,} ({df_clean['is_collab'].mean()*100:.1f}%)")

# 5. Add Decade & Era Features
print("\n5️⃣ ADDING TEMPORAL FEATURES...")
df_clean['decade'] = (df_clean['year'] // 10) * 10

def categorize_era(year):
    if year < 2000:
        return 'Pre-2000'
    elif year < 2011:
        return '2000-2010'
    elif year < 2021:
        return '2011-2020 (Streaming Era)'
    else:
        return '2021+'

df_clean['era'] = df_clean['year'].apply(categorize_era)
print("✅ Temporal features added!")
print("\n=== TRACKS BY ERA ===")
print(df_clean['era'].value_counts().sort_index())

# 6. Data Type Optimization
print("\n6️⃣ OPTIMIZING DATA TYPES...")
df_clean['explicit'] = df_clean['explicit'].astype('int8')
df_clean['is_collab'] = df_clean['is_collab'].astype('int8')
df_clean['track_number'] = df_clean['track_number'].astype('int16')
df_clean['disc_number'] = df_clean['disc_number'].astype('int8')
df_clean['key'] = df_clean['key'].astype('int8')
df_clean['mode'] = df_clean['mode'].astype('int8')
df_clean['time_signature'] = df_clean['time_signature'].astype('int8')
df_clean['year'] = df_clean['year'].astype('int16')
df_clean['decade'] = df_clean['decade'].astype('int16')
df_clean['num_artists'] = df_clean['num_artists'].astype('int8')

float_cols = ['danceability', 'energy', 'loudness', 'speechiness', 
              'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
for col in float_cols:
    df_clean[col] = df_clean[col].astype('float32')

print(f"✅ Data types optimized!")
print(f"Memory after optimization: {df_clean.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 7. Summary Statistics
print("\n7️⃣ SUMMARY STATISTICS...")
print("=== DATASET SUMMARY ===")
print(f"Total Tracks: {len(df_clean):,}")
print(f"Unique Artists: {df_clean['primary_artist'].nunique():,}")
print(f"Unique Albums: {df_clean['album'].nunique():,}")
print(f"Year Range: {df_clean['year'].min()} - {df_clean['year'].max()}")

# 8. Save Cleaned Dataset
print("\n8️⃣ SAVING CLEANED DATASET...")
output_csv = '../data/processed/spotify_cleaned.csv'
df_clean.to_csv(output_csv, index=False)
print(f"✅ Saved: {output_csv}")

output_parquet = '../data/processed/spotify_cleaned.parquet'
df_clean.to_parquet(output_parquet, index=False)
print(f"✅ Saved: {output_parquet}")

import os
csv_size = os.path.getsize(output_csv) / 1024**2
parquet_size = os.path.getsize(output_parquet) / 1024**2
print(f"\nCSV size: {csv_size:.2f} MB")
print(f"Parquet size: {parquet_size:.2f} MB (compression: {(1-parquet_size/csv_size)*100:.1f}%)")

print("\n" + "="*60)
print("🎉 DATA CLEANING COMPLETE!")
print("="*60)
