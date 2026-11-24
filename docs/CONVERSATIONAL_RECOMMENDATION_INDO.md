# 🎵 Sistem Rekomendasi Lagu - Conversational (Bahasa Indonesia)

## 💡 **Prinsip Desain**

✅ **User-friendly** - Bahasa sehari-hari, bukan istilah teknis  
✅ **Natural** - Pertanyaan seperti ngobrol dengan teman  
✅ **Simple** - Maksimal 3 pertanyaan  
✅ **Visual** - Pakai emoji & gambar, bukan angka

---

## 🗣️ **Alur Percakapan**

### **Pertanyaan 1: Aktivitas / Mood**
```
┌─────────────────────────────────────────────────┐
│  🎵 Rekomendasi Lagu Pintar                     │
│                                                 │
│  Lagi pengen dengerin lagu buat apa nih?        │
│                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │    😊      │  │    💪      │  │    📚      ││
│  │  Senang-   │  │  Olahraga  │  │  Belajar/  ││
│  │  senang    │  │            │  │  Kerja     ││
│  └────────────┘  └────────────┘  └────────────┘│
│                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │    😢      │  │    💤      │  │    🎉      ││
│  │  Galau/    │  │  Santai/   │  │  Pesta/    ││
│  │  Sedih     │  │  Tidur     │  │  Nongkrong ││
│  └────────────┘  └────────────┘  └────────────┘│
│                                                 │
│  ┌────────────┐  ┌────────────┐                │
│  │    🚗      │  │    ❤️      │                │
│  │  Nyetir/   │  │  Romantis  │                │
│  │  Perjalanan│  │            │                │
│  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────┘
```

**Mapping ke Database:**
- **Senang-senang** → `valence > 0.6, energy > 0.6`
- **Olahraga** → `energy > 0.7, tempo 120-180`
- **Belajar/Kerja** → `energy < 0.4, instrumentalness > 0.5`
- **Galau/Sedih** → `valence < 0.4, energy < 0.4`
- **Santai/Tidur** → `energy < 0.3, acousticness > 0.6`
- **Pesta/Nongkrong** → `danceability > 0.7, energy > 0.7`
- **Nyetir/Perjalanan** → `energy 0.5-0.7, tempo 100-130`
- **Romantis** → `valence 0.5-0.8, acousticness > 0.4`

---

### **Pertanyaan 2: Detail Aktivitas**

#### **Kalau pilih: 💪 Olahraga**
```
┌─────────────────────────────────────────────────┐
│  Olahraga apa nih?                              │
│                                                 │
│  ┌────────────────┐  ┌────────────────┐        │
│  │  🏃 Lari/Cardio│  │  🏋️ Gym/Angkat │        │
│  │                │  │     Beban      │        │
│  │  Lagu cepat    │  │  Lagu semangat │        │
│  │  & energik     │  │  tapi stabil   │        │
│  └────────────────┘  └───────────���────┘        │
│                                                 │
│  ┌────────────────┐  ┌────────────────┐        │
│  │  🧘 Yoga/      │  │  🚴 Bersepeda  │        │
│  │     Peregangan │  │                │        │
│  │  Lagu tenang   │  │  Lagu sedang   │        │
│  │  & rileks      │  │  & menyenangkan│        │
│  └────────────────┘  └────────────────┘        │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Lari/Cardio** → `energy > 0.8, tempo 140-180` (cepat & energik)
- **Gym/Angkat Beban** → `energy 0.7-0.9, tempo 110-140` (kuat & stabil)
- **Yoga/Peregangan** → `energy 0.2-0.4, acousticness > 0.5, tempo 60-90` (tenang)
- **Bersepeda** → `energy 0.6-0.8, tempo 110-140` (sedang energik)

---

#### **Kalau pilih: 📚 Belajar/Kerja**
```
┌─────────────────────────────────────────────────┐
│  Butuh konsentrasi atau musik latar aja?        │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🎧 Fokus       │  │  🎵 Musik Latar │      │
│  │     Maksimal    │  │                 │      │
│  │                 │  │  Gak masalah    │      │
│  │  Tanpa lirik    │  │  ada lirik      │      │
│  │  (instrumental) │  │                 │      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐                            │
│  │  ☕ Santai       │                            │
│  │     Kerja       │                            │
│  │                 │                            │
│  │  Lagu enak      │                            │
│  │  & gak ganggu   │                            │
│  └─────────────────┘                            │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Fokus Maksimal** → `instrumentalness > 0.7, speechiness < 0.05, energy < 0.3` (pure instrumental)
- **Musik Latar** → `energy 0.3-0.5, speechiness < 0.2` (ada lirik tapi subtle)
- **Santai Kerja** → `acousticness > 0.5, energy 0.3-0.5` (enak didenger)

---

#### **Kalau pilih: 😊 Senang-senang**
```
┌─────────────────────────────────────────────────┐
│  Mau ngapain?                                   │
│                                                 │
│  ┌────────────────┐  ┌────────────────┐        │
│  │  💃 Joget/     │  │  🎤 Nyanyi     │        │
│  │     Goyang     │  │                │        │
│  │                │  │  Lagu yang     │        │
│  │  Lagu groovy   │  │  enak buat     │        │
│  │  & catchy      │  │  sing-along    │        │
│  └────────────────┘  └────────────────┘        │
│                                                 │
│  ┌────────────────┐  ┌────────────────┐        │
│  │  😌 Santai     │  │  🌞 Pagi       │        │
│  │     Aja        │  │     Cerah      │        │
│  │                │  │                │        │
│  │  Mood booster  │  │  Feel good     │        │
│  │                │  │  vibes         │        │
│  └────────────────┘  └────────────────┘        │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Joget/Goyang** → `danceability > 0.7, tempo 100-130` (groovy, sweet spot!)
- **Nyanyi** → `speechiness 0.1-0.3, valence > 0.7` (catchy lyrics)
- **Santai Aja** → `energy 0.5-0.7, valence > 0.6` (chill happy)
- **Pagi Cerah** → `valence > 0.7, energy 0.5-0.7` (feel good)

---

#### **Kalau pilih: 😢 Galau/Sedih**
```
┌─────────────────────────────────────────────────┐
│  Butuh curhat atau pengen pelan-pelan aja?      │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  😭 Nangis      │  │  🎹 Melow       │      │
│  │     Curhat      │  │     Merenung    │      │
│  │                 │  │                 │      │
│  │  Lagu sedih     │  │  Lagu pelan     │      │
│  │  yang relate    │  │  & menenangkan  │      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐                            │
│  │  🌧️ Hujan-      │                            │
│  │     hujan       │                            │
│  │                 │                            │
│  │  Lagu buat      │                            │
│  │  nemenin ujan   │                            │
│  └─────────────────┘                            │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Nangis Curhat** → `valence 0.1-0.3, energy 0.3-0.6` (emotional release)
- **Melow Merenung** → `valence 0.2-0.4, acousticness > 0.5, tempo 60-90` (calm sad)
- **Hujan-hujan** → `valence 0.3-0.5, energy 0.2-0.4, acousticness > 0.4` (rainy vibe)

---

#### **Kalau pilih: 💤 Santai/Tidur**
```
┌─────────────────────────────────────────────────┐
│  Mau santai atau beneran tidur?                 │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  😴 Tidur       │  │  🧘 Meditasi    │      │
│  │                 │  │                 │      │
│  │  Lagu super     │  │  Lagu untuk     │      │
│  │  pelan & tenang │  │  fokus &        │      │
│  │                 │  │  ketenangan     │      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  📖 Baca        │  │  ☕ Ngopi       │      │
│  │     Buku        │  │     Santai      │      │
│  │                 │  │                 │      │
│  │  Background     │  │  Lagu enak      │      │
│  │  musik lembut   │  │  & nyaman       │      │
│  └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Tidur** → `energy < 0.2, loudness < -20, tempo 40-70` (very calm)
- **Meditasi** → `instrumentalness > 0.7, energy 0.1-0.3, tempo 50-80` (zen)
- **Baca Buku** → `energy 0.2-0.4, acousticness > 0.5, speechiness < 0.05` (soft background)
- **Ngopi Santai** → `energy 0.3-0.5, valence 0.4-0.7` (comfortable)

---

#### **Kalau pilih: 🎉 Pesta/Nongkrong**
```
┌─────────────────────────────────────────────────┐
│  Suasananya gimana?                             │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🕺 Dance       │  │  🎊 Hype        │      │
│  │     Party       │  │     Party       │      │
│  │                 │  │                 │      │
│  │  Lagu buat      │  │  Lagu super     │      │
│  │  nge-dance      │  │  energik        │      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🍹 Santai      │  │  🎶 Pre-Party   │      │
│  │     Nongkrong   │  │     Warmup      │      │
│  │                 │  │                 │      │
│  │  Chill vibes    │  │  Build up       │      │
│  │  bareng temen   │  │  energy         │      │
│  └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Dance Party** → `danceability > 0.7, energy > 0.7, tempo 110-130` (sweet spot dance!)
- **Hype Party** → `energy > 0.8, valence > 0.7, tempo 120-140` (super energetic)
- **Santai Nongkrong** → `energy 0.5-0.7, valence > 0.6, tempo 90-120` (chill happy)
- **Pre-Party Warmup** → `energy 0.6-0.8, tempo 100-130` (gradual buildup)

---

#### **Kalau pilih: 🚗 Nyetir/Perjalanan**
```
┌─────────────────────────────────────────────────┐
│  Mau kemana?                                    │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🛣️ Jalan       │  │  🏙️ Macet      │      │
│  │     Tol         │  │     di Kota     │      │
│  │                 │  │                 │      │
│  │  Lagu enak      │  │  Lagu santai    │      │
│  │  buat cruise    │  │  biar gak stress│      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🌃 Malam       │  │  🏞️ Road       │      │
│  │     Hari        │  │     Trip        │      │
│  │                 │  │                 │      │
│  │  Mood chill     │  │  Lagu petualang │      │
│  │  & santai       │  │  & bebas        │      │
│  └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Jalan Tol** → `tempo 110-130, energy 0.5-0.7, valence 0.5-0.8` (cruise speed)
- **Macet di Kota** → `tempo 80-100, energy 0.4-0.6` (patience music)
- **Malam Hari** → `tempo 80-110, energy 0.3-0.6, valence 0.4-0.7` (night vibe)
- **Road Trip** → `tempo 100-130, energy 0.6-0.8, valence > 0.6` (adventure!)

---

#### **Kalau pilih: ❤️ Romantis**
```
┌─────────────────────────────────────────────────┐
│  Suasana romantis yang gimana?                  │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  🕯️ Intimate    │  │  💑 Kencan      │      │
│  │                 │  │                 │      │
│  │  Lagu lembut    │  │  Lagu manis     │      │
│  │  & personal     │  │  & menyenangkan │      │
│  └─────────────────┘  └─────────────────┘      │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  💃 Slow        │  │  💕 Love        │      │
│  │     Dance       │  │     Songs       │      │
│  │                 │  │                 │      │
│  │  Lagu untuk     │  │  Lagu cinta     │      │
│  │  dance berdua   │  │  klasik         │      │
│  └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Intimate** → `energy 0.2-0.5, acousticness > 0.5, valence 0.5-0.8` (soft & close)
- **Kencan** → `energy 0.4-0.6, valence 0.6-0.9, tempo 80-110` (sweet)
- **Slow Dance** → `danceability 0.6-0.9, tempo 60-90, valence 0.6-0.9` (romantic dance)
- **Love Songs** → `valence 0.6-0.9, acousticness > 0.3` (classic love)

---

### **Pertanyaan 3: Seberapa Intens? (Opsional)**

**Hanya muncul kalau perlu klarifikasi intensity**

```
┌─────────────────────────────────────────────────┐
│  Mau yang gimana?                               │
│                                                 │
│  Pilih intensitas musik:                        │
│                                                 │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐│
│  │ 😌     │  │ 🙂     │  │ 😄     │  │ 🤩     ││
│  │ Pelan  │  │ Santai │  │ Semangat│ │ Maksimal││
│  │ Banget │  │        │  │        │  │        ││
│  └────────┘  └────────┘  └────────┘  └────────┘│
│                                                 │
│  Atau:                                          │
│                                                 │
│  Lagu cepat atau pelan?                         │
│                                                 │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐│
│  │ 🐢     │  │ 🚶     │  │ 🏃     │  │ ⚡     ││
│  │ Pelan  │  │ Sedang │  │ Cepat  │  │ Super  ││
│  │        │  │        │  │        │  │ Cepat  ││
│  └────────┘  └────────┘  └────────┘  └────────┘│
└─────────────────────────────────────────────────┘
```

**Mapping:**
- **Pelan Banget** 😌 → `energy 0.0-0.3, tempo 50-80`
- **Santai** 🙂 → `energy 0.3-0.5, tempo 80-110`
- **Semangat** 😄 → `energy 0.5-0.7, tempo 110-140`
- **Maksimal** 🤩 → `energy 0.7-1.0, tempo 140-180`

---

## 🎯 **Hasil Rekomendasi**

```
┌─────────────────────────────────────────────────┐
│  🎵 Playlist Sempurna Untukmu!                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ✨ Berdasarkan pilihan kamu:                   │
│     • Olahraga - Lari/Cardio                    │
│     • Lagu cepat & energik                      │
│     • Intensitas: Maksimal 🤩                   │
│                                                 │
│  📊 Ditemukan 234 lagu | Menampilkan 20 teratas │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 1. ▶️ Blinding Lights                     │ │
│  │    The Weeknd • 2020                      │ │
│  │    🎵 Cepat & Energik | Perfect! ⭐       │ │
│  ├───────────────────────────────────────────┤ │
│  │ 2. ▶️ Don't Start Now                     │ │
│  │    Dua Lipa • 2019                        │ │
│  │    🎵 Groovy & Powerful | Great fit! ⭐   │ │
│  ├───────────────────────────────────────────┤ │
│  │ 3. ▶️ Levitating                          │ │
│  │    Dua Lipa • 2020                        │ │
│  │    🎵 Upbeat & Danceable | Sweet spot! ⭐ │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  [🔄 Ubah Preferensi]  [💾 Simpan Playlist]    │
└─────────────────────────────────────────────────┘
```

---

## 🎨 **Visual Indicators (Tanpa Istilah Teknis)**

**Jangan pakai:**
- ❌ "Valence: 0.7"
- ❌ "Energy: 0.8" 
- ❌ "Tempo: 120 BPM"
- ❌ "Danceability: 0.6"

**Pakai ini:**
- ✅ "Mood: Senang 😊"
- ✅ "Intensitas: Tinggi ⚡"
- ✅ "Kecepatan: Cepat 🏃"
- ✅ "Cocok buat: Nge-dance 💃"

**Deskripsi Natural:**
- "Lagu ini cepat & energik, cocok buat lari!"
- "Perfect buat fokus kerja, tenang & gak ganggu"
- "Groovy banget, bikin pengen joget!"
- "Lagu sedih yang relate banget"

---

## 💻 **Implementasi**

### **Mapping Configuration**

```javascript
const MOOD_MAPPINGS_INDO = {
  // 😊 Senang-senang
  'senang': {
    base: { valence: [0.6, 1.0], energy: [0.6, 1.0] },
    
    submenu: {
      'joget': { 
        filters: { danceability: [0.7, 1.0], tempo: [100, 130] },
        description: 'Lagu groovy & catchy buat goyang'
      },
      'nyanyi': { 
        filters: { speechiness: [0.1, 0.3], valence: [0.7, 1.0] },
        description: 'Lagu enak buat sing-along'
      },
      'santai': { 
        filters: { energy: [0.5, 0.7], valence: [0.6, 1.0] },
        description: 'Mood booster yang santai'
      },
      'pagi_cerah': { 
        filters: { valence: [0.7, 1.0], energy: [0.5, 0.7] },
        description: 'Feel good vibes buat pagi'
      }
    }
  },
  
  // 💪 Olahraga
  'olahraga': {
    submenu: {
      'lari_cardio': {
        filters: { energy: [0.8, 1.0], tempo: [140, 180] },
        description: 'Lagu cepat & energik buat lari'
      },
      'gym_beban': {
        filters: { energy: [0.7, 0.9], tempo: [110, 140] },
        description: 'Lagu semangat yang stabil'
      },
      'yoga': {
        filters: { energy: [0.2, 0.4], acousticness: [0.5, 1.0], tempo: [60, 90] },
        description: 'Lagu tenang & rileks'
      },
      'sepeda': {
        filters: { energy: [0.6, 0.8], tempo: [110, 140] },
        description: 'Lagu sedang & menyenangkan'
      }
    }
  },
  
  // 📚 Belajar/Kerja
  'belajar': {
    submenu: {
      'fokus_maksimal': {
        filters: { instrumentalness: [0.7, 1.0], speechiness: [0, 0.05], energy: [0, 0.3] },
        description: 'Tanpa lirik, full konsentrasi'
      },
      'musik_latar': {
        filters: { energy: [0.3, 0.5], speechiness: [0, 0.2] },
        description: 'Ada lirik tapi gak ganggu'
      },
      'santai_kerja': {
        filters: { acousticness: [0.5, 1.0], energy: [0.3, 0.5] },
        description: 'Lagu enak didenger'
      }
    }
  },
  
  // 😢 Galau/Sedih
  'galau': {
    base: { valence: [0, 0.4], energy: [0, 0.5] },
    
    submenu: {
      'nangis_curhat': {
        filters: { valence: [0.1, 0.3], energy: [0.3, 0.6] },
        description: 'Lagu sedih yang relate'
      },
      'melow_merenung': {
        filters: { valence: [0.2, 0.4], acousticness: [0.5, 1.0], tempo: [60, 90] },
        description: 'Lagu pelan & menenangkan'
      },
      'hujan': {
        filters: { valence: [0.3, 0.5], energy: [0.2, 0.4], acousticness: [0.4, 1.0] },
        description: 'Lagu buat nemenin ujan'
      }
    }
  },
  
  // 💤 Santai/Tidur
  'santai': {
    submenu: {
      'tidur': {
        filters: { energy: [0, 0.2], loudness: [-30, -15], tempo: [40, 70] },
        description: 'Super pelan & tenang'
      },
      'meditasi': {
        filters: { instrumentalness: [0.7, 1.0], energy: [0.1, 0.3], tempo: [50, 80] },
        description: 'Fokus & ketenangan'
      },
      'baca_buku': {
        filters: { energy: [0.2, 0.4], acousticness: [0.5, 1.0], speechiness: [0, 0.05] },
        description: 'Background musik lembut'
      },
      'ngopi': {
        filters: { energy: [0.3, 0.5], valence: [0.4, 0.7] },
        description: 'Lagu enak & nyaman'
      }
    }
  },
  
  // 🎉 Pesta/Nongkrong
  'pesta': {
    submenu: {
      'dance_party': {
        filters: { danceability: [0.7, 1.0], energy: [0.7, 1.0], tempo: [110, 130] },
        description: 'Lagu buat nge-dance'
      },
      'hype_party': {
        filters: { energy: [0.8, 1.0], valence: [0.7, 1.0], tempo: [120, 140] },
        description: 'Super energik & hype'
      },
      'santai_nongkrong': {
        filters: { energy: [0.5, 0.7], valence: [0.6, 1.0], tempo: [90, 120] },
        description: 'Chill vibes bareng temen'
      },
      'preparty': {
        filters: { energy: [0.6, 0.8], tempo: [100, 130] },
        description: 'Build up energy'
      }
    }
  },
  
  // 🚗 Nyetir/Perjalanan
  'nyetir': {
    submenu: {
      'jalan_tol': {
        filters: { tempo: [110, 130], energy: [0.5, 0.7], valence: [0.5, 0.8] },
        description: 'Enak buat cruise'
      },
      'macet': {
        filters: { tempo: [80, 100], energy: [0.4, 0.6] },
        description: 'Santai biar gak stress'
      },
      'malam': {
        filters: { tempo: [80, 110], energy: [0.3, 0.6], valence: [0.4, 0.7] },
        description: 'Mood chill & santai'
      },
      'roadtrip': {
        filters: { tempo: [100, 130], energy: [0.6, 0.8], valence: [0.6, 1.0] },
        description: 'Petualang & bebas'
      }
    }
  },
  
  // ❤️ Romantis
  'romantis': {
    submenu: {
      'intimate': {
        filters: { energy: [0.2, 0.5], acousticness: [0.5, 1.0], valence: [0.5, 0.8] },
        description: 'Lembut & personal'
      },
      'kencan': {
        filters: { energy: [0.4, 0.6], valence: [0.6, 0.9], tempo: [80, 110] },
        description: 'Manis & menyenangkan'
      },
      'slow_dance': {
        filters: { danceability: [0.6, 0.9], tempo: [60, 90], valence: [0.6, 0.9] },
        description: 'Dance berdua'
      },
      'love_songs': {
        filters: { valence: [0.6, 0.9], acousticness: [0.3, 1.0] },
        description: 'Lagu cinta klasik'
      }
    }
  }
};
```

---

## 🎓 **Keunggulan Approach Ini**

### **1. User Experience** ⭐⭐⭐⭐⭐
- Bahasa Indonesia natural
- Tanpa istilah teknis
- Emoji & visual aids
- Maksimal 3 klik untuk hasil

### **2. Demo Value** ⭐⭐⭐⭐⭐
- Dosen langsung paham
- Gak perlu penjelasan panjang
- Bisa live demo dengan mudah
- Impressive tapi gak overwhelming

### **3. Implementation** ⭐⭐⭐⭐⭐
- Simple rule-based
- No NLP training needed
- Fast development (3-4 hari)
- Easy to maintain

### **4. Academic Defense** ⭐⭐⭐⭐⭐
- Explainable AI
- Clear feature mapping
- User-centric design
- Backed by research (MER)

---

## 🚀 **Timeline: 4 Hari**

**Day 1:** UI components (8 mood cards + submenus)  
**Day 2:** Mapping logic + filter builder  
**Day 3:** API integration + results display  
**Day 4:** Testing + polish descriptions

---

**Gimana? Jauh lebih natural kan? 😊**

Mau langsung implement atau ada yang mau diubah lagi? 🎯
