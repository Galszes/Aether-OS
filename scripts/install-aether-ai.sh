#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
export NODE_OPTIONS="--dns-result-order=ipv4first"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== [1/8] Menghapus paket game & wallpaper bawaan ==="
apt-get purge -y kmines kpat ksudoku kmahjongg kubuntu-wallpapers plasma-workspace-wallpapers || true
apt-get autoremove -y

echo "=== [2/8] Menginstall paket APT kontrol desktop & runtime ==="
apt-get update
apt-get install -y \
  xdotool wmctrl curl scrot xclip jq ripgrep tmux libnotify-bin \
  python3-venv python3-pip portaudio19-dev nodejs npm qdbus-qt5

echo "=== [3/8] Menginstall Antigravity (agy) system-wide ==="
if [ -f "$REPO_DIR/private-assets/bin/agy" ]; then
  cp -f "$REPO_DIR/private-assets/bin/agy" /usr/local/bin/agy
  chmod +x /usr/local/bin/agy
else
  echo "PERINGATAN: private-assets/bin/agy tidak ditemukan (unduh arsip Release terlebih dahulu)."
fi

echo "=== [4/8] Menginstall Codex & OpenCode via npm ==="
npm install -g --fetch-retries=5 --fetch-timeout=300000 --fetch-retry-maxtimeout=120000 @openai/codex opencode-ai

echo "=== [5/8] Menginstall Faster-Whisper & Playwright ke /opt/aether-venv ==="
python3 -m venv /opt/aether-venv
/opt/aether-venv/bin/pip install --upgrade pip
/opt/aether-venv/bin/pip install faster-whisper sounddevice numpy playwright
ln -sf /opt/aether-venv/bin/playwright /usr/local/bin/playwright

echo "=== [6/8] Menginstall Playwright Chromium & model Whisper small ==="
mkdir -p /opt/pw-browsers /opt/aether-models/whisper
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers /opt/aether-venv/bin/playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers /opt/aether-venv/bin/playwright install-deps chromium
grep -q "PLAYWRIGHT_BROWSERS_PATH" /etc/environment || echo 'PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers' >> /etc/environment

/opt/aether-venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8', download_root='/opt/aether-models/whisper')"
grep -q "AETHER_WHISPER_MODEL_DIR" /etc/environment || echo 'AETHER_WHISPER_MODEL_DIR=/opt/aether-models/whisper' >> /etc/environment

echo "=== [7/8] Menginstall Hermes Agent ke /opt/hermes-agent ==="
rm -rf /opt/hermes-agent /opt/hermes-venv
git clone --depth 1 https://github.com/NousResearch/hermes-agent.git /opt/hermes-agent
python3 -m venv /opt/hermes-venv
/opt/hermes-venv/bin/pip install --upgrade pip
/opt/hermes-venv/bin/pip install -e /opt/hermes-agent
ln -sf /opt/hermes-venv/bin/hermes /usr/local/bin/hermes
[ -f /opt/hermes-venv/bin/hermes-acp ] && ln -sf /opt/hermes-venv/bin/hermes-acp /usr/local/bin/hermes-acp || true

echo "=== [8/8] Memasang aether-voice & bersih-bersih cache ==="
cp -f "$SCRIPT_DIR/aether-voice" /usr/local/bin/aether-voice
chmod +x /usr/local/bin/aether-voice
rm -rf /root/.cache/pip /root/.npm
apt-get clean

echo "--- Verifikasi Binary ---"
which hermes codex opencode aether-voice xdotool wmctrl curl git ffmpeg dolphin python3 playwright || true
ls -lh /usr/local/bin/agy /opt/aether-models/whisper /opt/pw-browsers
echo "=== INSTALASI AI HARNESS SELESAI ==="
