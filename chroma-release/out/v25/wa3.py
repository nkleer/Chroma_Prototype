"""v25 WA3 (records/v25/checks.md, "WA3 Standing", mandatory): each ring's median share of its change rises with the
life's highest standing level (world-answers-v1.md section 5).

    python3 -B wa3.py <wa run folder (wa_check.py run outputs, wa*.json)> [--out REPORT]

Per life: its share of the change in its groups, its places and its town (wa_check.py's share(): what the life caused
over the ring's total), and its highest standing level (`standing_peak`, 0 to 3). For each ring, the levels held by 30
lives or more, from the lowest upward; at each step the difference of the medians with a 95% bootstrap interval (each
level resampled on its own, 4,000 draws, seed 0). PASS when every step of every ring lies above 0; FAIL when a step's
interval lies wholly at or below 0; INCONCLUSIVE otherwise, or when a ring has fewer than two levels with 30 lives.
Beside it (shown): the same by highest rung, v24's reading."""
import argparse, glob, json, os, sys
import numpy as np

MIN = 30; RINGS = ("groups", "places", "town")


def share(l, ring):   # wa_check.py's share(), the same arithmetic
    c = (l["direct"][ring] or 0.0) + sum(v or 0.0 for k, v in l["ledger"][ring].items() if k != "direct")
    t = l["total"][ring] or 0.0
    if t > 1e-12:
        return c / t
    return 0.0 if c <= 1e-12 else None


def steps(L, key, rng):
    out = {}; worst = "PASS"
    for ring in RINGS:
        by = {}
        for l in L:
            s, v = l.get(key), share(l, ring)
            if s is not None and v is not None:
                by.setdefault(int(s), []).append(v)
        levels = sorted(k for k, v in by.items() if len(v) >= MIN)
        rows = [f"{k}: median {np.median(by[k]):.4f} ({len(by[k])})" for k in sorted(by)]
        if len(levels) < 2:
            out[ring] = ("INCONCLUSIVE", rows, ["fewer than two levels with 30 lives"]); worst = max(worst, "INCONCLUSIVE", key=ORDER.index)
            continue
        res = "PASS"; st = []
        for a, b in zip(levels, levels[1:]):
            A, B = np.asarray(by[a]), np.asarray(by[b])
            d = np.median(rng.choice(B, (4000, len(B))), axis=1) - np.median(rng.choice(A, (4000, len(A))), axis=1)
            lo, hi = np.quantile(d, [0.025, 0.975]); r = "PASS" if lo > 0 else "FAIL" if hi <= 0 else "INCONCLUSIVE"
            res = max(res, r, key=ORDER.index)
            st.append(f"{a} to {b}: {np.median(B) - np.median(A):+.4f} [{lo:+.4f}, {hi:+.4f}] {r}")
        out[ring] = (res, rows, st); worst = max(worst, res, key=ORDER.index)
    return worst, out


ORDER = ["PASS", "INCONCLUSIVE", "FAIL"]


def main():
    a = argparse.ArgumentParser(); a.add_argument("run"); a.add_argument("--out"); a = a.parse_args()
    fs = sorted(glob.glob(os.path.join(a.run, "wa*.json")))
    L = [l for f in fs for l in json.load(open(f))["lives"]]
    d0 = json.load(open(fs[0]))
    rep = [f"v25 WA3 on {d0.get('sha', '?')[:12]}: {len(L)} lives from {len(fs)} runs ({', '.join(os.path.basename(f) for f in fs)})"]
    worst, out = steps(L, "standing_peak", np.random.default_rng(0))
    rep.append(f"WA3 by highest standing level (mandatory): {worst}")
    for ring, (r, rows, st) in out.items():
        rep.append(f"  {ring}: {r}; " + "; ".join(rows)); rep += [f"    {s}" for s in st]
    w2, out2 = steps(L, "rung_peak", np.random.default_rng(0))
    rep.append(f"Beside it, by highest rung (v24's reading, shown): {w2}")
    for ring, (r, rows, st) in out2.items():
        rep.append(f"  {ring}: {r}; " + "; ".join(rows)); rep += [f"    {s}" for s in st]
    txt = "\n".join(rep); print(txt)
    if a.out:
        open(a.out, "w").write(txt + "\n")


if __name__ == "__main__":
    main()
