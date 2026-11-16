"""User-scoped Plasma 5 lock-screen, logout-screen, SDDM login-screen, and launcher appearance."""
from pathlib import Path
import configparser,datetime,json,os,shutil,subprocess,tempfile
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFileDialog,QMessageBox

def patch_user_delegate(qml_path,logo_source_expr):
    p=Path(qml_path)
    s=p.read_text()
    if 'source: wrapper.avatarPath' not in s:
        raise RuntimeError('Komponen gambar akun tidak dikenali: '+str(p))
    s=s.replace('source: wrapper.avatarPath',
                '// Aether centered lock-screen image\n            source: '+logo_source_expr,1)
    s=s.replace('fillMode: Image.PreserveAspectCrop','fillMode: Image.PreserveAspectFit',1)
    # A logo keeps its own alpha; the stock avatar circle crops it and
    # paints a disc and border behind it. Keep the image itself visible.
    circle_start=s.index('    // Draw a translucent background circle')
    image_start=s.index('    Item {\n        id: imageSource',circle_start)
    s=s[:circle_start]+s[image_start:]
    mask_start=s.index('    ShaderEffect {')
    label_start=s.index('    PlasmaComponents3.Label {',mask_start)
    s=s[:mask_start]+s[label_start:]
    p.write_text(s)

class Branding:
    theme_id='org.aether.lockstudio'
    sddm_theme_id='aether-sddm'
    def __init__(self,home=None):
        self.home=Path(home or Path.home())
        self.assets=self.home/'.local/share/aether-panel-studio/branding'
        self.package=self.home/'.local/share/plasma/look-and-feel'/self.theme_id
        self.sddm_package=self.home/'.local/share/aether-panel-studio/sddm-theme'/self.sddm_theme_id
        self.config=self.home/'.config/kscreenlockerrc'
        self.kdeglobals=self.home/'.config/kdeglobals'
        self.about_distro_config=self.home/'.config/kcm-about-distrorc'
        self.state=self.home/'.config/aether-panel-branding.json'
        self.backups=self.home/'theme-backups/AetherBranding'
        self.breeze=Path('/usr/share/plasma/look-and-feel/org.kde.breeze.desktop')
        self.sddm_base=Path('/usr/share/sddm/themes/kubuntu')
        if not self.sddm_base.exists():
            self.sddm_base=Path('/usr/share/sddm/themes/breeze')
        self.sddm_helper=Path(__file__).resolve().parent/'apply-sddm-branding.sh'
    def read_config(self):
        c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str;c.read(self.config);return c
    def active_lookandfeel_dir(self):
        pkg='Aeos'
        if self.kdeglobals.exists():
            c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str
            try:
                c.read(self.kdeglobals)
                if c.has_section('KDE') and 'LookAndFeelPackage' in c['KDE']:
                    pkg=c['KDE']['LookAndFeelPackage'].strip() or 'Aeos'
            except Exception:
                pass
        d=self.home/'.local/share/plasma/look-and-feel'/pkg
        if d.exists() and d.resolve()!=self.package.resolve():
            return d
        aeos=self.home/'.local/share/plasma/look-and-feel/Aeos'
        if aeos.exists() and aeos.resolve()!=self.package.resolve():
            return aeos
        return None
    def run(self,script):
        r=subprocess.run(['qdbus','org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript',script],text=True,capture_output=True,timeout=15)
        if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
        return r.stdout.strip()
    def read(self):
        if self.state.exists():return json.loads(self.state.read_text())
        return {}
    def backup(self):
        self.backups.mkdir(parents=True,exist_ok=True);b=self.backups/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');b.mkdir()
        c=self.read_config();old={}
        for section,key in [('Greeter','Theme'),('Greeter','WallpaperPlugin'),('Greeter][Wallpaper][org.kde.image][General','Image')]:old[section+'|'+key]=c.get(section,key,fallback=None)
        icons=self.run('var r=[]; panels().forEach(function(p){p.widgets().forEach(function(w){if(w.type==="org.kde.plasma.kickoff"){w.currentConfigGroup=["General"];r.push({id:w.id,icon:w.readConfig("icon","start-here-kde")});}});});print(JSON.stringify(r));')
        lnf=self.active_lookandfeel_dir()
        lnf_info=None
        if lnf:
            lnf_info={'path':str(lnf),'has_logout':(lnf/'contents/logout').exists(),'has_components':(lnf/'contents/components').exists()}
            if lnf_info['has_logout']:shutil.copytree(lnf/'contents/logout',b/'lnf_logout')
            if lnf_info['has_components']:shutil.copytree(lnf/'contents/components',b/'lnf_components')
        (b/'before.json').write_text(json.dumps({'config':old,'icons':json.loads(icons or '[]'),'state':self.read(),'state_exists':self.state.exists(),'lnf':lnf_info,'about_distro_existed':self.about_distro_config.exists()},indent=2))
        if self.about_distro_config.exists():shutil.copy2(self.about_distro_config,b/'kcm-about-distrorc')
        for name,src in [('assets',self.assets),('package',self.package),('sddm_package',self.sddm_package)]:
            if src.exists():shutil.copytree(src,b/name)
        return b
    def build_package(self,destination,logo):
        d=Path(destination)
        if d.exists():shutil.rmtree(d)
        (d/'contents').mkdir(parents=True)
        for name in ['lockscreen','logout','components','osd']:
            src=self.breeze/'contents'/name
            if src.exists():shutil.copytree(src,d/'contents'/name)
        (d/'metadata.json').write_text(json.dumps({'KPlugin':{'Id':self.theme_id,'Name':'Aether Lock Studio','License':'GPL-2.0-or-later','Version':'1.0','ServiceTypes':['Plasma/LookAndFeel']},'X-Plasma-APIVersion':'2','X-Plasma-MainScript':'defaults'}))
        (d/'contents/defaults').write_text('')
        if logo:
            patch_user_delegate(d/'contents/components/UserDelegate.qml',json.dumps(Path(logo).resolve().as_uri()))
    def sync_logout_theme(self,logo):
        lnf=self.active_lookandfeel_dir()
        if not lnf:return
        contents=lnf/'contents'
        contents.mkdir(parents=True,exist_ok=True)
        for name in ['logout','components']:
            dst=contents/name
            if dst.exists():shutil.rmtree(dst)
            src=self.breeze/'contents'/name
            if src.exists():shutil.copytree(src,dst)
        if logo and (contents/'components/UserDelegate.qml').exists():
            patch_user_delegate(contents/'components/UserDelegate.qml',json.dumps(Path(logo).resolve().as_uri()))
    def build_sddm_theme(self,destination,background=None,logo=None):
        if not self.sddm_base.exists():return None
        d=Path(destination)
        if d.exists():shutil.rmtree(d)
        d.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(self.sddm_base,d)
        bg_rel=None
        if background and Path(background).is_file():
            bg_name='background'+Path(background).suffix.lower()
            shutil.copy2(background,d/bg_name)
            bg_rel=bg_name
        logo_rel=None
        if logo and Path(logo).is_file():
            logo_name='lockLogo'+Path(logo).suffix.lower()
            shutil.copy2(logo,d/logo_name)
            logo_rel=logo_name
        tc=configparser.ConfigParser(interpolation=None,strict=False);tc.optionxform=str
        conf_path=d/'theme.conf'
        if conf_path.exists():tc.read(conf_path)
        if not tc.has_section('General'):tc.add_section('General')
        tc['General']['type']='image'
        if bg_rel:
            tc['General']['background']=bg_rel
        with conf_path.open('w') as f:tc.write(f,space_around_delimiters=False)
        user_conf=d/'theme.conf.user'
        uc=configparser.ConfigParser(interpolation=None,strict=False);uc.optionxform=str
        uc.add_section('General')
        uc['General']['type']='image'
        if bg_rel:
            uc['General']['background']=bg_rel
        with user_conf.open('w') as f:uc.write(f,space_around_delimiters=False)
        if logo_rel and (d/'components/UserDelegate.qml').exists():
            patch_user_delegate(d/'components/UserDelegate.qml','Qt.resolvedUrl('+json.dumps('../'+logo_rel)+')')
        return d
    def install_system_sddm(self):
        state=self.read()
        if not self.sddm_package.exists():
            self.build_sddm_theme(self.sddm_package,state.get('background'),state.get('lockLogo'))
        if not self.sddm_package.exists():
            raise RuntimeError('Tema SDDM lokal belum tersedia.')
        r=subprocess.run(['pkexec',str(self.sddm_helper),'install',str(self.sddm_package)],text=True,capture_output=True,timeout=120)
        if r.returncode:
            raise RuntimeError(r.stderr.strip() or r.stdout.strip() or 'Gagal memasang tema SDDM dengan pkexec.')
        return r.stdout.strip()
    def apply(self,selection,install_sddm=False):
        if not selection:raise ValueError('Pilih minimal satu gambar terlebih dahulu.')
        for path in selection.values():
            if not Path(path).is_file():raise ValueError('Gambar tidak ditemukan: '+path)
            if QPixmap(path).isNull():raise ValueError('Gambar tidak dapat dibaca: '+path)
        b=self.backup()
        try:
            self.assets.mkdir(parents=True,exist_ok=True);state=self.read()
            for key,src in selection.items():
                dst=self.assets/(key+Path(src).suffix.lower())
                if Path(src).resolve()!=dst.resolve():shutil.copy2(src,dst)
                state[key]=str(dst)
            c=self.read_config()
            if 'background' in selection:
                if not c.has_section('Greeter'):c.add_section('Greeter')
                c['Greeter']['WallpaperPlugin']='org.kde.image'
                sec='Greeter][Wallpaper][org.kde.image][General'
                if not c.has_section(sec):c.add_section(sec)
                c[sec]['Image']=Path(state['background']).as_uri()
            if 'lockLogo' in selection:
                self.build_package(self.package,state['lockLogo'])
                self.sync_logout_theme(state['lockLogo'])
                if not c.has_section('Greeter'):c.add_section('Greeter')
                c['Greeter']['Theme']=self.theme_id
            if 'background' in selection or 'lockLogo' in selection:
                self.config.parent.mkdir(parents=True,exist_ok=True)
                with self.config.open('w') as f:c.write(f,space_around_delimiters=False)
                self.build_sddm_theme(self.sddm_package,state.get('background'),state.get('lockLogo'))
            if 'homeLogo' in selection:
                script='var count=0; panels().forEach(function(p){p.widgets().forEach(function(w){if(w.type==="org.kde.plasma.kickoff"){w.currentConfigGroup=["General"];w.writeConfig("icon",ICON);w.reloadConfig();count++;}});});print(count);'.replace('ICON',json.dumps(state['homeLogo']))
                if self.run(script)=='0':raise RuntimeError('Menu Kickoff/Home tidak ditemukan.')
                about=configparser.ConfigParser(interpolation=None,strict=False);about.optionxform=str
                about.read(self.about_distro_config)
                if not about.has_section('General'):about.add_section('General')
                about['General']['LogoPath']=state['homeLogo']
                self.about_distro_config.parent.mkdir(parents=True,exist_ok=True)
                with self.about_distro_config.open('w') as f:about.write(f,space_around_delimiters=False)
            self.state.write_text(json.dumps(state,indent=2))
            if install_sddm and ('background' in selection or 'lockLogo' in selection):
                self.install_system_sddm()
            return b
        except Exception:
            self.restore(b);raise
    def restore(self,b):
        b=Path(b).resolve()
        if b.parent!=self.backups.resolve():raise ValueError('Backup tidak valid.')
        before=json.loads((b/'before.json').read_text());c=self.read_config()
        for pair,value in before['config'].items():
            section,key=pair.split('|',1)
            if value is None:
                if c.has_section(section):c.remove_option(section,key)
            else:
                if not c.has_section(section):c.add_section(section)
                c[section][key]=value
        self.config.parent.mkdir(parents=True,exist_ok=True)
        with self.config.open('w') as f:c.write(f,space_around_delimiters=False)
        for name,dst in [('assets',self.assets),('package',self.package),('sddm_package',self.sddm_package)]:
            if dst.exists():shutil.rmtree(dst)
            if (b/name).exists():shutil.copytree(b/name,dst)
        lnf_info=before.get('lnf')
        if lnf_info and lnf_info.get('path'):
            lnf=Path(lnf_info['path'])
            if lnf.exists():
                for part,bname,had in [('logout','lnf_logout',lnf_info.get('has_logout')),('components','lnf_components',lnf_info.get('has_components'))]:
                    dst=lnf/'contents'/part
                    if dst.exists():shutil.rmtree(dst)
                    if had and (b/bname).exists():shutil.copytree(b/bname,dst)
        if before['state_exists']:self.state.write_text(json.dumps(before['state'],indent=2))
        elif self.state.exists():self.state.unlink()
        if 'about_distro_existed' in before:
            if before['about_distro_existed']:shutil.copy2(b/'kcm-about-distrorc',self.about_distro_config)
            elif self.about_distro_config.exists():self.about_distro_config.unlink()
        self.run('var old=ICONS; panels().forEach(function(p){p.widgets().forEach(function(w){old.forEach(function(x){if(w.id===x.id){w.currentConfigGroup=["General"];w.writeConfig("icon",x.icon);w.reloadConfig();}});});});'.replace('ICONS',json.dumps(before['icons'])))

class BrandingTab(QWidget):
    selectionChanged=pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent);self.backend=Branding();self.selection={};self.preview_process=None;self.preview_dir=None;self.labels={}
        v=QVBoxLayout(self);v.setContentsMargins(18,18,18,18)
        title=QLabel('Layar kunci, Logout, Login SDDM & Logo');title.setStyleSheet('font-size:20px;font-weight:bold');v.addWidget(title)
        note=QLabel('Mengatur secara sinkron:\n• Layar Kunci (Meta+L): Background + Logo tengah (tanpa lingkaran)\n• Layar Konfirmasi Logout: Logo tengah (tanpa lingkaran) di atas latar gelap transparan\n• Layar Login SDDM (saat boot / setelah Logout): Background + Logo tengah (tanpa lingkaran)\n• Logo Home: ikon panel, pojok kiri atas launcher, dan System Information');note.setWordWrap(True);v.addWidget(note)
        for key,label in [('background','Background (Lock Screen & Login SDDM)'),('lockLogo','Logo tengah (Lock Screen, Logout & Login SDDM)'),('homeLogo','Logo Home, Launcher & System Information')]:
            row=QHBoxLayout();row.addWidget(QLabel(label),1);button=QPushButton('Pilih gambar…');button.clicked.connect(lambda checked=False,k=key:self.pick(k));row.addWidget(button);v.addLayout(row)
            preview=QLabel('Belum dipilih');preview.setAlignment(Qt.AlignCenter);preview.setMinimumHeight(60);preview.setMaximumHeight(110);v.addWidget(preview);self.labels[key]=preview
        row1=QHBoxLayout()
        for label,fn in [('Pratinjau Lock Screen',self.preview),('Pratinjau Logout',self.preview_logout),('Pratinjau Login SDDM',self.preview_sddm)]:
            button=QPushButton(label);button.clicked.connect(fn);row1.addWidget(button)
        v.addLayout(row1)
        row2=QHBoxLayout()
        for label,fn in [('Terapkan branding',self.apply),('Pasang ke Login SDDM (Admin)',self.apply_sddm),('Pulihkan terakhir',self.restore)]:
            button=QPushButton(label);button.clicked.connect(fn);row2.addWidget(button)
        v.addLayout(row2)
        self.status=QLabel('Pratinjau memakai mode uji tanpa mengunci/mengeluarkan sesi.');self.status.setWordWrap(True);v.addWidget(self.status);v.addStretch()
        lock=QPushButton('Kunci layar sekarang (Meta+L)');lock.clicked.connect(self.lock_screen);v.insertWidget(v.count()-1,lock)
        self.show_images()
    def show_images(self):
        state=dict(self.backend.read());state.update(self.selection)
        for key,label in self.labels.items():
            path=state.get(key)
            if not path:label.clear();label.setText('Belum dipilih');label.setToolTip('')
            if path:
                pix=QPixmap(path)
                if not pix.isNull():label.setPixmap(pix.scaled(300,96,Qt.KeepAspectRatio,Qt.SmoothTransformation));label.setToolTip(path)
    def pick(self,key):
        path,_=QFileDialog.getOpenFileName(self,'Pilih gambar','','Gambar (*.png *.jpg *.jpeg *.webp *.svg)')
        if path:
            if QPixmap(path).isNull():QMessageBox.warning(self,'Gambar','Format tidak bisa dibaca.');return
            self.selection[key]=path;self.show_images();self.status.setText('Pilihan belum diterapkan. Klik Terapkan atau Terapkan branding.');self.selectionChanged.emit()
    def clear_selection(self):
        self.selection={};self.show_images();self.selectionChanged.emit()
    def lock_screen(self):
        if self.selection:
            QMessageBox.information(self,'Belum diterapkan','Terapkan pilihan gambar terlebih dahulu.');return
        try:
            subprocess.run(['qdbus','org.freedesktop.ScreenSaver','/ScreenSaver','org.freedesktop.ScreenSaver.Lock'],check=True,text=True,capture_output=True,timeout=15)
        except Exception as e:QMessageBox.critical(self,'Kunci layar',str(e))
    def apply(self):
        try:
            need_sddm=('background' in self.selection or 'lockLogo' in self.selection)
            home_logo='homeLogo' in self.selection
            b=self.backend.apply(self.selection);self.clear_selection()
            msg=('Diterapkan ke Lock Screen, Logout Screen, dan paket tema SDDM lokal. ' if need_sddm else '')
            if home_logo:msg+='Logo Home, pojok launcher, dan System Information diperbarui. Buka ulang System Information untuk melihatnya. '
            msg+='Backup: '+str(b)
            if need_sddm:
                if QMessageBox.question(self,'Login SDDM','Pasang juga perubahan ini ke layar Login SDDM sistem sekarang? (Memerlukan password Admin)')==QMessageBox.Yes:
                    self.backend.install_system_sddm()
                    msg='Diterapkan ke Lock Screen, Logout Screen, dan Login SDDM sistem! Backup: '+str(b)
            self.status.setText(msg)
        except Exception as e:QMessageBox.critical(self,'Branding',str(e))
    def apply_sddm(self):
        try:
            if self.selection:
                self.backend.apply(self.selection);self.clear_selection()
            self.backend.install_system_sddm()
            self.status.setText('Tema Login SDDM sistem (/usr/share/sddm/themes/aether-sddm) berhasil dipasang dan diaktifkan.')
        except Exception as e:QMessageBox.critical(self,'Login SDDM',str(e))
    def restore(self):
        backups=sorted(self.backend.backups.glob('*/before.json'),reverse=True)
        if not backups:QMessageBox.information(self,'Backup','Belum ada backup branding.');return
        if QMessageBox.question(self,'Pulihkan','Pulihkan perubahan branding terakhir?')!=QMessageBox.Yes:return
        try:self.backend.restore(backups[0].parent);self.clear_selection();self.status.setText('Branding sebelumnya dipulihkan.')
        except Exception as e:QMessageBox.critical(self,'Branding',str(e))
    def _stop_preview(self):
        if self.preview_process and self.preview_process.poll() is None:
            self.preview_process.terminate()
            try:self.preview_process.wait(timeout=5)
            except Exception:pass
    def preview(self):
        try:
            self._stop_preview()
            self.preview_dir=tempfile.TemporaryDirectory(prefix='aether-lock-preview-')
            root=Path(self.preview_dir.name);state=self.backend.read();state.update(self.selection)
            package=root/'package';self.backend.build_package(package,state.get('lockLogo'))
            config=root/'config';config.mkdir();c=self.backend.read_config()
            if state.get('background'):
                sec='Greeter][Wallpaper][org.kde.image][General'
                if not c.has_section(sec):c.add_section(sec)
                c[sec]['Image']=Path(state['background']).resolve().as_uri()
                if not c.has_section('Greeter'):c.add_section('Greeter')
                c['Greeter']['WallpaperPlugin']='org.kde.image'
            with (config/'kscreenlockerrc').open('w') as f:c.write(f,space_around_delimiters=False)
            env=dict(os.environ);env['XDG_CONFIG_HOME']=str(config)
            self.preview_process=subprocess.Popen(['/usr/lib/x86_64-linux-gnu/libexec/kscreenlocker_greet','--testing','--theme',str(package)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.status.setText('Pratinjau Lock Screen terbuka. Tutup jendela pratinjau untuk kembali.')
        except Exception as e:QMessageBox.critical(self,'Pratinjau Lock Screen',str(e))
    def preview_logout(self):
        try:
            self._stop_preview()
            self.preview_dir=tempfile.TemporaryDirectory(prefix='aether-logout-preview-')
            root=Path(self.preview_dir.name);state=self.backend.read();state.update(self.selection)
            data_dir=root/'data';pkg=data_dir/'plasma/look-and-feel'/self.backend.theme_id
            self.backend.build_package(pkg,state.get('lockLogo'))
            env=dict(os.environ)
            env['XDG_DATA_HOME']=str(data_dir)
            self.preview_process=subprocess.Popen(['/usr/lib/x86_64-linux-gnu/libexec/ksmserver-logout-greeter','--windowed','--lookandfeel',self.backend.theme_id],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.status.setText('Pratinjau Logout Screen terbuka (mode jendela). Klik Cancel atau tekan Esc untuk menutup.')
        except Exception as e:QMessageBox.critical(self,'Pratinjau Logout',str(e))
    def preview_sddm(self):
        try:
            self._stop_preview()
            self.preview_dir=tempfile.TemporaryDirectory(prefix='aether-sddm-preview-')
            root=Path(self.preview_dir.name);state=self.backend.read();state.update(self.selection)
            theme_dir=root/'aether-sddm'
            self.backend.build_sddm_theme(theme_dir,state.get('background'),state.get('lockLogo'))
            self.preview_process=subprocess.Popen(['sddm-greeter','--test-mode','--theme',str(theme_dir)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.status.setText('Pratinjau Login SDDM terbuka. Tutup jendela pratinjau untuk kembali.')
        except Exception as e:QMessageBox.critical(self,'Pratinjau SDDM',str(e))
