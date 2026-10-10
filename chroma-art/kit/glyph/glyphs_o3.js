// Option icons, batch o3: paper, books, money and office things.
const { glyph } = require('./glyph');

const rd = (n) => Math.round(n * 100) / 100;
const rad = (a) => a * Math.PI / 180;
// a point transform: rotate deg (clockwise on screen) about (ox, oy), then move by (dx, dy)
const rot = (deg, ox, oy, dx = 0, dy = 0) => {
  const c = Math.cos(rad(deg)), s = Math.sin(rad(deg));
  return (x, y) => [ox + dx + (x - ox) * c - (y - oy) * s, oy + dy + (x - ox) * s + (y - oy) * c];
};
// apply a point transform to a path made only of absolute M, L, C, Q and Z commands
const xf = (d, f) => d.replace(/(-?\d*\.?\d+)[ ,]+(-?\d*\.?\d+)/g, (m, x, y) => f(+x, +y).map(rd).join(' '));
// a rounded rectangle drawn with Q corners, so that it can be turned with xf
const rr = (x, y, w, h, q) => `M${x + q} ${y}L${x + w - q} ${y}Q${x + w} ${y} ${x + w} ${y + q}L${x + w} ${y + h - q}Q${x + w} ${y + h} ${x + w - q} ${y + h}L${x + q} ${y + h}Q${x} ${y + h} ${x} ${y + h - q}L${x} ${y + q}Q${x} ${y} ${x + q} ${y}Z`;
const HEART = 'M24 42C10 32 4 25 4 17C4 10 9 6 15 6C19 6 22 8 24 11C26 8 29 6 33 6C39 6 44 10 44 17C44 25 38 32 24 42Z';
// the heart scaled about (24, 24) by s and moved by (dx, dy)
const heart = (s, dx = 0, dy = 0) => xf(HEART, (x, y) => [24 + (x - 24) * s + dx, 24 + (y - 24) * s + dy]);

const G = {
  'rulebook': (g, P) => {          // the rule books: two thick volumes lying one on the other
    g.fill('M7 28L44 28L44 44L7 44Q4 44 4 41L4 31Q4 28 7 28Z').cut('M10.5 28L10.5 44', 2).cut('M29 32.5L44 32.5M29 36L44 36M29 39.5L44 39.5', 1.4);
    const f = rot(-7, 24, 20, 0, -2);
    g.fill(xf('M6 11L41 11Q44 11 44 14L44 23Q44 26 41 26L6 26Z', f)).cut(xf('M40.5 11L40.5 26', f), 2).cut(xf('M6 15.5L20 15.5M6 19L20 19M6 22.5L20 22.5', f), 1.4);
  },
  'price-tag': (g, P) => {         // a price tag on its string, point up-left
    const f = rot(-45, 24, 26, -1.5, -2.5);
    g.fill(xf('M24 5L35 15.5Q36 16.5 36 18L36 41Q36 44 33 44L15 44Q12 44 12 41L12 18Q12 16.5 13 15.5Z', f))
      .cutFill(P.circ(...f(24, 15.5), 3)).cut(xf('M17 30L31 30', f), 2).cut(xf('M17 36L27 36', f), 2);
    g.layer();
    const h = f(24, 15.5);
    g.fill(P.arc(h[0] - 3.2, h[1] - 3.2, 4.6, 45, 270, 2.8));
  },
  'letter': (g, P) => {            // a sealed envelope
    g.hole(P.rect(3.5, 10, 41, 29, 3), P.rect(8, 14.5, 32, 20, 1));
    g.fill(P.cap(7, 13.5, 24, 27.5, 4)); g.fill(P.cap(41, 13.5, 24, 27.5, 4));
  },
  'piggy-bank': (g, P) => {        // a piggy bank, side view, coin slot on its back
    g.fill('M7 27C7 18 15 12.5 24 12.5C30 12.5 34.5 14.5 37.5 18L40.5 21H43C44.5 21 45 22 45 23.5V30C45 31.5 44.5 32.5 43 32.5H39.5C38 35 36 37 34 38V44H28V40H19V44H13V37.5C9 35 7 31 7 27Z')
      .cut('M18 17.5H27', 2.4).cutFill(P.circ(35, 23, 1.8));
    g.fill(P.poly([[29, 14], [33.5, 7], [37, 17]]));
    g.fill(P.arc(6.5, 22.5, 2.4, 30, 330, 2.8));
  },
  'map': (g, P) => {               // a folded map, a route to a cross
    g.fill(P.poly([[3, 10], [17, 5], [31, 10], [45, 5], [45, 38], [31, 43], [17, 38], [3, 43]]))
      .cut('M17 5V38', 2).cut('M31 10V43', 2)
      .cut('M8 36C12 30 14 27 20 28C26 29 25 21 30 19', 2).cut('M34.5 13.5L40 19M40 13.5L34.5 19', 2.2);
  },
  'pen': (g, P) => {               // a pen signing a sheet
    g.fill('M6 6Q6 4 8 4H26L35 13V42Q35 44 33 44H8Q6 44 6 42Z').cut('M26 4V13H35', 1.8).cut('M11 12H21M11 18H28M11 24H22', 2)
      .cut('M43.5 10L27 34.5L24 41.5L30.5 37L46.5 13', 6);
    g.layer();
    g.fill('M41.5 8.5L45 11L30 33.5L26.5 31Z'); g.fill('M26 32L29.5 34.5L25 39Z');
    g.fill(P.cap(10, 38, 14, 34, 2.8)); g.fill(P.cap(14, 34, 17, 38, 2.8)); g.fill(P.cap(17, 38, 22, 35, 2.8));
  },
  'calculator': (g, P) => {        // a pocket calculator: a window, blank keys
    g.fill(P.rect(9, 3, 30, 42, 4)).cutFill(P.rect(13.5, 7.5, 21, 9, 1.5));
    for (const y of [21, 27.5, 34]) for (const x of [13.5, 21.5, 29.5]) g.cutFill(P.rect(x, y, 5, 4.2, 1));
    g.cutFill(P.rect(13.5, 39.5, 13, 2.6, 1)).cutFill(P.rect(29.5, 39.5, 5, 2.6, 1));
  },
  'laptop': (g, P) => {            // an open laptop, front view
    g.hole(P.rect(8, 7, 32, 24, 2.5), P.rect(11.5, 10.5, 25, 17, 1));
    g.fill('M3 34H45V36.5C45 38.5 43.5 40 41.5 40H6.5C4.5 40 3 38.5 3 36.5Z').cutFill(P.rect(19, 33, 10, 3, 1));
  },
  'chart': (g, P) => {             // a bar chart with a rising arrow
    g.fill(P.cap(4.5, 43.5, 43.5, 43.5, 3));
    g.fill(P.rect(6, 33, 7, 9, 1)); g.fill(P.rect(16, 28, 7, 14, 1)); g.fill(P.rect(26, 23, 7, 19, 1)); g.fill(P.rect(36, 17, 7, 25, 1));
    g.fill(P.cap(5, 25, 15, 16, 3.2)); g.fill(P.cap(15, 16, 22, 21, 3.2)); g.fill(P.cap(22, 21, 35, 8.5, 3.2));
    g.fill(P.poly([[30, 5], [42, 3], [40, 15]]));
  },
  'credit-card': (g, P) => {       // a bank card: stripe and chip
    const f = rot(-14, 24, 24);
    g.fill(xf(rr(6, 12, 36, 24, 3.5), f)).cut(xf('M4 19L44 19', f), 4).cutFill(xf(rr(10.5, 24.5, 8, 6, 1.5), f)).cut(xf('M23 30.5L37 30.5', f), 2);
  },
  'diploma': (g, P) => {           // a rolled certificate, tied with a ribbon rosette
    const f = rot(-35, 24, 22);
    g.fill(xf(rr(4, 15.5, 40, 13, 4.5), f)).cut(xf('M9.5 16.5L9.5 27.5M38.5 16.5L38.5 27.5', f), 1.8)
      .cut(P.circ(24, 25, 5.6), 2.4).cut('M22.5 28L21 41M25.5 28L28 41', 6.4);
    g.layer();
    g.fill(P.circ(24, 25, 4.6)).cutFill(P.circ(24, 25, 1.6));
    g.fill(P.poly([[21.5, 28], [25, 28], [23.5, 42], [21.5, 39.5], [19, 41.5]]));
    g.fill(P.poly([[23, 28], [26.5, 28], [30, 41], [27.5, 39.5], [26, 42]]));
  },
  'mortarboard': (g, P) => {       // a graduation cap with its tassel
    g.fill('M12 23V33Q24 39 36 33V23Z').cut('M10 23.5L24 29.5L38 23.5', 3);
    g.layer();
    g.fill(P.poly([[3, 18], [24, 9], [45, 18], [24, 27]])).cutFill(P.circ(24, 18, 1.8)).cut('M24 18L39 20.5', 1.4);
    g.fill(P.cap(40.5, 20.5, 40.5, 32, 2.8)); g.fill(P.poly([[38, 31], [43, 31], [44.5, 40], [36.5, 40]]));
  },
  'bookshelf': (g, P) => {         // a shelf of books, the last one leaning on its neighbour
    const f = rot(-20, 44, 39), lean = xf(rr(37.5, 12, 6.5, 27, 1), f);
    g.fill(P.rect(3, 40, 42, 5, 1.2));
    g.fill(P.rect(5, 13, 6.5, 26, 1)).cut('M5 17.5H11.5M5 34H11.5', 1.6);
    g.fill(P.rect(13.5, 8, 6, 31, 1)).cut('M13.5 12.5H19.5M13.5 34H19.5', 1.6);
    g.fill(P.rect(21.5, 15, 7.5, 24, 1)).cut('M21.5 19.5H29M21.5 34H29', 1.6).cut(lean, 3);
    g.layer();
    g.fill(lean).cut(xf('M37.5 16.5L44 16.5M37.5 34L44 34', f), 1.6);
  },
  'picture-frame': (g, P) => {     // a framed picture hung on a nail
    g.fill(P.cap(13, 14, 24, 6, 2.8)); g.fill(P.cap(35, 14, 24, 6, 2.8)); g.fill(P.circ(24, 5.6, 2.6));
    g.hole(P.rect(5, 13, 38, 31, 2), P.rect(10, 18, 28, 21, 0.5));
    g.fill('M10 39L18.5 28L24 34L28.5 29.5L38 39Z'); g.fill(P.circ(31.5, 23.5, 2.8));
  },
  'playing-cards': (g, P) => {     // a fan of three cards
    const card = (deg) => xf(rr(15.5, 10.5, 17, 26, 2.5), rot(deg, 24, 43.5));
    const f1 = rot(-22, 24, 43.5), f2 = rot(0, 24, 43.5), f3 = rot(22, 24, 43.5);
    g.fill(card(-22)).cut(card(0), 3).cutFill(P.star(...f1(20, 16), 3.4, 2, 4, -90 - 22));
    g.layer();
    g.fill(card(0)).cut(card(22), 3).cutFill(P.circ(...f2(20, 15.5), 2.2));
    g.layer();
    g.fill(card(22)).cutFill(xf(heart(0.27, 0, 0), (x, y) => f3(x, y - 0.5)));
  },
  'collection-tin': (g, P) => {    // a coin dropping into a charity jar with a slotted lid
    g.fill(P.circ(24, 7.6, 4.6)).cut(P.circ(24, 7.6, 2.2), 1.4);
    g.fill(P.rect(13, 14.4, 22, 4.4, 1.6)).cut('M18 14.4H30', 2);
    g.fill('M16 21H32V23Q39 25.5 39 32.5V40Q39 45 34 45H14Q9 45 9 40V32.5Q9 25.5 16 23Z').cutFill(heart(0.34, 0, 10));
  },
  'gavel': (g, P) => {             // a judge's gavel over its block
    g.fill(P.rect(7, 39, 24, 6, 2)); g.fill(P.rect(10, 35.5, 18, 3, 1));
    const f = rot(45, 17, 22, 3, 0);
    g.fill(xf(rr(9, 15, 16, 14, 2), f)).fill(xf(rr(6.5, 13, 4.5, 18, 1.5), f)).fill(xf(rr(23, 13, 4.5, 18, 1.5), f));
    g.fill(P.cap(...f(17, 14), ...f(17, -1.5), 3.8));
  },
  'placard': (g, P) => {           // a protest placard held up on a stick
    g.fill(P.cap(24, 30, 24, 42.9, 4.2));
    g.layer();
    const f = rot(-8, 24, 18, 0, 1.5);
    g.fill(xf(rr(6, 4, 36, 25, 2), f)).cut(xf('M24 9L24 18', f), 3.2).cutFill(P.circ(...f(24, 23.5), 2));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
