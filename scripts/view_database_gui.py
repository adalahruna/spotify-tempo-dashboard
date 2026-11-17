"""
Simple Database Viewer GUI using Tkinter + subprocess
No psycopg2 needed - uses psql directly
"""

import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os

# ==============================================
# CONFIGURATION
# ==============================================
DB_CONFIG = {
    'host': 'localhost',
    'database': 'spotify_music_db',
    'user': 'postgres',
    'password': 'tempo2024',
    'port': 5432
}

PSQL_PATH = r'D:\postgre\bin\psql.exe'

# ==============================================
# FUNCTIONS
# ==============================================

def run_query(query):
    """Execute SQL query via psql"""
    try:
        result = subprocess.run(
            [
                PSQL_PATH,
                '-U', DB_CONFIG['user'],
                '-h', DB_CONFIG['host'],
                '-p', str(DB_CONFIG['port']),
                '-d', DB_CONFIG['database'],
                '-c', query
            ],
            env={**os.environ, 'PGPASSWORD': DB_CONFIG['password']},
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"ERROR:\n{result.stderr}"
    
    except Exception as e:
        return f"ERROR: {str(e)}"

def execute_custom_query():
    """Execute user's custom query"""
    query = query_text.get("1.0", tk.END).strip()
    if not query:
        messagebox.showwarning("Empty Query", "Please enter a SQL query")
        return
    
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", "Executing...\n")
    root.update()
    
    result = run_query(query)
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", result)

def load_preset(query, description):
    """Load preset query"""
    query_text.delete("1.0", tk.END)
    query_text.insert("1.0", query)
    status_label.config(text=f"Loaded: {description}")

# ==============================================
# PRESET QUERIES
# ==============================================

PRESETS = {
    "Count Records": (
        "SELECT COUNT(*) as total_records FROM spotify_tracks_raw;",
        "Total records in database"
    ),
    "Sample Data": (
        "SELECT name, artists, tempo, energy, year FROM spotify_tracks_raw LIMIT 20;",
        "First 20 tracks"
    ),
    "Tempo Zones": (
        """SELECT 
    CASE 
        WHEN tempo < 80 THEN '<80 BPM'
        WHEN tempo < 100 THEN '80-100 BPM'
        WHEN tempo <= 120 THEN '100-120 BPM (Sweet Spot)'
        WHEN tempo <= 140 THEN '120-140 BPM'
        ELSE '>140 BPM'
    END as tempo_zone,
    COUNT(*) as count,
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER())::numeric, 2) as percentage
FROM spotify_tracks_raw
WHERE tempo IS NOT NULL
GROUP BY tempo_zone
ORDER BY count DESC;""",
        "Tempo distribution by zones"
    ),
    "Top Hit Tracks": (
        """SELECT name, artists, year, 
    ROUND(tempo::numeric, 2) as tempo,
    ROUND(energy::numeric, 3) as energy,
    ROUND(danceability::numeric, 3) as danceability,
    ROUND(((energy + danceability + valence) / 3)::numeric, 3) as hit_score
FROM spotify_tracks_raw
WHERE tempo BETWEEN 100 AND 120
  AND energy > 0.7
  AND danceability > 0.6
ORDER BY hit_score DESC
LIMIT 20;""",
        "Top 20 tracks by hit formula"
    ),
    "Decade Trends": (
        """SELECT 
    FLOOR(year/10)*10 as decade,
    COUNT(*) as total_tracks,
    COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) as sweet_spot_tracks,
    ROUND((COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) * 100.0 / COUNT(*))::numeric, 2) as sweet_spot_pct
FROM spotify_tracks_raw
WHERE year IS NOT NULL AND tempo IS NOT NULL
GROUP BY decade
ORDER BY decade;""",
        "Sweet spot percentage by decade"
    ),
    "Tempo Stats": (
        """SELECT 
    MIN(tempo) as min_tempo,
    MAX(tempo) as max_tempo,
    ROUND(AVG(tempo::numeric), 2) as avg_tempo,
    COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) as sweet_spot_count,
    ROUND((COUNT(CASE WHEN tempo BETWEEN 100 AND 120 THEN 1 END) * 100.0 / COUNT(*))::numeric, 2) as sweet_spot_pct
FROM spotify_tracks_raw
WHERE tempo IS NOT NULL;""",
        "Overall tempo statistics"
    )
}

# ==============================================
# GUI SETUP
# ==============================================

root = tk.Tk()
root.title("Spotify Database Viewer")
root.geometry("1000x700")

# Title
title_label = tk.Label(root, text="🎵 Spotify Tracks Database Viewer", 
                        font=("Arial", 16, "bold"), pady=10)
title_label.pack()

# Preset Buttons Frame
preset_frame = tk.Frame(root)
preset_frame.pack(pady=5)

tk.Label(preset_frame, text="Quick Queries:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

for name, (query, desc) in PRESETS.items():
    btn = tk.Button(preset_frame, text=name, 
                    command=lambda q=query, d=desc: load_preset(q, d),
                    padx=10, pady=5)
    btn.pack(side=tk.LEFT, padx=2)

# Query Input
query_frame = tk.Frame(root)
query_frame.pack(pady=10, padx=10, fill=tk.BOTH)

tk.Label(query_frame, text="SQL Query:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

query_text = scrolledtext.ScrolledText(query_frame, height=8, font=("Consolas", 10))
query_text.pack(fill=tk.BOTH, expand=True)
query_text.insert("1.0", "SELECT COUNT(*) FROM spotify_tracks_raw;")

# Execute Button
execute_btn = tk.Button(root, text="▶ Execute Query", command=execute_custom_query,
                        font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                        padx=20, pady=10)
execute_btn.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Ready", font=("Arial", 9), fg="gray")
status_label.pack()

# Results
result_frame = tk.Frame(root)
result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

tk.Label(result_frame, text="Results:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

result_text = scrolledtext.ScrolledText(result_frame, height=15, font=("Consolas", 9))
result_text.pack(fill=tk.BOTH, expand=True)

# Footer
footer = tk.Label(root, text=f"Connected to: {DB_CONFIG['database']} @ {DB_CONFIG['host']}",
                  font=("Arial", 8), fg="gray")
footer.pack(pady=5)

# Run GUI
root.mainloop()
