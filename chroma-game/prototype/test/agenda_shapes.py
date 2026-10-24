"""v25 agenda against the Engine's contract (chroma-engine/notes/v25/contracts.md section 6) before the Engine has it:
stand-ins for foresee.agenda, review, apply_review, preview, set_pace and set_priority in the contract's shapes, and the
game's views, terminal and console commands driven through them. Exit 0 when every row holds. When the Engine's own
functions land, test/agenda_check.py plays real lives with them.

    python3 -B test/agenda_shapes.py [hud.json]     (writes the hud with the stand-ins, for the page's render test)

    AS1  the agenda reads the full shape: items, capacity in words, forks, a review for the linked group
    AS2  a preview before taking up an aim: what it takes, costs and competes with, its deadline, unknowns, the way back
    AS3  the review's answers reach apply_review once, in the contract's shape; a fork left out stays waiting
    AS4  pace and priority reach set_pace and set_priority; a wrong pace is refused in words
    AS5  a save (version 11) replays the same agenda acts in the same order, at the same week
    AS6  a fork card: the fork put this week on its own moment, its aims, why and preview; Enter (or a light steer) on
         it answers "later", never the character's pick; a why given as a Library WHY_NOW key reads as its line"""
import json, os, sys
import numpy as np
os.environ["CHROMA_GAME"] = json.dumps({"agenda": True, "aim_forks": "every"})
os.environ["CHROMA_ENGINE"] = json.dumps({"aims_v2": False})   # the stand-ins below are the Engine here, not aims v2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
os.chdir(os.path.dirname(HERE))
import pinned; pinned.ensure()
import random; random.seed(1)
from console import Console
import game_base
from game_agenda import AL
F = game_base.F
CAP = {"time": dict(have=20, committed=24, items=[0, 1, "work"]), "money": dict(have=1000, committed=300, items=[0]),
       "energy": dict(have=1, committed=0.5, items=[0])}
PV = dict(needs=["a club's membership"], cost=dict(entry=150, money=(200, 400)), hours=(5, 7), overlaps=[1, "ties"],
          window=dict(opens=30, closes=33), unknown=["whether a club takes them", "how far they get"], exit=dict(say="they can pause; the fee is not returned"))
calls = []
def agenda(S, n):
    return dict(items=[dict(slot=0, aim="to master chess", field="chess", face="UB", importance=0.8, why_now="a club opened nearby",
                            state="pursuing", priority=1, step=dict(i=2, of=5, say="a rated player", next_say="a tournament winner"),
                            progress=dict(frac=0.4, effort_years=1.5, years=(3, 2, 6)), lean=0.5, pending=["f1"],
                            bottleneck=dict(res="time", shared_with=[1]), earned=[dict(name="a club player", source="worked for")],
                            potential=[dict(name="Known", step="a master")]),
                       dict(slot=1, aim="a community garden", face="G", importance=0.4, state="reduced", priority=2,
                            step=dict(i=1, of=3), pending=["f2"])],
                capacity=CAP, forks=[dict(id="f1", slot=0, kind="pay", made_at_age=31, deadline_age=32.5, urgency=0.8, group=1, blocks="evenings"),
                                     dict(id="f2", slot=1, kind="take", made_at_age=31, urgency=0.3, group=1, blocks="evenings")])
def review(S, n, group):
    calls.append(("review", group))
    return dict(group=group, why="both want the same evenings", capacity=CAP,
                forks=[dict(id="f1", slot=0, kind="pay", why="the club's season starts", deadline_age=32.5, preview=PV,
                            options=[dict(key="go", say="Pay and go on"), dict(key="wait", say="Wait a year")]),
                       dict(id="f2", slot=1, kind="take", why="a plot came free", preview=dict(hours=2, overlaps=[0]),
                            options=[dict(key="take", say="Take the plot"), dict(key="leave", say="Leave it")])],
                combos=[dict(choices=dict(f1="go", f2="take"), capacity={"time": dict(have=20, committed=30)}, slower=[1]),
                        dict(choices=dict(f1="wait", f2="take"), capacity={"time": dict(have=20, committed=12)}, slower=[])])
def apply_review(S, n, a):
    calls.append(("apply", a)); return agenda(S, n)
def preview(S, n, aim, step=None):
    return PV
def set_pace(S, n, slot, st):
    calls.append(("pace", slot, st)); return agenda(S, n)
def set_priority(S, n, slot, r):
    calls.append(("prio", slot, r)); return agenda(S, n)
for f in (agenda, review, apply_review, preview, set_pace, set_priority):
    setattr(F, f.__name__, f)
c = Console()
for line in ["", "1", "Ari"]:
    t, b = c.handle(line)
    while b:
        t, b = c.handle("")
while c.g.pending is None:
    t, b = c.handle("")
    while b:
        t, b = c.handle("")
h = c.g.hud()
A, ok = h["agenda"], []
acts = lambda: [x for x in calls if x[0] != "review"]
ok.append(("AS1", A["full"] and len(A["items"]) == 2 and {c_["load"] for c_ in A["capacity"]} == {"stretched", "room to spare"}
           and list(A["reviews"]) == ["1"] and A["reviews"]["1"]["combos"][0]["slower"] == ["a community garden"]
           and "nan" not in c.handle("j")[0].lower()))
pv = h["aim_choices"][0]["preview"]
ok.append(("AS2", pv["hours"] == "about two evenings a week" and pv["overlaps"] == ["a community garden", "time with the people close to them"]
           and pv["window"].endswith("closes at 33") and len(pv["unknown"]) == 2 and pv["exit"].startswith("they can pause")))
c.handle("ja f1=wait s1=paused")
a1 = acts()[-1]
c.handle('agenda apply {"choices": {"f2": "take"}, "set": {}}')
a2 = acts()[-1]
ok.append(("AS3", a1 == ("apply", {"choices": {"f1": "wait"}, "set": {1: "paused"}}) and a2 == ("apply", {"choices": {"f2": "take"}, "set": {}})
           and sum(1 for x in calls if x[0] == "apply") == 2))
c.handle("jp0 paused"); p1 = acts()[-1]
c.handle("jr1 1"); p2 = acts()[-1]
ok.append(("AS4", p1 == ("pace", 0, "paused") and p2 == ("prio", 1, 1) and c.handle("jp0 fast")[0] == "No such pace."))
g = c.g; s = g.pending["s"]; loc = g.loc
na = len(g.L["names"])
L_was = {k_: g.L[k_] for k_ in ("AIM_FORK", "AIM_TAG", "AIM_NAMES") if k_ in g.L}
g.L["AIM_FORK"] = np.full(na, -1); g.L["AIM_FORK"][s] = 0
g.L["AIM_TAG"] = np.full((na, 8), -1); g.L["AIM_TAG"][s, 2] = 3; g.L["AIM_NAMES"] = dict(tags=("go", "pay", "drop", "later"))
loc["aim_fork"] = np.array([7]); loc["aim_forks"] = [[dict(id=7, aims=[0], kind="pay", why="the club's season starts", preview=PV, options=[], grouped=True, group=1)]]
card = g.fork_card(loc, g.fork_now(loc, s), s)
seen = []
real_decide = g.decide
g.decide = lambda k=None, **kw: seen.append(k)
g.pending["fork"] = card
c.handle(""); c.job = None; c.handle("~w")
g.decide = real_decide; c.job = None; del g.pending["fork"]
loc["aim_forks"][0][0]["why"] = "window"                  # a Library WHY_NOW key: its line, with the preview's facts
a2_was = loc.get("aim2"); loc["aim2"] = [[dict(field="chess", say="a place in the club's first team")]]
why_w = g.fork_card(loc, 7, s)["why"]; loc.pop("aim2") if a2_was is None else loc.__setitem__("aim2", a2_was)
for k_ in ("AIM_FORK", "AIM_TAG", "AIM_NAMES"):
    del g.L[k_]
g.L.update(L_was)
del loc["aim_fork"], loc["aim_forks"]
ok.append(("AS6", card["aims"] == ["to master chess"] and card["later"] == 2 and card["preview"]["hours"] == "about two evenings a week"
           and card["group"] == "1" and seen == [2, 2] and card["why"] == "the club's season starts"
           and (AL is None or f"closes when {g.name} is about 33" in why_w)))
sv = json.loads(c.save()); t0 = c.g.t
n0 = len(acts()); mine = acts()[:]
c2 = Console(); t, b = c2.load(json.dumps(sv))
while b:
    t, b = c2.handle("")
ok.append(("AS5", sv["version"] == 11 and acts()[n0:] == [x for x in mine if x[0] != "preview"][-len(acts()[n0:]):] and len(acts()) - n0 == 4
           and c2.g.t == t0))
for k, v in ok:
    print(k, "holds" if v else "FAILS")
if sys.argv[1:]:
    json.dump(h, open(sys.argv[1], "w"), default=str)
sys.exit(0 if all(v for _, v in ok) else 1)
