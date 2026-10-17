"""Story's methods for goals, dreams and plans, needs, hindsight, resolutions, the yearly chapter and the epitaph.

Part of class Story (story.py), which inherits GoalsMixin; moved out of story.py verbatim. A method here
reads module names through the imports below, the same objects story.py has, and self for everything on the Story."""
import numpy as np
import re
from story_base import (ADJ, CI, COLORS, DREAM_AGAIN, DREAM_FROM, DREAM_NEW, DREAM_SAY, EPITAPH, GOAL_C, GOAL_D,
    GOAL_END, HINDSIGHT, HORIZON_WORD, LIFE_END, LIFE_FROM, MOOD, NAMED_END, NAMED_SHORT, NEED_SAY, NOUN, PLAN_FROM,
    SHIFT, SURPRISE, TRIGGER, WEEKS, cap, dream_catalogue, dream_of, mk, phase, their)


class GoalsMixin:
    def temperament(self, moved, keys=()):
        return self.fill(self.pick(["People who know {N} say they have become {m}.", "Over the years {N} has become {m}."]),
                         ctx=dict(m=mk("T", ",".join(keys), ", and ".join(moved))))

    # ---------------------------------------------------------------- v7: dreams, passions and plans
    def goal_words(self, kind, domain, mix, gid=0):
        """What a goal is about: (as a dream, as a passion, as a plan's verb). The id keeps the same words for one goal;
        a dream the engine named from the Library's catalogue keeps its own words."""
        info = self.dreams.get(int(gid))
        if info:
            g_d = dream_of(info["name"], info.get("domain", ""))
            fb = self._generic_goal_words(domain, mix, gid)
            return g_d, their(info["passion"]) if info.get("passion") else fb[1], their(info["plan"]) if info.get("plan") else fb[2]
        return self._generic_goal_words(domain, mix, gid)

    def _generic_goal_words(self, domain, mix, gid=0):
        if domain in GOAL_D:
            return GOAL_D[domain]
        v = np.asarray(mix, float)
        c = COLORS[int(np.argmax(v))]
        g, verb = GOAL_C[c][int(gid) % len(GOAL_C[c])]
        return g, g, verb

    def life_words(self, gid):
        """A named dream's life-goal phrase ("a whole career keeping one town safe"), or None."""
        info = self.dreams.get(int(gid))
        return their(info["life"]) if info and info.get("life") else None

    def dream_info(self, rec):
        """The dream behind a goal record: the engine's names (name, passion, plan, life; flat on the record or under
        "dream"), completed from the Library's catalogue, kept by the goal's id for the HUD and the inner voice."""
        gid = int(rec.get("id", 0))
        d = rec["dream"] if isinstance(rec.get("dream"), dict) else rec
        name = next((d[k] for k in ("name", "dream") if isinstance(d.get(k), str) and d[k]), None)
        if name is None:
            return self.dreams.get(gid)
        cat = dream_catalogue()["by_name"].get(name, {})
        def f(*keys):
            for k in keys:
                if isinstance(d.get(k), str) and d[k]:
                    return d[k]
            return cat.get(keys[0]) if isinstance(cat.get(keys[0]), str) else None
        info = dict(name=name, domain=cat.get("domain") or (d.get("domain") if isinstance(d.get("domain"), str) else ""),
                    passion=f("passion"), plan=f("plan"), life=f("life", "life_goal", "life_phrase"))
        self.dreams[gid] = info
        return info

    def spark_say(self, rec):
        """The spark's narration line (the Library's say, with {N}), from the record or the catalogue."""
        d = rec["dream"] if isinstance(rec.get("dream"), dict) else rec
        say = d.get("say") if isinstance(d.get("say"), str) else rec.get("say") if isinstance(rec.get("say"), str) else None
        return say or dream_catalogue()["say"].get(self.setting, {}).get(rec.get("trigger", ""))

    def goal(self, rec):
        """A dream, passion or plan begins, turns into another, comes true or ends (engine v7 goal records)."""
        kind, what, src = rec["kind"], rec["what"], rec.get("source", "")
        info = self.dream_info(rec)
        if kind == "dream" and what != "begins":                           # no longer a dream: let go, pushed aside, a passion or a plan
            self.dreams_held.pop(int(rec.get("id", 0)), None)
        g_d, g_p, verb = self.goal_words(kind, rec.get("domain", ""), rec.get("mix", (0.2,) * 5), rec.get("id", 0))
        life = self.life_words(rec.get("id", 0)) if info else None
        hz = HORIZON_WORD.get(rec.get("horizon", ""), "")
        cols = "".join(c for c, x in zip(COLORS, rec.get("mix", ())) if x >= 0.24) or COLORS[int(np.argmax(rec.get("mix", (0.2,) * 5)))]
        ctx = dict(g=g_p if kind == "passion" else g_d, v=verb, h=hz, p=g_p, l=life or "")
        line = None
        if what == "begins" and kind == "dream":
            say = self.spark_say(rec) if info else None
            tr = TRIGGER.get(rec.get("trigger", ""))
            if say:                                     # the spark as the Library tells it, then the dream it left
                ctx["S"] = self.fill(say)
                again = info["name"] in {v for k, v in self.dreams_held.items() if k != int(rec.get("id", 0))}
                line = self.pick(DREAM_AGAIN if again else DREAM_SAY)
            elif tr:
                raw = tr[("earth", "tribal", "magic").index(self.setting)]
                ctx["T"] = self.fill(raw)
                lead = re.match(r"^((?:⟦[^⟧]*⟧)*)(Their|The|A|An|Someone|Watching) ", ctx["T"])
                if lead:                                # mid-sentence it stays lower case: "After their teacher Hester, ..."
                    ctx["T"] = lead.group(1) + lead.group(2).lower() + ctx["T"][lead.end(2):]
                line = self.pick(DREAM_FROM)
            else:
                line = self.pick(DREAM_NEW)
        elif what == "begins" and kind == "plan" and src != "dream":
            line = LIFE_FROM.get(src, LIFE_FROM[""]) if life and rec.get("horizon") == "life" else PLAN_FROM.get(src, PLAN_FROM[""])
        elif life and kind == "plan" and rec.get("horizon") == "life" and what in LIFE_END:
            line = LIFE_END[what]
        elif info and (kind, what) in NAMED_END:
            long_ = "," in g_d or len(g_d.split()) > 7
            line = self.pick((NAMED_SHORT if long_ and (kind, what) in NAMED_SHORT else NAMED_END)[(kind, what)])
        elif (kind, what) in GOAL_END:
            line = self.pick(GOAL_END[(kind, what)])
        if not line:
            return None
        if not hz:
            line = line.replace(" {h}", "")
        elif info:                                      # a named plan is a long phrase: the deadline after a comma
            line = line.replace(" {h}", ", {h}")
        if kind == "dream" and what == "begins" and info:
            self.dreams_held[int(rec.get("id", 0))] = info["name"]
        pay = f"{kind}|{what}|{cols}|{rec.get('domain', '')}|{src}|{rec.get('horizon', '')}"
        return mk("g", pay, self.fill(line, ctx=ctx))

    def name_goal(self, text, kind, domain, mix, gid, horizon=""):
        """The engine's default name for a goal ("the plan (B W)") in the story's words, for the inner voice and lessons."""
        g_d, g_p, verb = self.goal_words(kind, domain, mix, gid)
        life = self.life_words(gid) if kind == "plan" and horizon == "life" else None
        if life:
            return f"their life goal, {life}"
        return {"dream": f"the dream of {g_d}", "passion": f"the passion for {g_p}"}.get(kind, f"the plan to {verb}")

    # ---------------------------------------------------------------- v7: the inner voice before a choice, what came of it after
    def insight(self, key, line, heart_driver, head_driver, self_control):
        return mk("i", f"{key}|{heart_driver}|{head_driver}|{self_control:.2f}", self.fill(line))

    def aside(self, key, line):
        return mk("j", key, self.fill(line))

    def needs_line(self, needs):
        """The needs a choice's week moved, as one line (IDEAS.md, "Make needs visible"); empty when none moved."""
        if not needs:
            return ""
        bits = [f"{NEED_SAY.get(x['need'], x['need'])} {x['before'] * 100:.0f}% → {x['after'] * 100:.0f}%" for x in needs[:4]]
        return "Needs: " + ", ".join(bits) + "."

    def _hrng(self):
        """Its own random stream, so lives without pushes are told exactly as before."""
        if getattr(self, "_hr", None) is None:
            self._hr = np.random.default_rng(int(self.seed) + 9177)
        return self._hr

    def hindsight(self, kind, need, worked):
        """How the character judges a push, looking back (IDEAS.md, "Player intervention that helps")."""
        if kind == "accepted":
            return self.fill(self._hrng().choice(HINDSIGHT["accepted"]).replace("{need}", need or "what was missing"))
        if kind == "resented":
            return self.fill(self._hrng().choice(HINDSIGHT["resented_fail" if not worked else "resented_empty"]))
        return ""

    def resolution(self, r):
        """What came of a choice, as the terminal tells it (the browser draws the same dict as a panel)."""
        L = [self.fill(SURPRISE.get((r["worked"], r["surprise"]), "It is done."))]
        if r.get("pushed"):
            L.append(self.fill("You pushed {N} into it" + (", against everything in them." if not (r["with_heart"] or r["with_head"]) else
                                                          ", the way the head said." if r["with_head"] else ", the way the heart wanted.")))
        elif r.get("with_heart") and r.get("with_head"):
            L.append(self.fill("{N} followed both heart and head."))
        elif r.get("with_heart"):
            L.append(self.fill("{N} followed the heart over the head."))
        elif r.get("with_head"):
            L.append(self.fill("{N} followed the head over the heart."))
        elif "with_heart" in r:
            L.append(self.fill("{N} went a third way, neither the heart's first choice nor the head's."))
        if r.get("regret"):
            L.append(self.fill("It will be regretted: the heart won against the head, and lost."))
        bec = [mk("z", f"{c['what']}|{c['delta']}|{c['size']}", c["word"]) for c in r.get("became", [])]
        if bec:
            L.append(self.fill("{N} is " + (", ".join(bec[:-1]) + " and " + bec[-1] if len(bec) > 1 else bec[0]) + " now."))
        gained = [x["word"] for x in r.get("states", []) if x["what"] == "gained"]
        lost = [x["word"] for x in r.get("states", []) if x["what"] != "gained"]
        join = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
        if gained:
            L.append(self.fill("{N} is " + join(gained) + " now."))
        if lost:
            L.append(self.fill("{N} is no longer " + join(lost) + "."))
        cl = r.get("closer")
        if cl:
            L.append(mk("y", f"{cl['identity']}|{cl['guild']}|{cl['distance']}",
                        self.fill(("A step closer to becoming " if cl["distance"] < 0.05 else "Slowly moving toward ") + cl["guild"] + ".")))
        for les in r.get("lessons", [])[:2]:
            L.append(mk("n", les["key"], self.fill(les["line"])))
        return "\n".join(L)

    # ---------------------------------------------------------------- the yearly chapter
    def chapter(self, age, stage, w, content, peace, ident="", times=None):
        """The head of a new year: how life feels, what drives them, and where the ordinary weeks went. times: (marker
        payload, clause), how the times touched them as one clause of the mood's sentence (the game's lines_tied, item 6)."""
        w = np.asarray(w, float)
        stage = phase(age)
        band = ("h" if content >= 0.62 else "l" if content <= 0.30 else "m") + ("h" if peace >= 0.67 else "l" if peace <= 0.47 else "m")
        band = band if band in MOOD else "mm"
        L = [mk("m", f"{content:.2f}|{peace:.2f}", self.fill(self.pick(MOOD[band], stage), stage))]
        if times:                                    # item 6: "...; lean times: prices outran their money."
            mood = L[0][:-len("⟦/⟧")]
            L[0] = (mood[:-1] + "⟦/⟧; " + mk("X", times[0], times[1]) + "." if mood.endswith(".") else
                    L[0] + " " + mk("X", times[0], cap(times[1])) + ".")
        if self._last_c is not None and abs(content - self._last_c) > 0.15 and band != "mm":
            L.append(mk("d", f"{content - self._last_c:+.2f}", "Better than last year." if content > self._last_c else "Worse than last year."))
        self._last_c = content
        # a slow shift in emphasis, told once it has really happened
        top = COLORS[int(np.argmax(self.voice))]
        if (self._voice_top is not None and top != self._voice_top and self.voice[CI[top]] - self.voice[CI[self._voice_top]] > 0.025
                and age - self._shift_age >= 3):
            o = self._voice_top
            L.append(mk("s", f"{o}|{top}", self.fill(self.pick(SHIFT), ctx=dict(old=NOUN[o], new=NOUN[top], old_adj=ADJ[o], new_adj=ADJ[top]))))
            self._voice_top = top; self._shift_age = age
        elif self._voice_top is None and age >= 6:
            self._voice_top = top
        lead = tuple(self.leading())
        if age >= 6 and (lead[0] != self._values_told[0] or age - self._values_told[1] >= 6):
            self._values_told = (lead[0], age)
            s = "What drives {N} now is " + self.val(lead[0])
            s += (", and after that, " + self.val(lead[1]) + "." if len(lead) > 1 else ".")
            L.append(self.fill(s))
        wk = self.year["weeks"]
        if wk.sum() >= 3:
            c = COLORS[int(np.argmax(wk))]
            if c != self._weeks_told[0] or age - self._weeks_told[1] >= 3:      # told when it changes, or now and then
                self._weeks_told = (c, age)
                L.append(mk("k", c + "|" + ",".join(f"{x:.0f}" for x in wk), self.fill(self.pick([(c, x[0], x[1]) for x in WEEKS[c]], stage), stage)))
        if self.year["frictions"] >= 2:
            L.append(mk("f", self.year["frictions"], "Small frictions pile up all year."))
        self.last_weeks = [round(float(x), 1) for x in self.year["weeks"]]
        self.year = dict(weeks=np.zeros(5), frictions=0)
        head = f"── Age {int(round(age))}" + (f" · {ident}" if ident else "") + " ──"
        return head + "\n" + " ".join(L)

    def epitaph(self, w):
        lead = self.leading(np.asarray(w, float) * 0.5 + self.voice * 0.5)
        s = "Here the story of {N} ends. They are remembered as someone who " + mk("v", lead[0], EPITAPH[lead[0]])
        s += (", and " + mk("v", lead[1], EPITAPH[lead[1]]) + "." if len(lead) > 1 else ".")
        return self.fill(s)
