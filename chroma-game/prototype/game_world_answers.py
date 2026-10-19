"""Game's methods for the v24 world answers (chroma-world/spheres/world-answers-v1.md; plan section 6, Emren 10-19: "world
= forest, character = tree", and the tree can still move the forest), behind GAME world_answers, with the Engine's
world_answers switch and the batch's WORLD_ANSWERS. Words only: the Engine gives the world its answers; nothing here draws.

Part of class Game (game.py), which inherits WorldAnswersMixin. What it reads, from the Engine's played-life keys:
- the week's events: dict(wa_ledger=X), X one of
  - dict(told=dict(unit, size, who, age, cause=dict(acts, last, last_age))): a footprint in the world passed a step
    (D). unit is one of the shared unit keys (person_colours .. town_sphere, nation), size "a little", "clearly" or
    "a lot"; who names it: dict(cid) a person, dict(group, j) a setting, dict(place, kind) a place, dict(town, sphere)
    the town's sphere, dict(domain) the nation. cause.last is dict(moment, option) or a word ("being there").
  - dict(event=dict(event="sphere.key", age)): a sphere event in the goal's sphere in their town (E5).
  - dict(moment=dict(kind="world answers", key, sphere, answer, ...)): an ask (E4), a decision for others or a
    figure's moment (F), as it was answered.
- the run's wa_ledger (self.result, or the world's wa_output() at the end of a played life), lives[0]["rings"][ring] = dict(total, largest=dict(total, who), kept, level):
  what the world kept of each ring's largest footprint at the end (F5).
Lines are the Library's (earth_world_lines.py: BECAUSE, NATION, KEPT, CAUSE). Told in the story by size ("a lot" always,
"clearly" in the normal story, "a little" in the detailed one), all kept for the "Your world" panel, and the end of the
life reads back the largest footprint in each ring."""
import zlib

import story_base as SB
from game_base import ESP, GAME
from worldview import person_name

try:
    import earth_world_lines as WLN             # the Library's told lines (pinned next to the engine)
except ImportError:
    WLN = None

RINGS = ("person", "group", "place", "town_sphere", "nation")
RING_NAME = dict(person="People", group="Groups", place="Places", town_sphere="The town", nation="The country")
RING_OF = dict(person_colours="person", person_closer="person", person_further="person", person_trust_up="person",
               person_trust_down="person", group_norm="group", group_members="group", place_mix="place",
               place_founded="place", place_kept_open="place", town_sphere="town_sphere", nation="nation")
SIZE_LEVEL = {"a lot": 0, "clearly": 1, "a little": 2}   # the story's detail a told line needs
ACT_WORD = {"being there": "kept turning up", "leading it": "took the lead", "keeping it open": "kept it open",
            "holding out": "held out", "the years together": "shared the years", "a law passed": "pushed the law through"}
EVENT_AGAIN = 2 * 52                            # a sphere event in their goal's sphere: one every two years in the story
TOLD_FROM = 12                                  # a child's footprints wait in the panel (as setbacks, Emren 10-19)
TOLD_AGAIN = 52                                 # a "clearly" line, or a person's: one a ring a year in the story
PANEL_LINES = 40


def _pick(xs, *key):
    """One of the Library's variants, the same every time for the same footprint (no draw)."""
    return xs[zlib.crc32("|".join(str(k) for k in key).encode()) % len(xs)] if xs else ""


def _cap(s):
    return s[:1].upper() + s[1:]


class WorldAnswersMixin:
    def _wa_world(self):
        return self.setting if self.setting in ("earth", "tribal", "magic") else "earth"

    def _wa_names(self):
        return self.__dict__.setdefault("_wa_nm", {})

    def _wa_who(self, who, loc=None):
        """The words a told line's placeholders take for who: {friend}, {group}, {place}, {sphere_name}; cached by who, so
        the end's read-back names what the life named."""
        key = repr(sorted(who.items())) if isinstance(who, dict) else repr(who)
        nm = self._wa_names()
        if key in nm:
            return nm[key]
        out = {}
        if "cid" in who and getattr(self, "wv", None) is not None:
            out["friend"] = person_name(self.wv.seed, int(who["cid"]), False, self.setting) or "someone"
        if "group" in who:
            sp = getattr(ESP, "SETTING_PLACE", {}) if ESP is not None else {}
            out["group"] = sp.get(who["group"]) or f"the {who['group'] or 'group'}"
        if "place" in who:
            WL = (loc if loc is not None else self.loc or {}).get("WL")
            w_ = ""
            if WL is not None:
                try:
                    w_ = self._place_word(WL.W.place_info(int(who["place"])))
                except Exception:
                    w_ = ""
            out["place"] = w_ or "a place of theirs"
        if "sphere" in who:
            s_ = ((ESP.SPHERE.get(who["sphere"]) or {}).get("name") if ESP is not None else None) or str(who["sphere"])
            out["sphere_name"] = s_.lower()
        nm[key] = out
        return out

    def _wa_fill(self, text, who, loc=None):
        for k, v in self._wa_who(who, loc).items():
            text = text.replace("{" + k + "}", v)
        return _cap(self.story.fill(text))

    def _wa_cause(self, cause):
        """Since when, in the Library's words: "since Ari chose to start a reading group, at 34"; "" without a cause."""
        last = (cause or {}).get("last")
        if last is None or WLN is None or "last_age" not in cause:
            return ""
        if isinstance(last, dict):
            op = str(last.get("option") or "")
            if not op or "{" in op or op == "do nothing":
                act = f"faced {last.get('moment') or 'a choice'}"
            else:
                act = "chose " + SB.chooses(SB.act(op[:1].lower() + op[1:]))
        else:
            act = ACT_WORD.get(str(last), "kept at it")
        w = self._wa_world()
        tpl = _pick(WLN.CAUSE.get(w) or WLN.CAUSE["earth"], act, cause["last_age"])
        out = self.story.fill(tpl.replace("{act}", act).replace("{age}", str(int(cause["last_age"]))))
        return out[:1].lower() + out[1:]

    def _wa_line(self, ln, loc=None):
        """A told footprint as one line, with its cause; "" when the Library has no line for it."""
        if WLN is None:
            return ""
        w, unit, size, who = self._wa_world(), ln["unit"], ln["size"], ln.get("who") or {}
        if unit == "nation":
            xs = (WLN.NATION.get(who.get("domain")) or {})
            xs = xs.get(w) or xs.get("earth") or []
        else:
            xs = ((WLN.BECAUSE.get(unit) or {}).get(size) or {})
            xs = xs.get(w) or xs.get("earth") if isinstance(xs, dict) else xs
        tpl = _pick(xs or [], unit, size, ln.get("age"), repr(who))
        if not tpl:
            return ""
        text = self._wa_fill(tpl, who, loc)
        cz = self._wa_cause(ln.get("cause")) if unit != "nation" else ""   # the country: by what it visibly did, no act
        return f"{text.rstrip('.')}, {cz}." if cz else text

    def _wa_week(self, new, loc):
        """This week's world answers, from the week's new events: each told footprint as a line (kept in
        history["wa"]), keyed by the event, for the story's loop (_wa_told) and the pick's card. [] when off."""
        self._wa_items = {}
        if not GAME["world_answers"]:
            return []
        out = []
        for ev in new:
            x = ev.get("wa_ledger")
            if not isinstance(x, dict) or "told" not in x:
                continue
            ln = x["told"]
            text = self._wa_line(ln, loc)
            if not text:
                continue
            it = dict(age=round(float(ln.get("age", self.age())), 1), ring=RING_OF.get(ln["unit"], "person"), unit=ln["unit"],
                      size=ln["size"], text=text)
            self.history.setdefault("wa", []).append(it)
            self._wa_items[id(ev)] = it
            out.append(it)
        return out

    def _wa_told(self, t, x, ev=None):
        """One wa_ledger event in the story's loop: a footprint by its size, a sphere event in their goal's sphere (E5),
        or how a decision for others was taken."""
        it = (getattr(self, "_wa_items", None) or {}).get(id(ev)) if ev is not None else None
        lvl0 = int(self.burn_in)
        if it is not None:
            lv = SIZE_LEVEL.get(it["size"], 2)
            told = self.__dict__.setdefault("_wa_ring_t", {})
            often = lv == 1 or it["ring"] == "person"   # people's lines come often: one a year; a lot elsewhere always
            if it["age"] < TOLD_FROM or often and t - told.get(it["ring"], -10 ** 6) < TOLD_AGAIN:
                lv = 2                                  # the rest wait in "Your world" and the detailed story
            if lv <= 1:
                told[it["ring"]] = t
            self._say(it["text"], lv + lvl0, "world_answer", ring=it["ring"], size=it["size"])
        elif "event" in x and ESP is not None:
            k_ = x["event"].get("event") if isinstance(x["event"], dict) else x["event"]
            e_ = ESP.EVENT.get(str(k_)) or {}
            told = self.__dict__.setdefault("_wa_ev_t", {})
            sp = str(k_).split(".")[0]
            if not e_.get("line") or t - told.get(sp, -10 ** 6) < EVENT_AGAIN:
                return
            told[sp] = t
            self._say(e_["line"], 1 + lvl0, "world_answer_event", sphere=sp, name=e_.get("name", ""))
            self.history.setdefault("wa_events", []).append(dict(age=round(t / 52, 1), sphere=sp, name=e_.get("name", "")))
        elif "moment" in x:
            m_ = x["moment"]
            self.history.setdefault("wa_moments", []).append(dict(age=m_.get("age"), key=m_.get("key"), sphere=m_.get("sphere"),
                                                                  answer=m_.get("answer"), scope=m_.get("scope")))
            told = self.__dict__.setdefault("_wa_ring_t", {})
            if m_.get("key") == "decide" and m_.get("answer") == "decided" and "fair" in m_ and \
                    t - told.get("fair", -10 ** 6) >= TOLD_AGAIN:   # 4 to 8 decisions a year: how one landed, once a year
                told["fair"] = t
                self._say("Most people in town thought it fair." if m_["fair"] else "Not everyone in town thought it fair.",
                          1 + lvl0, "world_answer", ring="town_sphere", size="")

    def wa_card(self, xs):
        """After a pick: the world lines it left this week, the largest first (at most two), for "Because of you"."""
        xs = sorted(xs, key=lambda x: SIZE_LEVEL.get(x["size"], 2))
        return [x["text"] for x in xs if x["size"] != "a little"][:2]

    def wa_view(self):
        """The "Your world" panel: per ring, how many footprints were told and the newest line; the newest lines; the
        decisions taken for others and the asks. None when off."""
        if not GAME["world_answers"]:
            return None
        h = self.history.get("wa", [])
        rings = []
        for r in RINGS:
            xs = [x for x in h if x["ring"] == r]
            rings.append(dict(ring=r, name=RING_NAME[r], n=len(xs), line=xs[-1]["text"] if xs else ""))
        ms = self.history.get("wa_moments", [])
        return dict(rings=rings, lines=[dict(age=x["age"], ring=x["ring"], size=x["size"], text=x["text"]) for x in reversed(h[-PANEL_LINES:])],
                    asked=sum(1 for m in ms if str(m.get("key", "")).startswith("asked_")),
                    decided=sum(1 for m in ms if m.get("key") == "decide" and m.get("answer") == "decided"))

    def wa_kept(self):
        """At the end (F5): what the world kept of the largest footprint in each ring the life was told about, in the
        Library's KEPT words: [dict(ring, level, text)]; [] when off or before the end."""
        if not GAME["world_answers"] or WLN is None or not getattr(self, "over", False):
            return []
        o = self.result if isinstance(self.result, dict) else {}
        try:
            if "wa_ledger" in o:
                rings = o["wa_ledger"]["lives"][0]["rings"]
            else:                                       # a played life ends without the run's result: the world's own read
                WL = (self.loc or {}).get("WL")
                rings = WL.wa_output()["lives"][0]["rings"] if WL is not None and getattr(WL, "wa_on", False) else None
        except (KeyError, IndexError, TypeError, AttributeError):
            rings = None
        if not rings:
            return []
        told = {x["ring"] for x in self.history.get("wa", [])}
        w, out = self._wa_world(), []
        for r in RINGS:
            rr = rings.get(r) or {}
            lg, lv = rr.get("largest"), rr.get("level")
            if r not in told or not lg or lv is None:
                continue
            xs = ((WLN.KEPT.get(r) or {}).get(lv) or {})
            tpl = _pick(xs.get(w) or xs.get("earth") or [], r, lv, repr(lg.get("who")))
            who = lg.get("who") or {}
            if not tpl or ("{place}" in tpl and repr(sorted(who.items())) not in self._wa_names() and self.loc is None):
                continue
            out.append(dict(ring=r, level=lv, text=self._wa_fill(tpl, who)))
        return out
