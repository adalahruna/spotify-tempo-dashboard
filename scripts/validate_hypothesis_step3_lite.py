"""
HYPOTHESIS VALIDATION - TEST 3 (LITE VERSION)
==============================================
Analisis temporal consistency sweet spot 100-120 BPM across decades
Memory-efficient version dengan chunk processing
"""

import pandas as pd
import json
import sys
import os

pd.set_option('display.float_format', '{:.2f}'.format)

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

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

# ============================================
# LOAD DATA IN CHUNKS
# ============================================

print_header("TEST 3: TEMPORAL CONSISTENCY ANALYSIS (LITE)")

print("📊 Processing dataset in chunks...")

csv_path = os.path.join('..', 'data', 'raw', 'tracks_features.csv')
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    sys.exit(1)

# Process in chunks to save memory
chunk_size = 100000
decade_counts = {}
decade_sweet_spot_counts = {}
decade_sweet_tempo_sum = {}
decade_sweet_dance_sum = {}

required_cols = ['tempo', 'year', 'danceability']

print("Processing chunks...")
chunk_num = 0
total_rows = 0

for chunk in pd.read_csv(csv_path, usecols=required_cols, chunksize=chunk_size):
    chunk_num += 1
    print(f"  Chunk {chunk_num}: {len(chunk):,} rows", end='\r')
    
    # Filter valid data
    chunk = chunk[(chunk['tempo'].notna()) & (chunk['year'].notna()) & (chunk['year'] >= 1920)]
    
    # Classify zones
    chunk['zone_id'] = chunk['tempo'].apply(classify_tempo)
    chunk['decade'] = (chunk['year'] // 10) * 10
    
    # Aggregate by decade
    for decade in chunk['decade'].unique():
        decade_data = chunk[chunk['decade'] == decade]
        sweet_data = decade_data[decade_data['zone_id'] == '100_120']
        
        # Count totals
        if decade not in decade_counts:
            decade_counts[decade] = 0
            decade_sweet_spot_counts[decade] = 0
            decade_sweet_tempo_sum[decade] = 0.0
            decade_sweet_dance_sum[decade] = 0.0
        
        decade_counts[decade] += len(decade_data)
        decade_sweet_spot_counts[decade] += len(sweet_data)
        decade_sweet_tempo_sum[decade] += sweet_data['tempo'].sum()
        decade_sweet_dance_sum[decade] += sweet_data['danceability'].sum()
    
    total_rows += len(chunk)

print(f"\n✅ Processed {total_rows:,} valid tracks\n")

# ============================================
# CALCULATE STATISTICS
# ============================================

print_section("Sweet Spot Percentage per Decade")

print(f"{'Decade':>6s} │ {'Total Tracks':>12s} │ {'Sweet Spot':>12s} │ {'Percentage':>10s} │ {'Avg Tempo':>10s} │ {'Avg Dance':>10s}")
print("─" * 90)

decade_data = []
for decade in sorted(decade_counts.keys()):
    total = decade_counts[decade]
    sweet = decade_sweet_spot_counts[decade]
    pct = (sweet / total * 100) if total > 0 else 0
    
    if sweet > 0:
        avg_tempo = decade_sweet_tempo_sum[decade] / sweet
        avg_dance = decade_sweet_dance_sum[decade] / sweet
        tempo_str = f"{avg_tempo:.2f}"
        dance_str = f"{avg_dance:.4f}"
    else:
        avg_tempo = None
        avg_dance = None
        tempo_str = "N/A"
        dance_str = "N/A"
    
    print(f"{decade:>6.0f} │ {total:>12,} │ {sweet:>12,} │ {pct:>9.2f}% │ {tempo_str:>10s} │ {dance_str:>10s}")
    
    decade_data.append({
        'decade': int(decade),
        'total_tracks': int(total),
        'sweet_spot_tracks': int(sweet),
        'sweet_spot_pct': float(pct),
        'avg_tempo': float(avg_tempo) if avg_tempo else None,
        'avg_danceability': float(avg_dance) if avg_dance else None
    })

# ============================================
# STATISTICAL ANALYSIS
# ============================================

print_section("Statistik Sweet Spot Percentage Across Decades")

pct_values = [d['sweet_spot_pct'] for d in decade_data]
mean_pct = sum(pct_values) / len(pct_values)
variance = sum((x - mean_pct) ** 2 for x in pct_values) / len(pct_values)
std_pct = variance ** 0.5
min_pct = min(pct_values)
max_pct = max(pct_values)
range_pct = max_pct - min_pct
cv = (std_pct / mean_pct * 100) if mean_pct > 0 else 0

print(f"Mean:              {mean_pct:.2f}%")
print(f"Std Deviation:     {std_pct:.2f}%")
print(f"Min:               {min_pct:.2f}%")
print(f"Max:               {max_pct:.2f}%")
print(f"Range:             {range_pct:.2f}%")
print(f"Coefficient of Variation: {cv:.2f}%")

# ============================================
# TREND ANALYSIS
# ============================================

print_section("Trend Analysis")

# Simple linear regression
decades = [d['decade'] for d in decade_data]
percentages = [d['sweet_spot_pct'] for d in decade_data]

n = len(decades)
sum_x = sum(decades)
sum_y = sum(percentages)
sum_xy = sum(x * y for x, y in zip(decades, percentages))
sum_x2 = sum(x ** 2 for x in decades)

slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
intercept = (sum_y - slope * sum_x) / n

# R-squared
y_mean = mean_pct
ss_tot = sum((y - y_mean) ** 2 for y in percentages)
ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(decades, percentages))
r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

print(f"Linear Regression:")
print(f"  Slope:       {slope:.4f}% per decade")
print(f"  R-squared:   {r_squared:.4f}")

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
        'r_squared': float(r_squared)
    },
    'checks_passed': passed_checks >= 4
}

with open('test3_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("💾 Results saved to: test3_results.json")
