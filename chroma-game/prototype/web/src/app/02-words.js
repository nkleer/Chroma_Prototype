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
const CAUSE_FOOT = { pick: "Their own pick, back then, is why.", mark: "What happened back then left its mark.", moment: "What they met back then is why.",
  held: "It grew from what they already had.", money: "The money made it possible.", years: "Its time ran out.", unused: "Unused, it slipped away." };
function causeTip(pl) {     // marker Y: kind|age|person id|the earlier moment, or a year: event|source|turn|how far|up|down
  const k = pl[0];
  if (k === "event" || k === "source" || k === "turn")
    return tipBox(`${pip(pl[2])} ${ic("push")} A year that turned them`, "", [["How far the colors moved", `${Math.round(+pl[1] * 100)} pts`],
      ["Most up", `${pip(pl[2])} ${CNAME[pl[2]] || ""}`], ["Most down", `${pip(pl[3])} ${CNAME[pl[3]] || ""}`]],
      k === "event" ? "The week of this event moved them most the way the year went." : k === "source" ? "What moved them most the way the year went." : "No one event did it: the year moved them a little at a time.");
  const rows = [];
  if (pl[3]) rows.push(["Back then", esc(pl[3])]);
  if (pl[1]) rows.push(["At", `age ${esc(pl[1])}`]);
  const p = pl[2] ? castById(+pl[2]) : null;
  if (p) rows.push(["With", esc(p.name) + (p.alive ? "" : ", gone now")]);
  return tipBox(`${ic("route")} Why it came`, "", rows, CAUSE_FOOT[k] || "");
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
// spheres phase 4 and far ties: a lever act's icon, and a tie's news by its side
const LEVER_ICON = { exit: "ci-door-open", voice: "voice", loyalty: "anchor", neglect: "ci-door-shut", subvert: "mask", found: "sprout", fund: "coin", lead: "flag", office: "ci-gavel" };
const FAR_ICON = { good: "sun", hard: "rain", mixed: "ci-letter" };
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
    case "T": return tipBox(`${pip(pl[0])} A turning point`, pl[1] === "reinvention" ? "They took the way the voice pushed for, for good." : pl[1] === "snap back" ? "They went back to their own way, for good." : "They took a new way.",
      [["It held", pl[2] === "1" ? "yes" : "no: the old pull came back"]], "The price of being pushed against their own pull built up until it came to a head.");   // 5.6
    case "X": return tipBox(`${ic("globe")} What the times did`, esc(cap(pl[4] || "")), [], "Told only when the world really changed something of theirs.");   // WL1
    case "L": return tipBox(`${ic(LEVER_ICON[pl[0]] || "push")} Their act in town`, "", [["Where", esc(pl[1])], ["What came of it", esc(pl[2])]].concat(pl[3] ? [["Their standing there", esc(pl[3])]] : []),
      "What they do moves the places and the town around them a little, more as their standing there grows. The World panel (key g) keeps each act.");   // spheres phase 4
    case "N": return tipBox(`${ic("voice")} Word from one of their places`, "", [["Heard at", esc(pl[1] || "")]],
      pl[0] === "bent" ? "The story changed on its way to them, as stories do." : pl[0] === "warn" ? "A friendly warning: their name there is at stake." : "What one of their places thinks of them travels to the others, through the people who go to both.");   // S3
    case "S": { const ln = ((L && L.lines) || []).find((x) => x.kind === pl[0]);
      return tipBox(`${pip(pl[1])} ${ic("lock")} ${esc(ln ? ln.name : "A line they will not cross")}`, ln ? `Will not ${esc(ln.will_not)}` : "", [], "Twice it cost them dearly, and they held. An offer that touches it now weighs more than its price."); }   // S5
    case "F": return tipBox(`${ic(FAR_ICON[pl[0]] || "ci-letter")} News through a tie`, "", pl[2] ? [[`For ${esc(pl[1])}`, esc(pl[2])]] : [],
      "Something happened in the town where someone close to them lives, and it reached them.");   // far ties
    case "r": return tipBox(`${ic("scroll")} Read through their colors`, `“${esc(pl[0])}”`, [["How hard it hits", hitWord(+pl[1])]].concat(
      COLORS.includes(pl[2]) ? [["Pulls them toward", `${pip(pl[2])} ${CNAME[pl[2]]}`]] : []), COLORS.includes(pl[2]) ? "How they read it pulls their wanting toward its color." : "");
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
    case "Y": return causeTip(pl);   // Every change has a cause (GAME causes): the trail of a change, or a year that turned them
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
// item 3 (chroma-ideas/voice-mechanics.md): the voice in their head, one row on the panel; its numbers on hover
function voiceRowHTML(L) {
  const V = L.voice_row;
  if (!V || !V.n) return "";
  return `<div class="voicerow" id="voiceRow" tabindex="0">${ic("voice")}<span class="k">The voice in their head</span><span class="nm">${esc(V.name)}</span>${V.trust ? `<small>${esc(V.trust)}</small>` : ""}</div>`;
}
function voiceRowTip(L) {
  const V = L.voice_row, pts = (x) => `${x > 0 ? "+" : x < 0 ? "−" : ""}${Math.abs(x).toFixed(0)}`;
  const big = (xs) => COLORS.map((c, i) => [c, xs[i]]).filter(([, x]) => Math.abs(x) >= 1).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1])).slice(0, 3);
  const say = (xs) => big(xs).map(([c, x]) => `${CNAME[c]} ${pts(x)}`).join(" and ");
  const you = say(V.voice), life = say(V.life);
  const line = !V.steer ? "You have let them choose: the voice has not pushed yet." :
    (you ? `You moved their ${you} in this life.` : "Your pushes have not moved their colors much yet.") + (life ? ` Life itself moved ${life}.` : "");
  // S2: each way the voice pushed toward, how far it has become theirs, in the character's words (Library VOICE.own)
  const OWN_STEP = { asked: "only because the voice asks", ought: "they feel they ought to", sees: "they see why it matters", theirs: "it is theirs now" };
  const own = (V.own || []).map((o) => [`${pip(o.color)} ${CNAME[o.color]}`, esc(o.line || OWN_STEP[o.step] || "")]);
  return tipBox(`${ic("voice")} ${esc(cap(V.name))}`, esc(line), [["Pushed", `${V.steer} of ${V.n} moments`]].concat(V.steer ? [["The voice's part", `${pct(V.share)} of how their colors changed`]] : []).concat(own),
    "In points of 100, since you became the voice. Its name comes from what it pushes for most; the arrows on the wheel show where." +
    (own.length ? " The ways it pushes become theirs with light steers, their trust in you and people around them who live that way." : ""));
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

