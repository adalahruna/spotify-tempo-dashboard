"""
Visualisasi Analisis Tempo Sweet Spot
Generate charts untuk thesis presentation
"""

import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# ==============================================
# CONFIGURATION
# ==============================================
FIREBASE_CRED_PATH = r'D:\Semester 5\BIG DATA\Project\firebase-credentials.json'
OUTPUT_DIR = Path(r'D:\Semester 5\BIG DATA\Project\visualizations')

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# ==============================================
# FIREBASE CONNECTION
# ==============================================

print("🔥 Connecting to Firestore...")
cred = credentials.Certificate(FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
print("✅ Connected!\n")

# ==============================================
# LOAD DATA
# ==============================================

print("📊 Loading data from Firestore...")

# 1. Tempo Zones
tempo_zones_ref = db.collection('tempo_zones').stream()
tempo_zones_data = []
for doc in tempo_zones_ref:
    data = doc.to_dict()
    tempo_zones_data.append(data)

tempo_zones_df = pd.DataFrame(tempo_zones_data)
tempo_zones_df = tempo_zones_df.sort_values('count', ascending=False)

# 2. Decade Trends
decade_trends_ref = db.collection('decade_trends').stream()
decade_trends_data = []
for doc in decade_trends_ref:
    data = doc.to_dict()
    decade_trends_data.append(data)

decade_trends_df = pd.DataFrame(decade_trends_data)
decade_trends_df = decade_trends_df.sort_values('decade')

# 3. Audio Features Comparison
audio_comp_ref = db.collection('audio_features_comparison').stream()
audio_comp_data = []
for doc in audio_comp_ref:
    data = doc.to_dict()
    audio_comp_data.append(data)

audio_comp_df = pd.DataFrame(audio_comp_data)

# 4. Global Stats
global_stats = db.collection('summary').document('global_stats').get().to_dict()

print(f"✅ Loaded data:\n")
print(f"   • {len(tempo_zones_df)} tempo zones")
print(f"   • {len(decade_trends_df)} decades")
print(f"   • {len(audio_comp_df)} audio feature comparisons")
print(f"   • Global stats: {global_stats['total_tracks']:,} tracks\n")

# ==============================================
# VISUALIZATIONS
# ==============================================

# Chart 1: Tempo Zone Distribution (Bar Chart)
print("📊 Creating Chart 1: Tempo Zone Distribution...")
fig, ax = plt.subplots(figsize=(12, 7))

colors = ['#ff6b6b' if 'Sweet Spot' in name else '#4ecdc4' 
          for name in tempo_zones_df['zone_name']]

bars = ax.bar(tempo_zones_df['zone_name'], tempo_zones_df['count'], 
              color=colors, edgecolor='black', linewidth=1.5)

# Add percentage labels on bars
for i, (bar, pct) in enumerate(zip(bars, tempo_zones_df['percentage'])):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{pct}%',
            ha='center', va='bottom', fontweight='bold', fontsize=12)

ax.set_xlabel('Tempo Zone', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Tracks', fontsize=13, fontweight='bold')
ax.set_title('Distribusi Tempo Tracks Spotify (1.2M Tracks)', 
             fontsize=16, fontweight='bold', pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}K'))
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_tempo_distribution.png', dpi=300, bbox_inches='tight')
print(f"   ✅ Saved: 01_tempo_distribution.png\n")
plt.close()

# Chart 2: Danceability Comparison (Bar Chart)
print("📊 Creating Chart 2: Danceability Comparison...")
fig, ax = plt.subplots(figsize=(10, 7))

categories = audio_comp_df['category'].replace({
    'sweet_spot': '100-120 BPM\n(Sweet Spot)',
    'other_tempo': 'Other Tempo\nZones'
})

colors_comp = ['#ff6b6b', '#95a5a6']
bars = ax.bar(categories, audio_comp_df['avg_danceability'], 
              color=colors_comp, edgecolor='black', linewidth=1.5, width=0.6)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontweight='bold', fontsize=14)

# Calculate difference
sweet_spot_dance = audio_comp_df[audio_comp_df['category'] == 'sweet_spot']['avg_danceability'].values[0]
other_dance = audio_comp_df[audio_comp_df['category'] == 'other_tempo']['avg_danceability'].values[0]
diff_pct = ((sweet_spot_dance - other_dance) / other_dance) * 100

ax.set_ylabel('Average Danceability', fontsize=13, fontweight='bold')
ax.set_title(f'Perbandingan Danceability: Sweet Spot vs Others\n(+{diff_pct:.1f}% Higher in Sweet Spot)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylim(0, 0.6)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_danceability_comparison.png', dpi=300, bbox_inches='tight')
print(f"   ✅ Saved: 02_danceability_comparison.png\n")
plt.close()

# Chart 3: Decade Trends (Line Chart)
print("📊 Creating Chart 3: Decade Trends...")
fig, ax = plt.subplots(figsize=(14, 7))

# Filter out decade 0 (invalid data)
decade_trends_filtered = decade_trends_df[decade_trends_df['decade'] > 1900]

ax.plot(decade_trends_filtered['decade'], decade_trends_filtered['sweet_spot_pct'], 
        marker='o', linewidth=3, markersize=8, color='#ff6b6b', label='Sweet Spot %')

# Add horizontal line at 22%
ax.axhline(y=22, color='#95a5a6', linestyle='--', linewidth=2, alpha=0.7, label='Overall Average (22.18%)')

# Highlight peaks
max_pct = decade_trends_filtered['sweet_spot_pct'].max()
max_decade = decade_trends_filtered[decade_trends_filtered['sweet_spot_pct'] == max_pct]['decade'].values[0]
ax.scatter([max_decade], [max_pct], s=300, c='gold', edgecolors='black', linewidths=2, zorder=5)

ax.set_xlabel('Decade', fontsize=13, fontweight='bold')
ax.set_ylabel('Sweet Spot Percentage (%)', fontsize=13, fontweight='bold')
ax.set_title('Tren Sweet Spot (100-120 BPM) Across Decades (1900-2020)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(range(1900, 2030, 10))
ax.set_xticklabels(range(1900, 2030, 10), rotation=45)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_decade_trends.png', dpi=300, bbox_inches='tight')
print(f"   ✅ Saved: 03_decade_trends.png\n")
plt.close()

# Chart 4: Audio Features Radar Chart (Comparison)
print("📊 Creating Chart 4: Audio Features Comparison...")
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

features = ['Energy', 'Danceability', 'Valence', 'Acousticness']
sweet_spot_values = [
    audio_comp_df[audio_comp_df['category'] == 'sweet_spot']['avg_energy'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'sweet_spot']['avg_danceability'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'sweet_spot']['avg_valence'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'sweet_spot']['avg_acousticness'].values[0],
]

other_values = [
    audio_comp_df[audio_comp_df['category'] == 'other_tempo']['avg_energy'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'other_tempo']['avg_danceability'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'other_tempo']['avg_valence'].values[0],
    audio_comp_df[audio_comp_df['category'] == 'other_tempo']['avg_acousticness'].values[0],
]

# Close the plot
sweet_spot_values += sweet_spot_values[:1]
other_values += other_values[:1]

angles = [n / float(len(features)) * 2 * 3.14159 for n in range(len(features))]
angles += angles[:1]

ax.plot(angles, sweet_spot_values, 'o-', linewidth=2, color='#ff6b6b', label='Sweet Spot (100-120 BPM)')
ax.fill(angles, sweet_spot_values, alpha=0.25, color='#ff6b6b')

ax.plot(angles, other_values, 'o-', linewidth=2, color='#4ecdc4', label='Other Tempo')
ax.fill(angles, other_values, alpha=0.25, color='#4ecdc4')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(features, fontsize=12, fontweight='bold')
ax.set_ylim(0, 0.6)
ax.set_title('Audio Features Comparison\nSweet Spot vs Other Tempo', 
             fontsize=16, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
ax.grid(True)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '04_audio_features_radar.png', dpi=300, bbox_inches='tight')
print(f"   ✅ Saved: 04_audio_features_radar.png\n")
plt.close()

# Chart 5: Summary Statistics (Info Graphic)
print("📊 Creating Chart 5: Summary Statistics...")
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

# Title
ax.text(0.5, 0.95, 'ANALISIS TEMPO SWEET SPOT', 
        ha='center', fontsize=24, fontweight='bold', 
        transform=ax.transAxes)

ax.text(0.5, 0.88, 'Spotify Tracks Dataset (1920-2020)', 
        ha='center', fontsize=14, color='gray',
        transform=ax.transAxes)

# Key findings
findings = [
    {
        'title': 'Total Tracks Analyzed',
        'value': f"{global_stats['total_tracks']:,}",
        'icon': '🎵',
        'y': 0.75
    },
    {
        'title': 'Average Tempo',
        'value': f"{global_stats['avg_tempo']} BPM",
        'subtitle': '(Within Sweet Spot Range!)',
        'icon': '⏱️',
        'y': 0.60
    },
    {
        'title': 'Sweet Spot (100-120 BPM)',
        'value': f"{global_stats['sweet_spot_percentage']}%",
        'subtitle': f"({global_stats['sweet_spot_count']:,} tracks)",
        'icon': '⭐',
        'y': 0.45
    },
    {
        'title': 'Danceability Advantage',
        'value': f"+{diff_pct:.1f}%",
        'subtitle': 'Higher in Sweet Spot',
        'icon': '💃',
        'y': 0.30
    },
    {
        'title': 'Year Range',
        'value': f"{int(global_stats['earliest_year'])}-{int(global_stats['latest_year'])}",
        'subtitle': '100 years of music data',
        'icon': '📅',
        'y': 0.15
    }
]

for finding in findings:
    ax.text(0.1, finding['y'], finding['icon'], 
            fontsize=40, transform=ax.transAxes)
    ax.text(0.25, finding['y'] + 0.02, finding['title'], 
            fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.text(0.25, finding['y'] - 0.04, finding['value'], 
            fontsize=22, fontweight='bold', color='#ff6b6b', transform=ax.transAxes)
    if 'subtitle' in finding:
        ax.text(0.25, finding['y'] - 0.08, finding['subtitle'], 
                fontsize=11, color='gray', transform=ax.transAxes)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '05_summary_stats.png', dpi=300, bbox_inches='tight')
print(f"   ✅ Saved: 05_summary_stats.png\n")
plt.close()

# ==============================================
# SUMMARY
# ==============================================

print("=" * 60)
print("✅ VISUALIZATIONS COMPLETE!")
print("=" * 60)
print(f"\n📁 Saved to: {OUTPUT_DIR}")
print("\n📊 Charts created:")
print("   1. 01_tempo_distribution.png - Tempo zone distribution")
print("   2. 02_danceability_comparison.png - Danceability sweet spot vs others")
print("   3. 03_decade_trends.png - Sweet spot trends across decades")
print("   4. 04_audio_features_radar.png - Audio features comparison")
print("   5. 05_summary_stats.png - Key statistics summary")
print("\n💡 Ready for thesis presentation!")
