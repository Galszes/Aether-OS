#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_DIR="$(cd "$SCRIPT_DIR/../payloads" && pwd)"

echo "[1/3] Mengekstrak aether-desktop-sync.tar.gz ke /..."
tar -xzvf "$PAYLOAD_DIR/aether-desktop-sync.tar.gz" -C /

echo "[2/3] Merapikan ownership /etc/skel & launcher..."
chown -R root:root /etc/skel
chmod 755 /usr/local/share/applications/aether-*.desktop || true
chown root:root /usr/local/share/applications/aether-*.desktop || true

echo "[3/3] Verifikasi..."
grep -n "launchers=" /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
ls -lh /usr/local/share/applications/aether-*.desktop /usr/local/share/icons/aether-ai/
echo "=== DESKTOP & TASKBAR SYNC SELESAI ==="
