"""People's methods for the cast's own lives, wants and far ties.

Part of class People (world_people.py), which inherits LivesMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import numpy as np
from world_keys import CAST_WANTS, GROUP_KINDS, SECTORS, TOUCHES, WHO_SLOTS
from world_people_base import (BIT, C, CORE, FARW, FAR_DEFAULT, FAR_OFF, FAR_WHO, G, KID, KINMASK, KTA, K_CHURN,
    K_LEAD, LOCAL_KINDS, NEVER, NW_ARISE, PAR, R, WANT_FX, WANT_RATE, WI, _LOWBIT, _csum, _ix, _norm, _nz2, _uclip,
    likeness)


class LivesMixin:
    # ------------------------------------------------------------------ the cast's own lives (light; ruling R8)
    def _lives(self, t, dy=0.5):
        """Every half year (dy: years since the last step): health and illness, jobs, partners, children, moves, mood
        and colors of every cast member (light lives, ruling R8); whole (N, K) arrays, masked to the living, float32."""
        P = self.P; rng = self.rng; N = self.N; f32 = np.float32; nq = dy / 0.25   # quarters
        live = self.used & self.lv & ~self.dead[:, None]
        if not live.any():
            return
        U = rng.random((6,) + live.shape, dtype=f32)
        age = self._qage if getattr(self, "_qage_t", None) == t else (t - self.born).astype(f32) * f32(1 / 52.0)
        rm = self.rmask; part = (rm & BIT["partner"]) != 0
        # health: the age curve, serious illness (season, pandemic and medicine through W.rate_mult)
        hb = _uclip(f32(1) - f32(0.012) * np.maximum(age - 35, f32(0)), f32(0.2), f32(1))
        x_ = np.maximum(age - 30, f32(0))
        tk_ = self.far_par["take"] if self.far_on else None   # far_ties: the towns' events take over a share
        ill = live & (U[0] < (f32(P["ill_p"][0]) + f32(P["ill_p"][1] / 10) * x_ * np.sqrt(x_))
                      * f32(dy if tk_ is None else dy * (1 - tk_[2])) * self._rate_at("illness", self.mloc))
        h = self.health
        self.health = _uclip(h + f32(1 - 0.85 ** nq) * (hb - h) - f32(0.35) * ill, f32(0.02), f32(1))   # (the dead's drift is unread)
        # jobs: loss by the economy and sector, finding work by unemployment, retirement
        jm = np.asarray(self._rate("jobloss"), float)
        sec = self.sector
        jl = np.take(jm.astype(f32), _ix(sec), mode="clip") if jm.ndim == 1 and len(jm) > 1 else f32(jm)
        emp = self.emp
        lose = live & emp & (U[1] < f32(P["jobloss"] * dy if tk_ is None else P["jobloss"] * dy * (1 - tk_[0])) * jl)
        un = float(self._unemp("unemp")); nat = float(self._unemp("natural"))
        wa = (age >= 18) & (age < 64) & (sec >= 0)
        find = live & ~emp & wa & (U[2] < np.where(age < 19, f32(1 - 0.5 ** nq),
                                                   f32(min(1.0, P["rehire"] * _uclip(1 - 4 * (un - nat), 0.3, 1.5) * dy
                                                           * (1 if tk_ is None else 1 - tk_[1])))))
        emp2 = ((emp & ~lose) | find) & (age < 65)
        self.emp = emp2
        tm = (np.take(np.array([0.3, 0.5, 0.75], f32), _ix(self.mcls), mode="clip") + f32(0.12) * emp2
              - f32(0.15) * (~emp2 & (age >= 18) & (age < 65)))
        self.money = _uclip(self.money + f32(1 - 0.8 ** nq) * (tm - self.money), f32(0.02), f32(1))
        # partners, divorces, children (the character's own partner follows the engine)
        mp = self.mpart
        cpl = live & ~mp & (age >= 20) & (age < 70) & (U[3] < P["couple_p"] * dy)
        div = live & mp & (age < 75) & ~part & (U[3] < P["divorce_p"] * dy)
        self.mpart = (mp | cpl) & ~div
        kid = live & self.mpart & ~part & (age >= 22) & (age < 42) & (self.nkids < 4) & (U[4] < P["kid_p"] * dy)
        self.nkids = (self.nkids + kid).astype(np.int8)
        # moves away (a share of all moves leave the locality); the household does not move without the character
        hj = self.hhj[:, None]
        inhh = (hj >= 0) & (((self.mset >> np.maximum(hj, 0).astype(self.mset.dtype)) & 1) > 0)
        mr = np.take(self._mr_tab, age.astype(np.intp), mode="clip")
        mv = live & (age >= 18) & ~inhh & (U[5] < mr * f32(P["far_share"] * dy))
        if mv.any():
            mn, mk = _nz2(mv)
            nl_ = rng.choice(self.n_loc, len(mn), p=self.loc_p)
            if self._xsoc:   # people living in another society move there (their places are not modelled here)
                nl_ = np.where(self.msoc[mn, mk] == self.soc[mn], nl_, self.mloc[mn, mk])
            self.mloc[mn, mk] = nl_
            loc_bits = np.zeros(len(mn), self.mset.dtype)
            for j_ in range(self.M):
                loc_bits |= np.where(np.isin(self.skind[mn, j_], LOCAL_KINDS), self._bit(j_), 0).astype(self.mset.dtype)
            self.mset[mn, mk] &= ~loc_bits
        # mood: events knock it down, it comes back
        bad = ill | lose | div
        self.mood = _uclip(self.mood + f32(1 - 0.8 ** nq) * (f32(0.6) - self.mood) - f32(0.3) * bad, f32(0), f32(1))
        # colors: a slow drift toward their surroundings, faster when young; the character's children toward the
        # household (upbringing); partners barely converge (Caspi, Herbener and Ozer 1992); a step after a big event
        dn, dk = _nz2(live & ((age < 25) | (self.c >= P["layer_c"][2]) | part))
        da, dp = age[dn, dk], part[dn, dk]
        rate = f32(nq) * np.where(dp, f32(0.0015), np.interp(da, [0, 12, 18, 25, 40, 60], [0.04, 0.04, 0.03, 0.01, 0.004, 0.002]).astype(f32))
        jf = _LOWBIT[self.mset[dn, dk]]   # the context: the first group they share with the character, else the place
        lm = _norm(np.asarray(self.W.loc_mix, float)).astype(f32)
        ctx = np.take(lm, _ix(self.mloc[dn, dk]), axis=0, mode="clip")
        hj_ = jf >= 0
        ctx[hj_] = self.snorm[dn[hj_], jf[hj_]]
        ctx[dp] = self.w32[dn[dp]]
        chm = ((self.rmask[dn, dk] & BIT["child"]) != 0) & (da < 18) & (self.hhj[dn] >= 0)
        if chm.any():   # the character's children are brought up in the household
            ctx[chm] = self.snorm[dn[chm], self.hhj[dn[chm]]]
        pi = self.pie[dn, dk]
        pi += rate[:, None] * (ctx - pi)
        bd = bad[dn, dk]
        if bd.any():
            st_ = (0.05 * (1 - _uclip(da[bd], 0, 90) / 100))[:, None]
            pi[bd] += st_ * (self._dirichlet(np.full((int(bd.sum()), C), 1.0 / C), 1.0) - pi[bd])
        self.pie[dn, dk] = pi = _norm(pi)
        self._psq[dn, dk] = _csum(pi * pi)
        # what reaches the character: their crises sharpen the reading; events of the close
        close = live & (self.c >= P["layer_c"][2])
        cr = close & bad
        rv_ = None
        if cr.any():
            cn, ck = np.nonzero(cr)
            r_old = self.read[cn, ck]
            err0 = 0.5 * np.abs(r_old - self.pie[cn, ck]).sum(-1)
            self.read[cn, ck] = r_old + 0.3 * (self.pie[cn, ck] - r_old)
            rv_ = (err0 >= 0.45) & self.watch[cn]   # (cn, ck) in row order: the order _nz2 gives
        L2 = P["layer_c"][1]
        wn = self.watch[:, None] & close
        for kind_, m_ in (("ill", ill), ("lost_job", lose), ("divorce", div), ("moved_away", mv)):
            self._evs(*_nz2(m_ & wn), t, kind_)
        if rv_ is not None and rv_.any():   # a crisis shows who they are: the reading before and after
            rn, rk = cn[rv_], ck[rv_]
            self.events.extend(dict(n=n_, t=int(t), kind="reveal", cid=u_, role=r_, old=[round(float(x_), 3) for x_ in o_],
                                    new=[round(float(x_), 3) for x_ in w_])
                               for n_, u_, r_, o_, w_ in zip(rn.tolist(), self.uid[rn, rk].tolist(), self._rnames(rn, rk),
                                                             r_old[rv_], self.read[rn, rk]))
        c2 = self.c >= L2
        self.cont_t[(div & c2).any(1), 0] = t; self.cont_t[(lose & c2).any(1), 1] = t
        # the character's children's children; siblings' children
        gk = kid & ((rm & (BIT["child"] | BIT["sibling"])) != 0)
        if gk.any():
            gn, gkk = _nz2(gk)
            F = self._gen(gn, np.full(len(gn), t), t, ctx=self.pie[gn, gkk], sel=P["pie_inherit"])
            F["mloc"] = self.mloc[gn, gkk]; F["line"] = self.line[gn, gkk]; F["msoc"] = self.msoc[gn, gkk]
            self._inherit(F, self.faith[gn, gkk], self.party[gn, gkk])
            isch = (self.rmask[gn, gkk] & BIT["child"]) != 0
            sl = self._add(F, t, np.where(isch, R["grandchild"], R["kin"]), c0=np.where(isch, 0.35, 0.12), trust0=0.6,
                           kof=self.uid[gn, gkk], quiet=True)
            for n_, s_, ok_ in zip(gn, sl, isch):
                if self.watch[n_] and ok_ and s_ >= 0:
                    self.events.append(dict(n=int(n_), t=int(t), kind="born", cid=int(self.uid[n_, s_]), role="grandchild"))

    def _inherit(self, F, faith, party):
        """Faith and party pass from a parent most strongly (p_inherit)."""
        E = len(F["n"]); pi = self.P["p_inherit"]
        F["faith"] = np.where(self.rng.random(E) < pi, faith, F["faith"])
        F["party"] = np.where(self.rng.random(E) < pi, party, F["party"])
        return F

    def _membership(self, t):
        """Settings keep their size: members leave (turnover, moves, deaths) and new ones are met."""
        P = self.P; rng = self.rng; N, M = self.N, self.M
        act = (self.skind >= 0) & (self.skind != G["household"])
        churn = np.where(act, KTA[np.maximum(self.skind, 0), K_CHURN] * 0.25, 0).astype(np.float32)
        keep = np.zeros((N, self.K), bool)
        ls = self.slead
        keep[np.nonzero(ls >= 0)[0], ls[ls >= 0]] = True
        mn, mk = _nz2((self.mset > 0) & ~keep)   # members leave each of their groups at its turnover
        if len(mn):
            u_ = rng.random(len(mn), dtype=np.float32)
            gone = ((u_[:, None] < churn[mn]) * (1 << np.arange(M))).sum(1).astype(self.mset.dtype)
            self.mset[mn, mk] &= ~gone
        B = self._bits()
        cnt = self._count(B)
        deficit = np.where(act, np.maximum(self.sncast - cnt.astype(np.int64), 0), 0)
        if deficit.any():
            nn, jj = np.nonzero(deficit)
            rep = deficit[nn, jj]
            self._members(np.repeat(nn, _ix(rep)), np.repeat(jj, _ix(rep)), t, quiet=True)
        # a leader who left or died is replaced by the most standing member
        for n_, j_ in zip(*np.nonzero(act & (self.slead == -1) & np.isin(self.skind, [G[g_] for g_ in GROUP_KINDS if K_LEAD[G[g_]]]))):
            mem = np.nonzero(B[n_, :, j_] > 0)[0]
            if len(mem):
                k_ = int(mem[np.argmax(self.stand[n_, mem] + 0.1 * rng.random(len(mem)))])
                if self.lw and self._lead_vacant(n_, j_, k_, t):   # S7: the character stands higher and takes the lead
                    continue
                self.slead[n_, j_] = k_
                lr = K_LEAD[int(self.skind[n_, j_])]
                self.rmask[n_, k_] |= BIT[lr]

    def _new_people(self, t):
        """By chance and through others: strangers who stay, friends of friends (quarterly)."""
        rng = self.rng; N = self.N; a = self._age(t); P = self.P
        live = ~self.dead
        if a < 3:
            return
        L2 = P["layer_c"][1]
        nfr = (((self.rmask & BIT["friend"]) != 0) & (self.c >= L2) & self.lv).sum(1)
        lam_ff = P["meet"][0] * np.minimum(nfr, 6) / 3 * (a >= 12) * self.sociab
        lam_ch = P["meet"][1] * (a >= 14) * self.sociab
        k_ff = rng.poisson(lam_ff) * live; k_ch = rng.poisson(lam_ch) * live
        nn = np.repeat(np.arange(N), _ix(k_ff))
        if len(nn):   # someone a friend brings along: alike the friend
            frm = ((self.rmask[nn] & BIT["friend"]) != 0) & (self.c[nn] >= L2) & self.lv[nn]
            pick = np.argmax(np.where(frm, rng.random(frm.shape, dtype=np.float32), -1), 1)
            ctx = np.where(frm.any(1)[:, None], self.pie[nn, pick], self.w[nn])
            ages = np.maximum(5, a + rng.normal(0, 5, len(nn)))
            F = self._gen(nn, t - (ages * 52).astype(np.int64), t, ctx=ctx, sel=0.4)
            self._add(F, t, R["acquaintance"], c0=0.08, trust0=0.5, ctx_read=ctx, quiet=True)
        nn = np.repeat(np.arange(N), _ix(k_ch))
        if len(nn):   # by chance: travel, online, a stranger who stays
            ages = np.maximum(5, a + rng.normal(0, 10, len(nn)))
            far = rng.random(len(nn)) < 0.4
            loc = np.where(far, rng.choice(self.n_loc, len(nn), p=self.loc_p), self.loc[nn])
            F = self._gen(nn, t - (ages * 52).astype(np.int64), t, loc=loc)
            self._add(F, t, R["acquaintance"], c0=0.06, trust0=0.45, quiet=True)

    def _roles(self, t):
        """Roles that emerge: friend (a close non-kin tie), mentor, rival, prospect, elder (quarterly)."""
        P = self.P; rng = self.rng; a = self._age(t); L1, L2, L3, L4 = P["layer_c"]
        rm = self.rmask
        age = self._qage if getattr(self, "_qage_t", None) == t else (t - self.born).astype(np.float32) / np.float32(52)
        un = self.used & self.lv & ((rm & (KINMASK | BIT["partner"] | BIT["ex"])) == 0)   # living non-kin
        newf = un & (self.c >= L2) & ((rm & BIT["friend"]) == 0) & (a >= 3)
        self.rmask[newf] |= BIT["friend"]
        for n_, k_ in zip(*_nz2(newf & self.watch[:, None] & (a >= 12))):
            self.events.append(dict(n=int(n_), t=int(t), kind="friend", cid=int(self.uid[n_, k_])))
        rm = self.rmask
        lk = self._lk if getattr(self, "_lk", None) is not None else likeness(self.pie, self.w[:, None, :])

        def nz(m_, p_):   # the candidates in m_, each taken with chance p_ this quarter
            nn_, kk_ = _nz2(m_)
            h_ = rng.random(len(nn_)) < p_
            return nn_[h_], kk_[h_]
        new = {}
        if a >= 14:
            new["mentor"] = nz(un & (self.stand >= 1) & (age >= a + 10) & (self.trust >= 0.6) & (self.c >= L3)
                               & ((rm & BIT["mentor"]) == 0), 0.15 * 0.25)
        if a >= 10:
            new["rival"] = nz(un & ((rm & (BIT["colleague"] | BIT["classmate"])) != 0) & (np.abs(age - a) <= 8) & (lk < 0.45)
                              & ((rm & BIT["rival"]) == 0), 0.04 * 0.25)
        if a >= 15:   # someone of the sex the character is drawn to, single, near in age, close enough and alike
            pn, pk = _nz2(un & (self.pslot < 0)[:, None] & (np.abs(age - a) <= 6) & ~self.mpart & (self.c >= L3)
                                & (lk >= 0.5) & ((rm & BIT["prospect"]) == 0))
            at = self.attr[pn]; r_ = rng.random((2, len(pn)))
            comp = np.where(self.fem[pn, pk] != self.female[pn], (at <= 2) | ((at == 3) & (r_[0] < 0.15)),
                            (at >= 2) | ((at == 1) & (r_[0] < 0.15)))
            h_ = comp & (r_[1] < 0.3 * 0.25)
            new["prospect"] = (pn[h_], pk[h_])
        new["elder"] = _nz2(un & (age >= 65) & (self.stand >= 1) & ((rm & BIT["elder"]) == 0))
        for r_, (nn_, kk_) in new.items():
            self.rmask[nn_, kk_] |= BIT[r_]
        # partnered: prospects fade back to friends or acquaintances
        hp = np.nonzero(self.pslot >= 0)[0]
        self.rmask[hp] &= ~BIT["prospect"]
        for kind_ in ("mentor", "rival", "prospect"):
            for n_, k_ in zip(*new.get(kind_, ((), ()))):
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="role", role=kind_, cid=int(self.uid[n_, k_])))

    def _cleanup(self, t):
        """Faces with no tie and the faded with no role or mark go back to the statistics; the long dead are let go."""
        P = self.P; L4 = P["layer_c"][3]
        u = self.used
        role_keep = (self.rmask & (KINMASK | BIT["partner"] | BIT["ex"] | BIT["rival"] | BIT["mentor"])) != 0
        marks = (self.mgood + self.mbad > 0) | (self.debt != 0) | self.secret
        faded = u & self.lv & (self.c < L4 * 0.67) & (self.mset == 0) & ~role_keep & ~marks & ((t - self.since) > 13)
        faded |= u & self.face & self.lv & (self.c < 0.1) & ((t - self.since) > 26)
        gone = u & ~self.lv & ((t - self.died_t) > 10 * 52) & ((self.rmask & CORE) == 0)
        nn, kk = _nz2(faded | gone)
        if len(nn):
            self._drop(nn, kk, t, quiet=True)

    # ------------------------------------------------------------------ wants (spec 2 §5)
    def _wants_arise(self, t):
        P = self.P; rng = self.rng; a = self._age(t); L1, L2, L3, L4 = P["layer_c"]
        if a < 14:
            return
        cand = self.used & self.lv & (self.want < 0) & ~self.dead[:, None] & ((self.c >= L3) | (self.brk > NEVER // 2))
        nn, kk = _nz2(cand)
        if not len(nn):
            return
        age = (t - self.born[nn, kk]) / 52.0; c = self.c[nn, kk]; rm = self.rmask[nn, kk]
        has = lambda r_: (rm & BIT[r_]) != 0
        par = has("parent"); gp = has("grandparent")
        H = np.zeros((len(nn), NW_ARISE))
        held = self.held
        hk = lambda i_: held[nn, i_] if held.shape[1] > i_ else np.zeros(len(nn), bool)
        H[:, WI["money"]] = 0.12 * c * (c >= L2) * (((~self.emp[nn, kk]) & (age >= 18) & (age < 65)) | (self.money[nn, kk] < 0.2))
        H[:, WI["care"]] = 0.6 * (par | gp | has("partner")) * ((self.health[nn, kk] < 0.35) | (age >= 82))
        H[:, WI["successor"]] = 0.15 * par * self.fbiz[nn, kk] * (18 <= a <= 40) * (age >= 50)
        H[:, WI["grandchild"]] = 0.25 * par * (age >= 58) * ~hk(KID) * (25 <= a <= 45)
        comp = np.where(self.fem[nn, kk] != self.female[nn], self.attr[nn] <= 2, self.attr[nn] >= 2)
        lk = self._lk[nn, kk] if getattr(self, "_lk", None) is not None else likeness(self.pie[nn, kk], self.w[nn])
        H[:, WI["love"]] = (0.08 * lk * comp * ~hk(PAR) * (a >= 16) * (np.abs(age - a) <= 8) * ~self.mpart[nn, kk]
                            * ((rm & (KINMASK | BIT["ex"])) == 0) * (c >= 0.3))
        H[:, WI["rival"]] = (0.4 * has("rival") + 0.06 * has("colleague") * (lk < 0.5)) * (a >= 16)
        fg0, fgw = P["forgive"]
        H[:, WI["forgiveness"]] = (fg0 * ((t - self.brk[nn, kk]) >= fgw) * (self.brk[nn, kk] > NEVER // 2)
                                   * (c < 0.6 * self.cmax[nn, kk]) * (self.cmax[nn, kk] >= L2) * ((rm & KINMASK) != 0))
        H[:, WI["home"]] = 0.15 * (par | gp) * ~self._here(nn, kk) * (a >= 18)
        H[:, WI["stop"]] = 0.25 * self.risky[nn] * (c >= L1)
        H[:, WI["secret"]] = 0.03 * (self.trust[nn, kk] >= 0.75) * (c >= L1) * ~has("partner")
        tot = H @ np.ones(NW_ARISE)
        occ = rng.random(len(nn)) < 1 - np.exp(-0.25 * tot)
        if not occ.any():
            return
        cum = np.cumsum(H[occ], 1) / tot[occ, None]
        key = (rng.random(occ.sum())[:, None] > cum).sum(1)
        n2, k2 = nn[occ], kk[occ]
        self.want[n2, k2] = key; self.wripe[n2, k2] = 0; self.wstate[n2, k2] = 1; self.wknown[n2, k2] = False
        fg = key == WI["forgiveness"]   # a break brings one wish to make peace at most (answered or not, it is spent)
        self.brk[n2[fg], k2[fg]] = NEVER
        for n_, k_, w_ in zip(n2, k2, key):
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="begins", key=CAST_WANTS[int(w_)],
                                        cid=int(self.uid[n_, k_]), known=False, **self._far_cause(n_, k_, t)))

    def _wants_week(self, t):
        """Wants ripen; ripe ones fall due; wants that no longer hold are met or lapse (unanswered: after two years)."""
        P = self.P; L2 = P["layer_c"][1]
        nn, kk = _nz2(self.wstate > 0)
        if not len(nn):
            return
        st = self.wstate[nn, kk]; wk = self.want[nn, kk].astype(np.int64); c = self.c[nn, kk]
        g = st == 1
        wr = self.wripe[nn, kk] + g * WANT_RATE[np.maximum(wk, 0)] * (0.5 + c) / 52.0
        self.wripe[nn, kk] = wr
        self.wknown[nn[g & (c >= L2) & (wr >= 0.5)], kk[g & (c >= L2) & (wr >= 0.5)]] = True
        due = g & (wr >= 1)
        for n_, k_ in zip(nn[due], kk[due]):
            self.wstate[n_, k_] = 2; self.wdue[n_, k_] = t; self.wknown[n_, k_] = True
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="due", key=CAST_WANTS[int(self.want[n_, k_])],
                                        cid=int(self.uid[n_, k_]), known=True, **self._far_cause(n_, k_, t)))
        d = st == 2
        hk = self.held[nn, KID] if self.held.shape[1] > KID else np.zeros(len(nn), bool)
        met = ((wk == WI["grandchild"]) & hk) | ((wk == WI["home"]) & self._here(nn, kk))
        lapse = ((wk == WI["love"]) & ((self.pslot[nn] >= 0) | self.mpart[nn, kk])) | (d & ((t - self.wdue[nn, kk]) > 104))
        lapse |= ~self.lv[nn, kk]
        if self.far_on:   # far_ties: an unanswered call lapses within weeks; work an event found meets a wish for money
            lapse |= FARW[np.maximum(wk, 0)] & d & ((t - self.wdue[nn, kk]) > self.far_par["lapse"])
            met |= ((wk == WI["money"]) & self.emp[nn, kk] & ((t - self.far_t[nn, kk]) <= 26)
                    & ((self.far_sg[nn, kk] & 1) > 0)) & ~lapse
        for n_, k_, m_, d_ in zip(nn[met | lapse], kk[met | lapse], met[met | lapse], d[met | lapse]):
            if not m_ and d_:
                self.trust[n_, k_] = max(0.0, float(self.trust[n_, k_]) - 0.05)
            if self.watch[n_] and self.lv[n_, k_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="met" if m_ else "lapsed",
                                        key=CAST_WANTS[int(self.want[n_, k_])], cid=int(self.uid[n_, k_])))
            self.want[n_, k_] = -1; self.wstate[n_, k_] = 0

    def want_due(self, t=None):
        """Wants ripe this week, and those still unanswered every half year after: [(n, cast id, want key)]. The
        engine offers the matching moment with that person in its first who: slot."""
        t = self.t if t is None else t
        nn, kk = _nz2(self.wstate == 2)
        if not len(nn):
            return []
        wd = self.wdue[nn, kk]
        d = ((wd == t) | (((t - wd) % 26 == 0) & (t > wd))) & ~self.dead[nn]
        return [(int(n_), int(self.uid[n_, k_]), CAST_WANTS[int(self.want[n_, k_])]) for n_, k_ in zip(nn[d], kk[d])]

    def resolve_want(self, n, cid, key, accepted, succ=True, t=None):
        """The moment that answered a want: trust and closeness move, a mark is left, a loan becomes a debt."""
        t = self.t if t is None else t
        k = self._slot(n, cid)
        if k < 0:
            return None
        (dc_a, dt_a), (dc_r, dt_r), mk_a, mk_r = WANT_FX[key]
        h = 1.0 if succ else 0.5
        dc, dtr, mk = (dc_a * h, dt_a * h, mk_a) if accepted else (dc_r, dt_r, mk_r)
        if key == "rival" and accepted:   # competing for the place: winning makes an enemy, losing costs trust
            dc, dtr, mk = ((-0.1, -0.1, "made an enemy") if succ else (-0.03, -0.05, None))
            self.rmask[n, k] |= BIT["rival"]
        self.c[n, k] = _uclip(self.c[n, k] + dc, 0, 1); self.trust[n, k] = _uclip(self.trust[n, k] + dtr, 0, 1)
        if mk:
            bad = mk in ("refused someone in need", "made an enemy", "broke your word")
            if bad:
                self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
            else:
                self.mgood[n, k] = min(255, int(self.mgood[n, k]) + 1)
        if accepted and key == "money":
            self.debt[n, k] = min(100, int(self.debt[n, k]) + 1)   # they owe the character
        if accepted and key == "secret":
            self.secret[n, k] = True
        if accepted and key == "forgiveness":
            self.brk[n, k] = NEVER; self.mbad[n, k] = max(0, int(self.mbad[n, k]) - 1)
        if accepted and key == "love":
            self.rmask[n, k] |= BIT["prospect"]
        if accepted and key == "successor":
            self.rmask[n, k] |= BIT["mentor"]
        self.want[n, k] = -1; self.wstate[n, k] = 0; self.wknown[n, k] = False
        ev = dict(n=int(n), t=int(t), kind="want", state="met" if accepted else "refused", key=key, cid=int(cid),
                  worked=bool(succ), mark=mk)
        if self.watch[n]:
            self.events.append(ev)
        return ev

    # ------------------------------------------------------------------ far_ties (item 18): the towns' events and the ties
    def _far_init(self, run_seed):
        """far_ties (chroma-ideas/far-off-events.md): the sides of each town event (sphere_data.FAR, Outer world's
        far_sides.json), the per-slot record of the last event that touched a cast member, and its own random stream."""
        import sphere_data as SD
        N, K = self.N, self.K
        self.far_par = {**FAR_DEFAULT, **dict((getattr(self.W, "p", None) or {}).get("far_par") or {})}
        self.far_ev = np.full((N, K), -1, np.int16)      # the last event that touched them (index into sphere_data.EV)
        self.far_t = np.full((N, K), NEVER, np.int64)    # its week
        self.far_sg = np.zeros((N, K), np.int8)          # its sides that touched them: 1 good, 2 hard, 3 both (mixed)
        self.far_sd = np.full((N, K, 2), -1, np.int16)   # the good and the hard side (index into _far_sides)
        self.far_in = np.full((N, K), FAR_OFF, np.int64)  # taken in (F4): the week their year in the household ends
        self.far_from = np.full((N, K), -1, np.int64)    # ... and the town they came from
        self._far_rng = np.random.default_rng([self.seed, 84, self.run_seed])
        self._far_i = len(getattr(self.W, "sph_ev_log", ()))   # the world's town events already read
        self.far_n = {}                                   # counts for the checks (not saved)
        ek = {f"{e['sphere']}.{e['key']}": i for i, e in enumerate(SD.EV)}
        self._far_sides = []; self._far_tab = {}; self._far_mix = set()   # events whose own tone is mixed
        for k, v in SD.FAR.items():
            if k not in ek:
                continue
            ids = []
            for x in v["sides"]:
                bad = [w_ for w_ in x["who"] if w_ not in FAR_WHO and not (w_.startswith("sector:") and w_[7:] in SECTORS)]
                if bad or x["touch"] not in TOUCHES:
                    raise ValueError(f"far side of {k}: unknown who {bad} or touch {x['touch']!r}")
                ids.append(len(self._far_sides))
                self._far_sides.append(dict(x, event=k, far_event=v["far_event"]))
            self._far_tab[ek[k]] = ids
            if v["sign"] == "mixed":
                self._far_mix.add(ek[k])

    def _far_count(self, key, m=1):
        self.far_n[key] = self.far_n.get(key, 0) + int(np.sum(m))

    def _far_fit(self, nn, kk, who, age):
        """The cast members (nn, kk) a side reaches: every word of its who list fits their own state (16 and over)."""
        m = age >= 16
        own = self.fbiz[nn, kk] | (self.mcls[nn, kk] >= 2)
        for w_ in who:
            if w_ == "in_work":
                m = m & self.emp[nn, kk]
            elif w_ == "out_of_work":
                m = m & ~self.emp[nn, kk] & (age >= 18) & (age < 65)
            elif w_.startswith("sector:"):
                m = m & self.emp[nn, kk] & (self.sector[nn, kk] == SECTORS.index(w_[7:]))
            elif w_ == "owner":
                m = m & own
            elif w_ == "renter":
                m = m & ~own
            elif w_ == "poor":
                m = m & (self.money[nn, kk] < 0.15)
            elif w_ == "comfortable":
                m = m & (self.money[nn, kk] >= 0.4)
            elif w_ == "young":
                m = m & (age < 30)
            elif w_ == "old":
                m = m & (age >= 65)
            elif w_ == "ill":
                m = m & (self.health[nn, kk] < 0.5)
            elif w_ == "parent":
                m = m & (self.nkids[nn, kk] >= 1)
        return m

    def _far_touch(self, nn, kk, x, good, age):
        """A side's touch on the cast members it reached (far_sides.json touch_effects): work found or lost, money,
        home, health, safety (mood) and standing, up or down."""
        tch = x["touch"]; sg = 1.0 if good else -1.0
        self._far_count(f"{tch} {'good' if good else 'hard'}", len(nn))
        if tch == "work":
            e_ = self.emp[nn, kk]
            if good:
                wa = ~e_ & (age >= 18) & (age < 65)
                a_, b_ = nn[wa], kk[wa]
                sec_ = [w_[7:] for w_ in x["who"] if w_.startswith("sector:")]
                s0_ = SECTORS.index(sec_[0]) if sec_ else SECTORS.index("services")
                self.sector[a_, b_] = np.where(self.sector[a_, b_] < 0, s0_, self.sector[a_, b_])
                self.emp[a_, b_] = True
                self._far_count("found work", wa)
                self.money[nn[e_], kk[e_]] = np.minimum(self.money[nn[e_], kk[e_]] + 0.05, 1)   # better work
            else:
                self.emp[nn[e_], kk[e_]] = False
                self._far_count("lost work", e_)
        elif tch == "money":
            self.money[nn, kk] = np.clip(self.money[nn, kk] + 0.15 * sg, 0.02, 1)
        elif tch == "home":
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.1 * sg, 0, 1)
            if not good:
                self.money[nn, kk] = np.clip(self.money[nn, kk] - 0.1, 0.02, 1)
        elif tch == "health":
            self.health[nn, kk] = np.clip(self.health[nn, kk] + 0.15 * sg, 0.02, 1)
        elif tch == "safety":
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.1 * sg, 0, 1)
        elif tch == "standing":
            self.stand[nn, kk] = np.clip(self.stand[nn, kk].astype(np.int64) + int(sg), 0, 3)
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.05 * sg, 0, 1)

    def _far_week(self, t):
        """F1 and F2: each town event fired since last week (local ones only; the whole society's reach everyone the
        same way) touches the cast members living in that town by its sides; a touched tie among the ~15 closest living
        in another town calls (a far want, due within weeks, in the want's first who: slot)."""
        log = getattr(self.W, "sph_ev_log", None)
        if log is None or len(log) <= self._far_i:
            return
        rows = np.asarray(log[self._far_i:]).tolist(); self._far_i = len(log)
        fp = self.far_par; L2, L3 = self.P["layer_c"][1], self.P["layer_c"][2]; rng = self._far_rng
        live = self.used & self.lv & ~self.dead[:, None]
        if self._xsoc:
            live &= self.msoc == self.soc.astype(self.msoc.dtype)[:, None]
        for _, i_, l_ in rows:
            ids = self._far_tab.get(int(i_))
            if l_ < 0 or not ids:
                continue
            nn, kk = np.nonzero(live & (self.mloc == l_))
            if not len(nn):
                continue
            age = (t - self.born[nn, kk]) / 52.0
            hit = np.zeros((len(nn), 2), bool); sd = np.full((len(nn), 2), -1)
            for j in ids:
                x = self._far_sides[j]; g = x["sign"] == "good"
                h = self._far_fit(nn, kk, x["who"], age) & (rng.random(len(nn)) < x["share"] * fp["good" if g else "hard"])
                if h.any():
                    self._far_touch(nn[h], kk[h], x, g, age[h])
                    hit[h, 1 - g] = True; sd[h, 1 - g] = j
            a_ = hit.any(1)
            if not a_.any():
                continue
            n2, k2, h2, s2, ag2 = nn[a_], kk[a_], hit[a_], sd[a_], age[a_]
            self.far_ev[n2, k2] = i_; self.far_t[n2, k2] = t
            self.far_sg[n2, k2] = h2[:, 0] + 2 * h2[:, 1]; self.far_sd[n2, k2] = s2
            away = self.mloc[n2, k2] != self.loc[n2]
            mixed = h2.all(1) | (int(i_) in self._far_mix)   # both sides, or one side of a mixed event (its tone)
            key = np.where(mixed, WI["far_mixed"], np.where(h2[:, 1], WI["far_hard"], WI["far_good"]))
            pc = np.where(mixed, fp["call_mixed"], np.where(h2[:, 1], fp["call_hard"], fp["call_good"]))
            call = (away & (self.c[n2, k2] >= L2) & (self.want[n2, k2] < 0) & (ag2 >= 16) & (rng.random(len(n2)) < pc)
                    & (self._age(t) >= 14))   # (as every want: from the character's 14th year)
            for n_, k_, w_ in zip(n2[call], k2[call], key[call]):
                self.want[n_, k_] = w_; self.wripe[n_, k_] = 0; self.wstate[n_, k_] = 1; self.wknown[n_, k_] = False
                self._far_count(f"call {CAST_WANTS[int(w_)]}")
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="want", state="begins", key=CAST_WANTS[int(w_)],
                                            cid=int(self.uid[n_, k_]), known=False, **self._far_cause(n_, k_, t)))
            for j_ in np.nonzero(self.watch[n2] & (self.c[n2, k2] >= L3))[0]:   # a close tie's news reaches the story
                n_, k_ = int(n2[j_]), int(k2[j_])
                self.events.append(dict(n=n_, t=int(t), kind="far", cid=int(self.uid[n_, k_]), here=not bool(away[j_]),
                                        **self._far_cause(n_, k_, t)))

    def _far_cause(self, n, k, t):
        """F5: the event that touched cast member (n, k) within far_par cause weeks, for a want or a story line: {} if
        none (and always with far_ties off)."""
        if not self.far_on or t - int(self.far_t[n, k]) > self.far_par["cause"]:
            return {}
        sg = int(self.far_sg[n, k]); sides = [self._far_sides[j] for j in self.far_sd[n, k] if j >= 0]
        return dict(cause=dict(event=sides[0]["event"], far_event=sides[0]["far_event"], town=int(self.mloc[n, k])
                               if self.far_in[n, k] == FAR_OFF else int(self.far_from[n, k]),
                               sign="mixed" if sg == 3 or int(self.far_ev[n, k]) in self._far_mix else "good" if sg == 1 else "hard", week=int(self.far_t[n, k]),
                               touch=[x["touch"] for x in sides], line=[x["line"] for x in sides]))

    def far_info(self, n, cid, t=None):
        """What the game names in a far moment: the tie's town (their_town), the event (far_event), what happened to
        them (line) and the touch; None if the cast member has no far event on record."""
        k = self._slot(n, cid)
        if k < 0 or not self.far_on:
            return None
        c_ = self._far_cause(n, k, self.t if t is None else t).get("cause")
        if c_ is None:
            return None
        return dict(c_, their_town=self._loc_info(c_["town"]))

    def far_rel(self, n, k):
        """The who: slots cast member k of life n fits by their relation (far_ties picks the moment by its first)."""
        rm = int(self.rmask[n, k])
        out = [s_ for s_ in WHO_SLOTS if s_ in BIT and s_ != "friend" and (rm & BIT[s_])]
        if (rm & BIT["friend"]) and not (rm & KINMASK):
            out.append("friend")
        if self.pslot[n] == k:
            out.append("partner")
        return out

    def take_in(self, n, cid, t=None):
        """F4, "took them in": the tie moves into the character's town and household for far_par stay weeks; then they
        stay in town or go back, even odds."""
        t = self.t if t is None else t
        k = self._slot(n, cid)
        if k < 0 or not self.far_on or self.far_in[n, k] != FAR_OFF:
            return None
        self.far_from[n, k] = self.mloc[n, k]; self.far_in[n, k] = t + int(self.far_par["stay"])
        self.mloc[n, k] = self.loc[n]; self.msoc[n, k] = self.soc[n]
        if self.hhj[n] >= 0:
            self.mset[n, k] |= self._bit(int(self.hhj[n]))
        self._far_count("taken in")
        ev = dict(n=int(n), t=int(t), kind="taken in", cid=int(cid), until=int(self.far_in[n, k]))
        if self.watch[n]:
            self.events.append(ev)
        return ev

    def _far_month(self, t):
        """F4: a year in the household over, a tie taken in finds a place in town or goes back home."""
        nn, kk = np.nonzero(self.far_in <= t)
        for n_, k_ in zip(nn, kk):
            if self.hhj[n_] >= 0:
                self.mset[n_, k_] &= ~self._bit(int(self.hhj[n_]))
            back = self._far_rng.random() < 0.5 and self.far_from[n_, k_] >= 0
            if back and self.used[n_, k_] and self.lv[n_, k_]:
                self.mloc[n_, k_] = self.far_from[n_, k_]
                for j_ in range(self.M):
                    if np.isin(self.skind[n_, j_], LOCAL_KINDS):
                        self.mset[n_, k_] &= ~self._bit(j_)
            self._far_count("went back" if back else "stayed in town")
            if self.watch[n_] and self.used[n_, k_] and self.lv[n_, k_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="taken in", state="went back" if back else "stayed",
                                        cid=int(self.uid[n_, k_])))
            self.far_in[n_, k_] = FAR_OFF
