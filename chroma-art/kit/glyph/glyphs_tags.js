// Story tags: the marks on lines of the life story and dots on the life timeline.
const { glyph, P } = require('./glyph');

const HEART = 'M24 42C10 32 4 25 4 17C4 10 9 6 15 6C19 6 22 8 24 11C26 8 29 6 33 6C39 6 44 10 44 17C44 25 38 32 24 42Z';
const rd = (n) => Math.round(n * 100) / 100;
// apply a point transform to a path made only of absolute M, L, C, Q and Z commands
const xf = (d, f) => d.replace(/(-?\d*\.?\d+)[ ,]+(-?\d*\.?\d+)/g, (m, x, y) => f(+x, +y).map(rd).join(' '));
// rotate (degrees, clockwise on screen) about (ox, oy), then move by (dx, dy)
const rot = (deg, ox, oy, dx = 0, dy = 0, s = 1) => {
  const c = Math.cos(deg * Math.PI / 180), n = Math.sin(deg * Math.PI / 180);
  return (x, y) => { const u = (x - ox) * s, v = (y - oy) * s; return [ox + dx + u * c - v * n, oy + dy + u * n + v * c]; };
};
// a wavy thick line (fill), as a chain of capsules
const wave = (g, P, x, y0, y1, amp, w, turns = 1, ph = 0) => {
  const N = 16, pts = [];
  for (let i = 0; i <= N; i++) { const t = i / N; pts.push([x + amp * Math.sin(ph + t * turns * 2 * Math.PI), y0 + (y1 - y0) * t]); }
  for (let i = 0; i < N; i++) g.fill(P.cap(...pts[i], ...pts[i + 1], w));
};
const CLOUD = (g, P) => {
  g.fill(P.circ(14, 21, 7.5)); g.fill(P.circ(24.5, 15, 10)); g.fill(P.circ(34.5, 20.5, 8)); g.fill(P.rect(6.5, 19, 36, 10, 5));
};

const G = {
  'birth': (g, P) => {             // a newborn's two footprints
    for (const [x, s] of [[13, 1], [35, -1]]) {
      g.fill(`M${x} 44C${x - 6} 44 ${x - 7.5} 38 ${x - 7} 32C${x - 6.5} 26 ${x - 4.5} 22 ${x} 22C${x + 4.5} 22 ${x + 6.5} 26 ${x + 6.5} 31C${x + 6.5} 38 ${x + 5} 44 ${x} 44Z`);
      for (const [dx, cy, r] of [[4.6, 16.5, 2.6], [0.4, 15.2, 2.2], [-3.2, 15.6, 1.9], [-6, 17.4, 1.7]]) g.fill(P.circ(x + s * dx, cy, r));
    }
  },
  'quill': (g, P) => {             // a quill pen writing on a line
    g.fill('M13 34C11 20 26 6 44 3.5C42 18 29 32 13 34Z').cut('M15.5 32Q29 20 42 5.5', 1.6);
    g.fill(P.cap(15, 33, 10, 39.5, 3)); g.fill(P.poly([[8.5, 38], [11.5, 40.5], [7.5, 43]]));
    g.fill(P.cap(11, 44.5, 42, 44.5, 2.8));
  },
  'signpost': (g, P) => {          // a post with two arrow boards pointing different ways
    g.fill(P.rect(21.5, 5, 5, 38, 1));
    g.fill(P.poly([[9, 8], [36, 8], [42.5, 13], [36, 18], [9, 18]]));
    g.fill(P.poly([[39, 22], [12, 22], [5.5, 27], [12, 32], [39, 32]]));
    g.fill('M12 46Q24 38.5 36 46Z');
  },
  'cup': (g, P) => {               // a cup with a little steam
    g.fill('M7 21H35V30C35 37 30 41 23 41H19C12 41 7 37 7 30Z');
    g.fill(P.arc(35, 28, 5.5, -75, 75, 3.4));
    g.fill(P.cap(4, 44.5, 38, 44.5, 3));
    wave(g, P, 16, 4.5, 16.5, 1.8, 2.8, 1); wave(g, P, 25.5, 4.5, 16.5, 1.8, 2.8, 1);
  },
  'heartbreak': (g, P) => {        // a heart broken in two
    const Z = [[24, -2], [24, 9], [20, 16], [27, 23], [21, 30], [26, 36], [24, 44], [24, 50]];
    const L = rot(-9, 24, 44, -1.2, 0), R = rot(9, 24, 44, 1.2, 0);
    g.fill(xf(HEART, L)).cutFill(xf(P.poly([...Z, [50, 50], [50, -2]]), L));
    g.layer(); g.fill(xf(HEART, R)).cutFill(xf(P.poly([...Z, [-2, 50], [-2, -2]]), R));
  },
  'gravestone': (g, P) => {        // a rounded headstone with grass and a flower at its foot
    g.fill('M13 41V19A11 11 0 0 1 35 19V41Z').cut('M18.5 22H29.5', 2).cut('M18.5 28H29.5', 2);
    g.fill(P.rect(4, 41, 40, 4.5, 2));
    g.fill(P.circ(7.5, 32, 3)); g.fill(P.cap(7.5, 33, 7.5, 42, 2.2));
    g.fill(P.poly([[37.5, 42], [39, 34], [41, 42]])); g.fill(P.poly([[40, 42], [43.5, 35.5], [44, 42]]));
  },
  'storm': (g, P) => {             // a cloud with a lightning bolt
    const BOLT = P.poly([[22.5, 17], [12, 34.5], [21, 34.5], [15.5, 47], [36, 26.5], [27, 26.5], [32.5, 17]]);
    CLOUD(g, P); g.cut(BOLT, 2.6);
    g.layer(); g.fill(BOLT);
  },
  'globe': (g, P) => {             // a desk globe with its meridians
    g.fill(P.circ(24, 20, 14.5)).cut('M24 5.5A6.5 14.5 0 0 0 24 34.5A6.5 14.5 0 0 0 24 5.5', 1.8).cut('M9.5 20H38.5', 1.8);
    g.fill(P.arc(24, 20, 18, 25, 155, 3));
    g.fill(P.rect(22.5, 37, 3, 6)); g.fill(P.rect(15, 42.5, 18, 3.5, 1.5));
  },
  'box': (g, P) => {               // stacked, taped moving boxes
    g.fill(P.rect(8, 20, 32, 25, 1.6)).cut('M18 28.5H30', 2.6);
    g.fill(P.poly([[8, 18], [3, 8.5], [17.5, 5.5], [21.5, 18]])); g.fill(P.poly([[40, 18], [45, 8.5], [30.5, 5.5], [26.5, 18]]));
  },
  'newspaper': (g, P) => {         // a folded newspaper
    g.fill('M11 14H7.5Q4 14 4 17.5V39.5Q4 43 7.5 43H11Z');
    g.hole(P.rect(10, 6, 34, 37, 2.4), P.rect(14, 10, 26, 5, 1), P.rect(14, 19, 11, 11, 1), P.rect(28, 19, 12, 2.6, 1), P.rect(28, 24.5, 12, 2.6, 1), P.rect(14, 33.5, 26, 2.6, 1));
    g.cut('M10 15V43', 1.6);
  },
  'swords': (g, P) => {            // two crossed swords, points up
    const sword = (f) => [P.poly([f(-3, 6), f(-3, -14), f(0, -19.5), f(3, -14), f(3, 6)]),
      P.cap(...f(-8.5, 8), ...f(8.5, 8), 4), P.cap(...f(0, 9), ...f(0, 14.5), 3.6), P.circ(...f(0, 17), 3)];
    const A = sword(rot(40, 0, 0, 24, 23.5, 1.15)), B = sword(rot(-40, 0, 0, 24, 23.5, 1.15));
    for (const d of B) g.fill(d);
    for (const d of A) g.cut(d, 2.4);
    g.layer(); for (const d of A) g.fill(d);
  },
  'steps': (g, P) => {             // steps rising to a small flag
    g.fill(P.poly([[4, 45], [4, 38], [13, 38], [13, 31], [22, 31], [22, 24], [31, 24], [31, 17], [44, 17], [44, 45]]));
    g.fill(P.cap(40.5, 17, 40.5, 4.5, 2.8)); g.fill(P.poly([[39.5, 4], [28, 8.5], [39.5, 13]]));
  },
  'u-turn': (g, P) => {            // a bold arrow that bends back on itself
    g.fill(P.cap(8, 13, 27, 13, 7)); g.fill(P.arc(27, 24, 11, -90, 90, 7)); g.fill(P.rect(17, 31.5, 10.5, 7));
    g.fill(P.poly([[18.5, 25], [4.5, 35], [18.5, 45]]));
  },
  'breakthrough': (g, P) => {      // a bold arrow bursting through a brick wall split in two
    g.fill('M15 4H23V16L20 20L23 24L19 28H15Z'); g.fill('M15 30H19.5L23 34V44H15Z');
    g.fill('M25 4H33V44H25V34L28.5 30L25 26L29 21L25 16Z');
    g.cut('M15 11H23M25 11H33M15 38H23M25 38H33', 1.5);
    g.cutFill(P.cap(3, 24, 31, 24, 9)).cutFill(P.poly([[28, 11.5], [48.5, 24], [28, 36.5]]));
    g.layer();
    g.fill(P.cap(3, 24, 31, 24, 5.6)); g.fill(P.poly([[30, 14.5], [45, 24], [30, 33.5]]));
  },
  'stump': (g, P) => {             // a cut stump with a new shoot
    g.fill('M12 23H36V35C36 39 38 41.5 44 44.5H4C10 41.5 12 39 12 35Z').cut('M12 23A12 4 0 0 0 36 23', 1.8).cut('M18.5 31V39', 1.6).cut('M24.5 32V41', 1.6).cut('M30.5 31V39', 1.6);
    g.fill('M12 23A12 4 0 0 1 36 23Z');
    g.fill(P.cap(30, 22, 32, 11, 2.8)); g.fill(P.lens(31.5, 14, 22, 7.5, 3)); g.fill(P.lens(32, 11.5, 42, 5.5, 3));
  },
  'wall': (g, P) => {              // a stone wall, crenellated: hardened
    for (const x of [5, 19.5, 34]) g.fill(P.rect(x, 4, 9, 8.2, 1));
    const rows = [[14.2, [[5, 16.8], [19, 29], [31.2, 43]]], [24.4, [[5, 10.9], [13.1, 22.9], [25.1, 34.9], [37.1, 43]]], [34.6, [[5, 16.8], [19, 29], [31.2, 43]]]];
    for (const [y, bs] of rows) for (const [a, b] of bs) g.fill(P.rect(a, y, b - a, 8.2, 1));
  },
  'raincloud': (g, P) => {         // a cloud with falling rain
    CLOUD(g, P);
    const drop = (x, y) => g.fill(`M${x} ${y - 4.5}C${x + 1} ${y - 2} ${x + 2.4} ${y - 0.8} ${x + 2.4} ${y + 0.8}A2.4 2.4 0 0 1 ${x - 2.4} ${y + 0.8}C${x - 2.4} ${y - 0.8} ${x - 1} ${y - 2} ${x} ${y - 4.5}Z`);
    drop(14, 36); drop(24.5, 36); drop(35, 36); drop(19, 44); drop(30, 44);
  },
  'horseshoe': (g, P) => {         // a horseshoe, open end up, with nail holes
    g.fill(P.arc(24, 25, 12.5, 0, 180, 8.5)); g.fill(P.cap(11.5, 25, 13.5, 8, 8.5)); g.fill(P.cap(36.5, 25, 34.5, 8, 8.5));
    for (const a of [25, 60, 120, 155]) g.cutFill(P.circ(24 + Math.cos(a * Math.PI / 180) * 12.5, 25 + Math.sin(a * Math.PI / 180) * 12.5, 1.4));
    for (const [x, y] of [[12, 17], [36, 17]]) g.cutFill(P.circ(x, y, 1.4));
  },
  'masks': (g, P) => {             // two theatre masks, one smiling, one frowning
    const M = 'M-10 -11C-4 -14 4 -14 10 -11C11 -1 8 9 0 13C-8 9 -11 -1 -10 -11Z';
    const back = rot(-14, 0, 0, 17, 18, 1.08), front = rot(12, 0, 0, 31, 28, 1.08);
    const parts = (f, mouth) => [xf(P.lens(-7.5, -4, -2, -4, 1.7), f), xf(P.lens(2, -4, 7.5, -4, 1.7), f), xf(mouth, f)];
    g.fill(xf(M, back)); for (const d of parts(back, 'M-6 8.5Q0 -0.5 6 8.5Q0 4 -6 8.5Z')) g.cutFill(d);
    g.cut(xf(M, front), 2.6);
    g.layer(); g.fill(xf(M, front)); for (const d of parts(front, 'M-6 2Q0 11 6 2Q0 6 -6 2Z')) g.cutFill(d);
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
