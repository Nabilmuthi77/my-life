MASTER PROMPT — BUILD "MY LIFE" ANDROID APP

Python Flet | Premium Neumorphism | Local JSON | Android APK

Bertindaklah sebagai Senior Python Developer, Mobile UI/UX Designer, Software Architect, dan QA Engineer.

Tugasmu adalah membangun aplikasi Android bernama My Life menggunakan Python dan Flet ("flet") dengan implementasi yang benar-benar berfungsi, bukan sekadar prototype atau tampilan statis.

Bekerjalah langsung di workspace Antigravity IDE. Buat dan edit file proyek yang diperlukan, jalankan aplikasi, uji logika, perbaiki error, dan siapkan konfigurasi build APK.

Jangan berhenti setelah membuat mockup atau kode awal. Selesaikan implementasi hingga seluruh fitur utama dapat digunakan.

---

1. IDENTITAS DAN TUJUAN APLIKASI

Nama aplikasi: My Life

Tagline: "Progress, not perfection."

My Life adalah aplikasi self-improvement untuk memantau lima aspek kehidupan setiap hari menggunakan skor 0–10.

Lima aspek wajib:

1. JIWA
   Deskripsi: Mendekati Sang Pencipta
   Icon: simbol spiritual yang netral dan elegan.

2. RAGA
   Deskripsi: Menjaga tubuh
   Icon: heart atau health.

3. EMOSIONAL
   Deskripsi: Mengendalikan diri
   Icon: self-awareness atau psychology.

4. PRINSIPAL
   Deskripsi: Menjaga prinsip
   Icon: target atau compass.

5. FINANSIAL
   Deskripsi: Mengelola keuangan
   Icon: wallet atau account balance.

Bahasa antarmuka: Bahasa Indonesia.

Target utama: Android, dengan kemampuan menjalankan aplikasi melalui desktop/web selama pengembangan menggunakan Flet.

Prioritas:

1. Semua business rules benar.
2. Data tidak mudah hilang atau rusak.
3. UI sangat rapi, konsisten, dan responsif.
4. APK dapat dibangun dengan workflow yang terdokumentasi.

Jangan mengorbankan fungsionalitas demi tampilan.

---

2. REFERENSI VISUAL: NEUMORPHISM MODERN

Gunakan gambar referensi yang saya lampirkan sebagai acuan utama bahasa visual.

Saya ingin desain soft neumorphism / soft UI modern, bukan desain flat biasa, bukan material design standar, bukan glassmorphism, dan bukan skeuomorphism jadul.

Karakter visual yang wajib:

- Background dan komponen memiliki warna dasar yang sama atau sangat berdekatan.
- Kartu terlihat menyatu dengan permukaan background, tetapi timbul melalui soft shadow.
- Tombol memiliki ilusi pressed/raised yang halus.
- Gunakan kombinasi highlight terang dan bayangan gelap lembut dari arah berlawanan.
- Radius sudut konsisten, umumnya 16–26 px.
- Padding lega dan ritme spacing konsisten.
- Gunakan tipografi sans-serif modern, seperti Inter atau font sistem yang bersih.
- Gunakan ikon sederhana, konsisten, dan mudah dikenali.
- Animasi ringan saat interaksi, tanpa efek berlebihan.
- Hierarki visual harus jelas: judul, skor, label, progres, dan kontrol.
- Hindari terlalu banyak border. Jika menggunakan border, buat sangat tipis dan low-contrast.
- Jangan memberikan shadow tebal atau hitam pekat.
- Jangan membuat semua komponen tampak seperti tombol mengambang.
- Gunakan efek pressed/inset untuk komponen tertentu, terutama progress bar, toggle, dan tombol yang sedang aktif.
- Hindari gradient berlebihan, glass effect, tekstur, noise, dan dekorasi yang tidak mendukung fungsi.
- Jangan membuat tampilan seperti dashboard admin atau template aplikasi generik.

PENTING: desain harus terlihat seperti produk digital premium yang benar-benar dirancang dengan sengaja, bukan hasil generate UI generik.

2A. LIGHT THEME — PURE WHITE NEUMORPHISM

Light theme harus benar-benar putih dan monokrom.

Palet dasar:

- Background utama: "#F5F7FA" atau putih sangat bersih.
- Permukaan kartu: "#F5F7FA" atau "#FFFFFF".
- Permukaan tombol: mengikuti warna permukaan induknya.
- Teks utama: "#17212B".
- Teks sekunder: "#667085".
- Ikon netral: "#526171".
- Shadow terang: "#FFFFFF".
- Shadow gelap: "#D9E0E8".
- Accent utama: "#238D91" atau teal yang sangat terkontrol.
- Garis pemisah, jika dibutuhkan: "#E7ECF2".

ATURAN:

- Tidak boleh menggunakan cokelat, beige, krem, tan, atau aksen earth-tone.
- Jangan memberikan setiap aspek warna latar yang berbeda.
- Jangan menjadikan kartu merah, ungu, kuning, atau hijau terang.
- Ikon aspek boleh memakai sedikit aksen warna yang konsisten dan redup jika membantu identifikasi, tetapi permukaan kartu tetap monokrom.
- Skor utama harus berwarna gelap dan mudah dibaca.
- Shadow harus lembut, modern, dan tidak berlebihan.

Contoh raised shadow:

- Offset positif: sekitar "(5, 5)".
- Offset negatif: sekitar "(-5, -5)".
- Blur radius: sekitar "12–20".
- Opacity disesuaikan agar halus.

Sesuaikan implementasi dengan API Flet yang benar. Jika dua shadow pada satu elemen tidak didukung langsung, gunakan wrapper/container berlapis atau teknik lain yang kompatibel.

2B. DARK THEME — DEEP TEAL / BLUE-GREEN NEUMORPHISM

Dark theme menggunakan palet gelap yang menyatu.

Palet:

- Background utama: "#071A20".
- Surface utama: "#0B252D".
- Surface elevated: "#10313A".
- Surface pressed: "#06151A".
- Teks utama: "#F4FAFC".
- Teks sekunder: "#A9C0C8".
- Accent teal: "#36D6C0".
- Accent blue: "#48A9FF".
- Shadow gelap: "#041116".
- Highlight: "#163944".

ATURAN:

- Jangan menggunakan background abu-abu terang atau putih pada dark mode.
- Jangan menggunakan aksen cokelat.
- Seluruh dashboard, kartu, tombol, grafik, dan pengaturan harus mengikuti tema gelap.
- Teks utama putih atau near-white.
- Shadow gelap dan highlight biru-hijau harus menghasilkan efek depth yang lembut.
- Accent digunakan secara terkontrol untuk progres, status aktif, dan elemen penting.
- Hindari neon berlebihan yang membuat aplikasi terlihat seperti gaming dashboard.

2C. AUTO THEME

Sediakan tiga pilihan:

- Putih
- Gelap
- Auto

Auto harus mengikuti preferensi light/dark sistem perangkat jika platform menyediakan informasinya.

Implementasikan deteksi menggunakan API Flet yang valid, termasuk "page.platform_brightness" jika didukung oleh versi yang dipakai.

Jangan mengasumsikan API tersedia tanpa memeriksa versi Flet.

Jika platform tidak menyediakan brightness, gunakan fallback yang aman dan dokumentasikan perilakunya.

Saat preferensi tema diganti:

- Simpan pilihan ke JSON.
- Terapkan tema ke seluruh UI.
- Perbarui warna kartu, teks, ikon, grafik, tombol, navigasi, dan dialog.
- Jangan mengubah skor, progres, atau riwayat.
- Jangan mengharuskan aplikasi ditutup dan dibuka kembali.
- Jika perangkat mendukung perubahan brightness saat aplikasi berjalan, Auto harus memperbarui UI ketika brightness berubah.

Default preferensi tema: "auto".

---

3. STRUKTUR LAYAR DAN NAVIGASI

Buat aplikasi dengan bottom navigation yang terdiri dari:

1. Beranda
2. Riwayat
3. Pengaturan

Gunakan layout mobile-first, responsif, dan scrollable.

Target lebar desain utama sekitar 360–430 dp, tetapi jangan mengunci layout agar tidak berfungsi pada layar lain.

Gunakan safe area atau padding yang sesuai agar konten tidak tertutup status bar, navigation bar, atau keyboard.

3A. SPLASH SCREEN

Buat splash screen sederhana dan premium.

Isi:

- Logo berupa simbol daun atau pertumbuhan.
- Teks "My Life".
- Tagline "Progress, not perfection."
- Background menggunakan tema yang dipilih atau tema default yang konsisten.
- Transisi masuk singkat dan halus jika didukung.

Splash screen tidak boleh menahan pengguna terlalu lama.

3B. BERANDA / DASHBOARD

Header:

- Logo kecil atau nama "My Life".
- Tanggal hari ini dalam Bahasa Indonesia.
- Kalimat pendek: "Jadi 1% lebih baik setiap hari."
- Tombol atau kontrol pemilihan tema yang ringkas.

Summary card:

- Label "RATA-RATA HARI INI".
- Rata-rata dari lima skor, format satu angka desimal.
- Skor total dengan format "jumlah/50".
- Indikator visual yang menunjukkan kondisi keseluruhan.

Contoh:
Rata-rata "2.2/10"
Total "11/50"

Rumus:
"average = sum(scores.values()) / 5"

Di bawah summary tampilkan judul:
"Lima pilar hidup"

Kemudian lima kartu aspek dengan desain konsisten.

Setiap kartu aspek wajib memiliki:

- Ikon aspek.
- Nama aspek.
- Deskripsi singkat.
- Skor besar, misalnya "3/10".
- Tombol minus yang mudah ditekan.
- Tombol plus yang mudah ditekan.
- Indikator progres klik "0/10".
- Progress bar atau sepuluh dot.
- Animasi feedback ringan saat tombol digunakan.
- State disabled atau feedback yang sesuai saat batas skor tercapai.

Kartu tidak boleh terlalu padat.

Tombol plus dan minus harus memiliki touch target nyaman, idealnya sekitar 44–48 dp.

Ketika pengguna mengklik tombol:

- Perbarui UI segera.
- Simpan perubahan ke JSON.
- Update summary.
- Update grafik/riwayat yang relevan.
- Berikan feedback visual yang elegan.
- Jangan membuat tombol berpindah posisi ketika angka berubah.

3C. DETAIL ASPEK

Jika memungkinkan, pengguna dapat mengetuk kartu untuk membuka halaman detail aspek.

Tampilkan:

- Nama dan deskripsi aspek.
- Skor saat ini.
- Visual skor 0–10.
- Progres klik 0–10.
- Tombol plus dan minus.
- Riwayat skor aspek tersebut.
- Ringkasan aktivitas aspek hari ini.

Halaman detail menggunakan tema dan bahasa visual yang sama.

3D. HALAMAN RIWAYAT

Tampilkan histori tujuh hari terakhir.

Wajib ada:

- Grafik skor harian.
- Daftar tanggal.
- Rata-rata skor per tanggal.
- Total skor per tanggal.
- Kemampuan melihat detail skor lima aspek pada tanggal tertentu jika memungkinkan.

Grafik harus benar-benar memakai data yang disimpan, bukan data dummy.

Gunakan "LineChart" atau "BarChart" Flet sesuai dukungan versi yang dipakai.

Rekomendasi:

- Grafik utama menunjukkan rata-rata lima aspek per hari.
- Sumbu Y: 0–10.
- Sumbu X: tanggal.
- Maksimal tujuh tanggal.
- Tooltip atau label nilai jika didukung.
- Grafik mengikuti light/dark theme.
- Empty state yang bagus ketika riwayat belum tersedia.

Riwayat harus tetap benar ketika aplikasi tidak dibuka selama beberapa hari.

3E. AKTIVITAS TERBARU

Buat daftar aktivitas yang menampilkan:

- Nama aspek.
- Jenis aksi: progres bertambah, poin bertambah, atau poin berkurang.
- Waktu dan tanggal.
- Skor setelah aksi.
- Progres klik setelah aksi.

Contoh:
"Jiwa — Progres +1"
"Raga — Poin -1"
"Emosional — Mendapat +1 poin"

Urutkan dari yang terbaru.

Sediakan empty state ketika belum ada aktivitas.

3F. PENGATURAN

Tampilkan pilihan tema dalam bentuk kontrol yang jelas:

- Putih
- Gelap
- Auto

Tampilkan pilihan aktif secara visual.

Tambahkan bagian:

- Tentang aplikasi.
- Versi aplikasi.
- Informasi penyimpanan lokal.
- Backup data JSON.
- Reset data.

Reset data wajib memakai dialog konfirmasi sebelum menghapus atau mengembalikan data.

Jangan menghapus data tanpa persetujuan pengguna.

Jika memungkinkan, sediakan ekspor backup JSON melalui mekanisme file picker/share yang kompatibel dengan Android.

---

4. BUSINESS RULES — JANGAN ADA YANG TERLEWAT

Semua aturan berikut wajib diimplementasikan dengan benar.

4A. RANGE SKOR

Lima skor utama:

- Minimum 0.
- Maksimum 10.
- Harus berupa integer.

Tidak boleh ada skor negatif atau di atas 10, baik melalui UI maupun manipulasi data.

4B. TOMBOL MINUS

Ketika pengguna menekan minus:

- Skor aspek tersebut langsung berkurang 1.
- Minimum 0.
- Jika skor sudah 0, jangan dikurangi lagi.
- Berikan feedback visual yang wajar.
- Catat aktivitas klik walaupun skor tidak berubah, dengan hasil yang jelas.
- Progress klik tidak otomatis bertambah.

Keputusan penting:
Tombol minus tidak mengurangi counter progres. Counter progres hanya berubah akibat tombol plus, kecuali aturan tersebut diubah secara eksplisit di masa depan.

4C. TOMBOL PLUS

Klik plus tidak langsung menambah skor utama.

Setiap klik plus menambah counter progres aspek sebanyak 1.

Urutannya:

- 0/10 → 1/10
- 1/10 → 2/10
- ...
- 9/10 → klik ke-10 menghasilkan 1 poin utama dan progres kembali menjadi 0/10.

Ketika progres mencapai 10:

1. Tambahkan skor utama sebanyak 1, maksimum 10.
2. Reset progres aspek menjadi 0.
3. Catat aktivitas sebagai poin berhasil diperoleh.
4. Simpan data.
5. Update UI dan summary.

Jika skor utama sudah 10:

- Jangan memberikan poin di atas 10.
- Jangan membiarkan progres terus menumpuk menjadi poin yang tidak dapat digunakan.
- Pilih perilaku konsisten: nonaktifkan tombol plus atau berikan feedback bahwa skor sudah maksimal.
- Dokumentasikan perilaku tersebut.

Jangan pernah membuat counter mencapai 10 lalu tetap menyimpannya setelah poin berhasil diberikan.

4D. PENGURANGAN OTOMATIS HARIAN

Setiap pergantian tanggal kalender lokal, semua lima skor utama berkurang 1.

Aturan:

- Pengurangan maksimal satu kali per tanggal yang terlewati.
- Skor minimum tetap 0.
- Progress klik tidak ikut berkurang.
- Pengurangan harus tetap dihitung jika aplikasi tidak dibuka selama beberapa hari.
- Gunakan "last_date" yang disimpan dalam JSON.
- Jangan hanya bergantung pada timer yang berjalan saat aplikasi aktif.
- Jalankan pemeriksaan saat aplikasi mulai.
- Jika memungkinkan, periksa lagi ketika aplikasi kembali aktif setelah berada di background.

Contoh:
Tanggal 22:
Jiwa 3, Raga 4, Emosional 2, Prinsipal 2, Finansial 0.

Tanggal 23:
Jiwa 2, Raga 3, Emosional 1, Prinsipal 1, Finansial 0.

Tanggal 24:
Jiwa 1, Raga 2, Emosional 0, Prinsipal 0, Finansial 0.

Jika aplikasi baru dibuka tanggal 24, terapkan dua kali pengurangan dari tanggal 22 sampai kondisi tanggal 24.

PENTING:
Definisikan dengan jelas kapan snapshot skor dibuat. Skor tanggal lama harus disimpan sebelum pengurangan untuk tanggal berikutnya.

Jangan:

- Mengurangi skor berkali-kali pada hari yang sama.
- Mengurangi skor akibat aplikasi di-refresh pada hari yang sama.
- Menghapus progres klik akibat pergantian tanggal.
- Menggandakan pengurangan akibat dua proses startup.
- Menulis history tanggal yang sama berkali-kali dengan hasil berbeda tanpa kebijakan yang jelas.

Gunakan tanggal lokal perangkat dan ISO format "YYYY-MM-DD".

4E. DEFINISI RIWAYAT HARIAN

Riwayat harus merepresentasikan kondisi akhir hari yang konsisten.

Rekomendasi implementasi:

- Simpan snapshot skor hari sebelumnya sebelum pengurangan harian diterapkan.
- Snapshot tanggal yang sama di-upsert, bukan diduplikasi.
- Jika aplikasi digunakan hari ini, update snapshot hari ini setelah perubahan skor.
- Saat tanggal berubah, finalisasi hari sebelumnya, lalu inisialisasi snapshot hari baru.
- Riwayat tujuh hari dihitung dari tanggal kalender, bukan sekadar tujuh item terakhir.
- Jika ada hari tanpa interaksi, tanggal tersebut tetap boleh tampil dengan skor terakhir sesuai aturan pengurangan otomatis.

Tentukan dan implementasikan semantik ini secara konsisten di seluruh aplikasi.

---

5. LOCAL DATA STORAGE — JSON

File utama:

"my_life_data.json"

Data harus tersimpan secara lokal dan persisten.

PENTING UNTUK ANDROID:
Jangan berasumsi bahwa "Path.home()" atau current working directory merupakan lokasi penyimpanan aplikasi yang aman atau persisten pada APK.

Gunakan lokasi penyimpanan aplikasi yang sesuai dengan Android dan versi Flet yang digunakan, misalnya application data directory atau API penyimpanan yang direkomendasikan oleh Flet.

Pastikan file dapat dibaca dan ditulis setelah aplikasi dibuka ulang.

Untuk mode desktop/dev, gunakan lokasi lokal yang masuk akal.

Jangan menulis ke direktori instalasi aplikasi yang tidak memiliki izin tulis.

Contoh struktur JSON:

{
"last_date": "2026-10-22",
"scores": {
"jiwa": 3,
"raga": 4,
"emosional": 2,
"prinsipal": 2,
"finansial": 0
},
"progress": {
"jiwa": 5,
"raga": 2,
"emosional": 0,
"prinsipal": 4,
"finansial": 0
},
"history": [
{
"date": "2026-10-22",
"jiwa": 3,
"raga": 4,
"emosional": 2,
"prinsipal": 2,
"finansial": 0
}
],
"click_history": [],
"theme": "auto"
}

Format timestamp aktivitas sebaiknya ISO 8601.

Boleh menambahkan field versi schema, misalnya "schema_version", jika diperlukan untuk migrasi data.

5A. INITIAL DATA

Saat instalasi pertama dan belum ada file data, gunakan nilai awal:

Tanggal referensi: 22 Oktober 2026.

- Jiwa: 3.
- Raga: 4.
- Emosional: 2.
- Prinsipal: 2.
- Finansial: 0.

Progress awal semua aspek: 0.

Theme awal: "auto".

Jangan menginisialisasi ulang skor contoh setiap kali aplikasi dibuka.

Data contoh hanya boleh dipakai ketika file belum ada atau ketika pengguna secara eksplisit melakukan reset ke data awal.

Jika tanggal aktual lebih baru dari tanggal referensi, pengurangan harian harus diterapkan sesuai aturan.

5B. DATA INTEGRITY

Implementasikan:

- JSON parsing dengan error handling.
- Default untuk field yang hilang.
- Validasi tipe dan range.
- Backup atau pemulihan aman jika file JSON rusak.
- Atomic write menggunakan temporary file dan replace jika didukung.
- Hindari menimpa data valid dengan default hanya karena ada satu field yang hilang.
- Hindari duplikasi riwayat.
- Batasi panjang click history secara wajar, misalnya 500–1000 aktivitas terbaru.
- Simpan perubahan penting segera setelah aksi.
- Jangan mengandalkan memori aplikasi sebagai satu-satunya sumber data.

---

6. ARSITEKTUR DAN KUALITAS KODE

Gunakan Python dan Flet.

Entry point wajib:
"main.py"

Fungsi utama:
"main(page: ft.Page)"

Gunakan satu file "main.py" untuk implementasi utama sesuai kebutuhan proyek. File konfigurasi build dan dependency boleh terpisah.

Pisahkan tanggung jawab ke fungsi yang jelas, misalnya:

- "load_data()"
- "save_data()"
- "validate_data()"
- "apply_daily_decay()"
- "snapshot_daily_scores()"
- "change_score()"
- "record_activity()"
- "calculate_average()"
- "build_dashboard()"
- "build_history_page()"
- "build_settings_page()"
- "apply_theme()"

Nama fungsi boleh disesuaikan dengan arsitektur yang lebih baik.

Gunakan satu sumber kebenaran untuk state data.

Hindari:

- Duplikasi logika bisnis pada setiap kartu.
- Global mutable state yang tidak diperlukan.
- Hardcode warna di banyak lokasi.
- Callback yang menangkap nilai lama secara tidak sengaja.
- Membuat ulang handler yang menyebabkan klik ganda.
- Menggunakan API Flet yang sudah deprecated tanpa alasan.
- Membuat UI yang terlihat benar tetapi tidak terhubung ke data.

Gunakan centralized theme configuration agar seluruh komponen otomatis mengikuti tema.

Pastikan implementasi kompatibel dengan versi Flet yang dipilih. Periksa dokumentasi/API yang relevan dan lakukan smoke test daripada menebak nama properti atau enum.

---

7. ANIMASI DAN INTERAKSI

Buat animasi ringan dan elegan:

- Tombol plus/minus memberikan feedback pressed.
- Kartu memberikan feedback saat disentuh.
- Transisi navigasi halus.
- Progress bar bergerak ketika nilainya berubah.
- Skor memiliki transisi singkat saat bertambah atau berkurang.
- Theme switch memiliki transisi yang tidak mengganggu.

Gunakan API animasi Flet yang benar untuk versi terpilih.

Jika scale animation kompleks tidak stabil di Flet, gunakan alternatif sederhana yang reliable. Jangan membuat implementasi animasi merusak interaksi.

Aplikasi harus tetap responsif pada perangkat Android kelas menengah.

---

8. BUILD ANDROID APK VIA GITHUB ACTIONS

Buat file:

".github/workflows/build.yml"

Workflow wajib:

- Trigger saat push ke branch utama.
- Mendukung "workflow_dispatch".
- Menggunakan Ubuntu runner.
- Setup Python 3.11.
- Setup Java yang kompatibel dengan toolchain Flet build yang dipilih.
- Install dependencies.
- Jalankan "flet build apk -v".
- Upload file APK sebagai GitHub Actions artifact.
- Gagal secara jelas jika APK tidak dihasilkan.

Gunakan versi GitHub Actions yang sesuai dan tidak deprecated.

Buat "requirements.txt" yang sesuai dengan versi Flet yang benar-benar digunakan.

Periksa kebutuhan Android SDK, Java, Gradle, Flutter, dan dependensi build sesuai dokumentasi Flet terkini. Jangan mengasumsikan bahwa memasang Java dan Flet saja pasti cukup.

Jika diperlukan, tambahkan konfigurasi project/build Flet yang valid.

Pastikan aplikasi memiliki:

- Nama aplikasi My Life.
- Package identifier yang valid dan konsisten.
- Ikon aplikasi jika aset memungkinkan.
- Konfigurasi Android yang dibutuhkan untuk build.

Jangan mengklaim APK berhasil dibuat sebelum workflow atau perintah build benar-benar berhasil.

---

9. PENGUJIAN WAJIB

Buat pengujian logika otomatis jika memungkinkan, misalnya menggunakan "unittest" untuk business rules.

Minimal uji skenario berikut.

TEST 1 — PLUS NORMAL:
Skor Jiwa 3, progres 0.
Klik plus satu kali.
Hasil: skor 3, progres 1.

TEST 2 — PLUS KESEPULUH:
Skor Jiwa 3, progres 9.
Klik plus satu kali.
Hasil: skor 4, progres 0.

TEST 3 — SKOR MAKSIMUM:
Skor Jiwa 10.
Klik plus.
Hasil: skor tetap 10, tidak ada poin tambahan yang bisa ditimbun.

TEST 4 — MINUS NORMAL:
Skor Raga 4.
Klik minus.
Hasil: skor 3.

TEST 5 — MINUS DI NOL:
Skor Finansial 0.
Klik minus.
Hasil: skor tetap 0.

TEST 6 — DAILY DECAY:
Tanggal terakhir 22 Oktober, skor Jiwa 3.
Tanggal sekarang 24 Oktober.
Hasil skor Jiwa 1, dengan snapshot tanggal yang benar.

TEST 7 — DAILY DECAY DI NOL:
Skor 0 melewati beberapa hari.
Hasil tetap 0.

TEST 8 — PROGRESS SAAT GANTI HARI:
Progress Jiwa 6.
Pergantian hari.
Hasil progress tetap 6, sedangkan skor utama berkurang sesuai aturan.

TEST 9 — NO DOUBLE DECAY:
Jalankan pemeriksaan pergantian hari dua kali pada tanggal yang sama.
Hasil tidak ada pengurangan kedua.

TEST 10 — HISTORY:
Pastikan setiap tanggal memiliki maksimal satu snapshot yang valid dan urutan tanggal benar.

TEST 11 — PERSISTENCE:
Ubah skor, simpan, muat ulang JSON.
Pastikan skor, progres, tema, dan aktivitas tetap benar.

TEST 12 — THEME:
Ubah Putih → Gelap → Auto.
Pastikan semua komponen berubah tema tanpa mengubah data pengguna.

TEST 13 — CORRUPT JSON:
Simulasikan file rusak.
Pastikan aplikasi tidak crash tanpa penanganan dan memberikan pemulihan aman.

TEST 14 — EMPTY HISTORY:
Aplikasi tetap terlihat rapi jika belum memiliki cukup riwayat.

TEST 15 — RESPONSIVE:
Pastikan konten dapat di-scroll dan tidak terpotong pada lebar layar ponsel yang umum.

---

10. ACCEPTANCE CRITERIA

Pekerjaan baru dianggap selesai jika:

1. "main.py" dapat dijalankan dengan "flet run main.py".
2. Dashboard menampilkan lima aspek.
3. Semua skor dan progres menggunakan data nyata.
4. Semua aturan plus/minus benar.
5. Daily decay tidak berlipat ganda.
6. Riwayat tujuh hari konsisten.
7. Tema Putih benar-benar putih, tanpa cokelat/beige.
8. Tema Gelap benar-benar deep teal/blue-green dengan teks terang.
9. Auto mengikuti brightness perangkat jika tersedia.
10. Preferensi tema tersimpan.
11. Data tetap ada setelah aplikasi ditutup dan dibuka kembali.
12. UI responsif, scrollable, dan tidak mengalami overflow.
13. Tidak ada tombol utama yang hanya dekoratif.
14. Reset data membutuhkan konfirmasi.
15. Workflow GitHub Actions tersedia dan konfigurasi build valid.
16. Pengujian business rules berhasil.
17. Error yang ditemukan sudah diperbaiki atau didokumentasikan secara jujur.

---

11. CARA KERJA YANG SAYA INGINKAN

Lakukan secara berurutan:

FASE 1 — INSPEKSI

- Periksa isi workspace.
- Identifikasi versi Python dan Flet yang digunakan.
- Baca dokumentasi yang relevan.
- Buat rencana implementasi singkat.

FASE 2 — IMPLEMENTASI

- Buat atau perbarui main.py.
- Buat requirements.txt.
- Buat konfigurasi build Flet jika diperlukan.
- Buat workflow GitHub Actions.
- Buat pengujian business rules.

FASE 3 — VALIDASI

- Jalankan pemeriksaan sintaks.
- Jalankan unit tests.
- Jalankan smoke test Flet.
- Uji JSON persistence dan daily decay.
- Periksa semua tema.
- Periksa layout responsif.
- Perbaiki seluruh error yang dapat diperbaiki.

FASE 4 — FINALISASI

- Tampilkan struktur proyek akhir.
- Jelaskan file yang dibuat.
- Berikan perintah menjalankan aplikasi.
- Berikan perintah build APK.
- Jelaskan cara mengambil APK dari GitHub Actions.
- Laporkan hasil pengujian secara faktual.
- Sebutkan masalah yang belum terselesaikan, jika ada.

Jangan hanya memberikan tutorial atau potongan kode. Kerjakan langsung di workspace jika tool memungkinkan.

Jangan menghapus file proyek pengguna yang tidak relevan.

Jangan mengganti requirement inti dengan implementasi yang lebih mudah tetapi berbeda perilaku.

Jika ada detail teknis yang ambigu, pilih implementasi paling aman dan konsisten, dokumentasikan keputusan, lalu lanjutkan tanpa menunggu konfirmasi untuk hal-hal nonkritis.

HASIL AKHIR YANG DIHARAPKAN:
Aplikasi My Life yang berfungsi penuh, memiliki desain premium neumorphic seperti referensi, menyimpan data secara lokal, mematuhi semua business rules, dan memiliki jalur build APK Android yang dapat diuji.