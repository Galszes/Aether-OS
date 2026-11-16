# 02 — Tema ikon

Pasang tema ikon global dan pilih namanya untuk akun baru.

Prasyarat: 00-persiapan. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/02-ikon-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /usr/share/icons
cp -a "$R/private-assets/icons/Vivid-Glassy-Dark-Icons" /usr/share/icons/
python3 "$R/tools/merge-kconfig.py" "$R/modules/02-ikon/config/kdeglobals.ini" /etc/skel/.config/kdeglobals
```

## File dan kode yang terkait

Target `/usr/share/icons/Vivid-Glassy-Dark-Icons/index.theme` menentukan nama dan pewarisan ikon. Key `[Icons] Theme` pada kdeglobals memilih tema. Logo Home adalah gambar branding terpisah (sesi 06); memilih tema ikon tidak mengganti semua logo branding.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
