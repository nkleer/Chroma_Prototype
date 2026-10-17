/* ---------------- point 13: the whole character on one sheet (key c) ---------------- */
const sheetEl = document.createElement("div"); sheetEl.className = "help sheetwrap"; sheetEl.hidden = true; document.body.appendChild(sheetEl);
sheetEl.addEventListener("click", (e) => { if (e.target === sheetEl) closeSheet(); });
function closeSheet() { sheetEl.hidden = true; sheetEl.innerHTML = ""; hideTip(); }
function meterRow(label, frac, shown, col, def) {
  return `<div class="mt" data-def="${esc(def || "")}"><span class="ml">${label}</span><i><b style="width:${(clamp(frac) * 100).toFixed(0)}%;background:${col}"></b></i><span class="mv">${shown}</span></div>`;
}
function identityPath(L) {
  const out = [];
  for (const r of L.river || []) { const l = r[r.length - 1] || ""; if (!out.length || out[out.length - 1].l !== l) out.push({ l, from: r[0] }); }
  return out.map((x, i) => `<span class="chip">${x.l ? pips(lettersOf(x.l)) : ""}${esc((L.guilds || {})[x.l] || "Still forming")} <span class="muted">${Math.floor(x.from)}${i + 1 < out.length ? "–" + Math.floor(out[i + 1].from) : "+"}</span></span>`).join(`<span class="muted">›</span>`);
}
/* ---------------- point 13, v22 next look: the whole character on one sheet, in tabs (key c). Portrait reads like a page;
   Colors, Inner life, Around them and Ledger hold every number and definition of the one-page sheet before it. All five
   panels are in the page at once (the inactive ones hidden); the last tab is remembered in this browser. Replaces the old
   openSheet in app.js; it keeps sheetEl, closeSheet, meterRow and identityPath as they are. ---------------- */
const SH_TABS = [["portrait", "Portrait", "scroll"], ["colours", "Colors", "wheel"], ["inner", "Inner life", "heart"], ["around", "Around them", "people"], ["ledger", "Ledger", "book"]];
const SH_TAB_KEY = "chroma.sheetTab";
const SH_NEED_DEF = { safety: "Feeling safe: a home, money, health, no threat.", belonging: "Being part of a family, a circle, a community.", autonomy: "Choosing for themselves.",
  competence: "Being good at something and having it seen.", meaning: "Living for something beyond the day." };
const SH_NEED_WORD = { safety: "feeling safe", belonging: "belonging", autonomy: "room to choose for themselves", competence: "a sense of being good at something", meaning: "a sense of meaning" };
const SH_STAGE = { child: "in childhood", juvenile: "in their youth", "young adult": "in early adulthood", young_adult: "in early adulthood", adult: "in adulthood", mature: "in the middle years of life", elder: "in their elder years" };
const SH_AROUND_SHORT = [["own household", "Household"], ["ties", "Ties"], ["money", "Money"], ["health", "Health"], ["era", "The times"]];
const SH_BAND = { in: "part of them", rising: "rising", fading: "fading", out: "not part of them" };
const SH_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
const SH_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
// the portrait says its numbers in words: "thirty-two", "about a year"
function shNum(n) { n = Math.max(0, Math.floor(n)); return n < 20 ? SH_ONES[n] : n < 100 ? SH_TENS[Math.floor(n / 10)] + (n % 10 ? "-" + SH_ONES[n % 10] : "") : "more than a hundred"; }
function shYears(y) { return y < 1 ? "a few months" : y < 1.5 ? "about a year" : shNum(Math.round(y)) + " years"; }
function shList(xs) { return xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1]; }
const shA = (w) => /^(a|an|the|their|his|her) /i.test(w) ? w : (/^[aeiou]/i.test(w) ? "an " : "a ") + w;
const shMid = (g) => String(g || "").replace(/^The /, "the ");                      // a name mid-sentence: "the Striver"
const shK = (text, cs) => `<span class="shk" style="--k:${cs && cs.length ? `var(--c${cs[0]})` : "var(--ink)"}">${esc(text)}</span>`;
const shFar = (p) => /^(old |former )|^ex$/.test(p.role || "") ? 1 : 0;
const shSex = (L) => L.sexword || (L.sex ? (L.age < 13 ? (L.sex === "female" ? "a girl" : "a boy") : (L.sex === "female" ? "a woman" : "a man")) : "");
// identity runs from the yearly river rows: [{l, from}] (the same reading as identityPath)
function shRuns(L) {
  const out = [];
  for (const r of L.river || []) { const l = r[r.length - 1] || ""; if (!out.length || out[out.length - 1].l !== l) out.push({ l, from: r[0] }); }
  return out;
}
// Portrait: plain sentences from the data (who, who they are in colors, how they tend to be, what they live for, what holds them, what they lack)
function shPortrait(L) {
  const out = [], place = String(L.place || "").trim(), stage = L.stage === "mature" && L.age >= 60 ? "in the later years of life" : SH_STAGE[L.stage] || "";
  const who = L.stage === "child" ? shSex(L) || "a child" : (shSex(L) || "someone") + (stage ? " " + stage : "");
  out.push(`${esc(L.name || "They")} is ${L.age < 1 ? "a baby, not yet a year old" : shNum(L.age) + ", " + esc(who)}${place ? `, living in ${esc(shA(place))}` : ""}.`);
  const cs = lettersOf(L.label);
  if (cs.length && L.guild) {
    const mean = String(L.meaning || "").replace(": ", ", ");
    out.push(`Their colors make them ${shK(shMid(L.guild), cs)}${mean ? ": " + esc(mean) : ""}.`);
    const runs = shRuns(L), cur = runs[runs.length - 1], prev = runs[runs.length - 2];
    if (cur && cur.l === L.label) {
      const pg = prev && prev.l ? (L.guilds || {})[prev.l] : "";
      const yrs = Math.max(0, L.age - cur.from);
      if (pg) out.push(`They have been ${esc(shMid(L.guild))} for ${shYears(yrs)}, after a time as ${shK(shMid(pg), lettersOf(prev.l))}.`);
      else if (prev) out.push(`They have been ${esc(shMid(L.guild))} for ${shYears(yrs)}, the first shape their colors took.`);
      else if (yrs >= 1) out.push(`They have been ${esc(shMid(L.guild))} for ${shYears(yrs)}.`);
    }
  } else out.push("Who they are is still forming: no color leads them yet.");
  const T = L.temper || {}, tw = (k) => typeof T[k] === "number" ? temperWord(k, T[k]) : "";
  const R = { "hit hard by events": "Events hit them hard", "about average": "Events touch them about as much as anyone", "hard to shake": "They are hard to shake" }[tw("react")];
  const S = { "very sure of themselves": "they are very sure of who they are", "fairly sure": "they are fairly sure of who they are", "still searching": "they are still searching for who they are" }[tw("steady")];
  const M = { sunny: "Between events their mood comes back sunny", even: "Between events their mood settles even", low: "Between events their mood sinks low" }[tw("base_mood")];
  const O = { hopeful: "they trust that effort pays off", middling: "they are not sure that effort pays off", doubtful: "they doubt that effort pays off" }[tw("outlook")];
  if (R && S) out.push(/^They are /.test(R) ? `${R} and ${S.replace(/^they are /, "")}.` : `${R}, and ${S}.`);
  if (M && O) out.push(`${M}, and ${O}.`);
  const gs = (L.goals || []).slice().sort((a, b) => (b.strength || 0) - (a.strength || 0));
  if (gs.length) {
    const g = gs[0], nm = `<em>${esc(g.name)}</em>`, p = g.progress || 0;
    let t = g.kind === "passion" ? `Their passion is ${nm}` : g.kind === "plan" ? `They have a plan: to ${nm}, and it ${p >= 0.8 ? "is nearly done" : p >= 0.4 ? "is well under way" : "has only begun"}` : `They dream of ${nm}`;
    const d2 = gs.find((x) => x !== g && x.kind === "dream" && (x.strength || 0) >= 0.15);
    if (d2) t += g.kind === "dream" ? `, and of <em>${esc(d2.name)}</em>` : `${g.kind === "plan" ? "; " : ", and "}further off they dream of <em>${esc(d2.name)}</em>`;
    out.push(t + ".");
  } else out.push("They have no dream of their own yet.");
  const held = (L.titles || []).slice().sort((a, b) => (b.years || 0) - (a.years || 0)).map((t) => (t.named || [])[0]).filter((x) => x && x.say).slice(0, 3);
  out.push(held.length ? `What holds them in place is ${shList(held.map((x) => "being " + esc(x.say)))}.` : "No title holds them in place yet.");
  const ns = Object.entries(L.needs || {}).sort((a, b) => a[1] - b[1]);
  if (ns.length) { const [k, v] = ns[0], w = esc(SH_NEED_WORD[k] || k); out.push(v < 0.35 ? `What they lack most is ${w}.` : v < 0.6 ? `What they could use more of is ${w}.` : `Even their thinnest need, ${w}, is mostly met.`); }
  return out.join(" ");
}
// a trait row of the Portrait: label, slim bar, a word (the mockup's .trait); the hover gives the definition
function shTrait(label, frac, word, col, def) {
  return `<div class="shtrait" data-def="${esc(def || "")}"><span class="ml">${esc(label)}</span><span class="shbar"><i style="width:${(clamp(frac) * 100).toFixed(0)}%;background:${col}"></i></span><b>${esc(word)}</b></div>`;
}
const shNeedWord = (v) => v >= 0.75 ? "well met" : v >= 0.5 ? "met" : v >= 0.3 ? "thin" : "barely met";
// five small columns: the color now (fill), what they want (the line), the edge of who they are (the band)
function shColourBars(L) {
  const want = L.w.map((v, i) => Math.max(0, v + L.demand[i])), top = Math.max(0.5, ...L.w, ...want) * 1.08;
  const [enter, leave] = L.ident_rule || [0.22, 0.18], inId = lettersOf(L.label);
  return `<div class="shcbars">${COLORS.map((c, i) => `<div class="shcb" data-ci="${i}"><span class="t"><span class="edge" style="bottom:${(leave / top * 100).toFixed(1)}%;height:${((enter - leave) / top * 100).toFixed(1)}%"></span><i style="height:${(clamp(L.w[i] / top) * 100).toFixed(1)}%;background:var(--c${c})"></i><s style="bottom:${(clamp(want[i] / top) * 100).toFixed(1)}%"></s></span>${pip(c)}<small class="${inId.includes(c) ? "on" : ""}">${pct(L.w[i])}</small></div>`).join("")}</div>
    <div class="shlegend"><span><i class="lg-now"></i>now</span><span><i class="lg-want"></i>wants</span><span><i class="lg-edge"></i>the edge of who they are</span></div>`;
}
// a smooth line through points (Catmull-Rom as cubic Béziers); first: start with M, else continue with L
function shCurve(pts, first) {
  let d = (first ? "M" : "L") + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    d += `C${(p1[0] + (p2[0] - p0[0]) / 6).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) / 6).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) / 6).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) / 6).toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
}
// the life in color: river rows [age, w0..w4, content, peace, label] as five stacked bands; thicker where they were more content
function shRiver(L) {
  const R = (L.river || []).filter((r) => r && r.length >= 7);
  if (!R.length) return `<span class="empty">The river of their colors begins in early childhood.</span>`;
  const pts = R.map((r) => [r[0], r.slice(1, 6), r[6]]);
  if (L.age - pts[pts.length - 1][0] > 0.15) pts.push([L.age, L.w, L.content]);
  if (pts.length === 1) pts.unshift([pts[0][0] - 1, pts[0][1], pts[0][2]]);
  const W = 300, H = 80, a0 = pts[0][0], a1 = Math.max(a0 + 1, pts[pts.length - 1][0]), X = (a) => ((a - a0) / (a1 - a0)) * W, mid = H / 2;
  const edges = pts.map((p) => {
    const sum = p[1].reduce((s, v) => s + Math.max(0, v || 0), 0) || 1, t = H * (0.42 + 0.58 * clamp(p[2] == null ? 0.5 : p[2]));
    let y = mid - t / 2; const e = [y];
    p[1].forEach((v) => { y += t * Math.max(0, v || 0) / sum; e.push(y); });
    return e;
  });
  let bands = "", grid = "";
  COLORS.forEach((c, k) => {
    const up = pts.map((p, i) => [X(p[0]), edges[i][k]]), lo = pts.map((p, i) => [X(p[0]), edges[i][k + 1]]).reverse();
    bands += `<path fill="var(--c${c})" d="${shCurve(up, true)}${shCurve(lo, false)}Z"/>`;
  });
  for (let a = Math.floor(a0 / 10) * 10 + 10; a < a1; a += 10) grid += `<line x1="${X(a).toFixed(1)}" x2="${X(a).toFixed(1)}" y1="2" y2="${H - 2}"/>`;
  const marks = [];
  for (let a = Math.floor(a0 / 10) * 10 + 10; a < a1; a += 10) { const f = (a - a0) / (a1 - a0); if (f > 0.12 && f < 0.82) marks.push(`<span style="left:${(f * 100).toFixed(1)}%">${a}</span>`); }
  return `<div class="shriverw" id="shRiver" data-from="${a0 <= 0.5 ? "birth" : "the age of " + Math.floor(a0)}"><svg class="shriver" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true"><g class="gr">${grid}</g><g class="bd">${bands}</g></svg>
    <div class="shrax"><span>${a0 <= 0.5 ? "born" : "at " + Math.floor(a0)}</span>${marks.join("")}<span>now, ${Math.floor(L.age)}</span></div></div>`;
}
// Colors: now, wanted and held per color, and its place in who they are (the hover is the full color)
function shNowTable(L) {
  const want = L.w.map((v, i) => Math.max(0, v + L.demand[i])), hold = L.inertia.map((v) => v + 0.2), inId = lettersOf(L.label), dyn = L.dyn && L.dyn.bands;
  const [enter, leave] = L.ident_rule || [0.22, 0.18];
  const placeDef = `Whether the color is part of who they are: it joins above ${Math.round(enter * 100)}% and leaves below ${Math.round(leave * 100)}%. Rising: above ${Math.round(leave * 100)}%, not yet part of them. Fading: at or under ${Math.round(enter * 100)}%, held by the edge.`;
  return `<table class="shnow"><thead><tr><th></th><th data-def="${esc(SP_KEY[0][2])}">Now</th><th data-def="${esc(SP_KEY[1][2])}">Wants</th><th data-def="${esc(SP_KEY[2][2])}">Holds</th>${dyn ? `<th class="pl" data-def="${esc(placeDef)}">Place</th>` : ""}</tr></thead><tbody>
    ${COLORS.map((c, i) => `<tr data-ci="${i}"><th>${pip(c)}<span class="cn">${CNAME[c]}</span></th><td class="${inId.includes(c) ? "on" : ""}">${pct(L.w[i])}</td><td>${pct(want[i])}<span class="ar">${L.demand[i] > 0.005 ? "▲" : L.demand[i] < -0.005 ? "▼" : ""}</span></td><td>${pct(hold[i])}</td>${dyn ? `<td class="pl">${esc(SH_BAND[dyn[i]] || "")}</td>` : ""}</tr>`).join("")}</tbody></table>`;
}
function shSelect(key, focus) {
  const box = sheetEl.querySelector(".sheet"); if (!box) return;
  if (!SH_TABS.some((t) => t[0] === key)) key = SH_TABS[0][0];
  box.querySelectorAll('[role="tab"]').forEach((b) => { const on = b.dataset.tab === key; b.setAttribute("aria-selected", on ? "true" : "false"); b.tabIndex = on ? 0 : -1; if (on && focus) b.focus({ preventScroll: true }); });
  box.querySelectorAll('[role="tabpanel"]').forEach((p) => { p.hidden = p.dataset.tab !== key; });
  const pa = box.querySelector(".shpanels"); if (pa) pa.scrollTop = 0;
  hideTip();
  try { localStorage.setItem(SH_TAB_KEY, key); } catch (_) {}
  const bar = box.querySelector(".shtabs"), t = box.querySelector(`[role="tab"][data-tab="${key}"]`);      // keep the chosen tab in view where the bar scrolls sideways
  if (bar && t && bar.scrollWidth > bar.clientWidth + 1) {
    if (t.offsetLeft < bar.scrollLeft + 8) bar.scrollLeft = Math.max(0, t.offsetLeft - 16);
    else if (t.offsetLeft + t.offsetWidth > bar.scrollLeft + bar.clientWidth - 8) bar.scrollLeft = t.offsetLeft + t.offsetWidth - bar.clientWidth + 16;
  }
}
function pushesSaid(P) {               // F13: the judged pushes, and those that passed without a judgment by how they went
  const [ok, bad] = P.passed || [0, 0], S = [`${P.accepted || 0} they came to accept`, `${P.resented || 0} they resented`];
  if (ok + bad) S.push(`${ok + bad} passed without a judgment: ${ok} went well, ${bad} did not`);
  return S.join(", ");
}
function trustHTML(L) {                 // IDEAS.md, "Player intervention that helps": trust in the player, per color
  const T = L.trust || {}, P = L.pushes || {};
  if (!P.forced) return "";
  return `<h4>Trust in you</h4><div class="mts">${COLORS.map((c) => meterRow(`${pip(c)} ${CNAME[c]}`, (1 + (T[c] || 0)) / 2, sgn((T[c] || 0) * 100), `var(--c${c})`, "Built by your pushes in this color that they came to accept, lost by the ones they resented. Trust spares some of a push's resentment; distrust adds to it.")).join("")}</div>
    <p class="shnote">You pushed ${P.forced} time${P.forced === 1 ? "" : "s"}: ${pushesSaid(P)}.</p>`;
}
function openSheet() {
  const L = hud && hud.life; if (!L || !L.w) return;
  hideTip(); closeHud();
  const A = (n) => (hud.adj_defs || {})[n] || {};
  const want = L.w.map((v, i) => v + L.demand[i]), hold = L.inertia.map((v) => v + 0.2);
  // the Ledger: every color number with its definition (the old sheet's table)
  const row5 = (label, vs, def) => `<tr data-def="${esc(def)}"><th>${label}</th>${vs.map((v) => `<td>${pct(v)}</td>`).join("")}</tr>`;
  const ctab = `<table class="ctab"><thead><tr><th></th>${COLORS.map((c) => `<th>${pip(c)}<span class="cn">${CNAME[c]}</span></th>`).join("")}</tr></thead><tbody>
    ${row5("Now", L.w, SP_KEY[0][2])}${row5("Wants", want, SP_KEY[1][2])}${row5("Holds", hold, SP_KEY[2][2])}
    ${row5("Speed", L.acc, "How fast they could change now: how open their age is, times self-control, times belief, times the doors open to them.")}
    ${row5("Skill", L.skill, "Skill in each color's ways; it grows with use.")}${row5("Belief", L.belief, "Their belief that they can act in each color's ways.")}
    ${row5("Notices", L.lens, "What they notice first in a moment, as shares of 100.")}${row5("Voice", L.voice, "How the story tells them: 40% who they are now, 60% the last three years.")}
    ${L.dyn ? row5("Holds: deep", L.dyn.parts.core.map((v) => v + 0.2), "The deep part of what holds them (40% of it): what they notice first.") + row5("Holds: habit", L.dyn.parts.habit.map((v) => v + 0.2), "The habit part of what holds them (30%): the ways they have acted most.") + row5("Holds: roles", L.dyn.parts.roles.map((v) => v + 0.2), "The roles part of what holds them (30%): what the titles they have put themselves into expect.") : ""}</tbody></table>`;
  // Inner life: exactly the old sheet's meters, definitions and thresholds
  const I = L.inner || {}, N = L.needs || {};
  const inner = [
    meterRow("Satisfaction", L.content, pct(L.content), "var(--sat)", "How content they are with their life right now."),
    meterRow("Peace", L.peace, pct(L.peace), "var(--peace)", "How settled they are with who they are and how they live."),
    meterRow("Strain", L.stress / 1.5, pct(L.stress / 1.5), "var(--stress)", "The strain of the year, as a share of the most they can bear."),
    L.young ? "" : meterRow("Pent-up wanting", L.want / Math.max(L.want_thr, 1e-9), ringPct("want", L), "var(--want)", "What they were denied builds up; at 100% it breaks through and moves them on its own."),
    I.mood != null ? meterRow("Mood", (I.mood + 1) / 2, `${I.mood >= 0 ? "+" : "−"}${Math.abs(Math.round(I.mood * 100))}`, "var(--sat)", `Recent ups and downs, −100 to +100. Excited above ${Math.round((A("excited").on || 0) * 100)}, low below ${Math.round((A("low").on || 0) * 100)}.`) : "",
    I.self_control != null ? meterRow("Self-control", I.self_control / 1.6, String(Math.round(I.self_control * 100)), "var(--head)", `How much the head decides over the heart; it grows with plans kept and falls with plans broken. Disciplined above ${Math.round((A("disciplined").on || 1.22) * 100)}, impulsive below ${Math.round((A("impulsive").on || 0.88) * 100)}.`) : "",
    I.wound != null ? meterRow("Grief and harm", I.wound / 1.5, String(Math.round(I.wound * 100)), "var(--bad)", `What blows have left in them; it heals with time and support. Hurting above ${Math.round((A("hurting").on || 0.78) * 100)}.`) : "",
    I.gap != null ? meterRow("Gap to their ideal", I.gap / 0.3, String(Math.round(I.gap * 100)), "var(--arcane)", `How far who they are is from who they want to become. Searching above ${Math.round((A("searching").on || 0.15) * 100)}, settled below ${Math.round((A("settled").on || 0.06) * 100)}.`) : "",
    I.horizon != null ? meterRow("Time feels short", I.horizon, pct(I.horizon), "var(--gold)", "How short the years ahead feel; it rises with age and with losses, and makes what matters now weigh more.") : "",
    L.dyn ? meterRow("Open to change", L.dyn.openness / 1.5, L.dyn.openness.toFixed(2) + (L.dyn.window ? ", a window" : ""), "var(--arcane)", "A crossing or a hard time opens them: a rite of passage gives 1, a turning point or a hard event adds some, and it halves in about six months. Above 0.3 it is a window, when colors move more easily.") : "",
    I.formed != null ? meterRow("Lived experience", I.formed / 30, String(Math.round(I.formed)), "var(--gold)", "Surprises weighted by how much was at stake; an identity forms once this passes 6.") : ""].join("");
  const needs = Object.entries(N).map(([k, v]) => meterRow(cap(k), v, pct(v), "var(--peace)", SH_NEED_DEF[k] || "")).join("");
  const RS = L.res || {}, means = MEANS.filter(([k]) => RS[k] != null).map(([k, , def, col]) => meterRow(cap(k), RS[k], pct(RS[k]), col, def)).join("");
  const temperWords = L.temper ? TEMPER.map(([k, , , top, def]) => shTrait(TEMPER_NAME[k], L.temper[k] / top, temperWord(k, L.temper[k]), "var(--arcane)", def)).join("") : "";
  const temperNums = L.temper ? TEMPER.map(([k, , , top, def]) => meterRow(TEMPER_NAME[k], L.temper[k] / top, pct(L.temper[k] / top), "var(--gold)", `${def} Now ${temperWord(k, L.temper[k])}: ${L.temper[k].toFixed(2)} on a scale of 0 to ${top}.`)).join("") : "";
  const needWords = Object.entries(N).map(([k, v]) => shTrait(cap(k), v, shNeedWord(v), "var(--peace)", SH_NEED_DEF[k] || "")).join("");
  const states = (L.states || []).map((x, i) => `<div class="sdef"><span class="st g${x.good}${x.shadow !== undefined ? " shd" : ""}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span><span>${esc(stateDef(x))}${x.value != null ? ` Now ${esc(stateScale(x.var, x.scale, x.value))}.` : ""}</span></div>`).join("") || `<span class="empty">No marked state now</span>`;
  const stateChips = (L.states || []).map((x, i) => `<span class="st g${x.good}${x.shadow !== undefined ? " shd" : ""}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span>`).join("");
  const around = Object.entries(L.around || {}).map(([k, v]) => `<div class="sdef"><span class="chip" data-a="${esc(k)}">${esc(cap(k))}: <span class="w">${esc((L.around_words || {})[k] || "")} (${aroundPct(v)})</span></span><span>${esc(AROUND_DEF[k] || "")}</span></div>`).join("");
  const aroundShort = SH_AROUND_SHORT.filter(([k]) => (L.around || {})[k] != null).map(([k, w]) => `<div class="r" data-a="${esc(k)}"><span>${w}</span><b>${esc((L.around_words || {})[k] || "")}</b></div>`).join("");
  const titles = (L.titles || []).map((t) => `<div class="sdef"><span class="chip">${ic(KIND_ICON[t.kind])}${esc(cap(t.kind))}</span><span>${(t.named || []).map((x) => esc(cap(shortSay(x.say))) + (x.facets || []).map((f) => ", " + esc(shortSay(f.say))).join("")).join("; ") || ""} · ${yrsWord(t.years)} · invested ${investWord(t.invested)} · expects ${pips(lettersOf(t.expects))}${t.clash ? ` · ${ic("bolt")} in a clash` : ""}</span></div>`).join("") || `<span class="empty">No titles yet</span>`;
  const roles = (L.statuses || []).map((d, i) => `<span class="perk stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`).concat((L.perks || []).map((d, i) => `<span class="perk${d.state && d.state !== "held" ? " " + d.state : ""}" data-perk="${i}" style="--pc:${d.ways ? `var(--c${d.ways[0]})` : "var(--gold)"}">${ic(roleIconOf(d))}${esc(cap(d.name))}</span>`)).join("");
  const heldChips = (L.titles || []).map((t, i) => { const n = (t.named || [])[0]; return `<span class="chip shtl" data-ti="${i}">${ic(KIND_ICON[t.kind] || "anchor")}${esc(n ? cap(shortSay(n.say)) : cap(t.kind))}</span>`; })
    .concat((L.statuses || []).map((d, i) => `<span class="chip shtl stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`)).join("");
  const goals = (L.goals || []).map((g) => goalRow(g)).join("") || `<span class="empty">No dreams yet</span>`;
  // S5: the lines they will not cross, one "will not" each; the hover says what it is, when it formed and how it stands
  const LINE_STATE = { whole: "Not yet tested.", held: "Tested, and held.", crossed: "Crossed once, and it still weighs on them.", healed: "Crossed once, and since made right." };
  const lines = (L.lines || []).map((x) => `<div class="sdef" data-def="${esc(`${x.name}, since they were ${Math.floor(x.formed)}. ${LINE_STATE[x.state] || ""}`)}"><span class="chip ml">${pip(x.colour)}Will not</span><span>${esc(x.will_not)}</span></div>`).join("");
  // N1d: who they are, one line each, each shown only from the week the story found it; the hover says the sentence
  const who = (L.who || []).map(([k, v, def]) => `<div class="sdef whoy" data-def="${esc(def || "")}"><span class="chip ml">${esc(k)}</span><span>${esc(cap(v))}</span></div>`).join("");
  const people = (L.cast || []).slice().sort((a, b) => (b.alive - a.alive) || (b.seen - a.seen)).map((p) => `<tr data-pid="${p.id}"><td><span class="av${p.alive ? "" : " gone"}" style="--ac:${GROUP_COL[ROLE_GROUP[baseRole(p.role)] || "other"]}">${esc(p.name[0])}</span></td><td>${esc(p.name)}</td><td>${esc(cap(p.role))}</td><td>${p.met != null ? "met at " + Math.floor(p.met) : ""}</td><td>${p.alive ? "" : "gone"}</td></tr>`).join("");
  const near = (L.cast || []).filter((p) => p.alive).sort((a, b) => (shFar(a) - shFar(b)) || (b.seen - a.seen)), NEAR = 8;
  const closest = near.slice(0, NEAR).map((p) => `<span class="shp${shFar(p) ? " far" : ""}" data-pid="${p.id}"><span class="av" style="--ac:${GROUP_COL[ROLE_GROUP[baseRole(p.role)] || "other"]}">${esc(p.name[0])}</span>${esc(p.name)}<small>${esc(p.role)}</small></span>`).join("")
    + (near.length > NEAR ? `<button class="shp more" data-go="around">+${near.length - NEAR} more</button>` : "");
  let tab = SH_TABS[0][0]; try { tab = localStorage.getItem(SH_TAB_KEY) || tab; } catch (_) {}
  if (!SH_TABS.some((t) => t[0] === tab)) tab = SH_TABS[0][0];
  const panel = (k, body) => `<section class="shpanel p-${k}" role="tabpanel" id="shPanel-${k}" data-tab="${k}" aria-labelledby="shTab-${k}" tabindex="0"${k === tab ? "" : " hidden"}>${body}</section>`;
  const sex = L.sexword ? esc(L.sexword) + " · " : L.sex ? shSex(L) + " · " : "";
  sheetEl.hidden = false;
  sheetEl.innerHTML = `<div class="box paper sheet" role="dialog" aria-label="Character sheet">
    <div class="shh"><div class="shwho"><div class="shn">${esc(L.name)}</div><div class="muted">${Math.floor(L.age)} · ${sex}${esc(L.stage || "")} · ${esc(SETTING_NAME[L.setting] || "")}${L.place ? ", " + esc(L.place) : ""}</div></div>
      <div class="shid">${lettersOf(L.label).length ? pips(lettersOf(L.label)) : ""}<div><b>${esc(L.guild)}</b><div class="muted">${esc(L.meaning || "")}</div>${L.magic ? `<div class="mg">Magic: The Gathering calls it ${esc(L.magic)}</div>` : ""}</div></div>
      <button class="ghost" id="shClose" aria-label="Close">${ic("x")}</button></div>
    <div class="shtabs" role="tablist" aria-label="Character sheet">${SH_TABS.map(([k, w, icn]) => `<button class="shtab" role="tab" id="shTab-${k}" data-tab="${k}" aria-controls="shPanel-${k}" aria-selected="${k === tab}" tabindex="${k === tab ? 0 : -1}">${ic(icn)}<span>${w}</span></button>`).join("")}<span class="shhint" aria-hidden="true">${touchUI ? "Tap" : "Hover"} a row for what it means</span></div>
    <div class="shpanels">
      ${panel("portrait", `<div class="shsec sa-b"><h4>Portrait</h4><p class="shport">${shPortrait(L)}</p>${lines ? `<h4>Lines they will not cross</h4>${lines}` : ""}${temperWords ? `<h4>Temperament</h4><div class="shtraits">${temperWords}</div>` : ""}${needWords ? `<h4>Needs met</h4><div class="shtraits">${needWords}</div>` : ""}</div>
        <div class="shsec sa-a"><h4>Colors now and wanted</h4>${shColourBars(L)}<h4>The life in color</h4>${shRiver(L)}${stateChips ? `<h4>Right now</h4><div class="states shstates">${stateChips}</div>` : ""}</div>
        <div class="shsec sa-c">${aroundShort ? `<h4>Around them</h4><div class="sharound">${aroundShort}</div>` : ""}<h4>Closest people</h4><div class="shppl">${closest || `<span class="empty">Nobody met yet</span>`}</div><h4>Titles and statuses</h4><div class="chips">${heldChips || `<span class="empty">No titles yet</span>`}</div></div>`)}
      ${panel("colours", `<div class="shsec"><svg class="wheel big" id="shWheel" viewBox="-6 -2 212 206" aria-hidden="true"></svg>${spKeyHTML()}<h4>Who they have been</h4><div class="path">${identityPath(L) || `<span class="empty">Still forming</span>`}</div></div>
        <div class="shsec"><h4>Now, wanted and held</h4>${shNowTable(L)}<h4>What each color stands for</h4><div class="shideas">${COLORS.map((c) => `<div>${pip(c)}<span><b>${CNAME[c]}</b> ${esc(CIDEA[c])}</span></div>`).join("")}</div></div>`)}
      ${panel("inner", `<div class="shsec"><h4>Inner life</h4><div class="mts">${inner}</div><h4>Needs met</h4><div class="mts">${needs || `<span class="empty">Not known yet</span>`}</div>${trustHTML(L)}</div>
        <div class="shsec"><h4>States</h4>${states}</div>
        <div class="shsec"><h4>Dreams and plans</h4><div class="drms">${goals}</div></div>`)}
      ${panel("around", `<div class="shsec">${around ? `<h4>Around them</h4>${around}` : `<h4>Around them</h4><span class="empty">Nothing read yet</span>`}</div>
        <div class="shsec"><h4>Means</h4><div class="mts">${means || `<span class="empty">Not known yet</span>`}</div><h4>Titles</h4>${titles}${roles ? `<h4>Statuses and perks</h4><div class="perks">${roles}</div>` : ""}</div>
        <div class="shsec">${who ? `<h4>Who they are</h4>${who}` : ""}<h4>People</h4><table class="ptab">${people || "<tr><td>Nobody met yet</td></tr>"}</table></div>`)}
      ${panel("ledger", `<div class="shsec"><h4>The colors in numbers</h4>${ctab}</div>
        <div class="shsec">${temperNums ? `<h4>Temperament in numbers</h4><div class="mts">${temperNums}</div>` : ""}<p class="shnote">Every number the story keeps on them, as shares of 100. A color joins who they are above ${Math.round(((L.ident_rule || [])[0] || 0.22) * 100)}% and leaves below ${Math.round(((L.ident_rule || [])[1] || 0.18) * 100)}%. ${touchUI ? "Tap" : "Hover"} a row for its exact definition.</p></div>`)}
    </div></div>`;
  $("shWheel").innerHTML = spiderSVG(spOf(L, { id: "sh", hits: true }));
  sheetEl.querySelectorAll("#shWheel .hit").forEach((h) => setTip(h, () => tipColor(L, +h.dataset.c)));
  bindSpKey(sheetEl);
  sheetEl.querySelectorAll("[data-def]").forEach((el) => { if (el.dataset.def) setTip(el, () => tipBox((el.querySelector("th, .ml") || el).textContent, "", [], esc(el.dataset.def))); });
  sheetEl.querySelectorAll(".drm[data-gj]").forEach((el) => { const g = (L.goals || []).find((x) => x.j === +el.dataset.gj); if (g) setTip(el, () => goalTip({ kind: g.kind, colors: g.colors, domain: g.domain, source: g.source, horizon: g.horizon }, g)); });
  sheetEl.querySelectorAll("[data-ci]").forEach((el) => setTip(el, () => tipColor(L, +el.dataset.ci)));
  sheetEl.querySelectorAll("[data-st]").forEach((el) => { const x = (L.states || [])[+el.dataset.st]; if (x && x.reads) setTip(el, () => stTip(x)); });
  sheetEl.querySelectorAll("[data-a]").forEach((el) => { const k = el.dataset.a; setTip(el, () => aroundTip(k, L.around[k])); });
  sheetEl.querySelectorAll("[data-pid]").forEach((el) => setTip(el, () => personTip(+el.dataset.pid)));
  sheetEl.querySelectorAll("[data-rs]").forEach((el) => { const d = (L.statuses || [])[+el.dataset.rs]; if (d) setTip(el, () => roleTip(d)); });
  sheetEl.querySelectorAll("[data-perk]").forEach((el) => { const d = (L.perks || [])[+el.dataset.perk]; if (d) setTip(el, () => roleTip(d)); });
  sheetEl.querySelectorAll("[data-ti]").forEach((el) => { const t = (L.titles || [])[+el.dataset.ti], n = t && (t.named || [])[0]; if (n) setTip(el, () => roleTip(n)); });
  const rv = $("shRiver"); if (rv) setTip(rv, () => tipBox(`${ic("route")} The life in color`, "", [], `Each band is one color's share of who they were, year by year, from ${esc(rv.dataset.from)} to now. The river is thicker in the years they were more content.`));
  sheetEl.querySelectorAll("[data-go]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); shSelect(b.dataset.go, true); }));
  const bar = sheetEl.querySelector(".shtabs");
  const edges = () => { bar.classList.toggle("fl", bar.scrollLeft > 4); bar.classList.toggle("fr", bar.scrollLeft + bar.clientWidth < bar.scrollWidth - 4); };
  bar.addEventListener("scroll", edges, { passive: true });
  bar.querySelectorAll('[role="tab"]').forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); shSelect(b.dataset.tab, false); }));
  bar.addEventListener("keydown", (e) => {          // Left and Right (Home, End) move between the tabs
    const tabs = [...bar.querySelectorAll('[role="tab"]')], i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    const j = e.key === "ArrowRight" ? (i + 1) % tabs.length : e.key === "ArrowLeft" ? (i + tabs.length - 1) % tabs.length : e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : -1;
    if (j < 0) return;
    e.preventDefault(); e.stopPropagation(); shSelect(tabs[j].dataset.tab, true);
  });
  $("shClose").addEventListener("click", closeSheet);
  shSelect(tab, !touchUI); edges();
}

