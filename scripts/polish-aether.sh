#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== [1/4] Merapikan ownership /etc/skel ==="
chown -R root:root /etc/skel

echo "=== [2/4] Menginstall qdbus-qt5 ==="
apt-get update
apt-get install -y qdbus-qt5
apt-get clean

echo "=== [3/4] Memasang /usr/local/bin/aether-voice ==="
cp -f "$SCRIPT_DIR/aether-voice" /usr/local/bin/aether-voice
chmod +x /usr/local/bin/aether-voice

echo "=== [4/4] Membuat initrd dengan tema Plymouth aether-logo ==="
KVER=$(ls /lib/modules | tail -n 1)
echo "Kernel terdeteksi: $KVER"
if [ -f "/boot/initrd.img-$KVER" ]; then
  update-initramfs -u -k "$KVER"
else
  update-initramfs -c -k "$KVER"
fi
ls -lh /boot/initrd.img*
echo "=== POLISH AETHER OS SELESAI ==="
