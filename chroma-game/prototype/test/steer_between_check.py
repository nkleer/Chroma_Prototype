"""v24 steering between asks (GAME steer_between): the player's lean held while watching. Whole Earth lives through the
page's own bridge (console.Console), each moment left to them; one way with no lean, the other leaning toward one color
(--color, default R) after every ask from age 16. With the switch off the game plays as main (prove.py).

    python3 -B test/steer_between_check.py [--color R] [--presets 1,2,3,4] [--seeds 1] [--jobs 4]

    S1   every life plays to its end both ways (no crash)
    S2   a lean ends at the next ask (none is held while a moment waits), and each moved choice is in the steers record
    S3   a report: choices moved, and the leaned color's share at the end both ways

Exit 0 when S1 and S2 hold, 1 otherwise."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)


def play(preset, seed, color, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import pinned; pinned.ensure()
    import game
    from console import Console
    c = Console()
    c.handle(""); c.handle(preset)
    busy = c.handle("Ari")[1]
    while busy:
        busy = c.handle("")[1]
    bad, k, moved = [], 0, 0
    while c.mode == "play" and k < 3000:
        g = c.g
        if g.pending is not None:
            k += 1
            if g.steer_view() is not None:
                bad.append(f"at {g.age():.1f}: a lean held while a moment waits")
            busy = c.handle("")[1]
        else:
            if color != "-" and g.age() >= 16 and g.steer_view() is None:
                c.handle("~" + color.lower())
            busy = c.handle("")[1]
        while busy:
            busy = c.handle("")[1]
    g = c.g
    between = [x for x in g.history["steers"] if x["kind"] == "between"]
    w = game.E.softmax(g.loc["z"][0]) if g.loc is not None else None
    json.dump(dict(preset=preset, seed=seed, color=color, age=round(g.age(), 2), moments=k, moved=len(between), bad=bad,
                   share=None if w is None else round(float(w[game.COLORS.index(color if color != "-" else "R")]), 3)),
              open(out, "w"))


def run(preset, seed, color, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"steer_between": True}))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), color, out], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, color=color, crash=r.returncode)


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, color, out = sys.argv
        return play(preset, int(seed), color, out) or 0
    a = {"color": "R", "presets": "1,2,3,4", "seeds": "1", "jobs": "4"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    lo, _, hi = a["seeds"].partition("-")
    jobs = [(p, s, col) for p in a["presets"].split(",") for s in range(int(lo), int(hi or lo) + 1) for col in ("-", a["color"])]
    tmp = os.environ.get("TMPDIR", "/tmp")
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(j[0], j[1], j[2], os.path.join(tmp, f"steer_{os.getpid()}_{j[0]}_{j[1]}_{j[2]}.json")), jobs))
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']} lean {r['color']}: CRASH (exit {r['crash']})"); continue
        print(f"preset {r['preset']} seed {r['seed']} lean {r['color']}: age {r['age']}, {r['moments']} asks, {r['moved']} choices moved, "
              f"{a['color']} at the end {r['share']}")
    print(f"S1  lives played to their end: {len(res) - len(crash)} of {len(res)}")
    print(f"S2  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:6]))
    on = [r for r in res if r["color"] != "-" and "crash" not in r]; off = [r for r in res if r["color"] == "-" and "crash" not in r]
    mean = lambda xs: sum(xs) / max(len(xs), 1)
    print(f"S3  {a['color']} at the end: {mean([r['share'] for r in off]):.3f} with no lean, {mean([r['share'] for r in on]):.3f} leaning; "
          f"choices moved a life {mean([r['moved'] for r in on]):.1f}")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
