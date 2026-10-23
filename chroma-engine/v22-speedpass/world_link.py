"""world_link.py: how the engine reads the outer world (chroma-engine/world-build.md, "How the engine reads the world").

engine.run builds one WorldLink when P["world"] is True and calls it at fixed points; with the world off nothing here
runs and the engine is unchanged. The link owns the World (world.py, one per world seed) and the People (world_people.py,
one row per life of the run) and turns their state into what the engine already reads: era, drivers, niche, support,
rate multipliers per moment, gates on moments, closures on options, wants that bring a moment, and pushes after acts.

Rules kept: no color pair is special here (only the modules' overlap and distance); the world's history never depends
on the lives except through pushes; keys only, the game writes the words."""
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
from world_link_base import *  # noqa: F401,F403   (the tables and helpers, world_link_base.py)
from world_link_base import _code_md5, _isin_small, _uclip  # noqa: F401
from world_link_week import LinkWeekMixin
from world_link_rates import LinkRatesMixin
from world_link_life import LinkLifeMixin
import world_fit as WF   # v25 lane A (the realm, what a world rewards)


class WorldLink(LinkWeekMixin, LinkRatesMixin, LinkLifeMixin):
    # the link's set-up and its weekly step; the rest of its methods are in the mixins above
    def __init__(self, E, P, L, N, seed, female, attr, KILLS, ENDS, CAR):
        cfg = dict(P.get("world_cfg") or {})
        burn = cfg.pop("burn_years", 80)
        legacy = cfg.pop("legacy", None)   # People.save() of an earlier life: this one is born into that family line
        self.start = cfg.pop("start", None)   # v22.5, F12: what the start promises (read with start_hold on)
        W = P.get("world_obj")
        if W is None:
            ws = P.get("world_seed")
            s3_ = {k: bool(P[k]) for k in getattr(WM, "S3_RULES", ()) if k in P}   # stage 3 switches (stage3-rules.md §8)
            s3_.update({k: P[k] for k in getattr(WM, "SPH_RULES", ()) if P.get(k)})   # the spheres' (item 15), when on
            s3_.update({k: P[k] for k in getattr(WM, "C_RULES", ()) if P.get(k)})     # the C hooks' (item 10), when on
            s3_.update({k: P[k] for k in getattr(WM, "FIN_RULES", ()) if P.get(k)})   # the finishing pack's, when on
            if P.get("realm", "earth") != "earth":   # v25: a test realm (realm_neutral.py), and its colour-even bodies
                s3_["realm"] = P["realm"]
                if getattr(WF.realm(P["realm"]), "INST_EVEN", False):
                    s3_["inst_even"] = True
            if s3_:
                cfg["params"] = dict(cfg.get("params") or {}, **s3_)
            W = burned_world(int(seed if ws is None else ws), cfg, burn)
        self.W = W; self.t0 = int(W.t); self.N = N; self.E = E; self.L = L
        if "land_hx" in W.__dict__:   # v25 lane D: a world saved from a run with the land on keeps no feedback here
            del W.land_hx              # (WorldLink.land_setup sets it again with wa_land on)
        self.land = None; self.nat = None
        PP = P.get("people_obj")
        if PP is None:
            PP = PM.People(W, N, run_seed=int(seed), female=np.asarray(female, bool))
            PP.birth(self.t0, legacy=legacy)
            if P.get("start_hold") and self.start and legacy is None and N == 1:   # v22.5, F12: the game's one life is
                # drawn again until its birth keeps the start's promise (a run of many lives keeps its draw)
                for k_ in range(1, START_TRIES + 1):
                    if start_fits(PP, W, self.start).all():
                        break
                    PP = PM.People(W, N, run_seed=int(seed) + 7919 * k_, female=np.asarray(female, bool))
                    PP.birth(self.t0)
        for a_ in ("land", "nat", "nat_on", "quarrel_x"):   # v25 lane D: a People from a run with them on keeps none here
            PP.__dict__.pop(a_, None)                        # (land_setup and nat_setup set them again when on)
        self.PP = PP
        tr_ = tuple(P.get("trace_off") or ())   # test only (tools/white_trace.py): parts of the world read colour-blind
        if tr_:
            PP.trace_off = tr_
            if "rank" in tr_:
                PP.P = dict(PP.P, rank_k=0.0)
        PP.tilt_on = bool(P.get("tilt_world", False))   # v25 #10: what a world rewards, at the rung climb (world_fit.tilt_year)
        if PP.tilt_on:
            PP.tilt_R = WF.realm(P.get("realm", "earth"))
        S, K = L["S"], L["K"]; self.S = S
        names = L["names"]; src = L["src"]
        # each moment's rate kind (world-build.md: illness and old-age deaths by season and medicine, disasters by place,
        # crime by place, war, pandemic, job loss by sector, births)
        rk = np.full(S, -1)
        for si in range(S):
            nm = names[si]; life = str(src[si].get("life", "")); tier = str(src[si].get("tier", ""))
            if KILLS[si] >= 0:
                rk[si] = RK.index("old_death")
            elif ENDS[si] == CAR:
                rk[si] = RK.index("jobloss")
            elif nm in ("war comes", "the call to serve"):
                rk[si] = RK.index("war")
            elif "a baby on the way" in nm:
                rk[si] = RK.index("birth")
            elif PANDEMIC_W.search(nm):
                rk[si] = RK.index("pandemic")
            elif DISASTER_W.search(nm):
                rk[si] = RK.index("disaster")
            elif CRIME_W.search(nm):
                rk[si] = RK.index("crime")
            elif "health" in life and tier == "life event":
                rk[si] = RK.index("illness")
        self.rk = rk
        # the channels the engine reads (package §5): which moments a close person's divorce or quitting makes likelier,
        # which the wish to move scales, which options find a job, gain a place in education, or are an illness's
        PAR_ = [c_[0] for c_ in E.COMMITMENTS].index("partner")
        GR_ = L.get("ROLES") or {}; AT_ = np.asarray(GR_.get("A_TITLE", np.full((S, K), -1)))
        tn_ = list(GR_.get("names", [])); kn_ = list(GR_.get("kindname", []))
        car_t = [i_ for i_ in range(len(kn_)) if kn_[i_] == "career"]
        edu_t = [i_ for i_, nm_ in enumerate(tn_) if re.search(r"\b(student|pupil|apprentice|trainee|graduate)\b", str(nm_))]
        drops_ = [[str((nt or {}).get("drops") or "") for nt in (L["notes"][si] if si < len(L["notes"]) else [])] for si in range(S)]
        self.div_s = np.array([ENDS[si] == PAR_ or bool(re.search(r"\b(divorce|separat|marriage ends|break up|breaking up)", names[si]))
                               for si in range(S)], bool)
        self.quit_s = np.array([any(d_ and ("career" in d_ or "{title}" in d_) for d_ in drops_[si]) or
                                bool(re.search(r"\b(quit|resign|walk out|hand in your notice)", names[si])) for si in range(S)], bool)
        self.move_s = np.asarray(L["MOVES"][:S], bool) | np.array([bool(re.search(r"\bmov(e|es|ing)\b|somewhere else", names[si]))
                                                                  for si in range(S)], bool)
        self.job_o = np.isin(AT_, car_t) if AT_.shape == (S, K) else np.zeros((S, K), bool)
        self.adm_o = np.isin(AT_, edu_t) if AT_.shape == (S, K) and edu_t else np.zeros((S, K), bool)
        self.ill_s = rk == RK.index("illness")
        idx = {nm: i for i, nm in enumerate(names)}
        self.c2 = bool(W.p.get("c2_groups"))
        self.wm = [(x_[0], x_[1], x_[2], idx[x_[3]], x_[4], x_[5] if len(x_) > 5 else "all")
                   for x_ in WORLD_MOMENTS + (C2_MOMENTS if self.c2 else []) if x_[3] in idx]
        keep_ = {idx[k_] for k_ in C2_KEEP if k_ in idx} if self.c2 else set()
        self.wm_s = np.array(sorted({x[3] for x in self.wm} - keep_), int)
        if self.c2:   # C2: the moments only the world brings to a group (no everyday draw), the split, the drift read
            self.c2_only = np.array(sorted({idx[x_[3]] for x_ in C2_MOMENTS if x_[3] in idx and x_[3] not in C2_KEEP}), int)
            self.c2_split = idx.get("the congregation splits in two", -1)
            self.c2_par = dict(C2_DEFAULT, **(W.p.get("c2_par") or {}))
            self.c2_drift = None   # whose congregation is over the drift line (None: not read yet; the first read only sets it)
        self.toy = np.asarray(L.get("W_TOY", np.zeros((S, 4)))); self.toy_set = np.asarray(L.get("W_TOY_SET", np.zeros(S, bool)))
        self.toy_on = self.toy.sum(1) > 0
        self.holy = np.asarray(L.get("W_HOLY", np.full(S, -1))); self.where = np.asarray(L.get("W_WHERE", np.zeros((S, 1), bool)))
        self.group = np.asarray(L.get("W_GROUP", np.full(S, -1))); self.prem = np.asarray(L.get("W_PREMISE", np.full(S, -1)))
        self.want = np.asarray(L.get("W_WANT", np.full(S, -1)))
        # the spheres (item 15, phase 2): a moment among a haunt's regulars, one opened by a rung in its sphere, and the
        # haunt choices (an option's face picks the place)
        self.haunt = np.asarray(L.get("W_HAUNT", np.full(S, -1))); self.ladder = np.asarray(L.get("W_LADDER", np.full(S, -1)))
        self.msph = np.asarray(L.get("W_SPHERE", np.full(S, -1))); self.hpick = np.asarray(L.get("W_HPICK", np.zeros(S, bool)))
        self.osph = np.asarray(L.get("W_OSPH", np.full((S, K), -1))); self.ocol = np.asarray(L.get("W_OCOL", np.full((S, K), -1)))
        self.H_GREAT = WK.HAUNT_KINDS.index("gather.great")
        self.sphev = np.asarray(L.get("W_SPHEV", np.full(S, -1)))   # sphere events' moments (phase 3): the event's index
        if self.sphev.dtype == bool:                                  # (a batch read before phase 3: held back)
            self.sphev = np.where(self.sphev, 0, -1)
        # finishing pack, part 5 (grey_gate): a moment of a town gone grey, open while the sphere's grey share (World.sph_grey,
        # town: its greyest sphere) is at least the Library's threshold (sphere_data.SHADOW grey_gate, .25)
        self.shadow = np.asarray(L.get("W_SHADOW", np.full(S, -1)))
        import sphere_data as SD_
        self.grey_on = bool(P.get("grey_gate")); self.grey_thr = float(SD_.SHADOW.get("grey_gate", SD_.SHADOW["gate"]))
        self.new_gates = (self.haunt >= 0) | (self.ladder >= 0) | (self.sphev >= 0) | (self.shadow >= 0)   # the spheres'
        # gates (moment_factor)
        self.law = np.asarray(L.get("W_LAW", np.full((S, K), -1))); self.norm = np.asarray(L.get("W_NORM", np.full((S, K), -1)))
        self.tech = np.asarray(L.get("W_TECH", np.full((S, K), -1))); self.lever = np.asarray(L.get("W_LEVER", np.full((S, K), -1)))
        self.law_neg = np.asarray(L.get("W_LAW_NEG", np.zeros((S, K), bool)))     # a leading minus (v23 W38): the option
        self.norm_neg = np.asarray(L.get("W_NORM_NEG", np.zeros((S, K), bool)))   # goes against the law or norm in force
        self.push = np.asarray(L.get("W_PUSH", np.full((S, K), -1)))
        self._infer_pushes(E, L, S, K)
        self._lever_spheres(S, K)
        self.ssm = WK.LAW_KEYS.index("same-sex marriage")
        self.NI = {k_: i_ for i_, k_ in enumerate(WK.NORM_KEYS_ALL)}
        # a want moment's options that meet the want (the cast member's wish): a mark of helping or coming home, a title
        # or a skill it gives, a bond it makes, or kindness among its values; one marked as a refusal never does
        REFUSE = {"refused someone in need", "turned down a chance", "made an enemy", "broke your word"}
        MEET = {"helped someone in need", "came home"}
        self.meets = np.zeros((S, K), bool)
        for si in np.nonzero(self.want >= 0)[0]:
            for ki, nt in enumerate(L["notes"][si]):
                mk_ = str(nt.get("mark") or "").strip()
                if mk_ in REFUSE:
                    continue
                self.meets[si, ki] = bool(mk_ in MEET or nt.get("title") or nt.get("grants") or nt.get("binds")
                                          or "benevolence" in str(nt.get("v") or ""))
        self.want_s = {}                  # want key -> moments that answer it
        for si in np.nonzero(self.want >= 0)[0]:
            self.want_s.setdefault(WK.CAST_WANTS[int(self.want[si])], []).append(int(si))
        self.pending = {}                 # n -> (cast id, want key, moment) offered this week
        # spheres finishing pack, part 4: the moments with a fellow inmate (cast_want: fellow_inmate)
        self.inm_s = (self.want == WK.CAST_WANTS.index("fellow_inmate")) if "fellow_inmate" in WK.CAST_WANTS else np.zeros(S, bool)
        # S7 lead_ways: a post's moments (cast_want lead_*), fired with no holder (cid -1): a crisis or fall moment's way
        # (lead_way:), each option's way, fall and hand answers (lead:, fall:, hand:), and the engine's office titles
        self.lw = bool(getattr(PP, "lw", False))
        if self.lw:
            self.lway = np.asarray(L.get("W_LEAD_WAY", np.full(S, -1)))
            self.olead = np.asarray(L.get("W_LEAD", np.full((S, K), -1)))
            self.ofall = np.asarray(L.get("W_FALL", np.full((S, K), -1)))
            self.ohand = np.asarray(L.get("W_HAND", np.full((S, K), -1)))
            PP.lw_keys = {k_ for k_ in self.want_s if k_.startswith("lead_")}
            rid_ = dict((L.get("ROLES") or {}).get("ID") or {})
            self.lw_tid = np.array([rid_.get(nm_, -1) for nm_ in PP.lw_tnames], np.int64)   # -1: not in the catalogue
            self.lw_fire = {}             # n -> the post whose moment was offered this week
        # finishing pack, part 2 (place_turnover): "the place closed" and "the new place" (cast_want place_closed,
        # place_opened; no holder) come only with a closing or an opening of the life's place, never by a draw
        self.pt_m = np.isin(self.want, [WK.CAST_WANTS.index(w_) for w_ in WK.PLACE_WANTS])
        if getattr(PP, "pt_on", False):
            PP.pt_keys = {k_ for k_ in self.want_s if k_ in WK.PLACE_WANTS}
        # far_ties (item 18): a far moment's touch (touch:), and its options that take the tie in (mark: took them in)
        self.touch = np.asarray(L.get("W_TOUCH", np.full(S, -1)))
        self.took = np.zeros((S, K), bool)
        for si in np.nonzero(self.want >= 0)[0]:
            for ki, nt in enumerate(L["notes"][si][:K]):
                self.took[si, ki] = str((nt or {}).get("mark") or "").strip() == "took them in"
        # S3, S4 (sph_eyes, sph_odd): what their places see, the life-event moments' picks (stand-in for the pivotal picks)
        # and any act with a lever; an option's caught: and odd: tags (world_keys.CAUGHT_TAGS, ODD_TAGS)
        self.eyes_life = np.array([str(L["src"][si].get("tier", "")) == "life event" for si in range(S)], bool)
        self.caught = np.asarray(L.get("W_CAUGHT", np.full((S, K), -1))); self.odd = np.asarray(L.get("W_ODD", np.full((S, K), -1)))
        # S5, sacred lines: the moments of a life's own (cast_want: sacred, tragic, amends; no cast member holds them),
        # their line kinds, offer kind and round, and their options' tags (line:, tragic:, heal:)
        self.sac_on = bool(getattr(PP, "sac_on", False))
        self.sac_m = np.asarray(L.get("W_SACRED", np.full((S, 2), -1))).reshape(S, 2)
        self.sac_off = np.asarray(L.get("W_OFFER", np.full(S, -1))); self.sac_rnd = np.asarray(L.get("W_ROUND", np.full(S, -1)))
        self.sac_line = np.asarray(L.get("W_LINE", np.full((S, K), -1))); self.sac_trag = np.asarray(L.get("W_TRAGIC", np.full((S, K), -1)))
        self.sac_heal = np.asarray(L.get("W_HEAL", np.full((S, K), -1)))
        self.sac_pend = {}                # n -> the offer or amends (People.sac_q item) the week's pending moment answers
        # seen_done (S6): the path each option is on (the title it gives, else the title it aims at), and the People's
        # count of the paths seen walked, in the engine's title indices
        self.seen_on = bool(getattr(PP, "seen_on", False))
        if self.seen_on:
            NT_ = int(GR_.get("NT", 0)) if GR_ else 0
            PP.seen_setup(GR_ if NT_ else None)
            aim_ = np.asarray(GR_.get("A_AIM", np.full((S, K), -1))) if NT_ else np.full((S, K), -1)
            ok_ = NT_ and AT_.shape == (S, K) and aim_.shape == (S, K)
            self.sd_tk = np.where(AT_ >= 0, AT_, np.where((aim_ >= 0) & (aim_ < NT_), aim_, -1)) if ok_ else np.full((S, K), -1)
            self.sd_stat = np.zeros((2, PM.C))   # the felt-odds lift on offered options by their colour way: sum, weight
            self.sd_n = np.zeros(4)              # offered options; those on a path; the path part's sum; the whole lift's
        # body_trust (finishing pack part 3): the sphere of the body each option's path leads into (S6's paths: a title held
        # at a body of that sphere; -1 none), for the felt odds trust bends
        self.bt_on = bool(getattr(PP, "bt_on", False))
        if self.bt_on and self.seen_on:
            NT_ = int(GR_.get("NT", 0)) if GR_ else 0
            ins_ = np.asarray(GR_.get("institution", np.full(NT_, -1)))[:NT_] if NT_ else np.zeros(0, int)
            kd_ = np.array([PM.bt_title_kind(GR_["names"][i_], ins_[i_]) for i_ in range(NT_)] + [-1], np.int64)
            tj_ = np.where(kd_ >= 0, PM.BT_INST_J[np.maximum(kd_, 0)], -1)
            self.bt_tj = tj_[np.where((self.sd_tk >= 0) & (self.sd_tk < NT_), self.sd_tk, NT_)]
        # W40: a pack-made head of government leads the state (the first life to hold it, one state); a minister or head
        # of government can pass a law the norms already point to; a government that falls takes their office with it
        self.self_head = None; self.gov_office = np.zeros(N, bool); self.office_lost = np.zeros(N, bool)
        self.self_lead = float(P.get("world_self_lead", 0.05))   # quarterly pull of the government's colors to the leader's
        self.self_law = {}                # law key -> (life, week) a minister among the lives pushed it (W40)
        self.hist = []                    # monthly, published figures only (Emren 10:09): dict(t, recession, unemp, infl, war, era)
        self._pub = {}                    # the latest published figure per key
        self._rec_i = len(W.record)       # the public record before the birth stays in W.record (the panel's history)
        self._carry = []; self._pp_i = 0  # cast events not yet handed to the engine (the birth's come before the first week)
        self.dis_own = np.zeros(N); self.dis_near = np.zeros(N, bool)   # a disaster in one's town (severity) or a close one's
        self.dis_haz = [None] * N; self.dis_rec = [None] * N   # its hazard (world.HAZARDS) and record entry, where it struck
        self.dis_nhaz = [None] * N                             # the hazard of one in a close person's town
        self._nbw = {}                    # society id -> the neighbour's full World, once a life has gone there (N == 1)
        self.layer2 = float(PP.P["layer_c"][1])   # closeness of the close circle's second layer: "their people"
        self.acc_ = self.accept()
        self.fac = np.ones((N, S)); self.last_ev = self.t0
        self.fire_now = np.zeros((N, S), bool)
        self.fire_why = {}                # moment -> the world's record entry that brought it this week (the reports)
        self.log = []                     # world events while the run lived (JSON-safe, with the character's age)
        self.week_events = []

    def _infer_pushes(self, E, L, S, K):
        """Each option's lever, push domain, target and norm (S, K): as written, else inferred (world-fields.md)."""
        notes = L["notes"]; MARKS = list(L.get("MARKS", [])); MK = np.asarray(L["MARK"])
        at = np.asarray(L.get("W_AT", np.full(S, -1))); who = L.get("W_WHO", [[]] * S)
        sub = L.get("W_PUSH_SUB", {}); COMMIT = np.asarray(L["COMMIT"]); DOM = np.asarray(L["DOM"])
        CL = np.asarray(L.get("CLOSED", np.full((S, K), -1)))
        KN_ = [c_[0] for c_ in E.COMMITMENTS]
        # W40: a moment of national office (its requires: names a minister, the head of government or a member of
        # parliament) acts on the state; a minister's success there passes the law the norms already point to
        self.office_s = np.array([bool(re.search(r"\b(minister|head of government|member of parliament)\b",
                                                 str(L["src"][si].get("requires", "")))) for si in range(S)], bool)
        self.lev_i = np.full((S, K), -1, np.int64); self.dom_i = np.full((S, K), -1, np.int64)
        self.tgt_i = np.full((S, K), None, dtype=object); self.var_i = np.full((S, K), None, dtype=object)
        for si in range(S):
            row = notes[si] if si < len(notes) else []
            for ki in range(min(K, len(row))):
                nt = row[ki] if isinstance(row[ki], dict) else {}
                mk_ = MARKS[MK[si, ki]] if MK[si, ki] >= 0 else ""
                lv = int(self.lever[si, ki])
                if lv < 0:
                    if mk_ in LEVER_MARK:
                        lv = WK.LEVERS.index(LEVER_MARK[mk_])
                    elif nt.get("drops") or str(nt.get("moves", "")).strip().lower() in ("yes", "true", "1"):
                        lv = WK.LEVERS.index("exit")
                    elif CL[si, ki] == 0 and at[si] >= 0:
                        lv = WK.LEVERS.index("subvert")
                if lv < 0:
                    continue
                self.lev_i[si, ki] = lv
                d = int(self.push[si, ki]); tg = sub.get((si, ki))
                if d < 0:
                    if mk_ in NORM_MARK:   # coming out or naming one's gender moves the culture's acceptance of it
                        d = WK.DOMAINS.index("culture"); self.var_i[si, ki] = NORM_MARK[mk_]
                    elif self.office_s[si]:
                        d = WK.DOMAINS.index("state")
                    elif at[si] >= 0:
                        d = WK.DOMAINS.index("institution"); tg = WK.INST_KINDS[int(at[si])]
                    elif self.group[si] >= 0:
                        d = WK.DOMAINS.index("group"); tg = WK.GROUP_KINDS[int(self.group[si])]
                    elif who[si]:
                        d = WK.DOMAINS.index("close"); tg = who[si][0]
                    else:
                        ck = int(COMMIT[si, ki]) if COMMIT[si, ki] >= 0 else (int(np.argmax(DOM[si])) if DOM[si].max() > 0 else -1)
                        dn_, tg = PUSH_COMMIT.get(KN_[ck], ("close", None)) if ck >= 0 else ("close", None)
                        d = WK.DOMAINS.index(dn_)
                self.dom_i[si, ki] = d; self.tgt_i[si, ki] = tg
        # the norm each option is judged by (its norm:, else its law:, else coming out or naming one's gender): a close
        # person's strong objection to it grows into an approval closure (spec 2 §3)
        L2N = np.array([WK.NORM_KEYS_ALL.index(k_) for k_ in WK.LAW_KEYS_ALL] + [-1])   # a law key's norm (W38b keys sit after)
        nk_ = np.where(self.norm >= 0, self.norm, L2N[self.law]).astype(np.int64)
        for si, ki in zip(*np.nonzero((MK >= 0) & (nk_ < 0))):
            m_ = MARKS[MK[si, ki]]
            if m_ in NORM_MARK:
                nk_[si, ki] = WK.NORM_KEYS_ALL.index(NORM_MARK[m_])
        self.nrm_i = np.where(nk_ < len(WK.NORM_KEYS), nk_, -1)   # the W38b keys: close people's objections not kept

    def _lever_spheres(self, S, K):
        """Spheres phase 4 (sph_levers, sph_fair): the sphere each lever option lands in (S, K; -1 none) and an office act's
        kind (0 ban, 1 licence, 2 budget). The sphere: the moment's at: (an institution kind's sphere), else the option's
        push target where it names a group or institution kind, else the option's own sphere face, the moment's sphere,
        its haunt kind's or its sphere event's (Outer world's phase 4 answers, item 1). Office: against a law (-key) a
        ban, for a law a licence, else a budget."""
        import sphere_data as SD_
        at = np.asarray(self.L.get("W_AT", np.full(S, -1)))[:S] if hasattr(self, "L") else np.full(S, -1)
        self.lsph = np.full((S, K), -1, np.int64)
        ev_sph = np.array([WK.SPHERES.index(e_["sphere"]) for e_ in SD_.EV], np.int64)
        for si, ki in zip(*np.nonzero(self.lev_i >= 0)):
            j = -1
            if at[si] >= 0:
                j = int(WM.INST_SPH[int(at[si])])
            tg = self.tgt_i[si, ki]
            if j < 0 and isinstance(tg, str):
                if tg in WK.INST_KINDS:
                    j = int(WM.INST_SPH[WK.INST_KINDS.index(tg)])
                elif tg in WK.GROUP_KINDS:
                    j = int(WM.GROUP_SPH[WK.GROUP_KINDS.index(tg)])
            for j2 in (self.osph[si, ki], self.msph[si], WM.HAUNT_SPH[self.haunt[si]] if self.haunt[si] >= 0 else -1,
                       ev_sph[self.sphev[si]] if self.sphev[si] >= 0 else -1):
                if j < 0:
                    j = int(j2)
            self.lsph[si, ki] = j
        self.loff = np.where(self.law_neg, 0, np.where(self.law >= 0, 1, 2)).astype(np.int64)

    def fair_pull(self, s):
        """(N, K) utility from felt fairness (sph_fair): in a sphere a life feels treats it unfairly (under .35) exit,
        neglect and subvert there x 1.5 and voice and loyalty x .7 as odds; over .65 the reverse (dynamics.json
        felt_fairness)."""
        fr = getattr(self.PP, "fair", None)
        js = self.lsph[s]; lv = self.lev_i[s]
        if fr is None or not (js >= 0).any():
            return 0.0
        import sphere_data as SD_
        Fd = SD_.FAIR; lo_, hi_ = np.zeros(len(WK.LEVERS)), np.zeros(len(WK.LEVERS))
        for k_, v_ in Fd["low_mult"].items():
            lo_[WK.LEVERS.index(k_)] = np.log(v_)
        for k_, v_ in Fd["high_mult"].items():
            hi_[WK.LEVERS.index(k_)] = np.log(v_)
        on = (js >= 0) & (lv >= 0)
        f = np.take_along_axis(np.asarray(fr, float), np.maximum(js, 0).astype(np.intp), 1)
        lvi = np.maximum(lv, 0)
        u = np.where(f < Fd["low"], lo_[lvi], np.where(f > Fd["high"], hi_[lvi], 0.0))
        return np.where(on, u, 0.0)

    def trust_pull(self, s):
        """(N, K) utility from trust in a sphere's bodies (body_trust; sphere_data.TRUST low and high): in a sphere whose
        bodies a life trusts little (under low.under) exit and neglect x 1.3 and voice x .8 as odds, and subvert x 1.2 under
        subvert_under; over high.over voice and loyalty x 1.2 (finish-pack-draft.md part 3; Hirschman 1970). A life whose
        trust has not started (under 15) is not moved."""
        bt = getattr(self.PP, "btrust", None)
        js = self.lsph[s]; lv = self.lev_i[s]
        if bt is None or not (js >= 0).any():
            return 0.0
        import sphere_data as SD_
        T = SD_.TRUST; lo_, sv_, hi_ = np.zeros(len(WK.LEVERS)), np.zeros(len(WK.LEVERS)), np.zeros(len(WK.LEVERS))
        for k_, v_ in T["low"].items():
            if k_ in WK.LEVERS:
                (sv_ if k_ == "subvert" else lo_)[WK.LEVERS.index(k_)] = np.log(v_)
        for k_, v_ in T["high"].items():
            if k_ in WK.LEVERS:
                hi_[WK.LEVERS.index(k_)] = np.log(v_)
        on = (js >= 0) & (lv >= 0)
        f = np.take_along_axis(np.asarray(bt, float), np.maximum(js, 0).astype(np.intp), 1)
        f = np.where(np.isnan(f), 0.5, f)
        lvi = np.maximum(lv, 0)
        u = (np.where(f < T["low"]["under"], lo_[lvi], 0.0) + np.where(f < T["low"]["subvert_under"], sv_[lvi], 0.0)
             + np.where(f > T["high"]["over"], hi_[lvi], 0.0))
        return np.where(on, u, 0.0)

    def trust_felt(self, p_hat, s, opt):
        """body_trust: the felt odds of a pursuit in a sphere's bodies (an option on S6's path into a title held at a body
        of that sphere, bt_tj) move with the life's trust there, never the real odds (S6 stays felt): 2 x (btrust - .5) x
        S6's own most a seen path lifts (lift x cap; full trust feels as sure as a path seen walked to the cap), kept within
        .01 and .99 as seen_felt keeps them (odds already beyond them stay as they were). opt: every option but doing nothing."""
        tj = self.bt_tj[s]
        if not (tj >= 0).any():
            return p_hat
        PP = self.PP; sp_ = PP.sd_par
        f = np.take_along_axis(np.asarray(PP.btrust, float), np.maximum(tj, 0).astype(np.intp), 1)
        d = np.where((tj >= 0) & opt & ~np.isnan(f), 2.0 * (np.where(np.isnan(f), 0.5, f) - 0.5) * sp_["lift"] * sp_["cap"], 0.0)
        return np.where(d != 0, _uclip(p_hat + d, np.minimum(p_hat, 0.01), np.maximum(p_hat, 0.99)), p_hat)

    def accept(self):
        """Acceptance per norm key where each person lives and among their own people (N, n_norm), 0 to 1."""
        nv = np.array([float(self.W.norm(k_)) for k_ in WK.NORM_KEYS_ALL])
        ap = np.asarray(self.PP.approval, float)
        ap = np.pad(ap, ((0, 0), (0, len(nv) - ap.shape[1])))   # the W38b keys: no view of their own among one's people
        return _uclip(nv[None, :] + ap, 0, 1)

    # ---- every week, before the engine's week
    def week(self, t, S_):
        W, PP = self.W, self.PP
        self._carry.extend(PP.events[self._pp_i:])   # cast events the engine has not had yet (the birth's, the act's)
        if PP.wa_on:
            PP._wa_act = {}   # (the week's acts: the world answers' causes)
        W.tick(self.t0 + t)
        PP.tick(self.t0 + t, S_)
        self._pp_i = 0
        self.harsh_n = np.asarray(W.harsh_loc, float)[PP.loc] if np.ndim(W.harsh_loc) else np.full(self.N, float(W.harsh_loc))
        self._office(t, S_)
        new = [e for e in W.events_since(self.last_ev)] if t > 0 else []
        self.last_ev = int(W.t)
        rec_ = W.record[self._rec_i:]; self._rec_i = len(W.record)   # public only (Emren 10:09): the story and the panel
        self.week_events = [dict(e, age=round(t / 52, 2)) for e in rec_]
        for e in self.week_events:
            if e.get("kind") == "published":
                self._pub[e.get("key")] = e.get("value")
            elif e.get("kind") == "law changed" and e.get("key") in self.self_law:   # W40: the minister's own law
                n_, t_ = self.self_law.pop(e["key"])
                if W.t - t_ <= 26:
                    e["self"] = True; e["by_life"] = n_
                    if PP.wa_on:   # the world answers, D: a law passed is a national footprint, told by what it did
                        PP._wa_nation(n_, "state", 2.0, W.t, what="a law passed")
            elif e.get("domain") == "nature" and e.get("kind") == "disaster" and isinstance(e.get("value"), dict):
                l_ = int(e["value"].get("loc", -1)); sv_ = float(e["value"].get("severity", 0.5))
                own_ = PP.loc == l_
                for n_ in np.nonzero(own_ & (sv_ >= self.dis_own))[0]:   # the worst strike of the week, as dis_own keeps
                    self.dis_haz[n_] = e.get("key"); self.dis_rec[n_] = e
                self.dis_own = np.where(own_, np.maximum(self.dis_own, sv_), self.dis_own)
                nr_ = ~own_ & (PP.used & PP.lv & (PP.c >= self.layer2) & (PP.mloc == l_)).any(1)
                for n_ in np.nonzero(nr_)[0]:
                    self.dis_nhaz[n_] = e.get("key")
                self.dis_near |= nr_
        if self.gov_office.any() and any(e.get("kind") == "government falls" for e in rec_):
            self.office_lost = self.gov_office.copy()    # the engine ends their minister's or head of government's title
        self.log.extend(e for e in self.week_events if e.get("big") or e.get("domain") in ("era", "state", "abroad", "economy"))
        self.acc_ = self.accept()
        if t % 4 == 0:   # the world's course month by month, as published (for checks and the game's charts)
            self.hist.append(dict(t=int(t), recession=bool(getattr(W, "rec_declared", False)),
                                  unemp=self._pub.get("unemployment"), infl=self._pub.get("inflation"),
                                  war=int(getattr(W, "war", 0)), era=W.era_key))
        # moments the world's events bring this week
        self.fire_now[:] = False; self.fire_why = {}
        for e in new:
            for d, k, key, si, sh, sel in self.wm:
                if e.get("domain") == d and e.get("kind") == k and (key is None or e.get("value") == key or e.get("key") == key):
                    hit_ = PP.rng.random(self.N) < sh
                    if sel == "place":                     # only the people living in the event's place
                        hit_ &= PP.loc == int((e.get("value") or {}).get("loc", -1))
                    elif sel == "staff":                   # only the people who work there
                        hit_ &= self._staff(int((e.get("value") or {}).get("inst", -1)))
                    elif sel == "place_group":             # C2: the members of the moment's group kind in that place
                        hit_ &= (PP.loc == int((e.get("value") or {}).get("loc", -1))) & self._members(si)
                    elif sel == "faith_group":             # C2: the members of a congregation of the reviving faith
                        hit_ &= self._members(si, int((e.get("value") or {}).get("faith", -1)))
                    self.fire_now[:, si] |= hit_
                    self.fire_why[si] = e
        if self.sac_on and W.p.get("c3_inst"):   # S5: a C3 offer (sold, merged, a leak, a cover-up) reaches its staff
            for e in new:
                k_ = f"institution.{e.get('kind')}"
                if e.get("domain") == "institution" and k_ in self._sac_keys():
                    stf_ = np.nonzero(self._staff(int((e.get("value") or {}).get("inst", -1))))[0]
                    PP.sac_offer(stf_, k_, PP.t, reach=PP.sac_par["c3_reach"])
        if W.p.get("c3_inst"):
            self._c3_merged(new)
        if self.c2 and self.c2_split >= 0 and t % 4 == 0:
            self._c2_drift_q()
        # wants ripe this week: the moment that answers it, with the cast member in its first who: slot
        self.pending = {}
        for n_, cid_, key_ in PP.want_due(PP.t):
            ss_ = self.want_s.get(key_)
            if ss_ and key_.startswith("far_"):
                ss_ = self._far_pick(n_, cid_, ss_)
            if ss_ and n_ not in self.pending:
                si_ = ss_[int(PP.rng.integers(len(ss_)))]
                self.pending[n_] = (cid_, key_, si_); self.fire_now[n_, si_] = True
        if getattr(PP, "eyes_on", False):   # S3, S4: a caught-between (a go-between of either place first in who:) or an
            for n_, cid_, key_ in PP.eyes_due(PP.t):   # odd-one-out moment (no holder) waiting, as a want's moment comes
                ss_ = self.want_s.get(key_)
                if ss_ and key_ == "odd":   # S4: a moment of the odd place's sphere (its sphere: line), else a place-neutral one
                    sp_ = PP.eyes_sphere(n_)
                    ss_ = [s_ for s_ in ss_ if sp_ >= 0 and self.msph[s_] == sp_] or [s_ for s_ in ss_ if self.msph[s_] < 0]
                if ss_ and n_ not in self.pending:
                    si_ = ss_[int(PP._eyes_rng.integers(len(ss_)))]
                    self.pending[n_] = (cid_, key_, si_); self.fire_now[n_, si_] = True
        if self.lw:   # S7: a post's moment (taking it, a crisis of its way, its fall, the turn to routine, handing it on)
            self.lw_fire = {}
            for n_, key_, pid_, way_ in PP.lead_due(PP.t):
                if n_ in self.pending:
                    continue
                ss_ = self.want_s.get(key_) or []
                if key_ in ("lead_crisis", "lead_fall"):   # the moments of the post's own way, when the Library has them
                    ss_ = [si for si in ss_ if self.lway[si] == way_] or ss_
                if ss_:
                    si_ = ss_[int(PP._lw_rng.integers(len(ss_)))]
                    self.pending[n_] = (-1, key_, si_); self.fire_now[n_, si_] = True; self.lw_fire[n_] = pid_
        if getattr(PP, "pt_on", False) and PP.pt_keys:   # part 2: the place closed, the new place (no holder: cid -1)
            for n_, key_ in PP.pt_take(PP.t, self.pending):
                ss_ = self.want_s.get(key_) or []
                si_ = ss_[int(PP._pt_rng.integers(len(ss_)))]
                self.pending[n_] = (-1, key_, si_); self.fire_now[n_, si_] = True
        if self.sac_on:   # S5: an offer on a held line, a tragic trade-off or amends brings its moment (no holder: cid -1)
            self.sac_pend = {}
            for n_, it_ in PP.sac_due(PP.t):
                if n_ in self.pending:
                    continue
                si_ = self._sac_pick(n_, it_)
                if si_ is None:   # no moment for this line: decided off-screen by the character's own odds
                    if it_["kind"] != "amends" and PP.sac_par["quiet"]:
                        PP.sac_quiet(n_, it_, PP.t)
                    elif it_ in PP.sac_q.get(n_, []):
                        PP.sac_q[n_].remove(it_)
                    continue
                self.pending[n_] = (-1, it_["kind"], si_); self.fire_now[n_, si_] = True; self.sac_pend[n_] = it_
        if getattr(self, "wa_on", False):   # the world answers: an ask, a Known life's decision, a figure's moment
            self._wa_week()
        if self.land is not None:   # v25 lane D: the land's week (strikes, courses, drift, the moments it brings)
            self.land.week(S_)
        if self.nat is not None:    # v25 lane D: the national climb (yearly)
            self.nat.week(S_)
        return self.week_events
