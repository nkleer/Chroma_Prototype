// Option icons, batch A: "a narrow escape" and "falling in love".
const { glyph } = require('./glyph');

const rad = (a) => a * Math.PI / 180;

const G = {
  'candle': (g, P) => {            // a lit candle in a dish
    g.fill('M24 2.5C29 8.5 31.5 12 31.5 15.5C31.5 19.3 28.3 21.5 24 21.5C19.7 21.5 16.5 19.3 16.5 15.5C16.5 12 19 8.5 24 2.5Z')
      .cutFill('M24 11.5C25.9 14 26.8 15.6 26.8 17C26.8 18.5 25.6 19.4 24 19.4C22.4 19.4 21.2 18.5 21.2 17C21.2 15.6 22.1 14 24 11.5Z');
    g.layer();
    g.fill(P.rect(16, 24, 16, 17, 1.6)).cut('M20.5 24V31.5', 2);
    g.fill(P.rect(7, 40, 34, 5, 2.5));
  },
  'magnifier': (g, P) => {         // a magnifying glass
    g.hole(P.circ(20, 20, 14.5), P.circ(20, 20, 9.8));
    g.fill(P.cap(30, 30, 33, 33, 4.4));
    g.fill(P.cap(33.5, 33.5, 42, 42, 7));
    g.fill(P.arc(20, 20, 6.2, 195, 255, 2.4));
  },
  'sweets': (g, P) => {            // a wrapped sweet, twisted at both ends
    g.fill('M12.5 24C12.5 17 17.5 12.5 24 12.5C30.5 12.5 35.5 17 35.5 24C35.5 31 30.5 35.5 24 35.5C17.5 35.5 12.5 31 12.5 24Z')
      .cut('M17.5 15.5L27.5 34', 2.1).cut('M24.5 13.5L33 29.5', 2.1);
    g.fill(P.poly([[14, 24], [3.5, 12], [6.5, 18], [3, 24], [6.5, 30], [3.5, 36]]));
    g.fill(P.poly([[34, 24], [44.5, 12], [41.5, 18], [45, 24], [41.5, 30], [44.5, 36]]));
  },
  'summit': (g, P) => {            // one peak with a flag planted on top
    g.fill(P.poly([[3, 45], [22, 17], [45, 45]])).cut('M14.5 29.5L18 33L21.5 29L25 33L29 29.5', 1.8);
    g.fill(P.cap(22, 18, 22, 4, 2.8));
    g.fill(P.poly([[23, 3.5], [35, 3.5], [31, 8], [35, 12.5], [23, 12.5]]));
  },
  'sun': (g, P) => {               // a full sun with rays all round
    g.fill(P.circ(24, 24, 10));
    for (let i = 0; i < 8; i++) {
      const a = rad(i * 45), c = Math.cos(a), s = Math.sin(a);
      g.fill(P.cap(24 + c * 14.5, 24 + s * 14.5, 24 + c * 20.5, 24 + s * 20.5, 3.6));
    }
  },
  'badge': (g, P) => {             // a lawman's star badge, ball-tipped
    g.fill(P.star(24, 25.5, 19, 10.5, 5));
    for (let i = 0; i < 5; i++) { const a = rad(-90 + i * 72); g.fill(P.circ(24 + Math.cos(a) * 19, 25.5 + Math.sin(a) * 19, 3.1)); }
    g.cut(P.circ(24, 25.5, 5.4), 1.8);
  },
  'first-aid': (g, P) => {         // a first-aid case with a plus
    g.hole(P.rect(17, 7, 14, 9, 3), P.rect(20.5, 10.5, 7, 6, 1.2));
    g.fill(P.rect(4, 14, 40, 30, 4))
      .cutFill('M21 19H27V26H34V32H27V39H21V32H14V26H21Z');
  },
  'scales': (g, P) => {            // balance scales
    g.fill(P.circ(24, 7, 3));
    g.fill(P.cap(24, 8, 24, 41, 3.4));
    g.fill(P.rect(13, 41, 22, 4, 1.6));
    g.fill(P.cap(9.5, 12.5, 38.5, 12.5, 3.2));
    for (const x of [9.5, 38.5]) {
      g.fill(P.cap(x, 13, x - 5.5, 28, 2.4)); g.fill(P.cap(x, 13, x + 5.5, 28, 2.4));
      g.fill(`M${x - 7} 28H${x + 7}A7 7 0 0 1 ${x - 7} 28Z`);
    }
  },
  'megaphone': (g, P) => {         // a megaphone, sound going out
    g.fill(P.rect(4, 19, 5, 10, 1.4));
    g.fill(P.poly([[8, 19], [28, 9.5], [28, 38.5], [8, 29]]));
    g.fill(P.rect(26.5, 8, 4.5, 32, 1.6));
    g.fill(P.cap(15, 30, 13.5, 38, 4));
    g.fill(P.arc(30, 24, 9.5, -35, 35, 2.8)); g.fill(P.arc(30, 24, 14.5, -38, 38, 2.8));
  },
  'meditate': (g, P) => {          // someone sitting cross-legged, hands resting on the knees
    g.fill(P.circ(24, 8, 5.4));
    g.fill('M19.5 15.5H28.5Q31.2 15.5 31 18.2L29.5 33H18.5L17 18.2Q16.8 15.5 19.5 15.5Z');
    g.fill(P.cap(17.8, 18, 11, 29, 3.8)); g.fill(P.circ(10.5, 31.5, 2.6));
    g.fill(P.cap(30.2, 18, 37, 29, 3.8)); g.fill(P.circ(37.5, 31.5, 2.6));
    g.fill('M5 40C5 35.5 13 34.5 24 35.5C35 34.5 43 35.5 43 40C43 44 36 45.5 24 43.5C12 45.5 5 44 5 40Z');
  },
  'daisy': (g, P) => {             // an open flower on its stem
    for (let i = 0; i < 8; i++) {
      const a = rad(i * 45 + 22.5), c = Math.cos(a), s = Math.sin(a);
      g.fill(P.cap(24 + c * 5, 15.5 + s * 5, 24 + c * 10.5, 15.5 + s * 10.5, 6.4));
    }
    g.cutFill(P.circ(24, 15.5, 6.6));
    g.layer();
    g.fill(P.circ(24, 15.5, 4.4));
    g.fill(P.cap(24, 28, 24, 45, 3));
    g.fill(P.lens(25, 40, 36, 32, 3.6)).cut('M27 38.5L33.5 33.5', 1.3);
  },
  'trail': (g, P) => {             // a hot-air balloon: an adventure for two
    g.fill('M24 3C33.5 3 40 9.5 40 18C40 25 34 29.5 29.5 34.5H18.5C14 29.5 8 25 8 18C8 9.5 14.5 3 24 3Z')
      .cut('M19.5 4.5C15.5 10 15.5 26 20.5 34', 1.8).cut('M28.5 4.5C32.5 10 32.5 26 27.5 34', 1.8);
    g.fill(P.cap(20, 34, 20.5, 39, 2.4)); g.fill(P.cap(28, 34, 27.5, 39, 2.4));
    g.fill(P.rect(18, 38.5, 12, 7, 1.6));
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, fn]) => glyph(n, fn)) };
