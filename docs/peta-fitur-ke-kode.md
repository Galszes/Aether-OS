# Peta fitur → kode → file hasil

Source Studio: `modules/05-panel-studio/skel/Applications/AetherPanelStudio/`.

| Fitur | Fungsi sumber | File hasil di akun pengguna |
|---|---|---|
| Panel terpisah | app.py FIELDS; backend.py CONFIG_KEYS; data/main.qml updateBackgrounds | layout Plasma key splitPanel; QML widget Panel Islands |
| Transparansi/rounded/shadow panel | main.qml backgroundComponent | layout Plasma backgroundOpacity, cornerRadius, shadow* |
| Highlight aplikasi/tray | backend.py write_theme / update_frames | Aeos/widgets/tasks.svg, tabbar.svg |
| Popup/tooltip rounded | backend.py write_theme / write_tooltip | Aeos/dialogs/background.svg, widgets/background.svg, tooltip.svg beserta varian |
| Blur | backend.py configure_blur; panel_blur.py | kwinrc, region blur X11; source opsional blur.cpp |
| Dolphin/Kvantum | backend.py write_kvantum | AetherGlass.kvconfig dan AetherGlass.svg |
| Bilah judul | titlebar.py TitlebarColors.apply | aurorae/themes/Aeos-Blur/decoration.svg |
| Wallpaper desktop | Plasma Configure Desktop | plasma-org.kde.plasma.desktop-appletsrc / Image |
| Lock background | branding.py Branding.apply | branding/background.png, kscreenlockerrc |
| Logo Home / System Information | branding.py Branding.apply | icon Kickoff, kcm-about-distrorc LogoPath, homeLogo.png |
| Logo tengah tanpa lingkaran | branding.py patch_user_delegate | UserDelegate.qml pada lock, logout, SDDM |
| Login SDDM | branding.py build_sddm_theme; apply-sddm-branding.sh | /usr/share/sddm/themes/aether-sddm, /etc/sddm.conf.d |
| Splash | splash.py build_package / _qml | Splash.qml, images, ksplashrc |
| Font global | Plasma Fonts | kdeglobals; fontconfig |
| Jam dan baterai | Plasma panel editor dan Digital Clock | AppletOrder, fontFamily, fontSize, showDate pada layout |

Ganti gambar lewat editor untuk memperbarui state sekaligus. Mengganti file gambar secara manual dengan nama/ekstensi sama dapat mempertahankan path, tetapi QML atau aplikasi yang menyimpan cache perlu dibuka ulang. Mengedit QML hasil generator bisa tertimpa oleh Terapkan berikutnya.
