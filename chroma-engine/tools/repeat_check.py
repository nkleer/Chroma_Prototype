"""Emren's point 12 (2026-10-05 20:39): the same life event again and again. python3 calib_v8/repeat_check.py '{P}' [N] [seed]
Per life event (a child version counts as its original): lives that meet it, lives that meet it twice or more, and how
often a repeat comes within two years of the time before. The game tells life events, so these are what the player sees."""
import sys, json, numpy as np
from collections import defaultdict
sys.path.insert(0, "/mnt/project-files/chroma-engine/prototype")
import engine as E
from batch import load_batch
import os, batch as B_
if os.environ.get("LIB"):                      # LIB=<folder> for a staged or draft batch
    B_.LIB_DIR = os.environ["LIB"]
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 11
L = load_batch("earth", roles="/mnt/project-files/chroma-library/earth_perks_titles.py")
o = E.run(N=N, seed=seed, P=P, lib=L)
ROOT = np.asarray(L.get("ROOT", np.arange(L["S"])))
times = defaultdict(lambda: defaultdict(list))
for n, t, s in o["life_events"]:
    times[int(ROOT[s])][n].append(t / 52)
rows = []
tot = rep = rep2 = 0
for r, per in times.items():
    cnt = np.array([len(v) for v in per.values()])
    gaps = [b - a for v in per.values() for a, b in zip(v, v[1:])]
    tot += cnt.sum(); rep += (cnt - 1).sum(); rep2 += sum(g < 2 for g in gaps)
    tm = L["src"][r].get("timing", {}).get("times", "") if isinstance(L["src"][r].get("timing"), dict) else ""
    rows.append((L["names"][r], len(per) / N, np.mean(cnt >= 2) * len(per) / N, (cnt - 1).sum() / N,
                 np.mean(np.array(gaps) < 2) if gaps else 0, max(cnt), tm[:60]))
print("PARAMS", P, os.environ.get("LIB", ""))
ch_ = np.array([sum(1 for n_, t_, s_ in o["life_events"] if n_ == i and L["names"][s_] == "a child is born") for i in range(N)])
print(f"children born a life {ch_.mean():.2f}; never a child {np.mean(ch_ == 0):.2f}")
print(f"life events per life {tot / N:.1f}; repeats per life {rep / N:.1f} ({rep / tot:.0%} of all); repeats within 2 years {rep2 / N:.2f} per life")
print(f"{'event':48s} {'meet':>5s} {'2+':>5s} {'rep/life':>8s} {'<2y':>5s} {'max':>3s}  timing")
for nm, m, m2, rpl, g2, mx, tm in sorted(rows, key=lambda x: -x[3])[:40]:
    print(f"{nm[:48]:48s} {m:5.2f} {m2:5.2f} {rpl:8.2f} {g2:5.2f} {mx:3d}  {tm}")
