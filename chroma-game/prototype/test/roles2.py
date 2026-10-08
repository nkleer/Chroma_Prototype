"""Titles volume 2 in the game (engine hand-off titles-v2-handoff.md): profiles, facets, the engine's loss reasons and the
Library's base rate. Plays lives until a facet is held and prints the HUD's titles with their facets and profiles, then
tells a profile change and each loss reason through the story. Usage: python3 test/roles2.py [seed]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from game import Game, role_info, base_word
from story import plain, LOSS_LEAD
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3
facet_seen = prof_seen = base_seen = 0
for sd in range(seed, seed + 6):
    g = Game(name="Ari", seed=sd, world="questions")
    while not g.over and not (facet_seen and prof_seen >= 2 and base_seen):
        r = g.advance()
        if r == "checkpoint":
            if not base_seen:
                cp = g.cp_hud({i: i for i in range(20)})
                b = [(o["label"], o.get("base")) for o in cp["options"]] if cp else []
                if any(x for _, x in b):
                    base_seen = 1; print("base rates:", [(l[:40], x, base_word(x)) for l, x in b[:4]])
            g.decide(None)
        elif r == "resolved":
            g.resolution = None
        R = g.roles()
        if R:
            for k, xs in R["titles"].items():
                for x in xs:
                    if x.get("facets") and facet_seen < 3:
                        facet_seen += 1
                        print(f"{g.age():5.1f} HUD {k}: {x['name']} + facets {[f['say'] for f in x['facets']]}")
                    if x.get("profile") and prof_seen < 2:
                        prof_seen += 1; print(f"{g.age():5.1f} HUD {k}: {x['name']} held as: {x['profile']}")
    for f in g.feed:
        if f["tag"] == "role" and (f.get("what") == "reshaped" or f.get("how") in LOSS_LEAD):
            print(f"{f['age']:5.1f} [{f['how'][:40]}] {plain(f['text'])}")
GR = g.L["ROLES"]; st = g.story
doc = role_info(GR, GR["ID"]["physician"]); car = role_info(GR, GR["ID"][next(n for n in GR["names"][GR["NT"]:] if n.lower().startswith("car"))])
print(plain(st.title_line(dict(what="reshaped", how=GR["pwords"][doc["i"]][1]), doc)))
print(plain(st.title_line(dict(what="reshaped", how="in other ways"), doc)))
for w in LOSS_LEAD:
    print(plain(st.title_line(dict(what="lost", how=w), car)))
