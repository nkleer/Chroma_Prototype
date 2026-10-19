"""Game's methods for Bold ways (chroma-ideas/gameplay-2026-10-17/bold-ways.md; Emren "Build" 10-18 23:29 UTC), behind GAME
bold, with the Engine's played-life key bold_play. With either off nothing here runs, so every step plays as before.

Part of class Game (game.py), which inherits BoldMixin. The hand-over with the Engine (its note of 10-19 00:01 UTC),
for life 0 (game_base sets batch.BOLD_MOMENTS, which loads the Library's BOLD rows and LINKS):
- L["BOLD_S"]: {s: [row, ...]} (at most 2); L["BOLD"][row]: the compiled row (moment, s, base, colour, kind
  "bold:<moment>/<colour>", label, chance, req, change; src: the Library's own dict, works, fails and the act fields).
- situation: the game sets P["bold_ask"] when it will put this week's life event to the player (by pacing alone: the
  card is then always asked at choose); the Engine spends it at the choice.
- choose: loc["bold_now"][0], up to two dicts (row, slot, base: the way it plays as, label, chance: the written
  chance, p: their own odds, 10 to 90%, seen), None in a week not asked; loc["bold_pick"][0], the slot the character
  took (-1: none). The game answers with a = the base way and P["bold_take"] = the slot taken, or -1, always set.
- odds: the true odds are already the bold way's own p (a push's effort still comes off them, as for any way).
- end: the week's events carry dict(bold=dict(age, row, slot, label, moment, colour, p, ok)); what it won or cost
  comes as role events with how "through <bold label>", so the cause lines name it.
- returns: a bold pick plants a seed of kind "bold:<moment>/<colour>" (ok, bold=row, title, who); its link plays as a
  return whose seed has link=True, change=True for a shared link, gone=True if its person has died since.
On the card a bold way's number is BOLD_IX + 100 x slot + base (game_base bix gives the base back), so every array the
engine keeps per way reads the base way, and a pick of a bold way is never the same number as the ordinary one."""
import numpy as np
from game_base import BOLD_IX, ES, FREQ, GAME, role_info
from game_words import accept_word, clash_with, hint

BOLD_WORDS = dict(chip="bold", likelier="likelier for them", harder="harder for them",
                  went="took the bold way", pushed="you pushed them to the bold way",
                  safe="you held them back from the bold way")


def _as_list(x):
    """A row field as a list: a list as it is, a text split by ';' (the Library's catalogue names)."""
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return [y for y in x if y]
    return [y.strip() for y in str(x).split(";") if y.strip()] if x else []


KIND_SAY = dict(career="their work", community="their place in the community", partner="their partner",
                faith="their place in the faith")      # drops_if_fails: kind:<kind>, whatever title of that kind they hold


class BoldMixin:
    def _bold_on(self, loc):
        return bool(GAME["bold"]) and loc is not None and bool((loc.get("P") or {}).get("bold_play"))

    # ------------------------------------------------------------------ the pauses
    def _bold_situation(self, t, loc, s, until_checkpoint):
        """At the situation pause: when this week's moment will be put to the player (pacing only, as _checkpoint would
        judge it), ask the Engine for its bold ways. The card is then asked at choose whatever its importance. The
        engine puts a life event in the week's place after this pause (s_ev), and a return or a link after it too, so a
        bold way's link due and waiting asks as well (a return is always asked; with none this week, no bold way is
        offered on an ordinary week)."""
        self._bold_t = None
        if not self._bold_on(loc) or not until_checkpoint or t / 52 < self.start_age or self._turn_due(t):
            return
        if self._link_due(loc):
            self._bold_t = (int(t), -1)
        else:
            had = "had_ev" in loc and bool(np.asarray(loc["had_ev"]).ravel()[0])
            s = int(np.asarray(loc["s_ev"]).ravel()[0]) if had else s
            if not had or not self._bold_paced(t, loc, s):
                return
            self._bold_t = (int(t), int(s))
        loc["P"]["bold_ask"] = True

    def _bold_paced(self, t, loc, s):
        """A life event s this week, by _checkpoint's pacing for a life event."""
        if s == self.ORD or not self._bold_here(loc, s):
            return False
        gap_weeks, _thr, again = FREQ[self.freq]
        if t - self._last_cp < gap_weeks // 2:
            return False
        if t - self._last_seen.get(s, -10 ** 6) < (again // 2) * self._cp_n.get(s, 0):
            return False
        if GAME["returns"] and s in self._cp_n and self._ret_due(loc):
            return False
        return True

    def _link_due(self, loc):
        """A bold way's seed (kind "bold:<moment>/<colour>") of a pick the game kept is due and waiting: its link may be
        this week's moment (the Engine chooses after the situation pause)."""
        return any(str(x.get("kind", "")).startswith("bold:") and x.get("done") is None and x.get("due") is not None
                   and self.t >= x["due"] and int(x["t"]) in self._picks for x in loc.get("ep_seeds") or ())

    @staticmethod
    def _bold_here(loc, s):
        """Whether the Library has a bold way for moment s (the Engine's L["BOLD_S"]: {s: [row, ...]}; without it, any
        life event may have one: the Engine answers with none)."""
        L = loc["L"]
        of = L.get("BOLD_S")
        if of is None:
            return True
        if isinstance(of, dict):
            return bool(of.get(s) or of.get(L["names"][s]))
        return s < len(of) and bool(len(of[s]) if hasattr(of[s], "__len__") else of[s] >= 0)

    def _bold_choose(self, loc):
        """At the choose pause: the bold ways the Engine offers this week, and the character's own answer kept as it is
        unless the player changes it (P bold_take must always be set)."""
        self._bold_now, self._bold_pick = [], -1
        if not self._bold_on(loc):
            return
        bn = loc.get("bold_now")                        # per life: life 0's list, or None in a week not asked
        bn = bn[0] if bn is not None and len(bn) and (bn[0] is None or isinstance(bn[0], (list, tuple))) else bn
        self._bold_now = sorted((dict(b) for b in (bn or ())), key=lambda b: int(b.get("slot", 0)))[:2]
        bp = loc.get("bold_pick")
        self._bold_pick = int(np.asarray(bp).ravel()[0]) if bp is not None and np.size(bp) else -1
        if self._bold_pick not in {int(b.get("slot", i)) for i, b in enumerate(self._bold_now)}:
            self._bold_pick = -1
        if self._bold_now:
            loc["P"]["bold_take"] = self._bold_pick

    def _bold_forced(self, t, s):
        """The card the situation pause promised the player, with the bold ways the Engine offers."""
        return bool(self._bold_now) and self._bold_t == (int(t), int(s))

    def _bold_take(self, cp, choice):
        """decide(): the slot the answer takes (-1 for an ordinary way), for the Engine."""
        if self.loc is not None and "P" in self.loc:
            self.loc["P"]["bold_take"] = (int(choice) - BOLD_IX) // 100 if int(choice) >= BOLD_IX else -1

    # ------------------------------------------------------------------ the card
    def _bold_row(self, L, r):
        """The Library's BOLD row as the game reads it (one place, so a renamed field changes here only): the Engine's
        compiled row L["BOLD"][r] (moment, s, base, colour as an index, kind "bold:<moment>/<colour>", label, chance, req,
        change) over the Library's own dict in its src (works, fails, mark, the act fields), the colour as a letter."""
        rows = L.get("BOLD")
        row = rows[r] if isinstance(rows, (list, tuple)) and 0 <= int(r) < len(rows) else None
        if not isinstance(row, dict):
            return {}
        out = dict(row.get("src") or {}, **{k: v for k, v in row.items() if k != "src"})
        c = str(row.get("kind", "")).rpartition("/")[2].strip()
        out["colour"] = c if c in "WUBRG" and c else (row.get("src") or {}).get("colour", "")
        return out

    def _bold_stake(self, L, row, m, loc=None):
        """What a bold way wins and costs for good, from its row's fields in the Library's own vocabulary: on success
        title, grants, drops (a status shed), takes (rare); on failure title_if_fails, takes_if_fails, drops_if_fails (a
        title, or kind:<kind>: whatever title of that kind they hold), suspends_if_fails (a perk, for a while). A gain
        they already hold or cannot get at their age (the catalogue's ages=), or a loss of what they do not hold, changes
        nothing and is not said. Returns (win, cost),
        lists of short phrases, and the names they come from (win and cost: [(field, name)]), for the proof that the
        card's word holds."""
        GR = L.get("ROLES")
        def say(nm):
            if GR is not None and nm in GR["ID"]:
                return role_info(GR, GR["ID"][nm])["say"]
            return str(nm)
        ctx = (m or {}).get("ctx") or {}
        def who(sl):
            p = ctx.get("_p_" + str(sl)) if sl else None
            return p["name"] if p is not None and p.get("name") and p.get("alive", True) else f"their {sl}" if sl else "someone close"
        has = np.asarray(loc["r_has"][0], bool) if loc is not None and GR is not None and "r_has" in loc else None
        def held(nm):                                   # None: not known (no catalogue), so it is said
            if has is None:
                return None
            if nm.startswith("kind:"):
                return any(has[i] and GR["kindname"][i] == nm[5:] for i in range(min(len(has), len(GR["kindname"]))))
            i = GR["ID"].get(nm)
            return None if i is None or i >= len(has) else bool(has[i])
        P_ = loc.get("P") if loc is not None else None
        gate = P_ is None or bool(P_.get("title_ages", True))
        def too_young_or_old(nm):                       # the Engine gives a title or perk only inside its ages
            i = GR["ID"].get(nm) if GR is not None and gate and "ages" in GR else None
            return i is not None and not (GR["ages"][i][0] <= self.t / 52 <= GR["ages"][i][1])
        GAIN = dict(title="becomes {}", grants="gains {}", title_if_fails="becomes {}")
        LOSE = dict(drops="leaves {} behind", takes="gives up {}", takes_if_fails="loses {}", drops_if_fails="loses {}",
                    suspends_if_fails="loses {} for a while")
        def phrase(f_, x):
            if f_ == "break":
                return f"breaks with {who(x)}"
            if x.startswith("kind:"):
                return "loses " + KIND_SAY.get(x[5:], "their " + x[5:])
            return (GAIN.get(f_) or LOSE[f_]).format(say(x))
        def side(fields):
            out = []
            for f_ in fields:
                for x in _as_list(row.get(f_)):
                    h = held(x) if f_ != "break" else None
                    if (f_ in GAIN and (h is True or too_young_or_old(x))) or (f_ in LOSE and h is False):
                        continue                        # nothing would change
                    out.append((f_, x))
            return out
        names = dict(win=side(("title", "grants", "drops", "takes")),
                     cost=side(("takes_if_fails", "drops_if_fails", "title_if_fails", "suspends_if_fails", "break")))
        def course(nm):                                 # F16: a title that would start a partnership, children or a faith
            i = GR["ID"].get(nm) if GR is not None else None   # the life course can still turn down (its own chance)
            k = GR["kindname"][i] if i is not None else None
            return k in ("partner", "children", "faith") and held("kind:" + k) is False
        names["course"] = [x for f_, x in names["win"] + names["cost"] if f_ in GAIN and course(x)]
        win = _as_list(row.get("win_say")) or [phrase(f_, x) for f_, x in names["win"]]
        cost = _as_list(row.get("cost_say")) or [phrase(f_, x) for f_, x in names["cost"]]
        return win, cost, names

    def _bold_options(self, loc, cp):
        """The bold ways (up to two) on a card the Engine offered them for: one more option each, after the moment's
        own. Their own pick is the bold way when the character took one."""
        L = loc["L"]; s = cp["s"]; bi = cp["by_idx"]
        own0 = int(cp["own"])
        bp = self._bold_pick
        mine = next((b for i, b in enumerate(self._bold_now) if int(b.get("slot", i)) == bp), None) if bp >= 0 else None
        own = BOLD_IX + 100 * bp + int(mine["base"]) if mine is not None else own0
        bp = bp if mine is not None else -1
        new = []
        for j_, b in enumerate(self._bold_now):
            j = int(b.get("slot", j_))
            base = int(b["base"])
            bo = bi.get(base)
            if bo is None or bo["colors"] == "-" or b.get("p") is None:
                continue                                # a bold way grows from a way on the card, never from waiting; only the
                # slots the Engine offers (their own odds set: the step rule held and the ages fit what it wins)
            row = self._bold_row(L, b.get("row", -1))
            k = BOLD_IX + 100 * j + base
            col = row.get("colour") or row.get("color") or row.get("colors") or bo["colors"]
            col = "+".join(col) if isinstance(col, (list, tuple)) else str(col)
            label = self.story.fill_label(str(b.get("label") or row.get("label") or bo["label"]), cp["moment"])
            chance = float(b.get("chance", row.get("chance", bo["felt"])))
            p = float(np.clip(b["p"], 0.1, 0.9))
            rel = 0.0 if k == own else max(float(bo["rel"]) if base != own0 else 0.0, GAME["bold_rel"])
            pt = p
            if k != own:
                lg = np.log(p / (1 - p)) - GAME["effort"] * rel - (GAME["out_of_reach"] if bo["status"] == "out of reach" else 0)
                pt = float(1 / (1 + np.exp(-lg)))
            fit = None if abs(p - chance) < GAME["bold_hint"] else "likelier" if p > chance else "harder"
            win, cost, names = self._bold_stake(L, row, cp["moment"], loc)
            o = dict(bo, idx=k, label=label, colors=col, felt=chance, true=pt, true0=p, hint=hint(pt - chance), rel=rel,
                     acc="their own pick" if k == own else accept_word(rel), lean=0.0,
                     clash=clash_with(col, self._prev_label), commit=None, follows=bo.get("follows") or {},
                     bold=dict(slot=j, row=int(b.get("row", -1)), base=base, raw=str(b.get("label") or row.get("label") or ""), chance=round(chance, 3), p=round(p, 3), fit=fit,
                               fit_say=BOLD_WORDS.get(fit) if fit else None, win=win, cost=cost, names=names))
            for x in ("reality", "heart", "head", "drivers", "needs", "closed", "helped", "lever", "rung", "base", "seen", "wcause"):
                o.pop(x, None)
            o["roles_fx"] = []
            sk = dict(o.get("at_stake") or {})          # Stakes on the card: the bold way's own lines first
            sk.pop("fails", None); sk.pop("risk", None)
            if win:
                sk["win"] = "; ".join(win)
            if cost:
                sk["cost"] = "; ".join(cost)
            if sk:
                o["at_stake"] = sk
            gone = bool(cp["moment"]["ctx"].get("_gone")) if cp.get("moment") else False
            works, fails = _as_list(row.get("works")), _as_list(row.get("fails"))
            if gone and row.get("works_gone") and row.get("fails_gone"):   # a link's person is gone: the lines that remember them
                works, fails = _as_list(row["works_gone"]), _as_list(row["fails_gone"])
            if works and fails:
                o["bold_lines"] = (works, fails)
            new.append(o)
        if not new:
            return
        if bp >= 0 and own in {o["idx"] for o in new}:  # they went bold themselves: the ordinary way is a push away
            cp["own"] = own
            ob = bi[own0]
            ob["rel"] = max(float(ob["rel"]), GAME["bold_rel"]); ob["acc"] = accept_word(ob["rel"])
            lg = np.log(ob["true0"] / (1 - ob["true0"])) - GAME["effort"] * ob["rel"]
            ob["true"] = float(1 / (1 + np.exp(-lg))); ob["hint"] = hint(ob["true"] - ob["felt"])
            o_ = next(o for o in new if o["idx"] == own)
            cp["thought"] = self.story.reason(o_["colors"].replace("+", "")) + " " + self.story.confidence(o_["felt"])
        for o in new:
            bi[o["idx"]] = o
        cp["options"] = cp["options"] + new
        cp["bold"] = [dict(o["bold"], idx=o["idx"], label=o["label"], colors=o["colors"]) for o in new]

    # ------------------------------------------------------------------ the outcome, and the Book
    def _bold_came(self, cpw, ev, new, age):
        """A bold way was played this week (or the card offered one and the player kept to an ordinary way): kept for
        the Book's Bold ways list and the outcome card, with what it changed for good (the role events through it)."""
        cp = cpw["cp"]
        if not cp.get("bold"):
            return None
        k = int(cpw["choice"]); own = int(cpw["own"])
        if k < BOLD_IX:
            if own >= BOLD_IX:                          # held back from a bold way they would have taken
                return dict(kind="held", line=self.story.fill("{N} keeps to the safer way."))
            return None
        o = cp["by_idx"][k]; b = o["bold"]
        ok = bool(ev["success"])
        eb = next((e_["bold"] for e_ in new if isinstance(e_.get("bold"), dict)), None)   # the Engine's record of the try
        changed = []                                    # what came through the bold act (the Engine's "through <label>"), and
        via = "through " + b["raw"]                     # any change the card named for it, however the Engine applied it
        said = {str(n) for _f, n in b["names"]["win"] + b["names"]["cost"]}
        kinds = {n[5:] for n in said if n.startswith("kind:")}
        for e_ in new:
            r = e_.get("role")
            named = r is not None and (r.get("name") in said or (r.get("what") == "lost" and r.get("kind") in kinds))
            if r and r.get("what") in ("gained", "lost", "suspended") and (named or b["raw"] and str(r.get("how", "")).startswith(via)):
                changed.append(dict(what=r["what"], name=r["name"], kind=r.get("kind")))
        rec = dict(t=int(self.t), age=round(age, 1), moment=cp["title"], act=o["label"], colors=o["colors"], chance=b["chance"],
                   p=b["p"], p_used=round(float(o["true"]), 4), row=b["row"], ok=ok, pushed=k != own, stated=b["names"], changed=changed,
                   engine=dict(eb) if eb else None)
        self.history.setdefault("bold", []).append(rec)
        self._bold_watch = dict(rec=rec, said=said, kinds=kinds, via=via, t_end=int(self.t) + 8)
        said = b["win"] if ok else b["cost"]
        line = ("" if not said else self.story.fill("For good: {N} " + "; ".join(said) + "."))
        return dict(kind="won" if ok else "lost", line=line, chance=b["chance"], p=b["p"], colors=o["colors"])

    def _bold_late(self, new):
        """A change a bold way gave that lands in the weeks after the try (a facet waits up to 8 weeks for the title it
        refines): added to the try's record, for the proof that the card's word holds."""
        bw = self._bold_watch
        if bw is None or int(self.t) <= bw["rec"]["t"]:
            return
        if int(self.t) > bw["t_end"]:
            self._bold_watch = None
            return
        for e_ in new:
            r = e_.get("role")
            if r and r.get("what") in ("gained", "lost", "suspended") and (r.get("name") in bw["said"] or (r.get("what") == "lost" and r.get("kind") in bw["kinds"])
                                                              or str(r.get("how", "")).startswith(bw["via"])):
                bw["rec"]["changed"].append(dict(what=r["what"], name=r["name"], kind=r.get("kind"), late=int(self.t) - bw["rec"]["t"]))

    def _bold_link_came(self, ret, cpw, ev, age):
        """A bold way's link was played: paired with its try in the Book's list."""
        if not ret.get("link"):
            return
        o = cpw["cp"]["by_idx"][cpw["choice"]]
        for x in reversed(self.history.get("bold", [])):
            if x["t"] == int(ret["t"]):
                x["link"] = dict(age=round(age, 1), moment=cpw["cp"]["title"], act=o["label"], ok=bool(ev["success"]),
                                 side=ret.get("side"), shared=bool(ret.get("change")))
                break

    def _bold_book(self):
        """The Book's Bold ways list: each try (taken, won or lost) with its link when one came."""
        out = []
        for x in self.history.get("bold", []):
            d = dict(a=x["age"], m=x["moment"], w=x["act"], c=x["colors"], ok=x["ok"], p=bool(x["pushed"]))
            if x.get("link"):
                d["l"] = dict(a=x["link"]["age"], m=x["link"]["moment"], ok=x["link"]["ok"])
            out.append(d)
        return out

    def _bold_ret(self, ret, sd):
        """Picks come back: a seed that is a bold way's link carries its side, its shared change, title and person."""
        if not sd.get("link"):
            return ret
        ret = dict(ret, link=True, side=sd.get("side") or ("well" if sd.get("ok") else "badly"), change=bool(sd.get("change")),
                   gone=bool(sd.get("gone")))
        if sd.get("title"):
            ret["title"] = sd["title"]
        return ret

    def _bold_link_line(self, ret, age):
        """The opener of a bold way's link: it names the bold try (the Library's THREAD["bold_link"] by side, else
        built-in words)."""
        yrs = int(age - ret["age"])
        years = "a year" if yrs < 2 else f"{yrs} years"
        T = (getattr(ES, "THREAD", None) or {}).get("bold_link") or {}
        side = "well" if ret["ok"] else "badly"
        line = T.get(side) if isinstance(T, dict) else T
        if not line:
            line = ("{Years} ago, at “{moment}”, {N} took the bold way: {act}. It worked, and this is where it led."
                    if ret["ok"] else "{Years} ago, at “{moment}”, {N} took the bold way: {act}. It went badly, and this is where it led.")
        fills = dict(Years=years[:1].upper() + years[1:], years=years, moment=ret["moment"], act=str(ret["act"]),
                     who=self.story.say(ret["who"]) if ret.get("who") else "someone", title=str(ret.get("title") or ""))
        for f_, v_ in fills.items():
            line = line.replace("{" + f_ + "}", v_)
        return self.story.fill(line)
