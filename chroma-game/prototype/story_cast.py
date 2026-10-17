"""Story's methods for the cast: roles, who is due and who dies, picking people, filling the slots of a line.

Part of class Story (story.py), which inherits CastMixin; moved out of story.py verbatim. A method here
reads module names through the imports below, the same objects story.py has, and self for everything on the Story."""
import numpy as np
import re
from story_base import (CI, DEAD_FRESH, DEAD_LATELY, KILLS, NEW_KIN, ROLL_KIN, SHARP, STAGESETS, WORLD_LEAKS, cap,
    plain)


class CastMixin:
    def role(self, slot, stage, ctx):
        """Fill a role slot with a person (created when the story first needs them)."""
        if "_p_" + slot in ctx:
            return self.say(ctx["_p_" + slot])
        if slot in ctx:
            return ctx[slot]
        p = None
        if slot == "parent":
            ps = self.alive("mother") + self.alive("father")
            p = ps[int(self.rng.integers(len(ps)))] if ps else self.get("aunt", "their aunt {n}")
        elif slot == "grandparent":
            ps = self.alive("grandparent")
            p = ps[0] if ps else None
            if p is None and self.one_roll:             # F7: the eldest of the living takes the grandparents' seat
                ps = self.alive("mother") + self.alive("father") or self.alive("aunt") or self.alive("mentor")
                p = ps[0] if ps else self.get("old neighbour", "their old neighbour {n}")
            if p is None:
                ctx[slot] = "their late grandparents"
                return ctx[slot]
        elif slot == "elder":
            ps = self.alive("grandparent") or self.alive("mother") + self.alive("father") or self.alive("mentor")
            p = ps[0] if ps else self.get("old neighbour", "their old neighbour {n}")
        elif slot == "sibling":
            p = self.get("sibling") if self.alive("sibling") else self.get("cousin", "their cousin {n}")
        elif slot == "partner":
            p = self.get("partner") if self.alive("partner") else self.get("companion", "their companion {n}")
        elif slot == "friend":
            p = self.get("friend", "their friend {n}")
        elif slot == "friend2":
            fs = self.alive("friend")
            p = fs[1] if len(fs) > 1 else self.new("friend", "their friend {n}")
        elif slot == "newfriend":
            p = self.new("friend", "someone called {n}")
        elif slot == "rival":
            p = self.get("rival", self.W["classmate"] if stage <= 1 else "their rival {n}")
        elif slot == "mentor":
            p = self.new("mentor", (self.W["teacher"] if stage <= 1 else self.W["elder_mentor"]))
        elif slot == "teacher":
            p = self.get("teacher", self.W["teacher"])
        elif slot == "boss":
            p = self.get("boss", self.W["boss"])
        elif slot == "colleague":
            p = self.get("colleague", self.W["colleague"])
        elif slot == "child" and self.one_roll:        # F7: a birth names the newborn; otherwise the youngest at home
            ks = sorted(self.alive("child"), key=lambda q: q.get("made", 0))
            if ctx.get("_birth"):
                p = ks[-1] if ks and not ks[-1].get("born") and self.age - ks[-1].get("made", -99) < 0.1 else \
                    self.new("child", "their newborn {n}")
            elif ks or self.kids_n > 0:
                p = ks[-1] if ks else self.new("child", "their child {n}")
            else:                                       # no child of their own: the young one is family's, not theirs
                p = self.get("cousin", "their young cousin {n}")
        elif slot == "child":
            p = self.get("child", "their child {n}")
        elif slot == "prospect":
            p = self.new("prospect", "someone called {n}")
        elif slot == "close":
            ps = self.alive("partner") or self.alive("friend") or self.alive("sibling")
            p = ps[0] if ps else self.get("friend", "their friend {n}")
        elif slot == "carer":
            ps = self.alive("partner") or self.alive("mother") + self.alive("father") or self.alive("child") or self.alive("friend")
            p = ps[0] if ps else self.get("neighbour", "their neighbour {n}")
        elif slot == "dead":
            if ctx.get("_dying"):                       # a death scene: someone alive is about to die
                p = self._who_dies(ctx.get("_age", 30), ctx["_dying"])
            elif self.one_roll and ctx.get("_sit") in DEAD_FRESH:   # F7: a funeral's dead died lately (a friend's, a friend)
                fr_ = "friend" in ctx["_sit"]
                ps = [q for q in self._dead if ctx.get("_age", self.age) - q.get("gone", -99.0) <= DEAD_LATELY
                      and (not fr_ or q["role"] == "friend")]
                p = ps[-1] if ps else self.new("friend", "their friend {n}") if fr_ else \
                    self.new("late relative", "their late " + ("aunt" if self.rng.random() < 0.5 else "uncle") + " {n}")
                if not ps:
                    self.dies(p)
            elif self._dead:                            # otherwise the dead are those already gone
                p = self._dead[-1]
            else:
                p = self.new("late relative", "their late " + ("aunt" if self.rng.random() < 0.5 else "uncle") + " {n}")
                self.dies(p)
        elif slot == "disaster":
            age = ctx.get("_age", 0)
            if self._disaster is None or age - self._disaster[1] > 1.0:       # the same disaster, if one struck lately
                ds = self.W["disasters"]
                self._disaster = (ds[int(self.rng.integers(len(ds)))], age)
            ctx[slot] = self._disaster[0]
            return ctx[slot]
        elif slot == "brush":
            ctx[slot] = self.W["brushes"][int(self.rng.integers(len(self.W["brushes"])))]
            return ctx[slot]
        if p is None:
            ctx[slot] = "someone"
            return ctx[slot]
        ctx["_p_" + slot] = p
        ctx[slot] = self.say(p)
        return ctx[slot]

    def due_pop(self, kills=None):
        """F7: the first person the world has lost whom the story has not yet told, of the engine role kills (any, for a
        death that names none); None when there is none."""
        self.due = [(r, p) for r, p in self.due if p["alive"]]
        for i, (r, p) in enumerate(self.due):
            if kills in (None, "anyone") or r == kills:
                return self.due.pop(i)[1]
        return None

    def dies(self, p):
        if p is not None and p["alive"]:
            p["alive"] = False
            self._dead.append(p)
            if self.one_roll:
                p["gone"] = self.age                # F7: when, for the world's record of the same death

    def _who_dies(self, age, kills="anyone"):
        """Someone close dies. A library event can name the role (kills: parent, sibling, ...); otherwise
        grandparents first, then parents, later friends and siblings."""
        if self.one_roll:                           # F7: the one the world lost, when it has said who
            p = self.due_pop(kills)
            if p is not None:
                return p
            if kills == "partner" and not self.alive("partner") and self.alive("ex"):
                return self.alive("ex")[-1]             # a partner the story knew, though they had parted
        roles = KILLS.get(kills, ())
        named = [p for r in roles for p in self.alive(r)]
        if named:
            return named[0] if kills == "grandparent" else named[int(self.rng.integers(len(named)))]
        if kills in NEW_KIN:                        # the engine knows this person exists; the story meets them now
            return self.new(*NEW_KIN[kills])
        cands = []
        for p in self.people:
            if not p["alive"] or (self.one_roll and p["role"] in ROLL_KIN):   # F7: the engine's kin die only by its roll
                continue
            w = {"grandparent": 1.0 + age / 30, "mother": max(0.0, (age - 18) / 25), "father": max(0.0, (age - 18) / 25),
                 "sibling": max(0.0, (age - 45) / 60), "friend": max(0.0, (age - 40) / 80), "mentor": max(0.0, (age - 25) / 60),
                 "aunt": 0.3, "old neighbour": 0.3}.get(p["role"], 0.0)
            if w > 0:
                cands.append((w, p))
        cands.append((0.15, None))
        ws = np.array([w for w, _ in cands]); i = int(self.rng.choice(len(cands), p=ws / ws.sum()))
        p = cands[i][1]
        if p is None:
            p = self.new("old neighbour", "their old neighbour {n}" if age >= 25 else "their neighbour {n}")
        return p

    # ---------------------------------------------------------------- telling
    def pick(self, pool, stage=None, v=None):
        """One variant from a pool of (colors, text[, stages]), drawn by the voice (or by v)."""
        v = self.voice if v is None else v
        cands = []
        for e in pool:
            if isinstance(e, str):
                e = ("", e)
            if len(e) > 2:
                st = [c for c in e[2] if c.islower()]; wl = [c for c in e[2] if c.isupper()]
                if wl and self.wcode not in wl:
                    continue
                if st and stage is not None and not any(stage in STAGESETS[c] for c in st):
                    continue
            if self.hold and e[1] in WORLD_LEAKS.get(self.wcode, ()):   # F12: no money or sirens in the clan
                continue
            tag = e[0]
            w = float(np.mean([v[CI[c]] for c in tag])) if tag else 0.12
            cands.append((max(w, 1e-3) ** SHARP, e[1], tag))
        if not cands:
            self.last_tag = ""
            return ""
        fresh = [c for c in cands if c[1] not in self._recent] or cands
        ws = np.array([c[0] for c in fresh])
        _, text, self.last_tag = fresh[int(self.rng.choice(len(fresh), p=ws / ws.sum()))]
        self._recent.append(text)
        return text

    def fill(self, text, stage=0, ctx=None):
        ctx = {} if ctx is None else ctx
        def one(m):
            out = _one(m)
            if m.group(2):
                out = re.sub(r"^((?:⟦[^⟧]*⟧)*)someone called ", r"\1", out)
            return out + (m.group(2) or "")

        def _one(m):
            k = m.group(1)
            if k == "N":
                return self.name
            if k == "Ns":
                return self.name + "'s"
            if k == "place":                     # the town, or the place a moment is about (v22.4's caught, odd, lead)
                return str(ctx["place"]) if "place" in ctx else self.place
            if k == "seen_as":                   # N1d: girl or boy, young woman or young man, woman or man, as their world sees them
                f_ = getattr(self, "seen_as", None)
                return f_() if callable(f_) else "person"
            if k == "title":                     # the Library's {title}: the title that brought them here (engine next hand-off)
                return getattr(self, "title_now", None) or "their role"
            if "_p_" + k in ctx:
                return self.say(ctx["_p_" + k])
            if k in ctx:
                return str(ctx[k])
            if k.endswith("_cap"):
                return cap(self.role(k[:-4], stage, ctx))
            return self.role(k, stage, ctx)
        out = re.sub(r"\{(\w+)\}('s)?", one, text)
        # a {title} inside a filled-in act (an option's label in "{N} chooses {c}") is the held title too
        return cap(out.replace("{title}", getattr(self, "title_now", None) or "their role"))

    def fill_label(self, text, m):
        """An option's label with its role slots filled from the moment's own people (the scene's {friend} is the
        option's {friend}), as plain words for the page's buttons and the "chooses" line."""
        ctx, stage = m["ctx"], m["stage"]
        def one(mm):
            k = mm.group(1)
            if k == "N":
                out = self.name
            elif k == "Ns":
                out = self.name + "'s"
            elif k == "place":
                out = self.place
            elif k == "title":
                out = getattr(self, "title_now", None) or "their role"
            else:
                out = plain(self.role(k, stage, ctx))
                if mm.group(2):
                    out = re.sub(r"^someone called ", "", out)
            return out + (mm.group(2) or "")
        return re.sub(r"\{(\w+)\}('s)?", one, text)
