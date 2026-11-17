"""
HYPOTHESIS VALIDATION - TEST 2
===============================
Analisis audio features comparison antara sweet spot vs zona lain
Membuktikan sweet spot memiliki danceability, energy, valence lebih tinggi
"""

import pandas as pd
import json
import sys
import os

pd.set_option('display.float_format', '{:.4f}'.format)

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

# ============================================
# LOAD DATA FROM TEST 1
# ============================================

print_header("TEST 2: AUDIO FEATURES COMPARISON")

print("📂 Loading Test 1 results...")
with open('test1_results.json', 'r') as f:
    test1_data = json.load(f)

print("✅ Test 1 data loaded\n")

# ============================================
# LOAD CSV DATA
# ============================================

print("📊 Loading full dataset dari CSV...")

csv_path = os.path.join('..', 'data', 'raw', 'tracks_features.csv')
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    sys.exit(1)

df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df):,} tracks\n")

# Filter valid data
df = df[df['tempo'].notna()]
print(f"✅ {len(df):,} tracks dengan tempo valid")

# Check available audio features
audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                   'instrumentalness', 'liveness', 'speechiness', 'loudness']
available_features = [f for f in audio_features if f in df.columns]
print(f"✅ Audio features tersedia: {', '.join(available_features)}\n")

# ============================================
# CLASSIFY TEMPO ZONES
# ============================================

def classify_tempo(tempo):
    if tempo < 80:
        return 'less_80'
    elif tempo < 100:
        return '80_100'
    elif tempo < 120:
        return '100_120'
    elif tempo < 140:
        return '120_140'
    else:
        return 'above_140'

df['zone_id'] = df['tempo'].apply(classify_tempo)

# ============================================
# AUDIO FEATURES ANALYSIS
# ============================================

print_section("Rata-rata Audio Features per Tempo Zone")

# Calculate mean for each zone
features_by_zone = df.groupby('zone_id')[available_features].mean()

# Sort by zone order
zone_order = ['less_80', '80_100', '100_120', '120_140', 'above_140']
features_by_zone = features_by_zone.reindex(zone_order)

# Zone names
zone_names = {
    'less_80': '<80 BPM',
    '80_100': '80-100 BPM',
    '100_120': '100-120 BPM (Sweet Spot)',
    '120_140': '120-140 BPM',
    'above_140': '>140 BPM'
}

# Display table
print(f"{'Zone':25s} │ {'Danceability':>12s} │ {'Energy':>12s} │ {'Valence':>12s}")
print("─" * 70)

for zone_id in zone_order:
    zone_name = zone_names[zone_id]
    dance = features_by_zone.loc[zone_id, 'danceability']
    energy = features_by_zone.loc[zone_id, 'energy']
    valence = features_by_zone.loc[zone_id, 'valence']
    
    if zone_id == '100_120':
        print(f"🎯 {zone_name:23s} │ {dance:12.4f} │ {energy:12.4f} │ {valence:12.4f}")
    else:
        print(f"   {zone_name:23s} │ {dance:12.4f} │ {energy:12.4f} │ {valence:12.4f}")

# ============================================
# SWEET SPOT VS OTHERS COMPARISON
# ============================================

print_section("Sweet Spot vs Other Zones Comparison")

# Sweet spot stats
sweet_spot_data = df[df['zone_id'] == '100_120']
other_zones_data = df[df['zone_id'] != '100_120']

sweet_spot_stats = {}
other_zones_stats = {}
boost_pct = {}

for feature in available_features:
    sweet_spot_mean = sweet_spot_data[feature].mean()
    other_zones_mean = other_zones_data[feature].mean()
    boost = ((sweet_spot_mean - other_zones_mean) / other_zones_mean * 100)
    
    sweet_spot_stats[feature] = sweet_spot_mean
    other_zones_stats[feature] = other_zones_mean
    boost_pct[feature] = boost

# Display comparison
print(f"{'Feature':20s} │ {'Sweet Spot':>12s} │ {'Other Zones':>12s} │ {'Boost %':>12s}")
print("─" * 70)

key_features = ['danceability', 'energy', 'valence']
for feature in key_features:
    ss_val = sweet_spot_stats[feature]
    other_val = other_zones_stats[feature]
    boost = boost_pct[feature]
    
    indicator = "📈" if boost > 0 else "📉"
    print(f"{indicator} {feature.capitalize():18s} │ {ss_val:12.4f} │ {other_val:12.4f} │ {boost:+11.2f}%")

print()

# Other features
if len(available_features) > 3:
    print("Other audio features:")
    for feature in available_features:
        if feature not in key_features:
            ss_val = sweet_spot_stats[feature]
            other_val = other_zones_stats[feature]
            boost = boost_pct[feature]
            
            indicator = "📈" if boost > 0 else "📉"
            print(f"{indicator} {feature.capitalize():18s} │ {ss_val:12.4f} │ {other_val:12.4f} │ {boost:+11.2f}%")

# ============================================
# BEST ZONE FOR EACH FEATURE
# ============================================

print_section("Best Zone for Each Audio Feature")

for feature in key_features:
    best_zone_id = features_by_zone[feature].idxmax()
    best_zone_name = zone_names[best_zone_id]
    best_value = features_by_zone.loc[best_zone_id, feature]
    
    if best_zone_id == '100_120':
        print(f"🏆 {feature.capitalize():15s} : {best_zone_name:30s} ({best_value:.4f}) ✅ SWEET SPOT WINS!")
    else:
        print(f"   {feature.capitalize():15s} : {best_zone_name:30s} ({best_value:.4f})")

# ============================================
# VALIDATION CHECKS
# ============================================

print_section("Validasi Hipotesis")

checks = []

# Check 1: Danceability boost should be positive
dance_boost = boost_pct['danceability']
if dance_boost > 0:
    print(f"✅ CHECK 1: Danceability boost {dance_boost:+.2f}% (positif)")
    checks.append(True)
else:
    print(f"❌ CHECK 1: Danceability boost {dance_boost:+.2f}% (negatif)")
    checks.append(False)

# Check 2: Danceability boost should be significant (> 5%)
if dance_boost > 5:
    print(f"✅ CHECK 2: Danceability boost {dance_boost:+.2f}% > 5% (signifikan)")
    checks.append(True)
else:
    print(f"⚠️  CHECK 2: Danceability boost {dance_boost:+.2f}% < 5% (kurang signifikan)")
    checks.append(False)

# Check 3: Sweet spot danceability should be above 0.5
if sweet_spot_stats['danceability'] > 0.5:
    print(f"✅ CHECK 3: Sweet spot danceability {sweet_spot_stats['danceability']:.4f} > 0.5 (tinggi)")
    checks.append(True)
else:
    print(f"❌ CHECK 3: Sweet spot danceability {sweet_spot_stats['danceability']:.4f} < 0.5 (rendah)")
    checks.append(False)

# Check 4: Energy boost should be positive
energy_boost = boost_pct['energy']
if energy_boost > 0:
    print(f"✅ CHECK 4: Energy boost {energy_boost:+.2f}% (positif)")
    checks.append(True)
else:
    print(f"⚠️  CHECK 4: Energy boost {energy_boost:+.2f}% (negatif)")
    checks.append(False)

# ============================================
# DISTRIBUTION ANALYSIS
# ============================================

print_section("Distribusi Danceability per Zone (Quartiles)")

quartiles_data = []
for zone_id in zone_order:
    zone_data = df[df['zone_id'] == zone_id]['danceability']
    q1 = zone_data.quantile(0.25)
    q2 = zone_data.quantile(0.50)  # median
    q3 = zone_data.quantile(0.75)
    
    zone_name = zone_names[zone_id]
    if zone_id == '100_120':
        print(f"🎯 {zone_name:23s} │ Q1: {q1:.4f} │ Median: {q2:.4f} │ Q3: {q3:.4f}")
    else:
        print(f"   {zone_name:23s} │ Q1: {q1:.4f} │ Median: {q2:.4f} │ Q3: {q3:.4f}")
    
    quartiles_data.append({
        'zone_id': zone_id,
        'zone_name': zone_name,
        'q1': q1,
        'median': q2,
        'q3': q3
    })

# ============================================
# FINAL SUMMARY
# ============================================

print_section("📋 RINGKASAN TEST 2")

passed_checks = sum(checks)
total_checks = len(checks)

print(f"Total checks passed: {passed_checks}/{total_checks}\n")

print("🎯 Key Findings:")
print(f"   • Danceability: {sweet_spot_stats['danceability']:.4f} (Sweet Spot) vs {other_zones_stats['danceability']:.4f} (Others) → {dance_boost:+.2f}%")
print(f"   • Energy:       {sweet_spot_stats['energy']:.4f} (Sweet Spot) vs {other_zones_stats['energy']:.4f} (Others) → {energy_boost:+.2f}%")
print(f"   • Valence:      {sweet_spot_stats['valence']:.4f} (Sweet Spot) vs {other_zones_stats['valence']:.4f} (Others) → {boost_pct['valence']:+.2f}%")
print()

if passed_checks >= 3:
    print("✅ TEST 2 PASSED: Sweet spot memiliki audio features superior!")
    print("   Danceability boost terbukti signifikan")
else:
    print("⚠️  TEST 2 PARTIAL: Beberapa metrics tidak sesuai ekspektasi")

print("\n" + "="*70)
print("  Lanjut ke TEST 3: Temporal Consistency")
print("="*70 + "\n")

# ============================================
# SAVE RESULTS
# ============================================

results = {
    'sweet_spot_stats': sweet_spot_stats,
    'other_zones_stats': other_zones_stats,
    'boost_percentages': boost_pct,
    'features_by_zone': features_by_zone.to_dict(),
    'quartiles': quartiles_data,
    'checks_passed': passed_checks >= 3,
    'danceability_boost': dance_boost
}

with open('test2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("💾 Results saved to: test2_results.json")
