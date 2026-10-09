<script>
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
    out += `<span class="mk mk-${esc(k)}${c && COLORS.includes(c) ? " c-" + c : ""}" data-mk="${esc(k)}" data-pl="${esc(pl)}">`; depth++;
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

/* ---------------- what the marked words mean ---------------- */
const GATE = { "pulled away": "Old habits pulled them away: inertia beat the wish.", "not offered": "Nobody around them offered it: a door that was not open here.",
  "lacked the means": "They lacked the means for it: money, time, health, ties or freedom fell short.", unnoticed: "It never crossed their mind." };
const THOUGHT = { reason: "Why they lean toward it: the act's own colors speak.", react: "How they take what happened, in the story's own voice.",
  reluct: "Who they are, pushing back against your push.", missed: "A thought about the road not taken.", wait: "They would rather let it be." };
const TEMPER_NAME = { react: "Reactivity", steady: "Steadiness", base_mood: "Baseline mood", outlook: "Outlook" };
const RES_ICON = { money: "coin", time: "clock", health: "pulse", ties: "link", freedom: "feather", ...GI.res };
const castById = (id) => ((hud && hud.life && hud.life.cast) || []).find((p) => p.id === id);
function voiceOf(c) { const L = hud && hud.life; return L && L.voice ? L.voice[COLORS.indexOf(c)] : null; }
function colorMoves(dw) {
  if (!dw) return "";
  const xs = COLORS.map((c, i) => [c, dw[i]]).filter(([, v]) => Math.abs(v) >= 0.05).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 3);
  return xs.length ? xs.map(([c, v]) => `${pip(c)} ${updown(v, 1)}`).join(" &nbsp;") : "barely";
}
function resMoves(dr) {
  const xs = Object.entries(dr || {}).filter(([, v]) => Math.abs(v) >= 0.005);
  return xs.length ? xs.map(([k, v]) => `${ic(RES_ICON[k] || "dot")} ${ptsUp(v)}`).join(" &nbsp;") : "";
}
function personTip(id) {
  const p = castById(id);
  if (!p) return tipBox(`${ic("people")} Someone in the story`, "", [], "");
  const far = /^(old |former |ex$)/.test(p.role);
  return tipBox(`${ic(p.alive ? roleIcon(p.role) : "candle")} ${esc(p.name)}`, esc(cap(p.role)) + (p.alive ? (far ? ", far away now" : "") : ", gone"), [
    ["First met", p.met != null ? `at ${Math.floor(p.met)}` : "–"], ["In the story", `${p.seen} time${p.seen === 1 ? "" : "s"}`]],
    "");
}
function actTip(pl, it, el0text) {
  const { means, ends } = splitColors(pl);
  const rows = [], all = actColors(means, ends);
  if (all.length) rows.push(["Colors", pips(all) + " " + all.map((c) => CNAME[c]).join(" and ")]);
  if (it && it.ok != null) rows.push(["Result", it.ok ? `<span class="up">${ic("check")} it worked</span>` : `<span class="down">${ic("cross")} it went badly</span>`]);
  if (it && it.felt != null) rows.push(["Felt", `${fpct(it.felt)} likely; reality was ${hintWord(it.real - it.felt)}`]);
  if (it && it.pushed) rows.push(["You pushed", it.rel >= 0.05 ? `${it.rel < 0.3 ? "low" : it.rel < 0.6 ? "medium" : "high"} reluctance: stress and pent-up wanting` : "they hardly minded"]);
  if (it && it.dw) rows.push(["Colors moved", colorMoves(it.dw)]);
  if (it && it.dres && resMoves(it.dres)) rows.push(["Means moved", resMoves(it.dres)]);
  if (it && it.delta != null && Math.abs(it.delta) >= 0.15) rows.push(["Surprise", `<span class="${it.delta > 0 ? "up" : "down"}">${Math.abs(it.delta) >= 0.4 ? "much " : ""}${it.delta > 0 ? "better" : "worse"} than they expected</span>`]);
  return tipBox(`${ic("sign")} ${esc(cap(String(el0text || "The act")))}`, "", rows, "");
}
function mkTip(el) {
  const k = el.dataset.mk, pl = (el.dataset.pl || "").split("|");
  const host = el.closest("[data-i]"), it = host ? ITEMS[+host.dataset.i] : null;
  const L = hud && hud.life;
  switch (k) {
    case "p": return personTip(+pl[0]);
    case "a": return actTip(pl[0], it, el.textContent);
    case "w": return tipBox(`${ic("route")} What they wanted instead`, "", [], GATE[pl[0]] || "Something stood between them and what they wanted.");
    case "t": {
      const c = pl[0], v = c && COLORS.includes(c) ? voiceOf(c) : null;
      return tipBox(`${c && COLORS.includes(c) ? pip(c) : ic("voice")} A ${c && COLORS.includes(c) ? CNAME[c] + " " : ""}thought`, THOUGHT[pl[1]] || "",
        v != null ? [["In the story's voice", `${CNAME[c]} ${pct(v)} now`]] : [], "");
    }
    case "v": {
      const c = pl[0], i = COLORS.indexOf(c);
      const rows = L && L.w ? [["Now", pct(L.w[i])], ["Wants", `${pct(Math.max(0, L.w[i] + L.demand[i]))} (${updown(L.demand[i], 0, 100)} pts)`]] : [];
      return tipBox(`${pip(c)} ${CNAME[c]}: ${esc(VALUE[c])}`, CIDEA[c], rows, "");
    }
    case "m": return tipBox(`${ic("mood")} How the year feels`, "", [], bars([["Satisfaction", +pl[0], "var(--sat)", pct(+pl[0])], ["Peace", +pl[1], "var(--peace)", pct(+pl[1])]]) + "<p>Each year opens with its mood, told through their colors. Happy is not the same as at peace.</p>");
    case "d": return tipBox(`${ic("mood")} Since last year`, "", [["Satisfaction", ptsUp(+pl[0])]], "");
    case "s": return tipBox(`${pip(pl[0])} ${ic("push")} ${pip(pl[1])} The voice shifts`, "", [["Before", CNAME[pl[0]]], ["Now", CNAME[pl[1]]]], "The narrator's emphasis has moved: a change of identity is felt only once it has lasted.");
    case "k": {
      const n = pl[1].split(",").map(Number), top = Math.max(1, ...n);
      return tipBox(`${pip(pl[0])} Where the ordinary weeks went`, "", [], bars(COLORS.map((c, i) => [CNAME[c], n[i] / top, `var(--c${c})`, String(n[i])])) + "<p>Everyday acts count: every week spent one way makes that way a little more theirs.</p>");
    }
    case "f": return tipBox(`${ic("rain")} Small frictions`, "", [["This year", pl[0]]], "Daily irritations add up and wear on peace.");
    case "x": {
      const v = +pl[0], era = pl[1] === "era";
      return tipBox(`${ic(era ? "hourglass" : "globe")} How it landed`, "", [["Took it", tookWord(v)]],
        bars([["Pushed back", Math.max(0, -v), "var(--bad)", ""], ["Took it in", Math.max(0, v), "var(--ok)", ""]]) +
        `<p>${era ? "An era rewards some ways of living for years. Taking to it pulls their wanting toward its colors; resisting it pushes away." : `The event carried a message${COLORS.includes(pl[1]) ? ` (${CNAME[pl[1]]})` : ""}. Taking it in pulls their wanting that way; pushing back moves them away from it.`}</p>`);
    }
    case "e": return tipBox(`${ic("hourglass")} An era of ${esc(pl[0])}`, it && it.idea ? esc(it.idea) : "", [], "");
    case "O": return tipBox(`${ic(pl[1] || "ci-newspaper")} The world outside`, pl[2] === "1" ? "A big public event: everyone lives through it." : "It reaches their life, or their people.",
      [], hud && hud.world ? "The World panel (key g) has the public record and the history." : "");
    case "r": return tipBox(`${ic("scroll")} Read through their colors`, `“${esc(pl[0])}”`, [["How hard it hits", hitWord(+pl[1])]], "");
    case "c": {
      const kind = pl[0], ex = lettersOf(pl[1] || ""), t = L && (L.titles || []).find((x) => x.kind === kind);
      const rows = [];
      if (ex.length) rows.push(["It expects", pips(ex) + " " + ex.map((c) => CNAME[c]).join(" and ")]);
      if (t) rows.push(["Held now", `${Math.floor(t.years)} years · invested ${investWord(t.invested)}${t.clash ? ` · ${ic("bolt")} in a clash` : ""}`]);
      if (pl[2] && !["start", "inherited"].includes(pl[2])) rows.push(["What happened", esc(pl[2])]);
      return tipBox(`${ic(KIND_ICON[kind] || "anchor")} ${esc(cap(kind))}`, "", rows, "");
    }
    case "b": return tipBox(`${ic(pl[0] === "fit" ? "star" : "bolt")} Opposed colors joined`, "", [["How far apart", pct(+pl[1])]],
      pl[0] === "fit" ? "It worked, so both ways fit together: holding opposites gets easier." : "It failed, so it tore: holding opposites hurts, and they drift apart.");
    case "h": return tipBox(`${ic(pl[0] === "healed" ? "sprout" : "shield")} After the year's hardest blow`, "",
      [], bars([["The blow", (+pl[1]) / 3, "var(--bad)", pct((+pl[1]) / 3)], ["Support", +pl[2], "var(--peace)", pct(+pl[2])]]) +
      `<p>${pl[0] === "healed" ? "With support, a person comes back to their core." : "Alone, the blow hardens into who they are."}</p>`);
    case "q": return tipBox(`${ic(pl[0] === "trouble" ? "rain" : "sun")} A ${pl[0] === "trouble" ? "hard" : "lucky"} streak`, "", [["How strong", (+pl[1]) >= 1.8 ? "one thing after another" : "a run of it"]],
      pl[0] === "trouble" ? "Trouble makes more trouble likely for a while: one blow leaves less room for the next." : "Good fortune makes more good fortune likely for a while.");
    case "T": {
      const rows = (pl[0] || "").split(",").filter(Boolean).map((x) => { const m = x.match(/^([a-z_]+)([+-][\d.]+)$/); return m ? [TEMPER_NAME[m[1]] || m[1], ptsUp(+m[2])] : null; }).filter(Boolean);
      return tipBox(`${ic("mask")} Temperament`, "", rows, "");
    }
    case "R": return tipBox(`${ic("gate")} ${esc(cap((pl[0] || "").replace(/_/g, " ")))}`, "A new stage of life.", [], "");
    case "B": return tipBox(`${ic("burst")} A breakthrough`, "", [["Toward", `${pip(pl[0])} ${CNAME[pl[0]] || ""}`]], "What is denied builds up. Past its mark, pent-up wanting moves them on its own.");
    case "C": return tipBox(`${pip(pl[0])} ${ic("push")} ${pip(pl[1])} A lost faith`, "", [], `They stop believing in ${esc(VALUE[pl[0]] || "")}, and turn toward ${esc(VALUE[pl[1]] || "")}.`);
    case "i": return voiceTip(pl);
    case "j": return tipBox(`${ic("voice")} What bent this moment`, "", [], ASIDE[pl[0]] || "Something in who they are now.");
    case "g": return goalTip({ kind: pl[0], what: pl[1], colors: pl[2], domain: pl[3], source: pl[4], horizon: pl[5] });
    case "z": return changeTip(pl[0], +pl[1], +pl[2]);
    case "o": { const cur = findRole(pl[0]); return roleTip({ ...(cur || {}), name: pl[0], kind: pl[1], ways: pl[2], title: pl[3] === "1", plus: +pl[4] || 0, say: (cur && cur.say) || el.textContent }, cur); }
    case "y": return tipBox(`${pips(lettersOf(pl[0]))} Closer to ${esc(pl[1])}`, "", [["Still to go", `${(+pl[2] * 100).toFixed(1)} pts`]], "A color joins who they are above 22% and leaves below 18%.");
    case "n": return tipBox(`${ic("rune")} How the world works`, "", [], LESSON_WHY[pl[0]] || "What this week showed about the rules of a life.");
  }
  return "";
}

/* ---------------- v7: heart and head, what changed, dreams and plans ---------------- */
const DRV_TIP = { "what moves them": "their motives", "what they believe in": "their values" };
const ASIDE = { stressed: "Strain makes the heart louder and the head quieter.", little_control: "Self-control is low at this age and in this state: feelings mostly decide.",
  disciplined: "Plans kept and hard things done on purpose have made the head stronger.", undisciplined: "Giving in, again and again, has worn self-control down.",
  blind_spot: "The best way through is open, but they do not see it: what they notice first is shaped by their colors.", out_of_reach: "What their head would pick is closed to them here: no means, or nobody offers it.",
  hopeful: "Their outlook makes everything look likelier than it is.", gloomy: "Their outlook makes everything look less likely than it is.",
  short_horizon: "Time feels short, so what matters now outweighs what pays off later.", lean_other: "A choice is a draw, not a sum: people do not always do what they most want." };
const LESSON_WHY = { practice: "Skill grows with use.", hard_win: "Discipline is learned: hard wins on purpose build it.", self_control_up: "Discipline is learned: holding to a decision builds it.",
  self_control_down: "Giving in wears discipline down.", surprise_teaches: "The bigger the surprise, the more the colors move.", fail_own_ways: "A big failure in one's own ways turns a person toward what the moment needed.",
  defended: "A long-held way of acting is defended: one failure does not undo it.", habit: "Habits grow with each repeat.", door: "Some acts open doors: the surroundings shift.",
  binding: "Promises bind: they hold, and they cost freedom.", backfire: "Going against what is closed has a price.", need_met: "A need that was lacking lifts satisfaction most when it is met.",
  duty_kept: "Living up to a title deepens it.", commit_start: "A title brings its own ways and pulls toward them.", commit_end: "Leaving a title costs what was put in.",
  title_gain: "A new title brings its own ways and expectations, and what it gives and costs.", status_gain: "A status changes how others see them, and which doors open.",
  title_loss: "Losing a title takes the place it gave them.", perk_gain: "A skill, a bond or something owned makes some acts likelier to work, or opens doors.",
  perk_loss: "Without a perk some doors close; a skill fades slowly, so what was learned stays a while.", perk_helped: "What they had learned made the difference this time.",
  goal_step: "Steps that work feed a dream or plan.", goal_setback: "Setbacks weaken a goal, more so with self-doubt.", sealed: "Tries that worked and felt one's own make a dream a passion.",
  goal_end: "Every dream and plan ends somehow: done, given up or out of time.", loss: "Losing someone close makes time feel shorter.", stress_up: "Stress makes the next choice more impulsive.",
  regret: "Heart over head, then failure: regret.", rite: "A passage into a new stage of life.", turning_point: "Doubts that pile up turn a person.", breakthrough: "A want held back long enough breaks through.",
  closer_to: "Colors move a person toward a new identity.", drifting_from: "A color that falls away changes who they are, too: what stays defines them." };
function voiceTip(pl) {
  const v = hud && hud.cp && hud.cp.voice, sc = +pl[3];
  const rows = [["Heart wants", `${ic("heart")} ${esc((v && v.heart_driver) || pl[1] || "–")}`], ["Head says", `${ic("head")} ${esc((v && v.head_driver) || pl[2] || "–")}`]];
  return tipBox(`${ic("voice")} The inner voice`, `The head decides ${pct(sc)} of it now, the heart ${pct(1 - sc)}.`, rows, tugBar(sc));
}
function tugBar(sc, id) { return `<span class="tug"${id ? ` id="${id}"` : ""} style="--h:${((1 - sc) * 100).toFixed(0)}%"><span class="hrt">${ic("heart")}${pct(1 - sc)}</span><span class="tbar"><i></i></span><span class="hd">${pct(sc)}${ic("head")}</span></span>`; }
const NEED_ICON = { safety: "shield", belonging: "people", autonomy: "feather", competence: "star", meaning: "compass", ...GI.need };
// needs (IDEAS.md, "Make needs visible and learnable"): the five levels in the side panel, and what feeds each
const NEED_SHORT = { safety: "Safety", belonging: "Belonging", autonomy: "Own choice", competence: "Skill", meaning: "Meaning" };
const NEED_LONG = { safety: "safety", belonging: "belonging", autonomy: "room to choose", competence: "a sense of skill", meaning: "meaning" };
const NEED_FEEDS = {
  safety: "Acts that work, toward any color's ends (White most); money, health, a partner, a career, a safe place to live.",
  belonging: "Acts that work toward Red and Green ends most; friends and ties, a partner, children, a community or faith.",
  autonomy: "Acting in their own strongest colors; free time and freedom. Acting against who they are drains it a little.",
  competence: "Succeeding at something hard for them, in any color; a career. Failing drains it a little.",
  meaning: "Acts that work toward Blue and Black ends most; doing right by people who depend on them; children, faith, a career." };
const needWord = (v) => v >= 0.75 ? "well met" : v >= 0.5 ? "met" : v >= 0.3 ? "thin" : "barely met";
function needsRowHTML(L) {
  const N = L.needs || {};
  if (!Object.keys(N).length) return "";
  return `<div class="needs5" aria-label="Needs">${Object.entries(N).map(([k, v]) => `<div class="nd${v < 0.3 ? " barely" : v < (L.need_thin || 0.5) ? " thin" : ""}" data-nd="${k}" tabindex="0" aria-label="${esc(NEED_SHORT[k] || k)}: ${pct(v)}, ${needWord(v)}">${ic(NEED_ICON[k] || "dot")}<span class="lv">${pct(v)}</span><small>${esc(NEED_SHORT[k] || k)}</small></div>`).join("")}</div>`;
}
function needTip(k, L) {
  const v = (L.needs || {})[k] ?? 0;
  return tipBox(`${ic(NEED_ICON[k] || "dot")} ${esc(cap(NEED_LONG[k] || k))}`, "", [["Now", `${pct(v)}, ${needWord(v)}`], ["Fed by", esc(NEED_FEEDS[k] || "")]],
    "Every need fades a little each week unless something feeds it. A lacking need pulls satisfaction down, and meeting it lifts satisfaction most.");
}
const CHG = { content: [GI.meter.content || "mood", "var(--sat)", "Satisfaction"], peace: [GI.meter.peace || "leaf", "var(--peace)", "Peace"], mood: ["sun", "var(--sat)", "Mood"], stress: [GI.meter.strain || "bolt", "var(--stress)", "Strain", -1],
  outlook: ["sun", "var(--gold2)", "Outlook"], discipline: ["anchor", "var(--head)", "Self-control"], horizon: ["hourglass", "var(--arcane)", "Felt time", 0] };
function chgInfo(what) {          // icon html, accent color, name, good direction (1 up is good, -1 down is good, 0 neutral)
  const [k, x] = what.split(":");
  if (k === "color") return [pip(x), `var(--c${x})`, CNAME[x], 0];
  if (k === "res") return [ic(RES_ICON[x] || "dot"), "var(--gold)", cap(x), 1];
  if (k === "need") return [ic(NEED_ICON[x] || "dot"), "var(--peace)", "Need: " + x, 1];
  if (k === "skill") return [`${ic("bulb")}${pip(x)}`, `var(--c${x})`, `Skill in ${CNAME[x]} ways`, 1];
  if (k === "strength") return [ic(KIND_ICON[x] || "anchor"), "var(--gold)", `Bond to the ${x}`, 0];
  const c = CHG[k] || ["dot", "var(--gold)", cap(k), 1];
  return [ic(c[0]), c[1], c[2], c[3] ?? 1];
}
function chgChip(c, big) {
  const [icon, col, , good] = chgInfo(c.what), up = c.delta > 0, g = good === 0 ? "nu" : (up ? 1 : -1) * good > 0 ? "up" : "down";
  return `<span class="chg${big ? " big" : ""}" data-z="${esc(c.what)}|${c.delta}|${c.size}" style="--cc:${col}">${icon}<span>${esc(c.word)}</span><span class="ar ${g}">${up ? "▲" : "▼"}</span></span>`;
}
function changeTip(what, d, size) {
  const [icon, , name] = chgInfo(what);
  const k = what.split(":")[0];
  const big = Math.abs(d) * 100;
  const shown = k === "color" ? `${sgn(d * 100, 1)} pts` : (d > 0 ? "+" : "−") + (big >= 1 ? Math.round(big) : big.toFixed(1)) + "%";
  return tipBox(`${icon} ${esc(name)}`, "", [["This week", `<span class="${d > 0 ? "up" : "down"}">${shown}</span>`], ["How big", size >= 3 ? "a week to remember" : size >= 1 ? "a notable week" : "a small move"]],
    "");
}
const GOAL_ICON = { dream: "moon", passion: "flame", plan: "target", ...GI.goal };
const GOAL_WHAT = { begins: "begins", "became a passion": "becomes a passion", "became a plan": "becomes a plan", achieved: "comes true", "let go": "is let go",
  "not reached in time": "runs out of time", "pushed aside": "is crowded out", extended: "gets more time" };
const GOAL_SRC = { family: "from family", circle: "from people around them", story: "from a story", spectacle: "from a spectacle", stranger: "from a stranger",
  resolution: "a resolution", passion: "from a passion", need: "from a need", "old dream": "an old dream come back", dream: "from a dream", player: "set by you" };
const GOAL_HELP = { dream: "Dreams come from admired people and from stories, read through their own colors. They pull on what the character does.",
  passion: "A passion is a dream sealed by tries that worked and felt like their own. It lasts, and it can bring plans.",
  plan: "A plan has a horizon: a week, a year, five years or a life. Reaching one builds self-control; giving one up wears it down." };
function goalTip(g, item) {
  const cs = lettersOf(g.colors || (item && item.colors) || "");
  const rows = [];
  if (g.what) rows.push(["What happened", esc(GOAL_WHAT[g.what] || g.what)]);
  if (cs.length) {                     // a group of colors goes by Chroma's own name (Emren 20:46, point 16)
    const gn = cs.length > 1 ? ((hud && hud.life && hud.life.guilds) || {})[COLORS.filter((c) => cs.includes(c)).join("")] : "";
    rows.push(["In the ways of", pips(cs) + " " + cs.map((c) => CNAME[c]).join(" and ") + (gn ? ` <span class="muted">(${esc(gn)})</span>` : "")]);
  }
  if (item && item.dream && item.kind !== "dream") rows.push(["From the dream of", esc(item.dream)]);
  if (g.domain) rows.push(["About", `${ic(KIND_ICON[g.domain] || "anchor")} ${esc(g.domain)}`]);
  if (g.source) rows.push(["Where it came from", esc(GOAL_SRC[g.source] || g.source)]);
  if (g.horizon) rows.push(["Horizon", esc(g.horizon)]);
  if (item) {
    rows.push(["Strength", `${pct(item.strength)}`]);
    if (item.kind === "plan") {
      rows.push(["Feels", `${fpct(item.felt)} sure it will come true` + (item.felt0 != null && Math.abs(item.felt - item.felt0) >= 0.05 ? ` (was ${fpct(item.felt0)})` : "")]);
      rows.push(["Reality, roughly", `plans like it come true ${esc(item.hint)}`], ["Due", `at ${Math.floor(item.due)}`], ["Done so far", pct(item.progress)]);
      if (item.left_out && item.left_out.length) rows.push(["The feeling leaves out", esc(item.left_out.join(", "))]);
    }
  }
  return tipBox(`${ic(GOAL_ICON[g.kind] || "moon")} ${esc(cap(g.kind))}${item ? ": " + esc(item.name) : ""}`, "", rows, GOAL_HELP[g.kind] || "");
}

/* ---------------- worker link ---------------- */
let worker = null, ready = false, busy = false, hud = null, selected = null, digitBuf = "", digitTimer = null;
const stick = { bottom: true };
chronEl.addEventListener("scroll", () => { stick.bottom = chronEl.scrollHeight - chronEl.scrollTop - chronEl.clientHeight < 90; });
function send(text) {
  lastSent = text;
  if (!ready || busy) return;
  // Emren 10-07 01:57 (N3): a choice shows at once that it is being lived, and its outcome comes in the same window;
  // "Go on" closes the window before the weeks pass. sentFrom keeps the interlude out of the choice itself.
  const inPlay = hud && hud.mode === "play" && !hud.plan;
  sentFrom = inPlay && hud.cp && (text === "" || /^\d+$/.test(text)) ? "cp" : inPlay && hud.res && (text === "" || ["w", "m", "y", "d"].includes(text)) ? "res" : "";
  hideTip(); busy = true;
  if (sentFrom === "cp") markChoosing(text); else if (sentFrom === "res") closeEv();
  renderTransport(); lockInputs(true);
  worker.postMessage({ cmd: "line", text });
}
let sentFrom = "", choosing = null;
function markChoosing(text) {
  if (evWrap.hidden || !hud.cp) return;
  const o = text === "" ? hud.cp.options.find((x) => x.own) : hud.cp.options.find((x) => String(x.n) === text);
  choosing = { t: performance.now() };
  tableEl.classList.add("choosing");
  tableEl.querySelectorAll(".optdetail").forEach((x) => x.remove());
  tableEl.querySelectorAll(".opt").forEach((b) => b.classList.toggle("chosen", !!o && hud.cp.options[+b.dataset.i] === o));
  const ch = tableEl.querySelector(".opt.chosen"); if (ch) ch.scrollIntoView({ block: "nearest" });
  const f = tableEl.querySelector(".evf"), nm = (hud.life && hud.life.name) || "They";
  if (f) f.innerHTML = `<div class="trying" role="status"><span class="spin"></span><span><b>${esc(nm)}</b> ${text === "" ? "chooses for themselves" : "tries it"}<span class="dots"><i>.</i><i>.</i><i>.</i></span></span><span class="tbar"><i></i></span></div>`;
  const st = $("evStrip"); if (st && o) { st.classList.remove("idle"); st.innerHTML = `<div class="dt">${esc(nm)} ${text === "" ? "chooses for themselves" : "tries it"}: ${esc(cap(o.label))}</div>`; }
  if (ch && !narrow()) flyUp(ch);
}
// v22 next look, the one signature motion: the chosen card rises to the middle of the window with a gold ring, and when
// the outcome comes it turns over to its verdict, then gives way to the outcome window. Honours reduced motion.
const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let flyer = null;
function flyUp(card) {
  dropFlyer();
  if (reducedMotion()) return;
  const r = card.getBoundingClientRect(), box = tableEl.getBoundingClientRect();
  const w = Math.min(380, Math.max(300, r.width)), h = Math.max(r.height, 96);
  const el = document.createElement("div"); el.className = "flyer"; el.setAttribute("aria-hidden", "true");
  el.style.cssText = `left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px`;
  el.innerHTML = `<div class="fin"><div class="face front paper"><div class="optlook">${card.innerHTML}</div></div><div class="face back paper"></div></div><span class="fring"></span>`;
  document.body.appendChild(el); flyer = el; card.classList.add("lifted");
  const tx = box.left + box.width / 2 - w / 2, ty = box.top + box.height * 0.42 - h / 2;
  el.animate([{ left: r.left + "px", top: r.top + "px", width: r.width + "px", height: r.height + "px" },
    { left: tx + "px", top: ty + "px", width: w + "px", height: h + "px" }], { duration: 440, easing: "cubic-bezier(.2,.7,.2,1)", fill: "forwards" });
  el.classList.add("up");
}
function flipFlyer(worked, words) {
  const el = flyer; if (!el) return;
  const back = el.querySelector(".back");
  back.innerHTML = `<span class="fseal ${worked ? "ok" : "bad"}">${ic(worked ? "check" : "cross")}</span><b>${esc(words)}</b>`;
  el.classList.add("flip");
  setTimeout(() => { el.classList.add("gone"); setTimeout(() => { if (el.parentNode) el.remove(); if (flyer === el) flyer = null; }, 360); }, 900);
}
function dropFlyer() { if (flyer && flyer.parentNode) flyer.remove(); flyer = null; }
function closeEv() {
  if (evWrap.hidden) return;
  evWrap.classList.add("leaving"); tableEl.classList.remove("choosing");
  setTimeout(() => { evWrap.classList.remove("leaving"); if (busy || !(hud && (hud.cp || hud.res))) { showEv(false); tableEl.innerHTML = ""; lastCpKey = ""; } }, 180);
}
function pause() { if (worker && busy) worker.postMessage({ cmd: "stop" }); if (IL.on) ilFinish(); }
function toast(msg) {
  if (!msg) return;
  toastEl.textContent = msg; toastEl.classList.add("on");
  clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove("on"), 2200);
}
function lockInputs(on) { document.querySelectorAll(".tarot, .opt, #pushIt, #evLet, #goOn, .steps4 button, .ch, .tools [data-key]").forEach((b) => { b.disabled = on || b.hasAttribute("data-held") || (b.closest(".steps4") && !!(hud && (hud.cp || hud.mode !== "play"))); }); }

/* ---------------- the chronicle (the story, the main text) ---------------- */
let curYear = null, prologue = null, lastGuild = null;
let ITEMS = [], MARKS = [];
const yearEls = new Map(), WORLD_SEEN = new Map();
const TAG_ICON = { birth: "sprout", start: "voice", choice: "sign", moment: "dot", ordinary: "dot", loss: "candle", death: "candle", crisis: "storm",
  outside: "globe", move: "route", era: "hourglass", read: "scroll", clash: "bolt", rite: "gate", turn: "compass", breakthrough: "burst",
  healed: "sprout", hardened: "shield", trouble: "rain", fortune: "sun", temper: "mask", ledger: "book", note: "dot", goal: "moon", memory: "ci-diary", kin: "ci-birth", hint: "compass", ...GI.tag };
const KIND_ICON = { career: "case", partner: "heart", children: "child", community: "people", faith: "shrine", ...GI.kind };
const TAG_WORD = { choice: "Your moment", loss: "Loss", death: "Death", crisis: "Crisis", move: "A move", era: "The times", read: "Public life",
  clash: "Clash", rite: "A new stage", turn: "Turning point", breakthrough: "Breakthrough", healed: "Carried through", hardened: "Hardened",
  trouble: "Hard streak", fortune: "Lucky streak", temper: "Temperament", outside: "The world", commitment: "A title", moment: "A moment",
  ordinary: "Everyday", birth: "Birth", kin: "Family", start: "Your voice", note: "Note", hint: "How needs work", goal: "Dreams and plans", role: "Titles and perks" };
const MINOR = new Set(["ordinary", "note", "outside", "read", "era", "temper"]);
const isMinor = (it) => MINOR.has(it.tag) || (it.tag === "role" && !it.title);      // a perk's line is a small one; a title's is not
const MARK_PRI = { death: 9, loss: 9, commitment: 8, clash: 7, turn: 7, breakthrough: 7, choice: 6, crisis: 6, move: 5, rite: 5, healed: 4, hardened: 4, goal: 3, trouble: 3, fortune: 3, role: 3, era: 2 };
// titles and perks (Emren 12:05): icons by perk kind and by status; a title of a life domain takes the domain's icon
const PERK_ICON = { skill: "ci-anvil", credential: "ci-diploma", standing: "ci-medal", bond: "ci-handshake", asset: "ci-open-chest" };
const PERK_KIND_WORD = { skill: "A skill", credential: "A credential", standing: "Standing", bond: "A bond", asset: "Something of their own" };
const STATUS_ICON = { graduate: "ci-mortarboard", veteran: "ci-swords", "has killed in war": "ci-swords", widowed: "ci-candle", retiree: "ci-bench",
  homeowner: "ci-key", newcomer: "ci-suitcase", immigrant: "ci-globe", "someone with a record": "ci-gavel", "ex-prisoner": "ci-broken-chain", "in recovery": "ci-sapling",
  divorced: "ci-heartbreak", "eldest child": "ci-domain-family", "carer for a parent": "ci-hand-on-heart", homeless: "ci-box", "out of work": "ci-door-shut",
  "cancer survivor": "ci-domain-health", "left the faith": "ci-door-open", "doctoral graduate": "ci-diploma",
  "first-generation university student": "ci-domain-study", "former foster child": "ci-teddy-bear", "adopted person": "ci-holding-hands", refugee: "ci-tent",
  "asylum applicant": "ci-letter", "naturalised citizen": "ci-flag", "bankruptcy or insolvency in their history": "ci-wallet",
  "on probation or community supervision": "ci-chain", "living in residential care": "ci-elder", "returned migrant": "ci-u-turn", "displaced by a disaster": "ci-storm" };
const roleIconOf = (d) => d.title ? (d.kind === "status" ? STATUS_ICON[d.name] || "ci-shield" : KIND_ICON[d.kind] || "anchor") : PERK_ICON[d.kind] || "star";
const iconFor = (it) => it.tag === "commitment" ? (KIND_ICON[it.kind] || "anchor") : it.tag === "goal" ? (GOAL_ICON[it.kind] || "moon") : it.tag === "role" ? roleIconOf(it) : (TAG_ICON[it.tag] || "dot");
function resetChron() {
  feedEl.innerHTML = ""; curYear = null; prologue = null; lastGuild = null; ITEMS = []; MARKS = []; yearEls.clear(); WORLD_SEEN.clear(); stick.bottom = true;
}
function foldOld() {
  const yrs = feedEl.querySelectorAll(".yr:not(.prologue)");
  for (let i = 0; i < yrs.length - 4; i++) if (!yrs[i].dataset.user) yrs[i].classList.add("closed");
}
function newYear(it) {
  const sec = document.createElement("section"); sec.className = "yr"; sec.dataset.age = it.age;
  const cs = labelColors(it.label), fresh = it.guild !== lastGuild; lastGuild = it.guild;
  sec.innerHTML = `<div class="yh"><span class="ag"><small>AGE</small>${it.age}</span>${cs.length ? `<span class="gd">${pips(cs)}${fresh ? `<span>${esc(it.guild)}</span>${it.epithet ? `<span class="ep">${esc(it.epithet)}</span>` : ""}` : ""}</span>` : ""}<span class="rule"></span><span class="icons"></span><span class="mood"><b style="height:${(3 + 11 * clamp(it.content)).toFixed(1)}px;background:var(--sat)"></b><b style="height:${(3 + 11 * clamp(it.peace)).toFixed(1)}px;background:var(--peace)"></b></span></div><p class="lead" hidden></p><div class="ents"></div>`;
  const head = sec.firstChild;
  setTip(head, () => tipBox(`Age ${it.age} · ${esc(cap(it.stage))}`, it.guild ? `${pips(cs)} ${esc(it.guild)}${it.epithet ? ", " + esc(it.epithet) : ""}` : "Colors still forming", [],
    bars([["Satisfaction", it.content, "var(--sat)", pct(it.content)], ["Peace", it.peace, "var(--peace)", pct(it.peace)]].concat(
      COLORS.map((c, i) => [CNAME[c], it.w[i] / 0.6, `var(--c${c})`, pct(it.w[i])]))) + `<p>${sec.classList.contains("closed") ? "Click to open the year." : "Click to fold the year."}</p>`));
  head.addEventListener("click", () => { sec.classList.toggle("closed"); sec.dataset.user = "1"; hideTip(); });
  sec._ents = sec.querySelector(".ents"); sec._icons = sec.querySelector(".icons"); sec._lead = sec.querySelector(".lead"); sec._seen = new Set();
  feedEl.appendChild(sec); yearEls.set(it.age, sec);
  foldOld();
  return sec;
}
function addEntry(it) {
  if (it.tag === "year") { if (curYear) { curYear._lead.hidden = false; curYear._lead.innerHTML = rich(it.text); curYear._lead.dataset.i = it._i; } return; }
  if (!curYear && !prologue) {
    prologue = document.createElement("section"); prologue.className = "yr prologue";
    const e = document.createElement("div"); e.className = "ents"; prologue.append(e); prologue._ents = e; feedEl.appendChild(prologue);
  }
  const host = curYear ? curYear._ents : prologue._ents;
  const el = document.createElement("div");
  const name = iconFor(it);
  // v22 next look: the world's news folds into one "In the world" line per year (each piece keeps its own item, for the
  // marks and the life line), and a line already told in the last three years is not told again
  if (it.tag === "world" && /^⟦O:[^⟧|]*\|[^⟧|]*\|1⟧/.test(it.text || "")) {
    const key = String(it.text || "").replace(/⟦[^⟧]*⟧/g, "").replace(/\s+/g, " ").trim().toLowerCase();
    const seen = WORLD_SEEN.get(key);
    if (seen != null && (it.age ?? 0) - seen < 3) return;
    WORLD_SEEN.set(key, it.age ?? 0);
    const sec = curYear || prologue, piece = `<span class="wp" id="it${it._i}" data-i="${it._i}">${rich(it.text)}</span>`;
    if (sec._world) { sec._world.insertAdjacentHTML("beforeend", piece); return; }
    el.className = "en world minor wline"; el.dataset.i = it._i;
    el.innerHTML = `<span class="gut">${ic("ci-newspaper")}</span><span class="wk">In the world</span>${piece}`;
    setTip(el.querySelector(".gut"), () => tipBox(`${ic("ci-newspaper")} In the world`, "The public news of this year: everyone lives through it. What reaches their own life is told on its own line.", [], ""));
    sec._world = el; host.appendChild(el); return;
  }
  el.className = "en " + it.tag + (isMinor(it) ? " minor" : ""); el.dataset.i = it._i; el.id = "it" + it._i;
  if (it.tag === "ledger") { el.textContent = it.text.trim(); host.appendChild(el); return; }
  if (it.tag === "start") { el.textContent = it.text.replace(/=+/g, "").trim(); host.appendChild(el); return; }
  let res = "";
  if (it.tag === "choice") {
    const { means, ends } = splitColors(it.colors);
    const cs = [...new Set(means.concat(ends))];
    el.style.setProperty("--edge", cs.length === 1 ? `var(--c${cs[0]})` : cs.length ? `linear-gradient(180deg, ${cs.map((c) => `var(--c${c})`).join(", ")})` : "var(--gold)");
    res = `<span class="res">${it.pushed ? `${ic("push")} pushed ` : ""}${it.ok ? `<span class="ok">${ic("check")}</span>` : `<span class="bad">${ic("cross")}</span>`}</span>`;
  }
  let chips = "";
  if (it.tag === "choice" && it.res) {
    const r = it.res;
    chips = (r.heart || r.head ? `<span class="tag ${r.heart && r.head ? "head" : r.heart ? "heart" : "head"}">${ic(r.heart && !r.head ? "heart" : "head")}${r.heart && r.head ? "heart and head" : r.heart ? "heart" : "head"}</span>` : "") +
      (r.regret ? `<span class="tag regret">${ic("rain")}regret</span>` : "") + (r.became || []).map((c) => chgChip(c)).join("") +
      (r.closer && r.closer.distance < 0.05 ? `<span class="tag" data-y="1">${pips(lettersOf(r.closer.identity))}closer to ${esc(r.closer.guild)}</span>` : "") +
      (r.lesson ? `<span class="tag" data-n="1">${ic("rune")}</span>` : "");
    chips = chips ? `<div class="rchips">${chips}</div>` : "";
  }
  el.innerHTML = `<span class="gut${name === "dot" ? " nod" : ""}">${ic(name)}</span>${res}${rich(it.text)}${chips}`;
  if (it.tag === "choice" && it.res) el.classList.add("fresh");
  if (chips) {
    el.querySelectorAll("[data-z]").forEach((x) => { const z = x.dataset.z.split("|"); setTip(x, () => changeTip(z[0], +z[1], +z[2])); });
    const ly = el.querySelector("[data-n]"); if (ly) setTip(ly, () => tipBox(`${ic("rune")} How the world works`, rich(it.res.lesson.line), [], LESSON_WHY[it.res.lesson.key] || ""));
    const cy = el.querySelector("[data-y]"); if (cy) setTip(cy, () => tipBox(`${pips(lettersOf(it.res.closer.identity))} Closer to ${esc(it.res.closer.guild)}`, "", [["Still to go", `${(it.res.closer.distance * 100).toFixed(1)} pts`]], ""));
    el.querySelectorAll(".tag.heart, .tag.head").forEach((x) => setTip(x, () => tipBox(`${ic("voice")} Heart and head`, "", [], it.res.heart && it.res.head ? "Heart and head wanted the same thing, and they did it." : it.res.heart ? "They followed the heart over the head." : "They followed the head over the heart.")));
  }
  setTip(el.querySelector(".gut"), () => tipBox(`${ic(name)} ${esc(TAG_WORD[it.tag] || cap(it.tag))}`, it.sit ? esc(cap(it.sit)) : it.tag === "role" ? esc(cap(it.name) + ": " + it.what) : it.kind ? esc(cap(it.kind) + (it.what ? ": " + it.what : "")) : "", [["Age", (it.age ?? 0).toFixed(1)]]));
  host.appendChild(el);
  if (curYear && !isMinor(it) && !curYear._seen.has(name) && curYear._seen.size < 6) {
    curYear._seen.add(name); curYear._icons.insertAdjacentHTML("beforeend", ic(name));
  }
}
function addFeed(items) {
  for (const it of items || []) {
    if (it.tag === "birth") resetChron();
    it._i = ITEMS.length; ITEMS.push(it);
    if (it.tag === "chapter") curYear = newYear(it); else addEntry(it);
    if (MARK_PRI[it.tag] && !(it.tag === "commitment" && it.what === "inherited") && !(it.tag === "role" && !it.title)) MARKS.push(it);
  }
  if (items && items.length && stick.bottom) chronEl.scrollTop = chronEl.scrollHeight;
}
function openYear(age, itemIndex) {
  let sec = yearEls.get(age);
  if (!sec) { const ages = [...yearEls.keys()].filter((a) => a <= age); if (ages.length) sec = yearEls.get(Math.max(...ages)); }
  if (!sec) return;
  sec.classList.remove("closed"); sec.dataset.user = "1";
  const target = itemIndex != null ? document.getElementById("it" + itemIndex) : null;
  (target || sec).scrollIntoView({ block: target ? "center" : "start", behavior: "smooth" });
  sec.classList.remove("flash"); void sec.offsetWidth; sec.classList.add("flash");
  stick.bottom = false;
}

/* ---------------- part 1: the whole life as a line (the end is unknown: fog) ---------------- */
const SPAN = 100;
function curve(pts, first) {
  let d = (first ? "M" : "L") + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    const c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6, c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += `C${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
}
let lineGeo = null;
/* ---------------- part 1: the whole life as a line (the end is unknown: fog) ----------------
   parts/line.js, the zoomed life line after the approved mockup (Emren, 10-07): the lived years fill about three quarters
   of the strip, the years ahead are folded into the starry fog, identity runs as a thin band under the river, the events
   sit in a row under it. Replaces function drawLine() in app.js. Uses SPAN, curve, trunc, cosmos, lineGeo (keep
   `let lineGeo = null;`), and the shared helpers; cosmos(), the motes, scheduleLine and the ResizeObserver are unchanged. */

// One mapping for everything (river, band, glyphs, ticks, hover, clicks, fog). The lived years [0, now] take 74% of the
// inner width (a small child less: from 30% at birth, easing up to 74% at 8, so a first year is not absurdly wide); the
// years ahead, to SPAN, share the rest on a softened square root, so the near decades get more room than the far ones.
// When the life is over the lived span fills the whole width. A is the inverse of X.
function lnScale(W, pad, now, over) {
  const x0 = pad, xE = W - pad, t = clamp(now / 8);
  const f = over ? 1 : now <= 0 ? 0 : 0.3 + 0.44 * t * t * (3 - 2 * t);
  const xN = x0 + f * (xE - x0), fw = xE - xN, fy = Math.max(1e-6, SPAN - now);
  const E = 0.03, rE = Math.sqrt(E), K = Math.sqrt(1 + E) - rE;
  const X = (a) => a <= now ? (now > 0 ? x0 + (Math.max(0, a) / now) * (xN - x0) : x0)
    : over ? xE : xN + ((Math.sqrt(Math.min(1, (a - now) / fy) + E) - rE) / K) * fw;
  const A = (x) => {
    if (x <= xN || over || fw <= 0) return now > 0 && xN > x0 ? clamp((x - x0) / (xN - x0)) * now : 0;
    const q = Math.min(1, (x - xN) / fw) * K + rE;
    return now + (q * q - E) * fy;
  };
  return { X, A, x0, xN, xE };
}
// Rows from the strip's height: the river on top, the identity band right under it, the event glyphs, the age labels.
// 92 px on a desktop, 64 px on a phone (there the glyphs shrink to dots).
function lnLayout(H) {
  const sm = H < 80, tickY = H - (sm ? 4 : 6), gr = sm ? 2.8 : clamp(H * 0.082, 6.5, 9);
  const gy = tickY - 13 - gr, bandH = sm ? 3 : 3.5, bandY = gy - (sm ? 6.5 : gr + 4) - bandH;
  const top = sm ? 4 : 6, bot = bandY - (sm ? 2 : 3);
  return { sm, tickY, gr, gy, bandH, bandY, top, bot, mid: (top + bot) / 2, maxT: bot - top };
}
function lnF(v) { return (+v).toFixed(1); }
// The river: five stacked color bands whose thickness swells with satisfaction (r[6]), out of a point at birth.
function lnRiver(L, R, now, X, ly) {
  const eq = [0.2, 0.2, 0.2, 0.2, 0.2], norm = (s) => { const t = s.reduce((p, q) => p + q, 0) || 1; return s.map((v) => v / t); };
  const rows = R.map((r) => [r[0], norm(r.slice(1, 6)), clamp(r[6] || 0)]);
  if (!rows.length) { if (!(now > 0.05)) return ""; rows.push([now, eq, clamp(L.content == null ? 0.6 : L.content)]); }
  else {
    const last = rows[rows.length - 1];
    if (now - last[0] >= 0.25) rows.push([now, last[1], last[2]]);
    else if (now > last[0] && rows.length > 1) last[0] = now;       // too close for a smooth joint: stretch the last row
  }
  const T = (c) => ly.maxT * (0.42 + 0.58 * c), a1 = rows[0][0], s1 = rows[0][1], t1 = T(rows[0][2]);
  const pts = [[0, eq, 0.5]];
  for (const f of [0.06, 0.18, 0.36, 0.6, 0.82]) if (a1 * f > 0.04) pts.push([a1 * f, eq.map((v, k) => v + (s1[k] - v) * f), Math.max(0.5, t1 * Math.sqrt(f))]);
  for (const r of rows) pts.push([r[0], r[1], T(r[2])]);
  const edges = pts.map((p) => { let y = ly.mid - p[2] / 2; const e = [y]; for (let c = 0; c < 5; c++) { y += p[2] * p[1][c]; e.push(y); } return e; });
  const xs = pts.map((p) => X(p[0]));
  let layers = "";
  COLORS.forEach((c, k) => {
    const up = xs.map((x, i) => [x, edges[i][k]]), lo = xs.map((x, i) => [x, edges[i][k + 1]]).reverse();
    layers += `<path class="lay" fill="url(#lg${c})" d="${curve(up, true)}${curve(lo, false)}Z"/>`;
  });
  // drawn once, shown twice: the soft glow under the crisp bands
  return `<defs><g id="lnLays">${layers}</g></defs><use class="glowl" href="#lnLays"/><use class="lays" href="#lnLays"/><path class="sheen" d="${curve(xs.map((x, i) => [x, edges[i][0]]), true)}"/>`;
}
// Identity chapters as a thin band under the river: who they were, year by year, each identity blending into the next.
function lnBand(R, now, X, ly) {
  const runs = [];
  R.forEach((r, i) => {
    const a0 = i ? r[0] : 0, a1 = i + 1 < R.length ? R[i + 1][0] : now, l = r[8] || "";
    if (runs.length && runs[runs.length - 1].l === l) runs[runs.length - 1].a1 = a1; else runs.push({ l, a0, a1 });
  });
  if (!runs.length && now > 0.05) runs.push({ l: "", a0: 0, a1: now });
  if (!runs.length) return "";
  const xa = X(0), xb = Math.max(xa + 1, X(now)), off = (x) => clamp((x - xa) / (xb - xa)).toFixed(4);
  let stops = "";
  for (const u of runs) {
    const cs = lettersOf(u.l), parts = cs.length ? cs : [""], x0 = X(u.a0), w = Math.max(0, X(Math.min(u.a1, now)) - x0) / parts.length;
    parts.forEach((c, j) => {
      const p0 = x0 + w * j, e = Math.min(w * 0.3, 9), col = c ? `stop-color:var(--c${c});stop-opacity:0.95` : "stop-color:#d6cdf5;stop-opacity:0.2";
      stops += `<stop offset="${off(p0 + e)}" style="${col}"/><stop offset="${off(p0 + w - e)}" style="${col}"/>`;
    });
  }
  const y = ly.bandY, h = ly.bandH;
  return `<defs><linearGradient id="bandG" gradientUnits="userSpaceOnUse" x1="${lnF(xa)}" x2="${lnF(xb)}" y1="0" y2="0">${stops}</linearGradient></defs>` +
    `<rect class="bandglow" x="${lnF(xa)}" y="${lnF(y - 1)}" width="${lnF(xb - xa)}" height="${lnF(h + 2)}" rx="${lnF(h / 2 + 1)}" fill="url(#bandG)"/>` +
    `<rect class="band" x="${lnF(xa)}" y="${lnF(y)}" width="${lnF(xb - xa)}" height="${lnF(h)}" rx="${lnF(h / 2)}" fill="url(#bandG)"/>`;
}
// Events of the life at their ages, the most telling one where they crowd. A phone shows dots.
function lnGlyphs(byAge, now, X, ly, W) {
  const cand = [...byAge.entries()].map(([a, xs]) => [a, xs.slice().sort((p, q) => MARK_PRI[q.tag] - MARK_PRI[p.tag])]).sort((p, q) => MARK_PRI[q[1][0].tag] - MARK_PRI[p[1][0].tag] || p[0] - q[0]);
  const gr = ly.gr, gy = ly.gy, gap = ly.sm ? 8 : gr * 2 + 1.5, placed = [];
  let s = "";
  for (const [a, xs] of cand) {
    const x = clamp(X(clamp(a + 0.5, 0, now)), gr + 3, W - gr - 3);
    if (placed.some((px) => Math.abs(px - x) < gap)) continue;
    placed.push(x);
    const top1 = xs[0], cls = (MARK_PRI[top1.tag] >= 8 ? " big" : "") + (["death", "loss"].includes(top1.tag) ? " dark" : "") + (top1.tag === "choice" && !top1.ok ? " bad" : "");
    s += ly.sm
      ? `<g class="gl dot${cls}" data-age="${a}"><circle class="hit" cx="${lnF(x)}" cy="${lnF(gy)}" r="8"/><circle cx="${lnF(x)}" cy="${lnF(gy)}" r="${MARK_PRI[top1.tag] >= 8 ? 3.4 : gr}"/></g>`
      : `<g class="gl${cls}" data-age="${a}"><circle cx="${lnF(x)}" cy="${lnF(gy)}" r="${lnF(gr)}"/>${useIc(iconFor(top1), `x="${lnF(x - gr * 0.62)}" y="${lnF(gy - gr * 0.62)}" width="${lnF(gr * 1.24)}" height="${lnF(gr * 1.24)}"`)}</g>`;
  }
  return s;
}
// Age labels: in the lived part a readable step (1, 2, 5, 10 or 20 years, at least 46 px apart, 44 on a phone); in the fog the
// decades ahead, folded and fading with distance (thinned to every 20 or 50 years when they would crowd).
function lnTicks(now, over, S, ly, nx) {
  const { X, x0, xN } = S, ppy = now > 0 ? (xN - x0) / now : 0, gap = ly.sm ? 44 : 46, half = (a) => String(a).length * 3.3 + 1;
  const nowA = Math.floor(now + 1e-6), nowHalf = half(nowA);
  const step = [1, 2, 5, 10, 20, 25, 50].find((k) => k * ppy >= gap) || 100;
  let lived = "", grid = "", ahead = "";
  if (now > 0) for (let a = 0; a <= now + 1e-6; a += step) {
    const x = X(a);
    grid += `<line class="grid" x1="${lnF(x)}" x2="${lnF(x)}" y1="${lnF(ly.top)}" y2="${lnF(ly.bot)}"/>`;
    if (a === nowA || Math.abs(nx - x) < nowHalf + half(a) + 6) continue;
    lived += `<text class="tick known" x="${lnF(x)}" y="${ly.tickY}">${a}</text>`;
  }
  if (!over) {
    const fg = 26, px = (a) => Math.min(X(a), S.xE - half(a) + 8), far = (a) => now > 0 ? px(a) - nx >= nowHalf + half(a) + 8 : true;
    let as = [];
    for (const k of [10, 20, 50]) {
      as = []; for (let a = (Math.floor(now / k) + 1) * k; a <= SPAN; a += k) if (far(a)) as.push(a);
      if (as.every((a, i) => !i || px(a) - px(as[i - 1]) >= fg)) break;
    }
    for (const a of as) {
      const t = (a - now) / Math.max(1, SPAN - now);
      ahead += `<text class="tick fut" x="${lnF(px(a))}" y="${ly.tickY}" style="opacity:${(0.85 - 0.6 * t).toFixed(2)}">${a}</text>`;
    }
  }
  return { lived, grid, ahead, nowA };
}
// The hover: crosshair on the nearest river row and its tooltip, over the lived part only. The tip goes under the strip,
// so it never covers the year being read. Kept across redraws while the pointer rests on the river.
function lnHoverShow() {
  const G = lineGeo, h = lnHoverShow.at, cross = $("cross");
  if (!G || !h || !cross) return;
  const age = clamp(G.A(h.x), 0, G.now), R = G.R;
  let html, cx;
  if (R.length) {
    let best = R[0]; for (const row of R) if (Math.abs(row[0] - age) < Math.abs(best[0] - age)) best = row;
    cx = G.X(best[0]);
    const cs = lettersOf(best[8]);
    html = tipBox(`Age ${Math.round(best[0])}`, cs.length ? `${pips(cs)} ${esc((hud.life.guilds || {})[best[8]] || best[8])}` : "Colors still forming",
      [], bars(COLORS.map((c, i) => [CNAME[c], best[1 + i] / 0.6, `var(--c${c})`, pct(best[1 + i])]).concat([["Satisfaction", best[6], "var(--sat)", pct(best[6])], ["Peace", best[7], "var(--peace)", pct(best[7])]])) + "<p>The river swells when life is satisfying. Click to read that year.</p>");
  } else {
    cx = G.X(age);
    html = tipBox(`Age ${Math.round(age)}`, "Colors still forming", [], "The river takes its colors as the years leave their marks. Click to read that year.");
  }
  cross.setAttribute("x1", lnF(cx)); cross.setAttribute("x2", lnF(cx)); cross.setAttribute("visibility", "visible");
  showTipAt(html, h.cx, h.bottom);
  if (parseFloat(tipEl.style.top) < h.bottom) tipEl.style.top = h.bottom + 6 + "px";
}
function lnHoverOff() {
  if (!lnHoverShow.at) return;
  lnHoverShow.at = null;
  const cross = $("cross"); if (cross) cross.setAttribute("visibility", "hidden");
  if (tipOwner === "line") hideTip();
}
// Listeners live on the persistent svg (one set, delegated), so a redraw every few hundred ms costs no rebinding.
function lnWire() {
  if (lnWire.on) return;
  lnWire.on = true;
  const svgX = (e, r) => (e.clientX - r.left) * ((lineGeo ? lineGeo.W : r.width) / (r.width || 1));
  riverEl.addEventListener("pointermove", (e) => {
    if (!e.target || e.target.id !== "lineHov") { lnHoverOff(); return; }
    const r = riverEl.getBoundingClientRect();
    lnHoverShow.at = { x: svgX(e, r), cx: e.clientX, bottom: r.bottom };
    lnHoverShow();
  });
  riverEl.addEventListener("pointerleave", lnHoverOff);
  riverEl.addEventListener("click", (e) => {
    const G = lineGeo; if (!G || !e.target || !e.target.closest) return;
    const g = e.target.closest(".gl[data-age]");
    if (g) { const a = +g.dataset.age, xs = G.byAge.get(a) || []; hideTip(); openYear(a, xs[0] && xs[0]._i); return; }
    if (e.target.id === "lineHov") { const x = svgX(e, riverEl.getBoundingClientRect()); lnHoverOff(); hideTip(); openYear(Math.round(clamp(G.A(x), 0, G.now))); }
  });
}
function drawLine() {
  const W = Math.max(260, lineEl.clientWidth), H = Math.max(48, lineEl.clientHeight);
  const L = hud && hud.life, over = !!(hud && hud.mode === "over"), lived = !!(L && L.w);
  const now = lived ? Math.max(0, +L.age || 0) : 0, pad = W < 600 ? 12 : 16;
  const S = lnScale(W, pad, now, over), X = S.X, ly = lnLayout(H), nx = X(now);
  const R = (lived && L.river) || [];
  const byAge = new Map();
  for (const it of MARKS) { const a = Math.floor(it.age); if (!byAge.has(a)) byAge.set(a, []); byAge.get(a).push(it); }
  const tk = lnTicks(now, over, S, ly, nx);
  let s = `<defs>${COLORS.map((c) => `<linearGradient id="lg${c}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--c${c})" stop-opacity="0.96"/><stop offset="1" stop-color="var(--c${c})" stop-opacity="0.74"/></linearGradient>`).join("")}</defs>`;
  s += tk.grid;
  if (lived && !over) s += `<path class="path" d="M${lnF(nx)} ${lnF(ly.mid)}L${lnF(S.xE)} ${lnF(ly.mid)}"/>`;
  if (lived) s += lnRiver(L, R, now, X, ly) + lnBand(R, now, X, ly);
  s += tk.lived;
  const y1 = ly.top - 3, y2 = ly.bandY + ly.bandH + 3;
  s += `<line class="cross" id="cross" x1="0" x2="0" y1="${lnF(y1)}" y2="${lnF(y2)}" visibility="hidden"/>`;
  s += `<rect class="hov" id="lineHov" x="${lnF(S.x0)}" y="0" width="${lnF(lived ? Math.max(0, nx - S.x0) : 0)}" height="${lnF(y2 + 1)}"/>`;
  s += lnGlyphs(byAge, now, X, ly, W);
  // now: a gold line and a glowing bead on the river (drawn above the fog), at the end of a life the candle
  const nowLine = `<line class="nowg" x1="${lnF(nx)}" x2="${lnF(nx)}" y1="${lnF(y1)}" y2="${lnF(y2)}"/><line class="nowl" x1="${lnF(nx)}" x2="${lnF(nx)}" y1="${lnF(y1)}" y2="${lnF(y2)}"/>` +
    `<text class="nowt" x="${lnF(Math.min(nx, W - 6 - String(tk.nowA).length * 3.4))}" y="${ly.tickY}">${tk.nowA}</text>`;
  if (lived && over) {
    const cr = ly.sm ? 7 : 9;
    s += nowLine + `<g class="gl end"><circle cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${cr}"/>${useIc(GI.tag.death || "candle", `x="${lnF(nx - cr * 0.68)}" y="${lnF(ly.mid - cr * 0.68)}" width="${lnF(cr * 1.36)}" height="${lnF(cr * 1.36)}"`)}</g>`;
  }
  riverEl.setAttribute("viewBox", `0 0 ${W} ${H}`);
  riverEl.innerHTML = s;
  // above the fog: the identity thread going on into the unwritten years from who they are now, the decades ahead, now
  let ah = tk.ahead;
  if (lived && !over) {
    const xe = S.xE, y = lnF(ly.bandY + ly.bandH / 2), lc = lettersOf(L.label), c0 = lc.length ? `var(--c${lc[lc.length - 1]})` : "#d6cdf5";
    ah = `<defs><linearGradient id="aheadG" gradientUnits="userSpaceOnUse" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="0" y2="0"><stop offset="0" style="stop-color:${c0};stop-opacity:0.85"/><stop offset="0.2" style="stop-color:#d6cdf5;stop-opacity:0.3"/><stop offset="1" style="stop-color:#d6cdf5;stop-opacity:0.06"/></linearGradient></defs>` +
      `<line class="thread" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="${y}" y2="${y}" stroke="url(#aheadG)"/><line class="threadsh" x1="${lnF(nx)}" x2="${lnF(xe)}" y1="${y}" y2="${y}"/>` + ah +
      nowLine + `<circle class="nowhalo" cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${ly.sm ? 6 : 8.5}"/><circle class="nowdot" cx="${lnF(nx)}" cy="${lnF(ly.mid)}" r="${ly.sm ? 2.8 : 3.6}"/>`;
  }
  aheadEl.setAttribute("viewBox", `0 0 ${W} ${H}`);
  aheadEl.innerHTML = ah;
  cosmos(W, H);
  fogEl.style.left = Math.max(0, nx - 30) + "px";
  lineEl.classList.toggle("clear", over);
  lineEl.classList.toggle("nofogword", !over && S.xE - nx < 150);     // too little fog for the word UNWRITTEN
  lineGeo = { X, A: S.A, pad, W, now, R, byAge };
  lnWire();
  riverEl.querySelectorAll(".gl[data-age]").forEach((g) => {
    const xs = byAge.get(+g.dataset.age) || [];
    setTip(g, () => tipBox(`Age ${g.dataset.age}`, "", xs.slice(0, 5).map((it) => [ic(iconFor(it)), esc(trunc(plainText(it.text), 110))]), "Click to read it in the story."));
  });
  if (lnHoverShow.at) { if (lived && lnHoverShow.at.x <= nx) lnHoverShow(); else lnHoverOff(); }
}
const trunc = (s, n) => s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…" : s;
// The unwritten years as a cosmic fabric (Emren 10-07 01:57, N2a): stars, some twinkling, constellations in the five
// colors that come and go like lives that could be, and four-pointed sparks. Drawn once per size, anchored to the right
// edge of the line, so the fog uncovers the same sky as the life moves on.
function cosmos(W, H) {
  const el = $("cosmos");
  if (!el || (cosmos.w === W && cosmos.h === H)) return;
  cosmos.w = W; cosmos.h = H;
  let seed = 20261007; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const hue = ["W", "U", "B", "R", "G"], f = (v) => v.toFixed(1);
  let s = "";
  const n = Math.round((W * H) / 700);
  for (let i = 0; i < n; i++) {
    const x = rnd() * W, y = rnd() * H, r = 0.3 + Math.pow(rnd(), 3) * 1.2, tw = rnd() < 0.4, c = rnd() < 0.16 ? `var(--c${hue[Math.floor(rnd() * 5)]})` : "#ece6ff";
    s += `<circle${tw ? ' class="tw"' : ""} cx="${f(x)}" cy="${f(y)}" r="${r.toFixed(2)}" style="fill:${c};opacity:${(0.25 + rnd() * 0.6).toFixed(2)}${tw ? `;animation-delay:-${(rnd() * 8).toFixed(1)}s;animation-duration:${(2.5 + rnd() * 5).toFixed(1)}s` : ""}"/>`;
  }
  const k = Math.max(3, Math.round(W / 220));
  for (let j = 0; j < k; j++) {
    let x = W * (0.12 + 0.85 * rnd()), y = H * (0.2 + 0.6 * rnd());
    const pts = [[x, y]];
    for (let m = 0, mm = 3 + Math.floor(rnd() * 3); m < mm; m++) { x += 14 + rnd() * 34; y = clamp(y + (rnd() - 0.5) * 40, 8, H - 8); pts.push([x, y]); }
    const c = hue[j % 5], d = (rnd() * 14).toFixed(1);
    s += `<g class="con" style="--cc:var(--c${c});animation-delay:-${d}s"><polyline points="${pts.map((p) => f(p[0]) + "," + f(p[1])).join(" ")}"/>${pts.map((p) => `<circle cx="${f(p[0])}" cy="${f(p[1])}" r="1.3"/>`).join("")}</g>`;
  }
  for (let j = 0, m = Math.max(4, Math.round(W / 130)); j < m; j++) {
    const x = W * (0.08 + 0.9 * rnd()), y = H * (0.12 + 0.76 * rnd()), z = 2.5 + rnd() * 3.5, q = z * 0.22;
    s += `<path class="spark" style="animation-delay:-${(rnd() * 9).toFixed(1)}s;animation-duration:${(6 + rnd() * 6).toFixed(1)}s" d="M${f(x)} ${f(y - z)}L${f(x + q)} ${f(y - q)}L${f(x + z)} ${f(y)}L${f(x + q)} ${f(y + q)}L${f(x)} ${f(y + z)}L${f(x - q)} ${f(y + q)}L${f(x - z)} ${f(y)}L${f(x - q)} ${f(y - q)}Z"/>`;
  }
  el.setAttribute("viewBox", `0 0 ${W} ${H}`); el.style.width = W + "px";
  el.innerHTML = s;
}
(function motes() { for (let i = 0; i < 14; i++) { const b = document.createElement("b"); b.style.left = (8 + Math.random() * 88) + "%"; b.style.top = (10 + Math.random() * 78) + "%"; b.style.animationDelay = (Math.random() * 6).toFixed(2) + "s"; b.style.animationDuration = (4 + Math.random() * 5).toFixed(2) + "s"; fogEl.appendChild(b); } })();
let lineTimer = 0;
function scheduleLine() { if (lineTimer) return; lineTimer = requestAnimationFrame(() => { lineTimer = 0; drawLine(); }); }
new ResizeObserver(() => scheduleLine()).observe(lineEl);

/* ---------------- header and tools ---------------- */
$("brandPips").innerHTML = COLORS.map((c) => pip(c)).join("");
const SETTING_ICON = { earth: "globe", tribal: "flame", magic: "star", ...GI.setting, custom: "sliders" };
const SETTING_NAME = { earth: "Modern Earth", tribal: "Tribal", magic: "A world of magic" };
function renderWho(L) {
  if (!L) { whoEl.innerHTML = ""; return; }
  const lc = labelColors(L.label);
  whoEl.innerHTML = `<span class="nm">${esc(L.name)}</span><span class="age"><b>${Math.floor(L.age)}</b><small>${esc(L.stage || "")}</small></span>` +
    `<span class="crest">${lc.length ? pips(lc) : pip("W", "dim")}<span class="gn">${esc(L.guild || "Still forming")}</span></span>`;
  setTip(whoEl.querySelector(".crest"), () => tipBox(`${pips(lc)} ${esc(L.guild || "Still forming")}`, L.label ? esc(L.meaning || "") : "Too young for a formed identity yet.",
    L.label ? [["Colors", lc.map((c) => CNAME[c]).join(", ")]].concat(L.magic ? [["In Magic: The Gathering", esc(L.magic)]] : []) : [],
    L.label ? "A color joins who they are above 22% and leaves below 18%." : "An identity forms once enough has happened to them."));
  if (L.voice) {
    const vs = COLORS.map((c, i) => [c, L.voice[i]]).sort((a, b) => b[1] - a[1]);
    document.documentElement.style.setProperty("--t1", `var(--c${vs[0][0]})`);
    document.documentElement.style.setProperty("--t2", `var(--c${vs[1][0]})`);
  }
}
// v22 next look (Emren chose it 10-07 10:19): three labelled doors (Character, Book, World) and one Table menu for every
// setting; the menu stays open across state updates until it is closed
let menuOpen = false;
function renderTools(h) {
  const L = h && h.life;
  if (!L || !["play", "over"].includes(h.mode)) { toolsEl.innerHTML = ""; menuOpen = false; return; }
  const story = ["quiet", "normal", "every week"][L.detail];
  const row = (attr, icon, label, val, extra = "") => `<button class="mrow2" ${attr} role="menuitem"${extra}>${ic(icon)}<span class="t">${label}</span>${val != null ? `<span class="v">${val}</span>` : ""}</button>`;
  toolsEl.innerHTML = `
    <span class="savednote" id="savedNote" aria-live="polite">${autoOn ? `${ic("check")}<span>Saved after the last choice</span>` : ""}</span>
    <button class="tbtn hud-toggle" id="tHud" aria-pressed="${hudEl.classList.contains("open")}">${ic("wheel")}<span class="t">Status</span></button>
    <button class="tbtn door" data-page="c">${ic("ci-diary")}<span class="t">Character</span><kbd>c</kbd></button>
    <button class="tbtn door" data-page="b">${ic("ci-bookshelf")}<span class="t">Book</span><kbd>b</kbd></button>${h.world || L.world_era ? `
    <button class="tbtn door" data-page="g">${ic("ci-globe")}<span class="t">World</span><kbd>g</kbd></button>` : ""}
    <button class="tbtn door" id="tMenu" aria-haspopup="menu" aria-expanded="${menuOpen}">${ic("sliders")}<span class="t">Table</span></button>
    <div class="tpop" id="tPop" role="menu" aria-label="Table settings"${menuOpen ? "" : " hidden"}>
      <div class="pk">How the life is told</div>
      ${row('data-key="f"', "flag", "Moments", L.freq)}
      ${row('data-key="v"', "eye", "Story detail", story)}
      ${row('data-page="i"', "hourglass", "Interlude", PACE_WORD[ilPace])}
      ${row(`data-key="l" aria-pressed="${!!L.ledger}"`, "book", "Numbers under the story", L.ledger ? "on" : "off")}
      <div class="pk">This life</div>
      ${row(`data-page="a" aria-pressed="${autoOn}"`, "check", "Autosave after each choice", autoOn ? "on" : "off")}
      ${row(`data-page="s" id="tSave"${h.mode !== "play" ? " disabled" : ""}`, "ci-sealed-scroll", "Save to a file", "s")}
      ${row('data-page="o"', "ci-open-chest", "Load a life", "o")}
      ${row('data-page="n"', "new", "New life", "n")}
      ${row('id="tHelp"', "help", "Keys", "h")}
    </div>`;
  const tipsT = { f: () => tipBox(`${ic("flag")} Checkpoints: ${L.freq}`, "", [], "How often the life stops for you to steer: rare, normal, often or every moment. Key f."),
    v: () => tipBox(`${ic("eye")} Story: ${story}`, "", [], "How much of daily life the story tells: quiet, normal or every week. Key v."),
    l: () => tipBox(`${ic("book")} Ledger ${L.ledger ? "on" : "off"}`, "", [], "Show the engine's numbers under the story. Key l."),
    i: () => tipBox(`${ic("hourglass")} Interlude: ${PACE_WORD[ilPace]}`, "", [], "The everyday life between two moments: slow, short or off. Key i."),
    c: () => tipBox(`${ic("ci-diary")} Character sheet`, "", [], "Everything about them on one page. Key c."),
    b: () => tipBox(`${ic("ci-bookshelf")} The Book of Moments`, "", [], "What all your lives have met: moments (rare ones starred), identities, deeds and titles. Key b."),
    s: () => tipBox(`${ic("ci-sealed-scroll")} Save`, autoOn ? "Autosave is on" : "Autosave is off", [], `Save this life to a file. Key s.<br>${autoOn ? "After every moment and every choice the life is also kept in one slot in this browser, overwritten each time; Continue on the start screen opens it." : "Nothing is kept in this browser between choices."} Key a turns autosave ${autoOn ? "off" : "on"}.`),
    o: () => tipBox(`${ic("ci-open-chest")} Load`, "", [], "Load a saved life from its file. Key o."),
    n: () => tipBox(`${ic("new")} New life`, "", [], "Leave this life and choose a new start; you can save it first. Key n."),
    g: () => tipBox(`${ic("ci-globe")} The world`, L.world_era ? esc(cap(L.world_era.name)) : "", [], "What is publicly true now and what has happened, by age and era. Key g.") };
  tipsT.a = () => tipBox(`${ic("check")} Autosave ${autoOn ? "on" : "off"}`, "", [], "After every moment and every choice the life is kept in one slot in this browser, overwritten each time; Continue on the start screen opens it. Key a.");
  const inMenu = (b) => !!b.closest("#tPop");
  toolsEl.querySelectorAll("[data-key]").forEach((b) => { b.addEventListener("click", (e) => { e.stopPropagation(); send(b.dataset.key); }); if (!inMenu(b)) setTip(b, tipsT[b.dataset.key]); });
  toolsEl.querySelectorAll("[data-page]").forEach((b) => { b.addEventListener("click", (e) => { e.stopPropagation(); const k = b.dataset.page; if (!["i", "a"].includes(k)) setMenu(false); pageKey(k); }); if (!inMenu(b)) setTip(b, tipsT[b.dataset.page]); });
  $("tHelp").addEventListener("click", (e) => { e.stopPropagation(); setMenu(false); openHelp(); });
  $("tMenu").addEventListener("click", (e) => { e.stopPropagation(); hideTip(); setMenu(!menuOpen); });
  $("tPop").addEventListener("click", (e) => e.stopPropagation());
  setTip($("savedNote"), () => tipsT.s());
  setTip($("tHud"), () => tipBox(`${ic("wheel")} Status`, "", [], "Colors, mood, means, titles and people."));
  $("tHud").addEventListener("click", (e) => { e.stopPropagation(); hideTip(); hudEl.classList.toggle("open"); $("tHud").setAttribute("aria-pressed", hudEl.classList.contains("open")); });
}
function setMenu(on) {
  menuOpen = !!on; const p = $("tPop"), b = $("tMenu"); if (menuOpen) hideTip();
  if (p) p.hidden = !menuOpen; if (b) b.setAttribute("aria-expanded", menuOpen);
  if (menuOpen && p) { const f = p.querySelector("button:not([disabled])"); if (f && !touchUI) f.focus({ preventScroll: true }); }
}
function closeHud() { hudEl.classList.remove("open"); hideTip(); const t = $("tHud"); if (t) t.setAttribute("aria-pressed", "false"); }
document.addEventListener("click", (e) => {
  if (hudEl.classList.contains("open") && !e.target.closest("#hud, #tHud")) closeHud();
  if (menuOpen && !e.target.closest("#tPop, #tMenu")) setMenu(false);
});

/* ---------------- part 3: the character HUD ---------------- */
/* ---------------- point 7 (Emren 20:39): the spider graph. Where they are, where they want to be, what holds them, how fast
   they could move, and the edge of who they are (a color joins above 22%, leaves below 18%) ---------------- */
const SPA = [-90, -18, 54, 126, 198].map((a) => a * Math.PI / 180);
const SPR = 64, SPX = 100, SPY = 100;
const spRad = (v) => SPR * Math.sqrt(clamp(v, 0, 0.8) / 0.8);
const spAt = (i, r) => [SPX + r * Math.cos(SPA[i]), SPY + r * Math.sin(SPA[i])];
const spPts = (vs) => vs.map((v, i) => spAt(i, spRad(v)).map((x) => x.toFixed(1)).join(",")).join(" ");
const f1 = (p) => p.map((x) => x.toFixed(1)).join(",");
const circ = (r) => `M${(SPX - r).toFixed(1)} ${SPY}a${r.toFixed(1)} ${r.toFixed(1)} 0 1 0 ${(2 * r).toFixed(1)} 0a${r.toFixed(1)} ${r.toFixed(1)} 0 1 0 ${(-2 * r).toFixed(1)} 0`;
// o: {w, want, hold, acc, rule, id, hits, labels}; every array is the five colors W U B R G
function spiderSVG(o) {
  const id = o.id || "sp", w = o.w, P = w.map((v, i) => spAt(i, spRad(v)));
  let s = `<defs>${COLORS.map((c, i) => { const a = P[i], b = P[(i + 1) % 5]; return `<linearGradient id="${id}g${i}" gradientUnits="userSpaceOnUse" x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}"><stop offset="0" stop-color="var(--c${c})"/><stop offset="1" stop-color="var(--c${COLORS[(i + 1) % 5]})"/></linearGradient>`; }).join("")}</defs>`;
  for (const v of [0.4, 0.8]) s += `<polygon class="ring" points="${spPts([v, v, v, v, v])}"/>`;
  COLORS.forEach((_, i) => { const e = spAt(i, SPR); s += `<line class="ax" x1="${SPX}" y1="${SPY}" x2="${e[0].toFixed(1)}" y2="${e[1].toFixed(1)}"/>`; });
  const [enter, leave] = o.rule || [0.22, 0.18];
  s += `<path class="band" fill-rule="evenodd" d="${circ(spRad(enter))}${circ(spRad(leave))}"/>`;
  let fan = "";
  COLORS.forEach((_, i) => { const a = P[i], b = P[(i + 1) % 5]; fan += `<path d="M${SPX} ${SPY}L${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}Z" fill="url(#${id}g${i})"/>`; });
  s += `<g class="fan">${fan}</g>`;
  if (o.window) s += `<circle class="win" cx="${SPX}" cy="${SPY}" r="${(SPR + 2).toFixed(1)}"/>`;
  if (o.hold) s += `<polygon class="hold" points="${spPts(o.hold)}"/>`;
  if (o.want) s += `<polygon class="want" points="${spPts(o.want)}"/>`;
  s += `<polygon class="pos" points="${spPts(w)}"/>`;
  if (o.want) COLORS.forEach((c, i) => {            // the pull: from where they are to where they want to be, thicker the faster they could move
    const a = spRad(w[i]), b = spRad(o.want[i]), d = b - a;
    if (Math.abs(d) < 2.2) return;
    const sw = 1.2 + 3 * clamp((o.acc ? o.acc[i] : 0.15) / 0.4), dir = Math.sign(d), head = Math.min(Math.abs(d) * 0.6, 3.5 + sw);
    const ux = Math.cos(SPA[i]), uy = Math.sin(SPA[i]), hw = sw / 2 + 2.6;
    const p0 = spAt(i, a), p1 = spAt(i, b - dir * head), tip = spAt(i, b);
    s += `<g class="pull" style="color:var(--c${c})"><line x1="${p0[0].toFixed(1)}" y1="${p0[1].toFixed(1)}" x2="${p1[0].toFixed(1)}" y2="${p1[1].toFixed(1)}" stroke-width="${sw.toFixed(1)}"/>` +
      `<polygon points="${f1(tip)} ${f1([p1[0] - uy * hw, p1[1] + ux * hw])} ${f1([p1[0] + uy * hw, p1[1] - ux * hw])}"/></g>`;
  });
  if (o.labels !== false) COLORS.forEach((c, i) => {
    const e = spAt(i, SPR + 15), on = o.label ? lettersOf(o.label).includes(c) : w[i] > enter;
    const bd = o.bands ? o.bands[i] : "";
    if (bd === "fading" || bd === "rising") s += `<circle class="bd ${bd}" cx="${e[0].toFixed(1)}" cy="${e[1].toFixed(1)}" r="14.5"/>`;
    s += `<g class="orb" data-c="${c}"><circle cx="${e[0].toFixed(1)}" cy="${e[1].toFixed(1)}" r="11.5" fill="var(--p${c})" stroke="rgb(0 0 0 / .5)" opacity="${on ? 1 : 0.5}"/><use class="gx" href="#${MANA(c)}" x="${(e[0] - 8).toFixed(1)}" y="${(e[1] - 8).toFixed(1)}" width="16" height="16" style="color:var(--pInk)" opacity="${on ? 1 : 0.55}"/></g>`;
    const ly = i === 0 ? e[1] + 4 : e[1] + 25, lx = i === 0 ? e[0] + 16 : e[0];
    s += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="${i === 0 ? "start" : "middle"}" class="${on ? "on" : ""}">${pct(w[i])}</text>`;
    if (o.hits) { const hx = SPX + SPR * 0.62 * Math.cos(SPA[i]), hy = SPY + SPR * 0.62 * Math.sin(SPA[i]); s += `<circle class="hit" data-c="${i}" cx="${((hx + e[0]) / 2).toFixed(1)}" cy="${((hy + e[1]) / 2).toFixed(1)}" r="27"/>`; }
  });
  return s;
}
const spOf = (L, extra) => ({ w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])), hold: L.inertia.map((v) => v + 0.2), acc: L.acc,
  rule: (hud && hud.life && hud.life.ident_rule) || [0.22, 0.18], label: L.label, bands: L.dyn ? L.dyn.bands : null, window: !!(L.dyn && L.dyn.window), ...(extra || {}) });
// the key under the graph; each word's hover is its exact definition
const SP_KEY = [["pos", "Now", "Their five colors now, as shares of 100."],
  ["want", "Wants", "Where their wanting points: the colors they would move to if nothing held them back."],
  ["hold", "Holds", "What holds them where they are: 40% what they notice first, 30% their habits, 30% the titles they have put themselves into."],
  ["pull", "Pull", "The arrow runs from where they are to where they want to be. It is thicker the faster they could change now: how open their age is, times self-control, times their belief they can act that way, times the doors open to them."],
  ["band", "Edge", "The band from 18% to 22%: a color joins who they are above 22% and leaves below 18%. A dashed ring on a color: it is fading, held only by that edge. A bright ring: it is rising toward it."]];
function spKeyHTML() { return `<div class="spkey">${SP_KEY.map(([k, w]) => `<span data-spk="${k}"><i class="k-${k}"></i>${w}</span>`).join("")}</div>`; }
function bindSpKey(root) { root.querySelectorAll("[data-spk]").forEach((el) => { const k = SP_KEY.find((x) => x[0] === el.dataset.spk); setTip(el, () => tipBox(`<i class="spk k-${k[0]}"></i> ${k[1]}`, "", [], k[2])); }); }
// a slow week-by-week animation of the graph (point 2): frames [{w, want}], played over ms; the last frame is drawn with base's hits
const anims = new WeakMap();
// E9: a weekly trace row is [t, five colors, five wants, bands as letters (i, f, r, o), the identity label]
const BAND_CODE = { i: "in", f: "fading", r: "rising", o: "out" };
const frameOf = (f) => ({ t: f[0], w: f.slice(1, 6), want: f.slice(6, 11), ...(typeof f[11] === "string" && f[11].length === 5 ? { bands: [...f[11]].map((c) => BAND_CODE[c] || ""), label: f[12] || "" } : {}) });
const bandsOf = (A) => (A && A.bands ? { bands: A.bands, label: A.label } : {});
function animSpider(svg, frames, ms, base, done) {
  const prev = anims.get(svg); if (prev) cancelAnimationFrame(prev.raf);
  if (!frames.length) { if (done) done(); return; }
  const t0 = performance.now(), n = frames.length, st = { raf: 0 };
  anims.set(svg, st);
  const lerp = (a, b, f) => a.map((v, i) => v + (b[i] - v) * f);
  const draw = (now) => {
    const x = n === 1 ? 1 : clamp((now - t0) / Math.max(1, ms)) * (n - 1), k = Math.min(n - 2, Math.floor(x)), f = n === 1 ? 0 : x - k;
    const A = frames[Math.max(0, k)], B = frames[Math.min(n - 1, k + 1)];
    const end = now - t0 >= ms;
    svg.innerHTML = spiderSVG({ ...base, ...(end ? {} : bandsOf(f < 0.5 ? A : B)), w: end ? frames[n - 1].w : lerp(A.w, B.w, f), want: end ? frames[n - 1].want : lerp(A.want, B.want, f), hits: end && base.hits });
    if (end) { anims.delete(svg); if (done) done(); } else st.raf = requestAnimationFrame(draw);
  };
  st.raf = requestAnimationFrame(draw);
}

/* ---------------- point 4: exact definitions ---------------- */
// each "around them" driver, exactly as the engine reads it to time life events (engine.py, the event context X)
const AROUND_DEF = {
  "own household": "A partner counts 1, children 1, a community ½; the sum, minus 1.",
  ties: "People they can lean on, 0 to 100, minus 50.",
  money: "Their money, 0 to 100, minus 50.",
  health: "Their health, 0 to 100, minus 50.",
  era: "How hard the era of these years is pushing; 0 in quiet times.",
  "harsh world": "How hard life is in this world; set by the world.",
  unrest: "How unsettled this society is; set by the world.",
  prosperity: "How well off this society is; set by the world.",
  community: "A community they belong to, times what they have put into it.",
  stress: "Strain minus 50, kept between −50% and +100%.",
  "recent trouble": "Blows of recent years, fading with time; up to 200%.",
  "recent fortune": "Lucky turns of recent years, fading with time; up to 200%." };
const aroundPct = (v) => `${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.round(Math.abs(v) * 100)}%`;
function aroundBands(k) {
  const B = (hud && hud.around_bands) || {}, bs = B[k] || B["*"] || [], fl = ((hud && hud.around_floor) || {})[k] || ((hud && hud.around_floor) || {})["*"];
  return bs.map(([t, w]) => `${esc(w)} from ${aroundPct(t)}`).concat(fl ? [`${esc(fl)} below`] : []).join(", ");
}
function aroundTip(k, v) {
  const L = hud && hud.life, g = good(k, v), w = (L && L.around_words || {})[k] || "";
  return tipBox(`${ic("compass")} ${esc(cap(k))}: ${esc(w)} (${aroundPct(v)})`, esc(AROUND_DEF[k] || ""), [["Words", aroundBands(k)]],
    g > 0 ? "Now it makes good events likelier and hard ones rarer." : g < 0 ? "Now it makes hard events likelier." : "");
}
// a state's exact definition (engine.ADJECTIVES): the variable it reads over the last three months, where it begins and ends
function stateScale(var_, scale, v) {
  if (var_ === "stress") return `${Math.round(v / 1.5 * 100)}% of the most they can bear`;
  return scale === "of100" ? `${Math.round(v * 100)} of 100` : `${v < 0 ? "−" : ""}${Math.abs(Math.round(v * 100))} points`;
}
const oneIn = (s) => s >= 0.45 ? "about half" : `about 1 in ${Math.max(2, Math.round(1 / Math.max(s, 0.01)))}`;
function stateDef(x) {
  const D = (hud && hud.adj_defs && hud.adj_defs[x.name]) || x;
  const sc = (v) => stateScale(D.var, D.scale, v);
  return `${cap(D.reads)} ${D.side > 0 ? "above" : "below"} ${sc(D.on)} over the last three months; it ends ${D.side > 0 ? "below" : "above"} ${sc(D.off)}.`;
}
function stateTip(x) {
  const D = (hud && hud.adj_defs && hud.adj_defs[x.name]) || x;
  const rows = [];
  if (x.value != null) rows.push(["Now", stateScale(D.var, D.scale, x.value)]);
  if (x.years != null) rows.push(["For", yrsWord(x.years)]);
  if (D.share) rows.push(["Adults like this", oneIn(D.share)]);
  if (D.from_age) rows.push(["From age", String(Math.round(D.from_age))]);
  return tipBox(`${ic(x.icon)} ${esc(cap(x.word || D.say))}`, esc(stateDef(x)), rows, "");
}
const BAND_WORD = { in: "part of who they are", fading: "fading: at or under 22%, held by the edge", rising: "rising: above 18%, not yet part of them", out: "not part of who they are" };
function tipColor(L, i) {
  const c = COLORS[i], w = L.w[i], inId = lettersOf(L.label).includes(c), [enter, leave] = L.ident_rule || [0.22, 0.18];
  return tipBox(`${pip(c)} ${CNAME[c]}`, CIDEA[c], [
    ["Now", `<b>${pct(w)}</b>`],
    ["Wants", `${pct(Math.max(0, w + L.demand[i]))} (${updown(L.demand[i], 0, 100)} pts)`],
    ["Holds", pct(L.inertia[i] + 0.2)],
    ["Speed of change", pct(L.acc[i])],
    ["Skill in its ways", pct(L.skill[i])],
    ["Belief they can act so", pct(L.belief[i])],
    ["Notices first", pct(L.lens[i])],
    ["The story's voice", pct(L.voice[i])]].concat(L.dyn ? [["Place", BAND_WORD[L.dyn.bands[i]] || ""]] : []),
    L.label ? (inId ? `${CNAME[c]} is part of who they are; it leaves below ${Math.round(leave * 100)}%.` : `${CNAME[c]} is not part of who they are; it joins above ${Math.round(enter * 100)}%.`) : "");
}
const RINGS = [
  ["content", "Content", GI.meter.content || "mood", "var(--sat)", "Satisfaction: how content they are with life right now. Happy is not the same as peaceful."],
  ["peace", "Peace", GI.meter.peace || "leaf", "var(--peace)", "How settled they are with who they are and how they live."],
  ["stress", "Strain", GI.meter.strain || "bolt", "var(--stress)", "The strain of the year. Pushing them against their will adds to it."],
  ["want", "Wanting", GI.meter.wanting || "flame", "var(--want)", "Pent-up wanting: what they were denied builds up. At the mark it breaks through and moves them on its own."]];
// every 0..1 quantity reaches the player as a percent (Emren 09:25: "0.58 is for me and you, 58% is for the player")
function ringPct(k, L) { return k === "want" ? pct(Math.min(1, L.want / Math.max(L.want_thr, 1e-9))) : k === "stress" ? pct(L.stress / 1.5) : pct(L[k]); }
// v22 next look: the four meters as slim bars, each with a tick at its usual level (satisfaction and peace: their average
// over the last ten years of the river; wanting: the mark where it breaks through)
function usualOf(k, L) {
  const R = (L.river || []).filter((r) => r[0] >= L.age - 10), col = k === "content" ? 6 : k === "peace" ? 7 : -1;
  if (col > 0 && R.length >= 2) return R.reduce((t, r) => t + r[col], 0) / R.length;
  return null;
}
function meterHTML(r, L) {
  const [k, label, icon, color] = r;
  let frac = clamp(L[k]), tick = usualOf(k, L);
  if (k === "stress") frac = clamp(L.stress / 1.5);
  if (k === "want") { const topv = Math.max(L.want_thr * 1.25, 1e-9); frac = clamp(L.want / topv); tick = L.want_thr / topv; }
  return `<div class="mtr" data-ring="${k}" style="--mc:${color}">${useIc(icon, "").replace("<use", '<svg class="i' + (isGi(icon) ? " gx" : "") + '" aria-hidden="true"><use') + "</svg>"}<span class="ml">${label}</span><span class="mbar"><i style="width:${(frac * 100).toFixed(1)}%"></i>${tick != null ? `<b style="left:${(clamp(tick) * 100).toFixed(1)}%"></b>` : ""}</span><span class="pv">${ringPct(k, L)}</span></div>`;
}
function ringHTML(r, L) {
  const [k, label, icon, color] = r, R0 = 22, C = 2 * Math.PI * R0;
  let v = L[k], frac = clamp(v), mark = "";
  if (k === "stress") frac = clamp(v / 1.5);
  if (k === "want") {
    const topv = Math.max(L.want_thr * 1.25, 1); frac = clamp(v / topv);
    const a = (L.want_thr / topv) * 2 * Math.PI - Math.PI / 2;
    mark = `<line class="mark" x1="${(28 + 18 * Math.cos(a)).toFixed(1)}" y1="${(28 + 18 * Math.sin(a)).toFixed(1)}" x2="${(28 + 26 * Math.cos(a)).toFixed(1)}" y2="${(28 + 26 * Math.sin(a)).toFixed(1)}"/>`;
  }
  return `<div class="rg" data-ring="${k}" style="color:${color}"><svg viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="${R0}"/><circle class="fg" cx="28" cy="28" r="${R0}" stroke="${color}" stroke-dasharray="${(frac * C).toFixed(1)} ${C.toFixed(1)}"/>${mark}${useIc(icon, 'x="19" y="19" width="18" height="18"')}</svg><b class="pv">${ringPct(k, L)}</b><span>${label}</span></div>`;
}
const MEANS = [["money", GI.res.money || "coin", "Savings and income.", "var(--sat)"], ["time", GI.res.time || "clock", "Hours left over after duties.", "var(--cU)"], ["health", GI.res.health || "pulse", "Body and energy.", "var(--cG)"],
  ["ties", GI.res.ties || "link", "People they can lean on.", "var(--cR)"], ["freedom", GI.res.freedom || "feather", "Room to choose for themselves.", "var(--arcane)"]];
const KINDS = [["career", "Work"], ["partner", "Love"], ["children", "Family"], ["community", "Circle"], ["faith", "Faith"]];
const ROLE_GROUP = { mother: "kin", father: "kin", sibling: "kin", grandparent: "kin", cousin: "kin", aunt: "kin", "late relative": "kin", child: "kin",
  partner: "love", companion: "love", prospect: "love", ex: "love", friend: "friend", neighbour: "friend",
  teacher: "work", mentor: "work", boss: "work", colleague: "work", "former boss": "work", rival: "rival" };
const GROUP_COL = { kin: "#d8b469", love: "#f08aa4", friend: "#5fcac3", work: "#8fa6d8", rival: "#f2856d", other: "#9a90b8" };
const ROLE_ICON = { kin: "home", love: "heart", friend: "people", work: "case", rival: "bolt", other: "dot", ...GI.role };
const baseRole = (r) => String(r || "").replace(/^old /, "");
const roleIcon = (r) => baseRole(r) === "child" ? (GI.role.child || "child") : ROLE_ICON[ROLE_GROUP[baseRole(r)] || "other"];
const BAD_UP = new Set(["harsh world", "unrest", "stress", "recent trouble"]), NEUTRAL = new Set(["own household", "era"]);
const good = (k, v) => NEUTRAL.has(k) ? 0 : (BAD_UP.has(k) ? -1 : 1) * Math.sign(v);
function stateValue(x) { return x.var === "want" ? pct(x.value) + " of the way to breaking through" : x.var === "stress" ? pct(x.value / 1.5) + " of the most they can bear" : x.var === "mood" ? (x.value > 0 ? "lifted" : "lowered") + ` by recent weeks (${x.value > 0 ? "+" : "−"}${Math.round(Math.abs(x.value) * 100)}%)` : ["fortune", "trouble"].includes(x.var) ? (x.value >= 1.8 ? "one thing after another" : "some") : pct(x.value); }
function investWord(v) { return v >= 2 ? "a great deal" : v >= 1 ? "a lot" : v >= 0.35 ? "some" : "a little"; }
function temperWord(k, v) {
  const r = k === "react" ? v / 2 : v;
  return k === "react" ? (r >= 0.65 ? "hit hard by events" : r >= 0.4 ? "about average" : "hard to shake") :
    k === "steady" ? (v >= 0.6 ? "very sure of themselves" : v >= 0.3 ? "fairly sure" : "still searching") :
    k === "base_mood" ? (v >= 0.62 ? "sunny" : v >= 0.48 ? "even" : "low") : (v >= 0.55 ? "hopeful" : v >= 0.38 ? "middling" : "doubtful");
}
const TEMPER = [["react", "Reactive", "bolt", 2, "How hard events hit them."], ["steady", "Steady", "anchor", 1, "How sure they are of who they are."],
  ["base_mood", "Mood", "mood", 1, "Where their mood settles between events."], ["outlook", "Outlook", "sun", 1, "How sure they are that effort pays off."]];
// a title or perk's tooltip: its kind, the ways it asks for or helps, what it brings, and how it stands now
const shortSay = (x) => String(x || "").replace(/^(a|an|the) /, "");
// a title's name under its socket: the catalogue's say without its article, or a shorter word where the say runs long
const SOCK_WORD = { "girlfriend or boyfriend": "Sweetheart", "living together": "Living together", "partner of many years": "Years together",
  "regular worshipper": "Regular worshipper", "believer on the big days": "Big-days believer", "deacon or elder": "Elder",
  "residents' committee member": "Residents' committee", "neighbourhood volunteer": "Volunteer", "parent of three or more": "Parent of three+",
  psychotherapist: "Therapist", "cybersecurity analyst": "Security analyst", "neighbourhood-watch coordinator": "Street watch",
  "congregation musician": "Worship musician", "board-game club organiser": "Board-game club", "nonromantic life partner": "Life partner",
  "community-garden coordinator": "Garden coordinator", "search-and-rescue volunteer": "Rescue team", "parent-association organiser": "Parents' association",
  "housing-cooperative member": "Housing co-op", "community-kitchen volunteer": "Soup kitchen", "member of a monastic community": "Monastic life",
  "interfaith-dialogue participant": "Interfaith circle", "disability-rights organiser": "Disability rights", "restorative-justice advocate": "Restorative justice",
  "civil-liberties campaigner": "Civil liberties", "animal-shelter campaigner": "Animal shelter", "digital-rights advocate": "Digital rights",
  engaged: "Engaged", "community-radio presenter": "Radio presenter", "book-club organiser": "Book club", "lay religious teacher": "Lay teacher" };
const sockWord = (d) => SOCK_WORD[d.name] || cap(shortSay(d.say));
// a facet (a title held on top of another: newlywed on wife or husband), in a word or two under the socket
const FACET_WORD = { newlywed: "newlywed", "parent of three or more": "three or more", "parent of an only child": "an only child",
  "parent of independent adult children": "grown-up children", "parent with a child living abroad": "a child abroad", "home-educating parent": "home-educating",
  "parent coordinating complex support needs": "support needs", "parent raising a child across languages": "two languages", "caregiving partner": "caring for them",
  "spouse in a family-arranged marriage": "arranged", "partner in a multigenerational household": "with family", "grandparent raising a grandchild": "raising a grandchild" };
const facetWord = (f) => FACET_WORD[f.name] || shortSay(f.say);
// the Library's chance for an act: how often it works for an ordinary person of these ages
const baseWord = (b) => b >= 0.95 ? "it almost always works" : b < 0.05 ? "it almost never works" : `it works about ${Math.max(1, Math.min(9, Math.floor(b * 10 + 0.5)))} times in 10`;
const yrsWord = (y) => y < 1 ? "a few months" : y < 2 ? "about a year" : `${Math.round(y)} years`;
const waysHTML = (w) => { const cs = lettersOf(w || ""); return cs.length ? pips(cs) + " " + cs.map((c) => CNAME[c]).join(" and ") : "any"; };
const CLOSED_WORD = { law: "the law", approval: "the approval of others", means: "lack of means" };
function findRole(name) {
  const L = hud && hud.life; if (!L) return null;
  return (L.perks || []).find((x) => x.name === name) || (L.statuses || []).find((x) => x.name === name) ||
    [].concat(...(L.titles || []).map((t) => t.named || [])).find((x) => x.name === name) || null;
}
function roleTip(d, now) {
  const rows = [];
  if (d.title) {
    if (d.on) rows.push(["Held on", esc(cap(String(d.on)))]);
    if (d.profile) rows.push(["Their way", esc(d.profile)]);
    if (d.ways) rows.push(["Its ways", waysHTML(d.ways)]);
    if (d.meets && d.meets.length) rows.push(["Brings", d.meets.map(([w, g]) => `<span class="${g > 0 ? "up" : "down"}">${g > 0 ? "+" : "−"}${esc(w)}</span>`).join(", ")]);
  } else {
    rows.push(["Helps", d.plus > 0 ? `+${d.plus}% on acts in ${waysHTML(d.ways)} ways` : "opens doors that some acts need"]);
    if (d.half && d.kind === "skill") rows.push(["Unused", `half of it is gone in about ${d.half} years`]);
  }
  const st = now === undefined ? d : now;
  if (!st) rows.push(["Now", "not held"]);
  else if (st.state === "suspended") rows.push(["Now", `on hold${st.back_in > 0 ? ", back in " + yrsWord(st.back_in) : ""}`]);
  else if (st.state === "rusty") rows.push(["Now", "no longer held; it still helps a little while it fades"]);
  else if (st.years != null) rows.push(["Held", yrsWord(st.years)]);
  const head = d.title ? cap(shortSay(d.say || d.name)) : cap(d.name);
  const sub = d.title ? (d.kind === "status" ? "A status" : `A title in ${esc((KINDS.find((k) => k[0] === d.kind) || [0, cap(d.kind)])[1])}`) : PERK_KIND_WORD[d.kind] || "A perk";
  return tipBox(`${ic(roleIconOf(d))} ${esc(head)}`, sub, rows, "");
}
// a life holds about 25 perks: the HUD shows the first dozen (credentials, skills, assets, standing, bonds, then those on hold
// or fading) and a chip for the rest; the choice is remembered in this browser
const PERK_SHOW = 12;
let perksOpen = false; try { perksOpen = localStorage.getItem("chroma.perksOpen") === "1"; } catch (_) {}
let hudFrames = [], hudLast = null;
// Emren's point 6: a season of change between two stages of life, or into a new title (engine explain.season)
const seasonWords = (x) => `${x.kind === "stage" ? "Crossing into " + x.into : "Becoming " + x.into} · ${x.step_word}`;
const SEASON_DEF = "A season of change: the crossing, the in-between, then settling in. One moment in it can transform who they become.";
function seasonTip(x) { return tipBox(`${ic("gate")} ${esc(seasonWords(x))}`, SEASON_DEF, [["Step", `${x.step} of 3`], ["Weeks in", String(x.weeks_in)], ["Weeks left", String(x.weeks_left)]], ""); }
function renderHud(L) {
  if (!L || !L.w) { hudEl.innerHTML = ""; return; }
  const lc = labelColors(L.label);
  // point 5: each title held is a row (its life domain, its name, a facet, how long), the empty domains a row of faint signs
  const titles = KINDS.filter(([k]) => (L.titles || []).some((x) => x.kind === k)).map(([k, word]) => {
    const t = L.titles.find((x) => x.kind === k), ex = lettersOf(t.expects), nm = t.named || [];
    const label = nm.length ? sockWord(nm[0]) + (nm.length > 1 ? ` +${nm.length - 1}` : "") : word;
    const fc = nm.length && (nm[0].facets || []).length ? `<span class="fc">${esc(facetWord(nm[0].facets[nm[0].facets.length - 1]))}</span>` : "";
    return `<div class="trow${t.clash ? " clash" : ""}" data-sock="${k}" style="--sc:${ex.length ? `var(--c${ex[0]})` : "var(--gold)"};--yrs:${clamp(t.years / 30) * 100}%"><span class="o">${ic(KIND_ICON[k])}</span><span class="tx"><span class="tn">${esc(label)}</span>${fc}</span><span class="ty">${t.clash ? ic("bolt") : ""}${Math.floor(t.years)}y</span></div>`;
  }).join("") + ((empty) => empty.length ? `<div class="tempty">${empty.map(([k, word]) => `<span data-sock="${k}">${ic(KIND_ICON[k])}</span>`).join("")}<span class="muted">not yet: ${empty.map(([, w]) => w.toLowerCase()).join(", ")}</span></div>` : "")(KINDS.filter(([k]) => !(L.titles || []).some((x) => x.kind === k)));
  const cast = L.cast || [];
  const near = cast.filter((p) => p.alive && !/^(old |former )|^ex$/.test(p.role)).sort((a, b) => b.seen - a.seen);
  const far = cast.filter((p) => p.alive && /^(old |former )|^ex$/.test(p.role)).sort((a, b) => b.seen - a.seen);
  const gone = cast.filter((p) => !p.alive);
  const shown = near.slice(0, 12).concat(far.slice(0, 3), gone.slice(-3));
  const extra = cast.length - shown.length;
  const people = shown.map((p) => { const g = ROLE_GROUP[baseRole(p.role)] || "other"; return `<span class="av${p.alive ? "" : " gone"}${p.alive && far.includes(p) ? " far" : ""}" data-pid="${p.id}" style="--ac:${GROUP_COL[g]}">${esc(p.name[0])}</span>`; }).join("") + (extra > 0 ? `<span class="av more">+${extra}</span>` : "");
  const circle = L.circle ? CIRCLE_LAYERS.map(([k, word]) => { const xs = L.circle.filter((p) => p.layer === k && p.alive); return xs.length ? `<div class="crow"><span class="cl">${word}</span><span class="people">${xs.slice(0, k === 4 ? 14 : 10).map((p) => `<span class="av" data-cid="${p.id}" style="--ac:${p.read ? `var(--c${p.read[0]})` : "var(--muted)"}">${esc(p.name[0])}</span>`).join("")}${xs.length > (k === 4 ? 14 : 10) ? `<span class="muted">+${xs.length - (k === 4 ? 14 : 10)}</span>` : ""}</span></div>` : ""; }).join("") : "";
  const reach = L.reach ? L.reach.map((r) => `<div class="mt" data-reach="${r.ring}"><span class="ml">${ic(r.icon)} ${esc(r.word)}</span><i><b style="width:${(clamp(r.felt) * 100).toFixed(0)}%;background:var(--arcane)"></b></i><span class="mv">${esc(r.level_word)}</span></div>`).join("") : "";
  const AW = L.around_words || {};
  const around = Object.entries(L.around || {}).map(([k, v]) => { const g = good(k, v); return `<span class="chip ${g > 0 ? "up" : g < 0 ? "down" : ""}" data-a="${esc(k)}">${ic(g > 0 ? "sun" : g < 0 ? "rain" : "compass")}${esc(cap(k))}: <span class="w">${esc(AW[k] || (v > 0 ? "up" : "down"))}</span> <span class="pc">(${aroundPct(v)})</span></span>`; }).join("");
  const states = (L.states || []).map((x, i) => `<span class="st g${x.good}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span>`).join("");
  const statuses = (L.statuses || []).map((d, i) => `<span class="perk stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`).join("");
  const pk = L.perks || [], cut = !perksOpen && pk.length > PERK_SHOW + 2 ? PERK_SHOW : pk.length;
  const perks = pk.slice(0, cut).map((d, i) => `<span class="perk${d.state && d.state !== "held" ? " " + d.state : ""}" data-perk="${i}" style="--pc:${d.ways ? `var(--c${d.ways[0]})` : "var(--gold)"}">${ic(roleIconOf(d))}${esc(cap(d.name))}</span>`).join("")
    + (pk.length > PERK_SHOW + 2 ? `<button class="perk more" id="perkMore">${perksOpen ? "Fewer" : `+${pk.length - cut} more`}</button>` : "");
  // v22 next look: a compact crest on top that fits 800 px (identity, states, wheel, four meters, means, the goal they live
  // for now), the fuller record below it in the same panel (dreams and plans, titles, perks, people, around them)
  const g0 = (L.goals || []).slice().sort((a, b) => ({ passion: 0, plan: 1, dream: 2 }[a.kind] ?? 3) - ({ passion: 0, plan: 1, dream: 2 }[b.kind] ?? 3) || b.strength - a.strength)[0];
  hudEl.innerHTML = `<button class="ghost hud-close" id="hudClose" aria-label="Close status">${ic("x")}</button>
    <div class="crestbox"><div class="cpips">${lc.length ? pips(lc) : pip("W", "dim")}</div><div class="gn">${esc(L.guild || "Still forming")}</div>
      <div class="ep" id="crestMotto">${!L.label ? "colors still forming" : esc(L.meaning || "")}</div>
      ${L.label && L.label !== L.voice_label && L.voice_guild ? `<div class="vo">still told as ${esc(L.voice_guild)}</div>` : ""}${L.season_x ? `<div class="season" id="seasonChip">${ic("gate")} ${esc(seasonWords(L.season_x))}</div>` : ""}</div>
    ${states ? `<div class="states">${states}</div>` : ""}
    <div class="wheelw"><svg class="wheel" id="hudWheel" viewBox="-6 -2 212 206" role="img" aria-label="Spider graph of the five colors: where they are, where they want to be, what holds them">${spiderSVG(spOf(L, { id: "hw", hits: true }))}</svg><span class="wkey" id="wKey" tabindex="0" aria-label="How to read the wheel">?</span></div>
    <div class="meters">${RINGS.filter((r) => r[0] !== "want" || !L.young).map((r) => meterHTML(r, L)).join("")}</div>
    <div class="means5">${MEANS.map(([k, icn, , col]) => { const v = clamp(L.res[k]); return `<div class="mean" data-r="${k}" style="--mc:${col}"><span class="col"><i style="height:${(v * 100).toFixed(0)}%"></i></span>${ic(icn)}<small>${esc(cap(k))}</small></div>`; }).join("")}</div>
    ${needsRowHTML(L)}
    ${g0 ? `<div class="nowgoal" data-gj="${g0.j}">${ic(GOAL_ICON[g0.kind] || "moon")}<span class="k">${esc(cap(g0.kind))}</span><span class="nm">${esc(g0.name)}</span></div>` : ""}
    <button class="ghost sheetbtn" id="openSheet">${ic("ci-diary")} The whole character</button>
    <div class="hmore">
    ${goalsHTML(L)}
    <div class="hsec"><h4>Titles</h4><div class="trows">${titles}</div>${statuses ? `<div class="perks stats">${statuses}</div>` : ""}</div>
    ${perks ? `<div class="hsec"><h4>Perks${pk.length > PERK_SHOW + 2 ? ` <span class="cnt">${pk.length}</span>` : ""}</h4><div class="perks">${perks}</div></div>` : ""}
    ${circle ? `<div class="hsec"><h4>People</h4><div class="circle">${circle}</div></div>` : `<div class="hsec"><h4>People</h4><div class="people">${people || `<span class="empty">Nobody met yet</span>`}</div></div>`}
    ${reach ? `<div class="hsec"><h4>Reach</h4><div class="mts">${reach}</div></div>` : ""}
    ${around ? `<div class="hsec"><h4>Around them</h4><div class="chips">${around}</div></div>` : ""}
    ${L.temper ? `<div class="hsec"><h4>Temperament</h4><div class="tmpr">${TEMPER.map(([k, lb, icn, top]) => `<div class="tm" data-tm="${k}">${ic(icn)}<div><div class="bar"><b style="width:${(clamp(L.temper[k] / top) * 100).toFixed(1)}%"></b></div>${lb}</div></div>`).join("")}</div></div>` : ""}
    </div>`;
  setTip($("wKey"), () => tipBox(`${ic("wheel")} How to read the wheel`, "", SP_KEY.map(([k, w, d]) => [`<i class="spk k-${k}"></i> ${w}`, esc(d)]), "Hover a color for its numbers."));
  if (L.label && L.meaning) setTip($("crestMotto"), () => tipBox(`${pips(lc)} ${esc(L.guild)}`, esc(L.meaning), L.magic ? [["In Magic: The Gathering", esc(L.magic)]] : [], "A color joins who they are above 22% and leaves below 18%."));
  $("hudClose").addEventListener("click", () => closeHud());
  if ($("seasonChip")) setTip($("seasonChip"), () => seasonTip(L.season_x));
  const bindHits = () => hudEl.querySelectorAll("#hudWheel .hit").forEach((h) => setTip(h, () => tipColor(L, +h.dataset.c)));
  bindHits(); bindSpKey(hudEl);
  $("openSheet").addEventListener("click", (e) => { e.stopPropagation(); openSheet(); });
  hudEl.querySelectorAll("[data-nd]").forEach((el) => setTip(el, () => needTip(el.dataset.nd, L)));
  // point 2: the colors move to where they are now slowly, week by week when the weeks are known
  const fr = hudFrames.splice(0), last = hudLast; hudLast = { t: Math.round(L.age * 52), w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])) };
  if (last && !IL.on && (fr.length || last.w.some((v, i) => Math.abs(v - L.w[i]) > 0.002))) {
    const frames = [last].concat(fr.filter((_, i) => fr.length < 120 || i % Math.ceil(fr.length / 120) === 0), [hudLast]);
    animSpider($("hudWheel"), frames, clamp(frames.length * 45, 900, 2600), spOf(L, { id: "hw", hits: true }), bindHits);
  }
  hudEl.querySelectorAll("[data-ring]").forEach((el) => { const m = RINGS.find((x) => x[0] === el.dataset.ring); setTip(el, () => tipBox(`<span style="color:${m[3]}">${ic(m[2])}</span> ${m[1]}`, "", [["Now", m[0] === "want" ? `${ringPct("want", L)} of the way to breaking through` : m[0] === "stress" ? `${ringPct("stress", L)} of the most they can bear` : ringPct(m[0], L)]], m[4] + (m[0] === "want" && L.young ? " Only from young adulthood." : ""))); });
  hudEl.querySelectorAll("[data-r]").forEach((el) => { const r = MEANS.find((x) => x[0] === el.dataset.r); setTip(el, () => tipBox(`${ic(r[1])} ${cap(r[0])}`, "", [["Now", pct(L.res[r[0]])]], r[2])); });
  hudEl.querySelectorAll("[data-sock]").forEach((el) => {
    const k = el.dataset.sock, t = (L.titles || []).find((x) => x.kind === k);
    const nm = (t && t.named) || [];
    const as = nm.map((x) => `${esc(sockWord(x))}${(x.facets || []).map((f) => ", " + esc(shortSay(f.say))).join("")}${x.ways ? " " + pips(lettersOf(x.ways)) : ""} <span class="muted">${yrsWord(x.years)}</span>`).join("<br>");
    const way = nm.length && nm[0].profile ? [["Their way", esc(nm[0].profile)]] : [];
    const brings = nm.length && nm[0].meets && nm[0].meets.length ? [["It brings", nm[0].meets.map(([w, g]) => `<span class="${g > 0 ? "up" : "down"}">${g > 0 ? "+" : "−"}${esc(w)}</span>`).join(", ")]] : [];
    setTip(el, () => t ? tipBox(`${ic(KIND_ICON[k])} ${cap(k)}`, t.clash ? "In a clash: it asks for one thing, they want another." : "", (as ? [["As", as]] : []).concat(way, brings, [["Held", yrsWord(t.years)], ["Invested", investWord(t.invested)], ["It expects", pips(lettersOf(t.expects))]]), "")
      : tipBox(`${ic(KIND_ICON[k])} ${cap(k)}`, "Not held yet", [], ""));
  });
  hudEl.querySelectorAll("[data-pid]").forEach((el) => setTip(el, () => personTip(+el.dataset.pid)));
  hudEl.querySelectorAll("[data-cid]").forEach((el) => setTip(el, () => circleTip((L.circle || []).find((p) => p.id === +el.dataset.cid))));
  hudEl.querySelectorAll("[data-reach]").forEach((el) => { const r = (L.reach || []).find((x) => x.ring === el.dataset.reach); if (r) setTip(el, () => tipBox(`${ic(r.icon)} Reach: ${esc(r.word)}`, "",
    [["Standing", esc(r.level_word)], ["They feel", `${fpct(r.felt)} able to change it`], ["Reality, roughly", esc(r.hint || "unclear")]],
    "How far their acts can move it: the close circle always answers; the town a little; institutions and the state only through office, fame, wealth or invention.")); });
  hudEl.querySelectorAll("[data-a]").forEach((el) => { const k = el.dataset.a; setTip(el, () => aroundTip(k, L.around[k])); });
  hudEl.querySelectorAll("[data-tm]").forEach((el) => { const t = TEMPER.find((x) => x[0] === el.dataset.tm); setTip(el, () => tipBox(`${ic(t[2])} ${TEMPER_NAME[t[0]]}`, t[4], [["Now", temperWord(t[0], L.temper[t[0]])]], "")); });
  hudEl.querySelectorAll("[data-st]").forEach((el) => { const x = L.states[+el.dataset.st]; setTip(el, () => x.reads ? stateTip(x) : tipBox(`${ic(x.icon)} ${esc(cap(x.word))}`, "", [[esc(x.name), stateValue(x)]], "")); });
  hudEl.querySelectorAll("[data-gj]").forEach((el) => { const g = (L.goals || []).find((x) => x.j === +el.dataset.gj); if (g) setTip(el, () => goalTip({ kind: g.kind, colors: g.colors, domain: g.domain, source: g.source, horizon: g.horizon }, g)); });
  const ap = $("addPlan"); if (ap) { ap.addEventListener("click", (e) => { e.stopPropagation(); send("p"); }); setTip(ap, () => tipBox(`${ic("quill")} Make a plan`, "", [], "Set them a plan: a year, five years or a lifetime, in a life domain or in some colors. You see how sure they feel, and how plans like it usually go. Key p.")); }
  hudEl.querySelectorAll("[data-perk]").forEach((el) => { const d = L.perks[+el.dataset.perk]; setTip(el, () => roleTip(d)); });
  const pm = $("perkMore"); if (pm) pm.addEventListener("click", (e) => { e.stopPropagation(); perksOpen = !perksOpen; try { localStorage.setItem("chroma.perksOpen", perksOpen ? "1" : ""); } catch (_) {} renderHud(L); });
  hudEl.querySelectorAll("[data-rs]").forEach((el) => { const d = L.statuses[+el.dataset.rs]; setTip(el, () => roleTip(d)); });
}

function goalBG(cs) { return cs.length > 1 ? `linear-gradient(90deg, ${cs.map((c) => `var(--c${c})`).join(", ")})` : cs.length ? `var(--c${cs[0]})` : "var(--arcane)"; }
function goalRow(g, mine) {
  const cs = lettersOf(g.colors), col = cs.length ? `var(--c${cs[0]})` : "var(--arcane)";
  const fill = g.kind === "plan" ? Math.max(0.03, g.progress) : g.strength;
  const val = g.kind === "plan" ? `${g.by_player ? `<span class="mine">${ic("quill")}</span>` : ""}${fpct(g.felt)}` : pips(cs);
  return `<div class="drm ${g.kind}" data-gj="${g.j}" style="--gc:${col};--gbg:${g.kind === "plan" ? "linear-gradient(90deg, var(--gold3), var(--gold2))" : goalBG(cs)}">
    <span class="gi">${ic(GOAL_ICON[g.kind])}</span><div style="min-width:0"><div class="gn">${esc(cap(g.name))}</div><div class="gbar"><b style="width:${(clamp(fill) * 100).toFixed(0)}%"></b></div></div><span class="gv">${val}</span>${mine || ""}</div>`;
}
function goalsHTML(L) {
  const gs = L.goals;
  if (!gs) return "";
  const canPlan = hud && hud.mode === "play" && !L.young;
  return `<div class="hsec"><h4>Dreams and plans</h4><div class="drms">${gs.length ? gs.map((g) => goalRow(g)).join("") : `<span class="empty">No dreams yet</span>`}</div>${canPlan ? `<button class="ghost addplan" id="addPlan">${ic("quill")} Make a plan</button>` : ""}</div>`;
}

/* ---------------- making a plan (key p; engine v7 foresee.py) ---------------- */
const planEl = document.createElement("div"); planEl.className = "help plan"; planEl.hidden = true; document.body.appendChild(planEl);
planEl.addEventListener("click", (e) => { if (e.target === planEl) send("x"); });
function renderPlan(h) {
  const p = h && h.plan;
  if (!p || busy) { planEl.hidden = true; planEl.innerHTML = ""; return; }
  const L = h.life || {}, name = esc(L.name || "them");
  let body = "";
  if (p.step === "horizon") {
    const plans = (L.goals || []).filter((g) => g.kind === "plan");
    body = `<p class="muted" style="margin:0">A plan pulls on what ${name} does until it comes true, runs out of time, or is let go. Within…</p>
      <div class="opts">${p.horizons.map(([k, , t]) => `<button class="ch" data-v="${k}"><b>${esc(cap(t))}</b></button>`).join("")}</div>
      ${plans.length ? `<div class="muted" style="font-size:var(--fs-1)">Plans held now</div><div class="held">${plans.map((g, i) => goalRow(g, `<button class="ghost xbtn" data-v="d${i + 1}">${ic("x")} drop</button>`)).join("")}</div>` : ""}`;
  } else if (p.step === "what") {
    body = `<p class="muted" style="margin:0">${esc(cap(p.horizon === "life" ? "a lifetime" : "within " + (p.horizon === "year" ? "a year" : "five years")))}: a plan to…</p>
      <div class="opts">${p.domains.map(([k, d, t]) => `<button class="ch" data-v="${k}" ${(p.held || []).includes(d) ? `disabled data-held title="${name} already has this"` : ""}>${ic(KIND_ICON[d])} <b>${esc(cap(t))}</b></button>`).join("")}</div>
      <p class="muted" style="margin:6px 0">…or a pursuit in these ways:</p>
      <div class="colorpick">${COLORS.map((c) => `<button class="cbtn" data-c="${c}" aria-pressed="false">${pip(c)}<span>${CNAME[c]}</span></button>`).join("")}</div>
      <div class="inrow" style="margin-top:10px"><button class="primary" id="planCols">${ic("push")} This pursuit</button></div>`;
  } else {
    const v = p.preview || {};
    body = v.blocked ? `<p>${esc(v.blocked)}.</p>` : `<h3 style="margin:4px 0 0;font:600 var(--fs-3) var(--display)">${ic("target")} The plan to ${esc(v.name)}</h3>
      <div class="bigfelt"><b>${fpct(v.felt)}</b><div><div>how sure ${name} feels</div><div class="muted">plans like it come true <span class="hintw">${esc(v.hint)}</span></div></div></div>
      <table class="kv"><tr><td>Due</td><td>at ${Math.floor(v.due_age)}</td></tr><tr><td>Fit with who they are</td><td>${fitWord(v.fit)}</td></tr>${v.left_out && v.left_out.length ? `<tr><td>The feeling leaves out</td><td>${esc(v.left_out.join(", "))}</td></tr>` : ""}</table>
      <p class="muted" style="font-size:var(--fs-1)">They will hold your plan: it does not fade, and they will not drop it on their own. Keeping a plan builds self-control; giving it up wears it down.</p>`;
  }
  planEl.hidden = false;
  planEl.innerHTML = `<div class="box paper"><h2>${ic("quill")} A plan for ${name}</h2>${body}
    <div class="center" style="margin-top:12px;display:flex;gap:10px;justify-content:center">${p.step === "confirm" && !(p.preview || {}).blocked ? `<button class="primary" id="planOk">${ic("check")} Make the plan</button>` : ""}<button class="ghost" id="planX">${ic("x")} ${p.step === "horizon" ? "Close" : "Cancel"}</button></div></div>`;
  planEl.querySelectorAll("[data-v]").forEach((b) => b.addEventListener("click", () => send(b.dataset.v)));
  planEl.querySelectorAll(".cbtn").forEach((b) => b.addEventListener("click", () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true")));
  const pc = $("planCols"); if (pc) pc.addEventListener("click", () => { const cs = [...planEl.querySelectorAll('.cbtn[aria-pressed="true"]')].map((b) => b.dataset.c).join(""); if (cs) send(cs); else toast("Pick at least one color."); });
  const ok = $("planOk"); if (ok) ok.addEventListener("click", () => send(""));
  $("planX").addEventListener("click", () => send("x"));
  planEl.querySelectorAll(".drm").forEach((el) => { const g = (L.goals || []).find((x) => x.j === +el.dataset.gj); if (g) setTip(el, () => goalTip({ kind: g.kind, colors: g.colors, horizon: g.horizon, source: g.source, domain: g.domain }, g)); });
}

/* ---------------- part 2: the moment and its cards ---------------- */
const STRAIN = { no: 0, low: 1, medium: 2, high: 3 };
const ARROW = { "much worse": ["down", "▼▼"], worse: ["down", "▼"], "about right": ["eq", "●"], better: ["up", "▲"], "much better": ["up", "▲▲"] };
const MISREAD = { hopeful: ["down", "▼"], doubtful: ["up", "▲"], fair: ["eq", "●"] };
const MISREAD_WORD = { hopeful: "they think it likelier than it is", doubtful: "they think it less likely than it is", fair: "they read it about right" };
function shortName(label) {
  let s = cap(String(label).trim());
  const m = s.match(/^(.{10,}?)(,|;| — | - |:| and | until | so that | to see | while )/);
  if (m) s = m[1];
  if (s.length > 30) s = s.slice(0, 29).replace(/\s+\S*$/, "") + "…";
  return s;
}
function frameBG(cs) {
  if (!cs.length) return "linear-gradient(160deg,#5b566a,#2f2c3a)";
  if (cs.length === 1) return `linear-gradient(160deg, ${FRAME[cs[0]][0]}, ${FRAME[cs[0]][1]})`;
  if (cs.length === 2) return `linear-gradient(100deg, ${FRAME[cs[0]][0]}, ${FRAME[cs[0]][1]} 48%, ${FRAME[cs[1]][1]} 52%, ${FRAME[cs[1]][0]})`;
  return "linear-gradient(160deg, #ecd087, #a07a2c 55%, #e0bd6a)";
}
function artBG(cs) {
  if (!cs.length) return "radial-gradient(circle at 50% 60%, #6d6880, #1b1924)";
  if (cs.length === 1) return `radial-gradient(circle at 50% 62%, ${ART[cs[0]][0]} 0%, ${ART[cs[0]][1]} 72%)`;
  return `radial-gradient(circle at 30% 60%, ${ART[cs[0]][0]}cc 0%, transparent 55%), radial-gradient(circle at 72% 45%, ${ART[cs[1]][0]}cc 0%, transparent 55%), linear-gradient(110deg, ${ART[cs[0]][1]}, ${ART[cs[1]][1]})`;
}
function fxHTML(f) {
  const one = (x, cls) => { const k = x.slice(1); return `<span class="${cls}">${x[0] === "+" ? "+" : "−"}${ic(RES_ICON[k] || "dot")}</span>`; };
  const parts = (f.cost || []).map((x) => one(x, "c")).concat((f.win || []).map((x) => one(x, "w")), (f.lose || []).map((x) => one(x, "l")));
  return parts.length ? `<span class="fx">${parts.slice(0, 7).join("")}</span>` : "";
}
function firstThought(s) { const m = String(s || "").match(/⟦t:[^⟧]*⟧\*[^*]*\*⟦\/⟧/); return m ? m[0] : ""; }
const narrow = () => window.matchMedia("(max-width: 640px)").matches;

/* ---------------- the event window (Emren 09:25: a Paradox-style pop-up over the life, options as readable rows) ---------------- */
const evWrap = $("evwrap"), evBack = $("evback");
evBack.className = "evback"; evBack.innerHTML = `${ic("flag")} Back to the moment`;
evBack.addEventListener("click", () => setPeek(false));
function setPeek(on) { evWrap.classList.toggle("peek", on); evBack.hidden = !on || evWrap.hidden; if (on) { hideTip(); waitingCard(); } }
function showEv(on) { if (!on) { evWrap.hidden = true; evBack.hidden = true; evWrap.classList.remove("peek"); placeEv(false); } else evWrap.hidden = false; }
// v22 next look: the outcome window lies over the story column only, so the crest stays in view and its wheel and meters
// move while the result is read (desktop, where the crest is beside the story); the moment window covers the table
function placeEv(atRes) {
  const over = !!atRes && !evWrap.hidden && window.innerWidth > 1040 && !narrow();
  evWrap.classList.toggle("overstage", over);
  if (!over) { evWrap.style.left = evWrap.style.top = evWrap.style.width = evWrap.style.height = ""; return; }
  const r = stageEl.getBoundingClientRect();
  Object.assign(evWrap.style, { left: r.left + "px", top: r.top + "px", width: r.width + "px", height: r.height + "px" });
}
addEventListener("resize", () => { if (!evWrap.hidden && evWrap.classList.contains("overstage")) placeEv(true); });
// while a moment is set aside to look at the life, it waits as a card at the foot of the story (the Back button)
function waitingCard() {
  const cp = hud && hud.cp; if (!cp) { evBack.innerHTML = `${ic("flag")} Back to the moment`; return; }
  const src = picFor(cp.art);
  evBack.innerHTML = `${src ? `<img src="${esc(src)}" alt="" decoding="async" onerror="this.remove()">` : `<span class="wg">${ic("flag")}</span>`}<span class="wt"><small>A moment is waiting</small><b>${esc(cap(cp.title))}</b></span><span class="wgo">${ic("flag")} Open the moment</span>`;
}
const ACC_CLS = { "would go with it": "a0", "okay with it": "a1", reluctant: "a2", "against it": "a3", "their own pick": "own" };
const ACC_WORD = { "would go with it": "Would go with it", "okay with it": "Okay with it", reluctant: "Reluctant", "against it": "Against it", "their own pick": "Their own pick" };
const ACC_HELP = { "would go with it": "What they lean to, or close to it: pushed here, it costs them nothing.", "okay with it": "Not their first wish, but they are not against it: pushed here, it costs them nothing.",
  reluctant: "They would rather not: its colors lean against theirs, or they would rather do nothing. Weaker effort, some strain, and a wanting they swallow.", "against it": "It goes against who they are and who they want to be: half-hearted effort, strain, and pent-up wanting that can break through later.",
  "their own pick": "What they lean toward right now. Letting them choose costs nothing." };
const PLATE = { W: "#a88d3c", U: "#2c69b0", B: "#4a3a5e", R: "#b44627", G: "#2d7a46" };
const LIFE_ICON = [[/loss|grief|death/, "candle"], [/love|partner/, "heart"], [/child/, "child"], [/family|home/, "home"], [/work|money|career/, "case"],
  [/school|study|learning|mentor|mind/, "book"], [/friend|community|neighbour|team|choir/, "people"], [/faith|meaning|calling|tradition/, "shrine"],
  [/body|health|aging|sport/, "pulse"], [/nature/, "leaf"], [/conflict|risk|fear/, "bolt"], [/public|era|media/, "globe"], [/inner|identity|memory|passion/, "voice"],
  [/leisure|play|music|making|performing|food|travel/, "star"]];
function artIcon(a) {               // the moment's first life domain the icon set knows, then its tier, then a rough match
  const ds = String((a && a.life) || "").split(",").map((x) => x.trim()).filter(Boolean);
  for (const d of ds) if (GI.domain[d]) return GI.domain[d];
  if (a && GI.tier[a.tier]) return GI.tier[a.tier];
  const s = ds.join(" "); for (const [re, x] of LIFE_ICON) if (re.test(s)) return x; return a && a.recon ? "route" : "sign";
}
// an option's icon: drawn for this very option, else what the act is (a title it starts, money, a mark it leaves), else its color's mana symbol
function optIcon(o, sit) {
  const own = (GI.option[sit] || [])[o.k];
  if (own) return own;
  const t = String(o.tag || "").replace(/[-+][\d.]+$/, "");
  return GI.act[t] || (o.mark && GI.act[o.mark]) || null;
}
// the picture area: the moment's colors and a glyph for its part of life, until the visuals thread's pictures land (chroma-art/)
// the moment's picture (the visuals thread's engravings, chroma-art/game/pictures.json): by situation, then the original of a
// child version, then the first life domain, then the tier; the colors and a glyph show until it loads, or if it is missing
const PICS = __PICS__;
{ const f = $("fab"), u = PICS.texture && PICS.texture.unwritten_future; if (f && u) f.style.backgroundImage = `url("${u}")`; }
// a tribal or magic life shows its own world's tarot card (V The River, VI The Spires) wherever an Earth picture would show:
// the engravings are of the modern Earth (v22 patch, Emren 10-07 21:44 UTC); Earth lives read the pictures as before
const WORLD_CARD = { tribal: "5", magic: "6" };
const worldCard = (L) => { const k = WORLD_CARD[L && L.setting]; return k ? (PICS.tarot && PICS.tarot[k]) || "" : null; };
function picFor(a) {
  if (!a) return "";
  const w = worldCard(hud && hud.life); if (w != null) return w;
  const d = String(a.life || "").split(",").map((x) => x.trim()).find((x) => PICS.domain[x]);
  return PICS.situation[a.sit] || PICS.situation[a.variant_of] || (d && PICS.domain[d]) || PICS.tier[a.tier] || "";
}
function evArt(cs, icon, extra = "", a = null) {
  const src = picFor(a);
  return `<div class="evart" style="--art:${artBG(cs)}"><span class="stars"></span><span class="glyph">${ic(icon)}</span>${src ? `<img src="${esc(src)}" alt="" decoding="async" onerror="this.remove()">` : ""}${extra}</div>`;
}
function plate(ends) {
  if (!ends.length) return "#8a8174";
  return ends.length > 1 ? `linear-gradient(135deg, ${PLATE[ends[0]]} 0 50%, ${PLATE[ends[1]]} 50%)` : PLATE[ends[0]];
}
// v22 next look: an option is a compact card in a two-column grid. The icon tile carries the option's colors and its
// number (renumbered on the page in the order shown; the key still sends the engine's own number), the cost in colors sits
// at the top right, felt odds as a small ring gem with ▲/▼ only where reality differs. Badges only for what changes a
// decision: their own pick, the heart's and the head's pick, would rather not, against it, closed by the law or means.
// The rest (needs met, what may follow, perks that help) reads in the strip under the cards; .os keeps it for the phone.
const tileBG = (cs) => { const v = cs.map((c) => `var(--p${c})`); return !v.length ? "#d9cfbd" : v.length === 1 ? v[0] : `linear-gradient(135deg, ${v.map((x, k) => `${x} ${Math.round(k * 100 / (v.length - 1))}%`).join(", ")})`; };
function feltGem(f, cls, arrow) {
  const C = 2 * Math.PI * 6.5, v = clamp(f, 0.01, 0.99);
  return `<span class="gem"><svg viewBox="0 0 16 16" aria-hidden="true"><circle class="g0" cx="8" cy="8" r="6.5"/><circle class="g1" cx="8" cy="8" r="6.5" stroke-dasharray="${(v * C).toFixed(1)} ${C.toFixed(1)}"/></svg><b>${fpct(f)}</b>${arrow && cls !== "eq" ? `<i class="${cls}">${arrow}</i>` : ""}</span>`;
}
function optRow(o, i, num) {
  const pass = !o.means.length, st = o.status, ends = [...new Set(o.ends)], f = o.follows || {};
  const acc = o.own ? "their own pick" : o.accept || "okay with it";
  const oicon = pass ? null : optIcon(o, (hud && hud.cp && hud.cp.art && hud.cp.art.sit) || "");
  const [cls, arrow] = o.reality ? MISREAD[o.reality.misread] || ["eq", "●"] : ARROW[o.hint] || ["eq", ""];
  const n = num || o.n, cs = actColors(o.means, o.ends);
  const marks = [];
  if (o.own) marks.push(`<span class="mk2 own">${ic("crown")}their own pick</span>`);
  if (o.heart_pick) marks.push(`<span class="mk2 heart">${ic("heart")}heart</span>`);
  if (o.head_pick) marks.push(`<span class="mk2 head">${ic("head")}head</span>`);
  if (!o.own && (acc === "reluctant" || acc === "against it")) marks.push(`<span class="mk2 rel">${acc === "against it" ? "against it" : "would rather not"}</span>`);
  if (st === "out of reach") marks.push(`<span class="mk2 law why">${ic("lock")}${esc(o.why || "out of reach")}</span>`);
  else if (o.needs && o.closed) marks.push(`<span class="mk2 law why">${ic("lock")}${esc(CLOSED_WORD[o.closed] || "closed")}</span>`);
  if (o.lever) marks.push(`<span class="mk2 lever">${ic(o.lever.icon)}${esc(o.lever.name)}</span>`);
  const hp = (o.helped || []).find((h) => h.name === o.helped_row);     // a perk that sets this option apart; the strip lists all
  if (hp) marks.push(`<span class="mk2 rb up">${ic(roleIconOf(hp))}${esc(hp.pred)}</span>`);
  for (const x of (o.roles_fx || []).slice(0, 1)) marks.push(`<span class="mk2 rb ${x.gain ? "up" : "down"}${x.when === "fail" ? " iffail" : ""}">${ic(roleIconOf(x))}${x.gain ? "+" : "−"} ${esc(x.title ? shortSay(x.say) : x.name)}</span>`);
  const bits = [];                                      // the small print, shown on the phone and in the strip
  if (f.needs && f.needs.length) bits.push(`<span>meets ${esc(f.needs.join(" and "))}</span>`);
  for (const x of (f.lift || [])) bits.push(`<span class="up">${ic(NEED_ICON[x.need] || "dot")} ${esc(NEED_LONG[x.need] || x.need)} is ${esc(x.word)}: ${esc(x.lift)}</span>`);
  if (o.commit) bits.push(`<span>${ic(KIND_ICON[o.commit] || "anchor")} could start a ${esc(o.commit)}</span>`);
  if (o.needs) bits.push(`<span class="why">${ic("lock")} ${esc(o.needs.line)}</span>`);
  if (!pass) bits.push(fxHTML(f));
  if (pass) return `<button class="opt pass onone" data-i="${i}" data-num="${n}" style="--n:${i}" aria-label="${esc(n + ": " + cap(o.label) + ". " + ACC_WORD[acc])}">
    ${ic("hourglass")}<span class="obody"><span class="ot">${esc(cap(o.label))}</span><span class="os"><span>Nothing changes now; wanting and pressure keep building.</span></span></span>
    <span class="acc ${ACC_CLS[acc]}">${o.own ? ic("crown") : ""}${ACC_WORD[acc]}</span><span class="keyn">key ${n}</span></button>`;
  return `<button class="opt${o.own ? " own" : ""}${st === "out of reach" ? " far" : ""}${st === "didn't think of it" ? " ghost" : ""}" data-i="${i}" data-num="${n}" style="--n:${i};--tile:${tileBG(cs)}" aria-label="${esc(n + ": " + cap(o.label) + ". " + ACC_WORD[acc] + ". Feels " + fpct(o.felt))}">
    <span class="oi">${oicon ? ic(oicon) : `<svg class="mana" aria-hidden="true"><use href="#${MANA(ends[0] || cs[0])}"/></svg>`}<span class="no">${n}</span></span>
    <span class="ocost">${pips(cs)}</span>
    <span class="obody"><span class="ot">${esc(cap(o.label))}</span><span class="os">${bits.filter(Boolean).join("")}</span></span>
    <span class="ometa">${marks.join("")}<span class="acc ${ACC_CLS[acc]}">${o.own ? ic("crown") : ""}${ACC_WORD[acc]}</span><span class="odds"><small>feels</small>${feltGem(o.felt, cls, arrow)}</span></span>
  </button>`;
}
// the reading strip: what one option means, filled on hover or focus (it replaces the floating tooltip at a moment)
function stripHTML(o, num) {
  const f = o.follows || {}, acc = o.own ? "their own pick" : o.accept || "okay with it", facts = [];
  const pass = !o.means.length;
  if (!pass) {
    facts.push(`<span><b>Feels</b> ${fpct(o.felt)}${o.reality ? (o.reality.misread !== "fair" ? `, <span class="${o.reality.misread === "hopeful" ? "down" : "up"}">${o.reality.misread === "hopeful" ? "reality is harsher" : "reality is kinder"}</span>` : ", about right") : o.hint ? `, looks ${esc(o.hint)}` : ""}</span>`);
    if (o.base != null) facts.push(`<span><b>Most people</b> ${baseWord(o.base).replace(/^it /, "")}</span>`);
  }
  facts.push(`<span><b>${esc(ACC_WORD[acc])}</b>${o.status === "didn't think of it" ? " · hadn't thought of it" : ""}${acc === "against it" && o.clash && o.clash.length ? ` · ${o.clash.map((c) => CNAME[c]).join(" and ")} against who they are` : ""}</span>`);
  if (o.status === "considered" && !o.own && o.lean != null) facts.push(`<span><b>Their lean</b> ${pct(o.lean)}</span>`);
  if (f.needs && f.needs.length) facts.push(`<span><b>Meets</b> ${esc(f.needs.join(", "))}</span>`);
  if ((f.lift || []).length) facts.push(`<span class="up"><b>Lacking</b> ${f.lift.map((x) => `${esc(NEED_LONG[x.need] || x.need)} at ${pct(x.level)}: ${esc(x.lift)} to satisfaction if it works`).join("; ")}</span>`);
  if (!o.own && !pass && o.rel >= 0.02) facts.push(`<span${o.resent > o.rel + 0.005 ? ' class="down"' : ""}><b>If you push</b> ${o.resent < 0.05 ? "little resentment" : o.resent < 0.3 ? "some resentment" : o.resent < 0.6 ? "resentment: strain and pent-up wanting" : "strong resentment"}${Math.abs(o.trust || 0) >= 0.05 ? ` (${o.trust > 0 ? "they trust you" : "they distrust you"} in these colors)` : ""}; it counts against their own life unless it gives them something they lack</span>`);
  if (f.cost && f.cost.length) facts.push(`<span><b>Costs</b> ${f.cost.map((x) => `${ic(RES_ICON[x.slice(1)] || "dot")}${esc(x.slice(1))}`).join(" ")}</span>`);
  if (!pass) facts.push(`<span><b>If it works</b> ${f.win && f.win.length ? `<span class="up">${f.win.map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).join(" ")}</span>, ` : ""}toward ${pips(o.ends)}</span>`);
  if (!pass) facts.push(`<span><b>If it fails</b> <span class="down">${(f.lose || []).map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).concat(["strain", "doubt"]).join(", ")}</span></span>`);
  if (o.commit) facts.push(`<span><b>Could start</b> ${ic(KIND_ICON[o.commit] || "anchor")} a ${esc(o.commit)}${f.commit_p ? ` (about ${pct(f.commit_p)})` : ""}</span>`);
  if (o.lever) facts.push(`<span class="lever"><b>A push on the world</b> ${ic(o.lever.icon)}${esc(o.lever.what || o.lever.name)}${o.lever.target ? ` (${esc(o.lever.target)})` : ""}</span>`);
  if (o.status === "out of reach") facts.push(`<span class="down"><b>Out of reach</b> ${esc(o.why)}; can be forced, at higher risk</span>`);
  if (o.needs) facts.push(`<span><b>Needs</b> ${esc(o.needs.line)}${o.closed ? `; without it ${CLOSED_WORD[o.closed] || "the world"} stands in the way` : ""}</span>`);
  if ((o.helped || []).length) facts.push(`<span><b>Helped by</b> ${o.helped.map((h) => `${esc(h.pred)}${h.plus ? ` <span class="up">+${h.plus}%</span>` : ""}`).join(", ")}</span>`);
  if ((o.roles_fx || []).length) facts.push(`<span><b>Titles and perks</b> ${o.roles_fx.map((x) => `<span class="${x.gain ? "up" : "down"}">${esc(x.line)}</span>`).join("; ")}</span>`);
  return `<div class="dt"><span class="num">${num}</span> ${esc(cap(o.label))}</div><div class="facts">${facts.join("")}</div><div class="dhelp">${esc(ACC_HELP[acc])}</div>`;
}
function hhBars(o) {
  const why = (side) => ((o.drivers || {})[side] || []).map(([n, v]) => `<span class="${v > 0 ? "up" : "down"}">${v > 0 ? "+" : "−"}</span>${esc(n)}`).join(", ");
  const row = (icon, v, col, w) => `<div class="tipbar"><span style="color:${col}">${ic(icon)}</span><i><b style="width:${(clamp(v / 0.6) * 100).toFixed(0)}%;background:${col}"></b></i><span>${pct(v)}</span></div>${w ? `<div class="muted" style="font-size:var(--fs-1);margin:-1px 0 3px 20px">${w}</div>` : ""}`;
  return row("heart", o.heart, "var(--heart)", why("heart")) + row("head", o.head, "var(--head)", why("head"));
}
function tipOption(o, name, num) {
  const f = o.follows || {}, rows = [], acc = o.own ? "their own pick" : o.accept || "okay with it";
  // no colour or pair is called an enemy (implementation list item 5, chroma-philosophy/enemy-pairs.md): the option goes against who they are
  const against = acc === "against it" && o.clash && o.clash.length ? `<br><span class="down">${o.clash.map((c) => pip(c)).join("")} This goes against who they are</span>` : "";
  rows.push(["How they feel", `<b>${ACC_WORD[acc]}</b>` + (o.status === "didn't think of it" ? " (they hadn't thought of it)" : "") + against]);
  if (o.lever) rows.push(["A push on the world", `${ic(o.lever.icon)} ${esc(o.lever.name)}: ${esc(o.lever.what)}${o.lever.target ? ` (${esc(o.lever.target)})` : ""}`]);
  if (o.means.length) {
    rows.push(["Feels", `${fpct(o.felt)} likely to work`]);
    if (o.base != null) rows.push(["For most people", baseWord(o.base)]);
    if (o.reality) rows.push(["Reality, roughly", `works ${esc(o.reality.band)}` + (o.reality.misread !== "fair" ? `<br><span class="${o.reality.misread === "hopeful" ? "down" : "up"}">${MISREAD_WORD[o.reality.misread]}</span>${o.reality.why ? ` (${esc(o.reality.why)})` : ""}` : "")]);
    else rows.push(["Reality", o.hint ? `looks ${o.hint}` : "–"]);
    if (o.heart != null) rows.push(["Heart and head", hhBars(o)]);
    rows.push(["Colors", colorsHTML(o.means, o.ends) + " " + actColors(o.means, o.ends).map((c) => CNAME[c]).join(" and ")]);
  }
  if (o.status === "considered" && !o.own) rows.push(["Their lean", `${pct(o.lean)} likely to pick it themselves`]);
  if (o.status === "out of reach") rows.push(["Out of reach", `${esc(o.why)}; can be forced, at higher risk`]);
  if (f.needs && f.needs.length) rows.push(["Meets", esc(f.needs.join(", "))]);
  if (f.cost && f.cost.length) rows.push(["Costs", f.cost.map((x) => `${ic(RES_ICON[x.slice(1)] || "dot")} ${esc(x.slice(1))}`).join(" ")]);
  if (f.win && f.win.length) rows.push(["If it works", `<span class="up">${f.win.map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).join(" ")}</span>, draws them toward ${colorsHTML(o.ends, o.ends)}`]);
  else if (o.means.length) rows.push(["If it works", `draws them toward ${colorsHTML(o.ends, o.ends)}`]);
  if (o.means.length) rows.push(["If it fails", `<span class="down">${(f.lose || []).map((x) => `${x[0] === "+" ? "+" : "−"}${esc(x.slice(1))}`).concat(["strain", "doubt in these ways"]).join(", ")}</span>`]);
  if (o.commit) rows.push(["Could start", `${ic(KIND_ICON[o.commit] || "anchor")} a ${esc(o.commit)}` + (f.commit_p ? ` (about ${pct(f.commit_p)})` : "")]);
  if (o.needs) rows.push(["Needs", `${esc(cap(o.needs.line))}` + (o.closed ? `. Without it, ${CLOSED_WORD[o.closed] || "the world"} stands in the way: it can still be tried, at higher risk.` : ".")]);
  if ((o.helped || []).length) rows.push(["Helped by", o.helped.map((h) => `${ic(roleIconOf(h))} ${esc(cap(h.pred))}${h.plus ? ` <span class="up">+${h.plus}%</span>` : ""}`).join("<br>")]);
  if ((o.roles_fx || []).length) rows.push(["Titles and perks", o.roles_fx.map((x) => `<span class="${x.gain ? "up" : "down"}">${ic(roleIconOf(x))}</span> ${esc(x.line)}`).join("<br>")]);
  if (o.heart_pick || o.head_pick) rows.unshift(["Inner voice", (o.heart_pick ? `<span style="color:var(--heart)">${ic("heart")} the heart's pick</span> ` : "") + (o.head_pick ? `<span style="color:var(--head)">${ic("head")} the head's pick</span>` : "")]);
  return tipBox(`<span class="num">${num || o.n}</span> ${esc(cap(o.label))}`, "", rows, esc(ACC_HELP[acc]));
}
let lastArt = null, lastCpKey = "", CPNUM = new Map();
// G1 (B package): "Out of reach, but you could force it" folds into one row until opened; the choice is kept in this
// browser. Folded cards are not drawn at all, so nothing hidden can be hovered, clicked or measured. openOOR(num) opens
// the fold and focuses that card: a number key on a folded card shows it first, and the same key again pushes.
let oorOpen = false; try { oorOpen = localStorage.getItem("chroma.oorOpen") === "1"; } catch (_) {}
let openOOR = null;
function evHead(kick, title, right) { return `<div class="evh"><span class="kick">${kick}</span><h2 id="evTitle">${title}</h2>${right || ""}</div>`; }
function renderTable(h) {
  const cp = h && h.cp, L = h && h.life;
  const atres = !cp && !!(h && h.res) && !busy;
  stageEl.classList.toggle("atcp", (!!cp || atres) && !busy);
  stageEl.classList.toggle("atres", atres);
  if (!atres) feedEl.querySelectorAll(".en.fresh").forEach((x) => x.classList.remove("fresh"));
  if (choosing && busy) return;                       // the choice is being lived: the window keeps it, with its spinner
  if (choosing && atres) {                            // a beat of "trying" before the outcome, so the change reads as one
    const wait = (flyer ? 600 : 520) - (performance.now() - choosing.t);
    if (wait > 0) { clearTimeout(renderTable.t); renderTable.t = setTimeout(() => renderTable(hud), wait); return; }
  }
  const reveal = !!choosing && atres;
  choosing = null; tableEl.classList.remove("choosing");
  if (!reveal) dropFlyer();
  if (atres) return renderResolution(h, reveal);
  if (!cp || busy) { showEv(false); tableEl.innerHTML = ""; selected = null; lastCpKey = ""; return; }
  const key = cp.age + "|" + cp.title;
  if (key === lastCpKey && !evWrap.hidden) return;
  placeEv(false); dropFlyer();
  lastCpKey = key; selected = null; lastArt = cp.art || null;
  const n = cp.stake_word === "very high" ? 3 : cp.stake_word === "high" ? 2 : 1;
  const idx = cp.options.map((o, i) => [o, i]);
  // numbers in the order shown (Do nothing last), so a set-aside option leaves no gap; CPNUM maps them back
  const groups = [["considered", ""], ["didn't think of it", "Ways they haven't thought of"], ["out of reach", "Out of reach, but you could force it"]];
  const order = [];
  const parts = groups.map(([st, title]) => {
    const xs = idx.filter(([o]) => o.status === st && o.means.length).sort((a, b) => a[0].n - b[0].n);
    xs.forEach(([o]) => order.push(o));
    return [title, xs, st];
  });
  const passes = idx.filter(([o]) => !o.means.length);
  passes.forEach(([o]) => order.push(o));
  CPNUM = new Map(order.map((o, k) => [k + 1, o]));
  const numOf = (o) => order.indexOf(o) + 1;
  const cards = (xs) => xs.map(([o, i]) => optRow(o, i, numOf(o))).join("");
  const oorXs = (parts.find((p) => p[2] === "out of reach") || [0, []])[1];
  const nums = (xs) => { const a = numOf(xs[0][0]), b = numOf(xs[xs.length - 1][0]); return a === b ? `key ${a}` : `keys ${a}–${b}`; };
  const rows = parts.map(([title, xs, st]) => !xs.length ? "" : st === "out of reach"
      ? `<button type="button" class="ask sub oorfold" id="evOOR" aria-expanded="${oorOpen}" aria-controls="evOORg">${ic("lock")} ${title} <small>${xs.length} ${xs.length > 1 ? "options" : "option"} · ${nums(xs)}</small><span class="chev" aria-hidden="true">▸</span></button>`
        + `<div class="ogrid oorg" id="evOORg">${oorOpen ? cards(xs) : ""}</div>`
      : (title ? `<div class="ask sub">${title}</div>` : "") + `<div class="ogrid">${cards(xs)}</div>`).join("")
    + passes.map(([o, i]) => optRow(o, i, numOf(o))).join("");
  const pick = cp.options.filter((o) => o.heart_pick || o.head_pick || o.own);
  const cs = [...new Set([].concat(...pick.map((o) => o.ends)))].slice(0, 2);
  const a = cp.art || {}, kick = [`Age ${Math.floor(cp.age)}`, a.tier, String(a.life || "").split(",")[0].trim()].filter(Boolean).map(esc).join(" · ");
  // the inner voice in three short lines: what the heart says, what the head says, what they would do left alone
  const hp = cp.options.find((o) => o.heart_pick), dp = cp.options.find((o) => o.head_pick), op = cp.options.find((o) => o.own);
  const vline = (k, icon, who, o) => o ? `<div class="vline ${k}"><span class="vi">${ic(icon)}</span><span><small>${who}</small><em>${esc(cap(o.label))}</em></span></div>` : "";
  const vlines = cp.voice ? (hp && hp === dp ? vline("hd", "heart", "Heart and head agree", hp) : vline("h", "heart", "The heart says", hp) + vline("d", "head", "The head says", dp)) + vline("o", "crown", `Left alone, ${esc(L.name)} would`, op) : "";
  const asides = cp.voice ? cp.voice.asides.filter((x) => !/⟦j:lean_other⟧/.test(x)) : [];
  tableEl.innerHTML = evHead(`${ic("flag")} ${kick}`, esc(cap(cp.title)),
      `${cp.voice ? tugBar(cp.voice.self_control, "tug") : ""}<span class="stakes">${[1, 2, 3].map((k) => `<span class="${k <= n ? "" : "off"}">${ic("flame")}</span>`).join("")}</span>`) + `
    <div class="evl">${evArt(cs, artIcon(cp.art), "", cp.art)}
      <div class="evtext">
        ${cp.season && cp.season.this_week ? `<p class="seasonnote" id="cpSeason">${ic("gate")} ${cp.season.transform ? "A turning point of this season: this choice can change who they become." : esc(seasonWords(cp.season)) + "."}</p>` : ""}
        ${cp.scene ? `<p class="scene" data-i="cp">${rich(cp.scene)}</p>` : ""}
        ${cp.extra ? `<p class="note">${rich(cp.extra)}</p>` : ""}
        ${cp.thought ? `<p class="note">${rich(cp.thought)}</p>` : ""}
        ${cp.voice ? `<div class="voicebox"><p class="insight">${rich(cp.voice.line)}</p><div class="vlines">${vlines}</div>${asides.map((x) => `<p class="aside">${rich(x)}</p>`).join("")}</div>` : ""}
      </div></div>
    <div class="evr" id="evOpts"><div class="ask">What will ${esc(L.name)} do? <small>${touchUI ? "tap to read · tap again to push" : "hover to read · click or press its number to push"}</small></div>${rows}
      ${touchUI ? "" : `<div class="dstrip idle" id="evStrip" aria-live="polite"><div class="dt">Hover a card to read it here: how sure ${esc(L.name)} feels, what it would meet, what may follow.</div></div>`}</div>
    <div class="evf"><button class="primary" id="evLet">${ic("crown")} Let ${esc(narrow() ? "them" : L.name)} choose</button>
      <span class="legend"><span><b>Feels</b> how sure ${esc(L.name)} is it will work · ▲ reality kinder · ▼ harsher</span></span>
      <button class="ghost" id="evPeek">${ic("eye")} Look at the life</button></div>`;
  showEv(true); setPeek(false);
  $("evOpts").scrollTop = 0;
  if (cp.voice) setTip($("tug"), () => voiceTip([cp.voice.key, cp.voice.heart_driver, cp.voice.head_driver, cp.voice.self_control]));
  setTip(tableEl.querySelector(".stakes"), () => tipBox(`${ic("flame")} Stakes: ${cp.stake_word}`, "How much this moment can change them.", [], ""));
  $("evLet").addEventListener("click", () => send(""));
  const own = cp.options.find((o) => o.own); setTip($("evLet"), () => tipBox(`${ic("crown")} Their own choice`, own ? esc(cap(own.label)) : "", [], "They act as they lean, with no cost. Key Enter."));
  $("evPeek").addEventListener("click", () => setPeek(true));
  const strip = $("evStrip"), idleStrip = strip ? strip.innerHTML : "";
  const fill = (o, num) => { if (!strip) return; strip.classList.remove("idle"); strip.innerHTML = stripHTML(o, num); };
  // v22.1: when the mouse leaves a card, the reading goes back to the card that has keyboard focus, or to a card still
  // under the mouse, before it goes idle (v22 closed it even while another card had focus)
  let hov = null;
  const unfill = () => {
    if (!strip || tableEl.classList.contains("choosing")) return;
    const f = document.activeElement;
    if (f && f.classList && f.classList.contains("opt") && tableEl.contains(f)) return fill(cp.options[+f.dataset.i], +f.dataset.num);
    if (hov && hov[2].isConnected) return fill(hov[0], hov[1]);
    strip.classList.add("idle"); strip.innerHTML = idleStrip;
  };
  const bindOpt = (b) => {
    const o = cp.options[+b.dataset.i], num = +b.dataset.num;
    const hl = (on) => hudEl.querySelectorAll(".orb").forEach((x) => x.classList.toggle("hl", on && o.ends.includes(x.dataset.c)));
    b.addEventListener("pointerenter", (e) => { if (e.pointerType !== "touch") { hov = [o, num, b]; hl(true); fill(o, num); } });
    b.addEventListener("pointerleave", () => { if (hov && hov[2] === b) hov = null; hl(false); unfill(); });
    b.addEventListener("focus", () => fill(o, num)); b.addEventListener("blur", () => setTimeout(unfill, 0));   // after focus has landed
    b.addEventListener("click", () => {
      const go = () => send(o.own ? "" : String(o.n));
      if (!touchUI || selected === o.n) return go();
      selected = o.n;
      tableEl.querySelectorAll(".opt").forEach((x) => x.classList.toggle("sel", x === b));
      tableEl.querySelectorAll(".optdetail").forEach((x) => x.remove());
      const d = document.createElement("div"); d.className = "optdetail";
      d.innerHTML = tipOption(o, L.name, num) + `<div class="center" style="margin-top:8px"><button class="primary" id="pushIt">${ic(o.own ? "crown" : "push")} ${o.own ? "Let them choose this" : "Push them to this"}</button></div>`;
      b.after(d); $("pushIt").addEventListener("click", go);
      d.scrollIntoView({ block: "nearest" });
    });
  };
  tableEl.querySelectorAll(".opt").forEach(bindOpt);
  const fold = $("evOOR");
  const setOOR = (on) => {
    const g = $("evOORg"); if (!fold || !g) return;
    const had = g.contains(document.activeElement);
    oorOpen = on; try { localStorage.setItem("chroma.oorOpen", on ? "1" : ""); } catch (_) {}
    fold.setAttribute("aria-expanded", String(on));
    if (hov && g.contains(hov[2])) hov = null;
    g.innerHTML = on ? cards(oorXs) : "";
    g.querySelectorAll(".opt").forEach(bindOpt);
    if (had) fold.focus();
    unfill();
  };
  openOOR = fold ? (num) => { if (!oorOpen) setOOR(true); const b = $("evOORg").querySelector(`.opt[data-num="${num}"]`); if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "nearest" }); } } : null;
  if (fold) fold.addEventListener("click", () => { setOOR(!oorOpen); if (oorOpen) { const g = $("evOORg"); if (g.lastElementChild) g.lastElementChild.scrollIntoView({ block: "nearest" }); } });
}

const SURPRISE = { better: "better than they expected", "as expected": "as they expected", worse: "worse than they feared" };
function renderResolution(h, reveal) {
  const r = h.res, L = h.life;
  const key = "res|" + r.age + "|" + r.title;
  if (key === lastCpKey && !evWrap.hidden) return;
  tableEl.classList.toggle("reveal", !!reveal); if (reveal) setTimeout(() => tableEl.classList.remove("reveal"), 900);
  lastCpKey = key; selected = null;
  const { means, ends } = splitColors(r.colors);
  const hhs = (r.pushed ? `<span class="tag push">${ic("push")}pushed by you${r.rel >= 0.02 ? ` · they were ${r.rel < 0.3 ? "okay with it" : r.rel < 0.6 ? "reluctant" : "against it"}` : ""}</span>` : "") +
    (r.with_heart ? `<span class="tag heart">${ic("heart")}the heart's choice</span>` : "") + (r.with_head ? `<span class="tag head">${ic("head")}the head's choice</span>` : "") +
    (!r.with_heart && !r.with_head && !r.pushed ? `<span class="tag">${ic("route")}a third way</span>` : "") + (r.regret ? `<span class="tag regret">${ic("rain")}will be regretted</span>` : "");
  const people = (r.people || []).map(castById).filter(Boolean).slice(0, 5).map((p) => `<span class="av${p.alive ? "" : " gone"}" data-pid="${p.id}" style="--ac:${GROUP_COL[ROLE_GROUP[baseRole(p.role)] || "other"]}">${esc(p.name[0])}</span>`).join("");
  const top = (r.became || []).map((c) => c.what);
  const chips = (r.became || []).map((c) => chgChip(c, true)).concat((r.changes || []).filter((c) => !top.includes(c.what) && !c.what.startsWith("color:")).slice(0, 5).map((c) => chgChip(c))).join("");
  const dw = r.dw || [0, 0, 0, 0, 0], mx = Math.max(0.4, ...dw.map(Math.abs));
  const cmove = `<div class="cmove" id="cmove">${COLORS.map((c, i) => { const v = dw[i], hgt = Math.abs(v) / mx * 19; return `<div class="cb"><div class="col"><b style="background:var(--c${c});${v >= 0 ? `bottom:50%;height:${hgt.toFixed(1)}px` : `top:50%;height:${hgt.toFixed(1)}px`}"></b></div>${pip(c)}</div>`; }).join("")}</div>`;
  const cl = r.closer, nowC = lettersOf(r.identity && r.identity.now);
  const toward = cl ? `<div class="toward" id="toward">${pips(nowC.length ? nowC : ["W"])}<span>${ic("push")}</span>${pips(lettersOf(cl.identity))}<div><div class="tw">${esc(cl.guild)}</div><small>${cl.distance < 0.05 ? "a step away" : "on the way"}</small></div><div class="dist"><b style="width:${(clamp(1 - cl.distance / 0.15) * 100).toFixed(0)}%"></b></div></div>` :
    nowC.length ? `<div class="toward" id="toward">${pips(nowC)}<div><div class="tw">${esc(r.identity.guild)}</div><small>who they are now</small></div></div>` : "";
  const les = r.lessons || [];
  const vword = `${r.worked ? "It worked" : "It went badly"}${SURPRISE[r.surprise] ? ", " + SURPRISE[r.surprise] : ""}`;
  tableEl.innerHTML = evHead(`${ic("rune")} What came of it · Age ${Math.floor(r.age)}`, esc(cap(r.act)), colorsHTML(means, ends)) + `
    <div class="evl">${evArt(ends.length ? ends : means, artIcon(lastArt), `<span class="seal2 ${r.worked ? "ok" : "bad"}">${ic(r.worked ? "check" : "cross")}</span>`, lastArt)}
      <div class="evtext">
        <div class="verdict vbig ${r.worked ? "ok" : "bad"}"><span class="sur">${esc(vword)}</span></div>
        ${r.world_push ? `<div class="verdict"><span class="tag${r.world_push.backfire ? " down" : ""}">${ic("ci-crowd")}${esc(r.world_push.target ? cap(r.world_push.target) + ": " : "")}${esc(r.world_push.backfire ? "it backfired" : r.world_push.word)}</span></div>` : ""}
        ${r.long_shot ? `<div class="verdict"><span class="tag lshot">${ic("star")}a long shot${(r.long_shot.tries || 1) > 1 ? `, try ${r.long_shot.tries}` : ""}, ${r.long_shot.made ? "made" : "missed"}: ${esc(odds100(r.long_shot.odds))}</span>${r.long_shot.rung ? ` <span class="tag">${ic("route")}after ${r.long_shot.rung.years <= 1 ? "a year" : r.long_shot.rung.years + " years"} ${/^(a|an|the|one) /.test(r.long_shot.rung.say) ? "as " : ""}${esc(r.long_shot.rung.say)}</span>` : ""}</div>` : ""}
        <div class="verdict">${hhs}</div>
        ${people ? `<div class="verdict"><span class="muted">With</span><span class="with">${people}</span></div>` : ""}
      </div></div>
    <div class="evr"><div class="reso-r">
      <p class="scene" data-i="res">${rich(r.text)}</p>
      ${r.pressure ? `<p class="note pressure">${esc(r.pressure)}</p>` : ""}
      ${r.rename ? `<div class="rename" id="rename"><span class="k">${ic("quill")} A new name?</span><span>${esc(L.name)} names who they are. They may take a new name, or keep their own.</span>
        <div class="inrow"><input class="field" id="rnTxt" type="text" maxlength="24" autocomplete="off" spellcheck="false" value="${esc(r.rename.suggest)}" aria-label="New name"><button class="primary" id="rnTake">${ic("quill")} Take it</button><button class="ghost" id="rnKeep">Keep ${esc(r.rename.old)}</button></div></div>` : ""}
      ${chips ? `<div class="became">${chips}</div>` : ""}
      ${(r.needs || []).length ? `<div class="ndmove" id="ndmove">${r.needs.slice(0, 4).map((x) => `<div class="r">${ic(NEED_ICON[x.need] || "dot")}<span>${esc(cap(NEED_LONG[x.need] || x.need))}</span><span class="${x.delta > 0 ? "up" : "down"}">${pct(x.before)} → ${pct(x.after)}</span>${x.lacking && x.delta > 0 ? `<small class="muted">was lacking</small>` : ""}</div>`).join("")}</div>` : ""}
      ${r.hindsight && r.hindsight.line ? `<p class="hind ${r.hindsight.kind === "accepted" ? "up" : "down"}" id="hind">${rich(r.hindsight.line)}</p>` : ""}
      <div class="row2 shiftbox">${cmove}${toward}</div>
      ${(r.states || []).length ? `<div class="states">${r.states.map((x) => `<span class="st g${x.what === "gained" ? x.good : 0}${x.what === "gained" ? "" : " gone"}">${ic(x.icon)}${x.what === "gained" ? "Now " : "No longer "}${esc(x.word)}</span>`).join("")}</div>` : ""}
      ${(r.roles || []).length ? `<div class="states">${r.roles.map((x, i) => `<span class="st rl g${x.up ? 1 : 0}${x.up ? "" : " gone"}" data-rr="${i}">${ic(roleIconOf(x))}${esc(x.up && x.title ? "Now " + x.word : cap(x.word))}</span>`).join("")}</div>` : ""}
      ${les.length ? `<div class="lesson">${ic("rune")}<div><span class="k">How the world works</span>${rich(les[0].line)}${les.slice(1, 2).map((x) => `<span class="more">${rich(x.line)}</span>`).join("")}</div></div>` : ""}
    </div></div>
    <div class="evf"><button class="primary" id="goOn">${ic("play")} Go on</button><span class="legend"><span>Hover the changes and colors for the numbers behind them</span></span>
      <button class="ghost" id="evPeek">${ic("eye")} Look at the life</button></div>`;
  showEv(true); setPeek(false); placeEv(true);
  if (reveal && flyer) flipFlyer(r.worked, vword); else dropFlyer();
  $("goOn").addEventListener("click", () => send(""));
  $("evPeek").addEventListener("click", () => setPeek(true));
  if (r.rename) {
    const rn = (v) => { const box = $("rename"); if (box) box.remove(); lastSent = "="; if (!ready || busy) return; worker.postMessage({ cmd: "line", text: "=" + v }); };
    $("rnTake").addEventListener("click", () => rn(($("rnTxt").value || "").trim() || r.rename.suggest));
    $("rnKeep").addEventListener("click", () => rn(r.rename.old));
    $("rnTxt").addEventListener("keydown", (e) => { e.stopPropagation(); if (e.key === "Enter") { e.preventDefault(); $("rnTake").click(); } });
  }
  tableEl.querySelectorAll("[data-z]").forEach((x) => { const z = x.dataset.z.split("|"); setTip(x, () => changeTip(z[0], +z[1], +z[2])); });
  if ($("ndmove")) setTip($("ndmove"), () => tipBox(`${ic("compass")} Needs this week`, "", (r.needs || []).map((x) => [esc(cap(NEED_LONG[x.need] || x.need)), `${pct(x.before)} → ${pct(x.after)} (${sgn(x.delta * 100)} pts)`]), "An act that works feeds the needs its ends serve, and a lacking need lifts satisfaction most. Needs also fade a little every week."));
  if ($("hind")) setTip($("hind"), () => tipBox(`${ic("voice")} Looking back on your push`, "", [["Trust in you, these colors", `${sgn((r.hindsight.trust_before || 0) * 100)} → ${sgn((r.hindsight.trust_after || 0) * 100)}`]],
    r.hindsight.kind === "accepted" ? "It worked and gave them something they lacked, so part of the push's cost is undone: less strain and pent-up wanting, and it counts less against their own life." : "It failed, or gave them nothing they lacked. They hold it against you, and later pushes in these colors cost more."));
  tableEl.querySelectorAll("[data-pid]").forEach((x) => setTip(x, () => personTip(+x.dataset.pid)));
  tableEl.querySelectorAll("[data-rr]").forEach((x) => { const d = r.roles[+x.dataset.rr]; setTip(x, () => roleTip(d, findRole(d.name))); });
  setTip($("cmove"), () => tipBox(`${ic("wheel")} The colors this week`, "", [["Moved", colorMoves(r.dw)]], (r.push || []).map((p) => `${esc(cap(p.why))}: ${p.dir} ${pip(p.color)}`).join("<br>") || "Points are shares of 100."));
  if ($("toward")) setTip($("toward"), () => cl ? tipBox(`${pips(lettersOf(cl.identity))} Moving toward ${esc(cl.guild)}`, "", [["Still to go", `${(cl.distance * 100).toFixed(1)} pts`]], "A color joins who they are above 22% and leaves below 18%.") : tipBox(`${pips(nowC)} ${esc(r.identity.guild)}`, "", [], "No identity is close to changing this week."));
  tableEl.querySelectorAll(".verdict .tag").forEach((x) => setTip(x, () => tipBox(`${ic("voice")} Heart and head`, "", [], x.classList.contains("push") ? "You chose for them. If they were okay with it, it cost little; the less they wanted it, the more it cost: effort, strain and pent-up wanting." : x.classList.contains("regret") ? "The heart won against the head, and it failed. Regret lingers, and it can bring back what was let go." : "Before the choice, the heart (impulse) and the head (reflection) each had a favourite. This is which one they followed.")));
}

/* ---------------- menu, setup ---------------- */
/* ---------------- points 1 and 2 (Emren 20:39): between two moments, a slow interlude of everyday life. The routine of
   these years (routine.py, read through who they are), the season and age going by, and the colors moving week by week.
   The next moment waits until it ends; Skip (or Enter) ends it at once. ---------------- */
const IL_PACE = { slow: { wk: 120, min: 7000, max: 16000, line: 2700 }, short: { wk: 45, min: 3200, max: 7000, line: 1500 } };
const PACE_WORD = { slow: "slow", short: "short", off: "off" };
let ilPace = "slow"; try { ilPace = localStorage.getItem("chroma.pace") || "slow"; } catch (_) {}
const SEASON = (t) => { const k = ((t % 52) + 52) % 52; return k < 9 || k >= 48 ? "winter" : k < 22 ? "spring" : k < 35 ? "summer" : "autumn"; };
const SEASON_ICON = { winter: "ci-candle", spring: "ci-sapling", summer: "sun", autumn: "leaf" };
const interEl = document.createElement("div"); interEl.className = "inter"; interEl.hidden = true; stageEl.appendChild(interEl);
const IL = { on: false };
let lastSent = "";
function ilPic(L, age) {
  const w = worldCard(L); if (w != null) return w;
  const held = new Set((L.titles || []).map((t) => t.kind));
  const pool = age < 5 ? ["family", "home", "play"] : age < 18 ? ["school", "friends", "play", "family"] :
    [held.has("career") ? "work" : "home", held.has("children") ? "children" : "friends", held.has("partner") ? "partner" : "leisure",
      held.has("faith") ? "faith" : held.has("community") ? "community" : "nature", age >= 66 && !held.has("career") ? "leisure" : "home"];
  const k = pool[Math.floor(age) % pool.length];
  return PICS.domain[k] || PICS.tier.everyday || "";
}
function ilStart(L) {
  const P = IL_PACE[ilPace] || IL_PACE.slow;
  Object.assign(IL, { on: true, frames: [], lines: [], seen: new Set(), shown: 0, t0: performance.now(), last: 0, ended: false, tEnd: 0, k: 0, kt: performance.now(),
    picAge: -1, drawn: 0, base: spOf(L, { id: "il", labels: true }), L });
  // v22 next look: no second wheel. Where the crest is in view its own wheel moves week by week; on narrow screens (the
  // crest is in a drawer) the interlude keeps a small wheel of its own. The season and the year run as a strip.
  IL.side = !$("hudWheel") || $("hudWheel").offsetParent === null || narrow() || window.innerWidth <= 1040;   // one wheel on screen: the crest's when it shows
  IL.hbase = IL.side ? null : spOf(L, { id: "hw", hits: true });
  hudEl.classList.toggle("ilon", !IL.side);
  IL.frames.push(hudLast || { t: Math.round(L.age * 52), w: L.w, want: L.w.map((v, i) => Math.max(0.01, v + L.demand[i])) });
  interEl.innerHTML = `<div class="ilcard">
    <div class="ilpic" id="ilPic"></div>
    <div class="ilmain"><div class="ilkick">${ic("ci-cup")} Everyday life <span class="ilage" id="ilAge"></span></div><div class="illines" id="ilLines"></div></div>
    ${IL.side ? `<div class="ilside"><svg class="wheel" id="ilWheel" viewBox="-6 -2 212 206" aria-hidden="true"></svg></div>` : ""}
    <div class="ilfoot"><div class="ilseason" aria-hidden="true">${[["winter", 9], ["spring", 13], ["summer", 13], ["autumn", 13], ["winter", 4]].map(([s, w], i) => `<span class="sb ${s}" style="flex:${w}">${i === 4 ? "" : `${ic(SEASON_ICON[s])}<em>${cap(s)}</em>`}</span>`).join("")}<i class="ilmark" id="ilMark"></i><b class="ilprog" id="ilBar"></b></div><button class="ghost" id="ilSkip">${ic("step")} Skip</button></div></div>`;
  interEl.hidden = false; interEl.classList.remove("out");
  $("ilSkip").addEventListener("click", ilFinish);
  setTip($("ilSkip"), () => tipBox(`${ic("step")} Skip`, "", [], `Go straight to what comes next. The pace of these interludes is set under ${ic("hourglass")} (key i).`));
  void P; IL.raf = requestAnimationFrame(ilTick);
}
function ilFeed(h) {
  if (!IL.on || !h.life) return;
  for (const f of h.trace || []) IL.frames.push(frameOf(f));
  const r = h.routine;
  if (r && r.lines) for (const x of r.lines) if (!IL.seen.has(x)) { IL.seen.add(x); IL.lines.push({ text: x, age: r.age }); }
  IL.L = h.life;
  if (!h.busy && !IL.ended) {
    const P = IL_PACE[ilPace] || IL_PACE.slow, now = performance.now();
    IL.ended = true;
    IL.tEnd = Math.max(IL.t0 + clamp(IL.frames.length * P.wk, P.min, P.max), now + 900);
    IL.tEnd = Math.max(IL.tEnd, IL.t0 + Math.min(IL.lines.length, 4) * P.line + 600);
  }
}
function ilTick(now) {
  if (!IL.on) return;
  try { ilStep(now); } catch (e) { console.error(e); ilFinish(); }      // a fault in the telling never holds up the life
}
function ilStep(now) {
  const P = IL_PACE[ilPace] || IL_PACE.slow, N = IL.frames.length, dt = Math.max(0, now - IL.kt); IL.kt = Math.max(IL.kt, now);
  const rate = IL.ended ? Math.max(0, N - 1 - IL.k) / Math.max(60, IL.tEnd - now) : 1 / P.wk;
  IL.k = clamp(IL.k + rate * dt, 0, Math.max(0, N - 1));
  if (now - IL.drawn > 40 && N) {
    IL.drawn = now;
    const k = Math.floor(IL.k), f = IL.k - k, A = IL.frames[k], B = IL.frames[Math.min(N - 1, k + 1)];
    const lerp = (a, b) => a.map((v, i) => v + (b[i] - v) * f);
    const svg = IL.side ? $("ilWheel") : $("hudWheel");
    if (svg) svg.innerHTML = spiderSVG({ ...(IL.side ? IL.base : IL.hbase), ...bandsOf(f < 0.5 ? A : B), w: lerp(A.w, B.w), want: lerp(A.want, B.want) });
    const t = A.t + (B.t - A.t) * f, age = t / 52, wkn = ((t % 52) + 52) % 52;
    const mk = $("ilMark"); if (mk) mk.style.left = `${(wkn / 52 * 100).toFixed(2)}%`;
    const ag = $("ilAge"); if (ag) ag.innerHTML = `· age ${Math.floor(age)}, <span id="ilWk">week ${Math.floor(wkn) + 1}</span>`;   // #ilWk kept for the drivers
    if (Math.floor(age) !== IL.picAge) {
      IL.picAge = Math.floor(age);
      const src = ilPic(IL.L, age), box = $("ilPic");
      if (box && src && (!box.dataset.src || box.dataset.src !== src)) {
        box.dataset.src = src;
        const img = document.createElement("img"); img.alt = ""; img.src = src; img.decoding = "async"; img.onerror = () => img.remove();
        box.querySelectorAll("img").forEach((x) => { x.classList.add("gone"); setTimeout(() => x.remove(), 1400); });
        box.prepend(img);
      }
    }
    const bar = $("ilBar"); if (bar) bar.style.width = `${(IL.ended ? clamp((now - IL.t0) / Math.max(1, IL.tEnd - IL.t0)) : Math.min(0.9, (now - IL.t0) / (P.max * 1.4))) * 100}%`;
  }
  if (IL.shown < IL.lines.length && now - IL.last >= P.line) {
    IL.last = now;
    const box = $("ilLines");
    if (box) {
      const p = document.createElement("p"); p.innerHTML = rich(IL.lines[IL.shown].text); box.appendChild(p);
      const all = box.querySelectorAll("p:not(.gone)");
      if (all.length > 4) { all[0].classList.add("gone"); setTimeout(() => all[0].remove(), 900); }
    }
    IL.shown++;
  }
  if (IL.ended && now >= IL.tEnd) return ilFinish();
  IL.raf = requestAnimationFrame(ilTick);
}
function ilFinish() {
  if (!IL.on) return;
  IL.on = false; cancelAnimationFrame(IL.raf); hudEl.classList.remove("ilon");
  interEl.classList.add("out"); setTimeout(() => { if (!IL.on) { interEl.hidden = true; interEl.innerHTML = ""; } }, 500);
  hideTip();
  if (!hud) return;
  hudLast = null; hudFrames = [];
  if (hud.life && hud.life.w) renderHud(hud.life);
  renderTable(hud); renderTransport(); lockInputs(busy);
  if (stick.bottom) chronEl.scrollTop = chronEl.scrollHeight;
}
function ilWanted(h) {
  return busy && h.mode === "play" && h.job === "run" && !h.replay && ilPace !== "off" && !["w", "m"].includes(lastSent) && sentFrom !== "cp" && h.life && h.life.w && !IL.on;
}

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
function trustHTML(L) {                 // IDEAS.md, "Player intervention that helps": trust in the player, per color
  const T = L.trust || {}, P = L.pushes || {};
  if (!P.forced) return "";
  return `<h4>Trust in you</h4><div class="mts">${COLORS.map((c) => meterRow(`${pip(c)} ${CNAME[c]}`, (1 + (T[c] || 0)) / 2, sgn((T[c] || 0) * 100), `var(--c${c})`, "Built by your pushes in this color that they came to accept, lost by the ones they resented. Trust spares some of a push's resentment; distrust adds to it.")).join("")}</div>
    <p class="shnote">You pushed ${P.forced} time${P.forced === 1 ? "" : "s"}: ${P.accepted || 0} they came to accept, ${P.resented || 0} they resented.</p>`;
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
  const states = (L.states || []).map((x, i) => `<div class="sdef"><span class="st g${x.good}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span><span>${esc(stateDef(x))}${x.value != null ? ` Now ${esc(stateScale(x.var, x.scale, x.value))}.` : ""}</span></div>`).join("") || `<span class="empty">No marked state now</span>`;
  const stateChips = (L.states || []).map((x, i) => `<span class="st g${x.good}" data-st="${i}">${ic(x.icon)}${esc(cap(x.word))}</span>`).join("");
  const around = Object.entries(L.around || {}).map(([k, v]) => `<div class="sdef"><span class="chip" data-a="${esc(k)}">${esc(cap(k))}: <span class="w">${esc((L.around_words || {})[k] || "")} (${aroundPct(v)})</span></span><span>${esc(AROUND_DEF[k] || "")}</span></div>`).join("");
  const aroundShort = SH_AROUND_SHORT.filter(([k]) => (L.around || {})[k] != null).map(([k, w]) => `<div class="r" data-a="${esc(k)}"><span>${w}</span><b>${esc((L.around_words || {})[k] || "")}</b></div>`).join("");
  const titles = (L.titles || []).map((t) => `<div class="sdef"><span class="chip">${ic(KIND_ICON[t.kind])}${esc(cap(t.kind))}</span><span>${(t.named || []).map((x) => esc(cap(shortSay(x.say))) + (x.facets || []).map((f) => ", " + esc(shortSay(f.say))).join("")).join("; ") || ""} · ${yrsWord(t.years)} · invested ${investWord(t.invested)} · expects ${pips(lettersOf(t.expects))}${t.clash ? ` · ${ic("bolt")} in a clash` : ""}</span></div>`).join("") || `<span class="empty">No titles yet</span>`;
  const roles = (L.statuses || []).map((d, i) => `<span class="perk stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`).concat((L.perks || []).map((d, i) => `<span class="perk${d.state && d.state !== "held" ? " " + d.state : ""}" data-perk="${i}" style="--pc:${d.ways ? `var(--c${d.ways[0]})` : "var(--gold)"}">${ic(roleIconOf(d))}${esc(cap(d.name))}</span>`)).join("");
  const heldChips = (L.titles || []).map((t, i) => { const n = (t.named || [])[0]; return `<span class="chip shtl" data-ti="${i}">${ic(KIND_ICON[t.kind] || "anchor")}${esc(n ? cap(shortSay(n.say)) : cap(t.kind))}</span>`; })
    .concat((L.statuses || []).map((d, i) => `<span class="chip shtl stat" data-rs="${i}">${ic(roleIconOf(d))}${esc(cap(shortSay(d.say)))}</span>`)).join("");
  const goals = (L.goals || []).map((g) => goalRow(g)).join("") || `<span class="empty">No dreams yet</span>`;
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
      ${panel("portrait", `<div class="shsec sa-b"><h4>Portrait</h4><p class="shport">${shPortrait(L)}</p>${temperWords ? `<h4>Temperament</h4><div class="shtraits">${temperWords}</div>` : ""}${needWords ? `<h4>Needs met</h4><div class="shtraits">${needWords}</div>` : ""}</div>
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
  sheetEl.querySelectorAll("[data-st]").forEach((el) => { const x = (L.states || [])[+el.dataset.st]; if (x && x.reads) setTip(el, () => stateTip(x)); });
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

/* ---------------- the Book of Moments (points 11 and 15; Emren chose "Book and peace", 21:44): what every life met, kept in
   this browser across lives. It records; it does not rank. Rarity: the share of simulated modern Earth lives that meet a
   moment (rarity.py), until the engine and the Library tag real-life frequencies. ---------------- */
const BOOK_KEY = "chroma.book", CAT_KEY = "chroma.bookcat", BOOK_LIVES = 80;
const emptyBook = () => ({ v: 1, lives: {}, order: [], seen: {} });
let book = (() => { try { const b = JSON.parse(localStorage.getItem(BOOK_KEY) || "null"); if (b && b.v === 1 && b.seen && b.lives) return b; } catch (_) {} return emptyBook(); })();
let bookCat = (() => { try { return JSON.parse(localStorage.getItem(CAT_KEY) || "{}") || {}; } catch (_) { return {}; } })();
const catMaps = {};
function storeBook() { try { localStorage.setItem(BOOK_KEY, JSON.stringify(book)); } catch (_) {} }
function takeCat(c) { bookCat[c.world] = c; delete catMaps[c.world]; try { localStorage.setItem(CAT_KEY, JSON.stringify(bookCat)); } catch (_) {} }
const worldOf = (setting) => setting === "earth" ? "earth" : "base";
function catMap(world) {
  if (catMaps[world]) return catMaps[world];
  const c = bookCat[world]; if (!c) return null;
  const m = {};
  for (const [k, dom, tier, sh] of c.moments) m[k] = { name: k.slice(2), dom, tier, sh };
  for (const [n, sh] of c.deeds) m["d|" + n] = { name: n, sh };
  for (const [n, say, kind, sh] of c.titles) m["t|" + n] = { name: say, kind, sh };
  return (catMaps[world] = m);
}
function bookInfo(k) { for (const w of ["earth", "base"]) { const m = catMap(w); if (m && m[k]) return m[k]; } return null; }
// one life's record from the game: merged by its id, so a replayed or reloaded life never counts twice
function bookMerge(r) {
  if (!r || !r.id) return;
  const keys = [...(r.moments || []), ...(r.deeds || []).map((x) => "d|" + x), ...(r.titles || []).map((x) => "t|" + x),
    ...(r.idents || []).map((x) => "i|" + x), ...(r.long || []).map((x) => "l|" + x), "w|" + r.setting];
  let L = book.lives[r.id];
  if (!L) { L = book.lives[r.id] = { k: [], when: Date.now() }; book.order.push(r.id); }
  const had = new Set(L.k || []);
  for (const k of keys) if (!had.has(k)) { had.add(k); const s = book.seen[k] || (book.seen[k] = { n: 0, first: r.id }); s.n++; }
  Object.assign(L, { name: r.name, setting: r.setting, start: r.start, age: r.age, over: !!r.over, k: [...had] });
  if (r.final !== undefined) L.final = r.final;
  if (r.reading) L.reading = r.reading.words;
  for (const id of book.order.slice(0, Math.max(0, book.order.length - BOOK_LIVES))) if (book.lives[id]) delete book.lives[id].k;   // counts stay
  storeBook();
}
const firstHere = (id) => Object.entries(book.seen).filter(([, s]) => s.first === id).map(([k]) => k);
function rareWord(sh) {
  if (sh == null) return "";
  if (sh === 0) return `not met in ${((bookCat.earth || {}).lives || 0).toLocaleString()} simulated lives`;
  return sh >= 0.5 ? "most lives meet it" : sh >= 0.2 ? "many lives meet it" : `about 1 life in ${Math.round(1 / sh)}`;
}
const isRare = (sh) => sh != null && sh < 0.1;
const STAR_DEEDS = new Set(["came out", "named their gender"]);   // N1d §5: rare moments of a life, starred like the others
const isStar = (k, i) => (k.startsWith("d|") ? STAR_DEEDS.has(k.slice(2)) : false) || !!(i && isRare(i.sh));
const momentName = (k) => cap(k.slice(2));
const bookDef = { moments: "A moment counts once a life meets it: a situation the story tells, or a life event.",
  rare: "Moments that fewer than 1 in 10 simulated modern Earth lives meet, from birth to 80, across the four Earth starts.",
  deeds: "Things a life did at least once, as the engine marks them: kept a word, made an enemy, came home.",
  titles: "Every title or status a life has held, even for a week.",
  long: "A title reached for when it works for fewer than 1 in 10 people. Made or missed, each is kept: the trying is part of the life.", idents: "The 31 combinations of colors a life can be, under Chroma's own names. A life is one while its colors stay above 22%." };
const bookEl = document.createElement("div"); bookEl.className = "help sheetwrap"; bookEl.hidden = true; document.body.appendChild(bookEl);
bookEl.addEventListener("click", (e) => { if (e.target === bookEl) closeBook(); });
function closeBook() { bookEl.hidden = true; bookEl.innerHTML = ""; hideTip(); }
function openBook() {
  hideTip(); closeHud(); closeSheet();
  const S = book.seen, has = (k) => !!(S[k] && S[k].n);
  const lives = book.order.map((id) => [id, book.lives[id]]).filter(([, L]) => L);
  const E_ = catMap("earth"), B_ = catMap("base");
  const count = (m, pre) => m ? Object.keys(m).filter((k) => pre.includes(k[0] + "|")) : [];
  const eMom = count(E_, ["s|", "e|"]), bMom = count(B_, ["s|", "e|"]).filter((k) => !E_ || !E_[k]);
  const deeds = [...new Set([...count(E_, ["d|"]), ...count(B_, ["d|"])])], titles = count(E_, ["t|"]);
  const ID_ = ((bookCat.earth || bookCat.base || {}).idents) || {}, idents = Object.entries(ID_).map(([l, v]) => [l, v[0]]);
  const met = (ks) => ks.filter(has).length;
  // G3 (B package): one count of moments. The Book's count is the situations the story tells plus the life events, and
  // says so, so it agrees with the situation count elsewhere (822 situations and 59 life events: 881 moments)
  const momDef = (ks) => { const s_ = ks.filter((k) => k.startsWith("s|")).length; return `${bookDef.moments} Here: ${s_} situations and ${ks.length - s_} life events.`; };
  const stat = (n, of, label, def) => `<div class="bst" data-def="${esc(def || "")}"><b>${n}</b>${of != null ? `<span class="of">of ${of}</span>` : ""}<span class="bl">${label}</span></div>`;
  // rare moments met, rarest first
  const rare = Object.keys(S).filter((k) => /^[sed]\|/.test(k) && S[k].n).map((k) => [k, bookInfo(k)]).filter(([k, i]) => i && (k.startsWith("d|") ? STAR_DEEDS.has(k.slice(2)) : isRare(i.sh))).sort((a, b) => (a[1].sh ?? 1) - (b[1].sh ?? 1));
  const rareRows = rare.slice(0, 40).map(([k, i]) => { const f = book.lives[S[k].first]; return `<div class="brow"><span class="bn">${ic("star")} ${esc(momentName(k))}</span><span class="muted">${esc(rareWord(i.sh))}${f ? ` · first: ${esc(f.name)}` : ""}</span></div>`; }).join("")
    + (rare.length > 40 ? `<div class="muted">and ${rare.length - 40} more</div>` : "");
  const unmetRare = eMom.filter((k) => !has(k) && isRare(E_[k].sh)).length;
  const longK = Object.keys(S).filter((k) => k.startsWith("l|") && S[k].n).sort((a, b) => S[b].n - S[a].n);
  const longRows = longK.slice(0, 20).map((k) => { const [, how, nm] = k.split("|"), i = bookInfo("t|" + nm), f = book.lives[S[k].first];
    return `<div class="brow"><span class="bn">${ic("star")} ${how === "made" ? "Made it" : "Missed"}: ${esc(shortSay((i && i.name) || nm))}</span><span class="muted">${S[k].n === 1 ? "once" : S[k].n + " lives"}${f ? ` · first: ${esc(f.name)}` : ""}</span></div>`; }).join("");
  // moments by part of life (modern Earth)
  const doms = {};
  for (const k of eMom) { const d = E_[k].dom || "life"; (doms[d] = doms[d] || [0, 0])[1]++; if (has(k)) doms[d][0]++; }
  const big = Object.entries(doms).filter(([, v]) => v[1] >= 6).sort((a, b) => b[1][1] - a[1][1]), small = Object.entries(doms).filter(([, v]) => v[1] < 6);
  if (small.length) big.push(["other", small.reduce((t, [, v]) => [t[0] + v[0], t[1] + v[1]], [0, 0]), small.map(([d]) => d)]);
  const domRows = big.map(([d, [a, n], parts]) => meterRow(esc(cap(d)), a / n, `${a} of ${n}`, "var(--gold)", parts ? "Smaller parts of life together: " + parts.join(", ") + "." : "")).join("");
  const identGrid = idents.map(([l, nm]) => `<span class="bid${has("i|" + l) ? " on" : ""}" data-l="${l}">${pips(lettersOf(l))}<span>${esc(nm)}</span>${has("i|" + l) ? `<span class="bn2">${S["i|" + l].n}</span>` : ""}</span>`).join("");
  const deedChips = deeds.map((k) => `<span class="chip bdeed${has(k) ? " on" : ""}">${STAR_DEEDS.has(k.slice(2)) ? ic("star") : ""}${esc(cap(k.slice(2)))}${has(k) ? ` <b>${S[k].n}</b>` : ""}</span>`).join("");
  const heldT = titles.filter(has).map((k) => E_[k]).sort((a, b) => (a.sh ?? 1) - (b.sh ?? 1));
  const titleChips = heldT.map((i) => `<span class="chip${isRare(i.sh) ? " rare" : ""}" data-tip="${esc(cap(i.kind || "") + (i.sh != null ? " · " + rareWord(i.sh) : ""))}">${isRare(i.sh) ? ic("star") : ""}${esc(cap(shortSay(i.name)))}</span>`).join("") || `<span class="empty">None yet</span>`;
  const lifeRows = lives.slice().reverse().slice(0, 30).map(([id, L]) => { const nw = firstHere(id).filter((k) => /^[se]\|/.test(k)).length;
    const fin = L.final != null ? (((bookCat[worldOf(L.setting)] || {}).idents || {})[L.final] || ["Still forming"])[0] : "";
    return `<div class="brow blife"><span class="bn"><b>${esc(L.name || "")}</b><span class="muted">${esc(SETTING_NAME[L.setting] || "")} · ${Math.floor(L.start || 0)} to ${Math.floor(L.age || 0)}${L.over ? "" : ", living"}${fin ? " · " + esc(fin) : ""}</span></span>${L.reading ? `<span class="rd">${esc(L.reading)}</span>` : ""}${nw ? `<span class="muted">${nw} moment${nw === 1 ? "" : "s"} first met in this life</span>` : ""}</div>`; }).join("");
  const worlds = ["earth", "tribal", "magic"].map((w) => `<span class="chip${has("w|" + w) ? " on" : " off"}">${ic(SETTING_ICON[w] || "globe")}${esc(SETTING_NAME[w] || w)}${has("w|" + w) ? ` <b>${S["w|" + w].n}</b>` : ""}</span>`).join("");
  bookEl.hidden = false;
  bookEl.innerHTML = `<div class="box paper sheet bookp" role="dialog" aria-label="The Book of Moments">
    <div class="shh"><div class="bhd">${ic("ci-bookshelf")}<div><div class="shn">The Book of Moments</div><div class="muted">${lives.length ? `What ${lives.length === 1 ? "one life has" : lives.length + " lives have"} met, kept in this browser.` : "What your lives meet is kept here, in this browser."} It records; it does not rank.</div></div></div>
      <button class="ghost" id="bkClose" aria-label="Close">${ic("x")}</button></div>
    ${lives.length ? `<div class="bstats">${stat(lives.length, null, lives.length === 1 ? "life" : "lives")}${stat(met(eMom), eMom.length, "moments, modern Earth", momDef(eMom))}${bMom.length ? stat(met(bMom), bMom.length, "moments, tribal and magic", momDef(bMom)) : ""}${stat(rare.length, rare.length + unmetRare, "rare moments", bookDef.rare)}${longK.length ? stat(longK.length, null, "long shots", bookDef.long) : ""}${stat(met(deeds), deeds.length, "deeds", bookDef.deeds)}${titles.length ? stat(met(titles), titles.length, "titles", bookDef.titles) : ""}${stat(met(idents.map(([l]) => "i|" + l)), idents.length, "identities", bookDef.idents)}</div>
    <div class="shg">
      <section><h4>Rare moments met</h4>${rareRows || `<span class="empty">None yet. ${unmetRare} wait somewhere in a life.</span>`}<h4>Long shots</h4>${longRows || `<span class="empty">None yet. Any title can be reached for against long odds; a miss is kept here too.</span>`}<h4>Lives</h4>${lifeRows}<h4>Worlds</h4><div class="perks">${worlds}</div></section>
      <section><h4>Identities lived</h4><div class="bids">${identGrid}</div><h4>Deeds</h4><div class="perks">${deedChips}</div></section>
      <section><h4>Moments by part of life</h4><div class="mts">${domRows}</div><h4>Titles held</h4><div class="perks">${titleChips}</div></section>
    </div>` : `<p class="bempty">Nothing yet. Every life you play writes into this book: the moments it meets, the people it becomes, the titles it holds. Rare moments are marked with a star.</p>`}</div>`;
  bookEl.querySelectorAll("[data-def]").forEach((el) => { if (el.dataset.def) setTip(el, () => tipBox(esc(el.querySelector(".bl").textContent), "", [], esc(el.dataset.def))); });
  bookEl.querySelectorAll("[data-tip]").forEach((el) => setTip(el, () => tipBox(esc(el.textContent), "", [], esc(el.dataset.tip))));
  bookEl.querySelectorAll(".bid").forEach((el) => setTip(el, () => { const l = el.dataset.l, s = S["i|" + l]; return tipBox(`${pips(lettersOf(l))} ${esc(el.textContent.replace(/\d+$/, ""))}`, esc((ID_[l] || [])[1] || ""), s ? [["Lives", String(s.n)], ["First", esc((book.lives[s.first] || {}).name || "")]] : [], s ? "" : "No life has been this yet."); }));
  $("bkClose").addEventListener("click", closeBook);
}

/* ---------------- point 9: save a life to a file, load it back, and keep the last one in this browser ---------------- */
let saveWait = null;
const fileIn = document.createElement("input"); fileIn.type = "file"; fileIn.accept = ".json,application/json"; fileIn.hidden = true; document.body.appendChild(fileIn);
fileIn.addEventListener("change", async () => { const f = fileIn.files && fileIn.files[0]; fileIn.value = ""; if (!f) return; try { loadText(await f.text()); } catch (e) { toast("Could not read that file."); } });
function askSave() {
  return new Promise((res) => { if (!worker || !ready) return res(null); saveWait = res; worker.postMessage({ cmd: "save" }); setTimeout(() => { if (saveWait === res) { saveWait = null; res(null); } }, 8000); });
}
function autosave(data) { try { if (data) localStorage.setItem("chroma.autosave", data); } catch (_) {} }
// Worlds a finished life left behind (release row W41: fresh or earlier world), kept in this browser's IndexedDB, the
// newest three; the newest one's key, name and age also in localStorage for the setup step
const WDB = {
  db: null,
  open() { if (!this.db) this.db = new Promise((res) => { try { const r = indexedDB.open("chroma", 1); r.onupgradeneeded = () => r.result.createObjectStore("worlds"); r.onsuccess = () => res(r.result); r.onerror = () => res(null); } catch (_) { res(null); } }); return this.db; },
  async op(mode, f) { const db = await this.open(); if (!db) return null; return new Promise((res) => { try { const tx = db.transaction("worlds", mode), q = f(tx.objectStore("worlds")); tx.oncomplete = () => res(q ? q.result : true); tx.onerror = tx.onabort = () => res(null); } catch (_) { res(null); } }); },
  get(k) { return this.op("readonly", (st) => st.get(k)); },
  put(k, v) { return this.op("readwrite", (st) => st.put(v, k)); },
  del(k) { return this.op("readwrite", (st) => st.delete(k)); },
};
const worldMeta = () => { try { const m = JSON.parse(localStorage.getItem("chroma.world.last") || "null"); return m && m.key ? m : null; } catch (_) { return null; } };
async function keepWorld(data) {
  if (!data) return;
  let d = null; try { d = JSON.parse(data); } catch (_) { return; }
  if (!d || !d.key || !(await WDB.put(d.key, data))) return;
  let keys = []; try { keys = JSON.parse(localStorage.getItem("chroma.world.keys") || "[]"); } catch (_) {}
  keys = keys.filter((k) => k !== d.key).concat([d.key]);
  while (keys.length > 3) await WDB.del(keys.shift());
  const meta = { key: d.key, name: d.name, age: d.age };
  try { localStorage.setItem("chroma.world.keys", JSON.stringify(keys)); localStorage.setItem("chroma.world.last", JSON.stringify(meta)); } catch (_) {}
  if (worker && ready) worker.postMessage({ cmd: "world_in", text: JSON.stringify(meta) });
}
// the world a saved life began in, handed to the engine before it is replayed (false: not in this browser)
async function worldFor(d) {
  const e = d && d.setup && d.setup.earlier;
  if (!e || !e.key) return true;
  let text = typeof d.world_data === "string" ? d.world_data : null;
  if (text) await WDB.put(e.key, text); else text = await WDB.get(e.key);
  if (!text) return false;
  worker.postMessage({ cmd: "world_in", text });
  return true;
}
// Emren 10-07 01:57 (N6): autosave after each action into one slot, overwritten each time; on unless turned off (key a)
let autoOn = true; try { autoOn = localStorage.getItem("chroma.autosave.on") !== "off"; } catch (_) {}
function autoSaveNow() {
  askSave().then((d) => {
    if (!d) return; autosave(d);
    const b = $("savedNote"); if (!b) return;
    b.classList.remove("flash"); void b.offsetWidth; b.classList.add("flash");
  });
}
function savedLife() { try { const s = localStorage.getItem("chroma.autosave"); const d = s && JSON.parse(s); return d && d.game === "chroma" ? { text: s, name: d.name, age: d.age } : null; } catch (_) { return null; } }
async function saveToFile() {
  let data = await askSave(); if (!data) { toast("Nothing to save yet."); return false; }
  autosave(data);
  const d = JSON.parse(data), fn = `chroma-${String(d.name || "life").replace(/[^A-Za-z0-9-]+/g, "-")}-age-${Math.floor(d.age || 0)}.json`;
  if (d.setup && d.setup.earlier && d.setup.earlier.key) { const w = await WDB.get(d.setup.earlier.key); if (w) { d.world_data = w; data = JSON.stringify(d); } }
  let dl = null;
  try { dl = window.claude && window.claude.use ? await window.claude.use("downloads") : null; } catch (_) { dl = null; }
  if (dl) {
    try { await dl.save({ filename: fn, data }); toast(`Saved ${fn}`); return true; }
    catch (e) { if (e && e.code === "declined") { toast("Not saved."); return false; } }
  }
  showSaveText(fn, data);
  return true;
}
function showSaveText(fn, data) {
  helpEl.hidden = false;
  helpEl.innerHTML = `<div class="box paper savebox"><h2>${ic("ci-sealed-scroll")} Save this life</h2><p class="muted">This viewer cannot hand you a file, so here is the save itself. Copy it into a text file named <b>${esc(fn)}</b>; Load takes that file back.</p>
    <textarea class="field" id="saveText" readonly rows="6">${esc(data)}</textarea><div class="center" style="margin-top:10px;display:flex;gap:8px;justify-content:center"><button class="primary" id="saveCopy">${ic("check")} Copy</button><button class="ghost" id="helpClose">${ic("x")} Close</button></div></div>`;
  $("helpClose").addEventListener("click", closeHelp);
  $("saveCopy").addEventListener("click", () => { const t = $("saveText"); try { navigator.clipboard.writeText(t.value).then(() => toast("Copied"), () => { t.select(); }); } catch (_) { t.select(); } });
}
async function loadText(text) {
  let d = null; try { d = JSON.parse(text); } catch (_) {}
  if (!d || d.game !== "chroma") { toast("That is not a Chroma save."); return; }
  if (!(await worldFor(d))) { toast("This life began in an earlier world that is no longer in this browser. Load it from its saved file."); return; }
  if (d.world_data) { delete d.world_data; text = JSON.stringify(d); }
  if (busy) pause();
  closeHelp(); closeSheet(); if (IL.on) ilFinish();
  resetChron(); reviewEl.hidden = true; lastCpKey = "";
  worker.postMessage({ cmd: "load", text });
}
function askNewLife() {
  const L = hud && hud.life;
  if (!L || hud.mode !== "play") { send("n"); return; }
  hideTip(); helpEl.hidden = false;
  helpEl.innerHTML = `<div class="box paper"><h2>${ic("new")} A new life</h2><p>Keep ${esc(L.name)}'s life before you leave it? A saved life can be loaded again from its file, from the moment you left.</p>
    <div class="center" style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:12px"><button class="primary" id="nlSave">${ic("ci-sealed-scroll")} Save, then a new life</button><button class="ghost" id="nlGo">${ic("new")} New life without saving</button><button class="ghost" id="helpClose">${ic("x")} Stay</button></div></div>`;
  $("helpClose").addEventListener("click", closeHelp);
  $("nlGo").addEventListener("click", () => { closeHelp(); send("n"); });
  $("nlSave").addEventListener("click", async () => { closeHelp(); const ok = await saveToFile(); if (ok && helpEl.hidden) send("n"); else if (ok) { const go = document.createElement("button"); go.className = "primary"; go.innerHTML = `${ic("new")} Now a new life`; go.addEventListener("click", () => { closeHelp(); send("n"); }); helpEl.querySelector(".center").prepend(go); } });
}
function renderReplay(h) {
  let el = $("replayBox");
  if (!h.replay) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement("div"); el.id = "replayBox"; el.className = "replaying"; stageEl.appendChild(el); }
  const r = h.replay, f = r.n ? r.i / r.n : 1;
  el.innerHTML = `<div class="box"><div class="ilkick">${ic("ci-sealed-scroll")} Bringing a life back</div><h2>${esc(r.name || "")}</h2><p class="muted">Living it again from the start, choice by choice, up to age ${Math.floor(r.age || 0)}.</p><span class="ilbar"><i style="width:${(f * 100).toFixed(0)}%"></i></span></div>`;
}

/* ---------------- point 10 (Emren chose tarot cards): the life-choice cards on the start screen ---------------- */
const ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];
// the plates are the visuals thread's (chroma-art/game/pics/tarot-1..7.webp); Build your own opens the deck as 0, like the Fool
const TAROT_NAME = { 1: "The Cradle", 2: "The Village", 3: "The Library", 4: "The Streets", 5: "The River", 6: "The Spires" };
const TAROT_PIC = { 1: ["situation", "a child is born"], 2: ["domain", "faith"], 3: ["domain", "study"], 4: ["domain", "money"], 5: ["domain", "nature"], 6: ["domain", "mind"] };
const tarotPic = (k) => (PICS.tarot && PICS.tarot[k]) || (TAROT_PIC[k] && PICS[TAROT_PIC[k][0]][TAROT_PIC[k][1]]) || "";
const tarotName = (p) => p.setting === "custom" ? "The Crossroads" : TAROT_NAME[p.k] || p.title;
const tarotNum = (p) => p.setting === "custom" ? "0" : ROMAN[+p.k] || p.k;
let tarotSel = null, nameDraft = "", pendingName = null, lastMenu = [], setupAge = null;
// The last setup step sent (game thread, 10-07): the world is built and the years before the player are lived before the
// first state comes back (half a minute or more for an adult start), so the box says so at once instead of standing still.
function startingHTML() {
  const p = lastMenu.find((x) => x.k === tarotSel), age = p && p.age != null ? p.age : setupAge;
  return `<div class="starting" role="status"><span class="spin"></span><span>${age > 0 ? `Their world takes shape, and the years before you join them, to ${Math.round(age)}, are lived` : "Their world takes shape"}<span class="dots"><i>.</i><i>.</i><i>.</i></span></span></div>`;
}
function showStarting() {
  const box = screenEl.querySelector(".setup"); if (!box || box.querySelector(".starting")) return;
  box.querySelectorAll("button, input").forEach((x) => { x.disabled = true; });
  box.querySelectorAll(".choices, .colorpick, .inrow").forEach((x) => { x.hidden = true; });   // the answered step's controls give way to the note
  box.insertAdjacentHTML("beforeend", startingHTML());
}
function tarotCard(p, i) {
  const cs = p.colors || [], src = tarotPic(p.k);
  return `<button class="tarot${p.setting === "custom" ? " zero" : ""}${tarotSel === p.k ? " sel" : ""}" data-k="${p.k}" style="--n:${i};--art:${cs.length ? artBG(cs) : "radial-gradient(circle at 50% 60%, #8a7fc0, #1a1530)"}" aria-label="${esc(tarotName(p) + ": " + p.title)}">
    <span class="tn">${tarotNum(p)}</span>
    <span class="tp">${src ? `<img src="${esc(src)}" alt="" decoding="async" onerror="this.remove()">` : `<span class="tg">${ic(SETTING_ICON[p.setting] || "sliders")}</span>`}</span>
    <span class="tt">${esc(tarotName(p))}</span>${cs.length ? `<span class="tc">${pips(cs)}</span>` : ""}</button>`;
}
// v22 next look: the life is set up on the reading itself. The card's story on the left, the name and Begin on the right;
// a preset then starts at once (the engine's name step is answered with the name typed here), Build your own goes on to
// its steps with the name already given. Clicking a chosen card again reads it, it does not begin; a double click or the
// card's number still begins at once.
function readingText(p) {
  if (!p) return `<div class="rk">${ic("ci-crystal-ball")} The reading</div><p class="rhint">Choose a card to read where this life begins.</p>`;
  const cs = p.colors || [];
  return `<div class="rk">${tarotNum(p)} · ${esc(tarotName(p))}</div><h2>${esc(p.title.replace(/ \((tribal|a world of magic)\)$/, ""))}</h2><p>${esc(p.blurb)}</p>
    <dl><dt>World</dt><dd>${ic(SETTING_ICON[p.setting] || "globe")} ${esc(SETTING_NAME[p.setting] || "Your own, step by step")}</dd>
    <dt>You take over</dt><dd>${p.age === null ? "when you choose" : p.age === 0 ? "at birth" : "at " + p.age}</dd>
    ${cs.length ? `<dt>Raised toward</dt><dd>${pips(cs)} ${cs.map((c) => CNAME[c]).join(" and ")}</dd>` : ""}</dl>`;
}
const goWord = (p) => p && p.setting === "custom" ? "Build this life" : "Begin this life";
function beginLife(k, name) {
  pendingName = name == null ? null : String(name).trim();
  const r = $("readGo"); if (r) r.innerHTML = `<span class="spin"></span><span>Setting out…</span>`;
  send(k);
}
let bootMenu = null; try { bootMenu = JSON.parse(localStorage.getItem("chroma.menu") || "null"); } catch (_) {}
function renderScreen(h) {
  if (h.mode === "menu") {
    const booting = !!h.booting, sv = booting ? null : savedLife(), sel = h.menu.find((p) => p.k === tarotSel) || null;
    if (!booting) { lastMenu = h.menu; setupAge = null; try { localStorage.setItem("chroma.menu", JSON.stringify(h.menu)); } catch (_) {} }
    const hadFocus = document.activeElement && document.activeElement.id === "txt";
    screenEl.innerHTML = `<div class="hero"><h1>CHROMA</h1><div class="pips">${COLORS.map((c) => pip(c)).join("")}</div><p>One life. Five colors. You are the voice in their head.</p></div>
      <div class="spread"><div class="tarots${sel ? " picked" : ""}">${h.menu.slice().sort((a, b) => (b.setting === "custom") - (a.setting === "custom")).map(tarotCard).join("")}</div>
      <div id="reading" class="reading paper${sel ? " has" : " empty"}"><div class="rtext" id="readText">${readingText(sel)}</div>${sel ? `<div class="rgo" id="readGo"></div>` : ""}</div></div>
      ${booting ? `<div class="bootline"><span class="spin"></span><span id="bootMsg">Setting the table: loading Python and numpy in your browser…</span></div>` : ""}
      <div class="menufoot">${sv ? `<button class="primary" id="mContinue">${ic("play")} Continue ${esc(sv.name || "")}, at ${Math.floor(sv.age || 0)}</button>` : ""}${booting ? "" : `<button class="ghost" id="mLoad">${ic("ci-open-chest")} Load a life from a file</button>`}${!booting && book.order.length ? `<button class="ghost" id="mBook">${ic("ci-bookshelf")} The Book of Moments</button>` : ""}</div>`;
    const goRow = (p) => {
      let g = $("readGo");
      if (!g) { g = document.createElement("div"); g.className = "rgo"; g.id = "readGo"; $("reading").appendChild(g); }
      if (!$("txt")) {
        g.innerHTML = `<label class="nmrow"><span>Their name</span><input class="field" id="txt" type="text" maxlength="24" autocomplete="off" spellcheck="false" placeholder="a name, or leave empty" aria-label="Their name"></label>
          <button class="primary" id="go"${booting ? " disabled" : ""}>${ic("play")} <span id="goWord"></span></button>${booting ? `<small class="muted">The table is being set…</small>` : ""}`;
        const txt = $("txt"); txt.value = nameDraft;
        txt.addEventListener("input", () => { nameDraft = txt.value; });
        txt.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); $("go").click(); } });
        $("go").addEventListener("click", () => { if (!booting && tarotSel) beginLife(tarotSel, $("txt").value); });
      }
      $("goWord").textContent = goWord(p);
    };
    const pick = (k, focus) => {
      tarotSel = k; const p = h.menu.find((x) => x.k === k);
      screenEl.querySelectorAll(".tarot").forEach((x) => x.classList.toggle("sel", x.dataset.k === k));
      screenEl.querySelector(".tarots").classList.add("picked");
      const rd = $("reading"); rd.classList.add("has"); rd.classList.remove("empty");
      $("readText").innerHTML = readingText(p); goRow(p);
      if (focus && !touchUI) $("txt").focus({ preventScroll: true });
    };
    screenEl.querySelectorAll(".tarot").forEach((b) => {
      b.addEventListener("click", () => { pick(b.dataset.k, true); $("reading").scrollIntoView({ behavior: "smooth", block: "nearest" }); });
      b.addEventListener("dblclick", () => { if (!booting) beginLife(b.dataset.k, nameDraft); });
      if (!touchUI) b.addEventListener("pointerenter", () => pick(b.dataset.k, false));
    });
    if (sel) { pick(sel.k, false); if (hadFocus) $("txt").focus({ preventScroll: true }); }
    if ($("mContinue")) $("mContinue").addEventListener("click", () => loadText(sv.text));
    if ($("mLoad")) $("mLoad").addEventListener("click", () => fileIn.click());
    if ($("mBook")) $("mBook").addEventListener("click", openBook);
    return;
  }
  // the name typed on the reading answers the engine's name step (a preset's, or the first of Build your own)
  if (pendingName != null && h.step && h.step.key === "name" && (h.mode === "name" || h.mode === "custom")) {
    const v = pendingName; pendingName = null;
    send(v);
    screenEl.innerHTML = `<div class="setup">${h.mode === "name" ? startingHTML() : `<div class="starting" role="status"><span class="spin"></span><span>A moment<span class="dots"><i>.</i><i>.</i><i>.</i></span></span></div>`}</div>`;
    return;
  }
  if (h.mode === "custom" || h.mode === "name") {
    const s = h.step, last = h.mode === "name" || s.i === s.n - 1;
    let body = "";
    if (s.kind === "choice") body = `<div class="choices">${s.choices.map(([v, t, d]) => `<button class="ch" data-v="${v}"><b>${esc(t)}</b>${d ? `<span>${esc(d)}</span>` : ""}</button>`).join("")}</div>`;
    else if (s.kind === "colors") body = `<div class="colorpick">${COLORS.map((c) => `<button class="cbtn" data-c="${c}" aria-pressed="false">${pip(c)}<span>${CNAME[c]}</span></button>`).join("")}</div><div class="inrow"><button class="primary" id="go">${ic("push")} Next</button></div>`;
    else if (s.kind === "number") body = `<div class="inrow"><input type="range" id="num" min="0" max="60" step="1" value="0" aria-label="age"><span class="rangev" id="numv">0</span></div><div class="inrow" style="margin-top:12px"><button class="primary" id="go">${ic("push")} Next</button></div>`;
    else body = `<div class="inrow"><input class="field" id="txt" type="text" maxlength="24" autocomplete="off" spellcheck="false" placeholder="${s.key === "name" ? "a name, or leave empty" : "leave empty for random"}"><button class="primary" id="go">${ic(h.mode === "name" ? "play" : "push")} ${h.mode === "name" ? "Begin" : "Next"}</button></div>`;
    screenEl.innerHTML = `<div class="setup">${s.n > 1 ? `<div class="steps">${Array.from({ length: s.n }, (_, i) => `<b class="${i <= s.i ? "on" : ""}"></b>`).join("")}</div>` : ""}
      <div class="ttl">${esc(s.title.replace(/ \((tribal|a world of magic)\)$/, ""))}${s.n > 1 ? ` · step ${s.i + 1} of ${s.n}` : ""}</div><h2>${esc(s.q)}${s.help ? ` <button class="ghost qhelp" id="stepHelp" aria-label="More about this step">?</button>` : ""}</h2>${s.hint ? `<p class="hint">${esc(s.hint)}</p>` : ""}${body}</div>`;
    if (s.help) setTip($("stepHelp"), () => tipBox(esc(s.q), "", [], esc(s.help)));
    screenEl.querySelectorAll(".ch").forEach((b) => b.addEventListener("click", async () => {
      if (s.key === "earlier" && b.dataset.v !== "1") {
        const m = worldMeta(), w = m && await WDB.get(m.key);
        if (!w) { toast("That world is no longer in this browser; a fresh one, then."); send("1"); return; }
        worker.postMessage({ cmd: "world_in", text: w });
      }
      send(b.dataset.v); if (last && busy) showStarting();
    }));
    screenEl.querySelectorAll(".cbtn").forEach((b) => b.addEventListener("click", () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true")));
    const num = $("num"); if (num) num.addEventListener("input", () => { $("numv").textContent = num.value; });
    const txt = $("txt"), go = $("go");
    if (go) go.addEventListener("click", () => {
      if (s.kind === "colors") send([...screenEl.querySelectorAll('.cbtn[aria-pressed="true"]')].map((b) => b.dataset.c).join(""));
      else if (s.kind === "number") { if (s.key === "start_age") setupAge = +num.value; send(num.value); }
      else send(txt.value.trim());
      if (last && busy) showStarting();
    });
    if (txt) { txt.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); go.click(); } }); setTimeout(() => txt.focus({ preventScroll: true }), 30); }
    return;
  }
  screenEl.innerHTML = "";
}

/* ---------------- the end of a life ---------------- */
function gauge(v, label, color, help) {
  const r = 31, C = 2 * Math.PI * r;
  return `<div class="gauge" data-help="${esc(help)}"><svg viewBox="0 0 78 78" aria-hidden="true"><circle class="bg" cx="39" cy="39" r="${r}"/><circle class="fg" cx="39" cy="39" r="${r}" stroke="${color}" stroke-dasharray="${(clamp(v) * C).toFixed(1)} ${C.toFixed(1)}"/><text x="39" y="40">${Math.round(v * 100)}</text></svg><span>${label}</span></div>`;
}
function pathHTML(path, labels) {
  const chip = (g, i) => `<span class="chip">${labels && labels[i] ? pips(lettersOf(labels[i])) : ""}${esc(g)}</span>`;
  const join = (xs, o) => xs.map((g, i) => chip(g, i + o)).join(`<span class="muted">›</span>`);
  if (path.length <= 12) return join(path, 0);
  return join(path.slice(0, 5), 0) + `<span class="muted">› … ${path.length - 11} more ›</span>` + join(path.slice(-6), path.length - 6);
}
// what this life added to the Book, under its review
function bookNews(r) {
  if (!r || !r.id) return "";
  const ks = firstHere(r.id), mom = ks.filter((k) => /^[se]\|/.test(k)), rare = mom.filter((k) => { const i = bookInfo(k); return i && isRare(i.sh); });
  const ids = ks.filter((k) => k[0] === "i"), tis = ks.filter((k) => k[0] === "t"), lss = ks.filter((k) => k[0] === "l");
  const bits = [mom.length ? `${mom.length} moment${mom.length === 1 ? "" : "s"}${rare.length ? ` (${rare.length} rare)` : ""}` : "", ids.length ? `${ids.length} identit${ids.length === 1 ? "y" : "ies"}` : "", tis.length ? `${tis.length} title${tis.length === 1 ? "" : "s"}` : "", lss.length ? `${lss.length} long shot${lss.length === 1 ? "" : "s"}` : ""].filter(Boolean);
  return bits.length ? `<div class="center bnew"><span>${ic("ci-bookshelf")} New to your Book: ${bits.join(", ")}.</span>${rare.length ? `<div class="muted">${rare.slice(0, 3).map((k) => `${ic("star")} ${esc(momentName(k))}`).join(" · ")}</div>` : ""}</div>` : "";
}
const odds100 = (p) => p == null ? "long odds" : Math.round(p * 100) >= 1 ? `${Math.round(p * 100)} in 100` : "fewer than 1 in 100";
const L_name = (h) => (h && h.life && h.life.name) || "They";
function renderReview(h) {
  const r = h && h.review;
  if (!h || h.mode !== "over" || !r) { reviewEl.hidden = true; reviewEl.innerHTML = ""; return; }
  if (!reviewEl.hidden) return;
  reviewEl.hidden = false;
  reviewEl.innerHTML = `<div class="mh" style="justify-content:center"><span class="kick">${ic("candle")} The end of a life</span></div>
    <p class="epi" data-i="review">${rich(r.epitaph)}</p>
    ${r.story ? `<p class="lifep">${esc(r.story)}</p>` : ""}
    <div class="peace"><div class="kick">${ic("ci-scales")} The peace reading</div><p class="pw">${esc((r.reading || {}).words || "")}</p>${(r.long_shots || []).slice(0, 3).map((x) => `<p class="pls${x.made ? " made" : ""}">${ic("star")} ${esc(x.words)}</p>`).join("")}${(r.long_shots || []).length > 3 ? `<p class="pls muted">and ${r.long_shots.length - 3} more long shots</p>` : ""}</div>
    <div class="gauges">${gauge(r.fulfilment, "Satisfaction", "var(--sat)", "Their satisfaction, averaged over every week from 18 on.")}${gauge(r.serenity, "Peace", "var(--peace)", "Their peace, averaged over every week from 18 on.")}${gauge(r.integrity, "True to self", "var(--gold)", "1 minus the average reluctance of the choices you pushed on them. Choices left to them count as fully their own.")}${r.gifts != null ? gauge(r.gifts, "Their gifts", "var(--want)", "At each moment, their skill in the ways the chosen act used, against their best skill; averaged over every choice.") : ""}</div>
    <div class="muted center pnote">How well they lived is satisfaction and peace. How much the life was their own is being true to themselves and using their gifts. It is a reading, not a score.</div>
    <div class="center"><div class="muted" style="margin-bottom:6px">Identities lived · ${r.paths}</div><div class="path">${pathHTML(r.path, r.path_labels)}</div></div>
    ${r.died ? `<div class="center died">${ic("candle")} ${esc(L_name(h))} died at ${Math.floor(r.died.age)}, ${esc(r.died.how)}.</div>` : ""}
    <div class="muted center">${r.own} moments left to them · ${r.forced} pushed by you · ended as ${esc(r.final)}</div>
    ${bookNews(h.book)}
    <div class="center rvb"><button class="ghost" id="rvBook">${ic("ci-bookshelf")} Open the Book</button><button class="primary" id="again">${ic("new")} A new life</button></div>`;
  $("rvBook").addEventListener("click", openBook);
  reviewEl.querySelectorAll(".gauge").forEach((g) => setTip(g, () => tipBox(g.querySelector("span").textContent, "", [], g.dataset.help)));
  $("again").addEventListener("click", () => send(""));
  autoKey = ""; try { localStorage.removeItem("chroma.autosave"); } catch (_) {}
  if (h.world && worker && ready) worker.postMessage({ cmd: "world_out" });
}

/* ---------------- transport ---------------- */
function renderTransport() {
  const h = hud;
  if (!h || !["play", "over"].includes(h.mode)) { transEl.innerHTML = ""; return; }
  const L = h.life || {};
  const atCp = !!h.cp && !busy, over = h.mode === "over", atRes = !h.cp && !!h.res && !busy;
  let main;
  if (IL.on && !busy) main = `<button class="primary" id="tSkip">${ic("step")} Skip</button>`;
  else if (busy) main = `<button class="primary" id="tPause">${ic("pause")} Pause</button>`;
  else if (over) main = `<button class="primary" id="tMain">${ic("new")} New life</button>`;
  else if (atCp) main = `<button class="primary" id="tMain">${ic("crown")} <span>Let ${esc(narrow() ? "them" : L.name || "them")} choose</span></button>`;
  else if (atRes) main = `<button class="primary" id="tMain">${ic("play")} Go on</button>`;
  else main = `<button class="primary" id="tMain">${ic("play")} Live on</button>`;
  const dis = busy || atCp || over ? "disabled" : "";
  if (IL.on && !busy) {
    transEl.innerHTML = `${main}<span class="pace" role="group" aria-label="Interlude pace">${["slow", "short", "off"].map((p) => `<button data-pace="${p}" aria-pressed="${ilPace === p}">${ic(p === "off" ? "x" : "hourglass")}${PACE_WORD[p]}</button>`).join("")}</span><span class="live"><span class="t">Everyday life goes by. Skip to go straight on.</span></span>`;
    $("tSkip").addEventListener("click", ilFinish);
    transEl.querySelectorAll("[data-pace]").forEach((b) => { b.addEventListener("click", () => { ilPace = b.dataset.pace; try { localStorage.setItem("chroma.pace", ilPace); } catch (_) {} if (ilPace === "off") ilFinish(); else renderTransport(); renderTools(hud); });
      setTip(b, () => tipBox(`${ic("hourglass")} Interlude: ${PACE_WORD[b.dataset.pace]}`, "", [], "How long the everyday life between two moments is shown. Key i cycles it.")); });
    return;
  }
  transEl.innerHTML = `${main}
    <span class="steps4" role="group" aria-label="Step forward">${[["w", "1w", "one week"], ["m", "1m", "one month"], ["y", "1y", "one year"], ["d", "10y", "ten years"]].map(([k, t, d]) => `<button data-key="${k}" data-d="${d}" ${dis}>${ic("step")}${t}</button>`).join("")}</span>
    <span class="live">${busy ? `<span class="spin"></span><span>Living… <span class="t">age</span> ${L.age != null ? L.age.toFixed(1) : ""}</span>` : atCp ? `<span>${ic("flag")} <span class="t">A moment is waiting: choose for them, or let them choose.</span></span>` : over ? "" : atRes ? `<span>${ic("rune")} <span class="t">What came of the choice. Go on when ready.</span></span>` : `<span class="t">Live on to the next moment, or step through time.</span>`}</span>`;
  const tm = $("tMain"); if (tm) tm.addEventListener("click", () => send(""));
  if (tm && atCp) { const own = h.cp.options.find((o) => o.own); setTip(tm, () => tipBox(`${ic("crown")} Their own choice`, own ? esc(cap(own.label)) : "", [], "They act as they lean, with no reluctance cost. Key Enter.")); }
  const tp = $("tPause"); if (tp) tp.addEventListener("click", pause);
  const tsk = $("tSkip"); if (tsk) tsk.addEventListener("click", ilFinish);
  transEl.querySelectorAll(".steps4 button").forEach((b) => { b.addEventListener("click", () => send(b.dataset.key)); setTip(b, () => tipBox(`${ic("step")} Step ${b.dataset.d}`, "", [], "Stops early at a moment. Keys w, m, y, d.")); });
}

/* ---------------- help ---------------- */
function openHelp() {
  hideTip();
  helpEl.hidden = false;
  helpEl.innerHTML = `<div class="box paper"><h2>Keys</h2><dl>
    <dt><kbd>Enter</kbd></dt><dd>Live on to the next moment; at a moment, let them choose</dd>
    <dt><kbd>1</kbd>…<kbd>11</kbd></dt><dd>Push them to that option</dd>
    <dt><kbd>w</kbd> <kbd>m</kbd> <kbd>y</kbd> <kbd>d</kbd></dt><dd>Step a week, a month, a year, ten years</dd>
    <dt><kbd>Esc</kbd></dt><dd>Pause while time runs</dd>
    <dt><kbd>f</kbd></dt><dd>How often moments stop for you</dd>
    <dt><kbd>v</kbd></dt><dd>How much of daily life the story tells</dd>
    <dt><kbd>l</kbd></dt><dd>Ledger: the numbers under the story</dd>
    <dt><kbd>p</kbd></dt><dd>Dreams and plans: make a plan for them, or drop one</dd>
    <dt><kbd>c</kbd></dt><dd>The character sheet: everything about them</dd>
    <dt><kbd>b</kbd></dt><dd>The Book of Moments: what all your lives have met</dd>
    <dt><kbd>g</kbd></dt><dd>The World panel: the times, government, economy, laws and the history of the world around them (modern Earth lives)</dd>
    <dt><kbd>i</kbd></dt><dd>The everyday interlude between moments: slow, short or off</dd>
    <dt><kbd>s</kbd> <kbd>o</kbd></dt><dd>Save this life to a file; load one</dd>
    <dt><kbd>a</kbd></dt><dd>Autosave after every choice into one slot in this browser, on or off (Continue on the start screen)</dd>
    <dt><kbd>n</kbd></dt><dd>A new life (you can save this one first)</dd>
    <dt><kbd>h</kbd></dt><dd>This help</dd></dl>
    <p class="muted" style="margin:12px 0 0">Before each choice, the inner voice says what the heart (${ic("heart")}) and the head (${ic("head")}) want; after it, a page shows what came of it and how the world works. Colored words in the story can be hovered (or tapped): people, acts, thoughts and values show what the engine did behind them. The line at the top is the whole life; the fog is the part not yet lived.</p>
    ${GI_DATA.credit ? `<p class="muted credits">Icons from <a href="${GI_DATA.credit.source}" target="_blank" rel="noopener">${esc(GI_DATA.credit.source.replace(/^https?:\/\//, ""))}</a> by ${esc((GI_DATA.credit.authors || []).join(", "))}, under <a href="${GI_DATA.credit.license_url}" target="_blank" rel="noopener">${esc(GI_DATA.credit.license)}</a>.</p>` : ""}
    <div class="center" style="margin-top:12px"><button class="ghost" id="helpClose">${ic("x")} Close</button></div></div>`;
  $("helpClose").addEventListener("click", closeHelp);
}
helpEl.addEventListener("click", (e) => { if (e.target === helpEl) closeHelp(); });
// keys and buttons the page answers itself (the engine never sees them, so a save replays without them)
/* ---------------- the outer world (chroma-world/, Emren 2026-10-06): the cast by layer, and the world panel ---------------- */
const CIRCLE_LAYERS = [[1, "Support"], [2, "Sympathy"], [3, "Friends"], [4, "Known"]];
function circleTip(p) {
  if (!p) return tipBox(`${ic("people")} Someone`, "", [], "");
  const rows = [["Who", esc(p.roles.join(", ") || "someone they know") + (p.age != null ? `, ${p.age}` : "")], ["Close", esc(p.close)], ["Trust", esc(p.trust)]];
  if (p.read) rows.push(["As they read them", pips(lettersOf(p.read)) + " " + lettersOf(p.read).map((c) => CNAME[c]).join(" and ")]);
  if (p.want) rows.push(["Wants from them", esc(p.want)]);
  return tipBox(`${ic(p.alive ? "people" : "candle")} ${esc(p.name)}`, "", rows, "Their colors as the character reads them, which can be wrong; it sharpens with time together.");
}
const worldEl = document.createElement("div"); worldEl.className = "help sheetwrap"; worldEl.hidden = true; document.body.appendChild(worldEl);
worldEl.addEventListener("click", (e) => { if (e.target === worldEl) closeWorld(); });
function closeWorld() { worldEl.hidden = true; worldEl.innerHTML = ""; hideTip(); }
function wAge(a, name) { return a < 0 ? `${Math.max(1, Math.round(-a))} yrs before ${esc(name)}` : `at ${Math.floor(a)}`; }
function worldLine(W) {
  // the world's history beside the life: eras as bands, big events as marks, the out-of-work line; by age, never by year
  const lo = Math.min(-10, ...(W.eras || []).map((e) => e.from)), hi = Math.max(W.age + 4, 20), X = (a) => 8 + (a - lo) / (hi - lo) * 984;
  let g = `<defs>${(W.eras || []).map((e, i) => { const cs = lettersOf(e.letters); return `<linearGradient id="we${i}" x1="0" x2="0" y1="0" y2="1">${cs.map((c, k) => `<stop offset="${cs.length > 1 ? k / (cs.length - 1) : 0}" stop-color="var(--c${c})" stop-opacity="0.55"/>`).join("")}</linearGradient>`; }).join("")}</defs>`;
  (W.eras || []).forEach((e, i) => { const x0 = X(e.from), x1 = X(e.to == null ? W.age : e.to);
    g += `<rect class="wer" data-era="${i}" x="${x0.toFixed(1)}" y="8" width="${Math.max(1, x1 - x0).toFixed(1)}" height="34" rx="3" fill="url(#we${i})"/>`;
    const full = cap(e.name), short = full.replace(/^The /, "").replace(/ years$/, ""), room = x1 - x0 - 10;   // a label that fits its band
    const lab = full.length * 7.2 <= room ? full : short.length * 7.2 <= room ? short : "";
    if (lab) g += `<text class="wel" x="${(x0 + 6).toFixed(1)}" y="21">${esc(lab)}</text>`; });
  const ser = W.series || [];
  if (ser.length > 1) { const mx = Math.max(12, ...ser.map((p) => p[1]));
    g += `<polyline class="wun" points="${ser.map((p) => `${X(p[0]).toFixed(1)},${(42 - p[1] / mx * 18).toFixed(1)}`).join(" ")}"/>`; }
  g += `<rect class="wlife" x="${X(0).toFixed(1)}" y="48" width="${Math.max(1, X(W.age) - X(0)).toFixed(1)}" height="6" rx="3"/>`;
  (W.history || []).filter((h) => h.big).forEach((h, i) => { g += `<circle class="wev" data-h="${(W.history || []).indexOf(h)}" cx="${X(h.age).toFixed(1)}" cy="51" r="4.5"/>`; });
  for (let a = Math.ceil(lo / 10) * 10; a <= hi; a += 10) g += `<text class="wax" x="${X(a).toFixed(1)}" y="70" text-anchor="middle">${a === 0 ? "born" : a < 0 ? a : a}</text>`;
  return `<svg class="wline" viewBox="0 0 1000 76" role="img" aria-label="The world's history beside the life, by age">${g}</svg>`;
}
function openWorld() {
  const W = hud && hud.world; if (!W) { toast("The world's record opens at the next pause."); return; }
  hideTip(); closeHud();
  const nm = W.name;
  const era = W.era ? `<div class="wera">${pips(lettersOf(W.era.letters))}<div><b>${esc(cap(W.era.name))}</b><div class="muted">${esc(W.era.idea)}</div><small class="muted">${W.era.kind ? esc(W.era.kind) + " · " : ""}since ${W.era.since < 0 ? "before " + esc(nm) + " was born" : esc(nm) + " was " + Math.floor(W.era.since)}</small></div></div>` : "";
  const E = W.econ;
  const econ = E ? `<div class="mts">${[["The economy", esc(E.phase)], ["Out of work", `${E.unemp.toFixed(1)} in 100`], ["Prices", `up ${E.infl.toFixed(1)} in 100 a year`], ["Homes", esc(E.housing)]].map(([k, v]) => `<div class="wst"><span class="ml">${k}</span><span>${v}</span></div>`).join("")}</div>` : "";
  const G = W.gov;
  const gov = G ? `<div class="wera">${pips(lettersOf(G.letters))}<div><b>${/^[AEIOU]/.test(G.name.replace(/^The /, "")) ? "An" : "A"} ${esc(G.name.replace(/^The /, ""))} government</b><div class="muted">${G.leader ? "led by " + esc(G.leader) + "; " : ""}${G.support} in 100 back it in the polls${G.next_age != null ? `; the next election when ${esc(nm)} is about ${Math.round(G.next_age)}` : ""}</div></div></div>` : "";
  const state = [W.state && W.state.war, W.state && W.state.pandemic].filter(Boolean).map((x) => `<span class="chip">${esc(cap(x))}</span>`).join("");
  const P = W.place;
  const place = P ? `<div class="wst"><span class="ml">${ic("ci-cottage")} Where they live</span><span>${esc(P.name)}${P.kind ? ", " + esc(P.kind) : ""}${P.abroad ? `, abroad in ${esc(P.society)}: ${esc(P.status)}; the language: ${esc(P.language)}` : ""}</span></div>` : "";
  const laws = (W.laws || []).map((l) => `<span class="chip">${ic("ci-gavel")}${esc(cap(l.word))}: <span class="w">${esc(l.state)}</span></span>`).join("");
  const rights = (W.rights || []).map((r) => `<span class="chip">${ic("ci-scales")}${esc(cap(r.word))}: <span class="w">${r.level >= 0.8 ? "secure" : r.level >= 0.5 ? "partial" : "weak"}</span></span>`).join("");
  const polls = (W.polls || []).slice(0, 6).map((p) => `<div class="mt"><span class="ml">${esc(cap(p.word))}</span><i><b style="width:${p.share}%;background:var(--gold)"></b></i><span class="mv">${p.share} in 100</span></div>`).join("");
  const figs = (W.figures || []).map((f) => `<div class="wfig${f.alive ? "" : " gone"}">${pips(lettersOf(f.letters))}<span><b>${esc(f.name)}</b> <span class="muted">${esc(f.role)}${f.alive ? "" : ", gone"}</span></span></div>`).join("");
  const hist = (W.history || []).slice(0, 60).map((x, i) => `<div class="whist${x.big ? " big" : ""}"><span class="wa">${wAge(x.age, nm)}</span>${ic(x.icon)}<span>${esc(x.text)}</span></div>`).join("");
  worldEl.hidden = false;
  worldEl.innerHTML = `<div class="box paper sheet world" role="dialog" aria-label="The world">
    <div class="shh"><div><div class="shn">${ic("ci-globe")} The world</div><div class="muted">the public record, as of ${esc(nm)}'s ${Math.floor(W.age)}th year</div></div><button class="ghost" id="wClose" aria-label="Close">${ic("x")}</button></div>
    ${worldLine(W)}
    <div class="shg">
      <section><h4>The times</h4>${era || `<span class="empty">No era named yet</span>`}${place}<h4>Government</h4>${gov || `<span class="empty">–</span>`}${state ? `<div class="chips">${state}</div>` : ""}</section>
      <section><h4>The figures, as published</h4>${econ}${laws ? `<h4>Laws</h4><div class="chips">${laws}</div>` : ""}${rights ? `<h4>Rights</h4><div class="chips">${rights}</div>` : ""}</section>
      <section>${polls ? `<h4>What people accept</h4><div class="mts">${polls}</div>` : ""}${figs ? `<h4>Public figures <span class="muted" style="text-transform:none;letter-spacing:0">as ${esc(nm)} reads them</span></h4>${figs}` : ""}</section>
      <section class="wide"><h4>History</h4><div class="whists">${hist || `<span class="empty">Nothing yet</span>`}</div></section>
    </div></div>`;
  $("wClose").addEventListener("click", closeWorld);
  worldEl.querySelectorAll(".wer").forEach((el) => { const e = W.eras[+el.dataset.era]; setTip(el, () => tipBox(`${pips(lettersOf(e.letters))} ${esc(cap(e.name))}`, "", [["From", wAge(e.from, nm)], ["To", e.to == null ? "now" : wAge(e.to, nm)]], "An era is a stretch of years in which society rewards one way of living.")); });
  worldEl.querySelectorAll(".wev").forEach((el) => { const h = W.history[+el.dataset.h]; setTip(el, () => tipBox(`${ic(h.icon)} ${esc(h.text)}`, "", [["When", wAge(h.age, nm)]], "")); });
}

function pageKey(k) {
  if (k === "i") { ilPace = { slow: "short", short: "off", off: "slow" }[ilPace] || "slow"; try { localStorage.setItem("chroma.pace", ilPace); } catch (_) {} toast(`Interlude: ${PACE_WORD[ilPace]}`); if (ilPace === "off" && IL.on) ilFinish(); renderTools(hud); return; }
  if (k === "c") { if (sheetEl.hidden) openSheet(); else closeSheet(); return; }
  if (k === "b") { if (bookEl.hidden) openBook(); else closeBook(); return; }
  if (k === "g") { if (worldEl.hidden) openWorld(); else closeWorld(); return; }
  if (k === "s") { if (!busy && hud && hud.mode === "play") saveToFile(); return; }
  if (k === "a") { autoOn = !autoOn; try { localStorage.setItem("chroma.autosave.on", autoOn ? "on" : "off"); } catch (_) {} toast(`Autosave ${autoOn ? "on: after every choice, one slot in this browser" : "off"}`); renderTools(hud); if (autoOn && hud && hud.mode === "play" && !busy) autoSaveNow(); return; }
  if (k === "o") { fileIn.click(); return; }
  if (k === "n") { askNewLife(); return; }
}
function closeHelp() { helpEl.hidden = true; helpEl.innerHTML = ""; }

/* ---------------- state ---------------- */
let hudDrawn = 0;
let autoKey = "";
function applyState(m) {
  busy = !!m.busy; hud = m.hud;
  if (hud.book_cat) takeCat(hud.book_cat);
  if (hud.book) bookMerge(hud.book);
  if (ilWanted(hud)) ilStart(hud.life);
  if (IL.on) ilFeed(hud);
  else if (hud.trace && hud.trace.length && !hud.replay && hud.job !== "past") hudFrames.push(...hud.trace.map(frameOf));
  if (hud.replay || hud.job === "past") hudFrames = [];
  if (hud.loaded) toast(hud.loaded);
  renderReplay(hud);
  const prev = app.dataset.mode;
  app.dataset.mode = hud.mode;
  stageEl.classList.toggle("paper", !["menu", "custom", "name"].includes(hud.mode));   // the start lies on the night table
  if (prev !== hud.mode && !["play", "over"].includes(hud.mode)) hudEl.classList.remove("open");
  if (hud.mode === "menu" && prev !== "menu") { resetChron(); reviewEl.hidden = true; }
  addFeed(m.feed);
  renderWho(hud.life);
  renderTools(hud);
  if (["menu", "custom", "name"].includes(hud.mode)) { if (!busy) renderScreen(hud); } else screenEl.innerHTML = "";
  const t = performance.now();
  const hudEmpty = !!(hud.life && hud.life.w && !hudEl.firstElementChild);   // a life's first stretch runs under the interlude: draw the HUD once, not leave it blank
  if (((!busy || t - hudDrawn > 280) && !(IL.on && busy)) || hudEmpty) { if (hud.life && hud.life.w && (!IL.on || hudEmpty)) renderHud(hud.life); drawLine(); hudDrawn = t; }
  if (!IL.on) renderTable(hud);
  renderPlan(hud);
  renderReview(hud);
  renderTransport();
  lockInputs(busy);
  const ak = !busy && !hud.replay && hud.mode === "play" && (hud.cp || hud.res) ? (hud.cp ? "cp" + hud.cp.age + hud.cp.title : "res" + hud.res.age + hud.res.title) : "";
  if (ak && ak !== autoKey) { autoKey = ak; if (autoOn) autoSaveNow(); }
  if (hud.note) toast(hud.note.startsWith("error") ? hud.note : hud.note + ".");
  if (!busy && !IL.on && (hud.cp || hud.res) && stick.bottom) chronEl.scrollTop = chronEl.scrollHeight;
}

document.addEventListener("keydown", (e) => {
  if (!helpEl.hidden) { if (e.key === "Escape" || e.key === "h") closeHelp(); return; }
  if (e.target.closest("input, textarea")) return;
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (!sheetEl.hidden) { if (e.key === "Escape" || e.key === "c") closeSheet(); return; }
  if (!bookEl.hidden) { if (e.key === "Escape" || e.key === "b") closeBook(); return; }
  if (!worldEl.hidden) { if (e.key === "Escape" || e.key === "g") closeWorld(); return; }
  if (IL.on && !busy && ["Enter", " ", "Escape"].includes(e.key)) { e.preventDefault(); ilFinish(); return; }
  if (IL.on && busy && e.key === "Escape") { pause(); ilFinish(); return; }
  if (e.key === "Escape") { if (menuOpen) { setMenu(false); const m = $("tMenu"); if (m) m.focus(); return; } if (busy) pause(); else if (hud && hud.plan) send("x"); hideTip(); hudEl.classList.remove("open"); return; }
  if (!hud || busy) return;
  const mode = hud.mode;
  if (mode === "menu") { if (hud.menu.some((p) => p.k === e.key)) beginLife(e.key, nameDraft); else if (e.key === "o" || e.key === "b") pageKey(e.key); return; }
  if (!["play", "over"].includes(mode)) return;
  if (hud.plan && e.key !== "Enter" && e.key !== "x" && e.key !== "Escape") { if (/^[1-5]$/.test(e.key)) send(e.key); return; }
  if (e.key === "Enter") { if (e.target.closest("button")) return; e.preventDefault(); send(""); return; }
  if (e.key === "h" || e.key === "?") { openHelp(); return; }
  if (/^[0-9]$/.test(e.key) && hud.cp) {
    const max = hud.cp.options.length;
    digitBuf += e.key; clearTimeout(digitTimer);
    // the number on the card (shown in order, without gaps) is mapped back to the engine's own option number
    const fire = () => {
      const n = +digitBuf; digitBuf = ""; const o = CPNUM.size ? CPNUM.get(n) : hud.cp.options.find((x) => x.n === n);
      if (o && o.status === "out of reach" && !oorOpen && openOOR) return openOOR(n);   // a folded card is shown first
      if (o) send(o.own ? "" : String(o.n));
    };
    if (max >= 10 && digitBuf === "1") digitTimer = setTimeout(fire, 450); else fire();
    return;
  }
  if (!hud.cp && ["w", "m", "y", "d"].includes(e.key) && mode === "play") { send(e.key); return; }
  if (["i", "c", "b", "s", "o", "n", "a"].includes(e.key) || (e.key === "g" && (hud.world || (hud.life && hud.life.world_era)))) { pageKey(e.key); return; }
  if (["f", "v", "l", "p"].includes(e.key)) send(e.key);
  if (e.key === "x" && hud.plan) send("x");
});

function fatal(msg) {
  app.dataset.mode = "boot";
  screenEl.innerHTML = `<div class="boot"><div class="hero"><h1>CHROMA</h1></div><p>Could not start: ${esc(msg)}</p><p>This page runs the real engine (Python and numpy) inside your browser with WebAssembly. If the browser or this viewer blocks that, the same game runs in a terminal: python3 play.py in the project's chroma-game/prototype folder (needs Python 3 and numpy).</p></div>`;
}
stageEl.classList.remove("paper");
// v22 next look: a returning player sees the spread at once (the menu is kept from the last visit) while Python loads
if (bootMenu && bootMenu.length) renderScreen({ mode: "menu", menu: bootMenu, booting: true });
else screenEl.innerHTML = `<div class="boot"><div class="hero"><h1>CHROMA</h1><div class="pips">${COLORS.map((c) => pip(c)).join("")}</div><p>One life. Five colors. You are the voice in their head.</p></div><span class="spin"></span><span id="bootMsg">Loading Python and numpy in your browser (about 16 MB the first time)…</span><span class="bootbar"><i></i></span></div>`;
drawLine();
const watchdog = setTimeout(() => { if (!ready) fatal("the Python runtime did not start within 90 seconds."); }, 90000);
try {
  worker = new Worker(new URL("worker.js", location.href).href);
  worker.onmessage = (e) => {
    const m = e.data;
    if (m.kind === "state") { if (!ready) { ready = true; clearTimeout(watchdog); const wm = worldMeta(); if (wm) worker.postMessage({ cmd: "world_in", text: JSON.stringify(wm) }); } applyState(m); }
    else if (m.kind === "sys") { if (!ready) { const b = $("bootMsg"); if (b) b.textContent = m.text; } else { busy = false; toast(m.text); renderTransport(); lockInputs(false); } }
    else if (m.kind === "save") { const w = saveWait; saveWait = null; if (w) w(m.data); }
    else if (m.kind === "world") keepWorld(m.data);
    else if (m.kind === "fatal") { clearTimeout(watchdog); fatal(m.msg); }
  };
  worker.onerror = (e) => { clearTimeout(watchdog); fatal(e.message || "the engine worker failed to load."); };
} catch (e) { clearTimeout(watchdog); fatal(e.message || String(e)); }
</script>
