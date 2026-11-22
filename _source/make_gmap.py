"""Темна карта офісів у стилі «кінематографічна мапа»: підкладка img/dg-geo-map.jpg + підписи й маршрути."""
K = {'kyiv': (547, 386), 'ist': (525, 745), 'ant': (586, 905)}
VB = (300, 250, 720, 720)
def q(a, b, bx, by):
    (x1, y1), (x2, y2) = K[a], K[b]
    return f'M{x1},{y1} Q{(x1+x2)/2+bx:.0f},{(y1+y2)/2+by:.0f} {x2},{y2}'
routes = [q('kyiv', 'ist', -70, 0), q('ist', 'ant', -40, 0)]
def city(k, name, dx, anchor):
    x, y = K[k]
    return (f'<circle class="gm__halo" cx="{x}" cy="{y}" r="14"/><circle class="gm__pin" cx="{x}" cy="{y}" r="5"/>'
            f'<text class="gm__city" x="{x+dx}" y="{y+4}" text-anchor="{anchor}">{name}</text>')
svg = (f'<svg class="gm__svg" viewBox="{" ".join(map(str, VB))}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Схема офісів Dictum: Київ, Стамбул, Анталія">'
       f'<image href="img/dg-geo-map.jpg" x="0" y="0" width="1024" height="1024"/>'
       f'<text class="gm__country" x="560" y="442">Україна</text>'
       f'<text class="gm__country gm__country--tr" x="745" y="815">Туреччина</text>'
       f'<text class="gm__sea" x="700" y="652">Чорне море</text>'
       + ''.join(f'<path class="gm__route-glow" d="{d}"/>' for d in routes)
       + ''.join(f'<path class="gm__route" d="{d}"/>' for d in routes)
       + city('kyiv', 'Київ', 14, 'start') + city('ist', 'Стамбул', -14, 'end') + city('ant', 'Анталія', 14, 'start')
       + '</svg>')
open('gmap.svg', 'w').write(svg); print(len(svg))
