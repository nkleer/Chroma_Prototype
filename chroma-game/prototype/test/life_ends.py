"""Every life reaches its end, with no console error on the way: plays the peace_bands lives (Enter, or a push now and
then) and reports any that stop before the review or hit an error, with the traceback.
python3 test/life_ends.py [lives per push level] [first seed]"""
import sys, os, random, traceback, functools
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def life(args):
    seed, push = args
    import console
    from console import Console
    traces = []
    for nm in ("_on_play", "_work", "_review"):
        f = getattr(Console, nm)
        if getattr(f, "_wrapped", False):
            continue
        def w(self, *a, _f=f, **k):
            try:
                return _f(self, *a, **k)
            except Exception:
                traces.append(traceback.format_exc()); raise
        w._wrapped = True; setattr(Console, nm, w)
    rnd = random.Random(seed); c = Console(); c.handle("")
    key = rnd.choice(["1", "2", "3", "4"]); c.handle(key); c.handle("P" + str(seed))
    errs = []
    def send(x):
        t, busy = c.handle(x); k = 0
        if t and "[error" in t: errs.append(t[:300])
        while busy and k < 5000:
            t, busy = c.handle(""); k += 1
            if t and "[error" in t: errs.append(t[:300])
    n = 0
    while c.mode == "play" and n < 1500 and not errs:
        n += 1
        if c.g.pending is not None and c.numbering and rnd.random() < push:
            send(str(rnd.choice(list(c.numbering))))
        else:
            send("")
    g = c.g
    return dict(seed=seed, push=push, preset=key, steps=n, mode=c.mode, age=round(g.t / 52, 1), review=hasattr(g, "review"),
                errs=errs[:2], trace=traces[-1] if traces else "")


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    s0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    jobs = [(s0 + i * 7 + int(p * 100), p) for p in (0.0, 0.3, 0.7) for i in range(k)]
    bad = 0
    with Pool(4) as pool:
        for r in pool.imap_unordered(life, jobs):
            fail = not r["review"] or r["errs"]
            bad += bool(fail)
            print(f"seed {r['seed']} push {r['push']} preset {r['preset']} steps {r['steps']} mode {r['mode']} age {r['age']}"
                  + ("  <-- " + ("ERROR" if r["errs"] else "NO REVIEW") if fail else ""), flush=True)
            if fail:
                print("   ", r["errs"], "\n", r["trace"], flush=True)
    print("lives that did not end cleanly:", bad, "of", len(jobs))
