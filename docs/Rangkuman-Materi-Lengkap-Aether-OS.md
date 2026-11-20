# Rangkuman Materi Lengkap Proyek Aether OS

**Basis Sistem:** Kubuntu 24.04.5 LTS (*Noble Numbat*, x86_64) · KDE Plasma 5.27  
**Tool Remastering:** Cubic (*Custom Ubuntu ISO Creator* `2026.09.110`)  
**Repositori Proyek:** `https://github.com/Galszes/Aether-OS` (`~/Documents/aether-kubuntu-remaster`)  
**Sumber Rangkuman:** Riwayat sesi Codex (`01a1a5cf`, `01a1a611`, `01a1a738`, `01a1ca91`), catatan teknis (`Rangkuman-Aether-Panel-Studio-2026-11-11.md`, `Tutorial-Lengkap-Modifikasi-Kubuntu-Aether.md`, `Panduan-Aether-Per-Sesi.md`, `peta-fitur-ke-kode.md`, `Briefing-Video-Demo-Aether-OS.md`), serta hasil build & debugging ISO Cubic hingga versi final (`Sesi 00`–`11`).

---

## Bagian 1 — Identitas Proyek, Tujuan Awal & Spesifikasi Lingkungan

### 1.1 Latar Belakang & Tujuan Awal
Proyek **Aether OS** berawal dari gagasan untuk membangun sistem operasi Linux berbasis **Kubuntu 24.04 LTS (KDE Plasma 5)** yang langsung memadukan dua kebutuhan utama:
1. **Desktop modern *liquid/frosted glass* yang konsisten dan terkontrol** — memiliki taskbar terpisah adaptif (*Panel Islands*), tipografi non-pixelated, tema ikon kaca, efek blur nyata di atas VM maupun hardware fisik, serta branding OS yang menyatu dari boot menu hingga desktop.
2. **Ekosistem *Agentic AI Harness* siap pakai (*out-of-the-box*)** — menggabungkan **Antigravity (`agy`)**, **OpenAI Codex (`codex`)**, **Hermes Agent (`hermes`)**, **OpenCode (`opencode`)**, **Voice-to-Text lokal offline (`aether-voice`)**, otomasi browser (**Playwright + Chromium**), dan kontrol desktop X11 agar tersedia langsung secara global untuk setiap akun pengguna tanpa instalasi manual berulang.

### 1.2 Evolusi Pengembangan (Lintas Tahap)
- **Tahap 1 — Eksperimen Desain & Studio GUI (`4–11 Nov`, *Codex Sessions*):**
  Perancangan aset SVG tema `Aeos`, *Panel Islands* dengan celah spacer bening, perbaikan shadow highlight aplikasi & indikator tray, investigasi mendalam masalah blur KWin pada VirtualBox SVGA3D, normalisasi transparansi Kvantum pada Dolphin, pemisahan 4 lapisan branding (Home, Lock, Logout, SDDM), serta pembuatan aplikasi editor visual **Aether Panel Studio** (`PyQt5`).
- **Tahap 2 — Modularisasi Bahan Remaster (`11–13 Nov`, *Codex Modular Docs*):**
  Memecah seluruh modifikasi desktop menjadi modul sesi terpisah (`00` s/d `09` awal) dengan fragmen konfigurasi INI (`tools/merge-kconfig.py`), pencatatan checksum (`MANIFEST.json`), serta penyusunan dokumen presentasi/tutorial. *Catatan kondisi pada fase ini:* hingga 13 November, modul masih berfokus pada tampilan/branding desktop dan belum membundel AI Agents ataupun menguji boot ISO final.
- **Tahap 3 — Build ISO Nyata, Integrasi AI Harness & Debugging (`14–16 Nov`, *Final Build*):**
  Pembangunan ISO dari `kubuntu-24.04.5-desktop-amd64.iso` di Cubic (`/media/aether/.../aetheros`), pembuangan paket game & wallpaper Kubuntu, integrasi penuh AI Harness (`Sesi 09`), pemasangan Plymouth `aether-logo` & `initramfs`, perbaikan boot menu GRUB dan installer Calamares (*Try or Install Aether OS*), perbaikan blur VM (`aether-compat-blur-v6.so` + GLX), perbaikan izin eksekusi widget Panel Studio (`Sesi 10`), hingga penataan repositori mandiri di GitHub (`Galszes/Aether-OS`).

### 1.3 Spesifikasi Lingkungan Pengujian & Build
| Komponen | Detail Hasil Pemeriksaan |
|---|---|
| **Host Pengembangan** | Windows 11 · CPU Ryzen 3 seri 7000 (iGPU AMD) |
| **Virtualizer Guest** | Oracle VirtualBox (`VMSVGA`, 3D Acceleration aktif, VRAM 256 MB) |
| **Basis Distribusi** | Ubuntu / Kubuntu 24.04.5 LTS (`noble`, x86_64) |
| **Desktop & Compositor** | KDE Plasma 5.27 · Sesi **X11** · KWin `5.27.11` · `plasma-workspace` `5.27.12` · Qt `5.15.13` |
| **Renderer OpenGL Guest** | `VMware, Inc.` — `SVGA3D; build: RELEASE; LLVM;` · Mesa `25.2.8` · OpenGL `4.1, GLX` |
| **Kernel Target ISO** | `7.0.0-31-generic` (`vmlinuz-7.0.0-31-generic` & `initrd.img-7.0.0-31-generic`) |
| **Tool Remastering** | Cubic versi `2026.09.110` |

---

## Bagian 2 — Desain Antarmuka Desktop, *Panel Islands* & Tipografi

### 2.1 Konsep *Panel Islands* Adaptif (`splitPanel=1`)
Taskbar Aether OS menampilkan dua blok latar rounded (*pulau kiri* untuk Application Launcher & daftar aplikasi, *pulau kanan* untuk System Tray, baterai, & jam/tanggal) dengan ruang kosong di tengah yang benar-benar bening.

- **Satu Kontainer, Bukan Dua Panel Terpisah:** Diimplementasikan melalui widget kustom **`org.aether.panelislands`** (`data/main.qml`). Kontainer panel Plasma tetap selebar layar (bukan mode *Auto Hide*), namun QML memetakan posisi grup widget kiri dan kanan secara berkala (`updateBackgrounds`) dan hanya menggambar elemen `backgroundComponent` pada kedua rentang tersebut.
- **Lebar Mengikuti Isi:** Saat aplikasi dibuka atau ditutup, latar pulau kiri otomatis melebar dan menyusut mengikuti jumlah ikon taskbar. Spacer (*Flexible Spacer*) di tengah tidak diberi latar sehingga wallpaper tetap tampak jernih.
- **Rumus Geometri Sudut & Highlight:**
  - Dalam desain awal bersama Codex, sudut panel dan tombol aplikasi di dalam taskbar dirapikan memakai relasi **`inner corner + margin = outer corner`**, sehingga highlight tombol aplikasi tidak menabrak lengkungan tepi panel.
  - **Perbaikan Shadow & Indikator *Show Hidden Icons*:** Garis indikator biru pada tombol panah *System Tray* yang sebelumnya melewati sudut rounded diselaraskan menggunakan geometri frame `Aeos/widgets/tabbar.svg` dan `Aeos/widgets/tasks.svg` pada status normal, hover, aktif, dan minimized.
  - **Nilai Opasitas Panel:** Nilai aktif referensi adalah **23% opasitas** (~77% transparan), di mana pada slider Panel nilai `0` = bening dan `100` = pekat.
  - **Tooltip Rounded:** Slider **Rounded tooltip (hover)** (`0–18 px`) membentuk geometri latar dan *mask blur* dengan radius sudut yang sama agar kotak blur tidak keluar berbentuk persegi di tepi tooltip. Warna/opasitas tooltip mengikuti pengaturan popup (`dialogs/background.svg`, `widgets/background.svg`, `tooltip.svg`).

### 2.2 Tata Letak Widget & Jam/Baterai
- Posisi dan isi widget diatur lewat **Mode Edit Panel Plasma** (*Enter Edit Mode*), bukan dari slider warna Studio:
  - **Jam & Tanggal:** Widget *Digital Clock* disetel agar jam dan tanggal tersusun **vertikal (ditumpuk)** dengan tanggal di bawah jam.
  - **Baterai Mandiri:** Applet baterai dikeluarkan dari popup tray dan ditempatkan sebagai ikon mandiri tepat di sebelah jam/tray kanan.
  - **System Tray:** Ikon tray dikelola per item (*Always shown*, *Always hidden*, atau *Shown when relevant*) lewat *Configure System Tray*.

### 2.3 Standarisasi Tipografi Anti-Pixelated
Untuk mengatasi teks yang tampak bergerigi (*pixelated*) pada resolusi VM, Aether OS memisahkan penetapan font berdasarkan komponennya (`Sesi 01`, `04`, `07`, `08`):

| Elemen UI | Font Aktif | Lokasi Konfigurasi |
|---|---|---|
| **Font Global Desktop & Aplikasi** | **Google Sans (11 pt)** | `kdeglobals` (`modules/01-font/config/kdeglobals.ini`) & `fonts.conf` |
| **Label Taskbar & Window Manager** | **IBM Plex Sans (11 pt)** | `kdeglobals` (`Sesi 01`) |
| **Jam & Tanggal Panel** | **Urbanist (12 pt, Medium Italic)** | Layout *Digital Clock* (`plasma-org.kde.plasma.desktop-appletsrc`) |
| **Splash Screen Plasma** | **Urbanist** | `org.aether.splashstudio` (`Sesi 07`) |
| **Terminal Konsole** | **IBM Plex Mono** | Profil kaca `Aether Glass.profile` (`modules/08-konsole/`) |

File font lokal (Google Sans, Urbanist, Rounded Elegance) disimpan di `/usr/local/share/fonts/` (`fc-cache -f`), sedangkan IBM Plex berasal dari paket `fonts-ibm-plex`.

---

## Bagian 3 — Penyelidikan Blur KWin di VM & Transparansi Dolphin/Kvantum

### 3.1 Perbedaan Opasitas dan Blur
Transparansi (*opasitas*) hanya mengatur seberapa pekat warna latar SVG/Kvantum, sedangkan **blur** adalah efek *post-processing* compositor KWin yang memburamkan konten jendela di belakangnya. Transparansi tanpa efek blur hanya membuat jendela/teks di belakang tetap terlihat tajam.

### 3.2 Hasil Eksperimen Blur di VirtualBox (`SVGA3D`)
Pada pengujian 11 November (`AetherPanelStudio/diagnostics/`), ditemukan bahwa efek transparansi berjalan tetapi teks di belakang Dolphin dan menu Home tetap tajam (`ketajaman pola uji ≈ 23,32`). Sejumlah solusi diuji:

| Pendekatan yang Diuji | Hasil Pengukuran / Observasi | Keputusan |
|---|---|---|
| Blur bawaan KWin pada `SVGA3D` (strength 1 dan 8) | Pola garis uji tidak memburam; nilai ketajaman tetap **~23,32** | Tidak efektif di SVGA3D |
| KWin terpisah dengan `llvmpipe` (*software rendering*) | Blur tampak berhasil pada pola uji | Tidak dipilih sebagai default (beban CPU/software rendering) |
| Compositor `Picom` (`GLX` & `XRender`) | `Picom GLX` menghasilkan render tidak tepat; `XRender` tidak memblur | Tidak dipakai |
| **Efek Native KWin `aether-compat-blur` (`blur.cpp`)** | Ketajaman pola uji turun dari **23,32 ke 1,39** (**penurunan ketajaman ~94%** — bukti fisik efek blur, bukan benchmark FPS) | **Dipilih sebagai solusi kompatibilitas VM** |

- **Cara Kerja `aether-compat-blur`:** Plugin C++ (`blur.cpp`) yang dikompilasi untuk ABI **KWin X11 5.27.11**, menggunakan shader dua lintasan (*two-pass*, 17 sampel per lintasan), membaca `[Effect-blur] BlurStrength` (`1–15`) dari `kwinrc`, dan mengikuti region blur X11 per jendela.
- **Perbaikan *Ghosting* & *Peek at Desktop*:** Pada iterasi v5 (lalu diperbarui ke `aether-compat-blur-v6.so` di `apply-blur-fix.sh`), ditambahkan pengecatan ulang adegan agar isi frame sebelumnya tidak tertinggal (*ghosting* yang sempat dikira wallpaper berubah), serta pengecualian agar saat **Peek at Desktop** aktif jendela tidak ikut membuat desktop tampak blur.
- **Aktivasi di Chroot (`apply-blur-fix.sh`):**
  - Binary diletakkan di `/etc/skel/.local/opt/aether-kvantum/usr/lib/x86_64-linux-gnu/qt5/plugins/kwin/effects/plugins/aether-compat-blur-v6.so`.
  - Dimuat lewat hook `/etc/skel/.config/plasma-workspace/env/aether-qt-style.sh` (`QT_PLUGIN_PATH`).
  - Pada `kwinrc`: `aether-compat-blurEnabled=true`, `blurEnabled=false`, dan `GLPlatformInterface=glx`.
  - Penanda `/etc/skel/.config/aether-panel-studio-use-stock-blur` (via `restore-stock-blur.sh`) disiapkan bila pengguna ingin kembali ke blur bawaan KWin pada hardware fisik non-VM.

### 3.3 Normalisasi Transparansi Dolphin & Tema Kvantum `AetherGlass`
- Masalah awal pada Kvantum: nilai transparansi `0` tidak menghasilkan jendela yang pekat dan proses Dolphin lama tidak langsung memperbarui style.
- Perbaikan pada tema **`AetherGlass`** (`AetherGlass.kvconfig` & `AetherGlass.svg`):
  - Menggunakan `reduce_window_opacity`, `reduce_menu_opacity`, dan `transparent_dolphin_view` (agar area daftar file memperlihatkan kaca di bawahnya).
  - Menormalkan nilai alpha tetap pada elemen SVG `aether-window-normal` dan `aether-window-normal-inactive` menjadi `1`, serta menghapus alpha berlebih pada warna dasar agar tidak menumpuk.
  - **Konvensi Skala:** Untuk jendela/menu Kvantum berlaku rentang `0–50` di mana **`0` = pekat (solid)** dan **`50` = paling transparan** (berkebalikan dengan slider *opasitas panel* `0=bening, 100=pekat`).
  - Mengirim sinyal D-Bus/Qt style update dan menyediakan tombol **Buka Dolphin baru** (`dolphin --new-window --style kvantum`).

---

## Bagian 4 — Aplikasi GUI Kustom *Aether Panel Studio*

### 4.1 Peran & Fitur Utama
**Aether Panel Studio** (dibangun dengan **Python 3 + PyQt5**) adalah pusat kendali visual lokal yang mengubah pengaturan slider/color picker/file gambar menjadi konfigurasi KDE, SVG, Kvantum, dan QML tanpa pengguna perlu mengedit file kode atau Inkscape manual.
- **Delapan Tab Kontrol:** `Panel`, `Shadow`, `Ikon aplikasi`, `Popup`, `Jendela & Blur`, `Bilah judul`, `Layar kunci & Logo`, dan `Splash Screen`.
- **Preset Bawaan & Backup Aman:** Mendukung preset (`Liquid Blue`, `Crystal`, `Ocean`, `Midnight`), ekspor/impor JSON, serta membuat cadangan otomatis sebelum menerapkan perubahan ke `~/theme-backups/AetherPanelStudio/`, `~/theme-backups/AetherBranding/`, `~/theme-backups/AetherSplashStudio/`, dan `~/theme-backups/AetherTitlebar/`.

### 4.2 Peta Lengkap Fitur -> Kode Sumber -> File Hasil

| Fitur di Antarmuka | Berkas & Fungsi Sumber (`/opt/AetherPanelStudio/`) | Berkas Tujuan / Hasil di Akun Pengguna |
|---|---|---|
| **Panel terpisah adaptif** | `app.py` (`FIELDS`), `backend.py` (`DEFAULTS`, `CONFIG_KEYS`), `data/main.qml` (`updateBackgrounds`) | `plasma-org.kde.plasma.desktop-appletsrc` (`splitPanel=1`), widget `org.aether.panelislands` |
| **Transparansi, radius, padding, shadow panel** | `data/main.qml` (`backgroundComponent`), `data/main.xml`, `backend.py` | Key layout Plasma: `backgroundOpacity`, `cornerRadius`, `padding`, `shadow*` |
| **Highlight aplikasi & tray** | `backend.py` (`write_theme` / `update_frames`) | `Aeos/widgets/tasks.svg` & `Aeos/widgets/tabbar.svg` |
| **Popup, menu Home & tooltip rounded** | `backend.py` (`write_theme` / `write_tooltip`) | `Aeos/dialogs/background.svg`, `widgets/background.svg`, `tooltip.svg` |
| **Blur jendela & panel** | `backend.py` (`configure_blur`), `panel_blur.py`, `compat-blur/blur.cpp` | `~/.config/kwinrc`, region blur X11, plugin `aether-compat-blur-v6.so` |
| **Transparansi jendela Qt & Dolphin** | `backend.py` (`write_kvantum`) | `~/.config/Kvantum/AetherGlass/AetherGlass.kvconfig` & `AetherGlass.svg` |
| **Warna & tepi bilah judul** | `titlebar.py` (`TitlebarColors.apply`) | `~/.local/share/aurorae/themes/Aeos-Blur/decoration.svg` |
| **Wallpaper desktop** | Plasma *Configure Desktop* | `plasma-org.kde.plasma.desktop-appletsrc` (key `Image`) |
| **Background & logo tengah Lock Screen** | `branding.py` (`Branding.apply`) | `branding/background.png`, `branding/lockLogo.png`, `~/.config/kscreenlockerrc` |
| **Logo Home & System Information** | `branding.py` (`Branding.apply`) | Widget Kickoff, `branding/homeLogo.png`, `~/.config/kcm-about-distrorc` (`LogoPath`) |
| **Penghapusan lingkaran di belakang logo** | `branding.py` (`patch_user_delegate`) | `UserDelegate.qml` pada Lock (`org.aether.lockstudio`), Logout (`Aeos`), & SDDM (`aether-sddm`) |
| **Layar Login SDDM** | `branding.py` (`build_sddm_theme`), `apply-sddm-branding.sh` (`pkexec`) | `/usr/share/sddm/themes/aether-sddm/`, `/etc/sddm.conf.d/zz-aether-branding.conf` |
| **Splash Screen Plasma** | `splash.py` (`build_package` / `_qml`) | `~/.local/share/plasma/look-and-feel/org.aether.splashstudio/` (`Splash.qml`), `~/.config/ksplashrc` |

*(Catatan arsitektur dari `docs/struktur.md`: template QML widget di `modules/05-panel-studio/.../AetherPanelStudio/data/` dan widget terpasang di `modules/04-panel-terpisah/.../org.aether.panelislands/` harus tetap sinkron agar tombol Terapkan di Studio tidak menimpa perubahan panel).*

---

## Bagian 5 — Sistem Branding Berlapis (*Boot* hingga *Installer*)

### 5.1 Membedakan 4 Layar KDE yang Sering Tertukar
1. **Layar Kunci (*Lock Screen* — `Meta+L`):** Dikendalikan `KScreenLocker` via `~/.config/kscreenlockerrc` menunjuk ke paket `org.aether.lockstudio` (`background.png` dan `lockLogo.png`).
2. **Dialog Konfirmasi Logout:** Berada pada Look-and-Feel aktif (`Aeos/contents/logout/` & `Aeos/contents/components/`), memakai `UserDelegate.qml` tanpa lingkaran.
3. **Layar Login (`SDDM`):** Muncul setelah boot awal atau setelah logout selesai. Menggunakan `/usr/share/sddm/themes/aether-sddm/` dengan aktivasi di `/etc/sddm.conf.d/zz-aether-branding.conf` (`Current=aether-sddm`) serta jalur relatif `Qt.resolvedUrl("../lockLogo.png")` agar greeter tidak tergantung akses folder home pengguna.
4. **Splash Screen Plasma (`KSplash`):** Muncul sesudah login saat Plasma memuat (`org.aether.splashstudio`, `ksplashrc`). Dirancang dengan overlay lapisan gelap/hitam **60%** agar wallpaper latar redup, teks biru terang kontras tinggi, garis progress bar, serta font **Urbanist** (`"Aether Desktop"` / `"Menyiapkan desktop…"`).
- **Penanganan Avatar Bulat & Kabut Putih:** Helper `patch_user_delegate(...)` menghapus bidang lingkaran, mask shader bulat, dan bingkai tepi pada `UserDelegate.qml` sehingga logo PNG `512x512` tampil utuh sesuai transparansinya. Sementara itu, fenomena *kabut putih* terdiagnosis berasal dari properti `contrast`, `saturation`, dan `intensity` pada `WallpaperFader.qml` (telah didokumentasikan panduan penyesuaiannya ke `contrast: 1.0`, `saturation: 1.0`, `intensity: 1.0 - 0.4 * wallpaperFader.factor` agar tetap redup gelap tanpa pemutihan, dengan catatan tidak ditimpa paksa bila user mengedit tema manual).

### 5.2 Branding Level ISO (GRUB, Plymouth & Calamares Installer)
- **GRUB Menu Boot ISO (`payloads/grub.cfg` -> `custom-disk/boot/grub/grub.cfg`):** Mengubah seluruh entri boot Kubuntu menjadi **"Try or Install Aether OS"**, **"Aether OS (safe graphics)"**, dan **"OEM install (for manufacturers)"**.
- **Boot Splash Kernel (`Plymouth`):** Memasang tema `/usr/share/plymouth/themes/aether-logo/aether-logo.plymouth` sebagai default via `update-alternatives` (prioritas 200) dan mengompilasinya ke `initrd.img-7.0.0-31-generic` via `update-initramfs -u`.
- **Installer & Live Prompt (`apply-installer-brand.sh`, `aether-installer-prompt.py`):** Menghapus 12 slide Kubuntu di `/etc/calamares/branding/kubuntu/`, mengganti ikon, logo, dan `branding.desc`/`show.qml` ke **Aether OS**, serta mengganti `/usr/bin/kubuntu-installer-prompt` dengan dialog PyQt5 custom *Try Aether OS* / *Install Aether OS*.

---

## Bagian 6 — Integrasi *Agentic AI Harness* & *Offline Voice* (`Sesi 09`)

Seluruh ekosistem AI dipasang secara system-wide oleh skrip `scripts/install-aether-ai.sh` ke direktori sistem agar dapat dipakai dari akun Live (`kubuntu`) maupun user baru:

| Komponen | Lokasi & Metode Instalasi | Fungsi Utama |
|---|---|---|
| **Antigravity CLI (`agy`)** | `/usr/local/bin/agy` (`237 MB`, disalin dari `private-assets/bin/agy`) | Agentic coding & sistem CLI utama |
| **OpenAI Codex (`codex`)** | `/usr/local/bin/codex` -> `@openai/codex` (`npm install -g`) | Coding agent berbasis terminal |
| **OpenCode (`opencode`)** | `/usr/local/bin/opencode` -> `opencode-ai` (`npm install -g`) | AI coding CLI alternatif |
| **Hermes Agent (`hermes`)** | `/opt/hermes-agent` + `/opt/hermes-venv`, symlink `/usr/local/bin/hermes` | Agentic assistant lokal/CLI |
| **Voice Offline (`aether-voice`)** | `/usr/local/bin/aether-voice` + venv `/opt/aether-venv` + model **`faster-whisper` `small`** (`int8`, ~461 MB blob di `/opt/aether-models/whisper`, env `AETHER_WHISPER_MODEL_DIR`) | Transkripsi suara-ke-teks secara lokal tanpa koneksi internet |
| **Browser Automation** | `playwright` (`/usr/local/bin/playwright`) + Chromium (`chromium-1255` `414M`, `chromium_headless_shell-1255` `282M`, env `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`) | Navigasi & otomasi web terprogram |
| **Desktop & Terminal Control** | APT: `xdotool`, `wmctrl`, `scrot`, `xclip`, `qdbus-qt5`, `jq`, `ripgrep`, `tmux`, `libnotify-bin`, `curl`, `git` (`2.43.0`), `portaudio19-dev`, `python3-venv`, `nodejs`, `npm` | Memampukan agen mengendalikan jendela X11, mengambil screenshot, clipboard, dan D-Bus KDE |

---

## Bagian 7 — Alur Remastering Modular Cubic (`Sesi 00` – `11`) & Debugging Akhir

### 7.1 Daftar Lengkap 12 Sesi Remastering (`Galszes/Aether-OS`)

| Sesi | Nama Modul | Ringkasan Langkah Teknis di Chroot Cubic |
|---|---|---|
| **00** | `00-persiapan` | `apt-get update`, `purge` **6 paket bloatware** (`kmines`, `kpat`, `ksudoku`, `kmahjongg`, `kubuntu-wallpapers`, `plasma-workspace-wallpapers`) + `autoremove`, install `python3-pyqt5`, `qt5-style-kvantum`, `fonts-ibm-plex`, backup `/etc/skel`, pasang hook `00-aether-remaster-relocate.sh` + `relocate.py`. |
| **01** | `01-font` | Salin font ke `/usr/local/share/fonts/`, jalankan `fc-cache -f`, salin `fonts.conf` & `kcmfonts`, gabung fragmen font ke `kdeglobals` lewat `merge-kconfig.py`. |
| **02** | `02-ikon` | Salin `Vivid-Glassy-Dark-Icons` ke `/usr/share/icons/`, gabung `[Icons] Theme` ke `kdeglobals`. |
| **03** | `03-appearance-glass` | Pasang `Aeos`, `Aeos-Blur`, Kvantum `AetherGlass`, gabung `kdeglobals.ini`, `kwinrc.ini`, `plasmarc.ini`, serta pasang `aether-compat-blur` opsional untuk KWin X11 `5.27.11`. |
| **04** | `04-panel-terpisah` | Pasang plasmoid `org.aether.panelislands` dan gabung tata letak panel (`splitPanel=1`, jam, baterai, spacer) via `merge-kconfig.py`. |
| **05** | `05-panel-studio` | Pasang source aplikasi `AetherPanelStudio` dan `.desktop` launcher-nya. |
| **06** | `06-wallpaper-branding` | Pasang wallpaper 4K, tema SDDM `aether-sddm` + `zz-aether-branding.conf`, aset lock/Home, `kcm-about-distrorc`, dan config layout wallpaper. |
| **07** | `07-splash` | Pasang paket Look-and-Feel `org.aether.splashstudio` dan `ksplashrc`. |
| **08** | `08-konsole` | Salin profil terminal `Aether Glass.profile`, `AetherGlass.colorscheme`, `AetherGlass.css`, dan `konsolerc`. |
| **09** | `09-ai-harness` | Jalankan `scripts/install-aether-ai.sh` untuk memasang `agy`, `codex`, `hermes`, `opencode`, `aether-voice` + Whisper `small`, Playwright Chromium, dan tool kontrol X11. |
| **10** | `10-branding-dan-fix` | Jalankan berurutan `apply-hotfix.sh` (Plymouth) -> `apply-blur-fix.sh` (GLX & blur v6) -> `apply-desktop-sync.sh` -> `apply-installer-brand.sh` (Calamares & PyQt5 Prompt) -> `apply-panel-studio-fix.sh` -> `polish-aether.sh` (`qdbus-qt5`, `aether-voice`, `update-initramfs`). |
| **11** | `11-build-iso` | Perbarui `boot/grub/grub.cfg` pada tab Boot Cubic mengikuti `payloads/grub.cfg` (*Try or Install Aether OS*), lalu generate ISO. |

### 7.2 Mekanisme Anti-Timpa & Relokasi User Baru
- **`tools/merge-kconfig.py`:** Menggabungkan fragmen INI per grup/key ke file target di `/etc/skel/.config/` (`kdeglobals`, `kwinrc`, `plasmarc`, `plasma-org.kde.plasma.desktop-appletsrc`) sehingga sesi sebelumnya tidak tertimpa utuh.
- **`relocate.py`:** Hook pre-Plasma yang memindai sisa string `/home/aether` di config user baru dan menggantinya dengan path `$HOME` aktif.
- **Kemandirian Repositori (`payloads/` & `.gitignore`):** Ke-4 arsip payload akhir (`aether-blur-fix.tar.gz`, `aether-desktop-sync.tar.gz`, `aether-hotfix.tar.gz`, `aether-installer-brand.tar.gz`) beserta `grub.cfg` disertakan di folder `payloads/`, sementara aset visual berukuran besar (~377 MB) dan binary `agy` (`237 MB`, melebihi batas file tunggal 100 MB GitHub) dikemas dalam arsip Release `aether-kubuntu-remaster-final.tar.gz` dan dikecualikan dari commit Git standar lewat `.gitignore`.

### 7.3 Catatan *Debugging* Teknis Nyata saat Pengujian ISO (VirtualBox)
1. **Tombol *Install Kubuntu* masuk ke *Try Mode*:** Diperbaiki di `apply-installer-brand.sh` & `aether-installer-prompt.py` dengan mengeksekusi langsung `sudo -E calamares -D8` pada tombol *Install Aether OS*.
2. **Widget Aether Panel Studio `"Not Authorized to Execute"` & Error Path `/home/aether`:** Terjadi pada sesi Live (`kubuntu`) karena file `.desktop` di `plasma_icons/` masih `-rw-rw-r--` (tanpa `+x`) dan hardcode ke `/home/aether/.local/bin/aether-panel-studio`. Diselesaikan lewat `apply-panel-studio-fix.sh`: memindahkan aplikasi ke `/opt/AetherPanelStudio/`, membuat wrapper global `/usr/local/bin/aether-panel-studio`, dan menyetel `chmod 755` + `chown root:root` pada semua `.desktop`.
3. **Transfer ISO Besar Melewati Shared Folder `vboxsf`:** Penulisan berkas tunggal >500 MB pada VirtualBox shared folder (`vboxsf`) berisiko korup/gagal; solusinya ISO `~6.6 GB` dipecah per `350 MB` (`split -b 350M -d -a 3`) beserta skrip penggabung `GABUNG_DI_WINDOWS.bat`, serta penyiapan arsip `tar.gz` dilakukan langsung di partisi `ext4` sebelum dipindahkan agar symlink Linux utuh.
4. **Ketergantungan Server HTTP Lokal (`127.0.0.1:8765`):** Skrip `scripts/apply-*.sh`, `install-aether-ai.sh`, dan `polish-aether.sh` direfaktor agar membaca langsung dari `../payloads/` dan `../private-assets/bin/agy` secara lokal, lolos verifikasi `bash -n`, `py_compile`, dan `tar -tzf`.
5. **Status & Batasan Terbuka:** Plugin kompatibilitas blur (`aether-compat-blur-v6.so`) menargetkan KWin X11 `5.27.11`; perilaku di Wayland atau GPU berbeda dapat bervariasi. Selain itu, launcher taskbar **Hermes** pada uji Live ISO v5 sempat memunculkan gejala keluar cepat dari Konsole (perlu pemeriksaan runtime `--hold`/setup awal di build uji berikutnya), dan setiap ISO hasil generate baru wajib melewati uji boot Live serta uji instalasi VM penuh.
