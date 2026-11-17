# Dashboard Setup Guide

## **🚀 Quick Setup (5 Minutes)**

### **Step 1: Get Firebase Config**

1. **Go to Firebase Console:**
   ```
   https://console.firebase.google.com/
   ```

2. **Select your project:** `spotify-tempo-analysis`

3. **Click ⚙️ (Settings) → Project Settings**

4. **Scroll down to "Your apps"**

5. **Click "Web" (</> icon)**

6. **Register app:**
   - App nickname: `Tempo Dashboard`
   - ✅ Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"

7. **Copy the firebaseConfig object:**
   ```javascript
   const firebaseConfig = {
       apiKey: "AIza...",
       authDomain: "spotify-tempo-analysis.firebaseapp.com",
       projectId: "spotify-tempo-analysis",
       storageBucket: "spotify-tempo-analysis.appspot.com",
       messagingSenderId: "123456789",
       appId: "1:123456789:web:abc123"
   };
   ```

---

### **Step 2: Update app.js**

1. **Open:** `dashboard/app.js`

2. **Find this section (line 7-14):**
   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_API_KEY",
       authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
       projectId: "YOUR_PROJECT_ID",
       storageBucket: "YOUR_PROJECT_ID.appspot.com",
       messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
       appId: "YOUR_APP_ID"
   };
   ```

3. **Replace with your actual config** (from Step 1)

---

### **Step 3: Update Firestore Rules**

Dashboard needs READ access to Firestore.

1. **Go to:** Firebase Console → Firestore Database → Rules

2. **Replace rules with:**
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Allow read access to all collections
       match /{document=**} {
         allow read: if true;
         allow write: if false; // Only backend can write
       }
     }
   }
   ```

3. **Click "Publish"**

**⚠️ IMPORTANT:** These rules allow public read access. For production, add authentication!

---

### **Step 4: Run Dashboard**

**Option A: Live Server (Recommended)**

If using VS Code:
1. Install extension: "Live Server" by Ritwick Dey
2. Right-click `index.html` → "Open with Live Server"
3. Dashboard opens at `http://localhost:5500`

**Option B: Python HTTP Server**

```powershell
# Navigate to dashboard folder
cd "D:\Semester 5\BIG DATA\Project\dashboard"

# Start server
python -m http.server 8000

# Open browser: http://localhost:8000
```

**Option C: Direct File (May have CORS issues)**

Just double-click `index.html` (might not work due to Firebase security)

---

## **✅ Expected Result**

Dashboard should show:
- ✅ Total Tracks: 1.20M
- ✅ Avg Tempo: 117.63 BPM
- ✅ Sweet Spot %: 22.18%
- ✅ Danceability Boost: +13.4%
- ✅ 3 interactive charts
- ✅ Top 10 tracks table

---

## **🔥 Deploy to Firebase Hosting (Optional)**

Want to host online for FREE?

```powershell
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize hosting
cd "D:\Semester 5\BIG DATA\Project\dashboard"
firebase init hosting

# Select:
# - Use existing project: spotify-tempo-analysis
# - Public directory: . (current folder)
# - Configure as SPA: No
# - Set up GitHub actions: No
# - Overwrite index.html: No

# Deploy!
firebase deploy --only hosting

# Your dashboard will be live at:
# https://spotify-tempo-analysis.web.app
```

---

## **🐛 Troubleshooting**

### **Problem: Dashboard blank / no data**

**Check:**
1. Open browser console (F12)
2. Look for error messages
3. Common issues:
   - Firebase config incorrect → Update `app.js`
   - Firestore rules too restrictive → Update rules
   - CORS error → Use Live Server, not direct file

### **Problem: "Permission denied" error**

**Fix:** Update Firestore rules (Step 3 above)

### **Problem: Charts not rendering**

**Check:**
1. Data loaded? (Check console for "✅ Dashboard data loaded")
2. Chart.js loaded? (Check Network tab in DevTools)
3. Canvas elements exist? (Inspect HTML)

---

## **📝 Customization**

### **Change Colors:**

Edit `index.html` CSS:
```css
/* Line 31: Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Line 121: Card accent color */
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
```

### **Add More Charts:**

1. Add canvas in HTML:
   ```html
   <canvas id="myNewChart"></canvas>
   ```

2. Create chart in `app.js`:
   ```javascript
   const ctx = document.getElementById('myNewChart').getContext('2d');
   new Chart(ctx, { ... });
   ```

---

## **🎯 Next Steps**

After dashboard works:

1. **Add Authentication** (optional):
   ```javascript
   // In app.js
   firebase.auth().signInAnonymously();
   ```

2. **Add Real-time Updates:**
   ```javascript
   db.collection('summary').doc('global_stats')
     .onSnapshot(doc => {
       updateSummaryCards(doc.data());
     });
   ```

3. **Add Filters:**
   - Filter by decade
   - Filter by tempo range
   - Search tracks

4. **Export Features:**
   - Download charts as PNG
   - Export table to CSV

---

## **📚 Resources**

- [Chart.js Docs](https://www.chartjs.org/docs/latest/)
- [Firebase Web SDK](https://firebase.google.com/docs/web/setup)
- [Firestore Queries](https://firebase.google.com/docs/firestore/query-data/get-data)

---

**Need help? Check console errors first, then debug step by step!** 🔍
