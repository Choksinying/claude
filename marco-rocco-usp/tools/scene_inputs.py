"""Builds the inputs for the USP scene tiles (hand pressing, natural water, durian, sole on a wet floor...):
a square crop of the real product photo on a plain backdrop, which Nano Banana Pro then edits.
Specs are in scenes/specs.json: {"MR8012_3": {"model": "MR8012", "view": [cx, cy, f]}, ...}
(view as in data/usp2.js: centre and window width as fractions of photos2/<MODEL>.png).
Writes scenes/in/<NAME>.png (1024x1024).

usage: python tools/scene_inputs.py
"""
import json
import os

from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SIZE = 1024
BG = (238, 234, 229, 255)

specs = json.load(open(os.path.join(ROOT, 'scenes', 'specs.json')))
os.makedirs(os.path.join(ROOT, 'scenes', 'in'), exist_ok=True)
for name, s in specs.items():
    cut = Image.open(os.path.join(ROOT, 'photos2', f"{s['model']}.png")).convert('RGBA')
    W, H = cut.size
    cx, cy, f = s['view']
    k = SIZE / (f * W)                       # scale so the window fills the square
    big = cut.resize((round(W * k), round(H * k)), Image.LANCZOS)
    can = Image.new('RGBA', (SIZE, SIZE), BG)
    can.paste(big, (round(SIZE / 2 - cx * W * k), round(SIZE / 2 - cy * H * k)), big)
    can.convert('RGB').save(os.path.join(ROOT, 'scenes', 'in', f'{name}.png'))
    print(name, f'scale x{k:.2f}')
