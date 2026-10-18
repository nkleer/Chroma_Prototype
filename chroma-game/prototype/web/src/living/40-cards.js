"use strict";
/* ---------------- the Living HUD: the cards (v23 row V4; plan: the Living HUD in v23, decisions 1, 7 and 8) ----------------
   Today's moment window keeps its layout, order, printed numbers, folds, reading strip, buttons, outcome text and rename
   box (decision 7); this piece only adds classes and children to it, ported in spirit from the showcase's cards.js:
   - Weight: a way against who they are looks heavier. Each card .opt gets lv-<weight> classes and three layers of its
     own, all inside it and under its words: .lv-lift (the shading and shadow that say how it sits: a light card floats
     and catches the light under the pointer, a heavy one sags into the table with a tight dark contact and heavier ink),
     .lv-hold (the hold's ink wash) and, on their own pick, .lv-halo (a gold breath). The card and the window never move
     for it, and nothing reaches past a card. Cards are dressed through a MutationObserver on #table, as the ink look's
     tagOptions is, so the folds that setOOR and openOOR (and clarity) rebuild or move are dressed too.
   - The hold (decision 1): while this piece is mounted, #table carries data-hold="on" and each card data-hold="<ms>", the
     time to hold it to push: 0 for their own pick (a click acts at once), from 450 ms for a way they would go with to
     1600 ms for one out of reach and against who they are. A press fills the card (its ink wash and a ring round its
     number) and pushes when the time is reached while still pressed, through send() as a click would (so the choosing
     beat runs as today); letting go early, or leaving the card, takes it back. A click without a finished hold does not
     push; a click with no pointer behind it (Enter or Space on a focused card) acts at once, as do the number keys,
     Enter, the lean and "Let them choose", which never reach this guard. On a touch screen a tap reads the card as today
     and "Push them to this" pushes; a second tap reads again; a touch held for the card's time pushes. The pointerup and
     click after a finished hold are swallowed; on cards the long-press menu and text selection are off.
   - The hint under the question names the hold (the renderTable hook).
   - One turn-over (decision 8): today's choosing beat (markChoosing, flyUp, flipFlyer, lockInputs, the reveal) is the
     only one; at the outcome the moment's picture refocuses: what they hoped and what happened, two copies of it, slide
     together into one sharp image (with a jolt when it went worse than they expected, a bloom when better, a settle when
     as expected). The renderResolution hook plays it once for each outcome, never after a load; a lean turns no card.
   Motion: calm is slower and gentler, off draws every state as it is (the hold's fill in still steps, no refocus).
   Not taken from the showcase: its own window and cards, its LIGHTS (the ink look lights the picture from LK_LIGHTS),
   its document keys (1-9, 0, -, =), its demos and test hooks. */
(() => {
const CH = window.CH; if (!CH || !CH.piece) return;

/* ---------------- how they take a way: its weight and its hold ---------------- */
// the hold in ms by how they take it (06-moment.js ACC_WORD); out of reach is heavier whatever they feel about it
const HOLD = { "their own pick": 0, "would go with it": 450, "okay with it": 600, reluctant: 900, "against it": 1250 };
const WEIGHT = { "their own pick": 0, "would go with it": 0.12, "okay with it": 0.3, reluctant: 0.62, "against it": 0.88 };
const CLS = { "their own pick": "own", "would go with it": "go", "okay with it": "ok", reluctant: "rel", "against it": "against" };
const FAR_MS = 350, MAX_MS = 1600;
// a finger on their own pick still holds a moment, so a tap reads it as today (a tap is shorter)
const TOUCH_OWN = 200;
const accOf = (o) => (o.own ? "their own pick" : HOLD[o.accept] != null ? o.accept : "okay with it");
const far = (o) => o.status === "out of reach";
const holdOf = (o) => { const a = accOf(o); return a === "their own pick" ? 0 : Math.min(MAX_MS, HOLD[a] + (far(o) ? FAR_MS : 0)); };
const weightOf = (o) => Math.min(1, WEIGHT[accOf(o)] + (far(o) ? 0.15 : 0));
const inkOf = (o) => { const e = (o.ends && o.ends.length ? o.ends : o.means) || []; return e[0] ? CH.HUE.ink[e[0]] : "#3b2f20"; };
const HINT = { desk: "hover to read · hold, or press its number, to push", touch: "tap to read · hold or tap Push to push" };
const C = 2 * Math.PI * 22;            // the ring's length (r 22 in a 48 box round the 38 px roundel)
const RING = (ink) => `<svg class="lv-ring" viewBox="0 0 48 48" aria-hidden="true" style="--lv-ink:${ink}"><circle class="t" cx="24" cy="24" r="22"/><circle class="p" cx="24" cy="24" r="22" stroke-dasharray="${C.toFixed(1)}" stroke-dashoffset="${C.toFixed(1)}"/></svg>`;
const LAYERS = ["lv-lift", "lv-hold", "lv-halo", "lv-ring"];
const LV_CLS = ["lv", "lv-own", "lv-go", "lv-ok", "lv-rel", "lv-against", "lv-far", "lv-heavy", "lv-light", "lv-holding", "lv-held"];

let on = false, mo = null, offPick = null, lastPick = null, rfKey = "";
// the piece's own cost, for the frame budget (plan section 6): every entry point adds the time it took
let costMs = 0;
const timed = (f) => function (...a) { const t = performance.now(); try { return f.apply(this, a); } catch (e) { console.warn("living: cards", e); } finally { costMs += performance.now() - t; } };

/* ---------------- dressing the cards ---------------- */
function dress(b) {
  const cp = hud && hud.cp, o = cp && cp.options[+b.dataset.i]; if (!o) return;
  const a = accOf(o), k = weightOf(o), ms = holdOf(o), ink = inkOf(o);
  b.classList.add("lv", "lv-" + CLS[a]);
  if (far(o)) b.classList.add("lv-far");
  b.classList.add(k >= 0.6 ? "lv-heavy" : k <= 0.15 ? "lv-light" : "lv-mid");
  b.dataset.hold = String(ms);
  b.style.setProperty("--lv-k", k.toFixed(2)); b.style.setProperty("--lv-ink", ink);
  b.insertAdjacentHTML("afterbegin", `<span class="lv-lift" aria-hidden="true"></span><span class="lv-hold" aria-hidden="true"><i></i></span>${o.own ? '<span class="lv-halo" aria-hidden="true"></span>' : ""}`);
  const oi = b.querySelector(":scope > .oi"); if (oi) oi.insertAdjacentHTML("beforeend", RING(ink));
}
const dressAll = () => { if (on && hud && hud.cp) tableEl.querySelectorAll(".opt[data-i]:not(.lv)").forEach(dress); };
function undress(b) {
  b.classList.remove(...LV_CLS, "lv-mid"); b.removeAttribute("data-hold");
  ["--lv-k", "--lv-ink", "--lv-ms", "--lv-gx", "--lv-gy"].forEach((p) => b.style.removeProperty(p));
  b.querySelectorAll(LAYERS.map((c) => "." + c).join(",")).forEach((x) => x.remove());
}
// the hint under the question names the hold (decision 1); taken back when the piece goes
function hint(back) {
  const s = tableEl.querySelector("#evOpts > .ask small"); if (!s) return;
  if (back) { if (s._lvWas != null) { s.textContent = s._lvWas; delete s._lvWas; } return; }
  const want = touchUI ? HINT.touch : HINT.desk;
  if (s.textContent !== want) { if (s._lvWas == null) s._lvWas = s.textContent; s.textContent = want; }
}

/* ---------------- the hold: one set of capture listeners on #table (and the document for the release) ---------------- */
let cur = null, swallow = null;
const motionOff = () => CH.motion() === "off";
const cardOf = (e) => { const b = e.target && e.target.closest ? e.target.closest(".opt[data-i]") : null; return b && tableEl.contains(b) ? b : null; };
function msFor(b, type) { const ms = +b.dataset.hold || 0; return type === "touch" ? Math.max(ms, TOUCH_OWN) : ms; }
function startFill(b, ms) {
  b.style.setProperty("--lv-ms", ms + "ms");
  void b.offsetWidth;                  // the fill starts from empty even when a hold was just taken back
  b.classList.add("lv-holding");
}
function stopFill(b, held) {
  b.classList.remove("lv-holding");
  if (held) { b.classList.add("lv-held"); const r = b.querySelector(".lv-ring"); if (r) r.classList.add("full"); }
}
const down = timed((e) => {
  if (!on) return;
  const b = cardOf(e); if (!b) return;
  if (e.pointerType === "mouse" && e.button !== 0) return;
  if (cur && (cur.b.isConnected && !cur.done && performance.now() - cur.t0 < cur.ms + 4000)) return;   // one hold at a time
  if (cur) cancel();
  if (b.disabled || busy || !hud || !hud.cp || evWrap.hidden) return;
  const ms = msFor(b, e.pointerType); if (!ms) return;   // their own pick under a mouse: the click acts at once
  cur = { b, id: e.pointerId, type: e.pointerType, t0: e.timeStamp || performance.now(), x: e.clientX, y: e.clientY, ms, key: lastCpKey, done: false };
  const c = cur; c.timer = setTimeout(timed(() => finish(c)), ms);
  startFill(b, ms);
});
function cancel() {
  const c = cur; cur = null; if (!c) return;
  clearTimeout(c.timer); if (!c.done) stopFill(c.b, false);
}
function finish(c) {
  if (!c || c !== cur || c.done) return;
  clearTimeout(c.timer);
  const o = hud && hud.cp && hud.cp.options[+c.b.dataset.i];
  if (!o || !c.b.isConnected || busy || lastCpKey !== c.key || evWrap.hidden) return cancel();
  c.done = true; cur = null; swallow = { id: c.id, until: performance.now() + 8000 };
  stopFill(c.b, true);
  send(o.own ? "" : String(o.n));      // as the card's own click would: markChoosing, the flyer, the reveal
}
const up = timed((e) => {
  if (cur && e.pointerId === cur.id) {
    // the time was reached while pressed (a late timer still counts); else letting go takes it back
    if (e.type === "pointerup" && (e.timeStamp || performance.now()) - cur.t0 >= cur.ms - 8) finish(cur); else cancel();
  }
  if (swallow && e.pointerId === swallow.id) { swallow.until = performance.now() + 700; swallow.id = null; if (e.type === "pointerup") e.stopPropagation(); }
});
const move = timed((e) => {
  if (!cur || e.pointerId !== cur.id) return;
  if (cur.type === "mouse") { if (!cur.b.contains(e.target)) cancel(); return; }   // the mouse left the card
  if (Math.hypot(e.clientX - cur.x, e.clientY - cur.y) > 12) cancel();             // a finger that scrolls
});
const click = timed((e) => {
  if (!on) return;
  const b = cardOf(e); if (!b) return;
  const block = () => {
    e.preventDefault(); e.stopImmediatePropagation();
    // what a click outside them does today (04-line.js): close the drawer and the menu
    if (hudEl.classList.contains("open")) closeHud();
    if (menuOpen) setMenu(false);
  };
  if (swallow && performance.now() < swallow.until) return block();               // the click after a finished hold
  if (e.detail === 0) return;                                                      // Enter or Space on a focused card
  if (touchUI) { selected = null; return; }                                       // a tap reads, a second tap reads again
  if (b.dataset.hold === "0") return;                                              // their own pick: a click acts at once
  block();                                                                         // a click is not a hold
});
const menu = timed((e) => { if (on && cardOf(e)) e.preventDefault(); });
// a light card catches the light where the pointer is (mouse only; still with motion off)
let gxRaf = 0, gxEv = null;
const sheen = timed((e) => {
  if (e.pointerType !== "mouse" || motionOff()) return;
  gxEv = e; if (gxRaf) return;
  gxRaf = requestAnimationFrame(timed(() => {
    gxRaf = 0; const ev = gxEv, b = ev && cardOf(ev); if (!b || !b.classList.contains("lv")) return;
    const r = b.getBoundingClientRect(); if (!r.width) return;
    b.style.setProperty("--lv-gx", (((ev.clientX - r.left) / r.width) * 100).toFixed(0) + "%");
    b.style.setProperty("--lv-gy", (((ev.clientY - r.top) / r.height) * 100).toFixed(0) + "%");
  }));
});
const LISTEN = [[tableEl, "pointerdown", down], [tableEl, "click", click], [tableEl, "contextmenu", menu], [tableEl, "pointermove", sheen, { passive: true }],
  [document, "pointerup", up], [document, "pointercancel", up], [document, "pointermove", move, { passive: true }]];

/* ---------------- the refocus: what they hoped and what happened slide into one sharp picture ---------------- */
// how it landed against what they expected (the outcome's surprise; else the picked card's own misread)
function kindOf(res) {
  const s = res && res.surprise;
  if (s === "better" || s === "worse") return s;
  if (s === "as expected") return "expected";
  const m = lastPick && lastPick.reality && lastPick.reality.misread;
  return m === "hopeful" ? "worse" : m === "doubtful" ? "better" : "expected";
}
// how far apart the two pictures start: how far the outcome was from how sure they felt
const gapOf = (res) => CH.clamp(res.worked ? 1 - (res.felt == null ? 0.6 : res.felt) : res.felt == null ? 0.6 : res.felt);
// the hoped copy: rosier than life when it went worse, greyer and dimmer when it went better, nearly true otherwise
const HOPED = { worse: "blur(3px) saturate(1.3) sepia(.28) brightness(1.1)", better: "blur(3px) grayscale(.72) brightness(.86)", expected: "blur(2.5px) brightness(1.04)" };
function refocus(res, reveal) {
  const m = CH.motion(); if (m === "off") return;
  const art = tableEl.querySelector(".evart"), img = art && art.querySelector(":scope > img"); if (!img) return;
  let gone = false; const t = setTimeout(() => { gone = true; }, 1500);
  const go = timed(() => { clearTimeout(t); if (!gone && img.isConnected && img.naturalWidth && on) play(art, img, res, m, reveal); });
  if (img.complete) go(); else img.addEventListener("load", go, { once: true });
}
function play(art, img, res, m, reveal) {
  const W = art.clientWidth, H = art.clientHeight; if (!W || !H || !art.animate) return;
  art.querySelectorAll(".lv-rf").forEach((x) => x.remove());
  const kind = kindOf(res), calm = m === "calm", s = calm ? 1.6 : 1;
  const D = W * (0.02 + 0.07 * gapOf(res)) * (calm ? 0.6 : 1), Z = 1 + (2.2 * D) / W;
  const base = getComputedStyle(img).transform, B = base && base !== "none" ? " " + base : "";
  const box = document.createElement("span"); box.className = "lv-rf " + kind; box.setAttribute("aria-hidden", "true");
  const src = img.currentSrc || img.src;
  box.innerHTML = `<img class="soft" alt=""><img class="hoped" alt="" style="filter:${HOPED[kind]}"><img class="sharp" alt=""><i class="snap"></i>`;
  box.querySelectorAll("img").forEach((x) => { x._lk = 1; x.src = src; });   // _lk: the ink look's engravings leave the copies alone
  img.after(box);
  const [soft, hoped, sharp] = box.querySelectorAll("img"), snap = box.querySelector(".snap");
  const at = (dx, dy, z) => `translate(${dx.toFixed(1)}px, ${dy.toFixed(1)}px)${B} scale(${z.toFixed(4)})`;
  const delay = reveal && flyer ? 240 : 60, dur = 1000 * s, ease = "cubic-bezier(.6, 0, .9, .4)";   // accelerating into place: a snap
  const o = { duration: dur, delay, easing: ease, fill: "both" };
  soft.animate([{ transform: at(D, 0.32 * D, Z) }, { transform: at(0, 0, 1) }], o);
  sharp.animate([{ transform: at(D, 0.32 * D, Z), opacity: 0 }, { transform: at(0, 0, 1), opacity: 1 }], o);
  hoped.animate([{ transform: at(-0.9 * D, -0.32 * D, Z), opacity: 0.55 }, { transform: at(0, 0, 1), opacity: 0 }], { ...o, easing: "cubic-bezier(.5, 0, .8, .6)" });
  const t1 = delay + dur, after = { delay: t1, fill: "forwards" };   // the snap's light waits, unseen, for the snap
  if (kind === "worse") {
    if (!calm) box.animate([0, 6, -5, 3.5, -2, 1, 0].map((j) => ({ transform: `translate(${j}px, ${(j * 0.25).toFixed(2)}px)` })), { duration: 360, ...after, fill: "none" });
    snap.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 340 * s, ...after });
  } else if (kind === "better") snap.animate([{ opacity: 0.85, transform: "scale(.45)" }, { opacity: 0, transform: "scale(1.5)" }], { duration: 1100 * s, easing: "cubic-bezier(.2, .7, .3, 1)", ...after });
  else snap.animate([{ opacity: 0.7, transform: "scale(1.16)" }, { opacity: 0, transform: "scale(1)" }], { duration: 450 * s, easing: "cubic-bezier(.2, .7, .3, 1)", ...after });
  const end = t1 + (kind === "better" ? 1100 : kind === "worse" ? 360 : 450) * s;
  const out = box.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 180, delay: end, fill: "forwards" });
  out.onfinish = () => box.remove();
  setTimeout(() => box.remove(), end + 1200);
}

/* ---------------- the piece ---------------- */
CH.piece("cards", {
  order: 40,
  mount: timed(function () {
    if (!tableEl) return false;
    on = true; tableEl.dataset.hold = "on";
    LISTEN.forEach(([el, ev, f, opt]) => el.addEventListener(ev, f, opt ? { capture: true, ...opt } : true));
    mo = new MutationObserver(timed((rs) => { if (rs.some((r) => r.addedNodes.length)) dressAll(); }));
    mo.observe(tableEl, { childList: true, subtree: true });
    offPick = CH.on("pick", (x) => { lastPick = x && x.o; });
    dressAll(); hint(false);
    return true;
  }),
  destroy: timed(function () {
    on = false; cancel(); swallow = null;
    LISTEN.forEach(([el, ev, f, opt]) => el.removeEventListener(ev, f, opt ? { capture: true, ...opt } : true));
    if (mo) mo.disconnect(); mo = null;
    if (offPick) offPick(); offPick = null;
    delete tableEl.dataset.hold;
    tableEl.querySelectorAll(".opt.lv").forEach(undress);
    tableEl.querySelectorAll(".lv-rf").forEach((x) => x.remove());
    hint(true);
  }),
  hooks: {
    renderTable: timed(function () {
      if (cur && (!cur.b.isConnected || cur.key !== lastCpKey)) cancel();
      dressAll(); hint(false);
    }),
    renderResolution: timed(function (h, reveal) {
      if (!h || !h.res || h.replay || h.loaded || evWrap.hidden) return;
      const key = "res|" + h.res.age + "|" + h.res.title; if (key === rfKey) return;
      rfKey = key; refocus(h.res, !!reveal);
    }),
  },
  // the time this piece has spent, in ms since the page started (the frame-cost check reads it each frame)
  cost: () => costMs,
});
})();
