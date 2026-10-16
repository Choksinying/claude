"""Fills the parts of a cut-out that the listing's HEIGHT BOOST badge covered.

repair/in/<MODEL>.png is the cut-out on a plain backdrop (layout in repair/in/info.json);
repair/out/<MODEL>.png is the same picture restored by Nano Banana Pro. Taken from the restored picture:
the badge circle, other spots it filled in (smaller bites) and the surroundings of caption left-overs
it removed. Every other pixel stays the original photo. Writes photos2/<MODEL>.png.

usage: python tools/merge_repair.py [MR8012 ...]
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(__file__), '..')
info = json.load(open(os.path.join(ROOT, 'repair/in/info.json')))
models = sys.argv[1:] or sorted(info)
SEG = new_session('isnet-general-use')
os.makedirs(os.path.join(ROOT, 'photos2'), exist_ok=True)


def blobs(mask, min_px):
    """mask without its connected parts smaller than min_px (thin outline differences)."""
    lab, n = ndimage.label(mask)
    if not n:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    return np.isin(lab, [k + 1 for k, s in enumerate(sizes) if s >= min_px])


def feather(mask, px):
    return np.clip(cv2.GaussianBlur(mask.astype(np.float32), (0, 0), px) * 2, 0, 1)


def drop_specks(alpha, keep=0.01):
    lab, n = ndimage.label(alpha > 40)
    if n < 2:
        return alpha
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    good = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= keep * sizes.max()])
    good = ndimage.binary_dilation(good, iterations=3)
    return np.where(good, alpha, 0).astype(np.uint8)


for m in models:
    i = info[m]
    side, ox, oy = i['side'], i['ox'], i['oy']
    cut = np.array(Image.open(os.path.join(ROOT, f'photos/{m}.png')).convert('RGBA'))
    H, W = cut.shape[:2]
    orig = np.zeros((side, side, 4), np.uint8)
    orig[oy:oy + H, ox:ox + W] = cut

    fixed = Image.open(os.path.join(ROOT, f'repair/out/{m}.png')).convert('RGB').resize((side, side), Image.LANCZOS)
    fixed = np.array(fixed)
    # line the restored picture up with the original (it can drift by a few pixels)
    src = np.array(Image.open(os.path.join(ROOT, f'repair/in/{m}.png')).convert('L'), np.float32)
    dst = cv2.cvtColor(fixed, cv2.COLOR_RGB2GRAY).astype(np.float32)
    win = cv2.createHanningWindow((side, side), cv2.CV_32F)
    (dx, dy), _ = cv2.phaseCorrelate(src, dst, win)
    M = np.float32([[1, 0, -dx], [0, 1, -dy]])
    fixed = cv2.warpAffine(fixed, M, (side, side), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    fa = np.array(remove(Image.fromarray(fixed), session=SEG, only_mask=True))

    yy, xx = np.mgrid[0:side, 0:side]
    d = np.sqrt((xx - i['cx']) ** 2 + (yy - i['cy']) ** 2)
    w = np.clip((i['r'] + 10 - d) / 8, 0, 1)                   # 1 inside the badge circle, feathered edge
    # inside the circle, keep the original wherever it still has the shoe
    w = w * (1 - (orig[..., 3] > 200))
    # elsewhere: other bitten spots the restore filled in, and caption left-overs it removed
    oa = orig[..., 3]
    added = blobs(ndimage.binary_opening((fa > 200) & (oa < 60), iterations=2), 200)
    removed = blobs(ndimage.binary_opening((oa > 60) & (fa < 30), iterations=2), 150)
    w = np.maximum(w, feather(ndimage.binary_dilation(added, iterations=4), 3))
    w = np.maximum(w, feather(ndimage.binary_dilation(removed, iterations=22), 6))
    w = w[..., None]
    rgb = orig[..., :3] * (1 - w) + fixed * w
    a = orig[..., 3:].astype(np.float32) * (1 - w) + fa[..., None].astype(np.float32) * w
    out = np.dstack([rgb, a]).clip(0, 255).astype(np.uint8)
    out[..., 3] = drop_specks(out[..., 3])
    out[out[..., 3] < 12, 3] = 0
    ys, xs = np.nonzero(out[..., 3])
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(out).save(os.path.join(ROOT, f'photos2/{m}.png'))
    print(m, f'shift ({dx:+.1f},{dy:+.1f})', out.shape[1], 'x', out.shape[0], f'filled {added.sum()} px, removed {removed.sum()} px')
