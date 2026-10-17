"""Game's methods for the inner voice, threads, trust, the character's own ways, goals, learning and the weekly hooks.

Part of class Game (game.py), which inherits VoiceMixin; moved out of game.py verbatim. A method here reads
module names through the imports below, the same objects game.py has, and self for everything on the Game."""
import numpy as np
from game_base import (ADJ, ADJ_LOOK, C, CNAME, COLORS, E, ES, GAME, KNAMES, LINE_WAIT_TAGS, NEED_WORD, NOUN,
    OWN_STEPS, RNAMES, SH_FRAC, SH_HOLD, SH_SHOW, SH_SRC_SHOW, act, chooses, ident_name, need_level_word, neg_of,
    plain, role_info)
from game_words import (LONG_SHOT, LONG_SHOT_KINDS, NEED_HINT, THREAD_AGAIN, THREAD_YEARS, TITLE_KINDS, VOICE_AX,
    VOICE_FADE, VOICE_MIN, VOICE_RECALL, VOICE_SIDES, art, voice_share)

_NUMW = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
         "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")


def _num_word(n):
    """Picks come back's opener: years as a word up to twenty, digits after."""
    return _NUMW[n] if 0 <= n < len(_NUMW) else str(n)


class VoiceMixin:
    # ------------------------------------------------------------------ item 3: the voice in their head
    def _vsay(self, kind, xs):
        """A Library voice line pair: the first variant the first time this kind is told, the second after."""
        n = self._voice_said.get(kind, 0); self._voice_said[kind] = n + 1
        return xs[min(n, len(xs) - 1)] if isinstance(xs, list) else xs

    def _vfill(self, text, **kw):
        noun = ES.VOICE["noun"].get(self.setting, "voice") if ES else "voice"
        text = text.replace("{voice}", noun).replace("{name}", kw.pop("name", "") or self.voice_name())
        for k, v in kw.items():
            text = text.replace("{" + k + "}", str(v))
        return self.story.fill(text)

    def voice_name(self):
        """The voice's name in this life (voice-mechanics.md section 5): the strongest of the ten sides it pushed toward,
        trusted or doubted by the character's trust in that side's colors; "a voice" before VOICE_MIN pushes, "a quiet
        voice" when the player mostly lets them be."""
        if ES is None:
            return "the voice"
        v = self.history["voice"]; V = ES.VOICE
        noun = V["noun"].get(self.setting, "voice")
        if v["steer"] < VOICE_MIN:
            quiet = v["n"] >= 10 and v["steer"] / v["n"] < 0.2
            return (V["quiet"] if quiet else V["none"]).replace("{voice}", noun)
        ax = np.asarray(v.get("rk") or v["ax"], float)   # the side its pushes stood for most steadily among the open ways
        i = int(np.argmax(np.abs(ax))); sg = 1 if ax[i] > 0 else -1
        side = VOICE_SIDES[i][1 if sg > 0 else 2]
        cols = [c for c in range(C) if VOICE_AX[i, c] * sg > 0]
        tr = float(np.mean(self.trust[cols])) if cols else 0.0
        return V["name"][side]["doubted" if tr < 0 else "trusted"].replace("{voice}", noun)

    def _voice_trust(self, d):
        """The character's trust in the voice as one number: over the colors it pushed toward, an even mean; with item 7 on
        (GAME trust_judge), weighted by how much it pushed toward each, so the colors it pushed most decide the word."""
        pushed = d > 0
        if GAME["trust_judge"]:
            return float(d[pushed] @ self.trust[pushed] / d[pushed].sum())
        return float(np.mean(self.trust[pushed]))

    def voice_view(self, loc=None):
        """The panel row "The voice in their head": its name, the character's trust in words, and on hover what the voice
        moved in this life against what life itself moved, per color, in points."""
        v = self.history["voice"]; loc = self.loc if loc is None else loc
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed and v["steer"] else 0.0
        word = "" if not v["steer"] else "they trust it" if tr >= 0.25 else "they doubt it" if tr <= -0.25 else "they are unsure of it"
        total = (E.softmax(loc["z"][0]) - np.asarray(self._w_start, float)) if loc is not None and self._w_start is not None else np.zeros(C)
        vdw = self._vdw()
        return dict(name=self.voice_name(), trust=word, steer=v["steer"], n=v["n"], share=round(voice_share(vdw, total), 3),
                    voice=[round(float(x) * 100, 1) for x in vdw], life=[round(float(x) * 100, 1) for x in total - vdw],
                    toward=[round(float(x), 3) for x in d / max(v["steer"], 1)], **({"own": self.own_view()} if GAME["own_ix"] else {}))

    def _voice_pick(self, loc, cpw, worked, pushed, rel, moved, rs):
        """Item 3 at each decided moment: the record (the steer: the picked act's colors minus what they would have done),
        what the push moved, and the character's answer to the voice and its outcome (Library VOICE lines). Returns
        (answer, outcome) for a push, else None."""
        v = self.history["voice"]; v["n"] += 1
        if not pushed or ES is None:
            return None
        m = np.maximum(np.asarray(loc["m"][0], float), 0)
        cv = lambda k: m[k] / m[k].sum() if m[k].sum() > 0 else np.full(C, 0.2)
        k, own = int(cpw["choice"]), int(cpw["own"])
        diff = cv(k) - cv(own)
        v["steer"] += 1; v["rel"] = round(v["rel"] + rel, 3)
        v["d"] = [round(x + float(y), 4) for x, y in zip(v["d"], diff)]
        v["ax"] = [round(x + float(y), 4) for x, y in zip(v["ax"], VOICE_AX @ diff)]
        ks = [o for o in range(m.shape[0]) if m[o].sum() > 0]
        if len(ks) > 1:                                  # where the pick stood among the open ways, per side (-1 to 1)
            vals = np.array([VOICE_AX @ cv(o) for o in ks]); pv = VOICE_AX @ cv(k)
            rk = ((vals < pv - 1e-9).sum(0) - (vals > pv + 1e-9).sum(0)) / (len(ks) - 1)
            v["rk"] = [round(x + float(y), 4) for x, y in zip(v.get("rk") or [0.0] * len(VOICE_SIDES), rk)]
        dw = np.asarray(moved.get("dw") or np.zeros(C), float) / 100 + np.asarray((rs.get("pivot") or {}).get("moved") or np.zeros(C), float) / 100
        v["dw"] = [round(float(x) + float(y), 4) for x, y in zip(self._vdw(), dw)]; v["dw_t"] = int(self.t)
        self._vyear["steer"] += 1; self._vyear["won"] += int(worked)
        V = ES.VOICE; c = COLORS[int(np.argmax(cv(k)))]
        lead = int(np.argmax(E.softmax(loc["z"][0]))); ci = COLORS.index(c)
        rel_ = "same" if c in (self._core_label or COLORS[lead]) else "ally" if (ci - lead) % C in (1, C - 1) else "enemy"
        tr = float(self.trust[ci]); tw = "trust" if tr >= 0.25 else "doubt" if tr <= -0.25 else "unsure"
        last = self._vlast.get(c)
        if (last is not None and self.t - last["t"] <= VOICE_RECALL and not self._vlast.get("_mem")):
            # the voice pushed this way not long ago: they remember how it went (not twice running)
            key = "worked" if last["worked"] else "failed" if last.get("moment") else "failed_plain"
            ans = self._vfill(self._vsay("memory_" + key, V["memory"][key]), lost="“" + str(last.get("moment", "")) + "”")
        else:
            ans = self._vfill(V["answer"][c][rel_][tw][1 if rel >= 0.5 else 0])
        self._vlast["_mem"] = last is not None and self.t - last["t"] <= VOICE_RECALL and not self._vlast.get("_mem")
        self._vlast[c] = dict(worked=worked, moment=cpw["cp"]["title"], t=int(self.t))
        out = ""
        if rel >= GAME["hind_rel"]:                      # they resisted: was the voice right?
            out = self._vfill(V["outcome"]["right" if worked else "wrong"][1 if rel >= 0.5 else 0])
        rs["voice"] = dict(answer=ans, outcome=out, name=self.voice_name())
        return "“" + ans + "”", out

    def _voice_trust_turn(self):
        """Item 3: trust in a color crossing .5 or -.5 is told once, as the relationship turns."""
        if ES is None or self.burn_in:
            return
        for i, c in enumerate(COLORS):
            st = 1 if self.trust[i] >= 0.5 else -1 if self.trust[i] <= -0.5 else 0
            if st and st != self._trust_side[i]:
                d = "up" if st > 0 else "down"
                self._vline(self._vfill(self._vsay("turn", ES.VOICE["trust_turn"][c][d])), turn=d, color=c)
                self._vyear["turn"] = d
            self._trust_side[i] = st

    def _vline(self, text, **meta):
        """A voice line in the story: one a year at most (voice-mechanics.md section 9), the first that comes."""
        y = int(round(self.t / 52, 1))
        if y == self._vline_y:
            return False
        self._vline_y = y
        self._say(text, 0, "voice", **meta)
        return True

    def _vdw(self):
        """What the voice's pushes still hold of their colors now, per color: each push's move, fading as life pulls
        them back (VOICE_HALF)."""
        v = self.history["voice"]
        return np.asarray(v["dw"], float) * VOICE_FADE ** (self.t - v.get("dw_t", self.t))

    def _voice_became(self, lbl):
        """Item 3: a new name that the voice's pushes did most of is told as partly not their own doing."""
        v = self.history["voice"]; w = np.asarray(self._wring[-1], float)
        mark, self._name_mark = self._name_mark, (w.copy(), self._vdw().copy(), int(self.t))
        if ES is None or mark is None or self.burn_in or v["steer"] < VOICE_MIN or not lbl:
            return
        share = voice_share(self._vdw() - mark[1] * VOICE_FADE ** (self.t - mark[2]), w - mark[0])
        if share < 0.5 or self.t - v.get("became_t", -10 ** 6) < 5 * 52:
            return                                       # told when the voice did most of it, once in five years at most
        v["became_t"] = int(self.t)
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed else 0.0
        key = "trusted" if tr >= 0.25 else "doubted" if tr <= -0.25 else "unsure"
        head = ES.VOICE.get("became_head") if GAME["lines_tied"] else None
        if head:                                         # item 6: said beside the new name on the next year header
            self._became_head = (lbl, head[key])
            return
        self._vline(self._vfill(ES.VOICE["became"][key], ident=art(ident_name(lbl))), became=lbl, share=round(share, 2))

    def _voice_chapter(self, age):
        """Item 3: at most one voice line in a year's chapter, and only in years with something to say: the first year of
        the voice, trust turning, the voice winning most arguments, or a long quiet."""
        y, self._vyear = self._vyear, dict(steer=0, won=0, turn=None)
        v = self.history["voice"]
        if ES is None or self.burn_in or not v["n"]:
            return
        V = ES.VOICE["chapter"]; kind = None
        if y["turn"]:
            kind = "trust_up" if y["turn"] == "up" else "trust_down"
        elif y["steer"] and v["steer"] == y["steer"]:
            kind = "first"
        elif y["steer"] >= 3 and y["won"] * 2 > y["steer"]:
            kind = "won"
        elif not y["steer"] and v["steer"] and age - v.get("last_age", age) >= 3 and age - v.get("quiet_age", -99) >= 10:
            kind = "quiet"; v["quiet_age"] = age
        if y["steer"]:
            v["last_age"] = age
        if kind:
            self._vline(self._vfill(self._vsay("ch_" + kind, V[kind])), chapter=kind)

    def voice_review(self, h):
        """Item 3 at the end of a life: the voice's last sentence for the song (VOICE end) and the Book's line for this
        life (VOICE book)."""
        v = h["voice"]
        if ES is None:
            return {}
        V = ES.VOICE; vw = self.voice_view()
        share = vw["share"]; sw = next((w_ for b_, w_ in V["share"] if share < b_), V["share"][-1][1])
        d = np.asarray(v["d"], float); pushed = [c for c in range(C) if d[c] > 0]
        tr = self._voice_trust(d) if pushed and v["steer"] else 0.0
        key = "quiet" if v["steer"] < VOICE_MIN else "trusted" if tr > 0.2 else "doubted" if tr < -0.2 else "mixed"
        lead = COLORS[int(np.argmax(np.asarray(h["w"][-1][1], float)))] if h["w"] else "W"
        end = self._vfill(V["end"][key], adj=ADJ[lead], share=sw)
        names = [l_ for a_, l_, *_ in h.get("name", []) if l_]
        start = next((l_ for a_, l_, *_ in h.get("name", []) if a_ >= self.start_age and l_), names[0] if names else "")
        book = self._vfill(V["book"]["steered" if v["steer"] else "free"], start=art(ident_name(start)) if start else "still forming",
                           end=art(ident_name(names[-1])) if names else "still forming",
                           lean=V["lean"][COLORS[int(np.argmax(d))]] if v["steer"] else "")
        return dict(name=vw["name"], trust=vw["trust"], share=share, end=end, book=book, steer=v["steer"], n=v["n"],
                    voice=vw["voice"], life=vw["life"])

    def _thread_line(self, cause, age):
        """F5: the story sentence that ties a moment back to the pick that started its thread, and the cause in plain words
        for the hover. Built-in words until the Library's drop B (chroma-library/earth_play.py) brings its own."""
        when = "this year" if age - cause["age"] < 1 else "a year ago" if age - cause["age"] < 2 else f"at {cause['age']}"
        did = chooses(act(plain(cause["act"]))).rstrip(".")
        how = "you pushed it" if cause.get("pushed") else "they chose it themselves"
        why = f"It goes back to {when}, at “{cause['moment']}”, when they chose {did} ({how}), and {cause['what']}."
        T = getattr(ES, "THREAD", None); H = getattr(ES, "THREAD_HOVER", None)
        line = hover = ""
        if T and H:                                      # the Library's sentence by what the thread is, its hover first
            k = cause.get("key")
            who = next((self.story.say(p) for p in self.story.alive("partner")), "their partner") if cause.get("kind") == "partner" else ""
            fills = dict(title=art(cause.get("title", "")), who=who, plan=cause.get("goal") or "their plan",
                         dream=cause.get("goal") or "their dream", age=cause["age"])
            if k == "title":
                line, hover = T["title"]["held"], H["title"]["held"]
            elif k == "commitment" and cause.get("kind") in T["commitment"]:
                line, hover = T["commitment"][cause["kind"]], H["commitment"][cause["kind"]]
            elif k in ("plan", "dream"):
                line, hover = T[k], H[k]
            for f_, v_ in fills.items():
                line, hover = line.replace("{" + f_ + "}", str(v_)), hover.replace("{" + f_ + "}", str(v_))
        if not line:
            line = "This goes back to the day {N} chose " + did + "."
        return dict(line=self.story.fill(line), cause=(self.story.fill(hover) + " " if hover else "") + why, age=cause["age"])

    def _ret_line(self, ret, age):
        """Picks come back: the line a return opens on (the earlier pick and how long ago) and, for the hover, that
        moment and how it went. The Library's opener for the seed's kind and side (earth_story THREAD["seed"], or
        THREAD["seed_alone"] for a seed with no person; hover THREAD_HOVER["seed"]) when it has one, else built-in words."""
        yrs = int(age - ret["age"])
        did = chooses(act(plain(ret["act"]))).rstrip(".")
        years = "a year" if yrs < 2 else f"{_num_word(yrs)} years"
        side = "well" if ret["ok"] else "badly"
        how = "you pushed it" if ret.get("pushed") else "they chose it themselves"
        went = "" if ret["ok"] is None else ", and it worked" if ret["ok"] else ", and it went badly"
        why = f"At {int(ret['age'])}, at “{ret['moment']}”, they chose {did} ({how}){went}. What happens now leans on how that went."
        T = getattr(ES, "THREAD", None) or {}; H = getattr(ES, "THREAD_HOVER", None) or {}
        line = (T.get("seed") if ret.get("who") else T.get("seed_alone") or {}) or {}
        line = line.get(ret.get("kind")) or ""
        line = line.get(side, "") if isinstance(line, dict) else line
        hover = H.get("seed") or ""
        hover = hover.get(side, "") if isinstance(hover, dict) else hover
        if not line:
            line = f"{years[:1].upper() + years[1:]} ago, at “{ret['moment']}”, {{N}} chose {did}."
        fills = dict(who=self.story.say(ret["who"]) if ret.get("who") else "someone", years=years, age=str(int(ret["age"])), act=did)
        for f_, v_ in fills.items():
            line, hover = line.replace("{" + f_ + "}", v_), hover.replace("{" + f_ + "}", v_)
        return dict(line=self.story.fill(line), cause=(self.story.fill(hover) + " " if hover else "") + why, age=ret["age"], key="seed")

    def _thread_of(self, loc, s):
        """5.6 and F5: whether moment s follows from this life's own threads (it needs a title or perk they hold, an
        option steps a commitment they hold, or it offers a step toward a plan or dream they hold), and the pick that
        started that thread, when one did (the latest)."""
        L = loc["L"]; GR = L.get("ROLES") if loc.get("RON") else None
        found = []
        if GR is not None and "S_HOLDM" in GR and "r_has" in loc:
            hm = np.asarray(GR["S_HOLDM"][s], bool); has = np.asarray(loc["r_has"][0], bool); n = min(len(hm), len(has))
            found += [("r", int(i)) for i in np.nonzero(hm[:n] & has[:n])[0]]
        com = np.asarray(L["COMMIT"][s])[np.asarray(loc["mask"][0], bool)]
        found += [("c", KNAMES[d]) for d in sorted({int(x) for x in com if x >= 0}) if loc["held"][0, d]]
        if "gsr" in loc and "gk" in loc and "gid" in loc:
            found += [("g", int(loc["gid"][0, j])) for j in np.nonzero(loc["gk"][0] >= 0)[0] if loc["gsr"][0, j, s] >= 0.5]
        causes = [self._threads[f] for f in found if f in self._threads
                  and self.t - self._threads[f]["t"] <= THREAD_YEARS * 52 and self.t - self._threads[f].get("told", -10 ** 6) >= THREAD_AGAIN]
        return bool(found), (max(causes, key=lambda c_: c_["t"]) if causes else None)

    def trust_view(self):
        """Trust per color, for the page and the status screen."""
        return {c: round(float(v), 3) for c, v in zip(COLORS, self.trust)}

    def _tries(self, name):
        """Which try at this title this is: 1 + the misses at it since they last made it."""
        n = 1
        for x in reversed(self.history["long"]):
            if x["name"] == name:
                if x["made"]:
                    break
                n += 1
        return n

    @staticmethod
    def _long_shot(o):
        """Emren 2026-10-06 (packs thread): any title can be pushed for at long odds, and a missed one is a story of its own.
        The title an option reaches for if it works, when it works for fewer than LONG_SHOT of people (the Library's chance,
        else the true odds) or when failing grants the packs' long-shot perk; else None."""
        fx = o.get("roles_fx") or ()
        aim = next((d for d in fx if d["when"] == "ok" and d["gain"] and d.get("title")), None)
        if aim is None:
            return None
        odds = o.get("base", o.get("true"))
        marked = any(d["when"] == "fail" and d["gain"] and "long shot" in str(d.get("name", "")) for d in fx)
        if not marked and (odds is None or odds >= LONG_SHOT or aim.get("kind") not in LONG_SHOT_KINDS):
            return None
        return dict(name=aim["name"], say=aim["say"], odds=None if odds is None else round(float(odds), 3), rung=o.get("rung"))

    def _res_roles(self, loc, events):
        """Titles and perks this choice's week gained or lost (explain.after's title and perk events), as chips."""
        GR = self.L.get("ROLES") if loc.get("RON") else None
        out = []
        for e_ in events:
            if e_.get("kind") not in ("title", "perk") or GR is None or e_["name"] not in GR["ID"]:
                continue
            d = role_info(GR, GR["ID"][e_["name"]]); up = e_["what"] in ("gained", "regained", "restored", "reshaped")
            how = e_.get("how") or ""
            if not up and (how in ("replaced",) or how.startswith("became") or (how.startswith("the ") and how.endswith(" ended"))):
                continue                                # told by the title that replaced or ended it
            d.update(what=e_["what"], how=how, up=up, word=(d["say"] if d["title"] else d["pred"]) if up else
                     ("no longer " + d["say"]) if d["title"] else neg_of(d["pred"]))
            if e_["what"] == "reshaped":
                d["word"] = d["say"] + ", another way"
            if e_.get("profile"):
                d["profile"] = e_["profile"]
            if e_.get("refines"):
                d["on"] = e_["refines"]
            out.append(d)
        return out[:6]

    # ------------------------------------------------------------------ forced picks: costs
    def _follows(self, loc, s, k, felt, commit, recon):
        """What may follow an option, as the character can foresee it from the library's own tags: what it costs,
        what success and failure bring, which needs success meets, and the chance it starts a commitment.
        A placeholder until the engine gives foreseen outcomes for plans."""
        L = loc["L"]
        if loc["do_nothing"][0, k]:
            return dict(cost=[], win=[], lose=[], needs=[], commit_p=0.0)
        def moves(v):
            return [f"{'+' if x > 0 else '-'}{RNAMES[j]}" for j, x in enumerate(v) if abs(x) >= 0.02]
        e = np.maximum(loc["e"][0, k], 0)
        nv = E.NMAP @ e
        needs = [E.NEEDS[j] for j in np.argsort(-nv)[:2] if nv[j] > 0.05] if not recon else []
        cp = 0.0
        if commit >= 0 and not loc["held"][0, commit] and not recon:
            cp = felt * float(loc["P"]["commit_p"][commit])
        return dict(cost=moves(L["PAY"][s, k]), win=moves(L["WIN"][s, k]), lose=moves(L["LOSE"][s, k]),
                    needs=needs, commit_p=cp, lift=[] if recon else self._lift(loc, s, nv))

    def _lift(self, loc, s, nv):
        """Which lacking needs an option's ends would feed if it works, and how much that matters (IDEAS.md, "Make needs
        visible"): the engine's own refill rule (0.12 x stakes x ends' share x room left), read against how low the need
        is now. Needs met is the biggest driver of satisfaction, most of all a need that was lacking."""
        if "need" not in loc:
            return []
        need = loc["need"][0]; st = max(float(loc["L"]["STAKES"][s]), 0.9)
        out = []
        for j in np.argsort(-nv):
            lv = float(need[j])
            if nv[j] <= 0.05 or lv >= GAME["hind_thin"]:
                continue
            gain = 0.12 * st * float(nv[j]) * (1 - lv)
            out.append(dict(need=E.NEEDS[j], level=round(lv, 3), gain=round(gain, 3), word=need_level_word(lv),
                            lift="a big lift" if lv < 0.3 else "a lift"))
        return out[:2]

    @staticmethod
    def _ways(loc, k):
        """An act's ways as shares of one (even when it has none)."""
        m = np.maximum(np.asarray(loc["m"][0, k], float), 0)
        return m / m.sum() if m.sum() > 0 else np.full(C, 1 / C)

    # ------------------------------------------------------------------ S2: making it their own (GAME own_...)
    def _own_k(self, loc, k):
        """S2: what is left of a push's reluctance in act k's ways, 1 - own_rel x how far they have become theirs."""
        if not GAME["own_ix"] or not self.ix.any() or np.maximum(np.asarray(loc["m"][0, k], float), 0).sum() <= 0:
            return 1.0
        return 1.0 - GAME["own_rel"] * float(self._ways(loc, k) @ self.ix)

    @staticmethod
    def _around(loc):
        """S2: the colors around them as shares of one (the engine's "around": their haunts' faces and close people);
        even without it."""
        a = loc.get("around") if loc is not None else None
        a = np.maximum(np.asarray(a, float).reshape(-1)[:C], 0) if a is not None else np.zeros(C)
        return a / a.sum() if a.sum() > 0 else np.full(C, 1 / C)

    def _own_step(self, x):
        return next(k for lo, k in OWN_STEPS if x >= lo)

    def _own_push(self, loc, cpw, hind):
        """S2: a push toward ways the character would not have taken moves how far each has become theirs:
        own_k x push x A x T x S x H per color (GAME own_...). A hard push at high reluctance into a way not yet
        "ought to" can bounce back instead. Returns what moved, for the resolution, or None."""
        k, own = int(cpw["choice"]), int(cpw["own"])
        push = np.maximum(self._ways(loc, k) - self._ways(loc, own), 0)
        if push.sum() <= 0:
            return None
        f = self._force or {}
        before = self.ix.copy(); age = round(self.t / 52, 1)
        way = float(push @ before) / float(push.sum())
        if not f.get("light") and f.get("rel", 0.0) > GAME["own_react_rel"] and way < 0.25 and self._ixrng.random() < GAME["own_react"]:
            self.ix = np.clip(self.ix - GAME["own_react_back"] * push / push.max(), 0.0, 1.0)     # reactance: it bounces back
            loc["Q"][0] += GAME["backlash"] * float(f.get("resent", f.get("rel", 0.0)))
            for c in np.nonzero(self.ix < before)[0]:
                self.history["own_ix"].append((age, COLORS[c], "back"))
            return dict(kind="back", ix=[round(float(x), 3) for x in self.ix])
        A = GAME["own_light"] if f.get("light") else GAME["own_strong"]
        T = np.maximum(0.0, 0.5 + self.trust)
        S = 0.5 + GAME["own_sup"] * self._around(loc)
        judged = (hind or {}).get("kind")
        H = GAME["own_acc"] if judged == "accepted" else GAME["own_res"] if judged == "resented" else 1.0
        self.ix = np.clip(self.ix + GAME["own_k"] * push * A * T * S * H, 0.0, 1.0)
        for c in range(C):
            s0, s1 = self._own_step(before[c]), self._own_step(self.ix[c])
            if s0 != s1:
                self.history["own_ix"].append((age, COLORS[c], s1))
        return dict(kind="step", ix=[round(float(x), 3) for x in self.ix])

    def _own_lived(self, loc, cpw):
        """S2: a light steer toward a color that left them on their own pick, an act that color leads: the way moves
        own_lived x a light push of the act's share in it (own_k x share x own_light x T x S; no hindsight, nothing was
        pushed). Returns what moved, for the resolution, or None."""
        c = COLORS.index(cpw["lean"]); w = self._ways(loc, int(cpw["own"]))
        if int(np.argmax(w)) != c or w.max() - w.min() <= 1e-9:
            return None
        before = float(self.ix[c]); age = round(self.t / 52, 1)
        T = max(0.0, 0.5 + float(self.trust[c])); S = 0.5 + GAME["own_sup"] * float(self._around(loc)[c])
        self.ix[c] = min(1.0, before + GAME["own_k"] * GAME["own_lived"] * float(w[c]) * GAME["own_light"] * T * S)
        if self._own_step(before) != self._own_step(float(self.ix[c])):
            self.history["own_ix"].append((age, COLORS[c], self._own_step(float(self.ix[c]))))
        return dict(kind="step", ix=[round(float(x), 3) for x in self.ix])

    def _own_year(self):
        """S2, once a year: a way that led fewer of the year's acts than own_use times its own expected share fades by up
        to own_fade (a way the year never offered does not fade)."""
        need = GAME["own_use"] * self._ix_exp
        short = np.where(need > 0, np.clip(1 - self._ix_use / np.maximum(need, 1e-9), 0.0, 1.0), 0.0)
        self.ix = np.maximum(0.0, self.ix - GAME["own_fade"] * short)
        self._ix_use[:] = 0; self._ix_exp[:] = 0

    def own_view(self):
        """S2, the Voice row's hover: each way the voice pushed toward (or that has a step), how far it has become theirs,
        in the Library's words for that way (VOICE["own"]: trusted or doubted by their trust in that color)."""
        if not GAME["own_ix"]:
            return []
        d = np.asarray(self.history["voice"]["d"], float)
        V = (ES.VOICE.get("own") if ES is not None else None) or {}
        out = []
        for i, c in enumerate(COLORS):
            if d[i] <= 0 and self.ix[i] <= 0.005:
                continue
            step = self._own_step(float(self.ix[i]))
            lines = (V.get(c) or {}).get(step) or []
            line = self._vfill(lines[0 if self.trust[i] >= 0 else 1]) if lines else ""
            out.append(dict(color=c, ix=round(float(self.ix[i]), 3), step=step, line=line))
        return out

    def _profile(self, loc, k):
        """An act's colors for trust: its ways and its ends, half and half, as shares of one."""
        p = 0.5 * np.maximum(loc["m"][0, k], 0) + 0.5 * np.maximum(loc["e0"][0, k] if "e0" in loc else loc["e"][0, k], 0)
        return p / p.sum() if p.sum() > 0 else np.full(C, 1 / C)

    def _trust_on(self, loc, k):
        """The character's trust in the player along an act's colors, -1 to 1."""
        return float(self._profile(loc, k) @ self.trust)

    @staticmethod
    def _resent(rel, trust):
        """How much of a push's reluctance becomes resentment (stress and pent-up wanting): trust in the act's colors spares
        some of it, distrust adds to it. The effort (lower odds) is the character's own inertia and stays as it is."""
        return rel * (1 - GAME["trust_cut"] * max(trust, 0.0) + GAME["distrust_add"] * max(-trust, 0.0))

    def _on_odds(self, loc, p_true):
        f = self._force
        ret = (self._cp_week or {}).get("cp", {}).get("ret") if GAME["returns"] else None
        if f is None and (ret is None or ret["ok"] is None):
            return p_true
        pt = float(np.clip(p_true[0], 1e-6, 1 - 1e-6))
        lg = np.log(pt / (1 - pt))
        if f is not None:
            lg = lg - GAME["effort"] * f["rel"] - (GAME["out_of_reach"] if f["closed"] else 0.0)
        if ret is not None and ret["ok"] is not None:   # Picks come back: the first time tilts this time, a few points
            lg = lg + (GAME["ret_tilt"] if ret["ok"] else -GAME["ret_tilt"])
        p = p_true.copy(); p[0] = 1 / (1 + np.exp(-lg))
        return p

    def _owned_pick(self, cpw=None, loc=None):
        """v22.5 proposal (GAME own_mark, dream_own): this week's push is the moment's head or heart pick (explain.before's
        marks), or a step toward a dream, passion or plan they hold."""
        cpw = self._cp_week if cpw is None else cpw
        m = GAME["own_mark"]
        if (not m and not GAME["dream_own"]) or cpw is None or cpw["choice"] == cpw["own"]:
            return False
        v = cpw["cp"].get("view") or {}
        marks = ("head", "heart") if m == "both" else (m,) if m else ()
        if any(int(v.get(k, -1)) == int(cpw["choice"]) for k in marks):
            return True
        return bool(GAME["dream_own"]) and self._goal_served(self.loc if loc is None else loc, int(cpw["choice"]))[0] >= 0

    def _goal_served(self, loc, k):
        """v22.5 proposal: the goal slot option k serves most (the engine's goal fit rel, weighed by the goal's strength)
        and that fit, or (-1, 0) when it serves none by at least dream_fit."""
        if loc is None or "rel" not in loc or "gk" not in loc or np.ndim(loc["rel"]) != 3:
            return -1, 0.0
        r_ = np.asarray(loc["rel"][0][:, k], float) * (np.asarray(loc["gk"][0]) >= 0)
        sc = r_ * np.asarray(loc["gs"][0], float)
        if not len(sc):
            return -1, 0.0
        j = int(np.argmax(sc))
        return (j, float(r_[j])) if r_[j] >= GAME["dream_fit"] and sc[j] > 0 else (-1, 0.0)

    def _dream_step(self, loc, k):
        """v22.5 proposal: a push that served a goal worked: the voice's backing firms the goal up (dream_firm) and a plan
        gets dream_help of the engine's own step (fit x stakes x self-control x free time / the plan's size)."""
        j, ra = self._goal_served(loc, k)
        if j < 0:
            return
        P = loc["P"]
        loc["gs"][0, j] += GAME["dream_firm"] * (1 - float(loc["gs"][0, j]))
        if int(loc["gk"][0, j]) == 2 and GAME["dream_help"]:
            st = min(float(np.asarray(loc["stakes"]).ravel()[0]), 1.2)
            if int(loc["gd"][0, j]) < 0:
                step = ra * st * float(loc["ctrl"][0]) * (0.3 + 0.7 * float(loc["res"][0, 1])) / float(P["g_size"][int(loc["ghz"][0, j])])
                loc["gp"][0, j] += GAME["dream_help"] * step
            else:
                loc["gp"][0, j] = min(0.95, float(loc["gp"][0, j]) + 0.1 * ra * GAME["dream_help"])

    def _on_learn(self, loc, delta):
        f = self._force
        if f is None:
            return delta
        rel = f["rel"]; tr = f.get("trust", 0.0)
        f["resent"] = rs = self._resent(rel, tr)
        self._price = self._price_now() + rs + 0.5 * rel; self._price_t = int(self.t)   # 5.6: the price builds
        # item 4 (Emren 10-08 23:18): the price of a push moves from learning to cost. The act teaches in full (v22.1 cut a
        # reluctant act's lesson to learn_keep); what it teaches about who they are is the pivotal lesson (_pivot)
        d = delta
        if not GAME["learn_full"]:                       # off (GAME_OFF): v22.1's cut, trust letting more of it in
            d = delta.copy(); d[0] *= 1 - (1 - GAME["learn_keep"]) * rel * (1 - max(tr, 0.0))
        if self._owned_pick(loc=loc):                    # v22.5 proposal: what they judged best or wanted, and they did it
            loc["stress"][0] += GAME["own_stress"] * GAME["stress"] * rs
            if loc["succ"][0]:
                loc["Q"][0] *= 1 - GAME["own_free"]
                cpw = self._cp_week; v_ = cpw["cp"].get("view") or {}
                if GAME["own_teach"] and "dsc" in loc and int(v_.get("head", -1)) == int(cpw["choice"]):
                    hi_ = float(loc["P"]["disc_range"][1]) if "P" in loc else 1.4
                    loc["dsc"][0] += GAME["own_teach"] * (hi_ - float(loc["dsc"][0]))
                if GAME["dream_firm"] or GAME["dream_help"]:
                    self._dream_step(loc, int(cpw["choice"]))
        else:
            loc["stress"][0] += GAME["stress"] * rs
            loc["Q"][0] += GAME["backlash"] * rs                          # wanting what they were denied builds up
        if f["closed"] and not loc["succ"][0]:
            loc["stress"][0] += GAME["backfire_stress"]
            loc["res"][0, 0] = max(0.0, loc["res"][0, 0] - GAME["backfire_money"])
        f["succ"] = bool(loc["succ"][0])
        return d

    # ------------------------------------------------------------------ narration
    def _met(self, age, ev, sit):
        """What this life met, once each, with the age: moments, the world's readings, titles gained, deeds, deaths close by
        (implementation list item 1: the end of a life told as one paragraph)."""
        h = self.history
        if "situation" in ev:
            kind, name = "sit", sit
        elif "outside" in ev:
            kind, name = "read", ev["outside"]["name"]
        elif "role" in ev and ev["role"]["what"] == "gained":
            if ev["role"].get("kind") not in TITLE_KINDS:
                return                          # skills, bonds, children and partners are not a stage of the life
            kind, name = "role", ev["role"]["name"]
            GR = self.L.get("ROLES")
            if GR is not None and name in GR["ID"]:
                h["title_say"][name] = GR["say"][GR["ID"][name]]      # 'a baker', 'out of work'
        elif "mark" in ev:
            kind, name = "mark", ev["mark"]["mark"]
        elif "death" in ev:
            h["met"].append((round(age, 1), "death", ev["death"]["role"]))    # each death counts
            return
        else:
            return
        if name != "an ordinary week" and not any(m[1] == kind and m[2] == name for m in h["met"]):
            h["met"].append((round(age, 1), kind, name))

    def _say(self, line, level=0, tag="note", **meta):
        if " or " in line and self.loc is not None:     # two-word titles in their own words (N1d §3)
            line = self.gword(line)
        if level <= self.detail:
            if GAME["line_wait"] and line and tag in LINE_WAIT_TAGS:   # F10: a line said word for word waits its years
                said_ = self.__dict__.setdefault("_said_t", {}); k_ = plain(line)
                if self.t - said_.get(k_, -10 ** 9) < GAME["line_wait"] * 52:
                    return
                said_[k_] = self.t
            self.log.append(plain(line))
            if line:
                self.feed.append(dict(tag=tag, text=line, age=round(self.t / 52, 1), **meta))

    def _on_week(self, t, loc):
        if t % 52 == 0 and t >= 3 * 52:
            self._yearly(t, loc)
        if GAME["lean_self"] and self._leans and "z" in loc:   # v22.5 proposal: the way lived becomes who they are
            w_ = E.softmax(loc["z"][0])
            ls_ = GAME["lean_self"] * (float(loc["settle_f"][0]) if "settle_f" in loc else 1.0)   # F14: less with age
            for T, st, t0 in self._leans:
                f = 1 - (t - t0) / GAME["lean_weeks"]
                if f > 0:
                    loc["z"][0] += ls_ * st * f * E.centre(5 * (T - w_))
            for T, st in (getattr(self, "_own_leans", None) or {}).values():   # S2: a way that is theirs keeps leaning both
                loc["z"][0] += ls_ * st * E.centre(5 * (T - w_))
        if self._seasons and "need" in loc:              # v22.5 proposal: an owned pick's season holds, fading
            for e_, st_, t0 in self._seasons:
                f = 1 - (t - t0) / GAME["lean_weeks"]
                if f > 0:
                    nd = loc["need"][0]
                    nd += GAME["season_need"] * 0.12 * st_ * f * (E.NMAP @ e_) * (1 - nd)
                    loc["stress"][0] = max(0.0, float(loc["stress"][0]) - GAME["season_calm"] * f)
            self._seasons = [x for x in self._seasons if t - x[2] < GAME["lean_weeks"]]
        if not self._need_hint and not self.burn_in and "need" in loc and t / 52 >= max(self.start_age, 6):
            j = int(np.argmin(loc["need"][0]))
            if float(loc["need"][0, j]) < GAME["need_thin"]:   # IDEAS.md, "Make needs visible", fix 5: the rule, once
                self._need_hint = True
                self._say(NEED_HINT.format(need=NEED_WORD[E.NEEDS[j]], N=self.name), 0, "hint", need=E.NEEDS[j],
                          need_level=round(float(loc["need"][0, j]), 3))

    def conditions(self, loc):
        """The context the engine times life events by (v6 drivers, about -1..1; trouble and fortune 0..2)."""
        X = loc.get("X")
        if X is None:
            return {}
        return {c: float(X[0, i]) for i, c in enumerate(E.CTX)}

    def shadow_view(self, loc=None):
        """Light and shadow (stage 2, item 2) as the page shows it: per colour its shadow part (the share of the colour in
        shadow, 0 to 1), its force, whether the state shows (the engine's adjective, on above .5 and off below .35), whether
        the person has seen it, the line ("Red 40%, a quarter of it in shadow: reckless at times") and the sources in
        words. None while the engine's shadows switch is off. Reads only; nothing is drawn at random or written back."""
        loc = self.loc if loc is None else loc
        if loc is None or not loc.get("SHON") or "shS" not in loc:
            return None
        w = E.softmax(loc["z"][0]); s = np.asarray(loc["shS"][0]); e = np.asarray(loc["shA"][0])
        src = np.asarray(loc["sh_src"][0]); seen = np.asarray(loc["sh_seen"][0]); sk = np.asarray(loc["P"]["sh_src"], float)
        adj = np.asarray(loc["adj"][0]) if "adj" in loc else None
        cols = []
        for i, c in enumerate(COLORS):
            st = E.SH_STATES[i]; ai = E.ADJ_ID.get(st, -1)
            on = bool(adj is not None and 0 <= ai < len(adj) and adj[ai])
            frac = next(wd for top, wd in SH_FRAC if s[i] < top)
            how = st if on else f"{st} at times" if e[i] >= 0.2 else "hardly felt"
            en = [COLORS[j] for j in np.nonzero(E.ENEMY[i])[0]]
            words = (SH_HOLD[c], f"their {NOUN[c]} rules the rest", f"no {' or '.join(CNAME[x] for x in en)} to argue with",
                     "strain pressing on it")
            order = sorted((j for j in range(4) if src[i, j] >= SH_SRC_SHOW), key=lambda j: -sk[j] * src[i, j])
            cols.append(dict(c=c, state=st, part=round(float(s[i]), 3), force=round(float(e[i]), 3), on=on, seen=bool(seen[i]),
                             show=bool(s[i] >= SH_SHOW),
                             line=f"{CNAME[c]} {round(float(w[i]) * 100)}%, {frac} of it in shadow: {how}" if s[i] >= SH_SHOW else "",
                             src=[words[j] for j in order], src_v=[round(float(x), 3) for x in src[i]]))
        return dict(cols=cols, on=float(E.ADJ_ALL[E.ADJ_ID[E.SH_STATES[0]]][4]), off=float(E.ADJ_ALL[E.ADJ_ID[E.SH_STATES[0]]][5]))

    def shadow_pull(self, loc, k):
        """Item 2, the option card's mark: the colour whose shadow drives the heart's pick k, once the person has seen that
        shadow (seen[c]), else None. The shadow drives it when, without the shadow's overuse bonus (P sh_over x the option's
        colours x the force, the engine's own term on U_I), the heart would pick another option."""
        if k is None or k < 0 or not loc.get("SHON") or "shA" not in loc or "U_I" not in loc:
            return None
        e = np.asarray(loc["shA"][0]); m = np.asarray(loc["m"][0])
        ok = np.asarray(loc["seen"][0]) & ~np.asarray(loc["do_nothing"][0])
        if not ok[k]:
            return None
        shU = float(loc["P"]["sh_over"]) * (m @ e)
        alt = int(np.argmax(np.where(ok, np.asarray(loc["U_I"][0]) - shU, -np.inf)))
        if alt == k or shU[k] <= shU[alt]:
            return None
        c = int(np.argmax(m[k] * e))
        if m[k, c] * e[c] <= 0 or not bool(loc["sh_seen"][0][c]):
            return None
        return dict(c=COLORS[c], state=E.SH_STATES[c], icon=ADJ_LOOK.get(E.SH_STATES[c], ("dot", 0))[0])
