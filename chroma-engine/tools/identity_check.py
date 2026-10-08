"""Checklist C-E14: with everything since the go-live off (E.GOLIVE: the v10 weights, sex and gender, the release fixes,
the outer world), the engine lives the same lives as the go-live
engine (engine_v9_golive.py): same seed, same batch, same colors, satisfaction, titles and deaths week by week.
The Library's dreams change which sparks start dreams, so they are left out of the batch here (dreams=1 keeps them,
to show what they change). Also checks that V6_SWITCHES still reproduces v6 on both engines alike.
    python3 -B identity_check.py [lives] [years] [seed] [dreams=0|1]"""
import sys, os, importlib.util
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import engine as E, batch
if os.environ.get("RULES"):   # a folder holding only the go-live earth_rules.py (the rules changed since are content: the
    sys.path.insert(0, os.environ["RULES"])   # Library's next3 rates and gates, which the go-live engine cannot read)
spec = importlib.util.spec_from_file_location("engine_v9_golive", os.path.join(HERE, "engine_v9_golive.py"))
E9 = importlib.util.module_from_spec(spec); spec.loader.exec_module(E9)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60; Y = int(sys.argv[2]) if len(sys.argv) > 2 else 60
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5; keep_dreams = len(sys.argv) > 4 and sys.argv[4] == "1"
L = batch.load_batch("earth", packs=list(batch.PACKS))
if not keep_dreams:
    L.pop("DREAM_TRIGGERS", None); L.pop("DREAMS", None)
KEYS = ("W_hist", "M_hist", "S_hist", "A_hist")
def compare(a, b, label):
    bad = []
    for k in KEYS:
        if not np.array_equal(np.asarray(a[k]), np.asarray(b[k])):
            d = np.abs(np.asarray(a[k], float) - np.asarray(b[k], float)); bad.append(f"{k} max diff {d.max():.3g}")
    for k in ("content", "peace", "stress"):
        if k in a["V_hist"] and not np.array_equal(np.asarray(a["V_hist"][k]), np.asarray(b["V_hist"][k])):
            bad.append(f"V_hist[{k}]")
    if (a.get("roles") is None) != (b.get("roles") is None):
        bad.append("titles and perks on one side only")
    elif a.get("roles") is not None and not np.array_equal(np.asarray(a["roles"]["ever"]), np.asarray(b["roles"]["ever"])):
        bad.append("titles and perks")
    print(f"{label}: {'IDENTICAL' if not bad else 'DIFFERENT: ' + '; '.join(bad)}")
    return not bad
P0 = dict(E.DEFAULT); P0.update(getattr(E, "GOLIVE", {}))   # v10 weights, sex and gender (N1b), release fixes, world: off
ok = compare(E.run(N=N, years=Y, seed=seed, lib=L, P=P0), E9.run(N=N, years=Y, seed=seed, lib=L), f"v10 off vs go-live, {N} lives, {Y} years, seed {seed}" + (" (dreams in)" if keep_dreams else ""))
P10 = dict(E.DEFAULT); P10.update(getattr(E, "GOLIVE", {})); P10.update(E.V6_SWITCHES); P9 = dict(E9.DEFAULT); P9.update(E9.V6_SWITCHES)
ok &= compare(E.run(N=N, years=Y, seed=seed, lib=L, P=P10), E9.run(N=N, years=Y, seed=seed, lib=L, P=P9), "V6_SWITCHES on both")
sys.exit(0 if ok else 1)
