"""WorldLink's methods for a life moving through the world: other societies, titles taken, moves and returns, time in
groups, safety and resources, causes, after the act, who is in a moment, the output and saves. Part of class
WorldLink (world_link.py), which inherits LinkLifeMixin; moved out of world_link.py verbatim. A method here reads
module names through the imports below, the same objects world_link.py has, and self for everything on the link."""
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


class LinkLifeMixin:
    # ---- other societies (spec 5 §5; Emren 10:30 "Yes, fully")
    def on_title(self, n, name):
        """A title the engine just gave life n that moves it between societies or changes its standing there."""
        PP = self.PP
        if not hasattr(PP, "soc"):
            return
        abroad = int(PP.soc[n]) != int(PP.soc_home[n])
        if name in MIGRATE_T and not abroad:
            self.emigrate(n)
        elif name == "returned migrant" and abroad:
            self.return_home(n)
        elif name in CITIZEN_T and abroad:
            PP.set_status(n, "citizen")
        elif name == "second language":
            PP.lang_boost(n, 0.5)

    def emigrate(self, n):
        """Life n leaves for a neighbour, drawn toward the richer ones at peace (spec 5 §5). With one life the neighbour
        becomes a full World (spawned once, kept for a return) and the link reads it from then on."""
        W, PP = self.W, self.PP
        nx = int(getattr(W, "n_ext", 0))
        if nx <= 0:
            return None
        soc = np.asarray(getattr(W, "ext_society", np.arange(nx) + 1), int)
        rich = np.asarray(getattr(W, "ext_rich", np.ones(nx)), float)
        rel = np.asarray(getattr(W, "ext_relation", np.full(nx, 2)), float)
        wt = np.maximum(rich, 0.05) * np.where(rel > 0, 1.0, 0.1) * (soc != int(PP.soc[n]))
        if wt.sum() <= 0:
            return None
        k = int(PP.rng.choice(nx, p=wt / wt.sum())); sid = int(soc[k])
        if self.N == 1:
            W_new = self._nbw.get(sid)
            if W_new is None:
                W_new = W.spawn_neighbour(k); self._nbw[sid] = W_new
            loc = PP.emigrate(n, W_new=W_new)
        else:
            loc = PP.emigrate(n, society_id=sid)
        self._rebind()
        return loc

    def return_home(self, n):
        loc = self.PP.return_home(n)
        self._rebind()
        return loc

    def move(self, n, local, why=None):
        """A move the engine made: coming home from abroad goes back to the home society; any other is a move here."""
        PP = self.PP
        if why == "came home" and hasattr(PP, "soc") and int(PP.soc[n]) != int(PP.soc_home[n]):
            return self.return_home(n)
        return PP.move(int(n), local=local, why=why, t=PP.t)

    def _rebind(self):
        """After a switch of World (one life abroad or back): read the new one from its present on."""
        if getattr(self.PP, "W", self.W) is not self.W:
            self.W = self.PP.W
            if int(self.W.t) < int(self.PP.t):   # the World left behind ran on without the life: catch it up quietly
                self.W.tick(int(self.PP.t))
            self._rec_i = len(self.W.record); self.last_ev = int(self.W.t)
        self.acc_ = self.accept()

    def group_time(self, held, com, fai):
        """(N,) added to free time (package §5, time from the settings' time shares): the shares of one's clubs, scenes,
        online communities, gangs and movements, and a congregation one goes to without the faith commitment, less what
        the commitments already count (community: its largest group; faith: the congregation; career: work), against
        the typical life's (TIME_REF), so 0 at the typical world."""
        PP = self.PP; sk = np.asarray(PP.skind); ts = np.where(sk >= 0, np.asarray(PP.sts, float), 0.0)
        vk = _isin_small(sk, [PM.G[g_] for g_ in ("club", "scene", "online", "gang", "movement")])
        vs = np.where(vk, ts, 0.0)
        cg = np.where(sk == PM.G["congregation"], ts, 0.0).sum(1)
        extra = vs.sum(1) - np.where(held[:, com], vs.max(1), 0.0) + np.where(held[:, fai], 0.0, cg)
        return -(extra - TIME_REF)

    def safety(self):
        """What the place adds to the safety need's supply (N,): crime there, a war, a disaster's aftermath."""
        p = self.safety_parts()
        return p["crime"] + p["war"] + p["disaster"]

    def safety_parts(self):
        """safety() by cause, {"crime", "war", "disaster": (N,)}."""
        W, PP = self.W, self.PP
        cr = np.asarray(W.loc_crime, float)[PP.loc]; ds = np.minimum(np.asarray(W.loc_disaster, float)[PP.loc], 1)
        return {"crime": -0.5 * (cr - CRIME_REF), "war": -(0.15 * float(getattr(W, "war", 0) > 0)) + np.zeros(self.N),
                "disaster": -(0.15 * ds)}

    def resources(self, employed):
        """What the world adds to the targets the engine's resources drift to (money, freedom), (N,) each: rent where
        housing is dear for those without a home of their own, prices eating a fixed income, the welfare floor for those
        out of work, the rights there are. 0 at the burn-in's typical world."""
        p = self.resources_parts(employed)
        return p["housing"] + p["prices"] + p["welfare"], p["rights"]

    def resources_parts(self, employed):
        """resources() by cause: money from "housing" (rent), "prices" and "welfare" (the floor), freedom from
        "rights", each (N,)."""
        W, PP = self.W, self.PP
        rent = -0.05 * float(_uclip(W.housing, -1, 1)) * ~np.asarray(PP.own_home, bool)
        inf_ = self._pub.get("inflation"); inf_ = INFL_REF if inf_ is None else float(inf_)
        price = -0.004 * _uclip(inf_ - INFL_REF, -5, 15) * ~np.asarray(employed, bool)
        floor = 0.15 * (float(W.welfare) - WELF_REF) * ~np.asarray(employed, bool)
        free = np.full(self.N, 0.2 * (float(np.mean(W.rights)) - RIGHTS_REF))
        return {"housing": rent, "prices": price, "welfare": floor, "rights": free}

    def wl2_parts(self, employed):
        """WL2 (world-in-life.md), the small effects the world was missing, added to the targets the resources drift to,
        each (N,) and 0 in a calm world: money from "prices_work" (prices eat a wage too, as wages lag), "recession"
        (fewer hours and no raise for those who keep their job, twice in a severe one) and "disaster" (a disaster in
        their own town costs money); freedom from "rec_hours" (the hours cut give a little time back) and
        "disaster_time" (time spent clearing up); ties from "pandemic" (a lockdown cuts time with people)."""
        W, PP, k = self.W, self.PP, WL2_PAR
        emp = np.asarray(employed, bool)
        inf_ = self._pub.get("inflation"); inf_ = INFL_REF if inf_ is None else float(inf_)
        rec = float(getattr(W, "phase", 0) == 1) * (2.0 if getattr(W, "severity", 0) == 2 else 1.0)
        ds = np.minimum(np.asarray(W.loc_disaster, float)[PP.loc], 1)
        lock = float(getattr(W, "lockdown", 0.0))
        return {"prices_work": -k["price_work"] * 0.004 * _uclip(inf_ - INFL_REF, -5, 15) * emp,
                "recession": -k["rec_money"] * rec * emp, "rec_hours": k["rec_free"] * rec * emp,
                "disaster": -k["dis_money"] * ds, "disaster_time": -k["dis_free"] * ds,
                "pandemic": -k["pand_tie"] * lock + np.zeros(self.N)}

    def cause(self, kind, years=5, key=None):
        """The world behind an effect of `kind` (CAUSE_REC), for the game's hover: the latest public record entry of
        that kind in the last `years` years (domain, kind, key, the character's age then), else None; with key, only
        an entry about that key (a law's own change)."""
        want = CAUSE_REC.get(kind, ())
        if not want:
            return None
        lim = int(self.W.t) - 52 * years
        for e in reversed(self.W.record):
            if int(e.get("t", 0)) < lim:
                break
            if any(e.get("domain") == w_[0] and e.get("kind") == w_[1] and (len(w_) < 3 or str(e.get("key") or "").startswith(w_[2]))
                   for w_ in want) and (key is None or e.get("key") == key):
                return dict(domain=e.get("domain"), kind=e.get("kind"), key=e.get("key"),
                            age=round((int(e["t"]) - self.t0) / 52, 2))
        return None

    # ---- after the act
    def on_act(self, live, s, a, ma, succ, L, marks_defied=None):
        """The acts of this week: the close circle judges each (and objects by the act's norm), and an act with a lever
        pushes where it lands (written or inferred in _infer_pushes). Returns the push results, one per push."""
        idx = np.nonzero(live)[0]
        if not len(idx):
            return []
        si_, ai_ = s[idx], a[idx]
        out = self.PP.on_act(idx, ma[idx], succ[idx].astype(float), lever=self.lev_i[si_, ai_], pushes=self.dom_i[si_, ai_],
                             target=self.tgt_i[si_, ai_], norm=self.nrm_i[si_, ai_], var=self.var_i[si_, ai_], t=self.PP.t,
                             sphere=self.lsph[si_, ai_], office=self.loff[si_, ai_])
        res = out.get("results", []) if isinstance(out, dict) else []
        if getattr(self.PP, "eyes_on", False):   # S3: their places read the life-event moments' picks and the lever acts
            se_ = self.eyes_life[si_] | (self.lev_i[si_, ai_] >= 0)
            if se_.any():
                self.PP.eyes_see(idx[se_], ma[idx[se_]], succ[idx[se_]].astype(float), "act")
        hp_ = self.hpick[si_] & (succ[idx] > 0) & (self.osph[si_, ai_] >= 0) & (self.ocol[si_, ai_] >= 0)
        if hp_.any() and getattr(self.PP, "sph_h", False):   # the haunt choice (N1): the option's face picks the place
            for n_, s2_, a2_ in zip(idx[hp_], si_[hp_], ai_[hp_]):
                self.PP.pick_haunt(int(n_), int(self.osph[s2_, a2_]), int(self.ocol[s2_, a2_]))
        mn_ = self.gov_office[idx] & self.office_s[si_] & (succ[idx] > 0)
        if mn_.any():   # W40: a minister's success in office passes the law the norms already point to (it lands, or
            ld_ = self.law_due()   # not, at the world's next quarter; the record shows it as the character's if it does)
            if ld_ is not None:
                for n_ in idx[mn_]:
                    self.W.push("state", ld_[0], 2.0, ld_[1])
                    self.self_law[ld_[0]] = (int(n_), int(self.W.t))
        return res

    def option_levers(self, si):
        """Each option of moment si: None, or dict(lever, target) (target: the domain, or 'domain sub-kind'), for the
        game's icons (hooks §2.6). An empty list when no option pushes."""
        K_ = min(len(self.L["labels"][si]), self.lev_i.shape[1])
        out = []
        for ki in range(K_):
            lv = int(self.lev_i[si, ki])
            if lv < 0 or self.dom_i[si, ki] < 0:
                out.append(None); continue
            d = WK.DOMAINS[int(self.dom_i[si, ki])]; tg = self.tgt_i[si, ki]
            out.append(dict(lever=WK.LEVERS[lv], target=d if tg is None else f"{d} {tg}"))
        return out if any(x_ is not None for x_ in out) else []

    def who(self, n, si):
        """{slot: cast id} for the moment's who: slots (the game names them); a want's holder takes the first slot."""
        sl_ = list(self.L.get("W_WHO", [[]] * self.S)[si])
        if not sl_:
            return None
        pv_ = self.pending.get(int(n))
        first_ = pv_[0] if pv_ is not None and pv_[2] == si and pv_[0] >= 0 else None   # (a want of the life's own, or a post's moment with no holder, -1: none)
        if first_ is None and self.inm_s[si]:   # part 4: the closest active former-inmate tie (the moment is open only with one)
            k_ = self.PP.inmate_closest(int(n))
            first_ = int(self.PP.uid[int(n), k_]) if k_ >= 0 else None
        out = self.PP.fill(int(n), sl_[1:] if first_ is not None else sl_)
        if first_ is not None:
            out = {sl_[0]: int(first_), **out}
        return {k_: int(v_) for k_, v_ in out.items()}

    def output(self, log_lives, w=None):
        """What the run hands the game: the world's log and public state, its save, and each logged life's people."""
        PP = self.PP
        snap = self.W.snapshot()
        snap["gov"]["leader_self"] = self.self_head is not None and int(self.self_head) in [int(i) for i in log_lives]
        others = {int(k_): W_.save() for k_, W_ in (getattr(PP, "_Ws", None) or {}).items() if W_ is not self.W}
        out = dict(t0=self.t0, record=list(self.W.record), log=self.log, hist=self.hist, snapshot=snap,
                   save=self.W.save(), saves_other=others, people={int(i): PP.save(int(i)) for i in log_lives},
                   cast={int(i): PP.cast_view(int(i)) for i in log_lives},
                   place={int(i): PP.place_view(int(i)) for i in log_lives},
                   settings={int(i): PP.settings_view(int(i)) for i in log_lives},
                   reach={int(i): PP.reach_view(int(i)) for i in log_lives},
                   figures={int(i): PP.figure_view(int(i)) for i in log_lives})   # public figures as the life reads them
        if self.seen_on:   # seen_done (only when on): the refit's numbers, and each logged life's ten most seen paths
            out["seen"] = dict(self.seen_report(), paths={int(i): PP.seen_paths(int(i), top=10) for i in log_lives})
        return out

    def save(self, n):
        return dict(world=self.W.save(), people=self.PP.save(n))
