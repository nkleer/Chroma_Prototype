"""N6 with the outer world (row W41): a life born into the world an earlier life left behind (and one as its
grandchild) saves and loads back exactly, the world travelling beside the save as the page keeps it (IndexedDB, or
world_data in a save file). Life 1 is played to 12 and its world kept; life 2 is played with choices, pushes and
steps, saved, loaded into a fresh console with the world handed in first, and compared: engine state, cast and feed.
Run: python3 test/saveload_world.py [seed]"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import console as C

def run(c, line):
    feed = []
    text, busy = c.handle(line); feed += c.take_feed(); c.hud()
    while busy:
        text, busy = c.handle(""); feed += c.take_feed(); c.hud()
    return feed

def state(c):
    g = c.g; loc = g.loc
    return dict(t=g.t, w=np.round(np.asarray(loc["z"][0]), 9).tolist(), res=np.round(np.asarray(loc["res"][0]), 9).tolist(),
                cast=[(p["name"], p["role"], p["alive"]) for p in g.story.people], world_t=int(loc["WL"].W.t) if loc.get("WL") is not None else None)

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 77
a = C.Console(); a.handle(str(len(C.PRESETS) + 1))
for x in ["Lale", "1", "1", "3", "3", "1", "", "2", "1", "", "0", "4242"]:
    a.handle(x)
g = a.g; n = 0
while not g.over and g.age() < 12 and n < 3000:
    n += 1; st = g.advance()
    if st == "checkpoint": g.decide(None)
wo = a.world_out(); d = json.loads(wo)
print(f"life 1: {d['name']} to {d['age']}, world kept ({len(wo)} bytes)")
ok = True
for gc in (False, True):
    rng = np.random.default_rng(seed)
    b = C.Console(); b.world_in(json.dumps(dict(key=d["key"], name=d["name"], age=d["age"])))
    b.handle(str(len(C.PRESETS) + 1)); b.handle("Mira"); b.handle("2"); b.handle("1")
    b.world_in(wo); b.handle("3" if gc else "2")
    fb = []
    for x in ["1", "", "2", "1", "", "0", str(seed)]:
        fb += run(b, x)
    for step in range(40):
        if b.mode != "play":
            break
        if b.g.pending is not None:
            k = rng.random()
            fb += run(b, "" if k < 0.5 else str(int(rng.integers(1, len(b.g.pending["options"]) + 1))))
        else:
            k = rng.random()
            fb += run(b, "" if k < 0.6 else "y" if k < 0.85 else "m")
    saved = b.save(); sd = json.loads(saved)
    c = C.Console(); c.world_in(wo); text, busy = c.load(saved); fc = c.take_feed(); c.hud()
    while busy:
        text, busy = c.handle(""); fc += c.take_feed(); c.hud()
    sb, sc = state(b), state(c)
    bad = [k for k in sb if sb[k] != sc[k]]
    tb = [f.get("text") for f in fb]; tc = [f.get("text") for f in fc]
    same_feed = tb == tc
    if not same_feed:
        i = next((i for i, (x, y) in enumerate(zip(tb, tc)) if x != y), min(len(tb), len(tc)))
        print(f"  first difference at line {i} of {len(tb)}/{len(tc)}:", (tb[i] if i < len(tb) else None), "|", (tc[i] if i < len(tc) else None))
    print(f"life 2 ({'grandchild' if gc else 'the world left behind'}): Mira to {sd['age']}, {len(sd['inputs'])} inputs, "
          f"earlier={sd['setup'].get('earlier', {}).get('name')}; loaded: state {'same' if not bad else 'DIFFERS ' + str(bad)}, "
          f"feed {'same' if same_feed else 'DIFFERS'} ({len(tb)} lines)")
    ok = ok and not bad and same_feed
    c2 = C.Console(); c2.load(saved)
    print("  loaded without the world:", c2.mode, "|", (c2.note or "")[:80])
print("saveload_world:", "PASS" if ok else "FAIL")
