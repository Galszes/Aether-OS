# 03 — Appearance dan kaca

Tiga lapisan: Aeos untuk popup/Plasma, Aeos-Blur untuk bilah judul, dan Kvantum AetherGlass untuk permukaan aplikasi Qt.

Prasyarat: 00-persiapan; font dan ikon dianjurkan. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/03-appearance-glass-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /etc/skel/.local/share /etc/skel/.config
cp -a "$R/private-assets/appearance/share/." /etc/skel/.local/share/
cp -a "$R/private-assets/appearance/config/." /etc/skel/.config/
python3 "$R/tools/merge-kconfig.py" "$R/modules/03-appearance-glass/config/kdeglobals.ini" /etc/skel/.config/kdeglobals
python3 "$R/tools/merge-kconfig.py" "$R/modules/03-appearance-glass/config/kwinrc.ini" /etc/skel/.config/kwinrc
python3 "$R/tools/merge-kconfig.py" "$R/modules/03-appearance-glass/config/plasmarc.ini" /etc/skel/.config/plasmarc
```

## File dan kode yang terkait

Kvantum memilih AetherGlass lewat `.config/Kvantum/kvantum.kvconfig`; tema berada di `Kvantum/AetherGlass/`. Aeos berada di `.local/share/plasma/desktoptheme/Aeos`; dekorasi di `.local/share/aurorae/themes/Aeos-Blur/decoration.svg`. Fragment ini mengaktifkan blur KWin bawaan.

Efek VM kompatibilitas **opsional** hanya boleh dipakai jika `dpkg-query -W -f='${Version}' kwin-x11` menghasilkan `4:5.27.11-0ubuntu3`. Binary lokal berada di `private-assets/compat`, source di `source/compat-blur`. Jangan menyalin binary itu pada versi KWin berbeda. Untuk memakai binary yang cocok: salin direktori aether-kvantum ke `/etc/skel/.local/opt/`, buat env yang menambahkan direktori plugin Qt5 itu ke QT_PLUGIN_PATH, lalu pilih `blurEnabled=false` dan `aether-compat-blurEnabled=true` pada kwinrc. Verifikasi di sesi X11 sebelum mengemas ISO. Studio akan memilih plugin kompatibilitas bila binary tersedia; untuk tetap menggunakan native, buat marker `/etc/skel/.config/aether-panel-studio-use-stock-blur`.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.

## Perintah opsional untuk plugin VM dengan versi cocok

Jalankan bagian ini hanya setelah versi KWin diverifikasi persis. Untuk target lain tetap gunakan langkah utama blur native.

```sh
mkdir -p /etc/skel/.local/opt /etc/skel/.config/plasma-workspace/env
cp -a "$R/private-assets/compat/aether-kvantum" /etc/skel/.local/opt/
cat > /etc/skel/.config/plasma-workspace/env/aether-qt-style.sh <<'ENV'
#!/bin/sh
export QT_PLUGIN_PATH="$HOME/.local/opt/aether-kvantum/usr/lib/x86_64-linux-gnu/qt5/plugins${QT_PLUGIN_PATH:+:$QT_PLUGIN_PATH}"
ENV
chmod 755 /etc/skel/.config/plasma-workspace/env/aether-qt-style.sh
kwriteconfig5 --file /etc/skel/.config/kwinrc --group Plugins --key blurEnabled false
kwriteconfig5 --file /etc/skel/.config/kwinrc --group Plugins --key aether-compat-blurEnabled true
```
