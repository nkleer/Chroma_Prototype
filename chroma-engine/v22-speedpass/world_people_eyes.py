"""People's methods for approval, standing and reach, their places' eyes and the odd one out (S3, S4), and what the
engine reads each week.

Part of class People (world_people.py), which inherits EyesMixin; moved out of world_people.py verbatim. A method here
reads module names through the imports below, the same objects world_people.py has, and self for everything on the
People."""
import numpy as np
from library import COLORS
from world_keys import DOMAINS, HAUNT_KINDS, NORM_KEYS, SPHERES, CAUGHT_TAGS as WK_CAUGHT, ODD_TAGS as WK_ODD
from world_people_base import (C, EYES_DEFAULT, EYES_ENEMY, EYES_G, EYES_LEAVE, G, HAUNT_SPH, K_XC, MON, NEVER, NNORM,
    REACH, RING_OF, _EPS6, _csum, _isin_small, _logit, _norm, _sig, _uclip)


class EyesMixin:
    # ------------------------------------------------------------------ approval, standing, reach (spec 2 §3, spec 7)
    # ------------------------------------------------------------------ S3 their places' eyes, S4 the odd one out
    def _eyes_init(self, wp_):
        """S3 (sph_eyes; chroma-ideas/social-mechanics.md, "Their places' eyes"): each life's places are slots, its three
        haunts first (aligned with People.hnt), then its settings (aligned with the setting slots) of kind work,
        congregation or unit that no haunt holds. Per slot: the place's key (a haunt's flat place id; a setting's join week
        x 16 + kind), the life's name there (rep, -1..1), the week it became theirs and whether they are a go-between
        there (a bridge that worked); a slot whose place changes starts again at 0. S4 (sph_odd) adds per slot: the odd
        one out now, years held in a row, the life stage its moment last came in, blended in. Moments are picked from
        its own random stream only."""
        import sphere_data as SD
        N, Q = self.N, 3 + self.M
        R = SD.PLACE_READ
        self.eyes_par = {**EYES_DEFAULT, **dict(wp_.get("eyes_par") or {})}
        self._eyes_R = R
        self._eyes_tab = np.asarray(R["table"], float)[self.perm][:, self.perm]   # place face x act colour, this frame
        self._eyes_inv = np.argsort(self.perm)   # W U B R G -> this frame's index (faces in colour order: fc[..., _eyes_inv])
        self.eyes_key = np.full((N, Q), -1, np.int64)
        self.eyes_rep = np.zeros((N, Q)); self.eyes_t0 = np.zeros((N, Q), np.int64); self.eyes_gob = np.zeros((N, Q), bool)
        self.eyes_lr = np.zeros((N, Q)); self.eyes_la = np.full((N, Q), -1, np.int64)   # the last reading there, its act's lead
        self.eyes_dip = np.zeros(N)          # belonging a place given up still costs (S3's buffer), fading
        self.eyes_bel = np.zeros(N)          # belonging lost this month to S3 and S4 (the dip, kept-apart strain, contrast)
        self.eyes_apart = []                 # [life, slot a, slot b, key a, key b]: two places kept apart (S3)
        self.eyes_q = {}                     # life -> the caught-between or odd-one-out moment waiting for them
        self.eyes_off = {}                   # life -> the last one offered (for the game's slots, after it is met)
        self.eyes_last = np.full(N, NEVER, np.int64)   # the week of the last caught-between moment met
        self._eyes_rng = np.random.default_rng([self.seed, 91, self.run_seed])
        self._eyes_fc = np.full((N, Q, C), 1.0 / C); self._eyes_sp = np.full((N, Q), -1, np.int64)
        self._eyes_m = None; self._eyes_qt = None; self._eyes_yr = -1
        lg_ = getattr(self.W, "sph_ev_log", None); self._eyes_ev_i = 0 if lg_ is None else len(lg_)   # town events read
        ask = np.zeros((len(SD.EV), C))      # each sphere event's ask: its own sphere's row faces (W U B R G, signed)
        for i_, e_ in enumerate(SD.EV):
            for r_ in e_["rows"]:
                if r_["target"] == e_["sphere"] and r_["faces"]:
                    ask[i_] += r_["faces"]
        ask /= np.maximum(np.abs(ask).sum(1, keepdims=True), 1e-9)
        self._eyes_opp = (ask @ np.asarray(R["table"], float) @ ask.T) <= self.eyes_par["ev_opp"]   # asks read opposed
        self._eyes_evsph = np.array([SPHERES.index(e_["sphere"]) for e_ in SD.EV], np.int64)
        self._eyes_stages = list(SD.TIME_AGES)
        z = lambda: np.zeros(C)              # the checks' counts by lead colour (W U B R G), not saved
        self.eyes_stats = dict(drep=z(), nrep=z(), acts={}, talk=0, caught={}, caught_why={}, caught_tag={},
                               life_years=z(), place_years=z(), odd_years=z(), odd_fired=z(), blend=z(), hold=z(), leave=z(),
                               held=z(), gaps=np.zeros(16, np.int64))   # gaps: the widest between two places' readings of an act, by .1
        if self.odd_on:   # S4's years at a place, odd-one-out years and conversions per life (x lead colour), for the check's
            self.eyes_stats.update(life_place=np.zeros((N, C)), life_odd=np.zeros((N, C)), life_held=np.zeros((N, C)),   # shuffle reading
                                   life_movable=np.zeros((N, C)), movable_years=np.zeros(C))
        if self.odd_on:
            self.odd_now = np.zeros((N, Q), bool); self.odd_y = np.zeros((N, Q), np.int64)
            self.odd_stage = np.full((N, Q), -1, np.int64); self.odd_blend = np.zeros((N, Q), bool)
            self.odd_held = np.zeros((N, Q), bool)
            self.odd_mu = np.zeros((N, C)); self.odd_var = np.zeros((N, C))   # what they are used to (log shares, this frame's colours)
            self.odd_n = np.zeros(N, np.int64)   # years of their own places in it
            self.eyes_dw = np.zeros((N, C))  # blending in: the colours' step for the engine to apply (pie units, then cleared)

    def _eyes_places(self):
        """S3: (key, faces, sphere) of every life's place slots (N, 3 + M): the haunts, then the settings of kind work,
        congregation or unit not held at a haunt (key -1: no place). Faces in this world's frame: a haunt's World.hp_s, a
        setting's ways (snorm)."""
        W = self.W; N, Q = self.N, 3 + self.M
        key = np.full((N, Q), -1, np.int64); fc = np.full((N, Q, C), 1.0 / C); sp = np.full((N, Q), -1, np.int64)
        hp = getattr(W, "hp_s", None)
        if self.sph_h and hp is not None:
            h = self.hnt; ok = h >= 0
            key[:, :3] = np.where(ok, h, -1)
            fc[:, :3] = np.where(ok[..., None], hp.reshape(-1, C)[np.maximum(h, 0)], 1.0 / C)
            sp[:, :3] = np.where(ok, HAUNT_SPH[(np.maximum(h, 0) // hp.shape[2]) % len(HAUNT_KINDS)], -1)
        sk = self.skind.astype(np.int64); ok = _isin_small(sk, EYES_G)
        if self.sph_h:
            ok &= self.shnt < 0
        key[:, 3:] = np.where(ok, self.sjoin * 16 + sk, -1)
        fc[:, 3:] = np.where(ok[..., None], self.snorm, 1.0 / C)
        sp[:, 3:] = np.where(ok, self.set_sphere, -1)
        return key, fc, sp

    def _eyes_sync(self, t):
        """S3: the places read again. A haunt that moved slot keeps its name; a place given up is left: S3's buffer (its
        exit cost, KT's, a haunt's a club's, x its share of their places, as belonging lost and fading) and S4's
        hardening (a misfit leaving a haunt: its leading face + odd_harden); its slot starts again."""
        key, fc, sp = self._eyes_places()
        self._eyes_fc, self._eyes_sp = fc, sp
        old = self.eyes_key
        if (key == old).all():
            return
        N, Q = self.N, 3 + self.M
        eq = (key[:, :3, None] == old[:, None, :3]) & (key[:, :3, None] >= 0)
        hk = eq.any(2); src = np.where(hk, eq.argmax(2), np.arange(3)[None, :])
        keep = np.zeros((N, Q), bool); keep[:, :3] = hk; keep[:, 3:] = (key[:, 3:] == old[:, 3:]) & (key[:, 3:] >= 0)
        stay = np.concatenate([((old[:, :3, None] == key[:, None, :3]) & (old[:, :3, None] >= 0)).any(2), keep[:, 3:]], 1)
        gone = (old >= 0) & ~stay
        if gone.any():
            self._eyes_left(gone, old, t)
        st = [self.eyes_rep, self.eyes_t0, self.eyes_gob, self.eyes_lr, self.eyes_la]
        if self.odd_on:
            st += [self.odd_now, self.odd_y, self.odd_stage, self.odd_blend, self.odd_held]
        ar = np.arange(N)[:, None]
        for a_ in st:
            a_[:, :3] = a_[ar, src]
        new = ~keep
        self.eyes_rep[new] = 0.0; self.eyes_t0[new] = t; self.eyes_gob[new] = False; self.eyes_lr[new] = 0.0; self.eyes_la[new] = -1
        if self.odd_on:
            self.odd_now[new] = False; self.odd_y[new] = 0; self.odd_stage[new] = -1; self.odd_blend[new] = False
            self.odd_held[new] = False
        self.eyes_key = key

    def _eyes_left(self, gone, old, t):
        P_ = self.eyes_par; W = self.W
        nv = (old >= 0).sum(1)
        for n, q in zip(*np.nonzero(gone & ~self.dead[:, None])):
            xc = P_["buf_haunt"] if q < 3 else float(K_XC[int(old[n, q]) % 16])
            self.eyes_dip[n] += xc / max(int(nv[n]), 1)
            if self.odd_on and q < 3 and self.odd_now[n, q] and getattr(W, "hp_s", None) is not None:
                l, h, i = (int(x_) for x_ in np.unravel_index(int(old[n, q]), W.hp_s.shape[:3]))
                hp = W.hp_s[l, h, i]
                W._sph_place_set(l, h, i, W._sph_nudge(hp, np.eye(C)[int(np.argmax(hp))], P_["odd_harden"]))

    def _eyes_gobs(self, idx):
        """S3: the go-between at each of lives idx's place slots (cast slot, -1 none): the living leader of the setting
        that is the place, or of a setting held at the haunt (the go-betweens of _haunts_month, N4)."""
        E = len(idx); out = np.full((E, 3 + self.M), -1, np.int64)
        ld = self.slead[idx]
        ld = np.where((ld >= 0) & self.lv[idx[:, None], np.maximum(ld, 0)], ld, -1)
        out[:, 3:] = np.where(self.eyes_key[idx, 3:] >= 0, ld, -1)
        if self.sph_h:
            hn = self.hnt[idx]; sh = self.shnt[idx]
            m = (sh[:, None, :] == hn[:, :, None]) & (hn[:, :, None] >= 0) & (ld[:, None, :] >= 0)
            out[:, :3] = np.where(m.any(2), ld[np.arange(E)[:, None], m.argmax(2)], -1)
        return out

    def _eyes_lead(self, n, q):
        """The leading face of life n's place slot q, as an index of W U B R G."""
        return int(self.perm[int(np.argmax(self._eyes_fc[n, q]))])

    def eyes_see(self, idx, ma, q, kind="act"):
        """S3 (sph_eyes): lives idx did an act with colours ma (E, C), success q (E,: 1 it worked, 0 it failed, .5
        neither, as a leaving); kind a short word ("act", "title", "title lost", "left job", "left partner", "left
        faith", "crime", or a caller's own, as S5's). Each of their places reads it by its faces (sphere_data.PLACE_READ:
        own colour 1, ally .4, enemy -.4, by face share and act share; + .3 on success, - .3 on failure; a leaving or a
        title lost reads the colours walked away from, negated) and their name there moves act_w x the reading (x1.5
        where they are the odd one out, S4). Each go-between at one of their places carries it to their other places at
        .5 (PLACE_READ talk), read by the go-between's own colours (one story line, kind "talk"). Two places reading it
        more than .6 apart (caught_gap) wait to catch them between (a cast_want: caught moment). Returns the gaps found,
        [(life, slot a, slot b, gap)]. Off (eyes_on False), nothing."""
        if not self.eyes_on:
            return []
        idx = np.atleast_1d(np.asarray(idx, np.int64)); E = len(idx)
        if not E:
            return []
        ma = _norm(np.asarray(ma, float).reshape(E, C)); q = np.broadcast_to(np.asarray(q, float), (E,)).astype(float)
        lv_ = ~self.dead[idx]
        idx, ma, q = idx[lv_], ma[lv_], q[lv_]; E = len(idx)
        if not E:
            return []
        t = self.t; P_ = self.eyes_par; R = self._eyes_R
        self._eyes_sync(t)
        sg = -1.0 if kind in EYES_LEAVE else 1.0
        out = np.where(q > 0.5, R["success"], np.where(q < 0.5, R["failure"], 0.0))
        tm = ma @ self._eyes_tab.T                                # (E, C): how each face reads the act's colours
        ok = self.eyes_key[idx] >= 0
        r = sg * np.einsum("eqf,ef->eq", self._eyes_fc[idx], tm) + out[:, None]
        vis = np.where(self.odd_now[idx], P_["odd_vis"], 1.0) if self.odd_on else 1.0
        d = P_["act_w"] * r * ok * vis
        gb = self._eyes_gobs(idx); hg = (gb >= 0) & ok
        rg = np.zeros(gb.shape)
        if hg.any():   # talk: each go-between's own reading, to the life's other places at half weight
            pg = self.pie[idx[:, None], np.maximum(gb, 0)].astype(float)
            rg = np.where(hg, sg * np.einsum("eqf,ef->eq", pg, tm) + out[:, None], 0.0)
            d = d + P_["act_w"] * R["talk"] * (rg.sum(1, keepdims=True) - rg) * ok * vis
        old = self.eyes_rep[idx]
        new = _uclip(old + d, R["rep_range"][0], R["rep_range"][1])
        self.eyes_rep[idx] = new
        self.eyes_lr[idx] = np.where(ok, r, self.eyes_lr[idx])
        self.eyes_la[idx] = np.where(ok, self.perm[np.argmax(ma, 1)][:, None], self.eyes_la[idx])
        st = self.eyes_stats; lc = self.perm[np.argmax(self.w[idx], 1)]
        np.add.at(st["drep"], lc, ((new - old) * ok).sum(1)); np.add.at(st["nrep"], lc, ok.sum(1))
        st["acts"][kind] = st["acts"].get(kind, 0) + E
        # the lines the game writes (Library: earth_spheres.READ["X.Y"], X the reading place's leading face, Y the act's
        # leading colour, its gift clause for a reading above 0, its danger clause below; earth_spheres.TALK good, bent,
        # warn): one "eyes_read" event per act with every place's reading, one "talk" event for the strongest go-between
        ac = [COLORS[int(self.perm[int(np.argmax(ma[e_]))])] for e_ in range(E)]
        side = lambda v_: "gift" if v_ > 0 else "danger" if v_ < 0 else None
        for e_ in range(E):
            n_ = int(idx[e_])
            if not self.watch[n_] or not ok[e_].any():
                continue
            sp_ = self.setting_places(n_) if ok[e_, 3:].any() else []   # once per life, not once per setting slot
            self.events.append(dict(n=n_, t=int(t), kind="eyes_read", about=kind, act=ac[e_], worked=float(q[e_]),
                                    reads=[dict(place=self._eyes_desc(n_, int(x_), sp_), face=COLORS[self._eyes_lead(n_, int(x_))],
                                                side=side(r[e_, x_]), reading=round(float(r[e_, x_]), 3),
                                                rep=round(float(new[e_, x_]), 3)) for x_ in np.nonzero(ok[e_])[0]]))
        for e_ in np.nonzero(hg.any(1) & (ok.sum(1) >= 2))[0]:   # the story line: the strongest go-between's word
            n_ = int(idx[e_]); st["talk"] += 1
            if not self.watch[n_]:
                continue
            qf = int(np.argmax(np.where(hg[e_], np.abs(rg[e_]), -1.0)))
            r0, r1 = float(r[e_, qf]), float(rg[e_, qf])   # the place's reading, and the go-between's own as they carry it
            talk = "bent" if r0 * r1 < 0 else "good" if r0 > 0 else "warn"
            self.events.append(dict(n=n_, t=int(t), kind="talk", about=kind, go=int(self.uid[n_, gb[e_, qf]]),
                                    place=self._eyes_desc(n_, qf), face=COLORS[self._eyes_lead(n_, qf)], act=ac[e_],
                                    side=side(r0), told=side(r1), talk=talk,
                                    to=[self._eyes_desc(n_, int(x_)) for x_ in np.nonzero(ok[e_])[0] if x_ != qf]))
        gaps = []
        for e_ in np.nonzero(ok.sum(1) >= 2)[0]:   # caught between: two places that read it far apart
            qs = np.nonzero(ok[e_])[0]; rr = r[e_, qs]
            hi_, lo_ = int(qs[np.argmax(rr)]), int(qs[np.argmin(rr)])
            gp_ = float(rr.max() - rr.min())
            self.eyes_stats["gaps"][min(int(gp_ * 10), 15)] += 1
            if gp_ > R["caught_gap"]:
                gaps.append((int(idx[e_]), hi_, lo_, gp_))
                self._eyes_queue_caught(int(idx[e_]), hi_, lo_, "act", t)
        return gaps

    def _eyes_pair(self, n, qa, qb):
        """S3: the enemy pair life n's places qa and qb split on, as indices of W U B R G (qa's colour first): of the five
        enemy pairs, the one whose two colours the places hold most oppositely, each colour's gap read in its own scale
        (the faces' difference over the root of their mean share, as a chi-square reads two mixes). Two places read an act
        apart through their enemy colours (the reading's -.4; allies read alike), so that pair is what the life is caught
        between. Not each place's leading face: the places share their town's lean (about half of them lead Green), so two
        leading faces named that lean, not the pull (v22.4 fix round: the pairs with Green came three times as often as WB)."""
        fa, fb = self._eyes_fc[n, qa][self._eyes_inv], self._eyes_fc[n, qb][self._eyes_inv]
        pk_ = self.eyes_par["pair_k"]
        d_ = (fa - fb) / (np.sqrt(np.maximum(0.5 * (fa + fb), 1e-9)) if pk_ == 0.5 else np.maximum(0.5 * (fa + fb), 1e-9) ** pk_)
        if self.eyes_par["pair_norm"] > 0:   # each pair's gap against its usual gap (S3: a pair wide everywhere is no split)
            g_ = np.array([abs(d_[p_[0]] - d_[p_[1]]) for p_ in EYES_ENEMY])
            pg_ = getattr(self, "_eyes_pg", None)
            pg_ = g_.copy() if pg_ is None else pg_
            i_, j_ = EYES_ENEMY[int(np.argmax(g_ / np.maximum(pg_, 1e-9)))]
            self._eyes_pg = (1 - self.eyes_par["pair_norm"]) * pg_ + self.eyes_par["pair_norm"] * g_
        else:
            i_, j_ = max(EYES_ENEMY, key=lambda p_: abs(d_[p_[0]] - d_[p_[1]]))
        return (i_, j_) if d_[i_] >= d_[j_] else (j_, i_)

    def _eyes_queue_caught(self, n, qa, qb, why, t):
        """S3: a caught-between moment waits for life n (one at a time, cool weeks after the last met): its pair is the enemy
        pair the two places split on (_eyes_pair); place a is the one holding more of the pair's first colour in W U B R G
        order (WB, WR, UR, UG, BG)."""
        if n in self.eyes_q or t - self.eyes_last[n] < self.eyes_par["cool"] or qa == qb:
            return
        la, lb = self._eyes_pair(n, qa, qb)
        if lb < la:
            qa, qb, la, lb = qb, qa, lb, la
        self.eyes_q[n] = dict(key="caught", slots=[int(qa), int(qb)], keys=[int(self.eyes_key[n, qa]), int(self.eyes_key[n, qb])],
                              t=int(t), why=why, pair=COLORS[la] + COLORS[lb])
        cw = self.eyes_stats["caught_why"]; cw[why] = cw.get(why, 0) + 1

    def eyes_due(self, t=None):
        """S3, S4: the moments waiting this week, [(life, cast id or -1, "caught" or "odd")]: a caught-between moment
        with a go-between of either place in its first who: slot (place a's, else b's; -1 when neither has one), an
        odd-one-out moment with no holder (-1). One whose places changed, or that waited past wait weeks unmet, is dropped."""
        t = self.t if t is None else t; out = []
        for n, it in list(self.eyes_q.items()):
            if self.dead[n] or t - it["t"] > self.eyes_par["wait"] or any(self.eyes_key[n, q_] != k_ for q_, k_ in zip(it["slots"], it["keys"])):
                del self.eyes_q[n]; continue
            cid = -1
            if it["key"] == "caught":
                gb = self._eyes_gobs(np.array([n]))[0]
                for q_ in it["slots"]:
                    if gb[q_] >= 0:
                        cid = int(self.uid[n, gb[q_]]); break
            self.eyes_off[n] = it
            out.append((int(n), cid, it["key"]))
        return out

    def eyes_sphere(self, n):
        """S4: the sphere (index into SPHERES) of the place of life n's odd-one-out moment offered this week: a haunt's
        kind's, a setting's (set_sphere: a congregation faith, a unit prot, work its employer's sector; a setting held at a
        haunt is the haunt's); -1 none."""
        it = self.eyes_off.get(n)
        if it is None or it["key"] != "odd":
            return -1
        return int(self._eyes_sp[n, it["slots"][0]])

    def eyes_bridge_ok(self, n):
        """S3: the waiting caught-between moment's bridge is open: the life's rung is known or higher in both places'
        spheres (sph_hours' rungs; without them never)."""
        it = self.eyes_q.get(n)
        if it is None or it["key"] != "caught" or getattr(self, "rung", None) is None or not self.sph_hr:
            return False
        return all(self._eyes_sp[n, q_] >= 0 and np.floor(self.rung[n, self._eyes_sp[n, q_]]) >= 2 for q_ in it["slots"])

    def odd_hold_x(self, n):
        """S4: the log-odds an unplayed life adds to holding on (and takes off blending in) at the place of its waiting
        odd-one-out moment: hold_k x ((lead share - .2) / .2 in 0..1 + rung there / 4 - 1)."""
        it = self.eyes_q.get(n)
        if it is None or it["key"] != "odd":
            return 0.0
        q_ = it["slots"][0]; sp_ = self._eyes_sp[n, q_]
        rg = float(np.floor(self.rung[n, sp_])) if getattr(self, "rung", None) is not None and sp_ >= 0 else 0.0
        return self.eyes_par["hold_k"] * (float(np.clip((self.w[n].max() - 0.2) / 0.2, 0, 1)) + rg / 4 - 1)

    def eyes_resolve(self, n, key, code, succ=True, idle=False):
        """S3, S4: the waiting moment was met with an option tagged code (world_keys.CAUGHT_TAGS or ODD_TAGS; -1 none or
        doing nothing: kept apart, held on). Caught: side_a / side_b, that place's name + step, the other's - step, and felt
        fairness in the other's sphere - fair (sph_fair); bridge (only open at known or higher in both), worked: both +
        step and a go-between at both, failed: both - step; apart: nothing now, strain on belonging while both last;
        back: both - back. Odd: blend, their colours step odd_blend toward the place (eyes_dw) and its strain ends; hold,
        their ways kept; leave, they leave the place as leaving is built (a haunt dropped and its setting left; a setting
        left). Returns the event."""
        it = self.eyes_q.get(n)
        if it is None or it["key"] != key:
            return None
        del self.eyes_q[n]
        if any(self.eyes_key[n, q_] != k_ for q_, k_ in zip(it["slots"], it["keys"])):
            return None
        t = self.t; P_ = self.eyes_par; R = self._eyes_R; st = self.eyes_stats
        if key == "caught":
            tag = WK_CAUGHT[code] if 0 <= code < len(WK_CAUGHT) and not idle else "apart"
            a, b = it["slots"]
            if tag == "bridge" and not all(self._eyes_sp[n, q_] >= 0 and getattr(self, "rung", None) is not None
                                           and np.floor(self.rung[n, self._eyes_sp[n, q_]]) >= 2 for q_ in (a, b)):
                tag = "apart"
            rp = self.eyes_rep; s_ = P_["step"]
            if tag in ("side_a", "side_b"):
                w_, l_ = (a, b) if tag == "side_a" else (b, a)
                rp[n, w_] += s_; rp[n, l_] -= s_
                if getattr(self, "fair", None) is not None and self.sph_fr and self._eyes_sp[n, l_] >= 0:
                    j_ = self._eyes_sp[n, l_]; self.fair[n, j_] = max(0.0, self.fair[n, j_] - P_["fair"])
            elif tag == "bridge":
                rp[n, [a, b]] += s_ if succ else -s_
                if succ:
                    self.eyes_gob[n, [a, b]] = True
            elif tag == "apart":
                self.eyes_apart.append([int(n), int(a), int(b), int(it["keys"][0]), int(it["keys"][1])])
            elif tag == "back":
                rp[n, [a, b]] -= P_["back"]
            rp[n] = _uclip(rp[n], R["rep_range"][0], R["rep_range"][1])
            self.eyes_last[n] = t
            st["caught"][it["pair"]] = st["caught"].get(it["pair"], 0) + 1
            st["caught_tag"][tag] = st["caught_tag"].get(tag, 0) + 1
            ev = dict(n=int(n), t=int(t), kind="caught", tag=tag, worked=bool(succ), pair=it["pair"], why=it["why"],
                      place_a=self._eyes_desc(n, a), place_b=self._eyes_desc(n, b))
        else:
            tag = WK_ODD[code] if 0 <= code < len(WK_ODD) and not idle else "hold"
            q_ = it["slots"][0]; lc = int(self.perm[int(np.argmax(self.w[n]))])
            desc = self._eyes_desc(n, q_)
            if tag == "blend":
                dd = self._eyes_fc[n, q_] - self.w[n]; tv = 0.5 * np.abs(dd).sum()
                self.eyes_dw[n] += dd * min(1.0, P_["odd_blend"] / max(tv, 1e-9))
                self.odd_blend[n, q_] = True; st["blend"][lc] += 1
            elif tag == "leave":
                self._eyes_exit(n, q_, t); st["leave"][lc] += 1
            else:
                st["hold"][lc] += 1
            ev = dict(n=int(n), t=int(t), kind="odd", tag=tag, place=desc)
        if self.watch[n]:
            self.events.append(ev)
        return ev

    def _eyes_exit(self, n, q, t):
        """S4's leave: a haunt is dropped (and a setting held there left), a setting is left (as leaving is built: the life
        course may find another of its kind)."""
        if q < 3:
            p_ = int(self.hnt[n, q]); self.hnt[n, q] = -1
            for j_ in np.nonzero(self.shnt[n] == p_)[0]:
                self._leave(int(n), int(j_), t, "left")
        else:
            self._leave(int(n), int(q - 3), t, "left")

    def _eyes_desc(self, n, q, sp=None):
        """Life n's place slot q for the game: a haunt as World.place_info gives it, a setting as setting_places does (sp:
        setting_places(n) when the caller has it already)."""
        if self.eyes_key[n, q] < 0:
            return None
        if q < 3:
            return dict(self.W.place_info(int(self.eyes_key[n, q])), slot=int(q))
        for d_ in (self.setting_places(n) if sp is None else sp):
            if d_["slot"] == q - 3:
                return dict(d_, slot=int(q), setting=int(q - 3))
        return None

    def eyes_moment(self, n):
        """S3, S4: the slots of life n's caught-between moment ({place_a}, {place_b}, and the opposed pair, place a led by
        its first colour) or odd-one-out moment ({place}), as the game names them; None without one."""
        it = self.eyes_off.get(n)
        if it is None:
            return None
        if it["key"] == "caught":
            return dict(key="caught", pair=it["pair"], why=it["why"], place_a=self._eyes_desc(n, it["slots"][0]),
                        place_b=self._eyes_desc(n, it["slots"][1]))
        return dict(key="odd", place=self._eyes_desc(n, it["slots"][0]))

    def eyes_info(self, n):
        """S3, S4 for the game's "your places": each place with its leading face (a colour letter), the life's name there
        (rep -1..1, a word: "liked" at .25 or more, "talked about" at -.25 or less), the last act it read (act: its
        leading colour; side: "gift" or "danger", the sign of the reading: earth_spheres.READ["face.act"]), whether they
        are a go-between there, and (S4) the odd one out there, blended in, held on three years."""
        if not self.eyes_on:
            return []
        out = []
        for q_ in np.nonzero(self.eyes_key[n] >= 0)[0]:
            r_ = float(self.eyes_rep[n, q_])
            lr_ = float(self.eyes_lr[n, q_]); la_ = int(self.eyes_la[n, q_])
            d_ = dict(place=self._eyes_desc(n, int(q_)), face=COLORS[self._eyes_lead(n, int(q_))], rep=round(r_, 3),
                      word="liked" if r_ >= 0.25 else "talked about" if r_ <= -0.25 else None, go_between=bool(self.eyes_gob[n, q_]),
                      act=COLORS[la_] if la_ >= 0 else None, side="gift" if lr_ > 0 and la_ >= 0 else "danger" if lr_ < 0 else None)
            if self.odd_on:
                d_.update(odd=bool(self.odd_now[n, q_]), blended=bool(self.odd_blend[n, q_]), held=bool(self.odd_held[n, q_]))
            out.append(d_)
        return out

    def _eyes_rungs(self):
        """(N, 3 + M) the life's rung (0 newcomer .. 4 leader) in each place slot's sphere (0 without rungs)."""
        sp = self._eyes_sp
        if getattr(self, "rung", None) is None:
            return np.zeros(sp.shape, np.int64)
        return _uclip(np.floor(np.take_along_axis(self.rung, np.maximum(sp, 0), 1)), 0, 4).astype(np.int64)

    def _eyes_rung_mult(self):
        """(N, 9) twice: how fast the rungs climb (up) and fall (down) in each sphere: a good name at their places there
        (their mean) x rung_good, a bad one x rung_bad (S3); x odd_vis both ways where they are the odd one out (S4)."""
        R = self._eyes_R; N = self.N; ok = self.eyes_key >= 0; sp = np.where(ok, self._eyes_sp, -1)
        up = np.ones((N, 9)); dn = np.ones((N, 9))
        for j_ in range(9):
            m_ = sp == j_
            c_ = m_.sum(1)
            mr = (self.eyes_rep * m_).sum(1) / np.maximum(c_, 1)
            up[:, j_] = np.where(c_ > 0, np.where(mr > 0, R["rung_good"], np.where(mr < 0, R["rung_bad"], 1.0)), 1.0)
            if self.odd_on:
                od = (m_ & self.odd_now).any(1)
                up[:, j_] *= np.where(od, self.eyes_par["odd_vis"], 1.0); dn[:, j_] *= np.where(od, self.eyes_par["odd_vis"], 1.0)
        return up, dn

    def _odd_press(self):
        """S4: x odd_press on the pull of each place where the life is the odd one out and has not blended in: (N, M) for
        the settings (one held at such a haunt too), (N, 3) for the haunts."""
        P_ = self.eyes_par; on = self.odd_now & ~self.odd_blend
        mh = np.where(on[:, :3], P_["odd_press"], 1.0); ms = np.where(on[:, 3:], P_["odd_press"], 1.0)
        if self.sph_h:
            hit = (self.shnt[:, :, None] == self.hnt[:, None, :]) & (self.shnt[:, :, None] >= 0) & on[:, None, :3]
            ms = np.where(hit.any(2), P_["odd_press"], ms)
        return ms, mh

    def _eyes_month(self, t):
        """Monthly (S3, S4): the places read again; names fade (half in PLACE_READ half_life years), and a left place's
        cost to belonging (half in buf_half weeks); kept-apart pairs strain belonging while both last; each quarter, two
        of their places in whose spheres the town's events of the season ask opposite things (their asks read through the
        place reading at ev_opp or below) wait to catch them between; once a year of age, S4's odd one out."""
        self._eyes_sync(t)
        P_ = self.eyes_par; R = self._eyes_R
        dm = 4 if self._eyes_m is None else t - self._eyes_m; self._eyes_m = t
        self.eyes_rep *= 0.5 ** (dm / (52.0 * R["half_life"]))
        self.eyes_dip *= 0.5 ** (dm / P_["buf_half"])
        strain = np.zeros(self.N); keep = []
        for r_ in self.eyes_apart:
            n, a, b, ka, kb = r_
            if self.eyes_key[n, a] == ka and self.eyes_key[n, b] == kb and not self.dead[n]:
                keep.append(r_); strain[n] += P_["strain"]
        self.eyes_apart = keep
        if self._eyes_qt is None or t - self._eyes_qt >= 13:
            self._eyes_qt = t; self._eyes_season(t)
        con = np.zeros(self.N)
        if self.odd_on:
            if int(self._age(t)) != self._eyes_yr:
                self._eyes_yr = int(self._age(t)); self._odd_year(t)
            on = self.odd_now & ~self.odd_blend
            if on.any():
                con = P_["odd_contrast"] * (np.asarray(P_["odd_rung"])[self._eyes_rungs()] * on).sum(1)
        self.eyes_bel = self.eyes_dip + strain + con

    def _eyes_season(self, t):
        lg = getattr(self.W, "sph_ev_log", None)
        if lg is None or not len(lg):
            return
        rows = lg[self._eyes_ev_i:]; self._eyes_ev_i = len(lg)
        rows = rows[rows[:, 0] > t - 13]
        if len(rows) < 2:
            return
        ok = self.eyes_key >= 0
        for n in np.nonzero(~self.dead & (ok.sum(1) >= 2))[0]:
            if n in self.eyes_q or t - self.eyes_last[n] < self.eyes_par["cool"]:
                continue
            ev = np.unique(rows[(rows[:, 2] == self.loc[n]) | (rows[:, 2] < 0), 1])
            hit = []
            for e_ in ev:
                qs = np.nonzero(ok[n] & (self._eyes_sp[n] == self._eyes_evsph[e_]))[0]
                if len(qs):
                    hit.append((int(e_), int(qs[0])))
            done = False
            for i_ in range(len(hit)):
                for j_ in range(i_ + 1, len(hit)):
                    if hit[i_][1] != hit[j_][1] and self._eyes_opp[hit[i_][0], hit[j_][0]]:
                        self._eyes_queue_caught(int(n), hit[i_][1], hit[j_][1], "events", t); done = True; break
                if done:
                    break

    def _odd_year(self, t):
        """Yearly (S4, sph_odd): the odd one out at a place, a year or more there, with two or more such places: their lead
        colour's share of its faces sits more than odd_z spreads under what they are used to (each colour's mean share at
        their places, and its spread among them, a running mean over their years, odd_mem a year; first read after a year
        of it). Not under a fixed share of every place's faces: the places share their town's lean (most lean Green, work
        places and congregations are near-even mixes leaning White and Green), so a fixed share made Red-led lives the odd
        one out 25 times as often as Green-led ones (v22.4 fix round); a life is read against its own places, the same in
        a batch as alone in the game. Shares are read in proportion (log share): a colour common at their places spreads
        wider below its mean than a rare one, which cannot fall far, so read in plain shares Green-led lives were odd most
        and Red-led least (s4_odd 1.20x on the v22.4 refit). With odd_vmem (v22.5) the spread is learnt over a life: with
        two places and the spread of these two alone, the lower sits exactly one spread under the mean, so "odd" turned on
        whether that place had drifted down lately (a newcomer's workplace for White- and Green-led lives, whose faiths lean
        their way; a steady congregation for Blue- and Black-led ones). Its moment waits once a life stage per place (never after blending in there). Held
        odd_hold years in a row (odd, not blended), the place leans toward their colour by their rung there a year
        (odd_lean: a haunt's faces, through World's place setter; a setting's ways), and its regulars' colours
        odd_regular a year toward theirs."""
        P_ = self.eyes_par; W = self.W; live = ~self.dead; N = self.N
        lead = np.argmax(self.w, 1)
        lf = np.log(np.maximum(self._eyes_fc, 1e-6))   # the faces' shares in proportion (log share)
        share = np.take_along_axis(lf, lead[:, None, None], 2)[..., 0]
        el = (self.eyes_key >= 0) & live[:, None] & ((t - self.eyes_t0) >= 52)   # their places, a year or more theirs
        ne = el.sum(1); ar = np.arange(N)
        used = self.odd_mu[ar, lead] - P_["odd_z"] * np.sqrt(self.odd_var[ar, lead])
        odd = el & ((ne >= 2) & (self.odd_n > 0))[:, None] & (share < used[:, None])
        fc_ = np.where(el[..., None], lf, 0.0)
        mu = fc_.sum(1) / np.maximum(ne, 1)[:, None]
        var = (np.where(el[..., None], lf - mu[:, None, :], 0.0) ** 2).sum(1) / np.maximum(ne, 1)[:, None]
        hv = (ne > 0)[:, None]; k_ = np.where(self.odd_n > 0, P_["odd_mem"], 1.0)[:, None]
        self.odd_mu = np.where(hv, self.odd_mu + k_ * (mu - self.odd_mu), self.odd_mu)
        kv_ = k_ if P_["odd_vmem"] is None else np.where(self.odd_n > 0, P_["odd_vmem"], 1.0)[:, None]   # the spread (v22.5)
        self.odd_var = np.where(hv, self.odd_var + kv_ * (var - self.odd_var), self.odd_var)
        self.odd_n += ne > 0
        self.odd_now = odd
        self.odd_y = np.where(odd & ~self.odd_blend, self.odd_y + 1, 0)
        st = self.eyes_stats; lc = self.perm[lead]
        pl, oo = el.any(1), live & odd.any(1)
        np.add.at(st["life_years"], lc[live], 1); np.add.at(st["place_years"], lc[pl], 1); np.add.at(st["odd_years"], lc[oo], 1)
        st["life_place"][ar[pl], lc[pl]] += 1; st["life_odd"][ar[oo], lc[oo]] += 1
        rg = self._eyes_rungs()   # years at a place they could move: held odd_hold years past the first, a regular or more
        mv = (el & ((t - self.eyes_t0) >= 52 * (1 + P_["odd_hold"])) & (np.asarray(P_["odd_lean"])[rg] > 0)).any(1)
        np.add.at(st["movable_years"], lc[mv], 1); st["life_movable"][ar[mv], lc[mv]] += 1
        sg = self._eyes_stages.index(self._tstage(self._age(t))) if self._tstage(self._age(t)) in self._eyes_stages else -2
        cand = odd & ~self.odd_blend & (self.odd_stage != sg)
        for n in np.nonzero(cand.any(1))[0]:
            if n in self.eyes_q:
                continue
            q_ = int(np.argmax(cand[n])); self.odd_stage[n, q_] = sg
            self.eyes_q[n] = dict(key="odd", slots=[q_], keys=[int(self.eyes_key[n, q_])], t=int(t), why="odd")
            st["odd_fired"][lc[n]] += 1
        held = odd & ~self.odd_blend & (self.odd_y >= P_["odd_hold"])
        self.odd_held = held
        if not held.any():
            return
        for n, q_ in zip(*np.nonzero(held)):
            k_ = float(P_["odd_lean"][rg[n, q_]]); e_ = np.eye(C)[lead[n]]
            if k_ > 0:   # a conversion is a place that moves: a newcomer (odd_lean 0) holding out moves nothing
                st["held"][lc[n]] += 1; st["life_held"][n, lc[n]] += 1
            if q_ < 3:
                p_ = int(self.eyes_key[n, q_])
                if k_ > 0 and getattr(W, "hp_s", None) is not None:
                    l, h, i = (int(x_) for x_ in np.unravel_index(p_, W.hp_s.shape[:3]))
                    old_ = W.hp_s[l, h, i].copy() if self.wa_l else None
                    W._sph_place_set(l, h, i, W._sph_nudge(W.hp_s[l, h, i], e_, k_))
                    if self.wa_l:   # the world answers, D: the place the odd one out moved
                        self._wa_place(n, l, h, i, old_, W.hp_s[l, h, i], t, what="holding out")
                js = np.nonzero(self.shnt[n] == p_)[0]
            else:
                js = [q_ - 3]
                if k_ > 0:
                    sn0_ = self.snorm[n, q_ - 3].astype(float)
                    self.snorm[n, q_ - 3] = _norm(self.snorm[n, q_ - 3] + k_ * (e_ - self.snorm[n, q_ - 3])).astype(np.float32)
                    if self.wa_l:
                        self._wa_gmove(n, q_ - 3, t, dnorm=self.snorm[n, q_ - 3] - sn0_, what="holding out")
            for j_ in js:
                mem = np.nonzero(self.used[n] & self.lv[n] & ((self.mset[n] & self._bit(int(j_))) > 0))[0]
                if len(mem):
                    pm0_ = self.pie[n, mem].astype(float) if self.wa_l else None
                    self.pie[n, mem] = _norm(self.pie[n, mem] + P_["odd_regular"] * (self.w[n] - self.pie[n, mem])).astype(np.float32)
                    if self.wa_l:
                        self._wa_pmove(np.full(len(mem), n), mem, t, col=self.pie[n, mem] - pm0_, what="holding out")
                    self._psq[n, mem] = _csum(self.pie[n, mem] ** 2)

    def _norm_hist(self, t):
        v = np.zeros(NNORM)
        for i_, k_ in enumerate(NORM_KEYS):
            try:
                v[i_] = float(self.W.norm(k_))
            except Exception:
                v[i_] = 0.5
        self.nh.append(v)

    def _approval(self, t):
        """Acceptance per norm key as the character feels it, minus the society's: PP.approval, so that
        W.norm(key) + PP.approval is the acceptance where the character lives and among their own people. The local
        norm is the members' acceptance in the character's groups by time share (older and stricter members lag);
        the close circle (layers 1-2, by closeness^2) weighs in up to circle_w; a close person's strong disapproval of
        an act of the character's (objk) comes off it and fades."""
        P = self.P; N = self.N; L2 = P["layer_c"][1]
        if not self.nh:
            self._norm_hist(t)
        nh = np.array(self.nh); lnh = _logit(nh)
        now = lnh[-1]
        tsw = self.sts * (self.skind >= 0)
        accs = _sig(now[None, None, :] - 1.2 * self.sstrict[..., None])
        tt = tsw.sum(1, keepdims=True)
        self.local_norm = np.where(tt > 0, (tsw[..., None] * accs).sum(1) / np.maximum(tt, 1e-9), nh[-1][None, :])
        fi = self._fi; f32 = np.float32
        cc = np.take(self.c, fi)
        ok = np.take(self.used, fi) & np.take(self.lv, fi) & (cc >= L2)
        qf = _uclip((np.take(self.born, fi).astype(np.int64) + 20 * 52 - self.t0) // 13, 0, len(nh) - 1)
        # each close person's acceptance (N, KC, NNORM; float32, the whole close index, weighted 0 where not close):
        # half the norms now, half those when they were 20, less their strictness, plus a fixed personal view
        z = (0.5 * lnh).astype(f32)[qf]; z += (0.5 * now).astype(f32); z -= f32(1.2) * np.take(self.strict, fi)[..., None]
        z += _EPS6[np.take(self.nm, fi) % len(_EPS6)]
        acc = _sig(z)
        wc = np.where(ok, cc * cc, f32(0)).astype(f32); sw = wc.sum(1)
        circle = np.where(sw[:, None] > 0, np.einsum("nk,nkj->nj", wc, acc) / np.maximum(sw, 1e-9)[:, None], self.local_norm)
        wcl = (P["circle_w"] * sw / (sw + 1.0))[:, None]
        dt = (t - self._last_appr) / 52.0 if self._last_appr is not None else 0.0
        self.objk *= 0.5 ** (dt / P["obj_half"]); self._last_appr = t
        self.approval = _uclip((1 - wcl) * self.local_norm + wcl * circle - self.objk, 0, 1) - nh[-1][None, :]

    def _standing(self, t):
        """Standing per domain and per ring (spec 7 §2: a famous actor has national standing in culture and ordinary
        standing in the economy): money, the standing of the innermost circle (one level below theirs), a wide
        network, rank in groups and movements hold for every domain of their ring; titles count in their own domain
        (S["domain_standing"], one level 0-3 per domain) or, when the engine sends only S["title_standing"], in
        every outer ring (one level, or one per ring). A ring's standing is its best domain's; reach from the table,
        per ring (self.reach) and per domain (self.dreach, what a push uses)."""
        P = self.P; N = self.N; L1 = P["layer_c"][0]
        st = np.zeros((N, 4))
        mon = self.res[:, MON] if self.res.shape[1] > MON else np.full(N, 0.5)
        st[:, 1] = np.maximum(st[:, 1], (mon >= 0.85) + (mon >= 0.95))
        st[:, 3] = np.maximum(st[:, 3], 1.0 * (mon >= 0.95))
        tk = lambda A_: np.take(A_, self._fi)   # the close index (layer 1 is inside it)
        lend = np.where(tk(self.used) & tk(self.lv) & (tk(self.c) >= L1), tk(self.stand).astype(np.int64) - 1, 0).max(1)
        st[:, 1:3] = np.maximum(st[:, 1:3], lend[:, None])
        act = (self.used & self.lv & (self.c >= P["layer_c"][3])).sum(1)
        st[:, 1] = np.maximum(st[:, 1], 1.0 * (act >= P["wide_net"]))
        hi = (self.srank >= 0.8) & (self.scoh >= 0.3) & (self.skind >= 0) & (self.skind != G["household"])
        st[:, 1] = np.maximum(st[:, 1], 1.0 * hi.any(1))
        wk = ((self.skind == G["work"]) & (self.srank >= 0.85)).any(1)
        st[:, 2] = np.maximum(st[:, 2], 1.0 * wk)
        mv = self.skind == G["movement"]
        st[:, 3] = np.maximum(st[:, 3], np.where((mv & (self.srank >= 0.85)).any(1), 2, np.where((mv & (self.srank >= 0.6)).any(1), 1, 0)))
        st[:, 2] = np.maximum(st[:, 2], np.where((mv & (self.srank >= 0.85)).any(1), 2, 0))
        st = _uclip(np.round(st), 0, 3)
        sd = st[:, RING_OF]   # (N, domains): what holds across a whole ring
        ds = getattr(self, "dom_st", None); ts = getattr(self, "title_st", None)
        if ds is not None:
            sd = np.maximum(sd, _uclip(np.round(np.asarray(ds, float).reshape(N, len(DOMAINS))), 0, 3))
        elif ts is not None:
            ts = np.asarray(ts, float); tr = np.zeros((N, 4))
            if ts.ndim == 1:
                tr[:, 1:] = ts[:, None]
            else:
                tr = ts.reshape(N, 4)
            sd = np.maximum(sd, _uclip(np.round(tr), 0, 3)[:, RING_OF])
        for r_ in range(1, 4):
            st[:, r_] = sd[:, RING_OF == r_].max(1)
        st[:, 0] = st[:, 1:].max(1)
        sd[:, RING_OF == 0] = st[:, :1]
        self.standing = st; self.dstanding = sd
        lv = st.astype(np.int64)
        self.reach = np.stack([REACH[lv[:, r_], r_] for r_ in range(4)], 1)
        self.dreach = REACH[sd.astype(np.int64), RING_OF[None, :]]

    def _ties(self):
        lay3 = self.used & self.lv & (self.c >= self.P["layer_c"][2])
        self.ties = 1 - np.exp(-(self.c * lay3).sum(1) / self.P["ties_T"])

    def _felt(self):
        o = self.outlook
        self.felt_reach = _uclip(self.reach + self.P["fr_k"] * (o - 0.45)[:, None] * (1 + self.reach) + self.fr_bias[:, None], 0, 3)

    # ------------------------------------------------------------------ what the engine reads each week
    def _outputs(self, t):
        P = self.P; N = self.N; a = self._age(t)
        if getattr(self, "_cok", None) is not None and self._last_w == t:   # this week's close step
            c = self._cc * self._cok
        else:
            fi = self._fi
            c = np.take(self.c, fi) * (np.take(self.used, fi) & np.take(self.lv, fi) & (np.take(self.uid, fi) == self._cuid))
        c2 = c * c
        wg = c2 * self._caw                                       # the close circle's weight: closeness^2 x role by age
        csum = np.matmul(wg.astype(np.float64)[:, None, :], self._cpie)[:, 0, :]; cw = wg.sum(1)
        self._rx_close = (wg, csum, cw)   # v25 react (world_react.py) reads each close person's part (a record only)
        tot = self._setw + P["close_w"] * cw
        msc = (self._setmix + P["close_w"] * csum) / np.maximum(tot, 1e-9)[:, None]
        msc = np.where(tot[:, None] > 1e-9, msc, self.w)
        V = _norm(np.asarray(self.W.V, float)); ei = float(self._wf("era_i", 0.0))
        ep = _norm(np.asarray(self._wf("era_p", V), float))
        times = _norm(V + 0.5 * ei * (ep - V))
        b0, pk, at, wd = P["times_w"]
        tw = b0 + pk * np.exp(-((a - at) / wd) ** 2)
        self.niche = _norm((1 - tw) * msc + tw * times[None, :])
        # item 12, the steady current's parts (read only): close people, the places they are inside, the times
        pl_ = (self.places_mix if self.sph_hr and getattr(self, "places_mix", None) is not None else   # phase 2: the
               np.where(self._setw[:, None] > 1e-9, self._setmix / np.maximum(self._setw, 1e-9)[:, None], self.w))   # hours
        self.cur_parts = (np.where(cw[:, None] > 1e-9, csum / np.maximum(cw, 1e-9)[:, None], self.w), pl_,
                          np.broadcast_to(times, (N, C)))
        self._msg_raw = tot
        self.msg_w = _uclip(tot / P["msg_ref"], 0.25, 2.5)
        bs, bc = P["belong_k"]
        self.belong = 1 - np.exp(-(bs * self._belong_set + bc * c2.sum(1)))
        if getattr(self, "eyes_on", False):   # S3's buffer and kept-apart strain, S4's contrast (eyes_bel, monthly)
            self.belong = np.maximum(self.belong - self.eyes_bel, 0.0)
        self.help = 1 - np.exp(-(c * self._cav).sum(1) / P["help_H"])
        hard = _uclip(self.stress - 0.5, 0, 1)
        self.support = _uclip(P["sup_k"] * (self.help - P["help_ref"]) * (1 + hard), -0.3, 0.3)
        self._felt()
        ct = P["contagion"]
        self.contagion = dict(divorce=1 + ct[0] * np.exp(-(t - self.cont_t[:, 0]) / 104.0),
                              quit=1 + ct[1] * np.exp(-(t - self.cont_t[:, 1]) / 104.0))
