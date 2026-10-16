"""Makes the USP scene tiles used by template/usp2.html (`scene: '<NAME>'` in data/usp2.js):
scenes/out/<NAME>.png (Nano Banana Pro edits of the real-photo inputs in scenes/in/) -> scenes/tiles/<NAME>.jpg, 720px.

For the scenes in PASTE, the real product pixels are put back on top of the AI picture: the cut-out at its place
in the input (scenes/specs.json view for photos2/<MODEL>.png, or scenes/in/place.json for a single-shoe cut-out),
aligned to the output by phase correlation. So there the product is exactly the photo and only the surroundings
(feather, shadow) are AI.

usage: python tools/scene_tiles.py
"""
import json
import os

import cv2
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SC = os.path.join(ROOT, 'scenes')
SIZE = 720
PASTE = {'MR8030_4b': 'scenes/in/MR8030_taupe.png', 'MR8012_5': 'photos2/MR8012.png'}

place = json.load(open(os.path.join(SC, 'in', 'place.json')))
for name, s in json.load(open(os.path.join(SC, 'specs.json'))).items():
    # same placement as tools/scene_inputs.py
    W, H = Image.open(os.path.join(ROOT, 'photos2', f"{s['model']}.png")).size
    cx, cy, f = s['view']
    k = 1024 / (f * W)
    place[name] = {'x': round(512 - cx * W * k), 'y': round(512 - cy * H * k), 'w': round(W * k), 'h': round(H * k)}
os.makedirs(os.path.join(SC, 'tiles'), exist_ok=True)
for f in sorted(os.listdir(os.path.join(SC, 'out'))):
    name = f[:-4]
    out = Image.open(os.path.join(SC, 'out', f)).convert('RGB').resize((1024, 1024), Image.LANCZOS)
    if name in PASTE:
        p = place[name]
        cut = Image.open(os.path.join(ROOT, PASTE[name])).convert('RGBA').resize((p['w'], p['h']), Image.LANCZOS)
        inp = np.array(Image.open(os.path.join(SC, 'in', f)).convert('L'), np.float32)
        ai = np.array(out.convert('L'), np.float32)
        x0, y0, x1, y1 = p['x'] - 20, p['y'] - 20, p['x'] + p['w'] + 20, p['y'] + p['h'] + 20
        win = cv2.createHanningWindow((x1 - x0, y1 - y0), cv2.CV_32F)
        (dx, dy), resp = cv2.phaseCorrelate(inp[y0:y1, x0:x1], ai[y0:y1, x0:x1], win)
        print(name, f'shift {dx:+.1f},{dy:+.1f} (response {resp:.2f})')
        out.paste(cut, (round(p['x'] + dx), round(p['y'] + dy)), cut)
    out.resize((SIZE, SIZE), Image.LANCZOS).save(os.path.join(SC, 'tiles', f'{name}.jpg'), quality=90)
    print(name, 'ok')
