"""Замінює нічну мапу на світлу схему офісів (region_map.svg)."""
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
g = open('generate.py', encoding='utf-8').read()
if 'GEO_SVG' not in g:
    s = g.index('<div class="frame map reveal">')
    e = g.index('<div class="stack reveal" data-d="1">', s)
    g = g[:s] + '{geo_html()}\n    ' + g[e:]
    g = g.replace('<section class="section bg-2 bt" id="global">', '<section class="section is-light geo-sec" id="global">', 1)
    helper = '''
GEO_SVG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_map.svg'), encoding='utf-8').read()
GEO_META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'region_map.json'), encoding='utf-8'))
def geo_html():
    p = GEO_META['pos']
    lbl = lambda k, name, fl, side: f'<span class="geo__label geo__label--{side}" style="left:{p[k][0]}%;top:{p[k][1]}%">{flag(fl, 16)}{name}</span>'
    return (f'<div class="geo reveal" style="aspect-ratio:{GEO_META["W"]}/{GEO_META["H"]}">' + GEO_SVG
            + lbl('kyiv', 'Київ', 'ua', 'right') + lbl('ist', 'Стамбул', 'tr', 'left') + lbl('ant', 'Анталія', 'tr', 'right') + '</div>')

def page_home():'''
    g = g.replace('\ndef page_home():', helper, 1)
    if '\nimport os' not in g and 'import os' not in g.split('\n\n')[0]:
        g = 'import os, json\n' + g
    open('generate.py', 'w', encoding='utf-8').write(g)
i = open('i18n.py', encoding='utf-8').read()
if "'Чорне море'" not in i:
    i = i.replace('# --- theme v2\n', '''# --- theme v2
'Чорне море': ('Black Sea', 'Karadeniz', 'Чёрное море'),
'Схема офісів Dictum: Київ, Стамбул, Анталія': ('Dictum offices: Kyiv, Istanbul, Antalya', 'Dictum ofisleri: Kyiv, İstanbul, Antalya', 'Схема офисов Dictum: Киев, Стамбул, Анталия'),
''', 1)
    open('i18n.py', 'w', encoding='utf-8').write(i)
print('geo ok')
