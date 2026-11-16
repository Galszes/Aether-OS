# 01 — Font

Pasang file font, lalu terapkan pilihan global tanpa mengganti warna/ikon desktop.

Prasyarat: 00-persiapan. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/01-font-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /usr/local/share/fonts
cp -a "$R/private-assets/fonts/." /usr/local/share/fonts/
fc-cache -f /usr/local/share/fonts
cp -a "$R/modules/01-font/skel/." /etc/skel/
python3 "$R/tools/merge-kconfig.py" "$R/modules/01-font/config/kdeglobals.ini" /etc/skel/.config/kdeglobals
```

## File dan kode yang terkait

`config/kdeglobals.ini` hanya memuat key font (Google Sans global, IBM Plex Sans taskbar dan font WM). `skel/.config/fontconfig/fonts.conf` mengatur fontconfig. Urbanist jam 12 pt berada di sesi panel; Urbanist splash berada di sesi splash; IBM Plex Mono terminal berada di sesi Konsole. Untuk mengubah font setelah instalasi: System Settings → Fonts; jam melalui Configure Digital Clock. Aset font eksternal berada di private-assets dan tidak ikut GitHub secara default.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
