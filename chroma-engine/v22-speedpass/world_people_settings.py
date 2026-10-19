"""People's methods for settings (spec 3 §1) and the spheres of society, phase 2.

Part of class People (world_people.py), which inherits SettingsMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import numpy as np
from library import COLORS
from world_keys import GROUP_KINDS, HAUNT_KINDS, INST_KINDS, LADDER, SECTORS, SPHERES, TIME_ROWS
from world_people_base import (BIT, C, COMM_W, G, GROUP_SPH, HAUNT_AGE, HAUNT_COST, HAUNT_SPH, INST_OF, KINMASK, KTA,
    K_COH, K_DEPTH, K_DRIFT, K_F, K_GATE, K_LEAD, K_NCAST, K_SIZE, K_TS, K_TSY, K_WA, K_WM, K_WV, K_XC, LEAD_BIT,
    LEAD_ROLE, MEMBER_ROLE_OF, MON, SCENE_HAUNTS, SECTOR_SPH, SET_HAUNTS, SET_SUB, STATUS, VOLUNTARY, WORK_SUB, _LUT,
    _csum, _ix, _norm, _uclip, likeness, overlap)


class SettingsMixin:
    # ------------------------------------------------------------------ settings (spec 3 §1)
    def _new_setting(self, n, kind, t, ref=-1):
        """A free setting slot for life n, filled with a setting of this kind (no members yet); returns its index."""
        g = G[kind]; P = self.P; rng = self.rng
        free = np.nonzero(self.skind[n] < 0)[0]
        if not len(free):
            vol = [j_ for j_ in range(self.M) if self.skind[n, j_] in VOLUNTARY or self.skind[n, j_] == G["online"]]
            if not vol:
                return -1
            self._leave(n, min(vol, key=lambda j_: self.sts[n, j_]), t, "full")
            free = np.nonzero(self.skind[n] < 0)[0]
        j = int(free[0]); a = self._age(t)
        self.skind[n, j] = g; self.scoh[n, j] = _uclip(KTA[g, K_COH] + 0.08 * rng.standard_normal(), 0.05, 0.95)
        self.srank[n, j] = 0.5 if kind in ("household", "class") else 0.25
        self.sts[n, j] = KTA[g, K_TSY] if a < 18 else KTA[g, K_TS]
        self.ssize[n, j] = max(1, int(KTA[g, K_SIZE] * rng.lognormal(0, 0.4)))
        self.sgate[n, j] = K_GATE[g]; self.sxcost[n, j] = K_XC[g]
        self.sform[n, j] = t if kind in ("household", "class") else t - int(52 * rng.exponential(12))
        self.sjoin[n, j] = t; self.sref[n, j] = ref; self.slead[n, j] = -1; self.sncast[n, j] = 0
        self.mset[n] &= ~self._bit(j)
        if self.sph_h:
            self.shnt[n, j] = -1
        return j

    def _inst_pick(self, n, ikind, sector=-1):
        cand = np.nonzero(self.inst_kind == INST_KINDS.index(ikind))[0]
        if not len(cand):
            return -1
        here = cand[self.inst_loc[cand] == self.loc[n]]
        pool = here if len(here) else cand
        if sector >= 0 and self.inst_sector is not None:
            s_ = pool[np.asarray(self.inst_sector)[pool] == sector]
            pool = s_ if len(s_) else pool
        return int(self.rng.choice(pool))

    def join(self, n, kind, t=None, ref=-1, cause=None, quiet=False):
        """The character joins a group of this kind (life course, a moment, or a lever): members are drawn from the
        place's population (most cast members are met this way). cause: a movement's mix. Returns the setting index."""
        js = self._join_many(np.array([n]), kind, t, refs=None if ref < 0 else np.array([ref]), cause=cause, quiet=quiet)
        return int(js[0]) if len(js) else -1

    def _join_many(self, ns, kind, t=None, refs=None, cause=None, quiet=False, gate=True):
        """join() for many lives at once (vectorised members); returns their setting indices (-1: no room)."""
        t = self.t if t is None else t; rng = self.rng; W = self.W
        ns = np.asarray(ns, np.int64)
        if not len(ns):
            return np.zeros(0, np.int64)
        g = G[kind]; a = self._age(t)
        refs = np.full(len(ns), -1, np.int64) if refs is None else np.asarray(refs, np.int64).copy()
        for i_, n_ in enumerate(ns):
            if refs[i_] >= 0:
                continue
            if kind in INST_OF:
                refs[i_] = self._inst_pick(n_, "university" if (kind == "class" and a >= 17.5) else INST_OF[kind],
                                           self.psector[n_] if kind == "work" else -1)
            elif kind == "congregation":
                refs[i_] = int(self.pfaith[n_]) if self.pfaith[n_] >= 0 else self._faith_for(n_)
        gk = self._mig_gate(ns, kind, refs, t, a) if self._xsoc and gate else None
        if gk is not None and not gk.all():   # turned away this time (a migrant, at first): no setting
            out = np.full(len(ns), -1, np.int64)
            if gk.any():
                out[gk] = self._join_many(ns[gk], kind, t, refs[gk], cause, quiet, gate=False)
            return out
        js = np.array([self._new_setting(int(n_), kind, t, int(r_)) for n_, r_ in zip(ns, refs)], np.int64)
        ok = js >= 0
        ns, js, refs = ns[ok], js[ok], refs[ok]
        E = len(ns)
        if not E:
            return js
        lm = _norm(np.asarray(W.loc_mix, float)[self.loc[ns]])
        if kind in INST_OF:
            prof = _norm(np.asarray(W.inst_profile, float))
            anch = np.where((refs >= 0)[:, None], prof[np.maximum(refs, 0)], lm)
        elif kind == "congregation" and self.n_faith:
            fp = _norm(np.asarray(W.faith_profile, float))
            anch = np.where((refs >= 0)[:, None], fp[_uclip(refs, 0, len(fp) - 1)], lm)
            fp_ = getattr(self, "_force_place", None) if self.sph_h else None
            if fp_ is not None and fp_[0] in ns:   # the player's pick of a faith's place: the congregation meets there
                self.shnt[ns[ns == fp_[0]], js[ns == fp_[0]]] = fp_[1]
        elif kind == "movement" and cause is not None:
            anch = np.tile(_norm(np.asarray(cause, float)), (E, 1))
        elif self.sph_h and kind in ("club", "scene"):
            # spheres phase 2 (N1): the setting meets at a named place, one of their haunts (or the town's best fitting
            # place of such a kind, which becomes one), in place of the best of three random ways; the player's pick first
            fp_ = getattr(self, "_force_place", None)
            pl_ = np.array([fp_[1] if fp_ is not None and fp_[0] == n_ else self._haunt_for(int(n_), kind) for n_ in ns], np.int64)
            self.shnt[ns, js] = pl_
            anch = np.where((pl_ >= 0)[:, None], W.hp_s.reshape(-1, C)[np.maximum(pl_, 0)], lm)
        elif kind in ("club", "scene", "online", "gang", "movement"):
            # people choose the group that fits them (children: the parents choose): the best of three nearby ways
            base = lm if kind in ("club", "gang") else np.full((E, C), 1.0 / C)
            cands = self._dirichlet(np.repeat(base, 3, 0), 1.2).reshape(E, 3, C)
            who = self.w[ns] if a >= 10 else self.family_mix[ns]
            anch = cands[np.arange(E), np.argmax(overlap(cands, who[:, None, :]), 1)]
        elif kind == "household":
            anch = self.w[ns]
        else:
            anch = lm
        self.sanch[ns, js] = anch
        self.snorm[ns, js] = anch if kind == "household" else _norm(0.6 * anch + 0.4 * lm)
        if kind == "neighbours":
            eff = np.asarray(self._wf("nb_efficacy", np.full(max(self.n_nb, 1), 0.5)), float)[np.maximum(self.nb[ns], 0)]
            self.scoh[ns, js] = _uclip(0.2 + 0.5 * eff, 0.05, 0.95)
        cnt = np.round(KTA[g, K_NCAST] * rng.lognormal(0, 0.25, E)).astype(np.int64)
        self.sncast[ns, js] = cnt + (K_LEAD[g] is not None)
        if self._defer is not None:   # the month's joins get their members in one batch (_fill_members)
            self._defer.append((ns, js, cnt, g, quiet))
        else:
            self._fill_members([(ns, js, cnt, g, quiet)], t)
        if not quiet:
            for n_, j_, r_ in zip(ns, js, refs):
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="group_joined", group=kind, j=int(j_), ref=int(r_)))
        out = np.full(len(ok), -1, np.int64); out[ok] = js
        return out

    def _mig_gate(self, ns, kind, refs, t, a):
        """Who of lives ns gets in (spec 5 §5: gates are harder at first for a migrant): a citizen always; a migrant
        or resident with chance openness to migrants (the institution's, else the society's mean) x (g0 + (1 - g0) x
        language), easing toward 1 over the years since arrival (a resident halfway there). The home, the
        neighbours, online groups, care and a child's school are not gated. Draws only when a non-citizen asks."""
        ok = np.ones(len(ns), bool)
        if kind in ("household", "online", "neighbours", "ward") or (kind == "class" and a < 18):
            return ok
        st = self.stat[ns]; nc = st != 0
        if not nc.any():
            return ok
        om = np.atleast_1d(np.asarray(self._wf("inst_open_mig", 0.7), float))
        op = np.full(len(ns), float(om.mean()))
        if kind in INST_OF:
            hr = refs >= 0
            op[hr] = om[_uclip(refs[hr], 0, len(om) - 1)]
        g0, tau = self.P["mig_gate"]
        base = _uclip(op, 0, 1) * (g0 + (1 - g0) * self.lang[ns])
        yrs = np.maximum(t - self.arr_t[ns], 0) / 52.0
        p_ = base + (1 - base) * (1 - np.exp(-yrs / tau))
        p_ = np.where(st == STATUS.index("resident"), 0.5 + 0.5 * p_, p_)
        return ~nc | (self.rng.random(len(ns)) < p_)

    def _fill_members(self, batch, t):
        """Members and leaders for new settings [(lives, setting indices, member counts, kind, quiet)], in one go."""
        batch = [(ns[ok], js[ok], cnt[ok], g, q) for ns, js, cnt, g, q in batch
                 for ok in [(self.skind[ns, js] == g) & (self.sjoin[ns, js] == t)] if ok.any()]
        if not batch:
            return
        parts = []   # (lives, settings, leader?, quiet?): the members, then a leader where the kind has one
        for ns, js, cnt, g, q in batch:
            parts.append((np.repeat(ns, _ix(cnt)), np.repeat(js, _ix(cnt)), False, bool(q)))
            if K_LEAD[g] is not None:
                parts.append((ns, js, True, True))
        nn = np.concatenate([x_[0] for x_ in parts]); jj = np.concatenate([x_[1] for x_ in parts])
        ld = np.concatenate([np.full(len(x_[0]), x_[2]) for x_ in parts])
        qu = np.concatenate([np.full(len(x_[0]), x_[3]) for x_ in parts])
        sl_ = self._members(nn, jj, t, leader=ld, quiet=qu)
        ok = ld & (sl_ >= 0)
        if ok.any():
            ln, lj, sl_ = nn[ok], jj[ok], sl_[ok]
            gk = self.skind[ln, lj].astype(np.int64)
            self.slead[ln, lj] = sl_
            nc = gk != G["club"]
            self.stand[ln[nc], sl_[nc]] = np.maximum(1, self.stand[ln[nc], sl_[nc]])
            self.rmask[ln, sl_] |= LEAD_BIT[gk]; self.role[ln, sl_] = LEAD_ROLE[gk]

    def _faith_for(self, n):
        if not self.n_faith:
            return -1
        fp = _norm(np.asarray(self.W.faith_profile, float))
        sc = fp @ self.w[n]
        if len(sc) > 3 and hasattr(self.W, "faith_open"):   # C5: a movement slot only while it lives and holds join_share
            sc = np.where(self.W.faith_open(), sc, -np.inf)
        return int(np.argmax(sc))

    def _members(self, n, j, t, leader=False, quiet=False):
        """New cast members for settings (n, j), vectorised: ages, pies near the setting's norms, roles by kind.
        leader, quiet: one flag for all, or one per row (a leader is drawn older and takes the kind's leader role)."""
        n = np.asarray(n, np.int64); j = np.asarray(j, np.int64); E = len(n)
        if not E:
            return np.zeros(0, np.int64)
        rng = self.rng; a = self._age(t); g = self.skind[n, j].astype(np.int64)
        ld = np.broadcast_to(np.asarray(leader, bool), (E,))
        kinds = np.array(GROUP_KINDS)[g]
        ages = np.empty(E)
        for kd in np.unique(kinds):
            h = kinds == kd; m_ = h.sum(); lh = ld[h]
            if kd == "class":
                ag = (a + rng.normal(0, 0.35, m_)) if a < 17.5 else a + np.abs(rng.normal(0, 2.0, m_))
                ag = np.where(lh, rng.uniform(26, 62, m_), ag) if lh.any() else ag
            elif kd in ("work", "unit"):
                ag = np.where(lh, rng.uniform(35, 62, m_), rng.uniform(19, 64, m_)) if lh.any() else rng.uniform(19, 64, m_)
            elif kd == "congregation":
                ag = np.where(lh, rng.uniform(45, 75, m_), rng.uniform(5, 88, m_)) if lh.any() else rng.uniform(5, 88, m_)
            elif kd in ("scene", "gang"):
                ag = np.maximum(12, a + rng.normal(0, 4, m_))
            elif kd == "ward":
                ag = np.maximum(a, 60) + rng.normal(0, 8, m_)
            elif kd == "neighbours":
                ag = rng.uniform(1, 88, m_)
            else:
                ag = np.maximum(5, a + rng.normal(0, 10 if a >= 18 else 3, m_))
            ages[h] = _uclip(ag, 0, 99)
        born = t - (ages * 52).astype(np.int64)
        sel = np.where(np.isin(g, VOLUNTARY) | np.isin(g, [G["online"], G["gang"]]), 0.5, 0.25)[:, None]
        F = self._gen(n, born, t, ctx=self.snorm[n, j], sel=1.0, mcls=self.cls[n], p_same_cls=0.4)
        F["pie"] = _norm((1 - sel) * self._dirichlet(self._popmean(self.loc[n], born)) + sel * F["pie"])
        cong = g == G["congregation"]
        F["faith"] = np.where(cong, self.sref[n, j], F["faith"])
        wk = g == G["work"]
        F["emp"] = np.where(wk, True, F["emp"]); F["sector"] = np.where(wk & (self.psector[n] >= 0), self.psector[n], F["sector"])
        F["inst"] = np.where(wk | (g == G["class"]) | (g == G["unit"]), self.sref[n, j], -1)
        rn = np.where(ld, LEAD_ROLE[g], MEMBER_ROLE_OF[g]).astype(np.int64)
        c0 = _uclip(0.04 + 0.08 * rng.random(E), 0.03, 0.2)
        sl = self._add(F, t, rn, c0=c0, trust0=0.5, setbit=j, ctx_read=self.snorm[n, j], acc0=0.05,
                       quiet=np.broadcast_to(np.asarray(quiet, bool), (E,)) | ld, via="group")
        return sl

    def _leave(self, n, j, t, why="left"):
        if j < 0 or self.skind[n, j] < 0:
            return
        kind = GROUP_KINDS[int(self.skind[n, j])]
        bit = self._bit(j)
        self.mset[n] &= ~bit
        self.skind[n, j] = -1; self.sts[n, j] = 0; self.slead[n, j] = -1; self.sncast[n, j] = 0
        if self.sph_h:
            self.shnt[n, j] = -1
        if self.hhj[n] == j:
            self.hhj[n] = -1
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="group_left", group=kind, j=int(j), why=why))

    def leave(self, n, kind, t=None, why="left"):
        """The character leaves their group of this kind (the newest one), paying its exit cost in belonging."""
        js = np.nonzero(self.skind[n] == G[kind])[0]
        if len(js):
            self._leave(n, int(js[np.argmax(self.sjoin[n, js])]), self.t if t is None else t, why)

    def _bit(self, j):
        return (np.ones(1, self.mset.dtype) << np.asarray(j, self.mset.dtype))[0] if np.ndim(j) == 0 else \
            (np.ones(1, self.mset.dtype) << np.asarray(j).astype(self.mset.dtype))

    def _bits(self):
        """(N, K, M) membership of the living in each setting (float32)."""
        return np.take(_LUT[:, :self.M], np.where(self.lv, self.mset, 0).astype(np.uint8), axis=0)

    def _count(self, B):
        """(N, M) living members of each setting."""
        return np.matmul(np.ones((self.N, 1, self.K), np.float32), B)[:, 0, :]

    def _fsh(self, B=None):
        """Contact a year with each cast member through shared settings: the setting's contact x depth, shared out by
        attention (the alike and the already close get more; the members' mean keeps the setting's contact)."""
        B = self._bits() if B is None else B; P = self.P; f32 = np.float32
        g = np.maximum(self.skind, 0)
        fd = np.where(self.skind >= 0, KTA[g, K_F] * KTA[g, K_DEPTH], 0).astype(f32)
        if self._xsoc and (self.lang < 1).any():   # a language still being learned thins contact outside the home
            fd = np.where(g == G["household"], fd, fd * (0.4 + 0.6 * self.lang).astype(f32)[:, None])
        lk = self._lkm = likeness(self.pie, self.w32[:, None, :]).astype(f32)
        att = (f32(P["mingle"][0]) + f32(P["mingle"][1]) * lk * lk) * (self.c + f32(P["att_c0"])) ** f32(P["att_pow"])
        ma_ = P["mingle_age"]
        if ma_ is not None and ma_[0] > 0:   # near in age (every character of the run has the same age)
            f0 = ma_[2] if len(ma_) > 2 else 0.0
            dg = (self.born - self.t0).astype(f32); dg *= f32(1 / (52.0 * (ma_[0] + ma_[1] * self._age())))
            dg *= dg; dg += f32(1); np.reciprocal(dg, out=dg); dg *= f32(1 - f0); dg += f32(f0)
            dg[(self.rmask & KINMASK) != 0] = 1
            att *= dg
        A2 = np.empty((self.N, 2, self.K), f32); A2[:, 0] = att; A2[:, 1] = 1.0
        dc = np.matmul(A2, B)                                    # (N, 2, M): attention summed, members counted
        den = dc[:, 0] / np.maximum(dc[:, 1], 1.0)
        sw = ((self.sociab / np.sqrt(np.prod(P["soc_spread"]))) ** P["soc_set"]).astype(f32)[:, None]
        self.fsh = np.matmul(B, (fd / np.maximum(den, 1e-6))[..., None])[..., 0] * att * sw

    def _settings_month(self, t, S, B, dm=1.0):
        """Norms drift toward members (by standing), the character (by rank), the leader, the anchor (institution,
        faith, founding ways) and the culture (faster for the young); cohesion follows the members' spread; splits.
        dm: months since the last step (the monthly rates are scaled to it)."""
        N, M = self.N, self.M; P = self.P; W = self.W; a = self._age(t); f32 = np.float32
        act = self.skind >= 0
        if not act.any():
            return
        g = np.maximum(self.skind, 0)
        # sums over members, weighted by standing: their pies; their spread (sum of squares), strictness and weight
        wt = (1.0 + self.stand).astype(f32)
        msum = np.matmul(B.transpose(0, 2, 1), self.pie * wt[..., None])   # (N, M, C)
        Xs = np.empty((N, 4, self.K), f32)
        np.multiply(self._psq, wt, out=Xs[:, 0]); np.multiply(self.strict, wt, out=Xs[:, 1]); Xs[:, 2] = wt; Xs[:, 3] = 1.0
        Rw = np.matmul(Xs, B)                                    # (N, 4, M)
        mw = Rw[:, 2]; cnt = Rw[:, 3]
        memmix = np.where(mw[..., None] > 0, msum / np.maximum(mw[..., None], 1e-9), self.snorm)
        self._fitm = (C * _csum(memmix * self.snorm) - 1).astype(f32)   # how well members fit the ways
        self.srank += (act * (1 - (1 - P["rank_rev"]) ** dm) * (P["rank_base"] - self.srank)).astype(f32)
        ls = np.clip(self.slead, 0, None)
        lp = self.pie[np.arange(N)[:, None], ls]
        haslead = (self.slead >= 0) & self.lv[np.arange(N)[:, None], ls]
        lp = np.where((self.slead == -2)[..., None], self.w[:, None, :], lp)
        haslead = haslead | (self.slead == -2)
        inst_k = act & np.isin(g, [G["class"], G["work"], G["unit"], G["ward"]]) & (self.sref >= 0)
        if inst_k.any():
            prof = _norm(np.asarray(W.inst_profile, float))
            self.sanch[inst_k] = prof[_uclip(self.sref[inst_k], 0, len(prof) - 1)]
        V = _norm(np.asarray(W.V, float))
        young = 1.5 if a < 25 else 1.0
        tgt = (KTA[g, K_WM][..., None] * memmix + 0.15 * self.srank[..., None] * self.w[:, None, :]
               + 0.2 * haslead[..., None] * lp + KTA[g, K_WA][..., None] * self.sanch
               + young * KTA[g, K_WV][..., None] * V)
        hh = (g == G["household"]) & act
        if hh.any():   # a household's ways are its adults' ways
            hn, hj = np.nonzero(hh)
            al = (self.born <= t - 18 * 52) & self.lv          # the adults living in it (one household per life at most)
            if len(hn) == N:
                ba = (((self.mset >> hj[:, None].astype(self.mset.dtype)) & 1) * al).astype(f32); hp_ = self.pie
            else:
                ba = (((self.mset[hn] >> hj[:, None].astype(self.mset.dtype)) & 1) * al[hn]).astype(f32); hp_ = self.pie[hn]
            hsum = np.matmul(ba[:, None, :], hp_)[:, 0] + (a >= 18) * self.w[hn]
            hcnt = ba.sum(1) + (a >= 18)
            hmix = np.where(hcnt[:, None] > 0, hsum / np.maximum(hcnt[:, None], 1e-9), self.snorm[hn, hj])
            tgt[hn, hj] = hmix + 0.02 * V
        tgt = _norm(tgt)
        age_y = (t - self.sform) / 52.0
        rate = np.minimum(dm * KTA[g, K_DRIFT] * (1 - 0.5 * self.scoh) / (1 + np.maximum(age_y, 0) / 20), 1) * act
        self.snorm += (rate[..., None] * (tgt - self.snorm)).astype(f32)
        # cohesion: members pulling apart lower it; old ritual groups and outside threat keep it
        disp = np.sqrt(np.maximum(Rw[:, 0] / np.maximum(mw, 1e-9) - _csum(memmix * memmix), 0)) * (mw > 0)
        thr = 0.1 * ((g == G["unit"]) & (int(self._wf("war", 0)) > 0))
        tc = KTA[g, K_COH] - 0.8 * (disp - 0.35) + thr
        self.scoh += (act * ((1 - 0.96 ** dm) * (tc - self.scoh) + 0.015 * np.sqrt(dm) * self.rng.standard_normal((N, M)))).astype(f32)
        self.scoh = _uclip(self.scoh, 0.02, 0.98).astype(f32)
        # members' strictness on norm keys (for the local norms)
        self.sstrict = np.where(mw > 0, Rw[:, 1] / np.maximum(mw, 1e-9), 0).astype(f32)
        # splits: low cohesion and members pulling apart; the character goes with the side that fits them
        sp = act & ~hh & (self.scoh < 0.18) & (cnt >= 4) & (self.rng.random((N, M)) < 1 - 0.97 ** dm)
        for n_, j_ in zip(*np.nonzero(sp)):
            mem = np.nonzero(B[n_, :, j_] > 0)[0]
            lk = likeness(self.pie[n_, mem], self.w[n_])
            go = mem[lk < np.median(lk)]
            self.mset[n_, go] &= ~self._bit(j_)
            stay = mem[lk >= np.median(lk)]
            self.snorm[n_, j_] = _norm(0.5 * self.snorm[n_, j_] + 0.5 * self.pie[n_, stay].mean(0))
            self.scoh[n_, j_] = 0.55; self.sncast[n_, j_] = len(stay)
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="split", group=GROUP_KINDS[int(self.skind[n_, j_])],
                                        j=int(j_), left=[int(x_) for x_ in self.uid[n_, go]]))

    @property
    def set_sphere(self):
        """Each setting's sphere (N x M, index into SPHERES; -1 an empty slot): a work setting by its employer's
        sector (none known: commerce). Read only (item 15, Replace)."""
        g = self.skind.astype(np.int64); sph = GROUP_SPH[np.maximum(g, 0)]
        serv = SECTORS.index("services"); isec = self.inst_sector
        if isec is not None and len(isec):
            isec = np.asarray(isec, np.int64); sec = isec[np.clip(self.sref, 0, len(isec) - 1)]
            wsec = np.where((self.sref >= 0) & (sec >= 0), sec, serv)
        else:
            wsec = np.full(g.shape, serv)
        out = np.where(g < 0, -1, np.where(sph >= 0, sph, SECTOR_SPH[wsec]))
        if self.sph_h and getattr(self.W, "hp_s", None) is not None:   # phase 2: a setting at a place is in that place's sphere
            P_ = self.W.hp_s.shape[2]
            out = np.where(self.shnt >= 0, HAUNT_SPH[(np.maximum(self.shnt, 0) // P_) % len(HAUNT_KINDS)], out)
        return out

    def setting_places(self, n):
        """Life n's settings as places (item 15, phase 1d; read only, no dice): slot, kind, sphere, subsector, the
        place's name in the world's epoch, and the nearest face (the colour the setting's ways lean to most, with its
        name). A class at a university is learn.higher."""
        import sphere_data as SD
        ep = getattr(self.W, "sph_epoch", "modern"); ss = self.set_sphere[n]; out = []
        isec = self.inst_sector; ikind = self.inst_kind
        for j in np.nonzero(self.skind[n] >= 0)[0]:
            kind = GROUP_KINDS[int(self.skind[n, j])]; ref = int(self.sref[n, j])
            if kind == "work":
                sec = int(isec[ref]) if isec is not None and 0 <= ref < len(isec) and isec[ref] >= 0 else SECTORS.index("services")
                sub = WORK_SUB[SECTORS[sec]]
            elif kind == "class" and 0 <= ref < len(ikind) and ikind[ref] == INST_KINDS.index("university"):
                sub = "learn.higher"
            else:
                sub = SET_SUB[kind]
            sph = SPHERES[int(ss[j])]
            if not sub.startswith(sph + "."):        # the subsector follows the sphere the layer reads
                sub = sph + "." + SD.SUBSECTORS[sph][0]
            c = int(np.argmax(self.snorm[n, j])); fk = f"{sph}.{COLORS[c]}"
            out.append(dict(slot=int(j), kind=kind, sphere=sph, subsector=sub,
                            place=SD.PLACE_BY_EPOCH.get(sub, {}).get(ep), face=fk, face_name=SD.FACE_NAMES[fk]))
        return out

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 2
    def _sph_init(self):
        import sphere_data as SD
        N, M = self.N, self.M; pm = self.perm
        self.hnt = np.full((N, 3), -1, np.int64)     # N1: each life's haunts, flat place ids (World.place_info), best first
        self.shnt = np.full((N, M), -1, np.int64)    # the place a club, scene or congregation setting is held at
        self.rung = np.zeros((N, 9))                 # N2: standing in each sphere, 0 newcomer .. 4 leader (LADDER)
        self.ryrs = np.zeros((N, 9))                 # years present in each sphere's places
        self.hrs = np.zeros((N, len(TIME_ROWS)))     # hours a week by row (TIME_ROWS), this month
        self.hpick = -1                              # the year of age of the last yearly pick
        self.places_mix = None                       # the places part of item 12's current (sph_hours)
        self.places_ref = None                       # and the town's average for the same hours (cur_rel)
        self._hrng = np.random.default_rng([self.seed, 47, self.run_seed])   # haunt picks draw only here
        T = np.asarray(SD.TEACH, float)              # sphere x face x colour (W U B R G), into this world's frame
        self._teach = T[:, pm][:, :, pm]
        ep = getattr(self.W, "sph_epoch", "modern")
        self._tgrp = SD.TIME_GROUPS.index({"bands": "early", "villages": "early", "machine": "machine", "modern": "modern"}.get(ep, "middle"))
        self._time = SD.TIME; self._tages = SD.TIME_AGES; self._depth = np.array([SD.DEPTH[r_] for r_ in TIME_ROWS])
        self.mark = np.zeros((N, C))                 # the mark of the work drawn in so far (pie units, this world's frame)
        self.mark_dw = np.zeros((N, C))              # this year's step of it, for the engine to apply (then cleared)
        self._mark_yr = -1
        self._mark_tau = float(SD.MARK_TAU)
        hs_ = np.array([SD.HAUNT_SHARES[k_] for k_ in HAUNT_KINDS])   # how common each haunt kind is (modern shares)
        self._hprior = np.log(hs_ / hs_.mean())
        self._mark_pull = {k_: np.asarray(v_["pull"], float)[pm] for k_, v_ in SD.MARKS.items()}
        mz_ = {d_: (np.mean([v_[d_] for v_ in SD.MARKS.values()]), np.std([v_[d_] for v_ in SD.MARKS.values()]))
               for d_ in ("say", "skill")}
        self._mark_dim = {k_: (v_["danger"], v_["wear"], (v_["say"] - mz_["say"][0]) / mz_["say"][1],
                               (v_["skill"] - mz_["skill"][0]) / mz_["skill"][1]) for k_, v_ in SD.MARKS.items()}
        self.mark_wear = np.zeros(N)                 # years the body has aged beyond its own in hard work (.15 x wear a year)
        self.mark_hurt = np.zeros(N, bool)           # a serious injury at work this year, for the engine (then cleared)
        self.mark_die = np.zeros(N, bool)            # a death at work this year, for the engine (then cleared)
        self.mark_z = np.zeros((N, 2))               # the trade's say and skill (centred over the 60), while in it

    def _marks_year(self, t):
        """sph_marks, once a year: a worker's colours are drawn toward their trade's mark (marks.json, at its colour
        reading) with a drawing-in time of MARK_TAU years; the trade is the work setting's subsector (the employer's
        sector, as setting_places reads it). The step goes to the engine as mark_dw (pie units)."""
        a = self._age(t); yr = int(a)
        if yr == self._mark_yr:
            return
        self._mark_yr = yr
        wk = (self.skind == G["work"]); has = wk.any(1) & ~self.dead
        isec = self.inst_sector; serv = SECTORS.index("services")
        tgt = np.zeros((self.N, C)); dw_ = np.zeros((self.N, 2)); self.mark_z = np.zeros((self.N, 2))
        for n_ in np.nonzero(has)[0]:
            ref = int(self.sref[n_, int(np.argmax(wk[n_]))])
            sec = int(isec[ref]) if isec is not None and 0 <= ref < len(isec) and isec[ref] >= 0 else serv
            sub_ = WORK_SUB[SECTORS[sec]]
            tgt[n_] = self._mark_pull[sub_]
            dg_, wr_, sz_, kz_ = self._mark_dim[sub_]
            dw_[n_] = dg_, wr_; self.mark_z[n_] = sz_, kz_
        step = np.where(has[:, None], (tgt - self.mark) / self._mark_tau, 0.0)
        self.mark += step; self.mark_dw = self.mark_dw + step
        # the body (marks.json size.body): a serious injury at .03 x danger a work-year, a death at .0005 x danger; the
        # body ages .15 x wear years a year worked (the haunt stream draws, so every other stream draws as before)
        u_ = self._hrng.random((self.N, 2))
        self.mark_hurt |= has & (u_[:, 0] < 0.03 * dw_[:, 0])
        self.mark_die |= has & (u_[:, 1] < getattr(self, "mk_die", 0.0005) * dw_[:, 0])   # (engine work_die)
        self.mark_wear += 0.15 * dw_[:, 1] * has

    def _tstage(self, a):
        for st_, (lo_, hi_) in self._tages.items():
            if lo_ <= a < hi_ + 1:
                return st_
        return "old"

    def _haunt_hours(self, a):
        """Each life's free hours a week for haunts (the stage's mean, by sociability) and how many haunts that holds."""
        h = self._time[self._tstage(a)]["haunts"][self._tgrp] * np.sqrt(np.maximum(self.sociab, 0.05))
        n = np.where(h < 4, 1, np.where(h <= 10, 2, 3)) * (a >= 4)
        return h, n

    def _haunt_util(self, ns, a, kinds=None):
        """Utility of each place in each life's town (len(ns) x 31 kinds x N_PLACES): how common the kind is (the log of
        its share, HAUNT_SHARES), fit of the place's ways with the
        life's (a child's: the family's), money against what the kind costs, the age a kind asks, and a faith's places
        for those who keep one; plus a Gumbel draw from the haunt stream (who goes where is partly chance)."""
        W = self.W; hp = W.hp_s[self.loc[ns]]                                     # n x 31 x P x 5
        who = self.w[ns] if a >= 10 else self.family_mix[ns]
        fit_ = likeness(hp, who[:, None, None, :])
        mon = self.res[ns, MON] if self.res.shape[1] > MON else np.full(len(ns), 0.5)
        u = 12.0 * fit_ - 1.5 * HAUNT_COST[None, :, None] * (1 - mon)[:, None, None] + self._hprior[None, :, None]
        ok = (HAUNT_AGE <= a)[None, :]
        fk = np.array([k_.startswith("faith.") and k_ != "faith.seeking" for k_ in HAUNT_KINDS])
        ok = ok & ~(fk[None, :] & (self.pfaith[ns] < 0)[:, None])
        if kinds is not None:
            ok = ok & np.isin(np.arange(len(HAUNT_KINDS)), kinds)[None, :]
        u = u + self._hrng.gumbel(0, 1, u.shape)
        if getattr(self, "pt_on", False) and getattr(W, "pt_open", None) is not None:   # part 2: an empty slot is no place
            u = np.where(W.pt_open[self.loc[ns]] >= 0, -np.inf, u)
        return np.where(ok[:, :, None], u, -np.inf)

    def _haunts_year(self, t, ns=None):
        """N1: once a year (and on a move) each life picks its haunts by fit: one under 4 haunt hours a week, two at 4
        to 10, three above; a place they already go to, and one a setting of theirs meets at, is kept more often.
        A setting whose place is no longer theirs is left ("stopped going")."""
        a = self._age(t); live = ~self.dead
        ns = np.nonzero(live)[0] if ns is None else np.asarray(ns, np.int64)
        if not len(ns):
            return
        _, nh = self._haunt_hours(a); nh = nh[ns]
        u = self._haunt_util(ns, a)                                              # n x 31 x P
        H, P_ = u.shape[1], u.shape[2]
        base = self.loc[ns][:, None] * (H * P_)
        flat = u.reshape(len(ns), -1)
        held = self.hnt[ns]; linked = self.shnt[ns]
        for q_ in range(3):   # a haunt kept is easier to keep; one a setting meets at, easier still
            ok_ = (held[:, q_] >= 0) & (held[:, q_] // (H * P_) == self.loc[ns])
            ii_ = np.nonzero(ok_)[0]
            flat[ii_, held[ii_, q_] - base[ii_, 0]] += 1.0
        for j_ in range(self.M):
            ok_ = (linked[:, j_] >= 0) & (linked[:, j_] // (H * P_) == self.loc[ns])
            ii_ = np.nonzero(ok_)[0]
            flat[ii_, linked[ii_, j_] - base[ii_, 0]] += 2.0
        u = flat.reshape(u.shape)
        bp = u.argmax(2); bu = np.take_along_axis(u, bp[..., None], 2)[..., 0]  # each kind's best place
        order = np.argsort(-bu, 1, kind="stable")[:, :3]
        new = np.full((len(ns), 3), -1, np.int64)
        for q_ in range(3):
            k_ = order[:, q_]; ok_ = (q_ < nh) & np.isfinite(bu[np.arange(len(ns)), k_])
            new[ok_, q_] = base[ok_, 0] + k_[ok_] * P_ + bp[np.arange(len(ns)), k_][ok_]
        self.hnt[ns] = new
        for i_, n_ in enumerate(ns):   # settings held at a place that is no longer theirs
            for j_ in np.nonzero(self.shnt[n_] >= 0)[0]:
                if self.shnt[n_, j_] not in new[i_]:
                    self._leave(int(n_), int(j_), t, "stopped going")

    def _haunt_for(self, n, kind):
        """The place a new setting of this kind is held at: the life's best haunt of a fitting kind that no setting of
        theirs meets at yet, else the town's best fitting place of such a kind, which becomes a haunt. -1: none."""
        H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]; a = self._age()
        ks = SET_HAUNTS.get(kind)
        if not ks:
            return -1
        for p_ in self.hnt[n]:
            if p_ >= 0 and (p_ // P_) % H in ks and p_ not in self.shnt[n] and p_ // (H * P_) == self.loc[n]:
                return int(p_)
        u = self._haunt_util(np.array([n]), a, kinds=ks)[0]
        if not np.isfinite(u).any():
            return -1
        k_, i_ = np.unravel_index(int(np.argmax(u)), u.shape)
        p_ = int(self.loc[n] * H * P_ + k_ * P_ + i_)
        self._haunt_add(n, p_)
        return p_

    def _haunt_add(self, n, p_, first=False):
        """Place p_ becomes one of life n's haunts: first (the player's pick) or in a free slot, else in the last one."""
        h_ = [x_ for x_ in self.hnt[n] if x_ >= 0 and x_ != p_]
        h_ = [p_] + h_ if first else h_ + [p_]
        if len(h_) > 3:
            h_ = h_[:2] + [p_] if not first else h_[:3]
        self.hnt[n] = (h_ + [-1, -1, -1])[:3]

    def pick_haunt(self, n, sphere, colour, t=None, kind=None):
        """The player's (or the life's own) haunt choice (N1; the haunt choice moments): the town's place in that sphere
        whose ways lean most to that face becomes their first haunt, and they go: a setting meets there (a congregation
        for a faith's place, a scene or a club for the rest). colour: W U B R G (the face's letter); returns the place.
        kind: only places of that haunt kind (HAUNT_KINDS index; a footprint's place, foot_on), else any of the sphere's."""
        t = self.t if t is None else t; n = int(n)
        if not self.sph_h:
            return -1
        H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]; a = self._age(t)
        j = SPHERES.index(sphere) if isinstance(sphere, str) else int(sphere)
        c = int(self.iperm[COLORS.index(colour) if isinstance(colour, str) else int(colour)])
        ks = [k_ for k_ in range(H) if HAUNT_SPH[k_] == j and HAUNT_AGE[k_] <= a and (kind is None or k_ == kind)]
        if not ks:
            return -1
        hp = self.W.hp_s[self.loc[n]][ks]                                         # kinds x P x 5
        hc_ = hp[..., c]
        if getattr(self, "pt_on", False) and getattr(self.W, "pt_open", None) is not None:   # part 2: not an empty slot
            hc_ = np.where(self.W.pt_open[self.loc[n]][ks] >= 0, -np.inf, hc_)
            if not np.isfinite(hc_).any():
                return -1
        k_, i_ = np.unravel_index(int(np.argmax(hc_)), hp.shape[:2])
        p_ = int(self.loc[n] * H * P_ + ks[k_] * P_ + i_)
        self._haunt_add(n, p_, first=True)
        if p_ not in self.shnt[n]:
            kn_ = HAUNT_KINDS[ks[k_]]
            kind = "congregation" if kn_.startswith("faith.") else "scene" if kn_ in SCENE_HAUNTS else "club"
            if kind == "congregation" and self.pfaith[n] < 0:
                self.pfaith[n] = self._faith_for(n)
            self._force_place = (n, p_)
            try:
                self.join(n, kind, t)
            finally:
                self._force_place = None
        return p_

    def _haunts_month(self, t):
        """Monthly: a setting held at a place takes the place's ways as its anchor (the town's spheres reach the life
        through its haunts); the setting's leader is the keeper, its members regulars, and keepers and leaders of any
        setting can be go-betweens (N4)."""
        on = self.shnt >= 0
        if on.any():
            n_, j_ = np.nonzero(on)
            H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]
            p_ = self.shnt[n_, j_]
            self.sanch[n_, j_] = self.W.hp_s.reshape(-1, C)[p_]
            ld_ = self.slead[n_, j_]; ok_ = ld_ >= 0
            self.rmask[n_[ok_], ld_[ok_]] |= BIT["keeper"] | BIT["go-between"]
            B = self._bits()
            mem = (B[n_, :, j_] > 0)                                              # rows x K
            rr, kk = np.nonzero(mem)
            self.rmask[n_[rr], kk] |= BIT["regular"]
        ld = self.slead >= 0
        if ld.any():
            n_, j_ = np.nonzero(ld)
            self.rmask[n_, self.slead[n_, j_]] |= BIT["go-between"]

    def _sph_hours(self, t):
        """Monthly (sph_hours): hours a week in each of the eight rows (dynamics.json exposure, this epoch's column, by
        the life's settings), the places part of item 12's current (each row's mix x hours x depth x (1 + .25 x rung))
        and, yearly, the rungs (N2): years present in a sphere's places make a regular (1) and a known face (5); rank .85
        or more in a setting there makes a pillar, leading one a leader; absence fades a rung a step a year."""
        W = self.W; N = self.N; a = self._age(t); T = self._time[self._tstage(a)]; g = self._tgrp
        sph = getattr(W, "sph_s", None)
        if sph is None:
            return
        town = sph[self.loc]                                                      # N x 9 x 5
        ph_ = getattr(W, "sph_ph", None) if W.p.get("sph_pairs", False) else None
        tm = W.sph_teach_mix((town, None if ph_ is None else ph_[self.loc]), self._teach)   # each town sphere's teaching mix
        has = lambda k_: (self.skind == G[k_])
        def set_mix(k_):
            h_ = has(k_); any_ = h_.any(1); j_ = h_.argmax(1)
            return any_, self.snorm[np.arange(N), j_].astype(float)
        S_ = SPHERES.index
        hrs = np.zeros((N, 8)); mix = np.zeros((N, 8, C)); rs = np.zeros((N, 8), np.int64)
        wk_, wm_ = set_mix("work"); ws_ = self.set_sphere[np.arange(N), has("work").argmax(1)]
        hrs[:, 0] = T["work"][g] * wk_; mix[:, 0] = np.where(wk_[:, None], wm_, tm[:, S_("comm")]); rs[:, 0] = np.where(wk_, ws_, S_("comm"))
        cl_, cm_ = set_mix("class")
        hrs[:, 1] = np.where(cl_, max(T["learn"][g], 12.0 if a >= 5 else 0.0), T["learn"][g] * (a >= 18))
        mix[:, 1] = np.where(cl_[:, None], cm_, tm[:, S_("learn")]); rs[:, 1] = S_("learn")
        hh, _ = self._haunt_hours(a)
        if self.sph_h:
            ok_ = self.hnt >= 0; nk_ = ok_.sum(1)
            hs_ = HAUNT_SPH[(np.maximum(self.hnt, 0) // W.hp_s.shape[2]) % len(HAUNT_KINDS)]   # N x 3
            hm_ = np.einsum("nqf,nqfc->nqc", W.hp_s.reshape(-1, C)[np.maximum(self.hnt, 0)], self._teach[hs_])
            hm_ = (hm_ * ok_[..., None]).sum(1) / np.maximum(nk_, 1)[:, None]
            hsph = hs_[:, 0]
            hrs[:, 2] = hh * (nk_ > 0); mix[:, 2] = np.where((nk_ > 0)[:, None], hm_, tm[:, S_("gather")]); rs[:, 2] = hsph
        else:
            hrs[:, 2] = hh * (a >= 4); mix[:, 2] = tm[:, S_("gather")]; rs[:, 2] = S_("gather")
        fa_, fm_ = set_mix("congregation")
        hrs[:, 3] = T["faith"][g] * np.where(fa_, 1.6, 0.25)   # the row is the mean: members about 1.6 times it (most belong); mix[:, 3] = np.where(fa_[:, None], fm_, tm[:, S_("faith")]); rs[:, 3] = S_("faith")
        isch = (self.rmask & BIT["child"]) != 0
        small = (isch & self.used & self.lv & ((t - self.born) < 6 * 52)).any(1)
        hrs[:, 4] = T["care_given"][g] * np.where(small, 2.5, 1.0); mix[:, 4] = tm[:, S_("care")]; rs[:, 4] = S_("care")
        un_, um_ = set_mix("unit")
        hrs[:, 5] = np.where(un_, 40.0, T["service"][g]); mix[:, 5] = np.where(un_[:, None], um_, tm[:, S_("prot")]); rs[:, 5] = S_("prot")
        rr_ = np.floor(self.rung[:, S_("rule")])
        hrs[:, 6] = T["civic"][g] * np.where(rr_ >= 4, 6.0, np.where(rr_ >= 3, 3.0, 1.0)); mix[:, 6] = tm[:, S_("rule")]; rs[:, 6] = S_("rule")
        hrs[:, 7] = T["market"][g]; mix[:, 7] = tm[:, S_("comm")]; rs[:, 7] = S_("comm")
        if W.p.get("sph_deep", False):   # phase 5: the care load (who carries whom) adds care hours and costs work hours
            self.care_load = self._care_load(t)
            if getattr(self, "care_buy", None) is not None:   # bought help: care hours x .7 (phase5c-answers.md)
                self.care_load = self.care_load * np.where(self.care_buy, getattr(self, "care_buy_x", 0.7), 1.0)
            hrs[:, 4] += self.care_load; hrs[:, 0] = np.maximum(0.0, hrs[:, 0] - 0.1 * self.care_load)   # 1 work hour per 10
        if W.p.get("sph_seasons", False):                                         # N7: the year's rhythm in each row's sphere
            hrs = hrs * W._sph_tables()["seas_h"][rs, W.season]
        self.hrs = hrs
        if W.p.get("sph_shadow", False):   # N5: the shadow around them, the hours-weighted shadow share of their rows' spheres
            rsh = np.take_along_axis(W._sph_sh()[self.loc], rs[:, :, None], 1)  # N x 8 x 5
            self.sh_around = (hrs[..., None] * rsh).sum(1) / np.maximum(hrs.sum(1), 1e-9)[:, None]
        wt = hrs * self._depth[None] * (1 + 0.25 * np.floor(np.take_along_axis(self.rung, rs, 1)))
        if getattr(self, "odd_on", False):   # S4: an odd-one-out place's pull on their colours x odd_press (its row's weight;
            ms_, mh_ = self._odd_press()      # among the haunts, its share of the row)
            for r_, k_ in ((0, "work"), (3, "congregation"), (5, "unit")):
                h_ = has(k_)
                wt[:, r_] *= np.where(h_.any(1), ms_[np.arange(N), h_.argmax(1)], 1.0)
            if self.sph_h:
                hq_ = ok_ * mh_
                hmq_ = np.einsum("nqf,nqfc->nqc", W.hp_s.reshape(-1, C)[np.maximum(self.hnt, 0)], self._teach[hs_])
                mix[:, 2] = np.where((nk_ > 0)[:, None], (hmq_ * hq_[..., None]).sum(1) / np.maximum(hq_.sum(1), 1e-9)[:, None], mix[:, 2])
                wt[:, 2] *= np.where(nk_ > 0, hq_.sum(1) / np.maximum(nk_, 1), 1.0)
        tot = wt.sum(1)
        self.places_mix = np.where(tot[:, None] > 1e-9, (wt[..., None] * mix).sum(1) / np.maximum(tot, 1e-9)[:, None], self.w)
        # the same hours in the town's own place of each row's sphere: what the current's places part is read against (cur_rel)
        rm_ = np.take_along_axis(tm, rs[:, :, None], 1)
        self.places_ref = np.where(tot[:, None] > 1e-9, (wt[..., None] * rm_).sum(1) / np.maximum(tot, 1e-9)[:, None], 0.2)
        yr = int(a)
        if yr != getattr(self, "_rung_yr", -1):   # the rungs, once a year
            self._rung_yr = yr
            # present where a community meets them: the work, the class, each haunt, the congregation, the unit (not the
            # shops, the town's council or the care given at home, which make no one known)
            pres = np.zeros((N, 9)); ar_ = np.arange(N)
            np.add.at(pres, (ar_, rs[:, 0]), hrs[:, 0]); np.add.at(pres, (ar_, rs[:, 1]), hrs[:, 1] * cl_)
            np.add.at(pres, (ar_, rs[:, 3]), hrs[:, 3] * fa_); np.add.at(pres, (ar_, rs[:, 5]), hrs[:, 5] * un_)
            if self.sph_h:
                for q_ in range(3):
                    ok_ = self.hnt[:, q_] >= 0
                    np.add.at(pres, (ar_[ok_], hs_[ok_, q_]), (hrs[:, 2] / np.maximum(nk_, 1))[ok_])
            here = pres >= 2.0
            if getattr(self, "eyes_on", False):   # S3: a good name at their places speeds the climb, a bad one slows it; S4: x1.5 both ways
                mu_up, mu_dn = self._eyes_rung_mult()
                self.ryrs = np.where(here, self.ryrs + mu_up, self.ryrs * 0.8)
            else:
                self.ryrs = np.where(here, self.ryrs + 1, self.ryrs * 0.8)
            tg = np.where(self.ryrs >= 5, 2, np.where(self.ryrs >= 1, 1, 0)).astype(float)   # years make a regular, then a known face
            ss = self.set_sphere; act = self.skind >= 0
            for j_ in range(self.M):   # standing earned in a setting: a pillar there (rank .85 or more), its leader a leader
                sj = ss[:, j_]; ok_ = act[:, j_] & (sj >= 0)
                ii_ = np.nonzero(ok_)[0]
                tg[ii_, sj[ii_]] = np.maximum(tg[ii_, sj[ii_]], np.where(self.slead[ii_, j_] == -2, 4, np.where(self.srank[ii_, j_] >= 0.85, 3, 0)))
            if getattr(self, "eyes_on", False):
                self.rung = np.where(tg >= self.rung, np.minimum(tg, self.rung + mu_up), np.maximum(tg, self.rung - mu_dn))
            else:
                self.rung = np.where(tg >= self.rung, np.minimum(tg, self.rung + 1), np.maximum(tg, self.rung - 1))

    def _care_load(self, t):
        """Phase 5 (sph_deep), "who carries whom": hours a week of care each life gives (N; deep_state.care_load). A close
        partner, parent, parent-in-law or grandparent (closeness layer 2 or nearer) in poor health (under .35) or 82 or
        older needs care: partner 20, parent 12, parent-in-law 8, grandparent 4 hours, x 1.5 under health .2. A partner's
        lands on the life; a parent's or grandparent's is shared with the close siblings still living, and a
        parent-in-law's with the partner, each weighted 1 + .5 x the world's role strictness (1 - acceptance of role
        crossing) toward the expected carer (a daughter; a daughter-in-law); x (1 - .5 x the town's care.reach). At
        most 60. Not yet: money buying hours."""
        import sphere_data as SD
        D = SD.DEEP; H = D["care_hours"]
        L2 = self.P["layer_c"][1]; rm = self.rmask
        live = self.used & self.lv & (self.c >= L2)
        has = lambda r_: (rm & BIT[r_]) != 0
        age = (t - self.born) / 52.0; mine = (t - self.t0) / 52.0
        need = live & ((self.health < 0.35) | (age >= 82))
        fx = np.where(self.health < D["care_frail"], D["care_frail_x"], 1.0)
        rs = 1.0 - float(self.W.norm("role crossing"))
        wt = lambda fem_: 1.0 + D["care_role"] * rs * fem_                      # toward the expected carer
        own = wt(self.female.astype(float))
        sib = (live & has("sibling")) * wt(self.fem.astype(float))
        share = own / (own + sib.sum(1))                                         # of a parent's or grandparent's care
        pil = need & has("inlaw") & (age >= mine + 15)                          # the partner's parents
        ps_ = (self.used & self.lv & has("partner"))
        p_fem = (ps_ & self.fem).any(1).astype(float)
        share_il = np.where(ps_.any(1), own / (own + wt(p_fem)), 1.0)
        h = ((need & has("partner")) * H["partner"] * fx).sum(1) \
            + ((need & has("parent")) * H["parent"] * fx).sum(1) * share \
            + ((need & has("grandparent")) * H["grandparent"] * fx).sum(1) * share \
            + (pil * H["parent_in_law"] * fx).sum(1) * share_il
        W = self.W; E = W._sph_ev_tables()
        st = getattr(W, "sph_st", None)
        if st is not None and "care.reach" in E["own"]:
            k_ = E["own"].index("care.reach"); rch = np.clip(st[:, k_] + W.sph_st_soc[k_] - 0.5, 0, 1)[self.loc]
        else:
            rch = np.full(self.N, 0.5)
        return np.where(self.dead, 0.0, np.minimum(60.0, h * (1 - D["care_public"] * rch)))

    def haunts_info(self, n):
        """Life n's haunts (N1), best first, as World.place_info gives them, each with whether a setting of theirs meets
        there, and their rung in each sphere (N2): {sphere: rung word}. For the game's "your places"."""
        if not self.sph_h:
            return dict(haunts=[], rungs={})
        out = [dict(self.W.place_info(int(p_)), setting=bool(p_ in self.shnt[n])) for p_ in self.hnt[n] if p_ >= 0]
        return dict(haunts=out, rungs={s_: LADDER[int(self.rung[n, j_])] for j_, s_ in enumerate(SPHERES)})

    def around(self):
        """S2 (read only, for the game's "making it their own"): the colour shares of what surrounds each life (N x C,
        each row summing to 1): half the faces of their haunts (best first, weighted 3, 2, 1, as World.place_info gives
        them), half their close circle's colours (the steady current's close part); without haunts, the circle alone."""
        cl = np.asarray(self.cur_parts[0], float) if getattr(self, "cur_parts", None) is not None else np.full((self.N, C), 1.0 / C)
        hp = getattr(self.W, "hp_s", None)
        if not self.sph_h or hp is None:
            return _norm(cl)
        hf = np.zeros((self.N, C)); hw = np.zeros(self.N); ip = np.argsort(self.W.perm)
        for k_, wk_ in enumerate((3.0, 2.0, 1.0)[:self.hnt.shape[1]]):
            on = self.hnt[:, k_] >= 0
            if on.any():
                l_, h_, i_ = np.unravel_index(self.hnt[on, k_], hp.shape[:3])
                hf[on] += wk_ * np.asarray(hp[l_, h_, i_], float)[:, ip]; hw[on] += wk_
        hf = np.where(hw[:, None] > 0, hf / np.maximum(hw, 1e-9)[:, None], cl)
        return _norm(0.5 * _norm(hf) + 0.5 * cl)

    def _outputs_settings(self):
        """Cached monthly: the settings' part of the niche, of belonging and of the community driver."""
        act = self.skind >= 0; g = np.maximum(self.skind, 0); a = self._age()
        agew = np.where((g == G["class"]) & (12 <= a < 19), 1.5, 1.0)
        sw = self.sts * (0.5 + self.scoh) * agew * act
        if getattr(self, "odd_on", False):   # S4: an odd-one-out place's pull on their colours x odd_press
            sw = sw * self._odd_press()[0]
        self._setw = sw.sum(1); self._setmix = (sw[..., None] * self.snorm).sum(1)
        fitj = _uclip(likeness(self.snorm, self.w[:, None, :]), 0, 1)
        accj = 0.5 * fitj + 0.5 * self.srank
        self._belong_set = (self.sts * self.scoh * accj * act).sum(1)
        self._comm = (COMM_W[g] * self.scoh * accj * act).sum(1)
        self.community = _uclip(self.P["comm_k"] * (self._comm - self.P["comm_ref"]), -0.5, 0.5)
