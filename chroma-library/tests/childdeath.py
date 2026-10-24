"""Share of all lives that meet 'your child dies' (R15), with the parent's age at each loss. Base batch, no packs.
Usage: childdeath.py <lib dir> <engine copy> [seeds]"""
import sys, os, numpy as np
sys.dont_write_bytecode = True
LIB = os.path.abspath(sys.argv[1]); P = os.path.abspath(sys.argv[2])
SEEDS = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "61,62,63,64").split(",")]
sys.path.insert(0, P); os.chdir(P)
from multiprocessing import Pool
import engine as E, batch as B_
def one(seed):
    B_.LIB_DIR = LIB
    L = B_.load_batch("earth", roles=LIB + "/earth_perks_titles.py", packs=[])
    i = L["names"].index("your child dies"); j = L["names"].index("your child falls seriously ill")
    o = E.run(N=100, years=80, seed=seed, lib=L)
    ages = [t / 52 for (n, t, s) in o["life_events"] if s == i]
    return (o["sit_n"][:, i] > 0).tolist(), ages, (o["sit_n"][:, j] > 0).tolist()
if __name__ == "__main__":
    with Pool(4) as p: out = p.map(one, SEEDS)
    ever = np.concatenate([np.array(a) for a, _, _ in out]); ill = np.concatenate([np.array(c) for _, _, c in out])
    ages = np.array([x for _, b, _ in out for x in b])
    print(f"{LIB}: lives {len(ever)}; lose a child {ever.mean():.3f}; child seriously ill {ill.mean():.3f}; losses {len(ages)}")
    for lo, hi in [(0, 30), (30, 45), (45, 65), (65, 81)]:
        print(f"  parent aged {lo}-{hi}: {((ages >= lo) & (ages < hi)).sum()} losses ({((ages >= lo) & (ages < hi)).sum() / len(ever):.3f} a life)")
