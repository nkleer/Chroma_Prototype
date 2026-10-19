"""Game's methods for what the player sees: status, HUD, routine, family, news, cast, saves, plans, identity, health, the Book and the review.

Part of class Game (game.py), which inherits ViewsMixin; moved out of game.py verbatim. A method here reads
module names through the imports below, the same objects game.py has, and self for everything on the Game."""
import numpy as np
import re
from game_base import (C, CNAME, COLORS, CTX_WORDS, E, ESP, F, GAME, IDENT_NAME, KNAMES, NEED_WORD, NEWS_ALL, RNAMES,
    RT, STAGES, STATUS_WORD, X, an, around_word, ident_meaning, ident_name, invest_word, label_name, letters,
    magic_name, mk, need_level_word, place_word, season_of)
from game_words import (ACCEPT0, BODY_SAY, BODY_THE, BODY_WHAT, DECLINE_SAY, DRAWN, ID_LOCAL, INTEG_PUSHES,
    ROLE_STRICT0, SEASON_STEP, STAGE_WORD, TWO_RE, TWO_WORD, accept_word, age_word, clean, fit_word, last_talk,
    life_names, life_paragraph, peace_reading, rel_word, strict_word, voice_empty)


class ViewsMixin:
    # ------------------------------------------------------------------ status
    def status(self):
        loc = self.loc
        if loc is None:
            return "Not started."
        w = E.softmax(loc["z"][0]); a = E.softmax(loc["y"][0])
        kw = E.softmax(loc["k"][0]); habit = loc["habit"][0]
        hs = habit / max(habit.sum(), 1e-9) if habit.sum() > 0 else np.full(C, 0.2)
        rsh = (loc["held"][0] * loc["I"][0]) @ loc["prof"][0]
        role = rsh / rsh.sum() if rsh.sum() > 0 else np.full(C, 0.2)
        inertia = 0.4 * kw + 0.3 * hs + 0.3 * role - 0.2
        doors = loc["doors"](loc["nic"], loc["res"])[0]
        ready = float(loc["plast"][0] * loc["ctrl"][0])
        acc = ready * (loc["SE"][0] / 0.5) * doors
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        Q = float(loc["Q"][0])
        young = int(loc["stage"][0]) < 2
        lbl = self._core_label                   # 5.5: the name, from the last four years' colors
        now = E.identity(w, float(loc["M"][0]), self._prev_label)
        L = []
        L.append(f"{self.name}, age {self.age():.1f}, {STAGES[int(loc['stage'][0])].replace('_', ' ')}. Identity: {label_name(lbl)}"
                 + (f", {self._becoming}" if self._becoming else "") + "."
                 + (f" This year alone: {label_name(now)}." if now and now != lbl else ""))
        L.append("")
        L.append("           " + "  ".join(f"{CNAME[c]:>6}" for c in COLORS))
        L.append("position   " + "  ".join(f"{v * 100:5.0f}%" for v in w) + "   where they are")
        L.append("demand     " + "  ".join(f"{d * 100:+5.0f} " for d in a - w) + "   where they want to move")
        L.append("inertia    " + "  ".join(f"{d * 100:+5.0f} " for d in inertia) + "   how hard they hold on")
        L.append("accelerat. " + "  ".join(f"{v * 100:5.0f}%" for v in acc) + "   how fast they could move now")
        L.append("skill      " + "  ".join(f"{v * 100:5.0f}%" for v in loc["sig"][0]) + "   skillset")
        L.append("belief     " + "  ".join(f"{v * 100:5.0f}%" for v in loc["SE"][0]) + "   mindset: belief they can act that way")
        L.append("lens       " + "  ".join(f"{v * 100:5.0f}%" for v in kw) + "   mindset: what they notice first")
        L.append("voice      " + "  ".join(f"{v * 100:5.0f}%" for v in self.story.voice) + "   how the story is told (past and present identity)")
        L.append("")
        st = self.states(loc)
        if st:
            L.append("state        " + ", ".join(x["word"] for x in st))
        L.append(f"satisfaction {float(loc['content'][0]) * 100:.0f}%   peace {float(loc['peace'][0]) * 100:.0f}%   "
                 f"strain {float(loc['stress'][0]) * 100:.0f}%   pent-up wanting {Q / max(thr, 1e-9) * 100:.0f}% of breaking through"
                 + (" (once a young adult)" if young else ""))
        cond = self.conditions(loc)
        if cond:
            L.append("around them  " + ", ".join(f"{CTX_WORDS[k]}: {around_word(CTX_WORDS[k], v)}" for k, v in cond.items() if abs(v) >= 0.05))
        if "react" in loc:
            L.append(f"temperament  reactivity {float(loc['react'][0]) * 50:.0f}%   steadiness {float(loc['steady'][0]) * 100:.0f}%   "
                     f"baseline mood {float(loc['base_mood'][0]) * 100:.0f}%   outlook {float(loc['outlook'][0]) * 100:.0f}%")
        L.append("resources    " + "  ".join(f"{RNAMES[i]} {loc['res'][0, i] * 100:.0f}%" for i in range(5)))
        if "need" in loc:
            L.append("needs        " + "  ".join(f"{NEED_WORD[n]} {float(v) * 100:.0f}% ({need_level_word(float(v))})"
                                                for n, v in zip(E.NEEDS, loc["need"][0])))
        if self.history["forced"]:
            L.append("trust in you " + "  ".join(f"{CNAME[c]} {v * 100:+.0f}" for c, v in zip(COLORS, self.trust))
                     + f"   (pushes accepted {self.history['accepted']}, resented {self.history['resented']})")
        held = [k for k in range(len(KNAMES)) if loc["held"][0, k]]
        R = self.roles(loc)
        if held:
            for k in held:
                yrs = (self.t - loc["since"][0, k]) / 52
                cl = " - in a clash" if loc["clash0"][0, k] >= 0 else ""
                nm = ", ".join(x["say"] + "".join(f" ({f['say']})" for f in x.get("facets", []))
                               for x in (R["titles"].get(KNAMES[k], []) if R else []))
                L.append(f"title        {KNAMES[k]}{': ' + nm if nm else ''}: {yrs:.0f} years, invested {invest_word(float(loc['I'][0, k]))}, "
                         f"expects {letters(loc['prof'][0, k])}{cl}")
        else:
            L.append("titles       none yet")
        if R and R["statuses"]:
            L.append("status       " + ", ".join(x["say"] for x in R["statuses"]))
        if R and R["perks"]:
            L.append("perks        " + "; ".join(x["pred"] + {"held": "", "suspended": " (on hold for now)", "rusty": " (rusty)"}[x["state"]]
                                                for x in R["perks"]))
        for x in self.goals(loc):
            tail = (f" ({x['horizon']}, due at {x['due']:.0f}; feels {x['felt'] * 100:.0f}%, plans like it come true {x['hint']}; "
                    f"{x['progress'] * 100:.0f}% of the way)" if x["kind"] == "plan" else f" [{x['colors']}]")
            L.append(f"{x['kind']:<12} {x['name']}{tail}, strength {x['strength'] * 100:.0f}%" + (" [your plan]" if x["by_player"] else ""))
        return "\n".join(L)

    def hud(self):
        """Everything the browser's HUD shows, as plain numbers and words (status() is the same for the terminal)."""
        loc = self.loc
        d = dict(name=self.name, age=round(self.age(), 1), setting=self.setting, place=self.story.place,
                 freq=self.freq, detail=self.detail, ledger=self.ledger, over=self.over)
        if loc is None:
            return d
        w = E.softmax(loc["z"][0]); a = E.softmax(loc["y"][0])
        kw = E.softmax(loc["k"][0]); habit = loc["habit"][0]
        hs = habit / max(habit.sum(), 1e-9) if habit.sum() > 0 else np.full(C, 0.2)
        rsh = (loc["held"][0] * loc["I"][0]) @ loc["prof"][0]
        role = rsh / rsh.sum() if rsh.sum() > 0 else np.full(C, 0.2)
        inertia = 0.4 * kw + 0.3 * hs + 0.3 * role - 0.2
        doors = loc["doors"](loc["nic"], loc["res"])[0]
        acc = float(loc["plast"][0] * loc["ctrl"][0]) * (loc["SE"][0] / 0.5) * doors
        dyn = X.dynamics(loc, 0, self._prev_label) if hasattr(X, "dynamics") else None
        if dyn is not None:                          # the engine's own weekly feed (next hand-off), when the pin has it
            inertia = np.asarray(dyn["inertia"]); acc = np.asarray(dyn["accelerator"])
        thr = float(loc["q_thr"][0]) if "q_thr" in loc else float(loc["P"]["q_theta"])
        lbl = self._core_label                   # 5.5: the name, from the last four years' colors
        r = lambda v: [round(float(x), 3) for x in v]
        vl = self._voice_label
        d.update(stage=STAGES[int(loc["stage"][0])].replace("_", " "),
                 label=lbl, guild=ident_name(lbl), magic=magic_name(lbl), meaning=ident_meaning(lbl),
                 voice_label=vl, voice_guild=ident_name(vl) if vl else "", epithet=self._epithet if vl else "",
                 becoming=self._becoming if lbl else "", voice_row=self.voice_view(loc),
                 w=r(w), demand=r(a - w), inertia=r(inertia), acc=r(acc), skill=r(loc["sig"][0]), belief=r(loc["SE"][0]),
                 lens=r(kw), voice=r(self.story.voice),
                 content=round(float(loc["content"][0]), 3), peace=round(float(loc["peace"][0]), 3),
                 stress=round(float(loc["stress"][0]), 3), want=round(float(loc["Q"][0]), 2), want_thr=round(thr, 2),
                 young=int(loc["stage"][0]) < 2,
                 res={RNAMES[i]: round(float(loc["res"][0, i]), 3) for i in range(5)},
                 around={CTX_WORDS[k]: round(float(v), 2) for k, v in self.conditions(loc).items() if abs(v) >= 0.05},
                 around_words={CTX_WORDS[k]: around_word(CTX_WORDS[k], float(v)) for k, v in self.conditions(loc).items() if abs(v) >= 0.05},
                 states=self.states(loc))
        shv = self.shadow_view(loc)
        if shv is not None:                          # item 2: light and shadow, only with the engine's shadows switch on
            d["shadow"] = shv
        hv = self.health_view(loc)
        if hv is not None:                           # v22.5 F1: health's two halves, only with the engine's body or mind on
            d["health"] = hv
        if dyn is not None:
            d["dyn"] = dict(openness=dyn["openness"], window=bool(dyn["window"]), near=dyn["near"], bands=dyn["bands"],
                            parts={k: r(v) for k, v in dyn["inertia_parts"].items()}, readiness=dyn["readiness"])
        d["season_x"] = self.season(loc)
        d["sex"] = self.sex_now(loc)
        gv = self.gender_view(loc)
        d["sexword"] = gv["word"]; d["who"] = gv["rows"]
        if "react" in loc:
            d["temper"] = {k: round(float(loc[k][0]), 2) for k in ("react", "steady", "base_mood", "outlook")}
        d["needs"] = {n: round(float(v), 3) for n, v in zip(E.NEEDS, loc["need"][0])} if "need" in loc else {}
        d["need_thin"] = GAME["need_thin"]
        d["trust"] = self.trust_view(); d["pushes"] = dict(forced=self.history["forced"], accepted=self.history["accepted"],
                                                           resented=self.history["resented"], passed=list(self.history.get("passed", [0, 0])))
        d["inner"] = {k: round(float(np.ravel(loc[v])[0]), 3) for k, v in (("self_control", "dsc"), ("mood", "mood"), ("wound", "wound"),
                                                                          ("gap", "gap_r"), ("horizon", "hzf"), ("formed", "M"))
                      if v in loc}
        d["week"] = int(self.t % 52)
        d["season"] = season_of(self.t)
        d["ident_rule"] = [0.22, 0.18]              # a color joins who they are above .22 and leaves below .18 (engine.identity)
        d["titles"] = [dict(kind=KNAMES[k], years=round((self.t - loc["since"][0, k]) / 52, 1), invested=round(float(loc["I"][0, k]), 2),
                            expects=letters(loc["prof"][0, k]), clash=bool(loc["clash0"][0, k] >= 0))
                       for k in range(len(KNAMES)) if loc["held"][0, k]]
        R = self.roles(loc)
        if R is not None:                           # the titles inside each life domain, statuses, and perks
            g_ = gv["self"]
            gw = lambda x: ({k: gw(v) for k, v in x.items()} if isinstance(x, dict) else [gw(v) for v in x] if isinstance(x, list)
                            else self.gword(x, g_))
            for t_ in d["titles"]:
                t_["named"] = gw(R["titles"].get(t_["kind"], []))
            d["statuses"] = gw(R["statuses"]); d["perks"] = R["perks"]
        d["cast"] = [dict(id=p["id"], name=p["name"], role=p["role"], alive=p["alive"], met=p.get("met"), seen=p.get("seen", 0))
                     for p in self.story.people if p["introduced"]]
        d["spark"] = [[round(a_, 1), round(c_, 2), round(p_, 2)] for (a_, c_), (_, p_) in
                      zip(self.history["content"][-90:], self.history["peace"][-90:])]
        # the life so far, year by year, for the timeline: age, the five colors, satisfaction, peace, identity
        d["river"] = [[round(a_, 1)] + w_ + [round(c_, 2), round(p_, 2), l_] for (a_, w_), (_, c_), (_, p_), (_, l_) in
                      zip(self.history["w"], self.history["content"], self.history["peace"], self.history["label"])]
        d["guilds"] = dict({k: v for k, v in IDENT_NAME.items() if k}, **{l_: ident_name(l_) for _, l_ in self.history["label"] if l_})
        d["goals"] = self.goals()
        pv = self.places_view()
        if pv:
            d["places"] = pv
        try:
            ln = self._lines_view()                     # S5: the lines they will not cross, while sacred is on
        except Exception:
            ln = None
        if ln:
            d["lines"] = ln
        wd = self.world_data()
        if wd:                                          # the outer world: the named cast by layer, and reach by standing
            d["circle"] = self.wv.circle(wd[2], self.t, self.cast_names(wd[2])); d["reach"] = self.wv.reach(wd[3])
            self._want_why_rows(d["circle"])
            era = (wd[0] or {}).get("era")
            if era:
                from worldview import letters_of, era_name
                ls = letters_of(era.get("colors", era.get("letters", "W")))
                d["world_era"] = dict(letters=ls, name=era_name(ls))
        return d

    def _routine_ctx(self):
        loc = self.loc; held = loc["held"][0]; age = self.age(); K = {k: held[i] for i, k in enumerate(KNAMES)}
        R = self.roles(loc) or dict(titles={}, statuses=[], perks=[])
        adj = {E.ADJ_NAMES[i] for i in np.nonzero(np.asarray(loc["adj"][0]))[0]} if "adj" in loc else set()
        who = lambda *roles: next((p for r in roles for p in self.story.alive(r) if p["introduced"]), None)
        slot = {}
        partner, child, friend, parent = who("partner"), who("child"), who("friend"), who("mother", "father")
        for k, p in (("partner", partner), ("child", child), ("friend", friend), ("parent", parent)):
            if p is not None:
                slot[k] = mk("p", p["id"], p["name"])
        job = (R["titles"].get("career") or [None])[0]
        if job is not None:
            j_ = STATUS_WORD.get(job["name"], job["say"])          # with its article: "life as an office worker"
            slot["job"] = j_ if re.match(r"(a|an|the) ", j_) else an(j_)
        com = (R["titles"].get("community") or [None])[0]
        if com is not None or K.get("community"):
            nm = com["name"] if com else ""
            slot["circle"] = next((w for pat, w in self.CIRCLE if re.search(pat, nm)), "the circle" if self.setting == "tribal"
                                  else "the guild" if self.setting == "magic" else "the group")
        stats = {d["name"] for d in R["statuses"]}
        need = set()
        if K.get("career") and "job" in slot:
            need.add("career")
        if 5 <= age < 18 or (age < 26 and any("student" in d["name"] for xs in R["titles"].values() for d in xs)):
            need.add("student")
        if "retiree" in stats or (age >= 66 and not K.get("career")):
            need.add("retired")
        need |= {k for k in ("partner", "children", "faith", "community") if K.get(k) and (k not in ("partner", "children")
                                                                                         or (k == "partner" and partner) or (k == "children" and child))}
        if not K.get("partner") and age >= 18:
            need.add("no_partner")
        if friend:
            need.add("friend")
        if parent:
            need.add("parent_alive")
        need |= {a for a in ("poor", "wealthy", "stressed", "happy", "unhappy", "lonely", "calm", "restless") if a in adj}
        if float(loc["res"][0, 2]) < 0.45:
            need.add("in_poor_health")
        w = E.softmax(loc["z"][0])
        return dict(age=age, world=self.story.wcode, need=need, color=COLORS[int(np.argmax(w))], season=season_of(self.t), slot=slot)

    def routine(self, n=8):
        """Everyday lines for the interlude: what keeps happening in their life at this age (drawn once a year from routine.py,
        with its own seeded stream, so the telling never changes the life or the rest of the story)."""
        if RT is None or self.loc is None or self.over:
            return dict(age=int(self.age()), lines=[])
        a = int(self.age())
        if getattr(self, "_rout", None) is not None and self._rout["age"] == a:
            return self._rout
        ctx = self._routine_ctx()
        cands, wts = [], []
        for text, when in RT.ROUTINE:
            lo, hi = when.get("age", (0, 200))
            if not (lo <= ctx["age"] < hi) or ctx["world"] not in when.get("world", "ETM"):
                continue
            nd = when.get("need", ())
            if any(x not in ctx["need"] for x in nd) or (when.get("season") and when["season"] != ctx["season"]):
                continue
            if when.get("color") and when["color"] != ctx["color"]:
                continue
            cands.append(text); wts.append(1.0 + len(nd) + (1.0 if when.get("color") else 0) + (0.5 if when.get("season") else 0))
        rng = np.random.default_rng(self.seed * 1009 + a)
        k = min(n, len(cands))
        pick = rng.choice(len(cands), size=k, replace=False, p=np.array(wts) / sum(wts)) if k else []
        lines = []
        for i in pick:                      # only {N} and {place} are left for fill(), which never touches the cast for them
            x = re.sub(r"\{(partner|child|friend|parent|job|circle)\}", lambda m: ctx["slot"].get(m.group(1), "\x00"), cands[i])
            if "\x00" not in x and not re.search(r"\{(?!N\}|Ns\}|place\})\w+\}", x):
                lines.append(self.story.fill(x))
        self._rout = dict(age=a, lines=lines, season=ctx["season"], color=ctx["color"])
        return self._rout

    def take_trace(self):
        """The colors (and where they want to be) week by week since the page last asked: [[t, W..G, want W..G], ...]."""
        out, self._trace = self._trace, []
        return out

    def _kin_sync(self, t, loc):
        """With the outer world on, the family is the world's: siblings there at the birth are met quietly as older
        ones, a younger one born later is told; a sibling the world lost without a moment is said goodbye to."""
        first = self._kin_t is None
        self._kin_t = t
        n_e = int(loc["alive"][0, 1]); have = len(self.story.alive("sibling"))
        if n_e > have:
            wd = self.world_data()
            sib = sorted((p_ for p_ in (wd[2] if wd else []) if "sibling" in p_.get("roles", []) and p_.get("alive")),
                         key=lambda p_: -int(p_.get("born_t", 0)))
            sexes = [("f" if p_.get("sex") == "female" else "m") for p_ in sib[:n_e - have]]
            line = self.story.new_kin("sibling", n_e - have, sexes, told=not first and t / 52 >= 1)
            if line:
                self._say(line, 0 if not self.burn_in else 1, "kin")
        if first:
            return
        gap = self.__dict__.setdefault("_kin_gap", {})
        for role, n_w in (("sibling", n_e), ("grandparent", int(loc["alive"][0, 3]))):
            if n_w >= len(self.story.alive(role)):
                gap.pop(role, None)
            elif t - gap.setdefault(role, t) >= self.KIN_WAIT:   # the engine's own record of the death (told with its moment)
                gap.pop(role, None)                         # follows the world's within weeks; after KIN_WAIT, say it
                line = self.story.quiet_deaths(role, n_w, t / 52)
                if line:
                    self._say(line, 0 if not self.burn_in else 1, "death")

    def _world_news(self, r):
        """A big public event of the engine's world, told in the story (spec 1 §8: big public events always). The timeline
        keeps every one; the story does not repeat the same figure's news within NEWS_GAP weeks, nor the same line within two years."""
        if GAME["news_touch"] and not self._news_touches(r):
            return
        wl = self.wv.line(r, {})
        told = self.__dict__.setdefault("_news_t", {})
        key = (r["kind"], r["figure"]) if r.get("figure") is not None else wl[1] if wl else None
        if key is not None and self.t - told.get(key, -10 ** 6) < (self.NEWS_GAP if r.get("figure") is not None else 104):
            return
        if key is not None:
            told[key] = self.t
        if wl:
            self._say(mk("O", f"{r['kind']}|{wl[0]}|1", self.story.fill(wl[1])), 0 if not self.burn_in else 1, "world", kind=r["kind"], icon=wl[0])

    def _news_touches(self, r):
        """F10 (news_touch): whether a big public event touches them enough to be told. Their own place's news, a war, a
        pandemic and a recession always; the rest of the national news from news_age, a law only when it reaches a state
        not told before, a fallen government not again with the election that follows, and one kind at most once in
        news_gap years."""
        k_ = r["kind"]
        if r.get("locality") is not None or k_ in NEWS_ALL:
            return True
        if self.t / 52 < GAME["news_age"]:
            return False
        last = self.__dict__.setdefault("_news_k", {})
        if k_ == "law":
            st_ = self.__dict__.setdefault("_law_told", {})
            if st_.get(r.get("law")) == r.get("state"):
                return False
            st_[r.get("law")] = r.get("state")
            return True
        key_ = "government" if k_ in ("gov_falls", "election") else k_
        if self.t - last.get(key_, -10 ** 9) < GAME["news_gap"] * 52:
            return False
        last[key_] = self.t
        return True

    def _world_place(self, WL, birth=False):
        """Where a life begins and where it moves to (spec 3 §2.5b, §2.6: drawn, discovered as the story opens). birth:
        at the start, the story's birth line names the place (no line of its own)."""
        try:
            pv = WL.PP.place_view(0)
        except Exception:
            return
        from worldview import place_name, loc_key
        l = loc_key(pv.get("society", 0), pv.get("loc", 0))
        if l == self._wloc:
            return
        name = place_name(self.wv.seed, l, self.setting)
        kind = str(pv.get("kind", "")).replace("_", " ")
        a_kind = an(kind) if kind else ""
        if GAME["world_hold"] and kind:                 # v22.5, F12: the story's place is where the world has them
            self.story.place = place_word(kind)
        if birth:
            self._wloc = l
            self.story.birth_place = mk("O", "place|ci-cottage|1", name + (f", {a_kind}" if a_kind else ""))
            return
        soc, home = pv.get("society", 0), pv.get("home_society", 0)
        was = self.__dict__.get("_wsoc", home); self._wsoc = soc
        abroad = soc is not None and soc != home        # emigration (W35-3): the society they move to, and coming home
        where = (f", {a_kind}" if a_kind else "") + (f" in {self.wv.society_name(soc)}" if abroad else "")
        if self._wloc is None:
            line = f"{{N}} is born in {name}" + (f", {a_kind}" if a_kind else "") + "."
        elif abroad and soc != was:
            line = f"{{N}} moves abroad, to {name}{where}."
        elif not abroad and was not in (None, home):
            line = f"{{N}} comes home, to {name}" + (f", {a_kind}" if a_kind else "") + "."
        else:
            line = f"{{N}} moves to {name}{where}."
        first = self._wloc is None
        self._wloc = l
        tag, icon = ("world", "ci-cottage") if first else ("move", "ci-box")
        self._say(mk("O", f"place|{icon}|1", self.story.fill(line)), 0 if not self.burn_in else 1, tag, kind="place", icon=icon)

    def cast_names(self, cast):
        """One family, one set of names: the world's kin (parents, siblings, partner, children, grandparents) take the names
        the story already gave them, matched by role and sex; once matched, a person keeps the name for the life."""
        m = self.__dict__.setdefault("_castname", {})
        used = set(m.values())
        ROLE = dict(parent=("mother", "father"), sibling=("sibling",), partner=("partner",), child=("child",), grandparent=("grandparent",))
        from story import FEM_REF, MAS_REF
        for p in cast:
            if p.get("id") in m:
                continue
            r = next((x for x in ("partner", "parent", "child", "sibling", "grandparent") if x in p.get("roles", [])), None)
            if r is None:
                continue
            sx = "f" if p.get("sex") == "female" else "m"
            roles = ROLE[r] if r != "parent" else (("mother",) if sx == "f" else ("father",))
            def q_sex(q):
                return "f" if FEM_REF.search(q["ref"]) else "m" if MAS_REF.search(q["ref"]) else None
            cs = [q for q in self.story.people if q["role"] in roles and q["name"] not in used]
            if self.story.one_roll:                     # F7: the living keep the living's names, the dead the dead's
                cs = [q for q in cs if q["alive"] == bool(p.get("alive", True))]
            cs = [q for q in cs if q_sex(q) in (sx, None)] or cs
            cs.sort(key=lambda q: q["alive"] != bool(p.get("alive", True)))
            if cs:
                m[p["id"]] = cs[0]["name"]; used.add(cs[0]["name"])
        return m

    def _one_roll(self, loc, kids=False):
        """F7 (the engine's one_roll, outer world on): the kin the world has lost since the last call. Each waits in
        story.due for the next death of its role, so the scene, the funeral and the name are the world's. A child dies
        in the world only after the engine's moment, whose child the story has already named: kids=True, after the
        week's lines, gives the world's child that name (and the living child's name to whoever the world had under it)."""
        if not kids:
            evs = loc["events"][0]; i_ = self.__dict__.get("_due_i", 0); self._due_i = len(evs)
            dd = [ev["cast"] for ev in evs[i_:] if isinstance(ev.get("cast"), dict) and ev["cast"].get("kind") == "died"
                  and ev["cast"].get("role") in self.ROLL_ROLES]
            pend = self.__dict__.setdefault("_roll_kids", [])
            pend.extend(d for d in dd if d["role"] == "child")
            dd = [d for d in dd if d["role"] != "child"]
        else:
            dd, self._roll_kids = self.__dict__.get("_roll_kids", []), []
        if not dd:
            return
        wd = self.world_data()
        m = self.cast_names(wd[2]) if wd else self.__dict__.setdefault("_castname", {})
        sx_ = {c_["id"]: ("f" if c_.get("sex") == "female" else "m") for c_ in (wd[2] if wd else [])}
        claimed = self.__dict__.setdefault("_roll_dead", set())   # story people already matched to a world death
        from story import FEM_REF, MAS_REF
        for d in dd:
            cid, r = d.get("cid"), d["role"]
            roles = self.ROLL_ROLES[r]
            if r == "parent" and cid in sx_:
                roles = ("mother",) if sx_[cid] == "f" else ("father",)
            p = next((q for q in self.story.people if q["name"] == m.get(cid) and q["role"] in roles), None)
            if p is not None and not p["alive"]:
                claimed.add(p["id"]); continue
            gone = [q for q in self.story.people if q["role"] in roles and not q["alive"] and q["id"] not in claimed
                    and self.story.age - q.get("gone", -99.0) < 0.25] if kids else []
            if gone:                                    # the story told this death first: the world's person is that one
                q = gone[-1]; claimed.add(q["id"])
                if p is not None:                       # whoever the world had under that name takes the living one's
                    for k_, v_ in list(m.items()):
                        if v_ == q["name"] and k_ != cid:
                            m[k_] = p["name"]
                m[cid] = q["name"]
                continue
            if p is None:
                used = set(m.values()); due_ = {q["id"] for _, q in self.story.due}
                cs = [q for r_ in roles for q in self.story.alive(r_) if q["name"] not in used and q["id"] not in due_]
                sx = sx_.get(cid)
                cs = [q for q in cs if ("f" if FEM_REF.search(q["ref"]) else "m" if MAS_REF.search(q["ref"]) else sx) == sx] or cs
                if not cs:
                    continue
                p = cs[0]; m[cid] = p["name"]
            if all(q is not p for _, q in self.story.due):
                self.story.due.append((r, p))

    def _due_told(self, t):
        """F7: a death the world has had that no engine death of its role claims within DUE_WAIT weeks is told quietly,
        so the story never keeps naming them as alive (siblings and grandparents have their own wait in _kin_sync)."""
        since = self.__dict__.setdefault("_due_t", {})
        for r, p in list(self.story.due):
            if not p["alive"] or r in ("sibling", "grandparent", "child"):
                continue
            if t - since.setdefault(p["id"], t) >= self.DUE_WAIT:
                line = self.story.quiet_deaths(p["role"], len(self.story.alive(p["role"])) - 1, t / 52)
                if line:
                    self._say(line, 0 if not self.burn_in else 1, "death")

    def world_save(self):
        """The world this life leaves behind, for a later life to begin in (spec 1: legacy worlds): the world's whole
        state, and the character's cast for a grandchild's line. None without a world."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        if WL is None:
            return None
        d = dict(key=f"{int(WL.W._seed)}-{int(WL.t0)}-{int(WL.W.t)}", seed=int(WL.W._seed), name=self.name,
                 age=round(self.age(), 1), alive=getattr(self, "died", None) is None, world=WL.W.save())
        try:
            w = np.asarray(self.loc["w"][0], float) if "w" in self.loc else None
            d["people"] = WL.PP.save(0, w=w, alive=False)
        except Exception:
            pass
        return d

    def places_view(self):
        """Item 15's player view, "your places": the haunts they go to (the Library's name for the place, its kind, the face
        that leads it, whether a setting of theirs meets there), their standing in each sphere they have climbed in, and the
        town's spheres by their share of the hours. Display only; empty while the engine's sphere switches are off."""
        WL = self.loc.get("WL") if isinstance(self.loc, dict) else None
        if WL is None or ESP is None:
            return None
        try:
            hi = WL.PP.haunts_info(0)
        except Exception:
            return None
        if not hi["haunts"] and not hi["rungs"]:
            return None
        nm = lambda d, k: (d.get(k) or {}).get("name", k)
        haunts = []
        for h in hi["haunts"]:
            H = ESP.HAUNT.get(h["kind"], {}); ns = H.get("names") or [nm(ESP.PLACE, h["kind"])]
            haunts.append(dict(name=ns[h["name"] % len(ns)], kind=nm(ESP.PLACE, h["kind"]), sphere=h["sphere"],
                               sphere_name=nm(ESP.SPHERE, h["sphere"]), lead=h["leads"][-1], lead_name=nm(ESP.FACE, h["leads"]),
                               lead_line=(ESP.FACE.get(h["leads"]) or {}).get("line", ""), faces=h["faces"],
                               keeper=H.get("keeper", ""), setting=h["setting"]))
        LADDER = ["newcomer", "regular", "known", "pillar", "leader"]       # world_keys.LADDER, the engine's order
        rungs = [dict(sphere=s_, sphere_name=nm(ESP.SPHERE, s_), rung=LADDER.index(r_), word=ESP.RUNG[s_][LADDER.index(r_)],
                      question=(ESP.SPHERE.get(s_) or {}).get("question", ""))
                 for s_, r_ in hi["rungs"].items() if r_ in LADDER and s_ in ESP.RUNG]
        rungs.sort(key=lambda r: -r["rung"])
        town = []
        try:
            l = int(WL.PP.loc[0]); sp = WL.W._sph_portrait() if getattr(WL.W, "sph_s", None) is not None else []
            sp = next((x["spheres"] for x in sp if x["town"] == l), {})
            town = sorted((dict(sphere=s_, sphere_name=nm(ESP.SPHERE, s_), hours=v["hours"], lead=v["leads"][-1],
                                lead_name=nm(ESP.FACE, v["leads"])) for s_, v in sp.items()), key=lambda x: -x["hours"])
        except Exception:
            town = []
        P = dict(haunts=haunts, rungs=rungs, town=town)
        try:
            self._social_places(WL, hi, P)              # v22.4 (S1, S3, S4, S7): only while their switches are on
        except Exception:
            pass
        return P

    def world_data(self):
        """What the outer world shows now (world-hooks-for-engine.md), or None while the engine has no world."""
        if self.world_source is None:
            return None
        try:
            return self.world_source(self.t)
        except Exception:
            return None

    def goals(self, loc=None):
        """The dreams, passions and plans the character holds now; a plan comes with its foreseen outcome (foresee.py):
        the felt odds, and reality only as a rough hint, as Emren asked."""
        loc = self.loc if loc is None else loc
        if loc is None or "gk" not in loc:
            return []
        out = []
        for j in np.nonzero(loc["gk"][0] >= 0)[0]:
            kind = E.G_KINDS[int(loc["gk"][0, j])]; d = int(loc["gd"][0, j]); mix_ = loc["gm"][0, j]
            g_d, g_p, verb = self.story.goal_words(kind, KNAMES[d] if d >= 0 else "", mix_, int(loc["gid"][0, j]))
            item = dict(j=int(j), id=int(loc["gid"][0, j]), kind=kind, name={"dream": g_d, "passion": g_p}.get(kind, verb),
                        domain=KNAMES[d] if d >= 0 else "", colors=letters(np.asarray(mix_, float)),
                        strength=round(float(loc["gs"][0, j]), 2), source=E.G_SOURCES[int(loc["gsrc"][0, j])],
                        by_player=bool(loc["gby"][0, j]))
            info = self.story.dreams.get(item["id"])
            if info:                                # a dream the engine named from the Library's catalogue
                item["dream"] = info["name"]
            if kind == "plan":
                f = F.foresee(loc, 0, j)
                item.update(felt=f["felt"], hint=f["hint"], horizon=f["horizon"], due=f["due_age"], progress=f["progress"],
                            left_out=f["left_out"], felt0=f["felt_at_start"])
                life = self.story.life_words(item["id"]) if f["horizon"] == "life" else None
                if life:
                    item["name"] = life
            out.append(item)
        order = dict(passion=0, plan=1, dream=2)
        return clean(sorted(out, key=lambda x: (order[x["kind"]], -x["strength"])))

    def _paused_locals(self):
        """The engine's locals where the run waits now (a plan made here takes effect from this week)."""
        return self._msg[2] if self._msg is not None and not self.over else None

    def plan_preview(self, horizon="year", domain=None, mix=None):
        S = self._paused_locals()
        if S is None or "gk" not in S:
            return None
        if domain and S["held"][0, KNAMES.index(domain)]:
            return dict(blocked=f"{self.name} already has {'a ' + domain if domain != 'children' else 'children'}")
        f = F.preview(S, 0, horizon, domain, mix)
        f["name"] = self.story.goal_words("plan", domain or "", np.asarray(F._mix(S, 0, None if mix is None else np.asarray(mix, float))), 0)[2]
        return clean(f)

    def plan_add(self, horizon="year", domain=None, mix=None):
        S = self._paused_locals()
        if S is None or "gk" not in S:
            return -1, "plans need engine v7"
        j, f = F.add_plan(S, 0, horizon, domain, None if mix is None else np.asarray(mix, float))
        return j, clean(f)

    def plan_drop(self, j):
        S = self._paused_locals()
        return S is not None and F.drop_plan(S, 0, int(j))

    def cp_hud(self, numbering):
        """The pending checkpoint for the browser: the scene, and each option with its odds and what may follow."""
        cp = self.pending
        if cp is None:
            return None
        rev = {v: k for k, v in numbering.items()}
        meta = self.sitmeta.get(cp["sit"], {}); tags = meta.get("tags", []); marks = meta.get("marks", [])
        opts = []
        for o in cp["options"]:
            col = o["colors"]
            means, _, ends = col.partition(">")
            v = cp.get("view") or {}
            opts.append(dict(n=rev.get(o["idx"]), label=o["label"], colors=col,
                             means=[] if col == "-" else means.split("+"), ends=[] if col == "-" else (ends or means).split("+"),
                             felt=round(o["felt"], 3), hint=o["hint"], lean=round(o["lean"], 3), status=o["status"],
                             rel=round(o["rel"], 3), rel_word=rel_word(o["rel"]), why=o["why"], commit=o["commit"],
                             clash=o.get("clash", []),
                             own=o["idx"] == cp["own"], follows=o["follows"],
                             reality=o.get("reality"), heart=o.get("heart"), head=o.get("head"), drivers=o.get("drivers"),
                             heart_pick=o["idx"] == v.get("heart"), head_pick=o["idx"] == v.get("head"),
                             accept="their own pick" if o["idx"] == cp["own"] else o.get("acc") or accept_word(o["rel"]), k=int(o["idx"]),
                             trust=round(o.get("trust", 0.0), 3), resent=round(self._resent(o["rel"] * o.get("era_k", 1.0), o.get("trust", 0.0)), 3),
                             era=o.get("era", 0.0), wcause=o.get("wcause"),
                             needs=o.get("needs"), closed=o.get("closed"), helped=o.get("helped", []), roles_fx=o.get("roles_fx", []),
                             base=round(o["base"], 2) if o.get("base") is not None else None,
                             tag=tags[o["idx"]] if o["idx"] < len(tags) else "",
                             mark=marks[o["idx"]] if o["idx"] < len(marks) else ""))
            if o.get("seen"):                           # S6, only while seen_done is on
                opts[-1]["seen"] = o["seen"]
            if o.get("at_stake"):                       # Stakes on the card, only while stakes is on
                opts[-1]["at_stake"] = o["at_stake"]
            if o.get("commit_say"):                     # v22.5, F12 (world_hold): the world's word for a career
                opts[-1]["commit_say"] = o["commit_say"]
            if o.get("bold"):                           # Bold ways: the chip, the fit hint, what it wins and costs
                opts[-1]["bold"] = o["bold"]
            if o.get("arrows"):                         # v24 hover arrows, only while arrows is on
                opts[-1]["arrows"] = o["arrows"]
        sp = self.shadow_pull(self.loc, (cp.get("view") or {}).get("heart")) if self.loc is not None else None
        if sp is not None:                           # item 2: once seen, the heart's pick their shadow drives carries a mark
            for o in opts:
                if o["heart_pick"]:
                    o["shadow"] = sp
        # a perk that helps most of this moment's options says little on each row: the row names one that helps only a few
        cnt = {}
        for o in opts:
            for h in o["helped"]:
                if h.get("plus", 0) >= 3:
                    cnt[h["name"]] = cnt.get(h["name"], 0) + 1
        for o in opts:
            o["helped_row"] = next((h["name"] for h in o["helped"] if h.get("plus", 0) >= 3 and cnt[h["name"]] <= 2), None)
        st = cp["stakes"]
        v = cp.get("view")
        voice = None if v is None else dict(key=v["key"], line=v["line"], asides=v["asides"], self_control=v["self_control"],
                                            heart_driver=v["heart_driver"], head_driver=v["head_driver"], color=v["voice_color"])
        d = dict(age=round(cp["age"], 1), title=cp["title"], stakes=round(st, 2), season=self.season(),
                    stake_word="very high" if st >= 1.2 else "high" if st >= 0.95 else "moderate",
                    scene=cp.get("scene", ""), extra=cp.get("extra", ""), thought=cp.get("thought", ""), recon=cp["recon"],
                    thread=cp.get("thread"), era=self.era_view(), options=opts, voice=voice, art=dict(sit=cp["sit"], life=meta.get("life", ""), tier=meta.get("tier", ""),
                                                         tone=meta.get("tone", ""), variant_of=meta.get("variant_of", ""), recon=cp["recon"]))
        if GAME["stakes"]:                              # Stakes on the card: up to two lasting-change chips on each card
            d["stake_card"] = True
        return d

    def season(self, loc=None):
        """Emren's point 6: the crossing they are in (a stage or a new title), in words, or None (engine explain.season)."""
        loc = self.loc if loc is None else loc
        need = ("s", "sea_k", "sea_t0", "sea_done", "t", "P", "L")
        x = X.season(loc, 0) if loc is not None and hasattr(X, "season") and all(k in loc for k in need) else None
        if not x:
            return None
        into = STAGE_WORD.get(x["name"], x["name"].replace("_", " ")) if x["kind"] == "stage" else x["name"]
        return dict(kind=x["kind"], into=into, step=int(x["step"]), step_word=SEASON_STEP.get(int(x["step"]), ""),
                    this_week=x["this_week"], transform=x["transform"], weeks_in=x["weeks_in"], weeks_left=x["weeks_left"])

    def _idv(self, loc, k):
        """One of the engine's per-person identity values (for-the-engine.md §6), or None while the pin has none. The
        engine keeps some under its own names in the week's state (chroma-engine/sex-gender.md): ID_LOCAL maps them."""
        if loc is None:
            return None
        if k not in loc and k in ID_LOCAL:
            name, col = ID_LOCAL[k]
            if name not in loc:
                return None
            v = np.asarray(loc[name]); v = np.ravel(v[0] if v.ndim >= 2 else v)     # (1, k) per person, (1,) or a scalar
            x = v[col] if col is not None and v.size > col else v[0] if v.size else None
            if x is None:
                return None
            x = x.item() if hasattr(x, "item") else x
            if k == "role_fit":
                return 1 - float(x)
            if k == "role_strict" and "faith_given" in loc and "I" in loc:    # plus half a strongly held family faith
                try:
                    x = min(1.0, float(x) + 0.5 * float(np.ravel(loc["faith_given"])[0]) * float(np.asarray(loc["I"])[0, E.KIDX["faith"]]))
                except Exception:
                    pass
            return x
        if k not in loc:
            return None
        v = np.ravel(np.asarray(loc[k]))
        return v[0].item() if v.size else None

    def _found(self, loc, k):
        """Whether the character has found this about themselves by now (the engine's found_* week, never before)."""
        w = self._idv(loc, "found_" + k)
        return w is not None and 0 <= w <= self.t

    def _mark(self, loc, name):
        L = self.L
        if loc is None or name not in L.get("MARKS", []) or "mark_n" not in loc:
            return False
        return bool(np.asarray(loc["mark_n"])[0][L["MARKS"].index(name)] > 0)

    def gender_view(self, loc=None):
        """Who they are, as far as the story has found it (N1d): the role their world expects (f, m or x for the words),
        how they name themselves, and the sheet's lines. Nothing hidden shows before the week it is found."""
        loc = self.loc if loc is None else loc
        raised = self.sex_now(loc)
        rs = {"female": "f", "male": "m"}.get(raised)
        inter = bool(self._idv(loc, "intersex")) if self._idv(loc, "intersex") is not None else self.born_intersex
        gs = self._idv(loc, "gender_self") if self._found(loc, "gender") else None
        named = self._mark(loc, "named their gender")
        own = None
        if gs is not None and gs > 0:
            own = "x" if gs == 2 else {"f": "m", "m": "f"}.get(rs)
        selfg = own if (own and named) else rs
        acc = self._idv(loc, "accept_trans"); acc = ACCEPT0.get(self.setting, 0.5) if acc is None else acc
        seen = own if (own and named and acc >= 0.5) else rs
        age = self.age()
        rows = []
        if rs:
            rows.append(["Born", ("intersex, raised as " + {"f": "a girl", "m": "a boy"}[rs]) if inter else {"f": "a girl", "m": "a boy"}[rs],
                         "The body they were born with, chosen at setup or drawn at real rates."])
        elif inter:                         # before the first week: the engine has not yet drawn how they are raised
            rows.append(["Born", "intersex", "The body they were born with, chosen at setup or drawn at real rates."])
        if gs is not None:
            g_ = own or rs
            word = {"f": "a woman", "m": "a man", "x": "neither, or both"}.get(g_, "")
            how = "" if gs == 0 else (", and lives as themselves" if named else ", told a few" if self._mark(loc, "came out") else ", known only to them")
            rows.append(["Knows themselves as", word + how, "Who they know themselves to be. Found in play at real rates, never chosen and never changed by what they do."])
        at = self._idv(loc, "attr") if self._found(loc, "attr") else None
        if self._found(loc, "ace") and self._idv(loc, "ace"):
            rows.append(["Drawn to", "no one in that way", "Who they are drawn to, as the story found it."])
        elif at is not None and rs:
            o, s_ = ("men", "women") if rs == "f" else ("women", "men")
            out = "" if at < 2 else (", and out" if self._mark(loc, "came out") else ", not out")
            rows.append(["Drawn to", DRAWN[int(at)].format(o=o, s=s_) + out, "Who they are drawn to, as the story found it."])
        st = self._idv(loc, "role_strict"); st = ROLE_STRICT0.get(self.setting, 0.3) if st is None else st
        fit = self._idv(loc, "role_fit")
        rows.append(["What their world expects", strict_word(st) + ("" if fit is None or not rs else ", and " + fit_word(fit)),
                     "How firmly their world, their family's faith and the people around them expect them to live as a "
                     + ("girl or woman" if seen == "f" else "boy or man" if seen == "m" else "girl or a boy") + " should here, and how that sits with them. "
                     "Living outside it costs more where the world is strict."])
        return dict(raised=rs, self=selfg, seen=seen, word=age_word(selfg, age), seen_word=age_word(seen, age), rows=rows,
                    strict=st, named=named, own=own)

    def gword(self, text, g=None):
        """Two-word titles in the character's own words: wife or husband, mother or father... (N1d §3)."""
        if not isinstance(text, str) or " or " not in text:
            return text
        g = g or (self.gender_view()["self"] if self.loc is not None else None)
        k = {"f": 0, "m": 1, "x": 2}.get(g)
        return text if k is None else TWO_RE.sub(lambda m_: TWO_WORD[m_.group(1)][k], text)

    def rename(self, new):
        """A new name the character takes when they name their gender (N1d §4); the story uses it from now on."""
        new = (new or "").strip()[:24]
        if not new or new == self.name:
            return False
        old = self.name
        self.name = new; self.story.name = new
        self.history.setdefault("names", []).append((round(self.age(), 1), old, new))
        self._say(f"From now on, {new}.", 0, "moment")
        if isinstance(self.resolution, dict):
            self.resolution.pop("rename", None)
        return True

    def sex_now(self, loc=None):
        """'female' or 'male' as set up or drawn by the engine (None before the run has it)."""
        loc = self.loc if loc is None else loc
        if loc is None or "female" not in loc:
            return self.sex
        return "female" if bool(np.asarray(loc["female"])[0]) else "male"

    def _title_now(self, loc):
        """The title that brings them to this moment, for the Library's {title} slot (engine next hand-off)."""
        self.story.title_now = X.title_held(loc, 0) if hasattr(X, "title_held") and "s" in loc else None

    def _body_told(self, ev):
        """v22.5 F1 and F2: a line for the body's or the mind's own turn (a condition, a serious illness, an injury, a low
        season, anxiety, numbing) or a last decline, in BODY_SAY's and DECLINE_SAY's words. The Library's own moments tell
        theirs (the engine does not log those twice)."""
        if "decline" in ev:
            c = ev["decline"]["cause"]
            kd = "old" if c == "old age" else "serious" if c in ("of cancer", "of heart disease", "after a stroke", "of lung disease") else "condition"
            self._say(DECLINE_SAY[kd].format(name=self.name), 0, "decline", cause=c, weeks=int(ev["decline"].get("weeks", 0)))
            return
        b = ev["body"]; nm = b.get("name", ""); what = b["what"]
        if b["kind"] == "condition" and what == "begins" and b["age"] < 16:
            what = "begins young"
        elif b["kind"] == "serious" and what == "begins" and nm == "a stroke":
            what = "begins stroke"
        lv, say = BODY_SAY.get((b["kind"], what), (None, ""))
        if lv is None or self.burn_in and lv > 0:
            return
        self._say(say.format(name=self.name, what=BODY_WHAT.get(nm, nm), the=BODY_THE.get(nm, "it")), lv, "body",
                  kind=b["kind"], what=b["what"], **({"name": nm} if nm else {}))

    def health_view(self, loc):
        """v22.5 F1: health's two halves for the HUD (body and mind, 0 to 1), what weighs on them now (long-term
        conditions, a serious illness, a low season, anxiety, numbing) and whether a last decline has begun. None while the
        engine's body and mind switches are off (or the pin has neither)."""
        if loc is None or not loc.get("HM_ON") or "body_v" not in loc:
            return None
        t = self.t
        cond = [E.COND_KINDS[int(k)] for w_, k in zip(loc["bd_cw"][0], loc["bd_ck"][0]) if w_ > 0 and k >= 0] if "bd_cw" in loc else []
        sk = int(loc["bd_sk"][0]) if "bd_sk" in loc else -1
        me = loc["md_end"][0]
        return dict(body=round(float(loc["body_v"][0]), 3), mind=round(float(loc["mind_v"][0]), 3), conditions=cond,
                    serious=E.SER_KINDS[sk] if sk >= 0 else "",
                    threats=[k for k, e_ in zip(("low season", "anxiety", "numbing"), me) if e_ > t],
                    decline=bool(loc["dl_at"][0] > -10 ** 6))

    def _on_death(self, t, loc):
        """The character's own death (engine P["self_death"]): the story tells it and the life ends here."""
        died = loc.get("died") or []
        cause = died[-1][2] if died else "illness"
        age = int(t / 52)
        if cause.startswith("through "):
            how = f"after choosing to {cause[len('through '):]}"
        else:
            how = {"illness": "of an illness", "old age": "of old age"}.get(cause, cause)
        self._say(f"{self.name} dies at {age}, {how}.", 0, "death")
        self.died = dict(age=round(t / 52, 1), cause=cause, how=how)
        self.over = True; self.result = None
        self._life_review()
        return "over"

    def _gift_fit(self, o):
        """How well a chosen act fits what they are good at: their mean skill in the ways it uses, against their best
        skill (1 = their strongest way). None for doing nothing."""
        if self.loc is None or "sig" not in self.loc or not o.get("colors") or o["colors"] == "-":
            return None
        ways = [c for c in o["colors"].partition(">")[0].split("+") if c in COLORS]
        sig = np.asarray(self.loc["sig"][0], float)
        if not ways or sig.max() <= 0:
            return None
        return float(np.clip(np.mean([sig[COLORS.index(c)] for c in ways]) / sig.max(), 0, 1))

    # ------------------------------------------------------------------ the Book of Moments (Emren chose "Book and peace", 21:44)
    def life_id(self):
        first = self.history["names"][0][1] if self.history.get("names") else self.name   # a new name keeps the life's id
        return f"{self.seed}-{first}-{self.setting}-{int(self.start_age)}"

    def book(self):
        """What this life has met so far, for the Book of Moments the page keeps across lives: moments (situations and
        life events), deeds (the engine's marks), titles ever held, identities lived. Keys match book_catalog()."""
        o = self.result if self.over and self.result is not None and "sit_n" in self.result else None
        loc = self.loc
        if o is None and loc is None:
            return None
        L = self.L
        sit_n = np.asarray((o or loc)["sit_n"][0])
        mom = ["s|" + L["names"][i] for i in np.nonzero(sit_n > 0)[0] if L["names"][i] != "an ordinary week"]
        evr = [e_["name"] for e_ in L.get("EVR", [])]
        mom += ["e|" + n_ for n_ in dict.fromkeys(evr[int(j)] for _, _, j, _ in (o or loc)["read_log"] if int(j) < len(evr))]
        mk_n = np.asarray(o["marks"]["n"][0] if o is not None else loc.get("mark_n", np.zeros((1, 0)))[0])
        deeds = [L["MARKS"][i] for i in np.nonzero(mk_n > 0)[0]] if len(mk_n) else []
        titles = []
        GR = L.get("ROLES")
        if GR is not None:
            ever = o["roles"]["ever"][0] if o is not None and o.get("roles") else loc.get("r_ever", [None])[0]
            if ever is not None:
                titles = [GR["names"][i] for i in np.nonzero(np.asarray(ever)[:GR["NT"]])[0]]
        idents = list(dict.fromkeys(l_ for _, l_ in self.history["label"] if l_))
        d = dict(id=self.life_id(), name=self.name, setting=self.setting, start=round(self.start_age, 1), age=round(self.age(), 1),
                 over=bool(self.over), moments=mom, deeds=deeds, titles=titles, idents=idents,
                 long=list(dict.fromkeys(("made|" if x["made"] else "missed|") + x["name"] for x in self.history["long"])))
        if self.over and getattr(self, "review", None):
            r = self.review
            d.update(final=r["final_label"], reading=r["reading"])
        v = self.history["voice"]                    # item 3: the Book's Your Voice page adds the lives up
        d["voice"] = dict(n=v["n"], steer=v["steer"], ax=v["ax"], line=(getattr(self, "review", None) or {}).get("voice", {}).get("book", "")
                          if self.over else "")
        if self.history.get("returns"):              # Picks come back: each pick that came back, with the pick it came from
            d["returns"] = [dict(a=x["seed"]["age"], m=x["seed"]["moment"], b=x["age"], n=x["moment"]) for x in self.history["returns"]]
        if self.history.get("bold"):                 # Bold ways: each try (taken, won or lost), with its link
            d["bold"] = self._bold_book()
        return d

    def _life_review(self):
        h = self.history
        adult = [c for a, c in h["content"] if a >= 18]; adultp = [p for a, p in h["peace"] if a >= 18]
        ful = float(np.mean(adult)) if adult else 0.0
        ser = float(np.mean(adultp)) if adultp else 0.0
        # F13 (v22.4.1): read over the pushes, not over every pick of the life (hundreds, which hid even pushes "against
        # everything in them"); at least INTEG_PUSHES in the divisor, so one or two pushes cannot sink a life of its own
        n_rel = max(len(h["rel"]), INTEG_PUSHES)
        integ = 1 - float(np.sum(h["rel"])) / n_rel if h["rel"] else 1.0
        if GAME["own_ix"] and h["rel"] and len(h["rel_way"]) == len(h["rel"]):   # S2: a push in a way that became theirs
            integ = 1 - sum(r * (1 - (float(np.asarray(wy) @ self.ix) if wy is not None else 0.0))   # counts as their own by it
                            for r, wy in zip(h["rel"], h["rel_way"])) / n_rel
        o = self.result
        w = o["w"][0] if o is not None else E.softmax(self.loc["z"][0])
        # F13: one list of who they were, the chapter headings' names (history "name", _yearly), for the headings, the
        # review and the song alike; the year-by-year reading (history "label") swings too often to be a life's path
        labels = life_names(h)
        path = []
        for l in labels:
            if not path or path[-1] != l:
                path.append(l)
        gifts = float(np.mean(h["gift"])) if h["gift"] else None
        self.review = dict(epitaph=self.story.epitaph(w), fulfilment=ful, serenity=ser, integrity=integ, gifts=gifts,
                           final=label_name(labels[-1] if labels else ""), final_label=labels[-1] if labels else "",
                           path=[ident_name(l) for l in path], path_labels=list(path), paths=len(path),
                           forced=h["forced"], own=h["own"], accepted=h["accepted"], resented=h["resented"], trust=self.trust_view(),
                           passed=list(h.get("passed", [0, 0])),
                           age=round(self.age(), 1), died=getattr(self, "died", None),
                           long_shots=[dict(say=x["say"], made=x["made"], age=x["age"], odds=x["odds"], words=x["words"]) for x in h["long"]])
        self.review["reading"] = peace_reading(ful, ser, integ, gifts)
        self.review["story"] = life_paragraph(self.story.fill("{N}"), h, self.review, self.setting)
        cl = self._lines_closing()                           # S5: how their sacred lines stood at the end
        if cl:
            self.review["story"] += "\n\n" + cl
        self.review["voice"] = self.voice_review(h)          # item 3: the voice's last sentence and the Book's line
        vr = self.review["voice"] or {}
        if vr.get("end"):                                    # the voice's last sentence closes the song, before the last talk
            self.review["story"] += "\n\n" + vr["end"]
        # the last conversation with the voice (earth_story.py LAST_TALK) has no place of its own on the page yet: its own
        # field, and the song's last stanza after a blank line
        h.setdefault("voice", voice_empty())["share"] = vr.get("share", 0.0)
        self.review["last_talk"] = last_talk(self.story.fill("{N}"), self.story.fill("{Ns}"), h, self.review, self.setting)
        if self.review["last_talk"]:
            self.review["story"] += "\n\n" + self.review["last_talk"]
