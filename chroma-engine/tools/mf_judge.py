"""RE2 from MF's lives (Release, records/v25/checks.md): pools mf_run.py's files, warm arm before "--", controlling
after, and prints the row's three checks and the report.

    python3 -B chroma-engine/tools/mf_judge.py <warm1.json ...> -- <ctrl1.json ...> [--adequacy .05] [--json out.json]

The lives read: those with a family at the set-up (living in their parents' household) and alive at 19. Life (seed, n)
in one arm is matched with the same in the other; every file must come from the same commit with the same settings but
the arm, and each matched life must have got the same family in both (else the run is refused).

  1. Distance: the controlling arm ends 19 at least .03 (L1) further from the family's mix than the warm arm. The mean
     over matched lives of L1(ctrl) - L1(warm), its 95% interval from the larger of the pairs' standard error and the
     seeds' (the per-seed means' spread, with two seeds or more). PASS when the interval's lower end is .03 or more,
     FAIL when its upper end is below .03, INCONCLUSIVE otherwise.
  2. Backlash, controlling: the share of lives whose opposed colours (the colours the family's demand opposed) rose .02
     or more from 13 to 19, in .20 to .40.
  3. Backlash, warm: that share under .10.
     Shares (checks.md, "Share with a target"): Wilson 95%; PASS when the point estimate meets the target and the
     interval's half-width is no more than the adequacy (RE2 states none: .05 unless --adequacy says otherwise), FAIL
     when the whole interval misses it, INCONCLUSIVE otherwise.
RE2 is the worst of the three. The report adds, per arm and per family (the rejected demand's colours), which colours
rose from 13 to 19 (all lives, the backlash lives, and the lives that rejected the family's demands), the opposite
colour's backlash (diagnostic), and the responses to the family's demands by kind.
"""
import json
import math
import sys

import numpy as np

COL = "WUBRG"
RESP = ("accept", "adopt", "negotiate", "disagree", "backlash", "withdraw")
args = sys.argv[1:]
opts = {}
for k in ("--adequacy", "--json"):
    if k in args:
        i = args.index(k); opts[k] = args[i + 1]; del args[i:i + 2]
if "--" not in args:
    sys.exit(__doc__)
WF, CF = args[:args.index("--")], args[args.index("--") + 1:]
if not WF or not CF:
    sys.exit(__doc__)
ADEQ = float(opts.get("--adequacy", 0.05))


def load(fs, arm):
    runs = [json.load(open(f)) for f in fs]
    for f, r in zip(fs, runs):
        if r.get("tool") != "mf_run" or r["arm"] != arm:
            sys.exit(f"REFUSED: {f} is not an mf_run file of the {arm} arm")
    return runs


W, Cr = load(WF, "warm"), load(CF, "controlling")
allr = W + Cr


def strip(s):
    return {k: v for k, v in s.items() if k not in ("arm", "family")}


shas = {(r["sha"], r["dirty"]) for r in allr}
sets = {json.dumps(strip(r["settings"]), sort_keys=True) for r in allr}
problems = []
if len(shas) > 1:
    problems.append(f"files from different commits {sorted(shas)}: lives from different candidates are never pooled")
if len(sets) > 1:
    problems.append("files with different settings (beyond the arm)")
if any(d for _, d in shas):
    problems.append("a file ran on a tree with uncommitted engine, Library or pack changes")


def lives(runs):
    out = {}
    for r in runs:
        for lf in r["lives"]:
            key = (r["seed"], r["N"], lf["n"])
            if key in out:
                sys.exit(f"REFUSED: life {key} given twice")
            out[key] = lf
    return out


LW, LC = lives(W), lives(Cr)
if set(LW) != set(LC):
    problems.append(f"the arms' lives differ: {len(set(LW) ^ set(LC))} lives in one arm only (same seeds and N needed)")
bad_pair = [k for k in set(LW) & set(LC) if LW[k]["pair"] != LC[k]["pair"] or LW[k]["child_pre"] != LC[k]["child_pre"]]
if bad_pair:
    problems.append(f"{len(bad_pair)} matched lives differ before the set-up (not the same lives)")
if problems:
    print("RE2 INCONCLUSIVE: the runs cannot be pooled\n  " + "\n  ".join(problems))
    sys.exit(2)


def ok(lf):
    return bool(lf["has_family"]) and lf.get("l1_19") is not None


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def share_rule(p, lo, hi, a, b, below=False):
    """Target [a, b] (None: open; below: p < b). PASS / FAIL / INCONCLUSIVE by checks.md's share rule."""
    if math.isnan(p):
        return "INCONCLUSIVE"
    meets = (a is None or p >= a) and (b is None or (p < b if below else p <= b))
    if (b is not None and (lo >= b if below else lo > b)) or (a is not None and hi < a):
        return "FAIL"
    return "PASS" if meets and (hi - lo) / 2 <= ADEQ else "INCONCLUSIVE"


keys = sorted(k for k in LW if ok(LW[k]) and ok(LC[k]))
seeds = sorted({k[0] for k in keys})
res = {}
lines = []
pr = lines.append
pr(f"RE2 matched families: {len(WF)} warm and {len(CF)} controlling files, seeds {seeds}, commit "
   f"{allr[0]['sha'][:12]}, settings {json.dumps(strip(allr[0]['settings']), sort_keys=True)}")
pr(f"  warm family {W[0]['settings']['family']}, controlling family {Cr[0]['settings']['family']}")
nW, nC = len(LW), len(LC)
pr(f"  lives: {nW} an arm; read {len(keys)} matched (a family at the set-up, alive at 19 in both); left out: "
   f"no family at the set-up {sum(not LW[k]['has_family'] for k in LW)}, dead before 19 warm "
   f"{sum(LW[k]['has_family'] and LW[k].get('l1_19') is None for k in LW)} controlling "
   f"{sum(LC[k]['has_family'] and LC[k].get('l1_19') is None for k in LC)}")

# 1. distance
d = np.array([LC[k]["l1_19"] - LW[k]["l1_19"] for k in keys])
if len(d) >= 2:
    m = float(d.mean()); se_p = float(d.std(ddof=1) / math.sqrt(len(d)))
    per_seed = [float(np.mean([LC[k]["l1_19"] - LW[k]["l1_19"] for k in keys if k[0] == s])) for s in seeds]
    se_s = float(np.std(per_seed, ddof=1) / math.sqrt(len(per_seed))) if len(per_seed) >= 2 else 0.0
    se = max(se_p, se_s); lo, hi = m - 1.96 * se, m + 1.96 * se
    r1 = "PASS" if lo >= 0.03 else "FAIL" if hi < 0.03 else "INCONCLUSIVE"
else:
    m = se_p = se_s = lo = hi = float("nan"); per_seed = []; r1 = "INCONCLUSIVE"
res["distance"] = dict(result=r1, gap=m, lo=lo, hi=hi, se_pairs=se_p, se_seeds=se_s, n=len(d), per_seed=per_seed,
                       l1_warm=float(np.mean([LW[k]["l1_19"] for k in keys])) if keys else None,
                       l1_ctrl=float(np.mean([LC[k]["l1_19"] for k in keys])) if keys else None)
pr("")
pr(f"1. Distance to the family's mix at 19 (L1): warm {res['distance']['l1_warm']:.3f}, controlling "
   f"{res['distance']['l1_ctrl']:.3f}; gap {m:+.4f}, 95% [{lo:+.4f}, {hi:+.4f}] (se pairs {se_p:.4f}, seeds {se_s:.4f}; "
   f"{len(d)} pairs; per seed " + ", ".join(f"{s} {x:+.3f}" for s, x in zip(seeds, per_seed)) + f"); target >= .03: {r1}")
pr(f"   (at 13: warm {np.mean([LW[k]['l1_13'] for k in keys]):.3f}, controlling {np.mean([LC[k]['l1_13'] for k in keys]):.3f})"
   if keys else "")


# 2, 3. backlash shares (each arm's own lives read)
def arm_share(L, flag):
    ls = [lf for lf in L.values() if ok(lf)]
    k = sum(bool(lf[flag]) for lf in ls)
    return (k, len(ls)) + wilson(k, len(ls))


kc, nc, pc, loc, hic = arm_share(LC, "backlash")
kw, nw, pw, low, hiw = arm_share(LW, "backlash")
r2 = share_rule(pc, loc, hic, 0.20, 0.40)
r3 = share_rule(pw, low, hiw, None, 0.10, below=True)
res["backlash_ctrl"] = dict(result=r2, k=kc, n=nc, p=pc, lo=loc, hi=hic)
res["backlash_warm"] = dict(result=r3, k=kw, n=nw, p=pw, lo=low, hi=hiw)
pr("")
pr(f"2. Backlash, controlling: {kc}/{nc} = {pc:.3f}, Wilson 95% [{loc:.3f}, {hic:.3f}] (half-width {(hic - loc) / 2:.3f},"
   f" adequacy {ADEQ}); target .20 to .40: {r2}")
pr(f"3. Backlash, warm: {kw}/{nw} = {pw:.3f}, Wilson 95% [{low:.3f}, {hiw:.3f}] (half-width {(hiw - low) / 2:.3f}); "
   f"target under .10: {r3}")
order = {"FAIL": 0, "INCONCLUSIVE": 1, "PASS": 2}
row = min((r1, r2, r3), key=order.get)
res["RE2"] = row
pr("")
pr(f"RE2: {row}  (distance {r1}, backlash controlling {r2}, backlash warm {r3})")
pr("   backlash: the opposed colours' (all the family asks nothing of: for a pair, the other three) summed share up "
   ".02 or more from 13 to 19")

# the report: which colours rose, by the rejected demand
pr("")
pr("Which colours rose from 13 to 19, by the family's demand (its pair; the opposed colours are the other three, "
   "the opposite colour in brackets), mean change in share:")
hdr = "   " + " ".join(f"{c:>6}" for c in COL)
for arm, L in (("warm", LW), ("controlling", LC)):
    pr(f"  {arm}")
    for pair in ("WU", "UB", "BR", "RG", "GW"):
        ls = [lf for lf in L.values() if ok(lf) and lf["pair"] == pair]
        if not ls:
            continue
        opp = ls[0]["opposite"]
        bl = [lf for lf in ls if lf["backlash"]]; rj = [lf for lf in ls if lf["n_rej"]]
        def row_(xs):
            return " ".join(f"{np.mean([lf['rise'][c] for lf in xs]):+6.3f}" for c in COL) if xs else "   (none)"
        pr(f"    family {pair} (against {opp}): {len(ls)} lives, backlash {len(bl)} ({len(bl) / len(ls):.2f}), "
           f"opposite colour up .02 {sum(lf['backlash_opposite'] for lf in ls)}, rejected a demand {len(rj)}")
        pr(f"      {'':14}" + hdr)
        pr(f"      {'all':14}   " + row_(ls))
        pr(f"      {'backlash':14}   " + row_(bl))
        pr(f"      {'rejected':14}   " + row_(rj))
        if rj:
            rp_ = np.mean([lf["rej_purpose"] for lf in rj], 0)   # (lives that rejected only event asks: none)
            pr(f"      {'its purpose':14}   " + " ".join(f"{x:6.3f}" for x in rp_) + "   (the household's own rejected demands, mean)")
    ls = [lf for lf in L.values() if ok(lf)]
    bl = [lf for lf in ls if lf["backlash"]]
    pr(f"    the opposite colour (the child's lead at the set-up) up .02: "
       f"{sum(lf['backlash_opposite'] for lf in ls)}/{len(ls)} (diagnostic)")
    pr(f"    backlash lives' rise: opposite colour {np.mean([lf['rise_opposite'] for lf in bl]) if bl else float('nan'):+.3f}, "
       f"the other two opposed {np.mean([lf['rise_opposed'] - lf['rise_opposite'] for lf in bl]) if bl else float('nan'):+.3f}")
    res[f"opposite_{arm}"] = sum(lf["backlash_opposite"] for lf in ls) / max(len(ls), 1)

pr("")
pr("Responses to the family's demands from 13 to 19 (while living there), per life, and constrained:")
for arm, L in (("warm", LW), ("controlling", LC)):
    ls = [lf for lf in L.values() if ok(lf)]
    tot = {r: sum(lf["resp"]["13_19"]["family"].get(r, 0) for lf in ls) for r in RESP}
    n_ = max(sum(tot.values()), 1)
    oth = {r: sum(lf["resp"]["13_19"]["other"].get(r, 0) for lf in ls) for r in RESP}
    pr(f"  {arm:12} {sum(tot.values()) / max(len(ls), 1):5.1f} a life: " + ", ".join(f"{r} {tot[r] / n_:.2f}" for r in RESP)
       + f"; constrained {sum(lf['constrained']['13_19'] for lf in ls) / n_:.2f}; a town event's ask "
       f"{sum(lf.get('events', {}).get('13_19', 0) for lf in ls) / n_:.2f}; others' demands "
       f"{sum(oth.values()) / max(len(ls), 1):.1f} a life; left home by 19 "
       f"{sum(lf['left_home'] is not None and lf['left_home'] < 19 for lf in ls) / max(len(ls), 1):.2f}")
    res[f"responses_{arm}"] = tot
tm = [r["time"]["per_100_lives_s"] for r in allr]
pr("")
pr(f"Run time: {min(tm):.0f} to {max(tm):.0f} s per 100 lives (to 25), by file")
print("\n".join(lines))
if "--json" in opts:
    json.dump(res, open(opts["--json"], "w"), indent=1, default=float)
