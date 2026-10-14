// USP copy for each model, taken from "Marco Rocco USP" (one entry per model).
// title/subtitle: the headline; highlights: the 3 model-specific callouts;
// sticker: the round gold badge on the product [small top line, big line, small bottom line];
// unisex/colours: shown in the pill under the product;
// core: the 6 shared benefits in the bottom band (keys of CORE below);
// bg: background gradient [top, bottom], sampled from the model's main (BAU) image.

window.CORE = {
  durable:    { icon: 'shield-check', label: 'Durable' },
  eva:        { icon: 'layers',       label: 'EVA Material' },
  clean:      { icon: 'sparkles',     label: 'Easy to Clean' },
  light:      { icon: 'feather',      label: 'Lightweight' },
  soft:       { icon: 'cloud',        label: 'Soft & Cushioned' },
  waterproof: { icon: 'umbrella',     label: 'Waterproof' },
  nonslip:    { icon: 'footprints',   label: 'Non-Slip Sole' },
};

const CORE_DEFAULT = ['durable', 'eva', 'clean', 'light', 'soft', 'waterproof'];

window.MODELS = [
  {
    id: 'MR8012', title: 'Simple Wave Design', subtitle: 'Suits different daily occasions',
    sticker: ['', 'UNISEX', 'FOR ALL'],
    highlights: [
      { icon: 'footprints', text: 'Non-slip sole design' },
      { icon: 'wind', text: 'Breathable' },
      { icon: 'shield', text: 'Anti-slip efficiency' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#E7E1DA', '#C3BBB1'],
  },
  {
    id: 'MR8013', title: 'Trendy Chunky Sole', subtitle: 'Boost your height 4cm+',
    sticker: ['BOOST', '4CM+', 'HEIGHT'],
    highlights: [
      { icon: 'ruler', text: 'Thick sole, 4cm+ height boost' },
      { icon: 'footprints', text: 'Anti-slip efficiency' },
      { icon: 'star', text: 'Trendy chunky look' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#D5CDC7', '#AFA59D'],
  },
  {
    id: 'MR8015', title: 'Stylish Striped Pattern', subtitle: 'A versatile casual look',
    sticker: ['', 'UNISEX', 'FOR ALL'],
    highlights: [
      { icon: 'align-justify', text: 'Stylish striped pattern' },
      { icon: 'log-in', text: 'Easy slip-on style' },
      { icon: 'shirt', text: 'Versatile casual look' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#E2D5C9', '#AFA59C'],
  },
  {
    id: 'MR8017', title: '4cm Chunky Sole', subtitle: 'Convenient for daily routines',
    sticker: ['', '4CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: '4cm thick sole, chunky silhouette' },
      { icon: 'log-in', text: 'Easy slip-on style' },
      { icon: 'sparkle', text: 'Half-slipper design' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#CEC8C1', '#B3AAA1'],
  },
  {
    id: 'MR8018', title: '4cm Chunky Sole', subtitle: 'Easy to put on & take off',
    sticker: ['', '4CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: '4cm thick sole, chunky silhouette' },
      { icon: 'footprints', text: 'Non-slip outsole' },
      { icon: 'log-in', text: 'Slide-in design, easy on & off' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#D2CBC4', '#B7AEA5'],
  },
  {
    id: 'MR8021', title: 'Woven-Style Texture', subtitle: 'A stylish upper that stands out',
    sticker: ['', 'WOVEN', 'STYLE'],
    highlights: [
      { icon: 'grid-3x3', text: 'Woven-style pattern' },
      { icon: 'sparkle', text: 'Stylish upper texture' },
      { icon: 'log-in', text: 'Slide-in sandal design' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#DBBDB8', '#BE928C'],
  },
  {
    id: 'MR8022', title: '5cm Thick Sole', subtitle: 'From fashion to everyday',
    sticker: ['', '5CM', 'THICK SOLE'],
    highlights: [
      { icon: 'shuffle', text: 'Criss-cross straps' },
      { icon: 'square', text: 'Decorative square buckle' },
      { icon: 'ruler', text: '5cm thick sole' },
    ],
    unisex: false, colours: false, core: CORE_DEFAULT, bg: ['#ECEAE8', '#C4C0BC'],
  },
  {
    id: 'MR8024', title: 'Rain-Ready Style', subtitle: 'Fashion look meets rain-ready function',
    sticker: ['', 'RAIN', 'READY'],
    highlights: [
      { icon: 'cloud-rain', text: 'Waterproof boot design' },
      { icon: 'shield', text: 'More coverage than slippers or sandals' },
      { icon: 'shirt', text: 'Thick sole, easy outfit pairing' },
    ],
    unisex: false, colours: false, core: CORE_DEFAULT, bg: ['#F2DAD5', '#D3ACA6'],
  },
  {
    id: 'MR8026', title: 'Up to 7.5cm Sole', subtitle: 'Chunky but lightweight',
    sticker: ['UP TO', '7.5CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: 'Up to 7.5cm thick sole' },
      { icon: 'heart', text: 'Customisable charms' },
      { icon: 'sun', text: 'Suits casual & everyday styling' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#DEC4BF', '#BE968F'],
  },
  {
    id: 'MR8027', title: '5.5cm Thick Sole', subtitle: 'With a stylish wave pattern',
    sticker: ['', '5.5CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: '5.5cm thick sole' },
      { icon: 'waves', text: 'Stylish wave pattern' },
      { icon: 'heart', text: 'Customisable charm' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#E4CAC3', '#BF958B'],
  },
  {
    id: 'MR8028', title: '2-in-1 Convertible', subtitle: '2 ways to wear',
    sticker: ['', '2-IN-1', 'DESIGN'],
    highlights: [
      { icon: 'repeat-2', text: '2-in-1 convertible design' },
      { icon: 'sparkle', text: 'Heel-strap style' },
      { icon: 'log-in', text: 'Easy slip-on' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#ECE6E0', '#C2BAB0'],
  },
  {
    id: 'MR8029', title: '3.5cm Thick Sole', subtitle: 'Open-back half-slipper style',
    sticker: ['', '3.5CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: '3.5cm thick sole' },
      { icon: 'log-in', text: 'Open-back, easy to slip on' },
      { icon: 'sun', text: 'Suits outdoor sandal styling' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#CDC5BE', '#B2A89F'],
  },
  {
    id: 'MR8030', title: 'For Durian Lovers!', subtitle: 'Cute Malaysian-style design',
    sticker: ['FOR', 'DURIAN', 'LOVERS'],
    highlights: [
      { icon: 'heart', text: 'Durian pattern' },
      { icon: 'map-pin', text: 'Malaysian style' },
      { icon: 'shirt', text: 'Cute look, easy to pair with outfits' },
    ],
    // No waterproof claim for MR8030 in the USP sheet, so show its non-slip sole instead.
    unisex: false, colours: true,
    core: ['durable', 'eva', 'clean', 'light', 'soft', 'nonslip'], bg: ['#EDDBD7', '#D4AFAA'],
  },
  {
    id: 'MR8031', title: 'Simple Everyday Look', subtitle: 'Easy to match casual outfits',
    sticker: ['', 'UNISEX', 'FOR ALL'],
    highlights: [
      { icon: 'footprints', text: 'Non-slip, breathable sole' },
      { icon: 'shirt', text: 'Easy to match casual outfits' },
      { icon: 'house', text: 'Indoor & outdoor activities' },
    ],
    unisex: true, colours: true, core: CORE_DEFAULT, bg: ['#D7D2CA', '#B6ADA3'],
  },
  {
    id: 'MR8032', title: 'Triple Strap Style', subtitle: 'Casual look, easy slip-on',
    sticker: ['', 'TRIPLE', 'STRAPS'],
    highlights: [
      { icon: 'tally-3', text: 'Triple straps, casual look' },
      { icon: 'log-in', text: 'Easy slip-on style' },
      { icon: 'footprints', text: 'Non-slip, breathable sole' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#EAD7D3', '#CDACA6'],
  },
  {
    id: 'MR8033', title: 'Double Strap Style', subtitle: 'Easy slip-on comfort',
    sticker: ['', 'DOUBLE', 'STRAPS'],
    highlights: [
      { icon: 'tally-2', text: 'Double straps' },
      { icon: 'log-in', text: 'Easy slip-on style' },
      { icon: 'footprints', text: 'Non-slip, breathable sole' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#E0C2BD', '#BB918B'],
  },
  {
    id: 'MR8034', title: 'Korean Minimalist', subtitle: 'Easy to pair with daily outfits',
    sticker: ['', 'KOREAN', 'MINIMALIST'],
    highlights: [
      { icon: 'sparkle', text: 'Korean minimalist design' },
      { icon: 'shirt', text: 'Easy to pair with daily outfits' },
      { icon: 'footprints', text: 'Non-slip, breathable sole' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#F0DCD9', '#CCA7A3'],
  },
  {
    id: 'MR8035', title: 'Modern Masculine Look', subtitle: 'With a 4cm thick sole',
    sticker: ['', '4CM', 'THICK SOLE'],
    highlights: [
      { icon: 'ruler', text: '4cm thick sole' },
      { icon: 'star', text: 'Modern masculine look' },
      { icon: 'footprints', text: 'Non-slip, breathable sole' },
    ],
    unisex: false, colours: true, core: CORE_DEFAULT, bg: ['#DCE7F0', '#96A6B5'],
  },
];
