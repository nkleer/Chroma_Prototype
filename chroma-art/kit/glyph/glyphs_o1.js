// Option icons, batch o1: people, figures and poses.
const { glyph, P } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
// a figure as a list of parts: ['c', cx, cy, r] a circle, ['k', x1, y1, x2, y2, w] a capsule, ['r', x, y, w, h, rx] a rounded box,
// ['p', d] a raw path (not grown). k grows every part by k (for knocking a gap out of the layer behind).
const part = (p, k = 0) => {
  if (p[0] === 'c') return P.circ(p[1], p[2], p[3] + k);
  if (p[0] === 'k') return P.cap(p[1], p[2], p[3], p[4], p[5] + 2 * k);
  if (p[0] === 'r') return P.rect(p[1] - k, p[2] - k, p[3] + 2 * k, p[4] + 2 * k, p[5] + k);
  return p[1];
};
const put = (g, parts) => parts.forEach((p) => g.fill(part(p)));
const knock = (g, parts, k) => parts.forEach((p) => p[0] !== 'p' && g.cutFill(part(p, k)));
// a chain of capsules through points
const chain = (pts, w) => pts.slice(1).map((q, i) => ['k', ...pts[i], ...q, w]);
// turn a part list by deg about (ox, oy), then move by (dx, dy)
const turn = (parts, deg, ox, oy, dx = 0, dy = 0) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg));
  const f = (x, y) => [ox + dx + (x - ox) * c - (y - oy) * s, oy + dy + (x - ox) * s + (y - oy) * c];
  return parts.map((p) => p[0] === 'c' ? ['c', ...f(p[1], p[2]), p[3]] : p[0] === 'k' ? ['k', ...f(p[1], p[2]), ...f(p[3], p[4]), p[5]] : p);
};
// a wavy horizontal band from x0 to x1 at y, as a chain of capsules
const wave = (x0, x1, y, amp, w, turns, ph = 0) => {
  const N = 20, pts = [];
  for (let i = 0; i <= N; i++) { const t = i / N; pts.push([x0 + (x1 - x0) * t, y - amp * Math.sin(ph + t * turns * 2 * Math.PI)]); }
  return chain(pts, w);
};

const G = {
  'teacher': (g, P) => {           // someone at a blackboard, pointing at the chalk
    const FIG = [['c', 10.5, 17, 5], ['r', 3.5, 25, 14, 20, 6], ...chain([[14.5, 28], [20, 23], [26, 17]], 3.4)];
    g.fill(P.rect(16, 4, 29, 21, 1.5)).cut('M21.5 10.5H38', 1.8).cut('M30 17.5H39', 1.8);
    g.fill(P.cap(22, 24, 20.5, 45, 3)).fill(P.cap(39, 24, 40.5, 45, 3));
    knock(g, FIG, 2);
    g.layer(); put(g, FIG);
  },
  'crowd': (g, P) => {             // three people together, the middle one in front
    const MID = [['c', 24, 16, 6], ['p', 'M12 45C12 33 17 27.5 24 27.5C31 27.5 36 33 36 45Z']];
    for (const x of [11, 37]) { g.fill(P.circ(x, 12.5, 5)); g.fill(`M${x - 9} 45C${x - 9} 31 ${x - 5} 22 ${x} 22C${x + 5} 22 ${x + 9} 31 ${x + 9} 45Z`); }
    g.cutFill(P.circ(24, 16, 8.2)).cutFill('M9.5 47C9.5 32 15.5 25.3 24 25.3C32.5 25.3 38.5 32 38.5 47Z');
    g.layer(); put(g, MID);
  },
  'elder': (g, P) => {             // a stooped old figure leaning on a crook-handled stick
    g.fill(P.circ(27, 10.5, 5.2));
    g.fill('M15 30.5C13.5 24 15.5 17 21.5 15C25 14 27.5 16 27 19.5L23.5 30.5Z');
    put(g, chain([[23.5, 19], [28.5, 24.5], [33, 24.5]], 4));
    put(g, chain([[17.5, 29.5], [15.5, 37], [16, 44.5]], 5)); put(g, chain([[21, 29.5], [25, 36.5], [23.5, 44.5]], 5));
    g.fill(P.cap(16, 44.5, 20, 44.5, 3.2)); g.fill(P.cap(23.5, 44.5, 27.5, 44.5, 3.2));
    g.fill(P.cap(35, 24.5, 37, 45, 3.2)); g.fill(P.arc(31.8, 24, 3.3, 180, 360, 3));
  },
  'dancer': (g, P) => {            // a dancer, both arms flung up, one knee lifted
    g.fill(P.circ(25, 7.5, 4.8));
    g.fill(P.cap(24.5, 15.5, 23, 27, 7));
    put(g, chain([[21.5, 16], [15, 12], [12.5, 4.5]], 3.6)); put(g, chain([[27.5, 16], [34, 13], [38, 6]], 3.6));
    put(g, chain([[24, 28], [27, 36.5], [26.5, 44.5]], 4.4)); g.fill(P.cap(26.5, 44.5, 30, 44.5, 3));
    put(g, chain([[21.5, 28], [13, 32], [17.5, 39]], 4.4));
  },
  'hug': (g, P) => {               // two people leaning into a hug, heads together, an arm across the other's back
    const L = [['c', 18.5, 12, 5], ['k', 13, 41, 19.5, 24.5, 12]], ARM = chain([[21, 26], [28, 26], [34.5, 30]], 3.6);
    g.fill(P.circ(29.5, 12, 5)); g.fill(P.cap(35, 41, 28.5, 24.5, 12));
    knock(g, [...L, ...ARM], 1.8);
    g.layer(); put(g, [...L, ...ARM]);
  },
  'shrug': (g, P) => {             // someone shrugging, forearms up, palms open
    g.fill(P.circ(23.5, 10, 5.4));
    g.fill('M16.5 22C16.5 19.5 18.5 18 21 18H27C29.5 18 31.5 19.5 31.5 22V45H16.5Z');
    put(g, chain([[17.5, 21.5], [10, 30], [6, 21]], 3.6)); put(g, chain([[30.5, 21.5], [38, 30], [42, 21]], 3.6));
    g.fill(P.lens(2.5, 19, 8.5, 18, 1.2)); g.fill(P.lens(39.5, 18, 45.5, 19, 1.2));
  },
  'hiding': (g, P) => {            // someone peering over a brick wall: the top of a head and two eyes
    const eye = (x, y) => `M${x - 1.9} ${y}a1.9 2.9 0 1 0 3.8 0a1.9 2.9 0 1 0 -3.8 0Z`;
    g.fill(P.circ(24, 24, 11.5)).cutFill(eye(19.6, 21)).cutFill(eye(28.4, 21)).cutFill(P.rect(0, 28.5, 48, 20));
    g.layer();
    g.fill(P.rect(3, 31, 42, 14, 1.2)).cut('M3 38H45', 1.6).cut('M24 38V45', 1.6).cut('M10.5 38V45', 1.6).cut('M37.5 38V45', 1.6)
      .cut('M17 31V38', 1.6).cut('M31 31V38', 1.6);
  },
  'figure-bowing': (g, P) => {     // standing, bent deep at the waist, head low, an arm hanging: saying sorry
    g.fill(P.cap(15, 28, 14, 44, 5.6)); g.fill(P.cap(18, 28, 20, 44, 5.2));
    g.fill(P.cap(15, 26, 32, 22, 9));
    g.fill(P.circ(38.5, 26.5, 4.8));
    g.fill(P.cap(30, 23, 31, 36, 3.8));
  },
  'round-table': (g, P) => {       // a council: people seated at both ends of a table and one behind it
    g.fill(P.circ(24, 9.5, 4.6)); g.fill('M17 26V20C17 17.5 19 16 21.5 16H26.5C29 16 31 17.5 31 20V26Z');
    g.fill(P.rect(11, 26, 26, 4, 1.4)); g.fill(P.cap(15, 30, 15, 45, 3)); g.fill(P.cap(33, 30, 33, 45, 3));
    for (const s of [1, -1]) {
      const X = (x) => 24 + s * (x - 24);
      g.fill(P.circ(X(5.5), 15, 4.4)); g.fill(P.cap(X(5.5), 22, X(5.5), 31.5, 6));
      g.fill(P.cap(X(6), 33, X(11), 33, 4)); g.fill(P.cap(X(11), 33, X(11), 44.5, 3.6));
      g.fill(P.cap(X(3), 25, X(3), 45, 3));
    }
  },
  'swimmer': (g, P) => {           // a swimmer mid-stroke, an arm over, waves below
    g.fill(P.circ(12, 25.5, 4.8));
    g.fill(P.cap(18.5, 29, 37, 31, 6));
    put(g, chain([[20, 27], [26, 17], [17, 13]], 3.6));
    put(g, wave(3, 45, 38, 2, 3.2, 2.5)); put(g, wave(8, 40, 44.5, 1.5, 2.8, 2));
  },
  'diver': (g, P) => {             // a diver arcing down headfirst, arms out ahead, about to break the water
    g.fill(P.circ(26.5, 29.5, 4.9));
    put(g, [['k', 27, 22, 39.5, 33.5, 3.6], ['k', 27, 22.5, 18, 14.5, 7.8], ...chain([[18, 14.5], [10.5, 9.5], [5, 8.5]], 5), ['k', 5, 8.5, 4, 4.5, 3]]);
    put(g, wave(3, 45, 42.5, 1.4, 3, 3));
    g.fill(P.lens(46, 37.5, 43.5, 33, 1)); g.fill(P.lens(34, 37.5, 36.5, 33, 1));
  },
  'cartwheel': (g, P) => {         // a cartwheel: hands on the ground, legs flung up in a wide V
    const UP = [['c', 24, 9.5, 4.8], ['k', 24, 17, 24, 27, 6.4], ...chain([[22, 18], [15, 12], [10, 5]], 3.6), ...chain([[26, 18], [33, 12], [38, 5]], 3.6),
      ...chain([[22.5, 28], [17, 36], [12, 44]], 4.2), ...chain([[25.5, 28], [31, 36], [36, 44]], 4.2)];
    put(g, turn(UP, 160, 24, 22, 0, 1));
    g.fill(P.cap(4, 45, 30, 45, 2.6));
  },
  'wrestlers': (g, P) => {         // two people grappling, bent forward and braced, arms locked on each other's shoulders
    for (const s of [1, -1]) {
      const X = (x) => 24 + s * (x - 24);
      g.fill(P.circ(X(18.5), 13.5, 4.4));
      g.fill(P.cap(X(10), 28.5, X(18.5), 21.5, 8));
      put(g, chain([[X(9.5), 29], [X(4.5), 44.5]], 4.6)); put(g, chain([[X(11.5), 30.5], [X(16), 37.5], [X(15), 44.5]], 4.6));
      put(g, chain([[X(18), 20.5], [X(26.5), 20], [X(30), 24]], 3.4));
    }
  },
  'wheelchair': (g, P) => {        // a wheelchair, side view: push handle, back, seat, big wheel, footrest, front caster
    g.hole(P.circ(20, 32, 12.5), P.circ(20, 32, 8.3)); g.fill(P.circ(20, 32, 2.8));
    put(g, chain([[7.5, 6.5], [12.5, 6.5], [14, 23]], 3.8));
    g.fill(P.rect(12, 20.5, 23, 4.8, 1.6));
    put(g, chain([[33, 23], [37.5, 36.5], [43, 36.5]], 3.8));
    g.hole(P.circ(36.5, 42, 3.8), P.circ(36.5, 42, 1.4));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
