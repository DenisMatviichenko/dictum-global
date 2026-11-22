"""Світла точкова мапа офісів: підкладка img/dg-region.svg + шар маршрутів."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
g = open('generate.py', encoding='utf-8').read()
old = """    return (f'<div class="geo reveal" style="aspect-ratio:{GEO_META["W"]}/{GEO_META["H"]}">' + GEO_SVG"""
new = """    return (f'<div class="geo reveal"><div class="geo__map" style="aspect-ratio:{GEO_META["W"]}/{GEO_META["H"]}"><img class="geo__base" src="img/dg-region.svg" alt="" loading="lazy">' + GEO_SVG"""
if old in g:
    g = g.replace(old, new, 1)
    g = g.replace("""lbl('ant', 'Анталія', 'tr', 'right') + '</div>')""", """lbl('ant', 'Анталія', 'tr', 'right') + '</div></div>')""", 1)
    open('generate.py', 'w', encoding='utf-8').write(g)
print('geo2', 'geo__base' in g)
