# 10 — Branding Installer, Blur Fix & Sinkronisasi Akhir

Prasyarat: `09-ai-harness`. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sesi ini menerapkan seluruh perbaikan dan branding akhir sebelum build ISO:
- **Plymouth & Initramfs:** tema boot splash `aether-logo` (`apply-hotfix.sh`)
- **Blur Compatibility:** `aether-compat-blur-v6.so` + `kwinrc` (`GLPlatformInterface=glx`) (`apply-blur-fix.sh`)
- **Desktop & Taskbar Sync:** launcher taskbar (`Antigravity`, `Codex`, `Hermes`, `Dolphin`, `Firefox`) & widget `/etc/skel/` (`apply-desktop-sync.sh`)
- **Installer Branding:** branding Calamares & dialog PyQt5 *Try or Install Aether OS* (`apply-installer-brand.sh`)
- **Panel Studio System-Wide Fix:** pindah `AetherPanelStudio` ke `/opt/AetherPanelStudio` & beri izin `+x` semua `.desktop` (`apply-panel-studio-fix.sh`)
- **Polish Akhir:** pasang `aether-voice` & perbarui `initrd.img` (`polish-aether.sh`)

## Langkah manual

```sh
R=/tmp/aether-kubuntu-remaster
cd "$R/scripts"
bash apply-hotfix.sh
bash apply-blur-fix.sh
bash apply-desktop-sync.sh
bash apply-installer-brand.sh
bash apply-panel-studio-fix.sh
bash polish-aether.sh
```
