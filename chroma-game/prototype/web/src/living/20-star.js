"use strict";
/* ---------------- the Living HUD: the star (v23 row V2; plan: the Living HUD in v23, step 4) ----------------
   The living star takes the place of the HUD's spider graph (05-hud.js spiderSVG) while the Living HUD is on. Ported from
   the showcase's star.js (frozen 10-18 10:11 UTC): its runtime part, without the concept gallery and its demos.
   One Canvas2D medallion. The geometry is the game's own: five axes at -90, -18, 54, 126 and 198 degrees for W U B R G,
   each point at CH.spR(share) of the radius (0 to 80% of a share onto 0..1, square root), so it reads exactly as today's
   graph does. On it:
     the living star        who they are, as luminous ink fanning from the centre, each color as bright as its share; where
                            they want to be as a ghost star the body strains toward on springs; what holds them as fine
                            tethers to gilt anchors; how fast they could move as the stiffness of those springs; each
                            color's place (in, fading, rising, out). When an outcome lands, the star takes it in: it breathes
                            in as far as the outcome moved them, a ring of ink runs out in the color it turned them toward
                            most, and the orbs it moved flare or draw in.
     afterimages            the star 1, 4 and 10 years ago (S.river), as moonlit outlines and a trail of motes.
     tension threads        two opposed colors both above 15% hum on a string bowed round the color they share as a
                            neighbour; two allies share a calm arc of light between their orbs.
     the breaking point     pent-up wanting (S.dyn.near) glows in the core and, above 0.6, cracks it with light; a
                            breakthrough closes the cracks in gold; a new identity (S.label) shatters the star into its new
                            shape.
     a shadow               a color that casts a shadow has the tip of its point inked and hatched, as today's wheel does
                            (hud.life.shadow, only with the engine's shadows switch on; crosshatched while the state shows).
   Symbol first: nothing here prints a number; every part answers on hover (a color with the page's own tipColor reading).
   On the page (the piece at the end of this file): the star sits over the wheel in .wheelw (svg#hudWheel stays laid out,
   only hidden, as IL.side reads its offsetParent); the wheel's week-by-week motion (animSpider) plays on the star instead,
   and an outcome's motion waits until the outcome is shown; in the everyday interlude the HUD star follows the weeks on
   wide screens, and a small star takes #ilWheel's place on narrow ones (one star on screen at a time); #wKey reads the
   star's key; the voice row's hover runs the voice's ink along the star; a card under the mouse lights its colors' orbs.
   Motion: "full", "calm" (slower, fewer sparks) or "off" (one still frame per change, exactly the data). */
(() => {
const CH = window.CH; if (!CH) return;
const COLORS = CH.COLORS;
const TAU = Math.PI * 2;
const ANG = [-90, -18, 54, 126, 198].map((a) => (a * Math.PI) / 180);   // the game's SPA
const CO = ANG.map(Math.cos), SI = ANG.map(Math.sin);
const BR = COLORS.map((c) => CH.rgb(CH.HUE.bright[c])), PA = COLORS.map((c) => CH.rgb(CH.HUE.pale[c])), DE = COLORS.map((c) => CH.rgb(CH.HUE.deep[c]));
const NIGHT = [12, 9, 30], INK = [14, 10, 28];
const GOLD = [216, 180, 105], GOLD2 = [244, 223, 166], WANTC = [183, 156, 243], WARM = [255, 204, 122], HOT = [255, 244, 214], WHITE = [255, 251, 240];
const AFT = [206, 214, 230];   // A2's afterimages: moonlit silver, apart from the gold of what holds and the lavender of wants
const clamp = CH.clamp;
const rgba = (c, a) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a <= 0 ? 0 : a >= 1 ? 1 : a.toFixed(3)})`;
const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const DIM = DE.map((d) => mix(d, NIGHT, 0.3));   // a minor colour's ink: its deep tone, sunk a little into the night
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeBack = (t) => 1 + 2.2 * Math.pow(t - 1, 3) + 1.2 * Math.pow(t - 1, 2);   // a soft settle with a little overshoot
/* A1, the colour grammar's rule (each effect is as strong as that colour's share), the same for all five colours: how
   much of a colour's bright ink shows. At 10% or less a colour keeps a quarter of its light and its wedge falls back
   toward deep ink; at 35% or more it shines at full strength. So a child spread evenly is softly even, and a life led by
   one colour is a star of that colour. */
const inkK = (v) => 0.25 + 0.75 * CH.smooth(clamp((v - 0.1) / 0.25));
// A2: the five shares at an earlier age from the yearly river rows [age, W, U, B, R, G, ...], interpolated; null before
// the first row (so nothing is drawn before they were born or before the record starts)
function riverW(R, a) {
  if (!R || !R.length || a < 0 || a < R[0][0] - 1e-6) return null;
  let j = 0; while (j < R.length - 1 && R[j + 1][0] <= a) j++;
  const A = R[j], B = R[Math.min(R.length - 1, j + 1)], t = B[0] > A[0] ? clamp((a - A[0]) / (B[0] - A[0])) : 0;
  return [1, 2, 3, 4, 5].map((k) => A[k] + (B[k] - A[k]) * t);
}
// the opposed and the allied pairs of Magic's pie (CH.ENEMY, CH.ALLY), as axis indexes. Two opposed colours always have
// one colour between them that is a neighbour of both (White and Black share Blue): their string bows round it.
const isAlly = (i, j) => { const d = Math.abs(i - j); return d === 1 || d === 4; };
const PAIRS = CH.ENEMY.map(([a, b]) => { const ia = COLORS.indexOf(a), ib = COLORS.indexOf(b);
  return { a: ia, b: ib, foe: true, mid: [0, 1, 2, 3, 4].find((m) => m !== ia && m !== ib && isAlly(ia, m) && isAlly(m, ib)) }; })
  .concat(CH.ALLY.map(([a, b]) => ({ a: COLORS.indexOf(a), b: COLORS.indexOf(b), foe: false })));

/* ---------- the game's words, so every hover reads as today's HUD does: the page's own CIDEA, VALUE and BAND_WORD ---------- */
const IDEA = CIDEA;
// the star's key (#wKey): the wheel's key (05-hud.js SP_KEY) in the star's own symbols, with its afterimages and its core
const STAR_KEY = [["pos", "Now", "Their five colors now, as shares of 100. Each color shines as strongly as its share."],
  ["want", "Wants", "Where their wanting points: the colors they would move to if nothing held them back."],
  ["hold", "Holds", "What holds them where they are: 40% what they notice first, 30% their habits, 30% the titles they have put themselves into."],
  ["pull", "Pull", "The stream of light runs from where they are to where they want to be. It is wider the faster they could change now: how open their age is, times self-control, times their belief they can act that way, times the doors open to them."],
  ["band", "Edge", "The band from 18% to 22%: a color joins who they are above 22% and leaves below 18%. A dashed ring on a color: it is fading, held only by that edge. A bright ring: it is rising toward it."],
  ["after", "Years ago", "The faint silver outlines: their five colors 1, 4 and 10 years ago, so you can see which way they have drifted."],
  ["core", "Wanting", "Pent-up wanting glows in the core, warmer as it builds, and cracks it past 60%. A breakthrough closes the cracks in gold; a new identity shatters the star into its new shape."]];
const WANTING_DEF = "Pent-up wanting: what they were denied builds up. At the mark it breaks through and moves them on its own.";   // 05-hud.js RINGS
// pent-up wanting in words: a pressure, not a score
const nearWord = (n) => (n >= 1 ? "past the mark" : n >= 0.85 ? "close to the mark" : n >= 0.6 ? "straining: the core has cracked" : n >= 0.3 ? "building" : "quiet");
const speedWord = (a) => (a >= 0.5 ? "quickly" : a >= 0.25 ? "readily" : a >= 0.1 ? "slowly" : "hardly at all");
// how far a wanted share lies from the share now, in plain words ("11 points more", "1 point less")
const pts = (d) => { const p = Math.round(Math.abs(d) * 100); return p === 0 ? "the same as now" : `${p} point${p === 1 ? "" : "s"} ${d > 0 ? "more" : "less"}`; };
const pairName = (p) => `${CH.pip(COLORS[p.a])}${CH.pip(COLORS[p.b])} ${CH.NAME[COLORS[p.a]]} and ${CH.NAME[COLORS[p.b]]}`;

/* ---------- sprites: painted once, then stamped (far cheaper than a gradient per frame) ---------- */
const sprites = new Map();
// a soft round glow in one colour (keyed on the colour in steps of 3, so an easing colour does not make a sprite each frame)
function glow(c0) {
  const c = [Math.round(c0[0] / 3) * 3, Math.round(c0[1] / 3) * 3, Math.round(c0[2] / 3) * 3], key = c.join(","); let s = sprites.get(key); if (s) return s;
  if (sprites.size >= 256) sprites.clear();
  s = document.createElement("canvas"); s.width = s.height = 96; const x = s.getContext("2d");
  const g = x.createRadialGradient(48, 48, 0, 48, 48, 48);
  g.addColorStop(0, rgba(c, 1)); g.addColorStop(0.16, rgba(c, 0.72)); g.addColorStop(0.42, rgba(c, 0.2)); g.addColorStop(0.7, rgba(c, 0.05)); g.addColorStop(1, rgba(c, 0));
  x.fillStyle = g; x.fillRect(0, 0, 96, 96); sprites.set(key, s); return s;
}
function stamp(c, sp, x, y, r, a) { if (a <= 0.004 || r <= 0.2) return; c.globalAlpha = Math.min(1, a); c.drawImage(sp, x - r, y - r, 2 * r, 2 * r); }
// A1, a gilt anchor pin with a dark heart (what holds them): a bead of gold lit from the upper left. Radius 16 in a 40 sprite.
let PIN = null;
function pinSprite() {
  if (PIN) return PIN;
  const s = document.createElement("canvas"); s.width = s.height = 40; const x = s.getContext("2d");
  const g = x.createRadialGradient(20 - 5.6, 20 - 6.4, 0, 20, 20, 19.2); g.addColorStop(0, "#fff3cf"); g.addColorStop(0.5, "#d8b469"); g.addColorStop(1, "#6b5020");
  x.fillStyle = g; x.beginPath(); x.arc(20, 20, 16, 0, TAU); x.fill();
  x.strokeStyle = "rgba(42,28,8,0.55)"; x.lineWidth = 1.6; x.stroke();
  x.fillStyle = "rgba(30,20,8,0.8)"; x.beginPath(); x.arc(20, 20, 5.1, 0, TAU); x.fill();
  return (PIN = s);
}

/* ---------- A4: the crack network, grown once from a fixed seed so the same pressure always cracks the same way ----------
   Each crack is a list of points [x, y, r] in units of the star's reach (r = how far from the centre the point lies),
   wandering outward with small turns and sometimes forking. Drawn only as far out as the pressure has spread. */
const CRACKS = (() => {
  const rnd = CH.rng(4127), out = [];
  const grow = (a, x0, y0, len, depth) => {
    const p = [[x0, y0, Math.hypot(x0, y0)]]; let x = x0, y = y0, dx = Math.cos(a), dy = Math.sin(a), d = 0;
    while (d < len) {
      const step = 0.045 + rnd() * 0.05, turn = (rnd() - 0.5) * 0.9, r0 = Math.hypot(x, y) || 1;
      const c = Math.cos(turn), s = Math.sin(turn); let nx = dx * c - dy * s, ny = dx * s + dy * c;
      nx = nx * 0.78 + (x / r0) * 0.22; ny = ny * 0.78 + (y / r0) * 0.22; const nl = Math.hypot(nx, ny); dx = nx / nl; dy = ny / nl;   // keep heading outward
      x += dx * step; y += dy * step; d += step; p.push([x, y, Math.hypot(x, y)]);
      if (depth < 2 && rnd() < 0.2 && d > 0.15) grow(Math.atan2(dy, dx) + (rnd() < 0.5 ? -1 : 1) * (0.45 + rnd() * 0.4), x, y, (len - d) * (0.3 + rnd() * 0.3), depth + 1);
    }
    out.push({ p, depth: Math.min(1, depth) });
  };
  for (let k = 0; k < 7; k++) { const a = -Math.PI / 2 + (k / 7) * TAU + (rnd() - 0.5) * 0.5; grow(a, Math.cos(a) * 0.035, Math.sin(a) * 0.035, 1.1, 0); }
  return out;
})();

/* ---------- A4: the shards of a breakthrough, cut once from a fixed seed ----------
   A shard is a polygon whose corners sit in star coordinates [u, f]: u runs round the outline (0 at White's point, 1 at
   Blue's, ... 5 back at White) and f from the centre (0) to the outline (1), so the same shard sits in the old shape
   and in the new one. Seven jagged cuts run out from the centre; a jagged ring at about 40% cuts off seven small inner
   shards, and a second ring at about 72% splits some of the outer ones, so the pieces grow larger toward the rim
   (about eighteen in all), irregular like breaking glass. */
const SHARDS = (() => {
  const rnd = CH.rng(2203), NL = 7, stp = 5 / NL, u0 = rnd() * stp, out = [];
  const L = [...Array(NL)].map((_, k) => { const u = u0 + (k + (rnd() - 0.5) * 0.35) * stp;
    return { a: [u + (rnd() - 0.5) * 0.16, 0.34 + rnd() * 0.12], b: [u + (rnd() - 0.5) * 0.24, 0.66 + rnd() * 0.12], c: [u + (rnd() - 0.5) * 0.3, 1] }; });
  const add = (v) => out.push({ v, d: v.reduce((t, q) => t + q[1], 0) / v.length, burst: 0.6 + rnd() * 0.7, rot: (rnd() - 0.5) * 1.1, lag: rnd() * 0.06 });
  const mid = (p, q, j) => [(p[0] + q[0]) / 2 + (rnd() - 0.5) * 0.1, (p[1] + q[1]) / 2 + (rnd() - 0.5) * j];
  for (let k = 0; k < NL; k++) {
    const A = L[k], B0 = L[(k + 1) % NL], w = k === NL - 1 ? 5 : 0;
    const B = { a: [B0.a[0] + w, B0.a[1]], b: [B0.b[0] + w, B0.b[1]], c: [B0.c[0] + w, 1] };
    const r40 = mid(A.a, B.a, 0.08);
    add([[0, 0], A.a, r40, B.a]);   // the small inner shard of this sector
    const rim = []; for (let u = Math.floor(A.c[0]) + 1; u < B.c[0]; u++) rim.push([u, 1]);   // the star's corners on this stretch of the rim
    if (rnd() < 0.6) { const r72 = mid(A.b, B.b, 0.1); add([A.a, A.b, r72, B.b, B.a, r40]); add([A.b, A.c, ...rim, B.c, B.b, r72]); }
    else add([A.a, A.b, A.c, ...rim, B.c, B.b, B.a, r40]);
  }
  return out;
})();

let uid = 0;

/* ======================================================================================================================
   mount(host, opts): one star in host. opts.size "full" | "mini"; opts.frame "glass" (its own night-glass medallion) or
   "none"; opts.listen false to ignore the page's "outcome" events; opts.tipL() returns the life whose numbers a color's hover
   reads with the page's tipColor (else the star's own reading of what it draws). */
function mount(host, opts) {
  opts = opts || {};
  const id = ++uid;
  const mini = opts.size === "mini";
  const lay = { after: true, threads: true, core: true, flows: true, tethers: true, ghost: true };
  const glass = opts.frame !== "none";

  const root = document.createElement("div");
  root.className = "chs-star" + (mini ? " mini" : "") + (glass ? " glass" : "");
  host.appendChild(root);
  const bg = CH.canvas(root, "st-bg");   // the medallion, painted once per size
  const cv = CH.canvas(root, "st-cv");   // the star, drawn each frame
  const ctx = cv.getContext("2d");
  if (!ctx) { root.remove(); throw new Error("no 2D canvas"); }
  cv.setAttribute("role", "img");
  cv.setAttribute("aria-label", "The five colors as a star");
  // the five orbs at the axis ends carry the game's color glyphs; they are real elements, so they take focus and hover
  const orbBox = document.createElement("div"); orbBox.className = "st-orbs"; root.appendChild(orbBox);
  const orbs = COLORS.map((c, i) => {
    const o = document.createElement("span"); o.className = "st-orb"; o.dataset.c = c; o.tabIndex = mini ? -1 : 0;
    o.setAttribute("role", "img"); o.setAttribute("aria-label", CH.NAME[c]);
    o.innerHTML = CH.glyph(c); orbBox.appendChild(o);
    CH.tip(o, () => colorTip(i));
    o.addEventListener("pointerenter", () => setHover({ k: "pt", i })); o.addEventListener("pointerleave", () => setHover(null));
    o.addEventListener("focus", () => setHover({ k: "pt", i })); o.addEventListener("blur", () => setHover(null));
    return o;
  });

  /* the root is a square as large as the host allows (its size comes from the page), in layout pixels: the page may show
     the screen under a CSS scale, which the canvases already take into account (CH.canvas), so measuring the scaled box
     here would shrink the star twice. A host with no layout (not attached yet, or in a hidden panel) is left alone: the
     star keeps its size until the host has one. */
  const fitRoot = () => {
    if (!host.isConnected) return;
    const w = host.offsetWidth, hh = host.offsetHeight; if (!w) return;
    const s = Math.max(60, Math.floor(Math.min(w, hh > 24 ? hh : w)));
    if (root._s !== s) { root._s = s; root.style.width = root.style.height = s + "px"; cv.fit(); bg.fit(); dirty = true; }
  };
  let dirty = true;
  const ro = "ResizeObserver" in window ? new ResizeObserver(fitRoot) : null;
  if (ro) ro.observe(host);
  fitRoot();

  /* ---------- the state: st holds the data's targets, D what is drawn (eased and sprung toward st) ----------
     The shape (w, want, bands, label) comes from the latest state, or, while the star follows something else, from that:
     the wheel's weekly frames after a state (play), the interlude's weeks (follow and frame). The rest (holds, speed,
     pent-up wanting, the ink, the afterimages, the shadow) always comes from the latest state, st.S. */
  const st = { has: false, w: [0.2, 0.2, 0.2, 0.2, 0.2], want: [0.2, 0.2, 0.2, 0.2, 0.2], hold: [0.2, 0.2, 0.2, 0.2, 0.2], acc: [], bands: [], label: "", near: 0, wet: 0.5,
    tx: [], twx: [], thx: [0, 0, 0, 0, 0], T: [0, 0, 0, 0, 0], after: [null, null, null], S: null, age: 0, nb: 0, life: null, bts: [], seen: 0, items: null,
    shadow: null, voice: null, ends: [] };
  const D = { x: [0.05, 0.05, 0.05, 0.05, 0.05], v: [0, 0, 0, 0, 0], xw: [0, 0, 0, 0, 0], vw: [0, 0, 0, 0, 0], xh: [0, 0, 0, 0, 0], vh: [0, 0, 0, 0, 0],
    T: [0, 0, 0, 0, 0], near: 0, wet: 0.5, wc: [0.2, 0.2, 0.2, 0.2, 0.2], band: COLORS.map(() => [0, 0, 0, 1]), pair: PAIRS.map(() => 0),
    ae: [null, null, null], aa: [0, 0, 0], sh: [0, 0, 0, 0, 0] };
  const BI = { in: 0, fading: 1, rising: 2, out: 3 };
  // this star's own drawing state for each pair (its cached gradient, the bow or arc it drew last, for hover)
  const PS = PAIRS.map(() => ({ g: null, bow: null, ra: 0 }));
  // A3: a pair shows once both colours pass 15%, faint at first and full once the smaller of the two reaches about 28%
  const pairOn = (p) => { const m = Math.min(st.w[p.a], st.w[p.b]); return m > 0.15 ? 0.1 + 0.9 * CH.smooth(clamp((m - 0.15) / 0.13)) : 0; };
  let hover = null, sparks = [], flows = [], shat = null, rel = null, breath = null, tt = 0, lastRes = null, lastResAt = 0, spawnAcc = [0, 0, 0, 0, 0];
  let tl = null, following = false, lastShatter = -1e9, orbKey = "";

  // each colour's place (in, fading, rising, out): the game's bands, or worked out from the label when a state has none
  function bandsFrom(w, label, bands) {
    if (bands && bands.length === 5 && bands.every(Boolean)) return bands.slice();
    const ls = CH.lettersOf(label);
    return w.map((v, i) => (ls.includes(COLORS[i]) ? (v <= CH.IDENT.enter ? "fading" : "in") : v > CH.IDENT.leave ? "rising" : "out"));
  }
  const bandsOf = (S) => bandsFrom(S.w, S.label, S.dyn && S.dyn.bands);
  // part of who they are now: the bands say so ("in", or "fading" while the edge still holds it). The name they go by
  // (S.label) can lag the bands for a while; the orb, the Place row and the tip's last line all follow the bands.
  const inId = (i) => st.bands[i] === "in" || st.bands[i] === "fading";
  // A2: the shape at an earlier age, in radius units
  const shapeAt = (S, a) => { const w = riverW(S.river, a); return w ? w.map(CH.spR) : null; };
  // A1, the tethers: how hard what holds them pulls against what they want. Taut only when the anchor lies on the other
  // side of the point from the wanted place (their habits, lens and titles pull back while their wanting pulls on)
  const taut = () => { st.T = st.tx.map((x, i) => { const dW = st.twx[i] - x, dH = st.thx[i] - x; return clamp(Math.sqrt(Math.max(0, -dW * dH)) / 0.07); }); };
  // the orbs' place and names follow the bands (written only when they change: the interlude sets the shape each frame)
  function orbsOn() {
    const k = st.bands.join() + "|" + st.label; if (k === orbKey) return; orbKey = k;
    orbs.forEach((o, i) => { o.classList.toggle("on", inId(i)); o.setAttribute("aria-label", `${CH.NAME[COLORS[i]]}: ${placeWord(i)}`); });
  }
  /* the shape: where they are, where they want to be, each color's place and the name they go by. A new name shatters the
     star into its new shape (A4) unless told quiet; a name that flickers week by week breaks it once in 1.5 s at most. */
  function shape(w, want, bands, label, loud) {
    const was = st.label;
    st.w = w.slice(); st.want = (want || w).slice(); st.bands = bandsFrom(st.w, label, bands); st.label = label || "";
    st.tx = st.w.map(CH.spR); st.twx = st.want.map(CH.spR); taut();
    if (loud && st.has && was !== st.label && lay.core && CH.motion() !== "off" && tt - lastShatter > 1.5) { lastShatter = tt; shatter(); }
    orbsOn(); dirty = true;
    return was !== st.label;
  }
  // A4: the breakthroughs lived so far (story lines tagged "breakthrough"), counted as the story grows; a new life's (or a
  // load's) new array is counted again
  function breakthroughs(S) {
    const I = S.items || [];
    if (I !== st.items || I.length < st.seen) { st.items = I; st.seen = 0; st.bts = []; }
    for (; st.seen < I.length; st.seen++) if (I[st.seen] && I[st.seen].tag === "breakthrough") st.bts.push(I[st.seen]);
    return st.bts;
  }

  /* update(S, o): a new state. o.quiet: take it without an arrival (no kindling, no shatter, no breakthrough): the update
     after a load, the years before the player takes over, the Living HUD turned on. A new life (CH.life) starts afresh. */
  function update(S, o) {
    if (!S || !S.w) return;
    const quiet = !!(o && o.quiet), first = !st.has || st.life !== CH.life;
    const prevAge = st.age, prevNb = st.nb, prevNear = st.near, prevW = st.w, nearShown = D.near, prevLabel = st.label;
    if (first) st.has = false;
    st.S = S; st.life = CH.life;
    st.hold = (S.hold || S.w).slice(); st.thx = st.hold.map(CH.spR);
    st.acc = (S.acc || [0.15, 0.15, 0.15, 0.15, 0.15]).slice();
    st.near = S.dyn && typeof S.dyn.near === "number" ? Math.max(0, S.dyn.near) : 0;
    st.wet = typeof S.wet === "number" ? S.wet : 0.5;
    st.after = [1, 4, 10].map((k) => shapeAt(S, S.age - k));
    st.age = S.age || 0;
    st.shadow = S.shadow && S.shadow.cols ? S.shadow.cols.map((x) => (x && x.show ? [x.part, !!x.on] : null)) : null;
    const bts = breakthroughs(S); st.nb = bts.length;
    // the shape follows the state unless the star follows the weeks (the interlude) or the wheel's frames are playing
    if (first || !(following || tl)) shape(S.w, S.want, S.dyn && S.dyn.bands, S.label, false); else taut();
    if (first) {   // the first state: the star kindles from its centre (or simply appears: quiet, or motion off)
      D.xw = st.twx.slice(); D.xh = st.thx.slice(); D.T = st.T.slice(); D.near = st.near; D.wet = st.wet; D.wc = st.w.slice();
      D.band = st.bands.map((b) => [0, 1, 2, 3].map((k) => (BI[b] === k ? 1 : 0)));
      D.pair = PAIRS.map((p) => pairOn(p));
      D.ae = st.after.map((a) => (a ? a.slice() : null)); D.aa = st.after.map((a) => (a ? 1 : 0));
      D.sh = COLORS.map((_, i) => (st.shadow && st.shadow[i] ? 1 : 0));
      if (quiet || CH.motion() === "off") { D.x = st.tx.slice(); D.v = [0, 0, 0, 0, 0]; }
      sparks = []; flows = []; shat = null; rel = null; breath = null; tl = null;
    } else if (lay.core && !quiet && CH.motion() !== "off") {
      // A4: who they are changed: the star shatters and settles into its new shape. Or, with the same name, the wanting
      // broke through (a new "breakthrough" line, or the pressure falling from past the mark): a lighter release.
      if (prevLabel !== st.label && tt - lastShatter > 1.5) { lastShatter = tt; shatter(); }
      else if (prevLabel === st.label && st.age >= prevAge && (st.nb > prevNb || (prevNear >= 1 && st.near < 0.5))) release(bts.slice(prevNb), prevW, Math.max(prevNear, nearShown));
    }
    st.has = true; dirty = true;
    cv.setAttribute("aria-label", `The five colors: ${COLORS.map((c, i) => `${CH.NAME[c]} ${CH.pct(S.w[i])}`).join(", ")}. ${CH.guild(S)}.`);
    // an outcome reaching this state by the page's "outcome" event is handled by its listener (flow and breathe)
  }

  /* ---------- the wheel's motion: the page's weekly frames ({t, w, want, bands, label}, 05-hud.js frameOf) ----------
     play(frames, ms, wait): the shape runs through the frames over ms, as the wheel would have (animSpider); wait holds it
     at the first frame until go() (an outcome: until it is shown) or wait ms at most. Motion off: straight to the last.
     follow(true) and frame(f): the interlude's weeks set the shape; follow(false) gives it back to the latest state. */
  function frameShape(f, loud) { if (f && f.w) shape(f.w, f.want, f.bands, f.label != null ? f.label : st.label, loud); }
  function play(fs, ms, wait) {
    if (!fs || !fs.length) return;
    if (fs.length < 2 || CH.motion() === "off") { tl = null; return toState(); }
    tl = { fs, ms: Math.max(1, ms), t0: wait ? Infinity : performance.now(), until: performance.now() + (wait || 0) };
    frameShape(fs[0], false);
  }
  const go = () => { if (tl && tl.t0 === Infinity) tl.t0 = performance.now(); };
  function tick(now) {
    if (!tl) return;
    if (tl.t0 === Infinity) { if (now < tl.until) return; tl.t0 = now; }
    const u = (now - tl.t0) / tl.ms, n = tl.fs.length;
    if (u >= 1) { tl = null; toState(); return; }
    const x = clamp(u) * (n - 1), k = Math.min(n - 2, Math.floor(x)), f = x - k, A = tl.fs[k], B = tl.fs[k + 1], lerp = (a, b) => a.map((v, i) => v + ((b[i] ?? v) - v) * f);
    const C = f < 0.5 ? A : B;
    shape(lerp(A.w, B.w), lerp(A.want || A.w, B.want || B.w), C.bands, C.label != null ? C.label : st.label, true);
  }
  // the shape back to the latest state (at the end of the frames, or of the interlude)
  function toState() { const S = st.S; if (S && !following && !tl) shape(S.w, S.want, S.dyn && S.dyn.bands, S.label, true); }
  function follow(on) { if (following === !!on) return; following = !!on; if (on) tl = null; else toState(); }

/* ---------- the physics: springs, eases and sparks, stepped in small fixed steps ---------- */
  function lean(i, t) {
    // A1: the body strains toward what it wants: each point leans a little toward its wanted place and back, like
    // breathing, less where a taut tether holds it. Never further than 30% of the way, so the shape stays true.
    return 0.3 * (st.twx[i] - st.tx[i]) * (1 - 0.6 * D.T[i]) * (0.5 + 0.5 * Math.sin(t * 0.9 + i * 1.7));
  }
  function step(dt, t, calm) {
    const n = Math.max(1, Math.ceil(dt / (1 / 120))), h = dt / n;
    for (let s = 0; s < n; s++) for (let i = 0; i < 5; i++) {
      // the point: a spring whose stiffness is how fast they could move now (S.acc); moving toward what they want it is
      // lightly damped and overshoots a little, moving back it is heavily damped (it does not want to go there)
      const tgt = st.tx[i] + lean(i, t), K = 55 + 520 * clamp(st.acc[i] / 0.5);
      const toward = D.v[i] * (st.twx[i] - st.tx[i]) > 0, C = 2 * (toward ? 0.4 : 0.95) * Math.sqrt(K);
      D.v[i] += (K * (tgt - D.x[i]) - C * D.v[i]) * h; D.x[i] += D.v[i] * h;
      // the ghost star and the anchors follow critically damped, a touch slower
      D.vw[i] += (90 * (st.twx[i] - D.xw[i]) - 19 * D.vw[i]) * h; D.xw[i] += D.vw[i] * h;
      D.vh[i] += (90 * (st.thx[i] - D.xh[i]) - 19 * D.vh[i]) * h; D.xh[i] += D.vh[i] * h;
    }
    const e = 1 - Math.exp(-dt / 0.3), e2 = 1 - Math.exp(-dt / 0.45);
    D.near += (st.near - D.near) * e; D.wet += (st.wet - D.wet) * e2;
    for (let i = 0; i < 5; i++) {
      D.T[i] += (st.T[i] - D.T[i]) * e; D.wc[i] += (st.w[i] - D.wc[i]) * e;
      D.sh[i] += ((st.shadow && st.shadow[i] ? 1 : 0) - D.sh[i]) * e;
      const b = BI[st.bands[i]] ?? 3; for (let k = 0; k < 4; k++) D.band[i][k] += ((k === b ? 1 : 0) - D.band[i][k]) * e;
    }
    PAIRS.forEach((p, j) => { D.pair[j] += (pairOn(p) - D.pair[j]) * e; });
    for (let k = 0; k < 3; k++) {
      const a = st.after[k];
      if (a) { if (!D.ae[k]) D.ae[k] = a.slice(); for (let i = 0; i < 5; i++) D.ae[k][i] += (a[i] - D.ae[k][i]) * e; }
      D.aa[k] += ((a ? 1 : 0) - D.aa[k]) * e;
    }
    // A1, rising colours kindle: tiny sparks leave the point and drift up and out (fewer when calm)
    const tdt = dt * (calm ? 0.35 : 1);
    for (let i = 0; i < 5; i++) {
      const r = D.band[i][2]; if (r < 0.3 || mini && sparks.length > 14) continue;
      spawnAcc[i] += tdt * (calm ? 3.5 : 7) * r * (mini ? 0.5 : 1);
      while (spawnAcc[i] >= 1) { spawnAcc[i] -= 1; spawnSpark(i); }
    }
    sparks = sparks.filter((p) => (p.age += tdt) < p.life);
    for (const p of sparks) { p.vy -= 16 * G.sc * tdt; p.vx *= 1 - 1.2 * tdt; p.vy *= 1 - 0.6 * tdt; p.x += p.vx * tdt; p.y += p.vy * tdt; }
  }
  const srnd = CH.rng(77 + id);
  function spawnSpark(i) {
    if (!G.P || sparks.length > 60) return;
    const [x, y] = G.P[i], sp = (12 + 26 * srnd()) * G.sc, pr = (srnd() - 0.5) * 16 * G.sc;
    sparks.push({ i, x: x + (srnd() - 0.5) * 3, y: y + (srnd() - 0.5) * 3, vx: CO[i] * sp - SI[i] * pr, vy: SI[i] * sp + CO[i] * pr - 8 * G.sc, age: 0, life: 0.6 + srnd() * 0.8, r: (0.8 + srnd() * 1.0) * G.sc });
  }
  function snap() {   // motion off: everything exactly at the data
    D.x = st.tx.slice(); D.v = [0, 0, 0, 0, 0]; D.xw = st.twx.slice(); D.xh = st.thx.slice(); D.T = st.T.slice(); D.near = st.near; D.wet = st.wet; D.wc = st.w.slice();
    D.band = st.bands.map((b) => [0, 1, 2, 3].map((k) => (BI[b] === k ? 1 : 0)));
    D.pair = PAIRS.map((p) => pairOn(p));
    D.ae = st.after.map((a, k) => (a ? a.slice() : D.ae[k])); D.aa = st.after.map((a) => (a ? 1 : 0));
    D.sh = COLORS.map((_, i) => (st.shadow && st.shadow[i] ? 1 : 0));
    sparks = []; flows = []; shat = null; rel = null; breath = null;
  }
  // when nothing moves but the breathing (springs settled, no sparks, flows, outcome, breakthrough or hover), the loop draws at 30 fps
  function idle() {
    if (sparks.length || flows.length || shat || rel || breath || hover || tl || following) return false;
    for (let i = 0; i < 5; i++) if (Math.abs(D.x[i] - st.tx[i]) > 0.035 || Math.abs(D.v[i]) > 0.06 || Math.abs(D.wc[i] - st.w[i]) > 0.002 || Math.abs(D.xw[i] - st.twx[i]) > 0.003) return false;
    return Math.abs(D.near - st.near) < 0.005 && Math.abs(D.wet - st.wet) < 0.005;
  }

  /* ---------- geometry and the painted-once layers ---------- */
  const G = { s: 0 };
  function layout() {
    const w = cv._w || 0, h = cv._h || 0, s = Math.min(w, h);
    if (s < 20) return false;
    if (G.s === s && G.pw === cv.width && G.ph === cv.height) return true;
    Object.assign(G, { s, w, h, pw: cv.width, ph: cv.height, k: cv._k || 1, cx: w / 2, cy: h / 2 });
    G.R = s * (mini ? 0.32 : 0.33);                  // the star's reach: a share of 80% (the game's SPR)
    G.orbR = s * (mini ? 0.365 : 0.405);             // the orbs ride just outside it, inside the well's rim
    G.od = mini ? s * 0.118 : Math.max(12, s * 0.085);   // orb diameter
    G.sc = clamp(s / 300, 0.42, 1.8);                // line widths and glow sizes scale with the medallion
    G.disc = s * 0.488;
    G.rr = G.od / 2 + 2.5 + 2.2 * G.sc;              // the rising and fading rings, clear of the orb and its dark rim
    G.arcR = G.orbR - G.od / 2 - (mini ? 2 : 4) * G.sc;   // A3: the allies' arcs run just inside the ring of orbs
    G.O = ANG.map((a, i) => [G.cx + G.orbR * CO[i], G.cy + G.orbR * SI[i]]);
    root.style.setProperty("--od", G.od.toFixed(1) + "px");
    orbs.forEach((o, i) => { o.style.left = G.O[i][0].toFixed(1) + "px"; o.style.top = G.O[i][1].toFixed(1) + "px"; });
    // the identity edge (18% to 22%) as a ring, for brightening on hover
    G.band = new Path2D(); G.band.arc(G.cx, G.cy, G.R * CH.spR(CH.IDENT.enter), 0, TAU); G.band.arc(G.cx, G.cy, G.R * CH.spR(CH.IDENT.leave), 0, TAU, true);
    paintBack(); paintEngraving(); paintHi(); paintPairs(); paintPulls();
    G.wk = null; G.hk = null; refreshInk();
    return true;
  }
  /* A1: the body's ink, rebuilt only when a share moves by half a point or more (never per frame). The five colours fan from
     the centre as one conic sweep, each at its own axis as bright as its share (inkK); the heart is the same sweep in deep
     ink, where a colour that leads them stays deep and saturated and a small one falls back to night. */
  function refreshInk() {
    const w = D.wc; if (G.wk && w.every((v, i) => Math.abs(v - G.wk[i]) < 0.005)) return;
    G.wk = w.slice(); const K = w.map(inkK);
    G.inkK = K; G.ink = K.map((k, i) => mix(DIM[i], BR[i], k));
    G.conic = conicOf(G.ink, w);
    // the deep heart under it moves too little to see within a point and a half (and each new heart is filled again
    // where it is first copied)
    if (!G.hk || !G.heart || w.some((v, i) => Math.abs(v - G.hk[i]) >= 0.015)) { G.hk = w.slice(); paintHeart(K, w); }
  }
  /* the fan as one conic sweep: each colour pure at its own axis, and between two neighbours the blend sits nearer the
     weaker one, so a colour that leads them spreads across more of the star (the same rule for every pair) */
  const blendAt = (w, i, j) => clamp(0.5 + 1.1 * (w[i] - w[j]) / Math.max(1e-3, w[i] + w[j]), 0.18, 0.82);
  function conicOf(cols, w, x) {
    x = x || ctx; if (!x.createConicGradient) return null;
    const g = x.createConicGradient(ANG[0], G.cx, G.cy);
    for (let i = 0; i < 5; i++) { const j = (i + 1) % 5; g.addColorStop(i / 5, rgba(cols[i], 1)); g.addColorStop((i + blendAt(w, i, j)) / 5, rgba(mix(cols[i], cols[j], 0.5), 1)); }
    g.addColorStop(1, rgba(cols[0], 1));
    return g;
  }
  // A3's cached gradients: an allied arc runs from one colour to the other and fades out under the orbs; an opposed string
  // runs from one colour to the other across the 144 degrees round the colour between them
  function paintPairs() {
    PAIRS.forEach((p, j) => {
      const q = PS[j]; q.g = null; if (!ctx.createConicGradient) return;
      if (!p.foe) {   // allies are neighbours: from a's axis to b's axis is always a fifth of a turn clockwise
        const g = ctx.createConicGradient(ANG[p.a], G.cx, G.cy);
        g.addColorStop(0, rgba(BR[p.a], 0)); g.addColorStop(0.045, rgba(BR[p.a], 1)); g.addColorStop(0.155, rgba(BR[p.b], 1)); g.addColorStop(0.2, rgba(BR[p.b], 0)); g.addColorStop(1, rgba(BR[p.a], 0));
        q.g = g; return;
      }
      const cw = (p.mid - p.a + 5) % 5 === 1, s = cw ? p.a : p.b, e = cw ? p.b : p.a, g = ctx.createConicGradient(ANG[s], G.cx, G.cy);
      g.addColorStop(0, rgba(BR[s], 1)); g.addColorStop(0.4, rgba(BR[e], 1)); g.addColorStop(0.7, rgba(BR[e], 1)); g.addColorStop(0.85, rgba(BR[s], 1)); g.addColorStop(1, rgba(BR[s], 1));
      q.g = g;
    });
  }
  // A1, the pull: one horizontal gradient per colour, drawn in the wedge's own frame (so no gradient is made per frame)
  function paintPulls() {
    G.pullG = BR.map((b) => { const g = ctx.createLinearGradient(0, 0, 1, 0); g.addColorStop(0, rgba(mix(b, WHITE, 0.2), 0.75)); g.addColorStop(0.7, rgba(b, 0.3)); g.addColorStop(1, rgba(b, 0.04)); return g; });
  }
  // the light that travels slowly round the rim, as on cut glass when the head turns: one ring of light painted once, turned
  // each frame by its pattern's transform
  const HM = typeof DOMMatrix === "function" ? new DOMMatrix() : null;
  function paintHi() {
    G.hiPat = null; if (mini || !HM || !ctx.createConicGradient) return;
    const n = Math.ceil(2 * (G.R * 1.08 + 14 * G.sc) * G.k), s = document.createElement("canvas"); s.width = s.height = n;
    const x = s.getContext("2d"), g = x.createConicGradient(0, n / 2, n / 2);
    g.addColorStop(0, "rgba(255,250,236,0)"); g.addColorStop(0.06, "rgba(255,250,236,0.9)"); g.addColorStop(0.14, "rgba(255,250,236,0)");
    g.addColorStop(0.5, "rgba(255,250,236,0)"); g.addColorStop(0.56, "rgba(255,250,236,0.4)"); g.addColorStop(0.62, "rgba(255,250,236,0)"); g.addColorStop(1, "rgba(255,250,236,0)");
    x.fillStyle = g; x.fillRect(0, 0, n, n);
    const p = ctx.createPattern(s, "no-repeat"); if (p && p.setTransform) { G.hiPat = p; G.hiN = n; }
  }
  function turnHi(a) {
    const c = Math.cos(a), s = Math.sin(a), h = G.hiN / 2, k = G.k;
    HM.a = c / k; HM.b = s / k; HM.c = -s / k; HM.d = c / k; HM.e = G.cx - (c * h - s * h) / k; HM.f = G.cy - (s * h + c * h) / k;
    G.hiPat.setTransform(HM);
  }
  // the medallion: night glass with a faint nebula and dust, the game's two guide rings, the five axes, the identity
  // edge (the band from 18% to 22%) and, when the host is not a well already, a gilt bezel. Painted once per size.
  function paintBack() {
    if (bg.width !== G.pw || bg.height !== G.ph) { bg.width = G.pw; bg.height = G.ph; }
    const x = bg.getContext("2d"); x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, bg.width, bg.height); x.setTransform(G.k, 0, 0, G.k, 0, 0);
    const { cx, cy, R, s, sc } = G, rd = G.disc;
    x.save(); x.beginPath(); x.arc(cx, cy, glass ? rd : s * 0.47, 0, TAU); x.clip();
    if (glass) {
      const g = x.createRadialGradient(cx, cy - s * 0.05, 0, cx, cy, rd);
      g.addColorStop(0, "#1e1a42"); g.addColorStop(0.55, "#120f28"); g.addColorStop(1, "#07060e");
      x.fillStyle = g; x.fillRect(0, 0, G.w, G.h);
    }
    // a faint nebula in the glass: seeded noise, violet and a little gold, painted small and smoothed up
    const n = 72, nb = document.createElement("canvas"); nb.width = nb.height = n; const nx = nb.getContext("2d"), im = nx.createImageData(n, n);
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const v = CH.fbm(i / 15 + 3.1, j / 15 + 7.7, 4), u = CH.fbm(i / 9 + 11, j / 9 + 2, 3), o = (j * n + i) * 4;
      const a = Math.pow(clamp((v - 0.42) * 2.4), 2) * 0.55;
      im.data[o] = 120 + 90 * u; im.data[o + 1] = 96 + 70 * u; im.data[o + 2] = 210 - 60 * u; im.data[o + 3] = a * 255;
    }
    nx.putImageData(im, 0, 0);
    x.globalAlpha = glass ? 0.22 : 0.16; x.imageSmoothingQuality = "high"; x.drawImage(nb, cx - rd, cy - rd, rd * 2, rd * 2); x.globalAlpha = 1;
    // dust: seeded specks, a few with a soft halo
    const rnd = CH.rng(9001);
    for (let k = 0; k < (mini ? 26 : 60); k++) {
      const a = rnd() * TAU, r = Math.sqrt(rnd()) * rd * 0.96, px = cx + Math.cos(a) * r, py = cy + Math.sin(a) * r, b = rnd();
      x.fillStyle = rgba(b > 0.7 ? GOLD2 : [210, 200, 255], 0.18 + 0.4 * b * b);
      x.beginPath(); x.arc(px, py, (0.35 + b * 0.55) * sc, 0, TAU); x.fill();
      if (b > 0.93) { x.globalAlpha = 0.25; x.drawImage(glow([220, 210, 255]), px - 5 * sc, py - 5 * sc, 10 * sc, 10 * sc); x.globalAlpha = 1; }
    }
    // the guide rings at 40% and 80% (the game's), as engraved gilt hairlines, and the five axes fading outward
    x.lineWidth = Math.max(0.6, 0.7 * sc);
    for (const v of [0.4, 0.8]) { x.strokeStyle = rgba(GOLD, v === 0.8 ? 0.16 : 0.1); x.beginPath(); x.arc(cx, cy, R * CH.spR(v), 0, TAU); x.stroke(); }
    for (let i = 0; i < 5; i++) {
      const g = x.createLinearGradient(cx, cy, cx + CO[i] * G.orbR, cy + SI[i] * G.orbR);
      g.addColorStop(0, rgba(GOLD, 0.02)); g.addColorStop(0.5, rgba(GOLD, 0.13)); g.addColorStop(1, rgba(GOLD, 0.05));
      x.strokeStyle = g; x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx + CO[i] * (G.orbR - G.od * 0.55), cy + SI[i] * (G.orbR - G.od * 0.55)); x.stroke();
    }
    // A1, the identity edge: one soft gilt band from 18% to 22%, its outer rim (where a colour joins) engraved
    const r2 = R * CH.spR(CH.IDENT.enter);
    x.fillStyle = rgba(GOLD2, 0.05); x.fill(G.band, "evenodd");
    x.lineWidth = Math.max(0.45, 0.55 * sc); x.strokeStyle = rgba(GOLD2, 0.15); x.beginPath(); x.arc(cx, cy, r2, 0, TAU); x.stroke();
    // the rim of the glass darkens (a vignette), so the light gathers in the middle
    const vg = x.createRadialGradient(cx, cy, rd * 0.62, cx, cy, rd);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, glass ? "rgba(0,0,0,0.55)" : "rgba(0,0,0,0.25)");
    x.fillStyle = vg; x.fillRect(0, 0, G.w, G.h);
    x.restore();
    if (glass) {   // the gilt bezel: two hairlines, minute ticks and a notch at each axis
      const bz = x.createLinearGradient(cx - rd, cy - rd, cx + rd, cy + rd);
      bz.addColorStop(0, "#f4dfa6"); bz.addColorStop(0.35, "#8a6a2c"); bz.addColorStop(0.6, "#d8b469"); bz.addColorStop(1, "#5a4418");
      x.strokeStyle = bz; x.lineWidth = Math.max(1, 1.6 * sc); x.beginPath(); x.arc(cx, cy, rd - 0.8 * sc, 0, TAU); x.stroke();
      x.lineWidth = Math.max(0.5, 0.6 * sc); x.globalAlpha = 0.6; x.beginPath(); x.arc(cx, cy, rd - 4.2 * sc, 0, TAU); x.stroke();
      x.globalAlpha = 0.45;
      for (let k = 0; k < 60; k++) { const a = ANG[0] + (k / 60) * TAU, l = k % 12 === 0 ? 0 : k % 3 === 0 ? 2.6 : 1.4;
        if (!l) continue; x.beginPath(); x.moveTo(cx + Math.cos(a) * (rd - 4.2 * sc), cy + Math.sin(a) * (rd - 4.2 * sc)); x.lineTo(cx + Math.cos(a) * (rd - (4.2 + l) * sc), cy + Math.sin(a) * (rd - (4.2 + l) * sc)); x.stroke(); }
      x.globalAlpha = 1; x.fillStyle = "#e7c982";
      for (let i = 0; i < 5; i++) { const a = ANG[i], r = rd - 2.4 * sc, d = 2.2 * sc; x.beginPath();
        x.moveTo(cx + Math.cos(a) * (r + d), cy + Math.sin(a) * (r + d)); x.lineTo(cx + Math.cos(a + 0.03) * r, cy + Math.sin(a + 0.03) * r);
        x.lineTo(cx + Math.cos(a) * (r - d * 1.6), cy + Math.sin(a) * (r - d * 1.6)); x.lineTo(cx + Math.cos(a - 0.03) * r, cy + Math.sin(a - 0.03) * r); x.fill(); }
    }
  }
  // A1, the engraving: a fine five-fold guilloche, as on an engraved plate, laid over the ink of the body at low strength
  function paintEngraving() {
    G.eng = null; if (G.s < 170) return;   // too fine to read on a small medallion
    const c = document.createElement("canvas"); c.width = G.pw; c.height = G.ph;
    const x = c.getContext("2d"); x.setTransform(G.k, 0, 0, G.k, 0, 0);
    const { cx, cy, R } = G;
    x.lineWidth = 0.45; x.strokeStyle = "rgba(24,16,48,0.9)";
    for (const dir of [1, -1]) for (let m = 1; m <= 22; m++) {
      const base = R * 1.05 * (m / 22), ph = dir * m * 0.32; x.beginPath();
      for (let k = 0; k <= 180; k++) { const a = (k / 180) * TAU, r = base * (1 + 0.06 * Math.sin(5 * (a - ANG[0]) + ph));
        if (k) x.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); else x.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); }
      x.closePath(); x.stroke();
    }
    G.eng = c;
  }
  // A1, the heart of the star: the five colours' deep inks around the centre, each as deep as its share, fading out toward
  // the rim. Painted (small: a square as wide as the star's full reach) when the shares move, scaled to the star's reach.
  function paintHeart(K, w) {
    const hr = G.R, n = Math.max(8, Math.ceil(2 * hr * G.k)), c = G.heart || document.createElement("canvas");
    if (c.width !== n) { c.width = c.height = n; }
    const x = c.getContext("2d"); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = "source-over"; x.clearRect(0, 0, n, n);
    x.setTransform(n / (2 * hr), 0, 0, n / (2 * hr), 0, 0);
    if (x.createConicGradient) { const cols = K.map((k, i) => mix(NIGHT, DE[i], 0.2 + 0.8 * clamp((k - 0.25) / 0.75))), g = x.createConicGradient(ANG[0], hr, hr);
      for (let i = 0; i < 5; i++) { const j = (i + 1) % 5; g.addColorStop(i / 5, rgba(cols[i], 1)); g.addColorStop((i + blendAt(w, i, j)) / 5, rgba(mix(cols[i], cols[j], 0.5), 1)); }
      g.addColorStop(1, rgba(cols[0], 1)); x.fillStyle = g; }
    else x.fillStyle = "#1a1436";
    x.fillRect(0, 0, 2 * hr, 2 * hr);
    x.globalCompositeOperation = "destination-in";
    const m = x.createRadialGradient(hr, hr, 0, hr, hr, hr * 0.98);
    m.addColorStop(0, "rgba(0,0,0,0.92)"); m.addColorStop(0.35, "rgba(0,0,0,0.7)"); m.addColorStop(0.7, "rgba(0,0,0,0.22)"); m.addColorStop(1, "rgba(0,0,0,0)");
    x.fillStyle = m; x.fillRect(0, 0, 2 * hr, 2 * hr);
    G.heart = c;
  }

  /* ---------- drawing helpers ---------- */
  const P_ = (x, i) => [G.cx + G.R * x * CO[i], G.cy + G.R * x * SI[i]];
  function polyPath(P) { const p = new Path2D(); P.forEach((q, i) => (i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1]))); p.closePath(); return p; }
  // paths are rebuilt only when one of their corners moves by a tenth of a pixel or more
  const PC = {};
  function cpath(name, P) {
    const e = PC[name];
    if (e && e.n === P.length) { let same = true; for (let i = 0; i < P.length && same; i++) same = Math.abs(P[i][0] - e.P[i][0]) < 0.1 && Math.abs(P[i][1] - e.P[i][1]) < 0.1; if (same) return e; }
    return (PC[name] = { n: P.length, P: P.map((q) => q.slice()), p: polyPath(P), out: null });
  }
  // everything outside a shape (for drawing only where the star is not)
  function outside(e) { if (!e.out) { e.out = new Path2D(); e.out.rect(-4, -4, G.w + 8, G.h + 8); e.out.addPath(e.p); } return e.out; }
  // the point on the star's outline at u (0 at White's point, 1 at Blue's, ...), at f of the way out from the centre
  function starXY(P, u, f) {
    let w = u % 5; if (w < 0) w += 5;
    const i = Math.floor(w) % 5, j = (i + 1) % 5, s = w - Math.floor(w), x = P[i][0] + (P[j][0] - P[i][0]) * s, y = P[i][1] + (P[j][1] - P[i][1]) * s;
    return [G.cx + (x - G.cx) * f, G.cy + (y - G.cy) * f];
  }
  // the edge of wet ink: the outline cut into small steps and pushed outward by slow, seamless noise. The noise is sampled
  // ten times a second into a small table and eased between samples, so the edge creeps without per-frame noise work.
  const BM = mini ? 6 : 10, BN = [new Float32Array(5 * BM), new Float32Array(5 * BM)];
  let bnT = null;
  function bleedNoise(t) {
    const k = Math.floor(t * 10);
    const fill = (arr, tm) => { for (let n = 0; n < 5 * BM; n++) { const u = (n / (5 * BM)) * TAU; arr[n] = CH.fbm(Math.cos(u) * 1.6 + 1.3, Math.sin(u) * 1.6 + 2.21 + tm * 0.12, 3); } };
    if (bnT !== k) { if (bnT === k - 1) { const a = BN[0]; BN[0] = BN[1]; BN[1] = a; fill(BN[1], (k + 1) / 10); } else { fill(BN[0], k / 10); fill(BN[1], (k + 1) / 10); } bnT = k; }
    return t * 10 - k;
  }
  function bleedPath(P, amp, t) {
    const f = bleedNoise(t), p = new Path2D();
    for (let i = 0; i < 5; i++) {
      const a = P[i], b = P[(i + 1) % 5];
      for (let s = 0; s < BM; s++) {
        const q = s / BM, x = a[0] + (b[0] - a[0]) * q, y = a[1] + (b[1] - a[1]) * q, n = i * BM + s;
        let nx = x - G.cx, ny = y - G.cy; const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
        const v = BN[0][n] + (BN[1][n] - BN[0][n]) * f, d = amp * (0.25 + 1.3 * Math.max(0, v - 0.28));
        if (n) p.lineTo(x + nx * d, y + ny * d); else p.moveTo(x + nx * d, y + ny * d);
      }
    }
    p.closePath(); return p;
  }
  // copy the part of the heart under box b, scaled by f about the centre (the heart follows the star's reach)
  function blitHeart(x, f, b) {
    const hr = G.R * f, X0 = G.cx - hr, Y0 = G.cy - hr, x0 = Math.max(X0, b[0]), y0 = Math.max(Y0, b[1]), x1 = Math.min(X0 + 2 * hr, b[2]), y1 = Math.min(Y0 + 2 * hr, b[3]);
    if (x1 <= x0 || y1 <= y0 || !G.heart) return; const n = G.heart.width / (2 * hr);
    x.drawImage(G.heart, (x0 - X0) * n, (y0 - Y0) * n, (x1 - x0) * n, (y1 - y0) * n, x0, y0, x1 - x0, y1 - y0);
  }
  // copy the part of a painted-once, canvas-sized layer under box b
  function blit(c, img, b) {
    const k = G.k, x0 = Math.max(0, b[0]), y0 = Math.max(0, b[1]), x1 = Math.min(G.w, b[2]), y1 = Math.min(G.h, b[3]); if (x1 <= x0 || y1 <= y0) return;
    c.drawImage(img, x0 * k, y0 * k, (x1 - x0) * k, (y1 - y0) * k, x0, y0, x1 - x0, y1 - y0);
  }
  const bbox = (P, m) => { let a = 1e9, b = 1e9, c = -1e9, d = -1e9; for (const q of P) { if (q[0] < a) a = q[0]; if (q[1] < b) b = q[1]; if (q[0] > c) c = q[0]; if (q[1] > d) d = q[1]; } return [a - m, b - m, c + m, d + m]; };
  function fanFill(P) {   // without conic gradients: one linear gradient across the whole star (rarely needed)
    const g = ctx.createLinearGradient(P[0][0], P[0][1], P[3][0], P[3][1]); COLORS.forEach((_, i) => g.addColorStop(i / 4, rgba(G.ink ? G.ink[i] : BR[i], 1))); return g;
  }
  function glint(c, x, y, r, col) {
    c.fillStyle = col; c.beginPath();
    c.moveTo(x, y - r); c.quadraticCurveTo(x, y, x + r * 0.7, y); c.quadraticCurveTo(x, y, x, y + r); c.quadraticCurveTo(x, y, x - r * 0.7, y); c.quadraticCurveTo(x, y, x, y - r); c.fill();
  }
  function pin(c, x, y, hl) { const r = (mini ? 1.5 : 2) * G.sc * (hl ? 1.3 : 1); c.globalAlpha = 1; c.drawImage(pinSprite(), x - 2.5 * r, y - 2.5 * r, 5 * r, 5 * r); }
  // A4: the crack network out to a reach (in px), as three paths by depth (trunks, branches, twigs), clipped by the caller
  function crackPaths(reach, u) {
    const out = [new Path2D(), new Path2D()];
    for (const k of CRACKS) {
      const p = out[k.depth]; let started = false;
      for (let j = 0; j < k.p.length; j++) {
        const [x, y, r] = k.p[j], q = r * u;
        if (q > reach) {
          if (j && started) { const [x0, y0, r0] = k.p[j - 1], f = clamp((reach - r0 * u) / Math.max(1e-6, q - r0 * u)); p.lineTo(G.cx + (x0 + (x - x0) * f) * u, G.cy + (y0 + (y - y0) * f) * u); }
          break;
        }
        if (!started) { p.moveTo(G.cx + x * u, G.cy + y * u); started = true; } else p.lineTo(G.cx + x * u, G.cy + y * u);
      }
    }
    return out;
  }
  // A3: the bow of an opposed pair's string, sampled into BW as [x, y, nx, ny] (n points away from the centre)
  const NB = mini ? 12 : 24, BW = new Float32Array((NB + 1) * 4);
  function bow(A, C, B) {
    for (let k = 0; k <= NB; k++) {
      const s = k / NB, u = 1 - s, x = u * u * A[0] + 2 * u * s * C[0] + s * s * B[0], y = u * u * A[1] + 2 * u * s * C[1] + s * s * B[1];
      const dx = 2 * u * (C[0] - A[0]) + 2 * s * (B[0] - C[0]), dy = 2 * u * (C[1] - A[1]) + 2 * s * (B[1] - C[1]), l = Math.hypot(dx, dy) || 1;
      let nx = -dy / l, ny = dx / l; if (nx * (x - G.cx) + ny * (y - G.cy) < 0) { nx = -nx; ny = -ny; }
      BW[k * 4] = x; BW[k * 4 + 1] = y; BW[k * 4 + 2] = nx; BW[k * 4 + 3] = ny;
    }
  }

  /* A1: the body's ink. While the star moves (a corner moved 0.4 px or more in one of the last three frames) it is drawn
     straight onto the star's canvas. Once it rests it is drawn into its own layer and kept until something it shows
     changes: a corner drifting 0.4 px from where the layer has it, the ink (the shares), how wet it is or the key's
     highlight. So a resting star copies one image a frame instead of painting the fills, the heart, the clipped glows and
     the strokes again, and a moving one never paints a layer it would throw away the next frame (copying a layer just
     painted makes the browser fill it there and then). The layer holds only the soft ink, at 1.25 device pixels a pixel
     at most (a third of the pixels to fill on a 2x screen); the hairline that edges it is stroked live, crisp. The bleed
     of wet ink round it creeps every frame, so render draws that live too. */
  const BC = { c: null, P: null };
  let lastP = null, calmN = 0;
  const far = (A, B, d) => { for (let i = 0; i < 5; i++) if (Math.abs(A[i][0] - B[i][0]) > d || Math.abs(A[i][1] - B[i][1]) > d) return true; return false; };
  function drawInk(c, P, body, wet, key, xmax, a) {
    calmN = !lastP || far(P, lastP, 0.4) ? 0 : calmN + 1; lastP = P.map((q) => q.slice());
    const k = G.k, kl = Math.min(k, 1.25), inkv = G.conic, wq = Math.round(wet * 50);
    const kept = BC.c && BC.P && !far(P, BC.P, 0.4) && BC.ink === inkv && BC.wq === wq && BC.key === key && BC.k === k;
    if (!kept && calmN < 3 && a >= 0.99) { BC.P = null; drawBody(c, P, body, wet, key, xmax, true); return; }
    if (!kept) {
      const b = bbox(P, 2), x0 = Math.floor(b[0] * kl) / kl, y0 = Math.floor(b[1] * kl) / kl;
      const pw = Math.max(1, Math.ceil((b[2] - x0) * kl)), ph = Math.max(1, Math.ceil((b[3] - y0) * kl));
      const cnv = BC.c || (BC.c = document.createElement("canvas"));
      if (cnv.width < pw || cnv.height < ph) { cnv.width = Math.max(pw, cnv.width); cnv.height = Math.max(ph, cnv.height); }
      const x = cnv.getContext("2d");
      x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = "source-over"; x.clearRect(0, 0, cnv.width, cnv.height);
      x.setTransform(kl, 0, 0, kl, -x0 * kl, -y0 * kl);
      drawBody(x, P, body, wet, key, xmax, false);
      Object.assign(BC, { P: P.map((q) => q.slice()), ink: inkv, wq, key, k, kl, x0, y0, pw, ph });
    }
    c.globalAlpha = a; c.drawImage(BC.c, 0, 0, BC.pw, BC.ph, BC.x0, BC.y0, BC.pw / BC.kl, BC.ph / BC.kl);
    hairline(c, body, wet, key, a);
  }
  /* the body itself: the five inks fan from the centre, each as bright as its share, over a deep heart; each colour's lobe
     lit from within by its share; a faint engraving and facets like a cut stone; inside, light gathers softly toward the
     rim; and one inked hairline round it (crisper the drier). The bleed of wet ink and the slow highlight are drawn live
     in render. */
  function drawBody(c, P, body, wet, key, xmax, hair) {
    const { cx, cy, R, sc } = G, fill = G.conic || fanFill(P), bb = bbox(P, 2), reach = R * Math.max(0.3, xmax);
    c.globalAlpha = 0.92; c.fillStyle = fill; c.fill(body);
    c.save(); c.clip(body);
    c.globalAlpha = 0.85; blitHeart(c, reach / R, bb);
    // each colour's lobe glows from within as strongly as its share (the leading colour lights the star)
    c.globalCompositeOperation = "lighter";
    for (let i = 0; i < 5; i++) { const k = clamp((G.inkK[i] - 0.25) / 0.75), dx = P[i][0] - cx, dy = P[i][1] - cy, l = Math.hypot(dx, dy);
      if (k > 0.02 && l > 3) stamp(c, glow(BR[i]), cx + dx * 0.58, cy + dy * 0.58, l * 0.85, 0.2 * k); }
    // facets: each fan triangle catches the light from the upper left a little more or less, like a cut stone (faintly)
    c.globalAlpha = 1;
    for (let i = 0; i < 5; i++) {
      const a = P[i], b = P[(i + 1) % 5], mid = Math.atan2((a[1] + b[1]) / 2 - cy, (a[0] + b[0]) / 2 - cx), lit = Math.cos(mid + 2.36);
      c.beginPath(); c.moveTo(cx, cy); c.lineTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.closePath();
      if (lit > 0) { c.globalCompositeOperation = "lighter"; c.fillStyle = rgba(WHITE, 0.035 * lit); } else { c.globalCompositeOperation = "source-over"; c.fillStyle = rgba(NIGHT, 0.09 * -lit); }
      c.fill();
    }
    c.globalCompositeOperation = "source-over";
    if (G.eng) { c.globalAlpha = 0.07 + 0.05 * (1 - wet); blit(c, G.eng, bb); }
    // the inner glow: the colour gathers toward the rim and fades inward with no inner line (four nested strokes, each
    // half hidden by the clip), wider and softer the wetter the ink
    c.strokeStyle = fill; c.lineJoin = "round";
    const gw = (0.8 + 0.5 * wet) * sc;
    [[18, 0.08], [12, 0.1], [7, 0.14], [3, 0.22]].forEach(([w, a]) => { c.globalAlpha = a; c.lineWidth = w * gw; c.stroke(body); });
    c.globalCompositeOperation = "lighter"; c.globalAlpha = 0.12; c.lineWidth = 2 * gw; c.stroke(body);   // and catches the light
    c.globalCompositeOperation = "source-over";
    c.restore();
    if (hair) hairline(c, body, wet, key, 1);
  }
  // the inked hairline: the pigment gathered at the edge of the wash, crisp when dry, softer while the ink is wet
  function hairline(c, body, wet, key, a) {
    c.lineJoin = "round"; c.strokeStyle = G.conic || fanFill(G.P); c.globalAlpha = (0.92 - 0.42 * wet) * a;
    c.lineWidth = Math.max(0.6, (0.85 + 0.7 * wet) * G.sc) * (key === "pos" ? 1.8 : 1); c.stroke(body);
    c.globalAlpha = 1;
  }

  /* a shadow (decision 5, as today's wheel): the end of a color's point, as far in as its shadow part, cut square to the
     axis and inked: darkened, then hatched in the color's pale ink (crosshatched while the state shows), with the cut drawn
     as a fine line. The cut is the wheel's own (05-hud.js spiderSVG): where the edges toward both neighbours cross (1 - part)
     of the point's length. */
  const shLast = [null, null, null, null, null];
  function drawShadows(c, P, a) {
    const { cx, cy, sc } = G;
    for (let i = 0; i < 5; i++) {
      const x = st.shadow && st.shadow[i]; if (x) shLast[i] = x;
      const k = D.sh[i] * a, y = shLast[i]; if (k < 0.01 || !y || y[0] < 0.05) continue;
      const ux = CO[i], uy = SI[i], r1 = (P[i][0] - cx) * ux + (P[i][1] - cy) * uy, r0 = r1 * (1 - y[0]);
      if (r1 - r0 < 0.6) continue;
      const cut = (j) => { const b = P[j], pb = (b[0] - cx) * ux + (b[1] - cy) * uy, f = clamp((r1 - r0) / Math.max(r1 - pb, 1e-6));
        return [P[i][0] + (b[0] - P[i][0]) * f, P[i][1] + (b[1] - P[i][1]) * f]; };
      const A = cut((i + 4) % 5), B = cut((i + 1) % 5);
      c.save();
      c.beginPath(); c.moveTo(A[0], A[1]); c.lineTo(P[i][0], P[i][1]); c.lineTo(B[0], B[1]); c.closePath();
      c.globalAlpha = 0.55 * k; c.fillStyle = rgba(INK, 1); c.fill();
      c.clip();
      const bb = bbox([A, P[i], B], 1), gap = Math.max(1.6, 2.4 * sc), span = bb[2] - bb[0] + bb[3] - bb[1];
      c.strokeStyle = rgba(mix(PA[i], WHITE, 0.2), 1); c.lineWidth = Math.max(0.45, 0.6 * sc); c.globalAlpha = 0.6 * k;
      c.beginPath();
      for (let d = 0; d <= span; d += gap) { c.moveTo(bb[0] + d, bb[1]); c.lineTo(bb[0] + d - (bb[3] - bb[1]), bb[3]); }
      if (y[1]) for (let d = 0; d <= span; d += gap) { c.moveTo(bb[2] - d, bb[1]); c.lineTo(bb[2] - d + (bb[3] - bb[1]), bb[3]); }
      c.stroke();
      c.restore();
      c.globalAlpha = 0.7 * k; c.strokeStyle = rgba(BR[i], 1); c.lineWidth = Math.max(0.5, 0.7 * sc);
      c.beginPath(); c.moveTo(A[0], A[1]); c.lineTo(B[0], B[1]); c.stroke(); c.globalAlpha = 1;
    }
  }
  /* the voice in their head (05-hud.js item 3): while its row is read, thin dashed arrows from each point toward where the
     voice pushes (toward x 0.15 of a share, as the wheel draws them) */
  function drawVoice(c, P) {
    const v = st.voice; if (!v) return;
    c.lineCap = "round"; c.setLineDash([3 * G.sc, 2 * G.sc]);
    for (let i = 0; i < 5; i++) {
      const to = P_(CH.spR(clamp(st.w[i] + v[i], 0.01, 0.95)), i), dx = to[0] - P[i][0], dy = to[1] - P[i][1], l = Math.hypot(dx, dy);
      if (l < 1.5 * G.sc) continue;
      const ux = dx / l, uy = dy / l, hd = Math.min(l * 0.6, 3.5 * G.sc), bx = to[0] - ux * hd, by = to[1] - uy * hd;
      c.globalAlpha = 0.9; c.strokeStyle = rgba(mix(PA[i], WHITE, 0.25), 1); c.lineWidth = Math.max(0.7, 1.1 * G.sc);
      c.beginPath(); c.moveTo(P[i][0], P[i][1]); c.lineTo(bx, by); c.stroke();
      c.setLineDash([]); c.fillStyle = c.strokeStyle; c.beginPath(); c.moveTo(to[0], to[1]); c.lineTo(bx - uy * hd * 0.8, by + ux * hd * 0.8); c.lineTo(bx + uy * hd * 0.8, by - ux * hd * 0.8); c.closePath(); c.fill();
      c.setLineDash([3 * G.sc, 2 * G.sc]);
    }
    c.setLineDash([]); c.globalAlpha = 1;
  }

  /* ======================================================================================================================
     render(t, still): one frame. Back to front: the hovered axis and the edge band, A3's allied arcs, A2's old outlines,
     the body (A1), A2's motes, wants, holds and the pull (A1), the core (A4), a breakthrough's shards (A4), A3's opposed
     strings, the points and their place (A1), an outcome's ink. */
  function render(t, still) {
    if (!layout()) return;
    refreshInk();
    const c = ctx, { cx, cy, R, sc } = G;
    c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    c.clearRect(0, 0, cv.width, cv.height);
    c.setTransform(G.k, 0, 0, G.k, 0, 0);
    if (!st.has) return;
    // A1, an outcome landing: the whole star breathes in and settles back (see breathe), so the points, the body and all
    // that hangs on them swell together, by at most 6% of their reach
    const bu = breath ? (t - breath.t0) / breath.dur : -1;
    if (bu >= 1) breath = null;
    const bump = bu > 0 && bu < 1 ? (bu < 0.26 ? easeOut(bu / 0.26) : 1 - easeBack((bu - 0.26) / 0.74)) : 0, swell = 1 + 0.06 * (breath ? breath.k : 0) * bump;
    const P = D.x.map((x, i) => P_(Math.max(0.02, x) * swell, i)), Wp = D.xw.map(P_), H = D.xh.map(P_);
    G.P = P; G.Wp = Wp; G.H = H;
    const xmax = Math.max(...D.x) * swell, hi = hover && (hover.k === "pt" || hover.k === "hold" || hover.k === "want") ? hover.i : -1;
    const key = hover && hover.k === "key" ? hover.key : "";
    const sh = shat ? clamp((t - shat.t0) / shat.dur) : -1;
    if (sh >= 1) shat = null;
    const shatOn = sh >= 0 && sh < 1, bodyA = shatOn ? CH.smooth(clamp((sh - 0.79) / 0.21)) : 1;
    const ru = rel ? clamp((t - rel.t0) / rel.dur) : -1;
    if (ru >= 1) rel = null;
    const B = cpath("body", P), body = B.p, wet = clamp(D.wet);

    // the hovered colour's axis lights up, from the centre to its orb; so do the colours of the card under the mouse
    const lit = st.ends.length ? st.ends.concat(hi >= 0 && !st.ends.includes(hi) ? [hi] : []) : hi >= 0 ? [hi] : [];
    for (const j of lit) { c.globalCompositeOperation = "lighter"; const g = c.createLinearGradient(cx, cy, G.O[j][0], G.O[j][1]);
      g.addColorStop(0, rgba(BR[j], 0)); g.addColorStop(1, rgba(BR[j], 0.45)); c.strokeStyle = g; c.lineWidth = 1.4 * sc;
      c.beginPath(); c.moveTo(cx, cy); c.lineTo(G.O[j][0], G.O[j][1]); c.stroke(); c.globalCompositeOperation = "source-over"; }
    // A1, the identity edge brightens while the Edge key is read, or a colour on the edge (rising or fading) is hovered
    const edgeHi = key === "band" || (hi >= 0 && hover.k === "pt" && (st.bands[hi] === "rising" || st.bands[hi] === "fading"));
    if (edgeHi) { c.fillStyle = rgba(GOLD2, 0.07); c.fill(G.band, "evenodd"); }

    /* A3: allies. Two neighbours on the pie both above 15% share a calm arc of light just inside the ring of orbs, from one
       orb toward the other, coloured from one to the other and breathing slowly. */
    if (lay.threads) {
      c.globalCompositeOperation = "lighter"; c.lineCap = "round";
      PAIRS.forEach((p, j) => {
        const q = PS[j]; if (p.foe) return; q.ra = 0;
        if (D.pair[j] < 0.01) return;
        const ra = Math.max(G.arcR, R * Math.max(D.x[p.a], D.x[p.b]) + 6 * sc), a0 = ANG[p.a], a1 = a0 + TAU / 5;
        const br = D.pair[j] * (still ? 0.9 : 0.8 + 0.2 * Math.sin(t * 0.7 + j * 1.3)) * (hover && hover.k === "arc" && hover.p === j ? 1.5 : 1);
        c.strokeStyle = q.g || rgba(BR[p.a], 1);
        c.globalAlpha = 0.22 * br; c.lineWidth = 4 * sc; c.beginPath(); c.arc(cx, cy, ra, a0, a1); c.stroke();
        c.globalAlpha = 0.85 * br; c.lineWidth = Math.max(0.6, 0.9 * sc); c.stroke();
        q.ra = ra;
      });
      c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    }

    /* A2: afterimages. The star 1, 4 and 10 years ago as moonlit silver outlines, drawn only where the star is not now
       (where it used to reach and no longer does), each older one fainter and softer. An old image whose points all lie
       within 3 px of today's is left out (a life holding still shows none), and its outline is drawn only where it reaches
       3 px or more beyond today's star (a thinner sliver would read as a misprinted edge, not an afterimage). */
    const old = [];
    if (lay.after) {
      for (const k of [2, 1, 0]) {
        if (!D.ae[k] || D.aa[k] < 0.01) continue;
        const Q = D.ae[k].map((x, i) => P_(Math.max(0.02, x), i));
        let off = 0, out = 0; for (let i = 0; i < 5; i++) { off = Math.max(off, Math.hypot(Q[i][0] - P[i][0], Q[i][1] - P[i][1])); out = Math.max(out, (D.ae[k][i] - D.x[i]) * R); }
        const vis = D.aa[k] * CH.smooth(clamp((off - 2) / 2.5)); if (vis < 0.01) continue;
        old.push({ k, Q, vis, ov: vis * CH.smooth(clamp((out - 2.5) / 2)) });
      }
      // (drawn before the body, whose opaque ink then covers whatever part lies inside today's star: no clip needed)
      c.lineJoin = "round";
      for (const { k, Q, ov: vis } of old) {
        if (vis < 0.01) continue;
        const p = cpath("aft" + k, Q).p;
        c.fillStyle = rgba(AFT, [0.05, 0.04, 0.03][k] * vis); c.fill(p);
        c.strokeStyle = rgba(AFT, [0.1, 0.08, 0.06][k] * vis); c.lineWidth = (3 + k * 1.6) * sc; c.stroke(p);   // the soft blur of an old image
        c.strokeStyle = rgba(AFT, [0.5, 0.34, 0.22][k] * vis); c.lineWidth = Math.max(0.5, [0.9, 0.8, 0.7][k] * sc); c.stroke(p);
      }
    }

    /* A3: opposed colours. Two colours across the pie, both above 15%, are joined by a string bowed out round the colour
       between them (the neighbour they share), so it never crosses the ink. It hums: a standing wave whose height grows
       with the smaller of the two shares and with pent-up wanting. Its blur shows as a faint lens round it, drawn here
       behind the body (so the ink covers any part of it that dips inside); the string itself is drawn after the core,
       where it is this instant, each end in its own colour. Energy, never damage. */
    const nrT = clamp(D.near, 0, 1.2), strings = [];
    if (lay.threads) {
      const C72 = Math.cos(TAU / 5);
      PAIRS.forEach((p, j) => {
        const q = PS[j]; if (!p.foe) return; q.bow = null;
        if (D.pair[j] < 0.01) return;
        // the bow's crown clears the colour between them (and its wanted place, when wants are drawn) by an eighth of the reach
        const ra = Math.max(0.02, D.x[p.a]), rb = Math.max(0.02, D.x[p.b]), rm = Math.max(0.02, D.x[p.mid], lay.ghost ? D.xw[p.mid] : 0);
        const rc = Math.max(1.25 * Math.max(ra, rb), (rm + 0.13 - 0.25 * (ra + rb) * C72) / 0.5);
        const A = P[p.a], Bp = P[p.b], C = [cx + R * rc * CO[p.mid], cy + R * rc * SI[p.mid]];
        q.bow = [A, C, Bp]; bow(A, C, Bp);
        const al = D.pair[j] * D.pair[j] * (shatOn ? 1 - Math.sin(Math.PI * sh) : 1), hov = hover && hover.k === "thr" && hover.p === j;
        const amp = (1.2 + 6.5 * clamp(Math.min(st.w[p.a], st.w[p.b]) / 0.35)) * (0.5 + 0.8 * nrT) * sc, g = q.g || rgba(BR[p.a], 1);
        strings.push({ p, j, A, Bp, C, al, hov, amp, g });
        c.beginPath();
        for (let k = 0; k <= NB; k++) { const s = k / NB, e = amp * (Math.sin(Math.PI * s) + 0.35 * Math.abs(Math.sin(TAU * s))), o = k * 4; k ? c.lineTo(BW[o] + BW[o + 2] * e, BW[o + 1] + BW[o + 3] * e) : c.moveTo(BW[o] + BW[o + 2] * e, BW[o + 1] + BW[o + 3] * e); }
        for (let k = NB; k >= 0; k--) { const s = k / NB, e = amp * (Math.sin(Math.PI * s) + 0.35 * Math.abs(Math.sin(TAU * s))), o = k * 4; c.lineTo(BW[o] - BW[o + 2] * e, BW[o + 1] - BW[o + 3] * e); }
        c.closePath(); c.globalCompositeOperation = "lighter"; c.fillStyle = g; c.globalAlpha = 0.14 * al * (hov ? 1.6 : 1); c.fill();
      });
      c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    }

    /* A1: the body. The five inks fan from the centre, each as bright as its share, over a deep heart; a faint engraving and
       facets like a cut stone; inside, light gathers softly toward the rim. Round it only three things: one bleed of wet
       ink into the glass (wider the wetter the ink, S.wet), one inked hairline (crisper the drier) and a slow highlight.
       While the star shatters (A4) the shards take its place and the body fades back in under them as they settle. */
    if (bodyA > 0.01) {
      // the bleed of wet ink into the glass round it, wider the wetter (S.wet), creeping
      if (wet > 0.02) {
        c.globalCompositeOperation = "lighter"; c.fillStyle = G.conic || fanFill(P);
        c.globalAlpha = (0.07 + 0.17 * wet) * bodyA; c.fill(bleedPath(P, (1.2 + 10 * wet) * sc, still ? 0 : t));
        c.globalCompositeOperation = "source-over";
      }
      drawInk(c, P, body, wet, key, xmax, bodyA);
      // and the slow light round the rim (still: it rests at the upper left), live over the cached ink
      if (G.hiPat) {
        turnHi(still ? -2.4 : -2.4 + t * 0.55);
        c.globalCompositeOperation = "lighter"; c.strokeStyle = G.hiPat; c.globalAlpha = 0.5 * bodyA; c.lineJoin = "round"; c.lineWidth = Math.max(0.8, 1.5 * sc); c.stroke(body);
        c.globalCompositeOperation = "source-over";
      }
      // A1, an outcome landing: as the star breathes in, its own inks light up from within for a moment
      if (breath && bump > 0.01) { c.globalCompositeOperation = "lighter"; c.globalAlpha = Math.max(0, 0.2 * breath.k * bump) * bodyA; c.fillStyle = G.conic || fanFill(P); c.fill(body); c.globalCompositeOperation = "source-over"; }
      c.globalAlpha = 1;
      if (D.sh.some((v) => v > 0.01)) drawShadows(c, P, bodyA);
    }

    /* A1, an outcome landing: one ring of ink runs out from the core to the ring of orbs in the colour the outcome turned
       them toward most, thinning and fading as it goes (a faint wide halo under a fine line) */
    if (breath && bu > 0.04 && bu < 1) {
      const u = (bu - 0.04) / 0.96, r = R * 0.06 + (G.orbR - R * 0.06) * easeOut(u), a = (0.3 + 0.3 * breath.k) * Math.pow(1 - u, 1.5), col = mix(BR[breath.i], WHITE, 0.15);
      c.globalCompositeOperation = "lighter"; c.strokeStyle = rgba(col, 1);
      c.globalAlpha = a * 0.3; c.lineWidth = (5 - 2.5 * u) * sc; c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.stroke();
      c.globalAlpha = a; c.lineWidth = Math.max(0.6, (1.5 - 0.6 * u) * sc); c.stroke();
      c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    }

    /* A2: the comet's tails. Along each axis that drifted, a few silver motes run from the oldest image to where that colour
       stands now, fainter the older, drifting slowly toward now (still: resting). Each is a small silver bead with a soft
       halo, so it reads over bright ink as well as over the night glass. */
    if (lay.after && old.length && !mini) {
      const sp = glow(AFT), beads = [];
      c.globalCompositeOperation = "lighter";
      for (let i = 0; i < 5; i++) {
        const chain = old.map((o) => [o.Q[i], o.vis]).concat([[P[i], 1]]);
        let L = 0; const seg = [];
        for (let j = 0; j < chain.length - 1; j++) { const a = chain[j][0], b = chain[j + 1][0], l = Math.hypot(b[0] - a[0], b[1] - a[1]); seg.push(l); L += l; }
        if (L < 3) continue;
        const nm = Math.max(3, Math.min(6, Math.round(L / (5 * sc)))), ph = still ? 0.5 : (t * 0.22 + i * 0.17) % 1;
        for (let m = 0; m < nm; m++) {
          const s = (m + ph) / nm; let d = s * L, j = 0; while (j < seg.length - 1 && d > seg[j]) { d -= seg[j]; j++; }
          const a = chain[j][0], b = chain[j + 1][0], q = seg[j] > 0 ? Math.min(1, d / seg[j]) : 0, x = a[0] + (b[0] - a[0]) * q, y = a[1] + (b[1] - a[1]) * q;
          const env = CH.smooth(Math.min(1, s * 4)) * CH.smooth(Math.min(1, (1 - s) * 6)), al = (0.1 + 0.4 * s) * env * chain[j][1];
          if (al < 0.01) continue;
          stamp(c, sp, x, y, (3 + 2 * s) * sc, al * 0.7); beads.push(x, y, (0.85 + 0.6 * s) * sc, Math.min(1, al * 1.6));
        }
      }
      // the beads over their halos (one change of drawing mode for all of them)
      c.globalCompositeOperation = "source-over"; c.fillStyle = rgba(mix(AFT, WHITE, 0.4), 1);
      for (let n = 0; n < beads.length; n += 4) { c.globalAlpha = beads[n + 3]; c.beginPath(); c.arc(beads[n], beads[n + 1], beads[n + 2], 0, TAU); c.fill(); }
      c.globalAlpha = 1;
    }

    /* A1: wants, a faint luminous ghost star in the wanting colour, breathing on its light alone; a small four-point glint at
       each wanted place */
    if (lay.ghost) {
      const gp = cpath("want", Wp).p, br = (still ? 1 : 0.8 + 0.2 * Math.sin(t * 1.1)) * (key === "want" ? 2 : 1);
      c.globalCompositeOperation = "lighter"; c.lineJoin = "round";
      c.fillStyle = rgba(WANTC, 0.03 * br); c.fill(gp);
      c.strokeStyle = rgba(WANTC, 0.07 * br); c.lineWidth = 5 * sc; c.stroke(gp);
      c.strokeStyle = rgba(mix(WANTC, WHITE, 0.2), 0.28 * br); c.lineWidth = Math.max(0.5, 0.8 * sc); c.stroke(gp);
      Wp.forEach((q, i) => { if (Math.abs(D.xw[i] - D.x[i]) * R < 2.5) return; glint(c, q[0], q[1], 3.2 * sc * (hover && hover.k === "want" && hi === i ? 1.4 : 1), rgba(WANTC, Math.min(1, 0.75 * br))); });
      c.globalCompositeOperation = "source-over";
    }

    /* A1: holds. A gilt anchor pin at the hold radius on each axis and a fine thread from the point to it. The thread is
       taut, straight and quivering when what holds them pulls against what they want; otherwise it hangs slack and sags
       a little under its own weight (more on a level axis than an upright one). */
    if (lay.tethers) {
      c.lineCap = "round";
      const kh = key === "hold" ? 1.5 : 1;
      for (let i = 0; i < 5; i++) {
        const a = P[i], b = H[i], len = Math.hypot(b[0] - a[0], b[1] - a[1]), T = D.T[i];
        if (len > 2 * sc) {
          let nx = -SI[i], ny = CO[i]; if (ny < 0 || (ny === 0 && nx < 0)) { nx = -nx; ny = -ny; }   // the side gravity pulls a slack thread to
          const sag = (1 - T) * Math.min(len * 0.32, 7 * sc) * (0.3 + 0.7 * Math.abs(CO[i]));
          const q = still ? 0 : T * Math.sin(t * 71 + i * 2) * 0.45 * sc;   // a taut thread quivers
          const mx = (a[0] + b[0]) / 2 + nx * (sag * 2 + q), my = (a[1] + b[1]) / 2 + ny * (sag * 2 + q);
          c.globalAlpha = 1; c.strokeStyle = rgba(mix(GOLD2, WHITE, T * 0.5), (0.42 + 0.45 * T) * (i === hi ? 1.4 : kh));
          c.lineWidth = Math.max(0.5, (0.6 + 0.6 * T) * sc);
          c.beginPath(); c.moveTo(a[0], a[1]); c.quadraticCurveTo(mx, my, b[0], b[1]); c.stroke();
          if (T > 0.15) { c.globalCompositeOperation = "lighter"; c.strokeStyle = rgba(GOLD2, 0.12 * T * kh); c.lineWidth = 3 * sc; c.stroke(); c.globalCompositeOperation = "source-over"; }
        }
        pin(c, b[0], b[1], i === hi || key === "hold");
      }
    }

    /* A1: the pull. From each point toward its wanted place runs a tapered stream of light in its colour, wider the faster
       they could change now (S.acc), with motes flowing along it at that speed. */
    if (lay.ghost) {
      c.globalCompositeOperation = "lighter";
      const kp = key === "pull" ? 1.6 : 1;
      for (let i = 0; i < 5; i++) {
        const a = P[i], b = Wp[i], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy); if (len < 2.5) continue;
        const acc = clamp(st.acc[i] / 0.4), w0 = (1.4 + 3.6 * acc) * sc * (kp > 1 ? 1.3 : 1);
        c.save(); c.translate(a[0], a[1]); c.rotate(Math.atan2(dy, dx)); c.scale(len, 1);
        c.globalAlpha = Math.min(1, kp); c.fillStyle = G.pullG[i]; c.beginPath(); c.moveTo(0, w0 / 2); c.lineTo(1, 0); c.lineTo(0, -w0 / 2); c.closePath(); c.fill();
        c.restore();
        const n = mini ? 1 : 2, spd = 0.18 + 1.1 * acc;
        for (let j = 0; j < n; j++) { const u = still ? 0.38 + j * 0.36 : (t * spd + j / n + i * 0.13) % 1, m = easeIO(u);
          stamp(c, glow(PA[i]), a[0] + dx * m, a[1] + dy * m, (2.6 + 2.4 * acc) * sc, Math.sin(Math.PI * u)); }
      }
      c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    }
    drawVoice(c, P);

    /* A4: the breaking point. Pent-up wanting (S.dyn.near: pressure over the threshold) glows in the core, from a cool
       wanting-violet to warm gold as it rises, its pulse quickening; above 0.6 hairline cracks of light spread from the
       centre toward the edge, reaching it at 1. */
    if (lay.core && !shatOn) {
      const nr = clamp(D.near, 0, 1.3), n1 = Math.min(1, nr), hot = clamp((nr - 0.25) / 0.75), col = mix(WANTC, WARM, hot);
      const over = clamp((nr - 1) / 0.3);   // past the mark: hotter still
      const hz = 0.35 + 1.1 * n1 + 0.5 * over, ph = still ? 0.45 : (t * hz) % 1, beat = still ? 0.5 : Math.pow(Math.max(0, Math.sin(ph * TAU)), 4);   // a heartbeat, quicker as it rises
      c.globalCompositeOperation = "lighter";
      stamp(c, glow(col), cx, cy, R * (0.25 + 0.5 * n1), 0.07 + 0.25 * n1 + 0.06 * over);                          // the halo
      stamp(c, glow(mix(col, HOT, 0.45)), cx, cy, R * (0.07 + 0.11 * n1) * (1 + 0.16 * beat), 0.3 + 0.5 * n1);      // the nucleus
      stamp(c, glow(HOT), cx, cy, R * (0.03 + 0.05 * n1 + 0.02 * over), 0.45 + 0.55 * n1);
      // the pressure: rings of light leave the nucleus on each beat and fade before the rim
      if (n1 > 0.08) for (let k = 0; k < (still ? 1 : 2); k++) {
        const u = still ? 0.5 : (ph + k * 0.5) % 1, r = R * (0.05 + (0.12 + 0.3 * n1) * easeOut(u));
        c.globalAlpha = Math.pow(1 - u, 2) * (0.1 + 0.5 * n1); c.strokeStyle = rgba(col, 1); c.lineWidth = Math.max(0.5, (0.6 + 0.6 * n1) * sc);
        c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.stroke();
      }
      c.globalAlpha = 1;
      if (hover && hover.k === "core") { c.strokeStyle = rgba(WARM, 0.5); c.lineWidth = 0.8 * sc; c.beginPath(); c.arc(cx, cy, Math.max(10, R * 0.14), 0, TAU); c.stroke(); }
      const cr = rel ? 0 : clamp((nr - 0.6) / 0.4), u = R * Math.max(0.25, xmax);
      if (cr > 0.001) {
        const flick = still ? 1 : 0.8 + 0.2 * CH.noise(t * 3, 4.2), [p0, p1] = crackPaths(cr * 1.05 * u, u);
        c.save(); c.clip(body); c.lineCap = "round"; c.lineJoin = "round";
        // hairlines of warm light, the trunks a little stronger than their branches, with a faint glow of light leaking
        c.strokeStyle = rgba(WARM, 0.09 * flick); c.lineWidth = 1.8 * sc; c.stroke(p0); c.strokeStyle = rgba(WARM, 0.06 * flick); c.lineWidth = 1.4 * sc; c.stroke(p1);
        c.strokeStyle = rgba(mix(HOT, WARM, 0.5), 0.5 * flick); c.lineWidth = Math.max(0.3, 0.36 * sc); c.stroke(p0); c.strokeStyle = rgba(mix(HOT, WARM, 0.5), 0.34 * flick); c.lineWidth = Math.max(0.3, 0.28 * sc); c.stroke(p1);
        c.restore();
      }
      /* A4, a breakthrough within the same identity (a "breakthrough" story line): the core lets go in a flash, the cracks
         fill with gold and close back into the core (0.6 s), and a pulse of light runs out along each colour it turned
         them toward, ringing that point when it arrives. */
      if (rel) {
        stamp(c, glow(mix(WARM, HOT, 0.5)), cx, cy, R * (0.2 + 0.5 * easeOut(ru)), 0.85 * Math.pow(1 - ru, 2));
        const cu = clamp(ru / 0.46);
        if (cu < 1) {
          const [p0, p1] = crackPaths(rel.cr * 1.05 * u * (1 - easeIO(cu)), u), ga = 1 - 0.6 * cu;
          c.save(); c.clip(body); c.lineCap = "round"; c.lineJoin = "round";
          c.strokeStyle = rgba(GOLD, 0.35 * ga); c.lineWidth = 2.6 * sc; c.stroke(p0); c.lineWidth = 1.9 * sc; c.stroke(p1);
          c.strokeStyle = rgba(GOLD2, 0.95 * ga); c.lineWidth = Math.max(0.5, 0.75 * sc); c.stroke(p0); c.lineWidth = Math.max(0.4, 0.55 * sc); c.stroke(p1);
          c.restore();
        }
        for (const i of rel.ax) {
          const pu = clamp((ru - 0.12) / 0.5);
          if (pu > 0 && pu < 1) { const m = easeIO(pu), x = cx + (P[i][0] - cx) * m, y = cy + (P[i][1] - cy) * m;
            c.globalAlpha = 0.6 * Math.sin(Math.PI * pu); c.strokeStyle = rgba(mix(PA[i], WHITE, 0.3), 1); c.lineWidth = 1.4 * sc; c.beginPath(); c.moveTo(cx + (P[i][0] - cx) * Math.max(0, m - 0.25), cy + (P[i][1] - cy) * Math.max(0, m - 0.25)); c.lineTo(x, y); c.stroke();
            stamp(c, glow(mix(PA[i], WHITE, 0.3)), x, y, (4.5 - 1.5 * pu) * sc, 0.95 * Math.sin(Math.PI * pu)); }
          const qu = clamp((ru - 0.58) / 0.42);
          if (qu > 0 && qu < 1) { c.globalAlpha = (1 - qu) * 0.8; c.strokeStyle = rgba(BR[i], 1); c.lineWidth = 1.2 * sc; c.beginPath(); c.arc(P[i][0], P[i][1], (3 + 12 * easeOut(qu)) * sc, 0, TAU); c.stroke(); }
        }
        c.globalAlpha = 1;
      }
      c.globalCompositeOperation = "source-over";
    }

    // A4, when who they are changes: the shards
    if (shatOn) drawShatter(c, sh, P);

    // A3, the strings themselves, over the body and the core
    if (strings.length) {
      c.lineCap = "round"; c.lineJoin = "round";
      for (const { p, j, A, Bp, C, al, hov, amp, g } of strings) {
        bow(A, C, Bp);
        const w1 = TAU * (3.2 + 4 * nrT), w2 = TAU * (5.3 + 5 * nrT), c1 = still ? 0.85 : Math.cos(t * w1 + j), c2 = still ? 0.3 : Math.cos(t * w2 + j * 2.1);
        // the string at this instant: a faint dark shadow under it, the string in its two colours, and a soft glow
        c.beginPath();
        for (let k = 0; k <= NB; k++) { const s = k / NB, e = amp * (Math.sin(Math.PI * s) * c1 + 0.35 * Math.sin(TAU * s) * c2), o = k * 4; k ? c.lineTo(BW[o] + BW[o + 2] * e, BW[o + 1] + BW[o + 3] * e) : c.moveTo(BW[o] + BW[o + 2] * e, BW[o + 1] + BW[o + 3] * e); }
        c.globalCompositeOperation = "source-over";
        c.strokeStyle = rgba(INK, 1); c.globalAlpha = 0.35 * al; c.lineWidth = Math.max(1.4, 2.4 * sc); c.stroke();
        c.strokeStyle = g; c.globalAlpha = Math.min(1, 0.95 * al * (hov ? 1.1 : 1)); c.lineWidth = Math.max(0.6, (hov ? 1.5 : 1.1) * sc); c.stroke();
        c.globalCompositeOperation = "lighter"; c.globalAlpha = 0.2 * al * (hov ? 1.5 : 1); c.lineWidth = 4.5 * sc; c.stroke();
        stamp(c, glow(PA[p.a]), A[0], A[1], 3.5 * sc, al); stamp(c, glow(PA[p.b]), Bp[0], Bp[1], 3.5 * sc, al);   // where it is tied
      }
      c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
    }

    /* A1: the points and their place. In: a steady glow (a little brighter than the rest, so who they are leads). Fading:
       the glow flickers gently and a broken ring turns slowly round its orb. Rising: the point kindles and throws tiny
       sparks, and a bright ring lights round its orb. Out: quiet. */
    c.globalCompositeOperation = "lighter";
    for (let i = 0; i < 5; i++) {
      const [x, y] = P[i], b = D.band[i], O = G.O[i];
      const fl = still ? 0.75 : 0.45 + 0.55 * CH.noise(t * 2.1 + i * 9.7, i * 3.3);
      const gl = b[0] * 0.8 + b[1] * 0.55 * fl + b[2] * (0.45 + (still ? 0.1 : 0.15 * Math.sin(t * 5 + i))) + (i === hi ? 0.4 : 0);
      stamp(c, glow(BR[i]), x, y, (mini ? 8 : 12) * sc, gl);
      stamp(c, glow(BR[i]), O[0], O[1], G.od * 1.05, b[0] * 0.3 + b[2] * 0.35 + b[1] * 0.18 * fl + (i === hi ? 0.35 : 0));
      const rr = G.rr;
      if (b[1] > 0.02) {   // fading: a broken ring, turning slowly
        c.globalAlpha = b[1] * (0.5 + 0.4 * fl); c.strokeStyle = rgba(GOLD, 1); c.lineWidth = Math.max(0.8, 1.3 * sc);
        c.setLineDash([3.2 * sc, 2.6 * sc]); c.lineDashOffset = still ? 0 : -t * 1.6 * sc; c.beginPath(); c.arc(O[0], O[1], rr, 0, TAU); c.stroke(); c.setLineDash([]);
      }
      if (b[2] > 0.02) {   // rising: a bright ring kindling
        const k = still ? 1 : 0.75 + 0.25 * Math.sin(t * 3 + i);
        c.globalAlpha = b[2] * 0.85 * k; c.strokeStyle = rgba(GOLD2, 1); c.lineWidth = Math.max(0.8, 1.2 * sc); c.beginPath(); c.arc(O[0], O[1], rr, 0, TAU); c.stroke();
        c.globalAlpha = b[2] * 0.25 * k; c.lineWidth = 3.5 * sc; c.stroke();
        if (still) for (let s = 0; s < 3; s++) {   // a still frame keeps three sparks, so it still reads as kindling
          const d = (5 + s * 4.5) * sc, pr = (s % 2 ? 1 : -1) * (1.5 + s) * sc;
          stamp(c, glow(mix(BR[i], WARM, 0.5)), x + CO[i] * d - SI[i] * pr, y + SI[i] * d + CO[i] * pr - s * sc, (2.4 - s * 0.4) * sc, 0.8 - s * 0.18);
        }
      }
      c.globalAlpha = 1;
      // the point itself: a bead of pale ink with a white heart
      const pr = (mini ? 1.6 : 2.1) * sc * (i === hi ? 1.35 : 1);
      c.fillStyle = rgba(PA[i], 0.55 + 0.45 * (1 - b[3] * 0.4)); c.beginPath(); c.arc(x, y, pr, 0, TAU); c.fill();
      c.fillStyle = rgba(WHITE, 0.85); c.beginPath(); c.arc(x, y, pr * 0.45, 0, TAU); c.fill();
    }
    for (const p of sparks) { const f = 1 - p.age / p.life; stamp(c, glow(mix(BR[p.i], WARM, 0.45)), p.x, p.y, p.r * 3.4, f * f); stamp(c, glow(HOT), p.x, p.y, p.r * 1.2, f * 0.9); }
    c.globalAlpha = 1;

    /* the outcome's ink: when a pick moves the colours, drops of ink run along each axis that moved, into the point when
       the colour grew and out of it toward the centre when it shrank, more drops the bigger the move */
    if (flows.length) {
      flows = flows.filter((f) => t - f.t0 < f.n * 0.08 + 1.5);
      for (const f of flows) for (let j = 0; j < f.n; j++) {
        const u = clamp((t - f.t0 - j * 0.08) / 0.95); if (u <= 0 || u >= 1) continue;
        const m = easeIO(u), xp = Math.max(0.05, D.x[f.i]), r0 = f.dir > 0 ? 0.03 : xp, r1 = f.dir > 0 ? xp : 0.03;
        const rr = r0 + (r1 - r0) * m, rt = r0 + (r1 - r0) * easeIO(Math.max(0, u - 0.1)), side = ((j % 3) - 1) * 1.6 * sc;
        const hx = cx + R * rr * CO[f.i] - SI[f.i] * side, hy = cy + R * rr * SI[f.i] + CO[f.i] * side, tx = cx + R * rt * CO[f.i] - SI[f.i] * side, ty = cy + R * rt * SI[f.i] + CO[f.i] * side;
        c.globalAlpha = 1; c.strokeStyle = rgba(BR[f.i], 0.5 * Math.sin(Math.PI * u)); c.lineWidth = 1.6 * sc; c.beginPath(); c.moveTo(tx, ty); c.lineTo(hx, hy); c.stroke();
        stamp(c, glow(PA[f.i]), hx, hy, (2.5 + f.mag * 2) * sc, 0.95 * Math.sin(Math.PI * u));
      }
      for (const f of flows) {   // a ring of ink where the drops land
        const u = clamp((t - f.t0 - 0.95 - (f.n - 1) * 0.08 * 0.5) / 0.6); if (u <= 0 || u >= 1) continue;
        const at = f.dir > 0 ? P[f.i] : [cx, cy];
        c.globalAlpha = (1 - u) * 0.7; c.strokeStyle = rgba(BR[f.i], 1); c.lineWidth = 1.2 * sc; c.beginPath(); c.arc(at[0], at[1], (3 + 12 * easeOut(u)) * sc, 0, TAU); c.stroke();
      }
      c.globalAlpha = 1;
    }
    c.globalCompositeOperation = "source-over";
  }

  /* ---------- A4: the shatter, when who they are changes ----------
     For the first quarter second the new cracks shine on the old shape; then the shards burst a little way out, turning,
     and settle into the new shape one after another from the centre outward (with a small overshoot), each keeping the
     body's own ink, its seams a fine dark line. Over the last quarter second the body fades back in under them. */
  function shatter() {
    if (CH.motion() === "off") return;
    if (shat && tt - shat.t0 < 0.3) return;   // scrubbing back and forth: one burst at a time
    shat = { t0: tt, dur: 1.2, old: (G.P ? D.x : st.tx).map((x) => Math.max(0.02, x)) }; rel = null;
    const now = CH.lettersOf(st.label);
    orbs.forEach((o, i) => { if (now.includes(COLORS[i])) pulseOrb(i, "flare"); });
  }
  function drawShatter(c, u, P) {
    const { cx, cy, R, sc } = G, Po = shat.old.map(P_), fill = G.conic || fanFill(P);
    const morph = easeIO(clamp((u - 0.1) / 0.6)), kb = easeOut(clamp(u / 0.2)), xf = 1 - CH.smooth(clamp((u - 0.79) / 0.21)), flash = 1 - clamp(u / 0.21);
    const reach = R * Math.max(0.3, Math.max(...D.x));
    // the core lets go: a flash, and a ring of light out through the glass
    c.globalCompositeOperation = "lighter";
    stamp(c, glow(HOT), cx, cy, R * (0.25 + 0.4 * easeOut(Math.min(1, u * 3))), 0.75 * (1 - u) * (1 - u));
    const rw = clamp(u / 0.6); if (rw < 1) { c.globalAlpha = (1 - rw) * 0.6; c.strokeStyle = rgba(GOLD2, 1); c.lineWidth = (2.2 - 1.5 * rw) * sc; c.beginPath(); c.arc(cx, cy, R * (0.15 + 1.1 * easeOut(rw)), 0, TAU); c.stroke(); c.globalAlpha = 1; }
    c.globalCompositeOperation = "source-over"; c.lineJoin = "round";
    for (const s of SHARDS) {
      const V = s.v.map(([uu, ff]) => { const a = starXY(Po, uu, ff), b = starXY(P, uu, ff); return [a[0] + (b[0] - a[0]) * morph, a[1] + (b[1] - a[1]) * morph]; });
      let mx = 0, my = 0; for (const q of V) { mx += q[0]; my += q[1]; } mx /= V.length; my /= V.length;
      let dx = mx - cx, dy = my - cy; const dl = Math.hypot(dx, dy) || 1; dx /= dl; dy /= dl;
      const ks = easeBack(clamp((u - 0.2 - 0.32 * s.d - s.lag) / 0.45)), k = kb * (1 - ks);
      const off = R * 0.15 * s.burst * k * (0.45 + s.d), rot = s.rot * k;
      c.save();
      c.translate(mx + dx * off, my + dy * off); c.rotate(rot); c.translate(-mx, -my);
      c.beginPath(); V.forEach((q, i) => (i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1]))); c.closePath();
      c.globalAlpha = 0.95 * xf; c.fillStyle = fill; c.fill();
      c.save(); c.clip(); c.globalAlpha = 0.8 * xf; blitHeart(c, reach / R, bbox(V, 1)); c.restore();
      if (flash > 0) { c.globalCompositeOperation = "lighter"; c.globalAlpha = flash * 0.85; c.strokeStyle = rgba(mix(HOT, WARM, 0.4), 1); c.lineWidth = 1.3 * sc; c.stroke(); c.globalCompositeOperation = "source-over"; }
      c.globalAlpha = 0.85 * xf; c.strokeStyle = rgba(INK, 1); c.lineWidth = Math.max(0.5, 0.6 * sc); c.stroke();
      c.restore();
    }
    c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
  }
  /* ---------- A4: the release, when the wanting breaks through and who they are stays the same ---------- */
  function release(items, prevW, near0) {
    if (CH.motion() === "off" || !lay.core) return;
    // the colours it turned them toward: the story line's own colour marks, else the colours that moved, else the strongest wanting
    let ax = [];
    (items || []).forEach((x) => { for (const m of String(x.text || "").matchAll(/⟦v:([WUBRG])⟧/g)) { const i = COLORS.indexOf(m[1]); if (i >= 0 && !ax.includes(i)) ax.push(i); } });
    if (!ax.length && prevW) st.w.forEach((v, i) => { if (Math.abs(v - prevW[i]) > 0.004) ax.push(i); });
    if (!ax.length) { let bi = 0, bv = -1; st.w.forEach((v, i) => { const d = st.want[i] - v; if (d > bv) { bv = d; bi = i; } }); ax = [bi]; }
    rel = { t0: tt, dur: 1.3, ax, cr: Math.max(0.45, clamp(((near0 || 0) - 0.6) / 0.4)) };
    ax.forEach((i) => pulseOrb(i, "flare"));
    dirty = true;
  }

  /* ---------- the outcome's ink flows ---------- */
  function flow(dw) {
    if (!lay.flows || !dw || CH.motion() === "off") return;
    dw.forEach((d, i) => { const m = Math.abs(d); if (m < 0.3) return;   // res.dw is in points of share
      flows.push({ i, dir: Math.sign(d), mag: clamp(m / 4), n: Math.max(2, Math.round((2 + 5 * clamp(m / 4)) * (CH.motion() === "calm" ? 0.6 : 1))), t0: tt + 0.05 }); });
  }
  // restart an orb's one-off animation: "flare" (it lights and swells) or "ebb" (it draws in and dims, then returns); the
  // class goes when it ends, so the orb's hover and focus lift work again
  function pulseOrb(i, cls) {
    const o = orbs[i]; o.classList.remove("flare", "ebb");
    // put back on the next frame, so the animation starts again without the page being laid out there and then
    requestAnimationFrame(() => { if (!o.isConnected) return; o.classList.add(cls); o.addEventListener("animationend", () => o.classList.remove(cls), { once: true }); });
  }
  /* A1, an outcome landing (the page's "outcome" event, its colour moves res.dw in points of share): the person visibly
     takes it in. How strongly is k, all five moves together over 4 points (a move of 4 points or more is the fullest
     breath; the recorded outcomes run from 0 to 18 points, most under 5). The star breathes in by up to 6% of its reach
     and settles back with a small overshoot over 0.9 s, its inks lighting from within; one ring of ink runs out from the
     core in the colour it turned them toward most (the biggest gain); and the orbs of the colours that moved most (a
     third of a point or more, and at least a third of the biggest move) flare when the colour grew or draw in when it
     shrank. An outcome that moved them by less than about a sixth of a point in all shows nothing extra: nothing moved.
     Motion off draws nothing extra (the still frame already shows the new shape). */
  function breathe(dw) {
    if (!lay.flows || !dw || CH.motion() === "off") return;
    const tot = dw.reduce((t, d) => t + Math.abs(d), 0), k = clamp(tot / 4); if (k < 0.04) return;
    let gain = 0; dw.forEach((d, i) => { if (d > dw[gain]) gain = i; });
    breath = { t0: tt, dur: 0.9, k, i: gain };
    const top = Math.max(...dw.map(Math.abs));
    dw.forEach((d, i) => { if (Math.abs(d) >= Math.max(0.3, 0.35 * top)) pulseOrb(i, d > 0 ? "flare" : "ebb"); });
    dirty = true;
  }
  /* the page's "outcome" event (living/90-game.js: after the outcome's reveal). The wheel's frames that waited for it start
     now. The same outcome is taken once (the page may send it again within a moment). A quiet one (the outcome a load
     came back to) and a star that is not on screen let it pass, so it does not play a stale breath when it is shown. */
  const offOutcome = opts.listen === false ? null : CH.on("outcome", (x) => {
    go();
    const r = x && x.res, now = performance.now(); if (!r || !r.dw || x.quiet || (r === lastRes && now - lastResAt < 800)) return;
    lastRes = r; lastResAt = now;
    if (!root.isConnected || !root.getClientRects().length) return;
    flow(r.dw); breathe(r.dw);
  });
  const offMotion = CH.on("motion", (m) => { if (m === "off") { snap(); orbs.forEach((o) => o.classList.remove("flare", "ebb")); } dirty = true; });

  /* ---------- hover: symbol first, words on hover ---------- */
  function setHover(h) {
    const same = h && hover && h.k === hover.k && h.i === hover.i && h.p === hover.p && h.key === hover.key;
    if (!same && (h || hover)) { hover = h; dirty = true; litOrbs(); }
  }
  // an orb is lit (.hl, as the wheel's .orb.hl) while its color is hovered on the star, or a card under the mouse ends in it
  const litOrbs = () => orbs.forEach((o, i) => o.classList.toggle("hl", (!!hover && (hover.k === "pt" || hover.k === "hold" || hover.k === "want") && hover.i === i) || st.ends.includes(i)));
  // one nearest-target pass over the points, the anchors and the wanted places, each with its own reach; the closest wins
  function hit(x, y) {
    if (!G.P || !st.has) return null;
    const sc = G.sc, d2 = (p) => (x - p[0]) ** 2 + (y - p[1]) ** 2;
    let best = null, bv = 1;
    const near = (p, r, h) => { const v = d2(p) / (r * r); if (v < bv) { bv = v; best = h; } };
    G.P.forEach((p, i) => near(p, 7 * sc + 3, { k: "pt", i }));
    if (lay.tethers) G.H.forEach((p, i) => near(p, 5 * sc + 3, { k: "hold", i }));
    if (lay.ghost) G.Wp.forEach((p, i) => { if (Math.abs(D.xw[i] - D.x[i]) * G.R > 2.5) near(p, 5 * sc + 3, { k: "want", i }); });
    if (best) return best;
    if (lay.core && d2([G.cx, G.cy]) < Math.max(10, G.R * 0.14) ** 2) return { k: "core" };
    // a string or an arc answers only when it can be seen
    if (lay.threads) for (let j = 0; j < PAIRS.length; j++) {
      const p = PAIRS[j], q = PS[j]; if (D.pair[j] * D.pair[j] < 0.15) continue;
      if (p.foe) { if (q.bow && bowDist(x, y, q.bow) < 5 * sc + 2) return { k: "thr", p: j }; }
      else if (q.ra) { const r = Math.hypot(x - G.cx, y - G.cy), a = Math.atan2(y - G.cy, x - G.cx), rel_ = ((a - ANG[p.a]) % TAU + TAU) % TAU;
        if (Math.abs(r - q.ra) < 4 * sc + 2 && rel_ > 0.12 && rel_ < TAU / 5 - 0.12) return { k: "arc", p: j }; }
    }
    if (ctx.isPointInPath(cpath("body", G.P).p, x * G.k, y * G.k)) return { k: "body" };
    return null;
  }
  function bowDist(x, y, [A, C, B]) {
    let best = 1e9, px = A[0], py = A[1];
    for (let k = 1; k <= 16; k++) { const s = k / 16, u = 1 - s, qx = u * u * A[0] + 2 * u * s * C[0] + s * s * B[0], qy = u * u * A[1] + 2 * u * s * C[1] + s * s * B[1];
      best = Math.min(best, segDist(x, y, [px, py], [qx, qy])); px = qx; py = qy; }
    return best;
  }
  function segDist(x, y, a, b) { const dx = b[0] - a[0], dy = b[1] - a[1], l = dx * dx + dy * dy || 1, u = clamp(((x - a[0]) * dx + (y - a[1]) * dy) / l); return Math.hypot(x - a[0] - dx * u, y - a[1] - dy * u); }
  /* a child too young for who they are to have formed: no name yet, and the game says why (S.meaning "too young for who
     they are to have formed", S.young). Then no colour joins who they are, however far past 22% it is (Red stands at 32
     to 34% from 5 to 11 in the recorded life and is still only "rising"). */
  const tooYoung = () => { const S = st.S || {}; return !st.label && (!!S.young || /^too young/i.test(String(S.meaning || ""))); };
  // a colour past the edge (above 22%) that is not part of who they are (rising, or out before their first stop)
  const pastNotIn = (i) => st.w[i] > CH.IDENT.enter && (st.bands[i] === "rising" || st.bands[i] === "out");
  // the Place row and the orb's name for a screen reader: the game's band words, saying "past 22%" when it is
  function placeWord(i) {
    if (pastNotIn(i)) return tooYoung() ? "past 22%, but too young for who they are to have formed" : "rising: past 22%, not yet part of them";
    return BAND_WORD[st.bands[i]] || "";
  }
  // the tip's last line: what the colour's place means, from the same bands as the Place row and the orb, saying honestly
  // why a colour is not part of who they are yet (too young, or the name they go by, S.label, has not caught up yet), and
  // promising "it joins above 22%" only to a colour that is not past 22% already
  function placeFoot(i) {
    const c = COLORS[i], N = CH.NAME[c], b = st.bands[i], inL = CH.lettersOf(st.label).includes(c), young = tooYoung();
    if (b === "in") return !st.label ? `${N} is part of who they are; their name is still forming.` : inL ? `${N} is part of who they are; it leaves below 18%.` : `${N} is past 22% now, so it has joined who they are; the name they go by has not caught up yet.`;
    if (b === "fading") return inL || !st.label ? `${N} is still part of who they are, held by the edge; it leaves below 18%.` : `${N} is held by the edge, still part of who they are; the name they go by has not caught up yet.`;
    if (pastNotIn(i)) return young ? `${N} is past 22%, but who they are has not formed yet: they are still too young.` : !st.label ? `${N} is past 22%, but who they are has not formed yet.` : `${N} is past 22%; the name they go by has not caught up yet.`;
    if (b === "rising") return young ? `${N} is above 18%, but who they are has not formed yet: they are still too young.` : `${N} is above 18% but not yet part of who they are; it joins above 22%.`;
    if (young) return "Their colors are still forming: they are too young for who they are to have formed.";
    if (!st.label) return "Their colors are still forming; a color joins who they are above 22%.";
    return inL ? `${N} has dropped out of who they are; the name they go by has not caught up yet.` : `${N} is not part of who they are; it joins above 22%.`;
  }
  // a color's hover: the page's own reading (05-hud.js tipColor) of the life given by opts.tipL, as the wheel's; without
  // one (the interlude's small star, which follows the weeks), the star's reading of what it draws
  function colorTip(i) {
    const L = opts.tipL && opts.tipL();
    if (L && L.w && L.demand && typeof tipColor === "function") return tipColor(L, i);
    const c = COLORS[i], w = st.w[i], T = st.T[i];
    const tether = Math.abs(st.thx[i] - st.tx[i]) * G.R < 2 ? "held right where they are" : T > 0.35 ? "taut: what holds them pulls against what they want" : "slack: what holds them does not pull against their wanting";
    return CH.tipBox(`${CH.pip(c)} ${CH.NAME[c]}`, IDEA[c], [
      ["Now", `<b>${CH.pct(w)}</b>`],
      ["Wants", `${CH.pct(Math.max(0, st.want[i]))} (${pts(st.want[i] - w)})`],
      ["Holds", CH.pct(st.hold[i])],
      ["Place", placeWord(i)],
      ["Could change", `${speedWord(st.acc[i])} (${CH.pct(st.acc[i])})`],
      ["Tether", tether]],
      placeFoot(i));
  }
  function tipFor(h) {
    if (!h) return "";
    if (h.k === "pt") return colorTip(h.i);
    if (h.k === "hold") { const c = COLORS[h.i]; return CH.tipBox(`${CH.pip(c)} What holds their ${CH.NAME[c]}`, "", [["Holds", CH.pct(st.hold[h.i])], ["Now", CH.pct(st.w[h.i])]], STAR_KEY[2][2]); }
    if (h.k === "want") { const c = COLORS[h.i]; return CH.tipBox(`${CH.pip(c)} Where their ${CH.NAME[c]} wants to be`, "", [["Wants", CH.pct(st.want[h.i])], ["Now", CH.pct(st.w[h.i])]], STAR_KEY[1][2]); }
    if (h.k === "core") { const n = st.near; return CH.tipBox("Pent-up wanting", WANTING_DEF, [["Now", CH.cap(nearWord(n))], ["Pent up", `${CH.pct(n)} (it breaks through at 100%)`]],
      "It glows warmer as it builds, and cracks past 60%. A breakthrough closes the cracks in gold; a change in who they are shatters the star into its new shape."); }
    if (h.k === "thr") { const p = PAIRS[h.p], a = COLORS[p.a], b = COLORS[p.b], m = Math.min(st.w[p.a], st.w[p.b]), strong = m >= 0.25;
      return CH.tipBox(pairName(p), `Across the circle from each other, and both ${strong ? "strong in them" : "held"}: a string pulled from both ends.`,
        [[CH.NAME[a], CH.pct(st.w[p.a])], [CH.NAME[b], CH.pct(st.w[p.b])], ["The hum", st.near >= 0.6 ? "loud: much wanting is pent up" : strong ? "strong: both are held evenly" : "soft"]],
        `${CH.cap(VALUE[a])} pulls against ${VALUE[b]}. Each choice for one is a little choice against the other. It hums harder the more evenly both are held and the more wanting is pent up.`); }
    if (h.k === "arc") { const p = PAIRS[h.p], a = COLORS[p.a], b = COLORS[p.b], strong = Math.min(st.w[p.a], st.w[p.b]) >= 0.25;
      return CH.tipBox(pairName(p), `Neighbours on the circle, and both ${strong ? "strong in them" : "held"}: allies.`, [[CH.NAME[a], CH.pct(st.w[p.a])], [CH.NAME[b], CH.pct(st.w[p.b])]],
        `${CH.cap(VALUE[a])} and ${VALUE[b]} help each other along.`); }
    if (h.k === "body") { const ls = CH.lettersOf(st.label), S = st.S || {};
      return CH.tipBox(`${ls.map(CH.pip).join("")} ${CH.esc(CH.guild(S))}`, "Who they are now: the five colors as shares of 100. Each color shines as strongly as its share.", COLORS.map((c, i) => [`${CH.pip(c)} ${CH.NAME[c]}`, CH.pct(st.w[i])]), "Hover a point for its color, the core for pent-up wanting."); }
    return "";
  }
  CH.canvasTip(cv, (x, y) => { const h = hit(x, y); setHover(h); cv.style.cursor = h ? "help" : ""; return tipFor(h); }, { outside: true });
  cv.addEventListener("pointerleave", () => setHover(null));

  /* ---------- the loop ---------- */
  let skip = false, owed = 0;
  const offFrame = CH.frame((now, dt) => {
    const m = CH.motion();
    tick(performance.now());
    if (G.pw !== cv.width || G.ph !== cv.height) dirty = true;
    if (m === "off") { if (dirty) { snap(); render(0, true); dirty = false; } return; }
    // only breathing: every other frame (30 a second), the skipped time carried into the next step
    if (!dirty && st.has && idle()) { skip = !skip; if (skip) { owed += dt; return; } } else skip = false;
    const d = Math.min(0.1, dt + owed); owed = 0;
    const calm = m === "calm";
    tt += d * (calm ? 0.35 : 1);
    if (st.has) { layout(); step(d * (calm ? 0.55 : 1), tt, calm); }
    render(tt, false); dirty = false;
  }, root);

  const api = {
    update, play, go, follow,
    frame: (f) => { if (following) frameShape(f, true); },
    // the voice row read (its toward, per color) or left (null): the arrows, and the voice's ink running along the star
    voice: (tw, still) => { const was = !!st.voice; st.voice = tw ? tw.map((x) => x * 0.15) : null; dirty = true; if (tw && !was && !still) flow(tw.map((x) => x * 15)); },
    // the colors of the card under the mouse (indexes), or none
    ends: (ix) => { const e = ix || []; if (e.join() === st.ends.join()) return; st.ends = e; litOrbs(); dirty = true; },
    refit: () => { fitRoot(); cv.fit(); bg.fit(); dirty = true; },
    jump: () => { snap(); dirty = true; },
    // what is drawn, for the drivers (read only)
    peek: () => ({ has: st.has, w: st.w.slice(), label: st.label, bands: st.bands.slice(), x: D.x.slice(), s: root._s || 0, following, playing: !!tl,
      waiting: !!(tl && tl.t0 === Infinity), shadow: D.sh.slice(), voice: !!st.voice, ends: st.ends.slice(), shat: !!shat, rel: !!rel, breath: !!breath, flows: flows.length,
      P: G.P ? G.P.map((q) => q.slice()) : null, c: [G.cx, G.cy], R: G.R, box: cv.getBoundingClientRect().toJSON(), age: st.age }),
    destroy() { offFrame(); if (offOutcome) offOutcome(); offMotion(); if (ro) ro.disconnect(); root.remove(); },
  };
  root.lvPeek = api.peek;   // test/drive_living_star.js reads it from the element
  return api;
}

// the key's small symbols, drawn to match the star (they read on the parchment panel and on night glass alike)
function keySVG(k, gid) {
  const st = `<svg class="st-ks" viewBox="0 0 30 22" aria-hidden="true">`;
  if (k === "pos") return st + `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2e3a6"/><stop offset=".3" stop-color="#82b9f2"/><stop offset=".55" stop-color="#bba0d0"/><stop offset=".78" stop-color="#f38c6b"/><stop offset="1" stop-color="#7fd394"/></linearGradient></defs>
    <polygon points="15,2 24,8.6 20,19 9.5,18 6.5,9.5" fill="url(#${gid})" stroke="#2a2116" stroke-opacity=".75" stroke-width="1" stroke-linejoin="round"/><circle cx="15" cy="11" r="2.4" fill="#fffaf0" opacity=".85"/></svg>`;
  if (k === "want") return st + `<polygon points="15,1.5 26,9 21.5,20.5 8.5,20.5 4,9" fill="#b79cf3" fill-opacity=".14" stroke="#7a68dc" stroke-width="1.3" stroke-linejoin="round"/><path d="M15 6.5q.3 3.2 2.6 3.5q-2.3.3-2.6 3.5q-.3-3.2-2.6-3.5q2.3-.3 2.6-3.5z" fill="#7a68dc"/></svg>`;
  if (k === "hold") return st + `<path d="M5 6 Q 14 17 25 13" fill="none" stroke="#8a6a2c" stroke-width="1"/><circle cx="5" cy="6" r="2.2" fill="#bba0d0" stroke="#2a2116" stroke-opacity=".6" stroke-width=".7"/><circle cx="25" cy="13" r="3.2" fill="#d8b469" stroke="#6b5020" stroke-width=".9"/><circle cx="25" cy="13" r="1" fill="#2a2116"/></svg>`;
  if (k === "pull") return st + `<defs><linearGradient id="${gid}" x1="0" x2="1"><stop offset="0" stop-color="#1f4f8a"/><stop offset="1" stop-color="#b03c1d" stop-opacity=".35"/></linearGradient></defs>
    <path d="M3 8 L27 11 L3 14 Z" fill="url(#${gid})"/><circle cx="11" cy="11" r="1.8" fill="#82b9f2"/><circle cx="19" cy="11" r="1.4" fill="#f3ae90"/></svg>`;
  if (k === "after") return st + `<polygon points="15,1.5 26.5,9.5 22,21 8,21 3.5,9.5" fill="none" stroke="#8d97ad" stroke-width=".9" stroke-linejoin="round" opacity=".75"/><polygon points="15,5.5 22.5,10.5 19.5,18 10.5,18 7.5,10.5" fill="#bba0d0" fill-opacity=".35" stroke="#2a2116" stroke-opacity=".6" stroke-width=".8" stroke-linejoin="round"/><circle cx="26.5" cy="9.5" r="1.3" fill="#c9d1e0" stroke="#5d6578" stroke-width=".5"/><circle cx="24.4" cy="10" r=".9" fill="#c9d1e0" opacity=".75"/></svg>`;
  if (k === "core") return st + `<defs><radialGradient id="${gid}"><stop offset="0" stop-color="#fff4d6"/><stop offset=".35" stop-color="#ffcc7a"/><stop offset="1" stop-color="#b79cf3" stop-opacity="0"/></radialGradient></defs><circle cx="15" cy="11" r="9.5" fill="url(#${gid})"/><path d="M15 11 L18.5 7 L20.5 3.5 M15 11 L10.5 14.5 L9 18.5 M15 11 L21 14" fill="none" stroke="#8a6a2c" stroke-width=".8" stroke-linecap="round"/></svg>`;
  return st + `<path d="M3 19 A 14 14 0 0 1 27 19" fill="none" stroke="#d8b469" stroke-opacity=".4" stroke-width="5"/><path d="M3 19 A 14 14 0 0 1 27 19" fill="none" stroke="#8a6a2c" stroke-width=".8"/><circle cx="23.5" cy="6" r="3.4" fill="none" stroke="#8a6a2c" stroke-width="1.1" stroke-dasharray="2 1.4"/></svg>`;
}

/* ======================================================================================================================
   The piece: the star on the game page. living/90-game.js mounts it while the Living HUD is on and takes it down when it is
   turned off (today's wheel comes back with the HUD's redraw). Only one star is on screen at a time (decision 4): the
   HUD's, over the wheel; in the everyday interlude on narrow screens (IL.side: the HUD is a drawer there) a small one takes
   #ilWheel's place for the interlude. The character sheet keeps today's wheel. */
let hudStar = null, hudHost = null, ilStar = null, ilHost = null, ilFailed = null, lastS = null, ctxRef = null, ilK = -1, drawerMo = null;
const lerp5 = (a, b, f) => a.map((v, i) => v + ((b && b[i] != null ? b[i] : v) - v) * f);
// the HUD's star sits in .wheelw right after svg#hudWheel, which stays laid out but hidden (IL.side reads its offsetParent).
// renderHud rebuilds the panel, so the same host (and star, mid-motion) is put back after each redraw.
function place() {
  const svg = $("hudWheel"), wrap = svg && svg.closest(".wheelw");
  if (!hudHost || !wrap) return false;
  if (svg.nextElementSibling !== hudHost) svg.after(hudHost);
  return true;
}
// #wKey reads the star's key: its symbols with the wheel's exact definitions
const keyTip = () => tipBox(`${ic("wheel")} How to read the star`, "", STAR_KEY.map(([k, w, d]) => [`<span class="st-ktt">${keySVG(k, "lvk" + k)}</span> ${w}`, esc(d)]), "Hover a color for its numbers.");
// today's key, as renderHud writes it from the page's SP_KEY (put back when the star goes while the interlude holds the
// panel, which is not drawn again at once)
const wheelKeyTip = () => tipBox(`${ic("wheel")} How to read the wheel`, "", SP_KEY.map(([k, w, d]) => [`<i class="spk k-${k}"></i> ${w}`, esc(d)]), "Hover a color for its numbers.");
function bindHud(L) {
  const k = $("wKey"); if (k) { setTip(k, keyTip); k.setAttribute("aria-label", "How to read the star"); }
  // the voice in their head (item 3): its row's hover runs the voice's ink along the star and shows where it pushes
  const vr = $("voiceRow"), V = L && L.voice_row;
  if (!hudStar) return;
  if (!vr || !V || !V.steer) { hudStar.voice(null); return; }
  const on = () => hudStar && hudStar.voice(V.toward), off = () => hudStar && hudStar.voice(null);
  vr.addEventListener("mouseenter", on); vr.addEventListener("mouseleave", off); vr.addEventListener("focus", on); vr.addEventListener("blur", off);
  hudStar.voice(vr.matches(":hover") || document.activeElement === vr ? V.toward : null, true);   // the row was redrawn under the mouse
}
// a card under the mouse lights its colors' orbs and axes, as it lights the wheel's .orb today (06-moment.js bindOpt)
function cardEnds(b) {
  const o = b && hud && hud.cp && hud.cp.options && hud.cp.options[+b.dataset.i], e = (o && o.ends) || "";
  if (hudStar) hudStar.ends(COLORS.map((c, i) => (e.includes(c) ? i : -1)).filter((i) => i >= 0));
}
const onOver = (e) => { if (e.pointerType !== "touch") cardEnds(e.target.closest && e.target.closest(".opt[data-i]")); };
const onOut = (e) => { const to = e.relatedTarget && e.relatedTarget.closest ? e.relatedTarget.closest(".opt[data-i]") : null; cardEnds(to && tableEl.contains(to) ? to : null); };
// the interlude's week at IL.k (07-interlude.js ilStep): the wheel's frames, eased between two weeks
function ilFrame() {
  const N = IL.frames ? IL.frames.length : 0; if (!N) return null;
  const k = Math.floor(IL.k), f = IL.k - k, A = IL.frames[k], B = IL.frames[Math.min(N - 1, k + 1)], C = f < 0.5 ? A : B;
  return { w: lerp5(A.w, B.w, f), want: lerp5(A.want || A.w, B.want || B.w, f), bands: C.bands, label: C.label };
}
// the small star in the interlude on narrow screens: over #ilWheel, made for each interlude (the interlude redraws its card)
function ilMini(fr) {
  const svg = $("ilWheel"), side = svg && svg.closest(".ilside");
  if (!side) return null;
  if (ilStar && ilHost && ilHost.parentNode === side) return ilStar;
  dropIl();
  if (ilFailed === side) return null;
  ilHost = document.createElement("div"); ilHost.className = "lv-star lv-il";
  svg.after(ilHost);
  try {
    ilStar = mount(ilHost, { size: "mini", frame: "glass", listen: false });
    ilStar.update(lastS || ctxRef.state(), { quiet: true }); ilStar.follow(true); ilStar.frame(fr); ilStar.jump();
  } catch (e) { console.warn("living: the interlude's star did not start, today's wheel stays", e); ilFailed = side; dropIl(); return null; }
  return ilStar;
}
function dropIl() { const s = ilStar; ilStar = null; if (s) { try { s.destroy(); } catch (_) {} } if (ilHost) ilHost.remove(); ilHost = null; ilK = -1; }
// the interlude is over (or never was): the HUD's star follows the states again and the small one goes
function ilOver() { if (IL.on) return; dropIl(); if (hudStar) hudStar.follow(false); }

CH.piece("star", {
  order: 20,
  mount(ctx) {
    ctxRef = ctx;
    hudHost = document.createElement("div"); hudHost.className = "lv-star";
    try { hudStar = mount(hudHost, { size: "full", frame: "glass", tipL: () => hud && hud.life }); }
    catch (e) { console.warn("living: the star did not start, today's wheel stays", e); hudHost = null; hudStar = null; return false; }
    if (place() && hud && hud.life) bindHud(hud.life);
    tableEl.addEventListener("pointerover", onOver); tableEl.addEventListener("pointerout", onOut);
    // the drawer at 1040 px or less: the star measures again when it opens
    try { drawerMo = new MutationObserver(() => { if (hudEl.classList.contains("open") && hudStar) requestAnimationFrame(() => hudStar && hudStar.refit()); });
      drawerMo.observe(hudEl, { attributes: true, attributeFilter: ["class"] }); } catch (_) { drawerMo = null; }
    return true;
  },
  update(S, how) {
    lastS = S;
    if (!IL.on) ilOver(); else if (!IL.side && hudStar) hudStar.follow(true);
    if (hudStar) { place(); hudStar.update(S, how); }
    if (ilStar) ilStar.update(S, how);
  },
  destroy() {
    dropIl();
    tableEl.removeEventListener("pointerover", onOver); tableEl.removeEventListener("pointerout", onOut);
    if (drawerMo) drawerMo.disconnect(); drawerMo = null;
    const s = hudStar; hudStar = null; if (s) s.destroy();
    if (hudHost) hudHost.remove(); hudHost = null;
    // #wKey as today's (the HUD is drawn again by the switch, except under the interlude, which keeps the panel)
    const k = $("wKey"); if (k) { setTip(k, wheelKeyTip); k.setAttribute("aria-label", "How to read the wheel"); }
    lastS = null; ilFailed = null;
  },
  hooks: {
    // after each redraw of the panel: the host back over the wheel, #wKey and the voice row bound to the star
    renderHud(L) { if (!place()) return; bindHud(L); ilOver(); },
    // the wheel's week-by-week motion plays on the star instead (the wheel jumps to its last frame, hidden); an outcome's
    // waits for the outcome to show (the "outcome" event, 3 s at most), as the ink look holds the wheel for it
    animSpider(svg, fs, ms) {
      if (!hudStar || !svg || svg.id !== "hudWheel") return false;
      hudStar.play(fs, ms, typeof choosing !== "undefined" && choosing ? 3000 : 0);
      return true;
    },
    // the interlude: the HUD's star follows the weeks on wide screens; on narrow ones the small star does
    ilStep() {
      if (!IL.on || IL.k === ilK) return;
      const fr = ilFrame(); if (!fr) return;
      ilK = IL.k;
      if (!IL.side) { if (hudStar) { hudStar.follow(true); hudStar.frame(fr); } return; }
      const m = ilMini(fr); if (m) m.frame(fr);
    },
    // a new moment or outcome: no card is under the mouse any more
    renderTable() { if (hudStar && !tableEl.querySelector(".opt[data-i]:hover")) hudStar.ends([]); },
  },
});
})();
