"""v22.4 row G19 (records/v22.4/scope.md; item 26, "Colour choices lead somewhere", Engine PR #151): judges a run of
chroma-engine/tools/choice_check.py against the row's three targets. Its `sum` prints the tables but no verdict.

  identity  each steered group's identity in its own colour at 40 is at least the unsteered group's + .15
  content   no steered group's mean contentment over ages 30 to 70 is more than .12 below the unsteered group's
  perks     perks held at 50, 90th percentile, at most 27 in every group (the unsteered one too)

    python3 -B chroma-release/check_c26.py <run.npz>

The npz is choice_check.py's (fields grp, groups, W, content, nperks). Exit code 0 and a last line "C26 PASS" when all
three hold; else "C26 MISS". Read only."""
import sys
import numpy as np

ID_LIFT, CONTENT_DROP, PERKS_P90 = .15, .12, 27
d = np.load(sys.argv[1])
gl = [str(c) for c in d["groups"]]
if "-" not in gl:
    print("C26 MISS: the run has no unsteered group (\"-\")")
    sys.exit(1)
grp = d["grp"]
by = {c: grp == g for g, c in enumerate(gl)}
u = by["-"]
ok = True
print(f"{'group':10s} {'lives':>6s} {'own colour at 40':>17s} {'unsteered':>10s} {'lift':>6s} {'content 30-70':>14s} "
      f"{'drop':>6s} {'perks@50 p90':>13s}")
c_u = float(np.nanmean(d["content"][u][:, 30:70]))
for c in gl:
    m = by[c]
    cont = float(np.nanmean(d["content"][m][:, 30:70]))
    p90 = float(np.percentile(d["nperks"][m][:, 50], 90))
    line_ok = p90 <= PERKS_P90
    if c == "-":
        print(f"{'unsteered':10s} {int(m.sum()):6d} {'':>17s} {'':>10s} {'':>6s} {cont:14.3f} {'':>6s} {p90:13.0f}  "
              + ("ok" if line_ok else "MISS"))
    else:
        k = "WUBRG".index(c)
        own, base = float(d["W"][m][:, 40, k].mean()), float(d["W"][u][:, 40, k].mean())
        line_ok &= own - base >= ID_LIFT and c_u - cont <= CONTENT_DROP
        print(f"{c:10s} {int(m.sum()):6d} {own:17.3f} {base:10.3f} {own - base:6.3f} {cont:14.3f} {c_u - cont:6.3f} "
              f"{p90:13.0f}  " + ("ok" if line_ok else "MISS"))
    ok &= line_ok
print(f"targets: lift >= {ID_LIFT}, drop <= {CONTENT_DROP}, perks at 50 (90th percentile) <= {PERKS_P90}")
print("C26 PASS" if ok else "C26 MISS")
sys.exit(0 if ok else 1)
