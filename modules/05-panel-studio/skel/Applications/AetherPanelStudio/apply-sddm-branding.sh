#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
SRC_DIR="${2:-}"
TARGET_DIR="/usr/share/sddm/themes/aether-sddm"
CONF_FILE="/etc/sddm.conf.d/zz-aether-branding.conf"

case "$ACTION" in
  install)
    if [[ -z "$SRC_DIR" || ! -d "$SRC_DIR" ]]; then
      echo "Direktori sumber tema SDDM tidak ditemukan: $SRC_DIR" >&2
      exit 1
    fi
    rm -rf "$TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    cp -a "$SRC_DIR"/. "$TARGET_DIR"/
    chown -R root:root "$TARGET_DIR"
    chmod -R a+rX "$TARGET_DIR"
    mkdir -p /etc/sddm.conf.d
    cat > "$CONF_FILE" <<'EOF'
[Theme]
Current=aether-sddm
EOF
    chmod 644 "$CONF_FILE"
    echo "Tema SDDM aether-sddm berhasil dipasang di $TARGET_DIR dan diaktifkan di $CONF_FILE"
    ;;
  restore)
    rm -f "$CONF_FILE"
    rm -rf "$TARGET_DIR"
    echo "Konfigurasi SDDM dikembalikan ke bawaan sistem."
    ;;
  *)
    echo "Penggunaan: $0 {install <source_theme_dir>|restore}" >&2
    exit 1
    ;;
esac
