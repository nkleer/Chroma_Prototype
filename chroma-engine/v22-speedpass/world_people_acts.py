"""People's methods for acts, levers and pushes, body_trust, and the finishing pack's place_turnover.

Part of class People (world_people.py), which inherits ActsMixin; moved out of world_people.py verbatim. A method here
reads module names through the imports below, the same objects world_people.py has, and self for everything on the
People."""
import numpy as np
from library import COLORS
from world_keys import DOMAINS, GROUP_KINDS, HAUNT_KINDS, INST_KINDS, LADDER, LEVERS, SPHERES
from world_people_base import (BIT, BT_FIRST, BT_INST_J, C, DI, FAIR_PART_NAMES, FR_HABIT, G, HAUNT_SPH, LI, RING_OF,
    RUNG_MULT, _NKI, _csum, _ix, _norm, _uclip)


class ActsMixin:
    # ------------------------------------------------------------------ acts, levers and pushes (spec 2 §3, spec 7 §3)
    def on_act(self, idx, ma, succ, visibility=None, lever=None, pushes=None, base=None, target=None, norm=None,
               var=None, t=None, sphere=None, office=None):
        """The character's act this week (vectorised over idx): the close circle judges it (overlap of the act's mix
        with their pies), rank in groups moves, and acts with a lever push (size = base x reach x how well it went;
        a failed push can backfire). Returns dict(approval=(n,), results=[push results])."""
        t = self.t if t is None else t; P = self.P; rng = self.rng; L1, L2, L3, L4 = P["layer_c"]
        idx = np.atleast_1d(np.asarray(idx, np.int64)); E = len(idx)
        if not E:
            return dict(approval=np.zeros(0), results=[])
        ma = _norm(np.asarray(ma, float).reshape(E, C))
        q = _uclip(np.broadcast_to(np.asarray(succ, float), (E,)), 0, 1)
        vis = np.broadcast_to(np.asarray(0.5 if visibility is None else visibility, float), (E,))
        def as_idx(v_, tab):
            if v_ is None:
                return np.full(E, -1, np.int64)
            if isinstance(v_, np.ndarray) and v_.dtype.kind in "iu":
                return np.broadcast_to(v_.astype(np.int64), (E,))
            return np.array([(-1 if x_ is None else tab[x_] if isinstance(x_, str) else int(x_))
                             for x_ in np.broadcast_to(np.asarray(v_, dtype=object), (E,))], np.int64)
        lev = as_idx(lever, LI); dom = as_idx(pushes, DI); nk = as_idx(norm, _NKI)
        bas = np.broadcast_to(np.asarray(1.0 if base is None else base, float), (E,))
        tg = np.broadcast_to(np.asarray(-1 if target is None else target, dtype=object), (E,))
        # 1. the close circle judges what it sees
        ix = slice(None) if E == self.N and (idx == np.arange(E)).all() else idx   # (views when every life acts)
        fi = self._fi[ix]
        if getattr(self, "_cok", None) is not None and self._last_w == t:
            ok = self._cok[ix]; c = self._cc[ix]
        else:
            ok = np.take(self.used, fi) & np.take(self.lv, fi) & (np.take(self.uid, fi) == self._cuid[ix]); c = np.take(self.c, fi)
        f32 = np.float32
        off = np.where(c >= L1, f32(0.0), np.where(c >= L2, f32(0.3), f32(1.0)))
        obs = np.minimum(np.maximum((2 * vis[:, None]).astype(f32) - off, f32(0)), f32(1)) * ok
        ft = C * np.matmul(self._cpie[ix], ma[:, :, None])[..., 0] - 1.0
        wt = obs * c
        appr = (wt * ft).sum(1) / np.maximum(wt.sum(1), 1e-9)
        tr = np.take(self.trust, fi); tr0_ = tr.copy() if self.wa_l else None
        tr += f32(0.01) * obs * np.minimum(np.maximum(ft, -1.0), 1.0).astype(f32)
        np.minimum(np.maximum(tr, f32(0), out=tr), f32(1), out=tr); np.put(self.trust, fi, tr)
        if self.wa_l:   # the world answers, D: the trust the act moved in those who saw it
            self._wa_pflat(fi, t, dtr=tr - tr0_)
        strong = (ft < -0.6) & (obs > 0) & (c >= L2)
        hasn = nk >= 0
        if hasn.any():
            add = (strong * c ** 2 * 0.5).sum(1)
            np.add.at(self.objk, (_ix(idx[hasn]), _ix(nk[hasn])), add[hasn])
            np.clip(self.objk, 0, 1, out=self.objk)
        # 2. rank in groups: acts that fit the group's ways better than its members do (and work) raise it
        sk = self.skind[ix] >= 0
        fs = C * np.matmul(self.snorm[ix], ma[:, :, None])[..., 0] - 1.0
        vs = _uclip(2 * vis, 0, 1)[:, None] * sk * np.minimum(1, self.sts[ix] * 4)
        d_ = fs - self._fitm[ix]
        dr = P["rank_k"] * vs * np.where(d_ > 0, q[:, None] * d_, d_)
        self.srank[ix] = _uclip(self.srank[ix] + dr, 0, 1)
        # 3. levers
        res = []
        for e_ in np.nonzero((lev >= 0) & (dom >= 0) & ~self.dead[idx])[0]:
            res.append(self._push(int(idx[e_]), ma[e_], float(q[e_]), int(lev[e_]), int(dom[e_]), float(bas[e_]),
                                  tg[e_], None if var is None else (var[e_] if isinstance(var, (list, tuple, np.ndarray)) else var), t))
        # 4. spheres phase 4: the lever on the person's place or town sphere (sph_levers), the act kept for felt fairness
        if (getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False)) and sphere is not None:
            js = np.broadcast_to(np.asarray(sphere, np.int64), (E,))
            ok_ = np.broadcast_to(np.asarray(2 if office is None else office, np.int64), (E,))
            for e_ in np.nonzero((lev >= 0) & (js >= 0) & ~self.dead[idx])[0]:
                r_ = self._sph_lever(int(idx[e_]), int(js[e_]), int(lev[e_]), ma[e_], float(q[e_]), int(ok_[e_]), int(dom[e_]), t)
                if r_ is not None:
                    res.append(r_)
        if self.wa_g:   # the world answers, A: a good voice, found or lead act grows the setting it was made in
            self._wa_grow(idx, lev, q, None if sphere is None else np.broadcast_to(np.asarray(sphere, np.int64), (E,)), t)
        return dict(approval=appr, results=res)

    def _sph_lever(self, n, j, lev, ma, q, office, dom, t):
        """Phase 4: life n's lever lev in sphere j (Outer world's phase 4 answers). size = the reach for the act's ring
        (dreach, 0 to 3) / 3 x the rung's multiplier (newcomer .125 .. leader 2) x how well it went. It lands on their
        haunt in that sphere; else, working in that sphere (no named work place), on the town sphere at half the size;
        else on the town sphere at a quarter. A voice or loyalty act is kept for felt fairness (+1 went well, -1 not)."""
        lv = LEVERS[lev]
        if self.sph_fr and lv in ("voice", "loyalty"):
            self.fair_log.append([int(t), int(n), int(j), 1 if q >= 0.5 else -1])
        if not self.sph_lv:
            return None
        W = self.W
        rg = int(np.floor(self.rung[n, j])) if hasattr(self, "rung") else 0
        place = -1
        if getattr(self, "sph_h", False) and getattr(W, "hp_s", None) is not None:
            P_ = W.hp_s.shape[2]
            for p_ in self.hnt[n]:
                if p_ >= 0 and HAUNT_SPH[(p_ // P_) % len(HAUNT_KINDS)] == j:
                    place = int(p_); break
        # the reach: on their own place, the settings' ring (a place is a setting's ring, 1); on the town's sphere, the
        # ring of the act's own domain (an institution's, without one)
        reach = float(self.dreach[n, DI["group"] if place >= 0 else (dom if dom >= 0 else DI["institution"])])
        size = reach / 3.0 * float(RUNG_MULT[min(max(rg, 0), 4)]) * q
        if place < 0:
            ss_ = self.set_sphere[n]
            size *= 0.5 if ((self.skind[n] == G["work"]) & (ss_ == j)).any() else 0.25
        span = None
        if self.lw:   # S7: a leader's act in the sphere they lead: the lead lever's size x (.5 + legitimacy), a fund act
            p_ = self._lead_post(n, j)   # lasts what is left of the post (not phase 4's fixed 80 quarters), and the act
            if p_ is not None:            # counts for the way's falls (a failed one, a favour, a success)
                if lv == "lead":
                    size *= 0.5 + p_["legit"]
                if rg >= 4:
                    span = self._lead_left(p_, t)
                self._lead_act(p_, lv, q, t)
        if self.wa_l:   # the world answers, D: what the lever moves in their town, its places and spheres
            hp0_ = W.hp_s[int(self.loc[n])].copy() if getattr(W, "hp_s", None) is not None else None
            ss0_ = W.sph_s[int(self.loc[n])].copy() if getattr(W, "sph_s", None) is not None else None
        what = W.sph_lever(int(self.loc[n]), j, place, lv, ma, size, rg, self.rng, office=("ban", "licence", "budget")[office],
                           span=span, went=q)
        if self.wa_l and ss0_ is not None:
            self._wa_lever(n, int(self.loc[n]), hp0_, ss0_, lv, rg, t)
        return dict(kind="sphere lever", n=int(n), t=int(t), lever=lv, sphere=SPHERES[j], place=place, size=round(size, 4), reach=reach, went=q,
                    rung=LADDER[min(max(rg, 0), 4)], moved=what)

    def _sph_year4(self, t):
        """Yearly (phase 4): the lives leading a sphere in their town (rung leader) join its leaders' mix (sph_levers;
        World.sph_plead, town x sphere x (colour sums, count)); each life's felt fairness moves .1 of the way toward
        its town's target (World.sph_fair_target) + .1 per voice or loyalty act there in the last 3 years that went
        well, - .1 per one that did not, + .05 x rung (sph_fair)."""
        a = int(self._age(t))
        if a == self._p4_yr:
            return
        self._p4_yr = a; W = self.W; N = self.N
        live = ~self.dead
        if self.sph_lv and hasattr(self, "rung") and not self.lw:   # (lead_ways: the posts join it, each quarter)
            pl = np.zeros((self.n_loc, 9, C + 1))
            n_, j_ = np.nonzero((np.floor(self.rung) >= 4) & live[:, None])
            np.add.at(pl, (self.loc[n_], j_), np.concatenate([self.w[n_], np.ones((len(n_), 1))], 1))
            W.sph_plead = pl if len(n_) else None
        if self.sph_fr and getattr(W, "sph_s", None) is not None:
            self.fair_log = [r_ for r_ in self.fair_log if t - r_[0] <= 3 * 52]
            acts = np.zeros((N, 9))
            for _, n_, j_, v_ in self.fair_log:
                acts[n_, j_] += v_
            rg = np.floor(self.rung) if hasattr(self, "rung") else 0.0
            if getattr(self, "fr_read", False):   # S1: each part of fairness read at the weight the life's colours give it
                base = 0.5 + np.einsum("nc,njc->nj", self._fair_w(), W.sph_fair_parts()[self.loc])
            else:
                base = W.sph_fair_target()[self.loc]
            tgt = _uclip(base + 0.1 * acts + 0.05 * rg, 0, 1)
            self.fair = np.where(live[:, None], self.fair + 0.1 * (tgt - self.fair), self.fair)

    def _fair_w(self):
        """S1 (fair_read): how much each life looks for each part of fairness (N x 5, W U B R G): its colours squared,
        shared to 1, so an even life weighs each part .2 and a strong colour's part leads."""
        c2 = np.asarray(self.w, float) ** 2
        return c2 / np.maximum(c2.sum(1, keepdims=True), 1e-12)

    def fair_info(self, n):
        """S1 (fair_read; read only, for the hover): per sphere, the life's felt fairness and the part of fairness that
        weighs on it most (the Library's names: rules, reasons, due, respect, goodwill; None when no part reads under
        .5), with each part's weighted step."""
        if not getattr(self, "fr_read", False):
            return {}
        W = self.W; R = W.sph_fair_parts()[self.loc[n]]; w = self._fair_w()[n]
        out = {}
        for j, sp in enumerate(SPHERES):
            x = w * R[j]; k = int(np.argmin(x))
            out[sp] = dict(fair=round(float(self.fair[n, j]), 3), weakest=FAIR_PART_NAMES[k] if x[k] < 0 else None,
                           parts={FAIR_PART_NAMES[c]: round(float(x[c]), 4) for c in range(5)})
        return out

    def _fair_week(self, t):
        """S1 (fair_read): each tagged sphere event fired since last week (World.fair_tags) moves felt fairness in the
        sphere it touches, for the lives of its town (the whole society's: everyone), by .05 x the weight of its parts
        (their mean), up on its fair side and down on its unfair one. A part heard of more often than the others in
        recent years is heeded less (habituation; Helson 1964, Frederick and Loewenstein 1999): each of an event's
        parts moves with chance (rarest part's recent count + 1) / (its own + 1), the counts (every tagged part an event
        carries, heeded or not) fading with a half-life of FR_HABIT years, so each part of fairness, and so each
        colour's eye, is stirred about as often as the others."""
        log = getattr(self.W, "sph_ev_log", None)
        if self._fr_n.any():
            self._fr_n *= 0.5 ** (1.0 / (52.0 * FR_HABIT))
        if log is None or len(log) <= self._fr_i:
            return
        rows = np.asarray(log[self._fr_i:]).tolist(); self._fr_i = len(log)
        tags = self.W.fair_tags()["events"]; live = ~self.dead; wn = None
        for _, i_, l_ in rows:
            mv = tags.get(int(i_))
            if not mv:
                continue
            nn = np.nonzero(live & ((self.loc == l_) if l_ >= 0 else True))[0]
            if not len(nn):
                continue
            if wn is None:
                wn = self._fair_w()
            for j, ps, sd in mv:
                ps_ = list(dict.fromkeys("WUBRG".index(p_) for p_ in ps))
                self._fr_n[ps_] += 1.0; m_ = self._fr_n.min() + 1.0
                ix = [k_ for k_ in ps_ if self.rng.random() < m_ / (self._fr_n[k_] + 1.0)]
                if not ix:
                    continue
                self.fr_cnt[ix] += 1.0
                self.fair[nn, j] = _uclip(self.fair[nn, j] + 0.05 * sd * wn[nn][:, ix].mean(1), 0, 1)

    # ------------------------------------------------------------------ body_trust: trust in a sphere's bodies
    def _bt_init(self):
        """body_trust (the spheres' finishing pack, part 3; sphere_data.TRUST): each life's trust in each sphere's bodies
        (btrust, N x 9 in SPHERES order, 0 to 1; NaN until it starts at 15), the known parents' mean a legacy child starts
        from (bt_par), the body kind of a life's own body job (bt_kind, set by the engine from the titles held), what has
        been read of the town events and the world's log, and its own random stream (the start's noise only), so no other
        draw moves."""
        import sphere_data as SD
        N = self.N; W = self.W; self.bt = SD.TRUST
        self.btrust = np.full((N, len(SPHERES)), np.nan); self.bt_par = np.full((N, len(SPHERES)), np.nan)
        self.bt_kind = np.full(N, -1, np.int64)
        self.bt_lean = np.zeros(N)   # each life's own lean of trust (TRUST lean: its spread, 0 none), drawn at the start
        self._bt_rng = np.random.default_rng([self.seed, 103, self.run_seed])
        lg_ = getattr(W, "sph_ev_log", None)
        self._bt_i = 0 if lg_ is None else len(lg_); self._bt_li = len(getattr(W, "log", ())); self._bt_yr = -1
        self.bt_cnt = dict.fromkeys(("fair", "unfair", "scandal", "leak", "cover-up", "good", "bad", "work"), 0)   # read only

    def bt_jump(self, n, j, d, why=None):
        """body_trust: lives n (an index or an index array) jump by d in sphere j, within floor and ceiling (the table's
        falls already weigh about 1.5 times its rises, Slovic 1993). A life whose trust has not started (under 15) or that has ended does not move."""
        J = self.bt["jumps"]; n = np.atleast_1d(np.asarray(n, np.int64))
        n = n[~np.isnan(self.btrust[n, j]) & ~self.dead[n]]
        if not len(n):
            return
        self.btrust[n, j] = _uclip(self.btrust[n, j] + d, J["floor"], J["ceiling"])
        if why is not None:
            self.bt_cnt[why] += len(n)

    def _bt_week(self, t):
        """body_trust, each week: the start at 15 (a child of a legacy line from its known parents' mean +- noise, a first
        life from .5 + .3 x (its town's sphere fairness - .5)); the tagged sphere events fired since last week in their
        town (the whole society's: everyone), event_fair or event_unfair in each sphere a tag touches (felt_fairness.
        five_parts.events), and a neglect scandal or a faith scandal its own jump in its sphere in place of its tags there;
        C3's leak (its town, a national body's: everyone) and cover-up (hidden: only its staff know, those working there or
        holding a body job of its kind in its town) in the body's sphere."""
        import sphere_data as SD
        J = self.bt["jumps"]; W = self.W; N = self.N
        if self._age(t) >= 15:
            new = np.nonzero(np.isnan(self.btrust[:, 0]) & ~self.dead)[0]
            if len(new):
                st = BT_FIRST[0] + BT_FIRST[1] * (np.asarray(W.sph_fair_target(), float)[self.loc[new]] - 0.5)
                kp = ~np.isnan(self.bt_par[new, 0])
                if kp.any():
                    st[kp] = self.bt_par[new[kp]] + self._bt_rng.uniform(-self.bt["noise"], self.bt["noise"], (int(kp.sum()), st.shape[1]))
                if self.bt.get("lean"):   # v22.6 refit: people differ in how far they trust bodies at all, for life
                    self.bt_lean[new] = self._bt_rng.normal(0.0, self.bt["lean"], len(new))
                    st = st + self.bt_lean[new][:, None]
                self.btrust[new] = _uclip(st, J["floor"], J["ceiling"])
        lg_ = getattr(W, "sph_ev_log", None)
        if lg_ is not None:
            self._bt_i = min(self._bt_i, len(lg_))
            if len(lg_) > self._bt_i:
                rows = np.asarray(lg_[self._bt_i:]).tolist(); self._bt_i = len(lg_)
                tags = W.fair_tags()["events"]
                for _, i_, l_ in rows:
                    ev_ = SD.EV[int(i_)]; sc_ = J.get(f"{ev_['sphere']}.{ev_['key']}")
                    sds = {}
                    for j_, _, sd_ in tags.get(int(i_), ()):
                        sds.setdefault(int(j_), set()).add(int(sd_))
                    if sc_ is None and not sds:
                        continue
                    nn = np.nonzero(self.loc == l_)[0] if l_ >= 0 else np.arange(N)
                    if sc_ is not None:
                        jsc_ = SPHERES.index(ev_["sphere"]); sds[jsc_] = ()
                        self.bt_jump(nn, jsc_, sc_, "scandal")
                    for j_, ss_ in sds.items():
                        for sd_ in sorted(ss_):
                            self.bt_jump(nn, j_, J["event_fair"] if sd_ > 0 else J["event_unfair"], "fair" if sd_ > 0 else "unfair")
        log = getattr(W, "log", None)
        if log is not None:
            self._bt_li = min(self._bt_li, len(log))
            for e in log[self._bt_li:]:
                if e.get("domain") != "institution" or e.get("kind") not in ("leak", "cover-up") or e.get("key") not in INST_KINDS:
                    continue
                kd_ = INST_KINDS.index(e["key"]); j_ = int(BT_INST_J[kd_]); v_ = e.get("value") or {}
                if j_ < 0:
                    continue
                l_ = int(v_.get("loc", -1))
                if e["kind"] == "leak":
                    nn = np.arange(N) if e.get("big") or l_ < 0 else np.nonzero(self.loc == l_)[0]
                else:
                    i_ = int(v_.get("inst", -1))
                    st_ = ((self.skind == G["work"]) & (self.sref == i_)).any(1) | ((self.bt_kind == kd_) & (self.loc == l_))
                    nn = np.nonzero(st_)[0]
                self.bt_jump(nn, j_, J["institution." + e["kind"]], e["kind"])
            self._bt_li = len(log)

    def _bt_year(self, t):
        """body_trust, yearly: each life's trust moves drift_y of the way toward .5 + drift_k x (fair - .5) + its own lean, fair its felt
        fairness in that sphere (sph_fair; S1's read when fair_read is on); a year in a body job (bt_kind) or serving in
        a unit (the host) adds work_or_serve_y in that body's sphere."""
        a = int(self._age(t))
        if a == self._bt_yr:
            return
        self._bt_yr = a; T_ = self.bt; J = T_["jumps"]
        on = ~np.isnan(self.btrust[:, 0]) & ~self.dead
        if not on.any():
            return
        tgt = 0.5 + T_["drift_k"] * (self.fair - 0.5) + self.bt_lean[:, None]
        self.btrust[on] = _uclip(self.btrust[on] + T_["drift_y"] * (tgt[on] - self.btrust[on]), J["floor"], J["ceiling"])
        jb = np.where(self.bt_kind >= 0, BT_INST_J[np.maximum(self.bt_kind, 0)], -1)
        for j_ in np.unique(jb[jb >= 0]).tolist():
            self.bt_jump(np.nonzero(jb == j_)[0], j_, J["work_or_serve_y"], "work")
        prot_ = SPHERES.index("prot")
        un_ = np.nonzero((self.skind == G["unit"]).any(1) & (jb != prot_))[0]   # the host, without a force title counted
        if len(un_):
            self.bt_jump(un_, prot_, J["work_or_serve_y"], "work")

    def bt_save(self, n):
        """body_trust, for save(): life n's trust (None before it starts), the known parents' mean, and what was read."""
        f_ = lambda v_: [None if np.isnan(x_) else float(x_) for x_ in v_]
        return dict(v=f_(self.btrust[n]), par=f_(self.bt_par[n]), kind=int(self.bt_kind[n]), lean=float(self.bt_lean[n]), i=int(self._bt_i),
                    li=int(self._bt_li), yr=int(self._bt_yr), rng=self._bt_rng.bit_generator.state if self.N == 1 else None)

    def _push(self, n, ma, q, lev, dom, base, target, var, t):
        P = self.P; rng = self.rng; W = self.W
        lv = LEVERS[lev]; ring = int(RING_OF[dom]); reach = float(self.dreach[n, dom])   # the domain's own reach
        if lv not in P["backfire"]:   # the spheres' levers (found, fund, lead, office) act from phase 4 (item 15)
            return dict(kind="push", n=int(n), t=int(t), lever=lv, domain=DOMAINS[dom], target=None, size="none",
                        backfire=False)
        size = base * reach * q
        bfp = P["backfire"][lv]
        if lv == "voice":
            rights = np.asarray(self._wf("rights", np.ones(5)), float)
            bfp *= 1 + (1 - float(rights[0]))
        elif lv == "subvert":
            bfp *= 1 + float(self._wf("watch", 0.3))
        back = (q < 0.5) and rng.random() < bfp
        tgt_out = None
        if ring == 0:   # the close circle: closeness, trust, their colors
            k = self._slot(n, int(target)) if target is not None and not isinstance(target, str) and int(target) >= 0 else -1
            if k < 0 and isinstance(target, str) and target in BIT:
                cand = np.nonzero(self._has_role(n, target) & self.lv[n])[0]
                k = int(cand[np.argmax(self.c[n, cand])]) if len(cand) else -1
            if k < 0:
                cand = np.nonzero(self.used[n] & self.lv[n])[0]
                k = int(cand[np.argmax(self.c[n, cand])]) if len(cand) else -1
            if k >= 0:
                tgt_out = int(self.uid[n, k]); s_ = size / 3.0
                if self.wa_l:
                    p0_, c0_, t0_ = self.pie[n, k].astype(float), float(self.c[n, k]), float(self.trust[n, k])
                if lv == "voice":
                    self.trust[n, k] = min(1, self.trust[n, k] + 0.05 * s_)
                    self.pie[n, k] = _norm(self.pie[n, k] + 0.02 * s_ * (ma - self.pie[n, k]))
                    self._psq[n, k] = _csum(self.pie[n, k] ** 2)
                    self.read[n, k] += 0.1 * s_ * (self.pie[n, k] - self.read[n, k])
                elif lv == "loyalty":
                    self.c[n, k] = min(1, self.c[n, k] + 0.05 * s_); self.trust[n, k] = min(1, self.trust[n, k] + 0.05 * s_)
                elif lv == "exit":
                    self.c[n, k] *= (1 - 0.25 * size); self.brk[n, k] = t
                elif lv == "neglect":
                    self.c[n, k] = max(0, self.c[n, k] - 0.03 * size)
                elif lv == "subvert" and q >= 0.5:
                    self.debt[n, k] = min(100, int(self.debt[n, k]) + 1)
                if back:
                    self.trust[n, k] *= 0.85; self.c[n, k] *= 0.9; self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
                if self.wa_l:   # the world answers, D: the person the push moved
                    self._wa_pmove(np.array([n]), np.array([k]), t, col=(self.pie[n, k] - p0_)[None],
                                   dc=np.array([self.c[n, k] - c0_]), dtr=np.array([self.trust[n, k] - t0_]))
        elif ring == 1:   # a group (or the neighbourhood): norms, cohesion, rank
            if DOMAINS[dom] == "place":
                js = np.nonzero(self.skind[n] == G["neighbours"])[0]
            elif isinstance(target, str) and target in G:
                js = np.nonzero(self.skind[n] == G[target])[0]
            else:
                js = np.nonzero((self.skind[n] >= 0) & (self.skind[n] != G["household"]))[0]
                js = js[np.argsort(-self.sts[n, js])]
            if len(js):
                j = int(js[0]); tgt_out = GROUP_KINDS[int(self.skind[n, j])]; s_ = size / 3.0
                if lv == "voice":
                    sn0_ = self.snorm[n, j].astype(float)
                    self.snorm[n, j] = _norm(self.snorm[n, j] + 0.03 * s_ * (1 - self.scoh[n, j] / 2) * (ma - self.snorm[n, j]))
                    if self.wa_l:   # the world answers, D: the group's ways the voice moved
                        self._wa_gmove(n, j, t, dnorm=self.snorm[n, j] - sn0_)
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.02 * s_)
                elif lv == "loyalty":
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.03 * s_); self.scoh[n, j] = min(0.98, self.scoh[n, j] + 0.02 * s_)
                elif lv == "exit" and q >= 0.5:
                    self._leave(n, j, t, "exit")
                elif lv == "neglect":
                    self.srank[n, j] = max(0, self.srank[n, j] - 0.03 * size)
                elif lv == "subvert" and q >= 0.5:
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.04 * s_)
                if back:
                    self.srank[n, j] = max(0, self.srank[n, j] - 0.15)
        else:   # institutions and the outer rings: queued in the world (lands next quarter)
            amt = size if reach > 0 else base * q * P["crowd"]   # W.push takes reach units; the world scales them
            tgt_out = DOMAINS[dom] if target is None or isinstance(target, (int, np.integer)) else f"{DOMAINS[dom]} {target}"
            if amt > 0:
                W.push(DOMAINS[dom], self._push_var(n, dom, ma, var), float(amt), int(P["lever_sign"][lv]))
                if self.wa_l and not back and reach > 0:   # the world answers, D: a national push, told when clear or more
                    self._wa_nation(n, dom, float(amt), t)
            if back:   # a backfire in an institution or the state: rank at work falls; the engine may add the rest
                js = np.nonzero(self.skind[n] == G["work"])[0]
                if len(js):
                    self.srank[n, js[0]] = max(0, self.srank[n, js[0]] - 0.15)
        seen = 0.0 if back else size
        word = "none" if seen <= 0 or (ring >= 2 and reach <= 0) else "small" if seen < 0.75 else "clear" if seen < 2 else "strong"
        if ring >= 2 and not back:   # institutions and the outer rings: nothing visible yet when it is queued (spec 7 §3);
            word = "unseen"          # what it changes reaches the story later through the world's own record
        # returned only: the engine logs it once, as world_push (not also as a cast event)
        return dict(kind="push", n=int(n), t=int(t), lever=lv, domain=DOMAINS[dom], target=tgt_out, size=word,
                    backfire=bool(back))

    def _push_var(self, n, dom, ma, var):
        """The world variable a push moves when the engine names none: a color-valued domain takes the act's own
        leading color as its direction (spec 7 §4); others their main lever point."""
        if var is not None:
            return str(var)
        d = DOMAINS[dom]
        if d in ("state", "culture"):
            return COLORS[int(np.argmax(ma))]
        if d == "institution":
            js = np.nonzero((self.skind[n] >= 0) & (self.sref[n] >= 0) & np.isin(self.skind[n], [G["work"], G["class"], G["unit"], G["ward"]]))[0]
            return f"legitimacy:{int(self.sref[n, js[0]])}" if len(js) else "legitimacy:0"
        if d == "place":
            return f"efficacy:{int(self.nb[n])}" if self.nb[n] >= 0 else f"crime:{int(self.loc[n])}"
        if d == "belief":
            return f"faith:{int(self.pfaith[n])}" if self.pfaith[n] >= 0 else "secular"
        return dict(economy="inequality", tech="invent", nature="warming", abroad="relation:0").get(d, d)

    # ------------------------------------------------------------------ finishing pack, part 2 (place_turnover)
    # chroma-world/spheres/finish-pack-draft.md "Places close and open" (World._pt_q closes and opens the places): a
    # place's regulars lose that haunt (they pick another at the yearly pick, none while every place of the kind is shut),
    # a setting held there is left, their rung in its sphere falls one step (TURNOVER rung_step), the ties made there
    # (its members) are kept at half strength (tie_keep), and a post leading it ends (not a fall). Each is an event in the
    # life's log (kind "place", state closed or opened) and, where the Library has them, a moment (cast_want
    # place_closed, place_opened; fired with no holder, cid -1). The new place's moment comes to those who lost the old
    # one and still live in its town.
    def _pt_init(self, run_seed):
        import sphere_data as SD
        self._pt_par = SD.TURNOVER
        self._pt_i = len(getattr(self.W, "pt_log", None) or [])   # the world's closings read so far
        self.pt_hits = []    # [life, week]: a haunt of theirs closed (the run's pt_lives)
        self.pt_lost = []    # [life, place]: waiting for the new place in that slot
        self.pt_due = []     # [life, moment key, place, week queued]: a place moment waiting to come
        self.pt_keys = set() # the place moment keys the batch has (WorldLink sets them); none: none is waited for
        self._pt_rng = np.random.default_rng([self.seed, 113, self.run_seed])   # the moments' picks (only with moments)

    def _pt_ev(self, n, t, state, e, p):
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="place", state=state, place=int(p), haunt=e["kind"],
                                    sphere=e["kind"].split(".")[0], name=int(e["name"]), why=e["why"]))
        key_ = "place_" + state
        if key_ in self.pt_keys:
            self.pt_due.append([int(n), key_, int(p), int(t)])

    def _pt_q(self, t):
        """The world's closings and openings since the last quarter, on the lives (see above)."""
        log = getattr(self.W, "pt_log", None)
        if not log or len(log) <= self._pt_i:
            return
        new = log[self._pt_i:]; self._pt_i = len(log)
        TO = self._pt_par; B = None
        for e in new:
            p = int(e["place"]); j = SPHERES.index(e["kind"].split(".")[0])
            if e["what"] == "opened":
                for x_ in [x_ for x_ in self.pt_lost if x_[1] == p]:
                    self.pt_lost.remove(x_)
                    if not self.dead[x_[0]] and int(self.loc[x_[0]]) == int(e["town"]):
                        self._pt_ev(x_[0], t, "opened", e, p)
                continue
            who = np.nonzero(~self.dead & ((self.hnt == p).any(1) | (self.shnt == p).any(1)))[0]
            for n in who.tolist():
                if self.lw:   # the keeper's post ends: a place led, or a leading title over a setting held there
                    for po in [po for po in self.lw_posts if po["n"] == n and po["place"] == p]:
                        self._lead_end(po, t, "place closed")
                for j_ in np.nonzero(self.shnt[n] == p)[0].tolist():   # the setting held there: its ties kept at half,
                    B = self._bits() if B is None else B                 # the keeper no longer one, then left
                    mem = self.used[n] & (B[n, :, j_] > 0)
                    self.c[n, mem] *= np.float32(TO["tie_keep"])
                    k = int(self.slead[n, j_])
                    if k >= 0 and not ((self.slead[n] == k) & (self.shnt[n] >= 0) & (self.shnt[n] != p)).any():
                        self.rmask[n, k] &= ~BIT["keeper"]
                    self._leave(n, j_, t, "place closed")
                h_ = [x_ for x_ in self.hnt[n] if x_ >= 0 and x_ != p]   # the haunt is gone (best first, as before)
                self.hnt[n] = (h_ + [-1, -1, -1])[:3]
                self.rung[n, j] = max(0.0, self.rung[n, j] + TO["rung_step"])
                self.pt_hits.append([n, int(t)]); self.pt_lost.append([n, p])
                self._pt_ev(n, t, "closed", e, p)

    def pt_take(self, t, busy):
        """The place moments to bring this week [(life, key)] (busy: lives with a moment already brought); one waiting
        more than 8 weeks lapses."""
        out = []
        for d_ in list(self.pt_due):
            n, key, p, t0_ = d_
            if t - t0_ > 8 or self.dead[n]:
                self.pt_due.remove(d_)
            elif n not in busy and n not in {o_[0] for o_ in out}:
                self.pt_due.remove(d_); out.append((n, key))
        return out
