"""Early retirement and leaving the faith (engine, 2026-10-05): [LIB=<folder>] [ROLES=<catalogue>] python3
calib_v7/exits_check.py '{P}' [N] [seed]
Share at work by age against US employment by age (relative to age 50, so the engine's own level of work in midlife,
which is a separate matter, does not count), when people retire, the faith held by age, who leaves it and when."""
import sys, os, json, numpy as np
from collections import Counter
sys.path.insert(0, "/mnt/project-files/chroma-engine/prototype")
import engine as E, batch as B_
if os.environ.get("LIB"):
    B_.LIB_DIR = os.environ["LIB"]
L = B_.load_batch("earth", roles=os.environ.get("ROLES"))
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
for k_, v_ in P.items():
    if isinstance(v_, list):
        P[k_] = tuple(tuple(x) if isinstance(x, list) else x for x in v_)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 11
o = E.run(N=N, seed=seed, P=P, lib=L)
K = o["K_hist"]; CAR = E.KNAMES.index("career"); FAI = E.KNAMES.index("faith")
alive = o.get("alive_hist")
# US employment-population ratio by age, relative to 50 to 54 (BLS CPS annual averages, about 2023): 55-59 .91, 60-64 .71,
# 65-69 .42, 70-74 .23, 75+ .10; read at the middle of each band
REAL = {50: 1.0, 57: 0.91, 62: 0.71, 67: 0.42, 72: 0.23, 77: 0.10}
w50 = (K[50][:, CAR] > 0).mean()
print("PARAMS", P)
print("at work by age (share; relative to 50; real relative):")
for a in (30, 40, 45, 50, 55, 57, 60, 62, 65, 67, 70, 72, 75, 77, 80):
    w = (K[a][:, CAR] > 0).mean()
    print(f"  {a}: {w:.2f}  rel {w / max(w50, 1e-9):.2f}" + (f"  real {REAL[a]:.2f}" if a in REAL else ""))
ret = [c for c in o["commits"] if c[2] == CAR and c[3] == "retired"]
ra = np.array([c[1] / 52 for c in ret])
if len(ra):
    print("retired per life %.2f; age at retiring: 10%% %.1f, 25%% %.1f, median %.1f, 75%% %.1f, 90%% %.1f; before 60: %.2f, before pension age: %.2f"
          % (len(ra) / N, *np.percentile(ra, [10, 25, 50, 75, 90]), (ra < 60).mean(), (ra < E.DEFAULT["retire_age"]).mean()))
print("faith held at 10/15/20/25/30/40/60/80:", [round(float((K[a][:, FAI] > 0).mean()), 2) for a in (10, 15, 20, 25, 30, 40, 60, 80)])
fc = Counter(c[3] for c in o["commits"] if c[2] == FAI)
print("faith changes per life:", {k: round(v / N, 2) for k, v in fc.items()})
lv = np.array([c[1] / 52 for c in o["commits"] if c[2] == FAI and c[3] == "left"])
if len(lv):
    print("age at leaving: 25%% %.1f, median %.1f, 75%% %.1f; share of lives that ever left: %.2f"
          % (*np.percentile(lv, [25, 50, 75]), len({c[0] for c in o["commits"] if c[2] == FAI and c[3] == "left"}) / N))
inh = {c[0] for c in o["commits"] if c[2] == FAI and c[3] == "inherited"}
left = {c[0] for c in o["commits"] if c[2] == FAI and c[3] == "left"}
print("raised in a faith %.2f; of them left at some point %.2f; holding a faith at 40 among them %.2f, among the others %.2f"
      % (len(inh) / N, len(inh & left) / max(len(inh), 1), np.mean([K[40][n, FAI] > 0 for n in inh]) if inh else 0,
         np.mean([K[40][n, FAI] > 0 for n in range(N) if n not in inh])))
if o.get("roles") is not None:
    G = L["ROLES"]; ev = o["roles"]["ever"]
    for nm in ("retiree", "left the faith", "out of work", "regular worshipper", "believer on the big days", "activist in a cause", "seeker", "convert"):
        if nm in G["names"]:
            i_ = G["names"].index(nm); print(f"  title {nm}: {ev[:, i_].mean():.2f} (catalogue {G['share'][i_]:.2f})")
