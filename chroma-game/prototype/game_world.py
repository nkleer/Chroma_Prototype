"""Game's methods for the outer world in the story: world effects, levers, far ties, places, posts, lines, talks, the seen and social slots.

Part of class Game (game.py), which inherits WorldMixin; moved out of game.py verbatim. A method here reads
module names through the imports below, the same objects game.py has, and self for everything on the Game."""
import re
from game_base import (COLORS, ES, ESP, EngineWorld, GAME, LIB_READ, mk, plain, who_word)
from game_words import (FAIR_SIDE, FAR_AGAIN, FAR_SAY, HOME_UNTIL, LEAD_COLOUR, LEVER_AGAIN, SEEN_MARK, SEEN_ROW,
    SPH_LEVER, TALK_AGAIN, TALK_QUIET, WFX_AGAIN, WFX_BAND, WFX_CAUSE, WFX_KIND, WFX_KIND_LIB, cap_first, lead_words)


class WorldMixin:
    # ------------------------------------------------------------------ item 11: the world in their life (WL1, WL3 to WL6)
    @staticmethod
    def _wband(ch, size):
        """WL1's bands (the Library's proposal, set here): None (not told), "small" or "big"."""
        size = abs(float(size))
        if ch == "option":
            return "big"
        lo, hi = WFX_BAND.get(ch, WFX_BAND["risk"] if ch.endswith("risk") else (None, None))
        if lo is None or size < lo:
            return None
        return "big" if size >= hi else "small"

    @staticmethod
    def _wcause_text(c, kind):
        """A world effect's cause in plain words, for the hover: "the recession, since 34"."""
        if not c:
            return WFX_KIND.get(kind, kind)
        ck = c.get("kind")
        key = c.get("key")
        nm = (f"the {key}" if key and ck == "arrives" else key) or WFX_CAUSE.get(ck) or WFX_KIND.get(ck) or WFX_KIND.get(kind, kind)
        return str(nm) + (f", since {int(c['age'])}" if c.get("age") is not None else "")

    def _world_effects(self, t, loc):
        """WL1 and WL5 (item 11, world-in-life.md): when the engine reports that a world event changed something of theirs
        (STATE wfx: money, freedom, safety, a risk, a close person, their town), one small line sized to the change, the
        cause on hover; the same kind of line not again within a year. Each told effect goes into the life's record of what
        the times did (the World panel) and the year's line (WL4)."""
        if ES is None or "wfx" not in loc:
            return
        W = loc["wfx"]
        xs = W[0] if len(W) and isinstance(W[0], (list, tuple)) else W
        home = self._young_home(loc)
        for e in xs or []:
            ch, kind, d = e.get("channel", ""), e.get("kind", ""), e.get("dir", "up")
            band = self._wband(ch, e.get("size", 0))
            if band is None or ch == "moment":
                continue
            k = WFX_KIND_LIB.get(kind, kind)
            if home and ch in ES.WORLD_HOME_CHANNEL:      # F5: a child hears the money times through the home
                line = (((ES.WORLD_HOME.get(k) or {}).get(ch) or {}).get(d, {}).get(band)
                        or (ES.WORLD_HOME_CHANNEL.get(ch) or {}).get(d, {}).get(band))
            else:
                line = ((ES.WORLD.get(k) or {}).get(ch) or {}).get(d, {}).get(band) or (ES.WORLD_CHANNEL.get(ch) or {}).get(d, {}).get(band)
            if not line:
                continue
            key = (kind, ch, d)
            yk = abs(float(e.get("size", 0))) / (WFX_BAND.get(ch, WFX_BAND["risk"])[1] if ch != "option" else 1.0)
            self._wyear[key] = self._wyear.get(key, 0.0) + min(yk, 2.0)
            lc_ = self.__dict__.setdefault("_wfx_ch", {}).get(ch) if GAME["line_wait"] else None
            if t - self._wfx_t.get(key, -10 ** 6) < WFX_AGAIN or \
                    (lc_ is not None and lc_[1] != d and t - lc_[0] < WFX_AGAIN and band != "big"):
                # counted for the year's line, not told again; F10 (line_wait on): nor a small turn the other way in a
                # channel told within the year (the times took from their pocket, then put a little back)
                self.history["times"].append(dict(age=round(t / 52, 1), kind=k, channel=ch, dir=d, told=False))
                continue
            self._wfx_t[key] = t
            if GAME["line_wait"]:
                self._wfx_ch[ch] = (t, d)
            cause = self._wcause_text(e.get("cause"), kind)
            text = self.story.fill(line.replace("{who}", "someone close to them"))
            self._say(mk("X", f"{k}|{ch}|{d}|{band}|{cause.replace('|', '/')}", text), 0 if band == "big" else 1, "world_fx",
                      kind=k, channel=ch, dir=d, band=band, cause=cause)
            self.history["times"].append(dict(age=round(t / 52, 1), text=plain(text), kind=k, channel=ch, dir=d, cause=cause, big=band == "big"))

    def _young_home(self, loc):
        """F5 (v22.4.1): a child or juvenile (stage below young adult, as states() reads it) under HOME_UNTIL hears the
        money times and the grown-ups' work worries through the home, in the Library's WORLD_HOME and YEAR_WHAT_HOME words
        (pins without them: as before). The engine's juvenile stage runs to the mid-twenties, past the age most have
        their own pay and rent, so the age bounds it too."""
        return (loc is not None and "stage" in loc and int(loc["stage"][0]) < 2 and self.t / 52 < HOME_UNTIL
                and getattr(ES, "WORLD_HOME", None) is not None and getattr(ES, "YEAR_WHAT_HOME", None) is not None)

    def _times_year(self):
        """WL4: the year's one line on how the times touched them: close (a disaster, war, their town or a close person),
        else mixed (the two largest point opposite ways), else by the largest; what, from the two largest. With item 6 on
        (GAME lines_tied) it is not said: it returns (marker payload, clause) for the year's lead (story.chapter)."""
        y, self._wyear = self._wyear, {}
        if ES is None or not y or self.burn_in or sum(y.values()) < 1.0:
            return                                       # a year the times really touched them: one big change or a few small
        items = sorted(y.items(), key=lambda kv: -kv[1])[:2]
        good = lambda ch, d: (d == "up") == (not ch.endswith("risk"))
        if any(ch in ("home", "close person") or WFX_KIND_LIB.get(k, k) in ("disaster", "war") for (k, ch, d) in y):
            tone = "close"
        elif len(items) == 2 and good(*items[0][0][1:]) != good(*items[1][0][1:]):
            tone = "mixed"
        else:
            (k, ch, d), _ = items[0]
            tone = (("easier" if d == "up" else "lean") if ch in ("money", "time", "health", "ties") else
                    ("freer" if d == "up" else "narrower") if ch in ("freedom", "option") else
                    ("calmer" if d == "up" else "uneasy") if ch == "safety" else ("uneasy" if d == "up" else "calmer"))
        whats = []
        home = self._young_home(self.loc)
        for (k, ch, d), _ in items:
            if home and ch in ES.YEAR_WHAT_HOME_CHANNEL:    # F5: the year's clause through the home, while young
                w_ = (((ES.YEAR_WHAT_HOME.get(WFX_KIND_LIB.get(k, k)) or {}).get(ch) or {}).get(d)
                      or (ES.YEAR_WHAT_HOME_CHANNEL.get(ch) or {}).get(d))
            else:
                w_ = ((ES.YEAR_WHAT.get(WFX_KIND_LIB.get(k, k)) or {}).get(ch) or {}).get(d) or (ES.YEAR_WHAT_CHANNEL.get(ch) or {}).get(d)
            if w_ and w_ not in whats:
                whats.append(w_.replace("{who}", "someone close to them"))
        last = getattr(self, "_wyear_said", (None, -99))
        if whats and tone in ES.YEAR and not (last[0] == (tone, tuple(whats)) and self.t - last[1] < 3 * 52):
            self._wyear_said = ((tone, tuple(whats)), int(self.t))
            lead = getattr(ES, "YEAR_LEAD", None) if GAME["lines_tied"] else None
            if lead and tone in lead:                    # item 6: one clause in the year's lead, its hover the largest
                (k, ch, d), _ = items[0]
                return f"{WFX_KIND_LIB.get(k, k)}|{ch}|{d}|year|", lead[tone].replace("{what}", " and ".join(whats))
            self._say(self.story.fill(ES.YEAR[tone].replace("{what}", " and ".join(whats))), 0, "world_year", tone=tone)

    def _disaster_read(self, r):
        """WL6 (item 11): "a disaster in the next town" told as the disaster that happened, by the engine's hazard and
        where tags (Library DISASTER_READ): its scene, and the same color's reading in that disaster's words."""
        D = getattr(ES, "DISASTER_READ", None) if ES else None
        if not D or not r.get("hazard") or r["hazard"] not in D:
            return r
        d = D[r["hazard"]].get(r.get("where") or "near") or D[r["hazard"]].get("near")
        ev = LIB_READ.get(r["name"]) or {}
        c = next((x[4] for x in ev.get("readings", ()) if x[0] == r.get("reading")), None)
        if not d or c not in d:
            return r
        return dict(r, _scene=d.get("scene", ""), reading=d[c][0], say=d[c][1])

    def _read_color(self, r):
        """Item 6: the color a reading pulls their wanting toward (the engine takes in its want, engine.py's read events),
        from the batch's outside events by name and reading; "" when the library has none."""
        M = self.__dict__.setdefault("_read_want", {})
        if not M:
            for e in self.L.get("EVR") or []:
                for lab, w_ in zip(e["labels"], e["want"]):
                    M.setdefault((e["name"], lab), COLORS[int(w_)])
            M.setdefault(None, "")
        return M.get((r.get("name"), r.get("reading", "")), "")

    def _option_cause(self, cs):
        """WL3: the world's biggest reason an option is closed, harder or easier (engine option_causes), as the Library's
        note, and the cause's own name for the hover."""
        c = max(cs, key=lambda c_: abs(float(c_.get("size", 0) or 0)))
        how = c.get("how", "harder")
        h = "closed" if how in ("banned", "not there", "out of reach") else "easier" if how in ("allowed", "easier") else "harder"
        k = c.get("kind") if c.get("kind") in ("law", "norm", "technology") else "norm" if how == "frowned on" else "odds"
        note = (getattr(ES, "OPTION_CAUSE", {}).get(k) or {}).get(h) if ES else None
        if not note:
            return None
        return dict(note=note, how=h, hover=cap_first(self._wcause_text(c.get("cause"), c.get("key") or c.get("kind", ""))
                                                       if c.get("cause") else str(c.get("key") or c.get("kind", ""))) + f" ({how})")

    def world_panel(self):
        """The player's world panel: public facts now and the history so far, by age and era (spec 1 §8); with WL5's record
        of what the times did to them, and P3's steers against the era, for the timeline."""
        wd = self.world_data()
        if not wd:
            return None
        p = self.wv.panel(wd[0], wd[1], self.age())
        if isinstance(p, dict):
            p["times"] = [x for x in self.history.get("times", []) if x.get("told", True)][-60:]
            p["steers"] = self.history.get("steers", [])[-200:] if GAME["world_steers"] else []
            if GAME["land_row"]:                        # v25: the portrait's land row
                p["land"] = self.land_line((wd[0] or {}).get("place"))
            if GAME["prizes"]:                          # v25: what this world prizes, for the life's town
                p["prizes"] = self.prizes_view()
            if self.history.get("levers"):              # spheres phase 4: their lever acts on the town's spheres
                p["levers"] = self.history["levers"][-200:]
        return p

    # ------------------------------------------------------------------ spheres phase 4 and far ties: told, display only
    # (PRs #84 and #95, world-fields.md). They read the engine's events and the world as it stands; they draw no dice and
    # write nothing the engine reads. With sph_levers and far_ties off the engine logs none of these events.
    def _lever_where(self, loc, r):
        """Where a lever landed: their place in that sphere, by the Library's name for it as "their places" shows it (else
        the engine's place name in the world's epoch), or else the town's sphere."""
        WL = loc.get("WL")
        if int(r.get("place", -1)) >= 0 and WL is not None:
            try:
                h = WL.W.place_info(int(r["place"]))
                ns = ((ESP.HAUNT.get(h["kind"]) or {}).get("names") or []) if ESP is not None else []
                if ns:
                    return ns[h["name"] % len(ns)]
                import sphere_data as SD
                nm = (SD.PLACE_BY_EPOCH.get(h["kind"]) or {}).get(WL.W.sph_epoch)
                if nm:
                    return nm
            except Exception:
                pass
        return SPH_LEVER["sphere"].get(r.get("sphere"), "the town")

    def _lever_told(self, t, loc, r):
        """Spheres phase 4 (sph_levers): their lever act on their town's sphere (the engine's sphere_lever record) told as
        theirs: what they pushed, where it landed and whether it moved, backfired or set off an event. Nothing at all is
        quiet (the detailed story); the same lever on the same sphere within LEVER_AGAIN too. Kept for the World panel."""
        lv, sp, moved = r.get("lever", ""), r.get("sphere", ""), str(r.get("moved") or "none")
        act = SPH_LEVER["act"].get(lv)
        if not act:
            return
        head, _, rest = moved.partition(" ")
        went = ("fired" if head == "fired" else "state") if rest else moved if moved in ("moved", "backfired") else "none"
        what = SPH_LEVER["what"].get(rest, rest.replace("_", " ").replace(".", " "))
        where = self._lever_where(loc, r)
        tail = SPH_LEVER["moved"].get(lv, SPH_LEVER["moved"]["voice"]) if went == "moved" else SPH_LEVER[went].replace("{what}", what)
        text = self.story.fill(act.replace("{where}", where) + tail)
        came, rung = SPH_LEVER["came"][went], str(r.get("rung") or "")
        if ESP is not None:                             # the Library's words: the event set off, their rung in that sphere
            ev_ = (ESP.EVENT.get(f"{sp}.{rest}") or {}).get("name") if went == "fired" else None
            came = f"{came}: {ev_.lower()}" if ev_ else came
            LADDER = ["newcomer", "regular", "known", "pillar", "leader"]       # world_keys.LADDER, the engine's order
            rung = ESP.RUNG[sp][LADDER.index(rung)] if sp in ESP.RUNG and rung in LADDER else rung
        told = self.__dict__.setdefault("_lever_t", {})
        lvl = 0 if went in ("fired", "state") else 2 if went == "none" else 1
        if lvl == 1 and t - told.get((lv, sp), -10 ** 6) < LEVER_AGAIN:
            lvl = 2
        if lvl <= 1:
            told[(lv, sp)] = t
        self._say(mk("L", f"{lv}|{where}|{came}|{rung}", text), lvl + int(self.burn_in), "lever", lever=lv, sphere=sp, went=went)
        if went != "none" or float(r.get("size") or 0) > 0:     # an act with no reach at all (a child's) stays off the panel
            self.history.setdefault("levers", []).append(dict(age=round(t / 52, 1), lever=lv, sphere=sp, where=where, went=went,
                                                              came=came, rung=rung, text=plain(text)))

    def _far_town(self, loc, l_):
        """A town of their society by its name (as the World panel and the story name places)."""
        from worldview import place_name, loc_key
        WL = loc.get("WL")
        return place_name(self.wv.seed, loc_key(EngineWorld.soc(WL) if WL is not None else 0, int(l_)), self.setting)

    def _cast_who(self, cid):
        """A cast member as a world line names them ("their sister Mira"), and their name alone; None without a world."""
        wd = self.world_data()
        if not wd:
            return None
        from worldview import person_name
        p = next((c_ for c_ in wd[2] if c_.get("id") == cid), {})
        nm = self.cast_names(wd[2]).get(cid) or person_name(self.wv.seed, cid, False, self.setting)
        return who_word(p, nm), nm

    def _far_told(self, t, loc, c):
        """far_ties (PR #95): a close tie's news from the town they live in (cast event "far"), a tie taken into the
        household and how their stay ends ("taken in"); a want's cause (F5) is kept for the circle's hover."""
        kind, cid = c.get("kind"), int(c.get("cid", -1))
        if kind == "want":                                   # every want event passes here; only one with a cause is kept
            if c.get("cause"):
                self.__dict__.setdefault("_want_why", {})[cid] = (c.get("key"), c["cause"])
                self.__dict__.setdefault("_far_seen", {})[cid] = c["cause"]
            elif c.get("state") == "begins" and self.__dict__.get("_want_why"):
                self._want_why.pop(cid, None)
            return
        seen = self.__dict__.setdefault("_far_seen", {})     # cid -> the last far cause told or wanted (where they came from)
        who = self._cast_who(cid)
        if who is None:
            return
        w_, nm = who
        if kind == "far":
            cs = c.get("cause") or {}
            seen[cid] = cs
            sign = cs.get("sign") if cs.get("sign") in ("good", "hard", "mixed") else "mixed"
            text = (FAR_SAY["here" if c.get("here") else "away"][sign].replace("{town}", self._far_town(loc, cs.get("town", 0)))
                    .replace("{event}", cs.get("far_event") or "something happened"))
            lines = "; ".join(str(x_) for x_ in cs.get("line") or ())
            told = self.__dict__.setdefault("_far_t", {})
            lvl = 2 if c.get("here") or t - told.get(cid, -10 ** 6) < FAR_AGAIN else 1
            if lvl <= 1:
                told[cid] = t
            self._say(mk("F", f"{sign}|{nm}|{lines}", self._far_fill(text, w_)), lvl + int(self.burn_in), "far", kind="far",
                      sign=sign, here=bool(c.get("here")))
        elif kind == "taken in":
            st = c.get("state")
            if st is None:
                text = FAR_SAY["took"]
            elif st == "went back":
                l_ = (seen.get(cid) or {}).get("town")
                text = FAR_SAY["back"].replace("{town}", f" to {self._far_town(loc, l_)}" if l_ is not None else "")
            else:
                text = FAR_SAY["stayed"]
            self._say(self._far_fill(text, w_), (0 if st is None else 1) + int(self.burn_in), "far", kind="taken in", state=st or "")

    def _far_fill(self, text, who):
        """A far line with the tie named: their name at the start of a sentence capitalised, no comma before a stop."""
        return re.sub(r",([.:])", r"\1", cap_first(self.story.fill(text.replace("{who}", who))))

    def _far_moment(self, m, loc, s, ev=None):
        """A far moment (the Library's earth-far-ties.lib: cast_want far_hard, far_good or far_mixed) names the tie who
        calls in its first who: slot, {their_town} and {far_event}, from the engine's word on the call: the logged event's
        who and far, or, at a checkpoint, the call waiting on this moment (world_link pending, far_info; read only)."""
        if m is None or not self.batch or "far_event" in m["ctx"]:
            return
        if not str(self.L["src"][s].get("cast_want") or "").startswith("far_"):
            return
        WL = loc.get("WL")
        fi, slot, cid = None, None, None
        if ev is not None:
            fi = ev.get("far")
            slot, cid = next(iter((ev.get("who") or {}).items()), (None, None))
        elif WL is not None:
            fi = WL.far_info(0, s)
            pv = WL.pending.get(0)
            cid = int(pv[0]) if pv is not None and pv[2] == s else None
            slot = next(iter((self.L.get("W_WHO") or {s: ()})[s] or ()), None)
        if not fi:
            return
        m["ctx"]["their_town"] = self._far_town(loc, (fi.get("their_town") or {}).get("loc", fi.get("town", 0)))
        m["ctx"]["far_event"] = fi.get("far_event") or "something happened there"
        who = self._cast_who(int(cid)) if slot and cid is not None else None
        if who is not None and "_p_" + slot not in m["ctx"]:
            m["ctx"][slot] = who[1]

    # ------------------------------------------------------------------ v22.4's social mechanics (S1, S3 to S7): display only
    def _pron(self):
        """The character's object and possessive pronoun, by the gender they live as (N1d): her, him or them."""
        try:
            g = self.gender_view()["self"] if self.loc is not None else None
        except Exception:
            g = None
        return {"f": ("her", "her"), "m": ("him", "his")}.get(g, ("them", "their"))

    def _place_word(self, p):
        """A place of theirs by its plain name: a haunt by the Library's name for it ("the Curtain Call"), a setting's
        place by its own ("the house of worship"); "" for none."""
        if not isinstance(p, dict) or ESP is None:
            return ""
        if isinstance(p.get("place"), str):
            return p["place"]
        k = p.get("kind")
        if k is None:
            return ""
        ns = (ESP.HAUNT.get(k) or {}).get("names") or [(ESP.PLACE.get(k) or {}).get("name", "")]
        return str(ns[int(p.get("name", 0)) % len(ns)]) if ns and ns[0] else ""

    def _name_word(self, rep):
        """S3: their name at a place in the Library's words (earth_spheres.PLACE_NAME), from the engine's rep (-1 to 1)."""
        pn = getattr(ESP, "PLACE_NAME", None) or [(-1, "known")]
        return next((w for r, w in pn if float(rep) >= r), pn[-1][1])

    def _read_clause(self, face, act, side):
        """S3: how a place read an act (earth_spheres.READ "face.act", gift or danger): a clause after "thinks you"."""
        if not face or not act or side not in ("gift", "danger"):
            return ""
        return (getattr(ESP, "READ", {}).get(f"{face}.{act}") or {}).get(side, "")

    def _fair_lines(self, PP):
        """S1 (fair_read): per sphere that reads fair or unfair to them, the line for its hover in "their places": "Feels
        unfair to her: the council decided behind closed doors and gave no reason." Unfair names the part that pulls it
        down most, fair the part that holds it up most. None while the switch is off."""
        fi = PP.fair_info(0) if hasattr(PP, "fair_info") and ESP is not None else None
        if not fi:
            return None
        obj = self._pron()[0]; out = {}
        FP, FS = getattr(ESP, "FAIR_PART", {}), getattr(ESP, "FAIR", {})
        for sp, d in fi.items():
            f_, parts = float(d.get("fair", 0.5)), d.get("parts") or {}
            if f_ < FAIR_SIDE[0]:
                side, part = "unfair", d.get("weakest") or (min(parts, key=parts.get) if parts else None)
            elif f_ > FAIR_SIDE[1]:
                side, part = "fair", max(parts, key=parts.get) if parts else None
            else:
                continue
            w = (FS.get(f"{sp}.{part}") or FP.get(part) or {}).get(side)
            if w:
                out[sp] = dict(side=side, part=(FP.get(part) or {}).get("name", part), line=f"Feels {side} to {obj}: {w}.")
        return out or None

    def _eyes_word(self, e):
        """S3, S4: one place's eyes on them, for its hover: their name there, its last word on what they did (the
        reading as a clause), a go-between there, and with sph_odd whether they are the odd one out, blended in or held on."""
        d = dict(rep=round(float(e.get("rep", 0.0)), 2), name_word=self._name_word(e.get("rep", 0.0)),
                 read=self._read_clause(e.get("face"), e.get("act"), e.get("side")), go=bool(e.get("go_between")))
        if "odd" in e:
            d.update(odd=bool(e["odd"]), blended=bool(e.get("blended")), held=bool(e.get("held")))
        return d

    def _social_places(self, WL, hi, P):
        """v22.4 on "their places", each part only while its engine switch is on (nothing is added while off): S1's
        fairness line per sphere, S3's name and last word at each haunt and the places their settings meet (with S4's odd
        one out), and S7's posts they lead now."""
        PP = WL.PP
        try:
            fl = self._fair_lines(PP)
            if fl:
                P["fair"] = fl
        except Exception:
            pass
        if getattr(PP, "eyes_on", False):
            try:
                ei = PP.eyes_info(0) or []
            except Exception:
                ei = []
            byid, sets = {}, []
            for e_ in ei:
                pl = e_.get("place") or {}
                if int(pl.get("slot", 0)) >= 3:
                    sp = pl.get("sphere")
                    sets.append(dict(self._eyes_word(e_), name=self._place_word(pl), sphere=sp,
                                     sphere_name=(ESP.SPHERE.get(sp) or {}).get("name", sp), setting=pl.get("kind", ""),
                                     lead=str(pl.get("face") or e_.get("face") or "")[-1:], lead_name=pl.get("face_name", "")))
                else:
                    byid[int(pl.get("place", -1))] = self._eyes_word(e_)
            for h, h0 in zip(P["haunts"], hi["haunts"]):
                d_ = byid.get(int(h0.get("place", -2)))
                if d_:
                    h.update(d_)
            if sets:
                P["settings"] = [x for x in sets if x["name"]]
        try:
            posts = self._posts_view(WL)
        except Exception:
            posts = None
        if posts:
            P["posts"] = posts

    def _post_place(self, p):
        """S7: the plain name of what a post leads, the lead moments' {place}, in the Library's words (earth_spheres): a
        title's place (LEAD_PLACE), the setting led (SETTING_PLACE), a named place by its name, else the sphere's
        (SPHERE_PLACE)."""
        pl = p.get("place") or {}
        LP, SP = lead_words("LEAD_PLACE"), lead_words("SETTING_PLACE")
        if pl.get("title") in LP:
            return LP[pl["title"]]
        pk = str(p.get("post_kind") or "")
        st = pl.get("setting") or (pk[len("setting_"):] if pk.startswith("setting_") else None)
        if st in SP:   # "setting_member_led" is a post kind, no setting: on to the place or the sphere
            return SP[st]
        nm = self._place_word(pl) if pl.get("kind") else ""
        return nm or lead_words("SPHERE_PLACE").get(p.get("sphere") or pl.get("sphere")) or "the place"

    def _posts_view(self, WL):
        """S7 (lead_ways): the posts they lead now, for "their places": what they lead, their way (the Library's words, the
        game's colour), how accepted they are, since when, terms and falls. None while the switch is off, nothing is led
        or the Library has no words for the ways yet."""
        LW, LL = lead_words("LEAD_WAY"), lead_words("LEAD_LEGIT")
        if not getattr(WL, "lw", False) or not LW or not LL:
            return None
        out = []
        for p_ in WL.lead_info(0) or []:
            if p_.get("end") is not None:
                continue
            w_ = p_.get("way")
            lg = float(p_.get("legit", 0.5)); title = (p_.get("place") or {}).get("title")
            sp = p_.get("sphere")
            out.append(dict(name=self._post_place(p_), title=self.gword(title) if title else "", kind=p_.get("kind"),
                            sphere=sp, sphere_name=(ESP.SPHERE.get(sp) or {}).get("name", sp) if ESP is not None else sp,
                            way=LW.get(w_, str(w_ or "")), colour=LEAD_COLOUR.get(w_, p_.get("colour") or ""),
                            legit=round(lg, 2), legit_word=next((w for v, w in LL if lg >= v), LL[-1][1]),
                            since=round(float(p_.get("start") or 0.0), 1), terms=int(p_.get("terms") or 0),
                            falls=len(p_.get("falls") or ())))
        return out or None

    def _lines_view(self):
        """S5 (sacred): the lines they will not cross, for the sheet: its kind, the Library's name for it, one "will not"
        clause, its colour, the age it formed and how it stands (whole, held, crossed or healed). None while off."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        PP = getattr(WL, "PP", None)
        if PP is None or not getattr(PP, "sac_on", False) or ESP is None or not hasattr(ESP, "LINE"):
            return None
        import world_keys as WK_
        out = []
        for j in range(PP.sac_line.shape[1]):
            k = int(PP.sac_line[0, j])
            if k < 0:
                continue
            kind = WK_.SACRED_KINDS[k]; LN = ESP.LINE.get(kind) or {}
            wn = LN.get("will_not") or [""]
            held, crossed = int(PP.sac_held[0, j]), int(PP.sac_crossed[0, j])
            state = ("healed" if int(PP.sac_wound[0, j]) < -10 ** 6 else "crossed") if crossed else "held" if held else "whole"
            out.append(dict(kind=kind, name=LN.get("name", kind), will_not=wn[(self.seed + k) % len(wn)], colour=COLORS[k],
                            formed=round((int(PP.sac_t[0, j]) - WL.t0) / 52, 1), state=state, held=held, crossed=crossed))
        return out or None

    def _lines_closing(self):
        """S5: the closing paragraph's line per sacred line tested in the life (LINE held, crossed or healed)."""
        try:
            lines = self._lines_view() or []
        except Exception:
            return ""
        out = [self.story.fill((ESP.LINE.get(x["kind"]) or {}).get(x["state"], "")) for x in lines if x["state"] != "whole"]
        return " ".join(x_ for x_ in out if x_)

    def _talk_told(self, t, loc, c):
        """S3: a go-between brings a place's reading back ("Cato says the Curtain Call thinks you kept to the rules"), at
        most once in TALK_AGAIN weeks at the normal level and once in TALK_QUIET in the detailed story."""
        if self.burn_in or ESP is None or not hasattr(ESP, "TALK"):
            return
        told = self.__dict__.setdefault("_talk_t", [-10 ** 6, None])
        kind = c.get("talk") if c.get("talk") in ESP.TALK else "good"
        pl = self._place_word(c.get("place"))
        gap = t - told[0]
        if (pl, kind) == told[1] and kind == "good":
            gap /= 3                                    # the same good word from the same place: once in three times as long
        lvl = 1 if gap >= TALK_AGAIN else 2 if gap >= TALK_QUIET else 9
        if lvl > self.detail:
            return
        read = self._read_clause(c.get("face"), c.get("act"), c.get("told") or c.get("side"))
        who = self._cast_who(int(c.get("go", -1))) if read and pl else None
        if who is None:
            return
        tpl = ESP.TALK[kind]
        text = tpl[int(t) % len(tpl)].replace("{go}", who[1]).replace("{place}", pl).replace("{read}", read)
        told[0], told[1] = t, (pl, kind)
        self._say(mk("N", f"{kind}|{pl}", cap_first(text)), lvl, "talk", kind=kind, place=pl)

    def _line_told(self, t, c):
        """S5: the year a sacred line forms, the Library's line for it (LINE formed)."""
        if c.get("what") != "line" or ESP is None or not hasattr(ESP, "LINE"):
            return
        LN = ESP.LINE.get(c.get("line")) or {}
        if LN.get("formed"):
            self._say(mk("S", f"{c.get('line')}|{c.get('colour', '')}", self.story.fill(LN["formed"])), int(self.burn_in),
                      "line", kind=c.get("line"))

    def _seen_who(self, d, WL):
        """S6: the model as the option row names them ("her aunt Mira"), a public figure by name; None if unknown."""
        if d.get("figure") is not None and WL is not None:
            from worldview import FIG_SOC
            return self.wv.fig(int(d["figure"]) + FIG_SOC * EngineWorld.soc(WL))
        if d.get("who") is None:
            return None
        who = self._cast_who(int(d["who"]))
        if who is None:
            return None
        w_, nm = who
        if w_.startswith("their "):
            return self._pron()[1] + w_[len("their"):]
        return nm

    def _seen_rows(self, loc, s):
        """S6 (seen_done): per option of moment s, the row "Mira has seen it done: her aunt Ines" (SEEN_ROW says which
        options carry one): kind, the short word and the Library's sentence (earth_spheres.SEEN). None while off."""
        WL = loc.get("WL")
        if not getattr(WL, "seen_on", False) or ESP is None or not hasattr(ESP, "SEEN"):
            return None
        info = WL.seen_info(0, s) or []
        out = {}
        for k, d in enumerate(info):
            if not d or d.get("kind") not in SEEN_ROW["path" if d.get("path") is not None else "way"]:
                continue
            kind = d["kind"]
            who = self._seen_who(d, WL) if kind != "none" else ""
            if who is None:
                continue
            tpl = ESP.SEEN.get(kind) or []
            if not tpl:
                continue
            text = self.story.fill(tpl[(self.seed + s + k) % len(tpl)].replace("{who}", who))
            out[k] = dict(kind=kind, word=SEEN_MARK.get(kind, kind), text=text)
        return out or None

    def _seen_dream_told(self, t, d):
        """S6: a dream seeded from someone they watched (8 to 20): the Library's SEEN dream line."""
        if ESP is None or not hasattr(ESP, "SEEN") or not ESP.SEEN.get("dream"):
            return
        who = self._seen_who(d, self.loc.get("WL") if isinstance(self.loc, dict) else None)
        if who is None:
            return
        tpl = ESP.SEEN["dream"]
        self._say(self.story.fill(tpl[int(t) % len(tpl)].replace("{who}", who)), 1 + int(self.burn_in), "seen", kind="dream",
                  path=d.get("path", ""))

    def _social_slots(self, m, loc, s, ev=None):
        """v22.4's moments name what they are about (the Library's #103, #106, #107): a caught-between moment its two
        places ({place_a}, {place_b}), an odd-one-out its place and a lead moment the post's ({place}), a sacred offer its
        price ({offer}; there {place} stays the town). From the logged moment's own word, or at a checkpoint from the
        engine's on the moment waiting (eyes_info, lead_info, sacred_info; read only)."""
        if m is None:
            return
        cw = str(self.L["src"][s].get("cast_want") or "")
        if cw not in ("caught", "odd", "sacred", "tragic", "amends") and not cw.startswith("lead_"):
            return
        WL = loc.get("WL"); ctx = m["ctx"]; ctx["_social"] = True
        try:
            if cw in ("caught", "odd"):
                ei = ev.get("eyes") if ev is not None else WL.eyes_info(0, s) if hasattr(WL, "eyes_info") else None
                for k_ in ("place_a", "place_b", "place"):
                    if ei and ei.get(k_) and k_ not in ctx:
                        ctx[k_] = self._place_word(ei[k_])
            elif cw.startswith("lead_"):
                li = ev.get("lead") if ev is not None else WL.lead_info(0, s) if getattr(WL, "lw", False) else None
                if li and "place" not in ctx:
                    ctx["place"] = self._post_place(li)
            else:
                si = ev.get("sacred") if ev is not None else WL.sacred_info(0, s) if hasattr(WL, "sacred_info") else None
                if si and si.get("offer") and "offer" not in ctx:
                    ctx["offer"] = si["offer"]
        except Exception:
            pass

    def _want_why_rows(self, circle):
        """F5 on the circle's hover: a want that came of a far event carries its cause; a far want gets its own words."""
        why = self.__dict__.get("_want_why")
        if not why:
            return
        for p_ in circle:
            k_, cs = why.get(p_["id"], (None, None))
            if not cs or not p_.get("want") or p_["want"] != str(k_).replace("_", " "):
                continue
            p_["want"] = FAR_SAY["want"].get(k_, p_["want"])
            town = self._far_town(self.loc, cs.get("town", 0)) if isinstance(self.loc, dict) else "their town"
            p_["want_why"] = cap_first(f"{cs.get('far_event', 'something happened')} in {town}"
                                       + (": " + "; ".join(cs["line"]) if cs.get("line") else ""))
