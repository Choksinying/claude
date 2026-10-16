# Marco Rocco – USP images (listing image #2)

1080×1080 USP images for the Shopee / TikTok Shop listings, built from the "Marco Rocco USP" sheet.

**Current images: `final/`**. There are two per model, named by SKU:

- `MR80xx_USP.jpg`: layout A, the products on a podium with four USP tiles in a maroon band.
- `MR80xx_USP_2.jpg`: layout B, the products on a podium with four gold-ringed zoom circles.

Every product picture in them is the real product photo, so patterns and shapes are exactly the
product's. Only the spots that the listing's own graphics had covered were restored with Nano Banana Pro
(see below). The logo is the brand's logo file (`assets/logo.png`). The backdrop colour follows the Shopee
main images: greige for unisex, pink for female, blue for male.

## Edit and re-render

| What | Where |
|---|---|
| The 4 USPs per model, what each tile/circle zooms into, gender | `data/usp2.js` |
| Layouts, colours, fonts | `template/usp2.html` (gender colours are the `.unisex` / `.female` / `.male` rules) |
| Product photos (transparent cut-outs) | `photos2/<MODEL>.png` |

```bash
npm i playwright@1.56.1      # once; or use a global playwright
node render2.mjs             # all models, both layouts -> output2/*.png
node render2.mjs MR8030      # one model
```

Then convert `output2/*.png` to JPG for `final/`.

Each USP visual is a zoom into the real photo (`view: [cx, cy, f]`) with optional overlays:

- water beads (`assets/droplets.png`, drawn by `tools/droplets.py`);
- a height bracket;
- a wet tiled floor with reflection (non-slip);
- a slip-on arrow;
- a press arrow (soft);
- charms;
- a floating product above a feather (lightweight).

Some tiles are photo scenes instead (`scene: '<NAME>'`): MR8012 (all 4), MR8030 (all 4), MR8035 (soft,
waterproof) and MR8022 (waterproof). These show a hand pressing the footbed, natural running water, a durian, or a
feather.

1. `tools/scene_inputs.py` crops the real photo for each scene (`scenes/specs.json`) into `scenes/in/`.
2. Nano Banana Pro adds the hand, water and so on, leaving the product as it is.
3. The results are fetched into `scenes/out/` by the same workflow.
4. `tools/scene_tiles.py` makes `scenes/tiles/<NAME>.jpg`. For the MR8030 feather scene it also pastes the
   real product pixels back on top. The MR8012 feather scene does the same.

There are no photos of the outsoles, so no scene shows a sole. Outsole scenes drawn by the AI (MR8012_2,
MR8030_2/2b, MR8035_3) were wrong and are not used.

## Product photos

The cut-outs come from the designed main (BAU) images:

1. `tools/cutout.py` produced `photos/`.
2. Where the listing's HEIGHT BOOST badge or COLOUR dots had covered part of a shoe, Nano Banana Pro
   restored the picture (`repair/`, `repair2/`, fetched by `.github/workflows/fetch-repair-images.yml`).
3. `tools/merge_repair.py` and `tools/fix_smears.py` take only those spots from the restored picture.
   Every other pixel stays the original photo.
4. `tools/solidify.py` makes the inside of each shoe fully opaque.

## Earlier versions

- `output/`: first template version.
- `nano-banana/`: fully AI-generated version. It was replaced because the AI redrew the products and logo
  inaccurately.

Fonts: Poppins (SIL Open Font License, `fonts/OFL-Poppins.txt`). Icons: Lucide (ISC licence).
