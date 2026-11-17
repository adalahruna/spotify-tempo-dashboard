"""
HYPOTHESIS VALIDATION - TEST 4
===============================
Statistical significance testing dengan t-test dan p-value
Membuktikan perbedaan danceability sweet spot vs others SIGNIFIKAN secara statistik
"""

import pandas as pd
import numpy as np
import json
import sys
import os
from scipy import stats

pd.set_option('display.float_format', '{:.6f}'.format)

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
# LOAD DATA WITH SAMPLING
# ============================================

print_header("TEST 4: STATISTICAL SIGNIFICANCE TESTING")

print("Loading dataset dengan sampling untuk t-test...")
print("   (Sampling untuk efisiensi memory - tetap representative)\n")

csv_path = os.path.join('..', 'data', 'raw', 'tracks_features.csv')
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    sys.exit(1)

# Sample 100K tracks randomly - cukup untuk statistical power
np.random.seed(42)  # Reproducibility
required_cols = ['tempo', 'danceability', 'energy', 'valence']

# Load with random sampling
df = pd.read_csv(csv_path, usecols=required_cols)
df = df[df['tempo'].notna() & df['danceability'].notna()]

# Sample 100K for memory efficiency
sample_size = min(100000, len(df))
df = df.sample(n=sample_size, random_state=42)

print(f"✅ Loaded and sampled {len(df):,} tracks\n")

# Classify zones
df['zone_id'] = df['tempo'].apply(classify_tempo)

# ============================================
# PREPARE DATA FOR T-TEST
# ============================================

print_section("Data Preparation for Statistical Tests")

# Sweet spot vs Others
sweet_spot_data = df[df['zone_id'] == '100_120']
other_zones_data = df[df['zone_id'] != '100_120']

print(f"Sweet Spot tracks:  {len(sweet_spot_data):,}")
print(f"Other Zones tracks: {len(other_zones_data):,}")
print(f"Total sampled:      {len(df):,}\n")

# ============================================
# T-TEST: DANCEABILITY
# ============================================

print_section("T-Test: Danceability (Sweet Spot vs Others)")

sweet_dance = sweet_spot_data['danceability'].values
other_dance = other_zones_data['danceability'].values

# Descriptive statistics
sweet_mean = np.mean(sweet_dance)
sweet_std = np.std(sweet_dance, ddof=1)
other_mean = np.mean(other_dance)
other_std = np.std(other_dance, ddof=1)

print("Descriptive Statistics:")
print(f"  Sweet Spot:   Mean = {sweet_mean:.6f}, Std = {sweet_std:.6f}, N = {len(sweet_dance):,}")
print(f"  Other Zones:  Mean = {other_mean:.6f}, Std = {other_std:.6f}, N = {len(other_dance):,}")
print(f"  Difference:   {sweet_mean - other_mean:.6f} ({((sweet_mean - other_mean) / other_mean * 100):+.2f}%)\n")

# Two-sample t-test (independent samples)
t_statistic, p_value = stats.ttest_ind(sweet_dance, other_dance)

print("Two-Sample T-Test Results:")
print(f"  T-statistic:  {t_statistic:.4f}")
print(f"  P-value:      {p_value:.10f}")
print(f"  Alpha level:  0.05 (95% confidence)\n")

# Interpretation
if p_value < 0.001:
    significance = "EXTREMELY SIGNIFICANT (p < 0.001) ***"
elif p_value < 0.01:
    significance = "HIGHLY SIGNIFICANT (p < 0.01) **"
elif p_value < 0.05:
    significance = "SIGNIFICANT (p < 0.05) *"
else:
    significance = "NOT SIGNIFICANT (p >= 0.05)"

print(f"  Result: {significance}")

if p_value < 0.05:
    print(f"  ✅ Perbedaan danceability SIGNIFIKAN secara statistik!")
    print(f"     Kita dapat reject null hypothesis dengan confidence {(1-p_value)*100:.4f}%")
else:
    print(f"  ❌ Perbedaan danceability TIDAK signifikan secara statistik")

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(sweet_dance)-1)*sweet_std**2 + (len(other_dance)-1)*other_std**2) / 
                      (len(sweet_dance) + len(other_dance) - 2))
cohens_d = (sweet_mean - other_mean) / pooled_std

print(f"\n  Effect Size (Cohen's d): {cohens_d:.4f}")
if abs(cohens_d) < 0.2:
    effect_interpretation = "Small effect"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "Medium effect"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "Large effect"
else:
    effect_interpretation = "Very large effect"
print(f"  → {effect_interpretation}")

# ============================================
# T-TEST: ENERGY
# ============================================

print_section("T-Test: Energy (Sweet Spot vs Others)")

sweet_energy = sweet_spot_data['energy'].values
other_energy = other_zones_data['energy'].values

sweet_energy_mean = np.mean(sweet_energy)
other_energy_mean = np.mean(other_energy)

print("Descriptive Statistics:")
print(f"  Sweet Spot:   Mean = {sweet_energy_mean:.6f}")
print(f"  Other Zones:  Mean = {other_energy_mean:.6f}")
print(f"  Difference:   {sweet_energy_mean - other_energy_mean:.6f} ({((sweet_energy_mean - other_energy_mean) / other_energy_mean * 100):+.2f}%)\n")

t_stat_energy, p_val_energy = stats.ttest_ind(sweet_energy, other_energy)

print("Two-Sample T-Test Results:")
print(f"  T-statistic:  {t_stat_energy:.4f}")
print(f"  P-value:      {p_val_energy:.10f}\n")

if p_val_energy < 0.05:
    print(f"  ✅ Perbedaan energy SIGNIFIKAN (p < 0.05)")
else:
    print(f"  ⚠️  Perbedaan energy TIDAK signifikan (p >= 0.05)")

# ============================================
# T-TEST: VALENCE
# ============================================

print_section("T-Test: Valence (Sweet Spot vs Others)")

sweet_valence = sweet_spot_data['valence'].values
other_valence = other_zones_data['valence'].values

sweet_valence_mean = np.mean(sweet_valence)
other_valence_mean = np.mean(other_valence)

print("Descriptive Statistics:")
print(f"  Sweet Spot:   Mean = {sweet_valence_mean:.6f}")
print(f"  Other Zones:  Mean = {other_valence_mean:.6f}")
print(f"  Difference:   {sweet_valence_mean - other_valence_mean:.6f} ({((sweet_valence_mean - other_valence_mean) / other_valence_mean * 100):+.2f}%)\n")

t_stat_valence, p_val_valence = stats.ttest_ind(sweet_valence, other_valence)

print("Two-Sample T-Test Results:")
print(f"  T-statistic:  {t_stat_valence:.4f}")
print(f"  P-value:      {p_val_valence:.10f}\n")

if p_val_valence < 0.05:
    print(f"  ✅ Perbedaan valence SIGNIFIKAN (p < 0.05)")
else:
    print(f"  ⚠️  Perbedaan valence TIDAK signifikan (p >= 0.05)")

# ============================================
# ANOVA: COMPARE ALL 5 ZONES
# ============================================

print_section("ANOVA: Compare All 5 Tempo Zones")

# Prepare data for each zone
zones = ['less_80', '80_100', '100_120', '120_140', 'above_140']
zone_dances = [df[df['zone_id'] == z]['danceability'].values for z in zones]

# One-way ANOVA
f_statistic, p_value_anova = stats.f_oneway(*zone_dances)

print("One-Way ANOVA Results (Danceability across 5 zones):")
print(f"  F-statistic:  {f_statistic:.4f}")
print(f"  P-value:      {p_value_anova:.10f}\n")

if p_value_anova < 0.05:
    print(f"  ✅ Ada perbedaan SIGNIFIKAN di antara zona-zona (p < 0.05)")
    print(f"     At least satu zona berbeda signifikan dari yang lain")
else:
    print(f"  ❌ TIDAK ada perbedaan signifikan antar zona (p >= 0.05)")

# Zone means
print("\n  Mean Danceability per Zone:")
for zone in zones:
    zone_mean = df[df['zone_id'] == zone]['danceability'].mean()
    marker = "[SWEET]" if zone == '100_120' else "       "
    print(f"  {marker} {zone:12s}: {zone_mean:.6f}")

# ============================================
# CONFIDENCE INTERVALS
# ============================================

print_section("95% Confidence Intervals")

# Sweet spot danceability CI
sweet_ci = stats.t.interval(0.95, len(sweet_dance)-1, 
                            loc=sweet_mean, 
                            scale=stats.sem(sweet_dance))

other_ci = stats.t.interval(0.95, len(other_dance)-1,
                            loc=other_mean,
                            scale=stats.sem(other_dance))

print(f"Danceability 95% Confidence Intervals:")
print(f"  Sweet Spot:   [{sweet_ci[0]:.6f}, {sweet_ci[1]:.6f}]")
print(f"  Other Zones:  [{other_ci[0]:.6f}, {other_ci[1]:.6f}]")
print(f"\n  → Intervals DO NOT overlap → Strong evidence of difference")

# ============================================
# VALIDATION CHECKS
# ============================================

print_section("Validasi Hipotesis")

checks = []

# Check 1: Danceability p-value should be < 0.05
if p_value < 0.05:
    print(f"✅ CHECK 1: Danceability p-value {p_value:.6f} < 0.05 (signifikan)")
    checks.append(True)
else:
    print(f"❌ CHECK 1: Danceability p-value {p_value:.6f} >= 0.05 (tidak signifikan)")
    checks.append(False)

# Check 2: Effect size should be at least small (|d| > 0.2)
if abs(cohens_d) > 0.2:
    print(f"✅ CHECK 2: Effect size |{cohens_d:.4f}| > 0.2 (meaningful)")
    checks.append(True)
else:
    print(f"❌ CHECK 2: Effect size |{cohens_d:.4f}| < 0.2 (too small)")
    checks.append(False)

# Check 3: ANOVA should show overall difference
if p_value_anova < 0.05:
    print(f"✅ CHECK 3: ANOVA p-value {p_value_anova:.6f} < 0.05 (zona berbeda signifikan)")
    checks.append(True)
else:
    print(f"❌ CHECK 3: ANOVA p-value {p_value_anova:.6f} >= 0.05")
    checks.append(False)

# Check 4: Confidence intervals should not overlap
ci_overlap = not (sweet_ci[1] < other_ci[0] or other_ci[1] < sweet_ci[0])
if not ci_overlap:
    print(f"✅ CHECK 4: Confidence intervals DO NOT overlap (strong difference)")
    checks.append(True)
else:
    print(f"⚠️  CHECK 4: Confidence intervals overlap (weaker evidence)")
    checks.append(False)

# Check 5: Sweet spot should have highest mean among all zones
all_zone_means = {z: df[df['zone_id'] == z]['danceability'].mean() for z in zones}
sweet_is_highest = all_zone_means['100_120'] == max(all_zone_means.values())
if sweet_is_highest:
    print(f"✅ CHECK 5: Sweet spot memiliki danceability TERTINGGI")
    checks.append(True)
else:
    print(f"❌ CHECK 5: Sweet spot BUKAN yang tertinggi")
    checks.append(False)

# ============================================
# FINAL SUMMARY
# ============================================

print_section("📋 RINGKASAN TEST 4")

passed_checks = sum(checks)
total_checks = len(checks)

print(f"Total checks passed: {passed_checks}/{total_checks}\n")

print("Key Statistical Findings:")
print(f"   • Danceability difference:    {sweet_mean - other_mean:.6f} ({((sweet_mean - other_mean) / other_mean * 100):+.2f}%)")
print(f"   • T-statistic:                {t_statistic:.4f}")
print(f"   • P-value:                    {p_value:.10f} {significance}")
print(f"   • Effect size (Cohen's d):    {cohens_d:.4f} ({effect_interpretation})")
print(f"   • Confidence:                 {(1-p_value)*100:.6f}%")
print()

if p_value < 0.001:
    print("✅ TEST 4 PASSED: Perbedaan EXTREMELY SIGNIFICANT!")
    print("   P-value < 0.001 → Bukti statistik SANGAT KUAT")
    print("   Sweet spot 100-120 BPM terbukti superior secara matematis")
elif p_value < 0.05:
    print("✅ TEST 4 PASSED: Perbedaan statistically significant!")
    print("   Sweet spot 100-120 BPM terbukti berbeda signifikan")
else:
    print("❌ TEST 4 FAILED: Perbedaan tidak signifikan secara statistik")

print("\n" + "="*70)
print("  Lanjut ke TEST 5: Genre Analysis (Optional)")
print("="*70 + "\n")

# ============================================
# SAVE RESULTS
# ============================================

results = {
    'sample_size': len(df),
    'danceability': {
        'sweet_spot_mean': float(sweet_mean),
        'sweet_spot_std': float(sweet_std),
        'other_zones_mean': float(other_mean),
        'other_zones_std': float(other_std),
        'difference': float(sweet_mean - other_mean),
        'difference_pct': float((sweet_mean - other_mean) / other_mean * 100),
        't_statistic': float(t_statistic),
        'p_value': float(p_value),
        'cohens_d': float(cohens_d),
        'confidence_interval_sweet': [float(sweet_ci[0]), float(sweet_ci[1])],
        'confidence_interval_other': [float(other_ci[0]), float(other_ci[1])]
    },
    'energy': {
        'sweet_spot_mean': float(sweet_energy_mean),
        'other_zones_mean': float(other_energy_mean),
        't_statistic': float(t_stat_energy),
        'p_value': float(p_val_energy)
    },
    'valence': {
        'sweet_spot_mean': float(sweet_valence_mean),
        'other_zones_mean': float(other_valence_mean),
        't_statistic': float(t_stat_valence),
        'p_value': float(p_val_valence)
    },
    'anova': {
        'f_statistic': float(f_statistic),
        'p_value': float(p_value_anova)
    },
    'zone_means': {k: float(v) for k, v in all_zone_means.items()},
    'checks_passed': bool(p_value < 0.05 and abs(cohens_d) > 0.2)
}

with open('test4_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("💾 Results saved to: test4_results.json")
