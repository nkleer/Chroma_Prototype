"""v22.1 re-pin check: one whole life played through the page's own bridge (console.Console, as web/worker.js runs it),
every step's [text, busy, feed, hud] JSON kept, so two builds can be compared byte for byte. Deterministic: the seed and
name come from a seeded `random`; at a moment the script alternates letting them choose and pushing option 2.
    python3 -B test/same_life.py <preset 1-6> <seed> <out.jsonl>   (prints the md5 of the whole record)"""
import sys, os, json, random, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as _np
preset, seed, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
random.seed(seed)
from console import Console
c = Console()
def dflt(o):
    if isinstance(o, _np.generic): return o.item()
    if isinstance(o, _np.ndarray): return o.tolist()
    return str(o)
h = hashlib.md5(); n = 0; f = open(out, "w")
def step(line):
    global n
    text, busy = c.handle(line)
    rec = json.dumps([line, text, bool(busy), c.take_feed(), c.hud()], default=dflt, sort_keys=True)
    h.update(rec.encode()); f.write(rec + "\n"); n += 1
    return busy
step(""); step(preset); step("Ari")
k = 0
while c.mode == "play" and n < 20000:
    line = ""
    if c.g is not None and c.g.pending is not None:
        k += 1; line = "" if k % 2 else "2"
    while step(line): line = ""
f.close()
print(preset, seed, "steps", n, "age", c.g.age() if c.g else None, "md5", h.hexdigest())
