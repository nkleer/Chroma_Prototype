"""R15: a child's death and a child's serious illness on the real moments (the Library's staged next3 batch): share of
parents (lives that ever held children) who lose a child by 60, 75 and 85, and who see a child fall seriously ill.
Targets (earth-child-illness.lib): death about 4 in 100 parents by 60, 10 by 75, 16 by 90; illness about 1 in 10 by 50,
1 in 6 by 65, 1 in 3 by 85.  python3 -B calib_v10/child_deaths.py <lives> <years> <seed> [lib dir] [roles file]"""
import sys, os, json
import numpy as np
sys.dont_write_bytecode = True
PROTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, PROTO)
import engine as E, batch
N = int(sys.argv[1]); Y = int(sys.argv[2]); sd = int(sys.argv[3])
LIBD = sys.argv[4] if len(sys.argv) > 4 else "/mnt/project-files/chroma-library"
ROLES = sys.argv[5] if len(sys.argv) > 5 else "/mnt/project-files/chroma-library/drafts/next3/earth_perks_titles.py"
batch.LIB_DIR = LIBD
pm = {p: os.path.join(LIBD, f"earth_{p}.py") for p in batch.PACKS if os.path.exists(os.path.join(LIBD, f"earth_{p}.py"))}
L = batch.load_batch("earth", roles=ROLES, pack_moments=pm or None)
o = E.run(N=N, years=Y, seed=sd, lib=L, log_lives=tuple(range(N)), P=json.loads(os.environ.get("P", "{}")) or None)
par = np.zeros(N, bool); dth = np.full(N, np.inf); ill = np.full(N, np.inf); died = np.full(N, np.inf)
for n in range(N):
    for e in o["events"][n]:
        if "role" in e and e["role"].get("kind") == "children" and e["role"].get("what") == "gained":
            par[n] = True
        if "commitment" in e and e["commitment"].get("kind") == "children":
            par[n] = True
        if "death" in e and e["death"].get("role") == "child":
            dth[n] = min(dth[n], e["death"]["age"])
        if e.get("situation") == "your child falls seriously ill":
            ill[n] = min(ill[n], e["age"])
for n_, t_, c_ in o.get("died", []):
    died[n_] = min(died[n_], t_ / 52)
res = dict(lives=N, parents=int(par.sum()), child_death_all_lives=round(float(np.isfinite(dth).mean()), 3))   # C-X5: .10 to .12
for a_ in (50, 60, 65, 75, 85):
    alive_ = par & (died > a_)
    res[f"child_death_by_{a_}"] = round(float((dth[par] <= a_).mean()), 3)
    res[f"child_ill_by_{a_}"] = round(float((ill[par] <= a_).mean()), 3)
print(json.dumps(res))
