// Runs the Chroma engine (Python + numpy, via Pyodide) off the page's main thread.
// Page -> worker: {cmd: "line", text} | {cmd: "stop"} | {cmd: "save"} | {cmd: "load", text} | {cmd: "world_in", text} | {cmd: "world_out"}
// Worker -> page: {kind: "state", text, busy, feed, hud} | {kind: "save", data} | {kind: "world", data} | {kind: "sys", text} | {kind: "fatal", msg}
// The artifact host serves no .zip or .whl files, so the Python standard library and the numpy wheel
// are published as base64 text (name + ".b64.txt"). This fetch shim turns them back into bytes.
const realFetch = self.fetch.bind(self);
self.fetch = async (input, init) => {
  const url = typeof input === "string" ? input : (input && input.url) || String(input);
  if (!/\.(zip|whl)$/.test(url)) return realFetch(input, init);
  const opts = Object.assign({}, init || {}); delete opts.integrity;
  const r = await realFetch(url + ".b64.txt", opts);
  if (!r.ok) return r;
  const bin = atob((await r.text()).replace(/\s+/g, ""));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new Response(bytes, { status: 200, headers: { "Content-Type": "application/octet-stream" } });
};
importScripts("pyodide/pyodide.js");

const here = (p) => new URL(p, self.location.href).href;
const SOURCES = ["engine_pin/engine.py", "engine_pin/library.py", "engine_pin/combos.py", "engine_pin/batch.py", "engine_pin/earth_rules.py", "engine_pin/earth.py", "engine_pin/earth_perks_titles.py", "engine_pin/earth_science.py", "engine_pin/earth_politics.py", "engine_pin/earth_stage.py", "engine_pin/dreams.py", "engine_pin/packs/core/reach.py", "engine_pin/packs/core/longshot.py", "engine_pin/packs/science/catalogue.py", "engine_pin/packs/science/roles.py", "engine_pin/packs/science/helps.py", "engine_pin/packs/politics/catalogue.py", "engine_pin/packs/politics/roles.py", "engine_pin/packs/politics/helps.py", "engine_pin/packs/stage/catalogue.py", "engine_pin/packs/stage/roles.py", "engine_pin/packs/stage/helps.py", "engine_pin/world_keys.py", "engine_pin/world.py", "engine_pin/world_link.py", "engine_pin/world_people.py", "engine_pin/foresee.py", "engine_pin/explain.py", "link.py", "story.py", "worldview.py", "routine.py", "rarity.py", "game.py", "console.py"];
const BRIDGE = `
import sys, os, json
import numpy as _np
os.chdir("/home/pyodide/chroma"); sys.path.insert(0, "/home/pyodide/chroma")
from console import Console
_c = Console()
def _dflt(o):
    if isinstance(o, _np.generic):
        return o.item()
    if isinstance(o, _np.ndarray):
        return o.tolist()
    return str(o)
def _pack(text, busy):
    return json.dumps([text, bool(busy), _c.take_feed(), _c.hud()], default=_dflt)
def step(line):
    text, busy = _c.handle(line)
    return _pack(text, busy)
def stop_job():
    _c.stop()
    return _pack("", False)
def save():
    return _c.save()
def load(text):
    out, busy = _c.load(text)
    return _pack(out, busy)
def start():
    return _pack(_c.start_text(), False)
def world_in(text):
    return _c.world_in(text)
def world_out():
    return _c.world_out()
`;

let py = null, running = false, stopAsked = false, loadNext = null;
const post = (m) => self.postMessage(m);
const sys = (text) => post({ kind: "sys", text });
const send = (packed) => {
  const [text, busy, feed, hud] = JSON.parse(packed);
  post({ kind: "state", text, busy, feed, hud });
  return busy;
};

function loop() {
  if (stopAsked) {
    stopAsked = false; running = false;
    send(py.runPython("stop_job()"));
    if (loadNext !== null) { const t = loadNext; loadNext = null; load(t); }
    return;
  }
  let busy;
  try { py.globals.set("_line", ""); busy = send(py.runPython("step(_line)")); }
  catch (e) { running = false; sys("[error] " + e.message); return; }
  if (busy) setTimeout(loop, 0); else running = false;
}

function run(text) {
  let busy;
  try { py.globals.set("_line", text); busy = send(py.runPython("step(_line)")); }
  catch (e) { sys("[error] " + e.message); return; }
  if (busy) { running = true; setTimeout(loop, 0); }
}

self.onmessage = (e) => {
  const m = e.data;
  if (!py) return;
  if (m.cmd === "stop") { if (running) stopAsked = true; return; }
  if (m.cmd === "line" && !running) run(m.text);
  if (m.cmd === "save") { try { post({ kind: "save", data: py.runPython("save()") }); } catch (e) { sys("[error] " + e.message); } }
  if (m.cmd === "world_in") { try { py.globals.set("_wtext", m.text || ""); py.runPython("world_in(_wtext)"); } catch (e) { sys("[error] " + e.message); } return; }
  if (m.cmd === "world_out") { try { post({ kind: "world", data: py.runPython("world_out()") }); } catch (e) { post({ kind: "world", data: "" }); } return; }
  if (m.cmd === "load") { if (running) { stopAsked = true; loadNext = m.text; } else load(m.text); }
};

function load(text) {
  let busy;
  try { py.globals.set("_text", text); busy = send(py.runPython("load(_text)")); }
  catch (e) { sys("[error] " + e.message); return; }
  if (busy) { running = true; setTimeout(loop, 0); }
}

(async () => {
  try {
    const t0 = performance.now();
    py = await loadPyodide({ indexURL: here("pyodide/") });
    await py.loadPackage(here("pyodide/numpy-2.0.2-cp312-cp312-pyodide_2024_0_wasm32.whl"));
    py.FS.mkdirTree("/home/pyodide/chroma/engine_pin");
    for (const f of SOURCES) {
      const r = await fetch(here("py/" + f));
      if (!r.ok) throw new Error("could not load " + f + " (" + r.status + ")");
      const d = ("/home/pyodide/chroma/" + f).replace(/\/[^/]*$/, "");
      py.FS.mkdirTree(d);                                   // engine_pin/packs/<pack>/ for the content packs
      py.FS.writeFile("/home/pyodide/chroma/" + f, await r.text());
    }
    sys("Loading the engine…");
    py.runPython(BRIDGE);
    sys(`Ready in ${((performance.now() - t0) / 1000).toFixed(0)} s.`);
    send(py.runPython("start()"));
  } catch (e) {
    py = null;
    post({ kind: "fatal", msg: (e && e.message) ? e.message : String(e) });
  }
})();
