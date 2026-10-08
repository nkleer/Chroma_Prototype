"""Own death (self_death on): share of lives ended before 30, 50, 65 and 80 and by what. python3 chroma-engine/tools/death_check.py <lib dir> [N] [seed]
Real modern Earth (US period life table, both sexes): about .01 by 30, .04 by 50, .15 by 65, .40 by 80."""
import sys
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch
D = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 400; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 3
batch.LIB_DIR = D
L = batch.load_batch("earth", roles=D + "/earth_perks_titles.py")
o = E.run(N=N, years=85, seed=seed, lib=L, P=dict(self_death=True))
dd = o["died"]; ages = np.array([t / 52 for _, t, _ in dd]); cz = [c for _, _, c in dd]
kind = lambda c: "own act" if c.startswith("through") else c.split(" ")[0]
for a in (30, 50, 65, 80):
    m = ages < a
    print(f"died before {a}: {m.sum() / N:.3f}  causes", dict(Counter(kind(c) for c, x in zip(cz, m) if x)))
print(f"life events a life {len(o['life_events']) / N:.1f}")
