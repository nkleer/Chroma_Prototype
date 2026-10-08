"""How many colours an adult's identity holds (DECISIONS.md CHECK rows: "three is rare" vs "about one in five").
Identity as the engine labels it (engine.identity_path: a colour joins above .22, leaves below .18), at ages 30, 40, 50
and 60, among people alive at that age.
    python3 -B chroma-engine/tools/colour_count.py ENGINE_DIR earth|seed on|off LIVES YEARS SEED OUT.json"""
import sys, os, json, collections
d, libk, world, N, Y, seed, out = sys.argv[1:8]
os.environ["CHROMA_ENGINE"] = os.path.abspath(d)
import _engine   # the engine to check (tools/_engine.py) and the tree's Library and packs
import numpy as np
import engine as E, batch
batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS
L = batch.load_batch("earth", packs=list(batch.PACKS)) if libk == "earth" else None
Pd = dict(E.DEFAULT); Pd["world"] = world == "on"
o = E.run(N=int(N), years=int(Y), seed=int(seed), lib=L, P=Pd)
W, M = o["W_hist"], o["M_hist"]
death = {n: t / 52 for n, t, _ in o["died"]}
res = {}
for age in (30, 40, 50, 60):
    if age >= W.shape[0]:
        continue
    c = collections.Counter()
    for n in range(int(N)):
        if death.get(n, 999) <= age:
            continue
        lab = E.identity_path(W[:age + 1, n], M[:age + 1, n])[-1]
        c["unformed" if not lab else "five" if len(lab) == 5 else str(len(lab))] += 1
    res[age] = dict(c)
json.dump(dict(lib=libk, world=world, N=int(N), years=int(Y), seed=int(seed), counts=res), open(out, "w"))
print(libk, world, seed, {a: {k: v for k, v in sorted(c.items())} for a, c in res.items()})
