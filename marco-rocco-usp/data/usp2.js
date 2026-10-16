// USP images v2: the 4 chosen USPs per model, each shown as a zoom into the REAL product photo
// (photos2/<MODEL>.png), so the product pattern is exactly the product's.
//
// gender: picks the backdrop colour of the Shopee main images (unisex greige, female pink, male blue).
// view: [cx, cy, f] = centre of the zoom as fractions of the photo, f = zoom window width / photo width;
//     bottom: y = move the zoom up/down so the product's lowest point sits at y (fraction of the tile).
// float: true = whole product floating above a feather (lightweight).
// floor: y = wet tiled floor from y (fraction of the tile) down, with the product's reflection (non-slip);
//     0 = the whole tile is floor (top-down photos).
// fx: overlays - 'drops' (water beads on the product), {measure: {x, y1, y2, text}} (height bracket of
//     height h standing on the product's lowest point, or from y1 to y2),
//     {arrow: [x1, y1, x2, y2, bend]} (slip-on), {press: [x, y]} (soft), {swap: [x, y]} (2-in-1),
//     {charms: [[x, y, kind], ...]}; all positions are fractions of the tile.
// scene: '<NAME>' = a photo scene instead of the zoom (scenes/tiles/<NAME>.jpg, made from the real product photo
//     with Nano Banana Pro: hand pressing, natural water, sole on a wet floor...); crop: [cx, cy, f] of it.
// icon: small gold badge in the tile corner (layout A).
// b: overrides for the round zoom in layout B. A / B: layout options (hero box, B connector anchors).

const drops = { fx: ['drops'], icon: 'droplets' };

window.MODELS2 = [
  { id: 'MR8012', gender: 'unisex', usps: [
    { label: 'Wave pattern design', scene: 'MR8012_1', crop: [.55, .5, .86] },
    { label: 'Lightweight', scene: 'MR8012_5', crop: [.5, .44, .82], icon: 'feather' },
    { label: 'Soft & cushioned', scene: 'MR8012_3', crop: [.6, .46, .82], icon: 'cloud' },
    { label: 'Waterproof & easy to clean', scene: 'MR8012_4', crop: [.5, .45, .9], icon: 'droplets' },
  ] },
  { id: 'MR8013', gender: 'unisex', usps: [
    { label: 'Boost height 4cm+', view: [.76, .80, .36], bottom: .9, fx: [{ measure: { x: .9, h: .32, text: '4CM+', tagLeft: true } }] },
    { label: 'Anti-slip sole', view: [.55, .83, .36], floor: .8, icon: 'footprints' },
    { label: 'Soft & cushioned', view: [.68, .60, .30], fx: [{ press: [.5, .55] }], icon: 'cloud' },
    { label: 'Waterproof & easy to clean', view: [.36, .30, .30], ...drops },
  ] },
  { id: 'MR8015', gender: 'unisex', usps: [
    { label: 'Stylish striped pattern', view: [.78, .62, .36] },
    { label: 'Easy slip-on', view: [.82, .50, .42], fx: [{ arrow: [.95, .08, .78, .42, .2] }], icon: 'log-in' },
    { label: 'Lightweight', float: true, icon: 'feather' },
    { label: 'Waterproof & easy to clean', view: [.42, .50, .34], ...drops },
  ] },
  { id: 'MR8017', gender: 'unisex', usps: [
    { label: '4cm thick sole', view: [.70, .80, .40], bottom: .9, fx: [{ measure: { x: .9, h: .3, text: '4CM', tagLeft: true } }] },
    { label: 'Easy slip-on', view: [.78, .46, .42], fx: [{ arrow: [.95, .1, .62, .42, .2] }], icon: 'log-in' },
    { label: 'Soft & cushioned', view: [.72, .40, .30], fx: [{ press: [.5, .55] }], icon: 'cloud' },
    { label: 'Waterproof & easy to clean', view: [.35, .32, .36], ...drops },
  ] },
  { id: 'MR8018', gender: 'unisex', usps: [
    { label: '4cm thick sole', view: [.58, .84, .45], bottom: .9, fx: [{ measure: { x: .9, h: .25, text: '4CM', tagLeft: true } }] },
    { label: 'Non-slip outsole', view: [.45, .84, .45], floor: .8, icon: 'footprints' },
    { label: 'Easy slide-in', view: [.64, .78, .45], fx: [{ arrow: [.1, .1, .45, .45, -.2] }], icon: 'log-in' },
    { label: 'Soft & cushioned', view: [.36, .30, .40], fx: [{ press: [.5, .55] }], icon: 'cloud' },
  ] },
  { id: 'MR8021', gender: 'female', usps: [
    { label: 'Woven-style texture', view: [.22, .45, .24] },
    { label: 'Soft & cushioned', view: [.72, .74, .34], fx: [{ press: [.5, .55] }], icon: 'cloud' },
    { label: 'Lightweight', float: true, icon: 'feather' },
    { label: 'Waterproof & easy to clean', view: [.45, .55, .30], ...drops },
  ] },
  { id: 'MR8022', gender: 'female', usps: [
    { label: '5cm thick sole', view: [.80, .60, .50], fx: [{ measure: { x: .92, y1: .2, y2: .66, text: '5CM', tagLeft: true } }] },
    { label: 'Criss-cross straps', view: [.32, .35, .30] },
    { label: 'Gold logo buckle', view: [.64, .44, .40] },
    { label: 'Waterproof & easy to clean', scene: 'MR8022_4', icon: 'droplets' },
  ] },
  { id: 'MR8024', gender: 'female', usps: [
    { label: 'Waterproof boot', view: [.26, .45, .40], ...drops },
    { label: 'Rain-ready style', view: [.58, .45, .45], fx: ['drops'], icon: 'cloud-rain' },
    { label: 'More coverage', view: [.32, .50, .62], icon: 'shield' },
    { label: 'Thick sole', view: [.32, .84, .45], bottom: .9, fx: [{ measure: { x: .9, h: .22, text: '', tagLeft: true } }] },
  ] },
  { id: 'MR8026', gender: 'female', usps: [
    { label: 'Up to 7.5cm sole', view: [.80, .62, .36], bottom: .9, fx: [{ measure: { x: .92, h: .45, text: '7.5CM', tagLeft: true } }] },
    { label: 'Customizable charms', view: [.14, .44, .30],
      fx: [{ charms: [[.22, .32, 'flower'], [.4, .3, 'heart'], [.18, .52, 'smile'], [.38, .5, 'star'], [.26, .7, 'daisy']] }] },
    { label: 'Chunky but lightweight', float: true, icon: 'feather' },
    { label: 'Waterproof & easy to clean', view: [.45, .36, .30], ...drops },
  ] },
  { id: 'MR8027', gender: 'female', usps: [
    { label: '5.5cm thick sole', view: [.18, .76, .30], bottom: .9, fx: [{ measure: { x: .9, h: .35, text: '5.5CM', tagLeft: true } }] },
    { label: 'Stylish wave pattern', view: [.55, .66, .24] },
    { label: 'Customizable charm', view: [.85, .66, .26],
      fx: [{ charms: [[.3, .35, 'flower'], [.55, .4, 'heart'], [.35, .62, 'star'], [.62, .66, 'smile']] }] },
    { label: 'Waterproof & easy to clean', view: [.20, .60, .28], ...drops },
  ] },
  { id: 'MR8028', gender: 'unisex', usps: [
    { label: '2-in-1 design', view: [.76, .50, .32], fx: [{ swap: [.72, .72] }] },
    { label: 'Heel-strap style', view: [.20, .56, .32], icon: 'repeat-2' },
    { label: 'Easy slip-on', view: [.48, .20, .34], fx: [{ arrow: [.9, .1, .6, .45, .2] }], icon: 'log-in' },
    { label: 'Waterproof & easy to clean', view: [.30, .72, .30], ...drops },
  ] },
  { id: 'MR8029', gender: 'unisex', usps: [
    { label: '3.5cm thick sole', view: [.18, .76, .30], bottom: .9, fx: [{ measure: { x: .9, h: .3, text: '3.5CM', tagLeft: true } }] },
    { label: 'Easy slip-on', view: [.88, .30, .30], fx: [{ arrow: [.15, .1, .5, .4, -.2] }], icon: 'log-in' },
    { label: 'Outdoor styling', view: [.50, .60, .45], icon: 'sun' },
    { label: 'Waterproof & easy to clean', view: [.85, .60, .28], ...drops },
  ] },
  { id: 'MR8030', gender: 'female', usps: [
    { label: 'Durian pattern', scene: 'MR8030_1' },
    { label: 'Easy to clean', scene: 'MR8030_5', crop: [.56, .44, .84], icon: 'droplets' },
    { label: 'Soft & cushioned', scene: 'MR8030_3', crop: [.6, .55, .86], icon: 'cloud' },
    { label: 'Lightweight', scene: 'MR8030_4b', crop: [.5, .46, .8], icon: 'feather' },
  ] },
  { id: 'MR8031', gender: 'unisex', usps: [
    { label: 'Non-slip & breathable', view: [.18, .55, .36], icon: 'footprints' },
    { label: 'Indoor & outdoor', view: [.72, .50, .45], icon: 'house' },
    { label: 'Soft & cushioned', view: [.52, .60, .32], fx: [{ press: [.5, .55] }], icon: 'cloud' },
    { label: 'Waterproof & easy to clean', view: [.80, .36, .30], ...drops },
  ] },
  { id: 'MR8032', gender: 'female', usps: [
    { label: 'Triple straps', view: [.25, .33, .34] },
    { label: 'Easy slip-on', view: [.62, .73, .45], fx: [{ arrow: [.1, .1, .4, .4, -.2] }], icon: 'log-in' },
    { label: 'Non-slip sole', view: [.62, .25, .42], floor: 0, icon: 'footprints' },
    { label: 'Waterproof & easy to clean', view: [.55, .62, .32], ...drops },
  ] },
  { id: 'MR8033', gender: 'female', usps: [
    { label: 'Double straps', view: [.52, .45, .28] },
    { label: 'Easy slip-on', view: [.30, .50, .30], fx: [{ arrow: [.9, .1, .55, .45, .2] }], icon: 'log-in' },
    { label: 'Non-slip sole', view: [.75, .795, .30], floor: .8, icon: 'footprints' },
    { label: 'Waterproof & easy to clean', view: [.75, .55, .28], ...drops },
  ] },
  { id: 'MR8034', gender: 'female', B: { hero: [250, 515, 580, 150] }, usps: [
    { label: 'Korean minimalist design', view: [.44, .55, .34], icon: 'sparkle' },
    { label: 'Easy outfit pairing', view: [.16, .55, .32], icon: 'shirt' },
    { label: 'Non-slip sole', view: [.80, .585, .30], floor: .8, icon: 'footprints' },
    { label: 'Soft & cushioned', view: [.72, .55, .25], fx: [{ press: [.5, .45] }], icon: 'cloud' },
  ] },
  { id: 'MR8035', gender: 'male', usps: [
    { label: '4cm thick sole', view: [.82, .78, .38], bottom: .9, fx: [{ measure: { x: .92, h: .35, text: '4CM', tagLeft: true } }] },
    { label: 'Modern masculine look', view: [.24, .50, .55], icon: 'shirt' },
    { label: 'Soft & cushioned', scene: 'MR8035_5', crop: [.56, .5, .92], icon: 'cloud' },
    { label: 'Waterproof & easy to clean', scene: 'MR8035_4', icon: 'droplets' },
  ] },
];

for (const m of window.MODELS2) m.photo = `photos2/${m.id}.png`;
