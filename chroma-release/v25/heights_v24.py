"""v24 heights rows (records/v24/scope.md A1 to A5) on a candidate, against the A0 baseline on v23.1 (out/heights/):
the same reading of each height (out/heights/heights_judge.py, imported), Known as Emren chose it (`ge_known_strict`:
leading a sphere, "good name in town" or a master's stand-in, or Notable or Historic).

    python3 -B heights_v24.py <sha7> [--off <tag>] [--out REPORT] [--play-dir DIR --engine-dir DIR]

Reads out/v24/heights/play_<sha7>/ and engine_<sha7>/ (run.sh), and with --off play_<sha7>_<tag>/ (A5: the same
lives with Bold ways off). Release's readings, stated so the Engine and the Game tune to the same thing:
  A1  reader with READ_GOALS=1 ("reader+aims", the baseline's skilled player with an aim), presets 1 to 4 x seeds 1 to 6:
      Known or higher in .70 or more of its lives (v23.1: .583, 14 of 24). In v24 read only (Emren typed "Bar to v25",
      10-20 08:37 UTC; scope.md Rulings): printed on those 24 lives and, from wide_<sha7>/, seeds 7 to 12 and all 48;
      the row is RAN, and the .70 bar is judged in v25
  A2  lives left alone (engine lives, seeds 41 to 44, 400 x 100 years each): Known, Notable and Historic each within the
      noise band of the baseline's share: |new - base| <= 2 x sqrt(se_base^2 + se_new^2), each se the larger of the
      seed-to-seed one (sd of the four seeds' shares / 2) and the binomial one
  A3  the well-being lift of the reader over a life left alone ("none"), paired by preset and seed (mean of the review's
      'well'): not below the baseline's lift by more than 2 x the paired standard error of the two
  A4  colour-even, on the lives left alone (24 played lives are too few to split by colour; their Known by preset is
      printed): Known or higher, and an aim reached half way up its ladder or more, by the colour leading at 40 and by
      the two leading colours (pairs with 30 lives or more): the highest share over the lowest no wider than the
      baseline's Known split the same way (its fairness band: by leading colour 1.265, by leading pair 1.258, read
      from engine_e69b3bf here, v23.1's lives run again with the pairs kept, the same 1,600 lives as A0's); colours or
      pairs with too few lives are named
  A5  Bold ways on (the candidate) against off (--off): reader+aims reaches Known or Notable more often with it on;
      B3 and B7 are read from their own tools (not here)"""
import argparse, glob, json, math, os, sys, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = HERE if os.path.isfile(os.path.join(HERE, "heights_judge.py")) else \
    os.path.join(os.path.dirname(os.path.dirname(HERE)), "heights")   # the repo copy (chroma-release/v25/) keeps its judge beside it
sys.path.insert(0, BASE)
import heights_judge as HJ   # noqa: E402

COL = "WUBRG"
HEIGHTS = ("ge_known_strict", "ge_notable", "historic")
NAMES = dict(ge_known_strict="Known", ge_notable="Notable", historic="Historic")


def frac(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def se_seed(lives, k):
    """The larger of the seed-to-seed standard error and the binomial one, for the pooled share."""
    seeds = sorted({l["seed"] for l in lives})
    p = frac([l[k] for l in lives]); n = len(lives)
    b = math.sqrt(p * (1 - p) / n) if n > 1 else 0.0
    if len(seeds) < 2:
        return b
    ps = [frac([l[k] for l in lives if l["seed"] == s]) for s in seeds]
    m = sum(ps) / len(ps); sd = math.sqrt(sum((x - m) ** 2 for x in ps) / (len(ps) - 1))
    return max(b, sd / math.sqrt(len(ps)))


def engine_lives(pattern):
    """heights_judge's engine lives, with v24's extras (aims, pair40) where the run has them."""
    L = HJ.engine_lives(pattern)
    i = 0
    for f in sorted(glob.glob(pattern)):
        d = json.load(open(f))
        for n in range(d["N"]):
            L[i]["aim_half"] = None if not d.get("aims") else (d["aims"][n].get("frac") or 0) >= 0.5
            L[i]["pair40"] = None if not d.get("pair40") else tuple(d["pair40"][n])
            i += 1
    assert i == len(L)
    return L


def spread(lives, key, k, min_n=30):
    groups = defaultdict(list)
    for l in lives:
        if l.get(key) is not None and l.get(k) is not None:
            groups[l[key]].append(l[k])
    ok = {g: frac(v) for g, v in groups.items() if len(v) >= min_n}
    few = sorted(g for g, v in groups.items() if len(v) < min_n)
    if len(ok) < 2 or min(ok.values()) <= 0:
        return None, ok, few, groups
    return max(ok.values()) / min(ok.values()), ok, few, groups


def name(g):
    return COL[g] if isinstance(g, int) else "".join(COL[x] for x in g)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("sha7"); a.add_argument("--off"); a.add_argument("--out")
    a.add_argument("--play-dir"); a.add_argument("--engine-dir")   # trials: other folders in place of play_<sha7>, engine_<sha7>
    a.add_argument("--wide-dir")   # A1's seeds 7 to 12, in place of wide_<sha7>
    a = a.parse_args()
    s7 = a.sha7[:7]
    rep = [f"v24 heights (records/v24/scope.md A1 to A5) on {s7}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
           "", __doc__.split("\n\n", 2)[2].strip(), ""]
    verdict = {}
    B_eng = engine_lives(os.path.join(BASE, "engine_e69b3bf", "eng_*.json"))
    B_pair = engine_lives(os.path.join(HERE, "engine_e69b3bf", "eng_*.json"))   # A0's lives again, with pair40 kept (A4)
    B_play = HJ.play_lives(os.path.join(BASE, "play_e69b3bf"))
    N_eng = engine_lives(os.path.join(a.engine_dir or os.path.join(HERE, f"engine_{s7}"), "eng_*.json"))
    N_play = HJ.play_lives(a.play_dir or os.path.join(HERE, f"play_{s7}"))
    pol = lambda P, p: [l for l in P if l["policy"] == p]
    # A1
    ra = pol(N_play, "reader+aims")
    wd = a.wide_dir or os.path.join(HERE, f"wide_{s7}")
    rw = pol(HJ.play_lives(wd), "reader+aims") if os.path.isdir(wd) else []
    if len(ra) == 24:
        k = sum(l["ge_known_strict"] for l in ra); v = k / 24
        verdict["A1"] = "RAN"   # read only in v24: Emren typed "Bar to v25" (10-20 08:37 UTC)
        kw = sum(l["ge_known_strict"] for l in rw)
        more = (f"; seeds 7 to 12 {kw / 24:.3f} ({kw} of 24); all 48 {(k + kw) / 48:.3f} ({k + kw} of 48)" if len(rw) == 24
                else f"; seeds 7 to 12: {len(rw)} of 24 lives in {os.path.basename(wd)}, not read")
        rep.append(f"A1 heights_skilled: reader+aims Known or higher, seeds 1 to 6 {v:.3f} ({k} of 24){more}; v23.1 .583 on 24;"
                   f" read only in v24, the .70 bar in v25: {verdict['A1']}")
    else:
        rep.append(f"A1 heights_skilled: {len(ra)} of 24 reader+aims lives in play_{s7}: not read")
    # A2
    if len(N_eng) >= 1600:
        bad = []
        for k in HEIGHTS:
            pb, pn = frac([l[k] for l in B_eng]), frac([l[k] for l in N_eng])
            band = 2 * math.sqrt(se_seed(B_eng, k) ** 2 + se_seed(N_eng, k) ** 2)
            ok = abs(pn - pb) <= band
            bad += [] if ok else [k]
            rep.append(f"   A2 {NAMES[k]:<9} left alone {pn:.4f} (base {pb:.4f}, move {pn - pb:+.4f}, band +-{band:.4f}): {'ok' if ok else 'OUT'}")
        verdict["A2"] = "PASS" if not bad else "FAIL"
        rep.append(f"A2 heights_alone: {len(N_eng)} lives left alone, seeds {sorted({l['seed'] for l in N_eng})}: {verdict['A2']}")
    else:
        rep.append(f"A2 heights_alone: {len(N_eng)} of 1600 lives left alone in engine_{s7}: not read")
    # A3
    def lift(P):
        by = {(l["preset"], l["seed"]): l for l in pol(P, "none") if l.get("well") is not None}
        d = [l["well"] - by[(l["preset"], l["seed"])]["well"] for l in pol(P, "reader")
             if l.get("well") is not None and (l["preset"], l["seed"]) in by]
        if len(d) < 2:
            return None, None, len(d)
        m = sum(d) / len(d); sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
        return m, sd / math.sqrt(len(d)), len(d)
    mb, sb, nb = lift(B_play); mn, sn, nn = lift(N_play)
    if mn is not None and nn == 24:
        floor = mb - 2 * math.sqrt(sb ** 2 + sn ** 2)
        verdict["A3"] = "PASS" if mn >= floor else "FAIL"
        rep.append(f"A3 reader_lift: reader over none {mn:+.4f} +- {sn:.4f} (paired, {nn} lives; base {mb:+.4f} +- {sb:.4f}; "
                   f"floor {floor:+.4f}): {verdict['A3']}")
    else:
        rep.append(f"A3 reader_lift: {nn} paired reader/none lives in play_{s7}: not read")
    # A4
    if len(N_eng) >= 1600:
        bands = {}
        for key, lab, BL in (("lead40", "colour leading at 40", B_eng), ("pair40", "two colours leading at 40", B_pair)):
            bands[key], okb, _, _ = spread(BL, key, "ge_known_strict")
            if bands[key] is None:
                rep.append(f"   A4 the band by the {lab}: not readable on v23.1 ({len(BL)} lives)"); continue
            rep.append(f"   A4 the band: v23.1's Known by the {lab}, highest over lowest {bands[key]:.3f} "
                       f"({', '.join(f'{name(g)} {v:.3f}' for g, v in sorted(okb.items()))})")
        bad = []
        for key, lab in (("lead40", "leading colour"), ("pair40", "leading pair")):
            band = bands[key]
            for k, kl in (("ge_known_strict", "Known"), ("aim_half", "an aim half way")):
                if band is None:
                    bad.append(f"{kl}/{lab}"); continue
                r, ok, few, groups = spread(N_eng, key, k)
                if r is None:
                    rep.append(f"   A4 {kl} by {lab}: not readable ({len(ok)} groups with 30 lives or more)"); bad.append(f"{kl}/{lab}")
                    continue
                o = r <= band
                bad += [] if o else [f"{kl}/{lab}"]
                rep.append(f"   A4 {kl} by {lab}: highest over lowest {r:.3f} (band {band:.3f}): {'ok' if o else 'OUT'}; "
                           + ", ".join(f"{name(g)} {v:.3f} ({len(groups[g])})" for g, v in sorted(ok.items()))
                           + (f"; too few lives: {', '.join(name(g) for g in few)}" if few else ""))
        rp = defaultdict(list)
        for l in ra:
            rp[l["preset"]].append(l["ge_known_strict"])
        rep.append("   A4 reader+aims Known by preset (6 lives each, read only): "
                   + ", ".join(f"preset {p} {sum(v)}/{len(v)}" for p, v in sorted(rp.items())))
        verdict["A4"] = "PASS" if not bad else "FAIL"
        rep.append(f"A4 aims_even: {verdict['A4']}" + (f" (out: {', '.join(bad)})" if bad else ""))
    # A5
    if a.off:
        off = pol(HJ.play_lives(os.path.join(HERE, f"play_{s7}_{a.off}")), "reader+aims")
        if len(ra) == 24 and len(off) == 24:
            kn = lambda P: sum(l["ge_known_strict"] or l["ge_notable"] for l in P)
            on_k, off_k = kn(ra), kn(off)
            verdict["A5"] = "PASS" if on_k > off_k else "FAIL"
            rep.append(f"A5 bold_heights: reader+aims Known or Notable {on_k} of 24 with Bold ways on, {off_k} of 24 off: "
                       f"{verdict['A5']} (B3 and B7 from their own tools)")
        else:
            rep.append(f"A5 bold_heights: {len(ra)} on and {len(off)} off reader+aims lives: not read")
    # the tables
    rep += ["", "Lives left alone, candidate and v23.1:"]
    rep += HJ.table({f"{s7} all": N_eng, "v23.1 all": B_eng}, HJ.KEYS) if N_eng else ["  none"]
    rep += ["", "Played lives by policy, candidate:"]
    pols = sorted({l["policy"] for l in N_play})
    rep += HJ.table({p: pol(N_play, p) for p in pols}, ["ge_known_strict", "ge_notable", "historic", "historic_broad", "rung4", "good_name", "master"]) if pols else ["  none"]
    for p in pols:
        ws = [l["well"] for l in pol(N_play, p) if l.get("well") is not None]
        rep.append(f"    well {p:<14} {sum(ws) / len(ws):.3f} over {len(ws)} lives" if ws else f"    well {p:<14} n/a")
    rep += ["", "Verdicts: " + ", ".join(f"{k} {v}" for k, v in sorted(verdict.items()))]
    txt = "\n".join(rep) + "\n"
    if a.out:
        open(a.out, "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
