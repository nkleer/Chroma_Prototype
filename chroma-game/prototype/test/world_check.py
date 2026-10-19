"""v24 world answers (GAME world_answers, with the Engine's world_answers): the game's checks with it on. Whole Earth lives
through the page's own bridge (console.Console), each moment alternately left to them and pushed to its second way. With
it off the game plays as main (prove.py), so this checks the words and the panel only.

    python3 -B test/world_check.py [--presets 1,2,3,4] [--seeds 1] [--jobs 4] [--phase2 1]

    W1   every life plays to its end with world answers on (no crash)
    W2   every told world line, in the story, the panel and the end's read-back, is filled (no {slot} left) and the
         "Your world" panel is well formed at every moment (five rings, counts, the newest lines)
    W3   a report: told footprint lines a life (the spec's WA2 band, at least 3 and a median of 10 or more, is Release's
         to judge after the refit), by ring and size, sphere events told, asks and decisions, what the world kept

Exit 0 when W1 and W2 hold, 1 otherwise, 2 when the engine has no world answers."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.dirname(HERE)
SLOT = re.compile(r"\{\w+\}")


def panel_ok(p):
    return (isinstance(p, dict) and [r["ring"] for r in p.get("rings", [])] == ["person", "group", "place", "town_sphere", "nation"]
            and all(isinstance(r["n"], int) and r["n"] >= 0 and (bool(r["line"]) == (r["n"] > 0)) for r in p["rings"])
            and isinstance(p.get("lines"), list) and isinstance(p.get("asked"), int) and isinstance(p.get("decided"), int))


def play(preset, seed, out):
    sys.path.insert(0, GAME_DIR)
    os.chdir(GAME_DIR)
    import pinned; pinned.ensure()
    import game
    if "world_answers" not in game.E.DEFAULT:
        json.dump(dict(no_engine=True), open(out, "w"))
        return
    from console import Console
    c = Console()
    c.handle(""); c.handle(preset)
    busy = c.handle("Ari")[1]
    while busy:
        busy = c.handle("")[1]
    bad, k = [], 0
    while c.mode == "play" and k < 3000:
        g = c.g
        if g.pending is not None:
            k += 1
            p = g.hud().get("world_answers")
            if not panel_ok(p):
                bad.append(f"at {g.age():.1f}: panel {str(p)[:160]}")
            busy = c.handle("" if k % 2 else "2")[1]
        else:
            busy = c.handle("")[1]
        while busy:
            busy = c.handle("")[1]
    g = c.g
    h = g.history
    told = h.get("wa", [])
    feed = [f for f in g.feed if str(f.get("tag", "")).startswith("world_answer")]
    kept = (getattr(g, "review", None) or {}).get("world_kept") or []
    for x in told + feed + kept:
        if SLOT.search(x["text"]):
            bad.append(f"unfilled: {x['text'][:160]}")
    by = {}
    for x in told:
        by.setdefault(x["ring"], {}).setdefault(x["size"], 0)
        by[x["ring"]][x["size"]] += 1
    json.dump(dict(preset=preset, seed=seed, age=round(g.age(), 2), moments=k, bad=bad, told=len(told), by=by,
                   in_story=sum(1 for f in feed if f["tag"] == "world_answer"),
                   events=len(h.get("wa_events", [])), moments_wa=h.get("wa_moments", []), kept=kept,
                   sample=[x["text"] for x in told[:: max(1, len(told) // 4)]][:4]), open(out, "w"), default=str)


def run(preset, seed, out, phase2):
    env = dict(os.environ, CHROMA_GAME=json.dumps({"world_answers": True, "wa_phase2": bool(phase2)}))
    r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "_play", preset, str(seed), out], env=env)
    return json.load(open(out)) if r.returncode == 0 else dict(preset=preset, seed=seed, crash=r.returncode)


def seeds_of(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def main():
    if sys.argv[1:2] == ["_play"]:
        _, _, preset, seed, out = sys.argv
        return play(preset, int(seed), out) or 0
    a = {"presets": "1,2,3,4", "seeds": "1", "jobs": "4", "phase2": "0"}
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        a[args[i].lstrip("-")] = args[i + 1]
    tmp = os.environ.get("TMPDIR", "/tmp")
    jobs = [(p, s) for p in a["presets"].split(",") for s in seeds_of(a["seeds"])]
    with ThreadPoolExecutor(int(a["jobs"])) as ex:
        res = list(ex.map(lambda j: run(j[0], j[1], os.path.join(tmp, f"world_{os.getpid()}_{j[0]}_{j[1]}.json"),
                                        a["phase2"] == "1"), jobs))
    if any(r.get("no_engine") for r in res):
        print("the pinned engine has no world answers")
        return 2
    crash = [r for r in res if "crash" in r]
    bad = [b for r in res for b in r.get("bad", [])]
    for r in res:
        if "crash" in r:
            print(f"preset {r['preset']} seed {r['seed']}: CRASH (exit {r['crash']})"); continue
        dec = sum(1 for m in r["moments_wa"] if m.get("key") == "decide")
        print(f"preset {r['preset']} seed {r['seed']}: age {r['age']}, {r['moments']} moments; {r['told']} told lines "
              f"({r['in_story']} in the story) {r['by']}; {r['events']} sphere events; {len(r['moments_wa']) - dec} asks or "
              f"figures, {dec} decisions; kept {[(x['ring'], x['level']) for x in r['kept']]}")
        for x in r["sample"] + [x["text"] for x in r["kept"]][:2]:
            print("      " + x)
    ok = [r for r in res if "crash" not in r]
    told = sorted(r["told"] for r in ok)
    print(f"W1  lives played to their end with world answers on: {len(ok)} of {len(res)}")
    print(f"W2  problems: {len(bad)}" + "".join("\n      " + b for b in bad[:8]))
    if told:
        print(f"W3  told lines a life: fewest {told[0]}, median {told[len(told) // 2]} (WA2 band: at least 3, median 10 or more)")
    return 0 if not crash and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
