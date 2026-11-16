#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
export NODE_OPTIONS="--dns-result-order=ipv4first"

if [ ! -e /usr/local/lib/node_modules/@openai/codex/bin/codex.js ]; then
  echo "=== [4a/8] Menginstall Codex dari paket lokal ==="
  python3 -c "import urllib.request; urllib.request.urlretrieve('http://127.0.0.1:8765/codex-pkg.tar.gz', '/tmp/codex-pkg.tar.gz')"
  mkdir -p /usr/local/lib/node_modules
  tar -xzf /tmp/codex-pkg.tar.gz -C /usr/local/lib/node_modules
  ln -sf ../lib/node_modules/@openai/codex/bin/codex.js /usr/local/bin/codex
  rm -f /tmp/codex-pkg.tar.gz
fi

echo "=== [4b/8] Membersihkan sisa & menginstall OpenCode via npm ==="
rm -rf /usr/local/lib/node_modules/opencode-ai /usr/local/lib/node_modules/.opencode-ai-*
npm install -g --fetch-retries=5 --fetch-timeout=300000 --fetch-retry-maxtimeout=120000 opencode-ai

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

echo "=== [8/8] Bersih-bersih cache & verifikasi ==="
rm -rf /root/.cache/pip /root/.npm
apt-get clean

echo "--- Verifikasi Binary ---"
which hermes codex agy opencode xdotool wmctrl curl git ffmpeg dolphin python3 playwright
ls -lh /opt/aether-models/whisper /opt/pw-browsers
echo "=== SEMUA INSTALASI AETHER OS SELESAI ==="
