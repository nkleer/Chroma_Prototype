"use strict";
/* ---------------- the Living HUD on the game page (in place of the showcase's shell.js) ----------------
   A layer over the page, built like the ink look and clarity: it wraps a few page functions, runs each original first and
   changes no life. It keeps the switch (a "Living HUD" row in the Table menu, under the ink look only, stored in this
   browser as chroma.living, on unless turned off; no key, since l belongs to the game) and the life's stop log (CH.life).
   Turned off, or under the classic look, html[data-living] is "off": no living rule applies and the screen is today's. */
(() => {
const CH = window.CH; if (!CH) return;
const root = document.documentElement;
const keep = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };
const read = (k, d) => { try { return localStorage.getItem(k) || d; } catch (_) { return d; } };
const safe = (where, f) => { try { return f(); } catch (e) { console.error("living: " + where, e); } };

/* ---------------- the switch ---------------- */
let living = read("chroma.living", "on") !== "off";
const ink = () => root.dataset.look === "ink";                 // look.js sets it before this script runs
const active = () => living && ink();
const setRoot = () => { const v = active() ? "on" : "off"; if (root.dataset.living !== v) root.dataset.living = v; };
setRoot();

/* ---------------- the life and its stop log ---------------- */
// a new CH.life for each life and each load (resetChron runs for both): the page's own story items, and the stops
function newLife() {
  CH.life = { name: "", setting: "", guilds: {}, river: [], items: ITEMS, portraits: PICS.portrait || null,
    stops: [], ages: [], pushes: [], end_age: Infinity, rev: 0 };
}
newLife();
const _resetChron = resetChron;
resetChron = function () { _resetChron(); safe("reset", newLife); };

/* ---------------- the Table menu: the Living HUD row, after the ink look's Motion and Look ---------------- */
const _renderTools = renderTools;
renderTools = function (h) { _renderTools(h); safe("menu", addRow); };
const rowTip = () => tipBox(`${ic("sprout")} Living HUD: ${living ? "on" : "off"}`, "", [],
  "With the ink look: a moving sky, a living star of their colors, the life as a river, cards with weight, the story in the voice's hand and a window of their years. Off shows the screen as it was.");
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
function turn() { living = !living; keep("chroma.living", living ? "on" : "off"); setRoot(); }
// the look turned (or the motion, or this switch): the root and the row follow
CH.on("motion", () => safe("look", () => { setRoot(); addRow(); }));
})();
