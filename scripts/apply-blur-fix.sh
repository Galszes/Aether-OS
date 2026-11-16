#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_DIR="$(cd "$SCRIPT_DIR/../payloads" && pwd)"

echo "[1/3] Mengekstrak aether-blur-fix.tar.gz ke /etc/skel..."
tar -xzvf "$PAYLOAD_DIR/aether-blur-fix.tar.gz" -C /etc/skel
chmod +x /etc/skel/.config/plasma-workspace/env/aether-qt-style.sh
chown -R root:root /etc/skel

echo "[2/3] Memastikan /boot/vmlinuz tersedia..."
if [ ! -e /boot/vmlinuz ] && ls /boot/vmlinuz-* >/dev/null 2>&1; then
  ln -sf "$(basename "$(ls /boot/vmlinuz-* | tail -n1)")" /boot/vmlinuz
fi

echo "[3/3] Verifikasi..."
ls -lh /etc/skel/.local/opt/aether-kvantum/usr/lib/x86_64-linux-gnu/qt5/plugins/kwin/effects/plugins/aether-compat-blur-v6.so
ls -lh /etc/skel/.config/plasma-workspace/env/aether-qt-style.sh /etc/skel/.config/kwinrc
echo "=== BLUR FIX SELESAI ==="
