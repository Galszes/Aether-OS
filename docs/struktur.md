# Struktur dan aturan pembaruan

```
aether-kubuntu-remaster/
  README.md
  ASSETS.md
  modules/
    00-persiapan/ ... 09-build-iso/
      README.md       # perintah manual satu sesi
      MANIFEST.json   # checksum payload sesi
      config/         # fragmen INI, jika diperlukan
      skel/           # isi yang disalin ke /etc/skel
      root/           # isi yang disalin ke akar filesystem Cubic
      source/         # source efek opsional, jika ada
  tools/merge-kconfig.py
  docs/               # peta kode, presentasi, screenshot, PDF
  private-assets/     # salinan lokal, diabaikan Git
```

Kode widget terpasang ada di modul 04. Template yang dipasang ulang Studio ada di `modules/05-panel-studio/skel/Applications/AetherPanelStudio/data/`. Jika mengubah QML/schema panel, perbarui kedua salinan agar Terapkan Studio tidak mengembalikan versi lama. Nilai awal UI berada di backend.py DEFAULTS, pemetaan key widget di CONFIG_KEYS, dan pilihan UI di app.py FIELDS.

Saat mengubah font/ikon/warna, ubah fragmen sesi masing-masing. Saat menambah aset, catat asal dan lisensi di ASSETS.md. Setelah mengubah payload, perbarui checksum pada MANIFEST.json. Ini repositori persiapan; belum dipublikasikan dan belum diberi tag rilis.
