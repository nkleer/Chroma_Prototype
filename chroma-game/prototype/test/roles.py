"""Titles and perks in a played life (Emren 12:05): every title and perk line the story tells, with how the engine says it
came or went, and the status text at 30 and 50. Usage: python3 test/roles.py [seed]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from game import Game
from story import plain
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3
g = Game(name="Ari", seed=seed, world="questions")
shown = 0; st_at = {30, 50}
while not g.over:
    r = g.advance()
    if r == "checkpoint": g.decide(None)
    elif r == "resolved":
        rs = g.resolution
        if rs and rs.get("roles"): print("   resolution chips", [(x["word"], x["what"]) for x in rs["roles"]])
        g.resolution = None
    for f in g.feed[shown:]:
        if f["tag"] in ("role", "commitment"):
            print(f"{f['age']:5.1f} [{f['tag']}{'' if f['tag'] != 'role' else ': ' + f['how']}] {plain(f['text'])}")
    shown = len(g.feed)
    a = int(g.age())
    if a in st_at:
        st_at.discard(a); print("----\n" + g.status().split("resources")[1] + "\n----")
