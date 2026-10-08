"""How often each threshold season opens, and how often each of its three steps plays a moment (scratch, next2 batch).
python3 test/season_rate.py [lives] [preset]
Runs on the earth.py in engine_pin/ (the live batch has no seasons): for the staged batch, use a scratch copy of the
prototype with chroma-library/staging/next2/earth.py and earth_perks_titles.py and the engine's latest files in
engine_pin/, then run from the prototype folder with OMP_NUM_THREADS=1."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, game
from game import library_for, E, PRESETS
n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
key = sys.argv[2] if len(sys.argv) > 2 else "1"
p = dict(PRESETS[key]); p["start_age"] = 0.0
g = game.Game(name="R", seed=5, **p)
L, _ = library_for("earth")
o = E.run(N=n, years=80, seed=5, P=g.P, lib=L)
src = L["src"]; names = o["sit_names"]
th = {i: (str(x.get("threshold") or ""), int(x.get("step") or 1), str(x.get("transform") or "")) for i, x in enumerate(src) if x.get("threshold")}
opened = collections.Counter()
for who, t, k in o["seasons"]:
    opened[k] += 1
print("seasons opened (count over", n, "lives):", {E.STAGE_NAMES[k] if k < E.NS else f"title {k}": v for k, v in sorted(opened.items())})
step = collections.defaultdict(lambda: np.zeros(n, bool))
for i, (stg, st, tr) in th.items():
    step[(stg, st)] |= o["sit_n"][:, i] > 0
for (stg, st), v in sorted(step.items()):
    print(f"  {stg:12s} step {st}: {v.mean():.2f} of lives")
for i, (stg, st, tr) in sorted(th.items(), key=lambda x: (x[1][0], x[1][1])):
    print(f"    {stg:12s} {st} {'T' if tr else ' '} {(o['sit_n'][:, i] > 0).mean():.2f}  {names[i]}  requires: {str(src[i].get('requires') or '')[:90]}")
