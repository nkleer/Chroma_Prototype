"""calib_v10/people_check.py: world_people.py's own checks (world-build.md, "Order of work" step 2).

N lives (default 600) run 80 years in one World with a synthetic engine (Driver below: random-walk colors pulled a
little toward the niche, a career at about 22, a partner at about 28, children at about 30, outlook about 0.5). Every
calibration target of the per-character side of the outer world is printed with its target and ok or MISS, then the
rule checks: drawn births, alive counts against the engine's draws, Close first, color equivariance (W and U swapped,
not a rotation), determinism, the world's history independent of the lives, reach and push sizes (per domain), save
and load with a legacy birth, no color-pair rule in the source, the event vocabulary, the time PP takes, emigration and
return (spec 5 §5), the game's data (the birth event, cast, place, figure and move views), and the character's children
following the engine's count.

    OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B calib_v10/people_check.py [N] [years]

Writes calib_v10/people_check.out. Uses world.py; a small stub World with world-build.md's names stands in only when
world.py does not import (the scorecard says which).
"""
import sys, os, time, json, io, re, tokenize
HERE = os.path.dirname(os.path.abspath(__file__)); PROTO = os.path.dirname(HERE)
sys.path.insert(0, PROTO)
import numpy as np
import world_people as wp
from world_people import People, likeness, R, BIT, KINMASK, G, VOLUNTARY, ROLE, ENGINE_ROLES, NEVER
from world_keys import NORM_KEYS, CAST_WANTS, GROUP_KINDS, LEVERS, DOMAINS, RINGS, WHO_SLOTS, INST_KINDS

try:
    from world import World
    WORLD_SRC = "world.py"
except Exception as e_:   # world.py mid-edit: the stub keeps the check runnable
    World = None
    WORLD_SRC = f"stub World (world.py did not import: {type(e_).__name__}: {e_})"

C = 5
SWAP = [1, 0, 2, 3, 4]                       # W and U swapped: not a rotation of the wheel
ATTR_P = ((0.77, 0.11, 0.08, 0.02, 0.02), (0.83, 0.07, 0.04, 0.02, 0.04))   # engine.py attr_p (female, male)
MORT = (0.0006, 3.5e-5, 0.09)                # engine.py self_mort
OUT, SCORE = [], []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(name, val, lo, hi, target, fmt="{:.3f}"):
    ok = bool(lo <= val <= hi)
    say(f"  {'ok  ' if ok else 'MISS'} {name}: {fmt.format(val)}   (target {target})")
    SCORE.append((name, ok))
    return ok


def check_b(name, ok, detail, target):
    ok = bool(ok)
    say(f"  {'ok  ' if ok else 'MISS'} {name}: {detail}   (target {target})")
    SCORE.append((name, ok))
    return ok


def sm(z):
    e = np.exp(z - z.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


# ---------------------------------------------------------------------------------------------- a stub World
class StubWorld:
    """Only when world.py does not import: world-build.md's names with plain values (15 localities, 40
    neighbourhoods, institutions per locality, three faiths, norm S-curves). Color-indexed draws are canonical, then
    relabelled by color_perm, like world.py."""

    def __init__(self, seed, cfg=None, color_perm=None):
        self._seed = int(seed); P = self.perm = np.arange(C) if color_perm is None else np.asarray(color_perm)
        r = np.random.default_rng([self._seed + 104729, 0]); nl = 15
        self.loc_pop_share = r.dirichlet(np.full(nl, 2.0)); self.loc_class_mix = r.dirichlet([3, 5, 2], nl)
        self.loc_mix = r.dirichlet(np.full(C, 4.0), nl)[:, P]; self.loc_sectors = r.dirichlet(np.full(5, 3.0), nl)
        self.loc_feat = r.random((nl, 16)) < 0.2; self.loc_kind = np.arange(nl); self.unemp_loc = 0.04 + 0.03 * r.random(nl)
        self.nb_loc = np.arange(40) % nl; self.nb_class = r.integers(0, 3, 40); self.nb_efficacy = r.uniform(0.3, 0.7, 40)
        ik, il = [], []
        for l_ in range(nl):
            for k_ in ("school", "employer", "employer", "employer", "hospital") + (("university",) if l_ < 5 else ()):
                ik.append(INST_KINDS.index(k_)); il.append(l_)
        for k_ in ("army", "party", "party", "party"):
            ik.append(INST_KINDS.index(k_)); il.append(0)
        self.inst_kind = np.array(ik); self.inst_loc = np.array(il); self.inst_sector = r.integers(0, 5, len(ik))
        self.inst_profile = r.dirichlet(np.full(C, 2.0), len(ik))[:, P]
        self.secular = 0.4; self.faith_share = np.array([0.5, 0.3, 0.2]) * 0.6
        self.faith_profile = r.dirichlet(np.full(C, 2.0), 3)[:, P]
        self.V = r.dirichlet(np.full(C, 6.0))[P]; self.era_p = self.V.copy(); self.era_i = 0.0
        self.comm, self.watch, self.rights, self.war, self.unemp, self.natural = 0.8, 0.3, np.ones(5), 0, 0.05, 0.05
        self._nb = {k_: (0.2 + 0.7 * ((hash(k_) % 97) / 97.0)) for k_ in NORM_KEYS}
        self.t = 0; self.pushes = []

    def burn_in(self, years=80):
        self.t = int(years * 52); return self

    def tick(self, week=None):
        self.t = self.t + 1 if week is None else int(week)

    def norm(self, key):
        return float(1 / (1 + np.exp(-(np.log(self._nb[key] / (1 - self._nb[key])) + 0.0004 * (self.t - 4160)))))

    def tech_has(self, key):
        return True

    def cohort_mix(self, birth_week):
        return self.V.copy()

    def rate_mult(self, kind):
        return {"disaster": np.ones(15), "crime": np.ones(15), "jobloss": np.ones(5)}.get(kind, 1.0)

    def push(self, domain, var, amount, sign):
        self.pushes.append((domain, var, amount, sign))


def make_world(seed=7, perm=None, years=80):
    W = World(seed, color_perm=perm) if World is not None else StubWorld(seed, color_perm=perm)
    W.burn_in(years)
    return W


# ---------------------------------------------------------------------------------------------- the synthetic engine
class Driver:
    """What the engine would pass each week (S) and do after it (acts, levers, wants). Colors: a random walk pulled a
    little toward PP.niche (x msg_w); career from about 22 to 65 with job losses; a partner at about 28 (breakups,
    widowhood follows the cast); a first child at about 30 for most; community for some; faith from a practising
    family. Color noise is drawn canonical and relabelled by perm, so a permuted run gets the same lives."""

    def __init__(self, PP, seed, perm=None, die=False, levers=True):
        N = self.N = PP.N; r = self.r = np.random.default_rng([seed, 5])
        self.P = np.arange(C) if perm is None else np.asarray(perm)
        self.z = r.normal(0, 0.8, (N, C))[:, self.P]
        self.held = np.zeros((N, 5), bool)
        self.car_at = np.clip(r.normal(22, 3, N), 16, 32); self.ret_at = np.clip(r.normal(65, 2.5, N), 58, 72)
        self.jobless = np.zeros(N, bool); self.p_since = np.zeros(N, np.int64)
        self.com = r.random(N) < 0.3; self.com_at = r.uniform(20, 40, N)
        self.outlook = np.clip(r.normal(0.5, 0.12, N), 0.05, 0.95)
        f_ = PP.female
        self.attr = np.where(f_, r.choice(5, N, p=ATTR_P[0]), r.choice(5, N, p=ATTR_P[1]))
        self.risky = np.where(r.random(N) < 0.15, r.uniform(0.2, 0.8, N), 0.0)
        tl = r.random(N)
        self.title = np.where(tl < 0.003, 3, np.where(tl < 0.015, 2, np.where(tl < 0.07, 1, 0)))
        self.title_at = r.uniform(30, 55, N)
        self.kids_want = r.random(N) < 0.82
        self.mon0 = 0.06 * r.standard_normal(N)
        self.dead = np.zeros(N, bool); self.die = die; self.levers = levers; self.started = False
        self.ss_p = np.asarray(wp.PP_DEFAULT["same_sex"], float)   # the engine's partner_same_p by attraction 0-4
        self.psame = np.zeros(N, bool)
        self.n_due = {k_: 0 for k_ in CAST_WANTS}; self.push_res = []

    def S(self, PP, wk):
        r = self.r; N = self.N; a = wk / 52.0; h = self.held
        if not self.started:
            h[:, 4] = (PP.pfaith >= 0) & (r.random(N) < 0.6); self.started = True
        U = r.random((8, N))
        noise = r.normal(0, 1, (N, C))[:, self.P]
        w = sm(self.z)
        self.z += 0.03 * noise + 0.004 * PP.msg_w[:, None] * (np.log(PP.niche + 1e-4) - np.log(w + 1e-4))
        self.z -= self.z.mean(1, keepdims=True)
        w = sm(self.z)
        lose = h[:, 0] & (U[0] < 0.03 / 52); rehire = self.jobless & (U[0] < 1.5 / 52)
        self.jobless = (self.jobless | lose) & ~rehire
        h[:, 0] = (a >= self.car_at) & (a < self.ret_at) & ~self.jobless
        lost = h[:, 1] & (PP.alive[:, 4] == 0) & (wk > self.p_since)
        hz = np.where(a >= 18, 0.22 * np.exp(-((a - 28) / 9) ** 2) + 0.03 * (a < 75), 0.0)
        start = ~h[:, 1] & (U[1] < hz / 52) & ~self.dead
        brk = h[:, 1] & (U[2] < 0.015 / 52) & (a < 75)
        h[:, 1] = (h[:, 1] & ~brk & ~lost) | start; self.p_since[start] = wk
        self.psame[start] = U[7][start] < self.ss_p[np.clip(self.attr[start], 0, 4)]   # the engine's own draw
        h[:, 2] |= h[:, 1] & self.kids_want & (a >= 21) & (a < 42) & (U[3] < 0.3 / 52)
        h[:, 3] = self.com & (a >= self.com_at)
        if a >= 16:
            h[:, 4] = (h[:, 4] & ~(U[4] < 0.01 / 52)) | (U[4] > 1 - 0.002 / 52)
        one = np.ones(N)
        money = np.clip(np.array([0.3, 0.5, 0.75])[PP.cls] + 0.1 * h[:, 0] - 0.1 * self.jobless + self.mon0, 0.02, 1)
        res = np.stack([money, 0.6 - 0.15 * h[:, 0] - 0.1 * h[:, 2], np.clip(1 - 0.012 * max(0.0, a - 35), 0.15, 1) * one,
                        PP.ties, 0.5 * one], 1)
        if self.die:
            self.dead |= U[6] < (MORT[0] + MORT[1] * np.exp(MORT[2] * a)) / 52
        return dict(w=w, held=h.copy(), res=res, stress=np.where(U[5] < 0.02, 0.8, 0.2), outlook=self.outlook,
                    attr=self.attr, risky=self.risky, dead=self.dead.copy(), partner_same=self.psame.copy(),
                    title_standing=np.where(a >= self.title_at, self.title, 0))

    def act(self, PP, t, timer=None):
        """timer: [seconds] gets the CPU time of PP's own calls here (on_act, want_due, resolve_want), not the Driver's."""
        r = self.r; N = self.N
        ma = sm(self.z + 0.8 * r.normal(0, 1, (N, C))[:, self.P])
        succ = (r.random(N) < 0.6).astype(float)
        lev = np.full(N, -1, np.int64); dom = np.full(N, -1, np.int64); nk = np.full(N, -1, np.int64)
        if self.levers:
            L = np.nonzero(r.random(N) < 0.004)[0]
            lev[L] = r.integers(0, len(LEVERS), len(L))
            dom[L] = np.array([DOMAINS.index(d_) for d_ in ("close", "group", "place", "institution", "state", "culture")])[
                r.integers(0, 6, len(L))]
            nk[L] = np.where(r.random(len(L)) < 0.3, r.integers(0, len(NORM_KEYS), len(L)), -1)
            succ[L] = r.random(len(L))
        c0 = time.process_time()
        out = PP.on_act(np.arange(N), ma, succ, 0.5, lever=lev, pushes=dom, norm=nk)
        due = PP.want_due(t)
        tp = time.process_time() - c0
        self.push_res += out["results"]
        for n_, cid, key in due:
            self.n_due[key] += 1
            ac_, sc_ = r.random() < 0.6, r.random() < 0.7
            c0 = time.process_time()
            PP.resolve_want(n_, cid, key, ac_, sc_)
            tp += time.process_time() - c0
        if timer is not None:
            timer[0] += tp
        return out


def pop_pies(PP, loc, born, rng):
    """Random people of the same place and generation (the statistics a cast member is drawn from)."""
    m = PP._popmean(np.asarray(loc), np.asarray(born))
    g = rng.standard_gamma(np.maximum(m, 0.002) * PP.P["conc"] * C)
    return g / g.sum(1, keepdims=True)


def run(PP, W, D, years, t0, hook=None, timer=None):
    """years of weekly ticks; hook(wk, t) runs after each week (not timed); timer: [seconds] of PP's own calls."""
    for wk in range(int(years * 52)):
        t = t0 + wk
        W.tick(t)
        S = D.S(PP, wk)
        c0 = time.process_time()
        PP.tick(t, S)
        if timer is not None:
            timer[0] += time.process_time() - c0
        D.act(PP, t, timer)
        if hook is not None:
            hook(wk + 1, t)


# ---------------------------------------------------------------------------------------------- 1. the main run
def main_run(N, Y):
    say(f"== 1. main run: {N} lives x {Y} years in {WORLD_SRC}, world seed 7, run seed 3 (auto_move on)")
    W = make_world(7); t0 = W.t
    fem = np.random.default_rng(11).random(N) < 0.5
    PP = People(W, N, 3, female=fem, cfg=dict(auto_move=True))
    c0 = time.process_time(); PP.birth(t0); tb = time.process_time() - c0
    D = Driver(PP, 3)
    L = PP.P["layer_c"]; rng = np.random.default_rng(99)
    rec = dict(lay={}, nofr={}, vol={}, moves={0: PP.n_moves.copy()}, yk={}, kinsh={}, out={}, stand={}, events=set(),
               ev_kinds={}, partners=[], pfollow=[], fr={}, close={}, trans=[], alive0=PP.alive.copy(), sib15=None,
               felt=None, psex=[], reveal=[0, 0], frd=np.zeros(N), frd_all=[0])
    prev_p = np.full(N, -1, np.int64)
    saved_lines = {}

    def hook(wk, t):
        nonlocal prev_p
        rec["frd"] += PP.died[:, 2] > 0   # the engine's "closest friend dies" moment
        rec["frd_all"][0] += sum(1 for e_ in PP.events if e_["kind"] == "died" and e_.get("role") == "friend")
        for e_ in PP.events:   # the vocabulary the game receives
            rec["ev_kinds"][e_["kind"]] = rec["ev_kinds"].get(e_["kind"], 0) + 1
            if e_["kind"] == "reveal":   # the reading before and after, the after nearer the truth
                k_ = PP._slot(e_["n"], e_["cid"]); tr_ = PP.pie[e_["n"], k_] if k_ >= 0 else None
                ok_ = (tr_ is not None and len(e_.get("old", [])) == C and len(e_.get("new", [])) == C
                       and np.abs(np.subtract(e_["new"], tr_)).sum() < np.abs(np.subtract(e_["old"], tr_)).sum())
                rec["reveal"][0] += 1; rec["reveal"][1] += bool(ok_)
            for k_, v_ in e_.items():
                if isinstance(v_, str):
                    rec["events"].add((k_, v_))
        # a new partner: likeness now against a random person of the same place and generation
        ps = PP.pslot; has = ps >= 0
        uidp = np.where(has, PP.uid[np.arange(N), np.maximum(ps, 0)], -1)
        new = has & (uidp != prev_p) & ~D.dead
        for n_ in np.nonzero(new)[0]:
            k_ = ps[n_]
            rp = pop_pies(PP, [PP.loc[n_]], [PP.born[n_, k_]], rng)[0]
            rec["partners"].append(dict(n=int(n_), uid=int(uidp[n_]), t=t, pie=PP.pie[n_, k_].astype(float).copy(),
                                        w=PP.w[n_].copy(), lk=float(likeness(PP.pie[n_, k_], PP.w[n_])),
                                        lkr=float(likeness(rp, PP.w[n_])), done=False))
        prev_p = uidp
        if wk % 52:
            return
        a = wk // 52
        hp = np.nonzero((PP.pslot >= 0) & ~D.dead)[0]
        if len(hp):   # the cast partner's sex follows the engine's partner_same (S), and how many are same-sex
            fp = PP.fem[hp, PP.pslot[hp]]
            rec["psex"].append(((fp == (PP.female[hp] == D.psame[hp])).sum(), (fp == PP.female[hp]).sum(),
                                D.ss_p[np.clip(D.attr[hp], 0, 4)].sum(), len(hp)))
        u = PP.used & PP.lv
        rec["lay"][a] = np.stack([(u & (PP.c >= L[i])).sum(1) for i in range(4)], 1)
        rec["nofr"][a] = PP.alive[:, 2] == 0
        rec["vol"][a] = np.isin(PP.skind, VOLUNTARY).any(1)
        rec["moves"][a] = PP.n_moves.copy()
        cl = u & (PP.c >= L[1])
        kin = (PP.rmask & KINMASK) != 0
        yk = cl & kin & (PP.born >= PP.t0 + 10 * 52)
        rec["yk"][a] = yk.sum(1) / np.maximum(cl.sum(1), 1)
        rec["kinsh"][a] = (cl & kin).sum(1) / np.maximum(cl.sum(1), 1)
        rec["out"][a] = dict(msg_w=PP.msg_w.copy(), community=PP.community.copy(), ties=PP.ties.copy(),
                             support=PP.support.copy(), belong=PP.belong.copy(), help=PP.help.copy(),
                             nsum=PP.niche.sum(1).copy(), approval=PP.approval.copy(), ln=PP.local_norm.copy(),
                             soc=np.array([W.norm(k_) for k_ in NORM_KEYS]), loc=PP.loc.copy())
        rec["stand"][a] = PP.standing.copy()
        if a in (30, 37, 45, 52):
            rec["close"][a] = {(int(n_), int(PP.uid[n_, k_])) for n_, k_ in zip(*np.nonzero(cl))}
            rec["close_kin"] = rec.get("close_kin", set()) | {(int(n_), int(PP.uid[n_, k_])) for n_, k_ in zip(*np.nonzero(cl & kin))}
        if a in (25, 35, 45, 55):   # friends near and alike
            fr = cl & ~kin & ((PP.rmask & (BIT["partner"] | BIT["ex"])) == 0)
            l4 = u & ~kin & (PP.c >= L[3]) & (PP.c < L[2])
            nn, kk = np.nonzero(fr); n4, k4 = np.nonzero(l4)
            rp = pop_pies(PP, PP.loc[nn], PP.born[nn, kk], rng)
            same = PP.mloc == PP.loc[:, None]
            rec["fr"][a] = dict(lk_f=likeness(PP.pie[nn, kk], PP.w[nn]).mean(), lk_4=likeness(PP.pie[n4, k4], PP.w[n4]).mean(),
                                lk_r=likeness(rp, PP.w[nn]).mean(), near_f=same[nn, kk].mean(), near_4=same[n4, k4].mean(),
                                near_r=float((PP.loc_p ** 2).sum()), set_f=(PP.mset[nn, kk] > 0).mean(),
                                aged_f=np.abs((PP.born[nn, kk] - PP.t0) / 52).mean(),
                                aged_4=np.abs((PP.born[n4, k4] - PP.t0) / 52).mean())
        if a == 15:   # siblings ever born by 15 (the engine draws them all at birth)
            rec["sib15"] = (PP.used & ((PP.rmask & BIT["sibling"]) != 0) & (PP.born <= t)).sum(1)
        if a in (40, 75):   # parent-child pairs among the cast (cousins and their parents, grandchildren and theirs)
            for n_ in range(N):
                us = np.nonzero(PP.used[n_])[0]
                by = {int(PP.uid[n_, k_]): k_ for k_ in us}
                for k_ in us:
                    pk = by.get(int(PP.kof[n_, k_]))
                    rm_ = int(PP.rmask[n_, k_])
                    if pk is None or not (rm_ & (BIT["kin"] | BIT["grandchild"])) or (rm_ & BIT["child"]):
                        continue
                    gap = (PP.born[n_, k_] - PP.born[n_, pk]) / 52
                    if 15 <= gap <= 45:
                        rec["trans"].append((int(PP.faith[n_, k_]), int(PP.faith[n_, pk]), int(PP.party[n_, k_]),
                                             int(PP.party[n_, pk]), PP.pie[n_, k_].astype(float), PP.pie[n_, pk].astype(float)))
        if a == 60:
            for n_ in range(10):
                saved_lines[n_] = PP.save(n_, w=PP.w[n_])
        for p_ in rec["partners"]:   # 15 years on with the same partner: did they move toward the character?
            if not p_["done"] and t - p_["t"] >= 15 * 52:
                p_["done"] = True
                n_ = p_["n"]; k_ = PP.pslot[n_]
                if k_ >= 0 and PP.uid[n_, k_] == p_["uid"] and PP.lv[n_, k_]:
                    rec["pfollow"].append((float(likeness(PP.pie[n_, k_], PP.w[n_])), float(likeness(p_["pie"], PP.w[n_])),
                                           float(likeness(p_["pie"], p_["w"]))))
        if a == 40:   # felt reach against outlook
            rec["felt"] = (PP.felt_reach.copy(), D.outlook.copy(), PP.reach.copy())

    timer = [0.0]
    c_all = time.process_time(); w_all = time.time()
    run(PP, W, D, Y, t0 + 1, hook, timer)
    say(f"  birth {tb:.2f} s; PP calls {timer[0]:.1f} s CPU; whole run {time.process_time() - c_all:.1f} s CPU, "
        f"{time.time() - w_all:.0f} s wall (the machine is shared)")
    return W, PP, D, rec, timer[0], saved_lines


def report_main(N, Y, W, PP, D, rec, tpp):
    L = PP.P["layer_c"]
    ages = [a for a in rec["lay"] if 25 <= a <= 60]
    lay = np.concatenate([rec["lay"][a] for a in ages]).mean(0)
    say("\n== 2. the cast (spec 2 §1-2; Dunbar's layers, cumulative, ages 25-60)")
    say(f"  layers by age: " + "; ".join(f"{a}: " + "/".join(f"{x:.0f}" for x in rec["lay"][a].mean(0)) for a in
                                         (5, 10, 15, 20, 30, 40, 50, 60, 70, 79) if a in rec["lay"]))
    check("support layer (closeness >= %.2f)" % L[0], lay[0], 3.5, 7.0, "about 5")
    check("sympathy layer (>= %.2f)" % L[1], lay[1], 11, 20, "about 15")
    check("friends layer (>= %.2f)" % L[2], lay[2], 35, 70, "about 50")
    check("active network (>= %.2f)" % L[3], lay[3], 100, 200, "about 150")
    for a0, a1 in ((30, 37), (45, 52)):
        if a0 in rec["close"] and a1 in rec["close"]:
            s0, s1 = rec["close"][a0], rec["close"][a1]
            rep = 1 - len(s0 & s1) / max(len(s0), 1)
            kin0 = s0 & rec["close_kin"]
            repk = 1 - len(kin0 & s1) / max(len(kin0), 1); repn = 1 - len((s0 - kin0) & s1) / max(len(s0 - kin0), 1)
            check(f"close ties (layers 1-2) at {a0} gone from them by {a1}", rep, 0.35, 0.65,
                  f"about half in 7 years (Mollenhorst, Volker and Flap 2014); kin {repk:.2f}, others {repn:.2f}")
    say("\n== 3. friends: near and alike (homophily, propinquity)")
    fr = rec["fr"]
    for a in sorted(fr):
        f_ = fr[a]
        say(f"  age {a}: likeness friends {f_['lk_f']:.3f}, layer-4 acquaintances {f_['lk_4']:.3f}, random same place and "
            f"generation {f_['lk_r']:.3f}; same locality friends {f_['near_f']:.2f}, layer 4 {f_['near_4']:.2f}, "
            f"random {f_['near_r']:.2f}; friends sharing a group now {f_['set_f']:.2f}; mean age gap {f_['aged_f']:.1f} y "
            f"(layer-4 acquaintances {f_['aged_4']:.1f} y)")
    m = {k_: np.mean([fr[a][k_] for a in fr]) for k_ in fr[min(fr)]}
    check("friends more alike than random people", m["lk_f"] - m["lk_r"], 0.03, 0.4, "> 0.03 likeness")
    check("friends more alike than layer-4 acquaintances", m["lk_f"] - m["lk_4"], 0.01, 0.4, "> 0.01 likeness")
    check("friends living in the same locality", m["near_f"], 0.55, 0.95, f"most (random {m['near_r']:.2f})")
    check("friends nearer in age than layer-4 acquaintances (mean gap, years)", m["aged_4"] - m["aged_f"], 3, 40,
          f"> 3 years nearer (age homophily; friends {m['aged_f']:.1f} y apart)", "{:.1f}")
    say("\n== 4. partners: start alike, barely converge (Caspi, Herbener and Ozer 1992; Watson et al. 2004)")
    ps = rec["partners"]
    lk = np.array([p_["lk"] for p_ in ps]); lkr = np.array([p_["lkr"] for p_ in ps])
    pie = np.array([p_["pie"] for p_ in ps]); ww = np.array([p_["w"] for p_ in ps])
    cr = np.mean([np.corrcoef(pie[:, c_], ww[:, c_])[0, 1] for c_ in range(C)]) if len(ps) > 5 else 0.0
    say(f"  {len(ps)} partnerships; likeness at the start {lk.mean():.3f} vs a random person of the same place and "
        f"generation {lkr.mean():.3f}; color correlation between spouses {cr:.2f}")
    check("spouses alike at the start (likeness above random)", lk.mean() - lkr.mean(), 0.04, 0.4, "> 0.04")
    check("spouses' color correlation at the start", cr, 0.2, 0.7, "0.2-0.7 (values and politics about 0.4-0.5)")
    px = np.array(rec["psex"], float).sum(0)
    say(f"  partner's sex: the cast partner agrees with the engine's partner_same in {px[0] / px[3]:.3f} of partnered "
        f"life-years; same-sex {px[1] / px[3]:.3f} (the engine's same_sex table by attraction gives {px[2] / px[3]:.3f})")
    check_b("the cast partner's sex follows the engine's S['partner_same']", px[0] == px[3], f"{int(px[0])}/{int(px[3])}",
            "all partnered life-years")
    pf = np.array(rec["pfollow"])
    if len(pf):
        conv = (pf[:, 0] - pf[:, 1]).mean()
        say(f"  {len(pf)} still together after 15 years: the partner's own move toward the character {conv:+.3f} likeness"
            f" (their likeness at the start {pf[:, 2].mean():.3f}, now {pf[:, 0].mean():.3f})")
        check("spouses' convergence over 15 years (the partner's own move)", conv, -0.01, 0.05, "small: 0 to 0.05")
    else:
        check_b("spouses' convergence over 15 years", False, "no couple lasted 15 years", "measured")
    say("\n== 5. what passes from parents: faith and party most strongly (Jennings, Stoker and Bowers 2009)")
    tr = rec["trans"]
    if len(tr) > 50:
        fc = np.array([x[0] for x in tr]); fp = np.array([x[1] for x in tr])
        pc = np.array([x[2] for x in tr]); pp = np.array([x[3] for x in tr])
        def kappa(a_, b_):
            po = (a_ == b_).mean(); vals = np.union1d(a_, b_)
            pe = sum((a_ == v_).mean() * (b_ == v_).mean() for v_ in vals)
            return (po - pe) / max(1 - pe, 1e-9)
        pc_ = np.array([x[4] for x in tr]); pp_ = np.array([x[5] for x in tr])
        pcorr = np.mean([np.corrcoef(pc_[:, c_], pp_[:, c_])[0, 1] for c_ in range(C)])
        kf, kp = kappa(fc, fp), kappa(pc, pp)
        say(f"  {len(tr)} parent-child pairs in the casts: faith agreement kappa {kf:.2f}, party kappa {kp:.2f}, "
            f"color correlation {pcorr:.2f}")
        check("faith passes from parents (kappa)", kf, 0.5, 0.95, "strong: 0.5-0.95")
        check("party passes from parents (kappa)", kp, 0.4, 0.95, "strong: 0.4-0.95")
        check("faith and party pass more strongly than colors", min(kf, kp) - pcorr, 0.1, 1.0, "kappa above color corr")
    else:
        check_b("parent-child pairs", False, f"only {len(tr)} pairs", "> 50")
    say("\n== 6. no close friend, groups, old age")
    nf = np.concatenate([rec["nofr"][a] for a in rec["nofr"] if 25 <= a <= 65]).mean()
    check("adults 25-65 with no close friend", nf, 0.05, 0.18, "about 1 in 10")
    say("  by age: " + ", ".join(f"{a}: {rec['nofr'][a].mean():.2f}" for a in (10, 20, 30, 45, 60, 70, 79) if a in rec["nofr"]))
    vol = np.concatenate([rec["vol"][a] for a in rec["vol"] if 25 <= a <= 65]).mean()
    check("adults 25-65 in at least one voluntary group (congregation, club, scene, movement)", vol, 0.35, 0.65, "about half")
    if 50 in rec["yk"] and 79 in rec["yk"]:
        y50, y80 = rec["yk"][50].mean(), rec["yk"][79].mean()
        say(f"  younger kin's share of layers 1-2: 50: {y50:.2f}, 65: {rec['yk'].get(65, np.zeros(1)).mean():.2f}, 79: {y80:.2f}; "
            f"all kin: 50: {rec['kinsh'][50].mean():.2f}, 79: {rec['kinsh'][79].mean():.2f}")
        check("old age shifts the close circle toward younger kin (share at 79 minus at 50)", y80 - y50, 0.08, 0.8, "> 0.08")
    say("\n== 7. place and moving (US Census CPS: about 8.5% a year, highest in the twenties)")
    mv = rec["moves"]; yrs = sorted(mv)
    per = {a: (mv[a] - mv[a - 1]).mean() for a in yrs if a - 1 in mv}
    band = lambda lo, hi: np.mean([per[a] for a in per if lo <= a - 1 < hi])
    bands = dict(child=band(0, 18), b18=band(18, 20), b20=band(20, 30), b30=band(30, 45), b45=band(45, 65), b65=band(65, 90))
    tot = np.mean(list(per.values()))
    say("  yearly rate by age: 0-17 %.3f, 18-19 %.3f, 20-29 %.3f, 30-44 %.3f, 45-64 %.3f, 65+ %.3f" % tuple(bands.values()))
    check("moving a year, all ages", tot, 0.07, 0.10, "about 0.085")
    check_b("moving peaks in the twenties", bands["b20"] >= max(v_ for k_, v_ in bands.items() if k_ != "b20"),
            f"20-29 {bands['b20']:.3f}", "highest band")
    say("\n== 8. what the engine reads (ranges, adults 25-65)")
    ad = [a for a in rec["out"] if 25 <= a <= 65]
    g = lambda k_: np.concatenate([rec["out"][a][k_] for a in ad])
    msg = g("msg_w"); com = g("community"); ties = g("ties"); sup = g("support"); bel = g("belong"); hlp = g("help")
    nsum = np.concatenate([rec["out"][a]["nsum"] for a in rec["out"]])
    say(f"  msg_w median {np.median(msg):.2f} (10-90%: {np.percentile(msg, 10):.2f}-{np.percentile(msg, 90):.2f}); by age " +
        ", ".join(f"{a}: {np.median(rec['out'][a]['msg_w']):.2f}" for a in (5, 15, 20, 30, 50, 70, 79) if a in rec["out"]))
    check("msg_w median, adults", np.median(msg), 0.8, 1.25, "about 1 (1 = today's niche push)")
    check("niche rows are pies", np.abs(nsum - 1).max(), 0, 1e-6, "sum to 1", "{:.1e}")
    say(f"  community median {np.median(com):+.3f} (10-90%: {np.percentile(com, 10):+.2f} to {np.percentile(com, 90):+.2f}),"
        f" range {com.min():+.2f}..{com.max():+.2f}")
    check("community driver centred", np.median(com), -0.12, 0.12, "about 0, in -0.5..0.5")
    check("community driver spread (10-90%)", np.percentile(com, 90) - np.percentile(com, 10), 0.15, 0.9, "varies across lives")
    say(f"  ties median {np.median(ties):.2f} (10-90%: {np.percentile(ties, 10):.2f}-{np.percentile(ties, 90):.2f}); belong "
        f"{np.median(bel):.2f}; help {np.median(hlp):.2f}; support {np.median(sup):+.3f} "
        f"({np.percentile(sup, 10):+.2f} to {np.percentile(sup, 90):+.2f})")
    check("ties driver median", np.median(ties), 0.35, 0.75, "about 0.55, in 0..1")
    check("support centred", np.median(sup), -0.06, 0.06, "about 0 (adds to the engine's support)")
    ap = np.concatenate([rec["out"][a]["approval"] for a in ad]); ln = np.concatenate([rec["out"][a]["ln"] for a in ad])
    soc = np.concatenate([np.tile(rec["out"][a]["soc"], (N, 1)) for a in ad]); lo_ = np.concatenate([rec["out"][a]["loc"] for a in ad])
    felt = soc + ap
    say("  acceptance felt (society's + PP.approval), mean and sd across lives, adults: " +
        ", ".join(f"{k_} {soc[:, i_].mean():.2f}{ap[:, i_].mean():+.2f} sd {ap[:, i_].std():.2f}" for i_, k_ in enumerate(NORM_KEYS)))
    say("  local norm (the groups) minus society's, mean: " + ", ".join(f"{k_} {(ln - soc)[:, i_].mean():+.2f}" for i_, k_ in enumerate(NORM_KEYS[:8])) + " ...")
    for key_ in ("transition", "coming out"):
        if key_ in NORM_KEYS:
            i_ = NORM_KEYS.index(key_)
            bl = [felt[lo_ == l_, i_].mean() for l_ in np.unique(lo_) if (lo_ == l_).sum() > 50]
            say(f"  {key_}: felt acceptance by locality {min(bl):.2f}..{max(bl):.2f} (society's {soc[:, i_].mean():.2f})")
    check_b("approval has one column per NORM_KEYS key; felt acceptance in 0..1", ap.shape[1] == len(NORM_KEYS)
            and felt.min() >= -1e-9 and felt.max() <= 1 + 1e-9, f"{ap.shape[1]} keys, {felt.min():.2f}..{felt.max():.2f}",
            f"{len(NORM_KEYS)} keys")
    check("felt acceptance stays near the society's (mean |PP.approval|)", np.abs(ap).mean(), 0, 0.2, "< 0.2")
    check("felt acceptance varies with groups and circle (sd across lives, mean over keys)", ap.std(0).mean(), 0.03, 0.25, "0.03-0.25")
    st = np.concatenate([rec["stand"][a] for a in ad])
    say("  standing by ring (share at 0/1/2/3): " + "; ".join(
        f"{RINGS[r_]}: " + "/".join(f"{(st[:, r_] == v_).mean():.2f}" for v_ in range(4)) for r_ in range(4)))
    fr_, ol, rc = rec["felt"]
    ordin = (rc == np.array([3, 1, 0, 0])).all(1)
    cf = np.corrcoef(fr_[ordin, 1], ol[ordin])[0, 1] if ordin.sum() > 10 else 0
    say(f"  at 40: {ordin.mean():.2f} of lives have ordinary reach 3/1/0/0; felt reach in settings and place for them "
        f"{fr_[ordin, 1].mean():.2f} (sd {fr_[ordin, 1].std():.2f}), state ring {fr_[ordin, 3].mean():.2f}")
    check("felt reach follows outlook (corr, ordinary reach)", cf, 0.5, 1.0, "> 0.5")
    check_b("felt reach in 0..3", fr_.min() >= 0 and fr_.max() <= 3, f"{fr_.min():.2f}..{fr_.max():.2f}", "0..3")
    if rec["sib15"] is not None:
        check("siblings born by 15 (mean)", rec["sib15"].mean(), 1.1, 1.5, "about the engine's 1.35 (0-3 at 0.2/0.4/0.25/0.15)")
    say("\n== 9. wants and pushes in the run")
    yrs_ad = N * max(Y - 14, 1)
    say("  wants due a life-year from 14: " + ", ".join(f"{k_} {v_ / yrs_ad:.3f}" for k_, v_ in D.n_due.items()))
    tot_w = sum(D.n_due.values()) / yrs_ad
    check("cast wants falling due a year (adult)", tot_w, 0.3, 4.0, "a few a year")
    check("a relative's wish to make peace after a break, falling due per life", D.n_due["forgiveness"] / N, 0.4, 1.2,
          "0.5-1 (about a quarter estranged from a relative; most reconcile once at most, Pillemer 2020)", "{:.2f}")
    say(f"  friends who died, as cast events: {rec['frd_all'][0] / N:.2f} a life; of them the closest friend (the engine's "
        f"moment): {rec['frd'].mean():.2f}")
    check("the closest friend's death (the engine's friend column), per life", rec["frd"].mean(), 0.05, 1.0,
          "at most about once a life (world off: under 0.5)", "{:.2f}")
    pr = D.push_res
    sz = {}
    for r_ in pr:
        sz.setdefault(r_["domain"], {}).setdefault(r_["size"], 0); sz[r_["domain"]][r_["size"]] += 1
    say(f"  {len(pr)} pushes; sizes by domain: " + "; ".join(f"{d_}: {v_}" for d_, v_ in sorted(sz.items())))
    say(f"  backfires {np.mean([r_['backfire'] for r_ in pr]):.3f}")
    st_none = sz.get("state", {}); share_none = (st_none.get("none", 0) + st_none.get("unseen", 0)) / max(sum(st_none.values()), 1)
    check("a push on the state shows nothing when made (unseen, or none on a backfire; W35-14)", share_none, 0.99, 1.0, "always")
    say("\n== 10. event vocabulary sent to the game")
    say("  event kinds: " + ", ".join(f"{k_} {v_}" for k_, v_ in sorted(rec["ev_kinds"].items())))
    rv = rec["reveal"]
    check_b("a reveal event carries the reading before and after (after nearer the truth)", rv[0] > 0 and rv[1] == rv[0],
            f"{rv[1]}/{rv[0]}", "all")
    check_b("push results are returned to the engine, not also sent as cast events", rec["ev_kinds"].get("push", 0) == 0
            and len(pr) > 0, f"{rec['ev_kinds'].get('push', 0)} push events, {len(pr)} results", "0 events")
    return tot_w


def vocab_check(evs):
    eng = open(os.path.join(PROTO, "engine.py")).read()
    mk = re.search(r"MARK_BASE = \[(.*?)\]", eng, re.S)
    marks = set(re.findall(r'"([^"]+)"', mk.group(1))) if mk else set()
    allowed = dict(
        kind={"born", "joined", "left", "died", "break", "ex", "partner", "friend", "role", "want", "group_joined",
              "group_left", "split", "parents_apart", "ill", "lost_job", "divorce", "moved_away", "reveal", "push",
              "face", "moved"},
        role=set(ROLE) | set(WHO_SLOTS) | {"sibling", "child", "grandchild"},
        group=set(GROUP_KINDS), key=set(CAST_WANTS), lever=set(LEVERS), domain=set(DOMAINS),
        size={"none", "small", "clear", "strong", "unseen"}, state={"begins", "due", "met", "lapsed", "refused"},
        via={"group"}, mark=marks,
        why={"fight", "left", "moved", "drifted away", "job ended", "left the faith", "finished", "school changed",
             "left home", "exit", "full", "came home", "emigrated", "returned"})
    bad = []
    for k_, v_ in sorted(evs):
        if k_ == "target":
            ok = v_ in DOMAINS or v_ in GROUP_KINDS or v_.split(" ")[0] in DOMAINS
        else:
            ok = v_ in allowed.get(k_, set())
        if not ok:
            bad.append(f"{k_}={v_}")
    yr = [v_ for _, v_ in evs if re.search(r"\d", v_)]
    check_b("event strings are keys from the shared vocabularies (marks: engine MARK_BASE)", not bad and not yr,
            "all known" if not bad and not yr else "unknown: " + ", ".join(bad + yr), "no free text, no numbers")


# ---------------------------------------------------------------------------------------------- 2. other checks
def births_check(n=1000):
    say(f"\n== 11. drawn births over {n} lives")
    W = make_world(7)
    PP = People(W, n, 21, female=np.random.default_rng(1).random(n) < 0.5)
    PP.birth(W.t)
    ps = np.asarray(W.loc_pop_share, float); ps = ps / ps.sum()
    got = np.bincount(PP.loc, minlength=len(ps)) / n
    cm = np.asarray(W.loc_class_mix, float); cm = cm / cm.sum(1, keepdims=True)
    cls_p = ps @ cm; cls_g = np.bincount(PP.cls, minlength=3) / n
    chi = n * ((got - ps) ** 2 / np.maximum(ps, 1e-9)).sum(); chc = n * ((cls_g - cls_p) ** 2 / np.maximum(cls_p, 1e-9)).sum()
    say(f"  localities: max gap {np.abs(got - ps).max():.3f}, chi-square {chi:.1f} on {len(ps) - 1} df; classes drawn "
        f"{np.round(cls_g, 3)} vs population {np.round(cls_p, 3)}")
    check("locality shares match the population (chi-square, 14 df: 5% critical value 23.7)", chi, 0, 23.7, "< 23.7", "{:.1f}")
    chs = [chc]   # classes: this run and four more of 1000 births (one run alone misses 1 time in 20 by chance)
    for s_ in range(22, 26):
        Pc = People(W, n, s_, female=np.random.default_rng(s_).random(n) < 0.5); Pc.birth(W.t)
        g_ = np.bincount(Pc.cls, minlength=3) / n; chs.append(n * ((g_ - cls_p) ** 2 / np.maximum(cls_p, 1e-9)).sum())
    say(f"  classes: chi-square by run {', '.join(f'{x_:.1f}' for x_ in chs)} (2 df each)")
    check("class shares match the population (chi-square summed over 5 runs of 1000, 10 df: 5% critical value 18.3)",
          sum(chs), 0, 18.31, "< 18.3", "{:.1f}")
    nbl = np.asarray(W.nb_loc)
    check_b("every neighbourhood is in the life's locality", (nbl[PP.nb] == PP.loc).all(), "yes" if (nbl[PP.nb] == PP.loc).all() else "no", "all")
    a0 = PP.alive
    say(f"  alive at birth (parents, siblings born, friend, grandparents, partner): means {np.round(a0.mean(0), 2)}; engine "
        f"draws 2, 0-3 (mean 1.35, all born at once), 1, 2-4 (mean 3), 0")
    check("parents alive at birth", a0[:, 0].mean(), 1.97, 2.0, "2 (the engine's)")
    check("grandparents alive at birth (mean)", a0[:, 3].mean(), 2.5, 3.6, "about 3 (engine: 2-4 uniform)")
    fs = np.asarray(W.faith_share, float); sec = float(getattr(W, "secular", 1 - fs.sum()))
    fam = np.bincount(PP.pfaith + 1, minlength=len(fs) + 1) / n
    say(f"  family faith drawn (none, faiths...) {np.round(fam, 3)} vs society secular {sec:.2f}, faiths {np.round(fs, 3)}")
    return PP


def close_first_check():
    say("\n== 12. Close first: the times' share of the niche by age (the rest is the settings and the close circle)")
    b0, pk, at, wd = wp.PP_DEFAULT["times_w"]
    tw = {a: b0 + pk * np.exp(-((a - at) / wd) ** 2) for a in (3, 8, 12, 15, 20, 25, 30, 40, 60, 80)}
    say("  " + ", ".join(f"{a}: {v_:.2f}" for a, v_ in tw.items()))
    peak = max(tw, key=tw.get)
    check_b("the times weigh most at 15 to 25", 15 <= peak <= 25, f"peak at {peak}", "15-25")
    check("the times' share is below the close circle and settings' at every age", max(tw.values()), 0, 0.45, "< 0.5")
    check("the times' share in childhood and late life (max of 3, 8, 60, 80)", max(tw[3], tw[8], tw[60], tw[80]), 0, 0.08, "small")
    # in the code: replace the times and see the niche move by that share
    W = make_world(7); PP = People(W, 50, 4); PP.birth(W.t)
    D = Driver(PP, 4, levers=False)
    run(PP, W, D, 20, W.t + 1)
    n0 = PP.niche.copy(); V0 = np.asarray(W.V, float).copy()
    alt = np.roll(V0, 1)
    try:
        W.V = alt; ei = getattr(W, "era_i", 0.0); W.era_i = 0.0
        PP._outputs(PP.t)
        dn = np.abs(PP.niche - n0).sum(1).mean() / np.abs(wp._norm(alt) - wp._norm(V0 + 0.5 * ei * (wp._norm(np.asarray(W.era_p, float)) - V0))).sum()
    finally:
        W.V = V0; W.era_i = ei
        PP._outputs(PP.t)
    say(f"  at 20 in the code: a change of the times moves the niche by {dn:.2f} of it (formula {tw[20]:.2f})")
    check("the niche follows the times by the age weight (age 20)", abs(dn - tw[20]), 0, 0.03, "equal to the weight")


def fade_check(N=120):
    say(f"\n== 13. without contact: friends fade within 1-2 years, kin far slower (Roberts and Dunbar 2011); {N} lives cut at 40")
    W = make_world(7); PP = People(W, N, 5); PP.birth(W.t)
    D = Driver(PP, 5, levers=False)
    run(PP, W, D, 40, W.t + 1)
    L2 = PP.P["layer_c"][1]; rng = np.random.default_rng(3)
    CUT = np.zeros((N, PP.K), bool); picks = []
    hh = ((PP.mset >> np.maximum(PP.hhj, 0).astype(PP.mset.dtype)[:, None]) & 1).astype(bool) & (PP.hhj >= 0)[:, None]
    for n_ in range(N):
        u = PP.used[n_] & PP.lv[n_] & (PP.c[n_] >= L2) & ~hh[n_]
        kin = (PP.rmask[n_] & KINMASK) != 0
        fr = np.nonzero(u & ~kin & ((PP.rmask[n_] & BIT["friend"]) != 0))[0]
        kn = np.nonzero(u & kin & ((PP.rmask[n_] & (BIT["parent"] | BIT["sibling"])) != 0))[0]
        for kind_, cand in (("friend", fr), ("kin", kn)):
            if len(cand):
                k_ = int(rng.choice(cand)); CUT[n_, k_] = True; picks.append((n_, k_, kind_, float(PP.c[n_, k_]), int(PP.uid[n_, k_])))
    orig_tt, orig_ci = PP._tie_target, PP._close_index

    def tt(n2=None, k2=None):
        f, e, lk, cap = orig_tt(n2, k2)
        m = CUT if n2 is None else CUT[n2, k2]
        return np.where(m, 0, f), np.where(m, 0, e), lk, cap

    def ci():
        orig_ci()
        m = CUT[PP._n2, PP.ci]
        PP._cdf[m] = 0; PP._cf0[m] = 0
    PP._tie_target = tt; PP._close_index = ci; PP._close_index()
    res = {1: [], 2: []}
    t0 = PP.t
    for yr in (1, 2):
        run(PP, W, D, 1, PP.t + 1)
        for n_, k_, kind_, c0, uid in picks:
            if PP.uid[n_, k_] == uid and PP.lv[n_, k_]:
                res[yr].append((kind_, PP.c[n_, k_] / c0, PP.c[n_, k_] >= L2))
    for yr in (1, 2):
        f_ = [x[1] for x in res[yr] if x[0] == "friend"]; k_ = [x[1] for x in res[yr] if x[0] == "kin"]
        fo = np.mean([not x[2] for x in res[yr] if x[0] == "friend"]); ko = np.mean([not x[2] for x in res[yr] if x[0] == "kin"])
        say(f"  after {yr} year(s): closeness kept, friends {np.median(f_):.2f} ({len(f_)}), kin {np.median(k_):.2f} "
            f"({len(k_)}); out of layers 1-2: friends {fo:.2f}, kin {ko:.2f}")
        if yr == 1:
            check("friends' closeness kept after a year without contact", np.median(f_), 0, 0.5, "< 0.5")
        else:
            check("friends' closeness kept after two years without contact", np.median(f_), 0, 0.25, "< 0.25")
            check("kin's closeness kept after two years without contact", np.median(k_), 0.45, 1.0, "> 0.45 (far slower)")


def equivariance_check(N=100, Y=10):
    say(f"\n== 14. equivariance: W and U swapped (not a rotation), {N} lives x {Y} years, same seeds")
    if World is not None:
        W1, W2 = make_world(7), make_world(7, SWAP)
    else:
        W1, W2 = make_world(7), make_world(7, SWAP)
    dw = max(np.abs(np.asarray(W2.loc_mix) - np.asarray(W1.loc_mix)[:, SWAP]).max(), np.abs(np.asarray(W2.V) - np.asarray(W1.V)[SWAP]).max())
    say(f"  the world's own relabelling (loc_mix, V): max gap {dw:.1e}")
    fem = np.random.default_rng(2).random(N) < 0.5
    P1 = People(W1, N, 8, female=fem); P2 = People(W2, N, 8, female=fem)
    P1.birth(W1.t); P2.birth(W2.t)
    same0 = (P1.used == P2.used).all() and (P1.loc == P2.loc).all() and (P1.cls == P2.cls).all()
    gb = np.abs(P2.pie - P1.pie[..., SWAP]).max()
    check_b("births: same places, classes and casts; pies relabelled", same0 and gb < 1e-5, f"same {same0}, pie gap {gb:.1e}", "exact")
    D1, D2 = Driver(P1, 8), Driver(P2, 8, perm=SWAP)
    gaps = []
    for yr in range(Y):
        run(P1, W1, D1, 1, P1.t + 1); run(P2, W2, D2, 1, P2.t + 1)
        g = max(np.abs(P2.niche - P1.niche[:, SWAP]).max(), np.abs(P2.msg_w - P1.msg_w).max(),
                np.abs(P2.approval - P1.approval).max(), np.abs(P2.standing - P1.standing).max(),
                np.abs(P2.community - P1.community).max(), np.abs(P2.felt_reach - P1.felt_reach).max())
        gaps.append((g, bool((P1.used == P2.used).all())))
    say("  yearly max gap (niche relabelled; msg_w, approval, standing, community, felt reach equal): " +
        ", ".join(f"{g:.1e}" for g, _ in gaps))
    check_b("every color-indexed output is the same relabelling", max(g for g, _ in gaps) < 1e-4 and all(s for _, s in gaps),
            f"max gap {max(g for g, _ in gaps):.1e}, casts identical {all(s for _, s in gaps)}", "< 1e-4")
    f1, f2 = P1.figure_view(0), P2.figure_view(0)
    fg = max([np.abs(np.asarray(b_["read"]) - np.asarray(a_["read"])[SWAP]).max() for a_, b_ in zip(f1, f2)] or [9.0])
    check_b("public figures read through the character: the same relabelling", len(f1) == len(f2) > 0 and fg < 2e-3,
            f"{len(f1)} figures, gap {fg:.1e} (rounded to 0.001)", "< 2e-3")


def determinism_check(N=60, Y=10):
    say(f"\n== 15. determinism and the world's independence ({N} lives x {Y} years)")
    snaps = []
    for rep in range(2):
        W = make_world(7); PP = People(W, N, 12); PP.birth(W.t)
        D = Driver(PP, 12, die=True)
        run(PP, W, D, Y, W.t + 1)
        snaps.append((PP.c.copy(), PP.pie.copy(), PP.niche.copy(), PP.skind.copy(), len(D.push_res), PP.n_moves.copy(), W, PP, D))
    a, b = snaps
    same = all(np.array_equal(x, y) for x, y in zip(a[:4], b[:4])) and a[4] == b[4] and np.array_equal(a[5], b[5])
    check_b("the same seeds give the same lives", same, "identical" if same else "differ", "identical")
    # the world's history with lives that never push equals the world alone
    W_alone = make_world(7)
    W_lives = make_world(7); PP = People(W_lives, N, 13); PP.birth(W_lives.t)
    D = Driver(PP, 13, levers=False)
    run(PP, W_lives, D, Y, W_lives.t + 1)
    for wk in range(Y * 52):
        W_alone.tick(W_alone.t + 1)
    keys = [k_ for k_ in ("V", "era_p", "unemp", "prosper", "unrest", "loc_crime", "nb_efficacy") if hasattr(W_alone, k_)]
    eq = all(np.array_equal(np.asarray(getattr(W_alone, k_)), np.asarray(getattr(W_lives, k_))) for k_ in keys)
    eq &= len(getattr(W_alone, "log", [])) == len(getattr(W_lives, "log", []))
    check_b("the world's history does not depend on the lives (no pushes: identical)", eq,
            f"{', '.join(keys)} and the log {'identical' if eq else 'differ'}", "identical")
    npush = len(getattr(W_lives, "push_log", [])) + len(getattr(W_lives, "pushes", []))
    W_p, D_p = a[6], a[8]
    say(f"  with levers on, the lives reached the world only through W.push: {len(D_p.push_res)} pushes "
        f"({sum(r_['domain'] in ('institution', 'state', 'culture') for r_ in D_p.push_res)} queued in the world)")
    return a[7], a[6]


def reach_check():
    say("\n== 16. standing, reach and push sizes (spec 7 §2-3)")
    W = make_world(7); PP = People(W, 4, 14); PP.birth(W.t)
    D = Driver(PP, 14, levers=False)
    run(PP, W, D, 30, W.t + 1)
    ts = np.array([0, 1, 2, 3])
    S = D.S(PP, 30 * 52 + 1); S["title_standing"] = ts; S["res"][:, 0] = 0.5
    PP.tick(PP.t + 1, S); PP.month(PP.t, S)
    say("  title standing 0..3 -> standing " + "; ".join("/".join(str(int(x)) for x in PP.standing[i]) for i in range(4))
        + " -> reach " + "; ".join("/".join(str(int(x)) for x in PP.reach[i]) for i in range(4)))
    rv = [PP.reach_view(i) for i in range(4)]
    vals = [x_ for v_ in rv for x_ in v_["felt"] + v_["hint"]]
    say("  the game's reach view (felt; hint): " + "; ".join(f"{v_['felt']}; {v_['hint']}" for v_ in rv))
    check_b("the game's reach view: felt on 0..1; hint only rough, three steps (0, .5, 1)",
            all(0 <= x_ <= 1 for x_ in vals) and all(x_ in (0.0, 0.5, 1.0) for v_ in rv for x_ in v_["hint"] + v_["domain_hint"])
            and all(len(v_["felt"]) == len(v_["hint"]) == len(RINGS) for v_ in rv)
            and all(len(v_["domain_hint"]) == len(DOMAINS) for v_ in rv),
            f"{min(vals):.2f}..{max(vals):.2f}; hints {sorted(set(x_ for v_ in rv for x_ in v_['hint']))}", "0..1; hint 0, .5 or 1")
    check_b("an ordinary life's reach is 3/1/0/0 (close, settings and place, institutions, state)",
            PP.standing[0, 1:].max() > 0 or (PP.reach[0] == [3, 1, 0, 0]).all(),
            "/".join(str(int(x)) for x in PP.reach[0]), "3/1/0/0 unless ties or groups lend standing")
    q0 = len(getattr(W, "_queue", getattr(W, "pushes", [])))
    ma = np.tile(np.eye(C)[0] * 0.6 + 0.08, (4, 1))
    out = PP.on_act(np.arange(4), ma, 1.0, 0.8, lever=np.full(4, LEVERS.index("voice")), pushes=np.full(4, DOMAINS.index("state")))
    sizes = [r_["size"] for r_ in out["results"]]
    q = getattr(W, "_queue", getattr(W, "pushes", []))
    amts = [x[2] for x in list(q)[q0:]]
    say(f"  a vote or voice on the state that went well, by title standing 0..3: {sizes}; W.push amounts {np.round(amts, 6)}")
    check_b("an ordinary voice on the state shows nothing and pushes one of millions", sizes[0] in ("none", "unseen") and amts[0] <= 1e-5,
            f"{sizes[0]}, {amts[0]:.0e}", "unseen, 1e-6")
    check_b("a national figure's voice reaches the world clearly (W.push of a clear size, 0.75+; shown unseen when made)",
            sizes[3] == "unseen" and amts[3] >= 0.75, f"{sizes[3]}, {amts[3]:.2f}", "unseen, 0.75 or more")
    out = PP.on_act(np.arange(4), ma, 1.0, 0.8, lever=np.full(4, LEVERS.index("voice")), pushes=np.full(4, DOMAINS.index("close")))
    check_b("anyone's voice in the close circle is felt", all(r_["size"] != "none" for r_ in out["results"]),
            str([r_["size"] for r_ in out["results"]]), "never none")
    check_b("push results only returned (not also in PP.events)", not any(e_["kind"] == "push" for e_ in PP.events),
            f"{sum(e_['kind'] == 'push' for e_ in PP.events)} push events", "none")
    # standing per domain (spec 7 §2: a famous actor has national standing in culture, ordinary in the economy)
    ds = np.zeros((4, len(DOMAINS))); ds[3, DOMAINS.index("culture")] = 3; ds[2, DOMAINS.index("institution")] = 2
    S2 = D.S(PP, 30 * 52 + 2); S2["title_standing"] = ts; S2["domain_standing"] = ds; S2["res"][:, 0] = 0.5
    PP.tick(PP.t + 4, S2); PP.month(PP.t, S2)
    by = {}; bya = {}
    for d_ in ("culture", "economy", "state"):
        q0_ = len(getattr(W, "_queue", getattr(W, "pushes", [])))
        o_ = PP.on_act(np.array([3]), ma[:1], 1.0, 0.8, lever=np.array([LEVERS.index("voice")]), pushes=np.array([DOMAINS.index(d_)]))
        by[d_] = o_["results"][0]["size"]; nq_ = list(getattr(W, "_queue", getattr(W, "pushes", [])))[q0_:]
        bya[d_] = float(nq_[0][2]) if nq_ else 0.0
    rv3 = PP.reach_view(3)
    say(f"  domain standing (life 3: culture 3, the rest none): standing by ring {[int(x_) for x_ in PP.standing[3]]}, "
        f"reach culture {PP.dreach[3, DOMAINS.index('culture')]:.0f}, economy {PP.dreach[3, DOMAINS.index('economy')]:.0f}, "
        f"state {PP.dreach[3, DOMAINS.index('state')]:.0f}; a voice that went well: {by}")
    check_b("standing per domain: a cultural figure's voice reaches culture clearly, the economy and the state as one of millions",
            bya["culture"] >= 0.75 and bya["economy"] <= 1e-5 and bya["state"] <= 1e-5
            and all(by[d_] == "unseen" for d_ in by) and rv3["domain_standing"][DOMAINS.index("culture")] == 3,
            f"W.push culture {bya['culture']:.2f}, economy {bya['economy']:.0e}, state {bya['state']:.0e} (shown {by['culture']})",
            "0.75+; 1e-5 or less; 1e-5 or less (shown unseen)")
    # without domain standing, title standing works as before (every outer ring)
    S3 = D.S(PP, 30 * 52 + 3); S3["title_standing"] = ts; S3["res"][:, 0] = 0.5
    PP.tick(PP.t + 4, S3); PP.month(PP.t, S3)
    sz3 = []
    for d_ in ("culture", "economy", "state"):
        q0_ = len(getattr(W, "_queue", getattr(W, "pushes", [])))
        PP.on_act(np.array([3]), ma[:1], 1.0, 0.8, lever=np.array([LEVERS.index("voice")]), pushes=np.array([DOMAINS.index(d_)]))
        nq_ = list(getattr(W, "_queue", getattr(W, "pushes", [])))[q0_:]
        sz3.append(round(float(nq_[0][2]), 2) if nq_ else 0.0)
    check_b("title standing alone (no domain standing) still counts in every outer ring",
            all(x_ >= 0.75 for x_ in sz3) and (PP.dreach == PP.reach[:, wp.RING_OF]).all(),
            f"W.push culture, economy, state {sz3}", "0.75 or more in each")


def save_check(PP, W, saved_lines):
    say("\n== 17. save and load; a legacy line")
    ns = list(range(min(6, PP.N)))
    ds = [PP.save(n_) for n_ in ns]
    js = json.dumps(ds); ds2 = json.loads(js)
    P2 = People.load(W, ds2, run_seed=PP.run_seed)
    PP._alive_counts()   # alive is refreshed monthly; the loaded one is fresh
    def same(f_, i, n_):   # cast fields on the used slots (a dropped member's slot keeps stale values; never read)
        a_, b_ = getattr(P2, f_)[i], getattr(PP, f_)[n_]
        if f_ in ("skind", "snorm"):
            return np.array_equal(a_, b_)
        u_ = PP.used[n_]
        return np.array_equal(P2.used[i], u_) and np.array_equal(a_[u_], b_[u_])
    ok = all(same(f_, i, n_) for i, n_ in enumerate(ns) for f_ in ("c", "pie", "read", "uid", "rmask", "skind", "snorm", "mset", "lv", "born", "trust"))
    ok &= all(np.allclose(P2.alive[i], PP.alive[n_]) for i, n_ in enumerate(ns))
    check_b("save -> JSON -> load gives the same casts and settings", ok, f"{len(js) // 1024} KB for {len(ns)} lives", "identical")
    try:
        P2.tick(PP.t + 1, dict(w=PP.w[ns], held=PP.held[ns], res=PP.res[ns])); runs = True
    except Exception as e_:
        runs = f"{type(e_).__name__}: {e_}"
    check_b("a loaded cast runs on", runs is True, "ran a week" if runs is True else runs, "runs")
    if not saved_lines:
        check_b("legacy birth", False, "no saved line (run shorter than 60 years)", "placed"); return
    WL = make_world(7, years=80 + 60)
    lines = [saved_lines[i % len(saved_lines)] for i in range(20)]
    PL = People(WL, 20, 77); PL.birth(WL.t, legacy=lines)
    placed = 0; gp = 0
    for i, lg in enumerate(lines):
        kids = [m_ for m_ in lg["cast"] if "child" in m_["roles"] and m_["alive"]]
        par = np.nonzero(PL.used[i] & ((PL.rmask[i] & BIT["parent"]) != 0))[0]
        pies = [np.asarray(m_["pie"], np.float32) for m_ in kids]
        if any(any(np.allclose(PL.pie[i, k_], p_, atol=1e-6) for p_ in pies) for k_ in par):
            placed += 1
        g_ = np.nonzero(PL.used[i] & ((PL.rmask[i] & BIT["grandparent"]) != 0))[0]
        if lg["self"]["pie"] is not None and any(np.allclose(PL.pie[i, k_], lg["self"]["pie"], atol=1e-6) for k_ in g_):
            gp += 1
    can = sum(1 for lg in lines if any("child" in m_["roles"] and m_["alive"] and 18 <= (WL.t - m_["born"]) / 52 <= 46 for m_ in lg["cast"]))
    say(f"  20 births into 10 saved lines (saved at 60, born 60 years after the line's own birth): {can} lines had a grown "
        f"child to be the parent; placed {placed}; the ancestor a grandparent in {gp}")
    check_b("a legacy birth is placed in the family", placed == can and can > 0, f"{placed}/{can}", "all that can be")


def rules_check():
    say("\n== 18. rules in world_people.py's source")
    src = open(wp.__file__).read()
    names = set()
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NAME:
            names.add(tok.string)
    bad = sorted(names & {"A", "ALLY", "ENEMY", "AXES", "FRAMINGS", "FR"}) + sorted(n_ for n_ in names if "framing" in n_.lower())
    check_b("no color-pair rule (A, ALLY, ENEMY, AXES, FRAMINGS, framing, FR)", not bad and "framing" not in src.lower(),
            "none" if not bad else ", ".join(bad), "none")
    imps = re.findall(r"^\s*(?:from|import)\s+([\w.]+)", src, re.M)
    check_b("imports: numpy, the standard library (sys), library, world_keys only (never engine.py or world.py)",
            set(imps) <= {"numpy", "sys", "library", "world_keys"}, ", ".join(sorted(set(imps))),
            "numpy, sys, library, world_keys")
    import ast
    tree = ast.parse(src); docs = set()
    for nd in ast.walk(tree):
        if isinstance(nd, (ast.Module, ast.FunctionDef, ast.ClassDef)) and nd.body and isinstance(nd.body[0], ast.Expr) \
                and isinstance(getattr(nd.body[0], "value", None), ast.Constant):
            docs.add(id(nd.body[0].value))
    yrs = [nd.value for nd in ast.walk(tree) if isinstance(nd, ast.Constant) and isinstance(nd.value, str)
           and id(nd) not in docs and re.search(r"\b(1[89]\d\d|20\d\d)\b", nd.value)]
    check_b("timeless: no year in any string the module produces (docstrings aside)", not yrs, "none" if not yrs else str(yrs[:3]), "none")


def emigration_check(Nb=200, Y0=30):
    say(f"\n== 20. emigration and return (spec 5 §5): one life with the neighbour's World; {Nb} lives sharing one World")
    W = make_world(7); t0 = W.t
    how = "W.spawn_neighbour(0)" if hasattr(W, "spawn_neighbour") else "a second World with society_id 1"

    def one(seed):
        PP = People(W if seed is None else make_world(7), 1, 5, female=[True])
        Wh = PP.W; PP.birth(t0); D = Driver(PP, 5); out = {}
        Wx = [Wh]

        def go(t1, t2):
            for t in range(t1, t2):
                Wx[0].tick(t); PP.tick(t, D.S(PP, t - t0)); D.act(PP, t)
        go(t0 + 1, t0 + Y0 * 52)
        if hasattr(Wh, "spawn_neighbour"):   # the neighbour at full detail, at the moment of leaving
            Wn_ = Wh.spawn_neighbour(0)
        else:
            Wn_ = make_world(8); Wn_.society_id = 1
            for t_ in range(Wn_.t + 1, PP.t + 1):
                Wn_.tick(t_)
        sid = out["sid"] = int(getattr(Wn_, "society_id", 1))
        u = PP.used[0] & PP.lv[0]; L2 = PP.P["layer_c"][1]
        hh = PP.hhj[0]; mates = np.nonzero(u & (hh >= 0) & (((PP.mset[0] >> max(hh, 0)) & 1) > 0))[0]
        home = np.nonzero(u & (PP.c[0] >= L2) & ~np.isin(np.arange(PP.K), mates))[0]
        fr = home[(PP.rmask[0, home] & KINMASK) == 0]; kn = home[(PP.rmask[0, home] & KINMASK) != 0]
        c_fr, c_kn = PP.c[0, fr].copy(), PP.c[0, kn].copy(); cls0 = int(PP.cls[0])
        t = PP.t + 1
        loc = PP.emigrate(0, Wn_, None, t); Wx[0] = PP.W
        out["arrive"] = dict(world=PP.W is Wn_, soc=int(PP.soc[0]), status=str(PP.status[0]), lang=float(PP.lang[0]),
                             cls=(cls0, int(PP.cls[0])), sets=sorted(GROUP_KINDS[k_] for k_ in PP.skind[0] if k_ >= 0),
                             mates=bool(len(mates)) and all(PP._here(0, k_) and PP.msoc[0, k_] == sid for k_ in mates),
                             left=len(home) > 0 and not any(PP._here(0, k_) for k_ in home),
                             ev=[e_ for e_ in PP.events if e_["kind"] == "moved"], pv=PP.place_view(0))
        go(t + 1, t + 1 + 3 * 52)
        out["3y"] = dict(lang=float(PP.lang[0]), fr=float(np.median(PP.c[0, fr] / np.maximum(c_fr, 1e-6))) if len(fr) else None,
                         kn=float(np.median(PP.c[0, kn] / np.maximum(c_kn, 1e-6))) if len(kn) else None,
                         sets=sorted(GROUP_KINDS[k_] for k_ in PP.skind[0] if k_ >= 0))
        go(t + 1 + 3 * 52, t + 1 + 6 * 52)
        out["6y"] = dict(lang=float(PP.lang[0]), cls=int(PP.cls[0]))
        PP.set_status(0, "resident"); PP.lang_boost(0, 0.5); st_ = str(PP.status[0])
        t = PP.t + 1
        PP.return_home(0, None, t); Wx[0] = PP.W
        out["back"] = dict(world=PP.W is Wh, soc=int(PP.soc[0]), status=str(PP.status[0]), lang=float(PP.lang[0]),
                           cls=int(PP.cls[0]), cls_home=int(PP.cls_home[0]), st_before=st_,
                           ev=[e_ for e_ in PP.events if e_["kind"] == "moved"],
                           near=int(sum(PP._here(0, k_) for k_ in home if PP.lv[0, k_])))
        go(t + 1, t + 1 + 52)
        out["c"] = PP.c.copy(); out["uid"] = PP.uid.copy()
        return out

    o = one(None)
    a_ = o["arrive"]; sid = o["sid"]
    say(f"  one life, emigrating at {Y0} through {how}: {a_['ev']}; then {a_['pv']}")
    say(f"  settings kept {a_['sets']}; class {a_['cls'][0]} -> {a_['cls'][1]}; after 3 years: language {o['3y']['lang']:.2f}, "
        f"closeness kept by friends at home {o['3y']['fr'] or 0:.2f}, by kin {o['3y']['kn'] or 0:.2f}, settings {o['3y']['sets']}; after 6: "
        f"language {o['6y']['lang']:.2f}, class {o['6y']['cls']}")
    check_b("emigrating: the neighbour's World, its society id, a migrant with a language to learn, one class lower",
            a_["world"] and a_["soc"] == sid and a_["status"] == "migrant" and abs(a_["lang"] - wp.PP_DEFAULT["lang0"]) < 1e-9
            and a_["cls"][1] == max(0, a_["cls"][0] - 1) and a_["ev"] and a_["ev"][0]["why"] == "emigrated"
            and a_["ev"][0]["society"] == sid and a_["pv"]["society"] == sid and a_["pv"]["status"] == "migrant",
            f"world switched {a_['world']}, society {a_['soc']}, {a_['status']}, language {a_['lang']:.2f}, class "
            f"{a_['cls'][0]}->{a_['cls'][1]}", "all")
    check_b("fewer settings at first (household and online only); the household that came lives there; the rest are far",
            set(a_["sets"]) <= {"household", "online"} and a_["mates"] and a_["left"],
            f"{a_['sets']}, came along here {a_['mates']}, left behind far {a_['left']}", "all")
    check("language after 3 years abroad (an adult at full exposure)", o["3y"]["lang"], 0.4, 0.85, "0.4-0.85: grows, not native")
    if o["3y"]["fr"] is not None and o["3y"]["kn"] is not None:
        check_b("friends left behind fade by the distance rules; kin far slower", o["3y"]["fr"] < 0.5 and o["3y"]["kn"] > o["3y"]["fr"],
                f"friends {o['3y']['fr']:.2f}, kin {o['3y']['kn']:.2f} of their closeness kept", "friends < 0.5, kin more")
    b_ = o["back"]
    check_b("return reverses it: the home World, citizen, native language, class back, the people at home near again",
            b_["world"] and b_["soc"] == 0 and b_["status"] == "citizen" and b_["lang"] == 1.0 and b_["cls"] >= b_["cls_home"]
            and b_["ev"] and b_["ev"][0]["why"] == "returned" and b_["st_before"] == "resident",
            f"world {b_['world']}, society {b_['soc']}, {b_['status']}, language {b_['lang']}, class {b_['cls']} "
            f"(home {b_['cls_home']}), {b_['near']} of the people left behind near again; set_status gave {b_['st_before']}", "all")
    o2 = one(1)
    same = np.array_equal(o["c"], o2["c"]) and np.array_equal(o["uid"], o2["uid"])
    check_b("emigration is deterministic (the same seeds: the same life abroad and back)", same, "identical" if same else "differ",
            "identical")
    # many lives in one shared World: the bookkeeping only (no world switch); migrants against those who stay
    W = make_world(7); PP = People(W, Nb, 6, female=np.random.default_rng(6).random(Nb) < 0.5); PP.birth(W.t); D = Driver(PP, 6)
    run(PP, W, D, Y0, W.t + 1)
    mig = np.arange(Nb) % 2 == 0
    nset0 = ((PP.skind >= 0) & (PP.skind != G["household"])).sum(1)
    for n_ in np.nonzero(mig & ~D.dead)[0]:
        PP.emigrate(int(n_), None, 1, PP.t + 1)
    shared = PP.W is W
    t1 = PP.t
    for wk in range(52):
        t = t1 + 1 + wk
        W.tick(t); PP.tick(t, D.S(PP, Y0 * 52 + wk)); D.act(PP, t)
    live = ~D.dead
    nset = ((PP.skind >= 0) & (PP.skind != G["household"]) & (PP.skind != G["online"])).sum(1)
    L2 = PP.P["layer_c"][1]
    near2 = (PP.used & PP.lv & (PP.c >= L2) & (PP.mloc == PP.loc[:, None]) & (PP.msoc == PP.soc[:, None])).sum(1)
    m_, c_ = mig & live, ~mig & live
    say(f"  {Nb} lives in one World, half emigrating at {Y0} (bookkeeping only, the World kept: {shared}): a year on, settings "
        f"outside home {nset[m_].mean():.2f} (migrants) against {nset[c_].mean():.2f}; close people where they live "
        f"{near2[m_].mean():.2f} against {near2[c_].mean():.2f}; language {PP.lang[m_].mean():.2f}; statuses "
        f"{sorted(set(map(str, PP.status[m_])))}, {sorted(set(map(str, PP.status[c_])))}; before leaving {nset0[mig].mean():.2f} settings")
    check_b("shared World: same bookkeeping, no switch; migrants hold fewer settings and fewer close people nearby at first",
            shared and (PP.soc[m_] == 1).all() and (PP.soc[c_] == 0).all() and nset[m_].mean() < nset[c_].mean()
            and near2[m_].mean() < near2[c_].mean() and set(PP.status[m_]) == {"migrant"} and set(PP.status[c_]) == {"citizen"},
            f"settings {nset[m_].mean():.2f} < {nset[c_].mean():.2f}, close nearby {near2[m_].mean():.2f} < {near2[c_].mean():.2f}",
            "fewer at first")


def game_data_check():
    say("\n== 21. the game's data: the birth event, the views")
    W = make_world(7); N = 20; PP = People(W, N, 9, female=np.random.default_rng(9).random(N) < 0.5); PP.birth(W.t)
    D = Driver(PP, 9)
    t = W.t + 1; W.tick(t); PP.tick(t, D.S(PP, 1))
    bn = [e_ for e_ in PP.events if e_["kind"] == "born" and "cls" in e_]
    check_b("the drawn birth (place, neighbourhood, class) reaches the engine in the first week's events",
            len(bn) == N and all(("loc" in e_ and "nb" in e_) for e_ in bn), f"{len(bn)} of {N} in week 1", "all")
    run(PP, W, D, 35, t + 1)
    cv = PP.cast_view(0, layers=(1, 2, 3)); keys = {"last_contact", "loc", "society", "partner", "children"}
    ids = set(int(x_) for x_ in PP.uid[0, PP.used[0]])
    ref_ok = all((c_["partner"] in (None, "you") or c_["partner"] in ids) and all(x_ == "you" or x_ in ids for x_ in c_["children"])
                 for c_ in cv)
    par = [c_ for c_ in cv if c_["role"] == "parent"]; pt = [c_ for c_ in cv if c_["role"] == "partner"]
    fam_ok = all("you" in c_["children"] for c_ in par) and all(c_["partner"] == "you" for c_ in pt)
    lc_ok = all(c_["last_contact"] is None or 0 <= c_["last_contact"] <= 36 * 52 for c_ in cv)
    say(f"  cast view of life 0 (layers 1-3, {len(cv)} people): e.g. " +
        "; ".join(f"{c_['role']} (last met {c_['last_contact']} wk ago, loc {c_['loc']}, partner {c_['partner']}, children "
                  f"{c_['children']})" for c_ in cv[:3]))
    check_b("cast view: last contact, locality and society, partner and children ids (ids in the cast; 'you' for the character)",
            cv and all(keys <= set(c_) for c_ in cv) and ref_ok and fam_ok and lc_ok,
            f"fields {all(keys <= set(c_) for c_ in cv)}, ids {ref_ok}, parents and partner {fam_ok}, weeks {lc_ok}", "all")
    pv = PP.place_view(0)
    check_b("place view: society id, status and language", {"society", "status", "lang"} <= set(pv) and pv["status"] == "citizen"
            and pv["lang"] == 1.0, str({k_: pv[k_] for k_ in ("society", "status", "lang")}), "society, status, language")
    st0 = json.dumps(PP.rng.bit_generator.state, default=str)
    mo = PP.move_options(0, 3); mo2 = PP.move_options(0, 3)
    same_rng = json.dumps(PP.rng.bit_generator.state, default=str) == st0
    say(f"  move options for life 0: {mo}")
    check_b("move options: 3 candidate localities (id, kind, size, features), not the current one; the life's stream untouched",
            len(mo) == 3 and mo == mo2 and len({m_["loc"] for m_ in mo}) == 3 and all(m_["loc"] != PP.loc[0] for m_ in mo)
            and all({"loc", "kind", "size", "features"} <= set(m_) for m_ in mo) and same_rng,
            f"{[m_['loc'] for m_ in mo]}, repeatable {mo == mo2}, stream untouched {same_rng}", "all")
    fv = PP.figure_view(0, W)
    if not fv:
        check_b("public figures through the character's reading", World is None, "no figures (stub World)" if World is None else "none", "figures")
        return
    pie = np.asarray(W.fig_pie, float)
    gap = min(np.abs(np.asarray(f_["read"]) - pie[f_["id"]]).sum() for f_ in fv)
    diff = len({tuple(f_["read"]) for f_ in PP.figure_view(1, W)} ^ {tuple(f_["read"]) for f_ in fv}) > 0
    say(f"  figures for life 0: " + "; ".join(f"{f_['role_name']} (standing {f_['standing']}) read {f_['read']}" for f_ in fv[:3]))
    check_b("public figures: id, role, standing and the character's reading (never the true pie; differs by life)",
            all({"id", "role", "read", "standing"} <= set(f_) for f_ in fv) and gap > 0.01 and diff
            and all(abs(sum(f_["read"]) - 1) < 0.01 for f_ in fv),
            f"{len(fv)} figures, nearest reading to a true pie {gap:.2f} (L1), lives differ {diff}", "readings only")


def children_check():
    say("\n== 22. the character's children follow the engine's count (S['children'], its alive[:, 5])")
    W = make_world(7); t0 = W.t
    PP = People(W, 1, 11, female=[True]); PP.birth(t0); D = Driver(PP, 11)
    for t in range(t0 + 1, t0 + 26 * 52):
        W.tick(t); PP.tick(t, D.S(PP, t - t0)); D.act(PP, t)
    liv = lambda: int((PP.used[0] & PP.lv[0] & ((PP.rmask[0] & BIT["child"]) != 0)).sum())
    c0 = max(1, liv())
    plan = {0: c0, 40: c0 + 1, 90: c0 + 2, 140: "kill"}
    cnt = float(c0); trace = []; born = 0
    for wk in range(200):
        t = PP.t + 1
        if wk in plan:
            if plan[wk] == "kill":   # the engine's death moment: kill() in the cast and its own count one lower
                PP.kill(0, "child"); cnt -= 1
            else:
                cnt = float(plan[wk])
        S = D.S(PP, t - t0); S["children"] = np.array([cnt]); h_ = S["held"].copy(); h_[:, wp.KID] = True; S["held"] = h_
        W.tick(t); PP.tick(t, S); D.act(PP, t)
        born += sum(1 for e_ in PP.events if e_["kind"] == "born" and e_.get("role") == "child")
        trace.append((int(cnt), liv()))
    steps = [x_ for i_, x_ in enumerate(trace) if i_ == 0 or trace[i_ - 1] != x_]
    say(f"  one life from 26, the engine's count {c0} -> {c0 + 1} -> {c0 + 2}, then a child's death (kill) and {c0 + 1}: "
        f"(engine, cast) {steps}; 'born' cast events {born}")
    check_b("each child the engine adds joins the cast with a 'born' event; a death keeps them in step (no replacement)",
            all(a_ == b_ for a_, b_ in trace[1:]) and born == 2 and trace[-1] == (c0 + 1, c0 + 1),
            f"{steps}, {born} born events", "the cast's living children = the engine's count")


def timing_note(tpp, N, Y):
    say("\n== 19. speed")
    per = tpp / (N * Y / (600 * 80))
    check(f"PP.week/month/quarter + on_act + wants, scaled to 600 lives x 80 years (CPU, one core)", per, 0, 60, "< 60 s", "{:.1f} s")


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    Y = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    T = time.time()
    say(f"people_check: world_people.py against its targets ({time.strftime('%H:%M')}; world: {WORLD_SRC})")
    W, PP, D, rec, tpp, saved_lines = main_run(N, Y)
    report_main(N, Y, W, PP, D, rec, tpp)
    vocab_check(rec["events"] | {(k_, v_) for r_ in D.push_res for k_, v_ in r_.items() if isinstance(v_, str) and k_ != "kind"})
    births_check()
    close_first_check()
    fade_check()
    equivariance_check()
    PPd, Wd = determinism_check()
    reach_check()
    save_check(PPd, Wd, saved_lines)
    rules_check()
    emigration_check()
    game_data_check()
    children_check()
    timing_note(tpp, N, Y)
    nok = sum(ok for _, ok in SCORE)
    say(f"\nscore: {nok}/{len(SCORE)} ok; MISS: " + (", ".join(n_ for n_, ok in SCORE if not ok) or "none"))
    say(f"(whole check {time.time() - T:.0f} s wall)")
    with open(os.path.join(HERE, "people_check.out"), "w") as f_:
        f_.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
