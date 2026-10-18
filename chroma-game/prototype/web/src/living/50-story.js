"use strict";
/* ---------------- the Living HUD: the story (row V5; plan: the Living HUD in v23, step 6) ----------------
   Ported from the showcase's story.js (concept W4, the voice's hand, with B1's wet ink). It styles today's chronicle
   (#feed, 03-chronicle.js newYear, addEntry, addFeed) and replaces nothing: the years (.yr, .yh), the lines (.en.<tag>),
   the markers and their mkTip hovers, the folds, the chips, clarity's lines, sticking to the bottom and #chron's aria-live
   all stay as they are. Living only adds classes, custom properties and a few children:
   - The voice's hand. Each year is written in the hand of the voice telling it (hud.life.voice: who they are now, blended
     with a fading memory of who they were), in the variable face Fraunces (axes opsz, wght, SOFT, WONK):
       White   steadier and more formal: a larger optical size, slightly wider tracking, even leading
       Blue    finer and lighter: a lower weight, hairline contrast, a cool blue-black ink
       Black   deeper ink: a darker, violet-black ink with a soft shadow
       Red     warmer: Fraunces' wonky forms and a warm ink; the year's first line leans forward a little
       Green   rounder: SOFT high, a broader optical size, more room between words and lines
     Each colour shapes the hand only as far as the voice leans to it past an even fifth, so a mixed voice writes a mixed
     hand, and the five pure hands carry about the same ink. Their own thoughts (*...*) stay in Spectral italic. Without
     Fraunces the hands fall back to Spectral (html.sy-nofr) and keep tracking, leading, the lean and the inks.
   - Which voice a year takes: the one in force when it closed, from the stop log (CH.life.stops, living/90-game.js): the
     last stop before its end. A year is kept once it is over (a later stop exists), never while it is lived, so the year
     being lived takes the last stop so far and a year never changes its hand when it ends. The log comes back equal after
     a load, so the story looks the same live and after a save and load.
   - When the voice changed for real (a new leading colour, or a move of 12 points over three years), the old hand shows
     faintly behind the year's first line for three years, word on word, fading by a third a year. The years are read up
     to the age lived (floor(S.age)), never to an end that has not come.
   - A quill in each year's head says on hover whose voice tells the year and how that shows in the letters.
   - The year's first line opens like a book's chapter: a gilt capital, the rest of its first word in small capitals.
   - New lines soak in like ink: they come up from the paper from their first word, darker and feathered while wet, then
     dry in two steps; the year being lived stays a little wet (S.wet). A new year draws its rule and gilds its age. Look's
     own arrival (lk-in) steps aside in the story while this piece is on.
   Motion: full; calm (slower, and fewer lines soak at once); off and reduced motion (nothing moves). No CH.frame: the
   arrivals are CSS animations of opacity, transform and one sliding mask. Off (the menu row, the classic look):
   destroy() takes every class, property and child back out, and the story is today's. */
(() => {
const CH = window.CH; if (!CH || !CH.piece) return;
const CS = CH.COLORS, NAME = CH.NAME, clampV = CH.clamp, root = document.documentElement;
const EVEN = [0.2, 0.2, 0.2, 0.2, 0.2];
const GHOST_YEARS = 3;         // how long an old hand shows through after the voice changed
const MOVED = 0.12;            // a move of the voice that changes its hand: 12 points over three years, summed over the colours
const now = () => performance.now();
let on = false;                // mounted
const M = { ms: 0, calls: 0 }; // what this piece costs (script time), read by test/drive_living_story.js
const timed = (f) => (...a) => { const t = now(); try { return f(...a); } finally { M.ms += now() - t; M.calls++; } };
const safe = (where, f) => { try { return f(); } catch (e) { console.warn("living: story " + where, e); } };

/* ---------- the voice's hand ---------- */
// How far the voice leans to a colour, past an even fifth: 0 at 20% or less, 1 at 45% or more, eased.
const pullOf = (v) => Math.pow(clampV(((v || 0) - 0.2) / 0.25), 0.85);
// The plain hand (an even voice: a child's, or nobody's yet) and what each colour's whole hand adds to it. wght and opsz
// are Fraunces' axes; track, ws and lh are em of letter- and word-spacing and added line height; skew is degrees of lean
// (the year's first line only); shadow is the soft shadow of deep ink (0..1). Balanced so that each pure hand lays about
// as much ink on the page as the plain one: the colours differ in kind, not in loudness.
const PLAIN = { wght: 370, opsz: 20, soft: 0, wonk: 0, track: 0, ws: 0, lh: 0, skew: 0, shadow: 0 };
const HAND = {
  W: { opsz: 40, track: 0.022, wght: 30, lh: 0.04 },
  U: { wght: -12, opsz: 26, track: 0.008 },
  B: { wght: -26, opsz: -4, track: -0.004, shadow: 0.7 },
  R: { wonk: 1, skew: -1.5, wght: 8, opsz: 6, track: -0.002 },
  G: { soft: 100, opsz: -11, wght: 4, ws: 0.06, lh: 0.06 },
};
// the inks: the game's parchment ink (--parchInk) and the ink each colour writes in (dark enough to read as body text)
const INK0 = [42, 33, 22];
const INK = { W: [66, 47, 12], U: [12, 30, 62], B: [44, 28, 56], R: [96, 34, 18], G: [22, 56, 30] };
// the voice's own mark (the quill) in the game's engraving inks
const MARK = { W: [143, 113, 22], U: [28, 92, 162], B: [78, 57, 102], R: [176, 60, 29], G: [34, 115, 62] };
// handOf(v): every colour adds its own hand as far as the voice leans to it; when several lean at once their pulls share
// one whole hand, so a mixed voice never writes more than a pure one
function handOf(v) {
  v = v || EVEN;
  const p = CS.map((c, i) => pullOf(v[i]));
  const tot = p.reduce((a, b) => a + b, 0), k = tot > 1 ? 1 / tot : 1;
  const h = Object.assign({}, PLAIN), ink = INK0.slice();
  CS.forEach((c, i) => {
    const w = p[i] * k; if (!w) return;
    Object.keys(HAND[c]).forEach((key) => { h[key] += HAND[c][key] * w; });
    for (let j = 0; j < 3; j++) ink[j] += (INK[c][j] - INK0[j]) * w;
  });
  h.wonk = h.wonk >= 0.5 ? 1 : 0;                           // Fraunces swaps in its wonky forms past one half
  h.ink = ink.map((x) => Math.round(clampV(x, 0, 255)));
  h.pull = p.map((x) => x * k);
  // without the variable face: Spectral's medium weight only for a heavy hand, and a lighter ink for a fine (Blue) one
  h.fbWght = h.wght >= 480 ? 500 : 400;
  h.fbInk = h.ink.map((x) => Math.round(x + (110 - x) * 0.2 * h.pull[1]));
  return h;
}
// one string per hand as the eye sees it (rounded as setHand rounds), so a voice that barely moves restyles nothing
const handKey = (h) => [Math.round(h.wght / 2), Math.round(h.opsz), Math.round(h.soft / 2), h.wonk, Math.round(h.track * 1000), Math.round(h.ws * 1000),
  Math.round(h.lh * 100), Math.round(h.skew * 10), Math.round(h.shadow * 50), h.ink.join(".")].join(",");
const HAND_PROPS = ["--h-wght", "--h-opsz", "--h-soft", "--h-wonk", "--h-track", "--h-ws", "--h-lh", "--h-skew", "--h-sh", "--h-ink", "--h-fbw", "--h-fbink", "--h-wet", "--g"];
// the hand as custom properties on an element; living/50-story.css reads them
function setHand(el, h) {
  const st = el.style, put = (k, val) => { if (st.getPropertyValue(k) !== val) st.setProperty(k, val); };
  put("--h-wght", String(Math.round(h.wght / 2) * 2));
  put("--h-opsz", String(Math.round(h.opsz)));
  put("--h-soft", String(Math.round(h.soft / 2) * 2));
  put("--h-wonk", String(h.wonk));
  put("--h-track", (Math.round(h.track * 1000) / 1000).toFixed(3) + "em");
  put("--h-ws", (Math.round(h.ws * 1000) / 1000).toFixed(3) + "em");
  put("--h-lh", (1.62 + Math.round(h.lh * 100) / 100).toFixed(2));
  put("--h-skew", (Math.round(h.skew * 10) / 10).toFixed(1) + "deg");
  put("--h-sh", (Math.round(h.shadow * 50) / 50).toFixed(2));
  put("--h-ink", h.ink.join(" "));
  put("--h-fbw", String(h.fbWght));
  put("--h-fbink", h.fbInk.join(" "));
  // the costly parts of a hand only where they show: a lean sets the first line's words in slanted boxes, and only deep
  // (Black) ink carries a text shadow
  el.classList.toggle("sy-lean", Math.abs(h.skew) >= 0.25);
  el.classList.toggle("sy-deep", h.shadow >= 0.04);
}
const rgbOf = (a) => `rgb(${a.map((x) => Math.round(x)).join(" ")})`;
// the voice's own colour, for its quill: the leading inks mixed by how far the voice leans to each
function voiceInk(v) {
  const p = CS.map((c, i) => pullOf(v[i])), tot = p.reduce((a, b) => a + b, 0);
  if (tot < 0.05) return "rgb(109 92 65)";
  const out = [0, 0, 0]; CS.forEach((c, i) => { for (let j = 0; j < 3; j++) out[j] += MARK[c][j] * p[i] / tot; });
  return rgbOf(out);
}
const l1 = (a, b) => a.reduce((s, x, i) => s + Math.abs(x - b[i]), 0);
// the colour that leads the voice (index), or -1 while none stands out (21.5%, as the story's own leading reads it)
const leadOf = (v) => { let b = -1, m = 0.215; (v || EVEN).forEach((x, i) => { if (x >= m) { m = x; b = i; } }); return b; };
// the voice in plain words: "mostly Red (35%), then White (21%)"
function voiceWords(v) {
  const order = CS.map((c, i) => [c, v[i] || 0]).sort((a, b) => b[1] - a[1]);
  const lead = order.filter(([, x]) => x >= 0.215).slice(0, 2);
  if (!lead.length) return "evenly, in no one color's voice yet";
  return lead.map(([c, x], i) => `${i ? "then " : "mostly "}${NAME[c]} (${CH.pct(x)})`).join(", ");
}
// how the voice moved between two years: the one or two colours whose share changed most, with both numbers
function shiftWords(a, before) {
  const d = CS.map((c, i) => [c, (a[i] || 0) - (before[i] || 0), before[i] || 0, a[i] || 0]).filter((x) => Math.abs(x[1]) >= 0.02)
    .sort((x, y) => Math.abs(y[1]) - Math.abs(x[1])).slice(0, 2);
  if (!d.length) return "it has hardly moved";
  return d.map(([c, x, b, n]) => `${NAME[c]} has ${x > 0 ? "grown" : "faded"} from ${CH.pct(b)} to ${CH.pct(n)}`).join(" and ");
}
const TRAIT = { W: "steady, formal letters, set a little wider", U: "fine, light strokes with hairline contrast",
  B: "deep, dark ink with a soft shadow", R: "warm ink and lively letters, the first line leaning forward", G: "rounder, softer letters with room to breathe" };
function handWords(v) {
  const p = CS.map((c, i) => [c, pullOf(v[i])]).filter(([, x]) => x > 0.12).sort((a, b) => b[1] - a[1]);
  if (!p.length) return "An even hand: no color leads the telling yet.";
  return p.map(([c, x], i) => `${i ? (x > 0.4 ? "with " : "and a little of ") : "Lettered as " + NAME[c] + " writes: "}${i ? NAME[c] + "'s " : ""}${TRAIT[c]}`).join("; ") + ".";
}

/* ---------- the voice of each year: the one in force when the year closed (its last stop in CH.life.stops). Only a year
   that is over is kept (a stop after its end exists); the year being lived takes the last stop so far, which is the same
   stop once it is over. A year before the first stop takes the first stop's voice. ---------- */
const isOver = (L, y) => { const A = L.ages; return A.length > 0 && A[A.length - 1] > y + 1 - 1e-6; };
const yearMemo = new WeakMap();
function yearStop(L, y) {
  let m = yearMemo.get(L); if (!m) { m = new Map(); yearMemo.set(L, m); }
  if (m.has(y)) return m.get(y);
  const s = L.stops[CH.stopAt(y + 1 - 1e-6)];
  if (s && isOver(L, y)) m.set(y, s);
  return s;
}
const yearVoice = (L, y) => { if (!L || y < 0) return EVEN; const s = yearStop(L, y), v = s && s.life.voice; return v && v.length === 5 ? v : EVEN; };

/* ---------- when the hand really changed, and the old hand that shows through after it ----------
   A year's hand changed when its voice leads with another colour than three years before, or moved more than 12 points
   since then. The change is dated to the first such year (within a long drift only a new leading colour counts again), and
   for the three years from it the year's first line carries the hand of before the change behind it, at full strength,
   then two thirds, then one third. Kept for years that are over; the year being lived is read again at each update. */
const changed = (v, w) => leadOf(v) !== leadOf(w) || l1(v, w) > MOVED;
const evMemo = new WeakMap();
function evAt(L, y) {
  if (!L || y < 1) return false;
  let m = evMemo.get(L); if (!m) { m = new Map(); evMemo.set(L, m); }
  if (m.has(y)) return m.get(y);
  const v = yearVoice(L, y), b3 = yearVoice(L, y - 3);
  let e = false;
  if (changed(v, b3) && !evAt(L, y - 1) && !evAt(L, y - 2)) {
    const v1 = yearVoice(L, y - 1), b4 = yearVoice(L, y - 4);
    e = !changed(v1, b4) || (leadOf(v) !== leadOf(b3) && leadOf(v1) === leadOf(b4));
  }
  if (isOver(L, y)) m.set(y, e);
  return e;
}
// the years lived so far, in order, so each one reads the two before it from the memo
const eventsTo = (L, upTo) => { for (let y = 1; y <= upTo; y++) evAt(L, y); };
const NOG = { k: 0, v: EVEN, at: -1 };
// the old hand behind year y: how strongly it shows (k), whose voice it was (v) and the year of the change (at)
function ghostOf(L, y) {
  if (!L || y < 1) return NOG;
  for (let d = 0; d < GHOST_YEARS; d++) { const e = y - d; if (evAt(L, e)) return { k: 1 - d / GHOST_YEARS, v: yearVoice(L, e - 3), at: e }; }
  return NOG;
}

/* ---------- the year's first line: a gilt capital and small capitals; word by word where a lean or an old hand needs it ---------- */
// after a one-letter word ("A", "I") the next word takes the small capitals too, so it reads "A YEAR that passes..."
function gildFirst(el) {
  const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let n, i = -1;
  while ((n = tw.nextNode())) { i = n.data.search(/[A-Za-z0-9]/); if (i >= 0) break; }
  if (!n) return;
  const wrapIn = (node, a, b, cls) => { const r = document.createRange(); r.setStart(node, a); r.setEnd(node, b); const s = document.createElement("span"); s.className = cls; r.surroundContents(s); return s; };
  const init = wrapIn(n, i, i + 1, "sy-init");
  const t2 = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let x, past = false;
  while ((x = t2.nextNode())) {
    if (!past) { if (init.contains(x)) past = true; continue; }
    if (/^\s*$/.test(x.data)) continue;
    const m = /^(\s*)([A-Za-z0-9'’-]+)/.exec(x.data);
    if (m) wrapIn(x, m[1].length, m[1].length + m[2].length, "sy-sc");
    break;
  }
}
// each word in its own box, so a lean slants each word without shifting the lines, and the old hand lines up word on word
function wrapWords(el) {
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [];
  let n; while ((n = w.nextNode())) nodes.push(n);
  nodes.forEach((t) => {
    const parts = t.data.split(/(\s+)/); if (parts.length === 1 && !parts[0]) return;
    const f = document.createDocumentFragment();
    parts.forEach((p) => { if (!p) return; if (/^\s+$/.test(p)) f.appendChild(document.createTextNode(p)); else { const s = document.createElement("span"); s.className = "sy-w"; s.textContent = p; f.appendChild(s); } });
    t.parentNode.replaceChild(f, t);
  });
  glue(el);
}
// A line may break between any two inline blocks, so a full stop or a "'s" just outside a marked phrase could start the
// next line on its own: it joins the word it touches (keeping the plain ink); an opening bracket or quote joins the next.
const CLOSER = /^[.,;:!?…)\]}’”"'»]+(?:s|S)?[.,;:!?…)\]}’”"'»]*$/, OPENER = /^[(\[{‘“"'«]+$/;
function glue(el) {
  const ws = [...el.querySelectorAll(".sy-w")]; if (ws.length < 2) return;
  const r = document.createRange();
  const touching = (a, b) => { r.setStartAfter(a); r.setEndBefore(b); return r.toString() === ""; };
  for (let i = 1; i < ws.length; i++) {
    const a = ws[i - 1], b = ws[i]; if (!a) continue;
    if (a.parentNode === b.parentNode || !a.parentNode || !b.parentNode) continue;
    if (CLOSER.test(b.textContent) && touching(a, b)) {
      const p = document.createElement("span"); p.className = "sy-p"; p.textContent = b.textContent;
      a.appendChild(p); b.remove(); ws[i] = a;
    } else if (OPENER.test(a.textContent) && touching(a, b)) {
      const p = document.createElement("span"); p.className = "sy-p"; p.textContent = a.textContent;
      b.insertBefore(p, b.firstChild); a.remove(); ws[i - 1] = null;
    }
  }
}
/* The old hand writes the same words in the same places, in its own letters: each word of the first line again, on the
   same line, centred on the word above it and fitted to its width. Its letters are CSS generated text (data-w), so the
   story's own text (innerText, a copy, a screen reader) holds every word once. Measured only when something changed it
   (its words, its hand, its width, a font). Every measure is divided by any CSS scale above the column. */
function alignGhost(sec) {
  const st = sec._sy; if (!st || !st.dirty) return;
  const lead = leadOf_(sec), g = lead && lead.querySelector(":scope > .sy-ghost");
  if (!g || !lead.isConnected) { st.dirty = false; return; }
  const ws = [...lead.querySelectorAll(".sy-w")]; if (!ws.length) { st.dirty = false; return; }
  const gr = g.getBoundingClientRect(), gw0 = g.offsetWidth;
  if (!gr.width || !gw0) return;                                   // not drawn yet (a folded or hidden story): later
  st.dirty = false;
  const s = gr.width / gw0;
  const at = ws.map((w) => { const r = w.getBoundingClientRect(), tw = w.offsetWidth; return { w, tw, x: ((r.left + r.right) / 2 - gr.left) / s - tw / 2, y: (r.top - gr.top) / s }; });
  const key = at.map((p) => `${p.x.toFixed(1)}:${p.y.toFixed(1)}:${p.tw}`).join(",") + "|" + g.style.cssText;
  if (st.ghostKey === key) return;
  st.ghostKey = key;
  const f = document.createDocumentFragment();
  at.forEach((p) => {
    const d = document.createElement("span"), init = p.w.querySelector(".sy-init");
    d.className = "sy-gl" + (init ? " sy-gl0" : p.w.querySelector(".sy-sc") ? " sy-glsc" : "");
    if (init) { d.dataset.a = init.textContent; d.dataset.w = p.w.textContent.slice(init.textContent.length); } else d.dataset.w = p.w.textContent;
    d.style.left = p.x.toFixed(2) + "px"; d.style.top = p.y.toFixed(2) + "px"; f.appendChild(d);
  });
  g.textContent = ""; g.appendChild(f);
  const gl = [...g.children], gw = gl.map((d) => d.offsetWidth);       // read every width, then write
  gl.forEach((d, i) => { const k = gw[i] ? clampV(at[i].tw / gw[i], 0.8, 1.25) : 1; d.style.transform = `scaleX(${k.toFixed(4)})`; });
}
let alignT = 0;
const alignAll = timed(() => { alignT = 0; if (on) sections().forEach(alignGhost); });
const alignSoon = () => { if (!alignT) alignT = setTimeout(alignAll, 0); };

/* ---------- the years on the page ---------- */
const sections = () => [...feedEl.children].filter((x) => x.classList.contains("yr"));
const leadOf_ = (sec) => sec.querySelector(":scope > .lead");
const isOpen = (sec) => !sec.classList.contains("closed");
const quill = (cls) => CH.icon("ci-quill", cls || "");
// the first line as the page wrote it, then decorated: gilt always; word by word only while the year is open and a lean or
// an old hand needs it. The page sets a year's first line once (03-chronicle.js addEntry, tag "year").
function renderLead(sec) {
  const st = sec._sy, lead = leadOf_(sec); if (!st || !lead || lead.hidden) return;
  const it = ITEMS[+lead.dataset.i]; if (!it) return;
  const words = isOpen(sec) && (st.lean || st.ghost.k > 0);
  if (st.leadEl === lead && st.leadI === it._i && st.words === words && lead.querySelector(".sy-init")) return;
  lead.innerHTML = rich(it.text);
  if (words) wrapWords(lead);                                       // words first, so the capital sits inside its word's box
  gildFirst(lead);
  if (words && st.ghost.k > 0) {
    const g = document.createElement("span"); g.className = "sy-ghost"; g.setAttribute("aria-hidden", "true");
    setHand(g, handOf(st.ghost.v)); g.style.setProperty("--g", (0.16 + 0.14 * st.ghost.k).toFixed(3));
    lead.appendChild(g); st.dirty = true; st.ghostKey = null; alignSoon();
  }
  st.leadEl = lead; st.leadI = it._i; st.words = words; st.open = isOpen(sec);
}
// the hand of one year (or the prologue's even one): set at once, never animated, since it lays the text out again. The
// year being lived, when its hand changes visibly at a stop, lets its first line come in again (opacity only).
function handSection(sec, L, cur, fade) {
  const pro = sec.classList.contains("prologue"), age = pro ? -1 : +sec.dataset.age;
  const st = sec._sy || (sec._sy = { key: "", gk: "", voice: null, ghost: NOG, lean: false, final: false, open: isOpen(sec), wet: -1 });
  if (st.final && !cur) return;
  const v = pro ? EVEN : yearVoice(L, age), h = handOf(v), key = handKey(h);
  const g = pro ? NOG : ghostOf(L, age), gk = g.k > 0 ? `${g.at}:${g.k.toFixed(2)}` : "";
  st.final = pro || isOver(L, age);
  if (key === st.key && gk === st.gk) { if (!st.leadEl) renderLead(sec); return; }
  const was = st.voice;
  const seen = fade && cur && st.key && was && CH.motion() !== "off" && (leadOf(v) !== leadOf(was) || l1(v, was) >= 0.04);
  st.key = key; st.gk = gk; st.voice = v; st.ghost = g; st.lean = Math.abs(h.skew) >= 0.25;
  setHand(sec, h);
  sec.classList.add("sy-hd");
  sec.classList.toggle("sy-ghosted", g.k > 0);
  st.leadEl = null; renderLead(sec);
  const lead = leadOf_(sec);
  if (seen && lead && !lead.hidden) { lead.classList.remove("sy-x"); void lead.offsetWidth; lead.classList.add("sy-x"); lead.addEventListener("animationend", () => lead.classList.remove("sy-x"), { once: true }); }
  if (!pro) markHand(sec, v, g);
}
// the quill in the year's head: the voice's ink, an older quill behind it while an old hand shows through
function markHand(sec, v, g) {
  const head = sec.querySelector(":scope > .yh"); if (!head) return;
  let q = head.querySelector(":scope > .sy-hand");
  if (!q) {
    q = document.createElement("span"); q.className = "sy-hand"; q.setAttribute("aria-hidden", "true");
    head.insertBefore(q, head.querySelector(":scope > .mood"));
    setTip(q, () => handTip(sec));
    // a finger's tap reads the quill (the page's tapped tip) instead of folding the year as a tap on the head does
    q.addEventListener("pointerdown", (e) => { q._touch = e.pointerType !== "mouse"; });
    q.addEventListener("click", (e) => { if (q._touch) e.stopPropagation(); });
  }
  const ink = voiceInk(v), gi = g.k > 0 ? voiceInk(g.v) : "", mk = ink + "|" + gi + "|" + g.k;
  if (q.dataset.k === mk) return;
  q.dataset.k = mk; q.style.color = ink;
  q.innerHTML = (gi ? `<span class="sy-hg" style="color:${gi};opacity:${(0.3 + 0.4 * g.k).toFixed(2)}">${quill()}</span>` : "") + quill();
}
function handTip(sec) {
  const st = sec._sy || {}, v = st.voice || EVEN, g = st.ghost || NOG;
  return tipBox(`${quill()} The voice's hand`, `This year the story is told ${voiceWords(v)}.`, [], `${handWords(v)}<br>` +
    (g.k > 0 ? `The voice changed at ${g.at}: ${shiftWords(yearVoice(CH.life, g.at), g.v)} in three years. Until ${g.at + GHOST_YEARS}, the older hand shows faintly behind each year's first line.`
      : "The voice blends who they are now with who they were; older selves fade from it over about three years."));
}
// the year being lived is still wet (S.wet in tenths, so a drifting wetness does not restyle it every week)
function setWet(sec, wet) {
  const st = sec._sy; if (!st) return;
  const q = Math.round(clampV(wet) * 10) / 10; if (q === st.wet) return; st.wet = q;
  if (q > 0) sec.style.setProperty("--h-wet", q.toFixed(1)); else unstyle(sec, "--h-wet");   // dry: as a year that was never lived here
  sec.classList.toggle("sy-wet", q >= 0.1);
}
let curSec = null;
const update = timed(function (S, how) {
  if (!on || !S || !CH.life) return;
  const L = CH.life, secs = sections(); if (!secs.length) return;
  eventsTo(L, Math.floor(S.age + 1e-9));
  const last = secs[secs.length - 1];
  if (curSec && curSec !== last && curSec.isConnected) { setWet(curSec, 0); curSec.classList.remove("sy-now"); }
  secs.forEach((sec) => handSection(sec, L, sec === last, !how.quiet));
  setWet(last, S.wet || 0); last.classList.add("sy-now"); curSec = last;
});

/* ---------- arrivals: new lines soak in like ink (B1), from their first word; a new year draws its rule ----------
   A line's text is held in a span of its own (.sy-tx) only while it soaks, so the mask that slides along it leaves the
   icon in the margin alone; then the text goes back as the page wrote it. The feather dries in two steps (two repaints). */
const soaking = new Set();
const KEEP_OUT = ".gut, .res, .rchips, .cl-dw, .lk-mk, .lk-rarem";
// the line's words: the first unbroken run of its children that is not the icon, the verdict, the chips or a mark
function holdText(el) {
  if (el.querySelector(":scope > .sy-tx")) return;
  const kids = [...el.childNodes], out = (n) => n.nodeType === 1 && n.matches(KEEP_OUT);
  const a = kids.findIndex((n) => !out(n)); if (a < 0) return;
  let b = a; while (b < kids.length && !out(kids[b])) b++;
  const run = kids.slice(a, b); if (!run.some((n) => n.nodeType === 1 || n.data.trim())) return;
  const tx = document.createElement("span"); tx.className = "sy-tx";
  el.insertBefore(tx, run[0]); run.forEach((n) => tx.appendChild(n));
}
function letText(el) { const tx = el.querySelector(":scope > .sy-tx"); if (tx) tx.replaceWith(...tx.childNodes); }
// a property taken back off an element, and its style attribute with it once nothing is left in it
const unstyle = (el, p) => { el.style.removeProperty(p); if (el.getAttribute("style") === "") el.removeAttribute("style"); };
function dry(el) {
  clearTimeout(el._syDry); el._syDry = 0; soaking.delete(el);
  el.classList.remove("sy-in", "sy-wet1", "sy-wet2"); unstyle(el, "--sy-d"); letText(el);
}
function soak(el, i, calm) {
  const d = Math.min(6, i) * (calm ? 200 : 80), dryMs = calm ? 5000 : 2800;
  if (el.classList.contains("en")) holdText(el);
  el.style.setProperty("--sy-d", `${d}ms`);
  el.classList.add("sy-in", "sy-wet1"); soaking.add(el);
  clearTimeout(el._syDry);
  el._syDry = setTimeout(() => { el.classList.replace("sy-wet1", "sy-wet2"); el._syDry = setTimeout(() => dry(el), dryMs * 0.5); }, d + dryMs * 0.5);
}
function newSec(sec) {
  sec.classList.add("sy-new");
  const rule = sec.querySelector(":scope > .yh > .rule");
  const done = () => sec.classList.remove("sy-new");
  if (rule) rule.addEventListener("animationend", done, { once: true }); else done();
  setTimeout(done, 3200);
}
const arrive = timed(function (items) {
  if (!on || !items || !items.length || !hud) return;
  const live = !hud.replay && hud.job !== "past" && !hud.loaded;
  // a new year takes the hand of the voice now at once (the stop the update reads is this state's), so its letters do not
  // change a moment after they arrive
  if (live && hud.life && hud.life.voice && hud.life.voice.length === 5)
    for (const it of items) if (it.tag === "chapter") { const sec = yearEls.get(it.age); if (sec && !sec._sy) { const st = sec._sy = { key: "", gk: "", voice: null, ghost: NOG, lean: false, final: false, open: isOpen(sec), wet: -1 }, h = handOf(hud.life.voice);
      st.key = handKey(h); st.voice = hud.life.voice.slice(); st.lean = Math.abs(h.skew) >= 0.25; setHand(sec, h); sec.classList.add("sy-hd"); markHand(sec, st.voice, NOG); } }
  // a year's first line, as soon as the page writes it
  for (const it of items) if (it.tag === "year") { const lead = feedEl.querySelector(`.lead[data-i="${it._i}"]`), sec = lead && lead.closest(".yr"); if (sec && sec._sy) { sec._sy.leadEl = null; renderLead(sec); } }
  const m = CH.motion();
  if (!live || m === "off" || items.length > 40) return;
  const calm = m === "calm", most = calm ? 4 : 8;
  let k = 0;
  for (let j = Math.max(0, items.length - most); j < items.length; j++) {
    const it = items[j];
    if (it.tag === "chapter") { const sec = yearEls.get(it.age); if (sec) newSec(sec); continue; }
    const el = it.tag === "year" ? feedEl.querySelector(`.lead[data-i="${it._i}"]`) : document.getElementById("it" + it._i);
    if (!el || !feedEl.contains(el) || el.classList.contains("ledger") || el.classList.contains("start")) continue;
    soak(el, k++, calm);
  }
});
// wrapped once here, acting only while this piece is mounted (and so only while the Living HUD is on)
const _addFeed = addFeed;
addFeed = function (items) { _addFeed(items); if (on) safe("arrive", () => arrive(items)); };

/* ---------- the face: Fraunces when it loaded, else the hands fall back to Spectral (handOf: fbWght, fbInk) ---------- */
const hasFace = () => [...document.fonts].some((f) => /fraunces/i.test(f.family) && f.status === "loaded");
const setFace = (ok) => { if (on) root.classList.toggle("sy-nofr", !ok); };
let faceTried = false;
function checkFace() {
  if (!document.fonts || !document.fonts.load) { setFace(false); return; }
  setFace(hasFace());
  if (faceTried) return; faceTried = true;
  document.fonts.load('400 17px "Fraunces"').then((fs) => setFace(!!fs && fs.some((f) => f.status === "loaded"))).catch(() => setFace(false));
}

/* ---------- mount and take down ---------- */
let mo = null, ro = null, lastW = 0;
const reAlign = () => { if (!on) return; sections().forEach((s) => { if (s._sy) { s._sy.dirty = true; s._sy.ghostKey = null; } }); alignSoon(); };
const onFonts = () => { setFace(hasFace()); reAlign(); };
const offs = [];
// a year folded or opened (a click on its head, the page's foldOld, a year opened from the life line): its first line again
const onFold = timed((rs) => {
  const seen = new Set();
  for (const r of rs) { const s = r.target; if (seen.has(s) || !s._sy || !s.classList.contains("yr")) continue; seen.add(s);
    if (s._sy.open !== isOpen(s)) { s._sy.open = isOpen(s); s._sy.leadEl = null; renderLead(s); if (s._sy.ghost.k > 0 && s._sy.open) { s._sy.dirty = true; alignSoon(); } } }
});
function mount() {
  if (typeof feedEl === "undefined" || !feedEl || typeof rich !== "function" || typeof yearEls === "undefined") return false;
  on = true; curSec = null;
  feedEl.classList.add("sy-on");
  checkFace();
  if ("MutationObserver" in window) { mo = new MutationObserver(onFold); mo.observe(feedEl, { attributes: true, attributeFilter: ["class"], subtree: true }); }
  if ("ResizeObserver" in window) { ro = new ResizeObserver(() => { const w = feedEl.offsetWidth; if (w !== lastW) { lastW = w; reAlign(); } }); ro.observe(feedEl); }
  if (document.fonts && document.fonts.addEventListener) document.fonts.addEventListener("loadingdone", onFonts);
  offs.push(CH.on("resize", reAlign));
  // turning motion off mid-arrival dries every line at once (the still frame shows dry ink)
  offs.push(CH.on("motion", (m) => { if (m === "off") [...soaking].forEach(dry); }));
  return true;
}
function destroy() {
  on = false;
  if (mo) mo.disconnect(); if (ro) ro.disconnect(); mo = ro = null; lastW = 0;
  if (document.fonts && document.fonts.removeEventListener) document.fonts.removeEventListener("loadingdone", onFonts);
  offs.splice(0).forEach((f) => f());
  clearTimeout(alignT); alignT = 0;
  [...soaking].forEach(dry);
  feedEl.querySelectorAll(".sy-tx").forEach((tx) => tx.replaceWith(...tx.childNodes));
  feedEl.querySelectorAll(".sy-new").forEach((s) => s.classList.remove("sy-new"));
  for (const sec of sections()) {
    const st = sec._sy; delete sec._sy;
    HAND_PROPS.forEach((p) => unstyle(sec, p));
    sec.classList.remove("sy-hd", "sy-lean", "sy-deep", "sy-ghosted", "sy-now", "sy-wet");
    sec.querySelectorAll(":scope > .yh > .sy-hand").forEach((q) => q.remove());
    const lead = leadOf_(sec);
    if (st && lead && !lead.hidden) { const it = ITEMS[+lead.dataset.i]; if (it) lead.innerHTML = rich(it.text); }
    if (lead) lead.classList.remove("sy-x", "sy-in", "sy-wet1", "sy-wet2");
  }
  feedEl.classList.remove("sy-on");
  root.classList.remove("sy-nofr");
  curSec = null;
}

CH.mods.story = { hand: handOf, ink: voiceInk, yearVoice, ghostOf, cost: M };
CH.piece("story", { order: 50, mount, update, destroy });
})();
