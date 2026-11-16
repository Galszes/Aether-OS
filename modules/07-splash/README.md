# 07 — Splash Screen

Pasang splash setelah login dengan overlay hitam 60%, font Urbanist dan progress biru.

Prasyarat: 00-persiapan, 01-font; 05 untuk editor. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/07-splash-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /etc/skel/.local/share/plasma/look-and-feel
cp -a "$R/private-assets/splash/org.aether.splashstudio" /etc/skel/.local/share/plasma/look-and-feel/
cp -a "$R/modules/07-splash/skel/." /etc/skel/
```

## File dan kode yang terkait

Pemilih tema: .config/ksplashrc. Layout: org.aether.splashstudio/contents/splash/Splash.qml. Gambar: contents/splash/images/background.jpeg dan logo.svg. State editor: .config/aether-splash-studio.json. splash.py membangun ulang Splash.qml dari pilihan Studio; edit permanen lewat editor/generator agar tidak tertimpa saat Terapkan berikutnya. Pratinjau nyata memakai ksplashqml --test --window. Preview tidak mengubah sesi login.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
