"""Makes the outline logo (monogram + MARCO ROCCO, no maroon square) in one colour on a transparent
background, from assets/logo.png (white logo on the maroon square):

  assets/logo_brown.png  brown of the listing images' logo, for unisex and male models
  assets/logo_white.png  white, for female models

usage: python tools/logo_variants.py
"""
import os

import numpy as np
from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')
COLOURS = {'brown': (75, 38, 27), 'white': (255, 255, 255)}

src = np.array(Image.open(os.path.join(ASSETS, 'logo.png')).convert('RGB')).astype(np.float32)
g_bg = np.median(src[:20, :20, 1])                       # green channel of the maroon square
alpha = np.clip((src[..., 1] - g_bg) / (255 - g_bg), 0, 1)
ys, xs = np.nonzero(alpha > .05)
pad = 6
alpha = alpha[ys.min() - pad:ys.max() + pad + 1, xs.min() - pad:xs.max() + pad + 1]

for name, rgb in COLOURS.items():
    out = np.zeros(alpha.shape + (4,), np.uint8)
    out[..., :3] = rgb
    out[..., 3] = (alpha * 255).round()
    Image.fromarray(out, 'RGBA').save(os.path.join(ASSETS, f'logo_{name}.png'))
    print(f'logo_{name}.png', out.shape[1], 'x', out.shape[0])
