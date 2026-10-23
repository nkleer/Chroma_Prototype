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
const SOURCES = ["engine_pin/engine.py", "engine_pin/library.py", "engine_pin/combos.py", "engine_pin/batch.py", "engine_pin/earth_rules.py", "engine_pin/earth.py", "engine_pin/earth_perks_titles.py", "engine_pin/earth_science.py", "engine_pin/earth_politics.py", "engine_pin/earth_stage.py", "engine_pin/dreams.py", "engine_pin/worlds.py", "engine_pin/earth_age_fit.py", "engine_pin/earth_story.py", "engine_pin/earth_play.py", "engine_pin/packs/core/reach.py", "engine_pin/packs/core/longshot.py", "engine_pin/packs/science/catalogue.py", "engine_pin/packs/science/roles.py", "engine_pin/packs/science/helps.py", "engine_pin/packs/politics/catalogue.py", "engine_pin/packs/politics/roles.py", "engine_pin/packs/politics/helps.py", "engine_pin/packs/stage/catalogue.py", "engine_pin/packs/stage/roles.py", "engine_pin/packs/stage/helps.py", "engine_pin/world_keys.py", "engine_pin/world.py", "engine_pin/world_link.py", "engine_pin/world_people.py", "engine_pin/sphere_data.py", "engine_pin/sphere_ev_base.py", "engine_pin/earth_spheres.py", "engine_pin/packs/art/catalogue.py", "engine_pin/packs/art/roles.py", "engine_pin/packs/art/helps.py", "engine_pin/earth_art.py", "engine_pin/world_base.py", "engine_pin/world_events.py", "engine_pin/world_hooks.py", "engine_pin/world_people_acts.py", "engine_pin/world_people_base.py", "engine_pin/world_people_eyes.py", "engine_pin/world_people_lead.py", "engine_pin/world_people_answers.py", "engine_pin/world_people_lives.py", "engine_pin/world_people_roster.py", "engine_pin/world_people_sacred.py", "engine_pin/world_people_settings.py", "engine_pin/world_people_ticks.py", "engine_pin/world_people_views.py", "engine_pin/world_society.py", "engine_pin/world_spheres.py", "engine_pin/world_years.py", "engine_pin/world_link_base.py", "engine_pin/world_link_life.py", "engine_pin/world_link_rates.py", "engine_pin/world_link_week.py", "engine_pin/parts.py", "engine_pin/rules_art.py", "engine_pin/rules_chance.py", "engine_pin/rules_drivers.py", "engine_pin/rules_moments.py", "engine_pin/rules_more.py", "engine_pin/rules_norms.py", "engine_pin/rules_packs.py", "engine_pin/rules_perks.py", "engine_pin/rules_titles.py", "engine_pin/rules_world.py", "engine_pin/run_01_start.py", "engine_pin/run_02_goals.py", "engine_pin/run_03_moments.py", "engine_pin/run_04_titles.py", "engine_pin/run_05_conditions.py", "engine_pin/run_06_world.py", "engine_pin/run_07_body.py", "engine_pin/run_08_fixes.py", "engine_pin/run_09_week.py", "engine_pin/run_10_situation.py", "engine_pin/run_11_choice.py", "engine_pin/run_12_commitments.py", "engine_pin/run_13_learning.py", "engine_pin/run_14_marks.py", "engine_pin/run_15_titles.py", "engine_pin/run_16_world.py", "engine_pin/run_17_inner.py", "engine_pin/run_18_integrate.py", "engine_pin/realm_earth.py", "engine_pin/earth_foot.py", "engine_pin/earth_science_foot.py", "engine_pin/earth_politics_foot.py", "engine_pin/earth_stage_foot.py", "engine_pin/earth_art_foot.py", "engine_pin/earth_aims.py", "engine_pin/earth_aim_moments.py", "engine_pin/earth_aim_moments_foot.py", "engine_pin/earth_world_answers.py", "engine_pin/earth_world_answers_foot.py", "engine_pin/earth_world_lines.py", "engine_pin/footprint_names.py", "engine_pin/packs/science/aims.py", "engine_pin/packs/politics/aims.py", "engine_pin/packs/stage/aims.py", "engine_pin/packs/art/aims.py", "engine_pin/rules_callings.py", "engine_pin/earth_callings.py", "engine_pin/earth_callings_foot.py", "engine_pin/packs/callings/catalogue.py", "engine_pin/packs/callings/roles.py", "engine_pin/packs/callings/helps.py", "engine_pin/packs/callings/aims.py", "engine_pin/world_fit.py", "engine_pin/world_land.py", "engine_pin/world_national.py", "engine_pin/realm_neutral.py", "engine_pin/earth_aim_lines.py", "engine_pin/earth_react_lines.py", "engine_pin/earth_nature.py", "engine_pin/earth_nature_foot.py", "engine_pin/earth_national.py", "engine_pin/earth_national_foot.py", "engine_pin/foresee.py", "engine_pin/explain.py", "link.py", "story_text.py", "story_base.py", "story_cast.py", "story_moments.py", "story_lines.py", "story_goals.py", "story.py", "worldview.py", "routine_text.py", "routine.py", "rarity.py", "game_base.py", "game_words.py", "game_checkpoints.py", "game_world.py", "game_voice.py", "game_life.py", "game_views.py", "game_causes.py", "game_bold.py", "game_because.py", "game_foot.py", "game_aims.py", "game_agenda.py", "game_prizes.py", "game_clash.py", "game_land.py", "game_asks.py", "game_world_answers.py", "game.py", "console.py"];
// CODE_PARTS: the web folder's build (tools/webdir.py) packs SOURCES into this many py/code-<n>.json files ({path: text}),
// so one published version needs a few entries for the code, not one per file (the artifact holds at most 511 files).
// 0 (this folder as committed) reads each file from py/ as before.
const CODE_PARTS = 0;
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
    sys("Loading numpy…");
    await py.loadPackage(here("pyodide/numpy-2.0.2-cp312-cp312-pyodide_2024_0_wasm32.whl"));
    py.FS.mkdirTree("/home/pyodide/chroma/engine_pin");
    sys("Loading the game's files…");
    const code = {};
    for (let n = 1; n <= CODE_PARTS; n++) {
      const r = await fetch(here("py/code-" + n + ".json"));
      if (!r.ok) throw new Error("could not load code part " + n + " (" + r.status + ")");
      Object.assign(code, await r.json());
    }
    for (const f of SOURCES) {
      let text = code[f];
      if (text === undefined) {
        const r = await fetch(here("py/" + f));
        if (!r.ok) throw new Error("could not load " + f + " (" + r.status + ")");
        text = await r.text();
      }
      const d = ("/home/pyodide/chroma/" + f).replace(/\/[^/]*$/, "");
      py.FS.mkdirTree(d);                                   // engine_pin/packs/<pack>/ for the content packs
      py.FS.writeFile("/home/pyodide/chroma/" + f, text);
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
