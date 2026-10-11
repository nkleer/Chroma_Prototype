"""v22.4 row G19 (records/v22.4/scope.md; item 26, "Colour choices lead somewhere", Engine PR #151): judges a run of
chroma-engine/tools/choice_check.py against the row's targets. Its `sum` prints the tables but no verdict.

  identity  each steered group's identity in its own colour at 40 is at least the unsteered group's + .15
  content   no steered group's mean contentment over ages 30 to 70 is more than .12 below the unsteered group's;
            Black's drop is printed but not judged (Emren 10-11 01:37: accepted as Black's cost of belonging)
  perks     perks held at 50, 90th percentile, at most 27 in every group (the unsteered one too)
  edge      Black's edge (Engine PR #176; Emren 10-11 01:37, "give black a slight advantage boost, compared to others"):
            the run's black_edge is above 0 with role_practice on (the engine's DEFAULT under the run's PX)

Printed as information, not judged: each drop's standard error over lives (a bootstrap over the group's lives, fixed
seed), and what the edge does: the Black group's money at 60 and perks held at 50 against the other four steered
groups', with the difference's standard error. The edge is slight by Emren's word and its effect on these is about the
size of the noise at G19's run, so the record reports it (scope.md, G19).

    python3 -B chroma-release/check_c26.py <run.npz>

The npz is choice_check.py's (fields grp, groups, W, content, nperks, res, px). The engine is the tree's (or
CHROMA_ENGINE), read through chroma-engine/tools/_engine.py. Exit code 0 and a last line "C26 PASS" when every judged
target holds; else "C26 MISS". Read only."""
import os
import sys
import json
import numpy as np

ID_LIFT, CONTENT_DROP, PERKS_P90 = .15, .12, 27
NOT_JUDGED = {"B"}   # drop reported only (Emren 10-11 01:37)
BOOT = 400
d = np.load(sys.argv[1])
gl = [str(c) for c in d["groups"]]
if "-" not in gl:
    print("C26 MISS: the run has no unsteered group (\"-\")")
    sys.exit(1)
grp = d["grp"]
by = {c: grp == g for g, c in enumerate(gl)}
u = by["-"]
rng = np.random.default_rng(26)


def boot(x, stat):
    """Standard error of stat(x) over x's lives (rows), resampled with replacement."""
    return float(np.std([stat(x[rng.integers(0, len(x), len(x))]) for _ in range(BOOT)]))


cmean = lambda x: float(np.nanmean(x[:, 30:70]))
ok = True
print(f"{'group':10s} {'lives':>6s} {'own colour at 40':>17s} {'unsteered':>10s} {'lift':>6s} {'content 30-70':>14s} "
      f"{'drop':>6s} {'se':>5s} {'perks@50 p90':>13s}")
cu = d["content"][u]
c_u, se_u = cmean(cu), boot(cu, cmean)
for c in gl:
    m = by[c]
    cont = cmean(d["content"][m])
    p90 = float(np.percentile(d["nperks"][m][:, 50], 90))
    line_ok = p90 <= PERKS_P90
    if c == "-":
        print(f"{'unsteered':10s} {int(m.sum()):6d} {'':>17s} {'':>10s} {'':>6s} {cont:14.3f} {'':>6s} {'':>5s} "
              f"{p90:13.0f}  " + ("ok" if line_ok else "MISS"))
    else:
        k = "WUBRG".index(c)
        own, base = float(d["W"][m][:, 40, k].mean()), float(d["W"][u][:, 40, k].mean())
        se = (boot(d["content"][m], cmean) ** 2 + se_u ** 2) ** .5
        line_ok &= own - base >= ID_LIFT and (c in NOT_JUDGED or c_u - cont <= CONTENT_DROP)
        print(f"{c:10s} {int(m.sum()):6d} {own:17.3f} {base:10.3f} {own - base:6.3f} {cont:14.3f} {c_u - cont:6.3f} "
              f"{se:5.3f} {p90:13.0f}  " + ("ok" if line_ok else "MISS")
              + ("  (drop reported, not judged)" if c in NOT_JUDGED else ""))
    ok &= line_ok
print(f"targets: lift >= {ID_LIFT}, drop <= {CONTENT_DROP} (Black's reported, not judged), "
      f"perks at 50 (90th percentile) <= {PERKS_P90}; se: the drop's standard error over lives (information)")

# Black's edge: the switch is judged; what it does is reported
px = json.loads(str(d["px"])) if "px" in d.files else {}
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-engine", "tools"))
    import _engine  # noqa: E402,F401
    import engine as E  # noqa: E402
    P = {**E.DEFAULT, **px}
    edge, rp = float(P.get("black_edge", 0) or 0), bool(P.get("role_practice"))
    edge_ok = edge > 0 and rp
    print(f"Black's edge: black_edge {edge:g}, role_practice {'on' if rp else 'off'} (engine {E.__file__})  "
          + ("ok" if edge_ok else "MISS"))
except Exception as e:   # an engine that cannot be read: the edge is not shown, so the row misses
    edge_ok = False
    print(f"Black's edge: could not read the engine ({type(e).__name__}: {e})  MISS")
ok &= edge_ok
if "B" in gl and "res" in d.files:
    oth = np.zeros(len(grp), bool)
    for c in gl:
        if c not in ("-", "B"):
            oth |= by[c]
    for lab, x, fmt in (("money at 60", d["res"][:, 60, 0], "{:.3f}"), ("perks held at 50", d["nperks"][:, 50], "{:.1f}")):
        b, o = x[by["B"]].astype(float), x[oth].astype(float)
        se = (boot(b, np.mean) ** 2 + boot(o, np.mean) ** 2) ** .5
        print(f"  {lab}: Black {fmt.format(b.mean())}, the other steered groups {fmt.format(o.mean())}, difference "
              f"{b.mean() - o.mean():+.3f} (se {se:.3f}; reported, not judged)")
print("C26 PASS" if ok else "C26 MISS")
sys.exit(0 if ok else 1)
