"""Game's methods for "Because of you, and meanwhile" (chroma-ideas/next-table-2026-10-19/plan.md section 1; Emren
10-19 "Clarity first": v23.2), behind GAME because. Words only: nothing here draws, so with it on every step plays as
with it off.

Part of class Game (game.py), which inherits BecauseMixin. What it reads, from the Engine's played-life key need_why:
- loc["nw"][0]: this week's need moves by source, shape (len(E.NSOURCES), needs), from the start of the week to the
  pause, summing exactly to the week's change. Copied at the choose pause (cp["nw0"]) and diffed at the end pause, it
  splits what moved after the pick by source.
- loc["nw_imp"][0]: this week's silent setback, an index into the Library's IMPOSITIONS (-1 none).
- loc["nw_imp_cause"][0], when the Engine has it (v24, N3): where the setback came from, an index into E.IMP_CAUSES
  (-1 none); the told line names it.
"Because of you" is the act itself and what the game did at the pause (a push's cost); "meanwhile" is every other
source, each line with its biggest cause. Every need change of a point or more lands in at least one group."""
import numpy as np
from game_base import E, GAME
from story_base import NEED_SAY

YOU = ("act", "player")                     # the sources that are the pick's own
SRC_SAY = dict(                             # "meanwhile": what moved it, as a short cause
    fade="as the weeks wore on", setback="a setback", outside="what happened around them", reading="how they took the news",
    loss="a loss", means="money and means", commitments="what they are committed to", titles="what they are",
    care="family looking after them", goals="a goal", people="people turning to them", age="their age",
)
SETBACK_SAY = {                             # the silent setbacks (the Library's IMPOSITIONS), told in a short line
    "a rule is imposed on you": "A new rule hems {N} in.",
    "an institution betrays its promise": "Something {N} counted on breaks its promise.",
    "you are lied to and misled": "{N} finds out they were misled.",
    "someone takes what you earned": "Someone takes what {N} earned.",
    "your community or habitat is damaged": "The place {N} belongs to is damaged.",
    "you are forbidden to see someone you love": "{N} is kept from someone they love.",
    "evidence you trusted is overturned": "Something {N} was sure of turns out wrong.",
    "you are made dependent on others": "{N} is left depending on others.",
    "your traditions are mocked or banned": "The ways {N} grew up with are mocked.",
    "lawlessness spreads around you": "Things grow lawless around {N}.",
}
CAUSE_SAY = {                               # v24 N3: where a setback came from (E.IMP_CAUSES), after the told line's comma
    "family": "at home", "school": "at school", "work": "at work", "a partner": "through a partner",
    "friends": "among friends", "crime nearby": "with crime nearby", "a disaster": "after a disaster", "war": "in the war",
    "the authorities": "by order of the authorities", "the law failing": "as the law fails",
    "failing health": "as their health fails", "old age": "with old age", "word going round": "as word goes round",
    "a stranger": "through a stranger",
}
CAUSE_NONE = "and they cannot tell why"   # a setback whose cause the Engine did not give
SPLIT_MIN = 0.005                           # half a point: a part this small is not a line of its own
SETBACK_AGE = 12.0                          # silent setbacks are told from this age (a small child's are not theirs to read)


class BecauseMixin:
    def _because_on(self, loc):
        return GAME["because"] and loc is not None and "nw" in loc and loc["nw"][0] is not None

    def _nw(self, loc):
        return np.asarray(loc["nw"][0], float).copy() if self._because_on(loc) else None

    def _setback(self, loc):
        """This week's silent setback as (name, told line, cause), or None. The cause (v24) is E.IMP_CAUSES' name, or
        None when the Engine gives none; with no cause key at all the line is as before."""
        if not self._because_on(loc) or "nw_imp" not in loc:
            return None
        i = int(np.asarray(loc["nw_imp"][0]).ravel()[0])
        imp = getattr(E, "IMPOSITIONS", None)
        if i < 0 or imp is None or i >= len(imp):
            return None
        nm = imp[i][0]
        line = SETBACK_SAY.get(nm, "Something goes against {N}.")
        if "nw_imp_cause" not in loc or loc["nw_imp_cause"][0] is None:
            return nm, self.story.fill(line), None
        c = int(np.asarray(loc["nw_imp_cause"][0]).ravel()[0])
        cs = getattr(E, "IMP_CAUSES", None) or ()
        cause = cs[c] if 0 <= c < len(cs) else None
        say = CAUSE_SAY.get(cause, f"through {cause}") if cause else CAUSE_NONE
        return nm, self.story.fill(line[:-1] + ", " + say + "."), cause

    def _because(self, loc, cpw, needs):
        """The needs the pick's week moved, split into what the pick did and what else happened (each with its cause),
        and the week's silent setback. None when the record is off."""
        nw0 = cpw["cp"].get("nw0")
        if nw0 is None or not self._because_on(loc):
            return None
        d = self._nw(loc) - nw0                     # moves after the pick, by source and need
        src = list(E.NSOURCES)
        you_i = [src.index(s) for s in YOU if s in src]
        you, mw = [], []
        for x in needs:                             # the needs that moved a point or more (_needs_moved)
            j = E.NEEDS.index(x["need"])
            col = d[:, j]
            yd = float(col[you_i].sum()); md = float(x["delta"]) - yd   # a point or more in all: one part is half a point
            if abs(yd) < SPLIT_MIN:                 # a part too small for a line of its own goes to the other one,
                md = float(x["delta"])              # so the lines shown always add up to the change
            elif abs(md) < SPLIT_MIN:
                yd = float(x["delta"])
            if abs(yd) >= SPLIT_MIN:
                pl = abs(col[src.index("player")]) if "player" in src else 0.0
                you.append(dict(need=x["need"], delta=round(yd, 3), why="your push" if pl > abs(col[src.index("act")]) else "this choice"))
            if abs(md) >= SPLIT_MIN:
                ks = [k for k in np.argsort(-np.abs(col)) if src[k] not in YOU and col[k] * md > 0][:2]
                why = " and ".join(SRC_SAY.get(src[k], src[k]) for k in ks) or SRC_SAY["fade"]
                mw.append(dict(need=x["need"], delta=round(md, 3), why=why))
        sb = self._setback(loc)
        out = dict(you=you, meanwhile=mw)
        if sb:
            out["setback"] = dict(name=sb[0], line=sb[1])
            if sb[2]:
                out["setback"]["cause"] = sb[2]
        return out

    def because_line(self, sp):
        """The split as two short lines for the story and the console."""
        if not sp:
            return ""
        say = lambda xs: ", ".join(f"{NEED_SAY.get(x['need'], x['need'])} {x['delta'] * 100:+.0f} ({x['why']})" for x in xs)
        lines = []
        if sp["you"]:
            lines.append("Because of you: " + say(sp["you"]) + ".")
        if sp["meanwhile"]:
            lines.append("Meanwhile: " + say(sp["meanwhile"]) + ".")
        if sp.get("setback"):
            lines.append(sp["setback"]["line"])
        return "\n".join(lines)
