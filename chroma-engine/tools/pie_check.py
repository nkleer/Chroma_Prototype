"""Does a batch tilt the pie? python3 calib_v8/pie_check.py [lib dir or 'live'] [N] [seed]
The mean color weights at 20, 40 and 70, and the most met everyday moments with the color their options lean to."""
import sys
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, "/mnt/project-files/chroma-engine/prototype")
import engine as E, batch
D = sys.argv[1] if len(sys.argv) > 1 else "live"; N = int(sys.argv[2]) if len(sys.argv) > 2 else 200
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 11
if D != "live":
    batch.LIB_DIR = D
L = batch.load_batch("earth", roles=(D + "/earth_perks_titles.py") if D != "live" else None)
o = E.run(N=N, years=80, seed=seed, lib=L)
w = np.asarray(o["W_hist"])
for a in (20, 40, 70):
    print(f"pie at {a}:", " ".join(f"{c} {x:.3f}" for c, x in zip("WUBRG", w[a].mean(0))))
cnt = o["sit_n"].mean(0); ev = np.asarray(L["EVERYDAY"]) if "EVERYDAY" in L else np.ones(L["S"], bool)
M = np.asarray(L["M"])   # S, K, C option color profiles
for i in np.argsort(-cnt)[:10]:
    lean = M[i].mean(0)
    print(f"  {L['names'][i][:46]:46s} {cnt[i]:7.1f} a life   options lean " + " ".join(f"{c}{x:.2f}" for c, x in zip("WUBRG", lean)))
