"""World's methods for the spheres of society: phases 1c and 2, the finishing pack's place_turnover, and phase 4.

Part of class World (world.py), which inherits SpheresMixin; moved out of world.py verbatim. A method here reads
module names through the imports below, the same objects world.py has, and self for everything on the World."""
import numpy as np
from world_keys import HAUNT_KINDS, INST_KINDS, SECTORS, SPHERES
from world_base import C, FUND_SPAN, HAUNT_SPH, K_PAT, LEAD_W, N_PLACES, SPH, SPH_PAIRS, _norm, _uclip, fair_tags


class SpheresMixin:
    # ------------------------------------------------------------------ the spheres of society (item 15): phase 1c
    # Each town's nine spheres: a size (its share of the town's waking hours) and five face shares (one per colour),
    # updated each quarter after _society_q (needs and demand are fresh) and before _figures_q. Read only: nothing in a
    # life reads it yet, and it draws no dice. Rules: chroma-world/spheres/data/dynamics.json (face_mix, size, drivers),
    # proposal chroma-ideas/spheres-implementation.md section 3, phase 1; the tables: sphere_data.py.
    SPH_EPOCH = {"earth": "modern", "tribal": "bands", "magic": "magic"}
    SPH_DRV_K = None

    def _sph_tables(self):
        """The sphere tables in this world's colour frame (permuted like _tables), made once (not saved)."""
        c_ = getattr(self, "_cache_sph", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        P_ = self.perm; pr = dict(SD.PARAMS, **(self.p.get("sph_par") or {})); ep = self.SPH_EPOCH.get(self.cfg.get("setting", "earth"), "modern")
        M0 = np.asarray(SD.M0[ep], float)[:, P_]
        if self.p.get("realm", "earth") != "earth":   # v25: a test realm (realm_neutral) may start every sphere at .2 a colour
            import world_fit as WF_
            if getattr(WF_.realm(self.p["realm"]), "SPH_M0_EVEN", False):
                M0 = np.full_like(M0, 0.2)
        D = np.array([SD.D[d] for d in SD.DRIVERS], float)[:, :, P_]            # 8 drivers x 9 spheres x 5 colours
        D = D - D.mean(1, keepdims=True)                                          # each colour's mean over the spheres out
        kd = dict(pr["k_drivers"], insecurity=pr["kQ"], plenty=pr["kO"])
        MEET = np.asarray(SD.MEETS, float)[:, P_, :]                              # 9 x 5 x (safety, belonging, meaning)
        sp = SD.SPHERES; ix = {s_: i_ for i_, s_ in enumerate(sp)}
        vec = lambda d_, dflt=0.0: np.array([float(d_.get(s_, dflt)) for s_ in sp])
        phi = np.zeros((9, 3))                                                    # under 15, 15 to 29, 65 and over
        for k_, v_ in pr["phi"].items():
            s_, a_ = (k_.split("<")[0], 0) if "<" in k_ else (k_[:-3], 2) if k_.endswith("65+") else (k_[:-5], 1)
            phi[ix[s_], a_] = v_
        alpha = np.zeros(9); alpha[ix["prod"]] = pr["alpha_prod"]
        c_ = dict(ep=ep, M0=M0, D=D, kd=np.array([kd[d] for d in SD.DRIVERS]), MEET=MEET,
                  MEETc=MEET - MEET.mean(1, keepdims=True), rho=vec(pr["rho"]), eps=vec(pr["eps"], 1.0),
                  beta=vec(pr["beta"]), zeta=vec(pr["zeta"]), alpha=alpha, phi=phi,
                  base=np.asarray(pr["base_share"][ep], float), mem=np.array([pr["drv_mem"]["war" if d == "war" else "others"]
                                                                         for d in SD.DRIVERS]),
                  war=(ix["prot"], ix["rule"]), plague=(ix["care"], ix["gather"]), pr=pr, n_drv=len(SD.DRIVERS))
        # phase 3: the joins' spill (N6), the year's rhythm (N7) and the pair faces, in this world's colour frame
        inv = np.argsort(P_); ci = {c_k: inv["WUBRG".index(c_k)] for c_k in "WUBRG"}
        pA = np.zeros((len(SPH_PAIRS), C)); pT = np.full((len(SPH_PAIRS), C), 0.2 / 3)
        for k_, pp in enumerate(SPH_PAIRS):
            pA[k_, [ci[pp[0]], ci[pp[1]]]] = 1.0; pT[k_, [ci[pp[0]], ci[pp[1]]]] = 0.4
        c_.update(Jsp=np.asarray(SD.J[ep], float) * (1 - float(SD.SEPARATION[ep])),
                  seas_h=np.array([SD.SEASONS["hours"][s_] for s_ in sp]), seas_z=np.array([SD.SEASONS["hazards"][s_] for s_ in sp]),
                  pairA=pA, pairT=pT, pair_i=np.array([[ci[pp[0]], ci[pp[1]]] for pp in SPH_PAIRS]))
        self._cache_sph = c_
        return c_


    def _sph_town_needs(self):
        """Each town's unmet needs (n_loc x 5), from the population groups of its place class (_society_q's
        group_unmet), with its own crime and disasters in place of its class's mean."""
        U = self.group_unmet; pl = self.gidx[2]; w = self.pop.reshape(-1)
        Uc = np.stack([(w[pl == k][:, None] * U[pl == k]).sum(0) / max(w[pl == k].sum(), 1e-12) for k in range(3)])
        PW = self._place_w(); lp = self.loc_place
        pc, pdis = PW @ self.loc_crime, PW @ np.minimum(self.loc_disaster, 1)
        Ut = Uc[lp].copy()
        Ut[:, 0] += 0.4 * (self.loc_crime - pc[lp]) + 0.3 * (np.minimum(self.loc_disaster, 1) - pdis[lp])
        return _uclip(Ut, 0, 1)

    def _sph_ages(self):
        """Each town's shares under 15, 15 to 29 and 65 and over (n_loc x 3), from its place class's groups."""
        pop = self.pop.sum(axis=(1, 3, 4))                                        # age band x place class
        pop = pop / np.maximum(pop.sum(0, keepdims=True), 1e-12)
        a3 = np.stack([pop[0], pop[1] + 0.5 * pop[2], pop[6] + pop[7]], 1)        # place class x 3
        return a3[self.loc_place]

    def _sph_drivers(self):
        """The eight drivers' levels in each town (n_loc x 8; dynamics.json drivers)."""
        nl = self.n_loc
        sec = self.security() - 0.4 * self.loc_crime - 0.3 * np.minimum(self.loc_disaster, 1) - 0.2 * (self.fear - self.p["fear0"])
        y = self.gap + (self.natural - self.loc_unemp) / 10 - (self.food + self.energy) / 6
        war = 0.5 * (self.war == 1) + 1.0 * (self.war == 2) + 0.2 * bool(np.any(self.ext_war))
        crowd = 100 * self.loc_growth + 50 * self.mig_in
        ineq = 5 * self.ineq
        school = self.loc_sectors[:, SECTORS.index("knowledge")]                 # proxy until the literate share is built
        media = self.inst_kind == INST_KINDS.index("media")
        expo = self.watch * (float(self.inst_capacity[media].mean()) if media.any() else 0.0)
        tv = np.asarray(self.tech_adopt_v, float); au = float(np.mean(self.automation)); tr = float(np.sum(self.ext_trade))
        last = getattr(self, "sph_chg_last", None)
        n_ = 0 if last is None else min(len(tv), len(last[0]))            # a new kind counts from its second quarter
        chg = 0.0 if last is None else (float(np.maximum(tv[:n_] - last[0][:n_], 0).sum()) + (au - last[1]) + (tr - last[2]))
        self.sph_chg_last = (tv.copy(), au, tr)
        chg += float(getattr(self, "norm_speed", 0.0))
        b = lambda x_: np.broadcast_to(np.asarray(x_, float), (nl,))
        return np.stack([-b(sec), b(y), b(war), b(crowd), b(ineq), b(school), b(expo), b(chg)], 1)   # insecurity: -sec

    def _sph_leaders(self):
        """Per town and sphere: the leaders' colour mix, their corruption and the bodies' age (capacity- and reach-
        weighted over the sphere's institutions in town, else the whole country's); has: whether the sphere has any."""
        nl = self.n_loc
        # a body with no reach beyond itself (a faith body, a party) still leads its own sphere: reach counts from .2
        A = (self.inst_sphere[:, None] == np.arange(9)[None]) * (self.inst_capacity * np.maximum(self.inst_reach, 0.2) + 1e-9)[:, None]
        B = (np.asarray(self.inst_loc)[:, None] == np.arange(nl)[None]).astype(float)        # institution x town
        X = np.concatenate([self.inst_leader_pie, self.inst_corruption[:, None], self.inst_age[:, None],
                            np.ones((len(A), 1))], 1)                                         # what is averaged, and 1
        loc = np.einsum("il,ij,ik->ljk", B, A, X)                                            # town x sphere x (5 + 3)
        nat = np.einsum("ij,ik->jk", A, X)[None]                                             # the whole country's
        has_l = loc[..., -1] > 1e-6
        tot = np.where(has_l[..., None], loc, nat)
        has = tot[..., -1] > 1e-6
        m = tot[..., :-1] / np.maximum(tot[..., -1:], 1e-12)
        Ld = np.where(has[..., None], m[..., :C], 0.2); corr = np.where(has, m[..., C], 0.0)
        age = np.where(has, m[..., C + 1], 50.0)
        return Ld, corr, age, has

    def _sphere_q(self):
        T = self._sph_tables(); pr = T["pr"]; nl = self.n_loc
        U = self._sph_town_needs(); un = U[:, [0, 1, 4]]                          # safety, belonging, meaning
        x_lvl = self._sph_drivers(); ages = self._sph_ages()
        tech = float(self.tech_adopt_v[self.tech_keys.index("internet")]) if "internet" in self.tech_keys else 0.0
        auto = float(np.mean(self.automation[[SECTORS.index("farm"), SECTORS.index("industry")]]))
        if getattr(self, "sph_s", None) is None:                                  # the first quarter: home ways, at rest
            self.sph_s = np.tile(T["M0"], (nl, 1, 1)); self.sph_ds = np.zeros((nl, 9, C)); self.sph_H = self.sph_s.copy()
            self.sph_Z = np.tile(T["base"], (nl, 1)); self.sph_need = un.copy(); self.sph_drv = x_lvl.copy()
            self.sph_ref = dict(ages=ages.copy(), tech=tech, auto=auto); self.sph_rat = np.ones(9)
        s, Z = self.sph_s, self.sph_Z
        # needs (N): gaps from the town's slow baseline, plus the pushback of what the town's spheres leave unmet
        e = un - self.sph_need
        sup = np.einsum("lj,ljc,jcn->ln", Z, s, T["MEET"]); sup0 = np.einsum("lj,jcn->ln", Z, 0.2 * T["MEET"])
        e = e + pr["kS"] * (sup0 - sup)
        self.sph_need += pr["need_mem"] * (un - self.sph_need)
        Nt = pr["kN"] * np.einsum("ln,jcn->ljc", e, T["MEETc"])
        # drivers (Q, O, T): each level against the town's memory of it, by the sphere's own projected weights
        x = _uclip(x_lvl - self.sph_drv, -1, 1)
        self.sph_drv += T["mem"] * (x_lvl - self.sph_drv); self.sph_x = x
        Tt = np.einsum("d,ld,djc->ljc", T["kd"], x, T["D"])
        Kt = pr["kK"] * (np.asarray(self.loc_mix, float) - 0.2)[:, None, :]     # the culture's lean in town
        Xt = self._sph_events_q(e) if self.p.get("sph_events", False) else 0.0   # phase 3: the events' fading shifts
        if self.p.get("sph_joins", False) and self.p.get("sph_events", False):   # N6: a shift spills to joined spheres
            Xt = Xt + np.einsum("jk,ljc->lkc", T["Jsp"], Xt)
        if self.p.get("sph_links", False) and self.p.get("sph_events", False):   # the links between spheres
            Xt = Xt + self._sph_links_q()
        Dm = T["M0"][None] * np.exp(Nt + Tt + Kt + Xt)
        Dm = Dm / Dm.sum(-1, keepdims=True)
        Ld, corr, age, has = self._sph_leaders()
        if self.p.get("sph_levers", False) and getattr(self, "sph_plead", None) is not None:   # lead: the lives leading
            pn = self.sph_plead[..., C]                                                       # a sphere in town join its
            Ld = np.where(pn[..., None] > 0, (Ld * has[..., None] + LEAD_W * self.sph_plead[..., :C])   # leaders' mix
                          / np.maximum(has[..., None] + LEAD_W * pn[..., None], 1e-9), Ld)
            has = has | (pn > 0)
        Lg = 1 - np.exp(-s / pr["sL"])
        ds = (T["rho"][None, :, None] * Lg * (Dm - s) + pr["mu"] * self.sph_ds
              + pr["aH"] * np.minimum(age, 100)[..., None] / 50 * (self.sph_H - s)
              + has[..., None] * pr["aL"] * (1 + pr["kOl"] * corr)[..., None] * (Ld - s)
              + pr["aA"] * U[:, 2][:, None, None] * (0.2 - s))
        s_new = np.maximum(s + ds, pr["s_min"]); s_new /= s_new.sum(-1, keepdims=True)
        self.sph_ds = s_new - s; self.sph_s = s_new
        if self.p.get("sph_levers", False) and getattr(self, "sph_fund", None):          # a patron's pull on the sphere
            self._sph_fund_q(place=False)
        if self.p.get("sph_shadow", False):
            self._sph_shadow_q()
        self.sph_H += pr["H_mem"] * (s_new - self.sph_H)
        if self.p.get("sph_pairs", False):
            self._sph_pairs_q(T, s_new)
        # sizes: hours by epoch base, income, budget, the town's ages and technology; war and plague jump, a war's
        # rise partly kept
        Yr = _uclip(1 + 0.01 * self.gap - 0.01 * (self.loc_unemp - self.natural), 0.5, 2.0)
        lz = (T["eps"][None] * np.log(Yr)[:, None] + T["beta"][None] * (self.welfare - self.p["welfare0"])
              + (ages - self.sph_ref["ages"]) @ T["phi"].T - T["alpha"][None] * (auto - self.sph_ref["auto"])
              + T["zeta"][None] * (tech - self.sph_ref["tech"]))
        jump = np.ones(9); wj = pr["war_jump"]; pj = pr["plague_jump"]
        if self.war == 2:
            jump[T["war"][0]], jump[T["war"][1]] = wj["prot"], wj["rule"]
        if self.pandemic == 2:
            jump[T["plague"][0]], jump[T["plague"][1]] = pj["care"], pj["gather"]
        if self.war == 2:
            kept = 1 + wj["ratchet_kept"] * (jump - 1)
            self.sph_rat = np.maximum(self.sph_rat, np.where(np.arange(9) == T["war"][0], kept, np.where(np.arange(9) == T["war"][1], kept, 1.0)))
        mult = np.maximum(jump, self.sph_rat)
        Zs = T["base"][None] * mult[None] * np.exp(lz); Zs /= Zs.sum(1, keepdims=True)
        kz = np.where(jump > 1.0001, 0.25, pr["kZ"])                              # a war or plague moves hours within a year
        self.sph_Z = Z + kz[None] * (Zs - Z)

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 2
    def _sph_rng(self):
        """The spheres' own dice stream ("sphere", after the world's other streams; world-fields.md), made the first
        time a sphere rule draws, so every other stream draws as before and a world with the rules off saves as before."""
        k = len(self._STREAMS)
        if len(self.R) == k:
            self.R.append(np.random.default_rng([self._seed + 104729, k] + ([self.society_id] if self.society_id else [])))
        return self.R[k]

    def _sph_places_q(self):
        """N1: each town's named places, N_PLACES per haunt kind (31), each with a face mix that follows its sphere's mix
        in town at the sphere's own speed (rho), leaning its own lasting way (hp_off, drawn once: a place is like itself,
        never like every place of its kind). hp_nm: a name number the Library's place names are read by."""
        T = self._sph_tables(); nl = self.n_loc; H = len(HAUNT_KINDS)
        base = self.sph_s[:, HAUNT_SPH][:, :, None, :]                            # town x kind x 1 x 5
        if getattr(self, "hp_off", None) is None:
            r = self._sph_rng(); sd = float(T["pr"].get("place_sd", 0.6))
            self.hp_off = r.normal(0, sd, (nl, H, N_PLACES, C))[..., self.perm]   # drawn in W U B R G, held in this frame
            if self.p.get("realm", "earth") != "earth":   # v25: a test realm's places may have no lasting lean (realm_neutral)
                import world_fit as WF_
                if getattr(WF_.realm(self.p["realm"]), "PLACE_FACES_EVEN", False):
                    self.hp_off = np.zeros_like(self.hp_off)
            self.hp_nm = r.integers(0, 1000, (nl, H, N_PLACES))
            self.hp_s = base * np.exp(self.hp_off); self.hp_s /= self.hp_s.sum(-1, keepdims=True)
        tgt = base * np.exp(self.hp_off); tgt /= tgt.sum(-1, keepdims=True)
        rho = T["rho"][HAUNT_SPH][None, :, None, None]
        if self.p.get("sph_levers", False) and getattr(self, "hp_hold", None) is not None:   # loyalty slows a place
            q = int(self.t // 13)
            rho = rho * np.where(self.hp_hold[..., 0] >= q, self.hp_hold[..., 1], 1.0)[..., None]
        self.hp_s += rho * (tgt - self.hp_s)
        if self.p.get("sph_levers", False) and getattr(self, "sph_fund", None):          # a patron's pull on a place
            self._sph_fund_q(place=True)

    # ------------------------------------------------------------------ spheres finishing pack, part 2 (place_turnover)
    # chroma-world/spheres/finish-pack-draft.md "Places close and open", values sphere_data.TURNOVER: each named place
    # closes with a quarterly hazard base(kind) / 4 x misfit x loss x hold x epoch (x the slump and dearth cascades on
    # owned trade while they run), and three town events close one place of their kind outright; the empty slot opens
    # again 2 to 6 quarters later (uniform) as a new place with a new name: the town sphere's mix with a fresh lean (hp_off,
    # drawn as the first places' were), or a founder's mix where a found act in that kind went well in the last 2 years.
    # Its own dice stream (after the spheres'), so switching it on moves no other draw; off, nothing of it exists.
    def _pt_rng(self):
        """place_turnover's own dice stream, made after the spheres' stream the first time it draws."""
        k = len(self._STREAMS) + 1
        self._sph_rng()
        if len(self.R) == k:
            self.R.append(np.random.default_rng([self._seed + 130363, k] + ([self.society_id] if self.society_id else [])))
        return self.R[k]

    def _pt_init(self):
        """The part's state, made the first time it is needed: pt_open (town x kind x slot) the quarter a closed slot
        opens again (-1: open); pt_log, every closing and opening (dicts: q, town, kind, slot, what closed / opened, why
        hazard / event:<key> / found / new, place, name); pt_exits [quarter, place] the known faces' exits (rung 2 or
        more); pt_found [quarter, town, kind, mix] the found acts that went well; pt_ev_i the sphere events read so far."""
        if getattr(self, "pt_open", None) is None:
            self.pt_open = np.full((self.n_loc, len(HAUNT_KINDS), N_PLACES), -1, np.int64)
            self.pt_log = []; self.pt_exits = []; self.pt_found = []
            self.pt_ev_i = len(getattr(self, "sph_ev_log", ()))

    def _pt_tables(self):
        """TURNOVER as arrays (made once, not saved): base a quarter by haunt kind (x the epoch), the owned trade kinds,
        the close events (event index: haunt kind index) and the cascades that raise owned trade (cascade id: x)."""
        c_ = getattr(self, "_cache_pt", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        TO = SD.TURNOVER
        ep = float(TO["epoch"].get(self.sph_epoch, 1.0))
        base = np.array([TO["base_y"][k_] for k_ in HAUNT_KINDS]) / 4.0 * ep
        trade = np.array([TO["group"][k_] == TO["cascade_group"] for k_ in HAUNT_KINDS])
        sk = {f"{e_['sphere']}.{e_['key']}": i_ for i_, e_ in enumerate(SD.EV)}   # the data names an event sphere.key
        close = {sk[k_]: (HAUNT_KINDS.index(h_), k_) for k_, h_ in TO["events_close"].items() if k_ in sk}
        c_ = self._cache_pt = dict(base=base, trade=trade, close=close, cas=dict(TO["cascades"]), TO=TO,
                                   vq=(int(TO["vacant_q"][0]), int(TO["vacant_q"][1])),
                                   sd=float(self._sph_tables()["pr"].get("place_sd", 0.6)))
        return c_

    def _pt_hazard(self, q):
        """This quarter's closing chance of every place (town x kind x slot): base / 4 x misfit x loss x hold x epoch x
        the running cascades on owned trade. misfit = 1 + k x max(0, TV(place, town sphere) - free); loss = 1 + per x the
        known faces who left the place by exit in the last 4 quarters, at most cap; hold = the loyalty lever's factor
        (hp_hold) while it lasts."""
        T = self._pt_tables(); TO = T["TO"]; nl = self.n_loc
        town = self.sph_s[:, HAUNT_SPH][:, :, None, :]
        tv = 0.5 * np.abs(self.hp_s - town).sum(-1)
        mis = 1 + TO["misfit_k"] * np.maximum(0.0, tv - TO["misfit_free"])
        ex = np.zeros(self.pt_open.size)
        for qe_, p_ in self.pt_exits:
            if q - qe_ < 4:
                ex[int(p_)] += 1
        loss = np.minimum(1 + TO["loss_per"] * ex.reshape(self.pt_open.shape), TO["loss_cap"])
        hz = T["base"][None, :, None] * mis * loss
        if self.p.get("sph_levers", False) and getattr(self, "hp_hold", None) is not None:
            hz = hz * np.where(self.hp_hold[..., 0] >= q, self.hp_hold[..., 1], 1.0)
        if self.p.get("sph_cascades", False) and getattr(self, "sph_cas", None):   # slump, war, disaster: x 1.5 on owned trade
            ids = self._sph_p3_tables()["ids"]; cf = np.ones(nl)
            for c_, lc_ in sorted({(ids[x[0]], int(x[1])) for x in self.sph_cas}):   # (each running cascade once)
                if c_ in T["cas"]:
                    if lc_ < 0:
                        cf = cf * T["cas"][c_]
                    else:
                        cf[lc_] *= T["cas"][c_]
            hz = hz * np.where(T["trade"][None, :, None], cf[:, None, None], 1.0)
        if getattr(self, "wa_keep", None):   # the world answers, B: a place a life there leads closes less often
            hz = np.array(hz, float); hz.reshape(-1)[list(self.wa_keep)] *= np.array(list(self.wa_keep.values()))
        return hz

    def _pt_close(self, l, h, i, q, why):
        lo_, hi_ = self._pt_tables()["vq"]
        self.pt_open[l, h, i] = q + int(self._pt_rng().integers(lo_, hi_ + 1))   # empty 2 to 6 quarters (uniform)
        p_ = int(np.ravel_multi_index((l, h, i), self.pt_open.shape))
        if getattr(self, "hp_hold", None) is not None:
            self.hp_hold[l, h, i] = [-1, 0.0]
        if getattr(self, "sph_fund", None):   # a patron's pull on the place ends with it
            self.sph_fund = [f_ for f_ in self.sph_fund if int(f_[2]) != p_]
        self.pt_log.append(dict(q=int(q), town=int(l), kind=HAUNT_KINDS[h], slot=int(i), what="closed", why=why, place=p_,
                                name=int(self.hp_nm[l, h, i])))

    def _pt_q(self):
        """Each quarter (place_turnover, after the places' mixes): the empty slots due open, the three events' closings
        (a place of their kind in the town the event fired in; a society's event, in its town of highest hazard; the
        place most at risk goes), then the hazard's."""
        self._pt_init(); T = self._pt_tables(); q = int(self.t // 13); r = self._pt_rng(); nl = self.n_loc
        self.pt_exits = [x for x in self.pt_exits if q - x[0] < 4]
        self.pt_found = [x for x in self.pt_found if q - x[0] < 8]
        # 1. the new places
        for l, h, i in zip(*np.nonzero((self.pt_open >= 0) & (self.pt_open <= q))):
            l, h, i = int(l), int(h), int(i)
            off = r.normal(0, T["sd"], C)[self.perm]                     # drawn in W U B R G, as the first places' were
            if self.p.get("realm", "earth") != "earth":   # v25: a test realm's new places have no lasting lean either
                import world_fit as WF_
                if getattr(WF_.realm(self.p["realm"]), "PLACE_FACES_EVEN", False):
                    off = np.zeros_like(off)
            old = int(self.hp_nm[l, h, i]); nm = old
            while nm == old:
                nm = int(r.integers(0, 1000))
            town = self.sph_s[l, HAUNT_SPH[h]]
            fd = [x for x in self.pt_found if x[1] == l and x[2] == h]
            if fd:   # the founder's mix (the latest found act that went well), held as its lasting lean
                self.hp_off[l, h, i] = 0.0; self.hp_s[l, h, i] = town
                self._sph_place_set(l, h, i, _norm(np.asarray(fd[-1][3], float)))
                self.pt_found = [x for x in self.pt_found if x is not fd[-1]]
            else:
                self.hp_off[l, h, i] = off
                m_ = town * np.exp(off); self.hp_s[l, h, i] = m_ / m_.sum()
            self.hp_nm[l, h, i] = nm; self.pt_open[l, h, i] = -1
            self.pt_log.append(dict(q=q, town=l, kind=HAUNT_KINDS[h], slot=i, what="opened", why="found" if fd else "new",
                                    place=int(np.ravel_multi_index((l, h, i), self.pt_open.shape)), name=nm))
        hz = self._pt_hazard(q)
        # 2. the events that close a place of their kind outright
        log = getattr(self, "sph_ev_log", None)
        if log is not None and len(log) > self.pt_ev_i:
            rows = np.asarray(log[self.pt_ev_i:]).tolist(); self.pt_ev_i = len(log)
            for _, ei_, l_ in rows:
                if int(ei_) not in T["close"]:
                    continue
                h, key_ = T["close"][int(ei_)]
                l = int(l_) if l_ >= 0 else int(np.argmax(self._cache_evh[:, int(ei_)]))
                op = np.nonzero(self.pt_open[l, h] < 0)[0]
                if len(op):
                    i = int(op[np.argmax(hz[l, h, op])])
                    self._pt_close(l, h, i, q, "event:" + key_)
        # 3. the hazard (one draw for every place, open or not, so the stream keeps its pace)
        u = r.random(hz.shape)
        for l, h, i in zip(*np.nonzero((u < hz) & (self.pt_open < 0))):
            self._pt_close(int(l), int(h), int(i), q, "hazard")

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 4
    def _sph_nudge(self, mix, toward, k):
        """A face mix moved k of the way toward toward (0..1 shares), kept over the floor and summing to 1."""
        m = np.maximum(mix + k * (toward - mix), 0.005)
        return m / m.sum()

    def _sph_place_set(self, l, h, i, new):
        """A place's face mix set to new, its lasting lean (hp_off) moved with it, so the change stays."""
        old = self.hp_s[l, h, i]
        self.hp_off[l, h, i] += np.log(np.maximum(new, 1e-9)) - np.log(np.maximum(old, 1e-9))
        self.hp_s[l, h, i] = new

    def sph_lever(self, loc, j, place, lever, ma, size, rung, rng, office="budget", span=None, went=1.0):
        """Phase 4 (sph_levers): a life's lever lands on its place (a flat place id, World.place_info) or, with place -1,
        on its town's sphere j (the caller passes the smaller size there). ma: the act's colours in this world's frame;
        size: reach / 3 x the rung's multiplier x how well it went; rung: 0 newcomer .. 4 leader. span: a fund act's
        quarters when the caller knows them (lead_ways: what is left of a leader's post), else FUND_SPAN by rung. Returns
        what moved (a word) for the record. went: how well the act went (place_turnover reads a found act that went well,
        .5 or more). dynamics.json levers' on_the_mix, as Outer world's answers read them."""
        if size <= 0 or getattr(self, "sph_s", None) is None:
            return "none"
        loc = int(loc); j = int(j); q = int(self.t // 13); ma = np.asarray(ma, float)
        hp_ok = place >= 0 and getattr(self, "hp_s", None) is not None
        if hp_ok:
            l, h, i = (int(x) for x in np.unravel_index(int(place), self.hp_s.shape[:3]))
        nP = int((HAUNT_SPH == j).sum()) * N_PLACES                            # places of the sphere in town
        town = self.sph_s[loc, j]
        def on_place(k_, toward):
            if hp_ok:
                new = self._sph_nudge(self.hp_s[l, h, i], toward, k_)
                d_ = new - self.hp_s[l, h, i]; self._sph_place_set(l, h, i, new)
                self.sph_s[loc, j] = self._sph_nudge(town, town + d_, 1.0 / max(nP, 1))
            else:
                self.sph_s[loc, j] = self._sph_nudge(town, toward, k_)
        away = np.maximum(2 * (self.hp_s[l, h, i] if hp_ok else town) - ma, 0.0)
        away = away / max(away.sum(), 1e-9)
        if lever == "voice":
            on_place(0.03 * size, ma)
        elif lever == "subvert":
            if self.p.get("sph_shadow", False):                                   # N5: feeds its shadow side
                sh_ = self._sph_sh(); c_ = int(np.argmax(ma))
                sh_[loc, j, c_] = min(1.0, sh_[loc, j, c_] + self._sh_par()["subvert"] * size)
            if rng.random() < 0.4:                                               # backfires 4 in 10
                on_place(0.02 * size, away); return "backfired"
            on_place(0.03 * size, ma)
        elif lever == "neglect":
            on_place(0.02 * size, town)
        elif lever == "exit":
            on_place(0.01 * size, away)
            if rung >= 2 and hp_ok:                                               # a known face's leaving is felt
                if self.p.get("place_turnover", False):                           # (and, part 2, raises its closing
                    self._pt_init(); self.pt_exits.append([q, int(place)])        # hazard for 4 quarters)
                lead_ = np.eye(C)[int(np.argmax(self.hp_s[l, h, i]))]
                self._sph_place_set(l, h, i, self._sph_nudge(self.hp_s[l, h, i], self.hp_s[l, h, i] - 0.02 * lead_ + 0.02 * town, 1.0))
        elif lever == "loyalty":
            if hp_ok:
                if getattr(self, "hp_hold", None) is None:
                    self.hp_hold = np.zeros(self.hp_s.shape[:3] + (2,)); self.hp_hold[..., 0] = -1
                self.hp_hold[l, h, i] = [q + 4, max(0.0, 1 - 0.1 * size)]
            else:
                return "none"
        elif lever == "found":
            top = np.argsort(-ma)[:2]
            face = np.zeros(C); face[top[0]] = 1.0
            if ma[top[1]] >= 0.26:                                                # a pair face: two colours of .26 or more
                face[top] = 0.5
            new = _norm(0.75 * face + 0.25 * town)
            hs_ = np.nonzero(HAUNT_SPH == j)[0]
            if getattr(self, "hp_s", None) is not None and len(hs_):
                if hp_ok and HAUNT_SPH[h] == j:
                    hs_ = np.array([h])
                cand = self.hp_s[loc, hs_].reshape(-1, C)                         # the place furthest from the founder
                dd_ = np.abs(cand - new).sum(1)
                pt_ = self.p.get("place_turnover", False)
                if pt_:   # part 2: a closed slot is not a place to found in; a found act that went well is kept 2 years
                    self._pt_init()   # (the next place to open in that kind, in that town, is the founder's)
                    dd_ = np.where(self.pt_open[loc, hs_].reshape(-1) >= 0, -np.inf, dd_)
                if np.isfinite(dd_).any():
                    k_ = int(np.argmax(dd_))
                    h2, i2 = int(hs_[k_ // N_PLACES]), k_ % N_PLACES
                    self._sph_place_set(loc, h2, i2, new)
                    if pt_ and went >= 0.5:
                        self.pt_found.append([q, int(loc), h2, [float(x) for x in new]])
                elif pt_ and went >= 0.5:   # every place of the kind closed: the founder's opens the first empty slot
                    self.pt_found += [[q, int(loc), int(h_), [float(x) for x in new]] for h_ in hs_]
            self.sph_s[loc, j] = self._sph_nudge(town, new, 1.0 / (nP + 1))
        elif lever == "fund":
            span = FUND_SPAN[min(int(rung), 4)] if span is None else int(span)
            if span <= 0:
                return "none"
            if not hasattr(self, "sph_fund") or self.sph_fund is None:
                self.sph_fund = []
            onp = hp_ok and rung < 3                                              # a pillar's endowment: the town sphere
            self.sph_fund.append([loc, j, int(place) if onp else -1, [float(x) for x in ma], float(size), q + span])
        elif lever == "office":
            return self._sph_office(loc, j, office, size, rng)
        elif lever == "lead":   # a leading post's act: open from "known" (one place) up; its colours pull the place like a
            if rung < 2:        # strong voice (v22.3; S7's posts and tenure take over in v22.4)
                return "none"
            on_place(0.05 * size, ma)
        else:
            return "none"
        return "moved"

    def _sh_par(self):
        """N5's numbers (dynamics.json shadow_state.share: start, relax, event_row, subvert, fairness_gap, comm_grey)."""
        import sphere_data as SD
        return SD.SHADOW["share"]

    def _sph_sh(self):
        """N5's shadow shares (town x sphere x colour, 0..1; made at the start value the first time they are needed)."""
        if getattr(self, "sph_sh", None) is None:
            self.sph_sh = np.full((self.n_loc, 9, C), self._sh_par()["start"])
        return self.sph_sh

    def _sph_shadow_q(self):
        """Phase 5, N5 (sph_shadow), each quarter: every shadow share relaxes .02 of the gap toward .1 and moves .01 x
        (.5 - the town's felt-fairness target in that sphere): a sphere that fails people grows its shadow, fair
        enforcement and trust shrink it; comm's also move .01 x (comm.grey - .5) (shadow_state.share)."""
        sh = self._sph_sh(); pr = self._sh_par()
        d = pr["relax"] * (pr["start"] - sh) + pr["fairness_gap"] * (0.5 - self.sph_fair_target())[..., None]
        E = self._sph_ev_tables()
        if getattr(self, "sph_st", None) is not None and "comm.grey" in E["own"]:
            k_ = E["own"].index("comm.grey")
            g_ = np.clip(self.sph_st[:, k_] + self.sph_st_soc[k_] - 0.5, 0, 1)
            d[:, SPH["comm"]] += pr["comm_grey"] * (g_ - 0.5)[:, None]
        self.sph_sh = np.clip(sh + d, 0, 1)

    def sph_grey(self):
        """N5's grey share of each town's spheres (town x sphere): the face-weighted shadow share, no dice."""
        sh = self._sph_sh() if self.p.get("sph_shadow", False) else np.full((self.n_loc, 9, C), self._sh_par()["start"])
        return (self.sph_s * sh).sum(-1)

    def sph_state(self, key):
        """One sphere state for each town (n_loc,): the town's plus the society's for its own states, the world's for the
        16 world states; .5 where the sphere events are off (phase 5's debts read comm.credit and prot.order)."""
        import sphere_data as SD
        E = self._sph_ev_tables(); st = getattr(self, "sph_st", None)
        if key in E["own"]:
            if st is None:
                return np.full(self.n_loc, 0.5)
            k = E["own"].index(key)
            return _uclip(st[:, k] + self.sph_st_soc[k] - 0.5, 0, 1)
        return self._sph_world_states(E)[:, list(SD.STATE_WORLD).index(key)]

    def sph_fair_target(self):
        """Phase 4 (sph_fair): where each town's felt fairness in each sphere settles (n_loc x 9), before a life's own acts
        and rung: .5 + .3 x (the sphere's fair-hearing states - .5) - .3 x (its against states - .5); a sphere with no
        against state of its own reads rule.favour at .15 (dynamics.json felt_fairness; Tyler 1990). States are the town's
        plus the society's (own) or the world's (the 16 world states); without the sphere events, own states read .5."""
        import sphere_data as SD
        E = self._sph_ev_tables(); nl = self.n_loc
        st = getattr(self, "sph_st", None)
        own = _uclip(st + self.sph_st_soc[None] - 0.5, 0, 1) if st is not None else np.full((nl, len(E["own"])), 0.5)
        ws = self._sph_world_states(E)
        def val(k):
            if k in E["own"]:
                return own[:, E["own"].index(k)]
            return ws[:, list(SD.STATE_WORLD).index(k)]
        out = np.full((nl, len(SPHERES)), 0.5)
        for j, sp in enumerate(SPHERES):
            d = SD.FAIR["states"].get(sp, {})
            fr = [val(k) for k in d.get("fair", [])]
            ag = d.get("against") or []
            if fr:
                out[:, j] += 0.3 * (np.mean(fr, 0) - 0.5)
            out[:, j] -= (0.3 if ag else 0.15) * (np.mean([val(k) for k in (ag or ["rule.favour"])], 0) - 0.5)
        return out

    def _sph_fair_terms(self, sp):
        """S1 (fair_read): the terms of sphere sp's fairness target as (key, coefficient, the towns' values), the same
        terms sph_fair_target adds: + .3 over its fair states, - .3 over its against states (none: rule.favour at .15)."""
        import sphere_data as SD
        E = self._sph_ev_tables(); nl = self.n_loc
        st = getattr(self, "sph_st", None)
        own = _uclip(st + self.sph_st_soc[None] - 0.5, 0, 1) if st is not None else np.full((nl, len(E["own"])), 0.5)
        ws = self._sph_world_states(E)
        def val(k):
            if k in E["own"]:
                return own[:, E["own"].index(k)]
            return ws[:, list(SD.STATE_WORLD).index(k)]
        d = SD.FAIR["states"].get(sp, {})
        fr = list(d.get("fair", [])); ag = list(d.get("against") or [])
        out = [(k, 0.3 / len(fr), val(k)) for k in fr]
        out += [(k, -(0.3 if ag else 0.15) / max(len(ag), 1), val(k)) for k in (ag or ["rule.favour"])]
        return out

    def fair_tags(self):
        """S1 (fair_read): the parts each fairness state and each sphere event reads (module fair_tags)."""
        return fair_tags()

    def sph_fair_parts(self):
        """S1 (fair_read): how each of the five parts of fairness (W the same rules for all, U the truth and the reasons,
        B their due, R respect and a say, G people who mean well by us) reads each town's sphere (n_loc x 9 x 5), as a
        step from .5. A state's term is split evenly among its parts (fair_parts); a part with states reads them at
        the number of parts present, and a part with none reads the sphere's whole step, so that the parts at .2 each
        (an even person) give exactly sph_fair_target's step. Each part is then centred on the parts' common mean over
        the towns and spheres (an even person's read stays the same)."""
        tags = fair_tags()
        out = np.zeros((self.n_loc, len(SPHERES), 5))
        for j, sp in enumerate(SPHERES):
            e = np.zeros((self.n_loc, 5)); has = np.zeros(5, bool)
            for k, c, v in self._sph_fair_terms(sp):
                ps = tags["parts"].get(k) or "WUBRG"
                for p in ps:
                    e[:, "WUBRG".index(p)] += c / len(ps) * (v - 0.5); has["WUBRG".index(p)] = True
            D = e.sum(1)
            out[:, j] = np.where(has[None], has.sum() * e, D[:, None])
        # Each part reads the society at the same level overall: the parts differ in where they find a body fair or
        # unfair, not in how fair the whole society looks to them (centred over the towns and spheres, keeping the
        # parts' mean, so an even person's read is unchanged); without it the parts whose states run high (the same
        # rules for all) made one colour's lives feel the whole society fairer (v22.4 refit: .054 apart by lead colour)
        m_ = out.mean((0, 1))
        return out - (m_ - m_.mean())[None, None]

    def _sph_fund_q(self, place):
        """The patrons' pulls this quarter (kPat .005 x size toward their colours), on places or on town spheres; a pull
        ends after its span."""
        q = int(self.t // 13)
        self.sph_fund = [f for f in self.sph_fund if f[5] >= q]
        for loc, j, p_, ma, size, _ in self.sph_fund:
            if place and p_ >= 0 and getattr(self, "hp_s", None) is not None:
                l, h, i = np.unravel_index(int(p_), self.hp_s.shape[:3])
                self._sph_place_set(l, h, i, self._sph_nudge(self.hp_s[l, h, i], np.asarray(ma), K_PAT * size))
            elif not place and p_ < 0:
                self.sph_s[loc, j] = self._sph_nudge(self.sph_s[loc, j], np.asarray(ma), K_PAT * size)

    def _sph_office(self, loc, j, kind, size, rng):
        """An office act on sphere j (kind ban, licence or budget; levers.office.events): with chance min(1, size) it
        fires that sphere's event for it in the town (its own rows; next quarter), or, where the sphere has none, moves
        the state by by x .05 x size."""
        import sphere_data as SD
        ent = SD.LEVER_OFFICE.get(SPHERES[j], {}).get(kind)
        if ent is None or rng.random() >= min(1.0, size):
            return "none"
        if "event" in ent:
            if not self.p.get("sph_events", False):
                return "none"
            self.fire_sphere_event(ent["event"], loc, big=False)
            return "fired " + ent["event"]
        E = self._sph_ev_tables()
        if ent["state"] in E["own"] and getattr(self, "sph_st", None) is not None:
            k_ = E["own"].index(ent["state"])
            self.sph_st[loc, k_] = min(1.0, max(0.0, self.sph_st[loc, k_] + ent["by"] * 0.05 * size))
            return "moved " + ent["state"]
        return "none"
