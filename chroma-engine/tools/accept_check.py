"""Emren's point 7: how many of a moment's ways the character would go with, is okay with, reluctant about, or against
(explain.before's accept levels), and how fit with their colors is spread. python3 accept_check.py [lives] [years]"""
import os, sys, types, json
import numpy as np
from collections import Counter
PROTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open("/mnt/project-files/chroma-game/prototype/link.py").read()
src = src[:src.rindex("E = load_engine()")]
link = types.ModuleType("link"); link.__file__ = "/mnt/project-files/chroma-game/prototype/link.py"
exec(compile(src, link.__file__, "exec"), link.__dict__)
sys.path.insert(0, PROTO); os.chdir(PROTO)
E = link.load_engine(PROTO)
from batch import load_batch
import explain as X
L = load_batch("earth")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8; Y = int(sys.argv[2]) if len(sys.argv) > 2 else 70
gen = E.run_steps(N=N, years=Y, seed=31, lib=L)
msg = next(gen)
per = Counter(); fits = []; moments = 0; by_stage = {}; rel = []; cl = []; sh_bad = []
while True:
    kind, t, S, v = msg
    if kind == "choose" and t % 4 == 0:
        for n in range(N):
            b = X.before(S, n)
            lv = [o["accept"]["level"] for o in b["options"] if "accept" in o]
            if len(lv) < 3:
                continue
            moments += 1
            c = Counter(lv)
            for k_ in ("would go with it", "okay with it", "reluctant", "against"):
                per[k_] += c[k_] / len(lv)
            st = int(S["stage"][n]); by_stage.setdefault(st, Counter()).update({k_: c[k_] / len(lv) for k_ in c}); by_stage[st]["_n"] += 1
            fits += [o["accept"]["fit"] for o in b["options"] if "accept" in o]
            rel += [o["accept"]["reluctance"] for o in b["options"] if "accept" in o]
            cl += [o["accept"]["clash"] for o in b["options"] if "accept" in o]
            sh_bad.append(sum(x in ("reluctant", "against") for x in lv) / len(lv))
    try:
        msg = gen.send(v)
    except StopIteration:
        break
print(f"{moments} moments; share of a moment's ways at each level:", {k: round(v / moments, 3) for k, v in per.items()})
for st in sorted(by_stage):
    c = by_stage[st]; n_ = c.pop("_n")
    print(f"  {E.STAGE_NAMES[st]:12s}", {k: round(v / n_, 2) for k, v in c.items()})
print("fit percentiles 5/25/50/75/95:", np.round(np.percentile(fits, [5, 25, 50, 75, 95]), 2).tolist())
print("clash percentiles 5/25/50/75/95:", np.round(np.percentile(cl, [5, 25, 50, 75, 95]), 2).tolist())
print("moments with 70% or more of their ways reluctant or against:", round(float(np.mean(np.array(sh_bad) >= 0.7)), 3))
print("reluctance: share > 0:", round(float(np.mean(np.array(rel) > 0)), 2), "mean when > 0:", round(float(np.mean([r for r in rel if r > 0] or [0])), 2))
