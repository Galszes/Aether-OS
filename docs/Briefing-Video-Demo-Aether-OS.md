# Briefing Produksi: Demonstrasi Aether OS

**Format:** presentasi akademik dengan voiceover Bahasa Indonesia dan callout layar  
**Platform:** YouTube Unlisted  
**Durasi sasaran:** 8 menit 40 detik; batas mutlak 10 menit  
**Basis teknis:** Kubuntu 24.04 x86_64, KDE Plasma 5.27, remaster modular Cubic

## Tujuan dan pesan utama

Tunjukkan bahwa Aether OS adalah remaster Kubuntu yang dibentuk melalui sesi konfigurasi terpisah: font, ikon, Appearance, panel, Aether Panel Studio, branding, splash, dan validasi ISO. Buktikan fitur melalui desktop yang benar-benar berjalan dan hubungkan kontrol Studio dengan file atau kode yang mengubahnya.

Sampaikan batas proyek dengan jujur. Folder `aether-kubuntu-remaster` adalah bahan modular Cubic; ISO hasil akhir dari struktur tersebut belum diuji boot. Aether Panel Studio, tema, dan konfigurasi dibuat untuk Plasma 5.27. Efek blur kompatibilitas khusus hanya ditujukan untuk KWin X11 5.27.11 pada mesin sumber. Paket AI Agents belum menjadi bagian dari modul ISO.

## Timeline dan naskah rekaman

| Waktu | Visual / layar yang direkam | Narasi voiceover siap baca | Teks callout di layar |
|---|---|---|---|
| **00:00–00:30** 30 dtk | Mulai dari layar gelap. Tampilkan boot VM, splash Aether, kemudian potongan singkat layar login. Judul video muncul perlahan. | “Ini Aether OS, remaster Kubuntu yang saya siapkan sebagai proyek akademik. Fokus proyek ini adalah membangun pengalaman desktop KDE yang konsisten, lalu memecah proses remastering-nya menjadi sesi yang dapat ditinjau dan diulang.” | `AETHER OS` · `Remaster Kubuntu 24.04` · `Proyek akademik` |
| **00:30–01:05** 35 dtk | Tampilkan menu boot VM lalu desktop live Kubuntu. Buka installer. Jangan rekam splash terlalu lama. | “Proses dimulai dari ISO Kubuntu 24.04 di mesin virtual. Setelah masuk ke lingkungan live, saya menjalankan installer pada disk virtual khusus untuk pengujian. Dengan cara ini, tahap pemasangan tidak mengubah sistem utama.” | `VM pengujian` · `Disk virtual khusus` |
| **01:05–01:45** 40 dtk | Rekam ringkas layar bahasa, keyboard, jaringan, jenis instalasi, dan konfirmasi disk virtual. Potong layar yang menampilkan nama akun, kata sandi, atau serial. | “Installer menyiapkan sistem dasar Kubuntu. Di rekaman ini, pilihan instalasi ditampilkan singkat agar fokus tetap pada perubahan remaster. Proses penyalinan file dipercepat; langkah konfirmasi disk tetap diperlihatkan supaya konteks instalasinya jelas.” | `Instalasi Kubuntu` · `Salin file: timelapse` · `Akun uji` |
| **01:45–02:25** 40 dtk | Timelapse proses pemasangan; sisipkan 2–3 potongan status installer. Tampilkan reboot dan pelepasan ISO virtual jika dilakukan. | “Setelah paket dasar selesai disalin, VM melakukan restart. Pada penggunaan nyata, proses ini berlangsung lebih lama daripada cuplikan timelapse. Sesudah instalasi, saya masuk ke sesi desktop hasil pengujian untuk memeriksa konfigurasi remaster.” | `Timelapse proses instalasi` · `Restart ke sistem terpasang` |
| **02:25–03:05** 40 dtk | Boot hasil instalasi, SDDM dengan background dan logo, login akun demo, splash Plasma. Tampilkan transition tanpa menampilkan kredensial. | “Branding dibagi menurut tahapnya. SDDM adalah layar login, splash muncul saat Plasma sedang dimuat, sedangkan lock screen dan konfirmasi logout merupakan layar yang berbeda. Pemisahan ini penting karena setiap layar memiliki file tema dan cara penerapan sendiri.” | `SDDM: login` · `Splash: Plasma mulai` · `Lock dan logout: komponen terpisah` |
| **03:05–04:15** 70 dtk | Tampilkan desktop penuh. Perbesar panel bawah. Buka beberapa aplikasi lalu tutup untuk memperlihatkan bidang kiri berubah lebar. Buka launcher dan hidden icons. | “Pada desktop, panel memakai dua bidang rounded yang mengikuti kelompok aplikasi dan tray. Spacer di antaranya tidak diberi latar, sehingga terlihat bening. Ini pengaturan visual dalam satu panel Plasma, bukan dua kontainer panel terpisah. Saya membuka dan menutup aplikasi untuk menunjukkan bidang taskbar menyesuaikan isi.” | `Panel Islands: splitPanel=1` · `Ruang kosong bening` · `Lebar mengikuti isi` |
| **04:15–05:05** 50 dtk | Tunjukkan menu edit panel; pindahkan baterai ke dekat jam bila aman. Buka system tray settings, digital clock, lalu tampilkan System Settings Fonts secara singkat. | “Isi dan posisi widget diatur dari mode edit Plasma. Baterai adalah applet mandiri yang bisa dipindahkan; ikon tray diatur melalui konfigurasi System Tray. Font desktop menggunakan Google Sans, taskbar IBM Plex Sans, jam Urbanist 12 poin, dan profil terminal IBM Plex Mono.” | `Font global: Google Sans` · `Jam: Urbanist 12 pt` · `Terminal: IBM Plex Mono` · `Baterai: applet terpisah` |
| **05:05–06:25** 80 dtk | Buka Aether Panel Studio. Tampilkan tab Panel dan toggle split, geser opasitas/radius. Beralih ke Shadow, Popup, Jendela & Blur, dan Bilah Judul. Tekan Terapkan hanya bila perubahan yang direkam memang ingin disimpan; jika tidak, batalkan. | “Aether Panel Studio menyediakan kontrol untuk tampilan panel, shadow, highlight ikon, popup dan bilah judul. Opasitas mengatur seberapa tembus permukaan; blur berasal dari compositor KWin dan merupakan kontrol terpisah. Studio juga membuat backup sebelum perubahan panel diterapkan. Di tab Jendela dan Blur terdapat pengaturan Kvantum untuk aplikasi yang mendukungnya.” | `Opasitas ≠ blur` · `Panel / Shadow / Popup / Blur / Bilah Judul` · `Backup sebelum Terapkan` |
| **06:25–07:15** 50 dtk | Tampilkan tab Layar kunci & Logo. Lihat preview lock, SDDM dan logout bila waktu cukup. Beralih ke Splash Screen, tampilkan preview nyata serta judul/font/overlay. | “Tab Branding mengatur background lock screen, logo tengah, logo Home, dan pemasangan tema SDDM. Logo Home dipakai launcher dan System Information; logo tengah lock screen diproses terpisah. Tab Splash membuat tema layar mulai Plasma dengan gambar, teks, font, lapisan gelap, dan progress bar. Preview digunakan sebelum menerapkan perubahan.” | `Home → Launcher + Info Center` · `Lock logo → lock/logout/SDDM` · `Splash → setelah login` |
| **07:15–08:10** 55 dtk | Tampilkan struktur folder repo modular, README tiap sesi, fragmen kdeglobals, `main.qml`, `backend.py`, dan modul Cubic. Tampilkan layar terminal singkat tanpa key. | “Remastering disusun per sesi: persiapan, font, ikon, Appearance, panel, Studio, branding, splash, Konsole, lalu build dan uji ISO. Isi `skel` menjadi setelan akun baru, sedangkan `root` memasang file sistem. Panel Islands dihitung di `main.qml`; `backend.py` menghubungkan kontrol Studio dengan konfigurasi. Untuk AI Agents, saya perlu tegas: repo ini belum memasukkan Codex, Antigravity, OpenCode, atau Hermes ke ISO. Codex yang tersedia di mesin pengembangan tidak berarti ikut terpasang di image Cubic.” | `Sesi Cubic modular` · `/etc/skel: akun baru` · `/usr/share: aset sistem` · `AI Agents: belum dibundel ke ISO` |
| **08:10–08:40** 30 dtk | Kembali ke desktop, tampilkan panel dan About/System Information. Akhiri dengan judul dan status proyek. | “Aether OS menggabungkan kustomisasi KDE dengan alat untuk mengubah panel dan branding. Bahan Cubic sudah dipecah agar setiap tahap dapat diperiksa. Langkah berikutnya adalah membangun ISO dari modul ini, lalu menguji live session dan instalasi VM sebelum menyebutnya sebagai rilis teruji. Terima kasih.” | `Aether OS` · `Kubuntu 24.04 + kustomisasi KDE` · `ISO modular: perlu uji boot akhir` |

**Total durasi sasaran: 8:40.** Sisakan sekitar 20–40 detik untuk transisi, jeda narasi, atau kesalahan kecil, sehingga hasil akhir tetap di bawah 9:20.

## Catatan AI Agents dan klaim integrasi

Modul Cubic yang tersedia memasang font, tema, ikon, panel, Aether Panel Studio, branding, splash, dan profil Konsole. Tidak ada sesi atau payload untuk memasang Antigravity, OpenCode, Hermes, maupun konfigurasi harness AI.

Perintah `codex` ditemukan pada mesin pengembangan (`/usr/local/bin/codex`), tetapi tidak disalin oleh sesi modul ke image Cubic. Antigravity, OpenCode, dan Hermes tidak ditemukan sebagai executable pada PATH mesin pengembangan saat pemeriksaan. Karena ISO akhir belum dibangun dan diuji, video tidak boleh menyebut satu pun agent sebagai aplikasi bawaan Aether OS.

Jika tim ingin menunjukkan AI, labeli sebagai **demo lingkungan pengembangan terpisah**. Gunakan akun demo tanpa kredensial nyata di layar, tunjukkan langkah integrasi yang memang sudah diuji, dan bedakan dari isi ISO. Klaim “terintegrasi di ISO” baru layak setelah paket, dependensi, lisensi, metode autentikasi, serta uji offline/online ditambahkan ke modul dan diverifikasi di ISO hasil Cubic.

## Checklist persiapan sebelum rekam

### VM dan alur instalasi

- Gunakan snapshot VM bersih dan disk virtual khusus yang aman dihapus; jangan gunakan disk sistem utama.
- Rekam sekurangnya 1920×1080 pada 30 fps dengan skala desktop 100% agar teks konfigurasi terbaca.
- Alokasikan sumber daya yang cukup untuk instalasi dan Plasma; gunakan akselerasi 3D bila tersedia dan catat adapter grafis virtual yang dipakai.
- Siapkan ISO Kubuntu 24.04, checksum ISO, proyek Cubic modular, dan urutan layar installer sebelum mulai merekam.
- Uji lebih dulu boot live, installer, restart ke sistem terpasang, SDDM, login, splash, dan panel. Simpan snapshot sebelum tahap yang mengubah disk.
- Atur zoom editor/terminal agar nama modul dan kode penting dapat dibaca. Tutup notifikasi, launcher pencarian, dan jendela yang tidak dipakai.
- Rekam timelapse hanya pada penyalinan paket. Pertahankan cuplikan konfirmasi disk virtual dan selesaikan jump cut dengan kartu teks singkat.

### Privasi dan aset

- Buat akun demo tanpa nama pribadi; jangan tampilkan email, nama host pribadi, daftar file pribadi, atau riwayat terminal.
- Jangan tampilkan password, token, API key, file `.env`, konfigurasi provider, QR autentikasi, atau URL sesi yang memuat token.
- Untuk AI, gunakan akun uji kosong atau placeholder yang sudah disamarkan. Pastikan perintah demo tidak mencetak environment variable atau log autentikasi.
- Periksa hak penggunaan logo, wallpaper, font, tema ikon, dan aset pihak ketiga sebelum video dipublikasikan atau repositori dibuka.
- Simpan voiceover dan project file rekaman; gunakan noise gate ringan dan pastikan callout tidak menutupi menu yang sedang dijelaskan.

### Klaim teknis yang harus akurat

- Panel adaptif adalah dua bidang latar di dalam **satu kontainer panel Plasma**. Spacer tengah bening; ini bukan dua panel OS independen.
- Opasitas mengatur transparansi. Blur memerlukan efek KWin/compositor yang benar-benar aktif; hasil VM dapat berbeda dari perangkat fisik.
- Efek kompatibilitas Aether ditargetkan untuk KWin X11 5.27.11 pada mesin sumber. Modul modular default memilih blur KWin bawaan dan menonaktifkan plugin kompatibilitas. Jangan menampilkan blur khusus seolah dijamin di semua versi atau Wayland.
- Konfigurasi dan PDF modul sudah disiapkan, tetapi ISO dari struktur modular ini belum boot-tested. Sebutkan status ini pada callout atau narasi jika video memperlihatkan repo.
- Jangan mengatakan Codex/Antigravity/OpenCode/Hermes terpasang di Aether OS. Saat pemeriksaan, hanya executable Codex ditemukan pada host pengembangan; tidak ada payload agent pada modul ISO.

## Metadata YouTube Unlisted

**Judul yang disarankan:**  
`Aether OS: Remaster Kubuntu dengan Panel Adaptif dan Aether Panel Studio | Demo Proyek`

**Deskripsi:**

```text
Aether OS adalah proyek remaster Kubuntu 24.04 dengan fokus pada personalisasi KDE Plasma dan alur remaster modular menggunakan Cubic.

Video ini mendemonstrasikan proses instalasi di VM, branding boot/login/splash, panel adaptif, pengaturan font dan ikon, serta Aether Panel Studio. Kustomisasi dibagi ke sesi terpisah agar file tujuan dan kode yang mengubahnya dapat ditinjau.

Status: modul remaster sudah disusun; ISO akhir dari struktur modular ini belum diuji boot. Blur KWin bergantung pada versi compositor dan sesi grafis. AI Agents tidak dibundel pada ISO yang ditunjukkan.

Basis: Kubuntu 24.04 x86_64, KDE Plasma 5.27.
Repositori/bahan proyek: [tambahkan tautan setelah repositori siap]
```

**Chapters / timestamps:**

```text
00:00 Aether OS dan tujuan proyek
00:30 Boot VM dan Kubuntu Live
01:05 Proses instalasi Kubuntu
01:45 Timelapse pemasangan
02:25 First boot: SDDM dan splash
03:05 Desktop dan panel adaptif
04:15 Font, baterai, dan System Tray
05:05 Aether Panel Studio
06:25 Branding dan Splash Screen
07:15 Struktur modul Cubic dan status AI Agents
08:10 Penutup dan status pengujian
```

## Catatan editorial

Rekam voiceover berdasarkan kolom narasi setelah gambar terkunci. Jika durasi melewati 9:20, pendekkan timelapse dan layar konfigurasi; jangan menghapus penjelasan bahwa ISO belum diuji atau status AI Agents. Pastikan bab video tepat mengikuti waktu final setelah proses editing.
