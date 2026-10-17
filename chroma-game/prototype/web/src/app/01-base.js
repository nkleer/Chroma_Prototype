"use strict";
const $ = (id) => document.getElementById(id);
const app = $("app"), feedEl = $("feed"), chronEl = $("chron"), screenEl = $("screen"), tableEl = $("table"), reviewEl = $("review"), stageEl = $("stage");
const hudEl = $("hud"), whoEl = $("who"), toolsEl = $("tools"), transEl = $("transport"), tipEl = $("tip"), helpEl = $("help"), toastEl = $("toast");
const lineEl = $("line"), riverEl = $("river"), fogEl = $("fog"), aheadEl = $("ahead");
const COLORS = ["W", "U", "B", "R", "G"];
const CNAME = { W: "White", U: "Blue", B: "Black", R: "Red", G: "Green" };
const CIDEA = { W: "Peace through order: duty, fairness, belonging.", U: "Perfection through knowledge: curiosity, mastery, foresight.",
  B: "Power through opportunity: ambition, self-reliance, getting what is theirs.", R: "Freedom through action: passion, feeling, the moment.",
  G: "Harmony through acceptance: nature, tradition, growing into what they are." };
const GOAL = { W: "Order", U: "Knowledge", B: "Power", R: "Freedom", G: "Harmony" };
const VALUE = { W: "doing right by others", U: "understanding how things work", B: "getting ahead on their own terms", R: "feeling alive and free", G: "staying true to their roots and their people" };
const FRAME = { W: ["#efe4c2", "#b3a274"], U: ["#4f8ad0", "#1b3c70"], B: ["#5e4f6b", "#1e1828"], R: ["#d25a3c", "#6e2318"], G: ["#4f9c5f", "#1c4a29"] };
const ART = { W: ["#fff3c8", "#7d6836"], U: ["#a4d2ff", "#0f3164"], B: ["#b28fd0", "#170f21"], R: ["#ffb592", "#6c190d"], G: ["#aef2b9", "#123a1e"] };
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const cap = (s) => s ? s[0].toUpperCase() + s.slice(1) : s;
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const pct = (v) => Math.round(v * 100) + "%";
const fpct = (v) => Math.min(99, Math.max(1, Math.round(v * 100))) + "%"; // felt odds: never "sure" either way
const sgn = (v, d = 0) => (v > 0 ? "+" : v < 0 ? "−" : "±") + Math.abs(v).toFixed(d);
// Chroma's own icons come from the visuals thread's sprite (chroma-art/game/ink-icons.svg): woodcut glyphs, fill-based, ids "ci-..."
const GI_DATA = __GI_DATA__, GI = GI_DATA.map;
const isGi = (name) => /^(gi|ci)-/.test(String(name || ""));
const ic = (name, cls = "") => isGi(name) ? `<svg class="i gx ${cls}" aria-hidden="true"><use href="#${name}"/></svg>` : `<svg class="i ${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
const useIc = (name, attrs) => `<use${isGi(name) ? ' class="gx"' : ""} href="#${isGi(name) ? name : "i-" + name}" ${attrs}/>`;
// a color's sign: the visuals thread's own (ci-color-w ...), else the page's older mana symbol
const MANA = (c) => (GI.color && GI.color[c]) || "m-" + c;
const pip = (c, cls = "") => `<span class="pip p${c} ${cls}"><svg aria-hidden="true"><use href="#${MANA(c)}"/></svg></span>`;
const pips = (cs) => cs && cs.length ? `<span class="pips">${cs.map((c) => pip(c)).join("")}</span>` : "";
const lettersOf = (s) => String(s || "").split("").filter((c) => COLORS.includes(c));
const labelColors = lettersOf;
const MKRE = /⟦([^⟧]*)⟧/g;
const plainText = (s) => String(s ?? "").replace(MKRE, "");
function splitColors(col) {             // "W+U>G" -> means [W,U], ends [G]
  if (!col || col === "-") return { means: [], ends: [] };
  const [m, e] = col.split(">");
  const means = lettersOf(m), ends = e ? lettersOf(e) : means;
  return { means, ends };
}
// Emren 10-07 01:57 (N5): an action is tied to its colors, with no order between its way and its ends: one set of pips
const actColors = (means, ends) => COLORS.filter((c) => means.includes(c) || ends.includes(c));
function colorsHTML(means, ends) {
  if (!means.length) return "";
  return pips(actColors(means, ends));
}
function hintWord(d) { return d < -0.25 ? "much worse" : d < -0.08 ? "worse" : d <= 0.08 ? "about right" : d <= 0.25 ? "better" : "much better"; }

/* ---------------- interactive story text: ⟦kind:payload⟧text⟦/⟧ ---------------- */
function rich(s) {
  s = String(s ?? "");
  let out = "", depth = 0, last = 0;
  for (const m of s.matchAll(MKRE)) {
    out += esc(s.slice(last, m.index)); last = m.index + m[0].length;
    const t = m[1];
    if (t === "/") { if (depth > 0) { out += "</span>"; depth--; } continue; }
    const j = t.indexOf(":"), k = t.slice(0, j), pl = t.slice(j + 1);
    let c = "";
    if (k === "a" || k === "w") c = lettersOf(pl.split(">")[0])[0] || "";
    else if (k === "v") c = pl; else if (k === "t") c = pl.split("|")[0]; else if (k === "o") c = (pl.split("|")[2] || "")[0] || "";
    // item 6 (the game's lines_tied): a reading, and news that carried a message, show the color they pulled as a chip
    const chip = (k === "r" && COLORS.includes(pl.split("|")[2])) ? pl.split("|")[2] : (k === "x" && pl.split("|")[2] === "1" && COLORS.includes(pl.split("|")[1])) ? pl.split("|")[1] : "";
    out += `<span class="mk mk-${esc(k)}${c && COLORS.includes(c) ? " c-" + c : ""}${chip ? " mkc" : ""}" data-mk="${esc(k)}" data-pl="${esc(pl)}">${chip ? pip(chip) : ""}`; depth++;
  }
  out += esc(s.slice(last));
  while (depth-- > 0) out += "</span>";
  return out.replace(/\*([^*\n]+)\*/g, "<em>$1</em>").replace(/\n/g, "<br>");
}

/* ---------------- tooltips ---------------- */
const tips = new WeakMap();
let tipOwner = null;
const touchUI = window.matchMedia("(hover: none)").matches;
function setTip(el, fn) { if (el) { el.setAttribute("data-tip", ""); tips.set(el, fn); } }
function placeTip(r, side) {
  const t = tipEl.getBoundingClientRect();
  let x, y;
  if (side && r.right + t.width + 12 < innerWidth) { x = r.right + 10; y = r.top + 10; }
  else if (side && r.left - t.width - 12 > 0) { x = r.left - t.width - 10; y = r.top + 10; }
  else { x = r.left + r.width / 2 - t.width / 2; y = r.top - t.height - 8; if (y < 8) y = r.bottom + 8; }
  if (y + t.height > innerHeight - 8) y = Math.max(8, innerHeight - t.height - 8);
  x = Math.max(8, Math.min(x, innerWidth - t.width - 8));
  tipEl.style.left = x + "px"; tipEl.style.top = y + "px";
}
function showTip(el) {
  const fn = tips.get(el) || (el.classList && el.classList.contains("mk") ? () => mkTip(el) : null);
  if (!fn) return;
  const html = fn(); if (!html) return;
  if (tipOwner && tipOwner.classList) tipOwner.classList.remove("on");
  tipOwner = el; tipEl.innerHTML = html; tipEl.hidden = false;
  if (el.classList) el.classList.add("on");
  placeTip(el.getBoundingClientRect(), el.classList && el.classList.contains("tarot"));
}
function showTipAt(html, x, y) {
  tipOwner = "line"; tipEl.innerHTML = html; tipEl.hidden = false;
  placeTip({ left: x, right: x, top: y, bottom: y, width: 0, height: 0 }, false);
}
function hideTip() { if (tipOwner && tipOwner.classList) tipOwner.classList.remove("on"); tipOwner = null; tipEl.hidden = true; }
document.addEventListener("pointerover", (e) => {
  if (e.pointerType === "touch") return;
  const el = e.target.closest("[data-tip], .mk");
  if (el && el !== tipOwner) showTip(el); else if (!el && tipOwner && tipOwner !== "line") hideTip();
});
// on touch a tapped tip closes by itself after a few seconds, and a button that acts (a step, a door, Let them choose)
// does its job without leaving its tip open over the page (v22 next look; the phone tooltips fix)
let tipTimer = 0;
document.addEventListener("pointerdown", (e) => {
  if (e.pointerType !== "touch") return;
  const el = e.target.closest("[data-tip], .mk");
  const acts = el && el.matches("button:not(.qhelp)");
  if (el && !acts && !el.classList.contains("tarot") && !el.classList.contains("opt") && el !== tipOwner) { showTip(el); clearTimeout(tipTimer); tipTimer = setTimeout(() => { if (tipOwner === el) hideTip(); }, 3200); }
  else if (!e.target.closest(".tarot, .opt")) hideTip();
});
document.addEventListener("scroll", () => { if (tipOwner !== "line") hideTip(); }, true);
function tipBox(title, quote, rows, foot) {
  return `<h5>${title}</h5>${quote ? `<p class="q">${quote}</p>` : ""}${rows && rows.length ? `<table>${rows.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join("")}</table>` : ""}${foot ? `<p>${foot}</p>` : ""}`;
}
const ptsUp = (v) => `<span class="${v > 0.004 ? "up" : v < -0.004 ? "down" : ""}">${v > 0 ? "+" : v < 0 ? "−" : "±"}${Math.round(Math.abs(v) * 100)}%</span>`;   // a change in a 0..1 quantity
const tookWord = (v) => `<span class="${v > 0.05 ? "up" : v < -0.05 ? "down" : ""}">${v >= 0.5 ? "lifted them a lot" : v >= 0.15 ? "lifted them" : v > -0.15 ? "barely touched them" : v > -0.5 ? "weighed on them" : "hit them hard"}</span>`;
const hitWord = (v) => Math.abs(v) >= 0.6 ? "hard" : Math.abs(v) >= 0.25 ? "noticeably" : "lightly";
const fitWord = (v) => `<span class="${v > 0.05 ? "up" : v < -0.05 ? "down" : ""}">${v >= 0.25 ? "fits them well" : v >= 0.05 ? "fits them" : v > -0.05 ? "neither here nor there" : v > -0.25 ? "a poor fit" : "goes against who they are"}</span>`;
const updown = (v, d = 0, k = 1) => `<span class="${v > 0.004 ? "up" : v < -0.004 ? "down" : ""}">${sgn(v * k, d)}</span>`;
function bars(rows) {      // [[label, value 0..1, color, shown]]
  return `<div class="bars">${rows.map(([l, v, c, s]) => `<div><span>${l}</span><i><b style="width:${(clamp(v) * 100).toFixed(0)}%;background:${c}"></b></i><span>${s}</span></div>`).join("")}</div>`;
}

