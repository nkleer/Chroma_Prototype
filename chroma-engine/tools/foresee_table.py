"""Measure foresee.HINT: how plans turn out in simulated lives, given the felt odds at the start and what felt odds leave
out (self-control, free time, stress, fit with who one is, a domain plan). One logistic model per horizon.
python3 calib_v7/foresee_table.py [N] [seed] [earth|seed] [P json]   (run from prototype/)"""
import collections, json, sys
sys.path.insert(0, ".")
import numpy as np
import engine as E

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 3
lib = sys.argv[3] if len(sys.argv) > 3 else "earth"
P = {"goals": True, "history": "calm", **(json.loads(sys.argv[4]) if len(sys.argv) > 4 else {})}
L = None
if lib == "earth":
    from batch import load_batch
    L = load_batch("earth")
o = E.run(N=N, seed=seed, years=80, P=P, lib=L)

ev = collections.defaultdict(list)
for g in o["goals"]:
    ev[(g["life"], g["id"])].append(g)
rows = collections.defaultdict(list)
for key, gs in ev.items():
    b = [g for g in gs if g["what"] == "begins" and g["kind"] == "plan"]
    if not b:
        continue
    b = b[-1]
    ends = [g["what"] for g in gs if g["what"] in ("achieved", "let go", "not reached in time", "drifted away", "pushed aside")]
    if not ends:
        continue
    ontime = ends[-1] == "achieved" and not any(g["what"] == "extended" for g in gs)
    f = min(max(b["felt"], 0.01), 0.99)
    rows[b["horizon"]].append([1.0, np.log(f / (1 - f)), b["self_control"], b["free_time"], b["stress"], b["fit"],
                               float(b["domain"] != "a pursuit"), float(ontime), b["felt"]])


def logit_fit(X, y, l2=1e-2, it=50):
    b = np.zeros(X.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p) - l2 * b
        H = (X * (p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(b))
        b = b + np.linalg.solve(H, g)
    return b


HINT = {}
for h in E.HORIZONS:
    R = np.array(rows.get(h, []))
    if len(R) < 30:
        print(f"{h}: only {len(R)} plans ended; kept the felt odds as the hint")
        HINT[h] = [0.0, 1.0, 0, 0, 0, 0, 0]
        continue
    X, y, felt = R[:, :7], R[:, 7], R[:, 8]
    keep = [0, 1, 2, 3, 4, 5] + ([6] if 0 < X[:, 6].mean() < 1 else [])
    b = np.zeros(7); b[keep] = logit_fit(X[:, keep], y)
    p = 1 / (1 + np.exp(-X @ b))
    print(f"{h}: n {len(R)}  on time {y.mean():.2f}  felt {felt.mean():.2f}  Brier felt {np.mean((felt - y) ** 2):.3f}  "
          f"Brier hint {np.mean((p - y) ** 2):.3f}")
    for lo, hi in ((0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)):
        m = (felt >= lo) & (felt < hi)
        if m.sum():
            print(f"    felt {lo:.1f}-{min(hi, 1):.1f}: n {m.sum():4d}  reached in time {y[m].mean():.2f}  hint {p[m].mean():.2f}")
    HINT[h] = [round(float(x), 3) for x in b]
print("HINT = {")
for h in E.HORIZONS:
    print(f"    {h!r}: {HINT[h]},")
print("}")
