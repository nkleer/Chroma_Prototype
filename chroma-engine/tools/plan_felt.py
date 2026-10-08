"""Plan felt odds at the start of a plan, and how often such plans are reached in time (game's finding: 28% at .99+).
python3 calib_v7/plan_felt.py '{P}'"""
import os, sys, json
import numpy as np
PROTO = "/mnt/project-files/chroma-engine/prototype"
sys.path.insert(0, PROTO); os.chdir(PROTO)
import engine as E
from batch import load_batch
L = load_batch("earth")
PX = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
o = E.run(N=int(os.environ.get("N", 160)), years=70, seed=5, lib=L, P=PX)
g = o["goals"]
beg = {(r["life"], r["id"]): r for r in g if r.get("kind") == "plan" and r["what"] == "begins"}
end = {}
for r in g:
    if r.get("kind") == "plan" and (r["life"], r["id"]) in beg and r["what"] != "begins":
        end.setdefault((r["life"], r["id"]), r["what"])
f = np.array([b["felt"] for b in beg.values()]); ok = np.array([end.get(k) == "achieved" for k in beg])
print(PX, "plans", len(f), "felt percentiles 5/25/50/75/95", np.round(np.percentile(f, [5, 25, 50, 75, 95]), 2).tolist(),
      "share >= .99:", round(float((f >= 0.99).mean()), 2), ">= .9:", round(float((f >= 0.9).mean()), 2))
for lo, hi in ((0, .3), (.3, .6), (.6, .9), (.9, .99), (.99, 1.01)):
    sel = (f >= lo) & (f < hi)
    if sel.sum():
        print(f"  felt {lo:.2f}-{hi:.2f}: n={sel.sum():5d} reached {ok[sel].mean():.2f}")
from collections import Counter
print("  ends:", Counter(end.values()).most_common(6))
