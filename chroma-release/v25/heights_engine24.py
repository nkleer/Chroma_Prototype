"""v24 (records/v24/scope.md A2, A4; Release's copy of out/heights/heights_engine.py, the A0 baseline's, with
the aims and the engine's own heights added to the record): how often a life left alone reaches each height, in engine
lives with the outer world on, as the game plays Earth. One seed a call; heights_judge.py pools the seeds.

    python3 -B heights_engine24.py <tree> <seed> <N> <years> <out.json> [<px json>]

<px json> (trials only; the record runs the commit's own defaults): switches laid over DEFAULT; upper-case keys set
batch.py's flags before the library loads (for example {"AIMS": true, "aims": true, "heights": true}).

<tree> is a whole repository tree (chroma-engine, chroma-library, chroma-packs). The run is driven by run_steps with
every value sent back unchanged (the same lives as run()), so the peaks over the life can be read at each year's
first week: rungs fall a step a year toward a lower target, and end-of-life values understate them.
Added for v24 (read only when the run has them, so the baseline's reading above is unchanged): per life, the engine's
own heights (o["heights"]: the week each of Known, Notable, Historic was first reached, -1 never) and the aims
(o["aims"]: aims ever taken from the log, the most steps reached of any aim and of its ladder, callings held, aims set by
the player); `aims_names` lists the catalogue; pair40, the two leading colours at 40."""
import json, os, sys, time

tree, seed, N, Y, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
eng = os.path.join(tree, "chroma-engine", "v22-speedpass")
sys.path.insert(0, eng)
import numpy as np
import engine as E, batch
batch.LIB_DIR = os.path.join(tree, "chroma-library"); batch.PACK_DIR = os.path.join(tree, "chroma-packs")
from world_people_base import G, LEAD_KINDS

PX = json.loads(sys.argv[6]) if len(sys.argv) > 6 else {}
for k_, v_ in PX.items():
    if k_.isupper():
        setattr(batch, k_, v_)
L = batch.load_batch("earth", packs=list(batch.PACKS))
P = dict(E.DEFAULT); P["world"] = True
P.update({k_: v_ for k_, v_ in PX.items() if not k_.isupper()})
t0 = time.time()
g = E.run_steps(N=N, years=Y, seed=seed, P=P, lib=L)
rung = stand = rep = None; lead = {k: np.zeros(N, bool) for k in LEAD_KINDS}
p = next(g)
try:
    while True:
        if p.kind == "week" and p.t % 52 == 0:
            WL = p.state.get("WL")
            PP = getattr(WL, "PP", None)
            if PP is not None:
                r = np.floor(PP.rung)
                rung = r if rung is None else np.maximum(rung, r)
                s = np.asarray(PP.standing) if hasattr(PP, "standing") else None
                if s is not None:
                    stand = s if stand is None else np.maximum(stand, s)
                if hasattr(PP, "eyes_rep"):
                    e = PP.eyes_rep.max(1)
                    rep = e if rep is None else np.maximum(rep, e)
                me = PP.slead == -2
                for k in LEAD_KINDS:
                    lead[k] |= (me & (PP.skind == G[k])).any(1)
        p = g.send(p.value)
except StopIteration as done:
    o = done.value
R = o["roles"]; names = list(R["names"]); NT = R["NT"]; ever = np.asarray(R["ever"]).astype(bool)
tier = np.asarray(L["ROLES"]["TIER"]) if "TIER" in L["ROLES"] else np.zeros(len(names), int)
idx = {n: i for i, n in enumerate(names)}
def ev(nm):
    return ever[:, idx[nm]] if nm in idx else np.zeros(N, bool)
summits = [names[i] for i in range(len(names)) if i < len(tier) and tier[i] == 2]
res = dict(tree=tree, px=PX, seed=seed, N=N, years=Y, secs=round(time.time() - t0, 1), NT=NT, names=names, summits=summits,
           ever=[np.nonzero(ever[n])[0].tolist() for n in range(N)],
           rung_peak=rung.tolist() if rung is not None else None, standing_peak=stand.tolist() if stand is not None else None,
           rep_peak=rep.tolist() if rep is not None else None, lead={k: v.tolist() for k, v in lead.items()}, keys=sorted(o),
           lead40=[int(np.argmax(o["W_hist"][40][n])) for n in range(N)] if len(o["W_hist"]) > 40 else None,
           lead_end=[int(np.argmax(np.asarray(o["w"])[n])) for n in range(N)] if np.ndim(o.get("w")) == 2 else None,
           died=np.asarray(o["died"]).tolist() if np.ndim(o.get("died")) == 1 else None)
if len(o["W_hist"]) > 40:   # v24 A4: the two leading colours at 40, as a pair (i < j)
    res["pair40"] = [sorted(int(x_) for x_ in np.argsort(np.asarray(o["W_hist"][40][n]))[-2:]) for n in range(N)]
if isinstance(o.get("heights"), dict):
    res["ht_names"] = list(o["heights"]["names"]); res["ht_week"] = np.asarray(o["heights"]["week"]).tolist()
if isinstance(o.get("aims"), dict):
    A = o["aims"]; best = np.asarray(A["best"]); log = A.get("log") or []
    of = [len(x_["steps"]) for x_ in L["AIMS"]["aims"]] if "AIMS" in L else None
    took = [sorted({r_["aim"] for r_ in log if r_["life"] == n}) for n in range(N)]
    res["aims_names"] = list(A["names"])
    res["aims"] = [dict(took=len(took[n]), steps=int(best[n].max()) if best.shape[1] else 0,
                        frac=round(float(max((best[n, a_] / of[a_] for a_ in range(len(of)) if of[a_]), default=0.0)), 3) if of else None,
                        calling=bool(np.asarray(A["calling"])[n].any()), by_player=bool(np.asarray(A["by_player"])[n].any()))
                   for n in range(N)]
json.dump(res, open(out, "w"))
print(f"seed {seed}: {N} lives x {Y} years in {res['secs']} s; {len(summits)} summits named; rung peak >=3 in "
      f"{int(((rung if rung is not None else np.zeros((N, 1))) >= 3).any(1).sum())} lives")
