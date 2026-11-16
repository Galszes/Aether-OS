#!/usr/bin/env python3
"""Build reference PDFs on the host; dependencies: python3-pyqt5, python3-markdown."""
import os,re,textwrap
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import markdown
from PyQt5.QtCore import QUrl, QSizeF
from PyQt5.QtGui import QTextDocument,QTextOption,QFont,QImage
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication
R=Path(__file__).resolve().parent.parent
app=QApplication([])
out=R/'docs/pdf';out.mkdir(exist_ok=True)
css='''body {font-family:"DejaVu Sans";font-size:9pt;color:#14283b;} h1{font-size:18pt;color:#134f7a;} h2{font-size:12pt;color:#134f7a;} h3{font-size:10pt;} pre{font-family:"DejaVu Sans Mono";font-size:7pt;background-color:#edf3f7;} code{font-family:"DejaVu Sans Mono";font-size:7pt;} table{border-collapse:collapse;width:100%;font-size:7.5pt;} th,td{border:1px solid #bacbd6;padding:4px;} th{background:#e3eef5;} p{margin-top:6px;margin-bottom:6px;}'''
def make(text,target):
 # Explicit shell continuations wrap long command lines in the printed reference.
 def wrap_code(m):
  lines=[]
  for line in m.group(2).splitlines():
   if len(line)>100 and line.startswith(('cp ','python3 ','kwriteconfig5 ')):
    chunks=textwrap.wrap(line,width=96,break_long_words=False,break_on_hyphens=False)
    lines.extend((s+' \\' if i<len(chunks)-1 else '    '+s) for i,s in enumerate(chunks))
   else:lines.append(line)
  return '```'+m.group(1)+'\n'+'\n'.join(lines)+'\n```'
 text=re.sub(r'```([^\n]*)\n(.*?)```',wrap_code,text,flags=re.S)
 html=markdown.markdown(text,extensions=['tables','fenced_code'])
 resources=[]
 def resolve_image(m):
  source=m.group(1);path=R/source
  if not path.exists():path=R/'docs'/source
  image=QImage(str(path))
  if image.isNull():raise RuntimeError('Screenshot missing: '+str(path))
  url=QUrl.fromLocalFile(str(path));resources.append((url,image))
  return '<img src="'+url.toString()+'" width="640" height="'+str(round(640*image.height()/image.width()))+'" />'
 html=re.sub(r'<img[^>]*src="([^"]+)"[^>]*>',resolve_image,html)
 doc=QTextDocument();doc.setDefaultFont(QFont('DejaVu Sans',9));doc.setDefaultStyleSheet(css)
 doc.setBaseUrl(QUrl.fromLocalFile(str(R)+'/'))
 opt=doc.defaultTextOption();opt.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere);doc.setDefaultTextOption(opt)
 for url,image in resources:doc.addResource(QTextDocument.ImageResource,url,image)
 doc.setHtml(html)
 printer=QPrinter(QPrinter.HighResolution);printer.setOutputFormat(QPrinter.PdfFormat);printer.setOutputFileName(str(target));printer.setPageSize(QPrinter.A4);printer.setPageMargins(14,14,14,14,QPrinter.Millimeter)
 doc.print_(printer)
 print(target.name,target.stat().st_size)
make((R/'docs/Panduan-Aether-Per-Sesi.md').read_text(),out/'Panduan-Aether-Per-Sesi.pdf')
shots={'04-panel-terpisah':'04-studio-panel.png','05-panel-studio':'03-studio-titlebar.png','06-wallpaper-branding':'01-studio-branding.png','07-splash':'02-studio-splash.png'}
for d in sorted((R/'modules').iterdir()):
 text=(d/'README.md').read_text()
 if d.name in shots:text+='\n\n![Antarmuka terkait](docs/screenshots/'+shots[d.name]+')\n'
 make(text,out/(d.name+'.pdf'))
