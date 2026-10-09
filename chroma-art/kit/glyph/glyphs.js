// The sample set: the five colours, the four meters and the 25 life domains.
const { glyph } = require('./glyph');

const HEART = 'M24 42C10 32 4 25 4 17C4 10 9 6 15 6C19 6 22 8 24 11C26 8 29 6 33 6C39 6 44 10 44 17C44 25 38 32 24 42Z';

const G = {
  // ---- the five colours (our own signs, not Magic's mana symbols) ----
  'color W': (g, P) => {           // a column: order, law, the common good
    g.fill(P.rect(9, 6, 30, 5, 1.2));
    g.fill(P.poly([[12, 12.5], [36, 12.5], [33, 16.5], [15, 16.5]]));
    for (const x of [15, 21.7, 28.4]) g.fill(P.rect(x, 18, 4.6, 17.5, 1));
    g.fill(P.rect(13, 37, 22, 3.6, 1)); g.fill(P.rect(9, 42, 30, 4, 1.2));
  },
  'color U': (g, P) => {           // an open eye: seeing, knowing
    g.hole('M3 24Q24 4 45 24Q24 44 3 24Z', 'M9.5 24Q24 10.5 38.5 24Q24 37.5 9.5 24Z');
    g.hole(P.circ(24, 24, 5.8), P.circ(24, 24, 2.3));
  },
  'color B': (g, P) => {           // a crown: power, ambition
    g.fill(P.poly([[9, 31], [7.5, 14], [16.5, 22], [24, 9], [31.5, 22], [40.5, 14], [39, 31]]));
    g.fill(P.circ(7.5, 11.5, 2.7)); g.fill(P.circ(24, 6.5, 2.7)); g.fill(P.circ(40.5, 11.5, 2.7));
    g.hole(P.rect(8, 33.5, 32, 7.5, 1.6), P.poly([[24, 35], [26.6, 37.25], [24, 39.5], [21.4, 37.25]]), P.circ(14, 37.25, 1.4), P.circ(34, 37.25, 1.4));
  },
  'color R': (g) => {              // a tall flame: passion, action
    g.hole('M24 45C13 45 8.5 36 11.5 28C13.5 22 19 18.5 18 9C24.5 13 26.5 19 25.5 24C28.5 21 29.5 17 28.5 12.5C35.5 18.5 39.5 27 36.5 35.5C34.5 41.5 30 45 24 45Z',
      'M24 40.5C19.5 40.5 17.5 36 19.5 32C20.5 29.5 23 28 23 24C27 27 29 30.5 28.5 34.5C28 38.5 26.5 40.5 24 40.5Z');
  },
  'color G': (g, P) => {           // a seedling: growth, nature
    g.fill(P.cap(10, 43.5, 38, 43.5, 3.2));
    g.fill(P.cap(24, 42, 24, 25, 3.2));
    g.fill(P.lens(23, 28, 7, 18, 4.2)).cut('M20 26L11 20.5', 1.4);
    g.fill(P.lens(25, 23, 42, 9, 5)).cut('M28 20.5L38 12.5', 1.4);
  },

  // ---- the four meters ----
  'meter content': (g, P) => {     // the sun up over the horizon
    g.fill(P.cap(5, 39, 43, 39, 3.2));
    g.fill('M12 35.5A12 12 0 0 1 36 35.5Z');
    for (const a of [180, 215, 250, 290, 325, 360]) { const c = Math.cos(a * Math.PI / 180), s = Math.sin(a * Math.PI / 180); if (a === 180 || a === 360) continue; g.fill(P.cap(24 + c * 16, 35.5 + s * 16, 24 + c * 22, 35.5 + s * 22, 3.2)); }
  },
  'meter peace': (g, P) => {       // a moon over still water
    g.fill(P.circ(22, 16, 11)).cutFill(P.circ(27, 12.5, 9.5));
    g.layer();
    g.fill(P.cap(6, 32, 42, 32, 3.2)); g.fill(P.cap(12, 39, 36, 39, 3.2)); g.fill(P.cap(18, 45, 30, 45, 3));
  },
  'meter strain': (g, P) => {      // a spring pressed flat under a weight
    g.fill(P.rect(9, 5, 30, 12, 2.4)).cut('M15 9.5H33', 1.6);
    const zz = [[14, 20.5], [34, 24.5], [14, 28.5], [34, 32.5], [14, 36.5], [34, 40.5]];
    for (let i = 0; i < zz.length - 1; i++) g.fill(P.cap(...zz[i], ...zz[i + 1], 2.8));
    g.fill(P.rect(7, 42.5, 34, 4, 1.6));
  },
  'meter wanting': (g, P) => {     // a star just out of reach of a ladder
    g.fill(P.star(35, 10.5, 8.5, 3.6));
    g.fill(P.cap(6, 46, 18, 22, 2.8)); g.fill(P.cap(15, 46, 27, 22, 2.8));
    for (const t of [0.18, 0.43, 0.68, 0.93]) { const y = 46 - t * 24, xl = 6 + t * 12; g.fill(P.cap(xl, y, xl + 9, y, 2.4)); }
  },

  // ---- the 25 life domains ----
  'domain work': (g, P) => {
    g.hole(P.rect(17, 6, 14, 10, 3), P.rect(20, 9.5, 8, 7, 1.5));
    g.fill(P.rect(5, 15, 38, 10.5, 3)); g.fill(P.rect(5, 27.5, 38, 15.5, 3));
    g.fill(P.rect(20.5, 22, 7, 8, 1.2));
  },
  'domain family': (g, P) => {
    g.fill(P.circ(11, 10.5, 4.6)); g.fill(P.rect(5, 17, 12, 27.5, 5.5));
    g.fill(P.circ(37, 10.5, 4.6)); g.fill(P.rect(31, 17, 12, 27.5, 5.5));
    g.fill(P.circ(24, 22, 3.8)); g.fill(P.rect(19.5, 28, 9, 16.5, 4.2));
  },
  'domain home': (g, P) => {
    g.fill(P.rect(31, 7, 5, 10, 0.8));
    g.fill(P.poly([[3, 23], [24, 5.5], [45, 23], [41.5, 26.5], [24, 12], [6.5, 26.5]]));
    g.hole(P.poly([[10.5, 28], [24, 16.5], [37.5, 28], [37.5, 44.5], [10.5, 44.5]]), P.rect(20, 32, 8, 12.5, 1), P.circ(24, 24.5, 2.2));
  },
  'domain body': (g, P) => {
    g.fill(P.circ(31, 8, 4.4));
    g.fill(P.cap(28.5, 15, 22.5, 27, 5.2));
    g.fill(P.cap(26.5, 16.5, 19, 21, 3.4)); g.fill(P.cap(19, 21, 14.5, 17, 3.4));
    g.fill(P.cap(27.5, 17.5, 33.5, 22.5, 3.4)); g.fill(P.cap(33.5, 22.5, 38.5, 18.5, 3.4));
    g.fill(P.cap(22.5, 27, 30, 33.5, 4.2)); g.fill(P.cap(30, 33.5, 29, 43, 4)); g.fill(P.cap(29, 43, 33, 43.5, 3));
    g.fill(P.cap(22.5, 27, 16, 35, 4.2)); g.fill(P.cap(16, 35, 8, 33.5, 4));
  },
  'domain health': (g) => { g.fill(HEART).cut('M5 22H15L18.5 15.5L23.5 30L28 18L31 22H43', 2.6); },
  'domain school': (g, P) => {
    g.fill(P.arc(24, 10.5, 5, 180, 360, 2.8));
    g.fill('M10 22C10 14.5 15 11 24 11C33 11 38 14.5 38 22V41C38 43.5 36.5 45 34 45H14C11.5 45 10 43.5 10 41Z')
      .cut('M10.5 22.5C15 25 33 25 37.5 22.5', 2).cut(P.rect(15.5, 30, 17, 10, 2), 2).cut('M21 30V27', 2).cut('M27 30V27', 2);
  },
  'domain friends': (g, P) => {
    g.fill(P.circ(15.5, 13, 6.2)); g.fill('M3 45C3 32 8 25.5 15.5 25.5C23 25.5 28 32 28 45Z')
      .cut(P.circ(32.5, 15.5, 6.2), 2.6).cut('M20 45C20 33.5 25 28 32.5 28C40 28 45 33.5 45 45', 2.6);
    g.layer(); g.fill(P.circ(32.5, 15.5, 6.2)); g.fill('M20 45C20 33.5 25 28 32.5 28C40 28 45 33.5 45 45Z');
  },
  'domain leisure': (g, P) => {
    g.fill('M4 23C6 12 14 6.5 24 6.5C34 6.5 42 12 44 23C40 21 36 21 34 23C30 21 27.5 21 24 23C20.5 21 18 21 14 23C12 21 8 21 4 23Z')
      .cut('M24 7.5L16 22', 1.8).cut('M24 7.5L32 22', 1.8);
    g.fill(P.cap(24, 23.5, 24, 43, 3)); g.fill(P.cap(10, 44, 38, 44, 3));
  },
  'domain money': (g, P) => {
    for (const y of [37, 30, 23]) g.fill(P.rect(5, y, 23, 6, 3));
    g.layer(); g.fill(P.circ(33, 31, 10.5)).cut(P.circ(33, 31, 6.8), 1.6).cutFill(P.poly([[33, 27.6], [36.4, 31], [33, 34.4], [29.6, 31]]));
  },
  'domain community': (g, P) => {
    g.hole(P.poly([[3, 45], [3, 30], [10.5, 23], [18, 30], [18, 45]]), P.rect(7, 32, 4, 4));
    g.hole(P.poly([[30, 45], [30, 28], [37.5, 21], [45, 28], [45, 45]]), P.rect(37, 31, 4, 4));
    g.layer(); g.hole(P.poly([[14, 45], [14, 22], [24, 12], [34, 22], [34, 45]]), P.rect(20.5, 34, 7, 11), P.circ(24, 24, 2.4));
  },
  'domain love': (g) => { g.fill(HEART).cut('M10.5 16C10.5 13 12.5 11 15.5 10.8', 2.4); },
  'domain loss': (g, P) => {       // a tulip bowed over on its stem, petals fallen
    g.fill('M13 45C12 34 13 24 18 17C22 11.5 30 10 34 15.5C35.5 17.5 36 20 35.5 22L33.5 22C34 20.5 33.5 18.5 32.5 17.5C29.5 13.5 23.5 14.5 20.5 19C16.5 25 15.5 34 16.2 45Z');
    g.fill('M29 23.5H40.5C41 29 39.5 35 34.75 37C30 35 28.5 29 29 23.5Z').cut('M34.75 24V36', 1.5).cut('M31.5 23.5L33 30', 1.2).cut('M38 23.5L36.5 30', 1.2);
    g.fill(P.lens(14.5, 35, 5, 27, 3.2)).cut('M13.5 34L7 28.5', 1.1);
    g.fill(P.lens(30, 44.5, 37, 42.5, 1.7)); g.fill(P.lens(39, 45.5, 44.5, 41.5, 1.5));
  },
  'domain inner': (g, P) => {
    g.fill(P.circ(24, 24, 20)).cut(P.circ(24, 24, 16.5), 1.4).cutFill(P.circ(24, 20, 5)).cutFill(P.poly([[21.6, 22.5], [26.4, 22.5], [28, 34.5], [20, 34.5]]));
  },
  'domain children': (g, P) => {
    g.fill('M9 25A15 15 0 0 1 24 10V25Z');
    g.fill('M7 27H40Q40 37.5 30 39H17Q7 37.5 7 27Z');
    g.fill(P.cap(39.5, 27, 41.5, 15, 3)); g.fill(P.cap(41.5, 15, 45.5, 14, 3));
    g.hole(P.circ(15, 43, 4.4), P.circ(15, 43, 1.8)); g.hole(P.circ(32, 43, 4.4), P.circ(32, 43, 1.8));
  },
  'domain nature': (g, P) => {
    g.fill(P.circ(39, 10, 5));
    g.fill(P.poly([[2, 43], [18.5, 13], [35, 43]])).cut('M13 23.5L16 27L18.5 23L21 27L24 23.5', 1.8).cut(P.poly([[21, 43], [33.5, 21], [46, 43]]), 2.6);
    g.layer(); g.fill(P.poly([[21, 43], [33.5, 21], [46, 43]]));
  },
  'domain public life': (g, P) => {
    g.fill(P.rect(17, 5, 14, 17, 1.2)).cut('M20.5 13L23 16L28 9', 2);
    g.hole(P.rect(7, 24, 34, 21, 2.2), P.rect(15, 27.5, 18, 2.8, 1.2));
  },
  'domain partner': (g, P) => {
    // two interlocked rings: B under A at the lower crossing, A under B at the upper one
    g.hole(P.circ(30, 22, 12.5), P.circ(30, 22, 8.5)).cutFill(P.arc(18, 26, 10.5, 15, 58, 6.6));
    g.layer();
    g.hole(P.circ(18, 26, 12.5), P.circ(18, 26, 8.5)).cutFill(P.arc(30, 22, 10.5, 195, 238, 6.6));
  },
  'domain play': (g, P) => {
    g.fill(P.poly([[24, 3], [36, 16], [24, 31], [12, 16]])).cut('M24 4V30', 1.8).cut('M13 16H35', 1.8);
    g.fill(P.cap(24, 31, 21, 36.5, 1.8)); g.fill(P.cap(21, 36.5, 26, 40.5, 1.8)); g.fill(P.cap(26, 40.5, 22.5, 46, 1.8));
    g.fill(P.poly([[17.5, 34], [21, 36.5], [17.5, 39]])); g.fill(P.poly([[24.5, 36.5], [21, 36.5], [24.5, 34]]));
    g.fill(P.poly([[29.5, 38], [26, 40.5], [29.5, 43]]));
  },
  'domain conflict': (g, P) => {
    g.fill(P.cap(3, 24, 16, 24, 3.6)); g.fill(P.poly([[14.5, 16], [22.5, 24], [14.5, 32]]));
    g.fill(P.cap(45, 24, 32, 24, 3.6)); g.fill(P.poly([[33.5, 16], [25.5, 24], [33.5, 32]]));
    for (const [x1, y1, x2, y2] of [[24, 9, 24, 13.5], [24, 34.5, 24, 39], [17, 11, 19.5, 15], [31, 11, 28.5, 15], [17, 37, 19.5, 33], [31, 37, 28.5, 33]]) g.fill(P.cap(x1, y1, x2, y2, 2.4));
  },
  'domain faith': (g, P) => {      // someone kneeling, head bowed, hands together
    g.fill(P.circ(28.5, 12.5, 4.6));
    g.fill(P.cap(19, 33, 23.5, 19, 7.4));
    g.fill(P.cap(19, 34, 29, 42.5, 6.2)); g.fill(P.cap(29, 43, 11, 43.5, 5)); g.fill(P.cap(11, 43.5, 7, 45.5, 3));
    g.fill(P.cap(23.5, 20, 28, 28.5, 3.6)); g.fill(P.cap(28, 28.5, 33, 19.5, 3.4)); g.fill(P.lens(33.5, 21, 35.5, 14, 1.4));
  },
  'domain era': (g, P) => {
    g.fill(P.rect(9, 4, 30, 4.4, 1.6)); g.fill(P.rect(9, 39.6, 30, 4.4, 1.6));
    for (const s of [1, -1]) { const X = (x) => 24 + s * (x - 24); g.fill(P.cap(X(13.5), 9, X(13.5), 13, 2.6)); g.fill(P.cap(X(13.5), 13, X(22.5), 24, 2.6)); g.fill(P.cap(X(22.5), 24, X(13.5), 35, 2.6)); g.fill(P.cap(X(13.5), 35, X(13.5), 39, 2.6)); }
    g.fill(P.poly([[17, 15], [31, 15], [24, 22.5]])); g.fill(P.poly([[16.5, 37.5], [24, 30.5], [31.5, 37.5]])); g.fill(P.cap(24, 23.5, 24, 30, 1.4));
  },
  'domain passion': (g, P) => {
    g.hole('M12.5 23.5C7 26 6 36 11.5 41C17 46 27 44.5 28.5 37.5C29.5 33 32.5 33 34 30C36.5 25.5 33 19.5 27.5 20C24.5 20.3 23.5 23 20 22.5C17.5 22.2 15 22.3 12.5 23.5Z', P.circ(20.5, 32.5, 3.6));
    g.fill(P.cap(27, 26, 40, 11, 3.6)); g.fill(P.cap(39.5, 11.5, 43.5, 5.5, 5.4));
  },
  'domain travel': (g, P) => {
    g.fill('M4 33.5H44L38.5 42.5H10.5Z');
    g.fill(P.cap(24, 5.5, 24, 32, 2.4));
    g.fill(P.poly([[26.5, 7], [41, 28.5], [26.5, 28.5]])); g.fill(P.poly([[21.5, 11], [21.5, 28.5], [8.5, 28.5]]));
    g.fill(P.poly([[25, 3], [32, 5.5], [25, 8]]));
  },
  'domain mind': (g) => {
    g.fill('M14 45V37C8 33 6.5 27 6.5 21.5C6.5 11 14.5 4.5 24 4.5C33.5 4.5 40.5 11 40.5 19.5L44.5 28L40.5 29V34C40.5 37 38 38.5 34.5 38.5H30V45Z')
      .cut('M24 19.5m0 -1.2a1.4 1.4 0 1 1 -1.4 1.4a2.8 2.8 0 0 1 2.8 -2.8a4.4 4.4 0 0 1 4.4 4.4a6 6 0 0 1 -6 6a7.6 7.6 0 0 1 -7.6 -7.6', 2.1);
  },
  'domain study': (g) => {
    g.fill('M24 13C18 9.5 10 9.5 3.5 11.5V38C10 36 18 36 24 39.5Z').fill('M24 13C30 9.5 38 9.5 44.5 11.5V38C38 36 30 36 24 39.5Z');
    g.cut('M24 12V41', 2.2);
    for (const y of [18, 24, 30]) g.cut(`M8 ${y}C12.5 ${y - 1.4} 16.5 ${y - 1.2} 20 ${y + 0.4}`, 1.5).cut(`M40 ${y}C35.5 ${y - 1.4} 31.5 ${y - 1.2} 28 ${y + 0.4}`, 1.5);
  },
};

module.exports = { GLYPHS: Object.entries(G).map(([n, f]) => glyph(n, f)) };
