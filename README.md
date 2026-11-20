# Aether Kubuntu Remaster — Sesi Modular & AI Harness

Repositori modifikasi **Kubuntu 24.04 LTS x86_64 (Plasma 5.27)** menjadi **Aether OS** menggunakan **Cubic (Custom Ubuntu ISO Creator)**. Setiap sesi/modul mempunyai `README.md`, payload, dan konfigurasi sendiri, mencakup tema glass/blur, **Agentic AI Harness**, serta branding installer **Aether OS**.

---

## 1. Urutan Sesi Modular (`00` – `11`)

Salin repositori ini (beserta folder `private-assets/` dari Release) ke `/tmp/aether-kubuntu-remaster` di dalam Terminal Cubic, lalu ikuti sesi secara berurutan:

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
| **09** | [09 AI Harness](modules/09-ai-harness/README.md) | Antigravity (`agy`), `codex`, `hermes`, `opencode`, `aether-voice` (`faster-whisper-small`), `playwright` + Chromium, dan tool kontrol desktop |
| **10** | [10 Branding & Fix](modules/10-branding-dan-fix/README.md) | Plymouth `aether-logo`, blur fix GLX, sinkronisasi taskbar/widget, Calamares *Try or Install Aether OS*, dan fix Panel Studio |
| **11** | [11 Build ISO](modules/11-build-iso/README.md) | Konfigurasi boot GRUB (`payloads/grub.cfg`), pemeriksaan akhir, dan generate ISO |

---

## 2. Konfigurasi Menu Boot GRUB (Tab Boot Cubic)

Setelah menyelesaikan sesi `00` s/d `10` dan keluar dari Terminal Cubic (klik **Next**), pada tab **Boot** (`boot/grub/grub.cfg`), samakan isinya dengan [`payloads/grub.cfg`](payloads/grub.cfg) agar menu boot menampilkan **"Try or Install Aether OS"** dan **"Aether OS (safe graphics)"**, lalu klik **Generate** untuk membangun berkas ISO.

---

## 3. Struktur Direktori

- `modules/` — Sesi modular `00` s/d `11` (`skel/` untuk `/etc/skel`, `root/` untuk `/`, dan `config/` untuk fragmen INI yang digabung dengan `tools/merge-kconfig.py`).
- `scripts/` — Skrip otomatisasi yang dipanggil oleh sesi `09` dan `10` (lihat [scripts/README.md](scripts/README.md)).
- `payloads/` — Paket payload `.tar.gz` dan `grub.cfg` yang digunakan langsung oleh `scripts/`.
- `tools/` — Utilitas pendukung (`merge-kconfig.py` dan `build-pdf.py`).
- `docs/` — Dokumentasi arsitektur, panduan lengkap *All-In-One* ([docs/Aether-OS-All-In-One-Master-Guide.md](docs/Aether-OS-All-In-One-Master-Guide.md)), rangkuman materi ([docs/Rangkuman-Materi-Lengkap-Aether-OS.md](docs/Rangkuman-Materi-Lengkap-Aether-OS.md)), daftar perintah wajib ([docs/Daftar-Perintah-Wajib-Kelompok-Aether-OS.md](docs/Daftar-Perintah-Wajib-Kelompok-Aether-OS.md)), peta fitur ke kode ([docs/peta-fitur-ke-kode.md](docs/peta-fitur-ke-kode.md)), alur presentasi ([docs/presentasi.md](docs/presentasi.md)), screenshot, dan PDF per sesi ([docs/pdf/Panduan-Aether-Per-Sesi.pdf](docs/pdf/Panduan-Aether-Per-Sesi.pdf)).
- `private-assets/` — Aset lokal (font, ikon, tema, wallpaper, dan binary `bin/agy` `237 MB`; disertakan penuh pada arsip Release `aether-kubuntu-remaster-final.tar.gz`).
