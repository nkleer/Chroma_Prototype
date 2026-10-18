"""People's methods for the world read through world-build.md's names, adding and dropping people, and birth.

Part of class People (world_people.py), which inherits RosterMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import numpy as np
from world_keys import INST_KINDS, SECTORS
from world_people_base import (BIT, C, CORE, FAR_OFF, KINMASK, NEVER, R, ROLE, ROLE_ORDER, STATUS, _csum, _ix, _norm,
    _uclip, likeness, overlap)


class RosterMixin:
    # ------------------------------------------------------------------ the world, read through world-build.md's names
    def _world_static(self):
        W = self.W
        ps = np.asarray(W.loc_pop_share, float); self.n_loc = len(ps); self.loc_p = ps / ps.sum()
        self.n_nb = len(np.asarray(W.nb_loc))
        fs = np.asarray(getattr(W, "faith_share", np.zeros(0)), float); self.n_faith = len(fs)
        sec = getattr(W, "secular", None)
        p_none = float(sec) if sec is not None and np.ndim(sec) == 0 else max(0.0, 1.0 - fs.sum())
        pf = np.concatenate([[p_none], fs * (1 - p_none) / max(fs.sum(), 1e-9)]) if len(fs) else np.ones(1)
        self.faith_p = pf / pf.sum()
        self._inst_refresh()

    def _inst_refresh(self):
        W = self.W
        ik = np.asarray(getattr(W, "inst_kind", []))
        if ik.dtype.kind in "US" or ik.dtype == object:
            ik = np.array([INST_KINDS.index(k_) if k_ in INST_KINDS else -1 for k_ in ik], np.int64)
        self.inst_kind = ik.astype(np.int64); self.inst_loc = np.asarray(getattr(W, "inst_loc", np.zeros(len(ik))), np.int64)
        self.parties = np.nonzero(self.inst_kind == INST_KINDS.index("party"))[0]
        isec = getattr(W, "inst_sector", None)
        self.inst_sector = None if isec is None else np.asarray(isec)

    def _wf(self, name, default):
        v = getattr(self.W, name, default)
        return default if v is None else v

    @property
    def status(self):
        """Each life's status in the society it lives in: "citizen", "migrant" or "resident"."""
        return np.array(STATUS)[self.stat]

    def _here(self, n, k):
        """Cast members (n, k) living in the character's locality (and society)."""
        h = self.mloc[n, k] == self.loc[n]
        return h & (self.msoc[n, k] == self.soc[n]) if self._xsoc else h

    def _unemp(self, name, default=0.05):
        """Unemployment as a share (world.py keeps it in percent)."""
        v = np.asarray(self._wf(name, default), float)
        return v / 100.0 if v.size and np.nanmax(v) > 1.0 else v

    def _rate(self, kind, locs=None):
        try:
            v = self.W.rate_mult(kind)
        except Exception:
            return 1.0
        v = np.asarray(v, float)
        if v.ndim == 0 or locs is None:
            return float(v) if v.ndim == 0 else v
        return v[_uclip(locs, 0, len(v) - 1)]

    def _cohort(self, born):
        """The generation's mix for each birth week (a table by birth year; a generation still under 26 is read
        again each quarter, since the world can still change it)."""
        yr = np.floor_divide(np.asarray(born, np.int64), 52)
        if yr.size == 0:   # nobody to draw (an only child has no siblings): an empty table of mixes
            return np.zeros(yr.shape + (C,))
        lo, hi = int(yr.min()), int(yr.max())
        tb = self._coh_tab
        if tb is None or lo < self._coh_y0 or hi >= self._coh_y0 + len(tb[0]):   # (re)grow the table
            y0 = min(lo, self._coh_y0 if tb is not None else lo) - 10
            y1 = max(hi, self._coh_y0 + len(tb[0]) - 1 if tb is not None else hi) + 10
            nt = (np.zeros((y1 - y0 + 1, C)), np.full(y1 - y0 + 1, -1, np.int64))
            if tb is not None:
                nt[0][self._coh_y0 - y0:self._coh_y0 - y0 + len(tb[0])] = tb[0]
                nt[1][self._coh_y0 - y0:self._coh_y0 - y0 + len(tb[0])] = tb[1]
            self._coh_tab = tb = nt; self._coh_y0 = y0
        q = self.t // 13
        row = yr - self._coh_y0
        uq = np.unique(row)
        need = uq[(tb[1][uq] < 0) | ((tb[1][uq] != q) & ((self.t - (uq + self._coh_y0) * 52) <= 26 * 52))]
        for r_ in need.tolist():
            try:
                v_ = np.asarray(self.W.cohort_mix(int((r_ + self._coh_y0) * 52 + 26)), float)
            except Exception:
                v_ = np.asarray(self.W.V, float)
            tb[0][r_] = _norm(v_); tb[1][r_] = q
        return tb[0][row]

    def _popmean(self, loc, born):
        lm = np.asarray(self.W.loc_mix, float)[loc]
        return _norm(self.P["pw_loc"] * _norm(lm) + self.P["pw_coh"] * self._cohort(born))

    def _dirichlet(self, m, conc=None):
        a_ = np.maximum(m, 0.002) * (self.P["conc"] if conc is None else conc) * C
        g_ = self.rng.standard_gamma(a_[..., self.iperm])[..., self.perm]
        return _norm(g_ + 1e-12)

    def _party_of(self, pie):
        if not len(self.parties):
            return np.full(len(pie), -1, np.int64)
        prof = _norm(np.asarray(self.W.inst_profile, float)[self.parties])
        sc = pie @ prof.T + 0.05 * self.rng.gumbel(size=(len(pie), len(self.parties)))
        out = self.parties[np.argmax(sc, 1)]
        return np.where(self.rng.random(len(pie)) < 0.35, -1, out)   # about a third hold no party

    def _faith_draw(self, E):
        return self.rng.choice(len(self.faith_p), E, p=self.faith_p) - 1

    def _class_draw(self, loc):
        cm = np.asarray(self.W.loc_class_mix, float)[loc]
        cm = np.cumsum(cm / cm.sum(1, keepdims=True), 1)
        return np.minimum((self.rng.random(len(loc))[:, None] > cm).sum(1), 2)

    def _q(self, age, health=None, mcls=None):
        """Yearly death chance by age, health and class (life table); float32 for float32 ages."""
        c_, a_, b_ = self.P["mort"]
        age = np.asarray(age)
        q_ = c_ + a_ * np.exp(b_ * age)
        if mcls is not None:
            q_ = q_ * np.take(np.asarray(self.P["mort_cls"], q_.dtype), _ix(mcls), mode="clip")
        if health is not None:
            q_ = q_ * (0.6 + 0.8 * (1 - health))
        return np.minimum(q_, 0.9)

    def _rate_at(self, kind, locs):
        """W.rate_mult(kind) at each location in locs (float32; a scalar when the world gives one)."""
        v = self._rate(kind)
        if np.ndim(v) == 0:
            return np.float32(v)
        return np.take(np.asarray(v, np.float32), _ix(locs), mode="clip")

    def _surv(self, a1, a2):
        c_, a_, b_ = self.P["mort"]
        H_ = lambda x: c_ * x + a_ / b_ * (np.exp(b_ * x) - 1)
        return np.exp(-(H_(np.asarray(a2, float)) - H_(np.asarray(a1, float))))

    def _age(self, t=None):
        return ((self.t if t is None else t) - self.t0) / 52.0

    def _mage(self, t=None):
        return ((self.t if t is None else t) - self.born) / 52.0

    # ------------------------------------------------------------------ adding and dropping people
    def _gen(self, n, born, t, loc=None, ctx=None, sel=0.0, mcls=None, p_same_cls=0.0):
        """Fields for len(n) new people met by lives n, born in weeks born; ctx: a mix they share (a setting's norms,
        a family's ways) with weight sel."""
        rng = self.rng; E = len(n); P = self.P
        n = np.asarray(n, np.int64); born = np.asarray(born, np.int64)
        loc = self.loc[n] if loc is None else np.asarray(loc, np.int64)
        if ctx is not None and sel >= 1:
            m_ = _norm(np.asarray(ctx, float))
        else:
            m_ = self._popmean(loc, born)
            if ctx is not None:
                m_ = _norm((1 - sel) * m_ + sel * np.asarray(ctx, float))
        pie = self._dirichlet(m_)
        age = (t - born) / 52.0
        cl = self._class_draw(loc)
        if mcls is not None:
            cl = np.where(rng.random(E) < p_same_cls, mcls, cl)
        adult = age >= 18
        emp = adult & (age < 65) & (rng.random(E) < 0.78)
        ls = np.asarray(self._wf("loc_sectors", np.full((self.n_loc, len(SECTORS)), 0.2)), float)[loc]
        ls = np.cumsum(ls / np.maximum(ls.sum(1, keepdims=True), 1e-9), 1)
        sec = np.minimum((rng.random(E)[:, None] > ls).sum(1), len(SECTORS) - 1)
        sec = np.where(age >= 16, sec, -1)
        pp_ = np.interp(age, [18, 25, 32, 45, 65, 80], [0.05, 0.35, 0.6, 0.68, 0.65, 0.45])
        mpart = adult & (rng.random(E) < pp_)
        nk = np.where(age > 24, rng.poisson(_uclip((age - 24) / 10, 0, 1.8)), 0)
        hb = _uclip(1 - 0.012 * np.maximum(0, age - 35), 0.2, 1)
        health = _uclip(hb - 0.1 * rng.random(E), 0.05, 1)
        money = _uclip(np.array([0.3, 0.5, 0.75])[cl] + 0.1 * emp - 0.15 * (adult & (age < 65) & ~emp)
                        + 0.08 * rng.standard_normal(E), 0.02, 1)
        stand = np.where(adult, rng.choice(4, E, p=P["stand_p"]), 0)
        return dict(n=n, born=born, pie=pie, fem=rng.random(E) < 0.5, mloc=loc, mcls=cl, emp=emp, sector=sec,
                    mpart=mpart, nkids=np.minimum(nk, 6), health=health, money=money, stand=stand,
                    faith=self._faith_draw(E), party=self._party_of(pie),
                    strict=rng.standard_normal(E) + P["strict_age"] * (age - 40),
                    nm=rng.integers(0, 2 ** 31 - 1, E), line=rng.integers(0, 2 ** 31 - 1, E))

    def _add(self, F, t, role, c0=0.05, trust0=0.5, setbit=None, ctx_read=None, acc0=0.1, face=False,
             alive=True, kof=None, quiet=False, via=None):
        """Put the people in F (from _gen, optionally edited) into free slots of their lives; returns the slots."""
        n = np.asarray(F["n"], np.int64); E = len(n)
        if E == 0:
            return np.zeros(0, np.int64)
        P = self.P; rng = self.rng
        order = np.argsort(n, kind="stable"); n_s = n[order]
        first = np.searchsorted(n_s, n_s); rank_s = np.arange(E) - first
        rank = np.empty(E, np.int64); rank[order] = rank_s
        un, cnt = np.unique(n, return_counts=True)
        nfree = (~self.used[un]).sum(1)
        if (nfree < cnt).any():
            self._evict(un[nfree < cnt], (cnt - nfree)[nfree < cnt], t)
        free = ~self.used[un]                                 # the free slots of each life, in order
        nfree = free.sum(1); fl = np.flatnonzero(free)
        start = np.concatenate([[0], np.cumsum(nfree)[:-1]])
        inv = np.searchsorted(un, n)
        ok = rank < nfree[inv]
        slot = fl[start[inv[ok]] + rank[ok]] % self.K
        n = n[ok]
        sl = lambda a_: (np.asarray(a_)[ok] if np.ndim(a_) else np.full(len(n), a_))
        role = sl(role); rm = (1 << role.astype(np.int64)).astype(np.int32)
        self.used[n, slot] = True; self.lv[n, slot] = sl(alive)
        self.uid[n, slot] = self.unext[n] + rank[ok]
        np.add.at(self.unext, _ix(un), cnt)
        self.role[n, slot] = role; self.rmask[n, slot] = rm; self.face[n, slot] = face
        for k_ in ("born", "fem", "mloc", "mcls", "emp", "sector", "mpart", "nkids", "health", "money", "stand", "faith",
                   "party", "strict", "nm", "line"):
            getattr(self, k_)[n, slot] = sl(F[k_])
        self.pie[n, slot] = sl(F["pie"]) if np.ndim(F["pie"]) == 2 else F["pie"]
        self._psq[n, slot] = _csum(self.pie[n, slot] ** 2)
        self.fbiz[n, slot] = sl(F.get("fbiz", False))
        self.kof[n, slot] = -1 if kof is None else sl(kof)
        self.since[n, slot] = t; self.died_t[n, slot] = np.where(sl(alive), NEVER, t)
        c0 = _uclip(sl(c0), 0, 1); self.c[n, slot] = c0; self.cmax[n, slot] = c0
        self.trust[n, slot] = sl(trust0); self.last[n, slot] = t
        self.debt[n, slot] = 0; self.mgood[n, slot] = 0; self.mbad[n, slot] = 0; self.secret[n, slot] = False
        if getattr(self, "comrade", None) is not None:
            self.comrade[n, slot] = False
        if getattr(self, "inmate", None) is not None:
            self.inmate[n, slot] = False; self.inmate_t[n, slot] = NEVER
        if self.far_on:
            self.far_ev[n, slot] = -1; self.far_t[n, slot] = NEVER; self.far_sg[n, slot] = 0; self.far_sd[n, slot] = -1
            self.far_in[n, slot] = FAR_OFF; self.far_from[n, slot] = -1
        self.brk[n, slot] = NEVER; self.mood[n, slot] = 0.6; self.want[n, slot] = -1; self.wripe[n, slot] = 0
        self.wstate[n, slot] = 0; self.wknown[n, slot] = False; self.wdue[n, slot] = NEVER; self.inci[n, slot] = False
        self.inst[n, slot] = sl(F.get("inst", -1))
        self.msoc[n, slot] = sl(F["msoc"]) if "msoc" in F else self.soc[n]
        self.mset[n, slot] = 0
        if setbit is not None:
            sb = sl(setbit)
            self.mset[n, slot] = np.where(sb >= 0, 1 << np.maximum(sb, 0), 0).astype(self.mset.dtype)
        self.fkin[n, slot] = self._kf_near[role]; self.fkin_far[n, slot] = self._kf_far[role]
        # the character's first reading: the context they met in, the character's own lens, and noise; a little truth
        lmx = np.asarray(self.W.loc_mix, float)
        ctx = (lmx[np.minimum(self.mloc[n, slot], len(lmx) - 1)] if ctx_read is None
               else sl(ctx_read) if np.ndim(ctx_read) == 2 else np.tile(np.asarray(ctx_read, float), (len(n), 1)))
        prior = _norm(0.35 * _norm(ctx) + 0.35 * self.lens[n] + 0.3 * self._dirichlet(np.full((len(n), C), 1.0 / C), 1.0))
        a0 = sl(acc0)[:, None]
        self.read[n, slot] = (1 - a0) * prior + a0 * self.pie[n, slot]
        self._lkm[n, slot] = likeness(self.pie[n, slot], self.w32[n])
        if np.ndim(quiet):   # one flag per person: the events of those met openly
            q_ = sl(quiet)
            if not q_.all():
                self._ev_join(n[~q_], slot[~q_], t, via)
        elif not quiet:
            self._ev_join(n, slot, t, via)
        full = np.full(E, -1, np.int64); full[ok] = slot
        return full

    def _ev_join(self, n, slot, t, via):
        wn = self.watch[n]
        if not wn.any():
            return
        if via is not None:   # a group of people met at once: one event per life
            for n_ in np.unique(n[wn]):
                ss = slot[n == n_]
                self.events.append(dict(n=int(n_), t=int(t), kind="joined", via=via, cids=[int(x_) for x_ in self.uid[n_, ss]]))
            return
        for n_, s_ in zip(n[wn], slot[wn]):
            self.events.append(dict(n=int(n_), t=int(t), kind="joined", cid=int(self.uid[n_, s_]), role=self._rname(n_, s_)))

    def _evict(self, ns, need, t):
        """Make room in lives ns for need[i] people: the least tied go back to the statistics (faces, the long dead,
        faded acquaintances first; kin, the core and the partner last or never)."""
        ns = np.asarray(ns, np.int64); need = np.asarray(need, np.int64)
        rm = self.rmask[ns]
        sc = (self.c[ns] + 2.0 * ((rm & KINMASK) != 0) + 3.0 * ((rm & CORE) != 0)
              + 0.3 * ((self.mgood[ns] > 0) | (self.mbad[ns] > 0)) + 0.5 * (self.mset[ns] > 0) + 1.0 * self.inci[ns]
              - 1.0 * self.face[ns] - 1.5 * (~self.lv[ns] & ((t - self.died_t[ns]) > 5 * 52)))
        sc = np.where(self.used[ns], sc, np.inf)
        ps = self.pslot[ns]; hp = ps >= 0
        sc[np.nonzero(hp)[0], ps[hp]] = np.inf
        order = np.argsort(sc, 1, kind="stable")
        r_, p_ = np.nonzero(np.arange(self.K)[None, :] < need[:, None])
        k_ = order[r_, p_]
        ok = np.isfinite(sc[r_, k_])
        self._drop(ns[r_[ok]], k_[ok], t, quiet=True)

    def _drop(self, n, k, t, quiet=False):
        n = np.asarray(n, np.int64); k = np.asarray(k, np.int64)
        if not len(n):
            return
        if not quiet:
            sel = self.watch[n] & (self.cmax[n, k] >= self.P["layer_c"][2]) & self.lv[n, k]
            for n_, k_ in zip(n[sel], k[sel]):
                self.events.append(dict(n=int(n_), t=int(t), kind="left", cid=int(self.uid[n_, k_]), role=self._rname(n_, k_)))
        self.used[n, k] = False; self.lv[n, k] = False; self.mset[n, k] = 0; self.want[n, k] = -1; self.uid[n, k] = -1
        self.wstate[n, k] = 0; self.inci[n, k] = False; self.c[n, k] = 0; self.rmask[n, k] = 0; self.role[n, k] = -1
        for j_ in range(self.M):
            hit = self.slead[n, j_] == k
            self.slead[n[hit], j_] = -1
        hit = self.pslot[n] == k
        self.pslot[n[hit]] = -1

    def _rnames(self, n, k):
        """_rname for many (n, k) at once."""
        rm = self.rmask[n, k]; out = np.full(len(rm), -1)
        for i_ in range(len(ROLE_ORDER) - 1, -1, -1):
            out = np.where((rm & BIT[ROLE_ORDER[i_]]) != 0, i_, out)
        ro = self.role[n, k]
        return [ROLE_ORDER[i_] if i_ >= 0 else ROLE[r_] if r_ >= 0 else "acquaintance" for i_, r_ in zip(out.tolist(), ro.tolist())]

    def _evs(self, n, k, t, kind, **kw):
        """Events of one kind about cast members (n, k) of watched lives."""
        w_ = self.watch[n]; n, k = n[w_], k[w_]
        if len(n):
            self.events.extend(dict(n=n_, t=int(t), kind=kind, cid=u_, role=r_, **kw)
                               for n_, u_, r_ in zip(n.tolist(), self.uid[n, k].tolist(), self._rnames(n, k)))

    def _rname(self, n, k):
        m_ = int(self.rmask[n, k])
        for r_ in ROLE_ORDER:
            if m_ & BIT[r_]:
                return r_
        return ROLE[int(self.role[n, k])] if self.role[n, k] >= 0 else "acquaintance"

    def _slot(self, n, cid):
        hit = np.nonzero(self.used[n] & (self.uid[n] == cid))[0]
        return int(hit[0]) if len(hit) else -1

    # ------------------------------------------------------------------ birth (spec 3 §2.5b)
    def birth(self, t0, legacy=None):
        """Locality, neighbourhood, class, parents and the born-into cast, drawn from the society's population shares.
        legacy: a dict from save() (or one per life): the birth is placed in that family line."""
        self.t0 = t0 = int(t0); self.t = t0; self._last_lives = t0
        N = self.N; P = self.P; rng = self.rng; W = self.W
        self.loc = rng.choice(self.n_loc, N, p=self.loc_p)
        self.cls = self._class_draw(self.loc)
        self._pick_nb(np.arange(N))
        self.fr_bias = P["fr_bias"] * rng.standard_normal(N)
        lo_, hi_ = P["soc_spread"]
        self.sociab = np.exp(rng.uniform(np.log(lo_), np.log(hi_), N))
        self.vol_tgt = rng.choice(3, N, p=[0.25, 0.5, 0.25])
        allN = np.arange(N)
        # parents: the mother first, then a partner chosen alike (assortative: the best of five)
        am = _uclip(rng.normal(30.5, 5.2, N), 17, 46); af = _uclip(am + rng.normal(2.5, 4.0, N), 18, 62)
        Fm = self._gen(allN, t0 - (am * 52).astype(np.int64), t0); Fm["fem"][:] = True
        Ff = self._gen(allN, t0 - (af * 52).astype(np.int64), t0, mcls=self.cls, p_same_cls=0.8); Ff["fem"][:] = False
        cands = np.stack([self._dirichlet(self._popmean(self.loc, Ff["born"])) for _ in range(5)], 1)
        Ff["pie"] = cands[allN, np.argmax(overlap(cands, Fm["pie"][:, None, :]), 1)]
        for F_ in (Fm, Ff):
            F_["mcls"][:] = self.cls; F_["mpart"][:] = True; F_["mloc"][:] = self.loc
        fam_f = self._faith_draw(N)
        Fm["faith"] = fam_f; Ff["faith"] = np.where(rng.random(N) < 0.8, fam_f, self._faith_draw(N))
        Ff["party"] = np.where(rng.random(N) < 0.6, Fm["party"], Ff["party"])
        Fm["fbiz"] = rng.random(N) < P["p_biz"] / 2; Ff["fbiz"] = rng.random(N) < P["p_biz"] / 2
        sep = rng.random(N) < P["p_sep"]
        self.pfaith = fam_f.astype(np.int64); self.pparty = Fm["party"].astype(np.int64); self.pline = Ff["line"].copy()
        self.family_mix = _norm(0.5 * (Fm["pie"] + Ff["pie"]))
        Ff["line"] = self.pline
        sm = self._add(Fm, t0, R["parent"], c0=0.95, trust0=0.9, acc0=0.2, quiet=True)
        sf = self._add(Ff, t0, R["parent"], c0=np.where(sep, 0.45, 0.92), trust0=0.85, acc0=0.2, quiet=True)
        self.mloc[allN[sep], sf[sep]] = np.where(rng.random(sep.sum()) < 0.6, self.loc[sep],
                                                  rng.choice(self.n_loc, sep.sum(), p=self.loc_p))
        # siblings (the engine's distribution); older ones are here, younger ones are born later
        nsib = rng.choice(4, N, p=P["sib_p"])
        older = np.floor(rng.random(N) * (nsib + 1)).astype(np.int64)
        self.older_sib = older; self.younger_sib = nsib - older
        gaps = 1.5 + rng.gamma(2.0, 0.8, (N, 3))
        sib_n, sib_b = [], []
        for i_ in range(3):
            o_ = older > i_
            sib_n.append(allN[o_]); sib_b.append(t0 - (gaps[o_, :i_ + 1].sum(1) * 52).astype(np.int64))
        sib_n = np.concatenate(sib_n); sib_b = np.concatenate(sib_b)
        ok_ = (am[sib_n] - (t0 - sib_b) / 52) >= 16
        sib_n, sib_b = sib_n[ok_], sib_b[ok_]
        Fs = self._gen(sib_n, sib_b, t0, ctx=self.family_mix[sib_n], sel=P["pie_inherit"])
        Fs["mcls"][:] = self.cls[sib_n]; Fs["mloc"][:] = self.loc[sib_n]; Fs["line"][:] = self.pline[sib_n]
        self._inherit(Fs, self.pfaith[sib_n], self.pparty[sib_n])
        ss = self._add(Fs, t0, R["sibling"], c0=0.7, trust0=0.7, acc0=0.2, quiet=True)
        for i_ in range(3):
            y_ = self.younger_sib > i_
            for n_, b_ in zip(allN[y_], t0 + ((gaps[y_, :i_ + 1].sum(1)) * 52).astype(np.int64)):
                if am[n_] + (b_ - t0) / 52 <= 44:
                    self.pend.setdefault(int(b_), []).append((int(n_), "sibling"))
        # grandparents: alive now if they lived through the years since the parent was born
        gp_n, gp_b, gp_f, gp_s, gp_l, gp_fa, gp_pa = [], [], [], [], [], [], []
        for par_age, par_pie, par_line, F_ in ((am, Fm["pie"], Fm["line"], Fm), (af, Ff["pie"], self.pline, Ff)):
            ga = par_age + _uclip(rng.normal(28, 5, N), 17, 45)
            for fem_, gage in ((True, ga), (False, ga + rng.normal(2.5, 3.5, N))):
                live = rng.random(N) < self._surv(gage - par_age, gage)
                gp_n.append(allN[live]); gp_b.append(t0 - (gage[live] * 52).astype(np.int64)); gp_f.append(np.full(live.sum(), fem_))
                gp_s.append(par_pie[live]); gp_l.append(par_line[live]); gp_fa.append(F_["faith"][live]); gp_pa.append(F_["party"][live])
        gp_n = np.concatenate(gp_n)
        Fg = self._gen(gp_n, np.concatenate(gp_b), t0, ctx=np.concatenate(gp_s), sel=P["pie_inherit"])
        Fg["fem"] = np.concatenate(gp_f); Fg["line"] = np.concatenate(gp_l)
        self._inherit(Fg, np.concatenate(gp_fa), np.concatenate(gp_pa))
        far = rng.random(len(gp_n)) < 0.4
        Fg["mloc"] = np.where(far, rng.choice(self.n_loc, len(gp_n), p=self.loc_p), self.loc[gp_n])
        Fg["mpart"][:] = True
        self._add(Fg, t0, R["grandparent"], c0=np.where(far, 0.2, 0.35), trust0=0.7, acc0=0.15, quiet=True)
        # aunts and uncles (the parents' siblings, some with partners) and their children, the cousins
        au_n, au_b, au_s, au_l, au_k, au_f, au_p = [], [], [], [], [], [], []
        for par_age, F_, par_line, par_slot in ((am, Fm, Fm["line"], sm), (af, Ff, self.pline, sf)):
            k_ = rng.choice(4, N, p=P["sib_p"])
            for i_ in range(3):
                h_ = k_ > i_
                au_n.append(allN[h_]); au_b.append(t0 - ((par_age[h_] + rng.normal(0, 4, h_.sum())) * 52).astype(np.int64))
                au_s.append(F_["pie"][h_]); au_l.append(par_line[h_]); au_k.append(self.uid[allN[h_], par_slot[h_]])
                au_f.append(F_["faith"][h_]); au_p.append(F_["party"][h_])
        au_n = np.concatenate(au_n); au_b = np.concatenate(au_b)
        Fa = self._gen(au_n, au_b, t0, ctx=np.concatenate(au_s), sel=P["pie_inherit"])
        Fa["line"] = np.concatenate(au_l)
        self._inherit(Fa, np.concatenate(au_f), np.concatenate(au_p))
        livea = rng.random(len(au_n)) < self._surv(20, (t0 - au_b) / 52)
        far = rng.random(len(au_n)) < 0.4
        Fa["mloc"] = np.where(far, rng.choice(self.n_loc, len(au_n), p=self.loc_p), self.loc[au_n])
        Fa = {k2: (v2[livea] if np.ndim(v2) else v2) for k2, v2 in Fa.items()}
        sa = self._add(Fa, t0, R["kin"], c0=np.where(far[livea], 0.06, 0.12), trust0=0.6, kof=np.concatenate(au_k)[livea], quiet=True)
        an = Fa["n"]
        sp_ = rng.random(len(an)) < 0.6
        Fp = self._gen(an[sp_], Fa["born"][sp_] + (rng.normal(0, 3, sp_.sum()) * 52).astype(np.int64), t0)
        Fp["mloc"] = Fa["mloc"][sp_]; Fp["mpart"][:] = True; Fp["fem"] = ~Fa["fem"][sp_]
        self._add(Fp, t0, R["kin"], c0=0.05, trust0=0.5, kof=self.uid[an[sp_], sa[sp_]], quiet=True)
        nco = rng.choice(4, len(an), p=[0.25, 0.3, 0.3, 0.15])
        nco = _ix(nco); co_n = np.repeat(an, nco); co_src = np.repeat(np.arange(len(an)), nco)
        co_b = np.minimum(t0 + (rng.normal(-1, 5, len(co_n)) * 52).astype(np.int64), t0)
        Fc = self._gen(co_n, co_b, t0, ctx=Fa["pie"][co_src], sel=P["pie_inherit"])
        Fc["mloc"] = Fa["mloc"][co_src]; Fc["line"] = Fa["line"][co_src]
        self._inherit(Fc, Fa["faith"][co_src], Fa["party"][co_src])
        self._add(Fc, t0, R["kin"], c0=np.where(Fc["mloc"] == self.loc[co_n], 0.08, 0.04), trust0=0.55,
                  kof=self.uid[co_n, sa[co_src]], quiet=True)
        # the household: the parents (unless apart) and the older siblings
        for n_ in range(N):
            j_ = self._new_setting(n_, "household", t0)
            self.hhj[n_] = j_
        bit = np.uint8(1) if self.mset.dtype == np.uint8 else np.uint16(1)
        hj = self.hhj
        self.mset[allN, sm] |= (bit << hj).astype(self.mset.dtype)
        self.mset[allN[~sep], sf[~sep]] |= (bit << hj[~sep]).astype(self.mset.dtype)
        self.mset[sib_n, ss] |= (bit << hj[sib_n]).astype(self.mset.dtype)
        self.snorm[allN, hj] = self.family_mix; self.sanch[allN, hj] = self.family_mix
        if legacy is not None:
            for n_ in range(N):
                lg = legacy[n_] if isinstance(legacy, (list, tuple)) else legacy
                if lg:
                    self._legacy(n_, lg, t0)
        self._fsh(); self._close_index(); self._alive_counts(np.arange(N)); self._outputs_settings(); self._approval(t0)
        # the drawn birth is delivered with the first week's events (the engine takes events after a week; held back
        # here so that it arrives exactly once, whoever reads PP.events)
        self._carry = [dict(n=int(n_), t=t0, kind="born", loc=int(self.loc[n_]), nb=int(self.nb[n_]), cls=int(self.cls[n_]))
                       for n_ in range(N) if self.watch[n_]]
        self.events = []
        self.cls_home = np.asarray(self.cls, np.int64).copy(); self.loc_home = np.asarray(self.loc, np.int64).copy()
        self.par_apart = np.asarray(sep, bool).copy()

    def _pick_nb(self, ns):
        nbl = np.asarray(self.W.nb_loc, np.int64); nbc = np.asarray(self._wf("nb_class", np.ones(len(nbl))), np.int64)
        for n_ in ns:
            cand = np.nonzero(nbl == self.loc[n_])[0]
            if not len(cand):
                self.nb[n_] = -1; continue
            wt = np.where(nbc[cand] == self.cls[n_], 4.0, 1.0)
            self.nb[n_] = int(self.rng.choice(cand, p=wt / wt.sum()))

    def _legacy(self, n, lg, t):
        """A legacy line: one of the ancestor's grown children becomes a parent; the ancestor and their partner are
        grandparents; the ancestor's other children are aunts and uncles; their children are cousins."""
        cast = lg.get("cast", [])
        kids = [m_ for m_ in cast if "child" in m_.get("roles", []) and m_.get("alive") and 18 <= (t - m_["born"]) / 52 <= 46]
        if not kids:
            self.loc[n] = int(_uclip(lg.get("loc", self.loc[n]), 0, self.n_loc - 1)); return
        par = kids[int(self.rng.integers(len(kids)))]
        self.loc[n] = int(_uclip(par.get("mloc", lg.get("loc", self.loc[n])), 0, self.n_loc - 1))
        self.cls[n] = int(lg.get("cls", self.cls[n]))
        self._pick_nb([n])
        keep = self.used[n] & ((self.rmask[n] & (BIT["parent"] | BIT["sibling"])) != 0)
        drop = np.nonzero(self.used[n] & ~keep)[0]
        self._drop(np.full(len(drop), n), drop, t, quiet=True)
        ps = np.nonzero(self.used[n] & ((self.rmask[n] & BIT["parent"]) != 0))[0]
        same = [p_ for p_ in ps if bool(self.fem[n, p_]) == bool(par.get("fem"))]
        if same:   # the inherited child takes the place of the drawn parent of the same sex
            p_ = same[0]
            for k_ in ("born", "fem", "nm", "line", "mcls", "faith", "party"):
                if k_ in par:
                    getattr(self, k_)[n, p_] = par[k_]
            self.pie[n, p_] = par["pie"]; self.mloc[n, p_] = self.loc[n]; self._psq[n, p_] = _csum(self.pie[n, p_] ** 2)
            self.family_mix[n] = _norm(self.pie[n, ps].mean(0)); self.pline[n] = int(par.get("line", 0))
        if getattr(self, "bt_on", False) and (lg.get("btrust") or {}).get("v") is not None:
            # body_trust: the inheriting parent grew up in the ancestor's home and took the ancestor's trust at 15, so the
            # ancestor's trust (as saved) is the known parents' mean this child starts from at 15
            v_ = np.array([np.nan if x_ is None else x_ for x_ in lg["btrust"]["v"]], float)
            if not np.isnan(v_).any():
                self.bt_par[n] = v_
        anc = lg.get("self", {})
        add = []
        if anc.get("alive", False) and anc.get("pie") is not None:
            add.append((dict(anc, roles=["grandparent"]), R["grandparent"], 0.35))
        for m_ in cast:
            if not m_.get("alive"):
                continue
            rl = m_.get("roles", [])
            if "partner" in rl:
                add.append((m_, R["grandparent"], 0.35))
            elif "child" in rl and m_ is not par:
                add.append((m_, R["kin"], 0.12))
            elif "grandchild" in rl:
                add.append((m_, R["kin"], 0.08))
        for m_, r_, c_ in add:
            F = self._gen(np.array([n]), np.array([int(m_["born"])]), t)
            F["pie"] = np.asarray(m_["pie"], float)[None]
            for k_ in ("fem", "nm", "line", "mcls", "faith", "party", "mloc"):
                if k_ in m_:
                    F[k_] = np.array([m_[k_]])
            self._add(F, t, r_, c0=c_, trust0=0.6, acc0=0.15, quiet=True)
