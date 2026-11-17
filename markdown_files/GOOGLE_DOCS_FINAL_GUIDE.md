# 📄 PANDUAN FINALISASI PROPOSAL DI GOOGLE DOCS

## ✅ STATUS: Proposal UNESA_2 Siap untuk Google Docs

File yang dipilih: **`PROPOSAL_TUGAS_AKHIR_UNESA_2.md`**

### ✨ Keunggulan Versi Ini:
1. ✅ **Tidak ada HTML tags** (tidak perlu cleanup manual)
2. ✅ **Formula LaTeX** ($...$ dan $$...$$) siap konversi otomatis
3. ✅ **Bahasa natural** (bilingual Indonesia-Inggris seimbang)
4. ✅ **Konten lengkap** (BAB I-III, Daftar Pustaka, Lampiran 1-5)
5. ✅ **30+ halaman** konten substansial

---

## 📋 LANGKAH IMPORT KE GOOGLE DOCS

### Metode 1: Import Langsung (Recommended)
1. Buka Google Drive
2. Klik kanan → **New** → **Google Docs** → **Blank document**
3. Di Google Docs, klik **File** → **Import**
4. Upload file `PROPOSAL_TUGAS_AKHIR_UNESA_2.md`
5. Google Docs akan otomatis convert Markdown ke Doc format

### Metode 2: Copy-Paste
1. Buka `PROPOSAL_TUGAS_AKHIR_UNESA_2.md` di VS Code/Notepad
2. Select All (Ctrl+A), Copy (Ctrl+C)
3. Paste di Google Docs baru
4. Formula LaTeX akan muncul sebagai plain text (butuh konversi manual)

### Metode 3: Via Pandoc (Advanced)
```powershell
# Install Pandoc dulu jika belum ada
pandoc PROPOSAL_TUGAS_AKHIR_UNESA_2.md -o PROPOSAL_UNESA.docx
# Upload .docx ke Google Drive, open with Google Docs
```

---

## 🎨 FORMATTING SESUAI PEDOMAN UNESA

### 1. **Paper Size & Margins**
- **File → Page setup**
  - Paper size: **Custom** → Width: 14.8 cm, Height: 21 cm (A5)
  - Margins:
    - Left: **2.5 cm**
    - Right: **2 cm**
    - Top: **2.5 cm**
    - Bottom: **2 cm**

### 2. **Font & Line Spacing**
- Select All (Ctrl+A)
- Font: **Book Antiqua**
- Size: **10 pt**
- Line spacing: **1.15**

### 3. **Heading Styles**
| Level | Style | Size | Bold |
|-------|-------|------|------|
| BAB I (H1) | Book Antiqua | 12 pt | ✅ Bold, Centered |
| A. Latar Belakang (H2) | Book Antiqua | 11 pt | ✅ Bold |
| 1. Sub-section (H3) | Book Antiqua | 10 pt | ✅ Bold |

**Cara Apply:**
1. Highlight "BAB I"
2. Klik **Format** → **Paragraph styles** → **Heading 1**
3. Modify: Font Book Antiqua 12pt, Bold, Center align
4. Ulangi untuk H2, H3

### 4. **Page Numbers**
- **Insert → Page numbers**
- Position: Bottom center
- Halaman awal (cover, daftar isi): **Romawi** (i, ii, iii)
- BAB I dst: **Arabic** (1, 2, 3)

**Cara membuat numbering berbeda:**
1. Letakkan cursor di akhir halaman cover
2. **Insert → Break → Section break (Next page)**
3. Pada bagian romawi: Format page number → Romawi
4. Pada BAB I: Format page number → Arabic, start at 1

### 5. **Table of Contents (Daftar Isi)**
- Letakkan cursor di halaman Daftar Isi
- **Insert → Table of contents**
- Pilih style dengan page numbers
- Setiap kali update heading, klik TOC → klik **Update**

---

## ✏️ PLACEHOLDER YANG HARUS DIISI

Cari dan ganti placeholder berikut:

| Placeholder | Ganti dengan |
|-------------|--------------|
| `Person` (nama) | Nama lengkap mahasiswa |
| `Person` (NIM) | Nomor Induk Mahasiswa |
| `Person` (Program Studi) | Contoh: "Informatika" / "Ilmu Komputer" |
| `Person` (Fakultas) | Contoh: "Fakultas Teknik" / "FMIPA" |
| `Person` (Lab) | Contoh: "Lab Big Data & AI" |

**Cara cepat:**
1. Ctrl+H (Find and Replace)
2. Find: `Person`
3. Replace: (isi sesuai data)
4. Replace All

---

## 🧪 FORMULA MATEMATIKA (PENTING!)

Proposal ini menggunakan **LaTeX notation** untuk formula matematika.

### Contoh Formula yang Ada:

**Inline formula:** `$H_0$`, `$p < 0.05$`, `$\alpha = 0.05$`

**Block formula:**
```
$$\text{hit_probability} = \left(\frac{\text{popularity}}{100} \times 0,4\right) + (\text{danceability} \times 0,3) + (\text{energy} \times 0,2) + (\text{balanced_valence} \times 0,1)$$
```

### Google Docs Auto-Conversion:
- ❌ Google Docs **TIDAK otomatis render LaTeX**
- ✅ Gunakan Add-on: **Auto-LaTeX Equations** atau **TeX equation editor**

### Cara Install Add-on:
1. **Extensions → Add-ons → Get add-ons**
2. Cari: **"Auto-LaTeX Equations"**
3. Install & authorize
4. Highlight formula LaTeX (termasuk `$...$` atau `$$...$$`)
5. **Extensions → Auto-LaTeX Equations → Render Equations**

### Alternatif Manual (jika add-on tidak bekerja):
1. Copy formula LaTeX (tanpa `$` symbols)
2. Buka [CodeCogs Equation Editor](https://latex.codecogs.com/eqneditor/editor.php)
3. Paste formula, generate image
4. Download image, insert ke Google Docs

---

## 📊 KODE PYTHON & SYNTAX HIGHLIGHTING

File ini berisi contoh kode Python (misalnya di BAB III bagian F & G).

### Formatting Kode:
1. Pilih semua kode Python
2. Font: **Courier New** atau **Consolas** (monospace)
3. Size: **9 pt**
4. Background: Light gray (#F5F5F5)
5. Border: Optional (Insert → Drawing → Rectangle around code)

**Contoh kode:**
```python
def categorize_tempo(tempo):
    if tempo < 80:
        return 'very_slow'
    # ... etc
```

---

## 📑 CHECKLIST FINAL

Sebelum submit, pastikan:

- [ ] **Cover page** lengkap (nama, NIM, prodi, fakultas)
- [ ] **Daftar Isi** ter-generate dan up-to-date
- [ ] **Page numbers** benar (romawi di awal, arabic di BAB)
- [ ] **Font Book Antiqua 10pt** konsisten di seluruh dokumen
- [ ] **Line spacing 1.15** applied
- [ ] **Margins** sesuai pedoman (L:2.5 T:2.5 R:2 B:2)
- [ ] **Placeholder "Person"** sudah diganti semua
- [ ] **Formula LaTeX** sudah di-render (atau convert ke image)
- [ ] **Kode Python** menggunakan monospace font
- [ ] **Referensi** lengkap 13 items di Daftar Pustaka
- [ ] **Lampiran 1-5** ada dan lengkap
- [ ] **Tidak ada kata ganti persona** (saya, kami, kita, peneliti)
- [ ] **Struktur paragraf** 1 ide pokok + min 2 ide pendukung

---

## 🚀 EXPORT KE PDF (untuk Submission)

1. **File → Download → PDF Document (.pdf)**
2. Pastikan:
   - All pages rendered correctly
   - Formula matematika tampil (bukan plain text)
   - Page numbers correct
   - Font tidak berubah

---

## 🆘 TROUBLESHOOTING

### Issue 1: Formula LaTeX Tidak Ter-Render
**Solusi:**
- Install add-on "Auto-LaTeX Equations"
- Atau convert manual via CodeCogs

### Issue 2: Font Book Antiqua Tidak Tersedia
**Solusi:**
- Gunakan **Times New Roman** sebagai alternatif
- Atau download & install Book Antiqua font di sistem

### Issue 3: A5 Paper Size Tidak Ada
**Solusi:**
- Pilih **Custom size**
- Width: 14.8 cm (5.83 inches)
- Height: 21 cm (8.27 inches)

### Issue 4: Page Numbers Tidak Bisa Berbeda
**Solusi:**
- Gunakan **Section Break** (bukan Page Break)
- Format page number **per section**

---

## 📞 NEXT STEPS

1. ✅ Import `PROPOSAL_TUGAS_AKHIR_UNESA_2.md` ke Google Docs
2. ✅ Apply formatting (font, margins, spacing)
3. ✅ Ganti placeholder "Person"
4. ✅ Render formula LaTeX
5. ✅ Generate Table of Contents
6. ✅ Setup page numbers (romawi → arabic)
7. ✅ Review & proofread
8. ✅ Export to PDF
9. ✅ Submit untuk Sempro! 🎓

---

**Good luck dengan seminar proposal! 🚀**
