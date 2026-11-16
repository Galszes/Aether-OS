#!/usr/bin/env python3
"""Merge one explicit INI fragment; preserve target sections/keys not in it."""
import configparser,sys
from pathlib import Path
if len(sys.argv)!=3:raise SystemExit('Usage: merge-kconfig.py FRAGMENT TARGET')
def read(p):
 c=configparser.ConfigParser(interpolation=None,strict=False);c.optionxform=str;c.read(p);return c
source,target=map(Path,sys.argv[1:]);data=read(target);changes=read(source)
if not source.is_file():raise SystemExit('Fragment missing: '+str(source))
for section in changes.sections():
 if not data.has_section(section):data.add_section(section)
 for key,value in changes[section].items():data[section][key]=value
 target.parent.mkdir(parents=True,exist_ok=True)
with target.open('w') as f:data.write(f,space_around_delimiters=False)
print('Merged:',source,'->',target)
