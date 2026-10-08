"""Emren's point 7 (2026-10-05 20:39): does color inertia only ever build up? python3 chroma-engine/tools/inertia_check.py '{P}' [N] [seed]
By age: plasticity, steadiness, experience settling, how far a person moves in a year, distance from the deep core;
raw rank-order stability (before the survey's measurement error); movement in years with and without a transition."""
import os, sys, json, numpy as np
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E
import schwartz as SW
from batch import load_batch
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 11
L = load_batch("earth", roles=os.path.join(_engine.LIBRARY, "earth_perks_titles.py"))
o = E.run(N=N, seed=seed, P=P, lib=L)
W = np.asarray(o["W_hist"]); V = o["V_hist"]; Mh = np.asarray(o["M_hist"])
PP = dict(E.DEFAULT); PP.update(P)
print("PARAMS", P)
print("age  plast  steady  settle  moved/yr  from core  breakthroughs/yr  conversions/yr")
brk = np.array([b[1] / 52 for b in o["breaks"]])
conv = np.array([c[1] / 52 for c in o["conv"]]) if "conv" in o else None
for a in (8, 12, 16, 20, 25, 30, 40, 50, 60, 70, 79):
    moved = 0.5 * np.abs(W[a + 1] - W[a]).sum(1).mean() if a + 1 < len(W) else np.nan
    core = np.asarray(V["core"][a]); dist = 0.5 * np.abs(W[a] - core).sum(1).mean()
    nb = np.mean((brk >= a) & (brk < a + 1)) * len(brk) / N if brk is not None and len(brk) else 0
    nc = np.mean((conv >= a) & (conv < a + 1)) * len(conv) / N if conv is not None and len(conv) else 0
    print(f"{a:3d}  {np.mean(V['plast'][a]):.3f}  {np.mean(V['steady'][a]):.3f}  {np.mean(np.log1p(Mh[a] / PP['M0'])):.2f}"
          f"   {moved:.4f}    {dist:.4f}       {nb:.3f}            {nc:.3f}")
st = SW.stability(o, ((20, 22), (45, 47), (30, 42), (40, 52), (50, 62), (16, 66), (60, 72)))
print("raw rank-order stability (survey reads x0.8):", st)
# movement in the year after a commitment starts or ends, against years without one, ages 20-70
ch = np.zeros((N, len(W)), bool)
for (n, t, kk, why, *_) in o["commits"]:
    y_ = int(t // 52)
    if 20 <= y_ < 70: ch[n, y_] = True
mv = 0.5 * np.abs(W[1:] - W[:-1]).sum(2).T          # N x years-1: movement from year y to y+1
yrs = np.arange(20, 70)
m_ch = mv[:, yrs][ch[:, yrs]].mean(); m_no = mv[:, yrs][~ch[:, yrs]].mean()
print(f"moved in a year with a commitment change {m_ch:.4f}, without {m_no:.4f}, ratio {m_ch / m_no:.2f}")
print("rites at ages:", {r: round(float(np.median([x['age'] for x in o['rites'] if x['to'] == r])), 1) for r in E.STAGE_NAMES[1:]})
rows = SW.compare(o)
print("SCORECARD", f"{sum(r[-1] for r in rows)} of {len(rows)}", "; ".join(f"{k} {v:+.2f}/{t:+.2f}" for k, v, t, lo, hi, src, ok in rows if "stab" in k or "satisf" in k))
_c = np.asarray(o["V_hist"]["content"]); _g = 0.5 * np.abs(np.asarray(o["A_hist"]) - W).sum(-1)
print("satisfaction 30/50/70", round(float(_c[30].mean()), 3), round(float(_c[50].mean()), 3), round(float(_c[70].mean()), 3),
      "| want gap 30/50", round(float(_g[30].mean()), 3), round(float(_g[50].mean()), 3))
