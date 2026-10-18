"""Every change has a cause (GAME causes, causes_fold): the game's proof rows. Whole lives played through the page's own
bridge (console.Console), as test/same_life.py plays them: the seed and name from a seeded random, a moment alternately
left to them and pushed to option 2.

    python3 -B test/causes_check.py same [--presets 1,2,3,4,5,6] [--seed 7]
        C1: each life with causes and causes_fold on against the same life with them off, every step compared after
        taking out the lines the switches rewrite (role, role_fold, year) and the cause trail markers; the rest of each
        step (the text, the HUD, every other line) must match byte for byte
    python3 -B test/causes_check.py rows [--presets 1,2,3,4] [--seeds 1-6] [--jobs 4]
        C2 to C5 over the played Earth lives: the gains and the losses that name a cause (counted apart; a gain or loss
        whose way already says why counts as named), C3 a named cause before its line (the trail's age), C4 the years
        whose colours moved cause_turn or more that name a mover, and none reading "like many others", C5 the separate
        gain and loss lines a life

Each life runs in its own process (CHROMA_GAME sets the switches). Prints one line per life and the rows; exit 0 when
C1 matches (same) or when the counts were made (rows: the bars are Release's; the script prints them beside the counts)."""
import hashlib, json, os, random, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
ON = {"causes": True, "causes_fold": True}
OFF = {"causes": False, "causes_fold": False}
REWRITTEN = ("role", "role_fold", "year")
TRAIL = re.compile(r"⟦Y:[^⟧]*⟧")
NEEDS = ("in time", "slipped away", "time passed")
TURN = 0.10                                    # GAME cause_turn


def play(preset, seed, out):
    """One whole life; each step's [line, text, busy, feed, hud] as JSON lines in out."""
    sys.path.insert(0, GAME_DIR)
    import numpy as np
    from console import Console
    random.seed(seed)
    c = Console()
    dflt = lambda o: o.item() if isinstance(o, np.generic) else o.tolist() if isinstance(o, np.ndarray) else str(o)
    n, k = 0, 0
    with open(out, "w") as f:
        def step(line):
            nonlocal n
            text, busy = c.handle(line)
            f.write(json.dumps([line, text, bool(busy), c.take_feed(), c.hud()], default=dflt, sort_keys=True) + "\n"); n += 1
            return busy
        step(""); step(preset); step("Ari")
        while c.mode == "play" and n < 20000:
            line = ""
            if c.g is not None and c.g.pending is not None:
                k += 1; line = "" if k % 2 else "2"
            while step(line):
                line = ""


def run(preset, seed, sw, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps(sw))
    subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out], env=env, check=True,
                   cwd=GAME_DIR)
    return out


MARK = re.compile(r"⟦[^⟧]*⟧")


def masked(line):
    """A step without what the switches rewrite: those lines in the feed, and their plain text in the step's text."""
    rec = json.loads(line)
    gone = [MARK.sub("", x.get("text", "")) for x in rec[3] if x.get("tag") in REWRITTEN]
    rec[3] = [MARK.sub("", json.dumps(x, sort_keys=True)) for x in rec[3] if x.get("tag") not in REWRITTEN]
    text = rec[1] or ""
    for g in gone:
        for part in g.split("\n"):
            if part.strip():
                text = text.replace(part, "")
    rec[1] = re.sub(r"\s+", " ", text).strip()
    return json.dumps(rec, sort_keys=True)


def same(presets, seed, tmp, jobs):
    with ThreadPoolExecutor(jobs) as ex:
        fut = {(p, s): ex.submit(run, p, seed, sw, os.path.join(tmp, f"c1-{p}-{seed}-{s}.jsonl"))
               for p in presets for s, sw in (("off", OFF), ("on", ON))}
        res = {k: f.result() for k, f in fut.items()}
    bad = 0
    for p in presets:
        a = open(res[(p, "off")]).read().splitlines(); b = open(res[(p, "on")]).read().splitlines()
        ma = [masked(x) for x in a]; mb = [masked(x) for x in b]
        first = next((i for i, (x, y) in enumerate(zip(ma, mb)) if x != y), None)
        ok = len(ma) == len(mb) and first is None
        bad += not ok
        h = lambda xs: hashlib.md5("\n".join(xs).encode()).hexdigest()[:12]
        print(f"C1 preset {p} seed {seed}: steps {len(a)} / {len(b)}, masked md5 {h(ma)} / {h(mb)}, "
              + ("same" if ok else f"DIFFERS at step {first if first is not None else min(len(a), len(b))}"))
    return bad == 0


def counts(path):
    c = dict(gain=0, gain_named=0, lose=0, lose_named=0, lines=0, c3=0, c3_miss=0, turned=0, turned_named=0, many=0, years=0)
    w0 = None
    for line in open(path):
        for x in json.loads(line)[3]:
            tag = x.get("tag")
            if tag == "chapter":
                w = x.get("w")
                if w0 is not None and w is not None and x.get("age", 0) >= 6:
                    c["years"] += 1
                    if sum(abs(a - b) for a, b in zip(w, w0)) >= TURN:
                        c["turned"] += 1
                        c["_turn_open"] = True
                w0 = w
            elif tag == "year" and c.pop("_turn_open", False):
                t = x.get("text", "")
                c["turned_named"] += bool(re.search(r"⟦Y:(event|source)\|", t))
                c["many"] += "like many others" in t
            if tag in ("role", "role_fold"):
                items = x.get("items") or [dict(what=x.get("what"), how=x.get("how", ""), cause=x.get("cause", ""))]
                c["lines"] += tag == "role"
                for it in items:
                    g = it.get("what") != "lost"
                    named = bool(it.get("cause")) or (tag == "role" and it.get("how") not in NEEDS)
                    c["gain" if g else "lose"] += 1; c["gain_named" if g else "lose_named"] += named
                for a in re.findall(r"⟦Y:(?:pick|mark|moment)\|([\d.]*)\|", x.get("text", "")):
                    c["c3"] += 1; c["c3_miss"] += bool(a) and float(a) > float(x.get("age", 0)) + 0.05
    c.pop("_turn_open", None)
    return c


def rows(presets, seeds, tmp, jobs):
    with ThreadPoolExecutor(jobs) as ex:
        fut = {(p, s): ex.submit(run, p, s, ON, os.path.join(tmp, f"rows-{p}-{s}.jsonl")) for p in presets for s in seeds}
        lives = {k: counts(f.result()) for k, f in fut.items()}
    tot = {}
    for (p, s), c in sorted(lives.items()):
        print(f"preset {p} seed {s}: gains {c['gain_named']}/{c['gain']}, losses {c['lose_named']}/{c['lose']}, "
              f"turned years {c['turned_named']}/{c['turned']} of {c['years']}, role lines {c['lines']}")
        for k, v in c.items():
            tot[k] = tot.get(k, 0) + v
    n = len(lives); pc = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"
    print(f"C2 gains named {tot['gain_named']}/{tot['gain']} = {pc(tot['gain_named'], tot['gain'])}, losses named "
          f"{tot['lose_named']}/{tot['lose']} = {pc(tot['lose_named'], tot['lose'])} (bar: at least 90% each)")
    print(f"C3 trail ages after their line: {tot['c3_miss']} of {tot['c3']} (bar: none)")
    print(f"C4 turned years naming a mover {tot['turned_named']}/{tot['turned']} = {pc(tot['turned_named'], tot['turned'])}, "
          f"reading 'like many others' {tot['many']} (bar: at least 90%, none)")
    print(f"C5 separate gain and loss lines a life {tot['lines'] / max(n, 1):.1f} (bar: at most about 45)")
    return True


def opt(a, k, d):
    return a[a.index(k) + 1] if k in a else d


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "_play":
        play(a[1], int(a[2]), a[3]); sys.exit(0)
    import tempfile
    tmp = opt(a, "--out", None) or tempfile.mkdtemp(prefix="causes-")
    jobs = int(opt(a, "--jobs", "4"))
    if a and a[0] == "same":
        ok = same(opt(a, "--presets", "1,2,3,4,5,6").split(","), int(opt(a, "--seed", "7")), tmp, jobs)
    elif a and a[0] == "rows":
        lo, _, hi = opt(a, "--seeds", "1-6").partition("-")
        ok = rows(opt(a, "--presets", "1,2,3,4").split(","), range(int(lo), int(hi or lo) + 1), tmp, jobs)
    else:
        print(__doc__); sys.exit(2)
    print("records in", tmp)
    sys.exit(0 if ok else 1)
