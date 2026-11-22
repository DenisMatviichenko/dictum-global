"""Світла точкова мапа регіону (img/dg-region.svg) + шар маршрутів (_source/region_map.svg, region_map.json)."""
import math, json, importlib.util, sys, io
spec = importlib.util.spec_from_file_location('mm', 'make_map.py'); mm = importlib.util.module_from_spec(spec)
_o = sys.stdout; sys.stdout = io.StringIO(); spec.loader.exec_module(mm); sys.stdout = _o
LON0, LON1, LAT0, LAT1 = 20.6, 46.2, 35.4, 53.2
C = math.cos(math.radians(44)); K = 30
W = (LON1 - LON0) * C * K; H = (LAT1 - LAT0) * K
P = lambda lon, lat: ((lon - LON0) * C * K, (LAT1 - lat) * K)
def inside(pt, poly):
    x, y = pt; c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
MED = [(19.5, 34.0)] + mm.MED[1:-1] + [(21.5, 37.0), (21.2, 37.8), (20.9, 38.6), (20.4, 39.4), (19.5, 39.8)]
water = [mm.BLACK, mm.AZOV, mm.MARMARA, MED, [(46.6, 47.0), (47.5, 47.0), (47.5, 40.0), (48.9, 38.0), (49.5, 38.0), (49.5, 47.5), (46.8, 47.4)]]
ua, tr = [mm.UA], [mm.TR_A, mm.TR_E]
land_extra = [mm.CYPRUS, mm.CRETE]
step = .2
grey, uad, trd = [], [], []
row = 0
lat = LAT1 - step / 2
while lat > LAT0:
    lon = LON0 + (step / 2 if row % 2 else step) / C * .5
    while lon < LON1:
        p = (lon, lat)
        if any(inside(p, h) for h in ua): uad.append(P(*p))
        elif any(inside(p, h) for h in tr): trd.append(P(*p))
        elif not any(inside(p, w) for w in water) or any(inside(p, l) for l in land_extra): grey.append(P(*p))
        lon += step / C
    lat -= step * .87; row += 1
d = lambda pts: ''.join(f'M{x:.0f} {y:.0f}h0' for x, y in pts)
r = step * K * .27
base = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}">'
        f'<g fill="none" stroke-linecap="round" stroke-width="{2*r:.1f}">'
        f'<path stroke="#D6DBCD" d="{d(grey)}"/><path stroke="#8FA63C" d="{d(uad)}"/><path stroke="#A9BE5A" d="{d(trd)}"/></g></svg>')
open('dg-region.svg', 'w').write(base)

CITIES = {'kyiv': (30.52, 50.45), 'ist': (28.98, 41.01), 'ant': (30.71, 36.90)}
cx = {k: P(*v) for k, v in CITIES.items()}
def arc(a, b, bend):
    (x1, y1), (x2, y2) = cx[a], cx[b]
    L = math.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    qx, qy = (x1 + x2) / 2 + nx * bend * L, (y1 + y2) / 2 + ny * bend * L
    return f'M{x1:.1f},{y1:.1f} Q{qx:.1f},{qy:.1f} {x2:.1f},{y2:.1f}'
routes = [arc('kyiv', 'ist', .22), arc('kyiv', 'ant', -.2), arc('ist', 'ant', .3)]
ua_l, tr_l, sea_l = P(34.8, 48.9), P(35.4, 38.7), P(36.2, 43.2)
over = (f'<svg class="geo__svg" viewBox="0 0 {W:.0f} {H:.0f}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Схема офісів Dictum: Київ, Стамбул, Анталія">'
        f'<text class="geo__country" x="{ua_l[0]:.0f}" y="{ua_l[1]:.0f}">Україна</text>'
        f'<text class="geo__country" x="{tr_l[0]:.0f}" y="{tr_l[1]:.0f}">Туреччина</text>'
        f'<text class="geo__sea" x="{sea_l[0]:.0f}" y="{sea_l[1]:.0f}">Чорне море</text>'
        + ''.join(f'<path class="geo__route-glow" d="{x}"/>' for x in routes)
        + ''.join(f'<path class="geo__route" d="{x}" style="animation-delay:{i*.6:.1f}s"/>' for i, x in enumerate(routes))
        + ''.join(f'<circle class="geo__halo" cx="{x:.1f}" cy="{y:.1f}" r="18" style="animation-delay:{i*.8:.1f}s"/><circle class="geo__pin" cx="{x:.1f}" cy="{y:.1f}" r="8"/><circle class="geo__pin-in" cx="{x:.1f}" cy="{y:.1f}" r="3.2"/>' for i, (x, y) in enumerate(cx.values()))
        + '</svg>')
open('region_map.svg', 'w').write(over)
pos = {k: (round(x / W * 100, 1), round(y / H * 100, 1)) for k, (x, y) in cx.items()}
json.dump({'W': round(W), 'H': round(H), 'pos': pos}, open('region_map.json', 'w'))
print(round(W), round(H), len(grey), len(uad), len(trd), len(base) // 1024, 'KB', pos)
