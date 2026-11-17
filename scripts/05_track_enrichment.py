"""
Create Track-Level Enrichment Features
Features: mood_cluster, emotional_arc, tempo_band, novelty_score, hit_probability, etc.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("📦 Loading datasets...")
df = pd.read_parquet('../data/processed/spotify_cleaned.parquet')
decade_trends = pd.read_parquet('../data/processed/spotify_decade_trends.parquet')
print(f"✅ Loaded {len(df):,} tracks")
print(f"✅ Loaded {len(decade_trends)} decade trends")
print("="*60)

# Merge with decade trends
df_enriched = df.merge(
    decade_trends[['decade', 'mean_energy_by_decade', 'mean_valence_by_decade', 
                   'mean_tempo_by_decade', 'mean_loudness_by_decade', 
                   'mean_acousticness_by_decade', 'acousticness_decline_idx']],
    on='decade', how='left'
)
print(f"✅ Merged with decade trends")

print("\n1️⃣ CREATING MOOD & EMOTIONAL FEATURES...")

# Emotional Arc (Valence x Energy quadrants)
def classify_emotional_arc(row):
    """Classify emotional quadrant"""
    energy = row['energy']
    valence = row['valence']
    
    if energy > 0.6 and valence > 0.6:
        return 'Q1_euphoric'
    elif energy > 0.6 and valence <= 0.6:
        return 'Q2_angry'
    elif energy <= 0.6 and valence <= 0.6:
        return 'Q3_depressed'
    else:
        return 'Q4_content'

df_enriched['emotional_arc'] = df_enriched.apply(classify_emotional_arc, axis=1)

# Mood Index (continuous composite)
df_enriched['mood_index'] = (df_enriched['valence'] + df_enriched['energy']) / 2

print(f"✅ Created emotional_arc and mood_index")

print("\n2️⃣ CREATING MOOD CLUSTER (RULE-BASED)...")
# Rule-based mood clustering (simpler, no sklearn needed)
def classify_mood_cluster(row):
    """Classify mood based on valence, energy, tempo"""
    valence = row['valence']
    energy = row['energy']
    tempo = row['tempo']
    
    if energy > 0.6 and valence > 0.6:
        return 'happy_energetic'
    elif energy > 0.6 and valence <= 0.5:
        return 'angry_intense'
    elif energy <= 0.5 and valence <= 0.4:
        return 'sad_slow'
    elif energy <= 0.5 and valence > 0.5:
        return 'calm_positive'
    else:
        return 'melancholic'

df_enriched['mood_cluster'] = df_enriched.apply(classify_mood_cluster, axis=1)

print(f"✅ Created mood_cluster")
print("\n=== MOOD CLUSTER DISTRIBUTION ===")
print(df_enriched['mood_cluster'].value_counts())

print("\n3️⃣ CREATING TEMPO & AUDIO RATIO FEATURES...")

# Tempo Band
def classify_tempo_band(tempo):
    """Classify tempo into bands"""
    if tempo < 80:
        return 'very_slow'
    elif tempo < 100:
        return 'slow'
    elif tempo < 120:
        return 'medium'
    elif tempo < 140:
        return 'fast'
    else:
        return 'very_fast'

df_enriched['tempo_band'] = df_enriched['tempo'].apply(classify_tempo_band)

# Acoustic-Synthetic Ratio
df_enriched['acoustic_synthetic_ratio'] = df_enriched['acousticness'] / (df_enriched['energy'] + 0.001)

# Energy-Loudness Ratio
df_enriched['energy_loudness_ratio'] = df_enriched['energy'] / (abs(df_enriched['loudness']) + 0.001)

print(f"✅ Created tempo_band, acoustic_synthetic_ratio, energy_loudness_ratio")

print("\n4️⃣ CREATING BINARY FLAGS...")

# Likely instrumental
df_enriched['is_likely_instrumental'] = (df_enriched['instrumentalness'] > 0.5).astype(int)

# Likely live
df_enriched['is_likely_live'] = (df_enriched['liveness'] > 0.8).astype(int)

# Likely spoken word
df_enriched['is_likely_spoken_word'] = (df_enriched['speechiness'] > 0.66).astype(int)

print(f"✅ Created binary flags")
print(f"Instrumental tracks: {df_enriched['is_likely_instrumental'].sum():,} ({df_enriched['is_likely_instrumental'].mean()*100:.1f}%)")
print(f"Live tracks: {df_enriched['is_likely_live'].sum():,} ({df_enriched['is_likely_live'].mean()*100:.1f}%)")
print(f"Spoken word tracks: {df_enriched['is_likely_spoken_word'].sum():,} ({df_enriched['is_likely_spoken_word'].mean()*100:.1f}%)")

print("\n5️⃣ CALCULATING NOVELTY SCORE...")
# Novelty: how different is track from its decade average
audio_features = ['energy', 'valence', 'danceability', 'acousticness', 'tempo']
novelty_scores = []

for idx, row in df_enriched.iterrows():
    if pd.isna(row['mean_energy_by_decade']):
        novelty_scores.append(0)
        continue
    
    # Calculate euclidean distance from decade average
    track_profile = np.array([row[feat] for feat in audio_features[:4]])  # Exclude tempo for scale
    decade_profile = np.array([
        row['mean_energy_by_decade'],
        row['mean_valence_by_decade'],
        row['mean_danceability_by_decade'] if 'mean_danceability_by_decade' in row else 0.5,
        row['mean_acousticness_by_decade']
    ])
    
    distance = np.sqrt(((track_profile - decade_profile) ** 2).sum())
    novelty_scores.append(distance)

df_enriched['novelty_score'] = novelty_scores

print(f"✅ Created novelty_score")
print(f"Mean novelty: {df_enriched['novelty_score'].mean():.3f}")
print(f"High novelty tracks (>0.5): {(df_enriched['novelty_score'] > 0.5).sum():,}")

print("\n6️⃣ CALCULATING HIT PROBABILITY SCORE...")
# Hit probability: composite score based on audio features
# High energy + high valence + medium tempo + not too acoustic
df_enriched['hit_probability'] = (
    df_enriched['energy'] * 0.3 +
    df_enriched['valence'] * 0.2 +
    df_enriched['danceability'] * 0.3 +
    (1 - df_enriched['acousticness']) * 0.1 +
    ((df_enriched['tempo'] >= 100) & (df_enriched['tempo'] <= 130)).astype(int) * 0.1
)

print(f"✅ Created hit_probability")
print(f"Mean hit probability: {df_enriched['hit_probability'].mean():.3f}")
print(f"High probability tracks (>0.7): {(df_enriched['hit_probability'] > 0.7).sum():,}")

print("\n7️⃣ IDENTIFYING SAD BANGERS...")
# Sad Banger: high tempo + low valence + high energy/danceability
df_enriched['is_sad_banger'] = (
    (df_enriched['tempo'] >= 100) & 
    (df_enriched['tempo'] <= 120) &
    (df_enriched['valence'] < 0.4) &
    ((df_enriched['energy'] > 0.6) | (df_enriched['danceability'] > 0.6))
).astype(int)

sad_banger_count = df_enriched['is_sad_banger'].sum()
print(f"✅ Identified {sad_banger_count:,} sad bangers ({sad_banger_count/len(df_enriched)*100:.1f}%)")

print("\n8️⃣ SUMMARY STATISTICS...")
print("\n=== EMOTIONAL ARC DISTRIBUTION ===")
print(df_enriched['emotional_arc'].value_counts())

print("\n=== TEMPO BAND DISTRIBUTION ===")
print(df_enriched['tempo_band'].value_counts())

print("\n=== TOP 10 MOST NOVEL TRACKS ===")
top_novel = df_enriched.nlargest(10, 'novelty_score')[
    ['name', 'primary_artist', 'year', 'novelty_score', 'mood_cluster']
]
print(top_novel.to_string(index=False))

print("\n=== TOP 10 HIGHEST HIT PROBABILITY ===")
top_hits = df_enriched.nlargest(10, 'hit_probability')[
    ['name', 'primary_artist', 'hit_probability', 'energy', 'valence', 'danceability']
]
print(top_hits.to_string(index=False))

print("\n9️⃣ SAVING ENRICHED DATASET...")
# Select relevant columns for master dataset
columns_to_keep = [
    # Original identifiers
    'id', 'name', 'album', 'album_id', 'primary_artist', 'primary_artist_id',
    # Temporal
    'year', 'decade', 'era', 'release_date',
    # Audio features
    'energy', 'valence', 'danceability', 'acousticness', 'instrumentalness',
    'speechiness', 'liveness', 'loudness', 'tempo', 'key', 'mode',
    'duration_ms', 'time_signature', 'explicit',
    # Track metadata
    'track_number', 'disc_number', 'num_artists', 'is_collab',
    # Enriched features
    'emotional_arc', 'mood_index', 'mood_cluster', 'tempo_band',
    'acoustic_synthetic_ratio', 'energy_loudness_ratio',
    'is_likely_instrumental', 'is_likely_live', 'is_likely_spoken_word',
    'novelty_score', 'hit_probability', 'is_sad_banger',
    # Decade context
    'mean_energy_by_decade', 'mean_valence_by_decade', 
    'mean_acousticness_by_decade', 'acousticness_decline_idx'
]

df_master = df_enriched[columns_to_keep].copy()

output_parquet = '../data/processed/spotify_master_enriched.parquet'
df_master.to_parquet(output_parquet, index=False)
print(f"✅ Saved: {output_parquet}")

import os
parquet_size = os.path.getsize(output_parquet) / 1024**2
print(f"File size: {parquet_size:.2f} MB")

print("\n" + "="*60)
print("🎉 TRACK ENRICHMENT COMPLETE!")
print("="*60)
print(f"\nEnriched {len(df_master):,} tracks with {len(df_master.columns)} total columns")
print("\nNew Features Added:")
print("- Mood: emotional_arc, mood_index, mood_cluster")
print("- Tempo: tempo_band")
print("- Ratios: acoustic_synthetic_ratio, energy_loudness_ratio")
print("- Flags: is_likely_instrumental, is_likely_live, is_likely_spoken_word")
print("- Scores: novelty_score, hit_probability")
print("- Special: is_sad_banger")
print("- Context: decade trends merged")
