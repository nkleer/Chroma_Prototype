// Option icons, batch o7: sport, music, play and animals.
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f = (n) => Math.round(n * 100) / 100;
// an ellipse centred on (cx, cy), turned by deg
const ell = (cx, cy, rx, ry, deg = 0) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg));
  const a = [cx - rx * c, cy - rx * s], b = [cx + rx * c, cy + rx * s];
  return `M${f(a[0])} ${f(a[1])}A${rx} ${ry} ${deg} 1 0 ${f(b[0])} ${f(b[1])}A${rx} ${ry} ${deg} 1 0 ${f(a[0])} ${f(a[1])}Z`;
};
// turn (deg about cx, cy), scale by k and move so (cx, cy) lands on (tx, ty)
const xf = (d, cx, cy, deg, k, tx, ty) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg));
  return d.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g, (m, x, y) => {
    const dx = x - cx, dy = y - cy;
    return `${f(tx + k * (dx * c - dy * s))} ${f(ty + k * (dx * s + dy * c))}`;
  });
};
const pt = (cx, cy, r, a) => [cx + Math.cos(rad(a)) * r, cy + Math.sin(rad(a)) * r];

const G = {
  // ---- sport ----
  'ball': (g, P) => {              // a football: a solid ball with its patch seams carved
    const k = Math.cos(rad(36));
    g.fill(P.circ(24, 24, 20.5)).cut(P.star(24, 24, 7.5, 7.5 * k, 5, -90), 1.9);
    for (let i = 0; i < 5; i++) {
      const a = -90 + 72 * i, c = pt(24, 24, 20, a);
      g.cut(`M${pt(24, 24, 7.5, a).map(f).join(' ')}L${pt(24, 24, 13, a).map(f).join(' ')}`, 1.9);
      g.cut(P.star(c[0], c[1], 7, 7 * k, 5, a + 180), 1.9);
    }
  },
  'running-shoe': (g, P) => {      // a trainer, side view: high heel collar, laces down the instep, a thick sole
    g.fill('M4.5 40C4 33 5 26 7 19.5L15 21C16.5 24.5 20 24.5 21.5 21L21 14L25.5 13.5C29 21 35 27 41 30C44.5 31.5 46 34.5 45.5 38V41.5C45.5 43 44.5 44 43 44H7C5.5 44 4.5 43 4.5 41.5Z')
      .cut('M4 37.5H46', 1.8)
      .cut('M24.5 21.5L29 17.5', 1.6).cut('M28.5 25L33 21', 1.6).cut('M33 28.5L37 24.5', 1.6);
  },
  'boot': (g, P) => {              // a heavy laced boot swung up in a kick, swing lines behind it
    const T = (d) => xf(d, 26, 24, -28, 0.92, 26, 21);
    g.fill(T('M11 4L24 4L24.5 21C30 22 37 23.5 41 26.5C44 28.5 45 32 44 35.5L10 35.5L10 22C10 15 10.5 9 11 4Z'))
      .cut(T('M18 10L26 10'), 1.7).cut(T('M18 15.5L26 15.5'), 1.7);
    g.fill(T('M9 37.5L44 37.5C44.5 40 43 42 40.5 42L9 42Z'));
    g.fill(T('M9 41L18 41L18 46L9 46Z'));
    for (const y of [20, 28, 36]) g.fill(T(`M${-6 + y / 6} ${y}L5 ${y}L5 ${y + 3}L${-6 + y / 6} ${y + 3}Z`));
  },
  'weights': (g, P) => {           // a dumbbell: a bar with two plates each end
    g.fill(P.cap(10, 24, 38, 24, 4.4));
    g.fill(P.rect(9.5, 10.5, 7, 27, 2)); g.fill(P.rect(31.5, 10.5, 7, 27, 2));
    g.fill(P.rect(3, 15.5, 8, 17, 2)); g.fill(P.rect(37, 15.5, 8, 17, 2));
    g.cut('M10.3 14V34', 1.5).cut('M37.7 14V34', 1.5);
  },
  'trophy': (g, P) => {            // a two-handled cup on a stem and plinth, a star carved in the bowl
    g.fill(P.arc(12, 14.5, 5.8, 90, 270, 3.2)); g.fill(P.arc(36, 14.5, 5.8, -90, 90, 3.2));
    g.fill('M11 5.5H37V15C37 24 31.5 29.5 24 29.5C16.5 29.5 11 24 11 15Z').cutFill(P.star(24, 16, 6, 2.5));
    g.fill(P.rect(21, 28, 6, 8)); g.fill(P.rect(16, 35.5, 16, 3.5, 1)); g.fill(P.rect(12, 40.5, 24, 5, 1.2));
  },
  'medal': (g, P) => {             // a medal disc hanging from a V of ribbon
    g.fill(P.poly([[8, 3], [17.5, 3], [24, 15.5], [30.5, 3], [40, 3], [29.5, 24.5], [18.5, 24.5]]))
      .cut('M12.8 3.5L21.5 21', 1.6).cut('M35.2 3.5L26.5 21', 1.6)
      .cutFill(P.circ(24, 33.5, 13.2));
    g.layer();
    g.fill(P.circ(24, 33.5, 11)).cut(P.circ(24, 33.5, 7.8), 1.5).cutFill(P.star(24, 33.8, 5.2, 2.2));
  },
  'whistle': (g, P) => {           // a coach's whistle: round chamber, mouthpiece, air slot, a ring for the cord
    g.fill(P.circ(29, 28, 13.5)); g.fill(P.rect(3, 14.5, 27, 10, 2.5));
    g.cutFill(P.rect(20.5, 12, 6.5, 6, 1.2)).cut(P.circ(29, 28, 6), 1.8);
    g.hole(P.circ(40.3, 16.7, 4.4), P.circ(40.3, 16.7, 1.9));
  },
  'flag': (g, P) => {              // a waving flag on a pole
    g.fill(P.cap(10, 6, 10, 44, 3.4)); g.fill(P.circ(10, 5, 3));
    g.fill('M12 8C18 4.5 24 10.5 31 8C35 6.5 39 6.5 43 8V28C39 26.5 35 26.5 31 28C24 30.5 18 24.5 12 28Z')
      .cut('M31 9.5V26', 1.6);
  },
  'chess-piece': (g, P) => {       // a chess knight: horse head on a collar and base
    g.fill('M14 35C14 29 17 26.5 20 24L10 26.5C7.5 27 6 25.5 6.5 23.5L8 18.5C10.5 14 13.5 11 17 9L19.5 3.5L23 7.5C31 8 36 15 36 24C36 28 35 31 34.5 35Z')
      .cutFill(P.circ(17, 14.5, 1.9)).cut('M29 10.5C32.5 14 34 19 34 24', 1.6);
    g.fill(P.rect(12, 36.5, 24, 3.6, 1.2)); g.fill(P.rect(9, 41, 30, 4.5, 1.5));
  },

  // ---- music ----
  'music-note': (g, P) => {        // two quavers joined by a beam
    g.fill(ell(12.5, 37, 6.4, 4.6, -22)); g.fill(ell(34.5, 32, 6.4, 4.6, -22));
    g.fill(P.rect(16.2, 11, 3.4, 26)); g.fill(P.rect(38.2, 6, 3.4, 26));
    g.fill(P.poly([[16.2, 8], [41.6, 3], [41.6, 9.5], [16.2, 14.5]]));
  },
  'record': (g, P) => {            // a record with its grooves and label, the tone arm resting on it
    g.fill(P.circ(21, 26, 18.5)).cut(P.circ(21, 26, 13.5), 1.4).cut(P.circ(21, 26, 9.5), 1.4)
      .cutFill(P.circ(21, 26, 1.8))
      .cut('M41 5V25L32 34', 7);
    g.layer();
    g.fill(P.circ(41, 6, 3.6)); g.fill(P.cap(41, 6, 41, 25, 3)); g.fill(P.cap(41, 25, 33, 33, 3)); g.fill(P.cap(34, 32, 30.5, 35.5, 5));
  },
  'piano': (g, P) => {             // an upright piano, front view: cabinet, keyboard with its black keys, legs and pedals
    g.fill(P.rect(5.5, 4, 37, 13.5, 2)).cut('M10 10H38', 1.6);
    g.fill(P.rect(3, 15.5, 4.2, 29.5, 1)); g.fill(P.rect(40.8, 15.5, 4.2, 29.5, 1));
    for (const x of [11.9, 16.8, 26.5, 31.4, 36.3]) g.fill(P.rect(x - 1.7, 17, 3.4, 9.5, 0.6));
    g.fill(P.rect(3, 30.5, 42, 4.4));
    g.fill(P.rect(15, 40.5, 18, 4.5, 1)).cut('M21 40V43', 1.6).cut('M27 40V43', 1.6);
  },
  'drum': (g, P) => {              // a side drum with its zigzag cords, two sticks crossed above
    g.fill(P.rect(6, 22, 36, 22, 2.5)).cut('M6 27H42', 1.8).cut('M6 39H42', 1.8)
      .cut('M9 27L15 39L21 27L27 39L33 27L39 39', 1.6);
    g.fill(P.cap(7, 4, 25, 17, 3)); g.fill(P.cap(41, 4, 23, 17, 3));
    g.fill(P.circ(25, 17, 2.6)); g.fill(P.circ(23, 17, 2.6));
  },
  'metronome': (g, P) => {         // a pyramid metronome, its arm and weight swung out to one side
    g.fill(P.poly([[18, 10], [30, 10], [38.5, 40], [9.5, 40]])).cut('M24 37L37.5 3.5', 6.6);
    g.fill(P.rect(6, 40.5, 36, 4.5, 1.2));
    g.layer();
    g.fill(P.cap(24, 37, 37.5, 3.5, 3)); g.fill(P.cap(33.5, 13.5, 35.4, 8.8, 7)); g.fill(P.circ(24, 36.5, 2.8));
  },
  'bell': (g, P) => {              // a bell ringing: crown loop, flared lip, clapper, two strokes of sound
    g.fill(P.arc(24, 7, 3.6, 180, 360, 2.8));
    g.fill('M24 7C31.5 7 34.5 12 34.5 19C34.5 27 36 31 42 34V38H6V34C12 31 13.5 27 13.5 19C13.5 12 16.5 7 24 7Z').cut('M8 33H40', 1.8);
    g.fill(P.circ(24, 42, 3.6));
    g.fill(P.cap(5, 11, 8, 17, 2.8)); g.fill(P.cap(43, 11, 40, 17, 2.8));
  },

  // ---- animals ----
  'dog': (g, P) => {               // a dog standing, tail up, ear down, a collar
    g.fill(P.rect(8, 19, 29, 12, 6));
    for (const x of [11, 17, 28.5, 34]) g.fill(P.cap(x, 27, x, 43, 3.8));
    g.fill(P.cap(10, 22, 5.5, 12, 3.4));
    g.fill(P.cap(32, 24, 36, 13, 8)).cut('M30.5 19L38 21', 1.6);
    g.fill(P.circ(37, 11.5, 6.2)); g.fill(P.cap(38.5, 14.5, 43.5, 15, 5.6)).cutFill(P.circ(38.5, 10, 1.4));
    g.layer(); g.fill(P.lens(34, 8, 31, 19, 1.6));
  },
  'fish': (g, P) => {              // a goldfish with a flowing tail, two bubbles
    g.fill(ell(20, 26, 13.5, 9.5)).cutFill(P.circ(12, 24, 1.8)).cut('M16.5 19C18.5 23 18.5 29 16.5 33', 1.6);
    g.fill('M31 26C35 20 39 13 45.5 12C42.5 18 41.5 22 43 26C41.5 30 42.5 34 45.5 40C39 39 35 32 31 26Z');
    g.fill('M14 18C16.5 12 23 10 29 13L28 19Z');
    g.fill(P.circ(6.5, 13, 2.4)); g.fill(P.circ(10.5, 6, 1.8));
  },
  'frog': (g, P) => {              // a frog sitting: crouched hind leg, eye up on top, front leg straight
    g.fill('M6 42C4 33 9 26.5 17 23.5C23 21 27 18.5 31 17C37 15 44.5 17 45 23C45.5 26 43.5 28 40 29C37 30 35.5 31.5 35 34L34 42Z')
      .cut('M7.5 38C8 31 13 27.5 18.5 27.5C24 27.5 27 31 27 35', 1.8).cut('M44.5 23.5C41.5 25.5 38.5 26 35 25.5', 1.6);
    g.fill(P.circ(33.5, 15, 6.2)).cutFill(P.circ(34.5, 14.5, 2.4));
    g.fill(P.cap(5.5, 43.5, 29, 43.5, 3.6)); g.fill(P.cap(36.5, 30, 38, 43, 3.6)); g.fill(P.cap(36, 43.5, 42.5, 43.5, 3.2));
  },
  'owl': (g, P) => {               // an owl on a branch: ear tufts, big round eyes, a beak
    g.fill('M11 4L18.5 11.5H29.5L37 4L37.5 19C38.5 31 34 40 24 40C14 40 9.5 31 10.5 19Z')
      .cutFill(P.circ(18.5, 19.5, 5.2)).cutFill(P.circ(29.5, 19.5, 5.2))
      .cut('M14 29C15 33.5 17.5 36 20 37', 1.6).cut('M34 29C33 33.5 30.5 36 28 37', 1.6);
    g.layer();
    g.fill(P.circ(18.5, 19.5, 2.4)); g.fill(P.circ(29.5, 19.5, 2.4)); g.fill(P.poly([[22, 24], [26, 24], [24, 28.5]]));
    g.fill(P.cap(3.5, 43.5, 44.5, 43.5, 3.6)); g.fill(P.cap(20, 39, 19, 43, 2.8)); g.fill(P.cap(28, 39, 29, 43, 2.8));
  },
  'beehive': (g, P) => {           // a domed straw skep on a board, a bee flying beside it
    g.fill('M4 40C4 24 10 9.5 20 9.5C30 9.5 36 24 36 40Z')
      .cut('M5 33H35', 1.8).cut('M7 26H33', 1.8).cut('M10 19H30', 1.8)
      .cutFill('M16.5 40.5V37.5A3.5 3.5 0 0 1 23.5 37.5V40.5Z');
    g.fill(P.rect(2.5, 41, 37, 4, 1.5));
    g.fill(ell(41, 19, 4.6, 3.2, 25)).cut('M40.5 15.5L39 21.5', 1.3);
    g.fill(P.lens(40, 15, 36, 9, 1.5)); g.fill(P.lens(42, 15.5, 45, 9.5, 1.5));
  },
  'tortoise': (g, P) => {          // a tortoise, side view: high plated shell, head out, stubby legs
    g.fill('M5.5 32C5.5 18 12.5 10 22 10C31.5 10 38.5 18 38.5 32Z')
      .cut('M5 24.5H39', 1.7).cut('M16 24.5L14.5 12', 1.7).cut('M28 24.5L29.5 12', 1.7).cut('M22 24.5V32', 1.7);
    g.fill(P.rect(3.5, 31, 37, 4.4, 2.2));
    g.fill(P.cap(37.5, 31, 41, 25.5, 5)); g.fill(ell(41.5, 24.5, 4.2, 3.4, -10)).cutFill(P.circ(42.5, 23.5, 1));
    g.fill(P.rect(9, 34, 6.5, 9, 2.6)); g.fill(P.rect(27.5, 34, 6.5, 9, 2.6));
    g.fill(P.poly([[4.5, 31.5], [1.5, 35.5], [6.5, 34.5]]));
  },
  'helmet': (g, P) => {            // a soldier's steel helmet, side view, the chin strap hanging below
    g.fill('M4 33C5 31 6 29.5 6.5 27C7 15 14 8 24.5 8C35 8 41.5 15 42 26C42.5 28.5 43.5 30 45.5 31L44.5 32.5C38 31.5 30 31.5 24 31.5C16 31.5 9 32 4 33Z')
      .cut('M7 26C17 24.5 32 24.5 42 25.5', 1.6);
    g.fill(P.arc(24, 31, 10, 0, 180, 2.8));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, fn]) => glyph(n, fn)) };
