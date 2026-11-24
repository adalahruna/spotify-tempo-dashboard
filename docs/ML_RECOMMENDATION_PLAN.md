# 🎵 ML Recommendation System - Feasibility & Design

## 📋 **Your Idea:**
> "Rekomendasi lagu berdasarkan **makna lagu** dan **pertanyaan user**"

---

## ✅ **Feasibility Analysis**

### **Current Data Available:**
```python
# Audio Features (from Spotify API):
- tempo (BPM)
- danceability (0-1)
- energy (0-1)
- valence (0-1)              # "Happiness" / positivity
- acousticness (0-1)
- instrumentalness (0-1)
- liveness (0-1)
- speechiness (0-1)
- loudness (dB)
- duration_ms

# Metadata:
- name, artists, year
```

### **What We DON'T Have:**
❌ **Lyrics** (kata-kata lagu)  
❌ **Song meaning/themes** (tema/makna)  
❌ **Genre labels**  
❌ **Language**  
❌ **Song descriptions**  

---

## 🤔 **Is "Semantic Recommendation" Possible?**

### **Option 1: Pure Semantic (What You Asked)**
**Requirement:** Lyrics + NLP model  
**Complexity:** ⭐⭐⭐⭐⭐ (Very High)  
**Feasibility:** ⚠️ **CHALLENGING** - Need lyrics dataset + LLM integration

**Example:**
```
User: "Recommend sad breakup songs"
System: Analyzes lyrics → Finds themes of sadness, loss, breakup
Result: Returns songs with matching themes
```

**Challenges:**
1. No lyrics in current dataset (need external API like Genius/Musixmatch)
2. Need NLP model (BERT, GPT) untuk analyze meaning
3. Expensive API calls (Genius API has rate limits)
4. Processing time (slow for 1.2M tracks)

**Verdict:** 🟡 **Possible but COMPLEX** - Not recommended for thesis timeline

---

### **Option 2: Emotion-Based (Recommended Alternative)**
**Requirement:** Use `valence` + `energy` + audio features  
**Complexity:** ⭐⭐⭐ (Moderate)  
**Feasibility:** ✅ **FEASIBLE** - Data already exists!

**Core Idea:**
Map user questions → Emotion states → Audio features

**Example:**
```
User: "I need songs to cheer me up"
System: Maps to → High valence + High energy
Result: Returns upbeat, positive songs

User: "Songs for relaxation"
System: Maps to → Low energy + High acousticness
Result: Returns calm, acoustic songs

User: "Workout playlist"
System: Maps to → High energy + High tempo (120-140 BPM)
Result: Returns energetic, fast songs
```

**Mapping Table:**
| User Intent | Valence | Energy | Tempo | Acousticness |
|------------|---------|--------|-------|--------------|
| Happy/Upbeat | High (>0.6) | High (>0.6) | 100-140 | Low |
| Sad/Melancholic | Low (<0.4) | Low (<0.4) | 60-100 | Medium |
| Energetic/Workout | Medium | High (>0.7) | 120-180 | Low |
| Calm/Relaxing | Medium | Low (<0.3) | 60-90 | High (>0.6) |
| Party/Dance | High (>0.6) | High (>0.7) | 100-130 | Low |
| Focus/Study | Low-Med | Low (<0.4) | 70-110 | Med-High |
| Romantic | Med-High | Low-Med | 70-110 | Med-High |
| Angry/Aggressive | Low-Med | High (>0.8) | 120-180 | Low |

**Verdict:** ✅ **RECOMMENDED** - Realistic, demo-able, defensible

---

### **Option 3: Hybrid Approach (Best of Both)**
**Requirement:** Audio features + Basic genre/mood tags  
**Complexity:** ⭐⭐⭐⭐ (High but Manageable)  
**Feasibility:** ✅ **FEASIBLE** - Add lightweight metadata

**Core Idea:**
Combine emotion-based + simple text tags

**How it works:**
1. **Pre-process:** Add mood tags to tracks (one-time, can be semi-automated)
2. **User query:** "Recommend sad songs about love"
3. **System:** 
   - Parse query → Extract keywords ("sad", "love")
   - Map "sad" → Low valence + Low energy
   - Filter by tags (if exists)
   - Rank by audio feature similarity
4. **Result:** Returns matching tracks

**Example Tags (can add manually for top tracks):**
```python
{
  "Shape of You": ["love", "romantic", "pop", "dance"],
  "Blinding Lights": ["energetic", "night", "driving", "80s"],
  "Someone You Loved": ["sad", "breakup", "emotional", "piano"]
}
```

**Verdict:** ✅ **BALANCED** - More semantic than pure audio, less complex than full NLP

---

## 🎯 **RECOMMENDED APPROACH: Emotion-Based + ML**

### **Why This Works Best:**

1. ✅ **Data Already Exists** - No need for external APIs
2. ✅ **Fast** - Query in <100ms (indexed PostgreSQL)
3. ✅ **Defensible** - Backed by Spotify's research on audio features
4. ✅ **Demo-able** - Works real-time in dashboard
5. ✅ **Academically Valid** - Emotion recognition from audio is established field
6. ✅ **Scalable** - Works with 1.2M tracks without issues

### **Technical Architecture:**

```
┌─────────────────────────────────────────────────┐
│  USER INPUT                                     │
│  "I need songs for studying"                    │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  INTENT CLASSIFIER (Simple NLP)                 │
│  - Keyword matching                             │
│  - Predefined intents (10-15 categories)        │
│  - Maps to audio feature ranges                 │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  FEATURE MAPPING                                │
│  "studying" → {                                 │
│    valence: 0.3-0.5,                           │
│    energy: 0.2-0.4,                            │
│    tempo: 70-110,                              │
│    instrumentalness: >0.5                       │
│  }                                              │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  ML RECOMMENDATION ENGINE                       │
│  1. Filter by feature ranges                    │
│  2. Calculate similarity scores                 │
│  3. Apply sweet spot boost (if applicable)      │
│  4. Rank by relevance                          │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  RESULTS                                        │
│  Top 20 tracks with explanation                │
│  "These songs have low energy and high          │
│   instrumentalness, perfect for focus"          │
└─────────────────────────────────────────────────┘
```

---

## 💻 **Implementation Plan**

### **Phase 1: Intent Classification (1-2 days)**

**Create intent mapping:**
```python
INTENT_MAP = {
    # Happy/Upbeat
    "happy|upbeat|cheerful|joy|positive": {
        "intent": "happy",
        "valence": (0.6, 1.0),
        "energy": (0.6, 1.0),
        "tempo": (100, 140),
        "danceability": (0.5, 1.0)
    },
    
    # Sad/Melancholic
    "sad|melancholic|depressed|down|blue": {
        "intent": "sad",
        "valence": (0.0, 0.4),
        "energy": (0.0, 0.4),
        "tempo": (60, 100),
        "acousticness": (0.3, 1.0)
    },
    
    # Workout/Energy
    "workout|gym|exercise|run|cardio": {
        "intent": "workout",
        "energy": (0.7, 1.0),
        "tempo": (120, 180),
        "danceability": (0.6, 1.0),
        "loudness": (-8, 0)
    },
    
    # Study/Focus
    "study|focus|concentrate|work": {
        "intent": "focus",
        "energy": (0.2, 0.4),
        "valence": (0.3, 0.6),
        "instrumentalness": (0.5, 1.0),
        "speechiness": (0.0, 0.1)
    },
    
    # Relaxation
    "relax|calm|chill|sleep|meditation": {
        "intent": "relax",
        "energy": (0.0, 0.3),
        "acousticness": (0.6, 1.0),
        "tempo": (60, 90),
        "loudness": (-20, -8)
    },
    
    # Party/Dance
    "party|dance|club|night|festival": {
        "intent": "party",
        "energy": (0.7, 1.0),
        "danceability": (0.7, 1.0),
        "valence": (0.6, 1.0),
        "tempo": (110, 130)
    },
    
    # Romantic
    "romantic|love|date|intimate": {
        "intent": "romantic",
        "valence": (0.5, 0.8),
        "energy": (0.3, 0.6),
        "acousticness": (0.4, 1.0),
        "tempo": (70, 110)
    },
    
    # Driving
    "drive|road|trip|cruise": {
        "intent": "driving",
        "energy": (0.5, 0.8),
        "tempo": (100, 130),
        "valence": (0.5, 0.8)
    }
}
```

### **Phase 2: Recommendation Engine (2-3 days)**

**Algorithm:**
```python
def recommend_by_emotion(user_query, limit=20):
    # 1. Parse user query
    intent_match = classify_intent(user_query)
    
    # 2. Get feature ranges
    feature_ranges = INTENT_MAP[intent_match]
    
    # 3. Build SQL query with filters
    sql = """
        SELECT 
            id, name, artists, year,
            tempo, danceability, energy, valence,
            acousticness, instrumentalness,
            -- Calculate relevance score
            (
                -- Valence match (40% weight)
                (1 - ABS(valence - %s)) * 0.4 +
                -- Energy match (30% weight)
                (1 - ABS(energy - %s)) * 0.3 +
                -- Tempo match (20% weight)
                (1 - ABS(tempo - %s) / 100) * 0.2 +
                -- Other features (10% weight)
                (acousticness * %s + danceability * %s) * 0.1
            ) as relevance_score
        FROM spotify_tracks_raw
        WHERE
            valence BETWEEN %s AND %s
            AND energy BETWEEN %s AND %s
            AND tempo BETWEEN %s AND %s
        ORDER BY relevance_score DESC
        LIMIT %s
    """
    
    # 4. Execute and return
    return results
```

### **Phase 3: Dashboard Integration (1 day)**

**Add new tab: "Smart Recommendations"**

UI Flow:
```
┌─────────────────────────────────────────────┐
│  🎵 Smart Recommendation                    │
│                                             │
│  How are you feeling?                       │
│  ┌───────────────────────────────────────┐ │
│  │ I need songs for...                   │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  Quick presets:                             │
│  [😊 Happy] [😢 Sad] [💪 Workout]          │
│  [📚 Study] [💤 Relax] [🎉 Party]          │
│                                             │
│  ───────────────────────────────────────    │
│                                             │
│  Results (20 tracks):                       │
│  ✓ Based on your mood: "Workout"            │
│  ✓ High energy (0.7-1.0)                    │
│  ✓ Fast tempo (120-180 BPM)                 │
│                                             │
│  [Track list with play buttons...]          │
└─────────────────────────────────────────────┘
```

---

## 📊 **ML Models to Build**

### **Model 1: Intent Classifier**
- **Input:** User text query
- **Output:** Intent category (happy, sad, workout, etc.)
- **Algorithm:** Simple keyword matching → Can upgrade to Naive Bayes later
- **Accuracy Target:** 85%+
- **Training:** Use predefined patterns + validate with sample queries

### **Model 2: Recommendation Scorer**
- **Input:** Intent + Audio features
- **Output:** Relevance score (0-1)
- **Algorithm:** Weighted similarity (cosine similarity or euclidean distance)
- **Accuracy Target:** 80%+ user satisfaction
- **Training:** Use existing audio features + validate with listening tests

### **Model 3: Personalization (Optional - Future Work)**
- **Input:** User listening history
- **Output:** Personalized recommendations
- **Algorithm:** Collaborative filtering
- **Complexity:** High (can mention as "future improvement")

---

## 🎓 **Academic Justification**

### **Literature Support:**

1. **"Music Emotion Recognition" (MER)**
   - Established field in MIR (Music Information Retrieval)
   - Valence-Arousal model widely accepted
   - Spotify uses similar approach

2. **"Audio Features for Emotion"**
   - Valence correlates with happiness (Russell, 1980)
   - Energy/Arousal for intensity (Thayer, 1989)
   - Tempo affects perceived emotion (Gabrielsson, 2001)

3. **"Context-Aware Recommendation"**
   - Mood-based playlist generation (Schedl et al., 2018)
   - Situation-based music recommendation (Wang et al., 2012)

### **Research Questions (for thesis):**

1. **RQ1:** Can audio features accurately represent emotional intent?
2. **RQ2:** How effective is emotion-based recommendation vs. popularity-based?
3. **RQ3:** Does sweet spot tempo enhance recommendation quality?

### **Hypothesis:**
> "Emotion-based recommendations using audio features (valence, energy, tempo) provide higher user satisfaction than popularity-based recommendations, especially when combined with tempo sweet spot analysis."

---

## 🚀 **Implementation Timeline**

| Phase | Task | Days | Deliverable |
|-------|------|------|-------------|
| 1 | Intent classification | 2 | Intent mapper with 8-10 categories |
| 2 | Recommendation API | 2-3 | `/api/recommend` endpoint |
| 3 | Dashboard UI | 1 | "Smart Recommendations" tab |
| 4 | Testing & tuning | 1-2 | User feedback validation |
| 5 | Documentation | 1 | Algorithm explanation for thesis |
| **Total** | | **7-9 days** | **Working recommendation system** |

---

## 🎯 **Success Metrics**

1. **Response Time:** <200ms for recommendations
2. **Relevance:** 80%+ user satisfaction (survey after demo)
3. **Coverage:** Works for 8-10 different moods/contexts
4. **Accuracy:** Intent classifier 85%+ accuracy
5. **Demo-ability:** Live demo during presentation works smoothly

---

## 🆚 **Alternative Ideas (If You Don't Like Emotion-Based)**

### **Alt 1: Tempo-Based Recommendation**
**Concept:** "Find similar tempo songs"  
**Use Case:** "Songs like Shape of You (96 BPM)"  
**Complexity:** ⭐ (Very Easy)  
**Uniqueness:** ⭐⭐ (Low - too simple)

### **Alt 2: Audio Similarity Recommendation**
**Concept:** "Songs that sound similar"  
**Use Case:** "Find songs similar to Blinding Lights"  
**Complexity:** ⭐⭐⭐ (Moderate)  
**Uniqueness:** ⭐⭐⭐ (Medium - common approach)

### **Alt 3: Era-Based Time Travel**
**Concept:** "Discover hits from different decades with similar feel"  
**Use Case:** "80s songs with modern energy"  
**Complexity:** ⭐⭐ (Easy)  
**Uniqueness:** ⭐⭐⭐⭐ (Interesting angle)

### **Alt 4: Sweet Spot Evolution**
**Concept:** "How artists' tempo evolved over time"  
**Use Case:** "Track Ed Sheeran's tempo changes 2010-2020"  
**Complexity:** ⭐⭐ (Easy)  
**Uniqueness:** ⭐⭐⭐⭐⭐ (Very unique - ties to thesis theme)

---

## 💡 **My Recommendation**

**Go with: Emotion-Based Recommendation (Option 2)**

**Why:**
1. ✅ Realistic within thesis timeline
2. ✅ Academically defensible (backed by research)
3. ✅ Demo-able and impressive
4. ✅ Uses existing data (no external dependencies)
5. ✅ Novel enough to be interesting
6. ✅ Practical real-world application
7. ✅ Can integrate sweet spot analysis (bonus points!)

**Sweet Spot Integration:**
> "Recommendations in the 100-120 BPM sweet spot get a +10% relevance boost for dance/party moods, backed by our earlier analysis showing higher danceability in this range."

---

## 📝 **Next Steps**

1. **Decide on approach** (Emotion-based recommended)
2. **Define intents** (8-10 mood/context categories)
3. **Build intent classifier** (keyword matching)
4. **Create recommendation API** (SQL query with scoring)
5. **Add dashboard tab** (UI for user input)
6. **Test and validate** (manual testing + feedback)
7. **Document for thesis** (algorithm explanation)

---

**What do you think? Mau pakai emotion-based atau ada ide lain?** 🤔

Let me know and we can start building! 🚀
