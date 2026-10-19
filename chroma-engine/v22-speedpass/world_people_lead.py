"""People's methods for ways to lead (S7), who slots, and place and moving.

Part of class People (world_people.py), which inherits LeadMixin; moved out of world_people.py verbatim. A method here
reads module names through the imports below, the same objects world_people.py has, and self for everything on the
People."""
import numpy as np
from library import COLORS
from world_keys import FEATURES, GROUP_KINDS, HAUNT_KINDS, INST_KINDS, LEAD_WAYS, SPHERES
from world_people_base import (BIT, C, G, HEA, KINMASK, LEAD_BIT, LEAD_DEFAULT, LEAD_KINDS, LEAD_OWNED, LEAD_TITLES,
    LOCAL_KINDS, MON, NEVER, R, _uclip)


class LeadMixin:
    # ------------------------------------------------------------------ S7, ways to lead (lead_ways)
    # chroma-ideas/social-mechanics.md S7, "The leader's time in post" first: a post per leading role a life holds (it
    # leads one of its settings, kind "setting", or one held at a named place, "place", or holds an office title,
    # LEAD_TITLES, kind "office"). Each post keeps its start, its way (rules W, knowing best U, favours owed B, inspiring R, custom G)
    # and its legitimacy (the fit of the way's colour to the led place's faces through the place reading, scaled 0..1,
    # less the falls' steps). Its time in post is the Outer world's (dynamics.json lead_posts, by post kind and epoch: a
    # term renewed with chance min(.95, renew x (.5 + legitimacy)) up to max_terms, a yearly end chance, an age out;
    # health under .35 ends it; national offices keep the world's own elections). It also ends at a move, when a rival
    # of higher rung takes over, or by a fall (legitimacy under .2), each told as an event and, where the Library has
    # them, a moment (cast_want lead_take, lead_crisis, lead_fall, lead_routine, lead_hand; fired with no holder, cid -1).
    def _lead_init(self):
        import sphere_data as SD
        wp_ = getattr(self.W, "p", None) or {}
        self.lw_par = {**LEAD_DEFAULT, **dict(wp_.get("lead_par") or {})}
        tb = SD.PLACE_READING
        T = np.array([[float(tb[COLORS[f_]][COLORS[c_]]) for c_ in range(C)] for f_ in range(C)])   # face x act colour
        self._lw_T = T[self.perm][:, self.perm]          # in this world's frame
        LP = SD.LEAD_POSTS
        self._lw_kinds = LP["kinds"]
        self._lw_hk = {h_: k_ for k_, v_ in LP["kinds"].items() for h_ in v_["haunts"]}   # a place's post kind by haunt kind
        self._lw_gk = {g_: k_ for k_, v_ in LP["kinds"].items() for g_ in v_["groups"]}   # a setting's by group kind
        self._lw_fast = np.array([LP["fast_line"][sp_] for sp_ in SPHERES])
        self._lw_hist = []        # the town spheres' face mixes the last five quarters (custom's fast change: 4 quarters)
        self._lw_need = float(SD.DEEP["money"]["need_line"])   # favours: money under the need line
        self._lw_ev_i = len(getattr(self.W, "sph_ev_log", ()))   # the crises: the sphere events read so far
        self.lw_posts = []        # the posts held now: dicts (see _lead_new)
        self.lw_ended = []        # the posts that ended, oldest first
        self.lw_due = []          # [life, moment key, post id, week queued]: a post's moment waiting to come
        self.lw_lost = []         # [life, office index, why]: an office title the engine takes away (a fall, a term)
        self.lw_keys = set()      # the lead moment keys the batch has (WorldLink sets it); none: no moment is waited for
        self.lw_tnames = list(LEAD_TITLES)
        self.lw_has = np.zeros((self.N, len(LEAD_TITLES)), bool)    # the leading titles held (the engine's, each week)
        self.lead_sh = np.zeros((self.N, C))                       # the shadow target years in one way add (with shadows)
        self._lw_next = 0; self._lw_q = -1; self._lw_back = {}
        self._lw_rng = np.random.default_rng([self.seed, 97, self.run_seed])   # the posts' own dice

    def _lead_cell(self, pk):
        """The time in post of post kind pk in this world's epoch (form, term_q, renew, max_terms, end_y, age_out), None
        where the kind has no post then. A national office keeps the world's own elections (no term, no end chance of
        S7's); where there are none, it is held at the ruler's pleasure (end_y .1)."""
        if pk == "national":
            el_ = float(getattr(self.W, "regime", 0.0)) >= 0
            return dict(form="chosen" if el_ else "appointed", term_q=None, renew=None, max_terms=None,
                        end_y=0.0 if el_ else self.lw_par["ruler_end"], age_out=None)
        return self._lw_kinds[pk]["by"].get(getattr(self.W, "sph_epoch", "modern"))

    def _lead_kind(self, n, kind, slot, place):
        """The post kind (lead_posts) of a setting led (by the haunt kind of its place, else its group kind) or an office."""
        if kind == "office":
            tn_ = self.lw_tnames[slot]
            return LEAD_OWNED[tn_] if self.lw_par["owner_kind"] and tn_ in LEAD_OWNED else LEAD_TITLES[tn_][0]
        if kind == "place":
            return self._lw_hk.get(HAUNT_KINDS[(int(place) // self.W.hp_s.shape[2]) % len(HAUNT_KINDS)])
        return self._lw_gk.get(GROUP_KINDS[int(self.skind[n, slot])])

    def _lead_left(self, p, t):
        """Quarters left in post (phase 4's fund span for a leader): the term's rest, else the next vote for a national
        office, else the expected time to its yearly end chance; never past the age out; at least 1."""
        c_ = self._lead_cell(p["pk"]) or {}
        if c_.get("term_q"):
            q_ = c_["term_q"] - (t - p["term_t0"]) // 13
        elif p["pk"] == "national" and float(getattr(self.W, "regime", 0.0)) >= 0:
            q_ = int(getattr(self.W, "next_vote", 16))
        else:
            q_ = 4.0 / c_["end_y"] if c_.get("end_y") else 80
        if c_.get("age_out"):
            q_ = min(q_, 4 * (c_["age_out"] - self._age(t)))
        return max(1, int(q_))

    def _lead_renew(self, p, t):
        """A term's end: handed over after max_terms in a row, else renewed with chance min(.95, renew x (.5 +
        legitimacy)), else it ends."""
        c_ = self._lead_cell(p["pk"]) or {}
        p["terms"] += 1
        if c_.get("max_terms") and p["terms"] >= c_["max_terms"]:
            self._lead_end(p, t, "term limit")
        elif self._lw_rng.random() < min(0.95, float(c_.get("renew") or 0.0) * (0.5 + p["legit"])):
            p["term_t0"] = int(t)
            self._lead_ev(p, t, "renewed", terms=p["terms"])
        else:
            self._lead_end(p, t, "term")

    def _lead_faces(self, p):
        """The led place's faces (this world's frame): the named place, the setting's ways, or the town's sphere."""
        W = self.W; n = p["n"]
        if p["kind"] == "office" and p.get("gslot", -1) >= 0:   # a leading title over a setting the life is still in
            g_ = p["gslot"]
            if self.skind[n, g_] >= 0 and int(self.sjoin[n, g_]) == p["gjoin"]:
                if p["place"] >= 0 and getattr(W, "hp_s", None) is not None and int(self.shnt[n, g_]) == p["place"]:
                    return np.asarray(W.hp_s.reshape(-1, C)[p["place"]], float)
                return np.asarray(self.snorm[n, g_], float)
        if p["kind"] == "place" and getattr(W, "hp_s", None) is not None:
            return np.asarray(W.hp_s.reshape(-1, C)[p["place"]], float)
        if p["kind"] in ("place", "setting"):
            return np.asarray(self.snorm[n, p["slot"]], float)
        if getattr(W, "sph_s", None) is not None:
            return np.asarray(W.sph_s[p["loc"], p["sphere"]], float)
        return np.full(C, 1.0 / C)

    def _lead_fit(self, p):
        """The fit of the post's way to the led place: the place's reading of the way's colour (own +1, ally +.4,
        enemy -.4, dynamics.json place_reading), from -.4..1 to 0..1."""
        r = float(self._lead_faces(p) @ self._lw_T[:, int(self.iperm[p["way"]])])
        return (r + 0.4) / 1.4

    def _lead_legit(self, p):
        p["legit"] = float(min(max(self._lead_fit(p) + p["dent"], 0.0), 1.0))
        return p["legit"]

    def _lead_post(self, n, j):
        """Life n's post in sphere j (the most legitimate, when several), else None."""
        best = None
        for p in self.lw_posts:
            if p["n"] == n and p["sphere"] == j and (best is None or p["legit"] > best["legit"]):
                best = p
        return best

    def _lead_ev(self, p, t, state, **kw):
        if self.watch[p["n"]]:
            self.events.append(dict(n=int(p["n"]), t=int(t), kind="lead", state=state, post=p["kind"],
                                    sphere=SPHERES[p["sphere"]], way=LEAD_WAYS[p["way"]], legit=round(p["legit"], 3), **kw))

    def _lead_queue(self, p, key, t):
        """A post's moment waits to come (only when the batch has moments of that key)."""
        if key in self.lw_keys and not any(d_[2] == p["id"] and d_[1] == key for d_ in self.lw_due):
            self.lw_due.append([int(p["n"]), key, int(p["id"]), int(t)])
            return True
        return False

    def _lead_new(self, n, kind, j, slot, place, t, gslot=-1):
        """A post begins: the character picks the way of its lead colour (a lead_take moment can change it). gslot: the
        setting a leading title leads (-1 none)."""
        pk = self._lead_kind(n, kind, slot, place)
        if pk is None or self._lead_cell(pk) is None:   # no such post in this epoch
            return None
        c = int(self.perm[int(np.argmax(self.w[n]))])
        p = dict(id=self._lw_next, n=int(n), kind=kind, pk=pk, terms=0, sphere=int(j), slot=int(slot), place=int(place),
                 loc=int(self.loc[n]), t0=int(t), term_t0=int(t), way=c, col=c, way_t=int(t), succ_t=int(t), fade_t=int(t),
                 fades=0, dent=0.0, legit=0.0, join=int(self.sjoin[n, slot]) if kind != "office" else -1, fair_lo=False,
                 money_yr=-1, falls=[], fought=0, end_t=None, why=None, gslot=int(gslot),
                 gjoin=int(self.sjoin[n, gslot]) if gslot >= 0 else -1)
        self._lw_next += 1
        self._lead_legit(p)
        self.lw_posts.append(p)
        self._lead_ev(p, t, "took", title=self.lw_tnames[slot] if kind == "office" else None)
        self._lead_queue(p, "lead_take", t)
        return p

    def _lead_end(self, p, t, why):
        """A post ends: a setting's lead goes to its most standing member; an office S7 ended (a fall, a term, a
        hand-over, a move...) is taken from the engine's titles, and a favours leader's other posts lose what the office
        paid for."""
        if p not in self.lw_posts:
            return
        self.lw_posts.remove(p)
        p["end_t"] = int(t); p["why"] = why
        self.lw_ended.append(p)
        self.lw_due = [d_ for d_ in self.lw_due if d_[2] != p["id"]]
        n = p["n"]
        if p["kind"] != "office" and self.slead[n, p["slot"]] == -2 and why != "rival":
            self.slead[n, p["slot"]] = -1   # handed to the most standing member (no dice), else left for the members' turn
            if self.skind[n, p["slot"]] >= 0:
                mem = np.nonzero((self._bits()[n, :, p["slot"]] > 0) & self.lv[n])[0]
                if len(mem):
                    k = int(mem[np.argmax(self.stand[n, mem])])
                    self.slead[n, p["slot"]] = k; self.rmask[n, k] |= LEAD_BIT[int(self.skind[n, p["slot"]])]
        if p["kind"] == "office":
            if why not in ("died", "office ended"):   # S7 ended it: the engine takes the title (a fall, a term, a move)
                self.lw_lost.append([int(n), int(p["slot"]), why])
            if why != "died":   # favours owed: the office that paid them has ended
                for q_ in [q_ for q_ in self.lw_posts if q_["n"] == n and q_["way"] == 2]:
                    self._lead_step(q_, t, "favours", why="the office ended")
        self._lead_ev(p, t, "ended", why=why, years=round((t - p["t0"]) / 52.0, 2))

    def _lead_crises(self):
        """The crises since the last quarter: the sphere events fired (World.sph_ev_log), counted per (town, the event's
        sphere); town -1: an event of the whole society, a crisis in every town."""
        log = getattr(self.W, "sph_ev_log", None); out = {}
        if log is None or len(log) <= self._lw_ev_i:
            return out
        rows = np.asarray(log[self._lw_ev_i:]).tolist(); self._lw_ev_i = len(log)
        sph = self.W._sph_ev_tables()["sph"]
        for _, i_, l_ in rows:
            k_ = (int(l_), int(sph[int(i_)]))
            out[k_] = out.get(k_, 0) + 1
        return out

    def _lead_step(self, p, t, key, why=None):
        """A fall's step in legitimacy (lead_par step, the same for every way); the crisis of the way waits to come
        (lead_crisis), or the turn to routine for a fading inspiring leader; under the fall line, the fall."""
        if p not in self.lw_posts:
            return
        size = self.lw_par["step"]
        p["dent"] -= size; p["falls"].append([int(t), int(p["way"]), key])
        self._lead_legit(p)
        self._lead_ev(p, t, "step", key=key, why=why, size=size)
        if p["legit"] < self.lw_par["fall"]:
            self._lead_fall(p, t)
        elif key == "inspiring" and p["fades"] >= self.lw_par["routine"] and "lead_routine" in self.lw_keys:
            self._lead_queue(p, "lead_routine", t)
        else:
            self._lead_queue(p, "lead_crisis", t)

    def _lead_fall(self, p, t):
        """Legitimacy under the fall line: the fall moment (go, fight, again), else the post ends; a post that has
        fought off a fall gets no second fight: its next fall ends it."""
        if any(d_[2] == p["id"] and d_[1] == "lead_fall" for d_ in self.lw_due):
            return
        self.lw_due = [d_ for d_ in self.lw_due if d_[2] != p["id"]]   # the fall comes before any crisis
        self._lead_ev(p, t, "falling")
        if p.get("fought") or not self._lead_queue(p, "lead_fall", t):
            self._lead_end(p, t, "fell")

    def _lead_act(self, p, lv, q, t):
        """A leader's lever act in the sphere they lead (phase 4's levers): a success keeps an inspiring leader's spark
        (no fade for a year); a visible failure is knowing best's mistake; a favour (subvert) touching the leader is a
        rules leader's scandal."""
        if q >= 0.5:
            p["succ_t"] = int(t); p["fades"] = 0
        if p["way"] == 1 and q < 0.5:
            self._lead_step(p, t, "knowing", why="a failed lead act")
        elif p["way"] == 0 and lv == "subvert":
            self._lead_step(p, t, "rules", why="a favour")

    def _lead_vacant(self, n, j, k, t):
        """A setting's leader left or died (the members' most standing one, k, would follow): with lead_ways the
        character takes the lead instead when the setting's kind can be led (LEAD_KINDS), they are of age, and they
        stand higher: their rung in the setting's sphere (a regular 1, a known face 2, a pillar 3) above k's (1 +
        standing). True when they took it."""
        if (GROUP_KINDS[int(self.skind[n, j])] not in LEAD_KINDS or self.dead[n] or self._age(t) < self.lw_par["take_age"]
                or not hasattr(self, "rung")):
            return False
        sj = int(self.set_sphere[n, j])
        if sj < 0 or int(np.floor(self.rung[n, sj])) <= 1 + int(self.stand[n, k]):
            return False
        pl_ = int(self.shnt[n, j]) if getattr(self.W, "hp_s", None) is not None else -1
        if self._lead_new(int(n), "place" if pl_ >= 0 else "setting", sj, int(j), pl_, t) is None:
            return False
        self.slead[n, j] = -2
        return True

    def _lead_q(self, t):
        """Each quarter: posts end (death, the office or setting gone, a move (a title over a workplace goes with the
        job), frailty, the age out, the yearly end chance, a rival of higher rung, the term's end unrenewed), the
        legitimacy of the rest, the quarter's crises (_lead_crises) and the falls of each way, new posts (a pillar takes
        the lead; an office title), the leaders' mix of each town sphere (World.sph_plead, each post x (.5 +
        legitimacy)) and the shadow target."""
        if self._lw_q == t:
            return
        self._lw_q = t; W = self.W; par = self.lw_par; a = self._age(t)
        if getattr(W, "sph_s", None) is not None:
            self._lw_hist = (self._lw_hist + [np.array(W.sph_s, float)])[-5:]
        # 1. ends
        for p in list(self.lw_posts):
            n = p["n"]; why = None; c_ = self._lead_cell(p["pk"])
            if p["kind"] == "office" and LEAD_TITLES[self.lw_tnames[p["slot"]]][2] == "work":   # a title over a workplace
                p["loc"] = int(self.loc[n])   # goes with the job through a move, as the engine keeps both (v22.4 fix round)
            if self.dead[n]:
                why = "died"
            elif p["kind"] == "office" and not self.lw_has[n, p["slot"]]:
                why = "office ended"
            elif p["kind"] != "office" and (self.skind[n, p["slot"]] < 0 or int(self.sjoin[n, p["slot"]]) != p["join"]):
                why = "left"
            elif int(self.loc[n]) != p["loc"]:
                why = "moved"
            elif c_ is None:
                why = "no such post"
            elif float(self.res[n, HEA]) < par["frail"]:
                why = "frail"
            elif c_.get("age_out") and a >= c_["age_out"]:
                why = "retired"
            elif c_.get("end_y") and self._lw_rng.random() < 1 - (1 - c_["end_y"]) ** 0.25:
                why = "stepped down"
            if why:
                self._lead_end(p, t, why)
        # 2. a rival of higher rung: the setting's most standing member (rung 1 + standing) above 4 x legitimacy
        B = None
        for p in [p_ for p_ in self.lw_posts if p_["kind"] != "office"]:
            if self._lw_rng.random() >= par["rival"]:
                continue
            B = self._bits() if B is None else B
            n = p["n"]; mem = np.nonzero((B[n, :, p["slot"]] > 0) & self.lv[n])[0]
            if not len(mem):
                continue
            k = int(mem[np.argmax(self.stand[n, mem])])
            if 1 + int(self.stand[n, k]) > 4 * p["legit"]:
                self._lead_end(p, t, "rival")
                self.slead[n, p["slot"]] = k
                self.rmask[n, k] |= LEAD_BIT[int(self.skind[n, p["slot"]])]
        # 3. legitimacy and the falls of each way
        fair_ = W.sph_fair_target() if self.lw_posts else None
        tv_ = (0.5 * np.abs(self._lw_hist[-1] - self._lw_hist[0]).sum(-1)) if len(self._lw_hist) == 5 else None
        cr_ = self._lead_crises()
        for p in list(self.lw_posts):
            if p not in self.lw_posts:
                continue
            n = p["n"]; l_, j_ = p["loc"], p["sphere"]
            self._lead_legit(p)
            # the quarter's crises: each sphere event in the sphere led (the town's own, or the whole society's) tests a
            # way at one even chance, crisis: a rules leader fails it rule-bound, a knowing leader is shown wrong, an
            # inspiring leader carries it otherwise (a new success); favours and custom fall by their own roads below
            for _ in range(cr_.get((l_, j_), 0) + cr_.get((-1, j_), 0)):
                w_ = p["way"]
                if p not in self.lw_posts:
                    break
                if w_ in (0, 1) and self._lw_rng.random() < par["crisis"]:
                    self._lead_step(p, t, LEAD_WAYS[w_],
                                    why="rule-bound in a crisis" if w_ == 0 else "shown wrong in a crisis")
                elif w_ == 3 and self._lw_rng.random() >= par["crisis"]:
                    p["succ_t"] = int(t); p["fades"] = 0
            if p not in self.lw_posts:
                continue
            if p["way"] == 0:   # rules: a fairness scandal among the led (their felt fairness falls under the line)
                lo_ = bool(fair_[l_, j_] < par["fair_line"])
                if lo_ and not p["fair_lo"]:
                    self._lead_step(p, t, "rules", why="a fairness scandal")
                p["fair_lo"] = lo_
            elif p["way"] == 2:   # favours: once a year, money under the need line, or (fav_drop) under that share of
                m_ = float(self.res[n, MON])   # its best since leading by favours: less to give than the clients came for
                if par["fav_drop"]:
                    hi_ = p.get("money_hi")
                    p["money_hi"] = [p["way_t"], m_] if hi_ is None or hi_[0] != p["way_t"] else [hi_[0], max(hi_[1], m_)]
                if int(a) != p["money_yr"]:
                    p["money_yr"] = int(a)
                    if m_ < self._lw_need and t > p["t0"]:
                        self._lead_step(p, t, "favours", why="money under need")
                    elif par["fav_drop"] and t > p["t0"] and m_ < par["fav_drop"] * p["money_hi"][1]:
                        self._lead_step(p, t, "favours", why="less to give")
            elif p["way"] == 3:   # inspiring: a year without a new success fades the spark
                if t - p["succ_t"] >= 52 and t - p["fade_t"] >= 52:
                    p["fade_t"] = int(t); p["fades"] += 1
                    self._lead_step(p, t, "inspiring", why="no new success")
            elif p["way"] == 4 and tv_ is not None:   # custom: the town sphere changed fast over the last four quarters
                # (fast_gap: no new custom step within that many weeks of the last, so one stretch of change, read
                # over four quarters, is not counted again each quarter it stays in the window)
                if (tv_[l_, j_] > par["fast_k"] * self._lw_fast[j_]
                        and t - p.get("fast_t", NEVER) >= par["fast_gap"]):
                    p["fast_t"] = int(t)
                    self._lead_step(p, t, "custom", why="fast change")
        # 4. a term's end: handing the post on (lead_hand: chosen, open or stay), else renewed or not
        for p in list(self.lw_posts):
            c_ = self._lead_cell(p["pk"]) or {}
            if p in self.lw_posts and c_.get("term_q") and t - p["term_t0"] >= 13 * c_["term_q"]:
                if not any(d_[2] == p["id"] and d_[1] in ("lead_hand", "lead_fall") for d_ in self.lw_due):
                    if not self._lead_queue(p, "lead_hand", t):
                        self._lead_renew(p, t)
        # 5. new posts: a pillar of a setting with a leader takes the lead (when they stand at least as high as its
        # leader: rung 3 against the leader's 1 + standing), and every office title held is a post
        if a >= par["take_age"]:
            held = {(p["n"], p["kind"] == "office", p["slot"]) for p in self.lw_posts}
            kinds = np.array([G[k_] for k_ in LEAD_KINDS])
            cand = (~self.dead[:, None] & np.isin(self.skind, kinds) & (self.srank >= 0.85) & (self.slead != -2))
            nn, jj = np.nonzero(cand)
            u = self._lw_rng.random(len(nn))
            for n, j_, u_ in zip(nn, jj, u):
                n, j_ = int(n), int(j_)
                if (n, False, j_) in held:
                    continue
                k = int(self.slead[n, j_])
                if k >= 0 and 1 + int(self.stand[n, k]) > 3:
                    continue
                if u_ >= par["take"] * (2.0 if self._lw_back.get((n, j_), NEVER) <= t else 1.0):
                    continue
                pl_ = int(self.shnt[n, j_]) if getattr(self, "shnt", None) is not None and getattr(W, "hp_s", None) is not None else -1
                p = self._lead_new(n, "place" if pl_ >= 0 else "setting", int(self.set_sphere[n, j_]), j_, pl_, t)
                if p is None:
                    continue
                if k >= 0:   # the leader they replace is a member again (unless they lead another of the life's settings)
                    others = (self.slead[n] == k); others[j_] = False
                    if not others.any():
                        self.rmask[n, k] &= ~LEAD_BIT[int(self.skind[n, j_])]
                self.slead[n, j_] = -2
        gone_ = {(int(n_), int(i_)) for n_, i_, _ in self.lw_lost}   # titles a post's end took (the engine drops them
        for n, i_ in zip(*np.nonzero(self.lw_has & ~self.dead[:, None])):   # after this week): no new post for them
            if (int(n), int(i_)) in gone_:
                continue
            if (int(n), True, int(i_)) not in {(p["n"], p["kind"] == "office", p["slot"]) for p in self.lw_posts}:
                pk_, sp_, gk_ = LEAD_TITLES[self.lw_tnames[i_]]
                gs_ = np.nonzero(self.skind[n] == G[gk_])[0] if gk_ else []   # the setting it leads, when the life is in one
                j_ = SPHERES.index(sp_); pl_ = -1
                if len(gs_):
                    gs_ = int(gs_[0]); j_ = int(self.set_sphere[n, gs_])
                    if getattr(self, "shnt", None) is not None and getattr(W, "hp_s", None) is not None:
                        pl_ = int(self.shnt[n, gs_])
                self._lead_new(int(n), "office", j_, int(i_), pl_, t, gslot=gs_ if isinstance(gs_, int) else -1)
        # 6. the leaders' mix of each town sphere (the lead lever's size x (.5 + legitimacy)), and the shadow target
        pl = np.zeros((self.n_loc, 9, C + 1))
        self.lead_sh = np.zeros((self.N, C))
        for p in self.lw_posts:
            if self.dead[p["n"]]:
                continue
            wt_ = 0.5 + p["legit"]
            pl[p["loc"], p["sphere"], :C] += wt_ * self.w[p["n"]]; pl[p["loc"], p["sphere"], C] += wt_
            c_ = int(self.iperm[p["way"]])
            self.lead_sh[p["n"], c_] = max(self.lead_sh[p["n"], c_],
                                           par["sh"] * min((t - p["way_t"]) / 52.0 / par["sh_years"], 1.0))
        W.sph_plead = pl if pl[..., C].any() else None

    def lead_due(self, t=None):
        """The posts' moments waiting this week [(life, key, post id)]; those waited for too long lapse (a fall's: the
        post ends, "fell"; a hand-over's: it ends at its term)."""
        t = self.t if t is None else t
        out = []
        for d_ in list(self.lw_due):
            if d_ not in self.lw_due:   # taken out with its post (an earlier lapse ended or renewed the same post)
                continue
            n, key, pid, t0_ = d_
            p = next((p_ for p_ in self.lw_posts if p_["id"] == pid), None)
            if p is None or self.dead[n]:
                self.lw_due.remove(d_); continue
            if t - t0_ > self.lw_par["wait"]:
                self.lw_due.remove(d_)
                if key == "lead_fall":
                    self._lead_end(p, t, "fell")
                elif key == "lead_hand":   # unanswered: they stay on, as the term's renewal decides
                    self._lead_renew(p, t)
                continue
            out.append((int(n), key, int(pid), p["way"]))
        return out

    def lead_resolve(self, n, pid, key, way, fall, hand, succ, idle, t=None):
        """The post's moment came and the character acted: way (an option's lead:, -1 none), fall (go 0, fight 1,
        again 2), hand (chosen 0, open 1, stay 2). take: the post takes the option's way; crisis: an option of the post's
        way holds it, another way shifts the post to it; routine: a rules option moves the inspiring post to rules;
        fall: go ends it, fight keeps it when the act works (legitimacy back to .3; once a post) and ends it when not,
        again stands down (the take chance there doubles after a year); hand: chosen or open hands it on, stay leaves it
        to the term's renewal (lead_posts: renew x (.5 + legitimacy), max_terms).
        Returns the event."""
        t = self.t if t is None else t
        p = next((p_ for p_ in self.lw_posts if p_["id"] == int(pid)), None)
        self.lw_due = [d_ for d_ in self.lw_due if not (d_[2] == int(pid) and d_[1] == key)]
        if p is None:
            return None
        way = -1 if idle else int(way); fall = -1 if idle else int(fall); hand = -1 if idle else int(hand)
        ans = None
        def set_way(c_):
            if c_ != p["way"]:
                p["way"] = int(c_); p["way_t"] = int(t); p["succ_t"] = int(t); p["fade_t"] = int(t); p["fades"] = 0
                p["fair_lo"] = False
                self._lead_legit(p)
        if key in ("lead_take", "lead_crisis") and way >= 0:
            ans = "held" if way == p["way"] else "shifted"
            set_way(way)
        elif key == "lead_routine":
            ans = "routine" if way == 0 else "kept"
            if way == 0:
                set_way(0)
        elif key == "lead_fall":
            if fall == 1 and succ:
                ans = "fought"; p["fought"] = 1; p["dent"] = self.lw_par["fight"] - self._lead_fit(p); self._lead_legit(p)
            elif fall == 2:
                ans = "stood down"; self._lw_back[(int(n), int(p["slot"]))] = int(t) + int(self.lw_par["again"])
                self._lead_end(p, t, "stood down")
            else:
                ans = "fell"; self._lead_end(p, t, "fell")
        elif key == "lead_hand":
            if hand in (0, 1):
                ans = "handed on"; self._lead_end(p, t, "handed on")
            else:   # stay (or no answer): the term's renewal decides (renewed, a term limit or the term's end)
                ans = "stayed"; self._lead_renew(p, t)
        ev = dict(n=int(n), t=int(t), kind="lead", state="answered", key=key, answer=ans, post=p["kind"],
                  sphere=SPHERES[p["sphere"]], way=LEAD_WAYS[p["way"]], legit=round(p["legit"], 3), worked=bool(succ))
        if self.watch[n]:
            self.events.append(ev)
        return ev

    def lead_info(self, n):
        """Life n's posts for the game: each with its kind, sphere, the led place (its name in the world's epoch, or the
        setting kind or the office), the way (rules .. custom), legitimacy, start and end (age), the end's reason and
        its falls; the posts held now first, then the ended ones."""
        out = []
        for p in [p_ for p_ in self.lw_posts if p_["n"] == n] + [p_ for p_ in self.lw_ended if p_["n"] == n]:
            if p["place"] >= 0 and getattr(self.W, "place_info", None) is not None:   # a named place: its name and kind
                where = dict(self.W.place_info(int(p["place"])))
            else:
                where = {}
            if p["kind"] == "office":
                where["title"] = self.lw_tnames[p["slot"]]
            sl_ = p["slot"] if p["kind"] != "office" else p.get("gslot", -1)
            if sl_ >= 0 and self.skind[n, sl_] >= 0:
                where["setting"] = GROUP_KINDS[int(self.skind[n, sl_])]
            if not where:
                where["sphere"] = SPHERES[p["sphere"]]   # the town's sphere
            out.append(dict(id=p["id"], kind=p["kind"], sphere=SPHERES[p["sphere"]], place=where, way=LEAD_WAYS[p["way"]],
                            colour=COLORS[p["col"]], legit=round(p["legit"], 3), start=round((p["t0"] - self.t0) / 52.0, 2),
                            end=None if p["end_t"] is None else round((p["end_t"] - self.t0) / 52.0, 2), why=p["why"],
                            post_kind=p["pk"], terms=p["terms"],
                            falls=[dict(age=round((f_[0] - self.t0) / 52.0, 2), way=LEAD_WAYS[f_[1]], key=f_[2]) for f_ in p["falls"]]))
        return out

    # ------------------------------------------------------------------ who: slots (world-fields.md)
    def fill(self, n, slots, at=None, t=None):
        """{slot: cast id} for a moment's who: slots, from the cast by role and closeness, else a new face (never
        blocks). at: an institution kind for the slot "at" (the person who stands for it there)."""
        t = self.t if t is None else t; rng = self.rng; a = self._age(t)
        taken = set(); out = {}
        u = self.used[n] & self.lv[n]
        age = (t - self.born[n]) / 52.0
        for s_ in ([slots] if isinstance(slots, str) else list(slots)) + (["at"] if at is not None else []):
            if s_ == "dead":
                cand = np.nonzero(self.used[n] & ~self.lv[n] & (self.cmax[n] >= self.P["layer_c"][3]))[0]
                score = self.cmax[n, cand] - (t - self.died_t[n, cand]) / 5200.0
            elif s_ == "partner":
                cand = np.array([self.pslot[n]]) if self.pslot[n] >= 0 and self.lv[n, self.pslot[n]] else np.zeros(0, np.int64)
                score = np.ones(len(cand))
            elif s_ == "elder":
                cand = np.nonzero(u & (((self.rmask[n] & BIT["elder"]) != 0) | ((age >= 60) & (age >= a + 20))))[0]
                score = self.c[n, cand] + 0.5 * ((self.rmask[n, cand] & BIT["elder"]) != 0)
            elif s_ == "friend":
                cand = np.nonzero(u & ((self.rmask[n] & BIT["friend"]) != 0) & ((self.rmask[n] & KINMASK) == 0))[0]
                score = self.c[n, cand]
            elif s_ == "at":
                cand = np.zeros(0, np.int64); score = cand
            elif s_ in BIT:
                cand = np.nonzero(u & ((self.rmask[n] & BIT[s_]) != 0))[0]
                score = self.c[n, cand] + 0.3 * self.inci[n, cand]
                if s_ in ("boss", "colleague", "teacher"):
                    j_ = np.nonzero(self.skind[n] == G["work" if s_ != "teacher" else "class"])[0]
                    if len(j_):
                        score = score + 1.0 * (((self.mset[n, cand] >> j_[0]) & 1) > 0)
            else:
                cand = np.zeros(0, np.int64); score = cand
            keep = np.array([k_ not in taken for k_ in cand], bool) if len(cand) else np.zeros(0, bool)
            cand, score = cand[keep], np.asarray(score)[keep]
            if self.wa_n and len(cand) and s_ not in ("dead", "partner"):   # the world answers, E2: who fits the goal
                score = score + self._wa_fill_bonus(n, cand)
            if len(cand):
                k = int(cand[np.argmax(score)])
            else:
                k = self._face(n, s_, t, at)
            if k >= 0:
                taken.add(k); out[s_] = int(self.uid[n, k])
        return out

    def _face(self, n, slot, t, at=None):
        """A new person for a slot no cast member fits: drawn from the locality, layer 4, dropped unless a tie forms."""
        rng = self.rng; a = self._age(t)
        off = dict(parent=28, grandparent=55, elder=40, child=-28, teacher=20, boss=15, mentor=15).get(slot, 0)
        ag = max(1.0, a + off + rng.normal(0, 5))
        F = self._gen(np.array([n]), np.array([t - int(ag * 52)]), t)
        # a face never takes a core or family role: a partner slot gets a date, a family slot a distant relative
        role = (R["prospect"] if slot == "partner" else R["kin"] if slot in ("parent", "child", "sibling", "grandparent")
                else R[slot] if slot in R and slot not in ("dead", "at") else R["acquaintance"])
        if slot == "prospect":
            same = rng.random() < self.P["same_sex"][int(_uclip(self.attr[n], 0, 4))]
            F["fem"] = np.array([bool(self.female[n]) == bool(same)])
        if slot in ("boss", "teacher", "mentor", "elder", "at"):
            F["stand"] = np.array([1])
        sl = self._add(F, t, role, c0=0.05, trust0=0.45, face=True, alive=slot != "dead", quiet=True)
        if not len(sl):
            return -1
        k = int(sl[0])
        if slot == "at" and at is not None:
            self.inst[n, k] = self._inst_pick(n, at) if at in INST_KINDS else -1
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="face", cid=int(self.uid[n, k]), role=slot))
        return k

    # ------------------------------------------------------------------ place and moving (spec 3 §2.6)
    def move_wish(self, t=None, S=None):
        """Weekly chance of moving (all moves, local and away): by age, peaking in the twenties (about 8-9% a year
        overall, US Census), higher after a partnership starts or ends. The engine scales its moving moments by it."""
        t = self.t if t is None else t; a = self._age(t); P = self.P
        r = np.interp(a, [a_ for a_, _ in P["move_age"]], [r_ for _, r_ in P["move_age"]])
        pc = np.exp(-(t - self.par_change) / 26.0)
        un = float(self._unemp("unemp"))
        ul = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, un)), float)[self.loc]
        r = r * (1 + 1.5 * pc) * _uclip(1 + 3 * (ul - un), 0.7, 1.5)
        r = np.full(self.N, r / 52.0) if np.ndim(r) == 0 else r / 52.0
        if getattr(self, "roots", None) is not None:   # phase 5: roots, the move wish x .5 while a holding is held
            r = r * np.where(self.roots, 0.5, 1.0)
        return r

    def kin_let_down(self, n, by, t):
        """Phase 5, a kin debt broken: trust falls by `by` with the closest living parent or sibling, who remembers."""
        u = self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["parent"] | BIT["sibling"])) != 0)
        if u.any():
            k = int(np.argmax(np.where(u, self.c[n], -1)))
            self.trust[n, k] = max(0.0, float(self.trust[n, k]) - by)

    def move(self, n, loc=None, why=None, t=None, local=None):
        """The household moves: to loc (another locality), or within the locality (a new neighbourhood). Distant
        ties fade faster (W.comm slows that); the local groups, their rank and the neighbourhood circle are lost.
        why: 'left home' (a home of one's own), 'came home' (back to the parents' place), or None."""
        t = self.t if t is None else t; rng = self.rng; P = self.P; a = self._age(t)
        if why == "left home" and not self.own_home[n]:
            self._leave_home(n, t)
        if why == "came home":
            ps = np.nonzero(self._has_role(n, "parent") & self.lv[n] & (self.msoc[n] == self.soc[n]))[0]
            loc = int(min(self.mloc[n, ps[0]], self.n_loc - 1)) if len(ps) else loc
        if local is None:
            local = loc is None and rng.random() >= P["far_share"] * (1.3 if 18 <= a < 30 else 1.0)
        old = int(self.loc[n])
        if not local:
            if loc is None:
                wt = self._move_wt(n, a)
                loc = int(rng.choice(self.n_loc, p=wt / wt.sum())) if wt.sum() > 0 else old
            self.loc[n] = int(loc)
            for j_ in range(self.M):   # local groups are lost (online ones stay; the household moves)
                if self.skind[n, j_] in LOCAL_KINDS:
                    self._leave(n, j_, t, "moved")
            hh = self.hhj[n]
            if hh >= 0:   # the household moves along: the partner, the children at home (a child: parents, siblings)
                mates = np.nonzero(((self.mset[n] >> hh) & 1) > 0)[0]
                self.mloc[n, mates] = loc; self.msoc[n, mates] = self.soc[n]
        else:
            js = np.nonzero(self.skind[n] == G["neighbours"])[0]
            for j_ in js:
                self._leave(n, int(j_), t, "moved")
        self._pick_nb([n])
        self.n_moves[n] += 1; self.last_move[n] = t
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="moved", loc=int(self.loc[n]), nb=int(self.nb[n]),
                                    away=not local, why=why))

    def _move_wt(self, n, a):
        """Weights of the other localities for a move away: population, young adults toward cities, universities
        and the capital, work (lower unemployment), the old toward their children and parents."""
        wt = self.loc_p.copy()
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        if feat.shape[1] == len(FEATURES) and 18 <= a < 30:
            wt = wt * (1 + 1.0 * feat[:, [FEATURES.index("capital"), FEATURES.index("university"), FEATURES.index("city")]].any(1))
        un = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, 0.05)), float)
        wt = wt * np.exp(-8 * (un - un.mean()))
        kin_l = self.mloc[n, self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["child"] | BIT["parent"])) != 0)
                          & (self.msoc[n] == self.soc[n])]
        kin_l = kin_l[kin_l < self.n_loc]
        if a >= 60 and len(kin_l):
            wt[kin_l] *= 3
        wt[int(self.loc[n])] = 0
        return wt

    def move_options(self, n, k=3, t=None):
        """Up to k candidate localities for a move away, drawn by the weights move() uses (a stream of their own, so
        asking changes nothing): [dict(loc, kind, size, features)], size 0-3 (village, town, city, metropolis)."""
        t = self.t if t is None else int(t); n = int(n)
        wt = self._move_wt(n, self._age(t))
        cand = np.nonzero(wt > 0)[0]
        if not len(cand):
            return []
        r_ = np.random.default_rng([self.seed, 37, self.run_seed, n, max(int(t), 0)])
        key = np.log(wt[cand]) + r_.gumbel(size=len(cand))   # weighted draws without replacement (Gumbel top-k)
        return [self._loc_info(int(l_)) for l_ in cand[np.argsort(-key, kind="stable")[:int(k)]]]

    def _loc_info(self, l):
        kk = self._wf("loc_kind_key", None)
        kind = kk[l] if kk is not None else np.asarray(self._wf("loc_kind", np.zeros(self.n_loc)))[l]
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        fl = [FEATURES[i_] for i_ in np.nonzero(feat[l])[0]] if feat.shape[1] == len(FEATURES) else []
        sz = np.asarray(self._wf("loc_size", np.zeros(self.n_loc, np.int64)))
        return dict(loc=int(l), kind=kind.item() if hasattr(kind, "item") else kind,
                    size=int(sz[l]) if len(sz) > l else 0, features=fl)
