// The six footprint kinds (v24 §3, chroma-ideas/next-table-2026-10-19/plan.md): one icon heads each stack.
const { glyph } = require('./glyph');

const G = {
  'footprint people': (g, P) => {  // three people joined: a small cast, each a head and shoulders, tied by lines
    g.fill(P.cap(24, 14, 11, 35, 3)); g.fill(P.cap(24, 14, 37, 35, 3)); g.fill(P.cap(11, 35, 37, 35, 3));
    g.layer();
    for (const [x, y] of [[24, 9], [10, 30], [38, 30]]) {
      g.fill(P.circ(x, y, 4.6)); g.fill(`M${x - 7.5} ${y + 13}C${x - 7.5} ${y + 7.5} ${x - 4} ${y + 5.5} ${x} ${y + 5.5}C${x + 4} ${y + 5.5} ${x + 7.5} ${y + 7.5} ${x + 7.5} ${y + 13}Z`);
    }
  },
  'footprint places': (g, P) => {  // a map pin with a round window
    g.hole('M24 45C17 35.5 9.5 27 9.5 18.5C9.5 10.5 16 4 24 4C32 4 38.5 10.5 38.5 18.5C38.5 27 31 35.5 24 45Z', P.circ(24, 18.5, 6));
  },
  'footprint means': (g, P) => {   // a full basket on its arm: what a life has to draw on
    g.fill(P.arc(24, 22, 14, 180, 360, 3.6));
    g.layer();
    g.fill(P.circ(16.5, 21.5, 5)); g.fill(P.circ(31.5, 21.5, 5)); g.fill(P.circ(24, 18.5, 5.5));
    g.layer();
    g.fill(P.poly([[4.5, 24], [43.5, 24], [38.5, 44], [9.5, 44]])).cut('M9 31H39', 2).cut('M11 37.5H37', 2);
  },
  'footprint marks': (g, P) => {   // a tally: four strokes and the bar across them
    for (const x of [11, 19, 27, 35]) g.fill(P.cap(x, 9, x + 1.5, 39, 4.4));
    g.layer(); g.fill(P.cap(5, 32, 43, 15, 4.4));
  },
  'footprint doors': (g, P) => {   // an open archway with the path running on through it
    g.hole('M6 45V21C6 11 14 4 24 4C34 4 42 11 42 21V45Z', 'M13 45V22C13 15.5 18 11 24 11C30 11 35 15.5 35 22V45Z');
    g.fill(P.poly([[21.5, 27], [26.5, 27], [33, 45], [15, 45]]));
  },
  'footprint lessons': (g, P) => { // the colour wheel in five parts, one part drawn out: a lesson taken from one colour
    const rad = (d) => d * Math.PI / 180, pt = (cx, cy, rr, d) => `${(cx + Math.cos(rad(d)) * rr).toFixed(2)} ${(cy + Math.sin(rad(d)) * rr).toFixed(2)}`;
    const slice = (cx, cy, rr, a0, a1) => `M${cx} ${cy}L${pt(cx, cy, rr, a0)}A${rr} ${rr} 0 0 1 ${pt(cx, cy, rr, a1)}Z`;
    const [cx, cy, rr] = [22.5, 26, 17];
    for (let i = 1; i < 5; i++) g.fill(slice(cx, cy, rr, -126 + i * 72 + 3.2, -126 + (i + 1) * 72 - 3.2));
    const dx = Math.cos(rad(-90)) * 5.5 + 3.5, dy = Math.sin(rad(-90)) * 5.5;
    g.fill(slice(cx + dx, cy + dy, rr, -126 + 3.2, -54 - 3.2));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
