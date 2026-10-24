"""v25 round 0 (records/v25/evaluation.md section 8): v24's lives read by the v25 rules of records/v25/checks.md.

    python3 -B r0judge.py <engine sha7> [--play <play sha7>] [--out REPORT]

Reads out/v24/heights/engine_<sha7>/ (lives left alone, run.sh engine) and, with --play, play_<sha7>/ (reader-aims).
  A2  Known, Notable and Historic left alone against A0 (v23.1's lives, engine_e69b3bf), "the same within d" with
      d = .05, .03, .005: the 95% interval of the difference, each side's se the larger of the binomial and the
      seed-to-seed one (v24's se_seed). PASS inside, FAIL wholly outside, INCONCLUSIVE otherwise.
  F2  the Known floor, f = 2/3: by leading colour at 40 (5 cohorts) and by the two leading colours at 40 (10), each
      cohort at least 100 lives; weakest over strongest by point estimate, log-scale se from the two binomial ses,
      one-sided 95% bounds. Every life left alone reaches 40 here (engine DEFAULT has self_death off), so "alive at
      40" keeps them all.
  A1  printed only (round 0 has 24 played lives; the row is read on 48 at the freeze): Known share, Wilson 95%."""
import argparse, math, os, sys, time
from collections import defaultdict

H = "/mnt/project-files/chroma-release/out/v24/heights"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE if os.path.isfile(os.path.join(HERE, "heights_v24.py")) else H)   # the repo copy's readers sit beside it
import heights_v24 as V   # noqa: E402

COL = "WUBRG"; F = 2 / 3; MIN = 100
A2D = dict(ge_known_strict=.05, ge_notable=.03, historic=.005)


def wilson(k, n, z=1.96):
    if not n:
        return float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def a2(new, base):
    out = []; worst = "PASS"
    for k, d in A2D.items():
        pn, pb = V.frac([l[k] for l in new]), V.frac([l[k] for l in base])
        se = math.sqrt(V.se_seed(new, k) ** 2 + V.se_seed(base, k) ** 2)
        lo, hi = pn - pb - 1.96 * se, pn - pb + 1.96 * se
        r = "PASS" if -d <= lo and hi <= d else "FAIL" if hi < -d or lo > d else "INCONCLUSIVE"
        worst = max(worst, r, key=["PASS", "INCONCLUSIVE", "FAIL"].index)
        out.append(f"  {V.NAMES[k]:<9} {pn:.4f} against {pb:.4f}: difference {pn - pb:+.4f}, 95% [{lo:+.4f}, {hi:+.4f}],"
                   f" within {d}: {r}")
    return worst, out


def floor(lives, key, k="ge_known_strict"):
    g = defaultdict(list)
    for l in lives:
        if l.get(key) is not None:
            g[l[key]].append(1 if l[k] else 0)
    want = 5 if key == "lead40" else 10
    rate = {c: (sum(v) / len(v), len(v)) for c, v in g.items()}
    rows = [f"    {V.name(c):<3} {p:.3f} ({n} lives)" for c, (p, n) in sorted(rate.items(), key=lambda x: -x[1][0])]
    few = [V.name(c) for c, (_, n) in rate.items() if n < MIN]
    if len(rate) < want or few:
        return "INCONCLUSIVE", rows, (f"{want - len(rate)} cohorts missing; " if len(rate) < want else "") + \
            (f"under {MIN} lives: {', '.join(sorted(few))}" if few else "")
    w = min(rate, key=lambda c: rate[c][0]); s = max(rate, key=lambda c: rate[c][0])
    (rw, nw), (rs, ns) = rate[w], rate[s]
    if rw <= 0:
        return "FAIL", rows, f"{V.name(w)} reaches Known in none of its {nw} lives"
    se = math.sqrt((rw * (1 - rw) / nw) / rw ** 2 + (rs * (1 - rs) / ns) / rs ** 2)
    ratio = rw / rs; lo, hi = ratio * math.exp(-1.645 * se), ratio * math.exp(1.645 * se)
    r = "PASS" if lo >= F else "FAIL" if hi < F else "INCONCLUSIVE"
    return r, rows, f"{V.name(w)} {rw:.3f} over {V.name(s)} {rs:.3f}: ratio {ratio:.3f}, one-sided 95% [{lo:.3f}, {hi:.3f}]"


def main():
    a = argparse.ArgumentParser(); a.add_argument("sha7"); a.add_argument("--play"); a.add_argument("--out")
    a.add_argument("--heights", default=H, help="folder holding engine_<sha7>/ for both sides, e.g. out/v24/heights/pc"
                   " for lives run on Emren's PC (both sides must come from one machine)")
    a = a.parse_args()
    s7 = a.sha7[:7]; R = a.heights
    new = V.engine_lives(os.path.join(R, f"engine_{s7}", "eng_*.json"))
    seeds = {l["seed"] for l in new}   # both sides on the same seeds (an extension adds a block to each, evaluation.md §3)
    base = [l for l in V.engine_lives(os.path.join(R, "engine_e69b3bf", "eng_*.json")) if l["seed"] in seeds]
    if {l["seed"] for l in base} != seeds:
        sys.exit(f"STOP: A0 lacks seeds {sorted(seeds - {l['seed'] for l in base})}: run out/v25/ext.sh on e69b3bf first")
    rep = [f"v25 round 0 by the v25 rules (records/v25/checks.md) on {s7}, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC",
           f"lives left alone: {len(new)} (seeds {sorted({l['seed'] for l in new})}); A0 base {len(base)}; both from {R}", ""]
    r, out = a2(new, base)
    rep += [f"A2 heights left alone against A0 (mandatory): {r}"] + out + [""]
    res = dict(A2=r)
    for key, lab in (("lead40", "colours"), ("pair40", "pairs")):
        r, rows, why = floor(new, key)
        rep += [f"F2 the Known floor by {lab} (mandatory): {r}: {why}"] + rows + [""]
        res["F2 " + lab] = r
    res["F2"] = "PASS" if res["F2 colours"] == res["F2 pairs"] == "PASS" else \
        "FAIL" if "FAIL" in (res["F2 colours"], res["F2 pairs"]) else "INCONCLUSIVE"
    rep += [f"F2 as a row: {res['F2']} (PASS only when both readings pass)", ""]
    if a.play:
        P = V.HJ.play_lives(os.path.join(H, f"play_{a.play[:7]}"))
        k = sum(1 for l in P if l["ge_known_strict"]); n = len(P); lo, hi = wilson(k, n)
        rep += [f"A1 printed (calibration; read on 48 lives at the freeze): reader-aims on {a.play[:7]}, Known {k} of {n}"
                f" = {k / n if n else float('nan'):.3f}, Wilson 95% [{lo:.3f}, {hi:.3f}], target .70"]
        by = defaultdict(list)
        for l in P:
            by[l["preset"]].append(l["ge_known_strict"])
        rep += ["   by preset: " + ", ".join(f"{p} {sum(v)}/{len(v)}" for p, v in sorted(by.items())), ""]
    txt = "\n".join(rep)
    print(txt)
    if a.out:
        open(a.out, "w").write(txt + "\n")


if __name__ == "__main__":
    main()
