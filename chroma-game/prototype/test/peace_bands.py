"""Where the peace reading's bands fall (game.PEACE_BANDS): play whole lives with the player pushing none, some or most of
the choices, and print how well they lived and how much the life was their own.
python3 test/peace_bands.py [lives per push level]"""
import sys, os, random
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def life(args):
    seed, push = args
    from console import Console
    from game import PRESETS
    rnd = random.Random(seed); c = Console(); c.handle("")
    key = rnd.choice(["1", "2", "3", "4"]); c.handle(key); c.handle("P" + str(seed))
    def send(x):
        _, busy = c.handle(x)
        while busy:
            _, busy = c.handle("")
    n = 0
    while c.mode == "play" and n < 4000:
        n += 1
        if c.g.pending is not None and c.numbering and rnd.random() < push:
            send(str(rnd.choice(list(c.numbering))))
        else:
            send("")
    r = c.g.review
    return push, key, r["fulfilment"], r["serenity"], r["integrity"], r["gifts"], r["reading"]["well"], r["reading"]["own"], r["reading"]["words"]


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    jobs = [(1000 + i * 7 + int(p * 100), p) for p in (0.0, 0.3, 0.7) for i in range(k)]
    with Pool(4) as pool:
        rows = pool.map(life, jobs)
    for r in rows:
        print(f"push {r[0]:.1f} preset {r[1]} sat {r[2]:.2f} peace {r[3]:.2f} integ {r[4]:.2f} gifts {r[5]:.2f} | well {r[6]:.3f} own {r[7]:.3f} | {r[8]}")
