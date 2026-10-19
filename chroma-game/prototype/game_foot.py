"""Game's methods for v24 footprints (chroma-ideas/next-table-2026-10-19/plan.md section 3; Emren 10-19: "make them
stackable to understand whole picture easily"), behind GAME foot, with the Engine's foot_on. Words only: the Engine
gives the footprints their state; nothing here draws.

Part of class Game (game.py), which inherits FootMixin. What it reads, from the Engine's played-life keys:
- the week's events: dict(foot=dict(age, moment, label, worked, feet=[dict(kind, value, cid?)])) for each act that left
  footprints: kind person, place, means, mark, door or lesson; value the Library's words (footprint_names.py); cid the
  cast id for a person. Only what landed.
- loc["foot_open"][0]: the doors still waiting, [(kind, since_t)].
- foresee.marks_toward(S, n), when the Engine has it: the titles and perks a held mark counts toward, nearest first.
Shown as six stacks only (people, places, means, marks, doors, lessons), each a count and one plain line; after a
pick, at most one line per kind inside "Because of you"; marks only when they near a title or perk."""
from game_base import F, GAME
from worldview import person_name

try:
    import footprint_names as FN                # the Library's plain words (pinned next to the engine)
except ImportError:
    FN = None

KINDS = ("person", "place", "means", "mark", "door", "lesson")
STACK = dict(person="People", place="Places", means="Means", mark="Marks", door="Doors", lesson="Lessons")
ICON = dict(person="ci-footprint-people", place="ci-footprint-places", means="ci-footprint-means",
            mark="ci-footprint-marks", door="ci-footprint-doors", lesson="ci-footprint-lessons")
LINE_ITEMS = 3                                  # a stack's line names its newest few; the rest wait behind the hover
HOVER_ITEMS = 12


class FootMixin:
    def _foot_week(self, new):
        """This week's footprints, from the week's new events (the Engine's dict(foot=...) record of each act that left
        some), kept in history["foot"]; [] when off."""
        if not GAME["foot"]:
            return []
        out = [dict(age=round(ev["foot"]["age"], 1), kind=str(f["kind"]), value=str(f["value"]), who=int(f.get("cid", -1)),
                    sit=ev["foot"]["moment"]) for ev in new if "foot" in ev for f in ev["foot"]["feet"]]
        if out:
            self.history.setdefault("foot", []).extend(out)
        return out

    def _foot_word(self, x):
        """Plain words for one footprint; a person by name when the cast has one."""
        k, v = x["kind"], x["value"]
        w = FN.line(k, v) if FN is not None else v
        if k == "person" and x.get("who", -1) >= 0 and getattr(self, "wv", None) is not None:
            nm = person_name(self.wv.seed, x["who"], False, self.setting)
            w = (f"lost {nm} ({w[5:]})" if w.startswith("lost ") else f"{nm} ({w})") if nm else w
        return w

    def foot_lines(self, xs):
        """After a pick: at most one line per kind it touched, as [dict(kind, icon, line)]."""
        out = []
        for k in KINDS:
            ws = list(dict.fromkeys(self._foot_word(x) for x in xs if x["kind"] == k))
            if k == "mark" and ws and not self._marks_near():
                continue                        # a mark is told only when it nears a title or perk (Emren's condition)
            if ws:
                out.append(dict(kind=k, icon=ICON[k], line=f"{STACK[k]}: " + ", ".join(ws)))
        return out

    def _marks_near(self):
        """The titles and perks a held mark counts toward and not yet reached, nearest first (the Engine's view); [] when
        it has none."""
        f = getattr(F, "marks_toward", None)
        S = getattr(self, "loc", None)
        if f is None or S is None:
            return []
        try:
            return [m for m in f(S, 0) or [] if not m.get("done")]
        except (KeyError, TypeError):
            return []

    def foot_stacks(self):
        """The life so far as the six stacks: [dict(kind, name, icon, n, line, items)], items newest first for the hover;
        None when off."""
        if not GAME["foot"] or "foot" not in self.history:
            return None
        h = self.history["foot"]
        out, near = [], []
        for k in KINDS:
            xs = [x for x in reversed(h) if x["kind"] == k]
            items = [dict(age=x["age"], word=self._foot_word(x), sit=x["sit"]) for x in xs[:HOVER_ITEMS]]
            if k == "means":                     # which way each went, summed: no second meter
                tot = {}
                for x in xs:
                    res, sign = x["value"].rstrip(".0123456789+-"), x["value"][len(x["value"].rstrip(".0123456789+-")):]
                    try:
                        tot[res] = tot.get(res, 0.0) + float(sign)
                    except ValueError:
                        continue
                word = (lambda r: FN.MEANS.get(r, r)) if FN is not None else (lambda r: r)
                line = ", ".join(f"{word(r)} {'up' if v > 0 else 'down'}" for r, v in sorted(tot.items(), key=lambda kv: -abs(kv[1]))
                                 if abs(v) >= 0.005)
            elif k == "mark":                    # only when it nears a title or perk: "2 of 3 toward ..."
                near = self._marks_near()
                line = "; ".join(f"{m['have']} of {m['need']} toward {m['title']}" for m in near[:2])
            elif k == "door":                    # the doors still waiting, then the ones taken
                op = (self.loc or {}).get("foot_open") if getattr(self, "loc", None) is not None else None
                wait = [FN.line("door", d) if FN is not None else d for d, _ in ((op or [None])[0] or [])]
                line = ("waiting: " + ", ".join(wait[:LINE_ITEMS])) if wait else ", ".join(list(dict.fromkeys(i["word"] for i in items))[:LINE_ITEMS])
            else:
                line = ", ".join(list(dict.fromkeys(i["word"] for i in items))[:LINE_ITEMS])
            n = len(near) if k == "mark" else len(xs)   # marks count only those nearing a title or perk
            out.append(dict(kind=k, name=STACK[k], icon=ICON[k], n=n, line=line, items=items if n else []))
        return out
