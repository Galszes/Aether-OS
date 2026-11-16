# 04 — Panel terpisah adaptif

Pasang widget dan layout panel. Perubahan di sini mengatur panel, bukan memasang aplikasi Studio.

Prasyarat: 00-persiapan, 03-appearance-glass; 05 untuk helper blur panel. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/04-panel-terpisah-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /etc/skel/.local/share
cp -a "$R/private-assets/panel/share/." /etc/skel/.local/share/
cp -a "$R/modules/04-panel-terpisah/skel/." /etc/skel/
python3 "$R/tools/merge-kconfig.py" "$R/modules/04-panel-terpisah/config/plasma-layout.ini" /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
```

## File dan kode yang terkait

`contents/ui/main.qml` widget menghitung dua latar pada `updateBackgrounds()`. `splitPanel=1` mengaktifkan pemisahan visual; `backgroundOpacity=0.23`, `cornerRadius=21` dan `contentMargin=10` mengatur kaca. Kontainer tetap satu panel Plasma. Celah spacer tidak digambar dan region blur mengikuti bidang yang terlihat lewat helper panel_blur.py milik Studio; karena itu sesi 05 diperlukan untuk blur panel khusus.

Layout snapshot: Home 28; aplikasi 30; tray 32; jam 45; baterai 87; Show Desktop 46. `AppletOrder=82;80;28;31;30;81;32;45;87;46`. ID tersebut bukan nilai universal. Setelah boot: klik kanan panel → Edit Mode, seret baterai atau widget, lalu keluar mode edit. Urbanist jam, tanggal bertumpuk, dan spacer fleksibel sudah disimpan. Wallpaper serta Home logo dipasang pada sesi 06.

Dua template QML harus tetap sinkron: widget aktif di modul 04 dan `data/main.qml` di modul 05. Studio menyalin template miliknya saat Terapkan.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
