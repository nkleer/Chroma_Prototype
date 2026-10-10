"""S6 "Seen it done" refit target (chroma-release/records/v22.4/scope.md, row G10 <s6_felt>): the mean felt-odds lift
per colour way within .01 of each other. [LIB=<folder>] python3 -B chroma-engine/tools/seen_check.py [N] [seed] [years]
['{P}']

Earth with the packs and the outer world on, as the game plays it: the engine's DEFAULT with world and seen_done on, then
'{P}' laid over it (the refit's switch set, when DEFAULT does not carry it). The lift is WorldLink.seen_report's
lift_by_colour: over the options offered, each option's felt-odds lift from what the life has seen walked (its path plus
its colour way), weighted by the option's ways in each colour. Default 60 lives x 80 years, seed 7 (the builder's seed).
The last line is "S6_FELT OK" when the spread (highest colour minus lowest) is at most .01, else "S6_FELT MISS"; exit
code 0 on OK."""
import sys, os, json, time, hashlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
import engine as E, batch as B_
if os.environ.get("LIB"):
    B_.LIB_DIR = os.environ["LIB"]
TARGET = 0.01
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
Y = int(sys.argv[3]) if len(sys.argv) > 3 else 80
PX = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
if "seen_done" not in E.DEFAULT:
    print("S6_FELT MISS: this engine has no seen_done switch")
    sys.exit(1)
P = dict(E.DEFAULT); P["world"] = True; P["seen_done"] = True; P.update(PX)
L = B_.load_batch("earth", packs=list(B_.PACKS))
t0 = time.process_time()
o = E.run(N=N, years=Y, seed=seed, lib=L, P=P)
sr = (o.get("world") or {}).get("seen")
print("engine", _engine.ENGINE, "engine.py", hashlib.md5(open(os.path.join(_engine.ENGINE, "engine.py"), "rb").read()).hexdigest()[:12])
print(f"{N} lives x {Y} years, seed {seed}, world on; P over DEFAULT {json.dumps(dict(seen_done=True, **PX))} "
      f"({time.process_time() - t0:.0f} s)")
if not sr:
    print("S6_FELT MISS: no seen report (seen_done did not switch on: is the world on?)")
    sys.exit(1)
lift = sr["lift_by_colour"]
print("felt-odds lift per colour way:", "  ".join(f"{c_} {v_:.4f}" for c_, v_ in zip("WUBRG", lift)))
print(f"options offered {sr['offered']}, on a path {sr['on_path']} (path lift {sr['path_lift']:.4f}); mean lift "
      f"{sr['mean_lift']:.4f}")
spread = max(lift) - min(lift)
ok = spread <= TARGET
print(f"S6_FELT {'OK' if ok else 'MISS'}: spread {spread:.4f} {'within' if ok else 'over'} {TARGET}")
sys.exit(0 if ok else 1)
