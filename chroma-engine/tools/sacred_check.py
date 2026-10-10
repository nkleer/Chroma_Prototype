"""S5 sacred lines: the v22.4 refit targets (chroma-release/records/v22.4/scope.md, row G9), on the engine of a tree.

Lives on Earth with the packs and the outer world on, with the switch `sacred` and what it needs (sph_events, c3_inst,
sph_haunts, sph_hours, cur_on) switched on where the engine's DEFAULT has them off; everything else as DEFAULT. The
lines, the years each colour led and the money not had come from the world's People (its audit arrays), read at the
end of each run through run_steps (STATE "WL").
  lines   lines per colour in proportion to its leading years: for each colour, its share of the lines formed over its
          share of the years it led the life's colours; ok when every colour's ratio is within --tol of 1 (1/tol to
          tol). The scope gives no number for "in proportion"; --tol defaults to 1.5, as S1's and S3's counts.
  money   money lost per lead colour within 1.2x: each life's lead colour is the one that led it longest; the mean money
          not had by holding a line, per life, in each lead colour; ok when the largest is within 1.2x of the smallest
          (also printed: per held offer, which does not count to the target).

    python3 -B chroma-engine/tools/sacred_check.py lines|money|all [--lives 300] [--years 80] [--seeds 31,32,33,34]
        [--tol 1.5] [--jobs 4]
Run it in a checkout of the commit (or set CHROMA_ENGINE; tools/_engine.py). Exit code 0 when the target(s) pass.
The report's last line per target reads "s5_lines: ok ..." or "s5_money: FAIL ...". """
import sys, os, time, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import numpy as np

NEEDS = ("sacred", "sph_events", "c3_inst", "sph_haunts", "sph_hours", "cur_on")


def one(args):
    """One seed: (lines per engine colour, lead years per colour, lead colour per life, money lost per life, offers
    held per life, the People's counts, whether each life formed a line)."""
    N, Y, seed = args
    E = _engine.with_steps()
    import batch
    batch.LIB_DIR = _engine.LIBRARY; batch.PACK_DIR = _engine.PACKS
    L = batch.load_batch("earth", packs=list(batch.PACKS))
    Pd = dict(E.DEFAULT); Pd["world"] = True
    Pd.update({k: True for k in NEEDS if not Pd.get(k)})
    g = E.run_steps(N=N, years=Y, seed=seed, lib=L, P=Pd)
    msg = next(g); WL = None
    while True:
        kind, t, S, val = msg
        if WL is None and S.get("WL") is not None:
            WL = S["WL"]
        try:
            msg = g.send(val)
        except StopIteration:
            break
    PP = WL.PP
    C = PP.sac_lead_y.shape[1]
    lines = np.zeros(C)
    for k in PP.sac_line[PP.sac_line >= 0]:
        lines[int(PP.sac_col[int(k)])] += 1
    return (lines, PP.sac_lead_y.sum(0), np.argmax(PP.sac_lead_y, 1), PP.sac_lost[:, 0].copy(),
            PP.sac_held.sum(1).copy(), dict(PP.sac_n), (PP.sac_line >= 0).any(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", choices=["lines", "money", "all"])
    ap.add_argument("--lives", type=int, default=300)
    ap.add_argument("--years", type=int, default=80)
    ap.add_argument("--seeds", default="31,32,33,34")
    ap.add_argument("--tol", type=float, default=1.5)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    seeds = [int(x) for x in a.seeds.split(",") if x.strip()]
    E = _engine.with_steps()
    from world_people import COLORS
    t0 = time.time()
    jobs = [(a.lives, a.years, s) for s in seeds]
    if a.jobs > 1 and len(jobs) > 1:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(min(a.jobs, len(jobs))) as ex:
            res = list(ex.map(one, jobs))
    else:
        res = [one(j) for j in jobs]
    lines = sum(r[0] for r in res); lead_y = sum(r[1] for r in res)
    lead = np.concatenate([r[2] for r in res]); lost = np.concatenate([r[3] for r in res])
    held = np.concatenate([r[4] for r in res]); has = np.concatenate([r[6] for r in res])
    cnt = {}
    for r in res:
        for k, v in r[5].items():
            cnt[k] = cnt.get(k, 0) + v
    forced = [k for k in NEEDS if not E.DEFAULT.get(k)]
    print(f"S5 sacred lines: engine {_engine.ENGINE}; {a.lives} lives x {a.years} years, seeds {a.seeds} (pooled), world on"
          f"{'; switched on for the check: ' + ', '.join(forced) if forced else '; every needed switch on in DEFAULT'}"
          f" ({time.time() - t0:.0f} s)")
    print("  counts: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())))
    print(f"  lives with a line: {int(has.sum())} of {len(has)}; lines formed {int(lines.sum())}")
    bad = 0
    if a.target in ("lines", "all"):
        ls = lines / max(lines.sum(), 1); ys = lead_y / max(lead_y.sum(), 1e-9)
        ratio = np.where(ys > 0, ls / np.maximum(ys, 1e-12), np.nan)
        print("  lines by colour: " + ", ".join(f"{COLORS[c]} {int(lines[c])} lines, {ys[c]:.3f} of lead years, ratio "
                                               f"{ratio[c]:.2f}" for c in range(len(COLORS))))
        none = [COLORS[c] for c in range(len(COLORS)) if ys[c] > 0 and lines[c] == 0]
        dev = np.nanmax(np.maximum(ratio, 1 / np.maximum(ratio, 1e-12))) if lines.sum() and not none else np.inf
        ok = bool(np.isfinite(dev) and dev <= a.tol)
        bad += not ok
        print(f"s5_lines: {'ok' if ok else 'FAIL'} worst colour "
              f"{f'{dev:.2f}x' if not none else 'none: ' + ' '.join(none) + ' led but formed no line'} from its share of "
              f"lead years (target within {a.tol}x)")
    if a.target in ("money", "all"):
        per = np.array([lost[lead == c].mean() if (lead == c).any() else np.nan for c in range(len(COLORS))])
        nl = np.array([int((lead == c).sum()) for c in range(len(COLORS))])
        ph = np.array([lost[lead == c].sum() / max(held[lead == c].sum(), 1) for c in range(len(COLORS))])
        print("  money not had by lead colour (mean per life; per held offer): " + ", ".join(
            f"{COLORS[c]} {per[c]:.4f} ({nl[c]} lives; {ph[c]:.4f})" for c in range(len(COLORS))))
        lo, hi = np.nanmin(per), np.nanmax(per)
        spread = hi / lo if lo > 0 else np.inf
        ok = bool(np.isfinite(spread) and spread <= 1.2 and not np.isnan(per).any())
        bad += not ok
        zero = [COLORS[c] for c in range(len(COLORS)) if not per[c] > 0]
        print(f"s5_money: {'ok' if ok else 'FAIL'} money lost per lead colour "
              f"{f'{spread:.2f}x apart' if not zero else 'none lost by ' + ' '.join(zero)} (target within 1.2x)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
