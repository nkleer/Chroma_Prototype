"""Game's methods for the run between checkpoints: steers, checkpoints and their options, resolutions, hindsight, turning points.

Part of class Game (game.py), which inherits CheckpointsMixin; moved out of game.py verbatim. A method here reads
module names through the imports below, the same objects game.py has, and self for everything on the Game."""
import numpy as np
import re
from game_base import (ADJ, ADJ_LOOK, BOLD_IX, C, CNAME, COLORS, DRIVER_WORD, E, EP, FREQ, GAME, KNAMES, NEED_WORD, STAGES, X,
    act, bix, chooses, ident_name, letters, lever_info, mk, need_level_word, push_words, res_names, role_info, world_says)
from game_words import (ACC_FROM_ENGINE, PRESSURE, RARE_SHARE, STAKE_KIND, STAKE_MARK, STAKE_NEAR, STAKE_SOON,
    THREAD_COMMIT, THREAD_GOAL, accept_word, clash_with, clean, hint, long_shot_words, reluctance, stake_risk)
from story_base import LIB_ECHO, LIB_GONE, PERSON_SLOTS
from game_base import F


class CheckpointsMixin:
    def _light_steer(self, loc, cp, c):
        """P3: a light steer toward color c. Their own pick is drawn again with the steer added to each option's pull, as
        the engine's P["steer"] does before the draw (same formula; the moment is put to the player after the engine's
        draw, so the game draws it here). Returns the option and dict(color, share): the share of the drawn act's odds
        that the steer gave it, which is the share of a push's cost it carries."""
        P = loc["P"]; U = np.asarray(loc["U"][0], float); dn = np.asarray(loc["do_nothing"][0], bool)
        seen = np.asarray(loc["seen"][0], bool) & np.asarray(loc["mask"][0], bool)
        tau = float(P["tau0"] * (1 + 0.5 * float(loc["stress"][0])))
        m = np.asarray(loc["m"][0], float); mix = np.zeros(C); mix[COLORS.index(c)] = 1.0
        sU = np.where(dn, 0.0, GAME["light_k"] * (5 * (m @ mix) - 1))
        lg0 = np.where(seen, U / tau, -np.inf); lg1 = np.where(seen, (U + sU) / tau, -np.inf)
        p0 = np.exp(lg0 - lg0.max()); p0 /= p0.sum(); p1 = np.exp(lg1 - lg1.max()); p1 /= p1.sum()
        k = int((p1.cumsum() > self._prng.random()).argmax())
        if k not in cp["by_idx"]:
            return None, None
        share = float(np.clip(1 - p0[k] / max(p1[k], 1e-12), 0.0, 1.0))
        return k, dict(color=c, share=round(share, 3), moved=round(float(p1[k] - p0[k]), 3))

    def _era_fit(self, loc, T):
        """P3: how much an act's ways go with the era's pull (1) or against it (-1); 0 in quiet times. From the engine's
        STATE e_i (the era's strength) and e_p (its colors)."""
        if "e_p" not in loc or "e_i" not in loc:
            return 0.0
        ep = np.asarray(loc["e_p"], float).reshape(-1, C)[0] if np.size(loc["e_p"]) >= C else None
        ei = float(np.asarray(loc["e_i"], float).ravel()[0])
        if ep is None or ei <= 0:
            return 0.0
        a, b = np.asarray(T, float) - 0.2, ep - 0.2
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        return 0.0 if na < 1e-9 or nb < 1e-9 else float(np.dot(a, b) / (na * nb) * min(1.0, ei / GAME["era_full"]))

    def era_view(self, loc=None):
        """P3: the era's pull for the page: its colors as letters and shares, its strength 0 to 1."""
        loc = self.loc if loc is None else loc
        if loc is None or "e_p" not in loc or "e_i" not in loc or np.size(loc["e_p"]) < C:
            return None
        ep = np.asarray(loc["e_p"], float).reshape(-1, C)[0]; ei = float(np.asarray(loc["e_i"], float).ravel()[0])
        return dict(p=[round(float(x), 3) for x in ep], i=round(min(1.0, ei / GAME["era_full"]), 3), letters=letters(ep))

    # ------------------------------------------------------------------ checkpoints
    def _importance(self, loc, s, a):
        L = loc["L"]
        stakes = float(L["STAKES"][s])
        stage = int(loc["stage"][0])
        commit = bool((L["COMMIT"][s][loc["mask"][0]] >= 0).any())
        rite = stage < len(STAGES) - 1 and bool(L["RIT"][s, stage + 1])
        U_R, U_I = loc["U_R"][0], loc["U_I"][0]
        seen = loc["seen"][0] & ~loc["do_nothing"][0]
        conflict = seen.any() and int(np.argmax(np.where(seen, U_R, -np.inf))) != int(np.argmax(np.where(seen, U_I, -np.inf)))
        return stakes + 0.4 * commit + 0.3 * rite + 0.3 * conflict

    def _checkpoint(self, t, loc, a):
        recon = bool(loc["recon"][0])
        s = int(loc["s"][0])
        if s == self.ORD and not recon:
            return None
        gap_weeks, thr, again = FREQ[self.freq]
        if not recon and self._turn_due(t):
            return self._build_turning(t, loc, a)
        sea = None if recon else self.season(loc)
        self._ret_cand = ret = self._return_of(loc, s) if GAME["returns"] and not recon else None
        if sea and sea["this_week"]:
            # Emren's point 6: a crossing is never a quiet level-up, so each of its season's moments (the crossing, the
            # in-between, settling in, and above all the transforming chance) is put to the player, whatever the pacing
            pass
        elif recon:
            # a commitment in a clash coming up for decision is always a moment for the player (Emren: clash endings
            # are checkpoints); a quieter reconsideration waits like any other moment. Neither repeats too soon.
            kk = int(loc["rk"][0])
            if t - self._last_recon.get(kk, -10 ** 6) < again // 2:
                return None
            if loc["clash0"][0, kk] < 0 and t - self._last_cp < gap_weeks:
                return None
            self._last_recon[kk] = t
        elif GAME["rung_ask"] and self._rung_here(loc, s) and t - self._last_seen.get(s, -10 ** 6) >= again // 2:
            pass                                        # v22.5 proposal: the next rung of a pack career or a summit is asked
        elif ret is not None:
            pass                                        # Picks come back: a return is always put to the player
        elif GAME["bold"] and self._bold_forced(t, s):
            pass                                        # Bold ways: the situation pause promised this card (bold_ask)
        else:
            # v6: life events are rare and come at real rates, so they are the big moments to offer the player; everyday
            # situations fill most weeks, and each one waits longer every time it has been a checkpoint (variety)
            life = "had_ev" in loc and bool(loc["had_ev"][0]) and int(loc["s_ev"][0]) == s
            sh = self._sit_share.get(self.L["names"][s])
            rare = GAME["rare_ask"] and s not in self._cp_n and sh is not None and sh < RARE_SHARE
            if t - self._last_cp < (gap_weeks // 2 if life or rare else gap_weeks):
                return None
            wait = (again // 2) * self._cp_n.get(s, 0) if life else again * (1 + self._cp_n.get(s, 0))
            if t - self._last_seen.get(s, -10 ** 6) < wait:
                return None
            if GAME["returns"] and s in self._cp_n and self._ret_due(loc):
                return None                     # Picks come back: a moment met before waits while a return is due
            tied, cause = self._thread_of(loc, s) if t / 52 >= self.start_age else (True, None)
            if (not tied and not life and thr > 0
                    and (self._sit_share.get(self.L["names"][s]) or 0.0) >= GAME["told_share"]):
                return None                     # 5.6: an everyday moment with no tie to this life is told, not asked
            fork = self._fork(loc, s) if (GAME["fork_k"] or GAME["fork_told"]) else 0.0
            if GAME["fork_told"] and fork == 0 and not life and not rare and not tied and thr > 0:
                return None                     # v22.5 proposal: every option ends alike: told, not asked
            if (self._importance(loc, s, a) + (0.5 if life else 0.0) + GAME["tie_imp"] * tied
                    + GAME["tie_pick"] * (cause is not None) + GAME["fork_k"] * fork + GAME["rare_imp"] * rare < thr):
                return None
            if GAME["returns"] and s in self._cp_n and self.__dict__.get("_ret_owed", 0) > 0:
                self._ret_owed -= 1
                return None                     # Picks come back: a return took this repeat's place: told, not asked
            if GAME["bold"] and not life and not rare and self._link_owed > 0:
                self._link_owed -= 1
                return None                     # Bold ways: a link took this everyday ask's place: told, not asked
        self._last_seen[s] = t
        self._cp_n[s] = self._cp_n.get(s, 0) + 1
        return self._build_checkpoint(t, loc, a)

    def _fork(self, loc, s):
        """v22.5 proposal: the share (0 to 1) of a moment's open options that lead somewhere lasting: a title or perk
        given or taken (the Library's act fields), a commitment started, or money, time, health, ties or freedom won,
        lost or paid. 0 when every option ends alike."""
        L = loc["L"]; mask = np.asarray(loc["mask"][0], bool) & ~np.asarray(loc["do_nothing"][0], bool)
        ks = np.nonzero(mask)[0]
        if not len(ks):
            return 0.0
        GR = L.get("ROLES") if loc.get("RON") else None
        hasfx = GR["A_HASFX"][s] if GR is not None and "A_HASFX" in GR else np.zeros(len(mask), bool)
        lasting = [bool(hasfx[k]) or int(L["COMMIT"][s, k]) >= 0 or bool(np.abs(L["WIN"][s, k]).sum() + np.abs(L["LOSE"][s, k]).sum()
                   + np.abs(L["PAY"][s, k]).sum() >= 0.02) for k in ks]
        return float(np.mean(lasting))

    def _rung_here(self, loc, s):
        """v22.5 proposal: an open option of this moment gives a pack career's rung or a summit (batch A_TIER)."""
        GR = loc["L"].get("ROLES") if loc.get("RON") else None
        if GR is None or "A_TIER" not in GR:
            return False
        o_ = np.asarray(loc["open_"][0], bool) & np.asarray(loc["mask"][0], bool)
        return bool((np.asarray(GR["A_TIER"][s])[o_] >= 0).any())

    @staticmethod
    def _colors(loc, k):
        """An option's colors: its ways, and the end they serve when that differs ('W>U': White means for a Blue end)."""
        means = letters(loc["m"][0, k])
        e = np.maximum(loc["e0"][0, k], 0) if "e0" in loc else None
        ends = letters(e) if e is not None and e.sum() > 0 else means
        return means if ends == means else f"{means}>{ends}"

    @staticmethod
    def _kills(L, s):
        """The role who dies in this moment (the Library's kills: field), or None."""
        k = int(L["KILLS"][s]) if "KILLS" in L else -1
        return E.ROLES[k] if k >= 0 else None

    def _true_odds(self, loc, k):
        P, L = loc["P"], loc["L"]
        m = loc["m"][0, k]; alpha = loc["alpha"][0]
        fit = P["fit"] * (m * (alpha - alpha.mean())).sum()
        pb = loc.get("pbump")                       # perks that help acts in their ways (logit units, as the engine adds them)
        pb = float(pb[0, k]) if np.ndim(pb) == 2 else 0.0
        return float(1 / (1 + np.exp(-P["gain"] * ((m * (loc["sig"][0] + loc["f_tot"][0])).sum() + fit - loc["diff"][0, k]) - pb)))

    def _build_checkpoint(self, t, loc, a):
        L = loc["L"]; s = int(loc["s"][0])
        mask = loc["mask"][0]; seen = loc["seen"][0]; open_ = loc["open_"][0]
        open_r = loc["open_r"][0]; dn = loc["do_nothing"][0]
        U = loc["U"][0]; pr = loc["pr"][0]; p_hat = loc["p_hat"][0]
        own = int(a[0])
        recon = bool(loc["recon"][0])
        seen_k = [k for k in range(len(mask)) if mask[k] and seen[k] and not (recon and k > 3)]
        Ubest = max([float(U[own])] + [float(U[k]) for k in seen_k])         # the best they see, not the sampled pick
        u_dn = max([float(U[k]) for k in range(len(mask)) if mask[k] and dn[k]] or [-np.inf])
        gaps = [Ubest - float(U[k]) for k in seen_k if k != own and not dn[k]]
        ref = max(GAME["rel_ref"], float(np.median(gaps)) if gaps else 0.0)       # this moment's typical gap
        labels = L["labels"][s]
        opts = []
        for k in range(len(mask)):
            if not mask[k]:
                continue
            if recon and k > 3:
                continue
            if dn[k]:
                status = "considered"
            elif seen[k]:
                status = "considered"
            elif open_[k]:
                status = "didn't think of it"
            else:
                status = "out of reach"
            why = ""
            if status == "out of reach":
                req = L["REQ"][s, k]; res = loc["res"][0]; rn_ = res_names(self.setting)
                lack = [rn_[j] for j in range(len(req)) if req[j] > 0 and res[j] < req[j]]
                why = "lacks " + ", ".join(lack) if (lack and not open_r[k]) else "not on offer around them"
                if GAME["world_hold"] and not open_r[k] and not lack:   # F12: the means gate closed it, with each need met
                    j_ = min((j for j in range(len(req)) if req[j] > 0), key=lambda j: res[j] - req[j], default=None)
                    why = f"stretched for {rn_[j_]}" if j_ is not None else why
            clash = [] if dn[k] else clash_with(self._colors(loc, k), self._prev_label)
            rel = 0.0 if k == own else reluctance(Ubest - float(U[k]), ref, u_dn - float(U[k]), bool(clash)) * self._own_k(loc, k)
            pt = self._true_odds(loc, k); pt0 = pt
            if k != own:
                lg = np.log(pt / (1 - pt)) - GAME["effort"] * rel - (GAME["out_of_reach"] if status == "out of reach" else 0)
                pt = float(1 / (1 + np.exp(-lg)))
            ph = float(p_hat[k])
            label = world_says(self.setting, "LABELS", labels[k], labels[k])   # F12: in the clan's or the towers' words
            label = label.replace("{title}", getattr(self.story, "title_now", None) or "their role")
            if recon:
                kk = int(loc["rk"][0]); label = re.sub(r"\bit\b", f"the {KNAMES[kk]}", label, count=1)
            commit = int(L["COMMIT"][s, k])
            opts.append(dict(idx=k, label=label, colors=self._colors(loc, k) if not dn[k] else "-",
                             felt=ph, true=pt, hint=hint(pt - ph) if not dn[k] else "",
                             lean=float(pr[k]) if np.isfinite(pr[k]) else 0.0,
                             rel=rel, status=status, why=why, gap=Ubest - float(U[k]), span=Ubest - u_dn, clash=clash, true0=pt0,
                             acc="their own pick" if k == own else accept_word(rel), trust=self._trust_on(loc, k),
                             commit=KNAMES[commit] if commit >= 0 and not loc["held"][0, commit] else None,
                             follows=self._follows(loc, s, k, ph, commit, recon)))
            if opts[-1]["commit"] == "career" and world_says(self.setting, "WORDS", "career"):   # F12: a life's work, a post
                opts[-1]["commit_say"] = world_says(self.setting, "WORDS", "career")
        title = world_says(self.setting, "TITLES", L["names"][s], L["names"][s])   # F12: the moment as that world calls it
        extra = ""
        kind = None
        if recon:
            kk = int(loc["rk"][0]); kind = KNAMES[kk]
            held_y = (t - loc["since"][0, kk]) / 52
            title = f"reconsidering their {kind}"
            asks = " and ".join(ADJ[c] for c in letters(loc["prof"][0, kk]).split("+"))
            wants = " and ".join(ADJ[c] for c in letters(E.softmax(loc["y"][0])).split("+"))
            extra = self.story.recon_note(kind, held_y, asks, wants)
            if self.ledger:
                extra += (f" [invested {loc['I'][0, kk]:.2f}; expects {letters(loc['prof'][0, kk])}, "
                          f"wants {letters(E.softmax(loc['y'][0]))}]")
        # the scene, and what the character thinks about the act they lean toward
        if self.story.one_roll and loc.get("WL") is not None:
            self._one_roll(loc)                         # F7: the world's dead, before the scene names anyone
        ret = getattr(self, "_ret_cand", None) if GAME["returns"] else None
        if ret is not None and ret.get("link") and ret.get("title"):
            self.story.title_now = ret["title"]         # Bold ways: a shared link's {title} is the title the bold try was about
        m = self.story.moment(t, L["names"][s], int(loc["stage"][0]), t / 52, kind, self._kills(L, s),
                              ret["who"] if ret else None)
        self._far_moment(m, loc, s)                     # far_ties: the far moment's tie, town and event (Library slots)
        self._social_slots(m, loc, s)                   # v22.4: the places, post or price the moment is about
        if m["ctx"].get("_social"):                     # and its options' own slots, as its scene fills them
            for o in opts:
                o["label"] = self.story.slots_in(o["label"], m)
        try:
            sr = self._seen_rows(loc, s)                # S6: "seen it done" on the option row
        except Exception:
            sr = None
        for o in opts if sr else ():
            if o["idx"] in sr and o["colors"] != "-":   # never on doing nothing
                o["seen"] = sr[o["idx"]]
        lean = next((o for o in opts if o["idx"] == own), None)
        thought = ""
        if lean is not None and lean["colors"] != "-":
            thought = self.story.reason(lean["colors"].replace("+", "")) + " " + self.story.confidence(lean["felt"])
        elif lean is not None:
            thought = self.story.thought("Not now. Let it be.", "wait", "")
        mm = np.maximum(np.asarray(loc["m"][0], float), 0)
        oc = loc.get("option_causes"); causes = oc(0) if callable(oc) else None
        for o in opts:                                  # P3: steering with the era's pull costs less, against it more
            fit = self._era_fit(loc, mm[o["idx"]] / mm[o["idx"]].sum()) if mm[o["idx"]].sum() > 0 else 0.0
            o["era"] = round(fit, 2); o["era_k"] = float(np.clip(1 - GAME["era_cost"] * fit, 0.5, 1.5))
            if causes and o["idx"] < len(causes) and causes[o["idx"]]:
                o["wcause"] = self._option_cause(causes[o["idx"]])   # WL3: the world closes it, or makes it harder or easier
        if GAME["arrows"] and hasattr(F, "arrows"):     # v24: the hover arrows, the Engine's forecast without its numbers
            fa = {d["k"]: d for d in F.arrows(loc, 0)}
            for o in opts:
                d = fa.get(o["idx"])
                if d:
                    o["arrows"] = {w: [{x_: a_[x_] for x_ in ("kind", "name", "dir", "size", "word")} for a_ in d[w]]
                                   for w in ("win", "fail")}
        aw = self.aim_ways_view(loc)                    # v24 aims: which options lead into an aim's next step
        for o in opts:
            if aw.get(o["idx"]):
                o["aims"] = aw[o["idx"]]
        cp = dict(t=t, age=t / 52, title=title, extra=extra, stakes=float(L["STAKES"][s]), recon=recon, s=s, sit=L["names"][s],
                  scene=self.story.scene(m), thought=thought, moment=m,
                  options=sorted(opts, key=lambda o: o["idx"]), own=own, a=a.copy(), by_idx={o["idx"]: o for o in opts})
        for o in opts:                                  # the Library's role slots in an option ({friend}, {boss}): the scene's people
            if "{" in o["label"]:
                o["label"] = self.story.fill_label(o["label"], m)
        if GAME["stakes"] and "notes" in L:             # Stakes on the card: what each way changes for good (display only)
            for o in opts:
                st = self._stake_of(L, s, m, o)
                if st:
                    o["at_stake"] = st
        if not recon and t / 52 >= self.start_age:      # F5: a moment that follows from a pick of theirs says so
            _, cause = self._thread_of(loc, s)
            if cause is not None:
                cp["thread"] = self._thread_line(cause, t / 52); cause["told"] = int(t)   # each thread told once in a while
        if ret is not None:                             # Picks come back: the return opens on the pick it answers
            cp["ret"] = ret; cp["thread"] = self._ret_line(ret, t / 52); cp["seed"] = self._seed_view(ret, m, opts)
            if ret.get("link"):                         # Bold ways: a link opens on the bold try and takes an everyday ask's place
                cp["thread"]["line"] = self._bold_link_line(ret, t / 52); cp["seed"]["link"] = ret.get("side")
                self._link_owed += 1
            else:
                self._ret_owed = self.__dict__.get("_ret_owed", 0) + 1   # it takes the place of the next repeat that would be asked
        b = X.say(X.before(loc, 0, rng=self.vrng), self.name)
        cp["snap"] = X.snapshot(loc, 0, b)
        if GAME["because"]:
            cp["nw0"] = self._nw(loc)                   # Because of you: the week's need record at the pick
        cp["view"] = self._view(loc, b, cp)
        if GAME["bold"] and self._bold_now and not recon:
            self._bold_options(loc, cp)                 # Bold ways: up to two more ways, after the moment's own
        return cp

    # ------------------------------------------------------------------ v7: the character's view, and what came of it
    def _goal_words(self, loc, text):
        """The engine's default goal names ("the plan (B W)") in the story's words."""
        if not text or "gk" not in loc or "the " not in text:
            return text
        for j in np.nonzero(loc["gk"][0] >= 0)[0]:
            raw = X.goal_name(loc, 0, j)
            if raw in text:
                kind = E.G_KINDS[int(loc["gk"][0, j])]; d = int(loc["gd"][0, j])
                hz = E.HORIZONS[int(loc["ghz"][0, j])] if kind == "plan" and "ghz" in loc else ""
                text = text.replace(raw, self.story.name_goal(raw, kind, KNAMES[d] if d >= 0 else "", loc["gm"][0, j], int(loc["gid"][0, j]), hz))
        return text

    def _view(self, loc, b, cp):
        """explain.before(), joined to the checkpoint's options: the heart's and the head's share of each, the reality
        hint (a band of words; the game's own odds, which include the cost of a push), and the inner voice in story words."""
        raw = {o["k"]: o for o in b["options"]}
        L = loc["L"]; s = int(loc["s"][0])
        rename = []
        for o in cp["options"]:
            e = raw.get(o["idx"], {})
            o["kind"] = e.get("kind", "")
            acc = e.get("accept")
            if acc and o["idx"] != cp["own"]:          # the engine's word and the cost of forcing it
                o["acc"] = ACC_FROM_ENGINE.get(acc["level"], acc["level"]); o["rel"] = float(acc["reluctance"])
                kx = self._own_k(loc, o["idx"])
                if kx < 1.0:                            # S2: a way that has become theirs costs less to be pushed into
                    o["rel"] *= kx; o["acc"] = accept_word(o["rel"])
                o["acc_clash"] = float(acc["clash"])
                if o["acc"] not in ("reluctant", "against it"):
                    o["clash"] = []
                pt = o["true0"]
                lg = np.log(pt / (1 - pt)) - GAME["effort"] * o["rel"] - (GAME["out_of_reach"] if o["status"] == "out of reach" else 0)
                o["true"] = float(1 / (1 + np.exp(-lg)))
                if o["colors"] != "-":
                    o["hint"] = hint(o["true"] - o["felt"])
            if e.get("needs"):                          # titles and perks: what it needs, which perks help it, what it gives or takes
                o["needs"] = self._role_need(e["needs"]); o["closed"] = e.get("closed")
            GR = L.get("ROLES")
            if e.get("helped_by") and GR is not None:
                o["helped"] = [role_info(GR, GR["ID"][nm]) for nm in e["helped_by"] if nm in GR["ID"]]
            lv = lever_info(e.get("lever") or (L["LEVER"][s][o["idx"]] if "LEVER" in L else None),
                            e.get("target") or (L["TARGET"][s][o["idx"]] if "TARGET" in L else None))
            if lv:                                      # spec 7: the lever an act on the outer world uses, and its target
                o["lever"] = lv
            o["roles_fx"] = self._role_fx(loc, s, o["idx"])
            if any(d["when"] == "ok" and d["gain"] and d.get("title") for d in o["roles_fx"]):
                o["rung"] = self._rung_below(loc, s)    # the step they stand on, for a long shot's climb
            if e.get("base") is not None:               # the Library's chance: how often it works for most people at these ages
                o["base"] = float(e["base"])
            if o["label"] != L["labels"][s][o["idx"]]:
                rename.append((L["labels"][s][o["idx"]], o["label"]))
            if e.get("felt") is None:
                continue
            # the engine's reality hint is for the act as the character would do it; a push costs effort on top (rel)
            o["reality"] = dict(e["reality"], why=self._goal_words(loc, e["reality"]["why"]))
            o["heart"], o["head"] = e["heart"], e["head"]
            o["drivers"] = {k: [[DRIVER_WORD.get(nm, nm), round(v, 3)] for nm, v in e["drivers"][k]] for k in ("heart", "head")}
        ins = b["insight"]
        line = self._goal_words(loc, ins["line"])
        for a_, b_ in rename:
            line = line.replace(a_, b_)
        asides = [self.story.aside(x["key"], self._goal_words(loc, x["line"])) for x in b["asides"]]
        own, heart, head = cp["own"], b["heart"], b["head"]
        if heart >= 0 and own not in (heart, head) and own in cp["by_idx"]:
            asides.append(self.story.aside("lean_other", "Yet when it comes to it, {N} leans toward “" + cp["by_idx"][own]["label"] + "”."))
        return dict(key=ins["key"], line=self.story.insight(ins["key"], line, ins["heart_driver"], ins["head_driver"], b["self_control"]),
                    asides=asides, heart=heart, head=head, self_control=b["self_control"], voice_color=b["voice_color"],
                    heart_driver=DRIVER_WORD.get(ins["heart_driver"], ins["heart_driver"]),
                    head_driver=DRIVER_WORD.get(ins["head_driver"], ins["head_driver"]))

    def _resolution(self, loc, cpw, ev, text, o, pushed, rel, moved):
        """explain.after() for the choice just made: what happened, what changed in the person and around them, who it
        touched, what they are moving toward, and how the world works, as this week showed it."""
        r = X.say(X.after(cpw["cp"]["snap"], loc, 0, rng=self.vrng), self.name)
        def word(c):
            w = re.sub(r" in ([WUBRG]) ways", lambda m_: f" in {CNAME[m_.group(1)]} ways", c["word"])
            return dict(what=c["what"], word=w, delta=c["delta"], size=c["size"])
        changes = [word(c) for c in r["changes"] if c["size"] >= 0.5 and c["word"]][:9]
        became = [c for c in changes if c["size"] >= 1][:3]
        a = r["act"]
        res = dict(age=round(self.t / 52, 1), title=cpw["cp"]["title"], act=o["label"], colors=o["colors"], worked=bool(a["worked"]),
                   surprise=a["surprise"], felt=round(float(a["felt"]), 2), pushed=pushed, rel=round(rel, 2),
                   with_heart=bool(a.get("with_heart")), with_head=bool(a.get("with_head")), regret=bool(a.get("regret")),
                   text=text, changes=changes, became=became,
                   push=[dict(why=k, color=v["color"], dir=v["dir"]) for k, v in r["color_push"].items() if v["size"] >= 1][:3],
                   closer=dict(r["identity"]["closer_to"], guild=ident_name(r["identity"]["closer_to"]["identity"])) if r["identity"]["closer_to"] else None,
                   identity=dict(before=r["identity"]["before"], now=r["identity"]["now"], guild=ident_name(r["identity"]["now"])),
                   lessons=[dict(key=l_["key"], line=self._goal_words(loc, l_["line"])) for l_ in r["lessons"]],
                   events=r["events"], people=sorted({int(x) for x in re.findall(r"⟦p:(\d+)⟧", text)}),
                   states=[dict(word=e_["say"], what=e_["what"], good=ADJ_LOOK.get(e_["name"], ("", 0))[1],
                                icon=ADJ_LOOK.get(e_["name"], ("dot", 0))[0]) for e_ in r["events"] if e_.get("kind") == "state"],
                   roles=self._res_roles(loc, r["events"]),
                   dw=moved.get("dw"), dres=moved.get("dres"), new=True)
        wp = push_words(r.get("world_push") or a.get("world_push"))
        if wp:                                          # spec 7 §3: what a push on the outer world did
            res["world_push"] = wp
        ls = self._long_shot(o)
        if ls:                                          # a title reached for against long odds: kept, made or missed
            ls.update(made=bool(a["worked"]), age=res["age"], moment=res["title"],
                      tries=self._tries(ls["name"]))
            ls["words"] = long_shot_words(ls)
            self.history["long"].append(ls); res["long_shot"] = ls
        gv = self.gender_view(loc)
        cw = a.get("cross", o.get("cross"))            # the engine's crossing weight on the act (for-the-engine.md §6)
        if cw is None and loc is not None and "act_cw" in loc:
            cw = float(np.ravel(loc["act_cw"])[0])
        if cw and float(cw) > 0 and gv["strict"] >= 0.4:   # one short line of felt pressure; nothing where the world is loose
            res["pressure"] = self.story.rng.choice(PRESSURE.get(self.setting, PRESSURE["earth"])).replace("{N}", self.name)
        if gv["named"] and not self._named_seen:       # they named their gender: a new name, if they want one
            self._named_seen = True
            res["rename"] = dict(old=self.name, suggest=self.story._name(gv["own"] if gv["own"] in ("f", "m", "x") else "x"))
        res["say"] = self.story.resolution(res)
        return clean(res)

    def _needs_moved(self, loc, snap):
        """Every need that moved this week, from just before the choice to the end of the week (IDEAS.md, "Make needs
        visible", fix 2), with its level in the sheet's words."""
        if "need" not in loc or snap.get("need") is None:
            return []
        before = np.asarray(snap["need"], float); after = np.asarray(loc["need"][0], float)
        out = []
        for j, nm in enumerate(E.NEEDS):
            d = float(after[j] - before[j])
            if abs(d) < 0.01:                            # a point or more, so the shown percentages differ
                continue
            out.append(dict(need=nm, before=round(float(before[j]), 3), after=round(float(after[j]), 3), delta=round(d, 3),
                            lacking=bool(before[j] < GAME["need_thin"]), word=need_level_word(float(after[j]))))
        return sorted(out, key=lambda x: -abs(x["delta"]))

    def _hindsight(self, loc, cpw, worked, needs):
        """The character judges the push just made (IDEAS.md, "Player intervention that helps"), if they were at least
        reluctant about it ("okay with it" costs nothing, so there is nothing to look back on). Accepted: it worked and
        fed a need they lacked; part of its costs is undone and trust grows along the act's colors. Resented: it failed,
        or it worked but fed nothing they lacked while they were reluctant; trust falls, and a failure adds wanting.
        Otherwise it passes without a judgment. Changes the engine's state in place, as the forced-pick costs do."""
        f = self._force or {}
        rel = float(f.get("rel", 0.0)); rs = float(f.get("resent", rel))
        prof = self._profile(loc, cpw["choice"])
        # what the act gave to needs they lacked: its ends' share of the engine's refill, read at the moment (follows
        # "lift"); one act lifts a need by about a point, which the week's drain and other events can hide in the totals
        lift = (cpw["cp"]["by_idx"].get(cpw["choice"], {}).get("follows") or {}).get("lift") or []
        gain = sum(x["gain"] for x in lift)
        fed = lift[0] if lift else None
        out = dict(kind="none", share=0.0, need=fed["need"] if fed else None, trust_before=round(self._trust_on(loc, cpw["choice"]), 3))
        if rel < GAME["hind_rel"]:                          # they were fine with it: nothing to look back on
            pass
        elif worked and gain >= GAME["hind_min"]:
            share = GAME["hind_max"] * min(1.0, gain / GAME["hind_full"])
            loc["stress"][0] = max(0.0, float(loc["stress"][0]) - share * GAME["stress"] * rs)
            loc["Q"][0] = max(0.0, float(loc["Q"][0]) - share * GAME["backlash"] * rs)
            aut = E.NEEDS.index("autonomy")
            lost = next((-x["delta"] for x in needs if x["need"] == "autonomy" and x["delta"] < 0), 0.0)
            if lost > 0:
                loc["need"][0, aut] += share * lost
            if self.history["rel"]:
                self.history["rel"][-1] *= 1 - share           # a push they came to own counts less against "their own"
            self.trust += GAME["trust_gain"] * share / GAME["hind_max"] * prof * (1 - self.trust)
            self.history["accepted"] += 1
            out.update(kind="accepted", share=round(share, 3))
        elif rel >= 0.3 and (not worked or gain < GAME["hind_min"]):
            if not worked:
                loc["Q"][0] += GAME["resent_more"] * GAME["backlash"] * rs
            self.trust -= GAME["trust_loss"] * rel * prof * (1 + self.trust)
            self.history["resented"] += 1
            out.update(kind="resented", share=round(rel, 3))
        if out["kind"] == "none" and GAME["trust_judge"]:   # item 7: an unjudged push still moves trust by how it went
            st = (GAME["judge_a"] + GAME["judge_b"] * rel) * prof
            self.trust += st * (1 - self.trust) if worked else -st * (1 + self.trust)
            out["judged"] = "worked" if worked else "failed"
        if out["kind"] == "none":                           # F13: the review counts the pushes that passed unjudged
            self.history.setdefault("passed", [0, 0])[0 if worked else 1] += 1
        self.trust = np.clip(self.trust, -1.0, 1.0)
        out["trust_after"] = round(self._trust_on(loc, cpw["choice"]), 3)
        out["line"] = self.story.hindsight(out["kind"], NEED_WORD.get(out["need"], out["need"] or ""), worked)
        return out

    def _pivot(self, loc, cpw, worked, hind):
        """Item 4: the pick at a moment put to the player is a turning point (GAME piv...). It moves the colors, and part of
        the deep core, toward the picked ways (or toward what they wanted, on a backfire) and starts the season lean (F2).
        Changes the engine's state in place at the week's end, as the forced-pick costs do."""
        pushed = int(cpw["choice"]) != int(cpw["own"])
        k, own = bix(cpw["choice"]), bix(cpw["own"])     # Bold ways: a bold way teaches its base way's ways
        m = np.maximum(np.asarray(loc["m"][0], float), 0)
        if m[k].sum() <= 0:                                  # doing nothing teaches nothing about their ways
            return None
        T = m[k] / m[k].sum()
        w = E.softmax(loc["z"][0]); dist = float(0.5 * np.abs(T - w).sum())
        stakes = float(loc["L"]["STAKES"][int(loc["s"][0])])
        judged = (hind or {}).get("kind")
        kind, share, lean = ("own", GAME["piv_own"], GAME["piv_own"]) if not pushed else ("toward", 1.0, 1.0)
        if pushed and (not worked or judged == "resented"):
            kind, share, lean = "half", GAME["piv_fail"], 0.5
            if not worked and (judged == "resented" or self._prng.random() < min(0.8, GAME["backfire"] * dist * stakes)):
                if m[own].sum() > 0:                         # it backfires: they learn toward what they wanted instead
                    kind, share, lean, T = "backfire", 1.0, 0.0, m[own] / m[own].sum()
        size = share * (1 + GAME["piv_far"] * dist)
        if (GAME["season_need"] or GAME["season_calm"]) and kind == "toward" and (self._owned_pick(cpw, loc) or judged == "accepted"):
            e_ = np.maximum(np.asarray(loc["e0"][0, k] if "e0" in loc else loc["e"][0, k], float), 0)
            self._seasons.append((e_ / e_.sum() if e_.sum() > 0 else T, max(stakes, 0.9), int(self.t)))   # the new routine
        plast = float(loc["plast"][0]) if "plast" in loc else 0.2
        dz = GAME["piv"] * plast * size * E.centre(5 * (T - w))
        loc["z"][0] += dz
        if "k" in loc:
            loc["k"][0] += GAME["piv_core"] * dz
            if kind == "own":                                # letting them choose steadies them
                loc["k"][0] += GAME["piv_steady"] * (loc["z"][0] - loc["k"][0])
        if lean:
            self._leans.append((T, lean, int(self.t)))
            dec = 0.5 ** ((self.t - self._pick_t) / GAME["pick_half"])
            self._pick_mix = self._pick_mix * dec + lean * T; self._pick_wt = self._pick_wt * dec + lean; self._pick_t = int(self.t)
        self.history["pivots"].append((round(self.t / 52, 1), kind, [round(float(x), 3) for x in w],
                                       [round(float(x), 3) for x in T], round(size, 3)))
        return dict(kind=kind, size=round(size, 3), toward=letters(T), dist=round(dist, 3),
                    moved=[round(float(x) * 100, 2) for x in E.softmax(loc["z"][0]) - w])

    def _plan_lean(self, loc, g):
        """Item 4, 5.4: a plan they take up leans toward the ways of their recent picks (GAME plan_lean), so a few picks can
        shape a decade. Changes the new plan's colors in place (and the moments that offer it a step)."""
        if g.get("kind") != "plan" or g.get("what") != "begins" or g.get("by_player") or self._pick_wt <= 0 or "gid" not in loc:
            return
        js = np.nonzero(loc["gid"][0] == int(g.get("id", -1)))[0]
        if not len(js):
            return
        j = int(js[0])
        wt = self._pick_wt * 0.5 ** ((self.t - self._pick_t) / GAME["pick_half"])
        lam = GAME["plan_lean"] * min(1.0, wt)
        if lam < 0.02:
            return
        mix = (1 - lam) * np.asarray(loc["gm"][0, j], float) + lam * self._pick_mix / max(self._pick_wt, 1e-9)
        loc["gm"][0, j] = mix / mix.sum()
        if callable(loc.get("goal_rel_S")) and "gsr" in loc:
            loc["gsr"][0, j] = loc["goal_rel_S"](loc["gm"][0, j], int(loc["gd"][0, j]))
        g["mix"] = loc["gm"][0, j].round(2).tolist(); g["led"] = round(lam, 2)

    def _mark_threads(self, cpw, new, GR, age):
        """F5 (item 4, gameplay-feel.md 5.3): what this week's pick started (a title or perk, a commitment, a plan or
        dream of their own) becomes a thread; later moments that follow from it say so, the pick on hover."""
        o = cpw["cp"]["by_idx"][cpw["choice"]]
        if o["colors"] == "-":                           # waiting starts no thread
            return
        cause = dict(age=int(age), t=int(self.t), act=o["label"], moment=cpw["cp"]["title"], pushed=cpw["choice"] != cpw["own"])
        self._last_pick = cause
        for ev in new:
            r, c, g = ev.get("role"), ev.get("commitment"), ev.get("goal")
            if r and r["what"] == "gained" and GR is not None and r["name"] in GR["ID"] and GR["ID"][r["name"]] < GR["NT"]:
                d = role_info(GR, GR["ID"][r["name"]])
                self._threads[("r", d["i"])] = dict(cause, key="title", title=d["say"], what="they became " + d["say"])
            elif c and c["what"] == "start":
                self._threads[("c", c["kind"])] = dict(cause, key="commitment", kind=c["kind"],
                                                       what=THREAD_COMMIT.get(c["kind"], "a commitment began"))
            elif g and g.get("what") == "begins" and g.get("kind") in THREAD_GOAL:
                gid = int(g.get("id", -1))
                nm = (self.story.dreams.get(gid) or {}).get("name", "") if g["kind"] != "plan" else ""
                self._threads[("g", gid)] = dict(cause, key="plan" if g["kind"] == "plan" else "dream", goal=nm, what=THREAD_GOAL[g["kind"]])

    # ------------------------------------------------------------------ Picks come back (GAME returns)
    def _seed_pick(self, cpw, new, m, age):
        """An asked pick is kept by its week (the moment, the way, how it went, the age, the person in its scene): the
        Engine's seed list (ep_seeds) names a seed by that week."""
        o = cpw["cp"]["by_idx"][cpw["choice"]]
        ok = next((bool(ev["success"]) for ev in new if "situation" in ev), None)
        who = next((m["ctx"]["_p_" + sl] for sl in PERSON_SLOTS if m is not None and m["ctx"].get("_p_" + sl) is not None), None)
        self._picks[int(self.t)] = dict(t=int(self.t), age=round(age, 1), moment=cpw["cp"]["title"], act=o["label"], ok=ok,
                                        who=who, pushed=cpw["choice"] != cpw["own"])

    def _seed_mark(self, mark, m):
        """This week's asked pick left a mark: the person in its scene (as the story's mark keeps them, after the outcome
        is told) joins the pick, and the game's own seed is planted, for the echoes of that mark without the Engine's hook."""
        pick = self._picks.get(int(self.t))
        if pick is None:
            return
        if pick["who"] is None and m is not None:
            pick["who"] = next((m["ctx"]["_p_" + sl] for sl in PERSON_SLOTS if m["ctx"].get("_p_" + sl) is not None), None)
        self._seeds.append(dict(pick, kind=mark))

    def _return_of(self, loc, s):
        """The seed this week's moment answers, or None. The Engine's hook (echo_play) names it: ep_now, an index into
        ep_seeds (dicts: t the pick's week, kind, src, ok, due, done, got). Without the hook, a moment that echoes a mark
        (the Library's echo:) answers this life's oldest seed of that mark not yet come back, ret_gap weeks or more after
        its pick."""
        if "ep_now" in loc:
            k = int(np.asarray(loc["ep_now"]).ravel()[0])
            if k < 0 or k >= len(loc.get("ep_seeds") or ()):
                return None
            sd = loc["ep_seeds"][k]
            pick = self._picks.get(int(sd["t"]))
            if pick is None:                            # a pick the game did not keep: told as an ordinary moment
                return None
            ret = dict(pick, kind=sd["kind"], ok=bool(sd["ok"]), k=k)
            return self._bold_ret(ret, sd) if GAME["bold"] else ret
        mark = LIB_ECHO.get(self.L["names"][s])
        if not mark:
            return None
        return next((x for x in self._seeds if x["kind"] == mark and "came" not in x and self.t - x["t"] >= GAME["ret_gap"]
                     and (x["who"] is None or x["who"]["alive"] or self.L["names"][s] in LIB_GONE)), None)   # the dead: a memory

    def _stake_of(self, L, s, m, o):
        """Stakes on the card: what a way changes for good, from the Library's own fields for it. people: what its mark
        does to someone (STAKE_MARK; mark: the Library's word), by name when the way's own words or the moment's one person say who (person: their
        story id); fails: a closed way's own backfire; risk: the risk to life if it fails (death_if_fails). It reads the
        moment's people as they stand and creates or introduces no one, so nothing is drawn and nothing else reads
        differently."""
        row = L["notes"][s]
        nt = row[o["idx"]] if o["idx"] < len(row) else None
        if not isinstance(nt, dict):
            return None
        ctx, out = m["ctx"], {}
        say = STAKE_MARK.get(nt.get("mark"))
        if say:
            here = [sl for sl in PERSON_SLOTS if ctx.get("_p_" + sl) is not None]
            own = [sl for sl in re.findall(r"\{(\w+)\}", L["labels"][s][o["idx"]]) if sl in here]
            who = [sl for sl in (own or (here if len(here) == 1 else []))
                   if not (nt["mark"] == "made a friend" and sl in STAKE_NEAR) and not (nt["mark"] in STAKE_KIND and sl == "child")]
            p = ctx["_p_" + who[0]] if who else None
            if p is not None and (not p.get("alive", True) or who[0] == ctx.get("_gone_slot")):
                p = None                                # someone who has died or is gone is never named as here
            out["people"] = say[0].format(p=p["name"]) if p and p.get("name") else say[1]
            out["mark"] = nt["mark"]
            if p and p.get("name"):
                out["person"] = p.get("id")
        bf = re.search(r"backfire:\s*(.+)$", str(nt.get("closed") or ""))
        if bf and not STAKE_SOON.search(bf.group(1)):
            out["fails"] = self._stake_fill(bf.group(1).strip().rstrip("."), ctx)
        if nt.get("death_if_fails"):
            out["risk"] = stake_risk(float(nt["death_if_fails"]))
        return out or None

    def _stake_fill(self, text, ctx):
        """A backfire's slots: the character, their place, and the moment's people by name (no one new: "their <role>")."""
        def one(mm):
            k = mm.group(1)
            if k in ("N", "Ns"):
                return self.name + ("'s" if k == "Ns" else "")
            if k == "place":
                return self.story.place
            p = ctx.get("_p_" + k)
            return p["name"] if p is not None and p.get("name") else "their " + k
        return re.sub(r"\{(\w+)\}", one, text)

    def _seed_view(self, ret, m, opts):
        """Release's proof rows (chroma-release/check_picks.py): the seed a return answers, as its ask carries it. now:
        who fills the return's person slot (a story id; memory:<id> and heard:<id> come with the Library's scenes); tilt:
        the change to the return's odds, the mean over its ways; t: the pick's week (age is rounded to .1 year)."""
        p = ret.get("who")
        now = next((m["ctx"]["_p_" + sl]["id"] for sl in PERSON_SLOTS if m["ctx"].get("_p_" + sl) is not None), None)
        if now is not None and m["ctx"].get("_gone"):
            now = f"memory:{now}"                       # the seed's person remembered (the Library's scenes_gone)
        tau = 0.0 if ret["ok"] is None else GAME["ret_tilt"] if ret["ok"] else -GAME["ret_tilt"]
        pt = np.clip([o["true"] for o in opts if o["colors"] != "-"], 1e-6, 1 - 1e-6)
        dp = 1 / (1 + np.exp(-(np.log(pt / (1 - pt)) + tau))) - pt
        return dict(t=int(ret["t"]), age=ret["age"], sit=ret["moment"], way=ret["act"], went=None if ret["ok"] is None else "well" if ret["ok"] else "badly",
                    person=p["id"] if p else None, near=bool(p and p["alive"] and not p["role"].startswith("old ")),
                    now=now, tilt=round(float(dp.mean()), 4) if len(dp) else 0.0)

    def _ret_due(self, loc):
        """Whether a seed is due and waiting (the Engine's ep_seeds); never without the hook."""
        return any(x["done"] is None and x["due"] is not None and self.t >= x["due"] for x in loc.get("ep_seeds") or ())

    def _ret_came(self, cpw, ev, age):
        """A return was played: the seed has come back. Kept for the Book's pair and the song, and the outcome card's
        line, its hover the first time."""
        ret = cpw["cp"]["ret"]; o = cpw["cp"]["by_idx"][cpw["choice"]]
        ret["came"] = int(self.t)
        self.history.setdefault("returns", []).append(dict(age=round(age, 1), moment=cpw["cp"]["title"], act=o["label"],
            ok=bool(ev["success"]), seed=dict(age=ret["age"], moment=ret["moment"], act=ret["act"], ok=ret["ok"]),
            who=ret["who"]["name"] if ret.get("who") else None))
        return dict(line=self.story.fill(f"This came from what {{N}} did at {int(ret['age'])}."), cause=cpw["cp"]["thread"]["cause"])

    # ------------------------------------------------------------------ 5.6: the price builds to a turning point
    def _price_now(self):
        return self._price * 0.5 ** ((self.t - self._price_t) / GAME["turn_half"])

    def _turn_due(self, t):
        if EP is None or self.setting != "earth" or t / 52 < max(self.start_age, 14) or len(self.history["turns"]) >= GAME["turn_max"]:
            return False
        last = self.history["turns"][-1]["t"] if self.history["turns"] else -10 ** 6
        return t - last >= GAME["turn_gap"] and t - self._last_cp >= FREQ[self.freq][0] // 2 and self._price_now() >= GAME["turn_line"]

    def _build_turning(self, t, loc, a):
        """5.6: "the day it all comes to a head" (Library earth_play.py), built by the game: five one-color options, their
        own pick the option of their lead color. The engine's moment this week goes on as their own."""
        S = EP.SITUATIONS[0]
        w = E.softmax(loc["z"][0]); lead = COLORS[int(np.argmax(w))]
        opts = []
        for i, (label, means, _e, _d, _t, x) in enumerate(S["options"]):
            c = means[0]
            opts.append(dict(idx=i, label=label, colors=c, felt=float(x.get("chance", 0.55)), hint="", lean=0.0, status="open",
                             rel=0.0 if c == lead else 0.3, why="", commit=None, follows={}, kind="", act=x.get("act", label),
                             acc="their own pick" if c == lead else "okay with it", trust=float(self.trust[COLORS.index(c)]),
                             era=0.0))
        own = next(o["idx"] for o in opts if o["colors"] == lead)
        sc = dict((c_, x_) for c_, x_ in S["scenes"]["earth"])
        cp = dict(t=t, age=t / 52, title=S["name"], extra="", stakes=float(S["stakes"]), recon=False, s=int(loc["s"][0]), sit=S["name"],
                  scene=self.story.fill(sc.get(lead) or sc.get("", "")), thought="", moment=None, options=opts, own=own, a=a.copy(),
                  by_idx={o["idx"]: o for o in opts}, turning=True)
        return cp

    def _turning_end(self, t, loc, tp):
        """5.6: the turning point's pick, at the end of its week: a lesson turn_piv times a pick's toward the chosen color,
        half of it into the deep core; held (the option's chance, more for their own lead), the strain and the pent-up
        wanting are let go and the new way leads their acts for a year; broken, a little of it stays."""
        cp, k = tp["cp"], tp["choice"]
        o = cp["by_idx"][k]; c = o["colors"]; ci = COLORS.index(c)
        w = E.softmax(loc["z"][0]); lead = cp["by_idx"][cp["own"]]["colors"]
        d = np.asarray(self.history["voice"]["d"], float)
        pushed = COLORS[int(np.argmax(d))] if d.max() > 0 else None
        kind = "snap back" if c == lead else "reinvention" if c == pushed else "turn"
        held = bool(self._prng.random() < min(0.9, o["felt"] + (0.2 if c == lead else 0.0)))
        T = np.full(C, 0.1); T[ci] = 0.6
        plast = float(loc["plast"][0]) if "plast" in loc else 0.2
        dz = GAME["piv"] * GAME["turn_piv"] * plast * (1.0 if held else 0.4) * E.centre(5 * (T - w))
        loc["z"][0] += dz
        if "k" in loc:
            loc["k"][0] += (0.5 if held else 0.15) * dz
        if held:
            loc["stress"][0] *= 0.5; loc["Q"][0] *= 0.3
            self._leans.append((T, 1.0, int(t))); self._leans.append((T, 1.0, int(t) + GAME["lean_weeks"]))
        self._price, self._price_t = 0.0, int(t)
        self.history["turns"].append(dict(t=int(t), age=round(t / 52, 1), color=c, kind=kind, held=held))
        outs = EP.SITUATIONS[0]["outcomes"][0 if held else 1]
        line = self.story.fill("{N} decides " + chooses(act(o["act"])) + ". " + outs[len(self.history["turns"]) % len(outs)])
        self._say(mk("T", f"{c}|{kind}|{int(held)}", line), 0, "turning", color=c, kind=kind, held=held)
