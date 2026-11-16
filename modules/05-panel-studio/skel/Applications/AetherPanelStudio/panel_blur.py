"""Set rounded X11 blur regions on the matching Plasma dock, without restarting KWin."""
import json,math,re,subprocess,sys,ctypes as C

def regions(boxes):
 out=[]
 for x,y,w,h,r in boxes:
  x,y,w,h,r=map(round,(x,y,w,h,r));r=min(r,w//2,h//2)
  for row in range(h):
   dy=max(r-row-.5,row-(h-r)+.5,0)
   inset=math.ceil(r-math.sqrt(max(0,r*r-dy*dy))) if dy else 0
   if w>2*inset:out.extend([x+inset,y+row,w-2*inset,1])
 return out

def main():
 width,height,boxes=json.loads(sys.argv[1]);values=regions(boxes)

 ids=re.findall(r'0x[0-9a-f]+',subprocess.check_output(['xprop','-root','_NET_CLIENT_LIST'],text=True))
 for wid in ids:
  props=subprocess.check_output(['xprop','-id',wid,'_NET_WM_WINDOW_TYPE','WM_CLASS'],text=True)
  if '_NET_WM_WINDOW_TYPE_DOCK' not in props or 'plasmashell' not in props.lower():continue
  geom=subprocess.check_output(['xwininfo','-id',wid],text=True)
  if not re.search(r'Width: '+str(round(width))+r'\b',geom) or not re.search(r'Height: '+str(round(height))+r'\b',geom):continue
  if values:
   lib=C.CDLL('libX11.so.6');lib.XOpenDisplay.restype=C.c_void_p
   lib.XInternAtom.argtypes=[C.c_void_p,C.c_char_p,C.c_int];lib.XInternAtom.restype=C.c_ulong
   lib.XChangeProperty.argtypes=[C.c_void_p,C.c_ulong,C.c_ulong,C.c_ulong,C.c_int,C.c_int,C.c_void_p,C.c_int]
   lib.XCloseDisplay.argtypes=[C.c_void_p]
   display=lib.XOpenDisplay(None)
   if not display:raise RuntimeError('X11 display unavailable')
   atom=lib.XInternAtom(display,b'_KDE_NET_WM_BLUR_BEHIND_REGION',0)
   data=(C.c_ulong*len(values))(*values)
   lib.XChangeProperty(display,int(wid,16),atom,6,32,0,C.cast(data,C.c_void_p),len(values))
   lib.XCloseDisplay(display)
if __name__=='__main__':main()
