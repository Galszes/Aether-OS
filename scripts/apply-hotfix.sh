#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_DIR="$(cd "$SCRIPT_DIR/../payloads" && pwd)"

echo "[1/4] Mengekstrak aether-hotfix.tar.gz ke /..."
tar -xzvf "$PAYLOAD_DIR/aether-hotfix.tar.gz" -C /

echo "[2/4] Mengatur tema Plymouth aether-logo..."
update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth 200
update-alternatives --set default.plymouth /usr/share/plymouth/themes/aether-logo/aether-logo.plymouth

echo "[3/4] Memperbarui initramfs..."
update-initramfs -u

echo "[4/4] Verifikasi..."
ls -la /etc/skel/.config/plasmashellrc /etc/skel/.config/kactivitymanagerdrc
readlink -f /etc/alternatives/default.plymouth
echo "=== AETHER HOTFIX SELESAI ==="
