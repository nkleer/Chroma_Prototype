"""World's methods for nature, the C hooks (item 10) and abroad.

Part of class World (world.py), which inherits HooksMixin; moved out of world.py verbatim. A method here reads module
names through the imports below, the same objects world.py has, and self for everything on the World."""
import numpy as np
from world_keys import FEATURES, INST_KINDS, SPHERES
from world_base import (C, C_DEFAULT, FIG_ROLES, HAZARDS, NF, NM, PANDEMIC, SECTOR_GUILDS, WAR_STATES, WEEK_SEASON,
    _norm, _tv, _uclip)


class HooksMixin:
    # ------------------------------------------------------------------------------------------------ nature (spec 5 §2)
    def _warming_now(self):
        return {"low": 1.1, "middle": 1.2, "high": 1.3}.get(self.climate, 1.2)

    def _warming(self, t):
        """Degrees above pre-industrial. The scenario is anchored at the birth (t0): about 1.2 then, rising ~0.22 a
        decade and slowing as policy bites (middle path, IPCC AR6; Forster et al. 2023); before the birth it rises
        toward that value."""
        w0 = self._warming_now()
        r0, tau = {"low": (0.015, 35.0), "middle": (0.022, 70.0), "high": (0.03, 400.0)}.get(self.climate, (0.022, 70.0))
        y = (t - (self.clim_t0 if self.clim_t0 is not None else self.t0)) / 52.0
        if y >= 0:
            return w0 + r0 * tau * (1 - np.exp(-y / tau))
        return w0 * np.exp(y * r0 / w0)

    @staticmethod
    def _extremes(w):
        """How often extremes come against pre-industrial (flood fire quake storm heat). Hot extremes 2.8x at 1 degree,
        5.6x at 2 (IPCC AR6, 10-year events); heavy rain 1.3x and 1.7x; drought (fire) 1.7x and 2.4x; storms a little
        more; quakes unchanged."""
        return np.array([1 + .25 * w + .05 * w * w, 1 + .6 * w + .05 * w * w, 1.0, 1 + .15 * w + .05 * w * w,
                         1 + 1.3 * w + .5 * w * w])

    def _nature_q(self):
        p, r = self.p, self.R[1]
        x = r.random(8)
        self.warming = float(self._warming(self.t))
        self.extremes = self._extremes(self.warming)
        q_season = WEEK_SEASON[(self.t + 7) % 52]          # season in the middle of the coming quarter
        sf = np.array([[1.2, 1.2, .6, 1.0], [.2, .8, 2.2, .8], [1, 1, 1, 1], [1.5, .6, .6, 1.3], [0, .5, 3.3, .2]])[:, q_season]
        rate = self.loc_hazards * np.array(p["dis_base"]) * self.extremes * sf / 4 * self.pace
        if getattr(self, "land_hx", None) is not None:   # v25 wa_land: the hazards answer the land's state (world_land.py)
            rate = rate * self.land_hx
        draw = r.random(rate.shape)
        sev = r.random(rate.shape)
        when = r.random(rate.shape)
        hit = draw < rate
        self.loc_disaster = np.maximum(self.loc_disaster - 0.25, 0)
        for l, h in zip(*np.nonzero(hit)):                 # the coming quarter's disasters, each on its own week
            self.dis_pending.append([int(self.t + 1 + int(13 * when[l, h])), int(l), int(h), float(sev[l, h])])
        # price shocks (energy: war and new energy; food: heat and drought)
        eh = p["e_haz"] * (1 + 1.5 * (self.war == 1) + 4 * (self.war == 2) + 1.0 * self.ext_war.any()) * (0.7 if self._has_new("new energy") else 1.0)
        self.energy *= p["e_decay"]; self.food *= p["f_decay"]
        if x[0] < eh:
            self.energy += p["e_size"][0] + (p["e_size"][1] - p["e_size"][0]) * x[1]
            self._event("nature", "price shock", "energy", round(float(self.energy), 1), big=self.energy > 5)
        fh_ = self._c_par("drought_fhaz") if p.get("c4_nature") and getattr(self, "c4_dry", 0) > 0 else 1.0   # C4
        if x[2] < p["f_haz"] * (0.5 + 0.5 * self.extremes[4] / 2.8) * fh_:
            self.food += p["f_size"][0] + (p["f_size"][1] - p["f_size"][0]) * x[3]
            self._event("nature", "price shock", "food", round(float(self.food), 1), big=False)
        # pandemic: none, rising, peak, waning (about 2% a year for a severe one; Marani et al. 2021)
        ph = self.pandemic
        self.pand_q += 1
        if ph == 0 and x[4] < 1 - np.exp(-p["pand_haz"] / 4 * self.pace):
            self.pandemic, self.pand_q = 1, 0; self.pand_n += 1
        elif ph == 1 and self.pand_q >= 1 + (x[5] < 0.5):
            self.pandemic, self.pand_q = 2, 0
        elif ph == 2 and self.pand_q >= 2 + int(x[5] * 3):
            self.pandemic, self.pand_q = 3, 0
        elif ph == 3 and self.pand_q >= 2 + int(x[6] * 3):
            self.pandemic, self.pand_q = 0, 0
        if self.pandemic != ph:
            self._event("nature", "pandemic", PANDEMIC[self.pandemic], None, big=self.pandemic in (1, 2) or ph == 3)
        self.lockdown = 0.35 if self.pandemic == 2 else 0.15 if self.pandemic in (1, 3) else 0.0
        scar = (max(self.energy, 0) + max(self.food, 0)) / 6.0
        lh = np.log(np.maximum((self.loc_hazards * np.array(p["dis_base"]) * self.extremes).sum(1), 1e-4) / self.haz_ref)
        self.harsh_loc = _uclip(0.5 * lh, -1, 1.5) + 0.5 * np.minimum(self.loc_disaster, 1) + np.minimum(scar, 1.5)
        if p.get("c4_nature"):
            self._c4_nature_q(int(q_season))

    # ------------------------------------------------------------------ the C hooks (item 10), built by the Outer world
    # stage3-rules.md section 5. Each is off unless its switch is on; off, it draws nothing and adds nothing to the save.
    def _c_par(self, k):
        return (self.p.get("c_par") or {}).get(k, C_DEFAULT[k])

    def _c_rng(self, k):
        """A fresh generator for this quarter's draws of C hook k: keyed on the seed, the hook and the week, so it keeps
        no state to save and moves no other stream (the hooks' events are chance, so their dice stay: LW2 2e)."""
        return np.random.default_rng([self._seed + 104729, 7000 + int(k), int(self.t)] + ([self.society_id] if self.society_id else []))

    def _c4_nature_q(self, q_season):
        """C4, nature's own year: per place each quarter, a season of bad air (cities, industry), bad water or a poisoned
        river (industry, mining), a dry year (farming and hotter places, drawn in summer), a glorious spring (everywhere,
        drawn in spring) and the recovery after a disaster. Rates are yearly, at the birth's climate, times the pace."""
        nl, t, c = self.n_loc, int(self.t), self._c_par
        if getattr(self, "c4_ill", None) is None:          # made on the first quarter the hook runs, so a world with it off
            self.c4_ill = np.ones(nl)                      # saves nothing of it
            self.c4_ill_to = np.zeros(nl, np.int64)
            self.c4_air_t = np.full(nl, -9999, np.int64)
            self.c4_dis = self.loc_disaster >= 1
            self.c4_dry = 0
        self.c4_dry = max(int(self.c4_dry) - 1, 0)
        x = self._c_rng(4).random((nl, 5))
        ft = lambda f: self.loc_feat[:, FEATURES.index(f)]
        ref = self._extremes(self._warming_now())          # the birth's extremes: the start rates hold there
        hz = self.loc_hazards[:, HAZARDS.index("heat")]
        hot = hz > hz.mean()
        pace = self.pace

        def ill(l, k, weeks):
            on = self.c4_ill_to[l] > t
            self.c4_ill[l] = max(self.c4_ill[l], k) if on else k
            self.c4_ill_to[l] = max(self.c4_ill_to[l], t + weeks)

        heat = 1 + c("air_heat") * (self.extremes[4] / ref[4] - 1)
        air = (ft("city") | ft("industry")) & (t - self.c4_air_t >= 52) & (x[:, 0] < c("air") / 4 * max(heat, 0) * pace)
        for l in np.nonzero(air)[0]:
            self.c4_air_t[l] = t
            ill(l, c("air_ill"), 13)
            self._event("nature", "bad air", None, dict(loc=int(l)), big=False)
        dirty = ft("industry") | ft("mining")
        for l in np.nonzero(dirty)[0]:
            if x[l, 1] < c("river") / 4 * pace:
                kind, k_, w_ = "poisoned river", c("river_ill"), 26
            elif x[l, 1] < (c("river") + c("water")) / 4 * pace:
                kind, k_, w_ = "bad water", c("water_ill"), 13
            else:
                continue
            self.loc_services[l] = np.maximum(self.loc_services[l] - c("water_serv"), 0.05)   # each class's
            ill(l, k_, w_)
            self._event("nature", kind, None, dict(loc=int(l)), big=False)
        if q_season == 2:                                  # the dry year shows in summer
            dry = (ft("farming") | hot) & (x[:, 2] < c("drought") * self.extremes[1] / ref[1] * pace)
            if dry.any():
                share = float(self.loc_pop_share[dry].sum())
                self.food += self.p["f_size"][0] * c("drought_food") * min(1.0, 3 * share)
                self.c4_dry = 2                            # the food shock's chance doubles for this quarter and the next
            for l in np.nonzero(dry)[0]:
                self.loc_services[l] = np.maximum(self.loc_services[l] - c("drought_serv"), 0.05)
                self._event("nature", "drought", None, dict(loc=int(l), farming=bool(ft("farming")[l])), big=False)
        if q_season == 1:                                  # a glorious spring
            for l in np.nonzero(x[:, 3] < c("spring") * pace)[0]:
                self._event("nature", "glorious spring", None, dict(loc=int(l), farming=bool(ft("farming")[l])), big=False)
        hit = self.loc_disaster >= 1                       # a disaster's active years end: the town builds itself back
        for l in np.nonzero(self.c4_dis & ~hit)[0]:
            cn = (self.inst_kind == INST_KINDS.index("council")) & (self.inst_loc == l)
            self.inst_capacity[cn] = np.maximum(self.inst_capacity[cn] - c("rec_cost"), 0.05)
            self._event("nature", "recovery", None, dict(loc=int(l)), big=False)
        self.c4_dis = hit

    def _c5_state(self):
        """C5's own state, made the first year the hook runs (a world with it off saves none of it)."""
        if getattr(self, "c5_prof", None) is None:
            self.c5_prof = np.full((NM, C), 0.2)            # each slot's colours, fixed for the movement's life
            self.c5_on = np.zeros(NM, bool)                 # a living movement holds the slot
            self.c5_born = np.zeros(NM, np.int64)           # the founding week
            self.c5_ceil = np.zeros(NM)                     # the share its growth heads for
            self.c5_fade = np.zeros(NM)                     # years from the founding until a failing one fades (0: it lasts)
            self.c5_parent = np.full(NM, -1, np.int64)      # the tradition it came from (-1: spiritual but secular)
            self.c5_loc = np.full(NM, -1, np.int64)         # the town it was founded in
            self.c5_fig = np.full(NM, -1, np.int64)         # its founder, a public figure
            self.c5_reach = np.ones(NM)                     # its growth scale (a founder's reach, c5_found_by)
            self.c5_tense = np.zeros((NF + NM, NF + NM), bool)   # pairs of faiths in a tense stretch
            self.c5_found_t, self.c5_found_l = -9999, -1    # the last founding: week and town (the founding gate)

    def faith_open(self, min_share=None):
        """Faiths a person can take up: the traditions, and C5's living movements holding min_share of the people
        (default join_share)."""
        nf = self._nf()
        ok = np.arange(nf) < NF
        if nf > NF and getattr(self, "c5_on", None) is not None:
            ms = self._c_par("join_share") if min_share is None else min_share
            ok[NF:] = self.c5_on & (np.asarray(self.faith_share)[NF:] >= ms)
        return ok

    def living_faiths(self):
        """C5's movement slots as the Faith sphere's "living faiths" (read only): each living movement's slot, faith
        index, share of the people, colours (W U B R G), founding week and town, parent tradition and founder."""
        if getattr(self, "c5_prof", None) is None:
            return []
        inv = np.argsort(self.perm)
        return [dict(slot=int(k), faith=NF + int(k), share=round(float(self.faith_share[NF + k]), 4),
                     colours=[round(float(v), 3) for v in self.c5_prof[k][inv]], born=int(self.c5_born[k]),
                     town=int(self.c5_loc[k]), parent=int(self.c5_parent[k]), founder=int(self.c5_fig[k]),
                     lasting=bool(self.c5_fade[k] == 0))
                for k in np.nonzero(self.c5_on)[0]]

    def c5_founding(self, loc):
        """C5's founding gate per person (earth_rules INNER "a following of your own"): a movement founded in the
        person's town within found_open weeks (the founding took a free slot)."""
        loc = np.asarray(loc)
        if getattr(self, "c5_prof", None) is None or self.t - int(self.c5_found_t) >= self._c_par("found_open"):
            return np.zeros(loc.shape, bool)
        return loc == int(self.c5_found_l)

    def c5_found_by(self, pie, reach=1.0):
        """C5: the person founds the movement founded in their town (the option of "a following of your own"): its
        colours become the founder's own and its growth scales with their reach (1 typical). For the Engine to call."""
        if getattr(self, "c5_prof", None) is None or self.t - int(self.c5_found_t) >= self._c_par("found_open"):
            return -1
        k = int(np.argmax(np.where(self.c5_on, self.c5_born, -1)))
        self.c5_prof[k] = _norm(np.asarray(pie, float)); self.c5_reach[k] = float(max(reach, 0.1))
        self.FPROF[NF + k] = self.c5_prof[k]
        return k

    def _c5_move(self, src, dst, amount):
        """Move a share of all the people from faith column src to dst (0 secular, 1.. faiths), group by group in
        proportion to src's own groups; returns the share moved."""
        m = self.pop[..., src, :]
        tot = float(m.sum())
        a = min(float(amount), tot)
        if a <= 0:
            return 0.0
        mv = m * (a / tot)
        self.pop[..., src, :] -= mv; self.pop[..., dst, :] += mv
        return a

    def _c5_y(self):
        """C5, new faith movements (stage3-rules.md section 5): founding, growth, fading, claims and tension, once a
        year after the belief year. Invented movements only; conflict is told indirectly."""
        self._c5_state()
        c, t = self._c_par, int(self.t)
        x = self._c_rng(5).random(16 + 2 * (NF + NM) ** 2)   # 0-7 founding, 8.. claims, 16.. tension
        fs = self.pop.sum((0, 1, 2, 4))                     # 0 secular, 1.. faiths
        # founding
        U = getattr(self, "group_unmet", None)
        free = np.nonzero(~self.c5_on)[0]
        if U is not None and len(free):
            exc = max(float(self.unmet_mean[4] - self.need_base[4]), 0.0)
            pf = c("found") * (1 + c("found_mean") * exc) * (1 + c("found_speed") * float(getattr(self, "norm_speed", 0.0))) * self.pace
            if x[0] < pf:
                k = int(free[0])
                par = int(np.argmax(fs[1:])) if fs[1:].max() >= fs[0] else -1
                pp = self.FPROF[par] if par >= 0 else self.V
                size = self.pop.reshape(-1) * self.gadult
                want = _norm(self.gmix + self.p["zeta"] * (U @ self.NEEDM))
                wm = size * U[:, 4] ** 3
                prof = _norm(0.5 * (wm[:, None] * want).sum(0) / max(wm.sum(), 1e-12) + 0.5 * pp)
                ok = x[2] < c("succeed")
                l = int(min(np.searchsorted(np.cumsum(self.loc_pop_share) / self.loc_pop_share.sum(), x[1]), self.n_loc - 1))
                self.c5_prof[k], self.c5_on[k], self.c5_born[k] = prof, True, t
                self.c5_ceil[k] = (c("ceil_lo") + (c("ceil_hi") - c("ceil_lo")) * x[3]) if ok else (c("fail_lo") + (c("fail_hi") - c("fail_lo")) * x[3])
                self.c5_fade[k] = 0.0 if ok else c("fade_y0") + (c("fade_y1") - c("fade_y0")) * x[4]
                self.c5_parent[k], self.c5_loc[k], self.c5_reach[k] = par, l, 1.0
                self.c5_found_t, self.c5_found_l = t, l
                self.FPROF[NF + k] = prof
                self._c5_move(par + 1, NF + 1 + k, 0.5 * c("seed_share"))
                self._c5_move(0, NF + 1 + k, 0.5 * c("seed_share"))
                # its founder, a public figure outside the roles (no seat to fill; the figure lives on in the record)
                fid = len(self.F_role)
                self.F_role.append(FIG_ROLES.index("preacher")); self.F_pie.append(_norm(prof * np.exp(0.25 * self._cn(self._c_rng(6)))).tolist())
                self.F_standing.append(float(0.1 + 0.1 * x[5])); self.F_alive.append(True); self.F_party.append(-1)
                self.F_born.append(int(t - (30 + 20 * x[6]) * 52)); self.F_female.append(bool(x[7] < 0.5)); self.F_mom.append(0.05)
                self.F_active.append(True); self.F_inst.append(-1)
                self.c5_fig[k] = fid
                self._event("belief", "new movement", None, dict(slot=k, loc=l, parent=par, fig=fid), big=False)
                self.fire_sphere_event("new_teaching", l)  # its sphere event (world-fired: faith.new_teaching)
        # growth, fading, claims, freeing
        fs = self.pop.sum((0, 1, 2, 4))
        for k in np.nonzero(self.c5_on)[0]:
            col, par = NF + 1 + int(k), int(self.c5_parent[k]) + 1
            s_ = float(fs[col]); age = (t - int(self.c5_born[k])) / 52.0
            failing = self.c5_fade[k] > 0
            if failing and age >= self.c5_fade[k]:
                ds = -c("fade") * s_
            else:
                ds = c("grow") * self.c5_reach[k] * s_ * (1 - s_ / self.c5_ceil[k]) * self.pace
            if ds > 0:
                got = self._c5_move(par, col, 0.5 * ds) if par > 0 else 0.0
                self._c5_move(0, col, ds - got)
                if x[8 + k] < c("claims") and age > 0 and s_ < 0.9 * self.c5_ceil[k]:   # while it still grows
                    self._event("belief", "claims spread", None, dict(slot=int(k), loc=int(self.c5_loc[k])), big=False)
            elif ds < 0:
                self._c5_move(col, par, -0.5 * ds); self._c5_move(col, 0, -0.5 * ds)
            s_ = float(self.pop[..., col, :].sum())
            if (s_ < c("free_share") and age >= c("free_y")) or (failing and age >= c("fail_y")):
                self._c5_move(col, par, 0.5 * s_); self._c5_move(col, 0, s_)
                self.pop[..., col, :] = 0.0
                self._event("belief", "movement fades", None, dict(slot=int(k), years=round(age, 1)), big=False)
                self.c5_on[k] = False; self.c5_prof[k] = 0.2; self.FPROF[NF + k] = 0.2
                self.c5_tense[NF + k, :] = False; self.c5_tense[:, NF + k] = False
        self.faith_share = self.pop.sum((0, 1, 2, 4))[1:].copy()
        # tension between two faiths: both over 5%, far apart, trust low; told indirectly, in a town
        sh = self.faith_share
        alive = self.faith_open(0.0)
        big_ = alive & (sh > c("tension_share"))
        cum = np.cumsum(self.loc_pop_share) / self.loc_pop_share.sum()
        nn = (NF + NM) ** 2
        for i in range(NF + NM):
            for j in range(i + 1, NF + NM):
                xr, xl = x[16 + i * (NF + NM) + j], x[16 + nn + i * (NF + NM) + j]
                on = bool(big_[i] and big_[j] and _tv(self.FPROF[i], self.FPROF[j]) > c("tension_tv") and self.trust < c("tension_trust"))
                start = on and not self.c5_tense[i, j]
                self.c5_tense[i, j] = on
                if start or (on and xr < c("tension_p")):
                    l = int(min(np.searchsorted(cum, xl), self.n_loc - 1))
                    self._event("belief", "faith tension", None, dict(faiths=[i, j], loc=l, start=start), big=False)

    # C3's sphere events (spheres-phase3-answers.md section 1; the relay of 10-10 01:00 UTC): a closure averted by the
    # state is the sphere's closure, a leak its exposure; sold and merged are words only. Ordinary closures and scandals
    # are mapped in _sph_wf_key, so only these new events call fire_sphere_event. big as for the world event: a town
    # body's leak stays in its town, a national one's acts for the whole society (fire-big, Engine #78)
    C3_SPH = {"nationalised": {"prod": "works_close", "comm": "lender_fails"},
              "leak": {"rule": "favour_exposed", "care": "neglect_scandal", "faith": "scandal"}}

    def _c3_sph(self, i, kind, big):
        key = self.C3_SPH.get(kind, {}).get(SPHERES[int(self.inst_sphere[i])])
        if key is not None:
            self.fire_sphere_event(key, int(self.inst_loc[i]), big=big)

    def _c3_state(self):
        """C3's own state, made the first quarter the hook runs (a world with it off saves none of it)."""
        if getattr(self, "c3_cover", None) is None:
            self.c3_cover = np.zeros(self.n_inst, np.int64)   # the week a hidden cover-up would surface by itself
            self.c3_break = np.zeros(self.n_inst, bool)       # an insider spoke up this quarter

    def _c3_nationalise(self, close):
        """C3 nationalised: a big firm or bank about to close in a deep recession becomes a public body (half of them,
        where the state's capacity is .5 or more); it then drifts toward the government as public bodies do."""
        self._c3_state()
        c = self._c_par
        deep = self.phase == 1 and self.severity >= 1 and self.capacity >= c("nat_cap")
        if not deep:
            return close
        x = self._c_rng(30).random(self.n_inst)
        nat = close & self.inst_firm & (self.inst_level == 2) & (x < c("nat_share"))
        K_ = {k_: INST_KINDS.index(k_) for k_ in ("employer", "bank")}
        for i in np.nonzero(nat)[0]:
            self.inst_public[i] = True; self.inst_firm[i] = False
            self.inst_pubemp[i] = self.inst_kind[i] == K_["employer"]
            self.inst_finances[i] = 0.5
            self._inst_event(i, "nationalised", big=True)
            self._c3_sph(i, "nationalised", big=True)
        return close & ~nat

    def _c3_inst_q(self, close):
        """C3, institution events (stage3-rules.md section 5): sold, merged, a leak and a cover-up, each quarter at a
        quarter of the yearly start rates. Each is recorded with _inst_event; scandals and closures stay as built, and
        the spheres read them as their own events (spheres-phase3-answers.md, world-fired)."""
        self._c3_state()
        n, t, c = self.n_inst, int(self.t), self._c_par
        r = self._c_rng(3); x = r.random((n, 6)); nz = r.normal(size=(n, C))
        k = self.inst_kind; K_ = {k_: INST_KINDS.index(k_) for k_ in INST_KINDS}
        free = ~close
        ls_ = self.p["lead_spread_s3"] if self._s3("hist_chance_only") else 0.3
        size = self.inst_level * 2.0 + self.inst_capacity                 # who is the bigger of two firms
        # sold: a private firm or bank changes hands; new owners bring their own leader and the sector's big ways
        sold = free & self.inst_firm & (x[:, 0] < c("sold") / 4 * np.where(self.inst_finances < 0.3, c("sold_poor"), 1.0))
        for i in np.nonzero(sold)[0]:
            peers = np.nonzero(self.inst_firm & (self.inst_sector == self.inst_sector[i]) & (np.arange(n) != i))[0]
            if len(peers):
                j = peers[int(np.argmax(size[peers]))]
                self.inst_profile[i] = _norm(self.inst_profile[i] + c("sold_pull") * (self.inst_profile[j] - self.inst_profile[i]))
            if self.inst_leader_fig[i] < 0:
                self.inst_leader_q[i] = 0; self.inst_leader_pie[i] = _norm(self.V * np.exp(ls_ * nz[i]))
            self._inst_event(i, "sold", big=bool(self.inst_level[i] == 2))
        # merged: the smaller of two firms of one sector in one place is folded into the bigger; its slot is a new firm
        emp = free & ~sold & self.inst_firm & (k == K_["employer"])
        done = np.zeros(n, bool)
        for i in np.nonzero(emp & (x[:, 1] < c("merged") / 4))[0]:
            if done[i]:
                continue
            rivals = np.nonzero(emp & ~done & (self.inst_sector == self.inst_sector[i]) & (self.inst_loc == self.inst_loc[i])
                                & (np.arange(n) != i))[0]
            if not len(rivals):
                continue
            j = rivals[int(np.argmax(size[rivals]))]
            small, big = (i, j) if size[i] <= size[j] else (j, i)
            done[[small, big]] = True
            self._event("institution", "merged", INST_KINDS[k[small]], dict(inst=int(small), into=int(big),
                        loc=int(self.inst_loc[small]), gen=int(self.inst_gen[small])), big=False)
            sec = int(self.inst_sector[small]) if self.inst_sector[small] >= 0 else 2
            g = SECTOR_GUILDS[sec][int(x[small, 5] * len(SECTOR_GUILDS[sec]))]
            self.inst_native[small] = self._profile_src(g); self.inst_profile[small] = self.inst_native[small].copy()
            self.inst_finances[small], self.inst_age[small], self.inst_gen[small] = 0.5, 0.0, self.inst_gen[small] + 1
            self.inst_corruption[small], self.inst_legitimacy[small], self.inst_leader_q[small] = 0.1, self.inst_legit0[small], 0
            self.inst_leader_pie[small] = _norm(self.V * np.exp(ls_ * nz[small]))
            self._inst_event(small, "new firm", big=False)
        # a leak: private files get out, more where nearly everyone is online and the body is weak
        net = float(self.tech_adopt("internet")) if "internet" in self.tech_keys else 0.0
        lk_k = np.isin(k, [K_[k_] for k_ in ("hospital", "council", "ministry")]) | self.inst_firm
        leak = free & lk_k & (x[:, 2] < c("leak") / 4 * (0.5 + net) * np.maximum(1.5 - self.inst_capacity, 0))
        for i in np.nonzero(leak)[0]:
            self.inst_legitimacy[i] = max(self.inst_legitimacy[i] - c("leak_legit"), 0.02)
            self.trust = max(self.trust - c("leak_trust"), 0.02)
            big = bool(self.inst_level[i] == 2)
            self._inst_event(i, "leak", big=big)
            self._c3_sph(i, "leak", big=big)
        # a cover-up: money, safety checks, records or negligence (never harm to children or sexual violence); hidden,
        # it is not on the record; its staff know
        cv_k = np.isin(k, [K_[k_] for k_ in ("hospital", "bank", "council", "police", "faith body")])
        cov = free & cv_k & (self.c3_cover <= t) & (x[:, 3] < (c("cover") + c("cover_c") * self.inst_corruption) / 4)
        for i in np.nonzero(cov)[0]:
            yrs = c("cover_y0") + (c("cover_y1") - c("cover_y0")) * x[i, 4]
            self.c3_cover[i] = t + int(52 * yrs)
            subj = ("money", "safety checks", "records", "negligence")[int(x[i, 5] * 4) % 4]
            self._event("institution", "cover-up", INST_KINDS[k[i]], dict(inst=int(i), loc=int(self.inst_loc[i]),
                        gen=int(self.inst_gen[i]), subject=subj), big=False, public=False)

    def c4_illness(self):
        """C4: each place's multiplier on illness (bad air, bad water, a poisoned river), or None with the hook off."""
        if getattr(self, "c4_ill", None) is None:
            return None
        return np.where(self.c4_ill_to > self.t, self.c4_ill, 1.0)

    def _strike(self):
        """Disasters drawn for this week strike: the locality's recovery, its services, the record, disaster_now."""
        due = [d for d in self.dis_pending if d[0] <= self.t]
        if not due:
            return
        self.dis_pending = [d for d in self.dis_pending if d[0] > self.t]
        for _, l, h, sv in due:
            self.loc_disaster[l] = max(self.loc_disaster[l], 1.0 + 2.0 * sv)
            self.loc_services[l] *= 1 - 0.1 * sv
            if max(sv, 0.01) > self.disaster_now[l]:
                self.disaster_now[l], self.disaster_kind[l] = max(sv, 0.01), h
            self._event("nature", "disaster", HAZARDS[h], dict(loc=int(l), severity=round(float(sv), 2)), big=bool(sv > 0.9))
        self.dis_on = True

    # ------------------------------------------------------------------------------------------------ abroad (spec 5 §5)
    def _ext_q(self):
        p, r = self.p, self.R[2]
        n = self.n_ext
        x = r.random((n, 10)); xw = r.random(6); nz = self._cn(r, n)
        # world cycle: a global recession about once a decade, lasting about 3 quarters (estimate)
        if self.world_rec:
            self.world_q += 1
            if xw[0] < 0.35: self.world_rec = 0
        elif xw[0] < 0.025 * self.pace:
            self.world_rec, self.world_q = 1, 0
            self._event("abroad", "world recession", None, None, big=False)
        # neighbours' cycles: own hazard, the world, contagion from home along trade
        home_hit = float(self.phase == 1 and self.rec_q <= 2)
        haz = (0.02 + 0.004 * self.ext_exp_q / 4 + 0.08 * self.world_rec + 0.3 * self.ext_trade * home_hit) * self.pace
        rec = self.ext_phase == 1
        start = ~rec & (x[:, 0] < haz)
        end = rec & (x[:, 1] < 1 / 3.5) & (self.ext_rec_q >= 2)
        self.ext_phase = np.where(start, 1, np.where(end, 0, self.ext_phase))
        self.ext_rec_q = np.where(start, 0, self.ext_rec_q + 1)
        self.ext_exp_q = np.where(self.ext_phase == 0, self.ext_exp_q + 1, 0)
        lag = (self.ext_rec_q >= 1) & (self.ext_rec_q <= 3)
        self.trade_hit = float((self.ext_trade * lag).sum())
        # governments and value climates
        ch = self.ext_next_gov <= 0
        self.ext_G = np.where(ch[:, None], _norm(self.ext_V * np.exp(0.3 * nz)), self.ext_G)
        self.ext_next_gov = np.where(ch, 28 + (x[:, 2] * 16).astype(int), self.ext_next_gov - 1)
        self.ext_V = _norm(self.ext_V + 0.02 * (self.ext_anchor - self.ext_V) + 0.002 * nz)
        # regimes: mixed regimes are the least stable (Hegre et al. 2001)
        mixed = np.abs(self.ext_regime) < 6
        flip = mixed & (x[:, 3] < 0.01)
        self.ext_regime = np.where(flip, np.where(x[:, 4] < 0.5, x[:, 5] * 4 + 6, -6 - x[:, 5] * 4), self.ext_regime)
        # relations drift toward what the regimes and crises make likely (estimate)
        dem = (self.ext_regime >= 6) & (self.regime >= 6)
        closed = (self.ext_regime < 0) | (self.regime < 0)
        tgt = np.where(dem, 0, np.where(closed, 2 + (self.ext_phase == 1), 1))
        mv = x[:, 6] < 0.03
        self.ext_relation = _uclip(self.ext_relation + np.where(mv, np.sign(tgt - self.ext_relation), 0), 0, 3).astype(int)
        # neighbours' own wars (refugees)
        ew = self.ext_war == 1
        self.ext_war = np.where(ew, (x[:, 7] > 0.08).astype(int), (x[:, 7] < 0.0015 * (1 + 3 * (self.ext_regime < 6)) * self.pace).astype(int))
        for j in np.nonzero((self.ext_war == 1) & ~ew)[0]:
            self._event("abroad", "war abroad", None, dict(society=int(j)), big=False)
        # home's war (spec 1 §3; R7: rare and abroad by default in a rich democracy)
        if self.war == 0:
            dp = np.where((self.ext_regime >= 6) & (self.regime >= 6), p["war_dem"], 1.0)
            cf = 1 + (self.phase == 1) * (self.severity + 1) * 0.5 + (self.ext_phase == 1) + 2 * (self.since_break < 8) * (self.regime < 6)
            hz = np.array(p["war_rel"])[self.ext_relation] * dp * cf * self.pace
            hit = np.nonzero(x[:, 8] < hz)[0]
            if len(hit):
                j = int(hit[0])
                home = (self.ext_relation[j] == 3) and (self.ext_regime[j] < 6) and xw[1] < p["war_home_p"]
                self.war, self.war_with, self.war_q = (2 if home else 1), j, 0
            elif xw[2] < p["war_abroad"] * self.pace * (1 + self.ext_war.any()):
                self.war, self.war_with, self.war_q = 1, -1, 0
            if self.war and self.war_with >= 0:
                self.ext_relation[self.war_with] = 3
            if self.war:
                self._event("abroad", "war begins", WAR_STATES[self.war], dict(society=self.war_with), big=True)
        else:
            self.war_q += 1
            if xw[3] < (0.05 if self.war == 1 else 0.08):
                lost = bool(xw[4] < 0.4)
                self._event("abroad", "war ends", WAR_STATES[self.war], dict(society=self.war_with, lost=lost), big=True)
                if lost: self.lost_war_q = 8
                self.war, self.war_with = 0, -1
            elif self.war == 1 and self.war_with >= 0 and xw[5] < 0.01:
                self.war = 2
                self._event("abroad", "war comes home", None, dict(society=self.war_with), big=True)
        self.lost_war_q = max(self.lost_war_q - 1, 0)
        # migration push: neighbours at war or poor, the home economy pulling
        self.ext_migration = _uclip(0.2 * (1 - self.ext_rich) + 0.6 * self.ext_war + 0.2 * (self.ext_phase == 1), 0, 1)
