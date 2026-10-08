"""Scratch: at what age each threshold season opens, against the age windows of its moments (next2 batch).
Runs on the earth.py in engine_pin/ (the live batch has no seasons): for the staged batch, use a scratch copy of the
prototype with chroma-library/staging/next2/earth.py and earth_perks_titles.py and the engine's latest files in
engine_pin/, then run from the prototype folder with OMP_NUM_THREADS=1."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, game
from game import library_for, E, PRESETS
n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
p = dict(PRESETS["1"]); p["start_age"] = 0.0
g = game.Game(name="R", seed=9, **p)
L, _ = library_for("earth")
o = E.run(N=n, years=80, seed=9, P=g.P, lib=L)
ages = collections.defaultdict(list)
for who, t, k in o["seasons"]:
    if k < E.NS:
        ages[E.STAGE_NAMES[k]].append(t / 52)
win = {}
for i, x in enumerate(L["src"]):
    if x.get("threshold"):
        win.setdefault(x["threshold"], L["AGE"][i].tolist())
for st, a in ages.items():
    a = np.array(a); lo, hi = win.get(st, [0, 0])
    inside = ((a + 22 / 52 >= lo) & (a + 1 / 52 <= hi)).mean()
    print(f"{st:12s} opens at age p10 {np.percentile(a, 10):.1f} median {np.median(a):.1f} p90 {np.percentile(a, 90):.1f}; moments' window {lo:.0f}-{hi:.0f}; seasons that overlap it {inside:.2f}")
