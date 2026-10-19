"""v24 asks (GAME ask_matter, with aims on): which moments are put to the player when what matters to the character now
weighs in. Whole Earth lives, each moment left to them, played with aims on and ask_matter 0 (as before) and at the
value given; the same seeds both ways. With ask_matter at 0 the game plays as main (prove.py).

    python3 -B test/asks_check.py [--matter 0.5] [--presets 1,2,3,4] [--seeds 1] [--jobs 4]

    Q1   every life plays to its end both ways (no crash)
    Q2   with it on, every card asked for what matters says why (an aim, a need they lack, the people in their life)
    Q3   a report: asks a life both ways, and the share asked for what matters, by kind

Exit 0 when Q1 and Q2 hold, 1 otherwise."""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)


def play(preset, seed, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import game
    p = {k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")}
    g = game.Game(name="Ari", seed=seed, **p)
    asks, why, bad, k = 0, Counter(), [], 0
    while not g.over and k < 3000:
        if g.advance() != "checkpoint":
            continue
        cp = g.pending; k += 1
        if not cp.get("turning"):
            asks += 1
            w = cp.get("why_ask")
            if w:
                why[w["kind"]] += 1
                if not w.get("say") or w["kind"] not in ("aim", "need", "people"):
                    bad.append(f"at {cp['age']:.1f}: {w}")
        g.decide(None)
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), asks=asks, why=why, bad=bad), open(out, "w"))


def run(preset, seed, matter, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"aims": True, "ask_matter": matter}))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, crash=r.returncode)


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, out = sys.argv
        return play(preset, int(seed), out) or 0
    a = {"matter": "0.5", "presets": "1,2,3,4", "seeds": "1", "jobs": "4"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    lo, _, hi = a["seeds"].partition("-")
    jobs = [(p, s, m) for p in a["presets"].split(",") for s in range(int(lo), int(hi or lo) + 1) for m in (0.0, float(a["matter"]))]
    tmp = os.environ.get("TMPDIR", "/tmp")
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: dict(run(j[0], j[1], j[2], os.path.join(tmp, f"asks_{os.getpid()}_{j[0]}_{j[1]}_{j[2]}.json")), m=j[2]), jobs))
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']} matter {r['m']}: CRASH (exit {r['crash']})"); continue
        print(f"preset {r['preset']} seed {r['seed']} matter {r['m']}: age {r['age']}, {r['asks']} asks, for what matters {dict(r['why'])}")
    off = [r for r in res if r["m"] == 0.0 and "crash" not in r]; on = [r for r in res if r["m"] > 0 and "crash" not in r]
    why = Counter()
    for r in on:
        why.update(r["why"])
    n_on = sum(r["asks"] for r in on)
    print(f"Q1  lives played to their end: {len(res) - len(crash)} of {len(res)}")
    print(f"Q2  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:6]))
    print(f"Q3  asks a life: {sum(r['asks'] for r in off) / max(len(off), 1):.1f} off, {n_on / max(len(on), 1):.1f} at {a['matter']}; "
          f"asked for what matters: {sum(why.values())} of {n_on} ({dict(why)})")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
