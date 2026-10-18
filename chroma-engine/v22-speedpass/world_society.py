"""World's methods for the economy, the state, institutions, places, culture and society (with stage 3).

Part of class World (world.py), which inherits SocietyMixin; moved out of world.py verbatim. A method here reads
module names through the imports below, the same objects world.py has, and self for everything on the World."""
import numpy as np
from library import ERA_KINDS
from combos import IDEAS
from world_keys import INST_KINDS, LAW_KEYS, LAW_STATES
from world_base import (BREAKTHROUGHS, C, COMBO_DIR, COMBO_KEYS, COMBO_MIX, LI, NF, NI, NL, NN, NORM_RIGHT, PHASES,
    RIGHTS, S3_RULES, SECTOR_GUILDS, _cl, _norm, _sig, _tv, _uclip)


class SocietyMixin:
    # ------------------------------------------------------------------------------------------------ economy (spec 1 §2)
    def _econ_q(self):
        p, r = self.p, self.R[3]
        x = r.random(8)
        self.gap_prev, self.unemp_prev = self.gap, self.unemp
        self.house_hist = np.roll(self.house_hist, 1); self.house_hist[0] = self.housing
        if self.phase == 0:
            self.exp_q += 1
            yrs = self.exp_q / 4
            h = (p["h0"] + p["h_age"] * yrs + p["h_imb"] * max(self.housing, 0) + p["h_trade"] * self.trade_hit
                 + p["h_world"] * self.world_rec + p["h_shock"] * max(self.energy, 0) / 5
                 + 0.4 * (self.pandemic == 2) + 0.15 * (self.war == 2))
            if x[0] < 1 - np.exp(-h * self.pace):
                boom = _cl(self.house_hist.max(), 0, 1)
                pr = np.array(p["sev_p"], float)
                pr[2] *= (1 + p["crisis_boom"] * boom) * self.pace
                if self.pandemic == 2 or self.war == 2: pr[0] *= 0.2
                pr /= pr.sum()
                sev = int((x[1] > np.cumsum(pr)).sum())
                self.phase, self.severity, self.rec_q = 1, min(sev, 2), 0
                self.rec_len = 2 + int(-np.log(max(x[2], 1e-9)) * (p["rec_len"][self.severity] - 2))
                self.u_rise_tgt = self.u_rise + p["u_rise"][self.severity] * (0.7 + 0.6 * x[3])
                self.rec_start_t = self.t; self.n_rec += 1
                self.cycles.append([int(self.t), -1, int(self.severity)])
        else:
            self.rec_q += 1
            if self.rec_q >= self.rec_len:
                self.phase, self.exp_q, self.last_sev = 0, 0, self.severity
                self.rec_end_t = self.t
                self.cycles[-1][1] = int(self.t)
        # output gap
        if self.phase == 1:
            self.gap += 0.5 * (p["gap_floor"][self.severity] - self.gap)
        else:
            tgt = p["gap_boom"] * (1 - np.exp(-self.exp_q / 4 / p["gap_tau"]))
            self.gap += p["gap_rec"][self.last_sev] * (tgt - self.gap)
        self.gap += 0.02 * r.normal() - 0.05 * max(self.energy, 0) / 5
        self.gap = _cl(self.gap, -1, 1)
        self.gap_ema += 0.01 * (self.gap - self.gap_ema)
        # unemployment: natural + a rise that decays with a half-life of about 2 years (spec 1 §2)
        if self.phase == 1:
            self.u_rise += 0.45 * (self.u_rise_tgt - self.u_rise)
        else:
            self.u_rise *= 0.5 ** (1 / p["u_half"][self.last_sev])
        self.u_noise = 0.6 * self.u_noise + 0.12 * r.normal()
        auto = float((self.automation * self._sectors()).sum())
        self.unemp = _cl(self.natural + self.u_rise + self.u_noise + 4 * max(auto - 0.15, 0) + 3 * (self.war == 2), 1.5, 30)
        # inflation: 2% baseline, demand, price shocks, war and pandemic (spec 1 §2)
        self.infl_e = 0.7 * self.infl_e + 0.3 * r.normal()
        self.infl = _cl(p["infl0"] + p["infl_gap"] * self.gap + self.energy + self.food + 2.5 * (self.war == 2)
                                  + 0.8 * (self.pandemic == 3) + 1.2 * max(self.housing, 0) + self.infl_e, -2, 15)
        # housing: momentum with mean reversion; recessions knock it down, crises hard
        self.house_m = 0.85 * self.house_m - 0.03 * self.housing + 0.02 * self.gap + 0.022 * r.normal()
        if self.phase == 1: self.house_m -= (0.01, 0.03, 0.08)[self.severity]
        self.housing = _cl(self.housing + self.house_m, -1, 1)
        # inequality drifts with automation, welfare and crises
        self.ineq = _cl(self.ineq + 0.01 * (p["ineq0"] - self.ineq) + 0.002 * (auto - 0.15) * 10
                                  - 0.002 * (self.welfare - p["welfare0"]) * 10 + 0.003 * (self.phase == 1) * (self.severity == 2)
                                  + 0.002 * r.normal(), 0.15, 0.6)
        # what pays off (spec 1 §2, spec 6 §2): centred on the cycle so it favours no color over time
        s = self.gap - self.gap_ema
        pos = getattr(self, "Pos", np.full(C, 0.2))
        self.payoff = _norm(0.2 + p["pay_pos"] * s * (pos - 0.2) + p["pay_ent"] * s * self.DENT * 0.2)
        self._derive_econ()

    def _sectors(self):
        """National sector shares (farm industry services knowledge public): population-weighted localities."""
        return (self.loc_pop_share[:, None] * self.loc_sectors).sum(0)

    def _derive_econ(self):
        p = self.p
        sh = self._sectors()
        cyc = np.array([0.9, 1.5, 1.0, 0.6, 0.3])           # how far each sector rides the cycle (estimate)
        stru = np.array([1.2, 1.1, 1.0, 0.65, 0.6])          # structural unemployment by sector (estimate)
        u_s = self.natural * stru / (sh * stru).sum() + (self.unemp - self.natural) * cyc / (sh * cyc).sum() \
            + 6 * np.maximum(self.automation - 0.15, 0)
        u_s *= self.unemp / max((sh * u_s).sum(), 1e-6)
        self.unemp_sector = _uclip(u_s, 0.5, 40)
        self.nat_sector = self.natural * stru / (sh * stru).sum()
        lu = (self.loc_sectors * self.unemp_sector).sum(1) * self.loc_ufac
        lu *= self.unemp / max((self.loc_pop_share * lu).sum(), 1e-6)
        self.loc_unemp = self.unemp_loc = _uclip(lu, 0.5, 45)
        self.prosper = self.gap
        self.phase_key = PHASES[self.phase]

    # ------------------------------------------------------------------------------------------------ state (spec 1 §3)
    def _state_q(self):
        p, r = self.p, self.R[4]
        x = r.random(8); xl = r.random(NL); nz = self._cn(r)
        d = _tv(self.G, self.Dem)
        sn_ = r.normal()
        if self._s3("hist_chance_only"):                   # LW2 2e: support follows the record, not dice
            sn_ = 0.0
        self.support += (-p["rule_cost"] / 4 + p["ev_gap"] * (self.gap - self.gap_prev) - p["ev_u"] * (self.unemp - self.unemp_prev)
                         - p["ev_infl"] * max(self.infl - 4, 0) - p["th_sup"] * 0.25 * max(d - 0.05, 0)
                         + 0.03 * (0.5 - self.support) * 0.25 + p["s_noise"] * sn_)
        self.support = _cl(self.support, 0.05, 0.95)
        self.gov_q += 1
        self.next_vote -= 1
        if self.next_vote <= 0 and self.regime >= 0:
            self._election(x, nz)
        elif self.regime < 0 and (self.Q > 0.5 * getattr(self, "q_thr", 1e9) if self._s3("hist_chance_only") else x[5] < 0.01):
            self.G = _norm(self.G + 0.1 * (self.Dem - self.G))   # closed regimes reshuffle rarely (2e: when pressure builds)
        # the law book (spec 1 §3): the support a law has (the norm, the government's fit with the law's colors, pushes
        # that count for more where the norms agree) points to a state; the law moves one step toward it with a small
        # chance each quarter, so laws trail norms by years
        n = _sig(self.norm_x[:NL])
        fit = (self.G - 0.2) @ self.NPROF[:NL].T
        neff = n + p["law_fit"] * fit + 0.12 * self.law_push * (n / 0.5) ** 2
        neff[LI["conscription"]] += 0.5 * (self.war == 2) + 0.15 * (self.war == 1)
        tgt = np.where(neff > p["law_cut"][1], 0, np.where(neff > p["law_cut"][0], 1, 2))
        margin = np.where(tgt < self.laws, neff - np.where(self.laws == 2, p["law_cut"][0], p["law_cut"][1]),
                          np.where(self.laws == 0, p["law_cut"][1], p["law_cut"][0]) - neff)
        hz = p["law_h"] * (1 + 10 * np.maximum(margin, 0)) * (p["law_open"] if self.open_q > 0 else 1.0) + 0.3 * (self.law_push > 0.5)
        mv = (tgt != self.laws) & (xl < hz)
        self.law_push *= 0.5
        self.law_since += 0.25
        for k in np.nonzero(mv)[0]:
            self._set_law(k, self.laws[k] + int(np.sign(tgt[k] - self.laws[k])))
        # welfare: a law-book entry that moves with government and with unmet safety (spec 1 §3)
        wt = p["welfare0"] + 3.0 * float((self.G - 0.2) @ self.WPROF) + 0.5 * (self.unmet_mean[0] - self.need_base[0] if hasattr(self, "unmet_mean") else 0)
        self.welfare = _cl(self.welfare + 0.02 * (wt - self.welfare) * (2 if self.open_q > 0 else 1), 0.05, 0.95)
        if abs(self.welfare - self.welfare_pub) >= 0.05:
            self._event("state", "welfare raised" if self.welfare > self.welfare_pub else "welfare cut", "welfare", round(self.welfare, 2), big=False)
            self.welfare_pub = round(self.welfare, 2)
        # rights (spec 1 §3): from the regime, the matching norms and laws, lockdowns
        nr = _sig(self.norm_x)
        tgt = self.rights_base * np.array([1.0, 0.85 + 0.15 * nr[NI["faith in public"]], 1.0 - self.lockdown,
                                           0.25 + 0.75 * np.mean([nr[NI["coming out"]], nr[NI["transition"]], (2 - self.laws[LI["same-sex marriage"]]) / 2]),
                                           0.35 + 0.65 * nr[NI["role crossing"]]])
        old = self.rights.copy()
        self.rights = _uclip(self.rights + 0.06 * (tgt - self.rights), 0, 1)
        self.rights[2] = min(self.rights[2], 1.0 - self.lockdown)
        for k in np.nonzero(np.floor(self.rights * 10) != np.floor(old * 10))[0]:
            self._event("state", "right gained" if self.rights[k] > old[k] else "right lost", RIGHTS[k], round(float(self.rights[k]), 1), big=False)
        # unrest (spec 1 §3): unemployment above natural, inequality, the gap between government and demand, repression
        rep = (1 - self.rights.mean()) * (self.regime < 6)
        ut = (0.25 * max(self.unemp - self.natural, 0) / 5 + 0.6 * max(self.ineq - 0.3, 0) + 1.5 * max(d - 0.08, 0)
              + 0.3 * rep + 0.4 * (self.war == 2) + 0.1 * (self.pandemic == 2) + 0.2 * (self.severity == 2) * (self.phase == 1)
              + 0.3 * self.lost_war_q / 8 + 0.15 * max(self.infl - 6, 0) / 6)
        self.unrest = _cl(self.unrest + 0.3 * (ut - self.unrest) + 0.01 * r.normal(), 0, 1)
        self._regime_derived()

    def _election(self, x, nz):
        p = self.p
        res = self.support + p["e_noise"] * (2 * x[0] - 1) * 1.7
        turnout = _cl(0.66 - 0.15 * (self.polar - 0.1) * 0 + 0.1 * (self.trust - 0.45) + 0.03 * (2 * x[1] - 1), 0.3, 0.9)
        if res < 0.5 and self._s3("hist_party_gov"):    # LW2 2a: the party closest to demand governs in its own colours,
            d = np.array([_tv(self.inst_profile[i], self.Dem) for i in self.party_ids])   # moved toward its voters, with
            d[self.gov_party] = 9                                                         # its leader's touch
            old = self.gov_party
            self._change_gov(int(np.argmin(d)), x[3])
            Pw = self.inst_profile[self.party_ids[self.gov_party]]
            fid = self.fig_role_now.get(0)
            L = np.asarray(self.F_pie[fid], float) if fid is not None and fid >= 0 else Pw
            self.G = _norm(Pw + p["gov_voter"] * (self.Dem - Pw) + p["lead_k"] * (L - Pw))
            self.s3_loser = (int(old), 4)
        elif res < 0.5:
            Gn = _norm(self.Dem + p["k_thermo"] * (self.Dem - self.G))
            self.G = _norm(Gn * np.exp(p["g_noise"] * nz))
            d = np.array([_tv(self.inst_profile[i], self.G) for i in self.party_ids])
            d[self.gov_party] = 9
            old = self.gov_party
            self._change_gov(int(np.argmin(d)), x[3])
            pid = self.party_ids[self.gov_party]
            self.inst_profile[pid] = 0.5 * self.inst_profile[pid] + 0.5 * self.G
        if res < 0.5:
            self.support = p["s_win"] + 0.02 * (2 * x[2] - 1)
            self._event("state", "election", "change", dict(party=self.gov_party, leader=self.fig, colors=self.G.round(2).tolist(),
                                                              support=round(float(res), 2), turnout=round(turnout, 2)), big=True)
        else:
            self.G = _norm(self.G + 0.2 * (self.Dem - self.G))
            self.support = float(0.5 + 0.5 * (res - 0.5) + 0.04)
            self._event("state", "election", "held", dict(party=self.gov_party, leader=self.fig, colors=self.G.round(2).tolist(),
                                                            support=round(float(res), 2), turnout=round(turnout, 2)), big=False)
        self.next_vote = 16 + int(x[3] * 5)

    def _change_gov(self, new, xv):
        """The governing party changes: the opposition leader of the new party becomes head of government, the old
        head leads the opposition; a new term starts."""
        old = self.gov_party
        self.gov_party, self.opp_party = new, old
        self.gov_q, self.u_at_office = 0, self.unemp
        self.n_gov_change = getattr(self, "n_gov_change", 0) + 1
        head_old, opp_old = self.fig_role_now.get(0), self.fig_role_now.get(1)
        if opp_old is not None and self.F_alive[opp_old] and self.F_party[opp_old] == new:
            self.F_standing[opp_old] = min(1.0, self.F_standing[opp_old] + 0.2)
            self.fig_role_now.pop(1, None)
            self._set_role(0, opp_old)
        else:
            self._new_fig(self.R[9], 0, quiet=True, party=new)
        if head_old is not None and self.F_alive[head_old]:
            self.F_party[head_old] = old
            self._set_role(1, head_old)
        else:
            self._new_fig(self.R[9], 1, quiet=True, party=old)
        self.next_vote = 16 + int(xv * 5)
        self.Q *= self.p["q_vote"]                         # the change people voted for releases pressure, and the new
        self.mandate_q = int(self.p["mandate_q"])          # order's distance from demand is its mandate for a while
        self._event("state", "government falls", None, dict(party=old), big=True)

    def _set_law(self, k, s):
        s = int(_uclip(s, 0, 2))
        if s == self.laws[k]:
            return
        old = self.laws[k]
        self.laws[k] = s
        self.law_since[k] = 0
        self._event("state", "law changed", LAW_KEYS[k], dict(state=LAW_STATES[s], was=LAW_STATES[old]), big=s != 1)

    # ------------------------------------------------------------------------------------------------ institutions (spec 4)
    def _inst_q(self):
        p, r = self.p, self.R[5]
        n = self.n_inst
        x = r.random((n, 8)); nz = self._cn(r, n)
        k = self.inst_kind
        pub = self.inst_public
        self.inst_age += 0.25
        # leaders: tenure about 6 years; public bodies' leaders are appointed by the government
        self.inst_leader_q += 1
        newl = (x[:, 0] < 1 / p["tenure_q"]) & (self.inst_leader_fig < 0)
        self.tenure_sum = getattr(self, "tenure_sum", 0.0) + float(self.inst_leader_q[newl].sum())   # hidden, for tests
        self.tenure_n = getattr(self, "tenure_n", 0) + int(newl.sum())
        base = np.where(pub[:, None], self.G, self.V)
        ls_ = p["lead_spread_s3"] if self._s3("hist_chance_only") else 0.3   # LW2 2e: who leads is chance, their colours
        self.inst_leader_pie = np.where(newl[:, None], _norm(base * np.exp(ls_ * nz)), self.inst_leader_pie)   # less so
        self.inst_leader_q = np.where(newl, 0, self.inst_leader_q)
        for i in np.nonzero(newl & (self.inst_level == 2))[0]:          # local routine changes stay off the record
            self._inst_event(i, "new leader")
        # profile drift: leader, mission, routine (toward White), oligarchy (toward Black), spec 4 §3
        prof = self.inst_profile
        party = k == INST_KINDS.index("party")
        if p.get("inst_even", False):    # colour-even: routine keeps the body's own past, oligarchy its leaders' colours
            if getattr(self, "inst_H", None) is None:   # the body's own past: a 25-year memory of its profile (H_mem)
                self.inst_H = prof.copy()
            rout_, olig_ = self.inst_H, self.inst_leader_pie
        else:
            rout_, olig_ = self.ROUT, self.OLIG
        dp = (p["inst_lead"] * (self.inst_leader_pie - prof) + p["inst_mission"] * (self.inst_native - prof)
              + p["inst_routine"] * np.minimum(self.inst_age, 100)[:, None] / 50 * (rout_ - prof)
              + p["inst_olig"] * self.inst_corruption[:, None] * (olig_ - prof))
        fb = self.inst_faith >= 0
        dp[fb] = 0.02 * (self.FPROF[self.inst_faith[fb]] - prof[fb])
        dp[party] = 0
        self.inst_profile = _norm(prof + dp)
        if p.get("inst_even", False):
            self.inst_H += self._sph_tables()["pr"]["H_mem"] * (self.inst_profile - self.inst_H)
        # capacity follows funding: the state budget, the market, members (spec 4 §3)
        budget = 0.6 + 0.4 * (self.welfare - self.p["welfare0"]) + 0.15 * self.gap
        ct = np.where(pub, self.capacity * (0.75 + 0.4 * budget), 0.45 + 0.45 * self.inst_finances)
        ct = np.where(fb, 0.4 + 0.8 * self.faith_share[np.maximum(self.inst_faith, 0)], ct)
        self.inst_capacity = _uclip(self.inst_capacity + 0.05 * (ct - self.inst_capacity) + 0.01 * r.normal(size=n), .05, 1)
        # corruption rises where oversight is weak and leaders entrench; falls with reform
        cterm = 0.12 * (1.9 - self.law_rule) / 1.0 * (1 + 0.3 * np.minimum(self.inst_leader_q / 24, 2))
        self.inst_corruption = _uclip(self.inst_corruption + 0.02 * (cterm * 0.85 - self.inst_corruption) + 0.006 * r.normal(size=n), .01, .9)
        self._state_corruption()
        # legitimacy follows performance, scandals, the media's mood and trust (OECD trust targets by kind)
        lt = self.inst_legit0 * (1 + 0.6 * (self.inst_capacity - 0.84)) * (1 - 0.8 * (self.inst_corruption - 0.14)) \
            * (0.45 + 0.55 * self.trust / self.p["trust0"] - 0.3 * (self.fear - self.p["fear0"]))
        gov = (k == INST_KINDS.index("ministry"))
        lt = np.where(gov, lt * (0.55 + 0.8 * (self.support - 0.5) + 0.45), lt)
        self.inst_legitimacy = _uclip(self.inst_legitimacy + 0.06 * (lt - self.inst_legitimacy), .02, .98)
        # openness by class and migrant status (R9): corruption favours insiders, trust and rights open doors
        oc = np.array([.78, .92, 1.0]) - np.array([.6, .2, 0.0])[None, :] * (self.inst_corruption[:, None] - 0.12) \
            - np.array([.4, .1, 0])[None, :] * (self.ineq - 0.32)
        self.inst_open_cls += 0.05 * (_uclip(oc, .2, 1) - self.inst_open_cls)
        om = 0.70 + 0.25 * (self.trust - 0.45) + 0.2 * (self.rights[0] - 0.85) - 0.3 * max(self.mig_in - 0.01, 0) * 20
        self.inst_open_mig += 0.05 * (_uclip(om, .3, 1) - self.inst_open_mig)
        self._openness()
        # firms live and die with the economy (business demography: 8-10% exit a year); public employers follow the
        # state's budget (welfare level and the public share), not the cycle (spec 1 §2)
        firm, pube = self.inst_firm, self.inst_pubemp
        cyc = np.array([0.9, 1.5, 1.0, 0.6, 0.3])[np.maximum(self.inst_sector, 0)]
        ftgt = np.where(pube, 0.5 + 1.2 * (self.welfare - p["welfare0"]), 0.5 + 0.5 * cyc * self.gap)
        self.inst_finances = _uclip(self.inst_finances + 0.15 * (ftgt - self.inst_finances)
                                     - 0.05 * self.automation[np.maximum(self.inst_sector, 0)] * firm + 0.05 * r.normal(size=n), -0.5, 1)
        ex = p["firm_exit"] * np.exp(-3 * (self.inst_finances - 0.5)) * np.where(self.inst_level == 2, p["firm_big"], 1.0)
        ex = np.where(pube, p["pub_exit"] * np.exp(-3 * (self.inst_finances - 0.5)), ex)
        close = (firm | pube) & (x[:, 1] < ex)
        # events: scandal, new leader, strike, budget cut, ruling, reform, closure (spec 4 §4)
        media_cap = self.inst_capacity[k == INST_KINDS.index("media")].mean()
        sc_ = p["scandal0"] + p["scandal_c"] * self.inst_corruption * media_cap * (0.5 + self.watch)
        if p.get("c3_inst") and getattr(self, "c3_cover", None) is not None:   # C3: a cover-up hides it, so it breaks
            hid_ = self.c3_cover > self.t                                      # three times as often, and at once
            sc_ = np.where(hid_, sc_ * self._c_par("cover_sc"), sc_)           # when an insider speaks up
            sc = ((x[:, 2] < sc_) | (hid_ & self.c3_break)) & ~party
            self.c3_cover = np.where(sc, 0, self.c3_cover); self.c3_break[:] = False
        else:
            sc = (x[:, 2] < sc_) & ~party
        for i in np.nonzero(sc)[0]:
            self.inst_legitimacy[i] -= 0.12; self.trust -= 0.002
            big = self.inst_level[i] == 2
            self._inst_event(i, "scandal", big=bool(big))
            if x[i, 3] < 0.5 and self.inst_leader_fig[i] < 0:
                self.inst_leader_q[i] = 0; self.inst_leader_pie[i] = _norm(base[i] * np.exp(ls_ * nz[i]))
                self._inst_event(i, "new leader")
            if self.inst_leader_fig[i] >= 0:
                self._fig_scandal(self.inst_leader_fig[i])
        ref = (self.inst_legitimacy < 0.22) & (x[:, 4] < 0.08)
        for i in np.nonzero(ref)[0]:
            self._reform_inst(i, self.inst_native[i])
        union = k == INST_KINDS.index("union")
        st = union & (x[:, 5] < 0.012 + 0.05 * max(self.infl - 3, 0) / 5 + 0.03 * (self.welfare < self.welfare_pub - 0.02))
        for i in np.nonzero(st)[0]:
            self._inst_event(i, "strike", big=self.infl > 6)
        if self.phase == 1 and self.rec_q == 3 and x[0, 6] < 0.6:
            cut = pub & (x[:, 6] < 0.25)
            self.inst_capacity[cut] *= 0.93
            self._event("institution", "budget cut", None, dict(n=int(cut.sum())), big=False)
        court = k == INST_KINDS.index("court")
        for i in np.nonzero(court & (x[:, 6] > 0.985))[0]:
            j = int(x[i, 0] * NL) % NL
            if _sig(self.norm_x[j]) > 0.55 and self.laws[j] > 0:
                self.law_push[j] += 0.6
            self._inst_event(i, "ruling", big=self.inst_level[i] == 2)
        if p.get("c3_inst"):                               # C3: some big closures in a deep recession are nationalised
            close = self._c3_nationalise(close)
        for i in np.nonzero(close)[0]:
            self._inst_event(i, "closure", big=self.inst_level[i] == 2)
            sec = int(self.inst_sector[i]) if self.inst_sector[i] >= 0 else 2
            g = SECTOR_GUILDS[sec][int(x[i, 7] * len(SECTOR_GUILDS[sec]))]
            self.inst_native[i] = self._profile_src(g); self.inst_profile[i] = self.inst_native[i].copy()
            if getattr(self, "inst_H", None) is not None:   # inst_even: a new body has no past but its founding
                self.inst_H[i] = self.inst_native[i].copy()
            self.inst_finances[i], self.inst_age[i], self.inst_gen[i] = 0.5, 0.0, self.inst_gen[i] + 1
            self.inst_corruption[i], self.inst_legitimacy[i], self.inst_leader_q[i] = 0.1, self.inst_legit0[i], 0
            self.inst_leader_pie[i] = _norm(self.V * np.exp(ls_ * nz[i]))
            self._inst_event(i, "new firm", big=False)
        self.n_closures = getattr(self, "n_closures", 0) + int(close.sum())
        if p.get("c3_inst"):
            self._c3_inst_q(close)

    def _inst_event(self, i, kind, big=False):
        self._event("institution", kind, INST_KINDS[self.inst_kind[i]], dict(inst=int(i), loc=int(self.inst_loc[i]),
                                                                          gen=int(self.inst_gen[i])), big=big)

    def _reform_inst(self, i, toward, step=0.4):
        self.inst_corruption[i] *= 0.5
        self.inst_profile[i] = _norm(self.inst_profile[i] + step * (toward - self.inst_profile[i]))
        self.inst_legitimacy[i] = min(0.95, self.inst_legitimacy[i] + 0.1)
        self._inst_event(i, "reform")

    # ------------------------------------------------------------------------------------------------ places (spec 3 §2)
    def _place_q(self):
        p, r = self.p, self.R[6]
        nl = self.n_loc
        x = r.random((nl, 3)); nz = self._cn(r, nl)
        self._derive_econ()
        # crime follows local unemployment, inequality and efficacy, with a lag (Sampson et al. 1997)
        nbl = self.nb_loc.astype(np.intp, copy=False)
        eff = np.bincount(nbl, self.nb_efficacy, nl) / np.bincount(nbl, None, nl)
        ct = self.loc_crime0 * (1 + 0.08 * (self.loc_unemp - self.natural * self.loc_ufac)) * (1 + 2.0 * (self.ineq - 0.32)) \
            * (1.35 - 0.6 * eff) / (1.35 - 0.6 * 0.57) * (1 + 0.3 * (self.war == 2))
        self.loc_crime = _uclip(self.loc_crime + 0.1 * (ct - self.loc_crime) + 0.01 * r.normal(size=nl), 0.01, 1)
        wave = (self.loc_crime > 1.3 * self.loc_crime_ma) & (x[:, 0] < 0.5)
        for l in np.nonzero(wave)[0]:
            self._event("place", "crime wave", None, dict(loc=int(l)), big=False)
            self.loc_crime_ma[l] = self.loc_crime[l]
        self.loc_crime_ma += 0.05 * (self.loc_crime - self.loc_crime_ma)
        nbf = np.array([1.6, 0.9, 0.5])[self.nb_class] * (1.4 - 0.8 * self.nb_efficacy) / (1.4 - 0.8 * 0.57)
        self.nb_crime = _uclip(self.loc_crime[self.nb_loc] * nbf, 0.005, 1)
        et = np.array([.45, .58, .70])[self.nb_class] + 0.3 * (self.trust - 0.45) - 0.2 * (self.loc_unemp[self.nb_loc] - 5) / 10
        self.nb_efficacy = _uclip(self.nb_efficacy + 0.03 * (et - self.nb_efficacy) + 0.01 * r.normal(size=self.n_nb), .05, .98)
        # rent follows the housing gap and local growth; services follow the state budget
        self.loc_rent = _uclip(self.loc_rent + 0.05 * (self.loc_rent0 * (1 + 0.5 * self.housing) * (1 + 3 * self.loc_growth) - self.loc_rent), 0.2, 4)
        st = np.array([[.6, .55, .4], [.7, .65, .55], [.8, .75, .7], [.85, .85, .85]])[self.loc_size] \
            * (0.8 + 0.4 * self.capacity) * (0.85 + 0.5 * (self.welfare - self.p["welfare0"]) + 0.1 * self.gap)
        self.loc_services = _uclip(self.loc_services + 0.04 * (st - self.loc_services), 0.05, 1)
        # local politics: own cycle, same thermostat
        self.loc_next_vote -= 1
        for l in np.nonzero(self.loc_next_vote <= 0)[0]:
            if x[l, 1] < 0.5:
                self.loc_gov[l] = _norm(_norm(self.loc_mix[l] + p["k_thermo"] * (self.loc_mix[l] - self.loc_gov[l])) * np.exp(0.25 * nz[l]))
                self._event("place", "local election", "change", dict(loc=int(l)), big=False)
            else:
                self._event("place", "local election", "held", dict(loc=int(l)), big=False)
            self.loc_next_vote[l] = 16 + int(x[l, 2] * 5)

    # ------------------------------------------------------------------------------------------------ culture (spec 1 §4)
    def _culture_q(self):
        p, r = self.p, self.R[7]
        nz = r.normal(size=NN)
        # norms: logit S-curves toward a target set by the modern baseline, the value climate, the era and the law
        fitV = (self.V - self.V_anchor) @ self.NPROF.T
        fitE = self.era_i * ((self.era_p - 0.2) @ self.NPROF.T) if self.era_key is not None else 0.0
        lawsign = np.zeros(NN); lawsign[:NL] = 1.0 - self.laws
        for kk, ri in NORM_RIGHT.items():
            lawsign[NI[kk]] = 2 * self.rights[ri] - 1
        speed = (self.norm_x - self.norm_hist[0]) / 5.0                # logit per year over the last 5 years
        old = self._share_old()
        back = p["norm_back"] * np.sign(speed) * np.maximum(np.abs(speed) - 0.08, 0) * old
        tgt = self.norm_x0 + p["norm_v"] * fitV + p["norm_era"] * fitE + p["norm_law"] * (lawsign - self.lawsign0) - back
        young = self._share_young()
        rr = p["norm_r"] / 4 * (1 + 2.0 * (young - 0.2)) * (1 + 0.5 * self.comm)
        if self._s3("cult_no_dice"):                       # LW1 1h: no dice in the culture
            nz = 0.0 * nz
        self.norm_x = self.norm_x + rr * _uclip(tgt - self.norm_x, -1, 1) + 0.25 * self.norm_push + 0.012 * nz
        self.norm_push *= 0.5
        self.norm_hist = np.roll(self.norm_hist, -1, 0); self.norm_hist[-1] = self.norm_x
        self.norm_speed = float(np.abs(speed).mean())
        # trust falls with scandals and polarisation, recovers slowly; media fear rises with crime and crises
        tt = p["trust0"] + 0.04 - 0.5 * max(self.polar - 0.12, 0) - 0.08 * (self.phase == 1) * self.severity - 0.1 * (self.unrest - 0.12)
        self.trust = _cl(self.trust + 0.03 * (tt - self.trust), 0.05, 0.9)
        ft = p["fear0"] + 0.6 * ((self.loc_pop_share * self.loc_crime).sum() / self.crime_ref - 1) + 0.15 * (self.phase == 1) \
            + 0.3 * (self.war > 0) + 0.2 * (self.pandemic in (1, 2)) + 0.1 * (self.loc_disaster > 0).mean()
        self.fear = _cl(self.fear + 0.2 * (ft - self.fear), 0.02, 1)

    def _share_old(self):
        return self.old_share

    def _share_young(self):
        return self.young_share

    def _place_w(self):
        """(3, n_loc) population weights of the localities in each place class."""
        m = (self.loc_place[None, :] == np.arange(3)[:, None]) * self.loc_pop_share[None, :]
        return m / m.sum(1, keepdims=True)

    # ------------------------------------------------------------------------------------------------ society (spec 6)
    def _pos(self):
        """What the order rewards (spec 6 §2): state and law, institutions by reach and capacity, the economy's payoff,
        the established faiths by share."""
        p = self.p
        lawmix = _norm(0.2 + 0.25 * ((1.0 - self.laws)[:, None] * (self.NPROF[:NL] - 0.2)).mean(0)
                       + 0.5 * (self.welfare - p["welfare0"]) * (self.WPROF - 0.2))
        S = p["w_gov"] * self.G + (1 - p["w_gov"]) * lawmix
        w = self.inst_reach * self.inst_capacity
        w = np.where(self.inst_faith >= 0, 0.0, w)
        I = (w[:, None] * self.inst_profile).sum(0) / w.sum()
        B = self.faith_share @ self.FPROF + self.secular * 0.2
        ws = p["w_pos"]
        self.pos_parts = np.array([S, I, self.payoff, B])
        return _norm(ws[0] * S + ws[1] * I + ws[2] * self.payoff + ws[3] * B)

    def _needs(self):
        """Unmet needs per population group (safety, belonging, autonomy, competence, meaning), 0 met .. 1 unmet, from
        the economy, the state, war, welfare, place, faith and how far the order rewards the group's ways."""
        a, c, pl, f, m = self.gidx
        PW = self._place_w()
        pu, pc, pdis = PW @ self.loc_unemp, PW @ self.loc_crime, PW @ np.minimum(self.loc_disaster, 1)
        u_g = pu[pl] * np.array([1.6, 0.9, 0.5])[c] * np.array([0, 1.8, 1.2, 1.0, 0.9, 1.0, 0.3, 0])[a] * np.where(m == 1, 1.5, 1.0)
        rel = (f > 0).astype(float)
        old = (a >= 6).astype(float)
        lower = (c == 0).astype(float)
        mis = np.maximum(_tv(self.gmix, self.Pos) - 0.08, 0)
        lawc = (self.gmix @ self.NPROF[:NL].T) @ (self.laws / 2.0) / NL      # how far the law book closes the group's ways
        speed = getattr(self, "norm_speed", 0.0)
        fastmig = max(self.mig_in - 0.008, 0) * 60
        safety = (0.10 + 0.04 * np.maximum(u_g - 4, 0) + 0.35 * (self.war == 2) + 0.06 * (self.war == 1) + 0.4 * pc[pl]
                  + 0.04 * max(self.infl - 3, 0) * (1 + lower) + 0.2 * (self.pandemic == 2) * (1 + old) + 0.3 * pdis[pl]
                  - 0.2 * (self.welfare - self.p["welfare0"]) * (1 + lower))
        belong = (0.25 - 0.10 * rel + 0.15 * m * (1 - self.inst_open_mig.mean()) * 2 + 0.10 * (a == 7) + 0.05 * (pl == 0)
                  + 2.0 * speed * (a >= 5) + 0.3 * fastmig * (m == 0) * (a >= 4) + 0.15 * (0.45 - self.trust))
        auton = 0.15 + 0.6 * (1 - self.rights.mean()) + 1.2 * lawc + 0.8 * mis + 0.3 * self.lockdown
        compet = 0.15 + 0.04 * np.maximum(u_g - 4, 0) + 0.3 * (self.automation.mean()) * lower + 0.8 * mis
        mean_ = 0.20 - 0.12 * rel + 0.08 * (1 - rel) * (self.phase == 1) + 0.8 * mis + 1.0 * speed
        U = _uclip(np.stack([safety, belong, auton, compet, mean_], 1), 0, 1)
        return U

    def _society_q(self):
        p, r = self.p, self.R[8]
        x = r.random(6); nz = self._cn(r)
        self.Pos = self._pos()
        # demand: the groups' wanted colors (their mix plus what their unmet needs ask for, NEED_MAP_V6), by size and
        # voice for elections, by size and mobilisation for pressure (spec 6 §3)
        U = self._needs()
        want = _norm(self.gmix + p["zeta"] * (U @ self.NEEDM))
        size = self.pop.reshape(-1) * self.gadult
        voice = np.where(self.gidx[4] == 1, 0.3, 1.0) * (0.15 + 0.85 * self.demo) * np.where(self.gidx[0] == 1, 0.7, 1.0)
        voice = np.where(self.gidx[1] == 2, np.maximum(voice, 0.5), voice)
        wv = size * voice
        wq = size * (1 + p["mobil"] * U.sum(1))
        if self._s3("hist_grievance") and getattr(self, "s3_grv", None) is not None:   # LW2 2d: those the last change
            wq = wq * (1 + self.s3_grv)                                                # left behind push harder
        D0 = (wv[:, None] * want).sum(0) / wv.sum()
        Dq0 = (wq[:, None] * want).sum(0) / wq.sum()
        self.D0 = D0                                       # demand before the thermostat (hidden; tests)
        th_ = p["th_dem_s3" if self._s3("hist_party_gov") else "th_dem"]   # LW2 2b: the thermostat, refit with 2a
        self.Dem = _norm(D0 - th_ * (self.G - D0))
        self.Dem_q = _norm(Dq0 - th_ * (self.G - Dq0) + getattr(self, "dem_push", np.zeros(C)))
        self.dem_push = getattr(self, "dem_push", np.zeros(C)) * 0.8
        self.polar = float((size * _tv(want, D0)).sum() / size.sum())
        um = (size[:, None] * U).sum(0) / size.sum()
        self.unmet_mean = um
        self.need_base += 0.02 * (um - self.need_base)
        self.group_unmet = U
        # pressure, accelerators, inertia (spec 6 §4)
        gap = _tv(self.Pos, self.Dem_q)
        rec = (self.phase == 1) * (1 + self.severity) / 3
        tn = np.array(self.tech_kind) >= 0                 # new kinds spreading fast
        tech = float((self.tech_adopt_v[tn] * (1 - self.tech_adopt_v[tn])).mean() * 4) if tn.any() else 0.0
        mixed = -5 <= self.regime < 6                      # half open, half closed: the least stable (Hegre et al. 2001)
        acc = (1 + 1.0 * rec + 1.5 * self.unrest + 2.0 * (self._share_young() - 0.25) + 0.3 * tech
               + 0.5 * (self.ext_trade.sum() + 10 * self.mig_in) * 0.3 + 0.5 * max(p["trust0"] - self.trust, 0) * 4
               + 0.8 * (self.lost_war_q > 0) + p["mixed_acc"] * mixed)
        self.gap_slow += p["q_hab_r"] * (gap - self.gap_slow)        # people get used to a gap they have long lived with
        if getattr(self, "mandate_q", 0) > 0:                         # ... and give a new government its mandate
            self.gap_slow = max(self.gap_slow, gap)
            self.mandate_q -= 1
        self.gap_now = gap
        hp_ = self._s3("hist_pressure")
        exc = max(gap - p["q_tol_s3" if hp_ else "q_tol"]
                  - p["q_hab_s3" if hp_ else "q_hab"] * (p["mixed_hab"] if mixed else 1.0) * self.gap_slow, 0)
        self.Q = self.Q * (1 - p["q_decay_s3" if hp_ else "q_decay"]) + self.pace * p["q_k_s3" if hp_ else "q_k"] * exc * max(acc, 0.2)
        self._s3_society(U, want, size, wv, wq, D0, acc)
        age_i = float(np.minimum(self.inst_age, 120) @ self.inst_reach) / (float(self.inst_reach.sum()) + 1e-9) / 60
        rigid = float((self.law_since > 20).sum()) / NL
        hold = (0.55 + 0.15 * age_i + 0.2 * self.capacity + 0.15 * rigid + 1.0 * (self._share_old() - 0.25)
                + 0.4 * (self.regime < -5) * (1 - self.demo) - p["mixed_hold"] * mixed)
        self.hold = hold
        self.q_thr = p["q_theta_s3" if hp_ else "q_theta"] * max(hold, 0.2) ** p["q_hold"]
        self.open_q = max(self.open_q - 1, 0)
        self.since_break += 0.25
        if self.Q > self.q_thr:
            self._breakthrough(U, want, size, x, nz)       # (it recomputes Pos)
        self.pos_hist = np.roll(self.pos_hist, -1, 0); self.pos_hist[-1] = self.Pos
        self._era()

    def _breakthrough(self, U, want, size, x, nz):
        """Reform, revolution, revival or restoration (spec 6 §5); then pressure resets and the society stays open."""
        p = self.p
        pos_before = self.Pos.copy()
        exc = self.unmet_mean - self.need_base
        change = _tv(self.Pos, self.pos_hist[0])
        if self.regime < 6 and (self.unrest > 0.3 or (self.phase == 1 and self.severity == 2) or self.war == 2 or self.lost_war_q > 0):
            kind = 1
        elif exc[4] > 0.02 and exc[4] >= exc.max() - 1e-12:
            kind = 2
        elif change > 0.05 and (exc[1] > 0.01 or self.norm_speed > 0.06):
            kind = 3
        else:
            kind = 0
        step = p["q_step"][kind]
        if kind == 1:                                        # toward the most mobilised groups, not the majority
            w = size * U.sum(1) ** 3
            T = _norm((w[:, None] * want).sum(0) / w.sum())
        elif kind == 3:                                      # toward the losers of the last change
            loss = np.maximum(_tv(self.gmix, self.Pos) - _tv(self.gmix, self.pos_hist[0]), 0)
            w = size * (loss + 1e-6)
            T = _norm(0.5 * (w[:, None] * want).sum(0) / w.sum() + 0.5 * self.pos_hist[0])
        else:
            T = self.Dem_q
        self._event("era", "breakthrough", BREAKTHROUGHS[kind], dict(regime=round(float(self.regime), 1)), big=True)
        self.last_break = BREAKTHROUGHS[kind]
        self.n_break = getattr(self, "n_break", 0) + 1
        if kind == 2:                                        # revival: belief and norms first (spec 6 §5)
            fit_ = self.FPROF @ ((U[:, 4] * size)[:, None] * want).sum(0)
            if len(fit_) > NF:                             # C5: only a living movement can be revived
                fit_[NF:] = np.where(self.faith_open(0.0)[NF:], fit_[NF:], -np.inf)
            f = int(np.argmax(fit_))                       # the faith that fits the unmet
            self.revival = (f, 8)
            self.norm_x += 0.6 * ((self.FPROF[f] - 0.2) @ self.NPROF.T) * 5
            self.G = _norm(self.G + step * (T - self.G))
            self._event("belief", "revival", None, dict(faith=f), big=True)
        else:                                                # a landslide or a wave of reforms: the order is formed anew
            Gt = T if self._s3("hist_pressure") else _norm(T * np.exp(0.5 * p["g_noise"] * nz))   # 2c: no spread
            self.G = Gt if kind != 0 else _norm(self.G + p["ref_g"] * (Gt - self.G))   # a reform goes part of the way
            old = self.gov_party
            d = np.array([_tv(self.inst_profile[i], self.G) for i in self.party_ids])
            if kind != 0:
                d[old] = 9                                   # a revolution or restoration removes the governing party
            else:
                d[old] -= p["break_keep"]                    # a reform wave the governing party can lead itself
            if int(np.argmin(d)) != old:                     # a landslide: the party that fits it best, a new term
                self._change_gov(int(np.argmin(d)), x[1])
                self.support = p["s_win"] + 0.05
            else:
                self.support = min(0.95, self.support + 0.05)
            pid = self.party_ids[self.gov_party]
            if not self._s3("hist_party_gov"):               # 2a: a party keeps its own colours; they move with its voters
                self.inst_profile[pid] = 0.5 * self.inst_profile[pid] + 0.5 * self.G
        # laws: a burst of landmark laws toward the target; institutions reorganised toward it
        fit = (T - 0.2) @ self.NPROF[:NL].T
        n = _sig(self.norm_x[:NL])
        for k_ in range(NL):
            if fit[k_] > 0.02 and n[k_] > 0.5 and self.laws[k_] > 0 and x[2] < step * 2:      # laws trail norms
                self._set_law(k_, self.laws[k_] - 1)
            elif fit[k_] < -0.02 and n[k_] < 0.5 and self.laws[k_] < 2 and x[3] < step * 2:
                self._set_law(k_, self.laws[k_] + 1)
        pub = np.nonzero(self.inst_public | (self.inst_kind == INST_KINDS.index("media")))[0]
        self.inst_profile[pub] = _norm(self.inst_profile[pub] + step * (T - self.inst_profile[pub]))
        self.inst_corruption[pub] *= 1 - 0.5 * step
        if kind == 1:                                        # the regime falls: toward the mobilised groups' voice
            self.regime = _cl(self.regime + (8 if x[4] < 0.6 else -6) * (0.5 + x[5]), -10, 10)
            self.unrest = min(1.0, self.unrest + 0.3)
            self._event("state", "regime changes", None, dict(regime=round(self.regime, 1)), big=True)
            self._regime_derived()
        self.Q = 0.0
        self.Pos = self._pos()
        if self._s3("hist_grievance"):                     # LW2 2d: who lost by this change keeps it in mind
            self._grieve(want, pos_before, self.Pos)
        self.gap_slow = _tv(self.Pos, self.Dem_q)          # the new order becomes what people measure against
        self.open_q = int(p["q_open"][kind] * 4)
        self.since_break = 0.0
        self.break_kind = kind
        self.break_t = self.t

    # ---- stage 3 of the v22 update (chroma-world/model/stage3-rules.md §2 and §3)
    def _m_sh(self):
        """LW1 1g: how shaken the last year was, 1 (calm) to 3, from the year's mean of the accelerators."""
        p = self.p
        a = getattr(self, "s3_acc", None)
        acc = float(np.mean(a)) if a else p["acc_calm"]
        return float(_cl(1 + p["k_sh"] * (acc - p["acc_calm"]), 1, 3))

    def _s3_young_pull(self):
        """LW1 1b and 1c: what schools and media stand for, and the movements of the time, pulling the young."""
        p, out = self.p, np.zeros(C)
        if self._s3("cult_schools"):
            k = self.inst_kind
            sm = np.isin(k, [INST_KINDS.index("school"), INST_KINDS.index("university"), INST_KINDS.index("media")])
            w = self.inst_capacity[sm] * self.inst_reach[sm]
            if w.sum() > 0:
                out += p["coh_inst"] * ((w[:, None] * self.inst_profile[sm]).sum(0) / w.sum() - self.Vc)
        if self._s3("cult_scenes") and getattr(self, "s3_mw", None) is not None:
            out += p["coh_scene"] * self.s3_mob * (self.s3_mw - self.Vc)
        return out

    def _grieve(self, want, before, after):
        """LW2 2d: each group's loss from a change of the order becomes a grievance that fades over years."""
        loss = np.maximum(_tv(want, after) - _tv(want, before), 0)
        g = getattr(self, "s3_grv", None)
        self.s3_grv = (np.zeros(len(loss)) if g is None else g) + self.p["lose_k"] * loss

    def _s3_society(self, U, want, size, wv, wq, D0, acc):
        """The stage 3 rules that read society's quarter: the shake (1g), movements (1c), parties (2a'), grievances."""
        p = self.p
        if not any(self._s3(k) for k in S3_RULES):
            return
        self.s3_want, self.s3_size = want, size
        if self._s3("cult_shake"):                         # 1g, plus fast growth: the gap a deviation above its mean
            gm = getattr(self, "s3_gap_m", None)
            if gm is None:
                gm, gv = float(self.gap), 0.0
            else:
                gv = self.s3_gap_v
            gm += 0.01 * (self.gap - gm); gv += 0.01 * ((self.gap - gm) ** 2 - gv)
            self.s3_gap_m, self.s3_gap_v = gm, gv
            self.s3_boom_q = (getattr(self, "s3_boom_q", 0) + 1) if self.gap - gm > np.sqrt(max(gv, 1e-12)) else 0
            self.acc = float(acc + 0.5 * (self.s3_boom_q >= 4))
            self.s3_acc = (getattr(self, "s3_acc", []) + [self.acc])[-4:]
        if self._s3("cult_scenes"):                        # 1c: the movements of the time (and a revival's faith)
            u = 1 + p["mobil"] * U.sum(1)
            ub = float((size * u).sum() / size.sum())
            w = size * np.maximum(u - ub, 0)
            mw = (w[:, None] * want).sum(0) / w.sum() if w.sum() > 0 else self.Vc.copy()
            m0 = getattr(self, "s3_mob_m", None)
            m0 = ub if m0 is None else m0 + (ub - m0) / 200
            self.s3_mob_m = m0
            mob = float(_cl(ub / m0 - 1, 0, 1))
            rv = getattr(self, "revival", (0, 0))
            if rv[1] > 0:
                mw, mob = 0.5 * mw + 0.5 * self.FPROF[rv[0]], max(mob, 0.5)
            self.s3_mw, self.s3_mob = _norm(mw), mob
        if self._s3("hist_party_gov"):                     # 2a': parties move slowly with their voters
            ids = self.party_ids
            prof = self.inst_profile[ids]
            close = np.argmin(0.5 * np.abs(want[:, None, :] - prof[None]).sum(-1), 1)
            lam = _cl((self._m_sh() - 1) / 2, 0, 1) if self._s3("cult_shake") else 0.0
            w = (1 - lam) * wv + lam * wq
            ls = getattr(self, "s3_loser", (-1, 0))
            for j in range(len(ids)):
                sel = close == j
                if w[sel].sum() > 0:
                    B = (w[sel][:, None] * want[sel]).sum(0) / w[sel].sum()
                    prof[j] = prof[j] + p["party_k"] * (B - prof[j])
                if j == ls[0] and ls[1] > 0:
                    prof[j] = prof[j] + p["loser_k"] * (D0 - prof[j])
            self.inst_profile[ids] = _norm(prof)
            if ls[1] > 0:
                self.s3_loser = (ls[0], ls[1] - 1)
        if self._s3("hist_grievance") and getattr(self, "s3_grv", None) is not None:
            if len(self.s3_grv) != len(want):
                self.s3_grv = np.zeros(len(want))
            self.s3_grv = self.s3_grv * (1 - p["grv_fade"] / 4)

    def _era(self):
        """Name what emerges (spec 6 §6): an era while Pos leans clearly toward one combination.

        The lean is read from the society's own slow normal (era_ref = 1), not from even: a typical rich society leans
        the same way from even all the time, which would name one endless era. Intensity is that lean, scaled. An era
        ends when the lean fades (era_off) or when the order has pointed elsewhere for era_switch quarters (at once
        after a breakthrough that turns it), and the next can begin at once. Swing is not a rule here: it comes from
        the thermostat in Dem and from the normal following the order."""
        p = self.p
        lam = p["era_ref"]
        self.Pos_era += p["era_smooth"] * (self.Pos - self.Pos_era)     # a stretch of years, not one quarter
        self.Pos_slow += p["era_mem"] * (self.Pos_era - self.Pos_slow)
        ref = (1 - lam) * 0.2 + lam * self.Pos_slow
        d = self.Pos_era - ref
        lean = 0.5 * np.abs(d).sum()
        nd = np.linalg.norm(d)
        best = int(np.argmax(COMBO_DIR @ d)) if nd > 0 else -1
        self.lean = lean
        e_on, e_off = self._era_th()
        just = getattr(self, "break_t", -1) == self.t
        if just and getattr(self, "break_kind", 0) == 2 and best >= 0 and not (self.era_key is not None and self.era_k == 2):
            if self.era_key is not None:                      # a revival is a cosmology era (spec 6 §5-6): it ends the
                self._era_end()                               # running one and names its own, even on a faint lean
            self._era_begin(best, max(lean, e_on))
            return
        if self.era_key is None:
            if lean > e_on and best >= 0:
                self._era_begin(best, lean)
            return
        cur = COMBO_KEYS.index(self.era_key)
        if lean < e_off:
            self._era_end()
            return
        cos = float(COMBO_DIR[cur] @ d / nd)
        if cos < p["era_keep"] and best != cur:              # the order has turned elsewhere
            self.era_lead_q += 1
            if self.era_lead_q >= p["era_switch"] or (just and cos < 0):
                self._era_end()
                if lean > e_on:
                    self._era_begin(best, lean)
                return
        else:
            self.era_lead_q = 0
        self.era_i = float(0.8 * self.era_i + 0.2 * self._inten(lean))

    def _inten(self, lean):
        p = self.p
        e_on = self._era_th()[0]
        return _cl(0.3 + 0.7 * (lean - e_on) / (p["era_hi"] - e_on), 0.3, 1.0)

    def _era_th(self):
        """The era's start and end leans (LW2 2c refits them when pressure alone makes the eras)."""
        p = self.p
        return (p["era_on_s3"], p["era_off_s3"]) if self._s3("hist_pressure") else (p["era_on"], p["era_off"])

    def _era_begin(self, best, lean):
        key = COMBO_KEYS[best]
        if getattr(self, "break_t", -10 ** 9) >= self.t - 8 * 13 and getattr(self, "break_kind", 0) == 2:   # 2 years
            kind = 2
        else:
            u = COMBO_DIR[best]
            c = np.array([(self.p["w_pos"][0] * (self.pos_parts[0] - 0.2)) @ u,
                          (self.p["w_pos"][1] * (self.pos_parts[1] - 0.2) + self.p["w_pos"][2] * (self.pos_parts[2] - 0.2)) @ u,
                          (self.p["w_pos"][3] * (self.pos_parts[3] - 0.2)) @ u])
            kind = int(np.argmax(c - c.mean()))
        self.era_key, self.era_k, self.era_i = key, kind, self._inten(lean)
        self.era_p = COMBO_MIX[best].copy()
        self.era_since, self.era_lead, self.era_lead_q = self.t, -1, 0
        self.n_era += 1
        by_break = getattr(self, "break_t", -10 ** 9) >= self.t - 8 * 13
        self.era_at.append([self.t, key, round(self.era_i, 3), ERA_KINDS[kind]])
        if self._s3("hist_grievance") and getattr(self, "s3_want", None) is not None:   # LW2 2d
            if getattr(self, "s3_grv", None) is None or len(self.s3_grv) != len(self.s3_want):
                self.s3_grv = np.zeros(len(self.s3_want))
            w_ = self.s3_size * self.s3_grv
            if w_.sum() > 0:                               # what the last change's losers want, as this era starts (tests)
                self.s3_era_ans = getattr(self, "s3_era_ans", []) + [(int(self.t), ((w_[:, None] * self.s3_want).sum(0)
                                                                                     / w_.sum()).tolist(), key)]
            self._grieve(self.s3_want, self.Pos_slow, self.Pos_era)
        self._event("era", "era begins", key, dict(kind=ERA_KINDS[kind], idea=IDEAS[key][0], intensity=round(self.era_i, 2),
                                                    breakthrough=bool(by_break)), big=True)

    def _era_end(self):
        self._event("era", "era ends", self.era_key, dict(years=round((self.t - self.era_since) / 52, 1)), big=True)
        self.era_key, self.era_i, self.era_k, self.era_p = None, 0.0, 0, np.zeros(C)
