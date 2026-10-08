"""Scratch: how many life events a life meets (birth to 80), per decade, and the most frequent ones.
python3 test/event_rate.py [lives] [preset]  (runs on the earth.py in engine_pin/)"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, game
from game import library_for, E, PRESETS
n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
key = sys.argv[2] if len(sys.argv) > 2 else "1"
p = dict(PRESETS[key]); p["start_age"] = 0.0
g = game.Game(name="R", seed=11, **p)
L, _ = library_for("earth")
o = E.run(N=n, years=80, seed=11, P=g.P, lib=L)
lev = o["life_events"]; names = o["sit_names"]
per = np.zeros(n); dec = np.zeros(8)
for who, t, s in lev:
    per[who] += 1; dec[min(int(t / 520), 7)] += 1
print(f"{len(names)} situations; life events per life: mean {per.mean():.1f} median {np.median(per):.0f} max {per.max():.0f}")
print("per decade (mean per life):", " ".join(f"{10 * i}s {dec[i] / n:.1f}" for i in range(8)))
c = collections.Counter(names[s] for _, _, s in lev)
for nm, k in c.most_common(12):
    print(f"   {k / n:5.2f} per life  {nm}")
