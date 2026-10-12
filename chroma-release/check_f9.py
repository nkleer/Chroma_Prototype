"""v22.5 rows K6 to K13, K15 and K16 (records/v22.5/scope.md): F9's life-course targets (F9.1 to F9.40), F14's colours
settling with age, F17's deeds and F19's mind, judged from the Engine's reader chroma-engine/tools/v225_read.py.

    python3 -B chroma-release/check_f9.py run --repo DIR [--commit SHA] [--seeds 41-52] [--lives 300] [--years 106]
                                              [--world on] [--px JSON] [--jobs N] [--log N] [--out DIR] [--no-record]
    python3 -B chroma-release/check_f9.py judge DIR [--commit SHA] [--no-record]     # judge a finished run again

`run` lives each seed in its own process: the reader of the checkout runs inside it (runpy) on the checkout's live
engine, Library and packs (CHROMA_ROOT and CHROMA_ENGINE set to the checkout), with every switch as DEFAULT plus --px
(default {"self_death": true}, so deaths come from the life; F9's deaths need it). Its JSON line is kept, and this
script adds what the rows need that the reader leaves out: F9.1 and F9.6 among the lives alive at 50 and by the colour
leading at 40, F9.5, F9.24 and F9.33 on their own denominators, causes of death by age, F9.37 to F9.40 at every age
and by colour, F14's movement, F17's deeds by colour and F19's stress and contentment by age. One file a seed,
seed<k>.json, in --out (default out/f9_<time>/). 106 years so that "living past 105" can be seen.

`judge` pools the seeds (shares and means weighted by each seed's lives; a median is the median of the seeds' medians,
with their range printed) and judges every row against its target in records/v22.5/scope.md. One results line per
table: f9_parents, f9_partners, f9_homes, f9_work, f9_illness, f9_deaths, f9_means, f14_settle, f17_deeds, f19_mind,
PASS when every judged target of the table holds, else MISS; a target the run cannot count (a counter the reader does
not have yet) leaves its table MISS and says so. Reported, not judged: F9.40's sizes, F14's lives that move late, the
colour leans of F17. Report: <out>/f9_report.txt. Exit code 0 when every table passes.
"""
import json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = "WUBRG"
TABLES = ["f9_parents", "f9_partners", "f9_homes", "f9_work", "f9_illness", "f9_deaths", "f9_means", "f14_settle",
          "f17_deeds", "f19_mind"]


# ---------------------------------------------------------------------------------------------------- one seed
def seed_main(repo, seed, lives, years, world, px, log):
    """Lives one seed through the checkout's reader and prints one JSON line: the reader's `out` plus `x`, ours."""
    import contextlib, io, runpy
    reader = os.path.join(repo, "chroma-engine", "tools", "v225_read.py")
    os.environ["CHROMA_ROOT"] = repo
    os.environ.setdefault("CHROMA_ENGINE", os.path.join(repo, "chroma-engine", "v22-speedpass"))
    os.environ["PX"] = json.dumps(px)
    os.environ["LOG"] = str(log)
    sys.path.insert(0, os.path.dirname(reader))
    sys.argv = [reader, str(lives), str(years), str(seed), world]
    with contextlib.redirect_stdout(io.StringIO()):
        g = runpy.run_path(reader, run_name="__main__")
    print(json.dumps(dict(out=g["out"], x=extras(g, years)), default=lambda o: o.item() if hasattr(o, "item") else str(o)))


def extras(g, Y):
    o, N, R, W, dage = g["o"], g["N"], g["R"], g["W"], g["dage"]
    first, ev_ages = g["first"], g["ev_ages"]
    MON, HEA, TIE = g["MON"], g["HEA"], g["TIE"]
    lead = np.argmax(W[min(40, Y)], 1)
    x = dict(N=N)
    a50 = dage > 50
    x["alive50"] = int(a50.sum())
    for k, nm in (("children", "par50"), ("partner", "part50")):
        hit = (first[k] <= 50) & a50
        x[nm] = [int(hit.sum()), int(a50.sum())]
        x[nm + "_by"] = {COLS[c]: [int((hit & (lead == c)).sum()), int((a50 & (lead == c)).sum())] for c in range(5)}
    leave = ev_ages({"the children leave home"})
    x["leave_first"] = [min(v) for v in leave.values()]
    sev = ev_ages({"a frightening diagnosis", "a serious accident or illness"})
    a80 = dage > 80
    x["sev50"] = [sum(1 for v in sev.values() if min(v) < 50), N]
    x["sev80"] = [sum(1 for n_, v in sev.items() if a80[n_] and min(v) <= 80), int(a80.sum())]
    x["dead_before"] = {a: [int((dage < a).sum()), N] for a in (30, 50, 65, 80, 90, 100) if a <= Y}
    x["past105"] = int((dage > 105).sum()) if Y > 105 else None
    x["causes_u40"], x["causes_65"] = {}, {}
    for n_, t_, c_ in o["died"]:
        c_ = "own act" if str(c_).startswith("through") else str(c_)
        b = "causes_u40" if t_ / 52 < 40 else ("causes_65" if t_ / 52 >= 65 else None)
        if b:
            x[b][c_] = x[b].get(c_, 0) + 1
    x["death_ages"] = [round(t_ / 52, 2) for _, t_, _ in o["died"]]
    # means at every age, the living
    def by_age(i, f, a0, a1):
        return {a: f(R[a, dage > a, i]) for a in range(a0, min(a1, Y) + 1) if (dage > a).sum() >= 5}
    w80 = lambda v: float(np.percentile(v, 90) - np.percentile(v, 10))
    x["health_w80"] = by_age(HEA, w80, 30, 90)
    x["ties_lo5"] = by_age(TIE, lambda v: float((v <= .05).mean()), 15, 90)
    x["ties_lo5_kid"] = {a: float((R[a, :, TIE] <= .05).mean()) for a in range(3, 15)}
    x["ties_mean15"] = float(R[15, dage > 15, TIE].mean()) if Y >= 15 else None
    x["money_lo5_15"] = float((R[15, dage > 15, MON] <= .05).mean()) if Y >= 15 else None
    # health at 98% or more: the longest run a life has from 30; below 25% outside a serious time
    Rh = R[:, :, HEA]
    run_ok, low, yrs = 0, 0, 0
    for n_ in range(N):
        end = int(min(Y, dage[n_])) if np.isfinite(dage[n_]) else Y
        r_ = mx_ = 0
        for a in range(30, end + 1):
            r_ = r_ + 1 if Rh[a, n_] >= .98 else 0
            mx_ = max(mx_, r_)
        run_ok += mx_ <= 1
        serious = sev.get(n_, [])
        last = end - 3 if np.isfinite(dage[n_]) else end + 1
        for a in range(30, end + 1):
            if a >= last or any(s <= a <= s + 2 for s in serious):
                continue
            yrs += 1
            low += Rh[a, n_] < .25
    x["health_run_ok"] = [run_ok, N]
    x["health_low_other"] = [int(low), int(yrs)]
    # F9.40: the colours in the means, by the colour leading at 40, the living at each age
    def grp(i, a0, a1, f):
        out = {}
        for c in range(5):
            vals = [R[a, (dage > a) & (lead == c), i] for a in range(a0, min(a1, Y) + 1)]
            v = np.concatenate([v_ for v_ in vals if len(v_)]) if any(len(v_) for v_ in vals) else np.array([])
            out[COLS[c]] = [f(v) if len(v) >= 5 else None, int(len(v))]
        return out
    x["c_health_w80"] = grp(HEA, 30, 70, w80)
    x["c_ties_late"] = grp(TIE, 60, 85, lambda v: float(v.mean()))
    x["c_money_mean"] = grp(MON, 30, 70, lambda v: float(v.mean()))
    x["c_money_w80"] = grp(MON, 30, 70, w80)
    # F14: half the summed change of the five weights over each decade, the living at its end
    for a0, a1 in ((25, 35), (45, 55), (65, 75)):
        if a1 <= Y:
            live = dage > a1
            x[f"move_{a0}"] = [float(np.abs(W[a1, live] - W[a0, live]).sum(1).sum() / 2), int(live.sum())]
    # F17: deeds per life, all and by colour
    mk = o["marks"]; MN = list(mk["names"]); MC = np.asarray(mk["n"])
    x["deeds"] = {}
    for nm in ("made an enemy", "hid a wrong", "defied an authority", "broke the law", "used drugs", "refused someone in need"):
        if nm in MN:
            col = MC[:, MN.index(nm)]
            x["deeds"][nm] = dict(all=[float(col.sum()), N],
                                  by={COLS[c]: [float(col[lead == c].sum()), int((lead == c).sum())] for c in range(5)})
    # F19: stress and contentment by age, the living
    V = o["V_hist"]
    for k in ("stress", "content"):
        if k in V:
            arr = np.asarray(V[k])
            x[k] = {a: [float(arr[a, dage > a].sum()), int((dage > a).sum())] for a in (8, 40, 50, 60, 70) if a <= Y}
    return x


# ---------------------------------------------------------------------------------------------------- pooling
def load(d):
    runs = []
    for f in sorted(os.listdir(d)):
        if f.startswith("seed") and f.endswith(".json"):
            runs.append(json.loads(open(os.path.join(d, f)).read().strip().splitlines()[-1]))
    return runs


def frac(runs, key, sub=None):
    """A [hits, of] count pooled over the seeds."""
    h = t = 0
    for r in runs:
        v = r["x"].get(key) if sub is None else (r["x"].get(key) or {}).get(str(sub))   # JSON keys are strings
        if v is None:
            continue
        h += v[0]; t += v[1]
    return h / t if t else None


def wmean(runs, key):
    """The reader's f9 value (or a list of values) pooled over the seeds, weighted by each seed's lives."""
    vals = [(r["out"]["f9"].get(key), r["out"]["lives"]) for r in runs]
    vals = [(v, n) for v, n in vals if v is not None]
    if not vals:
        return None
    if isinstance(vals[0][0], list):
        return [sum(v[i] * n for v, n in vals if v[i] is not None) / sum(n for v, n in vals if v[i] is not None)
                for i in range(len(vals[0][0]))]
    return sum(v * n for v, n in vals) / sum(n for _, n in vals)


def medians(runs, key):
    v = [r["out"]["f9"].get(key) for r in runs]
    v = [x if not isinstance(x, list) else x[0] for x in v if x is not None]
    return (float(np.median(v)), min(v), max(v)) if v else (None, None, None)


# ---------------------------------------------------------------------------------------------------- judging
class Table:
    def __init__(self, rid):
        self.rid, self.lines, self.ok = rid, [], True

    def judge(self, row, val, lo=None, hi=None, fmt="{:.3f}", note=""):
        if val is None:
            self.ok = False
            self.lines.append(f"  MISS {row}: not counted (the reader has no counter for it yet){note}")
            return
        good = (lo is None or val >= lo) and (hi is None or val <= hi)
        rng = (f"{fmt.format(lo)} to {fmt.format(hi)}" if lo is not None and hi is not None else
               f"at least {fmt.format(lo)}" if lo is not None else f"at most {fmt.format(hi)}")
        self.ok &= good
        self.lines.append(f"  {'ok  ' if good else 'MISS'} {row}: {fmt.format(val)} (target {rng}){note}")

    def judge_bool(self, row, good, text):
        self.ok &= bool(good)
        self.lines.append(f"  {'ok  ' if good else 'MISS'} {row}: {text}")

    def info(self, text):
        self.lines.append("       " + text)


def lean_rows(t, row, runs, key, whole, floor):
    """A rate by the colour leading at 40: within .15 below to .10 above the whole, and at or above the floor."""
    for c in COLS:
        v = frac(runs, key, c)
        n = sum(r["x"][key][c][1] for r in runs if key in r["x"])
        if v is None:
            t.judge(f"{row} {c}", None)
            continue
        t.judge(f"{row} {c} ({n} lives)", v, max(whole - .15, floor), whole + .10)


def judge(d, commit=None, record=True):
    runs = load(d)
    if not runs:
        sys.exit(f"STOP: no seed<k>.json in {d}")
    N = sum(r["out"]["lives"] for r in runs)
    seeds = [r["out"]["seed"] for r in runs]
    T = {k: Table(k) for k in TABLES}
    # parents
    t = T["f9_parents"]
    p50 = frac(runs, "par50")
    t.judge("F9.1 ever a parent by 50 (alive at 50)", p50, .78, .87)
    lean_rows(t, "F9.1 by colour", runs, "par50_by", p50, .60)
    m, lo_, hi_ = medians(runs, "F9.2b first 'a child is born' age, median")
    t.judge("F9.2 age at the first child ('a child is born'), median", m, 27, 33, "{:.1f}", f" (seeds {lo_} to {hi_})")
    t.info(f"the children commitment's first start, median of the seeds: {medians(runs, 'F9.2 first child (children commitment) age, median')[0]}")
    t.judge("F9.3 children per parent by 50, mean", wmean(runs, "F9.3 'a child is born' per parent by 50, mean"), 1.8, 2.5, "{:.2f}")
    t.judge("F9.4 births after 50, share of their births", wmean(runs, "F9.4 births after 50, share"), None, .03)
    lf = [a for r in runs for a in r["x"]["leave_first"]]
    t.judge("F9.5 the children leave home, parent's age, median", float(np.median(lf)) if lf else None, 48, 60, "{:.1f}")
    # partners
    t = T["f9_partners"]
    q50 = frac(runs, "part50")
    t.judge("F9.6 ever partnered by 50 (alive at 50)", q50, .83, .92)
    lean_rows(t, "F9.6 by colour", runs, "part50_by", q50, .70)
    m, lo_, hi_ = medians(runs, "F9.7 first partner age, median")
    t.judge("F9.7 age at the first partnership, median", m, 23, 30, "{:.1f}", f" (seeds {lo_} to {hi_})")
    t.judge("F9.8 first partnerships ending in a split, share of the partnered", wmean(runs, "F9.8 partnered with a split"), .30, .50)
    t.judge("F9.9 partner died first, partnered alive at 80", wmean(runs, "F9.9 widowed, partnered alive at 80"), .25, .45)
    t.judge("F9.10 partner died before 50, share of the partnered", wmean(runs, "F9.10 widowed before 50, of partnered"), .01, .05)
    # homes
    t = T["f9_homes"]
    t.judge("F9.11 ever owned a home by 50", wmean(runs, "F9.11 bought a home by 50"), .55, .75)
    m, lo_, hi_ = medians(runs, "F9.12 first purchase age, median")
    t.judge("F9.12 age at the first purchase, median", m, 28, 38, "{:.1f}", f" (seeds {lo_} to {hi_})")
    t.judge("F9.13 purchases per owner, mean", wmean(runs, "F9.13 purchases per owner"), 1.2, 2.5, "{:.2f}")
    t.judge("F9.14 purchases at 75 or older, share", wmean(runs, "F9.14 purchases at 75+, share"), None, .05)
    t.judge("F9.15 lost a home at least once (logged lives)", wmean(runs, "F9.15 lost a home (logged lives)"), .03, .12)
    t.judge("F9.16 owner to tenant only through a sale, a loss or care", wmean(runs, "F9.16 owner to tenant without a sale"), None, 0, "{:.0f}")
    # work
    t = T["f9_work"]
    t.judge("F9.17 job losses not chosen per life, mean", wmean(runs, "F9.17 job losses per life, mean"), 1.0, 2.5, "{:.2f}")
    v = wmean(runs, "F9.18 at least one / four or more")
    t.judge("F9.18 at least one job loss", v[0] if v else None, .45, .75)
    t.judge("F9.18 four or more", v[1] if v else None, None, .10)
    t.judge("F9.19 employers per working life, mean", wmean(runs, "F9.19 employers (career starts), mean"), 4, 12, "{:.2f}")
    t.judge("F9.20 firm crises felt per life, mean", wmean(runs, "F9.20 firm crises per life, mean"), .5, 3, "{:.2f}")
    t.judge("F9.21 out of work at 20 to 64, share of years", wmean(runs, "F9.21 out of work at 20-64 (not retired), share of years"), .04, .10)
    m, lo_, hi_ = medians(runs, "F9.22 retirement age, median")
    t.judge("F9.22 retirement age, median", m, 60, 67, "{:.1f}", f" (seeds {lo_} to {hi_})")
    t.judge("F9.22 still working at 72, share of the living", wmean(runs, "F9.22 working at 72, share of the living"), None, .15)
    # illness
    t = T["f9_illness"]
    v = wmean(runs, "F9.23 a lasting condition by 40/65/80 (living)")
    for i, (a, lo, hi) in enumerate(((40, .15, .30), (65, .45, .65), (80, .70, .90))):
        t.judge(f"F9.23 a lasting illness by {a} (living)", v[i] if v else None, lo, hi)
    t.judge("F9.24 a serious accident or illness before 50", frac(runs, "sev50"), .10, .25)
    t.judge("F9.24 ... by 80 (alive at 80)", frac(runs, "sev80"), .50, .75)
    v = wmean(runs, "F9.25 a low season by 65: moments (all) / body threats (logged)")
    t.judge("F9.25 a sadness that will not lift by 65", v[0] if v else None, .15, .30)
    if v:
        t.info(f"low seasons begun by 65 in the logged lives (F1's Mind): {v[1]:.3f}")
    t.judge("F9.26 an addiction takes hold", wmean(runs, "F9.26 an addiction takes hold"), .08, .18)
    t.judge("F9.27 lasting illnesses diagnosed twice", wmean(runs, "F9.27 a condition diagnosed twice, lives"), None, 0, "{:.0f}")
    # deaths
    t = T["f9_deaths"]
    for a, lo, hi in ((30, .008, .020), (50, .03, .06), (65, .08, .16), (80, .25, .42), (90, .60, .80), (100, .97, None)):
        t.judge(f"F9.{ {30: 28, 50: 29, 65: 30, 80: 31, 90: 32, 100: 33}[a] } dead before {a}", frac(runs, "dead_before", a), lo, hi)
    p105 = [r["x"]["past105"] for r in runs]
    t.judge_bool("F9.33 living past 105", None not in p105 and sum(p105) == 0,
                 f"{sum(p105) if None not in p105 else 'not seen (run 106 years)'} lives (target none)")
    da = np.array([a for r in runs for a in r["x"]["death_ages"]])
    t.judge("F9.34 age at death, median", float(np.median(da)) if len(da) else None, 82, 88, "{:.1f}")
    t.judge("F9.34 age at death, mean", float(da.mean()) if len(da) else None, 78, 84, "{:.1f}")
    u40, o65 = {}, {}
    for r in runs:
        for k_, v_ in r["x"]["causes_u40"].items():
            u40[k_] = u40.get(k_, 0) + v_
        for k_, v_ in r["x"]["causes_65"].items():
            o65[k_] = o65.get(k_, 0) + v_
    EXT = ("accident", "own act", "violence", "overdose", "killed", "drown", "crash", "fire", "fall")
    INT = ("illness", "old age", "disease", "heart", "stroke", "cancer", "condition")
    n40 = sum(u40.values()); n65 = sum(o65.values())
    t.judge("F9.35 before 40: an accident, violence or an overdose", sum(v for k, v in u40.items() if any(e in k for e in EXT)) / n40 if n40 else None,
            .30, .60, note=f" ({n40} deaths: {dict(sorted(u40.items(), key=lambda kv: -kv[1]))})")
    t.judge("F9.35 at 65 and over: an illness or old age", sum(v for k, v in o65.items() if any(e in k for e in INT)) / n65 if n65 else None,
            .85, None, note=f" ({n65} deaths; causes {dict(sorted(o65.items(), key=lambda kv: -kv[1])[:8])})")
    t.judge("F9.35 'of old age' before 85", sum(r["out"]["f9"].get("F9.35 of old age before 85", 0) for r in runs), None, 0, "{:.0f}")
    t.info("F9.36 (the same age at death across starts) is the Game's world_hold, a separate row")
    # means
    t = T["f9_means"]
    t.judge("F9.37 health 98% or more, share of adult years", wmean(runs, "F9.37 health 98%+, share of adult years"), None, .03)
    t.judge("F9.37 lives with no run above a year at 98% or more", frac(runs, "health_run_ok"), .95, None)
    hw = {}
    for r in runs:
        for a, v in r["x"]["health_w80"].items():
            hw.setdefault(int(a), []).append((v, r["out"]["lives"]))
    hw = {a: sum(v * n for v, n in l) / sum(n for _, n in l) for a, l in hw.items()}
    bad = {a: round(v, 3) for a, v in hw.items() if not .15 <= v <= .25}
    t.judge_bool("F9.37 the middle 80% of health over .15 to .25 at every age from 30", hw and not bad,
                 f"{min(hw.values()):.3f} to {max(hw.values()):.3f}" + (f"; outside at {bad}" if bad else "") if hw else "not counted")
    t.judge("F9.37 health below 25% outside a serious illness or the last 3 years, share of life-years", frac(runs, "health_low_other"), None, .01)
    v = wmean(runs, "F9.38 money 5% or less, adults at a time / at 15")
    t.judge("F9.38 money 5% or less, adults at a time", v[0] if v else None, .07, .13)
    m15 = sum(r["x"]["money_lo5_15"] * r["out"]["lives"] for r in runs) / N
    t.judge("F9.38 money 5% or less at 15", m15, .03, .08)
    t.judge("F9.38 five years running at 5% or less, adult lives", wmean(runs, "F9.38 five years running at 5% or less"), None, .10)
    t.judge("F9.38 money mean at 70 to 85 over 40 to 60", wmean(runs, "F9.38 money mean 70-85 / 40-60"), .9, None, "{:.2f}")
    tl = {}
    for r in runs:
        for a, v in r["x"]["ties_lo5"].items():
            tl.setdefault(int(a), []).append((v, r["out"]["lives"]))
    tl = {a: sum(v * n for v, n in l) / sum(n for _, n in l) for a, l in tl.items()}
    bad = {a: round(v, 3) for a, v in tl.items() if not .03 <= v <= .08}
    t.judge_bool("F9.39 ties 5% or less at .03 to .08 at every age from 15", tl and not bad,
                 f"{min(tl.values()):.3f} to {max(tl.values()):.3f}" + (f"; outside at {bad}" if bad else "") if tl else "not counted")
    kid = max(sum(r["x"]["ties_lo5_kid"][a] * r["out"]["lives"] for r in runs) / N for a in runs[0]["x"]["ties_lo5_kid"])
    t.judge("F9.39 ties 5% or less under 15, the highest age", kid, None, .02)
    t.judge("F9.39 ties mean at 15", sum(r["x"]["ties_mean15"] * r["out"]["lives"] for r in runs) / N, .50, .60)

    def cmean(key):
        out = {}
        for c in COLS:
            vals = [(r["x"][key][c][0], r["x"][key][c][1]) for r in runs if r["x"][key][c][0] is not None]
            out[c] = sum(v * n for v, n in vals) / sum(n for _, n in vals) if vals else None
        return out
    hw_c, tl_c, mm_c, mw_c = cmean("c_health_w80"), cmean("c_ties_late"), cmean("c_money_mean"), cmean("c_money_w80")
    oth = lambda d_, cs: np.mean([d_[c] for c in COLS if c not in cs and d_[c] is not None])
    t.judge_bool("F9.40 Red's health spread wider than the others' mean", hw_c["R"] is not None and hw_c["R"] > oth(hw_c, "R"),
                 f"R {hw_c['R']:.3f} against {oth(hw_c, 'R'):.3f} (lean {hw_c['R'] - oth(hw_c, 'R'):+.3f})")
    for c in "WG":
        t.judge_bool(f"F9.40 {c}'s ties at 60 to 85 above the others' mean", tl_c[c] is not None and tl_c[c] > oth(tl_c, c),
                     f"{c} {tl_c[c]:.3f} against {oth(tl_c, c):.3f} (lean {tl_c[c] - oth(tl_c, c):+.3f})")
    for c in "BU":
        t.judge_bool(f"F9.40 {c}'s money at 30 to 70 higher and more spread", mm_c[c] > oth(mm_c, c) and mw_c[c] > oth(mw_c, c),
                     f"{c} mean {mm_c[c]:.3f} against {oth(mm_c, c):.3f} ({mm_c[c] - oth(mm_c, c):+.3f}), "
                     f"spread {mw_c[c]:.3f} against {oth(mw_c, c):.3f} ({mw_c[c] - oth(mw_c, c):+.3f})")
    # F14
    t = T["f14_settle"]
    mv = {a: frac(runs, f"move_{a}") for a in (25, 45, 65)}
    if None in mv.values():
        t.judge("F14 movement", None)
    else:
        t.info(f"movement per decade, the living: 25-35 {mv[25]:.3f}, 45-55 {mv[45]:.3f}, 65-75 {mv[65]:.3f}")
        t.judge("F14 45-55 over 25-35 (\"half as fast by 50\")", mv[45] / mv[25], .40, .60)
        t.judge("F14 65-75 over 25-35 (\"a quarter as fast after 70\")", mv[65] / mv[25], .15, .35)
    # F17
    t = T["f17_deeds"]
    dd = {}
    for r in runs:
        for nm, v in r["x"]["deeds"].items():
            e = dd.setdefault(nm, dict(all=[0, 0], by={c: [0, 0] for c in COLS}))
            e["all"][0] += v["all"][0]; e["all"][1] += v["all"][1]
            for c in COLS:
                e["by"][c][0] += v["by"][c][0]; e["by"][c][1] += v["by"][c][1]
    rate = lambda nm, c: dd[nm]["by"][c][0] / max(dd[nm]["by"][c][1], 1)
    for nm in ("made an enemy", "hid a wrong", "defied an authority"):
        t.judge(f"F17 {nm}, per life", dd[nm]["all"][0] / dd[nm]["all"][1] if nm in dd else None, None, 5, "{:.2f}")
    for nm, c, how in (("broke the law", "W", "ratio"), ("used drugs", "U", "top"), ("refused someone in need", "G", "top")):
        if nm not in dd:
            t.judge(f"F17 {nm}", None)
            continue
        rs = {k: rate(nm, k) for k in COLS}
        t.info(f"{nm} per life by the colour leading at 40: " + ", ".join(f"{k} {v:.2f}" for k, v in rs.items()))
        if how == "ratio":
            others = sum(dd[nm]["by"][k][0] for k in COLS if k != c) / max(sum(dd[nm]["by"][k][1] for k in COLS if k != c), 1)
            t.judge(f"F17 White's {nm} over the other colours'", rs[c] / others if others else None, None, 1.0, "{:.2f}")
        else:
            top = max(rs, key=rs.get)
            t.judge_bool(f"F17 {c} not the most '{nm}' of the five", top != c, f"highest {top}")
    # F19
    t = T["f19_mind"]
    st, ct = ({a: frac(runs, k, a) for a in (8, 40, 50, 60, 70)} for k in ("stress", "content"))
    if None in st.values() or None in ct.values():
        t.judge("F19", None)
    else:
        t.judge_bool("F19 stress at 8 below stress at 40", st[8] < st[40], f"{st[8]:.3f} against {st[40]:.3f}")
        t.judge_bool("F19 contentment at 50 below 40 and 60", ct[50] < ct[40] and ct[50] < ct[60],
                     f"40 {ct[40]:.3f}, 50 {ct[50]:.3f}, 60 {ct[60]:.3f}")
        t.judge_bool("F19 contentment at 70 above 50", ct[70] > ct[50], f"70 {ct[70]:.3f}")
    # report and results
    rep = os.path.join(d, "f9_report.txt")
    head = [f"v22.5 F rows (check_f9.py): {N} lives, seeds {min(seeds)} to {max(seeds)} ({len(seeds)}), "
            f"{runs[0]['out']['years']} years, world {'on' if runs[0]['out']['world'] else 'off'}"
            + (f", commit {commit[:7]}" if commit else ""), ""]
    body = []
    for k in TABLES:
        body.append(f"{k}: {'PASS' if T[k].ok else 'MISS'}")
        body += T[k].lines + [""]
    ok = all(T[k].ok for k in TABLES)
    body.append("F9: " + ("PASS" if ok else "MISS") + f" ({sum(T[k].ok for k in TABLES)} of {len(TABLES)} tables)")
    open(rep, "w").write("\n".join(head + body) + "\n")
    print("\n".join(head + body))
    if record:
        sys.path.insert(0, HERE)
        import results
        rel = os.path.relpath(rep, os.path.dirname(HERE)) if rep.startswith(os.path.dirname(HERE)) else rep
        for k in TABLES:
            misses = sum(1 for ln in T[k].lines if ln.startswith("  MISS"))
            results.add(k, "PASS" if T[k].ok else "MISS", report=rel,
                        note=f"{N} lives, seeds {min(seeds)}-{max(seeds)}" + (f"; {misses} targets missed" if misses else ""),
                        candidate={"commit": commit} if commit else None, run=" ".join(sys.argv))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------------- main
def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "seed":
        seed_main(arg("--repo", "."), int(arg("--seed", 41)), int(arg("--lives", 300)), int(arg("--years", 106)),
                  arg("--world", "on"), json.loads(arg("--px", '{"self_death": true}')), int(arg("--log", 100)))
        return 0
    if cmd == "judge":
        return judge(sys.argv[2], arg("--commit", os.environ.get("CHROMA_COMMIT")), "--no-record" not in sys.argv)
    if cmd != "run":
        sys.exit(__doc__)
    repo = os.path.abspath(arg("--repo", "."))
    s0, s1 = (int(v) for v in arg("--seeds", "41-52").split("-"))
    out = os.path.abspath(arg("--out", os.path.join(os.path.dirname(HERE), "chroma-release", "out",
                                                   "f9_" + time.strftime("%Y%m%d-%H%M%S", time.gmtime()))))
    os.makedirs(out, exist_ok=True)
    jobs = int(arg("--jobs", os.cpu_count() or 2))
    passed = [a for name in ("--lives", "--years", "--world", "--px", "--log") if name in sys.argv for a in (name, arg(name, ""))]
    todo, live = list(range(s0, s1 + 1)), []
    env = dict(os.environ)
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        env.setdefault(v, "1")   # one thread a seed: the seeds run side by side
    t0 = time.time()
    while todo or live:
        while todo and len(live) < jobs:
            k = todo.pop(0)
            f = open(os.path.join(out, f"seed{k}.json"), "w")
            live.append((k, f, subprocess.Popen([sys.executable, "-B", os.path.abspath(__file__), "seed", "--repo", repo,
                                                  "--seed", str(k)] + passed, stdout=f, stderr=open(os.path.join(out, f"seed{k}.log"), "w"), env=env)))
        time.sleep(2)
        for item in list(live):
            k, f, p = item
            if p.poll() is not None:
                f.close(); live.remove(item)
                print(f"seed {k}: exit {p.returncode} at {time.time() - t0:.0f}s", flush=True)
                if p.returncode:
                    sys.exit(f"STOP: seed {k} failed; see {out}/seed{k}.log")
    return judge(out, arg("--commit", os.environ.get("CHROMA_COMMIT")), "--no-record" not in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
