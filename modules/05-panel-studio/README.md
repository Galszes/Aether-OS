# 05 — Aether Panel Studio

Pasang aplikasi Python/PyQt5 dan launcher. Kode dapat ditinjau terpisah dari aset tema.

Prasyarat: 00-persiapan, 03-appearance-glass, 04-panel-terpisah. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/05-panel-studio-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
cp -a "$R/modules/05-panel-studio/skel/." /etc/skel/
chmod 755 /etc/skel/.local/bin/aether-panel-studio
```

## File dan kode yang terkait

`app.py` mendefinisikan tab/kontrol; `backend.py` memetakan key ke konfigurasi widget dan menulis SVG/Kvantum/KWin. `branding.py`, `splash.py`, `titlebar.py` menangani tab khusus. Setelah boot cari Aether Panel Studio di launcher. Tab Panel → Panel terpisah adaptif mengubah splitPanel; tekan Terapkan.

Studio memerlukan tema Aeos dan widget Panel Islands aktif. Tab branding/splash paling lengkap setelah sesi 06/07. App belum berupa paket .deb; saat ini launcher dan source disalin ke home akun baru. Impor/ekspor JSON hanya pengaturan Studio, bukan ekspor seluruh distro.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
