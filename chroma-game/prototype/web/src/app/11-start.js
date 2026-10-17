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
    <div class="gauges">${gauge(r.fulfilment, "Satisfaction", "var(--sat)", "Their satisfaction, averaged over every week from 18 on.")}${gauge(r.serenity, "Peace", "var(--peace)", "Their peace, averaged over every week from 18 on.")}${gauge(r.integrity, "True to self", "var(--gold)", "1 minus the average reluctance of the choices you pushed on them (over at least ten pushes, so one or two cannot sink a life). A life you never pushed reads 1.")}${r.gifts != null ? gauge(r.gifts, "Their gifts", "var(--want)", "At each moment, their skill in the ways the chosen act used, against their best skill; averaged over every choice.") : ""}</div>
    <div class="muted center pnote">How well they lived is satisfaction and peace. How much the life was their own is being true to themselves and using their gifts. It is a reading, not a score.</div>
    <div class="center"><div class="muted" style="margin-bottom:6px">Identities lived · ${r.paths}</div><div class="path">${pathHTML(r.path, r.path_labels)}</div></div>
    ${r.died ? `<div class="center died">${ic("candle")} ${esc(L_name(h))} died at ${Math.floor(r.died.age)}, ${esc(r.died.how)}.</div>` : ""}
    <div class="muted center">${r.own} moments left to them · ${r.forced} pushed by you${r.forced ? ` (${esc(pushesSaid(r))})` : ""} · ended as ${esc(r.final)}</div>
    ${bookNews(h.book)}
    <div class="center rvb"><button class="ghost" id="rvBook">${ic("ci-bookshelf")} Open the Book</button><button class="primary" id="again">${ic("new")} A new life</button></div>`;
  $("rvBook").addEventListener("click", openBook);
  reviewEl.querySelectorAll(".gauge").forEach((g) => setTip(g, () => tipBox(g.querySelector("span").textContent, "", [], g.dataset.help)));
  $("again").addEventListener("click", () => send(""));
  autoKey = ""; try { localStorage.removeItem("chroma.autosave"); } catch (_) {}
  if (h.world && worker && ready) worker.postMessage({ cmd: "world_out" });
}

