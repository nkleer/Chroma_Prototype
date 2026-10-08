"""World-alone checks for world.py (chroma-world/calibration-and-tests.md §2.1; chroma-engine/world-build.md).

Runs N worlds of the first society ("typical rich", pace 1) for 100 years after the 80-year burn-in and prints every
target with its value and ok/MISS, then the structural tests: equivariance under non-rotation color permutations,
symmetry on an even start rotated through the pie (like LIB_SYM), swing, save/load identity, determinism, timing,
the W35 identifier scan, timelessness and the hidden-state check of the snapshot.

Allied and enemy pairs and triads are classified HERE ONLY, from the WUBRG wheel's adjacency; world.py never reads a
pair rule.

    OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B chroma-engine/tools/world_check.py [N_main=200] [N_sym=100]
"""
import sys, os, time, json, re, ast
import _engine   # the engine to check: CHROMA_ENGINE, default the tree's live engine (tools/_engine.py)
HERE = _engine.OUT
PROTO = _engine.ENGINE
import numpy as np
import world as WM
from world import World, COLORS, COMBO_KEYS, NORM_KEYS, LAW_KEYS, INST_KINDS, TECH_KEYS, BREAKTHROUGHS, _tv

N_MAIN, N_SYM = 200, 100            # set from the command line in __main__
YEARS = 100
Q = 13
C = 5
ROWS = []


def row(name, value, target, ok):
    """ok: True / False, or None for information only."""
    flag = "" if ok is None else ("ok" if ok else "MISS")
    ROWS.append((name, value, target, flag))
    print(f"  {name:<46s} {value!s:<34s} {target:<32s} {flag}", flush=True)


def fmt(x, d=2):
    if isinstance(x, (list, tuple, np.ndarray)):
        return "[" + " ".join(f"{float(v):.{d}f}" for v in x) + "]"
    return f"{float(x):.{d}f}"


def section(t):
    print(f"\n{t}", flush=True)


# ---------------------------------------------------------------------------------------------- wheel (test only)
def ctype(key):
    """single, allied pair, enemy pair, shard (allied triad), wedge (enemy triad), from WUBRG adjacency."""
    ix = sorted(COLORS.index(c) for c in key)
    if len(ix) == 1:
        return "single"
    if len(ix) == 2:
        return "allied pair" if (ix[1] - ix[0]) % 5 in (1, 4) else "enemy pair"
    s = set(ix)
    shard = any({i, (i + 1) % 5, (i + 2) % 5} == s for i in range(5))
    return "shard (allied triad)" if shard else "wedge (enemy triad)"


TYPES = ["single", "allied pair", "enemy pair", "shard (allied triad)", "wedge (enemy triad)"]
N_OF_TYPE = {t: sum(ctype(k) == t for k in COMBO_KEYS) for t in TYPES}


def kdir(key):
    v = np.array([1.0 / len(key) if c in key else 0.0 for c in COLORS]) - 0.2
    return v / np.linalg.norm(v)


# ---------------------------------------------------------------------------------------------- one world -> record
def collect(W):
    """Compact per-world record of everything the scorecard needs (the World is dropped after this)."""
    t0, t1 = W.t0, W.t
    tr = [x for x in W.trace if x["t"] > t0]
    T = lambda k: np.array([x[k] for x in tr])
    log = [e for e in W.log if e["t"] > t0]
    ev = lambda d, k: [e for e in log if e["domain"] == d and e["kind"] == k]
    rec = dict(t0=t0, t1=t1)
    rec["t"] = T("t"); rec["phase"] = T("phase"); rec["sev"] = T("sev"); rec["unemp"] = T("unemp"); rec["infl"] = T("infl")
    rec["gap"] = T("gap"); rec["support"] = T("support"); rec["gov_q"] = T("gov_q"); rec["natural"] = T("natural")
    rec["G"] = T("G"); rec["Dem"] = T("Dem"); rec["D0"] = T("D0"); rec["Pos"] = T("Pos"); rec["V"] = T("V")
    rec["era"] = [x["era"] for x in tr]; rec["era_i"] = T("era_i"); rec["lean"] = T("lean")
    rec["laws"] = T("laws"); rec["norms"] = T("norms"); rec["war"] = T("war"); rec["legit"] = T("legit")
    rec["trust"] = T("trust"); rec["regime"] = T("regime"); rec["temp"] = T("temp"); rec["jobloss"] = T("jobloss")
    rec["birth"] = T("birth"); rec["mig"] = T("mig"); rec["loc_unemp"] = T("loc_unemp")
    rec["cycles"] = [c for c in W.cycles if c[0] > t0]
    rec["gov_falls"] = len(ev("state", "government falls"))
    rec["elections"] = [e["value"] for e in ev("state", "election")]
    rec["elect_change"] = sum(e["key"] == "change" for e in ev("state", "election"))
    rec["breaks"] = [(e["t"], e["key"]) for e in ev("era", "breakthrough")]
    rec["era_log"] = [(e["t"], e["kind"], e["key"], e["value"]) for e in W.log if e["domain"] == "era"
                      and e["kind"] in ("era begins", "era ends")]
    rec["regime_changes"] = len(ev("state", "regime changes"))
    cl = [e["value"]["inst"] for e in ev("institution", "closure")]
    rec["closures"] = sum(bool(W.inst_firm[i]) for i in cl); rec["n_firm"] = int(W.inst_firm.sum())        # market firms
    rec["pub_closures"] = sum(bool(W.inst_pubemp[i]) for i in cl); rec["n_pub"] = int(W.inst_pubemp.sum())
    nl_ = [e["value"]["inst"] for e in ev("institution", "new leader")]
    rec["leader_entries"] = (len(nl_), sum(int(W.inst_level[i]) == 2 for i in nl_))
    rec["corruption"] = (float(W.corruption), float(W.inst_corruption.mean()))
    rec["tenure"] = (W.tenure_sum, W.tenure_n)
    rec["pandemics"] = sum(e["key"] == "rising" for e in ev("nature", "pandemic"))
    rec["disasters"] = [e["t"] for e in ev("nature", "disaster")]; rec["n_loc"] = W.n_loc
    rec["tech_arrive"] = len([e for e in ev("tech", "arrives")])
    # tech S-curves: years from 35% to 85% of a new kind's ceiling, for kinds born after the burn-in
    tt = [x["tech"] for x in tr]; tb = tr[-1]["tech_born"]
    sc = []
    for i, b in enumerate(tb):
        if b <= t0:
            continue
        a = np.array([v[i] if len(v) > i else 0.0 for v in tt])
        i35, i85 = np.nonzero(a >= 0.35)[0], np.nonzero(a >= 0.85)[0]
        if len(i35) and len(i85):
            sc.append((rec["t"][i85[0]] - rec["t"][i35[0]]) / 52)
    rec["tech_sc"] = sc
    # secular share by age band at the end (later generations come of age in more secure times)
    pop = W.pop
    rec["secular_age"] = (pop[:, :, :, 0, :].sum((1, 2, 3)) / pop.sum((1, 2, 3, 4))).tolist()
    rec["faith"] = W.faith_share.tolist(); rec["secular"] = W.secular
    rec["urban"] = float(W.loc_pop_share[W.loc_place == 0].sum()); rec["pop_share"] = W.loc_pop_share.copy()
    rec["season_death"] = []
    s0 = W.season
    for s in range(4):
        W.season = s; rec["season_death"].append(W.rate_mult("old_death"))
    W.season = s0
    rec["kinds"] = [k for _, k in rec["breaks"]]
    return rec


def run_world(seed, cfg=None, perm=None, years=YEARS):
    c = dict(trace=True); c.update(cfg or {})
    W = World(seed, cfg=c, color_perm=perm)
    W.burn_in(80)
    W.tick(W.t + years * 52)
    return W


# ---------------------------------------------------------------------------------------------- statistics
def era_stats(recs):
    """Era counts, lengths, gaps, shares by color and type, combination coverage, swing."""
    begins, lens, gaps, seqs = 0, [], [], []
    share_c = np.zeros(C); share_t = {t: 0.0 for t in TYPES}; seen = set(); q_tot = 0; q_era = 0
    for R in recs:
        t0, t1 = R["t0"], R["t1"]
        el = R["era_log"]
        begins += sum(1 for t, k, *_ in el if k == "era begins" and t > t0)
        open_t = None
        for t, k, key, v in el:
            if k == "era begins":
                open_t = t
            elif k == "era ends" and open_t is not None and open_t > t0:
                lens.append((t - open_t) / 52)
        for (ta, ka, *_), (tb, kb, *_) in zip(el[:-1], el[1:]):
            if ka == "era ends" and kb == "era begins" and ta > t0 and tb > ta:
                gaps.append((tb - ta) / 52)
        for e in R["era"]:
            q_tot += 1
            if e is not None:
                q_era += 1; seen.add(e)
                for c in e:
                    share_c[COLORS.index(c)] += 1.0 / len(e)
                share_t[ctype(e)] += 1
        # the sequence of eras with their strength (max intensity while it lasted)
        seq = []
        cur = None
        for e, i in zip(R["era"], R["era_i"]):
            if e != cur:
                if e is not None:
                    seq.append([e, i])
                cur = e
            elif e is not None:
                seq[-1][1] = max(seq[-1][1], i)
        seqs.append(seq)
    N = len(recs)
    out = dict(rate=begins / N, len=np.mean(lens) if lens else np.nan, gap=np.mean(gaps) if gaps else np.nan,
               time_share=q_era / max(q_tot, 1), share_c=share_c / max(share_c.sum(), 1e-9),
               share_t={t: share_t[t] / max(q_era, 1) for t in TYPES}, seen=seen, n_len=len(lens), n_gap=len(gaps))
    # swing: does the next era lean away (negative cosine) more often than two eras drawn at random?
    cons, strong = [], []
    allk = [s for seq in seqs for s in seq]
    for seq in seqs:
        if len(seq) < 2:
            continue
        imed = np.median([s[1] for s in allk])
        for a, b in zip(seq[:-1], seq[1:]):
            cs = float(kdir(a[0]) @ kdir(b[0]))
            cons.append(cs)
            if a[1] >= imed:
                strong.append(cs)
    rng = np.random.default_rng(0)
    ks = [s[0] for s in allk]
    if len(ks) > 2:
        ia, ib = rng.integers(0, len(ks), 20000), rng.integers(0, len(ks), 20000)
        chance = np.mean([kdir(ks[a]) @ kdir(ks[b]) < -1e-9 for a, b in zip(ia, ib) if a != b])
    else:
        chance = np.nan
    # chance within a world: two of the same world's eras that do not follow each other (controls for its own tilt)
    within = []
    for seq in seqs:
        for i in range(len(seq)):
            for j in range(i + 2, len(seq)):
                within.append(float(kdir(seq[i][0]) @ kdir(seq[j][0])) < -1e-9)
    out["swing"] = (np.mean(np.array(cons) < -1e-9) if cons else np.nan, np.mean(np.array(strong) < -1e-9) if strong else np.nan,
                    chance, len(strong), np.mean(within) if within else np.nan)
    # deep shifts: a new era that turns the order (its direction points away from the era before it)
    turns = sum(sum(1 for a, b in zip(seq[:-1], seq[1:]) if kdir(a[0]) @ kdir(b[0]) < -1e-9) for seq in seqs)
    out["turns"] = turns / N
    return out


def regime_rates(n_seeds=8, years=180):
    """Breakthroughs per decade by regime class (democracy >= 6, mixed -5..6, closed < -5), from worlds started at
    regime +9, +2 and -7 (spec 6 §8: mixed regimes break through far more, and the violent ones are there)."""
    yrs, br = np.zeros(3), np.zeros((3, 4))
    for r0 in (9.0, 2.0, -7.0):
        for s in range(n_seeds):
            W = World(300 + s, params=dict(regime0=r0))
            for q in range(years * 4):
                c = 0 if W.regime >= 6 else (2 if W.regime < -5 else 1)
                n0 = len(W.log)
                W.tick(W.t + Q)
                yrs[c] += 0.25
                for e in W.log[n0:]:
                    if e["kind"] == "breakthrough":
                        br[c, BREAKTHROUGHS.index(e["key"])] += 1
    return br / np.maximum(yrs, 1e-9)[:, None] * 10, yrs


def disaster_checks(seeds=(5, 6, 7, 8), years=60):
    """Weekly ticks: disaster_now against the record, the week within the quarter, rate_mult('disaster') with pace and
    in a struck locality (W35 review item 6)."""
    out = dict(flag=0, logged=0, woq=set(), mult={1.0: [], 2.0: []}, struck=[], calm=[])
    for pace in (1.0, 2.0):
        for seed in seeds:
            W = World(seed, cfg=dict(pace=pace)); W.burn_in(20)
            n0 = len(W.record)
            for w in range(W.t + 1, W.t + years * 52 + 1):
                W.tick(w)
                hit = W.disaster_now > 0
                if hit.any():
                    out["flag"] += int(hit.sum()) if pace == 1.0 else 0
                    out["woq"].add(W.t % 13)
                    assert (W.disaster_kind[hit] >= 0).all()
                if W.t % Q == 0:
                    m = W.rate_mult("disaster")
                    out["mult"][pace].append(float(np.mean(m)))
                    if pace == 1.0:
                        base = m / (1 + W.p["dis_active"] * np.minimum(W.loc_disaster, 1))
                        on = W.loc_disaster >= 1
                        out["struck"].extend((m[on] / base[on]).tolist()); out["calm"].extend((m[~on] / base[~on]).tolist())
            if pace == 1.0:
                out["logged"] += sum(1 for e in W.record[n0:] if e["kind"] == "disaster")
    return out


def spawn_checks():
    """spawn_neighbour (W35 review item 3, spec 5 §5): a full World per neighbour, its clock equal to home's."""
    H = World(7); H.burn_in(80); H.tick(H.t + 30 * 52)
    before = json.dumps(H.save(), sort_keys=True)
    times, okc, oks, tvs, regs, rel_ok = [], True, True, [], True, True
    for k in range(H.n_ext):
        t = time.time(); N = H.spawn_neighbour(k); times.append(time.time() - t)
        okc &= N.t == H.t and N.t0 == H.t0 and N.society_id == k + 1 and N.week_of_year == H.week_of_year
        rel_ok &= int(N.ext_society[0]) == 0 and int(N.ext_relation[0]) == int(H.ext_relation[k]) and N.n_ext == H.n_ext
        rel_ok &= sorted(N.ext_society[1:].tolist()) == [j + 1 for j in range(H.n_ext) if j != k]
        regs &= abs(N.regime - H.ext_regime[k]) < 1e-12 and np.allclose(N.G, H.ext_G[k])
        tvs.append(_tv(N.V, H.ext_V[k]))
        A = World.load(json.loads(json.dumps(N.save())))
        N.tick(N.t + 10 * 52); A.tick(A.t + 10 * 52)
        oks &= json.dumps(N.save(), sort_keys=True) == json.dumps(A.save(), sort_keys=True)
    home_same = json.dumps(H.save(), sort_keys=True) == before
    # equivariance of a spawned neighbour
    P = np.array([2, 4, 0, 1, 3])
    A = World(3); A.burn_in(30); B = World(3, color_perm=list(P)); B.burn_in(30)
    NA, NB = A.spawn_neighbour(1, years=20), B.spawn_neighbour(1, years=20)
    NA.tick(NA.t + 5 * 52); NB.tick(NB.t + 5 * 52)
    eq = max(float(np.abs(NA.V[P] - NB.V).max()), float(np.abs(NA.G[P] - NB.G).max()), float(np.abs(NA.Pos[P] - NB.Pos).max()))
    return dict(times=times, okc=okc, oks=oks, tv=tvs, regs=regs, rel=rel_ok, home=home_same, eq=eq)


def main():
    t_start = time.time()
    print(f"world_check: {N_MAIN} worlds x {YEARS} years after an 80-year burn-in, preset typical rich, pace 1")
    recs, times = [], []
    for s in range(N_MAIN):
        t = time.time()
        W = run_world(s)
        times.append(time.time() - t)
        recs.append(collect(W))
        del W
    N = len(recs)
    dec = N * YEARS / 10

    # ------------------------------------------------------------------------------------- economy (spec 1 §2)
    section("ECONOMY (spec 1 §2)                              value                              target")
    exp_l, rec_l, rise, recov = [], [], {0: [], 1: [], 2: []}, {0: [], 1: [], 2: []}
    n_crisis = 0; infl_ep = 0; u_all = []; jl = {0: [], 1: [], 2: [], "exp": []}; bm = {"rec": [], "exp": []}
    for R in recs:
        cyc = [c for c in R["cycles"] if c[1] > 0]
        for a, b in zip(cyc[:-1], cyc[1:]):
            exp_l.append((b[0] - a[1]) / 52)
        tq = R["t"]
        for c in cyc:
            rec_l.append((c[1] - c[0]) / 52 * 12)
            n_crisis += c[2] == 2
            i0 = int(np.searchsorted(tq, c[0])); i1 = int(np.searchsorted(tq, c[1]))
            if i0 >= len(tq) or i1 >= len(tq):
                continue
            base = R["unemp"][max(i0 - 1, 0)]
            rise[c[2]].append(R["unemp"][i0:min(i1 + 8, len(tq))].max() - base)
            # recovery: years from the trough's end until unemployment is back within half a point of natural
            later = np.nonzero(R["unemp"][i1:] <= R["natural"][i1:] + 0.5)[0]
            nxt = [d[0] for d in cyc if d[0] > c[1]]
            if len(later) and (not nxt or tq[i1 + later[0]] < nxt[0]):
                recov[c[2]].append(later[0] / 4)
        hi = R["infl"] >= 6
        infl_ep += int(np.sum(hi[1:] & hi[:-1] & ~np.concatenate([[False], hi[:-2] & hi[1:-1]])))
        u_all.append(R["unemp"])
        for i in range(len(tq)):
            if R["phase"][i] == 1:
                jl[int(R["sev"][i])].append(R["jobloss"][i]); bm["rec"].append(R["birth"][i])
            else:
                jl["exp"].append(R["jobloss"][i]); bm["exp"].append(R["birth"][i])
    u_all = np.concatenate(u_all)
    v = np.mean(exp_l); row("expansion length, years", fmt(v, 1), "about 5", 4.0 <= v <= 6.5)
    v = np.mean(rec_l); row("recession length, months", fmt(v, 1), "about 11", 8 <= v <= 14)
    v = N * YEARS / max(n_crisis, 1); row("banking crisis: once in ... years", fmt(v, 0), "20 to 40", 20 <= v <= 40)
    rs = [np.mean(rise[k]) if rise[k] else np.nan for k in range(3)]
    row("unemployment rise mild/severe/crisis, points", fmt(rs, 1), "about 1.5 / 3 / 5",
        abs(rs[0] - 1.5) <= 0.8 and abs(rs[1] - 3) <= 1.2 and abs(rs[2] - 5) <= 1.8)
    rc = [np.median(recov[k]) if recov[k] else np.nan for k in range(3)]
    row("recovery to natural, years mild/severe/crisis", fmt(rc, 1), "slow: crisis longest, >= 3", rc[2] >= 3 and rc[2] > rc[0])
    pc = np.percentile(u_all, [5, 50, 95])
    row("unemployment p5 / median / p95, percent", fmt(pc, 1), "realistic: 3-6 / 5-7.5 / 8-14",
        3 <= pc[0] <= 6 and 5 <= pc[1] <= 7.5 and 8 <= pc[2] <= 14)
    v = N * YEARS / max(infl_ep, 1); row("big inflation (>=6% two quarters): once in", fmt(v, 0) + " years", "20 to 25 (ok 15-35)", 15 <= v <= 35)
    j = [np.mean(jl[k]) for k in ("exp", 0, 1, 2)]
    row("job loss multiplier expansion/mild/severe/crisis", fmt(j, 2), "about double in a deep recession",
        1.6 <= j[3] <= 2.6 and j[2] > j[1] > j[0])
    b = [np.mean(bm["exp"]), np.mean(bm["rec"])]
    row("birth multiplier expansion / recession", fmt(b, 3), "births fall in downturns", b[1] < b[0])

    # ------------------------------------------------------------------------------------- state (spec 1 §3)
    section("STATE (spec 1 §3)")
    v = sum(R["gov_falls"] for R in recs) / dec
    row("changes of government per decade", fmt(v, 2), "every 8-10 years: 1.0-1.25", 0.9 <= v <= 1.4)
    el = [x for R in recs for x in R["elections"]]
    ch = sum(R["elect_change"] for R in recs)
    row("elections per decade; share lost by incumbents", f"{len(el) / dec:.2f}; {ch / max(len(el), 1):.2f}", "info", None)
    sup, gp, srec, sexp, slope_x, slope_y = [], [], [], [], [], []
    thd, thg = [], []
    for R in recs:
        sup.append(R["support"]); gp.append(R["gap"])
        srec += list(R["support"][R["phase"] == 1]); sexp += list(R["support"][R["phase"] == 0])
        m = R["gov_q"] > 0
        slope_x += list(R["gov_q"][m] / 4); slope_y += list(R["support"][m])
        dD = R["Dem"][1:] - R["Dem"][:-1]; dG = R["G"][1:] - R["G"][:-1]       # same-quarter changes (Wlezien 1995)
        m = np.abs(dG).sum(1) > 1e-9
        thd.append(dD[m].ravel()); thg.append(dG[m].ravel())
    c = np.corrcoef(np.concatenate(sup), np.concatenate(gp))[0, 1]
    row("support vs output gap: correlation", fmt(c, 2), "positive (economic vote)", c > 0.1)
    d = np.mean(srec) - np.mean(sexp)
    row("support in recession minus expansion", fmt(d, 3), "negative", d < -0.01)
    sl = np.polyfit(slope_x, slope_y, 1)[0]
    row("support per year in office (slope)", fmt(sl, 4), "negative (cost of ruling)", sl < 0)
    c = np.corrcoef(np.concatenate(thd), np.concatenate(thg))[0, 1]
    row("thermostat: corr(change in demand, change in G)", fmt(c, 2), "negative (demand moves against policy)", c < 0)
    turnout = [x["turnout"] for x in el]
    v = np.mean(turnout); row("turnout", fmt(v, 2), "about 2 in 3", 0.55 <= v <= 0.75)
    v = sum(R["regime_changes"] for R in recs) / N
    row("regime changes per world-century", fmt(v, 3), "rich democracies rarely fall", v <= 0.05)
    war = np.concatenate([R["war"] for R in recs])
    row("share of quarters at war abroad / at home", f"{np.mean(war == 1):.3f} / {np.mean(war == 2):.4f}", "rare, abroad (R7)",
        np.mean(war == 1) <= 0.12 and np.mean(war == 2) <= 0.005)
    # laws trail norms: years from the norm crossing 50% (law not legal) to the law becoming legal
    lags, early, n_leg = [], 0, 0
    for R in recs:
        L, Nn, tq = R["laws"], R["norms"], R["t"]
        for k in range(len(LAW_KEYS)):
            for i in range(1, len(tq)):
                if L[i - 1, k] > 0 and L[i, k] == 0:
                    n_leg += 1
                    if Nn[i, k] < 0.5:
                        early += 1
                    above = np.nonzero(Nn[:i, k] < 0.5)[0]
                    if Nn[i, k] >= 0.5 and len(above) and above[-1] + 1 < i:
                        lags.append((tq[i] - tq[above[-1] + 1]) / 52)
    v = np.median(lags) if lags else np.nan
    row("laws trail norms: median years from 50% to legal", fmt(v, 1) + f" (n={len(lags)})", "years (estimate: 2-15)", 2 <= v <= 15)
    v = early / max(n_leg, 1)
    row("legalisations with the norm still below 50%", fmt(v, 2) + f" (of {n_leg})", "few (estimate <= 0.35)", v <= 0.35)
    laws_end = np.mean([R["laws"][-1] for R in recs], 0)
    row("law state at the end, mean per key (0 legal..2)", fmt(laws_end, 1), "info: " + ",".join(k[:4] for k in LAW_KEYS), None)

    # ------------------------------------------------------------------------------------- culture (spec 1 §4)
    section("CULTURE (spec 1 §4)")
    sc = []
    for R in recs:
        Nn, tq = R["norms"], R["t"]
        for k in range(len(NORM_KEYS)):
            lo = Nn[:, k] <= 0.27
            for i in np.nonzero(lo)[0]:
                if i + 1 < len(tq) and not lo[i + 1]:
                    hi = np.nonzero(Nn[i + 1:, k] >= 0.70)[0]
                    if len(hi) and not lo[i + 1:i + 1 + hi[0]].any():
                        sc.append((tq[i + 1 + hi[0]] - tq[i]) / 52)
    v = np.median(sc) if sc else np.nan
    row("norm 27% -> 70% as it happens (target drifts)", fmt(v, 1) + f" (n={len(sc)})", "info (slow drivers: rare and slow)", None)
    # the S-curve itself: a norm whose drivers have turned (target held near 85%), from 27% to 70%
    cs = []
    for s in range(20):
        W = World(500 + s); W.burn_in(80)
        k = WM.NI["same-sex marriage"]
        W.norm_x0[k] += WM._logit(0.85) - WM._logit(W.norm("same-sex marriage"))
        W.norm_x[k] = WM._logit(0.27); W.norm_hist[:, k] = WM._logit(0.27)
        t0 = W.t; done = 99.0
        while W.t < t0 + 60 * 52:
            W.tick(W.t + 13)
            if W.norm("same-sex marriage") >= 0.70:
                done = (W.t - t0) / 52; break
        cs.append(done)
    v = np.median(cs)
    row("norm S-curve: 27% to 70% once the drivers turn", fmt(v, 1) + " years", "about 25 (same-sex marriage, Gallup)", 18 <= v <= 32)
    n10 = np.concatenate([np.abs(R["norms"][40:] - R["norms"][:-40]).ravel() for R in recs])
    row("norm change per decade, median / p90", f"{np.median(n10):.3f} / {np.percentile(n10, 90):.3f}", "info", None)
    nend = np.mean([R["norms"][-1] for R in recs], 0)
    row("norms at the end, mean", fmt(nend, 2), "info: NORM_KEYS order", None)
    vd10 = np.concatenate([[_tv(R["V"][i + 40], R["V"][i]) for i in range(0, len(R["V"]) - 40, 40)] for R in recs])
    vd100 = [_tv(R["V"][-1], R["V"][0]) for R in recs]
    row("value climate drift per decade (TV)", fmt(np.mean(vd10), 4), "modest (0.002-0.02)", 0.002 <= np.mean(vd10) <= 0.02)
    row("value climate drift per century (TV)", fmt(np.mean(vd100), 4), "clear: >= 2x a decade's, <= 0.12",
        2 * np.mean(vd10) <= np.mean(vd100) <= 0.12)
    tr = np.concatenate([R["trust"] for R in recs])
    row("social trust (0..1)", fmt(np.mean(tr), 3), "about 0.45 (ESS ~5 of 10)", 0.40 <= np.mean(tr) <= 0.50)
    kinds = [k for R in recs for k in R["kinds"]]
    row("restorations (backlash eras) per century", fmt(kinds.count("restoration") / N, 2), "backlash appears (> 0)",
        kinds.count("restoration") > 0)

    # ------------------------------------------------------------------------------------- society and eras (spec 6)
    section("SOCIETY AND ERAS (spec 6)")
    v = kinds.count("reform") / N
    row("reform waves: one every ... years", fmt(YEARS / max(v, 1e-9), 1) + f" ({v:.1f}/century)", "8 to 12", 7 <= YEARS / v <= 13)
    v = kinds.count("revolution") / N
    row("revolutions per world-century", fmt(v, 3), "essentially none", v <= 0.05)
    row("revivals per century", fmt(kinds.count("revival") / N, 2), "info", None)
    rv_in, rv_cos, rv_next = 0, 0, 0
    for R in recs:
        begins = [(t, v["kind"]) for t, kd, key, v in R["era_log"] if kd == "era begins"]
        bt = [t for t, k in R["breaks"]]
        for t, k in R["breaks"]:
            if k != "revival":
                continue
            nxt = [b for b in begins if b[0] >= t]
            later = [b for b in bt if b > t]
            if nxt and nxt[0][0] - t <= 8 * Q and not (later and later[0] <= nxt[0][0]):
                rv_in += 1; rv_cos += nxt[0][1] == "cosmology"
            rv_next += bool(nxt) and nxt[0][1] == "cosmology"
    n_rv = kinds.count("revival")
    row("revival then an era within 2 y: cosmology", f"{rv_cos} of {rv_in} (next era cosmology {rv_next} of {n_rv})",
        "all (spec 6 §5-6)", rv_in > 0 and rv_cos == rv_in)
    E = era_stats(recs)
    row("eras per century", fmt(E["rate"], 2), "about 5 (12 + 8 years)", 3.5 <= E["rate"] <= 7)
    row("era length, years", fmt(E["len"], 1) + f" (n={E['n_len']})", "near 12 (8-16)", 8 <= E["len"] <= 16)
    row("gap between eras, years", fmt(E["gap"], 1) + f" (n={E['n_gap']})", "near 8 (4-12)", 4 <= E["gap"] <= 12)
    row("share of years inside an era", fmt(E["time_share"], 2), "about 0.6 (12 / 20)", 0.45 <= E["time_share"] <= 0.75)
    v = YEARS / max(E["turns"], 1e-9)
    row("deep shifts (order turns away): one every", fmt(v, 1) + " years", "20 to 35", 20 <= v <= 35)
    row("era-year share by color W U B R G", fmt(E["share_c"], 3), "info (preset tilt)", None)
    row("era-year share by type", " ".join(f"{E['share_t'][t]:.2f}" for t in TYPES), "info: single allied enemy shard wedge", None)
    row("combinations seen as eras", f"{len(E['seen'])} of {len(COMBO_KEYS)}", "every combination reachable", len(E["seen"]) == len(COMBO_KEYS))
    for t in TYPES:
        if E["share_t"][t] <= 0:
            row(f"type never occurs: {t}", "0", "all types occur", False)
    sw = E["swing"]
    row("swing: next era leans away (all / after strong)", f"{sw[0]:.2f} / {sw[1]:.2f}", f"> chance {sw[2]:.2f}", sw[1] > sw[2] + 0.03)
    rr, ry = regime_rates()
    row("breakthroughs per decade: democracy / mixed / closed", fmt(rr.sum(1), 2) + f" (years {ry[1]:.0f} mixed)",
        "mixed far more (spec 6 §8)", rr[1].sum() >= 2 * rr[0].sum() and rr[1].sum() > rr[2].sum())
    row("revolutions per decade: democracy / mixed / closed", fmt(rr[:, 1], 2), "the violent ones in mixed regimes",
        rr[1, 1] > max(rr[0, 1], rr[2, 1]))

    # ------------------------------------------------------------------------------------- institutions (spec 4)
    section("INSTITUTIONS (spec 4)")
    lg = np.concatenate([R["legit"] for R in recs]).mean(0)
    tg = [0.40, 0.60, 0.50, 0.40]
    row("trust in government / police / courts / media", fmt(lg, 2), "0.4 / 0.6 / 0.5 / 0.4 (OECD 2023)",
        all(abs(a - b) <= 0.06 for a, b in zip(lg, tg)))
    v = sum(R["closures"] for R in recs) / sum(R["n_firm"] * YEARS for R in recs)
    row("firm exits per year (market firms)", fmt(v, 3), "0.08 to 0.10", 0.07 <= v <= 0.11)
    vp = sum(R["pub_closures"] for R in recs) / sum(R["n_pub"] * YEARS for R in recs)
    row("public employers closed or merged per year", fmt(vp, 3), "follow the budget: well below firms", vp < 0.4 * v)
    le = np.array([R["leader_entries"] for R in recs], float).sum(0) / (N * YEARS)
    row("new leaders on the record per year (national of them)", f"{le[0]:.1f} ({le[1]:.1f})",
        "routine local changes off the record", None)
    cr = np.mean([R["corruption"] for R in recs], 0)
    row("state corruption (public bodies by reach); all bodies", f"{cr[0]:.3f}; {cr[1]:.3f}", "info (registry state.corruption)", None)
    v = sum(R["tenure"][0] for R in recs) / max(sum(R["tenure"][1] for R in recs), 1) / 4
    row("leader tenure, years", fmt(v, 1), "5 to 7", 5 <= v <= 7)

    # ------------------------------------------------------------------------------------- outer ring and place (spec 3, 5)
    section("OUTER RING AND PLACE (spec 3, 5)")
    v = sum(R["pandemics"] for R in recs) / (N * YEARS)
    row("severe pandemics per year", fmt(v, 4), "about 0.02", 0.012 <= v <= 0.03)
    d10 = sum(sum(1 for t in R["disasters"] if t <= R["t0"] + 520) for R in recs) / sum(R["n_loc"] * 10 for R in recs)
    d90 = sum(sum(1 for t in R["disasters"] if t > R["t0"] + 4680) for R in recs) / sum(R["n_loc"] * 10 for R in recs)
    row("disasters per locality-year, first / last decade", f"{d10:.3f} / {d90:.3f}", "~0.04 today (estimate), rising", 0.025 <= d10 <= 0.06 and d90 > d10)
    D = disaster_checks()
    row("disaster_now: strikes flagged / logged (60 y x 4)", f"{D['flag']} / {D['logged']}", "every logged strike flagged",
        0.98 * D["logged"] <= D["flag"] <= D["logged"] and D["logged"] > 0)
    row("disaster strikes: weeks of the quarter used", f"{len(D['woq'])} of 13", "spread over the quarter", len(D["woq"]) == 13)
    m1, m2 = np.mean(D["mult"][1.0]), np.mean(D["mult"][2.0])
    row("rate_mult('disaster') mean, pace 1 / pace 2", f"{m1:.2f} / {m2:.2f}", "pace multiplies it", 1.7 <= m2 / m1 <= 2.3)
    v = np.mean(D["struck"]) / np.mean(D["calm"])
    row("rate_mult('disaster') recovering / calm locality", fmt(v, 2), "higher where a disaster struck", v > 1.5)
    tw = np.mean([(R["temp"][40] - R["temp"][0]) for R in recs])
    row("warming in the first decade, degrees", fmt(tw, 3), "0.2 to 0.25", 0.18 <= tw <= 0.26)
    ex = [WM.World._extremes(1.0)[4], WM.World._extremes(2.0)[4]]
    row("hot extremes at 1 and 2 degrees (x pre-industrial)", fmt(ex, 2), "2.8 / 5.6 (IPCC AR6)", abs(ex[0] - 2.8) < 0.05 and abs(ex[1] - 5.6) < 0.05)
    sd = np.mean([R["season_death"] for R in recs], 0)
    v = sd[0] / sd[2]
    row("winter / summer old-age deaths", fmt(v, 2), "1.1 to 1.3", 1.1 <= v <= 1.3)
    v = np.mean([np.mean(R["mig"]) for R in recs])
    row("migrant share of residents", fmt(v, 3), "about 1 in 7 (0.10-0.18)", 0.10 <= v <= 0.18)
    sa = np.mean([R["secular_age"] for R in recs], 0)
    row("secular share by age band 0-15 .. 75+", fmt(sa, 2), "younger more secular", sa[1:3].mean() > sa[6:].mean())
    row("faith shares (0 duty, 1 learning, 2 passion); secular", fmt(np.mean([R["faith"] for R in recs], 0), 2)
        + f"; {np.mean([R['secular'] for R in recs]):.2f}", "info", None)
    sc = [x for R in recs for x in R["tech_sc"]]
    v = np.median(sc) if sc else np.nan
    row("new technology: years from 35% to 85% of reach", fmt(v, 1) + f" (n={len(sc)})", "about 10 (smartphones)", 7 <= v <= 14)
    v = YEARS * N / max(sum(R["tech_arrive"] for R in recs), 1)
    row("a major new technology every ... years", fmt(v, 1), "15 to 25", 15 <= v <= 25)
    v = np.mean([R["urban"] for R in recs])
    row("city share of residents", fmt(v, 2), "info (urban incl. towns ~0.8)", None)
    sp = np.concatenate([R["loc_unemp"].max(1) / R["loc_unemp"].min(1) for R in recs])
    row("regional unemployment spread (max / min place)", fmt(np.median(sp), 2), "a factor of 2 to 3", 1.8 <= np.median(sp) <= 3.0)
    def wpct(v, w, q):
        o = np.argsort(v); c = np.cumsum(w[o]) / w.sum(); return v[o][min(np.searchsorted(c, q), len(v) - 1)]
    pp = [wpct(u, R["pop_share"], 0.9) / wpct(u, R["pop_share"], 0.1) for R in recs for u in R["loc_unemp"][::8]]
    row("unemployment P90 / P10 across residents", fmt(np.median(pp), 2), "info", None)

    # ------------------------------------------------------------------------------------- tests
    section("TESTS")
    t_w = np.mean(times)
    best = []
    for s in range(5):                                   # best of five: the benchmark least disturbed by other work
        t = time.time(); W = World(900 + s); W.burn_in(80); W.tick(W.t + YEARS * 52); best.append(time.time() - t)
    row("time per world (80 y burn-in + 100 y), batch mean", fmt(t_w, 2) + " s", "info (machine load varies)", None)
    row("time per world, best of 5 (no trace)", fmt(min(best), 2) + " s", "well under 2 s", min(best) < 1.8)

    # equivariance: same seed, a non-rotation permutation applied to every color table
    worst, eras_ok, other_ok = 0.0, True, True
    for P in ([1, 0, 2, 3, 4], [0, 3, 2, 1, 4], [2, 4, 0, 1, 3]):
        P = np.array(P); inv = np.argsort(P)
        for seed in (1, 2):
            A = run_world(seed); B = run_world(seed, perm=list(P))
            for a, b in zip(A.trace, B.trace):
                for k in ("V", "Pos", "G", "Dem"):
                    worst = max(worst, float(np.abs(a[k][P] - b[k]).max()))
                other_ok &= abs(a["unemp"] - b["unemp"]) < 1e-9 and abs(a["support"] - b["support"]) < 1e-9 \
                    and (a["laws"] == b["laws"]).all() and a["phase"] == b["phase"]
            img = lambda k: "".join(sorted([COLORS[inv[COLORS.index(c)]] for c in k], key=COLORS.index))
            ka = [e["key"] for e in A.log if e["kind"] == "era begins"]; kb = [e["key"] for e in B.log if e["kind"] == "era begins"]
            eras_ok &= [img(k) for k in ka] == kb and len(A.log) == len(B.log)
    row("equivariance (WU swap, UR swap, a 5-cycle; 180 y)", f"max diff {worst:.1e}; eras {eras_ok}; rest {other_ok}",
        "exact permutation", worst < 1e-9 and eras_ok and other_ok)

    # symmetry: even start, every color table rotated through the pie (world i uses rotation i mod 5)
    srecs = []
    for i in range(N_SYM):
        P = list(np.roll(np.arange(C), -(i % 5)))
        W = run_world(10000 + i, cfg=dict(preset="even"), perm=P)
        R = collect(W); R["rot"] = i % 5; srecs.append(R); del W
    S = era_stats(srecs)
    per_w = []
    for R in srecs:
        sh = np.zeros(C)
        for e in R["era"]:
            if e is not None:
                for c in e:
                    sh[COLORS.index(c)] += 1.0 / len(e)
        per_w.append(sh / max(sh.sum(), 1e-9))
    per_w = np.array(per_w)
    se = per_w.std(0) / np.sqrt(len(per_w))
    z = np.abs(S["share_c"] - 0.2) / np.maximum(se, 1e-9)
    row("symmetry: era-year share by color", fmt(S["share_c"], 3), f"even, |z|<3 (max z {z.max():.1f})", z.max() < 3)
    pos = np.array([R["Pos"].mean(0) for R in srecs]); vv = np.array([R["V"].mean(0) for R in srecs])
    zp = np.abs(pos.mean(0) - 0.2) / (pos.std(0) / np.sqrt(len(pos)) + 1e-12)
    zv = np.abs(vv.mean(0) - 0.2) / (vv.std(0) / np.sqrt(len(vv)) + 1e-12)
    row("symmetry: mean Pos by color", fmt(pos.mean(0), 3), f"even, |z|<3 (max z {zp.max():.1f})", zp.max() < 3)
    row("symmetry: mean V by color", fmt(vv.mean(0), 3), f"even, |z|<3 (max z {zv.max():.1f})", zv.max() < 3)
    per_combo = {t: S["share_t"][t] / N_OF_TYPE[t] for t in TYPES}
    row("symmetry: era years per combination, by type", " ".join(f"{per_combo[t]:.3f}" for t in TYPES),
        "info: single allied enemy shard wedge", None)
    ra = per_combo["enemy pair"] / max(per_combo["allied pair"], 1e-9)
    rw = per_combo["wedge (enemy triad)"] / max(per_combo["shard (allied triad)"], 1e-9)
    row("symmetry: enemy/allied pair; wedge/shard (per combo)", f"{ra:.2f}; {rw:.2f}", "all occur (wedges as available as shards)",
        min(ra, rw) > 0)
    row("symmetry: combinations seen as eras", f"{len(S['seen'])} of {len(COMBO_KEYS)}", "every combination", len(S["seen"]) == len(COMBO_KEYS))
    u0 = np.array([w for w, R in zip(per_w, srecs) if R["rot"] == 0]).mean(0)
    row("content tilt of the unrotated even world (rot 0)", fmt(u0, 3), "info: what the content tables lean to", None)
    sw = S["swing"]
    row("symmetry run swing: leans away (all / strong)", f"{sw[0]:.2f} / {sw[1]:.2f}", f"> chance {sw[2]:.2f}", sw[1] > sw[2] + 0.03)

    # save and load: 20 y + save + JSON + load + 20 y == 40 y
    A = World(7); A.burn_in(80); A.tick(A.t + 20 * 52)
    B = World.load(json.loads(json.dumps(A.save())))
    A.tick(A.t + 20 * 52); B.tick(B.t + 20 * 52)
    sa_, sb_ = json.dumps(A.save(), sort_keys=True), json.dumps(B.save(), sort_keys=True)
    row("save/load identity (20 y + save/load + 20 y = 40 y)", f"{sa_ == sb_} ({len(sa_) // 1024} KB)", "identical", sa_ == sb_)
    # determinism per seed, and no shared state between worlds (a world never sees N or another world)
    X = World(11); X.burn_in(80); X.tick(X.t + 30 * 52)
    Y = World(11); Z = World(12); Y.burn_in(80); Z.burn_in(80)
    for w in range(Y.t + 1, Y.t + 30 * 52 + 1):
        Y.tick(w); Z.tick(w)
    same = json.dumps(X.save(), sort_keys=True) == json.dumps(Y.save(), sort_keys=True)
    row("deterministic per seed, independent of other worlds", str(same), "identical", same)
    # weekly ticks equal one jump
    X2 = World(11); X2.burn_in(80)
    for w in range(X2.t + 1, X2.t + 30 * 52 + 1):
        X2.tick(w)
    same = json.dumps(X.save(), sort_keys=True) == json.dumps(X2.save(), sort_keys=True)
    row("tick(week) every week == tick(t + n)", str(same), "identical", same)
    # pace multiplies hazards only
    Pa = [run_world(s, cfg=dict(pace=2.0)) for s in range(10)]
    Pb = [run_world(s) for s in range(10)]
    ra_ = sum(len([c for c in W.cycles if c[0] > W.t0]) for W in Pa) / max(sum(len([c for c in W.cycles if c[0] > W.t0]) for W in Pb), 1)
    row("pace 2: recessions relative to pace 1", fmt(ra_, 2), "more (hazards x pace)", ra_ > 1.2)
    del Pa, Pb

    # spawn_neighbour (emigration, spec 5 §5)
    SP = spawn_checks()
    row("spawn_neighbour: time per neighbour, max", fmt(max(SP["times"]), 2) + " s" + f" (n={len(SP['times'])})", "under about 3 s",
        max(SP["times"]) < 3)
    row("spawn: t, t0, week equal; society_id k + 1", str(SP["okc"]), "True", SP["okc"])
    row("spawn: home is neighbour 0, relation mirrored", str(SP["rel"]), "True", SP["rel"])
    row("spawn: regime and government from the light state", str(SP["regs"]) + f"; V vs light TV {np.mean(SP['tv']):.3f}",
        "True; V near (TV < 0.06)", SP["regs"] and np.mean(SP["tv"]) < 0.06)
    row("spawn: home world untouched; neighbour save/load", f"{SP['home']}; {SP['oks']}", "True; identical", SP["home"] and SP["oks"])
    row("spawn: equivariance (5-cycle, 25 y)", f"max diff {SP['eq']:.1e}", "exact permutation", SP["eq"] < 1e-9)
    # burn_in on a world that has already run keeps the climate's anchor (W35 review section 5)
    Wc = World(7); Wc.burn_in(80); Wc.tick(Wc.t + 60 * 52); w1 = Wc.warming
    Wc.burn_in(20); Wc.tick(Wc.t + Q); w2 = Wc.warming
    d = Wc.save(); d["state"].pop("clim_t0"); Wl = World.load(json.loads(json.dumps(d)))
    row("burn_in after a run: warming before / after", f"{w1:.2f} / {w2:.2f}; legacy load anchored {Wl.clim_t0 == Wl.t0}",
        "keeps rising; True", w2 >= w1 and Wl.clim_t0 == Wl.t0)

    # W35: no world code reads a pair rule or the framing
    src = open(os.path.join(PROTO, "world.py")).read()
    tree = ast.parse(src)
    bad = set()
    forbidden = {"A", "ALLY", "ENEMY", "AXES", "FRAMINGS", "FR", "framing"}
    for node in ast.walk(tree):
        name = node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else \
            node.arg if isinstance(node, ast.arg) else None
        if name and (name in forbidden or name.startswith("framing")):
            bad.add(name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) else [])
            for m in mods:
                if m and m.split(".")[0] in ("engine", "batch", "explain", "multiprocessing"):
                    bad.add("import " + m)
                if isinstance(node, ast.ImportFrom):
                    for a in node.names:
                        if a.name in forbidden or a.name.startswith("framing"):
                            bad.add(a.name)
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value == "framing":
            bad.add('P["framing"]')
    row("W35 scan: A ALLY ENEMY AXES FRAMINGS FR framing", "none" if not bad else ",".join(sorted(bad)), "none", not bad)

    # content balance: each color's weight across the content tables
    ns = WM.NORM_PROF.sum(0); fs = WM.FAITH_PROF.sum(0); gs = np.sum(list(WM.GUILD_MIX.values()), 0)
    row("balance: norm profiles, column sums", fmt(ns, 2), "info (freedoms serve R and B more)", None)
    row("balance: faith profiles; guild mixes, column sums", fmt(fs, 2) + "; " + fmt(gs, 1), "even", np.ptp(fs) < 0.02 and np.ptp(gs) < 1e-9)
    # LOAD and COMBO_MIX against the engine's own (importing schwartz imports the engine; the test only)
    try:
        import schwartz, engine
        ok = np.allclose(WM.LOAD, schwartz.LOAD) and set(COMBO_KEYS) == set(engine.COMBO_MIX) and \
            all(np.allclose(WM.COMBO_MIX[i], engine.COMBO_MIX[k]) for i, k in enumerate(COMBO_KEYS))
        row("LOAD = schwartz.LOAD; COMBO_MIX = engine.COMBO_MIX", str(ok), "identical copies", ok)
    except Exception as e:                                            # the engine may be mid-edit in another session
        row("LOAD = schwartz.LOAD; COMBO_MIX = engine.COMBO_MIX", f"skipped ({type(e).__name__})", "identical copies", None)
    M = WM.LOAD - WM.LOAD.mean(0)
    prof = M @ (WM.V_RICH - 0.2)
    r = np.corrcoef(prof, WM.ESS_RICH - WM.ESS_RICH.mean())[0, 1]
    row("V_RICH: fit of its Schwartz profile to the ESS mean", f"r = {r:.2f}; V = {fmt(WM.V_RICH, 3)}", "shape match (LOAD spans 4 dims)", r > 0.5)

    # timeless, JSON-safe, public snapshot
    W = run_world(3, years=40)
    strs = []
    def walk(o):
        if isinstance(o, str):
            strs.append(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(k); walk(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                walk(v)
    snap = W.snapshot()
    walk(W.log); walk(W.record); walk(snap)
    years_ = [s for s in strs if re.search(r"(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)", s)]
    row("timeless: no year in any string the world writes", "none" if not years_ else str(years_[:3]), "none", not years_)
    try:
        json.dumps(W.log); json.dumps(W.record); json.dumps(snap); js = True
    except TypeError:
        js = False
    row("log, record and snapshot are JSON-safe", str(js), "True", js)
    keys = set()
    def wk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                keys.add(k); wk(v)
        elif isinstance(o, list):
            for v in o:
                wk(v)
    wk(snap)
    hidden = keys & {"Q", "pressure", "q_thr", "lean", "Pos", "Dem", "G", "odds", "hazard", "hazards", "pie", "harsh_loc", "V"}
    row("snapshot holds no hidden state", "none" if not hidden else ",".join(sorted(hidden)), "none", not hidden)
    entry = W.log[-1]
    ok = set(entry) >= {"t", "age", "era", "domain", "kind", "key", "value", "who"}
    row("log entry shape dict(t, age, era, domain, kind, key, value, who)", ",".join(entry), "those keys", ok)

    n_miss = sum(1 for r_ in ROWS if r_[3] == "MISS"); n_ok = sum(1 for r_ in ROWS if r_[3] == "ok")
    print(f"\n{n_ok} ok, {n_miss} MISS, {sum(1 for r_ in ROWS if r_[3] == '')} info; total time {time.time() - t_start:.0f} s")
    for r_ in ROWS:
        if r_[3] == "MISS":
            print("  MISS:", r_[0], r_[1], "| target", r_[2])


if __name__ == "__main__":
    N_MAIN = int(sys.argv[1]) if len(sys.argv) > 1 else N_MAIN
    N_SYM = int(sys.argv[2]) if len(sys.argv) > 2 else N_SYM
    main()
