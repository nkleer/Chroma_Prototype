// Option icons, batch p1: papers, politics, hands and a few things.
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;
const f2 = (n) => Math.round(n * 100) / 100;
// a point transform: rotate deg (clockwise on screen) about (ox, oy), then move by (dx, dy)
const rot = (deg, ox, oy, dx = 0, dy = 0) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg));
  return (x, y) => [ox + dx + (x - ox) * c - (y - oy) * s, oy + dy + (x - ox) * s + (y - oy) * c];
};
// apply a point transform to a path made only of absolute M, L, C, Q and Z commands
const xf = (d, f) => d.replace(/(-?\d*\.?\d+)[ ,]+(-?\d*\.?\d+)/g, (m, x, y) => f(+x, +y).map(f2).join(' '));
// a rounded rectangle drawn with Q corners, so that it can be turned with xf
const rr = (x, y, w, h, q) => `M${x + q} ${y}L${x + w - q} ${y}Q${x + w} ${y} ${x + w} ${y + q}L${x + w} ${y + h - q}Q${x + w} ${y + h} ${x + w - q} ${y + h}L${x + q} ${y + h}Q${x} ${y + h} ${x} ${y + h - q}L${x} ${y + q}Q${x} ${y} ${x + q} ${y}Z`;

const G = {
  'manuscript': (g, P) => {        // a stack of typed pages, a paper clip on the top sheet
    const front = [5, 11, 27, 34], mid = [10.5, 7, 27, 35], clip = [8, 4.5, 7, 15.5];
    const grow = ([x, y, w, h], k, q) => P.rect(x - k, y - k, w + 2 * k, h + 2 * k, q);
    g.fill(P.rect(16, 3, 27, 34, 1.5)).cutFill(grow(mid, 1.6, 3));
    g.layer();
    g.fill(grow(mid, 0, 1.5)).cutFill(grow(front, 1.8, 3)).cutFill(grow(clip, 1.6, 5));
    g.layer();
    g.fill(grow(front, 0, 1.5)).cut('M10 23H27M10 29H27M10 35H27M10 41H20', 2).cutFill(grow(clip, 1.6, 5));
    g.layer();
    g.hole(grow(clip, 0, 3.5), P.rect(10.6, 7.1, 1.8, 10.3, 0.9));
  },
  'script': (g, P) => {            // a play script held by two brass pins, its corner folded over, lines of dialogue
    g.fill('M6 4H42V32L31 44H6Z')
      .cutFill(P.circ(11.5, 10.5, 2.3)).cutFill(P.circ(11.5, 37.5, 2.3))
      .cut('M21 10.5H29M16.5 16H37M21 22.5H29M16.5 28H33', 2)
      .cutFill('M42 32L31 32L31 44Z');
    g.fill('M40 34.2L33.2 34.2L33.2 41.5Z');
  },
  'folder': (g, P) => {            // a case folder: tab, a paper standing out of it
    g.fill('M3 11Q3 8 6 8H15.5Q17.5 8 18.5 9.5L20.5 13H42Q45 13 45 16V40Q45 43 42 43H6Q3 43 3 40Z')
      .cutFill(P.rect(17.5, 2.5, 25, 22));
    g.layer();
    g.fill(P.rect(19.5, 4.5, 21, 20, 0.8)).cut('M24 10H36', 1.8);
    g.cut('M2 22.7H46', 3.4);
    g.layer();
    g.fill('M3 22.5H45V40Q45 43 42 43H6Q3 43 3 40Z');
  },
  'rubber-stamp': (g, P) => {      // a rubber stamp: ball handle, neck, block, a stamped line beneath
    g.fill(P.circ(24, 9, 6.5));
    g.fill('M20.5 14H27.5L29 23H19Z');
    g.fill(P.rect(9, 22.5, 30, 10, 2));
    g.fill(P.rect(11, 34.5, 26, 4, 1));
    g.fill(P.cap(8, 44, 40, 44, 2.8));
  },
  'eraser': (g, P) => {            // an eraser rubbing out the end of a pencil line, crumbs flying
    const f = rot(-30, 28, 19, -1.8, 8.4);
    g.fill(xf(rr(12, 10, 32, 16.5, 4), f)).cut(xf('M25.5 9L25.5 28', f), 2.2);
    g.fill(P.cap(4, 42.5, 16, 42.5, 3.2));
    g.fill(P.circ(25, 43, 2)).fill(P.circ(30.5, 44.5, 1.9)).fill(P.circ(35.5, 42, 1.9));
  },
  'leaflet': (g, P) => {           // a leaflet folded in half and partly opened: the candidate on its front
    const top = rot(-7, 24, 25), bot = rot(9, 24, 25);
    g.fill(xf(rr(9, 3, 30, 22, 1), top)).cutFill(P.circ(...top(24, 10.5), 3.6)).cutFill(xf('M17 22C17 17 20 14.5 24 14.5C28 14.5 31 17 31 22Z', top));
    g.fill(xf('M9 26L39 26L39 42Q39 43 38 43L10 43Q9 43 9 42Z', bot)).cut(xf('M14 31.5L34 31.5M14 37L29 37', bot), 2);
  },
  'ticket': (g, P) => {            // a ticket: bitten corners, a row of perforations, the far end torn off
    const f = rot(-18, 24, 24);
    let torn = ''; for (let i = 0; i < 5; i++) torn += `L${i % 2 ? 41 : 44.5} ${f2(11 + (i + 1) * 26 / 5)}`;
    g.fill(xf(`M3 11L41 11${torn}L3 37Z`, f))
      .cutFill(P.circ(...f(3, 11), 4.6)).cutFill(P.circ(...f(3, 37), 4.6))
      .cut(xf('M14.5 16.5L14.5 17.5M14.5 23.5L14.5 24.5M14.5 30.5L14.5 31.5', f), 2.4);
  },
  'rosette': (g, P) => {           // a party rosette: a pleated ring, a button, two ribbon tails
    g.fill(P.poly([[17, 26], [24, 30], [16, 46], [13, 41], [9, 43]])).fill(P.poly([[31, 26], [24, 30], [32, 46], [35, 41], [39, 43]]));
    g.cutFill(P.circ(24, 19, 17.5));
    g.layer();
    g.fill(P.star(24, 19, 16, 13, 18, -90)).cut(P.circ(24, 19, 10), 1.8);
    g.fill(P.circ(24, 19, 6.4));
  },
  'chain-of-office': (g, P) => {   // a mayor's chain: square links round the neck, a medallion hanging at the front
    const N = 10;
    for (let i = 0; i <= N; i++) {
      const a = -6 + i * (192 / N), x = 24 + Math.cos(rad(a)) * 18.5, y = 2 + Math.sin(rad(a)) * 21;
      if (y > 17 && Math.abs(x - 24) < 8) continue;
      g.fill(xf(rr(x - 3, y - 2.6, 6, 5.2, 1.2), rot(a + 90, x, y)));
    }
    g.fill(P.cap(24, 21, 24, 26, 3));
    g.fill(P.circ(24, 34.5, 10.5)).cut(P.circ(24, 34.5, 7), 1.6);
  },
  'town-hall': (g, P) => {         // a civic hall: a small dome, a pediment, columns, steps
    g.fill(P.cap(24, 2.5, 24, 6, 2.4));
    g.fill('M17 15A7 7 0 0 1 31 15Z');
    g.fill(P.poly([[5, 23], [24, 14.5], [43, 23]]));
    g.fill(P.rect(6, 24.5, 36, 3.5, 0.6));
    for (const x of [8, 16, 26, 34]) g.fill(P.rect(x, 29.5, 6, 10.5));
    g.fill(P.rect(5, 41.5, 38, 3.5, 0.6));
  },
  'knock': (g, P) => {             // a fist knocking on a door
    g.fill(P.rect(30, 3, 15, 42, 1)).cut(P.rect(34, 8, 7, 12, 0.6), 1.6).cut(P.rect(34, 26, 7, 14, 0.6), 1.6);
    g.cut(P.rect(5, 15, 27, 18, 4), 4);
    g.layer();
    g.fill(P.rect(9, 15, 13, 19, 4));
    for (const y of [18, 23, 28, 32.5]) g.fill(P.cap(15, y, 26, y, 4.6));
    g.cut('M17 20.5H27M17 25.5H27M17 30.3H27', 1.4);
    g.fill(P.cap(12, 31, 5, 44.5, 7));
    g.layer();
    g.fill(P.cap(10, 19, 22, 22, 4.4));
    g.fill(P.cap(19, 9, 17, 5, 2.8)).fill(P.cap(25, 9.5, 26, 5, 2.8)).fill(P.cap(13.5, 11, 10, 8, 2.8));
  },
  'applause': (g, P) => {          // two hands clapping, motion marks above
    const hand = (f, m) => {         // an open hand, fingers up, thumb out to the left (m = -1 mirrors it)
      const X = (x) => 24 + m * (x - 24), pts = (a) => a.map(([x, y]) => f(X(x), y)).flat();
      return [P.cap(...pts([[18.6, 24], [18.6, 12]]), 4.2), P.cap(...pts([[22.8, 24], [22.8, 9]]), 4.4), P.cap(...pts([[27, 24], [27, 10]]), 4.4),
        P.cap(...pts([[30.8, 25], [30.8, 14]]), 4), xf(rr(16.5, 19, 16.5, 16, 5), (x, y) => f(X(x), y)),
        P.cap(...pts([[18, 31], [12.5, 23.5]]), 4.8), xf(rr(18.5, 32, 11, 12, 2), (x, y) => f(X(x), y))];
    };
    const B = hand(rot(24, 24, 40, -7, 0), -1), F = hand(rot(-16, 24, 40, 5.5, 1), 1);
    B.forEach((d) => g.fill(d)); F.forEach((d) => g.cut(d, 3));
    g.layer();
    F.forEach((d) => g.fill(d));
    g.fill(P.cap(10, 7.5, 7, 3.5, 2.6)).fill(P.cap(39.5, 9, 43, 5, 2.6)).fill(P.cap(39, 16, 44, 15, 2.6));
  },
  'laughing-face': (g, P) => {     // a round face laughing: eyes squeezed shut, mouth wide open
    g.fill(P.circ(24, 24, 20))
      .cut('M12 19Q15.5 14 19 19', 2.4).cut('M29 19Q32.5 14 36 19', 2.4)
      .cutFill('M12 26H36C36 34 30.5 38.5 24 38.5C17.5 38.5 12 34 12 26Z');
    g.fill('M17.5 34Q24 29.5 30.5 34Q27.5 37 24 37Q20.5 37 17.5 34Z');
  },
  'crossed-fingers': (g, P) => {   // a raised hand, the middle finger crossed over the index
    const MID = P.cap(27.5, 27, 18, 8.5, 5.2), THUMB = P.cap(12.5, 36, 23, 30, 5);
    g.fill(P.rect(13, 24, 21, 17, 5)); g.fill(P.rect(16.5, 38, 14, 7, 2));
    g.fill(P.cap(30, 28, 30.5, 22, 5)); g.fill(P.cap(34.5, 30, 35, 25, 4.6));
    g.fill(P.cap(19.5, 27, 28.5, 6, 5.2));
    g.cut(MID, 2.6).cut(THUMB, 2.6);
    g.layer();
    g.fill(MID); g.fill(THUMB);
  },
  'target': (g, P) => {            // a bullseye with an arrow in its centre
    g.hole(P.circ(21, 27, 18), P.circ(21, 27, 14.5));
    g.hole(P.circ(21, 27, 11.5), P.circ(21, 27, 8));
    g.fill(P.circ(21, 27, 5));
    g.cut('M21 27L41 7', 5.6);
    g.layer();
    g.fill(P.cap(21, 27, 40, 8, 2.8));
    g.fill(P.poly([[37, 7], [38.5, 3], [44, 4], [41, 7]])).fill(P.poly([[41, 11], [45, 9.5], [44, 4], [41, 7]]));
  },
  'ring-box': (g, P) => {          // an open ring box, one ring standing in its cushion, the stone above the lid
    const GEM = P.poly([[17.5, 8.5], [20.5, 4.5], [27.5, 4.5], [30.5, 8.5], [24, 14.5]]);
    g.fill('M8 28V18Q8 13 13 13H35Q40 13 40 18V28Z').cutFill(P.circ(24, 24, 10.6)).cutFill(P.rect(15, 2, 18, 12.5)).cut(GEM, 2.8);
    g.layer();
    g.hole(P.circ(24, 24, 8.4), P.circ(24, 24, 5.2)).fill(GEM).cutFill(P.rect(3, 28.5, 42, 20));
    g.layer();
    g.fill(P.rect(6, 30.5, 36, 14.5, 3)).cut('M6 36H42', 1.8);
  },
  'chef-hat': (g, P) => {          // a tall pleated chef's hat
    g.fill(P.circ(14.5, 16, 8)).fill(P.circ(24, 11.5, 9.5)).fill(P.circ(33.5, 16, 8));
    g.fill(P.rect(12, 16, 24, 21)).cut('M18 24V36M24 22V36M30 24V36', 1.8);
    g.fill(P.rect(11, 38.5, 26, 6.5, 1.2));
  },
  'plane': (g, P) => {             // an airliner in flight, side view, climbing
    const f = rot(-14, 24, 24);
    g.fill(xf('M6 21Q6 19 9 19L38 19Q44 19.5 45 24Q44 28.5 38 29L10 29Q6 28 5 25Z', f)).cut(xf('M16 22.6L36 22.6', f), 1.6);
    g.fill(xf('M5 25L3 12L8 12L14 21Z', f));
    g.cut(xf('M22 25L30 25L19 39L14 39Z', f), 2.4);
    g.layer();
    g.fill(xf('M22 25L30 25L19 39L14 39Z', f));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, fn]) => glyph(n, fn)) };
