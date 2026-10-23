"""People's methods for emigration to other societies, the views for the game, and save and load.

Part of class People (world_people.py), which inherits ViewsMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import sys
import numpy as np
from world_keys import CAST_WANTS, DOMAINS, FEATURES, GROUP_KINDS, RINGS, SACRED_KINDS
from world_people_base import BIT, C, G, GATES, NEVER, R, ROLE, ROLE_ORDER, STATUS, _csum, _norm, _uclip


class ViewsMixin:
    # ------------------------------------------------------------------ other societies: emigration (spec 5 §5)
    def emigrate(self, n, W_new=None, society_id=None, t=None, with_partner=True):
        """Life n emigrates to another society (spec 5 §5; Emren 10:30 "Yes, fully"); returns the new locality.

        With one life (N == 1) the People switch their world to W_new, the neighbour at full detail
        (World.spawn_neighbour(k)), and keep the old World to go back to. With several lives sharing one World
        (N > 1) there is no second world to switch to: only the bookkeeping is done (society id, status, language,
        far ties, the settings left, the class), and the life stays on the shared World's places, rates and
        institutions, which stand in for the new country.

        The life arrives as a migrant: a locality drawn toward cities and work, the family's class one step lower at
        first, a new neighbourhood; every setting is left but online groups (and the household when the partner and
        children come along, with_partner; a child's whole household comes); a few people from the old country are
        met there; a language to learn (lang, from lang0); joining settings and institutions is harder at first
        (openness to migrants, _mig_gate). Everyone left behind stays in the cast as a far contact and fades by the
        distance rules. The engine changes the status (set_status) and adds to the language (lang_boost)."""
        t = self.t if t is None else int(t); P = self.P; rng = self.rng; n = int(n); a = self._age(t)
        sid = society_id if society_id is not None else getattr(W_new, "society_id", None)
        old = int(self.soc[n])
        sid = old + 1 if sid is None else int(sid)
        if sid == old:
            return int(self.loc[n])
        if sid == int(self.soc_home[n]):
            return self.return_home(n, W_new, t, with_partner)
        self._xsoc = True
        self._smem[(n, old)] = (float(self.lang[n]), int(self.stat[n]))
        if old == int(self.soc_home[n]):
            self.loc_home[n] = self.loc[n]; self.cls_home[n] = self.cls[n]
        mates, hh = self._coming(n, a, t, with_partner)
        self._leave_all(n, hh, t, "emigrated")
        # people from the old country met there (drawn from the old society, before the switch)
        nd = int(rng.integers(2, 6))
        ages = _uclip(max(a, 25.0) + rng.normal(0, 8, nd), 1, 90)
        Fd = self._gen(np.full(nd, n), t - (ages * 52).astype(np.int64), t, ctx=np.tile(self.w[n], (nd, 1)), sel=0.2)
        if self.N == 1 and W_new is not None and W_new is not self.W:   # the neighbour at full detail
            self._Ws[old] = self.W
            self._switch(W_new)
        loc = self._arrival_loc()
        self.soc[n] = sid; self.loc[n] = loc; self.arr_t[n] = t
        self.lang[n], self.stat[n] = self._smem.get((n, sid), (float(P["lang0"]), STATUS.index("migrant")))
        self.cls[n] = max(0, int(self.cls_home[n]) - 1)
        self._pick_nb([n])
        self._settle(n, mates, hh, t, a)
        Fd["mloc"] = np.full(nd, loc); Fd["msoc"] = np.full(nd, sid)
        self._add(Fd, t, R["acquaintance"], c0=0.08 + 0.06 * rng.random(nd), trust0=0.55, quiet=True)
        self._arrived(n, t, "emigrated")
        return loc

    def return_home(self, n, W_home=None, t=None, with_partner=True):
        """Life n goes back to the society it was born in (spec 5 §5: return is possible), undoing emigrate(): the
        home World again (N == 1: W_home, or the one kept when leaving), near the parents if they live there, else
        the old locality; citizen, native language, the family's class at least; settings left as on leaving (online
        groups stay; the household comes when the partner and children do); the people at home are near again.
        With N > 1, as for emigrate(), only the bookkeeping. Returns the locality."""
        t = self.t if t is None else int(t); n = int(n); a = self._age(t)
        home = int(self.soc_home[n]); cur = int(self.soc[n])
        if cur == home:
            return int(self.loc[n])
        self._smem[(n, cur)] = (float(self.lang[n]), int(self.stat[n]))
        mates, hh = self._coming(n, a, t, with_partner)
        self._leave_all(n, hh, t, "returned")
        if self.N == 1:
            Wh = W_home if W_home is not None else self._Ws.get(home)
            if Wh is not None and Wh is not self.W:
                self._Ws[cur] = self.W
                self._switch(Wh)
        ps = np.nonzero(self._has_role(n, "parent") & self.lv[n] & (self.msoc[n] == home))[0]
        loc = int(self.mloc[n, ps[0]]) if len(ps) else int(self.loc_home[n])
        loc = int(_uclip(loc, 0, self.n_loc - 1))
        self.soc[n] = home; self.loc[n] = loc; self.arr_t[n] = t
        self.lang[n] = 1.0; self.stat[n] = STATUS.index("citizen")
        self.cls[n] = max(int(self.cls[n]), int(self.cls_home[n]))
        self._pick_nb([n])
        self._settle(n, mates, hh, t, a)
        self._arrived(n, t, "returned")
        return loc

    def set_status(self, n, status):
        """The engine sets life n's status in the society it lives in: "citizen", "migrant" or "resident"."""
        self.stat[int(n)] = STATUS.index(status) if isinstance(status, str) else int(status)

    def lang_boost(self, n, x):
        """The engine adds to life n's language skill (a course, a partner from there): x of what is left to learn."""
        n = int(n); l_ = float(self.lang[n]); l_ += float(_uclip(x, 0, 1)) * (1 - l_)
        self.lang[n] = 1.0 if l_ > 0.995 else l_

    def _lang_step(self, t):
        """Monthly, for lives abroad: language skill grows by exposure (time in settings outside the home), fastest
        in childhood (lang_k); the family's class comes back once the language is good (0.8) and four years have
        passed since arrival. No draws."""
        P = self.P
        ab = np.nonzero(self.lang < 1)[0]
        if len(ab):
            k = float(np.interp(self._age(t), [x_ for x_, _ in P["lang_k"]], [y_ for _, y_ in P["lang_k"]]))
            sk = self.skind[ab]
            es = (self.sts[ab] * ((sk >= 0) & (sk != G["household"]) & (sk != G["online"]))).sum(1)
            ex = 0.3 + 0.7 * np.minimum(1.0, es / 0.35)
            l2 = 1 - (1 - self.lang[ab]) * np.exp(-k * ex * 4 / 52.0)
            self.lang[ab] = np.where(l2 > 0.995, 1.0, l2)
        back = (self.soc != self.soc_home) & (self.cls < self.cls_home) & (self.lang >= 0.8) & (t - self.arr_t >= 4 * 52)
        self.cls[back] = self.cls_home[back]

    def _coming(self, n, a, t, with_partner):
        """Who moves country with life n: a child's whole household; an adult's household when it is their own and
        the partner comes; else the partner and the children under 18 (with_partner). Returns (slots, household kept
        or -1)."""
        hh = int(self.hhj[n])
        if hh >= 0 and (a < 18 or (self.own_home[n] and with_partner)):
            return np.nonzero(self.used[n] & self.lv[n] & (((self.mset[n] >> hh) & 1) > 0))[0], hh
        ks = []
        if with_partner:
            ps = int(self.pslot[n])
            if ps >= 0 and self.lv[n, ps]:
                ks.append(ps)
            ks += np.nonzero(self.used[n] & self.lv[n] & ((self.rmask[n] & BIT["child"]) != 0)
                             & ((t - self.born[n]) < 18 * 52))[0].tolist()
        return np.array(sorted(set(ks)), np.int64), -1

    def _leave_all(self, n, keep, t, why):
        for j_ in range(self.M):
            if self.skind[n, j_] >= 0 and self.skind[n, j_] != G["online"] and j_ != keep:
                self._leave(n, j_, t, why)

    def _switch(self, W):
        """N == 1: the People now live in World W (its places, rates, institutions, generations)."""
        self.W = W; self._coh_tab = None
        self._world_static()
        if getattr(self, "pt_on", False):   # part 2: that world's closings from now on
            self._pt_i = len(getattr(W, "pt_log", None) or [])

    def _arrival_loc(self):
        """A migrant's first locality: population, cities and the capital (where migrants mostly settle), work."""
        wt = self.loc_p.copy()
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        if feat.shape[1] == len(FEATURES):
            wt = wt * (1 + 2.0 * feat[:, [FEATURES.index("capital"), FEATURES.index("city")]].any(1))
        un = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, 0.05)), float)
        wt = wt * np.exp(-8 * (un - un.mean()))
        return int(self.rng.choice(self.n_loc, p=wt / wt.sum()))

    def _settle(self, n, mates, hh, t, a):
        """Those who came along live where life n lives now; a household of their own when the old one was left."""
        self.mloc[n, mates] = self.loc[n]; self.msoc[n, mates] = self.soc[n]
        if hh < 0 and self.hhj[n] < 0 and (a >= 18 or len(mates)):
            j = self._new_setting(n, "household", t)
            self.hhj[n] = j; self.own_home[n] = a >= 18
            if j >= 0:
                self.sanch[n, j] = self.w[n]; self.snorm[n, j] = self.w[n]
                self.mset[n, mates] |= self._bit(j)

    def _arrived(self, n, t, why):
        self.n_moves[n] += 1; self.last_move[n] = t
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="moved", loc=int(self.loc[n]), nb=int(self.nb[n]),
                                    away=True, why=why, society=int(self.soc[n])))
        self._fsh(); self._close_index(); self._alive_counts([n]); self._outputs_settings()

    # ------------------------------------------------------------------ views for the game
    def _kin_links(self, n):
        """Partners and children among life n's cast, by slot: ({slot: partner's cast id or "you"}, {slot: [children's
        cast ids, "you" for the character]}), from the roles, family lines and kof links."""
        u = np.nonzero(self.used[n])[0]
        uid = self.uid[n]; rm = self.rmask[n]; kof = self.kof[n]; born = self.born[n]
        by = {int(uid[k]): int(k) for k in u}
        has = lambda k, r_: bool(int(rm[k]) & BIT[r_])
        par = [int(k) for k in u if has(k, "parent")]
        sib = [int(k) for k in u if has(k, "sibling")]
        kids = [int(k) for k in u if has(k, "child")]
        gps = [int(k) for k in u if has(k, "grandparent")]
        pa, ch = {}, {}
        ps = int(self.pslot[n])
        if ps >= 0 and self.used[n, ps]:
            pa[ps] = "you"
            ch[ps] = [int(uid[k]) for k in kids if int(kof[k]) == int(uid[ps])]
        if len(par) == 2 and not self.par_apart[n]:
            pa[par[0]] = int(uid[par[1]]); pa[par[1]] = int(uid[par[0]])
        for k in par:
            ch[k] = [int(uid[s_]) for s_ in sib] + ["you"]
        for i_, k in enumerate(gps):
            for k2 in gps[i_ + 1:]:
                if self.line[n, k] == self.line[n, k2] and self.fem[n, k] != self.fem[n, k2]:
                    pa.setdefault(k, int(uid[k2])); pa.setdefault(k2, int(uid[k]))
            mine = [p_ for p_ in par if self.line[n, p_] == self.line[n, k]]
            ch[k] = [int(uid[p_]) for p_ in mine] + [int(uid[m_]) for m_ in u if has(m_, "kin") and
                                                       any(int(kof[m_]) == int(uid[p_]) for p_ in mine)]
        # the rest through kof (kin of): someone 15 to 60 years younger is their child; kin about their age, their
        # partner (the partner's own family and friends are kin of the partner, not counted here)
        for m_ in u:
            x_ = by.get(int(kof[m_]))
            if x_ is None or x_ == ps or x_ in par:
                continue
            gap = (int(born[m_]) - int(born[x_])) / 52.0
            if 15 <= gap <= 60:
                ch.setdefault(x_, []).append(int(uid[m_]))
            elif abs(gap) < 15 and has(m_, "kin") and has(x_, "kin"):
                pa.setdefault(int(m_), int(uid[x_])); pa.setdefault(x_, int(uid[m_]))
        return pa, ch

    def cast_view(self, n, t=None, layers=(1, 2, 3, 4), dead=False):
        """The people around life n, closest first: their reading (never the true pie), closeness and trust (the game
        writes the words), their want when the character knows it, weeks since they last met (last_contact, None if
        never), where they live (loc, society), their partner's and children's cast ids ("you" for the character;
        None or [] when not in the cast)."""
        t = self.t if t is None else t; L = self.P["layer_c"]
        out = []
        pa, ch = self._kin_links(n)
        idx = np.nonzero(self.used[n] & (self.lv[n] | dead))[0]
        for k in idx[np.argsort(-self.c[n, idx])]:
            c = float(self.c[n, k])
            layer = 1 if c >= L[0] else 2 if c >= L[1] else 3 if c >= L[2] else 4 if c >= L[3] else 0
            if layer not in layers and not (dead and not self.lv[n, k]):
                continue
            rm = int(self.rmask[n, k])
            out.append(dict(id=int(self.uid[n, k]), name_idx=int(self.nm[n, k]), line=int(self.line[n, k]),
                            sex="female" if self.fem[n, k] else "male",
                            age=int(((t if self.lv[n, k] else self.died_t[n, k]) - self.born[n, k]) // 52),
                            alive=bool(self.lv[n, k]), role=self._rname(n, k), roles=[r_ for r_ in ROLE_ORDER if rm & BIT[r_]],
                            layer=layer, closeness=round(c, 2), trust=round(float(self.trust[n, k]), 2),
                            read=[round(float(x_), 3) for x_ in self.read[n, k]],
                            want=CAST_WANTS[int(self.want[n, k])] if self.want[n, k] >= 0 and self.wknown[n, k] else None,
                            standing=int(self.stand[n, k]), here=bool(self._here(n, k)),
                            owes=int(self.debt[n, k]), face=bool(self.face[n, k]),
                            last_contact=None if self.last[n, k] <= NEVER // 2 else int(t - self.last[n, k]),
                            loc=int(self.mloc[n, k]), society=int(self.msoc[n, k]),
                            partner=pa.get(int(k)), children=list(ch.get(int(k), []))))
        return out

    def place_view(self, n):
        W = self.W; l = int(self.loc[n])
        kk = self._wf("loc_kind_key", None)
        kind = kk[l] if kk is not None else np.asarray(self._wf("loc_kind", np.zeros(self.n_loc)))[l]
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        fl = [FEATURES[i_] for i_ in np.nonzero(feat[l])[0]] if feat.shape[1] == len(FEATURES) else []
        pv = dict(loc=l, nb=int(self.nb[n]), kind=kind.item() if hasattr(kind, "item") else kind, features=fl,
                  cls=int(self.cls[n]), own_home=bool(self.own_home[n]), moves=int(self.n_moves[n]),
                  society=int(self.soc[n]), home_society=int(self.soc_home[n]), status=STATUS[int(self.stat[n])],
                  lang=round(float(self.lang[n]), 2))
        if getattr(self, "eyes_on", False):   # S3, S4 (only when on): "your places", their faces and the life's name there
            pv["places"] = self.eyes_info(n)
        if getattr(self, "land", None) is not None:   # v25 lane D (wa_land): the portrait's land row, and the life's
            pv.update(self.land.place(n))               # ways and bridges
            pv.update(self.land.person(n))
        if getattr(self, "nat", None) is not None:   # v25 lane D (wa_nat_climb): national standing, its kinds apart
            pv["national"] = self.nat.view(n)
        return pv

    def figure_view(self, n, W=None):
        """The public figures in role (World W, default the People's): id, role (index; role_name when the world
        names them), party, standing, and their colors as life n reads them (spec 5 §6: only the character's reading,
        never the true pie): half what they show, the character's lens and a fixed personal slant."""
        W = self.W if W is None else W
        try:
            role = np.asarray(W.fig_role, np.int64); pie = np.asarray(W.fig_pie, float).reshape(-1, C)
            stn = np.asarray(W.fig_standing, float); alive = np.asarray(W.fig_alive, bool)
        except AttributeError:
            return []
        act = np.asarray(getattr(W, "fig_active", alive), bool)
        party = getattr(W, "fig_party", None); party = None if party is None else np.asarray(party, np.int64)
        names = getattr(sys.modules.get(type(W).__module__), "FIG_ROLES", None)
        out = []
        for f_ in np.nonzero(alive & act)[0].tolist():
            x_ = np.sin((f_ + 1) * 12.9898 + np.arange(C) * 78.233 + n * 0.618034 + self.run_seed * 0.414214) * 43758.5453
            sl_ = _norm((x_ - np.floor(x_) + 0.2)[self.perm])   # drawn in the canonical color frame, then relabelled
            rd = _norm(0.5 * pie[f_] + 0.3 * self.lens[n] + 0.2 * sl_)
            out.append(dict(id=int(f_), role=int(role[f_]),
                            role_name=names[int(role[f_])] if names is not None and 0 <= role[f_] < len(names) else None,
                            party=int(party[f_]) if party is not None and f_ < len(party) else -1,
                            standing=round(float(stn[f_]), 2), read=[round(float(v_), 3) for v_ in rd]))
        return out

    def settings_view(self, n):
        """The character's groups: kind, time share, cohesion, rank, members and leader, and their ways as the
        character reads them (the members' reading blended with what the group openly praises)."""
        out = []
        for j in np.nonzero(self.skind[n] >= 0)[0]:
            mem = np.nonzero(((self.mset[n] >> j) & 1).astype(bool) & self.used[n] & self.lv[n])[0]
            seen = _norm(0.5 * self.snorm[n, j] + 0.5 * (self.read[n, mem].mean(0) if len(mem) else self.snorm[n, j]))
            ld = int(self.slead[n, j])
            out.append(dict(j=int(j), kind=GROUP_KINDS[int(self.skind[n, j])], time_share=round(float(self.sts[n, j]), 3),
                            cohesion=round(float(self.scoh[n, j]), 2), rank=round(float(self.srank[n, j]), 2),
                            members=[int(x_) for x_ in self.uid[n, mem]], size=int(self.ssize[n, j]),
                            leader="you" if ld == -2 else (int(self.uid[n, ld]) if ld >= 0 and self.used[n, ld] else None),
                            gate=GATES[int(self.sgate[n, j])], exit_cost=round(float(self.sxcost[n, j]), 2),
                            years=int((self.t - self.sform[n, j]) // 52), ways=[round(float(x_), 3) for x_ in seen]))
        return out

    def reach_view(self, n):
        # felt and hint are 0 to 1 (reach level / 3): felt is the character's sense; hint is reality only as a rough
        # step (spec 7 §6): three steps, 0 (none), .5 (some: reach 1 or 2), 1 (full)
        return dict(rings=list(RINGS), standing=[int(x_) for x_ in self.standing[n]],
                    felt=[round(float(x_) / 3, 2) for x_ in self.felt_reach[n]],
                    hint=[round(round(float(x_) / 3 * 2) / 2, 2) for x_ in self.reach[n]],
                    domains=list(DOMAINS), domain_standing=[int(x_) for x_ in self.dstanding[n]],
                    domain_hint=[round(round(float(x_) / 3 * 2) / 2, 2) for x_ in self.dreach[n]])

    # ------------------------------------------------------------------ save and load
    _CAST_F = ("uid", "nm", "line", "kof", "role", "rmask", "face", "born", "fem", "since", "died_t", "c", "cmax", "trust",
               "last", "debt", "mgood", "mbad", "secret", "brk", "health", "money", "mcls", "emp", "sector", "inst", "mpart",
               "nkids", "mood", "want", "wripe", "wstate", "wknown", "wdue", "stand", "mloc", "faith", "party", "strict",
               "fbiz", "fkin", "fkin_far", "mset", "lv", "msoc")
    _SET_F = ("skind", "scoh", "srank", "sts", "ssize", "sncast", "sgate", "sxcost", "sform", "sjoin", "sref", "slead")
    _PER_F = ("loc", "nb", "cls", "pfaith", "pparty", "pline", "hhj", "own_home", "pslot", "psector", "n_moves", "last_move",
              "par_change", "older_sib", "younger_sib", "vol_tgt", "fr_bias", "sociab", "unext", "female", "soc", "soc_home",
              "stat", "lang", "arr_t", "cls_home", "loc_home", "par_apart")

    def save(self, n, w=None, alive=True):
        """One life's cast, settings and place as a JSON-safe dict (w: the character's own pie, for a legacy line)."""
        py = lambda v_: v_.item() if hasattr(v_, "item") else v_
        ks = np.nonzero(self.used[n])[0]
        cast = []
        for k in ks:
            d = {f_: py(getattr(self, f_)[n, k]) for f_ in self._CAST_F}
            d["slot"] = int(k); d["pie"] = [float(x_) for x_ in self.pie[n, k]]; d["read"] = [float(x_) for x_ in self.read[n, k]]
            d["roles"] = [r_ for r_ in ROLE if int(self.rmask[n, k]) & BIT[r_]]; d["alive"] = bool(self.lv[n, k])
            cast.append(d)
        sets = []
        for j in range(self.M):
            d = {f_: py(getattr(self, f_)[n, j]) for f_ in self._SET_F}
            d["snorm"] = [float(x_) for x_ in self.snorm[n, j]]; d["sanch"] = [float(x_) for x_ in self.sanch[n, j]]
            sets.append(d)
        per = {f_: py(getattr(self, f_)[n]) for f_ in self._PER_F}
        per["family_mix"] = [float(x_) for x_ in self.family_mix[n]]; per["objk"] = [float(x_) for x_ in self.objk[n]]
        per["smem"] = [[int(s_), float(l_), int(st_)] for (n_, s_), (l_, st_) in sorted(self._smem.items()) if n_ == n]
        out = dict(version=2, world_seed=self.seed, run_seed=self.run_seed, t=int(self.t), t0=int(self.t0), K=self.K, M=self.M,
                   loc=int(self.loc[n]), cls=int(self.cls[n]), cast=cast, settings=sets, person=per,
                   self=dict(born=int(self.t0), fem=bool(self.female[n]), alive=bool(alive),
                             pie=None if w is None else [float(x_) for x_ in np.asarray(w, float)], nm=0, line=int(self.pline[n]),
                             mloc=int(self.loc[n]), mcls=int(self.cls[n]), faith=int(self.pfaith[n])),
                   nh=[[float(x_) for x_ in v_] for v_ in self.nh])
        if self.N == 1:
            out["rng"] = self.rng.bit_generator.state
        if self.sph_h or self.sph_hr or self.sph_mk:   # spheres phase 2 (only when on: off, a life saves as v22.2 saved it)
            out["spheres"] = dict(mark=[float(x_) for x_ in self.mark[n]], mark_yr=int(self._mark_yr),
                                  mark_wear=float(self.mark_wear[n]), mark_z=[float(x_) for x_ in self.mark_z[n]], hnt=[int(x_) for x_ in self.hnt[n]], shnt=[int(x_) for x_ in self.shnt[n]],
                                  rung=[float(x_) for x_ in self.rung[n]], ryrs=[float(x_) for x_ in self.ryrs[n]],
                                  hpick=int(self.hpick), rung_yr=int(getattr(self, "_rung_yr", -1)),
                                  hrng=self._hrng.bit_generator.state if self.N == 1 else None)
        if getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False):   # phase 4 (only when on)
            out["spheres4"] = dict(fair=[float(x_) for x_ in self.fair[n]], p4_yr=int(self._p4_yr),
                                   fair_log=[[int(r_[0]), int(r_[2]), int(r_[3])] for r_ in self.fair_log if r_[1] == n])
            if getattr(self, "fr_read", False):   # S1 (only when on): the town events read
                out["spheres4"]["fr_i"] = int(self._fr_i)
                out["spheres4"]["fr_n"] = [float(x_) for x_ in self._fr_n]
        ca_, sa_ = getattr(self, "care_load", None), getattr(self, "sh_around", None)
        cm_ = getattr(self, "comrade", None)
        if ca_ is not None or sa_ is not None or cm_ is not None:   # phase 5 (only once on): this month's care load and
            out["spheres5"] = dict(care_load=None if ca_ is None else float(ca_[n]),   # shadow around them, the comrades
                                   sh_around=None if sa_ is None else [float(x_) for x_ in sa_[n]],
                                   comrade=None if cm_ is None else [int(k_) for k_ in np.nonzero(cm_[n])[0]],
                                   roots=None if getattr(self, "roots", None) is None else bool(self.roots[n]),
                                   care_buy=None if getattr(self, "care_buy", None) is None else bool(self.care_buy[n]))
        im_ = getattr(self, "inmate", None)
        if im_ is not None:   # part 4 (only when on): the fellow inmates' slots and when they were made
            ks_ = np.nonzero(im_[n])[0]
            out["inmate"] = dict(k=[int(k_) for k_ in ks_], t=[int(x_) for x_ in self.inmate_t[n, ks_]])
        if self.far_on:   # far_ties (only when on): the town events read, and each slot's last far event and stay
            ks_ = np.nonzero(self.far_t[n] != NEVER)[0]
            out["far"] = dict(i=int(self._far_i), k=[int(k_) for k_ in ks_], ev=[int(x_) for x_ in self.far_ev[n, ks_]],
                              t=[int(x_) for x_ in self.far_t[n, ks_]], sg=[int(x_) for x_ in self.far_sg[n, ks_]],
                              sd=[[int(y_) for y_ in x_] for x_ in self.far_sd[n, ks_]],
                              inn=[int(x_) for x_ in self.far_in[n, ks_]], frm=[int(x_) for x_ in self.far_from[n, ks_]],
                              rng=self._far_rng.bit_generator.state if self.N == 1 else None)
        if getattr(self, "p_wid", None) is not None:   # F7 one_roll (only once set): a partner the world took, not yet ended
            out["p_wid"] = bool(self.p_wid[n])
        if getattr(self, "eyes_on", False):   # S3, S4 (only when on): the places, the names there, the moments waiting, kept-apart pairs
            ev_ = dict(key=[int(x_) for x_ in self.eyes_key[n]], rep=[float(x_) for x_ in self.eyes_rep[n]],
                       t0=[int(x_) for x_ in self.eyes_t0[n]], gob=[bool(x_) for x_ in self.eyes_gob[n]],
                       lr=[float(x_) for x_ in self.eyes_lr[n]], la=[int(x_) for x_ in self.eyes_la[n]],
                       dip=float(self.eyes_dip[n]), bel=float(self.eyes_bel[n]), last=int(self.eyes_last[n]),
                       apart=[r_[1:] for r_ in self.eyes_apart if r_[0] == n], q=self.eyes_q.get(n),
                       m=self._eyes_m, qt=self._eyes_qt, yr=int(self._eyes_yr), ev_i=int(self._eyes_ev_i),
                       rng=self._eyes_rng.bit_generator.state if self.N == 1 else None)
            if self.odd_on:
                ev_.update(odd_now=[bool(x_) for x_ in self.odd_now[n]], odd_y=[int(x_) for x_ in self.odd_y[n]],
                           odd_stage=[int(x_) for x_ in self.odd_stage[n]], odd_blend=[bool(x_) for x_ in self.odd_blend[n]],
                           odd_held=[bool(x_) for x_ in self.odd_held[n]], dw=[float(x_) for x_ in self.eyes_dw[n]],
                           odd_lmu=[float(x_) for x_ in self.odd_mu[n]], odd_lvar=[float(x_) for x_ in self.odd_var[n]],
                           odd_n=int(self.odd_n[n]))
            out["eyes"] = ev_
        if getattr(self, "lw", False):   # S7 lead_ways (only when on): the life's posts, held and ended, and their moments
            out["lead"] = dict(posts=[dict(p_) for p_ in self.lw_posts if p_["n"] == n],   # (plain numbers already)
                               ended=[dict(p_) for p_ in self.lw_ended if p_["n"] == n],
                               due=[list(d_) for d_ in self.lw_due if d_[0] == n], q=int(self._lw_q), ev_i=int(self._lw_ev_i),
                               back=[[int(k_[1]), int(v_)] for k_, v_ in self._lw_back.items() if k_[0] == n],
                               has=[bool(x_) for x_ in self.lw_has[n]],
                               rng=self._lw_rng.bit_generator.state if self.N == 1 else None)
        if self.sac_on:   # S5 (only when on): the lines, the record that forms them, offers and amends waiting, wounds
            out["sacred"] = dict(i=int(self._sac_i), lm=int(self._sac_lm), line=self.sac_line[n].tolist(),
                                 t=self.sac_t[n].tolist(), wound=self.sac_wound[n].tolist(), held=self.sac_held[n].tolist(),
                                 crossed=self.sac_crossed[n].tolist(), paid=self.sac_paid[n].tolist(),
                                 lead=int(self.sac_lead[n]), lead_t=int(self.sac_lead_t[n]),
                                 lead_y=[float(x_) for x_ in self.sac_lead_y[n]], lost=[float(x_) for x_ in self.sac_lost[n]],
                                 tragic=int(self.sac_tragic[n]), q=[dict(x_) for x_ in self.sac_q.get(n, [])],
                                 ref=[[k_, v_] for (n_, k_), v_ in self.sac_ref.items() if n_ == n],
                                 am=[[j_, v_] for (n_, j_), v_ in self.sac_am.items() if n_ == n],
                                 lines=[SACRED_KINDS[int(k_)] for k_ in self.sac_line[n] if k_ >= 0],   # (for the sheet)
                                 rng=self._sac_rng.bit_generator.state if self.N == 1 else None)
        if getattr(self, "bt_on", False):   # body_trust (only when on)
            out["btrust"] = self.bt_save(n)
        if self.seen_on:   # seen_done (only when on): the paths seen, by title name; the colour ways; what each slot was
            ti_ = np.nonzero((self.sd_e[n] != 0) | (self.sd_f[n] > 0) | (self.sd_top[n] != -1))[0]   # credited at
            ks_ = np.nonzero(self.used[n] & ((self._sd_w[n] > 0).any(1) | (self._sd_wc[n] > 0)))[0]
            out["seen"] = dict(e={self.sd_names[i_]: [float(self.sd_e[n, i_]), float(self.sd_f[n, i_]), int(self.sd_top[n, i_]),
                                                      float(self.sd_topw[n, i_]), int(self.sd_topk[n, i_])] for i_ in ti_.tolist()},
                               ec=[float(x_) for x_ in self.sd_ec[n]], fc=[float(x_) for x_ in self.sd_fc[n]],
                               ctop=[int(x_) for x_ in self.sd_ctop[n]], ctopw=[float(x_) for x_ in self.sd_ctopw[n]],
                               ctopk=[int(x_) for x_ in self.sd_ctopk[n]],
                               figs=sorted(int(f_) for f_ in self._sd_figs), li=int(self._sd_li), k=[int(k_) for k_ in ks_],
                               w=[[float(y_) for y_ in self._sd_w[n, k_]] for k_ in ks_.tolist()],
                               wc=[float(self._sd_wc[n, k_]) for k_ in ks_.tolist()])
        return out

    @classmethod
    def load(cls, W, saved, run_seed=None, cfg=None):
        """Lives saved by save() continue in World W (one dict, or a list of them: one per life)."""
        saved = [saved] if isinstance(saved, dict) else list(saved)
        d0 = saved[0]
        cfg = dict(cfg or {}); cfg.setdefault("K", d0["K"]); cfg.setdefault("M", d0["M"])
        pp = cls(W, len(saved), d0["run_seed"] if run_seed is None else run_seed,
                 female=[d_["person"]["female"] for d_ in saved], cfg=cfg)
        pp.t0 = int(d0["t0"]); pp.t = int(d0["t"]); pp._last_lives = pp.t
        for n, d in enumerate(saved):
            per = dict(d["person"])
            if int(d.get("version", 1)) < 2 and "sociab" not in per:   # version 1 kept sociability as "soc"
                per["sociab"] = per.pop("soc", 1.0)
            for f_ in cls._PER_F:
                if f_ in per:   # (fields added since a save keep their defaults)
                    getattr(pp, f_)[n] = per[f_]
            if "cls_home" not in per:
                pp.cls_home[n] = pp.cls[n]; pp.loc_home[n] = pp.loc[n]
            for s_, l_, st_ in per.get("smem", []):
                pp._smem[(n, int(s_))] = (float(l_), int(st_))
            pp.family_mix[n] = per["family_mix"]; pp.objk[n] = per["objk"]
            for m_ in d["cast"]:
                k = m_["slot"]; pp.used[n, k] = True
                for f_ in cls._CAST_F:
                    if f_ in m_:
                        getattr(pp, f_)[n, k] = m_[f_]
                pp.pie[n, k] = m_["pie"]; pp.read[n, k] = m_["read"]
            for j, s_ in enumerate(d["settings"]):
                for f_ in cls._SET_F:
                    getattr(pp, f_)[n, j] = s_[f_]
                pp.snorm[n, j] = s_["snorm"]; pp.sanch[n, j] = s_["sanch"]
        if any("p_wid" in d_ for d_ in saved):   # F7 one_roll: a partner the world took, not yet ended (_sync)
            pp.p_wid = np.array([bool(d_.get("p_wid", False)) for d_ in saved])
        pp.nh = [np.asarray(v_, float) for v_ in d0.get("nh", [])]
        pp._psq = _csum(pp.pie * pp.pie).astype(np.float32)
        pp._xsoc = bool((pp.soc != pp.soc_home).any() or ((pp.msoc != pp.soc[:, None]) & pp.used).any())
        if len(saved) == 1 and "rng" in d0:
            pp.rng.bit_generator.state = d0["rng"]
        if pp.sph_h or pp.sph_hr or pp.sph_mk:
            for n, d in enumerate(saved):
                sp_ = d.get("spheres")
                if sp_:
                    pp.mark[n] = sp_.get("mark", [0.0] * C); pp._mark_yr = int(sp_.get("mark_yr", -1))
                    pp.mark_wear[n] = sp_.get("mark_wear", 0.0); pp.mark_z[n] = sp_.get("mark_z", [0.0, 0.0])
                    pp.hnt[n] = sp_["hnt"]; pp.shnt[n] = sp_["shnt"]; pp.rung[n] = sp_["rung"]; pp.ryrs[n] = sp_["ryrs"]
                    pp.hpick = int(sp_["hpick"]); pp._rung_yr = int(sp_["rung_yr"])
                    if len(saved) == 1 and sp_.get("hrng"):
                        pp._hrng.bit_generator.state = sp_["hrng"]
        if getattr(pp, "sph_lv", False) or getattr(pp, "sph_fr", False):
            for n, d in enumerate(saved):
                s4_ = d.get("spheres4")
                if s4_:
                    pp.fair[n] = s4_["fair"]; pp._p4_yr = int(s4_["p4_yr"])
                    pp.fair_log += [[t_, n, j_, v_] for t_, j_, v_ in s4_["fair_log"]]
                    if getattr(pp, "fr_read", False) and "fr_i" in s4_:
                        pp._fr_i = int(s4_["fr_i"])
                        if "fr_n" in s4_:
                            pp._fr_n = np.asarray(s4_["fr_n"], float)
        if any(d.get("spheres5") for d in saved):
            for n, d in enumerate(saved):
                s5_ = d.get("spheres5") or {}
                if s5_.get("care_load") is not None:
                    if getattr(pp, "care_load", None) is None:
                        pp.care_load = np.zeros(pp.N)
                    pp.care_load[n] = s5_["care_load"]
                if s5_.get("sh_around") is not None:
                    if getattr(pp, "sh_around", None) is None:
                        pp.sh_around = np.zeros((pp.N, C))
                    pp.sh_around[n] = s5_["sh_around"]
                if s5_.get("comrade") is not None and getattr(pp, "comrade", None) is not None:
                    pp.comrade[n, s5_["comrade"]] = True
                if s5_.get("roots") is not None and getattr(pp, "roots", None) is not None:
                    pp.roots[n] = bool(s5_["roots"])
                if s5_.get("care_buy") is not None and getattr(pp, "care_buy", None) is not None:
                    pp.care_buy[n] = bool(s5_["care_buy"])
        if getattr(pp, "inmate", None) is not None:   # part 4: the fellow inmates
            for n, d in enumerate(saved):
                im_ = d.get("inmate")
                if im_:
                    pp.inmate[n, im_["k"]] = True; pp.inmate_t[n, im_["k"]] = im_["t"]
        if pp.far_on:
            for n, d in enumerate(saved):
                f_ = d.get("far")
                if f_:
                    pp._far_i = int(f_["i"]); ks_ = np.asarray(f_["k"], np.int64)
                    if len(ks_):
                        pp.far_ev[n, ks_] = f_["ev"]; pp.far_t[n, ks_] = f_["t"]; pp.far_sg[n, ks_] = f_["sg"]
                        pp.far_sd[n, ks_] = f_["sd"]; pp.far_in[n, ks_] = f_["inn"]; pp.far_from[n, ks_] = f_["frm"]
                    if f_.get("rng") is not None and pp.N == 1:
                        pp._far_rng.bit_generator.state = f_["rng"]
        if pp.eyes_on:
            for n, d in enumerate(saved):
                e_ = d.get("eyes")
                if not e_:
                    continue
                pp.eyes_key[n] = e_["key"]; pp.eyes_rep[n] = e_["rep"]; pp.eyes_t0[n] = e_["t0"]; pp.eyes_gob[n] = e_["gob"]
                pp.eyes_lr[n] = e_["lr"]; pp.eyes_la[n] = e_["la"]
                pp.eyes_dip[n] = e_["dip"]; pp.eyes_bel[n] = e_["bel"]; pp.eyes_last[n] = e_["last"]
                pp.eyes_apart += [[n] + list(r_) for r_ in e_["apart"]]
                if e_.get("q"):
                    pp.eyes_q[n] = dict(e_["q"])
                pp._eyes_m = e_["m"]; pp._eyes_qt = e_["qt"]; pp._eyes_yr = int(e_["yr"]); pp._eyes_ev_i = int(e_["ev_i"])
                if pp.N == 1 and e_.get("rng") is not None:
                    pp._eyes_rng.bit_generator.state = e_["rng"]
                if pp.odd_on and "odd_now" in e_:
                    pp.odd_now[n] = e_["odd_now"]; pp.odd_y[n] = e_["odd_y"]; pp.odd_stage[n] = e_["odd_stage"]
                    pp.odd_blend[n] = e_["odd_blend"]; pp.odd_held[n] = e_["odd_held"]; pp.eyes_dw[n] = e_["dw"]
                    if "odd_lmu" in e_:   # what they are used to, in log shares (older saves: read afresh from their next year at places)
                        pp.odd_mu[n] = e_["odd_lmu"]; pp.odd_var[n] = e_["odd_lvar"]; pp.odd_n[n] = int(e_["odd_n"])
        if getattr(pp, "lw", False):
            for n, d in enumerate(saved):
                l_ = d.get("lead")
                if l_:
                    ids_ = {}   # each life's posts take new ids (lives saved apart may share them)
                    for p_ in l_["posts"] + l_["ended"]:
                        ids_[p_["id"]] = pp._lw_next
                        p_ = dict(p_, n=n, id=pp._lw_next); pp._lw_next += 1
                        (pp.lw_posts if p_.get("end_t") is None else pp.lw_ended).append(p_)
                    pp.lw_due += [[n, d_[1], ids_.get(d_[2], -1), d_[3]] for d_ in l_["due"]]
                    pp._lw_q = int(l_["q"]); pp.lw_has[n] = l_["has"]; pp._lw_ev_i = int(l_.get("ev_i", pp._lw_ev_i))
                    pp._lw_back.update({(n, int(k_)): int(v_) for k_, v_ in l_["back"]})
                    if l_.get("rng") is not None and pp.N == 1:
                        pp._lw_rng.bit_generator.state = l_["rng"]
        if pp.sac_on:
            for n, d in enumerate(saved):
                s_ = d.get("sacred")
                if s_:
                    pp._sac_i = int(s_["i"]); pp._sac_lm = int(s_["lm"])
                    pp.sac_line[n] = s_["line"]; pp.sac_t[n] = s_["t"]; pp.sac_wound[n] = s_["wound"]
                    pp.sac_held[n] = s_["held"]; pp.sac_crossed[n] = s_["crossed"]; pp.sac_paid[n] = s_["paid"]
                    pp.sac_lead[n] = s_["lead"]; pp.sac_lead_t[n] = s_["lead_t"]; pp.sac_lead_y[n] = s_["lead_y"]
                    pp.sac_lost[n] = s_["lost"]; pp.sac_tragic[n] = s_["tragic"]
                    if s_["q"]:
                        pp.sac_q[n] = [dict(x_) for x_ in s_["q"]]
                    pp.sac_ref.update({(n, k_): int(v_) for k_, v_ in s_["ref"]})
                    pp.sac_am.update({(n, int(j_)): int(v_) for j_, v_ in s_["am"]})
                    if s_.get("rng") is not None and pp.N == 1:
                        pp._sac_rng.bit_generator.state = s_["rng"]
        if pp.seen_on:   # seen_done: the cast as loaded is the cast last read (no change is seen at the next quarter)
            lv_ = pp.used & pp.lv
            pp._sd_uid = np.where(lv_, pp.uid, -1).astype(np.int32)
            pp._sd_emp = pp.emp.copy(); pp._sd_mp = pp.mpart.copy(); pp._sd_nk = pp.nkids.copy(); pp._sd_st = pp.stand.copy()
            pp._sd_saved = {}
            for n, d in enumerate(saved):
                s_ = d.get("seen")
                if s_:
                    pp._sd_saved[n] = s_["e"]; pp.sd_ec[n] = s_["ec"]; pp.sd_fc[n] = s_["fc"]
                    pp.sd_ctop[n] = s_["ctop"]; pp.sd_ctopw[n] = s_["ctopw"]; pp.sd_ctopk[n] = s_["ctopk"]
                    pp._sd_figs.update(s_["figs"]); pp._sd_li = int(s_["li"])
                    ks_ = np.asarray(s_["k"], np.int64)
                    if len(ks_):
                        pp._sd_w[n, ks_] = s_["w"]; pp._sd_wc[n, ks_] = s_["wc"]
        if getattr(pp, "bt_on", False):   # body_trust: the trust, the parents' mean, what was read
            for n, d in enumerate(saved):
                b_ = d.get("btrust")
                if b_:
                    pp.btrust[n] = [np.nan if x_ is None else x_ for x_ in b_["v"]]
                    pp.bt_par[n] = [np.nan if x_ is None else x_ for x_ in b_["par"]]
                    pp.bt_kind[n] = int(b_["kind"]); pp.bt_lean[n] = float(b_.get("lean", 0.0)); pp._bt_i = int(b_["i"]); pp._bt_li = int(b_["li"]); pp._bt_yr = int(b_["yr"])
                    if b_.get("rng") is not None and pp.N == 1:
                        pp._bt_rng.bit_generator.state = b_["rng"]
        pp._fsh(); pp._close_index(); pp._alive_counts(np.arange(pp.N)); pp._outputs_settings()
        return pp
