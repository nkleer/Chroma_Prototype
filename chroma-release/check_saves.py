"""v22.1 row B3 (chroma-release/checklist-v22.1.md): lives saved on live v22 load in a new build into the same life.

A save is the life's setup (seed included) and the player's lines since (game console.py, Console.save); loading replays
them. For each preset, a copy of the live game plays a life with seeded picks up to a number of moments and saves it, as
the page does. Then the save is loaded twice in fresh consoles, once by the live game and once by the new build, and both
play on with the same seeded picks. The HUD right after the load and every text and moment HUD after it must be equal.
Both games are copied to a scratch folder first (no __pycache__ or saves land in the shared folder).

    python3 -B chroma-release/check_saves.py --new-game DIR [--base-game DIR] [--presets 1,2,3,4,5,6] [--moments 6]
        [--after 25] [--seed 7] [--jobs 4] [--scratch DIR]

  --new-game   the new build's game folder (its own engine_pin); --base-game: default the live game, chroma-game/prototype.
  --moments    moments played before saving; --after: steps played on after the load.
Exit code 0 when every preset loads into the same life. Report: chroma-release/out/saves_<UTC time>.txt."""
import sys, os, argparse, json, time, pickle, shutil, subprocess, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py


def play_on(c, pick, rec, steps, J):
    def send(x):
        text, busy = c.handle(x); k = 0
        while busy and k < 100000:
            t2, busy = c.handle(""); text += t2; k += 1
        rec.append(("text", x, text))
    n = 0
    while c.mode == "play" and n < steps:
        n += 1
        if c.g.pending is not None:
            rec.append(("hud", "", J.dumps(c.hud(), sort_keys=True, default=str)))
            nums = sorted(c.numbering)
            send(str(pick.choice(nums)) if nums and pick.random() < 0.5 else "")
        else:
            send("")
    return send


def worker(argv):
    gdir, mode, preset, seed, M, after, save, out = argv
    import random, json as J
    sys.path.insert(0, gdir)
    from console import Console
    random.seed(int(seed) * 100 + int(preset))
    if mode == "make":
        pick = random.Random(int(seed) * 1000 + int(preset)); rec = []
        c = Console()
        for x in ("", str(preset), ""):
            text, busy = c.handle(x)
            while busy:
                t2, busy = c.handle(""); text += t2
        m = 0
        while c.mode == "play" and m < int(M):
            before = len([r for r in rec if r[0] == "hud"])
            play_on(c, pick, rec, 1, J)
            m += len([r for r in rec if r[0] == "hud"]) - before
        open(save, "w").write(c.save())
        pickle.dump({"age": round(float(c.g.age()), 1), "inputs": len(c.inputs)}, open(out, "wb"))
        return
    pick = random.Random(int(seed) * 7919 + int(preset)); rec = []
    c = Console()
    text, busy = c.load(open(save).read()); k = 0
    while busy and k < 100000:
        t2, busy = c.handle(""); text += t2; k += 1
    hud = c.hud(); hud.pop("note", None)
    rec.append(("loaded", "", J.dumps(hud, sort_keys=True, default=str)))
    rec.append(("load text", "", text))
    play_on(c, pick, rec, int(after), J)
    pickle.dump({"rec": rec, "age": round(float(c.g.age()), 1) if c.g else None, "mode": c.mode}, open(out, "wb"))


if len(sys.argv) > 1 and sys.argv[1] == "--worker":
    worker(sys.argv[2:]); sys.exit(0)

ap = argparse.ArgumentParser()
ap.add_argument("--new-game", required=True)
ap.add_argument("--base-game", default=P["game_live"])
ap.add_argument("--presets", default="1,2,3,4,5,6")
ap.add_argument("--moments", type=int, default=6)
ap.add_argument("--after", type=int, default=25)
ap.add_argument("--seed", default="7")
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--scratch", default=None)
a = ap.parse_args()

os.makedirs(P["release_out"], exist_ok=True)
REPORT = path("release_out", time.strftime("saves_%Y%m%d-%H%M%S.txt", time.gmtime()))
rep = open(REPORT, "w")


def say(s=""):
    print(s, flush=True); rep.write(s + "\n"); rep.flush()


work = a.scratch or tempfile.mkdtemp(prefix="saves_")
skip = shutil.ignore_patterns("__pycache__", "*.pyc", "web", "test")
g = {}
for tag, src in (("base", a.base_game), ("new", a.new_game)):
    d = os.path.join(work, "game_" + tag); shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(os.path.abspath(src), d, ignore=skip); g[tag] = d
md5 = lambda p: __import__("hashlib").md5(open(p, "rb").read()).hexdigest()[:12]
say(f"Old saves load, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
for tag, src in (("base", a.base_game), ("new", a.new_game)):
    say(f"  {tag:4s} {src} (game.py {md5(os.path.join(g[tag], 'game.py'))}, console.py {md5(os.path.join(g[tag], 'console.py'))}, "
        f"engine.py {md5(os.path.join(g[tag], 'engine_pin', 'engine.py'))})")
say(f"  presets {a.presets}; saved after {a.moments} moments, played on {a.after} steps after the load; seed {a.seed}")
env = dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
me = os.path.abspath(__file__)


def run_all(jobs):
    running, todo, bad = [], list(jobs), []
    while todo or running:
        while todo and len(running) < a.jobs:
            j = todo.pop(0)
            p = subprocess.Popen([sys.executable, "-B", me, "--worker"] + j[1], env=env, cwd=j[1][0],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            running.append((p, j[0]))
        time.sleep(2)
        for r in list(running):
            if r[0].poll() is not None:
                running.remove(r)
                if r[0].returncode != 0:
                    bad.append(r[1]); say(f"MISS {r[1]}: {r[0].stdout.read().decode()[-600:]}")
    return bad


presets = [x for x in a.presets.split(",") if x]
P = lambda *x: os.path.join(work, "_".join(map(str, x)))
bad = run_all([(f"save {p}", [g["base"], "make", p, a.seed, str(a.moments), "0", P("save", p, ".json"), P("made", p, ".pkl")]) for p in presets])
bad += run_all([(f"load {p} {t}", [g[t], "load", p, a.seed, "0", str(a.after), P("save", p, ".json"), P("load", p, t, ".pkl")])
                for p in presets for t in ("base", "new") if f"save {p}" not in bad])
ok = not bad
for p in presets:
    try:
        m = pickle.load(open(P("made", p, ".pkl"), "rb"))
        b = pickle.load(open(P("load", p, "base", ".pkl"), "rb")); n = pickle.load(open(P("load", p, "new", ".pkl"), "rb"))
    except Exception as e:
        ok = False; say(f"MISS preset {p}: a run left no output ({e})"); continue
    head = f"preset {p}: saved at {m['age']} after {m['inputs']} lines; loaded, then {sum(r[0] == 'hud' for r in b['rec'])} more moments to {b['age']}"
    first = next((i for i, (u, v) in enumerate(zip(b["rec"], n["rec"])) if u != v), None)
    if first is None and len(b["rec"]) == len(n["rec"]):
        say(f"ok   {head}: the same life ({len(b['rec'])} records)")
    else:
        ok = False
        if first is None:
            say(f"MISS {head}: the same until one stops ({len(b['rec'])} vs {len(n['rec'])} records)"); continue
        u, v = b["rec"][first], n["rec"][first]
        k = next((j for j, (x, y) in enumerate(zip(u[2], v[2])) if x != y), min(len(u[2]), len(v[2])))
        say(f"MISS {head}: first difference at record {first} ({u[0]} after {u[1]!r}), character {k}:")
        say(f"       live ...{u[2][max(0, k - 120):k + 160]!r}")
        say(f"       new  ...{v[2][max(0, k - 120):k + 160]!r}")
say("Old saves: " + ("PASS (every save loads into the same life)" if ok else "FAIL"))
say(f"report: {REPORT}; scratch {work}")
import results; results.done('saves', 0 if ok else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
