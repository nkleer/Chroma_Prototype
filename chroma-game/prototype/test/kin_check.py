"""One family in three places (release checks, consistency): the story's people, the engine's family counts
(locals alive: parents, siblings, closest friend, grandparents, partner, children) and the outer world's cast must
agree on who is alive. Plays lives with the world on and compares the three every 5 years.
   python3 test/kin_check.py [lives] [to age]"""
import sys, collections
sys.path.insert(0, __file__.rsplit("/test/", 1)[0])
import game
lives = int(sys.argv[1]) if len(sys.argv) > 1 else 4
to = float(sys.argv[2]) if len(sys.argv) > 2 else 60
COL = dict(parent=0, sibling=1, grandparent=3, partner=4, child=5)
STORY = dict(parent=("mother", "father"), sibling=("sibling",), grandparent=("grandparent",), partner=("partner",), child=("child",))
bad = collections.Counter(); seen = 0; ex = []; waiting = 0
for seed in range(1, lives + 1):
    g = game.Game(name="Lale", seed=seed * 11, **{k: v for k, v in game.PRESETS["1"].items() if k not in ("title", "blurb")})
    nxt, n = 5.0, 0
    while not g.over and g.age() < to and n < 5000:
        n += 1; st = g.advance()
        if st == "checkpoint": g.decide(None)
        if g.age() >= nxt and g.loc is not None and "alive" in g.loc and st != "checkpoint":   # (mid-week at a choice,
                                                                                               # the week's family news is not in yet)
            nxt += 5; seen += 1
            al = g.loc["alive"][0]; wd = g.world_data()
            for r, c in COL.items():
                e_ = int(al[c])
                s_ = sum(1 for q in g.story.people if q["role"] in STORY[r] and q["alive"])
                w_ = sum(1 for p in wd[2] if r in p.get("roles", []) and p.get("alive")) if wd else None
                gap = getattr(g, "_kin_gap", {})
                if r in ("sibling", "grandparent") and s_ > e_ and (r not in gap or g.t - gap[r] < g.KIN_WAIT):
                    waiting += 1; continue      # a death in the world waits a few weeks for the engine's own record
                for side, other in (("story vs engine", s_), ("world vs engine", w_)):
                    if other is not None and other != e_:
                        bad[(r, side)] += 1
                        if sum(1 for x in ex if x[0] == (r, side)) < 3:
                            ex.append(((r, side), seed * 11, round(g.age()), "engine", e_, "story", s_, "world", w_))
    print(f"life seed {seed * 11}: to {g.age():.0f}", flush=True)
print("checks (every 5 years):", seen)
for k, v in sorted(bad.items()):
    print(f"  {k[0]:12s} {k[1]:16s} {v} of {seen}")
print("examples ((role, side), seed, age, engine, story, world), up to 3 each:")
for e in ex: print("  ", e)
print("deaths waiting for the engine's record at a check (not counted):", waiting)
game_side = {k: v for k, v in bad.items() if k[1] == "story vs engine"}
print("Engine side (world cast vs engine counts; chroma-game/engine-requirements.md §5):",
      {k[0]: v for k, v in bad.items() if k[1] == "world vs engine"} or "none")
print("kin check (story vs engine):", "PASS" if not game_side else "FAIL")
