"""
Generate Artist-Level Aggregated Features
Features: catalog_size, career_span, hit_rate, sonic_evolution_score, etc.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("📦 Loading cleaned dataset...")
df = pd.read_parquet('../data/processed/spotify_cleaned.parquet')
print(f"✅ Loaded {len(df):,} tracks")
print("="*60)

# Filter out artists with unknown ID
df_valid = df[df['primary_artist_id'] != 'unknown'].copy()
print(f"Tracks with valid artist ID: {len(df_valid):,}")

print("\n1️⃣ CALCULATING ARTIST CATALOG METRICS...")
artist_stats = df_valid.groupby('primary_artist_id').agg({
    'id': 'count',  # catalog_size
    'year': ['min', 'max'],  # career bounds
    'primary_artist': 'first',  # artist name
    'album': 'nunique',  # unique albums
    'is_collab': 'mean'  # collaboration rate
}).reset_index()

artist_stats.columns = ['artist_id', 'catalog_size', 'career_start_year', 
                        'career_end_year', 'artist_name', 'num_albums', 'collab_rate']

# Career span
artist_stats['career_span_years'] = artist_stats['career_end_year'] - artist_stats['career_start_year']
artist_stats['career_span_years'] = artist_stats['career_span_years'].clip(lower=0)

print(f"✅ Calculated catalog metrics for {len(artist_stats):,} artists")

print("\n2️⃣ CALCULATING AUDIO PROFILE STATISTICS...")
audio_features = ['energy', 'valence', 'danceability', 'acousticness', 
                  'instrumentalness', 'speechiness', 'liveness', 'tempo', 'loudness']

# Mean and std of audio features per artist
audio_stats = df_valid.groupby('primary_artist_id')[audio_features].agg(['mean', 'std']).reset_index()
audio_stats.columns = ['artist_id'] + [f'{feat}_{stat}' for feat in audio_features for stat in ['mean', 'std']]

# Fill NaN std with 0 (for artists with single track)
audio_stats = audio_stats.fillna(0)

print(f"✅ Calculated audio profiles for {len(audio_stats):,} artists")

print("\n3️⃣ CALCULATING SONIC EVOLUTION SCORE...")
# Simplified sonic evolution using std of audio features
# Higher std = more diverse/evolving sound
evolution_data = df_valid.groupby('primary_artist_id')[audio_features].std().mean(axis=1).reset_index()
evolution_data.columns = ['artist_id', 'sonic_evolution_score']
evolution_data['sonic_evolution_score'] = evolution_data['sonic_evolution_score'].fillna(0)

print(f"✅ Calculated sonic evolution for {len(evolution_data):,} artists")

print("\n4️⃣ CALCULATING GENRE BREADTH...")
# Count unique decades artist has released in (proxy for genre/style diversity)
genre_breadth = df_valid.groupby('primary_artist_id')['decade'].nunique().reset_index()
genre_breadth.columns = ['artist_id', 'decade_breadth']

print(f"✅ Calculated genre breadth for {len(genre_breadth):,} artists")

print("\n5️⃣ CALCULATING POPULARITY METRICS...")
# Note: This dataset doesn't have explicit popularity score, 
# so we'll use proxies like explicit content rate and tempo diversity
popularity_proxies = df_valid.groupby('primary_artist_id').agg({
    'explicit': 'mean',  # explicit content rate
    'tempo': 'std',  # tempo diversity
    'duration_ms': 'mean'  # average track length
}).reset_index()
popularity_proxies.columns = ['artist_id', 'explicit_rate', 'tempo_diversity', 'avg_duration_ms']

print(f"✅ Calculated popularity proxies for {len(popularity_proxies):,} artists")

print("\n6️⃣ CALCULATING LONGEVITY SCORE...")
# Longevity: combination of career span, catalog size, and decade breadth
def calculate_longevity(row):
    """Composite longevity score"""
    # Normalize each component (0-1 scale)
    span_norm = min(row['career_span_years'] / 50, 1.0)  # Cap at 50 years
    catalog_norm = min(row['catalog_size'] / 100, 1.0)  # Cap at 100 tracks
    decade_norm = min(row['decade_breadth'] / 7, 1.0)  # Cap at 7 decades
    
    # Weighted average
    longevity = (span_norm * 0.4 + catalog_norm * 0.3 + decade_norm * 0.3)
    return longevity

print("\n7️⃣ MERGING ALL ARTIST FEATURES...")
# Merge all features
artist_features = artist_stats.copy()
artist_features = artist_features.merge(audio_stats, on='artist_id', how='left')
artist_features = artist_features.merge(evolution_data, on='artist_id', how='left')
artist_features = artist_features.merge(genre_breadth, on='artist_id', how='left')
artist_features = artist_features.merge(popularity_proxies, on='artist_id', how='left')

# Calculate longevity score
artist_features['longevity_score'] = artist_features.apply(calculate_longevity, axis=1)

# Calculate hit rate proxy (tracks with high energy + high valence)
hit_proxy = df_valid[
    (df_valid['energy'] > 0.7) & (df_valid['valence'] > 0.6)
].groupby('primary_artist_id').size().reset_index()
hit_proxy.columns = ['artist_id', 'high_energy_happy_tracks']
artist_features = artist_features.merge(hit_proxy, on='artist_id', how='left')
artist_features['high_energy_happy_tracks'] = artist_features['high_energy_happy_tracks'].fillna(0)
artist_features['hit_rate_proxy'] = artist_features['high_energy_happy_tracks'] / artist_features['catalog_size']

print(f"✅ Merged all features!")

print("\n8️⃣ SUMMARY STATISTICS...")
print(f"Total Artists: {len(artist_features):,}")
print(f"\n=== CAREER SPAN DISTRIBUTION ===")
print(artist_features['career_span_years'].describe())
print(f"\n=== CATALOG SIZE DISTRIBUTION ===")
print(artist_features['catalog_size'].describe())
print(f"\n=== LONGEVITY SCORE DISTRIBUTION ===")
print(artist_features['longevity_score'].describe())

print("\n9️⃣ IDENTIFYING TOP ARTISTS...")
# Top 10 by catalog size
print("\n=== TOP 10 ARTISTS BY CATALOG SIZE ===")
top_catalog = artist_features.nlargest(10, 'catalog_size')[
    ['artist_name', 'catalog_size', 'career_span_years', 'longevity_score']
]
print(top_catalog.to_string(index=False))

# Top 10 by longevity
print("\n=== TOP 10 ARTISTS BY LONGEVITY ===")
top_longevity = artist_features.nlargest(10, 'longevity_score')[
    ['artist_name', 'longevity_score', 'career_span_years', 'catalog_size']
]
print(top_longevity.to_string(index=False))

# Top 10 by sonic evolution
print("\n=== TOP 10 ARTISTS BY SONIC EVOLUTION ===")
top_evolution = artist_features.nlargest(10, 'sonic_evolution_score')[
    ['artist_name', 'sonic_evolution_score', 'career_span_years', 'catalog_size']
]
print(top_evolution.to_string(index=False))

print("\n🔟 SAVING ARTIST FEATURES...")
output_csv = '../data/processed/spotify_artist_features.csv'
artist_features.to_csv(output_csv, index=False)
print(f"✅ Saved: {output_csv}")

output_parquet = '../data/processed/spotify_artist_features.parquet'
artist_features.to_parquet(output_parquet, index=False)
print(f"✅ Saved: {output_parquet}")

import os
csv_size = os.path.getsize(output_csv) / 1024**2
print(f"File size: {csv_size:.2f} MB")

print("\n" + "="*60)
print("🎉 ARTIST FEATURES GENERATION COMPLETE!")
print("="*60)
print(f"\nGenerated {len(artist_features.columns)} features for {len(artist_features):,} artists")
print("\nKey Features:")
print("- Catalog metrics: catalog_size, career_span_years, num_albums")
print("- Audio profiles: mean & std for all audio features")
print("- Evolution: sonic_evolution_score")
print("- Diversity: decade_breadth, collab_rate")
print("- Performance: longevity_score, hit_rate_proxy")
