"""WorldLink's methods for how the world tilts the engine's rates: the era, moments by month, titles' sectors, options
closed by law, norm and technology, roles and acceptance, the channels, reach and odds. Part of class WorldLink
(world_link.py), which inherits LinkRatesMixin; moved out of world_link.py verbatim. A method here reads module names
through the imports below, the same objects world_link.py has, and self for everything on the link."""
# the same imports as world_link.py, so each method compiles to the code it was there
import copy
import hashlib
import json
import os
import pickle
import re
import sys
import numpy as np
try:   # speed pass: np.clip's own ufunc, called without its Python wrapper (the same numbers)
    from numpy._core.umath import clip as _uclip
except ImportError:
    from numpy.core.umath import clip as _uclip
import world as WM
import world_people as PM
import world_keys as WK
from world_link_base import *  # noqa: F401,F403
from world_link_base import _isin_small, _uclip  # noqa: F401


class LinkRatesMixin:
    def era(self):
        W = self.W
        return float(W.era_i), np.asarray(W.era_p, float), int(W.era_k)

    # ---- monthly: per person and moment, how the world tilts or gates the moment
    def moment_factor(self, age, sit_last=None):
        W, PP, N, S = self.W, self.PP, self.N, self.S
        f = np.ones((N, S))
        if self.toy_on.any():   # time of year: a set season holds the moment to it (x4 there, 0 elsewhere); an inferred
            a_ = np.where(self.toy_set, 1.0, 0.25)                    # tilt keeps a quarter of that (the year's mean stays 1)
            ins_ = self.toy[:, int(W.season)] > 0
            f *= np.where(self.toy_on, (1 - a_) + a_ * 4 * ins_, 1.0)[None]
        if (self.holy >= 0).any():   # a holy day moment comes in the weeks of that day (of the culture's main faith)
            hw_ = W.holy_weeks(); wk_ = int(W.week_of_year)
            for si in np.nonzero(self.holy >= 0)[0]:
                ws_ = hw_.get(WK.HOLY_KEYS[self.holy[si]], set())
                f[:, si] *= (52.0 / max(len(ws_), 1)) if wk_ in ws_ else 0.0
        if self.where.any():   # a place feature the moment needs
            feat = np.asarray(getattr(W, "loc_feat", np.zeros((1, self.where.shape[1]), bool)), bool)[PP.loc]   # N, F
            need = self.where.any(1)
            ok = (feat.astype(np.float32) @ self.where.T.astype(np.float32)) > 0                             # N, S
            f *= np.where(need[None], ok, 1.0)
        if self.c2 and len(self.c2_only):   # C2: these come only on the world's events
            f[:, self.c2_only] = 0.0
        if (self.group >= 0).any():   # a setting of that kind the person is in
            ing = (np.asarray(PP.skind)[:, :, None] == np.arange(len(WK.GROUP_KINDS))[None, None, :]).any(1)   # speed pass: one comparison
            gs_ = self.group >= 0
            f[:, gs_] *= ing[:, self.group[gs_]]
        if (self.haunt >= 0).any():   # spheres phase 2: among the regulars of a haunt of that kind (the great gathering:
            hn_ = getattr(PP, "hnt", None)                       # the whole town's); no haunts built, never
            hs_ = np.nonzero(self.haunt >= 0)[0]
            if hn_ is None or getattr(W, "hp_s", None) is None:
                f[:, hs_] = 0.0
            else:
                P_ = W.hp_s.shape[2]; hk_ = np.where(hn_ >= 0, (hn_ // P_) % len(WK.HAUNT_KINDS), -1)   # N x 3
                ok_ = (hk_[:, :, None] == self.haunt[hs_][None, None, :]).any(1) | (self.haunt[hs_] == self.H_GREAT)[None, :]
                f[:, hs_] *= ok_
        if (self.sphev >= 0).any():   # a sphere event's moment: only in a town that had that event in the last year, and
            se_ = np.nonzero(self.sphev >= 0)[0]                  # once for each time it fired (not met since it fired)
            last_ = getattr(W, "sph_ev_last", None)
            if not W.p.get("sph_events") or last_ is None:
                f[:, se_] = 0.0
            else:
                lf_ = last_[np.asarray(PP.loc)][:, self.sphev[se_]]
                f[:, se_] *= (int(W.t) - lf_) <= 52
                if sit_last is not None:
                    f[:, se_] *= sit_last[:, se_] < lf_
        if (self.ladder >= 0).any():   # a rung in the moment's sphere (no sphere: any) at least the one it names
            rg_ = getattr(PP, "rung", None)
            ls_ = np.nonzero(self.ladder >= 0)[0]
            if rg_ is None or not getattr(PP, "sph_hr", False):
                f[:, ls_] = 0.0
            else:
                rgm_ = np.where((self.msph[ls_] >= 0)[None, :], rg_[:, np.maximum(self.msph[ls_], 0)], rg_.max(1)[:, None])
                f[:, ls_] *= np.floor(rgm_) >= self.ladder[ls_][None, :]
        if self.pt_m.any():   # part 2: a place moment comes only with its closing or opening (brought, never drawn)
            f[:, self.pt_m] = 0.0
        if (self.shadow >= 0).any():   # part 5: the town gone grey (grey_gate, with sph_shadow's shares; off, never)
            sh_ = np.nonzero(self.shadow >= 0)[0]
            if not (self.grey_on and W.p.get("sph_shadow")):
                f[:, sh_] = 0.0
            else:
                g_ = W.sph_grey()[np.asarray(PP.loc)]                       # N x 9, each life's town
                g_ = np.concatenate([g_, g_.max(1, keepdims=True)], 1)      # + town: the greyest sphere
                f[:, sh_] *= g_[:, self.shadow[sh_]] >= self.grey_thr
        if (self.prem >= 0).any():   # a moment that needs a technology the world has not got
            th_ = {}   # speed pass: each technology asked once a week
            for si in np.nonzero(self.prem >= 0)[0]:
                k_ = int(self.prem[si])
                if k_ not in th_:
                    th_[k_] = W.tech_has(WK.TECH_KEYS[k_])
                if not th_[k_]:
                    f[:, si] = 0.0
        self.fac = f
        return f

    def rate_factor(self, held_title_sector):
        """Per person and moment, the world's multiplier on a life event's yearly rate (N, S)."""
        W, PP, N, S = self.W, self.PP, self.N, self.S
        r = np.ones((N, S))
        if getattr(self, "_rk_m", None) is None:   # speed pass: each kind's moments found once (rk never changes)
            self._rk_m = [(k_, nm_, self.rk == k_) for k_, nm_ in enumerate(RK) if (self.rk == k_).any()]
        for k_, nm_, m_ in self._rk_m:
            v_ = W.rate_mult(nm_)
            if nm_ in ("disaster", "crime"):
                v_ = np.asarray(v_, float)[PP.loc][:, None]
            elif nm_ == "jobloss":
                v_ = np.asarray(v_, float)[_uclip(held_title_sector, 0, len(v_) - 1)][:, None]
                v_ = np.where((held_title_sector >= 0)[:, None], v_, float(np.mean(W.rate_mult("jobloss"))))
                if getattr(PP, "c3_jl", None) is not None:   # C3: a merger's quarter of risk
                    v_ = v_ * np.where(PP.c3_jl > W.t, W._c_par("merge_jl"), 1.0)[:, None]
            r[:, m_] *= v_
        ci_ = W.c4_illness() if W.p.get("c4_nature") else None   # C4: bad air or water in the person's place
        if ci_ is not None and self.ill_s.any():
            r[:, self.ill_s] *= ci_[PP.loc][:, None]
        r[:, self.wm_s] = 0.0          # these come on the world's events instead
        return r

    # ---- options: law, norm and technology (world-fields.md)
    def closures(self, s, partner_same, age):
        """Units of closure per option (N, K) by kind: law, approval (norm) and means (technology), and the options
        the world has not got (not offered). A legal option written closed by law is opened (law_open)."""
        W, PP, N = self.W, self.PP, self.N
        K = self.law.shape[1]
        lw = self.law[s]; nm = self.norm[s]; te = self.tech[s]
        u_law = np.zeros((N, K)); law_open = np.zeros((N, K), bool); u_app = np.zeros((N, K)); u_mea = np.zeros((N, K))
        gone = np.zeros((N, K), bool)
        if (lw >= 0).any():
            st_ = np.array([W.law_state(k_) for k_ in WK.LAW_KEYS_ALL])[np.maximum(lw, 0)]   # 0 legal, 1 restricted, 2 banned
            if self.law_neg.any():   # -key: against the law where the act is in force or allowed (evading a call-up)
                st_ = np.where(self.law_neg[s], 2 - st_, st_)
            app_ = lw >= 0
            app_ &= (lw != self.ssm) | partner_same[:, None]      # same-sex marriage's law binds a same-sex couple only
            u_law = np.where(app_, np.where(st_ == 2, 1.0, np.where(st_ == 1, 0.5, 0.0)), 0.0)
            law_open = app_ & (st_ == 0)
        if (nm >= 0).any():
            acc_ = self.acc_                                        # N, n_norm: society's norm with the close circle's view
            if self.c2 and (self.group[s] >= 0).any():   # C2: in a group's moment, half society's norm, half the group's
                acc_ = self._c2_accept(s, acc_)
            a_ = np.take_along_axis(acc_, np.maximum(nm, 0), 1)
            if self.norm_neg.any():   # -key: frowned on where the norm is accepted (snubbing a same-sex partner)
                a_ = np.where(self.norm_neg[s], 1 - a_, a_)
            u_app = np.where(nm >= 0, 2.0 * (1 - a_), 0.0)
        if (te >= 0).any():
            for k_ in np.unique(te[te >= 0]):
                key = WK.TECH_KEYS[k_]
                if not W.tech_has(key):
                    gone |= te == k_
                else:
                    ad_ = np.array([W.tech_adopt(key, cls=int(c_)) for c_ in range(3)])[_uclip(PP.cls, 0, 2)]
                    u_mea = np.maximum(u_mea, np.where(te == k_, 1 - ad_[:, None], 0.0))
        if getattr(PP, "eyes_on", False) and (self.caught[s] == WK.CAUGHT_TAGS.index("bridge")).any():
            for n_, pv_ in self.pending.items():   # S3: a bridge is offered only to one known or more in both places' spheres
                if pv_[1] == "caught" and pv_[2] == s[n_] and not PP.eyes_bridge_ok(n_):
                    gone[n_] |= self.caught[s[n_]] == WK.CAUGHT_TAGS.index("bridge")
        return u_law, law_open, u_app, u_mea, gone

    def _c2_accept(self, s, acc_):
        """C2: acceptance per norm key for lives whose moment s has a group: (1 - group_half) x the society's norm +
        group_half x that group's view (its members' acceptance, as the local norm reads it: the norms now less 1.2 x the
        members' strictness), less a close person's objection; the rest keep acc_ (society with the close circle)."""
        PP, W = self.PP, self.W
        g_ = self.group[s]; rows = np.nonzero(g_ >= 0)[0]
        m_ = PP.skind[rows] == g_[rows][:, None]
        rows = rows[m_.any(1)]
        if not len(rows):
            return acc_
        m_ = PP.skind[rows] == g_[rows][:, None]
        j_ = np.argmax(np.where(m_, PP.sts[rows] + 1.0, 0.0), 1)
        nv = np.array([float(W.norm(k_)) for k_ in WK.NORM_KEYS_ALL])
        if not PP.nh:
            return acc_
        now = PM._logit(np.asarray(PP.nh[-1], float))
        grp = PM._sig(now[None, :] - 1.2 * PP.sstrict[rows, j_][:, None])
        grp = np.concatenate([grp, np.tile(nv[grp.shape[1]:], (len(rows), 1))], 1)
        ob = np.pad(np.asarray(PP.objk, float)[rows], ((0, 0), (0, len(nv) - PP.objk.shape[1])))
        h = self.c2_par["group_half"]
        out = acc_.copy()
        out[rows] = _uclip((1 - h) * nv[None, :] + h * grp - ob, 0, 1)
        return out

    # ---- the person's role and acceptance with the world on (N1b, outer world round 3)
    def role_norms(self):
        PP, W = self.PP, self.W
        ap_ = self.acc_
        rs_ = 1 - ap_[:, self.NI["role crossing"]]
        at_ = ap_[:, self.NI["transition"]] * float(np.asarray(W.rights)[WM.RIGHTS.index("sexuality")])
        return rs_, at_

    # ---- the channels the engine reads (package §5), each 1 or 0 at an ordinary person in an ordinary modern world
    def climate(self):
        """How hostile the place and one's people are to being out (N,): 0 at or above modern Earth's start (acceptance
        of coming out .70 x the sexuality right .73 after the 80-year burn-in, seeds 1-8), up to 1 where neither holds.
        A faith's community is in the local norms already, so the engine adds no faith term with the world on."""
        a_ = self.acc_[:, self.NI["coming out"]] * float(np.asarray(self.W.rights)[WM.RIGHTS.index("sexuality")])
        return _uclip((CLIM_REF - a_) / CLIM_REF, 0, 1)

    def channel_rates(self):
        """Per person and moment (N, S): a close person's divorce or quitting makes one's own likelier for a while
        (contagion, spec 2 §3), and the wish to move (move_wish, spec 3 §2.6: after a partnership starts or ends, where
        work is scarce) scales the moving moments against an ordinary person of that age."""
        PP = self.PP; r = np.ones((self.N, self.S))
        ct = getattr(PP, "contagion", None) or {}
        if self.div_s.any() and "divorce" in ct:
            r[:, self.div_s] *= np.asarray(ct["divorce"], float)[:, None]
        if self.quit_s.any() and "quit" in ct:
            r[:, self.quit_s] *= np.asarray(ct["quit"], float)[:, None]
        if self.move_s.any():
            ma_ = PP.P["move_age"]
            base = np.interp(PP._age(PP.t), [a_ for a_, _ in ma_], [r_ for _, r_ in ma_]) / 52.0
            mw_ = np.broadcast_to(np.asarray(PP.move_wish(), float), (self.N,))
            r[:, self.move_s] *= _uclip(mw_ / max(float(base), 1e-9), 0.5, 3.0)[:, None]
        return r

    def reach_pull(self, s):
        """(N, K) pull toward voice and subvert at institutions and the outer rings by felt reach (spec 7 §6): what makes
        a character vote, petition or organise. Zero at a felt reach of 0.75 (one of many who still count)."""
        lv = self.lev_i[s]; dm = self.dom_i[s]
        on = _isin_small(lv, [WK.LEVERS.index("voice"), WK.LEVERS.index("subvert")]) & (dm >= 0)
        if not on.any():
            return 0.0
        ring = np.where(dm >= 0, PM.RING_OF[np.maximum(dm, 0)], 0)
        on &= ring >= 2
        fr = np.take_along_axis(np.asarray(self.PP.felt_reach, float), ring.astype(np.intp), 1)
        return np.where(on, REACH_K * (fr / 3.0 - 0.25), 0.0)

    def odds(self, s):
        """(N, K) added to the options' difficulty (DIFF units; the engine's gain 3 turns .1 into about a third of an
        odds ratio): finding a job by the local unemployment (matching elasticity .5), a place in education by the
        local university's capacity and its openness to the person's class, an illness's acts by the hospitals'
        capacity there. 0 at the burn-in's typical world."""
        d = np.zeros((self.N, self.job_o.shape[1]))
        for v_ in self.odds_parts(s).values():
            d += v_
        return d

    def odds_parts(self, s):
        """odds() by cause, {"unemployment", "university places", "hospital places": (N, K)}, only those that apply."""
        W, PP = self.W, self.PP; N = self.N
        out = {}
        jo, ao = self.job_o[s], self.adm_o[s]
        if jo.any():
            ul = np.asarray(getattr(W, "loc_unemp", np.full(PP.n_loc, U_REF)), float)[PP.loc]
            out["unemployment"] = jo * _uclip(0.5 * np.log(np.maximum(ul, 0.5) / U_REF) / 3.0, -0.15, 0.25)[:, None]
        if ao.any() or self.ill_s[s].any():
            cap = np.asarray(W.inst_capacity, float); kd = np.asarray(W.inst_kind); il = np.asarray(W.inst_loc)
            def local(kind, v):   # the mean over that kind's institutions in each person's town, else the country's
                m_ = kd == WK.INST_KINDS.index(kind)
                if not m_.any():
                    return np.ones(N)
                tot = np.bincount(il[m_].astype(np.intp), weights=v[m_], minlength=PP.n_loc)
                cnt = np.bincount(il[m_].astype(np.intp), minlength=PP.n_loc)
                return np.where(cnt[PP.loc] > 0, tot[PP.loc] / np.maximum(cnt[PP.loc], 1), v[m_].mean())
            if ao.any():
                oc = np.asarray(W.inst_open_cls, float)[:, _uclip(PP.cls, 0, 2)]   # n_inst, N: openness to each one's class
                uni = kd == WK.INST_KINDS.index("university")
                op_ = oc[uni].mean(0) if uni.any() else np.full(N, OPEN_REF)
                f_ = local("university", cap) / CAP_REF * op_ / OPEN_REF
                out["university places"] = ao * _uclip(-np.log(np.maximum(f_, 0.1)) / 3.0, -0.15, 0.2)[:, None]
            if self.ill_s[s].any():
                f_ = local("hospital", cap) / CAP_REF
                out["hospital places"] = self.ill_s[s][:, None] * _uclip(-0.5 * np.log(np.maximum(f_, 0.1)) / 3.0, -0.1, 0.2)[:, None]
        if jo.any() and getattr(PP, "eyes_on", False):   # S3: a name opens or closes doors through a place's go-betweens:
            # finding work is easier by door x the mean name at their places with a go-between (or where they are one)
            gb_ = (PP._eyes_gobs(np.arange(N)) >= 0) | PP.eyes_gob
            hv_ = gb_ & (PP.eyes_key >= 0)
            dr_ = (PP.eyes_rep * hv_).sum(1) / np.maximum(hv_.sum(1), 1)
            out["go-betweens"] = jo * (-PP.eyes_par["door"] * dr_)[:, None]
        return out
