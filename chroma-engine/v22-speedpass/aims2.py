"""Aims v2 (v25 lane B, the switch aims_v2; Emren's decision #9 in chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md
section 5, which wins; chroma-engine/notes/v25/aims-shape.md sections 2 to 7 and contracts.md sections 1, 5 to 7).

Every aim a life holds is on its agenda, with no slot limit: held (an ambition, not pursued), active (at an intensity),
paused or dropped. Each rung keeps three clocks apart: effort (years of steady work, for active aims only, funded from
the one resource account), an external window (closes exactly at its last week; pausing does not stop it unless the rung
says pause_stops; never reopened by toggling; told once) and a demonstrated outcome (a door title of the rung held, a
contest or chance won, a work rung). Effort alone never reaches a rung. Consequential turns are forks: an unattended
life picks by its own odds; a player's fork (lives in aims2_par player) waits in aim_forks until answered and blocks
only its aim's progress past the fork. Gains: learning kept in proportion after a pause or a drop, selective upkeep (only
where a rung names it), integrated assets once per pair through an integrate outcome.

Realm-ready: the mechanics are colours (a field's face and the life's fit), needs (what practice restores, what strain
costs), means (money, the hours of the week), people (a partner's or family's support), places and powers (titles,
perks). In a magic realm a field is a school of the towers or a guild's ladder, the window the court's season of trials,
the entry cost an apprentice's fee: the realm's FIELDS and AIM_WEEK say so, the rules here stay. Earth's hours are in
realm_earth.AIM_WEEK, its integrated assets in realm_earth.AIM_ASSETS.

The fields: the Library's FIELDS_<WORLD> (<world>_fields.py) where present; every v1 aim with no field of its name gets
one from the adapter below (aims-shape.md section 7), with the clocks and demands of SHAPE_DEF: PROVISIONAL design values,
not research, to be replaced by the Library's per-field clocks.
"""
import os
import numpy as np

from world_keys import AIM_SHAPES, CAPACITY_BEFORE

HELD, ACTIVE, PAUSED, DROPPED = range(4)
STATES = ("held", "active", "paused", "dropped")
INTENSITY = dict(light=0.5, steady=1.0, hard=1.5)
SHAPES = list(AIM_SHAPES)

# aims-shape.md section 7: v1's area (or, empty, a career domain) -> the shape
AREA_SHAPE = dict(justice="cause", cause="cause", community="cause", freedom="cause", line="home", love="home",
                  home="home", land="land", faith="faith", craft="craft", art="art", knowledge="knowledge",
                  body="competition", adventure="venture", wealth="career", standing="career", care="career")

# ---- PROVISIONAL per-shape defaults for the adapter (design values, labelled; the Library's fields replace them) ----
# by the shape's rung index: years (median, 10th, 90th percentile) of steady effort from the rung below, the share of
# those who keep at it who reach it, the forks always put at it
YEARS = [(1.5, 0.5, 3.0), (2.5, 1.0, 5.0), (3.0, 1.5, 6.0), (4.0, 2.0, 9.0), (4.0, 2.0, 10.0)]
SHARE = [0.9, 0.6, 0.35, 0.15, 0.12]
FORKS = [["go_on"], ["pay"], ["take"], ["go_on", "take"], ["take"]]
ENTRY_BY_RUNG = [0.3, 1.0, 0.5, 0.5, 0.5]   # x the shape's entry: the big fee is the second rung's (a club, a course)
# per shape: hours a week at steady intensity on its first rung (x (1 + .25 rung)), money a year and the entry (shares
# of a year's free money; money x (1 + .3 rung)), how tiring (0 to 1), tests a year by rung (contests; 0: the
# engine-built chance at chance_y), shared preparation tags, the needs practice restores, rungs that come with time,
# the ages interest starts (from, best_to, late_from), and external windows by rung index
SHAPE_DEF = {
    "competition": dict(hours=5, money=.08, entry=.05, energy=.6, contests=(0, 4, 5, 5, 4), chance_y=.5,
                        prep=("strength", "a club"), meets=("competence", "belonging"), start=(6, 12, 18),
                        window={3: dict(deadline_age=40)}),
    "craft": dict(hours=6, money=.06, entry=.10, energy=.5, contests=(0, .5, .5, .5, .5), chance_y=.5,
                  prep=("a workshop",), meets=("competence",), start=(12, 16, 30)),
    "art": dict(hours=6, money=.04, entry=.03, energy=.4, contests=(0, 1, 1, 1, 1), chance_y=.5,
                prep=("a stage",), meets=("meaning", "competence"), start=(8, 14, 30)),
    "knowledge": dict(hours=8, money=.08, entry=.15, energy=.5, contests=(0, 1, 1, 1, .5), chance_y=.5,
                      prep=("reading",), meets=("competence", "meaning"), start=(10, 16, 30),
                      window={1: dict(every=1, open_weeks=6)}),
    "career": dict(hours=4, money=.02, entry=.05, energy=.5, contests=(0, 1, 1, 1, 1), chance_y=.5,
                   prep=("contacts",), meets=("competence",), start=(16, 20, 40)),
    "cause": dict(hours=4, money=.02, entry=0.0, energy=.4, contests=(0, .5, .5, .5, .5), chance_y=.5,
                  prep=("organising", "contacts"), meets=("belonging", "meaning"), start=(12, 18, 60)),
    "home": dict(hours=3, money=.05, entry=0.0, energy=.3, contests=(0, 0, 0, 0), chance_y=0.0,
                 prep=(), meets=("belonging",), start=(16, 25, 45), time=(2, 3)),
    "land": dict(hours=5, money=.04, entry=.05, energy=.5, contests=(0, .5, .5, .5, .5), chance_y=.5,
                 prep=("the land",), meets=("meaning", "autonomy"), start=(8, 20, 60)),
    "faith": dict(hours=3, money=.01, entry=0.0, energy=.2, contests=(0, .3, .3, .3, .3), chance_y=.3,
                  prep=("a congregation",), meets=("belonging", "meaning"), start=(8, 16, 70)),
    "venture": dict(hours=5, money=.12, entry=.10, energy=.6, contests=(0, 1, 1, 1), chance_y=.5,
                    prep=("strength", "travel"), meets=("autonomy", "competence"), start=(14, 20, 40)),
}

# the switch's numbers (DEFAULT aims2_par None = these; a dict there overrides any of them)
PAR = dict(
    player=(),          # the lives whose forks wait for the player (the game: (0,)); every other life is unattended
    prep_share=0.3,     # of an aim's hours that a shared preparation tag counts once (the second aim's part)
    support_share=0.15,  # of the first aim's hours a partner covers (the giver's time, debited once)
    family_pays=0.5,    # of a child's (under 18) aim money the family pays
    attention=2.5,      # active aims at steady intensity a life can attend to before quality drops
    over=1.2,           # demanded hours over capacity x this: overcommitted
    over_fork_wk=8,     # weeks overcommitted before the agenda review (or the character's own pick)
    strain_wk=26,       # weeks overcommitted before strain on needs (rest, the bonds that lost time)
    strain=(0.004, 0.002),   # a week's strain: stress up, belonging down (never a forced collapse)
    restore=0.002,      # a week's restoration of the needs a pursuit meets, per 10 funded hours, x the gap
    money_k=0.1,        # an entry cost (share of a year's free money) as a debit of the money level (once)
    money_floor=0.1,    # the money level the essentials take first
    refuse_need=1.3,    # going on without paying a fee: the need x this
    round_need=1.25,    # a way round a closed window: the need x this
    late=0.3,           # the need x (1 + this a decade) for a start after the field's late_from
    reask=52,           # weeks before an unchanged pending fork is put again
    window_warn=13,     # weeks before a window closes that it is a fork (once a rung)
    integrate_y=0.25,   # integrate outcomes a year for a life holding a pair the realm's AIM_ASSETS names
    refresh_wk=13,      # weeks of renewed use that refresh a lapsed upkeep
    meet=(0.03, 0.06, 0.09, 0.12),   # meaning met by a rung reached outside v1's slots (v1's own meet), by height
    assets=None,        # tests: an AIM_ASSETS table in place of the realm's
    field_patch=None,   # tests: {field name: {rung index: {key: value}}} over the compiled fields
)
NEVER = -10 ** 9
CACHE = {}   # the compiled fields of the last batch (and field_patch) a run used


def _fields_v1(AIM):
    """aims-shape.md section 7: each v1 aim (the batch's L["AIMS"]) as a field of section 3, by its area."""
    out = {}
    for a in AIM["aims"]:
        shape = AREA_SHAPE.get(a.get("area") or "", "career" if a["dom"] >= 0 else "career")
        out[a["name"]] = dict(shape=shape, v1=a, rungs=[dict(say=st["say"], ids=st["any"], names=st["names"], req=st["req"],
                                                            req_s=st["req_s"], h=st["h"]) for st in a["steps"]])
    return out


def _fields_lib(world, lib_dir):
    """The Library's FIELDS_<WORLD> (<world>_fields.py), or {}."""
    p_ = os.path.join(lib_dir, f"{world}_fields.py")
    if not os.path.exists(p_):
        return {}
    import importlib.util
    sp_ = importlib.util.spec_from_file_location(f"chroma_{world}_fields_v25", p_)
    m_ = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(m_)
    out = dict(getattr(m_, f"FIELDS_{world.upper()}", {}) or {})
    out.update(getattr(m_, f"FIELDS_{world.upper()}_LAND", {}) or {})   # the land's ways (land.json), when written
    return out


def compile_fields(L, par, C, NIDX, heights):
    """The fields for the engine (L["FIELDS"], built once per batch): the Library's where present, then every v1 aim
    without a field of its name by the adapter. Arrays by field x rung (K the most rungs)."""
    import batch as BA
    from world_keys import SPHERES as SPH_
    GR = L["ROLES"]; RID = {nm: i for i, nm in enumerate(GR["names"])}
    AIM = L["AIMS"]; V1 = {nm: i for i, nm in enumerate(AIM["names"])}
    lib = _fields_lib(L.get("world") or "earth", BA.LIB_DIR)
    items = []
    for nm, x in lib.items():
        if x.get("shape") not in AIM_SHAPES:
            continue
        rungs = []
        for r in x.get("rungs") or []:
            ids = np.array([RID[y] for y in r.get("any") or [] if y in RID], int)
            h = r.get("height") or ""
            rungs.append(dict(r, say=r.get("say", ""), ids=ids, names=[y for y in r.get("any") or [] if y in RID],
                              req=BA._code(r["req"]) if r.get("req") else None, req_s=r.get("req") or "",
                              h=heights.index(h) + 1 if h in heights else 0))
        if not rungs:
            continue
        face = np.zeros(C)
        for c in str(x.get("face") or "").replace(",", " ").split():
            if c.strip() in "WUBRG" and c.strip():
                face["WUBRG".index(c.strip())] += 1.0
        sph = str(x.get("sphere") or "")
        a1 = AIM["aims"][V1[nm]] if nm in V1 else None
        items.append(dict(name=nm, shape=x["shape"], face=face / face.sum() if face.sum() else np.full(C, 1 / C),
                          sph=SPH_.index(sph) if sph in SPH_ else -1, calling=bool(x.get("calling", False)),
                          v1=V1.get(nm, -1), rungs=rungs, prep=list(x.get("prep") or []), meets=list(x.get("meets") or []),
                          start=tuple(x.get("rungs")[0].get("start") or SHAPE_DEF[x["shape"]]["start"]),
                          words=dict(thing=x.get("thing", ""), doing=x.get("doing", ""), contest=x.get("contest", ""),
                                     round=list(x.get("round") or []), people=dict(x.get("people") or {})),
                          src="library", dom=a1["dom"] if a1 else -1))
    have = {it["name"] for it in items}
    for nm, x in _fields_v1(AIM).items():
        if nm in have:
            continue
        a1 = x["v1"]; d = SHAPE_DEF[x["shape"]]
        items.append(dict(name=nm, shape=x["shape"], face=a1["face"], sph=a1["sph"], calling=a1["calling"], v1=V1[nm],
                          rungs=x["rungs"], prep=list(d["prep"]), meets=list(d["meets"]), start=tuple(d["start"]),
                          words=dict(thing="", doing="", contest="", round=[], people={}), src="v1", dom=a1["dom"]))
    Fn = len(items); K = max(len(it["rungs"]) for it in items)
    z = lambda v=0.0, dt=float: np.full((Fn, K), v, dt)
    F = dict(names=[it["name"] for it in items], items=items, F=Fn, K=K, shape=np.array([SHAPES.index(it["shape"]) for it in items]),
             face=np.array([it["face"] for it in items]), sph=np.array([it["sph"] for it in items]),
             v1=np.array([it["v1"] for it in items]), nr=np.array([len(it["rungs"]) for it in items]),
             calling=np.array([it["calling"] for it in items], bool), start=np.array([it["start"] for it in items], float),
             ymed=z(), ylo=z(), yhi=z(), share=z(1.0), outy=z(), hours=z(), money=z(), entry=z(), energy=z(),
             time=z(False, bool), w_every=z(), w_open=z(), w_dage=z(-1.0), w_dyrs=z(-1.0), w_pstop=z(False, bool),
             up_yrs=z(-1.0), up_of=z(-1, int), up_work=z(False, bool), h=z(0, int),
             forks=[[[] for _ in range(K)] for _ in range(Fn)], ids=[[np.zeros(0, int)] * K for _ in range(Fn)],
             req=[[None] * K for _ in range(Fn)], say=[[""] * K for _ in range(Fn)], tnames=[[[] for _ in range(K)] for _ in range(Fn)])
    tags = sorted({t for it in items for t in it["prep"]})
    F["prep_tags"] = tags
    F["prep"] = np.array([sum(1 << tags.index(t) for t in it["prep"]) for it in items], np.int64)
    NJ = len(NIDX)
    F["meets"] = np.zeros((Fn, NJ))
    patch = par.get("field_patch") or {}
    for i, it in enumerate(items):
        for nd in it["meets"]:
            if nd in NIDX:
                F["meets"][i, NIDX[nd]] = 1.0
        d = SHAPE_DEF[it["shape"]]; Ks = len(AIM_SHAPES[it["shape"]]); nr = len(it["rungs"])
        for r, rg in enumerate(it["rungs"]):
            rg = dict(rg, **(patch.get(it["name"], {}).get(r, {})))
            k = r if nr >= Ks else int(round(r * (Ks - 1) / max(nr - 1, 1)))   # the shape rung it maps onto
            k = min(k, 4)
            dm = rg.get("demand") or {}
            ys = rg.get("years") or YEARS[k]
            F["ymed"][i, r], F["ylo"][i, r], F["yhi"][i, r] = (float(v) for v in ys)
            F["share"][i, r] = float(rg.get("share", SHARE[k]))
            ct = rg.get("contests_y", d["contests"][min(k, len(d["contests"]) - 1)])
            F["outy"][i, r] = float(ct) if ct else float(d["chance_y"])
            F["hours"][i, r] = float(dm.get("hours", d["hours"] * (1 + 0.25 * k)))
            F["money"][i, r] = float(dm.get("money", d["money"] * (1 + 0.3 * k)))
            F["entry"][i, r] = float(dm.get("entry", d["entry"] * ENTRY_BY_RUNG[k]))
            F["energy"][i, r] = float(dm.get("energy", d["energy"]))
            F["time"][i, r] = bool(rg.get("time", k in d.get("time", ())))
            if F["time"][i, r]:
                F["hours"][i, r] = F["money"][i, r] = F["entry"][i, r] = 0.0
            wd = rg["window"] if "window" in rg else d.get("window", {}).get(k)
            if wd:
                F["w_every"][i, r] = float(wd.get("every") or 0); F["w_open"][i, r] = float(wd.get("open_weeks") or 0)
                F["w_dage"][i, r] = float(wd["deadline_age"]) if wd.get("deadline_age") is not None else -1.0
                F["w_dyrs"][i, r] = float(wd["deadline_years"]) if wd.get("deadline_years") is not None else -1.0
                F["w_pstop"][i, r] = bool(wd.get("pause_stops", False))
            up = rg.get("upkeep")
            if up:
                F["up_yrs"][i, r] = float(up.get("years", 5)); F["up_of"][i, r] = ("proficiency", "access", "credential").index(up.get("of", "proficiency"))
                F["up_work"][i, r] = "work" in (up.get("kept_by") or ())
            F["forks"][i][r] = list(rg.get("forks") or FORKS[k])
            F["ids"][i][r] = np.asarray(rg["ids"], int); F["req"][i][r] = rg.get("req"); F["say"][i][r] = rg.get("say", "")
            F["tnames"][i][r] = list(rg.get("names") or []); F["h"][i, r] = int(rg.get("h", 0))
    lean = F["face"] - 1 / C
    F["lean"] = lean / np.maximum(np.linalg.norm(lean, axis=1, keepdims=True), 1e-9)
    F["of_v1"] = {int(v): i for i, v in enumerate(F["v1"]) if v >= 0}
    F["upkeep_any"] = bool((F["up_yrs"] > 0).any())
    F["src"] = "library+v1" if lib else "v1 adapter"
    return F


class Agenda:
    """Every life's aims (N x slots, growing as needed: no slot limit), the one resource account, the forks."""
    CELL = dict(f=(-1, int), st=(HELD, np.int8), inten=(1.0, float), pri=(0.0, float), rung=(0, int), eff=(0.0, float),
                need=(1.0, float), by=(False, bool), born=(0, int), talent=(1.0, float), funded=(0.0, float),
                fh=(0.0, float), dem=(0.0, float), rstart=(0, int), wclose=(-1, int), wclosed=(False, bool),
                wtold=(False, bool), wwarn=(False, bool), wround=(False, bool), declined=(False, bool),
                refused=(False, bool), fork=(-1, int), last_use=(0, int), act_wk=(0, int), fitf=(1.0, float),
                syn=(False, bool), prof=(1.0, float), noaccess=(False, bool))
    RUNG = dict(learned=(0.0, float), worked=(-1, np.int8), paid=(False, bool), faded=(False, bool))

    def __init__(s, N, F, par, seed, ctx):
        s.N, s.F, s.par, s.ctx = N, F, par, ctx
        s.rng = np.random.default_rng([int(seed), 2509])   # the agenda draws only here: no other stream moves
        s.MA = 4; s.K = F["K"]
        for nm, (v, dt) in s.CELL.items():
            setattr(s, nm, np.full((N, s.MA), v, dt))
        for nm, (v, dt) in s.RUNG.items():
            setattr(s, nm, np.full((N, s.MA, s.K), v, dt))
        s.player = set(int(x) for x in (par.get("player") or ()))
        s.forks = [[] for _ in range(N)]                  # aim_forks: each life's unresolved forks (player lives only)
        s.put_arr = np.full(N, -1)                        # aim_fork: the fork put this week (its id), -1 none
        s.next_id = 0; s.log = []; s.burden = []; s.decisions = 0
        s.debit = np.zeros(N)                             # entry costs decided, debited from the money at the next week
        s.cap = dict(time=np.zeros(N), money=np.zeros(N), energy=np.ones(N), attention=np.full(N, par["attention"]),
                     support=np.zeros(N))
        s.before = np.zeros((N, len(CAPACITY_BEFORE)))   # the hours work, care, household, ties and essentials take
        s.committed = dict(time=np.zeros(N), money=np.zeros(N), energy=np.zeros(N), attention=np.zeros(N),
                           support=np.zeros(N), access=np.zeros(N))
        s.entry_log = [[] for _ in range(N)]             # every entry cost paid (field, rung, week, amount): once each
        s.support_log = [[] for _ in range(N)]           # the support given (from whom, hours a week, month): once a month
        s.over_wk = np.zeros(N, int); s.strained = np.zeros(N, bool)
        s.assets = [[] for _ in range(N)]; s.awarded = [set() for _ in range(N)]
        tab = par.get("assets")
        if tab is None:
            from realm_earth import AIM_ASSETS as tab
        s.asset_tab = {}
        for k_, v_ in (tab or {}).items():
            s.asset_tab[tuple(sorted(k_))] = dict(v_)
        s.dirty = True; s.w = None; s.t = 0

    # ---- slots
    def _grow(s):
        add = s.MA
        for nm, (v, dt) in s.CELL.items():
            a = getattr(s, nm); setattr(s, nm, np.concatenate([a, np.full((s.N, add), v, dt)], 1))
        for nm, (v, dt) in s.RUNG.items():
            a = getattr(s, nm); setattr(s, nm, np.concatenate([a, np.full((s.N, add, s.K), v, dt)], 1))
        s.MA += add

    def _log(s, n, j, what, **extra):
        f = int(s.f[n, j])
        rec = dict(life=int(n), age=round(s.t / 52, 2), week=int(s.t), what=what, field=s.F["names"][f], slot=int(j),
                   state=STATES[int(s.st[n, j])], rung=int(s.rung[n, j]), of=int(s.F["nr"][f]), **extra)
        s.log.append(rec)
        ev = s.ctx["events"]
        if n in ev:
            ev[n].append(dict(aim2=rec))

    def fit(s, n, f):
        w = s.w[n] if s.w is not None else np.full(s.F["face"].shape[1], 1 / s.F["face"].shape[1])
        lm = w / w.sum() - 1 / len(w); nr = float(np.linalg.norm(lm))
        return float(s.F["lean"][f] @ (lm / nr)) if nr > 1e-9 else 0.0

    def strength(s, n, f):
        v1 = int(s.F["v1"][f]); ak = s.ctx["ak"]
        if v1 >= 0 and ak is not None:
            q = np.nonzero(ak[n] == v1)[0]
            if len(q):
                return float(s.ctx["astr"][n, q[0]])
        return 0.3

    def add(s, n, f, t, by=False, src=""):
        """Life n holds field f (an ambition; held, not yet pursued); the commitment to its step is a fork. A field it
        already holds is held again (its rungs, learning, entry costs paid and windows kept: nothing is earned twice)."""
        s.t = t
        js = np.nonzero(s.f[n] == f)[0]
        if len(js):
            j = int(js[0]); s.by[n, j] |= bool(by)
            if s.st[n, j] == DROPPED:
                s.st[n, j] = HELD; s._log(n, j, "held again", source=src)
                if s.rung[n, j] < s.F["nr"][f] and not s.F["time"][f, s.rung[n, j]]:
                    s.fork_new(n, [j], "go_on", t, "an ambition taken up again")
            return j
        fr = np.nonzero(s.f[n] < 0)[0]
        if not len(fr):
            s._grow(); fr = np.nonzero(s.f[n] < 0)[0]
        j = int(fr[0])
        for nm, (v, dt) in s.CELL.items():
            getattr(s, nm)[n, j] = v
        for nm, (v, dt) in s.RUNG.items():
            getattr(s, nm)[n, j] = v
        s.f[n, j] = f; s.st[n, j] = HELD; s.by[n, j] = bool(by); s.born[n, j] = t; s.last_use[n, j] = t
        s.talent[n, j] = float(np.exp(s.rng.normal(0.0, 0.25)))
        s.fitf[n, j] = float(np.clip(0.75 + 0.5 * s.fit(n, f), 0.4, 1.25))
        act = s.f[n] >= 0
        s.pri[n, j] = (s.pri[n, act].max() + 1) if act.sum() > 1 else 0.0
        s._log(n, j, "held", source=src, by_player=bool(by))
        s.start_rung(n, j, t, first=True)
        return j

    def start_rung(s, n, j, t, first=False):
        """A new rung: its need drawn (the long road at 1 - share: a tripled need; a late start costs more), its window
        set, and the commitment to it a fork (none for a rung that comes with time)."""
        f = int(s.f[n, j]); r = int(s.rung[n, j]); F = s.F
        s.rstart[n, j] = t; s.wclose[n, j] = -1; s.wclosed[n, j] = s.wtold[n, j] = s.wwarn[n, j] = s.wround[n, j] = False
        s.declined[n, j] = s.refused[n, j] = False; s.eff[n, j] = 0.0
        if r >= F["nr"][f]:
            s.dirty = True
            return
        med, lo, hi = F["ymed"][f, r], F["ylo"][f, r], F["yhi"][f, r]
        sg = max((np.log(max(hi, 1e-3)) - np.log(max(lo, 1e-3))) / 2.563, 0.05)
        nd = float(np.clip(med * np.exp(sg * s.rng.normal()), 0.7 * lo, 1.5 * hi))
        if s.rng.random() >= F["share"][f, r]:
            nd *= 3.0                                     # the long road
        if r == 0 and t / 52 > F["start"][f, 2]:
            nd *= 1 + s.par["late"] * (t / 52 - F["start"][f, 2]) / 10
        s.need[n, j] = max(nd, 0.05)
        cl = []
        if F["w_dage"][f, r] >= 0:
            cl.append(int(round(F["w_dage"][f, r] * 52)))
        if F["w_dyrs"][f, r] >= 0:
            cl.append(t + int(round(F["w_dyrs"][f, r] * 52)))
        if cl:
            s.wclose[n, j] = min(cl)
        s.dirty = True
        if F["time"][f, r]:
            return
        if r == 0 and t / 52 < F["start"][f, 0] and s.st[n, j] == HELD:
            return   # held until the age interest usually starts; then the commitment is a fork (month)
        kind = "pay" if ("pay" in F["forks"][f][r] and F["entry"][f, r] > 0 and not s.paid[n, j, r]) else "go_on"
        if first or s.st[n, j] != DROPPED:
            s.fork_new(n, [j], kind, t, "a new ambition" if first else "a new step")

    def v1_end(s, n, f, what):
        """v1 ended an aim: "let go" (the player, or a spark's drop) sets it aside; "faded" (no goal behind it) sets
        aside only an ambition not being pursued. Pushed aside by v1's slots, it stays on the agenda."""
        js = np.nonzero(s.f[n] == f)[0]
        if not len(js):
            return
        j = int(js[0])
        if what == "let go" or s.st[n, j] in (HELD, PAUSED):
            if s.st[n, j] != DROPPED:
                s.st[n, j] = DROPPED; s._log(n, j, "set aside", why=what, learned=round(float(s.learned[n, j].sum()), 2))
                s.dirty = True

    def pull(s, pu, door, ak):
        """The seeking: an active aim outside v1's slots raises the odds of the moments with a way into its rung, by
        its intensity (half of v1's own pull at the same strength)."""
        F = s.F
        for j in range(s.MA):
            f = s.f[:, j]
            on = (f >= 0) & (s.st[:, j] == ACTIVE)
            if not on.any():
                continue
            ns = np.nonzero(on)[0]; v1 = F["v1"][f[ns]]; r = s.rung[ns, j]
            ok = (v1 >= 0) & (r < door.shape[1] - 1)
            if ak is not None:
                ok &= ~(ak[ns] == v1[:, None]).any(1)
            if ok.any():
                ns, v1, r = ns[ok], v1[ok], r[ok]
                pu[ns] += (0.5 * s.inten[ns, j][:, None] * door[v1, r]).astype(np.float32)

    # ---- forks
    def options(s, n, j, kind):
        f = int(s.f[n, j]); r = int(min(s.rung[n, j], s.F["nr"][f] - 1))
        if r == 0 and s.t / 52 < s.F["start"][f, 0] and kind in ("go_on", "pay"):
            return ["pause", "drop"]   # too young for its first step: held until the age interest usually starts
        if kind == "go_on":
            return ["go_on", "light", "hard", "pause", "drop"]
        if kind == "pay":
            ok = s.can_pay(n, j)
            return (["pay"] if ok else []) + ["refuse", "pause", "drop"]
        if kind == "take":
            return ["take", "decline", "drop"]
        if kind == "window":
            return ["hard", "go_on", "pause", "drop"]
        if kind == "round":
            return ["round", "pause", "drop"]
        if kind == "over":
            return ["keep", "light_last", "pause_last"]
        return ["go_on", "drop"]

    def can_pay(s, n, j):
        """An entry is viable only when the life can meet it: its free money (a child's family pays its share)."""
        f = int(s.f[n, j]); r = int(s.rung[n, j])
        if r >= s.F["nr"][f]:
            return False
        e = s.F["entry"][f, r] * (1 - s.par["family_pays"] * (s.t / 52 < 18))
        return bool(s.cap["money"][n] >= 0.5 * e)

    def fork_new(s, n, js, kind, t, why):
        """A consequential turn for aims js of life n. Unattended: the character's own pick now, by its odds (declared
        policy). A player's: kept in aim_forks until answered, blocking only these aims' progress past it."""
        s.t = t
        fid = s.next_id; s.next_id += 1
        opts = s.options(n, js[0], kind)
        if n not in s.player:
            s.apply(n, dict(id=fid, aims=list(js), kind=kind, options=opts), s.policy(n, js, kind, opts), t, by="character")
            return fid
        fk = dict(id=fid, aims=[int(j) for j in js], kind=kind, why=why, options=opts + ["later"], week=int(t), put=-1,
                  changed=False, urgent=False, grouped=False, group=None)
        fk["preview"] = s.preview(n, int(js[0]))
        fk["facts"] = s._facts(n, fk)
        s.forks[n].append(fk)
        if kind != "over":
            for j in js:
                s.fork[n, j] = fid
        s._log(n, js[0], "fork", kind=kind, id=fid, aims=[s.F["names"][int(s.f[n, j])] for j in js], why=why)
        return fid

    def policy(s, n, js, kind, opts):
        """The character's own pick (an unattended life's fork): by fit, strength, the room in the account, and money."""
        j = js[0]; f = int(s.f[n, j]); ff = float(s.fitf[n, j]); st = s.strength(n, f)
        room = s.cap["time"][n] - s.committed["time"][n]
        dem = s.F["hours"][f, min(int(s.rung[n, j]), s.F["nr"][f] - 1)]
        roomy = 1.0 if room >= dem else 0.4
        nact = int(((s.st[n] == ACTIVE) & (s.f[n] >= 0)).sum())
        wt = dict(go_on=ff * (0.5 + st) * roomy, light=0.3 * ff * (0.5 + st) * (1.4 - roomy), hard=0.15 * ff * st * roomy,
                  pause=0.3 + 0.25 * nact, drop=0.12 * max(1.5 - ff, 0.1), pay=ff * (0.5 + st) * roomy,
                  refuse=0.4 * (1.4 - roomy) + 0.2, take=ff * (0.6 + st), decline=0.25, round=0.6 * ff * (0.5 + st),
                  keep=0.3, light_last=0.5, pause_last=0.4)
        p = np.array([wt.get(o, 0.1) for o in opts], float); p = p / p.sum()
        return opts[int(s.rng.choice(len(opts), p=p))]

    def apply(s, n, fk, opt, t, by="player", sets=None):
        """Apply a fork's option (and, for a review, the player's settings per aim) once; the fork is resolved."""
        s.t = t
        if isinstance(fk, int):
            fk = next((x for x in s.forks[n] if x["id"] == fk), None)
            if fk is None:
                return "no such fork"
        if opt is not None and opt not in fk["options"]:
            return f"not an option here: {opt}"
        if opt == "later":   # the player's "later": the fork stays open, only its aims wait
            fk["put"] = int(t); fk["changed"] = False
            s.burden.append(dict(what="later", life=int(n), week=int(t), id=fk["id"], aims=len(fk["aims"]), choices=0, kind=fk["kind"]))
            return None
        js = list(fk["aims"])
        for j in js:
            if s.f[n, j] < 0:
                continue
            s._do(n, j, opt, fk["kind"], t)
        for j, x in (sets or {}).items():
            s.set_pace(n, int(j), x.get("state"), x.get("intensity"), t)
            if x.get("priority") is not None:
                s.set_priority(n, int(j), x["priority"])
        if fk in s.forks[n]:
            s.forks[n].remove(fk)
        for j in js:
            if s.fork[n, j] == fk["id"]:
                s.fork[n, j] = -1
        s.decisions += 1
        if by == "player":
            s.burden.append(dict(what="answer", life=int(n), week=int(t), id=fk["id"], aims=len(js), choices=1 + len(sets or {}),
                                 kind=fk["kind"]))
        s._log(n, js[0], "decided", kind=fk["kind"], id=fk["id"], option=opt, by=by)
        s.dirty = True
        return None

    def _do(s, n, j, opt, kind, t):
        f = int(s.f[n, j]); r = int(s.rung[n, j]); nr = int(s.F["nr"][f])
        if opt in ("go_on", "pay", "hard", "light", "take", "round", "keep") and s.st[n, j] == DROPPED:
            return
        if opt in ("go_on", "pay"):
            s.activate(n, j, max(float(s.inten[n, j]), 1.0) if s.st[n, j] == ACTIVE else 1.0, t, pay=True)
        elif opt == "hard":
            s.activate(n, j, 1.5, t, pay=True)
        elif opt == "light":
            s.activate(n, j, 0.5, t, pay=True)
        elif opt == "refuse":
            if r < nr and not s.refused[n, j]:
                s.refused[n, j] = True; s.need[n, j] *= s.par["refuse_need"]
            s.activate(n, j, 1.0, t, pay=False)
        elif opt == "pause":
            if s.st[n, j] == ACTIVE:
                s.st[n, j] = PAUSED
        elif opt == "drop":
            s.st[n, j] = DROPPED; s._log(n, j, "set aside", learned=round(float(s.learned[n, j].sum()), 2))
        elif opt == "take":
            s.outcome(n, j, t, chance=True)
        elif opt == "decline":
            s.declined[n, j] = True
        elif opt == "round":
            if not s.wround[n, j]:
                s.wround[n, j] = True; s.need[n, j] *= s.par["round_need"]
        elif opt in ("light_last", "pause_last"):
            act = np.nonzero((s.st[n] == ACTIVE) & (s.f[n] >= 0))[0]
            if len(act):
                jl = int(act[np.argmax(s.pri[n, act])])
                if opt == "light_last":
                    s.inten[n, jl] = 0.5
                else:
                    s.st[n, jl] = PAUSED

    def activate(s, n, j, inten, t, pay=True):
        """Active at an intensity. The rung's entry cost is paid once, when first committed to (recorded); a pause and a
        resume never charge it again; a refused fee is never charged."""
        f = int(s.f[n, j]); r = int(s.rung[n, j])
        s.st[n, j] = ACTIVE; s.inten[n, j] = float(inten)
        if r < s.F["nr"][f] and pay and not s.paid[n, j, r] and not s.refused[n, j] and s.F["entry"][f, r] > 0:
            e = float(s.F["entry"][f, r]) * (1 - s.par["family_pays"] * (t / 52 < 18))
            s.paid[n, j, r] = True; s.debit[n] += e * s.par["money_k"]
            s.entry_log[n].append(dict(field=s.F["names"][f], rung=r, week=int(t), amount=round(e, 3)))
            s._log(n, j, "entry paid", amount=round(e, 3))
        s.dirty = True

    def set_pace(s, n, j, state, intensity=None, t=None):
        """The player's (or the game's) pace for an aim: state held, active, paused or dropped, and intensity."""
        t = s.t if t is None else t
        if state is None and intensity is None:
            return None
        if state in ("active", ACTIVE) or (state is None and intensity is not None):
            s.activate(n, j, INTENSITY.get(intensity, intensity) if intensity is not None else
                       (float(s.inten[n, j]) if s.st[n, j] == ACTIVE else 1.0), t, pay=True)
        elif state in ("held", HELD):
            s.st[n, j] = HELD
        elif state in ("paused", PAUSED):
            s.st[n, j] = PAUSED
        elif state in ("dropped", DROPPED):
            s.st[n, j] = DROPPED; s._log(n, j, "set aside", learned=round(float(s.learned[n, j].sum()), 2))
        else:
            return f"no state {state!r}"
        s.dirty = True
        return None

    def set_priority(s, n, j, rank):
        """The player's order of the active aims: aim j moves to rank (0 first); the others keep their order."""
        occ = [int(x) for x in np.argsort(s.pri[n], kind="stable") if s.f[n, x] >= 0 and x != j]
        rank = int(max(0, min(rank, len(occ))))
        occ.insert(rank, int(j))
        for i, x in enumerate(occ):
            s.pri[n, x] = float(i)
        s.dirty = True

    # ---- outcomes
    def outcome(s, n, j, t, chance=False):
        """A test (a contest, or a chance taken): success by fit, effort past the need, intensity, kept proficiency and
        luck. Won: the rung is reached and its first title the catalogue can grant is given. Lost: a setback."""
        f = int(s.f[n, j]); r = int(s.rung[n, j])
        if r >= s.F["nr"][f]:
            return False
        x = s.eff[n, j] / max(s.need[n, j], 1e-9) - 1
        p = 0.3 + 0.5 * (s.fitf[n, j] - 1) + 0.15 * min(max(x, 0.0), 2.0) + 0.1 * (s.inten[n, j] - 1) + 0.1 * chance
        p = float(np.clip(p * s.prof[n, j], 0.1, 0.85))
        won = s.rng.random() < p
        s._log(n, j, "test", chance=bool(chance), won=bool(won))
        if won:
            s.arrive(n, j, t, "won " + ("a chance taken" if chance else "a test"), grant=True)
        else:
            s.eff[n, j] = max(0.0, s.eff[n, j] - 0.05 * s.need[n, j])
        return won

    def arrive(s, n, j, t, how, grant=False):
        """The rung is reached through a demonstrated outcome: worked for (active, effort at least half its need, or a
        test won) or came anyway; its title kept for life as an achievement."""
        f = int(s.f[n, j]); r = int(s.rung[n, j]); F = s.F; cx = s.ctx
        worked = bool(grant or (s.st[n, j] == ACTIVE and s.eff[n, j] >= 0.5 * s.need[n, j]))
        s.worked[n, j, r] = 1 if worked else 0
        s.learned[n, j, r] = max(s.learned[n, j, r], 1.0 if worked else min(1.0, s.eff[n, j] / max(s.need[n, j], 1e-9)))
        if grant and len(F["ids"][f][r]):
            i = int(F["ids"][f][r][0])
            cx["r_gain"](n, i, "reached " + F["say"][f][r])
        v1 = int(F["v1"][f]); ak = cx["ak"]
        if s.born[n, j] <= t - 4 and not (v1 >= 0 and ak is not None and (ak[n] == v1).any()):
            h = int(F["h"][f, r]); nd = cx["need"]()
            m = cx["NIDX"]["meaning"]; nd[n, m] += s.par["meet"][h] * (1 - nd[n, m])
        s.rung[n, j] = r + 1
        s._log(n, j, "arrived", say=F["say"][f][r], how=how, worked=worked)
        s.start_rung(n, j, t)

    # ---- the week and the month
    def week(s, t, w, need, res, dead):
        """Effort, learning, windows, outcomes, restoration and strain; returns the week's stress from strain."""
        s.t = t; s.w = w; F = s.F; N = s.N
        if s.debit.any():
            mo = s.ctx["MON"]; res[:, mo] = np.clip(res[:, mo] - s.debit, 0, 1); s.debit[:] = 0
        occ = s.f >= 0
        if not occ.any():
            s.put_arr[:] = -1
            return 0.0
        f = np.maximum(s.f, 0); r = np.minimum(s.rung, F["K"] - 1)
        open_ = occ & (s.rung < F["nr"][f]) & ~dead[:, None]
        tm = F["time"][f, r]
        act = open_ & (s.st == ACTIVE) & ~tm
        blk = s.fork >= 0
        inc = s.funded * s.inten * s.fitf * s.talent * s.prof / 52.0
        e2 = s.eff + inc
        e2 = np.where(blk, np.minimum(e2, np.maximum(s.eff, s.need)), e2)   # a fork waits: effort stops at the need
        s.eff = np.where(act, e2, s.eff)
        rows, cols = np.nonzero(act)
        if len(rows):
            rr = s.rung[rows, cols]
            s.learned[rows, cols, rr] = np.maximum(s.learned[rows, cols, rr], np.minimum(1.0, s.eff[rows, cols] / s.need[rows, cols]))
        use = act & (s.funded > 0)
        s.last_use = np.where(use, t, s.last_use); s.act_wk = np.where(use, s.act_wk + 1, 0)
        # windows: a paused aim's deadline runs on unless the rung says pause_stops (deadline_years only)
        ps = open_ & (s.st == PAUSED) & (s.wclose >= 0) & F["w_pstop"][f, r] & (F["w_dyrs"][f, r] >= 0)
        if ps.any():
            s.wclose = np.where(ps, s.wclose + 1, s.wclose)
        # outcomes: eligible at the need, no fork waiting, the window open (a sitting, the deadline not passed)
        el = act & ~blk & (s.eff >= s.need) & ~s.noaccess
        if el.any():
            ev = F["w_every"][f, r]
            sit = (ev <= 0) | ((t % np.maximum(np.round(ev * 52), 1).astype(int)) < F["w_open"][f, r])
            dl = (s.wclose < 0) | (t <= s.wclose) | s.wround
            el = el & (sit | s.wround) & dl
            rate = F["outy"][f, r] / 52.0
            el = el & (rate > 0)
            rows, cols = np.nonzero(el)
            if len(rows):
                hit = s.rng.random(len(rows)) < rate[rows, cols]
                for n, j in zip(rows[hit], cols[hit]):
                    n, j = int(n), int(j); fj = int(s.f[n, j]); rj = int(s.rung[n, j])
                    if "take" in F["forks"][fj][rj] and not s.declined[n, j]:
                        s.fork_new(n, [j], "take", t, "a chance: " + F["say"][fj][rj])
                    elif F["outy"][fj, rj] > 0 and not (s.declined[n, j] and "take" in F["forks"][fj][rj]
                                                        and not F["outy"][fj, rj] > SHAPE_DEF[SHAPES[F["shape"][fj]]]["chance_y"]):
                        s.outcome(n, j, t)
        # a window about to close: a fork once a rung; closed: told once, never reopened by any state
        wn = act & (s.wclose >= 0) & ~s.wclosed & ~s.wwarn & (s.wclose - t <= s.par["window_warn"]) & (s.eff < s.need) & ~blk & ~s.wround
        for n, j in zip(*np.nonzero(wn)):
            s.wwarn[n, j] = True; s.fork_new(int(n), [int(j)], "window", t, "a window closes soon")
        cl = open_ & (s.wclose >= 0) & (t > s.wclose) & ~s.wclosed & ~s.wround
        for n, j in zip(*np.nonzero(cl)):
            n, j = int(n), int(j)
            s.wclosed[n, j] = True; s.wtold[n, j] = True
            s._log(n, j, "window closed", week_closed=int(s.wclose[n, j]))
            if s.st[n, j] in (ACTIVE, PAUSED, HELD) and s.fork[n, j] < 0:
                s.fork_new(n, [j], "round", t, "the window closed: a way round, or let it go")
        # restoration after the hours are spent (never capacity), and strain from an overfull agenda
        if len(s.F["meets"]) and act.any():
            g = (np.where(act, s.fh, 0.0)[..., None] * F["meets"][f]).sum(1) / 10.0
            need += s.par["restore"] * g * (1 - need)
        st_ = 0.0
        if s.strained.any():
            b = s.ctx["NIDX"]["belonging"]
            need[s.strained, b] = np.maximum(0.0, need[s.strained, b] - s.par["strain"][1])
            st_ = np.where(s.strained, s.par["strain"][0], 0.0)
        return st_

    def month(s, t, ns_, res, held, stress):
        """The account (capacity and funding), rungs reached through their titles, upkeep, the overfull agenda, the
        unattended lives' yearly look at what they hold, integrate outcomes, and the player's forks kept current."""
        s.t = t
        if not (s.f >= 0).any():
            return
        F = s.F; cx = s.ctx; occ = s.f >= 0
        for n, j in zip(*np.nonzero(occ)):
            s.fitf[n, j] = float(np.clip(0.75 + 0.5 * s.fit(int(n), int(s.f[n, j])), 0.4, 1.25))
        s.account(res, held, stress)
        # rungs reached through a title of theirs held (an act, a moment, the world's rules): the demonstrated outcome
        f = np.maximum(s.f, 0)
        op = occ & (s.rung < F["nr"][f])
        if op.any():
            rows, cols = np.nonzero(op)
            fr = f[rows, cols] * F["K"] + s.rung[rows, cols]
            for key in np.unique(fr):
                fi, ri = divmod(int(key), F["K"]); sel = fr == key
                ns, js = rows[sel], cols[sel]
                ids = F["ids"][fi][ri]
                ok = cx["r_ever"][ns][:, ids].any(1) if len(ids) else np.zeros(len(ns), bool)
                if F["req"][fi][ri] is not None and ok.any():
                    ok &= cx["ev_cond"](F["req"][fi][ri], ns_)[ns]
                WL = cx["WL"]() if cx["WON"]() else None
                if F["h"][fi, ri] == 1 and F["sph"][fi] >= 0 and WL is not None and hasattr(WL.PP, "rung"):
                    ok |= np.floor(np.asarray(WL.PP.rung)[ns, F["sph"][fi]]) >= 4   # a work rung: leading the sphere
                for n, j in zip(ns[ok], js[ok]):
                    s.arrive(int(n), int(j), t, "its title held")
        if F["upkeep_any"]:
            s.upkeep(t, held)
        # the overfull agenda: a review (or the character's own pick) once it has lasted over_fork_wk
        for n in np.nonzero(s.over_wk == s.par["over_fork_wk"])[0]:
            act = np.nonzero((s.st[n] == ACTIVE) & occ[n])[0]
            if len(act) >= 2 and not any(x["kind"] == "over" for x in s.forks[n]):
                s.fork_new(int(n), [int(j) for j in act], "over", t, "more is asked of the week than it holds")
        ys = occ & (s.st == HELD) & (s.rung == 0) & (s.fork < 0) & (t / 52 >= F["start"][f, 0]) & ((t - 4) / 52 < F["start"][f, 0])
        for n, j in zip(*np.nonzero(ys)):   # the age interest usually starts: the first step's commitment, a fork
            s.fork_new(int(n), [int(j)], "pay" if F["entry"][f[n, j], 0] > 0 and "pay" in F["forks"][f[n, j]][0] else "go_on",
                       t, "old enough to begin")
        if t % 52 == 0:   # unattended: once a year a held or paused ambition is looked at again (its own odds)
            for n, j in zip(*np.nonzero(occ & ((s.st == HELD) | (s.st == PAUSED)) & (s.fork < 0))):
                n, j = int(n), int(j)
                if n not in s.player and s.rung[n, j] < F["nr"][s.f[n, j]] and not F["time"][s.f[n, j], s.rung[n, j]]:
                    s.fork_new(n, [j], "go_on", t, "a year on")
        if s.asset_tab:
            s.integrate(t)
        for n in s.player:
            if n < s.N and s.forks[n]:
                s.refresh(n)

    def account(s, res, held, stress):
        """The one resource account (contracts.md section 5): what the week holds after work, care, the household,
        ties and the essentials; what money is free after essentials; energy and attention; and the active aims funded
        in their order of priority (shared preparation counted once, a partner's support once, debited from its giver)."""
        from realm_earth import AIM_WEEK as AW
        cx = s.ctx; N = s.N; F = s.F; par = s.par
        TIM, MON = cx["TIM"], cx["MON"]
        WL = cx["WL"]() if cx["WON"]() else None
        PP = WL.PP if WL is not None else None
        hrs = getattr(PP, "hrs", None) if PP is not None else None
        part = held[:, cx["PAR"]]
        if hrs is not None and np.asarray(hrs).shape[0] == N and np.asarray(hrs).sum() > 0:
            h = np.asarray(hrs, float)
            work = h[:, [0, 1, 5, 6, 7]].sum(1); care = h[:, 4]; ties = h[:, 3] + AW["partner"] * part
            have = np.maximum(0.0, AW["wake"] - AW["essentials"] - AW["household"] - work - care - ties)
        else:
            have = AW["free_open"] * res[:, TIM]
            rest = np.maximum(0.0, AW["wake"] - AW["essentials"] - AW["household"] - have)
            ld = held * cx["LOAD"]; tot = np.maximum(ld.sum(1), 1e-9)
            work = rest * np.where(ld.sum(1) > 0, ld[:, cx["CAR"]] / tot, 1.0)
            care = rest * np.where(ld.sum(1) > 0, ld[:, cx["KID"]] / tot, 0.0)
            ties = rest - work - care
        s.before = np.stack([work, care, np.full(N, AW["household"]), ties, np.full(N, AW["essentials"])], 1)
        money = np.clip((res[:, MON] - par["money_floor"]) / (1 - par["money_floor"]), 0, 1)
        child = s.t / 52 < 18
        s.cap["time"] = have; s.cap["money"] = money
        s.cap["energy"] = np.clip(1 - 0.25 * np.asarray(stress), 0.3, 1.0)
        f = np.maximum(s.f, 0); r = np.minimum(s.rung, F["K"] - 1)
        open_ = (s.f >= 0) & (s.rung < F["nr"][f]) & (s.st == ACTIVE) & ~F["time"][f, r]
        dh = np.where(open_, F["hours"][f, r] * s.inten, 0.0)
        dm = np.where(open_, F["money"][f, r] * s.inten * (1 - par["family_pays"] * child), 0.0)
        de = np.where(open_, F["energy"][f, r] * s.inten, 0.0)
        order = np.argsort(np.where(open_, s.pri, np.inf), 1, kind="stable")
        cum_h = np.zeros(N); cum_m = np.zeros(N); seen = np.zeros(N, np.int64)
        sup = np.where(part, par["support_share"], 0.0)   # a partner covers part of the first aim's hours
        s.syn[:] = False; fh = np.zeros_like(dh); fs = np.zeros_like(dh); used_sup = np.zeros(N)
        ar = np.arange(N); first = np.ones(N, bool)
        for q in range(s.MA):
            j = order[:, q]; on = open_[ar, j]
            if not on.any():
                continue
            d = dh[ar, j].copy()
            pm = F["prep"][f[ar, j]]
            shared = on & ((pm & seen) != 0)
            d = np.where(shared, d * (1 - par["prep_share"]), d)
            s.syn[ar[shared], j[shared]] = True
            sp = np.where(on & first, d * sup, 0.0); used_sup += sp; d = d - sp
            gh = np.clip(have - cum_h, 0, d); cum_h += np.where(on, d, 0.0)
            m = dm[ar, j]; gm = np.clip(money - cum_m, 0, m); cum_m += np.where(on, m, 0.0)
            sh = np.where(d > 0, gh / np.maximum(d, 1e-9), 1.0); sm = np.where(m > 0, gm / np.maximum(m, 1e-9), 1.0)
            fs[ar[on], j[on]] = np.minimum(sh, sm)[on]; fh[ar[on], j[on]] = (gh + sp)[on]
            dh[ar[on], j[on]] = (d + sp)[on]
            seen = np.where(on, seen | pm, seen); first = first & ~on
        en = de.sum(1); att = (s.inten * open_).sum(1)
        q_ = np.minimum(1.0, s.cap["energy"] / np.maximum(en, 1e-9)) * np.minimum(1.0, par["attention"] / np.maximum(att, 1e-9))
        s.funded = np.where(open_, fs * q_[:, None], 0.0); s.fh = np.where(open_, fh, 0.0); s.dem = dh
        s.committed["time"] = cum_h; s.committed["money"] = cum_m; s.committed["energy"] = en
        s.committed["attention"] = att; s.committed["support"] = used_sup
        s.committed["access"] = ((s.f >= 0) & (s.wclosed & ~s.wround | s.noaccess)).sum(1).astype(float)
        s.cap["support"] = used_sup
        for n in np.nonzero(used_sup > 0)[0]:
            s.support_log[n] = (s.support_log[n] + [dict(source="partner", hours=round(float(used_sup[n]), 2), week=int(s.t))])[-12:]
        ov = cum_h > par["over"] * have + 1e-9
        s.over_wk = np.where(ov, s.over_wk + 4, 0)
        st0 = s.strained.copy(); s.strained = s.over_wk >= par["strain_wk"]
        for n in np.nonzero(s.strained & ~st0)[0]:
            js = np.nonzero(open_[n])[0]
            if len(js):
                s._log(int(n), int(js[0]), "strain", hours=round(float(cum_h[n]), 1), have=round(float(have[n]), 1))
        s.dirty = False

    def upkeep(s, t, held):
        """Selective upkeep: only a rung that names it; the named part (proficiency, access or a credential's validity)
        lapses after its years without use; the achievement stays recorded; renewed use refreshes it."""
        F = s.F; cx = s.ctx
        for n, j in zip(*np.nonzero(s.f >= 0)):
            n, j = int(n), int(j); f = int(s.f[n, j])
            for r in range(int(s.rung[n, j])):
                if F["up_yrs"][f, r] <= 0:
                    continue
                if F["up_work"][f, r] and held[n, cx["CAR"]]:
                    s.last_use[n, j] = t
                if not s.faded[n, j, r] and t - s.last_use[n, j] > F["up_yrs"][f, r] * 52:
                    s.faded[n, j, r] = True; of = int(F["up_of"][f, r])
                    if of == 0:
                        s.prof[n, j] = 0.8
                    elif of == 1:
                        s.noaccess[n, j] = True
                    else:
                        for i in F["ids"][f][r]:
                            cx["r_lose"](n, int(i), "lapsed")
                    s._log(n, j, "upkeep lapsed", of=("proficiency", "access", "credential")[of], rung_of=r)
                elif s.faded[n, j, r] and s.act_wk[n, j] >= s.par["refresh_wk"]:
                    s.faded[n, j, r] = False; of = int(F["up_of"][f, r])
                    if of == 0:
                        s.prof[n, j] = 1.0
                    elif of == 1:
                        s.noaccess[n, j] = False
                    elif len(F["ids"][f][r]):
                        cx["r_gain"](n, int(F["ids"][f][r][0]), "renewed")
                    s._log(n, j, "upkeep refreshed", of=("proficiency", "access", "credential")[of], rung_of=r)

    def integrate(s, t):
        """An integrate outcome: a life holding rungs in two fields the realm pairs (AIM_ASSETS), one of them active,
        shows them used together (a test of both): the asset, once per pair a life (never again by switching aims)."""
        F = s.F
        for n in np.nonzero(((s.f >= 0) & (s.rung >= 1)).sum(1) >= 2)[0]:
            js = [int(j) for j in np.nonzero((s.f[n] >= 0) & (s.rung[n] >= 1))[0]]
            for a in range(len(js)):
                for b in range(a + 1, len(js)):
                    ja, jb = js[a], js[b]
                    fa, fb = int(s.f[n, ja]), int(s.f[n, jb])
                    for key in (tuple(sorted((F["names"][fa], F["names"][fb]))), tuple(sorted((SHAPES[F["shape"][fa]], SHAPES[F["shape"][fb]])))):
                        x = s.asset_tab.get(key)
                        if x is None or key in s.awarded[n]:
                            continue
                        ra, rb = x.get("rungs", (1, 1))
                        if s.rung[n, ja] < ra or s.rung[n, jb] < rb or not (s.st[n, ja] == ACTIVE or s.st[n, jb] == ACTIVE):
                            continue
                        if s.rng.random() >= s.par["integrate_y"] * 4 / 52:
                            continue
                        p = float(np.clip(0.3 + 0.25 * (s.fitf[n, ja] + s.fitf[n, jb] - 2), 0.1, 0.8))
                        if s.rng.random() >= p:
                            continue
                        s.awarded[n].add(key)
                        rec = dict(name=x.get("name", " and ".join(key)), pair=list(key), week=int(t), opens=x.get("opens", ""),
                                   slots=[ja, jb])
                        s.assets[n].append(rec)
                        tt = x.get("title") or ""
                        if tt and tt in s.ctx["RID"]:
                            s.ctx["r_gain"](int(n), int(s.ctx["RID"][tt]), "an integrated asset")
                        s._log(int(n), ja, "integrated asset", asset=rec["name"], pair=list(key))

    # ---- the player's forks: kept current, grouped by a shared bottleneck, put one a week
    def _facts(s, n, fk):
        j = fk["aims"][0]
        f = int(s.f[n, j]); r = int(min(s.rung[n, j], s.F["nr"][f] - 1))
        room = s.cap["time"][n] - s.committed["time"][n] + (s.dem[n, j] if s.st[n, j] == ACTIVE else 0.0)
        return (bool(room >= s.F["hours"][f, r]), int(s.wclose[n, j]), bool(s.wclosed[n, j]), int(s.rung[n, j]),
                bool(s.can_pay(n, j)), int(s.st[n, j]))

    def refresh(s, n):
        """A pending fork whose facts changed (a cost, a deadline, what the week holds) is rebuilt with the new facts and
        options; forks sharing a real bottleneck are grouped into one agenda review."""
        for fk in s.forks[n]:
            fk["aims"] = [j for j in fk["aims"] if s.f[n, j] >= 0]
            fa = s._facts(n, fk)
            if fa != fk["facts"]:
                fk["facts"] = fa; fk["changed"] = True
                fk["preview"] = s.preview(n, fk["aims"][0]); fk["options"] = s.options(n, fk["aims"][0], fk["kind"]) + ["later"]
            j = fk["aims"][0]
            fk["urgent"] = bool(s.wclose[n, j] >= 0 and not s.wclosed[n, j] and s.wclose[n, j] - s.t <= s.par["window_warn"])
        over = s.committed["time"][n] > s.cap["time"][n] + 1e-9
        keys = {}
        for fk in s.forks[n]:
            j = fk["aims"][0]; f = int(s.f[n, j]); r = int(min(s.rung[n, j], s.F["nr"][f] - 1))
            k = None
            if fk["kind"] == "over" or (over and fk["kind"] in ("go_on", "pay", "window") and s.F["hours"][f, r] > 0):
                k = "time"
            elif fk["kind"] in ("window", "round") and s.wclose[n, j] >= 0:
                k = "window:%d" % (int(s.wclose[n, j]) // 13)
            fk["group"] = k; keys[k] = keys.get(k, 0) + 1
        for fk in s.forks[n]:
            fk["grouped"] = bool(fk["group"] is not None and keys[fk["group"]] >= 2)

    def put(s, t):
        """At the situation pause: the one fork (or agenda review) put this week to each player life, replacing its
        next optional ask: the most urgent unresolved one not put in the last reask weeks unless its facts changed."""
        s.put_arr[:] = -1
        for n in s.player:
            if n >= s.N or not s.forks[n]:
                continue
            c = [fk for fk in s.forks[n] if fk["put"] < 0 or fk["changed"] or t - fk["put"] >= s.par["reask"]]
            if not c:
                continue
            def key(fk):
                j = fk["aims"][0]
                wc = int(s.wclose[n, j]) if s.wclose[n, j] >= 0 and not s.wclosed[n, j] else 10 ** 9
                return (not fk["urgent"], wc, ("window", "pay", "take", "round", "over", "go_on").index(fk["kind"])
                        if fk["kind"] in ("window", "pay", "take", "round", "over", "go_on") else 9, fk["week"], fk["id"])
            fk = min(c, key=key)
            grp = [x for x in s.forks[n] if fk["grouped"] and x["group"] == fk["group"]] or [fk]
            for x in grp:
                x["put"] = t; x["changed"] = False
            s.put_arr[n] = fk["id"]
            s.burden.append(dict(what="put", life=int(n), week=int(t), id=fk["id"], forks=len(grp),
                                 aims=len({j for x in grp for j in x["aims"]}), options=sum(len(x["options"]) for x in grp)))

    # ---- views (the Game's; draw nothing, cost no time)
    def preview(s, n, j=None, f=None, r=None):
        """What is known before a commitment, from the life's own state (never a simulated future): the step's
        requirements, one-time and ongoing costs, the window, the overlap with other aims and with care and ties in
        the one account, what is uncertain (in words and ranges), and what pausing or letting go keeps and costs."""
        F = s.F
        if j is not None:
            f = int(s.f[n, j]); r = int(s.rung[n, j]) if r is None else r
        r = int(min(r if r is not None else 0, F["nr"][f] - 1))
        it = F["items"][f]; t = s.t
        inten = float(s.inten[n, j]) if j is not None and s.st[n, j] == ACTIVE else 1.0
        hrs = float(F["hours"][f, r]); mon = float(F["money"][f, r]); ent = float(F["entry"][f, r])
        paid = bool(j is not None and s.paid[n, j, r])
        have = float(s.cap["time"][n]); used = float(s.committed["time"][n])
        mine = float(s.dem[n, j]) if j is not None and s.st[n, j] == ACTIVE else 0.0
        room = have - (used - mine)
        others = []
        for k in np.nonzero((s.f[n] >= 0) & (s.st[n] == ACTIVE))[0]:
            if j is not None and k == j:
                continue
            fk = int(s.f[n, k]); rk = int(min(s.rung[n, k], F["nr"][fk] - 1))
            sh = bool(F["prep"][fk] & F["prep"][f])
            others.append(dict(slot=int(k), field=F["names"][fk], hours=round(float(F["hours"][fk, rk] * s.inten[n, k]), 1),
                               shares_prep=sh))
        bf = dict(zip(CAPACITY_BEFORE, (round(float(x), 1) for x in s.before[n])))
        win = None
        if j is not None and s.wclose[n, j] >= 0:
            win = dict(closes_age=round(int(s.wclose[n, j]) / 52, 2), closed=bool(s.wclosed[n, j]),
                       pause_stops=bool(F["w_pstop"][f, r]))
        elif F["w_every"][f, r] > 0:
            win = dict(every_years=float(F["w_every"][f, r]), open_weeks=int(F["w_open"][f, r]))
        elif F["w_dage"][f, r] >= 0:
            win = dict(closes_age=float(F["w_dage"][f, r]), closed=bool(t / 52 > F["w_dage"][f, r]))
        unk = ["whether a test or a chance will go their way", "how the people close to them will take it"]
        if F["share"][f, r] < 0.5:
            unk.append("most who keep at this step never reach it")
        needs = ["to reach: " + F["say"][f][r]] + ["one of: " + ", ".join(F["tnames"][f][r][:3])] if F["tnames"][f][r] else []
        req = it["rungs"][r].get("req_s") or ""
        if req:
            needs.append("the world's condition: " + req)
        if not needs:
            needs = ["to reach: " + F["say"][f][r]]
        over = [int(o["slot"]) for o in others if room < hrs * inten]
        over += [k for k in ("work", "care", "ties") if room < hrs * inten and bf.get(k, 0) > 0]
        wd = None
        if win is not None and "closes_age" in win:
            wd = dict(opens=round(int(s.rstart[n, j]) / 52, 2) if j is not None else round(t / 52, 2),
                      closes=win["closes_age"], closed=win.get("closed", False), pause_stops=win.get("pause_stops", False))
        elif win is not None:
            wd = dict(opens=None, closes=None, every_years=win["every_years"], open_weeks=win["open_weeks"])
        ex = ("they can pause and keep what they learned; " + ("an entry paid is not charged again" if ent else "nothing is owed") +
              ("; the deadline runs on while paused" if wd and wd.get("closes") is not None and not wd.get("pause_stops") else "") +
              "; letting it go keeps the learning and the people met, " + ("the fee is not returned" if ent else "and costs nothing more"))
        return dict(field=F["names"][f], step=F["say"][f][r], rung=r, needs=needs,
                    cost=dict(entry=round(ent, 3), paid=paid, viable=bool(s.cap["money"][n] >= 0.5 * ent) if ent else True,
                              money=(round(mon * 0.5, 3), round(mon * 1.5, 3))),
                    hours=(round(hrs * 0.5, 1), round(hrs * 1.5, 1)), hours_now=round(hrs * inten, 1), room=round(room, 1),
                    funded=bool(room >= hrs * inten),
                    years=dict(typical=float(F["ymed"][f, r]), range=(float(F["ylo"][f, r]), float(F["yhi"][f, r])),
                               confirmed=False),
                    overlaps=over, overlap_aims=others, before=bf, window=wd, unknown=unk, time=bool(F["time"][f, r]),
                    exit=dict(say=ex))

    def item(s, n, j):
        """aims-shape.md section 6: one aim of S["aim2"]."""
        F = s.F; f = int(s.f[n, j]); r = int(s.rung[n, j]); nr = int(F["nr"][f]); rr = min(r, nr - 1)
        done = r >= nr; t = s.t
        frac = 1.0 if done else float(min(1.0, s.eff[n, j] / max(s.need[n, j], 1e-9)))
        fd = float(s.funded[n, j])
        left = None if done or s.st[n, j] != ACTIVE else round(max(0.0, F["ymed"][f, rr] * (1 - frac)) / max(fd * s.inten[n, j], 0.05), 1)
        bn = ""
        if not done:
            if s.fork[n, j] >= 0:
                bn = "a fork"
            elif s.wclosed[n, j] and not s.wround[n, j]:
                bn = "a window"
            elif s.noaccess[n, j]:
                bn = "a door"
            elif s.st[n, j] == ACTIVE and fd < 0.999:
                c = F["money"][f, rr] > 0 and s.committed["money"][n] > s.cap["money"][n]
                bn = "money" if c else "time"
            elif s.st[n, j] == ACTIVE and s.eff[n, j] >= s.need[n, j]:
                bn = "a door" if F["outy"][f, rr] <= 0 else ""
        win = None
        if s.wclose[n, j] >= 0:
            win = dict(opens=round(int(s.rstart[n, j]) / 52, 2), closes=round(int(s.wclose[n, j]) / 52, 2))
        return dict(slot=int(j), field=F["names"][f], shape=SHAPES[F["shape"][f]], state=STATES[int(s.st[n, j])],
                    intensity=float(s.inten[n, j]), priority=float(s.pri[n, j]), rung=r, of=nr,
                    say=None if done else F["say"][f][r], effort=round(float(s.eff[n, j]), 3),
                    need=round(float(s.need[n, j]), 3), frac=round(frac, 3), funded=round(fd, 3), years_left=left,
                    window=win, demand=dict(hours=float(F["hours"][f, rr]), money=float(F["money"][f, rr]),
                                            entry=float(F["entry"][f, rr])),
                    paid=[bool(x) for x in s.paid[n, j, :nr]], learned=[round(float(x), 3) for x in s.learned[n, j, :nr]],
                    by_player=bool(s.by[n, j]), late=bool(s.born[n, j] / 52 > F["start"][f, 2]),
                    worked=[int(x) for x in s.worked[n, j, :nr]], time=bool(not done and F["time"][f, r]),
                    assets=[a["name"] for a in s.assets[n] if j in a["slots"]], bottleneck=bn,
                    upkeep=[dict(rung=k, lapsed=bool(s.faded[n, j, k])) for k in range(min(r, nr)) if F["up_yrs"][f, k] > 0],
                    shared_prep=bool(s.syn[n, j]), fork=int(s.fork[n, j]))

    def items(s, n):
        return [s.item(n, int(j)) for j in np.nonzero(s.f[n] >= 0)[0]]

    def account_view(s, n):
        """contracts.md section 5: each resource dict(have, committed, items)."""
        F = s.F; out = {}
        act = [int(j) for j in np.nonzero((s.f[n] >= 0) & (s.st[n] == ACTIVE))[0]]
        nm = lambda j: dict(slot=j, field=F["names"][int(s.f[n, j])])
        out["time"] = dict(have=round(float(s.cap["time"][n]), 1), committed=round(float(s.committed["time"][n]), 1),
                           before={k: round(float(v), 1) for k, v in zip(CAPACITY_BEFORE, s.before[n])},
                           items=[dict(nm(j), hours=round(float(s.dem[n, j]), 1), funded=round(float(s.fh[n, j]), 1),
                                       shared_prep=bool(s.syn[n, j])) for j in act])
        out["money"] = dict(have=round(float(s.cap["money"][n]), 3), committed=round(float(s.committed["money"][n]), 3),
                            items=[dict(nm(j), year=round(float(F["money"][int(s.f[n, j]), min(int(s.rung[n, j]), F["nr"][int(s.f[n, j])] - 1)] * s.inten[n, j]), 3)) for j in act],
                            entries=list(s.entry_log[n]))
        out["energy"] = dict(have=round(float(s.cap["energy"][n]), 2), committed=round(float(s.committed["energy"][n]), 2), items=[nm(j) for j in act])
        out["attention"] = dict(have=float(s.par["attention"]), committed=round(float(s.committed["attention"][n]), 2),
                                items=[nm(j) for j in act])
        out["access"] = dict(have=len(act), committed=int(s.committed["access"][n]),
                             items=[nm(int(j)) for j in np.nonzero((s.f[n] >= 0) & ((s.wclosed[n] & ~s.wround[n]) | s.noaccess[n]))[0]])
        out["support"] = dict(have=round(float(s.cap["support"][n]), 2), committed=round(float(s.committed["support"][n]), 2),
                              items=list(s.support_log[n][-3:]))
        out["over"] = bool(s.committed["time"][n] > s.cap["time"][n] + 1e-9); out["strained"] = bool(s.strained[n])
        return out

    def output(s):
        return dict(fields=list(s.F["names"]), src=s.F["src"], log=s.log, burden=s.burden, decisions=s.decisions,
                    field=s.f.copy(), state=s.st.copy(), rung=s.rung.copy(), learned=s.learned.copy(),
                    worked=s.worked.copy(), paid=s.paid.copy(), assets=[list(a) for a in s.assets],
                    open_forks=[[dict(id=x["id"], kind=x["kind"], aims=list(x["aims"]), week=x["week"]) for x in fl] for fl in s.forks],
                    entries=[list(e) for e in s.entry_log])


class View:
    """S["aim2"] and S["capacity"]: per person, read when asked (nothing is built at a pause the game does not read)."""
    __slots__ = ("ag", "fn")

    def __init__(s, ag, fn):
        s.ag = ag; s.fn = fn

    def __getitem__(s, n):
        return getattr(s.ag, s.fn)(int(n))

    def __len__(s):
        return s.ag.N
