"""Sex at birth, own gender and the role the world expects, on the game's side (checklist N1d, release C-G1).
Checks: setup step 2 (title, four choices, the hover), intersex from setup reaching the game (and the engine once it
takes it), parents named by sex, the sheet's "who they are" block showing a trait only from the week it is found
(engine fields injected where the engine does not give them yet), two-word titles in the character's own words, and a
new name that keeps the life's id.   python3 test/identity_check.py [lives]"""
import sys, os, json
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, here); os.chdir(here)
import numpy as np
from console import Console, STEP_FORM, CUSTOM_STEPS
import game, story
LIVES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
bad = []
def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok: bad.append(what)

f = STEP_FORM["sex"]
check(f[1] == "Sex at birth", "step 2 title is 'Sex at birth'")
check(len(f[3]) == 4 and [c[1] for c in f[3]][:3] == ["Female", "Male", "Intersex"], "four choices: female, male, intersex, chance")
check(f[4].startswith("Three things, kept apart."), "the step's hover text")
check([s[0] for s in CUSTOM_STEPS].index("sex") == 1, "sex is step 2 of the custom setup")

for life in range(LIVES):
    c = Console(); c.handle("")
    k = [m["k"] for m in c.hud()["menu"] if "build" in m.get("title", "").lower()]
    c.handle(k[0] if k else "7")
    c.handle("")                                     # name: drawn once the sex is known
    c.handle("3" if life == 0 else str(1 + life % 2))
    while c.mode == "custom":
        c.handle("")
    g = c.g
    if life == 0:
        check(g.gender_view()["rows"][0][:2] == ["Born", "intersex"], "intersex before the first week: Born intersex on the sheet")
        text, busy = c.handle("")                    # the first week: the engine draws how they are raised
        while busy:
            text, busy = c.handle("")
        check(g.born_intersex and g.sex_now() in ("female", "male"), "intersex from setup reaches the game, raised as a girl or a boy")
        if game.ENGINE_INTERSEX:
            check(bool(g._idv(g.loc, "intersex")), "intersex reaches the engine")
    n = 0
    while c.mode == "play" and g.age() < 40 and n < 4000:
        n += 1; c.handle("")
    h = c.hud()["life"]
    gv = g.gender_view()
    found = {k: g._found(g.loc, k) for k in ("gender", "attr", "ace")}
    labels = [r[0] for r in gv["rows"]]
    if not found["gender"]:
        check("Knows themselves as" not in labels and "Knows themselves as" not in json.dumps(h.get("who")), f"life {life}: own gender not on the sheet before it is found")
    if not found["attr"] and not found["ace"]:
        check("Drawn to" not in labels, f"life {life}: attraction not on the sheet before it is found")
    check(labels[0] == "Born" and labels[-1] == "What their world expects", f"life {life}: the block opens with Born and ends with the world's expectation")
    fam = [(p["ref"], p["name"]) for p in g.story.people[:8]]
    check(not [1 for ref, nm in fam if ("mother" in ref and nm in story.NAMES_M) or ("father" in ref and nm in story.NAMES_F)], f"life {life}: parents named by their sex")

# a trait found later stays hidden now; found now, it shows; named, the words follow
loc = dict(g.loc); loc["gender_self"] = np.array([2]); loc["found_gender"] = np.array([g.t + 10])
check("Knows themselves as" not in [r[0] for r in g.gender_view(loc)["rows"]], "own gender found in ten weeks: hidden this week")
loc["found_gender"] = np.array([g.t])
gv = g.gender_view(loc)
kw = dict((r[0], r[1]) for r in gv["rows"]).get("Knows themselves as", "")
told = g._mark(loc, "came out")
check(kw.startswith("neither, or both") and (("told a few" in kw) if told else ("known only to them" in kw)), f"found this week: shown ({kw})")
check(g.gword("wife or husband", "f") == "wife" and g.gword("mother or father", "m") == "father" and g.gword("girlfriend or boyfriend", "x") == "partner", "two-word titles: wife, father, partner")
lid = g.life_id(); old = g.name
check(g.rename("Wren") and g.name == "Wren" and g.story.name == "Wren" and g.life_id() == lid, "a new name keeps the life's id")
check(g.history.get("names", [])[-1][1:] == (old, "Wren"), "the new name is in the history")
check("{seen_as}" not in g.story.fill("The {seen_as} at the door."), "the {seen_as} slot fills")
print("FAILED:", bad) if bad else print("identity checks: all passed")
sys.exit(1 if bad else 0)
