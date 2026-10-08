"""Release check for the Engine's speed pass (Emren 10-08 13:09: "check engine speed pass"): a faster engine must live
exactly the same lives as the live v22 engine, and be measurably faster.

For each seed and world setting, the base engine (default the frozen live v22 engine, chroma-engine/archive/live-v22)
and the new engine run the same lives on the same Library and packs (the live ones by default), each in its own
process, and every output they both return must be equal (arrays bit for bit, NaN equal to NaN). CPU time
(time.process_time) of each run gives the speed-up. Both engines are copied (top-level .py files and earth_rules) to a
scratch folder first and run with -B, so nothing is written in the shared folder except the report.

    python3 -B chroma-release/check_speedpass.py --new DIR [--base DIR] [--lib DIR] [--packs DIR] [--seeds 5,21,57]
        [--lives 40] [--years 80] [--worlds off,on,seed] [--timing 100] [--jobs 4] [--Pnew JSON] [--Pbase JSON]
        [--game DIR] [--base-game DIR] [--games 1,2,3,4,5,6] [--gseed 7]

  --new     the speed-pass engine folder.
  --worlds  off and on: the Earth batch with the live packs, outer world off or on (the live game plays Earth with it on);
            seed: the engine's own seed library, as v22's tribal and magic lives play.
  --Pnew    switch overrides for the new engine as JSON (for example the v23 switch set off), applied after DEFAULT.
  --timing  lives in the separate timing runs (one per engine and world setting, seed 5, same years); 0 skips them.
  --games   presets the game plays (1 to 6, default all; "" skips): a copy of the live game (chroma-game/prototype) runs
            each preset's whole life through its own console, as the page does, once with engine_pin's engine files from
            --base and once from --new (link.py must still find its six pause anchors; explain.py and foresee.py read the
            loop's locals). Picks come from a seeded stream (half the moments the character's own pick, half a numbered
            option); every text the console returns and the HUD at every moment must be equal.
  --game    the game folder the new engine plays in (default the live game); --base-game the one the base engine plays
            in (default --game). For a build with a game speed pass: --base-game chroma-game/prototype --game <build>.
Exit code 0 when every compared run is identical. Report: chroma-release/out/speedpass_<UTC time>.txt."""
import sys, os, argparse, json, time, pickle, shutil, subprocess, tempfile, glob

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py


def worker(argv):
    eng, lib, packs, seed, world, N, Y, Pjson, out = argv
    sys.path.insert(0, eng)
    import numpy as np  # noqa: F401
    import engine as E, batch
    batch.LIB_DIR = lib; batch.PACK_DIR = packs
    L = None if world == "seed" else batch.load_batch("earth", packs=list(batch.PACKS))   # seed: the engine's own 24, as tribal and magic lives
    P = dict(E.DEFAULT); P.update(json.loads(Pjson)); P["world"] = (world == "on")
    t0 = time.process_time()
    o = E.run(N=int(N), years=int(Y), seed=int(seed), lib=L, P=P)
    dt = time.process_time() - t0
    keep, dropped = {}, []
    for k, v in o.items():
        try:
            pickle.dumps(v); keep[k] = v
        except Exception:
            dropped.append(k)
    with open(out, "wb") as f:
        pickle.dump({"out": keep, "dropped": dropped, "cpu": dt, "engine_md5": __import__("hashlib").md5(
            open(os.path.join(eng, "engine.py"), "rb").read()).hexdigest()[:12]}, f)


def gworker(argv):
    """One whole life in the game copy gdir (cwd), preset `preset`, every console text and every moment's HUD."""
    gdir, preset, seed, Pjson, out = argv
    import random, json as J
    sys.path.insert(0, gdir)
    t0 = time.process_time()
    import link
    link.E.DEFAULT.update(J.loads(Pjson))
    from console import Console
    random.seed(int(seed) * 100 + int(preset))
    pick = random.Random(int(seed) * 1000 + int(preset))
    rec = []
    c = Console()

    def send(x):
        text, busy = c.handle(x); k = 0
        while busy and k < 100000:
            t2, busy = c.handle(""); text += t2; k += 1
        rec.append(("text", x, text))

    send(""); send(str(preset)); send("")
    n = cps = 0
    while c.mode == "play" and n < 6000:
        n += 1
        if c.g.pending is not None:
            cps += 1
            rec.append(("hud", "", J.dumps(c.hud(), sort_keys=True, default=str)))
            nums = sorted(c.numbering)
            send(str(pick.choice(nums)) if nums and pick.random() < 0.5 else "")
        else:
            send("")
    rec.append(("end", c.mode, J.dumps(getattr(c.g, "review", None), sort_keys=True, default=str)))
    with open(out, "wb") as f:
        pickle.dump({"rec": rec, "moments": cps, "steps": n, "mode": c.mode, "age": round(float(c.g.age()), 1),
                     "cpu": time.process_time() - t0}, f)


if len(sys.argv) > 1 and sys.argv[1] == "--worker":
    worker(sys.argv[2:]); sys.exit(0)
if len(sys.argv) > 1 and sys.argv[1] == "--gworker":
    gworker(sys.argv[2:]); sys.exit(0)

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--new", required=True)
ap.add_argument("--base", default=P["engine_live"])
ap.add_argument("--lib", default=P["library_live"])
ap.add_argument("--packs", default=P["packs_live"])
ap.add_argument("--seeds", default="5,21,57")
ap.add_argument("--lives", type=int, default=40)
ap.add_argument("--years", type=int, default=80)
ap.add_argument("--worlds", default="off,on,seed")
ap.add_argument("--timing", type=int, default=100)
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--Pnew", default="{}")
ap.add_argument("--Pbase", default="{}")
ap.add_argument("--scratch", default=None)
ap.add_argument("--tag", default="", help="added to the report's name (default the seeds), so runs on several machines never share one")
ap.add_argument("--game", default=P["game_live"])
ap.add_argument("--base-game", default=None)
ap.add_argument("--games", default="1,2,3,4,5,6")
ap.add_argument("--gseed", default="7")
a = ap.parse_args()

os.makedirs(P["release_out"], exist_ok=True)
ap2 = a.tag if a.tag else ("s" + a.seeds.replace(",", "-") if a.seeds else "games")
REPORT = path("release_out", time.strftime("speedpass_%Y%m%d-%H%M%S", time.gmtime()) + f"_{ap2}.txt")
rep = open(REPORT, "w")


def say(s=""):
    print(s); rep.write(s + "\n"); rep.flush()


work = a.scratch or tempfile.mkdtemp(prefix="speedpass_")
copies = {}
for tag, src in (("base", a.base), ("new", a.new)):
    d = os.path.join(work, tag); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(os.path.abspath(src), "*.py")):
        shutil.copy(f, d)
    copies[tag] = d
md5 = lambda p: __import__("hashlib").md5(open(p, "rb").read()).hexdigest()[:12]
games = [x for x in a.games.split(",") if x.strip()]
gcopies, gnotes = {}, []
if games:
    import ast
    for tag in ("base", "new"):
        gd = os.path.join(work, "game_" + tag)
        shutil.rmtree(gd, ignore_errors=True)
        gsrc = (a.base_game or a.game) if tag == "base" else a.game
        shutil.copytree(os.path.abspath(gsrc), gd, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "web", "test"))
        pin = os.path.join(gd, "engine_pin"); eng = copies[tag]
        tree = ast.parse(open(os.path.join(eng, "engine.py")).read())
        imported = {n.name.split(".")[0] for nd in ast.walk(tree) if isinstance(nd, ast.Import) for n in nd.names} | \
                   {nd.module.split(".")[0] for nd in ast.walk(tree) if isinstance(nd, ast.ImportFrom) and nd.module}
        put = []
        for f in sorted(os.listdir(eng)):
            if f.endswith(".py") and (os.path.exists(os.path.join(pin, f)) or f[:-3] in imported):
                shutil.copy(os.path.join(eng, f), pin); put.append(f)
        gcopies[tag] = gd; gnotes.append(f"  game {tag}: {gsrc} (game.py {md5(os.path.join(gd, 'game.py'))}) with engine_pin's "
                                         f"{', '.join(put)} from {tag}")
say(f"Speed pass check, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
say(f"  base {a.base} (engine.py {md5(os.path.join(copies['base'], 'engine.py'))}, {len(os.listdir(copies['base']))} files)")
say(f"  new  {a.new} (engine.py {md5(os.path.join(copies['new'], 'engine.py'))}, {len(os.listdir(copies['new']))} files)")
say(f"  Library {a.lib}, packs {a.packs}; {a.lives} lives x {a.years} years, seeds {a.seeds}, worlds {a.worlds}; "
    f"P new {a.Pnew}, P base {a.Pbase}")
for x in gnotes:
    say(x)

jobs = []   # (label, tag, seed, world, N, out path)
for sd in [x for x in a.seeds.split(",") if x]:          # --seeds "": the game lives only
    for w in [x for x in a.worlds.split(",") if x]:
        for tag in ("base", "new"):
            jobs.append((f"id-{sd}-{w}", tag, sd, w, a.lives, os.path.join(work, f"id_{sd}_{w}_{tag}.pkl")))
if a.timing:
    for w in [x for x in a.worlds.split(",") if x]:
        for tag in ("base", "new"):
            jobs.append((f"time-{w}", tag, "5", w, a.timing, os.path.join(work, f"time_{w}_{tag}.pkl")))
for g in games:
    for tag in ("base", "new"):
        jobs.append((f"game-{g}", tag, g, "game", 0, os.path.join(work, f"game_{g}_{tag}.pkl")))
env = dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
running, todo, failed = [], list(jobs), []
while todo or running:
    while todo and len(running) < a.jobs:
        lab, tag, sd, w, N, out = todo.pop(0)
        P = a.Pnew if tag == "new" else a.Pbase
        if w == "game":
            cmd = [sys.executable, "-B", os.path.abspath(__file__), "--gworker", gcopies[tag], sd, a.gseed, P, out]; cwd = gcopies[tag]
        else:
            cmd = [sys.executable, "-B", os.path.abspath(__file__), "--worker", copies[tag], os.path.abspath(a.lib),
                   os.path.abspath(a.packs), sd, w, str(N), str(a.years), P, out]; cwd = work
        p = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        running.append((p, lab, tag, out))
    time.sleep(2)
    for r in list(running):
        if r[0].poll() is not None:
            running.remove(r)
            if r[0].returncode != 0:
                failed.append(r[1] + "/" + r[2]); say(f"MISS run {r[1]} {r[2]} failed: {r[0].stdout.read().decode()[-600:]}")

SKIP = set()


def diff(x, y, path, out):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y), key=str):
            if k not in x or k not in y:
                out.append((f"{path}.{k}" if path else str(k), "only one engine returns it")); continue
            diff(x[k], y[k], f"{path}.{k}" if path else str(k), out)
        return
    if x is None or y is None:
        if (x is None) != (y is None):
            out.append((path, "None in one engine only"))
        return
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and not (len(x) and isinstance(x[0], (int, float, np.number))):
        if len(x) != len(y):
            out.append((path, f"length {len(x)} vs {len(y)}")); return
        for i, (u, v) in enumerate(zip(x, y)):
            n0 = len(out); diff(u, v, f"{path}[{i}]", out)
            if len(out) > n0:
                return
        return
    try:
        ax, ay = np.asarray(x), np.asarray(y)
    except Exception:
        if x != y:
            out.append((path, "differs"))
        return
    if ax.dtype == object or ay.dtype == object:
        if pickle.dumps(x) != pickle.dumps(y) and repr(x) != repr(y):
            out.append((path, "differs"))
        return
    if ax.shape != ay.shape:
        out.append((path, f"shape {ax.shape} vs {ay.shape}")); return
    if ax.dtype.kind in "fcib" and ay.dtype.kind in "fcib":
        eq = (ax == ay) | (np.isnan(ax) & np.isnan(ay)) if ax.dtype.kind in "fc" else (ax == ay)
        if not np.all(eq):
            gap = float(np.nanmax(np.abs(ax.astype(float) - ay.astype(float))))
            out.append((path, f"largest gap {gap:.3g}, first at {np.argwhere(~eq)[0].tolist() if ax.ndim else []}"))
    elif not np.array_equal(ax, ay):
        out.append((path, "differs"))


load = lambda p: pickle.load(open(p, "rb")) if os.path.exists(p) else None
ok = not failed; cpu = {}
for lab in dict.fromkeys(j[0] for j in jobs):
    b = load(next(j[5] for j in jobs if j[0] == lab and j[1] == "base"))
    n = load(next(j[5] for j in jobs if j[0] == lab and j[1] == "new"))
    if b is None or n is None:
        ok = False; say(f"MISS {lab}: a run left no output"); continue
    if lab.startswith("game-"):
        cpu[lab] = (b["cpu"], n["cpu"])
        head = (f"{lab}: {b['moments']} moments, life ends {b['mode']} at {b['age']}; base {b['cpu']:.0f} s, new {n['cpu']:.0f} s "
                f"CPU ({b['cpu'] / max(n['cpu'], 1e-9):.2f}x faster)")
        first = next((i for i, (u, v) in enumerate(zip(b["rec"], n["rec"])) if u != v), None)
        if first is None and len(b["rec"]) == len(n["rec"]):
            say(f"ok   {head}: identical ({len(b['rec'])} texts and HUDs)")
        else:
            ok = False
            if first is None:
                say(f"MISS {head}: the same until one life stops ({len(b['rec'])} vs {len(n['rec'])} records)")
            else:
                u, v = b["rec"][first], n["rec"][first]
                k = next((j for j, (x, y) in enumerate(zip(u[2], v[2])) if x != y), min(len(u[2]), len(v[2])))
                say(f"MISS {head}: first difference at record {first} of {len(b['rec'])} ({u[0]} after {u[1]!r}), character {k}:")
                say(f"       base ...{u[2][max(0, k - 120):k + 160]!r}")
                say(f"       new  ...{v[2][max(0, k - 120):k + 160]!r}")
        continue
    cpu[lab] = (b["cpu"], n["cpu"])
    out = []; diff(n["out"], b["out"], "", out)
    dropped = sorted(set(b["dropped"]) | set(n["dropped"]))
    head = f"{lab}: base {b['cpu']:.0f} s, new {n['cpu']:.0f} s CPU ({b['cpu'] / max(n['cpu'], 1e-9):.2f}x faster)"
    if out:
        ok = False; say(f"MISS {head}: {len(out)} outputs differ")
        for p_, w_ in out[:20]:
            say(f"       {p_}: {w_}")
    else:
        say(f"ok   {head}: identical ({len(n['out'])} outputs compared)")
    if dropped:
        say(f"       not compared (not picklable): {', '.join(dropped)}")
tb = sum(v[0] for v in cpu.values()); tn = sum(v[1] for v in cpu.values())
say(f"All runs: base {tb:.0f} s, new {tn:.0f} s CPU: {tb / max(tn, 1e-9):.2f}x faster overall")
say("Speed pass: " + ("PASS (identical lives)" if ok else "FAIL"))
say(f"report: {REPORT}; scratch {work}")
import results; results.done('speedpass', 0 if ok else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
