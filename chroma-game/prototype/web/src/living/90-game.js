"use strict";
/* ---------------- the Living HUD on the game page (in place of the showcase's shell.js) ----------------
   A layer over the page, built like the ink look and clarity: it wraps a few page functions, runs each original first and
   changes no life. It loads last, so it wraps the outermost (clarity's and look's) versions. A fault here never stops the
   game: every step after an original runs inside safe().
   - The switch: a "Living HUD" row in the Table menu, under the ink look only, stored in this browser as chroma.living,
     on unless turned off; no key (l belongs to the game). Turned off, or under the classic look, html[data-living] is
     "off", every piece is taken down and today's HUD, line and moment are drawn again: the screen is today's.
   - The life (CH.life) and its stop log, recorded after each state the page applies, during a load's replay too: a stop
     at each new moment, each new outcome, each new whole year of age and the end, with what only the states carry (the
     titles, perks, plans and push counters over time, a moment's tier and stakes, an outcome's verdict). A push's verdict
     is its own outcome's hindsight. Never saved: a load replays the life, so the log comes back as it was.
   - The state S, a new object at each update (hud.life is never changed: the page reads its want, res and pushes).
   - The pieces (CH.piece, living/00-core.js): mounted while the Living HUD is on, updated at most once a frame and 280 ms
     apart while time runs, told of the page's own redraws through thin hooks. Each runs as itself (CH.as), so the core
     times its frames and guards them piece by piece (CH.cost); html[data-lv-pieces] names the pieces standing, and the
     ink look's own ink (its drops into the wheel and the rings and points at the wheel's orbs, the river's light) gives
     way where a piece takes its place (living/90-game.css; the story's wet ink gives way in living/50-story.css).
   - The Table menu: the Living HUD row, and with the Living HUD on the Motion and Look rows' tooltips say what calm
     means now (decision 2: slower and fewer).
   - The events: "moment" and "outcome" when the page shows one (an outcome after its reveal beat), "pick" when a card is
     sent, "living" while time runs. During a load's replay the pieces stay still and nothing is told; then one quiet
     update, and the moment or outcome the life is back at is told once, quiet. */
(() => {
const CH = window.CH; if (!CH) return;
const root = document.documentElement;
const keep = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };
const read = (k, d) => { try { return localStorage.getItem(k) || d; } catch (_) { return d; } };
const safe = (where, f) => { try { return f(); } catch (e) { console.error("living: " + where, e); } };
const now = () => performance.now();

/* ---------------- the switch ---------------- */
let living = read("chroma.living", "on") !== "off";
const ink = () => root.dataset.look === "ink";                 // look.js sets it before this script runs
const active = () => living && ink();
const setRoot = () => { const v = active() ? "on" : "off"; if (root.dataset.living !== v) root.dataset.living = v; };
setRoot();

/* ---------------- the life and its stop log ---------------- */
let logKey = "", logYear = null, openCp = null, lastDoors = null;
// a new CH.life for each life and each load (resetChron runs for both, and at a birth line): the page's own story items
// (ITEMS, the same objects), the river and the identity names as the latest state sends them, and the stops
function newLife() {
  CH.life = { name: "", setting: "", guilds: {}, river: [], items: ITEMS, portraits: (typeof PICS === "object" && PICS.portrait) || null,
    stops: [], ages: [], pushes: [], end_age: Infinity, rev: 0, bytes: 0 };
  logKey = ""; logYear = null; openCp = null; lastDoors = null; evKey = "";
}
// what a stop keeps of the life: what the river, the window and the story read over time (1 to 2 KB)
const slim = (L) => ({
  label: L.label || "", guild: L.guild || "", magic: L.magic || "", stage: L.stage || "", voice: (L.voice || []).slice(),
  voice_label: L.voice_label || "", w: L.w.slice(), readiness: L.dyn ? L.dyn.readiness : null,
  titles: (L.titles || []).map((t) => ({ kind: t.kind, years: t.years, invested: t.invested, named: (t.named || []).map((x) => ({ name: x.name, say: x.say, years: x.years })),
    // river (V3): a role's colours tint its stratum and a quarrel cracks it
    expects: t.expects || "", clash: !!t.clash })),
  perks: (L.perks || []).map((p) => ({ name: p.name, say: p.say, kind: p.kind, ways: p.ways, state: p.state, years: p.years })),
  goals: (L.goals || []).map((g) => ({ id: g.id, kind: g.kind, name: g.name, colors: g.colors, strength: g.strength, progress: g.progress })),
  pushes: L.pushes ? { forced: L.pushes.forced, accepted: L.pushes.accepted, resented: L.pushes.resented, passed: (L.pushes.passed || []).slice() } : null,
});
function addStop(kind, h) {
  const life = CH.life, L = h.life;
  const st = { i: life.stops.length, kind, age: L.age, life: slim(L) };
  if (kind === "cp") {
    const c = h.cp, a = c.art || {};
    Object.assign(st, { cp: { age: c.age, title: c.title, tier: a.tier || "", stakes: c.stakes ?? null, stake_word: c.stake_word || "" }, resi: -1 });
  } else if (kind === "res") {
    const r = h.res, verdict = (r.hindsight && r.hindsight.kind) || "none";
    st.res = { age: r.age, title: r.title, act: r.act, colors: r.colors || "", pushed: !!r.pushed, rel: r.rel ?? 0, worked: !!r.worked,
      dw: r.dw ? r.dw.slice() : null, verdict };
    // the moment it answers: the open one of this week with the same title (a year may stand between them)
    st.cpi = -1;
    for (let j = life.stops.length - 1; j >= 0; j--) {
      const s = life.stops[j]; if (s.kind === "res") break;
      if (s.kind === "cp" && s.resi < 0 && s.cp.title === r.title && Math.abs(s.cp.age - r.age) < 0.15) { st.cpi = j; s.resi = st.i; break; }
    }
    // a push and how they took it, from its own outcome (hindsight is judged at the outcome itself, game_life.py)
    if (r.pushed) life.pushes.push({ age: r.age, title: r.title, act: r.act, colors: r.colors || "", rel: r.rel ?? 0, verdict,
      accepted: verdict === "accepted", resented: verdict === "resented", stop: st.i, cpi: st.cpi });
  }
  life.stops.push(st); life.ages.push(st.age); life.rev++;
  life.bytes += JSON.stringify(st).length;
}
// after each state, replays included. The moment and outcome key is the autosave's (13-state.js), without its
// "not busy, not replaying": a waiting moment that is sent again is one stop
function record(h) {
  const L = h.life, life = CH.life;
  if (!L || !L.w || !["play", "over"].includes(h.mode)) return;
  if (L.name) life.name = L.name;
  if (L.setting) life.setting = L.setting;
  if (L.guilds) life.guilds = L.guilds;
  if (L.river) life.river = L.river;
  const yr = Math.floor(L.age + 1e-9);
  if (logYear == null || yr > logYear) { logYear = yr; addStop("year", h); }
  if (h.cp) openCp = h.cp;
  const k = h.mode === "play" && (h.cp || h.res) ? (h.cp ? "cp" + h.cp.age + h.cp.title : "res" + h.res.age + h.res.title) : "";
  if (k && k !== logKey) { logKey = k; addStop(h.cp ? "cp" : "res", h); }
  if (h.mode === "over" && life.end_age === Infinity) { life.end_age = L.age; addStop("over", h); }
}

/* ---------------- the state S ---------------- */
const Z5 = [0, 0, 0, 0, 0];
// how open each colour's ways are (accelerator = readiness x belief x doors, explain.dynamics); held at the last good
// value while readiness x belief is too small to divide by, and said as "about" (S.doorsAbout)
function doorsOf(L) {
  const acc = L.acc || Z5, bel = L.belief || Z5, rd = L.dyn && L.dyn.readiness != null ? L.dyn.readiness : 0.5, about = [];
  const d = CH.COLORS.map((c, k) => {
    const div = rd * ((bel[k] ?? 0.5) / 0.5);
    about[k] = div < 0.02;
    return about[k] && lastDoors ? lastDoors[k] : CH.clamp((acc[k] || 0) / Math.max(1e-3, div), 0, 1.5);
  });
  lastDoors = d;
  return [d, about];
}
// how wet the ink is when the sky (atmos, CH.ink.wetOf) is not there: readiness, and an open window of change
const wetOf = (S) => { const y = S.dyn || {}; return CH.clamp((y.readiness ?? 0.5) + (y.window ? 0.35 * CH.clamp(y.openness || 0) : 0)); };
function stateOf(h) {
  const L = h && h.life; if (!L || !L.w) return null;
  const life = CH.life, S = Object.assign({}, L);
  // hud.life's own want (pent-up wanting), res (their means) and pushes (the push counters) stay there; S has its own
  S.wantQ = L.want; S.means = L.res; S.pushCounts = L.pushes;
  S.want = L.w.map((v, k) => Math.max(0.01, v + ((L.demand || Z5)[k] || 0)));
  S.hold = (L.inertia || Z5).map((v) => v + 0.2);
  [S.doors, S.doorsAbout] = doorsOf(L);
  S.items = ITEMS; S.pushes = life.pushes; S.river = L.river || [];
  S.moment = h.cp || (h.res && openCp && openCp.title === h.res.title ? openCp : null);   // an outcome keeps its moment
  S.res = h.res || null; S.waiting = !!h.cp;
  S.cut = Infinity; S.untold = []; S.pre = false; S.t = 0;                               // live, everything here is told
  S.stop = life.stops.length - 1; S.rev = life.rev;
  S.over = h.mode === "over"; S.end_age = life.end_age;
  S.wet = CH.ink && CH.ink.wetOf ? CH.ink.wetOf(S) : wetOf(S);
  return S;
}

/* ---------------- the pieces ---------------- */
// Each piece's mount, update, hooks and destroy run as that piece (CH.as), so its frames and handlers are its own (the
// per-piece guard and CH.cost, living/00-core.js). The names of the pieces standing are kept on html[data-lv-pieces], so
// the ink look's own ink gives way exactly where a piece takes its place (living/90-game.css).
const mounted = new Map();
const ctx = { state: () => stateOf(hud) };
const markPieces = () => { const v = [...mounted.keys()].join(" "); if (v) { if (root.dataset.lvPieces !== v) root.dataset.lvPieces = v; } else delete root.dataset.lvPieces; };
function mountOne(p) {
  if (!p || mounted.has(p.name)) return;
  let ok = false;
  try { ok = CH.as(p.name, () => (p.mount ? p.mount(ctx) !== false : true)); } catch (e) { console.warn(`living: ${p.name} did not start, today's piece stays`, e); }
  if (ok) { mounted.set(p.name, p); markPieces(); }
}
const mountAll = () => [...CH.pieces.values()].sort((a, b) => a.order - b.order).forEach(mountOne);
function destroyOne(p) { mounted.delete(p.name); markPieces(); safe(p.name + " destroy", () => CH.as(p.name, () => p.destroy && p.destroy())); }
const destroyAll = () => [...mounted.values()].reverse().forEach(destroyOne);
// the thin hooks: each mounted piece's hook of that name, after the page function, with its arguments
function hook(name, args) {
  let skip = false;
  for (const p of [...mounted.values()]) {
    const f = p.hooks && p.hooks[name];
    if (typeof f === "function" && safe(p.name + " " + name, () => CH.as(p.name, () => f.apply(p, args))) === true) skip = true;
  }
  return skip;
}
// a piece registered after the page started (or again, replacing itself)
CH.on("piece", (name) => safe("piece", () => {
  const p = CH.pieces.get(name), was = mounted.get(name);
  if (was && was !== p) destroyOne(was);
  if (!wasActive) return;
  mountOne(p);
  if (hud && hud.life && hud.life.w && !hud.replay) later({ quiet: true });
}));

/* ---------------- updates: at most once a frame, and 280 ms apart while time runs (as the page's own HUD) ---------------- */
let updAt = 0, updRaf = 0, updT = 0, updHow = null, frames = [];
function later(how) {
  updHow = updHow ? { quiet: updHow.quiet || !!how.quiet, loaded: updHow.loaded || !!how.loaded } : { quiet: !!how.quiet, loaded: !!how.loaded };
  if (updRaf || updT) return;
  const wait = busy ? 280 - (now() - updAt) : 0;
  if (wait > 0) updT = setTimeout(() => { updT = 0; updRaf = requestAnimationFrame(update); }, wait);
  else updRaf = requestAnimationFrame(update);
}
function update() {
  updRaf = 0; updAt = now();
  // how: quiet (no arrival to play: the update after a load, the years before the player takes over), loaded, and the
  // weekly frames (05-hud.js frameOf) the states brought since the last update
  const how = Object.assign({ frames }, updHow); updHow = null; frames = [];
  if (!mounted.size || !hud || hud.replay) return;
  const S = stateOf(hud); if (!S) return;
  for (const p of [...mounted.values()]) {
    if (!p.update) continue;
    const t = now(); safe(p.name + " update", () => CH.as(p.name, () => p.update(S, how))); CH.cost.note(p.name, now() - t);
  }
}

/* ---------------- events ---------------- */
let inApply = 0, queued = [], evKey = "", wasLiving = false;
// raised inside applyState, an event waits until the stop log has the state; the update after a load is quiet
function raise(x) { x.quiet = !!(inApply && hud && hud.loaded); if (inApply) queued.push(x); else fire(x, null); }
function fire(x, S) {
  if (x.ev === "living") return CH.emit("living", x.on);
  S = S || stateOf(hud); if (!S) return;
  CH.emit(x.ev, Object.assign({ S, quiet: x.quiet }, x.data));
}
// the page showed a new moment or outcome (lastCpKey changed and the window is up); a replay clears lastCpKey, so the one
// a load comes back to is told once
function noteKey() {
  if (!lastCpKey) { evKey = ""; return; }
  if (lastCpKey === evKey || evWrap.hidden) return;
  evKey = lastCpKey;
  if (!active() || !hud || hud.replay) return;
  const res = lastCpKey.startsWith("res|");
  raise({ ev: res ? "outcome" : "moment", data: res ? { res: hud.res } : { cp: hud.cp } });
}

/* ---------------- the wrappers ---------------- */
const _applyState = applyState;
applyState = function (m) {
  inApply++;
  try { return _applyState(m); } finally { inApply--; safe("state", afterState); }
};
function afterState() {
  const h = hud; if (!h) return;
  if (CH.life.items !== ITEMS) CH.life.items = ITEMS;          // resetChron replaces the array
  record(h);
  const evs = queued; queued = [];
  if (!active() || h.replay) return;                           // a load's replay: still and silent
  const lv = !!(busy && h.mode === "play" && h.job === "run");
  if (lv !== wasLiving) { wasLiving = lv; evs.unshift({ ev: "living", on: lv }); }
  if (h.trace && h.trace.length) { frames.push(...h.trace.map(frameOf)); if (frames.length > 3000) frames.splice(0, frames.length - 3000); }
  if (h.life && h.life.w) later({ quiet: !!h.loaded || h.job === "past", loaded: !!h.loaded });
  if (evs.length) { const S = stateOf(h); evs.forEach((x) => safe(x.ev, () => fire(x, S))); }
}
const _resetChron = resetChron;
resetChron = function () { _resetChron(); safe("reset", newLife); };
const _renderTable = renderTable;
renderTable = function (h) { _renderTable(h); safe("moment", noteKey); if (mounted.size) hook("renderTable", [h]); };
const _renderResolution = renderResolution;
renderResolution = function (h, reveal) { _renderResolution(h, reveal); safe("outcome", noteKey); if (mounted.size) hook("renderResolution", [h, reveal]); };
const _send = send;
send = function (text) {
  const was = busy, cp = hud && hud.cp;
  const r = _send(text);
  safe("pick", () => {
    if (was || !busy || sentFrom !== "cp" || !cp || !active()) return;
    const o = text === "" ? cp.options.find((x) => x.own) : cp.options.find((x) => String(x.n) === String(text));
    raise({ ev: "pick", data: { cp, o: o || null, text } });
  });
  return r;
};
const _ilStep = ilStep;
ilStep = function (t) { const r = _ilStep(t); if (mounted.size) hook("ilStep", [t]); return r; };
const _animSpider = animSpider;
animSpider = function (svg, fs, ms, base, done) {
  // a living piece that shows the wheel's motion itself skips it: the wheel jumps to its last frame, so it is right
  // again the moment the Living HUD is off
  if (mounted.size && fs && fs.length > 1 && hook("animSpider", [svg, fs, ms, base, done])) return _animSpider(svg, fs.slice(-1), 0, base, done);
  return _animSpider(svg, fs, ms, base, done);
};
const _renderHud = renderHud;
renderHud = function (L) { _renderHud(L); if (mounted.size) hook("renderHud", [L]); };
const _drawLine = drawLine;
drawLine = function () { _drawLine(); if (mounted.size) hook("drawLine", []); };
const _renderReview = renderReview;
renderReview = function (h) { _renderReview(h); if (mounted.size) hook("renderReview", [h]); };
const _renderTools = renderTools;
renderTools = function (h) { _renderTools(h); safe("menu", addRow); safe("menu words", reword); if (mounted.size) hook("renderTools", [h]); };

/* ---------------- the Table menu: the Living HUD row, after the ink look's Motion and Look ---------------- */
const rowTip = () => tipBox(`${ic("sprout")} Living HUD: ${living ? "on" : "off"}`, "", [],
  "With the ink look only. The night sky moves with their mood, their five colors show as a living star, the life line flows as a river, you hold a card to push them (longer when it goes against who they are), the story is written in the hand of the voice telling it, and a small round window gains a pane for each year. Off shows the screen as it was; the life plays the same either way.");
// Decision 2: with the Living HUD on, calm motion means slower and fewer, and the Motion and Look rows (look.js) say so
// in their tooltips; with it off (or under the classic look) the ink look's own words come back. The page rebuilds the
// menu with each state, so each new row is reworded once.
const WORDS = {
  motion: (v) => tipBox(`${ic("burst")} Motion: ${v}`, "", [],
    "How much moves: full (the sky, the star, the river and the window move, pictures breathe, ink soaks in, pages turn), calm (slower and fewer: the same changes, gentler, and fewer at once) or off (nothing moves; each change is drawn once). This device's reduced motion setting counts as off."),
  look: (v) => tipBox(`${ic("mask")} Look: ${v}`, "", [],
    "Ink (the engraved look; the Living HUD row below turns its living sky, star, river, cards, story and window on or off) or classic (the drawing of version 22, without the Living HUD). The helpers for choosing stay in both."),
};
function reword() {
  const pop = $("tPop"); if (!pop || typeof tips === "undefined") return;
  pop.querySelectorAll('[data-lk="motion"], [data-lk="look"]').forEach((b) => {
    const own = tips.get(b), mine = WORDS[b.dataset.lk];
    if (b._lvTip || !own || !mine) return;
    b._lvTip = 1;
    setTip(b, () => (active() ? mine(((b.querySelector(".v") || {}).textContent || "").trim()) : own()));
  });
}
function addRow() {
  const pop = $("tPop"); if (!pop) return;
  let b = pop.querySelector("[data-lv]");
  if (!ink()) { if (b) b.remove(); return; }                   // under the classic look the row is not there
  if (b) return;
  const at = pop.querySelector('[data-lk="look"]') || pop.querySelector('[data-page="i"]'); if (!at) return;
  at.insertAdjacentHTML("afterend", `<button class="mrow2" data-lv="living" role="menuitem">${ic("sprout")}<span class="t">Living HUD</span><span class="v">${living ? "on" : "off"}</span></button>`);
  b = pop.querySelector("[data-lv]");
  b.addEventListener("click", (e) => { e.stopPropagation(); turn(); b.querySelector(".v").textContent = living ? "on" : "off"; });
  setTip(b, rowTip);
}
function turn() { living = !living; keep("chroma.living", living ? "on" : "off"); safe("switch", sync); }
// on: mount the pieces and give them the life now. Off (or the classic look): take them down, then draw today's HUD,
// line and moment again, as the ink look does when it turns
let wasActive = false;
function sync() {
  setRoot(); addRow();
  const a = active(); if (a === wasActive) return;
  wasActive = a;
  if (a) { mountAll(); if (hud && hud.life && hud.life.w && !hud.replay) later({ quiet: true }); return; }
  destroyAll(); frames = [];
  if (!hud) return;
  if (hud.life && hud.life.w && !IL.on) renderHud(hud.life);
  drawLine();
  if (!IL.on) renderTable(hud);
}
// the look turned (or the motion, or this switch): the root, the row and the pieces follow
CH.on("motion", () => safe("look", sync));
newLife();
sync();
})();
