# 🧪 Test Sections - Debug Guide

## Problem
Tempo Zones, Top Tracks, dan Methodology sections masih kosong/tidak muncul saat tab di-klik.

## Quick Test (Browser Console)

1. **Open dashboard:** `http://localhost:8000/index.html`

2. **Open browser console:** Press `F12` → Go to "Console" tab

3. **Run this test:**
```javascript
// List all sections status
debugListSections();
```

Expected output:
```
📋 Section Status:
  overviewSection: VISIBLE (display: default)
  summaryCardsSection: VISIBLE (display: default)
  mainContentSection: VISIBLE (display: default)
  mlPredictionsSection: HIDDEN (display: none)
  topTracksSection: HIDDEN (display: none)
  tempoZonesSection: HIDDEN (display: none)
  methodologySection: HIDDEN (display: none)
```

4. **Test showing a section manually:**
```javascript
// Show Top Tracks section
debugShowSection('topTracksSection');
```

If you see "✅ Showed: topTracksSection" and content appears → JavaScript works, navigation handler issue.

If you see "❌ Section not found" → HTML structure issue.

5. **Test navigation:**
```javascript
// Test clicking Top Tracks tab
testNavigation('top-tracks');
```

This simulates clicking the "Top Tracks" tab.

---

## Test Each Section

### Test Top Tracks:
```javascript
const elem = document.getElementById('topTracksSection');
console.log('Found:', elem !== null);
elem.classList.remove('hidden');
elem.style.display = 'block';
```

Should show the Top Tracks table with filters.

### Test Tempo Zones:
```javascript
const elem = document.getElementById('tempoZonesSection');
console.log('Found:', elem !== null);
elem.classList.remove('hidden');
elem.style.display = 'block';
```

Should show 5 tempo zone cards.

### Test Methodology:
```javascript
const elem = document.getElementById('methodologySection');
console.log('Found:', elem !== null);
elem.classList.remove('hidden');
elem.style.display = 'block';
```

Should show methodology documentation.

---

## Manual Click Test

1. Open dashboard
2. Click "Top Tracks" tab in navigation
3. Open console (F12)
4. Look for logs:
   - "🔄 Switching to: top-tracks"
   - "  Showing sections: ['topTracksSection']"
   - "  ✅ Showed: topTracksSection"
   - "✅ Switched to: top-tracks"

If you DON'T see these logs → Navigation handler not running.

If you see "⚠️ Section not found: topTracksSection" → HTML ID mismatch.

---

## Common Issues & Fixes

### Issue 1: Section not found
**Symptom:** Console shows "❌ Section not found"

**Fix:**
```javascript
// Check if section exists in HTML
document.querySelectorAll('[id*="Section"]').forEach(el => {
  console.log('Found section:', el.id);
});
```

### Issue 2: Section found but not showing
**Symptom:** debugShowSection() says "✅ Showed" but nothing appears

**Possible causes:**
- CSS `display: none !important` override
- Z-index issue (behind other elements)
- Content is empty

**Fix:**
```javascript
const elem = document.getElementById('topTracksSection');
console.log('Computed style:', window.getComputedStyle(elem).display);
console.log('Has content:', elem.innerHTML.length > 0);
console.log('Z-index:', window.getComputedStyle(elem).zIndex);
```

### Issue 3: Navigation not working
**Symptom:** Clicking tabs does nothing

**Fix:**
```javascript
// Check if event listeners attached
const links = document.querySelectorAll('[data-path]');
console.log('Navigation links found:', links.length);
links.forEach(link => {
  console.log('  -', link.getAttribute('data-path'));
});
```

### Issue 4: DOMContentLoaded not fired
**Symptom:** No console logs at all

**Fix:**
```javascript
// Check if navigation handler initialized
if (window.showSections) {
  console.log('✅ Navigation handler loaded');
} else {
  console.log('❌ Navigation handler NOT loaded');
}
```

---

## Force Show All Sections (Nuclear Option)

If nothing works, force show everything:

```javascript
['topTracksSection', 'tempoZonesSection', 'methodologySection'].forEach(id => {
  const elem = document.getElementById(id);
  if (elem) {
    elem.classList.remove('hidden');
    elem.style.display = 'block';
    elem.style.visibility = 'visible';
    elem.style.opacity = '1';
    console.log('✅ Force showed:', id);
  }
});
```

---

## Check Data Loading

Sections might be hidden because data loading fails:

### Check Top Tracks data:
```javascript
console.log('Top tracks loaded:', window.topTracksData?.length || 0);
if (window.loadTopTracksData) {
  loadTopTracksData();
}
```

### Check Tempo Zones data:
```javascript
if (window.loadTempoZonesData) {
  loadTempoZonesData();
}
```

---

## Verify HTML Structure

Check if sections are in correct place:

```javascript
const main = document.querySelector('main');
const sections = main.querySelectorAll('section[id$="Section"]');
console.log('Sections in <main>:', sections.length);
sections.forEach(s => console.log('  -', s.id));
```

Expected: 7 sections (overview, summary, mainContent, mlPredictions, topTracks, tempoZones, methodology)

---

## Success Criteria

✅ `debugListSections()` shows all 7 sections
✅ `debugShowSection('topTracksSection')` makes content appear
✅ Clicking "Top Tracks" tab switches view
✅ Top Tracks table shows with data
✅ Tempo Zones shows 5 cards
✅ Methodology shows documentation

---

## Report Back

After running tests, report:
1. Which sections are found? (all 7 or missing some?)
2. Can you manually show sections with debugShowSection()?
3. Do navigation links exist? (check with querySelectorAll('[data-path]'))
4. Any console errors?

This will help identify exact issue!
