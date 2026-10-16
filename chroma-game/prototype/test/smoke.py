"""Smoke test: a short played life through the page's own bridge (console.Console, as web/worker.js runs it), in pure
Python, with no input() and no browser. It catches a crash, a NaN or None in the numbers, and a change in what the game
plays, in well under a minute (a whole life takes about 2 minutes; test/same_life.py is the full proof).

Two starts, each with random.seed(7): preset 1 (a newborn on modern Earth) with the keys w, m, y, s, l, l, then lived on
to age 5 with every checkpoint answered (Enter and 2 in turn, as same_life.py does), and a save that must load back
exactly; preset 6 (the world of magic) with the key d, lived on to age 12. Every step's [line, text, busy, feed, hud] record is hashed, so
two trees that play the same give the same md5 per start. It also checks that every game-side module the game imports is
listed in web/worker.js SOURCES, so the page loads it too.

    python3 -B test/smoke.py                 run it; exit 0 when nothing broke
    python3 -B test/smoke.py --same          also compare the md5s with test/smoke.golden.json (made with the same
                                             Python and numpy; otherwise it says so and asks for --base)
    python3 -B test/smoke.py --base DIR      also run the same starts on another game folder (for example the
                                             chroma-game/prototype of a worktree of origin/main) and compare
    python3 -B test/smoke.py --update        rewrite test/smoke.golden.json; only for a change meant to alter play
    python3 -B test/smoke.py --game DIR      play the game in DIR instead of the one this script sits in
"""
import hashlib, json, math, os, platform, random, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
GOLDEN = os.path.join(HERE, "smoke.golden.json")
STARTS = (("1", ["w", "m", "y", "s", "l", "l"], 5.0, True), ("6", ["d"], 12.0, False))   # preset, keys, live on to age, save


def args():
    a = sys.argv[1:]
    opt = {"same": "--same" in a, "update": "--update" in a, "json": "--json" in a, "base": None, "game": None}
    for k in ("base", "game"):
        if "--" + k in a:
            opt[k] = os.path.abspath(a[a.index("--" + k) + 1])
    return opt


def bad_numbers(x, where="hud"):
    """Every NaN, infinity or None among the numbers of a HUD record (None in a text field is fine)."""
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += bad_numbers(v, f"{where}.{k}")
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            out += bad_numbers(v, f"{where}[{i}]")
    elif isinstance(x, float) and not math.isfinite(x):
        out.append(where)
    return out


def play(game_dir):
    sys.path.insert(0, game_dir)
    import numpy as np
    from console import Console

    def dflt(o):
        if isinstance(o, np.generic):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)

    def state(c):
        loc = c.g.loc
        return [c.g.t] + [np.asarray(loc[k][0]).tolist() for k in ("z", "y", "res")]

    res, errors = {}, []
    for preset, keys, age, save in STARTS:
        t0 = time.time()
        random.seed(7)
        c = Console()
        h = hashlib.md5()
        n = 0

        def step(line):
            nonlocal n
            text, busy = c.handle(line)
            hud = c.hud()
            rec = json.dumps([line, text, bool(busy), c.take_feed(), hud], default=dflt, sort_keys=True)
            h.update(rec.encode())
            n += 1
            for w in bad_numbers(json.loads(rec)[4]):
                errors.append(f"preset {preset}, step {n}: not a number at {w}")
            if re.search(r"\bnan\b|Traceback", text or ""):
                errors.append(f"preset {preset}, step {n} ({line!r}): {text[-200:]!r}")
            return busy

        step("")
        step(preset)
        step("Ari")
        k = 0
        for key in keys:
            line = key
            while step(line):
                line = ""
        while c.mode == "play" and c.g.age() < age:
            line = ""
            if c.g.pending is not None:
                k += 1
                line = "" if k % 2 else "2"
            while step(line):
                line = ""
        for name in ("z", "y", "res"):
            v = np.asarray(c.g.loc[name][0], dtype=float)
            if not np.all(np.isfinite(v)):
                errors.append(f"preset {preset}: engine state {name} has a NaN or infinity")
        if save and c.mode == "play":
            b = Console()
            busy = b.load(c.save())[1]
            while busy:
                busy = b.handle("")[1]
            if state(b) != state(c):
                errors.append(f"preset {preset}: the saved life loads back different")
        res[preset] = dict(md5=h.hexdigest(), steps=n, checkpoints=k, age=round(float(c.g.age()), 2), mode=c.mode,
                           secs=round(time.time() - t0, 1))
    return res, errors


def page_files(game_dir):
    """Every game-side module the game's own files import must be in web/worker.js SOURCES, or the page lacks it (and a
    module imported under try/except, such as routine, would vanish from the page without an error)."""
    import ast
    wjs = open(os.path.join(game_dir, "web", "worker.js"), encoding="utf-8").read()
    srcs = set(json.loads(re.search(r"const SOURCES = (\[[^\]]*\]);", wjs).group(1)))
    missing = []
    for f in sorted(srcs):
        if f.startswith("engine_pin/") or not f.endswith(".py"):
            continue
        for n in ast.walk(ast.parse(open(os.path.join(game_dir, f), encoding="utf-8").read())):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module] if isinstance(n, ast.ImportFrom) and n.module else []
            for m in names:
                p = m.split(".")[0] + ".py"
                if os.path.isfile(os.path.join(game_dir, p)) and p not in srcs:
                    missing.append(f"{p} (imported by {f})")
    return sorted(set(missing))


def versions():
    import numpy as np
    return {"python": platform.python_version(), "numpy": np.__version__}


def main():
    opt = args()
    game = opt["game"] or os.path.dirname(HERE)
    t0 = time.time()
    res, errors = play(game)
    errors += [f"web/worker.js SOURCES lacks {m}" for m in page_files(game)]
    if opt["json"]:
        print(json.dumps({"res": res, "errors": errors}))
        return 0
    for p, r in res.items():
        print(f"preset {p}: {r['steps']} steps, {r['checkpoints']} checkpoints, age {r['age']}, {r['mode']}, "
              f"{r['secs']} s, md5 {r['md5']}")
    ok = not errors
    for e in errors:
        print("FAIL", e)
    now = {p: r["md5"] for p, r in res.items()}
    if opt["update"]:
        json.dump(dict(versions(), md5=now), open(GOLDEN, "w"), indent=1)
        print("wrote", os.path.relpath(GOLDEN))
    elif opt["same"]:
        g = json.load(open(GOLDEN))
        v = versions()
        if any(g.get(k) != v[k] for k in v):
            print(f"golden made with Python {g.get('python')}, numpy {g.get('numpy')}; this is Python {v['python']}, "
                  f"numpy {v['numpy']}: compare with --base <origin/main's chroma-game/prototype> instead")
            ok = False
        else:
            same = g["md5"] == now
            print("same as test/smoke.golden.json" if same else f"DIFFERENT from test/smoke.golden.json: {g['md5']}")
            ok &= same
    if opt["base"]:
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--json", "--game", opt["base"]],
                           capture_output=True, text=True)
        base = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else None
        if base is None:
            print("FAIL the base did not run:", r.stderr[-400:])
            ok = False
        else:
            bm = {p: x["md5"] for p, x in base["res"].items()}
            print("same as the base" if bm == now else f"DIFFERENT from the base: {bm}")
            ok &= bm == now and not base["errors"]
    print(f"smoke {'OK' if ok else 'FAIL'} in {time.time() - t0:.1f} s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
