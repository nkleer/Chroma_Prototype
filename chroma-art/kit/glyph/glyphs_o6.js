// Option icons, batch o6: vehicles, buildings, places and nature.
const { glyph, P } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
// a four-pointed twinkle, like the sparkle's
const twinkle = (cx, cy, R) => `M${cx} ${cy - R}Q${cx + R * 0.13} ${cy - R * 0.13} ${cx + R} ${cy}Q${cx + R * 0.13} ${cy + R * 0.13} ${cx} ${cy + R}Q${cx - R * 0.13} ${cy + R * 0.13} ${cx - R} ${cy}Q${cx - R * 0.13} ${cy - R * 0.13} ${cx} ${cy - R}Z`;
// wheels: carve a gap round each from the body layer, then draw them on a new layer with a hub hole
const wheels = (g, P, pts, r, gap = 1.9, hub = 1.9) => {
  for (const [x, y] of pts) g.cutFill(P.circ(x, y, r + gap));
  g.layer();
  for (const [x, y] of pts) if (hub) g.hole(P.circ(x, y, r), P.circ(x, y, hub)); else g.fill(P.circ(x, y, r));
};

const G = {
  'car': (g, P) => {               // a saloon car, side on, facing right
    g.fill('M3.5 34V27.5C3.5 25 5 23.5 7.5 23L14.5 21.5L19.5 13.5C20.3 12.2 21.5 11.5 23 11.5H31.5C33 11.5 34.1 12.2 34.9 13.4L40 21.5L42 22C44 22.6 45 24 45 26.5V34Z')
      .cutFill(P.poly([[18.5, 21.5], [22.5, 15], [26.6, 15], [26.6, 21.5]])).cutFill(P.poly([[29.4, 15], [32, 15], [36, 21.5], [29.4, 21.5]]));
    wheels(g, P, [[13.5, 34], [35, 34]], 5.6);
  },
  'bicycle': (g, P) => {           // a bicycle, side on
    for (const x of [11.5, 36.5]) g.hole(P.circ(x, 31, 9.6), P.circ(x, 31, 6.4));
    for (const x of [11.5, 36.5]) g.fill(P.circ(x, 31, 2));
    const BB = [23, 31], S = [19.5, 18.5], H = [32.5, 18.5];
    g.fill(P.cap(11.5, 31, ...BB, 2.8)); g.fill(P.cap(11.5, 31, ...S, 2.8)); g.fill(P.cap(...BB, ...S, 2.8));
    g.fill(P.cap(...BB, ...H, 2.8)); g.fill(P.cap(...S, ...H, 2.8)); g.fill(P.cap(...H, 36.5, 31, 2.8));
    g.fill(P.cap(15, 15.5, 22.5, 15.5, 3.2)); g.fill(P.cap(19.5, 16, 19.5, 18.5, 2.6));
    g.fill(P.cap(32.5, 18.5, 31.5, 13.5, 2.8)); g.fill(P.cap(29, 12.5, 34, 12.5, 2.8));
    g.fill(P.circ(...BB, 3.2));
  },
  'train': (g, P) => {             // a steam locomotive, side on, facing right
    g.fill(P.rect(2.5, 8, 16, 3.5, 1)); g.fill(P.rect(4, 10, 13, 22)).cutFill(P.rect(7, 14, 7, 7, 1));
    g.fill(P.rect(16, 17, 24, 13.5, 2.5)); g.fill('M21 17.5A3.5 3.5 0 0 1 28 17.5Z');
    g.fill(P.poly([[31, 17.5], [31, 10.5], [29.5, 6.5], [37.5, 6.5], [36, 10.5], [36, 17.5]]));
    g.fill(P.rect(3, 30, 39, 4.5, 1)); g.fill(P.poly([[39, 30], [46, 41], [38.5, 41]]));
    wheels(g, P, [[11.5, 38], [24.5, 38]], 6, 1.8, 0); g.fill(P.circ(34.5, 40.5, 3.6));
    g.cut('M11.5 38H24.5', 1.6);
  },
  'bus': (g, P) => {               // a single-decker bus, side on: a long row of windows
    g.fill(P.rect(3, 9, 42, 26, 4));
    for (const x of [6.5, 14, 21.5, 29]) g.cutFill(P.rect(x, 13, 5.5, 8, 1));
    g.cut(P.rect(36.8, 13.4, 4.6, 17.6, 0.6), 1.6);
    wheels(g, P, [[12, 35], [34, 35]], 5.4);
  },
  'van': (g, P) => {               // a camper van, side on, with a box on the roof rack
    g.fill(P.rect(9, 3.5, 22, 5.5, 1.6)); g.fill(P.cap(12.5, 8, 12.5, 12, 2.8)); g.fill(P.cap(27.5, 8, 27.5, 12, 2.8));
    g.fill('M3.5 35V14C3.5 12.5 4.5 11.5 6 11.5H36C37.5 11.5 38.5 12.3 39 13.5L41.5 22L43.5 23C44.5 23.6 45 24.5 45 26V35Z')
      .cutFill(P.rect(7, 15, 7, 7, 1)).cutFill(P.rect(16.5, 15, 7, 7, 1)).cutFill(P.poly([[30.5, 15], [36.2, 15], [38.4, 22], [30.5, 22]]))
      .cut('M27.2 15V31', 1.6);
    wheels(g, P, [[11.5, 35], [36, 35]], 5.4);
  },
  'suitcase': (g, P) => {          // an upright travel case with its handle pulled up, on two wheels
    g.fill(P.cap(19, 5, 29, 5, 3.4)); g.fill(P.cap(19, 5, 19, 15, 2.8)); g.fill(P.cap(29, 5, 29, 15, 2.8));
    g.fill(P.rect(11, 15, 26, 26, 3.5)).cut('M18 19V37', 2).cut('M30 19V37', 2);
    g.fill(P.circ(16, 43.5, 2.6)); g.fill(P.circ(32, 43.5, 2.6));
  },
  'bridge': (g, P) => {            // a humpbacked footbridge with its railing, water running under
    const q = (y0, yc, x) => { const t = (x - 3) / 42; return (1 - t) * (1 - t) * y0 + 2 * t * (1 - t) * yc + t * t * y0; };
    g.fill('M3 19Q24 3 45 19L45 22.4Q24 6.4 3 22.4Z');
    for (const x of [5, 14.5, 24, 33.5, 43]) g.fill(P.cap(x, q(21, 5, x), x, q(30, 14, x), 3.2));
    g.fill('M3 29Q24 13 45 29L45 36Q24 20 3 36Z');
    g.fill(P.cap(12, 39.5, 36, 39.5, 2.8)); g.fill(P.cap(18, 44.5, 30, 44.5, 2.8));
  },
  'tent': (g, P) => {              // a tent with its door flap tied back, poles crossed at the top
    g.fill(P.cap(24, 9, 19.5, 3, 2.8)); g.fill(P.cap(24, 9, 28.5, 3, 2.8));
    g.fill('M3 44Q14 35 24 8Q34 35 45 44Z')
      .cutFill('M24 17Q22 32 14.5 44H28.5Q25.5 31 24 17Z').cut('M24.5 18Q28 33 34 44', 1.6);
  },
  'cottage': (g, P) => {           // a little cottage, smoke from its chimney, a tree beside it
    g.fill(P.circ(11.5, 8.2, 2.8)); g.fill(P.circ(16.2, 4, 2.4));
    g.fill(P.rect(9, 13, 4.5, 10));
    g.fill(P.poly([[2, 28], [15.5, 14], [29, 28]]));
    g.fill(P.rect(5, 27, 21, 18)).cutFill(P.rect(17, 34, 5.5, 11, 1)).cutFill(P.rect(8.5, 31, 5.5, 5.5, 0.8));
    g.fill(P.circ(38.5, 24, 6.8)); g.fill(P.cap(38.5, 29, 38.5, 44.5, 3.2));
  },
  'barn': (g, P) => {              // a barn: gambrel roof, big crossed doors
    g.fill('M3.5 23L10 11.5L24 4.5L38 11.5L44.5 23H41V45H7V23Z').cut('M3 23H45', 1.6)
      .cut(P.rect(14, 28, 20, 18), 1.8).cut('M14 28L24 45M24 28L14 45M24 28L34 45M34 28L24 45M24 28V45', 1.6)
      .cutFill(P.rect(20.5, 12, 7, 6.5, 0.6));
  },
  'shop-front': (g, P) => {        // a shop front: sign, striped scalloped awning, window and door
    g.fill(P.rect(7, 3.5, 34, 6, 1.2));
    const n = 5, w = 40 / n, rr = w / 2;
    let d = 'M4 12H44V19.5'; for (let i = 0; i < n; i++) d += `A${rr} ${rr} 0 0 1 ${44 - (i + 1) * w} 19.5`; d += 'Z';
    g.fill(d); for (let i = 1; i < n; i++) g.cut(`M${4 + i * w} 12.5V19`, 1.6);
    g.layer();
    g.fill(P.rect(6, 26, 36, 19)).cutFill(P.rect(9.5, 29.5, 17, 10, 1)).cutFill(P.rect(30, 29.5, 8.5, 15.5));
  },
  'factory': (g, P) => {           // a factory: saw-tooth roof, two chimneys, a gate
    g.fill(P.rect(31, 5, 5.5, 20)); g.fill(P.rect(39, 11, 5, 14));
    g.fill('M3 45V25L12 17V25L21 17V25L30 17V24H45V45Z')
      .cutFill(P.rect(7, 29.5, 4, 4)).cutFill(P.rect(14.5, 29.5, 4, 4)).cutFill(P.rect(22, 29.5, 4, 4))
      .cutFill('M30 45V37A5.5 5.5 0 0 1 41 37V45Z');
    g.layer(); g.fill(P.cap(35.5, 33, 35.5, 45, 2.8));
  },
  'traffic-light': (g, P) => {     // a traffic light on its post
    g.fill(P.rect(15.5, 3, 17, 33.5, 4.5));
    for (const y of [10.5, 19.75, 29]) { g.cutFill(P.circ(24, y, 3.6)); g.fill(P.poly([[15.5, y - 4], [10.5, y - 4], [15.5, y + 1.5]])); g.fill(P.poly([[32.5, y - 4], [37.5, y - 4], [32.5, y + 1.5]])); }
    g.fill(P.rect(21.5, 36, 5, 9)); g.fill(P.rect(16, 42.5, 16, 3, 1));
  },
  'tree': (g, P) => {              // a full, round-crowned tree
    for (const [x, y, r] of [[24, 15, 11], [13.5, 21, 8], [34.5, 21, 8], [16.5, 11.5, 7], [31.5, 11.5, 7], [24, 25, 7.5]]) g.fill(P.circ(x, y, r));
    g.fill('M18.5 45C21 41 21.8 36 21.8 28H26.2C26.2 36 27 41 29.5 45Z');
    g.cut('M12 23A6 6 0 0 0 18 28', 1.6).cut('M30 28A6 6 0 0 0 36 23', 1.6);
  },
  'roots': (g, P) => {             // a tree on the ground line, its roots spread wide beneath
    for (const [x, y, r] of [[24, 10.5, 7.5], [16.5, 14, 5.5], [31.5, 14, 5.5]]) g.fill(P.circ(x, y, r));
    g.fill(P.rect(21.5, 15, 5, 17));
    for (const [a, b, w] of [[[24, 31], [14, 37.5], 4], [[14, 37.5], [5, 39.5], 2.8], [[14, 37.5], [11, 45], 2.8], [[24, 31], [20, 45], 3.4],
      [[24, 31], [34, 37.5], 4], [[34, 37.5], [43, 39.5], 2.8], [[34, 37.5], [37, 45], 2.8], [[24, 31], [28, 45], 3.4]]) g.fill(P.cap(...a, ...b, w));
    g.cutFill(P.rect(0, 24, 48, 7));
    g.layer(); g.fill(P.cap(4, 27.5, 44, 27.5, 3.2));
  },
  'fence': (g, P) => {             // a short picket fence
    for (let i = 0; i < 4; i++) { const x = 5 + i * 10; g.fill(P.poly([[x, 44], [x, 13], [x + 3.5, 7], [x + 7, 13], [x + 7, 44]])); }
    g.fill(P.rect(5, 19, 37, 4.2)); g.fill(P.rect(5, 33, 37, 4.2));
  },
  'wave': (g, P) => {              // a sea wave curling over
    g.fill('M3 45C5 34 12 20 23 12C31 6 41 6 44.5 13C46.5 17.5 43.5 22 39 21.5C41.5 19.5 41 16 38 15C33 13.5 27.5 18 27 25C26.5 33 33 39 45 39.5V45Z')
      .cut('M9 40C12 30 17 22 24 17', 1.6);
  },
  'moon': (g, P) => {              // a crescent moon with twinkling stars
    g.fill(P.circ(20, 26, 17)).cutFill(P.circ(13, 20.5, 16.5));
    g.fill(twinkle(38.5, 9, 6.5)); g.fill(twinkle(42, 27, 4)); g.fill(P.circ(38.5, 41.5, 2.2));
  },
  'firework': (g, P) => {          // a rocket's trail and its burst of sparks
    const cx = 27, cy = 17;
    for (let i = 0; i < 9; i++) {
      const a = rad(i * 40 - 70), c = Math.cos(a), s = Math.sin(a);
      g.fill(P.cap(cx + c * 4.5, cy + s * 4.5, cx + c * 11.5, cy + s * 11.5, 3.2)); g.fill(P.circ(cx + c * 15.5, cy + s * 15.5, 2.2));
    }
    g.fill(P.cap(9, 45, 11.5, 39, 2.8)); g.fill(P.cap(13.5, 35, 16.5, 30.5, 2.8));
  },
  'torch': (g, P) => {             // a torch (flashlight) throwing its beam up and right
    const f = (x, y) => { const c = Math.cos(rad(-45)), s = Math.sin(rad(-45)); return [15 + x * c - y * s, 33 + x * s + y * c]; };
    g.fill(P.cap(...f(-14, 0), ...f(0, 0), 7.6)).cut(`M${f(-7.5, 0).join(' ')}L${f(-4, 0).join(' ')}`, 2);
    g.fill(P.poly([f(-1, -3.8), f(5, -7), f(5, 7), f(-1, 3.8)]));
    for (const a of [-27, 0, 27]) { const q = (x, y) => f(x * Math.cos(rad(a)) - y * Math.sin(rad(a)), x * Math.sin(rad(a)) + y * Math.cos(rad(a))); g.fill(P.poly([q(9, -1.4), q(29, -3.6), q(29, 3.6), q(9, 1.4)])); }
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
