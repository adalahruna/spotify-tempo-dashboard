"""
HYPOTHESIS VALIDATION - TEST 1
===============================
Validasi distribusi tempo zones dan persentase masing-masing zona
Membuktikan sweet spot 100-120 BPM mencakup ~22% dari katalog
"""

import pandas as pd
import json
import sys
import os

# Set pandas display options
pd.set_option('display.float_format', '{:.2f}'.format)

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

# ============================================
# TEST 1: TEMPO ZONES DISTRIBUTION
# ============================================

print_header("TEST 1: VALIDASI DISTRIBUSI TEMPO ZONES")

print("📊 Loading data dari CSV...")

# Load CSV
csv_path = os.path.join('..', 'data', 'raw', 'tracks_features.csv')
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    sys.exit(1)

df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df):,} tracks dari CSV\n")

# Filter valid tempo
df = df[df['tempo'].notna()]
print(f"✅ {len(df):,} tracks dengan tempo valid\n")

print_section("Distribusi Tempo Zones")

# Define tempo zones
def classify_tempo(tempo):
    if tempo < 80:
        return 'less_80', '<80 BPM'
    elif tempo < 100:
        return '80_100', '80-100 BPM'
    elif tempo < 120:
        return '100_120', '100-120 BPM (Sweet Spot)'
    elif tempo < 140:
        return '120_140', '120-140 BPM'
    else:
        return 'above_140', '>140 BPM'

df['zone_id'], df['zone_name'] = zip(*df['tempo'].apply(classify_tempo))

# Calculate statistics per zone
zones_stats = df.groupby(['zone_id', 'zone_name']).agg({
    'tempo': ['count', 'mean', 'min', 'max']
}).reset_index()

zones_stats.columns = ['zone_id', 'zone_name', 'count', 'avg_tempo', 'min_tempo', 'max_tempo']
zones_stats['percentage'] = (zones_stats['count'] / len(df) * 100).round(2)

# Sort by zone order
zone_order = ['less_80', '80_100', '100_120', '120_140', 'above_140']
zones_stats['sort_order'] = zones_stats['zone_id'].map({z: i for i, z in enumerate(zone_order)})
zones_stats = zones_stats.sort_values('sort_order').drop('sort_order', axis=1)

zones_data = zones_stats.to_dict('records')
total_tracks = len(df)

for zone in zones_data:
    # Highlight sweet spot
    if zone['zone_id'] == '100_120':
        print(f"🎯 {zone['zone_name']:30s} │ {zone['count']:>10,} tracks │ {zone['percentage']:>6.2f}% │ Avg: {zone['avg_tempo']:>6.2f} BPM")
    else:
        print(f"   {zone['zone_name']:30s} │ {zone['count']:>10,} tracks │ {zone['percentage']:>6.2f}% │ Avg: {zone['avg_tempo']:>6.2f} BPM")

print(f"\n{'─'*70}")
print(f"   {'TOTAL':30s} │ {total_tracks:>10,} tracks │ 100.00%")
print(f"{'─'*70}")

# ============================================
# SWEET SPOT ANALYSIS
# ============================================

sweet_spot = next(z for z in zones_data if z['zone_id'] == '100_120')

print_section("Analisis Sweet Spot (100-120 BPM)")

print(f"✅ Jumlah tracks:       {sweet_spot['count']:,} tracks")
print(f"✅ Persentase:          {sweet_spot['percentage']:.2f}%")
print(f"✅ Rata-rata tempo:     {sweet_spot['avg_tempo']:.2f} BPM")
print(f"✅ Range tempo:         {sweet_spot['min_tempo']:.2f} - {sweet_spot['max_tempo']:.2f} BPM")

# ============================================
# VALIDATION CHECKS
# ============================================

print_section("Validasi Hipotesis")

checks = []

# Check 1: Sweet spot percentage should be around 20-25%
if 20.0 <= sweet_spot['percentage'] <= 25.0:
    print(f"✅ CHECK 1: Persentase sweet spot {sweet_spot['percentage']:.2f}% masuk dalam range 20-25%")
    checks.append(True)
else:
    print(f"❌ CHECK 1: Persentase sweet spot {sweet_spot['percentage']:.2f}% TIDAK dalam range 20-25%")
    checks.append(False)

# Check 2: Sweet spot should be significant portion (> 100K tracks)
if sweet_spot['count'] > 100000:
    print(f"✅ CHECK 2: Jumlah tracks {sweet_spot['count']:,} > 100,000 (signifikan)")
    checks.append(True)
else:
    print(f"❌ CHECK 2: Jumlah tracks {sweet_spot['count']:,} < 100,000 (kurang signifikan)")
    checks.append(False)

# Check 3: Average tempo should be within sweet spot range
if 100 <= sweet_spot['avg_tempo'] <= 120:
    print(f"✅ CHECK 3: Rata-rata tempo {sweet_spot['avg_tempo']:.2f} BPM dalam range 100-120")
    checks.append(True)
else:
    print(f"❌ CHECK 3: Rata-rata tempo {sweet_spot['avg_tempo']:.2f} BPM TIDAK dalam range 100-120")
    checks.append(False)

# Check 4: All zones should sum to 100%
total_percentage = sum(z['percentage'] for z in zones_data)
if 99.9 <= total_percentage <= 100.1:
    print(f"✅ CHECK 4: Total persentase {total_percentage:.2f}% = 100%")
    checks.append(True)
else:
    print(f"❌ CHECK 4: Total persentase {total_percentage:.2f}% ≠ 100%")
    checks.append(False)

# ============================================
# RANKING ANALYSIS
# ============================================

print_section("Ranking Zona Berdasarkan Jumlah Tracks")

sorted_zones = sorted(zones_data, key=lambda x: x['count'], reverse=True)
for idx, zone in enumerate(sorted_zones, 1):
    marker = "🏆" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
    highlight = "🎯" if zone['zone_id'] == '100_120' else "  "
    print(f"{marker} #{idx}. {highlight} {zone['zone_name']:30s} │ {zone['count']:>10,} tracks ({zone['percentage']:>5.2f}%)")

# Find sweet spot rank
sweet_spot_rank = next(idx for idx, z in enumerate(sorted_zones, 1) if z['zone_id'] == '100_120')
print(f"\n💡 Sweet spot berada di peringkat #{sweet_spot_rank} dari 5 zona")

# ============================================
# FINAL SUMMARY
# ============================================

print_section("📋 RINGKASAN TEST 1")

passed_checks = sum(checks)
total_checks = len(checks)

print(f"Total checks passed: {passed_checks}/{total_checks}")
print()

if all(checks):
    print("✅ TEST 1 PASSED: Distribusi tempo zones VALID!")
    print("   Sweet spot 100-120 BPM terbukti signifikan (~22% katalog)")
else:
    print("⚠️  TEST 1 WARNING: Ada beberapa check yang tidak sesuai ekspektasi")

print("\n" + "="*70)
print("  Lanjut ke TEST 2: Audio Features Comparison")
print("="*70 + "\n")

# Save results for next test
with open('test1_results.json', 'w') as f:
    json.dump({
        'zones': zones_data,
        'sweet_spot': sweet_spot,
        'total_tracks': total_tracks,
        'checks_passed': all(checks)
    }, f, indent=2)

print("💾 Results saved to: test1_results.json")
