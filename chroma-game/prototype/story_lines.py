"""Story's methods for the lines between moments: ordinary weeks, outside events, eras, titles, commitments, clashes, rites, conversions, breakthroughs.

Part of class Story (story.py), which inherits LinesMixin; moved out of story.py verbatim. A method here
reads module names through the imports below, the same objects story.py has, and self for everything on the Story."""
import numpy as np
from story_base import (CAREER, CAUSES, CLASH_HOW, COLORS, FAITH_ADJ, LOSS_LEAD, MISSED, NOTABLE, OUTSIDE, REASON,
    RITE, RITE_QUIET, SEVERE, SNOUN, STATUS_LINE, STATUS_WORD, TAKEN_IN, TOOK, TOOK_SMALL, VALUE, VALUE2, act, an,
    cap, chooses_mk, mk, neg_of, phase)


class LinesMixin:
    def told_moment(self, m, ev, colors=""):
        """A moment the player did not decide, told briefly: the scene, the act, the result."""
        a = self.act_in(m, ev["choice"])
        line = (self.scene(m) + " " + self.fill("{N} chooses {c}. ", ctx=dict(c=chooses_mk(a, colors)))).lstrip() + self._result(m, ev)
        gate = ev.get("gate"); wanted = ev.get("wanted")
        if gate and gate != "chosen" and wanted and wanted != ev["choice"]:
            w = self.act_in(m, wanted)
            why = {"pulled away": "{N} meant to {w}, but old habits won.",
                   "lacked the means": "{N} would rather have chosen {cw}, but could not manage it.",
                   "not offered": "{N} would rather have chosen {cw}, but nobody around them offered that."}.get(gate)
            if why:
                line += " " + self.fill(why, ctx=dict(w=mk("w", gate, w), cw=chooses_mk(w, gate, "w")))
            if why:
                line += " " + self.thought(self.pick(MISSED[0] if ev["success"] else MISSED[1]), "missed")
                return line
        if abs(float(ev.get("delta", 0))) > 0.25:
            line += " " + self.react(ev["success"], m["sit"])
        return line

    def ordinary(self, ev, k):
        """An ordinary week, told only at the most detailed level; always counted for the chapter."""
        if 0 <= k < 5:
            self.year["weeks"][k] += 1
        return self.fill("An ordinary week: {N} chooses to {a}.", ctx=dict(a=mk("a", COLORS[k] if 0 <= k < 5 else "", act(ev["choice"]))))

    # ---------------------------------------------------------------- the world and the life's turns
    def outside(self, o, stage, detail, tied=False):
        """An outside event, or None when it is not worth telling at this level of detail. tied (the game's lines_tied, item
        6): an event that carried a message always shows its color, with a small mark when it moved them little."""
        name = o["name"]; took = o.get("took")
        moved = took is not None and abs(took) > 0.45
        stage = phase(o["age"])
        if name == "small daily frictions add up":
            self.year["frictions"] += 1
        if detail < 2:
            if detail == 0 and name not in SEVERE:
                return None
            if detail == 1 and name not in NOTABLE and not moved:
                return None
        ctx = dict(_age=o["age"])
        if name == "moving somewhere new":
            old = self.place
            pl = [p for p in self.W["places"] if p != old]
            self.place = pl[int(self.rng.integers(len(pl)))]
            ctx.update(oldplace=old, newplace=self.place)
            again = self._moved_at is not None and o["age"] - self._moved_at < 1.0
            self._moved_at = o["age"]
            self.left_behind()
            if again:                   # a second move in a row
                return self.fill("Before they have even settled in, {N} moves again, this time to " + an(self.place) + ".")
        if name == "an institution rewards a kind of person":
            ctx["inst"] = self.W["inst"][0 if stage <= 1 else 1 if stage <= 3 else 2]
            ctx["inst_cap"] = cap(ctx["inst"])
        if name == "a brush with death":
            bs = self.W["brushes"]
            ctx["brush"] = bs[int(self.rng.integers(len(bs)))]; ctx["brush_cap"] = cap(ctx["brush"])
        line = self.fill(self.pick(OUTSIDE.get(name, [("", name + ".")]), stage), stage, ctx)
        chip = "|1" if tied else ""                     # item 6: the page shows the color as a chip
        if moved and o.get("message"):
            v = np.asarray(o["message"], float)
            c = COLORS[int(np.argmax(v))]
            if took > 0:
                line += " " + mk("x", f"{took:+.2f}|{c}{chip}", self.fill(self.pick(TOOK[0]), ctx=dict(value=(VALUE, VALUE2)[int(self.rng.integers(2))][c])))
            else:
                line += " " + mk("x", f"{took:+.2f}|{c}{chip}", self.fill(self.pick(TOOK[1])))
        elif tied and took is not None and o.get("message"):
            c = COLORS[int(np.argmax(np.asarray(o["message"], float)))]
            say = TOOK_SMALL["up" if took > 0.15 else "down" if took < -0.15 else "flat"]
            line += " " + mk("x", f"{took:+.2f}|{c}{chip}", self.fill(say))
        return line

    def era(self, e):
        took = e["took"]
        react = ("{N} takes to it." if took > 0.3 else "{N} sets their face against it." if took < -0.3 else "{N} barely notices.")
        return self.fill("The times are turning. " + self.W["era"].get(e["kind"], "") + " Everywhere, the talk is of "
                         + mk("e", e["kind"], e["idea"]) + ". " + mk("x", f"{took:+.2f}|era", react))

    def role_mark(self, d, text=None, state=""):
        """A title or perk as a hoverable phrase (marker o): the browser shows its kind, ways and what it does."""
        return mk("o", f"{d['name']}|{d['kind']}|{d['ways']}|{1 if d['title'] else 0}|{d.get('plus', 0)}|{state}",
                  d["say"] if text is None else text)

    def title_line(self, r, d, frm=None):
        """A title or perk gained, lost, suspended or restored (the engine's role event r, the catalogue's words d; frm: the
        title it grew from)."""
        what, how = r["what"], r["how"]
        lead = LOSS_LEAD.get(how, "") if what in ("lost", "suspended") else ""
        if what == "reshaped" and d["title"]:          # the same title, held another way now (the new profile's words)
            way = how.strip().rstrip(".")
            if not way or way == "in other ways":
                return self.fill("{N} is still " + self.role_mark(d) + ", but holds it differently now.")
            return self.fill("{N} is still " + self.role_mark(d) + ", and now " + way[0].lower() + way[1:] + ".")
        if d["title"]:
            if what == "gained":
                if d["kind"] == "status" and d["name"] in STATUS_LINE:
                    tpl, word = STATUS_LINE[d["name"]]
                    return self.fill(tpl.replace("<o>", self.role_mark(d, word)))
                if how == "changed jobs":
                    return self.fill("{N} changes jobs, and is " + self.role_mark(d) + " now.")
                if frm and d["kind"] in ("career", "community"):
                    return self.fill("{N} is " + self.role_mark(d) + " now, after being " + frm + ".")
                return self.fill("{N} is " + self.role_mark(d) + " now.")
            if what == "lost":
                if how == "gave it up":
                    return self.fill("{N} gives up being " + self.role_mark(d, state="lost") + ".")
                if how == "outgrew it" and d["kind"] in ("community", "career"):
                    return self.fill("{N} has outgrown being " + self.role_mark(d, state="lost") + ".")
                return self.fill(lead + "{N} is no longer " + self.role_mark(d, STATUS_WORD.get(d["name"], d["say"]), "lost") + ".")
            return ""
        pred = d["pred"]
        if what in ("gained", "regained", "restored"):
            again = what != "gained" or how == "regained"
            return self.fill("{N} " + self.role_mark(d, pred) + (" again." if again else "." if pred.startswith("always ") else " now."))
        if what == "suspended":
            return self.fill(lead + "{N} " + self.role_mark(d, neg_of(pred), "suspended") + ", for a while.")
        if what == "lost":
            lead = "Out of practice, " if how == "slipped away" and d["kind"] == "skill" else lead
            return self.fill(lead + "{N} " + self.role_mark(d, neg_of(pred), "lost") + ".")
        return ""

    def commitment(self, c, m=None, title=None):
        """A commitment starts, ends or changes. title: the catalogue's title that came with a start this week (role_info),
        told in the same line."""
        line = self._commitment(c, m, title)
        if title and c["what"] == "start" and c["kind"] != "career" and not (
                c["kind"] == "children" and title["name"] in ("mother or father", "adoptive parent", "foster parent", "stepparent")):
            line += " " + self.fill("{N} is " + self.role_mark(title) + " now.")
        return line

    def _commitment(self, c, m=None, title=None):
        kind, what = c["kind"], c["what"]
        prof = np.asarray(c["profile"], float) if c.get("profile") else None
        top = COLORS[int(np.argmax(prof))] if prof is not None else "W"
        if what == "inherited":
            return self.fill("{N} is raised in " + mk("c", f"faith|{top}|inherited", "the family faith") + ", " + an(FAITH_ADJ[top]) + " one.")
        if what == "start":
            through = c.get("through", "")
            if kind == "career":
                job = (mk("c", f"career|{top}|start", "work") + " as " + self.role_mark(title) if title else
                       mk("c", f"career|{top}|start", CAREER[self.setting].get(through, "work")))
                met = m["ctx"].get("_p_boss") if m else None     # the boss the scene already introduced
                if met is not None:
                    return self.fill("{N} takes up " + job + ".")
                boss = self.new("boss", self.W["new_boss"])
                return self.fill("{N} takes up " + job + ". " + cap(self.W["runs"].format(b=self.say(boss))))
            if kind == "partner":
                p = m["ctx"].get("_p_prospect") if m else None
                if p is None and m is not None and m["ctx"].get("_p_partner") is not None:
                    p = m["ctx"]["_p_partner"]                    # the companion the scene already named
                if p is None:
                    ps = self.alive("companion") + self.alive("prospect")
                    p = ps[-1] if ps else self.new("prospect", "someone called {n}")
                for q in self.alive("partner"):         # whoever was partner before is a former partner now
                    if q is not p:
                        q["role"] = "ex"
                p["role"] = "partner"
                return self.fill("{N} and " + self.say(p) + " make it official: " + mk("c", f"partner|{top}|start", "they are together now") + ".")
            if kind == "children" and title and title["name"] in ("adoptive parent", "foster parent", "stepparent"):
                if title["name"] == "stepparent":           # the engine counts the partner's child among theirs (R15)
                    ch = self.new("child", "a stepchild, {n}"); ch["born"] = True
                    ch["ref"] = "their stepchild " + ch["name"]
                    return self.fill("{N} becomes " + self.role_mark(title) + ": a partner's child, " + self.nm(ch) + ", is part of their life now.")
                ch = self.new("child", "a child, {n}" if title["name"] == "adoptive parent" else "a foster child, {n}")
                ch["ref"] = "their child " + ch["name"]
                if title["name"] == "adoptive parent":
                    return self.fill("{N} adopts " + self.nm(ch) + ": " + self.role_mark(title) + " now.")
                return self.fill("{N} takes in " + self.nm(ch) + ", a child who needs a home: " + self.role_mark(title) + " now.")
            if kind == "children" and self.one_roll and TAKEN_IN.search(through or ""):   # F7: an act that takes a
                ch = self.new("child", "a child, {n}"); ch["born"] = True              # child in is not a birth
                ch["ref"] = "their child " + ch["name"]
                return self.fill("{N} takes in " + self.nm(ch) + ", a child who needs a home.")
            if kind == "children":
                first = not self.alive("child")
                fresh = [q for q in self.alive("child") if not q.get("born") and getattr(self, "age", 0) - q.get("made", -99) < 0.1]
                if fresh:                               # a scene this week already held the newborn: the same child
                    ch = fresh[-1]; ch["born"] = True; first = len(self.alive("child")) == 1
                    return self.fill(("{N}'s first child is born: " if first else "Another child is born to {N}: ") + self.nm(ch) + ".")
                ch = self.new("child", "a child, {n}"); ch["born"] = True
                line = ("{N}'s first child is born: " if first else "Another child is born to {N}: ") + self.nm(ch) + "."
                ch["ref"] = "their child " + ch["name"]
                if through == "raise a big family":
                    more = [self.new("child", "their child {n}") for _ in range(2)]
                    for x in more:
                        x["introduced"] = True
                    line += " Then come " + self.nm(more[0]) + " and " + self.nm(more[1]) + "."
                return self.fill(line)
            by = "" if title and through == title["name"] else ", by choosing to " + act(through)    # a title that came in time
            if kind == "faith":
                if title and title["name"] in CAUSES:  # the engine's faith place also holds causes (the catalogue's campaigners)
                    return self.fill("{N} takes up " + mk("c", f"faith|{top}|start", "a cause") + by + ".")
                return self.fill("{N} takes up " + mk("c", f"faith|{top}|start", "a faith, " + an(FAITH_ADJ[top]) + " one") + by + ".")
            if kind == "community":
                return self.fill("{N} becomes part of " + mk("c", f"community|{top}|start", "a community in the {place}") + by + ".")
            return self.fill("{N} takes on a " + kind + ".")
        if what == "left":
            if kind == "partner":
                ps = self.alive("partner")
                if ps:
                    ps[0]["role"] = "ex"
                    return self.fill("{N} and " + self.nm(ps[0]) + " part ways.")
                return ""                               # already apart in the story: nothing to tell
            if kind == "career":
                for b in self.alive("boss"):
                    b["role"] = "former boss"
                return self.fill(self.pick([("R", "{N} walks out of their {job}, and does not look back."), ("", "{N} quits their {job}."),
                                            ("U", "{N} leaves their {job}, having learned what it had to teach.")]), ctx=dict(job=self.W["job"]))
            if kind == "faith":
                if c.get("drifted"):                    # no decision was made: it stopped mattering (the engine's drifted flag)
                    return self.fill(self.pick([("", "Somewhere along the way, what {N} believed in stops mattering to them."),
                                                ("U", "{N} stops believing without ever deciding to; the questions simply won."),
                                                ("R", "{N} stops showing up, and one day notices the belief is gone.")]))
                return self.fill("{N} leaves the faith.")
            if kind == "community":
                return self.fill("{N} drifts away from their community.")
            return self.fill("{N} walks away from their " + kind + ".")
        if what == "lost job":
            bs = self.alive("boss")
            for b in bs:
                b["role"] = "former boss"
            job_ = self.world_word("job", self.W["job"])   # F12 (world_hold): a place in the work in the clan
            return self.fill("{N} loses their " + mk("c", "career||lost job", job_) + "." + (f" {self.nm(bs[0])} does not meet their eye." if bs else ""))
        if what == "moved" and kind == "career":        # v22.5 job_move: the same work, another employer (S7: titles go along)
            job_ = mk("c", f"career|{top}|changed employer", self.world_word("job", self.W["job"]))
            return self.fill(self.pick([("", "{N} changes employer, and takes their " + job_ + " with them."),
                                        ("B", "{N} moves to an employer who pays better for the same " + job_ + "."),
                                        ("R", "{N} has had enough of the place, and takes their " + job_ + " somewhere new."),
                                        ("W", "{N} goes to work for another employer, doing the same " + job_ + " as before.")]))
        if what == "retired":
            return self.fill(self.pick([("", "{N} retires."), ("G", "{N} retires, and the days grow slower and wider."),
                                        ("B", "{N} retires, reluctantly, still counting what they are owed.")]))
        if what == "widowed":
            ps = self.alive("partner")
            if ps:
                self.dies(ps[0])
                return self.fill(self.nm(ps[0]) + " dies. {N} is " + mk("c", "partner||widowed", "widowed") + ".")
            gone = [p for p in self.people if p["role"] == "partner" and not p["alive"]]
            if gone and gone[-1]["name"] in self._told_dead:
                return self.fill("{N} is " + mk("c", "partner||widowed", "widowed") + ".")
            if gone:
                return self.fill(self.nm(gone[-1]) + " dies. {N} is " + mk("c", "partner||widowed", "widowed") + ".")
            return self.fill("{N}'s partner dies.")
        if what == "broke up" and kind == "partner":
            ps = self.alive("partner")
            if ps:
                ps[0]["role"] = "ex"
                return self.fill(self.pick([("", "{N} and {p} break up."), ("R", "{N} and {p} break up, loudly, and for good."),
                                            ("W", "{N} and {p} end it, as decently as they can."),
                                            ("G", "{N} and {p} let it go; whatever grew between them has run its course.")]),
                                 ctx=dict(p=self.nm(ps[0])))
            return ""
        if what == "outgrew it":                   # a title the person is too old for (a scout at nineteen): its own line tells it
            return ""
        return self.fill("{N} leaves their " + ("family years" if kind == "children" else kind) + " behind.")

    def clash(self, c):
        how = CLASH_HOW.get(c["how"], "it ends")
        return self.fill("The long quarrel between {N} and their own " + c["kind"] + " is over: " + how + ".")

    def rite(self, r, sit=None):
        to = r["to"]
        if r.get("quiet"):
            return mk("R", to, self.fill(RITE_QUIET.get(to, "{N} grows older.")))
        what = SNOUN.get(sit, "it")
        return mk("R", to, self.fill(self.pick(RITE.get(to, ["{N} grows older."])), ctx=dict(what=what, what_cap=cap(what))))

    def conversion(self, c):
        tow = np.asarray(c["toward"], float)
        new = COLORS[int(np.argmax(tow))]
        old = c["disowned"]
        return self.fill(mk("C", f"{old}|{new}", "Something gives way.") + " {N} loses faith in " + self.val(old) + ", and turns toward "
                         + self.val(new) + ". " + self.thought(self.pick(REASON[new]), "reason", new))

    def breakthrough(self, b):
        want = np.asarray(b["want"], float) - np.asarray(b["before"], float)
        new = COLORS[int(np.argmax(want))]
        age = float(b["age"]); last = self._broke
        self._broke = age
        if last is not None and age - last < 1.0:
            return None
        if last is not None and age - last < 4.0:
            return mk("B", new, self.fill(self.pick(["Once again {N} gives in to what they keep holding back: {v}.",
                                                   "The old wanting breaks through again: {v}."]), ctx=dict(v=self.val(new))))
        fresh = ("With a round birthday ahead, it feels like now or never. " if int(age) % 10 == 9 else
                 "New surroundings make it easier. " if self._moved_at is not None and age - self._moved_at < 1.0 else "")
        return self.fill(fresh + mk("B", new, "What {N} has held back for years breaks through.") + " They turn toward " + self.val(new) + ".")
