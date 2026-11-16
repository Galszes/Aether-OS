"""KDE Plasma 5 / Aeos integration. All user files stay under the home directory."""
from pathlib import Path
import configparser
import datetime
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as E

DEFAULTS = dict(panelColor='#174568', panelOpacity=38, panelRadius=18, padding=8,
                splitPanel=1,
                borderColor='#6fa8dc', borderOpacity=27, gradient=10,
                shadowColor='#020a1c', shadowOpacity=33, shadowBlur=14, shadowOffset=3,
                popupColor='#174568', popupOpacity=48, highlightColor='#479cff',
                highlightOpacity=24, highlightRadius=10, taskShadow=18, tooltipRadius=14,
                blurStrength=15, windowOpacity=18, menuOpacity=25,
                windowBlur=1, popupBlur=1, dolphinGlass=1)
LIMITS = {'splitPanel':(0,1),'panelOpacity':(0,100),'panelRadius':(0,40),'padding':(2,16),
          'borderOpacity':(0,100),'gradient':(0,25),'shadowOpacity':(0,100),
          'shadowBlur':(0,32),'shadowOffset':(-8,12),'popupOpacity':(0,100),
          'highlightOpacity':(0,100),'highlightRadius':(0,18),'taskShadow':(0,60),
          'tooltipRadius':(0,18),'blurStrength':(1,15),
          'windowOpacity':(0,50),'menuOpacity':(0,50),
          'windowBlur':(0,1),'popupBlur':(0,1),'dolphinGlass':(0,1)}
CONFIG_KEYS = {'splitPanel':'splitPanel','panelColor':'backgroundColor','panelOpacity':'backgroundOpacity',
              'panelRadius':'cornerRadius','padding':'contentMargin','borderColor':'borderColor',
              'borderOpacity':'borderOpacity','gradient':'glassGradient','shadowColor':'shadowColor',
              'shadowOpacity':'shadowOpacity','shadowBlur':'shadowBlur','shadowOffset':'shadowOffset'}
WINDOW_KEYS={'windowOpacity','menuOpacity','windowBlur','popupBlur','dolphinGlass','blurStrength'}
PERCENT_KEYS={'panelOpacity','borderOpacity','gradient','shadowOpacity'}
PRESETS = {
 'Liquid Blue': DEFAULTS,
 'Crystal': dict(DEFAULTS, panelColor='#4482a5',panelOpacity=22,popupColor='#367494',popupOpacity=32,gradient=13,borderOpacity=35,shadowOpacity=24,windowOpacity=24,menuOpacity=30),
 'Ocean': dict(DEFAULTS, panelColor='#205e88',panelOpacity=44,popupColor='#205e88',popupOpacity=55,highlightColor='#65d1ff',windowOpacity=18,menuOpacity=25),
 'Midnight': dict(DEFAULTS, panelColor='#081b36',panelOpacity=65,popupColor='#081b36',popupOpacity=72,gradient=6,windowOpacity=12,menuOpacity=18),
}
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
def tag(name): return '{'+NS+'}'+name

def validate(settings):
    if not isinstance(settings,dict): raise ValueError('Format pengaturan harus berupa objek JSON.')
    out=dict(DEFAULTS)
    for key in DEFAULTS:
        if key not in settings:continue
        v=settings[key]
        if key.endswith('Color'):
            if not isinstance(v,str) or not re.fullmatch(r'#[a-fA-F0-9]{6}',v):raise ValueError('Warna tidak valid: '+key)
            out[key]=v.lower()
        else:
            if isinstance(v,bool) or not isinstance(v,(int,float)):raise ValueError('Angka tidak valid: '+key)
            lo,hi=LIMITS[key]
            if not lo <= v <= hi:raise ValueError(f'{key} harus antara {lo} dan {hi}.')
            out[key]=int(v)
    return out


def add_frame(root,prefix,color,opacity,radius,shadow=0,compact=False):
    # Symmetric nine-slice pieces keep the soft shadow and fill inside the frame.
    size=48; c=20
    bounds={'topleft':(0,0,c,c),'top':(c,0,8,c),'topright':(28,0,c,c),
            'left':(0,c,c,8),'center':(c,c,8,8),'right':(28,c,c,8),
            'bottomleft':(0,28,c,c),'bottom':(c,28,8,c),'bottomright':(28,28,c,c)}
    def shape(part,inset,r):
        # Top-left / top / left are mirrored to obtain the other six pieces.
        if 'right' in part: tx='translate(48,0) scale(-1,1)'
        else:tx=''
        if 'bottom' in part:tx+=' translate(0,48) scale(1,-1)'
        if part=='center':d='M20,20 H28 V28 H20 Z'
        elif part in ['top','bottom']:d=f'M20,{inset} H28 V20 H20 Z'
        elif part in ['left','right']:d=f'M{inset},20 H20 V28 H{inset} Z'
        else:
            q=inset+r
            if r:d=f'M{inset},20 V{q} A{r},{r} 0 0 1 {q},{inset} H20 V20 Z'
            else:d=f'M{inset},20 V{inset} H20 V20 Z'
        return d,tx.strip()
    for part,(x,y,w,h) in bounds.items():
        g=E.SubElement(root,tag('g'),{'id':prefix+'-'+part})
        E.SubElement(g,tag('rect'),dict(x=str(x),y=str(y),width=str(w),height=str(h),fill=color,opacity='0.00001'))
        # Tray highlight spans the whole expander cell. Give its visible disc
        # its own inset so it stays inside the rounded panel island.
        layers=([(6,max(0,radius-4),color,opacity)] if compact else
                [(0,radius+2,'#020a1c',shadow/100*.13),(1,radius+1,'#020a1c',shadow/100*.25),(2,radius,color,opacity)])
        for inset,r,fill,alpha in layers:
            d,tx=shape(part,inset,r)
            E.SubElement(g,tag('path'),dict(d=d,transform=tx,fill=fill,opacity=str(alpha)))
    for side in ['top','bottom','left','right']:
        E.SubElement(root,tag('rect'),{'id':prefix+'-hint-'+side+'-margin','width':'2','height':'2','fill':'#ff00ff'})


def update_frames(path,settings,tray=False):
    doc=E.parse(path);root=doc.getroot()
    if tray: states=[(p,1) for p in ['active-tab','north-active-tab','south-active-tab','east-active-tab','west-active-tab']]
    else: states=[(d+'-'+s,k) for d in ['north','south','east','west'] for s,k in [('focus',1),('hover',.67),('normal',.15),('minimized',.1)]]
    for parent in list(root.iter()):
        for child in list(parent):
            if any(child.get('id','').startswith(p+'-') for p,_ in states):parent.remove(child)
    for prefix,k in states:
        add_frame(root,prefix,settings['highlightColor'],settings['highlightOpacity']/100*k,
                  settings['highlightRadius'],settings['taskShadow'] if not tray and k>=.67 else 0,
                  compact=tray)
    doc.write(path,encoding='UTF-8',xml_declaration=True)

def write_tooltip(path,settings):
    # Tooltips need matching visible and blur-mask corners. Keep these distinct
    # from popup windows so Home retains its own frame and dimensions.
    root=E.Element(tag('svg'),{'width':'48','height':'48','viewBox':'0 0 48 48','version':'1.1'})
    add_frame(root,'surface',settings['popupColor'],settings['popupOpacity']/100,settings['tooltipRadius'])
    add_frame(root,'mask','#ffffff',1,settings['tooltipRadius'])
    for elem in root.iter():
        ident=elem.get('id','')
        if ident.startswith('surface-'):elem.set('id',ident[len('surface-'):])
        if '-hint-' in ident or ident.startswith('hint-'):
            side=ident.split('-')[-2]
            # Enough content inset to keep labels away from rounded corners.
            margin=max(8,round(settings['tooltipRadius']*.7))
            elem.set('width',str(margin if side in ['left','right'] else 2))
            elem.set('height',str(margin if side in ['top','bottom'] else 2))
    E.ElementTree(root).write(path,encoding='UTF-8',xml_declaration=True)


class Backend:
    def __init__(self,home=None):
        self.home=Path(home or Path.home())
        self.theme=self.home/'.local/share/plasma/desktoptheme/Aeos'
        self.widget=self.home/'.local/share/plasma/plasmoids/org.aether.panelislands'
        self.state=self.home/'.config/aether-panel-studio.json'
        self.backups=self.home/'theme-backups/AetherPanelStudio'
        self.config=self.home/'.config/plasma-org.kde.plasma.desktop-appletsrc'
        self.kvantum=self.home/'.config/Kvantum/AetherGlass/AetherGlass.kvconfig'
    def parser(self):
        p=configparser.ConfigParser(interpolation=None,strict=False);p.optionxform=str;p.read(self.config);return p
    def targets(self):
        return [s for s in self.parser().sections() if re.fullmatch(r'Containments\]\[\d+\]\[Applets\]\[\d+',s) and self.parser()[s].get('plugin')=='org.aether.panelislands']
    def read(self):
        s=dict(DEFAULTS)
        if self.kvantum.exists():
            try:
                kp=configparser.ConfigParser(interpolation=None,strict=False)
                kp.optionxform=str;kp.read(self.kvantum)
                if kp.has_section('%General'):
                    g=kp['%General']
                    if 'reduce_window_opacity' in g:
                        try:s['windowOpacity']=int(g['reduce_window_opacity'])
                        except ValueError:pass
                    if 'reduce_menu_opacity' in g:
                        try:s['menuOpacity']=int(g['reduce_menu_opacity'])
                        except ValueError:pass
                    if 'blurring' in g:
                        s['windowBlur']=1 if g['blurring'].lower()=='true' else 0
                    if 'popup_blurring' in g:
                        s['popupBlur']=1 if g['popup_blurring'].lower()=='true' else 0
                if kp.has_section('Hacks') and 'transparent_dolphin_view' in kp['Hacks']:
                    s['dolphinGlass']=1 if kp['Hacks']['transparent_dolphin_view'].lower()=='true' else 0
            except Exception:pass
        kwin_path=self.home/'.config/kwinrc'
        if kwin_path.exists():
            try:
                kwin=configparser.ConfigParser(interpolation=None);kwin.optionxform=str;kwin.read(kwin_path)
                if kwin.has_section('Effect-blur') and 'BlurStrength' in kwin['Effect-blur']:
                    try:s['blurStrength']=int(kwin['Effect-blur']['BlurStrength'])
                    except ValueError:pass
            except Exception:pass
        if self.state.exists():
            try:
                saved=json.loads(self.state.read_text())
                if isinstance(saved,dict):
                    for k in DEFAULTS:
                        if k in saved:
                            try:s[k]=validate({k:saved[k]})[k]
                            except Exception:pass
            except Exception:pass
        p=self.parser()
        for target in self.targets()[:1]:
            section=target+'][Configuration][General'
            if section not in p:continue
            for key,name in CONFIG_KEYS.items():
                if name in p[section]:
                    raw=p[section][name]
                    s[key]=raw if key.endswith('Color') else round(float(raw)*(100 if key in PERCENT_KEYS else 1))
        # The original widget ignored cornerRadius; its actual radius was 10 + padding.
        schema=self.widget/'contents/config/main.xml'
        if schema.exists() and 'glassGradient' not in schema.read_text():
            s['panelRadius']=10+s['padding']
            s['taskShadow']=0
        return validate(s)
    def run(self,*args):
        r=subprocess.run(args,text=True,capture_output=True,timeout=40)
        if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip() or 'Perintah gagal: '+args[0])
        return r.stdout
    def check(self):
        if not self.theme.is_dir() or not self.widget.is_dir():raise RuntimeError('Aplikasi ini membutuhkan tema Aeos dan widget Panel Islands yang sudah terpasang.')
        if not self.targets():raise RuntimeError('Widget Panel Islands tidak ditemukan pada panel aktif.')
        active=self.home/'.config/plasmarc'
        if active.exists() and 'name=Aeos' not in active.read_text():raise RuntimeError('Aktifkan tema Plasma Aeos sebelum menerapkan pengaturan.')
    def backup(self):
        self.check();self.backups.mkdir(parents=True,exist_ok=True)
        b=self.backups/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');b.mkdir()
        paths=[self.theme.relative_to(self.home),self.widget.relative_to(self.home),self.config.relative_to(self.home),self.state.relative_to(self.home)]
        try:
            if self.kvantum.exists():paths.append(self.kvantum.relative_to(self.home))
            svg=self.kvantum.with_suffix('.svg')
            if svg.exists():paths.append(svg.relative_to(self.home))
        except ValueError:pass
        manifest={}
        for rel in paths:
            src=self.home/rel;manifest[str(rel)]=src.exists()
            if src.exists():
                dst=b/rel;dst.parent.mkdir(parents=True,exist_ok=True)
                if src.is_dir():shutil.copytree(src,dst)
                else:shutil.copy2(src,dst)
        (b/'manifest.json').write_text(json.dumps(manifest,indent=2))
        kwin=configparser.ConfigParser(interpolation=None);kwin.optionxform=str
        kwin.read(self.home/'.config/kwinrc')
        (b/'blur-settings.json').write_text(json.dumps(dict(kwin['Effect-blur']) if kwin.has_section('Effect-blur') else {}))
        return b
    def snapshots(self):
        return sorted([p for p in self.backups.glob('*') if (p/'manifest.json').exists()],reverse=True)
    def _restore_files(self,b):
        b=Path(b).resolve()
        if b.parent!=self.backups.resolve():raise ValueError('Lokasi backup tidak valid.')
        manifest=json.loads((b/'manifest.json').read_text())
        allowed={str(p.relative_to(self.home)) for p in [self.theme,self.widget,self.config,self.state,self.kvantum,self.kvantum.with_suffix('.svg')]}
        if not set(manifest).issubset(allowed):raise ValueError('Manifest backup tidak valid.')
        for rel,exists in manifest.items():
            dst=self.home/rel;src=b/rel
            if dst.is_dir():shutil.rmtree(dst)
            elif dst.exists():dst.unlink()
            if exists:
                dst.parent.mkdir(parents=True,exist_ok=True)
                if src.is_dir():shutil.copytree(src,dst)
                else:shutil.copy2(src,dst)
    def restore_blur(self,b):
        saved=Path(b)/'blur-settings.json'
        if not saved.exists():return
        config=configparser.ConfigParser(interpolation=None);config.optionxform=str
        path=self.home/'.config/kwinrc';config.read(path)
        config.remove_section('Effect-blur')
        values=json.loads(saved.read_text())
        if values:config['Effect-blur']=values
        with path.open('w') as f:config.write(f,space_around_delimiters=False)
        self.configure_blur()
    def restore(self,b):
        # Preserve the current state too; every restore can itself be undone.
        self.backup()
        self.run('systemctl','--user','stop','plasma-plasmashell.service')
        try:self._restore_files(b);self.restore_blur(b)
        finally:self.run('systemctl','--user','start','plasma-plasmashell.service')
    def write_theme(self,s):
        # Change only visible background pieces. Mask and shadow remain untouched.
        for sub in ['', 'translucent/', 'solid/', 'opaque/']:
            for name in ['dialogs/background.svg','widgets/background.svg']:
                p=self.theme/(sub+name)
                if not p.exists():continue
                doc=E.parse(p)
                for elem in doc.iter():
                    style=elem.get('style','')
                    if 'fill:#174568' in style or 'fill:#081b36' in style or 'fill:#1f252f' in style or elem.get('data-studio-surface')=='true':
                        # Opaque masks describe geometry, not visible surfaces.
                        if 'opacity:0.48;' not in style and elem.get('data-studio-surface')!='true':continue
                        elem.set('data-studio-surface','true')
                        style=re.sub(r'(?<![\w-])fill:#[\da-fA-F]{6}', 'fill:'+s['popupColor'],style)
                        style=re.sub(r'(?<![\w-])opacity:[\d.]+','opacity:'+str(s['popupOpacity']/100),style)
                        elem.set('style',style)
                doc.write(p,encoding='UTF-8',xml_declaration=True)
        for sub in ['', 'translucent/', 'solid/', 'opaque/']:
            tooltip=self.theme/(sub+'widgets/tooltip.svg')
            if tooltip.exists():write_tooltip(tooltip,s)
        for name,tray in [('tasks.svg',False),('tabbar.svg',True)]:update_frames(self.theme/'widgets'/name,s,tray)
        p=self.theme/'metadata.desktop';text=p.read_text();text=re.sub(r'X-KDE-PluginInfo-Version=.*','X-KDE-PluginInfo-Version=21.4.'+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),text);p.write_text(text)
        for f in self.theme.rglob('*.svg'):E.parse(f)
    def write_kvantum(self,s):
        if not self.kvantum.exists():return
        kp=configparser.ConfigParser(interpolation=None,strict=False);kp.optionxform=str
        kp.read(self.kvantum)
        if not kp.has_section('%General'):kp.add_section('%General')
        kp['%General']['reduce_window_opacity']=str(s['windowOpacity'])
        kp['%General']['reduce_menu_opacity']=str(s['menuOpacity'])
        kp['%General']['blurring']='true' if s['windowBlur'] else 'false'
        kp['%General']['popup_blurring']='true' if s['popupBlur'] else 'false'
        kp['%General']['translucent_windows']='true'
        if not kp.has_section('Hacks'):kp.add_section('Hacks')
        kp['Hacks']['transparent_dolphin_view']='true' if s['dolphinGlass'] else 'false'
        kp['Hacks']['blur_translucent']='true' if s['windowBlur'] else 'false'
        if not kp.has_section('GeneralColors'):kp.add_section('GeneralColors')
        # Dolphin's transparent-view hack reveals the window surface; do not
        # add an independent fixed alpha to the file view palette.
        for key in ['base.color','inactive.base.color']:
            color=kp['GeneralColors'].get(key,'#181818')
            kp['GeneralColors'][key]=color[:7] if re.fullmatch(r'#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?',color) else '#181818'
        svg=self.kvantum.with_suffix('.svg')
        if svg.exists():
            text=svg.read_text()
            # Normalize this theme's two custom window surfaces only.
            def opaque_surface(match):
                rect=match.group(0)
                if 'fill-opacity=' in rect:rect=re.sub(r'fill-opacity="[^"]*"','fill-opacity="1"',rect)
                else:rect=rect.replace('/>',' fill-opacity="1"/>')
                return rect
            text=re.sub(r'<rect\b[^>]*\bid="aether-window-normal(?:-inactive)?"[^>]*/>',opaque_surface,text)
            svg.write_text(text)
        with self.kvantum.open('w') as f:kp.write(f,space_around_delimiters=False)
    def install_widget(self):
        data=Path(__file__).parent/'data'
        shutil.copy2(data/'main.qml',self.widget/'contents/ui/main.qml')
        shutil.copy2(data/'main.xml',self.widget/'contents/config/main.xml')
    def configure_blur(self):
        plugin=self.home/'.local/opt/aether-kvantum/usr/lib/x86_64-linux-gnu/qt5/plugins/kwin/effects/plugins/aether-compat-blur-v6.so'
        engine='aether-compat-blur' if plugin.exists() and not (self.home/'.config/aether-panel-studio-use-stock-blur').exists() else 'blur'
        if engine=='aether-compat-blur':
            self.run('kwriteconfig5','--file',str(self.home/'.config/kwinrc'),'--group','Plugins','--key','blurEnabled','false')
            self.run('kwriteconfig5','--file',str(self.home/'.config/kwinrc'),'--group','Plugins','--key','aether-compat-blurEnabled','true')
            self.run('qdbus','org.kde.KWin','/Effects','org.kde.kwin.Effects.unloadEffect','blur')
        loaded=(self.run('qdbus','org.kde.KWin','/Effects','org.kde.kwin.Effects.isEffectLoaded',engine) or '').strip()
        if loaded!='true':
            result=self.run('qdbus','org.kde.KWin','/Effects','org.kde.kwin.Effects.loadEffect',engine)
            if result is not None and result.strip()!='true':raise RuntimeError('KWin gagal memuat efek blur '+engine)
        self.run('qdbus','org.kde.KWin','/Effects','org.kde.kwin.Effects.reconfigureEffect',engine)
    def apply(self,settings):
        s=validate(settings);self.check()
        previous=self.read()
        restart=any(s[k]!=previous[k] for k in DEFAULTS if k not in WINDOW_KEYS)
        b=self.backup();stopped=False
        try:
            if restart:
                self.run('systemctl','--user','stop','plasma-plasmashell.service');stopped=True
                self.install_widget();self.write_theme(s)
                p=self.parser()
                targets=[section for section in p.sections() if p[section].get('plugin')=='org.aether.panelislands']
                for target in targets:
                    section=target+'][Configuration][General'
                    if not p.has_section(section):p.add_section(section)
                    for key,name in CONFIG_KEYS.items():p[section][name]=str(s[key]/100 if key in PERCENT_KEYS else s[key])
                with self.config.open('w') as f:p.write(f,space_around_delimiters=False)
            self.write_kvantum(s)
            self.state.write_text(json.dumps(s,indent=2))
            self.run('kwriteconfig5','--file',str(self.home/'.config/kwinrc'),'--group','Effect-blur','--key','BlurStrength',str(s['blurStrength']))
            self.configure_blur()
            # Palette and style notifications are distinct in KDE's Qt platform theme.
            for change in [2,0]:
                try:self.run('dbus-send','--type=signal','/KGlobalSettings','org.kde.KGlobalSettings.notifyChange','int32:'+str(change),'int32:0')
                except Exception:pass
            if stopped:
                self.run('systemctl','--user','start','plasma-plasmashell.service');stopped=False
        except Exception:
            if stopped:
                try:self._restore_files(b);self.restore_blur(b)
                finally:self.run('systemctl','--user','start','plasma-plasmashell.service')
            else:
                manifest=json.loads((b/'manifest.json').read_text())
                for dst in [self.kvantum,self.kvantum.with_suffix('.svg'),self.state]:
                    rel=str(dst.relative_to(self.home));src=b/rel
                    if manifest.get(rel) and src.exists():shutil.copy2(src,dst)
                    elif rel in manifest and not manifest[rel] and dst.exists():dst.unlink()
                self.restore_blur(b)
            raise
        return b
