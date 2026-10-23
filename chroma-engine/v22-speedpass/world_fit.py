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


def imp_g(R, E, W, PP, hea, age, dead, par=None, land=None):
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
        mu = np.where(c[:, None] > 0, s / np.maximum(c, 1)[:, None], 1.0)[lc]
    else:
        mu = ((gl_c[al].sum(0) + gl_k.sum(0)) / max(int(al.sum()) + len(gl_k), 1))[None]
    gw = np.exp(Xc[0, _WORLD] @ Ew.T) if N else np.ones(E.shape[0])      # kinds, the world part
    g = np.clip(gl_c / np.maximum(mu, 1e-12) * gw[None], lo, hi)
    g[:, ~(E != 0).any(1)] = 1.0                                           # a kind that follows nothing: exactly v24's
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
