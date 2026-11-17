"""
Validate Tempo Sweet Spot Hypothesis for SEMPRO
Check data completeness, statistical power, and proof feasibility
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load data
print("Loading data...")
df = pd.read_parquet('data/processed/spotify_master_enriched.parquet')

print('='*70)
print('DATA AVAILABILITY CHECK - TEMPO SWEET SPOT HYPOTHESIS')
print('='*70)

# 1. Check if tempo data exists
print('\n1. TEMPO DATA:')
print(f'   Total tracks: {len(df):,}')
print(f'   Has tempo: {df["tempo"].notna().sum():,} ({df["tempo"].notna().mean()*100:.1f}%)')
print(f'   Missing tempo: {df["tempo"].isna().sum():,}')

# 2. Check tempo range
print('\n2. TEMPO RANGE:')
print(f'   Min: {df["tempo"].min():.1f} BPM')
print(f'   Max: {df["tempo"].max():.1f} BPM')
print(f'   Mean: {df["tempo"].mean():.1f} BPM')
print(f'   Median: {df["tempo"].median():.1f} BPM')

# 3. Check tempo bands
print('\n3. TEMPO BAND DISTRIBUTION:')
tempo_dist = df['tempo_band'].value_counts().sort_index()
for band, count in tempo_dist.items():
    pct = count / len(df) * 100
    print(f'   {band:12s}: {count:8,} ({pct:5.1f}%)')

# 4. Check mood cluster data
print('\n4. MOOD CLUSTER DATA:')
print(f'   Has mood: {df["mood_cluster"].notna().sum():,} ({df["mood_cluster"].notna().mean()*100:.1f}%)')
mood_dist = df['mood_cluster'].value_counts()
for mood, count in mood_dist.items():
    pct = count / len(df) * 100
    print(f'   {mood:20s}: {count:8,} ({pct:5.1f}%)')

# 5. Check hit probability
print('\n5. HIT PROBABILITY DATA:')
print(f'   Has hit_prob: {df["hit_probability"].notna().sum():,} ({df["hit_probability"].notna().mean()*100:.1f}%)')
print(f'   Mean: {df["hit_probability"].mean():.4f}')
print(f'   Min: {df["hit_probability"].min():.4f}')
print(f'   Max: {df["hit_probability"].max():.4f}')

# 6. CRITICAL TEST: Tempo sweet spot per mood
print('\n6. TEMPO SWEET SPOT VALIDATION:')
print('='*70)
print(f'{"MOOD":<20} {"BEST TEMPO":<15} {"HIT PROB":<12} {"SAMPLE SIZE"}')
print('-'*70)

universal_sweet_spot = True
for mood in sorted(df['mood_cluster'].dropna().unique()):
    mood_data = df[df['mood_cluster'] == mood]
    tempo_stats = mood_data.groupby('tempo_band')['hit_probability'].agg(['mean', 'count'])
    best = tempo_stats['mean'].idxmax()
    best_prob = tempo_stats['mean'].max()
    count = int(tempo_stats.loc[best, 'count'])
    
    marker = "✅" if best == 'medium' else "⚠️"
    print(f'{mood:<20} {best:<15} {best_prob:.4f}      {count:>8,} {marker}')
    
    if best != 'medium':
        universal_sweet_spot = False

# 7. Statistical power check
print('\n7. STATISTICAL POWER CHECK:')
print('-'*70)
medium_tempo = df[df['tempo_band'] == 'medium']
other_tempo = df[df['tempo_band'] != 'medium']
print(f'   Medium tempo tracks (100-120 BPM): {len(medium_tempo):,}')
print(f'   Other tempo tracks: {len(other_tempo):,}')
print(f'   Ratio: {len(medium_tempo)/len(other_tempo):.2f}:1')

# Calculate effect size
medium_hit = medium_tempo['hit_probability'].mean()
other_hit = other_tempo['hit_probability'].mean()
effect_size = medium_hit - other_hit
pooled_std = np.sqrt((medium_tempo['hit_probability'].std()**2 + other_tempo['hit_probability'].std()**2) / 2)
cohens_d = effect_size / pooled_std

print(f'\n   Medium tempo avg hit prob: {medium_hit:.4f}')
print(f'   Other tempo avg hit prob: {other_hit:.4f}')
print(f'   Effect size: +{effect_size:.4f} ({effect_size/other_hit*100:+.1f}%)')
print(f'   Cohen\'s d: {cohens_d:.4f} ({"Small" if abs(cohens_d) < 0.5 else "Medium" if abs(cohens_d) < 0.8 else "Large"})')

# 8. T-test (sample for proof)
print('\n8. STATISTICAL SIGNIFICANCE (T-TEST PREVIEW):')
print('-'*70)
t_stat, p_value = stats.ttest_ind(
    medium_tempo['hit_probability'].dropna(),
    other_tempo['hit_probability'].dropna()
)
print(f'   t-statistic: {t_stat:.4f}')
print(f'   p-value: {p_value:.4e}')
print(f'   Significance: {"✅ YES (p < 0.001)" if p_value < 0.001 else "⚠️ Check"}')

# 9. ANOVA across all tempo bands
print('\n9. ANOVA TEST (All Tempo Bands):')
print('-'*70)
tempo_groups = [group['hit_probability'].dropna() for name, group in df.groupby('tempo_band')]
f_stat, p_value_anova = stats.f_oneway(*tempo_groups)
print(f'   F-statistic: {f_stat:.4f}')
print(f'   p-value: {p_value_anova:.4e}')
print(f'   Significance: {"✅ YES (p < 0.001)" if p_value_anova < 0.001 else "⚠️ Check"}')

# 10. Final assessment
print('\n' + '='*70)
print('FINAL ASSESSMENT FOR SEMPRO')
print('='*70)

checks = []
checks.append(('Data Completeness', df['tempo'].notna().mean() > 0.95))
checks.append(('Tempo Coverage', df['tempo_band'].notna().mean() > 0.95))
checks.append(('Mood Classification', df['mood_cluster'].notna().mean() > 0.95))
checks.append(('Hit Probability', df['hit_probability'].notna().mean() > 0.95))
checks.append(('Sample Size (>100k)', len(df) > 100000))
checks.append(('Medium Tempo Sample (>50k)', len(medium_tempo) > 50000))
checks.append(('Statistical Significance', p_value < 0.001))
checks.append(('Universal Pattern', universal_sweet_spot))
checks.append(('Effect Size (>5%)', effect_size > 0.05))

print('\nChecklist:')
for check_name, passed in checks:
    status = '✅ PASS' if passed else '❌ FAIL'
    print(f'   [{status}] {check_name}')

all_passed = all(passed for _, passed in checks)
print('\n' + '='*70)
if all_passed:
    print('✅ SEMUA KRITERIA TERPENUHI - SIAP UNTUK SEMPRO!')
else:
    print('⚠️ ADA KRITERIA YANG PERLU DIPERBAIKI')
print('='*70)

# 11. Dataset future-proofing check
print('\n11. DATASET SUPPORT FOR FUTURE WORK:')
print('-'*70)

# Check available columns
available_cols = df.columns.tolist()
if 'year' in available_cols:
    print(f'   ✅ Time range: {df["year"].min():.0f} - {df["year"].max():.0f} ({df["year"].max() - df["year"].min():.0f} years)')
elif 'release_year' in available_cols:
    print(f'   ✅ Time range: {df["release_year"].min():.0f} - {df["release_year"].max():.0f} ({df["release_year"].max() - df["release_year"].min():.0f} years)')

if 'artists' in available_cols:
    print(f'   ✅ Artist coverage: {df["artists"].nunique():,} unique artists')
elif 'artist_name' in available_cols:
    print(f'   ✅ Artist coverage: {df["artist_name"].nunique():,} unique artists')
    
if 'album_name' in available_cols:
    print(f'   ✅ Album coverage: {df["album_name"].nunique():,} unique albums')

print(f'   ✅ Total features: {len(df.columns)} columns')
print(f'   ✅ Audio features: tempo, energy, valence, danceability, etc.')
print(f'   ✅ Derived features: mood_cluster, tempo_band, hit_probability')
print('\n   Dataset mendukung:')
print('   • Predictive modeling (classification/regression)')
print('   • Time-series analysis (decade trends)')
print('   • Artist/album-level aggregation')
print('   • Multi-feature correlation studies')
print('   • Genre/mood-based segmentation')

print('\n' + '='*70)
print('VALIDATION COMPLETE')
print('='*70)
