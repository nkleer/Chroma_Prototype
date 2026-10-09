// Acts the character's history remembers, and the options when a parent dies.
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const rot = (pts, cx, cy, deg) => pts.map(([x, y]) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg)), dx = x - cx, dy = y - cy;
  return [cx + dx * c - dy * s, cy + dx * s + dy * c];
});
// a rounded square of side s centred on (cx, cy), turned by deg, corners rounded by q
const rsq = (cx, cy, s, q, deg) => {
  const h = s / 2, c = [[-h, -h], [h, -h], [h, h], [-h, h]];
  const pts = rot(c.map(([x, y]) => [cx + x, cy + y]), cx, cy, deg);
  const f = (n) => Math.round(n * 100) / 100;
  let d = '';
  for (let i = 0; i < 4; i++) {
    const p = pts[i], a = pts[(i + 3) % 4], b = pts[(i + 1) % 4];
    const la = Math.hypot(a[0] - p[0], a[1] - p[1]), t = q / la;
    const p1 = [p[0] + (a[0] - p[0]) * t, p[1] + (a[1] - p[1]) * t], p2 = [p[0] + (b[0] - p[0]) * t, p[1] + (b[1] - p[1]) * t];
    d += `${i ? 'L' : 'M'}${f(p1[0])} ${f(p1[1])}Q${f(p[0])} ${f(p[1])} ${f(p2[0])} ${f(p2[1])}`;
  }
  return d + 'Z';
};
const at = (cx, cy, deg, x, y) => rot([[cx + x, cy + y]], cx, cy, deg)[0];

const G = {
  // ---- acts the character's history remembers ----
  'locked-chest': (g, P) => {      // hid a wrong: a chest shut with a padlock
    g.fill('M4 19V15.5C4 10 8.5 6 14 6H34C39.5 6 44 10 44 15.5V19Z');
    g.fill(P.rect(4, 21.5, 40, 21.5, 2));
    g.cut('M4 30H44', 1.8);
    g.cut(P.arc(24, 21, 5, 180, 360, 3), 4.4).cut(P.rect(16, 21, 16, 14, 2.5), 4.4);
    g.layer();
    g.fill(P.arc(24, 21, 5, 180, 360, 3));
    g.fill(P.rect(16, 21, 16, 14, 2.5)).cutFill(P.circ(24, 26.2, 1.9)).cutFill(P.poly([[22.9, 26.5], [25.1, 26.5], [25.8, 31.5], [22.2, 31.5]]));
  },
  'lifebuoy': (g, P) => {          // helped someone in need: a life ring with four bands
    g.hole(P.circ(24, 24, 20.5), P.circ(24, 24, 8.5));
    for (const a of [45, 135, 225, 315]) g.cutFill(P.arc(24, 24, 14.5, a - 21, a + 21, 5.4));
  },
  'dice': (g, P) => {              // took a wild risk: two dice
    g.fill(rsq(32, 16, 20, 4, 16)).cut(rsq(16.5, 30.5, 22, 4.5, -9), 4.4);
    for (const [x, y] of [[-5, -5], [5, 5], [-5, 5], [5, -5]]) g.cutFill(P.circ(...at(32, 16, 16, x, y), 2.2));
    g.layer();
    g.fill(rsq(16.5, 30.5, 22, 4.5, -9));
    for (const [x, y] of [[-5.5, -5.5], [0, 0], [5.5, 5.5]]) g.cutFill(P.circ(...at(16.5, 30.5, -9, x, y), 2.4));
  },
  'sealed-scroll': (g, P) => {     // kept your word: a charter under a wax seal
    g.fill(P.rect(10, 7, 28, 30)).cut('M15 15H33', 1.6).cut('M15 21H33', 1.6).cut('M15 27H26', 1.6);
    g.fill(P.rect(6, 3, 36, 7, 3.5)).fill(P.rect(6, 34, 36, 7, 3.5));
    g.cut(P.circ(31, 36, 7.5), 4.4);
    g.layer();
    g.fill(P.lens(29, 40, 25.5, 45.5, 2.6)).fill(P.lens(33, 40, 36.5, 45.5, 2.6));
    g.fill(P.star(31, 36, 8, 6.9, 13, 0)).cut(P.circ(31, 36, 3.6), 1.6);
  },
  'door-shut': (g, P) => {         // turned down a chance: a closed door in its frame
    g.hole(P.rect(6, 3, 36, 42, 1.5), P.rect(11.5, 8.5, 25, 36.5));
    g.fill(P.rect(13.5, 10.5, 21, 34.5, 0.8)).cut(P.rect(17, 14, 11, 11, 0.6), 1.6).cut(P.rect(17, 29, 11, 12, 0.6), 1.6)
      .cutFill(P.circ(31.2, 28, 1.6));
  },
  'door-open': (g, P) => {         // left home: the door swung wide, a step out
    g.hole(P.rect(4, 3, 27, 37, 1.5), P.rect(9.5, 8.5, 16, 31.5));
    g.fill(P.poly([[32.5, 6], [44, 10], [44, 37], [32.5, 40]])).cutFill(P.circ(41, 24, 1.5));
    g.fill(P.poly([[9.5, 41.5], [25.5, 41.5], [32.5, 45], [3, 45]]));
  },
  'torn-scroll': (g, P) => {       // broke your word: a deed torn in two
    const zz = [[25, 5], [22, 10], [26, 15], [22, 20], [26, 25], [22, 30], [26, 35], [23, 40], [25, 44]];
    const L = rot([[7, 5], ...zz, [7, 44]].map(([x, y]) => [x - 3, y]), 7, 44, -8);
    const R = rot([...zz, [41, 44], [41, 5]].map(([x, y]) => [x + 3, y]), 41, 44, 8);
    g.fill(P.poly(L)).fill(P.poly(R));
    for (const y of [14, 21, 28]) {
      const a = rot([[8, y], [17.5, y]].map(([x, yy]) => [x - 3, yy]), 7, 44, -8), b = rot([[30.5, y], [40, y]].map(([x, yy]) => [x + 3, yy]), 41, 44, 8);
      g.cut(`M${a[0].join(' ')}L${a[1].join(' ')}`, 1.6).cut(`M${b[0].join(' ')}L${b[1].join(' ')}`, 1.6);
    }
  },
  'padlock': (g, P) => {           // refused someone in need: a padlock
    g.fill(P.arc(24, 17, 9, 180, 360, 5)).fill(P.cap(15, 17, 15, 23, 5)).fill(P.cap(33, 17, 33, 23, 5));
    g.fill(P.rect(8, 22, 32, 23, 4)).cutFill(P.circ(24, 30.5, 3)).cutFill(P.poly([[22.4, 31.5], [25.6, 31.5], [26.6, 39.5], [21.4, 39.5]]));
  },
  'puppet': (g, P) => {            // gave in to pressure: a figure dangling from strings
    g.fill(P.cap(7, 9, 41, 4, 3.6));
    g.fill(P.cap(9.5, 9, 11.5, 23, 2)).fill(P.cap(38.5, 5, 36.5, 29, 2)).fill(P.cap(24.5, 7, 24.5, 14.5, 2));
    g.fill(P.circ(24.5, 18.5, 4.2));
    g.fill(P.rect(20, 24, 9, 11.5, 4));
    g.fill(P.cap(21, 26, 15.5, 29, 3)).fill(P.cap(15.5, 29, 11.5, 23.5, 3));
    g.fill(P.cap(28, 26, 33, 31, 3)).fill(P.cap(33, 31, 36.5, 29.5, 3));
    g.fill(P.cap(22, 34, 17.5, 38.5, 3.4)).fill(P.cap(17.5, 38.5, 19.5, 44.5, 3.2));
    g.fill(P.cap(27, 34, 28.5, 44.5, 3.4));
  },
  'key': (g, P) => {               // came home: a house key
    g.hole(P.circ(13, 13, 10), P.circ(13, 13, 4.6));
    g.fill(P.cap(19.5, 19.5, 40, 40, 4.8));
    g.fill(P.poly([[28.5, 28.5], [34.2, 22.8], [43.2, 31.8], [37.5, 37.5]])).cutFill(P.poly([[35.5, 27.5], [38, 25], [40, 27], [37.5, 29.5]]));
  },

  // ---- a parent dies ----
  'cracked-mask': (g, P) => {      // nobody will see you cry: a calm mask with a crack
    g.fill('M24 4C34.5 4 41.5 7.5 41.5 17C41.5 30 33.5 43.5 24 44C14.5 43.5 6.5 30 6.5 17C6.5 7.5 13.5 4 24 4Z')
      .cutFill(P.lens(12, 19.5, 21, 19.5, 2.1)).cutFill(P.lens(27, 19.5, 36, 19.5, 2.1)).cut('M19 33.5Q24 35.5 29 33.5', 1.9)
      .cut('M27 3L23.5 9.5L27.5 14.5L23.5 20L26 25.5L24.5 29', 2.2).cut('M23.5 9.5L19 7.5', 1.6);
  },
  'door-slam': (g, P) => {         // cry and rage, slam every door: a door with slam lines
    g.fill(P.rect(14, 4, 20, 41, 0.8)).cut(P.rect(17.2, 7.5, 10.3, 11.5, 0.6), 1.6).cut(P.rect(17.2, 23, 10.3, 18.5, 0.6), 1.6)
      .cutFill(P.circ(30.6, 24, 1.6));
    for (const s of [-1, 1]) {
      const X = (x) => 24 + s * (x - 24);
      g.fill(P.cap(X(10), 11, X(4.5), 7.5, 2.8)).fill(P.cap(X(10), 24, X(3.5), 24, 2.8)).fill(P.cap(X(10), 37, X(4.5), 40.5, 2.8));
    }
  },
  'shout': (g, P) => {             // shout their name: a head, mouth open, the sound going out
    g.fill('M8 45V36C5 33 3.5 28.5 3.5 22.5C3.5 13 9.5 7 17 7C23.5 7 27.5 11.5 27.5 17L30 21.5L27 22.5L21.5 25.5L27.5 29C27.5 33 25 35 21 35V45Z');
    g.fill(P.arc(26, 26, 8, -38, 38, 2.8)).fill(P.arc(26, 26, 13, -40, 40, 2.8)).fill(P.arc(26, 26, 18, -42, 42, 2.8));
  },
  'sapling': (g, P) => {           // plant something where they lie: a young tree on a mound
    g.fill('M3.5 45C6 37.5 14 33.5 24 33.5C34 33.5 42 37.5 44.5 45Z');
    g.fill(P.cap(24, 35, 24, 10, 3));
    g.fill(P.lens(24, 11, 24, 2.5, 2.8));
    g.fill(P.lens(23, 19, 14.5, 12.5, 2.8)).fill(P.lens(25, 19, 33.5, 12.5, 2.8));
    g.fill(P.lens(23, 28, 11, 21.5, 3.4)).fill(P.lens(25, 28, 37, 21.5, 3.4));
  },
  'open-chest': (g, P) => {        // go through their things alone: a trunk thrown open, letters inside
    const sheet = (cx, cy, a) => P.poly(rot([[cx - 4.5, cy - 7], [cx + 4.5, cy - 7], [cx + 4.5, cy + 7], [cx - 4.5, cy + 7]], cx, cy, a));
    const S = [[15, 22, -14], [24, 20, 0], [33, 22, 14]];
    g.fill(P.poly([[4, 4], [44, 4], [41.5, 21], [6.5, 21]])).cut('M10 9.5H38', 1.8);
    for (const [cx, cy, a] of S) g.cut(sheet(cx, cy, a), 4);
    g.layer();
    for (const [cx, cy, a] of S) g.fill(sheet(cx, cy, a));
    g.fill(P.rect(4, 27, 40, 18, 2)).cut('M4 33H44', 1.8);
  },
  'broom': (g, P) => {             // take on their jobs at home: a broom and a bucket
    g.fill(P.cap(30, 3.5, 17.5, 25, 3.2));
    g.fill(P.poly(rot([[13, 24], [22, 24], [26, 42], [9, 42]], 17.5, 24, 30))).cut(`M${at(17.5, 24, 30, -6, 4).join(' ')}L${at(17.5, 24, 30, 6, 4).join(' ')}`, 1.8);
    g.fill(P.poly([[27, 30], [44, 30], [42, 45], [29, 45]])).fill(P.arc(35.5, 30, 6.5, 180, 360, 2.6)).cut('M28 35H43', 1.6);
  },
  'lectern': (g, P) => {           // read out what you wrote: someone at a lectern, a sheet on it
    g.fill(P.circ(24, 8.5, 5.2));
    g.fill('M13 26V21C13 17 16 15 20 15H28C32 15 35 17 35 21V26Z');
    g.fill(P.poly([[5, 22], [43, 22], [41, 29], [7, 29]])).cut(P.rect(15, 24.2, 18, 2.6), 1.4);
    g.fill(P.poly([[11, 31], [37, 31], [34, 45], [14, 45]])).cut('M24 35V41', 1.6);
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
