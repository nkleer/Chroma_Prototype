"""People's methods for the weekly, monthly and quarterly ticks, ties, the engine's commitments in the cast and the
life course of settings.

Part of class People (world_people.py), which inherits TicksMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import numpy as np
from library import RESOURCES
from world_keys import HAUNT_KINDS
from world_people_base import (BIT, C, CAR, COM, CORE, ENGINE_ROLES, FAI, G, HEA, KID, KINMASK, PAR, R, TIM,
    VOLUNTARY, WI, _isin_small, _ix, _norm, _nz2, _uclip, likeness)


class TicksMixin:
    # ------------------------------------------------------------------ the weekly, monthly and quarterly ticks
    def _read_S(self, t, S):
        S = S or {}
        N = self.N
        g_ = lambda k_, d_: d_ if S.get(k_) is None else S.get(k_)
        self.w = _norm(np.asarray(g_("w", self.w), float).reshape(N, C)); self.w32 = self.w.astype(np.float32)
        self.held = np.asarray(g_("held", self.held), bool).reshape(N, -1)
        self.res = np.asarray(g_("res", np.full((N, len(RESOURCES)), 0.5)), float).reshape(N, -1)
        self.stress = np.broadcast_to(np.asarray(g_("stress", 0.0), float), (N,))
        self.outlook = np.broadcast_to(np.asarray(g_("outlook", 0.45), float), (N,))
        self.attr = np.broadcast_to(np.asarray(g_("attr", 0), np.int64), (N,))
        self.risky = np.broadcast_to(np.asarray(g_("risky", 0.0), float), (N,))
        self.dead = np.broadcast_to(np.asarray(g_("dead", False), bool), (N,)).copy()
        if S.get("lens") is not None:
            self.lens = _norm(np.asarray(S["lens"], float).reshape(N, C))
        if S.get("sector") is not None:
            self.psector = np.broadcast_to(np.asarray(S["sector"], np.int64), (N,)).copy()
        ps_ = S.get("partner_same")   # the engine's own draw: the partner it holds is of the character's sex
        self.partner_same = None if ps_ is None else np.broadcast_to(np.asarray(ps_, bool), (N,)).copy()
        ts_ = S.get("title_standing")
        self.title_st = None if ts_ is None else np.asarray(ts_, float)
        ds_ = S.get("domain_standing")   # (N, len(DOMAINS)) 0-3: a title's standing in its own domain
        self.dom_st = None if ds_ is None else np.asarray(ds_, float)
        if getattr(self, "lw", False) and S.get("lead_has") is not None:   # S7: the leading titles held (LEAD_TITLES)
            self.lw_has = np.asarray(S["lead_has"], bool).reshape(N, -1)
        kc_ = S.get("children")          # the engine's living children (its alive[:, 5]; or S["alive"] with 6 columns)
        if kc_ is None and S.get("alive") is not None and np.ndim(S["alive"]) == 2 and np.shape(S["alive"])[1] > 5:
            kc_ = np.asarray(S["alive"])[:, 5]
        if kc_ is not None:
            self.kids_eng = np.broadcast_to(np.round(np.asarray(kc_, float)).astype(np.int64), (N,)).copy()

    def tick(self, t, S):
        """One week of the cast, plus the month's settings and the quarter's outer layers on their weeks."""
        self.week(t, S)
        if t % 4 == 0:
            self.month(t, S)
        if t % 13 == 0:
            self.quarter(t, S)

    def week(self, t, S):
        """Cast layers 1-2 (contact, closeness, deaths), the partner and children the engine holds, wants ripening,
        and everything the engine reads this week. S: the engine's person state (see the module's notes)."""
        if self._last_w == t:
            return
        self._last_w = t; self.t = t
        self.events = self._carry; self._carry = []; self.died[:] = 0
        self._read_S(t, S)
        for n_, kind_ in self.pend.pop(t, []):
            self._born_kin(n_, kind_, t)
        self._sync(t)
        self._close_step(t, 1)
        if self.P["auto_move"]:
            mv = np.nonzero(~self.dead & (self.rng.random(self.N) < self.move_wish(t)))[0]
            for n_ in mv:
                self.move(int(n_), t=t)
        if self.far_on:
            self._far_week(t)
        if getattr(self, "fr_read", False):
            self._fair_week(t)
        if self.sac_on:
            self._sac_week(t)
        if getattr(self, "bt_on", False):
            self._bt_week(t)
        if self.wa_on:   # the world answers (world_people_answers): asks, told events, a Known life's decisions
            self._wa_week(t)
        self._wants_week(t)
        self._outputs(t)

    def month(self, t, S):
        if self._last_m == t:
            return
        self._last_m = t; self.t = t
        if self._last_w != t:
            self._read_S(t, S)
        if self.sph_h:   # spheres phase 2: a life that has moved picks its haunts in the new town
            H_ = len(HAUNT_KINDS) * self.W.hp_s.shape[2] if getattr(self.W, "hp_s", None) is not None else 0
            if H_:
                mv_ = np.nonzero(~self.dead & (self.hnt[:, 0] >= 0) & (self.hnt[:, 0] // H_ != self.loc))[0]
                if len(mv_) or self.hpick < 0 or int(self._age(t)) != self.hpick:
                    if self.hpick < 0 or int(self._age(t)) != self.hpick:
                        self.hpick = int(self._age(t)); self._haunts_year(t)
                    else:
                        self._haunts_year(t, mv_)
        self._lifecourse(t)
        if self.far_on:
            self._far_month(t)
        if self.sac_on:
            self._sac_month(t)
        if self._xsoc:
            self._lang_step(t)
        if getattr(self, "eyes_on", False):   # S3, S4: the places read again, names fade, the caught-between and odd-one-out moments wait
            self._eyes_month(t)
        if self.sph_h and getattr(self.W, "hp_s", None) is not None:
            self._haunts_month(t)
        if self.sph_hr:
            self._sph_hours(t)
        if self.sph_mk:
            self._marks_year(t)
        if getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False):
            self._sph_year4(t)
        if getattr(self, "bt_on", False):   # body_trust: after felt fairness's year
            self._bt_year(t)
        if self.wa_on:   # the world answers: presence in settings and places, the figures around a Known life
            self._wa_month(t)
        B = self._bits()
        if getattr(self, "comrade", None) is not None:   # phase 5: whoever shares a unit with them is a comrade from now on
            un_ = (self.skind == G["unit"])
            if un_.any():
                self.comrade |= (B * un_[:, None, :]).any(2)
        if self._last_set is None or t - self._last_set >= 8:   # the settings' slow drift: every second month
            self._settings_month(t, S, B, 1.0 if self._last_set is None else (t - self._last_set) / 4.0)
            self._last_set = t
        self._fsh(B)
        self._close_index()
        self._standing(t)
        self._outputs_settings()
        self._ties()

    def quarter(self, t, S):
        if self._last_q == t:
            return
        self._last_q = t; self.t = t
        if self._last_w != t:
            self._read_S(t, S)
        self._inst_refresh()
        self._norm_hist(t)
        self._outer_step(t)
        if t - self._last_lives >= 26:   # the cast's own light lives: every half year
            self._lives(t, (t - self._last_lives) / 52.0); self._last_lives = t
        self._ties()
        self._membership(t)
        self._new_people(t)
        self._roles(t)
        self._wants_arise(t)
        self._cleanup(t)
        self._alive_counts(np.arange(self.N))
        self._approval(t)   # felt acceptance per norm key: once a quarter (views move slowly)
        if getattr(self, "pt_on", False):   # part 2: the places that closed and opened this quarter (before the posts')
            self._pt_q(t)
        if self.lw:          # S7: the posts' quarter (after the settings' leaders are replaced)
            self._lead_q(t)
        if self.seen_on:    # seen_done (S6): what the cast and the figures were seen to do this quarter
            self._seen_q(t)

    # ------------------------------------------------------------------ ties: contact and closeness (spec 2 §3)
    def _tie_target(self, n2=None, k2=None):
        """What contact supports for slots (n2, k2) (index arrays of one shape; None: every slot, as (N, K)):
        contacts a year, the closeness they hold (ceiling x f / (f + f_half)), likeness to the character, ceiling.
        Likeness and the deliberate budget per unit of closeness^alloc_pow are the month's (_fsh, _close_index)."""
        P = self.P; f32 = np.float32
        if n2 is None:
            g = lambda A_: A_
            pp = lambda v_: v_[:, None]
        else:
            fi = _ix(np.asarray(n2, np.int64) * self.K + k2)
            g = lambda A_: np.take(A_, fi)
            pp = lambda v_: v_[n2]
        lk = g(self._lkm)
        near = g(self.mloc) == pp(self.loc.astype(self.mloc.dtype))
        if self._xsoc:   # someone in another society is far wherever they live
            near &= g(self.msoc) == pp(self.soc.astype(self.msoc.dtype))
        comm = float(self._wf("comm", 0.5))
        dist = np.where(near, f32(1.0), f32(P["dist_far"] + 0.5 * comm))
        hj = pp(self.hhj)
        hh = (((g(self.mset) >> np.maximum(hj, 0).astype(self.mset.dtype)) & 1) > 0) & (hj >= 0)
        core = np.where((g(self.rmask) & CORE) != 0, f32(1.3), f32(1.0))
        c = g(self.c)
        fdel = pp(self._Dn) * self._cpow(c) * core * dist * dist * ~hh
        f = g(self.fsh) + np.where(near, g(self.fkin), g(self.fkin_far) * f32(0.5 + comm)) + fdel
        cap = (f32(1 - P["cap_like"]) + f32(P["cap_like"]) * lk) * (f32(0.75) + f32(0.25) * g(self.trust))
        return f, cap * f / (f + f32(P["f_half"])), lk, cap

    def _cpow(self, c):
        """closeness^alloc_pow (2.5 by default: c^2 sqrt(c), cheaper than a power)."""
        ap = self.P["alloc_pow"]
        return c * c * np.sqrt(c) if ap == 2.5 else c ** np.float32(ap)

    def _close_step(self, t, dt_w):
        """Layers 1-2 weekly: closeness, contact and deaths of the close index (slow terms cached monthly)."""
        P = self.P; fi = self._fi
        ok = (np.take(self.uid, fi) == self._cuid) & np.take(self.lv, fi) & ~self.dead[:, None]   # dropped: id -1
        c = np.take(self.c, fi)
        f = self._cf0 + self._cdf * self._cpow(c)
        e = self._ccap * f / (f + np.float32(P["f_half"]))
        r_up, r_dk, r_dn = self._r_w if dt_w == 1 else [np.float32(1 - np.exp(-dt_w / 52.0 / P[k_]))
                                                         for k_ in ("tau_up", "tau_dn_kin", "tau_dn")]
        rdn = self._crdn if dt_w == 1 else np.where(self._ckin, r_dk, r_dn)
        if dt_w != 1 and getattr(self, "comrade", None) is not None:
            rdn = np.where(self._ccom, rdn * np.float32(0.5), rdn)
        if dt_w != 1 and getattr(self, "inmate", None) is not None:   # part 4: fellow inmates (once, with a comrade too)
            rdn = np.where(self._cinm, rdn * np.float32(0.5), rdn)
        rr = np.where(e > c, r_up, rdn)
        c2 = np.where(ok, c + (e - c) * rr, c).astype(np.float32)
        np.put(self.c, fi, c2)
        self._cok = ok; self._cc = c2   # for this week's on_act
        U = self.rng.random((2,) + f.shape, dtype=np.float32)
        met = ok & (U[0] < f * np.float32(dt_w / 52.0))
        np.put(self.last, fi[met], t)
        dies = ok & (U[1] < self._cq * np.float32(dt_w))
        if self.kids_eng is not None:   # the character's children die only by the engine's moment (R15, kill())
            dies &= (self._crm & BIT["child"]) == 0
        if dies.any():
            self._die(self._n2[dies], self.ci[dies], t)

    def _outer_step(self, t):
        """Quarterly: layers 3-4 (everyone outside the close index): closeness, contact, deaths; for all the living:
        the reading sharpens, trust drifts, a few ties break. Whole (N, K) arrays, masked, float32."""
        P = self.P; f32 = np.float32
        live = self.used & self.lv & ~self.dead[:, None]
        if not live.any():
            return
        f, e, lk, _ = self._tie_target()
        self._lk = lk
        out = live & ~self.inci
        c = self.c
        kin = (self.rmask & KINMASK) != 0
        r_up, r_dk, r_dn = (f32(1 - np.exp(-13 / 52.0 / P[k_])) for k_ in ("tau_up", "tau_dn_kin", "tau_dn"))
        if getattr(self, "inmate", None) is not None:   # part 4: fellow inmates outside the close index, at half speed too
            r_dn = np.where(self._inmate_on(), r_dn * f32(0.5), r_dn)
        c2 = np.where(out, c + (e - c) * np.where(e > c, r_up, np.where(kin, r_dk, r_dn)), c).astype(f32)
        self.c = c2; np.maximum(self.cmax, c2, out=self.cmax)
        U = self.rng.random((3,) + c.shape, dtype=f32)
        self.last[out & (U[0] < -np.expm1(f * f32(-0.25)))] = t
        age = self._qage = (t - self.born).astype(f32) * f32(1 / 52.0); self._qage_t = t
        q = np.minimum(self._q(age, self.health, self.mcls)
                       * np.where(age >= 65, self._rate_at("old_death", self.mloc), self._rate_at("illness", self.mloc)), f32(0.95))
        dies = out & (U[1] < -np.expm1(f32(0.25) * np.log1p(-q)))
        if self.kids_eng is not None:
            dies &= (self.rmask & BIT["child"]) == 0
        # the reading sharpens with shared time (contacts) and is bent by the character's lens
        # (in one pass: read += lam (pie - read), then read += m (lens - read), with m = 0.01 for the living)
        lam = np.where(live, -np.expm1(f * f32(-0.0025)), f32(0)); m_ = f32(0.01) * live
        a_ = (f32(1) - m_) * lam
        rd = self.read; tmp = self.pie * a_[..., None]; tmp += m_[..., None] * self.lens.astype(f32)[:, None, :]
        rd *= (f32(1) - a_ - m_)[..., None]; rd += tmp
        # trust drifts toward what likeness and shared history support
        tb = _uclip(f32(0.45) + f32(0.35) * lk + f32(0.05) * self.mgood - f32(0.1) * self.mbad, f32(0.02), f32(0.98))
        self.trust += live * f32(P["trust_k"]) * (tb - self.trust)
        # breaks: a fight or a betrayal (rarer among the alike; kin rarely)
        rm = self.rmask
        bp = f32(P["break_p"] * 0.25) * (f32(1.5) - lk) * np.where((rm & KINMASK) == 0, f32(1.0), f32(0.33))
        brk = live & (c2 >= P["layer_c"][2]) & ((rm & BIT["partner"]) == 0) & (U[2] < bp)
        for n_, k_ in zip(*_nz2(brk)):
            self._break(n_, k_, t)
        if dies.any():
            nn, kk = _nz2(dies)
            self._die(nn, kk, t)

    def _break(self, n, k, t, why="fight"):
        self.c[n, k] *= 0.3; self.trust[n, k] *= 0.6; self.brk[n, k] = t; self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="break", cid=int(self.uid[n, k]), role=self._rname(n, k), why=why))

    def _die(self, n, k, t, count=True):
        n = np.asarray(n, np.int64); k = np.asarray(k, np.int64)
        P = self.P
        hit = self.lv[n, k]
        n, k = n[hit], k[hit]
        if not len(n):
            return
        rm = self.rmask[n, k]
        if count:
            L2 = P["layer_c"][1]
            was_friend = ((rm & BIT["friend"]) != 0) & ((rm & KINMASK) == 0) & (self.c[n, k] >= L2)
            if was_friend.any():   # the engine's friend column is the closest friend (0/1): only their death counts
                fn, fk = n[was_friend], k[was_friend]
                un = np.unique(fn); rmu = self.rmask[un]; cu = self.c[un]
                cand = (self.used[un] & self.lv[un] & ((rmu & BIT["friend"]) != 0) & ((rmu & KINMASK) == 0) & (cu >= L2))
                best = np.argmax(np.where(cand, cu, -1), 1)
                was_friend[was_friend] = fk == best[np.searchsorted(un, fn)]
            for i_, r_ in enumerate(ENGINE_ROLES):
                h_ = was_friend if r_ == "friend" else (rm & BIT[r_]) != 0
                if h_.any():
                    self.died[:, i_] += np.bincount(_ix(n[h_]), minlength=self.N)
        self.lv[n, k] = False; self.died_t[n, k] = t; self.mset[n, k] = 0
        self.want[n, k] = -1; self.wstate[n, k] = 0
        ev = self.watch[n] & ((self.cmax[n, k] >= P["layer_c"][3]) | ((rm & KINMASK) != 0))
        ne, ke = n[ev], k[ev]
        if len(ne):
            self.events.extend(dict(n=n_, t=int(t), kind="died", cid=u_, role=r_, age=a_) for n_, u_, r_, a_ in
                               zip(ne.tolist(), self.uid[ne, ke].tolist(), self._rnames(ne, ke),
                                   ((t - self.born[ne, ke]) // 52).tolist()))
        self._alive_counts(np.unique(n))

    def kill(self, n, role, t=None):
        """An engine moment kills someone of this engine role (parent, sibling, friend, grandparent, partner): the
        member is chosen by the life table's odds; returns their cast id (or -1 when no one fits)."""
        t = self.t if t is None else t
        cand = np.nonzero(self._has_role(n, role) & self.lv[n])[0]
        if not len(cand):
            return -1
        q = self._q((t - self.born[n, cand]) / 52.0, self.health[n, cand]) + 1e-6
        k = int(self.rng.choice(cand, p=q / q.sum()))
        self._die([n], [k], t, count=False)
        return int(self.uid[n, k])

    def _has_role(self, n, role):
        u = self.used[n]
        if role == "friend":
            return u & ((self.rmask[n] & BIT["friend"]) != 0) & ((self.rmask[n] & KINMASK) == 0)
        if role == "partner":
            m_ = np.zeros(self.K, bool)
            if self.pslot[n] >= 0:
                m_[self.pslot[n]] = True
            return m_
        return u & ((self.rmask[n] & BIT[role]) != 0)

    def _inmate_on(self):
        """Part 4 (prison_ties): the fellow inmates still within 10 years of when they were made (N, K)."""
        return self.inmate & (self.t - self.inmate_t < 520)

    def inmate_closest(self, n):
        """Part 4: life n's closest living fellow inmate within the 10 years (a slot), -1 when none."""
        if getattr(self, "inmate", None) is None:
            return -1
        m_ = self._inmate_on()[n] & self.used[n] & self.lv[n]
        return int(np.argmax(np.where(m_, self.c[n], -1.0))) if m_.any() else -1

    def _close_index(self):
        """Monthly: the KC closest living people of each life (updated weekly), the denominator of deliberate
        contact, and the slow terms of their weekly update (contact from settings and kin, ceilings, death odds)."""
        P = self.P; N = self.N; f32 = np.float32
        np.maximum(self.cmax, self.c, out=self.cmax)
        ul = self.used & self.lv
        sc = np.where(ul, self.c, f32(-1))
        ci = np.argpartition(-sc, self.KC - 1, axis=1)[:, :self.KC]
        self.ci = ci; n2 = self._n2 = np.repeat(np.arange(N)[:, None], self.KC, 1)
        fi = self._fi = _ix(n2 * self.K + ci)   # flat (N, KC) indices into (N, K) arrays
        self.inci[:] = False
        np.put(self.inci, fi, np.take(sc, fi) >= 0)
        comm = float(self._wf("comm", 0.5))
        here = self.mloc == self.loc.astype(self.mloc.dtype)[:, None]
        if self._xsoc:
            here &= self.msoc == self.soc.astype(self.msoc.dtype)[:, None]
        dist = np.where(here, f32(1.0), f32(P["dist_far"] + 0.5 * comm))
        hh = (((self.mset >> np.maximum(self.hhj, 0).astype(self.mset.dtype)[:, None]) & 1) > 0) & (self.hhj[:, None] >= 0)
        core = np.where((self.rmask & CORE) != 0, f32(1.3), f32(1.0))
        self._den = (self._cpow(self.c) * core * dist * (ul & ~hh)).sum(1, dtype=np.float64) + 0.05
        a = self._age()
        dstage = 0.3 if a < 12 else 0.8 if a >= 70 else 1.0
        self._Dn = (P["D0"] * dstage * self.sociab * (0.5 + self.res[:, TIM]) / self._den).astype(f32)
        # cached for the weekly step: f = cf0 + cdf x c^alloc_pow, e = ccap x f / (f + f_half)
        f0, e0, lk, cap = self._tie_target(n2, ci)
        d2 = np.take(dist, fi)
        tk = lambda A_: np.take(A_, fi)
        self._cdf = (self._Dn[:, None] * tk(core) * d2 * d2 * ~tk(hh)).astype(f32)
        self._cf0 = np.maximum(f0 - self._cdf * self._cpow(tk(self.c)), 0).astype(f32)
        self._ccap = cap.astype(f32)
        self._crm = tk(self.rmask)
        self._ckin = (self._crm & KINMASK) != 0
        self._crdn = np.where(self._ckin, self._r_w[1], self._r_w[2])   # the weekly fading rate (kin fade slower)
        if getattr(self, "comrade", None) is not None:   # phase 5: comrades from a unit fade at half speed
            self._ccom = tk(self.comrade)
            self._crdn = np.where(self._ccom, self._crdn * np.float32(0.5), self._crdn)
        if getattr(self, "inmate", None) is not None:   # part 4: fellow inmates fade at half speed for 10 years
            self._cinm = tk(self._inmate_on())
            if getattr(self, "comrade", None) is not None:
                self._cinm = self._cinm & ~self._ccom   # (half speed once, a comrade or not)
            self._crdn = np.where(self._cinm, self._crdn * np.float32(0.5), self._crdn)
        self._cuid = tk(self.uid)
        self._cpie = np.take(self.pie.reshape(-1, C), fi, axis=0).astype(np.float64)   # float64: exact weekly sums
        self._cpage = (self.t - tk(self.born)) / 52.0
        age = self._cpage; lc = tk(self.mloc)
        q = self._q(age, tk(self.health), tk(self.mcls)) * np.where(age >= 65, self._rate("old_death", lc), self._rate("illness", lc))
        self._cq = (np.minimum(q, 0.95) / 52.0).astype(f32)
        self._cav = (tk(self.health) * (0.5 + 0.5 * tk(self.money)) * (tk(self.mood) >= 0.35)).astype(f32)
        # the weight of each close person's colors in the niche, by the character's age and their role (monthly)
        a = self._age(); rm = self._crm
        if a < 12:
            self._caw = np.where((rm & BIT["parent"]) != 0, f32(3.0), np.where((rm & BIT["sibling"]) != 0, f32(1.5), f32(0.5)))
        elif a < 18:
            peer = ~self._ckin & (np.abs(self._cpage - a) <= 3)
            self._caw = np.where((rm & BIT["parent"]) != 0, f32(0.8), np.where(peer, f32(2.0), f32(1.0)))
        else:
            self._caw = np.where((rm & BIT["partner"]) != 0, f32(1.5), f32(1.0))
        # the engine's friend column (a close non-kin friend, layers 1-2: all in the close index); the other columns
        # change with births, deaths and partners, which recount them, and once a quarter in full
        self.alive[:, 2] = (((self._crm & BIT["friend"]) != 0) & ~self._ckin & (tk(self.c) >= P["layer_c"][1])
                            & tk(self.used) & tk(self.lv)).any(1)

    def _alive_counts(self, ns=None):
        """The engine's alive columns, counted from the cast: living parents, siblings (born), a closest friend (0/1),
        grandparents, partner (0/1)."""
        ns = np.arange(self.N) if ns is None else np.unique(np.atleast_1d(np.asarray(ns, np.int64)))
        if not len(ns):
            return
        L2 = self.P["layer_c"][1]
        u = self.used[ns] & self.lv[ns]; rm = self.rmask[ns]
        hasr = lambda r_: ((rm & BIT[r_]) != 0) & u
        ps = self.pslot[ns]
        pl = (ps >= 0) & self.lv[ns, np.maximum(ps, 0)]
        self._nch[ns] = (((rm & BIT["child"]) != 0) & self.used[ns]).sum(1)   # children, living or not
        self._nchl[ns] = (((rm & BIT["child"]) != 0) & u).sum(1)              # living children
        self.alive[ns] = np.stack([hasr("parent").sum(1), (hasr("sibling") & (self.born[ns] <= self.t)).sum(1),
                                   (hasr("friend") & ((rm & KINMASK) == 0) & (self.c[ns] >= L2)).any(1),
                                   hasr("grandparent").sum(1), pl], 1)

    # ------------------------------------------------------------------ the engine's commitments in the cast
    def _born_kin(self, n, kind, t):
        """A younger sibling, or the character's own child, is born."""
        if self.dead[n] and kind == "child":
            return
        P = self.P; rng = self.rng
        if kind == "sibling":
            pr = np.nonzero(self._has_role(n, "parent") & self.lv[n])[0]
            ctx = _norm(self.pie[n, pr].mean(0)) if len(pr) else self.family_mix[n]
            F = self._gen(np.array([n]), np.array([t]), t, ctx=ctx[None], sel=P["pie_inherit"])
            F["mcls"][:] = self.cls[n]; F["line"][:] = self.pline[n]; F["mloc"][:] = self.mloc[n, pr[0]] if len(pr) else self.loc[n]
            F["msoc"] = np.full(1, self.msoc[n, pr[0]] if len(pr) else self.soc[n])
            F["faith"] = np.where(rng.random(1) < P["p_inherit"], self.pfaith[n], F["faith"])
            F["party"] = np.where(rng.random(1) < P["p_inherit"], self.pparty[n], F["party"])
            home = (not self.own_home[n]) and self.hhj[n] >= 0
            sl = self._add(F, t, R["sibling"], c0=0.5 if home else 0.15, trust0=0.6, acc0=0.2,
                           setbit=self.hhj[n] if home else -1, quiet=True)
        else:
            self._born_kids(np.array([n]), t)
            return
        if self.watch[n] and len(sl):
            self.events.append(dict(n=int(n), t=int(t), kind="born", cid=int(self.uid[n, sl[0]]), role=kind))
        self._alive_counts([n])

    def _born_kids(self, ns, t):
        """The characters ns each have a child: the two parents' ways pass on moderately; faith and party most
        strongly (p_inherit); the child joins the household."""
        ns = np.asarray(ns, np.int64); ns = ns[~self.dead[ns]]
        if not len(ns):
            return
        P = self.P; rng = self.rng; E = len(ns)
        ps = self.pslot[ns]; hp = ps >= 0; pk = np.maximum(ps, 0)
        ctx = np.where(hp[:, None], 0.5 * (self.w[ns] + self.pie[ns, pk]), self.w[ns])
        F = self._gen(ns, np.full(E, t), t, ctx=ctx, sel=P["pie_inherit"])
        F["mcls"][:] = self.cls[ns]; F["line"][:] = self.pline[ns]; F["mloc"][:] = self.loc[ns]
        myf = np.where(self.held[ns, FAI], self.pfaith[ns], -1) if self.held.shape[1] > FAI else np.full(E, -1)
        F["faith"] = np.where(rng.random(E) < P["p_inherit"], myf, F["faith"])
        pp_ = np.where(hp, self.party[ns, pk], self.pparty[ns])
        F["party"] = np.where(rng.random(E) < P["p_inherit"], pp_, F["party"])
        for n_ in ns[self.hhj[ns] < 0]:
            self.hhj[n_] = self._new_setting(int(n_), "household", t); self.own_home[n_] = True
        sl = self._add(F, t, R["child"], c0=0.85, trust0=0.8, acc0=0.3, setbit=self.hhj[ns], quiet=True)
        ok = sl >= 0
        self.kof[ns[ok & hp], sl[ok & hp]] = self.uid[ns[ok & hp], ps[ok & hp]]
        for n_, s_ in zip(ns[ok], sl[ok]):
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="born", cid=int(self.uid[n_, s_]), role="child"))
        self._alive_counts(ns)

    def _sync(self, t):
        """The partner and the children follow the engine's commitments."""
        held = self.held; P = self.P; rng = self.rng; a = self._age(t)
        ps = self.pslot
        has = (ps >= 0)
        hasliving = has.copy(); hasliving[has] = self.lv[np.nonzero(has)[0], ps[has]]
        if held.shape[1] <= PAR:
            return
        refill_ = held[:, PAR] & ~hasliving & ~self.dead
        if getattr(self, "or_on", False):   # F7 (one_roll): a partner the world took is not replaced while the engine still
            # holds the partnership (its widowhood ends it within weeks); only a new partner commitment brings someone
            wid_ = getattr(self, "p_wid", None)
            self.p_wid = ((np.zeros(len(held), bool) if wid_ is None else wid_) | (has & ~hasliving)) & held[:, PAR]
            refill_ &= ~self.p_wid
        for n_ in np.nonzero(refill_)[0]:
            self._new_partner(int(n_), t)
        for n_ in np.nonzero(~held[:, PAR] & hasliving)[0]:
            k_ = int(ps[n_])
            self.rmask[n_, k_] = (self.rmask[n_, k_] & ~BIT["partner"]) | BIT["ex"]; self.role[n_, k_] = R["ex"]
            if self.hhj[n_] >= 0:
                self.mset[n_, k_] &= ~self._bit(self.hhj[n_])
            self.c[n_, k_] *= 0.35; self.trust[n_, k_] *= 0.6; self.brk[n_, k_] = t; self.pslot[n_] = -1
            self.par_change[n_] = t
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="ex", cid=int(self.uid[n_, k_])))
            self._alive_counts([n_])
        dead_p = has & ~hasliving
        self.pslot[dead_p] = -1
        if self.partner_same is not None:   # the cast partner's sex follows the engine's partner_same
            hp = np.nonzero(self.pslot >= 0)[0]
            self.fem[hp, self.pslot[hp]] = self.female[hp] == self.partner_same[hp]
        if self.kids_eng is not None:   # the engine's count: each child it adds joins the cast, born now (deaths: kill())
            need = np.where(self.dead, 0, self.kids_eng - self._nchl)
            for r_ in range(int(need.max()) if len(need) else 0):
                self._born_kids(np.nonzero(need > r_)[0], t)
        elif held.shape[1] > KID:   # no count from the engine: the first child when it holds children
            self._born_kids(np.nonzero(held[:, KID] & (self._nch == 0) & ~self.dead)[0], t)

    def _new_partner(self, n, t):
        """The engine's partner commitment begins: a prospect from the cast, or someone new chosen alike (spouses
        start alike: the best of six); their family and friends join through them."""
        P = self.P; rng = self.rng; a = self._age(t)
        same = rng.random() < P["same_sex"][int(_uclip(self.attr[n], 0, 4))]
        if self.partner_same is not None:
            same = bool(self.partner_same[n])
        want_fem = bool(self.female[n]) == bool(same)
        cand = np.nonzero(self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["prospect"] | BIT["friend"])) != 0)
                          & ((self.rmask[n] & KINMASK) == 0) & (self.fem[n] == want_fem) & ~self.mpart[n]
                          & (np.abs((t - self.born[n]) / 52.0 - a) <= 8))[0]
        if len(cand) and rng.random() < 0.6:
            sc = likeness(self.pie[n, cand], self.w[n]) * self.c[n, cand] + 0.5 * (self.want[n, cand] == WI["love"])
            k = int(cand[np.argmax(sc)])
        else:
            born = t - ((a + rng.normal(1.5 if not want_fem else -1.0, 3.5, 6)) * 52).astype(np.int64)
            F = self._gen(np.full(6, n), born, t)
            best = int(np.argmax(likeness(F["pie"], self.w[n])))
            F = {k2: (v2[best:best + 1] if np.ndim(v2) else v2) for k2, v2 in F.items()}
            F["fem"] = np.array([want_fem]); F["mpart"] = np.array([False]); F["nkids"] = np.array([0])
            k = int(self._add(F, t, R["partner"], c0=0.5, trust0=0.7, acc0=0.15, quiet=True)[0])
            # the partner's family and friends come through them (spec 2 §1 "through others")
            pa = (t - self.born[n, k]) / 52.0
            fam_b = []
            for d_ in (rng.normal(30, 5), rng.normal(32, 5)):
                if rng.random() < self._surv(pa, pa + d_):
                    fam_b.append(t - int((pa + d_) * 52))
            nsb = rng.choice(4, p=P["sib_p"])
            fam_b += [t - int((pa + rng.normal(0, 4)) * 52) for _ in range(nsb)]
            if fam_b:
                Fi = self._gen(np.full(len(fam_b), n), np.array(fam_b), t, ctx=np.tile(self.pie[n, k], (len(fam_b), 1)),
                               sel=P["pie_inherit"])
                Fi["mloc"][:] = self.mloc[n, k]; Fi["line"][:] = self.line[n, k]; Fi["msoc"] = np.full(len(fam_b), self.msoc[n, k])
                self._add(Fi, t, R["inlaw"], c0=0.1, trust0=0.5, kof=np.full(len(fam_b), self.uid[n, k]), quiet=True)
            nf = int(rng.integers(3, 6))
            Ff = self._gen(np.full(nf, n), t - ((pa + rng.normal(0, 4, nf)) * 52).astype(np.int64), t,
                           ctx=np.tile(self.pie[n, k], (nf, 1)), sel=0.4)
            self._add(Ff, t, R["acquaintance"], c0=0.06, trust0=0.5, kof=np.full(nf, self.uid[n, k]), quiet=True)
        self.rmask[n, k] = (self.rmask[n, k] & ~BIT["prospect"]) | BIT["partner"]; self.role[n, k] = R["partner"]
        self.c[n, k] = max(float(self.c[n, k]), 0.85); self.trust[n, k] = max(float(self.trust[n, k]), 0.75)
        self.mloc[n, k] = self.loc[n]; self.msoc[n, k] = self.soc[n]; self.pslot[n] = k; self.par_change[n] = t
        if self.want[n, k] == WI["love"]:
            self.want[n, k] = -1; self.wstate[n, k] = 0
        if a >= 17 and not self.own_home[n]:
            self._leave_home(n, t)
        if self.hhj[n] < 0:
            self.hhj[n] = self._new_setting(n, "household", t); self.own_home[n] = True
        self.mset[n, k] |= self._bit(self.hhj[n])
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="partner", cid=int(self.uid[n, k])))
        self._alive_counts([n])

    def _leave_home(self, n, t):
        """The character leaves the parents' household for one of their own (the partner and children come along)."""
        old = self.hhj[n]
        if old >= 0:
            self._leave(n, int(old), t, "left home")
        j = self._new_setting(n, "household", t)
        self.hhj[n] = j; self.own_home[n] = True
        if j >= 0:
            self.sanch[n, j] = self.w[n]; self.snorm[n, j] = self.w[n]
            mates = np.nonzero(self.used[n] & self.lv[n] & (((self.rmask[n] & BIT["partner"]) != 0)
                                                            | (((self.rmask[n] & BIT["child"]) != 0) & ((t - self.born[n]) < 18 * 52))))[0]
            self.mset[n, mates] |= self._bit(j)

    # ------------------------------------------------------------------ the life course of settings (spec 3 §1.6)
    def _lifecourse(self, t):
        """Monthly: the groups a life holds by age and by the engine's commitments (spec 3 §1.6)."""
        self._defer = []
        try:
            self._lifecourse_(t)
        finally:
            batch, self._defer = self._defer, None
            self._fill_members(batch, t)

    def _lifecourse_(self, t):
        a = self._age(t); P = self.P; rng = self.rng; N = self.N; held = self.held
        live = ~self.dead
        has = lambda g_: (self.skind == G[g_]).any(1)
        nz = lambda m_: np.nonzero(m_)[0]
        mo = 1 / 12.0
        if a >= 4:
            self._join_many(nz(live & ~has("neighbours")), "neighbours", t)
        # school: a class from 5, a new one at 11, study after 18 for some
        cj = np.where(self.skind == G["class"], self.sjoin, -1).max(1)
        if 5 <= a < 18:
            need = live & ((cj < 0) | ((a >= 11) & (cj < self.t0 + 11 * 52)))
            for n_ in nz(need & (cj >= 0)):
                self.leave(int(n_), "class", t, "school changed")
            self._join_many(nz(need), "class", t)
        if a >= 18:
            sec = live & (cj >= 0) & (cj < self.t0 + int(17.5 * 52))
            leaving = sec | (live & (cj >= 0) & (t - cj > int(3.5 * 52)))
            for n_ in nz(leaving):
                self.leave(int(n_), "class", t, "finished")
            if a < 19:
                pu = np.asarray(P["p_uni"])[_uclip(self.cls, 0, 2)]
                self._join_many(nz(sec & (rng.random(N) < pu)), "class", t)
        nvol = _isin_small(self.skind, VOLUNTARY).sum(1)
        if 6 <= a < 18:   # children's and teenagers' activities; a scene or an online community for some teens
            self._join_many(nz(live & (nvol < self.vol_tgt) & (rng.random(N) < 0.1)), "club", t)
            if a >= 13:
                self._join_many(nz(live & ~has("scene") & (rng.random(N) < 0.3 / 60)), "scene", t)
                if self._tech("internet"):
                    self._join_many(nz(live & ~has("online") & (rng.random(N) < 0.5 / 60)), "online", t)
        if a >= 18:
            vj = P["vol_join"]
            self._join_many(nz(live & (nvol < 3) & (rng.random(N) < vj["club"] * mo)), "club", t)
            if a < 40:
                self._join_many(nz(live & ~has("scene") & (rng.random(N) < vj["scene"] * mo)), "scene", t)
            if a < 70 and self._tech("internet"):
                self._join_many(nz(live & ~has("online") & (rng.random(N) < vj["online"] * mo)), "online", t)
        # leaving groups: a steady rate, faster in old age (settings thin out)
        lv = P["vol_leave"] * (1 + max(0.0, a - 70) / 10) * (0.6 if a < 18 else 1.0) * mo
        vol_or_on = _isin_small(self.skind, np.concatenate([VOLUNTARY[VOLUNTARY != G["congregation"]], [G["online"]]]))
        for n_, j_ in zip(*np.nonzero(vol_or_on & (rng.random(self.skind.shape) < lv) & live[:, None])):
            if self.skind[n_, j_] == G["movement"] and self.srank[n_, j_] > 0.6:
                continue
            self._leave(int(n_), int(j_), t, "drifted away")
        # work, faith and community follow the engine's commitments
        if held.shape[1] > FAI and a >= 14:
            self._join_many(nz(live & held[:, CAR] & ~has("work")), "work", t)
            for n_ in nz(live & ~held[:, CAR] & has("work")):
                self.leave(int(n_), "work", t, "job ended")
            nf = nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith < 0))
            for n_ in nf:
                self.pfaith[n_] = self._faith_for(int(n_))
            self._join_many(nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith >= 0)), "congregation", t)
            if a >= 16:
                for n_ in nz(live & ~held[:, FAI] & has("congregation")):
                    self.leave(int(n_), "congregation", t, "left the faith")
            nvol = _isin_small(self.skind, VOLUNTARY).sum(1)
            self._join_many(nz(live & held[:, COM] & (nvol == 0)), "club", t)
        elif held.shape[1] > FAI and a < 14:   # a child goes to the congregation with a practising family
            self._join_many(nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith >= 0)), "congregation", t)
        # leaving home; care homes in old age
        if a >= 17.5:
            for n_ in nz(live & ~self.own_home & (rng.random(N) < P["leave_home"] * mo)):
                self._leave_home(int(n_), t)
        if a >= 75:
            hl = self.res[:, HEA] if self.res.shape[1] > HEA else np.full(N, 0.5)
            self._join_many(nz(live & (hl < 0.35) & ~has("ward") & (rng.random(N) < P["care_home"] * mo)), "ward", t)
        # parents separate while the child is young
        if a < 18:
            for n_ in nz(live & ~self.own_home & (rng.random(N) < P["sep_p"] * mo)):
                if self.hhj[n_] < 0:
                    continue
                pa = self._has_role(n_, "parent") & self.lv[n_]
                ps = np.nonzero(pa & ~self.fem[n_] & (((self.mset[n_] >> self.hhj[n_]) & 1) > 0))[0]
                if len(ps) and pa.sum() == 2:
                    self.mset[n_, ps] &= ~self._bit(self.hhj[n_]); self.par_apart[n_] = True
                    if self.watch[n_]:
                        self.events.append(dict(n=int(n_), t=int(t), kind="parents_apart", cid=int(self.uid[n_, ps[0]])))
        # the character's children leave home at 18 to 24; more children while the engine holds children
        isch = (self.rmask & BIT["child"]) != 0
        if a >= 30:   # (a child of the character's is 18 only from about 34)
            hb = (((self.mset >> np.maximum(self.hhj, 0).astype(self.mset.dtype)[:, None]) & 1) > 0) & (self.hhj >= 0)[:, None]
            cn, ck = _nz2(isch & self.used & self.lv & hb)
            go = ((t - self.born[cn, ck]) >= 18 * 52) & (rng.random(len(cn)) < 0.25 * mo)
            for n_, k_ in zip(cn[go], ck[go]):
                self.mset[n_, k_] &= ~self._bit(self.hhj[n_])
        if held.shape[1] > KID and a < 44 and self.kids_eng is None:   # (when the engine counts them, its count rules)
            nk = isch.sum(1)
            more = live & held[:, KID] & (self.pslot >= 0) & (nk >= 1) & (nk < 4)
            p_ = np.where(nk == 1, 0.15, 0.07) * mo
            self._born_kids(nz(more & (rng.random(N) < p_)), t)

    def _tech(self, key):
        try:
            return bool(self.W.tech_has(key))
        except Exception:
            return True
