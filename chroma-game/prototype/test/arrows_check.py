"""The v24 hover arrows (GAME arrows, with the Engine's foresee.arrows): the game's proof rows. Whole Earth lives, each
card alternately left to them and pushed to its second way, played with arrows on and with it off.

    python3 -B test/arrows_check.py [--presets 1,2,3,4] [--seeds 1-3] [--jobs 4]

    A1   the same life with it on and off: every card (age, moment, way, worked), the life's acts and its end the same
    A2   every way open at a card but doing nothing carries arrows for "if it works" and "if it fails", each arrow a kind
         (need, means, people, title), a name, up or down, a size 1 to 3 and its word; and no number reaches the page
    A3   how the arrows spread: by kind and by size, and how many ways show no arrow at all on a side

Each life runs in its own process (CHROMA_GAME sets the switch). Prints one line per life, then the rows; exit 0 when
A1 holds and A2 has no miss, 1 otherwise, 2 when the engine has no foresee.arrows."""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
KEYS = {"kind", "name", "dir", "size", "word"}
WORDS = {1: "a little", 2: "clearly", 3: "a lot"}


def play(preset, seed, on, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import game
    if not hasattr(game.F, "arrows"):
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    p = {k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")}
    g = game.Game(name="Ari", seed=seed, **p)
    cards, ways, k, seen = [], [], 0, None
    while not g.over and k < 3000:
        if g.advance() != "checkpoint":
            r = g.resolution
            if isinstance(r, dict) and id(r) != seen:
                seen = id(r)
                cards.append([r["age"], r["title"], r["act"], r["worked"]])
            continue
        cp = g.pending; k += 1
        if on:                                      # what the page gets for each way
            for o in g.cp_hud({o["idx"]: o["idx"] for o in cp["options"]})["options"] if hasattr(g, "cp_hud") else []:
                if o["colors"] != "-":
                    ways.append(o.get("arrows"))
        opts = [o["idx"] for o in cp["options"]]
        g.decide(opts[1] if k % 2 == 0 and len(opts) > 1 and not cp.get("turning") else None)
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), cards=cards, acts=g.history["acts"], ways=ways),
              open(out, "w"), default=str)


def run(preset, seed, on, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"arrows": on}))
    subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), "1" if on else "0", out],
                   env=env, check=True)
    return json.load(open(out))


def seeds_of(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, on, out = sys.argv
        return play(preset, int(seed), on == "1", out) or 0
    a = {"presets": "1,2,3,4", "seeds": "1-3", "jobs": "4"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    tmp = os.environ.get("TMPDIR", "/tmp")
    jobs = [(p, s) for p in a["presets"].split(",") for s in seeds_of(a["seeds"])]
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: (run(j[0], j[1], True, os.path.join(tmp, f"arrows_on_{os.getpid()}_{j[0]}_{j[1]}.json")),
                                     run(j[0], j[1], False, os.path.join(tmp, f"arrows_off_{os.getpid()}_{j[0]}_{j[1]}.json"))), jobs))
    if any(on.get("no_engine") for on, _ in res):
        print("the pinned engine has no foresee.arrows")
        return 2
    same, n_ways, miss, kinds, sizes, empty = 0, 0, [], Counter(), Counter(), Counter()
    for on, off in res:
        ok = on["cards"] == off["cards"] and on["acts"] == off["acts"] and on["age"] == off["age"]
        same += ok
        for w in on["ways"]:
            n_ways += 1
            if not isinstance(w, dict) or set(w) != {"win", "fail"}:
                miss.append(f"preset {on['preset']} seed {on['seed']}: {w}"); continue
            for side in ("win", "fail"):
                empty[side] += not w[side]
                for x in w[side]:
                    if set(x) != KEYS or x["dir"] not in ("up", "down") or x["size"] not in WORDS or x["word"] != WORDS[x["size"]]:
                        miss.append(f"preset {on['preset']} seed {on['seed']} {side}: {x}")
                    kinds[x.get("kind")] += 1; sizes[x.get("size")] += 1
        print(f"preset {on['preset']} seed {on['seed']}: age {on['age']}, {len(on['cards'])} cards, on and off "
              f"{'the same' if ok else 'DIFFER'}, {len(on['ways'])} ways shown")
    print(f"A1  lives the same with it on and off: {same} of {len(res)}")
    print(f"A2  ways with well-formed arrows and no number: {n_ways - len(miss)} of {n_ways}" + "".join("\n      " + m for m in miss[:6]))
    print(f"A3  arrows by kind {dict(kinds)}, by size {dict(sorted(sizes.items()))}; ways with no arrow if it works "
          f"{empty['win']}, if it fails {empty['fail']}")
    return 0 if same == len(res) and not miss else 1


if __name__ == "__main__":
    sys.exit(main())
