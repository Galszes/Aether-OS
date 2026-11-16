# 08 — Konsole

Pasang profil terminal dan skema warna; font monospace berbeda dari font global.

Prasyarat: 00-persiapan, 01-font, 03-appearance-glass. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/08-konsole-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /etc/skel/.local/share
cp -a "$R/modules/08-konsole/skel/." /etc/skel/
```

## File dan kode yang terkait

Aether Glass.profile memilih IBM Plex Mono dan skema AetherGlass.colorscheme. AetherGlass.css mengatur tab Konsole; konsolerc memilih profil default. Setelah boot gunakan Settings → Edit Current Profile → Appearance untuk font dan skema. Transparansi warna/profil dan blur compositor perlu bekerja bersama.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
