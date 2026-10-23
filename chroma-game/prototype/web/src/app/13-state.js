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
  if (!agendaEl.hidden && !busy) { if (hud.life && hud.life.agenda) openAgenda(agFocus); else closeAgenda(); }   // v25: the agenda follows the life
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
  if (!agendaEl.hidden) { if (e.key === "Escape" || e.key === "j") closeAgenda(); return; }
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
  if (e.key === "j" && hud.life && hud.life.agenda) { if (agendaEl.hidden) openAgenda(); else closeAgenda(); return; }
  if (["i", "c", "b", "s", "o", "n", "a"].includes(e.key) || (e.key === "g" && (hud.world || (hud.life && hud.life.world_era)))) { pageKey(e.key); return; }
  if (["f", "v", "l", "p", "k"].includes(e.key)) send(e.key);
  if (e.key === "x" && hud.plan) send("x");
});

function fatal(msg) {
  app.dataset.mode = "boot";
  screenEl.innerHTML = `<div class="boot"><div class="hero"><h1>CHROMA</h1></div><p>Could not start: ${esc(msg)}</p><p>This page runs the real engine (Python and numpy) inside your browser with WebAssembly. If the browser or this viewer blocks that, the same game runs in a terminal: python3 play.py in the project's chroma-game/prototype folder (needs Python 3 and numpy).</p></div>`;
}
stageEl.classList.remove("paper");
// the life choice screen waits for the engine: until Python, numpy and the game's files have loaded (about 16 MB the
// first time), only the loading screen shows (Emren 2026-10-11: "Do not load life choice screen before loading" them)
screenEl.innerHTML = `<div class="boot"><div class="hero"><h1>CHROMA</h1><div class="pips">${COLORS.map((c) => pip(c)).join("")}</div><p>One life. Five colors. You are the voice in their head.</p></div><span class="spin"></span><span id="bootMsg">Loading Python and numpy in your browser (about 16 MB the first time)…</span><span class="bootbar"><i></i></span></div>`;
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
