"""Emigration and return in the game (W35-3, spec 5 §5): a life with the world on is sent abroad at 25 and home at 31
(the engine's own WorldLink.emigrate and return_home, as the immigrant and returned migrant titles do), and the game
must tell both moves, show the society, status and language in the panel, read the neighbour's news from the arrival
on, give its places and figures names of their own, and keep every place name in one country distinct.
Run: python3 test/abroad_check.py [seed]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import game
import worldview as V

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
fails = []
def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        fails.append(what)

g = game.Game(name="Lale", seed=seed, **{k: v for k, v in game.PRESETS["1"].items() if k not in ("title", "blurb")})
feed = []
def play(to):
    n = 0
    while not g.over and g.age() < to and n < 5000:
        n += 1; st = g.advance()
        if st == "checkpoint": g.decide(None)
        feed.extend(g.feed); g.feed = []
play(25)
WL = g.loc.get("WL")
check(WL is not None, "the world is on")
if WL is None:
    sys.exit(1)
home_names = {V.place_name(g.wv.seed, l) for l in range(15)}
check(len(home_names) == 15, "the home country's 15 places have 15 names")
wd0 = g.world_source(g.t)
n_home = len(wd0[1])
loc_new = WL.emigrate(0)
check(loc_new is not None and int(WL.PP.soc[0]) != int(WL.PP.soc_home[0]), "the engine moved the life abroad")
play(31)
moves = [f["text"] for f in feed if f.get("tag") == "move"]
abroad = [m for m in moves if "moves abroad" in m]
check(len(abroad) == 1, "the move abroad is told once: " + (abroad[0][:120] if abroad else str(moves[-2:])))
wd = g.world_source(g.t)
p = g.wv.panel(wd[0], wd[1], g.age())
pl = p.get("place") or {}
check(pl.get("abroad") and pl.get("society") and pl.get("status") and pl.get("language"),
      f"panel abroad: {pl.get('name')} in {pl.get('society')}, {pl.get('status')}, language {pl.get('language')}")
check(pl.get("name") not in home_names, "the town abroad has a name of its own")
new = wd[1][n_home:]
check(all(r.get("locality") is None or r["locality"] >= V.LOC_SOC for r in new), f"news after the move is the new country's ({len(new)} entries)")
figs = [f["name"] for f in p.get("figures", [])]
check(len(figs) == len(set(figs)), f"the new country's figures have distinct names ({len(figs)})")
WL.return_home(0)
play(34)
home = [f["text"] for f in feed if f.get("tag") == "move" and "comes home" in f["text"]]
check(len(home) == 1, "the return is told: " + (home[0][:120] if home else "none"))
wd = g.world_source(g.t)
p = g.wv.panel(wd[0], wd[1], g.age())
check(not (p.get("place") or {}).get("abroad"), "the panel is home again: " + str((p.get("place") or {}).get("name")))
check(g.over or g.age() >= 33.9, f"the life runs on to {g.age():.1f}")
print("abroad check:", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)
