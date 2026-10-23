"""v25 clash moments on the card (GAME clash_card): the game's banner and option kinds against the Engine's S["clash"]
and L["CLASH_TAG"] (contracts.md section 3), before the Engine hands them over: stand-ins put in at a pause, the card
rebuilt and read the way the page reads it. Exit 0 when every row holds.

    python3 -B test/clash_check.py

    CL1  a clash moment's card has its banner: the demand's sphere in the Library's words and what is at stake (an aim,
         a need), and no colour named
    CL2  each option the Engine tags carries its kind (confront, give_in, leave, own_scene, bridge) to the page; the rest
         carry none
    CL3  a moment the Engine does not tag, or a week with no clash, has no banner"""
import json, os, sys
os.environ["CHROMA_GAME"] = json.dumps({"clash_card": True})
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
os.chdir(os.path.dirname(HERE))
import pinned; pinned.ensure()
import random; random.seed(5)
import numpy as np
from console import Console

c = Console()
for line in ["", "1", "Ari"]:
    t, b = c.handle(line)
    while b:
        t, b = c.handle("")
while c.g.pending is None:
    t, b = c.handle("")
    while b:
        t, b = c.handle("")
g = c.g; loc = g.loc; cp = g.pending; s = cp["s"]; ok = []
ks = sorted(cp["by_idx"])
tags = np.full((len(g.L["names"]), max(ks) + 1), -1)
tags[s, ks[0]] = 0
if len(ks) > 1:
    tags[s, ks[1]] = 4
g.L["CLASH_TAG"] = tags
loc["clash"] = [dict(id=3, demand=11, spheres=["faith"], holders=[], stakes=dict(needs=["autonomy"], aims=[]), options=["confront", "bridge"],
                     give_in_as=None)]
cl = g.clash_card(loc, s)
ok.append(("CL1", cl is not None and cl["spheres"] == ["Faith and rites"] and cl["stakes"] == ["room to choose"]
           and not any(w in json.dumps(cl).lower() for w in ("white", "blue", "black", "red", "green"))))
cp["clash_card"] = cl
for o in cp["options"]:
    if o["idx"] in cl["kinds"]:
        o["clash_kind"] = cl["kinds"][o["idx"]]
h = g.cp_hud(c.numbering)
kinds = {o.get("clash_kind") for o in h["options"]}
ok.append(("CL2", h.get("clash_card") == cl and kinds == ({"confront", "bridge", None} if len(ks) > 2 else {"confront", "bridge"} if len(ks) > 1 else {"confront"})))
other = next((x for x in range(len(g.L["names"])) if x != s), None)
loc["clash"] = [None]
ok.append(("CL3", g.clash_card(loc, s) is None and (other is None or g.clash_card(dict(loc, clash=[dict(id=1)]), other) is None)))
for k, v in ok:
    print(k, "holds" if v else "FAILS")
sys.exit(0 if all(v for _, v in ok) else 1)
