"""v25 land row (GAME land_row): the game's land words against the Engine's land keys (other-shapes.md sections 4 and
6) and land.json, before the Engine pins them: land.json from the shared folder (or --land PATH), stand-in keys put in
at a pause. Exit 0 when every row holds; once the Engine pins sphere_data.LAND, it is read from there.

    python3 -B test/land_check.py [--land PATH]

    LD1  the land line names three stretches by the town's kind, with health and wildness words from land.json's
         thresholds, the last hazard and how long ago, and the harvest; no number
    LD2  held ways never exceed three, each with its land.json name and three steps
    LD3  each held way's next step is the one after its step, with its usual years in words
    LD4  a bridge shows held only when both its ways are held (or the Engine holds it), and as a door naming the other
         way when one is
    LD5  the company at a land moment in words"""
import json, os, re, sys
os.environ["CHROMA_GAME"] = json.dumps({"land_row": True})
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
os.chdir(os.path.dirname(HERE))
import pinned; pinned.ensure()
import random; random.seed(9)
from console import Console
import game_land

a = sys.argv[1:]
path = a[a.index("--land") + 1] if "--land" in a else "/mnt/project-files/chroma-world/spheres/data/land.json"
if game_land.LAND is None:
    game_land.LAND = json.load(open(path))
D = game_land.LAND
c = Console()
for line in ["", "1", "Ari"]:
    t, b = c.handle(line)
    while b:
        t, b = c.handle("")
while c.g.pending is None:
    t, b = c.handle("")
    while b:
        t, b = c.handle("")
g = c.g; loc = g.loc; ok = []
age = g.age()
place = dict(kind="market_town", land=[dict(stretch="field", health=0.8, wild=0.2), dict(stretch="wood", health=0.4, wild=0.7),
                                       dict(stretch="water", health=0.55, wild=0.35)],
             land_hazard=dict(kind="flood", age=2.2), harvest="poor")
line = g.land_line(place)
ok.append(("LD1", line == "The farms are thriving and tamed; the common wood is worn and wild; the river meadows are fair and half-wild; "
                  "the flood came two years ago; the harvest was poor." and not re.search(r"\d", line)))
cat = {w["key"]: w for w in D["uses"]["ways"]["list"]}
br = D["uses"]["ways"]["bridges"][0]
loc["ways"] = [[dict(key=br["a"], step=1, step_since_age=age - 1), dict(key=br["b"], step=0, step_since_age=age),
                dict(key="allotment", step=3, step_since_age=age), dict(key="beekeeping", step=0, step_since_age=age)]]
V = g.land_ways()
ok.append(("LD2", len(V["ways"]) == 3 and all(len(w["steps"]) == 3 and w["name"] == cat[w["key"]]["name"] for w in V["ways"])))
w0 = V["ways"][0]
ok.append(("LD3", w0["next"] == cat[br["a"]]["ladder"][1].split(" (")[0] and w0["steps"][1]["clock"].startswith("usually")
           and V["ways"][2]["key"] == "allotment" and V["ways"][2]["next"] == ""))
held = [b for b in V["bridges"] if b["held"]]
loc["ways"] = [[dict(key=br["a"], step=1, step_since_age=age - 1)]]       # the Engine's form: bridges as dict(a, b, opens)
loc["bridges_open"] = [[dict(br)]]; loc["bridges_held"] = [[dict(br)]]
V2 = g.land_ways()
ok.append(("LD4", held and held[0]["opens"] == br["opens"]
           and all(b["need"] for b in V["bridges"] if not b["held"])
           and any(b["held"] and b["opens"] == br["opens"] for b in V2["bridges"])))
loc["company"] = [dict(kind="friend", cid=4)]
ok.append(("LD5", g.company_say(loc) == "with a friend"))
for k, v in ok:
    print(k, "holds" if v else "FAILS")
sys.exit(0 if all(v for _, v in ok) else 1)
