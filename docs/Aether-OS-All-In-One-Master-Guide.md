# AETHER OS — Dokumen Master *All-In-One* (Dari 0 Hingga ISO Final)

**Ringkasan Proyek:** Remastering **Kubuntu 24.04.5 LTS (*Noble Numbat*, x86_64)** berbasis **KDE Plasma 5.27** menggunakan **Cubic** menjadi **Aether OS** (*codename: Genesis*) dengan tema *frosted/liquid glass*, *Panel Islands*, aplikasi editor GUI kustom **Aether Panel Studio**, branding menyeluruh (*GRUB -> Plymouth -> SDDM -> Splash -> Lock/Logout -> Calamares Installer*), serta **Agentic AI Harness** & **Voice-to-Text offline** siap pakai.

**Cakupan Dokumen:** Menggabungkan **seluruh riwayat pekerjaan, desain, skrip, dan debugging dari awal (4 Nov)** bersama **Codex** (`01a1a5cf`, `01a1a611`, `01a1a738`, `01a1ca91`, `Rangkuman-Aether-Panel-Studio-2026-11-11.md`, `Tutorial-Lengkap-Modifikasi-Kubuntu-Aether.md`, `Panduan-Aether-Per-Sesi.md`, `peta-fitur-ke-kode.md`, `Briefing-Video-Demo-Aether-OS.md`) **dan** bersama **Antigravity** (`13–18 Nov`, instalasi AI Harness, Plymouth/GRUB/Calamares, blur fix v6, desktop sync, GitHub `https://github.com/Galszes/Aether-OS`, hingga pengujian VirtualBox `aetheros-v5`).

---

## DAFTAR ISI CEPAT (Navigasi Tanya-Jawab Utama)
1. **Bab 1:** Visi Awal, Spesifikasi Lingkungan, & Konsep Inti Remastering (`/etc/skel` vs `/` vs `custom-disk`)
2. **Bab 2 [Menjawab Pertanyaan #1]:** Cara Mengedit Wallpaper Default, Logo Boot (Plymouth), Semua Logo (Home, Info Center, Lock, Logout, SDDM), Splash Screen, Panel Islands, Blur KWin, Font, & Aether Panel Studio
3. **Bab 3 [Menjawab Pertanyaan #2]:** Cara Mengubah Logo Installer (Calamares) & Tampilan *"Try or Install Ubuntu/Kubuntu"* (GRUB + `kubuntu-installer-prompt`)
4. **Bab 4 [Menjawab Pertanyaan #3]:** Cara Memasukkan Package, Tool, & AI Harness ke dalam ISO beserta Fungsi Lengkap Masing-Masing
5. **Bab 5:** Pembuangan Bloatware & Urutan Eksekusi Modular Lengkap di Cubic (`Sesi 00` – `11`)
6. **Bab 6:** Log *Troubleshooting* & *Debugging* Nyata (Riwayat Codex + Antigravity v1 s/d v5)
7. **Bab 7:** Daftar Perintah Wajib & Bank Tanya-Jawab Presentasi/Sidang

---

## BAB 1 — Visi Awal, Lingkungan Sistem, & Prinsip Remastering dari 0

### 1.1 Visi & Sejarah Singkat (Codex -> Antigravity)
- **Ide Awal (`4 Nov`, Sesi Codex `01a1a5cf` & `01a1a611`):** Membangun distro Linux remaster Kubuntu 24.04 yang bertema *Agentic AI OS* dengan estetika desktop modern (taskbar terpisah transparan *rounded*, tanpa teks pixelated, tanpa *empty space* panel yang sia-sia) dan siap memuat agen AI (`Hermes`, `Antigravity`, `OpenCode`, `Codex`).
- **Fase 1 (`4–11 Nov`, Codex):** Eksperimen langsung pada SVG Plasma (`panel-background`, `tasks.svg`, `tabbar.svg`), perancangan widget `org.aether.panelislands`, lahirnya aplikasi PyQt5 **Aether Panel Studio**, investigasi blur KWin pada SVGA3D, normalisasi transparansi Dolphin di Kvantum `AetherGlass`, pemisahan 4 layar branding, serta pemulihan `agy` ke versi resmi `1.5.5` (sesi `01a1c9a1` setelah binary host sempat korup saat *auto-update*). Awalnya dikemas sebagai `Aeos-Remastering-Theme` (`4 Nov`, `install-to-system.sh`), lalu `Aeos-Remastering-Backup` (`7 Nov`), dan snapshot `Aether-Cubic-Remaster-20261111-172054` / `175706` (`11 Nov`).
- **Fase 2 (`11–13 Nov`, Codex):** Modularisasi ke repositori `aether-kubuntu-remaster/` dengan fragmen konfigurasi INI (`tools/merge-kconfig.py`), hook relokasi akun baru (`relocate.py`), PDF panduan per sesi (`tools/build-pdf.py`), checksum `MANIFEST.json`, dan *Briefing Video Demo*. *(Pada fase ini, modul baru mencakup tampilan desktop; AI Agents belum masuk ISO).*
- **Fase 3 (`14–18 Nov`, Antigravity):** Implementasi penuh di Cubic (`kubuntu-24.04.5-desktop-amd64.iso`), penghapusan game & wallpaper Kubuntu, pemasangan sistem **Agentic AI Harness** (`Sesi 09`), pemasangan **Plymouth `aether-logo`**, perbaikan `initramfs` + `vmlinuz`, perbaikan blur VirtualBox 3D Acceleration (`aether-compat-blur-v6.so` + GLX), branding **GRUB & Calamares (*Try or Install Aether OS*)**, sinkronisasi launcher taskbar AI & widget desktop, perbaikan permission `.desktop` Panel Studio (`Sesi 10`), serta pengemasan repo mandiri di `https://github.com/Galszes/Aether-OS`.

### 1.2 Spesifikasi Lingkungan Pengembangan & Target Build
| Komponen | Nilai Aktual |
|---|---|
| **Host Fisik** | Windows 11 · CPU Ryzen 3 seri 7000 (iGPU AMD) |
| **Mesin Virtual** | VirtualBox · Adapter **VMSVGA** · 3D Acceleration ON/OFF · VRAM 256 MB |
| **Base ISO** | `kubuntu-24.04.5-desktop-amd64.iso` (Ubuntu 24.04.5 LTS *Noble Numbat*, `x86_64`) |
| **Desktop & Compositor** | KDE Plasma `5.27` · Sesi **X11** · KWin `5.27.11` · Qt `5.15.13` |
| **Renderer OpenGL Guest** | `VMware, Inc.` (`SVGA3D; build: RELEASE; LLVM;`), Mesa `25.2.8`, OpenGL `4.1, GLX` |
| **Kernel Target ISO** | `7.0.0-31-generic` |
| **Remaster Tool** | **Cubic** versi `2026.09.110` (menyimpan proyek di disk terpisah `/dev/sdb1`) |

### 1.3 Mengapa Pemisahan Direktori ISO Sangat Krusial? (Prinsip Kerja dari 0)
Saat mengedit ISO di Cubic, perubahan di akun pribadi `/home/aether` **tidak otomatis ikut ke ISO** dan bahkan akan **rusak** saat diboot di Live ISO (yang memakai user bernama `kubuntu`) atau di-install dengan nama user lain. Karena itu digunakan 3 lapisan path berbeda:
1. **`custom-root/etc/skel/` (Template Home User Baru):**
   Ubuntu/Calamares/Casper otomatis menyalin seluruh isi `/etc/skel/` ke `/home/<nama_user>` setiap kali sesi Live berjalan atau akun baru dibuat. Semua config desktop (`kdeglobals`, `kwinrc`, `plasmarc`, `plasmashellrc`, `kactivitymanagerdrc`, `plasma-org.kde.plasma.desktop-appletsrc`), widget Plasma (`org.aether.panelislands`, `org.aether.lockstudio`, `org.aether.splashstudio`), tema Kvantum/Aurorae, `aether-compat-blur-v6.so`, dan wallpaper ditaruh di `/etc/skel/`.
2. **`custom-root/opt/` & `/usr/local/bin/` & `/usr/share/` (Sistem Global / Lintas User):**
   Binary aplikasi, AI Agent (`agy`, `codex`, `hermes`, `opencode`), venv Python (`/opt/aether-venv`, `/opt/hermes-venv`), model offline (`/opt/aether-models/whisper`), Chromium Playwright (`/opt/pw-browsers`), GUI `/opt/AetherPanelStudio`, ikon global (`Vivid-Glassy-Dark-Icons`, `aether-ai`), SDDM (`aether-sddm`), Plymouth (`aether-logo`), dan Calamares (`etc/calamares/branding/kubuntu/`).
3. **`custom-disk/` (Struktur Luar SquashFS / Menu Boot ISO):**
   Menu GRUB (`boot/grub/grub.cfg` & `loopback.cfg`), kernel `casper/vmlinuz`, dan `casper/initrd.gz`.

**Hook Relokasi Path (`00-aether-remaster-relocate.sh` + `/usr/local/lib/aether-remaster/relocate.py`):**
Karena beberapa file konfigurasi KDE menyimpan path absolut `/home/aether/...` (seperti path wallpaper dan logo Home di `plasma-org.kde.plasma.desktop-appletsrc` dan `kcm-about-distrorc`), **sebelum Plasma start**, skrip di `/etc/skel/.config/plasma-workspace/env/00-aether-remaster-relocate.sh` menjalankan `relocate.py "$HOME"` yang mengganti setiap teks `b'/home/aether'` di `.config/`, `.local/share/`, dll. menjadi path `$HOME` milik user yang sedang login (misal `/home/kubuntu`) lalu membuat penanda `~/.config/.aether-remaster-paths-v1`.

---

## BAB 2 — [Pertanyaan #1] Cara Mengedit Wallpaper Default, Logo Boot, Semua Logo, Splash Screen, & Modifikasi Desktop

Bagian ini menjawab secara tuntas: *"Gimana kamu edit wallpaper default, logo boot, semua logo, splash screen dan semua modifikasi itu?"*

### 2.1 Mengubah Wallpaper Default
- **File Gambar:** `wallhaven-jer33w_3840x2160.png` (resolusi 4K, 8,7 MB — berasal dari `private-assets/wallpaper/`) disalin ke `/etc/skel/Downloads/wallhaven-jer33w_3840x2160.png`.
- **Konfigurasi Desktop Plasma:** Key `Image=/home/aether/Downloads/wallhaven-jer33w_3840x2160.png` ditulis di `/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc` (dan digabung fragmennya di Sesi `06`).
- **Mengapa Sempat Gagal di Build v1 (dan Bagaimana Diselesaikan):**
  Di build ISO pertama, wallpaper yang muncul masih wallpaper default dan widget jam *ClearClock* tidak muncul karena pengaturan wallpaper + widget desktop terikat pada **Activity ID** di KDE. Tanpa file **`kactivitymanagerdrc`**, Plasma di Live ISO membuat Activity baru yang kosong. Setelah `kactivitymanagerdrc` ikut dibundel (via `aether-hotfix.tar.gz` / `aether-desktop-sync.tar.gz`) bersama `relocate.py` (yang mengubah `/home/aether/` -> `/home/<user>/`), wallpaper 4K dan widget jam langsung tampil identik.
- **Penghematan ISO:** Paket `kubuntu-wallpapers` (~188 MB) dan `plasma-workspace-wallpapers` (~93 MB) dihapus tuntas dengan `apt-get purge`.

### 2.2 Mengubah Logo Booting Awal (*Plymouth Boot Splash*)
Animasi logo yang muncul **segera setelah menu GRUB** (saat kernel Linux memuat sebelum layar login) dikendalikan oleh **Plymouth**, bukan KSplash atau SDDM.
1. **Aset & Definisi Tema:** Disiapkan paket tema di `/usr/share/plymouth/themes/aether-logo/` (termasuk `aether-logo.plymouth`, `watermark.png`, `progress-00.png`, animasi 16 frame `throbber-0001.png` s/d `throbber-0016.png`, serta aset dialog password disk `lock.png`, `entry.png`, `bullet.png`).
2. **Konfigurasi `aether-logo.plymouth`:** Memakai modul `ModuleName=two-step` dengan latar hitam murni (`BackgroundStartColor=0x000000`, `BackgroundEndColor=0x000000`), progress bar biru `0x479cff`, dan `ImageDir=/usr/share/plymouth/themes/aether-logo`.
3. **Registrasi & Aktivasi (`update-alternatives`):**
   ```bash
   update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth 200
   update-alternatives --set default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth
   ```
4. **Kompilasi ke `initramfs` (`update-initramfs`):**
   ```bash
   update-initramfs -u   # atau update-initramfs -c -k 7.0.0-31-generic
   ```
   **Mengapa wajib?** Karena Plymouth berjalan *sebelum* partisi root utama selesai di-mount. Tema `aether-logo` harus masuk ke dalam berkas `/boot/initrd.img-7.0.0-31-generic` (86 MB) yang nantinya dikemas Cubic ke `casper/initrd.gz` pada halaman *Kernel*.

### 2.3 Mengubah "Semua Logo" (Karena di KDE Terdiri dari 4 Komponen Terpisah!)
Di KDE Plasma 5, mengganti logo di satu tempat **tidak otomatis** mengganti logo di tempat lain karena masing-masing komponen membaca aset & file QML berbeda:

| Komponen Logo | Lokasi Tampil | Cara Mengubah & File Terkait |
|---|---|---|
| **1. Logo Home (Kickoff) & Info Center** | Tombol kiri bawah taskbar, pojok kiri atas menu *Application Launcher*, & halaman *System Information* | - Aset disimpan di `~/.local/share/aether-panel-studio/branding/homeLogo.png` (`512x512` PNG transparan).<br>- Ikon Kickoff disetel pada key `icon=` di `plasma-org.kde.plasma.desktop-appletsrc`.<br>- Logo System Information disetel di `/etc/skel/.config/kcm-about-distrorc` (`LogoPath=/home/aether/.local/share/aether-panel-studio/branding/homeLogo.png`, yang otomatis direlokasi oleh `relocate.py`). |
| **2. Logo Tengah Layar Kunci (*Lock Screen* `Meta+L`)** | Muncul saat layar dikunci | - Mengganti tema *KScreenLocker* via `/etc/skel/.config/kscreenlockerrc` -> `Theme=org.aether.lockstudio`, `WallpaperPlugin=org.kde.image`.<br>- Paket berada di `~/.local/share/plasma/look-and-feel/org.aether.lockstudio/`, membaca `background.png` dan `lockLogo.png`. |
| **3. Logo Dialog Konfirmasi *Logout*** | Layar Logout / Restart / Shutdown | - Mengubah komponen pada Look-and-Feel aktif: `~/.local/share/plasma/look-and-feel/Aeos/contents/logout/` & `contents/components/` agar selaras dengan `lockLogo.png`. |
| **4. Logo Layar Login (*SDDM Greeter*)** | Muncul saat boot awal & setelah Logout | - Tema ditaruh di direktori sistem `/usr/share/sddm/themes/aether-sddm/` (memuat `background.png` dan `lockLogo.png` dengan path relatif `Qt.resolvedUrl("../lockLogo.png")` agar akun user `sddm` bisa membacanya tanpa mengakses `/home/`).<br>- Diaktifkan melalui override `/etc/sddm.conf.d/zz-aether-branding.conf`: `[Theme] Current=aether-sddm`.<br>- Dipasang dari Studio via helper `apply-sddm-branding.sh` (`pkexec`). |

**Teknik Penting — Menghilangkan Bingkai Lingkaran Avatar Breeze (`patch_user_delegate`):**
Secara default, Breeze membungkus logo tengah dengan bidang lingkaran + *mask shader* bulat + bingkai tepi. Helper `patch_user_delegate(...)` di `branding.py` memodifikasi `contents/components/UserDelegate.qml` (di `org.aether.lockstudio`, `Aeos`, dan `aether-sddm`) untuk menghapus mask bulat tersebut dan memakai `Image.PreserveAspectFit`, sehingga logo PNG Aether tampil utuh tanpa terpotong lingkaran.

**Diagnosis *Kabut Putih* (`WallpaperFader.qml`):**
Pada dokumentasi Codex tercatat bahwa efek "kabut putih" saat prompt login/lock muncul berasal dari properti `contrast`, `saturation`, dan `intensity` bawaan `WallpaperFader.qml`. Solusi yang didokumentasikan (untuk edit manual tema) adalah menyetel `contrast: 1.0`, `saturation: 1.0`, `intensity: 1.0 - 0.4 * wallpaperFader.factor` (atau `0.6` agar lebih gelap) pada `org.aether.lockstudio` dan `aether-sddm`.

### 2.4 Mengubah Splash Screen Plasma (`KSplash`)
*Splash Screen* adalah layar pemuatan singkat **setelah login SDDM** saat sesi Plasma sedang dimulai (`Sesi 07`):
- Diaktifkan di `/etc/skel/.config/ksplashrc`: `Theme=org.aether.splashstudio`, `Engine=KSplashQML`.
- Paket berada di `/etc/skel/.local/share/plasma/look-and-feel/org.aether.splashstudio/`.
- **Isi Desain (`splash.py` generator):** Menggunakan file `Splash.qml` dengan gambar latar, logo transparan, judul (`"Aether Desktop"`), subjudul (`"Menyiapkan desktop…"`), font **Urbanist**, teks biru terang kontras tinggi + garis progress biru, dan **lapisan overlay hitam 60%** (menggantikan lapisan biru sebelumnya) untuk meredupkan background agar teks terbaca jelas.

### 2.5 Modifikasi Desktop Lainnya (Panel Islands, Ikon, Tema Glass, Blur, Font, Konsole, & Studio)
1. **Taskbar Terpisah Adaptif — *Panel Islands* (`Sesi 04`):**
   - Widget `org.aether.panelislands` (`data/main.qml`, `splitPanel=1`) berjalan di dalam **1 kontainer panel Plasma** selebar layar (bukan mode Auto Hide, bukan 2 panel OS terpisah).
   - `updateBackgrounds` menggambar latar rounded terpisah untuk blok kiri (Launcher + 5 ikon taskbar + margin separator) dan blok kanan (System Tray + applet baterai mandiri + jam-tanggal bertumpuk vertikal).
   - Spacer tengah (*Flexible Spacer*) dibiarkan transparan tanpa latar sehingga lebar pulau kiri dinamis mengikuti jumlah aplikasi yang terbuka.
   - Geometri sudut dirapikan dengan rumus **`inner corner + margin = outer corner`** pada `Aeos/widgets/tasks.svg` (highlight aplikasi) dan `Aeos/widgets/tabbar.svg` (memperbaiki indikator biru tombol *Show Hidden Icons* agar tidak menembus sudut rounded). Nilai referensi panel Studio saat pengujian panel adalah 23% opasitas (~77% transparan).
   - Ketebalan dan mode mengambang taskbar disinkronkan di `/etc/skel/.config/plasmashellrc`.
2. **Tipografi Anti-Pixelated (`Sesi 01`, `04`, `08`):**
   - Font global: **Google Sans (11 pt)** · Taskbar & WM: **IBM Plex Sans (11 pt)** · Jam digital: **Urbanist (12 pt, Medium Italic)** · Konsole terminal (`Aether Glass.profile`): **IBM Plex Mono**. Cache dibangun via `fc-cache -f`, aturan anti-aliasing di `fontconfig/fonts.conf` & `kcmfonts`.
3. **Tema Berlapis, Color Scheme, Bilah Judul, Konsole Kaca, GTK & Ikon (`Sesi 02`, `03`, `08`):**
   - **Color Scheme (`Aeos.colors`) & GTK:** Palet dark blue-slate dengan warna aksen `#4e6cb1` (`RGB 78, 108, 177`) dan teks `#d7f1f8`, disinkronkan pula ke tema GTK 3.0 & GTK 4.0 (`/etc/skel/.config/gtk-3.0/` & `gtk-4.0/`: `settings.ini`, `colors.css`, `gtk.css`, `window_decorations.css`) serta `gtkrc`/`gtkrc-2.0` agar aplikasi non-Qt tampil seragam.
   - **Ikon, Plasma Style & Dekorasi Jendela (`Aeos-Blur`):** **Vivid Glassy Dark Icons** (`/usr/share/icons/Vivid-Glassy-Dark-Icons`), **Aeos** (Plasma shell & popup: desain awal `panelBackground` `#174568` `38%`, `tasks.svg` 9-slice radius `10 px` `#479cff` `24%`, `dialogs/background.svg` `#174568` `48%`, tooltip rounded `14–18 px` beserta mask blur-nya; serta snapshot terbaru di `aether-panel-studio.json` dengan `popupColor=#252525` `52%`, `highlightColor=#ffffff` `32%` radius `18`, `blurStrength=15`, `windowOpacity=40`), **Aeos-Blur** (dekorasi *bilah judul/titlebar* Aurorae diduplikasi dari *Gently-Blur*, sehingga warna bar atas aplikasi & garis tepi bisa diubah dari tab *Bilah judul* tanpa terpaku biru default), dan **Kvantum `AetherGlass`** (aplikasi Qt/Dolphin).
   - **Terminal Konsole Kaca (`Sesi 08`):** Profil kustom `Aether Glass.profile`, skema warna `AetherGlass.colorscheme`, `AetherGlass.css`, serta `konsolerc` dengan transparansi & blur latar terminal.
   - **State JSON & Avatar Default:** Ketiga state editor Studio tersimpan di `/etc/skel/.config/` (`aether-panel-studio.json`, `aether-panel-branding.json`, `aether-splash-studio.json`), dilengkapi `.face` -> `.face.icon` (`23.910` bytes).
4. **4 Custom/Overridden Plasmoid & Widget Desktop Bebas Grid (`plasma-org.kde.plasma.desktop-appletsrc`):**
   - Bundel plasmoid di `/etc/skel/.local/share/plasma/plasmoids/` mencakup `org.aether.panelislands` (pulau panel), `org.kde.plasma.clearclock` (widget jam desktop transparan), `org.kde.plasma.kickoff` (menu Home transparan/blur), dan `org.kde.plasma.private.systemtray` (popup hidden icons & tray).
   - **Shortcut Panel Studio di Desktop (`org.kde.plasma.icon`):** Awalnya berupa shortcut *Folder View* (terkunci ke grid `5 x 11`), lalu diubah menjadi widget Desktop `org.kde.plasma.icon` (`aether-panel-studio-widget.desktop`) dengan `Name=` berisi karakter kosong (*zero-width space* `U+200B`) sehingga tampil ikon logo Aether bersih tanpa label teks dan dapat digeser bebas piksel-per-piksel.
5. **Solusi Blur KWin di VM & Transparansi Dolphin:**
   - **Temuan Riset Codex (`diagnostics/`):** Pada driver guest VirtualBox `SVGA3D`, slider blur bawaan KWin (strength 1 s/d 8) gagal memblur konten di belakang jendela (ketajaman garis pola uji tetap `23,32`), `llvmpipe` berat karena software rendering, dan `Picom` gagal/tidak akurat. Solusinya adalah menulis efek native C++ **`aether-compat-blur`** (`blur.cpp`, shader 2-pass 17 sampel per lintasan untuk ABI KWin X11 `5.27.11`, terhubung ke `panel_blur.py` untuk blur region panel via X11) yang menurunkan ketajaman pola uji dari **`23,32` -> `1,39`** (**~94% bukti fisik blur**). Iterasi `v5`–`v6` menambahkan *repaint* adegan guna menghilangkan *ghosting* frame serta pengecualian saat **Peek at Desktop** aktif.
   - **Penerapan di ISO (`apply-blur-fix.sh`):** Menyalin `aether-compat-blur-v6.so` ke `/etc/skel/.local/opt/aether-kvantum/.../plugins/`, memuatnya lewat `QT_PLUGIN_PATH` di `/etc/skel/.config/plasma-workspace/env/aether-qt-style.sh`, serta menyetel `kwinrc` (`blurEnabled=false`, `aether-compat-blurEnabled=true`, `GLPlatformInterface=glx`, `BlurStrength=8..15`) agar langsung blur baik saat VirtualBox 3D Acceleration ON maupun OFF.
   - **Transparansi Dolphin (`AetherGlass`):** Mengatur `reduce_window_opacity`, `reduce_menu_opacity`, `transparent_dolphin_view=true` (dengan tint `#18181828`), menormalkan alpha SVG `aether-window-normal` menjadi `1`, dengan rentang konsisten `0` (pekat) s/d `50` (transparan), plus opsi *Buka Dolphin baru* (`dolphin --new-window --style kvantum`).
6. **Aplikasi GUI *Aether Panel Studio* (`Sesi 05` & `10`):**
   - Dibangun dengan Python 3 + PyQt5 berisi 8 tab (`Panel`, `Shadow`, `Ikon aplikasi`, `Popup`, `Jendela & Blur`, `Bilah judul`, `Layar kunci & Logo`, `Splash Screen`), preset (`Liquid Blue`, `Crystal`, `Ocean`, `Midnight`), dan sistem auto-backup (`~/theme-backups/`).
   - File sumber utama: `app.py`, `backend.py`, `panel_blur.py`, `titlebar.py`, `branding.py`, `splash.py`, serta unit test `test_studio.py` & `test_branding.py` (11 tes lulus).

---

## BAB 3 — [Pertanyaan #2] Cara Mengubah Logo Installer & Tampilan *"Try or Install Ubuntu/Kubuntu"*

Bagian ini menjawab secara tuntas: *"Gimana cara kamu ubah logo installer dan tampilan try or install Ubuntu itu?"*

Proses booting hingga instalasi sebenarnya terbagi menjadi **3 komponen berbeda** — seluruhnya sudah diubah dari Kubuntu menjadi **Aether OS**:

### 3.1 Mengubah Menu Boot Hitam Pertama (`GRUB`) — *"Try or Install Aether OS"*
Menu hitam yang pertama kali muncul saat ISO/VM menyala tidak berada di dalam Linux chroot (`custom-root`), melainkan di partisi boot luar ISO (`custom-disk/boot/grub/`):
- **File yang diubah:** `custom-disk/boot/grub/grub.cfg` dan `custom-disk/boot/grub/loopback.cfg` (salinannya disimpan di `payloads/grub.cfg` dan bisa diedit juga lewat tab **Boot** pada Cubic).
- **Perubahan yang dilakukan:** Mengganti seluruh label `menuentry` dari Kubuntu menjadi:
  - `menuentry "Try or Install Aether OS"` -> memuat `/casper/vmlinuz boot=casper --- quiet splash` & `/casper/initrd.gz`
  - `menuentry "Aether OS (safe graphics)"` -> menambahkan parameter `nomodeset`
  - `menuentry "OEM install (for manufacturers)"` -> menambahkan `oem-config/enable=true`

### 3.2 Mengubah Tampilan Pop-up *"Try or Install"* Saat Masuk Live OS (`kubuntu-installer-prompt`)
Ketika mode Live selesai booting, Kubuntu 24.04 menjalankan layanan `start-kubuntu-live-env` yang memanggil `/usr/bin/kubuntu-installer-prompt` — jendela layar penuh yang menanyakan pilihan *Try* atau *Install*.
- **Masalah yang Sempat Ditemukan saat Uji ISO v4 (`15 Nov`):**
  1. Pop-up tersebut masih menampilkan logo & tulisan Kubuntu.
  2. Saat user menekan tombol **Install**, jendela installer malah menutup/gagal dan langsung masuk ke mode **Try**! Penyebabnya: ketika 12 slide PNG bawaan Kubuntu dihapus sebelumnya, file `show.qml` di `/etc/calamares/branding/kubuntu/` ikut terhapus sementara `branding.desc` masih menunjuk `slideshow: "show.qml"`, sehingga Calamares gagal memulai dan jatuh ke sesi Live.
- **Solusi Teknis (`scripts/aether-installer-prompt.py` & `apply-installer-brand.sh`):**
  1. Membackup skrip asli menjadi `/usr/bin/kubuntu-installer-prompt.orig`.
  2. Mengganti `/usr/bin/kubuntu-installer-prompt` (`chmod +x`) dengan aplikasi **PyQt5 fullscreen custom** bertema gelap `#0b1120`:
     - Menampilkan logo `/etc/calamares/branding/kubuntu/icon.png` (`140x140`), judul **"Try or Install Aether OS"**, subjudul **"Aether OS 24.04 LTS — Agentic AI Operating System"**.
     - Tombol **"Try Aether OS"** menutup dialog (`QApplication.quit()`) dan masuk ke Live Desktop.
     - Tombol **"Install Aether OS"** menyembunyikan tombol lalu menjalankan `subprocess.Popen(["sudo", "-E", "calamares", "-D8"])` dan memantau prosesnya sampai selesai.

### 3.3 Mengubah Logo, Warna, & Teks Installer (`Calamares`)
Paket `calamares-settings-kubuntu` dipertahankan, namun seluruh aset & identitas visualnya di `/etc/calamares/branding/kubuntu/` diganti (`aether-installer-brand.tar.gz`):
- **Hapus 12 Slide Lama Kubuntu:** `rm -f /etc/calamares/branding/kubuntu/[0-9][0-9]_*.png` (~18 MB lebih hemat) dan diganti **`show.qml`** kosong yang valid (`91 bytes`: `Presentation { id: presentation }`) agar Calamares tetap berjalan stabil tanpa error QML.
- **Perbarui `branding.desc`:**
  - `productName: Aether OS`, `shortProductName: Aether OS`, `version: 24.04 LTS`, `shortVersion: noble`, `bootloaderEntryName: Aether OS`.
  - Gambar diganti dengan aset Aether: `logo.png`, `icon.png`, `welcome.png`, `welcome-oem.png`.
  - Palet sidebar diubah sesuai tema gelap Aether (`SidebarBackground: "#0f172a"`, `SidebarText: "#FFFFFF"`, `SidebarTextCurrent: "#38bdf8"`).
- **Perbarui Shortcut Desktop Installer:** Pada `/usr/share/applications/kubuntu-calamares.desktop`, teks `Install Kubuntu` diubah menjadi `Install Aether OS` (`sed -i`) dan `Icon=` diarahkan ke `/etc/calamares/branding/kubuntu/icon.png`.

---

## BAB 4 — [Pertanyaan #3] Cara Memasukkan Package, Tool, & AI Harness beserta Fungsi Lengkapnya

Bagian ini menjawab secara tuntas: *"Gimana cara kamu bisa memasukan package, tool, dan harness itu? Apa fungsinya mereka semua?"*

### 4.1 Strategi Memasukkan ke ISO (Supaya Jalan di Live & Semua Akun Baru)
1. **Dijalankan di dalam Terminal `chroot` Cubic:** Semua pemasangan dilakukan di root filesystem calon ISO (`custom-root`), tidak mengotori OS host.
2. **Instalasi System-Wide (Di `/opt/`, `/usr/local/bin/`, `/usr/local/lib/`), BUKAN di `/home/aether/`:**
   - Binary/venv diletakkan di `/opt/aether-venv`, `/opt/hermes-venv`, `/opt/hermes-agent`, `/opt/pw-browsers`, `/opt/aether-models/whisper`, serta symlink executable di `/usr/local/bin/`.
   - **Mengapa pakai `python3 -m venv`?** Ubuntu 24.04 menerapkan aturan **PEP 668** yang melarang `pip install` langsung ke Python sistem. Virtual environment di `/opt/` menjaga sistem aman sekaligus bisa dipakai lintas user tanpa membawa API key pribadi pembuat ISO.
   - Variabel global ditambahkan ke `/etc/environment`: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` dan `AETHER_WHISPER_MODEL_DIR=/opt/aether-models/whisper`.
3. **Menangani Kendala Jaringan Saat Instalasi AI (`install-aether-ai.sh` -> `resume-aether-ai.sh`):**
   - Saat instalasi di Cubic tanggal 14 November, koneksi sempat terputus di tahap `[4/8]` (`npm` kena `ECONNRESET`, `ERR_SOCKET_TIMEOUT`, lalu `npm ERR! code ENOTEMPTY` akibat folder sisa `.opencode-ai-*`).
   - Solusi yang diterapkan: binary `agy` (`237 MB`) disalin lokal (`private-assets/bin/agy`), `codex` dikemas lokal (`codex-pkg.tar.gz`) atau via `npm install -g`, folder sisa `.opencode-ai-*` dibersihkan dulu, dan ditambahkan `NODE_OPTIONS="--dns-result-order=ipv4first"` + `--fetch-retries=5 --fetch-timeout=300000`.
4. **Menjadikan Taskbar Launcher Siap Klik (5 Ikon Utama):**
   - Ikon bawaan di `/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc` disetel ke: `Antigravity` -> `Codex` -> `Hermes` -> `Dolphin` -> `Firefox` (`applications:aether-antigravity.desktop,applications:aether-codex.desktop,applications:aether-hermes.desktop,applications:org.kde.dolphin.desktop,applications:firefox_firefox.desktop`), dengan ikon di `/usr/local/share/icons/aether-ai/` dan launcher `.desktop` (`Exec=konsole -e /usr/local/bin/...`) di `/usr/local/share/applications/`.

### 4.2 Katalog Lengkap Fungsi Setiap Package, Tool, Model & Harness

#### A. Agentic AI Harness (Otak Agen & Coding CLI)
| Nama | Lokasi di ISO | Fungsi Lengkap |
|---|---|---|
| **Antigravity CLI (`agy`)** | `/usr/local/bin/agy` (`237 MB`) | Agentic AI CLI & orchestrator untuk menganalisis kode, merencanakan tugas, mengeksekusi perintah, mengelola subagent/workflow, dan melihat layar. |
| **OpenAI Codex CLI (`codex`)** | `/usr/local/bin/codex` (`@openai/codex` di `/usr/local/lib/node_modules`) | Coding & system AI agent berbasis terminal untuk memodifikasi proyek, debugging, serta automasi repo. |
| **Hermes Agent (`hermes`)** | `/opt/hermes-agent` + `/opt/hermes-venv` -> symlink `/usr/local/bin/hermes` (`hermes-acp`) | Kerangka kerja AI agent interaktif yang terhubung ke modul suara, skill lokal, dan tool kontrol sistem (memiliki kemampuan *Text-to-Speech* seperti Microsoft Edge Neural `en-US-AriaNeural` / `id-ID-ArdiNeural` / `id-ID-GadisNeural` (stream cloud 0 MB di ISO) maupun TTS lokal). |
| **OpenCode (`opencode`)** | `/usr/local/bin/opencode` (`opencode-ai` via npm) | Coding agent CLI alternatif open-source di terminal. |

#### B. Sistem Suara Offline & Otomasi Browser
| Nama | Lokasi di ISO | Fungsi Lengkap |
|---|---|---|
| **Faster-Whisper Model `small`** | `/opt/aether-venv` + model `int8` (~461 MB blob) di `/opt/aether-models/whisper` | **"Telinga AI" (*Speech-to-Text* offline):** Mengonversi rekaman suara mikrofon (16 kHz) menjadi teks secara lokal tanpa membutuhkan internet (model `small` dipilih sebagai titik seimbang akurasi Bahasa Indonesia/Inggris vs ukuran ISO). |
| **`aether-voice`** | `/usr/local/bin/aether-voice` (memakai `sounddevice`, `numpy`, `faster-whisper`) | Jembatan CLI rekam mikrofon (`-s` detik, `-l` kode bahasa, `--transcribe-only`), transkripsi lokal via Faster-Whisper (`local_files_only=True`), lalu langsung mengirim teks perintah ke `hermes chat -q "<teks>"`. |
| **Playwright + Chromium** | `/opt/aether-venv/bin/playwright` (-> `/usr/local/bin/playwright`) + `/opt/pw-browsers` (`chromium-1255` `414M`, `chromium_headless_shell-1255` `282M`, `ffmpeg-1013` `5.1M`) | **Otomasi Web:** Mengendalikan browser Chromium secara terprogram (headless/GUI) untuk tugas riset web, pengisian form, & scraping oleh agen AI — terpisah dari **Firefox** yang tetap dipertahankan untuk user manusia. |

#### C. Tool Kontrol Desktop X11, Audio, & Utilitas Agen (APT)
| Paket / Tool | Fungsi Lengkap |
|---|---|
| **`xdotool`** | Mensimulasikan klik mouse, gerakan kursor, penekanan tombol keyboard, pencarian & fokus jendela di sesi **X11**. |
| **`wmctrl`** | Melihat daftar seluruh jendela aktif (`wmctrl -l`), mengaktifkan (`-a` / `-i -a`), memindah, atau mengatur ukuran jendela di Linux. *(Alasan sesi dikunci ke Plasma X11: `xdotool` & `wmctrl` tidak berjalan di native Wayland).* |
| **`scrot`** | Mengambil screenshot layar dari terminal untuk *vision debugging* agen AI (bersama `spectacle` / `import`). |
| **`xclip`** | Membaca dan menulis teks ke *clipboard* X11 agar agen bisa menukar teks/prompt dengan GUI. |
| **`qdbus-qt5`** | **Jembatan D-Bus KDE Plasma:** Mengontrol layanan KDE lewat CLI/skrip (seperti reload Plasma/KWin compositor, cek status efek blur, atau memicu aksi desktop). |
| **`ffmpeg` & `portaudio19-dev`** | Pemrosesan format audio & driver input mikrofon real-time (dibutuhkan oleh `sounddevice` + `faster-whisper` pada `aether-voice`). |
| **`nodejs` & `npm`** | Runtime JavaScript & manajer paket untuk menjalankan `@openai/codex` dan `opencode-ai`. |
| **`python3`, `python3-venv`, `python3-pip`, `python3-pyqt5`** | Bahasa pemrograman utama harness AI, manajemen lingkungan virtual terisolasi, serta GUI Qt untuk *Aether Panel Studio* & *Aether Installer Prompt*. |
| **`git`** (`2.43.0`) | Kontrol versi & kloning repo kode (baik oleh user maupun AI agent seperti clone `hermes-agent` dan repo `Aether-OS`). |
| **`curl`, `jq`, `ripgrep`, `tmux`, `libnotify-bin`** | `curl` (transfer HTTP/API/ntfy.sh), `jq` (parsing JSON CLI), `ripgrep` (pencarian kode sangat cepat untuk AI agent), `tmux` (sesi terminal persisten/multi-pane), `libnotify-bin` (`notify-send` notifikasi desktop saat tugas AI selesai). |
| **`qt5-style-kvantum`, `fonts-ibm-plex`** | Engine rendering kaca Kvantum untuk Qt/Dolphin & paket font monospace/sans IBM Plex. |

---

## BAB 5 — Perampingan Paket & Alur Remastering Modular (`Sesi 00` – `11`)

### 5.1 Daftar Paket yang Dihapus (Minimal 5 Paket) vs yang Dipertahankan
- **6 Paket Utama yang Dihapus (`apt-get purge -y` + `apt-get autoremove -y`):**
  1. `kmines` (Game Minesweeper KDE)
  2. `kpat` (Game Kartu KPatience KDE)
  3. `ksudoku` (Game Sudoku KDE)
  4. `kmahjongg` (Game Mahjongg KDE) *(+ 7 paket dependensi: `libkf5kdegames-data`, `libfreecell-solver0`, `libkf5kdegames7`, `libqt5opengl5t64`, `kdegames-mahjongg-data-kf5`, `kdegames-card-data-kf5`, `libkf5kmahjongglib5`)*
  5. `kubuntu-wallpapers` (~188 MB — diganti wallpaper 4K Aether OS)
  6. `plasma-workspace-wallpapers` (~93 MB — menghemat ukuran ISO)
- **Yang Sengaja Dipertahankan:** **Firefox** (browser utama desktop), **LibreOffice** termasuk **LibreOffice Calc** (kebutuhan aplikasi perkantoran offline), `linux-firmware-*` / `mesa-*` / `breeze` (driver & fondasi KDE), dan `calamares-settings-kubuntu` (installer OS).

### 5.2 Urutan Lengkap 12 Sesi Modular di Repositori `Galszes/Aether-OS`

| Sesi | Folder / Skrip | Ringkasan Aksi di Terminal Cubic (`R=/tmp/aether-kubuntu-remaster`) |
|---|---|---|
| **00** | `modules/00-persiapan` | `apt-get update`, `purge` 6 paket + `autoremove`, install `python3-pyqt5 qt5-style-kvantum fonts-ibm-plex`, backup `/etc/skel`, salin & `chmod 755` hook `relocate.py`. |
| **01** | `modules/01-font` | Salin font ke `/usr/local/share/fonts/`, `fc-cache -f`, salin `fonts.conf`/`kcmfonts`, gabung fragmen font ke `/etc/skel/.config/kdeglobals` via `tools/merge-kconfig.py`. |
| **02** | `modules/02-ikon` | Salin `Vivid-Glassy-Dark-Icons` ke `/usr/share/icons/`, gabung `[Icons] Theme` ke `kdeglobals`. |
| **03** | `modules/03-appearance-glass` | Pasang `Aeos`, `Aeos-Blur`, `AetherGlass`, gabung `kdeglobals.ini`, `kwinrc.ini`, `plasmarc.ini`, plus opsi `aether-compat-blur` untuk KWin `5.27.11`. |
| **04** | `modules/04-panel-terpisah` | Salin plasmoid `org.aether.panelislands` & gabung `plasma-layout.ini` (`splitPanel=1`, jam Urbanist, baterai, spacer) ke `plasma-org.kde.plasma.desktop-appletsrc`. |
| **05** | `modules/05-panel-studio` | Pasang `AetherPanelStudio` dan `.desktop` launcher-nya. |
| **06** | `modules/06-wallpaper-branding` | Pasang wallpaper 4K, tema SDDM `aether-sddm` + `zz-aether-branding.conf`, aset Lock/Home, `kcm-about-distrorc`, dan config wallpaper desktop. |
| **07** | `modules/07-splash` | Pasang `org.aether.splashstudio` dan `/etc/skel/.config/ksplashrc`. |
| **08** | `modules/08-konsole` | Salin profil kaca `Aether Glass.profile`, `AetherGlass.colorscheme`, `AetherGlass.css`, dan `konsolerc`. |
| **09** | `modules/09-ai-harness` | Jalankan `bash "$R/scripts/install-aether-ai.sh"` -> memasang `agy`, `codex`, `opencode`, `hermes`, `aether-voice` + Whisper `small`, Playwright Chromium, dan paket APT kontrol X11. |
| **10** | `modules/10-branding-dan-fix` | Jalankan berurutan di `$R/scripts`:<br>1. `bash apply-hotfix.sh` (Plymouth `aether-logo` + `update-initramfs -u`)<br>2. `bash apply-blur-fix.sh` (`aether-compat-blur-v6.so` + `GLX`)<br>3. `bash apply-desktop-sync.sh` (5 taskbar launcher AI/Dolphin/Firefox + widget desktop)<br>4. `bash apply-installer-brand.sh` (Calamares + PyQt5 `kubuntu-installer-prompt`)<br>5. `bash apply-panel-studio-fix.sh` (pindah ke `/opt/AetherPanelStudio` + `chmod 755` `.desktop`)<br>6. `bash polish-aether.sh` (`chown -R root:root /etc/skel`, `qdbus-qt5`, `aether-voice`, update `initrd.img`) |
| **11** | `modules/11-build-iso` | Keluar chroot (`Next>`), pastikan identitas OS Release Cubic (`Release: Genesis`, `etc/lsb-release` & `usr/lib/os-release` -> `aetheros 24.04.5 24.04 LTS amd64`, `.disk/info` -> `aetheros 24.04.5 24.04 LTS amd64 "Genesis"`), atur `boot/grub/grub.cfg` pada tab **Boot** sesuai `payloads/grub.cfg` (*Try or Install Aether OS*), pilih kompresi (`zstd` / `gzip` / `xz`), lalu **Generate** ISO (`filesystem.squashfs` ~`6,20 GB`, `initrd.gz` ~`89,6 MB`, `vmlinuz` ~`17,0 MB`). |

**Kemandirian Repo GitHub (`Galszes/Aether-OS`) vs Release Archive:**
Kode publik (`modules/`, `scripts/`, `payloads/*.tar.gz`, `payloads/grub.cfg`, `tools/`, `docs/`) disimpan di GitHub dengan semua skrip memakai path relatif (`$PAYLOAD_DIR/`, tanpa ketergantungan server `127.0.0.1:8765`). Sementara folder `private-assets/` (~377 MB mentah, termasuk binary `agy` `237 MB` yang melampaui limit 100 MB per file di GitHub serta ribuan symlink ikon Linux) di-ignore di `.gitignore` dan dibundel utuh di arsip rilis **`aether-kubuntu-remaster-final.tar.gz`**.

---

## BAB 6 — Log *Troubleshooting* & *Debugging* Nyata (Dari Awal hingga Build v5)

Setiap masalah nyata di bawah ini langsung dihadapi saat membangun dan menguji ISO di VirtualBox:

1. **Error Cubic `No valid disk boot kernels were found` (14 Nov):**
   - *Penyebab:* `update-initramfs -c` menghasilkan `initrd.img-7.0.0-31-generic` (86 MB) di `custom-root/boot/`, tetapi file fisik `vmlinuz-7.0.0-31-generic` (17 MB) tidak ada di sana (cuma symlink putus; kernel aslinya di `custom-disk/casper/vmlinuz`).
   - *Solusi:* Menyalin `vmlinuz-7.0.0-31-generic` ke `/boot/` di chroot Cubic sehingga halaman Kernel langsung mengenali kernel & initrd.
2. **Error Transfer ISO Besar ke VirtualBox Shared Folder (`vboxsf`) (14–15 Nov):**
   - *Penyebab:* Dolphin gagal menyalin berkas >5 GB (*"Could not write to file"*) karena aturan permission `vboxsf` dan batas stabilitas transfer berkas tunggal >500 MB.
   - *Solusi:* Memecah ISO (`6.4–7.9 GB`) per `350 MB` (`split -b 350M -d -a 3`) beserta skrip penggabung `GABUNG_DI_WINDOWS.bat` (`copy /b *.part*`), dan menyusun arsip `tar.gz` di partisi `ext4` terlebih dahulu agar ribuan symlink Linux tidak gagal dibuat di `vboxsf`.
3. **Efek Blur Hilang saat VirtualBox *3D Acceleration* Dinyalakan (15 Nov, ISO v2->v3):**
   - *Penyebab:* Saat 3D off memakai `llvmpipe`, tetapi saat 3D on dengan `VMSVGA`, plugin `aether-compat-blur-v6.so`, `aether-qt-style.sh`, dan setting `GLPlatformInterface=glx` pada `kwinrc` belum masuk ke `/etc/skel/`.
   - *Solusi:* Dipaketkan ke `aether-blur-fix.tar.gz` & `apply-blur-fix.sh` untuk dimasukkan ke `/etc/skel/`.
4. **Tombol *"Install Kubuntu"* Justru Masuk ke Mode *"Try"* + Branding Kubuntu (15 Nov, ISO v4->v5):**
   - *Penyebab:* Penghapusan `show.qml` bersama 12 slide membuat Calamares crash dan keluar ke sesi Live, sementara `/usr/bin/kubuntu-installer-prompt` asli masih memakai teks/logo Kubuntu.
   - *Solusi:* Menyertakan `show.qml` kosong valid (`91 bytes`), prompt PyQt5 `aether-installer-prompt.py` (*Try or Install Aether OS*, memanggil `sudo -E calamares -D8`), dan mengubah `grub.cfg` + `loopback.cfg`.
5. **Widget *Aether Panel Studio* Error `"Not Authorized to Execute"` di Live ISO v5 (15 Nov):**
   - *Penyebab:* File `.desktop` di `/etc/skel/.local/share/plasma_icons/` masih berizin `0664` (tanpa `+x`) dan `Exec=` + wrapper-nya masih hardcode path `/home/aether/...` (yang tidak ada pada user Live `kubuntu`).
   - *Solusi (`apply-panel-studio-fix.sh` & update Cubic 15–16 Nov):* Memindahkan `AetherPanelStudio` ke `/opt/AetherPanelStudio/`, membuat wrapper global `/usr/local/bin/aether-panel-studio`, mengubah `Exec=`, serta menyetel `chmod 755` & `chown root:root` seluruh `.desktop` (termasuk `aether-antigravity.desktop`, `aether-codex.desktop`, `aether-hermes.desktop`, dan `aether-panel-studio-widget.desktop` di `/usr/local/share/applications/` yang telah terverifikasi `-rwxr-xr-x 1 root root`).
6. **Disk Cubic (`/dev/sdb1`) Hilang / Cubic Layar Merah Setelah Reboot:**
   - *Penyebab:* `/dev/sdb1` tidak terdaftar di `/etc/fstab` sehingga harus di-mount ulang setelah VM menyala (`udisksctl mount -b /dev/sdb1`).
7. **Status Terbuka (*Engineering Transparency*):**
   - Pada uji ISO v5 (`15 Nov`, sebelum `chmod 755` pada `aether-hermes.desktop` tanggal 16 Nov), launcher taskbar **Hermes** sempat membuka Konsole sesaat lalu menutup cepat dengan pesan file tidak ditemukan; diagnosa/perbaikan lanjutan runtime Hermes belum dilanjutkan pada saat itu karena user memilih melewati pemeriksaan Hermes dan mengekspor konfigurasi, sementara `Antigravity` dan `Codex` di taskbar berjalan normal. Jika dijalankan ulang di build baru, disarankan mengecek `/usr/local/bin/hermes` di Konsole atau menambahkan `--hold` sementara pada `aether-hermes.desktop`.
   - Efek kompatibilitas `aether-compat-blur-v6.so` menargetkan ABI KWin X11 `5.27.11` dan memerlukan uji ulang jika berpindah ke Plasma 6 atau Wayland.

---

## BAB 7 — Ringkasan Perintah Wajib & Tanya-Jawab Presentasi

### 7.1 Perintah Kunci yang Sering Ditanyakan
- **Mount disk proyek Cubic tanpa `sudo`:** `udisksctl mount -b /dev/sdb1`
- **Hapus 6 bloatware + bersihkan ISO:** `apt-get purge -y kmines kpat ksudoku kmahjongg kubuntu-wallpapers plasma-workspace-wallpapers && apt-get autoremove -y && apt-get clean`
- **Salin isi modul ke `/etc/skel/` (dengan file tersembunyi):** `cp -a "$R/modules/01-font/skel/." /etc/skel/`
- **Gabung fragmen INI tanpa menimpa pengaturan lain:** `python3 "$R/tools/merge-kconfig.py" <fragmen.ini> /etc/skel/.config/<target>`
- **Aktifkan tema Plymouth & tanam ke `initramfs`:** `update-alternatives --set default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth && update-initramfs -u`
- **Perbaiki izin eksekusi widget/launcher KDE:** `chmod 755 <file.desktop> && chown root:root <file.desktop>`
- **Jalankan Studio / Dolphin kaca:** `aether-panel-studio` · `dolphin --new-window --style kvantum`
- **Cek sintaks & arsip sebelum build:** `bash -n scripts/*.sh` · `tar -tzf payloads/*.tar.gz`

### 7.2 Poin Kunci Menjawab 3 Pertanyaan Utama Secara Ringkas
1. **Wallpaper, Logo Boot, Semua Logo, & Splash:** Wallpaper ditaruh di `/etc/skel/Downloads/` + `plasma-org.kde.plasma.desktop-appletsrc` (bersama `kactivitymanagerdrc` & `relocate.py`). Logo boot diubah lewat **Plymouth** (`aether-logo`) dan ditanam ke `initrd.img` via `update-initramfs -u`. Logo desktop dipisah per perannya (**Home/Info Center** -> `homeLogo.png` + `kcm-about-distrorc`; **Lock Screen** -> `org.aether.lockstudio`; **Logout** -> `Aeos/contents/logout/`; **Login** -> SDDM `/usr/share/sddm/themes/aether-sddm/` + `zz-aether-branding.conf`) dengan menghapus lingkaran avatar via `UserDelegate.qml`. Splash pasca-login memakai **KSplash** (`org.aether.splashstudio` + overlay hitam 60% + Urbanist).
2. **Logo Installer & Tampilan *Try or Install*:** Menu boot hitam diubah di luar chroot pada `custom-disk/boot/grub/grub.cfg` & `loopback.cfg`. Pop-up *"Try or Install Kubuntu"* diganti di `/usr/bin/kubuntu-installer-prompt` memakai dialog PyQt5 custom `aether-installer-prompt.py` yang memanggil `sudo -E calamares -D8`. Logo, sidebar, dan slide Calamares diubah di `/etc/calamares/branding/kubuntu/` (`branding.desc`, menghapus 12 slide Kubuntu sambil menjaga `show.qml` minimal valid, serta mengubah `kubuntu-calamares.desktop`).
3. **Package, Tool, & Harness:** Dipasang langsung di dalam chroot Cubic secara *system-wide* (`/opt/` & `/usr/local/bin/`, bukan di `/home/`) lewat `install-aether-ai.sh` memakai APT, `npm install -g`, dan `python3 -m venv` (aturan PEP 668): `agy`, `codex`, `hermes`, & `opencode` sebagai AI coding/OS agent; `faster-whisper` (`small` di `/opt/aether-models/whisper`) + `aether-voice` sebagai *speech-to-text offline*; `playwright` + Chromium (`/opt/pw-browsers`) untuk otomasi web; serta `xdotool`, `wmctrl`, `scrot`, `xclip`, `qdbus-qt5`, `ffmpeg`, `tmux`, `ripgrep`, `jq`, `git` untuk memberi "mata, tangan, & komunikasi sistem" ke agen AI di sesi X11.
