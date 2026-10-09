// The five shadow states (implementation list item 2, light and shadow per colour; chroma-ideas/shadows-mechanics.md):
// the state word a colour's shadow shows in the crest once its force passes .5. White rigid, Blue indecisive, Black
// ruthless, Red reckless, Green stuck. Each shows the colour's way overused, never a judgement and never harm to a person.
const { glyph, P } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const at = (cx, cy, r, a) => [cx + Math.cos(rad(a)) * r, cy + Math.sin(rad(a)) * r];
// an arrowhead: tip, the direction it points (deg, 0 = right, clockwise), length and half-width at its base
const head = (tip, deg, len, half) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg)), bx = tip[0] - c * len, by = tip[1] - s * len;
  return P.poly([tip, [bx - s * half, by + c * half], [bx + s * half, by - c * half]]);
};
// a four-pointed spark of radius R; k sets how full its sides are
const spark = (cx, cy, R, k) => `M${cx} ${cy - R}Q${cx + R * k} ${cy - R * k} ${cx + R} ${cy}Q${cx + R * k} ${cy + R * k} ${cx} ${cy + R}`
  + `Q${cx - R * k} ${cy + R * k} ${cx - R} ${cy}Q${cx - R * k} ${cy - R * k} ${cx} ${cy - R}Z`;

const G = {
  'shadow-rigid': (g, P) => {      // White: a barred gate shut tight, a heavy beam across it in its brackets
    for (const x of [10, 21.5, 33]) g.fill(P.rect(x, 7, 5.5, 34));
    g.fill(P.rect(7, 3.5, 34.5, 5, 1)).fill(P.rect(7, 39.5, 34.5, 5, 1));
    g.cutFill(P.rect(0, 18, 48, 12));
    g.layer();
    g.fill(P.rect(2.5, 20, 43, 8, 1.4)).cut('M9.5 24H38.5', 1.5);
    g.fill(P.rect(3.5, 15.5, 5.5, 17, 1)).fill(P.rect(39, 15.5, 5.5, 17, 1));
  },
  'shadow-indecisive': (g, P) => { // Blue: a question going round in circles, two arrows chasing each other around it
    for (const a0 of [-75, 105]) {
      g.fill(P.arc(24, 24, 17, a0, a0 + 128, 4.2));
      const tip = at(24, 24, 17, a0 + 150);
      g.fill(head(tip, a0 + 150 + 90 - 9, 8.5, 5.6));
    }
    g.fill(P.arc(24, 19.5, 4.6, 190, 400, 3.4)).fill(P.cap(27.4, 22.6, 24, 25.8, 3.4)).fill(P.cap(24, 25.8, 24, 27.6, 3.4));
    g.fill(P.circ(24, 32.6, 2.1));
  },
  'shadow-ruthless': (g, P) => {   // Black: a shark's fin cutting through the water, its spray ahead of it
    g.fill('M9 34.5C14 24 23.5 12 40 5C34.5 13.5 32 24 35.5 34.5Z');
    g.fill('M3 37.5C7 37.5 8 35 11.5 35C15 35 16 37.5 19.5 37.5C23 37.5 24 35 27.5 35C31 35 32 37.5 35.5 37.5C39 37.5 40 35 43.5 35H45V40.5H43.5C40.5 40.5 39.5 43 35.5 43C31.5 43 30.5 40.5 27.5 40.5C24.5 40.5 23.5 43 19.5 43C15.5 43 14.5 40.5 11.5 40.5C8.5 40.5 7.5 43 3 43Z');
    g.fill(P.arc(7, 34, 4.5, 200, 265, 2.4)).fill(P.arc(4, 30, 4.5, 200, 265, 2.4));
  },
  'shadow-reckless': (g, P) => {   // Red: a firecracker's fuse already lit, its spark flying ahead of the curl
    const f = (x, y) => { const c = Math.cos(rad(-35)), s = Math.sin(rad(-35)); return [12 + x * c - y * s, 38 + x * s + y * c]; };
    g.fill(P.poly([f(-9, -5.5), f(9, -5.5), f(9, 5.5), f(-9, 5.5)])).cut(`M${f(4, -7).join(' ')}L${f(4, 7).join(' ')}`, 1.5);
    g.fill('M18.6 31.4C20 29 18 25 21 22.5C24 20 27 23.5 29.5 21L31.6 22.8C28.4 26.4 25.2 23.6 23.6 25.2C21.8 27 24.4 31.4 21.4 34.4Z');
    g.fill(spark(34.5, 14.5, 11.5, 0.27)).fill(P.circ(44, 4.5, 1.9)).fill(P.circ(44.5, 26, 1.7)).fill(P.circ(23.5, 5, 1.6));
  },
  'shadow-stuck': (g, P) => {      // Green: a cartwheel sunk to its hub in a deep rut, mud heaped either side
    const TOP = 'M2 34C5.5 34 7 29.5 10.5 29.5C13.5 29.5 14 33 16 34.5H32C34 33 34.5 29.5 37.5 29.5C41 29.5 42.5 34 46 34';
    g.hole(P.circ(24, 27, 16.5), P.circ(24, 27, 12.5)).fill(P.circ(24, 27, 3.8));
    for (const a of [0, 60, 120, 180, 240, 300]) g.fill(P.cap(...at(24, 27, 3, a), ...at(24, 27, 13, a), 2.8));
    g.cutFill(TOP + 'V48H2Z').cut(TOP, 3.4);
    g.layer();
    g.fill(TOP + 'V45H2Z').cut('M8 39.5H18M30 39.5H40', 1.5).cut('M14 42.5H34', 1.5);
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
