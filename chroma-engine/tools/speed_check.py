"""Checklist C-E15: how long a life takes, the go-live engine (engine_v9_golive.py) against today's engine, with the world
off and on. CPU time of this process (time.process_time), so other work on the machine moves it little.
Target: with the world on, at most about a third slower than the go-live engine.
    python3 -B speed_check.py [lives] [years] [seed] [which: v9,off,on]"""
import sys, os, time, json, importlib.util
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import engine as E, batch
if os.environ.get("RULES"):   # the go-live earth_rules (the go-live engine cannot read today's gates); both engines read it
    sys.path.insert(0, os.environ["RULES"])
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100; Y = int(sys.argv[2]) if len(sys.argv) > 2 else 80
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
which = (sys.argv[4] if len(sys.argv) > 4 else "v9,off,on").split(",")
L = batch.load_batch("earth", packs=list(batch.PACKS))
out = {}
for w_ in which:
    if w_ == "v9":
        spec = importlib.util.spec_from_file_location("engine_v9_golive", os.path.join(HERE, "engine_v9_golive.py"))
        M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M); P = None
    else:
        M = E; P = dict(E.DEFAULT); P["world"] = (w_ == "on")
        if w_ == "on" and "world" not in E.DEFAULT:
            print("world: not built yet"); continue
    t0 = time.process_time(); M.run(N=N, years=Y, seed=seed, lib=L, P=P); dt = time.process_time() - t0
    out[w_] = dt
    print(f"{w_:4s}: {dt:7.1f} s CPU for {N} lives x {Y} years = {1000 * dt / (N * Y):.2f} ms per life-year"
          + (f"  ({dt / out['v9']:.2f}x the go-live engine)" if "v9" in out and w_ != "v9" else ""))
print(json.dumps({k: round(v, 2) for k, v in out.items()}))
