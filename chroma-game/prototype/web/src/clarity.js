<script>
"use strict";
/* ---------------- clarity (thread "HUD and story flow check", Emren 10-10 10:25 UTC: "apply all of them") ----------------
   A layer over app.js and look.js, built like the ink look: it wraps a few functions, runs each original first and changes
   no life. Why each part, measured over 17 played lives: chroma-hud/gameplay-check/findings.md in the shared folder.
   1 quiet story: no story-only lines between moments. The voice's yearly line, the year's "times" line (it repeats a line
     already told), a memory whose moment is not told and an era they barely noticed leave the story. The interlude
     between moments tells what happened in those weeks (the moments, events, titles, with their color moves) instead of
     routine lines, and a told moment that moved their colors shows how, beside it.
   2 voice crest: the voice row is one line of symbols (the colors your pushes moved, and their share of who they became);
     its name, the trust and the voice's latest line are on hover.
   3 one-line inner voice: the moment keeps its quote and "Left alone, they would"; heart and head are icons on their
     cards and the tug's numbers are on hover; the outcome and the story drop the heart, head, third-way and regret tags,
     which change nothing in the life.
   4 the times where they count: no "with the times" badge on the cards; the push reading says what the times do to a push
     that costs something (the only thing they change).
   5 honest hovers: memories and moves no longer read as "a big public event"; the sheet's Self-control (discipline) is
     called Discipline, apart from the tug at a moment.
   8 fewer cards at once: at most five considered cards and Do nothing; the other considered ways, and the ways they
     haven't thought of, fold into one row each until opened (remembered in this browser).
   9 needs, + and −: a need's hover lists what is lifting it and what is pulling it down for this character now. */
(() => {
const cl = (f) => { try { return f(); } catch (e) { console.error("clarity:", e); } };
const keepK = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };
const readK = (k, d) => { try { return localStorage.getItem(k) || d; } catch (_) { return d; } };

/* ---------------- 1: quiet story ---------------- */
const MOMENT = new Set(["moment", "choice", "loss", "crisis"]);
let lastVoice = null;                    // the voice's latest line, told on the crest's hover (2)
function quiet(items) {
  for (const it of items || []) {
    if (!it || it._cl != null) continue;
    let hide = false;
    if (it.tag === "voice") { hide = true; lastVoice = it; }
    else if (it.tag === "world_year") hide = true;
    else if (it.tag === "era") hide = Math.abs(+it.took || 0) < 0.15;
    // a memory stays only beside the moment that brought it back (the same week)
    else if (it.tag === "memory") hide = !items.some((x) => x !== it && MOMENT.has(x.tag) && Math.abs((x.age || 0) - (it.age || 0)) < 0.05);
    it._cl = hide ? 1 : 0;
  }
}
// a told moment that moved their colors by a point or more shows how, in pips and arrows; the hover has the numbers
function dwChips(it) {
  if (!it || !it.dw || !["moment", "loss", "crisis"].includes(it.tag)) return "";
  if (Math.max(...it.dw.map(Math.abs)) < 1) return "";
  const xs = COLORS.map((c, i) => [c, it.dw[i]]).filter(([, v]) => Math.abs(v) >= 0.5).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 3);
  return `<span class="cl-dw" data-cldw="${it._i}">${xs.map(([c, v]) => `<span class="cl-c ${v > 0 ? "up" : "down"}">${pip(c)}<i>${Math.abs(v) >= 3 ? (v > 0 ? "▲▲" : "▼▼") : v > 0 ? "▲" : "▼"}</i></span>`).join("")}</span>`;
}
const dwTip = (it) => tipBox(`${ic("wheel")} How it moved them`, "", [["Colors", colorMoves(it.dw)]], "In points of 100. What happens to them, and what they do about it, moves their colors.");
function bindDw(root) {
  root.querySelectorAll("[data-cldw]").forEach((x) => { if (!x._clb) { x._clb = 1; const it = ITEMS[+x.dataset.cldw]; if (it) setTip(x, () => dwTip(it)); } });
}
const _addEntry = addEntry;
addEntry = function (it) {
  if (it && it._cl === 1) return;
  _addEntry(it);
  cl(() => {
    const h = dwChips(it); if (!h) return;
    const el = document.getElementById("it" + it._i); if (!el) return;
    el.insertAdjacentHTML("beforeend", h); bindDw(el);
  });
};
// the interlude between moments: what happened in these weeks, not routine lines
const IL_TAGS = new Set(["moment", "loss", "crisis", "read", "world_fx", "role", "commitment", "goal", "breakthrough", "rite", "death",
  "kin", "move", "healed", "hardened", "trouble", "fortune", "outside", "era", "memory"]);
function toInterlude(items) {
  if (!IL.on || !items) return;
  for (const it of items) {
    if (!IL_TAGS.has(it.tag) || it._cl === 1 || !it.text) continue;
    if (it.tag === "outside" && !/⟦x:/.test(it.text)) continue;      // an outside event they took no color from
    IL.lines.push({ text: it.text, age: it.age, cl: it });
  }
  if (IL.ended) { const P = IL_PACE[ilPace] || IL_PACE.slow; IL.tEnd = Math.max(IL.tEnd, IL.t0 + Math.min(IL.lines.length, 4) * P.line + 600); }
}
const _addFeed = addFeed;
addFeed = function (items) { cl(() => quiet(items)); _addFeed(items); cl(() => toInterlude(items)); };
const _ilFeed = ilFeed;
ilFeed = function (h) { _ilFeed(h && h.routine ? Object.assign({}, h, { routine: null }) : h); };
const _ilStart = ilStart;
ilStart = function (L) {
  _ilStart(L);
  cl(() => { const k = interEl.querySelector(".ilkick"); if (k) for (const n of k.childNodes) if (n.nodeType === 3 && /Everyday life/.test(n.data)) n.data = n.data.replace("Everyday life", "These weeks"); });
};
// each line the interlude writes: its item (for the hovers) and its color moves
const _ilStep = ilStep;
ilStep = function (now) {
  const n = IL.shown, r = _ilStep(now);
  if (IL.shown > n) cl(() => {
    const x = IL.lines[IL.shown - 1], box = $("ilLines"), p = box && box.lastElementChild;
    if (!x || !x.cl || !p || p.tagName !== "P") return;
    p.dataset.i = x.cl._i;
    const h = dwChips(x.cl); if (h) { p.insertAdjacentHTML("beforeend", h); bindDw(p); }
  });
  return r;
};

/* ---------------- 2: the voice crest ---------------- */
const vMoves = (V) => COLORS.map((c, i) => [c, (V.voice || [])[i] || 0]).filter(([, x]) => Math.abs(x) >= 1).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
const trustCls = (t) => /doubt/.test(t || "") ? "t-down" : /trust it/.test(t || "") ? "t-up" : "";
function ring(p) {
  const C = 2 * Math.PI * 6.5, v = clamp(p, 0, 1);
  return `<svg viewBox="0 0 16 16" aria-hidden="true"><circle class="r0" cx="8" cy="8" r="6.5"/><circle class="r1" cx="8" cy="8" r="6.5" stroke-dasharray="${(v * C).toFixed(1)} ${C.toFixed(1)}"/></svg>`;
}
voiceRowHTML = function (L) {
  const V = L && L.voice_row;
  if (!V || !V.n) return "";
  const mv = vMoves(V).slice(0, 2);
  const moves = mv.length ? mv.map(([c, x]) => `<span class="cl-c ${x > 0 ? "up" : "down"}">${pip(c)}<b>${x > 0 ? "▲" : "▼"}${Math.round(Math.abs(x))}</b></span>`).join("")
    : `<span class="cl-none">${V.steer ? "·" : "–"}</span>`;
  const label = `The voice in their head: ${V.name}. ` + (V.steer ? `Pushed ${V.steer} of ${V.n} moments; ${pct(V.share)} of how their colors changed.` : "No push yet.");
  return `<div class="voicerow cl-crest ${trustCls(V.trust)}" id="voiceRow" tabindex="0" aria-label="${esc(label)}">${ic("voice")}<span class="cl-vm">${moves}</span>${V.steer ? `<span class="cl-share">${ring(V.share)}<b>${pct(V.share)}</b></span>` : ""}</div>`;
};
voiceRowTip = function (L) {
  const V = L.voice_row, pts = (x) => `${x > 0 ? "+" : x < 0 ? "−" : ""}${Math.abs(x).toFixed(0)}`;
  const say = (xs) => COLORS.map((c, i) => [c, xs[i] || 0]).filter(([, x]) => Math.abs(x) >= 1).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 3).map(([c, x]) => `${pip(c)} ${CNAME[c]} ${pts(x)}`).join(", ");
  const you = say(V.voice || []), life = say(V.life || []);
  const rows = [["Pushed", `${V.steer} of ${V.n} moments`]];
  if (V.steer) rows.push(["You moved", you || "barely anything yet"], ["Life itself moved", life || "barely anything"], ["Your part", `${pct(V.share)} of how their colors changed` + (V.share < 0.1 && you ? " (life pulled the other way)" : "")]);
  rows.push(["Trust in you", esc(V.trust || "not judged yet")]);
  const last = lastVoice && lastVoice.text ? `<p class="q">${esc(plainText(lastVoice.text))}</p>` : "";
  return tipBox(`${ic("voice")} The voice in their head: ${esc(V.name)}`, "", rows, "") + last +
    `<p>${V.steer ? "In points of 100, since you became the voice. Its name comes from what it pushes for most; the arrows on the wheel show where." : "You have let them choose: the voice has not pushed yet."} Trust moves when a push they resisted turns out well or badly.</p>`;
};

/* ---------------- 3: one-line inner voice, and 4: the times where they count ---------------- */
const eraWord = (o) => {
  const e = +o.era || 0, k = clamp(1 - 0.4 * e, 0.5, 1.5), p = Math.round(Math.abs(1 - k) * 100);
  return Math.abs(e) >= 0.3 && !o.own && o.means && o.means.length && o.rel >= 0.02 && p >= 1 ? { up: e > 0, p } : null;
};
const _stripHTML = stripHTML;
stripHTML = function (o, num) {
  const s = _stripHTML(o, num);
  return cl(() => {
    const add = [];
    if (o.heart_pick || o.head_pick) add.push(`<span><b>Inner voice</b> ${o.heart_pick ? `<span style="color:var(--heart)">${ic("heart")} the heart's pick</span> ` : ""}${o.head_pick ? `<span style="color:var(--head)">${ic("head")} the head's pick</span>` : ""}</span>`);
    const e = eraWord(o);
    if (e) add.push(`<span class="${e.up ? "up" : "down"}"><b>The times</b> ${e.up ? "with them: this push costs" : "against them: this push costs"} ${e.p}% ${e.up ? "less" : "more"}</span>`);
    if (!add.length) return s;
    const at = s.lastIndexOf(`</div><div class="dhelp">`);
    return at < 0 ? s : s.slice(0, at) + add.join("") + s.slice(at);
  }) || s;
};
const _tipOption = tipOption;
tipOption = function (o, name, num) {
  const s = _tipOption(o, name, num);
  return cl(() => {
    const e = eraWord(o); if (!e) return s;
    const row = `<tr><td>The times</td><td><span class="${e.up ? "up" : "down"}">${e.up ? "with them" : "against them"}: this push costs ${e.p}% ${e.up ? "less" : "more"}</span></td></tr>`;
    return s.includes("</table>") ? s.replace("</table>", row + "</table>") : s;
  }) || s;
};
// the outcome: no heart, head, third-way or regret tags (display only); "pushed by you" stays
function plainVerdict(root) {
  root.querySelectorAll(".verdict .tag").forEach((t) => {
    if (t.classList.contains("heart") || t.classList.contains("head") || t.classList.contains("regret") ||
        (t.className === "tag" && t.querySelector('use[href="#i-route"]'))) t.remove();
  });
  root.querySelectorAll(".verdict").forEach((v) => { if (!v.textContent.trim() && !v.querySelector("svg, .av")) v.classList.add("cl-empty"); });
}
const _renderResolution = renderResolution;
renderResolution = function (h, reveal) { _renderResolution(h, reveal); cl(() => plainVerdict(tableEl)); };
// the tug keeps its picture; its numbers are on hover
function quietTug() {
  const t = $("tug"); if (!t || t._cl) return; t._cl = 1;
  t.querySelectorAll(".hrt, .hd").forEach((x) => { for (const n of [...x.childNodes]) if (n.nodeType === 3) n.remove(); });
}

/* ---------------- 8: fewer cards at once ---------------- */
let moreOpen = readK("chroma.clMore", "") === "1";
const SHOW = 5;
function rank(o) {
  return (o.own ? 1000 : 0) + (o.heart_pick ? 400 : 0) + (o.head_pick ? 300 : 0) +
    ((o.helped_row || o.lever || o.wcause || (o.roles_fx || []).length || o.commit) ? 100 : 0) + (+o.felt || 0) * 10;
}
function fewer(h) {
  const cp = h && h.cp; if (!cp || busy || !cp.options) return;
  const key = cp.age + "|" + cp.title;
  const box = $("evOpts"); if (!box || box._cl === key) return; box._cl = key;
  const cardOf = (b) => cp.options[+b.dataset.i];
  const grids = [...box.querySelectorAll(":scope > .ogrid:not(.oorg)")];
  const folds = [];
  // the considered ways: the grid with no heading before it
  const g0 = grids.find((g) => !(g.previousElementSibling && g.previousElementSibling.classList.contains("ask") && g.previousElementSibling.classList.contains("sub")));
  if (g0) {
    const cards = [...g0.querySelectorAll(":scope > .opt")];
    if (cards.length > SHOW + 1) {
      const keep = new Set(cards.slice().sort((a, b) => rank(cardOf(b)) - rank(cardOf(a))).slice(0, SHOW));
      const rest = cards.filter((b) => !keep.has(b));
      folds.push({ after: g0, cards: rest, title: "Other ways they considered" });
    }
  }
  // the ways they haven't thought of: their heading becomes the fold
  for (const g of grids) {
    if (g === g0) continue;
    const head = g.previousElementSibling;
    if (!head || !/haven't thought/.test(head.textContent)) continue;
    const cards = [...g.querySelectorAll(":scope > .opt")];
    if (!cards.length) continue;
    folds.push({ after: g, cards, title: "Ways they haven't thought of", head });
  }
  for (const f of folds) {
    const nums = f.cards.map((b) => +b.dataset.num).sort((a, b) => a - b);
    const grid = document.createElement("div"); grid.className = "ogrid cl-more";
    const btn = document.createElement("button"); btn.type = "button"; btn.className = "ask sub oorfold cl-fold";
    btn.innerHTML = `${ic("route")} ${f.title} <small>${nums.length} ${nums.length > 1 ? "options" : "option"} · ${nums.length > 1 ? "keys" : "key"} ${nums.join(", ")}</small><span class="chev" aria-hidden="true">▸</span>`;
    if (f.head) { f.head.replaceWith(btn); f.after.replaceWith(grid); }
    else { f.after.after(btn); btn.after(grid); }
    f.cards.forEach((b) => b.remove());
    const set = (on) => {
      btn.setAttribute("aria-expanded", String(on));
      if (on) f.cards.forEach((b) => grid.appendChild(b)); else f.cards.forEach((b) => b.remove());
    };
    btn.addEventListener("click", () => {
      moreOpen = btn.getAttribute("aria-expanded") !== "true"; keepK("chroma.clMore", moreOpen ? "1" : "");
      box.querySelectorAll(".cl-fold").forEach((x) => x._set && x._set(moreOpen));
      if (moreOpen && grid.lastElementChild) grid.lastElementChild.scrollIntoView({ block: "nearest" });
    });
    btn._set = set; set(moreOpen);
    setTip(btn, () => tipBox(`${ic("route")} ${f.title}`, "", [], "Folded to keep the moment readable. Their number keys still push them; open the row to read them."));
  }
}
const _renderTable = renderTable;
renderTable = function (h) { _renderTable(h); cl(() => { if (h && h.cp && !busy) { quietTug(); fewer(h); } }); };

/* ---------------- 5: honest hovers ---------------- */
const _mkTip = mkTip;
mkTip = function (el) {
  const k = el.dataset.mk, pl = (el.dataset.pl || "").split("|");
  if (k === "O" && pl[0] === "memory") return tipBox(`${ic(pl[1] || "ci-diary")} A memory`, "", [],
    "An old moment comes back to them: the same kind of moment again, or an act that leans the same way. Each old moment comes back in the story once.");
  if (k === "O" && pl[0] === "place") return tipBox(`${ic(pl[1] || "ci-box")} A move`, "", [],
    "Where they live now: its streets, its people and its dangers shape how safe they feel and where they belong.");
  return _mkTip(el);
};
cl(() => { if (CHG.discipline) CHG.discipline[2] = "Discipline"; });
const _openSheet = openSheet;
openSheet = function (...a) {
  const r = _openSheet(...a);
  cl(() => sheetEl.querySelectorAll(".mt").forEach((m) => {
    const l = m.querySelector(".ml"); if (!l || l.textContent !== "Self-control") return;
    l.textContent = "Discipline";
    m.dataset.def = "How well they hold to what the head decides. It grows with plans kept and hard wins, and falls with plans broken. At a moment, how much the head decides (the tug) also depends on their age, strain and peace.";
  }));
  return r;
};

/* ---------------- 9: needs, + and − ---------------- */
// the engine (engine.py, the weekly needs): means above half lift a need and below half drain it (safety from money and
// health, belonging from ties, room to choose from freedom and time); each held title pays its kind's needs
// (library.py COMMITMENTS) and its own; a family looks after a child; every need fades a little each week
const FROM_MEANS = { safety: [["money", 0.5], ["health", 0.5]], belonging: [["ties", 1]], autonomy: [["freedom", 0.6], ["time", 0.4]] };
const KIND_PAYS = { career: ["competence", "meaning", "safety"], partner: ["belonging", "safety"], children: ["meaning", "belonging"],
  community: ["belonging", "meaning"], faith: ["meaning", "belonging", "safety"] };
const ACT_PLUS = { safety: "acts that work, toward White ends most", belonging: "acts that work, toward Red and Green ends most",
  autonomy: "acting in their own strongest colors", competence: "succeeding at something hard for them", meaning: "acts that work, toward Blue and Black ends most" };
const ACT_MINUS = { autonomy: "acting against who they are, and pushes they resent", competence: "failing at what they try" };
needTip = function (k, L) {
  const v = (L.needs || {})[k] ?? 0, R = L.res || {}, plus = [], minus = [];
  // each means pulls on its own side of half (the engine adds them up, weighted)
  for (const [r] of FROM_MEANS[k] || []) if (R[r] != null)
    (R[r] >= 0.5 ? plus : minus).push(`${ic(RES_ICON[r] || "dot")} ${r} ${pct(R[r])}${R[r] >= 0.5 ? "" : ", under half"}`);
  for (const t of L.titles || []) {
    const nm = (t.named || [])[0], word = nm ? sockWord(nm) : ((KINDS.find(([x]) => x === t.kind) || [])[1] || cap(t.kind));
    const own = nm && (nm.meets || []).find(([w]) => w === NEED_LONG[k] || w === k);
    if (own) (own[1] > 0 ? plus : minus).push(`${ic(KIND_ICON[t.kind] || "anchor")} ${esc(word)}`);
    else if ((KIND_PAYS[t.kind] || []).includes(k)) plus.push(`${ic(KIND_ICON[t.kind] || "anchor")} ${esc(word)}`);
  }
  for (const d of L.statuses || []) {
    const m = (d.meets || []).find(([w]) => w === NEED_LONG[k] || w === k);
    if (m) (m[1] > 0 ? plus : minus).push(`${ic(roleIconOf(d))} ${esc(shortSay(d.say))}`);
  }
  if (L.stage === "child" && k !== "autonomy") plus.push(`${ic("home")} their family looks after them`);
  else if (L.stage === "juvenile" && k !== "autonomy") plus.push(`${ic("home")} their family, a little less now`);
  plus.push(esc(ACT_PLUS[k] || ""));
  if (ACT_MINUS[k]) minus.push(esc(ACT_MINUS[k]));
  minus.push("it fades a little every week");
  const li = (xs, c) => `<span class="${c}">${xs.join("<br>")}</span>`;
  return tipBox(`${ic(NEED_ICON[k] || "dot")} ${esc(cap(NEED_LONG[k] || k))}`, "", [["Now", `${pct(v)}, ${needWord(v)}`], [`<b class="up">+</b>`, li(plus.filter(Boolean), "up")], [`<b class="down">−</b>`, li(minus, "down")]],
    "A lacking need pulls satisfaction down, and meeting it lifts satisfaction most.");
};
})();
</script>
