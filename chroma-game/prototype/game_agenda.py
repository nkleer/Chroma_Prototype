"""Game's methods for the v25 agenda (Emren's decision file, chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md
section 5, decision #9: "a prominent, persistent frontend agenda showing importance, current step, progress, commitment
state, priorities, pending forks and actual bottlenecks. Allow inspection and adjustment. Distinguish potential rewards
from earned assets and explain their origins and uses"), behind GAME agenda. Words only: reading the agenda draws
nothing and costs no time, so with it on every step plays as with it off until the player adjusts something.

Part of class Game (game.py), which inherits AgendaMixin. What it reads, from the Engine's foresee.py:
- agenda(S, n), when the Engine has it (v25 aims, lane B): every held aim (no slot limit) with its importance, state,
  priority, step, progress and clock, the character's own lean, pending forks, its bottleneck, earned assets, potential
  rewards and upkeep; the shared capacity (one accounting for time, attention, energy, money, access and support); the
  unresolved forks with their deadlines and review groups.
- set_pace(S, n, slot, state), set_priority(S, n, slot, rank): the player's adjustments. These change the life.
- Without agenda (v24's engine), the agenda is read from aims(S, n): the aims, their steps and strength; no capacity,
  forks or bottlenecks, and the screen says so rather than inventing them.
The words for sizes are the game's (IMPORTANCE, STATE_SAY, LEAN, LOAD): never a number before a choice."""
import zlib

import numpy as np

from game_base import E, F, GAME
from game_words import clean

try:                                 # the Library's words for the agenda, previews and reviews (earth_aim_lines.py, v25)
    import earth_aim_lines as AL
except Exception:
    AL = None
IMPORTANCE = ((0.66, "central"), (0.33, "important"), (0.0, "in the background"))
STATE_SAY = dict(holding="held, not pursued", pursuing="pursued in full", reduced="pursued, less", keeping_up="kept up",
                 paused="paused", set_aside="set aside")
if AL is not None:                   # the Library's labels win ("going lightly" for reduced)
    STATE_SAY.update({k: v["label"] for k, v in AL.STATE_WORDS.items() if v.get("label")})
PACES = ("pursuing", "reduced", "keeping_up", "paused", "holding")       # what the player may set (set_aside: drop)
LEAN = ((0.33, "keen"), (-0.33, "of two minds"), (-1.01, "reluctant"))
LOAD = ((0.75, "room to spare"), (1.0, "full"), (1.2, "stretched"), (9e9, "overcommitted"))   # committed / have, up to
RESOURCES = ("time", "attention", "energy", "money", "access", "support")
RES_SAY = dict(time="Time", attention="Attention", energy="Energy", money="Money", access="Access", support="Support")
SHARE_SAY = ((0.6, "most get there"), (0.35, "about half get there"), (0.15, "few get there"), (0.0, "very few get there"))
MONEY_SAY = ((0.7, "more than they have spare"), (0.35, "most of what they have spare"), (0.1, "a fair part of what they have spare"),
             (0.0, "a little of what they have spare"))       # a cost / the free money of a year
OTHER_SAY = dict(work="work", care="the care they give", household="the household", ties="time with the people close to them",
                 essentials="what they need to live")


def _word(v, table):
    for cut, w in table:
        if v >= cut:
            return w
    return table[-1][1]


def hours_say(h):
    """Hours a week as evenings, a range when given (lo, hi): 'about two evenings a week'."""
    if h is None:
        return ""
    lo, hi = (h, h) if isinstance(h, (int, float)) else (float(h[0]), float(h[-1]))
    ev = lambda x: max(1, round(x / 3))
    w = ("one", "two", "three", "four", "five", "six", "seven")
    if hi < 1.5:
        return "an hour or so a week"
    if hi > 21:
        return "most of their free time"
    a, b = ev(lo), ev(hi)
    if a == b:
        return f"about {w[a - 1]} evening{'s' if a > 1 else ''} a week"
    return f"{w[a - 1]} to {w[b - 1]} evenings a week"


def money_say(m, have):
    """A money cost against the year's free money, in words (never a number before a choice)."""
    m = float(m[-1]) if isinstance(m, (list, tuple)) else float(m or 0)
    if m <= 0:
        return ""
    if not have or have <= 0:
        return "money they do not have spare"
    return _word(m / have, MONEY_SAY)


def _cap_item(s):
    """What a resource is spent on: an aim's slot (int), or the words for the rest (work, care, sleep, an entry); the
    Engine gives dict(slot, field) for an aim and dict(name, hours) for the time before aims."""
    if isinstance(s, dict):
        if s.get("slot") is not None:
            return int(s["slot"])
        s = s.get("name") or s.get("kind") or s.get("say") or ""
    return int(s) if str(s).isdigit() else OTHER_SAY.get(s, str(s))


def _upto(v, table):
    for cut, w in table:
        if v <= cut:
            return w
    return table[-1][1]


def years_say(y):
    """A clock's (median, low, high) years as a short range in words: 'usually 2 to 3 years'."""
    if not y:
        return ""
    lo, hi = float(y[1]), float(y[2])
    if hi < 1:
        return "usually under a year"
    lo_, hi_ = max(1, round(lo)), max(1, round(hi))
    return f"usually about {lo_} year{'s' if lo_ > 1 else ''}" if lo_ == hi_ else f"usually {lo_} to {hi_} years"


class AgendaMixin:
    def _agenda_raw(self, S):
        """The Engine's agenda (v25) or None; the v24 fallback is built in agenda_view."""
        if S is None or not hasattr(F, "agenda"):
            return None
        return F.agenda(S, 0)

    def agenda_view(self, loc=None):
        """The agenda for the screen: dict(items=[...], capacity=[...], forks=[...], full=bool), the most important first;
        None when off. full is False while the Engine gives only v24's aims (no capacity, forks or bottlenecks)."""
        if not GAME["agenda"] or not GAME["aims"]:
            return None
        loc = self.loc if loc is None else loc
        if loc is None:
            return None
        raw = self._agenda_raw(loc)
        if raw is None:
            return self._agenda_v24(loc)
        cap = {c["res"] if "res" in c else r: c for r, c in self._cap_items(raw.get("capacity"))}
        items = []
        for x in raw.get("items", []):
            st, pr = x.get("step") or {}, x.get("progress") or {}
            bn = x.get("bottleneck") or None
            items.append(dict(
                slot=int(x["slot"]), aim=x["aim"], field=x.get("field", ""), face=x.get("face", ""),
                calling=bool(x.get("calling")), by_player=bool(x.get("by_player")),
                importance=_word(float(x.get("importance", 0)), IMPORTANCE), why_now=x.get("why_now", ""),
                state=x.get("state", "holding"), state_say=STATE_SAY.get(x.get("state", "holding"), x.get("state", "")),
                priority=int(x.get("priority", 0)),
                step=dict(i=int(st.get("i", 0)), of=int(st.get("of", 0)), say=st.get("say", ""), next=st.get("next_say", "")),
                frac=None if pr.get("frac") is None else round(float(pr["frac"]), 2),
                effort_years=None if pr.get("effort_years") is None else round(float(pr["effort_years"]), 1),
                clock=years_say(pr.get("years")),
                lean=None if x.get("lean") is None else _word(float(x["lean"]), LEAN),
                pending=[str(f) for f in x.get("pending", [])],
                bottleneck=None if not bn else dict(res=bn.get("res", ""), say=RES_SAY.get(bn.get("res", ""), bn.get("res", "")),
                                                    shared_with=[str(s) for s in bn.get("shared_with", [])]),
                earned=[dict(name=a["name"], source=a.get("source", ""), age=a.get("age"), opens=a.get("opens", ""))
                        for a in x.get("earned", [])],
                potential=[dict(name=a["name"], step=a.get("step", "")) for a in x.get("potential", [])],
                upkeep=[dict(u) for u in x.get("upkeep", [])]))
        items.sort(key=lambda i: (i["priority"] or 99, i["slot"]))
        capacity = [dict(res=r, say=RES_SAY.get(r, r), load=_upto(self._load(c), LOAD),
                         items=[_cap_item(s) for s in c.get("items", [])])
                    for r, c in cap.items()]
        forks = [dict(id=str(f["id"]), slot=int(f["slot"]), kind=f.get("kind", ""), age=f.get("made_at_age"),
                      deadline=f.get("deadline_age"), urgency=float(f.get("urgency", 0)), group=f.get("group"),
                      blocks=f.get("blocks", "")) for f in raw.get("forks", [])]
        forks.sort(key=lambda f: -f["urgency"])
        groups = sorted({f["group"] for f in forks if f["group"] is not None}, key=str)
        groups += [int(f["id"]) if f["id"].isdigit() else f["id"] for f in forks if f["group"] is None]   # a fork on its
        # own is its own review (F.review takes its id as an int)
        reviews = {}
        if groups and self._paused_locals() is not None:     # a review is read at a pause, where it can be answered
            reviews = {str(g): v for g in groups for v in [self.review_view(g)] if v}
        return clean(dict(items=items, capacity=capacity, forks=forks, reviews=reviews, full=True))

    @staticmethod
    def _cap_items(c):
        if isinstance(c, dict):
            return [(r, c[r]) for r in RESOURCES if r in c]
        return [(x.get("res", ""), x) for x in (c or [])]

    @staticmethod
    def _load(c):
        have = float(c.get("have", 0) or 0)
        return float(c.get("committed", 0) or 0) / have if have > 0 else (9e9 if c.get("committed") else 0.0)

    def _agenda_v24(self, loc):
        """v24's aims read as an agenda: what the engine has (aims, steps, strength); nothing invented."""
        items = []
        for i, x in enumerate(self.aims_view(loc) or []):
            items.append(dict(
                slot=int(x["slot"]), aim=x["aim"], field="", face=x["face"], calling=bool(x["calling"]),
                by_player=not x["own"], importance=_word(float(x["strength"]), IMPORTANCE), why_now="",
                state="holding", state_say="held", priority=i + 1,
                step=dict(i=int(x["reached"]), of=len(x["steps"]), say=(x["steps"][x["reached"] - 1]["say"] if x["reached"] else ""),
                          next=x["next"] or ""),
                frac=None, effort_years=None, clock="", lean=None, pending=[], bottleneck=None,
                earned=[dict(name=s["say"], source="a step reached", age=None, opens="") for s in x["steps"] if s["reached"]],
                potential=[dict(name=s["height"], step=s["say"]) for s in x["steps"] if s.get("height") and not s["reached"]],
                upkeep=[]))
        return clean(dict(items=items, capacity=[], forks=[], reviews={}, full=False))

    def agenda_pace(self, slot, state):
        """The player sets how an aim is pursued (PACES): (agenda, None) or (None, why)."""
        S = self._paused_locals()
        if not GAME["agenda"] or S is None:
            return None, "not now"
        if state not in PACES:
            return None, "no such pace"
        if not hasattr(F, "set_pace"):
            return None, "this engine has no pace for aims yet"
        r = F.set_pace(S, 0, int(slot), state)
        if isinstance(r, str):
            return None, r
        self.history.setdefault("agenda", []).append((round(self.age(), 1), "pace", int(slot), state))
        return self.agenda_view(S), None

    def agenda_priority(self, slot, rank):
        """The player moves an aim to rank (1 = first): (agenda, None) or (None, why)."""
        S = self._paused_locals()
        if not GAME["agenda"] or S is None:
            return None, "not now"
        if not hasattr(F, "set_priority"):
            return None, "this engine has no priorities for aims yet"
        r = F.set_priority(S, 0, int(slot), int(rank))
        if isinstance(r, str):
            return None, r
        self.history.setdefault("agenda", []).append((round(self.age(), 1), "priority", int(slot), int(rank)))
        return self.agenda_view(S), None

    # ---- information before a commitment (decision #9, "Information before an aim commitment") and the agenda review
    # ("Group linked choices into an agenda review"): views of the Engine's foresee.preview and foresee.review. Both
    # read the one resource account and draw nothing; only apply_review changes the life.
    def _free_money(self, S):
        raw = self._agenda_raw(S)                            # the one account, as the agenda reads it
        c = (raw or {}).get("capacity") or S.get("capacity")
        c = c[0] if isinstance(c, (list, tuple)) and c and isinstance(c[0], dict) and "res" not in c[0] else c
        m = dict(self._cap_items(c)).get("money")
        return float(m.get("have", 0) or 0) - float(m.get("committed", 0) or 0) if m else 0.0

    def _names(self, S):
        """Aim slot -> its name, from the agenda (or v24's aims)."""
        raw = self._agenda_raw(S)
        xs = raw.get("items", []) if raw else (self.aims_view(S) or [])
        return {int(x["slot"]): x["aim"] for x in xs}

    def _with_say(self, w, names):
        if isinstance(w, dict):
            w = w.get("with", w.get("slot", ""))
        if isinstance(w, int) or (isinstance(w, str) and w.isdigit()):
            return names.get(int(w), "another aim")
        return OTHER_SAY.get(w, str(w))

    def _preview_words(self, pv, S, names):
        """The Engine's preview dict(needs, cost, hours, overlaps, window, unknown, exit) as the game's words: what it
        takes, what it costs, what it competes with, its deadline, what nobody can know yet, and how to step back."""
        if not pv:
            return None
        have = self._free_money(S)
        cost = pv.get("cost") or {}
        if not isinstance(cost, dict):
            cost = dict(money=cost)
        win = pv.get("window") or {}
        ex = pv.get("exit")
        return dict(
            needs=[str(x) for x in pv.get("needs") or []],
            hours=hours_say(pv.get("hours")),
            entry=money_say(cost.get("entry"), have),
            money=money_say(cost.get("money"), have),
            overlaps=[self._with_say(w, names) for w in pv.get("overlaps") or []],
            window=(f"opens at {int(win['opens'])}, " if win.get("opens") is not None and win["opens"] > self.age() else "")
                   + (f"closes at {int(win['closes'])}" if win.get("closes") is not None else ""),
            unknown=[str(x) for x in pv.get("unknown") or []],
            exit=(ex.get("say", "") if isinstance(ex, dict) else str(ex or "")))

    def _lib_line(self, lines, key, **slots):
        """One of the Library's lines, picked by the life's name and the key (the same line every time), with its slots
        filled; "" when a slot it names has no words here (a line is shown only when its fact is known)."""
        if not lines:
            return ""
        i0 = zlib.crc32(f"{self.name}|{key}".encode()) % len(lines)
        slots = dict(dict(N=self.name, Ns=self.name + "'s"), **{k: v for k, v in slots.items() if v})
        for j in range(len(lines)):                      # the picked line, else the next one whose slots are all known
            try:
                s = lines[(i0 + j) % len(lines)].format(**slots)
            except (KeyError, IndexError):
                continue
            return s[:1].upper() + s[1:]
        return ""

    @staticmethod
    def _aim_rec(loc, f):
        """The fork's first aim's record in S["aim2"] (field, say = the next rung's words), or {}."""
        a2 = loc.get("aim2") or []
        a2 = a2[0] if a2 and isinstance(a2[0], (list, tuple)) else a2
        try:
            r = a2[int(f.get("aims", [])[0])]
        except (IndexError, TypeError, ValueError):
            return {}
        return r if isinstance(r, dict) else {}

    def _why_now(self, why, raw, pv, aims, rec=None):
        """Why a fork is put now: when the Engine gives one of the Library's WHY_NOW keys (commit, cost, chance, window,
        over, changed), its line with the preview's facts and the aim's next rung (S["aim2"] say); else the Engine's
        words as they are."""
        rec = rec or {}
        if AL is None or not isinstance(why, str) or why not in getattr(AL, "WHY_NOW", {}):
            return why
        win = (raw.get("window") or {}).get("closes") if isinstance(raw.get("window"), dict) else None
        others = [w for w in (pv or {}).get("overlaps") or [] if w not in aims]
        return self._lib_line(AL.WHY_NOW[why], "why:" + why, thing=raw.get("thing") or rec.get("field"),
                              next=raw.get("next") or rec.get("say"), door=raw.get("door"), hours_words=(pv or {}).get("hours"),
                              money_words=(pv or {}).get("money"), other=others[0] if others else None,
                              closes=win is not None and f"when {self.name} is about {int(win)}")

    def _lib_preview(self, pv, raw, thing):
        """The preview as the Library's sentences (earth_aim_lines PREVIEW, in PREVIEW_ORDER), for the parts whose facts
        the Engine gave; "" without the Library's table."""
        if AL is None or not pv:
            return ""
        P = AL.PREVIEW
        aims_over = [w for w, r in zip(pv["overlaps"], raw.get("overlaps") or []) if isinstance(r, int) or str(r).isdigit()]
        win = (raw.get("window") or {}).get("closes")
        parts = dict(hours=pv["hours"] and self._lib_line(P["hours"], "hours", hours_words=pv["hours"], thing=thing),
                     money_year=pv["money"] and self._lib_line(P["money_year"], "money", money_words=f"{pv['money']}, each year"),
                     entry=pv["entry"] and self._lib_line(P["entry"], "entry", entry_words=pv["entry"]),
                     overlap_aim=aims_over and self._lib_line(P["overlap_aim"], "overlap", other=aims_over[0]),
                     overlap_work="work" in (raw.get("overlaps") or []) and self._lib_line(P["overlap_work"], "work"),
                     window=win is not None and self._lib_line(P["window"], "window", closes=f"when {self.name} is about {int(win)}"))
        return " ".join(parts[k] for k in AL.PREVIEW_ORDER if parts.get(k))

    def preview_view(self, aim, step=None):
        """Before taking up an aim or committing to its next step: the preview in words, or None (off, or an engine
        without previews: v24's aims show their ladder only)."""
        S = self._paused_locals()
        if not GAME["agenda"] or S is None or not hasattr(F, "preview"):
            return None
        pv = F.preview(S, 0, aim, step)
        if not pv or isinstance(pv, str):
            return None
        out = self._preview_words(pv, S, self._names(S))
        out["say"] = self._lib_preview(out, pv, pv.get("thing"))
        return clean(out)

    def review_view(self, group):
        """An agenda review: the linked forks of one group, why they are linked, each one's preview and options, the
        shared capacity now and after each combination the Engine lists. None when off or the Engine has none."""
        S = self._paused_locals()
        if not GAME["agenda"] or S is None or not hasattr(F, "review"):
            return None
        r = F.review(S, 0, group)
        if not r or isinstance(r, str):
            return None
        names = self._names(S)
        cap_words = lambda c: [dict(res=k, say=RES_SAY.get(k, k), load=_upto(self._load(v), LOAD)) for k, v in self._cap_items(c)]
        forks = [dict(id=str(f["id"]), slot=int(f["slot"]), aim=names.get(int(f["slot"]), "an aim"), kind=f.get("kind", ""),
                      why=f.get("why", ""), deadline=f.get("deadline_age"),
                      preview=self._preview_words(f.get("preview"), S, names),
                      options=[dict(key=str(o.get("key", i)), say=o.get("say", "")) for i, o in enumerate(f.get("options", []))])
                 for f in r.get("forks", [])]
        combos = [dict(choices={str(k): str(v) for k, v in (c.get("choices") or {}).items()}, capacity=cap_words(c.get("capacity")),
                       slower=[names.get(int(s), "an aim") for s in c.get("slower", [])]) for c in r.get("combos", [])]
        why = r.get("why", "")
        if AL is not None and why in AL.LINKED:
            why = self._lib_line(AL.LINKED[why], "linked") or why
        for f, x in zip(forks, r.get("forks", [])):
            if f["preview"]:
                f["preview"]["say"] = self._lib_preview(f["preview"], x.get("preview") or {}, (x.get("preview") or {}).get("thing"))
        return clean(dict(group=r.get("group", group), why=why, forks=forks, capacity=cap_words(r.get("capacity")),
                          combos=combos))

    def agenda_apply(self, choices, sets=None):
        """The player's answers to a review (or one fork): choices {fork id: option key}, sets {slot: pace}. Applied once
        by the Engine (no double debit): (agenda, None) or (None, why). A fork not in choices stays open."""
        S = self._paused_locals()
        if not GAME["agenda"] or S is None:
            return None, "not now"
        if not hasattr(F, "apply_review"):
            return None, "this engine has no agenda reviews yet"
        sets = {int(k): v for k, v in (sets or {}).items()}
        if any(v not in PACES for v in sets.values()):
            return None, "no such pace"
        r = F.apply_review(S, 0, dict(choices={str(k): str(v) for k, v in choices.items()}, set=sets))
        if isinstance(r, str):
            return None, r
        self.history.setdefault("agenda", []).append((round(self.age(), 1), "review", dict(choices), sets))
        return self.agenda_view(S), None

    # ---- fork cards (GAME aim_forks): the Engine puts at most one fork a week (S["aim_fork"], an id or -1) at the
    # situation pause, in place of the next optional ask; with aim_forks "every" it is always asked. When the week's
    # moment is the fork's own (L["AIM_FORK"][s] >= 0) its options answer it; on any other moment the card opens the
    # fork's review (F.review takes a fork id), and the moment is answered as usual
    def fork_now(self, loc, s):
        """The id of the fork the Engine put this week, else None."""
        if not GAME["aim_forks"] or loc is None or loc.get("aim_fork") is None:
            return None
        fid = np.asarray(loc["aim_fork"]).ravel()
        if fid.size and fid[0] is None:
            return None
        fid = int(fid[0]) if fid.size else -1
        return fid if fid >= 0 else None

    def fork_fresh(self, loc, fid, s=None):
        """Whether the fork put this week stops the life for its card: only when the Engine carries it on its own moment
        (a due fork, Engine 10-23). Any other fork waits on the agenda and comes as a card on the next moment asked anyway
        (fork_waiting, the urgent first), so fork cards keep a life's asks a year near v24's (Release's AM4)."""
        return fid is not None and self._fork_on_moment(s)

    def fork_waiting(self, loc):
        """A player's fork waiting that has not been put to them as a card yet (the urgent, then the oldest), or None."""
        if not GAME["aim_forks"] or loc is None:
            return None
        fs = loc.get("aim_forks") or []
        fs = fs[0] if fs and isinstance(fs[0], (list, tuple)) else fs
        done = {x[1] for x in self.history.get("forks_asked", [])}
        new = [f for f in fs or [] if isinstance(f, dict) and str(f.get("id")) not in done]
        if not new:
            return None
        f = min(new, key=lambda f: (not f.get("urgent"), f.get("week", 0), str(f.get("id"))))
        return int(f["id"]) if str(f["id"]).isdigit() else f["id"]

    def _fork_on_moment(self, s):
        return s is not None and "AIM_FORK" in self.L and int(np.asarray(self.L["AIM_FORK"])[s]) >= 0

    def fork_later(self, s):
        """The option of moment s that leaves a player's fork open ("later": only that aim waits), or None. The Engine
        tags it in L["AIM_TAG"][s, k] by the index of "later" in its tag names (L["AIM_NAMES"]["tags"], else
        world_keys.AIM_TAGS: contracts.md)."""
        names = (self.L.get("AIM_NAMES") or {}).get("tags") if isinstance(self.L.get("AIM_NAMES"), dict) else None
        if not names:
            try:
                import world_keys
                names = getattr(world_keys, "AIM_TAGS", ())
            except Exception:
                names = ()
        names = list(names or ())
        if "later" not in names or "AIM_TAG" not in self.L:
            return None
        row = np.asarray(self.L["AIM_TAG"])[s]
        ks = np.nonzero(row == names.index("later"))[0]
        return int(ks[0]) if ks.size else None

    def fork_card(self, loc, fid, s=None):
        """The fork on the card: which aims it is about, why now, its preview in words, and whether it is linked to
        other decisions (an agenda review), from S["aim_forks"]; None when the Engine has no record of it."""
        fs = loc.get("aim_forks") or []
        fs = fs[0] if fs and isinstance(fs[0], (list, tuple)) else fs
        f = next((x for x in fs if str(x.get("id")) == str(fid)), None)
        if f is None:
            return None
        names = self._names(loc)
        self.history.setdefault("forks_asked", []).append((round(self.age(), 1), str(fid), len(f.get("options", []))))
        aims = [names.get(int(a), "an aim") for a in f.get("aims", [])]
        pv = self._preview_words(f.get("preview"), loc, names)
        on = self._fork_on_moment(s) and str(self.fork_now(loc, s)) == str(fid)   # the moment is this fork's own
        return clean(dict(id=str(fid), aims=aims, kind=f.get("kind", ""),
                          why=self._why_now(f.get("why", ""), f.get("preview") or {}, pv, aims, self._aim_rec(loc, f)), preview=pv,
                          urgent=bool(f.get("urgent")), grouped=bool(f.get("grouped")),
                          group=None if f.get("group") is None else str(f["group"]),
                          later=self.fork_later(s) if on else None, on_moment=on,
                          review=str(f["group"]) if f.get("grouped") and f.get("group") is not None else str(fid)))

    @staticmethod
    def preview_lines(pv):
        """A preview as short lines: what it takes, costs, competes with, its deadline, the unknowns, the way back."""
        if not pv:
            return []
        L = [pv["say"]] if pv.get("say") else []
        if pv["needs"]:
            L.append("needs " + ", ".join(pv["needs"]))
        cost = [x for x in (pv["hours"], pv["money"] and f"each year {pv['money']}", pv["entry"] and f"to start, {pv['entry']}") if x]
        if cost:
            L.append("takes " + "; ".join(cost))
        if pv["overlaps"]:
            L.append("competes with " + ", ".join(pv["overlaps"]))
        if pv["window"]:
            L.append("the chance " + pv["window"])
        if pv["unknown"]:
            L.append("not known yet: " + ", ".join(pv["unknown"]))
        if pv["exit"]:
            L.append("stepping back: " + pv["exit"])
        return L

    def agenda_lines(self, A=None):
        """The agenda in plain lines (the terminal's key j)."""
        A = self.agenda_view() if A is None else A
        if not A:
            return ["The agenda is off."]
        L = [f"{self.name}'s agenda" + ("" if A["full"] else " (this engine shows aims only: no shared time or forks yet)")]
        if A["capacity"]:
            L.append("  " + " · ".join(f"{c['say']}: {c['load']}" for c in A["capacity"]))
        if not A["items"]:
            L.append("  No aims held.")
        names = {str(x["slot"]): x["aim"] for x in A["items"]}
        for x in A["items"]:
            L.append(f"  {x['priority']}. {x['aim']} [{x['face']}], {x['importance']}, {x['state_say']}"
                     + (f"; {x['lean']}" if x["lean"] else ""))
            st = x["step"]
            L.append(f"     step {st['i']} of {st['of']}" + (f", next: {st['next']}" if st["next"] else ", every step reached" if st["i"] >= st["of"] else "")
                     + (f" ({x['effort_years']:g} years at it, {x['clock']})" if x["effort_years"] is not None and x["clock"] else
                        f" ({x['clock']})" if x["clock"] else ""))
            if x["why_now"]:
                L.append(f"     why now: {x['why_now']}")
            if x["bottleneck"]:
                L.append(f"     held back by {x['bottleneck']['say'].lower()}"
                         + (f", shared with {', '.join(names.get(s, 'another aim') for s in x['bottleneck']['shared_with'])}"
                            if x["bottleneck"]["shared_with"] else ""))
            if x["pending"]:
                L.append(f"     waiting on you: {len(x['pending'])} decision{'s' if len(x['pending']) > 1 else ''}")
            if x["earned"]:
                L.append("     earned: " + ", ".join(a["name"] + (f" ({a['source']})" if a["source"] else "") for a in x["earned"]))
            if x["potential"]:
                L.append("     could bring: " + ", ".join(a["name"] for a in x["potential"]))
        if A["forks"]:
            L.append(f"  Decisions waiting: {len(A['forks'])}")
        for g, r in A.get("reviews", {}).items():
            L.append(f"  Linked decisions ({r['why'] or 'they share a limit'}):")
            for f in r["forks"]:
                L.append(f"     {f['id']}. {f['aim']}: " + " / ".join(f"{o['key']}={o['say']}" for o in f["options"]))
                L += [f"        {w}" for w in self.preview_lines(f["preview"])]
            for c in r["combos"]:
                L.append("     if " + ", ".join(f"{k}={v}" for k, v in c["choices"].items()) + ": "
                         + "; ".join(f"{x['say']} {x['load']}" for x in c["capacity"])
                         + (f"; slower: {', '.join(c['slower'])}" if c["slower"] else ""))
            L.append("     ja <decision>=<option> .. s<slot>=<pace>: answer them together")
        if A["full"]:
            L.append("  jp<slot> <pace>: pursuing, reduced, keeping_up, paused, holding · jr<slot> <rank>: move it")
        return L
