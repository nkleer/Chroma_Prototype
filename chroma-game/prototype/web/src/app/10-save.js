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

