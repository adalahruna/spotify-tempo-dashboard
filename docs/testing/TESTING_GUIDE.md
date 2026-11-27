# 🧪 Testing Guide - ML Predictions Integration

## ✅ Testing Checklist

### 1. **Start Servers** ⚡

Open 2 terminals:

**Terminal 1 - Flask API (port 5000):**
```powershell
cd "d:\Semester 5\BIG DATA\Project"
python api/search_api.py
```
Wait for: `Running on http://127.0.0.1:5000`

**Terminal 2 - Dashboard (port 8000):**
```powershell
cd "d:\Semester 5\BIG DATA\Project\dashboard"
python -m http.server 8000
```
Wait for: `Serving HTTP on :: port 8000`

---

### 2. **Test Dashboard** 🎨

1. **Open Browser:**
   - URL: `http://localhost:8000/index.html`
   - Should see: Green & White Stitch design dashboard

2. **Check Navigation Tabs:**
   - Top navigation should show:
     - ✅ Overview (active by default)
     - ✅ Search & Query
     - ✅ **ML Predictions** (with green "AI" badge) ⭐
     - ✅ Tempo Zones
     - ✅ Top Tracks
     - ✅ Methodology

3. **Click ML Predictions Tab:**
   - Tab should activate (turn green)
   - New section should appear below summary cards
   - Should see:
     - Title: "ML Predictions" with AI badge
     - Subtitle: "4 trained models analyzing 100K tracks • 93% accuracy"
     - Status badge: "Models Ready" with pulse animation
     - Embedded prediction interface (iframe)
     - 4 model performance cards at bottom

---

### 3. **Test ML Predictions Interface** 🤖

Inside the ML Predictions section:

1. **Check Sliders:**
   - Should see 14 sliders for audio features:
     - Tempo (BPM): 0-200
     - Energy: 0-1
     - Danceability: 0-1
     - Valence: 0-1
     - Acousticness: 0-1
     - Instrumentalness: 0-1
     - Liveness: 0-1
     - Speechiness: 0-1
     - Loudness: -60 to 0 dB
     - Duration: 0-600 seconds
     - Year: 1920-2023
     - Key: 0-11
     - Mode: 0-1
     - Time Signature: 3-7

2. **Set Test Values:**
   - Tempo: 120
   - Energy: 0.8
   - Danceability: 0.75
   - Valence: 0.6
   - Acousticness: 0.1
   - (Leave others at default)

3. **Click "Predict All" Button:**
   - Button should turn green briefly
   - Results should appear within 1-2 seconds

4. **Check Results:**
   - **Popularity Card:**
     - Score: Should be 70-80 (good score)
     - Progress bar should show
     - Interpretation: "Popular Track - Strong Performance"
   
   - **Hit Classification Card:**
     - Result: "HIT" or "FLOP"
     - Probability percentage
     - Confidence indicator (High/Medium/Low)
   
   - **Danceability Card:**
     - Score: 0.7-0.8 range
     - Percentage display

5. **Test Different Presets:**
   - Click preset buttons ("High Energy", "Chill Vibes", etc.)
   - Values should change automatically
   - Results should update

---

### 4. **Test API Directly** 🔌

Open new terminal or PowerShell:

```powershell
# Test 1: Predict All Endpoint
$body = '{"tempo":120,"energy":0.8,"danceability":0.75,"valence":0.6,"acousticness":0.1,"instrumentalness":0.0,"liveness":0.15,"speechiness":0.05,"loudness":-5,"duration_ms":200000,"year":2023,"key":5,"mode":1,"time_signature":4}'

Invoke-RestMethod -Uri "http://localhost:5000/api/predict/all" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "success": true,
  "input": { ... },
  "predictions": {
    "popularity": {
      "score": 74.46,
      "interpretation": "Popular Track - Strong Performance"
    },
    "hit_classification": {
      "is_hit": true,
      "probability": 1.0,
      "confidence": 1.0
    }
  }
}
```

---

### 5. **Test Navigation** 🧭

1. **Click each tab** and verify:
   - Overview: Shows stats and charts
   - Search & Query: Search interface appears
   - ML Predictions: ML section appears
   - Other tabs: Hide ML section

2. **Check sidebar navigation:**
   - Should also have ML Predictions link with AI badge
   - Clicking sidebar link should work same as top nav

3. **Mobile responsiveness:**
   - Resize browser window to mobile size
   - Navigation should adapt
   - ML Predictions iframe should be responsive

---

### 6. **Check Model Files** 📁

Verify all model files exist:

```powershell
Get-ChildItem "d:\Semester 5\BIG DATA\Project\models"
```

**Should see 8 files:**
- ✅ `popularity_predictor.pkl` (largest)
- ✅ `hit_classifier.pkl`
- ✅ `danceability_predictor.pkl`
- ✅ `tempo_optimizer.pkl`
- ✅ `feature_scaler.pkl`
- ✅ `danceability_scaler.pkl`
- ✅ `tempo_scaler.pkl`
- ✅ `models_metadata.json`

---

### 7. **Performance Metrics Display** 📊

At bottom of ML Predictions section, verify 4 cards show:

| Card | Metric | Expected Value |
|------|--------|----------------|
| Popularity Predictor | R² | 93.1% |
| Hit Classifier | Acc | 92.9% |
| Danceability | R² | 66.7% |
| Tempo Optimizer | R² | 19.4% |

---

## 🐛 Troubleshooting

### Issue: "ML Predictions tab doesn't show"
- **Solution:** Check browser console (F12) for JavaScript errors
- Verify `app.js` loaded correctly
- Hard refresh: Ctrl+Shift+R

### Issue: "Iframe shows 404"
- **Solution:** Check `predict.html` is in dashboard folder
- Verify path in iframe src: `src="predict.html"`

### Issue: "API predictions fail"
- **Solution:** 
  - Check Flask API is running on port 5000
  - Check CORS is enabled in `search_api.py`
  - Verify models loaded: Check Flask console for "Models loaded successfully"

### Issue: "Sliders don't update"
- **Solution:**
  - Check `predict.html` JavaScript is working
  - Open browser console, look for errors
  - Verify API connection

### Issue: "Navigation doesn't switch tabs"
- **Solution:**
  - Check `app.js` navigation handler initialized
  - Look for console log: "🎯 Navigation handler initialized"
  - Verify `data-path` attributes on nav links

---

## ✅ Success Criteria

Your integration is successful if:

1. ✅ Both servers start without errors
2. ✅ Dashboard loads with green design
3. ✅ ML Predictions tab visible with AI badge
4. ✅ Clicking tab shows ML section
5. ✅ All 14 sliders work
6. ✅ "Predict All" returns results
7. ✅ Results display correctly in cards
8. ✅ Model metrics show at bottom
9. ✅ No console errors (check F12)
10. ✅ API test returns JSON successfully

---

## 📸 Visual Checklist

When you test, you should see:

**Main Dashboard:**
- ✅ Green header with "Spotify Tempo Analytics"
- ✅ Navigation tabs with ML Predictions (AI badge)
- ✅ 4 summary metric cards
- ✅ Clean white background

**ML Predictions Section (when tab clicked):**
- ✅ Gradient background (light green/white)
- ✅ Brain icon with "ML Predictions" title
- ✅ "Models Ready" badge with pulse animation
- ✅ Embedded prediction interface (iframe)
- ✅ 4 performance metric cards
- ✅ All cards have green primary color accents

**Prediction Interface (inside iframe):**
- ✅ 14 labeled sliders with current values
- ✅ Preset buttons above sliders
- ✅ "Predict All" green button
- ✅ 3 result cards (Popularity, Hit, Danceability)
- ✅ Progress bars and percentage displays

---

## 🎉 Final Test

**Complete User Flow:**

1. Open `http://localhost:8000/index.html`
2. Wait for dashboard to load
3. Click "ML Predictions" tab
4. Adjust Tempo to 120
5. Adjust Energy to 0.8
6. Adjust Danceability to 0.75
7. Click "Predict All"
8. See results appear:
   - Popularity: ~74/100
   - Hit: YES (100% probability)
   - Danceability: ~0.78

**If all this works → Integration is PERFECT! 🎊**

---

## 📞 Need Help?

Check logs in:
- Flask API terminal (port 5000)
- Browser console (F12 → Console tab)
- Network tab (F12 → Network) for API calls

Common fixes:
- Restart both servers
- Clear browser cache (Ctrl+Shift+Del)
- Check firewall/antivirus not blocking ports
