"use strict";
/* ---------------- the Living HUD: the shared beat (plan step 9; the showcase's conductor, shell.js 243-280) ----------------
   One beat across the screen, so the pieces answer the life together. It only plays short Web Animations (opacity, scale,
   text-shadow and filter: never a layout property) on the page's own elements and the pieces' hosts, and changes nothing
   else:
     a pick       the life line (#line) and the star's well hush for a breath (600 ms), as the choice is made
     an outcome   that moves their colours a point or more in all (sum of |dw|, in points of 100): the star's well swells and
                  settles, and the age in the top bar (#who .age) glints. The sky's own ripple for it is the sky's
                  (living/10-atmos.js); this beat does not repeat it.
     a year       each new whole year of age while the life is being lived: one 700 ms glint staggered across the age in
                  the top bar, the rim of the window's medallion (.hud-medal, living/60-window.js) and the story's newest
                  year (#feed .yr .yh .ag)
   Motion: full; calm (slower, and fewer: the year's glint every other year); off and reduced motion (nothing plays).
   Nothing plays during a load's replay or for the update after it (living/90-game.js tells nothing then, and that update
   is quiet), nor for the years lived before the player takes over. The star's well is whatever the star gives as
   CH.mods.star.well(), else its host in the Status panel; while the star is not there, the beat leaves it out.
   The page rebuilds the top bar with each state and the Status panel with the HUD, so a beat that is playing moves to
   the new element at the same point of its time. */
(() => {
const CH = window.CH; if (!CH || !CH.piece) return;
const EASE = "cubic-bezier(.3, .7, .2, 1)";
const motion = () => CH.motion();
const slow = () => (motion() === "calm" ? 1.6 : 1);
const shown = (el) => !!el && el.isConnected && el.getClientRects().length > 0;
// what has played, for the drivers (test/drive_living.js joint part)
const count = { pick: 0, outcome: 0, year: 0 };

/* ---------- the elements ---------- */
const STAR_HOST = "#hud .hud-well, #hud .lv-star, #hud .chs-star:not(.mini)";
function well() {
  const s = CH.mods.star;
  if (s && typeof s.well === "function") { try { const el = s.well(); if (el) return el; } catch (_) { /* the star's own fault: no well this time */ } }
  return document.querySelector(STAR_HOST);
}
const lineOf = () => document.getElementById("line");
const ageOf = () => document.querySelector("#who .age > b") || document.querySelector("#who .age");
const medalOf = () => document.querySelector("#hud .hud-medal");
function newestYear() {
  const feed = document.getElementById("feed"); if (!feed) return null;
  for (let el = feed.lastElementChild; el; el = el.previousElementSibling) if (el.classList.contains("yr")) return el.querySelector(":scope > .yh > .ag");
  return null;
}

/* ---------- a beat: one Web Animation on an element found again if the page rebuilds it while it plays ---------- */
const playing = new Set();
let mo = null;
function settle(b) { playing.delete(b); if (!playing.size && mo) mo.disconnect(); }
function start(b, el, at) {
  let a; try { a = el.animate(b.kf(el), b.opt); } catch (_) { settle(b); return; }
  a.id = "lv-beat-" + b.kind; if (at) a.currentTime = at;
  b.a = a; b.el = el;
  a.onfinish = a.oncancel = () => { if (b.a === a) settle(b); };
}
function rehome() {
  playing.forEach((b) => {
    if (!b.find || (b.el && b.el.isConnected)) return;
    const el = b.find(), t = b.a ? b.a.currentTime : 0;
    if (!el || el === b.el) { settle(b); return; }
    if (b.a) { b.a.onfinish = b.a.oncancel = null; b.a.cancel(); }
    start(b, el, t);
  });
}
function watch() {
  if (!("MutationObserver" in window)) return;
  if (!mo) mo = new MutationObserver(rehome);
  ["who", "hud"].forEach((id) => { const el = document.getElementById(id); if (el) mo.observe(el, { childList: true, subtree: true }); });
}
// kf(el) gives the keyframes for that element (read from its own style, so its own look is kept); o: duration, delay,
// easing. find: how to find the element again when the page rebuilds it (only for elements it rebuilds)
function beat(kind, el, kf, o, find) {
  if (!shown(el) || !el.animate) return;
  // the same beat still playing on it ends first, so its light is not read as the element's own
  playing.forEach((p) => { if (p.el === el && p.kf === kf) { if (p.a) { p.a.onfinish = p.a.oncancel = null; p.a.cancel(); } playing.delete(p); } });
  const k = slow();
  const b = { kind, kf, find, opt: Object.assign({ easing: EASE }, o, { duration: o.duration * k, delay: (o.delay || 0) * k }) };
  playing.add(b);
  start(b, el, 0);
  if (find && playing.has(b)) watch();
}

/* ---------- the keyframes ---------- */
// a hush: the element's own opacity, dimmed by a little less than a fifth and back
const hush = (el) => { const o = parseFloat(getComputedStyle(el).opacity); const v = isFinite(o) ? o : 1; return [{ opacity: v }, { opacity: v * 0.82 }, { opacity: v }]; };
// a swell: the individual scale property, so a transform the element has of its own is kept
const swell = () => [{ scale: "1" }, { scale: "1.035", offset: 0.35 }, { scale: "1" }];
// a glint of gold light on text, over the text's own shadow
const GOLD = "rgb(244 223 166 / ", GLOW = "rgb(255 246 214 / ";
const glint = (el) => { const s = getComputedStyle(el).textShadow, own = s && s !== "none" ? s + ", " : "";
  return [{ textShadow: `${own}0 0 0 ${GOLD}0), 0 0 0 ${GLOW}0)` }, { textShadow: `${own}0 0 14px ${GOLD}.95), 0 0 2px ${GLOW}.9)`, offset: 0.3 }, { textShadow: `${own}0 0 0 ${GOLD}0), 0 0 0 ${GLOW}0)` }]; };
// a rim of gold light round the medallion, over the element's own filter
const rim = (el) => { const f = getComputedStyle(el).filter, own = f && f !== "none" ? f + " " : "";
  return [{ filter: `${own}drop-shadow(0 0 0 ${GOLD}0))` }, { filter: `${own}drop-shadow(0 0 9px ${GOLD}.85))`, offset: 0.3 }, { filter: `${own}drop-shadow(0 0 0 ${GOLD}0))` }]; };

/* ---------- the three beats ---------- */
const quiet = (x) => !x || x.quiet || motion() === "off" || (typeof hud !== "undefined" && hud && hud.replay);
function onPick(x) {
  if (quiet(x)) return;
  count.pick++;
  beat("pick", lineOf(), hush, { duration: 600, easing: "ease-in-out" });
  beat("pick", well(), hush, { duration: 600, easing: "ease-in-out" }, well);
}
function onOutcome(x) {
  if (quiet(x) || !x.res) return;
  const moved = (x.res.dw || []).reduce((t, v) => t + Math.abs(v || 0), 0);
  if (moved < 1) return;
  count.outcome++;
  beat("outcome", well(), swell, { duration: 700, easing: "cubic-bezier(.34, 1.56, .64, 1)" }, well);
  beat("outcome", ageOf(), glint, { duration: 700 }, ageOf);
}
// the year: read at each update. Their age moves only while the life is lived (time runs between moments; the update
// that brings a year may be the one that stops at a moment), so a new whole year in play is a year lived. The first
// update of a life, and a quiet one (after a load, the years before the player takes over), only note it
let year = -1, lifeOf = null, yearAt = 0;
const living = () => typeof hud !== "undefined" && !!hud && hud.mode === "play" && !hud.replay && hud.job !== "past";
function onUpdate(S, how) {
  const y = Math.floor((S.age || 0) + 1e-9);
  if (lifeOf !== CH.life || year < 0 || (how && how.quiet) || y < year) { lifeOf = CH.life; year = y; return; }
  if (y === year) return;
  year = y;
  if (!living() || motion() === "off") return;
  if (motion() === "calm" && y % 2) return;                        // calm: fewer
  const t = performance.now(); if (t - yearAt < 1200) return;      // years that fly by (a decade's step) glint once
  yearAt = t; count.year++;
  beat("year", ageOf(), glint, { duration: 700 }, ageOf);
  beat("year", medalOf(), rim, { duration: 700, delay: 80 }, medalOf);
  beat("year", newestYear(), glint, { duration: 700, delay: 160 });
}

/* ---------- the piece ---------- */
let offs = [];
function stop() { playing.forEach((b) => { if (b.a) { b.a.onfinish = b.a.oncancel = null; b.a.cancel(); } }); playing.clear(); if (mo) mo.disconnect(); }
CH.mods.beat = { count };
CH.piece("beat", {
  order: 95,
  mount() {
    year = -1; lifeOf = null;
    offs = [CH.on("pick", onPick), CH.on("outcome", onOutcome), CH.on("motion", (m) => { if (m === "off") stop(); })];
  },
  update: onUpdate,
  destroy() { offs.forEach((f) => f()); offs = []; stop(); },
});
})();
