"""Check the browser's story markers: balanced in every feed line and checkpoint, gone from the terminal text.
   python3 test/markers.py [lives]"""
import sys, re, random, collections, json
sys.path.insert(0, __file__.rsplit("/test/", 1)[0])
from console import Console

TOK = re.compile(r"⟦([^⟧]*)⟧")


def check(s, where, kinds, bad):
    depth = 0
    for m in TOK.finditer(s):
        t = m.group(1)
        if t == "/":
            depth -= 1
            if depth < 0:
                bad.append((where, s)); return
        else:
            if ":" not in t:
                bad.append((where, s)); return
            kinds[t.split(":", 1)[0]] += 1
            depth += 1
    if depth != 0:
        bad.append((where, s))


lives = int(sys.argv[1]) if len(sys.argv) > 1 else 4
rnd = random.Random(11)
kinds = collections.Counter(); bad = []; leaks = 0; braces = 0; states = 0; size = 0
for trial in range(lives):
    c = Console(); c.handle("")
    pick = rnd.choice("1234567")
    # build your own: name, sex, setting, times, technology, world, society, means, faith, upbringing, start age, seed
    script = [pick, "T" + str(trial)] if pick != "7" else ["7", "T", "1", "1", "2", "2", "1", "WU", "2", "1", "BG", "0", ""]
    for x in script:
        c.handle(x)
    for _ in range(20):                      # setup steps added later take Enter for their default
        if c.mode != "custom":
            break
        c.handle("")
    assert c.g is not None, f"setup {pick} did not start a life (mode {c.mode}, note {getattr(c, 'note', '')!r})"
    n = 0
    while c.mode == "play" and n < 4000:
        n += 1
        if c.job is None and c.g.pending is not None:
            text, busy = c.handle(rnd.choice(["", "", str(rnd.choice(list(c.numbering) or [1]))]))
        elif rnd.random() < 0.03:            # v7: make a plan now and then (key p), or drop one
            text = ""
            for x in rnd.choice([["p", "1", "1", ""], ["p", "2", rnd.choice(["UR", "W", "G", "3"]), ""], ["p", "3", "5", "x"], ["p", "d1"], ["p", "x"]]):
                t_, busy = c.handle(x); text += t_
        else:
            text, busy = c.handle("" if rnd.random() < 0.8 else rnd.choice(["v", "l", "y", "i"]))
        if "⟦" in text:
            leaks += 1
        feed = c.take_feed(); hud = c.hud(); states += 1
        size = max(size, len(json.dumps(hud)))
        for it in feed:
            check(it.get("text", ""), it["tag"], kinds, bad)
            if re.search(r"\{\w+\}", it.get("text", "")):
                braces += 1; print("BRACE", it["text"][:200])
        cp = hud.get("cp")
        if cp:
            for k in ("scene", "extra", "thought"):
                check(cp[k], "cp." + k, kinds, bad)
            if cp.get("voice"):
                for x in [cp["voice"]["line"]] + cp["voice"]["asides"]:
                    check(x, "cp.voice", kinds, bad)
                    if re.search(r"\{\w+\}", x):
                        braces += 1; print("BRACE", x[:200])
        res = hud.get("res")
        if res:
            for x in [res["say"], res["text"]]:
                check(x, "res", kinds, bad)
                if re.search(r"\{\w+\}", x):
                    braces += 1; print("BRACE", x[:200])
    if c.g.over:
        check(c.g.review["epitaph"], "epitaph", kinds, bad)
    print(f"life {trial} preset {pick} steps {n} over {c.g.over}")
print("markers:", dict(kinds))
print("unbalanced:", len(bad), "terminal leaks:", leaks, "unfilled braces:", braces, "largest hud json:", size)
for w, s in bad[:5]:
    print(" BAD", w, s[:300])
