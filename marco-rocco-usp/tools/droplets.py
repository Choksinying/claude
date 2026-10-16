"""Draws assets/droplets.png: transparent overlay of water beads, laid over a real product photo
for the "waterproof" visual (the photo underneath is untouched).

usage: python tools/droplets.py
"""
import os

import numpy as np
from PIL import Image

SIZE = 640
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
rgba = np.zeros((SIZE, SIZE, 4), np.float32)


def over(dst, rgb, a):
    """Alpha-composite colour rgb with per-pixel alpha a onto dst (premultiplied-free 'over')."""
    out_a = a + dst[..., 3] * (1 - a)
    for c in range(3):
        dst[..., c] = np.where(out_a > 0, (rgb[c] * a + dst[..., c] * dst[..., 3] * (1 - a)) / np.maximum(out_a, 1e-6), 0)
    dst[..., 3] = out_a


drops = []
while len(drops) < 70:
    r = float(rng.choice([rng.uniform(5, 9), rng.uniform(9, 16), rng.uniform(16, 26)], p=[.5, .35, .15]))
    x, y = rng.uniform(r, SIZE - r), rng.uniform(r, SIZE - r)
    if all((x - a) ** 2 + (y - b) ** 2 > (r + c + 6) ** 2 for a, b, c in drops):
        drops.append((x, y, r))

for x, y, r in drops:
    ry = r * 0.92
    d = np.sqrt(((xx - x) / r) ** 2 + ((yy - y) / ry) ** 2)
    # contact shadow, offset down-right
    ds = np.sqrt(((xx - x - r * .18) / (r * 1.05)) ** 2 + ((yy - y - r * .25) / (ry * 1.05)) ** 2)
    over(rgba, (0, 0, 0), np.clip(1 - ds, 0, 1) ** .6 * .28 * (ds < 1))
    inside = d < 1
    # bead body: clear centre, darker rim, bright refraction crescent at the bottom
    rim = np.clip((d - .55) / .45, 0, 1) ** 2
    over(rgba, (40, 40, 40), np.where(inside, rim * .32, 0))
    cres = np.clip(1 - np.sqrt(((xx - x + r * .1) / (r * .7)) ** 2 + ((yy - y - r * .45) / (ry * .38)) ** 2), 0, 1)
    over(rgba, (255, 255, 255), np.where(inside, cres * .55, 0))
    over(rgba, (255, 255, 255), np.where(inside, .10, 0))
    # specular highlight, top-left
    hl = np.clip(1 - np.sqrt(((xx - x + r * .38) / (r * .26)) ** 2 + ((yy - y + r * .4) / (ry * .17)) ** 2), 0, 1)
    over(rgba, (255, 255, 255), np.where(inside, np.clip(hl * 2.2, 0, 1) * .95, 0))

out = np.dstack([rgba[..., :3], rgba[..., 3:] * 255]).clip(0, 255).astype(np.uint8)
path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'droplets.png')
Image.fromarray(out, 'RGBA').save(path)
print('wrote', os.path.normpath(path))
