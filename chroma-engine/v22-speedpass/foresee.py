"""v7 foreseen outcome of a plan, for the game.

Emren (2026-10-04 21:39, 2026-10-05 04:57): the player can decide long plans and the game shows the foreseen odds; it
shows the character's felt odds, and reality only as a rough hint.

All functions work on S, the dict of run_steps' locals at a pause (chroma-game link.py yields it), and n, the person.

    from foresee import preview, add_plan, foresee, drop_plan, plans
    preview(S, n, "five years", domain="career")      # what the character feels before deciding (changes nothing)
    j, f = add_plan(S, n, "year", mix="U R")          # the player's plan: a pursuit in these ways, or a domain
    foresee(S, n, j)                                  # felt odds now, and a rough hint of how such plans go
    drop_plan(S, n, j)                                # the player lets it go (costs what was put in)

The hint is not the engine's true chance for this one life (no one can know it): it is how plans like this one, held
with these felt odds by people with this much self-control, free time and stress and this fit with who they are, turned
out in simulated lives (HINT, measured by calib_v7/foresee_table.py), told as a band of words.
"""
import numpy as np

import engine as E

BANDS = [(0.15, "rarely"), (0.35, "now and then"), (0.6, "about half the time"), (0.8, "more often than not"), (1.01, "usually")]

# logistic model of "reached in time" per horizon: intercept, logit(felt), self-control, free time, stress, fit, domain plan.
# Measured on simulated lives (calib_v7/foresee_table.py); refresh when the goal defaults change.
# Measured 2026-10-07 on 400 Earth lives with the world on (as the game plays), release engine and batch
# (calib_v10/cx2/foresee_on.out); Brier of the hint under the felt odds' in each horizon: year .077 vs .237,
# five years .129 vs .236, life .023 vs .078.
HINT = {
    'week': [0.0, 1.0, 0, 0, 0, 0, 0],
    'year': [-14.017, 1.636, 12.112, 5.467, 0.211, 2.863, 0.0],
    'five years': [-5.431, 0.61, 4.277, 1.793, 0.116, 1.302, 0.44],
    'life': [0.324, 2.349, 6.035, 4.051, 0.113, -3.327, 0.0],
}


def band(p):
    for hi, word in BANDS:
        if p < hi:
            return word
    return BANDS[-1][1]


def _logit(p):
    p = np.clip(p, 0.01, 0.99)
    return float(np.log(p / (1 - p)))


def hint(horizon, felt, self_control, free_time, stress, fit, domain):
    """How plans like this turned out in simulated lives: a rate, and its band in words."""
    b = HINT[horizon]
    x = [1.0, _logit(felt), self_control, free_time, stress, fit, float(domain)]
    p = 1 / (1 + np.exp(-float(np.dot(b, x))))
    return p, band(p)


def _mix(S, n, mix):
    if mix is None:
        m = np.asarray(S["w"][n], float).copy()
    elif isinstance(mix, str):
        m = E.parse(mix)
    else:
        m = np.asarray(mix, float)
    return m / max(m.sum(), 1e-9)


def _fit(S, n, mix):
    """Self-concordance (Sheldon & Elliot 1999): how well a plan's ways fit who the person is and wants to be."""
    og = 0.5 * (S["w"][n] + E.softmax(S["y"][n]))
    return float(np.clip(2 * (mix * og).sum() / og.max() - 1, -0.5, 1))


def _context(S, n):
    return float(S["ctrl"][n]), float(S["res"][n, E.RIDX["time"]]), float(S["stress"][n])


def _horizon(h):
    return E.HORIZONS.index(h) if isinstance(h, str) else int(h)


def _domain(d):
    if d is None or d == "a pursuit":
        return -1
    return E.KNAMES.index(d) if isinstance(d, str) else int(d)


def _what(S, n, felt, hz, dom, mix, weeks):
    ct, ft, st = _context(S, n)
    fit = _fit(S, n, mix)
    p, word = hint(E.HORIZONS[hz], felt, ct, ft, st, fit, dom >= 0)
    t = S["t"]
    return dict(felt=round(felt, 2), hint=word, hint_rate=round(float(p), 2), horizon=E.HORIZONS[hz],
                domain=E.KNAMES[dom] if dom >= 0 else "a pursuit", colors=dict(zip(E.COLORS, mix.round(2).tolist())),
                fit=round(fit, 2), due_age=round((t + weeks) / 52, 1),
                left_out=[nm for nm, bad in (("busy weeks", ft < 0.35), ("stress", st > 0.6), ("little self-control", ct < 0.4),
                                             ("a poor fit with who they are", fit < 0.1)) if bad])


def preview(S, n, horizon="year", domain=None, mix=None, strength=0.6):
    """What the character would feel about a plan before it is made (changes nothing)."""
    hz, dom, m = _horizon(horizon), _domain(domain), _mix(S, n, mix)
    _, _, weeks, felt = S["plan_odds"](n, m, dom, hz, strength)
    return _what(S, n, felt, hz, dom, m, weeks)


def add_plan(S, n, horizon="year", domain=None, mix=None, strength=0.6):
    """The player's plan. The character holds it (it does not fade from a poor fit, and they do not let it go on their
    own); it pulls on what they do as their own plans do. When their plans are full, their weakest own plan is pushed
    aside. Returns (slot, foresee) or (-1, reason)."""
    hz, dom, m = _horizon(horizon), _domain(domain), _mix(S, n, mix)
    gk, gs, gby = S["gk"], S["gs"], S["gby"]
    if dom >= 0 and S["held"][n, dom]:
        return -1, f"already holds a {E.KNAMES[dom]}"
    mine = np.nonzero(gk[n] == 2)[0]
    if len(mine) >= S["P"]["max_plans"]:
        own = [j for j in mine if not gby[n, j]]
        if not own:
            return -1, "the character already holds as many plans as they can"
        S["end_goal"](n, min(own, key=lambda j: gs[n, j]), "pushed aside")
    j = S["new_goal"](n, 2, m, dom, E.GSRC["player"], hz=hz, by=1, s0=strength)
    if j < 0:
        return -1, "no room for another goal"
    return j, foresee(S, n, j)


def foresee(S, n, j):
    """A plan's felt odds now (they change as the character learns how often chances come and how steps go), its odds
    at the start, progress, and the rough hint of reality."""
    if S["gk"][n, j] != 2:
        return None
    hz, dom = int(S["ghz"][n, j]), int(S["gd"][n, j])
    out = _what(S, n, float(S["gfelt"][n, j]), hz, dom, S["gm"][n, j], int(S["gh"][n, j] - S["t"]))
    out.update(felt_at_start=round(float(S["gfelt0"][n, j]), 2), progress=round(float(S["gp"][n, j]), 2),
               by_player=bool(S["gby"][n, j]), source=E.G_SOURCES[S["gsrc"][n, j]])
    return out


def plans(S, n):
    """Every plan the person holds now, the player's and their own: [(slot, foresee)]."""
    return [(int(j), foresee(S, n, j)) for j in np.nonzero(S["gk"][n] == 2)[0]]


def drop_plan(S, n, j):
    """The player lets a plan go: it costs what was put in, less for a person who has learned to let go."""
    if S["gk"][n, j] != 2:
        return False
    fa = np.clip((S["tries"][n] - S["wins"][n] + S["blocked"][n] - S["P"]["flex_exp"][0]) / S["P"]["flex_exp"][1], 0, 1)
    S["quit_"](n, j, "let go", 0.3 + 0.7 * fa)
    return True


# Hover arrows (WS1, "because of you, and meanwhile"; chroma-ideas/next-table-2026-10-19/plan.md section 1): before a
# pick, what each option would move if it works and if it does not, as arrows in three sizes (1 a little, 2 clearly, 3 a
# lot), never as numbers. Needs follow the engine's own weekly rules for the act (its ends met or drained, acting as
# oneself, succeeding at what was hard, at the character's felt odds); means and people the Library's costs, wins and
# losses (ties are people); titles the act's own fields and the commitment it may start. SIZES: the smallest move of
# each size, in each kind's units (a need's share of one; a means' share of one; a chance for a commitment to start).
SIZES = dict(need=(0.003, 0.01, 0.03), means=(0.02, 0.06, 0.15), people=(0.02, 0.06, 0.15), start=(0.1, 0.3, 0.6))
SIZE_WORDS = {1: "a little", 2: "clearly", 3: "a lot"}
PEOPLE_KINDS = ("partner", "children", "community")   # a commitment to people; the others (career, faith) are titles


def _size(kind, v):
    lo = SIZES[kind]
    return sum(abs(v) >= x for x in lo)


def _arrow(kind, name, v, size=None):
    sz = _size(kind if kind != "title" else "start", v) if size is None else size
    return dict(kind=kind, name=name, dir="up" if v > 0 else "down", size=int(sz), word=SIZE_WORDS[int(sz)],
                v=round(float(v), 4)) if sz else None


def arrows(S, n):
    """At the "choose" pause: for each option open to person n (seen or unnoticed, not "do nothing"), the arrows of what
    it would move if it works ("win") and if it does not ("fail"): [dict(k, win=[...], fail=[...])], each arrow
    dict(kind (need, means, people or title), name, dir (up or down), size (1 to 3), word, v). v is the engine's own
    estimate, for tests and the game's hidden layer only: the hover shows the arrow and its word, never the number.
    Read-only."""
    P = S["P"]; L = S["L"]; s = int(S["s"][n]); K = S["e"].shape[1]
    NIDX = {nm: j for j, nm in enumerate(E.NEEDS)}
    need = np.asarray(S["need"][n], float)
    room = (1 - need) if P["satiate"] else np.ones(len(need))
    NMAP_ = E.NMAP_V7 if P.get("need_tab") == "v7" else E.NMAP
    T = np.asarray(S["NMP"][n], float) if S.get("NM_ON") else NMAP_
    st = max(float(S["stakes"][n]), P["need_floor"])
    og = 0.5 * (np.asarray(S["w"][n], float) + E.softmax(S["y"][n]))
    GR = L.get("ROLES") if S.get("RON") else None
    TIE = E.RIDX["ties"]
    out = []
    for k in range(K):
        if not S["mask"][n, k] or S["do_nothing"][n, k]:
            continue
        e = np.asarray(S["e"][n, k], float); e0 = np.asarray(S["e0"][n, k], float)
        ma = np.asarray(S["m"][n, k], float); p = float(S["p_hat"][n, k])
        both = 0.06 * (T @ np.minimum(e0, 0))                       # acting against a value's ends drains, worked or not
        win = both + 0.12 * st * (T @ np.maximum(e, 0)) * room       # ends met when it works
        fail = both.copy()
        if P["aut_self"]:   # acting as oneself meets autonomy, worked or not; succeeding at what was hard meets competence
            cc = float(np.clip(2 * (ma * og).sum() / og.max() - 1, -0.5, 1))
            a_ = P["aut_act"] * cc * (room[NIDX["autonomy"]] if cc > 0 and P["satiate"] else 1)
            win[NIDX["autonomy"]] += a_; fail[NIDX["autonomy"]] += a_
            win[NIDX["competence"]] += P["comp_act"] * (0.5 + (1 - p)) * (room[NIDX["competence"]] if P["satiate"] else 1)
            fail[NIDX["competence"]] -= P["comp_act"] * 0.3
        if S.get("CU_ON"):   # learning in Blue's ways, worked or not
            ln_ = ma[1] * (1 - float(S["sig"][n, 1]))
            win[NIDX["meaning"]] += P["cu_learn"] * ln_; win[NIDX["autonomy"]] += 0.5 * P["cu_learn"] * ln_
            fail[NIDX["meaning"]] += P["cu_learn"] * ln_; fail[NIDX["autonomy"]] += 0.5 * P["cu_learn"] * ln_
        rm_ = room[NIDX["meaning"]] if P["satiate"] else 1
        duty_ = np.minimum(1, (np.asarray(S["held"][n], float) * np.asarray(S["I"][n], float)) @ E.DUTY)
        win[NIDX["meaning"]] += P["duty_mean"] * float(((np.maximum(e, 0) @ NMAP_.T) * duty_).sum()) * rm_   # serving those
        # one answers for; holding colours the world reads as opposed, when it works
        if P["ten_good"] and S.get("FRpos") is not None and S.get("J") is not None:
            FRp = np.asarray(S["FRpos"], float); wn_ = np.asarray(S["w"][n], float)
            span = float(ma @ FRp @ ma) * (1 + 4 * float(wn_ @ (FRp * (1 - np.asarray(S["J"][n], float))) @ wn_))
            win[NIDX["meaning"]] += P["ten_good"] * span * rm_
        cl_ = S["closed_s"][n, k] if S.get("closed_s") is not None else -1
        if cl_ == 1:   # an option others frown on backfires on belonging when it fails
            bk_ = min(float(S["clu_"][n, k]), 1.0) if S.get("CLU_ON") and S.get("clu_") is not None else 1.0
            fail[NIDX["belonging"]] -= 0.1 * bk_
        pay = np.asarray(L["PAY"][s, k], float) if "PAY" in L else np.zeros(len(E.RESOURCES))
        rw = pay + (np.asarray(L["WIN"][s, k], float) if "WIN" in L else 0)
        rl = pay + (np.asarray(L["LOSE"][s, k], float) if "LOSE" in L else 0)
        side = dict(win=[], fail=[])
        for nm_, nv_, rv_ in (("win", win, rw), ("fail", fail, rl)):
            ar_ = [_arrow("need", E.NEEDS[j], nv_[j]) for j in np.argsort(-np.abs(nv_))]
            ar_ += [_arrow("people" if j == TIE else "means", E.RESOURCES[j], rv_[j]) for j in np.argsort(-np.abs(rv_))]
            side[nm_] = [a for a in ar_ if a]
        kk = int(L["COMMIT"][s, k]) if "COMMIT" in L else -1
        if kk >= 0 and not S["held"][n, kk]:   # the commitment it may start, when it works
            a_ = _arrow("people" if E.KNAMES[kk] in PEOPLE_KINDS else "title", E.KNAMES[kk], float(P["commit_p"][kk]),
                        size=_size("start", float(P["commit_p"][kk])))
            if a_:
                side["win"].append(a_)
        if GR is not None and GR["A_HASFX"][s, k]:   # the act's own titles and perks, gained or given up
            for nm_ in ("win", "fail"):
                for op_, j_, _ in GR["A_FX"][(s, k)]["ok" if nm_ == "win" else "fail"]:
                    if j_ == -2:
                        j_ = _title_held(S, n, s)
                    if j_ < 0 or j_ >= len(GR["names"]):
                        continue
                    has_ = bool(S["r_has"][n, j_])
                    if op_ in ("title", "grants") and not has_:
                        side[nm_].append(dict(kind="title", name=GR["names"][j_], dir="up", size=3 if j_ < GR["NT"] else 2,
                                              word=SIZE_WORDS[3 if j_ < GR["NT"] else 2], v=1.0))
                    elif op_ in ("drops", "takes", "suspends") and has_:
                        side[nm_].append(dict(kind="title", name=GR["names"][j_], dir="down", size=3 if j_ < GR["NT"] else 2,
                                              word=SIZE_WORDS[3 if j_ < GR["NT"] else 2], v=-1.0))
        out.append(dict(k=k, **side))
    return out


def _title_held(S, n, s):
    import explain
    return explain.title_held_index(S, n, s)


# Aims v1 (chroma-ideas/next-table-2026-10-19/plan.md section 5; aims on, with the batch's aims): the aims track for the
# sheet and the HUD (where they stand, the next step, what helps), the aims the character already feels, and the
# player's setting or dropping of an aim. None of these changes a life but set_aim and drop_aim.
def aims(S, n):
    """The aims person n holds: [dict(slot, aim, face, domain, own ("set by you" until a spark makes it theirs),
    by_player, strength, calling, steps=[dict(say, height, reached)], reached, next (the next step's say), helps (the
    next step's titles and perks))]; [] with aims off."""
    if not S.get("AIM_ON"):
        return []
    A, ak = S["AIM"], S["ak"]
    out = []
    for q in np.nonzero(ak[n] >= 0)[0]:
        x = A["aims"][int(ak[n, q])]; k = int(S["astep"][n, q])
        st = [dict(say=s_["say"], height=E.AIM_HEIGHTS[s_["h"] - 1] if s_["h"] else None, reached=i < k)
              for i, s_ in enumerate(x["steps"])]
        nx = x["steps"][k] if k < len(x["steps"]) else None
        out.append(dict(slot=int(q), aim=x["name"], face="".join(E.COLORS[c] for c in np.nonzero(x["face"])[0]),
                        domain=E.KNAMES[x["dom"]] if x["dom"] >= 0 else "a pursuit", own=bool(S["aown"][n, q]),
                        by_player=bool(S["aby"][n, q]), strength=round(float(S["astr"][n, q]), 2),
                        calling=bool(S["acall"][n, q]), steps=st, reached=k, next=nx["say"] if nx else None,
                        helps=list(nx["names"]) if nx is not None else [],
                        below=x["below"]))
    return out


def aim_choices(S, n, k=6):
    """The aims person n already feels (the aims their dreams, passions and plans read as, held or not) and then the
    nearest to who they are now (their colours), k in all, held ones left out: [dict(aim, face, domain, felt, fit)]."""
    if not S.get("AIM_ON"):
        return []
    A, ak = S["AIM"], S["ak"]
    held = set(int(a) for a in ak[n] if a >= 0)
    felt = [int(a) for j, a in enumerate(S["gal"][n]) if a >= 0 and S["gk"][n, j] >= 0 and int(a) not in held]
    fit = S["aim_fit"](np.asarray(S["w"][n], float))
    rest = [int(a) for a in np.argsort(-fit) if int(a) not in held and int(a) not in felt]
    pick = list(dict.fromkeys(felt))[:k]
    pick += rest[:max(0, k - len(pick))]
    return [dict(aim=A["aims"][a]["name"], face="".join(E.COLORS[c] for c in np.nonzero(A["aims"][a]["face"])[0]),
                 domain=E.KNAMES[A["aims"][a]["dom"]] if A["aims"][a]["dom"] >= 0 else "a pursuit", felt=a in felt,
                 fit=round(float(fit[a]), 2)) for a in pick]


def set_aim(S, n, aim):
    """The player sets an aim (its name): held as "set by you" until a try at its spark moment works (and a rite, or
    the moment's own seal, makes it theirs); until then it pulls at aims_par reluctant and fades sooner. Returns the
    slot, or -1 with the reason."""
    if S.get("AIM2_ON"):   # aims v2: by field name; the new agenda, or an error in words
        return _set_aim2(S, n, aim)
    if not S.get("AIM_ON"):
        return -1, "aims are off"
    A = S["AIM"]
    if aim not in A["names"]:
        return -1, f"no aim {aim!r}"
    q = S["aim_take"](n, A["names"].index(aim), S["P"]["aims_par"]["set_s"], own=False, by=True, src="player")
    return (q, None) if q >= 0 else (-1, "no room for another aim")


def drop_aim(S, n, q):
    """The player lets aim slot q go."""
    if not S.get("AIM_ON") or S["ak"][n, q] < 0:
        return False
    S["aim_end"](n, int(q), "let go")
    return True


def aim_ways(S, n):
    """At the "choose" pause: which options are a way into the next step of an aim person n holds, {k: [dict(slot, aim,
    step (its say), height, if_fails)]}: the option gives (title or grants) one of that step's names when it works, or
    when it fails (if_fails). The moment itself may be a door to the step through another option; only the options
    that give it are named. Read-only; {} with aims off."""
    if not S.get("AIM_ON"):
        return {}
    L = S["L"]; GR = L["ROLES"]; A = S["AIM"]; s = int(S["s"][n]); K = S["e"].shape[1]
    nxt = []
    for q in np.nonzero(S["ak"][n] >= 0)[0]:
        x = A["aims"][int(S["ak"][n, q])]; k_ = int(S["astep"][n, q])
        if k_ < len(x["steps"]):
            nxt.append((int(q), x, x["steps"][k_]))
    out = {}
    for k in range(K):
        if not S["mask"][n, k] or S["do_nothing"][n, k] or (s, k) not in GR["A_FX"]:
            continue
        for when in ("ok", "fail"):
            gives = {j for op_, j, _ in GR["A_FX"][(s, k)][when] if op_ in ("title", "grants") and j >= 0}
            for q, x, st in nxt:
                if gives & set(int(j) for j in st["any"]):
                    out.setdefault(k, []).append(dict(slot=q, aim=x["name"], step=st["say"],
                                                      height=E.AIM_HEIGHTS[st["h"] - 1] if st["h"] else None,
                                                      if_fails=when == "fail"))
    return out


# Footprints (plan.md section 3): the marks stack shows a mark only when it nears a title or perk (Emren's condition,
# "2 of 3 toward ..."). marks_toward reads each title and perk rule's mark clauses (mk, mk_ok: one, within its years;
# mkn(m) >= k: k of them; mk_span: one) as units: have of need, for the ones the person does not hold yet where one of
# their marks counts. The rule's other parts (and an "or" around the marks) are not read: it is how near the marks are.
_MK_RULES = {}


def _mark_clauses(GR, gj, cf=False):
    import ast
    key_ = (id(GR), gj, cf)
    if key_ in _MK_RULES:
        return _MK_RULES[key_]
    out = []
    for i, r_ in enumerate(GR["rule"]):
        r_ = GR["rule_when"].get(i, r_) if gj else r_   # green_jobs: the newer rule in its place
        r_ = (GR.get("rule_fit") or {}).get(i, r_) if cf else r_   # cause_fit: the audit's tightened rule
        src_ = r_.get("req_s") or ""
        if "mk" not in src_:
            continue
        try:
            tree_ = ast.parse(src_, mode="eval")
        except SyntaxError:
            continue
        cl_, inner_ = [], set()
        for x in ast.walk(tree_):   # mkn(m) >= k (or > k): k of that mark
            if isinstance(x, ast.Compare) and len(x.ops) == 1 and isinstance(x.left, ast.Call) \
                    and getattr(x.left.func, "id", None) == "mkn" and isinstance(x.comparators[0], ast.Constant) \
                    and isinstance(x.ops[0], (ast.GtE, ast.Gt)) and x.left.args and isinstance(x.left.args[0], ast.Constant):
                k_ = int(x.comparators[0].value) + isinstance(x.ops[0], ast.Gt)
                cl_.append((x.left.args[0].value, "n", max(1, k_))); inner_.add(id(x.left))
        for x in ast.walk(tree_):
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) in ("mk", "mk_ok", "mkn", "mk_span") \
                    and id(x) not in inner_ and x.args and isinstance(x.args[0], ast.Constant):
                yrs_ = x.args[1].value if len(x.args) > 1 and isinstance(x.args[1], ast.Constant) else None
                cl_.append((x.args[0].value, "y", yrs_))
        if cl_:
            out.append((i, cl_))
    _MK_RULES[key_] = out
    return out


def marks_toward(S, n):
    """The titles and perks one of the person's marks counts toward, not held yet, nearest first: a list of
    dict(mark, title, say, kind ("title" or "perk"), have, need, done), mark the one of theirs left last; the ones still
    short first (fewest to go), then those whose marks are all there (done: the rule waits on something else, such as
    years in a career). [] without titles."""
    L = S["L"]
    GR = L.get("ROLES") if S.get("RON") else None
    if GR is None or S.get("mark_n") is None:
        return []
    MIDX_ = {m_: j_ for j_, m_ in enumerate(L["MARKS"])}
    mn_, ml_, t = S["mark_n"][n], S.get("mark_last"), S["t"]
    out = []
    for i, cl_ in _mark_clauses(GR, bool(S["P"].get("green_jobs")), bool(S["P"].get("cause_fit"))):
        if S["r_has"][n, i]:
            continue
        have_ = need_ = 0; last_ = (-1, None)
        for m_, how_, v_ in cl_:
            if m_ not in MIDX_:
                continue
            j_ = MIDX_[m_]; c_ = int(mn_[j_])
            if how_ == "n":
                need_ += v_; h_ = min(c_, v_)
            else:
                need_ += 1
                h_ = int(c_ > 0 and (v_ is None or ml_ is None or (t - ml_[n, j_]) <= v_ * 52 + 1e-9))
            have_ += h_
            if h_ and ml_ is not None and ml_[n, j_] > last_[0]:
                last_ = (int(ml_[n, j_]), m_)
            elif h_ and last_[1] is None:
                last_ = (last_[0], m_)
        if have_ and need_:
            out.append(dict(mark=last_[1], title=GR["names"][i], say=GR["say"][i],
                            kind="title" if i < GR["NT"] else "perk", have=have_, need=need_, done=have_ >= need_))
    out.sort(key=lambda d_: (d_["done"], d_["need"] - d_["have"], -d_["have"], d_["title"]))
    return out



# ---- aims v2 (aims_v2; v25 lane B, Emren's decision #9; contracts.md section 6 with Gamification's 10-23 shapes): the
# agenda, pace and priority, the agenda review and its application, the preview before a commitment. Views draw nothing
# and cost no time; set_pace, set_priority, apply_review and set_aim are the player's decisions (replayed from the
# inputs on load). Fork ids are ints; a fork answered "later" stays open, and only its aims wait.
GAME_PACE = ("holding", "pursuing", "reduced", "keeping_up", "paused", "set_aside")
OPT_SAY = dict(go_on="Go on", light="Go on, lightly", hard="Go on, hard", pause="Not now: pause it", drop="Let it go",
               pay="Pay and go on", refuse="Go on without paying", take="Take the chance", decline="Let the chance pass",
               round="Find a way round", keep="Keep everything as it is (slower)", light_last="Ease off the last in line",
               pause_last="Pause the last in line", later="Later")
BN_RES = {"time": "time", "money": "money", "a window": "window", "a fork": "fork", "a door": "access"}


def _game_state(AG, n, j):
    import aims2 as A2
    st = int(AG.st[n, j]); f = int(AG.f[n, j])
    if st == A2.ACTIVE:
        if AG.rung[n, j] >= AG.F["nr"][f]:
            return "keeping_up"
        return "reduced" if AG.inten[n, j] < 0.75 else "pursuing"
    return {A2.HELD: "holding", A2.PAUSED: "paused", A2.DROPPED: "set_aside"}[st]


def agenda(S, n):
    """The agenda (Gamification's shape): dict(items, capacity, forks, over, strained). Each item: slot, aim (the
    field's name), field, face, calling, by_player, importance, why_now, state (GAME_PACE), priority (1..n), step
    (i, of, say, next_say), progress (frac, effort_years, years), frac, lean (the character's own inclination, -1 to 1),
    pending (fork ids), bottleneck (dict(res, shared_with) or None), earned, potential, upkeep, and the engine's own
    item (S["aim2"]) under "engine". A view: draws nothing, costs no time."""
    if not S.get("AIM2_ON"):
        return dict(items=[], capacity={}, forks=[], over=False, strained=False, on=False)
    AG = S["AG"]; F = AG.F; n = int(n)
    occ = [int(j) for j in np.argsort(AG.pri[n], kind="stable") if AG.f[n, j] >= 0]
    rank = {j: i + 1 for i, j in enumerate(occ)}
    pend = {}
    for fk in AG.forks[n]:
        for j in fk["aims"]:
            pend.setdefault(j, []).append(fk)
    items = []
    for j in occ:
        it = AG.item(n, j); f = int(AG.f[n, j]); r = it["rung"]; nr = it["of"]; rr = min(r, nr - 1)
        fit = AG.fit(n, f)
        imp = max(0.05, round(AG.strength(n, f) * float(AG.fitf[n, j]), 2))
        pf = pend.get(j, [])
        bn = it["bottleneck"]
        others = [int(k) for k in occ if k != j and AG.st[n, k] == AG.st[n, j] == 1] if bn in ("time", "money") else []
        earned = [dict(name=F["say"][f][k], source="worked for" if it["worked"][k] == 1 else "came anyway",
                       titles=list(F["tnames"][f][k][:2])) for k in range(min(r, nr))]
        earned += [dict(name=a["name"], source="integrated", opens=a.get("opens", "")) for a in AG.assets[n] if j in a["slots"]]
        pot = [] if r >= nr else [dict(name=x, step=F["say"][f][r]) for x in F["tnames"][f][r][:3]] or [dict(name=F["say"][f][r], step=F["say"][f][r])]
        why = pf[0]["why"] if pf else ({"time": "the week is full", "money": "money is short", "a window": "its window has closed",
                                       "a door": "it waits for a way in"}.get(bn, ""))
        items.append(dict(slot=j, aim=F["names"][f], field=(F["items"][f]["words"].get("thing") or F["names"][f]),
                          face="".join("WUBRG"[c] for c in np.nonzero(F["face"][f] > 0)[0]), calling=bool(F["calling"][f]),
                          by_player=it["by_player"], importance=imp, why_now=why, state=_game_state(AG, n, j),
                          priority=rank[j], step=dict(i=r, of=nr, say=F["say"][f][rr] if r < nr else F["say"][f][nr - 1],
                                                      next_say=F["say"][f][r + 1] if r + 1 < nr else None),
                          progress=dict(frac=it["frac"], effort_years=it["effort"],
                                        years=(float(F["ymed"][f, rr]), float(F["ylo"][f, rr]), float(F["yhi"][f, rr]))),
                          frac=it["frac"], lean=round(fit, 2), pending=[x["id"] for x in pf],
                          bottleneck=dict(res=BN_RES.get(bn, bn), shared_with=others) if bn else None,
                          earned=earned, potential=pot, upkeep=it["upkeep"], intensity=it["intensity"],
                          funded=it["funded"], years_left=it["years_left"], window=it["window"], engine=it))
    cap = AG.account_view(n); over, strained = cap.pop("over"), cap.pop("strained")
    return dict(items=items, capacity=cap, forks=[_fork_card(AG, n, fk) for fk in AG.forks[n]], over=over, strained=strained,
                on=True, put=int(AG.put_arr[n]))


def _fork_card(AG, n, fk):
    j = fk["aims"][0]
    dl = round(int(AG.wclose[n, j]) / 52, 2) if AG.wclose[n, j] >= 0 and not AG.wclosed[n, j] else None
    urg = 1.0 if fk["urgent"] else (0.6 if fk["kind"] in ("window", "pay", "take") else 0.3)
    f = int(AG.f[n, j]); r = int(min(AG.rung[n, j], AG.F["nr"][f] - 1))
    blocks = "evenings" if AG.F["hours"][f, r] > 0 else ("money" if AG.F["money"][f, r] > 0 else "")
    return dict(id=fk["id"], slot=int(j), slots=list(fk["aims"]), kind=fk["kind"], why=fk["why"],
                made_at_age=round(fk["week"] / 52, 2), deadline_age=dl, urgency=urg, group=fk["group"] if fk["grouped"] else None,
                blocks=blocks, put=fk["put"] == AG.t)


def _pace(AG, n, j, pace, t):
    """A pace for aim j: a pending commitment fork on it is answered by it (one decision, one path)."""
    import aims2 as A2
    opt = dict(pursuing="go_on", reduced="light", paused="pause", set_aside="drop", hard="hard").get(pace)
    if pace == "keeping_up" and AG.rung[n, j] < AG.F["nr"][AG.f[n, j]]:
        return "keeping up is for a step already reached at the top of its ladder"
    for fk in list(AG.forks[n]):
        if j in fk["aims"] and fk["kind"] in ("go_on", "pay", "window", "round") and opt is not None:
            o = opt
            if fk["kind"] == "pay" and o == "go_on":
                o = "pay" if "pay" in fk["options"] else "refuse"
            if fk["kind"] == "round" and o in ("go_on", "light", "hard"):
                o = "round"
            if o in fk["options"]:
                return AG.apply(n, fk, o, t)
    st = dict(holding="held", pursuing="active", reduced="active", keeping_up="active", paused="paused",
              set_aside="dropped", hard="active")[pace]
    it = dict(pursuing=max(1.0, float(AG.inten[n, j])) if AG.st[n, j] == A2.ACTIVE else 1.0, reduced=0.5,
              keeping_up=0.5, hard=1.5).get(pace)
    return AG.set_pace(n, j, st, it, t)


def set_pace(S, n, slot, state):
    """The player's pace for an aim (GAME_PACE, or "hard"): the new agenda, or an error in words."""
    if not S.get("AIM2_ON"):
        return "aims v2 are off"
    AG = S["AG"]; n = int(n); slot = int(slot)
    if not (0 <= slot < AG.MA) or AG.f[n, slot] < 0:
        return f"no aim in slot {slot}"
    if state not in GAME_PACE + ("hard",):
        return f"no such pace: {state}"
    err = _pace(AG, n, slot, state, int(S["t"]))
    return err if err else agenda(S, n)


def set_priority(S, n, slot, rank):
    """The player's order: aim slot to rank (1 first); the new agenda, or an error in words."""
    if not S.get("AIM2_ON"):
        return "aims v2 are off"
    AG = S["AG"]; n = int(n); slot = int(slot)
    if not (0 <= slot < AG.MA) or AG.f[n, slot] < 0:
        return f"no aim in slot {slot}"
    AG.set_priority(n, slot, int(rank) - 1)
    return agenda(S, n)


def _group(AG, n, group):
    fks = AG.forks[n]
    if isinstance(group, (int, np.integer)):
        fk = next((x for x in fks if x["id"] == int(group)), None)
        if fk is None:
            return []
        return [x for x in fks if fk["grouped"] and x["group"] == fk["group"]] or [fk]
    return [x for x in fks if x["group"] == group]


def review(S, n, group):
    """The agenda review of a group (a fork id, or a group key): the linked forks, why they are linked, each one's
    preview and options, the account now, and the account after each combination of answers (with the aims it would
    leave slower). Draws nothing, costs no time."""
    if not S.get("AIM2_ON"):
        return None
    import itertools
    AG = S["AG"]; n = int(n); fks = _group(AG, n, group)
    if not fks:
        return None
    key = fks[0]["group"]
    why = ("they want the same hours of the week" if key == "time" else
           "their windows close at about the same time" if key and key.startswith("window") else fks[0]["why"])
    cap = AG.account_view(n); cap.pop("over"); cap.pop("strained")
    forks = [dict(id=fk["id"], slot=int(fk["aims"][0]), slots=list(fk["aims"]), kind=fk["kind"], why=fk["why"],
                  deadline_age=_fork_card(AG, n, fk)["deadline_age"], preview=AG.preview(n, int(fk["aims"][0])),
                  options=[dict(key=o, say=OPT_SAY.get(o, o)) for o in fk["options"]]) for fk in fks]
    combos = []
    opts = [[o for o in fk["options"] if o != "later"] for fk in fks]
    for ch in itertools.islice(itertools.product(*opts), 64):
        sets = {}
        for fk, o in zip(fks, ch):
            for j in fk["aims"]:
                if o in ("go_on", "pay", "refuse", "take", "round"):
                    sets[j] = (True, max(1.0, float(AG.inten[n, j])) if AG.st[n, j] == 1 else 1.0)
                elif o == "light":
                    sets[j] = (True, 0.5)
                elif o == "hard":
                    sets[j] = (True, 1.5)
                elif o in ("pause", "drop", "decline"):
                    sets[j] = (False, 0.0) if o != "decline" else sets.get(j, (AG.st[n, j] == 1, float(AG.inten[n, j])))
            if o in ("light_last", "pause_last"):
                act = [int(j) for j in np.nonzero((AG.st[n] == 1) & (AG.f[n] >= 0))[0]]
                if act:
                    jl = max(act, key=lambda j: AG.pri[n, j])
                    sets[jl] = (True, 0.5) if o == "light_last" else (False, 0.0)
        ch_h, ch_m, fund = AG.what_if(n, sets)
        combos.append(dict(choices={fk["id"]: o for fk, o in zip(fks, ch)},
                           capacity=dict(time=dict(have=round(float(AG.cap["time"][n]), 1), committed=round(ch_h, 1)),
                                         money=dict(have=round(float(AG.cap["money"][n]), 3), committed=round(ch_m, 3))),
                           slower=sorted(j for j, v in fund.items() if v < 0.999)))
    return dict(group=key if key is not None else fks[0]["id"], why=why, capacity=cap, forks=forks, combos=combos)


def apply_review(S, n, a):
    """Apply a review's answers once: dict(choices={fork id: option key}, set={slot: pace}); a fork left out stays
    open. The new agenda (with "errors", in words, for any answer that could not apply)."""
    if not S.get("AIM2_ON"):
        return "aims v2 are off"
    AG = S["AG"]; n = int(n); t = int(S["t"]); errs = []
    for fid, key in (a.get("choices") or {}).items():
        try:
            fid = int(fid)
        except (TypeError, ValueError):
            errs.append(f"no fork {fid}"); continue
        e = AG.apply(n, fid, key, t)
        if e:
            errs.append(e)
    for slot, pace in (a.get("set") or {}).items():
        e = set_pace(S, n, int(slot), pace)
        if isinstance(e, str):
            errs.append(e)
    out = agenda(S, n); out["errors"] = errs
    return out


def preview(S, n, name_or_slot, step=None):
    """What is known before a commitment (Gamification's shape): needs, cost (entry, money (lo, hi) a year), hours (lo,
    hi) a week, overlaps (slots, and work, care or ties), window (opens, closes) in ages, unknown, exit (say). From the
    life's own state, never a simulated future; draws nothing."""
    if not S.get("AIM2_ON"):
        return None
    AG = S["AG"]; n = int(n)
    if isinstance(name_or_slot, (int, np.integer)):
        j = int(name_or_slot)
        if not (0 <= j < AG.MA) or AG.f[n, j] < 0:
            return None
        return AG.preview(n, j=j, r=step)
    if name_or_slot not in AG.F["names"]:
        return None
    f = AG.F["names"].index(name_or_slot)
    js = np.nonzero(AG.f[n] == f)[0]
    return AG.preview(n, j=int(js[0]), r=step) if len(js) else AG.preview(n, f=f, r=step or 0)


def _set_aim2(S, n, name):
    AG = S["AG"]; n = int(n)
    if name not in AG.F["names"]:
        return f"no aim {name!r}"
    f = AG.F["names"].index(name); v1 = int(AG.F["v1"][f])
    if v1 >= 0 and S.get("aim_take") is not None:   # v1 holds it too (its seeking, its spark), as set by the player
        S["aim_take"](n, v1, S["P"]["aims_par"]["set_s"], own=False, by=True, src="player")
    if not (AG.f[n] == f).any() or AG.st[n, np.nonzero(AG.f[n] == f)[0][0]] == 3:
        AG.add(n, f, int(S["t"]), by=True, src="player")
    else:
        AG.by[n, np.nonzero(AG.f[n] == f)[0][0]] = True
    return agenda(S, n)
