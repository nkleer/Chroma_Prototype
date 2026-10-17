"""Story's methods for moments: thoughts, the voice, births, scenes, acts, outcomes, family, deaths and new kin, marks and streaks.

Part of class Story (story.py), which inherits MomentsMixin; moved out of story.py verbatim. A method here
reads module names through the imports below, the same objects story.py has, and self for everything on the Story."""
import numpy as np
import re
from story_base import (BIG_LOSS, BIG_WIN, BIG_WIN_SOFT, CI, COLORS, DEATH_CHILD, DEATH_FAR, DEATH_LINE, HARDENED,
    HEALED, KINDREF, LEFT_BEHIND, LIB_ECHO, LIB_GRIEF, LIB_OUTCOMES, LIB_OUT_NOT, LIB_READ, LIB_SCENES, MEMORY_YEARS,
    NOW_SHARE, OUTCOMES, OUT_OF_REACH, PERSON_SLOTS, REACT, REACT_GRIEF, REASON, REBOUND_FIT, REBOUND_SPLIT, RELUCT,
    RELUCT_LOW, SCENES, SOMBER, STREAK_BAD, STREAK_GOOD, VALUE, _worlds, act, cap, chooses_mk, mk, phase, plain,
    weights_of)


class MomentsMixin:
    def thought(self, text, kind="", tag=None):
        """An italic thought; its color is the variant's (the voice's, or the act's for a reason)."""
        return mk("t", f"{self.last_tag if tag is None else tag}|{kind}", f"*{text}*")

    def val(self, c):
        """What a color values, in words (marked for the browser)."""
        return mk("v", c, VALUE[c])

    # ---------------------------------------------------------------- the voice
    def update_voice(self, w):
        """Once a year: the memory of past identities takes in the present one, slowly."""
        w = np.asarray(w, float)
        a = 1 - np.exp(-1 / MEMORY_YEARS)
        self.mem = (1 - a) * self.mem + a * w
        self.voice = NOW_SHARE * w + (1 - NOW_SHARE) * self.mem

    def leading(self, v=None, n=2, thr=0.215):
        v = self.voice if v is None else v
        order = [COLORS[i] for i in np.argsort(-v)]
        return [c for c in order[:n] if v[CI[c]] >= thr] or order[:1]

    # ---------------------------------------------------------------- birth
    def birth(self, blurb=""):
        ctx = {}
        fam = [self.say(p) for p in self.alive("mother") + self.alive("father")]
        g = self.alive("grandparent"); s = self.alive("sibling")
        L = [f"{self.name} is born in {self.birth_place or 'a ' + self.place}. " + (blurb + " " if blurb else "")
             + f"The family: {fam[0]} and {fam[1]}"
             + (", " + " and ".join(self.say(p) for p in g) if g else "")
             + (", and " + " and ".join(self.say(x) for x in s) if s else "") + "."]
        return cap(" ".join(L))

    # ---------------------------------------------------------------- moments
    def moment(self, t, sit, stage, age, kind=None, kills=None, who=None):
        """The scene of this week's situation, built once (a checkpoint and its outcome share it).
        kills: the role who dies in it (the library's kills: field); a bereavement without one takes anyone close."""
        m = self._moment.get(t)
        if m is not None and m["sit"] == sit:
            return m
        ph = phase(age)
        ctx = dict(_age=age)
        if self.one_roll:                               # F7: the scene's dead fit it (DEAD_FRESH)
            ctx["_sit"] = sit
        if self.one_roll and sit == "a child is born":   # F7: the scene's child is the newborn
            ctx["_birth"] = True
        if kills or sit == "bereavement":
            ctx["_dying"] = kills or "anyone"
            if kills:
                p = self._who_dies(age, kills)
                ctx["_p_dead"] = p; ctx["_p_" + kills] = p
        if kind:
            ctx["kind"] = kind
            ps = self.alive("partner")
            ctx["kindref"] = (f"their life with {ps[0]['name']}" if ps else "their relationship") if kind == "partner" else KINDREF.get(kind, "their " + kind)
        tpl = self.pick(LIB_SCENES[sit], ph) if sit in LIB_SCENES else ""
        if not tpl and sit in SCENES:
            tpl = self.pick(SCENES[sit], ph)
        if not tpl and sit in LIB_SCENES:           # a Library moment not yet written for this world
            tpl = cap(act(sit)) + "."
        if who is None:                             # who: Picks come back's seed person (the game's returns), else
            who = self.marks.get(LIB_ECHO.get(sit))     # the latest person of the mark the echo answers
        if who is not None and who["alive"]:        # an echo: the same person as in the act it answers
            slot = next((x for x in re.findall(r"\{(\w+)\}", tpl) if x in PERSON_SLOTS), None)
            if slot:
                ctx["_p_" + slot] = who
        m = dict(sit=sit, ctx=ctx, tpl=tpl, text=None, stage=ph, age=age)
        self._moment = {t: m}
        return m

    def scene(self, m):
        """The scene's text, filled the first time it is told (people are introduced only when the player meets them)."""
        if m["text"] is None:
            m["text"] = self.fill(m["tpl"], m["stage"], m["ctx"]) if m["tpl"] else ""
            if m["sit"] == "a close friend moves away":
                if "_p_friend" not in m["ctx"]:         # the scene did not name them; the outcome may
                    m["ctx"]["_p_friend"] = self.get("friend", "their friend {n}")
                self.far(m["ctx"]["_p_friend"])
            elif m["sit"] == "the family moves to a new town":
                self.left_behind()
        return m["text"]

    def far(self, p):
        """Someone moves away: still alive and remembered by name, but no longer the one down the street."""
        if p is not None and p["alive"] and not p["role"].startswith("old "):
            p["role"] = "old " + p["role"]

    def left_behind(self):
        """A move: friends, rivals, teachers and neighbours stay in the old place; new ones come with the new one."""
        for p in self.people:
            if p["role"] in LEFT_BEHIND:
                self.far(p)

    def slots_in(self, text, m):
        """v22.4's moments (game.py _social_slots marks them): the slots in an option's label or act ({friend}, {place_a},
        {offer}...) as the moment's scene fills them, in plain words and lower case as written."""
        if not text or "{" not in text or not m:
            return text
        out = plain(self.fill(text, m["stage"], m["ctx"]))
        return out[:1].lower() + out[1:] if text[:1].islower() else out

    def act_in(self, m, label):
        """An option label as the character's act in this moment ('reshape it ...' names what is reshaped)."""
        a = act(label)
        if m and m["ctx"].get("_social"):
            a = self.slots_in(a, m)
        ref = m["ctx"].get("kindref") if m else None
        if ref:
            a = "walk away from " + ref if a == "walk away" else re.sub(r"\bit\b", ref, a)
        return a

    def recon_note(self, kind, years, asks, wants):
        """How long a commitment has been held, what it asks and what they want now, in words."""
        n = "a year" if years < 1.5 else f"{years:.0f} years"
        ps = self.alive("partner")
        held = dict(career="{N} has done this work for {n}.", partner="{N} has been with {p} for {n}.",
                    children="{N} has been raising a family for {n}.", community="{N} has belonged to the community for {n}.",
                    faith="{N} has kept the faith for {n}.").get(kind, "{N} has held their " + kind + " for {n}.")
        line = self.fill(held, ctx=dict(n=n, p=self.nm(ps[0]) if ps else "their partner"))
        if asks == wants:
            return line + " It still fits who they are, mostly; yet something nags."
        return line + f" It asks them to be {asks}; lately they want to be {wants}."

    def reason(self, colors):
        """Why they lean toward an act, in their own words: the act's colors speak."""
        return self.thought(self.pick([(c, x) for c in REASON for x in REASON[c]], v=weights_of(colors)), "reason")

    def confidence(self, felt):
        n = self.name
        return (f"{n} feels sure of it." if felt > 0.7 else f"{n} thinks it could work." if felt > 0.45 else
                f"{n} is not sure it will work." if felt > 0.25 else f"{n} doubts it will work at all.")

    def _result(self, m, ev):
        sit = m["sit"]; succ = bool(ev["success"]); d = float(ev.get("delta", 0.0))
        lines = (LIB_OUTCOMES.get(sit) or OUTCOMES.get(sit) or (["It works."], ["It goes badly."]))[0 if succ else 1]
        k = int(self.rng.integers(len(lines)))
        if sit in LIB_OUT_NOT and sit in LIB_OUTCOMES:   # F11b: a line that fits the act they took (the same draw from the stream)
            ix, nots = LIB_OUT_NOT[sit]
            j = ix.get(ev.get("choice"))
            no = nots[0 if succ else 1]
            if j is not None and len(no) == len(lines) and j in no[k]:
                fit = [i for i in range(len(lines)) if j not in no[i]]
                if fit:
                    k = fit[k % len(fit)]
        out = self.fill(lines[k], m["stage"], m["ctx"])
        if succ and d > 0.6:
            out += " " + self.fill(self.pick(BIG_WIN_SOFT if sit in SOMBER or sit in LIB_GRIEF else BIG_WIN))
        elif not succ and d < -1.0:
            out += " " + self.fill(self.pick(BIG_LOSS))
        return out

    def react(self, succ, sit=None):
        src = REACT_GRIEF if sit == "bereavement" or sit in LIB_GRIEF else REACT
        pool = [(c, x) for c in src for x in src[c][0 if succ else 1]]
        return self.thought(self.pick(pool), "react")

    def outcome(self, m, ev, chosen_label, pushed, rel, closed, colors=""):
        """A checkpoint resolved: what they did, how it went, and how they read it."""
        if m and "{" in chosen_label:                  # the option's role slots, as the player saw them
            chosen_label = self.fill_label(chosen_label, m)
        a = self.act_in(m, chosen_label)
        if not pushed:
            first = self.fill(self.pick(["{N} chooses {c}.", "So {N} chooses {c}.", "In the end, {N} chooses {c}."]),
                              ctx=dict(c=chooses_mk(a, colors)))
        else:
            if closed:
                inner = self.pick(OUT_OF_REACH)
            elif rel < 0.3:
                inner = self.pick(RELUCT_LOW)
            else:
                inner = self.pick([(c, x) for c in RELUCT for x in RELUCT[c]])
            first = self.fill("You push, and {N} goes along: they {a}. ", ctx=dict(a=mk("a", colors, a))) + self.thought(inner, "reluct")
        L = [first, self._result(m, ev) + " " + self.react(ev["success"], m["sit"])]
        if pushed and rel >= 0.3:
            L.append(self.fill("It costs {N}: strain, and a wanting they swallow for now."))
        if pushed and closed and not ev["success"]:
            L.append(self.world_word("backfire", "Forcing what was out of reach backfires: more stress, and money lost."))
        return "\n".join(L)

    def world_word(self, key, default=None):
        """v22.5, F12 (world_hold): the Library's word for key in this world (worlds.py WORDS), else default."""
        wd_ = _worlds() if self.hold else None
        return getattr(wd_, "WORDS", {}).get(self.setting, {}).get(key, default) if wd_ is not None else default

    def set_family(self, siblings, grandparents):
        """Match the family to the engine's (the Earth batch draws siblings and grandparents per person)."""
        for role, n, refs in (("sibling", siblings, None), ("grandparent", grandparents,
                              ["their grandmother {n}", "their grandfather {n}", "their other grandmother {n}", "their other grandfather {n}"])):
            have = self.alive(role)
            for p in have[n:]:
                self.people.remove(p)
            for i in range(len(have), n):
                ref = refs[i] if refs else "their " + ("older" if self.rng.random() < 0.5 else "younger") + " sibling {n}"
                self.new(role, ref)

    def death(self, d, m, age, alone=False):
        """The engine's record of a death (Earth batch). Returns a line, or None when a told scene already showed it.
        alone: a partner's death with no widowed commitment this week (with the world on it can come without one)."""
        role = d["role"]
        p = m["ctx"].get("_p_dead") if m is not None and m["ctx"].get("_dying") == role else None
        if p is None or not p["alive"]:
            p = self._who_dies(age, role)
        told = m is not None and m["text"] is not None and m["ctx"].get("_p_dead") is p
        self.dies(p)
        if told:
            self._told_dead.add(p["name"])
            return None
        if role == "partner" and not alone:         # the partnership's end tells it (commitment: widowed)
            return None
        if role == "partner":
            self._told_dead.add(p["name"])
        lines = DEATH_CHILD if role == "child" else DEATH_LINE
        return self.fill(self.pick(lines, phase(age)), phase(age), dict(_p_dead=p, _age=age))

    def settle(self, c):
        """A commitment's end that a moment already told: the people change as the line would have changed them."""
        kind, what = c["kind"], c["what"]
        if kind == "partner" and what in ("left", "broke up"):
            for q in self.alive("partner"):
                q["role"] = "ex"
        elif kind == "career" and what in ("left", "lost job"):
            for b in self.alive("boss"):
                b["role"] = "former boss"
        elif what == "widowed":
            ps = self.alive("partner")
            if ps:
                self.dies(ps[0])

    def world_siblings(self, sexes):
        """With the outer world on, the siblings at the birth are the world's: older ones, in the world's sexes."""
        for p, sx in zip(self.alive("sibling"), list(sexes) + [None] * len(self.alive("sibling"))):
            if sx is not None:
                self._used.discard(p["name"]); p["name"] = self._name(sx)
            p["ref"] = "their older " + {"f": "sister", "m": "brother"}.get(sx, "sibling") + " " + p["name"]

    def new_kin(self, role, n, sexes=(), told=True):
        """The engine's family grew (with the outer world on, younger siblings are born into it): add the newcomers, in
        the world's sexes when known. Returns the line, or None when they were there all along (told False)."""
        out = []
        for i in range(n):
            sx = sexes[i] if i < len(sexes) else None
            word = {"f": "sister", "m": "brother"}.get(sx, "sibling")
            p = self.new(role, ("their younger " if told else "their older ") + word + " {n}", sex=sx)
            out.append(p)
        if not told or not out:
            return None
        if len(out) == 1:
            w_ = {"f": "sister", "m": "brother"}.get(sexes[0] if sexes else None, "sibling")
            return self.fill("{N} has a new baby " + w_ + ": " + self.nm(out[0]) + ".")
        return self.fill("New babies in the family: " + " and ".join(self.nm(p) for p in out) + ".")

    def later_child(self, taken=False):
        """One more child (R15: a later child born or taken in while there are children already): a line. taken (F7): the
        week's moment took a child in, so the line says so instead of a birth."""
        ch = self.new("child", "a child, {n}"); ch["born"] = True
        line = self.fill(("{N} takes in another child, " + self.nm(ch) + ", who needs a home.") if taken else
                         ("Another child is born to {N}: " + self.nm(ch) + "."))
        ch["ref"] = "their child " + ch["name"]
        return line

    def quiet_deaths(self, role, left, age):
        """Grandparents of grown-up grandchildren die outside the Library's moments: say so briefly."""
        out = []
        gone = self.alive(role)[left:] if left < len(self.alive(role)) else []
        if self.one_roll and gone:                  # F7: those the world lost, before anyone the story picks
            due = [p for r, p in self.due if p["alive"] and p["role"] == role]
            gone = (due + [p for p in self.alive(role) if p not in due])[:len(gone)]
        for p in gone:
            self.dies(p)
            out.append(self.fill(self.pick(DEATH_FAR), phase(age), dict(_p_dead=p, _age=age)))
        return " ".join(out) or None

    def mark(self, mk, m):
        """An act left a mark: remember who was in the scene, so an echo can bring them back."""
        if m is None:
            return
        for slot in PERSON_SLOTS:
            p = m["ctx"].get("_p_" + slot)
            if p is not None:
                self.marks[mk] = p
                return

    def read(self, r, stage, color=""):
        """An outside event read through the character's colors (Earth batch): the scene and how they take it. color: the
        color the reading pulls their wanting toward, shown as its chip (the game's lines_tied, item 6)."""
        ev = LIB_READ.get(r["name"])
        scene = self.fill(r["_scene"], phase(r["age"]), dict(_age=r["age"])) if r.get("_scene") else \
            self.fill(self.pick(ev["scenes"], phase(r["age"])), phase(r["age"]), dict(_age=r["age"])) if ev and ev["scenes"] else ""
        say = self.fill(r["say"], phase(r["age"]), dict(_age=r["age"])) if r.get("say") else \
            self.fill("{N} takes it as " + r["reading"] + ".")
        return (scene + " " + mk("r", f"{r.get('reading', '')}|{float(r.get('impact', 0)):.2f}" + (f"|{color}" if color else ""),
                                 say)).strip()

    def tally(self, v):
        """An everyday week that was not told still counts toward the year's picture of how the weeks were spent."""
        v = np.maximum(np.asarray(v, float), 0)
        if v.sum() > 0:
            self.year["weeks"] += v / v.sum()

    def rebound(self, worked, span=0.0):
        """An act that joined colors the world sets against each other: it fit together, or it tore."""
        return mk("b", f"{'fit' if worked else 'tear'}|{span:.2f}", self.fill(self.pick(REBOUND_FIT if worked else REBOUND_SPLIT)))

    def aftermath(self, supported, age, wound=0.0, support=0.0):
        """After a hard blow (engine v6): with support a person comes back to their core; alone it hardens into them."""
        ctx = dict(_age=age)
        return mk("h", f"{'healed' if supported else 'hardened'}|{wound:.2f}|{support:.2f}",
                  self.fill(self.pick(HEALED if supported else HARDENED, phase(age)), phase(age), ctx))

    def streak(self, bad, level=0.0):
        return mk("q", f"{'trouble' if bad else 'fortune'}|{level:.2f}", self.fill(self.pick(STREAK_BAD if bad else STREAK_GOOD)))
