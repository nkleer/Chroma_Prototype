"""Because of you, and meanwhile (GAME because, with the Engine's need_why): the game's proof rows. Whole Earth lives,
each card alternately left to them and pushed to its second way, played with because on and with it off.

    python3 -B test/because_check.py [--presets 1,2,3,4] [--seeds 1-3] [--jobs 4]

    W1   the same life with it on and off: every card (age, moment, way, worked), the life's acts and its end the same
    W2   every need that moved a point or more after a pick is in "because of you" or "meanwhile", each line with its
         cause, and the two parts add up to its change (within half a point, the parts' rounding)
    W3   silent setbacks from age 12 told in a short line (the Engine's nw_imp weeks; the same line waits its years when
         line_wait is on) and how many fall in a pick's week, where the panel tells them

Each life runs in its own process (CHROMA_GAME sets the switch). Prints one line per life, then the rows; exit 0 when
W1 holds and W2 has no miss, 1 otherwise, 2 when the engine has no need_why."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

SETBACK_AGE = 12
HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)


def play(preset, seed, on, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import game
    if "need_why" not in game.E.DEFAULT:
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    p = {k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")}
    g = game.Game(name="Ari", seed=seed, **p)
    cards, splits, k, seen = [], [], 0, None
    while not g.over and k < 3000:
        if g.advance() != "checkpoint":
            r = g.resolution
            if isinstance(r, dict) and id(r) != seen:
                seen = id(r)
                cards.append([r["age"], r["title"], r["act"], r["worked"]])
                if on:
                    splits.append(dict(needs=r.get("needs") or [], because=r.get("because")))
            continue
        cp = g.pending; k += 1
        ways = [o["idx"] for o in cp["options"]]
        g.decide(ways[1] if k % 2 == 0 and len(ways) > 1 and not cp.get("turning") else None)
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), cards=cards, acts=g.history["acts"], splits=splits,
                   setbacks=len(g.history.get("setbacks", [])), told=sum(f["tag"] == "setback" for f in g.feed)),
              open(out, "w"), default=str)


def run(preset, seed, on, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"because": on}))
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
        res = list(ex.map(lambda j: (run(j[0], j[1], True, os.path.join(tmp, f"because_on_{os.getpid()}_{j[0]}_{j[1]}.json")),
                                     run(j[0], j[1], False, os.path.join(tmp, f"because_off_{os.getpid()}_{j[0]}_{j[1]}.json"))), jobs))
    if any(on.get("no_engine") for on, _ in res):
        print("the pinned engine has no need_why")
        return 2
    same, moved, miss, lines, sb = 0, 0, [], 0, []
    for on, off in res:
        ok = on["cards"] == off["cards"] and on["acts"] == off["acts"] and on["age"] == off["age"]
        same += ok
        n_sb = 0
        for sp in on["splits"]:
            b = sp["because"]
            for x in sp["needs"]:
                moved += 1
                parts = [y for y in ((b or {}).get("you", []) + (b or {}).get("meanwhile", [])) if y["need"] == x["need"]]
                if not parts or any(not y.get("why") for y in parts) or abs(sum(y["delta"] for y in parts) - x["delta"]) > 0.005:
                    miss.append(f"preset {on['preset']} seed {on['seed']} at {x}: {parts}")
            if b:
                lines += len(b["you"]) + len(b["meanwhile"])
                n_sb += bool(b.get("setback"))
        sb.append(n_sb)
        print(f"preset {on['preset']} seed {on['seed']}: age {on['age']}, {len(on['cards'])} cards, on and off "
              f"{'the same' if ok else 'DIFFER'}, setbacks {on['setbacks']}, told {on['told']} ({n_sb} in a pick's week)")
    print(f"W1  lives the same with it on and off: {same} of {len(res)}")
    print(f"W2  need moves of a point or more put in a group with a cause: {moved - len(miss)} of {moved} ({lines} lines)"
          + "".join("\n      " + m for m in miss[:6]))
    print(f"W3  silent setbacks from age {SETBACK_AGE:g}: {sum(on['setbacks'] for on, _ in res)} over {len(res)} lives, told "
          f"{sum(on['told'] for on, _ in res)} (a line said again waits its years), {sum(sb)} in a pick's week")
    return 0 if same == len(res) and not miss else 1


if __name__ == "__main__":
    sys.exit(main())
