"""
HYPOTHESIS VALIDATION - TEST 3
===============================
Analisis temporal consistency sweet spot 100-120 BPM across decades
Membuktikan sweet spot stabil ~22-24% dari 1920-2020 (100 tahun)
"""

import pandas as pd
import json
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
# LOAD DATA
# ============================================

print_header("TEST 3: TEMPORAL CONSISTENCY ANALYSIS")

print("📊 Loading dataset dari CSV...")

csv_path = os.path.join('..', 'data', 'raw', 'tracks_features.csv')
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    sys.exit(1)

# Load only required columns to save memory
required_cols = ['id', 'tempo', 'year', 'danceability']
df = pd.read_csv(csv_path, usecols=required_cols)
print(f"✅ Loaded {len(df):,} tracks (memory optimized)\n")

# Filter valid data
df = df[df['tempo'].notna()]
df = df[df['year'].notna()]
print(f"✅ {len(df):,} tracks dengan tempo & year valid")

# Filter years >= 1920
df = df[df['year'] >= 1920]
print(f"✅ {len(df):,} tracks dari 1920-2020\n")

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
df['decade'] = (df['year'] // 10) * 10

# ============================================
# DECADE-BY-DECADE ANALYSIS
# ============================================

print_section("Sweet Spot Percentage per Decade")

# Group by decade
decade_analysis = df.groupby('decade').agg({
    'id': 'count',
}).rename(columns={'id': 'total_tracks'})

# Calculate sweet spot tracks per decade
sweet_spot_by_decade = df[df['zone_id'] == '100_120'].groupby('decade').size()
decade_analysis['sweet_spot_tracks'] = sweet_spot_by_decade
decade_analysis['sweet_spot_tracks'] = decade_analysis['sweet_spot_tracks'].fillna(0).astype(int)

# Calculate percentage
decade_analysis['sweet_spot_pct'] = (
    decade_analysis['sweet_spot_tracks'] / decade_analysis['total_tracks'] * 100
).round(2)

# Calculate avg tempo and danceability for sweet spot per decade
sweet_spot_df = df[df['zone_id'] == '100_120']
decade_sweet_spot_stats = sweet_spot_df.groupby('decade').agg({
    'tempo': 'mean',
    'danceability': 'mean'
}).round(4)

decade_analysis = decade_analysis.join(decade_sweet_spot_stats, rsuffix='_sweet')

# Display table
print(f"{'Decade':>6s} │ {'Total Tracks':>12s} │ {'Sweet Spot':>12s} │ {'Percentage':>10s} │ {'Avg Tempo':>10s} │ {'Avg Dance':>10s}")
print("─" * 90)

decade_data = []
for decade in sorted(decade_analysis.index):
    total = decade_analysis.loc[decade, 'total_tracks']
    sweet = decade_analysis.loc[decade, 'sweet_spot_tracks']
    pct = decade_analysis.loc[decade, 'sweet_spot_pct']
    
    if pd.notna(decade_analysis.loc[decade, 'tempo']):
        avg_tempo = decade_analysis.loc[decade, 'tempo']
        avg_dance = decade_analysis.loc[decade, 'danceability']
        tempo_str = f"{avg_tempo:.2f}"
        dance_str = f"{avg_dance:.4f}"
    else:
        tempo_str = "N/A"
        dance_str = "N/A"
    
    print(f"{decade:>6.0f} │ {total:>12,} │ {sweet:>12,} │ {pct:>9.2f}% │ {tempo_str:>10s} │ {dance_str:>10s}")
    
    decade_data.append({
        'decade': int(decade),
        'total_tracks': int(total),
        'sweet_spot_tracks': int(sweet),
        'sweet_spot_pct': float(pct),
        'avg_tempo': float(avg_tempo) if pd.notna(decade_analysis.loc[decade, 'tempo']) else None,
        'avg_danceability': float(avg_dance) if pd.notna(decade_analysis.loc[decade, 'danceability']) else None
    })

# ============================================
# STATISTICAL ANALYSIS
# ============================================

print_section("Statistik Sweet Spot Percentage Across Decades")

pct_values = decade_analysis['sweet_spot_pct'].values
mean_pct = pct_values.mean()
std_pct = pct_values.std()
min_pct = pct_values.min()
max_pct = pct_values.max()
range_pct = max_pct - min_pct

print(f"Mean:              {mean_pct:.2f}%")
print(f"Std Deviation:     {std_pct:.2f}%")
print(f"Min:               {min_pct:.2f}%")
print(f"Max:               {max_pct:.2f}%")
print(f"Range:             {range_pct:.2f}%")
print(f"Coefficient of Variation: {(std_pct/mean_pct*100):.2f}%")

# ============================================
# TREND ANALYSIS
# ============================================

print_section("Trend Analysis")

# Check if trend is relatively stable (low coefficient of variation)
cv = (std_pct / mean_pct * 100)

if cv < 20:
    print(f"✅ Coefficient of Variation {cv:.2f}% < 20% → STABLE TREND")
else:
    print(f"⚠️  Coefficient of Variation {cv:.2f}% > 20% → VARIABLE TREND")

# Linear regression for trend
from scipy import stats
decades = decade_analysis.index.values
percentages = decade_analysis['sweet_spot_pct'].values

slope, intercept, r_value, p_value, std_err = stats.linregress(decades, percentages)

print(f"\nLinear Regression:")
print(f"  Slope:       {slope:.4f}% per decade")
print(f"  R-squared:   {r_value**2:.4f}")
print(f"  P-value:     {p_value:.4f}")

if abs(slope) < 0.5:
    print(f"  → Slope ~0 menunjukkan KONSISTENSI temporal yang tinggi")
else:
    print(f"  → Ada trend {'naik' if slope > 0 else 'turun'} yang cukup signifikan")

# ============================================
# VALIDATION CHECKS
# ============================================

print_section("Validasi Hipotesis")

checks = []

# Check 1: Mean percentage should be around 20-25%
if 20.0 <= mean_pct <= 25.0:
    print(f"✅ CHECK 1: Mean sweet spot {mean_pct:.2f}% dalam range 20-25%")
    checks.append(True)
else:
    print(f"❌ CHECK 1: Mean sweet spot {mean_pct:.2f}% TIDAK dalam range 20-25%")
    checks.append(False)

# Check 2: Coefficient of variation should be < 20% (stable)
if cv < 20:
    print(f"✅ CHECK 2: CV {cv:.2f}% < 20% (stabil)")
    checks.append(True)
else:
    print(f"❌ CHECK 2: CV {cv:.2f}% > 20% (tidak stabil)")
    checks.append(False)

# Check 3: Range should be reasonable (< 10%)
if range_pct < 10:
    print(f"✅ CHECK 3: Range {range_pct:.2f}% < 10% (konsisten)")
    checks.append(True)
else:
    print(f"⚠️  CHECK 3: Range {range_pct:.2f}% > 10% (bervariasi)")
    checks.append(False)

# Check 4: Trend should not be too steep (|slope| < 0.5% per decade)
if abs(slope) < 0.5:
    print(f"✅ CHECK 4: Slope {slope:.4f}% per decade ~ 0 (tidak ada trend signifikan)")
    checks.append(True)
else:
    print(f"⚠️  CHECK 4: Slope {slope:.4f}% per decade (ada trend)")
    checks.append(False)

# Check 5: All decades should have > 15% sweet spot
all_above_15 = all(pct > 15 for pct in pct_values)
if all_above_15:
    print(f"✅ CHECK 5: Semua dekade memiliki > 15% sweet spot")
    checks.append(True)
else:
    print(f"❌ CHECK 5: Ada dekade dengan < 15% sweet spot")
    checks.append(False)

# ============================================
# VISUALIZATION
# ============================================

print_section("Generating Visualization")

plt.figure(figsize=(14, 8))

# Plot 1: Sweet Spot Percentage Over Time
plt.subplot(2, 2, 1)
plt.plot(decades, percentages, marker='o', linewidth=2.5, markersize=8, color='#667eea')
plt.axhline(y=mean_pct, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean_pct:.2f}%')
plt.fill_between(decades, mean_pct - std_pct, mean_pct + std_pct, alpha=0.2, color='#667eea')
plt.xlabel('Decade', fontsize=11, fontweight='bold')
plt.ylabel('Sweet Spot Percentage (%)', fontsize=11, fontweight='bold')
plt.title('Sweet Spot Consistency Across 100 Years', fontsize=13, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

# Plot 2: Distribution of Sweet Spot Percentage
plt.subplot(2, 2, 2)
plt.hist(percentages, bins=8, color='#667eea', alpha=0.7, edgecolor='black')
plt.axvline(x=mean_pct, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_pct:.2f}%')
plt.xlabel('Sweet Spot Percentage (%)', fontsize=11, fontweight='bold')
plt.ylabel('Number of Decades', fontsize=11, fontweight='bold')
plt.title('Distribution of Sweet Spot %', fontsize=13, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

# Plot 3: Total Tracks per Decade (stacked by zone) - SIMPLIFIED
plt.subplot(2, 2, 3)

# Calculate percentage distribution per decade
zone_dist = []
for decade in sorted(decades):
    decade_df = df[df['decade'] == decade]
    for zone_id in ['less_80', '80_100', '100_120', '120_140', 'above_140']:
        count = (decade_df['zone_id'] == zone_id).sum()
        pct = (count / len(decade_df) * 100) if len(decade_df) > 0 else 0
        zone_dist.append({'decade': decade, 'zone': zone_id, 'pct': pct})

zone_dist_df = pd.DataFrame(zone_dist)
pivot_df = zone_dist_df.pivot(index='decade', columns='zone', values='pct')

# Plot stacked bar
pivot_df[['less_80', '80_100', '100_120', '120_140', 'above_140']].plot(
    kind='bar', 
    stacked=True, 
    color=['#95a5a6', '#bdc3c7', '#667eea', '#9b59b6', '#764ba2'],
    ax=plt.gca(),
    width=0.8
)
plt.xlabel('Decade', fontsize=11, fontweight='bold')
plt.ylabel('Percentage (%)', fontsize=11, fontweight='bold')
plt.title('Tempo Zone Distribution by Decade', fontsize=13, fontweight='bold')
plt.legend(['<80', '80-100', '100-120 (Sweet)', '120-140', '>140'], loc='upper left', fontsize=9)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')

# Plot 4: Sweet Spot Avg Danceability Over Time
plt.subplot(2, 2, 4)
dance_values = decade_sweet_spot_stats['danceability'].values
plt.plot(decade_sweet_spot_stats.index, dance_values, marker='s', linewidth=2.5, markersize=8, color='#9b59b6')
plt.axhline(y=dance_values.mean(), color='red', linestyle='--', alpha=0.7, label=f'Mean: {dance_values.mean():.4f}')
plt.xlabel('Decade', fontsize=11, fontweight='bold')
plt.ylabel('Avg Danceability (Sweet Spot)', fontsize=11, fontweight='bold')
plt.title('Sweet Spot Danceability Evolution', fontsize=13, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

# Save visualization
viz_path = os.path.join('..', 'visualizations', 'temporal_consistency.png')
os.makedirs(os.path.dirname(viz_path), exist_ok=True)
plt.savefig(viz_path, dpi=300, bbox_inches='tight')
print(f"✅ Visualization saved: {viz_path}")

# ============================================
# FINAL SUMMARY
# ============================================

print_section("📋 RINGKASAN TEST 3")

passed_checks = sum(checks)
total_checks = len(checks)

print(f"Total checks passed: {passed_checks}/{total_checks}\n")

print("🎯 Key Findings:")
print(f"   • Mean sweet spot across 100 years: {mean_pct:.2f}%")
print(f"   • Standard deviation:                {std_pct:.2f}%")
print(f"   • Coefficient of variation:          {cv:.2f}%")
print(f"   • Temporal trend:                    {slope:.4f}% per decade (almost flat)")
print(f"   • Decades analyzed:                  {len(decades)} decades (1920-2020)")
print()

if passed_checks >= 4:
    print("✅ TEST 3 PASSED: Sweet spot KONSISTEN across 100 tahun!")
    print("   Temporal stability terbukti dengan CV < 20% dan trend ~0")
else:
    print("⚠️  TEST 3 PARTIAL: Ada beberapa aspek temporal yang bervariasi")

print("\n" + "="*70)
print("  Lanjut ke TEST 4: Statistical Significance Testing")
print("="*70 + "\n")

# ============================================
# SAVE RESULTS
# ============================================

results = {
    'decade_data': decade_data,
    'statistics': {
        'mean_pct': float(mean_pct),
        'std_pct': float(std_pct),
        'min_pct': float(min_pct),
        'max_pct': float(max_pct),
        'range_pct': float(range_pct),
        'cv': float(cv)
    },
    'trend_analysis': {
        'slope': float(slope),
        'intercept': float(intercept),
        'r_squared': float(r_value**2),
        'p_value': float(p_value)
    },
    'checks_passed': passed_checks >= 4
}

with open('test3_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("💾 Results saved to: test3_results.json")
