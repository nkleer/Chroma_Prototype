"""How rare each moment is (the game's Book of Moments, Emren's "Book and peace" card): the share of simulated modern
Earth lives, birth to 80, that meet each moment (situation or life event), read event, deed (mark) and title or perk at
least once, on the live batch with batch.PACKS on. The same keys as the game's stopgap rarity.py (lives, sit, read, mark,
role), so the game reads it in its place. Four seeds, each drawing its own world.
    python3 calib_v8/rarity_build.py [lives per seed]     (env LIB, PACKS, PACK_DIR, PACK_MOMENTS for a test; OUT)"""
import sys, os, json, time
from multiprocessing import Pool
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); PROTO = os.path.dirname(HERE)
sys.path.insert(0, PROTO)
import engine as E, batch
if os.environ.get("LIB"):
    batch.LIB_DIR = os.environ["LIB"]
PACKS_ = [x for x in os.environ.get("PACKS", "").split(",") if x] or list(batch.PACKS)
PMOM_ = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None


def one(args):
    seed, n = args
    L = batch.load_batch("earth", packs=PACKS_, pack_moments=PMOM_)
    o = E.run(N=n, years=80, seed=seed, lib=L)
    rd = np.zeros((n, len(o["read_names"])), bool)
    for who, t, j, r in o["read_log"]:
        rd[who, j] = True
    R = o["roles"]
    return dict(n=n, sit=dict(zip(o["sit_names"], (o["sit_n"] > 0).sum(0).tolist())),
                read=dict(zip(o["read_names"], rd.sum(0).tolist())),
                mark=dict(zip(o["marks"]["names"], (o["marks"]["n"] > 0).sum(0).tolist())),
                role=dict(zip(R["names"], (R["ever"] > 0).sum(0).tolist())))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    t0 = time.time()
    with Pool(4) as pool:
        parts = pool.map(one, [(s, n) for s in (101, 102, 103, 104)])
    tot = sum(p["n"] for p in parts)
    out = dict(lives=tot, packs=PACKS_, note="share of simulated modern Earth lives, birth to 80, that meet each at least "
               "once (chroma-engine calib_v8/rarity_build.py); rare = under 1 life in 10")
    for kind in ("sit", "read", "mark", "role"):
        out[kind] = {k: round(sum(p[kind].get(k, 0) for p in parts) / tot, 4) for k in parts[0][kind]}
    dst = os.environ.get("OUT") or os.path.join(HERE, "rarity.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"{tot} lives in {time.time() - t0:.0f}s; {len(out['sit'])} moments, {len(out['role'])} titles and perks; wrote {dst}")
