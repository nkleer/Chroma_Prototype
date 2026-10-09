// Option icons, batch p2: stage and screen, science kit, the hunt, and the tribal and magic worlds.
const { glyph, P } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f = (n) => Math.round(n * 100) / 100;
// local frame: origin (ox, oy), x axis turned by deg (clockwise); returns a point mapper
const frame = (ox, oy, deg) => { const c = Math.cos(rad(deg)), s = Math.sin(rad(deg)); return (x, y) => [ox + x * c - y * s, oy + x * s + y * c]; };
const polyIn = (F, pts) => P.poly(pts.map(([x, y]) => F(x, y)));
// an ellipse centred on (cx, cy)
const ell = (cx, cy, rx, ry) => `M${f(cx - rx)} ${f(cy)}A${rx} ${ry} 0 1 0 ${f(cx + rx)} ${f(cy)}A${rx} ${ry} 0 1 0 ${f(cx - rx)} ${f(cy)}Z`;
// a polyline as path data
const line = (pts) => 'M' + pts.map(([x, y]) => `${f(x)} ${f(y)}`).join('L');
// a thick line through points, as round-ended strokes
// where the ray from p at angle a (deg) meets the line y = Y
const hitY = (p, a, Y) => { const t = (Y - p[1]) / Math.sin(rad(a)); return [p[0] + Math.cos(rad(a)) * t, Y]; };
const trail = (g, pts, w) => { for (let k = 0; k < pts.length - 1; k++) g.fill(P.cap(...pts[k], ...pts[k + 1], w)); };
// points along a spiral from radius r0 outwards, `pitch` per turn
const spiral = (cx, cy, r0, pitch, turns, a0 = 0, step = 0.12) => {
  const pts = [];
  for (let t = 0; t <= turns * 2 * Math.PI + 1e-6; t += step) { const r = r0 + pitch * t / (2 * Math.PI); pts.push([cx + Math.cos(t + a0) * r, cy + Math.sin(t + a0) * r]); }
  return pts;
};

const G = {
  'spotlight': (g, P) => {         // a stage lamp hung from a bar, its beam falling to a pool of light on the floor
    const deg = 62, F = frame(13, 12, deg);
    g.fill(P.cap(3.5, 4, 25, 4, 3.2)); g.fill(P.cap(13, 4, 13, 12, 3.2));
    g.fill(polyIn(F, [[-6, -6], [5, -6], [5, -8], [9.5, -8], [9.5, 8], [5, 8], [5, 6], [-6, 6]]));
    g.fill(P.cap(...F(-6, -3.2), ...F(-6, 3.2), 6));
    const a = F(13.2, -8.3), b = F(13.2, 8.3);
    g.fill(P.cap(...a, ...hitY(a, deg - 18, 38), 3.2)); g.fill(P.cap(...b, ...hitY(b, deg + 18, 38), 3.2));
    g.fill(ell(28.5, 42, 14, 3.8));
  },
  'stage-curtain': (g, P) => {     // a stage, its heavy curtains swept open under a swagged pelmet
    g.fill('M3 3H45V9.5Q38 16 31 9.5Q24 16 17 9.5Q10 16 3 9.5Z');
    g.fill('M3 12H21C19 20 14.5 25.5 10 29C12.5 32 14 35.5 14 39H3Z').cut('M7.5 14V26.5', 1.6).cut('M12.5 14C12.5 19 11.5 22 10 25', 1.6);
    g.fill('M45 12H27C29 20 33.5 25.5 38 29C35.5 32 34 35.5 34 39H45Z').cut('M40.5 14V26.5', 1.6).cut('M35.5 14C35.5 19 36.5 22 38 25', 1.6);
    g.fill(P.rect(2, 40.5, 44, 5, 1.2));
  },
  'radio': (g, P) => {             // a portable radio: carry handle, one aerial, a round speaker and a tuning dial
    g.fill(P.cap(34, 17, 41, 4, 2.8)); g.fill(P.circ(41.5, 3.6, 2.4));
    g.fill(P.arc(16, 17, 6, 180, 360, 3));
    g.fill(P.rect(4, 16.5, 40, 27, 4)).cut(P.circ(15.5, 30, 6.8), 2.2).cutFill(P.circ(15.5, 30, 2.2))
      .cutFill(P.rect(27.5, 22, 12, 5, 1)).cutFill(P.circ(33.5, 35, 3));
  },
  'specimen-jar': (g, P) => {      // a lidded glass jar with a pressed leaf inside
    g.fill(P.rect(10, 4, 28, 7, 2)).cut('M16 6.5V8.5', 1.6).cut('M24 6.5V8.5', 1.6).cut('M32 6.5V8.5', 1.6);
    g.hole(P.rect(9, 13, 30, 32, 4), P.rect(12.5, 16.5, 23, 25, 2.5));
    g.fill(P.lens(19.5, 37, 30, 19.5, 5.2)).cut('M21 35L28 21.5', 1.5);
    g.fill(P.cap(17.8, 38.8, 20.3, 36, 2.6));
  },
  'gauge': (g, P) => {             // a dial meter: a half-round face with ticks and a needle
    g.fill('M4 34A20 20 0 0 1 44 34V39.5C44 40.9 42.9 42 41.5 42H6.5C5.1 42 4 40.9 4 39.5Z')
      .cutFill('M8 34A16 16 0 0 1 40 34Z');
    g.layer();
    for (const a of [195, 232, 270, 308, 345]) g.fill(P.cap(24 + Math.cos(rad(a)) * 9.5, 34 + Math.sin(rad(a)) * 9.5, 24 + Math.cos(rad(a)) * 12.5, 34 + Math.sin(rad(a)) * 12.5, 2.4));
    const N = frame(24, 34, -48);
    g.fill(polyIn(N, [[0, -2.2], [13.8, -0.6], [13.8, 0.6], [0, 2.2]]));
    g.fill(P.circ(24, 34, 3.8));
  },
  'server': (g, P) => {            // a stack of server units, each with a drive slot and a light
    for (const y of [4, 14.2, 24.4, 34.6]) {
      g.fill(P.rect(9, y, 30, 8, 1.6)).cut(`M13.5 ${y + 4}H25`, 2).cutFill(P.circ(33.5, y + 4, 1.9));
    }
    g.fill(P.cap(12.5, 44.5, 15.5, 44.5, 2.8)); g.fill(P.cap(32.5, 44.5, 35.5, 44.5, 2.8));
  },
  'clapperboard': (g, P) => {      // a film clapperboard, the striped clapper open
    g.fill(P.rect(5, 21, 38, 23, 2.4));
    g.fill(P.rect(5, 14.5, 38, 5.6, 1)).cutFill(P.poly([[11, 14.5], [15.5, 14.5], [12.5, 20.1], [8, 20.1]]))
      .cutFill(P.poly([[20, 14.5], [24.5, 14.5], [21.5, 20.1], [17, 20.1]])).cutFill(P.poly([[29, 14.5], [33.5, 14.5], [30.5, 20.1], [26, 20.1]]))
      .cutFill(P.poly([[38, 14.5], [42.5, 14.5], [39.5, 20.1], [35, 20.1]]));
    const F = frame(5.5, 12.5, -22);
    g.fill(polyIn(F, [[0, -5.6], [38, -5.6], [38, 0], [0, 0]]));
    for (const x of [6, 15, 24, 33]) g.cutFill(polyIn(F, [[x, -5.6], [x + 4.5, -5.6], [x + 1.5, 0], [x - 3, 0]]));
  },
  'film-camera': (g, P) => {       // a cine camera with two film reels on top and a flared lens hood
    g.hole(P.circ(10, 15, 6), P.circ(10, 15, 1.7));
    g.hole(P.circ(26.5, 12.5, 8.5), P.circ(26.5, 12.5, 2), P.circ(26.5, 7.3, 1.6), P.circ(31, 15.1, 1.6), P.circ(22, 15.1, 1.6));
    g.fill(P.rect(4, 23, 28, 17, 2.5));
    g.fill(P.rect(31, 27.5, 5, 8));
    g.fill(P.poly([[35, 27], [45, 21.5], [45, 41.5], [35, 36]]));
    g.fill(P.poly([[13, 40], [23, 40], [25, 45], [11, 45]]));
  },
  'fishing-rod': (g, P) => {       // a fishing rod bent over, the line hanging from its tip with a float and a hook
    g.fill(P.cap(5, 45, 12.5, 37.5, 5.6));
    const rod = []; for (let i = 0; i <= 12; i++) { const t = i / 12; rod.push([(1 - t) ** 2 * 12 + 2 * (1 - t) * t * 25 + t * t * 39, (1 - t) ** 2 * 38 + 2 * (1 - t) * t * 4 + t * t * 6]); }
    for (let i = 0; i < rod.length - 1; i++) g.fill(P.cap(...rod[i], ...rod[i + 1], 4.4 - 1.4 * i / 11));
    g.hole(P.circ(15.5, 41.5, 4.6), P.circ(15.5, 41.5, 1.6));
    g.fill(P.cap(39, 6, 39, 36, 2.4));
    g.fill(P.lens(39, 15, 39, 29, 4)).cut('M34 22H44', 1.8);
    g.fill(P.arc(35.8, 37.5, 3.2, 0, 180, 2.8)); g.fill(P.poly([[31, 38], [32.4, 33.5], [34.4, 38]]));
  },
  'staff': (g, P) => {             // a tall staff with a gnarled knot at its head and two feathers hung from it
    g.fill(P.cap(18, 46, 26, 12, 5));
    g.fill('M26 1.5C31.5 1 35 4.5 34.5 9C34 13 30.5 15.5 26.5 15C22.5 14.5 19.5 11.5 20 7.5C20.3 4 22.5 1.8 26 1.5Z').cut('M24.5 6.5C26.5 5.5 29 6.5 29.5 8.5', 1.6);
    g.fill(P.cap(31, 13.5, 33, 18, 2.4)); g.fill(P.lens(32.5, 17, 34, 36, 3.4)).cut('M32.8 19L33.8 34', 1.4);
    g.fill(P.cap(33.5, 11.5, 38, 15, 2.4)); g.fill(P.lens(38, 14, 42.5, 31, 3)).cut('M38.4 16L42 29', 1.4);
  },
  'deer': (g, P) => {              // a stag standing side on, branching antlers
    g.fill(P.rect(8, 22, 25, 11, 5.5));
    for (const [x, d] of [[11, -1], [16, 0.5], [27, 0], [32, 0.5]]) g.fill(P.cap(x, 30, x + d, 45, 3));
    g.fill(P.cap(9, 24, 6, 20, 3.2));
    g.fill(P.poly([[27, 23], [31, 12.5], [37.5, 12.5], [34, 27]]));
    g.fill(P.cap(33.5, 14, 42, 18.5, 6)).cutFill(P.circ(35.8, 14, 1.3));
    g.fill(P.lens(31, 13.5, 26, 10, 1.8));
    trail(g, [[33, 11.5], [31.5, 6.5], [27, 3.5]], 2.6); g.fill(P.cap(31.5, 6.5, 33.5, 2.5, 2.6)); g.fill(P.cap(32.3, 9, 28.5, 8.5, 2.6));
    trail(g, [[36, 11], [38.5, 6], [43, 4]], 2.6); g.fill(P.cap(38.5, 6, 37.5, 2, 2.6)); g.fill(P.cap(37.4, 8.4, 41.5, 9, 2.6));
  },
  'feather': (g, P) => {           // a long feather, its vane split in two places, the bare quill below
    g.fill('M12 3C20 4.5 31 16 31 33L28.5 37C17.5 33 8 22 8 11C8 7 9.5 4 12 3Z')
      .cut('M12 4.5C18 12 25 23 29.5 36', 1.6).cutFill(P.poly([[8, 16.5], [16.5, 19.5], [8.6, 19]])).cutFill(P.poly([[31.5, 22], [24.5, 22.8], [31.2, 25.6]]));
    g.fill(P.cap(29.5, 36, 34.5, 45, 2.8));
  },
  'standing-stone': (g, P) => {    // two rough standing stones, a spiral carved on the taller one
    g.fill(P.poly([[12.5, 44], [11, 28], [12, 15], [16, 6], [21.5, 1.8], [26.5, 8], [29.5, 18], [30.5, 30], [30, 44]]))
      .cut(line(spiral(21, 24, 1, 4.4, 1.3, 0)), 2);
    g.fill(P.poly([[33, 44], [32.5, 30], [34, 22], [38, 17], [42, 21], [44, 30], [44.5, 44]]));
    g.fill(P.cap(3, 44.5, 45, 44.5, 3));
  },
  'tribal-mask': (g, P) => {       // a tall narrow carved mask: zigzag brow band, slit eyes, a long nose, a small mouth
    g.fill('M24 2C30 2 33 5.5 33 11.5V28C33 36 29 42.5 24 46.5C19 42.5 15 36 15 28V11.5C15 5.5 18 2 24 2Z')
      .cut('M17.5 10L20.5 7L23.5 10L26.5 7L29.5 10L31 8.5', 1.8)
      .cutFill(P.lens(17, 18, 22.3, 18, 1.7)).cutFill(P.lens(25.7, 18, 31, 18, 1.7))
      .cut('M22.3 21.5V30.5H25.7V21.5', 1.4).cutFill(P.rect(20.5, 35, 7, 3.4, 1.2));
  },
  'spirit': (g, P) => {            // a soft wisp rising, its tail curling, two dot eyes
    g.fill('M24 4C31 4 35.5 9 35.5 15.5C35.5 24 30 29 26 33C23 36 22.5 39.5 25.5 41C28 42 30.5 40.5 31 38C33 41.5 31 45.5 26.5 45.5C19.5 45.5 16.5 39 19 33C16 29 12.5 24 12.5 15.5C12.5 9 17 4 24 4Z')
      .cutFill(ell(20, 15, 1.7, 2.3)).cutFill(ell(28, 15, 1.7, 2.3));
  },
  'wand': (g, P) => {              // a wand with a spark bursting at its tip
    g.fill(P.cap(7, 42, 15, 34, 5.4)).cut('M12.6 32.6L16.4 36.4', 1.6);
    g.fill(P.cap(15, 34, 28.5, 20.5, 3.4));
    g.fill(P.star(35, 13, 10, 2.8, 4, -90));
    g.fill(P.star(42.5, 26, 4.2, 1.3, 4, -90)); g.fill(P.circ(25.5, 7, 1.8));
  },
  'wagon': (g, P) => {             // a covered wagon, side on: hooped canvas, a plank bed, big spoked wheels, the shaft
    g.fill('M6 24V15C6 8 11 4.5 18 4.5H30C37 4.5 42 8 42 15V24Z').cut('M15.5 6.5V22', 1.8).cut('M24 5.5V22', 1.8).cut('M32.5 6.5V22', 1.8);
    g.fill(P.rect(4, 26, 40, 7.5, 1.2));
    g.fill(P.cap(43, 31, 47, 37, 2.8));
    for (const [x, y, r] of [[13, 36, 9], [35, 37.5, 7.5]]) g.cutFill(P.circ(x, y, r + 1.9));
    g.layer();
    for (const [x, y, r] of [[13, 36, 9], [35, 37.5, 7.5]]) {
      g.hole(P.circ(x, y, r), P.circ(x, y, r - 2.8));
      g.fill(P.circ(x, y, 2.4));
      for (const a of [0, 60, 120]) g.fill(P.cap(x + Math.cos(rad(a)) * (r - 2), y + Math.sin(rad(a)) * (r - 2), x - Math.cos(rad(a)) * (r - 2), y - Math.sin(rad(a)) * (r - 2), 2.2));
    }
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, fn]) => glyph(n, fn)) };
