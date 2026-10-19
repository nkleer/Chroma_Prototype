"""v24 aims (GAME aims, with the Engine's aims and heights): the game's checks with it on. Whole Earth lives through the
page's own bridge (console.Console), each moment alternately left to them and pushed to its second way; at the first
moment from age 16 the player takes up the first aim offered, and at the first one from 40 lets the weakest go. With it
off the game plays as main (prove.py), so this checks the display and the player's two acts only.

    python3 -B test/aims_check.py [--presets 1,2,3,4] [--seeds 1] [--jobs 4]

    A1   every life plays to its end with aims on (no crash)
    A2   the HUD's aims track is well formed at every moment (slot, ladder, how far along, the next step) and the sheet
         (key s) and key a name every aim held
    A3   taking up an aim through the page's command holds it, "set by you"; letting one go removes it
    A4   a report: aims held, callings, heights reached, how many options led into an aim's next step

Exit 0 when A1 to A3 hold, 1 otherwise, 2 when the engine has no aims."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)


def well_formed(a):
    return (isinstance(a.get("slot"), int) and a.get("aim") and isinstance(a.get("steps"), list) and a["steps"]
            and 0 <= a["reached"] <= len(a["steps"]) and (a["next"] is None) == (a["reached"] >= len(a["steps"]))
            and all(s["reached"] == (i < a["reached"]) for i, s in enumerate(a["steps"])))


def play(preset, seed, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import pinned; pinned.ensure()
    import game
    if "aims" not in game.E.DEFAULT:
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    from console import Console
    c = Console()
    c.handle(""); c.handle(preset)
    busy = c.handle("Ari")[1]
    while busy:
        busy = c.handle("")[1]
    bad, k, took, dropped, ways, held_max = [], 0, None, None, 0, 0
    while c.mode == "play" and k < 3000:
        g = c.g
        if g.pending is not None:
            k += 1
            L = g.hud()
            for a in L.get("aims") or []:
                if not well_formed(a):
                    bad.append(f"at {g.age():.1f}: {a}")
            held_max = max(held_max, len(L.get("aims") or []))
            ways += sum(1 for o in (c.hud().get("cp") or {}).get("options", []) if o.get("aims"))
            if took is None and g.age() >= 16 and L.get("aim_choices"):
                nm = L["aim_choices"][0]["aim"]
                txt, _ = c.handle(f"aim set {nm}")
                x = [a for a in g.aims_view() or [] if a["aim"] == nm]
                took = (round(g.age(), 1), nm, bool(x and not x[0]["own"] and x[0]["by_player"]), txt[:80])
                if not took[2]:
                    bad.append(f"aim set {nm}: not held as set by you ({txt[:80]})")
            held = g.aims_view() or []
            if held:
                st, ka = g.status(), c.handle("a")[0]
                miss = [a["aim"] for a in held if a["aim"] not in st or a["aim"] not in ka]
                if miss:
                    bad.append(f"at {g.age():.1f}: sheet or key a leaves out {miss}")
            if dropped is None and g.age() >= 40 and held:
                w = min(held, key=lambda a: a["strength"])
                c.handle(f"aim drop {w['slot']}")
                gone = not any(a["slot"] == w["slot"] and a["aim"] == w["aim"] for a in g.aims_view() or [])
                dropped = (round(g.age(), 1), w["aim"], gone)
                if not gone:
                    bad.append(f"aim drop {w['slot']}: still held")
            busy = c.handle("" if k % 2 else "2")[1]
        else:
            busy = c.handle("")[1]
        while busy:
            busy = c.handle("")[1]
    g = c.g
    L = g.hud()
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), moments=k, bad=bad, took=took, dropped=dropped, ways=ways,
                   held_max=held_max, aims=[(a["aim"], a["reached"], len(a["steps"]), a["calling"], a["own"]) for a in L.get("aims") or []],
                   heights=L.get("heights") or []), open(out, "w"), default=str)


def run(preset, seed, out):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"aims": True}))
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
        res = list(ex.map(lambda j: run(j[0], j[1], os.path.join(tmp, f"aims_{os.getpid()}_{j[0]}_{j[1]}.json")), jobs))
    if any(r.get("no_engine") for r in res):
        print("the pinned engine has no aims")
        return 2
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']}: CRASH (exit {r['crash']})"); continue
        print(f"preset {r['preset']} seed {r['seed']}: age {r['age']}, {r['moments']} moments, up to {r['held_max']} aims, "
              f"{r['ways']} options toward an aim; took {r['took']}; dropped {r['dropped']}; at the end {r['aims']}; heights {r['heights']}")
    print(f"A1  lives played to their end with aims on: {len(res) - len(crash)} of {len(res)}")
    print(f"A2+A3  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:8]))
    print(f"A4  options toward an aim: {sum(r.get('ways', 0) for r in res)}; aims set by the player held: "
          f"{sum(1 for r in res if r.get('took') and r['took'][2])} of {sum(1 for r in res if r.get('took'))}")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
