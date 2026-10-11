"""How rare each moment is (the game's Book of Moments, Emren's "Book and peace" card): the share of simulated modern
Earth lives, birth to 80, that meet each moment (situation or life event), read event, deed (mark) and title or perk at
least once, on the live batch with batch.PACKS on and the outer world on, as the game plays modern Earth (presets 1-4 and
Build your own set P["world"]; the world's own moments, traders, two places, a name on the list, only come with it). The
same keys as the game's stopgap rarity.py (lives, sit, read, mark, role), so the game reads it in its place. Seeds 101,
102, ..., each drawing its own world; the table is the same however the seeds are split over machines.
    python3 chroma-engine/tools/rarity_build.py [lives per seed, 500] [seeds, 8]     (env LIB, PACKS, PACK_DIR,
        PACK_MOMENTS for a test; OUT)
    ... [lives] [seeds] --only 105,106,107,108 --parts DIR   run some seeds, each written to DIR/part_<seed>.json
    ... [lives] [seeds] --merge DIR                          the table from DIR's parts (every seed's must be there)"""
import sys, os, json, time
from multiprocessing import Pool
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
HERE = _engine.OUT; PROTO = _engine.ENGINE   # rarity.json to OUT (or OUT_DIR); the live table is the engine's rarity.json
import engine as E, batch
if os.environ.get("LIB"):
    batch.LIB_DIR = os.environ["LIB"]
PACKS_ = [x for x in os.environ.get("PACKS", "").split(",") if x] or list(batch.PACKS)
PMOM_ = json.loads(os.environ.get("PACK_MOMENTS", "{}")) or None


def one(args):
    seed, n = args
    L = batch.load_batch("earth", packs=PACKS_, pack_moments=PMOM_)
    P = dict(E.DEFAULT); P["world"] = True   # the outer world on, as the game plays modern Earth
    o = E.run(N=n, years=80, seed=seed, lib=L, P=P)
    rd = np.zeros((n, len(o["read_names"])), bool)
    for who, t, j, r in o["read_log"]:
        rd[who, j] = True
    R = o["roles"]
    return dict(n=n, sit=dict(zip(o["sit_names"], (o["sit_n"] > 0).sum(0).tolist())),
                read=dict(zip(o["read_names"], rd.sum(0).tolist())),
                mark=dict(zip(o["marks"]["names"], (o["marks"]["n"] > 0).sum(0).tolist())),
                role=dict(zip(R["names"], (R["ever"] > 0).sum(0).tolist())))


def table(parts, lives):
    tot = sum(p["n"] for p in parts)
    out = dict(lives=tot, packs=PACKS_, world=True, note="share of simulated modern Earth lives with the outer world on, "
               "birth to 80, that meet each at least once (chroma-engine tools/rarity_build.py); rare = under 1 life in 10")
    for kind in ("sit", "read", "mark", "role"):
        out[kind] = {k: round(sum(p[kind].get(k, 0) for p in parts) / tot, 4) for k in parts[0][kind]}
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("lives", nargs="?", type=int, default=500)
    ap.add_argument("seeds", nargs="?", type=int, default=8)
    ap.add_argument("--only", default=None)
    ap.add_argument("--parts", default=None)
    ap.add_argument("--merge", default=None)
    a = ap.parse_args()
    n, k = a.lives, a.seeds
    seeds = [101 + i for i in range(k)]
    opt = {f"--{x}": v for x, v in (("only", a.only), ("parts", a.parts), ("merge", a.merge)) if v is not None}
    t0 = time.time()
    if "--merge" in opt:
        parts = [json.load(open(os.path.join(opt["--merge"], f"part_{s}.json"), encoding="utf-8")) for s in seeds]
        if any(p["n"] != n for p in parts):
            raise SystemExit("the parts were run with another number of lives a seed")
    else:
        run_ = [int(x) for x in opt["--only"].split(",")] if "--only" in opt else seeds
        with Pool(min(4, len(run_))) as pool:
            parts = pool.map(one, [(s, n) for s in run_])
        if "--parts" in opt:
            os.makedirs(opt["--parts"], exist_ok=True)
            for s, p in zip(run_, parts):
                with open(os.path.join(opt["--parts"], f"part_{s}.json"), "w", encoding="utf-8") as f:
                    json.dump(p, f, ensure_ascii=False, sort_keys=True)
            print(f"seeds {run_}: {len(run_) * n} lives in {time.time() - t0:.0f}s; parts in {opt['--parts']}")
            if "--only" in opt:
                sys.exit(0)
    out = table(parts, n)
    dst = os.environ.get("OUT") or os.path.join(HERE, "rarity.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"{out['lives']} lives ({k} seeds x {n}) in {time.time() - t0:.0f}s; {len(out['sit'])} moments, "
          f"{len(out['role'])} titles and perks; wrote {dst}")
