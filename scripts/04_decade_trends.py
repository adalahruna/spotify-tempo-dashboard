"""
Generate Decade-Level Trend Features
Features: mean audio features by decade, trend analysis, evolution indices
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("📦 Loading cleaned dataset...")
df = pd.read_parquet('../data/processed/spotify_cleaned.parquet')
print(f"✅ Loaded {len(df):,} tracks")
print("="*60)

# Filter valid years (exclude year 0)
df_valid = df[df['year'] > 0].copy()
print(f"Tracks with valid year: {len(df_valid):,}")

print("\n1️⃣ CALCULATING DECADE AUDIO FEATURE MEANS...")
audio_features = ['energy', 'valence', 'danceability', 'acousticness', 
                  'instrumentalness', 'speechiness', 'liveness', 'loudness', 'tempo']

# Calculate mean of each audio feature by decade
decade_means = df_valid.groupby('decade')[audio_features].mean().reset_index()
decade_means.columns = ['decade'] + [f'mean_{feat}_by_decade' for feat in audio_features]

print(f"✅ Calculated decade means for {len(decade_means)} decades")
print(f"Year range: {decade_means['decade'].min()}s - {decade_means['decade'].max()}s")

print("\n2️⃣ CALCULATING DECADE TRACK COUNTS...")
decade_counts = df_valid.groupby('decade').size().reset_index()
decade_counts.columns = ['decade', 'decade_track_count']

print(f"✅ Calculated track counts by decade")

print("\n3️⃣ CALCULATING DECADE DIVERSITY METRICS...")
decade_diversity = df_valid.groupby('decade').agg({
    'primary_artist': 'nunique',  # unique artists
    'album': 'nunique',  # unique albums
    'explicit': 'mean',  # explicit rate
    'is_collab': 'mean',  # collaboration rate
    'key': 'nunique',  # key diversity
    'tempo': 'std'  # tempo variation
}).reset_index()

decade_diversity.columns = ['decade', 'unique_artists_count', 'unique_albums_count',
                            'explicit_rate', 'collab_rate', 'key_diversity', 'tempo_std']

print(f"✅ Calculated diversity metrics by decade")

print("\n4️⃣ CALCULATING TEMPORAL TRENDS...")
# Merge all decade data
decade_trends = decade_means.copy()
decade_trends = decade_trends.merge(decade_counts, on='decade', how='left')
decade_trends = decade_trends.merge(decade_diversity, on='decade', how='left')

# Calculate trend indices
# Acousticness decline index (comparing to 1920s baseline)
baseline_acousticness = decade_trends[decade_trends['decade'] == decade_trends['decade'].min()]['mean_acousticness_by_decade'].values[0]
decade_trends['acousticness_decline_idx'] = (baseline_acousticness - decade_trends['mean_acousticness_by_decade']) / baseline_acousticness

# Danceability trend (change from previous decade)
decade_trends['danceability_trend'] = decade_trends['mean_danceability_by_decade'].diff()

# Energy trend
decade_trends['energy_trend'] = decade_trends['mean_energy_by_decade'].diff()

# Loudness war index (increase in loudness over time)
baseline_loudness = decade_trends[decade_trends['decade'] == decade_trends['decade'].min()]['mean_loudness_by_decade'].values[0]
decade_trends['loudness_war_idx'] = decade_trends['mean_loudness_by_decade'] - baseline_loudness

print(f"✅ Calculated temporal trends")

print("\n5️⃣ DECADE SUMMARY STATISTICS...")
print("=== DECADE DISTRIBUTION ===")
print(decade_trends[['decade', 'decade_track_count']].to_string(index=False))

print("\n=== KEY AUDIO TRENDS ===")
print("\nEnergy by Decade:")
print(decade_trends[['decade', 'mean_energy_by_decade']].to_string(index=False))

print("\nValence by Decade:")
print(decade_trends[['decade', 'mean_valence_by_decade']].to_string(index=False))

print("\nAcousticness by Decade (showing decline):")
print(decade_trends[['decade', 'mean_acousticness_by_decade', 'acousticness_decline_idx']].to_string(index=False))

print("\nLoudness by Decade (showing loudness war):")
print(decade_trends[['decade', 'mean_loudness_by_decade', 'loudness_war_idx']].to_string(index=False))

print("\n6️⃣ IDENTIFYING KEY TRENDS...")
# Most energetic decade
most_energetic = decade_trends.loc[decade_trends['mean_energy_by_decade'].idxmax()]
print(f"\n🔥 MOST ENERGETIC DECADE: {int(most_energetic['decade'])}s")
print(f"   Energy: {most_energetic['mean_energy_by_decade']:.3f}")

# Happiest decade (highest valence)
happiest = decade_trends.loc[decade_trends['mean_valence_by_decade'].idxmax()]
print(f"\n😊 HAPPIEST DECADE: {int(happiest['decade'])}s")
print(f"   Valence: {happiest['mean_valence_by_decade']:.3f}")

# Most acoustic decade
most_acoustic = decade_trends.loc[decade_trends['mean_acousticness_by_decade'].idxmax()]
print(f"\n🎸 MOST ACOUSTIC DECADE: {int(most_acoustic['decade'])}s")
print(f"   Acousticness: {most_acoustic['mean_acousticness_by_decade']:.3f}")

# Decade with most tracks
most_tracks = decade_trends.loc[decade_trends['decade_track_count'].idxmax()]
print(f"\n📀 DECADE WITH MOST TRACKS: {int(most_tracks['decade'])}s")
print(f"   Track Count: {int(most_tracks['decade_track_count']):,}")

# Most collaborative decade
most_collab = decade_trends.loc[decade_trends['collab_rate'].idxmax()]
print(f"\n🤝 MOST COLLABORATIVE DECADE: {int(most_collab['decade'])}s")
print(f"   Collaboration Rate: {most_collab['collab_rate']:.1%}")

print("\n7️⃣ SAVING DECADE TRENDS...")
output_csv = '../data/processed/spotify_decade_trends.csv'
decade_trends.to_csv(output_csv, index=False)
print(f"✅ Saved: {output_csv}")

output_parquet = '../data/processed/spotify_decade_trends.parquet'
decade_trends.to_parquet(output_parquet, index=False)
print(f"✅ Saved: {output_parquet}")

import os
csv_size = os.path.getsize(output_csv) / 1024
print(f"File size: {csv_size:.2f} KB")

print("\n" + "="*60)
print("🎉 DECADE TRENDS GENERATION COMPLETE!")
print("="*60)
print(f"\nGenerated {len(decade_trends.columns)} features for {len(decade_trends)} decades")
print("\nKey Features:")
print("- Audio means: mean of all audio features per decade")
print("- Track counts: number of tracks per decade")
print("- Diversity: unique artists, albums, key diversity")
print("- Trends: acousticness_decline_idx, danceability_trend, loudness_war_idx")
print("- Rates: explicit_rate, collab_rate")
