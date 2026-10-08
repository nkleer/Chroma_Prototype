"""How the character feels about the options they could be pushed to (Emren 09:25, point 7): share of each word,
by age, and how often a moment reads reluctant or against for most of the options they see.
Usage: python3 test/acceptance.py FIRST_SEED LAST_SEED [world, default questions: the engine's mild default] (own picks only)."""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, '.')
from game import Game, accept_word, ACCEPT
c = collections.Counter(); cu = collections.Counter(); n = 0; lop = 0; m4 = 0; byage = collections.defaultdict(collections.Counter)
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    g = Game(name="T", seed=seed, world=(sys.argv[3] if len(sys.argv) > 3 else "questions"))
    while not g.over:
        r = g.advance()
        if r == "checkpoint":
            cp = g.pending; ws = []
            for o in cp["options"]:
                if o["idx"] == cp["own"] or o["colors"] == "-": continue
                w = o.get("acc") or accept_word(o["rel"])
                if o["status"] == "considered":
                    c[w] += 1; ws.append(w); byage[min(int(cp["age"] // 20), 3) * 20][w] += 1
                else:
                    cu[w] += 1
            if len(ws) >= 4:
                m4 += 1; lop += sum(w in ACCEPT[2:] for w in ws) >= 0.7 * len(ws)
            g.decide(None); n += 1
        elif r == "resolved": g.resolution = None
share = lambda cc: {k: round(cc[k] / max(sum(cc.values()), 1), 2) for k in ACCEPT}
print("moments", n, "options they see", share(c), "others", share(cu))
print("moments where 70%+ of what they see reads reluctant or against:", round(lop / max(m4, 1), 2))
for a in sorted(byage): print(f"  age {a}+", share(byage[a]))
