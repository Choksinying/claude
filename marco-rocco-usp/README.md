# Marco Rocco – USP images (listing image #2)

1080×1080 USP images for the Shopee / TikTok Shop listings, one per model, built from the
"Marco Rocco USP" sheet. Finished images are in `output/` (`MR8012_USP.png` … `MR8035_USP.png`).

Layout (same for every model):

- **Header:** Marco Rocco logo, model code, headline USP and a one-line subtitle.
- **Hero:**
  - product photo on the warm backdrop of the model's main image (greige for unisex, pink for female, blue for male);
  - three model-specific USP cards;
  - a round gold sticker;
  - a "Unisex · Multiple colours" pill.
- **Bottom band:** the six benefits every model shares: Durable, EVA Material, Easy to Clean, Lightweight,
  Soft & Cushioned, Waterproof. MR8030 shows Non-Slip Sole instead, since its sheet has no waterproof claim.

## Edit and re-render

| What | Where |
|---|---|
| Wording, icons, sticker text, background colours | `data/models.js` |
| Layout, fonts, brand colours | `template/usp.html` (colours are the CSS variables at the top) |
| Product photos | `photos/<MODEL>.png` (transparent cut-out) |

```bash
npm i playwright@1.56.1     # once; or use a global playwright
node render.mjs             # all models  -> output/<MODEL>_USP.png
node render.mjs MR8013      # just one
```

Open `template/usp.html?model=MR8013` in a browser to preview; the dropdown switches models.

## Product photos

`tools/cutout.py` makes the transparent cut-outs:

```bash
pip install "rembg[cpu]" opencv-python-headless scipy pillow
python tools/cutout.py plain  path/to/white-background-photo.jpg MR8013   # plain product photo (best)
python tools/cutout.py bau    path/to/MR8013_BAU.jpg            MR8013   # designed main image
```

The current cut-outs come from the designed main (BAU) images. The script drops their logo, the big
UNISEX/FEMALE/MALE word, the colour dots and the HEIGHT BOOST badge. Where that badge covered part of a
shoe, the spot is recorded in `photos/meta.js` and the template places the gold sticker over it.
Plain white-background photos give the cleanest result: run `plain` on them and re-render.

Fonts: Poppins (SIL Open Font License, `fonts/OFL-Poppins.txt`). Icons: Lucide (ISC licence).
