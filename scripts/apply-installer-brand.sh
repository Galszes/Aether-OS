#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_DIR="$(cd "$SCRIPT_DIR/../payloads" && pwd)"

echo "[1/3] Backup kubuntu-installer-prompt asli & hapus 12 slide Kubuntu..."
if [ -f /usr/bin/kubuntu-installer-prompt ] && [ ! -f /usr/bin/kubuntu-installer-prompt.orig ]; then
  mv /usr/bin/kubuntu-installer-prompt /usr/bin/kubuntu-installer-prompt.orig
fi
rm -f /etc/calamares/branding/kubuntu/[0-9][0-9]_*.png

echo "[2/3] Memasang branding Calamares + Aether Prompt..."
tar -xzvf "$PAYLOAD_DIR/aether-installer-brand.tar.gz" -C /
chmod +x /usr/bin/kubuntu-installer-prompt

echo "[3/3] Mengubah shortcut installer Kubuntu -> Aether OS..."
if [ -f /usr/share/applications/kubuntu-calamares.desktop ]; then
  sed -i 's/Install Kubuntu/Install Aether OS/g' /usr/share/applications/kubuntu-calamares.desktop
  sed -i 's|^Icon=.*|Icon=/etc/calamares/branding/kubuntu/icon.png|' /usr/share/applications/kubuntu-calamares.desktop
fi

ls -lh /usr/bin/kubuntu-installer-prompt /etc/calamares/branding/kubuntu/
echo "=== INSTALLER BRANDING & PROMPT AETHER OS SELESAI ==="
