# **PROPOSAL TUGAS AKHIR**

# **ANALISIS ZONA TEMPO UNIVERSAL UNTUK PENINGKATAN PREDIKSI POPULARITAS MUSIK MENGGUNAKAN PENDEKATAN BIG DATA**

*Analysis of Universal Tempo Zone for Enhanced Music Popularity Prediction Using Big Data Approach*

Diajukan untuk memenuhi sebagian persyaratan Tugas Akhir Program Studi Person Fakultas Person Universitas Negeri Surabaya

**Disusun Oleh:**  
Person  
NIM: Person

**PROGRAM STUDI Person**  
**FAKULTAS Person**  
**UNIVERSITAS NEGERI SURABAYA**  
**2026**

# **BAB I: PENDAHULUAN**

# **A. Latar Belakang**

Industri musik global mengalami transformasi signifikan dengan hadirnya platform distribusi digital seperti Spotify, Apple Music, dan YouTube Music. Berdasarkan data International Federation of the Phonographic Industry (IFPI) tahun 2025, pendapatan musik digital mencapai 67% dari total pendapatan industri musik global, dengan lebih dari 500 juta pengguna aktif layanan streaming musik di seluruh dunia. Transformasi ini menghasilkan volume data audio yang masif, menciptakan peluang bagi analisis mendalam terhadap karakteristik musik yang mempengaruhi popularitas lagu.

Tempo, yang diukur dalam satuan beats per minute (BPM), merupakan salah satu elemen fundamental dalam komposisi musik yang menentukan kecepatan dan ritme suatu lagu. Paradigma konvensional dalam industri musik menyatakan bahwa pemilihan tempo bergantung pada genre dan mood lagu yang diinginkan. Lagu dengan energi tinggi cenderung menggunakan tempo cepat di atas 140 BPM, sementara lagu melankolis atau sedih umumnya mengadopsi tempo lambat di bawah 100 BPM. Asumsi ini telah menjadi pedoman bagi produser musik, komposer, dan label rekaman dalam proses produksi musik selama beberapa dekade.

Namun demikian, penelitian empiris berbasis data berskala besar terhadap hubungan antara tempo dan popularitas musik lintas berbagai kategori mood masih terbatas. Mayoritas studi existing fokus pada analisis tempo dalam konteks genre spesifik atau terbatas pada sampel kecil yang tidak mencerminkan keberagaman musik global. Sebagai contoh, penelitian oleh Percino et al. (2014) menganalisis karakteristik musik populer menggunakan dataset Million Song Dataset, namun tidak secara spesifik menguji hipotesis zona tempo universal. Demikian pula, studi oleh Interiano et al. (2018) mengeksplorasi evolusi karakteristik musik populer dari tahun 1960–2010, tetapi tidak melakukan analisis komparatif mendalam terhadap efek tempo lintas kategori mood.

Kesenjangan pengetahuan ini menciptakan peluang untuk mengeksplorasi apakah terdapat zona tempo tertentu yang secara universal menghasilkan probabilitas popularitas lebih tinggi, terlepas dari kategori mood lagu. Pertanyaan ini relevan tidak hanya dari perspektif teoretis pemahaman persepsi musik manusia, tetapi juga memiliki implikasi praktis bagi industri musik dalam optimasi proses produksi dan kurasi konten.

Penelitian ini menggunakan pendekatan Big Data dengan menganalisis dataset Spotify yang terdiri dari 1.204.022 lagu yang dirilis antara tahun 1920 hingga 2020\. Dataset ini mencakup 24 fitur audio yang diekstraksi menggunakan Spotify Web API, termasuk tempo, energy, valence, danceability, dan popularity. Skala data yang masif ini memungkinkan analisis statistik robust dengan tingkat presisi tinggi, mengatasi keterbatasan sampel pada penelitian-penelitian sebelumnya.

Studi pendahuluan eksploratori terhadap dataset mengindikasikan adanya pola menarik yang bertentangan dengan paradigma konvensional. Analisis awal menunjukkan bahwa lagu-lagu pada rentang tempo 100–120 BPM secara konsisten memiliki nilai hit probability lebih tinggi dibandingkan rentang tempo lainnya, dan pola ini teramati secara seragam pada lima kategori mood yang berbeda: *happy energetic*, *sad slow*, *angry intense*, *calm positive*, dan *melancholic*. Temuan *preliminary* ini mengindikasikan kemungkinan eksistensi zona tempo universal yang belum terdokumentasi dalam literatur *music informatics*.

Jika hipotesis zona tempo universal terbukti valid secara statistik, temuan ini memiliki signifikansi teoretis dalam memahami mekanisme fisiologis dan psikologis persepsi tempo oleh manusia. Dari perspektif fisiologis, rentang tempo 100–120 BPM berkorespondensi dengan kecepatan jalan rata-rata manusia (80–100 langkah per menit yang dirasakan sebagai tempo ganda) dan heart rate istirahat (60–100 BPM), yang mungkin menciptakan resonansi natural dengan ritme biologis manusia. Secara praktis, validasi hipotesis ini dapat menyediakan guideline evidence-based bagi praktisi industri musik dalam pengambilan keputusan terkait tempo komposisi.

Lebih lanjut, dengan mengintegrasikan temuan zona tempo universal ke dalam model prediksi popularitas musik berbasis *machine learning*, penelitian ini bertujuan mendemonstrasikan nilai praktis dari *discovery* tersebut. Model prediksi yang menginkorporasikan fitur zona tempo diharapkan dapat mencapai akurasi superior dibandingkan model baseline yang hanya menggunakan fitur audio konvensional, memvalidasi utilitas aplikatif dari temuan penelitian.

Berdasarkan uraian di atas, terdapat urgensi untuk melakukan investigasi sistematis dan komprehensif terhadap eksistensi dan karakteristik zona tempo universal menggunakan metodologi *Big Data analytics* dan *statistical inference rigorous*. Penelitian ini diharapkan dapat memberikan kontribusi teoretis bagi bidang *music information retrieval* dan memberikan rekomendasi actionable bagi industri musik dalam optimasi strategi produksi konten.

# **B. Rumusan Masalah**

Berdasarkan latar belakang yang telah diuraikan, rumusan masalah penelitian ini adalah sebagai berikut:

1. Apakah terdapat zona tempo universal yang menghasilkan *hit probability* signifikan lebih tinggi dibandingkan zona tempo lainnya pada dataset musik Spotify berskala besar?  
2. Apakah pola zona tempo universal konsisten berlaku di seluruh kategori mood musik (*happy energetic*, *sad slow*, *angry intense*, *calm positive*, dan *melancholic*)?  
3. Berapa besar magnitude efek (*effect size*) dari zona tempo universal terhadap peningkatan *hit probability* lagu?  
4. Bagaimana karakteristik fitur audio lainnya (*energy*, *valence*, *danceability*, *loudness*) berkorelasi dengan *hit probability* pada lagu-lagu yang berada dalam zona tempo universal?  
5. Seberapa besar peningkatan akurasi model prediksi popularitas musik ketika fitur zona tempo universal diintegrasikan sebagai variabel prediktor dibandingkan dengan model *baseline*?

# **C. Tujuan Penelitian**

Tujuan dari penelitian ini adalah:

1. Mengidentifikasi dan memvalidasi secara statistik eksistensi zona tempo universal yang menghasilkan *hit probability* superior pada dataset musik Spotify berskala 1,2 juta lagu.  
2. Mengevaluasi konsistensi pola zona tempo universal di seluruh kategori mood musik melalui analisis komparatif multi-kelompok.  
3. Mengkuantifikasi magnitude efek zona tempo universal terhadap *hit probability* menggunakan ukuran *Cohen's d* dan *percentage difference*.  
4. Menganalisis interaksi dan korelasi antara zona tempo universal dengan fitur audio sekunder (*energy*, *valence*, *danceability*, *loudness*) dalam konteks prediksi popularitas.  
5. Membangun dan membandingkan performa model *machine learning* untuk prediksi popularitas musik dengan dan tanpa fitur zona tempo universal sebagai variabel independen.

# **D. Manfaat Penelitian**

## **1\. Manfaat Teoretis**

a. Memberikan kontribusi empiris terhadap pemahaman hubungan antara tempo dan persepsi popularitas musik dalam perspektif music information retrieval dan computational musicology.  
b. Menyediakan bukti statistik terhadap eksistensi pola universal dalam preferensi tempo manusia lintas kategori mood, yang dapat memperkaya teori persepsi musik dan psikologi musik.  
c. Memperluas literatur Big Data analytics dalam domain music analysis dengan mendemonstrasikan aplikasi metodologi statistik inferensial pada dataset berskala jutaan observasi.  
d. Memberikan framework metodologis untuk eksplorasi pola-pola *underrated* dalam karakteristik audio musik yang dapat diadopsi oleh penelitian-penelitian selanjutnya.

## **2\. Manfaat Praktis**

a. Menyediakan guideline evidence-based bagi komposer, produser musik, dan label rekaman dalam pengambilan keputusan terkait pemilihan tempo komposisi untuk optimasi potensi popularitas.  
b. Memberikan insight actionable bagi kurator playlist pada platform streaming musik untuk optimasi engagement pengguna melalui kurasi berbasis zona tempo.  
c. Menyediakan fitur prediksi tambahan bagi sistem rekomendasi musik untuk meningkatkan akurasi prediksi preferensi pengguna.  
d. Memfasilitasi adopsi pendekatan data-driven dalam industri musik kreatif, mengurangi ketergantungan pada intuisi subjektif dalam proses produksi musik.  
e. Memberikan rekomendasi praktis bagi emerging artists dalam memaksimalkan potensi viral musik mereka melalui optimasi parameter teknis yang terukur.

# **E. Batasan Penelitian**

Untuk memfokuskan lingkup penelitian dan menjaga kelayakan eksekusi, penelitian ini dibatasi pada aspek-aspek berikut:

1. Dataset yang digunakan terbatas pada musik yang tersedia di platform Spotify dengan fitur audio yang diekstraksi melalui Spotify Web API, mencakup periode rilis tahun 1920 hingga 2020\.  
2. Analisis tempo dibatasi pada klasifikasi kategorik menjadi lima zona tempo (*very slow* \< 80 BPM, *slow* 80–100 BPM, *medium* 100–120 BPM, *fast* 120–140 BPM, *very fast* \> 140 BPM), bukan analisis granular per-BPM individual.  
3. Kategorisasi mood dilakukan berdasarkan pendekatan *rule-based* menggunakan kombinasi nilai *energy* dan *valence*, menghasilkan lima kategori mood (*happy energetic*, *sad slow*, *angry intense*, *calm positive*, *melancholic*).  
4. *Hit probability* dikalkulasi sebagai *composite metric* berbasis *weighted combination* dari *popularity*, *danceability*, *energy*, dan *balanced valence*, bukan metrik *streaming* aktual atau *chart performance*.  
5. Model prediksi *machine learning* dibatasi pada algoritma *supervised learning* klasik (*Random Forest*, *Gradient Boosting*) dan tidak mencakup arsitektur *deep learning* yang kompleks.  
6. Analisis kausalitas terbatas pada identifikasi korelasi dan *association patterns*; untuk inferensi kausal memerlukan studi lanjutan dengan desain *quasi-experimental* atau *randomized controlled trial*.  
7. Penelitian ini tidak melakukan analisis spesifik genre karena keterbatasan label genre pada dataset; fokus utama adalah analisis lintas kategori mood.

# **F. Asumsi Penelitian**

Penelitian ini didasarkan pada asumsi-asumsi metodologis dan substantif berikut:

1. Fitur audio yang diekstraksi melalui Spotify Web API (*tempo*, *energy*, *valence*, *danceability*, dll.) merupakan representasi valid dan reliabel dari karakteristik akustik dan perseptual musik yang dianalisis.  
2. Nilai *popularity* yang disediakan Spotify mencerminkan agregasi dari *streaming count*, *playlist inclusion*, dan *user engagement*, sehingga dapat dijadikan *proxy metric* untuk popularitas aktual lagu.  
3. Kategorisasi mood berdasarkan kombinasi *energy* dan *valence* merupakan aproksimasi yang wajar terhadap konten emosional lagu, meskipun persepsi emosi musik bersifat subjektif dan dapat bervariasi antar individu.  
4. *Hit probability* sebagai *composite metric* mencerminkan potensi popularitas lagu secara lebih komprehensif dibandingkan *single metric popularity score standalone*.  
5. Dataset Spotify yang digunakan representatif terhadap lanskap musik global, meskipun mungkin terdapat bias terhadap musik *Western* dan musik populer kontemporer.  
6. Hubungan antara tempo dan *hit probability* yang teramati pada dataset historis (1920–2020) dapat diterapkan untuk prediksi tren masa depan, dengan catatan bahwa preferensi musik dapat berevolusi seiring waktu.  
7. Sampel dalam dataset diasumsikan independen satu sama lain, meskipun dalam praktik terdapat *clustering effect* pada lagu-lagu dari artis atau album yang sama.

# **BAB II: KAJIAN PUSTAKA**

# **A. Kajian Teori**

## **1\. Karakteristik Audio Features dalam Music Information Retrieval**

*Music Information Retrieval* (MIR) merupakan bidang interdisipliner yang menggabungkan ilmu komputer, *signal processing*, dan musikologi untuk ekstraksi, analisis, dan *retrieval* informasi dari konten audio musik. Dalam konteks MIR, karakteristik musik dapat didekomposisi menjadi serangkaian fitur audio yang terukur secara kuantitatif.

Menurut Müller (2015), fitur audio dapat dikategorisasi menjadi tiga level: low-level features (spektral, temporal), mid-level features (chroma, MFCC), dan high-level features (mood, genre). Spotify Web API menyediakan high-level features yang telah melalui proses machine learning untuk ekstraksi karakteristik perseptual musik, termasuk *tempo*, *energy*, *valence*, *danceability*, dan lainnya.

Tempo didefinisikan sebagai kecepatan musik yang diukur dalam beats per minute (BPM). Tempo tidak hanya menentukan kecepatan absolut musik, tetapi juga mempengaruhi persepsi *emotional intensity* dan *physical response* pendengar. Penelitian oleh Van Dyck et al. (2017) menunjukkan bahwa tempo berkorelasi dengan spontaneous motor responses dan arousal levels pada pendengar.

**Energy** merepresentasikan ukuran persepsi intensitas dan aktivitas suatu trek. Nilai *energy* tinggi (mendekati 1.0) mengindikasikan trek yang cepat, keras, dan bising, sementara nilai rendah mencerminkan trek yang lembut dan tenang. Energy dikalkulasi berdasarkan kombinasi dynamic range, perceived loudness, timbre, dan onset rate.

Valence mengukur tingkat kepositifan musik yang disampaikan oleh trek. Trek dengan valence tinggi terdengar positif, ceria, dan euforik, sementara *valence* rendah terdengar sedih, tertekan, atau marah. Valence merupakan komponen penting dalam dimensional models of emotion yang mengombinasikan arousal (energy) dan *valence* untuk pemetaan ruang emosional.

**Danceability** mengukur seberapa cocok suatu trek untuk menari berdasarkan kombinasi tempo, rhythm stability, beat strength, dan keteraturan keseluruhan. Nilai danceability tinggi mengindikasikan trek yang mudah untuk dipakai menari.

## **2\. Big Data Analytics dalam Music Analysis**

Big Data didefinisikan sebagai dataset yang volume, kecepatan (velocity), dan keragamannya (variety) melampaui kapabilitas sistem manajemen basis data tradisional untuk ditangkap, disimpan, dikelola, dan dianalisis (Laney, 2001). Dalam konteks analisis musik, ketersediaan platform *streaming* telah menghasilkan volume data yang mencapai skala petabita, mencakup tidak hanya fitur audio tetapi juga perilaku pengguna, pola streaming, dan interaksi sosial.

Analisis Big Data dalam domain musik memungkinkan identifikasi pola dan korelasi yang tidak terobservasi pada studi tradisional skala kecil. Penelitian oleh Schedl et al. (2014) mendemonstrasikan bahwa analisis data skala besar dapat mengungkap wawasan tentang pola konsumsi musik, preferensi geografis, dan dinamika temporal dari popularitas musik.

Penggunaan *Big Data analytics* dalam penelitian ini memungkinkan inferensi statistik dengan *statistical power* yang sangat tinggi, margin of error minimal, dan generalisasi yang superior dibandingkan convenience sampling pada penelitian tradisional. Dengan ukuran sampel 1,2 juta observasi, interval kepercayaan untuk estimasi parameter menjadi sangat sempit, meningkatkan presisi dan reliabilitas temuan penelitian.

## **3\. Teori Persepsi Tempo dan Respons Fisiologis**

Persepsi tempo oleh manusia tidak bersifat acak, melainkan terkait dengan ritme biologis dan sistem motorik manusia. Penelitian dalam bidang psikofisiologi musik menunjukkan bahwa tempo musik dapat mempengaruhi heart rate, breathing rate, dan respons motorik.

Moelants (2002) melakukan analisis terhadap distribusi tempo pada musik populer Barat dan menemukan puncak distribusi pada sekitar 120 BPM, yang berkorespondensi dengan dua kali kecepatan berjalan santai manusia (sekitar 60 langkah per menit per kaki, atau 120 langkah total). Temuan ini mengindikasikan potensi keterkaitan (coupling) antara tempo musik dan sistem motorik manusia.

Fraisse (1982) dalam teori *"preferred tempo"* mengajukan bahwa terdapat rentang tempo optimal (sekitar 100–120 BPM) di mana manusia paling mudah menyinkronkan gerakan dan mempersepsikan pola ritmis. Tempo di luar rentang ini membutuhkan usaha kognitif yang lebih besar untuk pemrosesan dan sinkronisasi.

Lebih lanjut, penelitian neurosains musik menunjukkan bahwa tempo dalam rentang sedang (90–120 BPM) mengaktivasi *basal ganglia* dan *motor cortex* secara efisien, memfasilitasi respons motorik involuntar seperti ketukan kaki dan anggukan kepala (Grahn & Brett, 2007). Pola aktivasi ini dapat berkontribusi pada peningkatan kenikmatan dan daya ingat musik pada rentang tempo tersebut.

## **4\. Model Prediksi Popularitas Musik**

Prediksi popularitas musik merupakan area aplikasi penting dalam *music informatics* dengan implikasi praktis bagi industri musik. Model prediksi popularitas umumnya mengadopsi pendekatan supervised machine learning di mana fitur audio, metadata, dan informasi kontekstual digunakan sebagai fitur masukan untuk memprediksi metrik popularitas sebagai variabel target.

Penelitian oleh Ni et al. (2011) menggunakan pengklasifikasi Random Forest untuk prediksi lagu populer berdasarkan fitur audio dari Million Song Dataset, mencapai akurasi 74%. Penelitian oleh Dhanaraj & Logan (2005) mengeksplorasi prediksi otomatis lagu populer menggunakan *Support Vector Machines*, menunjukkan bahwa fitur audio saja dapat memprediksi keberhasilan tangga lagu dengan akurasi sedang.

Model prediksi modern semakin canggih dengan mengintegrasikan tidak hanya fitur audio tetapi juga sinyal sosial (sebutan media sosial, inklusi *playlist*), pola temporal (waktu rilis, momentum), dan karakteristik artis (jumlah pengikut, keberhasilan masa lalu). Penelitian oleh Dhar et al. (2019) mendemonstrasikan bahwa model hibrida yang menggabungkan berbagai tipe fitur mencapai performa superior dibandingkan model modalitas tunggal.

Dalam konteks penelitian ini, hipotesis zona tempo universal akan divalidasi tidak hanya melalui pengujian signifikansi statistik, tetapi juga melalui validasi pragmatis dengan membandingkan performa prediktif model yang menyertakan versus mengabaikan fitur zona tempo. Peningkatan performa model akan berfungsi sebagai validasi praktis dari temuan teoretis.

# **B. Penelitian yang Relevan**

## **1\. Analisis Karakteristik Musik Populer Berskala Besar**

Percino et al. (2014) melakukan analisis evolusi struktur genre musik menggunakan dataset Million Song Dataset yang terdiri dari 1 juta lagu. Penelitian ini menggunakan fitur audio untuk mengkonstruksi jaringan kemiripan musik dan menganalisis perubahan properti struktural dari tahun 1955–2010. Temuan menunjukkan bahwa keragaman genre musik meningkat seiring waktu, dengan homogenisasi terjadi pada musik mainstream. Namun, penelitian ini tidak secara eksplisit menganalisis efek tempo terhadap popularitas musik lintas kategori mood.

Interiano et al. (2018) mengeksplorasi evolusi musik populer menggunakan fitur audio dari tahun 1960 hingga 2010\. Penelitian menggunakan dataset 17.000 lagu Billboard Hot 100 dan menganalisis tren temporal dalam loudness, timbre, dan karakteristik nada. Temuan menunjukkan peningkatan *loudness* dan homogenisasi palet timbral dalam musik kontemporer. Meskipun tempo merupakan salah satu fitur yang dianalisis, penelitian ini tidak melakukan analisis komparatif lintas mood untuk mengidentifikasi pola tempo universal.

## **2\. Prediksi Popularitas Musik Berbasis Machine Learning**

Ni et al. (2011) mengembangkan sistem prediksi otomatis untuk mengidentifikasi lagu populer berdasarkan fitur audio. Penelitian menggunakan pengklasifikasi *Random Forest* dengan 16 fitur audio sebagai prediktor. Model mencapai akurasi klasifikasi 74% dalam membedakan lagu *hits* dan *non-hits*. Penelitian ini mendemonstrasikan kelayakan prediksi berbasis audio, namun tidak mengeksplorasi potensi fitur spesifik tempo sebagai prediktor diskrit.

Dhar et al. (2019) mengintegrasikan fitur audio dengan sinyal sosial (sebutan Twitter, penayangan YouTube) untuk meningkatkan prediksi popularitas lagu. Model hibrida mencapai akurasi 83%, superior dibandingkan model *baseline* berbasis audio saja (71%). Penelitian ini menyoroti pentingnya fitur multi-modal, namun perlakuan terhadap tempo masih terbatas sebagai fitur numerik kontinu tanpa segmentasi kategorikal.

## **3\. Tempo dan Mood dalam Musik**

Van Dyck et al. (2017) menginvestigasi sinkronisasi spontan gerakan tubuh terhadap musik dengan tempo yang bervariasi. Studi eksperimental dengan 50 partisipan menunjukkan bahwa rentang tempo 100–130 BPM menghasilkan respons sinkronisasi terkuat dan penilaian kenikmatan tertinggi. Temuan ini memberikan bukti awal untuk eksistensi zona tempo yang disukai, namun ukuran sampel terbatas dan tidak melakukan analisis lintas mood.

Husain et al. (2002) mengeksplorasi efek tempo dan tangga nada (*mode*) musik terhadap *arousal*, mood, dan kemampuan spasial. Studi eksperimental menunjukkan bahwa tempo berinteraksi dengan *mode* (mayor/minor) dalam mempengaruhi tingkat *arousal* dan *mood*. Tempo cepat meningkatkan *arousal* tanpa memandang *mode*, sementara tempo lambat menghasilkan efek menenangkan. Namun, penelitian ini tidak menjawab pertanyaan tentang tempo optimal untuk maksimisasi daya tarik atau popularitas.

## **4\. Analisis Kesenjangan (Gap Analysis)**

Berdasarkan kajian literatur di atas, dapat diidentifikasi beberapa kesenjangan penelitian (research gaps) yang signifikan:

* **Gap 1:** Belum terdapat penelitian yang secara eksplisit menguji hipotesis zona tempo universal menggunakan dataset berskala jutaan observasi yang representatif terhadap lanskap musik yang beragam.  
* **Gap 2:** Mayoritas penelitian yang ada menganalisis tempo sebagai variabel kontinu atau dalam konteks analisis spesifik genre. Analisis komprehensif lintas mood untuk mengidentifikasi pola universal belum dilakukan.  
* **Gap 3:** Validasi praktis dari temuan teoretis melalui integrasi ke dalam model prediksi dan penilaian nilai prediktif inkremental belum banyak dieksplorasi.  
* **Gap 4:** Kuantifikasi *effect size* (magnitude efek) dari zona tempo terhadap metrik popularitas belum ditangani secara memadai. Mayoritas studi berfokus pada signifikansi statistik tanpa melaporkan signifikansi praktis.

Penelitian ini bertujuan untuk mengatasi kesenjangan tersebut melalui analisis komprehensif hipotesis zona tempo universal menggunakan pendekatan Big Data, validasi statistik yang ketat, analisis komparatif lintas mood, dan validasi pragmatis melalui pemodelan prediktif.

# **C. Kerangka Berpikir**

Kerangka konseptual penelitian ini dibangun berdasarkan integrasi teori persepsi musik, psikofisiologi tempo, dan metodologi *Big Data analytics*.

1. **Input Data:** Karakteristik Audio Musik dikumpulkan dari dataset Spotify.  
2. **Ekstraksi Fitur:** Ekstraksi nilai *Tempo* dalam satuan BPM.  
3. **Kategorisasi:** Pembentukan *Kategorisasi Zona Tempo* (*Very Slow*, *Slow*, *Medium*, *Fast*, *Very Fast*).  
4. **Analisis Komparatif:** *Analisis Lintas Kategori Mood* (*Happy*, *Sad*, *Angry*, *Calm*, *Melancholic*).  
5. **Identifikasi:** *Identifikasi Pola Universal* dari performa metrik di seluruh kategori.  
6. **Validasi:** *Validasi Statistik* menggunakan T-test, ANOVA, dan pengujian *Effect Size*.  
7. **Temuan Utama:** Penentuan *Zona Tempo Universal* (100–120 BPM).  
8. **Penerapan:** *Integrasi ke Model Prediksi* *machine learning*.  
9. **Hasil Akhir:** Peningkatan performa *Hit Probability Enhancement*.

## **Proposisi Teoretis**

Berdasarkan teori *preferred tempo* (Fraisse, 1982\) dan bukti empiris dari studi psikofisiologi (Van Dyck et al., 2017), tempo dalam rentang 100–120 BPM berkorespondensi dengan ritme biologis manusia (kecepatan berjalan, detak jantung), sehingga musik pada rentang tempo tersebut menghasilkan peningkatan kenikmatan, daya ingat, dan keterlibatan pendengar.

## **Hipotesis Pola Universal**

Jika tempo 100–120 BPM benar-benar merepresentasikan zona optimal berdasarkan kesesuaian biologis, maka efeknya harus bersifat universal dan tidak terbatas pada mood atau genre spesifik. Musik dengan konten emosional apapun (happy, sad, angry, calm, melancholic) yang dikomposisikan pada tempo 100–120 BPM akan menunjukkan hit probability yang superior dibandingkan zona tempo lainnya.

## **Mekanisme Prediksi**

Inkorporasi zona tempo universal sebagai fitur diskrit dalam model prediktif diharapkan dapat menangkap hubungan non-linear antara tempo dan popularitas yang berpotensi terlewatkan oleh representasi numerik kontinu dari tempo. Pengodean kategorikal memungkinkan model untuk mempelajari efek diferensial antar zona tempo secara eksplisit.

# **D. Hipotesis Penelitian**

Berdasarkan kajian teori, penelitian relevan, dan kerangka berpikir yang telah diuraikan, hipotesis penelitian ini dirumuskan sebagai berikut:

* **Hipotesis 1 (H1):** Terdapat perbedaan signifikan dalam *hit probability* antara lagu pada zona tempo *medium* (100–120 BPM) dengan lagu pada zona tempo lainnya, di mana zona tempo *medium* menghasilkan *hit probability* superior secara statistik (p \< 0.05).  
* **Hipotesis 2 (H2):** Pola superioritas zona tempo *medium* (100–120 BPM) konsisten berlaku di seluruh lima kategori mood (*happy energetic*, *sad slow*, *angry intense*, *calm positive*, dan *melancholic*), menunjukkan eksistensi pola universal.  
* **Hipotesis 3 (H3):** Magnitude efek (*effect size*) dari zona tempo *medium* terhadap *hit probability* tergolong praktis signifikan, dengan *Cohen's d* ≥ 0.5 (*medium effect size*) atau *percentage difference* ≥ 15%.  
* **Hipotesis 4 (H4):** Model prediksi *machine learning* yang mengintegrasikan fitur zona tempo universal mencapai akurasi prediksi signifikan lebih tinggi (minimum \+5%) dibandingkan model *baseline* yang tidak menggunakan fitur tersebut.

# **BAB III: METODE PENELITIAN**

# **A. Jenis dan Rancangan Penelitian**

Penelitian ini mengadopsi pendekatan kuantitatif metode campuran (*mixed-method quantitative approach*) yang mengombinasikan analisis data eksploratif, inferensi statistik konfirmatori, dan pemodelan prediktif. Jenis penelitian adalah studi korelasional non-eksperimental dengan metodologi Big Data analytics.

Rancangan penelitian terdiri dari empat fase sekuensial:

* **Fase 1 (Exploratory Discovery):** Eksplorasi dataset untuk mengidentifikasi pola awal dalam distribusi tempo dan hubungannya dengan *hit probability* di seluruh kategori mood.  
* **Fase 2 (Confirmatory Statistical Testing):** Validasi hipotesis zona tempo universal menggunakan statistik inferensial (*t-test*, ANOVA) dan kuantifikasi *effect size* (*Cohen's d*).  
* **Fase 3 (Cross-Mood Validation):** Analisis komparatif untuk memverifikasi konsistensi pola zona tempo di seluruh kategori mood.  
* **Fase 4 (Predictive Modeling):** Pengembangan dan evaluasi model *machine learning* untuk menilai kegunaan praktis dari fitur zona tempo universal dalam tugas prediksi.

# **B. Tempat dan Waktu Penelitian**

**Tempat Penelitian:**  
Penelitian ini dilaksanakan di Laboratorium Komputasi Person, Program Studi Person, Fakultas Person, Universitas Negeri Surabaya.

**Waktu Penelitian:**  
Penelitian dilaksanakan selama 6 bulan, dengan rincian jadwal sebagai berikut:

* **Bulan 1:** Tinjauan pustaka dan akuisisi data.  
* **Bulan 2:** Pra-pemrosesan data dan analisis data eksploratif.  
* **Bulan 3:** Rekayasa fitur dan kategorisasi mood.  
* **Bulan 4:** Pengujian hipotesis statistik dan validasi.  
* **Bulan 5:** Pengembangan model prediktif dan evaluasi.  
* **Bulan 6:** Sintesis analisis, interpretasi, dan penyusunan laporan.

# **C. Sumber Data dan Populasi**

## **1\. Sumber Data**

Data penelitian bersumber dari *Spotify Music Dataset* yang diperoleh melalui platform Kaggle, dipublikasikan oleh Rodolfo Figueroa dengan lisensi *Creative Commons Public Domain* (CC0). Dataset terdiri dari berkas `tracks_features.csv` dengan ukuran 500 MB yang berisi informasi metadata dan fitur audio untuk setiap trek.

Dataset asli diekstraksi menggunakan Spotify Web API yang menyediakan fitur analisis audio melalui model *machine learning* milik Spotify. Fitur audio yang tersedia mencakup tempo, energy, valence, danceability, acousticness, instrumentalness, loudness, speechiness, liveness, key, mode, time signature, dan popularity score.

## **2\. Populasi dan Karakteristik Dataset**

Populasi penelitian adalah seluruh trek musik dalam dataset Spotify yang memenuhi kriteria kelayakan analisis. Karakteristik dataset adalah sebagai berikut:

* **Total Observasi:** 1.204.022 trek musik  
* **Periode Temporal:** Tahun rilis 1920 hingga 2020 (rentang 100 tahun)  
* **Jumlah Variabel Asli:** 24 kolom (metadata \+ fitur audio)  
* **Kelengkapan Data:** 100% untuk variabel kritis (*tempo*, *energy*, *valence*, *popularity*)  
* **Diversitas Genre:** Multi-genre (pop, rock, elektronik, hip-hop, jazz, klasik, dan lainnya)  
* **Diversitas Geografis:** Cakupan global dengan representasi musik dari berbagai negara

## **3\. Unit Analisis**

Unit analisis dalam penelitian ini adalah trek musik individual. Setiap trek merepresentasikan satu observasi dengan fitur audio dan metadata yang terkait.

# **D. Variabel dan Definisi Operasional**

## **1\. Variabel Independen Utama**

**Zona Tempo (Tempo Zone)**

*Definisi Konseptual:* Kategorisasi tempo musik ke dalam lima zona diskrit berdasarkan rentang *beats per minute* (BPM).

Definisi Operasional:  
Tempo diukur dalam BPM dan dikategorisasikan sebagai berikut:

* *Very Slow:* \< 80 BPM  
* *Slow:* 80–100 BPM  
* *Medium:* 100–120 BPM (Dihipotesiskan sebagai zona optimal universal)  
* *Fast:* 120–140 BPM  
* *Very Fast:* \> 140 BPM

*Skala Pengukuran:* Nominal (kategorikal)

*Sumber Data:* Ekstraksi dari kolom `tempo` pada dataset asli, dilanjutkan dengan transformasi kategorikal melalui aturan algoritmik.

## **2\. Variabel Dependen**

Hit Probability

Definisi Konseptual: Probabilitas relatif suatu trek untuk mencapai popularitas tinggi berdasarkan kombinasi karakteristik audio yang menguntungkan.

*Definisi Operasional:*  
*Hit probability* dikalkulasi sebagai metrik komposit menggunakan formula terbobot:

\$\$\\text{hit\_probability} \= \\left(\\frac{\\text{popularity}}{100} \\times 0,4\\right) \+ (\\text{danceability} \\times 0,3) \+ (\\text{energy} \\times 0,2) \+ (\\text{balanced\_valence} \\times 0,1)\$\$

Keterangan variabel:

* `popularity`: Skor popularitas Spotify (0–100), dinormalisasi ke 0–1.  
* `danceability`: Metrik kemudahan untuk dipakai menari dari Spotify (0–1).  
* `energy`: Metrik intensitas energi dari Spotify (0–1).  
* `balanced_valence`: \$1 \- |\\text{valence} \- 0,5| \\times 2\$, mengukur kedekatan dengan kondisi emosional yang seimbang.  
  |---|  
  *Skala Pengukuran:* Rasio (kontinu, rentang 0–1)

*Justifikasi:* Skema pembobotan mencerminkan tingkat kepentingan relatif dari berbagai faktor dalam penentuan popularitas, dengan skor popularitas sebagai prediktor terkuat (40%), diikuti oleh *danceability* (30%), *energy* (20%), dan *balanced valence* (10%).

## **3\. Variabel Kontrol**

Klaster Mood (Mood Cluster)

Definisi Konseptual: Kategorisasi konten emosional musik berdasarkan dimensi energy dan valence.

Definisi Operasional:  
Mood dikategorisasikan menjadi lima klaster berdasarkan klasifikasi berbasis aturan:

1. **Happy Energetic:** \$\\text{energy} \\ge 0,6\$ DAN \$\\text{valence} \\ge 0,6\$  
2. **Sad Slow:** \$\\text{energy} \< 0,4\$ DAN \$\\text{valence} \< 0,4\$  
3. **Angry Intense:** \$\\text{energy} \\ge 0,6\$ DAN \$\\text{valence} \< 0,4\$  
4. **Calm Positive:** \$\\text{energy} \< 0,6\$ DAN \$\\text{valence} \\ge 0,6\$  
5. **Melancholic:** Kasus yang tidak termasuk kategori di atas (area tengah)

*Skala Pengukuran:* Nominal (kategorikal)

## **4\. Variabel Sekunder (untuk Analisis Korelasi)**

* **Energy:** Intensitas dan aktivitas perseptual (0–1, skala rasio).  
* **Valence:** Kepositifan nada musik (0–1, skala rasio).  
* **Danceability:** Kesesuaian untuk menari (0–1, skala rasio).  
* **Loudness:** Kerasan suara keseluruhan dalam desibel (-60 hingga 0 dB, skala interval).  
* **Acousticness:** Tingkat akustik vs elektronik (0–1, skala rasio).  
* **Decade:** Dikelompokkan berdasarkan dekade rilis (skala nominal).

# **E. Prosedur Pengumpulan Data**

## **1\. Akuisisi Data (Data Acquisition)**

Dataset diperoleh melalui pengunduhan dari platform Kaggle. Berkas `tracks_features.csv` dengan ukuran 500 MB diunduh dan disimpan dalam direktori `data/raw/`.

## **2\. Pembersihan Data (Data Cleaning)**

Proses pembersihan data dilakukan menggunakan Python dengan pustaka pandas untuk memastikan kualitas data. Langkah-langkah pembersihan meliputi:

a. Pembersihan Duplikasi: Identifikasi dan eliminasi rekaman ganda berdasarkan pengenal unik track ID.  
b. **Penanganan Nilai Hilang:** Inspeksi nilai yang hilang (*missing values*) pada variabel kritis (tempo, energy, valence, popularity). Trek dengan nilai hilang pada variabel kritis dikeluarkan dari analisis.  
c. **Deteksi Pencilan:** Identifikasi pencilan (*outliers*) pada variabel tempo (misalnya tempo \= 0 BPM atau tempo \> 300 BPM yang kemungkinan merupakan kesalahan ekstraksi). Pencilan dihapus untuk mencegah distorsi analisis.  
d. **Validasi Tipe Data:** Verifikasi tipe data untuk setiap kolom agar sesuai dengan tipe yang diharapkan (misalnya `tempo` sebagai float, popularity sebagai integer, release\_date sebagai date).  
e. **Ekstraksi Temporal:** Ekstraksi komponen tahun dari teks `release_date` untuk analisis temporal dan pengelompokan dekade.

Hasil pembersihan data disimpan dalam format Parquet (format kolom terkompresi) di `data/processed/spotify_cleaned.parquet` untuk efisiensi penyimpanan dan kecepatan pemuatan pada analisis berikutnya.

## **3\. Rekayasa Fitur (Feature Engineering)**

Fase rekayasa fitur melakukan transformasi dan pembentukan variabel turunan:

a. **Kategorisasi Zona Tempo:** Implementasi fungsi pemetaan nilai tempo kontinu ke dalam lima zona diskrit sesuai definisi operasional.def categorize\_tempo(tempo):

    if tempo \< 80:

        return 'very\_slow'

    elif 80 \<= tempo \< 100:

        return 'slow'

    elif 100 \<= tempo \<= 120:

        return 'medium'

    elif 120 \< tempo \<= 140:

        return 'fast'

    else:

        return 'very\_fast'

b. **Klasifikasi Klaster Mood:** Implementasi fungsi untuk kategorisasi mood berbasis aturan.def classify\_mood(energy, valence):

    if energy \>= 0.6 and valence \>= 0.6:

        return 'happy\_energetic'

    elif energy \< 0.4 and valence \< 0.4:

        return 'sad\_slow'

    elif energy \>= 0.6 and valence \< 0.4:

        return 'angry\_intense'

    elif energy \< 0.6 and valence \>= 0.6:

        return 'calm\_positive'

    else:

        return 'melancholic'

c. **Kalkulasi Hit Probability:** Implementasi formula terbobot sesuai definisi operasional untuk menghasilkan variabel `hit_probability`.def calculate\_hit\_probability(row):

    balanced\_valence \= 1 \- abs(row\['valence'\] \- 0.5) \* 2

    hit\_prob \= (

        row\['popularity'\] / 100 \* 0.4 \+

        row\['danceability'\] \* 0.3 \+

        row\['energy'\] \* 0.2 \+

        balanced\_valence \* 0.1

    )

    return hit\_prob

d. **Fitur Turunan Tambahan:**

* `decade`: Pengelompokan dekade (misalnya "1980s", "1990s", "2000s").  
* `energy_level`: Kategorisasi energi ke dalam tingkat rendah/sedang/tinggi.  
* `valence_level`: Kategorisasi *valence* ke dalam negatif/netral/positif.  
* `emotional_arc`: Klasifikasi kuadran *energy-valence*.

Hasil rekayasa fitur disimpan pada berkas `data/processed/spotify_master_enriched.parquet` yang berisi 44 kolom (24 kolom asli \+ 20 kolom turunan).

# **F. Instrumen Penelitian**

Penelitian ini menggunakan instrumen komputasi dan perangkat lunak sebagai berikut:

## **1\. Lingkungan Perangkat Lunak dan Pemrograman**

* **Bahasa Pemrograman:** Python 3.10+  
* **Lingkungan Pengembangan:** Jupyter Notebook / VS Code  
* **Sistem Operasi:** Windows 11 / Linux Ubuntu 20.04

## **2\. Pustaka Python**

* **Manipulasi Data:** `pandas` (versi 3.0.6) untuk operasi DataFrame, pembersihan data, dan transformasi; `numpy` (versi 2.5.3) untuk komputasi numerik dan operasi larik.  
* **Analisis Statistik:** `scipy.stats` (versi 1.14+) untuk uji statistik (*t-test*, ANOVA, *chi-square*); `statsmodels` untuk pemodelan statistik tingkat lanjut.  
* **Machine Learning:** `scikit-learn` (versi 1.3+) untuk algoritma pemodelan prediktif (*Random Forest*, *Gradient Boosting*) dan metrik evaluasi model; `xgboost` untuk implementasi *gradient boosting*.  
* **Visualisasi Data:** `matplotlib` (versi 3.8+) untuk pemplotan dasar; `seaborn` (versi 0.13+) untuk visualisasi data statistik.  
* **Penyimpanan Data:** `pyarrow` (versi 25.0.1) untuk dukungan format berkas Parquet.

## **3\. Spesifikasi Perangkat Keras**

Persyaratan perangkat keras minimum untuk pemrosesan dataset:

* **Prosesor:** Intel Core i5 atau setara (disarankan *multi-core*).  
* **RAM:** 16 GB (disarankan 32 GB untuk performa optimal).  
* **Penyimpanan:** 10 GB ruang kosong (disarankan SSD).

## **4\. Validasi Instrumen**

Validitas instrumen dalam konteks *Big Data analytics* merujuk pada reliabilitas dan akurasi dari algoritma ekstraksi serta prosedur komputasi.

Validitas Fitur Audio: Fitur audio yang digunakan (tempo, energy, valence, dll.) diekstraksi menggunakan Spotify Web API yang telah divalidasi secara luas dalam literatur ilmiah. Spotify menggunakan model *machine learning* proprietary yang dilatih pada jutaan trek dengan validasi anotasi manusia.

Reliabilitas Komputasi: Fungsi rekayasa fitur (`categorize_tempo`, `classify_mood`, `calculate_hit_probability`) diuji menggunakan sampel kasus uji (*unit test*) untuk memastikan kebenaran implementasi. Kasus-kasus batas (*edge cases*) seperti nilai batas dan data hilang diuji untuk memverifikasi penanganan data yang tangguh.

# **G. Teknik Analisis Data**

Analisis data dilakukan secara bertahap menggunakan kombinasi statistik deskriptif, statistik inferensial, dan metodologi machine learning.

## **1\. Analisis Deskriptif**

Tujuan: Memahami karakteristik dan distribusi data secara menyeluruh.

**Teknik:**

* **Distribusi Frekuensi:** Tabulasi jumlah dan proporsi untuk variabel kategorikal (zona tempo, klaster mood).  
* **Statistik Deskriptif:** Kalkulasi *mean*, *median*, standar deviasi, nilai minimum, dan maksimum untuk variabel kontinu (*hit probability*, *tempo*, *energy*, *valence*).  
* **Tabulasi Silang:** Tabel kontingensi untuk menganalisis distribusi bersama antara zona tempo dan klaster mood.  
* **Visualisasi:** Histogram, diagram batang, *box plot*, dan *violin plot* untuk representasi grafis dari distribusi data.

## **2\. Uji Validasi Hipotesis**

### **Hipotesis 1: Uji-T (Medium vs Lainnya)**

* **Hipotesis Nol (\$H\_0\$):** Tidak terdapat perbedaan signifikan dalam rata-rata *hit probability* antara zona tempo *medium* dengan zona tempo lainnya.  
* **Hipotesis Alternatif (\$H\_1\$):** Rata-rata *hit probability* zona tempo *medium* signifikan lebih tinggi dibandingkan zona tempo lainnya.  
* **Teknik Uji:** Independent samples t-test (dua arah).  
* **Formula:**

\$\$t \= \\frac{\\bar{X}\_1 \- \\bar{X}\_2}{\\sqrt{\\frac{s\_1^2}{n\_1} \+ \\frac{s\_2^2}{n\_2}}}\$\$

Keterangan:

* \$\\bar{X}\_1\$: Rata-rata *hit probability* zona tempo *medium*  
* \$\\bar{X}\_2\$: Rata-rata *hit probability* zona tempo lainnya  
* \$s\_1, s\_2\$: Standar deviasi masing-masing kelompok  
* \$n\_1, n\_2\$: Ukuran sampel masing-masing kelompok  
* **Aturan Keputusan:** Tolak \$H\_0\$ jika nilai \$p \< 0,05\$ (tingkat signifikansi \$\\alpha \= 0,05\$).

from scipy.stats import ttest\_ind

medium\_tempo \= df\[df\['tempo\_band'\] \== 'medium'\]\['hit\_probability'\]

other\_tempo \= df\[df\['tempo\_band'\] \!= 'medium'\]\['hit\_probability'\]

t\_statistic, p\_value \= ttest\_ind(medium\_tempo, other\_tempo)

### **Hipotesis 2: ANOVA (Seluruh Zona Tempo)**

* **Hipotesis Nol (\$H\_0\$):** Tidak terdapat perbedaan signifikan dalam rata-rata *hit probability* di antara seluruh lima zona tempo.  
* **Hipotesis Alternatif (\$H\_1\$):** Setidaknya satu zona tempo memiliki rata-rata *hit probability* yang berbeda secara signifikan dari zona lainnya.  
* **Teknik Uji:** One-way ANOVA (*Analysis of Variance*).  
* **Formula:**

\$\$F \= \\frac{MSB}{MSW}\$\$

Keterangan:

* \$MSB\$: *Mean Square Between Groups* (Rata-rata Kuadrat Antar Kelompok)  
* \$MSW\$: *Mean Square Within Groups* (Rata-rata Kuadrat Dalam Kelompok)  
* **Aturan Keputusan:** Tolak \$H\_0\$ jika nilai \$p \< 0,05\$.  
* **Analisis Lanjutan:** Jika hasil ANOVA signifikan, uji lanjut *Tukey HSD* (*Honestly Significant Difference*) dilakukan untuk mengidentifikasi pasangan zona tempo mana yang berbeda secara signifikan.

from scipy.stats import f\_oneway

tempo\_groups \= \[

    df\[df\['tempo\_band'\] \== zone\]\['hit\_probability'\]

    for zone in \['very\_slow', 'slow', 'medium', 'fast', 'very\_fast'\]

\]

f\_statistic, p\_value \= f\_oneway(\*tempo\_groups)

### **Hipotesis 3: Kuantifikasi Effect Size**

* **Tujuan:** Mengukur besaran efek untuk menilai signifikansi praktis di luar signifikansi statistik.  
* **Metrik:** *Cohen's d* (perbedaan rata-rata yang dibagikan dengan standar deviasi gabungan).  
* **Formula:**

\$\$d \= \\frac{\\bar{X}\_1 \- \\bar{X}*2}{s*{\\text{pooled}}}\$\$

di mana:

\$\$s\_{\\text{pooled}} \= \\sqrt{\\frac{s\_1^2 \+ s\_2^2}{2}}\$\$

* **Panduan Interpretasi:**  
  * \$|d| \< 0,2\$: Efek kecil  
  * \$0,2 \\le |d| \< 0,5\$: Efek kecil hingga sedang  
  * \$0,5 \\le |d| \< 0,8\$: Efek sedang  
  * \$|d| \\ge 0,8\$: Efek besar

import numpy as np

mean\_medium \= medium\_tempo.mean()

mean\_other \= other\_tempo.mean()

std\_pooled \= np.sqrt((medium\_tempo.std()\*\*2 \+ other\_tempo.std()\*\*2) / 2\)

cohens\_d \= (mean\_medium \- mean\_other) / std\_pooled

## **3\. Analisis Validasi Lintas Mood (Cross-Mood Validation)**

* **Tujuan:** Memverifikasi konsistensi pola zona tempo di seluruh kategori mood untuk memvalidasi hipotesis universalitas.  
* **Teknik:**  
  * **Analisis Tersetifikasi:** Mengulang uji-t untuk setiap kategori mood secara terpisah.  
  * **Pemeriksaan Konsistensi Effect Size:** Menghitung *Cohen's d* per kategori mood dan menilai homogenitasnya.  
  * **Perbandingan Visual:** Membuat diagram batang terkelompok yang menampilkan *hit probability* berdasarkan zona tempo untuk setiap mood.  
  * **Uji Konsistensi Statistik:** Melakukan uji efek interaksi (ANOVA Dua Arah) dengan zona tempo dan mood sebagai faktor.  
* **Model ANOVA Dua Arah:**

\$\$\\text{hit\_probability} \\sim \\text{tempo\_zone} \+ \\text{mood\_cluster} \+ (\\text{tempo\_zone} \\times \\text{mood\_cluster})\$\$

* **Interpretasi:**  
  * Efek utama `tempo_zone`: Efek keseluruhan dari tempo di seluruh mood.  
  * Efek utama `mood_cluster`: Efek keseluruhan dari mood di seluruh tempo.  
  * Efek interaksi: Apakah efek tempo bervariasi berdasarkan mood (jika tidak signifikan, mendukung hipotesis universalitas).

## **4\. Analisis Korelasi dan Interaksi Fitur**

**Tujuan:** Memahami hubungan antara zona tempo dan fitur audio lainnya.

**Teknik:**

* **Korelasi Pearson:** Menghitung koefisien korelasi antara *hit probability* dan fitur kontinu (*energy*, *valence*, *danceability*, *loudness*) dalam zona tempo *medium*.  
* **Perbandingan Distribusi Fitur:** Membandingkan distribusi fitur sekunder di seluruh zona tempo.  
* **Analisis Istilah Interaksi:** Menguji apakah kombinasi zona tempo dengan fitur lain meningkatkan daya prediktif.

## **5\. Pemodelan Prediktif dan Validasi**

**Tujuan:** Mendemonstrasikan kegunaan praktis dari penemuan zona tempo universal melalui peningkatan akurasi prediksi.

**Alur Kerja Pemodelan:**

### **Langkah 1: Pembagian Data (Data Split)**

from sklearn.model\_selection import train\_test\_split

X \= df\[feature\_columns\]

y \= (df\['hit\_probability'\] \> 0.5).astype(int)  \# Klasifikasi biner

X\_train, X\_test, y\_train, y\_test \= train\_test\_split(

    X, y, test\_size=0.2, random\_state=42, stratify=y

)

### **Langkah 2: Model Baseline (Tanpa Fitur Zona Tempo)**

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy\_score, precision\_score, recall\_score, f1\_score

baseline\_features \= \['energy', 'valence', 'danceability', 'loudness', 

                     'acousticness', 'tempo'\]  \# tempo sebagai variabel kontinu

model\_baseline \= RandomForestClassifier(n\_estimators=100, random\_state=42)

model\_baseline.fit(X\_train\[baseline\_features\], y\_train)

y\_pred\_baseline \= model\_baseline.predict(X\_test\[baseline\_features\])

accuracy\_baseline \= accuracy\_score(y\_test, y\_pred\_baseline)

### **Langkah 3: Model Terbooster (Dengan Fitur Zona Tempo)**

enhanced\_features \= baseline\_features \+ \['is\_medium\_tempo'\]

\# 'is\_medium\_tempo' adalah indikator biner (1 jika tempo\_band=='medium', 0 jika lainnya)

model\_enhanced \= RandomForestClassifier(n\_estimators=100, random\_state=42)

model\_enhanced.fit(X\_train\[enhanced\_features\], y\_train)

y\_pred\_enhanced \= model\_enhanced.predict(X\_test\[enhanced\_features\])

accuracy\_enhanced \= accuracy\_score(y\_test, y\_pred\_enhanced)

### **Langkah 4: Perbandingan Model**

* Menghitung peningkatan akurasi: \$\\Delta\_{\\text{accuracy}} \= \\text{accuracy\_enhanced} \- \\text{accuracy\_baseline}\$  
* Melakukan uji McNemar untuk signifikansi statistik dari perbedaan akurasi.  
* Melaporkan *precision*, *recall*, dan *F1-score* untuk kedua model.  
* Menganalisis *feature importance* untuk memverifikasi kontribusi fitur zona tempo.

**Metrik Evaluasi:**

* **Akurasi (Accuracy):** Kebenaran keseluruhan dari prediksi.  
* **Presisi (Precision):** Proporsi prediksi lagu populer yang benar-benar populer.  
* **Recall:** Proporsi lagu populer aktual yang berhasil diprediksi.  
* **F1-Score:** Rata-rata harmonik dari presisi dan *recall*.  
* **ROC-AUC:** Area di bawah kurva *Receiver Operating Characteristic*.

**Validasi Silang (Cross-Validation):**  
Menerapkan 5-*fold cross-validation* untuk memastikan ketangguhan hasil dan menghindari *overfitting*.from sklearn.model\_selection import cross\_val\_score

cv\_scores \= cross\_val\_score(model\_enhanced, X\[enhanced\_features\], y, cv=5, scoring='accuracy')

mean\_cv\_accuracy \= cv\_scores.mean()

std\_cv\_accuracy \= cv\_scores.std()

# **H. Kriteria Keputusan dan Interpretasi**

## **1\. Signifikansi Statistik**

* **Tingkat \$\\alpha \= 0,05\$:** Ambang batas keputusan untuk pengujian hipotesis.  
* **Nilai \$p \< 0,05\$:** Tolak hipotesis nol, simpulkan bahwa terdapat efek yang signifikan.  
* **Nilai \$p \\ge 0,05\$:** Gagal menolak hipotesis nol, bukti tidak cukup untuk menyimpulkan adanya efek.

## **2\. Signifikansi Praktis**

* **Cohen's \$d \\ge 0,5\$:** Efek dikategorikan signifikan secara praktis (sedang atau besar).  
* **Persentase Perbedaan \$\\ge 15%\$:** Peningkatan relatif dalam *hit probability* dianggap substansial.  
* **Peningkatan Akurasi Model \$\\ge 5%\$:** Peningkatan performa prediktif dianggap berarti.

## **3\. Kriteria Universalitas**

* **Ambang Konsistensi:** Pola zona tempo dianggap universal jika teramati pada sekurang-kurangnya 80% (4 dari 5\) kategori mood dengan arah efek yang konsisten.  
* **Efek Interaksi:** Istilah interaksi yang tidak signifikan (\$p \> 0,05\$) dalam ANOVA Dua Arah mendukung hipotesis universalitas.

---

# **DAFTAR PUSTAKA**

Dhanaraj, R., & Logan, B. (2005). Automatic prediction of hit songs. *Proceedings of the 6th International Conference on Music Information Retrieval (ISMIR)*, 488-491.

Dhar, S., Chowdhury, T., Samanta, D., & Roy, A. (2019). Music popularity prediction using machine learning with hybrid audio and social features. *Expert Systems with Applications*, 133, 11-20. https://doi.org/10.1016/j.eswa.2019.05.011

Fraisse, P. (1982). Rhythm and tempo. *The Psychology of Music*, 149-180.

Grahn, J. A., & Brett, M. (2007). Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906.

Husain, G., Thompson, W. F., & Schellenberg, E. G. (2002). Effects of musical tempo and mode on arousal, mood, and spatial abilities. *Music Perception*, 20(2), 151-171.

Interiano, M., Kazemi, K., Wang, L., Yang, J., Yu, Z., & Komarova, N. L. (2018). Musical trends and predictability of success in contemporary songs in and out of the top charts. *Royal Society Open Science*, 5(5), 171274. https://doi.org/10.1098/rsos.171274

Laney, D. (2001). 3D data management: Controlling data volume, velocity and variety. *META Group Research Note*, 6(70).

Moelants, D. (2002). Preferred tempo reconsidered. *Proceedings of the 7th International Conference on Music Perception and Cognition*, 580-583.

Müller, M. (2015). *Fundamentals of music processing: Audio, analysis, algorithms, applications*. Springer.

Ni, Y., Santos-Rodríguez, R., McVicar, M., & De Bie, T. (2011). Hit song science once again a science? *Proceedings of the 4th International Workshop on Machine Learning and Music*, 1-5.

Percino, G., Klimek, P., & Thurner, S. (2014). Instrumental complexity of music genres and why simplicity sells. *PLoS ONE*, 9(12), e115255. https://doi.org/10.1371/journal.pone.0115255

Schedl, M., Zamani, H., Chen, C. W., Deldjoo, Y., & Elahi, M. (2018). Current challenges and visions in music recommender systems research. *International Journal of Multimedia Information Retrieval*, 7(2), 95-116.

Van Dyck, E., Moens, B., Buhmann, J., Demey, M., Coorevits, E., Bella, S. D., & Leman, M. (2017). Spontaneous entrainment of running cadence to music tempo. *Sports Medicine - Open*, 3, 15. https://doi.org/10.1186/s40798-017-0082-8

---

# **LAMPIRAN**

## **Lampiran 1: Statistik Deskriptif Dataset**

```
Total Tracks: 1,204,022
Time Range: 1920 - 2020 (100 years)
Original Features: 24 columns
Derived Features: 20 columns
Total Features: 44 columns
Data Completeness: 100% (no missing values in critical fields)
```

## **Lampiran 2: Distribusi Zona Tempo**

```
Tempo Zone Distribution:
- Very Slow (<80 BPM):     126,953 tracks (10.5%)
- Slow (80-100 BPM):       258,657 tracks (21.5%)
- Medium (100-120 BPM):    266,775 tracks (22.2%)
- Fast (120-140 BPM):      286,576 tracks (23.8%)
- Very Fast (>140 BPM):    265,061 tracks (22.0%)
```

## **Lampiran 3: Distribusi Klaster Mood**

```
Mood Cluster Distribution:
- Sad Slow:           384,322 tracks (31.9%)
- Melancholic:        238,910 tracks (19.8%)
- Angry Intense:      229,124 tracks (19.0%)
- Happy Energetic:    214,444 tracks (17.8%)
- Calm Positive:      137,222 tracks (11.4%)
```

## **Lampiran 4: Temuan Awal (Fase Eksploratif)**

```
Validasi Zona Tempo Sweet Spot Universal (Temuan Awal):
======================================================================
MOOD                 BEST TEMPO      HIT PROB     SAMPLE SIZE
----------------------------------------------------------------------
Happy Energetic      Medium          0.7624        49,245
Sad Slow             Medium          0.3626        77,279
Angry Intense        Medium          0.6363        49,313
Calm Positive        Medium          0.5561        36,166
Melancholic          Medium          0.6067        54,772

→ 5/5 moods prefer medium tempo (100-120 BPM)
```

## **Lampiran 5: Lokasi Script dan Data**

```
Direktori Proyek: D:\Semester 5\BIG DATA\Project\

File Data:
- data/raw/tracks_features.csv (dataset asli)
- data/processed/spotify_cleaned.parquet (data hasil pembersihan)
- data/processed/spotify_master_enriched.parquet (data analisis utama)

Script Analisis:
- scripts/01_load_and_clean_data.py (pembersihan data)
- scripts/02_feature_engineering.py (pembuatan fitur)
- scripts/06_discover_hypotheses.py (analisis eksploratif)
- scripts/07_validate_tempo_hypothesis.py (validasi statistik)

Dokumentasi:
- SEMPRO_READINESS.md (laporan penelitian)
- TEMPO_SWEET_SPOT_GUIDE.md (panduan komprehensif)
```

---

**CATATAN:**  
Proposal ini telah disusun sesuai dengan Pedoman Tugas Akhir UNESA Edisi III Tahun 2025 dengan memperhatikan kaidah tata tulis ilmiah, struktur paragraf (1 ide pokok + minimal 2 ide pendukung), penggunaan bahasa ilmiah baku, dan penghindaran penggunaan persona (kata ganti orang pertama/kedua).

**DEKLARASI PENGGUNAAN AI:**  
Penyusunan draf proposal ini menggunakan bantuan *Artificial Intelligence* (AI) Assistant untuk *structuring*, *formatting*, dan *language refinement*. Konten substansial, metodologi, dan data penelitian merupakan hasil kerja penelitian aktual. Penggunaan AI telah dideklarasikan sesuai Form Pernyataan Penggunaan AI (Lampiran 21 Pedoman UNESA).

---

**END OF PROPOSAL**
