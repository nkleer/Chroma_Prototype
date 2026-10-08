"""Point 9: a saved life loads back exactly. Plays a life with Enter, pushes, steps, settings, a plan and a pause, saves it,
loads it into a fresh console, and compares the engine state, the story's cast and the whole feed.
Run: python3 test/saveload.py [seed]"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from console import Console

def run(c, line):
    """As the browser's worker does: one line, then empty lines while the console is busy."""
    feed = []
    text, busy = c.handle(line); feed += c.take_feed(); c.hud()
    while busy:
        text, busy = c.handle(""); feed += c.take_feed(); c.hud()
    return feed

def state(c):
    g = c.g; loc = g.loc
    return dict(t=g.t, w=np.round(np.asarray(loc["z"][0]), 9).tolist(), y=np.round(np.asarray(loc["y"][0]), 9).tolist(),
                res=np.round(np.asarray(loc["res"][0]), 9).tolist(), cast=[(p["name"], p["role"], p["alive"]) for p in g.story.people],
                pending=None if g.pending is None else g.pending["title"], label=g._prev_label)

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
rng = np.random.default_rng(seed)
a = Console(); fa = []
fa += run(a, "3"); a.custom["seed"] = seed
fa += run(a, "Lale")
for step in range(60):
    if a.mode != "play":
        break
    g = a.g
    if g.pending is not None:
        k = rng.random()
        line = "" if k < 0.5 else str(int(rng.integers(1, len(g.pending["options"]) + 1)))
        fa += run(a, line)
    else:
        k = rng.random()
        if step >= 5 and not any(x.startswith("@stop") for x in a.inputs):   # a pause in the middle of a run
            text, busy = a.handle(""); fa += a.take_feed()
            text, busy = a.handle(""); fa += a.take_feed()
            a.stop(); fa += a.take_feed()
        elif step == 12:
            fa += run(a, "f")
        elif step == 15:
            fa += run(a, "v")
        elif step == 18 and not a.g.hud().get("young"):
            fa += run(a, "p"); fa += run(a, "2"); fa += run(a, "1"); fa += run(a, "")
        else:
            fa += run(a, "" if k < 0.6 else "y" if k < 0.8 else "m")
saved = a.save()
d = json.loads(saved)
print(f"saved {len(saved)} bytes: {d['name']} at {d['age']}, {len(d['inputs'])} inputs; stops: {sum(1 for x in d['inputs'] if x.startswith('@stop'))}")
b = Console(); fb = []
text, busy = b.load(saved); fb += b.take_feed(); b.hud()
n = 0
while busy:
    text, busy = b.handle(""); fb += b.take_feed(); h = b.hud(); n += 1
print("replayed in", n, "steps; note:", h.get("note"), h.get("loaded"))
sa, sb = state(a), state(b)
bad = [k for k in sa if sa[k] != sb[k]]
print("state differs in:", bad or "nothing")
ta = [x["text"] for x in fa if x.get("text")]; tb = [x["text"] for x in fb if x.get("text")]
print("feed lines:", len(ta), len(tb), "same" if ta == tb else "DIFFERENT")
if ta != tb:
    i = next(i for i in range(min(len(ta), len(tb))) if ta[i] != tb[i]) if any(x != y for x, y in zip(ta, tb)) else min(len(ta), len(tb))
    print("first difference at", i, repr(ta[i][:120]) if i < len(ta) else None, "|", repr(tb[i][:120]) if i < len(tb) else None)
# the loaded life plays on the same as the original
if a.mode != "play" or b.mode != "play":   # the life ended in the run (a death at the last step): nothing to play on
    print("life over at", round(a.g.age(), 1), "; modes", a.mode, b.mode, "; next-run check skipped")
    sys.exit(1 if bad or ta != tb or a.mode != b.mode else 0)
fa2 = run(a, ""); fb2 = run(b, "")
print("next run same:", [x.get("text") for x in fa2] == [x.get("text") for x in fb2], "; next save same:", a.save().split('"inputs"')[1] == b.save().split('"inputs"')[1])
sys.exit(1 if bad or ta != tb else 0)
