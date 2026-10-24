# My Life — Android & Desktop Self-Improvement App

> *"Progress, not perfection."*

**My Life** adalah aplikasi self-improvement mobile (Android APK & Desktop) yang dibangun menggunakan **Python** dan **Flet 1.0**. Aplikasi ini memantau lima pilar aspek kehidupan setiap hari menggunakan skor 0–10, dilengkapi desain **Modern Soft Neumorphism**, penyimpanan lokal JSON persisten, pengurangan otomatis harian (*daily decay*), grafik 7 hari, dan alur build otomatis APK via GitHub Actions.

---

## 🌟 Lima Pilar Aspek Hidup

| Pilar | Deskripsi | Aksen Light | Aksen Dark | Ikon |
| :--- | :--- | :--- | :--- | :--- |
| **JIWA** | Mendekati Sang Pencipta | `#238D91` | `#36D6C0` | `SELF_IMPROVEMENT` |
| **RAGA** | Menjaga tubuh | `#E05D5D` | `#FF6B81` | `FAVORITE` |
| **EMOSIONAL** | Mengendalikan diri | `#5D7CE0` | `#6C9BFF` | `PSYCHOLOGY` |
| **PRINSIPAL** | Menjaga prinsip | `#E08C38` | `#FFAA5C` | `EXPLORE` |
| **FINANSIAL** | Mengelola keuangan | `#2CA56E` | `#48E59B` | `ACCOUNT_BALANCE_WALLET` |

---

## 🎨 Visual & Desain: Soft Neumorphism

- **Light Mode (Pure White Neumorphism)**:
  - Background utama: `#F5F7FA`
  - Permukaan kartu: `#F5F7FA` / `#FFFFFF`
  - Teks utama: `#17212B`, teks sekunder: `#667085`
  - Shadow ganda: Highlight `#FFFFFF` `(-4, -4)` dan Shadow gelap `#D9E0E8` `(4, 4)`
  - Aksen utama: `#238D91` (Teal terkontrol)
  - Tanpa warna cokelat, krem, atau beige.
- **Dark Mode (Deep Teal Neumorphism)**:
  - Background utama: `#071A20`
  - Permukaan kartu: `#0B252D`, elevated: `#10313A`, pressed: `#06151A`
  - Teks utama: `#F4FAFC`, teks sekunder: `#A9C0C8`
  - Shadow ganda: Highlight `#163944` `(-4, -4)` dan Shadow gelap `#041116` `(4, 4)`
  - Aksen: `#36D6C0` (Teal) & `#48A9FF` (Blue)
- **Auto Mode**:
  - Mengikuti preferensi kecerahan sistem (*system brightness*) secara *real-time*.

---

## ⚙️ Logika Bisnis (Business Rules)

1. **Range Skor**: 0 sampai 10 (integer).
2. **Tombol Plus [+]**:
   - Menambah counter progres klik (0/10 → 1/10 → ... → 9/10).
   - Pada klik ke-10: Skor utama bertambah 1 (maksimal 10), dan progres kembali ke 0/10.
   - Jika skor sudah 10: Tombol nonaktif / feedback bahwa skor sudah maksimal. Tidak ada poin yang ditimbun.
3. **Tombol Minus [-]**:
   - Mengurangi skor utama sebesar 1 (minimal 0).
   - **Tidak merubah/mengurangi counter progres klik**.
4. **Daily Decay (Pengurangan Otomatis Harian)**:
   - Setiap pergantian tanggal kalender, semua lima skor utama berkurang 1 (minimal 0).
   - Progres klik tetap dipertahankan (tidak ikut berkurang).
   - Snapshot skor tanggal lama disimpan ke riwayat sebelum pengurangan diterapkan.
   - Tidak ada pengurangan ganda (*no double decay*) pada hari yang sama.
5. **Penyimpanan Lokal Persisten**:
   - File data: `my_life_data.json`.
   - Menggunakan mekanisme *atomic write* (menulis ke file `.tmp` lalu di-replace) agar data tidak mudah rusak.
   - Dilengkapi pemulihan otomatis jika file rusak (*corrupt file safe recovery*).

---

## 📁 Struktur Proyek

```
my-life/
├── .github/
│   └── workflows/
│       └── build.yml               # Workflow GitHub Actions build APK Android
├── assets/
│   ├── icon.png                    # App Icon resolusi tinggi (512x512)
│   ├── logo.png                    # Logo daun/pertumbuhan transparan
│   └── styles/
│       └── theme_tokens.json       # Token warna & styling neumorphism
├── components/
│   ├── __init__.py
│   ├── neumorphic.py               # Card, Button, ProgressDots, Badge Neumorphic
│   ├── aspect_card.py              # Kartu interaktif 5 pilar hidup
│   ├── aspect_detail_modal.py      # Modal rincian pilar & histori 7 hari
│   ├── history_view.py             # Grafik batang 7 hari, riwayat & aktivitas
│   ├── settings_view.py            # Pemilihan tema, info storage, backup & reset
│   └── splash_screen.py            # Splash screen elegan dengan transisi halus
├── core/
│   ├── __init__.py
│   ├── constants.py                # Definisi pilar, skor awal, dan batas nilai
│   ├── data_manager.py             # Logika penyimpanan JSON, decay & snapshot
│   └── theme.py                    # ThemeManager & kalkulasi bayangan neumorphic
├── tests/
│   ├── __init__.py
│   └── test_business_rules.py      # 15 skenario pengujian unit otomatis
├── main.py                         # Entry point utama aplikasi
├── requirements.txt                # Dependensi proyek (flet==1.0.4, pillow)
└── .gitignore                      # Mengabaikan file build dan temporary data
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Jalankan di Desktop / Dev

```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan aplikasi
python main.py
```

### 2. Jalankan Pengujian Unit

```bash
python -m unittest discover tests -v
```

Semua 15 skenario pengujian bisnis (plus, minus, decay, persistence, corrupt JSON recovery, theme independence) akan diuji secara otomatis.

---

## 📦 Build APK Android via GitHub Actions

Workflow build telah disiapkan di [`.github/workflows/build.yml`](file:///.github/workflows/build.yml) mengacu pada konfigurasi stabil dari proyek One Piece:

1. Push repository ini ke GitHub (`main` atau `master` branch).
2. Buka tab **Actions** di repositori GitHub Anda.
3. Pilih workflow **Build My Life Android APK**.
4. Klik **Run workflow** (mendukung `workflow_dispatch`).
5. Tunggu hingga proses build selesai. File APK siap unduh akan tersedia di bagian **Artifacts** (`my-life-android-apk`).
