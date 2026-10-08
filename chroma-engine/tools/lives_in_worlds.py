"""Lives in worlds (chroma-world/calibration-and-tests.md 2.2, 2.5): the scorecard, identities at 40, job loss and births
in recessions, satisfaction in recessions, world lines a year, speed; the world on against the same lives with it off.
    python3 -B chroma-engine/tools/lives_in_worlds.py <world seed> [lives] [years] [on|off]      (env PACKS as in score_packs)"""
import sys, os, json, time
import numpy as np
sys.dont_write_bytecode = True
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
PROTO = _engine.ENGINE
import engine as E, schwartz as SW, batch
ws = int(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 300; Y = int(sys.argv[3]) if len(sys.argv) > 3 else 80
on = (sys.argv[4] if len(sys.argv) > 4 else "on") == "on"
packs = [x for x in os.environ.get("PACKS", "science,politics,stage").split(",") if x]
L = batch.load_batch("earth", packs=packs)
P = dict(E.DEFAULT); P.update(world=on, world_seed=ws)
LOG = tuple(range(0, N, max(1, N // 30)))
t0 = time.time()
o = E.run(N=N, years=Y, seed=100 + ws, lib=L, P=P, log_lives=LOG)
sec = time.time() - t0
out = dict(world_seed=ws, on=on, N=N, years=Y, seconds=round(sec, 1))
if Y >= 67:
    rows = SW.compare(o)
    out["scorecard"] = sum(r[-1] for r in rows); out["rows"] = {r[0]: round(float(r[1]), 3) for r in rows}
# identities at 40 (E.identity with its buffer, year by year)
A40 = min(40, Y); W40 = np.asarray(o["W_hist"][A40]); n_col = []
for i in range(N):
    Wi = np.array([o["W_hist"][y][i] for y in range(A40 + 1)]); Mi = np.array([o["M_hist"][y][i] for y in range(A40 + 1)])
    lab = E.identity_path(Wi, Mi)[-1]
    n_col.append(len(lab) if lab else 0)
n_col = np.array(n_col)
out["identity_at_40"] = {"one": round(float(np.mean(n_col == 1)), 3), "two": round(float(np.mean(n_col == 2)), 3),
                         "three+": round(float(np.mean((n_col >= 3) & (n_col < 5))), 3), "five (none stands out)": round(float(np.mean(n_col == 5)), 3)}
out["mean_colors_40"] = np.round(W40.mean(0), 3).tolist()
# job loss and births by the world's state (monthly world course; life events log)
names = L["names"]; CAR = E.KIDX["career"]
JL = {i for i, k in enumerate(L["ENDS"]) if k == CAR}
BB = {i for i, nm in enumerate(names) if "a baby on the way" in nm}
lev = o["life_events"]
if on and o.get("world"):
    H = o["world"]["hist"]; rec = np.zeros(Y * 52 + 1, bool); un = np.zeros(Y * 52 + 1)
    for h_ in H:   # published figures (world_link.hist)
        t = h_["t"]; rec[t:t + 4] = h_["recession"]; un[t:t + 4] = h_["unemp"] or 0.0
    wk = np.array([t for (_, t, s) in lev]); ss = np.array([s for (_, _, s) in lev])
    adult = wk >= 20 * 52
    jl = np.isin(ss, list(JL)) & adult; bb = np.isin(ss, list(BB)) & adult
    wr = rec[20 * 52:].mean() if rec[20 * 52:].any() else 0.0
    def rate(m, cond):
        nw = max(cond[20 * 52:].sum(), 1)
        return m[cond[wk]].sum() / nw
    out["recession_share_of_adult_weeks"] = round(float(wr), 3)
    if 0 < wr < 1:
        out["job_loss_per_week_recession_vs_not"] = [round(float(rate(jl, rec)), 4), round(float(rate(jl, ~rec)), 4)]
        out["births_per_week_recession_vs_not"] = [round(float(rate(bb, rec)), 4), round(float(rate(bb, ~rec)), 4)]
        sat = np.array(o["V_hist"]["content"])            # years x N
        yrec = np.array([rec[y * 52: y * 52 + 52].mean() > 0.5 for y in range(len(sat))])
        ad = np.arange(len(sat)) >= 20
        out["satisfaction_recession_vs_not"] = [round(float(sat[yrec & ad].mean()), 3) if (yrec & ad).any() else None,
                                                 round(float(sat[~yrec & ad].mean()), 3)]
    out["unemployment_mean_sd"] = [round(float(un.mean()), 2), round(float(un.std()), 2)]
    out["world_lines_a_year"] = round(len(o["world"]["log"]) / Y, 1)
    out["eras"] = sorted({str(h["era"]) for h in H})
    # cast: no close friend at the end of the run (alive column 2 is the closest friend)
    out["no_close_friend_at_end"] = round(float(np.mean(np.asarray(o["alive"])[:, 2] == 0)), 3)
print(json.dumps(out))
