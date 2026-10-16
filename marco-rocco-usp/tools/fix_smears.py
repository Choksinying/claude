"""Second clean-up pass for photos2/: where the listing's COLOUR dots overlapped a shoe, the first
cut-out step could only smudge the area. Finds those spots by comparing the cut-out with the original
main image, then (after Nano Banana Pro restores them) takes only those spots from the restored picture.

usage: python tools/fix_smears.py prep  <bau_dir> MR8012 ...   -> repair2/in/<MODEL>.png + info.json
       python tools/fix_smears.py merge MR8012 ...             <- repair2/out/<MODEL>.png, updates photos2/
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(__file__), '..')
DIR = os.path.join(ROOT, 'repair2')
BG = (236, 234, 231)


def locate(bau, cut):
    """top-left of cut-out `cut` (RGBA) inside the main image `bau` (RGB)."""
    mask = (cut[..., 3] > 250).astype(np.float32)
    r = cv2.matchTemplate(bau, cut[..., :3], cv2.TM_SQDIFF, mask=np.repeat(mask[..., None], 3, 2))
    return cv2.minMaxLoc(r)[2]


def prep(bau_dir, models):
    os.makedirs(os.path.join(DIR, 'in'), exist_ok=True)
    info = {}
    for m in models:
        bau = np.array(Image.open(os.path.join(bau_dir, f'{m}_BAU.jpg')).convert('RGB')).astype(np.float32)
        first = np.array(Image.open(os.path.join(ROOT, f'photos/{m}.png')).convert('RGBA')).astype(np.float32)
        cut = np.array(Image.open(os.path.join(ROOT, f'photos2/{m}.png')).convert('RGBA'))
        # smudged spots: where the first cut-out differs from the main image under the shoe
        x0, y0 = locate(bau, first)
        H, W = first.shape[:2]
        diff = np.abs(bau[y0:y0 + H, x0:x0 + W] - first[..., :3]).max(-1) * (first[..., 3] > 200)
        bad = ndimage.binary_opening(diff > 28, iterations=2)
        lab, n = ndimage.label(bad)
        sizes = ndimage.sum(bad, lab, range(1, n + 1)) if n else []
        bad = np.isin(lab, [k + 1 for k, s in enumerate(sizes) if s > 250])
        full = np.zeros(bau.shape[:2], bool)
        full[y0:y0 + H, x0:x0 + W] = ndimage.binary_dilation(bad, iterations=14)
        # same spots in photos2 coordinates
        x2, y2 = locate(bau, cut.astype(np.float32))
        h2, w2 = cut.shape[:2]
        spot = full[y2:y2 + h2, x2:x2 + w2]
        side = int(max(w2, h2) * 1.12)
        ox, oy = (side - w2) // 2, (side - h2) // 2
        can = Image.new('RGBA', (side, side), BG + (255,))
        can.alpha_composite(Image.fromarray(cut), (ox, oy))
        can.convert('RGB').save(os.path.join(DIR, 'in', f'{m}.png'))
        sq = np.zeros((side, side), np.uint8)
        sq[oy:oy + h2, ox:ox + w2] = spot * 255
        Image.fromarray(sq).save(os.path.join(DIR, 'in', f'{m}_spots.png'))
        info[m] = {'side': side, 'ox': ox, 'oy': oy, 'w': w2, 'h': h2}
        print(m, 'spots px', int(spot.sum()))
    path = os.path.join(DIR, 'in', 'info.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(info)
    json.dump(old, open(path, 'w'), indent=1)


def merge(models):
    from rembg import new_session, remove
    seg = new_session('isnet-general-use')
    info = json.load(open(os.path.join(DIR, 'in', 'info.json')))
    for m in models:
        i = info[m]
        side, ox, oy, w2, h2 = i['side'], i['ox'], i['oy'], i['w'], i['h']
        cut = np.array(Image.open(os.path.join(ROOT, f'photos2/{m}.png')).convert('RGBA')).astype(np.float32)
        fixed = np.array(Image.open(os.path.join(DIR, 'out', f'{m}.png')).convert('RGB').resize((side, side), Image.LANCZOS))
        src = np.array(Image.open(os.path.join(DIR, 'in', f'{m}.png')).convert('L'), np.float32)
        (dx, dy), _ = cv2.phaseCorrelate(src, cv2.cvtColor(fixed, cv2.COLOR_RGB2GRAY).astype(np.float32),
                                         cv2.createHanningWindow((side, side), cv2.CV_32F))
        fixed = cv2.warpAffine(fixed, np.float32([[1, 0, -dx], [0, 1, -dy]]), (side, side), borderMode=cv2.BORDER_REPLICATE)
        fa = np.array(remove(Image.fromarray(fixed), session=seg, only_mask=True)).astype(np.float32)
        spot = np.array(Image.open(os.path.join(DIR, 'in', f'{m}_spots.png'))).astype(np.float32) / 255
        w = np.clip(cv2.GaussianBlur(spot, (0, 0), 5) * 1.6, 0, 1)[oy:oy + h2, ox:ox + w2, None]
        rgb = cut[..., :3] * (1 - w) + fixed[oy:oy + h2, ox:ox + w2] * w
        a = cut[..., 3:] * (1 - w) + fa[oy:oy + h2, ox:ox + w2, None] * w
        out = np.dstack([rgb, a]).clip(0, 255).astype(np.uint8)
        out[out[..., 3] < 12, 3] = 0
        Image.fromarray(out).save(os.path.join(ROOT, f'photos2/{m}.png'))
        print(m, f'shift ({dx:+.1f},{dy:+.1f}) merged')


if __name__ == '__main__':
    if sys.argv[1] == 'prep':
        prep(sys.argv[2], sys.argv[3:])
    else:
        merge(sys.argv[2:])
