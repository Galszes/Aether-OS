# Aether Kubuntu Remaster — Sesi Modular & AI Harness

Repositori modifikasi **Kubuntu 24.04 LTS x86_64 (Plasma 5.27)** menjadi **Aether OS** menggunakan **Cubic (Custom Ubuntu ISO Creator)**. Setiap sesi/modul mempunyai `README.md`, payload, dan konfigurasi sendiri, dilengkapi skrip pasca-modul untuk instalasi **Agentic AI Harness**, **Blur Fix**, **Desktop Sync**, dan **Branding Installer**.

---

## 1. Urutan Sesi Modular (`modules/`)

Salin repositori ini (beserta folder `private-assets/`) ke `/tmp/aether-kubuntu-remaster` di dalam chroot Cubic, lalu jalankan perintah pada masing-masing modul secara berurutan:

| Sesi | Modul | Hasil Utama |
|---|---|---|
| **00** | [00 Persiapan](modules/00-persiapan/README.md) | Hapus 6 paket bloatware (`kmines`, `kpat`, `ksudoku`, `kmahjongg`, `kubuntu-wallpapers`, `plasma-workspace-wallpapers`), pasang dependensi dasar, backup `/etc/skel`, dan hook relokasi akun baru |
| **01** | [01 Font](modules/01-font/README.md) | Google Sans, Urbanist, Rounded Elegance, IBM Plex |
| **02** | [02 Ikon](modules/02-ikon/README.md) | Vivid Glassy Dark Icons |
| **03** | [03 Appearance](modules/03-appearance-glass/README.md) | Tema Aeos, Aeos-Blur, Kvantum `AetherGlass`, GTK, dan efek blur |
| **04** | [04 Panel Terpisah](modules/04-panel-terpisah/README.md) | Dua panel adaptif, jam/tanggal, baterai, dan tata letak widget |
| **05** | [05 Panel Studio](modules/05-panel-studio/README.md) | Aplikasi GUI **Aether Panel Studio** beserta launcher |
| **06** | [06 Wallpaper & Branding](modules/06-wallpaper-branding/README.md) | Wallpaper 4K, logo menu/lock/logout/System Information, dan tema SDDM |
| **07** | [07 Splash](modules/07-splash/README.md) | Splash screen `org.aether.splashstudio` (Urbanist + overlay hitam) |
| **08** | [08 Konsole](modules/08-konsole/README.md) | Profil terminal Konsole transparan/glass |
| **09** | [09 Build ISO](modules/09-build-iso/README.md) | Pemeriksaan akhir, konfigurasi GRUB, dan pengujian Live/Install |

---

## 2. Tahap AI Harness, Patch Blur & Branding Installer (`scripts/` & `payloads/`)

Setelah modul `00` sampai `08` selesai diterapkan di Terminal Cubic, jalankan skrip di [`scripts/`](scripts/README.md) dengan urutan berikut (semua file `.tar.gz` yang dibutuhkan sudah tersedia langsung di folder [`payloads/`](payloads) tanpa perlu server eksternal):

```bash
cd /tmp/aether-kubuntu-remaster/scripts

# 1. Pasang AI Harness (Hermes, Codex, OpenCode, Faster-Whisper, Playwright Chromium, aether-voice)
bash install-aether-ai.sh

# 2. Terapkan tema Plymouth aether-logo & hotfix dasar
bash apply-hotfix.sh

# 3. Terapkan patch kompatibilitas blur KWin/Kvantum & GLX
bash apply-blur-fix.sh

# 4. Sinkronkan launcher taskbar & widget desktop ke /etc/skel
bash apply-desktop-sync.sh

# 5. Terapkan branding Calamares & dialog PyQt5 "Try or Install Aether OS"
bash apply-installer-brand.sh

# 6. Pasang Aether Panel Studio system-wide (/opt/AetherPanelStudio) & perbaiki izin +x .desktop
bash apply-panel-studio-fix.sh

# 7. Rapikan ownership akhir & perbarui initramfs
bash polish-aether.sh
```

---

## 3. Konfigurasi Menu Boot GRUB (Tab Boot Cubic)

Setelah keluar dari Terminal Cubic (klik **Next**), pada tab **Boot** (`boot/grub/grub.cfg`), samakan isinya dengan [`payloads/grub.cfg`](payloads/grub.cfg) agar menu boot menampilkan **"Try or Install Aether OS"** dan **"Aether OS (safe graphics)"**, lalu klik **Generate** untuk membangun berkas ISO.

---

## 4. Struktur Direktori

- `modules/` — Sesi modular `00` s/d `09` (`skel/` untuk `/etc/skel`, `root/` untuk `/`, dan `config/` untuk fragmen INI yang digabung dengan `tools/merge-kconfig.py`).
- `scripts/` — Skrip otomatisasi AI harness, patch blur, sinkronisasi desktop, dan branding installer.
- `payloads/` — Paket payload `.tar.gz` dan `grub.cfg` yang digunakan langsung oleh `scripts/`.
- `tools/` — Utilitas pendukung (`merge-kconfig.py` dan `build-pdf.py`).
- `docs/` — Dokumentasi arsitektur, peta fitur ke kode ([docs/peta-fitur-ke-kode.md](docs/peta-fitur-ke-kode.md)), alur presentasi ([docs/presentasi.md](docs/presentasi.md)), screenshot, dan PDF per sesi ([docs/pdf/Panduan-Aether-Per-Sesi.pdf](docs/pdf/Panduan-Aether-Per-Sesi.pdf)).
- `private-assets/` — Aset tema/ikon/font/wallpaper lokal (lihat [ASSETS.md](ASSETS.md); disertakan penuh pada arsip rilis `aether-kubuntu-remaster-final.tar.gz`).
