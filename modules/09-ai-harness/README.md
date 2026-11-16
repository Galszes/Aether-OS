# 09 — Agentic AI Harness

Prasyarat: `00-persiapan` s/d `08-konsole`. Jalankan di Terminal Cubic setelah `R=/tmp/aether-kubuntu-remaster`.

Sesi ini memasang seluruh **Agentic AI Harness** secara system-wide agar langsung tersedia di Live ISO maupun hasil instalasi:
- **Antigravity (`agy`)** -> `/usr/local/bin/agy` (diambil dari `$R/private-assets/bin/agy`)
- **OpenAI Codex (`codex`)** & **OpenCode (`opencode`)** via `npm`
- **Hermes Agent (`hermes`)** -> `/opt/hermes-agent` + `/opt/hermes-venv` + `/usr/local/bin/hermes`
- **Voice-to-Text (`aether-voice`)** -> `faster-whisper` (`small`) di `/opt/aether-models/whisper`
- **Browser Automation** -> `playwright` + Chromium di `/opt/pw-browsers`
- **Desktop Automation Tools** -> `xdotool`, `wmctrl`, `scrot`, `xclip`, `jq`, `ripgrep`, `tmux`, `libnotify-bin`, `qdbus-qt5`

## Langkah manual

```sh
R=/tmp/aether-kubuntu-remaster
cp -a /etc/skel /var/backups/aether-sessions/09-ai-harness-skel
bash "$R/scripts/install-aether-ai.sh"
```
