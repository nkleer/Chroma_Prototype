"""The whole scorecard (schwartz.compare) on a staged batch with packs: LIB=<dir> PACKS=a,b PACK_MOMENTS='{...}'
python3 chroma-engine/tools/score_packs.py '{P}' [N] [seed]   (ROLES=<catalogue> when LIB has none)"""
import sys, os, json
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, schwartz as SW, batch
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 600; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 21
if os.environ.get("LIB"):
    batch.LIB_DIR = os.environ["LIB"]
PK = [x for x in os.environ.get("PACKS", "").split(",") if x]; PM = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None
L = batch.load_batch("earth", roles=os.environ.get("ROLES") or (os.path.join(batch.LIB_DIR, "earth_perks_titles.py") if os.environ.get("LIB") else None), packs=PK, pack_moments=PM)
o = E.run(N=N, seed=seed, P=P, lib=L)
rows = SW.compare(o)
print("PARAMS", P, "N", N, "seed", seed, "packs", PK)
print(f"SCORECARD {sum(r[-1] for r in rows)} of {len(rows)}")
for k, v, t, lo, hi, src, ok in rows:
    print(f"  {'ok ' if ok else 'MISS'} {k:44s} {v:+.2f}  target {t:+.2f} ({lo:+.2f} to {hi:+.2f})")
