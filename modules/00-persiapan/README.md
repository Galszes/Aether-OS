# 00 — Persiapan Cubic

Buat proyek dari ISO Kubuntu 24.04 x86_64, lalu masuk Terminal Cubic (sudah root). Salin folder repositori beserta aset lokal ke /tmp. Jangan menggunakan file akun pribadi sebagai bahan ISO.

## Langkah manual

```sh
R=/tmp/aether-kubuntu-remaster
cat /etc/os-release
apt-get update
apt-get purge -y kmines kpat ksudoku kmahjongg kubuntu-wallpapers plasma-workspace-wallpapers
apt-get autoremove -y
apt-get install -y python3-pyqt5 qt5-style-kvantum fonts-ibm-plex
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/00-original-skel
cp -a "$R/modules/00-persiapan/root/." /
cp -a "$R/modules/00-persiapan/skel/." /etc/skel/
chmod 755 /etc/skel/.config/plasma-workspace/env/00-aether-remaster-relocate.sh
```

## File dan kode yang terkait

Hook env berjalan sebelum Plasma untuk mengganti path `/home/aether` menjadi home akun baru. Source berada di `root/usr/local/lib/aether-remaster/relocate.py`. Ini hanya penyesuai path, bukan pemasang seluruh modul. Biarkan hook tersedia sebelum sesi 04–08. Terminal Cubic tidak menjalankan desktop; lihat hasil setelah boot VM.

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
