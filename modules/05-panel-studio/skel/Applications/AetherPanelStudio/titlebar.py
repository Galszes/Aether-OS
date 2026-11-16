"""Edit the two visible surface colors of the installed Aeos-Blur decoration."""
from datetime import datetime
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QFormLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget


class TitlebarColors:
    def __init__(self, home=None):
        self.home = Path(home or Path.home())
        self.svg = self.home / '.local/share/aurorae/themes/Aeos-Blur/decoration.svg'
        self.backups = self.home / 'theme-backups/AetherTitlebar'

    def read(self):
        source = self.svg.read_text()
        top = re.search(r'id="decoration-top"[\s\S]*?</g>', source)
        if not top:
            raise RuntimeError('Bagian bilah judul Aeos-Blur tidak ditemukan.')
        fills = re.findall(r'fill:(#[0-9a-fA-F]{6})', top.group())
        if len(fills) < 2:
            raise RuntimeError('Warna bilah judul Aeos-Blur tidak dikenali.')
        return {'titlebarBase': fills[0].lower(), 'titlebarEdge': fills[1].lower()}

    def backup(self):
        self.backups.mkdir(parents=True, exist_ok=True)
        snapshot = self.backups / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        snapshot.mkdir()
        shutil.copy2(self.svg, snapshot / 'decoration.svg')
        return snapshot

    def reconfigure(self):
        result = subprocess.run(['qdbus', 'org.kde.KWin', '/KWin', 'org.kde.KWin.reconfigure'],
                                text=True, capture_output=True, timeout=15)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or 'KWin gagal memuat ulang dekorasi.')

    def apply(self, colors):
        for key in ('titlebarBase', 'titlebarEdge'):
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', colors.get(key, '')):
                raise ValueError('Warna bilah judul tidak valid: ' + key)
        old = self.read()
        if all(colors[key].lower() == old[key] for key in old):
            return None
        before = self.svg.read_text()
        backup = self.backup()
        mapping = {old[key]: colors[key].lower() for key in old}
        updated = re.sub(r'(?<![\w-])fill:(#[0-9a-fA-F]{6})',
                         lambda m: 'fill:' + mapping.get(m.group(1).lower(), m.group(1)), before)
        ET.fromstring(updated)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.svg.parent,
                                             prefix='.decoration-', suffix='.svg', delete=False) as f:
                temp_path = Path(f.name)
                f.write(updated)
            os.chmod(temp_path, self.svg.stat().st_mode)
            os.replace(temp_path, self.svg)
            self.reconfigure()
        except Exception:
            if temp_path and temp_path.exists(): temp_path.unlink()
            shutil.copy2(backup / 'decoration.svg', self.svg)
            try: self.reconfigure()
            except Exception: pass
            raise
        return backup

    def restore(self, backup):
        backup = Path(backup).resolve()
        if backup.parent != self.backups.resolve() or not (backup / 'decoration.svg').is_file():
            raise ValueError('Backup bilah judul tidak valid.')
        current = self.backup()
        try:
            shutil.copy2(backup / 'decoration.svg', self.svg)
            self.reconfigure()
        except Exception:
            shutil.copy2(current / 'decoration.svg', self.svg)
            try: self.reconfigure()
            except Exception: pass
            raise


class TitlebarTab(QWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = TitlebarColors()
        self.colors = self.backend.read()
        self.original = dict(self.colors)
        self.dirty = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel('Bilah judul Aeos-Blur')
        title.setStyleSheet('font-size:20px;font-weight:bold')
        layout.addWidget(title)
        note = QLabel('Atur warna dasar bilah judul dan garis tepi biru pada jendela yang memakai dekorasi Aeos-Blur. Tombol Terapkan di bawah aplikasi juga menyimpan pilihan ini.')
        note.setWordWrap(True)
        layout.addWidget(note)
        form = QFormLayout()
        self.buttons = {}
        for key, caption in [('titlebarBase', 'Warna dasar bilah judul'),
                             ('titlebarEdge', 'Warna garis tepi')]:
            button = QPushButton()
            button.clicked.connect(lambda checked=False, k=key: self.pick(k))
            form.addRow(caption, button)
            self.buttons[key] = button
        layout.addLayout(form)
        self.status = QLabel('Warna tema Aeos-Blur saat ini.')
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        apply_button = QPushButton('Terapkan bilah judul')
        apply_button.clicked.connect(self.apply)
        layout.addWidget(apply_button)
        restore_button = QPushButton('Pulihkan warna sebelumnya')
        restore_button.clicked.connect(self.restore)
        layout.addWidget(restore_button)
        layout.addStretch()
        self.show_colors()

    def show_colors(self):
        for key, button in self.buttons.items():
            color = self.colors[key]
            button.setText(color.upper())
            button.setStyleSheet('QPushButton { border-left: 14px solid ' + color + '; }')

    def pick(self, key):
        color = QColorDialog.getColor(QColor(self.colors[key]), self, 'Pilih warna bilah judul')
        if color.isValid():
            self.colors[key] = color.name()
            self.dirty = self.colors != self.original
            self.show_colors()
            self.status.setText('Warna belum diterapkan.' if self.dirty else 'Warna tema Aeos-Blur saat ini.')
            self.selectionChanged.emit()

    def discard(self):
        self.colors = dict(self.original)
        self.dirty = False
        self.show_colors()
        self.selectionChanged.emit()

    def apply_selection(self):
        if not self.dirty: return None
        backup = self.backend.apply(self.colors)
        self.original = self.backend.read()
        self.discard()
        self.status.setText('Bilah judul diperbarui. Backup: ' + str(backup))
        return backup

    def apply(self):
        try: self.apply_selection()
        except Exception as exc: QMessageBox.critical(self, 'Bilah judul', str(exc))

    def restore(self):
        snapshots = sorted(self.backend.backups.glob('*/decoration.svg'), reverse=True)
        if not snapshots:
            QMessageBox.information(self, 'Backup', 'Belum ada backup bilah judul.')
            return
        if QMessageBox.question(self, 'Pulihkan', 'Pulihkan warna bilah judul sebelum perubahan terakhir?') != QMessageBox.Yes:
            return
        try:
            self.backend.restore(snapshots[0].parent)
            self.original = self.backend.read()
            self.discard()
            self.status.setText('Warna sebelumnya dipulihkan.')
        except Exception as exc: QMessageBox.critical(self, 'Bilah judul', str(exc))
