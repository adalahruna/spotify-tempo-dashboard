# 🎵 Cara Test Sistem Rekomendasi

## ✅ **Implementation Complete!**

Sistem rekomendasi conversational sudah diimplementasi dengan:
- ✅ 8 mood categories (Senang, Olahraga, Belajar, Galau, Santai, Pesta, Nyetir, Romantis)
- ✅ 32 sub-activities dengan filter berbeda
- ✅ Smart scoring algorithm
- ✅ Bahasa Indonesia 100%
- ✅ No technical terms!

---

## 🚀 **Cara Menjalankan:**

### **Step 1: Start Backend API**

```powershell
cd "d:\Semester 5\BIG DATA\Project"
python api/search_api.py
```

**Expected output:**
```
✅ ML Prediction endpoints loaded
✅ Recommendation endpoints loaded  ← NEW!
...
Starting server on http://localhost:5000
```

### **Step 2: Start Dashboard Server**

```powershell
cd "d:\Semester 5\BIG DATA\Project\dashboard"
python -m http.server 8000
```

### **Step 3: Open Dashboard**

**Main Dashboard:**  
**http://localhost:8000**

Lalu klik tab **"Smart Recommendations"** (ada badge "NEW") atau  
**http://localhost:8000/recommend.html** (standalone version)

---

## 🧪 **Test Scenarios:**

### **Scenario 1: Workout (Lari/Cardio - Maksimal)**

1. **Step 1:** Pilih mood: **💪 Olahraga**
2. **Step 2:** Pilih activity: **🏃 Lari/Cardio** - "Lagu cepat & energik buat lari"
3. **Step 3:** Pilih intensity: **🤩 Maksimal** - "Full power!"
4. Click: **Cari Lagu! 🎵**

**Expected Results:**
- ~200+ tracks found
- Tempo: 168-216 BPM (super cepat!) 
- Energy: >0.9 (sangat energik)
- Tracks like: "Blinding Lights", "Don't Start Now"

---

### **Scenario 2: Study (Fokus Maksimal - Pelan)**

1. **Step 1:** Pilih mood: **📚 Belajar/Kerja**
2. **Step 2:** Pilih activity: **🎧 Fokus Maksimal** - "Tanpa lirik, full konsentrasi"
3. **Step 3:** Pilih intensity: **😌 Pelan Banget** - "Santai & tenang"
4. Click: **Cari Lagu! 🎵**

**Expected Results:**
- Instrumental tracks only
- Energy: <0.2 (super tenang)
- Tempo: 60-85 BPM (pelan)
- Perfect for deep focus!

---

### **Scenario 3: Party (Dance - Semangat)**

1. **Step 1:** Pilih mood: **🎉 Pesta/Nongkrong**
2. **Step 2:** Pilih activity: **🕺 Dance Party** - "Lagu buat nge-dance"
3. **Step 3:** Pilih intensity: **😄 Semangat** - "Bikin excited"
4. Click: **Cari Lagu! 🎵**

**Expected Results:**
- Danceability: 0.7-1.0 (groovy)
- Energy: 0.8-1.0 (tinggi)
- Tempo: 121-143 BPM (upbeat, still near sweet spot!)
- Perfect dance tracks

---

### **Scenario 4: Galau (Melow - Sedang)**

1. **Step 1:** Pilih mood: **😢 Galau/Sedih**
2. **Step 2:** Pilih activity: **🎹 Melow Merenung** - "Lagu pelan & menenangkan"
3. **Step 3:** Pilih intensity: **🙂 Sedang** - "Enak didenger"
4. Click: **Cari Lagu! 🎵**

**Expected Results:**
- Valence: 0.2-0.4 (sad)
- Acousticness: >0.5 (acoustic)
- Tempo: 60-90 BPM (slow)
- Energy: moderate
- Sad, emotional but not too heavy

---

### **Scenario 5: Romantic (Intimate - Pelan)**

1. **Step 1:** Pilih mood: **❤️ Romantis**
2. **Step 2:** Pilih activity: **🕯️ Intimate** - "Lembut & personal"
3. **Step 3:** Pilih intensity: **😌 Pelan Banget** - "Santai & tenang"
4. Click: **Cari Lagu! 🎵**

**Expected Results:**
- Energy: 0.14-0.35 (very low)
- Acousticness: 0.5-1.0 (acoustic)
- Valence: 0.5-0.8 (romantic)
- Tempo: slower than base
- Perfect intimate moments

---

## 🎨 **UI Features:**

### **Step Indicator:**
- ● Step 1 → ○ Step 2 → ○ Step 3
- Changes to ✓ when completed
- **3 steps total** for better refinement!

### **Step 1: Mood Selection**
- 8 mood cards with emoji
- Gradient purple background
- Hover effect (lift up)
- Selected state (green border)

### **Step 2: Activity Selection**
- Mood-specific activities (3-4 per mood)
- Label + Description
- Natural language descriptions
- No technical terms!

### **Step 3: Intensity Selection** ⭐ **NEW!**
- 4 intensity levels:
  - 😌 **Pelan Banget** - Santai & tenang
  - 🙂 **Sedang** - Enak didenger (default)
  - 😄 **Semangat** - Bikin excited
  - 🤩 **Maksimal** - Full power!
- Adjusts energy & tempo multipliers
- Fine-tunes recommendations

### **Results Display:**
- Track ranking (1-20)
- Match score percentage
- Natural descriptions ("Cepat & Energik")
- Year, artist info
- BPM badge
- Intensity shown in summary

---

## 🔧 **API Endpoints:**

### **1. Get Available Moods**
```
GET http://localhost:5000/api/moods
```

**Response:**
```json
{
  "success": true,
  "moods": [
    {
      "id": "olahraga",
      "emoji": "💪",
      "label": "Olahraga",
      "activities": [
        {
          "id": "lari_cardio",
          "description": "Lagu cepat & energik buat lari"
        }
      ]
    }
  ]
}
```

### **2. Get Recommendations**
```
POST http://localhost:5000/api/recommend
Content-Type: application/json

{
  "mood": "olahraga",
  "activity": "lari_cardio",
  "intensity": "maximum",
  "limit": 20
}
```

**Response:**
```json
{
  "success": true,
  "mood": "olahraga",
  "activity": "lari_cardio",
  "intensity": "maximum",
  "description": "Lagu cepat & energik buat lari",
  "filters_applied": {
    "energy": [0.9, 1.0],
    "tempo": [168, 216]
  },
  "count": 234,
  "results": [
    {
      "id": "...",
      "name": "Blinding Lights",
      "artists": "The Weeknd",
      "year": 2020,
      "tempo": 171,
      "energy": 0.73,
      "match_score": 0.92,
      "match_description": "Super cepat & Energik"
    }
  ]
}
```

---

## 🧪 **Test with cURL:**

### **Test 1: Get Moods**
```powershell
curl http://localhost:5000/api/moods
```

### **Test 2: Get Workout Recommendations (Maximum Intensity)**
```powershell
curl -X POST http://localhost:5000/api/recommend `
  -H "Content-Type: application/json" `
  -d '{\"mood\":\"olahraga\",\"activity\":\"lari_cardio\",\"intensity\":\"maximum\",\"limit\":10}'
```

### **Test 3: Get Study Recommendations (Calm)**
```powershell
curl -X POST http://localhost:5000/api/recommend `
  -H "Content-Type: application/json" `
  -d '{\"mood\":\"belajar\",\"activity\":\"fokus_maksimal\",\"intensity\":\"calm\",\"limit\":10}'
```

---

## 📊 **Available Combinations:**

### **8 Moods × 32 Activities = Comprehensive Coverage!**

| Mood | Activities |
|------|-----------|
| 😊 Senang | Joget, Nyanyi, Santai, Pagi Cerah |
| 💪 Olahraga | Lari, Gym, Yoga, Sepeda |
| 📚 Belajar | Fokus Maksimal, Musik Latar, Santai Kerja |
| 😢 Galau | Nangis Curhat, Melow Merenung, Hujan-hujan |
| 💤 Santai | Tidur, Meditasi, Baca Buku, Ngopi |
| 🎉 Pesta | Dance Party, Hype Party, Santai Nongkrong, Pre-Party |
| 🚗 Nyetir | Jalan Tol, Macet, Malam Hari, Road Trip |
| ❤️ Romantis | Intimate, Kencan, Slow Dance, Love Songs |

---

## ⚠️ **Troubleshooting:**

### **Problem: "Gagal memuat data"**

**Solution:**
1. Check Flask API running: http://localhost:5000/api/moods
2. Should see JSON response with moods list
3. Check CORS enabled in `search_api.py`

### **Problem: "Gagal mendapatkan rekomendasi"**

**Solution:**
1. Test API directly:
```powershell
curl -X POST http://localhost:5000/api/recommend `
  -H "Content-Type: application/json" `
  -d '{\"mood\":\"senang\",\"activity\":\"joget\",\"limit\":5}'
```
2. Check database connection
3. Check error in Flask terminal

### **Problem: "No tracks found"**

**Solution:**
- Some filter combinations might have fewer tracks
- Try different activity
- Check database has data: `SELECT COUNT(*) FROM spotify_tracks_raw;`

---

## 🎓 **For Presentation:**

### **Demo Script (2 minutes):**

**Opening:**
> "Sistem rekomendasi ini berbeda dari yang lain. Tidak perlu tahu istilah teknis seperti BPM atau valence. Cukup jawab pertanyaan sederhana."

**Demo Step 1:**
> "Misalnya saya mau olahraga. Klik 'Olahraga'."

**Demo Step 2:**
> "Lari atau gym? Saya pilih 'Lari/Cardio - Lagu cepat & energik'."

**Demo Step 3:** ⭐ **NEW!**
> "Seberapa intens? Saya mau maksimal - full power!"

**Show Results:**
> "Sistem langsung filter dari 1.2 juta tracks dengan intensity adjustment. Base tempo 140-180 BPM, dikali 1.2x jadi 168-216 BPM. Energy dikali 1.3x. Result: 234 lagu yang match. Top recommendation: Blinding Lights - 92% match score."

**Explain Algorithm:**
> "Di belakang layar, sistem map 'Lari/Cardio' ke audio features: energy 0.8-1.0, tempo 140-180 BPM. Lalu scoring dengan weighted algorithm: 25% energy match, 25% tempo match, dll."

**Academic Value:**
> "Ini explainable AI. Setiap rekomendasi bisa dijelaskan kenapa match. Tidak black box."

---

## ✅ **Success Criteria:**

After testing, verify:
- [ ] All 8 moods clickable
- [ ] Each mood shows 3-4 activities
- [ ] "Lanjut" button works (step 1→2)
- [ ] "Lanjut" button works (step 2→3) ⭐ **NEW!**
- [ ] 4 intensity levels visible
- [ ] "Kembali" buttons work on all steps
- [ ] Recommendations load (<2 seconds)
- [ ] Results show 20 tracks
- [ ] Match scores displayed
- [ ] Natural descriptions visible
- [ ] Intensity shown in summary
- [ ] No technical jargon
- [ ] Responsive UI
- [ ] **3-step flow feels smooth**

---

## 🚀 **Next Steps (Optional Improvements):**

### **Phase 2 Enhancements:**
1. Add intensity slider (Pelan/Sedang/Cepat/Maksimal)
2. Save playlist feature
3. Export to Spotify
4. Add preview audio (if available)
5. Filter by decade
6. Share playlist link

### **For Thesis:**
1. Document algorithm explanation
2. Create flow diagram
3. User testing & feedback
4. Compare with baseline (popularity-based)
5. Measure user satisfaction

---

**Files Created:**
- ✅ `api/recommendation_api.py` - Backend logic
- ✅ `api/search_api.py` - Updated with blueprint
- ✅ `dashboard/recommend.html` - Frontend UI

**Ready to test!** 🎉

Open: http://localhost:8000/recommend.html
