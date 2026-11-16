# Menyiapkan aset setelah clone GitHub

Aset lokal sudah tersedia pada folder kerja ini. GitHub hanya membawa kode dan konfigurasi yang siap ditinjau; `private-assets/` tidak ikut Git. Untuk mereproduksi tampilan pada komputer lain, salin aset berizin ke path yang disebut README modul. Aset bertema Aeos pada salinan ini sudah dimodifikasi; mengunduh Aeos asli saja tidak memberikan highlight/popup yang sama.

| Sesi | Folder aset lokal yang harus disediakan |
|---|---|
| Font | private-assets/fonts/{g,u,r} |
| Ikon | private-assets/icons/Vivid-Glassy-Dark-Icons |
| Appearance | private-assets/appearance/{share,config} |
| Panel | private-assets/panel/share/plasma/plasmoids |
| Branding | private-assets/branding/{share,sddm} dan private-assets/wallpaper |
| Splash | private-assets/splash/org.aether.splashstudio |
| Blur VM opsional | private-assets/compat/aether-kvantum |

Jika nantinya izin distribusi sudah jelas, pindahkan aset yang diperbolehkan ke folder publik per modul, simpan lisensi sumber dan perbarui README. Hindari `git add -f private-assets` secara keseluruhan. Versi arsip lama tetap tersimpan terpisah di Documents.
