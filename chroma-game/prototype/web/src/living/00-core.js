"use strict";
/* ---------------- the Living HUD: its core (v23 rows V0 to V6; plan: the Living HUD in v23, section 2) ----------------
   The shared base every living piece stands on, ported from the showcase's core.js: the five colours and their pairs,
   small helpers, seeded noise, events, one frame loop (timed piece by piece, with a guard: CH.cost), canvases, the live
   life (CH.life, kept by living/90-game.js from the game's own states) and the bridges into the page: tooltips go
   through the page's one #tip (setTip, tipBox, showTipAt, hideTip), marked text through rich(), icons and pips through
   ic() and pip(), and the motion setting is the ink look's own (html[data-motion]). Left out of the showcase's core: its
   own tooltip box, the pips' title=, CH.load and the recorded life (CH.at, CH.synth), its own motion key (chs.motion)
   and the gallery's demos.
   Every piece registers here with CH.piece(name, spec); living/90-game.js mounts the pieces while the Living HUD is on
   (Table menu, ink look only), feeds them a new state S at each update and takes them down when it is turned off. */
(() => {
const CH = (window.CH = window.CH || {});
CH.mods = CH.mods || {};
const root = document.documentElement;

/* ---------- the five colours ---------- */
CH.COLORS = ["W", "U", "B", "R", "G"];
CH.NAME = { W: "White", U: "Blue", B: "Black", R: "Red", G: "Green" };
// the game's own tokens (style/01-base.css and look.js INK): bright, deep, pale plate, engraving ink
CH.HUE = {
  bright: { W: "#f2e3a6", U: "#82b9f2", B: "#bba0d0", R: "#f38c6b", G: "#7fd394" },
  deep: { W: "#8d7a3b", U: "#1f4f8a", B: "#3a2d4b", R: "#8c2f1f", G: "#1f6136" },
  pale: { W: "#f8f1d3", U: "#abcff1", B: "#c3b8bf", R: "#f3ae90", G: "#addaa1" },
  ink: { W: "#8f7116", U: "#1c5ca2", B: "#4e3966", R: "#b03c1d", G: "#22733e" },
};
CH.rgb = (hex) => { const n = parseInt(hex.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
// Magic's pie around the circle W U B R G: neighbours are allies, the two across are enemies (engine.ENEMY)
CH.ALLY = [["W", "U"], ["U", "B"], ["B", "R"], ["R", "G"], ["G", "W"]];
CH.ENEMY = [["W", "B"], ["W", "R"], ["U", "R"], ["U", "G"], ["B", "G"]];
CH.SHADOW = { W: "rigid", U: "indecisive", B: "ruthless", R: "reckless", G: "stuck in their ways" };
CH.IDENT = { enter: 0.22, leave: 0.18 };     // a colour joins who they are above 22% and leaves below 18% (engine.identity)
CH.lettersOf = (label) => CH.COLORS.filter((c) => String(label || "").includes(c));
// the same square-root radius as the game's spider graph (05-hud.js spRad): 0..0.8 of a share onto 0..1
CH.spR = (v) => Math.sqrt(Math.min(0.8, Math.max(0, v)) / 0.8);

/* ---------- small helpers ---------- */
CH.clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
CH.lerp = (a, b, t) => a + (b - a) * t;
CH.lerpArr = (A, B, t) => (A && B ? A.map((v, i) => v + ((B[i] ?? v) - v) * t) : A || B);
CH.smooth = (t) => t * t * (3 - 2 * t);
CH.pct = (v) => `${Math.round((v || 0) * 100)}%`;
CH.esc = (s) => String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
CH.cap = (s) => (s ? String(s)[0].toUpperCase() + String(s).slice(1) : "");
// a seeded random stream (mulberry32): decoration may vary, but the same seed always draws the same way
CH.rng = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
// 2D value noise with smooth interpolation, enough for drifting fog, ink edges and flow fields
const P = new Uint8Array(512); { const r = CH.rng(7); const p = [...Array(256).keys()]; for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } for (let i = 0; i < 512; i++) P[i] = p[i & 255]; }
const hash = (x, y) => P[(P[x & 255] + y) & 511] / 255;
CH.noise = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = CH.smooth(xf), v = CH.smooth(yf);
  return CH.lerp(CH.lerp(hash(xi, yi), hash(xi + 1, yi), u), CH.lerp(hash(xi, yi + 1), hash(xi + 1, yi + 1), u), v); };
CH.fbm = (x, y, o = 4) => { let s = 0, a = 0.5, f = 1; for (let i = 0; i < o; i++) { s += a * CH.noise(x * f, y * f); f *= 2; a *= 0.5; } return s; };

/* ---------- the story text's markers: the page's own rich() (01-base.js), which also writes data-mk, data-pl and chips ---------- */
CH.rich = (s) => rich(s);
CH.plain = (s) => plainText(s).replace(/\*/g, "");

/* ---------- owners: which piece is running now ----------
   living/90-game.js runs each piece's mount, update, hooks and destroy as that piece (CH.as), so whatever a piece starts
   there is its own: a frame function (CH.frame) is measured as the piece's, and an event handler (CH.on) runs as the
   piece. Only the per-piece guard (CH.frame, below) reads it: a piece it has dropped to still frames sees motion "off". */
let owner = "";
CH.owner = () => owner;
CH.as = (name, f) => { const was = owner; owner = name || ""; try { return f(); } finally { owner = was; } };

/* ---------- events ---------- */
const subs = new Map();
CH.on = (ev, fn) => { if (!subs.has(ev)) subs.set(ev, new Set()); const h = { fn, owner }; subs.get(ev).add(h); return () => subs.get(ev).delete(h); };
// each handler runs as the piece that subscribed; "motion" tells each the motion as that piece sees it
const call = (h, ev, x) => { const was = owner; owner = h.owner; try { h.fn(ev === "motion" ? CH.motion() : x); } catch (e) { console.error("living: " + ev, e); } finally { owner = was; } };
CH.emit = (ev, x) => { [...(subs.get(ev) || [])].forEach((h) => call(h, ev, x)); };
// Events (living/90-game.js): "moment" {cp, S, quiet} and "outcome" {res, S, quiet} when the page shows them; "pick"
// {cp, o, text, S} when a card is sent; "living" (true while time runs between moments); "motion" (full | calm | off);
// "piece" (a name, when a piece registers); "resize" after CH.refit().

/* ---------- motion: the ink look's own setting (Table menu: full, calm, off; the system's reduced motion counts as off) ----------
   look.js keeps it on html[data-motion]; any change to it, to the look or to the Living HUD switch is told as "motion" */
const MOTIONS = ["full", "calm", "off"];
const still = new Set();      // the pieces the guard dropped to still frames (CH.frame, below): to them motion is "off"
CH.motion = () => { if (owner && still.has(owner)) return "off"; const m = root.dataset.motion; return MOTIONS.includes(m) ? m : reducedMotion() ? "off" : "full"; };
CH.motionForced = () => reducedMotion();
CH.speed = () => ({ full: 1, calm: 0.35, off: 0 }[CH.motion()]);
try {
  new MutationObserver((rs) => { if (rs.some((r) => root.getAttribute(r.attributeName) !== r.oldValue)) CH.emit("motion", CH.motion()); })
    .observe(root, { attributes: true, attributeOldValue: true, attributeFilter: ["data-motion", "data-look", "data-living"] });
} catch (e) { console.warn("living: no MutationObserver, motion changes are not told", e); }

/* ---------- one frame loop: pieces add a draw(now, dt) and are called only while visible and the tab is shown ----------
   Each draw belongs to the piece that started it (CH.as) and is timed (performance.now() around it, the script's own
   time). The guard (plan step 9): when a piece's draws average more than GUARD_MS a frame over GUARD_S seconds, that
   piece drops to still frames for the rest of the page's life: from then on it sees motion "off" (CH.motion, CH.speed
   and its "motion" handlers), so it draws one still frame for each change the life brings, as every piece does with
   motion off, and it says so once with console.warn. CH.cost() gives drivers what each piece costs.
   A test key: localStorage "chroma.living.guard" = "off" keeps every piece moving (the guard still measures, and says
   once what it would have done), for the drivers that check a piece's own motion on a slow headless machine. */
const GUARD_MS = 6, GUARD_S = 5, KEEP = 1200;   // KEEP: frames kept for CH.cost (about 20 s at 60 frames a second)
const guardOn = () => { try { return localStorage.getItem("chroma.living.guard") !== "off"; } catch (_) { return true; } };
const tripped = new Map();    // the pieces the guard judged too costly: the mean (ms a frame) it judged them by
const drawers = new Set(); let raf = 0, lastT = 0;
CH.frame = (fn, el) => { const d = { fn, el, on: true, owner }; drawers.add(d);
  if (el && "IntersectionObserver" in window) { const io = new IntersectionObserver((es) => { d.on = es.some((e) => e.isIntersecting); }); io.observe(el); d.io = io; }
  if (!raf) raf = requestAnimationFrame(tick); return () => { drawers.delete(d); if (d.io) d.io.disconnect(); }; };
// what each piece's draws cost: the last KEEP frames it drew (ms), the guard's running window, its updates (90-game.js)
const costs = new Map(), all = { a: [], i: 0, total: 0 };
const costOf = (name) => { let c = costs.get(name); if (!c) costs.set(name, (c = { a: [], i: 0, total: 0, t0: 0, last: 0, sum: 0, k: 0, un: 0, us: 0 })); return c; };
const keep = (r, v) => { r.total++; if (r.a.length < KEEP) r.a.push(v); else { r.a[r.i] = v; r.i = (r.i + 1) % KEEP; } };
// the window is GUARD_S seconds of drawing without a break (a piece out of view or a hidden tab starts it again) and at
// least 20 frames, so a few costly frames after a pause are never judged alone
function guard(name, c, ms, t) {
  if (!c.t0 || t - c.last > 1000) { c.t0 = t; c.sum = 0; c.k = 0; }
  c.last = t; c.sum += ms; c.k++;
  if (t - c.t0 < GUARD_S * 1000 || c.k < 20) return;
  const mean = c.sum / c.k; c.t0 = t; c.sum = 0; c.k = 0;
  if (mean <= GUARD_MS || tripped.has(name)) return;
  tripped.set(name, +mean.toFixed(2));
  if (!guardOn()) { console.warn(`living: the ${name} took ${mean.toFixed(1)} ms a frame over ${GUARD_S} s, more than ${GUARD_MS}; the guard is off in this browser, so it keeps moving`); return; }
  still.add(name);
  console.warn(`living: the ${name} took ${mean.toFixed(1)} ms a frame over ${GUARD_S} s, more than ${GUARD_MS}; it now draws only when the life changes`);
  // the piece's own motion handlers hear "off", so it draws its still frame now
  [...(subs.get("motion") || [])].forEach((h) => { if (h.owner === name) call(h, "motion"); });
}
function tick(t) {
  const dt = Math.min(0.1, lastT ? (t - lastT) / 1000 : 0.016); lastT = t;
  if (!document.hidden) {
    const spent = new Map();
    drawers.forEach((d) => {
      if (!d.on || d.dead) return;
      const c0 = performance.now(), was = owner; owner = d.owner;
      try { d.fn(t / 1000, dt); } catch (e) { console.error("living: frame", e); d.dead = true; } finally { owner = was; }
      spent.set(d.owner, (spent.get(d.owner) || 0) + performance.now() - c0);
    });
    let sum = 0;
    spent.forEach((ms, name) => { const c = costOf(name || "page"); keep(c, ms); sum += ms; if (name) guard(name, c, ms, t); });
    if (spent.size) keep(all, sum);
  }
  raf = drawers.size ? requestAnimationFrame(tick) : 0;
}
const stat = (r) => { const s = r.a.slice().sort((p, q) => p - q), n = s.length;
  return { n, frames: r.total, mean: n ? +(s.reduce((x, v) => x + v, 0) / n).toFixed(3) : 0, p95: n ? +s[Math.min(n - 1, Math.floor(n * 0.95))].toFixed(3) : 0, max: n ? +s[n - 1].toFixed(3) : 0 }; };
// CH.cost() -> { piece: { mean, p95, max, n, frames, still, tripped, update } } over the last frames each piece drew (ms
// of script a frame; n: the frames read, at most KEEP; frames: every frame it drew since the counts began; still: the
// guard dropped it to still frames; tripped: the mean the guard judged it by, also when the guard is off; update: its
// mean ms an update, from living/90-game.js); "page" holds draws started outside any piece.
// CH.cost.all(): the same for all the pieces together, a frame at a time. CH.cost.reset() starts the counts over (the
// guard keeps its own window and its verdicts). CH.cost.note(piece, ms) adds one update's time.
CH.cost = () => { const out = {}; costs.forEach((c, name) => { out[name] = Object.assign(stat(c), { still: still.has(name), tripped: tripped.get(name) || null, update: c.un ? +(c.us / c.un).toFixed(3) : 0 }); }); return out; };
CH.cost.all = () => stat(all);
CH.cost.reset = () => { costs.forEach((c) => { c.a = []; c.i = 0; c.total = 0; c.un = 0; c.us = 0; }); all.a = []; all.i = 0; all.total = 0; };
CH.cost.note = (name, ms) => { const c = costOf(name); c.un++; c.us += ms; };
CH.cost.still = (name) => still.has(name);
/* a canvas sized to its box at the device's pixel ratio (at most 2), refitted on resize. c._w and c._h are its size in CSS
   pixels of the layout (draw in those after ctx.setTransform(c._k, 0, 0, c._k, 0, 0)); c._k also carries any CSS scale
   above it, so the bitmap stays crisp at every scale. Refitting writes only the bitmap's size, never the layout. */
const canvases = new Set();
CH.canvas = (host, cls) => {
  const c = document.createElement("canvas"); if (cls) c.className = cls; host.appendChild(c);
  const fit = () => { const r = c.getBoundingClientRect(), lw = c.offsetWidth || r.width, lh = c.offsetHeight || r.height;
    const vs = lw ? r.width / lw : 1, k = Math.min(2, window.devicePixelRatio || 1) * (vs || 1);
    const w = Math.max(1, Math.round(lw * k)), h = Math.max(1, Math.round(lh * k)); if (c.width !== w || c.height !== h) { c.width = w; c.height = h; } c._k = k; c._w = lw; c._h = lh; c._vs = vs || 1; };
  fit(); if ("ResizeObserver" in window) new ResizeObserver(fit).observe(c); c.fit = fit; canvases.add(c); return c;
};
// after the page changes a CSS scale (ResizeObserver does not see transforms): refit every canvas and tell the pieces
CH.refit = () => { canvases.forEach((c) => { if (c.isConnected) c.fit(); else canvases.delete(c); }); CH.emit("resize"); };
// a pointer event's position inside an element, in that element's own CSS pixels (undoing any CSS scale above it)
CH.local = (el, e) => { const r = el.getBoundingClientRect(), vs = el.offsetWidth ? r.width / el.offsetWidth : 1; return [(e.clientX - r.left) / vs, (e.clientY - r.top) / vs]; };

/* ---------- tooltips: the page's one #tip, symbol first and words on hover (the game's rule) ---------- */
CH.tip = (el, fn) => setTip(el, typeof fn === "function" ? fn : () => fn);
CH.tipBox = (title, sub, rows, foot) => tipBox(title, sub, rows, foot);
CH.hideTip = () => hideTip();
/* a canvas region's reading: hit(x, y) in CSS pixels returns html or "". A mouse reads it by hovering; a finger or pen by
   tapping the place, and the reading closes by itself after 3.2 s, as the page's own tapped tips do. opts.outside keeps
   the reading off the picture, beside it. The reading belongs to the pointer (as the life line's), so the page's own
   hover handling leaves it alone. */
CH.canvasTip = (canvas, hit, opts) => {
  let mine = false, shut = 0;
  const close = () => { clearTimeout(shut); if (mine && tipOwner === "line") hideTip(); mine = false; };
  const open = (e) => {
    const [x, y] = CH.local(canvas, e), html = hit(x, y);
    if (!html) { close(); return false; }
    showTipAt(html, e.clientX, e.clientY);
    if (opts && opts.outside) placeTip(canvas.getBoundingClientRect(), true);
    mine = true; return true;
  };
  canvas.addEventListener("pointermove", (e) => { if (e.pointerType === "mouse") open(e); });
  canvas.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse") close(); });
  canvas.addEventListener("pointerup", (e) => {
    if (e.pointerType === "mouse") return;
    setTimeout(() => { if (open(e)) { clearTimeout(shut); shut = setTimeout(close, 3200); } }, 0);
  });
};

/* ---------- icons: the page's own sprite (sprite.svg and the visuals thread's ink-icons.svg are in the page) ---------- */
// ci-* are the visuals thread's woodcut glyphs (filled); i-* and m-* are the page's line icons (stroked). The class "ci"
// stays on each, for the pieces' own rules.
CH.icon = (id, cls) => { const c = ("ci " + (cls || "")).trim();
  return /^i-/.test(id) ? ic(id.slice(2), c) : /^m-/.test(id) ? `<svg class="i ${c}" aria-hidden="true"><use href="#${id}"/></svg>` : ic(id, c); };
CH.glyph = (c, cls) => CH.icon(MANA(c), cls);
CH.pip = (c) => pip(c);

/* ---------- the live life: CH.life, kept by living/90-game.js (a new one for each life and each load) ---------- */
CH.life = null;
// the stop at or before an age, over the stops recorded so far
CH.stopAt = (age) => { const A = (CH.life && CH.life.ages) || []; let lo = 0, hi = A.length - 1; if (hi < 0 || age <= A[0]) return 0; if (age >= A[hi]) return hi;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (A[m] <= age) lo = m; else hi = m; } return lo; };
// is this story line told yet at S? Live, every line the page has is told: it is told when it is not past S's age
CH.seen = (S, x) => { const L = CH.life, it = typeof x === "number" ? L && L.items[x] : x; return !!(it && S && (it.age ?? 0) <= S.age + 1e-6); };
// the identity's names: the game's Chroma name, with Magic's on hover (game_base.py IDENT_NAME / magic_name)
CH.guild = (S) => S.guild || "Still forming";
CH.stageWord = (S) => CH.cap(String(S.stage || "").replace("_", " "));
// Magic's name for who they are, in plain words ("mono-Red" is Magic's shorthand for wholly Red), as the story says it
CH.magicWords = (m) => { if (!m) return ""; const mono = /^mono-(\w+)$/i.exec(m); return mono ? `Magic would call them wholly ${CH.esc(CH.cap(mono[1]))}.` : `Magic would call them ${CH.esc(m)}.`; };

/* ---------- the pieces: each living piece registers its game side here, and living/90-game.js mounts it ----------
   CH.piece(name, { order, mount(ctx), update(S, how), destroy(), hooks }) adds or replaces one. mount() returns false
   when it cannot stand (today's piece then stays); update(S, how) gets a new state S at each update, how.quiet when it
   must not play an arrival (the update after a load, the years lived before the player takes over); destroy() takes it
   down and puts today's piece back. hooks run after the page function of the same name (renderHud, drawLine, ilStep,
   renderTable, renderResolution, renderReview, renderTools) with its arguments; animSpider's hook runs first and returns
   true to skip the wheel's animation (the wheel then jumps to its last frame). */
CH.pieces = CH.pieces || new Map();
CH.piece = (name, spec) => { CH.pieces.set(name, Object.assign({ order: 50 }, spec, { name })); CH.emit("piece", name); };
})();
