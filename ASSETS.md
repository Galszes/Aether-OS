# Aset eksternal dan atribusi

`private-assets/` berisi salinan lokal untuk praktik Cubic dan masuk `.gitignore`. Folder ini tidak ikut clone GitHub; README modul menjelaskan kebutuhan aset dan jalur yang harus disediakan. Sebelum menerbitkan repositori, putuskan aset mana yang boleh didistribusikan dan sertakan lisensi/aslinya.

| Aset | Letak lokal | Status yang diketahui |
|---|---|---|
| Google Sans | private-assets/fonts/g | Izin distribusi harus dipastikan dari sumber font |
| Urbanist | private-assets/fonts/u | Sertakan teks lisensi dari paket sumber sebelum publikasi |
| Rounded Elegance | private-assets/fonts/r | Izin distribusi harus dipastikan dari sumber font |
| IBM Plex | apt: fonts-ibm-plex | Dipasang dari repositori Ubuntu |
| Vivid-Glassy-Dark-Icons | private-assets/icons | Pertahankan atribusi dan periksa lisensi tema sumber |
| Aeos / Aeos-Blur | private-assets/appearance/share | Metadata menyebut l4k1, GPLv3; modifikasi lokal tetap perlu membawa lisensi upstream |
| Override Kickoff/tray/lock/SDDM | private-assets/panel dan branding | Turunan komponen KDE; pertahankan copyright dan lisensi upstream |
| Wallpaper dan logo | private-assets/wallpaper, branding, splash | Periksa hak gambar sebelum publikasi |
| Binary blur VM | private-assets/compat | Khusus KWin X11 4:5.27.11-0ubuntu3; jangan anggap portable |

Kode Studio dan widget kustom disimpan pada modul 04/05. Repositori ini belum diberi satu lisensi menyeluruh karena asal dan ketentuan tiap komponen perlu ditetapkan; jangan mengklaim semua aset sebagai karya sendiri. Daftar ini adalah catatan pengemasan, bukan izin distribusi baru.
