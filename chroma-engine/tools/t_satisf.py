"""The game's side note (22:25): adult satisfaction lower on the new engine? Mean satisfaction by age, live batch.
python3 chroma-engine/tools/t_satisf.py '{P}' [N] [seed]"""
import sys, json
import numpy as np
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E
from batch import load_batch
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 150; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
o = E.run(N=N, seed=seed, P=P, lib=load_batch("earth"))
h = np.asarray(o["V_hist"]["content"]); pz = np.asarray(o["V_hist"]["peace"]); md = np.asarray(o["V_hist"]["mood"])
print("PARAMS", P)
for nm, x in (("satisfaction", h), ("peace", pz), ("mood", md)):
    print(f"  {nm:12s}", {a: round(float(np.nanmean(x[a])), 3) for a in (20, 30, 40, 50, 60, 70)})
