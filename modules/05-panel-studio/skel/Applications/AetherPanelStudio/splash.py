"""Editor for the Plasma session splash screen (not the SDDM login screen)."""

import configparser
import datetime
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPixmap, QImageReader, QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton,
    QLineEdit, QSlider, QFileDialog, QColorDialog, QMessageBox, QCheckBox,
    QFontComboBox,
)


DEFAULTS = {
    'title': 'Aether Desktop',
    'subtitle': 'Menyiapkan desktop…',
    'backgroundColor': '#000000',
    'accentColor': '#59b8f4',
    'overlayOpacity': 60,
    'fontFamily': 'Urbanist',
    'showProgress': True,
    'background': '',
    'logo': '',
}


def _qml_string(value):
    return json.dumps(value, ensure_ascii=False)


class SplashStudio:
    theme_id = 'org.aether.splashstudio'

    def __init__(self, home=None):
        self.home = Path(home or Path.home())
        self.config = self.home / '.config/ksplashrc'
        self.state = self.home / '.config/aether-splash-studio.json'
        self.package = self.home / '.local/share/plasma/look-and-feel' / self.theme_id
        self.backups = self.home / 'theme-backups/AetherSplashStudio'
        self.aeos = self.home / '.local/share/plasma/look-and-feel/Aeos/contents/splash/images'

    def read(self):
        data = dict(DEFAULTS)
        if self.state.exists():
            data.update(json.loads(self.state.read_text()))
        else:
            for key, name in [('background', 'background.jpeg'), ('logo', 'KDE_Plasma_5_banner.png')]:
                path = self.aeos / name
                if path.is_file():
                    data[key] = str(path)
        return data

    def active_theme(self):
        c = configparser.ConfigParser(interpolation=None)
        c.optionxform = str
        c.read(self.config)
        return c.get('KSplash', 'Theme', fallback='')

    def validate(self, data):
        result = dict(DEFAULTS)
        result.update(data)
        for key in ('title', 'subtitle'):
            if not isinstance(result[key], str) or len(result[key]) > 100 or '\n' in result[key]:
                raise ValueError('Teks splash harus satu baris, maksimal 100 karakter.')
        if not isinstance(result['fontFamily'], str) or not result['fontFamily'].strip() or len(result['fontFamily']) > 80 or '\n' in result['fontFamily']:
            raise ValueError('Nama font splash tidak valid.')
        result['fontFamily'] = result['fontFamily'].strip()
        for key in ('backgroundColor', 'accentColor'):
            color = QColor(result[key])
            if not color.isValid():
                raise ValueError('Warna tidak valid: ' + str(result[key]))
            result[key] = color.name()
        result['overlayOpacity'] = int(result['overlayOpacity'])
        if not 0 <= result['overlayOpacity'] <= 100:
            raise ValueError('Opasitas lapisan harus 0–100%.')
        result['showProgress'] = bool(result['showProgress'])
        for key in ('background', 'logo'):
            if result[key]:
                p = Path(result[key]).expanduser()
                if not p.is_file() or not QImageReader(str(p)).canRead():
                    raise ValueError('Gambar tidak dapat dibaca: ' + str(p))
                result[key] = str(p.resolve())
        return result

    def backup(self):
        self.backups.mkdir(parents=True, exist_ok=True)
        dest = self.backups / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        dest.mkdir()
        for source, name in [(self.config, 'ksplashrc'), (self.state, 'state.json')]:
            if source.exists():
                shutil.copy2(source, dest / name)
        if self.package.exists():
            shutil.copytree(self.package, dest / 'package')
        return dest

    def build_package(self, destination, data):
        data = self.validate(data)
        dest = Path(destination)
        images = dest / 'contents/splash/images'
        images.mkdir(parents=True, exist_ok=True)
        assets = {}
        for key in ('background', 'logo'):
            if data[key]:
                name = key + Path(data[key]).suffix.lower()
                shutil.copy2(data[key], images / name)
                assets[key] = name
            else:
                assets[key] = ''
        (dest / 'metadata.desktop').write_text(
            '[Desktop Entry]\nName=Aether Splash Studio\n'
            'Comment=Custom session splash screen\n'
            'X-KDE-PluginInfo-Name=' + self.theme_id + '\n'
            'X-KDE-ServiceTypes=Plasma/LookAndFeel\n'
            'X-KDE-PluginInfo-Version=1.0\n'
        )
        (dest / 'metadata.json').write_text(json.dumps({
            'KPlugin': {'Id': self.theme_id, 'Name': 'Aether Splash Studio',
                        'ServiceTypes': ['Plasma/LookAndFeel'], 'Version': '1.0'},
            'X-Plasma-APIVersion': '2',
        }, indent=2))
        (dest / 'contents/splash/Splash.qml').write_text(self._qml(data, assets))
        return assets

    def _qml(self, data, assets):
        background = 'images/' + assets['background'] if assets['background'] else ''
        logo = 'images/' + assets['logo'] if assets['logo'] else ''
        progress = 'true' if data['showProgress'] else 'false'
        return f'''import QtQuick 2.15

Rectangle {{
    id: root
    color: {_qml_string(data['backgroundColor'])}
    property int stage: 0

    Image {{
        anchors.fill: parent
        source: {_qml_string(background)}
        fillMode: Image.PreserveAspectCrop
        visible: source !== ""
        asynchronous: true
    }}
    Rectangle {{
        anchors.fill: parent
        color: {_qml_string(data['backgroundColor'])}
        opacity: {data['overlayOpacity'] / 100:.2f}
    }}
    Column {{
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.72, 600)
        spacing: 12

        Image {{
            anchors.horizontalCenter: parent.horizontalCenter
            width: Math.min(parent.width * 0.8, 420)
            height: Math.min(root.height * 0.20, 150)
            source: {_qml_string(logo)}
            fillMode: Image.PreserveAspectFit
            visible: source !== ""
            asynchronous: true
        }}
        Text {{
            width: parent.width
            text: {_qml_string(data['title'])}
            color: "#edf8ff"
            font.family: {_qml_string(data['fontFamily'])}
            font.pixelSize: Math.max(18, Math.min(root.height * 0.034, 34))
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            elide: Text.ElideRight
        }}
        Text {{
            width: parent.width
            text: {_qml_string(data['subtitle'])}
            color: "#c7e4fa"
            font.family: {_qml_string(data['fontFamily'])}
            font.pixelSize: Math.max(12, Math.min(root.height * 0.021, 21))
            horizontalAlignment: Text.AlignHCenter
            elide: Text.ElideRight
        }}
        Item {{ width: 1; height: 12 }}
        Rectangle {{
            id: track
            anchors.horizontalCenter: parent.horizontalCenter
            width: Math.min(parent.width * 0.6, 310)
            height: 4
            radius: 2
            color: "#3b607c"
            visible: {progress}
            Rectangle {{
                width: parent.width * Math.min(1, Math.max(0, root.stage / 5))
                height: parent.height
                radius: parent.radius
                color: {_qml_string(data['accentColor'])}
                Behavior on width {{ NumberAnimation {{ duration: 250 }} }}
            }}
        }}
    }}
}}
'''

    def apply(self, values):
        data = self.validate(values)
        backup = self.backup()
        try:
            self.package.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.aether-splash-', dir=self.package.parent) as temp:
                staged = Path(temp) / self.theme_id
                assets = self.build_package(staged, data)
                # Save stable paths inside the installed package for later edits.
                for key in ('background', 'logo'):
                    data[key] = str(self.package / 'contents/splash/images' / assets[key]) if assets[key] else ''
                if self.package.exists():
                    shutil.rmtree(self.package)
                shutil.move(str(staged), str(self.package))
            c = configparser.ConfigParser(interpolation=None)
            c.optionxform = str
            c.read(self.config)
            if not c.has_section('KSplash'):
                c.add_section('KSplash')
            c['KSplash']['Theme'] = self.theme_id
            c['KSplash']['Engine'] = 'KSplashQML'
            self.config.parent.mkdir(parents=True, exist_ok=True)
            with self.config.open('w') as f:
                c.write(f, space_around_delimiters=False)
            self.state.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            return backup
        except Exception:
            self.restore(backup)
            raise

    def restore(self, backup):
        backup = Path(backup).resolve()
        if backup.parent != self.backups.resolve():
            raise ValueError('Backup splash tidak valid.')
        for destination, name in [(self.config, 'ksplashrc'), (self.state, 'state.json')]:
            source = backup / name
            if source.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            elif destination.exists():
                destination.unlink()
        if self.package.exists():
            shutil.rmtree(self.package)
        if (backup / 'package').exists():
            shutil.copytree(backup / 'package', self.package)


class SplashPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.data = dict(DEFAULTS)
        self.setMinimumSize(340, 190)

    def paintEvent(self, _event):
        d = self.data
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.fillRect(self.rect(), QColor(d['backgroundColor']))
        if d['background']:
            pix = QPixmap(d['background'])
            if not pix.isNull():
                scaled = pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                x = (scaled.width() - self.width()) // 2
                y = (scaled.height() - self.height()) // 2
                p.drawPixmap(self.rect(), scaled, scaled.rect().adjusted(x, y, -x, -y))
        overlay = QColor(d['backgroundColor'])
        overlay.setAlpha(round(d['overlayOpacity'] * 2.55))
        p.fillRect(self.rect(), overlay)
        center = self.width() // 2
        cy = self.height() // 2
        if d['logo']:
            logo = QPixmap(d['logo'])
            if not logo.isNull():
                logo = logo.scaled(min(self.width() * 0.48, 190), 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                p.drawPixmap(center - logo.width() // 2, cy - 83, logo)
        p.setPen(QColor('#edf8ff'))
        font = p.font()
        font.setFamily(d['fontFamily'])
        font.setPointSize(13)
        font.setBold(True)
        p.setFont(font)
        p.drawText(0, cy + 12, self.width(), 25, Qt.AlignCenter, d['title'])
        font.setPointSize(9)
        font.setBold(False)
        p.setFont(font)
        p.setPen(QColor('#c7e4fa'))
        p.drawText(0, cy + 40, self.width(), 20, Qt.AlignCenter, d['subtitle'])
        if d['showProgress']:
            width = min(180, self.width() * 0.55)
            p.fillRect(int(center - width / 2), cy + 70, int(width), 3, QColor('#3b607c'))
            p.fillRect(int(center - width / 2), cy + 70, int(width * .65), 3, QColor(d['accentColor']))
        p.end()


class SplashTab(QWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = SplashStudio()
        self.current = self.backend.read()
        self.applied = dict(self.current)
        self.dirty = False
        self.preview_process = None
        self.preview_dir = None
        v = QVBoxLayout(self)
        v.setContentsMargins(18, 18, 18, 18)
        heading = QLabel('Splash Screen — saat masuk desktop')
        heading.setStyleSheet('font-size:20px;font-weight:bold')
        v.addWidget(heading)
        note = QLabel('Layar ini muncul setelah login SDDM, saat Plasma menyiapkan desktop. Gambar dan teks dapat diganti tanpa mengubah layar login atau layar kunci.')
        note.setWordWrap(True)
        v.addWidget(note)
        self.preview = SplashPreview()
        v.addWidget(self.preview)
        form = QFormLayout()
        v.addLayout(form)
        self.image_buttons = {}
        for key, label in [('background', 'Gambar latar'), ('logo', 'Logo tengah')]:
            row = QHBoxLayout()
            name = QLabel()
            name.setWordWrap(True)
            choose = QPushButton('Pilih…')
            choose.clicked.connect(lambda checked=False, k=key: self.pick_image(k))
            clear = QPushButton('Hapus')
            clear.clicked.connect(lambda checked=False, k=key: self.set_value(k, ''))
            row.addWidget(name, 1)
            row.addWidget(choose)
            row.addWidget(clear)
            form.addRow(label, row)
            self.image_buttons[key] = name
        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(100)
        self.title_edit.textChanged.connect(lambda text: self.set_value('title', text))
        form.addRow('Judul', self.title_edit)
        self.subtitle_edit = QLineEdit()
        self.subtitle_edit.setMaxLength(100)
        self.subtitle_edit.textChanged.connect(lambda text: self.set_value('subtitle', text))
        form.addRow('Teks kecil', self.subtitle_edit)
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(lambda font: self.set_value('fontFamily', font.family()))
        form.addRow('Font teks', self.font_combo)
        self.colors = {}
        for key, label in [('backgroundColor', 'Warna dasar & lapisan'), ('accentColor', 'Warna progress')]:
            button = QPushButton()
            button.clicked.connect(lambda checked=False, k=key: self.pick_color(k))
            form.addRow(label, button)
            self.colors[key] = button
        self.overlay = QSlider(Qt.Horizontal)
        self.overlay.setRange(0, 100)
        self.overlay.valueChanged.connect(lambda value: self.set_value('overlayOpacity', value))
        form.addRow('Lapisan gelap (%)', self.overlay)
        self.progress = QCheckBox('Tampilkan garis progress')
        self.progress.toggled.connect(lambda value: self.set_value('showProgress', value))
        form.addRow('', self.progress)
        row = QHBoxLayout()
        for label, method in [('Pratinjau nyata', self.open_preview), ('Terapkan splash', self.apply), ('Pulihkan terakhir', self.restore)]:
            button = QPushButton(label)
            button.clicked.connect(method)
            row.addWidget(button)
        v.addLayout(row)
        self.status = QLabel()
        self.status.setWordWrap(True)
        v.addWidget(self.status)
        v.addStretch()
        self.load(self.current)

    def load(self, data):
        self.current = dict(data)
        for widget in (self.title_edit, self.subtitle_edit, self.font_combo, self.overlay, self.progress):
            widget.blockSignals(True)
        self.title_edit.setText(self.current['title'])
        self.subtitle_edit.setText(self.current['subtitle'])
        self.font_combo.setCurrentFont(QFont(self.current['fontFamily']))
        self.overlay.setValue(self.current['overlayOpacity'])
        self.progress.setChecked(self.current['showProgress'])
        for widget in (self.title_edit, self.subtitle_edit, self.font_combo, self.overlay, self.progress):
            widget.blockSignals(False)
        for key, label in self.image_buttons.items():
            label.setText(Path(self.current[key]).name if self.current[key] else 'Tanpa gambar')
            label.setToolTip(self.current[key])
        for key, button in self.colors.items():
            button.setText(self.current[key])
            button.setStyleSheet('border-left: 14px solid ' + self.current[key] + ';')
        self.preview.data = dict(self.current)
        self.preview.update()
        self.dirty = self.current != self.applied
        self.selectionChanged.emit()

    def set_value(self, key, value):
        data = dict(self.current)
        data[key] = value
        self.load(data)

    def pick_image(self, key):
        path, _ = QFileDialog.getOpenFileName(self, 'Pilih gambar splash', '', 'Gambar (*.png *.jpg *.jpeg *.webp *.svg)')
        if path:
            if not QImageReader(path).canRead():
                QMessageBox.warning(self, 'Gambar', 'Gambar tidak dapat dibaca.')
                return
            self.set_value(key, path)

    def pick_color(self, key):
        color = QColorDialog.getColor(QColor(self.current[key]), self, 'Pilih warna')
        if color.isValid():
            self.set_value(key, color.name())

    def discard(self):
        self.load(self.applied)

    def apply_selection(self):
        if not self.dirty:
            return None
        backup = self.backend.apply(self.current)
        self.applied = self.backend.read()
        self.load(self.applied)
        self.status.setText('Splash screen diterapkan. Akan terlihat saat login berikutnya. Backup: ' + str(backup))
        return backup

    def apply(self):
        try:
            self.apply_selection()
        except Exception as e:
            QMessageBox.critical(self, 'Splash Screen', str(e))

    def restore(self):
        backups = sorted(self.backend.backups.glob('[0-9]*/ksplashrc'), reverse=True)
        if not backups:
            QMessageBox.information(self, 'Splash Screen', 'Belum ada backup splash.')
            return
        if QMessageBox.question(self, 'Pulihkan splash', 'Pulihkan splash sebelum perubahan terakhir?') != QMessageBox.Yes:
            return
        try:
            self.backend.backup()
            self.backend.restore(backups[0].parent)
            self.applied = self.backend.read()
            self.load(self.applied)
            self.status.setText('Splash sebelumnya dipulihkan.')
        except Exception as e:
            QMessageBox.critical(self, 'Splash Screen', str(e))

    def open_preview(self):
        try:
            if self.preview_process and self.preview_process.poll() is None:
                self.preview_process.terminate()
            if self.preview_dir:
                self.preview_dir.cleanup()
            self.preview_dir = tempfile.TemporaryDirectory(prefix='aether-splash-preview-')
            package = Path(self.preview_dir.name) / self.backend.theme_id
            self.backend.build_package(package, self.current)
            self.preview_process = subprocess.Popen(
                ['ksplashqml', '--test', '--window', str(package)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            self.status.setText('Pratinjau splash dibuka dalam jendela. Tutup jendelanya untuk kembali.')
        except Exception as e:
            QMessageBox.critical(self, 'Pratinjau Splash', str(e))
