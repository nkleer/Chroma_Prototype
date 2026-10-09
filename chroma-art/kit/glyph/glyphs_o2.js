// Batch o2: gestures, hands, heads and a few personal objects, for option rows.
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f2 = (n) => Math.round(n * 100) / 100;
// a path written in local coordinates, scaled by s, turned by deg and moved to (cx, cy): pass "x,y" pairs as numbers in the template
const local = (cx, cy, deg, s, cmds) => cmds.replace(/(-?[\d.]+) (-?[\d.]+)/g, (m, x, y) => {
  const c = Math.cos(rad(deg)), sn = Math.sin(rad(deg)), X = +x * s, Y = +y * s;
  return `${f2(cx + X * c - Y * sn)} ${f2(cy + X * sn + Y * c)}`;
});

const G = {
  'pointing': (g, P) => {          // a hand pointing right: cuff, index finger out, three fingers curled under, thumb on top
    g.fill(P.rect(3, 17, 6.5, 22, 1.6));
    g.fill(P.rect(11.5, 15.5, 15, 24, 5));
    g.fill(P.cap(18, 21, 44, 21, 6));
    for (const [y, x] of [[27.5, 31], [33, 30], [38, 27.5]]) g.fill(P.cap(18, y, x, y, 5.4));
    g.cut('M21 24.6H35', 1.6).cut('M21 30.3H33', 1.6).cut('M21 35.6H30', 1.6);
    g.layer(); g.fill(P.cap(14, 14.5, 27, 14, 5)).cut('M14 17.2H28', 1.4);
  },
  'whisper': (g, P) => {           // one head in profile whispers behind a cupped hand into a second head's ear
    g.fill('M6 45V36.5C3.5 33.5 2.5 29.5 2.5 24C2.5 14.5 8.5 8.5 16 8.5C22 8.5 26 12.5 26 18L28.5 22.5L26 23.5V28C26 31 24 33 20.5 33V45Z')
      .cut(P.arc(35, 24, 6.5, 115, 240, 4), 2.4).cut(P.cap(32.2, 29.9, 28.5, 37, 4.4), 2.4);
    g.layer(); g.fill(P.arc(35, 24, 6.5, 115, 240, 4)); g.fill(P.cap(32.2, 29.9, 28.5, 37, 4.4));
    g.fill(P.circ(40, 18.5, 6)); g.fill('M33.5 45C33.5 34 36 29 40.5 29C45 29 46 34 46 45Z');
  },
  'cross-arms': (g, P) => {        // standing firm: feet planted apart, arms folded across the chest
    g.fill(P.circ(24, 7.5, 5.8));
    g.fill(P.rect(15.5, 15, 17, 17, 5.5)).cut('M11 28L31 20.5', 7.6).cut('M37 28L17 20.5', 7.6);
    g.fill(P.cap(20.5, 30, 14, 44.5, 5.8)).fill(P.cap(27.5, 30, 34, 44.5, 5.8));
    g.layer(); g.fill(P.cap(11, 28, 31, 20.5, 5.2)).fill(P.cap(37, 28, 17, 20.5, 5.2));
  },
  'finger-on-lips': (g, P) => {    // a head in profile, a finger raised to the lips, the fist below the chin
    g.fill('M6 45V36.5C3 33.5 1.5 29 1.5 23C1.5 12.5 8.5 6 17.5 6C25.5 6 30 11.5 30 18L33 23.5L30 24.5V29C30 32.5 27.5 35 23.5 35V45Z')
      .cut(P.cap(35.5, 31, 35.5, 16.5, 5.4), 3.4).cut(P.rect(30, 28.5, 14.5, 12.5, 5), 3.4).cut(P.cap(37.5, 38, 38, 46, 8), 3.4);
    g.layer(); g.fill(P.cap(35.5, 31, 35.5, 16.5, 5.4)); g.fill(P.rect(30, 28.5, 14.5, 12.5, 5)).cut('M39 32.8H45', 1.5).cut('M39 36.8H45', 1.5);
    g.fill(P.cap(37.5, 38, 38, 46, 8));
  },
  'holding-hands': (g, P) => {     // a grown-up and a child walking hand in hand
    g.fill(P.circ(14, 8, 5.2)); g.fill(P.rect(8, 15.5, 12, 29.5, 5.5));
    g.fill(P.circ(35, 20, 4.2)); g.fill(P.rect(30, 26.5, 10, 18.5, 4.5));
    g.fill(P.cap(18.5, 19, 25.5, 30, 3.2)); g.fill(P.cap(31.5, 29, 26, 31, 3)); g.fill(P.circ(26, 31, 2.8));
  },
  'thumbs-up': (g, P) => {         // a fist, thumb up
    g.fill(P.rect(3.5, 23, 7, 21, 1.6));
    g.fill(P.rect(12.5, 21, 15, 23, 4.5));
    for (const [y, x] of [[24, 36], [29.5, 37], [35, 36], [40.5, 34]]) g.fill(P.cap(20, y, x, y, 5.6));
    g.cut('M23 26.8H36', 1.5).cut('M23 32.3H36', 1.5).cut('M23 37.8H34', 1.5);
    g.fill(P.cap(17.5, 23, 20, 6, 7)).cut('M23 20.5L21.6 12', 1.5);
  },
  'hand-on-heart': (g, P) => {     // a hand raised for a vow, fingers together, a heart carved in the palm
    g.fill(P.rect(13.5, 5, 21, 33, 6)); g.fill(P.rect(16.5, 35, 15, 10, 2));
    g.fill(P.cap(15, 32, 6.5, 20.5, 5.6));
    g.cut('M19.2 6V15', 1.4).cut('M24 5V15', 1.4).cut('M28.8 6V15', 1.4);
    g.cutFill('M24 34C18.5 30.2 16 27.4 16 24.2C16 21.5 17.9 19.8 20.1 19.8C21.8 19.8 23.2 20.8 24 22.3C24.8 20.8 26.2 19.8 27.9 19.8C30.1 19.8 32 21.5 32 24.2C32 27.4 29.5 30.2 24 34Z');
  },
  'ear': (g, P) => {               // an ear, its curl carved in
    g.fill('M15 20C15 10 22 4 29 4C37 4 42 10 42 18C42 24 39 27 36 30C33 33 32.5 36 31.5 39C30 43.5 26.5 45.5 22.5 45C18.5 44.5 16 41.5 16 38V33C15.3 29 15 25 15 20Z')
      .cut('M21 21C21 14 25 10 29.5 10C34 10 36.5 13.5 36.5 17.5C36.5 21 34 23 31.5 25C29 27 28 29.5 28 33', 2.2)
      .cut('M25.5 23C25.5 19 27.5 16.5 30 16.5', 2);
  },
  'teardrop': (g, P) => {          // a single large teardrop with a gleam
    g.fill('M24 3C30.5 13 37.5 21.5 37.5 31C37.5 39.5 31.5 45 24 45C16.5 45 10.5 39.5 10.5 31C10.5 21.5 17.5 13 24 3Z')
      .cut('M16.5 31C16.5 35.5 19 38.5 23 39', 2.2);
  },
  'footsteps': (g, P) => {         // shoe prints walking on, left then right
    const SOLE = 'M-5 -6C-5.5 -12 -3 -15 0 -15C3 -15 5.5 -12 5 -6C4.7 -3 3.2 -1 3.2 2C3.2 4 4.2 5 4.2 8C4.2 11 2.2 13 0 13C-2.2 13 -4.2 11 -4.2 8C-4.2 5 -3.2 4 -3.2 2C-3.2 -1 -4.7 -3 -5 -6Z';
    for (const [cx, cy, a] of [[15.5, 31, -10], [32.5, 17.5, 10]]) g.fill(local(cx, cy, a, 1, SOLE)).cut(local(cx, cy, a, 1, 'M-5 3.6L5 3.6'), 1.8);
  },
  'mirror': (g, P) => {            // a hand mirror, its glass catching the light
    g.fill('M24 2A14 15 0 1 0 24 32A14 15 0 1 0 24 2Z')
      .cut('M24 6.2A9.8 10.8 0 1 0 24 27.8A9.8 10.8 0 1 0 24 6.2Z', 1.8).cut('M18.5 19.5L25 11.5', 2);
    g.fill(P.rect(19.5, 30.5, 9, 5, 1.8)); g.fill(P.cap(24, 34, 24, 44.5, 5.6));
  },
  'microphone': (g, P) => {        // a microphone in its cradle, on a short stand
    g.fill(P.rect(16.5, 3, 15, 25, 7.5)).cut('M17 11H24', 1.6).cut('M17 16H24', 1.6).cut('M17 21H24', 1.6);
    g.fill(P.arc(24, 18, 12, 0, 180, 3.2)); g.fill(P.cap(24, 31, 24, 41, 3.4)); g.fill(P.cap(15, 43, 33, 43, 3.6));
  },
  'phone': (g, P) => {             // an old desk telephone, the handset in its cradle
    g.fill('M5 17C5 9.5 10 6 17 6H31C38 6 43 9.5 43 17V19H35V14H13V19H5Z');
    g.fill('M14 21H34L42 42C42.5 43.5 41.5 45 40 45H8C6.5 45 5.5 43.5 6 42Z').cut(P.circ(24, 33, 6.2), 2.4).cutFill(P.circ(24, 33, 1.8));
  },
  'screen': (g, P) => {            // an old television with rabbit-ear aerials
    g.fill(P.cap(24, 13, 14.5, 3.5, 2.8)); g.fill(P.cap(24, 13, 33.5, 3.5, 2.8));
    g.fill(P.rect(4, 12.5, 40, 28.5, 4)).cut(P.rect(8.5, 17, 24, 19.5, 4), 2.2).cutFill(P.circ(38.5, 21, 2)).cutFill(P.circ(38.5, 29, 2));
    g.fill(P.cap(10, 41, 8.5, 45, 3)); g.fill(P.cap(38, 41, 39.5, 45, 3));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
