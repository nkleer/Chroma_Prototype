"""The land with the world alone (v25 lane D, Release row LN2; chroma-world/spheres/land-checks-measure.md run C).

Each world seed runs once calm (the warming held at the birth's level, so extremes do not rise) and once with high
extremes (the "high" climate path: about +2.4 degrees over 80 years). The land runs with wa_land and its drift
(wa_land_dev) on and its moments and ways (wa_land_play) off, so no life tends or changes a stretch: the stretches move
only by their recovery, the hazards' hits, the town's uses and the times. One life is simulated because the engine
needs one; it holds no land way. Every town's three stretches are read each year.

    OMP_NUM_THREADS=1 python3 -B chroma-engine/tools/land_alone.py [--seeds 41,42,43,44] [--years 80] [--json FILE]

LN2 passes when, pooled over the seeds:
  calm:          each stretch's town mean (health and wildness) drifts .15 or less from its start in any year; a single
                 town's scar from a strike (a fire takes .3 of a wood, which regrows .03 a year) is a hazard, not drift,
                 so the largest single-town drift is printed for information only
  high extremes: the field's and the water's mean health fall .05 to .20 more than in calm by the last year (the
                 towns' mean; read against the calm run of the same seed, so recovery and hits common to both cancel)
Exit 0 on a pass, 1 on a fail. --json writes the yearly means and the per-town drifts (under OUT_DIR when relative;
never into the repository). About 2 minutes a run on one core, so about 16 minutes for the eight runs.
"""
import argparse, json, os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np
import engine as E, batch
import world_hooks as WH
import world_land as WLD

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", default="41,42,43,44")
ap.add_argument("--years", type=int, default=80)
ap.add_argument("--json", default=None)
A = ap.parse_args()
SEEDS = [int(s) for s in A.seeds.split(",") if s]
CALM_MAX, HIGH_LO, HIGH_HI = 0.15, 0.05, 0.20
ST = WLD.STRETCHES

# the land's yearly state, recorded after each Land._year
REC = []
_orig_year = WLD.Land._year


def _year(self, t, a):
    _orig_year(self, t, a)
    REC.append((self.h.copy(), self.wd.copy(), float(np.mean(np.asarray(self.W.extremes, float)))))


WLD.Land._year = _year
_orig_warm = WH.HooksMixin._warming
HOLD = [False]


def _warming(self, t):
    """Calm: the warming held at the birth's level from the birth on (the world before the birth as the engine has it)."""
    w = _orig_warm(self, t)
    if HOLD[0] and self.clim_t0 is not None and t >= self.clim_t0:
        return self._warming_now()
    return w


WH.HooksMixin._warming = _warming
L = batch.load_batch("earth")


def run(seed, calm):
    REC.clear(); HOLD[0] = calm
    P = dict(E.DEFAULT)
    P.update(world=True, world_seed=seed, world_answers=True, wa_land=True, wa_land_dev=True, wa_land_play=False,
             world_cfg=dict(climate="middle" if calm else "high"))
    t0 = time.time()
    E.run(N=1, years=A.years, seed=seed, lib=L, P=P)
    if not REC:
        sys.exit("land_alone: the land never ran (is wa_land wired on this engine?)")
    H = np.array([r[0] for r in REC]); Wd = np.array([r[1] for r in REC]); X = np.array([r[2] for r in REC])
    return dict(H=H, Wd=Wd, X=X, sec=time.time() - t0)


out = dict(seeds=SEEDS, years=A.years, runs={})
calm_drift = []; fall = {"field": [], "water": []}
for s in SEEDS:
    c = run(s, True); h = run(s, False)
    # drift from the first recorded year (the land's start as the life begins): the towns' mean, per stretch
    mh, mw = c["H"].mean(1), c["Wd"].mean(1)                                                  # years x stretches
    dm = np.maximum(np.abs(mh - mh[0]).max(0), np.abs(mw - mw[0]).max(0))                     # stretches
    dc = np.maximum(np.abs(c["H"] - c["H"][0]).max(0), np.abs(c["Wd"] - c["Wd"][0]).max(0))   # towns x stretches (information)
    calm_drift.append(float(dm.max()))
    row = dict(calm_max_drift=round(float(dm.max()), 4), calm_drift_by_stretch={ST[j]: round(float(dm[j]), 4) for j in range(3)},
               calm_single_town_max={ST[j]: round(float(dc[:, j].max()), 4) for j in range(3)},
               extremes_calm=[round(float(c["X"][0]), 3), round(float(c["X"][-1]), 3)],
               extremes_high=[round(float(h["X"][0]), 3), round(float(h["X"][-1]), 3)], seconds=[round(c["sec"]), round(h["sec"])])
    for j, nm in ((0, "field"), (2, "water")):
        f_ = float(c["H"][-1][:, j].mean() - h["H"][-1][:, j].mean())
        fall[nm].append(f_); row[f"high_fall_{nm}"] = round(f_, 4)
    row["calm_mean_health_by_year"] = {ST[j]: c["H"][:, :, j].mean(1).round(4).tolist() for j in range(3)}
    row["calm_mean_wild_by_year"] = {ST[j]: c["Wd"][:, :, j].mean(1).round(4).tolist() for j in range(3)}
    row["high_mean_health_by_year"] = {ST[j]: h["H"][:, :, j].mean(1).round(4).tolist() for j in range(3)}
    out["runs"][s] = row
    print(f"seed {s}: calm largest mean drift {row['calm_max_drift']:.3f} {row['calm_drift_by_stretch']} (one town at most "
          f"{row['calm_single_town_max']}); high extremes fall "
          f"field {row['high_fall_field']:+.3f} water {row['high_fall_water']:+.3f}; extremes {row['extremes_calm']} / "
          f"{row['extremes_high']}; {row['seconds']} s", flush=True)

ok_calm = max(calm_drift) <= CALM_MAX
mf, mw = float(np.mean(fall["field"])), float(np.mean(fall["water"]))
ok_high = HIGH_LO <= mf <= HIGH_HI and HIGH_LO <= mw <= HIGH_HI
out["LN2"] = dict(calm_max_drift=round(max(calm_drift), 4), calm_rule=f"<= {CALM_MAX}", calm_ok=ok_calm,
                  high_fall_field=round(mf, 4), high_fall_water=round(mw, 4), high_rule=f"{HIGH_LO} to {HIGH_HI}", high_ok=ok_high,
                  result="pass" if ok_calm and ok_high else "fail")
print(f"LN2 calm: largest mean drift {max(calm_drift):.3f} (<= {CALM_MAX}) {'ok' if ok_calm else 'MISS'}")
print(f"LN2 high extremes: mean fall field {mf:.3f}, water {mw:.3f} ({HIGH_LO} to {HIGH_HI}) {'ok' if ok_high else 'MISS'}")
print(f"LN2 {out['LN2']['result']}")
if A.json:
    p = A.json if os.path.isabs(A.json) else os.path.join(_engine.OUT, A.json)
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
sys.exit(0 if ok_calm and ok_high else 1)
