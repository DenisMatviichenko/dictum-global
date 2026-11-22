"""Точкова мапа регіону для смуги з цифрами: сірі точки суші, оливкові — Україна й Туреччина, дуга Київ → Стамбул."""
import math, importlib.util
spec = importlib.util.spec_from_file_location('mm', 'make_map.py'); mm = importlib.util.module_from_spec(spec)
import sys, io; _o = sys.stdout; sys.stdout = io.StringIO(); spec.loader.exec_module(mm); sys.stdout = _o
LON0, LON1, LAT0, LAT1 = 24.2, 44.6, 35.9, 52.6
C = math.cos(math.radians(44)); K = 20
W = (LON1 - LON0) * C * K; H = (LAT1 - LAT0) * K
P = lambda lon, lat: ((lon - LON0) * C * K, (LAT1 - lat) * K)
def inside(pt, poly):
    x, y = pt; c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
water = [mm.BLACK, mm.AZOV, mm.MARMARA, mm.MED]
home = [mm.UA, mm.TR_A, mm.TR_E]
step = .42
grey, olive = [], []
lat = LAT1 - step / 2
while lat > LAT0:
    lon = LON0 + step / 2
    while lon < LON1:
        p = (lon, lat)
        if any(inside(p, h) for h in home): olive.append(P(*p))
        elif not any(inside(p, w) for w in water): grey.append(P(*p))
        lon += step / C * .72
    lat -= step
d = lambda pts: ''.join(f'M{x:.1f} {y:.1f}h0' for x, y in pts)
(kx, ky), (ix, iy) = P(30.52, 50.45), P(28.98, 41.01)
qx, qy = kx - 70, (ky + iy) / 2
svg = (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
       f'<path class="dm__grey" d="{d(grey)}"/><path class="dm__home" d="{d(olive)}"/>'
       f'<path class="dm__arc" d="M{kx:.1f},{ky:.1f} Q{qx:.1f},{qy:.1f} {ix:.1f},{iy:.1f}"/>'
       f'<circle class="dm__halo" cx="{kx:.1f}" cy="{ky:.1f}" r="9"/><circle class="dm__pt" cx="{kx:.1f}" cy="{ky:.1f}" r="4"/>'
       f'<circle class="dm__halo" cx="{ix:.1f}" cy="{iy:.1f}" r="9" style="animation-delay:1.2s"/><circle class="dm__pt" cx="{ix:.1f}" cy="{iy:.1f}" r="4"/></svg>')
open('region_dots.svg', 'w').write(svg)
print(len(grey), len(olive), len(svg), round(W), round(H))
