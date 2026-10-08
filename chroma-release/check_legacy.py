"""v22.1 same-lives proof, the one start the other checks never compare (coordinator 10-08 12:07 UTC): a life begun in
the world an earlier life left behind, as its child and as its grandchild (the setup's "begin in an earlier world").

In a copy of the live game (live v22 engine) and a copy of the new build (its own engine_pin), the same flow runs as the
game's test/saveload_world.py: life 1 (Build your own, fixed answers) is played to 12 and its world kept (world_out);
then life 2 begins in that world, once as the child of that world and once as the grandchild, and plays 40 steps with
seeded picks, pushes and steps. Everything must be equal between the two games: the world JSON life 1 leaves behind,
every feed line and text of life 2, and its state at the end (week, colors, resources, cast, the world's week).
Both games are copied to a scratch folder first; nothing is written in the shared folder except the report.

    python3 -B chroma-release/check_legacy.py --game DIR [--base-game DIR] [--seeds 77,78] [--scratch DIR]

Exit code 0 when both starts are the same in both games. Report: chroma-release/out/legacy_<UTC time>.txt."""
import sys, os, argparse, json, time, pickle, shutil, subprocess, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py


def worker(argv):
    gdir, seed, out = argv
    sys.path.insert(0, gdir)
    import numpy as np
    import console as C

    def run(c, line, rec):
        text, busy = c.handle(line); rec.append(("text", line, text)); rec.append(("feed", line, json.dumps(c.take_feed(), sort_keys=True, default=str)))
        c.hud()
        while busy:
            text, busy = c.handle(""); rec.append(("text", "", text)); rec.append(("feed", "", json.dumps(c.take_feed(), sort_keys=True, default=str)))
            c.hud()

    def state(c):
        g = c.g; loc = g.loc
        return json.dumps(dict(t=g.t, w=np.asarray(loc["z"][0]).tolist(), res=np.asarray(loc["res"][0]).tolist(),
                               cast=[(p["name"], p["role"], p["alive"]) for p in g.story.people],
                               world_t=int(loc["WL"].W.t) if loc.get("WL") is not None else None), sort_keys=True)

    a = C.Console(); a.handle(str(len(C.PRESETS) + 1))
    for x in ["Lale", "1", "1", "3", "3", "1", "", "2", "1", "", "0", "4242"]:
        a.handle(x)
    g = a.g; n = 0
    while not g.over and g.age() < 12 and n < 3000:
        n += 1; st = g.advance()
        if st == "checkpoint":
            g.decide(None)
    wo = a.world_out(); d = json.loads(wo)
    res = {"world_out": wo, "life1_age": d.get("age")}
    for gc in (False, True):
        rng = np.random.default_rng(int(seed)); rec = []
        b = C.Console(); b.world_in(json.dumps(dict(key=d["key"], name=d["name"], age=d["age"])))
        b.handle(str(len(C.PRESETS) + 1)); b.handle("Mira"); b.handle("2"); b.handle("1")
        b.world_in(wo); b.handle("3" if gc else "2")
        for x in ["1", "", "2", "1", "", "0", str(seed)]:
            run(b, x, rec)
        for step in range(40):
            if b.mode != "play":
                break
            k = rng.random()
            if b.g.pending is not None:
                run(b, "" if k < 0.5 else str(int(rng.integers(1, len(b.g.pending["options"]) + 1))), rec)
            else:
                run(b, "" if k < 0.6 else "y" if k < 0.85 else "m", rec)
        rec.append(("state", "", state(b)))
        res["grandchild" if gc else "child"] = dict(rec=rec, age=round(float(b.g.age()), 1), mode=b.mode,
                                                    earlier=json.loads(b.save())["setup"].get("earlier", {}).get("name"))
    pickle.dump(res, open(out, "wb"))


if len(sys.argv) > 1 and sys.argv[1] == "--worker":
    worker(sys.argv[2:]); sys.exit(0)

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--base-game", default=P["game_live"])
ap.add_argument("--seeds", default="77,78")
ap.add_argument("--scratch", default=None)
a = ap.parse_args()
os.makedirs(P["release_out"], exist_ok=True)
REPORT = path("release_out", time.strftime("legacy_%Y%m%d-%H%M%S.txt", time.gmtime()))
rep = open(REPORT, "w")


def say(s=""):
    print(s, flush=True); rep.write(s + "\n"); rep.flush()


work = a.scratch or tempfile.mkdtemp(prefix="legacy_")
g = {}
for tag, src in (("base", a.base_game), ("new", a.game)):
    d = os.path.join(work, "game_" + tag); shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(os.path.abspath(src), d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "web", "test")); g[tag] = d
md5 = lambda p: __import__("hashlib").md5(open(p, "rb").read()).hexdigest()[:12]
say(f"A life begun in an earlier life's world, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC")
for tag, src in (("base", a.base_game), ("new", a.game)):
    say(f"  {tag:4s} {src} (game.py {md5(os.path.join(g[tag], 'game.py'))}, engine.py {md5(os.path.join(g[tag], 'engine_pin', 'engine.py'))}, "
        f"world.py {md5(os.path.join(g[tag], 'engine_pin', 'world.py'))})")
env = dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
seeds = [x for x in a.seeds.split(",") if x]
procs = [(s, t, subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "--worker", g[t], s, os.path.join(work, f"{t}_{s}.pkl")],
                                 cwd=g[t], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)) for s in seeds for t in ("base", "new")]
ok = True
for s, t, p in procs:
    o = p.communicate()[0].decode()
    if p.returncode != 0:
        ok = False; say(f"MISS seed {s} {t}: the run failed: {o[-600:]}")
for s in seeds:
    try:
        B = pickle.load(open(os.path.join(work, f"base_{s}.pkl"), "rb")); N = pickle.load(open(os.path.join(work, f"new_{s}.pkl"), "rb"))
    except Exception as e:
        ok = False; say(f"MISS seed {s}: no output ({e})"); continue
    same_w = B["world_out"] == N["world_out"]
    say(("ok  " if same_w else "MISS") + f" seed {s}: the world life 1 leaves behind at {B['life1_age']}: "
        + (f"identical ({len(B['world_out'])} bytes)" if same_w else "DIFFERS"))
    ok &= same_w
    for k in ("child", "grandchild"):
        x, y = B[k]["rec"], N[k]["rec"]
        first = next((i for i, (u, v) in enumerate(zip(x, y)) if u != v), None)
        head = f"seed {s}, life 2 as the {k} of that world (earlier: {B[k]['earlier']}), to {B[k]['age']}"
        if first is None and len(x) == len(y):
            say(f"ok   {head}: identical ({len(x)} texts, feeds and the end state)")
        else:
            ok = False
            i = first if first is not None else min(len(x), len(y))
            u = x[i] if i < len(x) else ("<end>", "", ""); v = y[i] if i < len(y) else ("<end>", "", "")
            kk = next((j for j, (c1, c2) in enumerate(zip(u[2], v[2])) if c1 != c2), 0)
            say(f"MISS {head}: first difference at record {i} ({u[0]} after {u[1]!r}): live ...{u[2][max(0, kk - 100):kk + 140]!r} "
                f"new ...{v[2][max(0, kk - 100):kk + 140]!r}")
say("Earlier-world starts: " + ("PASS (identical)" if ok else "FAIL"))
say(f"report: {REPORT}; scratch {work}")
import results; results.done('legacy', 0 if ok else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
