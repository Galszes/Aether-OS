# Post-Remaster & AI Harness Scripts

Kumpulan skrip tambahan untuk tahap remastering Cubic (AI harness, blur fix, branding installer, dan sinkronisasi desktop `/etc/skel`):

| Berkas | Fungsi |
|---|---|
| `install-aether-ai.sh` | Instalasi awal AI harness (Hermes, Codex, Antigravity, OpenCode, Playwright, Whisper) |
| `resume-aether-ai.sh` | Melanjutkan instalasi paket/model AI yang tertunda |
| `polish-aether.sh` | Penyesuaian akhir environment & utilitas Aether OS |
| `aether-voice` | Utilitas voice-to-text lokal berbasis `faster-whisper` |
| `apply-blur-fix.sh` | Patch kompatibilitas blur KWin/Kvantum untuk GPU VM & hardware |
| `apply-desktop-sync.sh` | Sinkronisasi launcher taskbar & ikon desktop ke `/etc/skel/` |
| `apply-installer-brand.sh` | Branding Calamares, Plymouth, dan GRUB untuk Aether OS |
| `aether-installer-prompt.py` | Dialog prompt PyQt5 *Try or Install Aether OS* |
| `apply-hotfix.sh` | Hotfix konfigurasi sistem di chroot Cubic |
| `apply-panel-studio-fix.sh` | Pindahkan Aether Panel Studio ke `/opt` & beri izin `+x` pada `.desktop` |
