"""Long shots (Emren 2026-10-06, packs thread): a title reached for against long odds is kept in the Book and named in the
review, made or missed. Plays lives where the player pushes every long shot offered.
python3 test/longshot_check.py [lives] [seed]"""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from console import Console
import game
n_lives = int(sys.argv[1]) if len(sys.argv) > 1 else 2
rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
for trial in range(n_lives):
    t0 = time.time(); c = Console(); c.handle("")
    key = rnd.choice(["1", "2", "3", "4"]); c.handle(key); c.handle("L" + str(trial))
    offered = 0; steps = 0; errs = 0
    def send(x):
        global errs
        text, busy = c.handle(x)
        while busy:
            t2, busy = c.handle(""); text += t2
        errs += "[error" in text
    while c.mode == "play" and steps < 20000:   # a life from birth with the world on takes more than 4,000 steps
        steps += 1
        g = c.g; pick = None
        if g.pending is not None and c.numbering:
            by = g.pending.get("by_idx") or {}            # numbering gives the engine's option number, not a list position
            for num, i in c.numbering.items():
                if i in by and game.Game._long_shot(by[i]):
                    pick = num; offered += 1; break
        send(str(pick) if pick is not None else "")
    r = getattr(c.g, "review", None); b = c.g.book()
    if r is None:
        print(f"life {trial} preset {key} not over after {steps} steps (age {c.g.age():.1f}): FAIL"); sys.exit(1)
    print(f"life {trial} preset {key} age {r['age']} long shots offered {offered} kept {len(r['long_shots'])} errors {errs} secs {time.time() - t0:.0f}")
    for x in r["long_shots"][:6]:
        print("   ", x["words"])
    print("    book keys:", b["long"][:6])
