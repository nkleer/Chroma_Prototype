"""Threshold seasons (Emren's point 6) on a batch with seasons: when each stage's season opens, how often each step and the
transforming chance play a moment, and title seasons. python3 chroma-engine/tools/season_check.py <lib dir> [N] [seed] [packs]"""
import sys, json, collections
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch
D = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 150; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
PK = [x for x in (sys.argv[4] if len(sys.argv) > 4 else "").split(",") if x]
PM = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
batch.LIB_DIR = D
L = batch.load_batch("earth", roles=D + "/earth_perks_titles.py", packs=PK, pack_moments=PM)
o = E.run(N=N, years=80, seed=seed, lib=L, P=dict(self_death=True))
src = L["src"]; GR = L["ROLES"]
op = collections.defaultdict(list)
for n, t, k in o["seasons"]:
    op[k].append(t / 52)
def kname(k):
    return E.STAGE_NAMES[k] if k < E.NS else "title " + GR["names"][k - E.NS]
th = collections.defaultdict(list)
for i, x in enumerate(src):
    if x.get("threshold"):
        tk = str(x["threshold"]).strip()
        k = E.STAGE_NAMES.index(tk) if tk in E.STAGE_NAMES else E.NS + GR["ID"][tk[6:].strip()]
        th[k].append((int(x.get("step") or 1), str(x.get("transform") or "").lower() in ("yes", "true", "1"), i))
for k in sorted(op):
    a = np.array(op[k]); who = {n for n, t, kk in o["seasons"] if kk == k}
    print(f"{kname(k)[:40]:40s} opened {len(a):4d} (lives {len(who) / N:.2f}); age p10/50/90 {np.percentile(a, 10):.1f} {np.median(a):.1f} {np.percentile(a, 90):.1f}")
    for st in (1, 2, 3):
        ii = [i for s_, tr, i in th[k] if s_ == st]
        met = (o["sit_n"][:, ii] > 0).any(1) if ii else np.zeros(N, bool)
        print(f"     step {st}: {met.sum() / max(len(who), 1):.2f} of those opened")
    ti = [i for s_, tr, i in th[k] if tr]
    met = (o["sit_n"][:, ti] > 0).any(1) if ti else np.zeros(N, bool)
    print(f"     transforming chance: {met.sum() / max(len(who), 1):.2f} of those opened")
