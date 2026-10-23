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
  if (p.want && p.want_why) rows.push(["Why", esc(p.want_why)]);   // far ties (F5): what happened in their town
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
  // P3: each push or lean on the life's line, with the era's pull (light) or against it (dark)
  (W.steers || []).forEach((x, i) => { g += `<rect class="wst2 ${x.era >= 0.3 ? "with" : x.era <= -0.3 ? "against" : "even"}${x.kind === "lean" ? " lean" : ""}" data-st="${i}" x="${(X(x.age) - 1.5).toFixed(1)}" y="56" width="3" height="${x.kind === "lean" ? 4 : 7}" rx="1"/>`; });
  // spheres phase 4: each lever act of theirs on the town's spheres, by what came of it
  (W.levers || []).forEach((x, i) => { g += `<circle class="wlv ${x.went}" data-lv="${i}" cx="${X(x.age).toFixed(1)}" cy="58" r="2.6"/>`; });
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
  // WL5: the character's own record of what the world changed of theirs, by age
  const times = (W.times || []).slice().reverse().slice(0, 40).map((x) => `<div class="whist${x.big ? " big" : ""}" data-tm="${esc(x.cause || "")}"><span class="wa">${wAge(x.age, nm)}</span>${ic("globe")}<span>${esc(x.text)}</span></div>`).join("");
  const levers = (W.levers || []).map((x, i) => [x, i]).reverse().slice(0, 40).map(([x, i]) => `<div class="whist${x.went === "fired" || x.went === "state" ? " big" : ""}" data-lv="${i}"><span class="wa">${wAge(x.age, nm)}</span>${ic(LEVER_ICON[x.lever] || "push")}<span>${esc(x.text)}</span></div>`).join("");
  // v25 what this world prizes (#10): which ways count for more toward standing in each sphere of their town, and for them
  const Z = W.prizes;
  const prizes = Z ? (Z.even ? `<p class="muted">Every way counts alike here.</p>` : `<div class="mts">${Z.rows.filter((x) => x.more.length || x.less.length).map((x) => `<div class="wst prize"><span class="ml">${esc(x.name)}</span><span>${pips(lettersOf(x.more_c))} ${x.more.length ? esc(x.more.join(" and ")) + " count for more" : ""}${x.more.length && x.less.length ? "; " : ""}${x.less.length ? esc(x.less.join(" and ")) + " for less" : ""}</span><span class="muted">for ${esc(nm)}: ${esc(x.for_me)}</span></div>`).join("")}</div>`)
    + (Z.moves.length ? `<div class="whists">${Z.moves.slice().reverse().map((m) => `<div class="whist"><span class="wa">${wAge(m.age, nm)}</span>${ic("globe")}<span>${esc(m.name)} moved${m.cause ? ": " + esc(m.cause) : ""}</span></div>`).join("")}</div>` : "") : "";
  const hist = (W.history || []).slice(0, 60).map((x, i) => `<div class="whist${x.big ? " big" : ""}"><span class="wa">${wAge(x.age, nm)}</span>${ic(x.icon)}<span>${esc(x.text)}</span></div>`).join("");
  worldEl.hidden = false;
  worldEl.innerHTML = `<div class="box paper sheet world" role="dialog" aria-label="The world">
    <div class="shh"><div><div class="shn">${ic("ci-globe")} The world</div><div class="muted">the public record, as of ${esc(nm)}'s ${Math.floor(W.age)}th year</div></div><button class="ghost" id="wClose" aria-label="Close">${ic("x")}</button></div>
    ${worldLine(W)}
    <div class="shg">
      <section><h4>The times</h4>${era || `<span class="empty">No era named yet</span>`}${place}<h4>Government</h4>${gov || `<span class="empty">–</span>`}${state ? `<div class="chips">${state}</div>` : ""}</section>
      <section><h4>The figures, as published</h4>${econ}${laws ? `<h4>Laws</h4><div class="chips">${laws}</div>` : ""}${rights ? `<h4>Rights</h4><div class="chips">${rights}</div>` : ""}</section>
      <section>${polls ? `<h4>What people accept</h4><div class="mts">${polls}</div>` : ""}${figs ? `<h4>Public figures <span class="muted" style="text-transform:none;letter-spacing:0">as ${esc(nm)} reads them</span></h4>${figs}` : ""}</section>
      ${prizes ? `<section class="wide"><h4>What this world prizes <span class="muted" style="text-transform:none;letter-spacing:0">in ${esc(nm)}'s town, now</span></h4>${prizes}</section>` : ""}
      ${times ? `<section class="wide"><h4>What the times did to ${esc(nm)}</h4><div class="whists">${times}</div></section>` : ""}
      ${levers ? `<section class="wide"><h4>What ${esc(nm)} did in town</h4><div class="whists">${levers}</div></section>` : ""}
      <section class="wide"><h4>History</h4><div class="whists">${hist || `<span class="empty">Nothing yet</span>`}</div></section>
    </div></div>`;
  $("wClose").addEventListener("click", closeWorld);
  worldEl.querySelectorAll(".wer").forEach((el) => { const e = W.eras[+el.dataset.era]; setTip(el, () => tipBox(`${pips(lettersOf(e.letters))} ${esc(cap(e.name))}`, "", [["From", wAge(e.from, nm)], ["To", e.to == null ? "now" : wAge(e.to, nm)]], "An era is a stretch of years in which society rewards one way of living.")); });
  worldEl.querySelectorAll(".wev").forEach((el) => { const h = W.history[+el.dataset.h]; setTip(el, () => tipBox(`${ic(h.icon)} ${esc(h.text)}`, "", [["When", wAge(h.age, nm)]], "")); });
  worldEl.querySelectorAll("[data-tm]").forEach((el) => { if (el.dataset.tm) setTip(el, () => tipBox(`${ic("globe")} Why`, esc(cap(el.dataset.tm)), [], "")); });
  worldEl.querySelectorAll("[data-lv]").forEach((el) => { const x = W.levers[+el.dataset.lv]; setTip(el, () => tipBox(`${ic(LEVER_ICON[x.lever] || "push")} ${esc(cap(x.lever))} in ${esc(x.where)}`, "",
    [["When", wAge(x.age, nm)], ["What came of it", esc(x.came)]].concat(x.rung ? [["Their standing there", esc(x.rung)]] : []), "")); });
  worldEl.querySelectorAll(".wst2").forEach((el) => { const x = W.steers[+el.dataset.st]; setTip(el, () => tipBox(`${x.kind === "lean" ? pip(x.lean) + " A lean" : ic("push") + " A push"} ${x.colors && x.colors !== "-" ? "toward " + pips(lettersOf(x.colors)) : ""}`, "",
    [["When", wAge(x.age, nm)], ["The times", x.era >= 0.3 ? "with their pull: it cost less" : x.era <= -0.3 ? "against their pull: it cost more" : "neither with nor against"]], "")); });
}

function pageKey(k) {
  if (k === "i") { ilPace = { slow: "short", short: "off", off: "slow" }[ilPace] || "slow"; try { localStorage.setItem("chroma.pace", ilPace); } catch (_) {} toast(`Interlude: ${PACE_WORD[ilPace]}`); if (ilPace === "off" && IL.on) ilFinish(); renderTools(hud); return; }
  if (k === "c") { if (sheetEl.hidden) openSheet(); else closeSheet(); return; }
  if (k === "b") { if (bookEl.hidden) openBook(); else closeBook(); return; }
  if (k === "g") { if (worldEl.hidden) openWorld(); else closeWorld(); return; }
  if (k === "j") { if (agendaEl.hidden) openAgenda(); else closeAgenda(); return; }
  if (k === "s") { if (!busy && hud && hud.mode === "play") saveToFile(); return; }
  if (k === "a") { autoOn = !autoOn; try { localStorage.setItem("chroma.autosave.on", autoOn ? "on" : "off"); } catch (_) {} toast(`Autosave ${autoOn ? "on: after every choice, one slot in this browser" : "off"}`); renderTools(hud); if (autoOn && hud && hud.mode === "play" && !busy) autoSaveNow(); return; }
  if (k === "o") { fileIn.click(); return; }
  if (k === "n") { askNewLife(); return; }
}
function closeHelp() { helpEl.hidden = true; helpEl.innerHTML = ""; }

