// Resources, needs, goals, roles, world settings and two acts.
const { glyph } = require('./glyph');

const G = {
  'clock': (g, P) => {             // a pocket watch: bow, crown, face and two hands
    g.fill(P.arc(24, 7, 4.4, 180, 360, 3));
    g.fill(P.rect(20.5, 6.5, 7, 5, 1.2));
    g.hole(P.circ(24, 27.5, 17.5), P.circ(24, 27.5, 13));
    g.fill(P.cap(24, 27.5, 24, 17.5, 3.4)); g.fill(P.cap(24, 27.5, 31.5, 31.5, 3.4)); g.fill(P.circ(24, 27.5, 3.2));
  },
  'handshake': (g, P) => {         // two hands clasped: sleeves slanting down to the corners, an arched clasp with knuckles, a thumb on top
    g.fill('M1.5 33L8.5 20.5L15.5 25L8.5 37.5Z'); g.fill('M46.5 33L39.5 20.5L32.5 25L39.5 37.5Z');
    g.fill('M11 24C13.5 18.5 18.5 15.5 24 15.5C29.5 15.5 34.5 18.5 37 24L34 32.5C30.5 36 27.5 37.5 24 37.5C20.5 37.5 17.5 36 14 32.5Z')
      .cut('M19.5 25.5V34.5', 1.8).cut('M24 25.5V36', 1.8).cut('M28.5 25.5V34.5', 1.8);
    g.layer(); g.fill(P.cap(31, 20.5, 19, 13.5, 5.2));
  },
  'bird': (g, P) => {              // a dove in flight, wing raised
    g.fill(P.circ(11, 26, 4.6));
    g.fill(P.poly([[7, 24], [2.5, 26.5], [7.5, 28.5]]));
    g.fill('M8 27C12 35 24 39 34 35L44 40.5L41.5 33.5L45 29L35 30.5C29 29 21 24.5 14 22.5Z');
    g.fill('M16 26C16 16 24 8 40 5C37 10.5 35.5 16 31.5 21C28 26 21.5 28.5 16 26Z').cut('M21.5 23.5C24.5 18 29 13.5 35 10', 1.6);
  },
  'shield': (g, P) => {            // a heater shield with a carved chevron
    g.fill('M7 7H41V22C41 33 33.5 40.5 24 45C14.5 40.5 7 33 7 22Z').cut('M13 21L24 30L35 21', 2.2);
  },
  'campfire': (g, P) => {          // a low three-tongued fire on crossed logs
    g.fill('M24 33.5C16 33.5 12 29 12.5 23.5C13 19 16 17 16.5 12C19.5 14 20.5 17 20.5 20C22 16 23.5 12 23 6C29.5 10 31.5 15.5 30.5 20C32.5 18 33 15 32.5 12.5C36 16.5 37 21 36 25C35 30 31 33.5 24 33.5Z');
    g.fill(P.cap(7, 44, 41, 36, 5)); g.layer(); g.fill(P.cap(41, 44, 7, 36, 5));
  },
  'compass': (g, P) => {           // a compass rose in a ring
    g.hole(P.circ(24, 24, 15.5), P.circ(24, 24, 12.5));
    g.fill(P.star(24, 24, 21, 4.4, 4, -90)); g.fill(P.star(24, 24, 11, 3, 4, -45));
  },
  'anvil': (g, P) => {             // a hammer raised over an anvil
    g.fill('M4 22C9 22 12 24 14 25V21H42V28H35C32 28 31 30 31 32V36H37V43H13V36H19V32C19 30 18 28.5 15 28.5C10 28.5 6 26 4 22Z');
    const [x1, y1, cx, cy] = [10, 16.5, 31, 10], d = Math.hypot(cx - x1, cy - y1), ux = (cx - x1) / d, uy = (cy - y1) / d, nx = -uy, ny = ux;
    g.fill(P.cap(x1, y1, cx, cy, 3.4));
    g.fill(P.poly([[1, 1], [-1, 1], [-1, -1], [1, -1]].map(([a, b]) => [cx + ux * 3.4 * a + nx * 6.5 * b, cy + uy * 3.4 * a + ny * 6.5 * b])));
  },
  'lantern': (g, P) => {           // a lit lantern: ring, roof, window with flame, base
    g.fill(P.arc(24, 7.5, 4.4, 180, 360, 2.8));
    g.fill(P.poly([[17, 9], [31, 9], [37, 15], [11, 15]]));
    g.hole(P.rect(12.5, 16.5, 23, 22, 1.5), P.rect(16, 20, 16, 15, 1));
    g.fill('M24 21.5C26.5 25 28 27.5 28 30C28 32.5 26.5 34 24 34C21.5 34 20 32.5 20 30C20 27.5 21.5 25 24 21.5Z');
    g.fill(P.rect(10.5, 40, 27, 5, 1.6));
  },
  'dream': (g, P) => {             // a thought cloud with trailing bubbles, holding a star
    g.fill('M14 30C9 30 6.5 26.5 7.5 22.5C8.5 19 12 17.5 15 18.5C15.5 12.5 20.5 8.5 26.5 9C31 9.5 34 12 35 15.5C39.5 15.5 43 18.5 43 23C43 27 40 30 36 30Z')
      .cutFill(P.star(25.5, 20.5, 6.5, 2.8));
    g.fill(P.circ(13, 36, 3.4)); g.fill(P.circ(7.5, 42.5, 2.4));
  },
  'checklist': (g, P) => {         // a clipboard with ticked lines
    g.fill(P.rect(9, 8, 30, 37, 3))
      .cut('M14 18.5L16.5 21L20 16.5', 2).cut('M24 19H34', 2)
      .cut('M14 28.5L16.5 31L20 26.5', 2).cut('M24 29H34', 2)
      .cut('M14 38H20', 2).cut('M24 38H34', 2)
      .cutFill(P.rect(15.5, 5, 17, 8.5, 2));
    g.layer(); g.fill(P.rect(17.5, 4, 13, 7, 2));
  },
  'rival': (g, P) => {             // two narrowed eyes under angry brows
    g.fill(P.cap(5.5, 10.5, 20.5, 18.5, 5)); g.fill(P.cap(42.5, 10.5, 27.5, 18.5, 5));
    g.fill('M3.5 25.5L21.5 29C21 34.5 17 38.5 12.5 38C7.5 37.5 4 32.5 3.5 25.5Z').cutFill(P.circ(14, 32.5, 2.4));
    g.fill('M44.5 25.5L26.5 29C27 34.5 31 38.5 35.5 38C40.5 37.5 44 32.5 44.5 25.5Z').cutFill(P.circ(34, 32.5, 2.4));
  },
  'person': (g, P) => {            // a single head-and-shoulders bust
    g.fill(P.circ(24, 14, 8));
    g.fill('M8 45C8 32 14.5 26 24 26C33.5 26 40 32 40 45Z');
  },
  'hut': (g, P) => {               // a round hut under a conical thatched roof
    g.fill(P.cap(24, 2.5, 24, 6, 2.6));
    g.fill(P.poly([[24, 4], [46, 27], [42, 25], [38, 28], [33, 25], [28, 28], [24, 25.5], [20, 28], [15, 25], [10, 28], [6, 25], [2, 27]]))
      .cut('M17.5 12H30.5', 1.6).cut('M12 18.5H36', 1.6);
    g.hole(P.rect(10, 29.5, 28, 15, 1.2), 'M19.5 44.5V36A4.5 4.5 0 0 1 28.5 36V44.5Z');
  },
  'crystal-ball': (g, P) => {      // a crystal ball on a stand, a sparkle inside
    g.fill(P.circ(24, 19.5, 14.5)).cut('M14.5 18A10 10 0 0 1 21 10', 2).cutFill(P.star(28, 20, 6, 1.6, 4));
    g.fill(P.poly([[15.5, 36], [32.5, 36], [37, 44.5], [11, 44.5]]));
  },
  'sparkle': (g, P) => {           // a big four-pointed star with small sparks
    g.fill('M20 6Q22 24 38 26Q22 28 20 46Q18 28 2 26Q18 24 20 6Z');
    g.fill('M37 3Q37.8 9.2 44 10Q37.8 10.8 37 17Q36.2 10.8 30 10Q36.2 9.2 37 3Z');
    g.fill(P.circ(39, 40, 2.6));
  },
  'palm': (g, P) => {              // an open hand raised, palm out
    for (const [x, t] of [[15, 13], [21.5, 7], [28, 8], [34, 14]]) g.fill(P.cap(x, 26, x, t, 5));
    g.fill(P.rect(12.5, 22, 24, 17, 5)); g.fill(P.rect(16, 36, 17, 9, 2));
    g.fill(P.cap(14, 34, 6.5, 24.5, 5.4));
  },
  'fist': (g, P) => {              // a raised fist: four curled fingers, the thumb across them, the wrist
    for (const x of [14.5, 21, 27.5, 34]) g.fill(P.cap(x, 9, x, 18, 6));
    g.fill(P.rect(11.5, 13, 25.5, 19, 4)).cut('M17.75 6V16', 1.6).cut('M24.25 6V16', 1.6).cut('M30.75 6V16', 1.6)
      .cut('M11 20.5H27.5C29.5 20.5 30.5 22 30.5 24', 1.8);
    g.fill(P.rect(15.5, 31, 17, 14, 2)).cut('M15 35H33', 1.6);
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
