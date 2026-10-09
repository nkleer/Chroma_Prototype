// Option icons, batch o5: tools, making, science and seeing things.
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f2 = (n) => Math.round(n * 100) / 100;

// Turn a path about (cx, cy) by deg (clockwise on screen), scale by s, then move by (dx, dy).
// Handles M L H V C Q A Z, absolute and relative; arcs are assumed circular (rx = ry), as all of ours are.
function xf(d, deg, cx = 24, cy = 24, s = 1, dx = 0, dy = 0) {
  const c = Math.cos(rad(deg)), n = Math.sin(rad(deg));
  const T = (x, y) => { const u = (x - cx) * s, v = (y - cy) * s; return [f2(cx + dx + u * c - v * n), f2(cy + dy + u * n + v * c)]; };
  const tk = d.match(/[a-zA-Z]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?/g);
  let i = 0, x = 0, y = 0, sx = 0, sy = 0, cmd = '', out = '';
  const num = () => parseFloat(tk[i++]);
  const isNum = () => i < tk.length && !/[a-zA-Z]/.test(tk[i]);
  while (i < tk.length) {
    if (/[a-zA-Z]/.test(tk[i])) cmd = tk[i++];
    const rel = cmd === cmd.toLowerCase(), C = cmd.toUpperCase();
    const pt = () => { const a = num(), b = num(); return rel ? [x + a, y + b] : [a, b]; };
    if (C === 'Z') { out += 'Z'; x = sx; y = sy; continue; }
    if (C === 'M') { [x, y] = pt(); sx = x; sy = y; out += 'M' + T(x, y).join(' '); cmd = rel ? 'l' : 'L'; }
    else if (C === 'L') { [x, y] = pt(); out += 'L' + T(x, y).join(' '); }
    else if (C === 'H') { const a = num(); x = rel ? x + a : a; out += 'L' + T(x, y).join(' '); }
    else if (C === 'V') { const a = num(); y = rel ? y + a : a; out += 'L' + T(x, y).join(' '); }
    else if (C === 'C') { const p1 = pt(), p2 = pt(), p3 = pt(); out += 'C' + [p1, p2, p3].map((p) => T(...p).join(' ')).join(' '); [x, y] = p3; }
    else if (C === 'Q') { const p1 = pt(), p2 = pt(); out += 'Q' + [p1, p2].map((p) => T(...p).join(' ')).join(' '); [x, y] = p2; }
    else if (C === 'A') {
      const rx = num(), ry = num(), rot = num(), la = num(), sw = num(), p = pt();
      out += `A${f2(rx * s)} ${f2(ry * s)} ${f2(rot + deg)} ${la} ${sw} ${T(...p).join(' ')}`; [x, y] = p;
    } else throw new Error('path command ' + cmd);
  }
  return out;
}
// the same turn applied to a whole drawing: returns a P-like toolkit whose shapes come out turned
const turned = (P, deg, cx = 24, cy = 24, s = 1, dx = 0, dy = 0) => {
  const t = (d) => xf(d, deg, cx, cy, s, dx, dy);
  const Q = {};
  for (const k of Object.keys(P)) Q[k] = (...a) => t(P[k](...a));
  Q.d = t;
  return Q;
};
// a thick line through a list of points, as a chain of round-ended strokes
const trail = (g, P, pts, w) => { for (let k = 0; k < pts.length - 1; k++) g.fill(P.cap(...pts[k], ...pts[k + 1], w)); };
// points along a spiral: centre, start radius, growth per turn, turns, start angle
const spiral = (cx, cy, r0, pitch, turns, a0, step = 0.08) => {
  const pts = [];
  for (let t = 0; t <= turns * 2 * Math.PI + 1e-6; t += step) { const r = r0 + pitch * t / (2 * Math.PI); pts.push([cx + Math.cos(t + a0) * r, cy + Math.sin(t + a0) * r]); }
  return pts;
};
// the same polyline with its points spaced evenly
const resample = (pts, step) => {
  const out = [pts[0]]; let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const [ax, ay] = pts[i - 1], [bx, by] = pts[i], seg = Math.hypot(bx - ax, by - ay); let t0 = 0;
    while (acc + seg * (1 - t0) >= step) { t0 += (step - acc) / seg; out.push([ax + (bx - ax) * t0, ay + (by - ay) * t0]); acc = 0; }
    acc += seg * (1 - t0);
  }
  return out;
};
// slanted cuts across a strand (a rope's twist), every `every` points from index k0
const twist = (g, pts, k0, every, half, sl, w) => {
  for (let k = k0; k < pts.length - 1; k += every) {
    const [x, y] = pts[k], [x2, y2] = pts[k + 1], d = Math.hypot(x2 - x, y2 - y), tx = (x2 - x) / d, ty = (y2 - y) / d;
    g.cut(`M${f2(x - ty * half - tx * sl)} ${f2(y + tx * half - ty * sl)}L${f2(x + ty * half + tx * sl)} ${f2(y - tx * half + ty * sl)}`, w);
  }
};

const G = {
  'hammer': (g, P) => {            // a claw hammer on its own, tilted
    const Q = turned(P, 40, 24, 24, 1.02, 1, 0);
    g.fill(Q.d('M9 6.5H21V16.5H9Z'));                                 // striking face
    g.fill(Q.d('M20 7.5H29C33 7.5 37 10 40 14.5L37.5 16C35 13.5 32 13 29 15.5H20Z'));   // cheek and claw
    g.fill(Q.rect(21, 14, 6.2, 18, 1));                               // handle top
    g.fill(Q.rect(20, 30, 8.2, 16, 3.6)).cut(Q.d('M20.5 33.5H27.5'), 1.8);   // grip
  },
  'spade': (g, P) => {             // a garden spade: D-grip, shaft, a blade with flat treads
    const Q = turned(P, 18, 24, 24);
    g.hole(Q.rect(16.5, 2.5, 15, 10, 3.5), Q.rect(20, 5.5, 8, 4, 1.2));
    g.fill(Q.rect(21.6, 10, 4.8, 17, 1));
    g.fill(Q.d('M20 23H28L29 27.5H19Z'));
    g.fill(Q.d('M14.5 27H33.5V36C33.5 41.5 29 45.5 24 46C19 45.5 14.5 41.5 14.5 36Z')).cut(Q.d('M24 31V40.5'), 1.8);
  },
  'wrench': (g, P) => {            // a double open-ended spanner
    const Q = turned(P, 45, 24, 24);
    g.fill(Q.rect(21.2, 8, 5.6, 32, 2));
    g.fill(Q.circ(24, 6.5, 8.6)).cutFill(Q.d('M20.6 -4H27.4V7.5Q24 9.5 20.6 7.5Z'));
    g.fill(Q.circ(24, 41.5, 7.4)).cutFill(Q.d('M21.1 52H26.9V42.5Q24 40.8 21.1 42.5Z'));
  },
  'watering-can': (g, P) => {      // a watering can, tipped to pour, drops falling from the rose
    const Q = turned(P, 12, 20, 30);
    g.fill(Q.d('M5 20H27V42C27 43.7 25.7 45 24 45H8C6.3 45 5 43.7 5 42Z')).cut(Q.d('M4.5 25.5H27.5'), 1.6);
    g.fill(Q.arc(13, 21, 8.5, 180, 300, 3.4)); g.fill(Q.cap(9, 13.6, 17.5, 13.6, 3.4));
    const [sx, sy, ex, ey] = [26, 38, 36, 20], L = Math.hypot(ex - sx, ey - sy), ux = (ex - sx) / L, uy = (ey - sy) / L;
    const at = (u, v) => [ex + ux * u - uy * v, ey + uy * u + ux * v];
    g.fill(Q.cap(sx, sy, ex, ey, 3.4));
    g.fill(Q.d(P.poly([at(-1, -1.8), at(5, -5.6), at(5, 5.6), at(-1, 1.8)])));   // the rose
    g.layer();
    for (const [x, y] of [[43.2, 28], [39.8, 35], [43.8, 39.5]]) g.fill(P.lens(x, y - 2.6, x, y + 2.6, 1.3));
  },
  'needle': (g, P) => {            // a reel of thread, its thread running up into a needle's eye
    g.fill(P.rect(3, 14, 24, 5, 1.8)); g.fill(P.rect(3, 40, 24, 5, 1.8));
    g.fill(P.rect(6, 18, 18, 23, 1)).cut('M6 24.5L24 28.5', 1.8).cut('M6 31.5L24 35.5', 1.8);
    g.fill('M40.2 4C42.6 4.2 44 5.8 43.5 8.2L35 39.5L31.5 46L31.6 38.8L37.6 7.2C38.1 5 38.8 4 40.2 4Z').cutFill(P.lens(40.6, 6.8, 39.1, 12.4, 0.35));
    g.layer();
    trail(g, P, [[15, 14], [16, 8.5], [20, 4.5], [26, 3], [32, 3.6], [36, 6], [39.6, 9.6]], 2.8);
  },
  'paintbrush': (g, P) => {        // an artist's brush over the stroke of paint it has just laid down
    const Q = turned(P, -42, 24, 20, 0.92);
    g.fill(Q.d('M24 1.5C26.3 1.5 27.8 3.2 27.8 6L28.6 22H19.4L20.2 6C20.2 3.2 21.7 1.5 24 1.5Z'));
    g.fill(Q.rect(18.6, 21.5, 10.8, 9, 1.2)).cut(Q.d('M18.4 25.8H29.6'), 1.8);
    g.fill(Q.d('M19 31.5H29C31.5 35 31.5 39.5 29.5 42.5C28 44.5 26 46 24 48.5C22 46 20 44.5 18.5 42.5C16.5 39.5 16.5 35 19 31.5Z'));
    g.fill('M38 42C34 37 30 41 26 40C22 39 18 35 13 38C10 40 7 39 4 37C5 41 8 44 12.5 43C17 42 20 45 25 45C31 45 34 43 38 42Z');
  },
  'set-square': (g, P) => {        // a drawing set square with a pencil laid along its long edge
    g.hole(P.poly([[4, 45], [4, 12], [37, 45]]), P.poly([[10, 39.5], [10, 26], [23.5, 39.5]]))
      .cut('M4 19H8', 1.6).cut('M4 26H8', 1.6).cut('M4 33H8', 1.6);
    const Q = turned(P, -45, 24, 24, 1, 6.5, -6.5);
    g.fill(Q.d('M21 3.5H27V33L24 40.5L21 33Z')).cut(Q.d('M20.5 33H27.5'), 1.6).cut(Q.d('M20.5 9H27.5'), 1.6);
  },
  'cog': (g, P) => {               // a single gear wheel
    const pts = [], N = 8;
    for (let k = 0; k < N; k++) {
      const a0 = k * 360 / N - 90;
      for (const [da, r] of [[-15, 15], [-10, 21], [10, 21], [15, 15]]) pts.push([24 + Math.cos(rad(a0 + da)) * r, 24 + Math.sin(rad(a0 + da)) * r]);
    }
    g.hole(P.poly(pts), P.circ(24, 24, 6.2));
  },
  'flask': (g, P) => {             // a conical laboratory flask, half full, bubbling
    g.hole('M18.5 12H29.5V19.5L42 39C43.5 41.5 42.5 44.5 39.5 44.5H8.5C5.5 44.5 4.5 41.5 6 39L18.5 19.5Z',
      'M21.5 12V20.4L15.6 29.5H32.4L26.5 20.4V12Z');
    g.fill(P.rect(16, 9, 16, 4.4, 1.6));
    g.layer();
    g.fill(P.circ(21, 4.5, 2.4)); g.fill(P.circ(28, 3.5, 1.6));
  },
  'microscope': (g, P) => {        // a microscope from the side: eyepiece, slanted tube, arm, stage, base
    g.fill(P.rect(8, 40.5, 32, 4.5, 2));
    g.fill(P.arc(23, 27, 12, -70, 85, 5));
    g.fill(P.cap(13.5, 5.5, 23, 24, 7.6)).cut('M13.5 12L20 9.2', 1.6);
    g.fill(P.cap(22.5, 23, 24.5, 28.5, 4));
    g.fill(P.rect(13, 31, 22, 4, 1.2));
    g.fill(P.cap(20, 15.5, 27.5, 15, 4.2));
  },
  'lightbulb': (g, P) => {         // a light bulb, filament glowing
    g.fill('M24 3C32 3 38 9 38 17C38 22 35.5 25 33 27.5C31.2 29.4 30.2 31 30 33.5H18C17.8 31 16.8 29.4 15 27.5C12.5 25 10 22 10 17C10 9 16 3 24 3Z')
      .cut('M19.5 33V24.5L22 21L24 25L26 21L28.5 24.5V33', 1.8).cut('M15.5 15.5C16 11.5 18.5 9 22 8.2', 2);
    g.fill(P.rect(17.5, 35, 13, 7.5, 2)).cut('M17 38.7H31', 1.6);
    g.fill(P.rect(21, 42, 6, 3.5, 1.6));
  },
  'puzzle': (g, P) => {            // one jigsaw piece
    g.fill(P.rect(6, 13, 30, 30, 2.4));
    g.fill(P.circ(21, 8.2, 5.6)); g.fill(P.rect(18, 9, 6, 6));
    g.fill(P.circ(40.8, 28, 5.6)); g.fill(P.rect(34, 25, 6, 6));
    g.cutFill(P.circ(9.8, 28, 5)).cutFill(P.rect(4, 25.5, 4, 5));
    g.cutFill(P.circ(21, 39.2, 5)).cutFill(P.rect(18.5, 41, 5, 4));
  },
  'ladder': (g, P) => {            // a tall ladder, standing upright
    g.fill(P.cap(11, 45, 14, 3, 4)); g.fill(P.cap(37, 45, 34, 3, 4));
    for (const y of [9, 17, 25, 33, 41]) g.fill(P.rect(12, y - 1.7, 24, 3.4, 0.8));
  },
  'chain': (g, P) => {             // three links of a chain
    const Q = turned(P, -45, 24, 24, 1.06);
    g.hole(Q.rect(17, 1.5, 14, 19, 7), Q.rect(21, 6, 6, 10, 3))
      .hole(Q.rect(17, 27.5, 14, 19, 7), Q.rect(21, 32, 6, 10, 3))
      .cut(Q.rect(21.5, 13, 5, 22, 2.5), 2.6);
    g.layer();
    g.fill(Q.rect(21.5, 13, 5, 22, 2.5));
  },
  'broken-chain': (g, P) => {      // the chain snapped: its middle link sprung open, the two halves pulled apart
    const U = turned(P, -45, 24, 24, 0.9, -2.4, -2.4), D = turned(P, -45, 24, 24, 0.9, 2.4, 2.4), C = turned(P, -45, 24, 24, 0.9);
    g.hole(U.rect(17, 0, 14, 18, 7), U.rect(21, 4.5, 6, 9, 3)).cut(U.arc(24, 17, 5, 200, 340, 0.1), 2.6);
    g.hole(D.rect(17, 30, 14, 18, 7), D.rect(21, 34.5, 6, 9, 3)).cut(D.arc(24, 31, 5, 20, 160, 0.1), 2.6);
    g.layer();
    g.fill(U.arc(24, 16.5, 4.8, -25, 205, 3.4)); g.fill(D.arc(24, 31.5, 4.8, 155, 385, 3.4));
    for (const [x1, y1, x2, y2] of [[14, 20.5, 8, 18.5], [14, 27.5, 8, 29.5], [34, 20.5, 40, 18.5], [34, 27.5, 40, 29.5]]) g.fill(C.cap(x1, y1, x2, y2, 2.6));
  },
  'rope': (g, P) => {              // a coil of rope, its twisted end hauled up and away, frayed
    const sp = spiral(19, 28, 3, 8, 1.75, rad(330)), e = sp[sp.length - 1];
    const all = resample(sp.concat([[e[0] + 3, e[1] - 5], [34, 12], [39, 7]]), 0.5);
    trail(g, P, all, 6);
    twist(g, all, Math.floor(all.length * 0.45), 9, 3.4, 1.8, 1.4);
    for (const [x, y] of [[43, 6.5], [42, 3], [39, 2.5]]) g.fill(P.cap(39, 7, x, y, 2.2));
  },
  'anchor': (g, P) => {            // a ship's anchor
    g.hole(P.circ(24, 7.5, 4.6), P.circ(24, 7.5, 2));
    g.fill(P.cap(14, 15.5, 34, 15.5, 3.6));
    g.fill(P.rect(21.7, 11, 4.6, 31, 1.5));
    g.fill(P.arc(24, 25, 17, 25, 155, 4.4));
    g.fill(P.poly([[41.5, 26], [44.5, 37], [35.5, 34]])); g.fill(P.poly([[6.5, 26], [3.5, 37], [12.5, 34]]));
  },
  'telescope': (g, P) => {         // a telescope on a tripod, aimed at the sky
    g.fill(P.cap(24, 27, 13, 45, 3.2)); g.fill(P.cap(24, 27, 35, 45, 3.2)); g.fill(P.cap(24, 27, 24, 45, 3));
    g.layer();
    const Q = turned(P, -32, 24, 22);
    g.fill(Q.rect(3, 19.5, 8, 5, 1)); g.fill(Q.rect(10, 18, 13, 8, 1)); g.fill(Q.rect(22, 16.5, 22, 11, 1.5)).cut(Q.d('M40 16V28'), 1.8);
    g.fill(P.rect(21, 23.5, 6, 6, 1.2));
  },
  'binoculars': (g, P) => {        // a pair of binoculars
    g.fill(P.rect(9, 7, 9, 10, 1.6)); g.fill(P.rect(30, 7, 9, 10, 1.6));
    g.fill(P.rect(4, 15, 17, 28, 7)).cutFill(P.circ(12.5, 34.5, 4.6));
    g.fill(P.rect(27, 15, 17, 28, 7)).cutFill(P.circ(35.5, 34.5, 4.6));
    g.fill(P.rect(19, 18, 10, 9, 1.4));
  },
  'camera': (g, P) => {            // a camera with a big round lens
    g.fill(P.poly([[15, 13], [18, 7.5], [29, 7.5], [32, 13]]));
    g.fill(P.rect(4, 12, 40, 30, 4)).cut(P.circ(24, 27, 9.5), 2.2).cutFill(P.rect(36, 16, 4, 3, 0.8));
    g.layer(); g.fill(P.rect(7.5, 9, 6, 4, 1));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
