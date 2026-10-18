"use strict";
/* ---------------- the Living HUD: the river (row V3; plan: the Living HUD in v23, step 5) ----------------
   The life line's ribbon becomes a river, ported from the showcase's river.js (its runtime part). Three canvases under
   svg#river in #line (the lived years, the fog, the live layer on top, which alone takes the pointer): the page's own
   line (04-line.js drawLine) still draws every redraw and keeps on top its year marks (.gl), the ages, the hover reading
   and "click a year to read it" (#lineHov, lineGeo); its bands, glow, sheen, grid and band turn clear, and the fog
   (#fog, #cosmos) and the ahead layer's thread, now line and bead give way to the river's own. The river keeps the line's one mapping (lnScale, the same width, pad and now), so the marks and ages stay over
   their years.
     the river      five colour bands out of a point at birth, as thick as life was satisfying (the river rows, softened
                    over a few years), in five inks of one lightness and one strength (colour-even), with a slow current
                    inside, ink that bleeds past its edges and blooms near now while it is wet (S.wet), a gleam at now
                    and the identity band under it (the identity of each year's chapter line). Before the first year it
                    is only its source: a point of light in a five-colour halo
     B3 the doors   five faint doorway arches in the fog ahead, one per colour, lit and near as far as that colour's ways
                    are open (S.doors); a narrowing way stands dimmer and farther off, never shut. Where the game holds
                    a way steady (S.doorsAbout, decision 10) its reading says "about"
     B2 sediment    under the river, a bed of earth for every title held (the stop log's titles: kind, years, invested,
                    what it expects), tinted by what it expects; small cut gems for perks where they first came, wax
                    seals for plans reached
     W3 threads     story lines (commitments, plans, dreams, quarrels) as fine threads arcing above the river from where
                    they began to where they were tied off, or on to now; an outcome runs light along the threads it
                    touches
     C2 seams       each push the voice made marks the river where it was made: a gold seam where it was taken to
                    heart, a dark knot where it was resented, a fine silver seam where it simply passed. How it was
                    taken is its own outcome's hindsight (CH.life.pushes, the stop log); a new one grows in when its
                    outcome is shown
     C4 the current while time runs, streaks of colour flow along the bands toward now and spill into the fog; their own
                    picks float as small lights; at a moment the flow slows, parts round now and one ripple spreads
   Its rows come from the line's own (lnLayout): threads above, the river, the band and the ground, down to the page's
   row of year marks; the line is 120 px high on screens taller than 800 px, 92 px on shorter ones and 64 px on phones
   (decision 6, 30-river.css). Symbol first, words on hover: each mark the page does not read itself (a thread, a door, a
   gem, a bed, a seam, the years ahead) gives its meaning in the page's one #tip, under the strip as the line's own.
   Motion (the ink look's setting): full; calm, a third of the speed and fewer flecks; off (and reduced motion), one
   still frame per change. Cost (PIECES "Cost"): the settled history (sediment, bands, seams, threads) is drawn once into
   an offscreen layer keyed on CH.life.rev and the size, a few steps a frame, and copied to the still canvas only when it
   changes; the fog with its doors (cached body and door sprites) redraws every third frame (calm every sixth), the live
   layer (current, flecks, gleam, hover) every frame (calm every other). While time runs the river grows in steps: a new
   layer at most every 400 ms (calm 800), and the age shown waits at the layer's end until the next one is in. */
(() => {
const CH = window.CH; if (!CH || !CH.piece) return;
const CS = CH.COLORS, HUE = CH.HUE, NAME = CH.NAME, clamp = CH.clamp;
const SPAN = 100;                      // the strip reads ages 0 to 100, as the line (04-line.js SPAN)

/* ---------- small helpers ---------- */
const RGB = {};
["bright", "deep", "pale", "ink"].forEach((k) => { RGB[k] = {}; CS.forEach((c) => (RGB[k][c] = CH.rgb(HUE[k][c]))); });
const rgba = (a, al) => `rgba(${a[0] | 0},${a[1] | 0},${a[2] | 0},${+clamp(al).toFixed(3)})`;
/* the river's own inks, colour-even: each set is one lightness and one chroma in OKLCH and only the hue turns (the
   game's own hues: W 92, U 252, B 308, R 37, G 152 degrees). The game's bright tokens are not even (Red and Green twice
   as vivid as White and Black), so they stay only for single small accents (gems, a breakthrough's star, a star).
     band  L .76 C .10    the bands, their glow, the identity band, the threads, the doors' light, the source at birth
     top   L .81 C .09    a band's lit upper edge          low   L .69 C .10   its lower edge
     pale  L .89 C .055   the current's streaks, the light through a doorway, their own picks
     deep  L .42 C .08    the dark rim of a wet bloom */
const oklch = (L, C, h) => {
  const a = C * Math.cos((h * Math.PI) / 180), b = C * Math.sin((h * Math.PI) / 180);
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  const enc = (v) => 255 * clamp(v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055);
  return [enc(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s), enc(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s), enc(-0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s)];
};
const HUEDEG = { W: 92, U: 252, B: 308, R: 37, G: 152 };
const INK = {};
Object.entries({ band: [0.76, 0.1], top: [0.81, 0.09], low: [0.69, 0.1], pale: [0.89, 0.055], deep: [0.42, 0.08] }).forEach(([k, [L, C]]) => {
  INK[k] = {}; CS.forEach((c) => (INK[k][c] = oklch(L, C, HUEDEG[c]))); });
const BAND = INK.band;
const mix3 = (p, q, t) => [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, p[2] + (q[2] - p[2]) * t];
const GOLD2 = [244, 223, 166], GOLDD = [156, 122, 46], LILAC = [214, 205, 245], UMBER = [58, 44, 62], FOGC = [56, 48, 98];
const easeIO = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeOut = (t) => 1 - Math.pow(1 - clamp(t), 3);
const sstep = (a, b, v) => { const t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); };
// a quoted line for a tooltip: cut at a sentence's end when one comes late enough, else at a word
const cut = (s, n) => {
  s = String(s || ""); if (s.length <= n) return s;
  const c = s.slice(0, n - 1), e = Math.max(c.lastIndexOf(". "), c.lastIndexOf("! "), c.lastIndexOf("? "));
  return e >= n * 0.6 ? c.slice(0, e + 1) : c.replace(/\s+\S*$/, "") + "…";
};
const names = (cs) => cs.map((c) => NAME[c]).join(cs.length > 2 ? ", " : " and ").replace(/, ([^,]*)$/, " and $1");
const pips = (cs) => cs.map(CH.pip).join("");
// a story marker's fields, e.g. marker("⟦c:faith|W|inherited⟧…", "c") -> ["faith", "W", "inherited"]
const marker = (text, k) => { const m = new RegExp("⟦" + k + ":([^⟧]*)⟧").exec(String(text || "")); return m ? m[1].split("|") : null; };
const words = (s) => new Set(CH.plain(s).toLowerCase().replace(/[^a-z ]/g, " ").split(/\s+/).filter((w) => w.length > 3));
const overlap = (A, B) => { let n = 0; A.forEach((w) => { if (B.has(w)) n++; }); return n; };
const bez = (a, b, c, d, t) => { const u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; };

/* ---------- the rows of the strip, from the line's own (04-line.js lnLayout) ----------
   The page keeps its row of year marks and the ages at the bottom; above them, from the top: the threads, the river,
   the identity band and the ground (beds of earth over one row of gems), shared as the showcase's strip shares them
   (threads 0.2, river 0.4, ground 0.33; a phone gives the river more). */
function layoutOf(H) {
  const pl = lnLayout(H), sm = pl.sm, s = H / 150, sk = Math.min(1.4, s);
  const top = sm ? 2.5 : 4 * sk, lim = pl.gy - (sm ? 4.9 : pl.gr + 2);
  const bandH = sm ? 2.6 : 3.4 * Math.min(1.3, s), gapA = sm ? 3 : 4 * Math.min(1.6, s), gapB = sm ? 3.5 : 4.5 * Math.min(1.5, s);
  const rest = Math.max(12, lim - top - gapA - bandH - gapB), w = sm ? [0.16, 0.5, 0.26] : [0.2, 0.4, 0.33], sum = w[0] + w[1] + w[2];
  const thH = (rest * w[0]) / sum, maxT = Math.min((rest * w[1]) / sum, H * 0.3), stH = rest - thH - maxT;
  const mid = top + thH + maxT / 2, bandY = mid + maxT / 2 + gapA, strTop = bandY + bandH + gapB, strBot = strTop + stH;
  const gemR = sm ? 2.6 : clamp(3.6 * s, 3.6, 5.2), gemsH = sm ? 4 : gemR * 2 + 4 * sk;
  return { sm, s, mid, maxT, bandH, bandY, strTop, strBot, gemR, gemsH, thTop: top, pitchMax: sm ? 6 : 9 * Math.min(1.6, s) };
}

/* ---------- textures, made once per page: the current's streaks, the fog, the glows (seeded noise, never random) ---------- */
const TX = {};
// noise that wraps every `per` units across x, so a tile repeats with no seam; the blend keeps its contrast
const pnoise = (x, y, per, o) => { const t = x / per, a = CH.fbm(x, y, o) - 0.5, b = CH.fbm(x - per, y, o) - 0.5; return 0.5 + (a * (1 - t) + b * t) / Math.sqrt((1 - t) * (1 - t) + t * t); };
const canvasOf = (w, h, f) => { const c = document.createElement("canvas"); c.width = w; c.height = h; f(c.getContext("2d"), w, h); return c; };
// the same into a canvas kept from before (cleared, resized only when its size changes), so images painted again and
// again make no new canvases
const repaint = (c, w, h, f) => { if (!c) return canvasOf(w, h, f); if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
  const g = c.getContext("2d"); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = "source-over"; g.clearRect(0, 0, w, h); f(g, w, h); return c; };
function pixels(w, h, fn) {
  return canvasOf(w, h, (g) => { const im = g.createImageData(w, h), d = im.data;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = fn(x, y), i = (y * w + x) * 4; d[i] = p[0]; d[i + 1] = p[1]; d[i + 2] = p[2]; d[i + 3] = p[3]; }
    g.putImageData(im, 0, 0); });
}
function textures() {
  if (TX.ok) return TX;
  TX.ok = true;
  // the current: long thin streaks, light ones and dark ones, stretched along the river (10 to 1)
  TX.flowL = pixels(512, 48, (x, y) => { const n = pnoise(x / 52, y / 2.9 + 3.1, 512 / 52, 3); const a = sstep(0.6, 0.9, n); return [255, 250, 236, a * 255]; });
  TX.flowD = pixels(512, 48, (x, y) => { const n = pnoise(x / 70 + 17, y / 3.4 + 9.7, 512 / 70, 3); const a = sstep(0.62, 0.92, n); return [16, 10, 34, a * 255]; });
  // the fog: soft billows, faintly tinted by the five inks here and there, as the line's nebula
  const base = [196, 188, 236];
  TX.fog = pixels(448, 112, (x, y) => {
    const n = pnoise(x / 58, y / 22, 448 / 58, 5), d = sstep(0.36, 0.86, n);
    const h = pnoise(x / 150 + 40, y / 54 + 11, 448 / 150, 2) * 5; let ws = 0; const tint = [0, 0, 0];
    CS.forEach((c, i) => { const w = Math.max(0, 1 - Math.abs(h - i - 0.5) * 1.15); ws += w; const b = BAND[c]; tint[0] += b[0] * w; tint[1] += b[1] * w; tint[2] += b[2] * w; });
    const col = ws ? mix3(base, tint.map((v) => v / ws), 0.3) : base;
    const edge = sstep(0, 0.22, y / 112) * sstep(0, 0.22, 1 - y / 112);   // soft top and bottom, so a stretched tile never shows a hard line
    return [col[0], col[1], col[2], d * edge * 235];
  });
  // a soft round glow per colour (the lights of their own picks) and in gold
  TX.dot = {};
  const glow = (rgb) => canvasOf(32, 32, (g) => { const r = g.createRadialGradient(16, 16, 0, 16, 16, 16); r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(0.22, rgba(rgb, 0.95)); r.addColorStop(0.55, rgba(rgb, 0.28)); r.addColorStop(1, rgba(rgb, 0)); g.fillStyle = r; g.fillRect(0, 0, 32, 32); });
  CS.forEach((c) => (TX.dot[c] = glow(INK.pale[c])));
  TX.gold = glow(GOLD2); TX.lilac = glow(LILAC);
  // the current's flecks: short soft streaks along the flow in each colour's pale ink, with no white core, so each
  // band keeps its own colour
  const streak = (rgb) => canvasOf(32, 8, (g) => { g.translate(16, 4); g.scale(4, 1); const r = g.createRadialGradient(0, 0, 0, 0, 0, 4); r.addColorStop(0, rgba(rgb, 0.9)); r.addColorStop(0.5, rgba(rgb, 0.42)); r.addColorStop(1, rgba(rgb, 0)); g.fillStyle = r; g.fillRect(-4, -4, 8, 8); });
  TX.streak = {};
  CS.forEach((c) => { TX.streak[c] = streak(INK.pale[c]); });
  // the glint at now: a four-pointed star of light
  TX.star = canvasOf(64, 64, (g) => {
    const r = g.createRadialGradient(32, 32, 0, 32, 32, 14); r.addColorStop(0, "rgba(255,250,232,1)"); r.addColorStop(0.35, "rgba(244,223,166,0.55)"); r.addColorStop(1, "rgba(244,223,166,0)");
    g.fillStyle = r; g.fillRect(0, 0, 64, 64);
    g.fillStyle = "rgba(255,248,226,0.95)";
    [[0, 1], [1, 0]].forEach(([vx, vy]) => { g.beginPath(); g.moveTo(32 - 30 * vx, 32 - 30 * vy); g.lineTo(32 + 1.6 * vy, 32 + 1.6 * vx); g.lineTo(32 + 30 * vx, 32 + 30 * vy); g.lineTo(32 - 1.6 * vy, 32 - 1.6 * vx); g.closePath(); g.fill(); });
  });
  // the gleam: a tall soft column of gold light
  TX.beam = canvasOf(48, 192, (g) => { g.translate(24, 96); g.scale(1, 4); const r = g.createRadialGradient(0, 0, 0, 0, 0, 24); r.addColorStop(0, "rgba(255,240,200,0.9)"); r.addColorStop(0.4, "rgba(232,196,120,0.35)"); r.addColorStop(1, "rgba(216,180,105,0)"); g.fillStyle = r; g.fillRect(-24, -24, 48, 48); });
  return TX;
}
// the engraver's hatching for the strata: fine diagonal lines, one device pixel wide (made for each canvas's scale)
function hatch(g, k) {
  const n = 5, tile = pixels(n, n, (x, y) => ((x + y) % n === 0 ? [14, 9, 26, 70] : [0, 0, 0, 0]));
  const p = g.createPattern(tile, "repeat");
  try { p.setTransform(new DOMMatrix([1 / k, 0, 0, 1 / k, 0, 0])); } catch (_) {}
  return p;
}
/* a soft rectangle of one colour: its alpha shaped down its height by `prof` ([[at, alpha], ...], 0 at the top to 1 at
   the bottom) and feathered in from the left over `fl` px and out to the right over `fr` px. It is all soft, so it is
   drawn at a third of the size and stretched back (one shared scratch canvas). */
const FS = document.createElement("canvas"), fsx = FS.getContext("2d");
// gradient stops that ease from alpha a0 at t0 to a1 at t1 (smoothstep), so a soft edge has no visible start
function soft(gr, t0, t1, rgb, a0, a1) {
  for (let i = 0; i <= 8; i++) { const u = i / 8, e = u * u * (3 - 2 * u); gr.addColorStop(clamp(t0 + (t1 - t0) * u, 0, 1), `rgba(${rgb},${(a0 + (a1 - a0) * e).toFixed(4)})`); }
}
function feathered(g, x, y, w, h, rgb, al, fl, fr, prof) {
  if (w < 1 || h < 1 || al <= 0.002) return;
  const sw = Math.max(2, Math.ceil(w / 3)), sh = Math.max(2, Math.ceil(h / 3));
  if (FS.width < sw || FS.height < sh) { FS.width = Math.max(FS.width, sw); FS.height = Math.max(FS.height, sh); }
  fsx.setTransform(1, 0, 0, 1, 0, 0); fsx.globalCompositeOperation = "source-over"; fsx.clearRect(0, 0, sw, sh);
  const v = fsx.createLinearGradient(0, 0, 0, sh); prof.forEach(([at, a]) => v.addColorStop(at, rgba(rgb, al * a)));
  fsx.fillStyle = v; fsx.fillRect(0, 0, sw, sh);
  fsx.globalCompositeOperation = "destination-in";
  const hz = fsx.createLinearGradient(0, 0, sw, 0), a = clamp(fl / w, 0, 0.5), b = clamp(1 - fr / w, 0.5, 1);
  if (fl > 0) soft(hz, 0, a, "0,0,0", 0, 1); else hz.addColorStop(0, "#000");
  if (fr > 0) soft(hz, b, 1, "0,0,0", 1, 0); else hz.addColorStop(1, "#000");
  fsx.fillStyle = hz; fsx.fillRect(0, 0, sw, sh); fsx.globalCompositeOperation = "source-over";
  g.drawImage(FS, 0, 0, sw, sh, x, y, w, h);
}
// erase toward a point: what is drawn between x0 and x1 fades out (strength at x1); where the ground and the threads
// meet now, so the present opens softly
function fadeOut(g, x0, x1, y0, y1, strength) {
  if (x1 - x0 < 1 || y1 - y0 < 1) return;
  g.save(); g.globalCompositeOperation = "destination-out";
  const gr = g.createLinearGradient(x0, 0, x1, 0); soft(gr, 0, 1, "0,0,0", 0, strength);
  g.fillStyle = gr; g.fillRect(x0, y0, x1 - x0, y1 - y0); g.restore();
}
// the game's own colour glyphs (the page's ink icons, ci-color-*), turned into small images for the doors' keystones
const GLY = {};
function glyphImg(c, onload) {
  if (GLY[c]) return GLY[c].ready ? GLY[c].img : null;
  const sym = document.getElementById("ci-color-" + c.toLowerCase());
  if (!sym) return null;
  const inner = sym.innerHTML, refs = [...inner.matchAll(/url\(#([^)]+)\)/g)].map((m) => document.getElementById(m[1])).filter(Boolean);
  const col = rgba(INK.pale[c], 1);
  const src = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 48 48" style="color:${col}"><defs>${refs.map((r) => r.outerHTML).join("")}</defs>${inner}</svg>`;
  const img = new Image(), e = (GLY[c] = { img, ready: false });
  img.onload = () => { e.ready = true; if (onload) onload(); };
  img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(src);
  return null;
}

/* ---------- reading the life: titles over time, perks, plans reached, story lines ----------
   From the live life (CH.life: the page's own story items and the stop log), read again each time the log grows (keyed
   on CH.life.rev). Everything read carries when the story first tells it (`seen`, `known`, `k1` are its ages; `seenW`,
   `knownW`, `k1W`, `w` the story line or stop that tells it). Live, every line the page has is told, so a mark shows
   from its age on. */
const wI = (x) => ({ a: x.age ?? 0, ki: x._i });
const wS = (s) => ({ a: s.age, si: s.i });
function indexOf(L) {
  const items = (L.items || []).map((x, i) => Object.assign({ _i: i }, x)).sort((p, q) => (p.age ?? 0) - (q.age ?? 0) || p._i - q._i);
  const I = { L, rev: L.rev, end: L.end_age, items };
  rowsOf(I);
  I.runs = titleRuns(L, items);
  I.perks = perksOf(L, items);
  I.seals = sealsOf(L, items);
  const th = threadsOf(L, items, I.runs);
  I.threads = th.threads; I.points = th.points;
  I.picks = L.stops.filter((s) => s.kind === "res" && s.res && !s.res.pushed).map((s) => ({ a: s.age, w: wS(s), cols: CH.lettersOf(s.res.colors), act: s.res.act || "" }));
  return I;
}
// the river rows (the whole history comes with every state, so they are read again whenever more came)
function rowsOf(I) { const R = I.L.river || []; I.nr = R.length; I.rows = R.slice().sort((p, q) => p[0] - q[0]); }
// B2: each title held, as one run per kind from where it began (age minus years held) to where it ended. The stops
// give how invested they were and what it expected of them over time; a story line that ended it gives the exact age.
const KEEPS = ["start", "inherited", "moved", "changed employer", "reshaped", "promoted"];
function titleRuns(L, items) {
  const runs = [], open = {};
  const close = (r, s, by) => {
    const a = s.age, it = items.find((x) => x.tag === "commitment" && (x.kind || "") === r.kind && !KEEPS.includes(x.what || "") && x.age > r.last - 0.25 && x.age <= a + 1e-6);
    r.end = it ? it.age : by != null ? by : (r.last + a) / 2; r.endItem = it || null; r.known = it ? it.age : a; r.knownW = it ? wI(it) : wS(s);
  };
  L.stops.forEach((s) => {
    const a = s.age, seen = new Set();
    (s.life.titles || []).forEach((t) => {
      const start = Math.max(0, a - (+t.years || 0));
      let r = open[t.kind];
      if (r && Math.abs(start - r.start) > 1.2) { close(r, s, Math.max(r.last, start)); r = null; }   // the same kind begun again: a new layer
      if (!r) {
        const st = items.find((x) => x.tag === "commitment" && (x.kind || "") === t.kind && (x.what === "start" || x.what === "inherited") && x.age >= start - 0.6 && x.age <= a + 1e-6);
        r = open[t.kind] = { kind: t.kind, start, seen: st ? Math.min(a, st.age) : a, seenW: st ? wI(st) : wS(s), samples: [], end: null, known: null, knownW: null }; runs.push(r);
      }
      const named = (t.named || []).map((n) => n.say || n.name).filter(Boolean);
      r.samples.push({ a, w: wS(s), inv: clamp(+t.invested || 0), exp: CH.lettersOf(t.expects), clash: !!t.clash, named, years: +t.years || 0 });
      r.last = a; seen.add(t.kind);
    });
    Object.keys(open).forEach((k) => { if (!seen.has(k)) { close(open[k], s); delete open[k]; } });
  });
  return runs;
}
// B2: every perk held at some stop, where it first came (the story's "gained" line, else the first stop less the years
// it had been held), when the story first tells of it, and when it was lost again (a lost gem keeps its place)
function perksOf(L, items) {
  const m = new Map();
  L.stops.forEach((s) => {
    const here = new Set();
    (s.life.perks || []).forEach((p) => {
      here.add(p.name);
      let e = m.get(p.name);
      if (!e) {
        const it = items.filter((x) => x.tag === "role" && x.name === p.name && x.what === "gained" && x.age <= s.age + 1e-6).pop();
        e = { name: p.name, say: p.say || p.name, kind: p.kind || "", ways: CH.lettersOf(p.ways), first: it ? it.age : Math.max(0, s.age - (+p.years || 0)), known: it ? it.age : s.age, knownW: it ? wI(it) : wS(s), ev: [] };
        m.set(p.name, e);
      } else if (e.ev.length && e.ev[e.ev.length - 1].lost) e.ev.push({ a: s.age, w: wS(s), lost: false });
    });
    m.forEach((e) => { if (!here.has(e.name) && !(e.ev.length && e.ev[e.ev.length - 1].lost)) e.ev.push({ a: s.age, w: wS(s), lost: true }); });
  });
  return [...m.values()].sort((p, q) => p.first - q.first);
}
// B2: plans reached: the story's "achieved" lines, and any plan whose progress reached 1 with no line telling it
function sealsOf(L, items) {
  const out = [];
  items.forEach((x) => {
    if (x.tag !== "goal") return;
    const g = marker(x.text, "g") || [];
    if ((x.what || g[1]) === "achieved") out.push({ a: x.age, w: wI(x), cols: CH.lettersOf(g[2] || ""), text: CH.plain(x.text), kind: x.kind || g[0] || "plan" });
  });
  const seen = new Set();
  L.stops.forEach((s) => (s.life.goals || []).forEach((g) => {
    if (g.progress == null || g.progress < 0.999 || seen.has(g.id)) return;
    seen.add(g.id);
    if (!out.some((o) => Math.abs(o.a - s.age) < 1.5)) out.push({ a: s.age, w: wS(s), cols: CH.lettersOf(g.colors), text: `${CH.cap(g.kind)}: ${g.name}`, kind: g.kind });
  }));
  return out.sort((p, q) => p.a - q.a);
}
// W3: the story lines as threads. A commitment runs from its start to its end, grouped by kind (a change of employer is
// a bead on it); a plan from "begins" to achieved / let go / not reached (matched by its marker and its words); a dream
// for as long as it stays among their dreams; a quarrel with a title from when the title first clashed to the line
// that tells it. Breakthroughs and turns are single points: short stitches rising from the river. Each thread keeps
// `seen` and `k1` (when the story first tells that it ended): before k1 it is still open.
function threadsOf(L, items, runs) {
  const T = [], P = [], openC = {}, openG = [], dreams = [];
  const runAt = (kind, a) => runs.find((r) => r.kind === kind && r.start <= a + 1.0 && (r.end == null || r.end >= a - 0.2));
  const fin = (o, a, end, x, kw) => { o.a1 = a; o.end = end; o.t1 = x || null; o.k1W = kw; o.k1 = kw.a; };
  items.forEach((x) => {
    const a = x.age ?? 0;
    if (x.tag === "commitment") {
      const c = marker(x.text, "c") || [], kind = x.kind || c[0] || "commitment", what = x.what || c[2] || "";
      const o = openC[kind];
      if (what === "start" || what === "inherited") {
        if (o) { const r = runAt(kind, o.a0); fin(o, r && r.end != null && r.end < a ? r.end : a, "fade", null, wI(x)); }
        const r = runAt(kind, a), cols = CH.lettersOf(c[1] || "");
        openC[kind] = { type: "commit", kind, a0: a, seen: a, seenW: wI(x), cols: cols.length ? cols : r ? r.samples[0].exp.slice(0, 2) : [], t0: x, beads: [], a1: null, k1: null, k1W: null, end: null };
        T.push(openC[kind]);
      } else if (o && KEEPS.includes(what)) o.beads.push({ a, x, w: wI(x) });
      else if (o) { fin(o, a, "knot", x, wI(x)); delete openC[kind]; }
    } else if (x.tag === "goal") {
      const g = marker(x.text, "g") || [], kind = x.kind || g[0] || "plan", what = x.what || g[1] || "", cols = CH.lettersOf(g[2] || "");
      const sig = [kind, g[2], g[3], g[4], g[5]].join("|");
      if (what === "begins") {
        const o = { type: kind === "plan" ? "plan" : "dream", kind, sig, a0: a, seen: a, seenW: wI(x), cols, t0: x, beads: [], a1: null, k1: null, k1W: null, end: null, w: words(x.text) };
        T.push(o); (kind === "plan" ? openG : dreams).push(o);
      } else if (kind === "plan") {
        const cand = openG.filter((o) => o.sig === sig);
        if (!cand.length) return;
        const w = words(x.text); let best = cand[0], bs = -1;
        cand.forEach((o) => { const s = overlap(o.w, w); if (s > bs) { bs = s; best = o; } });
        if (/extended/.test(what)) { best.beads.push({ a, x, w: wI(x) }); return; }
        fin(best, a, what === "achieved" ? "gold" : /let go|aside|gave up|give up|abandon/.test(what) ? "loose" : "knot", x, wI(x));
        openG.splice(openG.indexOf(best), 1);
      }
    } else if (x.tag === "clash") {
      const kind = x.kind || "", r = runs.find((q) => q.kind === kind && q.start <= a + 0.5 && (q.end == null || q.end >= a - 1));
      let a0 = a - 0.3;
      if (r) { let st = null; r.samples.forEach((s) => { if (s.a > a + 1e-6) return; if (s.clash && st == null) st = s.a; if (!s.clash) st = null; }); if (st != null && st < a) a0 = Math.max(r.start, st - 0.2); }
      // the quarrel is told by its line: it shows from there, already tied off
      T.push({ type: "clash", kind, a0, seen: a, seenW: wI(x), a1: a, k1: a, k1W: wI(x), end: "knot", cols: r ? r.samples[r.samples.length - 1].exp.slice(0, 2) : [], t0: x, t1: x, beads: [] });
    } else if (x.tag === "breakthrough") {
      const b = marker(x.text, "B") || [];
      P.push({ type: "break", a, w: wI(x), cols: CH.lettersOf(b[0] || ""), x });
    } else if (x.tag === "turn" || x.tag === "conversion") {
      const c = marker(x.text, "C") || [];
      P.push({ type: "turn", a, w: wI(x), from: CH.lettersOf(c[0] || "")[0] || "", to: CH.lettersOf(c[1] || "")[0] || "", x });
    }
  });
  // commitments still open at the end tie off where their title ended, if it did (known when the title is gone);
  // plans and the rest run on to now
  Object.values(openC).forEach((o) => { const r = runAt(o.kind, o.a0); if (r && r.end != null) fin(o, Math.max(o.a0, r.end), "fade", null, r.knownW); });
  // a dream lasts while it stays among their dreams (the HUD's goals at each stop, matched by its colours)
  dreams.forEach((o) => {
    const key = o.cols.join(""); let prev = o.a0;
    for (const s of L.stops) {
      if (s.age <= o.a0 + 1e-6) continue;
      if ((s.life.goals || []).some((g) => (g.kind === "dream" || g.kind === "passion") && CH.lettersOf(g.colors).join("") === key)) { prev = s.age; continue; }
      fin(o, Math.max(o.a0 + 0.05, (prev + s.age) / 2), "fade", null, wS(s)); return;
    }
  });
  return { threads: T, points: P };
}

/* ---------- words for the tooltips ---------- */
const KIND = { career: "Work", community: "A community", faith: "Faith", partner: "A partner", family: "Family", school: "School", plan: "A plan", dream: "A dream", passion: "A passion" };
const PERK_KIND = { skill: "a skill", credential: "a credential", asset: "something they own", bond: "a bond", standing: "their standing", status: "their status" };
const invWord = (v) => (v >= 0.85 ? "invested heart and soul" : v >= 0.6 ? "invested deeply" : v >= 0.35 ? "invested steadily" : "invested lightly");
const doorWord = (v) => (v >= 0.95 ? "wide open" : v >= 0.7 ? "open" : v >= 0.45 ? "narrowing" : "hard to reach");
// how open a way is against usual, in plain words and a percentage (S.doors: 1 is a way as open as usual); "about" where
// the game holds it steady (S.doorsAbout)
const doorSub = (v, about) => `${v >= 1.04 ? "more open than usual" : v >= 0.93 ? "about as open as usual" : v >= 0.75 ? "a little narrower than usual" : v >= 0.55 ? "narrower than usual" : "much narrower than usual"} (${about ? "about " : ""}${Math.round(v * 100)}% of usual)`;
const DOOR_MEAN = { W: "order, duty and doing right by others", U: "learning, skill and getting things exactly right", B: "ambition, self-reliance and their own advantage",
  R: "freedom, feeling and acting on impulse", G: "belonging, nature and things as they are" };
const yrs = (n) => { const v = Math.round(n); return v <= 0 ? "less than a year" : v === 1 ? "a year" : `${v} years`; };

/* ---------- the river on the line ---------- */
function make() {
  textures();
  const root = document.createElement("div");
  root.className = "rv";
  lineEl.insertBefore(root, lineEl.firstChild);
  /* three canvases, one over the other (the release's frame budget, PIECES "Cost"): the lived years, drawn again only
     when the view of them changes; the fog with its stars and doors, every other frame (every fourth when calm); and
     the live layer (the current, its flecks, the gleam at now, a push growing in, the lights), every frame (every other
     when calm). The last one takes the pointer. */
  const cv = CH.canvas(root, "rv-cv"), ctx = cv.getContext("2d");
  const cvF = CH.canvas(root, "rv-fog"), fctx = cvF.getContext("2d"), cvL = CH.canvas(root, "rv-live"), lctx = cvL.getContext("2d");
  if (!ctx || !fctx || !lctx) { root.remove(); return null; }
  [cv, cvF, cvL].forEach((c) => c.setAttribute("aria-hidden", "true"));                  // #line itself is the picture's label
  let stat = document.createElement("canvas"), sctx = stat.getContext("2d");             // everything that does not move
  let statB = document.createElement("canvas"), sctxB = statB.getContext("2d");          // the next one, built a step a frame
  // a cache's small round things (gems, seals, the turns on the threads), kept apart so that while the age eases they
  // are set at their stretched places one by one and keep their shape, not stretched with the years
  let gly = document.createElement("canvas"), gctx = gly.getContext("2d");
  let glyB = document.createElement("canvas"), gctxB = glyB.getContext("2d");
  const bloom = document.createElement("canvas"), bctx = bloom.getContext("2d");          // the river at a quarter size: its glow
  let bloomN = document.createElement("canvas"), bloomNB = document.createElement("canvas"); // the same, kept only where the ink is wet (one for each still layer)
  const bloomS = document.createElement("canvas"), sbctx = bloomS.getContext("2d");       // a scratch copy for softening the glow
  const rnd = CH.rng(31);                                                                 // the current's flecks: decoration, seeded
  const fogB = document.createElement("canvas"), fogF = document.createElement("canvas");  // the fog, back and front, at half size
  const tiny = document.createElement("canvas"); tiny.width = tiny.height = 1; const tctx = tiny.getContext("2d");

  /* I the life's index; S the state asked for; G the geometry the offscreen layer was drawn at (G.now, exact or a cache
     of the lived years); V this frame's view of it: s, the stretch from G's lived years to the age shown, vnx (now in G's
     pixels) and dnx (now on the page), D the page's own scale at the age shown */
  let I = null, S = null, G = null, V = null, job = null;
  let vAge = null, tAge = 0, wetV = 0, fogV = 1, doorsV = null, dirty = true, rebuild = true;
  // stale: the life has more to show than the layer on hand (a new stop, a push grown in); the next layer is then made
  // a step at a time while this one stands in. gen counts these, so a layer made before the last one is not taken as
  // having caught up. rebuild (a new size, a new life, a load, motion changed) makes one at once.
  let stale = false, gen = 0, gid = 0, fc = 0, waitN = 0, planAt = -1e9, stillKey = "", fogDirty = true, fogHover = -1;
  const restale = () => { stale = true; gen++; };
  let living = false, livingV = 0, partT = -1, partV = 0, rippleT = -1, tNow = 0, slowV = 1;
  let hover = null;                               // what the pointer is on: a door or a thread
  const pulses = [], flecks = [];                 // outcome lights, the current's flecks
  const timers = new Set();
  let pat = null, patK = 0;
  const off = () => CH.motion() === "off";
  // the motion clock: every loop and every arrival runs on it, so calm motion slows all of them alike (decision 2)
  let mt = 0;
  // pushes: one first seen while playing waits (not drawn) until its outcome is shown, then grows in from there; one
  // there at the start (or after a load) is simply there
  const seenP = new Set(), pend = new Map(), born = new Map();
  // what this piece costs each frame (script ms, its draws and its updates together), for the release's budget
  const ring = new Float32Array(1200); let ringN = 0, bucketT = -1, bucketMs = 0;
  const charge = (ms) => { const t = document.timeline ? document.timeline.currentTime : performance.now();
    if (t !== bucketT) { if (bucketT >= 0) ring[ringN++ % ring.length] = bucketMs; bucketT = t; bucketMs = 0; } bucketMs += ms; };
  // and by part (the layers it draws, the still layers it makes, the updates), for finding where the time goes
  let parts = {};
  const costOf = (k, t0) => { const ms = performance.now() - t0, q = parts[k] || (parts[k] = { ms: 0, n: 0, max: 0 }); q.ms += ms; q.n++; if (ms > q.max) q.max = ms; };
  // live, everything the page has is told: a mark shows from its age on
  const knows = (w, upTo) => !!w && w.a <= upTo + 1e-6;
  const stopKey = () => (S && S.stop != null ? S.stop : -1);
  // with motion off nothing ticks: a still frame that must change later (a lit thread going out) asks for it here
  const later = (ms, re) => { const id = setTimeout(() => { timers.delete(id); dirty = true; if (re) restale(); }, ms); timers.add(id); };

  /* the state asked for: the age eases there (about 400 ms); at once when it is the first, quiet (a load, the years
     before the player takes over), a new life, or motion is off */
  function update(st, how) {
    if (!st) return;
    const t0 = performance.now();
    const L = CH.life, fresh = !I || I.L !== L;
    if (fresh) { I = indexOf(L); rebuild = true; }
    else if (I.rev !== L.rev) { I = indexOf(L); restale(); }
    else if (I.nr !== (L.river || []).length) { rowsOf(I); restale(); }
    const still = vAge == null || fresh || !!(how && how.quiet);
    (L.pushes || []).forEach((p) => { if (seenP.has(p)) return; seenP.add(p); if (!still && !off()) { pend.set(p, performance.now()); later(2600, true); } });
    S = st; tAge = st.age;
    if (still || off()) { vAge = tAge; wetV = st.wet || 0; doorsV = (st.doors || [0, 0, 0, 0, 0]).slice(); fogV = st.age >= I.end - 0.01 ? 0 : 1; rebuild = true; }
    // a moment waiting when the river comes (a load, the switch turned on): the current stands parted round now
    if (st.waiting && partT < 0 && !living) partT = mt;
    dirty = true;
    charge(performance.now() - t0); costOf("update", t0);
  }

  /* ---------- building the still layer ----------
     The lived years only (ground, strata, gems, river, band, threads, the pushes grown in); the fog has its own canvas.
     exact: drawn at the age shown, its small round things in place. A cache (while the age eases): drawn for the newest
     age, its small round things kept in an atlas and set unstretched at their places in the years shown; one made for
     the age the life settles at is kept as the layer.
     A build is a dozen steps. When the layer on screen can still stand in, the next one is built into a second canvas a
     step or so per frame (about 1 ms each, on frames the fog is not drawn) and swapped in when it is done; otherwise
     (the first frame, a new size, a new life, a load) it is built at once. */
  function plan(age, exact, canvas, g) {
    const W = cv._w, H = cv._h, k = cv._k;
    if (!W || !H || !I) return null;
    if (canvas.width !== cv.width || canvas.height !== cv.height) { canvas.width = cv.width; canvas.height = cv.height; }
    if (!pat || patK !== k) { pat = hatch(g, k); patK = k; }
    const gc = canvas === stat ? gly : glyB, gg = exact ? g : canvas === stat ? gctx : gctxB;
    if (!exact && (gc.width !== cv.width || gc.height !== cv.height)) { gc.width = cv.width; gc.height = cv.height; }
    const now = Math.max(0, age), over = now >= I.end - 0.01;
    const pad = W < 600 ? 12 : 16, sc = lnScale(W, pad, now, over), ly = layoutOf(H), nx = sc.X(now);
    // know: how far the story is told in this layer; a cache keeps what is told to the age asked (tAge) at most
    const know = exact ? now : Math.min(now, Math.max(0, tAge));
    // a layer is drawn as wet as the ink is at the age it is made for (S.wet), so the one made for the newest age is
    // already the one to keep once the age settles there
    const NG = { W, H, k, pad, now, know, over, sc, ly, nx, X: sc.X, exact, wet: S ? S.wet || 0 : wetV, fog: fogV, cw: cv.width, ch: cv.height, sk: stopKey(), t: mt };
    // a cache keeps its small round things in an atlas (see put), each later set at its place in the years shown
    NG.atlas = exact ? null : { g: gg, W, H, cx: 0, cy: 0, rowH: 0, list: [] };
    NG.bN = canvas === stat ? bloomN : bloomNB;
    const steps = [
      () => { riverGeo(NG); },
      () => { riverPaths(NG); },
      () => { threadGeo(NG); pushGeo(NG); NG.doors = doorGeo(NG); },
      () => { g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, canvas.width, canvas.height); g.setTransform(k, 0, 0, k, 0, 0);
        g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
        // the atlas is cleared only as far down as its last use reached
        if (!exact) { gg.setTransform(1, 0, 0, 1, 0, 0); gg.clearRect(0, 0, gc.width, Math.min(gc.height, Math.ceil((gc._used || H) * k) + 2)); gg.setTransform(k, 0, 0, k, 0, 0); }
        drawGround(g, NG); },
      () => { drawStrata(g, NG); },
      () => { fadeOut(g, nx - (ly.sm ? 14 : 28), nx + 0.5, ly.strTop - 2, ly.strBot + 2, 1); drawGems(g, NG); },
      () => { drawRiver(g, NG, "glow"); },
      () => { drawRiver(g, NG, "bands"); },
      () => { drawRiver(g, NG, "ink"); },
      () => { drawRiver(g, NG, "ink2"); },
      () => { drawPushes(g, mt, true); },
      () => { drawBand(g, NG); },
      () => { drawThreads(g, NG, 1); },
      () => { drawThreads(g, NG, 2); },
      () => { drawPoints(g, NG); if (NG.atlas) gc._used = NG.atlas.cy + NG.atlas.rowH; },
    ];
    return { G: NG, steps, i: 0, canvas, g, exact, age, wet: NG.wet, fog: fogV, sk: NG.sk, gen };
  }
  // run a build's steps (at least one) while under `budget` ms; the drawing helpers read the geometry being built. A
  // canvas paints its drawing list when it is first read, so each step is painted at once (one pixel of it read into a
  // 1 x 1 canvas): the painting lands in the step's own frame, not all in the frame of the swap.
  function runSteps(J, budget) {
    const keep = G; G = J.G; const t0 = performance.now();
    try { do { J.steps[J.i++](); if (budget !== Infinity) tctx.drawImage(J.canvas, 0, 0, 1, 1, 0, 0, 1, 1); } while (J.i < J.steps.length && performance.now() - t0 < budget); } finally { G = keep; }
    return J.i >= J.steps.length;
  }
  // a finished build in the second canvas becomes the layer on screen
  function swapIn(J) {
    if (J.canvas === statB) { const c = stat; stat = statB; statB = c; const x = sctx; sctx = sctxB; sctxB = x;
      const d = gly; gly = glyB; glyB = d; const e = gctx; gctx = gctxB; gctxB = e; const f = bloomN; bloomN = bloomNB; bloomNB = f; }
    G = J.G; job = null; rebuild = false; gid++;
    if (J.gen === gen) stale = false;
  }
  function build(age, exact) { job = null; const J = plan(age, exact, stat, sctx); if (!J) return; runSteps(J, Infinity); swapIn(J); }
  // the age to build the lived years at while the age eases: forward, the age asked, which is the newest the life has
  // reached (nothing past it is known), never more than twice the age shown, so the stretch stays small; backward, the
  // age shown (the slice shrinks toward the age asked)
  const cacheAge = () => (tAge > vAge ? Math.min(I.end, tAge, Math.max(vAge * 2, vAge + 0.5)) : vAge);
  // this frame's view of the layer on hand: its lived years up to the age shown (or up to its own end, when it stops a
  // few pixels short of now, a gap the gleam covers), stretched to the age shown
  function viewOf() {
    const over = vAge >= I.end - 0.01, sc = lnScale(G.W, G.pad, vAge, over), a = Math.min(vAge, G.now), dnx = sc.X(vAge), vnx = G.X(a), x0 = G.sc.x0;
    const s = vnx - x0 > 0.5 ? (sc.X(a) - x0) / (vnx - x0) : 1;
    const D = { W: G.W, H: G.H, k: G.k, pad: G.pad, now: vAge, over, sc, ly: G.ly, nx: dnx, X: sc.X };
    D.doors = doorGeo(D);
    return { s, vnx, dnx, D, cache: true, x0, gap: dnx - sc.X(a) };
  }

  /* the river's shape: five bands stacked around the middle, out of a point at birth (as lnRiver in 04-line.js), drawn
     through the same smooth curve, sampled every 2.5 px so the fill, the hover, the threads and the current all agree */
  function riverGeo(G) {
    const { now, ly, X } = G, eq = [0.2, 0.2, 0.2, 0.2, 0.2];
    const norm = (s) => { const t = s.reduce((p, q) => p + q, 0) || 1; return s.map((v) => v / t); };
    const rows = [];
    for (const r of I.rows) { if (r[0] > now + 1e-6) break; rows.push([r[0], norm(r.slice(1, 6)), clamp(r[6] || 0), r[8] || "", r[7]]); }
    G.rows = rows; G.rv = null; G.rv0 = null; G.wetW = 0;
    if (!rows.length) { if (!(now > 0.05)) return; rows.push([now, eq, clamp(S && S.content != null ? S.content : 0.6), "", null]); }
    else {
      const last = rows[rows.length - 1];
      if (now - last[0] >= 0.25) rows.push([now, last[1], last[2], last[3], last[4]]);
      else if (now > last[0] && rows.length > 1) rows[rows.length - 1] = [now, last[1], last[2], last[3], last[4]];
    }
    // the outline swells with satisfaction softened over a few years (a triangular kernel, at least two years to each
    // side and wider where a year is only a few pixels), so the river breathes as a life does rather than year by year;
    // the colours' shares are softened a little the same way (a year, or about 8 px)
    const ppy = Math.max(0.5, (G.nx - X(0)) / Math.max(0.1, now));
    const soften = (hw, get) => { let lo = 0; return rows.map((r) => {
      while (rows[lo][0] < r[0] - hw) lo++;
      let w = 0, acc = null;
      for (let i = lo; i < rows.length && rows[i][0] < r[0] + hw; i++) { const wt = 1 - Math.abs(rows[i][0] - r[0]) / hw, v = get(rows[i]);
        if (acc == null) acc = Array.isArray(v) ? v.map(() => 0) : 0;
        if (Array.isArray(v)) v.forEach((x, k) => (acc[k] += x * wt)); else acc += v * wt; w += wt; }
      return !w ? get(r) : Array.isArray(acc) ? norm(acc) : acc / w; }); };
    const sm = soften(Math.max(2, 16 / ppy), (r) => r[2]), shares = soften(Math.max(0.75, 8 / ppy), (r) => r[1]);
    const T = (c) => ly.maxT * (0.42 + 0.58 * c), a1 = rows[0][0], s1 = shares[0], t1 = T(sm[0]);
    const pts = a1 > 0.05 ? [[0, eq, 0.5]] : [];
    for (const f of [0.06, 0.18, 0.36, 0.6, 0.82]) if (a1 * f > 0.04) pts.push([a1 * f, eq.map((v, k) => v + (s1[k] - v) * f), Math.max(0.5, t1 * Math.sqrt(f))]);
    rows.forEach((r, i) => pts.push([r[0], shares[i], T(sm[i])]));
    // at the end of a life the river closes softly over its last year
    if (G.over && pts.length > 2) { const L = pts[pts.length - 1]; L[2] = Math.max(0.5, L[2] * 0.25); }
    if (pts.length < 2) return;
    const E = pts.map((p) => { let y = ly.mid - p[2] / 2; const e = [y]; for (let c = 0; c < 5; c++) { y += p[2] * p[1][c]; e.push(y); } return e; });
    const xs = pts.map((p) => X(p[0])), n = pts.length, SX = [], SY = [[], [], [], [], [], []];
    for (let i = 0; i < n - 1; i++) {
      const i0 = Math.max(0, i - 1), i3 = Math.min(n - 1, i + 2), xA = xs[i], xB = xs[i + 1];
      const c1x = xA + (xB - xs[i0]) / 6, c2x = xB - (xs[i3] - xA) / 6, m = Math.max(2, Math.ceil((xB - xA) / 2.5));
      for (let s = i ? 1 : 0; s <= m; s++) {
        const t = s / m; SX.push(bez(xA, c1x, c2x, xB, t));
        for (let j = 0; j < 6; j++) { const yA = E[i][j], yB = E[i + 1][j]; SY[j].push(bez(yA, yA + (yB - E[i0][j]) / 6, yB - (E[i3][j] - yA) / 6, yB, t)); }
      }
    }
    // B1, wet ink: over the wet stretch before now the ink has not set, so its edges run: the river's outer edges creep
    // outward in small irregular lobes and the dividers between the colours waver, as far as the ink is wet (S.wet),
    // more the nearer now. Dry ink behind it keeps the crisp drawn curve. (Its reach is set for a thousand lived pixels
    // and shrinks with a narrower strip, so a phone's river is not wet from end to end.)
    const span = Math.max(1, G.nx - SX[0]), wetW = Math.min(span, (30 + 260 * G.wet) * clamp(span / 1000, 0.3, 1));
    G.wetW = wetW;
    if (G.wet > 0.02) {
      for (let i = 0; i < SX.length; i++) {
        const x = SX[i], r = sstep(G.nx - wetW, G.nx - wetW * 0.3, x) * G.wet; if (r <= 0.003) continue;
        const th = SY[5][i] - SY[0][i], cap = Math.min(1, th / 6);   // a hairline stream (a newborn's) barely runs
        for (let j = 0; j < 6; j++) {
          const outer = j === 0 || j === 5, nz = CH.fbm(x / 7, j * 3.1 + 0.7, 3);
          const d = cap * r * (outer ? 3.4 * (nz - 0.35) : 1.5 * (nz - 0.5));
          SY[j][i] += j === 0 ? -d : d;
        }
        for (let j = 1; j < 6; j++) if (SY[j][i] < SY[j - 1][i]) SY[j][i] = SY[j - 1][i];   // the colours never cross
      }
    }
    G.rv0 = { SX, SY };
  }
  // its second half (a step of its own, so no one step of a build is long): the lookup and the paths
  function riverPaths(G) {
    if (!G.rv0) return;
    const { SX, SY } = G.rv0; G.rv0 = null;
    // a lookup per pixel column: the six edges' heights (the current's flecks and the threads read it every frame)
    const c0 = Math.floor(SX[0]), c1 = Math.ceil(SX[SX.length - 1]), nc = Math.max(1, c1 - c0 + 1), tab = new Float32Array(nc * 6);
    let p = 0;
    for (let c = 0; c < nc; c++) {
      const x = c0 + c; while (p < SX.length - 2 && SX[p + 1] < x) p++;
      const xa = SX[p], xb = SX[Math.min(SX.length - 1, p + 1)], t = xb > xa ? clamp((x - xa) / (xb - xa)) : 0;
      for (let j = 0; j < 6; j++) { const ya = SY[j][p], yb = SY[j][Math.min(SX.length - 1, p + 1)]; tab[c * 6 + j] = ya + (yb - ya) * t; }
    }
    const edgePath = (j, back, path) => { const N = SX.length; if (!back) for (let i = 0; i < N; i++) path[i ? "lineTo" : "moveTo"](SX[i], SY[j][i]); else for (let i = N - 1; i >= 0; i--) path.lineTo(SX[i], SY[j][i]); };
    const outline = new Path2D(); edgePath(0, false, outline); edgePath(5, true, outline); outline.closePath();
    const bands = CS.map((c, j) => { const p2 = new Path2D(); edgePath(j, false, p2); edgePath(j + 1, true, p2); p2.closePath(); return p2; });
    // how much water the river holds, against a grown river across the lived part of the strip: the current carries as
    // many flecks as the river has room for (a child's thin stream only a few)
    let area = 0; for (let c = 0; c < nc; c++) area += tab[c * 6 + 5] - tab[c * 6];
    const fill = clamp(area / Math.max(1, G.W * 0.74 * G.ly.maxT * 0.75), 0.15, 1);
    G.rv = { SX, SY, c0, nc, tab, outline, bands, x0: SX[0], x1: SX[SX.length - 1], edgePath, fill };
  }
  // the height of edge j (0 the top, 5 the bottom) at x, from the column lookup
  const edge = (x, j) => { const R = G && G.rv; if (!R) return G ? G.ly.mid : 0; const c = Math.max(0, Math.min(R.nc - 1, Math.round(x) - R.c0)); return R.tab[c * 6 + j]; };

  /* where the fog begins: at now; at birth, when no year is lived yet, it is held back from the source (about 120 px
     on a desktop strip), so the first screen opens on a point of light in clear night, not on fog */
  const birthOf = (D) => !D.over && D.now <= 0.05;
  const fogFrom = (D) => D.nx + (birthOf(D) ? Math.min(120, D.W * 0.12) : 0);
  /* the fog's own darkness, behind the drifting veils: the unwritten years sit in a deeper night that begins at now and
     deepens over the next 160 px, so the present opens into the fog rather than into a dark slot */
  // (painted once into an image for the fog's width and laid on stretched as now moves: the fog draws it every few
  // frames, and its gradients over the whole fog were the dearest thing in it; made again when the width has changed by
  // more than a twenty-fifth, or the fog's strength by a fiftieth)
  let bodyImg = null, bodyKey = "", bodyL = 0;
  function drawFogBody(g, D) {
    if (fogV <= 0.01) return;
    const { W, H } = D, nx = fogFrom(D), L = Math.max(1, W - nx), lit = !D.over && D.now > 0.05, k = G.k;
    const key = `${W}|${H}|${k}|${Math.round(fogV * 50)}|${lit}|${D.ly.mid}|${D.ly.maxT}`;
    if (key !== bodyKey || Math.abs(L - bodyL) > bodyL * 0.04 + 2) {
      bodyKey = key; bodyL = L;
      bodyImg = repaint(bodyImg, Math.max(1, Math.ceil(L * k)), Math.max(1, Math.ceil(H * k)), (c) => { c.scale(k, k); paintFogBody(c, D, L, H, lit, Math.round(fogV * 50) / 50); });
    }
    g.drawImage(bodyImg, nx, 0, L, H);
  }
  function paintFogBody(g, D, L, H, lit, fv) {
    const gr = g.createLinearGradient(0, 0, L, 0);
    const r1 = Math.min(0.95, 160 / L); soft(gr, 0, r1, "12,9,28", 0, 0.42 * fv); gr.addColorStop(1, `rgba(16,11,36,${0.62 * fv})`);
    g.fillStyle = gr; g.fillRect(0, 0, L, H);
    // a faint even haze over it, thicker far off, and a low mist along the ground line the doors stand on
    const hz = g.createLinearGradient(0, 0, L, 0);
    soft(hz, 0, 0.3, "150,136,212", 0, 0.05 * fv); hz.addColorStop(1, `rgba(150,136,212,${0.11 * fv})`);
    g.fillStyle = hz; g.fillRect(0, 0, L, H);
    // the present's own light, opening into the mist just past now (so now is a threshold, not the edge of a dark slot)
    if (lit) {
      const rx = Math.min(170, L * 0.7), ry = D.ly.maxT * 1.25;
      g.save(); g.globalCompositeOperation = "lighter"; g.translate(0, D.ly.mid); g.scale(rx / ry, 1);
      const lg = g.createRadialGradient(0, 0, 0, 0, 0, ry); lg.addColorStop(0, `rgba(226,206,176,${0.08 * fv})`); lg.addColorStop(0.45, `rgba(176,160,214,${0.035 * fv})`); lg.addColorStop(1, "rgba(176,160,214,0)");
      g.fillStyle = lg; g.fillRect(0, -ry, ry, ry * 2); g.restore();
    }
    const y = D.ly.bandY + D.ly.bandH / 2, mh = D.ly.maxT * 0.42;
    feathered(g, 0, y - mh, L, mh * 2, [176, 164, 226], 0.1 * fv, Math.min(90, L * 0.4), 0, [[0, 0], [0.55, 1], [1, 0]]);
  }

  /* ---------- B2: the ground under the river ---------- */
  // the earliest age anything is laid in the ground by now (a title, a perk, a plan reached), or null
  function groundFrom(now) {
    let a = Infinity;
    I.runs.forEach((r) => { if (knows(r.seenW, now)) a = Math.min(a, r.start); });
    I.perks.forEach((p) => { if (knows(p.knownW, now)) a = Math.min(a, p.first); });
    I.seals.forEach((s) => { if (knows(s.w, now)) a = Math.min(a, s.a); });
    return a === Infinity ? null : a;
  }
  // a faint bed of earth under the lived years, from where the first thing was laid down to now, soft at every edge;
  // before anything is laid down, only a faint hairline where the ground will be
  function drawGround(g, G) {
    const { ly, X, now } = G; if (now <= 0.05) return;
    const xb = G.nx, a0 = groundFrom(G.know), xa = a0 == null ? null : X(a0);
    if (xa == null || xb - xa < 6) {
      const x0 = X(0); if (xb - x0 < 8) return;
      const gr = g.createLinearGradient(x0, 0, xb, 0); gr.addColorStop(0, "rgba(216,190,140,0)"); gr.addColorStop(0.25, "rgba(216,190,140,0.1)"); gr.addColorStop(0.85, "rgba(216,190,140,0.1)"); gr.addColorStop(1, "rgba(216,190,140,0)");
      g.strokeStyle = gr; g.lineWidth = 0.6; g.beginPath(); g.moveTo(x0, ly.strTop + 0.5); g.lineTo(xb, ly.strTop + 0.5); g.stroke();
      return;
    }
    const x0 = Math.max(X(0), xa - 22);
    feathered(g, x0, ly.strTop - 1, xb - x0, ly.strBot - ly.strTop + 2, [66, 50, 92], 0.16, Math.min(24, (xb - x0) * 0.3), Math.min(28, (xb - x0) * 0.3), [[0, 0], [0.25, 1], [0.75, 1], [1, 0]]);
  }
  // the strata: one bed of earth per title held, laid down like sediment: at every age the titles held then lie stacked
  // under the river, the newest on top, each as thick as they had put into it by then, the earth tinted by the colours
  // it expects of them (and a fine line of the main one along its top). A bed swells in where its title began and
  // pinches out where it ended; a title still held runs on to now. Earth, not ink: the river stays the one saturated
  // thing on the strip.
  function drawStrata(g, G) {
    const { ly, X, now, know } = G, vis = I.runs.filter((r) => knows(r.seenW, know) && r.start < now);
    G.strata = [];
    if (!vis.length) return;
    const room = ly.strBot - ly.strTop - ly.gemsH, Tm = Math.min(ly.pitchMax * 1.3, room * 0.46), gap = 0.9 * Math.min(1.4, ly.s), stepX = 2;
    if (room < 1) return;
    const beds = vis.map((r) => {
      // its samples: the stops that held it so far; later ones stay, as the thickness eases between stops
      const ended = knows(r.knownW, know), e = ended ? Math.min(r.end, now) : now, x0 = X(r.start), x1 = X(e), smp = r.samples.filter((q) => q.a > know + 1e-6 || knows(q.w, know));
      const tl = Math.min(20 * ly.s, (x1 - x0) * 0.6), short = clamp((x1 - x0) / (44 * ly.s), 0.3, 1);
      // the bed's drawn extent: half a swell before its first year, half a pinch after its last (never past now)
      const xs = x0 - tl / 2, xe = ended ? Math.min(X(now), x1 + tl / 2) : x1;
      // the samples are read left to right, so a cursor walks them once instead of searching them at every column
      let ci = 1, ce = 0;
      const invAt = (a) => {
        if (!smp.length) return 0.3; if (a <= smp[0].a) return smp[0].inv * clamp((a - r.start) / Math.max(0.2, smp[0].a - r.start));
        if (ci > 1 && smp[ci - 1].a > a) ci = 1;
        while (ci < smp.length && smp[ci].a < a) ci++;
        if (ci >= smp.length) return smp[smp.length - 1].inv;
        const p = smp[ci - 1], q = smp[ci]; return p.inv + (q.inv - p.inv) * ((a - p.a) / Math.max(1e-6, q.a - p.a));
      };
      const expAt = (a) => {
        if (!smp.length) return [];
        if (smp[ce].a > a + 0.01) ce = 0;
        while (ce + 1 < smp.length && smp[ce + 1].a <= a + 0.01) ce++;
        return smp[ce].exp;
      };
      const th = (x) => (x < xs || x > xe ? 0 : Tm * short * (0.2 + 0.8 * invAt(G.sc.A(x))) * CH.smooth(clamp((x - xs) / tl)) * (ended ? CH.smooth(clamp((x1 + tl / 2 - x) / tl)) : CH.smooth(clamp((xe - x) / 2.5 + 0.45))));
      return { r, xs, xe, ended, th, expAt, P: [] };
    }).filter((b) => b.xe - b.xs >= 1.5).sort((p, q) => q.r.start - p.r.start);   // the newest on top
    if (!beds.length) return;
    // stack them column by column (every 2 px, 4 while the age eases); where too many lie at once, they all thin to fit
    const xa = Math.min(...beds.map((b) => b.xs)), xb = Math.max(...beds.map((b) => b.xe));
    const cols = [];
    for (let x = xa; x <= xb + stepX - 0.01; x += stepX) cols.push(Math.min(x, xb));
    beds.forEach((b) => { [b.xs, b.xe].forEach((x) => cols.push(x)); });
    cols.sort((p, q) => p - q);
    let lastX = -1;
    cols.forEach((x) => {
      if (x - lastX < 0.5) return; lastX = x;
      const ths = beds.map((b) => b.th(x)), sum = ths.reduce((s, v) => s + v + (v > 0 ? gap * Math.min(1, v / 2) : 0), 0), f = Math.min(1, room / Math.max(1e-6, sum));
      let y = ly.strTop;
      beds.forEach((b, i) => { if (x < b.xs - 0.01 || x > b.xe + 0.01) return; const t = ths[i] * f; b.P.push([x, y, y + Math.max(0.12, t), b.expAt(G.sc.A(x))]); y += t + gap * Math.min(1, ths[i] / 2) * f; });
    });
    beds.forEach((b) => {
      const P = b.P; if (P.length < 2) return;
      // the earth: for each stretch with the same expected colours, the bed in earth tinted by each of them in turn
      // (a soft band per colour), and a fine line of the main one along its top
      let i0 = 0;
      while (i0 < P.length - 1) {
        let i1 = i0; const key = P[i0][3].join("");
        while (i1 < P.length - 1 && P[i1 + 1][3].join("") === key) i1++;
        const cs = P[i0][3].length ? P[i0][3] : [""], seg = P.slice(i0, Math.min(P.length, i1 + 2));
        cs.forEach((c, j) => {
          const col = mix3(UMBER, c ? BAND[c] : [150, 140, 175], 0.28);
          g.fillStyle = rgba(col, 0.7); g.beginPath();
          seg.forEach(([x, t0, t1], q) => g[q ? "lineTo" : "moveTo"](x, t0 + ((t1 - t0) * j) / cs.length));
          for (let q = seg.length - 1; q >= 0; q--) g.lineTo(seg[q][0], seg[q][1] + ((seg[q][2] - seg[q][1]) * (j + 1)) / cs.length);
          g.closePath(); g.fill();
        });
        const c0 = cs[0];
        g.lineWidth = 0.8; g.strokeStyle = c0 ? rgba(mix3(BAND[c0], INK.pale[c0], 0.3), 0.5) : "rgba(220,210,235,0.25)";
        g.beginPath(); seg.forEach(([x, t0], q) => g[q ? "lineTo" : "moveTo"](x, t0 + 0.4)); g.stroke();
        i0 = i1 + 1;
      }
      // a quarrel with the title cracks its bed while it lasts
      const smp = b.r.samples.filter((q) => q.a > know + 1e-6 || knows(q.w, know));
      if (smp.some((s) => s.clash && s.a <= now)) {
        const bed = new Path2D();
        P.forEach(([x, t0], q) => bed[q ? "lineTo" : "moveTo"](x, t0));
        for (let q = P.length - 1; q >= 0; q--) bed.lineTo(P[q][0], P[q][2]);
        bed.closePath();
        g.save(); g.clip(bed);
        smp.forEach((s, q) => { if (!s.clash || s.a > now) return; const x0 = X(Math.max(b.r.start, q ? smp[q - 1].a : b.r.start)), x1 = X(Math.min(now, s.a)); if (x1 - x0 < 3) return;
          g.strokeStyle = "rgba(8,5,16,0.55)"; g.lineWidth = 0.7; g.beginPath();
          for (let x = x0; x <= x1; x += 3) { const c = P.find((p) => p[0] >= x) || P[P.length - 1], m = (c[1] + c[2]) / 2; g[x === x0 ? "moveTo" : "lineTo"](x, m + ((Math.round(x / 3) % 2) ? -1 : 1) * (c[2] - c[1]) * 0.22); }
          g.stroke(); });
        g.restore();
      }
      // a soft darker lower edge
      g.lineWidth = 0.6; g.strokeStyle = "rgba(6,4,14,0.25)"; g.beginPath(); P.forEach(([x, , t1], q) => g[q ? "lineTo" : "moveTo"](x, t1)); g.stroke();
      G.strata.push({ r: b.r, xs: b.xs, xe: b.xe, P, ended: b.ended });
    });
    // the engraving: fine hatching through every bed at once, laid only over the earth already there (source-atop)
    g.save(); g.globalCompositeOperation = "source-atop"; g.globalAlpha = 0.5; g.fillStyle = pat;
    g.fillRect(xa - 2, ly.strTop - 2, Math.min(G.nx, xb + 2) - xa + 4, room + 4); g.restore();
  }
  // the gems (perks, at the age they first came) and the wax seals (plans reached), set in one row low in the ground;
  // gems that would touch gather into a short run centred on their years. On a phone's strip only the seals show, as
  // small gold dots.
  function drawGems(g, G) {
    const { ly, X, know: now } = G, gr = ly.gemR, y = ly.strBot - gr - 0.5, list = [];
    G.gems = [];
    I.perks.forEach((p) => { if (knows(p.knownW, now)) list.push({ t: "gem", a: p.first, p }); });
    I.seals.forEach((s) => { if (knows(s.w, now)) list.push({ t: "seal", a: s.a, s }); });
    list.sort((p, q) => p.a - q.a);
    if (ly.sm) {
      list.forEach((o) => { if (o.t !== "seal") return; const x = X(o.a);
        put(g, G, x, y + 1, 2.2, 2.2, 2.2, (q, a, b) => { q.fillStyle = "rgba(244,223,166,0.85)"; q.beginPath(); q.arc(a, b, 1.6, 0, Math.PI * 2); q.fill(); });
        G.gems.push(Object.assign({ x, y: y + 1, r: 4.5, lost: false }, o)); });
      return;
    }
    // a perk lost by now leaves only a faint small outline where it was found, out of the row's spacing; the gems still
    // held and the seals share one row, spread apart where they crowd (each group centred on its years), never past now
    const lostAt = (o) => o.t === "gem" && !!(o.p.ev.filter((e) => knows(e.w, now)).pop() || {}).lost;
    const held = list.filter((o) => !lostAt(o)), lo = G.sc.x0 + gr, hi = G.nx - gr - 2, avail = Math.max(1, hi - lo);
    const gone = [];   // hovered after the row, so a held gem in front wins
    list.forEach((o) => { if (held.includes(o)) return; const x = X(o.a), e = gr * 0.8 * 1.3 + 1; put(g, G, x, y, e, e, e, (q, a, b) => gem(q, a, b, gr * 0.8, o.p.ways, o.p.kind, true)); gone.push(Object.assign({ x, y, r: gr * 0.8 + 1, lost: true }, o)); });
    let sp = gr * 2.2, R = gr;
    if (held.length * sp > avail) { sp = Math.max(avail / held.length, 0.1); if (sp < gr * 1.25) R = Math.max(1.4, sp / 1.25); }
    const groups = [];
    held.forEach((o) => {
      o.x = X(o.a); groups.push({ items: [o], sum: o.x });
      while (groups.length > 1) {
        const B = groups[groups.length - 1], A = groups[groups.length - 2], nA = A.items.length, nB = B.items.length;
        if ((B.sum / nB - ((nB - 1) * sp) / 2) - (A.sum / nA + ((nA - 1) * sp) / 2) >= sp) break;
        A.items.push(...B.items); A.sum += B.sum; groups.pop();
      }
    });
    const xs = [];
    groups.forEach((gp) => { const n = gp.items.length; gp.items.forEach((o, i) => xs.push(gp.sum / n + (i - (n - 1) / 2) * sp)); });
    // keep them in the lived years without overlapping: a pass from the left, then one from the right
    for (let i = 0; i < xs.length; i++) xs[i] = Math.max(xs[i], i ? xs[i - 1] + sp : lo);
    for (let i = xs.length - 1; i >= 0; i--) xs[i] = Math.min(xs[i], i < xs.length - 1 ? xs[i + 1] - sp : hi);
    held.forEach((o, i) => {
      const x = xs[i];
      const e = R * 1.5 + 1;
      if (o.t === "gem") put(g, G, x, y, e, e, e, (q, a, b) => gem(q, a, b, R, o.p.ways, o.p.kind, false));
      else put(g, G, x, y, e, e, e, (q, a, b) => seal(q, a, b, R * 1.12, o.s.cols, o.a));
      G.gems.push(Object.assign({ x, y, r: Math.max(R + 1.5, sp / 2), lost: false }, o));
    });
    G.gems.push(...gone);
  }
  // a small cut stone: its outline by the kind of perk (a skill a round brilliant, a credential square, something owned
  // a cushion, a bond a pear, standing a marquise), its facets in the colours of the ways it opens; a lost one leaves
  // only its outline in the ground
  function gem(g, x, y, r, ways, kind, lost) {
    const cs = ways.length ? ways : ["W"], c0 = cs[0], c1 = cs[1] || c0;
    const sides = { skill: 8, credential: 4, asset: 8, bond: 5, standing: 4 }[kind] || 6;
    const pts = [];
    for (let i = 0; i < sides; i++) {
      let ang = (i / sides) * Math.PI * 2 - Math.PI / 2 + (kind === "credential" ? Math.PI / 4 : kind === "asset" ? Math.PI / 8 : 0), rr = r;
      if (kind === "standing") rr = i % 2 ? r * 0.55 : r * 1.15;                                     // a marquise: long and narrow
      if (kind === "bond") rr = i === 0 ? r * 1.25 : r * 0.92;                                          // a pear: a point above
      pts.push([x + Math.cos(ang) * rr, y + Math.sin(ang) * rr * (kind === "asset" ? 0.84 : 1)]);
    }
    const outline = () => { g.beginPath(); pts.forEach((p, i) => g[i ? "lineTo" : "moveTo"](p[0], p[1])); g.closePath(); };
    if (lost) { pts.forEach((p) => { p[0] = x + (p[0] - x) * 0.85; p[1] = y + (p[1] - y) * 0.85; }); outline(); g.strokeStyle = rgba(mix3(RGB.bright[c0], [150, 140, 170], 0.6), 0.26); g.lineWidth = 0.5; g.stroke(); return; }
    g.save(); g.globalAlpha = 0.8;
    // the facets: from the centre to each edge, lit from the upper left
    for (let i = 0; i < sides; i++) {
      const p = pts[i], q = pts[(i + 1) % sides], mx = (p[0] + q[0]) / 2 - x, my = (p[1] + q[1]) / 2 - y;
      const lit = clamp(0.5 - (mx * 0.7 + my * 0.7) / (r * 1.4)), c = (i < sides / 2 ? c0 : c1);
      g.fillStyle = rgba(mix3(RGB.deep[c], lit > 0.5 ? RGB.pale[c] : RGB.bright[c], 0.25 + lit * 0.75), 1);
      g.beginPath(); g.moveTo(x, y); g.lineTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.closePath(); g.fill();
    }
    if (kind === "skill") {
      // a round brilliant: an octagonal table turned half a facet, and the star facets running from it to the girdle
      const tb = pts.map((_, i) => { const a = ((i + 0.5) / sides) * Math.PI * 2 - Math.PI / 2; return [x + Math.cos(a) * r * 0.5, y + Math.sin(a) * r * 0.5]; });
      g.fillStyle = rgba(mix3(RGB.bright[c0], [255, 255, 255], 0.4), 0.5); g.beginPath(); tb.forEach((p, i) => g[i ? "lineTo" : "moveTo"](p[0], p[1])); g.closePath(); g.fill();
      g.strokeStyle = "rgba(10,6,20,0.35)"; g.lineWidth = 0.35; g.beginPath();
      tb.forEach((p, i) => { g.moveTo(p[0], p[1]); g.lineTo(pts[i][0], pts[i][1]); g.moveTo(p[0], p[1]); g.lineTo(pts[(i + 1) % sides][0], pts[(i + 1) % sides][1]); }); g.stroke();
    } else {
      // the table (the flat top facet)
      g.fillStyle = rgba(mix3(RGB.bright[c0], [255, 255, 255], 0.35), 0.55);
      g.beginPath(); pts.forEach((p, i) => g[i ? "lineTo" : "moveTo"](x + (p[0] - x) * 0.42, y + (p[1] - y) * 0.42)); g.closePath(); g.fill();
    }
    outline(); g.strokeStyle = "rgba(10,6,20,0.8)"; g.lineWidth = 0.6; g.stroke();
    g.fillStyle = "rgba(255,255,255,0.9)"; g.beginPath(); g.arc(x - r * 0.3, y - r * 0.36, Math.max(0.4, r * 0.14), 0, Math.PI * 2); g.fill();
    g.restore();
  }
  // a wax seal: a round of wax with a soft uneven rim in the plan's colour, a ring pressed into it and a star at its heart
  function seal(g, x, y, r, cols, a) {
    const c = cols[0] || "W", rng = CH.rng(Math.round(a * 100) + 7), wax = mix3(RGB.deep[c], RGB.bright[c], 0.38);
    g.save(); g.globalAlpha = 0.85;
    g.fillStyle = rgba(wax, 1); g.beginPath();
    for (let i = 0; i <= 14; i++) { const t = (i / 14) * Math.PI * 2, rr = r * (1 + (rng() - 0.5) * 0.22); g[i ? "lineTo" : "moveTo"](x + Math.cos(t) * rr, y + Math.sin(t) * rr); }
    g.closePath(); g.fill();
    g.strokeStyle = "rgba(8,5,14,0.7)"; g.lineWidth = 0.6; g.stroke();
    g.strokeStyle = rgba(mix3(wax, [0, 0, 0], 0.45), 0.9); g.lineWidth = 0.7; g.beginPath(); g.arc(x, y, r * 0.62, 0, Math.PI * 2); g.stroke();
    g.fillStyle = rgba(mix3(wax, [255, 240, 200], 0.55), 0.95); g.beginPath();
    for (let i = 0; i < 10; i++) { const t = (i / 10) * Math.PI * 2 - Math.PI / 2, rr = i % 2 ? r * 0.18 : r * 0.42; g[i ? "lineTo" : "moveTo"](x + Math.cos(t) * rr, y + Math.sin(t) * rr); }
    g.closePath(); g.fill();
    g.fillStyle = "rgba(255,245,225,0.5)"; g.beginPath(); g.arc(x - r * 0.4, y - r * 0.45, r * 0.22, 0, Math.PI * 2); g.fill();
    g.restore();
  }

  /* ---------- the river ---------- */
  // in three parts, so a build can paint them in different frames: the glow, the bands, the shading and the ink
  function drawRiver(g, G, part) {
    const R = G.rv; if (!R) return;
    if (part === "ink" || part === "ink2") riverInk(g, G, R, part);
    else riverBody(g, G, R, part);
  }
  function riverBody(g, G, R, part) {
    const { ly, nx } = G;
    // its glow: the bands at a quarter size, drawn back large and soft under the crisp ones (the line's blurred copy);
    // softened once at the small size, so the cheap stretch back up stays smooth
    const bw = Math.max(1, Math.ceil(G.W / 4)), bh = Math.max(1, Math.ceil(G.H / 4));
    if (part !== "bands") {
      if (bloom.width !== bw || bloom.height !== bh) { bloom.width = bw; bloom.height = bh; }
      bctx.setTransform(1, 0, 0, 1, 0, 0); bctx.clearRect(0, 0, bw, bh); bctx.setTransform(0.25, 0, 0, 0.25, 0, 0);
      CS.forEach((c, j) => { bctx.fillStyle = rgba(BAND[c], 1); bctx.fill(R.bands[j]); });
      bctx.setTransform(1, 0, 0, 1, 0, 0);
      {
        if (bloomS.width !== bw || bloomS.height !== bh) { bloomS.width = bw; bloomS.height = bh; }
        sbctx.clearRect(0, 0, bw, bh); sbctx.filter = "blur(1px)"; sbctx.drawImage(bloom, 0, 0); sbctx.filter = "none";
        bctx.clearRect(0, 0, bw, bh); bctx.drawImage(bloomS, 0, 0);
      }
      const gx0 = Math.max(0, Math.floor((R.x0 - 12) / 4)), gx1 = Math.min(bw, Math.ceil((nx + 12) / 4));
      const gy0 = Math.max(0, Math.floor((ly.mid - ly.maxT) / 4)), gy1 = Math.min(bh, Math.ceil((ly.mid + ly.maxT) / 4));
      if (gx1 > gx0 && gy1 > gy0) { g.save(); g.globalAlpha = 0.34; g.drawImage(bloom, gx0, gy0, gx1 - gx0, gy1 - gy0, gx0 * 4, gy0 * 4, (gx1 - gx0) * 4, (gy1 - gy0) * 4); g.restore(); }
    }
    if (part === "glow") return;
    // the five bands, each a little brighter at its upper edge (the line's gradients), in the even inks
    CS.forEach((c, j) => {
      let y0 = 1e9, y1 = -1e9; for (let i = 0; i < R.SX.length; i += 4) { y0 = Math.min(y0, R.SY[j][i]); y1 = Math.max(y1, R.SY[j + 1][i]); }
      const gr = g.createLinearGradient(0, y0, 0, Math.max(y0 + 1, y1));
      gr.addColorStop(0, rgba(INK.top[c], 0.97)); gr.addColorStop(1, rgba(INK.low[c], 0.8));
      g.fillStyle = gr; g.fill(R.bands[j]);
    });
  }
  function riverInk(g, G, R, part) {
    const { ly, nx } = G;
    const span = Math.max(1, nx - R.x0), wetW = G.wetW;
    const ink = (al) => { const gr = g.createLinearGradient(R.x0, 0, nx, 0); gr.addColorStop(0, `rgba(10,6,22,${al})`); gr.addColorStop(clamp(1 - wetW / span), `rgba(10,6,22,${al})`); gr.addColorStop(1, `rgba(10,6,22,${al * (1 - 0.85 * G.wet)})`); return gr; };
    g.lineJoin = "round";
    if (part === "ink2") {      // (the second step: the outer edges, the sheen, the blooms and the wet stretch's copy)
      g.strokeStyle = ink(0.5); g.lineWidth = 0.85;
      const oe = new Path2D(); R.edgePath(0, false, oe); R.edgePath(5, false, oe); g.stroke(oe);
      riverWet(g, G, R, wetW);
      return;
    }
    // body: a little shade at the very outer edges, so the river reads round, not flat; the same above and below and
    // kept thin, as White and Green always run on the outside and must not look darker than the colours between
    const sh = g.createLinearGradient(0, ly.mid - ly.maxT / 2, 0, ly.mid + ly.maxT / 2);
    sh.addColorStop(0, "rgba(10,6,24,0.24)"); sh.addColorStop(0.13, "rgba(10,6,24,0)"); sh.addColorStop(0.87, "rgba(10,6,24,0)"); sh.addColorStop(1, "rgba(10,6,24,0.24)");
    g.fillStyle = sh; g.fill(R.outline);
    // dry ink is engraved: fine dark lines between the bands and round the river (its outer edges in the next step),
    // softening toward now as long as the ink there is still wet (B1: wet near the pen, set behind it)
    g.strokeStyle = ink(0.30); g.lineWidth = 0.55;
    const dv = new Path2D(); for (let j = 1; j < 5; j++) R.edgePath(j, false, dv); g.stroke(dv);
  }
  function riverWet(g, G, R, wetW) {
    const { nx } = G;
    // the sheen along its upper edge (the line's .sheen)
    g.save(); g.translate(0, 0.9); const sp = new Path2D(); R.edgePath(0, false, sp); g.strokeStyle = "rgba(255,255,255,0.2)"; g.lineWidth = 0.8; g.stroke(sp); g.restore();
    // B1 blooms: where wet ink ran past the edge it dried as a small pale wash with a darker rim (a watercolour
    // backrun), a few along the wet stretch, as many and as strong as the ink is wet; seeded, so the same age looks the
    // same
    if (G.wet > 0.05 && wetW > 16) {
      const r = CH.rng(77), n = Math.round(3 + 3 * G.wet);
      for (let i = 0; i < n; i++) {
        const x = nx - 5 - r() * (wetW - 10), top = r() < 0.5, c = top ? CS[0] : CS[4], ey = edge(x, top ? 0 : 5), th = edge(x, 5) - edge(x, 0);
        if (th < 5) { r(); r(); r(); continue; }
        const rad = (2 + r() * 3.2) * (0.55 + 0.6 * G.wet), y = ey + (top ? -1 : 1) * (rad * 0.3 + r() * 1.2), ph = r() * 6.3, b = BAND[c];
        const blob = () => { g.beginPath(); for (let q = 0; q <= 12; q++) { const t = (q / 12) * Math.PI * 2, w = 1 + 0.26 * (CH.noise(ph + Math.cos(t) * 1.3, Math.sin(t) * 1.3 + i) - 0.5) * 2; g[q ? "lineTo" : "moveTo"](x + Math.cos(t) * rad * 1.35 * w, y + Math.sin(t) * rad * 0.75 * w); } g.closePath(); };
        blob(); g.fillStyle = rgba(b, 0.16 * G.wet); g.fill();
        g.strokeStyle = rgba(mix3(INK.deep[c], b, 0.45), 0.24 * G.wet); g.lineWidth = 0.5; g.stroke();
      }
    }
    // the wet stretch's own soft copy (drawn each frame, breathing): the glow kept only over the last wetW pixels
    G.wetMask = false;
    if (G.wet > 0.02) {
      const bN = G.bN, nctx = bN.getContext("2d");
      if (bN.width !== bloom.width || bN.height !== bloom.height) { bN.width = bloom.width; bN.height = bloom.height; }
      nctx.setTransform(1, 0, 0, 1, 0, 0); nctx.globalCompositeOperation = "source-over"; nctx.clearRect(0, 0, bN.width, bN.height);
      nctx.drawImage(bloom, 0, 0); nctx.globalCompositeOperation = "destination-in";
      const m = nctx.createLinearGradient((nx - wetW) / 4, 0, (nx + 10) / 4, 0);
      m.addColorStop(0, "rgba(0,0,0,0)"); m.addColorStop(0.75, "rgba(0,0,0,1)"); m.addColorStop(1, "rgba(0,0,0,0)");
      nctx.fillStyle = m; nctx.fillRect(0, 0, bN.width, bN.height); nctx.globalCompositeOperation = "source-over";
      G.wetMask = true;
    }
  }
  // the identity band under the river: who they were, year by year (the game's recorded identity, from each year's
  // chapter line), each identity blending into the next (lnBand)
  function drawBand(g, G) {
    const { X, ly, now, nx } = G;
    if (now <= 0.05) return;
    const ch = I.items.filter((x) => x.tag === "chapter" && (x.age ?? 0) <= now + 1e-6 && knows(wI(x), G.know)), runs = [];
    const add = (l, a0, a1) => { if (a1 <= a0) return; if (runs.length && runs[runs.length - 1].l === l) runs[runs.length - 1].a1 = a1; else runs.push({ l, a0, a1 }); };
    if (!ch.length || ch[0].age > 0) add("", 0, ch.length ? Math.min(now, ch[0].age) : now);
    ch.forEach((c, i) => add(c.label || "", c.age ?? 0, i + 1 < ch.length ? ch[i + 1].age : now));
    if (!runs.length) runs.push({ l: "", a0: 0, a1: now });
    const xa = X(0), xb = Math.max(xa + 1, nx), at = (x) => clamp((x - xa) / (xb - xa));
    const gr = g.createLinearGradient(xa, 0, xb, 0);
    runs.forEach((u) => {
      const cs = CH.lettersOf(u.l), parts = cs.length ? cs : [""], x0 = X(u.a0), w = Math.max(0, X(Math.min(u.a1, now)) - x0) / parts.length;
      parts.forEach((c, j) => { const p0 = x0 + w * j, e = Math.min(w * 0.3, 9), col = c ? rgba(BAND[c], 0.95) : "rgba(214,205,245,0.22)";
        gr.addColorStop(at(p0 + e), col); gr.addColorStop(at(p0 + w - e), col); });
    });
    const y = ly.bandY, h = ly.bandH;
    g.save(); g.globalAlpha = 0.22; g.fillStyle = gr; rr(g, xa, y - 1.2, xb - xa, h + 2.4, (h + 2.4) / 2); g.fill(); g.restore();
    g.fillStyle = gr; rr(g, xa, y, xb - xa, h, h / 2); g.fill();
    g.strokeStyle = "rgba(255,255,255,0.18)"; g.lineWidth = 0.5; g.beginPath(); g.moveTo(xa + h, y + 0.4); g.lineTo(xb - 1, y + 0.4); g.stroke();
  }
  // into the fog, the thread of who they are now, fading into the years ahead
  function drawFogThread(g, D) {
    if (D.over || D.now <= 0.05) return;
    const y = D.ly.bandY + D.ly.bandH / 2, lc = CH.lettersOf(S && S.label), c0 = lc.length ? BAND[lc[lc.length - 1]] : LILAC;
    const ag = g.createLinearGradient(D.nx, 0, D.sc.xE, 0);
    ag.addColorStop(0, rgba(c0, 0.75 * fogV + 0.1)); ag.addColorStop(0.22, rgba(LILAC, 0.26 * fogV)); ag.addColorStop(1, rgba(LILAC, 0.04 * fogV));
    g.strokeStyle = ag; g.lineWidth = 1.2; g.lineCap = "round"; g.beginPath(); g.moveTo(D.nx, y); g.lineTo(D.sc.xE, y); g.stroke();
  }
  const rr = (g, x, y, w, h, r) => { r = Math.min(r, w / 2, h / 2); g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };

  /* ---------- W3: the threads above the river ---------- */
  // each visible thread's arc: it leaves the river's upper edge where the line began and comes back down where it was
  // tied off (or at now). Its height grows with the log of its length (plans lower than commitments), so long lines
  // stay round arcs rather than flat rules; the open lines land spread over the last few pixels before now, the oldest
  // nearest now, so their arcs nest instead of knotting at one point.
  function threadGeo(G) {
    const { X, ly, now } = G;
    G.threads = []; G.points = [];
    if (!G.rv) return;
    const capOf = { commit: 1, dream: 0.86, clash: 0.72, plan: 0.62 };
    const isClosed = (t) => knows(t.k1W, G.know);
    const vis = I.threads.filter((t) => knows(t.seenW, G.know));
    const open = vis.filter((t) => !isClosed(t)).sort((p, q) => p.a0 - q.a0), spread = Math.min(9, 1.5 * Math.max(0, open.length - 1) + 3);
    const lw = Math.max(8, G.nx - G.sc.x0), lnL = Math.log(1 + lw);
    vis.forEach((t) => {
      const closed = isClosed(t), oi = closed ? -1 : open.indexOf(t);
      const xs = X(t.a0), xe = closed ? Math.max(xs, X(t.a1)) : Math.max(xs, G.nx - 1 - (open.length > 1 ? (spread * oi) / (open.length - 1) : 0));
      const ys = edge(xs, 0) - 0.4, ye = edge(xe, 0) - 0.4;
      const room = Math.max(4, Math.min(ys, ye) - ly.thTop), span = xe - xs;
      const h = span < 4 ? Math.min(room, 5 * ly.s) : Math.max(3, 0.85 * room * (capOf[t.type] || 0.7) * (Math.log(1 + span) / lnL));
      G.threads.push({ t, xs, xe, ys, ye, h, closed, span });
    });
    // keep long arcs of nearly the same height apart, a hair's breadth each
    const byH = G.threads.slice().sort((p, q) => q.span - p.span);
    byH.forEach((A, i) => { for (let j = 0; j < i; j++) { const B = byH[j], ov = Math.min(A.xe, B.xe) - Math.max(A.xs, B.xs);
      if (ov > Math.min(A.span, B.span) * 0.3 && Math.abs(A.h - B.h) < 2.2 * ly.s && A.h > 6) A.h = Math.max(3, A.h - 2.4 * ly.s); } });
    G.threads.forEach((T) => {
      const { xs, xe, ys, ye, h, span } = T, pts = [];
      if (span < 4) {   // a line begun and ended within months: a small stitch loop
        const w = Math.max(2.2, span);
        for (let i = 0; i <= 12; i++) { const u = i / 12; pts.push([bez(xs - 1, xs - 1.5, xs + w + 1.5, xs + w + 1, u), bez(ys, ys - h * 1.33, ys - h * 1.33, ye, u)]); }
      } else {
        // the control points stand straight over the ends, so the arc leaves and lands upright and stays round
        const top = Math.min(ys, ye) - h / 0.75, n = Math.max(10, Math.min(320, Math.ceil(span / 2.5)));
        for (let i = 0; i <= n; i++) { const u = i / n; pts.push([bez(xs, xs, xe, xe, u), bez(ys, top, top, ye, u)]); }
      }
      T.pts = pts;
    });
    I.points.forEach((p) => { if (!knows(p.w, Math.min(now, G.know))) return; const x = X(p.a); G.points.push({ p, x, y: edge(x, 0) - 0.5 }); });
  }
  // a thread's colour strands: one ply per colour (two at most), twisted round each other when there are two. `fade`
  // (0..1) lets the strand fade along its chord toward its end; `s0` carries the twist on from an earlier piece.
  function strand(g, pts, cols, al, w, dash, fade, s0) {
    const cs = cols.length ? cols.slice(0, 2) : [null];
    if (pts.length < 2) return;
    const style = (rgb, a) => {
      if (fade == null) return rgba(rgb, a);
      const p = pts[0], q = pts[pts.length - 1], gr = g.createLinearGradient(p[0], p[1], q[0] + 0.01, q[1]);
      gr.addColorStop(0, rgba(rgb, a)); gr.addColorStop(1, rgba(rgb, a * fade)); return gr;
    };
    if (dash && dash.beads) {   // a dream: beads of its colours in turn along one line
      g.lineCap = "round";
      cs.forEach((c, k) => { g.setLineDash([0.01, 3.2 * cs.length]); g.lineDashOffset = -3.2 * k - (s0 || 0); g.strokeStyle = style(c ? BAND[c] : LILAC, c ? al * 1.3 : al); g.lineWidth = w * 1.5;
        g.beginPath(); pts.forEach(([x, y], i) => g[i ? "lineTo" : "moveTo"](x, y)); g.stroke(); });
      g.setLineDash([]); g.lineDashOffset = 0; return;
    }
    if (dash) g.setLineDash(dash);
    cs.forEach((c, k) => {
      g.strokeStyle = style(c ? BAND[c] : LILAC, c ? al : al * 0.8); g.lineWidth = cs.length > 1 ? w * 0.8 : w;
      g.beginPath();
      let s = s0 || 0;
      for (let i = 0; i < pts.length; i++) {
        const [x, y] = pts[i];
        if (cs.length > 1) {
          const p = pts[Math.max(0, i - 1)], q = pts[Math.min(pts.length - 1, i + 1)], dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1;
          if (i) s += Math.hypot(x - pts[i - 1][0], y - pts[i - 1][1]);
          const o = 0.75 * Math.sin(s / 2.4 + k * Math.PI);
          g[i ? "lineTo" : "moveTo"](x - (dy / L) * o, y + (dx / L) * o);
        } else g[i ? "lineTo" : "moveTo"](x, y);
      }
      g.stroke();
    });
    if (dash) g.setLineDash([]);
  }
  const BEADS = { beads: true };
  const pathLen = (pts, i0, i1) => { let s = 0; for (let i = i0 + 1; i <= i1; i++) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return s; };
  // where a thread's last `len` px of length begin
  const tailFrom = (pts, len) => { let s = 0, i = pts.length - 1; while (i > 1 && s < len) { s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); i--; } return i; };
  // half = 1 or 2 draws only the first or the second half of them (a build paints them in two frames)
  function drawThreads(g, G, half) {
    const s = G.ly.s, n = G.threads.length, lo = half === 2 ? Math.ceil(n / 2) : 0, hi = half === 1 ? Math.ceil(n / 2) : n;
    g.lineCap = "round"; g.lineJoin = "round";
    G.threads.forEach((T, i) => {
      if (i < lo || i >= hi) return;
      // a line tied off long ago recedes, as memory does; the lines still open stay clear
      const t = T.t, pts = T.pts, rec = T.closed ? clamp(1 - (G.now - t.a1) / 30) : 1, al = (T.closed ? 0.22 + 0.24 * rec : 0.6) * (t.type === "dream" ? 0.85 : 1), w = (t.type === "commit" ? 1.05 : 0.9) * Math.min(1.4, s);
      const dash = t.type === "dream" ? BEADS : t.type === "clash" ? [1, 1.6] : null;
      if (T.closed && t.end === "fade") {   // a line that faded rather than ended: it thins out over its last stretch
        const c = Math.floor(pts.length * 0.62);
        strand(g, pts.slice(0, c + 1), t.cols, al, w, dash);
        strand(g, pts.slice(c), t.cols, al, w, dash, 0, pathLen(pts, 0, c));
      } else if (!T.closed && pts.length > 4) {   // a line still open runs on into the gleam at now, fading as it lands
        const c = tailFrom(pts, Math.min(22, pathLen(pts, 0, pts.length - 1) * 0.4));
        strand(g, pts.slice(0, c + 1), t.cols, al, w, dash);
        strand(g, pts.slice(c), t.cols, al, w, dash, 0.12, pathLen(pts, 0, c));
      } else strand(g, pts, t.cols, al, w, dash);
      const c = t.cols[0], col = c ? BAND[c] : LILAC, [ex, ey] = pts[pts.length - 1];
      // where it began: a stitch into the river
      g.fillStyle = rgba(col, 0.7); g.beginPath(); g.arc(pts[0][0], pts[0][1], 0.9 * Math.min(1.4, s), 0, Math.PI * 2); g.fill();
      // beads: a change along the way (a new employer, a plan given more time), only those the story has reached
      t.beads.forEach((b) => { if (!knows(b.w, G.know)) return; const bx = G.X(b.a); let best = pts[0]; for (const p of pts) if (Math.abs(p[0] - bx) < Math.abs(best[0] - bx)) best = p;
        g.fillStyle = rgba(mix3(col, [255, 255, 255], 0.5), 0.8); g.beginPath(); g.arc(best[0], best[1], 1.2 * Math.min(1.4, s), 0, Math.PI * 2); g.fill(); });
      if (!T.closed) return;
      // how it ended: tied off in a knot; a plan reached in a gold one; a plan let go frays; a faded line simply thins out
      const r = 1.6 * Math.min(1.4, s);
      if (t.end === "knot" || t.end === "gold") {
        const kc = t.end === "gold" ? GOLD2 : mix3(col, [255, 255, 255], 0.15);
        if (t.end === "gold") { g.fillStyle = "rgba(244,223,166,0.22)"; g.beginPath(); g.arc(ex, ey - r * 0.6, r * 2.4, 0, Math.PI * 2); g.fill(); }
        g.strokeStyle = rgba(kc, 0.85 * (0.6 + 0.4 * rec)); g.lineWidth = 0.7;
        g.beginPath(); g.moveTo(ex, ey - r * 0.6); g.lineTo(ex + r * 1.7, ey + r * 0.9); g.moveTo(ex, ey - r * 0.6); g.lineTo(ex + r * 0.4, ey + r * 1.6); g.stroke();
        g.fillStyle = rgba(kc, 0.6 + 0.4 * rec); g.beginPath(); g.ellipse(ex, ey - r * 0.6, r, r * 0.8, -0.5, 0, Math.PI * 2); g.fill();
        g.strokeStyle = "rgba(8,5,16,0.7)"; g.lineWidth = 0.5; g.stroke();
      } else if (t.end === "loose") {
        g.strokeStyle = rgba(col, 0.5); g.lineWidth = 0.5; g.beginPath();
        [-0.9, 0, 0.9].forEach((d) => { g.moveTo(ex, ey); g.lineTo(ex + r * 1.2 + d * 0.4, ey - r * (0.6 + d)); });
        g.stroke();
      }
    });
  }
  // breakthroughs (a short flare rising out of the river, a star at its tip) and turns (a hook from the old colour into
  // the new one)
  function drawPoints(g, G) {
    const s = Math.min(1.4, G.ly.s);
    G.points.forEach(({ p, x: px, y: py }) => put(g, G, px, py, 5 * s + 1, 12.5 * s + 1, 1.5, (g, x, y) => {
      if (p.type === "break") {
        const c = p.cols[0] || "W", col = RGB.bright[c], top = y - 9 * s;
        const gr = g.createLinearGradient(0, y, 0, top); gr.addColorStop(0, rgba(col, 0)); gr.addColorStop(1, rgba(col, 0.9));
        g.strokeStyle = gr; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x, top); g.stroke();
        g.fillStyle = rgba(mix3(col, [255, 255, 255], 0.4), 0.95); g.beginPath();
        for (let i = 0; i < 8; i++) { const t = (i / 8) * Math.PI * 2, rr2 = i % 2 ? 0.8 * s : 3 * s; g[i ? "lineTo" : "moveTo"](x + Math.cos(t) * rr2, top + Math.sin(t) * rr2); }
        g.closePath(); g.fill();
      } else {
        const a = p.from ? RGB.bright[p.from] : LILAC, b = p.to ? RGB.bright[p.to] : LILAC, top = y - 9 * s;
        const gr = g.createLinearGradient(x - 3 * s, y, x + 3 * s, top); gr.addColorStop(0, rgba(a, 0.85)); gr.addColorStop(1, rgba(b, 0.95));
        g.strokeStyle = gr; g.lineWidth = 1.1; g.beginPath(); g.moveTo(x - 3 * s, y); g.bezierCurveTo(x - 3 * s, top, x + 4 * s, y - 4 * s, x + 3 * s, top); g.stroke();
        g.fillStyle = rgba(b, 1); g.beginPath(); g.arc(x + 3 * s, top, 1.4 * s, 0, Math.PI * 2); g.fill();
      }
    }));
  }

  /* a small round thing at (x, y), reaching hw to each side, up above and dn below: drawn in place in a still layer;
     in a cache, into the atlas at the next free slot (a pixel apart), its place in the years kept with it */
  function put(g, G, x, y, hw, up, dn, fn) {
    const A = G.atlas;
    if (!A) { fn(g, x, y); return; }
    const w = Math.ceil(hw * 2) + 2, h = Math.ceil(up + dn) + 2;
    if (A.cx + w > A.W) { A.cx = 0; A.cy += A.rowH; A.rowH = 0; }
    if (A.cy + h > A.H) { fn(g, x, y); return; }   // the atlas is full: in place, stretched with the years
    const ax = A.cx + 1 + hw, ay = A.cy + 1 + up;
    fn(A.g, ax, ay); A.list.push([x, y, hw, up, dn, ax, ay]);
    A.cx += w; A.rowH = Math.max(A.rowH, h);
  }

  /* ---------- B3: the doors in the fog ---------- */
  // five doorways at fixed places in the fog, W U B R G from the nearest to the farthest, standing on the ground line;
  // set a little off an even row and at slightly different depths (seeded, the same every time), so they read as
  // arches standing in a landscape, not a row of gauges. On a narrow strip they stand smaller, with a clear gap.
  function doorGeo(D) {
    const out = [];
    if (D.over) return out;
    const { ly, sc } = D, nx = fogFrom(D), fw = sc.xE - nx;
    let dh = Math.min(ly.bandY - ly.thTop - 10 * Math.min(1.4, ly.s), ly.maxT * 1.18), dw = dh * 0.4;
    const lo = nx + (ly.sm ? Math.max(12, dw * 0.9) : Math.max(52, dw * 1.8)), hi = sc.xE - (ly.sm ? 5 : dw * 0.9);
    if ((hi - lo) / 5 < dw * 1.6) { dw = (hi - lo) / 8; dh = Math.min(dh, dw / (ly.sm ? 0.45 : 0.38)); }
    if (dw < 4 || fw < 40) return out;
    const slot = (hi - lo) / 5, jit = Math.max(0, (slot - 1.7 * dw) / 2), rng = CH.rng(509);
    CS.forEach((c, i) => {
      const j = (i % 2 ? 1 : -1) * jit * (0.35 + 0.4 * rng()), depth = 0.95 + 0.07 * rng();
      out.push({ c, i, x: lo + slot * (i + 0.5) + j, base: ly.bandY + ly.bandH / 2, w: dw, h: dh, depth, small: dw < 10 || ly.sm });
    });
    return out;
  }
  // a door's drawn shape from how open the way is (S.doors, 0 to about 1.5): a narrowing way stands smaller and farther
  // off (higher, toward the horizon) and dimmer; never gone, never shut (tendencies, not walls)
  const doorOpen = (v) => sstep(0.6, 1.1, v);
  function doorShape(d) {
    const v = doorsV ? doorsV[d.i] : 0.8, o = doorOpen(v), scl = (0.72 + 0.28 * o) * d.depth;
    const w = d.w * scl, h = d.h * scl, base = d.base - (1 - scl) * d.h * 0.42;
    return { v, o, lit: 0.18 + 0.82 * o, w, h, base, x: d.x, top: base - h };
  }
  // how each colour's light moves (the five-colour grammar): White even, Blue clear and slow, Black a slow low tide,
  // Red a flicker, Green a dappled breath. All of the same strength.
  const DOOR_FX = {
    W: (t) => 1 + 0.06 * Math.sin(t * 0.9),
    U: (t) => 1 + 0.07 * Math.sin(t * 0.55 + 1),
    B: (t) => 1 + 0.09 * Math.sin(t * 0.32 + 2),
    R: (t) => 1 + 0.05 * Math.sin(t * 6.1) * Math.sin(t * 2.3) + 0.04 * Math.sin(t * 1.4),
    G: (t) => 1 + 0.08 * Math.sin(t * 0.7 + 4) * (0.6 + 0.4 * Math.sin(t * 0.21)),
  };
  const archPath = (g, x, base, w, h) => { const r = w / 2; g.beginPath(); g.moveTo(x - r, base); g.lineTo(x - r, base - h + r); g.arc(x, base - h + r, r, Math.PI, 0); g.lineTo(x + r, base); };
  // a door is painted once into two small images for its shape (made again when its shape or brightness changes): its
  // light (the halo, the light through the doorway, the pool before it), laid on additively with its colour's flicker
  // as the image's strength, and its arch, keystone and mist, laid on as they are
  const doorSpr = new Map();
  function paintDoor(g, d, sh, which) {
    const { lit, w, h, base, x, top } = sh, small = d.small, b = BAND[d.c], p = INK.pale[d.c], r = w / 2;
    if (which === "glow") {
      const fx = 1.3;    // the image holds the light at its strongest (a hovered door's); the flicker dims it from there
      const halo = g.createRadialGradient(x, base - h * 0.45, 0, x, base - h * 0.45, h * 1.05);
      halo.addColorStop(0, rgba(b, 0.13 * lit * fx)); halo.addColorStop(0.5, rgba(b, 0.045 * lit * fx)); halo.addColorStop(1, rgba(b, 0));
      g.fillStyle = halo; g.fillRect(x - h * 1.1, base - h * 1.5, h * 2.2, h * 2);
      // the light beyond, spilling through the doorway: brightest low in the middle, as light through a gap
      g.save(); archPath(g, x, base, w - 0.8, h - 0.4); g.closePath(); g.clip();
      g.globalCompositeOperation = "lighter";
      g.translate(x, base - h * 0.32); g.scale(1, 2.3);
      const inner = g.createRadialGradient(0, 0, 0, 0, 0, r * 1.15);
      inner.addColorStop(0, rgba(mix3(p, [255, 255, 255], 0.3), 0.5 * lit * fx)); inner.addColorStop(0.45, rgba(b, 0.2 * lit * fx)); inner.addColorStop(1, rgba(b, 0));
      g.fillStyle = inner; g.fillRect(-r * 1.2, -h, r * 2.4, h * 2);
      g.restore();
      // the light pooling on the ground before the threshold, spilling forward toward now
      g.save(); g.globalCompositeOperation = "lighter"; g.translate(x - w * 0.25, base + 0.6); g.scale(1, 0.2);
      const pool = g.createRadialGradient(0, 0, 0, 0, 0, w * 1.8); pool.addColorStop(0, rgba(p, 0.32 * lit * fx)); pool.addColorStop(1, rgba(p, 0));
      g.fillStyle = pool; g.beginPath(); g.arc(0, 0, w * 1.8, 0, Math.PI * 2); g.fill(); g.restore();
      return;
    }
    // Black's arch takes a gold-violet rim, so it stands out of the lilac fog as clearly as the others do
    const rim = d.c === "B" ? mix3(b, GOLD2, 0.3) : mix3(b, p, 0.35);
    // the arch: a fine engraved hairline in the colour's ink, a fainter outer line; Blue's doubled as through glass
    g.lineWidth = small ? 0.6 : 0.8; g.strokeStyle = rgba(rim, 0.24 + 0.62 * lit); archPath(g, x, base, w, h); g.stroke();
    if (!small) { g.lineWidth = 0.45; g.strokeStyle = rgba(rim, 0.06 + 0.2 * lit); archPath(g, x, base, w + 2.8, h + 1.4); g.stroke(); }
    if (d.c === "U" && !small) { g.save(); g.globalAlpha *= 0.35; g.translate(1.1, -0.6); g.lineWidth = 0.55; g.strokeStyle = rgba(p, 0.6 * lit); archPath(g, x, base, w, h); g.stroke(); g.restore(); }
    // the keystone: the colour's own glyph set in the crown of the arch (a small bead of light on a small strip)
    if (!small) {
      const kr = Math.max(3.6, w * 0.24), ky = top - 0.3;
      g.fillStyle = "rgba(12,9,26,0.6)"; g.beginPath(); g.arc(x, ky, kr, 0, Math.PI * 2); g.fill();
      g.strokeStyle = rgba(rim, 0.25 + 0.6 * lit); g.lineWidth = 0.6; g.stroke();
      const im = glyphImg(d.c, () => { dirty = true; fogDirty = true; });
      if (im) { g.globalAlpha = 0.45 + 0.55 * lit; g.drawImage(im, x - kr * 0.74, ky - kr * 0.74, kr * 1.48, kr * 1.48); g.globalAlpha = 1; }
    } else { g.fillStyle = rgba(rim, 0.3 + 0.6 * lit); g.beginPath(); g.arc(x, top, Math.max(0.8, w * 0.1), 0, Math.PI * 2); g.fill(); }
    // the mist it stands in: a low veil over its lower third
    g.save(); g.translate(x, base + h * 0.02); g.scale(1, 0.42);
    const veil = g.createRadialGradient(0, 0, 0, 0, 0, Math.max(w * 1.5, h * 0.75));
    veil.addColorStop(0, rgba(FOGC, 0.62)); veil.addColorStop(0.55, rgba(FOGC, 0.32)); veil.addColorStop(1, rgba(FOGC, 0));
    g.fillStyle = veil; g.beginPath(); g.arc(0, 0, Math.max(w * 1.5, h * 0.75), 0, Math.PI * 2); g.fill(); g.restore();
  }
  function doorSprite(d, sh) {
    const k = G.k, { w, h, base, x, top } = sh, im = !d.small && !!glyphImg(d.c, () => { dirty = true; fogDirty = true; });
    // (to half a pixel and a twentieth of its light: a door easing to its new reading is painted again a few times,
    // not every time the fog is drawn)
    const key = `${Math.round(w * 2)}|${Math.round(h * 2)}|${Math.round(sh.lit * 20)}|${k}|${im}|${d.small}`;
    const had = doorSpr.get(d.i);
    if (had && had.key === key) return had;
    const rx = Math.max(1.1 * h, 2.05 * w, 0.75 * h) + 3, y0 = Math.min(base - 1.5 * h, top - Math.max(3.6, w * 0.24)) - 3;
    const y1 = base + Math.max(0.5 * h, 0.42 * Math.max(w * 1.5, h * 0.75) + 0.02 * h, 0.6 + 0.36 * w) + 3, bw = Math.ceil(rx * 2 * k), bh = Math.ceil((y1 - y0) * k);
    const at = (c) => c.setTransform(k, 0, 0, k, -(x - rx) * k, -y0 * k);
    const S2 = { key, bx: x, by: base, dx: x - rx, dy: y0, w: rx * 2, h: y1 - y0, glow: repaint(had && had.glow, bw, bh, (c) => { at(c); paintDoor(c, d, sh, "glow"); }), body: repaint(had && had.body, bw, bh, (c) => { at(c); paintDoor(c, d, sh, "body"); }) };
    doorSpr.set(d.i, S2);
    return S2;
  }
  function drawDoors(g, t, doors) {
    if (!doors.length || fogV < 0.02) return;
    const moving = !off();
    doors.forEach((d) => {
      const sh = doorShape(d), hov = hover && hover.door === d.i ? 1.3 : 1, fx = (moving ? DOOR_FX[d.c](t) : 1) * hov, sp = doorSprite(d, sh);
      // laid where the door stands now (the images keep their shape as now moves the doors along)
      const px = sp.dx + sh.x - sp.bx, py = sp.dy + sh.base - sp.by;
      g.save();
      g.globalCompositeOperation = "lighter"; g.globalAlpha = fogV * Math.min(1, fx / 1.3);
      g.drawImage(sp.glow, px, py, sp.w, sp.h);
      g.globalCompositeOperation = "source-over"; g.globalAlpha = fogV;
      g.drawImage(sp.body, px, py, sp.w, sp.h);
      g.restore();
    });
  }

  /* ---------- C2: the voice's pushes, as seams and knots in the river ---------- */
  // each push's crack: an irregular line down through the bands (noise, not a zig-zag), widest in its middle and fine at
  // both ends, with one or two short branches; seeded by its age, so it is always the same crack
  function pushGeo(G) {
    G.pushes = [];
    if (!G.rv) return;
    const tn = performance.now();
    (CH.life.pushes || []).forEach((p) => {
      const at = { a: p.age, si: p.stop };
      if (!knows(at, Math.min(G.now, G.know))) return;
      if (pend.has(p) && tn - pend.get(p) < 2500) return;          // its outcome is not shown yet
      const x = G.X(p.age), top = edge(x, 0), bot = edge(x, 5), rng = CH.rng(Math.round(p.age * 997));
      // a crack runs in from one edge (seeded) most of the way across, as a crack in a bowl does, not edge to edge
      const n = 18 + Math.floor(rng() * 7), amp = 2.6 + rng() * 1.2, ph = rng() * 50, pts = [], up = rng() < 0.5, reach = 0.62 + rng() * 0.3;
      for (let i = 0; i <= n; i++) {
        const u = i / n, taper = u < 0.5 ? 0.4 + 1.2 * u : 1 - 1.4 * (u - 0.5);
        const dx = amp * taper * ((CH.noise(ph + u * 4.2, 1.3) - 0.5) * 2 + (CH.noise(ph + u * 13, 7.7) - 0.5) * 0.7), f = u * reach;
        pts.push([x + dx, up ? bot - (bot - top) * f : top + (bot - top) * f]);
      }
      const br = [], nb = 1 + (rng() < 0.5 ? 1 : 0);
      for (let b = 0; b < nb; b++) {
        const i0 = 4 + Math.floor(rng() * Math.max(1, n - 9)), dir = rng() < 0.5 ? -1 : 1, len = (bot - top) * (0.1 + rng() * 0.08), seg = [pts[i0]];
        for (let q = 1; q <= 4; q++) { const u = q / 4; seg.push([pts[i0][0] + dir * len * 0.85 * u + (CH.noise(ph + b * 9 + u * 3, 4.1) - 0.5) * 1.2, pts[i0][1] + (up ? -len : len) * u]); }
        br.push(seg);
      }
      G.pushes.push({ p, at, x, top, bot, pts, br, mid: (top + bot) / 2, rot: rng() * Math.PI, born: born.get(p) || 0 });
    });
  }
  // a stroke that tapers from w0 to w1 along its first n points, filled as one ribbon (no beads where segments meet)
  function taper(g, pts, n, w0, w1, col, dx, dy) {
    n = Math.min(n, pts.length); if (n < 2) return;
    const lft = [], rgt = [], last = Math.max(1, pts.length - 1);
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
      const nx = -(b[1] - a[1]) / l, ny = (b[0] - a[0]) / l, w = (w0 + (w1 - w0) * (i / last)) / 2, px = pts[i][0] + dx, py = pts[i][1] + dy;
      lft.push([px + nx * w, py + ny * w]); rgt.push([px - nx * w, py - ny * w]);
    }
    g.fillStyle = col; g.beginPath(); g.moveTo(lft[0][0], lft[0][1]);
    for (let i = 1; i < n; i++) g.lineTo(lft[i][0], lft[i][1]);
    for (let i = n - 1; i >= 0; i--) g.lineTo(rgt[i][0], rgt[i][1]);
    g.closePath(); g.fill();
  }
  // how it was taken, as its own outcome judged it: taken to heart, resented, or passed without a judgment
  const pushHow = (P) => (P.p.accepted ? "seam" : P.p.resented ? "knot" : "quiet");
  // the marks: in the still layer once settled (`still`), in the moving layer while a new one grows in (its outcome just
  // shown): it heals in gold (taken to heart), sets as a dark knot (resented) or closes as a fine silver hairline
  function drawPushes(g, t, still) {
    const now = still ? G.now : vAge;
    const ws = clamp(Math.sqrt(G.ly.s), 1, 1.6), tp = (pts, n, w0, w1, col, dx, dy) => taper(g, pts, n, w0 * ws, w1 * ws, col, dx, dy);
    G.pushes.forEach((P) => {
      if (P.p.age > now + 1e-6) return;
      // a push growing in is drawn live; once grown it goes into the next still layer made, and stays live until that
      // layer is on screen (so it never blinks out between the two)
      const age = P.born ? t - P.born : 99, baked = !P.born || G.t >= P.born + 1.5;
      if (still !== baked) return;
      const how = pushHow(P), grow = easeOut(age / 0.9);
      g.save(); g.lineCap = "round"; g.lineJoin = "round";
      if (how === "knot") {
        // a dark knot: whorls of deep ink drawn tight in the river, the bands' ink lines bending round it as wood grain
        // bends round a knot in a plank
        const rx = (P.bot - P.top) * 0.2 * (1 + 0.6 * (1 - grow)), ry = rx * 0.72;
        g.lineWidth = 0.7; g.strokeStyle = `rgba(18,10,32,${(0.5 * grow).toFixed(3)})`;
        for (let j = 1; j <= 4; j++) {
          const y0 = edge(P.x, j), d = y0 - P.mid, sg = d < 0 ? -1 : 1, push = Math.max(0, rx * 1.5 - Math.abs(d) * 0.45) * grow;
          if (push < 0.3) continue;
          g.beginPath();
          for (let dx = -rx * 3.4; dx <= rx * 3.4 + 0.01; dx += 1.5) { const x = P.x + dx; g[dx === -rx * 3.4 ? "moveTo" : "lineTo"](x, edge(x, j) + sg * push * Math.exp(-((dx / (rx * 1.5)) ** 2))); }
          g.stroke();
        }
        g.translate(P.x, P.mid); g.rotate(P.rot * 0.2);
        const halo = g.createRadialGradient(0, 0, 0, 0, 0, rx * 2.2); halo.addColorStop(0, "rgba(22,12,40,0.55)"); halo.addColorStop(1, "rgba(22,12,40,0)");
        g.fillStyle = halo; g.beginPath(); g.ellipse(0, 0, rx * 2.2, ry * 2.4, 0, 0, Math.PI * 2); g.fill();
        g.lineWidth = 0.9;
        for (let i = 3; i >= 1; i--) { g.strokeStyle = `rgba(30,18,52,${0.55 + 0.12 * (3 - i)})`; g.beginPath(); g.ellipse(0.4 * i, 0, rx * (0.35 + 0.3 * i), ry * (0.35 + 0.3 * i), 0.2 * i, 0.3, Math.PI * 2 - 0.2); g.stroke(); }
        g.fillStyle = "rgba(26,14,44,0.95)"; g.beginPath(); g.ellipse(0, 0, rx * 0.42, ry * 0.42, 0, 0, Math.PI * 2); g.fill();
        g.strokeStyle = "rgba(187,160,208,0.35)"; g.lineWidth = 0.5; g.beginPath(); g.ellipse(-rx * 0.1, -ry * 0.12, rx * 0.25, ry * 0.2, 0, Math.PI, Math.PI * 1.8); g.stroke();
        g.restore();
        return;
      }
      const n = Math.max(2, Math.round(P.pts.length * grow)), whole = grow >= 0.999;
      if (how === "seam") {
        // kintsugi: a dark gold bed, the gold itself tapering from the surface down, and a fine highlight up and left
        tp(P.pts, n, 2.6, 0.8, "rgba(8,5,16,0.36)", 0, 0.3);
        tp(P.pts, n, 2.3, 0.7, rgba(GOLDD, 0.92), 0, 0);
        tp(P.pts, n, 1.7, 0.4, "rgba(228,190,104,0.96)", 0, 0);
        if (whole) P.br.forEach((b) => { tp(b, b.length, 1.4, 0.3, rgba(GOLDD, 0.85), 0, 0); tp(b, b.length, 0.9, 0.2, "rgba(228,190,104,0.95)", 0, 0); });
        tp(P.pts, n, 0.45, 0.25, "rgba(255,244,212,0.75)", -0.4, -0.4);
      } else {
        // passed without a judgment: a healed hairline of silver, soft as if a little blurred
        tp(P.pts, n, 1.8, 1.0, "rgba(214,214,232,0.09)", 0, 0);
        tp(P.pts, n, 0.7, 0.45, "rgba(236,236,246,0.3)", 0, 0);
        if (whole) P.br.forEach((b) => tp(b, b.length, 0.55, 0.2, "rgba(236,236,246,0.18)", 0, 0));
      }
      if (P.born && age < 1.4) { const f = 1 - age / 1.4, s = (P.bot - P.top) * 1.2; g.globalCompositeOperation = "lighter"; g.globalAlpha = f * 0.9; g.drawImage(how === "seam" ? TX.gold : TX.lilac, P.x - s / 2, P.mid - s / 2, s, s); }
      g.restore();
    });
  }
  // a push that has finished growing in is baked into the still layer
  function settlePushes(t) {
    let done = false;
    born.forEach((b, p) => { if (t - b >= 1.5) { born.delete(p); done = true; } });
    if (done) restale();
  }

  /* ---------- the moving layer ---------- */
  // the current inside the river: two streak layers flowing downstream (toward now), faster while the ink is wet
  function drawFlow(g, t) {
    const R = G.rv; if (!R) return;
    const { ly } = G, th = ly.maxT * 1.15, y = ly.mid - th / 2, tw = 300 * Math.max(0.8, ly.s), v = 9 + 20 * wetV, xr = Math.min(R.x1, V.vnx);
    g.save(); g.clip(R.outline);
    const tile = (img, speed, al, op, dy) => {
      g.globalAlpha = al; g.globalCompositeOperation = op;
      let x = R.x0 - tw + ((t * speed) % tw);
      for (; x < xr; x += tw) g.drawImage(img, x, y + dy, tw, th);
    };
    tile(TX.flowD, v * 0.62, 0.2, "source-over", th * 0.05);
    tile(TX.flowL, v, 0.3, "lighter", 0);
    g.restore();
    // wet ink near now: the newest stretch blooms and bleeds past its edges, breathing slowly (the soft copy of the
    // bands, kept only near now, laid over the crisp ones)
    if (wetV > 0.02 && G.wetMask) {
      const br = off() ? 1 : 0.8 + 0.2 * Math.sin(t * 1.3), sx0 = Math.max(0, Math.floor((V.vnx - G.wetW - 8) / 4)), sx1 = Math.min(G.bN.width, Math.ceil((V.vnx + 14) / 4));
      if (sx1 > sx0) { g.save(); g.globalAlpha = clamp(wetV * 0.9 * br); g.drawImage(G.bN, sx0, 0, sx1 - sx0, G.bN.height, sx0 * 4, 0, (sx1 - sx0) * 4, G.bN.height * 4); g.restore(); }
    }
  }
  // the fog: two veils of slow billows drifting toward the present (back and front), feathered into the river at now
  function drawFog(g, t, front) {
    const { W, H } = G, nx = fogFrom(V.D), fx0 = Math.max(0, nx - (G.ly.sm ? 14 : 56)), bw = Math.max(1, Math.ceil((W - fx0) / 2)), bh = Math.max(1, Math.ceil(H / 2));
    const buf = front ? fogF : fogB;
    if (buf.width !== bw || buf.height !== bh) { buf.width = bw; buf.height = bh; }
    const f = buf.getContext("2d");
    f.globalCompositeOperation = "source-over"; f.globalAlpha = 1; f.clearRect(0, 0, bw, bh);
    const tileH = bh * (front ? 1.25 : 1.7), tileW = tileH * 4;
    const layer = (speed, dy, al, flip) => {
      f.globalAlpha = al;
      let x = -(((t * speed) % tileW) + tileW) % tileW;
      for (; x < bw; x += tileW) {
        if (flip) { f.save(); f.translate(0, bh); f.scale(1, -1); f.drawImage(TX.fog, x, dy, tileW, tileH); f.restore(); }
        else f.drawImage(TX.fog, x, dy, tileW, tileH);
      }
    };
    if (front) layer(3.4, -bh * 0.05, 0.75, true);
    else { layer(1.4, -bh * 0.35, 1, false); layer(2.2, -bh * 0.2, 0.55, true); }
    // feather: none at now, full a little way into the fog
    f.globalCompositeOperation = "destination-in"; f.globalAlpha = 1;
    const fe = f.createLinearGradient(0, 0, Math.min(80, Math.max(16, bw * 0.4)), 0); soft(fe, 0, 1, "0,0,0", 0, 1);
    f.fillStyle = fe; f.fillRect(0, 0, bw, bh);
    g.save(); g.globalAlpha = (front ? 0.42 : 0.8) * fogV; g.drawImage(buf, fx0, 0, bw * 2, bh * 2); g.restore();
  }
  // a few stars behind the fog, fixed to the far edge so the fog uncovers the same sky as the life moves on
  let starKey = "", stars = [];
  function drawStars(g, t) {
    const { W, H } = G, nx = fogFrom(V.D), key = W + "x" + H;
    if (key !== starKey) {
      starKey = key; const r = CH.rng(20261007), n = Math.round((W * H) / 2600);
      stars = Array.from({ length: n }, () => ({ x: W - r() * W, y: 4 + r() * (H - 26), s: 0.35 + Math.pow(r(), 3) * 1.1, a: 0.25 + r() * 0.55, f: 0.3 + r() * 1.2, p: r() * 6.3, c: r() < 0.14 ? CS[Math.floor(r() * 5)] : null, spark: r() < 0.06 }));
    }
    stars.forEach((s) => {
      const ramp = clamp((s.x - nx - 20) / 80); if (ramp <= 0) return;
      const al = s.a * ramp * fogV * (0.6 + 0.4 * Math.sin(t * s.f + s.p));
      if (s.spark) {   // a four-pointed spark, flaring now and then
        const e = Math.pow(Math.max(0, Math.sin(t * 0.21 + s.p)), 8) * ramp * fogV; if (e < 0.02) return;
        const z = 9 * e + 2; g.save(); g.globalAlpha = e; g.globalCompositeOperation = "lighter"; g.drawImage(TX.star, s.x - z, s.y - z, z * 2, z * 2); g.restore(); return;
      }
      g.fillStyle = s.c ? rgba(RGB.bright[s.c], al) : `rgba(236,230,255,${al.toFixed(3)})`;
      g.beginPath(); g.arc(s.x, s.y, s.s, 0, Math.PI * 2); g.fill();
    });
  }
  // the gleam at now: a soft column of gold, the bright meniscus where the river meets the fog, a slow four-pointed glint
  function drawGleam(g, t) {
    const R = G.rv; if (!R) return;
    const { ly } = G, nx = V.dnx, top = edge(V.vnx, 0), bot = edge(V.vnx, 5), br = off() ? 1 : 0.86 + 0.14 * Math.sin(t * 1.7), over = V.D.over;
    g.save(); g.globalCompositeOperation = "lighter";
    const bh = (bot - top) + ly.maxT * 0.9, bw = 20 * Math.min(1.5, ly.s);
    g.globalAlpha = (over ? 0.3 : 0.55) * br; g.drawImage(TX.beam, nx - bw / 2, ly.mid - bh / 2, bw, bh);
    if (!over) {
      g.globalAlpha = 0.9; g.strokeStyle = "rgba(255,244,214,0.9)"; g.lineWidth = 1.1; g.beginPath(); g.moveTo(nx, top - 1); g.lineTo(nx, bot + 1); g.stroke();
      g.strokeStyle = "rgba(244,223,166,0.25)"; g.lineWidth = 0.7; g.beginPath(); g.moveTo(nx, bot + 1); g.lineTo(nx, ly.bandY); g.stroke();
    }
    const z = (over ? 7 : 9) * Math.min(1.5, ly.s) * (off() ? 1 : 0.92 + 0.08 * Math.sin(t * 2.3)), rot = t * 0.25;
    g.globalAlpha = 0.95; g.translate(nx, ly.mid); g.rotate(rot); g.drawImage(TX.star, -z, -z, z * 2, z * 2);
    g.restore();
  }
  /* the source: before any year is lived the river is a point of light where it will begin, a white-gold bead in a
     soft halo of all five colours, each as strong as the others (every colour is even at birth, as the game starts
     every life), breathing over three seconds, with a faint dashed course running on into the fog. Through the first
     year it fades as the river grows out of it. */
  function sourceOf() {
    if (!V || V.D.over || vAge >= 1) return null;
    const ly = G.ly, a = 1 - sstep(0.05, 1, vAge), hs = clamp(ly.maxT / 45, 0.6, 1.4);
    return { x: V.D.sc.x0 + 10 * hs * a, y: ly.mid, a, hs };
  }
  function drawSource(g, t) {
    const P = sourceOf(); if (!P || P.a <= 0.01) return;
    const { x, y, a, hs } = P, br = off() ? 0 : Math.sin((t * Math.PI * 2) / 3), R = 26 * hs * (1 + 0.07 * br);
    g.save(); g.globalCompositeOperation = "lighter";
    // the course ahead: a faint dashed line along the river's middle, fading into the fog, drifting slowly outward
    // (it stops short of the first door, so it leads toward all five, not into one colour's)
    const d0 = (V.D.doors || [])[0], stopAt = d0 ? d0.x - d0.w * 1.4 - x : G.W * 0.3;
    if (vAge <= 0.05 && stopAt > 40) {
      const len = Math.min(stopAt, 380 * hs), cg = g.createLinearGradient(x + 8, 0, x + len, 0);
      cg.addColorStop(0, `rgba(244,223,166,${(0.3 * a).toFixed(3)})`); cg.addColorStop(1, "rgba(214,205,245,0)");
      g.strokeStyle = cg; g.lineWidth = 0.8; g.setLineDash([2, 6]); g.lineDashOffset = -t * 4;
      g.beginPath(); g.moveTo(x + 8, y); g.lineTo(x + len, y); g.stroke(); g.setLineDash([]); g.lineDashOffset = 0;
    }
    // the five colours' halo: one soft glow each, set a few pixels toward its place on the pie (W above, then U, B, R,
    // G round the circle, turning very slowly), so the rim shows each colour and the middle runs white
    CS.forEach((c, i) => {
      const ang = -Math.PI / 2 + (i * Math.PI * 2) / 5 + t * 0.08, ox = x + Math.cos(ang) * 7 * hs, oy = y + Math.sin(ang) * 7 * hs;
      const hg = g.createRadialGradient(ox, oy, 0, ox, oy, R);
      hg.addColorStop(0, rgba(BAND[c], 0.35 * a * (0.88 + 0.12 * br))); hg.addColorStop(0.4, rgba(BAND[c], 0.16 * a)); hg.addColorStop(1, rgba(BAND[c], 0));
      g.fillStyle = hg; g.beginPath(); g.arc(ox, oy, R, 0, Math.PI * 2); g.fill();
    });
    // the bead: white-gold, about 6 px across
    g.globalCompositeOperation = "source-over";
    const bg = g.createRadialGradient(x, y, 0, x, y, 3.4 * hs);
    bg.addColorStop(0, `rgba(255,252,240,${a.toFixed(3)})`); bg.addColorStop(0.55, `rgba(248,232,186,${(0.95 * a).toFixed(3)})`); bg.addColorStop(1, "rgba(244,223,166,0)");
    g.fillStyle = bg; g.beginPath(); g.arc(x, y, 3.4 * hs, 0, Math.PI * 2); g.fill();
    g.restore();
  }
  // light along the threads: now and then a glint travels an open line toward now; after an outcome, light runs along
  // every thread it touched
  function drawThreadLight(g, t) {
    if (!G.threads.length) return;
    g.save(); g.globalCompositeOperation = "lighter";
    const run = (T, u, al, len) => {
      const pts = T.pts, n = pts.length, i = Math.min(n - 1, Math.floor(u * (n - 1)));
      for (let k = 0; k < len && i - k > 0; k++) { const a = pts[i - k], b = pts[i - k - 1]; g.strokeStyle = `rgba(255,242,205,${(al * (1 - k / len)).toFixed(3)})`; g.lineWidth = 1.4; g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke(); }
      const p = pts[i], s = 7 * al * Math.min(1.4, G.ly.s); g.globalAlpha = 1; g.drawImage(TX.gold, p[0] - s, p[1] - s, s * 2, s * 2);
    };
    const shown = (T) => knows(T.t.seenW, vAge);
    if (!off()) G.threads.forEach((T, j) => {
      if (T.closed || T.span < 30 || !shown(T)) return;
      const per = 11 + (j % 5) * 2.3, ph = ((t + j * 3.7) % per) / per;
      if (ph < 0.3) run(T, easeIO(ph / 0.3), 0.45 * Math.sin((ph / 0.3) * Math.PI), Math.ceil(10 / 2.5));
    });
    // an outcome: each thread it touched lights up along its whole length in its own colours (quick to rise, slow to
    // fade), while a bright head runs from where the line began to now and flares there. With motion off the lines
    // simply stand lit for a moment, with no head.
    const w = Math.min(1.4, G.ly.s);
    for (let q = pulses.length - 1; q >= 0; q--) {
      const P = pulses[q], e = (t - P.t0) / P.dur, still = P.still;
      if (still ? performance.now() - P.ms >= P.dur * 1700 : e >= 1.7) { pulses.splice(q, 1); dirty = true; continue; }
      const env = still ? 1 : e < 0.12 ? easeOut(e / 0.12) : clamp(1 - (e - 0.12) / 1.58) ** 1.4;
      G.threads.forEach((T) => {
        if (!P.keys.has(T.t) || !shown(T)) return;
        // a soft glow added on, then the line itself laid over in its own clear colours (so it lights, not bleaches)
        g.globalAlpha = env * 0.2; strand(g, T.pts, T.t.cols, 1, 3.6 * w, null);
        g.globalCompositeOperation = "source-over"; g.globalAlpha = env * 0.9; strand(g, T.pts, T.t.cols, 1, 1.2 * w, null);
        g.globalCompositeOperation = "lighter"; g.globalAlpha = 1;
        if (still) return;
        if (e <= 1) run(T, easeIO(e), 0.95, Math.ceil(56 / 2.5));
        else if (e < 1.5) { const f = 1 - (e - 1) / 0.5, p = T.pts[T.pts.length - 1], z = 13 * w * (0.6 + 0.4 * f); g.globalAlpha = f; g.drawImage(TX.gold, p[0] - z, p[1] - z, z * 2, z * 2); g.globalAlpha = 1; }
      });
      if (!still) dirty = true;
    }
    g.restore();
  }
  // the hovered thread, bright over the others
  function drawHover(g) {
    if (!hover || !hover.T) return;
    const T = hover.T; g.save(); g.lineCap = "round"; g.lineJoin = "round";
    g.shadowColor = "rgba(244,223,166,0.6)"; g.shadowBlur = 6; strand(g, T.pts, T.t.cols, 1, 1.6, null); g.restore();
  }

  /* ---------- C4: the current ---------- */
  // streaks of each band's colour carried downstream toward now; past now they spill into the fog and fade. At a moment
  // the flow slows and parts round now (a clear eye opens there); their own picks of the last years float on it as
  // small lights. Calm motion: fewer of them.
  const FLECKS = () => Math.round((G.ly.sm ? 26 : 48) * (CH.motion() === "calm" ? 0.4 : 1) * G.rv.fill);
  function part(f, R, c) {   // the flow parting round now while a moment waits
    const rr = G.ly.maxT * 0.75, dx = f.x - V.vnx, dy = f.y - G.ly.mid, d = Math.hypot(dx * 0.6, dy);
    if (d < rr) f.y = clamp(f.y + Math.sign(dy || 1) * (rr - d) * 1.1 * partV, R.tab[c * 6] + 0.8, R.tab[c * 6 + 5] - 0.8);
  }
  function stepFlecks(dt, t) {
    if (!G || !G.rv || V.D.over) { flecks.length = 0; return; }
    const want = livingV > 0.01 && !off() ? FLECKS() : 0, sp = CH.speed() * slowV, R = G.rv, mid = G.ly.mid, nx = V.vnx;
    while (flecks.length < want) {
      const r = rnd();   // decoration only: where a fleck is born does not read the data
      flecks.push({ k: Math.floor(rnd() * 5), u: 0.15 + rnd() * 0.7, x: R.x0 + r * (nx - R.x0), v: 22 + rnd() * 30, a: 0, life: 1, spill: false, vx: 0, vy: 0, y: 0, ph: rnd() * 6.3, sz: 0.8 + rnd() * 0.7 });
    }
    if (flecks.length > want) flecks.length = Math.max(want, flecks.length - 2);
    for (const f of flecks) {
      if (!f.spill) {
        f.x += f.v * sp * dt;
        const c = Math.max(0, Math.min(R.nc - 1, Math.round(f.x) - R.c0)), a = R.tab[c * 6 + f.k], b = R.tab[c * 6 + f.k + 1];
        f.y = a + (b - a) * f.u + Math.sin(t * 1.3 + f.ph) * 0.5;
        if (partV > 0.01) part(f, R, c);
        f.a = Math.min(1, f.a + dt * 2);
        if (f.x >= nx) { f.spill = true; f.vx = f.v * 0.7; f.vy = (f.y - mid) * 0.5 + (rnd() - 0.5) * 10; }
      } else {
        f.x += f.vx * sp * dt; f.y += f.vy * sp * dt; f.vx *= Math.pow(0.55, dt); f.vy *= Math.pow(0.7, dt); f.life -= dt * 0.75 * Math.max(0.3, sp);
        if (f.life <= 0) { f.spill = false; f.life = 1; f.a = 0; f.x = R.x0 + rnd() * Math.min(120, nx - R.x0); }
      }
    }
  }
  // with motion off, the current is one still frame: a seeded scatter of streaks along the bands (the same every time
  // for the same state), parted round now while a moment waits
  function stillFlecks() {
    flecks.length = 0;
    if (!G || !G.rv || V.D.over || livingV < 0.01) return;
    const R = G.rv, r = CH.rng(38), n = Math.round(FLECKS() * 0.7);
    for (let i = 0; i < n; i++) {
      const k = Math.floor(r() * 5), u = 0.15 + r() * 0.7, x = R.x0 + 6 + r() * Math.max(1, V.vnx - R.x0 - 10);
      const c = Math.max(0, Math.min(R.nc - 1, Math.round(x) - R.c0)), a = R.tab[c * 6 + k], b = R.tab[c * 6 + k + 1];
      const f = { k, u, x, y: a + (b - a) * u, v: 22 + r() * 30, a: 1, life: 1, spill: false, vx: 0, vy: 0, ph: r() * 6.3, sz: 0.8 + r() * 0.7 };
      if (partV > 0.01) part(f, R, c);
      flecks.push(f);
    }
  }
  const fogVisFor = (f) => (f.spill ? clamp(1 - (f.x - V.vnx) / 160) : 1);
  function drawFlecks(g, t) {
    if (!flecks.length && livingV < 0.01) return;
    const s = Math.min(1.4, G.ly.s), dryX = V.vnx - (G.wetW || 0), rr2 = G.ly.maxT * 0.75;
    g.save();
    for (const f of flecks) {
      const c = CS[f.k];
      let al = f.a * (f.spill ? f.life * 0.6 : 0.7) * livingV * fogVisFor(f) * (!f.spill && f.x < dryX ? 0.5 : 1);
      // the clear eye at now while a moment waits: the streaks there dim
      if (partV > 0.01 && !f.spill && Math.hypot((f.x - V.vnx) * 0.6, f.y - G.ly.mid) < rr2) al *= 1 - 0.6 * partV;
      if (al < 0.02) continue;
      const h = 2.4 * f.sz * s * (f.spill ? 1 + (1 - f.life) * 1.2 : 1), len = h * (f.spill ? 2.2 : 3 + f.v / 22);
      // on the bands the pale ink is laid over (the same on every colour); spilled into the fog it glows
      g.globalCompositeOperation = f.spill ? "lighter" : "source-over"; g.globalAlpha = al;
      g.drawImage(TX.streak[c], f.x - len / 2, f.y - h / 2, len, h);
    }
    // their own picks of the last twelve years, floating on the current as small lights
    g.globalCompositeOperation = "lighter";
    const now = vAge;
    if (!V.D.over) for (const p of I.picks) {
      if (p.a < now - 12 || !knows(p.w, now)) continue;
      const rec = 1 - (now - p.a) / 12, x = G.X(p.a) + Math.sin(t * 0.4 + p.a) * 1.5, rng = (Math.sin(p.a * 91.7) + 1) / 2, y = G.ly.mid + (rng - 0.5) * G.ly.maxT * 0.5 + Math.sin(t * 0.9 + p.a * 3) * 1.2;
      const z = 4.5 * s; g.globalAlpha = livingV * rec * 0.85;
      g.drawImage(TX.dot[p.cols[0] || "W"], x - z, y - z, z * 2, z * 2);
      g.globalAlpha = livingV * rec * 0.6; g.drawImage(TX.gold, x - z * 0.5, y - z * 0.5, z, z);
    }
    g.restore();
  }
  // a moment's one ripple: rings of warm light spreading out on the water from now (kept on the water), easing out
  function drawRipple(g, t) {
    if (rippleT < 0) return;
    const e0 = (t - rippleT) / 1.8; if (e0 > 1.25) { rippleT = -1; dirty = true; return; }
    if (!G.rv) return;
    const cx = V.vnx, cy = G.ly.mid, R0 = G.ly.maxT * 0.9;
    // one soft swell of light on the water, spreading back from now inside the river (and only there): a ring of warm
    // light with no hard line, a fainter one after it
    g.save();
    const clip = new Path2D(); clip.rect(G.rv.x0, 0, cx - G.rv.x0, G.H);
    g.clip(clip); g.clip(G.rv.outline);
    g.globalCompositeOperation = "lighter";
    for (let i = 0; i < 2; i++) {
      const e = e0 - i * 0.25; if (e <= 0 || e >= 1) continue;
      const rx = 3 + easeOut(e) * R0 * (1 - i * 0.2), out = rx * 1.25, al = (i ? 0.26 : 0.44) * (1 - easeOut(e));
      g.save(); g.translate(cx, cy); g.scale(1 / V.s, 0.35);
      const rg = g.createRadialGradient(0, 0, 0, 0, 0, out), pk = rx / out;
      rg.addColorStop(0, "rgba(255,236,190,0)"); rg.addColorStop(pk * 0.72, "rgba(255,236,190,0)");
      rg.addColorStop(pk, `rgba(255,236,190,${al.toFixed(3)})`); rg.addColorStop(1, "rgba(255,236,190,0)");
      g.fillStyle = rg; g.fillRect(-out, -out, out * 2, out * 2); g.restore();
    }
    g.restore();
    dirty = true;
  }

  /* ---------- the frame ---------- */
  function frame(now, dt) {
    const t0 = performance.now();
    try { step(dt); } finally { charge(performance.now() - t0); }
  }
  function step(dt) {
    if (!S || !I) return;
    const snap = off(), calm = CH.motion() === "calm";
    mt += dt * CH.speed();
    tNow = mt;
    fc++;
    // ease toward the asked state (an exponential ease: fast at first, settling softly, about 400 ms); the age settles
    // its last few thousandths of a year at once (well under a pixel), the ink's wetness its last hundredth. Forward, the
    // age shown runs at most to the end of the layer on hand: the next layer is made while it waits, a step at a time,
    // so no frame makes a whole layer at once.
    const k = 1 - Math.exp(-dt * 7.5);
    const ease = (v, tg, eps = 1e-4) => (snap ? tg : Math.abs(tg - v) < eps ? tg : v + (tg - v) * k);
    const tE = !snap && G && !rebuild && tAge > G.now ? Math.max(G.now, Math.min(vAge, tAge)) : tAge;
    vAge = ease(vAge, tE, 0.004);
    const wT = S.wet || 0; wetV = ease(wetV, wT, 0.01);
    const fT = vAge >= I.end - 0.01 ? 0 : 1;
    if (snap) fogV = fT; else if (fogV !== fT) { const nF = fogV + (fT - fogV) * (1 - Math.exp(-dt * 1.8)); fogV = Math.abs(nF - fT) < 2e-3 ? fT : nF; dirty = true; }
    const td = S.doors || [0, 0, 0, 0, 0]; if (!doorsV) doorsV = td.slice();
    doorsV = doorsV.map((v, i) => { const n = ease(v, td[i]); if (n !== v) dirty = true; return n; });
    // the current shows while time runs; while a moment waits it stays, slowed and parted, at a little over half
    const lT = living ? 1 : partT >= 0 ? 0.6 : 0;
    livingV = snap ? lT : livingV + (lT - livingV) * (1 - Math.exp(-dt * (lT > livingV ? 2.5 : 0.9)));
    const partTarget = partT >= 0 && !living ? 1 : 0; partV = snap ? partTarget : partV + (partTarget - partV) * (1 - Math.exp(-dt * 3));
    slowV = 1 - 0.85 * partV;
    settlePushes(mt);
    const hd = hover && hover.door != null ? hover.door : -1; if (hd !== fogHover) { fogHover = hd; fogDirty = true; }
    // which layers this frame draws: the fog one frame in three (calm: one in six; its veils drift a few pixels a
    // second), the live layer every frame (calm: every other); a step of the next still layer only on a frame without
    // the fog (calm: nor the live layer), so the costs do not pile up on one frame
    const fogDue = snap || fogDirty || fc % (calm ? 6 : 3) === 1, liveDue = snap || !calm || fc % 2 === 0;
    const buildOK = !fogDue && (!calm || fc % 2 === 1);
    // the still layer: drawn exactly once everything has settled; while the age eases, a cache of the lived years up to
    // the newest age (cacheAge), made again as the life moves on. Both are built a step at a time in the second canvas
    // while the layer on screen stands in.
    const sized = !!G && G.cw === cv.width && G.ch === cv.height && G.W === cv._w && G.H === cv._h;
    const settled = vAge === tAge && wetV === wT && fogV === fT, tb = performance.now();
    if (!G || !sized || rebuild) {
      // nothing on hand stands in (the first frame, a new size, a new life, a load, motion changed): at once
      build(settled ? vAge : cacheAge(), settled); dirty = true;
    } else if (settled) {
      // a cache made for this very age, as wet and as foggy, is kept as it is: it is drawn as fully as an exact layer
      // (its small round things are set from its atlas, unstretched at a stretch of 1)
      const sk = stopKey(), need = stale || G.now !== vAge || (!G.exact && G.know < vAge - 1e-6) || G.wet !== wetV || G.fog !== fogV || G.sk !== sk;
      if (need) {
        if (snap || G.now < vAge - 1e-6 || (G.now === vAge && G.sk > sk)) build(vAge, true);
        else {
          if (!job || !job.exact || job.age !== vAge || job.wet !== wetV || job.fog !== fogV || job.sk !== sk) job = plan(vAge, true, statB, sctxB);
          if (job && buildOK && runSteps(job, 1.5)) swapIn(job);
        }
        dirty = true;
      }
    } else {
      if (job && job.exact) job = null;
      // while time runs a new stop comes every 280 ms or so: a new layer is begun at most every 400 ms (calm 800), and
      // the age shown waits at the end of the one on hand meanwhile
      const fwd = tAge > vAge, target = cacheAge(), tn = performance.now();
      if (!job && (stale || (fwd && G.now < target - 1e-6) || (!fwd && viewOf().s > 1.8)) && (!living || tn - planAt >= (calm ? 800 : 400))) {
        job = plan(target, false, statB, sctxB); planAt = tn; }
      // a layer made before the newest stop is still newer than the one on screen: it is finished and shown, and the
      // next one follows (dropping it would starve the river while the stops come faster than a layer is made)
      waitN = job && fwd && vAge >= G.now - 1e-6 ? waitN + 1 : 0;
      if (job && (buildOK || waitN > 6) && runSteps(job, 1.5)) swapIn(job);
      dirty = true;
    }
    costOf(job || G.now !== vAge || stillKey === "" ? "build" : "idle", tb);
    V = G ? (G.exact && G.now === vAge ? { s: 1, vnx: G.nx, dnx: G.nx, D: G, cache: false, x0: G.sc.x0 } : viewOf()) : null;
    if (!G || !V) return;
    if (snap && !dirty) return;
    dirty = false;   // cleared before drawing, so anything that asks for another frame while drawing keeps its ask
    if (!snap) stepFlecks(Math.min(dt, 0.05), mt); else stillFlecks();
    render(mt, snap, fogDue, liveDue);
  }
  function render(t, all, fogDue, liveDue) {
    const key = V.cache ? `${gid}|${V.s}|${V.vnx}|${V.dnx}` : `${gid}`;
    let t0 = performance.now();
    if (all || key !== stillKey) { stillKey = key; renderStill(); costOf("still", t0); t0 = performance.now(); }
    if (all || fogDue) { fogDirty = false; renderFog(t); costOf("fog", t0); t0 = performance.now(); }
    if (all || liveDue) { renderLive(t); costOf("live", t0); }
  }
  // the lived years: the layer on hand, or while the age eases its slice up to now stretched to the age shown, with
  // its small round things set unstretched each at its place in the years shown
  function renderStill() {
    const k = G.k, s = V.s, x0 = G.sc.x0;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
    ctx.clearRect(0, 0, cv.width, cv.height);
    if (!V.cache) { ctx.drawImage(stat, 0, 0); return; }
    ctx.setTransform(k * s, 0, 0, k, k * x0 * (1 - s), 0);
    const sw = Math.min(stat.width, Math.ceil(V.vnx * k));
    if (sw > 0) ctx.drawImage(stat, 0, 0, sw, stat.height, 0, 0, sw / k, G.H);
    ctx.setTransform(k, 0, 0, k, 0, 0);
    // the cache's threads and ground run on past now: there they fade into it, as they do once settled
    fadeOut(ctx, V.dnx - 18, V.dnx + 0.5, 0, edge(V.vnx, 0) - 1, 0.92);
    fadeOut(ctx, V.dnx - (G.ly.sm ? 14 : 28), V.dnx + 0.5, G.ly.strTop - 2, G.ly.strBot + 2, 1);
    const al = G.atlas ? G.atlas.list : [];
    for (let i = 0; i < al.length; i++) {
      const [sx, sy, hw, up, dn, ax, ay] = al[i]; if (sx > V.vnx + 0.5) continue;
      const a = Math.floor((ax - hw) * k), b = Math.ceil((ax + hw) * k), t0 = Math.floor((ay - up) * k), t1 = Math.ceil((ay + dn) * k);
      ctx.drawImage(gly, a, t0, b - a, t1 - t0, x0 + (sx - x0) * s + (a / k - ax), sy + (t0 / k - ay), (b - a) / k, (t1 - t0) / k);
    }
  }
  // the years ahead: the fog's darkness, the thread of who they are going on into it, the stars, the back veil, the
  // doors, the front veil
  let fogClear = false;
  function renderFog(t) {
    const g = fctx;
    if (fogV <= 0.01) { if (!fogClear) { g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, cvF.width, cvF.height); fogClear = true; } return; }
    fogClear = false;
    g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    g.clearRect(0, 0, cvF.width, cvF.height);
    g.setTransform(G.k, 0, 0, G.k, 0, 0);
    const D = V.cache ? V.D : G;
    drawFogBody(g, D); drawFogThread(g, D);
    drawStars(g, t); drawFog(g, t, false); drawDoors(g, t, D.doors || []); drawFog(g, t, true);
  }
  // what moves on the lived years and at now
  function renderLive(t) {
    const g = lctx, k = G.k, s = V.s, x0 = G.sc.x0, src = () => g.setTransform(k * s, 0, 0, k, k * x0 * (1 - s), 0), page = () => g.setTransform(k, 0, 0, k, 0, 0);
    g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    g.clearRect(0, 0, cvL.width, cvL.height);
    src(); g.save();
    if (V.cache) { g.beginPath(); g.rect(0, 0, V.vnx, G.H); g.clip(); }
    drawFlow(g, t);
    drawPushes(g, t, false);
    g.restore();
    drawFlecks(g, t);
    page(); drawGleam(g, t); drawSource(g, t);
    src(); g.save();
    if (V.cache) { g.beginPath(); g.rect(0, 0, V.vnx + 1, G.H); g.clip(); }
    drawThreadLight(g, t); drawHover(g);
    drawRipple(g, t);
    g.restore();
  }

  /* ---------- hover: what each mark means ----------
     Read at the age shown (vAge). While the age eases the pointer is turned into the cached layer's pixels first. The
     plain river and its band are the page's own reading (#lineHov, over them); everything else is read here. */
  function nearThread(x, y) {
    let best = null, bd = 4.5;
    (G.threads || []).forEach((T) => {
      if (!knows(T.t.seenW, vAge) || x < T.xs - 4 || x > T.xe + 4) return;
      for (let i = 0; i < T.pts.length; i += 1) { const d = Math.hypot(T.pts[i][0] - x, T.pts[i][1] - y); if (d < bd) { bd = d; best = T; } }
    });
    return best;
  }
  const pushAt = (sx, y) => (G.pushes || []).find((P) => knows(P.at, vAge) && Math.abs(sx - P.x) < 5 && y > P.top - 2 && y < P.bot + 2);
  function pushTip(P) {
    const h = pushHow(P);
    const how = h === "seam" ? "They came round to it: the mark healed in gold." : h === "knot" ? "They resented it: it set hard as a knot." : "They went along and said nothing: a fine seam.";
    return CH.tipBox(`The voice pushed at ${Math.floor(P.p.age)}`, "not their own pick", [], `<i>${CH.esc(P.p.act || "")}</i><br>${how}`);
  }
  // over the page's own hover area (the river and its band): only a seam, or a breakthrough or turn rising from it
  function markAt(x, y) {
    if (!G || !S || !V) return "";
    const sx = V.cache ? G.sc.x0 + (x - G.sc.x0) / V.s : x, ly = G.ly;
    for (const P of G.points || []) if (knows(P.p.w, vAge) && Math.abs(sx - P.x) < 5 && y < P.y + 2 && y > P.y - 14 * ly.s) return pointTip(P.p);
    const P = pushAt(sx, y);
    return P ? pushTip(P) : "";
  }
  const pointTip = (p) => CH.tipBox(p.type === "break" ? `${pips(p.cols)} A breakthrough at ${Math.floor(p.a)}` : `${p.from ? CH.pip(p.from) : ""} → ${p.to ? CH.pip(p.to) : ""} A turn at ${Math.floor(p.a)}`, "", [],
    CH.esc(cut(CH.plain(p.x.text), 200)));
  function hit(x, y) {
    const was = hover; hover = null;
    const html = read(x, y);
    if (was !== hover && !(was && hover && was.door === hover.door && was.T === hover.T)) dirty = true;
    shown = !!html;
    return html;
  }
  function read(x, y) {
    if (!G || !S || !V) return "";
    const now = vAge, nm = (CH.life && CH.life.name) || "They", x0 = G.sc.x0, sx = V.cache ? x0 + (x - x0) / V.s : x, upTo = V.vnx + 1, ly = G.ly;
    // the source, before the first year
    const src = sourceOf();
    if (src && src.a > 0.3 && Math.hypot(x - src.x, y - src.y) < 14 * src.hs)
      return CH.tipBox("Where the river begins", "", [], `${CH.esc(nm)}'s life starts here. Every colour is even and nothing is lived yet: the river grows out of this point as the years leave their marks.`);
    // the doors (in the fog, the page's own pixels)
    for (const d of (V.cache ? V.D.doors : G.doors) || []) {
      const D = doorShape(d);
      if (Math.abs(x - D.x) < Math.max(D.w * 0.8, 5) && y > D.top - 8 && y < D.base + 4) {
        const v = doorsV[d.i], about = !!(S.doorsAbout && S.doorsAbout[d.i]); hover = { door: d.i };
        return CH.tipBox(`${CH.pip(d.c)} ${NAME[d.c]}'s ways: ${doorWord(v)}`, doorSub(v, about), [],
          `How open ${NAME[d.c]}'s ways are to ${CH.esc(nm)} now (${DOOR_MEAN[d.c]}): what their world allows and what their means reach. The nearer and brighter the door, the easier a step that way.${about ? " At this age the game holds it steady at its last clear reading, so it is about right, not exact." : ""}`);
      }
    }
    if (sx <= upTo + 4) {
      // breakthroughs and turns
      for (const P of G.points || []) if (knows(P.p.w, now) && Math.abs(sx - P.x) < 5 && y < P.y + 2 && y > P.y - 14 * ly.s) return pointTip(P.p);
      // the threads: their start line, and their end line only once it is told
      const T = nearThread(sx, y);
      if (T) {
        hover = { T }; const t = T.t, closed = knows(t.k1W, now), a0 = Math.floor(t.a0), a1 = closed ? Math.floor(t.a1) : null;
        const head = t.type === "commit" ? KIND[t.kind] || CH.cap(t.kind) : t.type === "clash" ? `A quarrel with their ${CH.esc(t.kind)}` : KIND[t.kind] || "A story line";
        const how = !closed ? `since ${a0}, still going` : t.end === "gold" ? `from ${a0} to ${a1}, reached` : t.end === "loose" ? `from ${a0} to ${a1}, let go` : t.end === "fade" ? `from ${a0}, faded by ${a1}` : `from ${a0} to ${a1}, tied off`;
        const told = (x) => x && knows(wI(x), now);
        const beads = t.beads.filter((b) => told(b.x));
        const lines = [told(t.t0) && cut(CH.plain(t.t0.text), 220), ...beads.slice(-1).map((b) => cut(CH.plain(b.x.text), 160)), closed && told(t.t1) && t.t1 !== t.t0 && cut(CH.plain(t.t1.text), 220)].filter(Boolean);
        return CH.tipBox(`${t.cols.length ? pips(t.cols) + " " : ""}${CH.esc(head)}`, how, [], lines.map(CH.esc).join("<br><br>"));
      }
      // the pushes
      const P = pushAt(sx, y); if (P) return pushTip(P);
      // gems and seals
      for (const o of G.gems || []) {
        if (!knows(o.t === "gem" ? o.p.knownW : o.s.w, now)) continue;
        if (Math.abs(sx - o.x) > o.r + 1 + (V.cache ? 2 : 0) || Math.abs(y - o.y) > o.r + 1) continue;
        if (o.t === "seal") return CH.tipBox(`${pips(o.s.cols)} A plan reached at ${Math.floor(o.a)}`, "", [], CH.esc(cut(o.s.text, 200)));
        const p = o.p, told = p.ev.filter((e) => knows(e.w, now)), lost = (told[told.length - 1] || {}).lost ? told.filter((e) => e.lost).pop() : null;
        return CH.tipBox(CH.esc(CH.cap(p.say)), `${PERK_KIND[p.kind] || CH.esc(p.kind)}, since ${Math.floor(p.first)}${lost ? `, lost at ${Math.floor(lost.a)}` : ""}`,
          p.ways.length ? [["Opens ways", `${pips(p.ways)} ${names(p.ways)}`]] : [], lost ? "Its place stays in the ground, as an outline." : "Set into the ground the year it came.");
      }
      // the strata: what the title was called, as far as the story has told, and how long and how deeply
      for (const L of G.strata || []) {
        if (!knows(L.r.seenW, now) || sx < L.xs || sx > L.xe) continue;
        const c = L.P.find((p) => p[0] >= sx) || L.P[L.P.length - 1]; if (y < c[1] - 0.8 || y > c[2] + 0.8) continue;
        const r = L.r, smp = r.samples.filter((s) => knows(s.w, now)), last = smp[smp.length - 1] || r.samples[0], ended = knows(r.knownW, now);
        const held = (ended ? Math.min(r.end, now) : now) - r.start;
        const past = [...new Set(smp.flatMap((s) => s.named))];
        const title = (last && last.named[0]) || past[past.length - 1] || KIND[r.kind] || r.kind;
        const said = past.length > 1 ? past.slice(-4) : [];
        return CH.tipBox(CH.esc(CH.cap(title)), `${yrs(held)}, ${invWord(last ? last.inv : 0)}${ended ? ", now behind them" : ""}`,
          [["Invested", CH.pct(last ? last.inv : 0)], ["Expects", last && last.exp.length ? `${pips(last.exp)} ${names(last.exp)}` : "nothing in particular"]],
          `${said.length ? CH.esc(CH.cap(said.join(", then "))) + ". " : ""}A layer of ground they built under the life, as thick as they put into it.`);
      }
    }
    if (fogV > 0.5 && x > fogFrom(V.D) + 8) return CH.tipBox("The years ahead", "", [], "Unwritten. The doors stand as near and as bright as each colour's ways are open now; nothing ahead is shut for good.");
    return "";
  }
  // the readings go under the strip, as the line's own (04-line.js lnHoverShow), so they never cover the year read
  let shown = false;
  const under = () => { if (!shown || tipOwner !== "line" || tipEl.hidden) return; const b = lineEl.getBoundingClientRect().bottom; if (parseFloat(tipEl.style.top) < b) tipEl.style.top = b + 6 + "px"; };
  CH.canvasTip(cvL, hit);
  const leave = () => { shown = false; if (hover) { hover = null; dirty = true; } };
  const onMove = (e) => { if (e.pointerType === "mouse") under(); };
  const onUp = (e) => { if (e.pointerType !== "mouse") setTimeout(under, 0); };
  cvL.addEventListener("pointermove", onMove);
  cvL.addEventListener("pointerup", onUp);
  cvL.addEventListener("pointerleave", leave);
  /* over the page's own hover area: its reading of the year stands, unless the pointer is on a seam (or a breakthrough
     or turn), whose own reading then takes its place (the line's own listener runs first, on svg#river) */
  let over = null;
  function onLine(e) {
    if (e.pointerType !== "mouse") return;
    if (!e.target || e.target.id !== "lineHov") { over = null; return; }
    const [x, y] = CH.local(cvL, e), html = markAt(x, y);
    over = html ? { html, cx: e.clientX } : null;
    if (over) showOver();
  }
  function showOver() {
    if (!over || !lnHoverShow.at) return;
    const cross = document.getElementById("cross"); if (cross) cross.setAttribute("visibility", "hidden");
    showTipAt(over.html, over.cx, lineEl.getBoundingClientRect().bottom);
    const b = lineEl.getBoundingClientRect().bottom; if (parseFloat(tipEl.style.top) < b) tipEl.style.top = b + 6 + "px";
  }
  const offLine = () => { over = null; };
  lineEl.addEventListener("pointermove", onLine);
  lineEl.addEventListener("pointerleave", offLine);

  /* ---------- events ---------- */
  // a moment: the current parts and slows round now, and one ripple spreads from it (none with motion off, or quiet)
  function moment(quiet) { partT = tNow; rippleT = off() || quiet ? -1 : tNow; dirty = true; }
  function setLiving(v) { living = !!v; if (living) partT = -1; dirty = true; }
  // an outcome lights the threads it touched: the open lines that share the act's colours, and any line that began or
  // ended at this stop; a push it shows grows in. With motion off the lines stand lit for a moment, then a later still
  // frame puts them out, and the push is simply there.
  function outcome(res, quiet) {
    if (!res || !I) return;
    if (res.pushed) {
      const p = (CH.life.pushes || []).find((q) => q.age === res.age && q.title === res.title);
      if (p) { seenP.add(p); pend.delete(p); if (!quiet && !off()) born.set(p, tNow); restale(); }
    }
    if (quiet) return;
    // (read from the whole index, not the layer on screen: a line the outcome itself began is drawn once the layer
    // catches up with the outcome's stop, a frame or few later, and lights then)
    const cs = CH.lettersOf(res.colors), a = res.age != null ? res.age : vAge, keys = new Set();
    I.threads.forEach((t) => { if (t.seen > a + 0.05) return;
      const closedBy = t.k1 != null && t.k1 <= a - 0.05, open = !closedBy;
      if ((open && t.cols.some((c) => cs.includes(c))) || Math.abs(t.a0 - a) < 0.2 || (t.a1 != null && t.k1 <= a + 0.05 && Math.abs(t.a1 - a) < 0.2)) keys.add(t); });
    if (keys.size) { const P = { t0: tNow, ms: performance.now(), dur: off() ? 1.6 : 1.5, keys, still: off() }; pulses.push(P); if (P.still) later(P.dur * 1.7 * 1000 + 60); }
    dirty = true;
  }
  const subs = [
    CH.on("living", setLiving),
    CH.on("moment", (x) => moment(x && x.quiet)),
    CH.on("outcome", (x) => outcome(x && x.res, x && x.quiet)),
    CH.on("motion", () => { rebuild = true; dirty = true; }),
    CH.on("resize", () => { rebuild = true; dirty = true; }),
  ];
  // time may already be running when the river comes
  living = !!(busy && hud && hud.mode === "play" && hud.job === "run");
  const stop = CH.frame(frame, root);

  /* the page's line on top: the canvas stays first in #line (under svg#river), and the marks the page keeps that sit on
     the river's rows (its hover area, the year's cross, the candle at the end) move to the river's rows. Redone after
     each drawLine, which writes them again. */
  function align() {
    if (lineEl.firstChild !== root) lineEl.insertBefore(root, lineEl.firstChild);
    lineEl.classList.add("lv-river");
    const ly = layoutOf(Math.max(48, cv._h || lineEl.clientHeight)), y1 = ly.mid - ly.maxT / 2 - 3, y2 = ly.bandY + ly.bandH + 3;
    const hov = document.getElementById("lineHov"); if (hov) { hov.setAttribute("y", (y1 + 1).toFixed(1)); hov.setAttribute("height", (y2 - y1 - 1).toFixed(1)); }
    const cross = document.getElementById("cross"); if (cross) { cross.setAttribute("y1", y1.toFixed(1)); cross.setAttribute("y2", y2.toFixed(1)); }
    const end = riverEl.querySelector(".gl.end");
    if (end) { const c = end.querySelector("circle"), u = end.querySelector("use"), r = c ? +c.getAttribute("r") : 0;
      if (c) c.setAttribute("cy", ly.mid.toFixed(1)); if (u) u.setAttribute("y", (ly.mid - r * 0.68).toFixed(1)); }
    showOver();
  }
  align();

  return {
    update, align,
    destroy() {
      stop(); subs.forEach((u) => u()); timers.forEach(clearTimeout); timers.clear();
      lineEl.removeEventListener("pointermove", onLine); lineEl.removeEventListener("pointerleave", offLine);
      if (shown && tipOwner === "line") hideTip();
      root.remove(); lineEl.classList.remove("lv-river");
      scheduleLine();                       // the page's line draws its own rows again
    },
    // this piece's script per frame over the last frames (up to 1200): mean, 95th percentile and worst, in ms
    perf() {
      const n = Math.min(ringN, ring.length), xs = Array.from(ring.slice(0, n)).sort((p, q) => p - q);
      const by = {}; for (const k in parts) by[k] = { perFrame: n ? parts[k].ms / n : 0, n: parts[k].n, each: parts[k].ms / parts[k].n, max: parts[k].max };
      return { frames: n, mean: n ? xs.reduce((s, v) => s + v, 0) / n : 0, p95: n ? xs[Math.min(n - 1, Math.floor(n * 0.95))] : 0, max: n ? xs[n - 1] : 0, parts: by, reset() { ringN = 0; parts = {}; } };
    },
  };
}

/* ---------- the piece ---------- */
let inst = null;
CH.piece("river", {
  order: 30,
  mount() {
    if (typeof lnLayout !== "function" || typeof lnScale !== "function" || typeof lineEl === "undefined" || !lineEl) return false;
    try { inst = make(); } catch (e) { console.warn("living: the river did not start, the line stays", e); inst = null; }
    if (!inst) { const r = lineEl.querySelector(":scope > .rv"); if (r) r.remove(); lineEl.classList.remove("lv-river"); return false; }
    return true;
  },
  update(S, how) { if (inst) inst.update(S, how); },
  destroy() { if (inst) { const i = inst; inst = null; i.destroy(); } },
  perf() { return inst ? inst.perf() : null; },
  hooks: { drawLine() { if (inst) inst.align(); } },
});
})();
