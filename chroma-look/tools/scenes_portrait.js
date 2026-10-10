// "Their own tarot card": a portrait card of the main character that ages with them.
// One setting per lead colour (w u b r g), the same setting at four ages (child ~8, youth ~17, adult ~40, elder ~75),
// so the card visibly ages. Portrait art: painted on the usual 880x500 stage, the card keeps only the window
// x 293..587, y 40..460 (render_portraits.js cuts it), but the whole stage is painted so the edges are never blank.
// The main character is drawn gender-neutral (hair 'short', wear 'none' or 'coat'), an ink silhouette with a paper rim.
const KIT = '/mnt/project-files/chroma-art/kit/';
const { W, H, rng, r1 } = require(KIT + 'engrave');
const K = require(KIT + 'props');
const Q = require(KIT + 'props2');
const CA = require(KIT + 'props_cards_a');
const CB = require(KIT + 'props_cards_b');
const DB = require(KIT + 'props_domains_b');
const DA = require(KIT + 'props_domains_a');
const LV = require(KIT + 'props_love');
const WK = require(KIT + 'props_work');
const TR = require(KIT + 'props_tribal');
const PR = require(KIT + 'props_v223_prod1');
const W39 = require(KIT + 'props_w39_b');
const KD = require(KIT + 'props_kids');
const { WARM, COLD, DAWN, LEAF, SKY, smoothPath } = K;
const { MORN } = KD;
const { DUSK, EMBER } = CB;
const { FLAME } = TR;
const { solid, joints, reach } = CB;
const { figure: figPaths, smooth } = require(KIT + 'figure');

const AGES = ['child', 'youth', 'adult', 'elder'];
const COLS = ['w', 'u', 'b', 'r', 'g'];

// the main character at each age: a child's proportions, a slim youth, an adult in a coat, an elder in a coat
const BODY = {
  child: { h: 136, child: true, wear: 'none', hair: 'short' },
  youth: { h: 214, build: .9, wear: 'none', hair: 'short' },
  adult: { h: 240, build: 1.02, wear: 'coat', hair: 'short' },
  elder: { h: 228, build: 1, wear: 'coat', hair: 'short' },
};
const mc = (age, o) => ({ ...BODY[age], ...o });
// The coat: figure.js's long coat flares like a skirt when the legs stride, which reads as a dress at card size.
// The main character's coat is cut here instead: to mid-thigh, its front edge kept close to the body,
// its back hem streaming behind in the wind (flap, degrees).
const rad = (a) => a * Math.PI / 180;
function coatPath(o, J, { len = .21, spread = .055, flap = 0 } = {}) {
  const { h, f, hip, sh } = J;
  if ((o.turn || 0) >= .5) {
    // seen from the front or the back: a straight coat, a little wider than the hips
    const g = o.build || 1, top = sh[1] + .012 * h, wy = hip[1] - .14 * h, hy = hip[1] + len * h;
    return smooth([[sh[0] - .04 * h, sh[1] - .012 * h], [sh[0] + .04 * h, sh[1] - .012 * h], [sh[0] + .092 * h * g, top + .01 * h], [sh[0] + .1 * h * g, top + .05 * h], [hip[0] + .088 * h * g, wy],
      [hip[0] + .098 * h * g, hip[1]], [hip[0] + .104 * h * g, hy], [hip[0], hy + .006 * h], [hip[0] - .104 * h * g, hy], [hip[0] - .098 * h * g, hip[1]], [hip[0] - .088 * h * g, wy],
      [sh[0] - .1 * h * g, top + .05 * h], [sh[0] - .092 * h * g, top + .01 * h]], .4);
  }
  const ax = [sh[0] - hip[0], sh[1] - hip[1]], L = Math.hypot(ax[0], ax[1]), ux = ax[0] / L, uy = ax[1] / L, nx = -uy * f, ny = ux * f;
  const sw = .045;
  const at = (t, fr, bk) => { const c = [hip[0] + ax[0] * t, hip[1] + ax[1] * t]; return [[c[0] + nx * fr * h, c[1] + ny * fr * h], [c[0] - nx * bk * h, c[1] - ny * bk * h]]; };
  const [s1, s2] = at(.95, sw * 1.1, sw), [w1, w2] = at(.5, sw * 1.04, sw * .96);
  const knees = (o.legs || [[4, 0], [-4, 0]]).map(([ta]) => [hip[0] + f * Math.sin(rad(ta)) * .245 * h * .95, hip[1] + Math.cos(rad(ta)) * .245 * h * .95]);
  const fwd = Math.max(...knees.map((q) => f * (q[0] - hip[0])));
  const fl = rad(flap), back = f * Math.sin(fl) * len * h * .9, lift = Math.abs(Math.sin(fl)) * len * h * .35;
  let hf, hb, mid = null;
  if (o.seat) { hf = [hip[0] + f * Math.max(fwd * .8, .06 * h), hip[1] + .02 * h]; hb = [hip[0] - f * .08 * h, hip[1] + .05 * h]; }
  else {
    hf = [hip[0] + f * Math.min(Math.max(fwd * .6, .045 * h), spread * h) - back * .35, hip[1] + len * h - lift * .4];
    hb = [hip[0] - f * .075 * h - back, hip[1] + len * h - lift];
    if (flap) mid = [(hf[0] + hb[0]) / 2 - back * .1, (hf[1] + hb[1]) / 2 + .025 * h];
  }
  const pts = [s1, w1, [hip[0] + f * .055 * h, hip[1]], hf, ...(mid ? [mid] : []), hb, [hip[0] - f * .07 * h, hip[1] - .02 * h], w2, s2];
  return smooth(pts, .5);
}
// draw the main character: figure.js's body, the coat cut above, and any extra shapes (a scarf), all under one paper rim
let RIM = 0;
function person(P, o, rim, { extra = [] } = {}) {
  const J = joints(o), coat = o.wear === 'coat';
  let all = figPaths({ ...o, wear: coat ? 'none' : o.wear });
  if ((o.turn || 0) >= .5) {
    // seen from the front or the back the feet point at us: swap figure.js's side-view feet for short rounded ones
    const ps = all.match(/<path d="[^"]+"\/>/g);
    J.knees.forEach((k, i) => { ps[i * 3 + 2] = `<path d="${ell(k.an[0], k.an[1] + .006 * o.h, .028 * o.h, .016 * o.h)}"/>`; });
    all = ps.join('');
  }
  const ds = []; if (coat) ds.push(coatPath(o, J, o.coat || {}));
  for (const e of extra) ds.push(typeof e === 'function' ? e(J) : e);
  all += ds.map((d) => `<path d="${d}"/>`).join('');
  for (const m of all.matchAll(/d="([^"]+)"/g)) P.shade(m[1], 1);
  const id = 'mcrim' + (++RIM), [dx, dy, w = 1.4] = rim;
  P.raw(`<filter id="${id}" x="-20%" y="-20%" width="140%" height="140%"><feOffset in="SourceAlpha" dx="${-dx}" dy="${-dy}" result="o"/><feComposite in="SourceAlpha" in2="o" operator="out" result="edge"/><feGaussianBlur in="edge" stdDeviation="${.3 * w}" result="soft"/><feFlood flood-color="${P.PAPER}"/><feComposite in2="soft" operator="in" result="rim"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="rim"/></feMerge></filter><g fill="${P.INK}" filter="url(#${id})">${all}</g>`);
  return J;
}
const stand = (P, o, rim, opt) => person(P, o, rim, opt);
// a walking stick from the hand to the ground
const stick = (P, J, i, ground, { f = 1, lean = 6, crook = true } = {}) => {
  const [x, y] = J.hands[i].hand;
  if (crook) W39.cane(P, x, y - 2, ground, { f, lean });
  else { const fx = x + f * Math.tan(lean * Math.PI / 180) * (ground - y); P.stroke(`M${r1(x)} ${r1(y - 26)}L${r1(fx)} ${ground}`, 3.4); }
};
// a scarf streaming from the neck in the wind (dir 1 = to the right)
const scarf = (dir = 1, len = 46, w = 7, seed = 1) => (J) => {
  const [nx, ny] = J.neck, n = 10, top = [], bot = [];
  for (let i = 0; i <= n; i++) {
    const u = i / n, x = nx + dir * (4 + u * len), y = ny + 3 + u * 6 + Math.sin(u * 7 + seed) * 4 * u, hw = w * (1 - u * .45) / 2;
    top.push([x, y - hw]); bot.unshift([x, y + hw]);
  }
  return `M${r1(nx - dir * 4)} ${r1(ny - 2)}` + [...top, ...bot].map(([a, b]) => `L${r1(a)} ${r1(b)}`).join('') + `L${r1(nx - dir * 4)} ${r1(ny + 6)}Z`;
};
const ell = (x, y, rx, ry) => `M${r1(x - rx)} ${r1(y)}a${r1(rx)} ${r1(ry)} 0 1 0 ${r1(2 * rx)} 0a${r1(rx)} ${r1(ry)} 0 1 0 ${r1(-2 * rx)} 0Z`;

// ======================================================================= W: the sunlit hall
// A tall hall of pale stone: two columns frame a high arched window full of morning sky; the light pours through it
// onto the flagstones. A stone bench stands under the window. The figure stands upright and still in the light;
// the elder sits on the bench, both hands on a stick.
const hallW = (P) => {
  const FL = 404, CX = 440;
  Q.room(P, { wall: .4, floor: .46, floorY: FL, night: .06, skirting: false });
  // the stone courses of the back wall
  let st = ''; for (let y = FL - 30; y > 0; y -= 30) st += `M0 ${y}H${W}`;
  P.stroke(st, .5, 'opacity=".3"');
  // the high window: a tall round-headed opening, two slender mullions, the morning sky and a far garden's treetops
  const wx = 388, ww = 104, wy = 74, wh = 222;
  LV.archWindow(P, wx, wy, ww, wh, { t: .6, frame: 16, bars: 2, transom: 0, outside: () => {
    for (let i = 0; i < 7; i++) P.tone(P.rect(wx, wy + i * 30, ww, wh), .18 - i * .026, { a: 'h', line: 0 });
    P.wash(P.rect(wx, wy, ww, wh * .5), SKY, .28);
    P.wash(P.rect(wx, wy + wh * .45, ww, wh * .55), MORN, .3);
    KD.cloud(P, wx + 30, wy + 92, 64, { seed: 4, t: .02 });
    KD.birds(P, [[wx + 70, wy + 60, .8], [wx + 82, wy + 52, .6]]);
    // the far garden: a row of rounded treetops along the bottom of the window
    P.tone(`M${wx - 4} ${wy + wh}V${wy + wh - 14}C${wx + 20} ${wy + wh - 20} ${wx + 60} ${wy + wh - 18} ${wx + ww + 4} ${wy + wh - 16}V${wy + wh}Z`, .4, { a: 'a', line: .8 });
    K.tree(P, wx + 16, wy + wh - 10, 66, { t: .44, seed: 7, crown: .85 });
    K.tree(P, wx + ww - 14, wy + wh - 12, 54, { t: .48, seed: 3, crown: .85 });
    P.wash(P.rect(wx, wy + wh - 30, ww, 30), LEAF, .25);
  } });
  // the deep stone sill
  solid(P, P.rect(wx - 26, wy + wh + 16, ww + 52, 10), .62, { a: 'h' });
  // the light: the window glows, a shaft falls forward through the air, a bright patch lies on the floor
  P.light(CX, wy + wh * .55, 230, MORN, .14, .55);
  P.beam(`M${wx} ${wy + wh}L${wx + ww} ${wy + wh}L${wx + ww + 70} 476L${wx - 70} 476Z`, MORN, .34, .14);
  P.beam(`M${wx - 10} ${FL}L${wx + ww + 10} ${FL}L${wx + ww + 64} 476L${wx - 64} 476Z`, MORN, .5, .16);
  // the stone bench under the window, the same in every card
  solid(P, P.rect(CX - 62, 356, 124, 9), .58, { a: 'h' });
  solid(P, `${P.rect(CX - 52, 365, 16, FL - 365)}${P.rect(CX + 36, 365, 16, FL - 365)}`, .66, { a: 'v' });
  // the flagstones: courses running back, joints converging on the window
  let fs = ''; for (const y of [418, 438, 464]) fs += `M0 ${y}H${W}`;
  for (const x of [-200, -40, 120, 280, 600, 760, 920, 1080]) fs += `M${r1(CX + (x - CX) * .32)} ${FL}L${x} 500`;
  P.stroke(fs, .6, 'opacity=".45"');
  // the columns that frame the window, and the arches springing from them overhead
  const arch = `M300 0V70A140 140 0 0 1 580 70V0Z`;
  P.tone(`M240 0H640V70H580A140 140 0 0 0 300 70H240Z`, .5, { a: 'v', line: 1 });
  P.stroke('M300 70A140 140 0 0 1 580 70', 1.2);
  for (const x of [318, 562]) {
    WK.column(P, x, 66, FL, { w: 38, t: .26 });
    P.tone(P.rect(x + 6, 80, 13, FL - 92), .44, { a: 'v', line: 0 });
  }
  P.stroke('M220 0V404M660 0V404', 1);
  return { FL, CX };
};
const W_ = {
  // seen from behind, standing still before the high window, on the lit flagstones in front of the bench
  child: (P) => { const { CX } = hallW(P);
    stand(P, mc('child', { x: CX, y: 434, h: 146, f: 1, turn: 1, legs: [[8, 0], [-8, 0]], arms: [[18, -4], [-18, 4]] }), [-1.4, -1.6]); },
  youth: (P) => { const { CX } = hallW(P);
    stand(P, mc('youth', { x: CX, y: 434, h: 226, f: 1, turn: 1, legs: [[8, 0], [-8, 0]], arms: [[16, -4], [-16, 4]] }), [-1.4, -1.6]); },
  adult: (P) => { const { CX } = hallW(P);
    stand(P, mc('adult', { x: CX, y: 434, h: 250, f: 1, turn: 1, legs: [[8, 0], [-8, 0]], arms: [[15, -4], [-15, 4]] }), [-1.4, -1.6]); },
  // the elder sits on the bench, side-on, both hands on the stick, facing the light
  elder: (P) => { const { FL, CX } = hallW(P);
    const o = mc('elder', { x: CX - 18, seat: 352, f: 1, lean: 16, bow: 14, legs: [[80, 82], [72, 76]], arms: [[0, 0], [0, 0]] });
    o.arms = reach(o, 0, [CX + 36, 334], 1); o.arms = reach({ ...o }, 1, [CX + 30, 340], 1);
    const J = stand(P, o, [-1.4, -1.6]);
    stick(P, J, 0, FL + 2, { f: 1, lean: 4 }); },
};

// ======================================================================= U: the study at night
// A study at night: shelves of books to the ceiling on the left, a window full of stars on the right, the desk under
// it with an open book, a stack of books and a green-shaded lamp, the one warm light. The child stretches on tiptoe
// for a book on the shelf; the youth reads hunched at the desk; the adult stands at the window, book in hand, looking
// up at the stars; the elder reads in the chair, a stick leant against the desk.
const lampU = (P, x, y) => {
  const color = '#e8d08a';
  P.ink(`M${x - 18} ${y}h36v-6h-36ZM${x - 2} ${y - 6}v-30h4v30Z`);
  P.tone(`M${x - 30} ${y - 36}q30 -24 60 0Z`, .75, { a: 'h', line: 1 });
  P.wash(`M${x - 30} ${y - 36}q30 -24 60 0Z`, '#5e8a5a', .45);
  P.lit(`M${x - 28} ${y - 36}h56v4h-56Z`, color, .6, .6);
  P.light(x, y - 24, 150, color, .3, .9);
  P.beam(`M${x - 28} ${y - 34}L${x + 28} ${y - 34}L${x + 80} ${y}L${x - 84} ${y}Z`, color, .6, .14);
};
const studyU = (P) => {
  const FL = 404, DT = 318;
  Q.room(P, { wall: .82, floor: .86, floorY: FL, night: .72 });
  // the window: deep night sky full of stars over the dark roofs
  const wx = 470, wy = 82, ww = 110, wh = 176;
  DA.windowIn(P, wx, wy, ww, wh, { bars: 'v', frame: 12, tone: .88, sill: false, outside: () => {
    for (let i = 0; i < 6; i++) P.tone(P.rect(wx, wy + i * 30, ww, wh), .62 - i * .05, { a: 'h', line: 0 });
    P.wash(P.rect(wx, wy, ww, wh), COLD, .5);
    P.light(wx + ww / 2, wy + wh * .4, 120, null, 0, .35);
    const R = rng(23); let s = '';
    for (let i = 0; i < 60; i++) s += P.circ(wx + R() * ww, wy + R() * (wh - 36), .7 + R() * 1.2);
    P.glint(s);
    const spark = (x, y, r) => P.glint(`M${x} ${y - r}L${x + r * .25} ${y - r * .25}L${x + r} ${y}L${x + r * .25} ${y + r * .25}L${x} ${y + r}L${x - r * .25} ${y + r * .25}L${x - r} ${y}L${x - r * .25} ${y - r * .25}Z`);
    spark(wx + 28, wy + 40, 6); spark(wx + 84, wy + 74, 5); spark(wx + 70, wy + 20, 4); spark(wx + 16, wy + 104, 3.4);
    // the roofs across the street: one dark line, two lit windows
    P.tone(`M${wx - 10} ${wy + wh}V${wy + wh - 22}H${wx + 30}L${wx + 44} ${wy + wh - 34}L${wx + 58} ${wy + wh - 22}H${wx + 78}V${wy + wh - 30}H${wx + ww + 10}V${wy + wh}Z`, .94, { a: 'h', line: .8 });
    P.lit(P.rect(wx + 14, wy + wh - 14, 6, 8), WARM, .6, .5); P.lit(P.rect(wx + 92, wy + wh - 20, 6, 8), WARM, .6, .5);
  } });
  P.tone(P.rect(wx - 20, wy + wh + 12, ww + 40, 9), .8, { a: 'h' });
  P.light(wx + ww / 2, wy + wh / 2, 140, COLD, .16, .4);
  // the shelves, floor to ceiling, on the left
  DB.shelves(P, 232, 394, FL, 26, { t: .86, seed: 4, bay: 162, lo: .52, hi: .88 });
  // the desk under the window: an open book, a stack of books, the lamp
  solid(P, P.rect(446, DT, 190, 10), .74, { a: 'h' });
  solid(P, `${P.rect(456, DT + 10, 10, FL - DT - 10)}${P.rect(612, DT + 10, 10, FL - DT - 10)}`, .88, { a: 'v' });
  solid(P, P.rect(552, DT + 10, 60, 34), .84, { a: 'v' });
  DB.bookStack(P, 586, DT, { n: 4, seed: 7, w: 40 });
  DB.openBook(P, 508, DT, 60);
  lampU(P, 556, DT);
  // the chair at the desk
  Q.chair(P, 430, 346, { f: 1, t: .86 });
  return { FL, DT };
};
const U_ = {
  child: (P) => { const { FL } = studyU(P);
    // a book pulled half out of a high shelf
    const bk = 'M364 262L368 230L382 232L378 264Z';
    CA.solid(P, bk, .2, { a: 'v', line: 1 }); P.wash(bk, '#b5442e', .4);
    P.light(374, 248, 40, null, 0, .4);
    const o = mc('child', { x: 412, y: FL - 6, f: -1, lean: -6, bow: -22, legs: [[2, -6], [-6, -4]], arms: [[0, 0], [-14, 12]] });
    o.arms = reach(o, 0, [376, 238], 1);
    const J = stand(P, o, [1.6, -1.4]);
    // on tiptoe: the toes still on the floor, the heels lifted
    for (const k of J.knees) P.ink(`M${r1(k.an[0] - 4)} ${r1(k.an[1] - 2)}L${r1(k.an[0] + 3)} ${r1(k.an[1])}L${r1(k.an[0] - 8)} ${FL}L${r1(k.an[0] - 14)} ${FL}Z`); },
  youth: (P) => { const { FL, DT } = studyU(P);
    const o = mc('youth', { x: 432, seat: 342, f: 1, lean: 26, bow: 22, legs: [[82, 84], [76, 80]], arms: [[0, 0], [0, 0]] });
    o.arms = reach(o, 0, [496, DT - 4], 1); o.arms = reach({ ...o }, 1, [512, DT - 6], 1);
    stand(P, o, [1.6, -1.4]); },
  adult: (P) => { const { FL, DT } = studyU(P);
    // standing at the window in front of the desk, looking up at the stars, a book held open at the waist
    const o = mc('adult', { x: 474, y: FL + 6, f: 1, lean: -4, bow: -20, legs: [[4, 0], [-4, 0]], arms: [[0, 0], [0, 0]] });
    const J0 = joints(o);
    o.arms = reach(o, 0, [J0.sh[0] + 28, J0.sh[1] + 70], 1);
    o.arms = reach({ ...o }, 1, [J0.sh[0] + 34, J0.sh[1] + 66], 1);
    const J = stand(P, o, [1.6, -1.4]);
    const [hx, hy] = J.hands[1].hand;
    CA.solid(P, `M${r1(hx - 10)} ${r1(hy)}l16 -12l18 4l-14 14Z`, .08, { a: 'h', line: 1 }); },
  elder: (P) => { const { FL, DT } = studyU(P);
    const o = mc('elder', { x: 428, seat: 342, f: 1, lean: 12, bow: 24, legs: [[80, 82], [74, 78]], arms: [[0, 0], [0, 0]] });
    o.arms = reach(o, 0, [482, 296], 1); o.arms = reach({ ...o }, 1, [488, 302], 1);
    // the stick leant against the desk
    P.stroke(`M468 ${FL}L486 ${DT - 34}`, 3.2); P.stroke(`M486 ${DT - 34}c2 -8 12 -8 13 0`, 3.2);
    const J = stand(P, o, [1.6, -1.4]);
    const [hx, hy] = J.hands[0].hand;
    CA.solid(P, `M${r1(hx - 12)} ${r1(hy - 2)}l14 -14l16 8l-14 14Z`, .08, { a: 'h', line: 1 }); },
};

// ======================================================================= B: the city stair at dusk
// A broad stone stair climbs from the lower left to a landing at the foot of a tall tower, its windows lit, against a
// dusk sky; the city's lights spread below. The child climbs the first steps, the youth takes them two at a time, the
// adult strides near the top; the elder stands on the top landing, turned to look down over the lights.
const STAIR = { x0: 286, y0: 470, run: 26, rise: 16, n: 8 };
const stepY = (x) => { const { x0, y0, run, rise, n } = STAIR; const i = Math.max(0, Math.min(n, Math.floor((x - x0) / run) + 1)); return y0 - i * rise; };
const stairB = (P) => {
  P.setNight(.42, 1);
  const HZ = 404;
  // the dusk sky: deep violet overhead, glowing amber low over the city
  const grad = [[0, .88], [50, .8], [100, .7], [150, .58], [200, .46], [250, .34], [300, .24], [340, .16], [370, .1]];
  for (const [y, t] of grad) P.tone(P.rect(0, y, W, HZ - y), t, { a: 'h', line: 0 });
  P.wash(P.rect(0, 0, W, 170), '#6d5a8e', .32);
  P.wash(P.rect(0, 220, W, 190), DUSK, .34);
  P.clip(P.rect(0, 0, W, HZ), () => P.light(400, 390, 260, DUSK, .2, .6));
  const R = rng(31); let s = ''; for (let i = 0; i < 30; i++) s += P.circ(R() * W, 4 + R() * 120, .5 + R() * .8); P.glint(s);
  // the city below: far towers pale, near blocks dark, many windows lit
  K.skyline(P, { base: HZ + 10, lo: 318, hi: 366, seed: 5, t: .5, lit: .14, wmin: 20, wmax: 46 });
  K.skyline(P, { base: 500, lo: 366, hi: 404, seed: 8, t: .82, lit: .42, wmin: 28, wmax: 60 });
  P.light(360, 430, 130, WARM, .18, .35);
  // the tower: a tall slab of a building at the head of the stair, its windows lit, a lit crown and a mast
  const tl = 530, tr = 630, tt = 66;
  P.tone(P.rect(tl, tt, tr - tl, 420 - tt), .86, { a: 'v' });
  P.tone(P.rect(tl + 12, tt - 22, tr - tl - 24, 22), .88, { a: 'v' });
  P.ink(`M${(tl + tr) / 2 - 1.5} ${tt - 22}v-34h3v34Z`);
  const RW = rng(12);
  for (let y = tt + 12; y < 344; y += 15) for (let x = tl + 7; x < tr - 6; x += 12) {
    if (y < tt + 36 || RW() < .45) P.lit(P.rect(x, y, 6, 8), WARM, .6, .45); else P.tone(P.rect(x, y, 6, 8), .96, { a: 'h', line: 0 });
  }
  P.lit(P.rect(tl + 16, tt - 16, tr - tl - 32, 7), WARM, .65, .6);
  P.light(tl + 40, tt + 20, 110, WARM, .22, .5);
  P.wash(P.rect(tl, tt - 22, tr - tl, 60), WARM, .22);
  // the stair: broad stone steps rising to a landing at the tower's foot, a balustrade along the landing
  const { x0, y0, run, rise, n } = STAIR, top = y0 - n * rise, xl = x0 + run * n;
  let d = `M${x0 - 40} 500V${y0}H${x0}`;
  for (let i = 1; i <= n; i++) d += `V${y0 - rise * i}H${x0 + run * i}`;
  d += `H${W}V500Z`;
  solid(P, d, .62, { a: 'd' });
  let nose = ''; for (let i = 1; i <= n; i++) nose += P.rect(x0 + run * (i - 1), y0 - rise * i, run, 3.5);
  nose += P.rect(xl, top, W - xl, 3.5);
  P.tone(nose, .1, { a: 'h', line: .6 });
  P.beam(`M${x0} ${y0}L${xl} ${top}H${W}V500H${x0}Z`, DUSK, .22, .1);
  let posts = ''; for (let x = xl + 40; x < W; x += 15) posts += P.rect(x - 2.5, top - 30, 5, 30);
  P.ink(posts); solid(P, P.rect(xl + 34, top - 36, W, 7), .74, { a: 'h' });
  return { top, xl };
};
const B_ = {
  child: (P) => { stairB(P);
    // climbing the first steps, one foot up a step
    const x = 366, o = mc('child', { x, y: stepY(x - 8) + 1, f: 1, lean: 14, bow: -14, legs: [[50, 74], [-10, 6]], arms: [[40, 30], [-26, 20]] });
    stand(P, o, [-1.6, -1.2]); },
  youth: (P) => { stairB(P);
    // taking the steps two at a time
    const x = 408, o = mc('youth', { x, y: stepY(x - 16) + 1, f: 1, lean: 16, bow: -10, legs: [[52, 66], [-18, 10]], arms: [[-44, 76], [58, 84]] });
    stand(P, o, [-1.6, -1.2]); },
  adult: (P) => { stairB(P);
    const x = 452, o = mc('adult', { x, y: stepY(x - 12) + 1, f: 1, lean: 10, bow: -8, legs: [[40, 54], [-12, 6]], arms: [[-18, 14], [22, 30]], coat: { flap: 8 } });
    stand(P, o, [-1.6, -1.2]); },
  elder: (P) => { const { top, xl } = stairB(P);
    // on the top landing, turned back, looking down over the city's lights
    const o = mc('elder', { x: xl + 4, y: top + 1, f: -1, lean: 10, bow: 22, legs: [[6, 2], [-6, 2]], arms: [[0, 0], [-6, 10]] });
    o.arms = reach(o, 0, [xl - 26, top - 4], 1);
    const J = stand(P, o, [-1.6, -1.2]);
    stick(P, J, 0, top + 1, { f: -1, lean: 4 }); },
};

// ======================================================================= R: the hilltop at sunset
// An open hilltop at sunset in a strong wind: a long sky streaked with cloud, the sun going down behind far hills,
// the grass streaming, a small fire on the crest throwing sparks downwind. The child flies a kite; the youth flings
// both arms open to the wind; the adult strides into it, coat flapping; the elder stands into it on a tall staff.
const hillR = (P) => {
  const HZ = 338;
  // the sky: dusky overhead, burning low down
  const grad = [[0, .58], [50, .5], [100, .42], [150, .34], [200, .26], [250, .18], [290, .1], [318, .05]];
  for (const [y, t] of grad) P.tone(P.rect(0, y, W, HZ - y), t, { a: 'h', line: 0 });
  P.wash(P.rect(0, 0, W, 160), '#8a6a8e', .18);
  P.wash(P.rect(0, 150, W, HZ - 150), DUSK, .34);
  P.wash(ell(330, HZ - 10, 170, 60), '#efb27a', .4);
  // long streaks of cloud driven by the wind
  const R = rng(17); let cl = '';
  for (let i = 0; i < 9; i++) { const y = 70 + i * 26 + R() * 10, x = -40 + R() * 400, w = 260 + R() * 300, h = 5 + R() * 5;
    cl += `M${r1(x)} ${r1(y)}q${r1(w * .5)} ${r1(-h * 1.6)} ${r1(w)} ${r1(-h * .3)}q${r1(-w * .45)} ${r1(h * 1.4)} ${r1(-w)} ${r1(h * .3)}Z`; }
  P.tone(cl, .5, { a: 'h', line: .7 });
  P.wash(cl, '#b9605a', .22);
  // the sun going down behind the far hills, its light low across everything
  P.clip(P.rect(0, 0, W, HZ - 6), () => P.lit(P.circ(336, HZ - 8, 18), '#f2c27a', .7, .9));
  P.light(336, HZ - 12, 240, DAWN, .2, .7);
  P.tone(`M-20 ${HZ}C60 ${HZ - 22} 160 ${HZ - 26} 250 ${HZ - 12}C300 ${HZ - 4} 360 ${HZ - 4} 420 ${HZ - 14}C520 ${HZ - 30} 660 ${HZ - 24} 900 ${HZ - 6}V${HZ + 30}H-20Z`, .64, { a: 'a', line: .9 });
  // the hilltop: a long crest, dark against the bright sky
  const crest = 'M-20 500V444C120 420 260 404 360 400C440 396 500 398 580 408C700 424 800 440 900 452V500Z';
  P.tone(crest, .76, { a: 'd', line: 1.1 });
  P.beam('M-20 444C120 420 260 404 360 400C440 396 500 398 580 408L560 430C480 420 400 418 320 424C200 434 80 450 -20 470Z', DAWN, .3, .16);
  // the grass streaming downwind along the crest
  let gr = ''; const G = rng(4);
  for (let i = 0; i < 120; i++) { const x = 220 + G() * 460, base = 400 + Math.pow((x - 440) / 260, 2) * 40 + G() * 50, hh = 8 + G() * 14;
    gr += `M${r1(x)} ${r1(base)}q${r1(hh * .3)} ${r1(-hh * .6)} ${r1(hh * .9)} ${r1(-hh * .7)}`; }
  P.stroke(gr, .9);
  // the wind itself: a few long flicks across the sky
  P.stroke('M300 128q70 -8 150 4M352 180q60 -6 120 4M470 236q50 -4 96 4', .9, 'opacity=".55"');
  // the small fire on the crest, sparks and smoke blown away downwind
  const fx = 540, fg = 408;
  const fire = CB.campfire(P, fx, fg, { s: .95, r: 130, o: .32, glow: .7 });
  CB.smoke(P, fire[0] + 2, fire[1] + 10, { h: 200, drift: 90, seed: 2, w: .8, t: .14 });
  const RS = rng(9); let sp = '';
  for (let i = 0; i < 30; i++) { const u = RS(), x = fx - 6 + u * 40 + (RS() - .3) * (14 + u * 30), y = fg - 34 - u * 170 - RS() * 20, r = 2.6 - u * 1.3;
    sp += `M${r1(x)} ${r1(y)}l${r1(r * 2.4)} ${r1(-r * .6)}l${r1(-r * .4)} ${r1(r)}Z`; }
  P.glint(sp); P.over(`<path d="${sp}" fill="${FLAME}" opacity=".6"/>`);
  return { HZ };
};
const groundR = (x) => 400 + Math.pow((x - 440) / 260, 2) * 40 - 2;
const R_ = {
  child: (P) => { hillR(P);
    // flying a kite: facing downwind, one arm up holding the string, the kite high up on the right
    const x = 432, o = mc('child', { x, y: groundR(x) + 4, f: 1, lean: -6, bow: -26, legs: [[16, 4], [-14, 6]], arms: [[150, 10], [30, 30]] });
    const J = stand(P, o, [-1.8, -.8], { extra: [scarf(1, 34, 6, 2)] });
    const [hx, hy] = J.hands[0].hand, kx = 540, ky = 108;
    P.stroke(`M${r1(hx)} ${r1(hy)}Q${r1((hx + kx) / 2 + 26)} ${r1((hy + ky) / 2 + 30)} ${kx} ${ky + 20}`, .8);
    const kite = `M${kx} ${ky - 18}L${kx + 14} ${ky - 2}L${kx} ${ky + 20}L${kx - 13} ${ky - 2}Z`;
    CA.solid(P, kite, .2, { a: 'h', line: 1.1 }); P.wash(kite, '#b5442e', .4);
    P.stroke(`M${kx} ${ky + 20}q12 10 6 22q-8 12 6 22q12 10 22 4`, 1);
    P.ink(`M${kx + 4} ${ky + 32}l5 -3l1 6ZM${kx + 8} ${ky + 54}l5 -3l1 6Z`); },
  youth: (P) => { hillR(P);
    const x = 446, o = mc('youth', { x, y: groundR(x) + 4, f: -1, lean: -8, bow: -18, legs: [[14, 2], [-16, 4]], arms: [[122, 8], [-118, -8]] });
    stand(P, o, [-1.8, -.8]); },
  adult: (P) => { hillR(P);
    const x = 446, o = mc('adult', { x, y: groundR(x) + 4, f: -1, lean: 14, bow: -4, legs: [[24, 8], [-22, 18]], arms: [[-34, 40], [40, 50]], coat: { flap: 30, len: .25 } });
    stand(P, o, [-1.8, -.8]); },
  elder: (P) => { hillR(P);
    const x = 446, o = mc('elder', { x, y: groundR(x) + 4, f: -1, lean: 10, bow: 4, legs: [[10, 2], [-8, 4]], arms: [[0, 0], [70, 10]], coat: { flap: 26, len: .25 } });
    o.arms = reach(o, 0, [x - 34, 270], 1);
    const J = stand(P, o, [-1.8, -.8]);
    // the tall staff
    const [hx, hy] = J.hands[0].hand;
    P.stroke(`M${r1(hx + 2)} ${r1(hy - 40)}L${r1(hx - 6)} ${r1(groundR(hx) + 6)}`, 3.6); },
};

// ======================================================================= G: the great tree in the clearing
// A clearing in an old forest, one great tree at its heart, its dark crown filling the sky; sunlight slants down through
// a gap in the canopy onto the moss. On the left a sapling the child planted, which grows from card to card.
// The child waters it from a can; the youth, the adult and the elder each stand with a hand on the great trunk.
const SAP = { child: 30, youth: 70, adult: 118, elder: 164 };
const { capsule } = require(KIT + 'figure');
const treeG = (P, age) => {
  const GR = 404, TX = 532;
  Q.outdoors(P, { sky: .24, ground: .5, horizon: 340 });
  P.wash(P.rect(0, 0, W, 340), LEAF, .16);
  // the far forest: trunks fading back into green light
  const R = rng(14);
  for (let i = 0; i < 22; i++) { const x = R() * W, w = 7 + R() * 14, t = (x > 290 && x < 430 ? .18 : .36) + R() * .22;
    P.tone(`M${r1(x - w / 2)} 362L${r1(x - w * .35)} 0H${r1(x + w * .35)}L${r1(x + w / 2)} 362Z`, t, { a: 'v', line: .7 }); }
  P.tone(P.rect(0, 296, W, 66), .44, { a: 'a', line: 0 });
  P.wash(P.rect(0, 296, W, 66), LEAF, .2);
  // the forest floor and the clearing, a pool of light in the middle
  P.tone(`M-20 500V372C160 354 300 348 440 350C600 352 740 358 900 374V500Z`, .6, { a: 'h', line: 1 });
  // the great tree: a broad trunk flaring into roots, three great limbs into the crown
  const limbs = [[[TX - 14, 214], 22, [TX - 120, 92], 9], [[TX + 12, 210], 20, [TX + 84, 70], 9], [[TX, 206], 18, [TX - 18, 44], 8], [[TX - 60, 150], 10, [TX - 150, 128], 5]];
  P.tone(limbs.map(([A, ra, B, rb]) => capsule(A, ra, B, rb)).join(''), .76, { a: 'v', line: 1.1 });
  const trunk = `M${TX - 86} ${GR + 6}C${TX - 52} ${GR - 2} ${TX - 38} ${GR - 24} ${TX - 36} ${GR - 64}C${TX - 34} 290 ${TX - 40} 240 ${TX - 30} 196L${TX + 30} 196C${TX + 38} 240 ${TX + 34} 290 ${TX + 36} ${GR - 64}C${TX + 38} ${GR - 24} ${TX + 56} ${GR - 2} ${TX + 92} ${GR + 8}Z`;
  P.tone(trunk, .72, { a: 'v', line: 1.2 });
  // the bark: long furrows, the lit side and the shadowed side, the roots' knuckles
  P.tone(`M${TX + 14} 200C${TX + 22} 250 ${TX + 22} 300 ${TX + 24} ${GR - 60}C${TX + 26} ${GR - 24} ${TX + 40} ${GR - 4} ${TX + 70} ${GR + 6}L${TX + 92} ${GR + 8}C${TX + 56} ${GR - 2} ${TX + 38} ${GR - 24} ${TX + 36} ${GR - 64}C${TX + 34} 290 ${TX + 38} 240 ${TX + 30} 196Z`, .92, { a: 'v', line: 0 });
  let bk = ''; const RB = rng(3);
  for (let i = 0; i < 8; i++) { const x = TX - 30 + i * 7 + RB() * 3; bk += `M${r1(x + (i - 4) * 3)} ${GR - 10}C${r1(x + RB() * 6 - 3)} 320 ${r1(x - 3)} 260 ${r1(x - 2 + (i - 4) * 1.5)} ${r1(200 + RB() * 30)}`; }
  P.stroke(bk, .9, 'opacity=".65"');
  P.stroke(`M${TX - 60} ${GR + 2}q16 -10 26 -26M${TX + 50} ${GR + 2}q-14 -8 -20 -24`, 1.1);
  // the crown: dark, heavy leaf filling the sky, a gap of light at the upper left
  // many leafy clumps, the far ones first, packed into one heavy crown
  const RC = rng(6), clumps = [];
  for (let i = 0; i < 64; i++) { const x = 350 + RC() * 400, y = -20 + RC() * 150 + Math.abs(x - 560) * .2, r = 18 + RC() * 22; clumps.push([x, y, r]); }
  clumps.sort((p, q) => p[1] - q[1]);
  for (const [cx, cy, r] of clumps) {
    const pts = []; for (let j = 0; j < 14; j++) { const a = j / 14 * Math.PI * 2, k = .82 + RC() * .3; pts.push([cx + Math.cos(a) * r * 1.25 * k, cy + Math.sin(a) * r * .8 * k]); }
    P.tone(smoothPath(pts), .74 + RC() * .16, { a: j2(cx), line: .6 });
  }
  P.tone(`M-20 0H330C320 30 290 60 300 100C250 120 200 110 160 140C100 130 40 150 -20 140Z`, .84, { a: 'a', line: 1 });
  P.wash(P.rect(200, 0, 560, 200), LEAF, .34);
  let lf = ''; const RL = rng(19);
  for (let i = 0; i < 70; i++) { const x = 340 + RL() * 360, y = 4 + RL() * 180; lf += `M${r1(x)} ${r1(y)}q4 -5 9 -2`; }
  P.over(`<path d="${lf}" stroke="${P.PAPER}" stroke-width="1" opacity=".35" fill="none"/>`);
  // the sunlight slanting down through the gap onto the clearing
  P.beam('M300 90L360 70L500 420L374 428Z', MORN, .5, .14);
  P.beam(ell(428, 414, 150, 26), MORN, .55, .2);
  P.light(400, 250, 180, MORN, .12, .35);
  // ferns and moss tufts round the clearing
  let fn = ''; const F = rng(8);
  for (let i = 0; i < 18; i++) { const x = 240 + F() * 420, y = 404 + F() * 80; if (Math.abs(x - 430) < 90 && y < 440) continue;
    for (const s of [-1, 1]) fn += `M${r1(x)} ${r1(y)}q${r1(s * 6)} -14 ${r1(s * 18)} -16`; }
  P.stroke(fn, 1);
  // the sapling, grown a little more in each card
  const sh = SAP[age], sx = 346;
  P.tone(ell(sx, GR + 8, 16, 4), .82, { a: 'h', line: .6 });
  if (sh < 50) {
    P.ink(`M${sx - 1.4} ${GR + 6}V${GR + 6 - sh}h2.8V${GR + 6}Z`);
    P.tone(`M${sx} ${GR + 6 - sh * .55}c-10 -3 -16 -10 -15 -18c8 -1 14 7 15 18ZM${sx} ${GR + 6 - sh * .9}c7 -7 15 -9 19 -5c-4 8 -12 9 -19 5Z`, .5, { a: 'a', line: .8 });
    P.wash(ell(sx, GR - sh * .7, 16, 12), LEAF, .45);
  } else {
    K.tree(P, sx, GR + 6, sh, { t: .58, seed: 4, crown: .9 });
    P.wash(ell(sx, GR + 6 - sh * .72, sh * .32, sh * .28), LEAF, .4);
  }
  return { GR, TX };
};
const j2 = (x) => (Math.round(x / 10) % 2 ? 'a' : 'd');
const handOnTrunk = (o, i, y, TX) => reach(o, i, [TX - 36, y], 1);
const G_ = {
  child: (P) => { const { GR } = treeG(P, 'child');
    // watering the sapling: facing it, the can held out, a thin fall of water
    const o = mc('child', { x: 400, y: GR + 4, f: -1, lean: 10, bow: 16, legs: [[6, 0], [-6, 2]], arms: [[0, 0], [-10, 10]] });
    o.arms = reach(o, 0, [378, GR - 66], 1);
    const J = stand(P, o, [-1.6, -1.4]);
    const [hx, hy] = J.hands[0].hand;
    PR.wateringCan(P, hx + 2, hy - 2, { s: .62, f: -1, t: .5 });
    const sx = hx + 2 - 52 * .62, sy = hy - 2 + 8 * .62;
    P.over(`<path d="M${r1(sx)} ${r1(sy)}q-4 10 -2 ${r1(GR - sy - 30)}M${r1(sx - 3)} ${r1(sy + 2)}q-3 10 -4 ${r1(GR - sy - 34)}" stroke="${'#7d9ccc'}" stroke-width="1" opacity=".7" fill="none"/>`); },
  youth: (P) => { const { GR, TX } = treeG(P, 'youth');
    const o = mc('youth', { x: 438, y: GR + 4, f: 1, lean: -6, bow: -26, legs: [[6, 0], [-8, 2]], arms: [[0, 0], [-4, 8]] });
    o.arms = handOnTrunk(o, 0, 236, TX);
    stand(P, o, [-1.6, -1.4]); },
  adult: (P) => { const { GR, TX } = treeG(P, 'adult');
    const o = mc('adult', { x: 432, y: GR + 4, f: 1, lean: 4, bow: 10, legs: [[8, 0], [-8, 2]], arms: [[0, 0], [-4, 8]] });
    o.arms = handOnTrunk(o, 0, 250, TX);
    stand(P, o, [-1.6, -1.4]); },
  elder: (P) => { const { GR, TX } = treeG(P, 'elder');
    const o = mc('elder', { x: 430, y: GR + 4, f: 1, lean: 12, bow: 14, legs: [[8, 2], [-8, 4]], arms: [[0, 0], [0, 0]] });
    o.arms = handOnTrunk(o, 0, 270, TX);
    const J0 = joints(o);
    o.arms = reach({ ...o }, 1, [J0.hip[0] + 2, J0.hip[1] + 26], 1);
    const J = stand(P, o, [-1.6, -1.4]);
    stick(P, J, 1, GR + 6, { f: 1, lean: -4 }); },
};

const SCENES = {}, ORDER = [];
const BY = { w: W_, u: U_, b: B_, r: R_, g: G_ };
for (const c of COLS) for (const a of AGES) { const n = `portrait-${c}-${a}`; SCENES[n] = BY[c][a]; ORDER.push(n); }
module.exports = { SCENES, ORDER, AGES, COLS };
