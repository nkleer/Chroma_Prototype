"""world_react.py: v25 lane C, the life's answers to what is asked of it (Emren's decisions #2, #3 and #4).

The engine's `react` switch (and `clash`, `seek` on top of it), world on only; off, nothing here exists. The design is
What shapes a life's chroma-ideas/life-drivers-2026-10-20/v25-specs.md; the names are the Engine's contracts
(chroma-engine/notes/v25/contracts.md sections 2 to 4, other-shapes.md section 3).

A demand is something a source actually asks of a life: its household, partner, a parent who lives apart, a close
friend, each setting it is in (class, work, congregation, club, scene, unit and the rest), the state (the town's rule
events) and on Earth nature (a disaster in their town: a process, with stakes, never a colour). Each demand has a
purpose and a method (each in colours as the world reads them: the source's ways, and the channel's reading,
realm_earth.REACT_CHANNEL_READ), stakes (needs, aims, commitments, means), and the source's power (dependence),
legitimacy (trust) and control. Once a month (and in any week the caller hands demands in, P["scn"]) each source makes a
demand at its own rate, and each demand gets one response drawn from explainable odds (a logit over the six RESPONSES,
by named terms; infeasible ones are not drawn: no exit, nobody to negotiate with); the player's pick at a clash moment
is honoured. The five layers stay apart: the reaction (a state), the act, the learning (trust in the source, what works
with it), the consequences (ties, access, the place: recorded as footprints) and value development, a step
c' = (1 - a) c + a q on the life's colours, q by the response (backlash toward an alternative actually in reach, never an
inversion; constrained obedience none toward the demand). A source's demand replaces its part of the niche's social
pull and of the steady current for that month (no double counting); a's scale comes from the part it replaces, so a life
accepting everything moves as it did before.

Realm-ready: sources, channels, responses, the terms and the colours are core; what a channel reads as, the age of
standing and which institutions exist are realm data. A magic realm's temple, guild or court asks through the same
channels; a realm whose data gives its forest a voice may give nature demands of its own (here nature asks nothing).
"""
import numpy as np
from world_keys import RESPONSES, CHANNELS, CLASH_KINDS, STATES, GROUP_KINDS, SPHERES, CAUGHT_TAGS, ODD_TAGS
from realm_earth import REACT_CHANNEL_READ, REACT_ADULT_AGE

C = 5
NR = len(RESPONSES)
ACC, ADO, NEG, DIS, BAC, WDR = (RESPONSES.index(r_) for r_ in ("accept", "adopt", "negotiate", "disagree", "backlash", "withdraw"))
CH = {c_: i_ for i_, c_ in enumerate(CHANNELS)}
ST = {s_: i_ for i_, s_ in enumerate(STATES)}
SPH = {s_: i_ for i_, s_ in enumerate(SPHERES)}
G = {g_: i_ for i_, g_ in enumerate(GROUP_KINDS)}
# the named terms of the response odds (each about -1..1); the "why" key the Library words for each
TERMS = ("trust", "control", "dependence", "conviction", "method", "split", "alternative", "need", "aim", "age",
         "history", "exit", "warmth", "agency", "firm")
TI = {t_: i_ for i_, t_ in enumerate(TERMS)}
WHY_OF = dict(trust="why_trust", control="why_control", dependence="why_dependence", conviction="why_conviction",
              method="why_conviction", split="why_conviction", alternative="why_alternative", need="why_need",
              aim="why_aim", age="why_age", history="why_history", exit="why_exit", warmth="why_trust",
              agency="why_dependence", firm="why_conviction")
# each group kind as a source: its kind, channel, sphere (None: its setting's own) and monthly demand rate at full
# involvement (provisional [C]); the household's channel turns to pressure when its control is high
SRC_KIND = {"household": ("person", "attach", "care", 0.35), "class": ("body", "routine", "learn", 0.15),
            "work": ("body", "incentive", None, 0.15), "congregation": ("body", "routine", "faith", 0.10),
            "club": ("gathering", "activity", "gather", 0.06), "scene": ("gathering", "encounter", "gather", 0.06),
            "online": ("gathering", "encounter", "gather", 0.04), "neighbours": ("gathering", "belonging", "gather", 0.04),
            "gang": ("gathering", "pressure", "prot", 0.10), "unit": ("state", "enforce", "prot", 0.20),
            "ward": ("state", "provision", "care", 0.10), "movement": ("gathering", "activity", "rule", 0.06)}
PERSONS = ("partner", "parent", "friend")   # the slots after the settings, then nature, then the state

REACT_DEFAULT = dict(
    # the odds: response -> {term: weight}, and a bias each (provisional [M], explainable: the two largest terms of the
    # response drawn are its why)
    coef=dict(accept=dict(trust=1.4, control=-1.2, dependence=0.3, conviction=1.6, method=0.6, alternative=-0.3, need=1.0,
                          aim=0.8, age=-0.3, history=-0.8, warmth=1.0),
              adopt=dict(trust=0.3, control=-0.3, split=2.0, aim=0.6, conviction=0.3),
              negotiate=dict(trust=0.6, control=-0.6, dependence=-1.2, agency=1.5, warmth=0.4),
              disagree=dict(warmth=1.2, control=-1.0, dependence=-0.4, conviction=-1.2, firm=1.0, age=0.8),
              backlash=dict(trust=-0.6, control=1.6, conviction=-1.2, method=-0.8, need=-1.0, age=1.2, history=0.8,
                            alternative=0.6, warmth=-0.8),
              withdraw=dict(exit=1.5, alternative=0.5, dependence=-1.2, warmth=-0.6)),
    bias=dict(accept=0.3, adopt=-0.3, negotiate=-0.6, disagree=-0.2, backlash=-0.8, withdraw=-0.8),
    rate_k=1.0,            # x every source's demand rate
    person_rate=dict(partner=0.15, parent=0.08, friend=0.06), state_rate=0.5, nature_rate=1.0,
    resp_a=dict(accept=1.2, adopt=0.6, negotiate=0.5, disagree=0.3, backlash=0.8, withdraw=0.6),   # x the part replaced
    sig_k=1.0, teen_k=0.5, a_max=0.15,   # significance: x (1 + sig_k x stakes + teen_k x adolescence), a at most a_max
    constrained=0.3,       # dependence x control at which disagreeing or rejecting stays outward compliance (no exit)
    alt_min=0.05,          # an alternative's reach x what it offers below this: none in reach (backlash stays inward)
    learn=dict(accept=0.02, adopt=0.01, negotiate=0.03, negotiate_fail=-0.02, disagree=0.0, disagree_cold=-0.01,
               backlash=-0.04, withdraw=-0.02, constrained=-0.03, broken=-0.03),
    griev_add=0.15, griev_half=3.0,   # constrained obedience's grievance, and its half-life in years
    recip=dict(strict=0.05, close=0.03, local=0.02),   # reciprocity: a tie's control after talks, closeness after
    # backlash, a place's local practice after talks (x the life's standing there)
    states_half=dict(boredom=0.25, frustration=0.5, anger=0.15, content=0.5, low_mood=1.0),   # years
    log_keep=40,
)
CLASH_DEFAULT = dict(
    thr=0.25,              # the stakes at which a demand that conflicts with an aim, need or commitment is a clash
    age=10.0, sphere_yrs=2.0, decade_n=3,   # ceilings, provisional [C]: from age 10; one per sphere in 2 years; 3 in 10
    a_major=0.08,          # a clash's colour step, at full stakes (a major demand: 0.05 to 0.15 once)
    merge_cos=0.8,         # two demands one dispute: the same stake and purposes this alike
    wait=26,               # weeks a carried clash (or a seeking moment) waits for an ask to replace, before the clash is
                           # answered in the background (the seeking moment is dropped)
)
SEEK_DEFAULT = dict(
    k_max=1.0 / 3,         # attraction's share of the encounter mix at full independence (Emren's starting suggestion)
    self_w=0.4, need_w=0.25, aim_w=0.25, cur_w=0.2, relief_w=0.15,   # attraction's motives
    bored_cur=1.0,         # boredom's lift of curiosity
    dim_k=2.0,             # diminishing returns: the same kind of encounter again gives exp(-dim_k x its share lately)
    content_k=0.5,         # contentment keeps a satisfying life stable: k x (1 - content_k x content)
    try_p=0.04, try_gap=0.25,   # monthly chance of trying a new place, at an attraction this far from what surrounds them
    exp_mem=0.2,           # how far one experience revises expectations
)


def _norm(x):
    x = np.maximum(x, 0.0)
    s_ = x.sum(-1, keepdims=True)
    return np.where(s_ > 1e-12, x / np.maximum(s_, 1e-12), 1.0 / C)


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def _centre(x):
    return x - x.mean(-1, keepdims=True)


class React:
    """One run's reactions (and clashes, seeking) over N lives in WorldLink WL. The engine calls month() each fourth week
    (and week() for the caller's demands), reads dnic (this month's change to the niche pull), cur_parts() and takes
    dz (the colour steps, then cleared) into its integrate step."""

    def __init__(self, N, P, seed, WL, FR, clash=False, seek=False):
        self.N = N; self.WL = WL; self.PP = WL.PP; self.FR = np.asarray(FR, float)
        self.FRc = self.FR - self.FR.mean(1, keepdims=True)   # the tension, centred: an even mix sits with anything at 0
        self._nmp = None
        rp = dict(REACT_DEFAULT); rp.update(P.get("react_par") or {}); self.p = rp
        cp = dict(CLASH_DEFAULT); cp.update(P.get("clash_par") or {}); self.cp = cp
        sp = dict(SEEK_DEFAULT); sp.update(P.get("seek_par") or {}); self.sp = sp
        self.clash_on = bool(clash); self.seek_on = bool(seek); self.scn_on = bool(P.get("scn"))
        self.rng = np.random.default_rng([int(seed), 2525])
        M = self.M = self.PP.M; self.J = M + len(PERSONS) + 2
        self.JN = M + len(PERSONS); self.JS = M + len(PERSONS) + 1   # nature's slot, the state's
        COEF = np.zeros((NR, len(TERMS))); BIAS = np.zeros(NR)
        for r_, d_ in rp["coef"].items():
            for t_, v_ in d_.items():
                COEF[RESPONSES.index(r_), TI[t_]] = v_
        for r_, v_ in rp["bias"].items():
            BIAS[RESPONSES.index(r_)] = v_
        self.COEF, self.BIAS = COEF, BIAS
        self.RA = np.array([rp["resp_a"][r_] for r_ in RESPONSES])
        self.CHR = np.array([np.zeros(C) if REACT_CHANNEL_READ.get(c_) is None else np.asarray(REACT_CHANNEL_READ[c_], float)
                             for c_ in CHANNELS])
        self.CH_OWN = np.array([REACT_CHANNEL_READ.get(c_) is None for c_ in CHANNELS])
        J = self.J
        self.griev = np.zeros((N, J)); self.ndem = np.zeros((N, J)); self.dtr = np.zeros((N, J))   # grievance, demands met,
        self.ndis = np.zeros((N, J))     # learned trust in a setting; disagreements in a row (a tie's control moves after them)
        self.key_t = np.full((N, J), -1, np.int64)   # the source key each slot held (a new setting starts again)
        self.active = np.zeros((N, J), bool)         # a demand this month: its part of the pull is the demand's
        self.dnic = np.zeros((N, C)); self.dz = np.zeros((N, C))
        self.rm_close = None; self.rm_rows = None    # this month's removals from the current's close and places parts
        self.st_lv = np.zeros((N, len(STATES))); self.st_wk = np.zeros((N, len(STATES)), np.int64)
        self.demands = [[] for _ in range(N)]; self.responses = [[] for _ in range(N)]
        self.log = [[] for _ in range(N)]; self.involve = [{} for _ in range(N)]
        self.scn_demand = [[] for _ in range(N)]; self.scn_cast = []; self.scn_missed = []
        self.states_list = [None] * N; self.seek_list = [None] * N
        self.n_id = 0
        self.count = np.zeros((len(SRC_KIND) + len(PERSONS) + 2, NR), np.int64)   # responses by source kind
        self.drift_by = np.zeros(len(SRC_KIND) + len(PERSONS) + 2)                # colour step (half L1) by source kind
        self.n_constrained = 0; self.n_inner = 0; self.n_drift = 0
        self.ev_i = len(getattr(WL.W, "sph_ev_log", ()))
        self._ev_ask = None
        self._last_m = -1
        # clashes (clash, decision #3)
        self.clash = [None] * N; self.clash_now = [[] for _ in range(N)]; self.disputes = [[] for _ in range(N)]
        self.cl_last = np.full((N, len(SPHERES)), -10 ** 9, np.int64); self.cl_hist = [[] for _ in range(N)]
        self.cl_wk = [[] for _ in range(N)]   # every clash put: (week, sphere, stakes), for the record and the checks
        self.carry = {}   # life -> dispute id of a clash waiting for its moment
        self.cl_stats = dict(put=0, carried=0, background=0, merged=0, repeat_held=0, ceiling=0, by_colour_only=0,
                             replaced=0, dropped_natural=0, family={k_: 0 for k_ in CLASH_KINDS},
                             give_in={k_: 0 for k_ in ("willing", "strategic", "constrained")}, by_sphere=np.zeros(len(SPHERES), np.int64))
        self.d_id = 0
        # seeking (seek, decision #4)
        self.attr = np.full((N, C), 1.0 / C); self.k_ind = np.zeros(N); self.enc = np.full((N, C), 1.0 / C)
        self.expect = np.zeros((N, C)); self.tried = [[] for _ in range(N)]
        self.sk_stats = dict(tries=0, admitted=0, refused=0, no_access=0, good=0, bad=0)
        self._pend_try = []

    # ------------------------------------------------------------------ the sources
    def _ind(self, age, held_car, res_mon, res_fre):
        """Independence 0..1 from the life's circumstances: its own home, its own income, standing by age (a soft ramp
        around the realm's age of standing, one part among four, never a switch) and its freedom."""
        PP = self.PP
        own = np.asarray(PP.own_home, float)
        inc = np.clip(0.7 * held_car + 0.3 * np.clip((res_mon - 0.2) / 0.4, 0, 1) * (age >= 15), 0, 1)
        return np.clip(0.25 * own + 0.3 * inc + 0.3 * _sig((age - REACT_ADULT_AGE) / 1.5) + 0.15 * res_fre, 0, 1)

    def _sources(self, age, ctx):
        """(per source slot) its mix, weights in the niche and the current, involvement, warmth, legitimacy, control,
        dependence, exit and talk, sphere, kind and channel; every array (N, J)."""
        PP = self.PP; N, M, J = self.N, self.M, self.J
        f = np.float64
        sk = np.asarray(PP.skind, np.int64); act = sk >= 0; skc = np.maximum(sk, 0)
        mix = np.full((N, J, C), 1.0 / C); wn = np.zeros((N, J)); wcl = np.zeros((N, J)); wpl = np.zeros((N, J))
        warm = np.zeros((N, J)); leg = np.full((N, J), 0.5); ctl = np.zeros((N, J)); dep = np.zeros((N, J))
        exit_ = np.zeros((N, J), bool); talk = np.zeros((N, J), bool); bel = np.zeros((N, J))
        sph = np.full((N, J), -1, np.int64); kind = np.full((N, J), -1, np.int64); chan = np.zeros((N, J), np.int64)
        rate = np.zeros((N, J)); ok = np.zeros((N, J), bool)
        close_w = float(PP.P.get("close_w", 0.15) or 0.15)
        wg, csum, cw = getattr(PP, "_rx_close", (None, None, None))
        K = PP.K
        wgK = np.zeros(N * K)
        if wg is not None:
            np.add.at(wgK, np.asarray(PP._fi).ravel(), np.asarray(wg, f).ravel())
        wgK = wgK.reshape(N, K)
        self._wgK = wgK; self._hh_mb = {}
        sw = np.asarray(getattr(PP, "_rx_sw", np.zeros((N, M))), f)
        ind = ctx["ind"]
        hhj = np.asarray(PP.hhj, np.int64); own = np.asarray(PP.own_home, bool); psl = np.asarray(PP.pslot, np.int64)
        used = PP.used & PP.lv; c = np.asarray(PP.c, f); tr = np.asarray(PP.trust, f); strict = _sig(np.asarray(PP.strict, f))
        pie = np.asarray(PP.pie, f); rm = np.asarray(PP.rmask)
        import world_people_base as WB
        BIT = WB.BIT
        setsph = np.asarray(PP.set_sphere, np.int64) if hasattr(PP, "set_sphere") else np.full((N, M), -1)
        ar = np.arange(N)
        bt = ctx.get("btrust")
        # the settings
        for j in range(M):
            a_ = act[:, j]
            if not a_.any():
                continue
            kn = np.array([GROUP_KINDS[x_] for x_ in skc[:, j]])
            mix[:, j] = np.where(a_[:, None], np.asarray(PP.snorm[:, j], f), 1.0 / C)
            wn[:, j] = np.where(a_, sw[:, j], 0.0)
            warm[:, j] = np.asarray(PP.scoh[:, j], f)
            ctl[:, j] = np.clip(np.asarray(PP.sstrict[:, j], f), 0, 1)
            sp_ = np.array([SPH[SRC_KIND[k_][2]] if SRC_KIND[k_][2] else -1 for k_ in kn])
            sph[:, j] = np.where(sp_ >= 0, sp_, setsph[:, j])
            kind[:, j] = skc[:, j]
            chan[:, j] = np.array([CH[SRC_KIND[k_][1]] for k_ in kn])
            rate[:, j] = np.array([SRC_KIND[k_][3] for k_ in kn])
            rk_ = np.asarray(PP.srank[:, j], f)
            bl_ = bt[ar, np.maximum(sph[:, j], 0)] if bt is not None else np.full(N, np.nan)
            leg[:, j] = np.where(np.isnan(bl_), 0.45 + 0.2 * rk_, 0.5 * bl_ + 0.25 + 0.1 * rk_)
            bel[:, j] = np.clip(0.5 * warm[:, j] + 0.5 * rk_, 0, 1)
            ok[:, j] = a_
            hh_ = a_ & (sk[:, j] == G["household"])
            parents_ = hh_ & ~own & (hhj == j)
            dep[:, j] = np.select([parents_, hh_, sk[:, j] == G["class"], sk[:, j] == G["work"], sk[:, j] == G["unit"],
                                   sk[:, j] == G["ward"], sk[:, j] == G["congregation"]],
                                  [np.clip(1 - ind, 0, 1), 0.2, 0.1 + 0.6 * _sig((16 - age) / 1.5),
                                   0.3 + 0.5 * (1 - ctx["res_mon"]), 0.8, 0.7, 0.15 + 0.2 * ctx["faith_i"]], 0.1)
            exit_[:, j] = np.select([parents_, hh_, sk[:, j] == G["class"], sk[:, j] == G["work"],
                                     (sk[:, j] == G["unit"]) | (sk[:, j] == G["ward"])],
                                    [ind > 0.55, False, ind >= 0.4, ind >= 0.4, False], (age >= 14) | (ind >= 0.3))
            rg_ = np.asarray(PP.rung, f)[ar, np.maximum(sph[:, j], 0)] if getattr(PP, "rung", None) is not None else np.zeros(N)
            talk[:, j] = np.select([(sk[:, j] == G["unit"]) | (sk[:, j] == G["ward"]), (sk[:, j] == G["class"]) | (sk[:, j] == G["work"])],
                                   [rg_ >= 3, (rk_ >= 0.4) | (ctl[:, j] < 0.6)], warm[:, j] > 0.2)
            if hh_.any():   # the household: its ways and its members (the partner apart), one source
                mb_ = ((rm >= 0) & used & (((np.asarray(PP.mset).astype(np.int64) >> j) & 1) > 0)
                       & (np.arange(K)[None, :] != psl[:, None]) & hh_[:, None])
                mw_ = close_w * wgK * mb_
                mws_ = mw_.sum(1)
                mix[:, j] = np.where(hh_[:, None], (sw[:, j, None] * mix[:, j] + (mw_[..., None] * pie).sum(1))
                                     / np.maximum(sw[:, j] + mws_, 1e-12)[:, None], mix[:, j])
                wn[:, j] += np.where(hh_, mws_, 0.0)
                wcl[:, j] = np.where(hh_, mws_ / close_w, 0.0)
                cm_ = np.where(mb_, c, 0.0); n_ = np.maximum(mb_.sum(1), 1)
                warm[:, j] = np.where(hh_, np.where(mb_.any(1), cm_.sum(1) / n_, warm[:, j]), warm[:, j])
                leg[:, j] = np.where(hh_ & mb_.any(1), np.where(mb_, tr, 0).sum(1) / n_, leg[:, j])
                ctl[:, j] = np.where(hh_ & mb_.any(1), np.maximum(ctl[:, j], np.where(mb_, strict, 0).sum(1) / n_), ctl[:, j])
                talk[:, j] = np.where(hh_, (leg[:, j] >= 0.35) & (ctl[:, j] < 0.85), talk[:, j])
                chan[:, j] = np.where(hh_ & (ctl[:, j] > 0.6), CH["pressure"], chan[:, j])
                self._hh_mb[j] = mb_
        # the places part of the current (sph_hours' rows: work 0, class 1, congregation 3, unit 5)
        rows = getattr(PP, "_rx_rows", None)
        if rows is not None:
            wt, _ = rows; tot_ = np.maximum(wt.sum(1), 1e-12)
            for g_, r_ in (("work", 0), ("class", 1), ("congregation", 3), ("unit", 5)):
                h_ = act & (sk == G[g_])
                first_ = h_ & (np.cumsum(h_, 1) == 1)
                wpl[:, :M] += first_ * (wt[:, r_] / tot_)[:, None]
        else:
            wpl[:, :M] = sw / np.maximum(sw.sum(1, keepdims=True), 1e-12)
        # the persons: the partner, a parent living apart (after leaving home), the closest friend
        kin = (rm & WB.KINMASK) != 0 if hasattr(WB, "KINMASK") else np.zeros_like(rm, bool)
        live = used & (c >= 0.2)
        is_par = live & ((rm & BIT["parent"]) != 0)
        is_fr = live & (((rm & BIT["friend"]) != 0) | ((rm & BIT["mentor"]) != 0)) & ~kin & (np.arange(K)[None] != psl[:, None])
        pk = np.full((N, len(PERSONS)), -1, np.int64)
        pk[:, 0] = np.where((psl >= 0) & live[ar, np.maximum(psl, 0)], psl, -1)
        cp_ = np.where(is_par & own[:, None], c, -1.0); pk[:, 1] = np.where(cp_.max(1) >= 0, cp_.argmax(1), -1)
        cf_ = np.where(is_fr, c, -1.0); pk[:, 2] = np.where(cf_.max(1) >= 0, cf_.argmax(1), -1)
        self._pk = pk
        yrs_par = ctx["par_yrs"]
        for i_, nm_ in enumerate(PERSONS):
            j = M + i_; k_ = np.maximum(pk[:, i_], 0); h_ = pk[:, i_] >= 0
            ok[:, j] = h_
            mix[:, j] = np.where(h_[:, None], pie[ar, k_], 1.0 / C)
            wn[:, j] = np.where(h_, close_w * wgK[ar, k_], 0.0); wcl[:, j] = np.where(h_, wgK[ar, k_], 0.0)
            warm[:, j] = np.where(h_, c[ar, k_], 0.0); leg[:, j] = np.where(h_, tr[ar, k_], 0.5)
            ctl[:, j] = np.where(h_, strict[ar, k_], 0.0); bel[:, j] = warm[:, j]
            sph[:, j] = SPH["gather"] if nm_ == "friend" else SPH["care"]
            kind[:, j] = len(GROUP_KINDS) + i_
            chan[:, j] = CH["example"] if nm_ == "friend" else np.where(ctl[:, j] > 0.6, CH["pressure"], CH["attach"])
            rate[:, j] = self.p["person_rate"][nm_]
            dep[:, j] = {"partner": 0.3 + 0.4 * own * np.clip(yrs_par / 5, 0, 1), "parent": 0.1 + 0.2 * (1 - ctx["held_car"]),
                         "friend": np.full(N, 0.05)}[nm_]
            exit_[:, j] = ind >= (0.5 if nm_ == "partner" else 0.3)
            talk[:, j] = h_ & (leg[:, j] >= 0.35) & (ctl[:, j] <= 0.85)
        # nature and the state: no ways of their own in the pull; they ask only on their events
        for j, nm_ in ((self.JN, "nature"), (self.JS, "state")):
            kind[:, j] = len(GROUP_KINDS) + len(PERSONS) + (0 if nm_ == "nature" else 1)
            sph[:, j] = SPH["prod"] if nm_ == "nature" else SPH["rule"]
            chan[:, j] = CH["process"] if nm_ == "nature" else CH["rule"]
            dep[:, j] = (0.3 + 0.5 * ctx["farm"]) if nm_ == "nature" else 0.5
            exit_[:, j] = (ind >= 0.5) if nm_ == "nature" else False
            rg_ = np.asarray(PP.rung, f)[:, SPH["rule"]] if getattr(PP, "rung", None) is not None else np.zeros(N)
            talk[:, j] = False if nm_ == "nature" else (rg_ >= 3)
            ctl[:, j] = 0.5; warm[:, j] = 0.5   # impersonal: no warmth either way
            leg[:, j] = 0.5 if nm_ == "nature" else (0.5 * np.nan_to_num(bt[:, SPH["rule"]], nan=0.5) + 0.25
                                                                        if bt is not None else 0.5)
        leg = np.clip(leg + self.dtr, 0, 1)
        return dict(mix=mix, wn=wn, wcl=wcl, wpl=wpl, warm=warm, leg=leg, ctl=ctl, dep=dep, exit=exit_, talk=talk, bel=bel,
                    sph=sph, kind=kind, chan=chan, rate=rate, ok=ok, wgK=wgK, sw=sw, csum=csum, cw=cw, close_w=close_w)

    def nmap(self, ix):
        """Each life's own needs-to-colours table (the engine's NMP), for these lives."""
        return self._nmp[ix]

    @staticmethod
    def kind_name(k):
        if k < 0:
            return None
        if k < len(GROUP_KINDS):
            return GROUP_KINDS[k]
        k -= len(GROUP_KINDS)
        return PERSONS[k] if k < len(PERSONS) else ("nature", "state")[k - len(PERSONS)]

    def fit(self, X, y):
        """How far mix X sits with mix y as the world reads colours, -1..1 (overlap, less the framing's tension, centred so
        that an even mix sits at 0 with anything)."""
        return np.tanh(2.0 * (5.0 * (X * y).sum(-1) - 1.0) - 8.0 * ((X @ self.FRc) * y).sum(-1))

    # ------------------------------------------------------------------ the month: demands and responses
    def _events(self, t, loc):
        """The town's sphere events since the last month (World.sph_ev_log: week, event, town or -1), each with its ask
        (its own sphere's faces, W U B R G, the positive part): [(life, sphere, ask)] for the lives in that town."""
        W = self.WL.W; lg = getattr(W, "sph_ev_log", None)
        if lg is None or not len(lg):
            return []
        rows = lg[self.ev_i:]; self.ev_i = len(lg)
        if not len(rows):
            return []
        if self._ev_ask is None:
            import sphere_data as SD
            ask = np.zeros((len(SD.EV), C))
            for i_, e_ in enumerate(SD.EV):
                for r_ in e_["rows"]:
                    if r_["target"] == e_["sphere"] and r_["faces"]:
                        ask[i_] += r_["faces"]
            self._ev_ask = ask; self._ev_sph = np.array([SPH[e_["sphere"]] for e_ in SD.EV], np.int64)
        out = []
        for wk_, e_, town_ in rows[rows[:, 0] > t - 5]:
            a_ = np.maximum(self._ev_ask[e_], 0)
            if a_.sum() <= 0:
                continue
            for n in np.nonzero((loc == town_) | (town_ < 0))[0]:
                out.append((int(n), int(self._ev_sph[e_]), a_ / a_.sum()))
        return out

    def month(self, t, age, ctx, scn_only=False):
        """One step: the sources' demands this month (scn_only: only the caller's this week), each one's response and its
        layers. ctx: the engine's arrays (w, conv, plast, need, nimp, lack, res, held, I, prof, aims, ...)."""
        N, M, J = self.N, self.M, self.J; rp = self.p; PP = self.PP
        dead = ctx["dead"]
        S_ = self._sources(age, ctx)
        self._S = S_
        rng = self.rng
        self._last_ctx = ctx; self._nmp = ctx["nmp"]
        if not scn_only:
            self.active[:] = False
            new_key = S_["kind"] * 1000 + np.arange(J)[None]
            fresh = new_key != self.key_t
            if fresh.any():   # a new setting in a slot (or a new partner, parent, friend): its history starts again
                self.griev[fresh] = 0; self.ndem[fresh] = 0; self.dtr[fresh] = 0; self.ndis[fresh] = 0
                self.key_t = new_key
            self.griev *= 0.5 ** (1 / (12 * rp["griev_half"]))
        # the demands: each source at its own rate, x its involvement (its part of their sources) and its control
        nd, jd, pur, src = [], [], [], []
        if not scn_only:
            wrel = S_["wn"] / np.maximum(S_["wn"].max(1, keepdims=True), 1e-12)
            p_ = rp["rate_k"] * S_["rate"] * np.clip(0.3 + 0.7 * wrel, 0, 1) * (0.5 + S_["ctl"]) * S_["ok"] * ~dead[:, None]
            p_[:, self.JN:] = 0.0
            hit = rng.random((N, J)) < p_
            for n, j in zip(*np.nonzero(hit)):
                nd.append(n); jd.append(j); pur.append(None); src.append(None)
            for n, sp_, ask_ in self._events(t, ctx["loc"]):   # a sphere event's ask: from their setting in its sphere, or
                if dead[n]:                                       # the state for the rule sphere
                    continue
                js_ = np.nonzero(S_["ok"][n, :M] & (S_["sph"][n, :M] == sp_))[0]
                if len(js_):
                    j_ = int(js_[np.argmax(S_["wn"][n, js_])])
                elif sp_ == SPH["rule"] and rng.random() < rp["state_rate"]:
                    j_ = self.JS
                else:
                    continue
                nd.append(n); jd.append(j_); pur.append(ask_); src.append("event")
            dis_ = ctx.get("dis_own")
            if dis_ is not None:   # nature: a disaster in their town is a condition with stakes (it asks nothing in colours)
                for n in np.nonzero((dis_ > 0) & ~dead)[0]:
                    if rng.random() < rp["nature_rate"]:
                        nd.append(int(n)); jd.append(self.JN); pur.append(np.zeros(C)); src.append(("nature", float(dis_[n])))
        forced = {}
        for n in (range(N) if self.scn_on else ()):   # the caller's (P["scn"]): each as this week's demand, the same path
            for d_ in list(self.scn_demand[n]):
                j_ = self._scn_slot(n, d_)
                if j_ is None:
                    self.scn_missed.append((n, d_.get("tag"), "no such source"))
                    continue
                forced[len(nd)] = d_
                nd.append(n); jd.append(j_); pur.append(np.asarray(d_["purpose"], float) if d_.get("purpose") is not None else None)
                src.append(("scn", d_))
            self.scn_demand[n].clear()
        if not nd:
            return
        nd = np.asarray(nd, np.int64); jd = np.asarray(jd, np.int64); D = len(nd)
        mixd = S_["mix"][nd, jd]
        purpose = np.array([mixd[i_] if p0_ is None else p0_ for i_, p0_ in enumerate(pur)])
        purpose = np.where(purpose.sum(1, keepdims=True) > 0, _norm(purpose - 0.1 * (purpose.sum(1, keepdims=True) > 0)), 0.0)
        purpose = np.where(purpose.sum(1, keepdims=True) > 0, purpose, 0.0)
        purpose[np.array([isinstance(s_, tuple) and s_[0] == "nature" for s_ in src])] = 0.0   # nature asks nothing
        ch = S_["chan"][nd, jd]
        method = np.where(self.CH_OWN[ch][:, None], purpose, 0.5 * purpose + 0.5 * self.CHR[ch])
        method = np.where(method.sum(1, keepdims=True) > 0, _norm(method), 0.0)
        leg = S_["leg"][nd, jd].copy(); ctl = S_["ctl"][nd, jd].copy(); dep = S_["dep"][nd, jd].copy()
        warm = S_["warm"][nd, jd].copy(); ext = S_["exit"][nd, jd].copy(); talk = S_["talk"][nd, jd].copy()
        for i_, s_ in enumerate(src):
            if isinstance(s_, tuple) and s_[0] == "nature":
                ctl[i_] = min(1.0, 0.3 + s_[1])
            if i_ in forced:
                d_ = forced[i_]
                if d_.get("method") is not None:
                    method[i_] = _norm(np.asarray(d_["method"], float))
                for k_, a_ in (("legit", leg), ("control", ctl), ("power", dep)):
                    if d_.get(k_) is not None:
                        a_[i_] = float(d_[k_])
                if d_.get("channel") in CH:
                    ch[i_] = CH[d_["channel"]]
                if d_.get("exit") is not None:
                    ext[i_] = bool(d_["exit"])
                if d_.get("talk") is not None:
                    talk[i_] = bool(d_["talk"])
        nat = ch == CH["process"]
        conv = ctx["conv"][nd]; w = ctx["w"][nd]
        dem = _norm(purpose + method)
        has_c = purpose.sum(1) > 0
        fp = np.where(has_c, self.fit(conv, purpose), 0.0)
        fm = np.where(method.sum(1) > 0, self.fit(conv, method), 0.0)
        # the alternatives: their other settings and close people, by reach x what each offers that the demand denies
        aw, am = self._alts(nd, jd, S_)
        offer = np.maximum(0.0, self.fit(am, conv[:, None, :]) - np.where(has_c[:, None], self.fit(am, dem[:, None, :]), 0.0))
        reach = aw / np.maximum(aw.max(1, keepdims=True), 1e-12)
        ro = reach * offer
        alt_s = ro.max(1)
        q_alt = np.where((ro.sum(1) > 1e-12)[:, None], (ro[..., None] * am).sum(1) / np.maximum(ro.sum(1), 1e-12)[:, None], 0.0)
        q_rest = np.where((aw.sum(1) > 1e-12)[:, None], (aw[..., None] * am).sum(1) / np.maximum(aw.sum(1), 1e-12)[:, None], w)
        # needs, aims and commitments it touches
        lack = ctx["lack"][nd]; nm_ = self.nmap(nd)
        felt = np.einsum("dn,dnc->dc", lack, nm_)
        nmeet = np.where(has_c & (felt.sum(1) > 1e-6),   # no need felt: the demand neither meets nor denies one
                         np.clip(5 * (felt * purpose).sum(1) / np.maximum(felt.sum(1), 1e-9) - 1, -1, 1), 0.0)
        aut = ctx["need_aut"][nd]; aut_thr = ctl * np.clip(0.3 + (0.6 - aut), 0, 1)
        need_t = 0.5 * nmeet - aut_thr
        af, as_ = ctx["aim_face"][nd], ctx["aim_s"][nd]   # (D, A, C), (D, A): aims (or goals) and their strength
        afit = np.where(has_c[:, None], self.fit(af, purpose[:, None, :]), 0.0) * (as_ > 0)
        aim_use = (as_ * np.maximum(afit, 0)).max(1) if af.shape[1] else np.zeros(D)
        aim_conf = (as_ * np.maximum(-afit, 0)).max(1) if af.shape[1] else np.zeros(D)
        held, Ii, prof = ctx["held"][nd], ctx["I"][nd], ctx["prof"][nd]
        own_k = np.array([ctx["kidx"].get(self.kind_name(int(k_)), -1) for k_ in S_["kind"][nd, jd]])
        cfit = np.where(has_c[:, None], self.fit(prof, purpose[:, None, :]), 0.0)
        cc_ = held * Ii * np.maximum(-cfit, 0)
        cc_[np.arange(D)[own_k >= 0], own_k[own_k >= 0]] = 0.0
        com_conf = cc_.max(1) if cc_.shape[1] else np.zeros(D)
        com_k = cc_.argmax(1) if cc_.shape[1] else np.zeros(D, int)
        kn_ = [self.kind_name(int(k_)) for k_ in S_["kind"][nd, jd]]
        hours = np.array([k_ in ("work", "class", "unit") for k_ in kn_]) * ctl
        time_conf = hours * ctx["cares"][nd] * np.clip(1 - ctx["res_tim"][nd], 0, 1)
        need_conf = ctx["nimp_aut"][nd] * (aut < 0.4) * ctl + nat * np.clip(ctl, 0, 1) * ctx["means_low"][nd]
        stakes_sc = np.maximum.reduce([aim_conf, com_conf, time_conf, need_conf]) * (0.5 + 0.5 * np.maximum(ctl, dep))
        for i_, d_ in forced.items():   # the caller's stakes, when given as a number (P["scn"] only), as legit and control
            if isinstance(d_.get("stakes"), (int, float, np.integer, np.floating)) and not isinstance(d_.get("stakes"), bool):
                stakes_sc[i_] = float(d_["stakes"])
        ad = age_d = np.exp(-((age - 15.5) / 2.5) ** 2) * np.ones(D)
        ind = ctx["ind"][nd]
        hist = np.clip(self.griev[nd, jd] * (0.5 + ind) + 0.1 * np.minimum(self.ndis[nd, jd], 5) * (ctl > leg), 0, 1.0)
        bel = S_["bel"][nd, jd]
        firm = np.clip((conv.max(1) - 0.2) / 0.3, 0, 1)
        X = np.zeros((D, len(TERMS)))
        X[:, TI["trust"]] = leg - 0.5; X[:, TI["control"]] = ctl - leg; X[:, TI["dependence"]] = dep
        X[:, TI["conviction"]] = fp; X[:, TI["method"]] = fm; X[:, TI["split"]] = np.abs(fp - fm) * has_c
        X[:, TI["alternative"]] = alt_s; X[:, TI["need"]] = need_t; X[:, TI["aim"]] = aim_use - aim_conf
        X[:, TI["age"]] = ad; X[:, TI["history"]] = hist; X[:, TI["exit"]] = ext * (1 - bel + 0.3 * alt_s)
        X[:, TI["warmth"]] = warm - 0.5; X[:, TI["agency"]] = 0.6 * ind + 0.4 * np.clip(bel, 0, 1); X[:, TI["firm"]] = firm
        Z = X @ self.COEF.T + self.BIAS[None]
        ok = np.ones((D, NR), bool)
        ok[:, NEG] = talk; ok[:, WDR] = ext                   # feasibility first: nobody to talk to, no exit
        ok[nat, BAC] = False; ok[nat, NEG] = False; ok[~has_c, ADO] = False   # nature: nothing to reject or bargain with
        Z = np.where(ok, Z, -np.inf)
        pr = np.exp(Z - Z.max(1, keepdims=True)); pr /= pr.sum(1, keepdims=True)
        r = (pr.cumsum(1) > rng.random((D, 1))).argmax(1)
        byp = np.zeros(D, bool)
        for i_, d_ in forced.items():
            if d_.get("response") in RESPONSES and ok[i_, RESPONSES.index(d_["response"])]:
                r[i_] = RESPONSES.index(d_["response"]); byp[i_] = bool(d_.get("by_player", True))
        dd = dict(nd=nd, jd=jd, purpose=purpose, method=method, ch=ch, leg=leg, ctl=ctl, dep=dep, warm=warm, ext=ext,
                  talk=talk, fp=fp, fm=fm, alt_s=alt_s, q_alt=q_alt, q_rest=q_rest, nmeet=nmeet, aim_use=aim_use,
                  aim_conf=aim_conf, com_conf=com_conf, com_k=com_k, time_conf=time_conf, need_conf=need_conf,
                  stakes=stakes_sc, X=X, Z=Z, ok=ok, pr=pr, src=src, ind=ind, conv=conv, w=w, has_c=has_c, ad=ad,
                  kn=kn_, af=af, as_=as_, forced=forced)
        self._dd = dd
        hold_ = np.zeros(D, bool)
        if self.clash_on:   # a demand with stakes may come as a clash (the clash's own answer then sets its layers)
            hold_ = self._clash_check(t, age, dd, ctx)
        for i_ in np.nonzero(~hold_)[0]:
            self._respond(t, age, dd, i_, int(r[i_]), bool(byp[i_]), ctx)
        self.active[nd, jd] = True
        self._removals(S_, ctx)

    def _scn_slot(self, n, d_):
        """The source slot of a caller's demand: source=dict(key=<a group kind, partner, parent, friend, nature or
        state>) or kind and sphere; None when the life has no such source."""
        s_ = d_.get("source") or {}
        key = s_.get("key") or s_.get("sphere") or s_.get("kind")
        if key in ("nature", "state"):
            return self.JN if key == "nature" else self.JS
        if key in PERSONS:
            i_ = PERSONS.index(key)
            return self.M + i_ if self._pk[n, i_] >= 0 else None
        if key in G:
            js_ = np.nonzero(np.asarray(self.PP.skind[n]) == G[key])[0]
            return int(js_[0]) if len(js_) else None
        if isinstance(s_.get("place"), (int, np.integer)) and 0 <= int(s_["place"]) < self.M:
            return int(s_["place"])
        return None

    def _alts(self, nd, jd, S_):
        """Each demand's alternatives in reach: the life's other settings (by weight) and close people (not the source's),
        (D, M + K) weights and (D, M + K, C) mixes."""
        PP = self.PP; M = self.M; K = PP.K
        sw = S_["sw"][nd].copy()
        sw[np.arange(len(nd))[jd < M], jd[jd < M]] = 0.0
        sm = S_["mix"][nd, :M]
        wk = S_["wgK"][nd].copy()
        for i_ in range(len(PERSONS)):
            on_ = jd == M + i_
            k_ = self._pk[nd[on_], i_]
            wk[np.nonzero(on_)[0][k_ >= 0], k_[k_ >= 0]] = 0.0
        for j_, mb_ in getattr(self, "_hh_mb", {}).items():
            on_ = jd == j_
            wk[on_] = np.where(mb_[nd[on_]], 0.0, wk[on_])
        pie = np.asarray(PP.pie[nd], float)
        return np.concatenate([sw, S_["close_w"] * wk], 1), np.concatenate([sm, pie], 1)

    # ------------------------------------------------------------------ one response and its five layers
    def _q_of(self, dd, i, r, negotiated=True):
        """Value development's direction q for response r to demand i (None: no colour step)."""
        w = dd["w"][i]; pur = dd["purpose"][i]; met = dd["method"][i]
        if not dd["has_c"][i] and r != WDR:
            return None   # nature, or a demand with no colours: nothing to take up (only where they go, if they leave)
        if r == ACC:
            return _norm(pur + met)
        if r == ADO:
            return _norm(w + (pur if dd["fp"][i] >= dd["fm"][i] else met))
        if r == NEG:
            if not negotiated:
                return None
            dem = _norm(pur + met)
            both = np.maximum(0, -(self.FR @ w)) * np.maximum(0, -(self.FR @ dem))   # allies of both, as the world reads them
            shared = np.minimum(w, dem) + (both / both.sum() * 0.5 * np.minimum(w, dem).sum() if both.sum() > 0 else 0)
            return _norm(w + shared)
        if r == DIS:
            c_ = dd["conv"][i] ** 1.5
            return c_ / c_.sum()   # a small firming of what they hold
        if r == BAC:
            return dd["q_alt"][i] if dd["alt_s"][i] >= self.p["alt_min"] else None   # toward an alternative in reach, or none
        if r == WDR:
            return dd["q_rest"][i] if dd["ext"][i] else None   # where they go, by the time spent there
        return None

    def _respond(self, t, age, dd, i, r, by_player, ctx, clash=None, a_k=1.0, succ=None):
        """Response r to demand i: the reaction, the act, the learning, the consequences and the colour step, kept
        apart; the records (S["demands"], S["responses"], S["react_log"]). clash: the dispute when it came as one."""
        rp = self.p; PP = self.PP
        n = int(dd["nd"][i]); j = int(dd["jd"][i]); kn = dd["kn"][i]
        leg, ctl, dep, warm, ext = dd["leg"][i], dd["ctl"][i], dd["dep"][i], dd["warm"][i], dd["ext"][i]
        nat = dd["ch"][i] == CH["process"]
        constrained = (r in (DIS, BAC)) and dep * ctl >= rp["constrained"] and not ext
        neg_ok = True
        if r == NEG:   # talks: part won or not, by their agency against the source's control
            p_ = _sig(2.5 * (dd["X"][i, TI["agency"]] + leg - ctl - 0.3))
            neg_ok = bool(self.rng.random() < p_) if succ is None else bool(succ)
        comply = r in (ACC, ADO) or (r == NEG and neg_ok) or constrained
        convinced = r == ACC or (r == ADO)
        q = self._q_of(dd, i, r, neg_ok)
        if constrained and r == DIS:
            q = None   # constrained obedience: compliance without conviction, no step toward the demand
        # 1. the reaction (a state, never from a colour)
        hab = 1.0 / (1.0 + 0.15 * self.ndem[n, j])   # exposure lowers surprise and anger; it is not acceptance
        st = ("none", 0.0)
        if r == BAC or (constrained and ctl > leg):
            st = ("anger", float(np.clip((max(ctl - leg, 0) + 0.3 * self.griev[n, j] + 0.2) * hab, 0, 1)))
        elif constrained or (nat and r != WDR):
            st = ("frustration", float(np.clip(0.3 + 0.5 * ctl, 0, 1)))
        elif r == ACC and dd["nmeet"][i] > 0:
            st = ("content", float(np.clip(0.3 + 0.5 * dd["nmeet"][i], 0, 1)))
        if st[0] != "none":
            s_ = ST[st[0]]
            self.st_lv[n, s_] = max(self.st_lv[n, s_], st[1])
        # 2. the act
        act = {ACC: "takes it up", ADO: "takes up part of it", NEG: "talks terms" if neg_ok else "talks, without terms",
               DIS: "holds their own view", BAC: "turns away from it", WDR: "steps away" if ext else "withdraws inwardly"}[r]
        if constrained:
            act = "complies outwardly"
        if nat:
            act = {ACC: "adapts to it", DIS: "holds on", WDR: "leaves the land", ADO: "adapts to part of it"}.get(r, act)
        # 3. learning: trust in the source, what works with it, whether its claims held
        lr = rp["learn"]
        held_ = bool(self.rng.random() < 0.5 + 0.4 * (leg - 0.5)) if r in (ACC, ADO) else None
        dtr = {ACC: lr["accept"], ADO: lr["adopt"], NEG: lr["negotiate"] if neg_ok else lr["negotiate_fail"],
               DIS: lr["disagree"] if warm >= 0.5 else lr["disagree_cold"], BAC: lr["backlash"], WDR: lr["withdraw"]}[r]
        if constrained:
            dtr = lr["constrained"]
        if held_ is False:
            dtr += lr["broken"]
        dtr *= 2.0 if clash is not None else 1.0
        effects = []
        if not nat:
            self._trust(n, j, dtr)
            effects.append(dict(foot="tie", who=kn, trust=round(float(dtr), 3)))
        # 4. consequences: reciprocity by power, exits, obligations, grievance
        rc = rp["recip"]
        if r == NEG and neg_ok and j < self.M + len(PERSONS):
            ag = float(dd["X"][i, TI["agency"]])
            self._soften(n, j, rc["strict"] * ag, ctx)
            effects.append(dict(foot="obligation", who=kn, renegotiated=True))
        if r == DIS:
            self.ndis[n, j] += 1
            if self.ndis[n, j] >= 3 and warm >= 0.5:   # a tie that allows disagreement learns to: its control eases
                self._soften(n, j, 0.4 * rc["strict"], ctx)
        else:
            self.ndis[n, j] = 0
        if r == BAC and not nat:
            self._strain(n, j, rc["close"])
            effects.append(dict(foot="tie", who=kn, strained=True))
        if constrained:
            self.griev[n, j] += rp["griev_add"] * ctl; self.n_constrained += 1
            effects.append(dict(foot="obligation", who=kn, kept_outwardly=True))
        if r == WDR and ext:
            effects.append(self._exit(n, j, t, kn))
        elif r == WDR:
            self.n_inner += 1
        if comply and not constrained and not nat:
            effects.append(dict(foot="obligation", who=kn, kept=True))
        # 5. value development: c' = (1 - a) c + a q, a from the part of the pull the demand replaced
        drift = None
        if q is not None:
            a = self._a(n, j, r, dd, i, ctx, clash, a_k)
            if a > 0:
                wv = dd["w"][i]
                dz = _centre(np.log((1 - a) * wv + a * q) - np.log(np.maximum(wv, 1e-12)))
                self.dz[n] += dz
                ki_ = int(self._S["kind"][n, j])
                self.drift_by[ki_] += 0.5 * np.abs((1 - a) * wv + a * q - wv).sum(); self.n_drift += 1
                drift = dict(q=[round(float(x_), 3) for x_ in q], a=round(float(a), 4))
        self.ndem[n, j] += 1
        self.count[int(self._S["kind"][n, j]), r] += 1
        # the records
        Xi = dd["X"][i]; con = self.COEF[r] * Xi
        top = [TERMS[x_] for x_ in np.argsort(-np.abs(con)) if abs(con[x_]) > 1e-9]
        why = list(dict.fromkeys(WHY_OF[x_] for x_ in top))[:2]
        self.n_id += 1
        dm = self._demand_rec(t, dd, i, self.n_id)
        rs = dict(demand=dm["id"], response=RESPONSES[r], by_player=bool(by_player), state=dict(kind=st[0], level=round(st[1], 3)),
                  act=act, learn=dict(trust=round(float(dtr), 3), works=float(neg_ok) if r == NEG else None, held=held_),
                  effects=effects, drift=drift, comply=bool(comply), convinced=bool(convinced and not constrained),
                  purpose_ok=bool(dd["fp"][i] > 0), method_ok=bool(dd["fm"][i] > 0), why=why,
                  constrained=bool(constrained), odds={RESPONSES[k_]: round(float(dd["pr"][i, k_]), 3) for k_ in range(NR)})
        if dm.get("tag") is not None:
            rs["tag"] = dm["tag"]
        if clash is not None:
            rs["clash"] = clash
        self.demands[n].append(dm); self.responses[n].append(rs)
        lg = self.log[n]; lg.append(dict(t=int(t), age=round(float(age), 2), demand=dm["id"], source=dm["source"], tag=dm.get("tag"),
                                         response=RESPONSES[r], layers=dict(state=rs["state"], act=act, learn=rs["learn"],
                                                                            effects=effects, drift=drift),
                                         comply=rs["comply"], convinced=rs["convinced"], why=why, clash=clash))
        if len(lg) > rp["log_keep"]:
            del lg[0]
        return rs

    def _demand_rec(self, t, dd, i, id_):
        n = int(dd["nd"][i]); j = int(dd["jd"][i]); kn = dd["kn"][i]
        s_ = dd["src"][i]
        kind = SRC_KIND[kn][0] if kn in SRC_KIND else ("person" if kn in PERSONS else kn)
        cid = int(self.PP.uid[n, self._pk[n, PERSONS.index(kn)]]) if kn in PERSONS else -1
        sp = int(self._S["sph"][n, j])
        stakes = dict(needs=[x_ for x_, v_ in (("autonomy", dd["need_conf"][i]), ("safety", dd["need_conf"][i] * (dd["ch"][i] == CH["process"])))
                             if v_ > 0.05],
                      aims=[int(x_) for x_ in np.nonzero(dd["as_"][i] * np.maximum(-self.fit(dd["af"][i], dd["purpose"][i][None]), 0) > 0.1)[0]]
                      if dd["has_c"][i] and dd["af"].shape[1] else [],
                      commitments=[int(dd["com_k"][i])] if dd["com_conf"][i] > 0.1 else [],
                      means=round(float(dd["dep"][i]), 3), access=[kn] if dd["ext"][i] else [],
                      score=round(float(dd["stakes"][i]), 3))
        rec = dict(id=id_, week=int(t), source=dict(kind=kind, key=kn, sphere=SPHERES[sp] if sp >= 0 else None, cid=cid,
                                                     place=j if j < self.M else -1),
                   channel=CHANNELS[int(dd["ch"][i])], purpose=[round(float(x_), 3) for x_ in dd["purpose"][i]],
                   method=[round(float(x_), 3) for x_ in dd["method"][i]], stakes=stakes, power=round(float(dd["dep"][i]), 3),
                   legit=round(float(dd["leg"][i]), 3), control=round(float(dd["ctl"][i]), 3))
        if isinstance(s_, tuple) and s_[0] == "scn":
            rec["tag"] = s_[1].get("tag"); rec["by"] = "caller"
        elif s_ == "event":
            rec["by"] = "event"
        return rec

    def _a(self, n, j, r, dd, i, ctx, clash, a_k):
        """The experience's significance: the part of the pull its source holds (so taking everything up moves a life as
        before), x the response's factor, x (1 + stakes + adolescence), x dependence for the household, a parent, a
        partner and work; a clash's at least a_major x its stakes. At most a_max."""
        rp = self.p; S_ = self._S
        base = ctx["a_nic"][n] * S_["wn"][n, j] / max(ctx["tot_nic"][n], 1e-12) \
            + ctx["a_cl"][n] * S_["wcl"][n, j] / max(ctx["tot_cl"][n], 1e-12) + ctx["a_pl"][n] * S_["wpl"][n, j]
        kn = dd["kn"][i]; dep = dd["dep"][i]
        fd = (0.6 + 0.8 * dep) if kn in ("household", "parent") else (0.8 + 0.6 * dep) if kn in ("partner", "work") else 1.0
        a = base * self.RA[r] * fd * (1 + rp["sig_k"] * dd["stakes"][i] + rp["teen_k"] * dd["ad"][i]) * a_k
        if clash is not None:
            a = max(a, self.cp["a_major"] * min(1.0, dd["stakes"][i] / max(self.cp["thr"], 1e-9)) * self.RA[r] / self.RA[ACC])
        if dd["forced"].get(i, {}).get("a") is not None:
            a = float(dd["forced"][i]["a"])
        return float(min(max(a, 0.0), rp["a_max"]))

    def _trust(self, n, j, dtr):
        PP = self.PP; M = self.M
        if j < M and int(PP.skind[n, j]) == G["household"] and j in getattr(self, "_hh_mb", {}):
            mb = self._hh_mb[j][n]
            PP.trust[n, mb] = np.clip(PP.trust[n, mb] + dtr, 0, 1)
        elif M <= j < M + len(PERSONS):
            k = self._pk[n, j - M]
            if k >= 0:
                PP.trust[n, k] = np.clip(PP.trust[n, k] + dtr, 0, 1)
                return
        self.dtr[n, j] = float(np.clip(self.dtr[n, j] + dtr, -0.4, 0.4))

    def _soften(self, n, j, x, ctx):
        """Reciprocity by power: a person's control eases after talks or a disagreement it learnt to allow; a group's local
        practice (not an institution's or the state's) moves toward theirs by their standing there."""
        PP = self.PP; M = self.M
        if M <= j < M + len(PERSONS):
            k = self._pk[n, j - M]
            if k >= 0:
                PP.strict[n, k] -= np.float32(x * 4)   # strict is read through a sigmoid: 4 x near its middle
        elif j < M and PP.skind[n, j] >= 0:
            kn = GROUP_KINDS[int(PP.skind[n, j])]
            if kn in ("household", "club", "scene", "online", "neighbours", "gang", "movement", "work"):
                k_ = self.p["recip"]["local"] * (float(PP.srank[n, j]) if kn != "household" else ctx["ind"][n] + 0.5)
                PP.snorm[n, j] = _norm(PP.snorm[n, j] + k_ * (ctx["w"][n] - PP.snorm[n, j])).astype(np.float32)
                if kn == "household" and j in getattr(self, "_hh_mb", {}):
                    mb = self._hh_mb[j][n]
                    PP.strict[n, mb] -= np.float32(x * 2)

    def _strain(self, n, j, x):
        PP = self.PP; M = self.M
        if M <= j < M + len(PERSONS):
            k = self._pk[n, j - M]
            if k >= 0:
                PP.c[n, k] = max(0.0, float(PP.c[n, k]) - x)
        elif j < M and j in getattr(self, "_hh_mb", {}):
            mb = self._hh_mb[j][n]
            PP.c[n, mb] = np.maximum(0.0, PP.c[n, mb] - np.float32(x))

    def _exit(self, n, j, t, kn):
        """Withdrawal where an exit exists: home left (the world's own leaving home), a voluntary group left, school or
        work kept with less of their time (the engine's commitments decide quitting), a tie stepped back from."""
        PP = self.PP; M = self.M
        if j < M and PP.skind[n, j] >= 0:
            g_ = GROUP_KINDS[int(PP.skind[n, j])]
            if g_ == "household" and not PP.own_home[n]:
                PP._leave_home(int(n), int(PP.t)); return dict(foot="access", left="home")
            if g_ in ("club", "scene", "online", "neighbours", "gang", "movement", "congregation"):
                PP._leave(int(n), int(j), int(PP.t), "left"); return dict(foot="access", left=g_)
            PP.sts[n, j] *= np.float32(0.8); return dict(foot="access", less_time=g_)
        if M <= j < M + len(PERSONS):
            self._strain(n, j, 0.05); return dict(foot="tie", who=kn, stepped_back=True)
        return dict(foot="place", left=kn)

    def _removals(self, S_, ctx):
        """This month's change to the niche's pull and the current's parts, for the sources whose demand replaced theirs."""
        N, M = self.N, self.M
        act = self.active
        wn, mix = S_["wn"], S_["mix"]
        rn = (act[..., None] * wn[..., None] * mix).sum(1); rd = (act * wn).sum(1)
        tot = ctx["tot_nic"]; msc = ctx["msc"]
        ok = (rd > 0) & (tot - rd > 1e-9)
        msc2 = np.where(ok[:, None], (msc * tot[:, None] - rn) / np.maximum(tot - rd, 1e-9)[:, None], msc)
        self.dnic = (1 - ctx["tw"]) * (msc2 - msc)
        # the current: the close part without the persons (household members, partner, parent, friend) whose demand came
        wcl = S_["wcl"]; csum, cw = S_["csum"], S_["cw"]
        if csum is not None:
            pr_ = (act * wcl).sum(1)
            pn_ = (act[..., None] * wcl[..., None] * mix).sum(1)
            ok2 = (pr_ > 0) & (cw - pr_ > 1e-9)
            self.rm_close = (ok2, np.where(ok2[:, None], (csum - pn_) / np.maximum(cw - pr_, 1e-9)[:, None], 0.0))
        rows = getattr(self.PP, "_rx_rows", None)
        wpl = (act * S_["wpl"])
        if rows is not None and wpl.any():
            pl_ = np.asarray(self.PP.places_mix, float); sh_ = wpl.sum(1)
            pn_ = (wpl[..., None] * mix).sum(1)
            ok3 = (sh_ > 0) & (sh_ < 1 - 1e-9)
            self.rm_rows = (ok3, np.where(ok3[:, None], (pl_ - pn_) / np.maximum(1 - sh_, 1e-9)[:, None], 0.0))
        else:
            self.rm_rows = None

    def cur_parts(self, cl_, st_):
        """The current's close and places parts with this month's replaced sources out."""
        if self.rm_close is not None:
            ok, v = self.rm_close; cl_ = np.where(ok[:, None], v, cl_)
        if self.rm_rows is not None:
            ok, v = self.rm_rows; st_ = np.where(ok[:, None], v, st_)
        return cl_, st_

    def take_dz(self):
        dz = self.dz; self.dz = np.zeros_like(dz)
        return dz

    # ------------------------------------------------------------------ states (situational and wellbeing, never colours)
    def states_month(self, t, ctx):
        """Each month: the states fade by their half-lives and are read again from their causes; durations count weeks
        held at .3 or more. Returns (stress, mood) changes, the states' contextual effects."""
        hl = self.p["states_half"]
        for s_, i_ in ST.items():
            self.st_lv[:, i_] *= 0.5 ** (1 / (12 * hl[s_]))
        f_need = ctx["f_need"]
        tg = np.clip((f_need - 0.55) / 0.3, 0, 1)                                   # contentment: important needs met
        self.st_lv[:, ST["content"]] += 0.25 * (tg - self.st_lv[:, ST["content"]])
        fr_ = ctx["aim_block"]                                                      # frustration: a valued aim blocked
        self.st_lv[:, ST["frustration"]] = np.maximum(self.st_lv[:, ST["frustration"]], fr_)
        en_ = np.clip(ctx["engage"], 0, 1)                                          # boredom: engagement against need
        bo_ = np.clip(0.5 * (ctx["lack_comp"] + ctx["lack_mean"]) + 0.5 * (1 - en_) - 0.5 * ctx["stress"] - 0.25, 0, 1)
        self.st_lv[:, ST["boredom"]] += 0.3 * (bo_ - self.st_lv[:, ST["boredom"]])
        lm_ = np.clip((0.45 - ctx["content"]) / 0.2, 0, 1)                          # persistent low mood: months of low wellbeing
        up_ = lm_ > self.st_lv[:, ST["low_mood"]]
        self.st_lv[:, ST["low_mood"]] += np.where(up_, 0.08, 0.3) * (lm_ - self.st_lv[:, ST["low_mood"]])
        self.st_lv = np.clip(self.st_lv, 0, 1)
        self.st_wk = np.where(self.st_lv >= 0.3, self.st_wk + 4, 0)
        ds = 0.05 * self.st_lv[:, ST["anger"]] + 0.03 * self.st_lv[:, ST["frustration"]]
        dm = -0.02 * self.st_lv[:, ST["low_mood"]]
        return ds, dm

    def states_view(self):
        self.states_list[:] = [{s_: dict(level=round(float(self.st_lv[n, i_]), 3), weeks=int(self.st_wk[n, i_]))
                                for s_, i_ in ST.items()} for n in range(self.N)]
        return self.states_list

    def week_reset(self):
        """A new week: this week's demands, responses and clash start empty (the lists stay the same objects)."""
        for x_ in self.demands:
            x_.clear()
        for x_ in self.responses:
            x_.clear()
        self.clash[:] = [None] * self.N

    def involve_year(self, ctx):
        """Yearly: each source's involvement in the life: its share of their time and company, the needs it meets
        (lack it answers), and their dependence on it (S["involve"])."""
        S_ = getattr(self, "_S", None)
        if S_ is None:
            return
        tot = np.maximum(ctx["tot_nic"], 1e-12)
        felt = np.einsum("nd,ndc->nc", ctx["lack_all"], self.nmap(np.arange(self.N)))
        fn = felt / np.maximum(felt.sum(1, keepdims=True), 1e-12)
        for n in range(self.N):
            d_ = {}
            for j in np.nonzero(S_["ok"][n])[0]:
                kn = self.kind_name(int(S_["kind"][n, j])); key = kn if kn not in d_ else f"{kn}.{j}"
                d_[key] = dict(time=round(float(S_["wn"][n, j] / tot[n]), 3),
                               needs=round(float(5 * (fn[n] * S_["mix"][n, j]).sum() - 1), 3), dependence=round(float(S_["dep"][n, j]), 3))
            self.involve[n] = d_

    # ------------------------------------------------------------------ clashes (clash, decision #3)
    def set_lib(self, L):
        """The batch's clash moments (the Library's <world>_clash.py, loaded with the clash switch): by setting and band."""
        self.CL_S = {}; self.CLASH_TAG = None; self.SK_S = {}; self.RP_S = []; self.SEEK_TAG = None; self.REPAIR_TAG = None
        self.AGE = np.asarray(L["AGE"])
        if L.get("W_STATE") is not None:   # the Library's seeking moments (state:) and repair moments (repair: options)
            ws_ = np.asarray(L["W_STATE"]); rt_ = np.asarray(L["REPAIR_TAG"])
            self.SEEK_TAG = np.asarray(L["SEEK_TAG"]); self.REPAIR_TAG = rt_
            for s_ in np.nonzero(ws_ >= 0)[0]:
                self.SK_S.setdefault(int(ws_[s_]), []).append(int(s_))
            self.RP_S = [int(s_) for s_ in np.nonzero((rt_ >= 0).any(1) & (ws_ < 0))[0]]
        cs = L.get("W_CLASH")
        if cs is None:
            return
        self.CLASH_TAG = np.asarray(L["CLASH_TAG"])
        band = np.asarray(L.get("W_BAND", np.full(len(cs), -1)))
        for s_ in np.nonzero(np.asarray(cs) >= 0)[0]:
            self.CL_S.setdefault((int(cs[s_]), int(band[s_])), []).append(int(s_))

    CLASH_SET = ("household", "school", "work", "congregation", "town", "group", "land")   # the Library's clash: settings

    def _setting_of(self, kn):
        return {"household": 0, "partner": 0, "parent": 0, "class": 1, "work": 2, "congregation": 3, "state": 4, "unit": 4,
                "ward": 4, "nature": 6}.get(kn, 5)

    def _dd_sub(self, dd, i):
        out = {}
        for k_, v_ in dd.items():
            if isinstance(v_, np.ndarray) and v_.ndim and len(v_) == len(dd["nd"]):
                out[k_] = v_[i:i + 1].copy()
            elif isinstance(v_, list) and len(v_) == len(dd["nd"]):
                out[k_] = v_[i:i + 1]
            else:
                out[k_] = v_
        out["forced"] = {0: dd["forced"][i]} if i in dd["forced"] else {}
        return out

    def _stake_key(self, dd, i):
        v = dict(aim=dd["aim_conf"][i], commit=dd["com_conf"][i], time=dd["time_conf"][i], need=dd["need_conf"][i])
        k_ = max(v, key=v.get)
        if v[k_] <= 0:   # stakes the caller gave (P["scn"]) with none of the life's own: the caller's dispute
            return ("given",)
        if k_ == "aim":
            af = dd["af"][i]; as_ = dd["as_"][i]
            return ("aim", int(np.argmax(as_ * np.maximum(-self.fit(af, dd["purpose"][i][None]), 0))))
        if k_ == "commit":
            return ("commit", int(dd["com_k"][i]))
        return (k_,)

    def _stakes_say(self, dd, i, key):
        """What is at stake, in the shape the Game reads (contracts.md section 3): aims (aim indices), needs (names),
        commitments (kind names), means (time or money), access; with the dispute key and the stakes score."""
        import engine as _E
        out = dict(key=list(key), score=round(float(dd["stakes"][i]), 3), aims=[], needs=[], commitments=[], means=False,
                   access=[])
        if key[0] == "aim":
            out["aims"] = [int(key[1])]
        elif key[0] == "commit":
            out["commitments"] = [_E.KNAMES[int(key[1])]] if 0 <= int(key[1]) < len(_E.KNAMES) else []
        elif key[0] == "time":
            out["means"] = True
        elif key[0] == "need":
            if dd["ch"][i] == CH["process"]:
                out["means"] = True   # nature: their livelihood
            else:
                out["needs"] = ["autonomy"]
        return out

    def _feasible(self, dd, i):
        return dict(confront=True, give_in=True, leave=bool(dd["ext"][i]), own_scene=bool(dd["alt_s"][i] >= self.p["alt_min"]),
                    bridge=bool(dd["talk"][i]))

    def _give_in_as(self, dd, i):
        if dd["fp"][i] > 0.2 and dd["leg"][i] >= 0.5:
            return "willing"
        if dd["dep"][i] * dd["ctl"][i] >= self.p["constrained"] and not dd["ext"][i]:
            return "constrained"
        return "strategic"

    def _clash_check(self, t, age, dd, ctx):
        """Demands with real stakes against an aim, need or commitment come as clashes, within the ceilings; connected
        ones merge; an open dispute is not put again while nothing in it changed. Returns the demands handled here."""
        cp = self.cp; D = len(dd["nd"]); hold = np.zeros(D, bool)
        if age < cp["age"]:
            return hold
        cand = np.nonzero(dd["stakes"] >= cp["thr"])[0]
        # colour alone never starts one: count the demands whose colours oppose theirs but carry no stakes
        self.cl_stats["by_colour_only"] += int(((dd["fp"] < -0.3) & (dd["stakes"] < cp["thr"])).sum())
        done = set()
        for i in cand:
            if i in done:
                continue
            n = int(dd["nd"][i]); j = int(dd["jd"][i])
            key = self._stake_key(dd, i)
            group = [i] + [i2 for i2 in cand if i2 != i and i2 not in done and dd["nd"][i2] == n and dd["jd"][i2] != j
                           and self._stake_key(dd, i2) == key
                           and float(dd["purpose"][i] @ dd["purpose"][i2]) / max(np.linalg.norm(dd["purpose"][i]) * np.linalg.norm(dd["purpose"][i2]), 1e-9) >= cp["merge_cos"]]
            done.update(group)
            holders = [dd["kn"][g_] for g_ in group]
            sp = int(self._S["sph"][n, j]); sps = sorted({int(self._S["sph"][n, int(dd["jd"][g_])]) for g_ in group})
            feas = self._feasible(dd, i)
            sig_ = (round(float(dd["stakes"][i]), 1), round(float(dd["dep"][i]), 1), tuple(sorted(k_ for k_, v_ in feas.items() if v_)))
            dsp = None
            for d0 in self.disputes[n]:   # an open dispute on the same stake, a purpose alike: the same dispute
                if d0["open"] and d0["key"] == list(key):
                    dsp = d0; break
            if dsp is not None:
                new_h = [h_ for h_ in holders if h_ not in dsp["holders"]]
                if new_h:
                    dsp["holders"] += new_h; self.cl_stats["merged"] += 1
                if not new_h and dsp["sig"] == list(sig_[:2]) + [list(sig_[2])]:
                    self.cl_stats["repeat_held"] += 1
                    continue   # unchanged: not put again (the demand is answered in the background as any other)
            if len(group) > 1:
                self.cl_stats["merged"] += len(group) - 1
            yrs = np.asarray(self.cl_hist[n]); dec_ = int(((t - yrs) < 520).sum()) if len(yrs) else 0
            touched = sorted({max(s_, 0) for s_ in sps} | ({SPHERES.index(x_) for x_ in dsp["spheres"]} if dsp is not None else set()))
            if any(t - self.cl_last[n, s_] < 52 * cp["sphere_yrs"] for s_ in touched) or dec_ >= cp["decade_n"]:
                # (every sphere the dispute touches: one a sphere in 2 years, whichever sphere it comes through)
                self.cl_stats["ceiling"] += 1
                continue
            # a clash: one dispute, its holders, its stakes, its feasible options
            if dsp is None:
                self.d_id += 1
                dsp = dict(id=self.d_id, key=list(key), since=int(t), last_asked=-1, changed=int(t), holders=holders,
                           spheres=[SPHERES[s_] for s_ in sps if s_ >= 0], open=True, family=None, give_in_as=None,
                           stake=list(key), sig=None, n_asked=0)
                self.disputes[n].append(dsp)
            dsp["sig"] = list(sig_[:2]) + [list(sig_[2])]; dsp["last_asked"] = int(t); dsp["changed"] = int(t); dsp["n_asked"] += 1
            dsp["setting_id"] = j if j < self.M else -1; dsp["sphere"] = SPHERES[sp] if sp >= 0 else None
            dsp["k"] = round(float(dd["stakes"][i]), 3)
            for s_ in touched:
                self.cl_last[n, s_] = t
                if SPHERES[s_] not in dsp["spheres"]:
                    dsp["spheres"].append(SPHERES[s_])
            self.cl_hist[n].append(int(t)); self.cl_wk[n].append((int(t), list(touched), float(dd["stakes"][i])))
            self.cl_stats["put"] += 1; self.cl_stats["by_sphere"][max(sp, 0)] += 1
            gia = self._give_in_as(dd, i)
            setting = self._setting_of(dd["kn"][i])
            hold[group] = True
            rec = dict(id=dsp["id"], demand=dict(key=dd["kn"][i], sphere=SPHERES[sp] if sp >= 0 else None,
                                                 purpose=[round(float(x_), 3) for x_ in dd["purpose"][i]]), spheres=dsp["spheres"], holders=list(dsp["holders"]), stakes=self._stakes_say(dd, i, key), options=[k_ for k_, v_ in feas.items() if v_], give_in_as=gia,
                       sphere=SPHERES[sp] if sp >= 0 else None, setting_id=j if j < self.M else -1, k=round(float(dd["stakes"][i]), 3),
                       setting=self.CLASH_SET[setting], holder=self._holder(n, j), ally=self._ally(n, j), scene=self._scene(n, dd, i),
                       carried=False)
            sub = self._dd_sub(dd, i)
            band = 0 if age < 20 else 1
            av_ = getattr(self, "avail", None)   # (the moments open to them this week: stage, age, conditions, once)
            ss = [s_ for s_ in getattr(self, "CL_S", {}).get((setting, band), []) if self.AGE[s_, 0] <= age <= self.AGE[s_, 1]
                  and (av_ is None or av_[n, s_])]
            if ss and n not in self.carry:   # the Library's clash moment for it: it waits for its week, as a want's moment does
                s_ = ss[int(self.rng.integers(len(ss)))]
                self.carry[n] = dict(dispute=dsp, sub=sub, s=s_, t=int(t), rec=rec, feas=feas, gia=gia, group=[dd["kn"][g_] for g_ in group])
                rec["carried"] = True; rec["moment"] = int(s_); self.cl_stats["carried"] += 1
            else:   # no moment for it: answered in the background, by the same odds
                self.cl_stats["background"] += 1
                r = int((dd["pr"][i].cumsum() > self.rng.random()).argmax())
                fr_ = dd["forced"].get(i, {}).get("response")   # the caller's response (P["scn"]), when feasible
                if fr_ in RESPONSES and dd["ok"][i, RESPONSES.index(fr_)]:
                    r = RESPONSES.index(fr_)
                self._clash_apply(t, age, n, dsp, sub, r, False, ctx, rec, gia, succ=None)
            self.clash[n] = rec
        return hold

    def _holder(self, n, j):
        if self.M <= j < self.M + len(PERSONS):
            k = self._pk[n, j - self.M]
            return int(self.PP.uid[n, k]) if k >= 0 else -1
        if j < self.M and j in getattr(self, "_hh_mb", {}):
            mb = np.nonzero(self._hh_mb[j][n])[0]
            if len(mb):
                return int(self.PP.uid[n, mb[np.argmax(self.PP.c[n, mb])]])
        return -1

    def _ally(self, n, j):
        """A person both sides trust (for a bridge): their most trusted close person who is not the holder."""
        PP = self.PP; h = self._holder(n, j)
        ok = PP.used[n] & PP.lv[n] & (PP.c[n] >= 0.3) & (PP.trust[n] >= 0.6) & (PP.uid[n] != h)
        ks = np.nonzero(ok)[0]
        return int(PP.uid[n, ks[np.argmax(PP.trust[n, ks])]]) if len(ks) else -1

    def _scene(self, n, dd, i):
        """The setting or place an own_scene option finds: the life's other setting that fits them best, or -1."""
        S_ = self._S; M = self.M
        js = [j_ for j_ in range(M) if S_["ok"][n, j_] and j_ != dd["jd"][i]]
        if not js:
            return -1
        f_ = self.fit(S_["mix"][n, js], dd["conv"][i][None])
        return int(js[int(np.argmax(f_))])

    FAMILY_RESP = {"confront": None, "give_in": ACC, "leave": WDR, "own_scene": BAC, "bridge": NEG}

    def _clash_apply(self, t, age, n, dsp, sub, r_or_family, by_player, ctx, rec, gia, succ=None):
        """A clash answered: by the player's or the life's pick of a family (CLASH_KINDS), or a drawn response; its
        layers through _respond with a clash's weight, and the dispute's state."""
        if isinstance(r_or_family, str):
            fam = r_or_family
            r = self.FAMILY_RESP[fam]
            if r is None:   # confronting: a secure stand in a warm tie, a backlash in a cold one
                r = DIS if sub["warm"][0] >= 0.5 else BAC
        else:
            r = r_or_family
            fam = {ACC: "give_in", ADO: "give_in", NEG: "bridge", DIS: "confront", WDR: "leave"}.get(r, None)
            if r == BAC:
                fam = "own_scene" if sub["alt_s"][0] >= self.p["alt_min"] else "confront"
        if fam == "give_in" and r in (ACC, ADO) and gia != "willing":   # strategic: outward, no inward step; constrained:
            r = DIS if gia == "constrained" else ADO                      # obedience (no step, grievance)
            sub = dict(sub); sub["has_c"] = sub["has_c"] if gia == "constrained" else np.zeros(1, bool)
            if gia == "constrained":
                sub["ext"] = np.zeros(1, bool); sub["dep"] = np.maximum(sub["dep"], 1.0); sub["ctl"] = np.maximum(sub["ctl"], self.p["constrained"])
        rs = self._respond(t, age, sub, 0, r, by_player, ctx, clash=dsp["id"], succ=succ)
        rs["family"] = fam; rs["give_in_as"] = gia if fam == "give_in" else None
        self.cl_stats["family"][fam] += 1
        if fam == "give_in":
            self.cl_stats["give_in"][gia] += 1
        # the dispute: settled, or left open (not asked again until something in it changes)
        if fam == "confront":
            p_ = _sig(3 * (float(sub["X"][0, TI["agency"]]) - float(sub["dep"][0] * sub["ctl"][0]))) if succ is None else float(succ)
            dropped = bool(self.rng.random() < p_) if succ is None else bool(succ)
            rs["outcome"] = "dropped" if dropped else "enforced"
            if dropped:
                self._soften(n, int(sub["jd"][0]), 0.1, ctx)
            else:
                self.griev[n, int(sub["jd"][0])] += 0.5 * self.p["griev_add"]
            dsp["open"] = not dropped
        elif fam == "bridge":
            ok_ = rs["learn"]["works"]
            rs["outcome"] = "renegotiated" if ok_ else "no terms"
            dsp["open"] = not ok_
        elif fam == "own_scene":
            rs["outcome"] = "sought another scene"
            if self.seek_on:
                self._try_entry(t, n, sub["q_alt"][0] if sub["alt_s"][0] >= self.p["alt_min"] else sub["conv"][0], "relief")
            dsp["open"] = True
        else:
            rs["outcome"] = {"give_in": "gave in", "leave": "left"}[fam]
            dsp["open"] = False
        dsp["family"] = fam; dsp["give_in_as"] = rs["give_in_as"]; dsp["outcome"] = rs["outcome"]
        rec["demand"] = rs["demand"]; rec["answer"] = dict(family=fam, response=rs["response"], outcome=rs["outcome"],
                                                             by_player=bool(by_player))
        return rs

    def clash_week(self, t, WL):
        """After the world's week: each clash waiting for its moment past clash_par wait weeks is answered in the
        background (v25_fire brings the moment in a week with an ask it can take the place of)."""
        for n, c_ in list(self.carry.items()):
            if t - c_["t"] > self.cp["wait"]:
                del self.carry[n]
                sub = c_["sub"]; r = int((sub["pr"][0].cumsum() > self.rng.random()).argmax())
                self._clash_apply(t, t / 52.0, n, c_["dispute"], sub, r, False, self._last_ctx, c_["rec"], c_["gia"])
                c_["rec"]["carried"] = False; self.cl_stats["background"] += 1

    def _open(self, n, s_):
        av_ = getattr(self, "avail", None)
        return av_ is None or bool(av_[n, s_])

    def clash_on_week(self, s):
        """This week's carried clash moments: {life: carry} for the lives whose moment s is theirs."""
        return {n: c_ for n, c_ in self.carry.items() if int(s[n]) == c_["s"]}

    def clash_mask(self, s, mask):
        """The infeasible families' options are not offered (no exit, nobody to talk to, no other scene in reach)."""
        if self.CLASH_TAG is None:
            return mask
        on = self.clash_on_week(s)
        if not on:
            return mask
        mask = mask.copy()
        for n, c_ in on.items():
            tg = self.CLASH_TAG[c_["s"]]
            for k_ in range(min(len(tg), mask.shape[1])):
                if tg[k_] >= 0 and not c_["feas"][CLASH_KINDS[tg[k_]]]:
                    mask[n, k_] = False
        return mask

    def clash_pull(self, s, K):
        """(N, K) log odds an unplayed life adds to each option of its clash moment: the response odds of its family."""
        u = np.zeros((self.N, K))
        if self.CLASH_TAG is None:
            return u
        for n, c_ in self.clash_on_week(s).items():
            z_ = c_["sub"]["Z"][0]; tg = self.CLASH_TAG[c_["s"]]
            fz = {"confront": np.logaddexp(z_[DIS], z_[BAC]), "give_in": np.logaddexp(z_[ACC], z_[ADO]), "leave": z_[WDR],
                  "own_scene": z_[BAC] if c_["feas"]["own_scene"] else -np.inf, "bridge": z_[NEG]}
            for k_ in range(min(len(tg), K)):
                if tg[k_] >= 0 and np.isfinite(fz[CLASH_KINDS[tg[k_]]]):
                    u[n, k_] = fz[CLASH_KINDS[tg[k_]]]
            u[n] -= u[n][np.isfinite(u[n])].mean() if np.isfinite(u[n]).any() else 0.0
        return np.where(np.isfinite(u), u, 0.0)

    def clash_answer(self, t, s, a, succ, idle, players):
        """After the act: a carried clash moment answered (its option's family; the player's pick for a played life)."""
        for n, c_ in self.clash_on_week(s).items():
            del self.carry[n]
            self.cl_stats["replaced"] += 1
            tg = self.CLASH_TAG[c_["s"]]; k_ = int(a[n])
            fam = CLASH_KINDS[tg[k_]] if 0 <= k_ < len(tg) and tg[k_] >= 0 and not idle[n] else "give_in"
            self._clash_apply(t, t / 52.0, n, c_["dispute"], c_["sub"], fam, n in players, self._last_ctx, c_["rec"],
                              c_["gia"], succ=bool(succ[n]))
            self.clash[n] = c_["rec"]

    def v25_fire(self, fire, frc, WL):
        """The question budget: a clash, seeking or repair moment waiting is put only in a week that already holds an
        optional ask for that life, and takes its place: a life event drawn by its rate (the moment is preferred, as the
        world's are), or a caught-between or odd-one-out moment the world brought (dropped; S3 and S4 keep their state).
        Never in place of anything else the world brings (a death, a birth, a want's or a decision's moment). frc is
        changed in place."""
        PP = self.PP
        waiting = [(n, c_["s"], "clash") for n, c_ in self.carry.items()] + \
                  [(n, c_["s"], "seek") for n, c_ in getattr(self, "sk_carry", {}).items() if n not in self.carry]
        for n, s_, k_ in waiting:
            if not self._open(n, s_) or PP.dead[n]:
                continue
            pend = WL.pending.get(n)
            eyes = pend is not None and pend[1] in ("caught", "odd")
            other = frc[n].copy()
            if eyes:
                other[pend[2]] = False
            if other.any():
                continue   # the world brings something else this week: it waits
            if eyes:
                frc[n, pend[2]] = False; fire[n, pend[2]] = False; WL.pending.pop(n, None)
                PP.eyes_q.pop(n, None); PP.eyes_off.pop(n, None)
                self.cl_stats["dropped_natural"] += 1
            elif not fire[n].any():
                continue   # no ask this week to take the place of
            else:
                self.cl_stats["replaced_event"] = self.cl_stats.get("replaced_event", 0) + 1
            frc[n, s_] = True
            if k_ == "clash":   # S["clash"]: the clash this week's moment puts (the Game's card)
                self.clash[n] = self.carry[n]["rec"]

    # ------------------------------------------------------------------ seeking (seek, decision #4)
    def seek_month(self, t, age, ctx):
        """Attraction (what draws them), apart from access, attempted entry and experience. Seeking moves attraction only:
        a new place comes through its own access and admission, and its colours only through living there."""
        sp = self.sp; N = self.N
        conv = ctx["conv"]; ind = ctx["ind"]
        felt = np.einsum("nd,ndc->nc", ctx["lack_all"], self.nmap(np.arange(N)))
        need_ = _norm(felt + 1e-9)
        aim_ = _norm((ctx["aim_s"][..., None] * ctx["aim_face"]).sum(1) + 1e-9) if ctx["aim_face"].shape[1] else np.full((N, C), 0.2)
        cur_ = _norm(np.maximum(0.3 - self.enc, 0) + 1e-3)   # curiosity: the colours they have met least lately
        bored = self.st_lv[:, ST["boredom"]]
        rel_ = getattr(self, "relief", np.full((N, C), 0.2))
        pres = np.clip(self.st_lv[:, ST["anger"]] + self.st_lv[:, ST["frustration"]], 0, 1)
        mot = dict(belong=sp["self_w"] * np.ones(N), instrumental=sp["need_w"] * np.ones(N), curious=sp["cur_w"] * (1 + sp["bored_cur"] * bored),
                   challenge=sp["aim_w"] * np.ones(N), relief=sp["relief_w"] * pres)
        A = (mot["belong"][:, None] * conv + mot["instrumental"][:, None] * need_ + mot["challenge"][:, None] * aim_
             + mot["curious"][:, None] * cur_ + mot["relief"][:, None] * rel_)
        A = A * np.exp(-sp["dim_k"] * (self.enc - 0.2)) * np.exp(np.clip(self.expect, -1, 1))   # diminishing returns; expectations
        self.attr = _norm(A)
        content = self.st_lv[:, ST["content"]]
        self.k_ind = sp["k_max"] * ind * (1 - sp["content_k"] * content)
        self.motives = mot
        # attempted entry: now and then, where what draws them is far from what surrounds them
        gap = 0.5 * np.abs(self.attr - ctx["nic"]).sum(1)
        p_ = sp["try_p"] * np.clip((gap - sp["try_gap"]) / 0.2, 0, 1) * (1 + bored) * (ind >= 0.3) * ~ctx["dead"]
        for n in np.nonzero(self.rng.random(N) < p_)[0]:
            mk_ = max(("belong", "instrumental", "curious", "challenge", "relief"), key=lambda k_: mot[k_][n])
            self._try_entry(t, int(n), self.attr[n], mk_)
        # experience: half a year in, how it went there revises what they expect (attraction can shift either way)
        for n, it in self._pend_try[:]:
            if t - it["t"] >= 26:
                self._pend_try.remove((n, it))
                p_ = it.get("place", -1)
                if p_ < 0 or p_ not in self.PP.hnt[n]:
                    it["experience"] = "left"
                    continue
                hp = self.PP.W.hp_s.reshape(-1, C)[p_]
                f_ = float(self.fit(hp, ctx["w"][n])) + 0.5 * (float(ctx["belong"][n]) - 0.5)
                it["experience"] = "good" if f_ > 0 else "bad"
                self.sk_stats["good" if f_ > 0 else "bad"] += 1
                self.expect[n] += sp["exp_mem"] * np.sign(f_) * (np.asarray(hp, float) - 0.2) * 5
                self.expect[n] = np.clip(self.expect[n], -1, 1)

    def _try_entry(self, t, n, mix, motive):
        """An attempt at entry: access (a place of that face in their town, open at their age), then admission (its gate,
        their independence and means); admitted, they go there (People.pick_haunt). Never a colour step."""
        PP = self.PP
        sph = {"belong": "gather", "instrumental": "comm", "curious": "learn", "challenge": "arts", "relief": "gather"}[motive]
        col = int(np.argmax(mix))
        self.sk_stats["tries"] += 1
        rec = dict(t=int(t), age=round(t / 52.0, 2), motive=motive, colour="WUBRG"[col], sphere=sph, access=False, admitted=False,
                   place=-1, experience=None)
        if not getattr(PP, "sph_h", False):
            self.sk_stats["no_access"] += 1
            self.tried[n].append(rec); return rec
        ind = float(self._last_ctx["ind"][n]) if getattr(self, "_last_ctx", None) else 0.5
        mon = float(self._last_ctx["res_mon"][n]) if getattr(self, "_last_ctx", None) else 0.5
        rec["access"] = True
        p_admit = float(np.clip(0.25 + 0.35 * ind + 0.3 * mon, 0.05, 0.95))
        if self.rng.random() < p_admit:
            p_ = PP.pick_haunt(n, sph, col)
            if p_ < 0 and sph != "gather":
                p_ = PP.pick_haunt(n, "gather", col)
            rec["admitted"] = p_ >= 0; rec["place"] = int(p_); rec["access"] = p_ >= 0   # no such place open to them: no access
        self.sk_stats["admitted" if rec["admitted"] else "refused" if rec["access"] else "no_access"] += 1
        self.tried[n].append(rec)
        if len(self.tried[n]) > 20:
            del self.tried[n][0]
        if rec["admitted"]:
            self._pend_try.append((n, rec))
        return rec

    def seek_draw_mix(self, nic):
        """The encounter mix of the moment draw: (1 - k) x surroundings + k x attraction, k by actual independence."""
        return (1 - self.k_ind)[:, None] * nic + self.k_ind[:, None] * self.attr

    def seek_view(self):
        self.seek_list[:] = [dict(attraction=[round(float(x_), 3) for x_ in self.attr[n]],
                     motives={k_: round(float(v_[n]), 3) for k_, v_ in getattr(self, "motives", {}).items()},
                     k=round(float(self.k_ind[n]), 3), tried=list(self.tried[n])) for n in range(self.N)]
        return self.seek_list

    def encounter(self, a_mix, live):
        """Weekly: what they met this week (the moment's colours), a running mean over about half a year."""
        self.enc = np.where(live[:, None], self.enc + (_norm(a_mix) - self.enc) / 26.0, self.enc)

    def aim_block(self, t, astr, astep):
        """Frustration's cause: a valued aim (strength .4 or more) with no step for over a year, by how long."""
        N = self.N
        if astr is None:
            return np.zeros(N)
        sm = np.asarray(astep).sum(1)
        last = getattr(self, "_astep", None)
        if last is None or len(last) != N:
            self._astep = sm.copy(); self._astep_t = np.full(N, t)
        moved = sm != self._astep
        self._astep_t = np.where(moved, t, self._astep_t); self._astep = sm.copy()
        return np.asarray(astr).max(1) * (np.asarray(astr).max(1) >= 0.4) * np.clip((t - self._astep_t) / 52 - 1, 0, 1)

    def engage(self, tries):
        """Engagement this month: the wanted attempts made (the engine's tries), about three a month at full."""
        last = getattr(self, "_tries", None)
        d_ = np.asarray(tries, float) - (last if last is not None else np.asarray(tries, float))
        self._tries = np.asarray(tries, float).copy()
        return np.clip(d_ / 3.0, 0, 1)

    def clash_now_update(self):
        """S["clash_now"]: each life's open disputes with stakes .25 or more: dict(sphere, setting_id, k, id)."""
        for n in range(self.N):
            self.clash_now[n][:] = [dict(sphere=d_.get("sphere"), setting_id=d_.get("setting_id", -1), k=d_.get("k", 0.0), id=d_["id"])
                                    for d_ in self.disputes[n] if d_["open"] and d_.get("k", 0) >= 0.25]

    # ------------------------------------------------------------------ what they can do about a state; a tie's repair
    SEEK_W = dict(boredom=dict(deepen=1.0, method=0.8, own_interest=0.8, help=0.2, revise=0.3, withdraw=0.2, persist=-0.3, keep=-0.5),
                  frustration=dict(revise=0.8, help=0.8, persist=0.4, negotiate=0.5, method=0.5, withdraw=0.3, keep=-0.3),
                  anger=dict(negotiate=0.8, withdraw=0.6, help=0.3, persist=-0.3, keep=-0.5),
                  content=dict(keep=1.0, deepen=0.5, persist=0.3, withdraw=-0.5, revise=-0.5),
                  low_mood=dict(help=1.0, own_interest=0.3, withdraw=0.3, deepen=-0.2))

    def seek_week(self, t, WL, age):
        """After the world's week: a state held (.5 or more, eight weeks) brings its seeking moment once a year at most; a
        tie with the partner gone sour (trust under .45, or a backlash or forced compliance with them lately) brings a
        repair moment once in two years at most. Each waits up to clash_par wait weeks, as a clash does, and takes the
        place of the next caught-between or odd-one-out ask."""
        if not self.SK_S and not self.RP_S:
            return
        if not hasattr(self, "sk_carry"):
            self.sk_carry = {}; self.sk_last = np.full((self.N, len(STATES)), -10 ** 9); self.rp_last = np.full(self.N, -10 ** 9)
        for n, c_ in list(self.sk_carry.items()):
            if t - c_["t"] > self.cp["wait"]:
                del self.sk_carry[n]
        if t % 4:
            return
        live = ~self.PP.dead
        for n in np.nonzero(live)[0]:
            if n in self.sk_carry or n in self.carry:
                continue
            ss, kind = [], None
            pk = self._pk[n, 0] if hasattr(self, "_pk") else -1
            sour = pk >= 0 and (self.PP.trust[n, pk] < 0.45 or any(r_.get("source", {}).get("key") == "partner" and
                                                               r_["response"] in ("backlash", "disagree") and t - r_["t"] < 13
                                                               for r_ in self.log[n][-5:]))
            if sour and t - self.rp_last[n] >= 104 and self.RP_S:
                ss = [s_ for s_ in self.RP_S if self.AGE[s_, 0] <= age <= self.AGE[s_, 1] and self._open(n, s_)]; kind = "repair"
            if not ss:
                for st_ in np.argsort(-self.st_lv[n]):
                    if (self.st_lv[n, st_] >= 0.5 and self.st_wk[n, st_] >= 8 and t - self.sk_last[n].max() >= 52   # one a year
                            and st_ in self.SK_S):
                        ss = [s_ for s_ in self.SK_S[st_] if self.AGE[s_, 0] <= age <= self.AGE[s_, 1] and self._open(n, s_)]
                        if ss:
                            kind = STATES[st_]; break
            if ss:
                s_ = ss[int(self.rng.integers(len(ss)))]
                self.sk_carry[n] = dict(s=s_, t=int(t), kind=kind)
                if kind == "repair":
                    self.rp_last[n] = t
                else:
                    self.sk_last[n, STATES.index(kind)] = t

    def _sk_on(self, s):
        return {n: c_ for n, c_ in getattr(self, "sk_carry", {}).items() if int(s[n]) == c_["s"]}

    def seek_pull(self, s, K):
        """(N, K) log odds an unplayed life adds to the options of its seeking or repair moment: by its states, and for
        a tie by trust, warmth and control (talk and repair where there is trust, a boundary where there is control,
        separation where trust is gone and they can stand alone)."""
        u = np.zeros((self.N, K))
        for n, c_ in self._sk_on(s).items():
            if c_["kind"] == "repair":
                k_ = self._pk[n, 0]
                if k_ < 0:
                    continue
                tr = float(self.PP.trust[n, k_]); cl = float(self.PP.c[n, k_]); ct = float(_sig(self.PP.strict[n, k_]))
                ind = float(self._last_ctx["ind"][n]) if getattr(self, "_last_ctx", None) else 0.5
                wt = dict(talk=1.0 * tr, repair=1.0 * tr + 0.5 * cl, boundary=1.5 * ct, routine=0.8 * cl, renegotiate=0.8 * tr + 0.5 * ct,
                          shared=1.0 * cl, separate=2.0 * (0.5 - tr) + 1.0 * (ind - 0.5) - 1.0 * cl)
                tg = self.REPAIR_TAG[c_["s"]]; voc = ("talk", "repair", "boundary", "routine", "renegotiate", "shared", "separate")
            else:
                wt = {}
                for st_, i_ in ST.items():
                    for k2_, v_ in self.SEEK_W[st_].items():
                        wt[k2_] = wt.get(k2_, 0.0) + v_ * self.st_lv[n, i_]
                tg = self.SEEK_TAG[c_["s"]]; voc = ("deepen", "method", "help", "negotiate", "own_interest", "persist", "keep", "revise", "withdraw")
            for k2_ in range(min(len(tg), K)):
                if tg[k2_] >= 0:
                    u[n, k2_] = wt.get(voc[tg[k2_]], 0.0)
        return u

    def seek_answer(self, t, s, a, succ, idle, players):
        """A seeking or repair moment answered: the state or the tie moves by what was done and how it went (better,
        worse, or no different); a new interest is an attempt at entry (seek's own stages); never a colour step."""
        for n, c_ in self._sk_on(s).items():
            del self.sk_carry[n]
            k_ = int(a[n]); ok_ = bool(succ[n]) and not idle[n]
            rec = dict(t=int(t), age=round(t / 52.0, 2), kind=c_["kind"], moment=int(c_["s"]), by_player=n in players, worked=ok_)
            if c_["kind"] == "repair":
                tg = self.REPAIR_TAG[c_["s"]]; act = ("talk", "repair", "boundary", "routine", "renegotiate", "shared", "separate")[tg[k_]] \
                    if 0 <= k_ < len(tg) and tg[k_] >= 0 and not idle[n] else "nothing"
                pk = self._pk[n, 0]
                if pk >= 0:
                    sg = 1.0 if ok_ else -0.5
                    dtr, dc, dct = dict(talk=(0.05, 0.02, 0), repair=(0.06, 0.04, 0), boundary=(0.0, 0.0, -0.4), routine=(0.02, 0.04, 0),
                                        renegotiate=(0.04, 0.02, -0.3), shared=(0.03, 0.05, 0), separate=(-0.1, -0.2, 0),
                                        nothing=(-0.02, -0.01, 0)).get(act, (0, 0, 0))
                    if act != "separate":
                        dtr, dc = dtr * sg, dc * sg
                    self.PP.trust[n, pk] = np.clip(self.PP.trust[n, pk] + dtr, 0, 1)
                    self.PP.c[n, pk] = np.clip(self.PP.c[n, pk] + dc, 0, 1)
                    self.PP.strict[n, pk] += np.float32(dct * (1.0 if ok_ else 0.3))
                    rec.update(act=act, trust=round(float(dtr), 3), close=round(float(dc), 3),
                               effects=[dict(foot="tie", who="partner", trust=round(float(dtr), 3), close=round(float(dc), 3))])
            else:
                tg = self.SEEK_TAG[c_["s"]]; voc = ("deepen", "method", "help", "negotiate", "own_interest", "persist", "keep", "revise", "withdraw")
                act = voc[tg[k_]] if 0 <= k_ < len(tg) and tg[k_] >= 0 and not idle[n] else "nothing"
                eff = dict(deepen=dict(boredom=-0.3, frustration=-0.1), method=dict(boredom=-0.25, frustration=-0.1),
                           help=dict(low_mood=-0.2, frustration=-0.2), negotiate=dict(anger=-0.3, frustration=-0.1),
                           own_interest=dict(boredom=-0.2), persist=dict(frustration=-0.1), keep=dict(content=0.1),
                           revise=dict(frustration=-0.3), withdraw=dict(anger=-0.2, frustration=-0.2, boredom=0.1)).get(act, {})
                for st_, v_ in eff.items():
                    v_ = v_ if ok_ or v_ > 0 else -0.5 * v_   # a try that fails can make it worse
                    self.st_lv[n, ST[st_]] = float(np.clip(self.st_lv[n, ST[st_]] + v_, 0, 1))
                if act == "own_interest" and ok_:
                    self._try_entry(t, n, self.attr[n], "curious")
                rec.update(act=act, states={k2_: round(float(self.st_lv[n, ST[k2_]]), 3) for k2_ in eff})
            self.sk_stats.setdefault("answered", []).append(rec)
            lg = self.log[n]; lg.append(dict(t=int(t), age=rec["age"], demand=None, source=dict(key="partner" if c_["kind"] == "repair" else "self"),
                                             response=None, seek=rec))
            if len(lg) > self.p["log_keep"]:
                del lg[0]

    # ------------------------------------------------------------------ the caller's cast (P["scn"])
    def apply_cast(self, items, w_set=None):
        """S["scn_cast"]: (life, role, dict(colours, warmth, control, reach, trust, promise, keeps)); role a cast role, a
        group kind (its ways, cohesion, strictness) or "self" (the life's own mix, returned for the engine)."""
        PP = self.PP; import world_people_base as WB
        selfs = []
        for n, role, d_ in items:
            n = int(n)
            if role == "self":
                if d_.get("colours") is not None:
                    selfs.append((n, _norm(np.asarray(d_["colours"], float))))
                continue
            if role in G:
                js = np.nonzero(np.asarray(PP.skind[n]) == G[role])[0]
                if not len(js):
                    continue
                j = int(js[0])
                if d_.get("colours") is not None:
                    PP.snorm[n, j] = _norm(np.asarray(d_["colours"], float)).astype(np.float32)
                if d_.get("warmth") is not None:
                    PP.scoh[n, j] = np.float32(d_["warmth"])
                if d_.get("control") is not None:
                    PP.sstrict[n, j] = np.float32(d_["control"])
                if role == "household":   # the household's people too
                    mb = PP.used[n] & PP.lv[n] & (((np.asarray(PP.mset[n]).astype(np.int64) >> j) & 1) > 0)
                    self._set_people(n, np.nonzero(mb)[0], d_)
                continue
            bit = WB.BIT.get(role)
            if bit is None:
                continue
            ks = np.nonzero(PP.used[n] & PP.lv[n] & ((PP.rmask[n] & bit) != 0))[0]
            if not len(ks):
                continue
            self._set_people(n, ks[np.argsort(-PP.c[n, ks])][:1 if role in ("partner",) else len(ks)], d_)
        return selfs

    def _set_people(self, n, ks, d_):
        PP = self.PP
        for k in ks:
            if d_.get("colours") is not None:
                PP.pie[n, k] = _norm(np.asarray(d_["colours"], float)).astype(np.float32)
            if d_.get("warmth") is not None:
                PP.c[n, k] = np.float32(d_["warmth"])
            if d_.get("control") is not None:   # 0..1, read through the sigmoid the strictness is
                cc_ = float(np.clip(d_["control"], 0.01, 0.99)); PP.strict[n, k] = np.float32(np.log(cc_ / (1 - cc_)))
            if d_.get("trust") is not None:
                PP.trust[n, k] = np.float32(d_["trust"])
            if d_.get("reach") is not None and float(d_["reach"]) <= 0:
                self.out_of_reach = getattr(self, "out_of_reach", set()); self.out_of_reach.add((n, int(k)))
            if d_.get("promise") is not None:
                self.promises = getattr(self, "promises", {}); self.promises[(n, int(k))] = (d_["promise"], bool(d_.get("keeps", True)))

    # ------------------------------------------------------------------ the run's output (read by Release)
    def output(self):
        kinds = list(GROUP_KINDS) + list(PERSONS) + ["nature", "state"]
        return dict(responses=RESPONSES, kinds=kinds, count=self.count.copy(), drift_by=self.drift_by.copy(),
                    constrained=self.n_constrained, inner=self.n_inner, drifts=self.n_drift, log=self.log,
                    clash=dict(self.cl_stats, by_sphere=self.cl_stats["by_sphere"].copy(), weeks=[list(x_) for x_ in self.cl_wk])
                    if self.clash_on else None,
                    disputes=self.disputes if self.clash_on else None,
                    seek=dict(self.sk_stats, tried=self.tried) if self.seek_on else None)
