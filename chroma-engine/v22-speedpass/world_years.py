"""World's methods for public figures, history, the yearly update, pushes and what the engine reads.

Part of class World (world.py), which inherits YearsMixin; moved out of world.py verbatim. A method here reads module
names through the imports below, the same objects world.py has, and self for everything on the World."""
import numpy as np
from library import COLORS
from world_keys import HOLY_KEYS, INST_KINDS, NORM_KEYS, TECH_KEYS
from world_base import (AGE_BANDS, C, FIG_ROLES, HOLY_BASE, HOLY_LUNAR, LAW_MOD, LI, LOC_KINDS, NEW_TECH, NF, NI,
    NORM_MOD, NT, SEC_REF, SEVERITY, TECH_CEIL, _cl, _jsafe, _logit, _norm, _sig, _uclip)


class YearsMixin:
    # ------------------------------------------------------------------------------------------------ public figures
    def _figures_q(self):
        r = self.R[9]
        x = r.random((len(FIG_ROLES), 4))
        for role, fid in list(self.fig_role_now.items()):
            if not self.F_alive[fid]:
                continue
            xr = x[role]
            age = (self.t - self.F_born[fid]) / 52
            self.F_mom[fid] = 0.8 * self.F_mom[fid] + 0.03 * (xr[0] - 0.5)
            self.F_standing[fid] = _cl(self.F_standing[fid] + self.F_mom[fid] * 0.3, 0.02, 1)
            if role == 0:
                self.F_standing[fid] = float(0.5 * self.F_standing[fid] + 0.5 * (0.3 + self.support))
            mort = 0.0005 * np.exp(0.085 * (age - 30)) / 4         # Gompertz, rich-country life table (estimate)
            if xr[1] < mort:
                self.F_alive[fid] = False; self.F_active[fid] = False
                self._event("figure", "death", FIG_ROLES[self.F_role[fid]], dict(fig=fid), big=self.F_standing[fid] > 0.4)
                self._replace_fig(role)
                continue
            if xr[2] < 0.008 * (1 + self.watch):
                self._fig_scandal(fid)
            retire = (FIG_ROLES[role] == "athlete" and age > 34) or (role >= 2 and age > 70) or self.F_standing[fid] < 0.05
            if retire and role >= 2 and xr[3] < 0.3:
                self.F_active[fid] = False
                self._event("figure", "falls", FIG_ROLES[role], dict(fig=fid), big=False)
                self._replace_fig(role)

    def _fig_scandal(self, fid):
        self.F_standing[fid] = max(0.02, self.F_standing[fid] - 0.25)
        self.F_mom[fid] -= 0.05
        self._event("figure", "scandal", FIG_ROLES[self.F_role[fid]], dict(fig=int(fid)), big=self.F_standing[fid] > 0.3)
        if self.F_role[fid] == 0:
            self.support -= 0.04

    def _replace_fig(self, role):
        if role == 0:                                         # a death in office: the party picks a new leader
            self._new_fig(self.R[9], 0, party=self.gov_party)
        else:
            self._new_fig(self.R[9], role, party=self.opp_party if role == 1 else None)

    # ------------------------------------------------------------------------------------------------ history (spec 5 §4)
    def _entry(self, domain, kind, key, value, big=False):
        # world-build.md "Game data": dict(t, age, era, domain, kind, key, value, who); age and who are the
        # character's, so the world writes None and the engine fills them; big marks headline events
        return dict(t=int(self.t), age=None, era=self.era_key, domain=domain, kind=kind, key=key,
                    value=_jsafe(value), who=None, big=bool(big))

    def _event(self, domain, kind, key, value, big=False, public=True):
        e = self._entry(domain, kind, key, value, big)
        if self.p.get("sph_events", False):   # spheres phase 3: the world-fired sphere events, fired at the next quarter
            v_ = value if isinstance(value, dict) else {}
            if domain == "state" and kind == "regime changes":   # which way, against the regime the last quarter saw
                was_ = getattr(self, "sph_reg_seen", None)
                v_ = dict(v_, state=None if was_ is None or float(self.regime) == was_ else ("up" if float(self.regime) > was_ else "down"))
            if not hasattr(self, "sph_wq") or self.sph_wq is None:
                self.sph_wq = []
            self.sph_wq.append([domain, kind, None if key is None else str(key), int(v_.get("loc", -1)), int(v_.get("inst", -1)),
                                None if v_.get("state") is None else str(v_["state"]), bool(big)])
        self.log.append(e)
        if public:
            self.record.append(e)

    def _history_q(self):
        # published figures lag a quarter; recessions are declared after the fact (two quarters in), as is the end
        self.record.append(self._entry("economy", "published", "unemployment", round(self.unemp_prev, 1)))
        self.record.append(self._entry("economy", "published", "inflation", round(self.infl, 1)))
        self.record.append(self._entry("state", "poll", "support", round(self.support, 2)))
        if self.phase == 1 and not self.rec_declared and self.rec_q >= 2:
            self.rec_declared = True
            self._event("economy", "recession declared", SEVERITY[self.severity], None, big=self.severity >= 1)
        if self.phase == 0 and self.rec_declared and self.t - self.rec_end_t >= 26:
            self.rec_declared = False
            self._event("economy", "recession over", None, None, big=False)
        if self.t % 104 == 0:
            self.norm_pub = _sig(self.norm_x).round(2)
            self.record.append(self._entry("culture", "poll", "norms", {k: float(v) for k, v in zip(NORM_KEYS, self.norm_pub)}))

    def _trace(self):
        """Hidden per-quarter state for the world-alone tests (cfg trace=True); never part of the game data."""
        K = self.inst_kind
        leg = [float(self.inst_legitimacy[K == INST_KINDS.index(x)].mean()) for x in ("ministry", "police", "court", "media")]
        self.trace.append(dict(t=self.t, phase=self.phase, sev=self.severity, unemp=self.unemp, infl=self.infl, gap=self.gap,
                               support=self.support, party=self.gov_party, G=self.G.copy(), Dem=self.Dem.copy(),
                               Pos=self.Pos.copy(), V=self.V.copy(), era=self.era_key, era_i=self.era_i, lean=self.lean,
                               Q=self.Q, thr=self.q_thr, unrest=self.unrest, trust=self.trust, legit=leg, war=self.war,
                               pandemic=self.pandemic, laws=self.laws.copy(), norms=_sig(self.norm_x), welfare=self.welfare,
                               mig=self.migrant_share, secular=self.secular, housing=self.housing, ineq=self.ineq,
                               loc_unemp=self.loc_unemp.copy(), payoff=self.payoff.copy(), polar=self.polar,
                               regime=self.regime, gov_q=self.gov_q, natural=self.natural, D0=self.D0.copy(),
                               tech=(self.tech_adopt_v / np.maximum(self.tech_ceil, 1e-3)).copy(), tech_born=list(self.tech_born),
                               temp=float(self._warming(self.t)), jobloss=float(self.rate_mult("jobloss").mean()),
                               birth=self.rate_mult("birth"), parts=self.pos_parts.copy(), Pos_era=self.Pos_era.copy(),
                               Pos_slow=self.Pos_slow.copy()))

    def events_since(self, t):
        """Log entries after world week t (the week's world events for the engine's events list)."""
        out = []
        for e in reversed(self.log):
            if e["t"] <= t:
                break
            out.append(e)
        return out[::-1]

    # ------------------------------------------------------------------------------------------------ yearly
    def _has_new(self, kind):
        return any(self.tech_kind[i] == NEW_TECH.index(kind) and self.tech_adopt_v[i] > 0.3 for i in range(len(self.tech_keys)))

    def _tech_y(self):
        """Technology (spec 5 §1): a generic modern kit at its level; a few new generic kinds arrive and spread."""
        p, r = self.p, self.R[10]
        x = r.random(4)
        lvl = self.cfg["tech_level"]
        rate = p["new_tech"] * {"behind": 0.6, "modern": 1.0, "ahead": 1.5}[lvl]
        if x[0] < rate:
            missing = [i for i in range(NT) if not self.tech_exists[i]]
            if missing:
                i = missing[int(x[1] * len(missing))]
                self.tech_exists[i] = True; self.tech_adopt_v[i] = 0.03; self.tech_ceil[i] = TECH_CEIL["modern"][i]
                self.tech_kind[i] = -2; self.tech_born[i] = int(self.t)
                self._event("tech", "arrives", TECH_KEYS[i], None, big=False)
            else:
                kind = int(x[1] * len(NEW_TECH))
                n_same = sum(1 for k_ in self.tech_kind if k_ == kind)
                key = f"{NEW_TECH[kind]} {n_same + 1}"
                self.tech_keys.append(key); self.tech_kind.append(kind); self.tech_born.append(int(self.t))
                self.tech_adopt_v = np.append(self.tech_adopt_v, 0.03); self.tech_ceil = np.append(self.tech_ceil, 0.6 + 0.35 * x[2])
                self.tech_exists = np.append(self.tech_exists, True)
                self._event("tech", "arrives", key, None, big=False)
        openness = float(self.V @ self.DOPEN) * 5
        sp = p["tech_r"] * (1 + 0.5 * self.gap) * (1 + 0.3 * openness)
        a = _uclip(self.tech_adopt_v, 1e-4, 1 - 1e-4)
        c = np.maximum(self.tech_ceil, 1e-3)
        frac = _uclip(a / c, 1e-4, 1 - 1e-4)
        before = self.tech_adopt_v.copy()
        self.tech_adopt_v = np.where(self.tech_exists, c * _sig(_logit(frac) + sp), 0.0)
        for i in np.nonzero((before < 0.5 * c) & (self.tech_adopt_v >= 0.5 * c) & (np.array(self.tech_born) > 0))[0]:
            self._event("tech", "spreads", self.tech_keys[i], round(float(self.tech_adopt_v[i]), 2), big=False)
        # effects of the new kinds
        kinds = np.array(self.tech_kind)
        def adopt_of(kind):
            m = kinds == NEW_TECH.index(kind)
            return float(self.tech_adopt_v[m].sum()) if m.any() else 0.0
        self.medical = _cl(self.medical + 0.05 * (self.medical0 + 0.08 * adopt_of("new treatment") - self.medical), 0, 0.98)
        self.comm = _cl(0.4 * self.tech_adopt_v[0] + 0.4 * self.tech_adopt_v[2] + 0.1 * adopt_of("new medium") + 0.1 * adopt_of("new way to meet"), 0, 1)
        wt = {"behind": .25, "modern": .40, "ahead": .55}[lvl] + 0.2 * (self.regime < 0) + 0.1 * adopt_of("new watch")
        self.watch = _cl(self.watch + 0.1 * (wt - self.watch), 0, 1)
        newm = adopt_of("new machine") + 0.5 * self.tech_adopt_v[TECH_KEYS.index("ai helper")]
        base = np.array([.10, .25, .15, .10, .03]) * (0.7 if lvl == "behind" else 1.3 if lvl == "ahead" else 1.0)
        spread = np.array([max(self.tech_adopt_v[i] - before[i], 0) for i in range(len(self.tech_keys))])
        mach = float(sum(spread[i] for i in range(len(self.tech_keys)) if kinds[i] == NEW_TECH.index("new machine")))
        self.automation = _uclip(self.automation + 0.15 * (base - self.automation) + mach * np.array([.3, 1.0, .6, .3, .1]), 0, 1)
        # sectors: automation shrinks the exposed sectors, new kinds of jobs grow knowledge, welfare moves the public sector
        jobs = adopt_of("new kind of job")
        tilt = np.array([-.4, -.6, -.1, .2, 0]) * (self.automation - base) * 2 + np.array([0, 0, 0, .15, 0]) * jobs \
            + np.array([0, 0, 0, 0, 0.8]) * (self.welfare - p["welfare0"])
        self.sector_tilt += 0.2 * (tilt - self.sector_tilt)
        self.loc_sectors = _norm(self.loc_sector_base * np.exp(self.sector_tilt))

    def _belief_y(self):
        """Belief (spec 5 §3): switching at real rates, insecurity raises religiosity, revivals, the calendar."""
        p, r = self.p, self.R[11]
        x = r.random(4)
        pop = self.pop
        insecure = _cl((self.phase == 1) * (self.severity + 1) / 3 + 0.6 * (self.war == 2) + 0.3 * (self.pandemic in (1, 2))
                                 + 0.3 * (self.loc_disaster > 0).mean(), 0, 1)
        adult = pop[1:]
        rel = adult[:, :, :, 1:, :]
        sec = adult[:, :, :, :1, :]
        dis = self._place_w() @ np.minimum(self.loc_disaster, 1)
        # leaving comes mostly in early adulthood (Pew 2015), joining a little more with age (both by adult age band)
        a_lv = np.array([2.5, 1.5, 0.7, 0.5, 0.4, 0.3, 0.3])[:, None, None, None, None]
        a_jn = np.array([0.6, 0.8, 1.0, 1.0, 1.2, 1.4, 1.4])[:, None, None, None, None]
        lv = p["leave_p"] * (1 - 0.6 * insecure) * a_lv
        jn = p["join_p"] * (1 + 2.0 * insecure) * (1 + 3 * dis)[None, None, :, None, None] * a_jn   # Bentzen 2019: disasters
        rv = getattr(self, "revival", None)
        fshare = rel.sum((0, 1, 2, 4)); fshare = fshare / max(fshare.sum(), 1e-9)
        attract = fshare.copy()
        if rv is not None and rv[1] > 0:
            attract[rv[0]] += 1.0; jn = jn * 3
            self.revival = (rv[0], rv[1] - 1)
        attract /= attract.sum()
        leave = rel * lv
        join = sec * jn
        sw = rel * p["switch_p"]
        moved = sw.sum(3, keepdims=True)
        new_rel = rel - leave - sw + join * attract[None, None, None, :, None] + moved * attract[None, None, None, :, None]
        new_sec = sec + leave.sum(3, keepdims=True) - join
        self.pop[1:, :, :, 1:, :] = np.maximum(new_rel, 0)
        self.pop[1:, :, :, :1, :] = np.maximum(new_sec, 0)
        self.switched = float(p["leave_p"] * (1 - 0.6 * insecure) + p["switch_p"])
        self.spiritual = _cl(self.spiritual + 0.05 * (0.1 + 0.3 * self.secular - self.spiritual), 0, 1)
        self.conspiracy = _cl(self.conspiracy + 0.1 * (0.08 + 0.3 * (0.45 - self.trust) + 0.2 * self.fear - self.conspiracy), 0, 1)
        self.holy_shift = (self.holy_shift + np.array(HOLY_LUNAR + [0.0] * (self._nf() - NF))) % 52

    def _generations_y(self):
        """Each generation's mix is set while it is 15 to 25 (spec 1 §4): from the society's values, the era and how
        secure the times are, read through the engine's Schwartz map (secure youth lean to self-direction and
        universalism, insecure youth to security and tradition), never a color rule."""
        p, r = self.p, self.R[12]
        y = self.t // 52
        nz = self._cn(r)
        sec = self.security()
        self.sec_hist = getattr(self, "sec_hist", []) + [round(sec, 4)]
        ca_ = p["coh_anchor"]
        base = _norm((1 - ca_) * self.Vc + ca_ * self.V_anchor)
        era = self.era_i * (self.era_p - 0.2) if self.era_key is not None else np.zeros(C)
        if self._s3("cult_anchor"):                        # LW1 1e as reworked (Emren 10-09): the young are drawn toward
            if getattr(self, "V_start", None) is None:     # the society's starting values moved by the era, whose hold
                self.V_start = np.asarray(self.Vc, float).copy()   # fades with its age: a bounded target, never a push
            if self.era_key is not None:                            # that lasts (which ran away)
                era = era * np.exp(-(self.t - self.era_since) / (52.0 * p["era_fade_y"]))
            tgt_ = np.maximum(self.V_start + p["era_home_k"] * era, 0.005)
            base = _norm((1 - p["coh_home"]) * self.Vc + p["coh_home"] * tgt_ / tgt_.sum())
            era = np.zeros(C)
        open_ = 1.5 if self.open_q > 0 else 1.0
        m_ = self._m_sh() if self._s3("cult_shake") else 1.0                          # LW1 1g: shaken times move faster
        if self._s3("cult_no_dice"):                                                  # LW1 1h: no dice in the culture
            nz = 0.0 * nz
        if m_ == 1.0 and not (self._s3("cult_schools") or self._s3("cult_scenes")):
            imp = _norm(base + p["coh_era"] * open_ * era + p["coh_sec"] * (sec - SEC_REF) * self.DSEC * 0.2) * np.exp(p["coh_noise"] * nz)
        else:
            imp = _norm(base + m_ * p["coh_gain"] * (p["coh_era"] * open_ * era + p["coh_sec"] * (sec - SEC_REF) * self.DSEC * 0.2)
                        + m_ * self._s3_young_pull()) * np.exp(p["coh_noise"] * nz)
        imp /= imp.sum()
        self._ensure_coh(y)
        for age in range(15, 26):
            b = self.Y0 + y - age
            if b < 0 or self.coh_fixed[b]:
                continue
            self.coh_n[b] += 1
            self.coh[b] += (imp - self.coh[b]) / self.coh_n[b]
            if age == 25:
                self.coh_fixed[b] = True
        for b in range(max(self.Y0 + y - 14, 0), self.Y0 + y + 1):       # the unformed young follow the society
            if not self.coh_fixed[b] and self.coh_n[b] == 0:
                self.coh[b] = base
        if self._s3("cult_adults"):                        # LW1 1d: generations past 25 move with the times, a fifth as fast
            bs = np.arange(max(self.Y0 + y - 100, 0), max(self.Y0 + y - 25, 0))
            bs = bs[self.coh_fixed[bs]]
            if len(bs):
                self.coh[bs] += p["coh_adult"] / 11 * m_ * (imp - self.coh[bs])
                self.coh[bs] /= self.coh[bs].sum(1, keepdims=True)

    def security(self):
        """How secure the times are for the young (0..1): work, war, pandemic, prices, welfare (estimate)."""
        return _cl(1 - 0.06 * max(self.unemp - self.natural, 0) - 0.12 * (self.phase == 1) * (1 + self.severity)
                             - 0.45 * (self.war == 2) - 0.1 * (self.war == 1) - 0.15 * (self.pandemic == 2)
                             - 0.03 * max(self.infl - 5, 0) + 0.2 * (self.welfare - self.p["welfare0"]) - 0.15 * self.unrest, 0, 1)

    def _ensure_coh(self, y):
        need = self.Y0 + y + 30
        if need > len(self.coh):
            extra = need - len(self.coh) + 100
            self.coh = np.concatenate([self.coh, np.tile(self.coh[-1], (extra, 1))])
            self.coh_fixed = np.concatenate([self.coh_fixed, np.zeros(extra, bool)])
            self.coh_n = np.concatenate([self.coh_n, np.zeros(extra)])

    def _pop_y(self):
        """Population (spec 2 §6): deaths, ageing, births, coming of age, migrants, class mobility; places."""
        p, r = self.p, self.R[12]
        x = r.random(4)
        pop = self.pop
        mort = np.array([.0003, .0005, .0008, .0015, .0035, .008, .02, .08])           # rich-country life tables (estimate)
        mult = 1 + 0.3 * (self.pandemic == 2) * np.array([0, 0, 0, 0, .2, .5, 1, 1.5]) + 0.01 * (self.war == 2)
        pop *= (1 - mort * mult)[:, None, None, None, None]
        width = np.array([15, 10, 10, 10, 10, 10, 10, 1e9])
        flow = pop / width[:, None, None, None, None]
        flow[-1] = 0
        # coming of age: in secure times some of the faithful young leave (secularisation by generation)
        sec = self.security()
        psi = _cl(p["secularise"] * (1 + 3.0 * (sec - SEC_REF)) * (0.3 if getattr(self, "revival", (0, 0))[1] > 0 else 1), 0, 0.5)
        f0 = flow[0].copy()
        lv = f0[:, :, 1:, :] * psi
        f0[:, :, 1:, :] -= lv; f0[:, :, :1, :] += lv.sum(2, keepdims=True)
        flow[0] = f0
        pop -= flow
        pop[1:] += flow[:-1]
        # births (Sobotka et al. 2011: put off in downturns), into the parents' class, place and faith, native-born
        parents = pop[2:4].sum(0).sum(-1)
        pop[0, ..., 0] += 0.042 * self.rate_mult("birth") * parents
        # migrants (UN DESA; OECD: about 1 in 7 foreign-born): inflow pulled by the economy, pushed by neighbours
        push = float((self.ext_migration * (0.5 + self.ext_trade)).sum())
        self.mig_in = float(p["mig0"] * (1 + 0.8 * self.gap) * (0.7 + 0.6 * push) * (0.5 + 0.5 * self.demo))
        if push > 0.8 and x[0] < 0.5 and self.ext_war.any():
            self._event("abroad", "refugees arrive", None, dict(share=round(self.mig_in, 4)), big=False)
        tot = pop.sum()
        newm = self.mig_in * tot
        ma = np.array([0, .4, .45, .1, .05, 0, 0, 0]); mc = np.array([.45, .45, .10]); mp = np.array([.7, .25, .05])
        mf = np.array([.25, .30, .15, .30] + [0.0] * (self._nf() - NF))   # C5: no migrant arrives in a movement
        pop[..., 1] += newm * ma[:, None, None, None] * mc[None, :, None, None] * mp[None, None, :, None] * mf[None, None, None, :]
        pop[..., 1] *= 1 - p["mig_out"]
        # class mobility (small, downward in recessions)
        down = 0.004 + 0.004 * (self.phase == 1)
        up = 0.006 * (1 + self.gap)
        lo, mi, hi = pop[:, 0].copy(), pop[:, 1].copy(), pop[:, 2].copy()
        pop[:, 0] += down * mi - up * lo; pop[:, 1] += up * lo - down * mi + 0.004 * hi - 0.003 * mi
        pop[:, 2] += 0.003 * mi - 0.004 * hi
        # places: growth follows the local economy; declining places lose people (spec 3 §2.3)
        g = (0.004 * self.loc_trend_base() - 0.003 * (self.loc_unemp - self.unemp) / max(self.unemp, 1)
             + 0.02 * (self.loc_pop0 - self.loc_pop_share) / self.loc_pop0)
        self.loc_growth = 0.7 * self.loc_growth + 0.3 * g
        old_tr = self.loc_trend.copy()
        self.loc_trend = np.where(self.loc_growth > 0.002, 2, np.where(self.loc_growth < -0.002, 0, 1))
        self.loc_pop_share = self.loc_pop_share * (1 + g); self.loc_pop_share /= self.loc_pop_share.sum()
        place = np.array([(self.loc_pop_share * (self.loc_place == k)).sum() for k in range(3)])
        cur = pop.sum((0, 1, 3, 4))
        pop *= (place / np.maximum(cur / cur.sum(), 1e-9))[None, None, :, None, None]
        self.pop = pop / pop.sum()
        # faith shares, migrants, value climate
        self._group_mix()
        self.V = self._V()
        self.Vc_hist.append(self.V.tolist())
        w = self.pop.reshape(-1) * self.gadult
        pl = self.gidx[2]
        lm = np.array([(w[pl == k][:, None] * self.gmix[pl == k]).sum(0) / max(w[pl == k].sum(), 1e-9) for k in range(3)])
        self.loc_mix = _norm(lm[self.loc_place] + 0.15 * (self.loc_class_mix[:, 2:3] - 0.15) * self.DSEC * 0.2)

    def loc_trend_base(self):
        k = [LOC_KINDS[i] for i in self.loc_kind]
        return np.array([{"capital": .8, "tech boom town": 2.0, "energy boom town": 1.5, "declining industrial town": -2.0,
                          "commuter suburb": .8, "remote area": -1.0, "fishing village": -.8, "mountain village": -.6,
                          "university city": .5}.get(x, 0.0) for x in k])

    def _group_mix(self):
        """Each group's mix: its generations' mixes plus class, place, faith and migrant tilts (the class and place
        tilts run along the secure and openness directions of the Schwartz map)."""
        p = self.p
        y = self.t // 52
        self._ensure_coh(y)
        cb = np.zeros((8, C))
        for a, (lo, hi) in enumerate(AGE_BANDS):
            bs = np.arange(self.Y0 + y - min(hi, 100) + 1, self.Y0 + y - lo + 1)
            bs = bs[bs >= 0]
            cb[a] = self.coh[bs].mean(0)
        self.coh_band = cb
        w = self.pop.sum((1, 2, 3, 4))
        self.Vc = _norm((w[1:, None] * cb[1:]).sum(0) / w[1:].sum())
        tc = p["tilt_class"] * np.array([-1, 0, 1])[:, None] * self.DSEC * 0.2 * 5
        tp = p["tilt_place"] * np.array([1, 0, -1])[:, None] * self.DOPEN * 0.2 * 5
        tf = np.vstack([np.zeros(C), p["tilt_faith"] * (self.FPROF - 0.2)])
        if hasattr(self, "ext_V"):
            ev = (self.ext_V * (self.ext_migration + 0.1)[:, None]).sum(0) / (self.ext_migration + 0.1).sum()
            self.mig_tilt = p["tilt_mig"] * (ev - self.Vc)
        tm = np.vstack([np.zeros(C), self.mig_tilt])
        a, c, pl, f, m = self.gidx
        if self._s3("cult_pushback") and getattr(self, "group_unmet", None) is not None and len(self.Vc_hist) > 10:
            dV = self.V - np.asarray(self.Vc_hist[-11])  # LW1 1f: the last decade's change, braked by those it leaves behind
            u_ = self.group_unmet.sum(1); u_ = _uclip(u_ / max(u_.mean(), 1e-9) - 1, 0, 2)
            lb = (u_ * np.where(a >= 4, 1.0, np.where(a >= 3, 0.5, 0.2)) * np.array([0.7, 1.0, 1.3])[pl]
                  * np.array([1.3, 1.0, 0.7])[c])
            self.gmix = _norm(cb[a] + tc[c] + tp[pl] + tf[f] + tm[m] - p["coh_back"] * lb[:, None] * dV, 0.01)
        else:
            self.gmix = _norm(cb[a] + tc[c] + tp[pl] + tf[f] + tm[m], 0.01)
        a_ = self.pop.sum((1, 2, 3, 4))
        self.old_share, self.young_share = float(a_[5:].sum() / a_[1:].sum()), float(a_[1:3].sum() / a_[1:].sum())
        fs = self.pop.sum((0, 1, 2, 4))
        self.secular = float(fs[0])
        self.faith_share = fs[1:].copy()
        self.migrant_share = float(self.pop[..., 1].sum())

    def _V(self):
        w = self.pop.reshape(-1) * self.gadult
        return _norm((w[:, None] * self.gmix).sum(0) / w.sum())

    # ------------------------------------------------------------------------------------------------ pushes (spec 7 §3)
    def push(self, domain, var, amount, sign):
        """Queue a push from a life; it lands at the next quarter tick, scaled into the domain's own dynamics.
        amount is the push's size in reach units (0 one of the crowd .. 3 strongly: base x reach x how well it went);
        sign is +1 or -1. Variables by domain (an id follows a colon, e.g. "legitimacy:12"):
          state: "support"; a law key (a minister passes what the norms support, fails more often against them);
                 "welfare"; "pressure" (a movement's push on the society's pressure); a color letter (its direction)
          culture: a norm key (moves acceptance a little, with a lag); "trust"; a color letter
          economy: "inequality", "housing"; place: "crime:<loc>", "efficacy:<nb>", "unemp:<loc>"
          institution: "legitimacy:<id>", "corruption:<id>", "capacity:<id>", "reform:<id>"
          tech: "adopt:<key>", "medical", "invent"; belief: "faith:<f>", "secular"; abroad: "relation:<society>"
          nature: "warming" (tiny)."""
        self._queue.append([str(domain), str(var), float(amount), 1.0 if sign >= 0 else -1.0])

    def _apply_pushes(self):
        CROWD = 1e-6                                          # an ordinary voice is one of millions
        for dom, var, amt, sg in self._queue:
            a = max(amt, CROWD) * sg
            key, _, idx = var.partition(":")
            done = None
            try:
                if dom == "state" and key == "support":
                    self.support = _cl(self.support + 0.01 * a, 0.02, 0.98); done = 0.01 * a
                elif dom == "state" and key in LI:
                    self.law_push[LI[key]] += 0.6 * a; done = 0.6 * a     # a minister (3) passes it if norms agree
                elif dom == "state" and key == "welfare":
                    self.welfare = _cl(self.welfare + 0.01 * a, 0.05, 0.95); done = 0.01 * a
                elif dom == "state" and key == "pressure":
                    self.Q = max(0.0, self.Q + 0.05 * a * getattr(self, "q_thr", self.p["q_theta"])); done = 0.05 * a
                elif dom in ("state", "culture") and key in COLORS:
                    dv = np.zeros(C); dv[COLORS.index(key)] = 0.005 * a; dv -= dv.mean()
                    self.dem_push = getattr(self, "dem_push", np.zeros(C)) + dv; done = 0.005 * a
                elif dom == "culture" and key in NI:
                    self.norm_push[NI[key]] += 0.05 * a; done = 0.05 * a
                elif dom == "culture" and key == "trust":
                    self.trust = _cl(self.trust + 0.005 * a, 0.02, 0.95); done = 0.005 * a
                elif dom == "economy" and key == "inequality":
                    self.ineq = _cl(self.ineq + 0.002 * a, 0.15, 0.6); done = 0.002 * a
                elif dom == "economy" and key == "housing":
                    self.housing = _cl(self.housing + 0.01 * a, -1, 1); done = 0.01 * a
                elif dom == "place" and key == "crime":
                    self.loc_crime[int(idx)] = _uclip(self.loc_crime[int(idx)] + 0.02 * a, 0.01, 1); done = 0.02 * a
                elif dom == "place" and key == "efficacy":
                    self.nb_efficacy[int(idx)] = _uclip(self.nb_efficacy[int(idx)] + 0.03 * a, 0.05, 0.98); done = 0.03 * a
                elif dom == "place" and key == "unemp":
                    self.loc_ufac[int(idx)] = max(0.3, self.loc_ufac[int(idx)] + 0.02 * a); done = 0.02 * a
                elif dom == "institution" and key in ("legitimacy", "corruption", "capacity"):
                    arr = getattr(self, "inst_" + key); i = int(idx)
                    arr[i] = _uclip(arr[i] + 0.03 * a, 0.01, 0.99); done = 0.03 * a
                    if a < 0 and getattr(self, "c3_cover", None) is not None and self.c3_cover[i] > self.t:
                        self.c3_break[i] = True                    # C3: an insider speaks up; the scandal breaks
                elif dom == "institution" and key == "reform" and a > 0:
                    i = int(idx)
                    if a >= 1.5: self._reform_inst(i, self.inst_native[i], step=0.2 * a)
                    done = a
                elif dom == "tech" and key == "adopt" and idx in self.tech_keys:
                    i = self.tech_keys.index(idx)
                    self.tech_adopt_v[i] = _uclip(self.tech_adopt_v[i] + 0.002 * a, 0, self.tech_ceil[i]); done = 0.002 * a
                elif dom == "tech" and key == "medical":
                    self.medical0 = _cl(self.medical0 + 0.005 * a, 0, 0.95); done = 0.005 * a
                elif dom == "tech" and key == "invent" and a >= 2.0:
                    self.medical0 = _cl(self.medical0 + 0.01, 0, 0.95); done = 0.01
                elif dom == "belief" and key == "faith":
                    f = int(idx); d = 0.002 * a * self.pop[1:, :, :, 0, :]
                    self.pop[1:, :, :, 0, :] -= d; self.pop[1:, :, :, 1 + f, :] += d; done = 0.002 * a
                elif dom == "belief" and key == "secular":
                    d = 0.002 * a * self.pop[1:, :, :, 1:, :]
                    self.pop[1:, :, :, 1:, :] -= d; self.pop[1:, :, :, :1, :] += d.sum(3, keepdims=True); done = 0.002 * a
                elif dom == "abroad" and key == "relation" and abs(a) >= 1:
                    j = int(idx); self.ext_relation[j] = int(_uclip(self.ext_relation[j] - np.sign(a), 0, 3)); done = -np.sign(a)
                elif dom == "nature" and key == "warming":
                    done = 0.0
            except (ValueError, IndexError):
                done = None
            self.push_log.append(dict(t=int(self.t), domain=dom, var=var, amount=amt, sign=sg,
                                      applied=None if done is None else float(done)))
        self._queue = []
        if len(self.push_log) > 400:
            self.push_log = self.push_log[-400:]

    # ------------------------------------------------------------------------------------------------ what the engine reads
    def law_state(self, key):
        return int(self.laws[LI[key]]) if key in LI else int(LAW_MOD[key])   # W38b keys: the modern law book

    def norm(self, key):
        return float(_sig(self.norm_x[NI[key]])) if key in NI else float(NORM_MOD[key])   # W38b keys: modern acceptance

    def tech_has(self, key):
        return key in self.tech_keys and bool(self.tech_exists[self.tech_keys.index(key)])

    def tech_adopt(self, key, cls=None, age=None, place=None):
        """Adoption 0..1, nationally or for a group: the young, the rich and the urban first (spec 5 §1)."""
        if not self.tech_has(key):
            return 0.0
        a = float(self.tech_adopt_v[self.tech_keys.index(key)])
        if cls is None and age is None and place is None:
            return a
        off = 0.0
        if cls is not None: off += (-0.8, 0.0, 0.7)[int(cls)]
        if place is not None: off += (0.3, 0.0, -0.6)[int(place)]
        if age is not None: off += _cl((35 - age) / 25, -2.0, 0.8)
        return float(_sig(_logit(a) + off))

    def holy_weeks(self, faith=None):
        """{holy key: set of weeks of the year} for a faith (default: the culture's main faith) this year."""
        f = int(np.argmax(self.faith_share)) if faith is None or faith < 0 else int(faith)
        sh = int(round(self.holy_shift[f]))
        return {k: set(int((w + sh) % 52) for w in HOLY_BASE[f][k]) for k in HOLY_KEYS}

    def cohort_mix(self, birth_week):
        """A generation's mix: fixed when it is 15 to 25; the current base while it is younger."""
        b = int(self.Y0 + np.floor(birth_week / 52))
        self._ensure_coh(self.t // 52)
        b = int(_uclip(b, 0, len(self.coh) - 1))
        return self.coh[b].copy()

    def rate_mult(self, kind):
        """Multipliers on the Library's per_year rates (world-build.md). Season, pandemic and medicine for illness and
        old-age deaths (scalar); locality arrays for disaster and crime (crime_nb per neighbourhood); a sector array for
        job loss; scalars for war, pandemic moments and births. Health effects stay rate multipliers only (R5)."""
        s = self.season
        if kind == "illness":
            return float((1.3, 1.0, 0.75, 0.95)[s] * (1, 1.3, 2.0, 1.3)[self.pandemic] * (1 - 0.5 * (self.medical - self.medical0)))
        if kind == "old_death":
            return float((1.12, 0.99, 0.92, 0.97)[s] * (1, 1.2, 1.6, 1.15)[self.pandemic] * (1 - 0.5 * (self.medical - self.medical0)))
        if kind == "disaster":                             # pace, and the recovery years after a strike (loc_disaster);
            hzx = self.loc_hazards * np.array(self.p["dis_base"]) * self.extremes
            if getattr(self, "land_hx", None) is not None:   # v25 wa_land: the hazards answer the land's state
                hzx = hzx * self.land_hx
            hz = hzx.sum(1) / self.haz_ref   # the strike
            return self.pace * hz * (1 + self.p["dis_active"] * np.minimum(self.loc_disaster, 1))          # itself: disaster_now
        if kind == "crime":
            return self.loc_crime / self.crime_ref
        if kind == "crime_nb":
            return self.nb_crime / self.crime_ref
        if kind == "war":
            return float((0.3, 4.0, 15.0)[self.war])
        if kind == "pandemic":
            return float((0.2, 2.0, 4.0, 1.5)[self.pandemic])
        if kind == "jobloss":
            return self.unemp_sector / self.nat_sector
        if kind == "birth":
            return _cl(1 - 0.015 * (self.unemp - self.natural) - 0.15 * (self.war == 2) - 0.08 * (self.pandemic == 2)
                                 + 0.03 * max(self.gap, 0), 0.6, 1.1)
        raise KeyError(kind)

    @property
    def faith_profile(self):
        return self.FPROF
