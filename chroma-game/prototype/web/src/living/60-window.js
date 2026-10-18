"use strict";
/* ---------------- the Living HUD: the life's window (v23 row V6; plan: the Living HUD in v23, step 8) ----------------
   A round stained-glass rose window that is glazed as the person lives, one pane a year, and at the end of the life is
   lit from behind. Ported from the showcase's window.js (its runtime part; not its demo or test hooks).
   On the game page (the piece at the end of this file):
     the medallion    a small window in the Status panel's crest, on the right, as their portrait is on the left: a pane
                      for each year as it is lived. The crest is rebuilt with the HUD (renderHud), so the hook puts the
                      same medallion back each time; a new life (or a load) gets a new one.
     the end          the full window in the review, in the place of the ink look's portrait (.lk-final), with their name
                      and years beneath it. "Finis" and the rest of the review stay, and the light never falls on the
                      review's buttons. It waits while a chapter plate is up, then lights up over about 11 s; a click,
                      Space or Esc skips to the lit window (Space only when the focus is not on a button), never Enter
                      (Enter still starts a new life). Still when motion is off.
   Decoration only: it reads the life as the page has it (S, the story items, the stop log) and changes nothing.

   The plan of the window (the cartoon, as a glazier would call it) is the same for every life and never reads ahead: it
   is drawn for a century, as today's life river runs from 0 to 100, and it does not know when the life will end.
     the boss         a small crystal at the centre: the birth. In the HUD's medallion it glows warm from birth, the one
                      light in a window still waiting for its glass.
     six rings        a layout only, from the centre out: petals for 0 to 10, five lobes for 10 to 15, then pointed
                      lancets for 15 to 25, 25 to 36, 36 to 60 and 60 to 100. Each ring holds one pane per year, the first
                      at the top, the rest clockwise. A life past 100 widens the last ring to hold every year it has
                      lived, never more. An iron ring (the armature) parts the rings; it stands from birth, as a window's
                      frame is set before its glass. The rings' bounds fall where the game's rites of passage fall (15,
                      25, 36, 60), but the words on hover always name the game's own stage of life for that year.
   What each pane shows, read from that year's row of the life river (S.river: shares W U B R G, satisfaction, peace),
   that year's chapter line (S.items, tag "chapter": who they were, as the game recorded it, and the stage of life) and
   the story lines of that year (S.items):
     the glass        cut into two to four pieces, as a glazier cuts glass. The leading colour fills the head of the arch;
                      any other colour that is part of who they are, or at least 12% that year, has its own piece below
                      it, in the pie's order (three at most besides the leader; when a fourth would be needed, the two
                      weakest share the last piece). The colours left share the foot of the pane as one streaky sheet in
                      their own pale hues, the strongest as its ground and each as veins as strong as its share. Each
                      piece is as large as its share. Who they are shines as bold jewel glass; the rest is paler glass
                      of the same hue, never grey, so in a life led by one colour the others are smaller, not lesser
                      (rule 4). The cuts lean the same way all round a ring, so a colour that holds for years runs
                      round the ring as a band.
                      Brightness comes from satisfaction (a hard year is deep, dense glass; a happy one luminous);
                      clarity from peace (a troubled year is milky and full of seeds, a peaceful one clear, with a
                      bright glint across it). The years before the river's record, and a year with every colour even,
                      are pearl glass with the five colours faint in it: the even start every life grows from.
     heavier lead     a turning point: who they are changed from the year before (the chapter line's identity), or the
                      year held a breakthrough, a crisis, a turn or a rite of passage. A rite that falls on the first year
                      of a ring is told by the iron ring itself (and on hover, with the rite's own line), so the calendar
                      does not stack heavy lead at the top of every ring.
     a jewel          a faceted jewel for a bond begun (a commitment) or someone close lost; in the full window also a
                      small round jewel for the life event that moved them most in each ring (the outcome's colour moves,
                      only when they were large). Its colour is the colour of what they chose (or of the commitment).
   Unlived years are only the cartoon: the glazier's gold lines on night glass, at every size. The year being lived fills
   from its inner edge.
   At the end of the life (S.age >= CH.life.end_age) the window is finished: the room falls to dusk and the window is lit
   from behind. The light runs through the years in order, centre outward, each ring clockwise. The panes after the last
   year lived get no glass of their own: they keep the gold tracery on night glass, and last of all the sun behind the boss
   floods them with a warm, low light (about a quarter of the lived glass's), so the light reads as a halo round the life,
   never as a ring that fell short of full (rule 2). The frame falls toward silhouette, a warm sun sits behind the boss,
   and in full size faint coloured rays fall from it.
   Symbol first, words on hover (or focus, or a tap): each pane tells its age, the game's stage of life, who they were
   that year, satisfaction and peace in words (with the number), and what happened that year in one line. Arrow keys
   walk the years.
   Motion: "full" (a slow shimmer crosses the glass, jewels glint, dust drifts in the rays), "calm" (the same, a third of
   the speed, no dust) or "off" (one still frame per change; the lit window simply lit).
   Cost: everything still is drawn once into offscreen copies, and the window itself is composed again only where
   something changed (a pane filling, a mark set, a pane being lit, the hovered pane). A change of the whole window's
   light (the dusk, the frame's lift, day again) is one compose under a fading picture of the old light. What moves every
   frame is small (the year's glow, a glint) or done by the browser's compositor (the shimmer, the dust, the bloom's and
   the rays' breath, the fade). The glass textures are made the first time a size needs them (the medallion only the
   streaks), and the years are glazed a few milliseconds' worth a frame, still frames too, so no one task runs long. */
(() => {
const CH = window.CH; if (!CH) return;
const CS = CH.COLORS, NAME = CH.NAME, clamp = CH.clamp, TAU = Math.PI * 2, TOP = -Math.PI / 2;

/* ---------- small helpers ---------- */
const mix = (p, q, t) => [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, p[2] + (q[2] - p[2]) * t];
const rgba = (c, a) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a == null ? 1 : +a.toFixed(3)})`;
const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const sstep = (a, b, v) => { const t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); };
const trunc = (s, n) => (s.length > n ? s.slice(0, n - 1).replace(/[\s,;:]+\S*$/, "") + "…" : s);
const names = (cs) => cs.map((c) => NAME[c]).join(cs.length > 2 ? ", " : " and ").replace(/, ([^,]*)$/, " and $1");
// canvas filters (saturate, brightness, blur) where the browser has them; the window still draws without them
const FILTER = typeof CanvasRenderingContext2D !== "undefined" && "filter" in CanvasRenderingContext2D.prototype;

/* ---------- the glass: five jewel tones, each in a deep, a true and a luminous sheet ----------
   The game's colours (CH.HUE) are inks on parchment; glass needs the same hues as light passes through them: White as
   amber gold, Blue as sapphire, Black as amethyst, Red as ruby, Green as emerald. They are balanced so each is as
   beautiful and as strong as the others (rule 4): in OKLCH each true sheet has a chroma of 15.5 to 17.6 (Red no longer
   the strongest), each deep one 9 to 12, each luminous one 9.4 to 11.7. Black is a deep violet, never a dark stain. */
const GLASS = {
  W: { dim: [114, 72, 2], mid: [236, 166, 30], lum: [255, 228, 148] },
  U: { dim: [14, 40, 104], mid: [44, 112, 218], lum: [150, 200, 255] },
  B: { dim: [52, 24, 88], mid: [136, 84, 200], lum: [218, 186, 250] },
  R: { dim: [96, 28, 20], mid: [210, 76, 52], lum: [255, 176, 142] },
  G: { dim: [2, 72, 36], mid: [20, 160, 84], lum: [156, 238, 176] },
};
// a sheet's colour from that year's satisfaction (0..1): a hard year deep and dense, a happy one luminous
const glassRGB = (c, sat, jit) => { const g = GLASS[c], b = clamp(0.2 + 0.8 * sat + (jit || 0));
  return b < 0.6 ? mix(g.dim, g.mid, b / 0.6) : mix(g.mid, g.lum, ((b - 0.6) / 0.4) * 0.38); };
// paler glass: the same hue taken part of the way toward a pale, nearly colourless sheet (its depth still follows the
// year's satisfaction), so it reads quieter than who they are but keeps its own colour, never a grey (see QUIET)
const TINT = (sat) => mix([150, 142, 146], [246, 240, 228], clamp(0.2 + 0.8 * sat));
const sheetRGB = (c, sat, q, jit) => { const b = glassRGB(c, sat, jit); return q > 0 ? mix(b, TINT(sat), q) : b; };
// how pale each piece is: who they are as bold jewel glass, a leading colour that is not (yet) who they are a little
// paler, the other colours with a piece of their own paler again, and the ground at the foot of a pane (streaky glass
// in the pale hue of the strongest colour left; the others run through it as veins, each as strong as its share) the
// palest. Every one keeps at least three fifths of its hue's strength (OKLCH chroma: the other colours' pieces about
// 70 to 80%, the ground 61 to 75%), so every colour shows in its own hue.
const QUIET = { own: 0, lead: 0.12, sig: 0.28, ground: 0.34 };
const NIGHT = [12, 12, 28];               // the cartoon's ground: night seen through clear, unglazed glass
const SPAND = [26, 30, 64];               // the spandrels between arches: deep night-blue background glass
const PEARL = [238, 230, 216];            // the even start: pearl glass with the five colours faint in it
const LEAD = [20, 16, 24], GOLD = [216, 180, 105], GOLD2 = [244, 223, 166], GOLD3 = [138, 106, 44];
const INITIAL = [0.2, 0.2, 0.2, 0.2, 0.2];  // the engine's starting point: every colour even
// the years before the life river's first row (early childhood) have no satisfaction or peace on record: their glass is
// painted even, clear and mid-bright, and the hover says so instead of showing numbers
const PRE_SAT = 0.62, PRE_PEACE = 0.75;
const OWN = 0.12;                         // a colour of at least 12% that year has its own piece of glass
const PIECES = 4;                         // at most four pieces of glass in a pane (before a large one is halved)
const EVENT_MIN = 4.5;                    // a life event earns a small jewel when its outcome moved the colours this much
                                          // (the sum of the outcome's colour moves, in points of share)

/* ---------- the plan: rings, a pane per year, laid out for a century ----------
   (the rings' names are the layout's only, for reading this code: the hover names each year's stage as the game does) */
const STAGES = [
  { from: 0, to: 10, name: "Childhood", w: 0.205, arch: "round", hf: 0.42 },
  { from: 10, to: 15, name: "Late childhood", w: 0.125, arch: "round", hf: 0.62 },
  { from: 15, to: 25, name: "Youth", w: 0.15, arch: "point", hf: 0.5 },
  { from: 25, to: 36, name: "Young adulthood", w: 0.15, arch: "point", hf: 0.5 },
  { from: 36, to: 60, name: "Adulthood", w: 0.18, arch: "point", hf: 0.42 },
  { from: 60, to: 100, name: "Later life", w: 0.165, arch: "point", hf: 0.5 },
];
const CENTURY = 100;
const BOSS = 0.068;                       // the boss's radius, in window radii
// N panes: a century, or every year lived past it
function plan(N) {
  const rings = STAGES.map((s, i) => Object.assign({}, s, { to: i === STAGES.length - 1 ? N : s.to, years: [] }));
  for (let y = 0; y < N; y++) rings.find((r) => y >= r.from && y < r.to).years.push(y);
  const tot = rings.reduce((s, r) => s + r.w, 0);
  let r0 = BOSS;
  const panes = [];
  rings.forEach((g, gi) => {
    g.i = gi; g.a = r0; g.b = r0 + ((1 - BOSS) * g.w) / tot; r0 = g.b; g.n = g.years.length; g.d = TAU / g.n;
    g.s = g.b - g.hf * (g.b - g.a);        // where the arches spring
    g.panes = g.years.map((y, j) => lancet(g, j, y));
    panes.push(...g.panes);
  });
  rings.forEach((g) => g.panes.forEach((p, j) => { p.spand = spandrel(g, p, g.panes[(j + 1) % g.n]); }));
  return { N, rings, panes };
}
// one pane: an annular sector whose outer edge is an arch (round petals at the centre, pointed lancets further out)
function lancet(g, j, y) {
  const phi = TOP + j * g.d, al = g.d / 2, t0 = phi - al, t1 = phi + al;
  const N = [Math.cos(phi), Math.sin(phi)], T = [-Math.sin(phi), Math.cos(phi)];
  const w = g.s * Math.sin(al), m = g.s * Math.cos(al), H = g.b - m;
  const loc = (u, v) => [N[0] * (m + v) + T[0] * u, N[1] * (m + v) + T[1] * u];
  // the right half of the arch, from the springing (u = w) to the apex (u = 0)
  const half = [], K = 12;
  if (g.arch === "point") { const uc = (w * w - H * H) / (2 * w), rho = w - uc, p1 = Math.acos(clamp(-uc / rho, -1, 1));
    for (let i = 0; i <= K; i++) { const ps = (p1 * i) / K; half.push([uc + rho * Math.cos(ps), rho * Math.sin(ps)]); } }
  else for (let i = 0; i <= K; i++) { const ps = (Math.PI / 2) * (i / K); half.push([w * Math.cos(ps), H * Math.sin(ps)]); }
  half[K] = [0, H];
  const archR = half.map(([u, v]) => loc(u, v));                     // springing right -> apex
  const archL = half.slice().reverse().map(([u, v]) => loc(-u, v));  // apex -> springing left
  const inner = arcPts(g.a, t0, t1);
  const poly = [...inner, ...arcPts(g.s, t1, t1), ...archR.slice(1), ...archL.slice(1), [g.s * Math.cos(t0), g.s * Math.sin(t0)]];
  // the plain sector (the small medallion's pane: at that size arches are only noise)
  const sec = [...arcPts(g.a, t0, t1), ...arcPts(g.b, t1, t0)];
  const P = { y, ring: g.i, j, phi, t0, t1, a: g.a, b: g.b, s: g.s, archR, archL, poly, sec };
  P.area = Math.abs(area(poly)); P.cen = centroid(poly); P.scen = centroid(sec);
  P.width = 2 * Math.hypot(P.cen[0], P.cen[1]) * Math.sin(al);
  return P;
}
function arcPts(r, t0, t1) { const n = Math.max(1, Math.ceil(Math.abs(t1 - t0) / 0.05)), o = []; for (let i = 0; i <= n; i++) { const t = t0 + ((t1 - t0) * i) / n; o.push([r * Math.cos(t), r * Math.sin(t)]); } return o; }
// the curved triangle between two neighbouring arches, under the ring's outer circle
function spandrel(g, A, B) {
  const outer = arcPts(g.b, A.phi, A.phi + g.d);
  return [...A.archR.slice().reverse(), ...outer.slice(1, -1), ...B.archL];
}
function area(p) { let s = 0; for (let i = 0, n = p.length; i < n; i++) { const a = p[i], b = p[(i + 1) % n]; s += a[0] * b[1] - b[0] * a[1]; } return s / 2; }
function centroid(p) { let x = 0, y = 0, s = 0; for (let i = 0, n = p.length; i < n; i++) { const a = p[i], b = p[(i + 1) % n], c = a[0] * b[1] - b[0] * a[1]; s += c; x += (a[0] + b[0]) * c; y += (a[1] + b[1]) * c; }
  if (Math.abs(s) < 1e-12) return p[0]; return [x / (3 * s), y / (3 * s)]; }
// keep the part of a polygon on one side of a line (n . x <= d)
function clipHalf(poly, nx, ny, d) {
  const out = [];
  for (let i = 0, n = poly.length; i < n; i++) {
    const a = poly[i], b = poly[(i + 1) % n], da = nx * a[0] + ny * a[1] - d, db = nx * b[0] + ny * b[1] - d;
    if (da <= 0) out.push(a);
    if ((da < 0 && db > 0) || (da > 0 && db < 0)) { const t = da / (da - db); out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]); }
  }
  return out;
}
/* The glazier's cuts, sized by the year's colours (see the head of the file): the leading colour across the head of the
   arch, then each colour with its own piece in the pie's order (W U B R G), then the colours left together as the
   ground at the foot. Each cut is across the pane, from its head toward its foot; the slant is the same for every
   pane of a ring, so neighbouring years' cuts continue into each other and a colour that holds for years runs round
   the ring as a band. Each piece is exactly its share of the pane. */
// the year's pieces of glass, from the head of the pane to its foot: the leading colour, the colours with a piece of
// their own (part of who they are, or at least 12% that year: the strongest first, then in the pie's order), and the
// colours left as one ground. Four pieces at most, so when a ground is needed it takes the weakest of three. The same
// for the full window and the medallion.
function partsOf(w, label) {
  const sh = (c) => w[CS.indexOf(c)], ls = CH.lettersOf(label);
  const lead = CS.reduce((a, c) => (sh(c) > sh(a) + 1e-9 ? c : a), CS[0]);
  let sig = CS.filter((c) => c !== lead && (sh(c) >= OWN || ls.includes(c))).sort((a, b) => sh(b) - sh(a)).slice(0, PIECES - 1);
  const left = () => CS.filter((c) => c !== lead && !sig.includes(c)).reduce((s, c) => s + sh(c), 0);
  if (sig.length === PIECES - 1 && left() >= 0.06) sig = sig.slice(0, PIECES - 2);
  sig.sort((a, b) => CS.indexOf(a) - CS.indexOf(b));
  const minors = CS.filter((c) => c !== lead && !sig.includes(c)).sort((a, b) => sh(b) - sh(a));
  const gsum = minors.reduce((s, c) => s + sh(c), 0);
  const parts = [{ c: lead, v: sh(lead), role: "lead" }, ...sig.map((c) => ({ c, v: sh(c), role: "sig" }))];
  // (colours too small for a ground together, under 6%, add their area to the last piece)
  if (minors.length && gsum >= 0.06) parts.push({ c: minors[0], v: gsum, role: "ground", minors: minors.map((c) => [c, sh(c)]) });
  else parts[parts.length - 1].v += gsum;
  return parts;
}
function cutPane(P, w, label) {
  const rs = CH.rng(9001 + P.ring * 977), slant = (rs() - 0.5) * 0.3;
  const parts = partsOf(w, label);
  const tot = parts.reduce((s, x) => s + x.v, 0), A = P.area, out = [];
  const Nx = Math.cos(P.phi), Ny = Math.sin(P.phi), Tx = -Ny, Ty = Nx;
  const ext = (q, ax, ay) => { let lo = Infinity, hi = -Infinity; q.forEach(([x, y]) => { const d = ax * x + ay * y; lo = Math.min(lo, d); hi = Math.max(hi, d); }); return [lo, hi]; };
  // cut off the part of q on the high side of direction t (n . x >= d) whose area is `want`
  const take = (q, t, want) => {
    const nx = Math.cos(t), ny = Math.sin(t); let [lo, hi] = ext(q, nx, ny);
    for (let i = 0; i < 28; i++) { const d = (lo + hi) / 2, ar = Math.abs(area(clipHalf(q, -nx, -ny, -d))); if (ar > want) lo = d; else hi = d; }
    const d = (lo + hi) / 2; return [clipHalf(q, -nx, -ny, -d), clipHalf(q, nx, ny, d)];
  };
  let rest = P.poly;
  parts.forEach((pt, k) => {
    if (k === parts.length - 1) { out.push(Object.assign({ poly: rest }, pt)); return; }
    const [piece, left] = take(rest, P.phi + slant, (pt.v / tot) * A);
    if (piece.length >= 3) out.push(Object.assign({ poly: piece }, pt));
    rest = left;
  });
  // a piece too large for one sheet is cut once more, along the ring's own slant (the same colour on both sides)
  const tgt = 0.02, pieces = [];
  out.forEach((q) => {
    const ar = Math.abs(area(q.poly));
    if (ar < tgt * 1.7) { pieces.push(q); return; }
    const [w0, w1] = ext(q.poly, Tx, Ty), [h0, h1] = ext(q.poly, Nx, Ny);
    const t = ((w1 - w0) > (h1 - h0) ? P.phi + Math.PI / 2 : P.phi) + slant, [A1, B1] = take(q.poly, t, ar * 0.5);
    if (A1.length < 3 || B1.length < 3) { pieces.push(q); return; }
    pieces.push(Object.assign({}, q, { poly: A1 }), Object.assign({}, q, { poly: B1 }));
  });
  return pieces;
}

/* ---------- reading the life, year by year (S.river and S.items, never ahead of S.age) ----------
   Who they were each year and the stage of life are the game's own, from that year's chapter line (S.items, tag
   "chapter": label, guild, stage), the same record the top bar, the HUD's name and the story's year heads read. The
   river row's last field is only the year's strongest colours, not who they are, so it is not read for that. */
const TURN = { breakthrough: "a breakthrough", rite: "a rite of passage", crisis: "a crisis", turn: "a turn" };
// what to tell of a year, most telling first; the year's own summary line ("A good year: ...") when nothing else
const RANK = ["death", "loss", "commitment", "breakthrough", "rite", "crisis", "turn", "choice", "decline", "move", "kin", "birth", "moment", "goal", "fortune", "trouble", "hardened", "year"];
// (the story's markers are written with the brackets U+27E6 and U+27E7; spelled as escapes, so this file reads the
// same whatever character set the page declares)
const marker = (text, k) => { const m = new RegExp("\u27e6" + k + ":([^\u27e7]*)\u27e7([^\u27e6]*)").exec(String(text || "")); return m ? { f: m[1].split("|"), body: m[2] } : null; };
const actColors = (it) => { const m = marker(it.text, "a"); return m ? CH.lettersOf(m.f[0].split(">")[0]) : []; };
const guildOf = (label) => { const g = CH.life && CH.life.guilds; const ls = CH.lettersOf(label); if (!ls.length) return "Still forming"; return (g && g[ls.join("")]) || names(ls); };
const firstSentence = (s) => { const m = /^(.+?[.!?])(\s|$)/.exec(s); return m ? m[1] : s; };
// one plain line for what happened: a choice by its moment and what they chose, a smaller moment by its first line
// and what they chose, anything else by its first sentence. What they chose is kept whole when it fits in 170
// characters: the scene is shortened first, and only then the choice, at a word.
const CAP = 170;
function lineOf(it) {
  const m = marker(it.text, "a"), act = m && m.body ? CH.plain(m.body).replace(/\s+/g, " ").trim() : "", first = firstSentence(CH.plain(it.text).replace(/\s+/g, " ").trim());
  const withAct = (head, verb) => { const room = CAP - head.length - verb.length - 1; return `${head}${verb}${act.length + 1 <= room ? act + "." : trunc(act, Math.max(24, room))}`; };
  if (it.tag === "choice" && it.title && act) return withAct(`${CH.cap(it.title)}: `, "chose to ");
  if (it.tag === "moment" && act) return withAct(`${trunc(first, 80)} `, "Chose to ");
  return trunc(first, CAP);
}
// the moments (checkpoints) and their outcomes, by title and age, from the stop log (living/90-game.js: a moment's tier
// and stakes, an outcome's colour moves): which choices were life events, and how much the outcome moved them (the sum
// of its colour moves; the largest change when the moves were not recorded). The log grows as they live, so the index
// is made again when a stop is added (CH.life.rev)
let cpIndex = null, resIndex = null, cpLife = null, cpRev = -1;
const index = () => { if (cpLife === CH.life && cpRev === CH.life.rev) return; cpLife = CH.life; cpRev = CH.life.rev; cpIndex = []; resIndex = [];
  (CH.life.stops || []).forEach((s) => { if (s.kind === "cp" && s.cp) cpIndex.push(Object.assign({ at: s.age }, s.cp)); if (s.kind === "res" && s.res) resIndex.push(Object.assign({ at: s.age }, s.res)); }); };
const near = (list, it) => list.find((c) => c.title === it.title && Math.abs((c.age ?? c.at) - it.age) < 0.6) || null;
const weight = (res) => { if (!res) return 0; if (Array.isArray(res.dw)) return res.dw.reduce((s, v) => s + Math.abs(+v || 0), 0);
  return Math.max(0, ...(res.changes || []).map((c) => +c.size || 0)); };
// what each story line gives the window, worked out once per line (the page keeps the same line objects, ITEMS, for the
// whole life). A choice's weight as a life event is looked up until its outcome is in the log.
const INFO = new WeakMap();
const info = (it) => {
  let o = INFO.get(it);
  if (!o) {
    const rk = RANK.indexOf(it.tag);
    o = { rank: rk < 0 ? 99 : rk, line: rk >= 0 ? lineOf(it) : "", cs: actColors(it), event: 0, judged: it.tag !== "choice", rev: -1 };
    if (it.tag === "breakthrough") { const v = marker(it.text, "v"); o.held = CH.plain(v ? v.body : "").trim(); }
    if (it.tag === "commitment") { const m = marker(it.text, "c"); o.bond = m ? CH.lettersOf(m.f[1]) : []; }
    INFO.set(it, o);
  }
  if (!o.judged && CH.life && o.rev !== CH.life.rev) {
    o.rev = CH.life.rev; index();
    const cp = near(cpIndex, it), res = near(resIndex, it);
    if (res) { o.judged = true; if (cp && (cp.tier === "life event" || cp.stakes >= 1)) o.event = weight(res); }
  }
  return o;
};
function readYears(S, PL) {
  const rows = S.river || [], byY = new Map(), Y = [], now = Math.floor((S.age || 0) + 1e-6);
  rows.forEach((r) => byY.set(Math.round(r[0]), r));
  const first = rows[0], items = S.items || [];
  const its = Array.from({ length: PL.N }, () => []), chap = new Map();
  items.forEach((it) => { const y = Math.floor(it.age ?? 0); if (y < 0 || y >= PL.N) return; its[y].push(it); if (it.tag === "chapter" && !chap.has(y)) chap.set(y, it); });
  // the stage a life begins in (the years before the first chapter line have none of their own)
  const st0 = { stage: (CH.life.stops[0] && CH.life.stops[0].life.stage) || "child" };
  let prevLabel = null, last = null, lastCh = null;
  for (let y = 0; y < PL.N; y++) {
    const I = { y, items: its[y], river0: first ? Math.round(first[0]) : null };
    Y.push(I);
    if (y > now) continue;                 // not lived yet: nothing to read
    let row = byY.get(y), pre = false;
    // before the river's first row the colours are the engine's even start; a lived year the river skipped keeps the
    // year before it
    if (!row && (!first || y < first[0])) { row = [y, ...INITIAL, PRE_SAT, PRE_PEACE, ""]; pre = true; }
    else if (!row && last) row = [y, ...last.slice(1)];
    if (!row) continue;
    last = row;
    // the year's chapter line (a lived year without one keeps the year before's)
    const ch = chap.get(y) || lastCh; if (ch) lastCh = ch;
    I.row = row; I.pre = pre; I.w = row.slice(1, 6); I.sat = row[6]; I.peace = row[7];
    I.label = !pre && ch ? ch.label || "" : "";
    I.who = I.label ? (ch.guild || guildOf(I.label)) : "Still forming";
    I.stage = CH.stageWord(!pre && ch ? ch : st0);
    I.even = pre || Math.max(...I.w) - Math.min(...I.w) < 0.04;
    I.sig = row.slice(1, 8).map((v) => (typeof v === "number" ? v.toFixed(3) : v)).join(",") + "," + I.label;
    const G = PL.rings[PL.panes[y].ring];
    // a turning point: who they are changed from the year before, or the year held a breakthrough, a crisis, a turn or
    // a rite (a rite on a ring's first year is the iron ring's own, told on hover with the rite's own line)
    if (prevLabel !== null && I.label !== prevLabel) I.turn = I.label ? (prevLabel ? `who they are changes: ${I.who}` : `who they are takes shape: ${I.who}`) : "who they are loosens";
    const rite = its[y].find((it) => it.tag === "rite");
    if (rite) { const m = marker(rite.text, "R");
      I.rite = { ring: y === G.from && G.i > 0, to: m ? CH.stageWord({ stage: m.f[0] }) : "", line: trunc(firstSentence(CH.plain(rite.text).replace(/\s+/g, " ").trim()), CAP) }; }
    const t = its[y].find((it) => TURN[it.tag] && !(it === rite && I.rite.ring));
    if (t && !I.turn) { I.turn = TURN[t.tag] + (t.tag === "breakthrough" ? `: ${info(t).held || "what was held back breaks through"}` : ""); I.turnRite = t === rite; }
    prevLabel = I.label;
    // a faceted jewel: a bond begun or someone close lost
    let J = null;
    its[y].forEach((it) => {
      if (it.tag === "loss") { if (!J || J.kind !== "loss") J = { size: 2, kind: "loss", it, cs: info(it).cs }; }
      else if (it.tag === "commitment" && it.what === "start" && !J) J = { size: 2, kind: "bond", it, cs: info(it).bond };
    });
    I.jewel = J;
    // the year's line: its most telling story line (the first of the most telling kind; a rite is told with its own
    // note, so it is not told twice)
    let best = null; its[y].forEach((it) => { if (it.tag !== "rite" && info(it).rank < 99 && (!best || info(it).rank < info(best).rank)) best = it; });
    I.line = best ? info(best).line : "";
  }
  // a small jewel: in each ring, the life event lived so far whose outcome moved them most, when it moved them much
  PL.rings.forEach((G) => {
    let best = null, bw = EVENT_MIN;
    G.years.forEach((y) => { const I = Y[y]; if (!I.row || I.jewel) return;
      I.items.forEach((it) => { if (it.tag !== "choice") return; const w = info(it).event; if (w >= bw) { bw = w; best = { I, it, w }; } }); });
    if (best) best.I.jewel = { size: 1, kind: "event", it: best.it, cs: info(best.it).cs, w: best.w };
  });
  Y.forEach((I) => { if (I.jewel && !I.jewel.cs.length && I.w) I.jewel.cs = [CS[I.w.indexOf(Math.max(...I.w))]]; });
  return Y;
}

/* ---------- shared textures: glass sheet streaks, opal clouds and coloured veins, each made once, when first needed
   (the medallion needs only the streaks; the full window the rest, a colour's veins when a ground first shows it) ---------- */
const make = (n, fn) => { const c = document.createElement("canvas"); c.width = c.height = n; const g = c.getContext("2d"), im = g.createImageData(n, n), d = im.data;
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const o = (y * n + x) * 4, v = fn(x / n, y / n, x, y); d[o] = v[0]; d[o + 1] = v[1]; d[o + 2] = v[2]; d[o + 3] = v[3]; }
  g.putImageData(im, 0, 0); return c; };
const MADE = {}, VEIN = {};
const TEX = {
  // streaks: a sheet of hand-made glass is thicker and thinner in long waves, with fine seed and ripple (grey 50% = flat)
  get streak() { return MADE.streak || (MADE.streak = make(320, (u, v, x, y) => { const s = CH.fbm(u * 5 + 0.7 * CH.noise(u * 3, v * 3), v * 26, 3), f = CH.noise(x * 0.45, y * 0.45);
    const g = clamp(0.5 + (s - 0.5) * 1.15 + (f - 0.5) * 0.18) * 255; return [g, g, g, 255]; })); },
  // opal: the milky clouds of an unsettled year
  get opal() { return MADE.opal || (MADE.opal = make(256, (u, v) => { const s = CH.fbm(u * 6 + 3, v * 6 + 9, 4); const a = sstep(0.42, 0.72, s) * 255; return [255, 255, 255, a]; })); },
};
const textures = () => TEX;
// veins: the quiet colours drawn through the ground's sheet, as in streaky glass (each colour its own pattern)
const veinOf = (c) => VEIN[c] || (VEIN[c] = ((i) => { const col = mix(mix(GLASS[c].dim, GLASS[c].mid, 0.62), [110, 104, 100], 0.14);
  return make(192, (u, v) => { const s = CH.fbm(u * 3.4 + 0.9 * CH.noise(u * 2 + i * 5, v * 2 + i * 3), v * 12 + i * 7.3, 3); return [col[0], col[1], col[2], sstep(0.4, 0.6, s) * 255]; }); })(CS.indexOf(c)));

/* ---------- the instance: mount(host, { size: "mini" | "full", hold }) ----------
   hold() true keeps the end's light waiting (the page's chapter plate is up). The instance: update(S); skip() (the end's
   light at once at its end); lighting() (true while the end's light runs); destroy(). Its root's data-light says where
   the light is: "day" while they live, "lighting", then "lit". */
function mount(host, opts) {
  opts = opts || {};
  const full = opts.size !== "mini";
  const root = document.createElement("div");
  root.className = "chw " + (full ? "chw-full" : "chw-mini");
  host.appendChild(root);
  const cv = CH.canvas(root, "chw-glass");
  // the rays and the halo fall outside the window's square, into the room in front of it, on their own canvases (full
  // size only), added with screen
  let rv = null, mv = null;
  if (full) { rv = document.createElement("canvas"); rv.className = "chw-rays"; rv.setAttribute("aria-hidden", "true"); root.appendChild(rv);
    // the dust in the light: a few specks the compositor moves (CSS), so nothing is drawn for them frame by frame
    mv = document.createElement("div"); mv.className = "chw-motes"; mv.setAttribute("aria-hidden", "true");
    const r = CH.rng(4242);
    mv.innerHTML = Array.from({ length: 26 }, () => { const d = 15 + r() * 20, s = (1.2 + r() * 1.6).toFixed(1);
      return `<b style="left:${(r() * 100).toFixed(1)}%;opacity:${(0.3 + r() * 0.4).toFixed(2)}"><i style="--s:${s}px;animation-duration:${d.toFixed(1)}s;animation-delay:${(-r() * d).toFixed(1)}s"></i></b>`; }).join("");
    root.appendChild(mv); }
  cv.tabIndex = 0; cv.setAttribute("role", "img");
  // the fade: a picture of the window in its old light, laid over it while the new light comes in
  const dk = document.createElement("canvas"); dk.className = "chw-fade"; dk.setAttribute("aria-hidden", "true"); cv.after(dk);
  // layers the compositor moves: the shimmer (soft light), the bloom (screen), and the frame's moving light (screen)
  const shim = document.createElement("div"); shim.className = "chw-shim"; shim.setAttribute("aria-hidden", "true"); shim.innerHTML = "<i></i>"; root.appendChild(shim);
  const bl = document.createElement("canvas"); bl.className = "chw-bloom"; bl.setAttribute("aria-hidden", "true"); root.appendChild(bl);
  const fx = CH.canvas(root, "chw-fx"); fx.setAttribute("aria-hidden", "true");
  const live = document.createElement("div"); live.className = "chw-sr"; live.setAttribute("aria-live", "polite"); root.appendChild(live);

  const st = {
    S: null, PL: null, Y: [], key: "", age: 0, target: 0, first: true, lit: 0, sweep: 0, atEnd: false, qIn: 0,
    litP: 0, litC: 0, setC: 0, xf: 0, xfDur: 1, dkOp: -1, synth: false, painted: new Map(), spand: new Set(), cuts: new Map(), hover: -1, focus: -1, X: null, caches: null,
    marksFor: "", t: 0, motes: null, RL: null, rays: "", jewelYs: [], all: true, rects: [], litA: null, bloMax: 0,
    fxRects: [], bloomFor: "", bloomOp: -1, raysOp: -1, motesOp: -1, motesOn: false, touch: false, light: "",
  };

  /* the window's place in its canvas: centred, the rim inside the square, a little room for its shadow */
  function geom() {
    const W = cv._w, H = cv._h, side = Math.min(W, H), k = cv._k || 1;
    const R = full ? (side * 0.485) / 1.075 : (side * 0.48) / 1.22, Rr = full ? side * 0.485 : R * 1.05;
    // 2: every craft detail (the full window); 1: a medallion; 0: a tiny one (the HUD's 96 and 64)
    const detail = full && R > 110 ? 2 : R > 52 ? 1 : 0;
    const cx = W / 2, cy = H / 2, size = Math.ceil(side / 2 + 2) * 2, x0 = cx - size / 2, y0 = cy - size / 2;
    const amp = detail === 2 ? 0.0032 : 0.0018;
    // a slight irregularity in every line the glazier drew, the same for the lead and the glass it holds
    // (each point is worked out once per size and remembered)
    const memo = new WeakMap();
    const px = (p) => { let q = memo.get(p); if (q) return q; const x = p[0], y = p[1], dx = (CH.noise(x * 9 + 31, y * 9 + 7) - 0.5) * amp, dy = (CH.noise(x * 9 + 77, y * 9 + 51) - 0.5) * amp;
      q = [cx + (x + dx) * R, cy + (y + dy) * R]; memo.set(p, q); return q; };
    return { W, H, k, R, Rr, cx, cy, size, x0, y0, detail, px };
  }
  // an offscreen copy of the window's square (or, with whole, of the canvas), drawn in the canvas's own CSS pixels
  const mkCache = (X, whole) => { const c = document.createElement("canvas"), w = whole ? X.W : X.size, h = whole ? X.H : X.size;
    c.width = Math.max(1, Math.round(w * X.k)); c.height = Math.max(1, Math.round(h * X.k)); const g = c.getContext("2d");
    if (whole) g.setTransform(X.k, 0, 0, X.k, 0, 0); else g.setTransform(X.k, 0, 0, X.k, -X.x0 * X.k, -X.y0 * X.k); return { c, g }; };
  const put = (g, X, C) => g.drawImage(C.c, X.x0, X.y0, X.size, X.size);
  // a polygon's bounding box in CSS pixels, so a wash or a recompose touches only its own pixels
  const BOX = new WeakMap();
  const boxOf = (X, poly, m) => { let b = BOX.get(poly); if (!(b && b.X === X)) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    poly.forEach((p) => { const q = X.px(p); x0 = Math.min(x0, q[0]); y0 = Math.min(y0, q[1]); x1 = Math.max(x1, q[0]); y1 = Math.max(y1, q[1]); });
    b = { X, r: [x0, y0, x1 - x0, y1 - y0] }; BOX.set(poly, b); } m = m == null ? 2 : m; return [b.r[0] - m, b.r[1] - m, b.r[2] + 2 * m, b.r[3] + 2 * m]; };
  const path = (g, X, poly) => { poly.forEach((p, i) => { const q = X.px(p); if (i) g.lineTo(q[0], q[1]); else g.moveTo(q[0], q[1]); }); g.closePath(); };
  const shapeOf = (X, P) => (X.detail === 2 ? P.poly : P.sec);
  // the box a pane's recompose must cover: its sector, its heavier lead and jewel, its gold outline
  const paneBox = (X, P) => boxOf(X, P.sec, Math.max(4, X.R * 0.03));

  function rebuild() {
    // a hidden host (no size yet, such as the end screen before the end) waits for its size
    if (Math.min(cv._w || 0, cv._h || 0) < 16) { st.X = null; st.caches = null; st.painted.clear(); st.spand.clear(); st.marksFor = ""; return; }
    st.X = geom(); const X = st.X;
    st.caches = { base: mkCache(X, true), lived: mkCache(X), lead: mkCache(X), frame: mkCache(X), marks: mkCache(X), lit: null, litSmall: null };
    st.painted.clear(); st.spand.clear(); st.marksFor = ""; st.rays = ""; st.bloomFor = ""; st.litA = null; st.xf = 0; setOp(dk, "dkOp", 0);
    root.classList.toggle("chw-d0", X.detail === 0);
    // the shimmer covers the glass; the bloom the window's square
    Object.assign(shim.style, { left: X.cx - X.R + "px", top: X.cy - X.R + "px", width: 2 * X.R + "px", height: 2 * X.R + "px" });
    Object.assign(bl.style, { left: X.x0 + "px", top: X.y0 + "px", width: X.size + "px", height: X.size + "px" });
    const bw = Math.max(16, Math.round(X.size * X.k * 0.09)); bl.width = bw; bl.height = bw;
    if (st.PL) { paintBase(); paintFrame(); }
    st.RL = fitRays();
    st.all = true;
  }

  /* ---------- the cartoon: night glass with the glazier's gold lines, at every size ---------- */
  function paintBase() {
    const X = st.X, g = st.caches.base.g, T = textures(), D = X.detail, R = X.R;
    // a soft shadow under the frame, so the window sits on its page as an object (drawn once, here)
    g.save(); g.beginPath(); g.arc(X.cx, X.cy + R * 0.02, D === 2 ? X.Rr * 1.004 : R, 0, TAU);
    g.shadowColor = D === 2 ? "rgba(0,0,0,0.55)" : "rgba(60,40,10,0.35)"; g.shadowBlur = R * (D === 2 ? 0.06 : 0.1); g.shadowOffsetY = R * 0.02; g.fillStyle = D === 2 ? "rgba(8,6,12,1)" : rgba(GOLD3); g.fill(); g.restore();
    g.save(); g.beginPath(); g.arc(X.cx, X.cy, R * 1.003, 0, TAU); g.clip();
    g.fillStyle = rgba(NIGHT); g.fillRect(X.x0, X.y0, X.size, X.size);
    if (D === 2) st.PL.panes.forEach((P) => { const r = CH.rng(77 + P.y * 7), t = (r() - 0.5) * 0.5;
      g.beginPath(); path(g, X, P.poly); g.fillStyle = rgba(mix(NIGHT, t > 0 ? [30, 30, 62] : [6, 6, 16], Math.abs(t))); g.fill(); });
    g.globalCompositeOperation = "overlay"; g.globalAlpha = D === 2 ? 0.4 : 0.3; g.drawImage(T.streak, X.x0, X.y0, X.size, X.size);
    g.globalCompositeOperation = "screen"; g.globalAlpha = 1;
    // the room's light catching the glass from the upper left (a little stronger in the medallion, which sits on the
    // HUD's lit parchment)
    const sh = g.createLinearGradient(X.cx - R, X.cy - R, X.cx + R, X.cy + R);
    sh.addColorStop(0, `rgba(110,104,170,${D === 2 ? 0.14 : 0.2})`); sh.addColorStop(0.45, "rgba(50,46,90,0.03)"); sh.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = sh; g.fillRect(X.x0, X.y0, X.size, X.size);
    if (D <= 1) {
      // the crystal at the heart is lit from birth: its warm light spreads into the night glass round it (the panes,
      // as they are glazed, lie over it)
      const rb = BOSS * R, hg = g.createRadialGradient(X.cx, X.cy, rb * 0.6, X.cx, X.cy, rb * 4.2);
      hg.addColorStop(0, "rgba(255,214,150,0.6)"); hg.addColorStop(0.35, "rgba(255,200,130,0.22)"); hg.addColorStop(1, "rgba(255,190,120,0)");
      g.fillStyle = hg; g.fillRect(X.x0, X.y0, X.size, X.size);
    }
    g.globalCompositeOperation = "source-over";
    // the cartoon: every pane's outline in fine gold, as the glazier draws it before the glass is cut (in the medallion,
    // the rings and each pane's sides)
    g.lineJoin = "round";
    if (D === 2) { g.strokeStyle = "rgba(216,180,105,0.26)"; g.lineWidth = Math.max(0.6, R * 0.0024); st.PL.panes.forEach((P) => { g.beginPath(); path(g, X, P.poly); g.stroke(); }); }
    else {
      g.strokeStyle = "rgba(216,180,105,0.3)"; g.lineWidth = Math.max(0.45, R * 0.009);
      st.PL.rings.forEach((G) => G.panes.forEach((P) => { const c = Math.cos(P.t1), s = Math.sin(P.t1);
        g.beginPath(); g.moveTo(X.cx + c * G.a * R, X.cy + s * G.a * R); g.lineTo(X.cx + c * G.b * R, X.cy + s * G.b * R); g.stroke(); }));
      g.strokeStyle = "rgba(226,190,112,0.55)"; g.lineWidth = Math.max(0.6, R * 0.014);
      st.PL.rings.forEach((G) => { if (G.i) { g.beginPath(); g.arc(X.cx, X.cy, G.a * R, 0, TAU); g.stroke(); } });
    }
    g.restore();
  }

  /* ---------- one year's glass, painted into the lived window once (S.river's row for that year) ---------- */
  function paintPane(P, I) {
    const X = st.X, g = st.caches.lived.g, D = X.detail, shape = shapeOf(X, P);
    // a year painted again (its row came late) is first cleared
    if (st.painted.has(P.y)) { g.save(); g.globalCompositeOperation = "destination-out"; g.beginPath(); path(g, X, shape); g.fill(); g.restore(); st.spand.delete(P.y); }
    if (D <= 1) paintFlat(P, I); else paintFull(P, I);
    paintLead(P);
    st.painted.set(P.y, I.sig);
  }
  // the small medallion: the same pieces as the full window (partsOf), laid as bands across the pane from its outer
  // edge (the leading colour) to its inner one (the ground), each band as large as its share of the pane's area. As
  // the shares hold from year to year, the bands run round each ring like the river's; no colour is lost at this size.
  function paintFlat(P, I) {
    const X = st.X, g = st.caches.lived.g, R = X.R, sat = clamp(I.sat), ls = CH.lettersOf(I.label);
    const sector = (r0, r1, col) => { g.beginPath(); g.arc(X.cx, X.cy, r1 * R, P.t0, P.t1); g.arc(X.cx, X.cy, r0 * R, P.t1, P.t0, true); g.closePath(); g.fillStyle = rgba(col); g.fill(); };
    if (I.even) sector(P.a, P.b, mix([200, 192, 180], PEARL, clamp(0.3 + 0.7 * sat)));
    else {
      const parts = partsOf(I.w, I.label), tot = parts.reduce((s, x) => s + x.v, 0), a2 = P.a * P.a, b2 = P.b * P.b;
      let acc = 0, r1 = P.b;
      parts.forEach((q, k) => { acc += q.v / tot; const r0 = k === parts.length - 1 ? P.a : Math.sqrt(b2 - (b2 - a2) * acc);
        const quiet = QUIET[ls.includes(q.c) ? "own" : q.role];
        // (each band a hair over its edge, so no seam of night shows between two bands)
        sector(Math.max(P.a, r0 - 0.002), r1, sheetRGB(q.c, sat, quiet)); r1 = r0; });
    }
    // light through the thickness, brightest in the middle of the pane
    const c = X.px(P.scen), rad = Math.max(P.width, P.b - P.a) * R * 0.8, lg = g.createRadialGradient(c[0], c[1], 0, c[0], c[1], rad);
    lg.addColorStop(0, `rgba(255,248,226,${0.1 + 0.12 * sat})`); lg.addColorStop(1, "rgba(255,248,226,0)");
    g.save(); g.beginPath(); path(g, X, P.sec); g.clip(); g.globalCompositeOperation = "screen"; g.fillStyle = lg; const bx = boxOf(X, P.sec); g.fillRect(bx[0], bx[1], bx[2], bx[3]); g.restore();
  }
  // the full window: the glazier's pieces, each a sheet with its own streaks; clarity and seeds from peace
  function paintFull(P, I) {
    const X = st.X, g = st.caches.lived.g, T = textures(), R = X.R, r = CH.rng(313 + P.y * 17);
    const haze = clamp((0.7 - I.peace) / 0.35), sat = clamp(I.sat), ls = CH.lettersOf(I.label);
    const bx = boxOf(X, P.poly), c = X.px(P.cen), ext = Math.max(P.width, P.b - P.a) * R;
    g.save(); g.beginPath(); path(g, X, P.poly); g.clip();
    let pieces = [];
    if (I.even) {
      // pearl: the five colours faint in milky glass, turning as the light moves across it
      g.fillStyle = rgba(mix([196, 188, 176], PEARL, clamp(0.3 + 0.7 * sat))); g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      if (g.createConicGradient) { const cg = g.createConicGradient(P.phi + r() * TAU, c[0], c[1]);
        CS.concat(CS[0]).forEach((k, i) => cg.addColorStop(i / 5, rgba(GLASS[k].lum))); g.globalAlpha = 0.26; g.fillStyle = cg; g.fillRect(bx[0], bx[1], bx[2], bx[3]); g.globalAlpha = 1; }
    } else {
      const key = P.y + "|" + I.sig;
      pieces = st.cuts.get(key); if (!pieces) { pieces = cutPane(P, I.w, I.label); st.cuts.set(key, pieces); }
      // who they are as bold jewel glass; the other colours paler glass of their own hue (the ground the palest)
      pieces.forEach((q) => {
        const quiet = QUIET[ls.includes(q.c) ? "own" : q.role], jit = (r() - 0.5) * 0.08;
        g.beginPath(); path(g, X, q.poly); g.fillStyle = rgba(sheetRGB(q.c, sat, quiet, jit)); g.fill();
        if (q.role === "ground") veins(g, X, P, q, r);
      });
    }
    // the sheet's streaks, laid along the pane at a seeded slant
    g.save(); g.translate(c[0], c[1]); g.rotate(P.phi + Math.PI / 2 + (r() - 0.5) * 0.7);
    g.globalCompositeOperation = "overlay"; g.globalAlpha = 0.36 + 0.24 * haze; const sz = ext * 2.2;
    g.drawImage(T.streak, r() * 120, r() * 120, 200, 200, -sz / 2, -sz / 2, sz, sz);
    g.restore();
    // light through the thickness: brighter in the middle of the pane, darker where the glass meets the lead
    const lg = g.createRadialGradient(c[0], c[1], 0, c[0], c[1], ext * 0.75);
    lg.addColorStop(0, `rgba(255,248,226,${0.06 + 0.1 * sat})`); lg.addColorStop(0.6, "rgba(255,248,226,0.02)"); lg.addColorStop(1, "rgba(0,0,0,0)");
    g.globalCompositeOperation = "screen"; g.fillStyle = lg; g.fillRect(bx[0], bx[1], bx[2], bx[3]);
    g.globalCompositeOperation = "source-over";
    g.beginPath(); path(g, X, P.poly); g.lineWidth = Math.max(1, R * 0.024); g.strokeStyle = "rgba(10,6,14,0.3)"; g.stroke();
    // clarity from peace: a troubled year is greyer, milky and full of seeds; a peaceful one clear, with a glint
    if (haze > 0.02) {
      g.globalCompositeOperation = "saturation"; g.fillStyle = `rgba(128,128,128,${0.3 * haze})`; g.fillRect(bx[0], bx[1], bx[2], bx[3]);
      // (the milk is the pane's own colour made pale, so a troubled year stays its colour, only clouded)
      const milk = opalOf(pieces.length ? pieces[0].c : "W", sat);
      g.globalCompositeOperation = "screen"; g.globalAlpha = 0.5 * haze; const so = ext * 2;
      g.drawImage(milk, r() * 100, r() * 100, 150, 150, c[0] - so / 2, c[1] - so / 2, so, so);
      g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    }
    const nb = 2 + Math.round(14 * haze);
    for (let i = 0; i < nb; i++) {
      const u = (r() - 0.5) * 0.8, v = 0.12 + r() * 0.76, rr = P.a + (P.s - P.a) * v, t = P.phi + u * (P.t1 - P.t0);
      const q = X.px([rr * Math.cos(t), rr * Math.sin(t)]), br = R * (0.0022 + r() * 0.0036);
      g.beginPath(); g.arc(q[0], q[1], br, 0, TAU); g.fillStyle = "rgba(255,255,255,0.10)"; g.fill();
      g.lineWidth = Math.max(0.5, br * 0.35); g.strokeStyle = "rgba(20,10,20,0.26)"; g.stroke();
      g.beginPath(); g.arc(q[0] - br * 0.35, q[1] - br * 0.35, br * 0.32, 0, TAU); g.fillStyle = "rgba(255,255,255,0.5)"; g.fill();
    }
    if (I.peace >= 0.65) {
      // a clear year: one crisp diagonal glint across the glass, and a fainter one beside it
      const W = P.width * R, Hh = (P.b - P.a) * R;
      g.save(); g.translate(c[0], c[1]); g.rotate(P.phi + Math.PI / 2); g.globalCompositeOperation = "screen"; g.lineCap = "round";
      const o = (r() - 0.5) * W * 0.2;
      g.strokeStyle = "rgba(255,255,255,0.18)"; g.lineWidth = 1; g.beginPath(); g.moveTo(-W * 0.3 + o, Hh * 0.32); g.lineTo(W * 0.24 + o, -Hh * 0.34); g.stroke();
      g.strokeStyle = "rgba(255,255,255,0.09)"; g.lineWidth = 0.7; g.beginPath(); g.moveTo(-W * 0.18 + o, Hh * 0.36); g.lineTo(W * 0.32 + o, -Hh * 0.22); g.stroke();
      g.restore();
    }
    // the cuts between the pieces: thin lead, lighter than the pane's own
    if (pieces.length > 1) { g.lineJoin = "round"; g.strokeStyle = rgba(LEAD, 0.92); g.lineWidth = Math.max(0.6, R * 0.0048);
      pieces.forEach((q) => { g.beginPath(); path(g, X, q.poly); g.stroke(); }); }
    g.restore();
    // the spandrels on either side, once their pane is lived
    const G = st.PL.rings[P.ring];
    paintSpandrel(P); paintSpandrel(G.panes[(P.j - 1 + G.n) % G.n]);
  }
  // milky clouds tinted with a colour (made once per colour and size of brightness)
  const OPAL = new Map();
  function opalOf(c, sat) {
    const k = c + Math.round(sat * 4); let o = OPAL.get(k); if (o) return o;
    const T = textures(), col = mix(glassRGB(c, sat), [250, 246, 240], 0.55);
    o = document.createElement("canvas"); o.width = o.height = T.opal.width; const g = o.getContext("2d");
    g.drawImage(T.opal, 0, 0); g.globalCompositeOperation = "source-in"; g.fillStyle = rgba(col); g.fillRect(0, 0, o.width, o.height);
    OPAL.set(k, o); return o;
  }
  // the quiet colours drawn through the ground piece as veins, each as strong as its share among them
  function veins(g, X, P, q, r) {
    const c = X.px(P.cen), sz = Math.max(P.width, P.b - P.a) * X.R * 2.2, tot = q.minors.reduce((s, x) => s + x[1], 0);
    g.save(); g.beginPath(); path(g, X, q.poly); g.clip(); g.translate(c[0], c[1]); g.rotate(P.phi + Math.PI / 2 + (r() - 0.5) * 0.6);
    q.minors.forEach(([m, v]) => { g.globalAlpha = 0.92 * clamp((v / tot) * 2); g.drawImage(veinOf(m), r() * 80, r() * 80, 110, 110, -sz / 2, -sz / 2, sz, sz); });
    g.restore();
  }
  // the spandrel after a pane: deep night-blue glass with a fine gold-ink tendril
  function paintSpandrel(P) {
    if (st.spand.has(P.y)) return; st.spand.add(P.y);
    const X = st.X, g = st.caches.lived.g, T = textures(), r = CH.rng(555 + P.y * 3);
    g.save(); g.beginPath(); path(g, X, P.spand); g.clip();
    const bx = boxOf(X, P.spand);
    g.fillStyle = rgba(mix(SPAND, [14, 16, 40], r() * 0.5)); g.fillRect(bx[0], bx[1], bx[2], bx[3]);
    g.globalCompositeOperation = "overlay"; g.globalAlpha = 0.35; const c = X.px(centroid(P.spand)), sz = X.R * 0.3;
    g.drawImage(T.streak, r() * 100, r() * 100, 120, 120, c[0] - sz / 2, c[1] - sz / 2, sz, sz);
    g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    const sp = centroid(P.spand), dir = Math.atan2(sp[1], sp[0]), q = X.px(sp), L = X.R * 0.02;
    g.strokeStyle = "rgba(216,180,105,0.45)"; g.lineWidth = Math.max(0.6, X.R * 0.0026); g.lineCap = "round";
    g.beginPath(); g.moveTo(q[0] - Math.cos(dir) * L * 1.4, q[1] - Math.sin(dir) * L * 1.4);
    g.quadraticCurveTo(q[0] + Math.cos(dir + 1.4) * L, q[1] + Math.sin(dir + 1.4) * L, q[0] + Math.cos(dir) * L * 0.6, q[1] + Math.sin(dir) * L * 0.6); g.stroke();
    g.beginPath(); g.arc(q[0] + Math.cos(dir) * L * 0.6, q[1] + Math.sin(dir) * L * 0.6, L * 0.32, 0, TAU); g.stroke();
    g.restore();
  }

  /* ---------- the lead, the frame, the boss and the marks ---------- */
  function leadLine(g, X, pts, w, closed) {
    g.beginPath(); pts.forEach((p, i) => { const q = X.px(p); if (i) g.lineTo(q[0], q[1]); else g.moveTo(q[0], q[1]); }); if (closed) g.closePath();
    g.lineWidth = w + Math.max(X.detail ? 0.6 : 0.35, w * 0.35); g.strokeStyle = "rgba(4,2,8,0.55)"; g.stroke();   // the putty line, crisp
    g.lineWidth = w; g.strokeStyle = rgba(LEAD); g.stroke();                                             // the came
    if (X.detail >= 1) { g.save(); g.translate(-w * 0.18, -w * 0.22); g.lineWidth = Math.max(0.5, w * 0.3); g.strokeStyle = "rgba(196,184,214,0.16)"; g.stroke(); g.restore(); }
  }
  const leadW = (X) => { const D = X.detail, R = X.R; return { wL: Math.max(0.55, R * (D === 2 ? 0.0085 : 0.011)), wBar: Math.max(0.9, R * (D === 2 ? 0.016 : D === 1 ? 0.022 : 0.03)) }; };
  // a lived pane's own lead (the lead comes with the glass): its side toward the next year, its arch, and the side
  // toward the year before when that is the ring's first pane
  function paintLead(P) {
    const X = st.X, g = st.caches.lead.g, G = st.PL.rings[P.ring], D = X.detail, { wL } = leadW(X);
    g.lineJoin = "round"; g.lineCap = "round";
    const top = D === 2 ? P.s : P.b;
    const side = (t) => { const pts = [[P.a * Math.cos(t), P.a * Math.sin(t)], [top * Math.cos(t), top * Math.sin(t)]];
      if (D === 2) return leadLine(g, X, pts, wL);
      g.beginPath(); path(g, X, pts); g.lineWidth = wL; g.strokeStyle = "rgba(52,38,30,0.78)"; g.stroke(); };
    if (P.j < G.n - 1 || G.n === 1) side(P.t1);
    if (P.j === 0) side(P.t0);
    if (D === 2) leadLine(g, X, [...P.archR.slice().reverse(), ...P.archL.slice(1)], wL);
    else { const { wBar } = leadW(X); g.lineCap = "butt"; g.strokeStyle = "rgba(58,42,28,0.82)"; g.lineWidth = wBar * 0.8;
      [P.a, P.b].forEach((r, i) => { if (!i && !P.ring) return; g.beginPath(); g.arc(X.cx, X.cy, r * X.R, P.t0 - 0.002, P.t1 + 0.002); g.stroke(); }); }
  }
  // the window's frame, drawn once per size: the iron rings between the rings of years, the rim and the boss
  function paintFrame() {
    const X = st.X, g = st.caches.frame.g, { wBar } = leadW(X);
    g.lineJoin = "round"; g.lineCap = "round";
    if (X.detail === 2) { st.PL.rings.forEach((G) => { if (G.i === 0) return; ring(g, X, G.a, wBar); }); rim(g, X); } else rimSmall(g, X);
    boss(g, X);
  }
  function ring(g, X, r, w) {
    const R = X.R, pts = arcPts(r, 0, TAU);
    if (X.detail === 2) { leadLine(g, X, pts, w, true);
      g.beginPath(); pts.forEach((p, i) => { const q = X.px([p[0] * (1 - w * 0.22 / (r * R)), p[1] * (1 - w * 0.22 / (r * R))]); if (i) g.lineTo(q[0], q[1]); else g.moveTo(q[0], q[1]); });
      g.closePath(); g.lineWidth = Math.max(0.5, w * 0.16); g.strokeStyle = "rgba(216,180,105,0.28)"; g.stroke(); }
    else { g.beginPath(); g.arc(X.cx, X.cy, r * R, 0, TAU); g.lineWidth = w; g.strokeStyle = "rgba(58,44,30,0.92)"; g.stroke(); }
  }
  function rim(g, X) {
    const { cx, cy, R, Rr } = X;
    g.save();
    // the frame: gilt bronze, lit from the upper left
    const gr = g.createLinearGradient(cx - Rr, cy - Rr, cx + Rr, cy + Rr);
    gr.addColorStop(0, rgba(GOLD2)); gr.addColorStop(0.35, rgba(GOLD)); gr.addColorStop(0.7, rgba(GOLD3)); gr.addColorStop(1, rgba([74, 54, 22]));
    g.beginPath(); g.arc(cx, cy, Rr, 0, TAU); g.arc(cx, cy, R * 0.996, 0, TAU, true); g.fillStyle = gr; g.fill("evenodd");
    // an engraved band: fine hatching between two fillets, as the game's engraved plates
    const r1 = R + (Rr - R) * 0.3, r2 = R + (Rr - R) * 0.78;
    g.beginPath(); g.arc(cx, cy, r2, 0, TAU); g.arc(cx, cy, r1, 0, TAU, true); g.fillStyle = "rgba(60,40,14,0.55)"; g.fill("evenodd");
    g.strokeStyle = "rgba(244,223,166,0.32)"; g.lineWidth = 0.6; g.beginPath();
    for (let i = 0; i < 360; i++) { const t = (i / 360) * TAU, c = Math.cos(t), s = Math.sin(t); g.moveTo(cx + c * (r1 + 1), cy + s * (r1 + 1)); g.lineTo(cx + c * (r2 - 1), cy + s * (r2 - 1)); }
    g.stroke();
    [r1, r2].forEach((r) => { g.beginPath(); g.arc(cx, cy, r, 0, TAU); g.lineWidth = 1; g.strokeStyle = "rgba(40,26,8,0.75)"; g.stroke(); });
    // studs on the band, one at every other lead of the outer ring
    const G = st.PL.rings[st.PL.rings.length - 1], rs = (r1 + r2) / 2, sr = (r2 - r1) * 0.36;
    G.panes.forEach((P, j) => { if (j % 2) return; const x = cx + Math.cos(P.t0) * rs, y = cy + Math.sin(P.t0) * rs, sg = g.createRadialGradient(x - sr * 0.4, y - sr * 0.4, 0, x, y, sr);
      sg.addColorStop(0, rgba(GOLD2)); sg.addColorStop(0.6, rgba(GOLD)); sg.addColorStop(1, rgba(GOLD3)); g.beginPath(); g.arc(x, y, sr, 0, TAU); g.fillStyle = sg; g.fill();
      g.lineWidth = 0.6; g.strokeStyle = "rgba(40,26,8,0.8)"; g.stroke(); });
    // the edges: a dark line at the glass and outside, a bright fillet on the frame's top edge
    g.lineWidth = Math.max(1, R * 0.012); g.strokeStyle = rgba(LEAD); g.beginPath(); g.arc(cx, cy, R, 0, TAU); g.stroke();
    g.lineWidth = Math.max(0.6, R * 0.004); g.strokeStyle = "rgba(20,12,4,0.85)"; g.beginPath(); g.arc(cx, cy, Rr - g.lineWidth / 2, 0, TAU); g.stroke();
    g.lineWidth = Math.max(0.5, R * 0.003); g.strokeStyle = "rgba(255,240,200,0.5)"; g.beginPath(); g.arc(cx, cy, Rr - Math.max(1, R * 0.008), Math.PI * 0.95, Math.PI * 1.65); g.stroke();
    g.restore();
  }
  // the small medallion's frame: an octofoil of gilt (eight round lobes about a thin band), so on the HUD it reads as a
  // rosette of glass, never as a second dark disc under the star
  function rimSmall(g, X) {
    const { cx, cy, R, Rr } = X, n = 8, rc = R * 0.86, rl = R * 0.36;
    const lobe = (i) => { const t = TOP + (i * TAU) / n; return [cx + Math.cos(t) * rc, cy + Math.sin(t) * rc, t]; };
    const shapes = () => { g.beginPath(); g.arc(cx, cy, Rr, 0, TAU); for (let i = 0; i < n; i++) { const [x, y] = lobe(i); g.moveTo(x + rl, y); g.arc(x, y, rl, 0, TAU); } };
    const gr = g.createLinearGradient(cx - R * 1.2, cy - R * 1.2, cx + R * 1.2, cy + R * 1.2);
    gr.addColorStop(0, rgba(GOLD2)); gr.addColorStop(0.45, rgba(GOLD)); gr.addColorStop(1, rgba(GOLD3));
    g.save(); g.beginPath(); g.rect(X.x0, X.y0, X.size, X.size); g.arc(cx, cy, R * 0.996, 0, TAU); g.clip("evenodd");
    shapes(); g.lineWidth = Math.max(1, R * 0.045); g.lineJoin = "round"; g.strokeStyle = "rgba(70,46,12,0.9)"; g.stroke();
    shapes(); g.fillStyle = gr; g.fill("nonzero");
    // an engraved fillet following each lobe, and a bright edge where the light from the upper left catches it
    for (let i = 0; i < n; i++) { const [x, y, t] = lobe(i);
      g.beginPath(); g.arc(x, y, rl * 0.7, t - 1.25, t + 1.25); g.lineWidth = Math.max(0.5, R * 0.016); g.strokeStyle = "rgba(110,76,22,0.55)"; g.stroke();
      const lt = 0.5 + 0.5 * Math.cos(t + Math.PI * 0.75); if (lt > 0.4) { g.beginPath(); g.arc(x, y, rl - R * 0.02, t - 0.9, t + 0.9); g.lineWidth = Math.max(0.5, R * 0.014); g.strokeStyle = `rgba(255,246,214,${(0.7 * lt).toFixed(2)})`; g.stroke(); } }
    g.lineWidth = Math.max(0.6, R * 0.02); g.strokeStyle = "rgba(48,32,10,0.85)"; g.beginPath(); g.arc(cx, cy, R, 0, TAU); g.stroke();
    g.restore();
  }
  // the boss at the centre: the birth, a clear crystal with the five colours faint in its facets
  function boss(g, X) {
    const { cx, cy, R, detail: D } = X, rb = BOSS * R;
    g.save();
    // in the medallion the crystal is lit from birth: a warm glow round it, over the first panes as they come
    if (D <= 1) { const hg = g.createRadialGradient(cx, cy, rb * 0.8, cx, cy, rb * 2.4);
      hg.addColorStop(0, "rgba(255,214,150,0.6)"); hg.addColorStop(1, "rgba(255,214,150,0)");
      g.globalCompositeOperation = "screen"; g.fillStyle = hg; g.beginPath(); g.arc(cx, cy, rb * 2.4, 0, TAU); g.fill(); g.globalCompositeOperation = "source-over"; }
    const gr = g.createRadialGradient(cx - rb * 0.3, cy - rb * 0.3, 0, cx, cy, rb);
    gr.addColorStop(0, rgba(GOLD2)); gr.addColorStop(0.7, rgba(GOLD)); gr.addColorStop(1, rgba(GOLD3));
    g.beginPath(); g.arc(cx, cy, rb, 0, TAU); g.fillStyle = gr; g.fill(); g.lineWidth = Math.max(0.6, R * 0.006); g.strokeStyle = rgba(LEAD); g.stroke();
    const rc = rb * 0.66;
    if (D >= 1) {
      for (let i = 0; i < 5; i++) { const a0 = TOP + (i - 0.5) * (TAU / 5), a1 = a0 + TAU / 5, c = CS[i];
        g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, rc, a0, a1); g.closePath(); g.fillStyle = rgba(mix(GLASS[c].lum, [255, 252, 244], 0.55)); g.fill(); }
      g.beginPath(); g.arc(cx, cy, rc * 0.5, 0, TAU); g.fillStyle = "rgba(255,253,246,0.9)"; g.fill();
      g.lineWidth = 0.6; g.strokeStyle = "rgba(60,40,14,0.6)"; g.beginPath(); g.arc(cx, cy, rc, 0, TAU); g.stroke();
    } else { const cg = g.createRadialGradient(cx, cy, 0, cx, cy, rc); cg.addColorStop(0, "rgba(255,252,240,1)"); cg.addColorStop(1, "rgba(255,226,170,0.95)");
      g.beginPath(); g.arc(cx, cy, rc, 0, TAU); g.fillStyle = cg; g.fill(); }
    g.beginPath(); g.arc(cx - rc * 0.35, cy - rc * 0.38, rc * 0.22, 0, TAU); g.fillStyle = "rgba(255,255,255,0.9)"; g.fill();
    g.restore();
  }
  // what the years lived so far add to the window: heavier lead round a turning point, a jewel for a moment that
  // mattered (set once the year's glass is half in; drawn again only where they changed)
  // what a year shows on its glass (its heavy lead, its jewel), to know which years' marks changed
  const markSig = (I, D) => (I && I.row ? (I.turn ? "t" : "") + (I.jewel && (D === 2 || (I.jewel.size === 2 && D === 1)) ? I.jewel.size + I.jewel.cs.join("") : "") : "");
  function markOf(g, X, I, y) {
    const P = st.PL.panes[y], D = X.detail, { wL } = leadW(X);
    g.lineJoin = "round"; g.lineCap = "round";
    if (I.turn) leadLine(g, X, shapeOf(X, P), wL * (D === 2 ? 2.1 : D === 1 ? 1.8 : 1.3), true);
    if (I.jewel && (D === 2 || (I.jewel.size === 2 && D === 1))) jewel(g, X, P, I.jewel);
  }
  // all the marks (after a change of size), or only the years whose marks changed: their boxes are cleared and every
  // mark that reaches into them drawn again there (a year passing changes one or two, not the whole window)
  function paintMarks(Y, ys, sig) {
    const X = st.X, g = st.caches.marks.g;
    if (!ys) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, g.canvas.width, g.canvas.height); g.restore();
      Y.forEach((I, y) => { if (sig[y]) markOf(g, X, I, y); }); return; }
    const bx = ys.map((y) => paneBox(X, st.PL.panes[y])), meets = (a, b) => a[0] < b[0] + b[2] && b[0] < a[0] + a[2] && a[1] < b[1] + b[3] && b[1] < a[1] + a[3];
    g.save(); g.beginPath(); bx.forEach((b) => g.rect(b[0], b[1], b[2], b[3])); g.clip(); bx.forEach((b) => g.clearRect(b[0], b[1], b[2], b[3]));
    Y.forEach((I, y) => { if (sig[y] && bx.some((b) => meets(b, paneBox(X, st.PL.panes[y])))) markOf(g, X, I, y); });
    g.restore();
    bx.forEach((b) => st.rects.push(b));
  }
  // a jewel set in the glass: faceted for a bond begun or someone lost, a small round one for a life event
  // where a jewel sits in its pane and how large it is (in canvas pixels)
  const jewelAt = (X, P, J) => { const big = J.size === 2, D = X.detail;
    if (D <= 1) return { c: X.px(P.scen), rj: Math.max(1.3, Math.min(P.width, P.b - P.a) * X.R * 0.2) };
    return { c: X.px(P.jc || (P.jc = [P.cen[0] * 1.03, P.cen[1] * 1.03])), rj: Math.min(P.width * X.R * (big ? 0.26 : 0.13), X.R * (big ? 0.027 : 0.012)) }; };
  function jewel(g, X, P, J) {
    const big = J.size === 2, { c, rj } = jewelAt(X, P, J);
    const col = J.cs[0], G = GLASS[col], col2 = J.cs[1] ? GLASS[J.cs[1]] : G;
    g.save();
    if (X.detail <= 1) {
      // at the medallion's size, a gold-set bead of the jewel's colour
      g.beginPath(); g.arc(c[0], c[1], rj * 1.35, 0, TAU); g.fillStyle = rgba(GOLD); g.fill(); g.lineWidth = 0.5; g.strokeStyle = "rgba(50,32,8,0.8)"; g.stroke();
      g.beginPath(); g.arc(c[0], c[1], rj * 0.85, 0, TAU); g.fillStyle = rgba(G.mid); g.fill();
      g.restore(); return;
    }
    // the gold collet that holds it
    const cg = g.createRadialGradient(c[0] - rj * 0.5, c[1] - rj * 0.5, 0, c[0], c[1], rj * 1.4);
    cg.addColorStop(0, rgba(GOLD2)); cg.addColorStop(0.6, rgba(GOLD)); cg.addColorStop(1, rgba(GOLD3));
    if (big) { g.beginPath(); g.arc(c[0], c[1], rj * 1.38, 0, TAU); g.fillStyle = cg; g.fill(); g.lineWidth = Math.max(0.5, rj * 0.12); g.strokeStyle = "rgba(30,18,6,0.85)"; g.stroke(); }
    else { g.beginPath(); g.arc(c[0], c[1], rj * 1.3, 0, TAU); g.fillStyle = cg; g.fill(); g.lineWidth = 0.5; g.strokeStyle = "rgba(30,18,6,0.85)"; g.stroke(); }
    if (big) {
      // eight facets round a table, each lit by how it faces the light (from the upper left)
      const n = 8, rt = rj * 0.52, rot = Math.PI / 8;
      for (let i = 0; i < n; i++) { const a0 = rot + (i / n) * TAU, a1 = rot + ((i + 1) / n) * TAU, am = (a0 + a1) / 2;
        const lit = 0.5 + 0.5 * Math.cos(am - (-Math.PI * 0.75)), cc = mix(i % 2 ? col2.dim : G.dim, i % 2 ? col2.lum : G.lum, 0.15 + 0.8 * lit);
        g.beginPath(); g.moveTo(c[0] + Math.cos(a0) * rt, c[1] + Math.sin(a0) * rt); g.lineTo(c[0] + Math.cos(a0) * rj, c[1] + Math.sin(a0) * rj);
        g.lineTo(c[0] + Math.cos(a1) * rj, c[1] + Math.sin(a1) * rj); g.lineTo(c[0] + Math.cos(a1) * rt, c[1] + Math.sin(a1) * rt); g.closePath(); g.fillStyle = rgba(cc); g.fill(); }
      g.beginPath(); for (let i = 0; i < n; i++) { const a = rot + (i / n) * TAU; g[i ? "lineTo" : "moveTo"](c[0] + Math.cos(a) * rt, c[1] + Math.sin(a) * rt); } g.closePath();
      const tg = g.createLinearGradient(c[0] - rt, c[1] - rt, c[0] + rt, c[1] + rt); tg.addColorStop(0, rgba(G.lum)); tg.addColorStop(1, rgba(G.mid)); g.fillStyle = tg; g.fill();
      g.lineWidth = Math.max(0.4, rj * 0.06); g.strokeStyle = "rgba(255,255,255,0.35)"; g.stroke();
    } else {
      // a cabochon: a smooth dome of the colour in a gold ring
      const rg = g.createRadialGradient(c[0] - rj * 0.35, c[1] - rj * 0.35, 0, c[0], c[1], rj);
      rg.addColorStop(0, rgba(mix(G.lum, [255, 255, 255], 0.3))); rg.addColorStop(0.45, rgba(G.mid)); rg.addColorStop(1, rgba(G.dim));
      g.beginPath(); g.arc(c[0], c[1], rj, 0, TAU); g.fillStyle = rg; g.fill();
    }
    g.beginPath(); g.arc(c[0] - rj * 0.32, c[1] - rj * 0.36, rj * 0.2, 0, TAU); g.fillStyle = "rgba(255,255,255,0.85)"; g.fill();
    g.restore();
  }

  /* ---------- the lit window: the same glass with the sun behind it (built once, at the end) ---------- */
  function litCache() {
    const C = st.caches, X = st.X, R = X.R, NL = st.lastY + 1, key = st.painted.size + "|" + NL;
    if (C.lit && C.lit.key === key) return C.lit.c;
    const L = C.lit || mkCache(X), g = L.g, k = X.k;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, L.c.width, L.c.height);
    // the cartoon as it is (gold tracery on night glass), under everything
    g.drawImage(C.base.c, X.x0 * k, X.y0 * k, X.size * k, X.size * k, 0, 0, L.c.width, L.c.height);
    g.restore();
    // the panes after the last year lived get no glass of their own: the sun behind the boss floods their night glass
    // with a warm, low light (about a quarter of the lived glass's), stronger nearer the heart, so the light reads as a
    // halo round the life and never as glass that is missing
    const rest = runs((P) => (P.y >= NL ? 1 : 0));
    if (rest) { g.save(); g.clip(rest); g.globalCompositeOperation = "screen";
      const wg = g.createRadialGradient(X.cx, X.cy, R * 0.3, X.cx, X.cy, R * 1.02);
      wg.addColorStop(0, "rgba(255,166,84,0.4)"); wg.addColorStop(0.6, "rgba(255,160,76,0.32)"); wg.addColorStop(1, "rgba(250,150,70,0.24)");
      g.fillStyle = wg; g.fillRect(X.x0, X.y0, X.size, X.size);
      // (the gold lines catch the same light a little more than the glass between them)
      g.globalCompositeOperation = "source-over"; g.lineJoin = "round"; g.strokeStyle = "rgba(240,206,134,0.42)";
      if (X.detail === 2) { g.lineWidth = Math.max(0.6, R * 0.0026); st.PL.panes.forEach((P) => { if (P.y >= NL) { g.beginPath(); path(g, X, P.poly); g.stroke(); } }); }
      else { g.lineWidth = Math.max(0.45, R * 0.009); st.PL.panes.forEach((P) => { if (P.y >= NL) { g.beginPath(); path(g, X, P.sec); g.stroke(); } }); }
      g.restore(); }
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
    // the coloured glass burns deeper and brighter: more saturated, a little brighter (never washed toward pastel)
    g.filter = FILTER ? (X.detail === 2 ? "saturate(1.3) brightness(1.06)" : "saturate(1.12) brightness(1.05)") : "none"; g.drawImage(C.lived.c, 0, 0);
    if (!FILTER) { g.globalCompositeOperation = "overlay"; g.globalAlpha = 0.25; g.drawImage(C.lived.c, 0, 0); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1; }
    // and the lead goes to silhouette against it
    g.filter = FILTER ? "brightness(0.45)" : "none"; g.drawImage(C.lead.c, 0, 0);
    g.filter = "none"; g.restore();
    L.key = key; C.lit = L; C.litSmall = null; st.bloomFor = ""; st.all = true;
    return L.c;
  }

  /* ---------- the state, eased: the age (panes fill as it passes) and the light at the end ---------- */
  function update(S) {
    if (!S || !CH.life) return;
    st.S = S;
    const N = Math.max(CENTURY, Math.floor(S.age + 1e-6) + 1);
    if (!st.PL || st.PL.N !== N) { st.PL = plan(N); st.cuts.clear(); rebuild(); st.key = ""; }
    // the years are read again only when a river row or a story line was added or taken away
    const key = (S.river ? S.river.length : 0) + "|" + (S.items ? S.items.length : 0) + "|" + Math.floor(S.age + 1e-6);
    // (a year passing repaints only what changed: its pane, the marks that moved, the outline of the year being lived)
    if (key !== st.key) { if (!st.key) st.all = true; st.key = key; st.Y = readYears(S, st.PL); }
    st.target = S.age;
    const was = st.atEnd, y0 = st.lastY;
    st.atEnd = S.age >= CH.life.end_age - 0.01;
    st.lastY = Math.floor(S.age + 1e-6);
    if (st.X && y0 !== st.lastY && st.X.detail <= 1) [y0, st.lastY].forEach((y) => { if (st.PL.panes[y]) st.rects.push(paneBox(st.X, st.PL.panes[y])); });
    if (was !== st.atEnd) st.all = true;
    // the first state is shown as it is (no filling from birth); later changes ease
    if (st.first || CH.motion() === "off") { st.age = S.age; st.first = false; }
    if (CH.motion() === "off") { still(); st.all = true; }
    cv.setAttribute("aria-label", label());
    if (CH.motion() === "off") render(true);
    mark();
  }
  // motion off: every light at its end state, no fade
  function still() { st.sweep = st.lit = st.litP = st.litC = st.setC = st.atEnd ? 1 : 0; st.xf = 0; setOp(dk, "dkOp", 0); root.classList.toggle("chw-lit", !!st.litC); }
  // a click, Space or Esc at the end (the piece below): the light at once at its end, as with motion off; it moves on
  // from there as the motion setting says
  function skip() { if (!st.S || !st.atEnd) return; st.age = st.target; still(); st.all = true; render(true); mark(); }
  // where the end's light is, on the root (data-light): day while they live, lighting, lit
  function mark() {
    const v = !st.atEnd || (!st.litP && !st.litC && !st.sweep) ? "day" : st.sweep >= 1 && st.setC >= 1 && st.litP >= 1 && st.xf <= 0 ? "lit" : "lighting";
    if (v !== st.light) { st.light = v; root.dataset.light = v; }
  }
  function label() {
    const S = st.S, n = Math.floor(S.age);
    return st.atEnd ? `The life's window, lit from behind: one pane for each of the ${n + 1} years of ${CH.life.name ? CH.life.name + "'s" : "their"} life. Use the arrow keys to read the years.`
      : `The life's window: one pane for each year lived, glazed so far to age ${n}. Use the arrow keys to read the years.`;
  }
  // how much of a year's pane is glazed: the year being lived fills as it goes; at the end the last year is whole
  const fillOf = (y) => { const f = clamp(st.age - y); return st.atEnd && y === st.lastY ? Math.max(f, st.litC) : f; };

  /* ---------- the frame loop: ease, paint what is new, compose what changed, move what moves ---------- */
  function draw(now, dt) {
    if (!st.PL || !st.S || !st.X) return;
    const mot = CH.motion(), sp = CH.speed();
    if (mot === "off") { if (st.all || st.rects.length || st.more) render(true); mark(); return; }
    st.t += dt * sp;
    // ease the age: the panes fill in order as it passes (about 0.4 s, a long jump a little longer; slower when calm)
    if (mot !== "off" && Math.abs(st.target - st.age) > 1e-4) {
      const a0 = st.age, k = 1 - Math.exp(-dt / (0.13 / Math.sqrt(Math.max(0.35, sp)))); st.age += (st.target - st.age) * k; if (Math.abs(st.target - st.age) < 0.002) st.age = st.target;
      wantYears(a0, st.age);
    }
    // the light at the end: dusk falls, then the sweep runs through the years in order, then the window breathes. It
    // waits to begin while the page holds it (a chapter plate is up); once begun, or skipped to, it stays
    const wait = !st.litC && !st.litP && !!(opts.hold && opts.hold());
    const done = st.atEnd && (st.litC > 0 || (!wait && st.age >= st.target - 0.02 && allPainted()));
    const litT = done ? 1 : 0;
    // the light on the layers over the glass (bloom, rays, glints, flares) eases with a ramp of fixed length
    if (st.litP !== litT) { st.litP = litT ? Math.min(1, st.litP + dt / 1.2) : Math.max(0, st.litP - dt / 0.7); st.lit = easeIO(st.litP); }
    if (done && st.sweep < 1 && st.lit > 0.6) st.sweep = Math.min(1, st.sweep + dt / (8 / Math.sqrt(Math.max(0.35, sp))));
    if (!st.atEnd && st.sweep > 0) st.sweep = Math.max(0, st.sweep - dt * 3);
    // the glass's own light (dusk falling at the end, the frame lifting a little once the light has run through, day
    // again on going back) changes in one compose, under a picture of the old light that fades away
    const setT = done && st.sweep >= 1 ? 1 : 0;
    if (st.litC !== litT || st.setC !== setT) { fadeFrom(litT < st.litC ? 0.7 : st.litC !== litT ? 1.2 : 1.5); st.litC = litT; st.setC = setT; st.all = true;
      // (the light crossing the glass while they live gives way to the light behind it)
      root.classList.toggle("chw-lit", !!litT); }
    if (st.xf > 0) { st.xf = Math.max(0, st.xf - dt / st.xfDur); setOp(dk, "dkOp", easeIO(st.xf)); }
    render(false, now);
    mark();
  }
  // keep what shows (the window, and any fade still running over it) on the fade canvas, at full strength
  function fadeFrom(dur) {
    const X = st.X, g = dk.getContext("2d"), o = st.xf > 0.002 ? st.dkOp : 0;
    if (dk.width !== cv.width || dk.height !== cv.height) { dk.width = cv.width; dk.height = cv.height; }
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
    if (o > 0) { g.globalCompositeOperation = "destination-in"; g.fillStyle = `rgba(0,0,0,${o})`; g.fillRect(0, 0, dk.width, dk.height); g.globalCompositeOperation = "destination-over"; }
    else g.clearRect(0, 0, dk.width, dk.height);
    // (only the window's own disc, which is opaque, so the two pictures mix exactly and the shadow round it is kept once)
    g.setTransform(cv._k, 0, 0, cv._k, 0, 0); g.beginPath(); g.arc(X.cx, X.cy, X.detail === 2 ? X.Rr : X.R, 0, TAU); g.clip();
    g.drawImage(cv, 0, 0, X.W, X.H); g.restore();
    st.xf = 1; st.xfDur = dur; setOp(dk, "dkOp", 1);
  }
  const allPainted = () => { for (let y = 0; y <= Math.min(st.lastY, st.PL.N - 1); y++) if (st.Y[y] && st.Y[y].row && !st.painted.has(y)) return false; return true; };
  // the panes whose glazing changed between two eased ages
  function wantYears(a0, a1) {
    const lo = Math.max(0, Math.floor(Math.min(a0, a1))), hi = Math.min(st.PL.N - 1, Math.floor(Math.max(a0, a1)));
    if (hi - lo > 5) { st.all = true; return; }
    for (let y = lo; y <= hi; y++) st.rects.push(paneBox(st.X, st.PL.panes[y]));
  }

  function render(still, now) {
    if (!st.X || !st.caches || !st.PL || !st.S) return;
    const X = st.X, PL = st.PL, Y = st.Y, mot = still ? "off" : CH.motion();
    // paint any year now lived that has no glass yet (in motion a few milliseconds' worth a frame, in the order the
    // years were lived, so a long jump glazes over a few frames), and the marks when the years read changed
    // (still frames glaze a little more a frame, and go on in the next frame: st.more)
    const t0 = performance.now(), cur = Math.min(PL.N - 1, st.lastY), budget = mot !== "off" ? 6 : 24;
    st.more = false;
    for (let y = 0; y <= cur; y++) { const I = Y[y]; if (!I || !I.row || st.painted.get(y) === I.sig) continue;
      if (fillOf(y) <= 0 && y > Math.floor(st.age)) continue;
      if (performance.now() - t0 > budget) { st.more = true; break; }
      paintPane(PL.panes[y], I); st.rects.push(paneBox(X, PL.panes[y])); }
    // (a year's marks are set once its glass is half in, or at once for the year being lived: never on bare night)
    const markOn = (y) => fillOf(y) >= 0.45 || (y === st.lastY && Math.abs(st.target - st.age) < 0.02);
    let nOn = 0; for (let y = 0; y <= cur; y++) if (Y[y] && Y[y].row && markOn(y)) nOn++;
    const mKey = st.key + "|" + nOn + "|" + X.size;
    if (st.marksFor !== mKey) {
      const sig = Y.map((I, y) => (markOn(y) ? markSig(I, X.detail) : "")), was = st.marksFor.split("|").pop() === String(X.size) && st.markSig;
      const ch = was ? sig.map((v, y) => (v !== (st.markSig[y] || "") ? y : -1)).filter((y) => y >= 0) : null;
      for (let y = sig.length; was && y < st.markSig.length; y++) if (st.markSig[y]) ch.push(y);
      if (ch && ch.length <= 12) { if (ch.length) paintMarks(Y, ch, sig); } else { paintMarks(Y, null, sig); st.all = true; }
      st.marksFor = mKey; st.markSig = sig;
      // the jewelled years, for the glints (worked out here, not every frame)
      st.jewelYs = Y.filter((I) => I.row && I.jewel && X.detail === 2).map((I) => I.y); }
    // at the end, the lit glass (made a few frames into the dusk, not in the frame that starts it; let go on going back)
    if (!st.atEnd && st.caches.lit && !st.litC) { st.caches.lit = null; st.caches.litSmall = null; }
    if (st.litC && st.lit > 0.25 && allPainted()) litCache();
    // what of the window must be composed again: all of it after a change of size or of its light; while the sweep
    // runs, only the panes it is lighting; while they live, the panes that filled and the marks that changed
    const A = litAlphas();
    if (A && st.litA && !st.all) A.forEach((a, y) => { if (a !== st.litA[y]) st.rects.push(paneBox(X, PL.panes[y])); });
    st.litA = A;
    if (st.all) { compose(null); st.all = false; st.rects.length = 0; }
    else if (st.rects.length) { const rs = st.rects.splice(0); compose(rs.length > 24 ? null : rs); }
    layers(mot, now || 0);
  }
  /* The end's light, in years: how far it has run through the life (0 to the last year lived + FADE), and last of all
     the low, warm light over the panes after the last year. Each pane takes FADE years of the sweep to come fully alight, so a few burn at once, like
     a flame running along a fuse. */
  const FADE = 2.6, FLOOD = 4;
  const sweepPos = () => (st.atEnd ? easeIO(st.sweep) * (st.lastY + 1 + FADE + FLOOD) : 0);
  function litAlphas() {
    if (!st.atEnd || !st.litC || !st.caches.lit) return null;
    const pos = sweepPos(), NL = st.lastY + 1;
    return st.PL.panes.map((P) => (P.y < NL ? clamp((pos - P.y) / FADE) : clamp((pos - NL - FADE * 0.5) / FLOOD)));
  }

  /* ---------- composing the still window (all of it, or one box) from the copies ---------- */
  function compose(rects) {
    const X = st.X, C = st.caches, g = cv.getContext("2d"), R = X.R, lit = st.litC;
    g.setTransform(cv._k, 0, 0, cv._k, 0, 0);
    g.save();
    // (the boxes snapped out to whole device pixels, so their edges leave no seam)
    if (rects) { const k = cv._k, B = rects.map((r) => { const x = Math.floor(r[0] * k) / k, y = Math.floor(r[1] * k) / k; return [x, y, Math.ceil((r[0] + r[2]) * k) / k - x, Math.ceil((r[1] + r[3]) * k) / k - y]; });
      g.beginPath(); B.forEach((r) => g.rect(r[0], r[1], r[2], r[3])); g.clip(); B.forEach((r) => g.clearRect(r[0], r[1], r[2], r[3])); }
    else g.clearRect(0, 0, X.W, X.H);
    g.drawImage(C.base.c, 0, 0, X.W, X.H);
    // the glazed years: every pane lived, the year being lived filled from its inner edge
    const lp = runs((P) => (st.painted.has(P.y) ? fillOf(P.y) : 0));
    if (lp) { g.save(); g.clip(lp); put(g, X, C.lived); g.restore(); }
    // the room's light on the glass: day while they live (a small medallion lighter, as on parchment), dusk at the end
    const day = X.detail === 2 ? [228, 222, 236] : [244, 240, 246], dusk = X.detail === 2 ? [118, 110, 142] : [222, 214, 230];
    g.save(); g.globalCompositeOperation = "multiply"; g.beginPath(); g.arc(X.cx, X.cy, R * 1.002, 0, TAU); g.fillStyle = rgba(mix(day, dusk, lit)); g.fill(); g.restore();
    put(g, X, C.lead);
    // the lit years: the light reaches each pane in turn
    if (st.litA && C.lit) {
      const done = runs((P) => (st.litA[P.y] >= 1 ? 1 : 0));
      g.save(); g.globalAlpha = lit; if (done) { g.save(); g.clip(done); put(g, X, C.lit); g.restore(); }
      st.litA.forEach((a, y) => { if (a <= 0 || a >= 1) return; const p = new Path2D(); sector(p, X, st.PL.panes[y], st.PL.panes[y].b);
        g.save(); g.clip(p); g.globalAlpha = lit * easeIO(a); put(g, X, C.lit); g.restore(); });
      g.restore();
    }
    // the frame, which goes toward silhouette as the dusk falls and settles a little lighter once the window is lit
    put(g, X, C.frame);
    const fd = lit * (1 - 0.4 * st.setC);
    if (fd > 0.002 && X.detail === 2) frameShade(g, X, mix([255, 255, 255], [150, 140, 170], fd));
    put(g, X, C.marks);
    if (X.detail <= 1 && !st.atEnd && st.PL.panes[st.lastY]) { g.beginPath(); path(g, X, st.PL.panes[st.lastY].sec); g.lineJoin = "round"; g.lineWidth = Math.max(0.9, R * 0.03); g.strokeStyle = rgba([196, 140, 40], 0.95); g.stroke(); }
    // the hovered or focused year, outlined in gold (a soft wide stroke under a sharp one)
    const hv = st.hover >= 0 ? st.hover : st.focus;
    if (hv >= 0 && st.PL.panes[hv]) { const P = st.PL.panes[hv]; g.lineJoin = "round";
      g.beginPath(); path(g, X, shapeOf(X, P)); g.lineWidth = Math.max(3, R * 0.03); g.strokeStyle = rgba(GOLD2, 0.22); g.stroke();
      g.lineWidth = Math.max(1.2, R * 0.009); g.strokeStyle = rgba(GOLD2, 0.95); g.stroke(); }
    g.restore();
  }
  // the frame's own shapes darkened by the dusk (multiply on the rim, the iron rings and the boss only)
  function frameShade(g, X, col) {
    const R = X.R, { wBar } = leadW(X);
    g.save(); g.globalCompositeOperation = "multiply"; g.fillStyle = g.strokeStyle = rgba(col);
    g.beginPath(); g.arc(X.cx, X.cy, X.Rr + 0.5, 0, TAU); g.arc(X.cx, X.cy, R * 0.99, 0, TAU, true); g.fill("evenodd");
    st.PL.rings.forEach((G) => { if (!G.i) return; g.beginPath(); g.arc(X.cx, X.cy, G.a * R, 0, TAU); g.lineWidth = wBar * 1.5; g.stroke(); });
    g.beginPath(); g.arc(X.cx, X.cy, BOSS * R + 0.5, 0, TAU); g.fill();
    g.restore();
  }
  // a path of the panes with a share f(P) > 0 of their glass shown: the panes shown whole in each ring run from its
  // first pane, so each ring is one sector (or one ring); the pane being glazed is drawn from its inner edge
  function runs(f) {
    const p = new Path2D(), X = st.X, R = X.R; let any = false;
    st.PL.rings.forEach((G) => {
      // (the run of whole panes starts at the ring's first pane for the years lived, later for the panes after them)
      let s = 0; while (s < G.n && f(G.panes[s]) < 0.999) s++;
      let e = s; while (e < G.n && f(G.panes[e]) >= 0.999) e++;
      if (e > s) { any = true;
        if (e - s === G.n) { p.moveTo(X.cx + G.b * R * 1.002, X.cy); p.arc(X.cx, X.cy, G.b * R * 1.002, 0, TAU); p.moveTo(X.cx + G.a * R * 0.995, X.cy); p.arc(X.cx, X.cy, G.a * R * 0.995, TAU, 0, true); }
        else arcSector(p, X, G.a * 0.995, G.b * 1.002, G.panes[s].t0 - 0.004, G.panes[e - 1].t1 + 0.004); }
      G.panes.forEach((P, j) => { if (j >= s && j < e) return; const v = f(P); if (v <= 0) return; if (v >= 0.999) { any = true; sector(p, X, P, P.b); return; }
        any = true; arcSector(p, X, P.a * 0.995, P.a + (P.b - P.a) * easeIO(v), P.t0 - 0.004, P.t1 + 0.004); });
    });
    return any ? p : null;
  }
  function arcSector(p, X, r0, r1, t0, t1) { const R = X.R; p.moveTo(X.cx + Math.cos(t0) * r0 * R, X.cy + Math.sin(t0) * r0 * R); p.arc(X.cx, X.cy, r1 * R, t0, t1); p.arc(X.cx, X.cy, r0 * R, t1, t0, true); p.closePath(); }
  // a pane's whole sector (the lancet and the halves of the spandrels beside it)
  const sector = (p, X, P, b) => arcSector(p, X, P.a * 0.995, b * 1.002, P.t0 - 0.004, P.t1 + 0.004);

  /* ---------- what moves: the year's glow, the glints, the sweep's flares (on their own canvas), the shimmer, the
     bloom's and the rays' breath (the compositor's), the dust in the rays ---------- */
  function layers(mot, now) {
    const X = st.X, t = st.t, lit = st.lit;
    // the moving light, added over the window (screen): clear last frame's boxes, draw this frame's
    const g = fx.getContext("2d"); g.setTransform(fx._k, 0, 0, fx._k, 0, 0);
    st.fxRects.forEach((r) => g.clearRect(r[0], r[1], r[2], r[3])); st.fxRects = [];
    if (!st.atEnd && X.detail === 2 && st.lastY >= 0 && st.lastY < st.PL.N) nowMark(g, X, st.PL.panes[st.lastY], fillOf(st.lastY), t, mot);
    if (mot !== "off") { glints(g, X, t, lit); flares(g, X); }
    // the bloom: the lit glass's light spilling over the lead, and a warm sun behind the boss
    const pos = sweepPos(), NL = st.lastY + 1;
    // (going back, the bloom keeps its last picture and fades with the light)
    if (st.atEnd) st.bloMax = sstep(0, 1, pos / NL);
    const blo = lit * st.bloMax * (mot === "off" ? 1 : 1 + 0.08 * Math.sin(t * 0.7));
    if (blo > 0.004 && st.atEnd) paintBloom(X);
    setOp(bl, "bloomOp", clamp(0.3 * blo));
    // the rays (full size): the halo and the shafts drawn once, revealed and breathing by their opacity
    if (rv) {
      const ro = lit * sstep(0, 1, st.sweep * 1.25 - 0.1) * (mot === "off" ? 1 : 0.86 + 0.14 * Math.sin(t * 0.45));
      if (ro > 0.004 && X.detail === 2) paintRays();
      setOp(rv, "raysOp", X.detail === 2 ? clamp(ro) : 0);
      motes(mot, t, lit);
    }
  }
  const setOp = (el, k, v) => { v = Math.round(v * 200) / 200; if (st[k] !== v) { st[k] = v; el.style.opacity = v; el.style.visibility = v > 0 ? "visible" : "hidden"; } };
  function nowMark(g, X, P, f, t, mot) {
    const R = X.R, r = (P.a + (P.b - P.a) * easeIO(f)) * R, pulse = mot === "off" ? 0.7 : 0.6 + 0.4 * Math.sin(t * 2.2);
    const x = X.cx + Math.cos(P.phi) * r, y = X.cy + Math.sin(P.phi) * r, rad = Math.max(3, Math.min(P.width, P.b - P.a) * R * 0.42);
    const gr = g.createRadialGradient(x, y, 0, x, y, rad); gr.addColorStop(0, `rgba(255,226,170,${0.4 * pulse})`); gr.addColorStop(0.5, `rgba(255,214,150,${0.12 * pulse})`); gr.addColorStop(1, "rgba(255,214,150,0)");
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, rad, 0, TAU); g.fill();
    if (X.detail >= 1 && f > 0.02 && f < 0.98) { g.beginPath(); g.arc(X.cx, X.cy, r, P.t0 + 0.01, P.t1 - 0.01); g.lineWidth = Math.max(1, R * 0.005); g.strokeStyle = `rgba(255,240,210,${0.55 * pulse})`; g.stroke(); }
    const bx = boxOf(X, P.sec, rad + 2); st.fxRects.push(bx);
  }
  function glints(g, X, t, lit) {
    // now and then a jewel catches the light: a four-pointed star, a breath long
    if (X.detail < 2) return;
    const per = 1.9, slot = Math.floor(t / per), ph = (t % per) / per;
    const a = Math.sin(clamp(ph / 0.45) * Math.PI) * (0.6 + 0.4 * lit); if (a <= 0.01) return;
    const js = st.jewelYs.filter((y) => fillOf(y) >= 1); if (!js.length) return;
    const y = js[Math.floor(CH.rng(slot * 7 + 3)() * js.length)], I = st.Y[y]; if (!I || !I.jewel) return;
    const { c, rj } = jewelAt(X, st.PL.panes[y], I.jewel); if (rj < 1.2) return;
    const x = c[0] - rj * 0.3, yy = c[1] - rj * 0.35, L = rj * (2.6 + lit);
    g.save(); g.strokeStyle = `rgba(255,250,235,${0.85 * a})`; g.lineCap = "round";
    [[L, 0.9], [L * 0.55, 0.6]].forEach(([l, w], i) => { g.lineWidth = w; g.beginPath(); const r = i * Math.PI / 4; g.moveTo(x - Math.cos(r) * l, yy - Math.sin(r) * l); g.lineTo(x + Math.cos(r) * l, yy + Math.sin(r) * l);
      g.moveTo(x + Math.sin(r) * l, yy - Math.cos(r) * l); g.lineTo(x - Math.sin(r) * l, yy + Math.cos(r) * l); g.stroke(); });
    g.restore();
    st.fxRects.push([x - L - 2, yy - L - 2, 2 * L + 4, 2 * L + 4]);
  }
  // each pane flares warm as the light reaches it
  function flares(g, X) {
    if (!st.litA) return;
    st.litA.forEach((a, y) => { if (a <= 0 || a >= 1) return; const P = st.PL.panes[y], c = X.px(X.detail === 2 ? P.cen : P.scen), rad = Math.max(P.width, P.b - P.a) * X.R * 0.9, fl = Math.sin(Math.PI * a) * st.lit;
      const fg = g.createRadialGradient(c[0], c[1], 0, c[0], c[1], rad); fg.addColorStop(0, `rgba(255,232,186,${0.5 * fl})`); fg.addColorStop(1, "rgba(255,232,186,0)");
      g.fillStyle = fg; g.fillRect(c[0] - rad, c[1] - rad, rad * 2, rad * 2); st.fxRects.push([c[0] - rad - 1, c[1] - rad - 1, rad * 2 + 2, rad * 2 + 2]); });
  }
  // the bloom's picture: the lit panes, small and soft, and the sun behind the boss (drawn again only while the sweep
  // moves; its strength is the layer's opacity)
  function paintBloom(X) {
    const C = st.caches; if (!C.lit) return;
    if (st.sweep >= 1 && st.bloomFor === "done") return;
    const key = st.sweep >= 1 ? "done" : st.litA ? st.litA.map((a) => (a >= 1 ? 1 : a <= 0 ? 0 : 2)).join("") + "|" + Math.round(sweepPos() * 4) : "x";
    if (st.bloomFor === key) return; st.bloomFor = key;
    const bw = bl.width, s = bw / X.size;
    if (!C.litSmall) { const c = document.createElement("canvas"); c.width = c.height = bw; const g = c.getContext("2d"); g.imageSmoothingQuality = "high";
      if (FILTER) g.filter = "blur(1.2px)"; g.drawImage(C.lit.c, 0, 0, bw, bw); C.litSmall = c; }
    const g = bl.getContext("2d"); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, bw, bw);
    g.setTransform(s, 0, 0, s, -X.x0 * s, -X.y0 * s);
    const A = st.litA || [], dn = runs((P) => (A[P.y] >= 1 ? 1 : 0));
    if (dn) { g.save(); g.clip(dn); g.drawImage(C.litSmall, X.x0, X.y0, X.size, X.size); g.restore(); }
    A.forEach((a, y) => { if (a <= 0 || a >= 1) return; const p = new Path2D(); sector(p, X, st.PL.panes[y], st.PL.panes[y].b); g.save(); g.clip(p); g.globalAlpha = a; g.drawImage(C.litSmall, X.x0, X.y0, X.size, X.size); g.restore(); });
    // the sun behind the centre: one warm glow from the boss
    const hs = g.createRadialGradient(X.cx, X.cy, 0, X.cx, X.cy, X.R * 0.9); hs.addColorStop(0, "rgba(255,226,170,0.5)"); hs.addColorStop(0.4, "rgba(255,210,150,0.16)"); hs.addColorStop(1, "rgba(255,200,140,0)");
    g.globalCompositeOperation = "lighter"; g.fillStyle = hs; g.fillRect(X.x0, X.y0, X.size, X.size); g.globalCompositeOperation = "source-over";
  }

  /* ---------- the rays: coloured shafts of light falling from the lit window, drawn once, soft, at half resolution ---------- */
  // the rays' canvases reach past the window's square (sides and below); worked out on a change of size only, with how
  // far down the light may fall before a box that clips its overflow (so no container's edge ever cuts a shaft)
  function fitRays() {
    if (!rv) return null;
    const W = root.offsetWidth, H = root.offsetHeight; if (!W || !H) return null;
    const L = { ex: 0.1, et: 0.1, eb: 0.3 }, cw = W * (1 + 2 * L.ex), ch = H * (1 + L.et + L.eb), k = (cv._k || 1) * 0.5;
    Object.assign(rv.style, { left: -W * L.ex + "px", top: -H * L.et + "px", width: cw + "px", height: ch + "px" });
    const w = Math.max(1, Math.round(cw * k)), h = Math.max(1, Math.round(ch * k)); if (rv.width !== w || rv.height !== h) { rv.width = w; rv.height = h; }
    const rr = root.getBoundingClientRect(), vs = rr.width / W || 1; let lim = H * (1 + L.eb);
    for (let e = root.parentElement; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e); if (cs.overflowY !== "visible" || cs.overflowX !== "visible") lim = Math.min(lim, (e.getBoundingClientRect().bottom - rr.top) / vs); }
    st.rays = "";
    // the dust's box: the air below the window's heart, down to where the shafts fade (and never past a clipping box)
    const X = st.X;
    if (X) { const top = X.cy + X.R * 0.15, bot = Math.max(top + 10, Math.min(X.cy + X.R * 1.6, lim - 8));
      Object.assign(mv.style, { left: X.cx - X.R * 1.2 + "px", top: top + "px", width: X.R * 2.1 + "px", height: bot - top + "px" }); }
    return { k, cw, ch, ox: W * L.ex, oy: H * L.et, W, H, lim };
  }
  function paintRays() {
    const RL = st.RL, X = st.X; if (!RL) return;
    const key = st.key + "|" + X.size + "|" + RL.lim; if (st.rays === key) return; st.rays = key;
    const g = rv.getContext("2d"); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, rv.width, rv.height);
    g.setTransform(RL.k, 0, 0, RL.k, RL.ox * RL.k, RL.oy * RL.k);
    paintShafts(g, X, RL);
    // a halo of light round the frame, warm, as from a sky behind it
    // (it starts clear at the frame: a radial gradient pads its inside with its first colour)
    const hr = Math.min(X.Rr * 1.42, X.Rr + Math.min(RL.ox, RL.oy) * 0.95), hg = g.createRadialGradient(X.cx, X.cy, X.Rr * 0.97, X.cx, X.cy, hr), f = (X.Rr * 1.01 - X.Rr * 0.97) / (hr - X.Rr * 0.97);
    hg.addColorStop(0, "rgba(255,214,150,0)"); hg.addColorStop(clamp(f), "rgba(255,214,150,0.3)"); hg.addColorStop(clamp(f + 0.3), "rgba(240,170,120,0.09)"); hg.addColorStop(1, "rgba(0,0,0,0)");
    g.globalCompositeOperation = "lighter"; g.fillStyle = hg; g.fillRect(-RL.ox, -RL.oy, RL.cw, RL.ch);
    g.globalCompositeOperation = "source-over";
  }
  /* Shafts of light: eight, from the brightest years (satisfaction) of the two outer rings lived, spread round the
     window, each in the colour of that year's leading glass with its hue kept. They fall a little to the left, widen
     as they fall, show only in the air below the window's heart and fade out well before the floor. */
  function paintShafts(g, X, RL) {
    const PL = st.PL, Y = st.Y, rings = PL.rings.filter((G) => G.years.some((y) => Y[y] && Y[y].row)).slice(-2).map((G) => G.i);
    const cand = PL.panes.filter((P) => rings.includes(P.ring) && Y[P.y] && Y[P.y].row && P.y <= st.lastY).sort((a, b) => Y[b.y].sat - Y[a.y].sat);
    const picks = [];
    cand.forEach((P) => { if (picks.length >= 8) return; if (picks.every((Q) => Math.abs(((P.phi - Q.phi + 3 * Math.PI) % TAU) - Math.PI) > TAU / 11)) picks.push(P); });
    const sl = 0.1, dir = [-Math.sin(sl), Math.cos(sl)], floor = Math.min(X.cy + X.R * 1.7, RL.lim - 6), r = CH.rng(808);
    g.save(); g.globalCompositeOperation = "lighter";
    picks.forEach((P) => {
      const I = Y[P.y], lead = CS[I.w.indexOf(Math.max(...I.w))], p = X.px(P.cen), len = Math.max(10, (floor - p[1]) / dir[1]);
      const w0 = P.width * X.R * (0.3 + r() * 0.15), w1 = w0 * (2 + r() * 0.6);
      const col = mix(glassRGB(lead, clamp(I.sat)), [255, 238, 206], 0.35), a = 0.06 + 0.06 * clamp(I.sat);
      const e = [p[0] + dir[0] * len, p[1] + dir[1] * len], nx = -dir[1], ny = dir[0];
      const gr = g.createLinearGradient(p[0], p[1], e[0], e[1]);
      gr.addColorStop(0, rgba(col, 0)); gr.addColorStop(0.3, rgba(col, a)); gr.addColorStop(0.8, rgba(col, 0)); gr.addColorStop(1, rgba(col, 0));
      g.beginPath(); g.moveTo(p[0] + nx * w0 / 2, p[1] + ny * w0 / 2); g.lineTo(e[0] + nx * w1 / 2, e[1] + ny * w1 / 2); g.lineTo(e[0] - nx * w1 / 2, e[1] - ny * w1 / 2); g.lineTo(p[0] - nx * w0 / 2, p[1] - ny * w0 / 2); g.closePath();
      g.fillStyle = gr; g.fill();
    });
    // light only shows in the air below the window's heart, strongest past its lower rim
    g.globalCompositeOperation = "destination-in";
    const m = g.createLinearGradient(0, X.cy + X.R * 0.1, 0, X.cy + X.R * 1.1); m.addColorStop(0, "rgba(0,0,0,0)"); m.addColorStop(0.6, "rgba(0,0,0,0.35)"); m.addColorStop(1, "rgba(0,0,0,1)");
    g.fillStyle = m; g.fillRect(-RL.ox, -RL.oy, RL.cw, RL.ch);
    g.restore();
  }
  // dust drifting in the light (full motion only, once the light has run half way): the specks fall by themselves
  // (CSS); here only the box's strength is set, and the box is taken out of the page when it is not shown
  function motes(mot, t, lit) {
    if (!mv) return;
    const on = mot === "full" && lit > 0.01 && st.sweep > 0.5 && st.X.detail === 2;
    if (on !== st.motesOn) { st.motesOn = on; root.classList.toggle("chw-mo", on); }
    setOp(mv, "motesOp", on ? lit * clamp(st.sweep * 2 - 1) : 0);
  }

  /* ---------- hover, keys and taps: each year in words ---------- */
  function hit(x, y) {
    const X = st.X, PL = st.PL; if (!X || !PL) return -2;
    const dx = (x - X.cx) / X.R, dy = (y - X.cy) / X.R, r = Math.hypot(dx, dy);
    if (r > 1.0) return -2; if (r < BOSS) return -3;
    const G = PL.rings.find((g) => r >= g.a && r < g.b) || PL.rings[PL.rings.length - 1];
    const rel = (((Math.atan2(dy, dx) - TOP + G.d / 2) % TAU) + TAU) % TAU;
    return G.panes[Math.min(G.n - 1, Math.floor(rel / G.d))].y;
  }
  const SATW = (v) => (v >= 0.8 ? "Deeply content" : v >= 0.65 ? "Content" : v >= 0.5 ? "Getting by" : v >= 0.35 ? "Discontented" : "Unhappy");
  const PEACEW = (v) => (v >= 0.68 ? "At peace" : v >= 0.55 ? "Calm" : v >= 0.42 ? "Unsettled" : "Troubled");
  const BRIGHTW = (v) => (v >= 0.65 ? "bright glass" : v >= 0.45 ? "glass of middling depth" : "deep, dense glass");
  const CLEARW = (v) => (v >= 0.65 ? "clear glass" : v >= 0.5 ? "a little milky" : "milky, full of seeds");
  // one year in words: a heading, its stage, rows and a foot, each part both as the tooltip's HTML and as plain text
  // for the screen reader's live region
  function words(y) {
    const PL = st.PL, S = st.S;
    if (y === -3) { const b = (S.items || []).find((it) => it.tag === "birth"), l = b ? trunc(firstSentence(CH.plain(b.text)), 130) : "";
      return { head: "Birth", sub: "The boss at the centre, where the window begins.", rows: [], foot: l ? [[CH.esc(l), l]] : [] }; }
    const P = PL.panes[y], I = st.Y[y], lived = I && I.row && y <= st.lastY && fillOf(y) > 0;
    if (!lived) {
      // the panes after the last year: nothing told of them, not even their age (at the end, only the light round the
      // life: no "not lived", nothing that counts what was not reached)
      if (st.atEnd) return { head: "Light round the life", sub: "The window's gold tracery on night glass, lit from behind.", rows: [], foot: [] };
      return { head: "Not lived yet", sub: "Night glass and the glazier's gold lines: its colours come as the years are lived.", rows: [], foot: [] };
    }
    // the game's stage of life that year (from its chapter line); a year with a rite of passage names both, once the
    // game has moved on to the new stage (the year being lived names it only when the top bar does)
    const to = I.rite && I.rite.to && I.rite.to !== I.stage && (y < st.lastY || CH.stageWord(S) !== I.stage) ? I.rite.to : "";
    const head = `Age ${y}`, stage = to ? `${I.stage}, then ${to}` : I.stage;
    // the rite's own line: on the iron ring when the rite falls on a ring's first year, else with the heavier lead
    const rite = I.rite ? (I.rite.ring ? [`<b>The iron ring:</b> a rite of passage. ${CH.esc(I.rite.line)}`, `The iron ring: a rite of passage. ${I.rite.line}`]
      : [`<b>A rite of passage:</b> ${CH.esc(I.rite.line)}`, `A rite of passage: ${I.rite.line}`]) : null;
    if (I.pre) {
      const note = I.river0 != null ? `The life river's record begins at age ${I.river0}; before it, the even start every life grows from.` : "The life river's record has not begun yet: the even start every life grows from.";
      const foot = I.line ? [[CH.esc(I.line), I.line]] : [];
      foot.push([CH.esc(note), note]);
      if (rite) foot.push(rite);
      return { head, sub: stage, rows: [["Who they were", "Still forming", "Still forming"], ["The glass", "Pearl: every colour even (20% each)", "Pearl, every colour even, 20% each"]], foot };
    }
    const top = CS.map((c, i) => [c, I.w[i]]).sort((a, b) => b[1] - a[1]).slice(0, 3), who = I.who;
    const sat = `${SATW(I.sat)} (${CH.pct(I.sat)})`, peace = `${PEACEW(I.peace)} (${CH.pct(I.peace)})`;
    const dim = (s) => ` <span class="chw-tdim">${s}</span>`;
    const rows = [["Who they were", CH.esc(who), who],
      ["The glass", top.map(([c, v]) => `${CH.pip(c)} ${CH.pct(v)}`).join(" "), top.map(([c, v]) => `${NAME[c]} ${CH.pct(v)}`).join(", ")],
      ["Satisfaction", sat + dim(BRIGHTW(I.sat)), `${sat}, ${BRIGHTW(I.sat)}`], ["Peace", peace + dim(CLEARW(I.peace)), `${peace}, ${CLEARW(I.peace)}`]];
    const foot = [];
    if (I.line) foot.push([CH.esc(I.line), I.line]);
    // (a rite that is the turning point is told once, with the heavier lead)
    const tl = I.turnRite && I.rite ? ` ${I.rite.line}` : "";
    if (I.turn) foot.push([`<b>Heavier lead:</b> a turning point, ${CH.esc(I.turn)}.${CH.esc(tl)}`, `Heavier lead: a turning point, ${I.turn}.${tl}`]);
    if (rite && !tl) foot.push(rite);
    if (I.jewel && (st.X.detail === 2 || (I.jewel.size === 2 && st.X.detail === 1))) { const k = I.jewel.size === 2 ? "A jewel" : "A small jewel";
      const w = `${I.jewel.kind === "loss" ? "someone close was lost" : I.jewel.kind === "bond" ? "a bond began" : "the life event that moved them most in this ring of years"}, in the colour of ${names(I.jewel.cs)}.`;
      foot.push([`<b>${k}:</b> ${CH.esc(w)}`, `${k}: ${w}`]); }
    return { head: head + (I.y === st.lastY && st.atEnd ? ", the last year" : ""), sub: stage, rows, foot };
  }
  function tipFor(y) {
    if (y < 0 && y !== -3) return "";
    const w = words(y);
    return CH.tipBox(w.head, w.sub, w.rows.map((r) => [r[0], r[1]]), w.foot.map((f) => f[0]).join("<br>"));
  }
  const speak = (y) => { const w = words(y); return [`${w.head}. ${w.sub}`.replace(/\.?$/, "."), ...w.rows.map((r) => `${r[0]}: ${r[2]}.`), ...w.foot.map((f) => f[1])].join(" "); };
  const setHover = (v) => { if (v === st.hover) return; const old = st.hover; st.hover = v; outlineChanged(old, v); };
  const outlineChanged = (a, b) => { if (!st.X) return; [a, b].forEach((y) => { if (y >= 0 && st.PL.panes[y]) st.rects.push(paneBox(st.X, st.PL.panes[y])); }); if (CH.motion() === "off") render(true); };
  CH.canvasTip(cv, (x, y) => { const h = hit(x, y); if (!st.synth) setHover(h >= 0 ? h : -1); return h === -2 ? "" : tipFor(h); });
  cv.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse" || !e.pointerType) setHover(-1); });
  // the same words for the keyboard: a pointer move made at the pane's centre shows the tooltip there
  const tipAt = (cx, cy) => cv.dispatchEvent(new PointerEvent("pointermove", { clientX: cx, clientY: cy, bubbles: true, pointerType: "mouse" }));
  const tipAtPane = (y) => { const X = st.X; if (!X) return; const P = st.PL.panes[y], q = X.px(X.detail === 2 ? P.cen : P.scen), r = cv.getBoundingClientRect(), vs = cv.offsetWidth ? r.width / cv.offsetWidth : 1;
    st.synth = true; tipAt(r.left + q[0] * vs, r.top + q[1] * vs); st.synth = false; };
  // a tap opens the reading through CH.canvasTip (it stays until the next touch elsewhere); that touch also clears the
  // tapped pane's outline here
  const offTap = (e) => { if (e.pointerType === "mouse" || e.target === cv || st.hover < 0) return; setHover(-1); };
  document.addEventListener("pointerdown", offTap, true);
  cv.addEventListener("keydown", (e) => {
    if (!st.PL) return; let last = Math.min(st.PL.N - 1, st.lastY);
    // (a year just begun, with no glass in it yet, is not read)
    if (last > 0 && fillOf(last) <= 0) last--;
    let f = st.focus < 0 ? last : st.focus;
    if (e.key === "ArrowLeft" || e.key === "ArrowDown") f = Math.max(0, f - 1); else if (e.key === "ArrowRight" || e.key === "ArrowUp") f = Math.min(last, f + 1);
    else if (e.key === "Home") f = 0; else if (e.key === "End") f = last; else return;
    e.preventDefault(); const old = st.focus; st.focus = f; outlineChanged(old, f);
    live.textContent = speak(f); tipAtPane(f);
  });
  cv.addEventListener("blur", () => { const old = st.focus; st.focus = -1; outlineChanged(old, -1); });

  /* motion: the shimmer runs in the compositor at the setting's speed; "off" stops every moving layer */
  function onMotion() {
    const m = CH.motion(), sp = CH.speed();
    root.classList.toggle("chw-off", m === "off");
    root.style.setProperty("--chw-per", (11 / Math.max(0.35, sp || 1)).toFixed(1) + "s");
    if (m === "off" && st.S) { st.age = st.target; still(); }
    st.all = true; render(m === "off");
  }
  onMotion();
  const refit = () => { cv.fit(); fx.fit(); const X = st.X; if (!X || X.W !== cv._w || X.H !== cv._h || X.k !== cv._k) { rebuild(); if (st.S) render(true); } else st.RL = fitRays(); };
  const offs = [
    CH.frame(draw, root),
    CH.on("resize", () => { cv.fit(); fx.fit(); rebuild(); if (st.S) render(true); }),
    CH.on("motion", onMotion),
  ];
  const ro = "ResizeObserver" in window ? new ResizeObserver(refit) : null;
  if (ro) ro.observe(root);
  return {
    update, skip,
    lighting: () => st.atEnd && st.light !== "lit",
    destroy() { offs.forEach((f) => f && f()); if (ro) ro.disconnect(); document.removeEventListener("pointerdown", offTap, true); root.remove(); },
  };
}
CH.mods.window = { mount };

/* ---------- on the game page: the medallion in the Status panel's crest, the full window in the review ---------- */
let medal = null, medalEl = null, medalLife = null;      // the medallion, its host (kept across the HUD's rebuilds), its life
let end = null, endEl = null, endLife = null;            // the full window at the end, its host in the review, its life
let lastS = null;
// the ink look's chapter plate ("Finis" at the end, shown a moment after the review) covers the screen while it is up:
// the end's light waits for it, and for that moment
const plateUp = () => { const p = document.querySelector(".lk-plate"); return !!(p && !p.hidden); };
// the crest holds their portrait on the left (the ink look) and the medallion on the right; the HUD rebuilds the crest,
// so the same medallion is put back each time. A new life, or a load, gets a new one.
function placeMedal() {
  const box = hudEl.querySelector(".crestbox");
  if (!medalEl) { medalEl = document.createElement("div"); medalEl.className = "hud-medal"; }
  if (box) { box.classList.add("chw-crest"); if (medalEl.parentNode !== box) box.appendChild(medalEl); }
  if (medal && medalLife === CH.life) return;
  if (medal) medal.destroy();
  medal = mount(medalEl, { size: "mini" }); medalLife = CH.life;
  if (lastS && lastS.items === CH.life.items) medal.update(lastS);
}
// the end: the full window where the ink look put their portrait (.lk-final, hidden while the window is there), with
// their name and years beneath it, as the portrait had; the rest of the review stays as it is
function placeEnd(h) {
  if (!h || h.mode !== "over" || reviewEl.hidden) { takeEnd(); return; }
  if (endEl && endEl.parentNode === reviewEl && endLife === CH.life) return;
  takeEnd();
  const L = h.life || {}, r = h.review || {}, fin = reviewEl.querySelector(".lk-final"), head = reviewEl.querySelector(".mh");
  endEl = document.createElement("div"); endEl.className = "chw-end";
  endEl.innerHTML = `<div class="chw-endwin"></div><div class="lk-yrs">${CH.esc(L.name || "")} · ${r.died ? Math.floor(r.died.age) : Math.floor(L.age || 0)} years</div>`;
  if (fin) { fin.classList.add("chw-gone"); const d = fin.style.getPropertyValue("--lk-d"); if (d) endEl.style.setProperty("--lk-d", d); fin.after(endEl); }
  else if (head) head.after(endEl); else reviewEl.prepend(endEl);
  const t0 = performance.now();
  end = mount(endEl.firstElementChild, { size: "full", hold: () => plateUp() || performance.now() - t0 < 600 }); endLife = CH.life;
  if (lastS && lastS.items === CH.life.items) end.update(lastS);
  addEventListener("keydown", onKey, true);
}
function takeEnd() {
  removeEventListener("keydown", onKey, true);
  if (end) end.destroy();
  if (endEl) endEl.remove();
  end = endEl = endLife = null;
  reviewEl.querySelectorAll(".chw-gone").forEach((x) => x.classList.remove("chw-gone"));
}
// skipping the end's light: a click in the review, Space (not on a button) or Esc; never Enter, which starts a new life.
// The key or click that closes a chapter plate, or a key while the Book, the sheet, Help or the World is open, is theirs.
const opened = () => [helpEl, sheetEl, bookEl, worldEl].some((x) => x && !x.hidden);
const skippable = () => !!(end && end.lighting() && !plateUp() && !opened());
function onKey(e) {
  if (e.metaKey || e.ctrlKey || e.altKey || !skippable()) return;
  const t = e.target && e.target.closest ? e.target : null;
  if (e.key === "Escape") skip();
  else if (e.key === " " && !(t && t.closest("button, a, input, textarea, select, [role=button], [role=menuitem], [contenteditable]"))) { e.preventDefault(); skip(); }
}
const onClick = () => { if (skippable()) skip(); };
const skip = () => { end.skip(); if (medal) medal.skip(); };

CH.piece("window", {
  order: 60,
  mount(ctx) {
    if (typeof hudEl === "undefined" || typeof reviewEl === "undefined") return false;
    lastS = ctx.state();
    placeMedal();
    placeEnd(hud);
    reviewEl.addEventListener("click", onClick);
    return true;
  },
  update(S, how) {
    lastS = S;
    if (medalLife !== CH.life) placeMedal();
    medal.update(S);
    if (end && endLife !== CH.life) takeEnd();
    if (end) end.update(S);
    // a life that comes back already over (a load) is shown lit, with no light to play
    if (how && how.quiet && S.over) { medal.skip(); if (end) end.skip(); }
  },
  destroy() {
    takeEnd();
    reviewEl.removeEventListener("click", onClick);
    if (medal) medal.destroy();
    if (medalEl) medalEl.remove();
    hudEl.querySelectorAll(".chw-crest").forEach((x) => x.classList.remove("chw-crest"));
    medal = medalEl = medalLife = lastS = null;
  },
  hooks: {
    renderHud() { placeMedal(); },
    renderReview(h) { placeEnd(h); },
  },
});
})();
