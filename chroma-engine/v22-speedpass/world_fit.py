"""v25 lane A: how the world bears on a life (chroma-engine/notes/v25/other-shapes.md sections 1 and 2, contracts.md
sections 1 and 8; Emren's v25 decisions #5 and #10). Functions only, on the World and People state; _run calls them.

- imp_world (N3, setbacks that fit the world): each setback kind's weight for each life, g[n, k] = the product over the
  kind's facts of (fact / ref) ** e (realm.IMP_WORLD), clipped to IMP_WORLD_CLIP. The facts about the life (crime where
  it lives, harm, the land, frailty, age) are divided by their mean over the living people (the lives and their casts)
  each year, so each kind's count holds and only who gets it moves; the facts about the world (weak law, repression) are
  read against IMP_WORLD_REF and not normalised, so a harsher world has more.
- tilt_world (#10, what a world rewards): r[town, sphere, colour] from the town's sphere mix and the realm's incentives,
  read at one site only, the years that make a regular and a known face (world_people_settings._sph_hours).

The realm (realm_earth, or the test world realm_neutral) is chosen by P["realm"]. Nothing here draws from the run's
streams; an institution's own deviation is drawn from a stream seeded by its id.
"""
import numpy as np

C = 5
IMP_FACTS = ("crime", "weak", "repress", "harm", "land", "frail", "age")   # the cause keys (nw_imp_cause's 14 + index)
LIFE_FACTS = ("crime", "harm", "land", "frail", "age")                    # normalised over the living people
WORLD_FACTS = ("weak", "repress")                                         # read against the realm's refs
_FI = {f: i for i, f in enumerate(IMP_FACTS)}
_LIFE = np.array([_FI[f] for f in LIFE_FACTS]); _WORLD = np.array([_FI[f] for f in WORLD_FACTS])
IMP_WORLD_DEFAULT = dict(norm="country")   # imp_world_par: "country" (every living person) or "town" (each town's own)


def realm(name="earth"):
    """The realm module a run reads its world-fit constants from (P["realm"]: "earth", or "neutral", the test world)."""
    if name in (None, "earth"):
        import realm_earth as R
    elif name == "neutral":
        import realm_neutral as R
    else:
        raise ValueError(f"realm {name!r}: 'earth' or 'neutral'")
    return R


def imp_causes(R):
    """The cause words nw_imp_cause indexes with imp_world on: the realm's IMP_CAUSES (head 6's, 0 to 13), then one per
    IMP_FACTS (in the realm's IMP_CAUSE words, templates unfilled), then the betrayal's own word for weak law."""
    return tuple(R.IMP_CAUSES) + tuple(R.IMP_CAUSE.get(f, f) for f in IMP_FACTS) + (R.IMP_CAUSE_BETRAY_WEAK,)


def imp_elasticities(R, nI):
    """IMP_WORLD as an array (kinds x IMP_FACTS); None when the catalogue's setbacks are not the realm's (another count)."""
    if len(R.IMP_WORLD) != nI:
        return None
    E = np.zeros((nI, len(IMP_FACTS)))
    for k, d in enumerate(R.IMP_WORLD):
        for f, e in d.items():
            E[k, _FI[f]] = float(e)
    return E


def _age_x(R, a):
    x = np.ones(np.shape(a))
    for a0, m in R.IMP_AGE_X:
        x = np.where(a >= a0, float(m), x)
    return x


def harm_loc(W):
    """Each locality's harm (1 struck by a disaster this week or recovering from one, else 0), and the war (0 or 1)."""
    h = ((np.asarray(W.loc_disaster) > 0) | (np.asarray(W.disaster_now) > 0)).astype(float)
    return h, float(int(getattr(W, "war", 0)) > 0)


def imp_key(W, PP, year):
    """What g is computed from that can change within a year: the year, the war, the struck towns, the lives' homes."""
    h, w = harm_loc(W)
    return (int(year), w, h.tobytes(), np.asarray(PP.loc).tobytes())


def _log_facts(R, W, loc, frail, age, land, hl, war):
    """log factor of each IMP_FACTS for people at localities loc (frailty 1 - health, age in years, land 0/1)."""
    ref = R.IMP_WORLD_REF; nl = len(np.asarray(W.loc_crime))
    ok = (loc >= 0) & (loc < nl); l_ = np.where(ok, loc, 0)
    X = np.zeros((len(loc), len(IMP_FACTS)))
    X[:, _FI["crime"]] = np.where(ok, np.log(np.maximum(np.asarray(W.loc_crime, float)[l_], 1e-6) / ref["crime"]), 0.0)
    harm = np.maximum(np.where(ok, hl[l_], 0.0), war)
    X[:, _FI["harm"]] = np.log1p(R.IMP_HARM_K * harm)
    X[:, _FI["land"]] = np.log(R.IMP_LAND_X) * np.asarray(land, float)
    X[:, _FI["frail"]] = np.log(np.maximum(frail, 1e-3) / ref["frail"])
    X[:, _FI["age"]] = np.log(_age_x(R, age))
    X[:, _FI["weak"]] = np.log(max(1.0 - float(W.law_rule), 1e-3) / ref["weak"])
    X[:, _FI["repress"]] = np.log(max(1.0 - float(np.mean(W.rights)), 1e-3) / ref["repress"])
    return X


def imp_g(R, E, W, PP, hea, age, dead, par=None, land=None, out=None):
    """g (lives x kinds) and the lives' log facts X (lives x IMP_FACTS, for the cause). hea: the lives' health; age: their
    age (the lives are one cohort); dead: theirs; land: None, or each life's 'a loved stretch lost' (wa_land)."""
    par = dict(IMP_WORLD_DEFAULT, **(par or {}))
    lo, hi = R.IMP_WORLD_CLIP; N = len(hea); t_w = int(W.t)
    hl, war = harm_loc(W)
    land_c = np.zeros(N) if land is None else np.asarray(land, float)
    Xc = _log_facts(R, W, np.asarray(PP.loc), 1.0 - np.asarray(hea, float), np.full(N, float(age)), land_c, hl, war)
    m = PP.used & PP.lv & (PP.born <= t_w)                                 # the casts' living people
    ml = np.asarray(PP.mloc)[m].astype(np.int64)
    Xk = _log_facts(R, W, ml, 1.0 - PP.health[m].astype(float), (t_w - PP.born[m]) / 52.0, np.zeros(len(ml)), hl, war)
    El = E[:, _LIFE]; Ew = E[:, _WORLD]
    gl_c = np.clip(np.exp(Xc[:, _LIFE] @ El.T), lo, hi)                    # lives x kinds, the life part
    gl_k = np.clip(np.exp(Xk[:, _LIFE] @ El.T), lo, hi)
    al = ~np.asarray(dead, bool)
    if par["norm"] == "town":
        nl = len(np.asarray(W.loc_crime)); lc = np.clip(np.asarray(PP.loc), 0, nl - 1); lk = np.clip(ml, 0, nl - 1)
        s = np.zeros((nl, E.shape[0])); c = np.zeros(nl)
        np.add.at(s, lc[al], gl_c[al]); np.add.at(c, lc[al], 1.0); np.add.at(s, lk, gl_k); np.add.at(c, lk, 1.0)
        mt = np.where(c[:, None] > 0, s / np.maximum(c, 1)[:, None], 1.0); mu_c, mu_k = mt[lc], mt[lk]
    else:
        mu_c = mu_k = ((gl_c[al].sum(0) + gl_k.sum(0)) / max(int(al.sum()) + len(gl_k), 1))[None]
    gw = np.exp(Xc[0, _WORLD] @ Ew.T) if N else np.ones(E.shape[0])      # kinds, the world part
    g = np.clip(gl_c / np.maximum(mu_c, 1e-12) * gw[None], lo, hi)
    g[:, ~(E != 0).any(1)] = 1.0                                           # a kind that follows nothing: exactly v24's
    if out is not None:   # for the checks: the life part over every living person, normalised (its mean per kind is 1)
        out["pop"] = np.concatenate([(gl_c / np.maximum(mu_c, 1e-12))[al], gl_k / np.maximum(mu_k, 1e-12)])
        out["world"] = gw
    return g, Xc


def imp_fact(E, X, ii, k):
    """The fact that weighed most toward each drawn setback (IMP_FACTS index, -1 none): the largest positive e x ln(fact /
    ref) of the kind's facts (a fact below its ref made the setback less likely, so it is never named)."""
    T = E[k] * X[ii]
    j = T.argmax(1)
    return np.where(T[np.arange(len(ii)), j] > 1e-9, j, -1)


def imp_words(R, k, f, W, loc, kinds):
    """The panel's words for setback k's fact f (IMP_FACTS index) at locality loc; kinds: each town's last disaster
    kind (HAZARDS index, -1 none)."""
    if f < 0:
        return None
    nm = IMP_FACTS[f]
    if nm == "weak" and k == 1:
        return R.IMP_CAUSE_BETRAY_WEAK
    w = R.IMP_CAUSE.get(nm, nm)
    if "{disaster_kind}" in w:
        from world_base import HAZARDS
        dk = int(kinds[loc]) if 0 <= loc < len(kinds) else -1
        w = w.replace("{disaster_kind}", HAZARDS[dk] if dk >= 0 else "disaster")
    return w.replace("{stretch}", "the stretch you love")


# ---------------------------------------------------------------------------------------------- what a world rewards
def tilt_tables(R, perm):
    """The realm's tilt in the world's colour frame (perm): the formal layer per sphere (9 x 5) and its law ref, and,
    when the realm states profiles (contracts.md section 8), the map DC (dims x 5) and each kind's incentives as
    (mean - .5, sd) per dimension; DC None when the realm has none (then r = mix / .2, plus any layer)."""
    from sphere_data import SPHERES
    perm = np.asarray(perm, np.int64)
    lay = np.asarray(getattr(R, "TILT_LAYER", (0.0,) * C), float)[perm]
    formal = np.array([s in getattr(R, "TILT_FORMAL", ()) for s in SPHERES], float)
    T = dict(layer=formal[:, None] * lay[None], law_ref=float(getattr(R, "TILT_LAW_REF", 0.73)),
             mix_k=float(getattr(R, "MIX_K", 1.0)), mix_even=bool(getattr(R, "SPH_MIX_EVEN", False)),
             k=float(getattr(R, "PROFILE_K", 0.0)), clip=tuple(getattr(R, "PROFILE_CLIP", (0.5, 2.0))), DC=None)
    dims = getattr(R, "PROFILE_DIMS", None); prof = getattr(R, "PROFILES", None); dc = getattr(R, "DIM_COLOURS", None)
    if not dims or not prof or not dc:
        return T
    inc = lambda e: (np.array([e["incentives"][d][0] for d in dims], float) - 0.5,
                     np.array([e["incentives"][d][1] for d in dims], float))
    T["DC"] = np.array([[float(dc[d][c]) for c in "WUBRG"] for d in dims])[:, perm]
    T["place"] = {nm: inc(e) for nm, e in prof.get("place", {}).items()}
    T["community"] = {nm: inc(e) for nm, e in prof.get("community", {}).items()}
    bd = prof.get("institution", {})
    T["body"] = inc(next(iter(bd.values()))) if bd else None
    T["period"] = {nm: inc(e) for nm, e in prof.get("period", {}).items()}
    T["groups"] = dict(getattr(R, "COMMUNITY_GROUPS", {}))
    return T


def _mix(W, T):
    """The towns' sphere mixes as the tilt reads them: the world's, or .2 a colour in a realm that reads them even
    (realm_neutral: r = 1 everywhere, always, whatever its burn-in does)."""
    s = np.asarray(W.sph_s, float)
    return np.full_like(s, 0.2) if T.get("mix_even") else s


def _mixr(sph, T):
    """The sphere mix's part of r: 1 + MIX_K x (mix / .2 - 1) (MIX_K 1: mix / .2)."""
    return 1.0 + T["mix_k"] * (sph / 0.2 - 1.0)


def tilt_r(x, T, clip=None):
    """r from x = (1 + MIX_K x (mix / .2 - 1)) x (1 + k x dev . DC) + layer x law: each cell held to the clip and each sphere renormalised to a
    mean of 1 (repeated until both hold), so a mix that drifts far stays a tendency, never a wall."""
    lo, hi = clip or T["clip"]
    r = np.asarray(x, float)
    for _ in range(64):
        r = np.clip(r, lo, hi); m = r.mean(-1, keepdims=True); r = r / m
        if np.abs(m - 1).max() < 1e-13:
            break
    return r


def _draw(seed, key, mean_sd):
    """A deviation per dimension, mean + sd x a normal draw from a stream seeded by the world's seed and key."""
    m, sd = mean_sd
    if not sd.any():
        return m.copy()
    return m + sd * np.random.default_rng([int(seed)] + [int(k) & 0x7FFFFFFF for k in key]).standard_normal(len(m))


def tilt_town(W, T, cache, sph=None, law=None):
    """Each town's r (towns x 9 x 5) and its incentives' deviation (towns x dims): its place kind's draw (seeded by the
    world's seed and the town) and the epoch's (modern: the reference, 0). T: tilt_tables; cache: a dict kept per run."""
    from world_base import LOC_KINDS
    sph = _mix(W, T) if sph is None else sph; nl = sph.shape[0]
    law = T["layer"][None] * (float(W.law_rule) / T["law_ref"]) if law is None else law
    if T["DC"] is None:
        return tilt_r(_mixr(sph, T) + law, T), None
    D = T["DC"].shape[0]; z_ = (np.zeros(D), np.zeros(D))
    per = T["period"].get(W._sph_tables()["ep"], z_)
    if "town" not in cache:
        cache["town"] = np.array([_draw(int(getattr(W, "_seed", 0)), (7717, l),
                                        T["place"].get(LOC_KINDS[int(W.loc_kind[l])], z_)) for l in range(nl)])
    xt = cache["town"] + per[0]
    return tilt_r(_mixr(sph, T) * (1 + T["k"] * (xt @ T["DC"]))[:, None, :] + law, T), xt


def tilt_year(PP, here, age):
    """Once a year, at the rungs (world_people_settings._sph_hours): r for each town and life, and each life's gain per
    sphere, its pie's fit to r over the mean of that over the town's people (its living casts there, and the lives
    present in the sphere), so the tilt moves standing between colours and adds none. Lists the cells that moved .02 or
    more since last listed (PP.tilt_moves). Returns the gain (N x 9) that multiplies a year present."""
    from world_people_base import G as GK
    from world_keys import GROUP_KINDS
    W = PP.W; N = PP.N; nl = W.sph_s.shape[0]
    T = getattr(PP, "_tilt_T", None)
    if T is None:
        T = PP._tilt_T = tilt_tables(PP.tilt_R, getattr(W, "perm", np.arange(C))); PP._tilt_dev = {}
        PP.tilt_moves = [[] for _ in range(N)]; PP.tilt_listed = None; PP.tilt_ver = 0
    seed = int(getattr(W, "_seed", 0)); cache = PP._tilt_dev
    law = T["layer"][None] * (float(W.law_rule) / T["law_ref"])           # 1 x 9 x 5
    loc = np.clip(np.asarray(PP.loc), 0, nl - 1)
    if T["DC"] is None:
        r_town = tilt_r(_mixr(_mix(W, T), T) + law, T); r_n = r_town[loc]
    else:
        D = T["DC"].shape[0]
        r_town, xt = tilt_town(W, T, cache, None, law)
        # a life's own settings in each sphere: the body's draw (an institution's by its id) and its community's
        xs = np.zeros((N, 9, D)); ns = np.zeros((N, 9))
        ss = PP.set_sphere; act = (PP.skind >= 0) & (ss >= 0) & ~np.asarray(PP.dead)[:, None]
        inst_k = {GK[g_] for g_ in ("work", "class", "unit", "ward") if g_ in GK}
        for n_, j_ in zip(*np.nonzero(act)):
            g_ = int(PP.skind[n_, j_]); ref_ = int(PP.sref[n_, j_])
            key_ = (7718, g_, ref_) if (ref_ >= 0 and g_ in inst_k) else \
                (7719, g_, ref_, int(PP.loc[n_])) if ref_ >= 0 else (7719, g_, int(PP.run_seed), int(n_), int(j_), int(PP.sjoin[n_, j_]))
            dv_ = cache.get(key_)
            if dv_ is None:
                dv_ = _draw(seed, key_, T["body"]) if T["body"] is not None else np.zeros(D)
                cm_ = T["groups"].get(GROUP_KINDS[g_])
                if cm_ in T["community"]:
                    dv_ = dv_ + _draw(seed, key_ + (7720,), T["community"][cm_])
                cache[key_] = dv_
            xs[n_, ss[n_, j_]] += dv_; ns[n_, ss[n_, j_]] += 1
        xp = xt[loc][:, None, :] + xs / np.maximum(ns, 1)[..., None]        # N x 9 x dims
        r_n = tilt_r(_mixr(_mix(W, T)[loc], T) * (1 + T["k"] * (xp @ T["DC"])) + law, T)
    # the gain: the pie's fit to r over the mean fit of the town's people in the sphere (the casts living there, the lives present)
    p_ = np.asarray(PP.w, float); p_ = p_ / np.maximum(p_.sum(1, keepdims=True), 1e-12)
    val = np.einsum("nc,nsc->ns", p_, r_n)
    t_w = int(W.t); m_ = PP.used & PP.lv & ((t_w - PP.born) >= 15 * 52)
    ml_ = np.asarray(PP.mloc)[m_].astype(np.int64); ok_ = (ml_ >= 0) & (ml_ < nl)
    pk_ = PP.pie[m_][ok_].astype(float); pk_ /= np.maximum(pk_.sum(1, keepdims=True), 1e-12)
    sp_ = np.zeros((nl, C)); np.add.at(sp_, ml_[ok_], pk_); cnt = np.bincount(ml_[ok_], minlength=nl).astype(float)
    tot = np.einsum("lc,lsc->ls", sp_, r_town); cnt = np.repeat(cnt[:, None], 9, 1)
    hl_ = here & ~np.asarray(PP.dead)[:, None]
    np.add.at(tot, loc, np.where(hl_, val, 0.0)); np.add.at(cnt, loc, hl_.astype(float))
    gain = val / np.maximum(np.where(cnt > 0, tot / np.maximum(cnt, 1), 1.0), 1e-9)[loc]
    # what the game reads: r in each life's town now, and the cells that moved .02 or more since last listed
    if PP.tilt_listed is not None:
        big = np.abs(r_n - PP.tilt_listed) >= 0.02
        big &= ~np.asarray(PP.dead)[:, None, None]
        if big.any():
            from sphere_data import SPHERES
            moved_home = loc != PP.tilt_lloc
            dt_ = r_town[loc] - PP.tilt_ltown
            for n_, s_, c_ in zip(*np.nonzero(big)):
                d_ = float(r_n[n_, s_, c_] - PP.tilt_listed[n_, s_, c_])
                cause = "a new town" if moved_home[n_] else ("the town's ways" if abs(dt_[n_, s_, c_]) >= 0.5 * abs(d_)
                                                             else "their places")
                PP.tilt_moves[n_].append(dict(sphere=SPHERES[s_], colour="WUBRG"[int(c_)],
                                              age=int(age), by=round(d_, 3), to=round(float(r_n[n_, s_, c_]), 3), cause=cause))
            PP.tilt_listed[big] = r_n[big]; PP.tilt_ltown[big] = r_town[loc][big]
        PP.tilt_lloc = loc.copy()
    else:
        PP.tilt_listed = r_n.copy(); PP.tilt_ltown = r_town[loc].copy(); PP.tilt_lloc = loc.copy()
    PP.tilt_r = r_n; PP.tilt_town = r_town; PP.tilt_gain = gain; PP.tilt_ver += 1
    return gain


def prizes(PP):
    """S["prizes"]: per life {sphere: [W, U, B, R, G]}, r in their town (and their places) as last computed; 1 even."""
    from sphere_data import SPHERES
    r = PP.tilt_r
    return [{s_: [round(float(x), 3) for x in r[n, j]] for j, s_ in enumerate(SPHERES)} for n in range(len(r))]
