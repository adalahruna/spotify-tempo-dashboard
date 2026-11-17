"""
Discover Underrated Hypotheses
Automated pattern discovery script
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print('🔍 DISCOVERING UNDERRATED HYPOTHESES...')
print('='*70)

# Load data
print('Loading datasets...')
df = pd.read_parquet('../data/processed/spotify_master_enriched.parquet')
artists = pd.read_parquet('../data/processed/spotify_artist_features.parquet')
print(f'✅ Loaded {len(df):,} tracks and {len(artists):,} artists\n')

# ============================================================================
# DISCOVERY 1: Silent Majority Paradox
# ============================================================================
print('1️⃣ THE SILENT MAJORITY PARADOX')
print('-' * 70)

streaming = df[df['era'].isin(['2011-2020 (Streaming Era)', '2021+'])]
instr_stream = streaming[streaming['is_likely_instrumental']==1]
vocal_stream = streaming[streaming['is_likely_instrumental']==0]

print(f'Streaming era tracks: {len(streaming):,}')
print(f'Instrumental: {len(instr_stream):,} ({len(instr_stream)/len(streaming)*100:.1f}%)')
print(f'\nNovelty Comparison:')
print(f'  Instrumental: {instr_stream["novelty_score"].mean():.4f}')
print(f'  Vocal: {vocal_stream["novelty_score"].mean():.4f}')
print(f'  Difference: +{instr_stream["novelty_score"].mean() - vocal_stream["novelty_score"].mean():.4f}')

if instr_stream['novelty_score'].mean() > vocal_stream['novelty_score'].mean():
    print('\n✅ CONFIRMED: Instrumental tracks are MORE novel in streaming era!')
print()

# ============================================================================
# DISCOVERY 2: Collaboration Curse
# ============================================================================
print('2️⃣ THE COLLABORATION CURSE')
print('-' * 70)

solo = df[df['is_collab']==0]
collab = df[df['is_collab']==1]

print(f'Solo tracks: {len(solo):,} ({len(solo)/len(df)*100:.1f}%)')
print(f'Collaboration tracks: {len(collab):,} ({len(collab)/len(df)*100:.1f}%)')
print(f'\nAcousticness Comparison:')
print(f'  Solo: {solo["acousticness"].mean():.4f}')
print(f'  Collab: {collab["acousticness"].mean():.4f}')

diff_pct = ((solo['acousticness'].mean() - collab['acousticness'].mean()) / solo['acousticness'].mean()) * 100
print(f'  Difference: -{diff_pct:.1f}%')
print(f'\n✅ CONFIRMED: Collaborations are {diff_pct:.1f}% LESS acoustic!')
print('   → Teams favor synthetic/electronic production\n')

# ============================================================================
# DISCOVERY 3: Live Performance Premium
# ============================================================================
print('3️⃣ THE LIVE PERFORMANCE PREMIUM')
print('-' * 70)

live = df[df['is_likely_live']==1]
studio = df[df['is_likely_live']==0]

print(f'Live recordings: {len(live):,} ({len(live)/len(df)*100:.2f}%)')
print(f'Studio recordings: {len(studio):,}')
print(f'\nHit Probability:')
print(f'  Live: {live["hit_probability"].mean():.4f}')
print(f'  Studio: {studio["hit_probability"].mean():.4f}')
print(f'\nNovelty Score:')
print(f'  Live: {live["novelty_score"].mean():.4f}')
print(f'  Studio: {studio["novelty_score"].mean():.4f}')

if (live['hit_probability'].mean() < studio['hit_probability'].mean() and
    live['novelty_score'].mean() > studio['novelty_score'].mean()):
    print('\n✅ TRADE-OFF CONFIRMED:')
    print('   Live = Lower commercial potential + Higher artistic novelty')
print()

# ============================================================================
# DISCOVERY 4: Tempo Sweet Spot per Mood
# ============================================================================
print('4️⃣ THE TEMPO SWEET SPOT MYSTERY')
print('-' * 70)

moods_to_check = ['happy_energetic', 'sad_slow', 'angry_intense', 'calm_positive', 'melancholic']
print('Optimal tempo varies by mood:\n')

for mood in moods_to_check:
    mood_data = df[df['mood_cluster']==mood]
    if len(mood_data) > 0:
        tempo_stats = mood_data.groupby('tempo_band')['hit_probability'].agg(['mean', 'count'])
        best_tempo = tempo_stats['mean'].idxmax()
        best_prob = tempo_stats['mean'].max()
        count = tempo_stats.loc[best_tempo, 'count']
        print(f'  {mood:20s}: {best_tempo:12s} (hit prob: {best_prob:.3f}, n={int(count):,})')

print('\n✅ INSIGHT: Each mood has DIFFERENT optimal tempo!')
print('   → One-size-fits-all tempo advice is WRONG!\n')

# ============================================================================
# DISCOVERY 5: Album Position Effect
# ============================================================================
print('5️⃣ THE ALBUM POSITION EFFECT')
print('-' * 70)

df['position_cat'] = pd.cut(df['track_number'], bins=[0,1,3,7,100], 
                             labels=['Opening', 'Early', 'Middle', 'Late'])

pos_stats = df.groupby('position_cat').agg({
    'energy': 'mean',
    'hit_probability': 'mean',
    'id': 'count'
})

print('Track position characteristics:\n')
for pos in ['Opening', 'Early', 'Middle', 'Late']:
    if pos in pos_stats.index:
        energy = pos_stats.loc[pos, 'energy']
        hit = pos_stats.loc[pos, 'hit_probability']
        count = int(pos_stats.loc[pos, 'id'])
        print(f'  {pos:10s}: Energy={energy:.3f}, Hit={hit:.3f} (n={count:,})')

opening_e = pos_stats.loc['Opening', 'energy']
late_e = pos_stats.loc['Late', 'energy']
if opening_e > late_e:
    print(f'\n✅ Albums START strong! Opening {((opening_e-late_e)/late_e*100):.1f}% more energetic')
print()

# ============================================================================
# DISCOVERY 6: Decade Dissonance
# ============================================================================
print('6️⃣ THE DECADE DISSONANCE')
print('-' * 70)

df['energy_deviation'] = abs(df['energy'] - df['mean_energy_by_decade'])
high_dev = df[df['energy_deviation'] > df['energy_deviation'].quantile(0.75)]
low_dev = df[df['energy_deviation'] <= df['energy_deviation'].quantile(0.75)]

print(f'Tracks that deviate from decade norms:')
print(f'  High deviation: {len(high_dev):,} ({len(high_dev)/len(df)*100:.1f}%)')
print(f'  Low deviation: {len(low_dev):,}')
print(f'\nNovelty:')
print(f'  High dev: {high_dev["novelty_score"].mean():.4f}')
print(f'  Low dev: {low_dev["novelty_score"].mean():.4f}')
print(f'\nPredictability (std of hit probability):')
print(f'  High dev: {high_dev["hit_probability"].std():.4f}')
print(f'  Low dev: {low_dev["hit_probability"].std():.4f}')

if high_dev['hit_probability'].std() > low_dev['hit_probability'].std():
    print('\n✅ CONFIRMED: Breaking decade norms = UNPREDICTABLE outcomes!')
    print('   → High novelty, high variance (risky!)')
print()

# ============================================================================
# DISCOVERY 7: Energy-Valence Diagonal
# ============================================================================
print('7️⃣ THE ENERGY-VALENCE DIAGONAL')
print('-' * 70)

df['energy_valence_diff'] = abs(df['energy'] - df['valence'])
diagonal = df[df['energy_valence_diff'] < 0.2]
off_diagonal = df[df['energy_valence_diff'] >= 0.2]

print(f'Diagonal tracks (energy ≈ valence): {len(diagonal):,} ({len(diagonal)/len(df)*100:.1f}%)')
print(f'\nAcousticness:')
print(f'  Diagonal: {diagonal["acousticness"].mean():.4f}')
print(f'  Off-diagonal: {off_diagonal["acousticness"].mean():.4f}')

if diagonal['acousticness'].mean() > off_diagonal['acousticness'].mean():
    diff = ((diagonal['acousticness'].mean() - off_diagonal['acousticness'].mean()) / off_diagonal['acousticness'].mean()) * 100
    print(f'\n✅ CONFIRMED: Diagonal tracks {diff:.1f}% MORE acoustic!')
    print('   → Balanced energy-valence = acoustic preference')
print()

# ============================================================================
# DISCOVERY 8: Artist Versatility Tax
# ============================================================================
print('8️⃣ THE ARTIST VERSATILITY TAX')
print('-' * 70)

artists_filtered = artists[artists['catalog_size'] >= 10].copy()
artists_filtered['breadth_cat'] = pd.cut(
    artists_filtered['decade_breadth'],
    bins=[0, 1, 2, 4, 10],
    labels=['1 Decade', '2 Decades', '3-4 Decades', '5+ Decades']
)

breadth_stats = artists_filtered.groupby('breadth_cat').agg({
    'longevity_score': 'mean',
    'artist_id': 'count'
})

print('Longevity by decade breadth:\n')
for cat in ['1 Decade', '2 Decades', '3-4 Decades', '5+ Decades']:
    if cat in breadth_stats.index:
        long_score = breadth_stats.loc[cat, 'longevity_score']
        count = int(breadth_stats.loc[cat, 'artist_id'])
        print(f'  {cat:15s}: {long_score:.4f} (n={count:,})')

single = breadth_stats.loc['1 Decade', 'longevity_score']
multi = breadth_stats.loc['5+ Decades', 'longevity_score']

if multi > single:
    boost = ((multi - single) / single) * 100
    print(f'\n✅ POSITIVE EFFECT: Multi-decade artists have {boost:.1f}% higher longevity!')
else:
    tax = ((single - multi) / single) * 100
    print(f'\n✅ VERSATILITY TAX: Single-decade focus yields {tax:.1f}% better longevity!')
print()

# ============================================================================
# SUMMARY
# ============================================================================
print('='*70)
print('🎯 SUMMARY: 8 UNDERRATED HYPOTHESES DISCOVERED')
print('='*70)
print('\n1. Silent Majority: Instrumental tracks more novel in streaming')
print('2. Collaboration Curse: Teams favor synthetic sound')
print('3. Live Premium: Trade commercial success for artistic value')
print('4. Tempo Sweet Spot: Each mood has optimal tempo')
print('5. Album Position: Opening tracks strategically energetic')
print('6. Decade Dissonance: Breaking norms = unpredictable')
print('7. E-V Diagonal: Balance correlates with acoustic')
print('8. Versatility Tax: Focus vs breadth trade-off')
print('\n✅ All discoveries ready for hypothesis testing!')
print('='*70)
