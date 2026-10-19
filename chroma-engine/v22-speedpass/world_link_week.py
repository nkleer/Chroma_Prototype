"""WorldLink's methods for what each week brings: congregations, sacred lines, offices and laws, disasters and deaths
for the story, the act's pushes resolved, far ties, eyes, ways to lead, seen it done. Part of class WorldLink
(world_link.py), which inherits LinkWeekMixin; moved out of world_link.py verbatim. A method here reads module names
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
from world_link_base import _uclip  # noqa: F401


class LinkWeekMixin:
    def _members(self, si, ref=None):
        """C2: the lives in a setting of moment si's group kind (and, given ref, one tied to that faith or body) (N,)."""
        PP = self.PP; m_ = PP.skind == int(self.group[si])
        if ref is not None:
            m_ &= PP.sref == ref
        return m_.any(1)

    def _c2_cong(self):
        """C2: each life's main congregation (N,; -1 none): its setting of that kind with the most time."""
        PP = self.PP; cg_ = PP.skind == PM.G["congregation"]
        j_ = np.argmax(np.where(cg_, PP.sts + 1.0, 0.0), 1)
        return np.where(cg_.any(1), j_, -1)

    def _c2_drift_q(self):
        """C2: a congregation whose ways have drifted far from its faith body's (total variation above drift_tv) splits:
        when a life's congregation first crosses it, the split comes to them with drift_share (once a crossing)."""
        PP, W = self.PP, self.W
        j_ = self._c2_cong(); has = j_ >= 0
        if not has.any() or not getattr(PP, "n_faith", 0):
            self.c2_drift = np.zeros(self.N, bool)
            return
        fp = np.asarray(W.faith_profile, float); fp = fp / np.maximum(fp.sum(1, keepdims=True), 1e-12)
        n_ = np.nonzero(has)[0]; jj = j_[n_]
        rf = np.clip(PP.sref[n_, jj], 0, len(fp) - 1)
        tv = 0.5 * np.abs(PP.snorm[n_, jj] - fp[rf]).sum(1)
        over = np.zeros(self.N, bool); over[n_] = tv > self.c2_par["drift_tv"]
        new_ = over & ~self.c2_drift if self.c2_drift is not None else np.zeros(self.N, bool)
        self.c2_drift = over
        if new_.any():
            hit_ = new_ & (PP.rng.random(self.N) < self.c2_par["drift_share"])
            if hit_.any():
                self.fire_now[hit_, self.c2_split] = True
                self.fire_why[self.c2_split] = dict(domain="group", kind="congregation drifts", key="congregation",
                                                    value=None, t=int(W.t))

    def _sac_keys(self):
        import sphere_data as SD_
        return SD_.OFFER["events"]

    def _sac_pick(self, n, it):
        """S5: the moment for an offer, tragic trade-off or amends waiting for life n: of its kind (cast_want), for the
        line it touches (sacred:; a tragic one for both, either order), then the offer's kind (offer:) and round
        (round:), each dropped in turn when none fits; None when no moment is for that line. A tragic offer with no
        moment for the pair comes as a plain offer on its first line."""
        PP = self.PP
        kinds = [int(PP.sac_line[n, j]) for j in it["slots"]]
        ss = self.want_s.get(it["kind"]) or []
        if it["kind"] == "tragic":
            c_ = [si for si in ss if set(self.sac_m[si].tolist()) == set(kinds)]
            if c_:
                si = c_[int(PP._sac_rng.integers(len(c_)))]
                m0_ = int(self.sac_m[si, 0])
                it["ab"] = [j for j in it["slots"] if int(PP.sac_line[n, j]) == m0_] + \
                           [j for j in it["slots"] if int(PP.sac_line[n, j]) != m0_]
                return si
            it.update(kind="sacred", slots=it["slots"][:1], round=0, size=1.0, tragic_none=True)
            kinds = kinds[:1]; ss = self.want_s.get("sacred") or []
        c_ = [si for si in ss if self.sac_m[si, 0] in (-1, kinds[0]) and self.sac_m[si, 1] < 0]
        if not c_:
            PP._sac_count("no moment")
            return None
        if it["kind"] == "sacred":
            import sphere_data as SD_
            ok_ = WK.OFFER_KINDS.index(SD_.OFFER["events"][it["key"]]["kind"])
            for f_ in (lambda si: self.sac_m[si, 0] == kinds[0] and self.sac_off[si] == ok_ and self.sac_rnd[si] == it["round"],
                       lambda si: self.sac_m[si, 0] == kinds[0] and self.sac_off[si] == ok_,
                       lambda si: self.sac_m[si, 0] == kinds[0] and self.sac_rnd[si] in (-1, it["round"]),
                       lambda si: self.sac_m[si, 0] == kinds[0]):
                d_ = [si for si in c_ if f_(si)]
                if d_:
                    c_ = d_
                    break
        else:
            d_ = [si for si in c_ if self.sac_m[si, 0] == kinds[0]]
            c_ = d_ or c_
        return c_[int(PP._sac_rng.integers(len(c_)))]

    def sacred_info(self, n, si):
        """S5: for a sacred, tragic or amends moment brought this week, the line or lines (kind and colour), the offer (the
        Outer world's words: the {offer} slot; its kind and gesture), the round, its size and the refusal odds
        (People.sac_info); None for any other moment."""
        it_ = self.sac_pend.get(int(n)); pv_ = self.pending.get(int(n))
        if it_ is None or pv_ is None or pv_[2] != int(si):
            return None
        return self.PP.sac_info(int(n), it_)

    def sacred_tilt(self, s, pr, mask=None):
        """S5: the character's own pick at an offer on a held line: the options that cross it (line: cross) share 1 - the
        refusal odds, all others (holding, untagged, doing nothing) the rest; at a tragic trade-off a, b and torn share
        sacred_par tragic_w (untagged options keep their own odds). Within a group, by the character's own odds; a group
        none of whose options they noticed (all at 0) still gets its share, evenly over its options the moment offers
        (mask): saying no, or giving in, needs no noticing. pr (N, K) is changed in place for those lives."""
        PP = self.PP
        for n_, it_ in self.sac_pend.items():
            si = self.pending.get(n_, (0, 0, -1))[2]
            if si != int(s[n_]):
                continue
            p_ = pr[n_]; mk_ = np.ones(len(p_), bool) if mask is None else np.asarray(mask[n_], bool)

            def share(g_):   # the group's own odds, or evenly over its options when none was noticed
                return p_ * g_ / p_[g_].sum() if p_[g_].sum() > 0 else g_ / g_.sum()
            if it_["kind"] == "sacred":
                x_ = (self.sac_line[si] == 1) & mk_
                h_ = ~x_ & mk_
                if x_.any() and h_.any():
                    q_ = PP.sac_odds(it_)
                    pr[n_] = (1 - q_) * share(x_) + q_ * share(h_)
                    PP._sac_count("tilted")
            elif it_["kind"] == "tragic":
                tg_ = self.sac_trag[si]; tw_ = PP.sac_par["tragic_w"]
                grp_ = [((tg_ == g_) & mk_, tw_[g_]) for g_ in range(3)]
                tot_ = sum(w_ for m_, w_ in grp_ if m_.any()); ptag_ = p_[(tg_ >= 0) & mk_].sum()
                ut_ = (tg_ < 0) & mk_
                ptag_ = ptag_ if ptag_ > 0 or ut_.any() and p_[ut_].sum() > 0 else 1.0
                if tot_ > 0:
                    q_ = np.where(ut_, p_, 0.0)
                    for m_, w_ in grp_:
                        if m_.any():
                            q_ = q_ + ptag_ * (w_ / tot_) * share(m_)
                    pr[n_] = q_ / q_.sum()
                    PP._sac_count("tilted")
        return pr

    def sacred_act(self, live, ma, cost):
        """S5, after the act and its costs: acts that cost something real count toward a line in their colour and heal a
        wound in it (People.sac_act). Returns the healing events."""
        idx = np.nonzero(live)[0]
        return self.PP.sac_act(idx, ma[idx], np.asarray(cost)[idx]) if len(idx) else []

    def _staff(self, i):
        """The lives whose own work setting is institution i (N,)."""
        PP = self.PP
        return ((PP.skind == PM.G["work"]) & (PP.sref == i)).any(1)

    def _c3_merged(self, new):
        """C3 merged: the folded firm's staff, lives and cast alike, now work at the bigger one (its slot became a new
        firm), and a quarter of the lives among them face the job-loss rate x3 for a quarter."""
        PP, W = self.PP, self.W
        for e in new:
            if e.get("domain") != "institution" or e.get("kind") != "merged":
                continue
            v = e.get("value") or {}; a, b = int(v.get("inst", -1)), int(v.get("into", -1))
            if a < 0 or b < 0:
                continue
            moved = self._staff(a)
            wk = (PP.skind == PM.G["work"]) & (PP.sref == a)
            PP.sref[wk] = b
            PP.inst[PP.inst == a] = b
            if moved.any():
                if getattr(PP, "c3_jl", None) is None:     # made on the first merger (a world with C3 off saves none)
                    PP.c3_jl = np.zeros(self.N, np.int64)
                hit = moved & (PP.rng.random(self.N) < W._c_par("merge_share"))
                PP.c3_jl = np.where(hit, int(W.t) + 13, PP.c3_jl)

    def drain(self):
        """The cast events since the last call (n, kind, ...), each handed over once: the birth's before the first week,
        the week's own, and those of the act (pushes, wants met or refused)."""
        out = self._carry + list(self.PP.events[self._pp_i:])
        self._carry = []; self._pp_i = len(self.PP.events)
        return out

    def disasters(self):
        """Since the last call: the severity of a disaster in each person's own town (0 none), and whether one struck a
        close person's town (layers 1 and 2). The engine brings the disaster's outside event on these (spec 5 §2)."""
        own, near = self.dis_own.copy(), self.dis_near.copy()
        self.dis_own[:] = 0; self.dis_near[:] = False
        self.dis_haz_now, self.dis_rec_now, self.dis_nhaz_now = self.dis_haz, self.dis_rec, self.dis_nhaz   # this call's,
        self.dis_haz = [None] * self.N; self.dis_rec = [None] * self.N; self.dis_nhaz = [None] * self.N   # for the story
        return own, near

    def story(self, ns, dead):
        """This week's public events for each logged life {n: [entries]}: big ones always, the rest only when they touch
        the character (self=True: their town's disaster, crime wave or election, their own workplace, school or unit)
        or their people (touches=[cast ids] in layers 1 and 2: where they live or work) (Emren 10:42; hooks §2.3)."""
        PP = self.PP; out = {}
        if not self.week_events:
            return out
        INSTK = [WK.GROUP_KINDS.index(g_) for g_ in ("work", "class", "unit", "ward")]
        for n in ns:
            if dead[n]:
                continue
            ks = np.nonzero(PP.used[n] & PP.lv[n] & (PP.c[n] >= self.layer2))[0]
            mine = set(int(x_) for x_ in PP.sref[n][np.isin(PP.skind[n], INSTK) & (PP.sref[n] >= 0)])
            lst = []
            for e in self.week_events:
                v = e.get("value") if isinstance(e.get("value"), dict) else {}
                me, tch = (bool(e.get("self")) and e.get("by_life") == n) or v.get("life") == n, []
                if "inst" in v and e.get("domain") == "institution" and e.get("kind") != "new firm":   # (a new firm
                    i_ = int(v["inst"]); me = me or i_ in mine                     # can reuse a closed one's id)
                    tch = [int(PP.uid[n, k]) for k in ks if int(PP.inst[n, k]) == i_]
                elif "loc" in v and e.get("kind") in LOCAL_SEEN:
                    l_ = int(v["loc"]); me = me or int(PP.loc[n]) == l_
                    if e.get("kind") != "local election":
                        tch = [int(PP.uid[n, k]) for k in ks if int(PP.mloc[n, k]) == l_]
                if e.get("big") or me or tch:
                    lst.append(dict(e, self=me, touches=tch))
            if lst:
                out[n] = lst
        return out

    def _office(self, t, S_):
        W = self.W; self.office_lost = np.zeros(self.N, bool)
        go_ = S_.get("gov_office"); hg_ = S_.get("head_gov")
        self.gov_office = np.zeros(self.N, bool) if go_ is None else np.asarray(go_, bool).copy()
        if hg_ is None:
            return
        hg_ = np.asarray(hg_, bool)
        if self.self_head is not None and not hg_[self.self_head]:
            W._event("state", "head of government", "left office", dict(life=int(self.self_head)), big=True)
            self.self_head = None
        if self.self_head is None and hg_.any():
            self.self_head = int(np.argmax(hg_))
            W._event("state", "head of government", "self", dict(life=self.self_head, party=int(W.gov_party)), big=True)
        if self.self_head is not None and t % 13 == 0:   # the leader's own colors pull the government's
            g_ = np.asarray(W.G, float) + self.self_lead * (np.asarray(S_["w"], float)[self.self_head] - W.G)
            W.G = g_ / g_.sum()

    def law_due(self):
        """The law the norms (and the government's fit) already point away from its state: (key, sign) or None; sign +1
        moves it toward legal, -1 toward banned. A minister passes what the norms support (spec 4, world.push)."""
        W = self.W; p = W.p; NL = len(WK.LAW_KEYS)
        n_ = WM._sig(np.asarray(W.norm_x[:NL], float))
        neff = n_ + p["law_fit"] * ((np.asarray(W.G) - 0.2) @ np.asarray(W.NPROF)[:NL].T)
        tgt = np.where(neff > p["law_cut"][1], 0, np.where(neff > p["law_cut"][0], 1, 2))
        laws = np.asarray(W.laws)
        gap = np.where(tgt != laws, np.minimum(np.abs(neff - p["law_cut"][0]), np.abs(neff - p["law_cut"][1])), -1.0)
        if gap.max() < 0:
            return None
        k = int(np.argmax(gap))
        return WK.LAW_KEYS[k], (1 if tgt[k] < laws[k] else -1)

    def deaths(self):
        """This week's deaths in each person's cast by the engine's roles (N, 5): the engine lives the moment."""
        return np.asarray(self.PP.died)

    def resolve(self, n, s_n, a_n, succ_n, idle_n):
        """After the act: a want the moment answered (met or refused) moves trust and closeness."""
        pv_ = self.pending.get(int(n))
        if pv_ is None or pv_[2] != int(s_n):
            return None
        if pv_[1] in ("caught", "odd"):   # S3, S4: the option's tag decides (none, or doing nothing: kept apart, held on)
            tg_ = (self.caught if pv_[1] == "caught" else self.odd)[s_n, a_n] if a_n < self.caught.shape[1] else -1
            return self.PP.eyes_resolve(int(n), pv_[1], int(tg_), succ=bool(succ_n), idle=bool(idle_n))
        if self.lw and pv_[1].startswith("lead_"):   # S7: the post's moment answered (no holder)
            pid_ = self.lw_fire.get(int(n))
            if pid_ is None:
                return None
            return self.PP.lead_resolve(int(n), pid_, pv_[1], self.olead[s_n, a_n], self.ofall[s_n, a_n], self.ohand[s_n, a_n],
                                        bool(succ_n), bool(idle_n))
        if pv_[1] in WK.PLACE_WANTS:   # part 2: a place moment is the life's own (nothing to meet or refuse)
            return None
        if pv_[1] in WK.OWN_WANTS:   # S5: an offer, a tragic trade-off or amends (no cast member holds it)
            it_ = self.sac_pend.get(int(n))
            if it_ is None:
                return None
            tab_ = {"sacred": self.sac_line, "tragic": self.sac_trag, "amends": self.sac_heal}[it_["kind"]]
            tg_ = -1 if idle_n else int(tab_[s_n, a_n])
            return self.PP.sac_resolve(int(n), it_, tg_, bool(idle_n), None)
        ev_ = self.PP.resolve_want(int(n), pv_[0], pv_[1], bool(self.meets[s_n, a_n]) and not idle_n, succ=bool(succ_n))
        if pv_[1].startswith("far_") and self.took[s_n, a_n] and not idle_n and succ_n:   # F4: the tie comes to stay
            self.PP.take_in(int(n), pv_[0])
        return ev_

    def _far_pick(self, n, cid, ss):
        """far_ties: the far moments that fit the call: by what the event touched (touch:) and by the tie's relation
        (the moment's first who: slot), each dropped in turn when none fits."""
        PP = self.PP
        tch = set((PP.far_info(n, cid) or {}).get("touch") or ())
        k_ = PP._slot(n, cid)
        rel = set(PP.far_rel(n, k_)) if k_ >= 0 else set()
        who_ = self.L.get("W_WHO", [[]] * self.S)
        t_ok = lambda si: self.touch[si] < 0 or WK.TOUCHES[int(self.touch[si])] in tch
        r_ok = lambda si: bool(who_[si]) and who_[si][0] in rel
        for f_ in (lambda si: t_ok(si) and r_ok(si), t_ok, r_ok):
            c_ = [si for si in ss if f_(si)]
            if c_:
                return c_
        return ss

    def far_info(self, n, si):
        """far_ties: for a far moment offered this week, the tie's town and what happened there (People.far_info)."""
        pv_ = self.pending.get(int(n))
        if pv_ is None or pv_[2] != int(si) or not pv_[1].startswith("far_"):
            return None
        return self.PP.far_info(int(n), pv_[0])

    def eyes_info(self, n, si):
        """S3, S4: for a caught-between or odd-one-out moment offered this week, its slots ({place_a}, {place_b} and the
        opposed pair; or {place}) as People.eyes_moment gives them; None otherwise."""
        pv_ = self.pending.get(int(n))
        if pv_ is None or pv_[2] != int(si) or pv_[1] not in ("caught", "odd"):
            return None
        return self.PP.eyes_moment(int(n))

    def eyes_pull(self, s):
        """(N, K) log odds (S4, sph_odd): on an odd-one-out moment an unplayed life holds on more, and blends in less, the
        stronger its own lead colour and the higher its rung at the place (People.odd_hold_x). 0 elsewhere."""
        PP = self.PP
        od = self.odd[s]
        if not getattr(PP, "odd_on", False) or not (od >= 0).any():
            return 0.0
        u = np.zeros(od.shape)
        for n_, pv_ in self.pending.items():
            if pv_[1] == "odd" and pv_[2] == s[n_]:
                x_ = PP.odd_hold_x(n_)
                u[n_] = np.where(od[n_] == WK.ODD_TAGS.index("hold"), x_, np.where(od[n_] == WK.ODD_TAGS.index("blend"), -x_, 0.0))
        return u

    def lead_info(self, n, si=None):
        """S7: life n's posts (People.lead_info: kind, sphere, the led place, way, legitimacy, start, end and its reason,
        falls); with si, only the post whose moment si is this week (its {place}), else None."""
        if not self.lw:
            return None
        info = self.PP.lead_info(int(n))
        if si is None:
            return info
        pv_ = self.pending.get(int(n))
        if pv_ is None or pv_[2] != int(si) or not pv_[1].startswith("lead_"):
            return None
        pid_ = self.lw_fire.get(int(n))
        return next((dict(p_, moment=pv_[1]) for p_ in info if p_["id"] == pid_), None)

    def seen_felt(self, p_hat, s, m, opt, offered):
        """seen_done (S6): felt odds with what each life has seen walked (never the real odds): the option's path (its
        title, People.sd_lt) plus its colour way (its ways x People.sd_lc), on every option but doing nothing (opt),
        kept within .01 and .99 (odds already beyond them stay as they were). offered: the options open to them this week, for the colour-even check (sd_stat)."""
        PP = self.PP; tk = self.sd_tk[s]
        lt = np.take_along_axis(PP.sd_lt, np.maximum(tk, 0), 1) * (tk >= 0) if PP.sd_nt else np.zeros(tk.shape)
        lf = lt + np.einsum("nkc,nc->nk", m, PP.sd_lc)
        of_ = offered & opt
        self.sd_stat[0] += np.einsum("nk,nkc->c", lf * of_, m); self.sd_stat[1] += np.einsum("nk,nkc->c", of_.astype(float), m)
        self.sd_n += (of_.sum(), (of_ & (tk >= 0)).sum(), (lt * of_).sum(), (lf * of_).sum())
        return np.where(opt, _uclip(p_hat + lf, np.minimum(p_hat, 0.01), np.maximum(p_hat, 0.99)), p_hat)

    def seen_info(self, n, si):
        """seen_done, for the game's option row: per option of moment si, the strongest model on its path (People.
        seen_model) or, on no path, on its leading colour way (People.seen_way): kind (the Library's earth_spheres.SEEN
        word: seen, wrong, far, none), who (the model's cast id; absent for none), path or way, exposure, failures seen,
        lift; None for an option with no ways (doing nothing)."""
        if not self.seen_on:
            return None
        si = int(si); nk = len(self.L["labels"][si]); tk = self.sd_tk[si][:nk]; M_ = np.asarray(self.L["M"][si])[:nk]
        return [self.PP.seen_model(int(n), int(x_)) if x_ >= 0 else
                self.PP.seen_way(int(n), int(np.argmax(M_[k_]))) if M_[k_].sum() > 0 else None
                for k_, x_ in enumerate(tk.tolist())]

    def seen_report(self):
        """seen_done's numbers for the refit: the mean felt-odds lift on offered options per colour way (each option
        weighted by its ways), and the share of offered options on a path with their mean path lift."""
        if not self.seen_on:
            return None
        n_ = self.sd_n
        return dict(lift_by_colour=(self.sd_stat[0] / np.maximum(self.sd_stat[1], 1e-9)).round(4).tolist(),
                    offered=int(n_[0]), on_path=int(n_[1]), path_lift=round(float(n_[2] / max(n_[1], 1)), 4),
                    mean_lift=round(float(n_[3] / max(n_[0], 1)), 4))
