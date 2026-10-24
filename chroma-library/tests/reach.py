"""Reach and repeat test: the share of lives that ever meet each moment, the mean count a life, and the spacing between
repeats against each moment's gap. 400 lives (4 x 100, seeds 41-44).
Usage: python3 reach.py <lib dir> <out.json> <engine copy dir> [packs]   (as titles_by_source.py; set PACK_DIR)
Moved here from a scratch copy for the release check (L7, 2026-10-06)."""
import sys, os, json
sys.dont_write_bytecode = True
LIB = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); P = os.path.abspath(sys.argv[3])
PACKS = [x for x in (sys.argv[4] if len(sys.argv) > 4 else "").split(",") if x]
sys.path.insert(0, P); os.chdir(P)
import numpy as np
from multiprocessing import Pool
import engine as E
import batch as B_
def one(seed):
    B_.LIB_DIR = LIB
    L = B_.load_batch("earth", roles=LIB + "/earth_perks_titles.py", packs=PACKS)
    o = E.run(N=100, years=80, seed=seed, lib=L)
    return o["sit_n"].tolist()
if __name__ == "__main__":
    B_.LIB_DIR = LIB
    L = B_.load_batch("earth", roles=LIB + "/earth_perks_titles.py", packs=PACKS)
    with Pool(4) as p: out = p.map(one, [41, 42, 43, 44])
    sn = np.concatenate([np.array(x) for x in out], 0)
    res = []
    for i, s in enumerate(L["src"]):
        gap = s.get("gap") or (s.get("timing") or {}).get("gap_years")
        res.append(dict(name=L["names"][i], tier=s.get("tier"), ever=float((sn[:, i] > 0).mean()), mean=float(sn[:, i].mean()),
                        per_meeter=float(sn[:, i][sn[:, i] > 0].mean()) if (sn[:, i] > 0).any() else 0.0,
                        share=s.get("share"), stages=s.get("stages", ""), age=s.get("age"), rate=s.get("rate"), gap=gap,
                        once=bool(s.get("once"))))
    json.dump(dict(packs=PACKS, lib=LIB, moments=res), open(OUT, "w"), indent=0)
    def span(r):
        a = r["age"] or (0, 110); return max(1.0, min(80, a[1]) - a[0])
    over = []
    for r in res:
        g = r["gap"]
        if r["once"] and r["per_meeter"] > 1.05: over.append((r["name"], "once", round(r["per_meeter"], 2)))
        elif g:
            lo = float(str(g).split("-")[0]) if isinstance(g, str) else float(g[0] if isinstance(g, (list, tuple)) else g)
            if lo > 0 and r["per_meeter"] > span(r) / lo + 1: over.append((r["name"], g, round(r["per_meeter"], 2)))
    sh = [(r["name"], r["share"], round(r["ever"], 3)) for r in res if r["share"]]
    rat = sorted(r["ever"] / float(r["share"]) for r in res if r["share"])
    tiers = {}
    for r in res: tiers[r["tier"]] = tiers.get(r["tier"], 0) + r["mean"]
    print(f"packs {PACKS or 'none'}: {len(res)} moments; a life holds " + ", ".join(f"{k} {v:.1f}" for k, v in tiers.items()))
    print(f"share moments {len(rat)}: reach/share median {rat[len(rat) // 2]:.2f}, min {rat[0]:.2f}, max {rat[-1]:.2f}")
    print(f"moments over their gap or once: {len(over)} {over[:10]}")
    ev = sorted([r for r in res if r["tier"] == "life event"], key=lambda r: -r["mean"])
    print("life events, most a life:", [(r["name"], round(r["mean"], 1)) for r in ev[:5]])
