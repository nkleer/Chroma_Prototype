"""v22.5 refit read (F9 and the means targets, chroma-ideas/means/modifiers.md; chroma-ideas/realism/v22.5-realism-list.md):
Earth with the live packs, world on or off, every switch as DEFAULT plus PX. Prints one JSON line of the rows the refit
fits, then a short table.
    PX='{json}' python3 -B chroma-engine/tools/v225_read.py <lives> <years> <seed> <on|off>
Rows: health, money and ties by age (mean, the middle 80%'s width, the share at 5% or less, health's share at 98% or
more); ever partnered, ever a parent and ever in a faith by 50 and by the end; deaths before 30/50/65/80/90/100 (when
self_death is on) and their causes; per life the enemies, hidden wrongs and defiances; White's breaking-the-law ratio
(its rate per life over the others'); how far the pie moves per decade at 25-35, 45-55 and 65-75."""
import sys, os, json, time
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch
N, Y, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); world = sys.argv[4] == "on"
L = batch.load_batch("earth", packs=list(batch.PACKS))
P = dict(E.DEFAULT); P.update(json.loads(os.environ.get("PX", "{}"))); P["world"] = world
t0 = time.time()
o = E.run(N=N, years=Y, seed=seed, lib=L, P=P)
R = np.asarray(o["R_hist"]); W = np.asarray(o["W_hist"])   # years+1 x N x 5
MON, HEA, TIE = 0, 2, 3
dage = np.full(N, np.inf); cause = {}
for n_, t_, c_ in o["died"]:
    dage[n_] = t_ / 52; cause[n_] = c_
out = dict(lives=N, years=Y, seed=seed, world=world, sec=round(time.time() - t0))
AGES = [a for a in (10, 15, 20, 30, 40, 50, 60, 70, 80, 90) if a <= Y]
for nm, i in (("health", HEA), ("money", MON), ("ties", TIE)):
    rows = {}
    for a in AGES:
        live = dage > a
        if live.sum() < 5:
            continue
        x = R[a, live, i]
        rows[a] = dict(mean=round(float(x.mean()), 3), w80=round(float(np.percentile(x, 90) - np.percentile(x, 10)), 3),
                       lo5=round(float((x <= 0.05).mean()), 3), hi98=round(float((x >= 0.98).mean()), 3))
    out[nm] = rows
# commitments ever started (or inherited, for a faith), by 50 and by the end
KS = {"partner": E.KIDX["partner"], "children": E.KIDX["children"], "faith": E.KIDX["faith"]}
first = {k: np.full(N, np.inf) for k in KS}
for c_ in o["commits"]:
    n_, t_, kk, how = c_[0], c_[1], c_[2], c_[3]
    for k, ki in KS.items():
        if kk == ki and how in ("start", "inherited"):
            first[k][n_] = min(first[k][n_], t_ / 52)
for k in KS:
    out[k] = dict(by50=round(float((first[k] <= 50).mean()), 3), ever=round(float(np.isfinite(first[k]).mean()), 3))
if o["died"]:
    out["died_before"] = {a: round(float((dage < a).mean()), 3) for a in (30, 50, 65, 80, 90, 100) if a <= Y}
    out["causes"] = dict(Counter(("own act" if str(c).startswith("through") else c) for c in cause.values()).most_common(10))
mk = o["marks"]; MN = mk["names"]; MC = np.asarray(mk["n"])
for nm in ("made an enemy", "hid a wrong", "defied an authority", "broke the law", "used drugs", "took a life"):
    if nm in MN:
        out["mark: " + nm] = round(float(MC[:, MN.index(nm)].mean()), 2)
if "broke the law" in MN:   # White's rate per life over the rest, by the colour leading at 40
    lead = np.argmax(W[min(40, Y)], 1); bl = MC[:, MN.index("broke the law")]
    if (lead == 0).any() and (lead != 0).any() and bl[lead != 0].mean() > 0:
        out["white_law_ratio"] = round(float(bl[lead == 0].mean() / bl[lead != 0].mean()), 2)
mv = {}
for a0, a1 in ((25, 35), (45, 55), (65, 75)):
    if a1 <= Y:
        live = dage > a1
        mv[f"{a0}-{a1}"] = round(float(np.abs(W[a1, live] - W[a0, live]).sum(1).mean() / 2), 3)
out["pie_move"] = mv
print(json.dumps(out))
for nm in ("health", "money", "ties"):
    print(f"{nm:7s}" + "".join(f"  {a}: {r['mean']:.2f} w{r['w80']:.2f} lo{r['lo5']:.2f}" + (f" hi{r['hi98']:.2f}" if nm == "health" else "")
                              for a, r in out[nm].items()))
