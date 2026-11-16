# 06 — Wallpaper dan seluruh branding

Pisahkan wallpaper desktop, logo Home, logo tengah lock/logout, dan tema login SDDM.

Prasyarat: 00-persiapan, 03-appearance-glass, 04-panel-terpisah; 05 untuk editor. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sebelum menyalin, simpan `/etc/skel` dengan nama sesi:

```sh
mkdir -p /var/backups/aether-sessions
cp -a /etc/skel /var/backups/aether-sessions/06-wallpaper-branding-skel
```

Gunakan nama backup baru jika mengulang sesi; jangan menumpuk ke folder backup yang sama.

## Langkah manual

```sh
mkdir -p /etc/skel/.local/share /etc/skel/Downloads /usr/share/sddm/themes
cp -a "$R/private-assets/branding/share/." /etc/skel/.local/share/
cp -a "$R/private-assets/wallpaper/." /etc/skel/Downloads/
cp -a "$R/private-assets/branding/sddm/aether-sddm" /usr/share/sddm/themes/
cp -a "$R/modules/06-wallpaper-branding/root/." /
cp -a "$R/modules/06-wallpaper-branding/skel/." /etc/skel/
python3 "$R/tools/merge-kconfig.py" "$R/modules/06-wallpaper-branding/config/plasma-layout.ini" /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
```

## File dan kode yang terkait

Desktop wallpaper: key Image dalam grup Wallpaper layout Plasma, file Downloads/wallhaven-jer33w_3840x2160.png. Lock background: branding/background.png dan Image pada kscreenlockerrc. Home logo: branding/homeLogo.png, icon pada applet Kickoff dan LogoPath pada kcm-about-distrorc. Header launcher override memakai ikon yang sama.

Logo tengah lock: org.aether.lockstudio/contents/components/UserDelegate.qml. Logout: Aeos/contents/components/UserDelegate.qml. Lingkaran avatar dihilangkan melalui patch_user_delegate() pada branding.py. SDDM memakai tema sistem aether-sddm dan /etc/sddm.conf.d/zz-aether-branding.conf. Lock (Meta+L), logout, login, dan splash merupakan komponen berbeda. Setelah boot, ubah melalui Studio → Layar kunci & Logo; SDDM memerlukan tombol Pasang ke Login SDDM (Admin).

Lihat `MANIFEST.json` untuk daftar payload dan checksum berkas sesi ini. Nilai ID widget pada snapshot berasal dari desktop sumber; instalasi lain dapat memiliki ID berbeda.
