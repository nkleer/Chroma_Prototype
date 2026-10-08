"""Release check C-E14 (chroma-release/checklist.md, section 9).

With everything added since the go-live switched off (engine.GOLIVE: the v10 weights, sex and gender, the release fixes,
the outer world), today's engine must live the same lives as the go-live engine (engine_v9_golive.py): same seeds, same
batch, every output both engines return equal. engine.V6_SWITCHES must still give the same lives on both engines.

Read only: it imports the engine from --proto and the Library through batch.py, and writes nothing in either folder.
Everything printed also goes to chroma-release/out/identity_<UTC time>.txt.
The Library's dreams are taken out of the batch, because the go-live engine never read them (the Engine's own
prototype/identity_check.py does the same).

    python3 -B chroma-release/check_identity.py [--proto DIR] [--lib DIR] [--rules DIR] [--lives 40] [--years 70]
                                                [--seeds 5,21,57] [--packs science,politics,stage]

  --proto  the engine folder (default chroma-engine/prototype). The final check runs it on the game's pin as well.
  --lib    a Library folder to read instead of chroma-library. Keep it a batch the go-live rules can read: next3's new
           moments have no conditions in the go-live earth_rules.py, so load_batch stops on them (11:47); the check
           holds the content fixed at the live v21 batch, as the Engine's identity_check does.
  --rules  a folder holding only the go-live earth_rules.py, put first on the path (as the Engine's RULES variable).
           Default: a temporary copy of the game's v21 pin of it (chroma-game/prototype-v21/engine_pin/, whose
           engine.py is byte-identical to engine_v9_golive.py). The go-live engine cannot read today's gates (it has no
           `younger_siblings`), and the rules are content both engines read the same way.

Exit code 0 when every comparison is identical, 1 otherwise."""
import sys, os, argparse, importlib.util, time, shutil, tempfile, atexit
import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma-env"))
os.environ.setdefault("CHROMA_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the tree this script sits in
from paths import P, path, ROOT   # backend plan item 6: every folder is named once, in chroma-env/paths.py
ap = argparse.ArgumentParser()
ap.add_argument("--proto", default=P["engine_v23"])   # calib scripts and engine_v9_golive.py live here (backend item 7 may rename)
ap.add_argument("--golive", default=None, help="the go-live engine (default engine_v9_golive.py in chroma-engine/tools, else in --proto)")
ap.add_argument("--lib", default=None)
ap.add_argument("--rules", default=os.environ.get("RULES"))
ap.add_argument("--lives", type=int, default=40)
ap.add_argument("--years", type=int, default=70)
ap.add_argument("--seeds", default="5,21,57")
ap.add_argument("--packs", default=None, help="comma list; default batch.PACKS")
a = ap.parse_args()

class Tee:   # everything printed also goes to chroma-release/out/identity_<UTC time>.txt
    def __init__(self, *f): self.f = f
    def write(self, x):
        for f_ in self.f: f_.write(x)
    def flush(self):
        for f_ in self.f: f_.flush()
os.makedirs(P["release_out"], exist_ok=True)
REPORT = path("release_out", time.strftime("identity_%Y%m%d-%H%M.txt", time.gmtime()))
sys.stdout = Tee(sys.__stdout__, open(REPORT, "w"))

PROTO = os.path.abspath(a.proto)
sys.path.insert(0, PROTO)
GOLIVE_RULES = path("game_v21", "engine_pin", "earth_rules.py")   # the v21 game's pinned rules (go-live engine)
if not a.rules and os.path.exists(GOLIVE_RULES):
    a.rules = tempfile.mkdtemp(prefix="golive_rules_")
    atexit.register(shutil.rmtree, a.rules, True)
    shutil.copy(GOLIVE_RULES, a.rules)
if a.rules:
    sys.path.insert(0, os.path.abspath(a.rules))
import engine as E, batch
if a.lib:
    batch.LIB_DIR = os.path.abspath(a.lib)
GOLIVE = a.golive or next((f for f in (os.path.join(ROOT, "chroma-engine", "tools", "engine_v9_golive.py"),   # the Engine's tools
                                         os.path.join(PROTO, "engine_v9_golive.py")) if os.path.exists(f)),          # (backend item 7)
                           os.path.join(PROTO, "engine_v9_golive.py"))
spec = importlib.util.spec_from_file_location("engine_v9_golive", GOLIVE)
E9 = importlib.util.module_from_spec(spec); spec.loader.exec_module(E9)

packs = list(batch.PACKS) if a.packs is None else [p for p in a.packs.split(",") if p]
L = batch.load_batch("earth", packs=packs)
for k in ("DREAM_TRIGGERS", "DREAMS"):
    L.pop(k, None)

SKIP = {"world", "sit_names", "read_names"}
NOTES = []   # new columns appended to an output (a role added at the end, like R15's living children)   # None with the world off; names, not lives


def diff(x, y, path, out):
    """Every place where two run outputs differ, as (path, what) pairs. Keys only one engine returns are noted apart."""
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) & set(y), key=str):
            if path == "" and k in SKIP:
                continue
            diff(x[k], y[k], f"{path}.{k}" if path else str(k), out)
        return
    if x is None or y is None:
        if (x is None) != (y is None):
            out.append((path, "None in one engine only"))
        return
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and not (len(x) and isinstance(x[0], (int, float, np.number))):
        if len(x) != len(y):
            out.append((path, f"length {len(x)} vs {len(y)}"))
            return
        for i, (u, v) in enumerate(zip(x, y)):
            n0 = len(out)
            diff(u, v, f"{path}[{i}]", out)
            if len(out) > n0:          # the first differing entry is enough to find it
                return
        return
    try:
        ax, ay = np.asarray(x), np.asarray(y)
    except Exception:
        if x != y:
            out.append((path, "differs"))
        return
    if ax.shape != ay.shape:
        if ax.ndim == ay.ndim and ax.ndim >= 1 and ax.shape[:-1] == ay.shape[:-1] and ax.shape[-1] > ay.shape[-1]:
            NOTES.append(f"{path}: today's engine adds {ax.shape[-1] - ay.shape[-1]} column(s) at the end; the first "
                         f"{ay.shape[-1]} are compared")
            ax = ax[..., :ay.shape[-1]]
        else:
            out.append((path, f"shape {ax.shape} vs {ay.shape}"))
            return
    if ax.dtype.kind in "fcib" and ay.dtype.kind in "fcib":
        eq = (ax == ay) | (np.isnan(ax) & np.isnan(ay)) if ax.dtype.kind in "fc" else (ax == ay)
        if not np.all(eq):
            where = np.argwhere(~eq)[0].tolist() if ax.ndim else []
            gap = float(np.nanmax(np.abs(ax.astype(float) - ay.astype(float))))
            out.append((path, f"largest gap {gap:.3g}, first at index {where}" + (" (year, life...)" if path.endswith("_hist") else "")))
    elif not np.array_equal(ax, ay):
        out.append((path, "differs"))


def compare(label, P_new, P_old, seed):
    t0 = time.time()
    o_new = E.run(N=a.lives, years=a.years, seed=seed, lib=L, P=P_new)
    t1 = time.time()
    o_old = E9.run(N=a.lives, years=a.years, seed=seed, lib=L, P=P_old)
    t2 = time.time()
    out = []
    diff(o_new, o_old, "", out)
    only_new = sorted(set(o_new) - set(o_old)); only_old = sorted(set(o_old) - set(o_new))
    head = f"{label}, seed {seed}, {a.lives} lives x {a.years} years ({t1 - t0:.0f} s today, {t2 - t1:.0f} s go-live)"
    if out:
        print(f"MISS {head}: {len(out)} outputs differ")
        for p_, w_ in out[:25]:
            print(f"       {p_}: {w_}")
        if len(out) > 25:
            print(f"       ... and {len(out) - 25} more")
    else:
        print(f"ok   {head}: identical")
    for n_ in sorted(set(NOTES)):
        print(f"       info: {n_}")
    NOTES.clear()
    if only_old:
        print(f"       outputs only the go-live engine returns: {', '.join(only_old)}")
    return not out, only_new


print(f"C-E14 identity: engine {os.path.join(PROTO, 'engine.py')}; go-live engine {GOLIVE}")
print("  rules:", a.rules or "the engine's own earth_rules.py")
print(f"  Library {batch.LIB_DIR}, packs {packs}, dreams left out; switches off: {sorted(getattr(E, 'GOLIVE', {}))}")
if not hasattr(E, "GOLIVE"):
    print("MISS engine.GOLIVE is missing: nothing turns the new parts off")
ok = True; new_keys = set()
for sd in [int(x) for x in a.seeds.split(",")]:
    P0 = dict(E.DEFAULT); P0.update(getattr(E, "GOLIVE", {}))
    r, nk = compare("go-live switches vs engine_v9_golive.py", P0, None, sd); ok &= r; new_keys |= set(nk)
sd = int(a.seeds.split(",")[0])
P10 = dict(E.DEFAULT); P10.update(getattr(E, "GOLIVE", {})); P10.update(E.V6_SWITCHES)
P9 = dict(E9.DEFAULT); P9.update(E9.V6_SWITCHES)
r, _ = compare("V6_SWITCHES on both engines", P10, P9, sd); ok &= r
# the same seed twice: nothing outside the seed (time, dict order, a global generator) reaches the lives
P0 = dict(E.DEFAULT)
o1 = E.run(N=a.lives // 2, years=a.years // 2, seed=sd, lib=L, P=P0)
o2 = E.run(N=a.lives // 2, years=a.years // 2, seed=sd, lib=L, P=dict(P0))
out = []; diff(o1, o2, "", out)
print(("ok   " if not out else "MISS ") + f"today's engine, all defaults, the same seed twice: " + ("identical" if not out else f"{len(out)} outputs differ, e.g. {out[0]}"))
ok &= not out
if new_keys:
    print(f"  info: outputs only today's engine returns (not compared): {', '.join(sorted(new_keys))}")
print("C-E14:", "PASS" if ok else "FAIL")
print("report:", REPORT)
import results; results.done('identity', 0 if ok else 1, REPORT)   # backend plan item 4: the result in out/results.jsonl
sys.exit(0 if ok else 1)
