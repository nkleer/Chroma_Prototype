// Option icons, batch B: "a long dark season" (calendar .. talk) and "falling in love" (question .. locked-heart).
const { glyph, P } = require('./glyph');

const HEART = 'M24 42C10 32 4 25 4 17C4 10 9 6 15 6C19 6 22 8 24 11C26 8 29 6 33 6C39 6 44 10 44 17C44 25 38 32 24 42Z';
// the heart path scaled about (24, 24) by s and moved by (dx, dy)
const heart = (s, dx = 0, dy = 0) => HEART.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g,
  (m, x, y) => `${Math.round((24 + (x - 24) * s + dx) * 100) / 100} ${Math.round((24 + (y - 24) * s + dy) * 100) / 100}`);
// a wavy vertical line drawn as a chain of round-ended strokes
const wave = (g, P, x0, y0, y1, amp, w, turns = 1) => {
  const n = 24, pts = [];
  for (let i = 0; i <= n; i++) { const t = i / n; pts.push([x0 + amp * Math.sin(t * turns * 2 * Math.PI), y0 + (y1 - y0) * t]); }
  for (let i = 0; i < n; i++) g.fill(P.cap(...pts[i], ...pts[i + 1], w));
};

const G = {
  // ---- a long dark season ----
  'calendar': (g, P) => {          // a wall calendar page, held by two rings
    g.fill(P.rect(6, 9, 36, 35, 3)).cut('M6 18H42', 2);
    for (const y of [22.5, 29.5, 36.5]) for (const x of [11, 21.5, 32]) g.cutFill(P.rect(x, y, 5, 4.2, 0.8));
    g.cutFill(P.rect(12, 7, 6, 8, 3)).cutFill(P.rect(30, 7, 6, 8, 3));
    g.layer(); g.fill(P.cap(15, 5, 15, 12, 3.2)); g.fill(P.cap(33, 5, 33, 12, 3.2));
  },
  'diary': (g, P) => {             // a closed notebook: spine, a label on the cover, a ribbon marker hanging out
    g.fill(P.poly([[24.5, 38], [31.5, 38], [31.5, 46], [28, 42.5], [24.5, 46]]));
    g.layer();
    g.fill(P.rect(8, 3, 31, 38, 3)).cut('M14 3V41', 2).cut(P.rect(19.5, 10, 13.5, 8, 1), 1.8);
  },
  'headphones': (g, P) => {
    g.fill(P.arc(24, 26, 17, 180, 360, 4));
    g.fill(P.rect(3.5, 24, 10, 19, 4)).cut('M10 27.5V39.5', 1.8);
    g.fill(P.rect(34.5, 24, 10, 19, 4)).cut('M38 27.5V39.5', 1.8);
  },
  'bed': (g, P) => {               // a bed, side view, pillow at the head
    g.fill(P.rect(3.5, 11, 5, 34, 1.5)); g.fill(P.rect(39.5, 23, 5, 22, 1.5));
    g.fill(P.rect(7, 27, 34, 11, 1.5)).cut('M20 27V38', 1.8);
    g.fill(P.rect(10, 19, 12, 6.5, 3.2));
  },
  'stethoscope': (g, P) => {
    g.fill(P.cap(9, 6, 9, 17, 3.6)); g.fill(P.cap(29, 6, 29, 17, 3.6));
    g.fill(P.cap(9, 5, 13, 3.8, 3.6)); g.fill(P.cap(29, 5, 25, 3.8, 3.6));
    g.fill(P.arc(19, 17, 10, 0, 180, 3.6));
    g.fill(P.cap(19, 27, 19, 32, 3.6)); g.fill(P.arc(27, 32, 8, 0, 180, 3.6));
    g.fill(P.cap(35, 32, 35, 28, 3.6));
    g.fill(P.circ(35, 23.5, 7.5)).cut(P.circ(35, 23.5, 4), 1.8);
  },
  'scissors': (g, P) => {          // open scissors, blades up
    g.hole(P.circ(14, 37, 7), P.circ(14, 37, 3.6)); g.hole(P.circ(34, 37, 7), P.circ(34, 37, 3.6));
    g.fill(P.cap(17.5, 31.5, 24, 22, 4)); g.fill(P.cap(30.5, 31.5, 24, 22, 4));
    g.fill(P.lens(24.5, 24, 35, 4, 3.2)); g.fill(P.lens(23.5, 24, 13, 4, 3.2));
    g.cutFill(P.circ(24, 21.5, 1.6));
  },
  'talk': (g, P) => {              // two speech bubbles, one over the other
    g.fill(P.rect(3, 5, 28, 19, 8)); g.fill(P.poly([[8, 20], [6, 30], [16, 22]]))
      .cut(P.rect(17, 18, 28, 19, 8), 2.8).cut('M38 33L41 43L30 36', 2.8);
    g.layer(); g.fill(P.rect(17, 18, 28, 19, 8)); g.fill(P.poly([[33, 34], [41, 43], [38, 30]]))
      .cutFill(P.circ(24.5, 27.5, 2)).cutFill(P.circ(31, 27.5, 2)).cutFill(P.circ(37.5, 27.5, 2));
  },
  // ---- falling in love ----
  'question': (g, P) => {          // one speech bubble asking
    g.fill(P.rect(4, 4, 40, 32, 13)); g.fill(P.poly([[10, 30], [7, 45], [22, 34]]));
    g.cutFill(P.arc(24, 14.5, 5, 190, 400, 3.4)).cutFill(P.cap(27.8, 17.7, 24, 21.5, 3.4)).cutFill(P.cap(24, 21.5, 24, 23.5, 3.4));
    g.cutFill(P.circ(24, 29, 2.1));
  },
  'wallet': (g, P) => {            // a billfold with a note showing and the clasp tab shut
    g.fill(P.poly([[8, 9.5], [31, 5.5], [33, 17], [10, 21]])).cut('M5 13H36', 2);
    g.layer(); g.fill(P.rect(4, 13, 36, 30, 4)).cutFill(P.rect(24.5, 20.5, 23, 15, 4.5));
    g.layer(); g.fill(P.rect(26.5, 22.5, 18.5, 11, 3.5)).cutFill(P.circ(37.5, 28, 2));
  },
  'pot': (g, P) => {               // a steaming cooking pot
    for (const x of [16, 24, 32]) wave(g, P, x, 17, 4, 1.8, 3);
    g.layer();
    g.fill(P.rect(5, 21, 38, 5, 1.8)); g.fill('M8 25H40V36C40 41 36.5 44 31.5 44H16.5C11.5 44 8 41 8 36Z').cut('M8 26.5H40', 1.8);
    g.fill(P.cap(3, 30, 9, 30, 3.6)); g.fill(P.cap(39, 30, 45, 30, 3.6));
  },
  'domino-mask': (g, P) => {       // a masquerade eye mask, corners swept up
    g.hole('M3 12.5C9 18.5 16 14.5 24 18.5C32 14.5 39 18.5 45 12.5C46 25.5 42 35.5 34 35.5C29 35.5 27 32.5 24 29.5C21 32.5 19 35.5 14 35.5C6 35.5 2 25.5 3 12.5Z',
      P.lens(9.5, 23.5, 19.5, 25, 3), P.lens(28.5, 25, 38.5, 23.5, 3));
  },
  'locked-heart': (g, P) => {      // a heart with a padlock hung on it
    g.fill(heart(0.92, 0, -3)).cutFill(P.rect(22.5, 23, 21, 22, 4)).cut(P.arc(33, 27.5, 5.2, 180, 360, 0.1), 7.2);
    g.layer();
    g.fill(P.arc(33, 28, 5.2, 180, 360, 3)); g.fill(P.rect(24.5, 27.5, 17, 16, 2.5)).cutFill(P.circ(33, 33.5, 2)).cutFill(P.rect(32, 33.5, 2, 5.5, 0.6));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
