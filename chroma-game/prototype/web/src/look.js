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
   on the moment's picture that shows which way the card under the mouse would pull them. The status panel reads at a
   glance: trends, danger glow, the wheel a year ago, sparklines in its hovers and a key (Emren 10-10 10:53 UTC). Honours
   and big moments are scaled by rarity and impact: gilt seal plates, struck chips, a heavier frame, weight in the story
   (Emren 10-10 11:24 UTC). */
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
  const il = host.classList.contains("ilpic"), card = host.classList.contains("lk-pc");
  if (moving() && !il && !card && !(host.classList.contains("evart") && hud && hud.res && !hud.cp)) {
    img.classList.add("lk-print");
    img.addEventListener("animationend", (e) => { if (e.animationName === "lkprint") img.classList.remove("lk-print"); });
  }
  const list = lightsOf(img.getAttribute("src"));
  if (!list || !list.length) return;
  const box = document.createElement("span"); box.className = "lk-lights"; box.setAttribute("aria-hidden", "true");
  box._img = img; box._ls = list; box._ar = host.closest(".tarot") || card ? 0.7 : 1.76;
  box.innerHTML = lightsHTML(list);
  if (card) host.appendChild(box); else img.after(box);
  img._lights = box;
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
const lightPortraits = (root) => root && root.querySelectorAll(".lk-pc:not(.crest) img").forEach(living);
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
    lightPortraits(sec);
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
  if (!p || !moving()) return;
  const L = hud && hud.life;
  if (lifeKey(L) !== plateLife) { plateLife = lifeKey(L); plateNo = 0; plateSeen.clear(); }
  if (plateSeen.has(p.key) || plateQ.length >= 2) return;
  plateSeen.add(p.key); plateQ.push(p);
  if (!plateBusy) { plateBusy = true; clearTimeout(plateT); plateT = setTimeout(nextPlate, p.wait != null ? p.wait : revealPending() ? 1500 : 200); }
}
function nextPlate() {
  const p = plateQ.shift(); if (!p) { plateBusy = false; return; }
  plateNo++;
  const L = hud && hud.life, por = !p.seal && p.portrait !== false && ink() ? portraitOf(L) : null;
  plateEl.innerHTML = `<div class="lk-veil"></div><div class="lk-pl paper${p.kind ? " " + p.kind : ""}" style="${p.colors && p.colors.length ? `--k1:${INK[p.colors[0]]};--k2:${INK[p.colors[1] || p.colors[0]]}` : ""}">
    <div class="rn">${p.numeral || ROMAN(plateNo)}</div>${ORN}
    ${p.seal ? sealHTML(p.seal) : por ? portraitHTML(por, "plate") : ""}
    ${p.kick ? `<div class="kick">${esc(p.kick)}</div>` : ""}<h3>${p.pips && p.pips.length ? pips(p.pips) + " " : ""}${esc(p.title)}</h3>
    ${p.sub ? `<p>${esc(p.sub)}</p>` : ""}${ORN}</div>`;
  safe(() => lightPortraits(plateEl));
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
  safe(() => { memW = yearAgo(L); });
  _renderHud(L); safe(() => afterHud(L)); safe(() => hudMarks(L)); safe(() => honourHud(L));
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
    const show = (on) => { leanShow(on ? o : null); safe(() => hudPreview(on ? o : null)); };
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
renderTable = function (h) { _renderTable(h); safe(() => inkMoment(h)); safe(() => weighMoment(h)); };

// the outcome: the ink runs, the chips stamp in, a long shot made or a title won is a chapter
const _renderResolution = renderResolution;
renderResolution = function (h, reveal) {
  const fr = reveal && flyer ? flyer.getBoundingClientRect() : null, key = h && h.res ? "res|" + h.res.age + "|" + h.res.title : "";
  _renderResolution(h, reveal);
  safe(() => hudPreview(null));
  safe(() => {
    if (!h || !h.res || tableEl._lkRes === key) return;
    tableEl._lkRes = key;
    const r = h.res;
    if (reveal && moving()) {
      tableEl.classList.add("lk-rev"); setTimeout(() => tableEl.classList.remove("lk-rev"), 2600);
      const dw = moved && now() - moved.t < 1500 ? moved.dw : r.dw;
      if (fr && dw) { holdUntil = now() + 1250; arm(holdUntil); setTimeout(() => safe(() => inkDrops(fr, dw)), 430); }
    }
    safe(() => honourOutcome(r, reveal));
    if (hud && hud.replay) return;
    // a long shot made, or a title earned that is not an everyday one, is a chapter; a rare one is a gilt plate with its
    // seal. A long shot that brings the title is one plate, not two.
    const best = (r.roles || []).map((x) => ({ x, hn: honour(x) })).filter((o) => o.x.title && o.hn.t >= 2).sort((a, b) => b.hn.t - a.hn.t)[0];
    const ends = splitColors(r.colors).ends, ls = r.long_shot && r.long_shot.made;
    if (ls) plate({ key: "ls|" + key, kind: "ls hon", seal: best ? roleIconOf(best.x) : "star", kick: "Against the odds", title: cap(best ? best.x.word : r.act),
      sub: `A long shot, made: ${odds100(r.long_shot.odds)}.${best && best.hn.sh != null ? " " + cap(rarityWord(best.hn.sh)) + "." : ""}`, colors: ends, hold: 3600 });
    else if (best) plate(best.hn.t >= 3
      ? { key: "ti|" + key + best.x.word, kind: "ti hon", seal: roleIconOf(best.x), kick: "A rare title", title: cap(best.x.word), sub: `${cap(rarityWord(best.hn.sh))}.`, colors: ends, hold: 3600 }
      : { key: "ti|" + key + best.x.word, kind: "ti", kick: "A new title", title: cap(best.x.word), sub: cap(r.act), colors: ends });
  });
};

// the story: new lines come in like wet ink; taking over the life is the first chapter
const _addFeed = addFeed;
addFeed = function (items) {
  _addFeed(items);
  safe(() => {
    if (items && items.some((it) => it.tag === "birth")) lifeN++;
    safe(() => weighFeed(items || [], !!hud && !hud.replay && hud.job !== "past" && !hud.loaded && (items || []).length <= 24));
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
    lightPortraits(reviewEl);
    if (moving()) { reviewEl.classList.add("lk-rv"); [...reviewEl.children].forEach((c, k) => c.style.setProperty("--lk-d", 900 + Math.min(k, 12) * 150 + "ms")); }
    if (L && !hud.replay) plate({ key: "end|" + lifeKey(L), kind: "end", numeral: "Finis", kick: "The end of a life", title: L.name, sub: r.final ? `Ended as ${r.final}.` : "", colors: lettersOf(L.label), hold: 2600, wait: 150 });
  });
};

/* ---------------- the start spread (Emren 10-10 09:54 UTC: "The Cradle should be first, left-most option. The crossroads
   must be right-most option. We need to click the option without jumping the game. Click the life starter, and write the
   name, and game starts.") ----------------
   The cards run I to VI with the Crossroads (0, Build your own) last. A click picks the card and puts the cursor in the
   name: nothing scrolls, a double click no longer begins, and once a card is clicked the mouse passing over the others no
   longer changes the reading. If the name would sit below the fold, the reading docks at the foot of the window instead
   of the page moving. Enter or Begin starts the life, as before. Every look and motion setting. */
let spreadPicked = false;
const _renderScreen = renderScreen;
renderScreen = function (h) {
  _renderScreen(h);
  safe(() => {
    if (!h || h.mode !== "menu") { spreadPicked = spreadDocked = false; screenEl.style.paddingBottom = ""; return; }
    const row = screenEl.querySelector(".tarots"), rd = $("reading"); if (!row || !rd) return;
    const isZero = (b) => b.classList.contains("zero");
    [...row.querySelectorAll(".tarot")].sort((a, b) => isZero(a) - isZero(b) || +a.dataset.k - +b.dataset.k)
      .forEach((b, i) => { b.style.setProperty("--n", i); row.appendChild(b); });
    rd.scrollIntoView = () => {};                       // app.js scrolls the reading into view on a click: the page stays put
    row.addEventListener("dblclick", (e) => { if (e.target.closest(".tarot")) e.stopPropagation(); }, true);
    row.addEventListener("pointerenter", (e) => { if (spreadPicked && e.target.classList && e.target.classList.contains("tarot")) e.stopPropagation(); }, true);
    row.addEventListener("click", (e) => { if (e.target.closest(".tarot")) { spreadPicked = true; requestAnimationFrame(() => safe(dockReading)); } }, true);
    if (spreadPicked) dockReading();
  });
};
let spreadDocked = false;
function dockReading() {
  const rd = $("reading"), go = $("go"); if (!rd || !go) return;
  if (!rd.classList.contains("lk-dock")) {
    const s = screenEl.getBoundingClientRect(), g = go.getBoundingClientRect();
    if (!spreadDocked && g.bottom <= s.bottom - 6 && g.top >= s.top) return;
    rd.classList.add("lk-dock"); if (!spreadDocked) rd.classList.add("lk-dockin");
    spreadDocked = true;
  }
  screenEl.style.paddingBottom = rd.getBoundingClientRect().height + 24 + "px";   // the cards and the foot can still scroll clear of it
  if (!touchUI && $("txt")) $("txt").focus({ preventScroll: true });
}

/* ---------------- reading the panel at a glance (Emren 10-10 10:53 UTC: "apply everything to improve visual quality") ----
   The status panel says which way things are going and what is in danger, without opening a hover:
   - a ▲ or ▼ beside a meter, a mean or a need that moved 4 points or more since a year ago (green when that is good for
     them, red when it is not, gold for wanting, which is neither);
   - a red glow on a meter or mean in a danger zone (satisfaction or peace under 20%, strain over 80%, a mean under 15%),
     a gold one on wanting close to breaking through;
   - on the wheel, a dotted outline of their colors a year ago (from the river), so the direction they moved shows;
   - in the hover of a meter, mean or need, a line of its last years and where it stood a year ago;
   - a "?" on the crest with every mark and symbol of the panel in one key.
   The history is kept here, per life, from the panel's own numbers (the river gives the wheel and the two moods back to
   birth); nothing is sent to the engine. Every look and motion setting; calm and off keep the glow still. */
const TREND_MIN = 4, KEEP_YRS = 15;
const MEANS_K = ["money", "time", "health", "ties", "freedom"];
let hist = [], histKey = "", memW = null;
function panelNow(L) {
  const v = { content: clamp(L.content), peace: clamp(L.peace), stress: clamp(L.stress / 1.5), want: clamp(L.want / Math.max(L.want_thr, 1e-9)) };
  for (const k of MEANS_K) if (L.res && L.res[k] != null) v["r." + k] = clamp(L.res[k]);
  for (const [k, x] of Object.entries(L.needs || {})) v["n." + k] = clamp(x);
  return v;
}
function record(L) {
  const key = lifeKey(L), last = hist[hist.length - 1];
  if (key !== histKey || (last && L.age < last.a - 0.01)) { hist = []; histKey = key; }
  if (hud && hud.replay) return;
  const l2 = hist[hist.length - 1];
  if (l2 && L.age - l2.a < 1 / 12) { l2.v = panelNow(L); return; }   // one sample a month; the newest month keeps its last word
  hist.push({ a: L.age, v: panelNow(L) });
  while (hist.length && hist[0].a < L.age - KEEP_YRS) hist.shift();
}
// the value of a panel number a year ago: our own samples first, the river for the two moods (it goes back to birth)
function agoOf(k, L) {
  let best = null;
  for (const s of hist) if (s.a <= L.age - 1 && s.v[k] != null) best = s.v[k];
  if (best == null && (k === "content" || k === "peace")) {
    const col = k === "content" ? 6 : 7;
    for (const r of L.river || []) if (r[0] <= L.age - 1 && r.length > col) best = r[col];
  }
  return best;
}
function seriesOf(k, L) {
  const pts = hist.filter((s) => s.v[k] != null).map((s) => [s.a, s.v[k]]);
  if (pts.length < 6 && (k === "content" || k === "peace")) {
    const col = k === "content" ? 6 : 7;
    return (L.river || []).filter((r) => r[0] >= L.age - KEEP_YRS && r.length > col).map((r) => [r[0], r[col]]).concat([[L.age, panelNow(L)[k]]]);
  }
  return pts;
}
function yearAgo(L) {
  if (!L || !L.river || L.age < 1.5) return null;
  let row = null;
  for (const r of L.river) if (r[0] <= L.age - 1) row = r;
  return row ? row.slice(1, 6) : null;
}
const GOOD_OF = (k) => k === "stress" ? -1 : k === "want" ? 0 : 1;
const warnOf = (k, v) => k === "stress" ? (v >= 0.8 ? "high" : "") : k === "want" ? (v >= 0.9 ? "near" : "") : k === "content" || k === "peace" ? (v <= 0.2 ? "low" : "") : k.startsWith("r.") ? (v <= 0.15 ? "low" : "") : "";
function hudMarks(L) {
  if (!L || !L.w) return;
  record(L);
  const cur = panelNow(L);
  const mark = (el, k) => {
    if (!el) return;
    const ago = agoOf(k, L), d = ago == null ? 0 : Math.round(cur[k] * 100) - Math.round(ago * 100);
    if (Math.abs(d) >= TREND_MIN) { el.dataset.lkTr = d > 0 ? "up" : "down"; el.dataset.lkGood = String(Math.sign(d) * GOOD_OF(k.replace(/^[rn]\./, "")) || 0); }
    else { delete el.dataset.lkTr; delete el.dataset.lkGood; }
    const w = warnOf(k, cur[k]); if (w) el.dataset.lkWarn = w; else delete el.dataset.lkWarn;
  };
  hudEl.querySelectorAll(".mtr[data-ring]").forEach((el) => mark(el, el.dataset.ring));
  hudEl.querySelectorAll(".mean[data-r]").forEach((el) => mark(el, "r." + el.dataset.r));
  hudEl.querySelectorAll(".nd[data-nd]").forEach((el) => mark(el, "n." + el.dataset.nd));
  const crest = hudEl.querySelector(".crestbox");
  if (crest && !$("lkKey")) {
    crest.insertAdjacentHTML("beforeend", `<span class="wkey lk-key" id="lkKey" tabindex="0" aria-label="What the marks on this panel mean">?</span>`);
    setTip($("lkKey"), () => panelKey(L));
  }
}
const KEY_SW = { up: `<b class="lk-sw up">▲</b>`, down: `<b class="lk-sw down">▼</b>` };
function panelKey(L) {
  const rows = [[`${KEY_SW.up}${KEY_SW.down}`, "Up or down 4 points or more since a year ago: green when that is good for them, red when it is not."],
    [`<b class="lk-sw glow"></b>`, "A danger zone: satisfaction or peace under 20%, strain over 80%, a mean under 15%. Gold on wanting: close to breaking through."],
    [`<i class="spk k-mem"></i>`, "On the wheel: their colors a year ago, so you can see which way they moved."]];
  rows.push([`<span class="lk-sw down">${ic(NEED_ICON.safety || "shield")}</span>`, "A need under 30% pulses."]);
  rows.push([`<b class="lk-pvb spend lk-key-pv">−</b><b class="lk-pvb win lk-key-pv">+</b>`, "While a card is under the mouse: what it would spend (−), win (+) or put at risk if it fails (−?) among the means, and the needs it meets (+)."]);
  return tipBox(`${ic("ci-crystal-ball")} Reading this panel`, "", rows, "Hover any meter, mean or need for its numbers and a line of its last years.");
}
// the hover of a meter, mean or need: its last years as a line, and where it stood a year ago
function sparkHTML(k, L) {
  const S = seriesOf(k, L); if (S.length < 3) return "";
  const a0 = S[0][0], a1 = Math.max(S[S.length - 1][0], a0 + 0.5), W = 180, H = 34;
  let lo = Math.min(...S.map((s) => s[1])), hi = Math.max(...S.map((s) => s[1]));       // its own range, at least 20 points tall
  const mid = (lo + hi) / 2, half = Math.max(0.1, (hi - lo) / 2 + 0.04); lo = Math.max(0, mid - half); hi = Math.min(1, lo + 2 * half); lo = Math.max(0, hi - 2 * half);
  const x = (a) => ((a - a0) / (a1 - a0) * (W - 4) + 2).toFixed(1), y = (v) => (H - 3 - clamp((v - lo) / (hi - lo)) * (H - 6)).toFixed(1);
  const d = S.map(([a, v], i) => `${i ? "L" : "M"}${x(a)} ${y(v)}`).join("");
  const ago = agoOf(k, L), nowv = panelNow(L)[k];
  const ref = ago != null ? `<line class="ago" x1="2" x2="${W - 2}" y1="${y(ago)}" y2="${y(ago)}"/>` : "";
  const yrs = Math.max(1, Math.round(a1 - a0));
  const diff = ago != null ? Math.round(nowv * 100) - Math.round(ago * 100) : null, gd = diff ? Math.sign(diff) * GOOD_OF(k.replace(/^[rn]\./, "")) : 0;
  return `<div class="lk-spark"><svg viewBox="0 0 ${W} ${H}" aria-hidden="true">${ref}<path d="${d}"/><circle cx="${x(S[S.length - 1][0])}" cy="${y(nowv)}" r="2.4"/></svg>
    <span>the last ${yrs} year${yrs > 1 ? "s" : ""}${ago != null ? ` · a year ago ${Math.round(ago * 100)}%${diff ? ` <b class="${gd > 0 ? "up" : gd < 0 ? "down" : ""}">${diff > 0 ? "+" : "−"}${Math.abs(diff)}</b>` : ", the same"}` : ""}</span></div>`;
}
const _showTip = showTip;
showTip = function (el) {
  _showTip(el);
  safe(() => {
    const L = hud && hud.life; if (!L || !el || !el.closest || tipOwner !== el || !el.closest("#hud")) return;
    const k = el.matches(".mtr[data-ring]") ? el.dataset.ring : el.matches(".mean[data-r]") ? "r." + el.dataset.r : el.matches(".nd[data-nd]") ? "n." + el.dataset.nd : "";
    const sp = k && sparkHTML(k, L); if (!sp) return;
    tipEl.insertAdjacentHTML("beforeend", sp); placeTip(el.getBoundingClientRect(), false);
  });
};
// the wheel's memory: the outline of a year ago, under where they are now
// a card under the mouse marks on the panel what it would spend, win or risk (its means) and the needs it meets
const NEED_OF = (w) => { w = String(w || "").toLowerCase(); return Object.keys(NEED_SHORT).find((k) => k === w || NEED_SHORT[k].toLowerCase() === w || (NEED_LONG[k] || "") === w) || ""; };
function hudPreview(o) {
  hudEl.querySelectorAll(".lk-pvb").forEach((x) => x.remove());
  hudEl.querySelectorAll(".lk-pv").forEach((x) => x.classList.remove("lk-pv"));
  if (!o) return;
  const f = o.follows || {}, by = {};
  const put = (k, s) => { (by[k] = by[k] || new Set()).add(s); };
  for (const x of f.cost || []) put(x.slice(1), "spend");
  for (const x of f.win || []) put(x.slice(1), x[0] === "+" ? "win" : "spend");
  for (const x of f.lose || []) put(x.slice(1), "risk");
  for (const [k, s] of Object.entries(by)) {
    const el = hudEl.querySelector(`.mean[data-r="${k}"]`); if (!el) continue;
    const word = s.has("spend") ? "−" : s.has("win") && s.has("risk") ? "±" : s.has("win") ? "+" : "−?";
    const cls = s.has("spend") ? "spend" : s.has("win") ? "win" : "risk";
    el.classList.add("lk-pv"); el.insertAdjacentHTML("beforeend", `<b class="lk-pvb ${cls}">${word}</b>`);
  }
  for (const w of f.needs || []) {
    const k = NEED_OF(w), el = k && hudEl.querySelector(`.nd[data-nd="${k}"]`); if (!el) continue;
    el.classList.add("lk-pv"); el.insertAdjacentHTML("beforeend", `<b class="lk-pvb win">+</b>`);
  }
}
const _spiderSVG = spiderSVG;
spiderSVG = function (o) {
  const s = _spiderSVG(o);
  if (!o || o.id !== "hw" || !memW) return s;
  const at = s.indexOf('<polygon class="pos"');
  return at < 0 ? s : s.slice(0, at) + `<polygon class="lk-mem" points="${spPts(memW)}"/>` + s.slice(at);
};
SP_KEY.push(["mem", "A year ago", "The faint dotted outline: their five colors a year ago, so you can see which way they have moved since."]);

/* ---------------- honours and weight (Emren 10-10 11:24 UTC: "you can visually show big impact events or hard-earned
   perks/titles in better, professional way") ----------------
   Scaled by how rare and how hard-won, from what the page already has. A title's rarity is the Book's: the share of
   simulated modern Earth lives that ever hold it (rarity.py). A perk is hard-won when an act earned it. An event weighs by
   what it is (a loss, a breakthrough) and by how far it moved their colors.
   - a rare title (fewer than 1 life in 10), or a long shot made, is a gilt plate with a struck seal; an earned title that
     is not an everyday one keeps its plate; an everyday title or a status they did not earn has none
   - at the outcome, an honour's chip is struck like a medal with its rarity beside it; a week that moved their colors
     more than most says so, and its card is framed heavier; a very high stakes moment has an ember edge
   - in the story, a loss carries a mourning rule, a turning point an ink roundel, an earned honour a small seal, and a
     moment fewer than 1 life in 10 meets a star; the moment itself says it is rare
   - in the panel, a new honour shines once, and a rare title keeps a small star
   Statuses that are hard to bear (divorced, widowed, out of work) are never celebrated. Every mark works in both looks;
   calm motion keeps them still, and off shows them without any movement. */
const SOMBRE = new Set(["widowed", "divorced", "homeless", "out of work", "someone with a record", "ex-prisoner", "refugee", "asylum applicant",
  "bankruptcy or insolvency in their history", "on probation or community supervision", "living in residential care", "displaced by a disaster",
  "has killed in war", "carer for a parent"]);
const EARNED_ST = new Set(["graduate", "doctoral graduate", "homeowner", "naturalised citizen", "cancer survivor", "in recovery", "veteran", "retiree",
  "first-generation university student"]);
const HEAVY = 5;                                     // points of 100 one color moves at an outcome; about 1 outcome in 8 moves more
const BIG_TAGS = new Set(["breakthrough", "turn", "clash", "crisis", "healed", "hardened"]);
// 3 rare title, 2 earned (an uncommon title, or a perk an act earned), 1 everyday, 0 nothing to honour, -1 hard to bear
function honour(x) {
  if (!x || x.up === false || x.what === "lost") return { t: 0, sh: null };
  if (x.kind === "status") { if (SOMBRE.has(x.name)) return { t: -1, sh: null }; if (!EARNED_ST.has(x.name)) return { t: 0, sh: null }; }
  if (x.title) {
    const i = bookInfo("t|" + x.name), sh = i && i.sh != null ? i.sh : null;
    return { t: isRare(sh) ? 3 : sh != null && sh >= 0.3 ? 1 : 2, sh };
  }
  return { t: /^through /.test(x.how || "") ? 2 : x.kind === "credential" || x.kind === "standing" ? 1 : 0, sh: null };
}
const livesN = () => ((bookCat.earth || {}).lives || 0);
const oneIn = (sh) => sh === 0 ? `none in ${livesN().toLocaleString()}` : `1 in ${Math.round(1 / sh)}`;
const rarityWord = (sh) => sh == null ? "" : sh === 0 ? `not one of ${livesN().toLocaleString()} simulated lives held it` : `only about 1 life in ${Math.round(1 / sh)} ever holds it`;
const RAR_FOOT = "Rarity is the share of simulated modern Earth lives, birth to 80, that ever meet it.";
// the seal: a scalloped medallion, struck in gilt, the honour's own sign in the middle
const SEAL_EDGE = (() => { let d = ""; for (let k = 0; k < 48; k++) { const a = (k / 48) * Math.PI * 2, rr = k % 2 ? 27.2 : 30; d += (k ? "L" : "M") + (32 + rr * Math.cos(a)).toFixed(2) + " " + (32 + rr * Math.sin(a)).toFixed(2); } return d + "Z"; })();
const sealHTML = (icon, cls = "") => `<span class="lk-seal ${cls}" aria-hidden="true"><svg viewBox="0 0 64 64"><path class="e" d="${SEAL_EDGE}"/><circle class="f" cx="32" cy="32" r="23.5"/><circle class="r" cx="32" cy="32" r="20.5"/></svg>${ic(icon)}</span>`;
const addTip = (el, more) => { const f = tips.get(el); if (f) setTip(el, () => f() + more()); };
const maxMove = (dw) => dw && dw.length ? Math.max(...dw.map(Math.abs)) : 0;

// the outcome: honours struck, a heavy week framed and named, without changing a word of what app.js wrote
function honourOutcome(r, reveal) {
  const ev = tableEl;
  ev.querySelectorAll(".st.rl[data-rr]").forEach((el) => {
    const x = (r.roles || [])[+el.dataset.rr], hn = honour(x); if (!x) return;
    if (hn.t < 0) { el.classList.add("lk-sombre"); return; }
    if (hn.t < 2) return;
    el.classList.add("lk-hon", "t" + hn.t);
    el.insertAdjacentHTML("beforeend", `<small class="lk-rar">${hn.sh != null ? (hn.t >= 3 ? "★ " : "") + esc(oneIn(hn.sh)) : "hard-won"}</small>`);
    addTip(el, () => `<p class="lk-tiprar">${hn.sh != null ? `${ic("star")} ${esc(cap(rarityWord(hn.sh)))}. ${RAR_FOOT}` : `${ic("star")} Hard-won: an act of theirs earned it, not the years.`}</p>`);
  });
  const mx = maxMove(r.dw);
  ev.classList.remove("lk-stakes3");
  ev.classList.toggle("lk-heavy", mx >= HEAVY);
  ev.classList.toggle("lk-honour", !!(r.long_shot && r.long_shot.made) || (r.roles || []).some((x) => honour(x).t >= 3));
  if (mx >= HEAVY) {
    const row = ev.querySelector(".evtext .verdict.vbig"); if (!row || row.querySelector(".lk-impact")) return;
    const big = COLORS.map((c, i) => [c, r.dw[i]]).filter(([, v]) => Math.abs(v) >= 1.5).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 2);
    row.insertAdjacentHTML("afterend", `<div class="verdict"><span class="tag lk-impact">${ic("burst")}It changed them: ${big.map(([c, v]) => `${pip(c)}${v > 0 ? "+" : "−"}${Math.round(Math.abs(v))}`).join(" ")}</span></div>`);
    setTip(ev.querySelector(".lk-impact"), () => tipBox(`${ic("burst")} A week that changed them`, "", [["Moved", colorMoves(r.dw)]],
      `One of their colors moved ${Math.round(mx)} points of 100 this week; most outcomes move each color by less than ${HEAVY}.`));
    if (reveal && moving()) { ev.classList.remove("lk-shock"); void ev.offsetWidth; ev.classList.add("lk-shock"); setTimeout(() => ev.classList.remove("lk-shock"), 1600); }
  }
}

// the moment: a rare one says so beside its age, and a very high stakes moment has an ember edge
function weighMoment(h) {
  const cp = h && h.cp; if (!cp) return;
  tableEl.classList.remove("lk-heavy", "lk-honour");
  tableEl.classList.toggle("lk-stakes3", cp.stake_word === "very high");
  const kick = tableEl.querySelector(".evh .kick"); if (!kick || kick.querySelector(".lk-rarek")) return;
  const i = bookInfo("s|" + cp.title); if (!i || !isRare(i.sh)) return;
  kick.insertAdjacentHTML("beforeend", ` <span class="lk-rarek">${ic("star")}rare · ${esc(oneIn(i.sh))}</span>`);
  setTip(kick.querySelector(".lk-rarek"), () => tipBox(`${ic("star")} A rare moment`, "", [["Lives that meet it", i.sh === 0 ? `none of ${livesN().toLocaleString()}` : `about ${oneIn(i.sh)}`]], RAR_FOOT + " It is kept in your Book once met."));
}

// the story: weight by what it is and how far it moved them; a fresh loss tolls once on the stage
function weighFeed(items, live) {
  let toll = false;
  for (const it of items) {
    const el = it && document.getElementById("it" + it._i); if (!el || el._lkw) continue; el._lkw = 1;
    if (it.tag === "death" || it.tag === "loss") { el.classList.add("lk-grave"); toll = true; }
    else if (BIG_TAGS.has(it.tag) || (it.tag !== "choice" && maxMove(it.dw) >= 3)) el.classList.add("lk-big");
    else if (it.tag === "commitment" && it.what === "start") el.classList.add("lk-mile");
    if (it.tag === "role") {
      const hn = honour(it);
      if (hn.t < 0) el.classList.add("lk-sombre");
      else if (hn.t >= 2) {
        el.classList.add("lk-hon", "t" + hn.t);
        el.insertAdjacentHTML("beforeend", `<span class="lk-mk" data-lkmk="${it._i}">${sealHTML(roleIconOf(it), "xs")}${hn.sh != null ? esc(oneIn(hn.sh)) : "hard-won"}</span>`);
        setTip(el.querySelector(".lk-mk"), () => tipBox(`${ic(roleIconOf(it))} ${hn.t >= 3 ? "A rare title" : it.title ? "An earned title" : "A hard-won perk"}`, "", [],
          hn.sh != null ? `${esc(cap(rarityWord(hn.sh)))}. ${RAR_FOOT}` : "An act of theirs earned it, not the years."));
      }
    }
    const si = it.sit && it.tag !== "role" ? bookInfo("s|" + it.sit) : null;
    if (si && isRare(si.sh) && !el.querySelector(".lk-rarem")) {
      el.insertAdjacentHTML("beforeend", `<span class="lk-rarem">${ic("star")}${esc(oneIn(si.sh))}</span>`);
      setTip(el.querySelector(".lk-rarem"), () => tipBox(`${ic("star")} A rare moment`, esc(cap(it.sit)), [["Lives that meet it", si.sh === 0 ? `none of ${livesN().toLocaleString()}` : `about ${oneIn(si.sh)}`]], RAR_FOOT));
    }
  }
  if (toll && live && lively()) { stageEl.classList.remove("lk-toll"); void stageEl.offsetWidth; stageEl.classList.add("lk-toll"); setTimeout(() => stageEl.classList.remove("lk-toll"), 2600); }
}

// the panel: a new title or perk shines once (a few seconds, carried across the panel's redraws), a rare title keeps a star
const SHINE_MS = 5200, shine = new Map();
let heldKey = "", held = null;
function honourHud(L) {
  const k = lifeKey(L), all = [].concat(...(L.titles || []).map((t) => t.named || []), L.perks || [], L.statuses || []).filter(Boolean);
  if (heldKey !== k) shine.clear();
  else if (held && hud && !hud.replay && !hud.loaded) for (const d of all) if (!held.has(d.name) && !(d.years >= 1) && honour({ ...d, up: true }).t >= 1) shine.set(d.name, now());
  held = new Set(all.map((d) => d.name)); heldKey = k;
  const mark = (el, d) => {
    if (!el || !d) return;
    const hn = honour({ ...d, up: true });
    if (d.title && hn.t >= 3 && !el.querySelector(".lk-hstar")) {
      (el.querySelector(".tn") || el).insertAdjacentHTML("beforeend", `<i class="lk-hstar">${ic("star")}</i>`);
      addTip(el, () => `<p class="lk-tiprar">${ic("star")} ${esc(cap(rarityWord(hn.sh)))}. ${RAR_FOOT}</p>`);
    }
    const t0 = shine.get(d.name); if (t0 == null) return;
    const age = now() - t0;
    if (age >= SHINE_MS) { shine.delete(d.name); return; }
    el.classList.add("lk-new", "t" + Math.max(1, hn.t)); el.style.setProperty("--lk-sd", -Math.round(age) + "ms");
  };
  hudEl.querySelectorAll(".trow[data-sock]").forEach((el) => { const t = (L.titles || []).find((x) => x.kind === el.dataset.sock); mark(el, t && (t.named || [])[0]); });
  hudEl.querySelectorAll(".perk[data-perk]").forEach((el) => mark(el, (L.perks || [])[+el.dataset.perk]));
  hudEl.querySelectorAll(".perk.stat[data-rs]").forEach((el) => mark(el, (L.statuses || [])[+el.dataset.rs]));
}

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
