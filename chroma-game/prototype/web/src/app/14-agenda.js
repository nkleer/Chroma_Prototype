/* ---------------- v25 the agenda (the game's agenda switch; Emren's decision file section 5, #9): every held aim on one
   persistent page (key j, the Agenda door): importance, the step and its clock, the commitment state and priority, the
   character's own lean, pending decisions, the real bottleneck, earned assets apart from what an aim could bring. A
   compact strip of it sits in the status panel. Reading it costs no time; pace and priority are the player's acts. ---- */
const agendaEl = document.createElement("div"); agendaEl.className = "help sheetwrap"; agendaEl.hidden = true; document.body.appendChild(agendaEl);
agendaEl.addEventListener("click", (e) => { if (e.target === agendaEl) closeAgenda(); });
let agFocus = null;              // the aim the player just adjusted: the page reopens on it when the new state comes
function closeAgenda() { agendaEl.hidden = true; agendaEl.innerHTML = ""; hideTip(); }
const AG_PACE = [["pursuing", "In full"], ["reduced", "Less"], ["keeping_up", "Keep up"], ["paused", "Pause"], ["holding", "Just hold"]];
const AG_FORK = { go_on: "go on or stop", pay: "pay the cost", take: "take the chance", round: "a way round" };
const agLadder = (x) => `<span class="ladder">${Array.from({ length: x.step.of }, (_, i) => `<i class="${i < x.step.i ? "on" : ""}"></i>`).join("")}</span>`;
const agStep = (x) => x.step.of ? `step ${x.step.i} of ${x.step.of}${x.step.next ? `, next: ${esc(x.step.next)}` : x.step.i >= x.step.of ? ", every step reached" : ""}` : "";
const agForkWord = (f) => esc(AG_FORK[f.kind] || f.kind || "a decision");
function agendaStripHTML(L) {      // the status panel's strip: the first three aims, and decisions waiting
  const A = L.agenda; if (!A) return "";
  const rows = A.items.slice(0, 3).map((x) => `<div class="agrow" data-agj="${x.slot}">${ic(x.calling ? "flame" : "route")}<span class="an">${esc(x.aim)}</span>${agLadder(x)}${x.pending.length ? `<b class="agwait" title="decisions waiting">${x.pending.length}</b>` : ""}</div>`).join("");
  const more = A.items.length > 3 ? `<span class="muted">+${A.items.length - 3} more</span>` : "";
  return `<div class="hsec agstrip"><h4>Agenda${A.forks.length ? ` <span class="cnt">${A.forks.length} waiting</span>` : ""}</h4>${rows || `<span class="empty">No aims yet</span>`}${more}<button class="ghost agopen" id="agOpen">${ic("route")} Open the agenda <kbd>j</kbd></button></div>`;
}
function agendaStripBind(root) {
  const b = root.querySelector("#agOpen"); if (b) b.addEventListener("click", (e) => { e.stopPropagation(); openAgenda(); });
  root.querySelectorAll("[data-agj]").forEach((el) => el.addEventListener("click", (e) => { e.stopPropagation(); openAgenda(+el.dataset.agj); }));
}
function openAgenda(focus) {
  const L = hud && hud.life, A = L && L.agenda; if (!A) { toast("The agenda opens once the life has begun."); return; }
  hideTip(); closeHud();
  const can = A.full && hud.mode === "play" && !busy;
  const capRow = A.capacity.length ? `<div class="agcap">${A.capacity.map((c) => `<span class="chip ag-${c.load.replace(/ /g, "-")}" data-agc="${esc(c.res)}">${esc(c.say)}: <b>${esc(c.load)}</b></span>`).join("")}</div>` : "";
  const groups = {}; A.forks.forEach((f) => { const g = f.group == null ? "solo-" + f.id : "g-" + f.group; (groups[g] = groups[g] || []).push(f); });
  const aimOf = (s) => (A.items.find((x) => x.slot === s) || {}).aim || "an aim";
  const forks = Object.entries(groups).map(([g, fs]) => `<div class="agfg">${fs.length > 1 ? `<div class="muted">Linked: ${fs.length} decisions that share ${esc(fs[0].blocks || "a limit")}${can && (A.reviews || {})[String(fs[0].group)] ? ` <button class="ghost" data-agrv="${esc(String(fs[0].group))}">Look at them together</button>` : ""}</div>` : ""}${fs.map((f) => `<div class="wst"><span>${ic("flag")} ${esc(cap(aimOf(f.slot)))}: ${agForkWord(f)}</span><span class="ml">${f.deadline != null ? `decide by ${Math.floor(f.deadline)}` : f.age != null ? `waiting since ${Math.floor(f.age)}` : ""}</span></div>`).join("")}</div>`).join("");
  const card = (x) => {
    const bn = x.bottleneck ? `<div class="agbn">${ic("hourglass")} Held back by ${esc(x.bottleneck.say.toLowerCase())}${x.bottleneck.shared_with.length ? `, shared with ${x.bottleneck.shared_with.map((s) => esc(aimOf(+s))).join(", ")}` : ""}</div>` : "";
    const prog = x.frac != null ? `<div class="agprog"><i style="width:${Math.round(x.frac * 100)}%"></i></div>` : "";
    const clock = [x.effort_years != null ? `${x.effort_years} years at it` : "", x.clock].filter(Boolean).join(" · ");
    const earned = x.earned.map((a) => `<span class="chip" data-agx="${x.slot}" title="${esc(a.source || "")}">${ic("check")}${esc(a.name)}</span>`).join("");
    const pot = x.potential.map((a) => `<span class="chip dim">${ic("star")}${esc(a.name)}${a.step ? ` <span class="muted">at ${esc(a.step)}</span>` : ""}</span>`).join("");
    const ctl = can ? `<div class="agctl">${AG_PACE.map(([k, w]) => `<button class="ghost${x.state === k ? " on" : ""}" data-agp="${x.slot}" data-pace="${k}" aria-pressed="${x.state === k}">${w}</button>`).join("")}
      <button class="ghost" data-agr="${x.slot}" data-rank="${Math.max(1, x.priority - 1)}" aria-label="Move up"${x.priority <= 1 ? " disabled" : ""}>↑</button><button class="ghost" data-agr="${x.slot}" data-rank="${x.priority + 1}" aria-label="Move down"${x.priority >= A.items.length ? " disabled" : ""}>↓</button></div>` : "";
    return `<section class="agcard${focus === x.slot ? " focus" : ""}" id="ag${x.slot}"><div class="agh"><b class="agn">${x.priority}</b>${ic(x.calling ? "flame" : "route")}<span class="an">${esc(x.aim)}</span> ${pips(lettersOf(x.face || ""))}
      <span class="chip">${esc(x.importance)}</span><span class="chip">${esc(x.state_say)}</span>${x.by_player ? `<span class="muted">set by you</span>` : ""}${x.calling ? `<span class="muted">a calling</span>` : ""}</div>
      <div class="agl">${agLadder(x)} <span>${agStep(x)}</span></div>${prog}${clock ? `<div class="muted">${esc(clock)}</div>` : ""}
      ${x.why_now ? `<div>${esc(cap(x.why_now))}</div>` : ""}${x.lean ? `<div class="muted">${esc(L.name)} is ${esc(x.lean)} about it</div>` : ""}${bn}
      ${x.pending.length ? `<div class="agwaitl">${ic("flag")} ${x.pending.length} decision${x.pending.length > 1 ? "s" : ""} waiting on you</div>` : ""}
      ${earned ? `<div class="aged"><span class="ml">Earned</span><div class="chips">${earned}</div></div>` : ""}${pot ? `<div class="aged"><span class="ml">Could bring</span><div class="chips">${pot}</div></div>` : ""}${ctl}</section>`;
  };
  agendaEl.hidden = false;
  agendaEl.innerHTML = `<div class="box paper sheet world agenda" role="dialog" aria-label="The agenda">
    <div class="shh"><div><div class="shn">${ic("route")} The agenda</div><div class="muted">what ${esc(L.name)} is working toward, at ${Math.floor(L.age)}</div></div><button class="ghost" id="agClose" aria-label="Close">${ic("x")}</button></div>
    ${A.full ? "" : `<p class="note">This engine shows the aims only. Shared time and money, the decisions waiting and what holds an aim back come with the v25 engine.</p>`}
    ${capRow}
    ${forks ? `<h4>Decisions waiting</h4><div class="agforks">${forks}</div>` : ""}
    <div class="agitems">${A.items.map(card).join("") || `<span class="empty">No aims yet</span>`}</div></div>`;
  $("agClose").addEventListener("click", closeAgenda);
  agendaEl.querySelectorAll("[data-agp]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); send(`agenda pace ${b.dataset.agp} ${b.dataset.pace}`); agFocus = +b.dataset.agp; }));
  agendaEl.querySelectorAll("[data-agr]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); send(`agenda prio ${b.dataset.agr} ${b.dataset.rank}`); agFocus = +b.dataset.agr; }));
  agendaEl.querySelectorAll("[data-agc]").forEach((el) => { const c = A.capacity.find((y) => y.res === el.dataset.agc); if (c) setTip(el, () => tipBox(`${esc(c.say)}: ${esc(c.load)}`, "", c.items.map((s) => [esc(cap(typeof s === "number" ? aimOf(s) : s)), "draws on it"]), "One account for every aim, with work, care and the people in their life.")); });
  agendaEl.querySelectorAll("[data-agrv]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); openReview(b.dataset.agrv); }));
  if (focus != null) { const el = $("ag" + focus); if (el) el.scrollIntoView({ block: "nearest" }); }
}

/* Information before a commitment (#9): what taking up an aim would ask, from the life as it is (the Engine's preview):
   what it needs, what it takes, what it competes with, its deadline, what nobody knows yet, and how to step back. Shown
   before the aim is taken up; the v24 engine has no previews, and then the choice is taken at once as before. */
function previewRows(pv) {
  const r = [];
  if (pv.needs.length) r.push(["Needs", esc(pv.needs.join(", "))]);
  const take = [pv.hours, pv.money && `each year ${pv.money}`, pv.entry && `to start, ${pv.entry}`].filter(Boolean);
  if (take.length) r.push(["Takes", esc(take.join("; "))]);
  if (pv.overlaps.length) r.push(["Competes with", esc(pv.overlaps.join(", "))]);
  if (pv.window) r.push(["The chance", esc(pv.window)]);
  if (pv.unknown.length) r.push(["Not known yet", esc(pv.unknown.join(", "))]);
  if (pv.exit) r.push(["Stepping back", esc(pv.exit)]);
  return r;
}
const previewTable = (pv) => { const r = previewRows(pv); return r.length ? `<table class="agpv">${r.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join("")}</table>` : ""; };
function openPreview(c) {
  hideTip(); closeHud();
  agendaEl.hidden = false;
  agendaEl.innerHTML = `<div class="box paper sheet world agenda" role="dialog" aria-label="Before taking it up">
    <div class="shh"><div><div class="shn">${ic("target")} ${esc(c.aim)} ${aimFace(c.face)}</div><div class="muted">what it would ask of ${esc(hud.life.name)}, as things stand</div></div><button class="ghost" id="agClose" aria-label="Close">${ic("x")}</button></div>
    ${previewTable(c.preview) || `<p class="muted">Nothing it asks is known yet.</p>`}
    <div class="center agbtns"><button class="primary" id="pvOk">${ic("check")} Take it up</button><button class="ghost" id="pvNo">Not now</button></div></div>`;
  $("agClose").addEventListener("click", closeAgenda); $("pvNo").addEventListener("click", closeAgenda);
  $("pvOk").addEventListener("click", () => { closeAgenda(); send(`aim set ${c.aim}`); });
}
/* The agenda review (#9): decisions that share a real limit (time, money, a deadline, a person's time) seen and answered
   together. Each shows why it is linked, what each way would ask, and the shared account now and after the ways picked,
   as the Engine lists them. Any decision left unanswered stays waiting; nothing is approved for the player. */
function openReview(g) {
  const L = hud && hud.life, A = L && L.agenda, R = A && (A.reviews || {})[g]; if (!R) return;
  const pick = {};
  const capChips = (cs) => cs.map((c) => `<span class="chip ag-${c.load.replace(/ /g, "-")}">${esc(c.say)}: <b>${esc(c.load)}</b></span>`).join("");
  const draw = () => {
    const combo = R.combos.find((c) => R.forks.every((f) => (c.choices[f.id] || null) === (pick[f.id] || null)));
    const after = combo ? `<div class="agcap"><span class="ml">After</span>${capChips(combo.capacity)}</div>${combo.slower.length ? `<div class="muted">Slower: ${esc(combo.slower.join(", "))}</div>` : ""}` : Object.keys(pick).length ? `<div class="muted">The account after these is worked out when they are applied.</div>` : "";
    agendaEl.innerHTML = `<div class="box paper sheet world agenda" role="dialog" aria-label="Decisions together">
      <div class="shh"><div><div class="shn">${ic("flag")} Decisions together</div><div class="muted">${esc(cap(R.why || "they share a limit"))}</div></div><button class="ghost" id="agClose" aria-label="Close">${ic("x")}</button></div>
      <div class="agcap"><span class="ml">Now</span>${capChips(R.capacity)}</div>${after}
      ${R.forks.map((f) => `<section class="agcard"><div class="agh">${ic("route")}<span class="an">${esc(f.aim)}</span>${f.deadline != null ? `<span class="chip">decide by ${Math.floor(f.deadline)}</span>` : ""}</div>
        ${f.why ? `<div>${esc(cap(f.why))}</div>` : ""}${f.preview ? previewTable(f.preview) : ""}
        <div class="agctl">${f.options.map((o) => `<button class="ghost${pick[f.id] === o.key ? " on" : ""}" data-rf="${esc(f.id)}" data-ro="${esc(o.key)}" aria-pressed="${pick[f.id] === o.key}">${esc(o.say)}</button>`).join("")}</div></section>`).join("")}
      <div class="center agbtns"><button class="primary" id="rvOk"${Object.keys(pick).length ? "" : " disabled"}>${ic("check")} Settle ${Object.keys(pick).length < R.forks.length ? "these, leave the rest waiting" : "them"}</button><button class="ghost" id="rvBack">Back to the agenda</button></div></div>`;
    $("agClose").addEventListener("click", closeAgenda); $("rvBack").addEventListener("click", () => openAgenda());
    agendaEl.querySelectorAll("[data-rf]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); const k = b.dataset.rf; pick[k] = pick[k] === b.dataset.ro ? undefined : b.dataset.ro; if (pick[k] === undefined) delete pick[k]; draw(); }));
    const ok = $("rvOk"); if (ok) ok.addEventListener("click", () => { send(`agenda apply ${JSON.stringify({ choices: pick, set: {} })}`); agFocus = R.forks[0].slot; });
  };
  hideTip(); closeHud(); agendaEl.hidden = false; draw();
}
/* A fork card (the game's aim_forks): the moment is a decision about held aims; the card says which, why now and what
   each way would ask, and when the decision is linked to others, opens them together. */
function forkNoteHTML(f) {
  return `<div class="note fork">${ic("flag")} A decision on their aim${f.aims.length > 1 ? "s" : ""}, ${esc(f.aims.join(" and ") || "an aim")}${f.why ? `. ${esc(cap(f.why))}` : ""}
    ${f.preview ? previewTable(f.preview) : ""}${f.grouped && f.group != null ? `<button class="ghost" data-fkrv="${esc(f.group)}">Linked with other decisions: see them together</button>` : ""}
    ${f.later != null ? `<p class="muted">Not choosing leaves it waiting on the agenda: only this aim waits. It is never decided for you.</p>` : ""}</div>`;
}
document.addEventListener("click", (e) => { const b = e.target.closest && e.target.closest("[data-fkrv]"); if (b) { e.stopPropagation(); openReview(b.dataset.fkrv); } });
/* A clash moment (the game's clash_card, #3): a real demand meets something that matters to them. The banner names the
   part of life it is in and what is at stake, never their colours against the others'; each option carries its kind. */
const CLASH_KIND = { confront: ["voice", "stand up to it"], give_in: ["anchor", "go along with it"], leave: ["gate", "leave it behind"],
  own_scene: ["candle", "find people of their own"], bridge: ["link", "build a bridge"] };
const clashChip = (k) => { const c = CLASH_KIND[k]; return c ? `<span class="mk2 clash">${ic(c[0])}${c[1]}</span>` : ""; };
function clashBannerHTML(c) {
  return `<p class="note clash">${ic("bolt")} At odds${c.spheres.length ? ` in ${esc(c.spheres.join(" and ").toLowerCase())}` : ""}${c.stakes.length ? `: what is asked runs against ${esc(c.stakes.join(", "))}` : ""}</p>`;
}
/* The land ways they hold (the game's land_row; land-v1.md section 5): each way with its three steps, the next one and
   its usual years, and the bridges: a held pair opens something; one half held names the other as a door. */
const LAND_ICON = { field: "sprout", wood: "leaf", water: "rain" };
function landHTML(D) {
  if (!D.ways.length && !D.bridges.length) return "";
  const ws = D.ways.map((w) => `<div class="agrow" title="${esc(w.hours + " hours a week; meets " + w.meets)}">${ic(LAND_ICON[w.stretch] || "leaf")}<span class="an">${esc(w.name)}</span><span class="ladder">${w.steps.map((s, i) => `<i class="${i < w.step ? "on" : ""}"></i>`).join("")}</span>${w.next ? `<span class="muted">next: ${esc(w.next)}${w.steps[w.step] && w.steps[w.step].clock ? ` (${esc(w.steps[w.step].clock)})` : ""}</span>` : ""}</div>`).join("");
  const bs = D.bridges.map((b) => b.held ? `<span class="chip">${ic("crown")}${esc(b.opens)}</span>` : `<span class="chip dim">${ic("gate")}${esc(b.opens)} <span class="muted">with ${esc(b.need)}</span></span>`).join("");
  return `<div class="agstrip land"><h4>The land</h4>${ws}${bs ? `<div class="chips">${bs}</div>` : ""}</div>`;
}
