#!/usr/bin/env python3
"""Aether Panel Studio — local desktop editor for Aeos on Plasma 5."""
import json
import sys
from pathlib import Path
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRectF, QPointF
from PyQt5.QtGui import QColor, QPainter, QLinearGradient, QFont, QIcon
from PyQt5.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,
    QLabel,QPushButton,QSlider,QTabWidget,QScrollArea,QFormLayout,QColorDialog,
    QFileDialog,QComboBox,QMessageBox,QInputDialog,QSplitter,QFrame)
from backend import Backend,DEFAULTS,PRESETS,LIMITS,validate

class Worker(QThread):
    done=pyqtSignal(object)
    failed=pyqtSignal(str)
    def __init__(self,fn):super().__init__();self.fn=fn
    def run(self):
        try:self.done.emit(self.fn())
        except Exception as e:self.failed.emit(str(e))

class Preview(QWidget):
    def __init__(self):
        super().__init__();self.s=dict(DEFAULTS);self.setMinimumHeight(320);self.setMinimumWidth(330)
    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);s=self.s
        w,h=self.width(),self.height()
        bg=QLinearGradient(0,0,w,h);bg.setColorAt(0,QColor('#0c2036'));bg.setColorAt(.5,QColor('#285e7b'));bg.setColorAt(1,QColor('#627d9a'));p.fillRect(self.rect(),bg)
        p.setPen(Qt.NoPen)
        for x,y,r,c in [(.15,.25,.22,'#467a8e'),(.8,.2,.2,'#3c658c'),(.3,.65,.28,'#2a8f82'),(.65,.75,.25,'#7a4d8c')]:
            p.setBrush(QColor(c));p.drawEllipse(QPointF(w*x,h*y),w*r,w*r)
        def glass(rect,base,alpha,radius,gradient=False):
            for spread in range(s['shadowBlur'],0,-2):
                c=QColor(s['shadowColor']);c.setAlphaF(s['shadowOpacity']/100*.035)
                p.setBrush(c);p.drawRoundedRect(rect.adjusted(-spread/2,-spread/2+s['shadowOffset'],spread/2,spread/2+s['shadowOffset']),radius+spread/2,radius+spread/2)
            c=QColor(base);c.setAlphaF(alpha)
            if gradient:
                g=QLinearGradient(rect.topLeft(),rect.bottomLeft());top=QColor(base).lighter(125);top.setAlphaF(min(1,alpha+s['gradient']/100));g.setColorAt(0,top);g.setColorAt(.5,c);c2=QColor(base);c2.setAlphaF(max(0,alpha-s['gradient']/160));g.setColorAt(1,c2);p.setBrush(g)
            else:p.setBrush(c)
            edge=QColor(s['borderColor']);edge.setAlphaF(s['borderOpacity']/100);p.setPen(edge);p.drawRoundedRect(rect,radius,radius);p.setPen(Qt.NoPen)
        # Translucent application window (Dolphin / Berkas)
        win_rect=QRectF(16,20,w*0.58,h-100)
        for sp in range(10,0,-2):
            sc=QColor('#000000');sc.setAlphaF(0.04)
            p.setBrush(sc);p.drawRoundedRect(win_rect.adjusted(-sp/2,-sp/2+3,sp/2,sp/2+3),9+sp/2,9+sp/2)
        win_alpha=max(0.4,1.0-(s['windowOpacity']/100*0.9))
        win_col=QColor('#1e242c');win_col.setAlphaF(win_alpha)
        p.setBrush(win_col);p.setPen(QColor(120,160,200,60));p.drawRoundedRect(win_rect,9,9);p.setPen(Qt.NoPen)
        tb_rect=QRectF(win_rect.left(),win_rect.top(),win_rect.width(),24)
        p.setBrush(QColor(25,32,42,int(255*min(1.0,win_alpha+0.15))));p.drawRoundedRect(tb_rect,9,9)
        p.fillRect(QRectF(win_rect.left(),win_rect.top()+14,win_rect.width(),10),QColor(25,32,42,int(255*min(1.0,win_alpha+0.15))))
        for i,col in enumerate(['#ff5f56','#ffbd2e','#27c93f']):
            p.setBrush(QColor(col));p.drawEllipse(QPointF(win_rect.left()+12+i*12,win_rect.top()+12),3.5,3.5)
        p.setPen(QColor('#9bbcd8'));p.setFont(QFont('Sans Serif',8))
        p.drawText(QRectF(win_rect.left()+52,win_rect.top()+2,win_rect.width()-58,20),Qt.AlignLeft|Qt.AlignVCenter,'Dolphin · Berkas')
        p.setPen(Qt.NoPen)
        view_rect=QRectF(win_rect.left()+8,win_rect.top()+30,win_rect.width()-16,win_rect.height()-38)
        view_alpha=0.22 if s['dolphinGlass'] else 0.88
        view_col=QColor('#181818' if not s['dolphinGlass'] else '#102235');view_col.setAlphaF(view_alpha)
        p.setBrush(view_col);p.drawRoundedRect(view_rect,6,6)
        side_w=max(48.0,(win_rect.width()-16)*0.36)
        p.setBrush(QColor(255,255,255,10));p.drawRoundedRect(QRectF(view_rect.left(),view_rect.top(),side_w,view_rect.height()),6,6)
        for fi,fname in enumerate(['Utama','Dokumen','Unduhan']):
            fy=view_rect.top()+14+fi*22
            p.setBrush(QColor('#5da5da'));p.drawEllipse(QPointF(view_rect.left()+10,fy),3.5,3.5)
            p.setPen(QColor('#b8d5ee'));p.setFont(QFont('Sans Serif',7))
            p.drawText(QRectF(view_rect.left()+18,fy-8,side_w-20,16),Qt.AlignVCenter,fname);p.setPen(Qt.NoPen)
        for ci in range(min(4,max(2,int((view_rect.height()-20)/45)*2))):
            cx=view_rect.left()+side_w+10+(ci%2)*((view_rect.width()-side_w-18)/2)
            cy=view_rect.top()+12+(ci//2)*44
            p.setBrush(QColor(60,130,200,45 if s['dolphinGlass'] else 80));p.drawRoundedRect(QRectF(cx,cy,28,22),4,4)
            p.setBrush(QColor('#78b9ec'));p.drawRect(QRectF(cx+3,cy+3,10,5))
        # Popup window (overlapping)
        popup=QRectF(w*0.42,32,w*0.54,h-134);glass(popup,s['popupColor'],s['popupOpacity']/100,10)
        p.setPen(QColor('#e5f1ff'));p.setFont(QFont('Sans Serif',10,QFont.Bold));p.drawText(QRectF(popup.left()+14,popup.top()+12,popup.width()-28,22),'Home · Menu');p.setPen(Qt.NoPen)
        p.setBrush(QColor(220,239,255,24));p.drawRoundedRect(QRectF(popup.left()+14,popup.top()+38,popup.width()-28,24),6,6)
        for i,label in enumerate(['Aplikasi','Audio','Jaringan','Setelan']):
            xx=popup.left()+12+(i%2)*(popup.width()-24)/2;yy=popup.top()+80+(i//2)*42
            p.setBrush(QColor('#73bbf3'));p.drawEllipse(QPointF(xx+8,yy),7,7)
            p.setPen(QColor('#e7f3ff'));p.setFont(QFont('Sans Serif',8));p.drawText(QRectF(xx+20,yy-9,(popup.width()-24)/2-18,18),label);p.setPen(Qt.NoPen)
        tip=QRectF(popup.left()+14,popup.bottom()-46,popup.width()-28,32)
        glass(tip,s['popupColor'],s['popupOpacity']/100,s['tooltipRadius'])
        p.setPen(QColor('#e5f1ff'));p.setFont(QFont('Sans Serif',8));p.drawText(tip,Qt.AlignCenter,'Tooltip hover');p.setPen(Qt.NoPen)
        # Panel at bottom
        panel=QRectF(16,h-62,w-32,46)
        if s['splitPanel']:
            left=QRectF(panel.left(),panel.top(),panel.width()*.60,panel.height())
            right=QRectF(panel.left()+panel.width()*.72,panel.top(),panel.width()*.28,panel.height())
            for island in (left,right):glass(island,s['panelColor'],s['panelOpacity']/100,min(s['panelRadius'],23),True)
        else:glass(panel,s['panelColor'],s['panelOpacity']/100,min(s['panelRadius'],23),True)
        for i in range(5):
            if s['splitPanel']:
                x=(left.left()+14+i*min(48.0,(left.width()-28)/3)) if i<3 else (right.left()+8+(i-3)*min(40.0,(right.width()-16)/2))
            else:x=panel.left()+14+i*min(48.0,(panel.width()-28)/5)
            if i==2:
                box=QRectF(x-4,panel.top()+3,32,40)
                for spread in range(5,0,-1):
                    col=QColor(s['shadowColor']);col.setAlphaF(s['taskShadow']/100*.13);p.setBrush(col);p.drawRoundedRect(box.adjusted(-spread/2,-spread/2,spread/2,spread/2),s['highlightRadius']+spread/2,s['highlightRadius']+spread/2)
                c=QColor(s['highlightColor']);c.setAlphaF(s['highlightOpacity']/100);p.setBrush(c);p.drawRoundedRect(box,s['highlightRadius'],s['highlightRadius'])
            p.setBrush(QColor(['#72b6ef','#b2d8ff','#7bc9ed','#b6b3f5','#e0ecf9'][i]));p.drawEllipse(QPointF(x+12,panel.center().y()),9,9)
        p.end()

FIELDS=[
 ('Panel',[('splitPanel','Panel terpisah adaptif','toggle'),('panelColor','Warna panel','color'),('panelOpacity','Opasitas panel','%'),('panelRadius','Sudut rounded','px'),('padding','Jarak isi ke tepi','px'),('gradient','Pantulan kaca','%'),('borderColor','Warna tepian','color'),('borderOpacity','Opasitas tepian','%')]),
 ('Shadow',[('shadowColor','Warna shadow panel','color'),('shadowOpacity','Kepekatan shadow panel','%'),('shadowBlur','Blur shadow panel','px'),('shadowOffset','Posisi vertikal shadow','px'),('taskShadow','Shadow highlight aplikasi','%')]),
 ('Ikon aplikasi',[('highlightColor','Warna highlight','color'),('highlightOpacity','Opasitas highlight','%'),('highlightRadius','Sudut highlight','px')]),
 ('Popup',[('popupColor','Warna popup','color'),('popupOpacity','Opasitas popup','%'),('tooltipRadius','Rounded tooltip (hover)','px')]),
 ('Jendela & Blur',[('blurStrength','Kekuatan blur (global)','/ 15'),('windowOpacity','Transparansi jendela (Kvantum)','%'),('menuOpacity','Transparansi menu & popup Qt','%'),('windowBlur','Efek blur jendela aplikasi','toggle'),('popupBlur','Efek blur menu & popup Qt','toggle'),('dolphinGlass','Frosted glass Dolphin view','toggle')])]

class Window(QMainWindow):
    def __init__(self):
        super().__init__();self.backend=Backend();self.worker=None;self.loading=False;self.dirty=False
        self.setWindowTitle('Aether Panel Studio');self.setWindowIcon(QIcon.fromTheme('preferences-desktop-theme'));self.resize(1080,760)
        try:self.s=self.backend.read()
        except Exception:self.s=dict(DEFAULTS)
        self.applied=dict(self.s);self.controls={};self.values={}
        root=QWidget();self.setCentralWidget(root);layout=QVBoxLayout(root);layout.setContentsMargins(24,22,24,18);layout.setSpacing(14)
        title=QLabel('Aether Panel Studio');title.setObjectName('title');layout.addWidget(title)
        sub=QLabel('Atur kaca, warna, bentuk, dan bayangan panel KDE-mu.');sub.setObjectName('muted');layout.addWidget(sub)
        top=QHBoxLayout();top.addWidget(QLabel('Preset'));self.presets=QComboBox();self.presets.addItems(['Pilih preset…']+list(PRESETS));self.presets.activated[str].connect(self.preset);top.addWidget(self.presets)
        for text,fn in [('Impor',self.import_settings),('Ekspor',self.export_settings),('Backup',self.backup),('Pulihkan…',self.restore),('Buka Dolphin baru',self.open_dolphin)]:
            b=QPushButton(text);b.clicked.connect(fn);top.addWidget(b)
        top.addStretch();layout.addLayout(top)
        split=QSplitter();layout.addWidget(split,1)
        left=QWidget();lv=QVBoxLayout(left);lv.setContentsMargins(0,0,12,0)
        self.preview=Preview();lv.addWidget(self.preview,1)
        hint=QLabel('Pratinjau ilustratif • backdrop desktop menentukan hasil akhir.\nTransparansi: 0% opasitas = bening, 100% = pekat.');hint.setWordWrap(True);hint.setObjectName('muted');lv.addWidget(hint);split.addWidget(left)
        self.tabs=QTabWidget();split.addWidget(self.tabs);split.setSizes([440,560])
        for label,fields in FIELDS:
            body=QWidget();form=QFormLayout(body);form.setContentsMargins(18,22,18,22);form.setVerticalSpacing(25)
            for key,text,unit in fields:
                if unit=='color':
                    control=QPushButton();control.clicked.connect(lambda checked=False,k=key:self.pick_color(k));self.controls[key]=control;form.addRow(text,control)
                elif unit=='toggle':
                    control=QPushButton();control.setCheckable(True);control.setCursor(Qt.PointingHandCursor)
                    control.clicked.connect(lambda checked,k=key:self.toggled(k,checked))
                    self.controls[key]=control;form.addRow(text,control)
                else:
                    row=QWidget();rh=QHBoxLayout(row);rh.setContentsMargins(0,0,0,0)
                    slider=QSlider(Qt.Horizontal);slider.setRange(*LIMITS[key]);slider.valueChanged.connect(lambda v,k=key:self.changed(k,v));self.controls[key]=slider
                    value=QLabel();value.setMinimumWidth(52);value.setAlignment(Qt.AlignRight|Qt.AlignVCenter);self.values[key]=(value,unit);rh.addWidget(slider,1);rh.addWidget(value);form.addRow(text,row)
            note=('Mode terpisah menggambar dua latar yang mengikuti lebar aplikasi dan tray; bagian kosong tetap bening. Mode nonaktif menggambar satu latar penuh.' if label=='Panel' else ('Rounded tooltip mengatur popup informasi saat pointer berhenti di tombol atau ikon aplikasi. Warna dan opasitas mengikuti popup.' if label=='Popup' else ('Shadow aplikasi mengikuti highlight ikon aktif dan hover.' if label=='Shadow' else ('0% = pekat; 50% = lebih transparan. Pengaturan diterapkan ke tema Kvantum AetherGlass. Dolphin yang sudah berjalan mungkin perlu dibuka sebagai proses baru. Blur memakai efek kompatibilitas Aether untuk KWin X11/VMSVGA. Slider mengatur blur di belakang panel, popup, dan jendela yang meminta blur. Transparansi jendela yang terbuka mungkin perlu dimuat ulang oleh aplikasinya.' if label=='Jendela & Blur' else ''))))
            if note:
                n=QLabel(note);n.setWordWrap(True);n.setObjectName('muted');form.addRow(n)
            scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setWidget(body);scroll.setFrameShape(QFrame.NoFrame);self.tabs.addTab(scroll,label)
        from titlebar import TitlebarTab
        self.titlebar_tab=TitlebarTab(self)
        titlebar_scroll=QScrollArea();titlebar_scroll.setWidgetResizable(True);titlebar_scroll.setWidget(self.titlebar_tab)
        self.tabs.addTab(titlebar_scroll,'Bilah judul')
        from branding import BrandingTab
        self.branding_tab=BrandingTab(self)
        branding_scroll=QScrollArea();branding_scroll.setWidgetResizable(True);branding_scroll.setWidget(self.branding_tab)
        self.tabs.addTab(branding_scroll,'Layar kunci & Logo')
        from splash import SplashTab
        self.splash_tab=SplashTab(self)
        splash_scroll=QScrollArea();splash_scroll.setWidgetResizable(True);splash_scroll.setWidget(self.splash_tab)
        self.tabs.addTab(splash_scroll,'Splash Screen')
        self.status=QLabel('Siap. Pengaturan desktop belum berubah.');self.status.setWordWrap(True);layout.addWidget(self.status)
        foot=QHBoxLayout();msg=QLabel('Backup otomatis saat Terapkan. Edit jendela/blur tidak memuat ulang desktop.');msg.setWordWrap(True);msg.setObjectName('muted');foot.addWidget(msg,1)
        self.reset=QPushButton('Batalkan edit');self.reset.clicked.connect(self.cancel_edits);foot.addWidget(self.reset)
        self.apply_btn=QPushButton('Terapkan');self.apply_btn.setObjectName('primary');self.apply_btn.clicked.connect(self.apply);foot.addWidget(self.apply_btn);layout.addLayout(foot)
        self.load(self.s,False)
        self.branding_tab.selectionChanged.connect(self.refresh)
        self.titlebar_tab.selectionChanged.connect(self.refresh)
        self.splash_tab.selectionChanged.connect(self.refresh)
        self.setStyleSheet('''QMainWindow,QWidget { background: #0c1929; color: #dceafa; font-size: 13px; }
QLabel#title { font-size: 27px; font-weight: 650; } QLabel#muted { color: #8fa9c1; font-size: 12px; }
QPushButton,QComboBox { background: #182e46; border: 1px solid #30506d; border-radius: 8px; padding: 9px 13px; }
QPushButton:hover { background: #244867; } QPushButton:disabled { color: #65788e; background: #122236; }
QPushButton#primary { background: #2479be; border-color: #4da9ed; font-weight: bold; }
QTabWidget::pane { border: 1px solid #284058; border-radius: 9px; } QTabBar::tab { background: #112339; padding: 11px 12px; }
QTabBar::tab:selected { background: #234b6b; color: #bce4ff; } QSlider::groove:horizontal { height: 5px; background: #294158; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #54a9e3; border-radius: 2px; } QSlider::handle:horizontal { background: #c0e8ff; width: 16px; margin: -6px 0; border-radius: 8px; }
QScrollBar:vertical { background: #102137; width: 8px; } QScrollBar::handle:vertical { background: #36536f; min-height: 30px; border-radius: 4px; }
''')
    def _update_toggle_btn(self,key,active):
        c=self.controls[key]
        c.setText('✓  Aktif' if active else '✕  Nonaktif')
        c.setStyleSheet(
            'QPushButton { background: #1c5f94; border: 1px solid #4da9ed; color: #ffffff; font-weight: bold; border-radius: 8px; padding: 8px 14px; }'
            if active else
            'QPushButton { background: #182433; border: 1px solid #2e4359; color: #7f97af; border-radius: 8px; padding: 8px 14px; }'
        )
    def toggled(self,key,checked):
        if self.loading:return
        self.s[key]=1 if checked else 0
        self._update_toggle_btn(key,checked)
        self.dirty=True;self.refresh()
    def load(self,s,dirty=True):
        self.loading=True;self.s=validate(s)
        for key,c in self.controls.items():
            if key.endswith('Color'):
                c.setText(self.s[key].upper());c.setStyleSheet('QPushButton { border-left: 14px solid '+self.s[key]+'; }')
            elif key in LIMITS and LIMITS[key]==(0,1):
                active=bool(self.s[key])
                c.setChecked(active);self._update_toggle_btn(key,active)
            else:c.setValue(self.s[key]);self.values[key][0].setText(str(self.s[key])+' '+self.values[key][1])
        self.loading=False;self.dirty=dirty;self.refresh()
        if not dirty:self.status.setText("Siap. Pengaturan sesuai desktop saat ini.")
    def refresh(self):
        pending=self.dirty or bool(self.branding_tab.selection) or self.titlebar_tab.dirty or self.splash_tab.dirty
        self.preview.s=self.s.copy();self.preview.update();self.apply_btn.setEnabled(pending and self.worker is None);self.reset.setEnabled(pending and self.worker is None)
        if pending:self.status.setText('Ada perubahan di pratinjau. Klik Terapkan untuk mengubah desktop.')
    def changed(self,key,value):
        if self.loading:return
        self.s[key]=value;self.values[key][0].setText(str(value)+' '+self.values[key][1]);self.dirty=True;self.refresh()
    def pick_color(self,key):
        c=QColorDialog.getColor(QColor(self.s[key]),self,'Pilih warna')
        if c.isValid():s=self.s.copy();s[key]=c.name();self.load(s)
    def preset(self,name):
        if name in PRESETS:self.load(dict(PRESETS[name]))
    def import_settings(self):
        path,_=QFileDialog.getOpenFileName(self,'Impor pengaturan','','JSON (*.json)')
        if path:
            try:self.load(validate(json.loads(Path(path).read_text())))
            except Exception as e:self.error(str(e))
    def export_settings(self):
        path,_=QFileDialog.getSaveFileName(self,'Ekspor pengaturan','aether-panel.json','JSON (*.json)')
        if path:
            try:Path(path).write_text(json.dumps(self.s,indent=2));self.status.setText('Preset diekspor ke '+path)
            except Exception as e:self.error(str(e))
    def error(self,text):
        self.status.setText('Gagal: '+text);QMessageBox.critical(self,'Aether Panel Studio',text)
    def work(self,fn,done):
        if self.worker:return
        self.centralWidget().setEnabled(False);self.status.setText('Sedang memproses…');self.worker=Worker(fn)
        def finish(result=None,error=None):
            w=self.worker;self.worker=None;self.centralWidget().setEnabled(True)
            if error:self.error(error)
            else:done(result)
            self.refresh();w.wait();w.deleteLater()
        self.worker.done.connect(lambda x:finish(x));self.worker.failed.connect(lambda e:finish(error=e));self.worker.start()
    def open_dolphin(self):
        import subprocess
        subprocess.Popen(['dolphin','--new-window','--style','kvantum'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    def cancel_edits(self):
        self.branding_tab.clear_selection();self.titlebar_tab.discard();self.splash_tab.discard();self.load(dict(self.applied),False)
    def apply(self):
        branding_backup=None
        titlebar_backup=None
        splash_backup=None
        if self.titlebar_tab.dirty:
            try:titlebar_backup=self.titlebar_tab.apply_selection()
            except Exception as e:self.error(str(e));return
        if self.branding_tab.selection:
            try:
                branding_selection=dict(self.branding_tab.selection)
                branding_backup=self.branding_tab.backend.apply(branding_selection)
                self.branding_tab.clear_selection()
                message=[]
                if 'homeLogo' in branding_selection:message.append('Logo Home, pojok launcher, dan System Information diterapkan. Buka ulang System Information untuk melihatnya.')
                if 'background' in branding_selection or 'lockLogo' in branding_selection:message.append('Layar kunci diterapkan; login SDDM sistem dipasang terpisah.')
                self.branding_tab.status.setText(' '.join(message)+' Backup: '+str(branding_backup))
            except Exception as e:self.error(str(e));return
        if self.splash_tab.dirty:
            try:splash_backup=self.splash_tab.apply_selection()
            except Exception as e:self.error(str(e));return
        if not self.dirty:
            if branding_backup or titlebar_backup or splash_backup:self.status.setText('Perubahan diterapkan. Backup bilah judul: '+str(titlebar_backup)+'; branding: '+str(branding_backup)+'; splash: '+str(splash_backup))
            return
        settings=self.s.copy()
        def done(b):
            self.applied=settings.copy();self.load(settings,False);self.status.setText('Diterapkan. Jika Dolphin lama belum berubah, buka proses baru lewat tombol Buka Dolphin baru. Backup: '+str(b)+('; logo / layar kunci: '+str(branding_backup) if branding_backup else '')+('; bilah judul: '+str(titlebar_backup) if titlebar_backup else '')+('; splash: '+str(splash_backup) if splash_backup else ''))
        self.work(lambda:self.backend.apply(settings),done)
    def backup(self):self.work(self.backend.backup,lambda p:self.status.setText('Backup tersimpan: '+str(p)))
    def restore(self):
        snapshots=self.backend.snapshots()
        if not snapshots:QMessageBox.information(self,'Pulihkan','Belum ada backup dari aplikasi ini.');return
        labels=[p.name for p in snapshots];choice,ok=QInputDialog.getItem(self,'Pulihkan backup','Pilih waktu backup:',labels,0,False)
        if not ok:return
        if QMessageBox.question(self,'Pulihkan backup','Pulihkan tema dan konfigurasi panel dari backup ini? Kondisi saat ini juga akan dicadangkan.')!=QMessageBox.Yes:return
        def done(_):self.applied=self.backend.read();self.load(self.applied,False);self.status.setText('Backup berhasil dipulihkan.')
        self.work(lambda:self.backend.restore(snapshots[labels.index(choice)]),done)
    def closeEvent(self,event):
        if self.worker:QMessageBox.information(self,'Tunggu','Tunggu proses selesai sebelum menutup aplikasi.');event.ignore();return
        if (self.dirty or bool(self.branding_tab.selection) or self.titlebar_tab.dirty or self.splash_tab.dirty) and QMessageBox.question(self,'Tutup aplikasi','Buang perubahan pratinjau yang belum diterapkan?')!=QMessageBox.Yes:event.ignore();return
        event.accept()

if __name__=='__main__':
    app=QApplication(sys.argv);app.setApplicationName('Aether Panel Studio');app.setDesktopFileName('aether-panel-studio')
    window=Window()
    if '--splash' in sys.argv:window.tabs.setCurrentIndex(window.tabs.count()-1)
    elif '--branding' in sys.argv:window.tabs.setCurrentIndex(window.tabs.count()-2)
    elif '--titlebar' in sys.argv:window.tabs.setCurrentIndex(window.tabs.count()-3)
    window.show();sys.exit(app.exec_())
