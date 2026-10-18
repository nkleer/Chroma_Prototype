"""Game's methods for "Every change has a cause" (chroma-ideas/gameplay-2026-10-17/every-change-has-a-cause.md; Emren
10-18 "Staged" and "Fold"), behind GAME causes (G1 to G3) and causes_fold (G4). Words only: nothing here draws, so with
either switch on every step plays as with it off.

Part of class Game (game.py), which inherits CausesMixin. What it reads:
- the role event's why (the Engine's played-life key role_why, PR E1): a list of the rule's parts that held, in order,
  each a dict with k one of
    mark    mark (the Library's mark words), t (the week it was left): a pick the game kept that week names its act,
            age and person (Picks come back's record)
    moment  name (the moment met), t (its week)
    held    name (the title or perk it builds on), t (since when)
    money   (the money for it)
    age, stage, luck, none, pack (pack, clause): told by the Library's cause: phrase when it has one, else not named
  and for a loss, k held with years (time passed: years held) or unused with years and as (slipped away: years since
  used; as unused, alone, short of money or time). Any other k names nothing. A rule in the Library's CAUSE_HOLD (the
  L1 audit's loose rules) is told only with its cause: phrase, never with the clause that held.
  Without why, a loss that ran its time says the years the game saw it held; a gain names nothing.
- loc["asrc_c"] (the Engine's E1 (a), at the pause): what moved the colours, by source (ASOURCES), cumulative, shape
  (sources, C). The year line diffs two pauses for the year's movers after its own told events.
- the Library's words (earth_story CAUSE, YEAR_WHY, FOLD), key by key over the stand-ins below."""
import re
import numpy as np
from game_base import C, COLORS, E, ES, GAME, mk, neg_of, plain, role_info
from game_words import FADE_WORDS, GROW_WORDS

# stand-in words, until the Library's (L2) replace them key by key: {N} the character, {age} an age, {n} years in words
CAUSE0 = dict(
    pick="since {N} chose to {act} at {age}",                  # a mark their own asked pick left
    pick_who="since {N} chose to {act} at {age}, with {P}",
    pick_gone="since {N} chose to {act} at {age}, with {P}, gone now",
    mark="since the time {N} {what}, at {age}",               # a mark a moment left (no pick of theirs; MARK_SAY words)
    moment="after {what} at {age}",
    held_title="as {say}",                                     # {say}: the title as said ("a nurse")
    held_perk="as one who {say}",                              # {say}: the perk's predicate ("can drive")
    money="with the money for it",
    years="after {n} years",                                   # a loss: its time ran out (years_one, unused_one: n is 1)
    years_one="after a year",
    unused_one="after a year unused",
    unused="after {n} years unused",                           # a loss: it slipped away (a skill unused)
    unused_alone="after {n} years with few people close",     # a bond, while their ties were thin (the Engine's as)
    unused_money="after {n} years short of money",             # an asset, while money was short
    unused_time="after {n} years",                             # a standing, as time went by
)
YEAR0 = dict(
    turn="A year that turned {N}: {how}.",
    turn_by="A year that turned {N}: after {ev}, {how}.",
    src={"unmet needs": "what they went without", "surroundings": "the people around them", "role models": "the people they look up to",
         "settling back": "settling back into themselves", "turning points": "a turning point",
         "talking oneself into it": "talking themselves into it", "resolutions": "their own resolutions",
         "outside events": "what happened around them", "the times": "the times", "discontent": "discontent",
         "contentment": "contentment", "restlessness": "restlessness", "dreams and plans": "their dreams and plans",
         "a shorter horizon": "a shorter horizon"},
)
FOLD0 = dict(gain="This year {N} {got}.", lose="This year {N} {lost}.", both="This year {N} {got}, and {lost}.")
UNUSED_AS = {"alone": "unused_alone", "short of money": "unused_money", "time": "unused_time"}   # the Engine's as on a loss
CAUSE_HOWS = ("in time", "slipped away", "time passed")       # the ways a change comes with no cause told today
FOLD_KINDS = ("skill", "standing", "bond")                     # G4: small perks that come and go (titles keep their line)
FOLD_HOWS = ("in time", "slipped away", "time passed", "regained")
_NUMW = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")


def _words(name, base):
    """The Library's table name (earth_story) over the stand-in, key by key."""
    lib = getattr(ES, name, None) if ES is not None else None
    return {**base, **lib} if isinstance(lib, dict) else base


def _years(y):
    n = max(1, int(round(float(y))))
    return _NUMW[n] if n < len(_NUMW) else str(n)


def _n_words(W, key, y):
    """A loss's words with its years: the key's _one form when the years round to one (the Library's years_one)."""
    if max(1, int(round(float(y)))) == 1 and key in ("years", "unused") and key + "_one" in W:
        return W[key + "_one"]
    return W[key].replace("{n}", _years(y))


def _clean(s):
    """Text for a marker payload: no markers, no separators."""
    return re.sub(r"[|⟦⟧]", " ", plain(str(s or ""))).strip()


def _join(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


class CausesMixin:
    # ------------------------------------------------------------------ G1, G3: a gain or loss names its cause
    def _role_cause(self, r, d, how):
        """The cause of a title or perk gained in time, or lost as time passed or unused: (kind, phrase with its trail
        marker) or None. Records when the game saw it gained, for a loss's years without the Engine's why."""
        name, t = r["name"], int(self.t)
        held = self.__dict__.setdefault("_cause_since", {})
        if r["what"] in ("gained", "regained", "restored"):
            held[name] = t
        if how not in CAUSE_HOWS:
            return None
        W = _words("CAUSE", CAUSE0)
        why = r.get("why") or []
        if r["what"] == "lost":
            part = next((p for p in why if p.get("k") in ("held", "unused") and p.get("years") is not None), None)
            if part is None and how == "time passed" and name in held:
                part = dict(k="held", years=(t - held[name]) / 52)
            if part is None:
                return None
            k = "years" if part["k"] == "held" else "unused"
            w = W[UNUSED_AS[part["as"]]].replace("{n}", _years(part["years"])) \
                if k == "unused" and UNUSED_AS.get(part.get("as")) in W else _n_words(W, k, part["years"])
            return k, self._trail(k, w, "")
        if name in (getattr(ES, "CAUSE_HOLD", None) or ()):   # a rule the Library's audit found loose (L1): the clause
            say = next((p["say"] for p in why if p.get("say")), None)   # that held may read false, so only its cause:
            return ("none", self._trail("none", say, "")) if say else None   # phrase, until cause_fit tightens it
        for part in why:
            got = self._cause_part(part, W)
            if got:
                return got
        return None

    def _cause_part(self, part, W):
        k, age = part.get("k"), (lambda w: _years(w / 52) if w is not None else "")
        if k == "mark":
            pick = next((self._picks.get(int(part["t"]) + dt) for dt in (0, -1, 1) if self._picks.get(int(part["t"]) + dt)), None) \
                if part.get("t") is not None else None
            if pick is not None:
                act = _clean(pick["act"]); act = act[:1].lower() + act[1:]
                p = pick.get("who")
                known = p is not None and p.get("introduced") and p.get("name")
                tpl = W["pick"] if not known else W["pick_who"] if p.get("alive", True) else W["pick_gone"]
                txt = tpl.replace("{act}", act).replace("{age}", str(int(pick["age"]))).replace(
                    "{P}", mk("p", p["id"], p["name"]) if known else "")
                return "pick", self._trail("pick", txt, f"{pick['age']}|{p['id'] if known else ''}|{_clean(pick['moment'])}")
            what = (getattr(ES, "MARK_SAY", None) or {}).get(part.get("mark")) or part.get("mark") or part.get("name")
            if what:                                    # the mark as the song says it ("kept their word")
                a = int(part["t"] / 52) if part.get("t") is not None else ""
                return "mark", self._trail("mark", W["mark"].replace("{what}", _clean(what)).replace("{age}", str(a)),
                                           f"{a}||{_clean(part.get('moment') or what)}")
            return None
        if k == "moment" and part.get("name"):
            a = int(part["t"] / 52) if part.get("t") is not None else ""
            return "moment", self._trail("moment", W["moment"].replace("{what}", _clean(part["name"])).replace("{age}", str(a)),
                                         f"{a}||{_clean(part['name'])}")
        GR = self.L.get("ROLES") or {}
        if k == "held" and part.get("name") in GR.get("ID", {}):
            d = role_info(GR, GR["ID"][part["name"]])
            say = d["say"] if d["title"] else d["pred"]  # a perk as a predicate ("is known for turning up")
            return "held", self._trail("held", W["held_title" if d["title"] else "held_perk"].replace("{say}", say),
                                       "||" + _clean(d["say"]))
        if k == "money":
            return "money", self._trail("money", W["money"], "")
        if k in ("age", "stage", "none", "pack") and part.get("say"):      # the Library's cause: phrase, as the Engine passes it
            return k, self._trail(k, part["say"], "")
        return None

    def _trail(self, kind, text, payload):
        """G3: the cause as a hoverable phrase (marker Y: kind|age|person id|the earlier moment)."""
        out = self.story.fill(text)
        if text[:1].islower():                          # a clause inside the line: fill capitalises a sentence's start
            out = out[:1].lower() + out[1:]
        return mk("Y", f"{kind}|{payload}" if payload else kind, out)

    def _with_cause(self, line, cause):
        """The role line with its cause as the last clause ("Ari can swim now, since ...")."""
        s = line.rstrip()
        return (s[:-1] + ", " + cause + "." if s.endswith(".") else s + " " + cause + ".") if s else line

    # ------------------------------------------------------------------ G2: a year that turned them says why
    def _cause_week(self, ev):
        """This week's colour move, kept with its told event (the same one the temperament line uses)."""
        dw = self.__dict__.get("_cause_dw")
        if ev is not None and dw is not None:
            self.__dict__.setdefault("_cause_evs", []).append((dw, ev))

    def _cause_year(self, body, w, loc):
        """The year's mood line, when the colours moved cause_turn or more (L1 over the five) since the last chapter,
        becomes a line naming the biggest mover: a told event of the year whose week moved them cause_share or more of
        the way they went, else the Engine's top source (asrc_c), else only how they turned."""
        w = np.asarray(w, float)
        prev, self._cause_w0 = self.__dict__.get("_cause_w0"), w
        evs, self._cause_evs = self.__dict__.get("_cause_evs", []), []
        src_now = loc.get("asrc_c")                                       # a live view, ASOURCES x colours: copy it
        src_now = np.array(src_now, float) if src_now is not None else None
        src_prev, self._cause_src0 = self.__dict__.get("_cause_src0"), src_now
        if prev is None or self.burn_in or not body or self.t < 6 * 52:     # a small child: the mood line, as today
            return body
        shift = w - prev
        if np.abs(shift).sum() < GAME["cause_turn"]:
            return body
        up, dn = int(np.argmax(shift)), int(np.argmin(shift))
        how = GROW_WORDS[COLORS[up]] + (" and " + FADE_WORDS[COLORS[dn]] if shift[dn] <= -0.03 else "")
        Y = _words("YEAR_WHY", YEAR0)
        ss = float(shift @ shift)
        sc = sorted(((float(np.asarray(dw) @ shift) / ss, n) for dw, n in evs), reverse=True)
        ev, kind = None, "turn"
        if sc and sc[0][0] >= GAME["cause_share"]:
            ev, kind = sc[0][1], "event"
        elif src_now is not None and src_prev is not None and len(getattr(E, "ASOURCES", ())) == len(src_now):
            ds = (src_now - src_prev) @ shift / ss
            j = int(np.argmax(ds))
            if ds[j] >= GAME["cause_share"]:
                ev, kind = Y["src"].get(E.ASOURCES[j], E.ASOURCES[j]), "source"
        text = (Y["turn_by"].replace("{ev}", ev) if ev else Y["turn"]).replace("{how}", how)
        line = mk("Y", f"{kind}|{np.abs(shift).sum():.2f}|{COLORS[up]}|{COLORS[dn]}", self.story.fill(text))
        m = re.match(r"⟦m:([^⟧]*)⟧(.*?)⟦/⟧", body)
        if not m:
            return body
        tail = body[m.end():]
        own = line if m.group(2).endswith(".") else line[:line.rindex(".")] + line[line.rindex(".") + 1:]
        self.__dict__.setdefault("_cause_turns", []).append(kind)
        return f"⟦m:{m.group(1)}⟧{own}⟦/⟧{tail}"

    # ------------------------------------------------------------------ G4: small changes fold into the year
    def _fold_role(self, r, d, how, cause, lvl):
        """causes_fold: a small perk gained or lost in time is kept for the year's fold line instead of its own line."""
        if not (GAME["causes_fold"] and not self.burn_in and not d["title"] and d["kind"] in FOLD_KINDS and how in FOLD_HOWS
                and r["what"] in ("gained", "regained", "lost") and not d["pred"].startswith(("once ", "always "))):
            return False
        self.__dict__.setdefault("_fold", []).append((r["what"] != "lost", d, cause, lvl))
        return True

    def _fold_year(self):
        """The year's small gains and losses as one line (FOLD), each with its cause inside its own marker."""
        fold, self._fold = self.__dict__.get("_fold", []), []
        if not fold or self.burn_in:                    # the years before the chosen start: told briefly, without it
            return
        lvl = min(x[3] for x in fold)
        fold = [x[:3] for x in fold]
        F = _words("FOLD", FOLD0)
        part = lambda g, d, c: self.story.role_mark(d, (d["pred"] if g else neg_of(d["pred"])) + (" (" + c[1] + ")" if c else ""),
                                                   "" if g else "lost")
        got = [part(g, d, c) for g, d, c in fold if g]
        lost = [part(g, d, c) for g, d, c in fold if not g]
        tpl = F["both"] if got and lost else F["gain"] if got else F["lose"]
        line = self.story.fill(tpl.replace("{got}", _join(got) if got else "").replace("{lost}", _join(lost) if lost else ""))
        self._say(line, lvl, "role_fold", items=[dict(name=d["name"], what="gained" if g else "lost", cause=c[0] if c else "")
                                               for g, d, c in fold])
