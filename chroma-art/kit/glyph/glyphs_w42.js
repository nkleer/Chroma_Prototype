// World panel icons, batch w42: hard times and disasters, public figures rising and falling, and the online age.
const { glyph, P } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f = (n) => Math.round(n * 100) / 100;
const HEART = 'M24 42C10 32 4 25 4 17C4 10 9 6 15 6C19 6 22 8 24 11C26 8 29 6 33 6C39 6 44 10 44 17C44 25 38 32 24 42Z';
// apply a point transform to a path made only of absolute M, L, C, Q and Z commands
const xf = (d, fn) => d.replace(/(-?\d*\.?\d+)[ ,]+(-?\d*\.?\d+)/g, (m, x, y) => fn(+x, +y).map(f).join(' '));
// scale about (24, 24) by s, then centre on (cx, cy)
const sc = (s, cx, cy) => (x, y) => [cx + (x - 24) * s, cy + (y - 24) * s];
// a thick line through points, as round-ended strokes
const trail = (g, pts, w) => { for (let k = 0; k < pts.length - 1; k++) g.fill(P.cap(...pts[k], ...pts[k + 1], w)); };
// a polyline as path data (for cuts)
const line = (pts) => 'M' + pts.map(([x, y]) => `${f(x)} ${f(y)}`).join('L');
// points along a quadratic curve
const quad = (a, c, b, n = 12) => { const pts = []; for (let i = 0; i <= n; i++) { const t = i / n, u = 1 - t; pts.push([u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]]); } return pts; };
// an arrowhead: tip, direction it points (deg, 0 = right, clockwise), length and half-width at its base
const head = (tip, deg, len, half) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg)), bx = tip[0] - c * len, by = tip[1] - s * len;
  return P.poly([tip, [bx - s * half, by + c * half], [bx + s * half, by - c * half]]);
};
// points along a sine wave from x0 to x1 about y
const sine = (x0, x1, y, amp, period, ph = 0, n = 24) => { const pts = []; for (let i = 0; i <= n; i++) { const x = x0 + (x1 - x0) * i / n; pts.push([x, y + amp * Math.sin(ph + 2 * Math.PI * (x - x0) / period)]); } return pts; };
// a polyline clipped to y0..y1 (its points run downwards)
const clipY = (pts, y0, y1) => {
  const out = [];
  for (let k = 0; k < pts.length - 1; k++) {
    const [a, b] = [pts[k], pts[k + 1]], at = (y) => [a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y];
    if (b[1] < y0 || a[1] > y1) continue;
    out.push(a[1] < y0 ? at(y0) : a);
    if (b[1] > y1) { out.push(at(y1)); break; }
    if (k === pts.length - 2) out.push(b);
  }
  return out;
};

// a four-pointed spark of radius R, k sets how full its sides are
const spark = (cx, cy, R, k) => `M${f(cx)} ${f(cy - R)}Q${f(cx + R * k)} ${f(cy - R * k)} ${f(cx + R)} ${f(cy)}Q${f(cx + R * k)} ${f(cy + R * k)} ${f(cx)} ${f(cy + R)}Q${f(cx - R * k)} ${f(cy + R * k)} ${f(cx - R)} ${f(cy)}Q${f(cx - R * k)} ${f(cy - R * k)} ${f(cx)} ${f(cy - R)}Z`;
// local frame: origin (ox, oy), turned by deg (clockwise); returns a point mapper
const frame = (ox, oy, deg) => { const c = Math.cos(rad(deg)), s = Math.sin(rad(deg)); return (x, y) => [ox + x * c - y * s, oy + x * s + y * c]; };
// a plain standing figure, feet at the frame's origin: round head, pill body, two legs, arms given as [shoulder, hand] pairs
const figure = (g, F, ...arms) => {
  g.fill(P.circ(...F(0, -22), 4.3));
  g.fill(P.cap(...F(0, -14.5), ...F(0, -8), 7.4));
  g.fill(P.cap(...F(-1.8, -7), ...F(-2.4, -1.4), 3.4)); g.fill(P.cap(...F(1.8, -7), ...F(2.4, -1.4), 3.4));
  for (const [a, b] of arms) g.fill(P.cap(...F(...a), ...F(...b), 3.2));
};

const G = {
  'chart-falling': (g, P) => {     // a bar chart stepping down, a jagged arrow falling over it
    g.fill(P.cap(4.5, 43.5, 43.5, 43.5, 3));
    for (const [x, y] of [[6, 18], [16, 24], [26, 30], [36, 36]]) g.fill(P.rect(x, y, 7, 42 - y, 1));
    trail(g, [[4.5, 5], [13, 13.5], [18.5, 9], [31.5, 22]], 3.2); g.fill(head([39.5, 30], 45, 9, 5.6));
  },
  'flame': (g, P) => {             // one tall flame of three deep tongues, the inner tongue carved out, two embers flying
    g.hole('M24 45.5C15 45.5 8.5 40 8.5 32C8.5 25 12 20.5 9.5 10.5C15 14 18.5 19 19.5 25C19 17 21.5 9 25.5 2C31 8.5 32 16 29.5 24C31.5 19.5 35 15.5 38.5 12.5C41 19 40 25.5 39.5 32C39 40.5 32.5 45.5 24 45.5Z',
      'M24 41.5C20.5 41.5 18.2 38.7 19 35C19.8 32 22.5 30.5 23.2 27.5C27 30 29.5 33.2 29 36.6C28.5 39.6 26.5 41.5 24 41.5Z');
    g.fill(P.circ(5, 4.5, 2)); g.fill(P.circ(43.5, 5.5, 2));
  },
  'quake': (g, P) => {             // ground split by a jagged crack, its right side dropped, shake marks over either side
    const K = [[28.5, 15], [20.5, 23.5], [28, 31], [21.5, 37], [25.5, 42], [23.5, 48]];
    const L = clipY(K, 20, 45), R = clipY(K, 27.5, 45).map(([x, y]) => [x + 4, y]);
    g.fill(P.poly([[3, 21], [9, 20], [15, 20.6], ...L, [3, 45]]));
    g.fill(P.poly([...R, [45, 45], [45, 28.5], [39, 27.6], [34, 28.2]]));
    for (const [r, a] of [[6.5, 36], [11.5, 30]]) { g.fill(P.arc(15, 11, r, 180 - a, 180 + a, 3)); g.fill(P.arc(33, 18, r, -a, a, 3)); }
  },
  'flood': (g, P) => {             // a house's roof and upper wall above rising water, two wave lines
    const W1 = sine(3, 45, 34.5, 1.6, 10.5, 0), W2 = sine(3, 45, 41.5, 1.6, 10.5, 0);
    g.fill(P.poly([[3.5, 18.5], [24, 3.5], [44.5, 18.5]])).fill(P.rect(32, 5.5, 5.5, 10, 0.6));
    g.fill(P.rect(9.5, 18.5, 29, 20)).cut('M3 18.5H45', 1.8).cutFill(P.rect(19.5, 21.5, 9, 4.6, 0.8));
    g.cut(line(W1), 3.4 + 4.4).cutFill(P.rect(2, 36, 44, 12));
    g.layer();
    trail(g, W1, 3.4); trail(g, W2, 3.4);
  },
  'figure-rising': (g, P) => {     // a figure on the top of three rising steps, arms up, an arrow curving up beside it
    g.fill(P.poly([[3, 45], [3, 39.5], [14, 39.5], [14, 34], [25, 34], [25, 28.5], [41, 28.5], [41, 45]])).cut('M14 40V45M25 34.5V45', 1.6);
    figure(g, frame(33, 28.5, 0), [[-3, -13], [-8, -20]], [[3, -13], [8, -20]]);
    trail(g, quad([5, 30], [16.5, 29.5], [17.5, 12.5]), 3.4); g.fill(head([17.6, 3.5], -88, 9, 5.2));
  },
  'figure-falling': (g, P) => {    // a figure tipping off the edge of a step, an arrow curving down beside it
    g.fill(P.poly([[3, 45], [3, 39.5], [11, 39.5], [11, 33.5], [19, 33.5], [19, 27.5], [26, 27.5], [26, 45]])).cut('M11 40V45M19 34V45', 1.6);
    figure(g, frame(24, 27.5, 52), [[-3, -13], [-9, -17]], [[3, -13], [6.5, -20.5]]);
    trail(g, quad([30.5, 33], [39.5, 31.5], [39.5, 37.5], 8), 3.4); g.fill(head([39.5, 45.5], 90, 8.5, 5.2));
  },
  'signal': (g, P) => {            // three signal arcs above a dot
    for (const r of [8.5, 17, 25.5]) g.fill(P.arc(24, 41, r, 225, 315, 5));
    g.fill(P.circ(24, 41, 3.8));
  },
  'chat-spark': (g, P) => {        // a speech bubble with a four-pointed spark (and a small one) inside
    g.fill(P.rect(3.5, 3.5, 41, 32.5, 11)); g.fill(P.poly([[9.5, 31], [7, 45.5], [22, 34]]))
      .cutFill(P.rect(7.6, 7.6, 32.8, 24.3, 7.2));
    g.layer();
    g.fill(spark(21, 20.5, 9.6, 0.2)); g.fill(spark(33.5, 14, 3.6, 0.2));
  },
  'phone-heart': (g, P) => {       // a smartphone standing upright, a heart on its screen
    g.fill(P.rect(11.5, 2.5, 25, 43, 5)).cutFill(P.rect(14.6, 8.5, 18.8, 29.5, 1.5)).cut('M21.5 5.6H26.5', 1.6).cutFill(P.circ(24, 41.6, 1.7));
    g.layer();
    g.fill(xf(HEART, sc(0.37, 24, 23.5)));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, fn]) => glyph(n, fn)) };
