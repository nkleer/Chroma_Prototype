"""The held version on the Library's next batch (staged, not live): seasons of change, {title}, own death, the new moments.
python3 test/next2_check.py [lives] [push share]"""
import sys, os, random, json, time, collections, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from console import Console
n_lives = int(sys.argv[1]) if len(sys.argv) > 1 else 3
push = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 21)
for trial in range(n_lives):
    t0 = time.time(); c = Console(); c.handle("")
    key = rnd.choice(["1", "2", "3", "4"]); c.handle(key); c.handle("N" + str(trial))
    errs = []; seasons = collections.Counter(); turning = 0; seamo = 0; sea_titles = []; title_lines = []; unfilled = []; cps = 0
    def send(x):
        text, busy = c.handle(x)
        while busy:
            t2, busy = c.handle(""); text += t2
        if "[error" in text:
            errs.append(text[-300:])
        for m in re.findall(r"[^\n]*\{[a-z_]+\}[^\n]*", text):
            unfilled.append(m[:160])
    steps = 0
    while c.mode == "play" and steps < 4000:
        steps += 1
        h = c.hud()
        sx = (h.get("life") or {}).get("season_x")
        if sx:
            seasons[(sx["kind"], sx["into"], sx["step"])] += 1
        cp = h.get("cp")
        if cp:
            cps += 1
            if cp.get("season") and cp["season"].get("this_week"):
                seamo += 1; sea_titles.append((cp["season"]["into"], cp["season"]["step"], cp.get("title", "")[:50]))
                if cp["season"].get("transform"):
                    turning += 1
            for o in cp["options"]:
                if "{" in o["label"]:
                    unfilled.append("label: " + o["label"])
        if c.g.pending is not None and c.numbering and rnd.random() < push:
            send(str(rnd.choice(list(c.numbering))))
        else:
            send("")
    for f in c.g.feed if hasattr(c.g, "feed") else []:
        pass
    r = c.g.review
    print(f"life {trial} preset {key} age {r['age']} died {r.get('died')} cps {cps} errors {len(errs)} unfilled {len(unfilled)} secs {time.time() - t0:.0f}")
    print("   seasons:", sorted({(k, i) for k, i, s in seasons}), "season moments:", seamo, "turning points:", turning)
    for st in sea_titles[:8]:
        print("     ", st)
    print("   reading:", r["reading"]["words"], {k: round(r[k], 2) for k in ("fulfilment", "serenity", "integrity")})
    for e in errs[:3]:
        print("   ERROR", e)
    for u in unfilled[:5]:
        print("   UNFILLED", u)
