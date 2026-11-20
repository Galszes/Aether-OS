# Daftar Perintah Wajib Dipahami Kelompok — Proyek Aether OS

Dokumen ini berisi seluruh perintah (*commands*) penting yang digunakan dari tahap persiapan host, chroot di Terminal Cubic (`Sesi 00`–`11`), instalasi AI Harness, pemecahan masalah KDE Plasma, hingga penggunaan harian di desktop **Aether OS**.

---

## Kelompok 1 — Perintah Persiapan Host & Disk Cubic (Di Luar Chroot)

Perintah-perintah ini dijalankan di komputer/VM host (sebelum atau saat membuka **Cubic**):

| Perintah | Fungsi & Penjelasan untuk Kelompok |
|---|---|
| `lsblk` | Menampilkan daftar seluruh disk dan partisi (*block devices*), seperti `/dev/sda1` (sistem utama) dan `/dev/sdb1` (disk proyek Cubic ~49 GiB), beserta titik *mount*-nya. |
| `udisksctl mount -b /dev/sdb1` | Me-*mount* partisi proyek Cubic tanpa memerlukan `sudo`. Hasilnya otomatis masuk ke `/media/aether/<UUID>/` (misal `/media/aether/7e771b5c-613f-4192-b383-1621c3716665`). *(Untuk melepas: `udisksctl unmount -b /dev/sdb1`.)* |
| `cubic` *(atau `cubic /path/proyek`)* | Membuka aplikasi GUI **Cubic (Custom Ubuntu ISO Creator)**. Saat diberikan argumen folder proyek yang sudah ada, Cubic langsung mengenali konfigurasi `cubic.conf`. |
| `git clone https://github.com/Galszes/Aether-OS.git /tmp/aether-kubuntu-remaster` | Mengunduh (*clone*) repositori kode & skrip Aether OS dari GitHub ke `/tmp/aether-kubuntu-remaster` di dalam lingkungan Cubic. |
| `tar -xzf aether-kubuntu-remaster-final.tar.gz -C /tmp` | Mengekstrak arsip rilis lengkap (`.tar.gz`, menjaga *permissions* dan *symlink* Linux tetap utuh) ke direktori `/tmp` (`-x` extract, `-z` gzip, `-f` file, `-C` target folder). Digunakan agar `private-assets/` (font, ikon, tema, wallpaper, `bin/agy`) ikut tersedia. |

---

## Kelompok 2 — Manajemen Paket APT & Penghapusan Bloatware (`Sesi 00` & `09`)

Dijalankan di Terminal Cubic (`root@cubic:~#`):

1. **Memperbarui indeks daftar paket dari repositori Ubuntu:**
   ```bash
   apt-get update
   ```
2. **Menghapus 6 paket bawaan Kubuntu yang tidak diperlukan (*bloatware* game & wallpaper default):**
   ```bash
   apt-get purge -y kmines kpat ksudoku kmahjongg kubuntu-wallpapers plasma-workspace-wallpapers
   ```
   - Menghapus 4 game KDE (`kmines`, `kpat`, `ksudoku`, `kmahjongg`) serta 2 paket wallpaper default (`kubuntu-wallpapers`, `plasma-workspace-wallpapers`) untuk merampingkan ISO dan mengganti visual bawaan Kubuntu.
3. **Menghapus paket dependensi yatim (*orphaned dependencies*):**
   ```bash
   apt-get autoremove -y
   ```
   - Otomatis membuang library pendukung yang tadinya hanya dipakai oleh game di atas (misalnya `libkf5kdegames-data`, `libfreecell-solver0`, `libkf5kdegames7`, `libqt5opengl5t64`).
4. **Memasang dependensi GUI, tema, runtime AI, & tool kontrol X11:**
   ```bash
   apt-get install -y python3-pyqt5 qt5-style-kvantum fonts-ibm-plex
   apt-get install -y xdotool wmctrl curl scrot xclip jq ripgrep tmux libnotify-bin python3-venv python3-pip portaudio19-dev nodejs npm qdbus-qt5
   ```
5. **Membersihkan cache arsip `.deb` hasil unduhan sebelum ISO di-generate:**
   ```bash
   apt-get clean
   ```

> **Perbedaan penting untuk dihafal:**
> - `apt remove`: menghapus binary program, tapi **menyisakan file konfigurasi**.
> - `apt purge`: menghapus program **beserta seluruh file konfigurasinya** sampai bersih.
> - `apt autoremove`: menghapus **dependensi yang sudah tidak terpakai** oleh paket lain.
> - `apt clean`: menghapus **cache `.deb`** di `/var/cache/apt/archives/` agar ukuran ISO akhir tidak membengkak.

---

## Kelompok 3 — Penyalinan File, Template `/etc/skel` & Penggabungan Konfigurasi (`Sesi 00`–`08`)

Konsep inti di balik remastering Kubuntu adalah membedakan sistem global vs **template user baru (`/etc/skel`)**.

1. **Menentukan variabel path kerja & cadangan tiap sesi:**
   ```bash
   R=/tmp/aether-kubuntu-remaster
   mkdir -p /var/backups/aether-sessions
   cp -a /etc/skel /var/backups/aether-sessions/00-original-skel
   ```
   - `R=...` mempermudah penulisan path agar tidak mengetik panjang berulang kali.
   - `mkdir -p` membuat folder bersarang tanpa error jika folder sudah ada.
2. **Menyalin isi modul ke `/etc/skel/` atau `/`:**
   ```bash
   cp -a "$R/modules/00-persiapan/root/." /
   cp -a "$R/modules/01-font/skel/." /etc/skel/
   ```
   - **Arti flag `-a` (*archive*):** menyalin secara rekursif sekaligus **mempertahankan symlink, timestamp, dan hak akses asli**.
   - **Mengapa pakai titik `/.` di belakang (`skel/.`)?** Agar yang disalin adalah **seluruh isi di dalam folder `skel`** (termasuk file/folder tersembunyi berawalan titik seperti `.config` dan `.local`), bukan membuat folder `skel` baru di dalam `/etc/skel/skel`.
   - **Mengapa harus ke `/etc/skel/`?** Saat ISO diboot sebagai *Live* (user `kubuntu`) maupun ketika di-install dengan nama user apa pun, Ubuntu menyalin seluruh isi `/etc/skel/` ke folder `/home/<nama_user>`.
3. **Membangun ulang cache font sistem setelah menyalin font custom:**
   ```bash
   cp -a "$R/private-assets/fonts/." /usr/local/share/fonts/
   fc-cache -f /usr/local/share/fonts
   ```
   - `fc-cache -f` memaksa Fontconfig memindai ulang folder agar **Google Sans**, **Urbanist**, dan **Rounded Elegance** langsung dikenali Plasma.
4. **Menggabungkan fragmen konfigurasi KDE tanpa saling menimpa:**
   ```bash
   python3 "$R/tools/merge-kconfig.py" "$R/modules/01-font/config/kdeglobals.ini" /etc/skel/.config/kdeglobals
   python3 "$R/tools/merge-kconfig.py" "$R/modules/02-ikon/config/kdeglobals.ini" /etc/skel/.config/kdeglobals
   python3 "$R/tools/merge-kconfig.py" "$R/modules/03-appearance-glass/config/kwinrc.ini" /etc/skel/.config/kwinrc
   ```
   - **Mengapa memakai `merge-kconfig.py` dan bukan `cp` langsung?** File `kdeglobals` berisi banyak bagian (font, ikon, warna, tema). Jika Sesi 02 menyalin file `kdeglobals` utuh, pengaturan font dari Sesi 01 akan hilang tertimpa. `merge-kconfig.py` hanya menyisipkan/memperbarui key dari fragmen INI sesi terkait.

---

## Kelompok 4 — Hak Akses (`chmod`) & Kepemilikan (`chown`) di KDE Plasma

Banyak bug pada remastering Linux muncul hanya karena **izin eksekusi** dan **kepemilikan file**:

1. **Memberi izin *executable* (`chmod 755` / `chmod +x`):**
   ```bash
   chmod 755 /etc/skel/.config/plasma-workspace/env/00-aether-remaster-relocate.sh
   chmod 755 /etc/skel/.config/plasma-workspace/env/aether-qt-style.sh
   chmod 755 /etc/skel/.local/share/plasma_icons/aether-panel-studio*.desktop
   chmod 755 /usr/local/share/applications/aether-*.desktop
   chmod +x /usr/local/bin/aether-panel-studio /usr/bin/kubuntu-installer-prompt
   ```
   - **`755` (`rwxr-xr-x`):** pemilik (`root`) bisa baca/tulis/eksekusi; grup dan semua user lain bisa baca dan **eksekusi**.
   - **Mengapa wajib untuk `.desktop` widget?** KDE Plasma memblokir eksekusi file `.desktop` di desktop/widget (`org.kde.plasma.icon`) yang tidak memiliki bit `+x` dengan pesan error ***"not authorized to execute"***.
   - **Mengapa wajib untuk skrip di `plasma-workspace/env/`?** Skrip environment pra-Plasma (`00-aether-remaster-relocate.sh` yang menjalankan `relocate.py` serta `aether-qt-style.sh` untuk `QT_PLUGIN_PATH`) hanya dieksekusi saat login jika berstatus executable.
2. **Menyetel kepemilikan menjadi `root:root` (`chown`):**
   ```bash
   chown -R root:root /etc/skel
   chown root:root /usr/local/share/applications/aether-*.desktop
   ```
   - File di `/etc/skel` dan `/usr/local/share/applications/` tidak boleh dimiliki UID personal (`1000` / `aether`). `chown -R root:root` memastikan kepemilikan bersih secara sistem, yang nantinya disalin Calamares/Casper ke UID user baru yang sesuai.

---

## Kelompok 5 — Instalasi Ekosistem *Agentic AI Harness* (`Sesi 09` — `install-aether-ai.sh`)

Seluruh AI agent diletakkan di `/opt/` dan `/usr/local/` (bukan di `/home/aether/`) agar tersedia untuk **semua user**:

1. **Memasang CLI AI berbasis Node.js secara global:**
   ```bash
   npm install -g @openai/codex opencode-ai
   ```
   - Flag `-g` (*global*) memasang paket ke `/usr/local/lib/node_modules/` dan menautkan executable ke `/usr/local/bin/codex` serta `/usr/local/bin/opencode`.
2. **Membuat Python Virtual Environment terisolasi di `/opt/`:**
   ```bash
   python3 -m venv /opt/aether-venv
   /opt/aether-venv/bin/pip install faster-whisper sounddevice numpy playwright
   ```
   - Ubuntu 24.04 menerapkan proteksi PEP 668 (*externally-managed-environment*) pada Python sistem, sehingga paket Python wajib dipasang ke virtual environment (`venv`) terpisah seperti `/opt/aether-venv` dan `/opt/hermes-venv`.
3. **Memasang Hermes Agent dalam mode *editable*:**
   ```bash
   git clone --depth 1 https://github.com/NousResearch/hermes-agent.git /opt/hermes-agent
   python3 -m venv /opt/hermes-venv
   /opt/hermes-venv/bin/pip install -e /opt/hermes-agent
   ```
   - `--depth 1` melakukan *shallow clone* (hanya commit terbaru) untuk menghemat waktu & ruang ISO.
   - `pip install -e` menginstal paket merujuk langsung ke folder `/opt/hermes-agent`.
4. **Memasang Browser Automation & Model Voice Offline:**
   ```bash
   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers /opt/aether-venv/bin/playwright install chromium
   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers /opt/aether-venv/bin/playwright install-deps chromium
   /opt/aether-venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', download_root='/opt/aether-models/whisper')"
   ```
   - Mengarahkan unduhan Chromium (`PLAYWRIGHT_BROWSERS_PATH`) dan model **`faster-whisper` `small`** (`AETHER_WHISPER_MODEL_DIR`) ke folder `/opt/` (bukan `~/.cache/`) agar dapat dipakai **offline** oleh user Live `kubuntu` maupun user hasil instalasi (ditulis ke `/etc/environment`).
5. **Membuat *symbolic link* (*shortcut* command) ke `/usr/local/bin/`:**
   ```bash
   ln -sf /opt/hermes-venv/bin/hermes /usr/local/bin/hermes
   ln -sf /opt/aether-venv/bin/playwright /usr/local/bin/playwright
   ```
   - `ln -sf` (`-s` symbolic, `-f` force/timpa jika ada) membuat perintah `hermes` dan `playwright` dapat dipanggil langsung dari terminal mana pun karena `/usr/local/bin` masuk ke `$PATH` sistem.

---

## Kelompok 6 — Boot Splash Plymouth, Kernel Initramfs & Branding Installer (`Sesi 10`)

1. **Mengekstrak paket payload langsung ke root filesystem `/`:**
   ```bash
   tar -xzvf "$PAYLOAD_DIR/aether-installer-brand.tar.gz" -C /
   tar -xzvf "$PAYLOAD_DIR/aether-hotfix.tar.gz" -C /
   ```
   - Berbeda dengan `aether-blur-fix.tar.gz` yang diekstrak ke `-C /etc/skel`, arsip di atas memuat path lengkap sistem (`etc/calamares/...`, `usr/bin/kubuntu-installer-prompt`, `usr/share/plymouth/...`) sehingga target ekstraknya adalah `-C /`.
2. **Mendaftarkan & mengaktifkan tema boot splash Plymouth `aether-logo`:**
   ```bash
   update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth 200
   update-alternatives --set default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth
   ```
   - `update-alternatives` mengatur tema Plymouth aktif dengan prioritas tinggi (`200`).
3. **Memperbarui *Initial RAM Filesystem* (`initramfs`):**
   ```bash
   update-initramfs -u
   ```
   *(Atau `update-initramfs -u -k "$KVER"` / `-c -k "$KVER"` di `polish-aether.sh`.)*
   - **Sangat krusial:** Plymouth tampil **sebelum** root disk penuh di-mount saat booting. Jika `update-initramfs -u` tidak dijalankan, logo Plymouth `aether-logo` tidak masuk ke dalam `initrd.img-7.0.0-31-generic`, sehingga saat boot tetap muncul logo Kubuntu lama.
4. **Mengubah isi file konfigurasi/desktop secara otomatis dengan `sed -i`:**
   ```bash
   sed -i 's/Install Kubuntu/Install Aether OS/g' /usr/share/applications/kubuntu-calamares.desktop
   sed -i 's|^Exec=.*|Exec=/usr/local/bin/aether-panel-studio|' "$f"
   ```
   - `sed -i` (*stream editor in-place*) mengganti teks sesuai pola regex langsung di dalam file.
5. **Cara kerja *Live Prompt* (`kubuntu-installer-prompt`):**
   - Dialog PyQt5 custom pengganti wrapper asli, di mana tombol **Install Aether OS** menjalankan `sudo -E calamares -D8` (`-E` mempertahankan environment tampilan GUI X11/`DISPLAY` ke proses `calamares` yang berjalan sebagai `root`, `-D8` mengaktifkan logging debug installer).

---

## Kelompok 7 — Perintah Penggunaan, Verifikasi & Demo Harian di Aether OS

Perintah-perintah ini berguna saat mendemokan sistem di depan kelas/dosen atau memeriksa komponen:

| Perintah | Kegunaan saat Demo / Uji Sistem |
|---|---|
| `aether-panel-studio` *(atau `--branding`)* | Membuka aplikasi **Aether Panel Studio** (atau langsung ke tab *Layar kunci & Logo*). |
| `dolphin --new-window --style kvantum` | Membuka file manager Dolphin paksa memakai tema kaca Kvantum agar efek *frosted glass* langsung terlihat. |
| `agy` · `codex` · `hermes` · `opencode` | Menjalankan masing-masing **AI Coding / Agent CLI** langsung dari Konsole. |
| `aether-voice` | Menjalankan utilitas pengenalan suara offline berbasis model `faster-whisper small`. |
| `readlink -f /etc/alternatives/default.plymouth` | Memastikan tema Plymouth aktif benar-benar menunjuk ke `aether-logo.plymouth`. |
| `lsb_release -a` · `cat /etc/os-release` | Menampilkan identitas distribusi dan versi Ubuntu/Aether OS aktif. |
| `wmctrl -l` · `xdotool ...` | Melihat daftar seluruh jendela aktif di desktop X11 dan mensimulasikan kontrol klik/ketik oleh AI. |
| `spectacle -a -b -n -o file.png` | Mengambil tangkapan layar jendela aktif (`-a`) di latar belakang (`-b`) tanpa notifikasi (`-n`) langsung ke file (`-o`). |
| `bash -n script.sh` · `tar -tzf arsip.tar.gz` | Memvalidasi sintaks skrip bash tanpa mengeksekusinya dan mengecek keutuhan isi arsip `.tar.gz`. |

---

## Kelompok 8 — Pertanyaan Umum Saat Presentasi / Sidang & Jawaban Singkatnya

1. **"Mengapa perubahan tema ditaruh di `/etc/skel/`, bukan langsung di `/home/aether/`?"**
   -> Karena saat ISO dijalankan dalam mode Live (user `kubuntu`) atau di-install oleh orang lain dengan nama akun baru, `/home/aether/` tidak dipakai/tidak ada. Ubuntu otomatis menyalin seluruh isi `/etc/skel/` ke folder home user baru saat akun dibuat.
2. **"Kenapa pakai `merge-kconfig.py` padahal bisa `cp` file `kdeglobals` saja?"**
   -> Karena `kdeglobals` menyimpan banyak jenis pengaturan sekaligus (font, ikon, palet warna). Jika tiap modul menimpa file utuh dengan `cp`, pengaturan modul sebelumnya akan hilang. `merge-kconfig.py` hanya menggabungkan key tertentu dari potongan INI.
3. **"Apa bedanya `apt purge` dengan `apt remove`, dan kenapa perlu `autoremove` + `clean`?"**
   -> `remove` menyisakan file konfigurasi, sedangkan `purge` menghapus tuntas hingga konfigurasinya. `autoremove` membuang library dependensi bekas program yang dihapus, dan `clean` menghapus file cache `.deb` agar ukuran ISO lebih hemat.
4. **"Kenapa ikon/widget Aether Panel Studio sempat error *not authorized to execute* di Live ISO?"**
   -> Dua hal: file `.desktop` widget KDE di `plasma_icons/` wajib memiliki bit izin eksekusi (`chmod 755`), dan path `Exec=` sebelumnya masih hardcode ke `/home/aether/.local/bin/...` sehingga tidak ditemukan pada akun `kubuntu`. Solusinya dipindah ke `/opt/AetherPanelStudio` + `/usr/local/bin/aether-panel-studio` dan diberi `chmod 755`.
5. **"Kenapa `update-initramfs -u` wajib dijalankan setelah mengatur Plymouth?"**
   -> Karena animasi splash Plymouth muncul pada fase awal boot sebelum partisi root sistem termuat penuh; temanya harus dibungkus ke dalam berkas `initrd.img` di `/boot/`.
6. **"Kenapa `aether-venv` dan `hermes-venv` dibuat di `/opt/` pakai `python3 -m venv`?"**
   -> Agar paket Python AI (`faster-whisper`, `playwright`, `hermes-agent`) tidak bentrok dengan paket Python sistem Ubuntu 24.04 (aturan PEP 668) sekaligus bisa diakses oleh semua akun pengguna, tidak terikat ke satu folder home.
