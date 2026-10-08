"""How rare each moment is: the share of simulated modern Earth lives (birth to 80) that meet it at least once.
A game-side stopgap for the Book of Moments until the engine and the Library tag real-life frequencies.
python3 test/rarity_build.py [lives per preset]   (runs the four Earth presets in parallel, writes rarity.py)"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)


def one(args):
    key, n, seed = args
    import numpy as np, game
    from game import library_for, E, PRESETS
    p = dict(PRESETS[key]); p["start_age"] = 0.0
    g = game.Game(name="R", seed=seed, **p)
    L, _ = library_for("earth")
    o = E.run(N=n, years=80, seed=seed, P=g.P, lib=L)
    sit = (o["sit_n"] > 0).sum(0)
    rd = np.zeros((n, len(o["read_names"])), bool)
    for who, t, j, r in o["read_log"]:
        rd[who, j] = True
    R = o["roles"]
    return dict(n=n, sit=dict(zip(o["sit_names"], sit.tolist())), read=dict(zip(o["read_names"], rd.sum(0).tolist())),
                mark=dict(zip(o["marks"]["names"], (o["marks"]["n"] > 0).sum(0).tolist())),
                role=dict(zip(R["names"], (R["ever"] > 0).sum(0).tolist())))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    t0 = time.time()
    with Pool(4) as pool:
        parts = pool.map(one, [(k, n, 100 + i) for i, k in enumerate("1234")])
    tot = sum(p["n"] for p in parts)
    out = dict(lives=tot)
    for kind in ("sit", "read", "mark", "role"):
        keys = parts[0][kind].keys()
        out[kind] = {k: round(sum(p[kind][k] for p in parts) / tot, 4) for k in keys}
    with open(os.path.join(HERE, "rarity.py"), "w", encoding="utf-8") as f:
        f.write('"""How rare each moment is in modern Earth lives: the share of simulated lives, birth to 80, across the four\n'
                'Earth presets, that meet it at least once. Written by test/rarity_build.py; a stopgap until the engine and the\n'
                'Library tag real-life frequencies."""\n')
        f.write("RARITY = " + json.dumps(out, ensure_ascii=False, indent=0, sort_keys=True) + "\n")
    print(f"{tot} lives in {time.time() - t0:.0f}s; wrote rarity.py")
