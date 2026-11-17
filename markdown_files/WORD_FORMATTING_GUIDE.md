# 📝 PANDUAN FORMATTING PROPOSAL DI MS WORD

> **Untuk convert PROPOSAL_TUGAS_AKHIR_UNESA.md ke format Word sesuai Pedoman UNESA**

---

## 📋 **SPESIFIKASI FORMAT (Pedoman UNESA)**

### **A. Ukuran Kertas & Margin**

```
Ukuran Kertas: A5 (148 mm × 210 mm)
Orientasi: Portrait (Tegak)

Margin:
- Kiri: 2.5 cm
- Atas: 2.5 cm
- Kanan: 2 cm
- Bawah: 2 cm
```

**Cara Setting di Word:**
1. Klik **Layout** → **Size** → pilih **A5**
2. Klik **Layout** → **Margins** → **Custom Margins**
3. Masukkan nilai:
   - Left: 2.5 cm
   - Top: 2.5 cm
   - Right: 2 cm
   - Bottom: 2 cm
4. Klik **OK**

---

### **B. Font & Spacing**

```
Font Family: Book Antiqua
Font Size:
- Body Text: 10 pt
- Judul BAB (Heading 1): 12 pt BOLD
- Sub-judul (Heading 2): 11 pt BOLD
- Sub-sub-judul (Heading 3): 10 pt BOLD

Line Spacing: 1.15
Paragraph Spacing:
- Before: 0 pt
- After: 6 pt

Text Alignment: Justify (rata kiri-kanan)
First Line Indent: 1.27 cm (default tab)
```

**Cara Setting Font Default:**
1. Klik **Home** → **Font** dialog (klik panah kecil di pojok)
2. Pilih **Book Antiqua**, Size **10**
3. Klik **Set As Default** → pilih **All documents**
4. Klik **OK**

**Cara Setting Paragraph:**
1. Klik **Home** → **Paragraph** dialog (klik panah kecil)
2. Set:
   - Alignment: **Justified**
   - Indentation Left: 0, Right: 0, Special: **First line** 1.27 cm
   - Spacing Before: 0, After: 6 pt
   - Line spacing: **Multiple** at **1.15**
3. Klik **Set As Default** → **All documents**
4. Klik **OK**

---

### **C. Heading Styles**

#### **Heading 1 (Judul BAB)**
```
Font: Book Antiqua 12 pt BOLD
Alignment: Center
Spacing Before: 12 pt
Spacing After: 12 pt
ALL CAPS
```

Contoh:
```
BAB I
PENDAHULUAN
```

#### **Heading 2 (Sub Judul Level 1)**
```
Font: Book Antiqua 11 pt BOLD
Alignment: Left
Spacing Before: 12 pt
Spacing After: 6 pt
Format: A. Latar Belakang
```

#### **Heading 3 (Sub Judul Level 2)**
```
Font: Book Antiqua 10 pt BOLD
Alignment: Left
Spacing Before: 6 pt
Spacing After: 6 pt
Format: 1. Karakteristik Audio Features
```

**Cara Modify Styles:**
1. Klik **Home** → Right-click **Heading 1** → **Modify**
2. Set sesuai spesifikasi di atas
3. Centang **Automatically update**
4. Klik **OK**
5. Ulangi untuk Heading 2 dan Heading 3

---

### **D. Penomoran Halaman**

```
Bagian Awal (Cover - Daftar Isi):
- Nomor: Romawi kecil (i, ii, iii, ...)
- Posisi: Bawah tengah

Bagian Isi (BAB I dst):
- Nomor: Arab (1, 2, 3, ...)
- Posisi: Atas kanan (kecuali halaman pertama BAB)
```

**Cara Setting:**

**Section 1 (Bagian Awal):**
1. Posisi cursor di halaman cover
2. **Insert** → **Page Number** → **Bottom of Page** → **Plain Number 2** (center)
3. Double-click nomor halaman → pilih **Roman numerals** (i, ii, iii)

**Section 2 (BAB I dst):**
1. Posisi cursor di awal BAB I
2. **Layout** → **Breaks** → **Next Page** (buat section baru)
3. Double-click header area
4. Klik **Link to Previous** untuk unlink dari section sebelumnya
5. **Insert** → **Page Number** → **Top of Page** → **Plain Number 3** (right)
6. Format → **Start at: 1**

---

## 📄 **STRUKTUR DOKUMEN**

### **Urutan Halaman:**

```
1. HALAMAN COVER (i)
2. [KOSONG - untuk tanda tangan pembimbing] (ii)
3. DAFTAR ISI (iii)
4. [Page Break]
5. BAB I: PENDAHULUAN (1)
6. BAB II: KAJIAN PUSTAKA (lanjut)
7. BAB III: METODE PENELITIAN (lanjut)
8. DAFTAR PUSTAKA (lanjut)
9. LAMPIRAN (lanjut)
```

---

## 🎨 **TEMPLATE COVER PAGE**

Copy teks ini ke halaman pertama Word, lalu format:

```
[Logo UNESA - Insert Image]

PROPOSAL TUGAS AKHIR

ANALISIS ZONA TEMPO UNIVERSAL 
UNTUK PENINGKATAN PREDIKSI POPULARITAS MUSIK 
MENGGUNAKAN PENDEKATAN BIG DATA

Diajukan untuk memenuhi sebagian persyaratan
Tugas Akhir Program Studi [Nama Program Studi]
Fakultas [Nama Fakultas]
Universitas Negeri Surabaya

Disusun Oleh:
[Nama Mahasiswa]
NIM: [Nomor Induk Mahasiswa]

PROGRAM STUDI [NAMA PRODI]
FAKULTAS [NAMA FAKULTAS]
UNIVERSITAS NEGERI SURABAYA
2026
```

**Format Cover:**
- Semua teks: **Center alignment**
- Logo UNESA: Size 3-4 cm, centered, di bagian atas
- Judul: **Book Antiqua 14 pt BOLD**
- Subtitle (Diajukan...): Book Antiqua 11 pt
- Nama & NIM: Book Antiqua 12 pt
- Footer (Program Studi...): Book Antiqua 12 pt BOLD

---

## 📊 **DAFTAR ISI (Auto-Generate)**

**Cara Membuat:**
1. Pastikan semua judul sudah pakai Heading Styles
2. Posisi cursor di halaman Daftar Isi
3. **References** → **Table of Contents** → **Custom Table of Contents**
4. Settings:
   - Show levels: 3
   - Show page numbers: ✓
   - Right align page numbers: ✓
   - Tab leader: ...... (dots)
   - Format: From template
5. Klik **OK**

**Update Daftar Isi:**
- Right-click pada TOC → **Update Field** → **Update entire table**

---

## 🔢 **PENOMORAN OTOMATIS**

### **List Numerik (1, 2, 3)**
```
1. Item pertama
2. Item kedua
3. Item ketiga
```

### **List Alphabet (a, b, c)**
```
a) Sub-item pertama
b) Sub-item kedua
c) Sub-item ketiga
```

**Cara Setting:**
- **Home** → **Numbering** dropdown → **Define New Number Format**
- Pilih style sesuai kebutuhan

---

## 📝 **CODE BLOCKS & FORMULAS**

### **Code Block Python**
```
Font: Courier New 9 pt
Background: Light Gray (Shading)
Border: Solid line
Spacing: Before 6pt, After 6pt
```

**Cara Format:**
1. Paste code
2. Select semua code
3. **Home** → **Font** → **Courier New 9 pt**
4. **Home** → **Shading** → Light Gray
5. **Home** → **Borders** → **All Borders**

### **Mathematical Formulas**

Untuk formula matematika, gunakan **Equation Editor**:
1. **Insert** → **Equation**
2. Ketik formula dengan symbols yang tersedia
3. Atau ketik LaTeX-style: `x^2 + y^2 = z^2`

---

## 📊 **TABEL FORMAT**

```
Font: Book Antiqua 9 pt
Header Row: BOLD + Gray Background
Borders: All solid lines
Cell Padding: 0.05 cm
Alignment: Header = Center, Data = Left/Center
```

**Cara Create Table:**
1. **Insert** → **Table** → pilih jumlah kolom/baris
2. Right-click header row → **Table Properties** → **Row**
   - Check **Repeat as header row**
3. Select header → **Home** → **Shading** → Gray-25%
4. Select header → **Home** → **Bold**

---

## 🖼️ **IMAGES & DIAGRAMS**

```
Alignment: Center
Wrapping: In line with text
Caption: Below image
Caption Format: "Gambar [nomor]. [Judul]"
Font Caption: Book Antiqua 9 pt Italic
```

**Cara Insert Image:**
1. **Insert** → **Pictures** → pilih file
2. Resize sesuai kebutuhan (max width 10 cm untuk A5)
3. Right-click → **Wrap Text** → **In Line with Text**
4. Pastikan centered
5. **References** → **Insert Caption**
   - Label: Gambar
   - Position: Below selected item
   - Numbering: 1, 2, 3...

---

## 📚 **DAFTAR PUSTAKA FORMAT**

### **Format APA 7th Edition:**

**Jurnal:**
```
Penulis, A. A., & Penulis, B. B. (Tahun). Judul artikel. Nama Jurnal, Volume(Issue), halaman-halaman. https://doi.org/xxxxx
```

**Buku:**
```
Penulis, A. A. (Tahun). Judul buku (Edisi). Penerbit.
```

**Cara Format:**
- Hanging indent: 1.27 cm
- Line spacing: 1.15
- Sort alphabetically by author lastname

**Cara Set Hanging Indent:**
1. Select semua referensi
2. **Home** → **Paragraph** dialog
3. Indentation: Special → **Hanging** → 1.27 cm

---

## ✅ **FINAL CHECKLIST**

Sebelum submit, check:

- [ ] Ukuran kertas A5
- [ ] Margin sesuai (L:2.5, T:2.5, R:2, B:2)
- [ ] Font Book Antiqua 10pt
- [ ] Line spacing 1.15
- [ ] Justified alignment
- [ ] First line indent 1.27cm
- [ ] Heading styles consistent
- [ ] Page numbers correct (i,ii,iii... then 1,2,3...)
- [ ] Daftar Isi updated
- [ ] No orphan/widow paragraphs
- [ ] Cover page formatted
- [ ] Nama, NIM filled
- [ ] Daftar Pustaka sorted alphabetically
- [ ] All tables/figures numbered
- [ ] No syntax errors
- [ ] Print preview checked

---

## 🚀 **QUICK START STEPS**

### **Langkah Cepat (15 menit):**

1. **Buat dokumen baru Word**
2. **Set page A5** (Layout → Size → A5)
3. **Set margins** (Layout → Margins → Custom: 2.5, 2.5, 2, 2)
4. **Set default font** (Home → Font dialog → Book Antiqua 10pt → Set As Default)
5. **Set default paragraph** (Home → Paragraph → Justified, 1.15 spacing, First line 1.27cm → Set As Default)
6. **Modify Heading Styles** (Heading 1, 2, 3 sesuai guide)
7. **Buat Cover Page** (copy template, insert logo UNESA)
8. **Copy-paste konten dari PROPOSAL_TUGAS_AKHIR_UNESA.md**
9. **Apply Heading Styles** ke semua judul
10. **Insert Table of Contents** (References → TOC)
11. **Format code blocks** (Courier New + Gray background)
12. **Format tables** (Header bold + gray)
13. **Set page numbering** (Roman untuk awal, Arabic untuk isi)
14. **Update TOC** (Right-click → Update Field)
15. **Final check** dengan checklist di atas

---

## 💡 **TIPS & TRICKS**

### **Tip 1: Gunakan Styles Consistently**
- Jangan manual format (bold/size) untuk judul
- Selalu gunakan Heading Styles
- TOC akan auto-update

### **Tip 2: Navigation Pane**
- **View** → **Navigation Pane** (check)
- Lihat outline dokumen
- Easy jump antar sections

### **Tip 3: Show/Hide Formatting Marks**
- **Home** → ¶ (Show/Hide button)
- Lihat spaces, tabs, page breaks
- Helpful untuk debug formatting issues

### **Tip 4: Print Preview Before Submit**
- **File** → **Print** → lihat preview
- Check page breaks, margins, alignment
- Ensure no weird formatting

### **Tip 5: Save Multiple Versions**
- `Proposal_v1.docx`
- `Proposal_v2_revised.docx`
- `Proposal_FINAL.docx`
- Keep backups!

---

## 📞 **TROUBLESHOOTING**

### **Problem: Font berubah sendiri**
**Solution:** Set As Default font di awal, pastikan "All documents based on Normal template"

### **Problem: Paragraph indent inconsistent**
**Solution:** Clear all formatting (Ctrl+Space), reapply styles

### **Problem: Page numbers wrong**
**Solution:** Check section breaks, ensure "Link to Previous" di-unlink

### **Problem: TOC tidak update**
**Solution:** Right-click TOC → Update Field → Update entire table

### **Problem: Spacing between paragraphs too much**
**Solution:** Check Paragraph settings → Spacing After should be 6pt, not auto

---

## 📄 **TEMPLATE SIAP PAKAI**

Aku sudah buatkan file terpisah: `PROPOSAL_WORD_READY.md` yang isinya **SAMA PERSIS** dengan proposal tapi **formatted untuk copy-paste langsung ke Word**.

File tersebut include:
- ✅ Markers untuk heading styles ([H1], [H2], [H3])
- ✅ Indikator page breaks ([PAGE BREAK])
- ✅ Format code blocks ([CODE])
- ✅ Format tables ([TABLE])
- ✅ Instructions inline

**Cara pakai:**
1. Buka `PROPOSAL_WORD_READY.md`
2. Copy section by section
3. Paste ke Word
4. Apply formatting sesuai markers
5. Done!

---

## 🎓 **UNTUK SUBMISSION**

### **Checklist Final:**
- [ ] Print ke PDF (File → Save As → PDF)
- [ ] Check PDF appearance
- [ ] File size reasonable (<5 MB)
- [ ] Filename: `Proposal_TA_NamaAnda_NIM.pdf`
- [ ] Backup .docx file
- [ ] Ready to submit!

---

**STATUS:** ✅ **GUIDE COMPLETE**  
**Next:** Apply formatting ke Word document  
**Estimated Time:** 15-30 minutes

**Good luck with your proposal! 🚀**
