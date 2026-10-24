"""Stage 1 of v24: read the heights of lives left alone (heights_engine.py) and played lives (heights_play.py) and write
the baseline (records/v24/scope.md, A0).

    python3 -B heights_judge.py --engine 'DIR/eng_*.json' [--play DIR] [--out REPORT]

Release's reading of plan.md §5 on v23.1's state (the engine's names, out/heights/README.md says where each lives):
  Known     a sphere rung of 3 or 4 at any time (pillar or leader; the plan's "rung 4 or 5" counted from 1),
            "good name in town", or a master's stand-in ("master craftsperson", "a maker's hallmark": no master's
            perk exists)
  Notable   "known across the country" or "a household name", or any summit title (TIER 2)
  Historic  head of a state ("head of government"; no head-of-state title exists), of an order (no such title exists)
            or of a movement ("founder of a movement", or leading a movement setting); or a work or discovery that
            outlives them, read two ways: strict (none: nothing is checked after death) and broad (the perks below)
Each height is read as "at least": Known or higher, Notable or higher, Historic."""
import argparse, glob, json, math, os, time
from collections import Counter, defaultdict

KNOWN_ITEMS = ["good name in town"]
MASTER = ["master craftsperson", "a maker's hallmark"]
REACH = ["known across the country", "a household name"]
STATE = ["head of government"]
MOVEMENT = ["founder of a movement"]
WORKS = ["a finding that held up", "a method others use", "a dataset others use", "works in collectors' hands",
         "a reform with your name on it"]
COL = "WUBRG"


def parts(ever, summits, rung, lead):
    """The components a life reached; `ever` is a set of names."""
    p = {}
    p["rung3"] = rung is not None and max(rung) >= 3
    p["rung4"] = rung is not None and max(rung) >= 4
    p["good_name"] = any(x in ever for x in KNOWN_ITEMS)
    p["master"] = any(x in ever for x in MASTER)
    p["reach"] = any(x in ever for x in REACH)
    p["summit"] = any(x in ever for x in summits)
    p["state"] = any(x in ever for x in STATE)
    p["movement"] = any(x in ever for x in MOVEMENT) or bool((lead or {}).get("movement"))
    p["works"] = any(x in ever for x in WORKS)
    p["known"] = p["rung3"] or p["good_name"] or p["master"]
    p["notable"] = p["reach"] or p["summit"]
    p["historic"] = p["state"] or p["movement"]
    p["historic_broad"] = p["historic"] or p["works"]
    p["ge_known"] = p["known"] or p["notable"] or p["historic"]
    p["ge_notable"] = p["notable"] or p["historic"]
    # a stricter reading of Known, for Emren's choice: a sphere's leader (the top rung), not its pillar
    p["known_strict"] = p["rung4"] or p["good_name"] or p["master"]
    p["ge_known_strict"] = p["known_strict"] or p["notable"] or p["historic"]
    return p


KEYS = ["ge_known", "ge_known_strict", "ge_notable", "historic", "historic_broad", "known", "rung3", "rung4", "good_name", "master",
        "notable", "reach", "summit", "state", "movement", "works"]


def share(xs):
    n = len(xs); k = sum(xs)
    if not n:
        return "n/a"
    p = k / n; se = math.sqrt(p * (1 - p) / n) if n > 1 else 0
    return f"{p:.3f} +- {se:.3f} ({k}/{n})"


ALL_NAMED = KNOWN_ITEMS + MASTER + REACH + STATE + MOVEMENT + WORKS
MISSING = set()


def engine_lives(pattern):
    lives = []
    for f in sorted(glob.glob(pattern)):
        d = json.load(open(f)); names = d["names"]
        MISSING.update(x for x in ALL_NAMED if x not in names)
        for n in range(d["N"]):
            ever = {names[i] for i in d["ever"][n]}
            rung = d["rung_peak"][n] if d.get("rung_peak") else None
            lead = {k: v[n] for k, v in (d.get("lead") or {}).items()}
            p = parts(ever, d["summits"], rung, lead)
            p["seed"] = d["seed"]; p["lead40"] = (d.get("lead40") or [None] * d["N"])[n]
            lives.append(p)
    return lives


def play_lives(d):
    lives = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        r = json.load(open(f))
        if "ever" not in r:
            continue
        p = parts(set(r["ever"]), r["summits"], r.get("rung_peak"), r.get("lead"))
        p.update(policy=r["policy"] + ("+aims" if r.get("read_goals") else ""), preset=str(r["preset"]), seed=r["seed"],
                 well=r.get("well"), ful=r.get("ful"))
        lives.append(p)
    return lives


def table(groups, keys=KEYS):
    out = []
    w = max(len(g) for g in groups) + 2
    for k in keys:
        out.append(f"  {k:<15}" + "".join(f"{share([l[k] for l in ls]):>26}" for ls in groups.values()))
    return [" " * 17 + "".join(f"{g:>26}" for g in groups)] + out


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--engine", required=True); a.add_argument("--play"); a.add_argument("--out")
    a = a.parse_args()
    L = engine_lives(a.engine)
    rep = [f"v24 Stage 1 (records/v24/scope.md A0): heights reached on v23.1 (e69b3bf), {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
           "", __doc__.split("\n\n", 2)[2].strip(), "",
           f"Lives left alone: engine lives, Earth with its packs, world on, 100 years; {len(L)} lives over seeds "
           f"{sorted({l['seed'] for l in L})}. Share of lives, +- one standard error.", ""]
    rep += [f"Names the reading uses that the run does not know: {sorted(MISSING) or 'none'}", ""]
    by_seed = {f"seed {s}": [l for l in L if l["seed"] == s] for s in sorted({l["seed"] for l in L})}
    rep += table({"all": L, **by_seed}, KEYS)
    rep += ["", "By the colour leading at 40 (Known or higher, Notable or higher, Historic):"]
    by_c = defaultdict(list)
    for l in L:
        if l["lead40"] is not None:
            by_c[COL[l["lead40"]]].append(l)
    rep += table({c: by_c[c] for c in COL if by_c[c]}, ["ge_known", "ge_known_strict", "ge_notable", "historic", "historic_broad"])
    if a.play:
        P = play_lives(a.play)
        pols = sorted({l["policy"] for l in P})
        rep += ["", f"Played lives: the Game as the page plays it, Release's picks/impact.py policies; {len(P)} lives, "
                f"presets {sorted({l['preset'] for l in P})}, seeds {sorted({l['seed'] for l in P})}.", ""]
        rep += table({p: [l for l in P if l["policy"] == p] for p in pols}, KEYS)
        rep += ["", "  well-being reading (mean of the review's 'well'):"]
        for p in pols:
            ws = [l["well"] for l in P if l["policy"] == p and l["well"] is not None]
            rep.append(f"    {p:<14} {sum(ws) / len(ws):.3f} over {len(ws)} lives" if ws else f"    {p:<14} n/a")
    txt = "\n".join(rep) + "\n"
    if a.out:
        open(a.out, "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
