# 09 — Bangun dan uji ISO

Lanjutkan halaman Cubic setelah modul yang dipilih selesai. Aset yang dipilih dan dependensi harus tersedia; jangan menganggap clone GitHub membawa private-assets.

Prasyarat: Sesi 00–08 sesuai fitur yang dipilih. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/09-build-iso-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
grep '^splitPanel=' /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
cat /etc/skel/.config/ksplashrc
cat /etc/sddm.conf.d/zz-aether-branding.conf
```

## File dan kode yang terkait

Buat ISO, boot di VM, lalu instal ke disk VM kosong dengan username berbeda. Cek panel membesar/mengecil ketika aplikasi dibuka, celah bening, baterai dekat jam, font, ikon, Dolphin, lock, logout, login SDDM, splash, dan Studio. Cek ~/.aether-remaster-relocate.log pada akun baru. ISO baru dari struktur modular ini belum diuji boot.

Untuk rollback sesi saat masih di Cubic, kembalikan salinan file modul dari /var/backups/aether-sessions yang sesuai. Mengganti /etc/skel tidak memulihkan font/ikon/SDDM global; simpan proyek Cubic atau salinan target sistem sebelum mengulang perubahan global.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
