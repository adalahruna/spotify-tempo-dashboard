"""
Generate Album-Level Aggregated Features
Features: track_count, album_duration, audio coherence, track diversity, etc.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("📦 Loading cleaned dataset...")
df = pd.read_parquet('../data/processed/spotify_cleaned.parquet')
print(f"✅ Loaded {len(df):,} tracks")
print("="*60)

# Filter out albums with valid album_id
df_valid = df[df['album_id'].notna()].copy()
print(f"Tracks with valid album ID: {len(df_valid):,}")

print("\n1️⃣ CALCULATING ALBUM BASIC METRICS...")
album_stats = df_valid.groupby('album_id').agg({
    'id': 'count',  # track_count
    'album': 'first',  # album name
    'primary_artist': 'first',  # primary artist
    'year': 'first',  # release year
    'decade': 'first',  # decade
    'era': 'first',  # era
    'duration_ms': ['sum', 'mean', 'std'],  # duration stats
    'explicit': 'sum',  # explicit track count
    'is_collab': 'mean'  # collaboration rate
}).reset_index()

album_stats.columns = ['album_id', 'track_count', 'album_name', 'primary_artist',
                       'release_year', 'decade', 'era', 'total_duration_ms', 
                       'avg_track_duration_ms', 'track_duration_std', 
                       'explicit_track_count', 'collab_rate']

# Convert total duration to minutes
album_stats['total_duration_min'] = album_stats['total_duration_ms'] / 60000

print(f"✅ Calculated basic metrics for {len(album_stats):,} albums")

print("\n2️⃣ CALCULATING AUDIO COHERENCE...")
# Audio coherence: how consistent are audio features across album tracks
audio_features = ['energy', 'valence', 'danceability', 'acousticness', 
                  'instrumentalness', 'speechiness', 'tempo']

# Calculate mean and std for each audio feature per album
audio_stats = df_valid.groupby('album_id')[audio_features].agg(['mean', 'std']).reset_index()
audio_stats.columns = ['album_id'] + [f'{feat}_{stat}' for feat in audio_features for stat in ['mean', 'std']]
audio_stats = audio_stats.fillna(0)

# Calculate overall audio coherence (average of std across features)
# Lower std = more coherent album
std_cols = [col for col in audio_stats.columns if col.endswith('_std')]
audio_stats['audio_coherence_score'] = 1 / (1 + audio_stats[std_cols].mean(axis=1))

print(f"✅ Calculated audio coherence for {len(audio_stats):,} albums")

print("\n3️⃣ CALCULATING ALBUM DIVERSITY METRICS...")
# Track diversity
diversity_stats = df_valid.groupby('album_id').agg({
    'key': 'nunique',  # number of different keys used
    'tempo': 'std',  # tempo variation
    'mode': lambda x: x.value_counts().iloc[0] / len(x) if len(x) > 0 else 1  # mode dominance
}).reset_index()
diversity_stats.columns = ['album_id', 'key_diversity', 'tempo_diversity', 'mode_dominance']

print(f"✅ Calculated diversity metrics for {len(diversity_stats):,} albums")

print("\n4️⃣ CALCULATING ALBUM MOOD PROFILE...")
# Overall mood classification based on valence and energy
def classify_album_mood(energy, valence):
    """Classify album mood based on average energy and valence"""
    if energy > 0.6 and valence > 0.6:
        return 'Euphoric'
    elif energy > 0.6 and valence <= 0.6:
        return 'Intense/Angry'
    elif energy <= 0.6 and valence > 0.6:
        return 'Content/Peaceful'
    else:
        return 'Melancholic/Sad'

# Get mood from audio_stats
mood_profile = audio_stats[['album_id', 'energy_mean', 'valence_mean']].copy()
mood_profile['album_mood'] = mood_profile.apply(
    lambda row: classify_album_mood(row['energy_mean'], row['valence_mean']), axis=1
)

print(f"✅ Classified mood for {len(mood_profile):,} albums")

print("\n5️⃣ CALCULATING ALBUM TYPE INDICATORS...")
# Identify special album types
album_types = df_valid.groupby('album_id').agg({
    'instrumentalness': 'mean',
    'acousticness': 'mean',
    'liveness': 'mean',
    'speechiness': 'mean'
}).reset_index()

album_types['is_likely_instrumental'] = (album_types['instrumentalness'] > 0.5).astype(int)
album_types['is_likely_acoustic'] = (album_types['acousticness'] > 0.7).astype(int)
album_types['is_likely_live'] = (album_types['liveness'] > 0.8).astype(int)
album_types['is_likely_spoken_word'] = (album_types['speechiness'] > 0.66).astype(int)

album_types = album_types[['album_id', 'is_likely_instrumental', 'is_likely_acoustic', 
                           'is_likely_live', 'is_likely_spoken_word']]

print(f"✅ Identified album types for {len(album_types):,} albums")

print("\n6️⃣ MERGING ALL ALBUM FEATURES...")
# Merge all features
album_features = album_stats.copy()
album_features = album_features.merge(audio_stats, on='album_id', how='left')
album_features = album_features.merge(diversity_stats, on='album_id', how='left')
album_features = album_features.merge(mood_profile[['album_id', 'album_mood']], on='album_id', how='left')
album_features = album_features.merge(album_types, on='album_id', how='left')

print(f"✅ Merged all features!")

print("\n7️⃣ SUMMARY STATISTICS...")
print(f"Total Albums: {len(album_features):,}")
print(f"\n=== TRACK COUNT DISTRIBUTION ===")
print(album_features['track_count'].describe())
print(f"\n=== ALBUM DURATION DISTRIBUTION (minutes) ===")
print(album_features['total_duration_min'].describe())
print(f"\n=== AUDIO COHERENCE DISTRIBUTION ===")
print(album_features['audio_coherence_score'].describe())
print(f"\n=== ALBUM MOOD DISTRIBUTION ===")
print(album_features['album_mood'].value_counts())

print("\n8️⃣ IDENTIFYING INTERESTING ALBUMS...")
# Top 10 most coherent albums (with at least 5 tracks)
print("\n=== TOP 10 MOST COHERENT ALBUMS ===")
coherent_albums = album_features[album_features['track_count'] >= 5].nlargest(10, 'audio_coherence_score')[
    ['album_name', 'primary_artist', 'track_count', 'audio_coherence_score', 'album_mood']
]
print(coherent_albums.to_string(index=False))

# Top 10 longest albums
print("\n=== TOP 10 LONGEST ALBUMS ===")
longest_albums = album_features.nlargest(10, 'total_duration_min')[
    ['album_name', 'primary_artist', 'track_count', 'total_duration_min']
]
print(longest_albums.to_string(index=False))

# Top 10 most diverse albums (high tempo diversity, many keys)
album_features['diversity_score'] = (
    album_features['tempo_diversity'].fillna(0) * 0.5 + 
    album_features['key_diversity'] * 2
)
print("\n=== TOP 10 MOST DIVERSE ALBUMS ===")
diverse_albums = album_features[album_features['track_count'] >= 5].nlargest(10, 'diversity_score')[
    ['album_name', 'primary_artist', 'track_count', 'diversity_score', 'key_diversity']
]
print(diverse_albums.to_string(index=False))

print("\n9️⃣ SAVING ALBUM FEATURES...")
output_csv = '../data/processed/spotify_album_features.csv'
album_features.to_csv(output_csv, index=False)
print(f"✅ Saved: {output_csv}")

output_parquet = '../data/processed/spotify_album_features.parquet'
album_features.to_parquet(output_parquet, index=False)
print(f"✅ Saved: {output_parquet}")

import os
csv_size = os.path.getsize(output_csv) / 1024**2
print(f"File size: {csv_size:.2f} MB")

print("\n" + "="*60)
print("🎉 ALBUM FEATURES GENERATION COMPLETE!")
print("="*60)
print(f"\nGenerated {len(album_features.columns)} features for {len(album_features):,} albums")
print("\nKey Features:")
print("- Basic metrics: track_count, total_duration, explicit_track_count")
print("- Audio profiles: mean & std for all audio features")
print("- Coherence: audio_coherence_score")
print("- Diversity: key_diversity, tempo_diversity, mode_dominance")
print("- Mood: album_mood classification")
print("- Type indicators: instrumental, acoustic, live, spoken_word")
