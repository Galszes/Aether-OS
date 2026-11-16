#!/usr/bin/env python3
"""Fix source-home paths in the new user's copied /etc/skel files before Plasma starts."""

import os
import sys
from pathlib import Path


SOURCE_HOME = b'/home/aether'
MARKER = '.config/.aether-remaster-paths-v1'
SEARCH_DIRS = (
    '.config',
    '.local/share/plasma',
    '.local/share/aurorae',
    '.local/share/aether-panel-studio',
    '.local/share/konsole',
    '.local/share/applications',
    '.local/bin',
    'Applications/AetherPanelStudio',
)


def relocate(home):
    home = Path(home).expanduser().resolve()
    if not home.is_dir():
        raise ValueError('Home pengguna tidak ditemukan: ' + str(home))
    marker = home / MARKER
    if marker.exists():
        return 0
    target = os.fsencode(str(home))
    changed = 0
    if target != SOURCE_HOME:
        for rel in SEARCH_DIRS:
            directory = home / rel
            if not directory.exists():
                continue
            for path in directory.rglob('*'):
                if not path.is_file() or path.is_symlink() or path.stat().st_size > 2_000_000:
                    continue
                data = path.read_bytes()
                if SOURCE_HOME not in data or b'\0' in data:
                    continue
                path.write_bytes(data.replace(SOURCE_HOME, target))
                changed += 1
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text('Relocated from /home/aether to ' + str(home) + '\n')
    return changed


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Penggunaan: relocate.py /home/nama-pengguna')
    print('Berkas yang disesuaikan:', relocate(sys.argv[1]))
