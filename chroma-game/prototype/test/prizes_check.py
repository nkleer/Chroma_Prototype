"""v25 what this world prizes (GAME prizes): the game's words against the Engine's S["prizes"] (other-shapes.md section
6), before the Engine hands it over: stand-in rows put in the life's locals at a pause, then the world page, the status
lines and the town rows read. Exit 0 when every row holds; once the Engine's tilt_world lands, run it on a real life
with --real (the rows then check the Engine's own S["prizes"]).

    python3 -B test/prizes_check.py [--real]

    PZ1  every sphere in S["prizes"] has a row, in the Library's words (no colour named), on the world page too
    PZ2  the words follow the data: a cell at 1.15 or more counts for more, at .87 or less for less, else nothing;
         the person's climb reads easier, about even or steeper the way their colours meet the row
    PZ3  a world with every cell at 1 says "every way counts alike here"
    PZ4  the moves are listed with their sphere's name and cause"""
import json, os, sys
os.environ["CHROMA_GAME"] = json.dumps({"prizes": True})
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
os.chdir(os.path.dirname(HERE))
import pinned; pinned.ensure()
import random; random.seed(3)
import numpy as np
from console import Console

COLOUR_WORDS = ("white", "blue", "black", "red", "green")
c = Console()
for line in ["", "1", "Ari"]:
    t, b = c.handle(line)
    while b:
        t, b = c.handle("")
while c.g.pending is None:
    t, b = c.handle("")
    while b:
        t, b = c.handle("")
g, loc, ok = c.g, c.g.loc, []
real = "--real" in sys.argv
if not real:
    loc["w"] = np.array([[0.6, 0.1, 0.1, 0.1, 0.1]])
    loc["prizes"] = [dict(rule=[1.3, 1.2, 1.0, 0.7, 0.8], prod=[0.8, 1.0, 1.0, 1.25, 1.0], arts=[1.0] * 5, care=[1.1, 1.0, 1.0, 0.95, 0.95])]
    loc["prizes_moves"] = [[dict(sphere="rule", age=12.4, cause="a reform of the courts")]]
V = g.prizes_view()
P = g._prizes_raw(loc)
ok.append(("PZ1", V is not None and {x["sphere"] for x in V["rows"]} == set(P)
           and not any(w in json.dumps(V).lower() for w in COLOUR_WORDS)))
good = True
w = np.asarray(loc["w"][0], float); w = w / w.sum()
for x in V["rows"]:
    r = np.asarray(P[x["sphere"]], float)
    good &= len(x["more"]) == min(2, int((r >= 1.15).sum())) and len(x["less"]) == min(2, int((r <= 0.87).sum()))
    gw = float(w @ r)
    good &= x["for_me"] == ("easier" if gw >= 1.08 else "steeper" if gw <= 0.93 else "about even")
if not real:
    rows = {x["sphere"]: x for x in V["rows"]}
    good &= rows["rule"]["for_me"] == "easier" and rows["prod"]["for_me"] == "steeper" and rows["arts"]["for_me"] == "about even"
    good &= rows["rule"]["more_c"] == "WU" and not rows["care"]["more"] and not rows["care"]["less"]
    good &= any("count for more" in s for s in g.prizes_lines()) and bool((g.world_panel() or {}).get("prizes"))
ok.append(("PZ2", bool(good)))
if not real:
    loc["prizes"] = [{s: [1.0] * 5 for s in P}]
    ok.append(("PZ3", g.prizes_view()["even"] and g.prizes_lines() == ["what it prizes: every way counts alike here"]))
    loc["prizes"] = [P]
    ok.append(("PZ4", V["moves"] == [dict(sphere="rule", name="Rule and law", age=12.4, cause="a reform of the courts")]))
for k, v in ok:
    print(k, "holds" if v else "FAILS")
sys.exit(0 if all(v for _, v in ok) else 1)
