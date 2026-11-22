"""Смуга з цифрами: точкова мапа регіону з правильною дугою Київ → Стамбул."""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
g = open('generate.py', encoding='utf-8').read()
if 'DOTS_SVG' not in g:
    g = re.sub(r'<div class="facts2__map" aria-hidden="true">.*?</svg></div>', '<div class="facts2__map" aria-hidden="true">{DOTS_SVG}</div>', g, count=1, flags=re.S)
    g = g.replace('\ndef geo_html():', "\nDOTS_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_dots.svg'), encoding='utf-8').read()\ndef geo_html():", 1)
    open('generate.py', 'w', encoding='utf-8').write(g)
print('dots ok', 'DOTS_SVG' in g)
