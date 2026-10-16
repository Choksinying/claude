"""Makes the inside of each cut-out fully opaque. The background remover leaves some darker shoes
slightly see-through (alpha ~220-240); this sets alpha to 255 everywhere more than 3 px inside the
shoe's outline, keeping the soft outline and real holes (straps, clog holes) as they are.

usage: python tools/solidify.py photos2/*.png
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

for path in sys.argv[1:]:
    im = np.array(Image.open(path).convert('RGBA'))
    a = im[..., 3]
    inside = ndimage.binary_erosion(a > 128, iterations=3)
    before = int((inside & (a < 250)).sum())
    a[inside] = 255
    Image.fromarray(im).save(path)
    print(path, 'made opaque:', before, 'px')
