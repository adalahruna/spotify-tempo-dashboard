# 🗣️ Conversational Recommendation System Design

## 💡 **Core Concept**
Instead of complex NLP, use **guided questions** to clarify user intent and narrow down perfect recommendations.

---

## 🎯 **User Flow: Question-Based Filtering**

### **Step 1: Initial Intent**
```
System: "What kind of music are you looking for?"

Options:
[🎉 Party/Dance]  [💪 Workout]     [📚 Study/Focus]
[😊 Happy/Upbeat] [😢 Sad/Emotional] [💤 Relax/Sleep]
[🚗 Driving]      [❤️ Romantic]    [🎸 Discover]
```

### **Step 2: Refine by Energy**
```
System: "How energetic do you want the music?"

Slider: 
[Calm] ●━━━━━━━━━━ [Energetic]
  0%    25%   50%   75%   100%

Or buttons:
[Very Calm] [Moderate] [Energetic] [Very Intense]
```

### **Step 3: Refine by Tempo**
```
System: "What tempo/speed are you feeling?"

Options:
[Slow (60-80)]     - Ballads, ambient
[Moderate (80-110)] - Pop, R&B
[Sweet Spot (100-120)] - Dance, optimal groove ★
[Fast (120-140)]    - Upbeat pop, house
[Very Fast (140+)]  - EDM, workout
```

### **Step 4: Refine by Mood**
```
System: "What's your mood?"

Options:
[😊 Positive/Happy]   - High valence
[😐 Neutral]          - Medium valence
[😢 Sad/Melancholic]  - Low valence
[😤 Intense/Aggressive] - Low valence + high energy
```

### **Step 5: Additional Filters (Optional)**
```
System: "Any preferences?" (can skip)

[✓] Mostly instrumental (no vocals)
[✓] Acoustic/Organic sound
[✓] Loud/Powerful sound
[✓] From specific decade: [dropdown: 1960s-2020s]
```

### **Step 6: Results**
```
System: "Here are your recommendations!"

🎵 Found 47 tracks matching your criteria:
   • Party/Dance mood
   • High energy (0.7-1.0)
   • Sweet spot tempo (100-120 BPM)
   • Positive vibe

[Show top 20 results with play preview]
```

---

## 📊 **Question Tree Design**

```
START
  │
  ├─ Q1: What's your activity/mood?
  │   ├─ Party/Dance
  │   │   └─ Q2: Energy level? → High
  │   │       └─ Q3: Tempo? → 100-130 BPM (Sweet Spot!)
  │   │           └─ Results: energy>0.7, dance>0.7, tempo 100-130
  │   │
  │   ├─ Workout
  │   │   └─ Q2: Workout type?
  │   │       ├─ Cardio/Running → tempo 140-180, energy>0.8
  │   │       ├─ Weights/Strength → tempo 110-140, energy>0.7
  │   │       └─ Yoga/Stretch → tempo 60-90, energy<0.4
  │   │
  │   ├─ Study/Focus
  │   │   └─ Q2: Vocals or instrumental?
  │   │       ├─ Instrumental → instrumentalness>0.5
  │   │       └─ Background vocals OK → instrumentalness>0.2
  │   │       └─ Q3: Tempo? → 70-110 BPM
  │   │           └─ Results: energy<0.4, instrument>0.5, tempo 70-110
  │   │
  │   ├─ Happy/Upbeat
  │   │   └─ Q2: Activity?
  │   │       ├─ Dancing → tempo 100-130, dance>0.7
  │   │       ├─ Singing along → speechiness<0.2
  │   │       └─ Chilling → tempo 90-120
  │   │       └─ Results: valence>0.6, energy>0.6
  │   │
  │   ├─ Sad/Emotional
  │   │   └─ Q2: Need comfort or cathartic?
  │   │       ├─ Comfort (soothing) → acoustic>0.5, tempo 60-90
  │   │       └─ Cathartic (intense) → energy 0.3-0.6, loud>-10
  │   │       └─ Results: valence<0.4, energy<0.5
  │   │
  │   ├─ Relax/Sleep
  │   │   └─ Q2: Activity?
  │   │       ├─ Meditation → instrument>0.7, speech<0.05
  │   │       ├─ Sleep → energy<0.2, tempo 50-80
  │   │       └─ Casual chill → energy<0.4, acoustic>0.5
  │   │
  │   ├─ Driving
  │   │   └─ Q2: What kind of drive?
  │   │       ├─ Highway cruise → tempo 110-130, energy 0.5-0.7
  │   │       ├─ City driving → tempo 90-120, valence>0.5
  │   │       └─ Night drive → valence 0.4-0.7, energy 0.4-0.6
  │   │
  │   └─ Romantic
  │       └─ Q2: Setting?
  │           ├─ Date night → acoustic>0.4, tempo 70-110
  │           ├─ Intimate → energy<0.5, valence 0.5-0.8
  │           └─ Dance/Upbeat → tempo 100-120, dance>0.6
  │
  └─ RESULTS with explanation
```

---

## 🎨 **UI/UX Design**

### **Mockup: Conversational Interface**

```
┌─────────────────────────────────────────────────────────┐
│  🎵 Smart Music Recommendation                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  💬 Let's find your perfect playlist!                   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Question 1 of 3                                   │ │
│  │                                                   │ │
│  │ What are you in the mood for?                    │ │
│  │                                                   │ │
│  │  ┌────────┐  ┌────────┐  ┌────────┐            │ │
│  │  │  😊    │  │  💪    │  │  📚    │            │ │
│  │  │ Happy  │  │ Workout│  │ Study  │            │ │
│  │  └────────┘  └────────┘  └────────┘            │ │
│  │                                                   │ │
│  │  ┌────────┐  ┌────────┐  ┌────────┐            │ │
│  │  │  😢    │  │  💤    │  │  🎉    │            │ │
│  │  │  Sad   │  │ Relax  │  │ Party  │            │ │
│  │  └────────┘  └────────┘  └────────┘            │ │
│  │                                                   │ │
│  │  ┌────────┐  ┌────────┐                         │ │
│  │  │  🚗    │  │  ❤️    │                         │ │
│  │  │Driving │  │Romantic│                         │ │
│  │  └────────┘  └────────┘                         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  or type freely:                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ I want music for...                             │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**After selection:**

```
┌─────────────────────────────────────────────────────────┐
│  🎵 Smart Music Recommendation                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  You selected: 💪 Workout                               │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Question 2 of 3                                   │ │
│  │                                                   │ │
│  │ What type of workout?                            │ │
│  │                                                   │ │
│  │  ┌──────────────┐  ┌──────────────┐             │ │
│  │  │  🏃 Cardio   │  │  🏋️ Weights   │             │ │
│  │  │  Running     │  │  Strength    │             │ │
│  │  │  140-180 BPM │  │  110-140 BPM │             │ │
│  │  └──────────────┘  └──────────────┘             │ │
│  │                                                   │ │
│  │  ┌──────────────┐  ┌──────────────┐             │ │
│  │  │  🧘 Yoga     │  │  🤸 HIIT     │             │ │
│  │  │  Stretch     │  │  Intervals   │             │ │
│  │  │  60-90 BPM   │  │  120-160 BPM │             │ │
│  │  └──────────────┘  └──────────────┘             │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [← Back]                                 [Skip →]     │
└─────────────────────────────────────────────────────────┘
```

**Final step:**

```
┌─────────────────────────────────────────────────────────┐
│  🎵 Smart Music Recommendation                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  You selected: 💪 Workout → 🏃 Cardio                   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Question 3 of 3                                   │ │
│  │                                                   │ │
│  │ How intense?                                     │ │
│  │                                                   │ │
│  │  Energy Level                                    │ │
│  │  ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━● 90%       │ │
│  │  [Calm]  [Moderate]  [High]  [★ Intense]        │ │
│  │                                                   │ │
│  │  Preferred Tempo                                 │ │
│  │  ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━● 160 BPM   │ │
│  │  [60]   [90]   [120]   [150]   [180]            │ │
│  │                        ★ Sweet Spot              │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [← Back]              [Get Recommendations →]         │
└─────────────────────────────────────────────────────────┘
```

**Results:**

```
┌─────────────────────────────────────────────────────────┐
│  🎵 Your Perfect Playlist                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ✨ Based on your preferences:                          │
│     • 💪 Workout (Cardio/Running)                       │
│     • ⚡ High intensity (0.8-1.0)                       │
│     • 🎵 Fast tempo (150-170 BPM)                       │
│     • 😊 Upbeat mood                                    │
│                                                         │
│  📊 Found 234 tracks | Showing top 20                   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. Blinding Lights                              │   │
│  │    The Weeknd • 2020                            │   │
│  │    171 BPM | Energy: 0.73 | Dance: 0.51        │   │
│  │    [▶ Play Preview]                             │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ 2. Don't Start Now                              │   │
│  │    Dua Lipa • 2019                              │   │
│  │    124 BPM | Energy: 0.79 | Dance: 0.79        │   │
│  │    [▶ Play Preview]                             │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ 3. Levitating                                   │   │
│  │    Dua Lipa • 2020                              │   │
│  │    103 BPM | Energy: 0.70 | Dance: 0.70        │   │
│  │    [▶ Play Preview]                             │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [🔄 Adjust Preferences]  [💾 Save Playlist]           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 **Technical Implementation**

### **State Management**

```javascript
// User session state
const recommendationState = {
  step: 1,
  maxSteps: 3,
  
  // Collected answers
  answers: {
    primaryMood: null,      // 'workout', 'study', 'party', etc.
    secondaryChoice: null,  // activity-specific
    energyLevel: 0.5,       // 0-1 slider
    tempo: 120,             // 60-200 BPM
    valence: null,          // happiness level
    additionalFilters: []   // optional checkboxes
  },
  
  // Computed filters for query
  filters: {
    energy: { min: 0, max: 1 },
    tempo: { min: 60, max: 200 },
    valence: { min: 0, max: 1 },
    danceability: { min: 0, max: 1 },
    acousticness: { min: 0, max: 1 },
    instrumentalness: { min: 0, max: 1 }
  }
};
```

### **Question Flow Logic**

```javascript
// Define question trees
const QUESTION_TREES = {
  workout: {
    questions: [
      {
        id: 'workout_type',
        text: 'What type of workout?',
        options: [
          { label: '🏃 Cardio', value: 'cardio', 
            filters: { energy: [0.7, 1.0], tempo: [140, 180] }},
          { label: '🏋️ Weights', value: 'weights',
            filters: { energy: [0.6, 0.9], tempo: [110, 140] }},
          { label: '🧘 Yoga', value: 'yoga',
            filters: { energy: [0.2, 0.4], tempo: [60, 90], acousticness: [0.5, 1.0] }},
          { label: '🤸 HIIT', value: 'hiit',
            filters: { energy: [0.8, 1.0], tempo: [120, 180] }}
        ]
      },
      {
        id: 'intensity',
        text: 'How intense?',
        type: 'slider',
        range: [0, 1],
        default: 0.7,
        mapTo: 'energy'
      }
    ]
  },
  
  study: {
    questions: [
      {
        id: 'vocal_preference',
        text: 'Vocals or instrumental?',
        options: [
          { label: '🎹 Pure Instrumental', value: 'pure_inst',
            filters: { instrumentalness: [0.7, 1.0], speechiness: [0, 0.05] }},
          { label: '🎤 Minimal Vocals', value: 'min_vocal',
            filters: { instrumentalness: [0.3, 0.7], speechiness: [0, 0.1] }},
          { label: '🎵 Background Music', value: 'bg_music',
            filters: { energy: [0.2, 0.4], loudness: [-20, -10] }}
        ]
      },
      {
        id: 'tempo',
        text: 'Preferred tempo?',
        type: 'slider',
        range: [60, 120],
        default: 90,
        mapTo: 'tempo'
      }
    ]
  },
  
  party: {
    questions: [
      {
        id: 'party_vibe',
        text: 'What kind of party?',
        options: [
          { label: '🕺 Dance Floor', value: 'dance',
            filters: { danceability: [0.7, 1.0], energy: [0.7, 1.0], tempo: [110, 130] }},
          { label: '🎉 High Energy', value: 'hype',
            filters: { energy: [0.8, 1.0], valence: [0.7, 1.0], tempo: [120, 140] }},
          { label: '🍹 Chill Vibes', value: 'chill',
            filters: { energy: [0.5, 0.7], valence: [0.6, 0.9], tempo: [90, 110] }}
        ]
      }
    ]
  },
  
  happy: {
    questions: [
      {
        id: 'activity',
        text: 'What will you be doing?',
        options: [
          { label: '💃 Dancing', value: 'dance',
            filters: { danceability: [0.7, 1.0], tempo: [100, 130] }},
          { label: '🎤 Singing Along', value: 'sing',
            filters: { speechiness: [0.1, 0.3], valence: [0.7, 1.0] }},
          { label: '😌 Just Chilling', value: 'chill',
            filters: { energy: [0.5, 0.7], valence: [0.6, 0.9] }}
        ]
      }
    ]
  },
  
  sad: {
    questions: [
      {
        id: 'sad_type',
        text: 'Looking for comfort or catharsis?',
        options: [
          { label: '🤗 Comforting', value: 'comfort',
            filters: { valence: [0.2, 0.4], energy: [0.2, 0.4], acousticness: [0.5, 1.0] }},
          { label: '😭 Cathartic', value: 'cathartic',
            filters: { valence: [0.1, 0.3], energy: [0.3, 0.6], loudness: [-15, -5] }},
          { label: '🎹 Melancholic', value: 'melancholic',
            filters: { valence: [0.2, 0.4], instrumentalness: [0.3, 0.8], tempo: [60, 90] }}
        ]
      }
    ]
  },
  
  relax: {
    questions: [
      {
        id: 'relax_activity',
        text: 'What are you relaxing from?',
        options: [
          { label: '🧘 Meditation', value: 'meditation',
            filters: { energy: [0.1, 0.3], instrumentalness: [0.7, 1.0], tempo: [50, 80] }},
          { label: '💤 Sleep', value: 'sleep',
            filters: { energy: [0.0, 0.2], loudness: [-30, -15], tempo: [40, 70] }},
          { label: '📖 Reading', value: 'reading',
            filters: { energy: [0.2, 0.4], acousticness: [0.5, 1.0], speechiness: [0, 0.05] }}
        ]
      }
    ]
  },
  
  driving: {
    questions: [
      {
        id: 'drive_type',
        text: 'What kind of drive?',
        options: [
          { label: '🛣️ Highway Cruise', value: 'highway',
            filters: { tempo: [110, 130], energy: [0.5, 0.7], valence: [0.5, 0.8] }},
          { label: '🏙️ City', value: 'city',
            filters: { tempo: [90, 120], energy: [0.4, 0.6] }},
          { label: '🌃 Night Drive', value: 'night',
            filters: { tempo: [80, 110], energy: [0.3, 0.6], valence: [0.4, 0.7] }}
        ]
      }
    ]
  },
  
  romantic: {
    questions: [
      {
        id: 'romantic_setting',
        text: 'What\'s the vibe?',
        options: [
          { label: '🕯️ Intimate', value: 'intimate',
            filters: { energy: [0.2, 0.5], valence: [0.5, 0.8], acousticness: [0.5, 1.0] }},
          { label: '💑 Date Night', value: 'date',
            filters: { energy: [0.4, 0.6], valence: [0.6, 0.9], tempo: [80, 110] }},
          { label: '💃 Romantic Dance', value: 'dance',
            filters: { danceability: [0.6, 0.9], tempo: [100, 120], valence: [0.6, 0.9] }}
        ]
      }
    ]
  }
};
```

### **API Endpoint**

```python
@app.route('/api/recommend', methods=['POST'])
def recommend_tracks():
    """
    Smart recommendation based on conversational filters
    """
    data = request.json
    
    # Extract filters from conversation
    filters = data.get('filters', {})
    limit = data.get('limit', 20)
    
    # Build SQL query
    sql = """
        SELECT 
            id, name, artists, year,
            tempo, energy, valence, danceability,
            acousticness, instrumentalness, speechiness,
            -- Calculate match score
            (
                CASE WHEN energy BETWEEN %(energy_min)s AND %(energy_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.3 +
                CASE WHEN tempo BETWEEN %(tempo_min)s AND %(tempo_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.3 +
                CASE WHEN valence BETWEEN %(valence_min)s AND %(valence_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.2 +
                CASE WHEN danceability BETWEEN %(dance_min)s AND %(dance_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.1 +
                CASE WHEN acousticness BETWEEN %(acoustic_min)s AND %(acoustic_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.05 +
                CASE WHEN instrumentalness BETWEEN %(instrument_min)s AND %(instrument_max)s 
                     THEN 1.0 ELSE 0.5 END * 0.05
            ) as match_score
        FROM spotify_tracks_raw
        WHERE 1=1
    """
    
    params = {}
    
    # Apply filters
    if 'energy' in filters:
        sql += " AND energy BETWEEN %(energy_min)s AND %(energy_max)s"
        params['energy_min'] = filters['energy'][0]
        params['energy_max'] = filters['energy'][1]
    
    if 'tempo' in filters:
        sql += " AND tempo BETWEEN %(tempo_min)s AND %(tempo_max)s"
        params['tempo_min'] = filters['tempo'][0]
        params['tempo_max'] = filters['tempo'][1]
    
    # ... similar for other filters
    
    sql += " ORDER BY match_score DESC LIMIT %(limit)s"
    params['limit'] = limit
    
    # Execute query
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    results = cur.fetchall()
    
    return jsonify({
        'success': True,
        'count': len(results),
        'filters_applied': filters,
        'results': results
    })
```

---

## 🎓 **Why This Approach is BETTER**

### **1. User-Friendly**
✅ No need to understand "valence" or "energy"  
✅ Natural language choices  
✅ Progressive disclosure (step-by-step)

### **2. Demo-able**
✅ Interactive during presentation  
✅ Dosen bisa test live  
✅ Impressive conversational flow

### **3. Academically Valid**
✅ Clear intent classification  
✅ Feature mapping documented  
✅ Explainable results

### **4. Flexible**
✅ Easy to add new question paths  
✅ Can combine multiple filters  
✅ Users can go back and adjust

### **5. No Complex NLP Needed**
✅ Rule-based decision tree  
✅ Predefined mappings  
✅ Fast implementation (3-5 days)

---

## 🚀 **Implementation Timeline**

| Day | Task |
|-----|------|
| 1 | Design question trees for 8 moods |
| 2 | Build conversational UI components |
| 3 | Implement filter mapping logic |
| 4 | Build recommendation API endpoint |
| 5 | Integration + testing |
| **Total** | **5 days** |

---

## 💡 **Example Conversation**

**Scenario: User wants study music**

```
System: "What are you in the mood for?"
User: [Clicks 📚 Study/Focus]

System: "Do you prefer vocals or instrumental?"
User: [Clicks 🎹 Pure Instrumental]

System: "What tempo feels right?"
User: [Adjusts slider to 85 BPM]

System: "Perfect! Finding instrumental focus music around 85 BPM..."

Results:
✨ Found 1,247 tracks
📊 Filters: Instrumental (>0.7), Low energy (<0.4), Tempo 80-90 BPM
🎵 Top recommendation: [Lo-fi hip hop beats track]
```

---

**What do you think? Mau implement conversational approach ini?** 🎯
