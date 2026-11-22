"""Темна кінематографічна карта офісів замість світлої схеми."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
g = open('generate.py', encoding='utf-8').read()
if 'GMAP_SVG' not in g:
    g = g.replace('\ndef geo_html():', "\nGMAP_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gmap.svg'), encoding='utf-8').read()\ndef geo_html():\n    return '<div class=\"gm reveal\">' + GMAP_SVG + '</div>'\ndef geo_html_light():", 1)
    g = g.replace('<section class="section is-light geo-sec" id="global">', '<section class="section gm-sec" id="global">', 1)
    open('generate.py', 'w', encoding='utf-8').write(g)
print('gmap', 'GMAP_SVG' in g)
