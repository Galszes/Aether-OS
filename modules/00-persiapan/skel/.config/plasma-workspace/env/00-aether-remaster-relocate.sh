#!/bin/sh
# Perbaiki jalur /home/aether sebelum Plasma membaca konfigurasi pengguna baru.
if [ ! -e "$HOME/.config/.aether-remaster-paths-v1" ]; then
    /usr/bin/python3 /usr/local/lib/aether-remaster/relocate.py "$HOME" >"$HOME/.aether-remaster-relocate.log" 2>&1 || true
fi
