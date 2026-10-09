"""Same lives, engine side: one whole life played through the page's own bridge (console.Console, as web/worker.js runs
it), keeping at every step only what the engine holds (the week, the colours, wants, means, resources, needs, strain,
pent-up wanting, habit, mood, satisfaction, peace and the moment put to the player), so two builds whose screens differ
can still be compared for the life itself. Copy it into any game folder's test/ to run it there.
    python3 -B test/same_engine.py <preset 1-6> <seed> <own|push> <out.jsonl>   (prints the md5 of the whole record)
own: the player always lets them choose. push: as test/same_life.py, letting them choose and pushing option 2 in turn.
"""
import sys, os, json, random, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
preset, seed, mode, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
random.seed(seed)
from console import Console
KEYS = ("w", "y", "z", "res", "need", "stress", "Q", "habit", "mood", "content", "peace", "wound", "held")
c = Console()
h = hashlib.md5(); n = 0; f = open(out, "w")
def step(line):
    global n
    text, busy = c.handle(line)
    g = c.g
    if g is not None and g.loc is not None:
        loc = g.loc
        rec = dict(t=int(g.t), pending=(g.pending or {}).get("title") if isinstance(g.pending, dict) else None,
                   **{k: np.round(np.asarray(loc[k][0], float), 12).tolist() for k in KEYS if k in loc})
        s = json.dumps([line, rec], sort_keys=True)
        h.update(s.encode()); f.write(s + "\n"); n += 1
    return busy
step(""); step(preset); step("Ari")
k = 0
while c.mode == "play" and n < 20000:
    line = ""
    if c.g is not None and c.g.pending is not None:
        k += 1; line = "" if (mode == "own" or k % 2) else "2"
    while step(line): line = ""
f.close()
print(preset, seed, mode, "steps", n, "age", round(c.g.age(), 2) if c.g else None, "md5", h.hexdigest())
