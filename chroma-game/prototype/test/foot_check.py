"""v24 footprints (GAME foot, with the Engine's foot_on): the game's checks with it on. Whole Earth lives, each card
alternately left to them and pushed to its second way. With it off the game plays as main (prove.py), so this checks
the display only.

    python3 -B test/foot_check.py [--presets 1,2,3,4] [--seeds 1] [--jobs 4]

    F1   every life plays to its end with footprints on (no crash)
    F2   after a pick, at most one footprint line per kind, each kind one of the six, inside "Because of you"
    F3   the HUD and the Book show exactly six stacks, each a count and one line; the counts add up to the life's record
         (marks: only those nearing a title or perk)
    F4   how often picks leave footprints, by kind (a report)

Exit 0 when F1 to F3 hold, 1 otherwise, 2 when the engine has no foot_on."""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
KINDS = ("person", "place", "means", "mark", "door", "lesson")


def play(preset, seed, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import game
    if "foot_on" not in game.E.DEFAULT:
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    p = {k: v for k, v in game.PRESETS[preset].items() if k not in ("title", "blurb")}
    g = game.Game(name="Ari", seed=seed, **p)
    picks, lines, bad, k, seen = 0, Counter(), [], 0, None
    while not g.over and k < 3000:
        if g.advance() != "checkpoint":
            r = g.resolution
            if isinstance(r, dict) and id(r) != seen:
                seen = id(r); picks += 1
                ft = r.get("foot") or []
                ks = [x["kind"] for x in ft]
                if len(ks) != len(set(ks)) or any(x not in KINDS for x in ks):
                    bad.append(f"at {r['age']}: {ft}")
                lines.update(ks)
            continue
        cp = g.pending; k += 1
        ways = [o["idx"] for o in cp["options"]]
        g.decide(ways[1] if k % 2 == 0 and len(ways) > 1 and not cp.get("turning") else None)
    st, bk = g.hud().get("foot") or [], g.book().get("foot") or []
    h = Counter(x["kind"] for x in g.history.get("foot", []))
    for name, xs in (("hud", st), ("book", bk)):
        if [x["kind"] for x in xs] != list(KINDS) or any(x["n"] != h[x["kind"]] for x in xs if x["kind"] != "mark"):
            bad.append(f"{name} stacks: {[(x['kind'], x['n']) for x in xs]} vs {dict(h)}")
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), picks=picks, lines=lines, record=h, bad=bad,
                   stacks=[(x["name"], x["n"], x["line"]) for x in st]), open(out, "w"), default=str)


def run(preset, seed, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"foot": True}))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, crash=r.returncode)


def seeds_of(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, out = sys.argv
        return play(preset, int(seed), out) or 0
    a = {"presets": "1,2,3,4", "seeds": "1", "jobs": "4"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    tmp = os.environ.get("TMPDIR", "/tmp")
    jobs = [(p, s) for p in a["presets"].split(",") for s in seeds_of(a["seeds"])]
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(j[0], j[1], os.path.join(tmp, f"foot_{os.getpid()}_{j[0]}_{j[1]}.json")), jobs))
    if any(r.get("no_engine") for r in res):
        print("the pinned engine has no foot_on")
        return 2
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    lines, rec, picks = Counter(), Counter(), 0
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']}: CRASH (exit {r['crash']})"); continue
        picks += r["picks"]; lines.update(r["lines"]); rec.update(r["record"])
        print(f"preset {r['preset']} seed {r['seed']}: age {r['age']}, {r['picks']} picks; stacks "
              + "; ".join(f"{n} {c}" for n, c, _ in r["stacks"]))
    print(f"F1  lives played to their end with footprints on: {len(res) - len(crash)} of {len(res)}")
    print(f"F2+F3  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:6]))
    print(f"F4  footprint lines after {picks} picks: {dict(lines)}; the lives' record: {dict(rec)}")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
