# paired felt vs true odds over offered options: staged (with chance) or live batch. python3 felt_gap.py staged|live
import os, sys, types, numpy as np
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
PROTO = _engine.ENGINE
E = _engine.with_steps()   # the engine with run_steps(), the game's pause points
import batch
if sys.argv[1] == "staged":
    batch.LIB_DIR = os.path.join(_engine.LIBRARY, "staging")
    L = batch.load_batch("earth", roles=os.path.join(_engine.LIBRARY, "earth_perks_titles.py"))
else:
    L = batch.load_batch("earth")
N = 10; gen = E.run_steps(N=N, years=75, seed=33, lib=L); msg = next(gen)
H, T, ST, CH, B = [], [], [], [], []
while True:
    kind, t, S, v = msg
    if kind == "choose" and t % 3 == 0:
        P = S["P"]; m = S["m"]; alpha = S["alpha"]
        fk = P["fit"] * (m * (alpha - alpha.mean(1, keepdims=True))[:, None, :]).sum(2)
        lg = P["gain"] * ((m * (S["sig"] + S["f_tot"])[:, None, :]).sum(2) + fk - S["diff"]) + (S["pbump"] if "pbump" in S else 0)
        pt = 1 / (1 + np.exp(-lg)); ok = S["mask"] & ~S["do_nothing"]
        for n in range(N):
            k = np.nonzero(ok[n])[0]
            H += S["p_hat"][n, k].tolist(); T += pt[n, k].tolist(); ST += [int(S["stage"][n])] * len(k)
            ch = L.get("CHANCE"); CH += (ch[S["s"][n], k].tolist() if ch is not None else [np.nan] * len(k))
    try:
        msg = gen.send(v)
    except StopIteration:
        break
H, T, ST, CH = map(np.array, (H, T, ST, CH))
lgt = lambda p: np.log(np.clip(p, 1e-4, 1 - 1e-4) / (1 - np.clip(p, 1e-4, 1 - 1e-4)))
print(sys.argv[1], "options", len(H), "mean felt %.3f true %.3f; mean felt-true %.3f; mean |felt-true| %.3f; logit gap mean %.2f"
      % (H.mean(), T.mean(), (H - T).mean(), np.abs(H - T).mean(), (lgt(H) - lgt(T)).mean()))
if not np.isnan(CH).all():
    print("  mean chance %.3f" % np.nanmean(CH))
for st in range(6):
    s_ = ST == st
    if s_.sum():
        print(f"  {E.STAGE_NAMES[st]:12s} felt {H[s_].mean():.3f} true {T[s_].mean():.3f} logit gap {(lgt(H[s_]) - lgt(T[s_])).mean():+.2f}")
