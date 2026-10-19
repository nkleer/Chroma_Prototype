"""v24 talking it over (GAME talk, with ask_matter .5 so moments that matter count as big): through the page's own bridge
(console.Console). At each big moment the player talks option 2 over (key t2), then pushes it; other moments are left to
them. With the switch off the game plays as main (prove.py).

    python3 -B test/talk_check.py [--presets 1,2,3,4] [--seeds 1] [--jobs 4]

    T1   every life plays to its end (no crash)
    T2   at a big moment the talk answers in one quoted line, the option's reluctance falls by the stated share (never to
         a wall: at most .8), a second talk is refused, and an ordinary moment refuses it
    T3   a report: big moments a life, the mean fall, the answers' kinds

Exit 0 when T1 and T2 hold, 1 otherwise."""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)


def play(preset, seed, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import pinned; pinned.ensure()
    from console import Console
    c = Console()
    c.handle(""); c.handle(preset)
    busy = c.handle("Ari")[1]
    while busy:
        busy = c.handle("")[1]
    bad, k, big, falls, kinds, refused = [], 0, 0, [], Counter(), 0
    while c.mode == "play" and k < 3000:
        g = c.g
        line = ""
        if g.pending is not None:
            k += 1
            cp = g.pending
            o2 = cp["by_idx"].get(c.numbering.get(2)) if 2 in c.numbering else None
            if cp.get("big") and o2 is not None and o2["colors"] != "-":
                big += 1
                r0 = float(o2["rel"])
                txt, _ = c.handle("t2")
                t_ = cp.get("talked")
                if not t_ or not txt.startswith(g.name + ": “"):
                    bad.append(f"at {g.age():.1f}: talk said {txt[:60]!r}")
                else:
                    falls.append(t_["fall"]); kinds.update([t_["line"].split()[0].strip("“,.")])
                    if not (0 <= t_["fall"] <= 0.8) or abs(float(o2["rel"]) - round(r0 * (1 - t_["fall"]), 4)) > 0.01:
                        bad.append(f"at {g.age():.1f}: rel {r0} -> {o2['rel']} with fall {t_['fall']}")
                    if g.talk(o2["idx"]).get("error") is None:
                        bad.append(f"at {g.age():.1f}: a second talk was not refused")
                line = "2"
            elif not cp.get("big") and refused < 3 and 2 in c.numbering:
                if g.talk(c.numbering[2]).get("error") is None:
                    bad.append(f"at {g.age():.1f}: an ordinary moment took a talk")
                refused += 1
        busy = c.handle(line)[1]
        while busy:
            busy = c.handle("")[1]
    g = c.g
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), moments=k, big=big, falls=falls, kinds=kinds, bad=bad),
              open(out, "w"))


def run(preset, seed, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"talk": True, "ask_matter": 0.5}))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, crash=r.returncode)


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, out = sys.argv
        return play(preset, int(seed), out) or 0
    a = {"presets": "1,2,3,4", "seeds": "1", "jobs": "4"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    lo, _, hi = a["seeds"].partition("-")
    jobs = [(p, s) for p in a["presets"].split(",") for s in range(int(lo), int(hi or lo) + 1)]
    tmp = os.environ.get("TMPDIR", "/tmp")
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(j[0], j[1], os.path.join(tmp, f"talk_{os.getpid()}_{j[0]}_{j[1]}.json")), jobs))
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    falls, kinds = [], Counter()
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']}: CRASH (exit {r['crash']})"); continue
        falls += r["falls"]; kinds.update(r["kinds"])
        print(f"preset {r['preset']} seed {r['seed']}: age {r['age']}, {r['moments']} asks, {r['big']} big moments talked over")
    print(f"T1  lives played to their end: {len(res) - len(crash)} of {len(res)}")
    print(f"T2  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:6]))
    print(f"T3  talks {len(falls)}, mean fall {sum(falls) / max(len(falls), 1):.2f}; answers begin {dict(kinds)}")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
