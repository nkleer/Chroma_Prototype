"""Game's methods for states, roles and titles, recall, temperament, the end of a life, story lines and yearly chapters.

Part of class Game (game.py), which inherits LifeMixin; moved out of game.py verbatim. A method here reads
module names through the imports below, the same objects game.py has, and self for everything on the Game."""
import numpy as np
from game_base import (ADJ_LOOK, ADJ_READS, ADJ_SCALE, C, CNAME, COLORS, E, EPITHETS, ES, EngineWorld, GAME, KNAMES,
    PERK_ORDER, READ_GAP, READ_TOLD, RNAMES, ROLE_AGAIN, ROLE_QUIET, ROLE_QUIET_LOST, RUSTY, SPAN_TOLD, STAGES,
    STATES, STATE_NAME, STREAK_TOLD, SUS_T, TAKEN_IN, TOLD_GAP, WOUND_TOLD, X, act, an, batch_mod, from_engine,
    ident_name, label_name, letters, mk, neg_of, role_info, who_word, world_says)
from game_words import (BECOMING, BECOMING_YEARS, FADE_WORDS, GROW_WORDS, NAME_WEEKS, RECALL_GAP, RECALL_LINES,
    RECALL_MIN, TEMPER_AGAIN, TIED_COMMIT, TIED_COMMIT_ANY, WORLD_AGAIN, accept_word, cap_first)


class LifeMixin:
    def states(self, loc=None):
        """The character's states now: the engine's adjectives (engine.ADJECTIVES, point 3), else the game's own reading."""
        loc = self.loc if loc is None else loc
        if loc is None:
            return []
        if "adj" in loc:
            t = float(loc.get("t", self.t))
            out, sh = [], []
            av = loc.get("adj_v")
            ADJ_T = getattr(E, "ADJ_ALL", E.ADJECTIVES)     # the 21 states, then the shadow states (held only with shadows on)
            SV = self.shadow_view(loc) or {}
            for i in np.nonzero(np.asarray(loc["adj"][0]))[0]:
                nm = E.ADJ_NAMES[i]; icon, good = ADJ_LOOK.get(nm, ("dot", 0))
                _, _, var, side, on, off, from_age, _, share = ADJ_T[i]
                d = dict(word=E.ADJ_SAY[i], name=nm, icon=icon, good=good, var=var, reads=ADJ_READS.get(var, var),
                         years=round(max(0.0, t - float(loc["adj_since"][0, i])) / 52, 1),
                         side=int(side), on=float(on), off=float(off), from_age=float(from_age), share=float(share),
                         scale=ADJ_SCALE.get(var, "pts"),
                         value=round(float(av[0, i]) * side, 4) if av is not None else None)
                if i >= len(E.ADJECTIVES):                  # a shadow state: its colour's line and sources for the hover
                    c_ = var[-1]; d.update(reads=f"the pull of the shadow on {CNAME.get(c_, c_)}", scale="of100",
                                           shadow=next((x for x in SV.get("cols", ()) if x["c"] == c_), None))
                    sh.append(d)
                else:
                    out.append(d)
            return sorted(out, key=lambda d: -d["good"])[:6] + sh    # a shadow state always shows, beside the others
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        X = self.conditions(loc)
        v = dict(content=float(loc["content"][0]), peace=float(loc["peace"][0]), stress=float(loc["stress"][0]),
                 mood=float(np.ravel(loc["mood"])[0]) if "mood" in loc else 0.0, want=float(loc["Q"][0]) / max(thr, 1e-9),
                 fortune=X.get("fortune", 0.0), trouble=X.get("trouble", 0.0),
                 **{RNAMES[i]: float(loc["res"][0, i]) for i in range(5)})
        young = int(loc["stage"][0]) < 2
        out, used = [], set()
        if min(v["fortune"], v["trouble"]) >= 1.8:      # both at once: a life of ups and downs, told by whichever is larger
            used.add("trouble" if v["fortune"] >= v["trouble"] else "fortune")
        for word, icon, good, var, op, t in STATES:
            if var in used or (young and var in ("money", "want")):
                continue
            x = v[var]
            hit = x >= t if op == ">=" else x <= t
            if hit:
                used.add(var)
                out.append(dict(word=word, icon=icon, good=good, var=var, name=STATE_NAME[var],
                                value=round(x, 3), level=round(abs(x - t) / max(abs(t), 0.1), 3)))
        return sorted(out, key=lambda d: -d["level"])[:5]

    def roles(self, loc=None):
        """The titles, statuses and perks the character holds now (None without the catalogue): titles by life domain
        (a community holds up to three), statuses, and perks held, suspended for a while, or rusty (a skill or credential
        no longer held that still helps a little while it fades)."""
        loc = self.loc if loc is None else loc
        GR = self.L.get("ROLES")
        if loc is None or GR is None or not loc.get("RON") or "r_has" not in loc:
            return None
        t = float(self.t); NT = GR["NT"]
        has = np.asarray(loc["r_has"][0]); since = np.asarray(loc["r_since"][0])
        yrs = lambda i: round(max(0.0, t - float(since[i])) / 52, 1)
        out = dict(titles={}, statuses=[], perks=[])
        prof = np.asarray(loc["r_prof"][0]) if "r_prof" in loc and "pwords" in GR else None
        refm = GR.get("REFM"); facets = []
        for i in np.nonzero(has[:NT])[0]:
            d = role_info(GR, i); d["years"] = yrs(i)
            if prof is not None and len(GR["pwords"][i]) > 1:      # a title held in one of its ways (its profile's words)
                d["profile"] = GR["pwords"][i][int(prof[i])] or None
            if refm is not None and GR["refines"][i] >= 0:         # a facet: held on top of a title, never in its socket
                facets.append(d)
            elif d["kind"] == "status":
                out["statuses"].append(d)
            else:
                out["titles"].setdefault(d["kind"], []).append(d)
        for d in facets:                                           # on the held title it sits on (the engine keeps one)
            on = next((x for xs in out["titles"].values() for x in xs if refm[d["i"], x["i"]]), None)
            if on is None:
                on = next((x for x in facets if x is not d and refm[d["i"], x["i"]]), None)   # a facet on a facet
            if on is not None:
                d["on"] = on["name"]; on.setdefault("facets", []).append(d)
            else:
                out["titles"].setdefault(d["kind"], []).append(d)
        flat = lambda x: [y for f in x.get("facets", []) for y in [f] + flat(f)]
        for xs in out["titles"].values():                          # a facet on a facet (raising a grandchild) joins the title
            for x in xs:
                if x.get("facets"):
                    x["facets"] = flat(x)
                    for f in x["facets"]:
                        f.pop("facets", None)
        acc = np.asarray(loc["p_acc"][0]); sus = np.asarray(loc["p_sus"][0]); lev = np.asarray(loc["p_lev"][0])
        rusty = []
        for p in range(GR["NP"]):
            i = NT + p
            if has[i]:
                d = role_info(GR, i); d.update(state="held", years=yrs(i))
            elif acc[p] and sus[p] > SUS_T:
                d = role_info(GR, i); d.update(state="suspended", back_in=round(max(0.0, float(sus[p]) - t) / 52, 1))
            elif lev[p] >= RUSTY and GR["half"][p] > 0:
                d = role_info(GR, i); d.update(state="rusty", level=round(float(lev[p]), 2)); rusty.append(d)
                continue
            else:
                continue
            out["perks"].append(d)
        kinds = list(PERK_ORDER)
        out["perks"].sort(key=lambda d: (d["state"] != "held", kinds.index(d["kind"]) if d["kind"] in kinds else 9, -d.get("years", 0)))
        out["perks"] += sorted(rusty, key=lambda d: -d["level"])[:4]
        out["statuses"].sort(key=lambda d: d["years"])
        return out

    def _role_need(self, nm):
        """What an option needs that the character lacks (explain.before's needs: a title, a perk or a state), in words."""
        GR = self.L.get("ROLES") or {}
        if nm in GR.get("ID", {}):
            d = role_info(GR, GR["ID"][nm])
        else:
            d = dict(name=nm, say=nm, kind="state", title=False, ways="", pred="is " + nm)
        d["line"] = f"only if {self.name} {d['pred']}"
        return d

    def _rung_below(self, loc, s):
        """The title that brings them to this moment (holds:, the rung below a bold try) and how long they have held it,
        or None (Emren 09:18: big titles come through consecutive steps)."""
        GR = self.L.get("ROLES")
        if GR is None or not hasattr(X, "title_held_index") or "r_since" not in loc:
            return None
        i = X.title_held_index(loc, 0, s)
        if i < 0:
            return None
        yrs = (float(loc["t"]) - float(np.asarray(loc["r_since"][0])[i])) / 52
        return dict(say=role_info(GR, i)["say"], years=int(max(yrs, 0)))

    def _role_fx(self, loc, s, k):
        """What an option can give or take (the Library's act fields: title, grants, drops, takes, suspends; each also
        _if_fails), in words: [dict(op, when, name, say, title, kind, gain, line)]."""
        GR = self.L.get("ROLES")
        fx = GR["A_FX"].get((int(s), int(k))) if GR is not None and loc.get("RON") else None
        out = []
        for when in ("ok", "fail"):
            for op, j, yrs in (fx or {}).get(when, ()):
                if j == getattr(batch_mod(), "MISSED_TITLE", -3):   # {missed}: the title their last long shot missed
                    mt = loc.get("missed_t")
                    j = int(mt[0]) if mt is not None else -1
                elif j < 0:                                     # {title}: the title held that brought them here
                    if j <= getattr(batch_mod(), "KIND_ACT", -10):   # kind:<kind> drops every title of a kind: not shown
                        continue
                    j = X.title_held_index(loc, 0, s) if hasattr(X, "title_held_index") else -1
                if j < 0:
                    continue
                d = role_info(GR, j); gain = op in ("title", "grants")
                tail = d["pred"] if gain else neg_of(d["pred"])
                if op == "suspends":
                    tail += f", for {'a year' if yrs <= 1 else f'{yrs:g} years'}"
                d.update(op=op, when=when, gain=gain,
                         line=("If it works: " if when == "ok" else "If it fails: ") + f"{self.name} {tail}" + (" from then on." if gain else "."))
                out.append(d)
        return out

    @property
    def _recalled(self):
        """The old moments already told as memories (each comes back in the story once)."""
        if "_recalled_" not in self.__dict__:
            self._recalled_ = set()
        return self._recalled_

    @property
    def _told(self):
        """F11a (v22.4.1): the acts the story told, by moment, act and age (the engine's own keys for an episode)."""
        if "_told_" not in self.__dict__:
            self._told_ = set()
        return self._told_

    def _told_act(self, ev, lvl):
        """F11a: keep the act of a moment told at this level of detail, so a memory of it can come back."""
        if lvl <= self.detail:
            self._told.add((ev.get("situation"), ev.get("choice"), ev.get("age")))

    def _recall(self, t, sev):
        """Engine v10's memory (E1, interpretation-memory.md): an act that hit hard can come back when the same moment
        returns or an act leans the same way, about 2.7 times a year. The story tells one now and then: no two within
        RECALL_GAP years, each old moment once, a scar whatever its strength, any other only when it comes back strong, and
        only a choice the story told (F11a), so the memory's age, act and outcome are the ones the reader saw.
        With item 6 on (GAME lines_tied) it waits for this week's moment and is told inside its line (_recall_in)."""
        self._recall_now = None
        if t - self._recall_t < 52 * RECALL_GAP:
            return
        tied = GAME["lines_tied"] and getattr(ES, "RECALL_IN", None)
        for ev in sev:
            rc = ev.get("recall")
            if not rc:
                continue
            key = (rc.get("age"), rc.get("choice"))
            if (rc.get("situation"), rc.get("choice"), rc.get("age")) not in self._told:   # F11a: only a choice the story told
                continue
            if key in self._recalled or (not rc.get("scar") and float(rc.get("strength", 0)) < RECALL_MIN):
                continue
            a = int(rc.get("age", 0)); what = act(str(rc.get("choice", "")))
            when = "as a child" if a < 12 else f"at {a}"
            kind = "scar" if rc.get("scar") else "good" if rc.get("success") else "bad"
            if tied:
                self._recall_now = dict(key=key, a=a, what=what, when=when, kind=kind)
                return
            self._recall_t = t; self._recalled.add(key)
            pool = RECALL_LINES[kind]
            line = pool[(int(t) * 7 + a) % len(pool)].format(when=when, When=when[:1].upper() + when[1:], what=what)
            icon = "ci-heartbreak" if kind == "scar" else "ci-diary"
            self._say(mk("O", f"memory|{icon}|1", self.story.fill(line)), 0 if not self.burn_in else 1, "memory", icon=icon)
            return

    def _recall_in(self, t, line, lvl):
        """Item 6: the memory this week's moment brought back, as one more sentence of that moment's line (Library
        RECALL_IN) when the line is told at this level of detail. Only a told memory counts for the gap and the once-each
        rule, so one that came with an untold week can come back with a told one."""
        rc = self._recall_now
        if rc is None or not line or lvl > self.detail:
            return line
        self._recall_now = None
        self._recall_t = t; self._recalled.add(rc["key"])
        pool = ES.RECALL_IN[rc["kind"]]
        cl = pool[(int(t) * 7 + rc["a"]) % len(pool)].replace("{when}", rc["when"]).replace("{what}", rc["what"])
        icon = "ci-heartbreak" if rc["kind"] == "scar" else "ci-diary"
        return line + " " + mk("O", f"memory|{icon}|0", self.story.fill(cap_first(cl) + "."))

    def _tied_ev(self, name, lvl):
        """Item 6: this week's first told event, by name, for the temperament line (_temper_week)."""
        if GAME["lines_tied"] and name and lvl <= self.detail and self._week_ev is None:
            self._week_ev = name

    def _ev_name(self, ev):
        """Item 6: a death or a commitment's change as a noun phrase for TEMPER_CAUSE ("losing a parent", "the breakup")."""
        if "death" in ev:
            r = ev["death"]["role"]
            return "losing their partner" if r == "partner" else "losing " + an(r)
        if "commitment" in ev:
            c = ev["commitment"]
            return (TIED_COMMIT.get(c["what"]) or {}).get(c["kind"]) or TIED_COMMIT_ANY.get(c["what"], "").replace("{kind}", c["kind"])
        return None

    def _temper_week(self, loc):
        """Item 6: how far temperament moved this week, kept with the week's told event, if any."""
        ev, self._week_ev = self._week_ev, None
        if "react" not in loc:
            return
        now = np.array([float(loc[k][0]) for k, *_ in self.TEMPER])
        prev, self._temper_prev = self._temper_prev, now
        if ev is not None and prev is not None:
            self._temper_evs.append((now - prev, ev))

    def _family_faith(self, loc):
        """The engine gives an inherited faith a random profile; a chosen family faith replaces it."""
        F = E.KIDX["faith"]
        if self.faith_mix is None or not loc["held"][0, F]:
            return
        fm_ = (1 - GAME["faith_home"]) * self.faith_mix + GAME["faith_home"] * np.asarray(loc["fam"][0], float)
        loc["prof"][0, F] = fm_
        for ev in loc["events"][0][::-1]:
            if "commitment" in ev and ev["commitment"].get("what") == "inherited":
                ev["commitment"]["profile"] = fm_.round(2).tolist()
                break

    def _on_end(self, t, loc):
        """Tell what happened this week. The story (story.py) tells it; with the ledger on (key l), the numbers follow."""
        if "wound" in loc:                          # v6: the year's hardest blow, and how supported they were then
            wd = float(loc["wound"][0])
            if wd > self._yr["wound"]:
                self._yr.update(wound=wd, support=float(loc["support"][0]))
        if GAME["own_ix"] and not self.burn_in and "a" in loc:   # S2: the color leading this week's act, and each color's
            m_ = np.maximum(np.asarray(loc["m"][0], float), 0)     # share of the week's open options, for the yearly fade
            led = (m_.max(1) - m_.min(1) > 1e-9) & ~np.asarray(loc["do_nothing"][0], bool)    # even ways lead no color
            lead = np.argmax(m_, 1); a_ = int(loc["a"][0])
            if led[a_]:
                self._ix_use[lead[a_]] += 1
            o_ = led & np.asarray(loc["open_"][0], bool)
            if o_.any():
                self._ix_exp += np.bincount(lead[o_], minlength=C) / o_.sum()
        evs = loc["events"][0]
        new = evs[self._ev_i:]; self._ev_i = len(evs)
        w_now = E.softmax(loc["z"][0]); res_now = loc["res"][0].copy()
        moved = {}
        if self._w_prev is not None:     # what this week moved: colors in points, means, as the browser's hover shows them
            moved = dict(dw=[round(float(x) * 100, 2) for x in w_now - self._w_prev],
                         dres={RNAMES[i]: round(float(res_now[i] - self._res_prev[i]), 3) for i in range(5)
                               if abs(res_now[i] - self._res_prev[i]) >= 0.005})
        self._w_prev = w_now; self._res_prev = res_now
        cpw = self._cp_week; self._cp_week = None
        tp, self._turn_pick = self._turn_pick, None
        if tp is not None:
            self._turning_end(t, loc, tp)
        L = self.L
        s = int(loc["s"][0]); sit = L["names"][s]
        stage = int(loc["stage"][0]); age = t / 52
        sev = [ev for ev in new if "situation" in ev]
        self._recall(t, sev)
        kills = self._kills(L, s)
        if self.story.one_roll and loc.get("WL") is not None:
            self._one_roll(loc)                         # F7: the world's dead, before the week's scene and deaths are told
        m = None
        if sev or cpw is not None:
            kind = KNAMES[int(loc["rk"][0])] if bool(loc["recon"][0]) else None
            m = cpw["cp"]["moment"] if cpw is not None else self.story.moment(t, sit, stage, age, kind, kills)
            if cpw is None and sev:
                self._far_moment(m, loc, s, sev[0])     # far_ties: the far moment's tie, town and event (Library slots)
                self._social_slots(m, loc, s, sev[0])   # v22.4: the places, post or price the moment is about
        GR = L.get("ROLES") if loc.get("RON") else None
        fold, folded = {}, set()      # a title that came with a commitment started this week is told in the commitment's line
        gained_now = set()            # titles gained this week: a facet that came with one (newlywed) shows on the HUD only
        if GR is not None:
            starts = {ev["commitment"]["kind"] for ev in new if "commitment" in ev and ev["commitment"]["what"] == "start"}
            for ev in new:
                r = ev.get("role")
                if r and r["what"] == "gained" and r["name"] in GR["ID"]:
                    gained_now.add(GR["ID"][r["name"]])
                if (r and r["what"] == "gained" and r["kind"] in starts and r["kind"] not in fold and r["name"] in GR["ID"]
                        and not ("refines" in GR and GR["refines"][GR["ID"][r["name"]]] >= 0)):
                    fold[r["kind"]] = role_info(GR, GR["ID"][r["name"]]); folded.add(id(r))
        if cpw is not None and age >= self.start_age:
            self._mark_threads(cpw, new, GR, age)
            if GAME["returns"]:
                self._seed_pick(cpw, new, age)          # Picks come back: the pick, by its week
        if age >= self.start_age:
            self._world_effects(t, loc)               # WL1, WL5: what the world changed of theirs this week     # F5: what the pick started, for the moments that follow from it
        for ev in sev + [ev for ev in new if "situation" not in ev]:     # the moment first, then what followed from it
            self._met(age, ev, sit)
            if "situation" in ev:
                if m["ctx"].get("_dying") and not self.batch:   # the person in the scene is gone (the batch logs deaths itself)
                    self.story.scene(m)
                    self.story.dies(m["ctx"].get("_p_dead"))
                if cpw is not None:
                    o = cpw["cp"]["by_idx"][cpw["choice"]]
                    pushed = cpw["choice"] != cpw["own"]
                    f = self._force or {}
                    line = self.story.outcome(m, ev, L["labels"][s][cpw["choice"]], pushed, f.get("rel", 0.0) if pushed else 0.0,
                                              bool(f.get("closed")) if pushed else False, o["colors"])
                    line = self._recall_in(t, line, 0)              # item 6: the memory it brought back, inside it
                    self._told_act(ev, 0)
                    self._tied_ev("“" + cpw["cp"]["title"] + "”", 0)
                    rb = None
                    if "span" in loc and float(loc["span"][0]) > SPAN_TOLD:     # v6: joining opposed ways fits or tears
                        line += "\n" + self.story.rebound(bool(ev["success"]), float(loc["span"][0])); rb = bool(ev["success"])
                    if not ev["success"] and loc.get("SHON"):      # item 2: an act their shadow made fail is named
                        sl = self._shadow_fail(new, t)
                        if sl:
                            line += "\n" + sl
                    self.resolution = self._resolution(loc, cpw, ev, line, o, pushed, f.get("rel", 0.0) if pushed else 0.0, moved)
                    self.history["acts"].append((round(age, 1), o["colors"], bool(ev["success"]), bool(pushed)))   # the song's deeds
                    rs = self.resolution
                    rs["needs"] = self._needs_moved(loc, cpw["cp"]["snap"])
                    if pushed:
                        rs["hindsight"] = self._hindsight(loc, cpw, bool(ev["success"]), rs["needs"])
                        self._voice_trust_turn()
                    rs["pivot"] = self._pivot(loc, cpw, bool(ev["success"]), rs.get("hindsight"))
                    if GAME["returns"] and cpw["cp"].get("ret"):     # Picks come back: the card names the pick it came from
                        rs["back"] = self._ret_came(cpw, ev, age)
                    vo = self._voice_pick(loc, cpw, bool(ev["success"]), pushed, f.get("rel", 0.0) if pushed else 0.0, moved, rs)
                    if pushed and GAME["own_ix"]:       # S2: how far the pushed ways have become theirs
                        rs["own"] = self._own_push(loc, cpw, rs.get("hindsight"))
                    elif GAME["own_ix"] and cpw.get("lean"):     # S2: a light steer that kept their own pick
                        rs["own"] = self._own_lived(loc, cpw)
                    if vo:                              # item 3: their answer to the voice, and whether it was right
                        line = "\n".join(x for x in (vo[0], line, vo[1]) if x); rs["text"] = line
                    rs["say"] = "\n".join(x for x in (rs["say"], self.story.needs_line(rs["needs"]),
                                                        (rs.get("hindsight") or {}).get("line", "")) if x)
                    self._say(line, 0, "choice", sit=sit, ok=bool(ev["success"]), pushed=cpw["choice"] != cpw["own"],
                              colors=o["colors"], act=o["label"], rebound=rb, felt=round(o["felt"], 2), real=round(o["true"], 2),
                              rel=round(o["rel"], 2) if pushed else 0.0, delta=round(float(ev.get("delta", 0.0)), 2),
                              title=cpw["cp"]["title"], res=dict(became=rs["became"], closer=rs["closer"], surprise=rs["surprise"],
                                                                 heart=rs["with_heart"], head=rs["with_head"], regret=rs["regret"],
                                                                 lesson=rs["lessons"][0] if rs["lessons"] else None), **moved)
                    if self.ledger:
                        self._say(self._outcome_line(ev, cpw, loc), 0, "ledger")
                elif s == self.ORD:
                    line = self._recall_in(t, self.story.ordinary(ev, L["labels"][s].index(ev["choice"])), 2); self._told_act(ev, 2)
                    self._say(line, 2, "ordinary", colors=self._colors(loc, int(loc["a"][0])))
                elif sit in ("bereavement", "crisis or disaster") or kills:
                    col = self._colors(loc, int(loc["a"][0])); self._tied_ev("“" + sit + "”", 0); self._told_act(ev, 0)
                    self._say(self._recall_in(t, self.story.told_moment(m, ev, col), 0), 0, "loss" if (kills or sit == "bereavement") else "crisis",
                              sit=sit, ok=bool(ev["success"]), colors=col, delta=round(float(ev.get("delta", 0.0)), 2),
                              gate=ev.get("gate", ""), **moved)
                    if self.ledger:
                        self._say(self._choice_line(ev), 0, "ledger")
                elif self.detail >= 2:
                    col = self._colors(loc, int(loc["a"][0])); self._tied_ev("“" + sit + "”", 2); self._told_act(ev, 2)
                    self._say(self._recall_in(t, self.story.told_moment(m, ev, col), 2), 2, "moment", sit=sit, ok=bool(ev["success"]),
                              colors=col, delta=round(float(ev.get("delta", 0.0)), 2), gate=ev.get("gate", ""), **moved)
                elif (float(loc["L"]["STAKES"][s]) >= 1.0 and t - self._last_line.get(s, -10 ** 6) >= TOLD_GAP.get(sit, 104)
                      and not self.burn_in):
                    self._last_line[s] = t
                    col = self._colors(loc, int(loc["a"][0])); self._tied_ev("“" + sit + "”", 1); self._told_act(ev, 1)
                    self._say(self._recall_in(t, self.story.told_moment(m, ev, col), 1), 1, "moment", sit=sit, ok=bool(ev["success"]),
                              colors=col, delta=round(float(ev.get("delta", 0.0)), 2), gate=ev.get("gate", ""), **moved)
                    if self.ledger:
                        self._say(self._choice_line(ev), 1, "ledger")
                elif self.batch and L["src"][s].get("tier") == "everyday":   # untold everyday weeks still shape the year
                    self.story.tally(loc["m"][0, int(loc["a"][0])])
            else:
                line = None; tag = "note"; meta = {}
                if "outside" in ev:
                    o = ev["outside"]
                    line = self.story.outside(o, stage, 0 if self.burn_in else self.detail, GAME["lines_tied"])   # the past is told briefly
                    tag = "move" if o["name"] == "moving somewhere new" else "outside"
                    meta = dict(source=o.get("source", ""), sit=o["name"],
                                took=round(float(o["took"]), 2) if o.get("took") is not None else None,
                                message=letters(np.asarray(o["message"], float)) if o.get("message") is not None else "")
                elif "era" in ev:
                    line = self.story.era(ev["era"]); tag = "era"
                    meta = dict(kind=ev["era"]["kind"], idea=ev["era"]["idea"], took=round(float(ev["era"]["took"]), 2))
                elif "commitment" in ev:
                    c = ev["commitment"]
                    ends = int(L["ENDS"][s]) if "ENDS" in L else -1
                    shown = m is not None and m["text"] is not None
                    if not (shown and c["what"] != "start" and ends >= 0 and KNAMES[ends] == c["kind"]):
                        line = self.story.commitment(c, m, fold.get(c["kind"]) if c["what"] == "start" else None)
                    else:
                        self.story.settle(c)            # the moment told it; the people still change
                    tag = "commitment"; meta = dict(kind=c["kind"], what=c["what"],
                                                    expects=letters(np.asarray(c["profile"], float)) if c.get("profile") else "")
                elif "clash" in ev:
                    line = self.story.clash(ev["clash"]); tag = "clash"; meta = dict(kind=ev["clash"]["kind"])
                elif "rite" in ev:
                    line = self.story.rite(ev["rite"], sit if sev or cpw is not None else None)
                    tag = "rite"; meta = dict(to=ev["rite"]["to"].replace("_", " "))
                elif "conversion" in ev:
                    line = self.story.conversion(ev["conversion"]); tag = "turn"
                elif "breakthrough" in ev:
                    line = self.story.breakthrough(ev["breakthrough"]); tag = "breakthrough"
                elif "death" in ev:
                    alone = ev["death"]["role"] == "partner" and not any(
                        "commitment" in e_ and e_["commitment"]["what"] == "widowed" for e_ in new)
                    line = self.story.death(ev["death"], m, age, alone); tag = "death"
                elif "mark" in ev:
                    self.story.mark(ev["mark"]["mark"], m)
                    if GAME["returns"] and cpw is not None and age >= self.start_age:
                        self._seed_mark(ev["mark"]["mark"], m)   # Picks come back: a marked pick plants a seed
                elif "goal" in ev:                      # v7: dreams, passions and plans
                    g = ev["goal"]
                    if age >= self.start_age:
                        self._plan_lean(loc, g)         # item 4, 5.4: picks lead to plans
                    gl = self.story.goal(g)
                    if gl:
                        quiet = g["what"] in ("pushed aside", "extended") or (g["kind"] == "plan" and g.get("horizon") == "week")
                        lvl = 2 if quiet else 1 if self.burn_in and g["kind"] == "plan" else 0
                        self._say(gl, lvl, "goal", kind=g["kind"], what=g["what"], domain=g.get("domain", ""),
                                  source=g.get("source", ""), horizon=g.get("horizon", ""), trigger=g.get("trigger", ""),
                                  colors=letters(np.asarray(g.get("mix", (0.2,) * 5), float)),
                                  dream=(self.story.dreams.get(int(g.get("id", 0))) or {}).get("name", ""))
                elif "world" in ev:                     # the outer world (spec 1 §8): big public events always; the rest when it
                    w0 = ev["world"]                    # touches them or their people
                    if "domain" not in w0:
                        recs = [w0]
                    elif w0.get("big") or loc.get("WL") is None:
                        recs = []                       # the engine's big ones are told once, by news()
                    else:                               # the engine's own record (WL.story): their town, their workplace, their people
                        recs = [dict(r_, self=bool(w0.get("self")), touches=[int(x_) for x_ in w0.get("touches") or []])
                                for r_ in from_engine(w0, loc["WL"].t0, EngineWorld.soc(loc["WL"]))]
                    for w_ in recs:
                        wd = self.world_data()
                        byid = {c_["id"]: c_ for c_ in wd[2]} if wd else {}
                        names = {p_["id"]: who_word(byid.get(p_["id"], p_), p_["name"])
                                 for p_ in self.wv.circle(wd[2], names=self.cast_names(wd[2]))
                                 if p_["layer"] <= 3 and (p_["alive"] or not self.story.one_roll)} if wd else {}
                        wl = self.wv.line(w_, names)
                        if wl:                          # G2 (B package): the same world line is not told again within WORLD_AGAIN weeks
                            told = self.__dict__.setdefault("_wline_t", {})
                            if t - told.get((w_["kind"], wl[1]), -10 ** 6) < WORLD_AGAIN:
                                continue
                            told[(w_["kind"], wl[1])] = t
                            lvl = 0 if w_.get("big") or (w_.get("self") and w_["kind"] not in ("local_election", "crime_wave")) else \
                                2 if w_["kind"] == "local_election" else 1     # a council vote is for the detailed story only
                            self._say(mk("O", f"{w_['kind']}|{wl[0]}|{int(bool(w_.get('big')))}", self.story.fill(wl[1])),
                                      lvl, "world", kind=w_["kind"], icon=wl[0])
                elif "role" in ev and GR is not None and id(ev["role"]) not in folded and ev["role"]["name"] in GR["ID"]:
                    r = ev["role"]                      # a title or perk gained, lost, suspended or restored
                    d = role_info(GR, GR["ID"][r["name"]])
                    how = r["how"]
                    if how == "a partner at home, or the children grown":    # the rule's two reasons: say the one that holds
                        how = "a partner at home" if loc["held"][0, KNAMES.index("partner")] else "the children grown"
                    key = how.split(" ")[0] if how.startswith(("came ", "became ", "grew ", "through ")) else how
                    lvl = ROLE_QUIET.get(key, 0)
                    if r["what"] == "lost":
                        lvl = ROLE_QUIET_LOST.get(how, lvl)
                        if how.startswith("the ") and how.endswith(" ended"):
                            lvl = 9                     # a facet that ends with its title: the title's own line tells it
                    if (r["what"] == "gained" and "refines" in GR and GR["refines"][d["i"]] >= 0
                            and any(GR["REFM"][d["i"], j] for j in gained_now if j != d["i"] and j < GR["NT"])):
                        lvl = max(lvl, 2)               # newly married, the week of the wedding: the HUD shows it on the title
                    if not d["title"] and r["what"] != "suspended":
                        lvl = max(lvl, 1)               # perks: told at the normal level, titles always
                    if not d["title"] and t - self._role_told.get(r["name"], -10 ** 6) < ROLE_AGAIN:
                        lvl = max(lvl, 2)               # a perk that comes and goes (good for a loan) is told once in a while
                    if self.burn_in:
                        lvl += 1                        # the past before the chosen start age is told briefly
                    if lvl <= 2:
                        frm = how[len("grew from "):] if how.startswith("grew from ") else None
                        frm = GR["say"][GR["ID"][frm]] if frm in GR["ID"] else None
                        rl = self.story.title_line(r, d, frm)
                        if rl and lvl <= self.detail:
                            self._role_told[r["name"]] = t
                        if rl:
                            self._say(rl, lvl, "role", name=r["name"], kind=r["kind"], what=r["what"], how=how, title=d["title"],
                                      ways=d["ways"])
                elif "read" in ev:
                    r = ev["read"]
                    lvl = 2 if self.burn_in else 1 if (r["impact"] >= READ_TOLD and t - self._last_read >= READ_GAP
                                                       and t - self._read_told.get(r["name"], -10 ** 6) >= 5 * 52) else 2
                    if lvl <= self.detail:
                        self._last_read = t; self._read_told[r["name"]] = t
                        c_ = self._read_color(r) if GAME["lines_tied"] else ""   # item 6: the color it pulls toward
                        r = self._disaster_read(r)      # WL6: the disaster that happened, not always a flood
                        self._say(self.story.read(r, stage, c_), lvl, "read", sit=r["name"], reading=r.get("reading", ""),
                                  impact=round(float(r.get("impact", 0.0)), 2), **({"color": c_} if c_ else {}))
                elif "sphere_lever" in ev:              # spheres phase 4 (sph_levers): their act on the town's sphere
                    self._lever_told(t, loc, ev["sphere_lever"])
                elif "body" in ev or "decline" in ev:   # v22.5 F1 and F2: the body's and the mind's turns, a last decline
                    self._body_told(ev)
                elif "cast" in ev and ev["cast"].get("kind") in ("far", "taken in", "want"):
                    self._far_told(t, loc, ev["cast"])  # far_ties: a close tie's news, a tie taken in, a want's cause
                elif "cast" in ev and ev["cast"].get("kind") == "talk":
                    self._talk_told(t, loc, ev["cast"])  # S3: a go-between brings a place's word on them
                elif "cast" in ev and ev["cast"].get("kind") == "sacred":
                    self._line_told(t, ev["cast"])      # S5: a sacred line forms
                elif isinstance(ev.get("seen"), dict) and ev["seen"].get("kind") == "dream":
                    self._seen_dream_told(t, ev["seen"])   # S6: a dream seeded from someone they watched
                if line:
                    self._say(line, 0, tag, **meta)
                    if GAME["lines_tied"] and tag in ("death", "commitment"):
                        self._tied_ev(self._ev_name(ev), 0)
                    if self.ledger:
                        old = self._event_line(ev)
                        if old:
                            self._say(old, 0, "ledger")
        if self.story.one_roll and loc.get("WL") is not None:
            self._one_roll(loc, kids=True)              # F7: a child the world lost after the engine's moment
        if self.batch and "alive" in loc and loc.get("WL") is not None and (self._kin_t is None or t - self._kin_t >= 4
                                                                     or int(loc["alive"][0, 1]) > len(self.story.alive("sibling"))):
            self._kin_sync(t, loc)          # the family the world was born into, a new sibling the week it comes, else monthly
        if self.batch and "alive" in loc and loc["alive"].shape[1] > 5 and self.story.alive("child"):   # R15: a later child is one more in the family
            taken = self.story.one_roll and bool(TAKEN_IN.search(sit))   # F7: a child taken in is not a birth
            for _ in range(int(loc["alive"][0, 5]) - len(self.story.alive("child"))):
                self._say(self.story.later_child(taken) if taken else self.story.later_child(), 0 if not self.burn_in else 1, "kin")
        if GAME["lines_tied"]:
            self._temper_week(loc)
        self._force = None

    def _choice_line(self, ev):
        ok = "it worked" if ev["success"] else "it went badly"
        line = f"  {ev['age']:5.1f}  {ev['situation']}: {self.name} chose to {ev['choice']} ({ok})."
        if ev.get("gate") and ev["gate"] != "chosen" and ev.get("wanted") and ev["wanted"] != ev["choice"]:
            why = {"pulled away": "habit pulled them away", "unnoticed": "it never crossed their mind",
                   "lacked the means": "they lacked the means", "not offered": "it wasn't on offer"}.get(ev["gate"], ev["gate"])
            line += f" They wanted to {ev['wanted']}, but {why}."
        return line

    def _outcome_line(self, ev, cpw, loc):
        cp = cpw["cp"]; o = cp["by_idx"][cpw["choice"]]
        ok = "It worked." if ev["success"] else "It went badly."
        if cpw["choice"] == cpw["own"]:
            who = f"{self.name} did what they leaned toward: {o['label']}."
        else:
            who = f"You pushed {self.name} to {o['label']}."
        line = f"  {ev['age']:5.1f}  >> {who} {ok}"
        if self._force is not None and cpw["choice"] != cpw["own"]:
            acc = self._force.get("acc") or accept_word(self._force["rel"])
            if acc in ("reluctant", "against it"):
                line += f" It wasn't their choice ({acc}): stress and pent-up wanting rise."
            elif acc == "okay with it":
                line += " It wasn't their choice, but they were okay with it."
            if self._force["closed"] and not ev["success"]:
                line += " " + world_says(self.setting, "WORDS", "backfire",
                                         "Forcing what was out of reach backfired: more stress, some money lost.")
        return line

    def _event_line(self, ev):
        n = self.name
        if "outside" in ev:
            o = ev["outside"]; took = o.get("took")
            tail = ""
            if took is not None and o.get("message"):
                msg = letters(o["message"])
                tail = (f" It pulled their wanting toward {msg}." if took > 0.3 else
                        f" They pushed back against its {msg} message." if took < -0.3 else f" It left them unmoved.")
            return f"  {o['age']:5.1f}  [{o['source']}] {o['name'][0].upper() + o['name'][1:]}.{tail}"
        if "era" in ev:
            e = ev["era"]; took = e["took"]
            react = "embrace it" if took > 0.3 else "resist it" if took < -0.3 else "shrug it off"
            return f"  {e['age']:5.1f}  [the times] A {e['kind']} era of {e['name']} ({e['idea']}) begins. {n} tends to {react}."
        if "commitment" in ev:
            c = ev["commitment"]; kind = c["kind"]; what = c["what"]
            prof = letters(c["profile"]) if c.get("profile") else ""
            if what == "start":
                return f"  {c['age']:5.1f}  [title] {n} takes on a {kind}, through \"{c.get('through', '')}\". It expects {prof}."
            if what == "inherited":
                return f"  {c['age']:5.1f}  [title] {n} is raised inside the family faith, which expects {prof}."
            words = {"left": f"{n} walks away from their {kind}.", "lost job": f"{n} loses their job.",
                     "retired": f"{n} retires.", "widowed": f"{n}'s partner dies.", "moved": f"{n} changes employer."}
            return f"  {c['age']:5.1f}  [title] " + words.get(what, f"{kind}: {what}.")
        if "clash" in ev:
            c = ev["clash"]
            return f"  {c['end']:5.1f}  [clash] The clash with their {c['kind']} (since {c['start']:.1f}) ends: {c['how']}."
        if "rite" in ev:
            r = ev["rite"]
            if r.get("quiet"):
                return f"  {r['age']:5.1f}  [stage] {n} grows quietly into a {r['to'].replace('_', ' ')}."
            return f"  {r['age']:5.1f}  [stage] A rite of passage: {n} becomes a {r['to'].replace('_', ' ')} ({r['event']})."
        if "conversion" in ev:
            c = ev["conversion"]
            return (f"  {c['age']:5.1f}  [turning point] {n} loses faith in {CNAME[c['disowned']]} ways "
                    f"and turns toward {letters(c['toward'])}.")
        if "breakthrough" in ev:
            b = ev["breakthrough"]
            return (f"  {b['age']:5.1f}  [breakthrough] Pent-up wanting breaks through: {n} moves toward "
                    f"{letters(b['want'])}.")
        return None

    def _shadow_fail(self, new, t):
        """Item 2: "<State>: <clause>." for an act that failed because of the shadow (the engine's "shadow" event this week),
        in the Library's words (earth_story.SHADOW_FAIL); "" without them."""
        sh = next((e["shadow"] for e in new if "shadow" in e), None)
        W = getattr(ES, "SHADOW_FAIL", None) if ES is not None else None
        if sh is None or not W or not W.get(sh["state"]):
            return ""
        pool = W[sh["state"]]
        return self.story.fill(f"{sh['state'][:1].upper()}{sh['state'][1:]}: {pool[int(t) % len(pool)]}.")

    def _shadow_year(self, t, loc):
        """Item 2: the yearly chapter's line when a shadow state comes on (grow) or goes off (fade), in the Library's words
        (earth_story.SHADOW_YEAR). Only with the engine's shadows switch on; the first year sets what is known."""
        W = getattr(ES, "SHADOW_YEAR", None) if ES is not None else None
        if not loc.get("SHON") or "adj" not in loc or not W:
            return
        adj = np.asarray(loc["adj"][0])
        for st in E.SH_STATES:
            i = E.ADJ_ID.get(st, -1)
            on = bool(0 <= i < len(adj) and adj[i])
            was = self._sh_told.get(st)
            self._sh_told[st] = on
            if was is None or was == on or self.burn_in or not W.get(st):
                continue
            pool = W[st]["grow" if on else "fade"]
            self._say(self.story.fill(pool[(int(t) // 52) % len(pool)]), 1, "shadow", state=st, on=on)

    def _yearly(self, t, loc):
        if GAME["own_ix"] and not self.burn_in:
            self._own_year()
        w = E.softmax(loc["z"][0]); M = float(loc["M"][0])
        lbl = E.identity(w, M, self._prev_label); self._prev_label = lbl
        self.seen_labels.add(lbl)
        c, p = float(loc["content"][0]), float(loc["peace"][0])
        self.history["content"].append((t / 52, c)); self.history["peace"].append((t / 52, p)); self.history["label"].append((t / 52, lbl))
        self.history["w"].append((t / 52, [round(float(x), 3) for x in w]))
        # the story's voice: present identity blended with a fading memory of past ones (story.py)
        self.story.update_voice(w)
        self._shadow_year(t, loc)
        vl = self._core_label                       # 5.5: the chapter names who they have settled into, and who they are becoming
        self._becoming_year()
        if vl != self._voice_label:                 # a new identity in the telling: a short phrase for it
            eps = EPITHETS.get(vl, [])
            self._epithet = eps[len(self._named) % len(eps)] if eps else ""
            self._named.add(vl)
        ident = (ident_name(vl) + (f", {self._becoming or self._epithet}" if self._becoming or self._epithet else "")) if vl else ""
        self._voice_label = vl
        self.history["name"].append((t / 52, vl, self._becoming))
        # item 6 (GAME lines_tied): the times as a clause of the year's lead, and a new name the voice did most of on its header
        tied_times = GAME["lines_tied"] and getattr(ES, "YEAR_LEAD", None)
        times = self._times_year() if tied_times else None
        bh, self._became_head = self._became_head, None
        vh = bh[1] if bh is not None and vl and bh[0] == vl else ""
        self._say("", 0)
        head, _, body = self.story.chapter(t / 52, int(loc["stage"][0]), w, c, p, ident + (f" · {vh}" if vh else ""),
                                           times).partition("\n")
        self.log.append(head)
        self.feed.append(dict(tag="chapter", text="", age=int(round(t / 52)), stage=STAGES[int(loc["stage"][0])].replace("_", " "),
                              label=vl, guild=ident_name(vl) if vl else "", epithet=self._epithet if vl else "",
                              becoming=self._becoming if vl else "",
                              w=[round(float(x), 3) for x in w], content=round(c, 2), peace=round(p, 2),
                              voice=[round(float(x), 3) for x in self.story.voice], weeks=self.story.last_weeks,
                              **({"voice_head": vh} if vh else {})))
        if body:
            self._say(body, 0, "year")
        self._voice_chapter(t / 52)
        if not tied_times:
            self._times_year()                      # WL4: one line on how the times touched them this year
        self._year_notes(t, loc)
        if self.batch and "alive" in loc and loc.get("WL") is None:   # grandparents of grown-up grandchildren die outside
            # the Library's moments (with the outer world on, _kin_sync says it once the engine's record is overdue)
            line = self.story.quiet_deaths("grandparent", int(loc["alive"][0, 3]), t / 52)
            if line:
                self._say(line, 0 if not self.burn_in else 1, "death")
        if self.ledger:
            held = [KNAMES[k] for k in range(len(KNAMES)) if loc["held"][0, k]]
            cols = " ".join(f"{COLORS[i]}{w[i] * 100:3.0f}" for i in range(C))
            voice = " ".join(f"{COLORS[i]}{self.story.voice[i] * 100:3.0f}" for i in range(C))
            self._say(f"   [now {label_name(lbl) if lbl else 'unformed'} | {cols} | voice {voice} | content {c:.2f} peace {p:.2f}"
                      + (f" | {', '.join(held)}" if held else "") + "]", 0, "ledger")
        self._temperament_news(t, loc)

    def _name_week(self, w, loc):
        """5.5 (implementation list item 4; chroma-ideas/gameplay-feel.md): the name says who they have settled into, the
        identity of the colors held over the last four years, read week by week with the usual hold (a color joins above
        .22 and leaves below .18). Measured on lives left alone: 3.6 name changes after 18, against 13.9 for the
        yearly reading."""
        if len(self._wring) == NAME_WEEKS:
            self._wsum -= self._wring[0]
        self._wring.append(np.asarray(w, float)); self._wsum += self._wring[-1]
        if "M" in loc:
            was = self._core_label
            self._core_label = E.identity(self._wsum / len(self._wring), float(loc["M"][0]), self._core_label)
            if self._core_label != was:
                self._voice_became(self._core_label)

    def _becoming_year(self):
        """5.5: who they are becoming, once a year: the color that rose most over the last three years when it rose by
        BECOMING or more ("growing curious"), else a color of the name that fell as much ("loosening their hold on
        order"). Said once it has held two readings (F4), so it reads as news: about a third of adult years or less."""
        W = self.history["w"]
        cand = None
        if self._core_label and len(W) > BECOMING_YEARS:
            d = np.asarray(W[-1][1]) - np.asarray(W[-1 - BECOMING_YEARS][1])
            up, dn = int(np.argmax(d)), int(np.argmin(d))
            if d[up] >= BECOMING:
                cand = ("grow", COLORS[up])
            elif d[dn] <= -BECOMING and COLORS[dn] in self._core_label:
                cand = ("fade", COLORS[dn])
        shown = cand if cand is not None and cand == self._becoming_c else None
        self._becoming_c = cand
        self._becoming = "" if shown is None else (GROW_WORDS if shown[0] == "grow" else FADE_WORDS)[shown[1]]

    def _year_notes(self, t, loc):
        """Engine v6 loops, told once a year when they clearly happened: after a hard blow, support heals or its lack
        hardens; trouble and fortune come in streaks."""
        yr, age = self._yr, t / 52
        self._yr = dict(wound=0.0, support=0.0)
        if yr["wound"] >= WOUND_TOLD and not self.burn_in and t - self._after_t >= 4 * 52:
            if yr["support"] >= 0.75:
                self._say(self.story.aftermath(True, age, yr["wound"], yr["support"]), 0, "healed", wound=round(yr["wound"], 2),
                          support=round(yr["support"], 2)); self._after_t = t
            elif yr["support"] <= 0.4:
                self._say(self.story.aftermath(False, age, yr["wound"], yr["support"]), 0, "hardened", wound=round(yr["wound"], 2),
                          support=round(yr["support"], 2)); self._after_t = t
        if "trouble" in loc and t - self._streak_t >= 5 * 52 and not self.burn_in:
            tr, fo = float(loc["trouble"][0]), float(loc["fortune"][0])
            if tr >= STREAK_TOLD and tr > fo:
                self._say(self.story.streak(True, tr), 0, "trouble", streak=round(tr, 2)); self._streak_t = t
            elif fo >= STREAK_TOLD:
                self._say(self.story.streak(False, fo), 0, "fortune", streak=round(fo, 2)); self._streak_t = t

    def _temperament_news(self, t, loc):
        """Temperament is never set by the player; it forms from the life lived. Say when it has clearly moved."""
        if "react" not in loc or t < 6 * 52:
            return
        now = {k: float(loc[k][0]) for k, *_ in self.TEMPER}
        if self._temper_told is None:
            self._temper_told = now; self._temper_evs = []
            return
        moved = []; keys = []; sg = np.zeros(len(self.TEMPER))
        for i, (k, step, up, down) in enumerate(self.TEMPER):
            d = now[k] - self._temper_told[k]
            if abs(d) >= step:
                moved.append(up if d > 0 else down); keys.append(f"{k}{d:+.2f}"); self._temper_told[k] = now[k]
                sg[i] = np.sign(d) / step
        if moved:
            line = self._temper_cause(moved, keys, sg) if GAME["lines_tied"] else None
            self._say(line or self.story.temperament(moved, keys), 0, "temper", temper={k: round(v, 2) for k, v in now.items()})

    def _temper_cause(self, moved, keys, sg):
        """Item 6: the temperament line naming the told event of the stretch whose week moved it most the way it went
        (Library TEMPER_CAUSE), or None (today's line) when no told event moved it that way. An event it named is not named
        again within TEMPER_AGAIN weeks (a moment that comes back would otherwise be the cause year after year)."""
        evs, self._temper_evs = self._temper_evs, []
        T = getattr(ES, "TEMPER_CAUSE", None)
        named = self.__dict__.setdefault("_temper_named", {})
        sc = [(float(d @ sg), n) for d, n in evs if self.t - named.get(n, -10 ** 6) >= TEMPER_AGAIN]
        if not T or not sc or max(sc)[0] <= 0:
            return None
        ev = max(sc)[1]; named[ev] = int(self.t)
        return self.story.fill(self.story.pick(T).replace("{event}", ev), ctx=dict(m=mk("T", ",".join(keys), ", and ".join(moved))))
