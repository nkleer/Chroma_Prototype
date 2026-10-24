"""Lifetime title and perk shares on a lib folder, base batch only, with where each first gain came from. 400 lives.
Usage: python3 titles_by_source.py <lib dir with earth.py and earth_perks_titles.py> <out.json> [engine prototype dir]
Run it on a COPY of the engine (cp chroma-engine/prototype/*.py to scratch): it imports the engine from that dir. (Library 2026-10-06)"""
import sys, os, json, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.environ.get("CHROMA_ROOT", "/mnt/project-files"), "chroma-env"))   # folder names: chroma-env/paths.py
from paths import P as PATHS
P = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else PATHS["engine_v23"]
LIB = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2])
sys.path.insert(0, P); os.chdir(P)
from multiprocessing import Pool
import engine as E
import batch as B_
B_.LIB_DIR = LIB
CAT = LIB + "/earth_perks_titles.py"
def one(seed):
    B_.LIB_DIR = LIB
    L = B_.load_batch("earth", roles=CAT, packs=[])
    o = E.run(N=100, years=80, seed=seed, lib=L)
    R = o["roles"]; names = L["ROLES"]["names"]
    first = {}
    for (pn, t, i, what, how) in R["log"]:
        if what == "gained" and (pn, i) not in first:
            first[(pn, i)] = str(how)
    src = collections.defaultdict(collections.Counter)
    for (pn, i), h in first.items():
        src[names[i]][h] += 1
    return dict(ever={names[i]: int(v) for i, v in enumerate(R["ever"].sum(0))}, src={k: dict(v) for k, v in src.items()},
                share={names[i]: float(L["ROLES"]["share"][i]) for i in range(len(names))})
if __name__ == "__main__":
    with Pool(4) as p: out = p.map(one, [11, 12, 13, 14])
    ever = collections.Counter(); src = collections.defaultdict(collections.Counter)
    for o in out:
        ever.update(o["ever"])
        for k, v in o["src"].items(): src[k].update(v)
    res = {k: dict(cat=out[0]["share"][k], ever=ever[k] / 400, src=src[k].most_common(4)) for k in ever}
    json.dump(res, open(OUT, "w"), indent=0)
    bad = sorted(res.items(), key=lambda kv: -(kv[1]["ever"] - kv[1]["cat"]))
    for k, r in bad[:45]:
        print("%-34s cat %.3f ever %.3f | %s" % (k[:34], r["cat"], r["ever"], "; ".join(f"{h[:38]} {c}" for h, c in r["src"][:3])))
