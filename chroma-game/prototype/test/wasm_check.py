"""Under wasm32 (run by test/wasm_check.js): lives with the outer world on, every numpy call that would fail casting an
int64 array to int32 logged with its caller, then cast so the life goes on. Prints the spots; none means the browser
runs these lives as CPython does. Also times the lives (row W36: the browser must not feel stuck)."""
import sys, time, traceback, collections
import numpy as np
SPOTS = collections.Counter()
def _where():
    for fr in traceback.extract_stack()[:-2][::-1]:
        if "/w/" in fr.filename:
            return f"{fr.filename.split('/w/')[-1]}:{fr.lineno}: {(fr.line or '').strip()}"
    return "?"
def _wrap(name, argi):
    f = getattr(np, name)
    def g(*a, **k):
        try:
            return f(*a, **k)
        except TypeError as e:
            if "int64" not in str(e):
                raise
            SPOTS[(name, _where())] += 1
            a = list(a)
            for i in argi:
                if i < len(a):
                    a[i] = np.asarray(a[i]).astype(np.intp)
            return f(*a, **k)
    setattr(np, name, g)
for n_, i_ in (("repeat", (1,)), ("bincount", (0,)), ("take", (1,)), ("put", (1,)), ("unravel_index", (0,)),
               ("ravel_multi_index", (0,)), ("argpartition", (1,)), ("partition", (1,))):
    _wrap(n_, i_)
import game
lives, age = int(sys.argv[1]), float(sys.argv[2])
bad = 0
for seed in [4242, 1, 557247, 11, 3][:lives]:
    t0 = time.time()
    try:
        g = game.Game(name="Lale", seed=seed, **{k: v for k, v in game.PRESETS["1"].items() if k not in ("title", "blurb")})
        n = 0
        while not g.over and g.age() < age and n < 4000:
            n += 1; st = g.advance()
            if st == "checkpoint": g.decide(None)
        print(f"seed {seed}: age {g.age():.1f}, world {'on' if g.P.get('world') else 'off'}, {time.time() - t0:.0f} s", flush=True)
    except Exception:
        bad += 1; print(f"seed {seed}: FAILED"); traceback.print_exc(file=sys.stdout)
print("int64 spots under wasm32:", "none" if not SPOTS else "")
for (nm, w), c in SPOTS.most_common():
    print(f"  np.{nm} x{c} at {w}")
print("wasm check:", "PASS" if not SPOTS and not bad else "FAIL")
