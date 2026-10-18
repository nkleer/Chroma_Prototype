"""World's methods for the spheres of society: phase 3 (their events, chains, links and cascades) and Replace, and
save and load.

Part of class World (world.py), which inherits EventsMixin; moved out of world.py verbatim. A method here reads module
names through the imports below, the same objects world.py has, and self for everything on the World."""
import numpy as np
from library import COLORS, ERA_KINDS
from combos import IDEAS
from world_keys import (FEATURES, HAUNT_KINDS, INST_KINDS, LAW_KEYS, LAW_STATES, NORM_KEYS, SECTORS, SPHERES,
    STATE_SPHERE)
from world_base import (C, C_RULES, FIG_ROLES, FIN_RULES, HAUNT_SPH, INST_SPH, NF, N_PLACES, PANDEMIC, RIGHTS,
    S3_PARAMS, S3_RULES, SEASONS, SECTOR_SPH, SPH, SPH_PAIRS, SPH_RULES, STATE_PARTS, V224_RULES, WAR_STATES,
    WEEK_SEASON, _jsafe, _uclip)


class EventsMixin:
    # ------------------------------------------------------------------ the spheres of society (item 15): phase 3
    SPH_LAG = {"quarters": (1, 4), "a year": (3, 6), "years": (4, 20)}   # a chain's window, in quarters after its event

    def _sph_ev_tables(self):
        """The sphere events as arrays (made once, not saved): every event of sphere_data.EV, in its order (the Library's
        sphere_event: names an index here); its base chance a quarter (0 outside this world's epoch and for the
        world-fired events; else sph_ev_base for every event, the sph_par ev_base, or the fitted sphere_ev_base.BASE);
        hazard weights over the readers (the eight drivers, the hazard variables, the 74 sphere states; a bare state key
        is the event's own sphere's, else the one sphere that has it); the effect rows (a sphere's faces in this world's
        colour frame, and their steps on the sphere's own states); the chains; the world-fired events."""
        c_ = getattr(self, "_cache_sphev", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        try:
            from sphere_ev_base import BASE as FIT
        except ImportError:
            FIT = {}
        T = self._sph_tables(); pr = T["pr"]; ep = T["ep"]; EV = SD.EV; n = len(EV)
        key = {e["key"]: i for i, e in enumerate(EV)}
        cols = list(SD.DRIVERS) + list(SD.HAZARD_VARS) + list(SD.STATES); ci = {k: j for j, k in enumerate(cols)}
        def res(e, k):
            if k in ci:
                return k
            if f"{e['sphere']}.{k}" in ci:
                return f"{e['sphere']}.{k}"
            m_ = [s_ for s_ in SD.STATES if s_.split(".")[1] == k]
            return m_[0] if len(m_) == 1 else None
        b_ = self.p.get("sph_ev_base")
        tab = pr.get("ev_base") if isinstance(pr.get("ev_base"), dict) else {}
        fired = np.array([e.get("fired") is not None for e in EV])
        base = np.array([(float(b_) if b_ is not None else float(tab.get(e["key"], tab.get(e["family"], FIT.get(e["key"], 0.0)))))
                         * (ep in e["epochs"]) for e in EV]) * ~fired
        Hm = np.zeros((n, len(cols))); unread = []
        for i, e in enumerate(EV):
            for k, v in e["hazard"].items():
                r_ = res(e, k)
                if r_ is None:
                    unread.append((e["key"], k))
                else:
                    Hm[i, ci[r_]] += v
        own = [s_ for s_ in SD.STATES if s_ not in SD.STATE_WORLD or s_ == "rule.pressure"]   # (pressure: the world's Q only
        oi = {s_: j for j, s_ in enumerate(own)}                                                # with hist_pressure)
        rows = []
        for i, e in enumerate(EV):
            for r in e["rows"]:
                if r["target"] not in SPH:
                    continue                                   # a model domain's row: words only (answers item 3)
                f = np.zeros(C) if r["faces"] is None else np.asarray(r["faces"], float)[self.perm]
                st = [(oi[f"{r['target']}.{k}"], u) for k, u in r["state"].items() if f"{r['target']}.{k}" in oi]
                if f.any() or st:
                    rows.append((i, SPH[r["target"]], f, r["scope"] == "big", r["tau"], st))
        big = np.array([any(r["scope"] == "big" for r in e["rows"]) for e in EV])
        shrows = [(i, SPH[r["target"]], np.array([float(c_ in r["shadow"]) for c_ in COLORS])[self.perm], r["scope"] == "big")
                  for i, e in enumerate(EV) for r in e["rows"] if r.get("shadow") and r["target"] in SPH]   # N5's turns
        shsph = np.zeros((n, 9))
        for i_, j_, _, _ in shrows:
            shsph[i_, j_] = 1.0
        chains = [(i, key[k], *self.SPH_LAG.get(lag, self.SPH_LAG["years"])) for i, e in enumerate(EV)
                  for k, lag in e["chains"] if k in key]
        c_ = dict(n=n, key=key, names=[e["key"] for e in EV], base=base, cols=cols, Hm=Hm, unread=unread, dice=np.array([e["dice"] for e in EV]), big=big,
                  rows=rows, chains=chains, shrows=shrows, shsph=shsph / np.maximum(shsph.sum(1, keepdims=True), 1), sig=(float(pr.get("sig_local", 0.2)), float(pr.get("sig_big", 0.4))),
                  sph=np.array([SPH[e["sphere"]] for e in EV], np.int64), fired=fired, own=own,
                  wsi=[ci[s_] for s_ in SD.STATE_WORLD], osi=[ci[s_] for s_ in own], sr=dict(SD.STATE_RULE),
                  fam={(e["sphere"], e["family"]): [j for j, x in enumerate(EV) if (x["sphere"], x["family"]) == (e["sphere"], e["family"])]
                       for e in EV})
        self._cache_sphev = c_
        return c_

    def _sph_world_states(self, E):
        """The 16 sphere states that are world.py variables (dynamics.json events_run states.world_vars), per town, 0..1,
        in sphere_data.STATE_WORLD's order."""
        import sphere_data as SD
        nl = self.n_loc; p = self.p; b = lambda x_: np.broadcast_to(np.asarray(x_, float), (nl,))
        q_ = (float(self.Q) / max(2 * float(self.q_thr), 1e-9) if self._s3("hist_pressure") else None)
        ew = np.asarray(self.ext_war)
        rv = self.revival[1] > 0 if isinstance(self.revival, (tuple, list)) else False
        v = {"rule.trust": b(self.trust), "rule.purse": b(self.welfare), "rule.faction_heat": b(self.polar),
             "rule.favour": b(getattr(self, "corruption", 0.1)), "rule.say": b((self.regime + 10) / 20),
             "rule.pressure": None if q_ is None else b(q_), "prot.war": b(self.war / 2),
             "prot.order": 1 - np.asarray(self.loc_crime, float), "prot.threat": b(float((ew[1:] > 0).mean()) if len(ew) > 1 else 0.0),
             "comm.prices": b(0.5 + 0.05 * (self.infl - p["infl0"])), "care.outbreak": b(float(self.pandemic in (1, 2, 3))),
             "care.skill": b(self.medical), "prod.hands": 0.5 + (self.natural - np.asarray(self.loc_unemp, float)) / 20,
             "prod.stores": b(0.5 - self.food / 10), "faith.devotion": b(self.spiritual), "faith.fervour": b(0.5 + 0.3 * rv)}
        j_ = E["own"].index("rule.pressure")
        own = (self.sph_st[:, j_] + self.sph_st_soc[j_] - 0.5 if getattr(self, "sph_st", None) is not None
               else np.full(nl, 0.5))                                     # (phase 4's felt fairness reads without events)
        out = [own if (k == "rule.pressure" and v[k] is None) else v[k] for k in SD.STATE_WORLD]
        return _uclip(np.stack(out, 1), 0, 1)

    def _sph_hazard_x(self, E, e_need):
        """Each town's reading of every hazard reader (n_loc x len(cols)), clipped to -1..1: the drivers against the town's
        memory (as T), the hazard variables (drivers.vocabulary), the sphere states' level against their memory (own
        states: the town's plus the society's)."""
        import sphere_data as SD
        nl = self.n_loc; X = np.zeros((nl, len(E["cols"])))
        wl = (0.5 if self.war == 1 else 1.0 if self.war == 2 else 0.0) + 0.2 * float(np.any(np.asarray(self.ext_war) > 0))
        ob = float(self.pandemic in (1, 2, 3))
        hist = getattr(self, "sph_war4", None)
        hist = np.full((2, 4), [[wl], [ob]]) if hist is None or np.ndim(hist) == 1 else np.concatenate([hist[:, 1:], [[wl], [ob]]], 1)
        self.sph_war4 = hist
        nd = len(SD.DRIVERS); X[:, :nd] = self.sph_x
        hv = dict(war_drop=max(0.0, hist[0, 0] - wl), outbreak_drop=max(0.0, hist[1, 0] - ob),
                  disaster_now=np.minimum(np.asarray(self.loc_disaster, float), 1), meaning_gap=e_need[:, 2],
                  welfare=float(self.welfare) - float(self.p["welfare0"]),
                  old_share=self._sph_ages()[:, 2] - np.asarray(self.sph_ref["ages"], float)[:, 2])
        for j, k in enumerate(SD.HAZARD_VARS):
            X[:, nd + j] = hv.get(k, 0.0)
        lv = np.zeros((nl, len(SD.STATES)))
        k0 = nd + len(SD.HAZARD_VARS)
        lv[:, np.asarray(E["osi"]) - k0] = _uclip(self.sph_st + self.sph_st_soc[None] - 0.5, 0, 1)
        lv[:, np.asarray(E["wsi"]) - k0] = self._sph_world_states(E)
        if getattr(self, "sph_st_m", None) is None:
            self.sph_st_m = lv.copy()
        X[:, k0:] = lv - self.sph_st_m
        self.sph_st_m += E["sr"]["mem"] * (lv - self.sph_st_m)
        return _uclip(X, -1, 1)

    def fire_sphere_event(self, key, loc=-1, big=True):
        """A world rule fires sphere event key (bare, or "sphere.key") at the next quarter, in town loc (-1: where its
        hazard is highest; a big event acts for the whole society). big=False with a town keeps the event in that town,
        as for a world event that was not big. Nothing while sph_events is off."""
        if self.p.get("sph_events", False):
            if not hasattr(self, "sph_wq") or self.sph_wq is None:
                self.sph_wq = []
            self.sph_wq.append(["sphere", str(key).split(".")[-1], None, int(loc), -1, None, bool(big)])

    def _sph_wf_key(self, domain, kind, key, value):
        """The sphere event a world event fires (dynamics.json events_run world_fired; one key, one event), or None."""
        v = value if isinstance(value, dict) else {}
        if domain == "institution" and kind in ("closure", "scandal") and v.get("inst", -1) >= 0:
            i = int(v["inst"]); k_ = INST_KINDS[int(self.inst_kind[i])]; sp = int(self.inst_sphere[i])
            sec = int(self.inst_sector[i]) if self.inst_sector[i] >= 0 else -1
            if kind == "closure":
                if k_ == "bank":
                    return "lender_fails"
                if k_ == "employer" and sec in (SECTORS.index("farm"), SECTORS.index("industry")):
                    return "works_close"
                return (SPHERES[sp], "a_house_closes", v.get("loc", -1))
            if SPHERES[sp] == "rule":
                return "favour_exposed"
            if k_ == "faith body":
                return "scandal"
            if k_ in ("hospital", "charity"):
                return "neglect_scandal"
            if k_ == "bank" or (k_ == "employer" and sec == SECTORS.index("services")):
                return "swindle"
            return (SPHERES[sp], "trust_broken", v.get("loc", -1))
        if domain == "era" and kind == "breakthrough":
            return {"reform": "reform_wave", "revolution": "rising", "restoration": "restoration"}.get(key)
        if domain == "state" and kind == "law changed":
            return "drink_banned" if key == "alcohol" and v.get("state") == "banned" else None
        if domain == "tech" and kind == "arrives":
            return "new_medium" if key in ("phone", "internet", "video calls") else "new_tool"
        if domain == "nature" and kind == "pandemic":
            return "plague_wave" if key == "rising" else None
        if domain == "nature" and kind == "price shock":
            return "dearth" if key == "food" else None
        # the say and its rights (events_run world_fired, Outer world 10-10): speech or women's rights gained, or the
        # regime moving up, widen the say; a right lost in speech, faith, sexuality or women's rights, or the regime moving
        # down, narrows it, and only the fall seizes power (a lockdown's lost movement is neither)
        if domain == "state" and kind == "right gained":
            return "say_widened" if key in ("speech", "women") else None
        if domain == "state" and kind == "right lost":
            return "rights_narrowed" if key in ("speech", "faith", "sexuality", "women") else None
        if domain == "state" and kind == "regime changes":
            return {"up": "say_widened", "down": ["power_seized", "rights_narrowed"]}.get(v.get("state"))
        if domain == "nature" and kind == "drought":        # C4 (c4_nature)
            return "lean_year"
        if domain == "nature" and kind == "glorious spring":   # C4: in farming places
            l_ = int(v.get("loc", -1))
            ok_ = 0 <= l_ < self.n_loc and "farming" in FEATURES and bool(self.loc_feat[l_, FEATURES.index("farming")])
            return "rich_season" if ok_ else None
        if domain == "figure" and kind == "falls":
            return "star_falls" if key in ("star", "athlete") else None
        return {("belief", "revival"): "faith_revival", ("place", "crime wave"): "crime_wave",
                ("nature", "disaster"): "disaster_strikes", ("abroad", "war begins"): "call_up",
                ("abroad", "war ends"): "peace_made",
                ("institution", "budget cut"): "hands_short"}.get((domain, kind))

    def _sph_events_q(self, e_need):
        """Phase 3 (sph_events): this quarter's sphere events and the fading demand shifts of all that fired
        (dynamics.json face_mix "Events (X)": sig x faces x exp(-quarters / tau)). Each event's chance a quarter is its
        base x exp(hazard . readings) x 3 inside a chain's window (x the season's hazard with sph_seasons); a big event
        is one draw for the society. Dice only for events with dice (a hashed draw by world seed and quarter, so no
        stream moves); the rest add their chance each quarter and fire when the sum reaches 1, which goes back to 0
        (item 14: the same start, the same history). The world-fired events fire with the world's own (queued by _event
        since the last quarter). The sphere states relax toward .5. Returns X (n_loc x 9 x 5)."""
        E = self._sph_ev_tables(); nl = self.n_loc; n = E["n"]; q = int(self.t // 13); sr = E["sr"]
        if getattr(self, "sph_ev_last", None) is None:
            self.sph_ev_last = np.full((nl, n), -10 ** 6, np.int64)   # the week each event last fired in each town
            self.sph_ev_acc = np.zeros((nl, n)); self.sph_ev_win = np.zeros((nl, n, 2), np.int64)
            self.sph_ev_rows = np.zeros((0, 4 + C))                     # town, sphere, start quarter, tau, then sig x faces
            self.sph_ev_log = np.zeros((0, 3), np.int64)                # week, event, town (-1: the whole society)
            self.sph_st = np.full((nl, len(E["own"])), sr["start"]); self.sph_st_soc = np.full(len(E["own"]), sr["start"])
        xv = self._sph_hazard_x(E, e_need)
        p = E["base"][None] * np.exp(xv @ E["Hm"].T)
        w_ = self.sph_ev_win; p = p * np.where((w_[..., 0] <= q) & (q <= w_[..., 1]), 3.0, 1.0)
        if self.p.get("sph_seasons", False):   # N7: the season in the middle of the coming quarter
            p = p * self._sph_tables()["seas_z"][E["sph"], WEEK_SEASON[(self.t + 7) % 52]][None]
        if self.p.get("sph_memory", False) or self.p.get("pair_calm", False) or self.p.get("sph_cascades", False):
            p = p * self._sph_p3_factor(E, q, w_)
        if self.p.get("sph_shadow", False) and getattr(self, "sph_sh", None) is not None:   # N5: a grey sphere's shadow events
            p = p * np.exp(self.sph_grey() @ E["shsph"].T - self._sh_par()["start"] * (E["shsph"].sum(1) > 0)[None])
        self._cache_evh = np.exp(xv @ E["Hm"].T)                                         # for where a big event's local
        on = E["base"] > 0                                                               # rows act (not saved)
        if on.any():
            p = np.where(E["big"][None], p.mean(0, keepdims=True), p)                       # one chance for the society
            r = np.random.default_rng([self._seed + 7919, q]).random((nl, n))
            r[:, E["big"]] = r[:1, E["big"]]
            self.sph_ev_acc += np.where(E["dice"][None], 0.0, p)
            fire = on[None] & np.where(E["dice"][None], r < p, self.sph_ev_acc >= 1.0)
            self.sph_ev_acc = np.where(fire & ~E["dice"][None], 0.0, self.sph_ev_acc)
            fire[1:, E["big"]] = False                                                       # a big event fires once
            for l, i in zip(*np.nonzero(fire)):
                self._sph_fire(int(l), int(i), q, E)
        for dom, kind, k_, lc_, in_, st_, *bg_ in (getattr(self, "sph_wq", None) or []):   # the world-fired events
            ek = kind if dom == "sphere" else self._sph_wf_key(dom, kind, k_, dict(inst=in_, loc=lc_, state=st_) if in_ >= 0 else dict(loc=lc_, state=st_))
            if isinstance(ek, tuple):                                    # a house closes, trust broken: the sphere's own
                cand = E["fam"].get((ek[0], ek[1]), [])                  # event of that family with the highest hazard
                l_ = ek[2] if 0 <= ek[2] < nl else None
                h_ = self._cache_evh[l_ if l_ is not None else slice(None)]
                ek = E["names"][cand[int(np.argmax(np.atleast_2d(h_)[:, cand].mean(0)))]] if cand else None
            for ek in (ek if isinstance(ek, list) else [ek]):
                if ek is None or ek not in E["key"]:
                    continue
                i = E["key"][ek]; l = int(lc_) if 0 <= lc_ < nl else int(np.argmax(self._cache_evh[:, i]))
                here_ = 0 <= lc_ < nl
                self._sph_fire(l, i, q, E, here=here_, local=here_ and not (bg_[0] if bg_ else True))   # a town's own news

        self.sph_wq = []; self.sph_reg_seen = float(self.regime)
        if self.p.get("sph_memory", False):
            self.sph_mem = np.maximum(self._sph_mem() - self._sph_p3_tables()["fade"], 0.0)
        self.sph_st += sr["relax"] * (sr["start"] - self.sph_st); self.sph_st_soc += sr["relax"] * (sr["start"] - self.sph_st_soc)
        # the fading shifts of every row still acting
        R_ = self.sph_ev_rows; X = np.zeros((nl, 9, C))
        if len(R_):
            age = q - R_[:, 2]; k = np.exp(-age / R_[:, 3])
            keep = k >= 0.01; R_ = self.sph_ev_rows = R_[keep]; k = k[keep]
            np.add.at(X, (R_[:, 0].astype(np.intp), R_[:, 1].astype(np.intp)), R_[:, 4:] * k[:, None])
        return X

    SPH_LINK_LAG = {"weeks": 1, "months": 1, "quarters": 2, "years": 8, "decades": 40}   # a link's lag, in quarters

    def _sph_link_tables(self):
        """The 72 sphere-to-sphere links as arrays (made once, not saved): A (link x the 74 states) averages each link's
        from-states, signed; B (link x own state) is each to-state's step per unit, signed, x strength / 3 (to-states
        that are world.py variables are left alone: words only, as the events' domain rows); rate, 1 / the lag in
        quarters; F (link x sphere x face), the colour readings: + feeds, - starves on the link's low side, x strength / 3,
        in this world's colour frame."""
        c_ = getattr(self, "_cache_sphlk", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        E = self._sph_ev_tables(); si = {k: j for j, k in enumerate(SD.STATES)}; oi = {k: j for j, k in enumerate(E["own"])}
        nL = len(SD.LINKS); A = np.zeros((nL, len(SD.STATES))); B = np.zeros((nL, len(E["own"]))); F = np.zeros((nL, 9, C))
        lid = {l["id"]: j for j, l in enumerate(SD.LINKS)}
        for j, l in enumerate(SD.LINKS):
            for k, sg in l["src"]:
                A[j, si[k]] += sg / len(l["src"])
            for k, sg in l["dst"]:
                if k in oi:
                    B[j, oi[k]] += sg * l["strength"] / 3
        for r in SD.LINK_COLOUR:
            f = np.array([(c in r["feeds"]) - (c in r["starves"]) for c in COLORS], float)[self.perm]
            F[lid[r["link"]], SPH[r["faces_in"]]] += (1 if r["side"] == "low" else -1) * r["strength"] / 3 * f
        rate = np.array([1.0 / self.SPH_LINK_LAG.get(l["lag"], 8) for l in SD.LINKS])
        c_ = self._cache_sphlk = dict(A=A, B=B, F=F, rate=rate, osi=[si[k] for k in E["own"]], wsi=[si[k] for k in SD.STATE_WORLD])
        return c_

    def _sph_links_q(self):
        """Phase 3 (sph_links): each link's input is the mean of its from-states' levels minus .5 (signed, "(down)"
        turned), lagged (it moves 1 / lag of the way a quarter, from 0); each to-state of the sphere's own steps
        link_k x strength / 3 x the lagged input a quarter (link_k .01: the links' loop gain, .0138 at most, stays under
        the states' relax of .02); the colour readings shift demand by link_c x strength / 3 x the lagged input, the low
        side feeding the row's feeds and starving its starves (the high side the other way round). Returns the X shift
        (n_loc x 9 x 5)."""
        E = self._sph_ev_tables(); Lk = self._sph_link_tables(); pr = self._sph_tables()["pr"]; nl = self.n_loc
        lv = np.zeros((nl, Lk["A"].shape[1]))
        lv[:, Lk["osi"]] = _uclip(self.sph_st + self.sph_st_soc[None] - 0.5, 0, 1)
        lv[:, Lk["wsi"]] = self._sph_world_states(E)
        x = (lv - 0.5) @ Lk["A"].T
        if getattr(self, "sph_lk", None) is None:
            self.sph_lk = np.zeros_like(x)
        self.sph_lk += Lk["rate"][None] * (x - self.sph_lk)
        self.sph_st = np.clip(self.sph_st + float(pr.get("link_k", 0.01)) * (self.sph_lk @ Lk["B"]), 0, 1)   # as events do
        return -float(pr.get("link_c", 0.3)) * np.einsum("ln,njc->ljc", self.sph_lk, Lk["F"])

    CAS_LAG = {"quarters": (1, 4), "a year or two": (4, 8), "years": (4, 20), "decades": (20, 60)}   # a cascade step's
    # window after the step before, in quarters ("a year or two": about 6 quarters, Outer world's answer 5)

    def _sph_p3_tables(self):
        """The memories, the pairs' quarrels and the cascades as arrays (made once, not saved): MF (event x memory) what
        each firing adds, MR (memory x event) each memory's pull on each hazard, fade; PQ (pair x event) the quarrel
        events of each pair (a pair face calms its own sphere's: every event is its own sphere's); the cascades with
        their steps as event indices (a step whose event cannot happen in this world's epoch passes time, as a step with
        no event does)."""
        c_ = getattr(self, "_cache_sphp3", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        E = self._sph_ev_tables(); n = E["n"]; key = E["key"]; ep = self._sph_tables()["ep"]
        mems = list(SD.MEMORIES); MF = np.zeros((n, len(mems))); MR = np.zeros((len(mems), n))
        for m_, nm in enumerate(mems):
            for k, a in SD.MEMORIES[nm]["feeds"].items():
                MF[key[k], m_] += a
            for k, a in SD.MEMORIES[nm]["raises"].items():
                MR[m_, key[k]] += a
        PQ = np.zeros((len(SPH_PAIRS), n), bool)
        for j, pr_ in enumerate(SPH_PAIRS):
            for k in SD.PAIR_QUARRELS.get(pr_, []):
                PQ[j, key[k]] = True
        runs = (E["base"] > 0) | E["fired"]
        cas = []; ids = []
        for c in SD.CASCADES:
            if ep not in c["epochs"]:
                continue
            st = [(key[k] if k is not None and runs[key[k]] else -1, lag) for k, lag in c["steps"]]
            if st and st[0][0] >= 0:
                cas.append(st); ids.append(c["id"])
        c_ = self._cache_sphp3 = dict(MF=MF, MR=MR, fade=float(SD.MEM_FADE), PQ=PQ, cas=cas, ids=ids,
                                      cas_first={st[0][0]: k for k, st in enumerate(cas)})
        return c_

    def _sph_mem(self):
        if getattr(self, "sph_mem", None) is None:
            self.sph_mem = np.zeros((self.n_loc, self._sph_p3_tables()["MF"].shape[1]))
        return self.sph_mem

    def _sph_p3_factor(self, E, q, w_):
        """This quarter's hazard factor per town and event (n_loc x n) from the memories (sph_memory: exp(memory . size)),
        the pair faces' calm (pair_calm: while a pair face holds over .1, x (1 - 2 x held), at least .5, on its sphere's
        quarrel events; a pair face that broke, x 1.5 for 8 quarters) and the running cascades (sph_cascades: x 3 on the
        next step's event inside its window, not on top of a chain's own x 3)."""
        P3 = self._sph_p3_tables(); nl = self.n_loc; f = np.ones((nl, E["n"]))
        if self.p.get("sph_memory", False):
            f = f * np.exp(self._sph_mem() @ P3["MR"])
        if self.p.get("pair_calm", False) and self.p.get("sph_pairs", False) and getattr(self, "sph_ph", None) is not None:
            h = self.sph_ph[:, E["sph"], :]                                        # town x event x pair: its sphere's
            calm = np.where(h > 0.1, np.maximum(1 - 2 * h, 0.5), 1.0)
            brk = getattr(self, "sph_pbrk", None)
            if brk is not None:
                calm = calm * np.where(brk[:, E["sph"], :] >= q, 1.5, 1.0)
            f = f * np.prod(np.where(P3["PQ"].T[None], calm, 1.0), axis=2)
        if self.p.get("sph_cascades", False) and getattr(self, "sph_cas", None):
            inch = (w_[..., 0] <= q) & (q <= w_[..., 1])                          # already x 3 by a chain
            for c, loc, k, lo, hi in self.sph_cas:
                i = P3["cas"][c][k][0]
                if lo <= q <= hi:
                    rows = slice(None) if loc < 0 else loc
                    f[rows, i] = np.where(inch[rows, i], f[rows, i], f[rows, i] * 3.0)
            self.sph_cas = [x for x in self.sph_cas if q <= x[4]]                  # a window passed: it ends
        return f

    def _sph_p3_fired(self, l, i, q, E, loc):
        """Event i fired (in town loc; -1 the whole society): it feeds or drains the memories (sph_memory; a society's
        event in every town), moves on the cascades waiting for it, and starts the cascade it begins (sph_cascades; one
        of each per town or society at a time)."""
        P3 = self._sph_p3_tables()
        if self.p.get("sph_memory", False) and P3["MF"][i].any():
            m = self._sph_mem(); rows = slice(None) if loc < 0 else loc
            m[rows] = np.clip(m[rows] + P3["MF"][i], 0, 1)
        if self.p.get("sph_cascades", False):
            cas = getattr(self, "sph_cas", None) or []
            out = []
            for c, lc, k, lo, hi in cas:
                st = P3["cas"][c]
                if st[k][0] == i and lo <= q <= hi and (lc < 0 or loc < 0 or lc == loc):
                    nxt = self._sph_cas_next(st, k + 1, q)
                    if nxt is not None:
                        out.append([c, lc, *nxt])
                else:
                    out.append([c, lc, k, lo, hi])
            c0 = P3["cas_first"].get(i)
            if c0 is not None and not any(x[0] == c0 and x[1] == loc for x in out):
                nxt = self._sph_cas_next(P3["cas"][c0], 1, q)
                if nxt is not None:
                    out.append([c0, int(loc), *nxt])
            self.sph_cas = out

    def _sph_cas_next(self, st, k, q):
        """The cascade's next step with an event from step k, and its window [lo, hi] in quarters (a step with no event,
        or one that cannot happen here, passes its own lag), or None at the end."""
        lo, hi = q, q
        while k < len(st):
            a, b = self.CAS_LAG.get(st[k][1], self.CAS_LAG["years"])
            lo, hi = lo + a, hi + b
            if st[k][0] >= 0:
                return [k, lo, hi]
            k += 1
        return None

    def _sph_pairs_q(self, T, s):
        """Phase 3 (sph_pairs): the ten pair faces of each town sphere (dynamics.json pair_faces). A pair's strength pi
        rises pair_rise a quarter while both its faces have held pair_share of the sphere for pair_quarters running, or
        while a body leading the sphere in town has a leader holding both colours at pair_person or more (then at once
        to .5 at least); it falls pair_decay a quarter otherwise. The pair holds pi x min(s1, s2), taken equally from
        both faces (the five shares stay; sph_ph is the layer people's teaching reads). The same thresholds for all ten
        pairs, ally and enemy alike (Canon rule 4). Later: the quarrel calm (pair_calm), its entry into the memory H after
        five strong years, and the faster fade after its founder leaves."""
        pr = T["pr"]; nl = self.n_loc; i1, i2 = T["pair_i"][:, 0], T["pair_i"][:, 1]
        if getattr(self, "sph_pi", None) is None:
            self.sph_pi = np.zeros((nl, 9, len(SPH_PAIRS))); self.sph_pq = np.zeros((nl, 9, len(SPH_PAIRS)), np.int64)
        s1, s2 = s[..., i1], s[..., i2]                                            # town x sphere x pair
        ok = (s1 >= pr["pair_share"]) & (s2 >= pr["pair_share"])
        self.sph_pq = np.where(ok, self.sph_pq + 1, 0)
        lp = self.inst_leader_pie                                                 # a two-coloured leader of a body here
        two = (lp[:, i1] >= pr["pair_person"]) & (lp[:, i2] >= pr["pair_person"])   # institution x pair
        il = np.asarray(self.inst_loc); isp = self.inst_sphere; on_ = (il >= 0) & (il < nl) & (isp >= 0)
        lead = np.zeros((nl, 9, len(SPH_PAIRS)), bool)
        np.logical_or.at(lead, (il[on_], isp[on_]), two[on_])
        cond = (self.sph_pq >= pr["pair_quarters"]) | lead
        pi = np.clip(np.where(cond, self.sph_pi + pr["pair_rise"], self.sph_pi - pr["pair_decay"]), 0, 1)
        self.sph_pi = np.where(lead, np.maximum(pi, 0.5), pi)
        if self.p.get("pair_calm", False):   # a pair face that held .5 or more and fell under .2 broke (8 quarters' flare)
            if getattr(self, "sph_ppk", None) is None:
                self.sph_ppk = np.zeros_like(self.sph_pi); self.sph_pbrk = np.full(self.sph_pi.shape, -1, np.int64)
            broke = (self.sph_pi < 0.2) & (self.sph_ppk >= 0.5)
            self.sph_pbrk = np.where(broke, int(self.t // 13) + 8, self.sph_pbrk)
            self.sph_ppk = np.where(self.sph_pi < 0.2, 0.0, np.maximum(self.sph_ppk, self.sph_pi))
        h = self.sph_pi * np.minimum(s1, s2)
        take = np.einsum("ljp,pc->ljc", h, T["pairA"])                            # what each face gives to its pairs
        f = np.minimum(1.0, s / np.maximum(take, 1e-12))                          # never more than the face holds
        self.sph_ph = h * np.minimum(f[..., i1], f[..., i2])

    def sph_teach_mix(self, town, teach):
        """The teaching mix of town spheres (n x 9 x 5 face shares, read through the per-sphere teach matrices), with the
        pair faces' layer when sph_pairs is on: what a pair holds leaves its two faces and teaches .4 of each of its two
        colours and .2 spread over the other three (dynamics.json pair_faces "does")."""
        tm = np.einsum("njf,jfc->njc", town[0], teach)
        if town[1] is None:
            return tm
        T = self._sph_tables(); ph = town[1]
        adj = town[0] - np.einsum("njp,pc->njc", ph, T["pairA"])
        return np.einsum("njf,jfc->njc", adj, teach) + 2 * np.einsum("njp,pc->njc", ph, T["pairT"])

    def _sph_fire(self, l, i, q, E, here=False, local=False):
        """Event i fires in town l (a big event: for the whole society): its rows start acting and step the sphere's own
        states (a big row on the society's, in every town; a local row on the town's: town l, or for an event with a big
        row the top third of towns by its hazard, at least one), its chains open their windows, the log and the
        last-fired table take it. here: a world-fired event with a town of its own (its local rows act there); local: the
        world's event was not big (every row acts in that town only, and only that town's moments open)."""
        nl = self.n_loc; sr = E["sr"]
        if self.p.get("sph_memory", False) or self.p.get("sph_cascades", False):
            self._sph_p3_fired(l, i, q, E, l if (local or not E["big"][i]) else -1)
        if local:                 # a world event that stays in its town (a local body's closure or scandal, a town's
            loc_t = every = np.array([l])                     # crime wave): every row acts there, as a local row
        elif E["big"][i]:
            k_ = max(1, int(np.ceil(nl / 3)))
            loc_t = np.array([l]) if here else np.argsort(-self._cache_evh[:, i], kind="stable")[:k_]
            every = np.arange(nl)
        else:
            loc_t = every = np.array([l])
        add = []
        for (ei, j, f, bg, tau, st) in E["rows"]:
            if ei != i:
                continue
            bg = bg and not local
            towns = every if bg else loc_t
            if f.any():
                add += [np.concatenate([[t_, j, q, tau], (E["sig"][1] if bg else E["sig"][0]) * f]) for t_ in towns]
            for s_, u_ in st:
                if bg:
                    self.sph_st_soc[s_] = min(1.0, max(0.0, self.sph_st_soc[s_] + sr["step"] * u_))
                else:
                    self.sph_st[towns, s_] = np.clip(self.sph_st[towns, s_] + sr["step"] * u_, 0, 1)
        if add:
            self.sph_ev_rows = np.vstack([self.sph_ev_rows, np.array(add)])
        if self.p.get("sph_shadow", False):   # N5: the row's shadow colours turn toward their shadow side there
            sh_ = self._sph_sh(); k_ = self._sh_par()["event_row"]
            for (ei, j, v, bg) in E["shrows"]:
                if ei == i:
                    tw_ = every if (bg and not local) else loc_t
                    sh_[tw_, j] = np.minimum(1.0, sh_[tw_, j] + k_ * v)
        for (a, b, lo, hi) in E["chains"]:
            if a == i:
                self.sph_ev_win[every, b, 0] = q + lo; self.sph_ev_win[every, b, 1] = q + hi
        self.sph_ev_last[every, i] = int(self.t)
        self.sph_ev_log = np.vstack([self.sph_ev_log, [[int(self.t), i, -1 if E["big"][i] and not local else l]]])

    def place_info(self, p):
        """A named place (flat index town x kind x N_PLACES, as People.hnt holds it): its town, kind, sphere, name number,
        five face shares (W U B R G) and leading face. Public, as the town portrait is."""
        import sphere_data as SD
        l, h, i = np.unravel_index(int(p), (self.n_loc, len(HAUNT_KINDS), N_PLACES))
        f = self.hp_s[l, h, i][np.argsort(self.perm)]; c = int(np.argmax(f)); sp = SPHERES[HAUNT_SPH[h]]
        sh_ = getattr(self, "pt_open", None) is not None and self.pt_open[l, h, i] >= 0   # place_turnover: an empty slot
        return dict(place=int(p), town=int(l), kind=HAUNT_KINDS[h], sphere=sp, name=int(self.hp_nm[l, h, i]),
                    faces=[round(float(x), 3) for x in f], leads=f"{sp}.{COLORS[c]}", leads_name=SD.FACE_NAMES[f"{sp}.{COLORS[c]}"],
                    **({"closed": True} if sh_ else {}))

    # ------------------------------------------------------------------ the spheres of society (item 15): Replace
    @property
    def inst_sphere(self):
        """Each institution's sphere (index into SPHERES); an employer by its sector (no sector: commerce)."""
        sph = INST_SPH[self.inst_kind]
        sec = np.asarray(self.inst_sector)
        return np.where(sph >= 0, sph, SECTOR_SPH[np.where(sec >= 0, sec, SECTORS.index("services"))])

    @property
    def sph_epoch(self):
        """The spheres' epoch for this world's setting (modern days for Earth)."""
        return self.SPH_EPOCH.get(self.cfg.get("setting", "earth"), "modern")

    EV_SPHERE = {("belief", None): "faith", ("era", None): "rule", ("place", "crime wave"): "prot",
                 ("place", None): "rule", ("nature", "pandemic"): "care", ("nature", "disaster"): "prot",
                 ("nature", None): "comm", ("abroad", "refugees arrive"): "gather", ("abroad", "world recession"): "comm",
                 ("abroad", None): "prot", ("state", None): "rule", ("economy", None): "comm", ("tech", None): "prod",
                 ("figure", None): "rule", ("culture", None): "gather"}

    def event_sphere(self, e):
        """The sphere a world event belongs to (item 15, phase 1d; spheres-implementation.md section 5, "Sphere events
        onto the world's events"): an institution's by its sphere, a law on drink in gathering, else by its domain and
        kind. Read only: the event itself is not changed. None for a domain with no sphere."""
        d, k = e.get("domain"), e.get("kind")
        if d == "institution":
            i = (e.get("value") or {}).get("inst") if isinstance(e.get("value"), dict) else None
            return SPHERES[int(self.inst_sphere[i])] if i is not None and 0 <= i < len(self.inst_kind) else None
        if d == "state" and k == "law changed" and e.get("key") == "alcohol":
            return "gather"
        return self.EV_SPHERE.get((d, k), self.EV_SPHERE.get((d, None)))

    def sphere_insts(self, sphere):
        """The institutions of one sphere (a name or an index), in their stored order."""
        return np.nonzero(self.inst_sphere == (SPH[sphere] if isinstance(sphere, str) else int(sphere)))[0]

    def state_parts(self, sphere=None):
        """The state by part ({part: {field: value}}), all parts or one sphere's; the force is that sphere's police
        and army, read with sphere_insts."""
        return {k_: {f_: getattr(self, f_) for f_ in STATE_PARTS[k_]} for k_, s_ in STATE_SPHERE.items()
                if sphere is None or s_ == sphere}

    # the arrays world-build.md names, as views of the state
    def snapshot(self):
        """The public state for the world panel: never pressure, hazards or odds (Emren 10:09)."""
        figs = [dict(id=i, female=bool(self.F_female[i]), born_t=int(self.F_born[i]), role=FIG_ROLES[self.F_role[i]],
                     party=int(self.F_party[i]), standing=round(float(self.F_standing[i]), 2), alive=bool(self.F_alive[i]))
                for i in sorted(set(self.fig_role_now.values()))]
        last = {}
        for e in reversed(self.record):
            if e["kind"] == "published" and e["key"] not in last:
                last[e["key"]] = e["value"]
            if len(last) == 2:
                break
        return dict(t=int(self.t), week_of_year=int(self.week_of_year), season=SEASONS[self.season],
                    era=None if self.era_key is None else dict(key=self.era_key, kind=ERA_KINDS[self.era_k],
                                                              idea=IDEAS[self.era_key][0], since_t=int(self.era_since)),
                    econ=dict(phase_published="recession" if self.rec_declared else "expansion",
                              unemp=last.get("unemployment"), infl=last.get("inflation"), housing=round(float(self.housing), 1)),
                    gov=dict(colors=[round(float(v), 2) for v in self.G], leader=int(self.fig), party=int(self.gov_party),
                             support=round(float(self.support), 2), next_election_t=int(self.t + 13 * self.next_vote)),
                    laws={k: LAW_STATES[int(s)] for k, s in zip(LAW_KEYS, self.laws)}, welfare=round(float(self.welfare_pub), 2),
                    rights={k: round(float(v), 1) for k, v in zip(RIGHTS, self.rights)}, war=WAR_STATES[self.war],
                    pandemic=PANDEMIC[self.pandemic], norms={k: float(v) for k, v in zip(NORM_KEYS, self.norm_pub)},
                    faiths=[round(float(v), 2) for v in self.faith_share], secular=round(float(self.secular), 2),
                    tech={k: round(float(a), 2) for k, a, e in zip(self.tech_keys, self.tech_adopt_v, self.tech_exists) if e},
                    figures=figs, regime="democracy" if self.regime >= 6 else "autocracy" if self.regime < -5 else "mixed",
                    **({"spheres": self._sph_portrait()} if getattr(self, "sph_s", None) is not None else {}))

    def _sph_portrait(self):
        """The town portrait (item 15, N3), public: per town each sphere's share of the hours and its five face shares
        (W U B R G, the canonical order), with the leading face. Never the pressures, drivers or hazards behind them."""
        import sphere_data as SD
        inv = np.argsort(self.perm); out = []
        for l in range(self.n_loc):
            sp = {}
            for j, s_ in enumerate(SPHERES):
                f = self.sph_s[l, j][inv]; c = int(np.argmax(f))
                sp[s_] = dict(hours=round(float(self.sph_Z[l, j]), 3), faces=[round(float(x), 3) for x in f],
                              leads=f"{s_}.{COLORS[c]}", leads_name=SD.FACE_NAMES[f"{s_}.{COLORS[c]}"])
            out.append(dict(town=int(l), spheres=sp))
        return out

    # ------------------------------------------------------------------------------------------------ save and load
    def save(self):
        """JSON-safe dict of the whole state (lists, floats, ints, strings); World.load(d) continues identically."""
        st = {}
        for k, v in self.__dict__.items():
            if k in self._CONST or k.startswith("_cache"):
                continue
            if isinstance(v, np.ndarray):
                st[k] = {"__nd__": str(v.dtype), "shape": list(v.shape), "data": v.reshape(-1).tolist()}
            elif isinstance(v, (np.floating, np.integer, np.bool_)):
                st[k] = v.item()
            elif isinstance(v, dict) and k == "fig_role_now":
                st[k] = {"__intkeys__": [[int(a), int(b)] for a, b in v.items()]}
            elif isinstance(v, tuple):
                st[k] = {"__tuple__": _jsafe(list(v))}
            elif isinstance(v, list) and v and isinstance(v[0], np.ndarray):
                st[k] = {"__ndlist__": [x.tolist() for x in v]}
            else:
                st[k] = _jsafe(v)
        rng = []
        for g in self.R:
            s = g.bit_generator.state
            rng.append(dict(bit_generator=s["bit_generator"], state={a: str(b) for a, b in s["state"].items()},
                            has_uint32=int(s["has_uint32"]), uinteger=str(s["uinteger"])))
        cfg, par = {k: v for k, v in self.cfg.items() if k != "legacy"}, dict(self.p)
        if not any(self.p.get(k, False) for k in SPH_RULES):   # spheres off: saved as v22.2 saved it
            par = {k: v for k, v in par.items() if k not in SPH_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in SPH_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self.p.get(k) for k in V224_RULES):     # v22.4's switches off: saved as v22.3 saved it
            par = {k: v for k, v in par.items() if k not in V224_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in V224_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self.p.get(k) for k in FIN_RULES):      # the finishing pack's switches off: saved as before
            par = {k: v for k, v in par.items() if k not in FIN_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in FIN_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self.p.get(k) for k in C_RULES):        # the C hooks off: saved without them
            par = {k: v for k, v in par.items() if k not in C_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in C_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self._s3(k) for k in S3_RULES):        # stage 3 off: saved as v22.1 saved it (load restores them)
            par = {k: v for k, v in par.items() if k not in S3_RULES + S3_PARAMS}
            cp_ = {k: v for k, v in (cfg.get("params") or {}).items() if k not in S3_RULES + S3_PARAMS}
            cfg = {k: v for k, v in cfg.items() if k != "params"}
            if cp_:
                cfg["params"] = cp_
        return dict(version=1, seed=self._seed, society=int(self.society_id), cfg=_jsafe(cfg),
                    params=_jsafe(par), perm=self.perm.tolist(), rng=rng, state=st)

    @classmethod
    def load(cls, d):
        params = dict(d["params"])
        for k in S3_RULES + SPH_RULES + V224_RULES:        # saved before stage 3, the spheres or v22.4: their rules stay off
            params.setdefault(k, False)
        for k in FIN_RULES:                                # saved before the finishing pack: its switches stay off
            params.setdefault(k, False)
        for k in C_RULES:                                  # saved before the C hooks: they stay off
            params.setdefault(k, None if k == "c_par" else False)
        W = cls(d["seed"], cfg=d["cfg"], color_perm=d["perm"], params=params, society=d.get("society", 0))
        for k, v in d["state"].items():
            if isinstance(v, dict) and "__nd__" in v:
                v = np.array(v["data"], dtype=v["__nd__"]).reshape(v["shape"])
            elif isinstance(v, dict) and "__intkeys__" in v:
                v = {int(a): int(b) for a, b in v["__intkeys__"]}
            elif isinstance(v, dict) and "__tuple__" in v:
                v = tuple(v["__tuple__"])
            elif isinstance(v, dict) and "__ndlist__" in v:
                v = [np.array(x) for x in v["__ndlist__"]]
            setattr(W, k, v)
        if len(d["rng"]) > len(W.R):                       # the spheres' stream, once a sphere rule has drawn
            W._sph_rng()
        if len(d["rng"]) > len(W.R):                       # place_turnover's own stream, once it has drawn
            W._pt_rng()
        for g, s in zip(W.R, d["rng"]):
            g.bit_generator.state = dict(bit_generator=s["bit_generator"], state={a: int(b) for a, b in s["state"].items()},
                                         has_uint32=s["has_uint32"], uinteger=int(s["uinteger"]))
        if getattr(W, "c5_prof", None) is not None:      # C5: the movements' colours (FPROF is rebuilt, not saved)
            W.FPROF[NF:] = W.c5_prof
        if "clim_t0" not in d["state"] and W.t > 0:        # saved before the climate anchor was kept: freeze it
            W.clim_t0 = int(W.t0)
        return W
