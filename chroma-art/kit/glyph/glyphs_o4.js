// Option icons, batch o4: home, food and everyday things.
const { glyph, P } = require('./glyph');

const rd = (n) => Math.round(n * 100) / 100;
// apply a point transform to a path made only of absolute M, L, C, Q and Z commands
const xf = (d, f) => d.replace(/(-?\d*\.?\d+)[ ,]+(-?\d*\.?\d+)/g, (m, x, y) => f(+x, +y).map(rd).join(' '));
// rotate (degrees, clockwise on screen) about (ox, oy), then move by (dx, dy)
const rot = (deg, ox, oy, dx = 0, dy = 0) => {
  const c = Math.cos(deg * Math.PI / 180), n = Math.sin(deg * Math.PI / 180);
  return (x, y) => { const u = x - ox, v = y - oy; return [ox + dx + u * c - v * n, oy + dy + u * n + v * c]; };
};
// a thick line along a quadratic curve A -> (control C) -> B, as a chain of capsules
const qline = (g, P, ax, ay, cx, cy, bx, by, w) => {
  const N = 12, pts = [];
  for (let i = 0; i <= N; i++) { const t = i / N, u = 1 - t; pts.push([u * u * ax + 2 * u * t * cx + t * t * bx, u * u * ay + 2 * u * t * cy + t * t * by]); }
  for (let i = 0; i < N; i++) g.fill(P.cap(...pts[i], ...pts[i + 1], w));
};
// a tapered rod from (x1, y1) radius r1 to (x2, y2) radius r2, round at both ends
const taper = (x1, y1, r1, x2, y2, r2) => {
  const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy), nx = -dy / d, ny = dx / d;
  return P.poly([[x1 + nx * r1, y1 + ny * r1], [x2 + nx * r2, y2 + ny * r2], [x2 - nx * r2, y2 - ny * r2], [x1 - nx * r1, y1 - ny * r1]]) + P.circ(x1, y1, r1) + P.circ(x2, y2, r2);
};
// a wine glass with its foot at (fx, fy), tilted by deg
// returns [bowl, stem, foot] paths
const wineGlass = (fx, fy, deg) => {
  const f = rot(deg, 0, 0, fx, fy), pt = (x, y) => f(x, y).map(rd);
  return [xf('M-7.6 -30C-7.6 -20 -5 -14 0 -14C5 -14 7.6 -20 7.6 -30Z', f), P.cap(...pt(0, -15), ...pt(0, -2.5), 2.8), P.cap(...pt(-6, -1.6), ...pt(6, -1.6), 3)];
};

const G = {
  'plate': (g, P) => {             // a plate seen from above, a fork on the left and a knife on the right
    g.fill(P.circ(24, 24, 12.5)).cut(P.circ(24, 24, 8.3), 1.8);
    g.fill('M2 5H10V16C10 19.5 8.5 21.5 6 21.5C3.5 21.5 2 19.5 2 16Z').cut('M4.7 4V13', 1.4).cut('M7.3 4V13', 1.4);
    g.fill(P.cap(6, 20, 6, 43.5, 3.4));
    g.fill('M39 25V9C39 6.5 40.5 5 42 5C44.5 5 46 9 46 16C46 22 45 25 43.5 25Z');
    g.fill(P.cap(42, 24, 42, 43.5, 3.6));
  },
  'gift': (g, P) => {              // a wrapped present tied with a ribbon and a bow
    g.hole('M24 14C20 6 13 3 10 6C7.5 8.5 10 13 16 14Z', 'M21.5 12.5C18.5 8.5 14.5 7 12.8 8.3C11.8 9.3 13 11.8 16.5 12.5Z');
    g.hole('M24 14C28 6 35 3 38 6C40.5 8.5 38 13 32 14Z', 'M26.5 12.5C29.5 8.5 33.5 7 35.2 8.3C36.2 9.3 35 11.8 31.5 12.5Z');
    g.fill(P.rect(5, 15, 38, 8, 1.6)).cut('M20.5 15V23', 1.8).cut('M27.5 15V23', 1.8);
    g.fill(P.rect(8, 25, 32, 20, 1.6)).cut('M20.5 25V45', 1.8).cut('M27.5 25V45', 1.8);
  },
  'glass': (g, P) => {             // two wine glasses raised and touching in a toast
    const right = wineGlass(39.5, 44, -14);
    for (const d of wineGlass(8.5, 44, 14)) g.fill(d);
    g.cut(right[0], 2.6);
    g.layer(); for (const d of right) g.fill(d);
    g.cut(xf('M-6 -22H6', rot(-14, 0, 0, 39.5, 44)), 1.6);
    g.layer();
    for (const [x1, y1, x2, y2] of [[24, 3.5, 24, 8.5], [16.5, 6, 19, 10], [31.5, 6, 29, 10]]) g.fill(P.cap(x1, y1, x2, y2, 2.4));
  },
  'cake': (g, P) => {              // a two-tier birthday cake with three lit candles
    for (const x of [14.5, 24, 33.5]) {
      g.fill(P.rect(x - 1.6, 12, 3.2, 8.5, 0.6));
      g.fill(`M${x} 3C${x + 2.6} 6 ${x + 2.6} 9.8 ${x} 10C${x - 2.6} 9.8 ${x - 2.6} 6 ${x} 3Z`);
    }
    g.fill(P.rect(10, 21, 28, 10, 2)).cut('M10 26Q12.8 29 15.6 26T21.2 26T26.8 26T32.4 26T38 26', 1.8);
    g.fill(P.rect(5, 31, 38, 14, 2)).cut('M5 37Q8.2 40 11.3 37T17.7 37T24 37T30.3 37T36.7 37T43 37', 1.8).cut('M4 31H44', 1.8);
  },
  'balloons': (g, P) => {          // three party balloons on strings, tied together
    const ball = (cx, cy) => `M${cx} ${cy - 10}C${cx + 5.5} ${cy - 10} ${cx + 8} ${cy - 5.5} ${cx + 8} ${cy - 1}C${cx + 8} ${cy + 5} ${cx + 3.5} ${cy + 9.5} ${cx} ${cy + 9.5}C${cx - 3.5} ${cy + 9.5} ${cx - 8} ${cy + 5} ${cx - 8} ${cy - 1}C${cx - 8} ${cy - 5.5} ${cx - 5.5} ${cy - 10} ${cx} ${cy - 10}Z`
      + P.poly([[cx - 2.2, cy + 12], [cx + 2.2, cy + 12], [cx, cy + 8.5]]);
    qline(g, P, 11, 26, 13, 36, 23, 45, 1.9); qline(g, P, 37, 24, 35, 36, 25, 45, 1.9);
    g.fill(ball(11, 14)).cut('M6.5 12C6.5 9 8 7 10 6.5', 1.8);
    g.fill(ball(37, 12)).cut('M32.5 10C32.5 7 34 5 36 4.5', 1.8);
    g.cut(xf(ball(24, 21), (x, y) => [x, y]), 3);
    g.layer();
    qline(g, P, 24, 33, 22, 39, 24, 45, 1.9);
    g.fill(ball(24, 21)).cut('M19.5 19C19.5 16 21 14 23 13.5', 1.8);
  },
  'cookie-jar': (g, P) => {        // a biscuit jar, lid tipped off to the side, a biscuit half out of its mouth
    g.fill('M12 21H34V22C38 24 39 28 39 32V40C39 43 37 45 34 45H12C9 45 7 43 7 40V32C7 28 8 24 12 22Z').cut('M10 30H36', 1.6);
    g.fill(P.rect(11, 17.5, 24, 3.5, 1.2));
    g.layer();
    g.hole(P.circ(21, 13, 7.6), P.circ(18.5, 11, 1.4), P.circ(23.5, 10, 1.3), P.circ(22, 15.5, 1.4));
    g.fill('M31 5.5L43 9.5L41.8 13L29.8 9Z'); g.fill(P.rect(35.2, 4.2, 4, 3, 1));
  },
  'apple': (g, P) => {             // an apple with a stalk and a leaf
    g.fill('M24 17.5C20 14 8 13.5 6.5 25.5C5.5 35 12.5 45 18.5 45C21 45 22 44 24 44C26 44 27 45 29.5 45C35.5 45 42.5 35 41.5 25.5C40 13.5 28 14 24 17.5Z')
      .cut('M12.5 26C12.5 22.5 14.5 20.5 17.5 20', 2);
    g.fill(P.cap(23.5, 17, 25.5, 6, 2.8));
    g.fill(P.lens(27, 11.5, 39, 5, 3.4)).cut('M28.5 11L36 7', 1.2);
  },
  'vegetables': (g, P) => {        // a woven basket of vegetables: a cabbage, and a carrot with its leafy top
    g.fill(P.circ(15, 19, 8.5)).cut('M15 11.5V25', 1.6).cut('M9.5 15.5C12 18 13 21 13 24', 1.4);
    g.fill(taper(32.5, 15.5, 4.4, 25.5, 28, 1.8)).cut('M28.2 19.6L31.6 21.4', 1.4).cut('M30.6 15.4L34 17.2', 1.4);
    g.fill(P.lens(34, 12, 37, 2.5, 2.2)); g.fill(P.lens(35, 13, 44, 5.5, 2.2)); g.fill(P.lens(35.5, 15, 45, 16, 2));
    g.cut('M3 26.5H45', 2.4);
    g.layer();
    g.fill(P.rect(4, 27.5, 40, 5, 1.6));
    g.fill(P.poly([[7, 33.5], [41, 33.5], [37.5, 45], [10.5, 45]])).cut('M7 38.5H41', 1.6).cut('M17 34V45', 1.6).cut('M24 34V45', 1.6).cut('M31 34V45', 1.6);
  },
  'teddy-bear': (g, P) => {        // a teddy bear sitting up
    g.fill(P.circ(13.5, 8.5, 5)).cutFill(P.circ(13.5, 8.5, 1.9)); g.fill(P.circ(34.5, 8.5, 5)).cutFill(P.circ(34.5, 8.5, 1.9));
    g.layer();
    g.fill(P.circ(24, 35, 10)); g.fill(P.cap(16, 31, 8.5, 36.5, 6.4)); g.fill(P.cap(32, 31, 39.5, 36.5, 6.4));
    g.fill(P.circ(15.5, 41.5, 4.6)); g.fill(P.circ(32.5, 41.5, 4.6));
    g.cut(P.circ(24, 35, 4.5), 1.6).cut(P.circ(24, 16, 12.2), 2.4);
    g.layer();
    g.fill(P.circ(24, 16, 11)).cut(P.circ(24, 20.5, 4.2), 1.6).cutFill(P.circ(19.5, 14, 1.6)).cutFill(P.circ(28.5, 14, 1.6)).cutFill(P.circ(24, 19.2, 1.4));
  },
  'chair': (g, P) => {             // a wooden chair, side view
    g.fill(P.poly([[7.5, 4], [14, 3], [16, 45], [11, 45]])).cut('M11 8.5L12.3 21', 1.6);
    g.fill(P.rect(11, 23.5, 30, 6, 1.6));
    g.fill(P.poly([[35, 29], [40.5, 29], [41, 45], [36, 45]]));
    g.fill(P.cap(14, 37.5, 37, 37.5, 3));
  },
  'bench': (g, P) => {             // a park bench, front view
    g.fill(P.rect(5, 8, 38, 5, 1.6)); g.fill(P.rect(5, 15.5, 38, 5, 1.6));
    g.fill(P.rect(3, 25, 42, 5.5, 1.6));
    for (const x of [8, 36]) { g.fill(P.rect(x, 7, 4, 18.5, 1)); g.fill(P.rect(x, 30, 4, 15, 1)); g.fill(P.cap(x - 1, 44, x + 5, 44, 2.6)); }
  },
  'window': (g, P) => {            // a window with its curtains tied back at the sides
    g.fill(P.cap(3, 5, 45, 5, 3));
    g.hole(P.rect(14, 9.5, 20, 30.5, 1), P.rect(16.8, 12.3, 6, 12.2, 0.6), P.rect(25.2, 12.3, 6, 12.2, 0.6), P.rect(16.8, 27.2, 6, 10, 0.6), P.rect(25.2, 27.2, 6, 10, 0.6));
    g.fill(P.rect(11, 40, 26, 4.5, 1.2));
    g.fill('M3 7H11.5C11 15 10.5 20 8 24.5C10.5 30 11.5 35 11.5 40.5H3Z');
    g.fill('M45 7H36.5C37 15 37.5 20 40 24.5C37.5 30 36.5 35 36.5 40.5H45Z');
  },
  'clothes-hanger': (g, P) => {    // a shirt on a clothes hanger
    g.fill(P.arc(24, 7, 3.6, 150, 405, 2.6)); g.fill(P.cap(26.5, 9.6, 24, 13, 2.6));
    g.fill('M19 13.5L8 17L3 29L10 32L12.5 28V45H35.5V28L38 32L45 29L40 17L29 13.5Z')
      .cut('M19 13L24 20.5L29 13', 2).cut('M24 21.5V43', 1.6);
  },
  'umbrella': (g, P) => {          // a rain umbrella with a crook handle, raindrops falling on it
    const f = rot(-16, 24, 26);
    g.fill(xf('M5 25C5 13 13.5 6 24 6C34.5 6 43 13 43 25C40 22.5 36.5 22.5 33.5 25C30.5 22.5 27 22.5 24 25C21 22.5 17.5 22.5 14.5 25C11.5 22.5 8 22.5 5 25Z', f))
      .cut(xf('M24 7L18 22.5', f), 1.6).cut(xf('M24 7L30 22.5', f), 1.6);
    const [a, b] = [f(24, 4.5), f(24, 38)];
    g.fill(P.cap(...a, ...b, 3));
    g.fill(P.arc(...f(28.5, 38), 4.5, -16, 164, 3));
    g.fill(P.cap(...f(33, 38), ...f(33, 36), 3));
    for (const [x, y] of [[38, 3.5], [44, 11], [36.5, 13.5]]) g.fill(`M${x} ${y}C${x + 2} ${y + 3} ${x + 2.4} ${y + 4.3} ${x + 2.4} ${y + 5}C${x + 2.4} ${y + 6.5} ${x + 1.3} ${y + 7.5} ${x} ${y + 7.5}C${x - 1.3} ${y + 7.5} ${x - 2.4} ${y + 6.5} ${x - 2.4} ${y + 5}C${x - 2.4} ${y + 4.3} ${x - 2} ${y + 3} ${x} ${y}Z`);
  },
  'pills': (g, P) => {             // a medicine bottle with two tablets beside it
    g.fill(P.rect(7.5, 3.5, 21, 7.5, 1.6)).cut('M13 4V10.5', 1.6).cut('M18 4V10.5', 1.6).cut('M23 4V10.5', 1.6);
    g.fill(P.rect(6, 13, 24, 32, 3.5)).cutFill(P.rect(10, 21, 16, 14, 1));
    g.layer(); g.fill(P.rect(12.5, 26.5, 11, 3, 0.6));
    g.fill(P.circ(38.5, 39, 6)).cut('M33 39H44', 1.6);
    g.fill(P.cap(34, 26, 42, 18, 7)).cut('M35.5 19.5L40.5 24.5', 1.6);
  },
  'rubbish-bin': (g, P) => {       // a rubbish bin with its lid on
    g.fill(P.arc(24, 8.5, 4.5, 180, 360, 2.8));
    g.fill(P.rect(6, 9, 36, 5.5, 2));
    g.fill(P.poly([[9.5, 16.5], [38.5, 16.5], [35.5, 45], [12.5, 45]])).cut('M17 21L18 40', 2).cut('M24 21V40', 2).cut('M31 21L30 40', 2);
  },
  'pet-bowl': (g, P) => {          // a pet's food bowl heaped with kibble, a bone resting on it
    for (const [x, y, r] of [[12.5, 25.5, 4.2], [19, 23, 4.8], [27, 23, 4.8], [34.5, 25.5, 4.2]]) g.fill(P.circ(x, y, r));
    const bone = P.cap(14, 17, 34, 11, 4) + P.circ(12.4, 15, 3.3) + P.circ(13.6, 20.2, 3.3) + P.circ(34.4, 7.8, 3.3) + P.circ(35.6, 13, 3.3);
    g.cut('M3 28.5H45', 2.4).cut(bone, 2.6);
    g.layer(); g.fill(bone);
    g.layer();
    g.fill('M8.5 29.5H39.5L44.5 41C45.2 43 44 45 41.5 45H6.5C4 45 2.8 43 3.5 41Z').cut('M6.5 34.5H41.5', 1.8);
  },
  'mortar-and-pestle': (g, P) => { // a mortar with its pestle and a sprig of herbs
    g.fill(taper(26, 26, 4.2, 38, 5.5, 2.8));
    g.fill(P.cap(13, 25, 8, 4.5, 2.4)); g.fill(P.lens(11.2, 17, 3, 13.5, 2.2)); g.fill(P.lens(9.8, 11, 16, 6, 2));
    g.cut('M3 22H45', 2.4);
    g.layer();
    g.fill('M5 23H43V26C43 35 35.5 40.5 24 40.5C12.5 40.5 5 35 5 26Z').cut('M5 27.5H43', 1.8);
    g.fill(P.rect(15, 40, 18, 5, 1.6));
  },
  'shopping-bag': (g, P) => {      // a paper shopping bag with a cord handle
    const pts = []; for (let i = 0; i <= 14; i++) { const a = Math.PI + i * Math.PI / 14; pts.push([24 + 7 * Math.cos(a), 18.5 + 15 * Math.sin(a)]); }
    for (let i = 0; i < 14; i++) g.fill(P.cap(...pts[i], ...pts[i + 1], 2.8));
    g.layer();
    g.fill('M12 16H36L42.5 42C43 44 41.5 45 39.5 45H8.5C6.5 45 5 44 5.5 42Z').cut('M10.5 22H37.5', 1.8)
      .cutFill(P.circ(17, 18.8, 1.5)).cutFill(P.circ(31, 18.8, 1.5));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
