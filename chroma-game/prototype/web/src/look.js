<script>
"use strict";
/* ---------------- the ink look (thread "Visual improvement", Emren 10-10 07:30 UTC: "Implement all six, I want more
   eye-candies, more animation, more visual upgrades that helps players and gameplay") ----------------
   A layer over app.js: it wraps a few of its functions and draws after them, so app.js itself is unchanged and the life is
   unchanged. Every part sits behind two settings in the Table menu: Look (ink or classic, the v22 look) and Motion (full,
   calm or off; the system's reduced-motion setting counts as off). A fault in this layer never stops the game: each part
   runs inside safe().
   1 one ink language: look.css (paper grain, engraved rules, ink roundels, stamped seals) on the story and the cards; the
     status panel keeps v22's minimal drawing, symbols in front and words on hover (Emren 10-10 09:01 UTC)
   2 living engravings: each picture prints in like a plate pulled from the press, its own lamps, windows and candles glow
     and flicker (light positions recorded from the kit's scene code, chroma-art/game/lights.json), and it drifts slowly
   3 colour you can see move: at an outcome the card turns, ink drops run from it into the colour wheel, the wheel moves when
     they land, and the meters and means count to their new values with the change floating beside them
   4 their own tarot card: a portrait card in the crest, on the character sheet and at the end, by lead colour and age
   5 chapter plates: a page turns for the big turns (taking over, a new identity, a long shot made, a title, the end)
   6 the life river as it was, lit like the fog: its glow breathes, light drifts and gleams along it, and its colors
     flow into their new place when the life moves on (Emren 10-10 09:01 UTC)
   and for play: odds read by colour at a glance, a storm corner on cards they would rather not do, and a small lean wheel
   on the moment's picture that shows which way the card under the mouse would pull them. */
(() => {
const LK_LIGHTS = __LIGHTS__;
const LK_PORT = PICS.portrait || null;
const root = document.documentElement;
const keep = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };
const read = (k, d) => { try { return localStorage.getItem(k) || d; } catch (_) { return d; } };
const safe = (f) => { try { return f(); } catch (e) { console.error("look:", e); } };
const MOTION = ["full", "calm", "off"], LOOK = ["ink", "classic"];
const MOTION_WORD = { full: "full", calm: "calm", off: "off" }, LOOK_WORD = { ink: "ink", classic: "classic" };
let motion = read("chroma.motion", "full"), look = read("chroma.look", "ink");
if (!MOTION.includes(motion)) motion = "full";
if (!LOOK.includes(look)) look = "ink";
const ink = () => look === "ink";
const moving = () => motion !== "off" && !reducedMotion();
const lively = () => motion === "full" && !reducedMotion();
const setRoot = () => { root.dataset.look = look; root.dataset.motion = reducedMotion() && motion !== "off" ? "off" : motion; };
setRoot();
try { matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", setRoot); } catch (_) {}
const now = () => performance.now();
// ink on paper, one colour per letter (the paper palette): anything drawn over parchment or flying over the page
const INK = { W: "#8f7116", U: "#1c5ca2", B: "#4e3966", R: "#b03c1d", G: "#22733e" };

/* ---------------- shared drawing: the hatch the lean wheel is filled with ---------------- */
const SVGNS = "http://www.w3.org/2000/svg";
const defs = document.createElementNS(SVGNS, "svg");
defs.setAttribute("class", "lk-defs"); defs.setAttribute("aria-hidden", "true"); defs.setAttribute("focusable", "false");
defs.innerHTML = `<defs>
  <pattern id="lk-xh2" width="3.4" height="3.4" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)"><path d="M0 0V3.4" style="stroke:#2a2116;stroke-opacity:.5;stroke-width:.8"/><path d="M0 1.7H3.4" style="stroke:#2a2116;stroke-opacity:.22;stroke-width:.6"/></pattern>
</defs>`;
document.body.appendChild(defs);

/* ---------------- 6: the life river as it was, lit like the fog, its colors flowing into place ---------------- */
// Emren 10-10 09:01 UTC (thread "Visuals for the game"): the HUD stays minimal (symbols in front, words on hover) and the
// life river stays as before, "with color and color transition update, with similar lighting of the fog, as majestic but
// not crowded as possible". So the river keeps v22's bands, glow and sheen; over it (ink look) only light moves: the glow
// breathes like the fog's edge, a slow nebula of light drifts along the lived years and a gleam runs from birth to now.
// When the life moves on, the old bands fade into the new ones.
// Each redraw keeps the loops in step with one clock, so the frequent redraws while weeks run never restart them.
let rvKey = "", rvGhost = null, rvGhostAt = 0;
const rvClock = (sec) => `${(-((performance.now() / 1000) % sec)).toFixed(2)}s`;
const _drawLine = drawLine;
drawLine = function () {
  const was = riverEl.querySelector("#lnLays"), oldLays = was ? was.innerHTML : "", oldW = lineGeo ? lineGeo.W : 0;
  _drawLine();
  safe(() => riverLight(oldLays, oldW));
};
function ghostRiver(oldLays) {
  if (!rvGhost || !rvGhost.isConnected) {
    rvGhost = document.createElementNS(SVGNS, "svg"); rvGhost.setAttribute("class", "lk-rvghost"); rvGhost.setAttribute("aria-hidden", "true");
    riverEl.after(rvGhost);
  }
  rvGhost.setAttribute("viewBox", riverEl.getAttribute("viewBox"));
  rvGhost.innerHTML = `<g>${oldLays.replace(/class="lay"/g, 'class="lk-gl"')}</g>`;
  rvGhost.classList.remove("go"); void rvGhost.getBoundingClientRect(); rvGhost.classList.add("go");
  rvGhostAt = performance.now();
}
function riverLight(oldLays, oldW) {
  if (rvGhost && (!ink() || !moving())) rvGhost.classList.remove("go");
  const G = lineGeo, sheen = riverEl.querySelector(".sheen"), lays = [...riverEl.querySelectorAll("#lnLays .lay")];
  if (!ink() || !G || !sheen || !lays.length) return;
  const vb = riverEl.viewBox.baseVal, H = vb.height, x0 = G.X(0), nx = G.X(G.now), span = Math.max(1, nx - x0);
  const key = G.R.length + ":" + (+G.now).toFixed(2);
  const grew = key !== rvKey && rvKey !== "" && oldLays && oldW === G.W;
  rvKey = key;
  let m = `<defs><clipPath id="lkRvClip">${lays.map((p) => `<path d="${p.getAttribute("d")}"/>`).join("")}</clipPath>` +
    `<linearGradient id="lkShimG"><stop offset="0" stop-color="#fff6dc" stop-opacity="0"/><stop offset="0.5" stop-color="#fff6dc" stop-opacity="0.42"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>` +
    `<radialGradient id="lkNebG"><stop offset="0" stop-color="#ece6ff" stop-opacity="0.34"/><stop offset="0.55" stop-color="#cbb8ff" stop-opacity="0.12"/><stop offset="1" stop-color="#cbb8ff" stop-opacity="0"/></radialGradient>` +
    `<radialGradient id="lkNebW"><stop offset="0" stop-color="#f4dfa6" stop-opacity="0.26"/><stop offset="1" stop-color="#f4dfa6" stop-opacity="0"/></radialGradient></defs>`;
  if (lively() && span > 24) {
    const sw = clamp(span * 0.16, 26, 140), nw = clamp(span * 0.3, 60, 260), mid = vb.height / 2;
    m += `<g class="lk-rvl" clip-path="url(#lkRvClip)" aria-hidden="true">` +
      `<ellipse class="lk-neb" cx="${(x0 + nw * 0.3).toFixed(1)}" cy="${mid.toFixed(1)}" rx="${(nw / 2).toFixed(1)}" ry="${(H * 0.55).toFixed(1)}" fill="url(#lkNebG)" style="--d:${(span - nw * 0.6).toFixed(1)}px;animation-delay:${rvClock(84)}"/>` +
      `<ellipse class="lk-neb w" cx="${(nx - nw * 0.3).toFixed(1)}" cy="${mid.toFixed(1)}" rx="${(nw * 0.4).toFixed(1)}" ry="${(H * 0.45).toFixed(1)}" fill="url(#lkNebW)" style="--d:${(-(span - nw * 0.6)).toFixed(1)}px;animation-delay:${rvClock(122)}"/>` +
      `<rect class="lk-shim" x="${(x0 - sw).toFixed(1)}" y="0" width="${sw.toFixed(1)}" height="${H.toFixed(1)}" fill="url(#lkShimG)" style="--d:${(span + sw).toFixed(1)}px;animation-delay:${rvClock(22)}"/></g>`;
  }
  const g = document.createElementNS(SVGNS, "g"); g.setAttribute("class", "lk-river"); g.innerHTML = m;
  sheen.after(g);
  // the colors flowing into place: the bands as they were, on a sheet of their own over the river (the river redraws every
  // few weeks while time runs), fade into the new ones; a run of redraws keeps one fade going, then starts the next
  if (grew && moving() && !(hud && hud.replay) && performance.now() - rvGhostAt > 700) ghostRiver(oldLays);
  riverEl.style.setProperty("--lk-c6", rvClock(12));
}

/* ---------------- 2: living engravings ---------------- */
// LK_LIGHTS: picture -> "x,y,d,kind,strength,colour|..." (x, y, d in thousandths of the picture; kind g glow, w window or
// screen, f flame or bulb, b beam; colour three hex digits or empty)
const LCACHE = new Map();
function lightsOf(src) {
  const m = /(?:^|\/)pics\/([^/?#]+)\.webp/.exec(src || ""); if (!m) return null;
  if (LCACHE.has(m[1])) return LCACHE.get(m[1]);
  const raw = LK_LIGHTS[m[1]];
  const out = raw ? raw.split("|").filter(Boolean).map((t) => { const [x, y, d, k, a, c] = t.split(","); return { x: x / 1000, y: y / 1000, d: d / 1000, k, a: a / 100, c }; }) : null;
  LCACHE.set(m[1], out); return out;
}
const rgbOf = (c) => /^[0-9a-f]{3}$/i.test(c || "") ? [...c].map((h) => parseInt(h + h, 16)).join(" ") : "";
function lightsHTML(list) {
  return list.map((l, n) => {
    const cls = l.k === "f" ? "flame" : l.k === "w" ? "win" : l.k === "b" ? "beam" : l.d < 0.07 ? "bulb" : "glow";
    const a = { flame: 0.55 + 0.35 * l.a, win: 0.34 + 0.3 * l.a, beam: 0.2 + 0.2 * l.a, bulb: 0.42 + 0.32 * l.a, glow: 0.18 + 0.24 * l.a }[cls];
    const t = { flame: 1.3 + (n % 4) * 0.37, bulb: 1.5 + (n % 7) * 0.31, win: 9 + (n % 6) * 2.3, beam: 5.5 + (n % 3) * 1.4, glow: 4.5 + (n % 5) * 1.2 }[cls];
    const rgb = rgbOf(l.c);
    return `<i class="${cls}" style="--a:${a.toFixed(2)};--t:${t.toFixed(2)}s;--dl:${(-((n * 0.61) % 4)).toFixed(2)}s${rgb ? `;--lc:${rgb}` : ""}"></i>`;
  }).join("");
}
// the lights box covers the picture's own box; each light sits where object-fit: cover puts the picture, cut to the
// picture's edge (its glow drawn at its own centre inside the cut), so no light reaches past the picture
function fitLights(box) {
  const img = box._img; if (!img || !box.isConnected) { if (ro) ro.unobserve(box); return; }
  const W = box.clientWidth, H = box.clientHeight; if (!W || !H) return;
  const ar = img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : box._ar;
  const dw = W / H > ar ? W : H * ar, dh = W / H > ar ? W / ar : H, ox = (W - dw) / 2, oy = (H - dh) / 2, px = (v) => v.toFixed(1) + "px";
  [...box.children].forEach((e, n) => {
    const l = box._ls[n]; if (!l) return;
    const cx = ox + l.x * dw, cy = oy + l.y * dh, r = Math.max(0.012, l.d) * dw / 2;
    const x0 = Math.max(0, cx - r), y0 = Math.max(0, cy - r), x1 = Math.min(W, cx + r), y1 = Math.min(H, cy + r);
    if (x1 - x0 < 2 || y1 - y0 < 2) { e.hidden = true; return; }
    e.hidden = false;
    e.style.left = px(x0); e.style.top = px(y0); e.style.width = px(x1 - x0); e.style.height = px(y1 - y0);
    e.style.setProperty("--r", px(r)); e.style.setProperty("--cx", px(cx - x0)); e.style.setProperty("--cy", px(cy - y0));
  });
}
const ro = typeof ResizeObserver === "function" ? new ResizeObserver((es) => es.forEach((e) => safe(() => fitLights(e.target)))) : null;
const LIVE = ".evart img, .ilpic img, .tarot .tp img";
function living(img) {
  if (img._lk || !ink()) return;
  img._lk = 1;
  const host = img.parentElement; if (!host) return;
  const il = host.classList.contains("ilpic");
  if (moving() && !il && !(host.classList.contains("evart") && hud && hud.res && !hud.cp)) {
    img.classList.add("lk-print");
    img.addEventListener("animationend", (e) => { if (e.animationName === "lkprint") img.classList.remove("lk-print"); });
  }
  const list = lightsOf(img.getAttribute("src"));
  if (!list || !list.length) return;
  const box = document.createElement("span"); box.className = "lk-lights"; box.setAttribute("aria-hidden", "true");
  box._img = img; box._ls = list; box._ar = host.closest(".tarot") ? 0.7 : 1.76;
  box.innerHTML = lightsHTML(list);
  img.after(box); img._lights = box;
  fitLights(box); if (ro) ro.observe(box);
  if (!img.complete) img.addEventListener("load", () => fitLights(box), { once: true });
  img.addEventListener("error", () => box.remove(), { once: true });
}
function unliving() { document.querySelectorAll(".lk-lights").forEach((x) => x.remove()); document.querySelectorAll("img.lk-print").forEach((x) => x.classList.remove("lk-print")); document.querySelectorAll(LIVE).forEach((x) => { x._lk = 0; }); }
const watch = new MutationObserver((recs) => safe(() => {
  let opts = false;
  for (const r of recs) {
    for (const n of r.addedNodes) {
      if (n.nodeType !== 1) continue;
      if (n.matches(LIVE)) living(n); else if (n.querySelector) n.querySelectorAll(LIVE).forEach(living);
      if (n.classList.contains("opt") || (n.querySelector && n.querySelector(".opt"))) opts = true;
    }
    for (const n of r.removedNodes) if (n.nodeType === 1 && n._lights && n._lights.isConnected) n._lights.remove();
  }
  if (opts) tagOptions();
}));
[tableEl, interEl, screenEl].forEach((el) => el && watch.observe(el, { childList: true, subtree: true }));
document.querySelectorAll(LIVE).forEach(living);

/* ---------------- 4: their own tarot card ---------------- */
const AGE_KEY = (a) => a < 13 ? "child" : a < 26 ? "youth" : a < 60 ? "adult" : "elder";
const AGE_WORD = { child: "as a child", youth: "in their youth", adult: "in their prime", elder: "in old age" };
function portraitOf(L) {
  if (!LK_PORT || !L || !L.w) return null;
  const order = COLORS.map((c, i) => [c, L.w[i]]).sort((a, b) => b[1] - a[1]);
  const lead = order[0][0], second = order[1][0], age = AGE_KEY(+L.age || 0), src = LK_PORT[lead] && LK_PORT[lead][age];
  return src ? { src, lead, second, age, key: lead + age } : null;
}
const portraitHTML = (p, cls) => `<span class="lk-pc ${cls}" style="--k1:${INK[p.lead]};--k2:${INK[p.second]}"><img src="${esc(p.src)}" alt="" onerror="this.parentNode.remove()"><span class="lk-wash"></span></span>`;
const portraitTip = (p, L) => tipBox(`${pip(p.lead)} Their own card`, `${esc(L.name)} ${AGE_WORD[p.age]}, ${CNAME[p.lead]} leading, ${CNAME[p.second]} after it.`, [],
  "The card follows them: its place is their strongest color, its wash their two strongest, and the figure ages with them.");
let crestKey = "";
function inkCrest(L) {
  const box = hudEl.querySelector(".crestbox"); if (!box || !ink()) return;
  const p = portraitOf(L); if (!p) return;
  box.classList.add("lk-hasp");
  box.insertAdjacentHTML("afterbegin", portraitHTML(p, "crest"));
  const pc = box.firstElementChild;
  if (crestKey && crestKey !== p.key && !busy && moving()) pc.classList.add("lk-turn");
  if (!busy) crestKey = p.key;
  setTip(pc, () => portraitTip(p, L));
}
const _openSheet = openSheet;
openSheet = function () {
  _openSheet();
  safe(() => {
    const L = hud && hud.life, sec = sheetEl.querySelector("#shPanel-portrait .sa-b"); if (!ink() || !sec || !L) return;
    const p = portraitOf(L); if (!p) return;
    sec.insertAdjacentHTML("afterbegin", `<figure class="lk-shp">${portraitHTML(p, "sheet")}<figcaption>${pip(p.lead)} ${CNAME[p.lead]} leads · ${AGE_WORD[p.age]}</figcaption></figure>`);
  });
};

/* ---------------- 5: chapter plates ---------------- */
const ROMAN = (n) => { let s = "", v = n; for (const [k, r] of [[10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"]]) while (v >= k) { s += r; v -= k; } return s; };
const plateEl = document.createElement("div"); plateEl.className = "lk-plate"; plateEl.hidden = true; plateEl.setAttribute("aria-hidden", "true");
document.body.appendChild(plateEl);
const ORN = `<svg class="orn" viewBox="0 0 240 14" aria-hidden="true"><path d="M4 7H104M136 7H236" /><path d="M110 7l10-6 10 6-10 6z"/><circle cx="98" cy="7" r="1.6"/><circle cx="142" cy="7" r="1.6"/></svg>`;
let plateQ = [], plateBusy = false, plateNo = 0, plateLife = "", plateT = 0;
const plateSeen = new Set();
let lifeN = 0;                       // one more at every birth in the story, so two lives of the same name are two lives
function lifeKey(L) { return L ? lifeN + "|" + (L.name || "") + "|" + (L.setting || "") : ""; }
function plate(p) {
  if (!moving()) return;
  const L = hud && hud.life;
  if (lifeKey(L) !== plateLife) { plateLife = lifeKey(L); plateNo = 0; plateSeen.clear(); }
  if (plateSeen.has(p.key) || plateQ.length >= 2) return;
  plateSeen.add(p.key); plateQ.push(p);
  if (!plateBusy) { plateBusy = true; clearTimeout(plateT); plateT = setTimeout(nextPlate, p.wait != null ? p.wait : revealPending() ? 1500 : 200); }
}
function nextPlate() {
  const p = plateQ.shift(); if (!p) { plateBusy = false; return; }
  plateNo++;
  const L = hud && hud.life, por = p.portrait !== false && ink() ? portraitOf(L) : null;
  plateEl.innerHTML = `<div class="lk-veil"></div><div class="lk-pl paper${p.kind ? " " + p.kind : ""}" style="${p.colors && p.colors.length ? `--k1:${INK[p.colors[0]]};--k2:${INK[p.colors[1] || p.colors[0]]}` : ""}">
    <div class="rn">${p.numeral || ROMAN(plateNo)}</div>${ORN}
    ${por ? portraitHTML(por, "plate") : ""}
    ${p.kick ? `<div class="kick">${esc(p.kick)}</div>` : ""}<h3>${p.pips && p.pips.length ? pips(p.pips) + " " : ""}${esc(p.title)}</h3>
    ${p.sub ? `<p>${esc(p.sub)}</p>` : ""}${ORN}</div>`;
  plateEl.classList.toggle("calm", motion !== "full");
  plateEl.classList.remove("out"); plateEl.hidden = false; void plateEl.offsetWidth; plateEl.classList.add("in");
  clearTimeout(plateT); plateT = setTimeout(endPlate, p.hold || 3000);
}
function endPlate() {
  if (plateEl.hidden) return;
  plateEl.classList.remove("in"); plateEl.classList.add("out");
  clearTimeout(plateT); plateT = setTimeout(() => { plateEl.hidden = true; plateEl.classList.remove("out"); nextPlate(); }, 620);
}
// any click or key closes a plate at once; the click itself still reaches the page (the plate never catches it)
addEventListener("pointerdown", () => { if (!plateEl.hidden && plateEl.classList.contains("in")) { plateQ = []; endPlate(); } }, true);
addEventListener("keydown", () => { if (!plateEl.hidden && plateEl.classList.contains("in")) { plateQ = []; endPlate(); } }, true);

/* ---------------- 3: colour you can see move ---------------- */
// What changed since the last settled state (the HUD redraws often while weeks run; only a settled state counts).
// At an outcome the change waits for the ink to land: the card turns, the drops fly, then the wheel and meters move.
let snap = null, holdUntil = 0, pend = [], pendT = 0, moved = null;
const seenGuild = new Set();         // a chapter for each identity the first time they take it, not for swings back
const revealPending = () => !!(choosing && flyer) || holdUntil > now();
function later(fn) { pend.push(fn); arm(holdUntil); }
function arm(at) { clearTimeout(pendT); pendT = setTimeout(flush, Math.max(0, at - now())); }
function flush() { const fs = pend; pend = []; holdUntil = 0; fs.forEach((f) => safe(f)); }
const _animSpider = animSpider;
animSpider = function (svg, frames, ms, base, done) {
  if (holdUntil > now() && frames && frames.length && svg) {
    safe(() => { svg.innerHTML = spiderSVG({ ...base, w: frames[0].w, want: frames[0].want, hits: false }); });
    return later(() => _animSpider(svg, frames, ms, base, done));
  }
  return _animSpider(svg, frames, ms, base, done);
};
const GOOD_UP = { content: 1, peace: 1, stress: -1, want: 0 };
function readHud() {
  const s = { m: {}, r: {} };
  hudEl.querySelectorAll(".mtr[data-ring]").forEach((el) => { const i = el.querySelector(".mbar i"), v = el.querySelector(".pv"); if (i && v) s.m[el.dataset.ring] = { w: parseFloat(i.style.width) || 0, v: parseInt(v.textContent, 10) || 0 }; });
  hudEl.querySelectorAll(".mean[data-r]").forEach((el) => { const i = el.querySelector(".col i"); if (i) s.r[el.dataset.r] = parseFloat(i.style.height) || 0; });
  return s;
}
function countTo(el, a, b, ms) {
  if (!el) return;
  const t0 = now(), suf = (el.textContent.match(/\D*$/) || [""])[0];
  const step = (t) => { const f = clamp((t - t0) / ms), e = 1 - Math.pow(1 - f, 3); el.textContent = Math.round(a + (b - a) * e) + suf; if (f < 1 && el.isConnected) requestAnimationFrame(step); };
  el.textContent = a + suf; requestAnimationFrame(step);
}
function floatDelta(host, d, good, cls) {
  if (!host || !d) return;
  const e = document.createElement("em");
  e.className = `lk-dl ${cls || ""} ${d > 0 ? "up" : "down"} ${good > 0 ? "good" : good < 0 ? "bad" : "even"}`;
  e.textContent = (d > 0 ? "+" : "−") + Math.abs(d);
  host.appendChild(e);
  if (moving()) setTimeout(() => e.remove(), 3200);
}
function afterHud(L) {
  if (!L || !L.w) return;
  inkCrest(L);
  const settled = !busy && !IL.on && hud && !hud.replay && hud.job !== "past";
  if (!settled) return;
  const cur = readHud(), key = lifeKey(L), prev = snap && snap.key === key && L.age >= snap.age ? snap : null;
  const guild = L.label ? L.guild || "" : "";
  snap = { key, age: L.age, m: cur.m, r: cur.r, w: L.w.slice(), guild };
  if (!prev) { if (guild) seenGuild.add(key + guild); return; }
  // identity: a new name for who they are is a chapter
  if (guild && guild !== prev.guild && hud.mode === "play" && !seenGuild.has(key + guild))
    plate({ key: "id|" + guild, kind: "id", kick: prev.guild ? "They become" : "Their colors take shape", title: guild, sub: L.meaning || "", pips: lettersOf(L.label), colors: lettersOf(L.label) });
  if (guild) seenGuild.add(key + guild);
  const run = [];
  for (const [k, v] of Object.entries(cur.m)) {
    const p = prev.m[k]; if (!p || p.v === v.v) continue;
    const el = hudEl.querySelector(`.mtr[data-ring="${k}"]`), bar = el && el.querySelector(".mbar i"), pv = el && el.querySelector(".pv");
    if (!el) continue;
    if (moving()) { bar.style.transition = "none"; bar.style.width = p.w + "%"; pv.textContent = p.v + "%"; }
    run.push(() => { if (!el.isConnected) return; if (moving()) { void bar.offsetWidth; bar.style.transition = ""; bar.style.width = v.w + "%"; countTo(pv, p.v, v.v, 1000); } floatDelta(el, v.v - p.v, Math.sign(v.v - p.v) * (GOOD_UP[k] ?? 1)); el.classList.add("lk-moved"); });
  }
  for (const [k, h] of Object.entries(cur.r)) {
    const p = prev.r[k]; if (p == null || Math.round(p) === Math.round(h)) continue;
    const el = hudEl.querySelector(`.mean[data-r="${k}"]`), col = el && el.querySelector(".col i"); if (!el) continue;
    if (moving()) { col.style.transition = "none"; col.style.height = p + "%"; }
    run.push(() => { if (!el.isConnected) return; if (moving()) { void col.offsetWidth; col.style.transition = ""; col.style.height = h + "%"; } floatDelta(el, Math.round(h - p), Math.sign(h - p), "mn"); });
  }
  const dc = L.w.map((v, i) => Math.round(v * 100) - Math.round(prev.w[i] * 100));
  moved = { t: now(), dw: L.w.map((v, i) => (v - prev.w[i]) * 100) };    // the drops follow the wheel's own numbers
  if (dc.some((d) => d)) run.push(() => wheelDeltas(dc));
  if (!run.length) return;
  if (holdUntil > now()) later(() => run.forEach((f) => safe(f))); else run.forEach((f) => safe(f));
}
// the orbs: a ring where a color gained or lost, and the points beside it
function wheelDeltas(dc) {
  const svg = $("hudWheel"), wrap = svg && svg.closest(".wheelw"); if (!svg || !wrap || svg.offsetParent === null) return;
  const sb = svg.getBoundingClientRect(), wb = wrap.getBoundingClientRect(), k = Math.min(sb.width / 212, sb.height / 206);
  const ox = sb.left - wb.left + (sb.width - 212 * k) / 2, oy = sb.top - wb.top + (sb.height - 206 * k) / 2;
  dc.forEach((d, i) => {
    if (!d) return;
    const [x, y] = spAt(i, SPR + 15), px = ox + (x + 6) * k, py = oy + (y + 2) * k, c = COLORS[i];
    if (moving()) { const r = document.createElement("span"); r.className = `lk-ring ${d > 0 ? "up" : "down"}`; r.style.cssText = `left:${px}px;top:${py}px;--k:${INK[c]}`; wrap.appendChild(r); setTimeout(() => r.remove(), 1200); }
    const e = document.createElement("em"); e.className = `lk-dl wh ${d > 0 ? "up" : "down"} even`; e.style.cssText = `left:${px}px;top:${py - 20 * k}px;--k:${INK[c]}`;
    e.textContent = (d > 0 ? "+" : "−") + Math.abs(d); wrap.appendChild(e);
    if (moving()) setTimeout(() => e.remove(), 3200);
  });
}
// ink drops from the turned card into the wheel, one per color that moved
function inkDrops(from, dw) {
  const svg = $("hudWheel"); if (!svg || svg.offsetParent === null || !moving()) return;
  const sb = svg.getBoundingClientRect(); if (sb.bottom < 0 || sb.top > innerHeight || sb.width < 20) return;
  const k = Math.min(sb.width / 212, sb.height / 206), ox = sb.left + (sb.width - 212 * k) / 2, oy = sb.top + (sb.height - 206 * k) / 2;
  const mx = Math.max(0.4, ...dw.map(Math.abs)), sx = from.left + from.width / 2, sy = from.top + from.height / 2;
  dw.forEach((v, i) => {
    if (Math.abs(v) < 0.5) return;
    const c = COLORS[i], [x, y] = spAt(i, SPR + 15), tx = ox + (x + 6) * k, ty = oy + (y + 2) * k, size = 8 + 9 * clamp(Math.abs(v) / mx);
    const d = document.createElement("span"); d.className = "lk-drop" + (v < 0 ? " out" : ""); d.setAttribute("aria-hidden", "true");
    d.style.cssText = `--k:${INK[c]};width:${size.toFixed(1)}px;height:${size.toFixed(1)}px`;
    document.body.appendChild(d);
    const a = v > 0 ? [sx + (i - 2) * 9, sy] : [tx, ty], b = v > 0 ? [tx, ty] : [tx + (tx - sx) * 0.12, ty + 46];
    const mid = [(a[0] + b[0]) / 2 + (v > 0 ? 0 : 10), Math.min(a[1], b[1]) - (v > 0 ? 70 + i * 8 : 10)];
    const kf = v > 0
      ? [{ transform: `translate(${a[0]}px, ${a[1]}px) scale(.4)`, opacity: 0 }, { transform: `translate(${a[0]}px, ${a[1] - 8}px) scale(1)`, opacity: 1, offset: 0.12 },
        { transform: `translate(${mid[0]}px, ${mid[1]}px) scale(1.05)`, opacity: 1, offset: 0.55 }, { transform: `translate(${b[0]}px, ${b[1]}px) scale(.55)`, opacity: 0.9 }]
      : [{ transform: `translate(${a[0]}px, ${a[1]}px) scale(.7)`, opacity: 0.85 }, { transform: `translate(${b[0]}px, ${b[1]}px) scale(.3)`, opacity: 0 }];
    const an = d.animate(kf, { duration: v > 0 ? 760 + i * 50 : 900, easing: v > 0 ? "cubic-bezier(.5,0,.4,1)" : "ease-in", fill: "forwards" });
    an.onfinish = () => d.remove();
    setTimeout(() => d.remove(), 2000);
  });
}

/* ---------------- the hud, the moment, the outcome, the story, the end ---------------- */
const _renderHud = renderHud;
renderHud = function (L) {
  // an outcome about to turn over: hold the wheel and the meters until its ink lands (set before the wheel starts moving)
  safe(() => { const w = $("hudWheel"); if (!busy && choosing && flyer && moving() && !holdUntil && w && w.offsetParent !== null) holdUntil = now() + Math.max(0, 600 - (now() - choosing.t)) + 1250; });
  _renderHud(L); safe(() => afterHud(L));
};

// a moment: odds by colour, the storm corner, and the lean wheel on the picture
function tagOptions() {
  const cp = hud && hud.cp; if (!cp) return;
  tableEl.querySelectorAll(".opt[data-i]").forEach((b) => {
    if (b._lk) return; b._lk = 1;
    const o = cp.options[+b.dataset.i]; if (!o) return;
    const g = b.querySelector(".gem"); if (g) g.classList.add(o.felt >= 0.7 ? "hi" : o.felt < 0.4 ? "lo" : "mid");
    if (!o.own && o.accept === "reluctant") b.classList.add("lk-rel");
    if (!o.own && o.accept === "against it") b.classList.add("lk-against");
    if (o.heart_pick) b.classList.add("lk-heart");
    if (o.head_pick) b.classList.add("lk-head");
    const show = (on) => leanShow(on ? o : null);
    b.addEventListener("pointerenter", (e) => { if (e.pointerType !== "touch") show(true); });
    b.addEventListener("pointerleave", () => show(false));
    b.addEventListener("focus", () => show(true)); b.addEventListener("blur", () => show(false));
  });
}
const LR = 33, LX = 50, LY = 50;
const lrad = (v) => LR * Math.sqrt(clamp(v, 0, 0.8) / 0.8);
const lat = (i, r) => [LX + r * Math.cos(SPA[i]), LY + r * Math.sin(SPA[i])];
const lpts = (vs) => vs.map((v, i) => lat(i, lrad(v)).map((x) => x.toFixed(1)).join(",")).join(" ");
function leanSVG(L) {
  const ring = (r) => COLORS.map((_, i) => lat(i, r).map((x) => x.toFixed(1)).join(",")).join(" ");
  return `<svg viewBox="0 0 100 100" aria-hidden="true"><polygon class="r0" points="${ring(LR)}"/><polygon class="r1" points="${ring(LR / 2)}"/>` +
    COLORS.map((_, i) => { const e = lat(i, LR); return `<line class="sp" x1="${LX}" y1="${LY}" x2="${e[0].toFixed(1)}" y2="${e[1].toFixed(1)}"/>`; }).join("") +
    `<polygon class="sh" points="${lpts(L.w)}"/><g class="ar"></g>` +
    COLORS.map((c, i) => { const e = lat(i, LR + 8); return `<circle class="cd" data-c="${c}" cx="${e[0].toFixed(1)}" cy="${e[1].toFixed(1)}" r="4.6" style="fill:var(--p${c})"/>`; }).join("") + `</svg>`;
}
function leanArrows(box, o, L) {
  const g = box.querySelector(".ar"); if (!g) return;
  box.classList.toggle("on", !!o);
  if (!o || !o.means || !o.means.length) { g.innerHTML = ""; box.querySelectorAll(".cd").forEach((x) => x.classList.remove("hl")); return; }
  const cs = actColors(o.means, o.ends);
  g.innerHTML = cs.map((c) => {
    const i = COLORS.indexOf(c), r0 = lrad(L.w[i]), r1 = Math.min(LR + 3, r0 + (o.ends.includes(c) ? 15 : 10));
    const p0 = lat(i, r0), p1 = lat(i, r1 - 4), tip = lat(i, r1), ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]);
    return `<g class="${o.ends.includes(c) ? "end" : "mean"}" style="color:${INK[c]}"><line x1="${p0[0].toFixed(1)}" y1="${p0[1].toFixed(1)}" x2="${p1[0].toFixed(1)}" y2="${p1[1].toFixed(1)}"/>` +
      `<polygon points="${tip.map((x) => x.toFixed(1)).join(",")} ${(p1[0] - uy * 3.4).toFixed(1)},${(p1[1] + ux * 3.4).toFixed(1)} ${(p1[0] + uy * 3.4).toFixed(1)},${(p1[1] - ux * 3.4).toFixed(1)}"/></g>`;
  }).join("");
  box.querySelectorAll(".cd").forEach((x) => x.classList.toggle("hl", cs.includes(x.dataset.c)));
}
// the card under the mouse: its arrows on the picture's wheel and, where the reading opens as a card (a wide window, over
// the picture), on a wheel in the reading's corner
function leanShow(o) {
  const L = hud && hud.life; if (!L || !L.w || !ink()) return;
  const box = tableEl.querySelector(".lk-lean:not(.st)"); if (box) leanArrows(box, o, L);
  const strip = $("evStrip"); if (!strip) return;
  const on = !!o && !strip.classList.contains("idle") && !!(o.means && o.means.length);
  strip.classList.toggle("lk-hasl", on);
  let sw = strip.querySelector(".lk-lean.st");
  if (!on) { if (sw) sw.remove(); return; }
  if (!sw) { strip.insertAdjacentHTML("beforeend", `<span class="lk-lean st" aria-hidden="true">${leanSVG(L)}</span>`); sw = strip.lastElementChild; }
  leanArrows(sw, o, L);
}
function inkMoment(h) {
  const cp = h && h.cp, L = h && h.life; if (!cp || busy || !L || !L.w) return;
  tagOptions();
  const art = tableEl.querySelector(".evart"); if (!art || art.querySelector(".lk-lean") || !ink()) return;
  art.insertAdjacentHTML("beforeend", `<span class="lk-lean" id="lkLean">${leanSVG(L)}</span>`);
  setTip($("lkLean"), () => tipBox(`${ic("wheel")} Which way it pulls`, "", [], `${esc(L.name)}'s five colors now, in ink. Hover a card: the arrows show the colors it would pull them toward, solid for what it is for, thin for how it is done.`));
}
const _renderTable = renderTable;
renderTable = function (h) { _renderTable(h); safe(() => inkMoment(h)); };

// the outcome: the ink runs, the chips stamp in, a long shot made or a title won is a chapter
const _renderResolution = renderResolution;
renderResolution = function (h, reveal) {
  const fr = reveal && flyer ? flyer.getBoundingClientRect() : null, key = h && h.res ? "res|" + h.res.age + "|" + h.res.title : "";
  _renderResolution(h, reveal);
  safe(() => {
    if (!h || !h.res || tableEl._lkRes === key) return;
    tableEl._lkRes = key;
    const r = h.res;
    if (reveal && moving()) {
      tableEl.classList.add("lk-rev"); setTimeout(() => tableEl.classList.remove("lk-rev"), 2600);
      const dw = moved && now() - moved.t < 1500 ? moved.dw : r.dw;
      if (fr && dw) { holdUntil = now() + 1250; arm(holdUntil); setTimeout(() => safe(() => inkDrops(fr, dw)), 430); }
    }
    if (hud && hud.replay) return;
    if (r.long_shot && r.long_shot.made) plate({ key: "ls|" + key, kind: "ls", kick: "Against the odds", title: cap(r.act), sub: `A long shot, made: ${odds100(r.long_shot.odds)}.`, colors: splitColors(r.colors).ends });
    for (const x of (r.roles || []).filter((x) => x.up && x.title).slice(0, 1))
      plate({ key: "ti|" + key + x.word, kind: "ti", kick: "A new title", title: cap(x.word), sub: cap(r.act), colors: splitColors(r.colors).ends });
  });
};

// the story: new lines come in like wet ink; taking over the life is the first chapter
const _addFeed = addFeed;
addFeed = function (items) {
  _addFeed(items);
  safe(() => {
    if (items && items.some((it) => it.tag === "birth")) lifeN++;
    if (!items || !items.length || !hud || hud.replay || hud.job === "past" || hud.loaded) return;
    if (moving() && items.length <= 24) {
      let k = 0;
      for (const it of items) {
        const el = it.tag === "chapter" ? yearEls.get(it.age) : document.getElementById("it" + it._i);
        if (el && !el._lkin) { el._lkin = 1; el.classList.add("lk-in"); el.style.setProperty("--lk-d", Math.min(k++, 8) * 70 + "ms"); }
      }
    }
    const st = items.find((it) => it.tag === "start");
    const L = hud.life;
    if (st && L) plate({ key: "start|" + lifeKey(L), kind: "start", kick: `${L.name} is ${Math.floor(L.age)} now`, title: "The voice in their head", sub: "From here on, the choices at the big moments are yours to steer, or theirs to keep.", colors: lettersOf(L.label) });
  });
};

// the end: a last plate, their card as it ended, and the reading coming in line by line
const _renderReview = renderReview;
renderReview = function (h) {
  _renderReview(h);
  safe(() => {
    if (reviewEl.hidden) { reviewEl._lk = 0; return; }
    if (reviewEl._lk) return; reviewEl._lk = 1;
    const L = h.life, r = h.review || {};
    const p = ink() && L ? portraitOf(L) : null, head = reviewEl.querySelector(".mh");
    if (p && head) head.insertAdjacentHTML("afterend", `<div class="lk-final">${portraitHTML(p, "final")}<div class="lk-yrs">${esc(L.name)} · ${r.died ? Math.floor(r.died.age) : Math.floor(L.age)} years</div></div>`);
    if (moving()) { reviewEl.classList.add("lk-rv"); [...reviewEl.children].forEach((c, k) => c.style.setProperty("--lk-d", 900 + Math.min(k, 12) * 150 + "ms")); }
    if (L && !hud.replay) plate({ key: "end|" + lifeKey(L), kind: "end", numeral: "Finis", kick: "The end of a life", title: L.name, sub: r.final ? `Ended as ${r.final}.` : "", colors: lettersOf(L.label), hold: 2600, wait: 150 });
  });
};

/* ---------------- the two settings, in the Table menu after Interlude ---------------- */
const _renderTools = renderTools;
renderTools = function (h) { _renderTools(h); safe(addRows); };
const ROWS = { motion: ["burst", "Motion", () => MOTION_WORD[motion], "How much moves: full (pictures breathe, ink flies, pages turn), calm (changes still count up, nothing loops) or off."],
  look: ["mask", "Look", () => LOOK_WORD[look], "Ink (the engraved look) or classic (the drawing of version 22). The helpers for choosing and the changes beside the wheel and meters stay in both."] };
function addRows() {
  const pop = $("tPop"); if (!pop || pop.querySelector("[data-lk]")) return;
  const at = pop.querySelector('[data-page="i"]'); if (!at) return;
  at.insertAdjacentHTML("afterend", Object.entries(ROWS).map(([k, [icn, label, val]]) => `<button class="mrow2" data-lk="${k}" role="menuitem">${ic(icn)}<span class="t">${label}</span><span class="v">${val()}</span></button>`).join(""));
  pop.querySelectorAll("[data-lk]").forEach((b) => {
    b.addEventListener("click", (e) => { e.stopPropagation(); turn(b.dataset.lk); b.querySelector(".v").textContent = ROWS[b.dataset.lk][2](); });
    setTip(b, () => tipBox(`${ic(ROWS[b.dataset.lk][0])} ${ROWS[b.dataset.lk][1]}: ${ROWS[b.dataset.lk][2]()}`, "", [], ROWS[b.dataset.lk][3]));
  });
}
function turn(k) {
  if (k === "motion") { motion = MOTION[(MOTION.indexOf(motion) + 1) % MOTION.length]; keep("chroma.motion", motion); }
  else { look = LOOK[(LOOK.indexOf(look) + 1) % LOOK.length]; keep("chroma.look", look); }
  setRoot();
  if (!ink()) { unliving(); document.querySelectorAll(".lk-pc, .lk-lean, .lk-shp, .lk-final").forEach((x) => x.remove()); }
  else document.querySelectorAll(LIVE).forEach(living);
  if (hud && hud.life && hud.life.w && !IL.on) renderHud(hud.life);
  drawLine();
  if (k === "look" && ink() && hud && hud.cp && !busy) inkMoment(hud);
}

drawLine();
})();
</script>
