"use strict";
/* ---------------- the Living HUD: its core (v23 rows V0 to V6; plan: the Living HUD in v23, section 2) ----------------
   The shared base every living piece stands on, ported from the showcase's core.js: the five colours and their pairs,
   small helpers, seeded noise, events, one frame loop, canvases, the live life (CH.life, kept by living/90-game.js from
   the game's own states) and the bridges into the page: tooltips go through the page's one #tip (setTip, tipBox,
   showTipAt, hideTip), marked text through rich(), icons and pips through ic() and pip(), and the motion setting is the
   ink look's own (html[data-motion]). Left out of the showcase's core: its own tooltip box, the pips' title=, CH.load and
   the recorded life (CH.at, CH.synth), its own motion key (chs.motion) and the gallery's demos.
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

/* ---------- events ---------- */
const subs = new Map();
CH.on = (ev, fn) => { if (!subs.has(ev)) subs.set(ev, new Set()); subs.get(ev).add(fn); return () => subs.get(ev).delete(fn); };
CH.emit = (ev, x) => { (subs.get(ev) || []).forEach((fn) => { try { fn(x); } catch (e) { console.error("living: " + ev, e); } }); };
// Events (living/90-game.js): "moment" {cp, S, quiet} and "outcome" {res, S, quiet} when the page shows them; "pick"
// {cp, o, text, S} when a card is sent; "living" (true while time runs between moments); "motion" (full | calm | off);
// "piece" (a name, when a piece registers); "resize" after CH.refit().

/* ---------- motion: the ink look's own setting (Table menu: full, calm, off; the system's reduced motion counts as off) ----------
   look.js keeps it on html[data-motion]; any change to it, to the look or to the Living HUD switch is told as "motion" */
const MOTIONS = ["full", "calm", "off"];
CH.motion = () => { const m = root.dataset.motion; return MOTIONS.includes(m) ? m : reducedMotion() ? "off" : "full"; };
CH.motionForced = () => reducedMotion();
CH.speed = () => ({ full: 1, calm: 0.35, off: 0 }[CH.motion()]);
try {
  new MutationObserver((rs) => { if (rs.some((r) => root.getAttribute(r.attributeName) !== r.oldValue)) CH.emit("motion", CH.motion()); })
    .observe(root, { attributes: true, attributeOldValue: true, attributeFilter: ["data-motion", "data-look", "data-living"] });
} catch (e) { console.warn("living: no MutationObserver, motion changes are not told", e); }

/* ---------- one frame loop: pieces add a draw(now, dt) and are called only while visible and the tab is shown ---------- */
const drawers = new Set(); let raf = 0, lastT = 0;
CH.frame = (fn, el) => { const d = { fn, el, on: true }; drawers.add(d);
  if (el && "IntersectionObserver" in window) { const io = new IntersectionObserver((es) => { d.on = es.some((e) => e.isIntersecting); }); io.observe(el); d.io = io; }
  if (!raf) raf = requestAnimationFrame(tick); return () => { drawers.delete(d); if (d.io) d.io.disconnect(); }; };
function tick(t) {
  const dt = Math.min(0.1, lastT ? (t - lastT) / 1000 : 0.016); lastT = t;
  if (!document.hidden) drawers.forEach((d) => { if (d.on && !d.dead) { try { d.fn(t / 1000, dt); } catch (e) { console.error("living: frame", e); d.dead = true; } } });
  raf = drawers.size ? requestAnimationFrame(tick) : 0;
}
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
