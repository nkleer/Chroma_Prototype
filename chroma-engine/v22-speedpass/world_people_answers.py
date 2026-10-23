"""People's methods for the world answers v1 (chroma-world/spheres/world-answers-v1.md; the numbers in
sphere_data.WORLD_ANSWERS, copied from dynamics.json world_answers by tools/sphere_tables.py).

Part of class People (world_people.py), which inherits AnswersMixin. Nothing here exists until WorldLink.wa_setup()
calls wa_setup() (the engine's switch world_answers, with the world on); each part has its own sub-switch, so each can
be proved alone:
  A wa_groups   a member's presence leans their settings' ways (kept beside the norm, wa_soff); a good voice, found or
                lead act grows the setting; a setting the character led shrinks back when they no longer lead it
  B wa_places   a regular leans their haunts a little each year (in the place's lasting lean, hp_off); a place where
                the life stands as leader closes less often (World.wa_keep)
  D wa_ledger   record only: what each life moved, unit by unit (WA_UNITS, shared with the Library's lines,
                chroma-library/earth_world_lines.py, and the Game), told when a unit's total passes a step
  E wa_notice   the world notices what the character pursues: the goal's sphere (E1) weighs the people met (E2) and the
                haunt pick (E3); the sphere asks something of them (E4: asked_help, asked_lead, asked_speak); its events
                in their town reach the story and its offers come x 1.5 (E5). It adds no moment odds (aims v1's)
  F wa_phase2   a Known life's decisions for others (F2), the rivals, allies and successor around them (F3), the
                decisions in the ledger (F4), what the world kept (F5) and the price (F6). No land (v25)
Its own dice stream (_wa_rng), so the ledger alone draws nothing and moves no other draw."""
import numpy as np
from world_keys import DOMAINS, GROUP_KINDS, HAUNT_KINDS, LADDER, LEVERS, SPHERES
from world_people_base import BIT, C, DI, G, HAUNT_SPH, _csum, _norm, _uclip

# the ledger's unit keys (world-answers-v1.md section 4 D), shared with the Library's lines and the Game
WA_UNITS = ("person_colours", "person_closer", "person_further", "person_trust_up", "person_trust_down", "group_norm",
            "group_members", "place_mix", "place_founded", "place_kept_open", "town_sphere")
WA_NATION = ("state", "institution", "economy", "culture", "tech", "belief")   # national pushes, by domain
WA_RINGS = ("person", "group", "place", "town_sphere", "nation")               # what the world kept (F5), by ring
WA_SIZES = ("a little", "clearly", "a lot")
WA_KEPT = ("most", "some", "little")                                           # over .6, between, under .3
WA_RING_OF = dict(person_colours="person", person_closer="person", person_further="person", person_trust_up="person",
                  person_trust_down="person", group_norm="group", group_members="group", place_mix="place",
                  place_founded="place", place_kept_open="place", town_sphere="town_sphere", nation="nation")
# E1: a goal on a commitment takes its sphere (career: the work's own, read from the work setting), by the engine's
# commitment index (career, partner, children, community, faith)
WA_GOAL_SPH = {1: SPHERES.index("gather"), 2: SPHERES.index("care"), 3: SPHERES.index("gather"), 4: SPHERES.index("faith")}
# F2: the domain a decision at national standing pushes, by its sphere
WA_SPH_DOM = dict(rule="state", prot="state", comm="economy", prod="economy", learn="tech", care="institution",
                  faith="belief", arts="culture", gather="culture")
WA_SCOPES = ("place", "town_sphere", "nation")
_PK = ("person_colours", "person_closer", "person_further", "person_trust_up", "person_trust_down")


def _tv(a, b):
    return 0.5 * np.abs(np.asarray(a, float) - np.asarray(b, float)).sum(-1)


class AnswersMixin:
    wa_on = False
    wa_g = wa_p = wa_l = wa_n = wa_2 = False

    # ------------------------------------------------------------------ set up
    def wa_setup(self, P):
        """The world answers' state (P: the engine's switches world_answers and wa_*)."""
        import sphere_data as SD
        T = SD.WORLD_ANSWERS; N, K, M = self.N, self.K, self.M
        self.wa_on = True
        self.wa_g, self.wa_p, self.wa_l, self.wa_n, self.wa_2 = (bool(P.get(k_, False)) for k_ in
                                                                 ("wa_groups", "wa_places", "wa_ledger", "wa_notice", "wa_phase2"))
        self.wa_T = T; self.wa_steps = dict(T["ledger"]["steps"])
        self.wa_rec = float(T.get("recover", {}).get("y", 0.0))   # what a life caused fades back by this a year
        LG_ = T["ledger"]
        self.wa_age0 = float(LG_.get("from_age", 0))              # no footprint counted before this age
        self.wa_gap = 52.0 / LG_["per_unit_year"] if LG_.get("per_unit_year") else 0.0   # weeks between a unit's steps
        self.wa_tt = {}                                            # (unit's key) -> the week its last step was told
        self.wa_hcaus = None                                       # B: the caused part of each place's lasting lean
        self._wa_rng = np.random.default_rng([self.seed, 107, self.run_seed])
        self._wa_act = {}            # this week's act of each life that acted: (moment, option), set by WorldLink
        # D, the close circle (N x K: the person in each cast slot since their first caused change, uid)
        self.wa_puid = np.full((N, K), -1, np.int64)
        self.wa_ptot = np.zeros((N, K, 3))                    # colours (TV), closeness, trust (signed)
        self.wa_plev = np.zeros((N, K, 5), np.int8)           # steps told: _PK
        self.wa_pdir = np.zeros((N, K, C), np.float32)        # the colour change caused (summed), for what was kept
        self.wa_pbase = np.zeros((N, K, C), np.float32); self.wa_cbase = np.zeros((N, K, 2), np.float32)
        self.wa_pact = np.full((N, K, 2, 3), -1, np.int64)    # the last act that moved them toward, away: moment, option, week
        # D, the groups (N x M, each setting since the character joined it, sjoin)
        self.wa_gjoin = np.full((N, M), -10 ** 9, np.int64)
        self.wa_gtot = np.zeros((N, M, 2))                    # norm (TV), members gained (share of the size at joining)
        self.wa_glev = np.zeros((N, M, 2), np.int8)
        self.wa_gdir = np.zeros((N, M, C)); self.wa_gbase = np.zeros((N, M, C))
        self.wa_gact = np.full((N, M, 3), -1, np.int64)
        self.wa_gs0 = np.zeros((N, M)); self.wa_gled = np.zeros((N, M), bool)
        self.wa_soff = np.zeros((N, M, C), np.float32)        # A: the presence kept beside the norm
        self.wa_gwhat = [dict() for _ in range(N)]            # the setting's last presence or leading move: (what, week)
        # D, places, town spheres and the nation: per life, (unit, key) -> record
        self.wa_u = [dict() for _ in range(N)]
        self.wa_told = [[] for _ in range(N)]                 # every told line, per life
        self.wa_new = []                                       # (life, line) not yet handed to the engine
        self.wa_dec = []                                       # F2, F4: every decision (dicts)
        self.wa_ev = []                                        # E5: (life, sphere event) told for the goal
        # E: the goal each life pursues most (E1)
        self.wa_gsph = np.full(N, -1, np.int64); self.wa_gstr = np.zeros(N); self.wa_gsince = np.zeros(N, np.int64)
        self.wa_gmix = np.full((N, C), 1.0 / C)
        self.wa_q = []                                         # moments waiting: dicts n, key, sphere, cid, until
        self.wa_met = np.zeros(N)                              # E2: the fitting people met (a count, for the checks)
        self.wa_byr = np.zeros((N, 5)); self.wa_byw = np.zeros((N, 5))   # rings 1 to 3's caused change, and the weeks
        # lived, by the life's highest rung at the time (the check that what a life moves grows with standing)
        # F: the phase (Known), its sphere and start, the decisions' clock, the figures
        self.wa_known = np.zeros(N, bool); self.wa_nat = np.zeros(N, bool)
        self.wa_ksph = np.full(N, -1, np.int64); self.wa_kt0 = np.full(N, -1, np.int64)
        self.wa_rate = np.zeros(N); self.wa_sdec = np.zeros(N, np.int64); self.wa_ndec = np.zeros(N, np.int64)
        self.wa_kweeks = np.zeros(N, np.int64)
        self.wa_fig = [dict(rivals=[], allies=[], successor=None, after=None) for _ in range(N)]
        self._wa_yr = -1; self._wa_q = -1
        self._wa_ev_i = len(getattr(self.W, "sph_ev_log", ()))
        self._wa_cas = set()
        if self.wa_p:
            self.W.wa_keep = {}

    # ------------------------------------------------------------------ D, the ledger
    def _wa_ctx(self, n):
        return self._wa_act.get(int(n))

    def _wa_tell(self, n, unit, size, who, cause, t):
        ln = dict(unit=unit, size=size, who=who, age=round(float(self._age(t)), 2), cause=cause)
        self.wa_told[n].append(ln); self.wa_new.append((int(n), ln))

    def _wa_due(self, key, t):
        """A unit may tell a step now (per_unit_year: one a year); if so, it is marked told this week."""
        if self.wa_gap and t - self.wa_tt.get(key, -10 ** 9) < self.wa_gap:
            return False
        self.wa_tt[key] = int(t)
        return True

    def _wa_cause(self, acts, last, t):
        """The acts that made most of a unit's change (at most two) and the age of the last one."""
        top = sorted(acts.items(), key=lambda x_: -x_[1])[:2]
        out = dict(acts=[a_ for a_, _ in top])
        if last is not None:
            out["last"] = last[0]; out["last_age"] = round(float(self._age(last[1])), 2)
        return out

    def _wa_rg(self):
        """Each life's highest rung now (0 newcomer .. 4 leader)."""
        if not hasattr(self, "rung"):
            return np.zeros(self.N, np.int64)
        return np.clip(np.floor(np.asarray(self.rung).max(1)), 0, 4).astype(np.int64)

    def _wa_unit(self, n, unit, key, amt, who, t, base=None, d=None, size=None, what=None):
        """A unit of rings 1 and out (a place, a town sphere, the nation) moved by amt (TV, or a push's size): told when
        its total passes a step (wa_steps), or at size when one is given."""
        if not self.wa_l or self._age(t) < self.wa_age0:
            return
        if WA_RING_OF[unit] in ("place", "town_sphere"):
            self.wa_byr[n, self._wa_rg()[n]] += float(amt)
        u_ = self.wa_u[n]; rec = u_.get((unit, key))
        if rec is None:
            rec = u_[(unit, key)] = dict(unit=unit, who=who, tot=0.0, lev=0, acts={}, last=None, t0=int(t),
                                         base=None if base is None else np.array(base, float), dir=None)
        rec["tot"] += float(amt)
        if d is not None:
            rec["dir"] = np.array(d, float) if rec["dir"] is None else rec["dir"] + d
        a_ = self._wa_ctx(n) if what is None else what
        if a_ is not None:
            rec["acts"][a_] = rec["acts"].get(a_, 0.0) + float(amt); rec["last"] = (a_, int(t))
        if size is not None:
            rec["lev"] = max(rec["lev"], WA_SIZES.index(size) + 1)
            self._wa_tell(n, unit, size, who, self._wa_cause(rec["acts"], rec["last"], t), t)
            return
        st = self.wa_steps.get(unit)
        if not isinstance(st, (list, tuple)):
            return
        if rec["lev"] < len(st) and rec["tot"] >= st[rec["lev"]] - 1e-12 and self._wa_due(("u", n, unit, key), t):
            rec["lev"] += 1   # one step at a time, at most one a year (per_unit_year)
            self._wa_tell(n, unit, WA_SIZES[rec["lev"] - 1], who, self._wa_cause(rec["acts"], rec["last"], t), t)

    def _wa_pmove(self, nn, kk, t, col=None, dc=None, dtr=None, what=None):
        """People in the close circle moved by the life (nn, kk: life and cast slot, each pair once): col, the colour
        change (rows of C), dc and dtr, closeness and trust (signed). Told when a person's total passes a step."""
        if not self.wa_l or not len(nn) or self._age(t) < self.wa_age0:
            return
        nn = np.asarray(nn, np.int64); kk = np.asarray(kk, np.int64)
        new = self.uid[nn, kk] != self.wa_puid[nn, kk]
        if new.any():   # a person's first caused change (or a new person in the slot): the totals start
            a_, b_ = nn[new], kk[new]
            self.wa_puid[a_, b_] = self.uid[a_, b_]; self.wa_ptot[a_, b_] = 0; self.wa_plev[a_, b_] = 0
            self.wa_pdir[a_, b_] = 0; self.wa_pact[a_, b_] = -1
            self.wa_pbase[a_, b_] = self.pie[a_, b_] - (0 if col is None else np.asarray(col)[new])
            self.wa_cbase[a_, b_, 0] = self.c[a_, b_] - (0 if dc is None else np.asarray(dc)[new])
            self.wa_cbase[a_, b_, 1] = self.trust[a_, b_] - (0 if dtr is None else np.asarray(dtr)[new])
        if col is not None:
            col = np.asarray(col, float)
            self.wa_ptot[nn, kk, 0] += 0.5 * np.abs(col).sum(-1); self.wa_pdir[nn, kk] += col
        if dc is not None:
            self.wa_ptot[nn, kk, 1] += dc
        if dtr is not None:
            self.wa_ptot[nn, kk, 2] += dtr
        cx_ = [self._wa_ctx(n_) for n_ in nn] if what is None else None
        if cx_ is not None:   # the last act that moved each person, toward (up) or away (down)
            hs_ = np.array([x_ is not None and not isinstance(x_, str) for x_ in cx_], bool)
            if hs_.any():
                sg_ = np.zeros(len(nn))
                for v_ in (col if col is None else 0.5 * np.abs(col).sum(-1), dc, dtr):
                    if v_ is not None:
                        sg_ = sg_ + np.asarray(v_, float)
                for dn_, m_ in ((0, hs_ & (sg_ >= 0)), (1, hs_ & (sg_ < 0))):
                    ix_ = np.nonzero(m_)[0]
                    if len(ix_):
                        self.wa_pact[nn[ix_], kk[ix_], dn_] = [(cx_[i_][0], cx_[i_][1], int(t)) for i_ in ix_]
        tot = self.wa_ptot[nn, kk]
        L1 = float(self.P["layer_c"][0])
        sc, stie = self.wa_steps["person_colours"], self.wa_steps["person_tie"]
        def lev(v, st, big):
            return (v >= st[0] - 1e-12).astype(np.int8) + (v >= st[1] - 1e-12) + ((v >= st[-1] - 1e-12) & big)
        cn, ck = self.c[nn, kk], self.trust[nn, kk]
        lv_ = np.stack([lev(tot[:, 0], sc, tot[:, 0] >= sc[2] - 1e-12),
                        lev(tot[:, 1], stie, cn >= L1), lev(-tot[:, 1], stie, (cn <= 0.05) | (self.brk[nn, kk] >= t - 1)),
                        lev(tot[:, 2], stie, (ck >= 0.9) & (cn >= L1)), lev(-tot[:, 2], stie, (ck <= 0.1) | (self.brk[nn, kk] >= t - 1))], 1)
        up = (lv_ > self.wa_plev[nn, kk]) & (cn >= float(self.P["layer_c"][1]))[:, None]   # told of their people only
        if up.any():
            for r_, u_ in zip(*np.nonzero(up)):
                n_, k_ = int(nn[r_]), int(kk[r_])
                if not self._wa_due(("p", n_, int(self.uid[n_, k_]), int(u_)), t):
                    continue
                lv_[r_, u_] = self.wa_plev[n_, k_, u_] + 1   # one step at a time
                self.wa_plev[n_, k_, u_] = lv_[r_, u_]
                la_ = self.wa_pact[n_, k_, 1 if u_ in (2, 4) else 0]
                last_ = ((int(la_[0]), int(la_[1])), int(la_[2])) if la_[0] >= 0 else ((what or "the years together"), int(t))
                self._wa_tell(n_, _PK[u_], WA_SIZES[int(lv_[r_, u_]) - 1], dict(cid=int(self.uid[n_, k_])),
                              self._wa_cause({last_[0]: 1.0}, last_, t), t)

    def _wa_pflat(self, fi, t, dtr=None, dc=None):
        """_wa_pmove over flat (N x K) indices, where something moved."""
        fi = np.asarray(fi).reshape(-1)
        d_ = np.asarray(dtr if dtr is not None else dc, float).reshape(-1)
        m_ = d_ != 0
        if not m_.any():
            return
        f_ = fi[m_]
        self._wa_pmove(f_ // self.K, f_ % self.K, t, dtr=d_[m_] if dtr is not None else None, dc=d_[m_] if dc is not None else None)

    def _wa_gmove(self, n, j, t, dnorm=None, members=None, what=None):
        """A setting moved by the life: dnorm, its ways' change (C); members, the members it gained as a share of its
        size when the character joined it. Told when the setting's total passes a step."""
        if not self.wa_l or self._age(t) < self.wa_age0:
            return
        n, j = int(n), int(j)
        self._wa_greset(n, j)
        if dnorm is not None:
            self.wa_gtot[n, j, 0] += float(_tv(dnorm, 0)); self.wa_gdir[n, j] += dnorm
            self.wa_byr[n, self._wa_rg()[n]] += float(_tv(dnorm, 0))
        if members is not None:
            self.wa_gtot[n, j, 1] += float(members)
        a_ = self._wa_ctx(n) if what is None else None
        if a_ is not None:
            self.wa_gact[n, j] = (a_[0], a_[1], int(t))
        elif what is not None:
            self.wa_gwhat[n][j] = (what, int(t))
        for u_, unit in ((0, "group_norm"), (1, "group_members")):
            st = self.wa_steps[unit]; lv0 = int(self.wa_glev[n, j, u_]); lv = lv0
            if lv < len(st) and self.wa_gtot[n, j, u_] >= st[lv] - 1e-12 \
                    and self._wa_due(("g", n, int(self.sjoin[n, j]), j, u_), t):
                lv += 1   # one step at a time, at most one a year
            if lv > lv0:
                self.wa_glev[n, j, u_] = lv
                la_ = self.wa_gact[n, j]
                last_ = ((int(la_[0]), int(la_[1])), int(la_[2])) if la_[0] >= 0 else self.wa_gwhat[n].get(j, ("being there", int(t)))
                self._wa_tell(n, unit, WA_SIZES[lv - 1], dict(group=GROUP_KINDS[int(self.skind[n, j])], j=j),
                              self._wa_cause({last_[0]: 1.0}, last_, t), t)

    def _wa_gvec(self, m, d, t, what):
        """_wa_gmove for every setting in mask m at once (a norm change d, N x M x C), telling where a step is passed."""
        if self._age(t) < self.wa_age0:
            return
        self.wa_gtot[..., 0] += m * _tv(d, 0); self.wa_gdir += m[..., None] * d
        self.wa_byr[np.arange(self.N), self._wa_rg()] += (m * _tv(d, 0)).sum(1)
        st = self.wa_steps["group_norm"]
        lv = sum((self.wa_gtot[..., 0] >= s_ - 1e-12).astype(np.int8) for s_ in st)
        for n_, j_ in zip(*np.nonzero(m & (lv > self.wa_glev[..., 0]))):
            if not self._wa_due(("g", int(n_), int(self.sjoin[n_, j_]), int(j_), 0), t):
                continue
            lv[n_, j_] = self.wa_glev[n_, j_, 0] + 1   # one step at a time
            self.wa_glev[n_, j_, 0] = lv[n_, j_]; self.wa_gwhat[n_][int(j_)] = (what, int(t))
            la_ = self.wa_gact[n_, j_]
            last_ = ((int(la_[0]), int(la_[1])), int(la_[2])) if la_[0] >= 0 else (what, int(t))
            self._wa_tell(int(n_), "group_norm", WA_SIZES[int(lv[n_, j_]) - 1],
                          dict(group=GROUP_KINDS[int(self.skind[n_, j_])], j=int(j_)), self._wa_cause({last_[0]: 1.0}, last_, t), t)

    def _wa_greset(self, n, j):
        """A setting slot holds a new setting since the ledger last saw it: its totals start again."""
        if self.wa_gjoin[n, j] != self.sjoin[n, j]:
            self.wa_gjoin[n, j] = self.sjoin[n, j]; self.wa_gtot[n, j] = 0; self.wa_glev[n, j] = 0
            self.wa_gdir[n, j] = 0; self.wa_gbase[n, j] = self.snorm[n, j]; self.wa_gact[n, j] = -1
            self.wa_gs0[n, j] = max(1, int(self.ssize[n, j])); self.wa_gled[n, j] = False; self.wa_soff[n, j] = 0
            self.wa_gwhat[n].pop(j, None)

    def _wa_place(self, n, l, h, i, old, new, t, unit="place_mix", size=None, what=None):
        """A place (town l, kind h, slot i) moved by the life from old to new (the move kept as caused, to fade back)."""
        if self.wa_rec > 0 and self.wa_p:   # the fading is wa_places' (the ledger alone is a record)
            if self.wa_hcaus is None:
                self.wa_hcaus = np.zeros(self.W.hp_off.shape)
            self.wa_hcaus[int(l), int(h), int(i)] += np.log(np.maximum(new, 1e-9)) - np.log(np.maximum(old, 1e-9))
        p_ = int(np.ravel_multi_index((int(l), int(h), int(i)), self.W.hp_s.shape[:3]))
        self._wa_unit(int(n), unit, p_, float(_tv(new, old)), dict(place=p_, kind=HAUNT_KINDS[int(h)]), t,
                      base=old, d=np.asarray(new, float) - old, size=size, what=what)

    def _wa_lever(self, n, loc, hp0, ss0, lv, rg, t):
        """After a sphere lever (People._sph_lever): what it moved in the life's town, its places and spheres."""
        W = self.W
        if hp0 is not None:
            d_ = _tv(W.hp_s[loc], hp0)                                         # kinds x slots
            for h_, i_ in zip(*np.nonzero(d_ > 1e-9)):
                fd_ = lv == "found" and d_[h_, i_] >= d_.max() - 1e-12
                self._wa_place(n, loc, h_, i_, hp0[h_, i_], W.hp_s[loc, h_, i_], t,
                               unit="place_founded" if fd_ else "place_mix",
                               size=WA_SIZES[0 if rg < 2 else 1 if rg < 4 else 2] if fd_ else None)
        d_ = _tv(W.sph_s[loc], ss0)
        for j_ in np.nonzero(d_ > 1e-12)[0]:
            self._wa_unit(int(n), "town_sphere", (int(loc), int(j_)), float(d_[j_]), dict(town=int(loc), sphere=SPHERES[j_]), t,
                          base=ss0[j_], d=W.sph_s[loc, j_] - ss0[j_])

    def _wa_nation(self, n, dom, amt, t, what=None):
        """A push from the life to a national domain (ring 2 and out): counted; told when of size clear or more, by
        what it visibly did (the Library's NATION lines), never by a hidden number."""
        d_ = DOMAINS[dom] if not isinstance(dom, str) else dom
        if d_ not in WA_NATION:
            return
        size = None if amt < 0.75 else "clearly" if amt < 2 else "a lot"
        self._wa_unit(int(n), "nation", d_, float(amt), dict(domain=d_), t, size=size, what=what)

    def _wa_lead_norm(self, rate, tsum, s_old):
        """The leaders' mix (late effect): a setting the character leads drifts toward them through the drift's leader
        share (_settings_month's .2 of the target)."""
        ld_ = (self.slead == -2) & (self.skind >= 0)
        for n_, j_ in zip(*np.nonzero(ld_)):
            d_ = rate[n_, j_] * 0.2 / max(float(tsum[n_, j_]), 1e-9) * (self.w[n_] - s_old[n_, j_])
            self._wa_gmove(n_, j_, self.t, dnorm=d_, what="leading it")

    # ------------------------------------------------------------------ A, B: presence, growth, kept open
    def _wa_month(self, t):
        """Monthly (People.month, before the settings' drift): A's presence and shrink, the season's clock; a new year
        of age: B's presence and the places kept open, F's figures."""
        N, M = self.N, self.M; live = ~self.dead
        self.wa_byw[np.arange(N), self._wa_rg()] += 4 * live
        act = (self.skind >= 0) & (self.skind != G["household"]) & live[:, None]
        for n_, j_ in zip(*np.nonzero((self.skind >= 0) & (self.wa_gjoin != self.sjoin))):
            self._wa_greset(int(n_), int(j_))
        self.wa_soff[self.skind < 0] = 0
        if self.wa_g and act.any():
            GT = self.wa_T["groups"]; rk = self.srank
            e_, w_ = GT["rank_w"]["edges"], GT["rank_w"]["w"]
            rw = np.select([rk < e_[0], rk < e_[1], rk < e_[2]], w_[:3], w_[3])
            rw = np.where(self.slead == -2, GT["rank_w"]["leader"], rw)
            k_ = GT["k_pres"] * rw * (1 - GT["coh_damp"] * self.scoh) * act
            d_ = (k_[..., None] * (self.w[:, None, :] - self.snorm)).astype(np.float32)
            self.snorm += d_; self.wa_soff += d_
            if self.wa_l:
                self._wa_gvec(act, d_.astype(float), t, "being there")
            self.wa_gled |= (self.slead == -2) & act
            q = int(t // 13)
            if q != self._wa_q:   # a quarter: a setting the character no longer leads shrinks back toward its old size
                self._wa_q = q
                sh_ = self.wa_gled & (self.slead != -2) & (self.skind >= 0) & (self.ssize > self.wa_gs0)
                for n_, j_ in zip(*np.nonzero(sh_)):
                    self.ssize[n_, j_] -= max(1, int(np.ceil(GT["shrink_q"] * (self.ssize[n_, j_] - self.wa_gs0[n_, j_]))))
        if self.wa_2 and t % 13 == 0:
            self.wa_sdec[:] = 0
        if self.wa_p and t % 13 == 0:
            self._wa_kept_open(t)
        yr = int(self._age(t))
        if yr != self._wa_yr:
            self._wa_yr = yr
            if self.wa_rec > 0:
                self._wa_recover()
            if self.wa_p:
                self._wa_presence(t)
            if self.wa_2:
                self._wa_figures(t)

    def _wa_recover(self):
        """Yearly (recover y): what lives caused in a place's lasting lean (hp_off) and in a setting's norm (wa_soff) fades
        back toward its own way by y; a regular's or member's presence renews its share as it goes."""
        y = self.wa_rec; W = self.W
        if self.wa_hcaus is not None:
            op_ = getattr(W, "pt_open", None)
            if op_ is not None:   # a place closed or opened again: a new place, its lean its own
                self.wa_hcaus[op_ >= 0] = 0.0
            d_ = y * self.wa_hcaus
            W.hp_off -= d_; self.wa_hcaus -= d_
        if self.wa_g:
            d_ = (y * self.wa_soff).astype(np.float32)
            nm_ = np.maximum(self.snorm - d_, 1e-6)
            self.snorm[...] = np.where((self.skind >= 0)[..., None], nm_ / nm_.sum(-1, keepdims=True), self.snorm)
            self.wa_soff -= d_

    def _wa_presence(self, t):
        """B, yearly: each regular leans each haunt toward their colours by pres_lean[rung in its sphere] x the share of
        their hours spent there (kept in the place's lasting lean); a leader's place closes less often (World.wa_keep)."""
        W = self.W
        if not self.sph_h or getattr(W, "hp_s", None) is None:
            return
        PL = self.wa_T["places"]; pl_ = np.asarray(PL["pres_lean"], float)
        H, P_ = len(HAUNT_KINDS), W.hp_s.shape[2]
        hrs = getattr(self, "hrs", None)
        nk = (self.hnt >= 0).sum(1)
        keep = {}
        for n_ in np.nonzero(~self.dead & (nk > 0))[0]:
            if hrs is not None and hrs[n_].sum() > 0:
                sh_ = float(hrs[n_, 2]) / max(int(nk[n_]), 1) / float(hrs[n_].sum())
            else:
                sh_ = 0.2 / max(int(nk[n_]), 1)
            for p_ in self.hnt[n_]:
                if p_ < 0:
                    continue
                l, h, i = (int(x_) for x_ in np.unravel_index(int(p_), W.hp_s.shape[:3]))
                j_ = int(HAUNT_SPH[h]); rg = min(max(int(np.floor(self.rung[n_, j_])), 0), 4)
                if rg >= int(PL["kept_open"]["rung"]):
                    keep[int(p_)] = float(PL["kept_open"]["hazard_x"])
                k_ = pl_[rg] * sh_
                if k_ <= 0:
                    continue
                old = W.hp_s[l, h, i].copy(); new = W._sph_nudge(old, self.w[n_], k_)
                W._sph_place_set(l, h, i, new)
                self._wa_place(n_, l, h, i, old, new, t, what="being there")
        W.wa_keep = keep

    def _wa_kept_open(self, t):
        """B: a slump, war or disaster cascade running in a town closes no place a life there leads: kept open."""
        W = self.W
        cas = getattr(W, "sph_cas", None); keep = getattr(W, "wa_keep", None) or {}
        if not cas or not keep or getattr(W, "pt_open", None) is None:
            return
        run_ = {(int(x_[0]), int(x_[1])) for x_ in cas}
        for p_ in keep:
            l, h, i = (int(x_) for x_ in np.unravel_index(int(p_), W.hp_s.shape[:3]))
            if W.pt_open[l, h, i] >= 0:
                continue
            for c_, lc_ in run_:
                if (lc_ < 0 or lc_ == l) and (p_, c_) not in self._wa_cas:
                    self._wa_cas.add((p_, c_))
                    for n_ in np.nonzero(~self.dead & (self.hnt == p_).any(1))[0]:
                        j_ = int(HAUNT_SPH[h])
                        if np.floor(self.rung[n_, j_]) >= int(self.wa_T["places"]["kept_open"]["rung"]):
                            self._wa_unit(int(n_), "place_kept_open", int(p_), 1.0, dict(place=int(p_), kind=HAUNT_KINDS[h]),
                                          t, size="clearly", what="keeping it open")

    def _wa_grow(self, idx, lev, q, js, t):
        """A: an act with voice, found or lead that went well (q .5 or more), by a member of rank .5 or more, adds
        members to the setting: max(1, round(ssize x k x q x the group reach / 3))."""
        GR = self.wa_T["groups"]["grow"]; ok_l = [LEVERS.index(x_) for x_ in GR["levers"]]
        for e_ in range(len(idx)):
            if lev[e_] not in ok_l or q[e_] < GR["min_q"]:
                continue
            n = int(idx[e_]); j_ = int(js[e_]) if js is not None else -1
            cand = np.nonzero((self.skind[n] >= 0) & (self.skind[n] != G["household"]) & (self.srank[n] >= GR["min_rank"]))[0]
            if j_ >= 0:
                cand = cand[self.set_sphere[n, cand] == j_]
            if not len(cand):
                continue
            j = int(cand[np.argmax(self.sts[n, cand])])
            self._wa_greset(n, j)
            add = max(int(GR["min_add"]), int(round(float(self.ssize[n, j]) * GR["k"] * q[e_] * float(self.dreach[n, DI["group"]]) / 3)))
            self.ssize[n, j] += add
            self._wa_gmove(n, j, t, members=add / max(float(self.wa_gs0[n, j]), 1.0))

    # ------------------------------------------------------------------ E: the world notices what they pursue
    def wa_goal(self, gm, gd, gs, gb):
        """E1, weekly from the engine: each life's strongest goal slot (gm its ways; with aims, the aim's face), its
        strength and start, and its sphere: a commitment's (career: the work's sphere), else the sphere whose home ways
        (M0) fit it best."""
        gs = np.asarray(gs, float); b_ = gs.argmax(1); ar = np.arange(self.N)
        st = gs[ar, b_]; dm = np.asarray(gd)[ar, b_]; mx = np.asarray(gm, float)[ar, b_]
        M0 = self._wa_m0()
        sph = np.argmax(mx @ M0.T, 1)
        for c_, j_ in WA_GOAL_SPH.items():
            sph = np.where(dm == c_, j_, sph)
        if (dm == 0).any():
            ss_ = self.set_sphere; wk_ = (self.skind == G["work"]) & (ss_ >= 0)
            ws_ = np.where(wk_.any(1), ss_[ar, wk_.argmax(1)], -1)
            sph = np.where((dm == 0) & (ws_ >= 0), ws_, sph)
        sph = np.where(st > 0, sph, -1)
        new = sph != self.wa_gsph
        self.wa_gsince = np.where(new, np.asarray(gb)[ar, b_], self.wa_gsince)
        self.wa_gsph = sph; self.wa_gstr = np.where(st > 0, st, 0.0); self.wa_gmix = _norm(mx)

    def _wa_m0(self):
        W = self.W
        if getattr(W, "sph_s", None) is not None and hasattr(W, "_sph_tables"):
            return np.asarray(W._sph_tables()["M0"], float)
        import sphere_data as SD
        return np.asarray(SD.M0[next(iter(SD.M0))], float)[:, self.perm]

    def _wa_fill_bonus(self, n, cand):
        """E2: a moment's role slot leans to people who fit the goal: notice people x strength x fit (1 for a person who
        stands in the goal's sphere, else their colours' fit clipped to 0..1)."""
        j = int(self.wa_gsph[n])
        if j < 0 or not len(cand):
            return 0.0
        fit = _uclip(C * (self.pie[n, cand] @ self.wa_gmix[n]) - 1, 0, 1)
        fit = np.where(self._wa_cast_in(n, j)[cand] & (self.stand[n, cand] >= 1), 1.0, fit)
        return self.wa_T["notice"]["people"] * self.wa_gstr[n] * fit

    def _wa_alike(self, nn):
        """E2 for the people met by chance: the share of them drawn alike the goal (about doubling a fitting person's
        chance with a strong goal); its own stream."""
        p_ = self.wa_T["notice"]["people"] * self.wa_gstr[nn] * (self.wa_gsph[nn] >= 0)
        return self._wa_rng.random(len(nn)) < p_ / (1 + p_)

    def _wa_haunt_bonus(self, ns):
        """E3: the haunt pick leans to places in the goal's sphere (notice places x strength)."""
        j = self.wa_gsph[ns]
        return self.wa_T["notice"]["places"] * self.wa_gstr[ns][:, None] * ((HAUNT_SPH[None, :] == j[:, None]) & (j[:, None] >= 0))

    def _wa_offer_x(self, ns, key):
        """E5: an offer of the goal's sphere reaches them x offers_x."""
        sp_ = str(key).split(".")[0]
        if sp_ not in SPHERES:
            return 1.0
        return np.where(self.wa_gsph[ns] == SPHERES.index(sp_), self.wa_T["notice"]["offers_x"], 1.0)

    def _wa_cast_in(self, n, j):
        """The cast of life n who are in sphere j with them: members of a setting of theirs in that sphere."""
        ss_ = self.set_sphere[n]; js_ = np.nonzero((self.skind[n] >= 0) & (ss_ == j))[0]
        m_ = np.zeros(self.K, bool)
        for j_ in js_:
            m_ |= (self.mset[n] & self._bit(int(j_))) > 0
        return m_ & self.used[n] & self.lv[n]

    def _wa_week(self, t):
        """Weekly (People.week): E4's asks, E5's told events, F2's decisions and the figures' own."""
        N = self.N; r = self._wa_rng; live = ~self.dead
        self.wa_q = [x_ for x_ in self.wa_q if x_["until"] >= t and not self.dead[x_["n"]]]
        if self.wa_n:
            AK = self.wa_T["notice"]["ask"]; j = self.wa_gsph
            rg = np.where(j >= 0, np.floor(self.rung[np.arange(N), np.maximum(j, 0)]), -1) if hasattr(self, "rung") else np.full(N, -1.0)
            ok = live & (j >= 0) & (t - self.wa_gsince >= 52 * AK["after_y"]) & (rg >= AK["min_rung"])
            hit = ok & (r.random(N) < AK["rate_y"] / 52.0)
            for n_ in np.nonzero(hit)[0]:
                key = AK["by_rung"][min(int(rg[n_]), max(AK["by_rung"]))]
                self.wa_q.append(dict(n=int(n_), key=key, sphere=int(j[n_]), cid=-1, until=int(t) + 8))
            log = getattr(self.W, "sph_ev_log", None)
            if log is not None and len(log) > self._wa_ev_i:
                import sphere_data as SD
                rows = np.asarray(log[self._wa_ev_i:]).tolist(); self._wa_ev_i = len(log)
                for _, i_, l_ in rows:
                    e_ = SD.EV[int(i_)]; js_ = SPHERES.index(e_["sphere"]) if e_["sphere"] in SPHERES else -1
                    for n_ in np.nonzero(live & (self.wa_gsph == js_) & ((self.loc == l_) if l_ >= 0 else True))[0]:
                        self.wa_ev.append((int(n_), dict(event=f"{e_['sphere']}.{e_['key']}", age=round(float(self._age(t)), 2))))
        if self.wa_2:
            self._wa_decisions(t)

    # ------------------------------------------------------------------ F: the second phase, for Known lives
    def wa_set_known(self, known, national, t):
        """F1, weekly from the engine: who is Known (aims v1's heights: Known reached and the standing still held), and
        at national standing. Entering, the phase takes the sphere of their highest rung (the goal's on a tie)."""
        known = np.asarray(known, bool) & ~self.dead
        ent = known & ~self.wa_known; out = ~known & self.wa_known
        for n_ in np.nonzero(ent)[0]:
            rg_ = self.rung[n_] if hasattr(self, "rung") else np.zeros(len(SPHERES))
            tie = np.nonzero(rg_ >= rg_.max() - 1e-9)[0]
            j_ = int(self.wa_gsph[n_]) if self.wa_gsph[n_] in tie else int(tie[0])
            self.wa_ksph[n_] = j_; self.wa_kt0[n_] = t; self.wa_fig[n_]["after"] = None
            self._wa_draw_rate(n_, bool(national[n_]))
        for n_ in np.nonzero(out)[0]:   # the phase ends with the post or the name: a successor carries on
            sc_ = self.wa_fig[n_]["successor"]
            if sc_ is not None:
                self.wa_fig[n_]["after"] = dict(sc_, sphere=int(self.wa_ksph[n_]))
                self.wa_q.append(dict(n=int(n_), key="successor_hand", sphere=int(self.wa_ksph[n_]), cid=int(sc_["cid"]), until=int(t) + 8))
        self.wa_known[:] = known; self.wa_nat[:] = np.asarray(national, bool) & known
        self.wa_kweeks += known

    def _wa_draw_rate(self, n, nat):
        lo, hi = self.wa_T["phase2"]["decisions_y"]["national" if nat else "known"]
        if nat and getattr(self, "nat", None) is not None and self.nat.influence_only()[n]:   # v25: a national voice, no seat
            lo, hi = self.nat.C["influence_y"]
        self.wa_rate[n] = float(self._wa_rng.uniform(lo, hi))

    def _wa_open(self, n):
        """F2's open: 1.5 in a crisis (a recession declared, a war, a cascade running in their town), else 1."""
        W = self.W; o = self.wa_T["phase2"]["size"]["open"]["x"]
        if getattr(W, "rec_declared", False) or int(getattr(W, "war", 0) or 0) > 0:
            return o
        cas = getattr(W, "sph_cas", None) or []
        return o if any(int(x_[1]) < 0 or int(x_[1]) == int(self.loc[n]) for x_ in cas) else 1.0

    def _wa_team(self, n):
        """F3's team: 1 + .5 for each ally backing (trust .5 or more, close enough to stand by them), at most 2."""
        tm = self.wa_T["phase2"]["size"]["team"]; nb = 0
        for a_ in self.wa_fig[n]["allies"]:
            k_ = self._slot(n, a_["cid"])
            if k_ >= 0 and self.lv[n, k_] and self.trust[n, k_] >= 0.5 and self.c[n, k_] >= self.P["layer_c"][2]:
                nb += 1
        return min(tm["max"], 1 + tm["per_ally"] * nb)

    def _wa_figures(self, t):
        """F3, yearly while Known: the rivals (1 or 2 who stand high in the sphere, colours far from theirs), the allies
        (who stand in it, colours close), the successor from the second Known year (the closest younger one who
        stands in it). Each is a cast member; a rival with none in the cast stands without a slot (cid -1)."""
        F2 = self.wa_T["phase2"]; r = self._wa_rng
        for n_ in np.nonzero(self.wa_known)[0]:
            n_ = int(n_); j = int(self.wa_ksph[n_]); fg = self.wa_fig[n_]
            self._wa_draw_rate(n_, bool(self.wa_nat[n_]))
            inn = self._wa_cast_in(n_, j); tv = _tv(self.pie[n_], self.w[n_])
            cand = np.nonzero(inn & (self.stand[n_] >= 2) & (tv >= F2["rivals"]["min_tv"]))[0]
            nr = int(r.integers(F2["rivals"]["n"][0], F2["rivals"]["n"][1] + 1))
            riv = [dict(cid=int(self.uid[n_, k_]), mix=self.pie[n_, k_].astype(float).tolist(), reach=2.0,
                        per_y=float(r.uniform(*F2["rivals"]["decisions_y"])))
                   for k_ in cand[np.argsort(-tv[cand])][:nr]]
            if len(riv) < nr and not fg["rivals"]:   # none in the cast: a figure of the town who stands for the far side
                far = _norm(np.maximum(2 * self.W.sph_s[self.loc[n_], j] - self.w[n_], 0.005)) if getattr(self.W, "sph_s", None) is not None \
                    else _norm(1.0 - self.w[n_])
                if _tv(far, self.w[n_]) < F2["rivals"]["min_tv"]:
                    far = np.eye(C)[int(np.argmin(self.w[n_]))]
                riv.append(dict(cid=-1, mix=np.asarray(far, float).tolist(), reach=2.0, per_y=float(r.uniform(*F2["rivals"]["decisions_y"]))))
            fg["rivals"] = riv if riv else fg["rivals"]
            al = np.nonzero(inn & (self.stand[n_] >= 1) & (tv < F2["allies"]["max_tv"]))[0]
            new_al = [int(self.uid[n_, k_]) for k_ in al]
            old_al = [a_["cid"] for a_ in fg["allies"]]
            won = [x_ for x_ in new_al if x_ not in old_al]; lost = [x_ for x_ in old_al if x_ not in new_al]
            fg["allies"] = [dict(cid=x_) for x_ in new_al]
            if won and old_al is not None and t - self.wa_kt0[n_] >= 26:
                self.wa_q.append(dict(n=n_, key="ally_won", sphere=j, cid=int(won[0]), until=int(t) + 8))
            elif lost:
                self.wa_q.append(dict(n=n_, key="ally_lost", sphere=j, cid=int(lost[0]), until=int(t) + 8))
            if fg["successor"] is None and t - self.wa_kt0[n_] >= 52 * F2["successor"]["from_year"]:
                sc = np.nonzero(inn & (self.stand[n_] >= 1) & (self.born[n_] > self.t0))[0]
                if len(sc):
                    k_ = int(sc[np.argmax(self.c[n_, sc])])
                    fg["successor"] = dict(cid=int(self.uid[n_, k_]), mix=self.pie[n_, k_].astype(float).tolist(), reach=2.0,
                                           per_y=float(r.uniform(*F2["rivals"]["decisions_y"])))
                    self.wa_q.append(dict(n=n_, key="successor_seen", sphere=j, cid=fg["successor"]["cid"], until=int(t) + 8))

    def _wa_decisions(self, t):
        """F2's clock (weekly): a Known life's decisions for others (4 to 8 a year, 8 to 12 at national standing) wait
        for their moment; the rivals' own decisions land on the same town sphere (2 to 4 a year each, sized as F2 at
        their reach); after the phase, the successor carries on in their own direction."""
        r = self._wa_rng; W = self.W
        kn = np.nonzero(self.wa_known)[0]
        if len(kn):
            hit = r.random(len(kn)) < self.wa_rate[kn] / 52.0
            for n_ in kn[hit]:
                if not any(x_["n"] == n_ and x_["key"] == "decide" for x_ in self.wa_q):
                    self.wa_q.append(dict(n=int(n_), key="decide", sphere=int(self.wa_ksph[n_]), cid=-1, until=int(t) + 4))
        if getattr(W, "sph_s", None) is None:
            return
        for n_ in range(self.N):
            fg = self.wa_fig[n_]
            figs = [(x_, int(self.wa_ksph[n_]), "rival") for x_ in fg["rivals"]] if self.wa_known[n_] else []
            if fg["after"] is not None:
                figs.append((fg["after"], int(fg["after"]["sphere"]), "successor"))
            for x_, j, who in figs:
                if j < 0 or r.random() >= x_["per_y"] / 52.0:
                    continue
                q_ = 0.6; l = int(self.loc[n_])
                d_ = self.wa_T["phase2"]["size"]["k_town"] * x_["reach"] / 3 * q_ * self._wa_open(n_)
                W.sph_s[l, j] = W._sph_nudge(W.sph_s[l, j], np.asarray(x_["mix"], float), d_)
                if who == "rival" and x_["cid"] >= 0 and r.random() < 0.25:
                    self.wa_q.append(dict(n=int(n_), key="rival_push", sphere=j, cid=int(x_["cid"]), until=int(t) + 8))

    def wa_take(self, t, pending):
        """The moments waiting this week (one a life, not one with a moment already): (life, key, sphere, cid)."""
        out = []; seen = set(pending)
        for x_ in sorted(self.wa_q, key=lambda y_: (y_["key"] != "decide", y_["until"])):
            if x_["n"] in seen:
                continue
            seen.add(x_["n"]); out.append(x_)
        return out

    def wa_taken(self, x):
        if x in self.wa_q:
            self.wa_q.remove(x)

    def wa_resolve(self, n, key, j, scope, ma, succ, idle, t=None):
        """The moment the world brought, answered. A decision (F2) lands by the option's scope: on the town's sphere,
        d = k_town x reach / 3 x q x open x team; on their place in the sphere, .05 x q; at national standing, a push
        of reach x q x open x team. Its fairness (the option's fit with the town's ways in that sphere) moves felt
        fairness and trust in the sphere's bodies for everyone in town (body_trust's event jumps); the cast in the
        sphere judge it, fully seen. An ask (E4) or a figure's moment is recorded (its option's lever did the rest)."""
        t = self.t if t is None else t; n = int(n); W = self.W
        ev = dict(kind="world answers", key=key, sphere=SPHERES[j] if j >= 0 else None, age=round(float(self._age(t)), 2))
        if key != "decide":
            ev["answer"] = "left it" if idle else "took it up" if succ else "tried"
            return ev
        self.wa_ndec[n] += 1; self.wa_sdec[n] += 1
        F2 = self.wa_T["phase2"]; SZ = F2["size"]
        ma = _norm(np.asarray(ma, float)); l = int(self.loc[n])
        q = 0.8 if succ else 0.4; op = self._wa_open(n); tm = self._wa_team(n)
        sc = WA_SCOPES[scope] if 0 <= scope < len(WA_SCOPES) else "town_sphere"
        if sc == "nation" and not self.wa_nat[n]:
            sc = "town_sphere"
        ev.update(scope=sc, known=bool(self.wa_known[n]), national=bool(self.wa_nat[n]), open=op, team=tm)
        if idle:
            ev["answer"] = "left it"; self.wa_dec.append(dict(ev, n=n)); return ev
        moved = 0.0
        if sc == "place" and getattr(W, "hp_s", None) is not None:
            P_ = W.hp_s.shape[2]; hs_ = [int(p_) for p_ in self.hnt[n] if p_ >= 0 and HAUNT_SPH[(p_ // P_) % len(HAUNT_KINDS)] == j]
            if hs_:
                l2, h, i = (int(x_) for x_ in np.unravel_index(hs_[0], W.hp_s.shape[:3]))
            else:   # no place of theirs there: the town's place of the sphere most like them
                ks_ = np.nonzero(HAUNT_SPH == j)[0]; c_ = W.hp_s[l, ks_].reshape(-1, C)
                b_ = int(np.argmin(_tv(c_, self.w[n]))); l2, h, i = l, int(ks_[b_ // P_]), b_ % P_
            old = W.hp_s[l2, h, i].copy(); new = W._sph_nudge(old, ma, SZ["place"] * q)
            W._sph_place_set(l2, h, i, new); moved = float(_tv(new, old))
            self._wa_place(n, l2, h, i, old, new, t)
            ev["place"] = int(np.ravel_multi_index((l2, h, i), W.hp_s.shape[:3]))
        elif sc == "nation":
            dm = WA_SPH_DOM[SPHERES[j]]; amt = float(self.dreach[n, DI[dm]]) * q * op * tm
            var = self._push_var(n, DI[dm], ma, None); sg = 1
            if dm == "state" and getattr(self, "_wa_law", None) is not None:
                ld_ = self._wa_law()
                if ld_ is not None:
                    var, sg = ld_
            W.push(dm, var, max(amt, 0.0), sg); moved = amt
            self._wa_nation(n, dm, amt, t)
            ev.update(domain=dm, var=str(var))
        elif getattr(W, "sph_s", None) is not None:
            reach = max(float(self.dreach[n, DI["institution"]]), 1.0)
            d_ = SZ["k_town"] * reach / 3 * q * op * tm
            old = W.sph_s[l, j].copy(); W.sph_s[l, j] = W._sph_nudge(old, ma, d_); moved = float(_tv(W.sph_s[l, j], old))
            self._wa_unit(n, "town_sphere", (l, j), moved, dict(town=l, sphere=SPHERES[j]), t, base=old, d=W.sph_s[l, j] - old)
        if getattr(W, "sph_s", None) is not None:   # fair or unfair: the option's fit with the town's ways in the sphere
            fair = bool(C * float(ma @ W.sph_s[l, j]) - 1 >= 0)
            import sphere_data as SD
            jm = SD.TRUST["jumps"]["event_fair" if fair else "event_unfair"]
            here = ~self.dead & (self.loc == l)
            if getattr(self, "sph_fr", False):
                self.fair[here, j] = _uclip(self.fair[here, j] + jm, 0, 1)
            if getattr(self, "bt_on", False):
                bt_ = self.btrust[here, j]
                self.btrust[here, j] = np.where(np.isnan(bt_), bt_, _uclip(bt_ + jm, 0, 1))
            ev["fair"] = fair
        inn = np.nonzero(self._wa_cast_in(n, j))[0]   # the cast in the sphere judge it, fully seen
        if len(inn):
            ft = np.clip(C * (self.pie[n, inn] @ ma) - 1, -1, 1)
            t0_, c0_ = self.trust[n, inn].copy(), self.c[n, inn].copy()
            self.trust[n, inn] = _uclip(self.trust[n, inn] + 0.01 * ft, 0, 1); self.c[n, inn] = _uclip(self.c[n, inn] + 0.01 * ft, 0, 1)
            self._wa_pmove(np.full(len(inn), n), inn, t, dc=self.c[n, inn] - c0_, dtr=self.trust[n, inn] - t0_)
        ev.update(moved=round(moved, 5), answer="decided")
        self.wa_dec.append(dict(ev, n=n))
        return ev

    def wa_price(self):
        """F6: the hours a week the phase takes from home and friends (as a share of the week's free time), and the
        stress a month in a season with three or more decisions."""
        pr = self.wa_T["phase2"]["price"]
        return (self.wa_known * pr["hours_week"] / 112.0,
                self.wa_known * (self.wa_sdec >= 3) * pr["stress_month"])

    # ------------------------------------------------------------------ the ledger read back (D, F5)
    def wa_output(self):
        """Per life: the told lines, each ring's caused total and its largest footprint with what the world kept of it
        (F5: the share of the caused change still there, most over .6, little under .3), the decisions and Known weeks."""
        W = self.W; out = []
        for n in range(self.N):
            rings = {r_: dict(total=0.0, largest=None, kept=None, level=None) for r_ in WA_RINGS}
            def big(r_, tot, kept, who):
                rr = rings[r_]; rr["total"] += float(tot)
                if rr["largest"] is None or tot > rr["largest"]["total"]:
                    rr["largest"] = dict(total=round(float(tot), 5), who=who); rr["kept"] = kept
            for k_ in np.nonzero(self.wa_puid[n] >= 0)[0]:
                tot = float(self.wa_ptot[n, k_, 0]) + abs(float(self.wa_ptot[n, k_, 1])) + abs(float(self.wa_ptot[n, k_, 2]))
                kept = None
                if self.uid[n, k_] == self.wa_puid[n, k_]:
                    dv = self.wa_pdir[n, k_].astype(float); dd = float(dv @ dv)
                    if dd > 1e-12:
                        kept = float(np.clip((self.pie[n, k_] - self.wa_pbase[n, k_]) @ dv / dd, 0, 1))
                    elif abs(self.wa_ptot[n, k_, 1]) > 1e-9:
                        kept = float(np.clip((self.c[n, k_] - self.wa_cbase[n, k_, 0]) / self.wa_ptot[n, k_, 1], 0, 1))
                big("person", tot, kept, dict(cid=int(self.wa_puid[n, k_])))
            for j_ in range(self.M):
                tot = float(self.wa_gtot[n, j_].sum())
                if tot <= 0:
                    continue
                dv = self.wa_gdir[n, j_]; dd = float(dv @ dv); kept = None
                if self.skind[n, j_] >= 0 and self.sjoin[n, j_] == self.wa_gjoin[n, j_] and dd > 1e-12:
                    kept = float(np.clip((self.snorm[n, j_] - self.wa_gbase[n, j_]) @ dv / dd, 0, 1))
                big("group", tot, kept, dict(group=GROUP_KINDS[int(self.skind[n, j_])] if self.skind[n, j_] >= 0 else None, j=j_))
            for (unit, key), rec in self.wa_u[n].items():
                r_ = WA_RING_OF[unit]; kept = None
                if rec["dir"] is not None and rec["base"] is not None:
                    dv = rec["dir"]; dd = float(dv @ dv)
                    cur = None
                    if r_ == "place" and getattr(W, "hp_s", None) is not None:
                        cur = W.hp_s.reshape(-1, C)[int(key)]
                    elif r_ == "town_sphere" and getattr(W, "sph_s", None) is not None:
                        cur = W.sph_s[key[0], key[1]]
                    if cur is not None and dd > 1e-12:
                        kept = float(np.clip((cur - rec["base"]) @ dv / dd, 0, 1))
                big(r_, rec["tot"], kept, rec["who"])
            for rr in rings.values():
                rr["total"] = round(rr["total"], 5)
                if rr["kept"] is not None:
                    rr["level"] = WA_KEPT[0] if rr["kept"] > 0.6 else WA_KEPT[2] if rr["kept"] < 0.3 else WA_KEPT[1]
                    rr["kept"] = round(rr["kept"], 3)
            out.append(dict(told=len(self.wa_told[n]), rings=rings, decisions=int(self.wa_ndec[n]),
                            known_weeks=int(self.wa_kweeks[n]), met=float(self.wa_met[n]),
                            by_rung=dict(moved=[round(float(x_), 6) for x_ in self.wa_byr[n]],
                                         weeks=[int(x_) for x_ in self.wa_byw[n]])))
        return out
