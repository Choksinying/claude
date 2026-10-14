"""Cut the products out of Marco Rocco photos for the USP template.

Two kinds of source photo are handled:
  * designed main (BAU) images with overlays: script logo, big translucent UNISEX/FEMALE/MALE word,
    "COLOUR :" dots row and the round HEIGHT BOOST badge;
  * plain product photos (white / light background), which only need the background removed.

Overlays sit on the background, so they are simply excluded from the cut-out. The round badge can
cover part of a shoe; when it does, the area it covered is written to photos/<MODEL>.json as a
"patch" circle and the template places its round sticker exactly there.

usage:
  python tools/cutout.py bau   <src.jpg> <MODEL>     # designed main image
  python tools/cutout.py plain <src.jpg> <MODEL>     # plain product photo
Writes photos/<MODEL>.png (transparent, trimmed) and, if needed, photos/<MODEL>.json.
Needs: pip install "rembg[cpu]" opencv-python-headless scipy pillow
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "..", "photos")
SEG = new_session("isnet-general-use")


def fit_background(img, bgmask):
    """Smooth estimate of the backdrop behind everything, filled in from background pixels."""
    H, W = bgmask.shape
    f = 8
    small = cv2.resize(img, (W // f, H // f), interpolation=cv2.INTER_AREA)
    hole = cv2.resize((~bgmask).astype(np.uint8) * 255, (W // f, H // f), interpolation=cv2.INTER_NEAREST)
    small = cv2.inpaint(small, cv2.dilate(hole, np.ones((3, 3), np.uint8)), 6, cv2.INPAINT_TELEA)
    small = cv2.GaussianBlur(small, (0, 0), 2)
    return cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)


def bau_overlays(img, alpha0):
    """Masks of the designed-image overlays.

    Returns (backdrop, marks, badge, badge_circle, bg, halo):
      backdrop - logo and big word: they only cover background, so they get the backdrop colour;
      marks    - COLOUR : label and dots: thin marks that can sit on top of a shoe, so they are inpainted;
      badge    - the round HEIGHT BOOST badge and its label;
      halo     - plain-backdrop pixels around the big word that the segmenter half-keeps.
    """
    H, W = img.shape[:2]
    s = W / 1080.0
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    over = np.zeros((H, W), np.uint8)

    # script logo, top-left
    cv2.rectangle(over, (int(20 * s), int(25 * s)), (int(360 * s), int(145 * s)), 255, -1)

    # round HEIGHT BOOST badge (white ring) + the "+X.XCM" label under it
    roi = gray[int(700 * s):, int(700 * s):]
    circles = cv2.HoughCircles(cv2.GaussianBlur(roi, (5, 5), 1.5), cv2.HOUGH_GRADIENT, 1.2, 200,
                               param1=120, param2=40, minRadius=int(100 * s), maxRadius=int(140 * s))
    cx, cy, r = (circles[0][0] + [700 * s, 700 * s, 0]) if circles is not None else (885 * s, 900 * s, 122 * s)
    badge = np.zeros((H, W), np.uint8)
    cv2.circle(badge, (int(cx), int(cy)), int(r + 8 * s), 255, -1)
    cv2.rectangle(badge, (int(cx - 95 * s), int(cy + 85 * s)), (int(cx + 95 * s), int(cy + 140 * s)), 255, -1)

    # "COLOUR :" label and colour dots, left of the badge
    y0, y1, x0, x1 = int(915 * s), int(1010 * s), int(20 * s), int(cx - r - 10 * s)
    sub = gray[y0:y1, x0:x1]
    band = np.zeros(sub.shape, np.uint8)
    dots = cv2.HoughCircles(cv2.GaussianBlur(sub, (5, 5), 1), cv2.HOUGH_GRADIENT, 1.2, int(50 * s),
                            param1=100, param2=22, minRadius=int(20 * s), maxRadius=int(32 * s))
    if dots is not None:
        # real colour dots have a white ring and share one row (clog holes can look like circles too)
        ringed = []
        for x, y, rr in dots[0]:
            ring = np.zeros(sub.shape, np.uint8)
            cv2.circle(ring, (int(x), int(y)), int(rr + 1 * s), 255, max(2, int(3 * s)))
            outer = np.zeros(sub.shape, np.uint8)
            cv2.circle(outer, (int(x), int(y)), int(rr + 9 * s), 255, max(2, int(3 * s)))
            if sub[ring > 0].mean() > 200 or sub[ring > 0].mean() > sub[outer > 0].mean() + 15:
                ringed.append((x, y, rr))
        if ringed:
            # the row: same height and size as the clearly ringed dots (picks up dots the ring test missed)
            row_y, row_r = np.median([d[1] for d in ringed]), np.median([d[2] for d in ringed])
            ringed = [d for d in dots[0] if abs(d[1] - row_y) < 8 * s and abs(d[2] - row_r) < 5 * s]
        dots = np.array([ringed], np.float32) if ringed else None
    if dots is not None:
        for x, y, rr in dots[0]:
            cv2.circle(band, (int(x), int(y)), int(rr + 6 * s), 255, -1)
        # the label sits on the dots' row, ending just left of the first dot: mask its dark glyph pixels only
        first = dots[0][np.argmin(dots[0][:, 0])]
        ly, lx1 = int(first[1]), int(first[0] - first[2] - 4 * s)
        lx0 = max(0, int(lx1 - 260 * s))
        glyph = (sub[max(0, ly - int(26 * s)):ly + int(26 * s), lx0:lx1] < 90).astype(np.uint8) * 255
        band[max(0, ly - int(26 * s)):ly + int(26 * s), lx0:lx1] |= cv2.dilate(glyph, np.ones((5, 5), np.uint8))
    else:
        lab, n = ndimage.label(sub < 95)
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab == i)
            if len(ys) > 15 and ys.max() - ys.min() < 50 * s:
                band[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = 255
    marks = np.zeros((H, W), np.uint8)
    marks[y0:y1, x0:x1] = cv2.dilate(band, np.ones((5, 5), np.uint8))

    # big translucent word behind the products: an even, colourless lightening of the backdrop
    zone = np.zeros((H, W), bool)
    zone[int(150 * s):int(470 * s), :] = True
    bgmask = (alpha0 < 8) & (over == 0) & (badge == 0) & (marks == 0)
    bg = fit_background(img, bgmask)
    for _ in range(2):   # the segmenter sometimes counts a faint word as background: refit without it
        a = (img.astype(np.float32) - bg) / np.maximum(255.0 - bg, 1.0)
        lighter = zone & (a.mean(-1) > 0.08) & (a.max(-1) - a.min(-1) < 0.12)
        bg = fit_background(img, bgmask & ~cv2.dilate(lighter.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool))
    a = (img.astype(np.float32) - bg) / np.maximum(255.0 - bg, 1.0)
    amean, aspread = a.mean(-1), a.max(-1) - a.min(-1)
    cand = zone & (amean > 0.12) & (aspread < 0.09)
    halo = np.zeros((H, W), bool)
    if cand.sum() > 2000:
        hist, edges = np.histogram(amean[cand], bins=30, range=(0.15, 0.9))
        peak = edges[hist.argmax()] + (edges[1] - edges[0]) / 2
        strong = ndimage.binary_opening(cand & (np.abs(amean - peak) < 0.09), iterations=2)
        lab, n = ndimage.label(strong)
        if n:
            sizes = ndimage.sum(strong, lab, range(1, n + 1))
            strong = np.isin(lab, [i + 1 for i, z in enumerate(sizes) if z > 1500 * s * s])
        # only needed when the segmenter actually kept the word; otherwise leave the shoes untouched
        if n and strong.any() and (alpha0[strong] > 128).mean() > 0.2:
            # take in the letters' soft edges, but never more than a few pixels from a sure letter pixel
            weak = zone & (aspread < 0.16) & (np.abs(amean - peak) < 0.16)
            near = cv2.dilate(strong.astype(np.uint8), np.ones((int(15 * s), int(15 * s)), np.uint8)).astype(bool)
            text = strong | (weak & near)
            # inside the rows the word occupies, also drop looser matches (letter edges softened by shadows)
            rows = np.nonzero(strong.sum(1) > 60 * s)[0]
            if len(rows):
                band = np.zeros((H, W), bool)
                band[max(0, rows.min() - int(12 * s)):rows.max() + int(12 * s), :] = True
                text |= band & (aspread < 0.15) & (np.abs(amean - peak) < 0.2)
                # the segmenter leaves a soft halo of plain backdrop around the letters
                halo[max(0, rows.min() - int(30 * s)):rows.max() + int(30 * s), :] = True
                halo &= (amean < 0.2) & (aspread < 0.08)
            over |= cv2.dilate(text.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    return over, marks, badge, (float(cx), float(cy), float(r)), bg, halo


def keep_main_parts(alpha):
    """Drop specks: keep connected parts at least 3% the size of the biggest one."""
    lab, n = ndimage.label(alpha > 128)
    if n:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, z in enumerate(sizes) if z >= 0.03 * sizes.max()])
        alpha[~ndimage.binary_dilation(keep, iterations=3)] = 0
    return alpha


def main():
    kind, src, model = sys.argv[1:4]
    img = np.array(Image.open(src).convert("RGB"))
    H, W = img.shape[:2]
    alpha = np.array(remove(Image.fromarray(img), session=SEG, only_mask=True))
    alpha[alpha < 20] = 0
    patch = None

    if kind == "bau":
        # the cut-out shape comes from the original photo; overlay areas are then blanked out of it
        over, marks, badge, (cx, cy, r), bg, halo = bau_overlays(img, alpha)
        alpha[(over | badge) > 0] = 0
        alpha[halo & (alpha < 250)] = 0
        clean = img.copy()
        # marks on plain backdrop are dropped; marks overlapping a shoe are inpainted with the shoe's colour
        lab, n = ndimage.label(marks > 0)
        for i in range(1, n + 1):
            comp = lab == i
            ring = cv2.dilate(comp.astype(np.uint8), np.ones((11, 11), np.uint8)).astype(bool) & ~comp & (marks == 0)
            if (np.linalg.norm(img[ring].astype(np.float32) - bg[ring], axis=1) < 20).mean() > 0.5:
                alpha[comp] = 0
                marks[comp] = 0
        img = cv2.inpaint(clean, marks, 5, cv2.INPAINT_TELEA)
        alpha = keep_main_parts(alpha)
        # does a product run under the badge? (product pixels right at the badge edge)
        ring = cv2.dilate(badge, np.ones((25, 25), np.uint8)) & ~badge
        if ((alpha > 128) & (ring > 0)).sum() > 150:
            ys, xs = np.nonzero(badge)
            (px, py), pr = cv2.minEnclosingCircle(np.stack([xs, ys], 1).astype(np.float32))
            patch = (px, py, pr)
    else:
        # plain photo: the product is the large central part; logo / captions are small separate parts
        alpha = keep_main_parts(alpha)
        lab, n = ndimage.label(alpha > 128)
        if n > 1:
            sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            alpha[~ndimage.binary_dilation(lab == (sizes.argmax() + 1), iterations=3)] = 0

    rgba = np.dstack([img, alpha])
    ys, xs = np.nonzero(alpha)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    os.makedirs(PHOTOS, exist_ok=True)
    Image.fromarray(rgba[y0:y1, x0:x1]).save(os.path.join(PHOTOS, f"{model}.png"))

    # photos/meta.js (loaded by the template): where the round sticker must sit, as fractions of the cut-out
    meta_path = os.path.join(PHOTOS, "meta.js")
    prefix = "window.PHOTO_META = "
    meta = {}
    if os.path.exists(meta_path):
        meta = json.loads(open(meta_path).read().strip()[len(prefix):].rstrip(";"))
    meta.pop(model, None)
    if patch:
        w, h = x1 - x0, y1 - y0
        meta[model] = {"patch": {"x": round((patch[0] - x0) / w, 4), "y": round((patch[1] - y0) / h, 4),
                                 "r": round(patch[2] / w, 4)}}
    with open(meta_path, "w") as f:
        f.write(prefix + json.dumps(meta, indent=1, sort_keys=True) + ";\n")
    print(f"{model}: {x1 - x0}x{y1 - y0}" + (f"  patch {meta[model]['patch']}" if patch else ""))


if __name__ == "__main__":
    main()
