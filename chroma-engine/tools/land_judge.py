"""Judges Release's land rows from land_lives.py's files (chroma-world/spheres/land-checks-measure.md, run B), and
prints national standing's rates for WA8n.

    python3 -B chroma-engine/tools/land_judge.py <out41.json> [<out42.json> ...]

One line per row: id, PASS / FAIL / INCONCLUSIVE / INFO, the numbers and the rule. Rows that count small groups (LN6,
LN7, LN11, LN12) read only with 30 or more; fewer is INCONCLUSIVE. Parts the run cannot read are INCONCLUSIVE with the
reason. Exit 0 always (the verdicts are in the lines).
"""
import json, sys
from collections import Counter, defaultdict

import numpy as np

D = [json.load(open(p)) for p in sys.argv[1:]]
if not D:
    sys.exit(__doc__)
MIN_N = 30


def line(rid, verdict, nums, rule):
    print(f"{rid:<6s} {verdict:<12s} {nums}   [{rule}]")


def within(x, lo, hi):
    return lo <= x <= hi


lives = sum(d["N"] for d in D)
print(f"land rows on {len(D)} seed(s), {lives} lives, {D[0]['years']} years")

# LN3: adults at 120+ minutes a week in nature, pooled over the life-years
my = sum(d["log"]["mins_years"] for d in D); m120 = sum(d["log"]["mins_120"] for d in D)
if my:
    s = m120 / my
    line("LN3", "PASS" if within(s, .35, .65) else "FAIL", f"share {s:.3f} of {my} adult life-years", ".35 to .65")
else:
    line("LN3", "INCONCLUSIVE", "no adult life-years with minutes (wa_land_dev off?)", ".35 to .65")

# LN4: good and bad among the land moments shown (decisions apart; mixed in the denominator)
tone = Counter(m[4] for d in D for m in d["log"]["moments"] if not m[5])
tot = sum(tone.values())
if tot:
    g, b = tone["good"] / tot, tone["bad"] / tot
    ok = within(g, .45, .65) and within(b, .25, .45)
    line("LN4", "PASS" if ok else "FAIL", f"good {g:.3f}, bad {b:.3f}, mixed {tone['mixed'] / tot:.3f} of {tot} moments",
         "good .45 to .65, bad .25 to .45")
else:
    line("LN4", "INCONCLUSIVE", "no land moments shown", "good .45 to .65, bad .25 to .45")

# LN5: each colour's share of land picks (faces chosen); the faces' outcomes are not read here
fc = np.sum([d["land"]["counts"]["faces"] for d in D], 0).astype(float)
if fc.sum():
    sh = fc / fc.sum()
    line("LN5a", "PASS" if all(within(x, .17, .23) for x in sh) else "FAIL",
         "picks " + " ".join(f"{c} {x:.3f}" for c, x in zip("WUBRG", sh)) + f" of {int(fc.sum())}", "each .17 to .23")
else:
    line("LN5a", "INCONCLUSIVE", "no faces picked", "each .17 to .23")
line("LN5b", "INCONCLUSIVE", "the faces' outcomes with the moments' own effects taken out need a reader of the felt "
     "state per pick; not in this run's output", "faces within .05")

# LN6: flooded households back within a year, still low at two years
fb = [x for d in D for x in d["land"]["counts"]["flood_back"] if len(x) >= 5]
if len(fb) >= MIN_N:
    back = np.mean([not x[3] for x in fb]); low2 = np.mean([bool(x[4]) for x in fb])
    ok = within(back, .55, .75) and within(low2, .08, .20)
    line("LN6", "PASS" if ok else "FAIL", f"back {back:.3f}, still low {low2:.3f} of {len(fb)} flooded", ".55 to .75 back; .08 to .20 still low")
else:
    line("LN6", "INCONCLUSIVE", f"{len(fb)} flooded households followed two years (needs {MIN_N})", ".55 to .75 back; .08 to .20 still low")

# LN7: ordinary lives' share of their stretches' change (what a life caused, gross, over the stretches' gross movement
# year by year); Known lives' land decisions
shares, kn_dec = [], defaultdict(float)
for d in D:
    la = d["land"]
    ch = np.array(d["gross"]) if d.get("gross") is not None else \
        np.abs(np.array(la["health"]) - np.array(la["start_health"])) + np.abs(np.array(la["wild"]) - np.array(la["start_wild"]))
    dec_n = set()
    for x in la["decisions"]:
        kn_dec[(d["seed"], x["n"])] += abs(x["health"]) + abs(x["wild"]); dec_n.add(x["n"])
    for n, lv in enumerate(la["lives"]):
        if n in dec_n:
            continue
        cs, tc = 0.0, 0.0
        seen = set()
        for unit, l, st, amt in lv["told"]:
            cs += amt
            j = la["stretches"].index(st)
            if (l, j) not in seen:
                seen.add((l, j)); tc += ch[l][j]
        shares.append(cs / tc if tc > 1e-9 else 0.0)
med = float(np.median(shares)) if shares else float("nan")
kv = list(kn_dec.values())
if len(kv) >= MIN_N:
    k5 = np.mean([v >= .05 for v in kv])
    ok = med <= .01 and within(k5, .4, .6)
    line("LN7", "PASS" if ok else "FAIL", f"ordinary median share {med:.4f} of {len(shares)} lives; Known deciders at .05+ {k5:.3f} of {len(kv)}",
         "ordinary .01 or less; Known 1 in 2 (read at 30+)")
else:
    line("LN7", "INCONCLUSIVE", f"ordinary median share {med:.4f} of {len(shares)} lives; {len(kv)} Known lives with a land decision "
         f"(needs {MIN_N})", "ordinary .01 or less; Known 1 in 2 (read at 30+)")

# LN8: faith joining after a hit
line("LN8", "INCONCLUSIVE", "faith joining by life and year, hit against unhit towns, is not in this run's output (needs the "
     "engine's faith_join with the town's hits)", "+2 to +8 points")

# LN9 (runtime part): no one under 18 in a bad land moment
young_bad = [m for d in D for m in d["log"]["moments"] if m[4] == "bad" and m[2] < 18]
nb = sum(1 for d in D for m in d["log"]["moments"] if m[4] == "bad")
line("LN9rt", "PASS" if not young_bad else "FAIL",
     f"{len(young_bad)} bad land moments under 18 of {nb} bad" + (f"; e.g. {sorted({m[3] for m in young_bad})[:6]}" if young_bad else ""),
     "none (the text part is the Library's check)")

# LN10: company drawn: alone among adults' together moments; ties
co = [c for d in D for c in d["log"]["company"] if c[1] >= 18]
if co:
    al = np.mean([c[2] == "alone" for c in co])
    line("LN10a", "PASS" if within(al, .2, .4) else "FAIL", f"alone {al:.3f} of {len(co)} adults' together moments; kinds "
         + str(dict(Counter(c[2] for c in co).most_common())), "alone .2 to .4")
else:
    line("LN10a", "INCONCLUSIVE", "no together moments for adults", "alone .2 to .4")
line("LN10b", "INCONCLUSIVE", "ties moving as `company` says needs the ties before and after each moment; not in this run's output",
     "the right way in 9 of 10")

# LN11: ways taken up evenly
ways_list = None
try:
    import sphere_data as SD   # the engine's copy of land.json
    ways_list = SD.LAND["uses"]["ways"]["list"]
except Exception:
    pass
ever = defaultdict(set); lead_of = {}
for d in D:
    for n, key, age in d["log"]["ways"]:
        ever[key].add((d["seed"], n)); lead_of[(d["seed"], n)] = d["lead"][n]
if ways_list is not None and sum(len(v) for v in ever.values()) >= MIN_N:
    sh = {w["key"]: len(ever.get(w["key"], ())) / lives for w in ways_list}
    by_col = Counter()
    for w in ways_list:
        by_col[w["lead"][0]] += len(ever.get(w["key"], ()))
    cmin, cmax = min(by_col[c] for c in "WUBRG"), max(by_col[c] for c in "WUBRG")
    strat = defaultdict(set)
    for w in ways_list:
        for s_ in w.get("strategies") or []:
            for who in ever.get(w["key"], ()):
                strat[s_].add(lead_of[who])
    all_strat = {s_ for w in ways_list for s_ in (w.get("strategies") or [])}
    bad_w = [k for k, v in sh.items() if not within(v, .005, .10)]
    bad_s = [s_ for s_ in sorted(all_strat) if len(strat[s_]) < 3]
    ratio = cmax / cmin if cmin else float("inf")
    ok = not bad_w and ratio <= 1.3 and not bad_s
    line("LN11", "PASS" if ok else "FAIL", f"ways outside .005-.10: {len(bad_w)} of {len(sh)} {bad_w[:6]}; colours' ways taken "
         + " ".join(f"{c} {by_col[c]}" for c in "WUBRG") + f" (max/min {ratio:.2f}); strategies by <3 colours {bad_s}",
         "each way .005 to .10; colours within 1.3x; every strategy by 3+ colours")
else:
    line("LN11", "INCONCLUSIVE", f"{sum(len(v) for v in ever.values())} ways taken (needs {MIN_N}) or no sphere_data.LAND",
         "each way .005 to .10; colours within 1.3x; every strategy by 3+ colours")

# LN12: bridges
held = [lv for d in D for lv in d["land"]["lives"] if lv["bridges_open"]]
bc = Counter((b["a"], b["b"]) for d in D for lv in d["land"]["lives"] for b in lv["bridges_open"])
if len(held) >= MIN_N:
    s1 = len(held) / lives; top = max(bc.values()) / lives
    line("LN12", "PASS" if s1 >= .05 and top <= .03 else "FAIL", f"lives holding a bridge {s1:.3f} ({len(held)}); most-held "
         f"{top:.3f} {max(bc, key=bc.get)}", "1 in 20 or more; none over 3 in 100")
else:
    line("LN12", "INCONCLUSIVE", f"{len(held)} lives with a bridge (needs {MIN_N})", "1 in 20 or more; none over 3 in 100")

# WA8n: national standing's rates (the shares; decisions a national year are not read here)
if all(d.get("national") for d in D):
    reached = defaultdict(set); routes = Counter()
    for d in D:
        for x in d["national"]["log"]:
            if x.get("what") == "reached":
                reached[x["kind"]].add((d["seed"], x["n"])); routes[x.get("route")] += 1
    ev = sum(sum(d["national"]["ever"]) for d in D) / lives
    line("WA8n", "PASS" if within(ev, .01, .03) else "FAIL",
         f"ever national {ev:.4f}; " + " ".join(f"{k} {len(reached[k]) / lives:.4f}" for k in ("recognition", "influence", "authority"))
         + f"; routes taken {len(routes)} {dict(routes.most_common(5))}", "unplayed .01 to .03 (decisions a national year: not read here)")
else:
    line("WA8n", "INCONCLUSIVE", "no national output (wa_nat_climb off?)", "unplayed .01 to .03")
