"""Release check for the Engine's speed pass (Emren 10-08 13:09: "check engine speed pass"): a faster engine must live
exactly the same lives as the live v22 engine, and be measurably faster.

For each seed and world setting, the base engine (default the frozen live v22 engine, chroma-engine/archive/live-v22)
and the new engine run the same lives on the same Library and packs (the live ones by default), each in its own
process, and every output they both return must be equal (arrays bit for bit, NaN equal to NaN). CPU time
(time.process_time) of each run gives the speed-up. Both engines are copied (top-level .py files and earth_rules) to a
scratch folder first and run with -B, so nothing is written in the shared folder except the report.

    python3 -B chroma-release/check_speedpass.py --new DIR [--base DIR] [--lib DIR] [--packs DIR] [--seeds 5,21,57]
        [--lives 40] [--years 80] [--worlds off,on,seed] [--timing 100] [--jobs 4] [--Pnew JSON] [--Pbase JSON]
        [--new-lib DIR] [--new-packs DIR] [--game DIR] [--base-game DIR] [--games 1,2,3,4,5,6] [--gseed 7]

  --new     the speed-pass engine folder.
  --worlds  off and on: the Earth batch with the live packs, outer world off or on (the live game plays Earth with it on);
            seed: the engine's own seed library, as v22's tribal and magic lives play.
  --Pnew    switch overrides for the new engine as JSON (for example the v23 switch set off), applied after DEFAULT.
  --new-lib, --new-packs  the Library and packs the new engine runs on, when a candidate brings its own (default --lib
            and --packs, which the base engine always runs on): then a Library or packs change that moves the lives
            shows too.
  --timing  lives in the separate timing runs (one per engine and world setting, seed 5, same years); 0 skips them.
  --games   presets the game plays (1 to 6, default all; "" skips): a copy of the live game (chroma-game/prototype) runs
            each preset's whole life through its own console, as the page does, once with its engine_pin/ filled from
            --base, --lib and --packs and once from --new, --new-lib and --new-packs, by chroma-game/tools/pin.py as the game
            fills it (gamepin.py; link.py must still find its six pause anchors; explain.py and foresee.py read the
            loop's locals). Picks come from a seeded stream (half the moments the character's own pick, half a numbered
            option); every text the console returns and the HUD at every moment must be equal.
  --game    the game folder the new engine plays in (default the live game); --base-game the one the base engine plays
            in (default --game). For a build with a game speed pass: --base-game chroma-game/prototype --game <build>.
  The base side is kept (step 4 of chroma-env/plan-by-function-2026-10-18.md): each engine run of the base leaves a
  digest of every output it returns in the cache ($CHROMA_SPEEDPASS_CACHE, else /mnt/project-files/.cache/speedpass when
  the shared folder exists, else ~/.cache/chroma/speedpass), keyed by what that run reads and how it runs: the base
  engine's .py files, the Library's top-level files and the packs' files one folder down (*.md aside), the seed, world,
  lives, years and switches, the CHROMA_, PACK_ and TIER_ environment, this script's worker and digest code, and Python's
  and numpy's versions. The live engine changes only at a publish, so a same-lives part then runs the new engine alone,
  about half the time. Only values equal under the comparison below hash alike, so a new run that matches the kept
  digests is identical; one that does not runs the base again and is compared in full, as before, and a base that then
  does not give its kept digests fails the check (the key missed an input). Timing runs and game lives always run both.
  --fresh      run the base again even when it is kept (the new digests are kept); --cache DIR: another cache folder.
  --base-only  run and keep the base side only (no --new, nothing compared, no result line), for the proofs after it.
Exit code 0 when every compared run is identical. Report: chroma-release/out/speedpass_<UTC time>.txt."""
import sys, os, argparse, json, time, pickle, shutil, subprocess, tempfile, glob, hashlib, platform

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
ap.add_argument("--new", default=None)
ap.add_argument("--base", default=P["engine_live"])
ap.add_argument("--lib", default=P["library_live"])
ap.add_argument("--packs", default=P["packs_live"])
ap.add_argument("--new-lib", default=None, help="the Library the new engine runs on (default --lib): a candidate's own")
ap.add_argument("--new-packs", default=None, help="the packs the new engine runs on (default --packs)")
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
ap.add_argument("--fresh", action="store_true", help="run the base again even when the cache keeps its side")
ap.add_argument("--base-only", action="store_true", help="run and keep the base side only, for the proofs after it")
ap.add_argument("--cache", default=None, help="the cache folder (default $CHROMA_SPEEDPASS_CACHE, else the shared folder's .cache/speedpass)")
a = ap.parse_args()
if a.base_only:
    a.new, a.games, a.timing = a.new or a.base, "", 0
elif not a.new:
    ap.error("--new is needed (or --base-only)")

os.makedirs(P["release_out"], exist_ok=True)
ap2 = a.tag if a.tag else ("s" + a.seeds.replace(",", "-") if a.seeds else "games")
REPORT = path("release_out", time.strftime("speedpass_%Y%m%d-%H%M%S", time.gmtime()) + f"_{ap2}.txt")
rep = open(REPORT, "w")


def say(s=""):
    print(s); rep.write(s + "\n"); rep.flush()


work = a.scratch or tempfile.mkdtemp(prefix="speedpass_")
copies = {}
for tag, src in (("base", a.base), ("new", a.new)):
    d = os.path.join(work, tag); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)   # a reused --scratch: no earlier engine's files
    for f in glob.glob(os.path.join(os.path.abspath(src), "*.py")):
        shutil.copy(f, d)
    copies[tag] = d
md5 = lambda p: __import__("hashlib").md5(open(p, "rb").read()).hexdigest()[:12]
games = [x for x in a.games.split(",") if x.strip()]
gcopies, gnotes = {}, []
NLIB, NPACKS = a.new_lib or a.lib, a.new_packs or a.packs
if games:
    import gamepin
    trees = [os.path.dirname(os.path.dirname(os.path.abspath(g))) for g in (a.game, a.base_game) if g]   # where pin.py is
    for tag in ("base", "new"):
        gsrc = (a.base_game or a.game) if tag == "base" else a.game
        lb, pk = (a.lib, a.packs) if tag == "base" else (NLIB, NPACKS)
        gd = gamepin.copy(gsrc, os.path.join(work, "game_" + tag), also=trees, engine=copies[tag], lib=lb, packs=pk)
        gcopies[tag] = gd; gnotes.append(f"  game {tag}: {gsrc} (game.py {md5(os.path.join(gd, 'game.py'))}) with engine_pin filled "
                                         f"from {tag} (engine.py {md5(os.path.join(gd, 'engine_pin', 'engine.py'))}), Library {lb}, packs {pk}")
say(f"Speed pass check, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
say(f"  base {a.base} (engine.py {md5(os.path.join(copies['base'], 'engine.py'))}, {len(os.listdir(copies['base']))} files)")
say("  new  none (--base-only: the base side is run and kept, nothing is compared)" if a.base_only else
    f"  new  {a.new} (engine.py {md5(os.path.join(copies['new'], 'engine.py'))}, {len(os.listdir(copies['new']))} files)")
say(f"  Library {a.lib}, packs {a.packs}" + (f"; new on Library {NLIB}, packs {NPACKS}" if (NLIB, NPACKS) != (a.lib, a.packs) else "")
    + f"; {a.lives} lives x {a.years} years, seeds {a.seeds}, worlds {a.worlds}; "
    f"P new {a.Pnew}, P base {a.Pbase}")
for x in gnotes:
    say(x)

jobs = []   # (label, tag, seed, world, N, out path)
for sd in [x for x in a.seeds.split(",") if x]:          # --seeds "": the game lives only
    for w in [x for x in a.worlds.split(",") if x]:
        for tag in ("base",) if a.base_only else ("base", "new"):
            jobs.append((f"id-{sd}-{w}", tag, sd, w, a.lives, os.path.join(work, f"id_{sd}_{w}_{tag}.pkl")))
if a.timing:
    for w in [x for x in a.worlds.split(",") if x]:
        for tag in ("base", "new"):
            jobs.append((f"time-{w}", tag, "5", w, a.timing, os.path.join(work, f"time_{w}_{tag}.pkl")))
for g in games:
    for tag in ("base", "new"):
        jobs.append((f"game-{g}", tag, g, "game", 0, os.path.join(work, f"game_{g}_{tag}.pkl")))
CACHE = a.cache or os.environ.get("CHROMA_SPEEDPASS_CACHE") or (
    "/mnt/project-files/.cache/speedpass" if os.path.isdir("/mnt/project-files") else os.path.expanduser("~/.cache/chroma/speedpass"))
CACHE_FORM = "speedpass base side 1"   # a new form of entry or digest: a new number, so no old entry is read
ENV_FREE = ("CHROMA_COMMIT", "CHROMA_ROOT", "CHROMA_PROJECT", "CHROMA_WORLD_CACHE", "CHROMA_CACHE", "CHROMA_SPEEDPASS_CACHE",
            "CHROMA_PROOF_CACHE", "CHROMA_ENGINE_DIR", "CHROMA_LIBRARY_DIR", "CHROMA_PACKS_DIR")
# ENV_FREE: where things are and where caches live (the worker is given its folders); every other CHROMA_, PACK_, TIER_ value is in the key
load = lambda p: pickle.load(open(p, "rb")) if os.path.exists(p) else None


def canon(x, h):
    """Feed x to the hash h so that two values that hash alike are equal under diff() below (the reverse need not hold:
    a float32 and a float64 array of the same numbers hash apart, and the base then runs again)."""
    if isinstance(x, dict):
        h.update(b"D%d;" % len(x))
        for k in sorted(x, key=str):
            canon(k, h); canon(x[k], h)
        return
    if x is None:
        h.update(b"N;"); return
    if isinstance(x, (list, tuple)) and not (len(x) and isinstance(x[0], (int, float, np.number))):
        h.update(b"L%d;" % len(x))
        for u in x:
            canon(u, h)
        return
    try:
        ax = np.asarray(x)
    except Exception:
        h.update(b"P" + pickle.dumps(x) + b";"); return
    if ax.dtype == object:
        h.update(b"O" + pickle.dumps(x) + b";"); return
    body = np.ascontiguousarray(ax).reshape(-1)
    if ax.dtype.kind in "fc":                       # NaN equals NaN and -0.0 equals 0.0 in diff(), so they hash alike
        body = body.copy()
        f = body.view(body.real.dtype) if ax.dtype.kind == "c" else body
        f[np.isnan(f)] = np.nan; f[f == 0] = 0
    h.update(b"A" + ax.dtype.str.encode() + repr(ax.shape).encode() + b";" + body.tobytes())


def digests(o):
    """{output: digest} of one engine run's outputs."""
    out = {}
    for k, v in o.items():
        h = hashlib.sha256(); canon(v, h); out[k if isinstance(k, str) else repr(k)] = h.hexdigest()[:24]
    return out


_sig = {}


def files_sig(d, deep):
    """A hash over the names and contents of the files in folder d that a run can read (*.md and caches aside); deep: those
    one folder down too (the packs: core/ and each pack's own folder)."""
    d = os.path.abspath(d)
    if (d, deep) not in _sig:
        h = hashlib.sha256()

        def walk(p, rel, down):
            for f in sorted(os.listdir(p)):
                q = os.path.join(p, f)
                if os.path.isfile(q) and not f.endswith((".md", ".pyc")):
                    h.update(f"{rel}{f}\0".encode()); h.update(hashlib.sha256(open(q, "rb").read()).digest())
                elif down and os.path.isdir(q) and f != "__pycache__":
                    walk(q, rel + f + "/", False)
        walk(d, "", deep)
        _sig[(d, deep)] = h.hexdigest()
    return _sig[(d, deep)]


def base_key(sd, w, N):
    import inspect
    env_ = {k: v for k, v in sorted(os.environ.items()) if k.startswith(("CHROMA_", "PACK_", "TIER_")) and k not in ENV_FREE}
    parts = [CACHE_FORM, files_sig(copies["base"], False), files_sig(a.lib, False), files_sig(a.packs, True), str(sd), w, str(N),
             str(a.years), json.dumps(json.loads(a.Pbase), sort_keys=True), json.dumps(env_), inspect.getsource(worker),
             inspect.getsource(canon), platform.python_version(), np.__version__]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:32]


def cache_get(key):
    try:
        e = json.load(open(os.path.join(CACHE, key + ".json")))
        return e if e.get("key") == key else None
    except (OSError, ValueError):
        return None


def keep(j):
    """The base engine run j has run: its digests go into the cache (written whole, then moved into place)."""
    b = load(j[5])
    if b is None:
        return None
    e = dict(key=base_key(j[2], j[3], j[4]), digests=digests(b["out"]), outputs=len(b["out"]), dropped=b["dropped"], cpu=b["cpu"],
             engine_md5=b["engine_md5"], made=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), host=platform.node(),
             base=os.path.abspath(a.base), lib=os.path.abspath(a.lib), packs=os.path.abspath(a.packs), seed=j[2], world=j[3],
             lives=j[4], years=a.years, P=a.Pbase, commit=os.environ.get("CHROMA_COMMIT", ""))
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, e["key"] + ".json"); tmp = f"{p}.{os.getpid()}.tmp"
    with open(tmp, "w") as f:
        json.dump(e, f)
    os.replace(tmp, p)
    return e


engine_runs = [j for j in jobs if j[1] == "base" and j[0].startswith("id-")]
cached = {} if a.fresh else {j[0]: e for j in engine_runs for e in [cache_get(base_key(j[2], j[3], j[4]))] if e}
if engine_runs:
    say(f"  base side kept for {len(cached)} of {len(engine_runs)} engine runs" + (" (--fresh: run again)" if a.fresh else "")
        + f"; cache {CACHE}")
env = dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
failed = []


def run(todo):
    running = []
    while todo or running:
        while todo and len(running) < a.jobs:
            lab, tag, sd, w, N, out = todo.pop(0)
            P = a.Pnew if tag == "new" else a.Pbase
            if os.path.exists(out):                         # a reused --scratch: never an earlier run's output in its place
                os.remove(out)
            if w == "game":
                cmd = [sys.executable, "-B", os.path.abspath(__file__), "--gworker", gcopies[tag], sd, a.gseed, P, out]; cwd = gcopies[tag]
            else:
                cmd = [sys.executable, "-B", os.path.abspath(__file__), "--worker", copies[tag], os.path.abspath(NLIB if tag == "new" else a.lib),
                       os.path.abspath(NPACKS if tag == "new" else a.packs), sd, w, str(N), str(a.years), P, out]; cwd = work
            p = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            running.append((p, lab, tag, out))
        time.sleep(2)
        for r in list(running):
            if r[0].poll() is not None:
                running.remove(r)
                if r[0].returncode != 0:
                    failed.append(r[1] + "/" + r[2]); say(f"MISS run {r[1]} {r[2]} failed: {r[0].stdout.read().decode()[-600:]}")


run([j for j in jobs if not (j[1] == "base" and j[0] in cached)])
for j in engine_runs:
    if j[0] not in cached and j[0] + "/base" not in failed:
        keep(j)
if a.base_only:
    say(f"Base side: {'FAIL' if failed else 'kept'} ({len(engine_runs) - len(cached)} run, {len(cached)} already kept)")
    say(f"report: {REPORT}; scratch {work}")
    sys.exit(1 if failed else 0)
matched, again = {}, []   # labels whose new run equals the kept base side by digest; base runs to do after all
for lab, e in cached.items():
    n = load(next(j[5] for j in jobs if j[0] == lab and j[1] == "new"))
    if n is not None and digests(n["out"]) == e["digests"]:
        matched[lab] = (e, dict(cpu=n["cpu"], outputs=len(n["out"]), dropped=n["dropped"]))
    elif n is not None:
        again.append(next(j for j in engine_runs if j[0] == lab))
if again:
    say(f"  {len(again)} new run(s) differ from the kept base side: running the base again to compare in full")
    run(list(again))
    for j in again:
        e = keep(j) if j[0] + "/base" not in failed else None
        if e and e["digests"] != cached[j[0]]["digests"]:
            failed.append(j[0] + "/cache")
            say(f"MISS {j[0]}: the base run again does not give its kept digests (kept {cached[j[0]]['made']} on "
                f"{cached[j[0]]['host']}): the cache key misses an input, so a proof that matched this entry proves nothing")

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


ok = not failed; cpu = {}
for lab in dict.fromkeys(j[0] for j in jobs):
    if lab in matched:
        e, n = matched[lab]
        cpu[lab] = (e["cpu"], n["cpu"])
        say(f"ok   {lab}: base {e['cpu']:.0f} s (kept {e['made']} on {e['host']}), new {n['cpu']:.0f} s CPU "
            f"({e['cpu'] / max(n['cpu'], 1e-9):.2f}x faster): identical ({n['outputs']} outputs compared by digest)")
        dropped = sorted(set(e["dropped"]) | set(n["dropped"]))
        if dropped:
            say(f"       not compared (not picklable): {', '.join(dropped)}")
        continue
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
import results; results.done('speedpass' + ('_' + a.tag if a.tag else ''), 0 if ok else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
