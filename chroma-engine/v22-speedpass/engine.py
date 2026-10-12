"""Chroma engine prototype, v2 (concept check, not a product).

Changes from v1 (see engine_v1.py), following Emren's direction answers:
  * five shared human needs (safety, belonging, autonomy, competence, meaning),
    each met by several colors through NEED_MAP
  * ally/enemy tension is no longer built in: a `framing` matrix says how a
    world or culture interprets the relation between colors (neutral by default)
  * holding one dominant color has an upkeep cost that grows with concentration
  * life stages entered through rites of passage inside age windows; a rite
    consolidates the core identity (a lasting imprint) and stage, not age, sets plasticity

v3 (Emren, 2026-10-04: "preferences and availabilities are two different things";
colors can fail to shift even when the person wants them to):
  * a decision passes four gates: the world makes an option AVAILABLE (access through
    the niche), the mindset NOTICES it (deep core k), the person PREFERS it (aspiration a,
    what they consciously want) or is PULLED to it (current motives w and habit), and
    executive CONTROL (by stage, eroded by stress) decides which of the last two wins
  * unmet needs, norms and role models shape what a person wants (aspiration), not who
    they are; motives change only through what they actually do and live through

Vectorised over N independent lives. One tick = one week. Every life starts at 0.2 per color.
"""
import os
import re
import sys
from collections import namedtuple
import numpy as np
try:   # speed pass: np.clip's own ufunc, called without its Python wrapper (the same numbers)
    from numpy._core.umath import clip as _uclip
except ImportError:
    from numpy.core.umath import clip as _uclip
try:   # the outer world's key words (world_keys.py beside this file)
    import world_keys as WKEYS
except ImportError:   # pragma: no cover
    WKEYS = None
from library import COLORS, SITUATIONS, IMPOSITIONS, STAGES, NEEDS, NEED_MAP, NEED_MAP_V6, RESOURCES, COMMITMENTS, SOURCES, EVENTS, ERA_KINDS, DUTIES
from library import DREAM_TRIGGERS
from combos import IDEAS, ERA_COMBOS

C = 5
NJ = len(NEEDS)
IDX = {c: i for i, c in enumerate(COLORS)}
NIDX = {n: i for i, n in enumerate(NEEDS)}
NMAP_V5 = np.array(NEED_MAP, float)       # needs x colors
NMAP_V6 = np.array(NEED_MAP_V6, float)    # v6: autonomy is met by acting as oneself, not by a color
NMAP = NMAP_V6
STAGE_NAMES = [s[0] for s in STAGES]
STAGE_LO = np.array([s[1][0] for s in STAGES], float)
STAGE_HI = np.array([s[1][1] for s in STAGES], float)
STAGE_P = np.array([s[2] for s in STAGES], float)
NS = len(STAGES)
NR = len(RESOURCES); RIDX = {r: i for i, r in enumerate(RESOURCES)}
NK = len(COMMITMENTS); KIDX = {c[0]: i for i, c in enumerate(COMMITMENTS)}
KNAMES = [c[0] for c in COMMITMENTS]
CTX = ["family", "ties", "money", "health", "era", "harsh", "unrest", "prosper", "community", "stress",
       "trouble", "fortune"]   # v6 event drivers; trouble and fortune are the person's own recent record (loss and gain spirals)
CIDX = {c: i for i, c in enumerate(CTX)}


# ---------- the pie's geometry (W U B R G in a circle), used only to BUILD framings
def pie_relation():
    A = np.zeros((C, C))
    for i in range(C):
        for j in range(C):
            d = min((i - j) % C, (j - i) % C)
            A[i, j] = {0: 0, 1: 1, 2: -1}[d]
    return A
A = pie_relation()
ALLY = (A > 0).astype(float)
ENEMY = (A < 0).astype(float)

# A framing is how a world or culture reads the relation between two value families:
# > 0 seen as opposed (holding both creates tension), < 0 seen as reinforcing.
FRAMINGS = {
    "neutral": np.zeros((C, C)),
    "pie": ENEMY - 0.4 * ALLY,   # the Magic color pie taken literally
}


# The five enemy axes from Wizards' own writing ("Pie Fights", 2016; "Thank You for Being a Friend", 2017).
# Each axis is one shared question with two answers; the two allies of each side lean the same way,
# and the color allied to both sides stays out. (+1 = first answer, -1 = second, 0 = not part of it)
AXES = {                          #  W   U   B   R   G
    "group vs individual":         [+1,  0, -1, -1, +1],
    "security vs freedom":         [+1, +1, -1, -1,  0],
    "head vs heart":               [+1, +1,  0, -1, -1],
    "destiny vs free will":        [+1, -1, -1,  0, +1],
    "nature vs nurture":           [ 0, -1, -1, +1, +1],
}


def framing_from_axes(salience, bond=1.0):
    """How a world reads color relations, built from how salient each axis is in it, e.g.
    {"security vs freedom": 1.0}. Colors on opposite sides of a salient axis feel tension; colors on
    the same side reinforce each other (bond). All five axes at 1 reproduces Magic's pie."""
    F = np.zeros((C, C))
    for ax, sx in salience.items():
        v = np.array(AXES[ax], float)
        o = np.outer(v, v)
        F += sx * (np.where(o < 0, 1.0, 0.0) - bond * np.where(o > 0, 1.0, 0.0))
    np.fill_diagonal(F, 0)
    return F / 3.0


FRAMINGS["axes"] = framing_from_axes({k: 1.0 for k in AXES})   # the same pie, derived from the five axes
FRAMINGS["mild"] = framing_from_axes({k: 0.3 for k in AXES})   # v6 default world (Emren 22:46): mild tension on all five questions


def framing_from_pairs(spec):
    """Custom framing, e.g. {'WR': 1.0, 'UG': -0.5} (order vs freedom opposed; science and nature reinforcing)."""
    F = np.zeros((C, C))
    for pair, val in spec.items():
        i, j = IDX[pair[0]], IDX[pair[1]]
        F[i, j] = F[j, i] = val
    return F


def parse(s, index=IDX, n=C):
    v = np.zeros(n)
    if not s:
        return v
    for tok in s.split():
        k = 0
        while k < len(tok) and (tok[k].isalpha() or tok[k] == "_"):
            k += 1
        key, num = tok[:k], tok[k:]
        v[index[key]] += float(num) if num not in ("", "+", "-") else 1.0
    return v


DUTY = np.array([parse(DUTIES.get(k, ""), NIDX, NJ) for k in KNAMES])      # v6: commitments x needs of those it serves


def parse_tags(tag):
    """'req:money.3 time.2; win:money+.2; commit:career' -> dict of resource vectors and commitment index."""
    out = {k: np.zeros(NR) for k in ("req", "pay", "win", "lose")}; out["commit"] = -1
    for part in (tag or "").split(";"):
        part = part.strip()
        if not part:
            continue
        key, val = part.split(":")
        if key == "commit":
            out["commit"] = KIDX[val.strip()]
        else:
            out[key] = parse(val, RIDX, NR)
    return out


def kind_or_none(name):
    return KIDX[name] if name else -1


# ---------- compile library into padded arrays
DIHEDRAL = [[(i + r) % C for i in range(C)] for r in range(C)] + \
           [[(r - i) % C for i in range(C)] for r in range(C)]


def perm_inv(p):
    inv = [0] * C
    for i, j in enumerate(p):
        inv[j] = i
    return inv


# v7 library format (Library spec, sections 2 and 7): what an act leaves in a person's history (marks, for echoes),
# who can die in a life event (kills), and the kinds of closed options (pickable, with a backfire)
MARK_BASE = ["hid a wrong", "owned up", "kept your word", "broke your word", "learned a skill", "took a wild risk",
             "left home", "stayed home", "moved away", "turned down a chance", "helped someone in need",
             "refused someone in need", "made an enemy", "made a friend", "defied an authority", "gave in to pressure",
             "named their gender"]   # N1b: beside the Library's came out (chroma-identity/for-the-engine.md §2)
ROLES = ["parent", "sibling", "friend", "grandparent", "partner", "child"]   # child: only ever by illness or accident (R15)
CLOSED_KINDS = ["law", "approval", "means"]
CLOSED_UNKNOWN = []   # closed: kinds the compile did not know (read as approval); CHROMA_STRICT=1 makes them an error
TIERS = ["everyday", "life event", "inner", "echo", "engine"]
TAGS4 = ["habit", "door", "identity", "binds"]


# v23 life domains (Emren 10-04: "coefficients on the current color allocation; the deep core stays one, with modifiers per
# domain (work, home, friends, faith...)"). A moment's area: the Library's area: mark, else its first life: tag that names one.
AREAS = ["work", "home", "friends", "faith"]
AREA_OF_LIFE = {"work": 0, "school": 0, "study": 0, "learning": 0, "family": 1, "home": 1, "love": 1, "children": 1,
                "partner": 1, "loss": 1, "care": 1, "friends": 2, "community": 2, "play": 2, "leisure": 2, "sport": 2,
                "neighbours": 2, "a team": 2, "a choir": 2, "volunteering": 2, "faith": 3, "tradition": 3}


def area_of(s):
    """The life area a moment belongs to (index in AREAS), or -1 for the core (alone, the body, money, the world)."""
    a_ = str(s.get("area", "") or "").strip()
    if a_:
        return AREAS.index(a_) if a_ in AREAS else -1
    for t_ in str(s.get("life", "") or "").split(","):
        if t_.strip() in AREA_OF_LIFE:
            return AREA_OF_LIFE[t_.strip()]
    return -1


def compile_library(symmetric=False, situations=None):
    """symmetric=True adds all 10 rotations/reflections of the pie, so situation
    CONTENT favours no color. Used to test the engine rather than the library.
    situations: a list of situation dicts (a Library batch); default the seed library."""
    if symmetric:
        base = compile_library(False, situations)
        out = {}
        for key in ("M", "E", "ALPHA"):
            out[key] = np.concatenate([base[key][..., perm_inv(p)] for p in DIHEDRAL], 0)
        for key in ("DIFF", "MASK", "STAKES", "STG", "RIT", "OVR", "REQ", "PAY", "WIN", "LOSE", "COMMIT", "NEEDK", "EXCLK", "DOM", "RATE", "AGE", "DRV",
                    "TIER", "ONCE", "ONCE_K", "KILLS", "ENDS", "MOVES", "MARK", "CLOSED", "BODY", "TAG", "HEDON", "SC", "AREA"):
            out[key] = np.concatenate([base[key]] * 10, 0)
        out["PERY"] = np.concatenate([base["PERY"] / 10] * 10, 0)      # ten copies of each life event share its base rate
        out["OID"] = np.concatenate([base["OID"] + i * base["NOPT"] for i in range(10)], 0)
        out.update(NOPT=base["NOPT"] * 10, labels=base["labels"] * 10, names=base["names"] * 10, src=base["src"] * 10,
                   notes=base["notes"] * 10, K=base["K"], S=base["S"] * 10, IMP=base["IMP"], RECON=base["RECON"], MARKS=base["MARKS"])
        return out
    SITUATIONS_ = SITUATIONS if situations is None else situations
    S = len(SITUATIONS_)
    K = max(len(s["options"]) for s in SITUATIONS_) + 1  # +1 = "do nothing"
    marks = list(MARK_BASE) + sorted({o[5]["mark"] for s in SITUATIONS_ for o in s["options"]
                                      if len(o) > 5 and isinstance(o[5], dict) and o[5].get("mark") and o[5]["mark"] not in MARK_BASE})
    TIER = np.array([TIERS.index(s.get("tier", "everyday" if not s.get("per_year") else "life event"))
                     if s.get("tier", "everyday") in TIERS else 0 for s in SITUATIONS_])
    ONCE = np.array([bool(s.get("once")) for s in SITUATIONS_])
    ONCE_K = np.array([kind_or_none(s.get("needs")) if s.get("once") else -1 for s in SITUATIONS_])   # once per commitment held
    KILLS = np.array([ROLES.index(s["kills"].strip()) if s.get("kills") else -1 for s in SITUATIONS_])
    ENDS = np.array([kind_or_none(s.get("ends", "").strip() or None) for s in SITUATIONS_])
    MOVES = np.array([bool(s.get("moves")) for s in SITUATIONS_])
    AREA = np.array([area_of(s) for s in SITUATIONS_], int)
    MARK = np.full((S, K), -1); CLOSED = np.full((S, K), -1); BODY = np.zeros((S, K)); TAG = np.zeros((S, K, 4), bool)
    HEDON = np.zeros((S, K), bool); notes = []
    SC = np.zeros((S, K))                     # v7: self_control "+" (a promise kept, holding on, saving up) or "-" (giving in, giving up)
    M_ = np.zeros((S, K, C)); E_ = np.zeros((S, K, C)); DIFF = np.zeros((S, K))
    MASK = np.zeros((S, K), bool); OVR = np.zeros((S, K), bool)
    ALPHA = np.zeros((S, C)); STAKES = np.zeros(S); STG = np.zeros((S, NS), bool); RIT = np.zeros((S, NS), bool)
    OID = np.zeros((S, K), int); labels = []; names = []
    REQ = np.zeros((S, K, NR)); PAY = np.zeros((S, K, NR)); WIN = np.zeros((S, K, NR)); LOSE = np.zeros((S, K, NR))
    COMMIT = np.full((S, K), -1); NEEDK = np.full(S, -1); EXCLK = np.full(S, -1); DOM = np.zeros((S, NK)); RATE = np.ones(S)
    AGE = np.zeros((S, 2)); PERY = np.zeros((S, NS)); DRV = np.zeros((S, len(CTX)))
    oid = 0
    for si, s in enumerate(SITUATIONS_):
        ALPHA[si] = parse(s["alpha"]); STAKES[si] = s["stakes"]
        NEEDK[si] = kind_or_none(s.get("needs")); EXCLK[si] = kind_or_none(s.get("excludes"))
        DOM[si] = parse(s.get("domain", ""), KIDX, NK); RATE[si] = s.get("rate", 1.0); AGE[si] = s["age"]
        PERY[si] = s.get("per_year", (0,) * NS); DRV[si] = parse(s.get("drivers", ""), CIDX, len(CTX))
        for st in s["stages"].split():
            STG[si, STAGE_NAMES.index(st)] = True
        for st in s.get("rite", "").split():
            RIT[si, STAGE_NAMES.index(st)] = True
        row = []; nrow = []
        for ki, (lab, means, ends, diff, *tag) in enumerate(s["options"]):
            tg = parse_tags(tag[0] if tag else "")
            nt = tag[1] if len(tag) > 1 and isinstance(tag[1], dict) else {}
            nrow.append(nt)
            if nt.get("mark"):
                MARK[si, ki] = marks.index(nt["mark"])
            if nt.get("closed"):   # "closed: <kind>[: why]"; a kind run into the next words ("law; backfire: ...") reads as its kind
                kd = nt["closed"].replace(";", ":").replace("|", ":").split(":")[0].strip()
                if kd not in CLOSED_KINDS:   # checklist L1: an unknown kind no longer passes silently as approval
                    msg_ = f"closed: unknown kind {kd!r} in {s.get('name', si)!r}, option {ki + 1} (known: {', '.join(CLOSED_KINDS)})"
                    if os.environ.get("CHROMA_STRICT"):
                        raise ValueError(msg_)
                    CLOSED_UNKNOWN.append(msg_)
                    if len(CLOSED_UNKNOWN) <= 20:
                        print("WARNING " + msg_, file=sys.stderr)
                CLOSED[si, ki] = CLOSED_KINDS.index(kd) if kd in CLOSED_KINDS else 1
            BODY[si, ki] = {"light": 0.5, "heavy": 1.0}.get(nt.get("body"), 0.0)
            TAG[si, ki] = [bool(nt.get(k_)) for k_ in TAGS4]
            HEDON[si, ki] = "hedonism" in str(nt.get("v", "")) or "stimulation" in str(nt.get("v", ""))
            SC[si, ki] = {"+": 1.0, "-": -1.0}.get(str(nt.get("self_control", "")).strip(), 0.0)
            REQ[si, ki], PAY[si, ki], WIN[si, ki], LOSE[si, ki] = tg["req"], tg["pay"], tg["win"], tg["lose"]
            COMMIT[si, ki] = tg["commit"]
            m = parse(means); m = m / m.sum()
            M_[si, ki] = m; DIFF[si, ki] = diff; MASK[si, ki] = True
            E_[si, ki] = parse(ends) if ends else 0.7 * m   # framing adds opposition at run time
            OVR[si, ki] = bool(ends)
            OID[si, ki] = oid; oid += 1; row.append(lab)
        ki = len(s["options"])
        M_[si, ki] = 0.2; MASK[si, ki] = True; OVR[si, ki] = True
        OID[si, ki] = oid; oid += 1; row.append("do nothing")
        labels.append(row); names.append(s["name"]); notes.append(nrow)
    IMP = np.array([parse(e, NIDX, NJ) for _, e in IMPOSITIONS])
    return dict(M=M_, E=E_, DIFF=DIFF, MASK=MASK, OVR=OVR, ALPHA=ALPHA, STAKES=STAKES,
                STG=STG, RIT=RIT, OID=OID, NOPT=oid, labels=labels, names=names, K=K, S=S, IMP=IMP,
                REQ=REQ, PAY=PAY, WIN=WIN, LOSE=LOSE, COMMIT=COMMIT, NEEDK=NEEDK, EXCLK=EXCLK, DOM=DOM, RATE=RATE, AGE=AGE, PERY=PERY, DRV=DRV,
                RECON=names.index("reconsidering a commitment"),
                TIER=TIER, ONCE=ONCE, ONCE_K=ONCE_K, KILLS=KILLS, ENDS=ENDS, MOVES=MOVES, MARK=MARK, CLOSED=CLOSED, BODY=BODY, TAG=TAG,
                HEDON=HEDON, SC=SC, AREA=AREA, MARKS=marks, src=list(SITUATIONS_), notes=notes)


LIB = compile_library()


# ---------- the outside world (v4): events that happen to a person, and the eras a society lives through
def compile_events():
    E = dict(names=[e[0] for e in EVENTS], src=np.array([SOURCES.index(e[1]) for e in EVENTS]),
             kind=[], mix=np.zeros((len(EVENTS), C)), s=np.array([e[3] for e in EVENTS], float),
             rate=np.array([e[4] for e in EVENTS], float) / 52, need=np.zeros((len(EVENTS), NJ)),
             res=np.zeros((len(EVENTS), NR)), move=np.zeros(len(EVENTS), bool), door=np.zeros(len(EVENTS), bool))
    for j, (_, _, msg, _, _, eff) in enumerate(EVENTS):
        if msg in ("random", "niche", "faith", "none"):
            E["kind"].append(msg)
        else:
            E["kind"].append("fixed"); E["mix"][j] = parse(msg); E["mix"][j] /= E["mix"][j].sum()
        for tok in eff.split():
            if tok == "move": E["move"][j] = True
            elif tok == "door": E["door"][j] = True
            else:
                key, val = tok.split(":")
                if key == "need": E["need"][j] += parse(val, NIDX, NJ)
                else: E["res"][j] += parse(val, RIDX, NR)
    E["kind"] = np.array(E["kind"])
    return E
EV = compile_events()
COMBO_MIX = {k: np.array([1.0 / len(k) if c in k else 0.0 for c in COLORS]) for k in ERA_COMBOS}


def bound_logratios(z, lo, hi):
    """Emren's color bounds (2026-10-04): unless a setting says otherwise, nobody is fully one color and nobody loses a
    color entirely. Rows whose weights leave [lo, hi] are projected back by scaling the free colors together (their
    ratios are kept), so the person keeps their shape and only the extreme is trimmed."""
    w = softmax(z)
    bad = (w.max(1) > hi) | (w.min(1) < lo)
    if not bad.any():
        return z
    wb = w[bad]; a = np.zeros(len(wb)); b = np.full(len(wb), 1.0 / lo)
    for _ in range(40):                                   # find the scale s with sum(clip(s * w, lo, hi)) = 1
        s_ = (a + b) / 2
        tot = np.clip(s_[:, None] * wb, lo, hi).sum(1)
        a = np.where(tot < 1, s_, a); b = np.where(tot >= 1, s_, b)
    wn = np.clip(((a + b) / 2)[:, None] * wb, lo, hi); wn /= wn.sum(1, keepdims=True)
    z = z.copy(); z[bad] = centre(np.log(wn))
    return z


def random_messages(rng, n):
    """n random color messages: 1, 2 or 3 colors drawn evenly (enemy pairs and wedges as likely as allies)."""
    out = np.zeros((n, C))
    ks = rng.choice([1, 2, 3], size=n, p=[0.3, 0.4, 0.3])
    for i, kk in enumerate(ks):
        out[i, rng.choice(C, kk, replace=False)] = 1.0 / kk
    return out


def make_history(P, years, seed):
    """The eras a society goes through: (start week, end week, combo key, intensity, kind). Same for everyone in a run,
    and drawn from its own random stream so that comparisons between runs with the same seed share one history."""
    if P["history"] == "calm":
        return []
    if not isinstance(P["history"], str):
        return [(int(a * 52), int(b * 52), k, i, kd) for a, b, k, i, kd in P["history"]]
    r = np.random.default_rng(seed + 7919); out = []; t = 0.0
    if r.random() < 0.5:                                   # born into calm times or into an era
        t = r.exponential(1 / P["era_rate"])
    while t < years:
        dur = r.exponential(P["era_len"])
        out.append((int(t * 52), int(min(t + dur, years + 1) * 52), ERA_COMBOS[r.integers(len(ERA_COMBOS))],
                    float(r.uniform(0.3, 1.0)), ERA_KINDS[r.integers(len(ERA_KINDS))]))
        t += dur + r.exponential(1 / P["era_rate"])
    return out
LIB_SYM = compile_library(True)

DEFAULT = dict(
    # choice
    beta_V=3.0, beta_P=1.2, beta_H=0.5, act=0.6, tau0=0.6,
    # v3 gates: availability (world), noticing (mindset), control (wanting vs pull)
    access_base=0.85, access_k=1.5,      # chance an option is open; more in a niche that supports its methods
    notice_b=2.0, notice_g=1.0,          # chance an open option is even considered, by fit with the deep core
    ctrl_stage=(0.2, 0.4, 0.55, 0.7, 0.75, 0.75),  # executive control by life stage
    ctrl_stress=0.25,                    # control lost per unit of stress (stress runs 0..3)
    # v3 aspiration (what the person consciously wants)
    beta_A=1.0,      # pull of acting the way you want to become (reflective only)
    asp_rate=1.0,    # aspiration moves this many times faster than motives
    zeta_a=0.2,      # unmet needs make the colors that could meet them wanted (if you believe you can)
    chi_a=0.02, xi_a=0.005,  # norms of the niche, and what visibly works in the world
    eps_v=0.002,     # self-verification: over time you come to want what you are
    resign=0.3,      # failing at a wanted change pulls the want back toward who you are
    gap_stress=0.01, # stress from the distance between who you are and who you want to be
    # v4 resources (money, time, health, ties, freedom) and commitments (career, partner, children, community)
    res0=(0.3, 1.0, 0.95, 0.4, 0.2),          # at birth: family means, all the time, health, family ties, little freedom
    freedom_stage=(0.2, 0.5, 0.85, 0.9, 0.9, 0.85),
    req_g=15.0,      # how sharply a missing resource closes an option
    money_base=0.15, # money level with no income
    dom_freq=2.0,    # how much more often a held commitment's situations come up
    role_base=0.15,  # a role's expectations reach every situation a little
    beta_role=0.2,   # pull of a role's expected ways of acting (felt both as duty and as routine)
    invest=0.002,    # weekly growth of a commitment's strength while held (sunk investment)
    recon_p=0.004,   # weekly chance a poorly fitting, unsatisfying commitment comes up for reconsideration
    beta_exit=1.0,   # cost of walking away, per unit of commitment strength
    exit_weight=(1.0, 1.5, 4.0, 0.5, 3.0),   # career, partner, children, community, faith
    commit_p=(0.5, 0.35, 0.6, 0.08, 0.4),    # chance a successful step actually becomes the commitment (a match, a pregnancy, a membership)
    res_need=0.006, commit_need=0.004,  # how resources and commitments feed human needs
    retire_age=62.0,     # pension age: no new job hunt after it, out of work turns into retiree
    # retiring early or late (engine, 2026-10-05 ~16:30): a yearly rate by age for people at work, times health, the means
    # to stop (strongest before pension age) and how far the work has drifted from what they want; fitted so the share at
    # work falls like US employment by age (calib_v7/exits_check.py). None: the old rule (1% a week from pension age).
    retire_hz=((50, 0.0), (54, 0.0), (56, 0.045), (58, 0.05), (60, 0.035), (61.9, 0.035), (62, 0.11), (65, 0.12), (67, 0.12), (70, 0.14), (80, 0.2)),
    retire_health=2.0,   # poorer health, earlier (x e^(2 (.7 - health)))
    retire_means=0.8,    # money relative to the median, to this power before pension age (a third of it after)
    retire_misfit=1.5,   # work that no longer fits: x (1 + 1.5 misfit)
    pension_cut=0.06,    # a pension taken early is smaller: 6% for each year before pension age (at least half)
    kid_cost=0.12,       # what each child at home takes off the money level
    pension_k=0.3,       # v22.5 F9 (modifiers.md M15): a career's pension in the money a life drifts to (work pays .45)
    pension_base=0.0,    # v22.5 F9: a state pension from pension age for everyone, career or not (0: none, as before)
    faith_inherit=0.6,   # chance a child is raised inside a faith (each family's faith has its own color profile)
    faith_own_age=16.0,  # a faith one was raised in is the family's until then: it builds no strength of one's own before
                         # this age, so leaving it as a young adult costs little (0: as before)
    # drifting away from a faith or cause without a decision (engine, 2026-10-05): a yearly rate by age from faith_own_age,
    # likelier the less the person values tradition (the colors' tradition loading in the engine's Schwartz map, schwartz.py:
    # W 2.5, U -1.5, B -3.5, R -.5, G 3; tradition is the value most tied to religiousness, Saroglou et al. 2004) and the
    # less the faith has become their own (strength I). None: only walking away at a reconsideration, as before.
    faith_drift=((16, 0.03), (22, 0.03), (30, 0.015), (45, 0.006), (70, 0.004)),
    faith_tilt=(-0.71, 0.43, 1.0, 0.14, -0.86), faith_tilt_k=4.0,
    clash_on=0.3, clash_off=0.2,  # misfit at which holding a commitment becomes a clash with what you want, and ends
    clash_stress=0.01,   # weekly stress of living inside a commitment you no longer believe in
    commit_mix=(0.5, 0.25, 0.25),   # a new commitment's expected ways: the act that formed it, the person then, their surroundings
    faith_conc=1.5,      # how one-sided inherited faiths are (Dirichlet concentration; lower = more one-sided)
    rationalise=0.3,     # recommitting pulls what you want back toward the commitment (doubling down)
    # v4 pent-up demand (Emren's vectors, 2026-10-04): wanting that is blocked builds pressure; inertia holds it
    # back until it crystallises into a breakthrough (Baumeister 1994, "the crystallization of discontent")
    skill_gain=0.02, skill_fade=0.005,    # skillset: weekly gain with practice, fading without (v3 had 0.0005: everyone became skilled at everything)
    # the outside world (v4): personal events and eras. Acceptance of a message is
    # tanh(acc0 + acc_fit*fit with mindset + acc_disc*discontent + acc_open*openness + acc_conf*group lean (social sources)
    #      - acc_hold*holding what it would take); negative acceptance is pushing back (reactance)
    events_on=True, ev_scale=1.0,      # switch, and a multiplier on all event rates
    ev_eta=0.15,        # how far an accepted message moves the want (per unit strength and exposure)
    ev_z=0.05,          # how far it moves motives directly (felt experience), scaled by plasticity
    acc0=0.15, acc_fit=0.45, acc_disc=1.5, acc_open=0.5, acc_conf=1.0, acc_hold=0.5,
    gap_move=0.3,        # (.3 from the v22.4 refit) a gap one is acting to close weighs less in satisfaction: the distance to the person one wants to be
                         # (sat_gap) counts up to this share less as the ten-year acted ways (hist_m) run toward what is wanted
                         # beyond what is held (full at .5 of the acts there, none at an even .2). Progress toward a goal, not
                         # only its distance, sets how it feels (Carver and Scheier 1990). G19w, 10-11: in world-on lives that
                         # keep choosing Green the want-identity gap is the whole of the contentment drop. 0: as before
    cur_will=1.0,        # (1.0 from the v22.4 refit) the will tempers the current (item 12): on a colour the person wants beyond what they hold (full at .2
                         # above), the current pulls it down up to this share less (a tailwind stays). The times, the people and the places around a
                         # life do not follow its choices; with the world on they run toward White and Red, so lives that keep
                         # choosing Green or Blue were pulled out of them (G19w, 10-11: the current, own colour, ages 15-40,
                         # W +1.59 U -.38 B +.06 R +.63 G -2.12). 0: as before
    history="random",   # "random" eras, "calm" (none), or a list of (start age, end age, combo, intensity, kind)
    era_rate=1 / 8, era_len=12.0,      # eras: years of calm between them (mean 8), length (mean 12)
    era_norm=0.006,     # weekly pull of the times on the want (scaled by exposure and acceptance)
    era_niche=0.002,    # weekly shift of a person's surroundings toward the era's ways
    era_world=0.2,      # how much more the era's ways pay off
    era_shock=0.5,      # strength of the message when an era begins (a revolution, a reform, a revival)
    # feedback from the meta variables (v4): discontent wants what is missing, contentment settles,
    # restlessness wants out of inner tension, and a calm mind steers better
    fb_disc=0.04, fb_acc=0.02, fb_peace=0.03, peace_ctrl=0.6,
    q_decay=0.005,       # weekly fading of pent-up pressure (people get used to things; half-life about 2.7 years)
    q_tol=0.06,          # a gap between wanted and actual that people live with without pressure building
    q_theta=4.0,         # pressure needed for a breakthrough when the person holds the colors at stake evenly
    q_hold=2.0,          # how steeply inertia raises that threshold (pressure needed ~ hold ** q_hold)
    q_min_gap=0.1,       # a breakthrough needs a real gap between wanted and actual
    q_step=0.25,         # share of the way from who they are to who they want to be, taken at a breakthrough
    q_open=1.0,          # openness after a breakthrough (crisis units; a conversion gives 2)
    q_niche=0.3,         # a breakthrough moves the person's surroundings toward what they want
    # meta variables (Emren, 2026-10-04): satisfaction (content) and peace, both 0..1 through a logistic
    sat_mid_stage=(0.6, 0.62, 0.63, 0.705, 0.705, 0.705),   # v7: re-centred on where needs settle in Earth lives (v6 .6 .66 .7 .7 .7 .7)   # v5: what counts as enough grows with age, so children are more easily
                                                        # content and satisfaction falls through adolescence (Casas & Gonzalez-Carrasco, 2019)
    # v6: life events at real yearly base rates (library per_year); every other week is an everyday situation
    base_rates=True, need_floor=0.9,
    event_scale=1.2,     # Emren: big life events a little more often than real life, and not always bad news
    ev_spread=(0.5, 2.0),  # each person's own rate for each kind of event: between half and twice the typical rate
    ev_refr=1.0,         # years after an event before the same kind is fully likely again
    ev_gap=True,         # Emren's point 12 (2026-10-05): a life event's own gap: lo-hi (Library) replaces that ramp: no repeat
                         # before lo years, fully likely again by hi; a child version and its original count as one event
    world_harsh=0.0, world_unrest=0.0, world_prosper=0.0,   # the world: harsh environment, unstable state, economy (0 = typical)
    aut_self=True, aut_act=0.08,   # v6: autonomy met by acting in one's strongest colors (held or wanted)
    family_conc=1.0,     # v6: how alike families are (Dirichlet concentration per color; 0 = every family like the world)
    social_child=0.5,    # v6: how strongly children take on their family's ways (stage child 1x, juvenile 0.5x)
    turn_spread=(0.33, 3.0),   # v6: each life's own pace of new people: from a third to three times the typical turnover
    turn_stage=(0.2, 0.6, 1.0, 1.0, 1.0, 0.8),   # v6: children live mostly among family; circles change most in adult life
    turnover=0.3, turn_years=3.0,   # v6: share of one's surroundings renewed per year by new people, and how often the mix changes
    stage_p=(0.5, 0.45, 0.45, 0.5, 0.6, 0.8),   # v6 plasticity by life stage (None = the library's STAGES); experience
                         # and steadiness already slow adults, so the base no longer falls with age
    ordinary_w=1.0,      # v6: how often ordinary weeks come up, relative to their library rate
    gap_fill=1.0,        # the freed weeks go to the routine by its weight after (0) or before (1) its own pauses (1.0: survey
                         # scorecard 9.25 of 11 over four seeds on next2, against 7.5 at 0.5 and 6 at 0; engine 10-06 08:20)
    gap_keep=True,       # a moment's pause frees its weeks for the ordinary routine, not for the rare moments (engine 10-06)
    everyday_min=8,      # fewer ordinary everyday moments open than this (a stage that lags the age): neighbouring stages' join
    satiate=True,        # v6: needs fill with diminishing returns, so they settle short of full and keep pulling
    comp_act=0.05,       # v6: competence met by succeeding at what was hard, in any color
    duty_mean=0.05,      # v6: doing right by those who depend on you gives meaning
    duty_asp=0.0,        # v6: share of duty that also shapes the wanted self directly (0: duties shape choices; the self follows
                         # through practice. At 1, people narrowed to one color and broke through 7 times a life)
    duty_w=0.5,          # v6 (0.3 before the Library loops, which blur slow trends): how strongly the needs of those a commitment serves are felt as one's own
    flex=True, flex_rate=1 / 104, flex_depth=0.7, flex_exp=(150, 350),   # v6: accepting limits; chronically unmet needs matter
                         # less, more so after many wanted things failed or closed (flexible goal adjustment rises over adult
                         # life: Brandtstaedter & Renner 1990); flex_exp = (failures before it starts, failures to reach full)
    sat_need=5.0, sat_mid=0.86, sat_adapt=4.0, sat_mood=1.0, sat_gap=6.0, adapt_weeks=104, meta_weeks=26,
    green_jobs=True,    # v22.4: the green entry jobs' rules and the roads that name them (earth_rules.ROLES_WHEN), read
                         # once the catalogue has the titles (Library #152); off, they hold no rule of their own (as v22.3)
    acc_redraw=True,    # v22.4 (chroma-packs/notes/v22.4-engine-fallback-jobs.md): a first job or job move whose title its
                         # route refuses (acc_first, acc_move) re-draws among the other titles whose rules hold, by the same
                         # weights, so the life goes to its next-best fit, not to no title (off: the career starts untitled)
    occ_keep=0.6, occ_back=3.0,   # a new job after one ended within occ_back years returns to the last line of work with this
                         # chance (the packs, 01:40: a scientist who changed jobs stopped being a scientist). Job changes
                         # are about twice as common as changes of occupation (Kambourov & Manovskii 2008)
    sat_gap_ref=0.12,    # the gap between want and self that leaves satisfaction where it is (the gap people live with).
                         # .07 before turning points; their windows widen the usual gap (.12 to .16 at 50), so the level
                         # is re-centred on the same lives: satisfaction at 30/50/70 .73 .60 .64 against .72 .62 .62 without
                         # them (calib_v8/inertia_refD.out, 300 lives)
    age_windows=True,    # situations only come up inside their age window (v4)
    family_care=0.03,
    # v22.5 realism F3, a household and real people (chroma-ideas/realism/v22.5-realism-list.md; means-realism.md D1 to D3),
    # behind hh_money=False and ties_people=False. Tendencies, not walls: the family sets where a child's means sit, and a
    # life's own work, moves and people still carry them anywhere
    hh_money=False,      # D1, D2: until they live on their own, money is the household's: the family class (with the world
                         # off, the start's means) times the parents' work, so a parent's job loss, death or leaving lowers it.
                         # It hands over to their own between hh_ages as they work or move out; after, the family is a floor
    hh_cls=(0.12, 0.30, 0.55),   # the household's money by family class (poor, middle, well-off), both parents at work
    hh_earn=(0.5, 0.25),  # its share with no parent at work, and what each working parent adds (two: all of it; one living
                         # apart counts half). With the world off every living parent counts as at work
    hh_ages=(16.0, 25.0), # the ages over which the household's money hands over to their own while still at home
    hh_work=0.5,         # ... at home, the own share is that age ramp x (1 - hh_work + hh_work x at work)
    hh_floor=0.5,        # D2: money drifts no lower than this share of the family's class level, by closeness to a living
                         # parent (the family helps in hard times)
    ties_people=False,   # D3: ties are the people around them: with the world on, the people model's own closeness (People.ties,
                         # parents, siblings, grandparents, friends, partner, children, circle); with it off, from who is
                         # alive and held (tie_w). The odds of moments read the same number (one number)
    tie_w=(0.6, 0.3, 0.5, 0.15, 1.0, 0.4, 0.6, 0.25, 0.2),   # world off: a parent, a sibling, the closest friend, a
                         # grandparent, the partner, a child (each, up to three), the community, work and faith held
    tie_k=1.0,           # world on: ties = 1 - (1 - People.ties) ^ tie_k, as if People's ties_T were 20 / tie_k (F9 fit)
    tie_away=0.5,        # world off: a parent's weight once they live on their own
    tie_T=3.0,           # world off: ties = 1 - exp(-(sum of weights) / tie_T): about .55 for a child, .75 at 40 with a family
    # v22.5 realism F8, retirement ends work, behind retire_ends=False: once retired and not working, the work moments
    # (first life: tag work, or at: employer) no longer come, but the doors back (an option that starts a career) stay
    # open; going back to work is a choice of their own (an act), never a background title, and it ends the retirement
    # (one work status); a new job is not retired from in its first half year
    retire_ends=False,
    retire_back=26,      # weeks a job taken after retiring (or any job) runs before the retirement hazard reads it
    # v22.5 realism F10, once means once, behind world_only=False: a moment the world brings (world_link WORLD_MOMENTS:
    # elections, firm sales, mergers, leaks, cover-ups, a disaster's rebuilding, bad air) comes only on the world's event
    # for those it touches, never by the everyday draw, and not again inside its own gap:; a moment with no yearly rate
    # that waits for the world (per_year all 0) keeps its gap: in the everyday draw too. With F8 this brings firm crises
    # and the job losses after mergers to the world's own rates
    world_only=False,
    # v22.5 realism F7, one roll of the living, behind one_roll=False: the children at home are counted from the youngest
    # child (not the first), and the conditions read the youngest child's age (kid_young); in the game the story's people
    # follow the world's one list of who is alive (a death names the one the world lost, a birth names the newborn, a
    # feast seats the living, the news names only the living)
    one_roll=False,
    # color bounds (Emren, 2026-10-04): unless a setting says otherwise, no normal person is fully one color, loses a
    # color entirely, or stays perfectly even. Applied to both motives and wants every week
    max_color=0.75, min_color=0.03,
    min_spread=0.04,     # after childhood, a person whose colors are all within this of each other gets nudged off even    # weekly pull of a child's safety and belonging toward 0.85 (half in adolescence)
    pc_mid=1.6, pc_stress=2.0, pc_clash=3.0, pc_tension=2.0, pc_pent=1.0,
    # temperament (v5, Emren 2026-10-04): never preset. Everyone starts the same, and four slow traits form from the
    # life lived: the world met, how outcomes are read, attempts and their success. They form fastest in childhood
    # (a sensitive period) and keep shifting slowly after. They change how a person reacts, not what they want
    temperament=True,
    T_rate=0.006, T_stage=(1.0, 0.8, 0.5, 0.3, 0.2, 0.15),   # weekly learning rate by stage (time constant ~3 years in childhood, ~20 late in life)
    # reactivity: how hard events hit (stress and mood). A harsh or unpredictable world raises it, safety and belonging
    # lower it (adaptive calibration of stress responses: Del Giudice, Ellis & Shirtcliff, 2011)
    r_stage=(1.0, 0.6, 0.3, 0.1, 0.07, 0.05),   # reactivity forms mostly in childhood (a sensitive period), then barely moves
    r_harsh=0.6, r_unpred=0.6, r_support=1.0, r_ref=(0.6, 0.8, 0.74),   # refs: typical stress, surprise, support
    # steadiness: how firmly a person holds who they are. Succeeding in the colors they hold (self-verification), keeping
    # commitments (social investment) and being who they want to be build it; failing in what they hold, crises,
    # breakthroughs and walking away from commitments shake it. It slows change: plasticity / (1 + steady_k x steadiness)
    s_conf=0.02, s_hit=0.02, s_role=0.0005, s_fit=0.005, s_decay=0.004, steady_k=1.0, steady_want=0.5, steady_cap=0.7,   # fades with a half-life of about 3.3 years
    # baseline mood: the person's own usual satisfaction, a slow average of how life has gone (a set point life can move)
    sat_base=3.0, base_ref=0.55,
    # outlook: sense of control, learned from whether effort pays off (helplessness when it keeps failing or is blocked).
    # It bends felt odds (optimism or pessimism) and how much the person tries to become who they want to be
    o_bias=1.0, o_try=1.0, o_ref=0.45,   # ref: the typical share of wanted attempts that work out
    beta_N=4.0,      # weight of relieving unmet needs in choice
    # outcomes
    gain=3.0, loss=0.8, fit=2.0,
    # learning channels
    eta=0.7,         # instrumental learning rate
    rho=0.3,         # confirmation lens
    defend_k=0.35,   # v6 (v5: 1.0, which narrowed most elders to one color). how far experience discounts failures in the colors one holds (identity defence)
    fail_fit=0.2,    # v6: share of a failure's lesson that goes to what the situation called for (0: back toward oneself)
    unusual_k=0.15,  # v6: how much more an act unusual in one's surroundings moves the colors
    react_k=1.0, react_press=0.15,   # v6: reactance of steady people under strong pressure from their surroundings
    core_walk=0.0,   # v6: weekly random drift of the deep core in adults
    ev_open=0.15,    # v6: openness to change after a big event, per unit of surprise (a breakthrough gives 1)
    clust_years=3.0, wound_years=0.75,   # v6: memory of recent trouble and fortune; how long a hard event leaves one open
    broaden=0.5,     # v6: how much mood widens (good) or narrows (bad) the options a person even considers
    landmark=0.3,    # v6: how much a birthday, an age ending in 9 or new surroundings lowers the bar for a breakthrough
    care_k=0.2, heal_k=2.0, harden_k=4.0,   # v6: support pulls back to the core; after a hard event, support heals and
                                            # its absence lets the shift harden into the core
    zeta=0.0,        # v2 direct scarcity channel on motives; in v3 needs act on aspiration (zeta_a)
    need_set=0.5, need_drain=0.005,   # v6: 0.015 -> 0.005 with satiating refills (needs settle around 0.6-0.9)
    eps0=0.45,
    chi=0.03, xi=0.01,
    framing="mild",     # v6 default (Emren 22:46): mild tension on Magic's five questions. Name in FRAMINGS or a 5x5 matrix: how the world reads color relations
    ten_good=0.05, ten_bad=0.05, ten_split=0.5,   # v6: acts joining opposed colors pay off in meaning when they work, in stress
                                                # and lost integration when they fail. Enemy pairs (item 5, Emren 10-07 12:42
                                                # UTC): a fair bet, ten_bad = ten_good (.05), from the stage 2 refit
    mu=0.3,          # strength of framing tension/synergy (v3: 0.1 was too weak once upkeep and needs balance people)
    drift_frames=('pie', 'axes'),   # enemy pairs (item 5): the framing's weekly drift (mu) and its cut on ends sought through opposed
    ends_frames=('pie', 'axes'),    # means only in these worlds (Magic's pie taken literally; ("pie", "axes") from the stage 2 refit); the
                         # default world keeps its tension as felt calm and the bet, and every pair is an ordinary way to live
                         # (chroma-philosophy/enemy-pairs.md). None: every world (v6-v22.1)
    iota=0.1,        # integration learning
    upkeep=0.08,     # v6 (v4-v5: 0.13). cost of holding a concentrated identity (v4: 0.13 keeps strong dominance above 0.6 rare once eras and events push)
    # Shadows (Emren 2026-10-07 12:18 UTC, chroma-philosophy/shadows.md), in place of upkeep: a colour that rules a life
    # shows its own weakness, as Magic's writing names it, and the costs it brings pull the person back toward what they
    # lack through the loops the engine has (a failure teaches what the moment called for: fail_fit)
    shadows=True,             # item 2, on from the stage 2 refit
    # light and shadow (chroma-ideas/shadows-mechanics.md, 10-08): each colour has a shadow part s (0 to 1), which grows
    # toward a target from four sources: holding on while life asks to move, ruling the life, no enemy colour to argue,
    # strain. Its force e = min(1, w x s / sh_full) drives the effects; a state word shows from 18 (on .5, off .35)
    sh_world=False,             # shadows with the outer world on too (v22.3 refit: False, with the world on they blurred
                               # identities, one colour at 40 in .10 of lives against .25; back with its own fit)
    sh_age=13.0,               # a shadow part can grow from this age
    sh_src=(0.5, 0.5, 0.4, 0.4),   # how far each source alone moves the target: holding on, ruling, no counterweight, strain
    sh_grow=6.0, sh_fade=12.0,  # months for the shadow part to move most of the way to its target, growing and fading
    sh_full=0.20,              # the shadowed share (w x s) at which the force is full
    sh_care=0.5,               # being cared for softens the target (check 3: shadows can be lived with)
    sh_integ=0.5,              # holding an enemy pair well (integration J with either enemy) softens it
    sh_over=0.5,               # overuse: utility bonus, at full force, on options in the shadowed colour's ways (heart and head)
    sh_counter=0.03,           # a counter-pick that works (the player picks another way than the shadow's pull) lowers s
    sh_seen=0.15,              # a reflection moment met lowers s and marks the shadow seen
    sh_gain=(1.0, 1.0, 1.0, 1.0, 1.0),   # per colour, W U B R G: fitted so each dominant colour lasts about as long (check 2)
    sh_fail=1.0,               # logit cost, at a full shadow, on acts in the colour's own ways: its own downfall (unseen in felt odds)
    sh_tie=0.10,               # W rigid, B ruthless (R reckless half): ties fall by this much at a full shadow (people leave)
    sh_strain=0.004,           # W rigid: weekly strain of duty held too hard (stress)
    sh_form="own",   # how the pull works: "own" (the shadowed color gives way) or "balance" (back toward what is lacking)
    sh_pull=0.05,   # an active shadow pulls its own color back (log-ratio share a week at full strength)
    sh_will=0.5,    # the pull gives way to the will (G19, 10-11; .5 from the v22.4 refit): on a colour the person wants beyond what they hold (want
                    # above identity, full at .2 above), the shadow pulls back up to this share less. A shadow pulls back
                    # what one holds beyond what one wants (its own "holding on" source); a way one keeps choosing grows,
                    # and its other costs (sh_fail, sh_tie, sh_strain, sh_lapse, sh_door) stay. 0: as before
    sh_lapse=0.15,             # U indecisive: share of chosen acts lost while weighing them, at a full shadow (the chance passed)
    sh_body=0.10, sh_burn=0.5,  # R reckless: health falls by this much at a full shadow; discipline wears (yearly share)
    sh_door=0.5,               # G stuck in their ways: moments that could start something new come this much less often
    # dynamics
    mom=0.25, kappa_e=0.02, eps_core=0.01, M0=90.0, noise=0.03,   # v6 M0 (v5: 25)
    settle_log=True,  # v3: experience lowers plasticity logarithmically (v2: in proportion), so adults keep changing
    # stages and rites
    rite_h=0.01,     # chance that a fully surprising fitting event marks a passage at the window's opening
    rite_ready=4.0,  # how much readiness grows by the window's close
    rite_thr=1.4,    # an event below 0.2 x this at the window's close is a quiet passage
    rite_imprint=0.9,  # share of the gap between core and expressed identity closed at a rite
    rite_boost=1.0,  # plasticity boost after a rite
    stiffen=0.42,    # core consolidation rate multiplied by this at each rite (0.7 before turning points; .45 on the live batch,
                     # .42 on next2: four seeds x 600 lives, scorecard means 10 of 11, calib_v8/turning_next2.md)
    # transition windows (Emren's points 6 and 7, 2026-10-05; Emren chose "Turning points" 21:28): a turning point in life
    # (a commitment begun or ended, a new title, a move, a loss) leaves a person open for months, and while open, who they
    # are becoming settles into the deep core instead of being pulled back to the old self (values change most around
    # transitions: Bardi et al. 2014; new roles change people and the change lasts: Roberts, Wood & Smith 2005). Fitted to
    # rank-order stability (calib_v8/inertia_tw*.out; twL on four seeds, 300 to 900 lives). TW_OFF: as before
    tw_trans=0.7,    # openness (crisis units, as B) a transition adds; at most two count in one week
    tw_core=3.0,     # while open, how much faster the deep core follows who they are now (x (1 + tw_core x openness))
    tw_pull=1.0,     # while open, how much weaker the pull back to the old core (/ (1 + tw_pull x openness))
    tw_pen=0.5,      # a big life event's share of its push that goes straight into the deep core (penetration; .4 on the live batch)
    tw_sep=False,    # the window is its own state (TWo): it lets change settle without making the person wander more
    tw_want=0.0,     # while open, the want re-forms around who the person is becoming (goal adjustment after a transition:
                     # Heckhausen, Wrosch & Schulz 2010): the want's pull toward the self x (1 + tw_want x openness)
    tw_force=0.0,    # with tw_sep: while open, what happens moves the colors this much more (x (1 + tw_force x window)),
                     # while the person's own random wandering and the want keep their usual pace
    # threshold seasons (Emren's point 6, card 2026-10-05 20:59): a few months of linked moments around each crossing. A rite
    # of passage (or gaining a title a pathway marks as a rung) opens the season; the Library's moments with threshold:
    # come in three steps (1 the crossing, 2 the in-between, 3 settling in) in place of ordinary weeks, the person stays
    # open, and the moment marked transform: is the season's transforming chance
    season=True,
    season_weeks=(1, 10, 22),  # weeks after the crossing when steps 1, 2 and 3 come (a big life event that week defers it)
    season_len=30,             # weeks the season lasts; a step not met by then is skipped
    season_open=1.0,           # openness (crisis units) held at least this through the season (a rite gives 1)
    season_amp=2.0,            # the transforming choice moves the colors this many times as far as an ordinary act
    season_imprint=0.5,        # and closes this share of the gap between the deep core and who they are now
    season_by_age=True,        # a stage's season comes at the ages its moments are written for (the game, 22:42: rites come
                               # late, mostly at the end of their window, so a season opened only at the rite met no moment):
                               # it opens at the rite if the rite falls in those ages, else at an age drawn within them
    season_tr_week=16,         # every season carries its transforming chance (the packs, 22:44): a step with a plain and a
                               # transform: moment plays the plain one, and the transform: moment comes in its own week
    # identity (Emren's point 11, card 2026-10-05 20:58 "Sex set, rest found"; the Library's research note,
    # chroma-library/drafts/identity-research.md): sex comes from setup; who a person is drawn to and any unease with their
    # sex are drawn at birth at real rates, hidden, and never changed by an act. Society sets the cost of hiding and telling
    sex=None,            # "female", "male", a list (one per life), or None: half and half
    attr_p=((0.77, 0.11, 0.08, 0.02, 0.02), (0.83, 0.07, 0.04, 0.02, 0.04)),   # attraction 0 the other sex only, 1 mostly,
                         # 2 both, 3 mostly the same sex, 4 the same sex only; women, men (Gallup 2024: 9 in 100 US adults
                         # LGBTQ+, over half of them bisexual, more women; more gay men than lesbian women)
    attr_drift=0.001,    # yearly chance from 25 that a woman's attraction moves one step toward both (Diamond 2008: a
                         # small share; about 5 in 100 women over a life)
    unease_p=0.01,       # comes to feel their sex does not fit them (about 1 in 100; about 1 in 200 identify as transgender)
    aware_age=13.0,      # from this age a hidden attraction or unease weighs on them
    hide_stress=0.008,   # weekly stress of hiding it (minority stress: Meyer 2003), until a 'came out' mark; times
    climate=0.0,         # 1 + how hostile the world is (0 typical modern Earth) + half a family faith held strongly
    # sex at birth, own gender and the role the world expects (checklist N1b, chroma-identity/for-the-engine.md, Emren
    # 10-06 22:57 "a gender emphasis... about birth, not sexual preference, not social role"; ID_OFF: point 11 as it was)
    id_v2=True,
    title_ages=True,     # a title or perk is gained only inside its catalogue ages= (checklist C-X4); False: as at go-live
    far_share=0.45,      # E6: the share of one's own moves (moved away, moves:) that go to a new town; 1: all, as at go-live
    recon_held=True,     # a forced reconsideration is of a commitment still held (False: as at go-live, which could end one twice)
    child_norm=True,     # C-X5: each child dies at its own age's rate, not raised by the event scale or spread (False: go-live)
    child_gap=3.0,       # C-X5: years between one child and the next (the usual birth spacing)
    child_mort=5e-5,     # C-X5: the children's Gompertz level (mort[0] for everyone else)
    season_share=True,   # a threshold step's moment comes to the share of lives its times: gives (Library next3 §4)
    season_excl=True,   # K6 (v22.3, off): a step plays at most one moment, each at its own times: share (their sum, at
                         # most 1, is the step's share; the person's colours tilt which), not one draw per moment;
                         # "1 homeowner in 20" reads as 1 in 20, and a times: line with words only reads by season_words
    season_words=(("nearly every", 0.9), ("rare", 0.05), ("most", 0.7), ("many", 0.5), ("some", 0.25)),   # refit values
    move_near=True,     # K2 (v22.3, off): a moves: moment goes to a new town only when it says so (moves: far, or its name
    fam_far=0.3,         # names a new town; moves: near never; else fam_far of the time: leaving home, a smaller home), and a
                         # move within the town keeps half the circle (fam_far a refit value; newcomer .97 of lives vs .60)
    ow_weeks=26,         # weeks without work after losing a job before 'out of work' (52 at go-live: .07 of lives against .15)
    intersex_p=0.0005,   # born intersex (about 1 in 2,000; ISNA), raised as a girl or a boy half and half
    female_p=0.488,      # female at birth (about 105 boys per 100 girls; UN WPP)
    trans_p=0.006, nb_p=0.010,   # own gender: the other one (0.6 in 100), neither or both (1.0 in 100) (Pew 2022)
    ace_p=0.01,          # asexual (1 in 100; Bogaert 2004)
    role_strict=None,    # how strictly the world expects each sex's role, 0 to 1 (None: by setting, ROLE_BY_SETTING)
    role_boys=1.5,       # a boy under 13 who crosses is frowned on this much more than a girl (Fagot 1977; Martin 1990)
    role_k=4.0,          # closure units per unit of strictness x crossing weight (one unit = a written closed: approval);
                         # fitted so a job the world reserves for one sex goes to that sex .65 of the time at strictness .3
    role_title_stress=0.002,   # weekly stress of holding a title the world reserves for the other sex, x strictness
    role_fit_hl=3.0,     # years: half-life of role_fit's slow average (for gates and the game; it changes nothing itself)
    accept_trans=None,   # how far the world accepts living as one's own gender, 0 to 1 (None: by setting)
    out_stress=0.25,     # share of the hiding stress that stays after telling, x how hostile the world is (Meyer 2003)
    partner_same_p=(0.0, 0.03, 0.16, 0.8, 1.0),   # a new partner of the same sex, by attraction 0-4 (Pew 2013)
    ace_intim=0.3,       # an asexual person meets the intimacy moments this share as often
    intersex_fert=0.3,   # an intersex person's own pregnancy or fathering chance (estimate: many variations lower it)
    # a wider world (Emren's point 11, card 20:59 "By choice, rarely"): the character can die before old age, and can kill
    retire_season=True,  # retiring opens the elder season when the batch has a moment that retires (its first step)
    near_ratio=20.0,     # a failed act with death_if_fails puts the person in hospital this many times as often as it kills
    self_death=False,    # the character's own death: the life table (mort) x health, and the Library's death_if_fails on
                         # risky acts; a life that ends is idle from then on (o["died"]). Off: every life runs to the end
    self_mort=(0.0006, 3.5e-5, 0.09),   # the character's yearly chance of dying at age x: c + a exp(b x) (Gompertz-Makeham:
                         # accidents and illness at any age, then ageing); about 6 in 100 die before 50, 15 before 65 and 40
                         # before 80 (US life tables)
    self_health=1.5,     # the life table x exp(self_health x (0.6 - health))
    kill_caught=0.55,    # share of killings outside war that end in arrest (about half of US homicides are cleared, FBI)
    kill_prison=(5.0, 20.0),   # years in prison after a conviction, before [ex-prisoner]
    # dissonance and conversion
    theta0=2.5, Lam=1.2, crisis=2.0, crisis_half=26, D_decay=0.004, slack=0.05,
    # world
    f_world=np.zeros(C), lam_local=0.6, nu_niche=0.02,
    impose_p=0.03, impose_bias=None, world_profile=np.full(C, 0.2),
    # v7 dreams, passions and plans (Emren 21:39: dreams before adulthood; passions and long plans after, and a plan is
    # not a commitment. 2026-10-05 04:57: 1A dreams come from people and stories a person admires, a book, film or
    # parade too, read through their own colors; 2A tries that work and feel meaningful, sealed by a rite, make a dream
    # a passion; 3A plans reach a week, a year, five years or a life)
    goals=True,
    dream_rate=(1.0, 0.8, 0.4, 0.06, 0.04, 0.03),   # sparks a year that could start a dream, by stage (from age 4)
    d_adm0=-0.5, d_fit=1.5, d_open=0.5,   # chance a spark takes: fit of what it shows with who they are and want to be, openness
    d_read=0.6,          # how much a person reads what they admire through their own colors
    d_half=(1.5, 3.0, 2.0, 0.6, 0.6, 0.6),   # years for an unfed dream to fade by half, by stage
    d_dom=(0.45, 0.06, 0.06, 0.05, 0.04, 0.34),   # what dreams are about: career, partner, children, community, faith, a pursuit
    dream_grow=False,    # v22.5, F6 (dreams that grow up; chroma-ideas/realism/v22.5-realism-list.md): a dream is named only
                         # among dreams of its age (the Library's dreams.py DREAM_KIND and KIND_FROM: roles a child can see
                         # and play at from 4, standing and money from 9, a calling of one's own from 14), and the Library's
                         # DREAMS_MORE join; a spark keeps its subject (TRIGGER_DREAMS: a firefighter's visit sparks a
                         # firefighter, or no dream when they are too young for any it shows) and comes only at the ages its
                         # telling fits (TRIGGER_AGES); a play dream started before PLAY_UNTIL is short-lived. Off: as before
    dream_play_half=0.5,   # dream_grow: years for an unfed play dream of a young child to fade by half (children of 4 to 8
                           # change them often; Ginzberg's fantasy period)
    dream_subj=0.5,      # dream_grow: share of a dream's ways taken from the subject its spark showed (the rest: how the
                         # person read it)
    own_open=False,      # v22.5, F12 (the world and the start hold): a culture's own acts (the library's L["OWN"], from the
                         # Library's worlds.py OWN: the clan's rites, sharing and crafts, the towers' study and guild ways)
                         # are always on offer around the person; lacking the means still closes them. Off: as before
    start_hold=False,    # v22.5, F12: with the world on, a start keeps its promise (world_cfg["start"]: place, wealth,
                         # faith, hard streets, society): the birth is drawn again until the place kind, class and family
                         # faith fit; a child is raised in the family's own faith (none when the family holds none); the
                         # start's society stays in the circle around them (start_soc). Off: as before
    start_soc=0.3,       # start_hold: share of the start's society in the niche and in what the order rewards
    faith_fam_p=0.9,     # start_hold: chance a child of a family in a faith is raised in it, when the start leaves it open
    max_dreams=3, max_passions=2, max_plans=3,
    g_dream=0.3, g_pass=0.5, g_plan=0.8,   # pull of a goal on what the person decides to do
    g_pass_auto=0.3, g_plan_auto=0.2,      # pull felt without deciding: a loved activity (more if obsessive), a when-then plan
    g_notice=0.8,        # goals make fitting options noticed
    g_want=0.02,         # weekly pull of goals on the wanted self (dreams 1, passions .7, plans .5)
    g_up=0.12, g_down=0.06,   # goal strength from a success in its ways, lost from a failure (more with a dark outlook)
    seal_v=1.0, seal_s=0.3,   # a dream becomes a passion at a rite when this much meaningful success has gathered and it is this strong
    pass_half=8.0,       # years for an unpractised passion to fade by half
    pass_hold=0.25,      # share of inertia passions supply (as roles do)
    hp_mood=0.05, op_rum=0.01, op_away=8,   # harmonious passion lifts mood when lived; obsessive gnaws when away this many weeks
    ctl_fam=0.3, ctl_lack=0.4, ctl_spec=0.15, ctl_sup=0.3, ctl_free=0.2,   # what makes taking in a passion controlled, not free
    ctl_stress=0.3, ctl_press=0.8, ctl_mid=1.3,
    ctl_react=0.3,       # a reactive temperament (learned, v5) takes a passion in under more inner pressure
    g_size=(0.2, 7.0, 35.0, 250.0),   # progress a plan needs (fit x stakes x self-control x free time): a week, a year, five years, a life
    dream_plan=1.0,      # at coming of age, a strong unsealed dream becomes a five-year plan (chance per unit of strength)
    res_p=0.25,          # chance of a resolution at a birthday, per 0.15 of distance from who one wants to be (fresh start)
    pass_plan=0.08, dom_plan=0.4, revive=0.05,   # yearly rates: a passion becomes a plan; unmet needs make a plan; an old dream returns
    g_seek=1.0, g_seek_ev=0.6,   # plans make people seek chances: everyday situations, and life events of the plan's domain
    g_decay=0.01,        # weekly fading of a plan that does not fit who one is (scaled by 1 - concordance)
    g_drop=0.15,         # felt odds below which a person thinks of letting go
    g_quit=0.3, g_ruminate=0.02,   # stress of giving up what was invested; of clinging to a plan that seems hopeless
    felt_cp=0.9,         # how surely a person believes a good step into a commitment will stick
    felt_take=(0.15, 0.4),  # share of chances a person expects to take: base + this x outlook
    felt_kappa=10.0,     # v7: how sure a person is of how often chances come (lower: less sure); 0 = sure, as before 2026-10-05
    g_up_dream=0.02,     # a dream grows only a little from everyday success; it lives on meaning
    life_end=80.0,       # the end a life goal is planned against
    regret_k=0.5,        # weight of lost dreams that still fit who one wants to be, in satisfaction
    # v7, Emren's point 9 (content and peace over a life): the midlife low and the calm of later life
    mid_years=4.0,       # what counts as enough moves to a new stage's level over a few years, not in one step
    hope_young=0.1,      # how much more of life the young count on than it gives them now (over-prediction: Schwandt 2016)
    hope_up=1.0,         # yearly rate at which hopes rise with what life gives, while time feels open
    hope_let=0.5,        # yearly rate of letting go of unmet hopes once time feels short (developmental deadlines:
                         # Heckhausen, Wrosch & Schulz 2010); it scales with the weight below
    hope_hz=0.55,        # felt horizon from which hopes weigh fully: weight min(1, (felt horizon / hope_hz)^2)
    sat_hope=0.8,        # weight of unmet hope in satisfaction, and of life going better than hoped once hopes are let go:
                         # the U, low near 45-50 (Blanchflower 2021), with later life's expectations exceeded (Schwandt 2016)
    adjectives=True,     # v7 adjectives (point 3): happy, lonely, wealthy ... from the meta variables (ADJECTIVES)
    adj_smooth=0.3,      # monthly weight of the newest value in what an adjective reads (about the last three months)
    hz_calm=0.4,         # with time felt short, what happens stirs up less stress (socioemotional selectivity: Carstensen
                         # 2006; Charles 2010); stress falls most after fifty (Stone et al. 2010)
    seal_more=3.0,       # each passion already held raises the valuation a dream needs to be sealed by this share of seal_v
    seal_rival=0.5,      # a dream sealed beside a passion needs this share of that passion's valuation
    # the Library's batch format (pull-in of the modern Earth batch, 2026-10-05): conditions, echoes, tags, closed options
    cond_more=1.6, cond_less=0.6,   # each "likelier" clause that holds multiplies a moment's chance by this; "rarer" by this
    inner_w=1.0,         # weight of an inner moment in the week's draw when its condition holds (Library rate x this)
    echo_p=0.4,          # share of anchors (a mark, a stretch of life) that ever come back as an echo
    echo_w=0.1,          # weekly chance a due echo comes, once its condition holds (x its likelier/rarer factor)
    closed_acc=0.6, closed_diff=0.05,   # an option closed by law, approval or means is open less often, and harder
    tag_habit=0.02,      # an act flagged habit pulls a little harder toward its ways next time
    tag_door=0.03,       # an act flagged door that works moves the niche toward its ways (new options open)
    tag_identity=0.5,    # an act flagged identity teaches this much more about who one is
    bind_hold=0.3, bind_aut=0.001,   # an act flagged binds holds its colors, as a role does, and costs a little autonomy
    body_hurt=0.03,      # a heavy body act that fails hurts health (light ones half)
    read_p=0.8,          # chance an outside event comes when its time is due (x its likelier/rarer factor)
    read_beta=1.5,       # how strongly a person's colors pick the reading of an outside event
    read_k=0.5,          # scale of an outside event's effect on needs (base x the reading's impact; small events, half a life event)
    read_want=0.02,      # how far a reading moves the want toward its color
    inner_gap=26,        # weeks before the same inner moment can come again
    rejob=0.6,           # yearly chance of finding work again after losing or leaving a job (batch only)
    mort=(5e-5, 0.09),   # yearly chance of dying at age x: a * exp(b x) (Gompertz; about 0.4% at 50, 6% at 80, 16% at 90)
    world=False,         # the outer world (world.py, world_people.py through world_link.py): a living society around the lives
    world_cfg=None,      # World cfg (pace, tech_level, climate, setting, preset, legacy, start; burn_years), world_seed (else the run's)
    world_seed=None, world_obj=None, people_obj=None,   # a World or People already made (the game's saved world), else new
    # stage 3 of the v22 update, the world's rules (chroma-world/model/stage3-rules.md §8): a culture that moves (LW1) and
    # history from causes (LW2). Passed to a new World; a saved world keeps its own. Off by default: stage 1 goes live
    # alone as v22.2 (Emren 10-09 19:15 UTC), these come on with stages 2 to 4 (v22.3)
    cult_schools=True, cult_scenes=True, cult_adults=True, cult_anchor=True, cult_pushback=True, cult_shake=True,
    cult_no_dice=True, hist_party_gov=True, hist_pressure=True, hist_grievance=True, hist_chance_only=True,
    sph_town=True,      # the spheres of society (item 15, v22.3 stage 2), phase 1c: each town's spheres (world.py; read only)
    sph_haunts=True,    # phase 2, N1: named places and each life's haunts (world switches, passed to the world as sph_town is)
    sph_hours=True,     # phase 2: hours in nine spheres and the rungs (N2), the places part of item 12's current
    sph_marks=True,     # phase 2: the mark of the work (marks.json), drawn in yearly with the world on
    sph_events=True,    # phase 3: the sphere events (world.py _sph_events_q), and the Library's sphere_event: moments
    sph_seasons=True,   # phase 3, N7: the year's rhythm on the spheres' event hazards and hours (world switch)
    sph_joins=True,     # phase 3, N6: an event's shift spills to joined spheres (world switch)
    sph_pairs=True,     # phase 3: the ten pair faces per town sphere, taught through the spheres' rows (world switch)
    sph_links=True,     # phase 3: the links between spheres and their colour readings, with sph_events (world switch)
    sph_memory=True,    # phase 3: the four memories that make history (credit, plague, land, command; world switch)
    pair_calm=True,     # phase 3: held pair faces calm their quarrels, broken ones flare; with sph_pairs (world switch)
    sph_cascades=True,  # phase 3: the 14 cascades, each step raising the next while it runs (world switch)
    sph_levers=True,    # phase 4: the nine levers land on a place or the town's sphere, by reach and rung (world switch)
    sph_fair=True,      # phase 4: felt fairness per life and sphere tilts exit, neglect, subvert against voice, loyalty
    sph_shadow=True,    # phase 5, N5: the spheres' shadow shares; the shadow around a life feeds its own (with shadows)
    sph_deep=True,      # phase 5: the deep state of a life: the care load, service, debts, holdings (world switch)
    sph_titles=True,    # item 15: the 28 face titles are gained only by their rules (earth_rules.SPH_TITLE_ROLES); off,
                         # the engine reads none of those rules
    far_ties=True,      # item 18: a town's events touch the people living there; a close tie elsewhere calls (world switch;
                         # chroma-ideas/far-off-events.md); far_par: its tuning (world_people.FAR_DEFAULT; None: start values)
    far_par=None,
    fair_read=True,     # S1: each life reads its spheres' fairness through its colours' parts, and tagged sphere events
                         # move it (chroma-ideas/social-mechanics.md S1; world switch, with sph_fair)
    sph_eyes=True,      # S3 (chroma-ideas/social-mechanics.md): their places read their acts by their faces; a name per place,
                         # talk through go-betweens, caught between two places (world switch; needs sph_haunts)
    sph_odd=True,       # S4: the odd one out at a place: seen more, pressed to blend in, can move the place (world switch;
                         # needs sph_eyes)
    eyes_par=None,       # sph_eyes, sph_odd tuning: {name: value} over world_people.EYES_DEFAULT (None: the start values)
    lead_ways=True,     # S7 "Ways to lead" (chroma-ideas/social-mechanics.md): a post per leading role with its way,
                         # legitimacy and end, in place of phase 4's fixed leader's tenure; with sph_levers (world switch;
                         # lead_par: its tuning, world_people.LEAD_DEFAULT; None: start values)
    lead_par=None,
    sacred=True,        # S5, sacred lines (chroma-ideas/social-mechanics.md): up to two lines a life will not sell; the
                         # spheres' and C3's offers on them bring a moment the character refuses at .9 (world switch; with
    sacred_par=None,     # sph_events); sacred_par: its tuning (world_people.SAC_DEFAULT; None: start values)
    seen_done=True,     # S6 "Seen it done": paths and colour ways seen walked lift felt odds (never the real odds) and
                         # tilt young dreams (world switch; chroma-ideas/social-mechanics.md); seen_par: its tuning
                         # (world_people.SEEN_DEFAULT; None: start values)
    seen_par=None,
    sh_around=0.4,       # phase 5: how far the shadow around a life alone moves its shadow target (a fifth source)
    care_stress=0.02,    # phase 5: stress a month for each 10 hours a week of care load
    # phase 5, debts and holdings (deep_state.money_map; the Engine's defaults confirmed or set by Outer world 10-10,
    # chroma-world/spheres/phase5c-answers.md). bank_line: a bank lends where comm.credit + bank_cls x (class - 1) is this
    # or more; max_share: no new loan past this share of income in payments; sale: a hard-year sale fetches this part of
    # the value; estate: the chance a family leaves a home (and one more holding) is a + b x its class; lender: the
    # threat's stress, a + b x (1 - prot.order); kin_wait, tab_wait: years before kin lend again or the tab reopens after
    # a broken debt; ill_line: health under it is an illness (a hard year); kin_forgive: a partner or parent forgives a
    # kin debt that ends unpaid; buy: (mt at least, level at least x mt, chance a year) with a bank, for a home and for
    # land, a shop or a firm; buy_nb: (level, mt, chance a year) from savings before banks; land_taken: a land taking
    # takes held land; care_buy: (level, hours x) a carer buying help; found_lv: the level a found act needs to found a
    # workshop or shop
    deep_par=dict(bank_line=0.4, bank_cls=0.15, max_share=0.4, sale=0.7, estate_home=(0.3, 0.25),
                  estate_more=(0.1, 0.15), lender=(0.15, 0.3), kin_trust=0.2, kin_wait=2, tab_wait=2, ill_line=0.35,
                  kin_forgive=0.7, buy_home=(0.25, 0.8, 0.1), buy_more=(0.4, 0.9, 0.05), buy_nb_home=(0.45, 0.35, 0.05),
                  buy_nb_more=(0.45, 0.35, 0.03), land_taken=0.3, care_buy=(0.4, 0.7), found_lv=0.3),
    inst_even=True,     # phase 3: colour-even institutions, toward their own past and leaders, not W and B (world switch)
    c2_groups=True,     # item 10, C2 rest: group moments judged half by the group's norm; the strike vote and the
    c2_par=None,         # congregation's split on the world's events (world switch; world_link.C2_MOMENTS, C2_DEFAULT)
    c3_inst=True,       # item 10, C3: institution events (sold, merged, nationalised, a leak, a cover-up; world.py)
    c_par=None,          # the C hooks' tuning, {name: value} over world.C_DEFAULT (None: the start values)
    c4_nature=True,     # item 10, C4: nature's own year in each town (world.py, built by the Outer world; passed as sph_town is)
    c5_faith=True,      # item 10, C5: three faith movement slots, founding and tension (world.py); opens the founding gate
    wl2=True,           # item 11, WL2: the small effects the world was missing (world_link.WL2_PAR; values for the refit)
    birth_age=True,     # v22.3: a life's own births taper by real fertility for its age and sex (Emren 10-10 06:04,
                         # "Engine limit"): a woman's end near 45; adoption and taking a child in stay open at any age
    birth_k=2.5,         # birth_age: the own-birth moments' rate x this, so a life has about as many children as before (2.2)
    role_practice=True,  # what one holds is practice too (Emren 10-10: "choices must impact achieving perks: blue-dominated
                         # choices must increase chances to become researcher"; tools/choice_check.py). On v22.2's rules white and
                         # blue acts fail two to four times as often as the others (true odds .81 and .74 against .90 to .95):
                         # practice comes only from the week's one act, and the colors least acted stay least practised, so a
                         # life that keeps choosing white or blue barely becomes it and loses contentment (.60 to .45). On, each
                         # week the commitments held (profiles weighted by investment, at most one act's worth in all) count as
                         # role_skill of an act's practice in their ways, and draw the niche toward them at role_niche of its pace
    role_skill=0.5, role_niche=0.5,   # role_practice: a held role's weekly practice and its pull on the people around
    black_edge=0.25,     # role_practice: Black's edge (Emren 10-10 22:37 on item 26: "accept it but give black a slight advantage
                         # boost, compared to others"). Ambition turns what one holds into gain faster: a held role's weekly
                         # practice, and the years on a rung toward the title it leads to (rung_years), count 1 + black_edge x
                         # how Black-led the person is ((Black share - .2) / .3, from none at an even share to all at .5).
                         # Only with role_practice on
    read_skill=0.5,      # expertise reads the moment too: skill in an option's ways (sig above a beginner's .3, out of the .7
                         # to master) fills this share of what the person still misreads of its call and the world's push
                         # (read_moment). Felt odds leave out fit and f_tot in the share unread, and those are lowest for
                         # white and blue, so lives that act in those ways run overconfident and each failure pushes them
                         # away (choice_check, 10-10). 0: off, as before
    lens_want=0.5,       # the confirmation lens (rho) looks through who one is trying to become as well as who one is: a success
                         # confirms the acted ways in proportion to ((1 - lens_want) w + lens_want a) ** rho, a the want. With w
                         # alone a colour held weakly stays weak however often its acts succeed, and white and blue start
                         # lowest, so lives that keep choosing them are held back (choice_check, 10-10). 0: off, as before
    app_vigil=True,     # appraisal in learning (app_learn) as vigilance: threat focus weighs what an act teaches by appf_ for a gain
                         # as for a loss, instead of a loss up to (1 + app_k) and a gain (1 - app_k). Threat focus follows the
                         # security side of the deep core (W U), so with the tilt white and blue lives learn their losses at up to
                         # 1.4x and their gains at .6x and are taught out of their own colours (choice_check 10-10: net identity
                         # move per act in the steered colour -.012 white, -.007 blue, +.010 red at equal win rates). Feelings
                         # (fdelta: mood, stress, wounds) keep the tilt. False: as before
    near_gate=True,     # the world's gates (time of year, holy days, place features, settings, technology) also on the
                         # neighbouring stages' everyday moments (everyday_min); the spheres' gates always are
    world_pos_k=0.3,     # with the world on: how strongly what its order rewards (W.Pos) tilts the forces (f_world)
    kid_mort=5e-4,       # R15: a child's yearly chance of dying at least this (the Gompertz curve misses the young), and in
    infant_mort=0.005,   # the first year after a birth this more (about 4% of parents lose a child by 60, 9% by 75)
    # v7 felt horizon (Emren 2026-10-05 07:10 chose it): how much time a person feels is left. When it feels short, what
    # is emotionally meaningful now (closeness, care, the familiar) weighs more than exploring and getting ahead
    # (socioemotional selectivity: Carstensen, Isaacowitz & Charles 1999). It is mindset and experience, not age: age,
    # health and reminders (a death close by, a health scare) shape it, and a young person after a diagnosis shifts too.
    # A world setting (Emren 07:12: a soft trend that society, institutions, the state and peers can set; other worlds can
    # turn it, e.g. a society that sacrifices its elders): hz_tilt is which color ends limited time favors there.
    hz_k=1.0,            # weight of the felt horizon on what an option is worth (its ways and ends, by hz_tilt)
    hz_self=0.0,         # next version (Blue): the felt horizon's trend moves who one is too, not only the want (weekly, logits)
    hz_want=0.03,        # weekly pull of a short horizon on the want, toward the colors hz_tilt favors (.025 before
                         # the point 9 content curve, which took some of the push toward tradition away; re-measured)
    # (Earth scorecard, 300 lives: age r conservation +.10, openness -.10, self-enhancement -.11, self-transcendence +.11;
    # surveys +.15, -.13, -.10, +.08. Without the horizon the age trends were about 0)
    hz_tilt=None,        # None: modern Earth (HZ_TILT, from the Schwartz map and the surveys' age trends)
    hz_life=85.0, hz_span=60.0,   # the age a person expects to reach; years left at which time starts to feel limited
    hz_health=0.7,       # health below this shortens the felt years left in proportion
    hz_remind=0.15, hz_mem_half=3.0,   # a reminder of mortality (a death close by, a health shock) and its half-life in years
    hz_lag=1.0,          # years for the felt horizon to settle on what life shows (a slow mindset)
    # v7 discipline (Emren 07:17, the Library's card: "Yes, build it"): self-control differs between people of the same
    # stage, stress and peace; never preset, learned like temperament from plans kept and broken and hard wins
    # (self-efficacy: Bandura 1997; trait self-control: Tangney, Baumeister & Boone 2004)
    disc_rate=0.2,       # share of the way to the bound a kept or broken plan moves discipline
    disc_win=0.01,        # and a hard win (the act the person meant, done against the odds; x2 in childhood, x.3 when old)
    disc_tag=0.05,       # an act the Library flags self_control "+" or "-" (x2 in childhood, as hard wins)
    disc_back=20.0,      # years for discipline to drift halfway back to even when nothing builds or wears it
    disc_range=(0.6, 1.4),   # discipline multiplies the stage's self-control within these bounds
    # titles and perks (after v7; chroma-engine/perks-titles-format.md): on when the world has a catalogue
    read_moment=(0.3, 0.4),   # share of the moment's call and the world's push a person senses: base, plus with experience
    roles=True,
    title_move=0.04,     # yearly chance of a move inside a held career to a job with requirements the person now meets
    community_titles=3,  # community titles held at once (a team, a troop, a cause); other kinds hold one
    help_lift=1.0, window_lift=0.4, earned_cap=0.9,   # earned odds (Emren 21:03): preparation and timing lift an act that takes a
                         # title, in logit units at full preparation or the most favourable context; never past earned_cap
    try_lift=0.3, try_max=2,   # commitment (Emren 09:18: big titles take steps, commitment and tries): each earlier failed try
                         # at the same title or perk adds try_lift to the earned odds of the next, for at most try_max tries
    rung_years=5.0,      # a title among an act's HELPS counts by years held, min(years / rung_years, 1) (0: held or not)
    rung_min=1.0,        # a title that grows from another (after=) comes only after this many years on that one (Emren 09:18:
                         # no big title in a short time, in one step)
    long_shot=0.1,       # packs 08:02 (Emren 06:06, the anti-story): a failed act for a title, or one whose failure grants [a long
                         # shot that missed], is a long shot when its true odds were under this; it gives that perk, the
                         # clock ago_fail_long and {missed} (the title missed) for the echoes
    perk_cap=0.6,        # most that perks can add to an act's odds (logit units; a perk's odds .05 = +.2 logit, +5 points at even odds)
    perk_breadth=0.2,    # how much perks beyond the best one in a color add
    title_need=2.0,      # what a title's meets add to its commitment kind's own needs (x commit_need x strength)
    perk_loss=(0.03, 0.02, 0.02, 0.02),   # yearly chance of losing an unused skill, standing, a bond, an asset (more when poor or alone)
    profile_margin=0.05, # a title's other profile must fit the person's colors this much better (for about a year) to be taken
    # v10 interpretation and memory (Emren 2026-10-04 21:39, roadmap 3: "type and frequency of misjudgment depend on history,
    # color position, perks, titles, mindset"; order of 10-06 10:50 and 21:55: after the go-live, before the outer world).
    # Threat focus (0..1): how much a person reads what happens as a threat to guard against rather than a challenge to
    # take on (Lazarus 1984; prevention vs promotion focus, Higgins 1997; anxiety-based vs growth values, Schwartz 2012).
    # It comes from where the deep core sits on the security-vs-freedom axis, from recent hard events, and from reactivity.
    thr0=0.0,            # logit of threat focus for an even person with no history
    domains=True,      # life areas (A7, item 4), on from the stage 2 refit: a small offset on the colors per area (work, home, friends, faith); identity reads the core
    dom_share=0.3,      # the share of what a moment in an area teaches that stays in that area (the rest reaches the core)
    dom_half=3.0,       # years for an area's offset to fade halfway back to the core
    dom_end_half=1.0,   # ... while that part of life is not held (no work, no faith)
    dom_cap=0.6,        # largest offset per color, in log-ratio units (about +-.1 on a share near .2)
    # a curious, thinking life rewarded (item 7, chroma-ideas/curious-life.md C2 to C4), behind curious=False:
    curious=True,
    cu_keep=0.7,         # C2: from cu_age, skill in Blue's ways fades this much more slowly (knowledge keeps into the 60s)
    cu_age=40.0,
    cu_late=0.004,       # C2: from 55, skill in Blue's ways above a beginner's meets competence (and half as much meaning) weekly
    cu_learn=0.03,       # C3: an act in Blue's ways that teaches something new meets meaning (and half as much autonomy),
                         # whether it works or not, by how much there was still to learn
    cu_ask_rate=0.01,    # C4 "the one people ask": grows weekly from 35 while Blue skill is high and Blue held, fades slowly
    cu_ask=0.004,        # C4: from 50 it meets belonging and meaning weekly, by how much they are asked
    # each person's own colour-to-need table (P4; the Game's engine-needs-and-steering.md §1 and §4), behind nm_on=False:
    # NMP starts as the shared table and moves with what feeds them, within a band, each colour's column kept at its total
    nm_on=True,
    nm_lr_moment=0.01,   # an act that worked feeds what was lacking: its colours' cells for the needs that lacked most grow
    nm_lr_habit=0.0005,  # the colours one keeps using while a need lacks are slowly tied to it
    nm_lr_goal=0.0005,   # a held dream, passion or plan ties its colours to its domain's needs, by its strength
    nm_band=(0.5, 2.0),  # each cell stays within this band of the shared value
    nm_back=10.0,        # years for the table to drift halfway back to the shared one, unless kept up
    ev_need_k=0.5,       # an outside event lands harder on a need already lacking (0: as before; P4 §4)
    ev_state_k=0.3,      # at peace and content, a bad event adds less stress; strained, more
    ev_reach_k=0.1,      # and the person reaches for the colours their own table ties to safety (strained) or belonging (calm)
    thr_vec='schwartz',        # item 7 C1 ("schwartz" from the stage 2 refit; blue-satisfaction.md): the threat focus reads the deep core on the Schwartz map
                         # (anxiety-based minus growth values, AXSEC_SW), not on Magic's security axis, which counted Blue as
                         # fully security. None: Magic's axis (v10-v22); or a 5-vector
    thr_axis=1.0,        # weight of the deep core's position on the security-vs-freedom axis (W U security, B R freedom)
    thr_hist=1.0,        # weight of recent hard events (wound, trouble)
    thr_react=0.5,       # weight of reactivity (temperament) above its even level
    thr_lag=1.0,         # years over which threat focus follows these
    app_k=0.4,           # appraisal: threat focus makes a loss weigh up to (1 + app_k) and a gain (1 - app_k); challenge the
                         # reverse; on mood, trouble and competence (Sortheix & Schwartz 2017: growth values, small +r with
                         # life satisfaction; anxiety-based values, small -r)
    app_learn=1.0,       # how far appraisal also reaches what an act teaches about one's ways (dI, dD); 0: feelings only
    # misjudged odds (logit units, on felt odds only; the true odds never change): 
    mis_focus=0.6,       # challenge reads odds high, threat reads them low: mis_focus x (0.5 - threat focus)
    mis_mem=0.4,         # memories of how acts in the same ways went (successes minus failures, by stakes)
    mis_scar=0.6,        # a never-again scar in the option's ways reads its odds low
    mis_mood=0.3,        # a good mood reads odds high, a low one low (affect as information: Schwarz & Clore 1983)
    mis_status=0.15,     # status held (summits, standings) reads odds high: hubris
    mis_expert=0.5,      # skill and career years in the option's ways shrink every misreading above toward the true odds
    mem_pos=5.0,         # half-life in years of a good memory's pull
    mem_neg=3.0,         # and of a bad one's (fading affect bias: the sting of bad memories fades faster; Walker 2003)
    mem_eps=1.0,         # memories (stakes-weighted acts) a color needs before they count fully in its reading
    scar_min=0.6,        # stakes from which a failure can leave a never-again scar
    scar_k=0.15,         # size of the scar, per stakes, in the act's ways
    scar_half=12.0,      # half-life in years of a scar (faster with support: x (1 + support))
    scar_pull=0.3,       # how much a scar turns a person away from options in those ways
    epi_min=0.75,        # logged lives keep an episode of any act that hit this hard (|delta|; about 1 act in 20)
    epi_recall=0.7,      # an episode comes back when its lean matches the act's and its fading strength is above this
    # played lives (implementation list item 4 and P3, stage 1): settings the game changes week by week while the life
    # runs (P is read live). At these values every life is as before; lives with no player never change them
    own_k=1.0,           # the character's own weekly lesson on the colours (dI); the game: about .5 in weeks without the player
    drift_k=1.0,         # the random drift of the colours (noise) and of the deep core (core_walk)
    ev_push_k=1.0,       # an outside event's push on the colours: personal events and read events
    era_push_k=1.0,      # an era's push on the colours when it begins
    steer=None,          # the player's steer before a pick: a colour mix (C, or N x C); the engine clears it once the pick is
    steer_k=1.0,         # drawn. It adds steer_k * (5 * m @ mix - 1) to each option's pull (1: a third of the values' pull)
    wfx_step=0.01,       # a world effect on a drifting quantity (money, freedom, safety) is reported once it moved this much
    dis_match=False,     # WL6: a disaster brings the outside events of its own hazard (a fire's, not a flood's); off: any
    # the times as a steady current (item 12; world-in-life.md §6, living-world.md §1), behind cur_on=False: each month
    # the colours of the world around them (people and groups, the places they are inside, the times) push a little, and
    # the push takes over part of the random drift, so lives change for reasons. Target: about 10% (8 to 12) of colour
    # movement, drift's share down by as much, 50-year stability toward .15 to .45
    cur_on=True,
    cur_k=0.01,          # the monthly push at full exposure, world on (v22.3 refit: .35 -> .01; at .35, .2 or .1 it pulled whole worlds
                         # to one colour, Green leading half the lives; held near zero until its own fit)
    cur_off=19.25,       # with the world off (tribal and magic settings), its size against cur_k: .19 a month, as fitted (.35 x .55)
    cur_mix=(0.5, 0.25, 0.25),   # the current's parts: close people, the places they are inside, the times (era and climate)
    cur_age=(0.3, 1.0, 20.0, 7.0),   # exposure by age: base + peak x exp(-((age - at) / width)^2); most at 15 to 25, never zero
    cur_mem=1.0,         # years over which what reaches them adds up (a new circle or job takes a while to tell)
    cur_cut=0.55,        # the share of the random weekly noise the current takes over (stability rows stay in their ranges)
    # with the world on, the current pushes by how a life's people and places differ from its society's and town's own
    # mix (chroma-engine/notes/current-green-pull/): a world's own lean (Modern Earth starts Green-first, and the burn-in
    # and like-matched parents add to it) is the ground they stand on, not a pull on everyone. Off: cur_k as above
    cur_rel=True,
    cur_rel_k=0.42,      # its monthly push at full exposure, world on (.35 x 1.2: about 9% of colour movement)
    cur_bal=0.5,         # its pull toward balance (log shares), so identities at 40 stay as with the current off
    cur_era=0.5,         # how much of the era the times' part carries (Emren 10-10 15:07 UTC, "Era at half"); the era
                         # also moves lives through era_push_k and the niche, and the culture through each generation's people
    # v22.5 F1, a body and a mind (Emren 10-11 11:25 UTC; chroma-ideas/realism/v22.5-realism-list.md), off until the v22.5
    # refit. body: health's body half from a constitution, the age, long-term conditions, short illnesses and injuries that
    # heal in weeks, serious illnesses, pregnancy, and habits by colour, strain, loneliness, money and care as tendencies
    # (BODY_PAR, H1 to H17). mind: a level built over months from strain, losses, wounds, loneliness, meaning and rest, with
    # low seasons, anxiety and numbing as threats and steadier picks and resilience as rewards (MIND_PAR). Each wears the
    # other; health, the one number every reader uses (needs, doors, retiring, the felt horizon, the bar), is their mean.
    # The Library's body and mind moments happen to them (BODY_MOMENTS, MIND_MOMENTS). Off: health as before
    body=False, body_par=None,   # body_par: values laid over BODY_PAR
    mind=False, mind_par=None,   # mind_par: values laid over MIND_PAR
    # v22.5 F2, death from the life, off until the v22.5 refit: with self_death on, the risk reads the body (an accident by
    # age and Red's risks, the body's own failing against the level for the age, a serious illness's course, a condition's
    # complications), the cause is what they had, and a death that is not sudden comes after a last decline the story
    # can tell (events: decline). Off: the life table x health, as before
    death_life=False, death_par=None,   # death_par: values laid over DEATH_PAR
    # v22.5, the many-lives fixes (chroma-ideas/realism/many-lives.md F14 to F19, Emren's cards 10-11 17:31 to 17:42 UTC), each
    # off here and in UPD_OFF until the v22.5 refit. Emren's rule (17:35 UTC): colour effects are mid-tendencies, never solid
    # limits; diverse pathways stay possible as rare options. The values beside each are the guesses the refit starts from
    # F14 colours settle with age: plasticity (and the want's pace) x a factor read off these (age, factor) points; real
    # personality changes most in youth and early adulthood and little from about 50 (rank-order stability plateaus in
    # midlife: Roberts & DelVecchio 2000). The factor also slows the outside world's steps (the current, blending in, the
    # mark of the work) and the deep core's slow walk. On: ((30, 1.0), (50, 0.3), (70, 0.1)), so the pie moves half as much
    # in a decade by 50 as at 30 and about a third after 70 (Emren's card: a quarter; breakthroughs and conversions carry
    # the rest, as a life's own turning points). None: as before
    set_age=None,
    set_big=1.0,         # a big event (a death, a conversion, prison, a breakdown, a rite) lifts openness (B, crisis units)
                         # above the person's usual; that lift lifts the factor back toward 1 by lift / set_big, so a big
                         # event can still turn a life at any age while the everyday ups and downs do not
    set_usual=5.0,       # years the person's usual openness averages over
    # F15 the start leaves a lean: the start's colours (up_mix, the game's upbringing) leave a lean of up_l0 of the way
    # from even toward them, full to up_from, then fading by half every up_half years (half by 35). What they want and who
    # they are are pulled toward the start only while their own lean is below that, by the shortfall, so a life can go
    # past it or overcome it (a lean, not a lock); and what those pulls added fades at the same pace from up_from, while
    # what the life made of it on its own stays. Children of a family keep a lasting lean toward its values that weakens
    # in adulthood (Bengtson 2013; Min, Silverstein & Lendon 2012)
    up_mix=None,         # the start's colours (a 5-vector); None: no start, no lean
    up_l0=0.3,           # the lean at its fullest: this share of the way from even (0.2 each) to the start's colours
    up_lean=0.0,         # weekly pull on the want at a full shortfall, as the game's own upbringing until 15 (.006); with it
                         # on, the game's stands down
    up_self=0.0,         # weekly pull on who they are at a full shortfall, x plasticity (on: .05, about the current's push)
    up_from=15.0, up_half=20.0,
    up_ease=0.0,         # the setup's own society (world_profile, f_world: the clan's, the towers') pulls at 1 - up_ease of
                         # its strength (on: .8), so the start's world is a lean too and other colours can lead some lives
                         # (the clan's White and Green come mostly from its seed library's options, which this leaves)
    # F16 colours shape the life course: each life's own lean toward partnering, children and a faith (drawn once, its own
    # random stream) and its colours tilt the life events, acts and titles that would start one (falling in love, a baby
    # on the way, a faith joined); a rate x exp(course_mu + own lean + tilt . (5 w - 1)), never 0, so no path closes. A
    # faith a family raises a child in is the start's (faith_inherit), not leaned
    course=False,
    course_mu=(-1.2, -0.3, -3.5),   # partner, children, faith: log of the middle life's rate. Real rates: 85 to 90% ever
                         # partnered, 80 to 85% parents; faith by world and start. Measured (72 Earth lives, world off and
                         # on, faith_inherit .6, mu children -0.6): partnered 88%, parents 71 to 73%, a faith 77 to 79%
    course_sd=1.5,       # spread of each life's own lean (log units)
    course_tilt=((0.15, -0.15, -0.1, 0.05, 0.15),   # partner: W U B R G, log rate per unit of a colour's lead (5 w - 1)
                 (0.15, -0.2, -0.15, 0.0, 0.2),     # children
                 (0.3, -0.25, -0.25, 0.0, 0.2)),    # faith
    drv_self=False,      # F9: each life event's drivers average 1 over the run's own lives (on: True); the Library's
                         # DRV_NORM was measured on calm lives with the world off
    risk_norm=False,     # F9: the body's and mind's risks on the Library's moments choose who, not how many (on: True)
    ev_fit=None,         # F9: {life event: factor} on its per_year, fitted to Release's rows (records/v22.5/scope.md)
    cond_once=False,     # F9.27: a condition they already have is not diagnosed a second time (on: True)
    ill_real=False,      # F9: the Library's body and mind moments come at their own rates, without event_scale (on: True)
    par_split=None,      # F9: the share of a breakup moment (SPLIT_SOFT, from 16) that ends a home together; the rest are
                         # a rough patch the couple weathers. None: every one ends it
    par_age=None,        # F9: a partnership (living together) starts as this share of the time by age, read off these
                         # (age, share) points; a younger love is a romance, not a home together. None: at any age
    mon_drift=0.01,      # F9.38: the share of the gap to the money a life's situation brings that closes each week (.01: about
                         # two years to most of the way; faster, a hard spell is felt sooner and passes sooner)
    lone=None,           # F9.39 loneliness: a spell of withdrawal from the first age point (about 1 adult in 20 is often
                         # lonely, more when single, out of work, low or ill; ONS 2018, Holt-Lunstad 2015). It starts by the yearly rate
                         # read off age's (age, rate) points x exp of single, work, low, ill (each 0 or 1 x its weight) and ends at out a
                         # year x exp(-.5 x the same); while it lasts the ties a life drifts to are keep x the people's and close rate of
                         # the gap a week (not .01). Own random stream. dict(age, single, work, low, ill, out, keep, rate); None: as before
    job_gap=None,        # F9.38: out of work after a job (working age, not retired) the pay stops at once: (cut, fall, years):
                         # for that many years after the job ends the money they drift to is cut lower (benefits replace
                         # little) and it falls at fall a week (savings run down in months), not mon_drift; None: as before
    pair_pay=None,       # F9.38: a couple living together shares its money: a partner at work adds this to the money the life
                         # drifts to (from 18); None: as before (each life's own pay only)
    pay_col=None,        # F9.40 (with low_pay): the colours lean a job's pay, at its draw: (mu, sd), each five weights on
                         # (5 w - 1): pay x exp(mu . (5 w - 1)), its spread x exp(sd . (5 w - 1)). None: even
    kid_tie=None,        # F9.39 (ties_people, world on): under 15 a child's ties are first its family's: at least this (the
                         # people model's own closeness builds over the first years, so on its own a child of 4 to 6 sits
                         # near nothing); None: as before
    tie_col=None,        # F9.40 (world on): the colours lean ties: tie_k x exp(tie_col . (5 w - 1)) (five weights). None: even
    low_pay=None,        # F9.38 low pay: (sd, rho, half): each job's pay x exp(sd z d - (sd d)^2 / 2), mean 1, z drawn at each
                         # job start or change of employer (rho of it the last job's: pay follows a life), d halving every half
                         # years in the job (low pay is mostly a first step: pay rises with experience); own stream. None: as before
    age_free=None,       # F9: [life event, ...] that come by their age window at their highest stage rate, not by the life stage
                         # reached (a stage can begin years after its window opens); "your first full-time job" for F9.38
    birth_par=None,      # F9.3 (with birth_age): a life's own births x this factor by the children it has living (0, 1, 2, ...;
                         # the last for more): fewer go on to a third or fourth child. None: as before
    ti_fit=None,         # F9: {title: factor} on its yearly rate (the Library's or the packs' rule), fitted to Release's rows
                         # (records/v22.5/scope.md); "living together" for F9.6. None: as written
    home_sale=1.0,       # F9.15: in a hard year under the need line, the home itself is sold in this share of cases (other
                         # holdings still go first); otherwise the household gets by, cutting back and borrowing. 1.0: always
    birth_free=False,    # F9.2 to F9.4 (with birth_age): a life's own births come by its age (the moment's age window, at
                         # its highest per_year), not by the life stage it has reached; birth_age's taper then shapes them
    job_move=None,       # F9.19: a working life changes employer at this yearly chance by age, read off these (age, chance)
                         # points (after a year in work, before retiring): the career goes on, the workplace and its
                         # people change (with the world on, the work setting is left and a new one joined). None: never
    # F17 deeds by canon: an option that leaves a deed (a mark) leans by the colours canon gives it (log odds per unit
    # of a colour's lead, DEED_CANON); off-canon leans (White breaking the law, Blue the most drugs, Green refusing people
    # in need) become soft tendencies the other way. 0: as before; on: 1.0
    deed_canon=0.0,
    deed_rare=0.0,       # rare deeds (DEED_RARE: an enemy, a hidden wrong, defying an authority) leave their mark on this
                         # share x stakes of the acts (on: .15), so a life holds a few, not fifty: most such acts pass
    # F19 a mind that matches life: children carry less stress than adults (the week's additions x the factor read off
    # these (age, factor) points; on: ((10, 0.5), (18, 1.0))), and contentment dips in midlife and rises after 60 (logit
    # points on satisfaction; on: ((45, 0.0), (50, -0.15), (58, 0.0), (68, 0.45), (80, 0.6)); Blanchflower 2021). None: as before
    mind_kid=None,
    mind_u=None,
)
# the v22.5 joint refit (notes/v22.5-refit-plan.md §5; 800 lives x 100 years, world on, seeds 41, 42, 45, 46, read by
# tools/v225_read.py against Release's F9 rows, records/v22.5/scope.md): every v22.5 switch on and its values fitted.
# UPD_OFF holds what each was before (with it, the lives are v22.4.1's)
V225 = dict(
    body=True,
    mind=True,
    death_life=True,
    hh_money=True,
    ties_people=True,
    one_roll=True,
    retire_ends=True,
    world_only=True,
    dream_grow=True,
    own_open=True,
    start_hold=True,
    set_age=((30, 1.0), (50, 0.12), (70, 0.02)),
    up_lean=0.006,
    up_self=0.05,
    up_ease=0.8,
    course=True,
    deed_canon=2.0,
    deed_rare=0.15,
    mind_kid=((10, 0.5), (18, 1.0)),
    mind_u=((45, 0.0), (50, -0.15), (58, 0.0), (68, 0.45), (80, 0.6)),
    death_par=dict(frail=(1.4e-06, 0.125), frail_k=1.5, ser_age=0.012, frail_c=0.0002),
    course_mu=(-0.55, -0.2, -3.5),
    pension_k=0.45,
    pension_base=0.15,
    drv_self=True,
    risk_norm=True,
    par_age=((16, 0.0), (19, 0.35), (24, 1.0)),
    tie_k=1.75,
    par_split=0.06,
    ill_real=True,
    kid_cost=0.07,
    hh_cls=(0.12, 0.3, 0.55),
    ev_fit={'losing your job': 0.45,
            'a serious accident or illness': 0.6,
            'a long dark season': 0.65,
            'an addiction takes hold': 0.63,
            'living with a chronic illness': 0.75,
            'your first full-time job': 1.5,
            'a new job at last': 0.35,
            'buying a home': (1, 1, 1.8, 1.0, 0.7, 0.07),
            'divorce after twenty years': 0.5,
            'a child is born': 0.25,
            'a baby on the way, planned or not': 0.35},
    set_big=6.0,
    cond_once=True,
    job_move=((18, 0.22), (25, 0.14), (35, 0.08), (45, 0.05), (55, 0.03), (64, 0)),
    birth_free=True,
    home_sale=0.08,
    ti_fit={'living together': 4.5},
    birth_par=(1, 1, 0.4, 0.22, 0.1, 0.05),
    age_free=('your first full-time job',),
    mon_drift=0.015,
    lone=dict(age=((13, 0.02), (16, 0.01), (18, 0.003), (25, 0.007), (30, 0.012), (35, 0.014), (50, 0.014), (60, 0.012),
                   (70, 0.008), (80, 0.004), (95, 0.003)), single=0.7, work=0.5, low=1.0, ill=0.4, out=0.35, keep=0.05, rate=0.05),
    low_pay=(0.7, 0.3, 3.0),
    pay_col=((0.0, 0.08, 0.04, 0.0, 0.0), (0.0, 0.4, 0.1, 0.0, 0.0)),
    tie_col=(0.3, 0.0, 0.0, 0.0, 0.05),
    kid_tie=0.6,
    job_gap=(0.15, 0.05, 2.0),
    pair_pay=0.12,
    c_par=dict(sold=0.03, merged=0.015),
    eyes_par=dict(odd_vmem=0.05),   # S4: the spread of their places' shares learnt over about twenty years (world_people)
)
DEFAULT.update(V225)
# F17: the canon lean of each deed (W U B R G, log odds per unit of a colour's lead); deeds not named keep the Library's
DEED_CANON = {"broke the law": (-0.6, 0.0, 0.4, 0.4, -0.2), "used drugs": (-0.4, -0.4, 0.3, 0.5, 0.0),
              "refused someone in need": (-0.4, 0.0, 0.6, 0.0, -0.6), "broke your word": (-0.6, 0.0, 0.4, 0.3, -0.3),
              "took a wild risk": (-0.3, -0.2, 0.0, 0.6, -0.2)}
DEED_RARE = ("made an enemy", "hid a wrong", "defied an authority")

# generic outside events the Library batch covers with its own life events (dropped when a batch is loaded)
EV_DROP = {"moving somewhere new", "a mentor takes you under their wing", "an illness", "an unexpected windfall or loss of money",
           "a natural disaster hits where you live", "a hard season of scarcity", "a season of plenty", "a brush with death"}
# the channel a life event the world made likelier is reported in (wfx), by its kind (world_link.RK)
WFX_OPT = (0.25, 0.02)   # option_causes names a closure from this many units (access x .6 per unit), odds from this added difficulty
WFX_RISK = {"illness": "illness risk", "old_death": "death risk", "disaster": "disaster risk", "crime": "crime risk",
            "war": "war risk", "pandemic": "illness risk", "jobloss": "job loss risk"}
KILL_OFF = np.array([29.0, 0.0, 0.0, 55.0, 1.0, -29.0])         # how much older than the person each role is, on average
# (a child's death reads the children's own ages instead: the years since the first was born, kid_mort and infant_mort)
KILL_HIT = np.array([(0.1, 0.3), (0.1, 0.3), (0.1, 0.2), (0.05, 0.15), (0.4, 0.5), (0.3, 0.6)])   # belonging lost, stress, per role

# v7 switches off: run(P=V6_SWITCHES) reproduces engine v6 on the seed library
V6_SWITCHES = dict(goals=False, hz_k=0.0, hz_want=0.0, disc_rate=0.0, disc_win=0.0, disc_tag=0.0, roles=False, read_moment=(0.0, 0.0),
                   sat_mid_stage=(0.6, 0.66, 0.7, 0.7, 0.7, 0.7), mid_years=0.0, sat_hope=0.0, hz_calm=0.0,
                   retire_hz=None, faith_own_age=0.0, faith_drift=None, tw_trans=0.0, tw_core=0.0, tw_pull=0.0, tw_pen=0.0,
                   stiffen=0.7, ev_gap=False, season=False, retire_season=False, sat_gap_ref=0.07, gap_keep=False)
# turning points off (point 7, 2026-10-05): the deep core as it was before Emren chose them
TW_OFF = dict(tw_trans=0.0, tw_core=0.0, tw_pull=0.0, tw_pen=0.0, stiffen=0.7, sat_gap_ref=0.07)
# sex and gender (N1b) off: sex half and half, unease 1 in 100, one came out mark for both, no role (point 11 as it was)
ID_OFF = dict(id_v2=False)
FIX_OFF = dict(title_ages=False, season_share=False, ow_weeks=52, far_share=1.0, recon_held=False, child_norm=False)   # release fixes that change lives (C-X4, Library next3 §4)
# interpretation and memory off (E1): the v10 weights that change lives, at 0
V10_OFF = dict(app_k=0.0, app_learn=0.0, mis_focus=0.0, mis_mem=0.0, mis_scar=0.0, mis_mood=0.0, mis_status=0.0, scar_k=0.0,
               scar_pull=0.0)
# the next update's new mechanics off and its refitted values at v22.1's (implementation list; Release's C-E14 rule, 10-09):
# each stage adds its switches here and names them in the engine CHANGELOG
# births by the parent's age (birth_age): births a year per 1,000 women and per 1,000 men at each age (US NCHS natality,
# mothers 2019 and fathers' age-specific rates), read as a share of the peak; own births only
FERT_F = ((15, 0.0), (17, 17), (22, 66), (27, 93), (32, 98), (37, 52), (42, 12), (47, 1), (51, 0.0))
FERT_M = ((15, 0.0), (17, 8), (22, 60), (27, 95), (32, 100), (37, 60), (42, 25), (47, 9), (52, 3), (57, 1), (62, 0.0))
BIRTH_OWN = ("a child is born", "a baby on the way, planned or not")   # the moments of a life's own births
BIRTH_NOT = re.compile(r"adopt|foster|take (?:them )?in|surrogate|clinic|donor", re.I)   # other ways to a child


def toward(lv, m):
    """v22.5 F1: a level lv (0 to 1) moved by m: one for one going down (to .01), with diminishing returns going up, so a
    strong body or a steady mind nears 1 without passing it."""
    return np.where(m < 0, np.maximum(lv + m, 0.01), lv + (1 - lv) * (1 - np.exp(-np.maximum(m, 0) / (1 - lv))))


def fert(age, table):
    """A year's chance of a birth at this age as a share of the peak age's (FERT_F, FERT_M)."""
    xs, ys = zip(*table)
    return np.interp(age, xs, ys) / max(ys)


# v22.5 F1, a body and a mind (chroma-ideas/realism/v22.5-realism-list.md; Emren 10-11 11:25 UTC; the modifiers are
# chroma-ideas/means/modifiers.md H1 to H17). Rates are a year, sizes in health units (0 to 1). Every colour lean is a
# tendency, never a limit (Emren 10-11 17:35 UTC): a colour's share above or below the even .2, per .2, times its lean,
# so a life far into one colour moves a few points, and no colour closes or guarantees anything. The values are
# estimates for the one v22.5 refit (no part is tuned on its own before it). W U B R G in every 5-tuple.
BODY_PAR = dict(
    con_sd=0.035, con_frail=(0.04, 0.08),   # H1 constitution, lifelong: robust around 0 (sd); a few frail (share, extra loss)
    age=((0, 0.90), (25, 0.95), (35, 0.95), (60, 0.86), (70, 0.78), (80, 0.66), (90, 0.50), (100, 0.30)),   # H2 the body's
                             # level by age, alone (conditions, illness and injury come off it)
    base_half=1.0,           # R2 two speeds: years for the body's slow level to move halfway to where the life puts it
    ill_rate=((3, 2.0), (10, 1.5), (16, 1.0), (60, 0.8), (80, 1.2), (100, 1.5)),   # H4 short illnesses a year (flu, a bug)
    ill_size=(0.08, 0.22), ill_half=1.5,    # H4 a dip (drawn between) and the weeks it takes to halve
    inj_rate=((3, 0.10), (15, 0.12), (25, 0.08), (65, 0.06), (80, 0.15), (100, 0.25)),   # H5 injuries a year (falls late)
    inj_size=(0.12, 0.35), inj_half=5.0,    # H5 a dip and the weeks it takes to halve
    inj_keep=(0.1, 0.03),    # H5 the share of injuries that leave a lasting mark on the body, and its size
    cond_young=0.06,         # H3 a long-term condition from birth or early childhood (with the moments, about 1 in 8 by 16)
    cond_size=(0.03, 0.12),  # H3 a condition's weight on the body (drawn between; a second one adds)
    cond_max=0.25,           # the most the conditions together take
    cond_ease=0.03,          # H3 a young person's condition eases (asthma often does): a yearly chance, to 18
    cond_rate=((12, 0.004), (30, 0.008), (50, 0.02), (70, 0.035), (100, 0.04)),   # H3 without the Library's moments
    ser_size=(0.25, 0.45),   # H6 a serious illness: the dip while it lasts
    ser_months=(3, 24),      # H6 how long it lasts (treatment, recovery)
    ser_keep=(0.02, 0.08),   # H6 what it takes from the body for good, if they come through
    ser_rate=((35, 0.0), (45, 0.003), (60, 0.008), (75, 0.015), (100, 0.02)),   # H6 without the Library's moments
    preg=0.10, preg_half=8.0,   # H7 pregnancy and a birth: a dip, and the weeks it takes to halve
    # H8 to H10 habits by colour: rest and sleep (Blue's late nights, Red burning the candle; Green and White rest), moving
    # the body (Red and Green move, Blue sits, Black trains), moderation (White moderate, Red and Black indulge)
    rest=(0.02, -0.03, 0.0, -0.02, 0.02), move=(0.0, -0.02, 0.01, 0.03, 0.02), moderate=(0.02, 0.0, -0.01, -0.03, 0.0),
    disc=0.02,               # learned self-control holds the habits up: x (discipline - 1)
    care=(0.25, 0.25, 0.0, -0.1, -0.15),   # H11 early care (W keeps appointments, U reads the signs, G trusts the body too long):
                             # this share shorter dips and lighter serious illness
    heal=(0.0, 0.0, 0.0, 0.1, 0.25),       # how much faster dips heal: Green heals well, Red bounces back
    risk=(-0.1, 0.0, 0.1, 0.5, 0.15),      # H5 injury risk (log units): Red's risks and sport, Green outdoors
    strain=0.08, strain_from=0.4, strain_years=3.0,   # H12 years of strain (stress above this, a slow average) wear the body
    lonely=0.06, lonely_line=0.7,   # H13 few people: the level falls by up to this (belonging under the line)
    money=0.05, money_years=3.0,    # H14 money and class: +- this from the poorest to the best off (slow average; a child's
                                    # family's class with the world on); poorer lives also heal slower
    care_load=0.03,          # H16 years of caring for someone (world on): up to this at 20 hours a week
    mind_wear=0.12,          # each wears the other: a low mind (under .6) pulls the body's level down by up to this
    ill_mind=0.5,            # and a low season or anxiety makes short illnesses this much likelier
    moments=True,            # the Library's own body moments happen to the body: a diagnosis is a serious illness, "living
                             # with a chronic illness" a condition, a serious accident an injury or an illness
    risk_k=2.0,              # the body's risks on those moments: x exp(risk_k x (the level for the age - the body)), at most x2
)
# what each of the Library's body and mind moments is (moments=True); the engine's own rates stand in where a Library has none
BODY_MOMENTS = {"living with a chronic illness": "condition", "growing up with an illness": "condition",
                "the body remembers the wild years": "condition", "a frightening diagnosis": "serious",
                "a serious accident or illness": "accident or illness", "a fall at home": "injury",
                "burnout": "burnout"}
MIND_MOMENTS = {"a long dark season": "low", "a sadness that will not lift": "low", "burnout": "low",
                "an addiction takes hold": "numb"}
CO_TITLES = ("living together", "wife or husband", "married again", "partner of many years",
             "spouse in a family-arranged marriage")   # a home together (F9.6; pair_pay)
SPLIT_SOFT = ("a breakup",)   # F9 par_split: the young couple's moments that may end a home together or pass
COND_KINDS = ("asthma", "diabetes", "arthritis", "chronic pain", "heart condition", "epilepsy")
COND_P = ((0.45, 0.15, 0.0, 0.05, 0.05, 0.3), (0.1, 0.3, 0.3, 0.15, 0.15, 0.0))   # which, as a child and as an adult
COND_LETHAL = (0.3, 1.0, 0.0, 0.0, 1.5, 0.3)   # how far each condition's complications can end a life (F2; arthritis and pain do
                                               # not, they wear the body)
COND_DEATH = ("of a severe asthma attack", "of complications of their diabetes", "", "", "of heart failure", "of a seizure")
SER_KINDS = ("cancer", "heart disease", "a stroke", "lung disease")
MIND_PAR = dict(
    start=0.82,              # a young child's mind (the family holds it up)
    level=0.78,              # where the mind settles with nothing pulling it
    half=13.0,               # weeks for the mind to move halfway: it is built over months
    mood=0.4, content=0.2,   # a person's usual mood and how content life is, above or below their references, lift it
    mood_ref=0.7, content_ref=0.7,
    strain=0.2, strain_from=0.4,   # months of strain: stress above this (a three-month average)
    loss=0.07,               # losses and hard blows (the wound, to 1.5)
    scar=0.02,               # hurts built up over the years (the scars, to 3)
    lonely=0.12, lonely_line=0.7,  # few people: belonging under the line
    meaning=0.3,             # the meaning need above or below .9
    rest=0.04,               # rest: time left over under .15 drains the mind
    body=0.2,                # each wears the other: a body under .7 pulls the mind down by this x the gap
    low_dip=0.20, low_months=(2, 9),     # a low season: its weight on the mind and how long it lasts
    anx_dip=0.12, anx_months=(1, 6),     # anxiety
    numb_dip=0.08, numb_months=(3, 18),  # numbing (drink, pills, a screen all night): relief now, cost later
    low_rate=0.012, numb_rate=0.006,     # a year at an even mind, where a Library has no such moment
    anx_rate=0.02,           # a year at an even mind (no Library moment tells it)
    risk_k=3.0,              # each threat is likelier as the mind falls: x exp(risk_k x (.75 - mind)), at most x3, on the
                             # moments too
    steady=0.004,            # steadier picks: an act that works and fits who they are lifts the mind this much
    resil=0.1, resil_max=0.5,   # resilience: coming through a threat with people around adds this (to the max); it wards off
                             # the threats and shortens them
    moments=True,            # the Library's own mind moments start a threat: a long dark season, a sadness that will not
                             # lift, burnout, an addiction
    mind_w=0.5,              # health, the one number everything reads: (1 - mind_w) x body + mind_w x mind
)
# v22.5 F2, death from the life: the character's death risk reads the body, and the cause is what they had
DEATH_PAR = dict(
    acc=((0, 2e-4), (15, 2.5e-4), (20, 5e-4), (30, 3e-4), (70, 3e-4), (85, 1.2e-3), (100, 3e-3)),   # accidents a year
    acc_red=0.3,             # Red's risks: x exp(acc_red x (Red - .2) / .2)
    frail=(1.7e-5, 0.09),    # the body's own failing, a e^(b age) a year at the level for the age (Gompertz)
    frail_k=2.5,             # x exp(frail_k x (the level for the age - the body)): a weaker body fails sooner
    sudden=0.5,              # before old age, this share of a failing body goes at once (a heart attack, a stroke); the
                             # rest fail over weeks, of their heaviest condition or else of heart failure
    old_age=85.0,            # from this age a failing body with nothing named is old age
    frail_c=0.0,             # v22.5 F9.35: from 15, a failing body's background a year beside the Gompertz term (Makeham):
                             # the young who die of an illness, not only of an accident
    ser_fatal=dict(cancer=0.4, **{"heart disease": 0.15, "a stroke": 0.2, "lung disease": 0.4}),   # a serious
                             # illness's course ends in death this often (at 60, with the body at its age's level)
    ser_age=0.02, ser_age_lim=(0.4, 2.0),   # x (1 + this x (age - 60)), within these: the young come through more often
    cond_k=0.005,            # a condition's complications: its weight x this x e^(.06 (age - 50)) a year
    decline=dict(old=(12, 52), serious=(4, 20), condition=(8, 30)),   # weeks of the last decline, by what ends the life
)


UPD_OFF = dict(dis_match=False,
               # stage 2 (who they become): enemy pairs, shadows, threat axis and aging pull, life areas, a curious life,
               # each person's need table and events by need and state
               drift_frames=None, ends_frames=None, ten_bad=0.2, shadows=False, thr_vec=None,
               hz_self=0.0, hz_want=0.03, domains=False, curious=False, nm_on=False, ev_need_k=0.0, ev_state_k=0.0,
               ev_reach_k=0.0, cur_on=False, cur_rel=False,
               # stage 3, LW1 and LW2 (stage3-rules.md §8)
               cult_schools=False, cult_scenes=False, cult_adults=False, cult_anchor=False, cult_pushback=False,
               cult_shake=False, cult_no_dice=False, hist_party_gov=False, hist_pressure=False, hist_grievance=False,
               hist_chance_only=False,
               # stage 2 of v22.3, the spheres of society (item 15)
               sph_town=False, sph_haunts=False, sph_hours=False, sph_marks=False, sph_events=False,
               sph_seasons=False, sph_joins=False, sph_pairs=False, inst_even=False, sph_links=False,
               sph_memory=False, pair_calm=False, sph_cascades=False, sph_levers=False, sph_fair=False,
               sph_shadow=False, sph_deep=False, far_ties=False, sph_titles=False, fair_read=False, lead_ways=False,
               sph_eyes=False, sph_odd=False, sacred=False, seen_done=False,
               # item 11, the world in their life: WL2's small effects
               wl2=False, near_gate=False,
               # late births: a life's own births by real fertility for its age and sex
               birth_age=False,
               # what one holds is practice too
               role_practice=False, read_skill=0.0, lens_want=0.0, app_vigil=False, sh_will=0.0, cur_will=0.0, gap_move=0.0,
               # v22.4: a refused first job or job move re-draws to the next-best fit
               acc_redraw=False, green_jobs=False,
               # item 10, the C hooks (chroma-world/model/stage3-rules.md section 5)
               c3_inst=False, c4_nature=False, c5_faith=False, c2_groups=False,
               # the K limits' rule fixes (b-package.md K2 newcomer, K6 season steps)
               move_near=False, season_excl=False,
               # v22.5 F1 a body and a mind, F2 death from the life
               body=False, mind=False, death_life=False,
               # values the v22.5 refit changed (V225)
               death_par=None, course_mu=(-1.2, -0.3, -3.5), pension_k=0.3, pension_base=0.0, tie_k=1.0,
               kid_cost=0.12, hh_cls=(0.12, 0.30, 0.55), set_big=1.0, eyes_par=None,
               # v22.5, the many-lives fixes (F14 to F17, F19)
               set_age=None, up_lean=0.0, up_self=0.0, up_ease=0.0, course=False, par_age=None, par_split=None, job_move=None, birth_free=False, home_sale=1.0, ti_fit=None, birth_par=None, age_free=None, mon_drift=0.01, lone=None, low_pay=None, pay_col=None, tie_col=None, kid_tie=None, c_par=None, job_gap=None, pair_pay=None, ev_fit=None, ill_real=False, cond_once=False, risk_norm=False, drv_self=False, deed_canon=0.0, deed_rare=0.0,
               mind_kid=None, mind_u=None,
               # v22.5 realism (chroma-ideas/realism/v22.5-realism-list.md): F6 dreams that grow up, F12 the world and
               # the start hold
               dream_grow=False, own_open=False, start_hold=False,
               # v22.5 realism F3: a household and real people
               hh_money=False, ties_people=False,
               # v22.5 realism F8 and F10: retirement ends work; a world moment only on the world's event
               retire_ends=False, world_only=False,
               # v22.5 realism F7: one roll of the living
               one_roll=False,
    # the v22.3 refit's satisfaction level (the new mechanics lift satisfaction; the set point moved .80 -> .86)
    sat_mid=0.8)
# everything since the go-live off, for the identity check (C-E14): lives then equal engine_v9_golive.py
GOLIVE = {**V10_OFF, **ID_OFF, **FIX_OFF, **UPD_OFF, "world": False}
ROLE_BY_SETTING = dict(earth=0.3, tribal=0.7, magic=0.5)     # role_strict when None (estimates; ISSP 2012, WVS 7)
ACCEPT_BY_SETTING = dict(earth=0.5, tribal=0.3, magic=0.5)   # accept_trans when None (estimates)

# v7 adjectives (Emren's point 3): plain states read from the meta variables, needs and resources. The Library can use
# them in conditions (is_happy, adj('wealthy')) and in an act's or a situation's requires:, like perks; the game shows
# them. Each reads its value over the last few months (adj_smooth); it holds from when that passes `on` until it falls
# back past `off`, so it does not flicker. Thresholds give the share among adult Earth lives in the last column
# (calib_v7/adj_fit.py). Health states (fit, frail) wait for the aging body: health is still the same for everyone of an age. `without`: what a missing state does to an
# act that requires it, unless the act says otherwise (impossible: not offered; means: pickable, but harder).
# name, the words a sentence uses, variable, side (+1 high, -1 low), on, off, from age, without, adult share
ADJECTIVES = [
    ("happy", "happy", "content", +1, 0.741, 0.675, 0, "impossible", 0.25),
    ("unhappy", "unhappy", "content", -1, 0.364, 0.435, 0, "impossible", 0.12),
    ("calm", "at peace", "peace", +1, 0.621, 0.588, 0, "impossible", 0.18),
    ("restless", "restless", "peace", -1, 0.275, 0.324, 0, "impossible", 0.1),
    ("stressed", "under strain", "stress", +1, 0.809, 0.667, 0, "impossible", 0.18),
    ("excited", "excited", "mood", +1, 0.448, 0.366, 0, "impossible", 0.1),
    ("low", "low", "mood", -1, -0.0368, -0.00128, 0, "impossible", 0.1),
    ("hurting", "hurting", "wound", +1, 0.777, 0.581, 0, "impossible", 0.1),
    ("unfulfilled", "unfulfilled", "unmet_hope", +1, 0.345, 0.291, 18, "impossible", 0.1),
    ("lonely", "lonely", "belonging", -1, 0.559, 0.634, 0, "impossible", 0.11),
    ("adrift", "adrift", "meaning", -1, 0.828, 0.861, 12, "impossible", 0.1),
    ("insecure", "insecure", "safety", -1, 0.305, 0.372, 16, "impossible", 0.1),
    ("wealthy", "wealthy", "money", +1, 0.454, 0.41, 18, "means", 0.1),
    ("poor", "short of money", "money", -1, 0.0332, 0.0645, 18, "impossible", 0.15),
    ("stretched", "stretched thin", "time", -1, 0.0502, 0.1, 16, "impossible", 0.1),
    ("hemmed in", "hemmed in", "freedom", -1, 0.295, 0.359, 16, "impossible", 0.06),
    ("well connected", "well connected", "ties", +1, 0.852, 0.791, 12, "means", 0.15),
    ("disciplined", "disciplined", "discipline", +1, 1.22, 1.19, 12, "means", 0.15),
    ("impulsive", "impulsive", "discipline", -1, 0.882, 0.937, 12, "impossible", 0.1),
    ("searching", "searching", "gap", +1, 0.148, 0.138, 12, "impossible", 0.1),
    ("settled", "settled in who they are", "gap", -1, 0.0624, 0.0706, 12, "impossible", 0.1),
]
SH_STATES = ["rigid", "indecisive", "ruthless", "reckless", "stuck in their ways"]   # W U B R G
ADJ_BASE = len(ADJECTIVES)   # the adjectives before the shadow states (the outputs with shadows off)
# the five shadow states (stage 2, item 2), read like the adjectives (holds: rigid) and indexed after them: ADJ_ALL is the
# whole table (ADJ_NAMES, ADJ_ID, ADJ_SAY follow it); ADJECTIVES stays the 21 states, never held by the shadows
SH_ADJECTIVES = [(nm_, nm_, "shadow_" + c_, +1, 0.5, 0.35, 18, "impossible", 0.05) for nm_, c_ in zip(SH_STATES, "WUBRG")]
ADJ_ALL = ADJECTIVES + SH_ADJECTIVES
ADJ_NAMES = [a_[0] for a_ in ADJ_ALL]; ADJ_ID = {nm: i for i, nm in enumerate(ADJ_NAMES)}
ADJ_SAY = [a_[1] for a_ in ADJ_ALL]
ADJ_WITHOUT = np.array([("law", "approval", "means", "impossible").index(a_[7]) for a_ in ADJ_ALL])


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def centre(x):
    return x - x.mean(axis=-1, keepdims=True)


CHANNELS = ["instrumental", "scarcity", "social", "coherence", "upkeep", "conversion", "drift", "breakthrough", "outside world"]
# what moves the want (aspiration), tracked so a person's shift demand can be explained by its sources
ASOURCES = ["unmet needs", "surroundings", "role models", "settling back", "turning points", "talking oneself into it",
            "resolutions", "outside events", "the times", "discontent", "contentment", "restlessness", "dreams and plans",
            "a shorter horizon"]
AS_WEEKLY = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13]  # sources that act every week, in the order they are stacked

# v7 goals: dreams (before adulthood, and later sparks), passions (a dream sealed by a rite) and plans (adult, with a horizon)
G_KINDS = ["dream", "passion", "plan"]
HORIZONS = ["week", "year", "five years", "life"]
HORIZON_W = [1, 52, 260, None]                   # None: until the end a life goal is planned against
G_SOURCES = ["family", "circle", "story", "spectacle", "stranger", "resolution", "passion", "need", "old dream", "dream", "player"]
GSRC = {nm: i for i, nm in enumerate(G_SOURCES)}
TRIG_SRC = np.array([GSRC[tr[1]] for tr in DREAM_TRIGGERS])
TRIG_W = np.array([tr[2] for tr in DREAM_TRIGGERS], float)            # triggers x stages
TRIG_TILT = np.array([parse(tr[3]) if tr[3] else np.zeros(C) for tr in DREAM_TRIGGERS])
STEP_INC = 0.5       # progress a person imagines one good step brings, in units of a plan's size (fit x stakes)
# v7 felt horizon: the color ends that limited time favors. Derived from the Schwartz map (schwartz.LOAD): the colors whose
# values rise with age in surveys (conservation, self-transcendence) against those that fall (openness, self-enhancement)
HZ_TILT = np.array([0.96, 0.05, -1.0, -0.62, 0.61])
# next version (Blue): where the deep core sits between anxiety-based and growth values on the Schwartz map, for the threat
# focus: schwartz.LOAD, self-protection (power, security, conformity, tradition) minus growth (self-direction, stimulation,
# benevolence, universalism), scaled to 1 (Schwartz 2012; Sortheix & Schwartz 2017, the source the v10 layer cites)
AXSEC_SW = np.array([1.0, 0.526, -0.842, -0.737, 0.053])
HZ_ROLE = np.array([1.0, 1.0, 1.0, 0.4, 1.5, 1.5])   # how strongly each death reminds: parent, sibling, friend, grandparent, partner, child


def step_prior(L, P):
    """Weekly chance of a step into each commitment's domain at each life stage, as a person would know it from those
    around them (before they have lived that stage): life events at their base rates, plus everyday situations."""
    has = np.stack([(L["COMMIT"] == d_).any(1) for d_ in range(NK)], 1).astype(float)     # S x NK
    out = np.zeros((NS, NK))
    for st in range(NS):
        on = L["STG"][:, st]
        ev = L["PERY"][:, st] * on * P["event_scale"] / 52
        day = on & (L["PERY"].sum(1) == 0)
        rate = L["RATE"] * day; rate = rate / max(rate.sum(), 1e-9) * max(0.0, 1 - ev.sum())
        out[st] = (ev + rate) @ has
    return out


def _cdf_below(n, term, step, aux):
    """Speed pass (10-08): the sum of the first n terms of each element, the next term from step(term, j, aux) (aux:
    the element's own number the step reads). Each element goes through exactly the operations of the full-array loop it
    replaces, but only while it still adds terms (the full loop added 0.0 after that, which changes nothing), so the
    result is bit for bit the same. Longest first, so the elements still adding terms are always the first K."""
    nf = n.ravel(); cf = np.zeros(nf.size)
    idx = np.nonzero(nf > 0)[0]
    idx = idx[np.argsort(-nf[idx], kind="stable")]
    n_ = nf[idx]; t_ = term.ravel()[idx]; a_ = aux.ravel()[idx]; c_ = np.zeros(idx.size); K = idx.size; j = 0
    while K:
        c_[:K] = c_[:K] + t_[:K]
        t_[:K] = step(t_[:K], j, a_[:K])
        j += 1
        while K and n_[K - 1] <= j:
            K -= 1
    cf[idx] = c_
    return cf.reshape(n.shape)


EV_G = {"__builtins__": {}}   # speed pass: one globals dict for every condition (eval adds nothing to it)


def poisson_at_least(n, lam):
    """P(X >= n) for X ~ Poisson(lam), elementwise (n whole, small)."""
    n, lam = np.broadcast_arrays(np.asarray(n, int), np.maximum(np.asarray(lam, float), 1e-12))
    term = np.exp(-lam)
    cdf = _cdf_below(n, term, lambda t_, j, l_: t_ * l_ / (j + 1), lam)
    return np.where(n <= 0, 1.0, np.clip(1 - cdf, 0, 1))


def negbin_at_least(n, lam, kappa):
    """P(X >= n) for X with mean lam whose rate is itself unsure (negative binomial, shape kappa), elementwise."""
    n, lam = np.broadcast_arrays(np.asarray(n, int), np.maximum(np.asarray(lam, float), 1e-12))
    q = lam / (kappa + lam); term = (1 - q) ** kappa
    if np.ndim(kappa):   # (never in the engine: kappa is one number) the plain loop
        cdf = np.zeros(lam.shape)
        for j in range(int(n.max()) if n.size else 0):
            cdf = cdf + np.where(j < n, term, 0.0)
            term = term * (j + kappa) / (j + 1) * q
    else:
        cdf = _cdf_below(n, term, lambda t_, j, q_: t_ * (j + kappa) / (j + 1) * q_, q)
    return np.where(n <= 0, 1.0, np.clip(1 - cdf, 0, 1))


def felt_odds(chance, p_step, weeks, steps, domain, outlook, P=None):
    """The person's own odds of reaching a goal in time: how often they believe a chance comes (per week), how likely they
    believe a step works, the weeks left and the good steps still needed. They expect to take a share of their chances
    that grows with their sense of control, and they leave out what will get in the way: busy weeks, stress, their own
    pull elsewhere (the planning fallacy: Buehler, Griffin & Ross 1994). A domain goal (a partner, a career) needs one
    good step that sticks."""
    P = P or DEFAULT
    take = P["felt_take"][0] + P["felt_take"][1] * np.asarray(outlook)
    lam = np.asarray(chance) * np.asarray(p_step) * take * np.maximum(weeks, 0)
    kap = P.get("felt_kappa") or 0.0
    if kap:   # v7: they are not sure how often chances will come, so even a likely plan never feels certain
        return np.where(np.asarray(domain) >= 0, 1 - (1 + lam * P["felt_cp"] / kap) ** -kap, negbin_at_least(steps, lam, kap))
    return np.where(np.asarray(domain) >= 0, 1 - np.exp(-lam * P["felt_cp"]), poisson_at_least(steps, lam))
GROUP = np.array(AXES["group vs individual"], float)     # Magic's group (W, G) versus individual (B, R) axis


def _run(N=1000, years=80, seed=0, P=None, record_every=52, intervention=None, lib=None, log_lives=(), pausing=False):
    # the whole simulation; run() and run_steps() below call it. With pausing=True it pauses six times a week
    # (PAUSES); with pausing=False it never pauses and runs exactly as run() always did.
    P = {**DEFAULT, **(P or {})}
    NMAP = NMAP_V6 if P["aut_self"] else NMAP_V5
    SP_ = np.asarray(P["stage_p"], float) if P["stage_p"] is not None else STAGE_P    # plasticity by life stage
    rng = np.random.default_rng(seed)
    L = lib if lib is not None else LIB
    FR = FRAMINGS[P["framing"]] if isinstance(P["framing"], str) else np.asarray(P["framing"], float)
    FRpos = np.maximum(FR, 0)
    # default ends: serve your method colors, and (only if the culture frames them as
    # opposed) work against the opposed colors
    FRN_ = P["framing"] if isinstance(P["framing"], str) else None
    in_fr = lambda key: P[key] is None or FRN_ is None or FRN_ in P[key]   # a custom matrix keeps both
    Eeff = L["E"] if not in_fr("ends_frames") else \
        np.where(L["OVR"][..., None], L["E"], L["E"] - 0.25 * np.einsum("ij,skj->ski", FRpos, L["M"]))
    MU_ = P["mu"] if in_fr("drift_frames") else 0.0
    T = years * 52
    z = np.zeros((N, C)); k = np.zeros((N, C)); v = np.zeros((N, C))
    M = np.zeros(N); D = np.zeros((N, C)); J = np.zeros((N, C, C))
    sig = np.full((N, C), 0.3); SE = np.full((N, C), 0.5)
    need = np.full((N, NJ), 0.6); fb = np.zeros((N, C))
    nimp = np.ones((N, NJ))                                 # v6: how much each need matters to the person (accommodation)
    nic = np.tile(P["world_profile"], (N, 1)).astype(float)
    if P["family_conc"]:   # v6: each child is born into a family with its own ways (the person still starts at 0.2 each)
        wp_ = np.asarray(P["world_profile"], float); wp_ = wp_ / wp_.sum()
        nic = rng.dirichlet(P["family_conc"] * C * wp_, N)
    turn_pm = np.exp(rng.uniform(np.log(P["turn_spread"][0]), np.log(P["turn_spread"][1]), N))   # v6: rooted vs mobile lives
    circle = nic.copy()                                       # v6: the mix the people currently around you bring
    fam = nic.copy()                                          # v7: the family's own ways (whom a child first admires)
    stress = np.zeros(N); habit = np.zeros((N, C)); B = np.zeros(N)
    y = np.zeros((N, C))                     # aspiration log-ratios (who the person wants to be)
    res = np.tile(np.asarray(P["res0"], float), (N, 1))
    hh_res0 = res[:, RIDX["money"]].copy()                  # F3, world off: the start's means are the household's level
    held = np.zeros((N, NK), bool); I = np.zeros((N, NK)); prof = np.full((N, NK, C), 0.2)
    sat = np.full((N, NK), 0.6); since = np.zeros((N, NK)); pension = np.zeros(N)
    LOAD = np.array([c[1] for c in COMMITMENTS]); KPAY = np.array([parse(c[2], NIDX, NJ) for c in COMMITMENTS])
    FREE_STAGE = np.asarray(P["freedom_stage"], float)
    IMP_FREE = np.minimum(L["IMP"][:, NIDX["autonomy"]], 0)    # impositions on autonomy also take freedom
    BEREAVE = np.array([nm == "bereavement" for nm in L["names"]])
    EXIT = parse("R.5 U.3 B.2"); EXIT /= EXIT.sum()
    EXITW = np.asarray(P["exit_weight"], float)            # leaving children costs far more than leaving a club
    RATE = L["RATE"] * np.where(np.array(L["names"]) == "an ordinary week", P["ordinary_w"], 1.0)
    CP = np.asarray(P["commit_p"], float); retired = np.zeros(N, bool); faith_given = np.zeros(N, bool)   # raised in the faith they hold
    left_given = np.zeros(N, bool); faith_drifted = np.zeros(N, bool)   # left the faith they were raised in; drifted, not decided
    drift_now = np.zeros(N, bool)                         # this week's quiet endings of a faith (read by end)
    sit_n = np.zeros((N, L["S"]), np.int32); lev_log = []
    ev_pm = np.exp(rng.uniform(np.log(P["ev_spread"][0]), np.log(P["ev_spread"][1]), (N, L["S"])))   # personal event rates
    ev_last = np.full((N, L["S"]), -10 ** 6); DRV = L["DRV"]
    PERY = L["PERY"]; EVERYDAY = (PERY.sum(1) == 0) & L["STG"].any(1)     # v6: life events vs everyday situations
    if P["ev_fit"] or P["ill_real"]:   # F9: life events fitted to Release's rows; the body's and mind's at their real rates
        rn_ = np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]
        PERY = PERY.copy()
        for nm_, f_ in (P["ev_fit"] or {}).items():   # a factor, or one per stage
            PERY[rn_ == nm_] *= np.asarray(f_, float)
        if P["ill_real"]:   # Emren's event_scale makes big life events a little more often; illness keeps its real rate
            PERY[np.isin(rn_, list(BODY_MOMENTS) + list(MIND_MOMENTS))] /= P["event_scale"]
    REG_ = (EVERYDAY & (L["RATE"] >= 1) & ~np.asarray(L.get("INNER", np.zeros(L["S"], bool)), bool)
            & ~np.asarray(L.get("ECHO", np.zeros(L["S"], bool)), bool))       # ordinary everyday moments (not title or joining ones)
    CAR, PAR, KID, COM, FAI = KIDX["career"], KIDX["partner"], KIDX["children"], KIDX["community"], KIDX["faith"]
    clash0 = np.full((N, NK), -1); clashI = np.zeros((N, NK)); clash_by = np.full((N, NK), -1); clash_log = []
    MON, TIM, HEA, TIE, FRE = (RIDX[r] for r in ("money", "time", "health", "ties", "freedom"))
    commit_log = []; R_hist = []; K_hist = []
    birth_log = []   # each child a life gains (n, week, moment, option): the first, or one more while there are children
    plast = np.zeros(N); ctrl = np.zeros(N)
    fhz = np.zeros(N); hz_mem = np.zeros(N); hea_last = np.full(N, -1.0)   # v7 felt horizon: limited time felt, reminders
    dsc = np.ones(N)                                     # v7 discipline: self-control learned from plans kept and broken
    CUR_ON = bool(P["cur_on"]); cur_sum = np.zeros(N); cur_m = None   # item 12: the steady current, and how much it moved each life
    SHON = bool(P["shadows"]) and (bool(P["sh_world"]) or not bool(P["world"])); SHG_ = np.asarray(P["sh_gain"], float)
    NM_ON = bool(P["nm_on"])   # P4: each person's own colour-to-need table (needs x colours), from the shared one
    NMP = np.repeat(NMAP[None], N, 0); NM_TOT = NMAP.sum(0); NM_LO = P["nm_band"][0] * NMAP; NM_HI = P["nm_band"][1] * NMAP
    CU_ON = bool(P["curious"]); asked = np.zeros(N)   # item 7: how much others come to them for answers (C4)
    NA_OUT = len(ADJ_ALL) if SHON else ADJ_BASE   # the adjectives the outputs carry
    DOM_ON = bool(P["domains"]); NA_D = len(AREAS)
    Dz = np.zeros((N, NA_D, C)); D_hist = []   # v23 life domains: each area's offset on the colors (log-ratio units)
    # light and shadow: the shadow part s (shS), its force e (shA), the four sources (sh_src: holding on, ruling, no
    # counterweight, strain), whether the person has seen it (a reflection met), the last reflection and breakthrough
    shS = np.zeros((N, C)); shA = np.zeros((N, C)); sh_src = np.zeros((N, C, 4)); sh_seen = np.zeros((N, C), bool)
    sh_rt = np.full((N, C), -10 ** 7); sh_brk = np.full(N, -10 ** 7); sh_n = np.zeros((N, C), int); sh_log = []
    ENEMY_B = ENEMY > 0
    # the colours over the last ten years, each quarter (pair and insight moments: a colour's rise, how long it has held)
    w_q = np.full((40, N, C), 0.2); w_qi = 0
    HZT = HZ_TILT if P["hz_tilt"] is None else (parse(P["hz_tilt"]) if isinstance(P["hz_tilt"], str) else np.asarray(P["hz_tilt"], float))
    HZW = np.maximum(HZT, 0) / max(np.maximum(HZT, 0).sum(), 1e-9)   # where a short horizon pulls the want
    V_hist = {k_: [] for k_ in ("acc", "chan", "core", "wound", "support", "trouble", "fortune", "habit", "role", "SE", "ctrl", "plast", "Q", "doors", "content", "peace", "skill", "fneed", "mood", "stress", "cload", "tension",
                                       "react", "steady", "base_mood", "outlook", "gap",
                                       "n_dream", "n_passion", "n_plan", "harmonious", "regret", "horizon", "discipline", "n_titles", "n_perks", "lvl", "q_rel", "need", "unmet", "hope_w", "adj", "adj_v", "threat", "scar")}   # for the color vectors (Emren, 2026-10-04)
    CTRL = np.asarray(P["ctrl_stage"], float)
    gates = np.zeros((NS, 14))                # per stage: events, wanted-best unavailable, unnoticed, pulled away, tried, tried+succeeded,
                                             # want and pull disagree (both options seen), want won that conflict,
                                             # same two when the person wants to change (gap > 0.1), same two under high stress (> 1),
                                             # wanted-best closed by missing resources, closed by the niche
    stage = np.zeros(N, int); eps_k = np.full(N, P["eps_core"])
    tw_held = tw_has = None                   # what was held last week, for transition windows
    TWo = np.zeros(N)                         # an open window of its own (tw_sep), on the same half-life as openness
    chan = np.zeros((N, len(CHANNELS), C))
    conv_log = []; rite_log = []
    Q = np.zeros(N); brk_log = []; force_re = np.zeros(N, bool)   # pent-up demand and breakthroughs
    tries = np.zeros(N); wins = np.zeros(N); blocked = np.zeros(N)                 # wanted attempts, successes, wanted options closed
    lvl = np.full(N, 0.6); mood = np.zeros(N); content = np.full(N, 0.6); peace = np.full(N, 0.6)   # meta variables
    hold = np.full((N, C), 0.2)
    gap_r = np.zeros(N); q_rel = np.zeros(N); unmet = np.zeros(N); hzf = np.zeros(N)
    NA_ = len(ADJ_ALL); adj = np.zeros((N, NA_), bool); adj_since = np.zeros((N, NA_)); adj_log = []   # v7 adjectives
    adj_v = None
    ADJ_SIDE = np.array([a_[3] for a_ in ADJ_ALL], float); ADJ_ON = np.array([a_[4] for a_ in ADJ_ALL])
    ADJ_OFF = np.array([a_[5] for a_ in ADJ_ALL]); ADJ_AGE = np.array([a_[6] for a_ in ADJ_ALL], float)
    SMID = np.asarray(P["sat_mid_stage"], float) - 0.8 + P["sat_mid"]
    smid = np.full(N, SMID[0]); hope = lvl + P["hope_young"]   # v7: what counts as enough now; what life is hoped to give
    RST = None if P["r_stage"] is None else np.asarray(P["r_stage"], float)
    TST = np.asarray(P["T_stage"], float); RR = np.asarray(P["r_ref"], float); TON = 1.0 if P["temperament"] else 0.0
    react = np.ones(N); steady = np.zeros(N); base_mood = np.full(N, P["base_ref"]); outlook = np.full(N, P["o_ref"])   # temperament
    # the outside world: one shared history of eras, and personal events
    hist = make_history(P, years, seed)
    era_p = np.zeros((T + 1, C)); era_i = np.zeros(T + 1); era_k = np.zeros(T + 1, int); era_at = {}
    for a0, a1, key, inten, kind in hist:
        era_p[a0:a1] = COMBO_MIX[key]; era_i[a0:a1] = inten; era_k[a0:a1] = ERA_KINDS.index(kind); era_at[a0] = (key, inten, kind)
    ev_log = []
    def accept(idx, msg, social):
        """How person idx takes a message (+1 embraces it, -1 pushes back): fit with mindset, discontent,
        openness, group lean (for social sources), and how strongly they hold what it would take."""
        lens = softmax(k[idx]); wi = softmax(z[idx])
        fit = 5 * (lens * msg).sum(1) - 1
        give = np.maximum(0, wi - msg); give /= np.maximum(give.sum(1, keepdims=True), 1e-9)
        holdp = 5 * (give * hold[idx]).sum(1)
        return np.tanh(P["acc0"] + P["acc_fit"] * fit + P["acc_disc"] * (0.55 - content[idx]) + P["acc_open"] * np.minimum(B[idx], 2) / 2
                       + P["acc_conf"] * social * (wi @ GROUP) - P["acc_hold"] * (holdp - 1))
    def take_in(idx, msg, amt, src_i):
        """A taken message moves the want, and a little of the motives (felt experience)."""
        dy = P["ev_eta"] * amt[:, None] * centre(5 * (msg - softmax(y[idx])))
        y[idx] += dy; asrc[idx, src_i] += dy
        dz = P["ev_z"] * (plast[idx] * amt)[:, None] * centre(5 * (msg - softmax(z[idx])))
        pk_ = P["era_push_k"] if src_i == 8 else P["ev_push_k"]   # played lives: the game weighs outside pushes
        if pk_ != 1.0:
            dz = pk_ * dz
        z[idx] += dz; chan[idx, 8] += dz
    def sac_fx(n, ev_):
        """S5 (chroma-ideas/social-mechanics.md): what an offer, tragic trade-off or amends does in the engine. Held: the
        money and ties not had. Crossed: a moral injury (stress), a seed in the line colour's shadow part (with shadows)
        and a turning point's lesson toward the act's ways (the game's item 4 pick at its full "toward" kind: piv x
        plasticity x (1 + piv_far x distance), piv_core of it to the deep core). Healed: stress eased."""
        sp_ = WL.PP.sac_par
        res[n, MON] -= ev_.get("money", 0.0); res[n, TIE] -= ev_.get("ties", 0.0)
        if ev_.get("crossed"):
            stress[n] += ev_["wound"]
            if SHON:
                for c_ in ev_["colours"]:
                    shS[n, c_] = min(1.0, shS[n, c_] + ev_["seed"])
            T_ = np.maximum(ma[n], 0)
            if T_.sum() > 0 and sp_["piv"] and not ev_.get("quiet"):
                T_ = T_ / T_.sum(); w_ = softmax(z[n]); d_ = 0.5 * np.abs(T_ - w_).sum()
                dz_ = sp_["piv"] * plast[n] * (1 + sp_["piv_far"] * d_) * centre(5 * (T_ - w_))
                z[n] += dz_; k[n] += sp_["piv_core"] * dz_; chan[n, 7] += dz_
        if ev_.get("healed") or ev_.get("what") == "healed":
            stress[n] = max(0.0, stress[n] - ev_.get("heal", sp_["heal"]))
    def inst_expo():
        return 0.5 + 0.5 * held[:, CAR] + 0.3 * held[:, COM]
    def era_expo(kind):
        """Who an era reaches: a policy reaches everyone, institutions reach those inside them (work, community),
        a cosmology (a religious or ideological era) reaches the faithful most."""
        return [0.8 + 0.2 * held[:, CAR], inst_expo(), 0.4 + held[:, FAI] * (0.6 + I[:, FAI])][kind]
    f_need = np.full(N, 0.8); cload = np.zeros(N); tension = np.zeros(N)
    asrc = np.zeros((N, len(ASOURCES), C)); A_src = []          # what moved the want, by source (cumulative)
    W_hist = []; M_hist = []; S_hist = []; A_hist = []
    reb = np.zeros((N, 2))                                       # v6: tension rebounds over the life (fit together, split)
    trouble = np.zeros(N); fortune = np.zeros(N)                 # v6: recent big events that went badly / well (decay over years)
    thr = np.full(N, 0.5); mem_s = np.zeros((N, C)); mem_f = np.zeros((N, C)); scar = np.zeros((N, C))   # v10 interpretation
    AXSEC = np.array(AXES["security vs freedom"], float) if P["thr_vec"] is None else \
        (AXSEC_SW if P["thr_vec"] == "schwartz" else np.asarray(P["thr_vec"], float))
    MIS_ON = any(P[k_] for k_ in ("mis_focus", "mis_mem", "mis_scar", "mis_mood", "mis_status"))
    DMS_ = 0.5 ** (1 / (52 * P["mem_pos"])); DMF_ = 0.5 ** (1 / (52 * P["mem_neg"]))
    hub_ = np.zeros(N); xp_ = np.zeros((N, C))                    # status held (hubris) and expertise by color, yearly
    def mem_rel():
        """What memory says of each color's ways, -1 (went badly) to 1 (went well), shrunk while there is little of it."""
        return (mem_s - mem_f) / (mem_s + mem_f + P["mem_eps"])
    wound = np.zeros(N)                                          # v6: a hard event leaves the person open for months
    moved = np.zeros(N)                                          # v6: this week brought new people around the person
    support = np.zeros(N)                                        # v6: being cared for (belonging and ties)
    had_ev = np.zeros(N, bool)
    events = {i: [] for i in log_lives}
    epi = {i: [] for i in log_lives}                             # v10: episodes a logged life may recall (for the game)
    # ---- v7 goals: one row of slots per person; kind -1 = empty, 0 dream, 1 passion, 2 plan
    GON = bool(P["goals"])
    NGS = P["max_dreams"] + P["max_passions"] + P["max_plans"]; GMAX = (P["max_dreams"], P["max_passions"], P["max_plans"])
    gk = np.full((N, NGS), -1); gm = np.full((N, NGS, C), 0.2); gd = np.full((N, NGS), -1)   # kind, the ways it calls for, domain
    gs = np.zeros((N, NGS)); gp = np.zeros((N, NGS)); gv = np.zeros((N, NGS)); ga = np.full((N, NGS), 0.5)   # strength, progress,
    # meaningful success gathered (valuation), and how freely it was taken in (1 harmonious, 0 obsessive; Vallerand 2003)
    gi = np.zeros((N, NGS)); gpk = np.zeros((N, NGS))                          # investment (sunk), peak strength
    gb = np.zeros((N, NGS), int); gh = np.zeros((N, NGS), int); ghz = np.zeros((N, NGS), int); gx = np.zeros((N, NGS), int)  # born, due, horizon, extensions
    gsrc = np.zeros((N, NGS), int); gtrig = np.full((N, NGS), -1); gpar = np.full((N, NGS), -1); gby = np.zeros((N, NGS), int)
    # the Library's dreams (chroma-library/dreams.py, Emren 10-06 22:19, via batch): the setting's sparks, and the concrete
    # dreams a new one is named by (gname: its index in DRM_, carried into its passion and plans; -1 = plain naming)
    DTR_ = L.get("DREAM_TRIGGERS") or DREAM_TRIGGERS
    TRIG_SRC = np.array([GSRC[tr[1]] for tr in DTR_])
    TRIG_W = np.array([tr[2] for tr in DTR_], float)                   # triggers x stages
    TRIG_TILT = np.array([parse(tr[3]) if tr[3] else np.zeros(C) for tr in DTR_])
    DRM_ = L.get("DREAMS") or []
    DG_ON = bool(P.get("dream_grow")) and bool(DRM_)   # v22.5, F6: dreams that grow up
    if DG_ON:   # the Library's added dreams join, so every age has dreams of every colour (dreams.py DREAMS_MORE)
        DRM_ = list(DRM_) + list(L.get("DREAMS_MORE") or [])
    if DRM_:
        DRM_X = np.array([parse(d_["means"]) for d_ in DRM_]); DRM_X = DRM_X / DRM_X.sum(1, keepdims=True)   # its ways, as shares
        DRM_M = DRM_X - 1 / C
        DRM_M = DRM_M / np.linalg.norm(DRM_M, axis=1, keepdims=True)    # each dream's lean among the colors
        DRM_D = np.array([KIDX.get(d_["domain"], -1) for d_ in DRM_])
        DRM_S = np.array([[nm_ in d_["stages"].split() for nm_ in STAGE_NAMES] for d_ in DRM_])
    if DG_ON:   # F6: the youngest age each dream can start at (by its kind), the play dreams, each spark's subjects and ages
        DK_ = L.get("DREAM_KIND") or {}; KF_ = L.get("KIND_FROM") or {}
        DRM_FROM = np.array([float(KF_.get(DK_.get(d_["name"], ""), 0.0)) for d_ in DRM_])
        DRM_PLAY = np.array([DK_.get(d_["name"]) == "play" for d_ in DRM_])
        PLAY_UNTIL_ = float(L.get("PLAY_UNTIL") or 0.0)
        ix_ = {d_["name"]: i_ for i_, d_ in enumerate(DRM_)}; TD_ = L.get("TRIGGER_DREAMS") or {}
        TRIG_SUBJ = [[ix_[x_] for x_ in TD_.get(tr_[0], ()) if x_ in ix_] for tr_ in DTR_]
        TRIG_AGE = np.array([(L.get("TRIGGER_AGES") or {}).get(tr_[0], (0.0, 1e9)) for tr_ in DTR_], float)
    gname = np.full((N, NGS), -1)
    gplay = np.zeros((N, NGS), bool)   # F6: a play dream started before PLAY_UNTIL (short-lived)
    def dream_name(mix, dom, st):
        """The nearest concrete dream: of this setting, able to start at this stage, of this domain; nearest in colors, by
        the way it leans (a dream's mix is broad, so plain distance would favour the broadest dreams). F6 (dream_grow):
        and of a kind they are old enough for."""
        if not DRM_:
            return -1
        ok_ = (DRM_D == dom) & DRM_S[:, st]
        if DG_ON:
            ok_ = ok_ & (DRM_FROM <= age)
        if not ok_.any():
            return -1
        return int(np.argmax(np.where(ok_, DRM_M @ (mix / mix.sum() - 1 / C), -np.inf)))
    def dream_phrase(n, j):
        """What the goal in slot j is called: the dream's name, its passion phrase once sealed, its plan phrase as a
        five-year plan, its life phrase as a life goal."""
        d_ = DRM_[gname[n, j]]
        return d_["name"] if gk[n, j] == 0 else d_["passion"] if gk[n, j] == 1 else d_["life"] if ghz[n, j] == 3 else d_["plan"]
    gid = np.zeros((N, NGS), int); glast = np.zeros((N, NGS), int)
    gtt = np.full((N, NGS), -1)                                              # a plan aimed at a title (pathways): its id
    gch = np.zeros((N, NGS)); gph = np.zeros((N, NGS)); gfelt = np.zeros((N, NGS)); gfelt0 = np.zeros((N, NGS))   # felt chances, step odds, odds
    gsr = np.zeros((N, NGS, L["S"]))                                         # how much each situation offers a step toward it
    lost_m = np.full((N, 3, C), 0.2); lost_d = np.full((N, 3), -1); lost_s = np.zeros((N, 3)); lost_t = np.zeros((N, 3))
    lost_on = np.zeros((N, 3), bool); lost_id = np.zeros((N, 3), int)    # dreams, passions and plans let go of (regret, revival)
    lost_nm = np.full((N, 3), -1)                                         # and the concrete dream each was (gname)
    pres_c = np.zeros((N, C)); pres_d = np.zeros((N, NK)); pres_n = np.zeros(N)   # how often chances in each color and domain come
    regret = np.zeros(N); goal_log = []; gid_next = [1]
    HAS_STEP = np.stack([(L["COMMIT"] == d_).any(1) for d_ in range(NK)], 1).astype(float)   # S x NK: a situation can start it
    SH_REFL = np.array([SH_STATES.index(str((L["src"][i_] if i_ < len(L["src"]) else {}).get("holds") or "").strip())
                        if L["TIER"][i_] == TIERS.index("inner") and str((L["src"][i_] if i_ < len(L["src"]) else {}).get("holds") or "").strip()
                        in SH_STATES else -1 for i_ in range(L["S"])], int)   # the shadow a reflection moment sees, else -1
    SH_NEW = HAS_STEP.max(1)                                                                  # shadows: a moment that opens something new
    SPRIOR = step_prior(L, P)
    MS_ = L["M"] * L["MASK"][..., None]
    def goal_rel_S(mix, dom):
        """For seeking: how much each situation offers a step toward a goal."""
        if dom >= 0:
            return HAS_STEP[:, dom].copy()
        return _uclip((5 * np.einsum("skc,c->sk", MS_, mix) - 1) / 2, 0, 1).max(1)
    def glog(n, j, what, **extra):
        rec = dict(life=int(n), id=int(gid[n, j]), age=round(t / 52, 2), what=what, kind=G_KINDS[gk[n, j]],
                   domain=KNAMES[gd[n, j]] if gd[n, j] >= 0 else "a pursuit", mix=gm[n, j].round(2).tolist(),
                   source=G_SOURCES[gsrc[n, j]], strength=round(float(gs[n, j]), 2), **extra)
        if gtrig[n, j] >= 0:
            rec["trigger"] = DTR_[gtrig[n, j]][0]
            if what == "begins" and gk[n, j] == 0 and len(DTR_[gtrig[n, j]]) > 4:
                rec["say"] = DTR_[gtrig[n, j]][4]                 # the spark, told: one line with {N} for the character
        if gname[n, j] >= 0:
            d_ = DRM_[gname[n, j]]
            rec.update(name=dream_phrase(n, j), dream=d_["name"], passion=d_["passion"], plan=d_["plan"], life_goal=d_["life"])   # (life = the person)
        if gk[n, j] == 2:
            rec.update(horizon=HORIZONS[ghz[n, j]], progress=round(float(gp[n, j]), 2), felt=round(float(gfelt[n, j]), 2))
            if what == "begins":   # what the felt odds leave out (for the foreseen outcome's hint of reality: foresee.py)
                og_ = 0.5 * (w[n] + softmax(y[n]))
                rec.update(by_player=bool(gby[n, j]), self_control=round(float(ctrl[n]), 3), free_time=round(float(res[n, TIM]), 3),
                           stress=round(float(stress[n]), 3), fit=round(float(_uclip(2 * (gm[n, j] * og_).sum() / og_.max() - 1, -0.5, 1)), 3))
        if gk[n, j] == 1:
            rec["harmonious"] = round(float(ga[n, j]), 2)
        goal_log.append(rec)
        if n in events:
            events[n].append(dict(goal=rec))
    def new_goal(n, kind, mix, dom, src, hz=1, trig=-1, par=-1, by=0, s0=0.4, inherit=-1, target=-1, name=-1):
        """Open a slot for a new goal; when the kind is full, the new one replaces the weakest if it is stronger."""
        mine = np.nonzero(gk[n] == kind)[0]
        if len(mine) >= GMAX[kind]:
            j = mine[np.argmin(gs[n, mine])]
            if gs[n, j] >= s0 or gby[n, j]:
                return -1
            end_goal(n, j, "pushed aside")
        free = np.nonzero(gk[n] < 0)[0]
        if not len(free):
            return -1
        j = free[0]
        gk[n, j] = kind; gm[n, j] = mix / mix.sum(); gd[n, j] = dom; gs[n, j] = s0; gpk[n, j] = s0
        gsrc[n, j] = src; gtrig[n, j] = trig; gpar[n, j] = par; gby[n, j] = by; gb[n, j] = t; glast[n, j] = t
        gname[n, j] = name if name >= 0 else gname[n, par] if par >= 0 else dream_name(mix, dom, stage[n]) if kind == 0 else -1
        gplay[n, j] = DG_ON and kind == 0 and gname[n, j] >= 0 and DRM_PLAY[gname[n, j]] and age < PLAY_UNTIL_
        gp[n, j] = 0.0; gi[n, j] = 0.0; gx[n, j] = 0
        gv[n, j] = gv[n, inherit] if inherit >= 0 else 0.0; ga[n, j] = ga[n, inherit] if inherit >= 0 else 0.5
        gid[n, j] = gid_next[0]; gid_next[0] += 1
        gsr[n, j] = goal_rel_S(gm[n, j], dom); gtt[n, j] = target
        if target >= 0:   # a plan aimed at a title seeks the moments that open a way into it, and its kind's beginnings
            gsr[n, j] = np.maximum(GR["DOORS"][target].astype(float), 0.3 * (HAS_STEP[:, TK_[target]] if TK_[target] < NK else 0.0))
        if kind == 2:
            init_plan(n, j, hz)
        glog(n, j, "begins", **({"aims": GR["names"][target]} if target >= 0 else {}))
        return j
    def plan_odds(n, mix, dom, hz, s):
        """A person's first sense of a plan's chances (changes nothing; the game previews a plan with it): how often their
        weeks have offered such steps, how a step in its ways looks to them (skill, past feedback, outlook), the weeks to
        the deadline and the felt odds of reaching it in time. mix sums to 1."""
        hw = HORIZON_W[hz]
        weeks = hw if hw is not None else max(52, int((P["life_end"] - t / 52) * 52))
        pn = max(pres_n[n], 1e-9)
        ch = (pres_d[n, dom] if dom >= 0 else (mix * pres_c[n]).sum()) / pn
        mis1 = (P["mis_focus"] * (0.5 - thr[n]) + mix @ (P["mis_mem"] * mem_rel()[n] - P["mis_scar"] * scar[n])) if MIS_ON else 0.0
        ph = 1 / (1 + np.exp(-P["gain"] * ((mix * (sig[n] + fb[n])).sum() - 0.5) - TON * P["o_bias"] * (outlook[n] - P["o_ref"]) - mis1))
        if dom >= 0:   # what they know of such chances, from their own weeks or from people around them; and they imagine
            ch = max(ch, SPRIOR[min(stage[n] + 1, NS - 1), dom], SPRIOR[stage[n], dom])   # looking harder than before
            ch *= 1 + P["g_seek_ev"] * s
        felt = float(felt_odds(ch, ph, weeks, int(np.ceil(P["g_size"][hz] / STEP_INC)), dom, outlook[n], P))
        return ch, ph, weeks, felt
    def init_plan(n, j, hz):
        """A plan's deadline, and the person's first sense of their chances (plan_odds)."""
        ghz[n, j] = hz
        gch[n, j], gph[n, j], wk_, gfelt[n, j] = plan_odds(n, gm[n, j], gd[n, j], hz, gs[n, j])
        gfelt0[n, j] = gfelt[n, j]; gh[n, j] = t + wk_
        gp[n, j] = 0.0; gi[n, j] = 0.0; gx[n, j] = 0
    def seal(n, how, only=None):
        """2A: tries that worked and felt like one's own, sealed by a rite (or a turning point), make a dream a passion."""
        # a second passion takes far more than the first (most people have one, few have two or more; Vallerand 2003)
        cand = [j for j in np.nonzero(gk[n] == 0)[0] if gv[n, j] >= P["seal_v"] and gs[n, j] >= P["seal_s"] and (only is None or j in only)]
        for j in sorted(cand, key=lambda j_: -gv[n, j_]):
            held_p = gk[n] == 1   # one at a time: each passion held raises the bar, and a new love must rival the old
            if gv[n, j] < max(P["seal_v"] * (1 + P["seal_more"] * held_p.sum()), P["seal_rival"] * gv[n, held_p].max(initial=0.0)):
                continue
            mine = np.nonzero(gk[n] == 1)[0]
            if len(mine) >= GMAX[1]:
                jw = mine[np.argmin(gs[n, mine])]
                if gs[n, jw] >= gs[n, j]:
                    continue
                end_goal(n, jw, "pushed aside")
            gk[n, j] = 1; gs[n, j] = max(gs[n, j], 0.6); gpk[n, j] = max(gpk[n, j], gs[n, j]); glast[n, j] = t
            glog(n, j, "became a passion", sealed_by=how)
    def to_plan(n, j):
        """Coming of age: a dream still strong becomes a five-year plan (a plan is not yet a commitment)."""
        glog(n, j, "became a plan")
        if gd[n, j] >= 0 and held[n, gd[n, j]]:
            gd[n, j] = -1
        gk[n, j] = 2; gsrc[n, j] = GSRC["dream"]; gpar[n, j] = -1
        gsr[n, j] = goal_rel_S(gm[n, j], gd[n, j]); init_plan(n, j, 2)
        glog(n, j, "begins")
    def quit_(n, j, what, letgo):
        """Giving up costs what was put in, less for those who have learned to let go (Wrosch et al. 2003)."""
        stress[n] += P["g_quit"] * gi[n, j] * (1 - letgo)
        need[n, NIDX["meaning"]] -= 0.05 * min(gi[n, j], 1.0)
        outlook[n] += 0.05 * gs[n, j] * (0 - outlook[n]) * TON
        end_goal(n, j, what)
    def end_goal(n, j, what, keep=None):
        """Close a goal. A dream, passion or plan that mattered is kept among the things let go of (regret, revival)."""
        glog(n, j, what)
        if gk[n, j] == 2 and P["disc_rate"]:   # discipline is learned: a plan kept strengthens it, one given up weakens it
            if what == "achieved":
                dsc[n] += P["disc_rate"] * (P["disc_range"][1] - dsc[n])
            elif what in ("let go", "not reached in time"):
                dsc[n] -= P["disc_rate"] * (dsc[n] - P["disc_range"][0])
        if keep is None:
            keep = (gk[n, j] == 1) or (gk[n, j] == 0 and gpk[n, j] >= 0.45) or (gk[n, j] == 2 and (gi[n, j] > 0.5 or gsrc[n, j] in (GSRC["dream"], GSRC["passion"], GSRC["old dream"])))
        if keep and what not in ("achieved", "became a passion", "became a plan"):
            q_ = np.argmin(np.where(lost_on[n], lost_s[n], -1.0))
            lost_m[n, q_] = gm[n, j]; lost_d[n, q_] = gd[n, j]; lost_s[n, q_] = gpk[n, j]; lost_t[n, q_] = t / 52
            lost_on[n, q_] = True; lost_id[n, q_] = gid[n, j]; lost_nm[n, q_] = gname[n, j]
        for j2 in np.nonzero(gpar[n] == j)[0]:
            gpar[n, j2] = -1
        gk[n, j] = -1; gs[n, j] = 0.0; gpar[n, j] = -1; gby[n, j] = 0; gtt[n, j] = -1; gname[n, j] = -1
        ago["goal_end"][n] = t
    ar = np.arange(N)
    decay_B = 0.5 ** (1 / P["crisis_half"])
    nI = len(L["IMP"])
    pb = np.ones(nI) / nI if P["impose_bias"] is None else softmax(np.asarray(P["impose_bias"], float))
    real = (L["MASK"] & (L["M"].std(-1) > 1e-9)).reshape(-1)          # real options (not padding, not "do nothing")
    REQ_ALL = L["REQ"].reshape(-1, NR)[real]; M_ALL = L["M"].reshape(-1, C)[real]
    REQ_ROWS = np.nonzero((REQ_ALL > 0).any(1))[0]; REQ_SUB = REQ_ALL[REQ_ROWS]   # speed pass: options that need means
    def doors(nic, res):
        """For each color: chance that an option acted in that color's way is open to this person
        (the niche lets it happen, and the person has the means it needs)."""
        accn = _uclip(P["access_base"] + P["access_k"] * (nic - 0.2), 0.05, 1.0)
        rg = np.ones((len(res), len(REQ_ALL)))    # speed pass: an option that needs nothing is open to all (1.0 exactly)
        rg[:, REQ_ROWS] = np.where(REQ_SUB[None] > 0, 1 / (1 + np.exp(-P["req_g"] * (res[:, None, :] - REQ_SUB[None]))), 1.0).prod(-1)
        return accn * (rg @ M_ALL) / M_ALL.sum(0)[None]
    def end(ns, ks, why, t):
        for n, kk in zip(ns, ks):
            end_t[n, kk] = t; end_why[n, kk] = WHY.index(why) if why in WHY else -1
            if why == "retired": ago["retire"][n] = t
            if why in ("lost job", "broke up", "widowed"): ago["loss"][n] = t
            if kk == PAR and why in ("left", "broke up"): ago["breakup"][n] = t
            if why in ("left", "lost job", "broke up"):
                stress[n] += 0.5 * I[n, kk] * (0.5 + 2.5 * (prof[n, kk] * softmax(k[n])).sum())
                if why == "left":
                    B[n] += 0.5 * I[n, kk]                      # leaving opens the person up for a while
                    steady[n] *= 1 - 0.3 * I[n, kk] * TON       # and shakes how firmly they hold who they are
                    if kk in (COM, FAI): need[n, NIDX["meaning"]] -= 0.3 * I[n, kk]
                if kk in (PAR, COM): res[n, TIE] -= 0.15
                if kk == CAR: res[n, MON] -= 0.15
            if why == "retired":
                pension[n] = I[n, kk] * max(0.5, 1 - P["pension_cut"] * max(0.0, P["retire_age"] - t / 52)); retired[n] = True
            if kk == FAI:
                left_given[n] = why == "left" and faith_given[n]; faith_drifted[n] = bool(drift_now[n])   # how the last one ended
                faith_given[n] = False                          # a faith taken up again is one's own
            commit_log.append((int(n), t, int(kk), why, prof[n, kk].round(2).tolist(), round(float(I[n, kk]), 2)))
            if EYES_ON_ and WL is not None and kk in (CAR, PAR, FAI) and why in ("left", "broke up"):   # S3: their places
                WL.PP.eyes_see([n], prof[n, kk][None], [0.5], {CAR: "left job", PAR: "left partner", FAI: "left faith"}[kk])   # read
            if n in events:                                                  # the leaving by what was walked away from
                events[n].append(dict(commitment=dict(age=round(t / 52, 2), kind=KNAMES[kk], what=why,
                                                      profile=prof[n, kk].round(2).tolist(), strength=round(float(I[n, kk]), 2))))
                if kk == FAI and why == "left" and drift_now[n]:
                    events[n][-1]["commitment"]["drifted"] = True   # it stopped mattering; no decision was made
            held[n, kk] = False; I[n, kk] = 0.0

    # ---- the Library's batch format: marks (what an act leaves in a history), echoes, inner moments, who is alive,
    # what ends, tags, closed options, outside events read through the colors. All conditions are the engine's reading
    # (<world>_rules.py) of the Library's plain words
    BAT = "COND" in L
    NEVER = -10 ** 7
    MIDX = {m_: i_ for i_, m_ in enumerate(L["MARKS"])}; NM = len(L["MARKS"]); SIDX = {n_: i_ for i_, n_ in enumerate(L["names"])}
    mark_last = np.full((N, NM), NEVER); mark_first = np.full((N, NM), NEVER); mark_ok = np.zeros((N, NM), bool)
    mark_n = np.zeros((N, NM), np.int32)
    sit_last = np.full((N, L["S"]), NEVER); sit_first = np.full((N, L["S"]), NEVER); once_done = np.zeros((N, L["S"]), bool)
    ROOT = np.asarray(L.get("ROOT", np.arange(L["S"])))                  # each situation's original (itself, or variant_of)
    HASFAM_ = np.bincount(ROOT, minlength=L["S"])[ROOT] > 1               # situations that share their original with another
    def _gap(g_):   # the Library's gap: "2-5", (2, 5) or 3 (years)
        if g_ is None or g_ == "": return (np.nan, np.nan)
        if isinstance(g_, str):
            p_ = [float(x) for x in g_.replace(" ", "").split("-") if x]
            return (p_[0], p_[-1])
        if isinstance(g_, (int, float)): return (float(g_), float(g_))
        return (float(g_[0]), float(g_[-1]))
    GAP_ = np.array([_gap((s_.get("gap") or (s_.get("timing") or {}).get("gap_years")) if s_.get("tier") == "life event" or s_.get("per_year") else None)
                     for s_ in L.get("src", [{}] * L["S"])], float).reshape(-1, 2)   # build.py keeps it as timing gap_years
    GAPM_ = ~np.isnan(GAP_[:, 0]); GAPON_ = bool(P["ev_gap"] and GAPM_.any())
    # far_ties (item 18): a far moment (cast_want: far_*) comes only with a tie's call, never by the everyday draw
    FARS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        import world_keys as WK_
        FARS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_.startswith("far_")])
    FARS_ON_ = bool(FARS_.any())
    # lead_ways (S7): a post's moment (cast_want: lead_*) comes only with the post (taking it, a crisis, its fall, the
    # turn to routine, handing it on), never by the everyday draw of life events
    LEADS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        LEADS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_.startswith("lead_")])
    LEADS_ON_ = bool(LEADS_.any())
    # S5, sacred lines: an offer, tragic trade-off or amends moment (cast_want: sacred, tragic, amends) comes only when the
    # life's own line brings it (WorldLink), never by the everyday draw or a yearly rate; the switch turns the lines on
    SACS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        SACS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_ in WK_.OWN_WANTS])
    SACS_ON_ = bool(SACS_.any())
    SAC_ON_ = False                                       # (set with the world: its People has the lines)
    REG_ = REG_ & ~FARS_ & ~LEADS_ & ~SACS_   # (nor by the neighbouring stages' fill or the routine's; the Library's find, 10-10)
    # S3, S4 (sph_eyes, sph_odd): a caught-between or odd-one-out moment (cast_want: caught, odd) comes only when the place
    # reading brings it, never by the everyday draw
    EYEW_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        EYEW_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_ in ("caught", "odd")])
    EYEW_ON_ = bool(EYEW_.any())
    if EYEW_ON_:
        REG_ = REG_ & ~EYEW_   # (nor by the stages' fill or the routine's, as far moments)
    GAPLO_ = np.nan_to_num(GAP_[:, 0])[None]; GAPW_ = np.maximum(np.nan_to_num(GAP_[:, 1] - GAP_[:, 0]), 1 / 52)[None]
    # the same gap on an everyday or inner moment (a stray dog that follows you home is not a weekly thing): its weight ramps
    # from 0 at lo years after it last came to full at hi (the game thread's finding, 2026-10-05 22:00)
    GAPX_ = np.array([_gap((s_.get("gap") or (s_.get("timing") or {}).get("gap_years")) if s_.get("tier") in ("everyday", "inner") else None)
                      for s_ in L.get("src", [{}] * L["S"])], float).reshape(-1, 2)
    GAPXM_ = ~np.isnan(GAPX_[:, 0]); GAPXON_ = bool(P["ev_gap"] and GAPXM_.any())
    GAPXLO_ = np.nan_to_num(GAPX_[:, 0])[None]; GAPXW_ = np.maximum(np.nan_to_num(GAPX_[:, 1] - GAPX_[:, 0]), 1 / 52)[None]
    GAPM_I, GAPN_I, GAPX_I = np.nonzero(GAPM_)[0], np.nonzero(~GAPM_)[0], np.nonzero(GAPXM_)[0]   # speed pass: their columns
    ROUT_ = REG_ & ~(GAPXM_ & (GAPXLO_[0] > 0))   # gap_keep's routine: ordinary everyday moments whose gap starts at 0 (or none);
    # a moment whose gap starts later is an event in someone's life, and keeps its own rate and spacing (Library 07:27)
    FAMILY = L.get("FAMILY", {})                                           # an original's name -> it and its child versions
    alive = np.zeros((N, len(ROLES)))                     # parents, siblings, a closest friend, grandparents, partner, children
    kid_last = np.full(N, -10 ** 7)                        # the week the last child was born (R15: a baby's first year)
    kid_on = np.zeros(N, bool)                             # children held at the start of this week (counted already)
    # identity (point 11): sex from setup, attraction and unease drawn at birth and hidden
    sx_ = P["sex"]; rid = np.random.default_rng([int(seed), 11])   # its own random stream: the rest of the run is unchanged
    ID2 = bool(P["id_v2"])
    sxl_ = None if sx_ is None else [str(x).lower() for x in (sx_ if isinstance(sx_, (list, tuple, np.ndarray)) else [sx_] * N)]
    female = (rid.random(N) < (P["female_p"] if ID2 else 0.5)) if sx_ is None else np.array([x.startswith("f") for x in sxl_])
    attr = np.where(female, rid.choice(5, N, p=P["attr_p"][0]), rid.choice(5, N, p=P["attr_p"][1]))
    if ID2:   # N1b: own gender from the uniform that drew unease, so everyone who had unease keeps it; new draws go last
        ug_ = rid.random(N)
        gender_self = np.where(ug_ < P["trans_p"], 1, np.where(ug_ < P["trans_p"] + P["nb_p"], 2, 0))
        unease = gender_self > 0
        intersex = (rid.random(N) < P["intersex_p"]) if sx_ is None else np.array([x.startswith("i") for x in sxl_])
        raised_ = rid.random(N) < 0.5; attr_ix_ = np.where(raised_, rid.choice(5, N, p=P["attr_p"][0]), rid.choice(5, N, p=P["attr_p"][1]))
        female = np.where(intersex, raised_, female); attr = np.where(intersex, attr_ix_, attr)   # female: raised as
        ace = rid.random(N) < P["ace_p"]
        idr_ = np.random.default_rng([int(seed), 78])   # later identity draws (attraction drift, a partner's sex): own stream
        ps_u = idr_.random((N, 12))                     # one draw per partner, in order, whatever else the life does
        ps_n = np.zeros(N, int); partner_same = np.zeros(N, bool); par_prev = np.zeros(N, bool)
        named_g = np.zeros(N, bool); came_o = np.zeros(N, bool)      # own gender named; attraction told
        found_id = np.full((N, 4), NEVER)               # the week a moment gated on gender, attraction, ace, intersex first came
        rfit_avg = np.zeros(N); cross_title = np.zeros(N, bool); act_cw = np.zeros(N)
        setting_ = L.get("SETTING", "earth") if BAT else "earth"
        RS0 = P["role_strict"] if P["role_strict"] is not None else ROLE_BY_SETTING.get(setting_, 0.3)
        AT0 = P["accept_trans"] if P["accept_trans"] is not None else ACCEPT_BY_SETTING.get(setting_, 0.5)
    else:
        unease = rid.random(N) < P["unease_p"]
        gender_self = unease.astype(int); intersex = np.zeros(N, bool); ace = np.zeros(N, bool)
    dead = np.zeros(N, bool); died = []                   # the character's own death (self_death)
    pris_out = np.full(N, NEVER)                           # when a prison term ends ([ex-prisoner])
    if BAT:
        alive[:, 0] = 2; alive[:, 1] = rng.choice(4, N, p=[0.2, 0.4, 0.25, 0.15]); alive[:, 2] = 1; alive[:, 3] = rng.integers(2, 5, N)
    # birth order (checklist N4): which of the siblings are older; drawn from its own stream so no other draw moves
    older_sib = np.floor(np.random.default_rng([seed, 77]).random(N) * (alive[:, 1] + 1)).astype(int)
    younger_sib = alive[:, 1].astype(int) - older_sib
    friend_back = np.full(N, NEVER)
    AGO = ("le", "commit", "move", "death", "loss", "win", "hard_win", "fail_big", "breakup", "retire", "child", "job", "goal_end", "hard",
           "near_death", "fail_body", "fail_long")   # fail_body: a failed act that risked the body (body:, or death_if_fails)
    # (packs 07:52); fail_long: a failed long shot, an act for a title (or granting the long-shot perk) at true odds under
    # long_shot (packs 08:02)
    ago = {k_: np.full(N, NEVER) for k_ in AGO}           # the week each of these last happened
    STREAKS = ("quiet", "lo_meaning", "vlo_meaning", "lo_belong", "lo_peace", "hi_stress", "lo_time", "lo_auto", "ok_needs",
               "ok_body", "easing", "flat_comp")
    streak = {k_: np.zeros(N) for k_ in STREAKS}           # weeks in a row
    hist_m = np.full((N, C), 0.2); hist_e = np.full((N, C), 0.2)   # ten-year shares of the ways acted and the ends served
    hedon_n = np.zeros(N); bodyhab_n = np.zeros(N); fails13 = np.zeros(N); n_moves = np.zeros(N); heavy_risk = np.zeros(N)
    bind_m = np.zeros(N); bind_c = np.full((N, C), 0.2); end_t = np.full((N, NK), NEVER); widowed = np.zeros(N, bool)
    WHY = ["left", "lost job", "broke up", "widowed", "retired"]; end_why = np.full((N, NK), -1)
    comp_ref = np.full(N, 0.6); stress_slow = np.zeros(N); read_log = []; mark_log = []
    cond_ok = np.ones((N, L["S"]), bool); cond_fac = np.ones((N, L["S"])); cond_hold = np.zeros((N, L["S"])); cond_n = np.zeros(N)
    drv_sum = np.zeros(L["S"]); drv_cnt = np.zeros(L["S"])
    earn_sum = np.zeros(L["S"]); earn_cnt = np.zeros(L["S"])   # the earned lift of those who meet a title-giving moment
    ref_sum = np.zeros((L["S"], C)); ref_cnt = np.zeros(L["S"]); pk_sum = np.zeros((L["S"], L["K"])); pk_cnt = np.zeros((L["S"], L["K"]))   # chance
    WID_ON = JOBLOSS_ON = REJOB_ON = True; EV_KEEP = np.ones(len(EV["names"])); ECH = []; EVR = []
    if BAT:
        GATED = np.zeros(L["S"], bool); GATED[[c_["s"] for c_ in L["COND"]]] = True
        cond_ok[:, GATED] = False
        ECH = [c_ for c_ in L["COND"] if c_["kind"] == 2]; ECH_S = np.array([c_["s"] for c_ in ECH], int)
        ECH_R = RATE[ECH_S] / 0.3          # an echo's rate: (default .3) scales the share of its anchors that come back
        echo_anchor = np.full((N, len(ECH)), NEVER); echo_due = np.full((N, len(ECH)), NEVER); echo_end = np.full((N, len(ECH)), NEVER)
        echo_ready = np.zeros((N, len(ECH)), bool); echo_fac = np.ones((N, len(ECH)))
        EVR = L["EVR"]
        evr_next = np.stack([(max(e_["window"][0], 3) + rng.uniform(0, e_["gap"][1], N)) * 52 for e_ in EVR], 1) if EVR else np.zeros((N, 0))
        KILLS, ENDS, ONCE, ONCE_K = L["KILLS"], L["ENDS"], L["ONCE"], L["ONCE_K"]
        WID_ON = not (KILLS == ROLES.index("partner")).any()      # the batch's own "your partner dies" replaces built-in widowhood
        JOBLOSS_ON = not (ENDS == CAR).any()                      # and its "losing your job" the built-in job loss
        REJOB_ON = L.get("REJOB", -1) < 0                         # and its "a new job at last" the quiet return to work
        EV_KEEP = np.array([nm_ not in EV_DROP for nm_ in EV["names"]], float)
        KL_ = KILLS >= 0; INNER_ = L["INNER"]; KCH_ = KILLS[KL_] == ROLES.index("child")

    # ---- titles and perks (after v7): roles others recognise, and what a person can do or has access to
    RON = BAT and bool(P["roles"]) and "ROLES" in L
    EARN_ON = False; LOG_CAP = np.log(P["earned_cap"] / (1 - P["earned_cap"]))
    def earned(z, er):
        """An act's odds (logit z) with the earned lift er: a lift never carries the odds past earned_cap."""
        if not np.ndim(er) and er == 0.0:
            return z
        return z + np.where(er > 0, np.minimum(er, np.maximum(LOG_CAP - z, 0.0)), er)
    AQ_ON = BAT and bool(P["adjectives"]) and bool(L.get("ADJ_ANY"))   # v7: acts or situations require an adjective
    role_log = []
    LONG_ = -1; missed_t = np.full(N, -1)                    # the long-shot perk; the last title each life missed on a long shot
    C5F_ = -1                                                # C5: the title that founds a movement ("founder of a movement")
    tries_ct = None                                          # failed tries per life and title or perk (try_lift)
    if RON:
        GR = L["ROLES"]; NT_, NP_, NI_ = GR["NT"], GR["NP"], GR["NI"]
        if P.get("green_jobs") and GR.get("rule_when"):   # v22.4: the green entry jobs' rules and roads (ROLES_WHEN)
            GR = dict(GR, rule=[GR["rule_when"].get(i_, r_) for i_, r_ in enumerate(GR["rule"])])
        if P.get("sph_titles") and GR.get("rule_sph"):   # item 15: the sphere titles follow their own rules
            sr_ = {**GR["rule_sph"], **(GR.get("rule_sph_when") or {})} if P.get("green_jobs") else GR["rule_sph"]
            GR = dict(GR, rule=[sr_.get(i_, r_) for i_, r_ in enumerate(GR["rule"])])   # (earth_rules.SPH_TITLE_ROLES)
        r_has = np.zeros((N, NI_), bool); r_ever = np.zeros((N, NI_), bool)
        r_since = np.full((N, NI_), NEVER); r_end = np.full((N, NI_), NEVER)
        p_acc = np.zeros((N, NP_), bool); p_lev = np.zeros((N, NP_)); p_sus = np.full((N, NP_), NEVER)   # access, skill, suspended until
        tries_ct = np.zeros((N, NI_), np.int8)
        TK_ = GR["tkind"]; KT_ = np.zeros((NT_, NK)); ck_ = TK_ < NK; KT_[np.nonzero(ck_)[0], TK_[ck_]] = 1.0
        ODD4 = 4.0 * GR["odds"]; INDP = GR["ind"][NT_:]; WAYS_ = GR["ways"]
        PKIND_ = np.asarray(GR["pkind"]); CAREER_ = (np.asarray(GR["tkind"]) == 0).astype(float)   # v10: skills (0), standings (2); careers
        PW_, PN_, REF_ = GR["PW"], GR["PN"], GR["refines"]          # title profiles (colors) and facets (refines another title)
        REFM_ = GR["REFM"]                                          # items x titles: the titles a facet can sit on (any of them)
        _hm = GR.get("S_HOLDM"); _ht = GR.get("S_TEN")               # holds: (any of) and tenure: (point 6)
        if _hm is None:   # an older batch.py: the first name of holds: or requires: only
            _hm = np.zeros((L["S"], NI_), bool); _rq = GR["S_REQ"]; _hm[np.nonzero(_rq >= 0)[0], _rq[_rq >= 0]] = True
            _ht = np.full((L["S"], 2), np.nan)
        _tn = ~np.isnan(_ht[:, 0]); _hh = _hm.any(1)
        HOLDS_ = np.nonzero(_hh & ~_tn)[0]; HOLDM_ = _hm[HOLDS_].T.astype(np.float32)
        HOLD_C = np.nonzero(HOLDM_.any(1))[0]; HOLDM_C = HOLDM_[HOLD_C]   # speed pass: the rows that can count (0/1 sums, exact)
        TENS_ = [(int(s_), np.nonzero(_hm[s_])[0], float(_ht[s_, 0]), float(_ht[s_, 1])) for s_ in np.nonzero(_hh & _tn)[0]]
        if TENS_:   # speed pass: the tenure gates in one pass (each moment once; its titles side by side)
            TEN_S = np.array([e_[0] for e_ in TENS_], int); TEN_I = np.concatenate([e_[1] for e_ in TENS_])
            TEN_ST = np.cumsum([0] + [len(e_[1]) for e_ in TENS_[:-1]])
            TEN_LO = np.concatenate([np.full(len(e_[1]), e_[2]) for e_ in TENS_])
            TEN_HI = np.concatenate([np.full(len(e_[1]), e_[3]) for e_ in TENS_])
        f_pend = []                                                  # facets an act gave before their title came (newlywed, wedding week)
        PMASK_ = np.arange(PW_.shape[1])[None, :] < PN_[:, None]
        r_prof = np.zeros((N, NI_), int); r_drift = np.zeros((N, NI_), int)
        def fit_best(v_, i_):   # fit of colors v_ (C, or N x C) with the title's best-fitting profile
            f_ = np.tensordot(np.asarray(v_), PW_[i_].T, axes=1)
            return np.where(PMASK_[i_], f_, -np.inf).max(-1)
        MEM_K = np.isin(GR["pkind"], (0, 1)) & (GR["half"] > 0)      # skills and credentials leave a skill that fades by its half-life
        A_GR1 = np.full((L["S"], L["K"]), -1)                       # the perk an act grants (regaining is easier while the skill lasts)
        for (si_, ki_), fx_ in GR["A_FX"].items():
            gr_ = [j_ for op_, j_, _ in fx_["ok"] if op_ == "grants" and j_ >= NT_]
            if gr_: A_GR1[si_, ki_] = gr_[0]
        RULE_LOSS = np.array([GR["rule"][NT_ + p_]["lose"] is not None for p_ in range(NP_)], bool)   # lost only as the rule says
        ONCE_HOLD_ = [np.nonzero(GR["S_HOLDM"][:, i_] & np.asarray(L["ONCE"], bool))[0] for i_ in range(NI_)]
        KIND_NAMES_ = list(KNAMES) + ["status"]; KINDN_ = np.array(GR["kindname"][:NT_])   # batch.TITLE_KINDS
        EARN_ON = "A_EARN" in GR and bool((GR["HELP_N"] > 0).any() or (L.get("WINDOW_REF", np.zeros(1)) > 0).any())
        RID = GR["ID"]; LONG_ = RID.get("a long shot that missed", -1)
        C5F_ = RID.get("founder of a movement", -1) if P.get("c5_faith") else -1
        LONGF_ = np.zeros((L["S"], L["K"]), bool)            # options whose failure grants the long-shot perk (grants_if_fails:)
        for (si_, ki_), fx_ in GR["A_FX"].items():
            LONGF_[si_, ki_] = LONG_ >= 0 and any(op_ == "grants" and j_ == LONG_ for op_, j_, _ in fx_["fail"])
        LONGT_ = (GR["A_TITLE"] >= 0) | LONGF_
        TIER_ = np.asarray(GR.get("TIER", np.zeros(NI_, np.int8)))   # 1 a pack career, 2 a summit (batch._targets)
        AMS_ = GR.get("A_MISSED", np.zeros((L["S"], L["K"]), bool)); AMS_ON = bool(AMS_.any())
        TZM_ = np.minimum(np.asarray(GR.get("TIER_Z", np.zeros(NI_)), float),   # the budget's move on the odds, for
                          float(GR.get("BUDGET", {}).get("act_cap", 0.0)))         # {missed} (batch._chance)
        def missed_at(base_, ss_, aa_=None):
            """An option's title (A_TITLE or A_EARN rows) with title: {missed} read per person: the title that life last
            missed on a long shot (packs 09:39: the second try earns, counts tries and takes the tier lift)."""
            if not AMS_ON:
                return base_
            if aa_ is None:   # N x K rows for the moments ss_
                return np.where(AMS_[ss_] & (missed_t[:, None] >= 0), missed_t[:, None], base_)
            return np.where(AMS_[ss_, aa_] & (missed_t >= 0), missed_t, base_)
        OW_ = RID.get("out of work", -1); SOLDIER_ = RID.get("soldier", -1); CALL_ = SIDX.get("the call to serve", -1); CAP_K = np.array([P["community_titles"] if kk_ == COM else 1 for kk_ in range(NK)])
        ENGINE_GRANTED = {"widowed", "divorced", "retiree", "out of work", "newcomer", "veteran", "left the faith"}
        LZ_ = [i_ for i_ in range(NI_) if GR["rule"][i_]["lose"] is not None]
        AGES_T = [tuple(r_) for r_ in GR["ages"]]   # speed pass: each title's ages unpacked once (the same numbers)
        BG = [i_ for i_ in range(NI_) if GR["names"][i_] not in ENGINE_GRANTED and
              not (i_ < NT_ and TK_[i_] < NK and GR["rule"][i_]["rate"] is None)]      # items with a background rule
        TI_F = {list(GR["names"]).index(k_): float(f_) for k_, f_ in (P["ti_fit"] or {}).items() if k_ in list(GR["names"])}
        def r_rate(i_):
            r_ = GR["rule"][i_]
            if r_["rate"] is not None:
                return r_["rate"] * TI_F[i_] if i_ in TI_F else r_["rate"]   # F9: ti_fit
            lo_, hi_ = GR["ages"][i_]; span_ = max(1.0, min(hi_, lo_ + 40) - lo_)
            rt_ = -np.log(1 - min(GR["share"][i_], 0.95)) / span_
            return rt_ * TI_F[i_] if i_ in TI_F else rt_
    def r_note(n, i, what, how):
        role_log.append((int(n), t, int(i), what, how))
        if n in events:
            events[n].append(dict(role=dict(age=round(t / 52, 2), name=GR["names"][i], kind=GR["kindname"][i], what=what, how=how)))
    WL = None                                             # the outer world's link (set below when the world is on)
    EYES_LOSE_SKIP = {"replaced", "time passed", "outgrew it", "retired", "slipped away", "found work", "it ended",
                      "gave it up"}   # S3:
    # titles that end as the time or a commitment's end runs, or given up (the leaving itself is read, by end())
    def r_lose(n, i, why, succ=-1):
        if not r_has[n, i] and not (i >= NT_ and p_acc[n, i - NT_]):
            return
        r_has[n, i] = False; r_end[n, i] = t
        if (EYES_ON_ and WL is not None and i < NT_ and why not in EYES_LOSE_SKIP and not why.startswith("the ")
                and not why.startswith("became ") and why not in WHY):   # S3: a title lost in its own way (taken away, given
            WL.PP.eyes_see([n], PW_[i, r_prof[n, i]][None], [0.5], "title lost")   # up, its rule): read as walked away from
        if i < NT_:   # its facets go with it (no longer a newlywed once no longer married), unless they sit on another title
            for f_ in np.nonzero(REFM_[:, i] & r_has[n])[0]:   # held, or on the one that follows it (living together, married)
                if not (REFM_[f_] & r_has[n, :NT_]).any() and not (succ >= 0 and REFM_[f_, succ]):
                    r_lose(n, f_, "the " + GR["names"][i] + " ended")
        if i >= NT_:
            p_acc[n, i - NT_] = False; p_sus[n, i - NT_] = NEVER
            if not MEM_K[i - NT_]:
                p_lev[n, i - NT_] = 0.0                      # nothing left once access is gone (money spent, a bond broken)
        r_note(n, i, "lost", why)
        if i == SOLDIER_ and (t - r_since[n, i] >= 104          # however the service ends, after two years or more,
                              or (CALL_ >= 0 and t - r_since[n, i] >= 26 and sit_last[n, CALL_] >= r_since[n, i] - 8)):
            r_give(n, "veteran", "served")                     # or a conscript's term of half a year or more (W39)
    def r_gain(n, i, how, mix=None):
        if r_has[n, i]:
            return
        if P["title_ages"] and not (GR["ages"][i, 0] <= t / 52 <= GR["ages"][i, 1]):   # never outside the catalogue's ages
            return                                           # (C-X4: Emren's sanity check; the act still works)
        if CRS_ON and i < NT_ and TK_[i] < NK and CRS_J[TK_[i]] >= 0 and not held[n, TK_[i]]:
            j_ = CRS_J[TK_[i]]                               # F16: a title that would start a partnership, children or a faith
            if crs_rng.random() >= np.exp(CRS_MU[j_] + crs_own[n, j_] + (5 * w[n] - 1) @ CRS_T[j_]):   # leans as the acts do
                return
        if i < NT_ and REF_[i] >= 0 and not (REFM_[i] & r_has[n, :NT_]).any():
            f_pend.append((n, i, how, mix, t))               # a facet only on top of the title it refines: it waits a little
            return
        if i < NT_:                                          # the profile that fits: the act's colors, else the person's
            src_ = w[n] if mix is None else mix
            r_prof[n, i] = int(np.argmax(np.where(PMASK_[i], PW_[i] @ src_, -np.inf))); r_drift[n, i] = 0
        if i < NT_ and TK_[i] < NK:                          # a title of a commitment kind refines (or starts) that commitment
            kk = TK_[i]
            same = np.nonzero(r_has[n, :NT_] & (TK_ == kk) & (REF_[:NT_] < 0))[0]
            if REF_[i] < 0 and len(same) >= CAP_K[kk]:
                r_lose(n, same[np.argmin(r_since[n, same])], "replaced", succ=i)
            if not held[n, kk]:
                held[n, kk] = True; I[n, kk] = 0.2; sat[n, kk] = 0.6; since[n, kk] = t
                if RE_ON and kk == CAR:   # F8: an act that takes a job ends the retirement (one work status)
                    retired[n] = False
                pm_ = P["commit_mix"]
                prof[n, kk] = w[n].copy() if mix is None else pm_[0] * mix + pm_[1] * w[n] + pm_[2] * nic[n]
                commit_log.append((int(n), t, int(kk), "start", prof[n, kk].round(2).tolist(), 0.2))
                if n in events:
                    events[n].append(dict(commitment=dict(age=round(t / 52, 2), kind=KNAMES[kk], what="start", through=GR["names"][i],
                                                          profile=prof[n, kk].round(2).tolist())))
            if WAYS_[i].sum() > 0:                           # the role's expected ways become part of the commitment's profile
                held_k = np.nonzero(r_has[n, :NT_] & (TK_ == kk))[0]
                tw_ = (PW_[held_k, r_prof[n, held_k]].sum(0) + PW_[i, r_prof[n, i]]) / (len(held_k) + 1)
                prof[n, kk] = 0.5 * prof[n, kk] + 0.5 * tw_
        elif i >= NT_:
            p_ = i - NT_
            how = "regained" if p_lev[n, p_] > 0.05 and r_ever[n, i] else how
            p_acc[n, p_] = True; p_lev[n, p_] = 1.0; p_sus[n, p_] = NEVER
        first_ = not r_ever[n, i]
        r_has[n, i] = True; r_ever[n, i] = True; r_since[n, i] = t
        if len(ONCE_HOLD_[i]) and first_:                    # once: on a moment held by a title means once per title in a
            once_done[n, ROOT[ONCE_HOLD_[i]]] = False         # life (a second kind of career meets its new-stage moments
                                                              # again; the same title regained does not: Library 23:20)
        if i in TH_TITLE and first_:                         # a rung of a pathway: its threshold season opens (once:
            sea_open(n, NS + i)                              # back to the same line of work is no new crossing)
        r_note(n, i, "gained", how)
        if WL is not None:   # the world: a migrant's, refugee's or citizen's title moves the life between societies
            WL.on_title(int(n), GR["names"][i])
            if EYES_ON_ and (i < NT_ or GR["names"][i] == "someone with a record") and how != "arrested":
                # S3: their places see a title won (its profile's colours, else the act's), or a record (a crime found out:
                # the act's colours where an act gave it, else their own; a killing found out is read where it is caught)
                rec_ = GR["names"][i] == "someone with a record"
                src_ = mix if mix is not None else (PW_[i, r_prof[n, i]] if i < NT_ and not rec_ else w[n])
                src_ = src_ if np.sum(src_) > 0 else w[n]
                WL.PP.eyes_see([n], np.asarray(src_, float)[None], [0.0 if rec_ else 1.0], "crime" if rec_ else "title")
        if i < NT_ and f_pend:                               # facets an act gave while waiting for this title come with it
            for e_ in [e_ for e_ in f_pend if e_[0] == n and REFM_[e_[1], i]]:
                f_pend.remove(e_); r_gain(n, e_[1], e_[2], e_[3])
        for j_ in (GR["rule"][i]["grants"] if i < NI_ else []):
            r_gain(n, j_, "came with " + GR["names"][i])
    def r_close(n, i, why):
        """The last title of a commitment is gone: so is the commitment."""
        kk = TK_[i] if i < NT_ else NK
        if kk < NK and held[n, kk] and not (r_has[n, :NT_] & (TK_ == kk) & (REF_[:NT_] < 0)).any():
            end([n], [kk], why, t)
            if why == "retired":
                r_give(n, "retiree", "retired")
    def r_give(n, nm, how):
        if nm in RID:
            r_gain(n, RID[nm], how)
    def fx_targets(n, s_, j_):
        """What an act field acts on: the item named, the title held that brought the person here ({title}, -2), or every
        title of a kind held (kind:<kind>, -10 - the kind's index; the title itself, its facets go with it)."""
        if j_ >= 0:
            return [j_]
        if j_ == -2:
            h_ = held_title(n, s_)
            return [h_] if h_ >= 0 else []
        if j_ == -3:                                   # {missed}: the title of the last failed long shot
            return [int(missed_t[n])] if missed_t[n] >= 0 else []
        kn_ = KIND_NAMES_[-10 - j_]
        return [int(i_) for i_ in np.nonzero(r_has[n, :NT_] & (KINDN_ == kn_) & (REF_[:NT_] < 0))[0]]
    def held_title(n, s_):
        """The title (or perk) that brings person n to moment s_ (its holds:, with tenure: one held that long); the title
        itself before a facet on it, then the one held longest (explain.title_held tells the same one)."""
        ii_ = np.nonzero(GR["S_HOLDM"][s_] & r_has[n])[0]
        lo_, hi_ = GR["S_TEN"][s_]
        if not np.isnan(lo_):
            y_ = (t - r_since[n, ii_]) / 52; ii_ = ii_[(y_ >= lo_) & (y_ <= hi_)]
        if len(ii_) > 1:
            ii_ = sorted(ii_, key=lambda i_: (GR["refines"][i_] >= 0, r_since[n, i_]))
        return int(ii_[0]) if len(ii_) else -1
    def black_k():
        """black_edge: 1 + black_edge x how Black-led each person is now (Black share .2 -> 0, .5 or more -> 1)."""
        return 1.0 + P["black_edge"] * _uclip((w[:, 2] - 0.2) / 0.3, 0.0, 1.0)
    def r_weight(i_):
        """Who is likelier to gain it: practice in its ways (skills), colors that fit its ways, money, or ties."""
        wk_ = GR["rule"][i_]["weight"]
        if wk_ is None and i_ >= NT_ and GR["pkind"][i_ - NT_] == 0:
            wk_ = "practice"
        ind_ = GR["ind"][i_]
        if wk_ == "practice" and ind_.sum() > 0:
            return np.exp(_uclip(1.5 * (5 * (hist_m @ ind_) / ind_.sum() - 1), -2, 2))
        if wk_ == "colors" and WAYS_[i_].sum() > 0:
            return np.exp(_uclip(1.5 * (5 * fit_best(w, i_) - 1), -2, 2))
        if wk_ == "money":
            return np.exp(3 * (res[:, MON] - 0.5))
        if wk_ == "ties":
            return np.exp(3 * (res[:, TIE] - 0.5))
        return 1.0
    def r_act(n, op, j, yrs, how, mix=None):
        if op in ("title", "grants"):
            r_gain(n, j, how, mix)
        elif op == "drops":
            if r_has[n, j]:
                r_lose(n, j, "gave it up"); r_close(n, j, "left")
        elif op == "takes" and j >= NT_:
            r_lose(n, j, "taken away")
        elif op == "suspends" and j >= NT_ and p_acc[n, j - NT_]:
            p_sus[n, j - NT_] = t + int(yrs * 52); r_has[n, j] = False; r_note(n, j, "suspended", how)
        elif op in ("takes", "suspends"):
            r_lose(n, j, "taken away")
    def r_entry(n, kk, mix, ns_, move=False):
        """The first title of a commitment that has just started: one its rules allow, likelier the better its ways fit.
        move=True: a change inside a commitment already held (a new job), only to titles whose rules now hold."""
        cand = [i_ for i_ in range(NT_) if TK_[i_] == kk and GR["rule"][i_]["entry"] and REF_[i_] < 0 and GR["ages"][i_, 0] <= age <= GR["ages"][i_, 1]
                and not r_has[n, i_] and not (move and not GR["rule"][i_]["has_req"])]
        if not move and kk == CAR and P["occ_keep"] > 0:   # a new job is mostly in the same line of work as the last one
            prev_ = [i_ for i_ in range(NT_) if TK_[i_] == kk and REF_[i_] < 0 and not r_has[n, i_] and r_ever[n, i_]
                     and t - r_end[n, i_] <= 52 * P["occ_back"] and GR["ages"][i_, 0] <= age <= GR["ages"][i_, 1]
                     and TIER_[i_] != 2 and not GR["rule"][i_]["starts"]]   # never a summit or a seat won (packs 11:02)
            prev_ = [i_ for i_ in prev_ if ev_cond(GR["rule"][i_]["req"], ns_)[n]]   # and only while its rules still hold
            if prev_ and rng.random() < P["occ_keep"]:
                r_gain(n, max(prev_, key=lambda i_: r_end[n, i_]), "back to the same line of work")
                return
        ok_ = [i_ for i_ in cand if ev_cond(GR["rule"][i_]["req"], ns_)[n]]
        if not ok_ and not move:   # nobody's rules hold: a title with no rules of its own, else any but a pack career or
            ok_ = [i_ for i_ in cand if not GR["rule"][i_]["has_req"] and TIER_[i_] == 0] or \
                  [i_ for i_ in cand if TIER_[i_] == 0]   # summit (packs 11:02: no career from nothing)
        if not ok_:
            return
        wt_ = np.array([GR["share"][i_] * GR["rule"][i_]["norm"] * (np.exp(min(3.0, 2 * (5 * float(fit_best(mix, i_)) - 1))) if WAYS_[i_].sum() > 0 else 1.0)
                        for i_ in ok_])
        pick_ = ok_[int(rng.choice(len(ok_), p=wt_ / wt_.sum()))]
        if ID2 and TROLE_ON and TROLE_[pick_] >= 0:   # N1b: a job the world reserves for the other sex, as they are expected,
            # is closed by approval: taken only with closed_acc ^ units, else the person goes for another job (by weight)
            rs_n = min(1.0, float(np.broadcast_to(RS0, (N,))[n]) + (0.0 if WON else 0.5) * faith_given[n] * I[n, FAI])
            a_n = float(np.broadcast_to(AT0, (N,))[n]) if named_g[n] else 0.0
            ex_n = np.zeros(2); ex_n[int(not female[n])] += 1 - a_n; ex_n[int(female[n])] += a_n if gender_self[n] == 1 else 0.0
            tr_n = TROLE_[ok_]
            f_ = P["closed_acc"] ** (P["role_k"] * rs_n * np.where(tr_n >= 0, ex_n[1 - _uclip(tr_n, 0, 1)], 0.0))
            if ent_rng.random() >= f_[ok_.index(pick_)]:
                rest_ = [j_ for j_, i_ in enumerate(ok_) if i_ != pick_ and f_[j_] >= 1.0]
                if not rest_:
                    return
                w2_ = wt_[rest_]
                pick_ = ok_[rest_[int(rng.choice(len(rest_), p=w2_ / w2_.sum()))]]
        else:
            f_ = None
        acc_k_ = "acc_move" if move else "acc_first"
        ac_ = GR["rule"][pick_].get(acc_k_, 1.0)   # a route that overfills a title (Library next3
        if ac_ < 1 and ent_rng.random() >= ac_:    # §3): the job comes without that title
            if not P["acc_redraw"]:
                return
            out_ = {pick_}   # acc_redraw (v22.4): the next-best fit among the rest, each with its own acceptance
            while True:
                rest_ = [j_ for j_, i_ in enumerate(ok_) if i_ not in out_ and (f_ is None or f_[j_] >= 1.0)]
                if not rest_:
                    return
                w2_ = wt_[rest_]
                pick_ = ok_[rest_[int(ent_rng.choice(len(rest_), p=w2_ / w2_.sum()))]]
                ac_ = GR["rule"][pick_].get(acc_k_, 1.0)
                if not (ac_ < 1 and ent_rng.random() >= ac_):
                    break
                out_.add(pick_)
        r_gain(n, pick_, "changed jobs" if move else "came with the " + KNAMES[kk])

    HAD_IDX = {}
    NO_FOUND = np.zeros(N, bool)   # C5 founding (earth_rules INNER "a following of your own"): open only with c5_faith
    def cond_ns(t, age, w):
        """The engine's condition vocabulary (batch.COND_VOCAB): one value per person."""
        def ys(x):
            return np.where(x <= NEVER // 2, 99.0, (t - x) / 52.0)
        def mk(name, yrs=None):
            j_ = MIDX[name]; ok_ = mark_last[:, j_] > NEVER // 2
            return ok_ if yrs is None else ok_ & ((t - mark_last[:, j_]) <= np.asarray(yrs) * 52 + 1e-9)
        def had(names_, yrs):
            key_ = tuple(names_); idx_ = HAD_IDX.get(key_)   # speed pass: each list of names resolved once
            if idx_ is None:
                idx_ = HAD_IDX[key_] = [i_ for n_ in names_ for i_ in FAMILY.get(n_, [SIDX[n_]] if n_ in SIDX else [])]
            return ((t - sit_last[:, idx_]) <= yrs * 52).any(1) if idx_ else np.zeros(N, bool)
        ns = dict(abs=np.abs, mk=mk, mk_ok=lambda name, yrs=None: mk(name, yrs) & mark_ok[:, MIDX[name]],
                  mkn=lambda name: mark_n[:, MIDX[name]], mk_span=lambda name: ys(mark_first[:, MIDX[name]]) * (mark_n[:, MIDX[name]] > 0),
                  had=had, chance=lambda p: rng.random(N) < p,
                  age=age, age_mod=int(age) % 10, decade_edge=int(age) % 10 in (9, 0), round_birthday=int(age) % 10 == 0, stage=stage,
                  stress=stress, mood=mood, satisfaction=content, peace=peace, react=react, steady=steady, base_mood=base_mood,
                  outlook=outlook, support=support, wound=wound, trouble=trouble, fortune=fortune, cload=cload,
                  yrs_any=np.where(held, (t - since) / 52, 0).max(1), kids_home=kids, retired=retired, widowed=widowed,
                  fails13=fails13, hedon_n=hedon_n, bodyhab_n=bodyhab_n, n_moves=n_moves, heavy_risk=heavy_risk, bind_m=bind_m,
                  n_dream=(gk == 0).sum(1), n_passion=(gk == 1).sum(1), n_plan=(gk == 2).sum(1),
                  regret=regret, horizon=fhz, discipline=dsc, self_control=ctrl,     # v7: what was let go, time felt short, learned control
                  harsh=drv_h, unrest=drv_u, prosper=drv_p, era=era_i[t],
                  founding=(WL.W.c5_founding(WL.PP.loc) if WL is not None and P.get("c5_faith") else NO_FOUND),   # C5: a
                  # movement founded in the person's town within the year (the founding took a free slot)
                  haunts=np.full(N, bool(P.get("sph_haunts")) and WON))   # spheres phase 2: haunts built (the haunt choices)
        ns.update({nm_: stage == i_ for i_, nm_ in enumerate(STAGE_NAMES)})
        ns.update({nm_: need[:, i_] for i_, nm_ in enumerate(NEEDS)}); ns.update({nm_: res[:, i_] for i_, nm_ in enumerate(RESOURCES)})
        for i_, c_ in enumerate(COLORS):
            ns[c_] = w[:, i_]; ns["h" + c_] = hist_m[:, i_]; ns["e" + c_] = hist_e[:, i_]
        for i_, k_ in enumerate(KNAMES):
            ns["held_" + k_] = held[:, i_]; ns["yrs_" + k_] = np.where(held[:, i_], (t - since[:, i_]) / 52, 0.0)
            ns["ago_end_" + k_] = ys(end_t[:, i_])
        for i_, r_ in enumerate(ROLES[:4]):
            ns["alive_" + r_] = alive[:, i_]
        ns["alive_child"] = alive[:, 5]                    # R15: living children (a child's death leaves the others)
        ns["kid_young"] = np.where(held[:, KID] & (kid_last > NEVER // 2), (t - kid_last) / 52, 99.0)   # F7: the youngest's years
        ns["older_siblings"] = older_sib; ns["younger_siblings"] = younger_sib   # birth order (N4)
        for k_ in AGO:
            ns["ago_" + k_] = ys(ago[k_])
        ns.update(streak)
        ns["married"] = held[:, PAR] & (sit_last[:, SIDX["getting married"]] >= since[:, PAR]) if "getting married" in SIDX else np.zeros(N, bool)
        ns.update(female=female, male=~female, attr=attr, unease=unease)   # identity (point 11): sex, attraction 0-4, unease
        if ID2:   # N1b (chroma-identity/for-the-engine.md §2)
            rs_v, at_v, _ = role_view()
            ns.update(trans=gender_self == 1, nonbinary=gender_self == 2, ace=ace, intersex=intersex, partner_same=partner_same,
                      named_gender=named_g, cross_title=cross_title, role_fit=1 - rfit_avg, role_strict=rs_v, accept_trans=at_v)
        else:
            ns.update(trans=unease, nonbinary=np.zeros(N, bool), ace=ace, intersex=intersex, partner_same=np.zeros(N, bool),
                      named_gender=np.zeros(N, bool), cross_title=np.zeros(N, bool), role_fit=np.ones(N),
                      role_strict=np.zeros(N), accept_trans=np.full(N, 0.5))
        if RON:   # titles and perks: has('nurse'), was('soldier'), yrs_has('homeowner')
            ns["has"] = lambda nm: r_has[:, RID[nm]]; ns["was"] = lambda nm: r_ever[:, RID[nm]]
            ns["yrs_has"] = lambda nm: np.where(r_has[:, RID[nm]], (t - r_since[:, RID[nm]]) / 52, 0.0)
            ns["n_titles"] = r_has[:, :NT_].sum(1); ns["n_perks"] = r_has[:, NT_:].sum(1)
        else:
            ns["has"] = ns["was"] = lambda nm: np.zeros(N, bool); ns["yrs_has"] = lambda nm: np.zeros(N)
            ns["n_titles"] = ns["n_perks"] = np.zeros(N)
        ns["betrayed"] = had(["a partner's affair comes to light", "betrayed by a friend or a business partner"], 10)
        # stage 2 (Library's for-the-engine-stage2.md): a colour's rise over some years, how long it (or a pair) has held
        # above a share (quarterly, up to ten years), and the shadow's force, part, seen and years since its reflection
        def q_back(yrs):
            return w_q[(w_qi - 1 - int(round(4 * yrs))) % 40] if w_qi > int(round(4 * yrs)) else np.full((N, C), 0.2)
        def q_run(ok_):   # ok_ (40 quarters newest first, N): the quarters in a row, from the newest, that hold, in years
            return np.cumprod(ok_, 0).sum(0) / 4.0
        def q_new():
            return w_q[(w_qi - 1 - np.arange(min(w_qi, 40))) % 40]
        def first_age(names_):   # the age a moment (or any of a list) was first met, 99 if never
            idx_ = [i_ for n_ in names_ for i_ in FAMILY.get(n_, [SIDX[n_]] if n_ in SIDX else [])]
            if not idx_:
                return np.full(N, 99.0)
            f_ = np.where(sit_first[:, idx_] <= NEVER // 2, 10 ** 9, sit_first[:, idx_]).min(1)
            return np.where(f_ >= 10 ** 9, 99.0, f_ / 52.0)
        ns.update(first_age=first_age, rise=lambda c, yrs=2: w[:, IDX[c]] - q_back(yrs)[:, IDX[c]],
                  above_yrs=lambda c, th: q_run(q_new()[:, :, IDX[c]] > th),
                  pair_yrs=lambda c1, c2, th: q_run((q_new()[:, :, IDX[c1]] > th) & (q_new()[:, :, IDX[c2]] > th)),
                  sh=lambda c: shA[:, IDX[c]], sh_part=lambda c: shS[:, IDX[c]], sh_seen=lambda c: sh_seen[:, IDX[c]],
                  sh_ago=lambda c: ys(sh_rt[:, IDX[c]]))
        ns["adj"] = lambda nm: adj[:, ADJ_ID[nm]]                       # v7 adjectives: adj('wealthy'), is_wealthy
        ns["yrs_adj"] = lambda nm: np.where(adj[:, ADJ_ID[nm]], (t - adj_since[:, ADJ_ID[nm]]) / 52, 0.0)
        ns.update({"is_" + nm_.replace(" ", "_"): adj[:, i_] for i_, nm_ in enumerate(ADJ_NAMES)})
        return ns
    def ev_cond(code, ns):
        r_ = eval(code, EV_G, ns)
        if type(r_) is np.ndarray and r_.shape == (N,):   # speed pass: the same copy, without broadcasting
            return r_.astype(bool)
        if isinstance(r_, (bool, np.bool_)):
            return np.ones(N, bool) if r_ else np.zeros(N, bool)
        return np.broadcast_to(np.asarray(r_), (N,)).astype(bool)
    def ev_memo(code, ns, memo):
        """Speed pass: ev_cond, reusing the answer of an equal condition already read with the same ns. Never for one
        that draws chance (a fresh draw each time) or reads sa (set per echo)."""
        if memo is None or "chance" in code.co_names or "sa" in code.co_names:
            return ev_cond(code, ns)
        r_ = memo.get(code)
        if r_ is None:
            r_ = memo[code] = ev_cond(code, ns)
        return r_
    def factor(c_, ns, memo=None):
        f_ = np.ones(N)
        if not c_["more"] and not c_["less"]:   # speed pass: nothing to read, so 1 (as clip of ones gave)
            return f_
        for cd in c_["more"]:
            f_ = f_ * np.where(ev_memo(cd, ns, memo), P["cond_more"], 1.0)
        for cd in c_["less"]:
            f_ = f_ * np.where(ev_memo(cd, ns, memo), P["cond_less"], 1.0)
        return np.minimum(np.maximum(f_, 0.1), 6.0)   # speed pass: clip's own two steps, without its wrapper

    # threshold seasons (see season): which moments belong to which crossing, and each person's open season
    TH_K = np.full(L["S"], -1); TH_STEP = np.zeros(L["S"], int); TH_TR = np.zeros(L["S"], bool); TH_P = np.ones(L["S"])
    for si_, x_ in enumerate(L.get("src", []) if BAT else []):
        th_ = str(x_.get("threshold") or "").strip()
        if not th_:
            continue
        if th_.startswith("title:"):
            if not RON:
                continue
            if th_[6:].strip() not in GR["ID"]:
                raise ValueError(f"{L['names'][si_]}: threshold: {th_} names no title in the catalogue")
            TH_K[si_] = NS + GR["ID"][th_[6:].strip()]
        elif th_ in STAGE_NAMES:
            TH_K[si_] = STAGE_NAMES.index(th_)
        else:
            raise ValueError(f"{L['names'][si_]}: threshold: {th_} is neither a life stage {STAGE_NAMES} nor title:<name>")
        TH_STEP[si_] = int(x_.get("step") or 1)
        TH_TR[si_] = str(x_.get("transform") or "").strip().lower() in ("yes", "true", "1")
        if P["season_share"]:   # the share of lives its times: line gives ("perhaps 1 in 20", "about half"); else every season
            tm_ = str((x_.get("timing") or {}).get("times") or x_.get("times") or "").lower()
            m_ = re.search(r"\b1 in (\d+)", tm_)
            TH_P[si_] = 1.0 / float(m_.group(1)) if m_ else 0.5 if "half" in tm_ else 1.0
            if P["season_excl"]:   # K6: "1 homeowner in 20" counts too, and the words alone give a share
                m_ = re.search(r"\b1 (?:[a-z-]+ ){0,3}in (\d+)", tm_)
                h_ = [(m2_.start(), v_) for k_, v_ in P["season_words"] for m2_ in [re.search(r"\b" + k_, tm_)] if m2_]
                w_ = min(h_)[1] if h_ else 1.0   # the first such word in the line
                TH_P[si_] = 1.0 / float(m_.group(1)) if m_ else 0.5 if "half" in tm_ else w_
    SEA_ON = bool(P["season"]) and bool((TH_K >= 0).any())
    TH_ANY = TH_K >= 0; TH_TITLE = {int(k_ - NS) for k_ in TH_K[TH_K >= NS]}
    sea_k = np.full(N, -1); sea_t0 = np.zeros(N, int); sea_done = np.zeros((N, 4), bool); sea_log = []   # steps 1-3, transform
    sea_had = np.zeros((N, NS), bool)                     # a stage's season comes once in a life
    sea_rng = np.random.default_rng([int(seed), 79])       # season_share's draws, on their own stream
    ent_rng = np.random.default_rng([int(seed), 80])       # a first job's or a job move's title acceptance (acc_first, acc_move)
    far_rng = np.random.default_rng([int(seed), 81])       # whether one's own move is to a new town (far_share, E6)
    fam_rng = np.random.default_rng([int(seed), 84])       # whether the family's move is to a new town (move_near, K2)
    def _mv_far(x_):   # K2: moves: far / near from the Library; moves: yes is far when the moment names a new town
        v_ = str(x_.get("moves")).strip().lower()
        return 1.0 if v_ == "far" else 0.0 if v_ == "near" else 1.0 if "new town" in str(x_.get("name", "")) else P["fam_far"]
    MVF_ = np.array([_mv_far(x_) for x_ in L.get("src", [])] + [P["fam_far"]] * (L["S"] - len(L.get("src", []))))
    RETIRES_ = np.array([bool(x_.get("retires")) for x_ in L.get("src", [])] + [False] * (L["S"] - len(L.get("src", []))))
    ELD_ = STAGE_NAMES.index("elder")
    # retirement is the crossing into later life (the Library, 22:30): when the batch's elder season has a moment that
    # retires the person ('the last day at work'), retiring opens that season and its first step is the last day
    RET_SEA = SEA_ON and P["retire_season"] and bool((RETIRES_ & (TH_K == ELD_) & (TH_STEP == 1)).any())
    ret_pend = np.full(N, -1)
    # share: <0-1> on a moment (the Library, 23:50): the real share of people who ever meet it in life. Who they are is
    # drawn once, at birth (the person who goes fishing, runs a half marathon, volunteers at a shelter); the moment stays
    # closed to everyone else, and its once, gap and rate shape it for those it can come to
    SH_I = np.array([i_ for i_, x_ in enumerate(L.get("src", []) if BAT else []) if x_.get("share") is not None], int)
    SH_ON = len(SH_I) > 0
    if SH_ON:
        sh_v = np.array([float(L["src"][i_]["share"]) for i_ in SH_I])
        if ((sh_v <= 0) | (sh_v > 1)).any():
            raise ValueError(f"share: must be above 0 and at most 1 ({[L['names'][i_] for i_ in SH_I[(sh_v <= 0) | (sh_v > 1)]]})")
        if RON:   # the share is of all people: on a holds: moment, the draw among holders is share / the holders' share
            for j_, i_ in enumerate(SH_I):   # (the packs, 01:40: a door that needs holders reached only share x holders)
                if GR["S_HASHOLD"][i_]:
                    hsh_ = min(1.0, float(GR["share"][GR["S_HOLDM"][i_]].sum()))
                    sh_v[j_] = min(1.0, sh_v[j_] / hsh_) if hsh_ > 0 else sh_v[j_]
        SH_U = np.random.default_rng([int(seed), 17]).random((N, len(SH_I)))   # its own random stream
        grp_ = [str(L["src"][i_].get("share_group") or "").strip() for i_ in SH_I]
        for g_ in set(grp_) - {""}:   # share_group: one draw for the moments of a group (the two halves of a pair): with a
            jj_ = [j_ for j_, x_ in enumerate(grp_) if x_ == g_]   # common draw, those open to the rarer one are open to all
            SH_U[:, jj_] = SH_U[:, [jj_[0]]]
        SH_EL = SH_U < sh_v[None]
    SW_ = np.append(np.asarray(P["season_weeks"], int), int(P["season_tr_week"]))   # the weeks of steps 1-3 and the transform
    SEA_LEN_Y = P["season_len"] / 52
    # the ages a stage's season moments are written for: where their age windows meet, within the rite's own window
    SEA_LO = np.full(NS, np.nan); SEA_HI = np.full(NS, np.nan)
    for k_ in range(1, NS):
        m_ = TH_K == k_
        if SEA_ON and m_.any():
            lo_, hi_ = max(L["AGE"][m_, 0].max(), STAGE_LO[k_]), min(L["AGE"][m_, 1].min(), STAGE_HI[k_])
            if hi_ - lo_ < SEA_LEN_Y:   # the windows do not meet: the typical one
                lo_ = max(float(np.median(L["AGE"][m_, 0])), STAGE_LO[k_])
                hi_ = max(lo_ + SEA_LEN_Y, min(float(np.median(L["AGE"][m_, 1])), STAGE_HI[k_]))
            SEA_LO[k_], SEA_HI[k_] = lo_, hi_
    SEA_AGE_ON = SEA_ON and bool(P["season_by_age"]) and bool((~np.isnan(SEA_LO)).any())
    SEA_KS = [k_ for k_ in range(1, NS) if not np.isnan(SEA_LO[k_])]
    sea_age = (np.nan_to_num(SEA_LO)[None] + np.random.default_rng([int(seed), 13]).random((N, NS))
               * np.maximum(np.nan_to_num(SEA_HI - SEA_LO) - SEA_LEN_Y, 0)[None])   # its own random stream

    def sea_fits(k_, a_):   # a crossing at age a_ can open stage k_'s season (its moments can still be met)
        return not SEA_AGE_ON or k_ >= NS or np.isnan(SEA_LO[k_]) or (SEA_LO[k_] <= a_ <= SEA_HI[k_] - SEA_LEN_Y)

    # a wider world (point 11): the Library's death_if_fails: and kills: on options
    A_DEATH = np.zeros((L["S"], L["K"])); A_KILL = np.full((L["S"], L["K"]), -1)   # -2: someone the engine does not track
    A_KILLF = np.full((L["S"], L["K"]), -1); A_KILLFS = np.ones((L["S"], L["K"])); A_MOVE = np.zeros((L["S"], L["K"]), bool)
    A_LACK = np.ones((L["S"], L["K"]))   # lacking: <share>: without what the act requires, this share of the written chance
    CHILD_W = {"child", "children", "son", "daughter", "baby", "kid", "a child", "your child", "toddler", "pupil"}
    for si_, row_ in enumerate(L.get("notes", []) if BAT else []):
        for ki_, nt_ in enumerate(row_ or []):
            if not isinstance(nt_, dict):
                continue
            if nt_.get("death_if_fails"):
                A_DEATH[si_, ki_] = float(nt_["death_if_fails"])
            if nt_.get("kills"):
                r_ = str(nt_["kills"]).strip().lower()
                if r_ in CHILD_W:
                    raise ValueError(f"{L['names'][si_]}: kills: {r_} - a child is never a victim (Emren 2026-10-04 22:43)")
                A_KILL[si_, ki_] = ROLES.index(r_) if r_ in ROLES else -2
            if nt_.get("kills_if_fails"):   # the person named dies if the act fails (a friend who will not wake up);
                r_ = str(nt_["kills_if_fails"]).strip().lower()         # '<role> <share>': in that share of failures
                if len(r_.split()) > 1:
                    try:
                        A_KILLFS[si_, ki_] = float(r_.split()[-1]); r_ = " ".join(r_.split()[:-1])
                    except ValueError:
                        pass
                    if not 0 < A_KILLFS[si_, ki_] <= 1:
                        raise ValueError(f"{L['names'][si_]}: kills_if_fails: the share must be above 0 and at most 1")
                if r_ in CHILD_W:
                    raise ValueError(f"{L['names'][si_]}: kills_if_fails: {r_} - a child is never a victim (Emren 2026-10-04 22:43)")
                A_KILLF[si_, ki_] = ROLES.index(r_) if r_ in ROLES else -2
            if nt_.get("lacking") is not None:   # the packs (23:00): an outsider can try, but rarely wins (election night)
                A_LACK[si_, ki_] = float(nt_["lacking"])
                if not 0 < A_LACK[si_, ki_] <= 1:
                    raise ValueError(f"{L['names'][si_]}: lacking: must be a share above 0 and at most 1")
            if str(nt_.get("moves", "")).strip().lower() in ("yes", "true", "1"):   # the act moves the person (take the job abroad)
                A_MOVE[si_, ki_] = True
    AD_ON = bool((A_DEATH > 0).any()); AK_ON = bool((A_KILL != -1).any()); AKF_ON = bool((A_KILLF != -1).any())
    LACK_ON = bool((A_LACK < 1).any())
    # N1b: each option's role (women, men, keep, cross; an act that grants a title marked role= counts as that sex's act),
    # the options that name one's own gender (norm: transition, its mark, or came out in a moment only about gender), and
    # the moments that read who someone is
    IDC_ON = IDF_ON = TROLE_ON = False
    if ID2 and BAT:
        ROLE_ACT = np.array(L.get("ROLE_OPT", np.full((L["S"], L["K"]), -1)))
        TROLE_ = np.asarray(GR.get("role", np.full(NT_, -1))) if RON else np.zeros(0, int)
        TROLE_ON = bool((TROLE_ >= 0).any())
        if TROLE_ON:
            tr_ = GR["A_TITLE"]; tt_ = _uclip(tr_, 0, NT_ - 1)
            ROLE_ACT = np.where((ROLE_ACT < 0) & (tr_ >= 0) & (tr_ < NT_), TROLE_[tt_], ROLE_ACT)
        IDG = np.asarray(L.get("ID_GATE", np.zeros((L["S"], 4), bool)))
        IDF_ON = bool(IDG.any())
        COME_K = MIDX.get("came out", -1); NAMED_K = MIDX["named their gender"]
        CO_SPLIT = np.where(IDG[:, 0] & ~IDG[:, 1], 1, np.where(IDG[:, 1] & ~IDG[:, 0], 2, 0))   # came out tells: 0 all, 1 gender, 2 attraction
        TRANS_OPT = (L["MARK"] == NAMED_K) | ((L["MARK"] == COME_K) & (CO_SPLIT == 1)[:, None] & (COME_K >= 0))
        if "W_NORM" in L and WKEYS is not None:
            TRANS_OPT |= L["W_NORM"] == WKEYS.NORM_KEYS.index("transition")
        # a moment open to either mark (came out, or named their gender: growing old without hiding again): its written
        # closed: approval reads, for someone who named their own gender, how far the world accepts that (Library 10-07)
        MKBOTH_ = np.zeros(L["S"], bool)
        for c_ in L["COND"]:
            if "'came out'" in c_["rtxt"] and "'named their gender'" in c_["rtxt"]:
                MKBOTH_[c_["s"]] = True
        OPENMK_ = MKBOTH_[:, None] & (np.asarray(L["CLOSED"]) == 1)   # 1: approval (batch.WITHOUT)
        IDC_ON = bool(((ROLE_ACT >= 0) & (ROLE_ACT != 2)).any() or TRANS_OPT.any())
        COND_S = {c_["s"] for c_ in L["COND"]}
        INTIM_ = [int(x) for x in L.get("INTIM", [])]; BABY_ = SIDX.get("a baby on the way, planned or not", -1)
        PSP_ = np.asarray(P["partner_same_p"], float)

    def role_view():   # N1b: how strict the world is with each person, how far it accepts their own gender, which role it
        # expects of them (women, men): the sex they were raised as, and once they have named their own gender, that one
        # by the accepting share (a named nonbinary person's own gender carries no role, so that share expects nothing)
        rs_ = np.minimum(1.0, RS0 + (0.0 if WON else 0.5) * faith_given * I[:, FAI])   # with the world on the faith's
        # community is in the local norms already (outer world round 3, point 3)
        at_ = np.broadcast_to(np.asarray(AT0, float), (N,)).copy()   # the setting's share, or each person's with the world on
        a_ = np.where(named_g, at_, 0.0); bi_ = (~female).astype(int)
        ex_ = np.zeros((N, 2)); ex_[ar, bi_] += 1 - a_; ex_[ar, 1 - bi_] += np.where(gender_self == 1, a_, 0.0)
        return rs_, at_, ex_

    def die(n_, cause):   # the character's own death (self_death): the life is idle from now on
        if not dead[n_]:
            dead[n_] = True; died.append((int(n_), t, cause))
            if n_ in events:
                events[n_].append(dict(died=dict(age=round(t / 52, 2), cause=cause)))

    def sea_open(n_, k_):   # a crossing opens a season (a new one replaces one still running)
        if SEA_ON and ((k_ < NS and sea_had[n_, k_]) or dead[n_]):
            return
        if SEA_ON and (TH_K == k_).any():
            if k_ < NS:
                sea_had[n_, k_] = True
            sea_k[n_] = k_; sea_t0[n_] = t; sea_done[n_] = False
            sea_log.append((int(n_), t, int(k_)))

    WON = bool(P["world"]) and BAT                     # the outer world (world-build.md, "How the engine reads the world")
    MK_ON = bool(P.get("sph_marks")) and WON           # spheres phase 2: the mark of the work (world on only)
    EYES_ON_ = bool(P.get("sph_eyes")) and bool(P.get("sph_haunts")) and WON   # S3: their places read their acts (world on, with the haunts)
    ODD_ON_ = EYES_ON_ and bool(P.get("sph_odd"))      # S4: the odd one out at a place
    SHAR_ON = bool(P.get("sph_shadow")) and WON        # spheres phase 5: the shadow around a life (with shadows)
    DEEP_ON = bool(P.get("sph_deep")) and WON          # spheres phase 5: the care load
    WL2_ON = bool(P.get("wl2")) and WON                # WL2: prices for workers too, a recession's hours, a disaster's cost, a pandemic year
    CLU_ON = BAT and (IDC_ON or WON)                   # closures counted in units (N1b roles, the world's laws and norms)
    WL = None; drv_h, drv_u, drv_p = P["world_harsh"], P["world_unrest"], P["world_prosper"]
    LW_ON = False; LW_T_ = None   # S7 lead_ways (world on, with sph_levers): the office titles a post is made of
    SEEN_ON = False
    OWN_ON = bool(P.get("own_open")) and "OWN" in L       # v22.5, F12: the culture's own acts always on offer
    STH_ON = False; STH_SOC = None; STH_FW = None         # v22.5, F12: the start holds (world on)
    if WON:
        import world_link as WLM
        WL = WLM.WorldLink(sys.modules[__name__], P, L, N, seed, female, attr, KILLS, ENDS, CAR)
        WL.PP.or_on = bool(P.get("one_roll"))   # F7: a partner the world takes is not replaced (world_people._sync)
        LW_ON = bool(getattr(WL, "lw", False)) and RON
        if LW_ON:
            LW_T_ = WL.lw_tid
        nic = np.array(WL.PP.niche, float); circle = nic.copy()
        STH_ON = bool(P.get("start_hold"))
        if STH_ON and (getattr(WL, "start", None) or {}).get("society") is not None:   # the start's society around them
            STH_SOC = np.asarray(WL.start["society"], float); STH_SOC = STH_SOC / STH_SOC.sum()
            STH_FW = np.asarray(P["f_world"], float)
            nic = (1 - P["start_soc"]) * nic + P["start_soc"] * STH_SOC; circle = nic.copy()
        SEEN_ON = bool(P.get("seen_done")) and WL.seen_on   # S6, seen it done: felt odds and young dreams (world_people)
        if SEEN_ON:
            SD_DREAM_ = float(WL.PP.sd_par["dream"]); SD_AGES_ = tuple(WL.PP.sd_par["dream_ages"])
        if getattr(WL.PP, "family_mix", None) is not None:
            fam = np.array(WL.PP.family_mix, float)
        older_sib = np.asarray(WL.PP.older_sib, int).copy(); younger_sib = np.asarray(WL.PP.younger_sib, int).copy()
        alive[:, :5] = WL.PP.alive
        era_at.clear()                                     # the world's own eras replace the engine's drawn history
        W_WHO_ = L.get("W_WHO", [[] for _ in range(L["S"])])
        SAC_ON_ = bool(getattr(WL.PP, "sac_on", False))   # S5: the world's switch (P["sacred"], or a World made with it)
        if RON:
            W_SEC_ = np.asarray(GR.get("sector", np.full(NT_, -1)))[:NT_]; W_STD_ = np.asarray(GR.get("standing", np.full(NT_, -1)))[:NT_]
            W_GOV_ = [RID[x_] for x_ in ("minister", "head of government") if x_ in RID]; W_HOG_ = RID.get("head of government", -1)
            W_SDI_ = np.nonzero(W_STD_ >= 0)[0]   # titles with a standing, and the domain each counts in (spec 7 §2)
            _ins = np.asarray(GR.get("institution", np.full(NT_, -1)))[:NT_]; _sec = W_SEC_
            W_SDOM_ = np.array([WLM.WK.DOMAINS.index(WLM.title_domain(GR["names"][i_], WLM.WK.INST_KINDS[_ins[i_]] if _ins[i_] >= 0 else None,
                                                                     WLM.WK.SECTORS[_sec[i_]] if _sec[i_] >= 0 else None)) for i_ in W_SDI_], int)
        KCHILD_ = KILLS == ROLES.index("child")
        dq_ = np.zeros((N, 5), bool); dq_t = np.zeros((N, 5), np.int64)   # a cast death waiting for its moment (role, since)
        clim_w = np.zeros(N); DIS_J_ = [j_ for j_, e_ in enumerate(EVR) if WLM.DIS_EVR.search(e_["name"])]
        evr_ok = np.zeros((N, len(EVR)))   # a disaster's outside event comes again only after its shortest gap

        def world_cast(lst_):   # the cast's events in the story: a push is reported once (world_push), and a want the
            for e_ in lst_:     # moment met or refused once (cast_want)
                if e_.get("n") in events and e_.get("kind") != "push" and not (e_.get("kind") == "want" and "worked" in e_):
                    events[e_["n"]].append(dict(cast=e_))
        # WL6, for P["dis_match"] (the game may turn it on mid-run): the hazards each disaster event fits (by name); one
        # naming no hazard fits them all
        hz_j_ = {j_: {h_ for h_, rx_ in WLM.HAZ_EVR.items() if re.search(rx_, EVR[j_]["name"], re.I)} for j_ in DIS_J_}
        DIS_FOR_ = {}
        for h_ in WLM.HAZ_EVR:
            own_j_ = [j_ for j_ in DIS_J_ if h_ in hz_j_[j_]]; any_j_ = [j_ for j_ in DIS_J_ if not hz_j_[j_]]
            DIS_FOR_[h_] = set(own_j_ or any_j_ or DIS_J_)
    SV_ON = bool(P.get("sph_deep")) and WON and RON  # spheres phase 5: service as a chapter (deep_state.service)
    if SV_ON:
        import sphere_data as SD_, world_keys as WK_
        SVC_T = np.array([RID[x_] for x_ in ("soldier", "police officer") if x_ in RID], int)   # the host, the guard
        PROT_N = {"soldier", "police officer", "firefighter", "security guard"}
        def t_sph_(i_):   # a title's sphere: by name for the force, else its institution's, else its sector's
            if GR["names"][i_] in PROT_N:
                return "prot"
            in_ = int(GR["institution"][i_]) if "institution" in GR else -1
            if in_ >= 0 and WK_.INST_SPHERE[WK_.INST_KINDS[in_]]:
                return WK_.INST_SPHERE[WK_.INST_KINDS[in_]]
            se_ = int(GR["sector"][i_]) if "sector" in GR else -1
            return WK_.SECTOR_SPHERE[WK_.SECTORS[se_]] if se_ >= 0 else None
        PR_T = np.array([t_sph_(i_) in ("prot", "rule") for i_ in range(NT_)] + [False], bool)   # (-1: no title)
        SVS_ = SD_.DEEP["service"]; HV_ = SVS_["after_guard_or_host"]["hiring"]
        RW_ = float(SD_.DEEP["record_weight"].get(getattr(WL.W, "sph_epoch", "modern"), 1.0))
        # hiring odds as the options' difficulty (DIFF units: odds x exp(-3 x d))
        SV_D = (-np.log(1 + HV_["prot"]) / 3, -np.log(1 + HV_["other"]) / 3, -np.log(1 - 0.5 * RW_) / 3)
        # debts and holdings (deep_state.debts, holdings, money_map): a ledger of up to four debts and two holdings per
        # life, on the engine's money: a year's income is mt, a month's mt / 12 (spheres-phase5b-asks.md)
        DBT_ = SD_.DEEP["debts"]["holders"]; MM_ = SD_.DEEP["money"]; HKS_ = SD_.DEEP["holdings"]["kinds"]; DP_ = P["deep_par"]
        D_KIND = ["tab", "kin", "circle", "bank", "lender", "home_loan"]
        D_RATE = np.array([float(DBT_[k_]["rate"]) for k_ in D_KIND[:5]] + [0.04])
        D_SIZE = np.array([float(DBT_[k_]["size_months"]) for k_ in D_KIND[:5]] + [0.0])
        D_TERM = np.array([float(MM_["term_months"][k_]) for k_ in D_KIND])
        LSF_TERM = float(MM_["term_months"].get("land_shop_firm_loan", 120.0))   # land, a shop or a firm on a bank loan
        LT_I = next((i_ for i_, e_ in enumerate(SD_.EV) if e_["key"] == "land_taken"), -1)   # prod.land_taken
        WL.PP.care_buy_x = float(DP_["care_buy"][1])
        ep_ = getattr(WL.W, "sph_epoch", "modern")
        EPI_ = SD_.EPOCHS.index("sail" if ep_ == "magic" else ep_)   # magic: as sail, its base
        D_FROM = np.array([SD_.EPOCHS.index(DBT_[k_]["from"]) for k_ in D_KIND[:5]] + [SD_.EPOCHS.index("sail")])
        D_LEND = EPI_ >= D_FROM                              # which holders lend in this world's epoch
        H_KIND = ["home", "land_boat_herd", "workshop_shop", "firm"]
        H_VAL = np.array([float(HKS_[k_]["value_years"]) for k_ in H_KIND])
        H_YV = H_VAL * np.array([float(HKS_[k_]["yield"]) for k_ in H_KIND])   # a year's yield in years of income
        H_OK = EPI_ >= np.array([1, 1, 1, SD_.EPOCHS.index(HKS_["firm"].get("from", "sail"))])   # bands: no holdings
        NL_ = float(MM_["need_line"]); YR_ = 52; ER_ = ep_ if ep_ != "magic" else "sail"
        DL_ = int(SD_.DEEP["debts"]["ledger"])
        dk = np.full((N, DL_), -1); dsz = np.zeros((N, DL_)); dbal = np.zeros((N, DL_)); dpaid = np.zeros((N, DL_), int)
        dterm = np.ones((N, DL_)); drate = np.zeros((N, DL_)); dhold = np.full((N, DL_), -1)   # the holding a loan bought
        dstr = np.zeros((N, DL_), bool)                      # a kin debt stretched once by another term
        ev_seen = [0]                                        # the sphere events read so far (a land taking)
        hk = np.full((N, int(SD_.DEEP["holdings"]["max"])), -1)
        tab_shut = np.full(N, NEVER); kin_shut = np.full(N, NEVER); circ_out = np.zeros(N, bool); brec = np.full(N, NEVER)
        d_inc = np.full(N, float(P["money_base"]))           # a year's income, mt before holdings and payments
        car_prev = np.zeros(N, bool); hea_prev = np.ones(N); rec_prev = [False]
        hs_rng = np.random.default_rng([int(seed), 1719])   # F9.15 home_sale, on its own stream
        d_arm = np.ones(N, bool)   # a fall under the need line borrows once; again after climbing back or a new blow
        db_rng = np.random.default_rng([int(seed), 82])     # the debts' and holdings' draws, on their own stream
        DB_D = -np.log(1 - 0.05) / 3                         # a bank's record: hiring odds x .95 for 7 years

        def db_log(n, **kw):
            if n in events:
                events[n].append(dict(deep_state=dict(kw, age=round(t / 52, 2))))

        def db_clear(n, i):
            dk[n, i] = -1; dsz[n, i] = dbal[n, i] = 0.0; dpaid[n, i] = 0; dterm[n, i] = 1.0; drate[n, i] = 0.0; dhold[n, i] = -1
            dstr[n, i] = False

        def db_add(n, kind, size, term, rate, hold=-1):
            i = int(np.argmax(dk[n] < 0))
            dk[n, i] = kind; dsz[n, i] = dbal[n, i] = size; dpaid[n, i] = 0; dterm[n, i] = term; drate[n, i] = rate
            dhold[n, i] = hold
            db_log(n, kind="debt taken", holder=D_KIND[kind], months=round(float(size), 2))

        def db_share(n):   # the part of income the payments take
            a_ = dk[n] >= 0
            return float((dsz[n] / dterm[n] + drate[n] * dbal[n] / 12)[a_].sum())

        def bank_ok(n):    # a bank lends: the world's epoch, the town's credit and the person's class, no record
            if not D_LEND[3] or (brec[n] > NEVER and t - brec[n] < 7 * YR_):
                return False
            cr_ = float(WL.W.sph_state("comm.credit")[WL.PP.loc[n]])
            return cr_ + DP_["bank_cls"] * (int(WL.PP.cls[n]) - 1) >= DP_["bank_line"]

        def db_break(n, i):   # a debt that cannot be paid breaks (deep_state.debts.broken), by holder
            k_ = int(dk[n, i]); h_ = int(dhold[n, i])
            if k_ == 1:
                WL.PP.kin_let_down(n, DP_["kin_trust"], t); kin_shut[n] = t + DP_["kin_wait"] * YR_
            elif k_ == 0:
                tab_shut[n] = t + DP_["tab_wait"] * YR_
            elif k_ == 2:
                circ_out[n] = True
            elif k_ in (3, 5):
                brec[n] = t
            elif k_ == 4:   # the debt is sold on and pressed: a threat, read by the town's order (never graphic)
                od_ = float(WL.W.sph_state("prot.order")[WL.PP.loc[n]])
                stress[n] += DP_["lender"][0] + DP_["lender"][1] * (1 - od_)
            db_log(n, kind="debt broken", holder=D_KIND[k_])
            db_clear(n, i)
            if h_ >= 0 and hk[n, h_] >= 0:   # the holding the loan bought goes with it
                db_log(n, kind="holding lost", holding=H_KIND[int(hk[n, h_])], why="debt")
                hk[n, h_] = -1

        def db_month():
            """Each month (adults): a hard year makes the nearest debt due, payments run down the balances, a debt that
            ends unpaid breaks, a life under the need line borrows; once a year, a holding may be bought."""
            m1_ = np.maximum(d_inc, 0.02) / 12               # a month's income on the money level
            car_ = held[:, CAR].copy(); hea_ = res[:, HEA].copy(); rec_ = getattr(WL.W, "phase", 0) == 1
            hard_ = ~dead & ((car_prev & ~car_ & (age < 60)) | (rec_ and not rec_prev[0])
                             | ((hea_ < DP_["ill_line"]) & (hea_prev >= DP_["ill_line"])))
            car_prev[:] = car_; hea_prev[:] = hea_; rec_prev[0] = rec_
            d_arm[:] |= (res[:, MON] >= NL_) | hard_
            for n in np.nonzero(hard_)[0]:
                if res[n, MON] < NL_ and (hk[n] >= 0).any():   # a sale in a hard year: a holding other than the home first
                    j_ = int(np.argmax(np.where(hk[n] >= 0, np.where(hk[n] == 0, 1, 2), 0)))
                    if hk[n, j_] == 0 and P["home_sale"] < 1.0 and hs_rng.random() >= P["home_sale"]:
                        j_ = -1                                 # F9.15: they get by without selling the home
                if res[n, MON] < NL_ and (hk[n] >= 0).any() and j_ >= 0:
                    res[n, MON] = min(1.0, res[n, MON] + DP_["sale"] * H_VAL[hk[n, j_]] * 12 * m1_[n])
                    for i_ in np.nonzero(dhold[n] == j_)[0]:
                        res[n, MON] = max(0.0, res[n, MON] - dbal[n, i_] * m1_[n]); db_clear(n, i_)
                    db_log(n, kind="holding lost", holding=H_KIND[int(hk[n, j_])], why="sold"); hk[n, j_] = -1
                rows_ = np.nonzero((dk[n] >= 0) & (dk[n] != 5))[0]   # the nearest due debt is due now (a home loan runs on)
                if len(rows_):
                    i_ = int(rows_[np.argmin((dterm[n] - dpaid[n])[rows_])])
                    if res[n, MON] < NL_:
                        db_break(n, i_)
                    else:
                        res[n, MON] -= dbal[n, i_] * m1_[n]; db_log(n, kind="debt paid early", holder=D_KIND[int(dk[n, i_])])
                        db_clear(n, i_)
            act_ = (dk >= 0) & ~dead[:, None]
            dpaid[act_] += 1; dbal[act_] = np.maximum(0.0, dbal[act_] - (dsz / dterm)[act_])
            for n, i_ in zip(*np.nonzero(act_ & (dpaid >= dterm))):
                if res[n, MON] >= 0.1:
                    db_clear(n, i_)
                elif dk[n, i_] == 1 and not dstr[n, i_]:   # kin: a partner or parent forgives it, else it is stretched once
                    al_ = WL.PP.alive[n]
                    if (al_[0] > 0 or al_[4] > 0) and db_rng.random() < DP_["kin_forgive"]:
                        db_log(n, kind="debt forgiven", holder="kin"); db_clear(n, i_)
                    else:
                        dstr[n, i_] = True; dpaid[n, i_] = 0; dsz[n, i_] = dbal[n, i_] = 0.5 * dsz[n, i_]
                        db_log(n, kind="debt stretched", holder="kin")
                else:
                    db_break(n, i_)
            for n in np.nonzero(~dead & d_arm & (res[:, MON] < NL_) & (dk < 0).any(1))[0]:   # borrowing, in the lending order
                gap_ = (NL_ - res[n, MON]) / m1_[n]
                run_ = set(int(x_) for x_ in dk[n] if x_ >= 0)
                al_ = WL.PP.alive[n]
                if gap_ < 0.5 and D_LEND[0] and tab_shut[n] <= t and 0 not in run_:
                    k_ = 0
                elif D_LEND[1] and kin_shut[n] <= t and 1 not in run_ and al_[0] + al_[1] > 0:
                    k_ = 1
                elif D_LEND[2] and not circ_out[n] and 2 not in run_:
                    k_ = 2
                elif 3 not in run_ and bank_ok(n):
                    k_ = 3
                elif D_LEND[4] and 4 not in run_:
                    k_ = 4
                else:
                    continue
                db_add(n, k_, D_SIZE[k_], D_TERM[k_], D_RATE[k_]); d_arm[n] = False
                res[n, MON] = min(1.0, res[n, MON] + D_SIZE[k_] * m1_[n])
            if t % YR_ == 0 and 25 <= age <= 65 and H_OK[0]:   # buying, a home first, then land, a shop or a firm, by the
                # lines on the life's own income (phase5c-answers.md): with a bank from sail on, from savings before
                u_ = db_rng.random(N)
                for n in np.nonzero(~dead & (hk < 0).any(1))[0]:
                    j_ = int(np.argmax(hk[n] < 0)); free_ = (dk[n] < 0).any(); mt_ = float(d_inc[n]); lv_ = float(res[n, MON])
                    home_ = not (hk[n] == 0).any()
                    if D_LEND[3]:   # banks lend in this epoch
                        a_, b_, p_ = DP_["buy_home"] if home_ else DP_["buy_more"]
                        if not (u_[n] < p_ and mt_ >= a_ and lv_ >= b_ * mt_ and free_ and bank_ok(n)):
                            continue
                        if home_:
                            k_ = 0; loan_ = max(0.0, H_VAL[0] * 12 - 0.1 / m1_[n]); term_, rate_, kd_ = D_TERM[5], D_RATE[5], 5
                        else:
                            ks_ = [x_ for x_ in (1, 2, 3) if H_OK[x_]]
                            k_ = ks_[int(db_rng.integers(len(ks_)))]
                            loan_ = (H_VAL[k_] - 1) * 12; term_, rate_, kd_ = LSF_TERM, D_RATE[3], 3   # above one year
                        if db_share(n) + loan_ / term_ + rate_ * loan_ / 12 > DP_["max_share"]:
                            continue
                        res[n, MON] = max(0.1, lv_ - (0.1 if home_ else 12 * m1_[n]))   # the deposit, or one year's income
                        hk[n, j_] = k_; db_add(n, kd_, loan_, term_, rate_, hold=j_)
                    else:           # before banks: from savings
                        a_, b_, p_ = DP_["buy_nb_home"] if home_ else DP_["buy_nb_more"]
                        if not (u_[n] < p_ and lv_ >= a_ and mt_ >= b_):
                            continue
                        ks_ = [0] if home_ else [x_ for x_ in (1, 2, 3) if H_OK[x_]]
                        k_ = ks_[int(db_rng.integers(len(ks_)))]
                        res[n, MON] = max(0.1, lv_ - 12 * m1_[n]); hk[n, j_] = k_
                    db_log(n, kind="holding gained", holding=H_KIND[k_], why="bought")
            # a land taking in the life's town (prod.land_taken) takes held land
            lg_ = getattr(WL.W, "sph_ev_log", None)
            if lg_ is not None and len(lg_) > ev_seen[0]:
                new_ = lg_[ev_seen[0]:]; ev_seen[0] = len(lg_)
                for _, e_, l_ in new_[new_[:, 1] == LT_I] if LT_I >= 0 else ():
                    for n in np.nonzero(~dead & (hk == 1).any(1) & ((WL.PP.loc == l_) | (l_ < 0)))[0]:
                        if db_rng.random() < DP_["land_taken"]:
                            j_ = int(np.argmax(hk[n] == 1)); hk[n, j_] = -1
                            for i_ in np.nonzero(dhold[n] == j_)[0]:
                                db_clear(n, i_)
                            db_log(n, kind="holding lost", holding=H_KIND[1], why="taken")
            if getattr(WL.PP, "care_buy", None) is not None:   # a carer with money buys help: care hours x .7
                WL.PP.care_buy[:] = res[:, MON] >= DP_["care_buy"][0]
            WL.PP.roots[:] = (hk >= 0).any(1)                # roots: the move wish x .5 while one is held

        def db_inherit(n):
            """The last living parent dies: what the family held passes by the epoch's rule (deep_state.holdings.
            inheritance), the life's share 1 / (1 + siblings), a daughter's share x rights['women']."""
            cl_ = int(WL.PP.cls_home[n]); nsib_ = int(WL.PP.older_sib[n] + WL.PP.younger_sib[n])
            eld_ = int(WL.PP.older_sib[n]) == 0
            sh_ = 1.0 / (1 + nsib_)
            if female[n]:
                sh_ *= float(np.asarray(WL.W.rights)[WK_RIGHTS_W])
            est_ = []
            if db_rng.random() < DP_["estate_home"][0] + DP_["estate_home"][1] * cl_:
                est_.append(0)
            if db_rng.random() < DP_["estate_more"][0] + DP_["estate_more"][1] * cl_:
                ks_ = [k_ for k_ in (1, 2, 3) if H_OK[k_] and (k_ < 3 or cl_ == 2)]
                est_.append(ks_[int(db_rng.integers(len(ks_)))])
            m_ = max(float(d_inc[n]), 0.02)
            for k_ in est_:
                s_ = sh_
                if (k_ == 1 and ER_ in ("realms", "sail")) or (k_ == 0 and ER_ == "cities"):   # to the eldest
                    s_ = (1.0 if eld_ else 0.0) * (float(np.asarray(WL.W.rights)[WK_RIGHTS_W]) if female[n] else 1.0)
                if s_ <= 0:
                    continue
                if s_ >= 0.5 and (hk[n] < 0).any() and not (hk[n] == k_).any():
                    hk[n, int(np.argmax(hk[n] < 0))] = k_
                    db_log(n, kind="holding gained", holding=H_KIND[k_], why="inherited")
                else:   # a share in money: s x value years of income
                    res[n, MON] = min(1.0, res[n, MON] + s_ * H_VAL[k_] * m_)
                    db_log(n, kind="inheritance", holding=H_KIND[k_], share=round(s_, 2))
        import world as WMOD_
        WK_RIGHTS_W = WMOD_.RIGHTS.index("women")
    DB_ON = SV_ON
    BA_ON = bool(P.get("birth_age")) and BAT   # late births: own births by real fertility for age and sex
    RP_ON = bool(P.get("role_practice"))        # what one holds is practice too
    HH_ON = bool(P.get("hh_money"))   # F3 D1, D2: a child's money is the household's until they live on their own
    TP_ON = bool(P.get("ties_people"))   # F3 D3: ties are the people around them
    if HH_ON or TP_ON:
        if WON:
            B_PAR_ = WLM.PM.BIT["parent"]
        HH_CLS_ = np.asarray(P["hh_cls"], float); HH_E_ = P["hh_earn"]; TW_ = np.asarray(P["tie_w"], float)
        MO_ = P["mort"]
        _H = lambda x_: MO_[0] / MO_[1] * (np.exp(MO_[1] * x_) - 1)   # (seed library: no one is counted, so kin by the life table)

        def home_share(age):
            """F3: the share of their money that is already their own (0 a child at home, 1 on their own), and whether they
            live on their own."""
            ramp_ = _uclip((age - P["hh_ages"][0]) / max(P["hh_ages"][1] - P["hh_ages"][0], 1e-9), 0, 1)
            if WON:
                away_ = np.asarray(WL.PP.own_home, bool).copy()
            else:   # world off: a partner or a child of their own, no parent left, or 30
                away_ = held[:, PAR] | held[:, KID] | (age >= 30) | ((alive[:, 0] <= 0) if BAT else False)
            return np.where(away_, 1.0, ramp_ * (1 - P["hh_work"] + P["hh_work"] * held[:, CAR])), away_

        def household(age):
            """F3 D1, D2: the household's money level (class x the parents' work) and the family's floor level (class x
            closeness to a living parent)."""
            if WON:
                PP_ = WL.PP
                par_ = PP_.used & PP_.lv & ((PP_.rmask & B_PAR_) != 0)
                hj_ = np.asarray(PP_.hhj)
                in_ = (((PP_.mset >> np.maximum(hj_, 0).astype(PP_.mset.dtype)[:, None]) & 1) > 0) & (hj_ >= 0)[:, None]
                ern_ = (par_ & PP_.emp & in_).sum(1) + 0.5 * (par_ & PP_.emp & ~in_).sum(1)
                lv_ = HH_CLS_[_uclip(np.asarray(PP_.cls), 0, 2)]
                pc_ = np.where(par_, PP_.c, 0.0).max(1)
            else:
                np_ = alive[:, 0] if BAT else 2 * np.exp(-(_H(age + 30) - _H(30.0)))
                ern_ = np.minimum(np_, 2); lv_ = hh_res0 / max(HH_E_[0] + 2 * HH_E_[1], 1e-9)
                pc_ = 0.8 * (np_ > 0.5)
            return lv_ * (HH_E_[0] + HH_E_[1] * np.minimum(ern_, 2)), lv_ * pc_

        def ties_off(age, away_):
            """F3 D3, world off: ties from who is alive and held (parents, siblings, the closest friend, grandparents, the
            partner, children, community, work, faith)."""
            if BAT:
                kin_ = np.stack([np.minimum(alive[:, 0], 2), np.minimum(alive[:, 1], 3), np.minimum(alive[:, 2], 1),
                                 np.minimum(alive[:, 3], 3), held[:, PAR], np.minimum(np.maximum(alive[:, 5], held[:, KID]), 3)], 1)
            else:
                pa_ = 2 * np.exp(-(_H(age + 30) - _H(30.0))); ga_ = 3 * np.exp(-(_H(age + 58) - _H(58.0)))
                kin_ = np.stack([np.full(N, pa_), np.full(N, 1.3), np.full(N, 1.0), np.full(N, ga_), held[:, PAR],
                                 held[:, KID] * 2.0], 1)
            kin_[:, 0] = kin_[:, 0] * np.where(away_, P["tie_away"], 1.0)
            s_ = kin_ @ TW_[:6] + held[:, [COM, CAR, FAI]] @ TW_[6:9]
            return 1 - np.exp(-s_ / P["tie_T"])
    OR_ON = bool(P.get("one_roll"))   # F7: one roll of the living (the children at home by the youngest)
    BORN_S_ = L["names"].index("a child is born") if OR_ON and BAT and "a child is born" in L["names"] else -1
    RE_ON = bool(P.get("retire_ends")) and BAT   # F8: retirement ends work
    if RE_ON:
        import world_keys as WKR_
        WAT_ = np.asarray(L.get("W_AT", np.full(L["S"], -1)))
        lf1_ = np.array([(s_.get("life") or "").split(",")[0].strip() == "work" for s_ in L.get("src", [{}] * L["S"])])
        door_ = (L["COMMIT"] == CAR).any(1)                   # a door back: an option that starts a career
        WORK_S = ((lf1_ | (WAT_ == WKR_.INST_KINDS.index("employer"))) & ~door_)   # the forced S3/S4/S7 moments too (F8 thread, 10-12)
    WO_ON = bool(P.get("world_only")) and BAT   # F10: a world moment only on the world's event
    if WO_ON:
        WMZ_ = np.zeros(L["S"], bool)
        if WON:
            WMZ_[np.asarray(WL.wm_s, int)] = True
            REG_ = REG_ & ~WMZ_; ROUT_ = ROUT_ & ~WMZ_
        tl_ = np.array([s_.get("tier") == "life event" for s_ in L.get("src", [{}] * L["S"])])
        WG_ = (PERY.sum(1) == 0) & tl_ & GAPM_ & ~WMZ_          # waits for the world, with a gap: (the T4 seasons)
        WG_I = np.nonzero(WG_)[0]; WGLO_ = np.nan_to_num(GAP_[WG_I, 0])[None]
        WGW_ = np.maximum(np.nan_to_num(GAP_[WG_I, 1] - GAP_[WG_I, 0]), 1 / 52)[None]
    AF_ON = bool(P["age_free"]) and BAT                   # F9: life events by age, not by the life stage reached
    if AF_ON:
        AF_S = np.array([nm_ in set(P["age_free"]) for nm_ in np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]])
        AF_P = PERY[AF_S].max(1)[None]
    if BA_ON:
        BIRTH_S = np.array([nm_ in BIRTH_OWN for nm_ in L["names"]])
        # the rate keeps its mean over the moment's own age window, so the births come when they do in real life
        ag_w = [np.arange(int(L["AGE"][s_, 0]), int(L["AGE"][s_, 1]) + 1) for s_ in np.nonzero(BIRTH_S)[0]]
        BA_NF = np.array([max(fert(a_, FERT_F).mean(), 1e-6) for a_ in ag_w])
        BA_NM = np.array([max(fert(a_, FERT_M).mean(), 1e-6) for a_ in ag_w])
        BF_ON = bool(P["birth_free"])
        BF_P = PERY[BIRTH_S].max(1)[None]   # birth_free: each own-birth moment at its highest stage rate
        # a choice that starts a child of one's own (not adopting, fostering or taking a child in)
        BIRTH_O = np.zeros(L["COMMIT"].shape, bool)
        for s_ in range(L["S"]):
            if L["TIER"][s_] != 1:
                for a_ in range(len(L["labels"][s_])):
                    BIRTH_O[s_, a_] = L["COMMIT"][s_, a_] == KID and not BIRTH_NOT.search(L["labels"][s_][a_])
        ba_rng = np.random.default_rng([int(seed), 83])
    # ---- v22.5 F1 and F2: the body, the mind and death from the life, each behind its switch. Off, nothing here draws
    # or changes anything and health runs as before. The weekly steps are body_week() (in 3b, where health drifted) and
    # death_week() (in 4e, where the life table was read)
    BODY_ON = bool(P["body"]); MIND_ON = bool(P["mind"]); DTH_ON = bool(P["death_life"]); HM_ON = BODY_ON or MIND_ON
    BP_ = {**BODY_PAR, **(P["body_par"] or {})}; MP_ = {**MIND_PAR, **(P["mind_par"] or {})}
    DP2_ = {**DEATH_PAR, **(P["death_par"] or {})}
    BAGE_X, BAGE_Y = (np.asarray(x_, float) for x_ in zip(*BP_["age"]))   # the body's level by age, alone
    body_v = res[:, HEA].copy(); mind_v = np.full(N, float(MP_["start"]))  # the two halves of health
    hea_w = res[:, HEA].copy()                               # health as body_week last wrote it (what changed it since is a shock)
    bd_base = body_v.copy()                                  # the body's slow level, moving over years
    bd_ill = np.zeros(N); bd_inj = np.zeros(N); bd_preg = np.zeros(N)   # dips that heal in weeks: illness, injury, a birth
    bd_cw = np.zeros((N, 3)); bd_ck = np.full((N, 3), -1); bd_ca = np.zeros((N, 3))   # up to three long-term conditions:
                                                             # weight, kind (COND_KINDS), age at onset
    bd_ser = np.zeros(N); bd_sk = np.full(N, -1); bd_s0 = np.full(N, NEVER); bd_s1 = np.full(N, NEVER)   # a serious illness:
                                                             # its dip, kind (SER_KINDS), first and last week
    bd_keep = np.zeros(N)                                    # what illness and injury took from the body for good
    bd_con = np.zeros(N); bd_strain = np.zeros(N); bd_money = res[:, MON].copy(); bd_carel = np.zeros(N)
    md_str = np.zeros(N); md_res = np.zeros(N)               # the mind: months of strain; resilience
    md_end = np.full((N, 3), NEVER)                          # the week each threat ends: a low season, anxiety, numbing
    dl_at = np.full(N, NEVER); dl_t0 = np.full(N, NEVER); dl_cause = [""] * N   # a last decline: its end and start, of what
    SER_CF = np.array([DP2_["ser_fatal"][k_] for k_ in SER_KINDS])   # each serious illness's share of courses that end in death
    CLETH_ = np.asarray(COND_LETHAL, float)
    HAB_ = np.add(np.add(BP_["rest"], BP_["move"]), BP_["moderate"]); BCARE_ = np.asarray(BP_["care"], float)
    BHEAL_ = np.asarray(BP_["heal"], float); BRISK_ = np.asarray(BP_["risk"], float)
    LK_B = ("condition", "serious", "accident or illness", "injury", "burnout"); LK_M = ("low", "anx", "numb")
    BL_K = np.array([LK_B.index(BODY_MOMENTS[L["names"][r_]]) if L["names"][r_] in BODY_MOMENTS else -1 for r_ in ROOT])
    ML_K = np.array([LK_M.index(MIND_MOMENTS[L["names"][r_]]) if L["names"][r_] in MIND_MOMENTS else -1 for r_ in ROOT])
    BL_ON = BODY_ON and bool(BP_["moments"]) and bool((BL_K >= 0).any())   # the Library's own body moments happen to the body
    ML_ON = MIND_ON and bool(MP_["moments"]) and bool((ML_K >= 0).any())
    BL_COND = BL_ON and bool((BL_K == 0).any()); BL_SER = BL_ON and bool(np.isin(BL_K, (1, 2)).any())   # else the engine's rates
    ML_HAS = [ML_ON and bool((ML_K == k_).any()) for k_ in range(3)]
    BL_S = np.nonzero(BL_K >= 0)[0]; ML_S = np.nonzero(ML_K >= 0)[0]
    if HM_ON:   # the outputs carry the two halves (V_hist body and mind) only with a switch on
        V_hist["body"] = []; V_hist["mind"] = []
    PREG_O = np.zeros(L["COMMIT"].shape, bool)               # a choice that begins a child of one's own (H7)
    for s_ in np.nonzero([nm_ in BIRTH_OWN for nm_ in L["names"]])[0] if BODY_ON else ():
        for a_ in range(len(L["labels"][s_])):
            PREG_O[s_, a_] = L["COMMIT"][s_, a_] == KID and not BIRTH_NOT.search(L["labels"][s_][a_])
    PG_ON = bool(PREG_O.any())
    if BODY_ON:   # H1 and an early condition: drawn from their own stream, so no other draw moves
        crng_ = np.random.default_rng([int(seed), 5101])
        bd_con = crng_.normal(0, BP_["con_sd"], N) - (crng_.random(N) < BP_["con_frail"][0]) * BP_["con_frail"][1]
        cy_ = crng_.random(N) < BP_["cond_young"]; cs_ = crng_.uniform(*BP_["cond_size"], N); ck_ = crng_.choice(len(COND_KINDS), N, p=COND_P[0])
        bd_cw[cy_, 0] = cs_[cy_]; bd_ck[cy_, 0] = ck_[cy_]; bd_ca[cy_, 0] = crng_.uniform(0, 6, N)[cy_]

    def body_log(n_, **rec):   # a logged life's body and mind record (the game tells what it wants of it)
        if n_ in events:
            events[n_].append(dict(body=dict(age=round(t / 52, 2), **rec)))

    def bd_condition(n_, kind=None):   # a long-term condition begins (H3), at most three
        j_ = int(np.argmin(bd_cw[n_]))
        if bd_cw[n_, j_] > 0:
            return
        k_ = kind if kind is not None else int(rng.choice(len(COND_KINDS), p=COND_P[0 if age < 16 else 1]))
        if P["cond_once"] and (bd_ck[n_] == k_).any():   # F9.27 (F10): one they have already is not diagnosed again
            return
        bd_cw[n_, j_] = rng.uniform(*BP_["cond_size"]) * (1 - 0.3 * float(np.clip(lean_c[n_], -1, 1)))
        bd_ck[n_, j_] = k_; bd_ca[n_, j_] = age
        body_log(n_, kind="condition", name=COND_KINDS[k_], what="begins")

    def bd_serious(n_, kind):   # a serious illness begins (H6): a dip for months; early care finds it sooner
        if bd_sk[n_] >= 0 or dead[n_]:
            return
        bd_sk[n_] = kind; bd_s0[n_] = t
        bd_s1[n_] = t + int(4.33 * rng.uniform(*BP_["ser_months"]))
        bd_ser[n_] = rng.uniform(*BP_["ser_size"]) * (1 - 0.3 * float(np.clip(lean_c[n_], -1, 1)))
        body_log(n_, kind="serious", name=SER_KINDS[kind], what="begins")

    def bd_injury(n_, lo, hi, told=True):   # an injury: a dip that heals in weeks, now and then with a lasting mark (H5);
        bd_inj[n_] += rng.uniform(lo, hi)        # told=False when a Library moment already tells it
        if rng.random() < BP_["inj_keep"][0]:
            bd_keep[n_] += BP_["inj_keep"][1]
        if told:
            body_log(n_, kind="injury", what="hurt")

    def md_threat(n_, k_, told=True):   # a low season, anxiety or numbing begins (or goes on), shorter with resilience
        mo_ = MP_[("low_months", "anx_months", "numb_months")[k_]]
        end_ = t + int(4.33 * rng.uniform(*mo_) * (1 - 0.5 * md_res[n_]))
        if end_ > md_end[n_, k_]:
            if md_end[n_, k_] <= t and told:
                body_log(n_, kind=("low season", "anxiety", "numbing")[k_], what="begins")
            md_end[n_, k_] = end_

    lean_c = np.zeros(N)   # this week's early-care lean (H11), read by the helpers above

    def body_week(ht, ht0):
        """F1 in 3b, once a week from age 3: what changed health since last week reaches the body as a shock (a fall is an
        injury-like dip, a lift heals dips first), the body's and the mind's own events, each half moves, and health is
        written as their mean. ht is the old rule's level for the age with its work and title parts, ht0 its age part."""
        nonlocal lean_c
        al_ = ~dead; ext_ = res[:, HEA] - hea_w
        dec_ = np.where(dl_at > NEVER // 2, _uclip((t - dl_t0) / np.maximum(dl_at - dl_t0, 1), 0, 1), 0.0)   # F2: the decline
        lean_ = (w - 0.2) / 0.2                                  # each colour's share above or below even, per .2
        lean_c = lean_ @ BCARE_
        tab_ = np.interp(age, BAGE_X, BAGE_Y)
        low_ = md_end[:, 0] > t; anx_ = md_end[:, 1] > t; numb_ = md_end[:, 2] > t
        if BODY_ON:
            neg_ = np.maximum(-ext_, 0); pos_ = np.maximum(ext_, 0)
            bd_inj[:] += neg_
            h_ = np.minimum(pos_, bd_inj); bd_inj[:] -= h_; pos_ = pos_ - h_
            h_ = np.minimum(pos_, bd_ill); bd_ill[:] -= h_; bd_base[:] += pos_ - h_
            # the slow level: age, constitution, habits, strain, people, money, care, the mind, the work and titles (ht)
            bd_strain[:] += (stress - bd_strain) / (52 * BP_["strain_years"])
            bd_money[:] += (res[:, MON] - bd_money) / (52 * BP_["money_years"])
            mm_ = bd_money
            if WON:   # a child's money is the family's: its class
                mm_ = np.where(stage <= 1, np.array([0.08, 0.25, 0.5])[np.clip(np.asarray(WL.PP.cls), 0, 2)], bd_money)
            mods_ = (bd_con + lean_ @ HAB_ + BP_["disc"] * (dsc - 1) - 0.03 * numb_ - bd_keep + (ht - ht0)
                     - BP_["strain"] * _uclip((bd_strain - BP_["strain_from"]) / 1.0, 0, 1)
                     - BP_["lonely"] * _uclip((BP_["lonely_line"] - need[:, NIDX["belonging"]]) / 0.4, 0, 1)
                     + BP_["money"] * _uclip((mm_ - 0.2) / 0.2, -1, 1))
            if WON and getattr(WL.PP, "care_load", None) is not None:   # H16
                bd_carel[:] += (np.asarray(WL.PP.care_load, float) - bd_carel) / 104
                mods_ = mods_ - BP_["care_load"] * _uclip(bd_carel / 20, 0, 1)
            if MIND_ON:
                mods_ = mods_ - BP_["mind_wear"] * _uclip((0.6 - mind_v) / 0.4, 0, 1)
            tgt_ = toward(tab_, mods_)                            # around the age's level, never past 1
            bd_base[:] += (tgt_ - bd_base) * (1 - 0.5 ** (1 / (52 * BP_["base_half"])))
            # the dips heal: faster with early care and Green's and Red's ways, slower when poor or old
            slow_ = (1 + 0.3 * _uclip((0.15 - mm_) / 0.15, 0, 1)) * (1 + max(0.0, age - 60) / 40) \
                * (1 - 0.3 * _uclip(lean_c, -1, 1)) * (1 - 0.3 * _uclip(lean_ @ BHEAL_, -1, 1))
            bd_ill[:] *= 0.5 ** (1 / (BP_["ill_half"] * slow_)); bd_inj[:] *= 0.5 ** (1 / (BP_["inj_half"] * slow_))
            bd_preg[:] *= 0.5 ** (1 / BP_["preg_half"])
            # the body's own events this week: a short illness, an injury; a condition or a serious illness where the
            # Library has no moment for them; a young condition that eases; a serious illness that ends
            u_ = rng.random((N, 6))
            pi_ = np.interp(age, *zip(*BP_["ill_rate"])) * (1 + BP_["ill_mind"] * (low_ | anx_)) / 52
            ii_ = np.nonzero(al_ & (u_[:, 0] < pi_))[0]
            bd_ill[ii_] += BP_["ill_size"][0] + (BP_["ill_size"][1] - BP_["ill_size"][0]) * u_[ii_, 5]
            pj_ = np.interp(age, *zip(*BP_["inj_rate"])) * np.exp(lean_ @ BRISK_) / 52
            for n_ in np.nonzero(al_ & (u_[:, 1] < pj_))[0]:
                bd_injury(n_, *BP_["inj_size"])
            rk_ = np.minimum(np.exp(BP_["risk_k"] * (tab_ - body_v)), 2.0)
            if not BL_COND:
                for n_ in np.nonzero(al_ & (u_[:, 2] < np.interp(age, *zip(*BP_["cond_rate"])) * rk_ / 52))[0]:
                    bd_condition(n_)
            if not BL_SER:
                for n_ in np.nonzero(al_ & (u_[:, 3] < np.interp(age, *zip(*BP_["ser_rate"])) * rk_ / 52))[0]:
                    bd_serious(n_, int(rng.choice(len(SER_KINDS), p=(0.45, 0.3, 0.15, 0.1))))
            if age < 18:   # H3: a young person's condition may ease
                for n_ in np.nonzero(al_ & (u_[:, 4] < BP_["cond_ease"] / 52) & (bd_cw[:, 0] > 0) & (bd_ca[:, 0] < 16))[0]:
                    body_log(n_, kind="condition", name=COND_KINDS[bd_ck[n_, 0]], what="eases")
                    bd_cw[n_, 0] = 0.0; bd_ck[n_, 0] = -1
            for n_ in np.nonzero((bd_sk >= 0) & (t >= bd_s1) & al_ & (dl_at <= NEVER // 2))[0]:   # through it: some stays
                bd_keep[n_] += rng.uniform(*BP_["ser_keep"]); body_log(n_, kind="serious", name=SER_KINDS[bd_sk[n_]], what="through it")
                bd_sk[n_] = -1; bd_ser[n_] = 0.0; bd_s0[n_] = bd_s1[n_] = NEVER
            if BL_ON or PG_ON:   # the Library's own body moments this week, and a birth of their own (H7)
                lk_ = np.where(~recon & al_, BL_K[s], -1)
                for n_ in np.nonzero(lk_ >= 0)[0]:
                    k_ = int(lk_[n_]); nm_ = L["names"][ROOT[s[n_]]]
                    if k_ == 0:
                        bd_condition(n_, COND_KINDS.index("arthritis") if "wild years" in nm_ else None)
                    elif k_ == 1:   # a diagnosis: most often cancer, else the heart or the lungs
                        bd_serious(n_, int(rng.choice(len(SER_KINDS), p=(0.6, 0.25, 0.0, 0.15))))
                    elif k_ == 2 and rng.random() < np.clip((age - 30) / 50, 0.05, 0.5):   # an illness more often with age
                        bd_serious(n_, 1 if rng.random() < 0.6 else 2)
                    elif k_ == 2:
                        bd_injury(n_, 0.3, 0.45, False)
                    elif k_ == 3:
                        bd_injury(n_, 0.12, 0.3, False)
                    else:   # burnout: the body runs down for weeks
                        bd_ill[n_] += 0.1
                pg_ = PREG_O[s, a] & succ & ~idle & female & ~recon & al_
                bd_preg[pg_] += BP_["preg"]
            body_v[:] = _uclip(bd_base - np.minimum(bd_cw.sum(1), BP_["cond_max"]) - bd_ser - bd_ill - bd_inj - bd_preg, 0.01, 0.99) \
                * (1 - 0.85 * dec_)
        else:   # health as before, as the body half
            body_v[:] = _uclip(body_v + ext_, 0, 1); body_v[:] += 0.01 * (ht - body_v)
        if MIND_ON:
            md_str[:] += (stress - md_str) / 13                    # the last three months' strain
            bel_ = need[:, NIDX["belonging"]]
            mods_ = (MP_["mood"] * (base_mood - MP_["mood_ref"]) + MP_["content"] * (content - MP_["content_ref"])
                     + np.where(stage == 0, 0.06, np.where(stage == 1, 0.03, 0.0))   # the family holds a child's mind up
                     - MP_["strain"] * _uclip(md_str - MP_["strain_from"], 0, 1) - MP_["loss"] * np.minimum(wound, 1.5)
                     - MP_["scar"] * np.minimum(scar.sum(1), 3.0) - MP_["lonely"] * _uclip((MP_["lonely_line"] - bel_) / 0.4, 0, 1)
                     + _uclip(MP_["meaning"] * (need[:, NIDX["meaning"]] - 0.9), -0.06, 0.06)
                     - MP_["rest"] * _uclip((0.15 - res[:, TIM]) / 0.1, 0, 1) - MP_["body"] * np.maximum(0.7 - body_v, 0)
                     - MP_["low_dip"] * low_ - MP_["anx_dip"] * anx_ - MP_["numb_dip"] * numb_ - 0.3 * dec_)
            tgt_ = toward(np.full(N, float(MP_["level"])), mods_)
            mind_v[:] += (tgt_ - mind_v) * (1 - 0.5 ** (1 / MP_["half"]))
            own_ = (5 * (ma * hold).sum(1) - 1 > 0) & succ & ~idle & ~recon   # steadier picks: an act that works and fits them
            mind_v[:] = _uclip(mind_v + MP_["steady"] * own_, 0.01, 0.99)
            # the threats: the Library's moments start a low season or numbing; anxiety (and the others, where a Library
            # has no moment for them) by the engine's rate, likelier as the mind falls, less likely with resilience
            if ML_ON:
                lk_ = np.where(~recon & al_, ML_K[s], -1)
                for n_ in np.nonzero(lk_ >= 0)[0]:
                    md_threat(n_, int(lk_[n_]), False)
            rk_ = np.minimum(np.exp(MP_["risk_k"] * (0.75 - mind_v)), 3.0) * (1 - md_res) * (age >= 8)
            u_ = rng.random((N, 3))
            for k_, rt_ in enumerate((MP_["low_rate"], MP_["anx_rate"], MP_["numb_rate"] * (age >= 14))):
                if not ML_HAS[k_]:
                    for n_ in np.nonzero(al_ & (u_[:, k_] < rt_ * rk_ / 52))[0]:
                        md_threat(n_, k_)
            # what a threat does while it lasts: a low season lowers the mood, anxiety strains, numbing eases the strain a
            # little now and wears self-control
            mood[low_] -= 0.01; stress[anx_] += 0.02; stress[numb_] = np.maximum(stress[numb_] - 0.01, 0); dsc[numb_] *= 0.998
            ov_ = (md_end > NEVER // 2) & (md_end <= t) & al_[:, None]   # a threat over: with people around, resilience grows
            for n_, k_ in zip(*np.nonzero(ov_)):
                if bel_[n_] >= 0.6:
                    md_res[n_] = min(MP_["resil_max"], md_res[n_] + MP_["resil"])
                body_log(n_, kind=("low season", "anxiety", "numbing")[k_], what="lifts")
                md_end[n_, k_] = NEVER
            hea_ = (1 - MP_["mind_w"]) * body_v + MP_["mind_w"] * mind_v
        else:
            hea_ = body_v
        res[:, HEA] = hea_; hea_w[:] = hea_

    def death_week():
        """F2 in 4e, once a week while self_death is on: a decline that has run its course ends the life; otherwise each
        cause's risk this week from the body and what they have, and a death drawn is sudden (an accident, a heart attack
        or a stroke) or comes after a last decline the story can tell."""
        for n_ in np.nonzero((dl_at > NEVER // 2) & (t >= dl_at) & ~dead)[0]:
            die(n_, dl_cause[n_])
        al_ = ~dead & (dl_at <= NEVER // 2)
        if BODY_ON:   # the body without a serious illness's own dip (its course has its own risk) or a birth's
            bod_ = _uclip(bd_base - np.minimum(bd_cw.sum(1), BP_["cond_max"]) - bd_ill - bd_inj, 0.01, 0.99)
        else:
            bod_ = body_v if HM_ON else res[:, HEA]
        gap_ = np.interp(age, BAGE_X, BAGE_Y) - bod_
        qa_ = np.interp(age, *zip(*DP2_["acc"])) * np.exp(DP2_["acc_red"] * (w[:, 3] - 0.2) / 0.2)
        qf_ = (DP2_["frail"][0] * np.exp(DP2_["frail"][1] * age) + (DP2_["frail_c"] if age >= 15 else 0.0)) * np.exp(DP2_["frail_k"] * gap_)
        cl_ = bd_cw * np.where(bd_ck >= 0, CLETH_[np.maximum(bd_ck, 0)], 0.0)   # each condition's complications
        qc_ = DP2_["cond_k"] * cl_.sum(1) * np.exp(0.06 * (age - 50))
        cf_ = np.minimum(SER_CF[np.maximum(bd_sk, 0)] * float(np.clip(1 + DP2_["ser_age"] * (age - 60), *DP2_["ser_age_lim"]))
                         * np.exp(DP2_["frail_k"] * gap_ / 2), 0.95)
        wk_ = np.maximum(bd_s1 - bd_s0, 1)
        qs_ = np.where(bd_sk >= 0, 1 - (1 - cf_) ** (1 / wk_), 0.0)   # spread over the illness's weeks
        q_ = np.stack([qa_ / 52, qf_ / 52, qc_ / 52, qs_], 1)
        tot_ = 1 - np.prod(1 - np.minimum(q_, 1), 1)
        u_ = rng.random((N, 3))
        for n_ in np.nonzero(al_ & (u_[:, 0] < tot_))[0]:
            c_ = int(np.searchsorted(np.cumsum(q_[n_]) / q_[n_].sum(), u_[n_, 1]))
            if c_ == 0:
                die(n_, "in an accident"); continue
            if c_ == 1 and age < DP2_["old_age"] and u_[n_, 2] < DP2_["sudden"]:   # a failing body, at once
                die(n_, "of a sudden heart attack" if u_[n_, 2] < 0.7 * DP2_["sudden"] else "of a stroke"); continue
            if c_ == 3:
                why_, kd_ = {0: "of cancer", 1: "of heart disease", 2: "after a stroke", 3: "of lung disease"}[int(bd_sk[n_])], "serious"
            elif c_ == 1 and age >= DP2_["old_age"]:
                why_, kd_ = "old age", "old"
            elif c_ == 1 and not (cl_[n_] > 0).any():   # a failing body with nothing named: the heart, over weeks
                why_, kd_ = "of heart failure", "condition"
            else:   # a condition's complications (the one that weighs most): an asthma attack or a seizure is sudden
                k_ = int(bd_ck[n_, int(np.argmax(cl_[n_]))])
                if COND_KINDS[k_] in ("asthma", "epilepsy"):
                    die(n_, COND_DEATH[k_]); continue
                why_, kd_ = COND_DEATH[k_], "condition"
            dl_t0[n_] = t; dl_at[n_] = t + int(rng.uniform(*DP2_["decline"][kd_])); dl_cause[n_] = why_
            hz_mem[n_] += P["hz_remind"]
            if n_ in events:
                events[n_].append(dict(decline=dict(age=round(t / 52, 2), cause=why_, weeks=int(dl_at[n_] - t))))

    # v22.5, the many-lives fixes (each off unless its switch is set; none draws from the run's own random stream)
    SET_ON = P["set_age"] is not None                     # F14: colours settle with age
    settle_f = np.ones(N)                                 # this week's factor on plasticity (the game's V2 can read it)
    if SET_ON:
        SET_A, SET_F = np.asarray(P["set_age"], float).T
        set_bu = np.zeros(N)                              # the person's usual openness
    UPM_ = None if P["up_mix"] is None else np.asarray(P["up_mix"], float) / np.sum(P["up_mix"])   # F15: the start's lean
    UPL_ON = UPM_ is not None and bool(P["up_lean"] or P["up_self"] or P["up_ease"])
    if UPL_ON:
        UPD_ = UPM_ - 0.2; UPN_ = max(float(UPD_ @ UPD_), 1e-9)
        up_oy = np.zeros((N, C)); up_oz = np.zeros((N, C))   # what the start's pulls have added to the want and to who they are
        UP_DEC = 1 - 0.5 ** (1 / (52 * P["up_half"]))         # which fades by half every up_half years from up_from
        def up_short(v):
            """F15: how far a pie (N x C) falls short of the lean the start still leaves, 0 to 1 of the full lean."""
            return _uclip((P["up_l0"] * upf_ - (v - 0.2) @ UPD_ / UPN_) / P["up_l0"], 0, 1)
    DS_ON = bool(P["drv_self"]) and "DRVN" in L          # F9: the drivers' mean taken out in the run itself
    DRVN_ = np.asarray(L["DRVN"], float) if DS_ON else None
    PS_ON = P["par_split"] is not None                    # F9: a breakup and a home together
    if PS_ON:
        PS_SOFT = np.isin(np.asarray(ROOT), [i_ for i_, nm_ in enumerate(L["names"]) if nm_ in SPLIT_SOFT])
        ps_rng = np.random.default_rng([int(seed), 1709])
    PA_ON = P["par_age"] is not None                      # F9: partnerships by age
    if PA_ON:
        PA_A, PA_F = np.asarray(P["par_age"], float).T
    JM_ON = P["job_move"] is not None                     # F9.19: changing employer
    if JM_ON:
        JM_A, JM_F = np.asarray(P["job_move"], float).T
        jm_rng = np.random.default_rng([int(seed), 1713])
    LON_ON = P["lone"] is not None                        # F9.39: a spell of loneliness
    if LON_ON:
        LO_ = dict(P["lone"]); LA_, LF_ = np.asarray(LO_["age"], float).T
        lon_rng = np.random.default_rng([int(seed), 1721]); lone = np.zeros(N, bool)
    LP_ON = P["low_pay"] is not None                      # F9.38: each job's pay
    if LP_ON:
        lp_sd, lp_rho, lp_half = (float(x_) for x_ in P["low_pay"])
        lp_rng = np.random.default_rng([int(seed), 1723]); lp_z = np.zeros(N); lp_d = np.ones(N); lp_at = np.full(N, NEVER)
        lp_mu = np.zeros(N); lp_sc = np.ones(N)
        PC_ = None if P["pay_col"] is None else np.asarray(P["pay_col"], float)
    TC_ = None if P["tie_col"] is None else np.asarray(P["tie_col"], float)
    PRP_ON = P["pair_pay"] is not None                    # F9.38: a couple living together shares its money
    if PRP_ON:
        CO_T_ = np.array([i_ for i_, x_ in enumerate(GR["names"]) if x_ in CO_TITLES], int) if RON else np.zeros(0, int)
    CRS_ON = bool(P["course"])                            # F16: the life course leans
    if CRS_ON:
        CRS_KS = np.array([PAR, KID, FAI]); CRS_MU = np.asarray(P["course_mu"], float)
        CRS_T = np.asarray(P["course_tilt"], float)
        crs_rng = np.random.default_rng([int(seed), 1605])
        crs_own = crs_rng.normal(0.0, P["course_sd"], (N, 3))   # each life's own lean
        # the life events that start one (falling in love, a baby on the way): most of their options start that kind
        sh_ = np.stack([((L["COMMIT"] == k_) & L["MASK"]).sum(1) for k_ in CRS_KS], 1) / np.maximum(L["MASK"].sum(1), 1)[:, None]
        ev_ok_ = (L["PERY"].sum(1) > 0)[:, None] & (sh_ >= 0.4)
        CRS_EV = np.where(ev_ok_.any(1), ev_ok_.argmax(1), -1)   # which of the three each situation starts (-1: none)
        CRS_J = np.full(NK, -1); CRS_J[CRS_KS] = np.arange(3)
        def course_q():
            """F16: each life's rate multiplier for starting a partnership, a child, a faith (N x 3)."""
            return np.exp(CRS_MU[None] + crs_own + (5 * w - 1) @ CRS_T.T)
    DC_ON = bool(P["deed_canon"])                         # F17: deeds by canon
    if DC_ON:
        DC_M = np.zeros((len(L["MARKS"]), C))
        for nm_, v_ in DEED_CANON.items():
            if nm_ in L["MARKS"]:
                DC_M[L["MARKS"].index(nm_)] = v_
        DC_L = np.where((L["MARK"] >= 0)[..., None], DC_M[np.maximum(L["MARK"], 0)], 0.0)   # S x K x C: each option's lean
    DR_ON = bool(P["deed_rare"])
    if DR_ON:
        DR_M = np.isin(np.arange(len(L["MARKS"])), [L["MARKS"].index(m_) for m_ in DEED_RARE if m_ in L["MARKS"]])
        dr_rng = np.random.default_rng([int(seed), 1705])
    if P["mind_kid"] is not None:                         # F19
        MK_A, MK_F = np.asarray(P["mind_kid"], float).T
    if P["mind_u"] is not None:
        MU_A, MU_F = np.asarray(P["mind_u"], float).T
    # the world's effects on each life, for the game's story (stage 1: WL1, WL3, WL5): only in a game run (pausing) with
    # the world on, and read only, so every life is the same with them or without
    WFX_ON = bool(pausing and WON)
    wfx = [[] for _ in range(N)]                         # this week's world effects on each life (wfx_add)
    wfx_last = {}                                         # (channel, kind) -> the value last reported, per life (N,)
    wco_ = {}                                             # this week's option closures by cause (option_causes)

    def wfx_add(n, kind, channel, size, age_, cause=None, **more):
        """An effect of the world on life n: kind (the world's cause: prices, housing, welfare, rights, crime, war,
        disaster, unemployment, illness, pandemic, or a world event's kind), channel (what of theirs it touched),
        size (signed, in the channel's units), dir (up or down), cause (the world's record entry behind it, for the
        hover; None when the record has none), age; more keys as given (moment, share, hazard)."""
        e_ = dict(kind=kind, channel=channel, size=round(float(size), 4), dir="up" if size > 0 else "down",
                  cause=cause if cause is not None else WL.cause(kind), age=round(float(age_), 2))
        e_.update(more)
        wfx[n].append(e_)

    def wfx_track(channel, parts, age_, dead_):
        """Report each part (kind -> (N,)) that moved by wfx_step or more since it was last reported; the first
        reading only sets where it starts."""
        for kd_, v_ in parts.items():
            v_ = np.broadcast_to(np.asarray(v_, float), (N,))
            old_ = wfx_last.get((channel, kd_))
            if old_ is None:
                wfx_last[(channel, kd_)] = v_.copy()
                continue
            mv_ = np.nonzero(np.abs(v_ - old_) >= P["wfx_step"])[0]
            for n_ in mv_:
                if not dead_[n_]:
                    wfx_add(n_, kd_, channel, v_[n_] - old_[n_], age_)
            old_[mv_] = v_[mv_]

    def option_causes(n):
        """The world's causes behind each option of life n's moment this week (WL3), one list per option, each cause a
        dict: kind (law, norm, role, technology, unemployment, university places, hospital places), key (the law,
        norm or technology), channel "option", size (law: 1 banned, .5 restricted, -1 allowed where written closed;
        norm, role, technology: closure units; unemployment and places: difficulty added, - easier), how, cause (the
        world's record entry, as in wfx). Empty without the world or before the first moment."""
        if not wco_:
            return []
        s_ = int(wco_["s"][n]); K_ = len(L["labels"][s_]); out = [[] for _ in range(K_)]
        WK_ = WLM.WK; lw_, nm_, te_ = WL.law[s_], WL.norm[s_], WL.tech[s_]
        def add(k_, kind, key, size, how):
            out[k_].append(dict(kind=kind, key=key, channel="option", size=round(float(size), 4), how=how,
                                cause=WL.cause(kind, key=key if kind in ("law", "technology") else None)))
        od_ = WL.odds_parts(wco_["s"])
        for k_ in range(K_):
            if k_ < lw_.shape[0] and lw_[k_] >= 0:
                u_ = float(wco_["ul"][n, k_])
                if u_ > 0:
                    add(k_, "law", WK_.LAW_KEYS_ALL[lw_[k_]], u_, "banned" if u_ >= 1 else "restricted")
                elif wco_["lo"][n, k_] and wco_["closed0"][n, k_] == 0:
                    add(k_, "law", WK_.LAW_KEYS_ALL[lw_[k_]], -1.0, "allowed")
            if k_ < nm_.shape[0] and nm_[k_] >= 0 and wco_["ua"][n, k_] >= WFX_OPT[0]:
                add(k_, "norm", WK_.NORM_KEYS_ALL[nm_[k_]], wco_["ua"][n, k_], "frowned on")
            if wco_.get("role") is not None and wco_["role"][n, k_] >= WFX_OPT[0]:
                add(k_, "role", "role crossing", wco_["role"][n, k_], "frowned on")
            if k_ < te_.shape[0] and te_[k_] >= 0:
                if wco_["gone"][n, k_]:
                    add(k_, "technology", WK_.TECH_KEYS[te_[k_]], 1.0, "not there")
                elif wco_["um"][n, k_] >= WFX_OPT[0]:
                    add(k_, "technology", WK_.TECH_KEYS[te_[k_]], wco_["um"][n, k_], "out of reach")
            for kd_, v_ in od_.items():
                v_ = np.broadcast_to(v_, (N, WL.job_o.shape[1]))   # a moment-wide part (an illness's) is (N, 1)
                if abs(v_[n, k_]) >= WFX_OPT[1]:
                    add(k_, kd_, None, v_[n, k_], "harder" if v_[n, k_] > 0 else "easier")
        return out
    for t in range(T):
        age = t / 52.0
        z = bound_logratios(z, P["min_color"], P["max_color"]); y = bound_logratios(y, P["min_color"], P["max_color"])
        if t % 13 == 0:   # the colours each quarter (conditions: rise, above_yrs, pair_yrs)
            w_q[w_qi % 40] = softmax(z); w_qi += 1
        if age > 12 and t % 52 == 0:                                   # nobody stays perfectly unbiased
            w0_ = softmax(z); flat = (w0_.max(1) - w0_.min(1)) < P["min_spread"]
            if flat.any():
                z[flat, w0_[flat].argmax(1)] += 0.1; z[flat] = centre(z[flat])
        nk_ = held[:, KID] & ~kid_on                                  # R15: the first child, however the children came
        alive[nk_, 5] = np.maximum(alive[nk_, 5], 1); kid_last[nk_] = t; kid_on = held[:, KID].copy()
        kids = held[:, KID] & (t - (kid_last if OR_ON else since[:, KID]) < 20 * 52) & ((alive[:, 5] > 0) | (not BAT))   # children
        # still at home (F7, one_roll: until the youngest is grown; before, the first)
        load = held * LOAD
        load[:, KID] = np.where(kids, LOAD[KID], 0.05 * held[:, KID])
        res[:, TIM] = _uclip(1 - load.sum(1) - 0.3 * (stage == 0), 0.05, 1)
        if RON:   # a title's own hours (a nurse's shifts, a councillor's evenings)
            res[:, TIM] = _uclip(res[:, TIM] + r_has[:, :NT_] @ GR["meets_res"][:, TIM], 0.05, 1)
        if WON and age >= 3:   # the world: the hours of one's own groups that no commitment counts (clubs, a movement)
            res[:, TIM] = _uclip(res[:, TIM] + WL.group_time(held, COM, FAI), 0.05, 1)
        if RON and MIS_ON and t % 52 == 0:   # v10: status held (summits, standings: hubris) and expertise by color (skills, careers)
            hub_ = r_has[:, :NT_][:, TIER_[:NT_] == 2].sum(1) + 0.5 * r_has[:, NT_:][:, PKIND_ == 2].sum(1)
            xp_ = (p_lev * (PKIND_ == 0)) @ WAYS_[NT_:] + np.minimum((t - r_since[:, :NT_]) / 520, 1) * r_has[:, :NT_] @ (WAYS_[:NT_] * CAREER_[:, None])
        w = softmax(z)
        if WON:   # the world's week first: its society, the cast, settings and place of each life (they read last week's person)
            if RON:   # the sector of the career held (sector= on careers) and the standing its titles give (standing=)
                sec_w = np.where(r_has[:, :NT_] & (W_SEC_ >= 0), W_SEC_, -1).max(1)
                st_w = np.where(r_has[:, :NT_] & (W_STD_ >= 0), W_STD_, 0).max(1)
            if RON and len(W_SDI_):   # each domain's standing from the titles held (one level 0-3 per domain)
                st_t_ = r_has[:, W_SDI_] * W_STD_[W_SDI_]
                dst_w = np.stack([np.where(W_SDOM_ == d_, st_t_, 0).max(1) for d_ in range(len(WLM.WK.DOMAINS))], 1)
            WL.week(t, dict(w=w, held=held, res=res, stress=stress, outlook=outlook, attr=attr, dead=dead, lens=softmax(k),
                            partner_same=partner_same if ID2 else None, sector=sec_w if RON else None,
                            title_standing=st_w if RON else None, children=alive[:, 5].copy(),   # the cast keeps every child
                            domain_standing=dst_w if RON and len(W_SDI_) else None,
                            gov_office=r_has[:, W_GOV_].any(1) if RON and W_GOV_ else None,
                            head_gov=r_has[:, W_HOG_] if RON and W_HOG_ >= 0 else None,
                            lead_has=(np.where(LW_T_ >= 0, r_has[:, np.maximum(LW_T_, 0)], False) if LW_ON else None)))
            if LW_ON and WL.PP.lw_lost:   # S7: an office the post's end took (a fall, a term, a hand-over, a move)
                for n_, i_, why_ in WL.PP.lw_lost:
                    if LW_T_[i_] >= 0:
                        r_lose(n_, int(LW_T_[i_]), "the post " + why_)
                WL.PP.lw_lost = []
            for n_ in np.nonzero(WL.office_lost)[0]:   # W40: the government fell, and their office with it
                for i_ in W_GOV_:
                    r_lose(n_, i_, "the government fell")
            ei_, ep_, ek_ = WL.era()
            era_i[t], era_p[t], era_k[t] = ei_, ep_, ek_
            if WL.W.era_key != getattr(WL, "_era_key", None):   # an era begins: everyone hears its message (4b)
                WL._era_key = WL.W.era_key
                if WL.W.era_key in COMBO_MIX:
                    era_at[t] = (WL.W.era_key, ei_, ERA_KINDS[ek_])
            drv_h = WL.harsh_n; drv_u = float(WL.W.unrest); drv_p = float(WL.W.prosper)
            alive[:, :5] = WL.PP.alive
            if ID2:   # how strict the people around each person are with the role expected, and how far they accept a named gender
                RS0, AT0 = WL.role_norms()
            clim_w = WL.climate()   # how hostile the place and one's people are to being out (replaces climate + faith)
            if events:   # the world in the story (Emren 10:42): big public events always, the rest when they touch the character
                # or their people; and the cast's own events (the birth, people entering, wants), from the first week on
                for n_, lst_ in WL.story(list(events), dead).items():
                    events[n_].extend(dict(world=e_) for e_ in lst_)
                world_cast(WL.drain())
            else:
                WL.drain()
        if t % record_every == 0:
            W_hist.append(w.copy()); M_hist.append(M.copy()); S_hist.append(stage.copy()); A_hist.append(softmax(y))
            R_hist.append(res.copy()); K_hist.append(held * np.maximum(I, 1e-3))
            if DOM_ON:
                D_hist.append(Dz.astype(np.float32))
            V_hist["acc"].append(plast * ctrl); V_hist["core"].append(softmax(k)); V_hist["SE"].append(SE.copy())
            V_hist["habit"].append(habit / np.maximum(habit.sum(1, keepdims=True), 1e-9))
            V_hist["role"].append(np.einsum("nk,nkc->nc", held * I, prof))
            V_hist["ctrl"].append(ctrl.copy()); V_hist["plast"].append(plast.copy()); V_hist["Q"].append(Q.copy())
            V_hist["content"].append(content.copy()); V_hist["peace"].append(peace.copy()); V_hist["skill"].append(sig.copy())
            V_hist["need"].append(need.copy()); V_hist["adj"].append(adj[:, :NA_OUT].copy())
            V_hist["adj_v"].append((adj_v * ADJ_SIDE)[:, :NA_OUT] if adj_v is not None else np.full((N, NA_OUT), np.nan))
            for nm_, v_ in (("fneed", f_need), ("mood", mood), ("stress", stress), ("cload", cload), ("tension", tension),
                            ("react", react), ("steady", steady), ("base_mood", base_mood), ("outlook", outlook), ("gap", gap_r),
                            ("wound", wound), ("support", support), ("trouble", trouble), ("fortune", fortune), ("horizon", fhz), ("discipline", dsc), ("lvl", lvl), ("q_rel", q_rel), ("unmet", unmet), ("hope_w", hzf * unmet), ("threat", thr), ("scar", scar.sum(1))):
                V_hist[nm_].append(np.broadcast_to(v_, (N,)).copy())
            V_hist["doors"].append(doors(nic, res)); A_src.append(asrc.astype(np.float32)); V_hist["chan"].append(chan.astype(np.float32))
            if HM_ON:   # v22.5 F1: the two halves of health
                V_hist["body"].append(body_v.copy()); V_hist["mind"].append(mind_v.copy())
            for kk_, nm_ in enumerate(("n_dream", "n_passion", "n_plan")):
                V_hist[nm_].append((gk == kk_).sum(1))
            V_hist["harmonious"].append(np.where((gk == 1).any(1), (ga * gs * (gk == 1)).sum(1) / np.maximum((gs * (gk == 1)).sum(1), 1e-9), np.nan))
            V_hist["regret"].append(regret.copy())
            V_hist["n_titles"].append(r_has[:, :NT_].sum(1) if RON else np.zeros(N, int))
            V_hist["n_perks"].append(r_has[:, NT_:].sum(1) if RON else np.zeros(N, int))
        if intervention is not None:
            y0_ = y.copy(); intervention(t, P, nic, y); asrc[:, 6] += y - y0_
        if UPL_ON:   # F15: the start's lean, full to up_from, then fading by half every up_half years
            upf_ = 1.0 if age < P["up_from"] else 0.5 ** ((age - P["up_from"]) / P["up_half"])
            upe_ = 1 - P["up_ease"]                       # how much of the setup's own society pulls
            if P["up_lean"]:
                a_ = softmax(y)
                dy_ = (P["up_lean"] * up_short(a_))[:, None] * centre(5 * (UPM_[None] - a_))
                if age >= P["up_from"]:
                    dy_ = dy_ - UP_DEC * up_oy
                up_oy += dy_
                y = y + dy_; asrc[:, 1] += dy_
        if pausing:
            _ = yield Pause("week", t, locals(), None)
            if WFX_ON:
                wfx = [[] for _ in range(N)]
        e_i, e_p = era_i[t], era_p[t]
        f_w = P["world_pos_k"] * (np.asarray(WL.W.Pos, float) - 0.2) if WON else P["f_world"]   # what the order rewards
        if UPL_ON and P["up_ease"]:   # F15: the setup's society is a lean too (world_profile toward even)
            WP_ = 0.2 + upe_ * (np.asarray(P["world_profile"], float) - 0.2)
            if not WON:
                f_w = upe_ * np.asarray(f_w, float)
        if STH_SOC is not None:   # v22.5, F12: and what the start's society rewards
            f_w = (1 - P["start_soc"]) * f_w + P["start_soc"] * STH_FW
        f_tot = f_w[None, :] + P["lam_local"] * (nic - 0.2) * (np.asarray(WL.PP.msg_w, float)[:, None] if WON else 1.0) \
            + P["era_world"] * e_i * (e_p - 0.2)   # msg_w: how strongly one's groups and people pull (1 typical, spec 3 §1.4)
        if age < 3:
            continue
        stress0 = stress.copy()                        # reactivity scales whatever adds stress this week
        if BAT and not WON and t % 52 == 0 and age > 12:   # grandparents of grown children die outside the story (the Library writes it for childhood)
            alive[:, 3] = rng.binomial(alive[:, 3].astype(int), 1 - min(1, P["mort"][0] * np.exp(P["mort"][1] * (age + 55))))
        if BAT and t % 4 == 0:   # each month: which inner moments, echoes and life-event gates hold for each person
            alive[:, 4] = held[:, PAR]
            cond_hold += cond_ok * (stage >= 2)[:, None]; cond_n += (stage >= 2)
            back_ = (friend_back > NEVER // 2) & (t >= friend_back); alive[back_, 2] = 1; friend_back[back_] = NEVER
            ns = cond_ns(t, age, w)
            memo_ = {}   # speed pass: within this month a condition's text gives the same answer (none draws chance here)
            for c_ in L["COND"]:
                if c_["kind"] == 2:
                    continue
                cond_ok[:, c_["s"]] = ev_memo(c_["req"], ns, memo_)
                cond_fac[:, c_["s"]] = factor(c_, ns, memo_) * P["inner_w"] if c_["kind"] == 1 else factor(c_, ns, memo_)
            if ID2:   # N1b: intimacy comes less often to an asexual person; a same-sex couple has a baby only as planned;
                # an intersex person's own pregnancy or fathering is rarer (a moment without a condition starts from 1)
                for si_ in INTIM_:
                    cond_fac[:, si_] = (cond_fac[:, si_] if si_ in COND_S else 1.0) * np.where(ace, P["ace_intim"], 1.0)
                if BABY_ >= 0:
                    ok_ = ~(held[:, PAR] & partner_same) | ((gk == 2) & (gd == KID)).any(1)
                    f_ = np.where(intersex, P["intersex_fert"], 1.0)
                    if BABY_ in COND_S:
                        cond_fac[:, BABY_] *= f_; cond_ok[:, BABY_] &= ok_
                    else:
                        cond_fac[:, BABY_] = f_ * ok_
            for e_, c_ in enumerate(ECH):
                newa = (echo_anchor[:, e_] <= NEVER // 2) & ev_cond(c_["anchor"], ns)
                if np.count_nonzero(newa):   # the clock starts; only some anchors ever come back (the rest just hold the slot a while)
                    ii_ = np.nonzero(newa)[0]; lo_, hi_ = c_["delay"]
                    echo_anchor[ii_, e_] = t; echo_end[ii_, e_] = t + int((hi_ + 2) * 52)
                    echo_due[ii_, e_] = np.where(rng.random(len(ii_)) < P["echo_p"] * ECH_R[e_], t + rng.uniform(lo_, hi_, len(ii_)) * 52, 10 ** 9)
                old_ = (echo_anchor[:, e_] > NEVER // 2) & (t > echo_end[:, e_])
                echo_anchor[old_, e_] = NEVER
                pend = (echo_anchor[:, e_] > NEVER // 2) & (t >= echo_due[:, e_])
                echo_ready[:, e_] = False
                if np.count_nonzero(pend):
                    ns["sa"] = ys_ = np.where(pend, (t - echo_anchor[:, e_]) / 52, 0.0)
                    echo_ready[:, e_] = pend & ev_cond(c_["req"], ns)
                    echo_fac[:, e_] = factor(c_, ns)

        # ---- 1. situation: unlocked by life stage, weighted toward what your niche brings
        # gate: everything but the life stage (the age window, needs and excludes, and in a batch its conditions)
        gate = (((age >= L["AGE"][:, 0]) & (age <= L["AGE"][:, 1])) | (not P["age_windows"]))[None]
        nk_, ek_ = L["NEEDK"], L["EXCLK"]                     # situations that need, or exclude, a commitment
        excl = held.copy(); excl[:, CAR] |= retired                # no new career after retiring
        gate = gate & ((nk_ < 0)[None] | held[:, np.maximum(nk_, 0)]) & ((ek_ < 0)[None] | ~excl[:, np.maximum(ek_, 0)])
        if RE_ON:   # F8: retired and not working, the work moments no longer come (the doors back stay)
            gate = gate & ~((retired & ~held[:, CAR])[:, None] & WORK_S[None])
        avail = L["STG"][:, stage].T & gate                   # N,S: stage and gate
        if BAT:   # batch: once per life (or per commitment), the condition holds, the one who would die is alive
            avail0 = avail
            gate = gate & cond_ok & ~once_done[:, ROOT]
            if SH_ON:
                gate[:, SH_I] &= SH_EL
            if RON:   # a moment only someone holding a title or perk meets (a nurse's night shift): any of its holds:, and
                # with tenure: only while one of them has been held that many years (Emren's point 6: new, settled, senior)
                if HOLDS_.size:
                    gate[:, HOLDS_] &= (r_has[:, HOLD_C].astype(np.float32) @ HOLDM_C) > 0
                if TENS_:   # speed pass: the same test for every tenure moment at once (then the loop's last values)
                    y_ = (t - r_since[:, TEN_I]) / 52
                    gate[:, TEN_S] &= np.logical_or.reduceat(r_has[:, TEN_I] & (y_ >= TEN_LO) & (y_ <= TEN_HI), TEN_ST, axis=1)
                    s_, ii_, lo_, hi_ = TENS_[-1]; y_ = (t - r_since[:, ii_]) / 52
            if AQ_ON:   # v7: a moment that comes only to someone in a state (a wealthy person's advisor calls)
                gate &= (L["ADJ_SREQ"] < 0)[None] | adj[:, np.maximum(L["ADJ_SREQ"], 0)]
            if WON:   # a cast death this week (or one waiting for its moment) still opens its moment: the cast counted it already
                dth_ = (WL.deaths()[:, :5] > 0) | dq_
                if OR_ON:   # F7, one roll of the living: a death in the cast is the world's, so its moment comes only then
                    gate[:, KL_] &= np.concatenate([dth_, alive[:, 5:6] > 0], 1)[:, KILLS[KL_]]
                else:
                    gate[:, KL_] &= (alive[:, KILLS[KL_]] > 0) | np.concatenate([dth_, np.zeros((N, 1), bool)], 1)[:, KILLS[KL_]]
            else:
                gate[:, KL_] &= alive[:, KILLS[KL_]] > 0
            if BA_ON and BF_ON:   # birth_free: each own-birth moment at least a year after the last child
                gate[:, BIRTH_S] &= ((t - kid_last) >= 52)[:, None]
            if BORN_S_ >= 0:   # F7: the moment a child is born is a birth, at least a year after the last one
                gate[:, BORN_S_] &= (t - kid_last) >= 52
            gate[:, INNER_] &= (t - sit_last[:, INNER_]) >= P["inner_gap"]
            if SEA_ON:
                gate_sea = gate.copy()                         # for the season's own moments, before they are kept out
                gate[:, TH_ANY] = False                       # a season's moments come only in its season
            avail = L["STG"][:, stage].T & gate
        aff = np.exp(2.0 * (nic @ L["ALPHA"].T)) * avail * RATE[None] * (1 + P["dom_freq"] * (held * I) @ L["DOM"].T)
        if SACS_ON_:   # S5: a sacred line's moments come only with an offer (or a wound) of the life's own
            aff[:, SACS_] = 0.0
        if BAT:
            aff = aff * cond_fac
        if WON:   # the world: time of year, holy days, the place's features, the settings one is in, the technology there is
            mf_ = WL.moment_factor(age, sit_last); aff = aff * mf_
        if FARS_ON_:   # far_ties: a far moment comes only with a tie's call (forced), never by the everyday draw
            aff[:, FARS_] = 0.0
        if EYEW_ON_:   # S3, S4: a caught-between or odd-one-out moment comes only by the place reading
            aff[:, EYEW_] = 0.0
        if LEADS_ON_:   # lead_ways (S7): a post's moment comes only with the post (forced), never by the everyday draw
            aff[:, LEADS_] = 0.0
        if WO_ON:   # F10: a world moment only on the world's event; one waiting for the world keeps its gap:
            aff[:, WMZ_] = 0.0
            if len(WG_I):
                aff[:, WG_I] = aff[:, WG_I] * _uclip(((t - sit_last[:, WG_I]) / 52 - WGLO_) / WGW_, 0, 1)
        aff_open = aff                                 # the moments open to the person, before their pause
        if GAPXON_:   # gap: on an everyday or inner moment
            gapw_ = np.ones(sit_last.shape)   # speed pass: the ramp on the gapped moments' columns only (1 elsewhere, as before)
            gapw_[:, GAPX_I] = _uclip(((t - sit_last[:, GAPX_I]) / 52 - GAPXLO_[:, GAPX_I]) / GAPXW_[:, GAPX_I], 0, 1)
            aff = aff * gapw_
        if SHON:   # G stuck in their ways: moments that could start something new come less often
            sdr_ = 1 - P["sh_door"] * shA[:, 4][:, None] * SH_NEW[None]
            aff = aff * sdr_
        if DTH_ON and (dl_at > NEVER // 2).any():   # v22.5 F2: in a last decline nothing new begins
            aff = aff * np.where((dl_at > NEVER // 2)[:, None], 1 - 0.95 * SH_NEW[None], 1.0)
        seekE = 1.0 if not SHON else sdr_
        if GON:   # v7: plans (and a little, passions) make people seek chances for them; a domain plan seeks its life events
            aff = aff * (1 + P["g_seek"] * np.einsum("ng,ngs->ns", gs * np.where(gk == 2, 1.0, np.where(gk == 1, 0.5, 0.0)), gsr))
            seekE = seekE * (1 + P["g_seek_ev"] * np.einsum("ng,ngs->ns", gs * ((gk == 2) & (gd >= 0)), gsr))
        if P["base_rates"]:
            # v6: life events come at their real yearly rates; every other week is ordinary life (an everyday situation)
            # the outside context moves each kind of event: family, resources, the era, the world
            X = np.stack([held[:, PAR] + held[:, KID] + 0.5 * held[:, COM] - 1.0,
                          (np.asarray(WL.PP.ties, float) if WON and not TP_ON else res[:, TIE]) - 0.5, res[:, MON] - 0.5,
                          res[:, HEA] - 0.5, np.full(N, era_i[t]), np.broadcast_to(drv_h, (N,)), np.full(N, drv_u),
                          np.full(N, drv_p), held[:, COM] * I[:, COM] + (np.asarray(WL.PP.community, float) if WON else 0.0),
                          _uclip(stress - 0.5, -0.5, 1.0), np.minimum(trouble, 2.0), np.minimum(fortune, 2.0)], 1)
            if GAPON_:   # the Library's gap: lo-hi (speed pass: each column computed once, by the rule that keeps it)
                refr = np.empty(ev_last.shape)
                refr[:, GAPN_I] = 1 - np.exp(-(t - ev_last[:, GAPN_I]) / (52 * P["ev_refr"]))
                refr[:, GAPM_I] = _uclip(((t - ev_last[:, GAPM_I]) / 52 - GAPLO_[:, GAPM_I]) / GAPW_[:, GAPM_I], 0, 1)
            else:
                refr = 1 - np.exp(-(t - ev_last) / (52 * P["ev_refr"]))
            xd_ = np.exp(X @ DRV.T)   # speed pass: computed once, used twice (the same numbers)
            ev_p = PERY[:, stage].T * avail * P["event_scale"] / 52 * ev_pm * xd_ * refr * seekE   # N,S
            if BA_ON and BF_ON:   # F9: a life's own births by its age, not its stage (the age window is in the gate)
                ev_p[:, BIRTH_S] = (BF_P * np.broadcast_to(gate, ev_p.shape)[:, BIRTH_S] * P["event_scale"] / 52
                                    * np.broadcast_to(ev_pm, ev_p.shape)[:, BIRTH_S] * xd_[:, BIRTH_S] * refr[:, BIRTH_S]
                                    * np.broadcast_to(seekE, ev_p.shape)[:, BIRTH_S])
            if AF_ON:   # F9: these life events by age, not the life stage reached (the age window is in the gate)
                ev_p[:, AF_S] = (AF_P * np.broadcast_to(gate, ev_p.shape)[:, AF_S] * P["event_scale"] / 52
                                 * np.broadcast_to(ev_pm, ev_p.shape)[:, AF_S] * xd_[:, AF_S] * refr[:, AF_S]
                                 * np.broadcast_to(seekE, ev_p.shape)[:, AF_S])
            if BAT:   # how much the drivers raise each event's rate on average among those it can happen to (for DRV_NORM)
                el_ = avail & (PERY[:, stage].T > 0)
                drv_sum += (xd_ * el_).sum(0); drv_cnt += el_.sum(0)
                if DS_ON:   # F9: the drivers choose who, not how many, also with the world on and the v22.5 means: each
                    # life event's rate over its drivers' mean so far in this run (the norm its per_year already took out)
                    ev_p = ev_p * np.where(drv_cnt > 0, DRVN_ / np.maximum(drv_sum / np.maximum(drv_cnt, 1), 1e-9), 1.0)[None]
            if BAT:
                ev_p = ev_p * cond_fac             # the engine's likelier / rarer reading of a life event (1 when it has none)
            if CRS_ON:   # F16: the life events that start a partnership, a child, a faith come at each life's own lean
                crq_ = course_q(); cev_ = CRS_EV >= 0                # (a child's at it whether or not they hold one)
                cm_ = crq_[:, np.maximum(CRS_EV[cev_], 0)]
                cm_ = np.where(held[:, CRS_KS[np.maximum(CRS_EV[cev_], 0)]] & (CRS_EV[cev_] != 1)[None], 1.0, cm_)
                ev_p[:, cev_] *= cm_
            if BA_ON and P["birth_par"] is not None:   # F9.3: by the children already living
                bp_ = np.asarray(P["birth_par"], float)
                ev_p[:, BIRTH_S] *= bp_[np.minimum(alive[:, 5].astype(int), len(bp_) - 1)][:, None]
            if BA_ON:   # late births: a life's own births by its age and sex
                ev_p[:, BIRTH_S] *= P["birth_k"] * np.where(female[:, None], fert(age, FERT_F) / BA_NF[None],
                                                            fert(age, FERT_M) / BA_NM[None])
            if BAT:   # deaths come at the rate of the age of those still alive (engine-owned; the Library's window still gates)
                qd_ = np.repeat(np.minimum(1, P["mort"][0] * np.exp(P["mort"][1] * (age + KILL_OFF[KILLS[KL_]])))[None], N, 0)
                if KCH_.any():   # R15: the children's own ages (the first child's years, less a little for the younger ones)
                    ca_ = np.maximum((t - since[:, KID]) / 52 - 1.5, 0)
                    qc_ = np.maximum(P["mort"][0] * np.exp(P["mort"][1] * ca_), P["kid_mort"]) + P["infant_mort"] * (t - kid_last < 52)
                    qd_[:, KCH_] = np.minimum(qc_, 1)[:, None]
                ev_p[:, KL_] = ((1 - (1 - qd_) ** alive[:, KILLS[KL_]]) * avail[:, KL_] * P["event_scale"] / 52 * ev_pm[:, KL_]
                                * np.exp(X @ DRV[KL_].T) * refr[:, KL_])
                if KCH_.any() and P["child_norm"]:   # C-X5: each child at their own age (the first child's years, each later
                    kc_ = np.nonzero(KL_)[0][KCH_]   # one about child_gap younger), a baby's first year once, and not raised by
                    a1_ = (t - since[:, KID]) / 52; nk_ = alive[:, KILLS[kc_[0]]]   # the event scale or one's spread (the
                    sv_ = 1 - P["infant_mort"] * (t - kid_last < 52)                # drivers still choose whose child)
                    for j_ in range(int(nk_.max(initial=0))):
                        q_ = np.maximum(P["child_mort"] * np.exp(P["mort"][1] * np.maximum(a1_ - P["child_gap"] * j_, 0)), P["kid_mort"])
                        sv_ = sv_ * np.where(nk_ > j_, 1 - np.minimum(q_, 1), 1.0)
                    ev_p[:, kc_] = ((1 - sv_) * (nk_ > 0))[:, None] * avail[:, kc_] / 52 * np.exp(X @ DRV[kc_].T) * refr[:, kc_]
            if WON:   # the world: each life event's rate by season, place, medicine and war (W.rate_mult), gated as above;
                # the world's own events, a cast member's ripe want and a death in the cast bring their moments (the
                # cast's deaths replace the engine's draw of them, but a child's, which the engine still keeps)
                rf_w = WL.rate_factor(sec_w if RON else np.full(N, -1))
                ev_p = ev_p * rf_w * mf_ * WL.channel_rates()   # and contagion, move wish
                ev_p[:, KL_ & ~KCHILD_] = 0.0
                frc_ = WL.fire_now.copy(); fdd_ = np.zeros_like(frc_); dfr_ = []
                if BA_ON and frc_[:, BIRTH_S].any():   # a birth the world brings comes by the same age and sex
                    frc_[:, BIRTH_S] &= (ba_rng.random(N) < np.where(female, fert(age, FERT_F), fert(age, FERT_M)))[:, None]
                for r_ in range(5):
                    for n in np.nonzero(dth_[:, r_])[0]:
                        ks_ = np.nonzero((KILLS == r_) & avail[n])[0]
                        si_ = int(ks_[WL.PP.rng.integers(len(ks_))]) if len(ks_) else -1
                        if si_ >= 0:
                            frc_[n, si_] = True; fdd_[n, si_] = True
                        dfr_.append((int(n), r_, si_))
                frc_ &= avail; fdd_ &= avail
                if CRS_ON and frc_[:, cev_].any():   # F16: a match or a birth the world brings, at the same lean (as a chance)
                    frc_[:, cev_] &= crs_rng.random(frc_[:, cev_].shape) < cm_
                if WO_ON:   # F10: a world moment is not brought again inside its own gap: (once means once)
                    frc_[:, WMZ_] &= refr[:, WMZ_] > 0
            if FARS_ON_:
                ev_p[:, FARS_] = 0.0
            if EYEW_ON_:
                ev_p[:, EYEW_] = 0.0
            if LEADS_ON_:
                ev_p[:, LEADS_] = 0.0
            if SACS_ON_:
                ev_p[:, SACS_] = 0.0
            if BL_ON:   # v22.5 F1: the body's own risks (constitution, habits, strain, money) reach its moments in the Library
                bk_ = np.minimum(np.exp(BP_["risk_k"] * (np.interp(age, BAGE_X, BAGE_Y) - body_v)), 2.0)
                if P["risk_norm"]:   # F9: the risks choose who, the Library's rates how many (the living's mean is 1)
                    bk_ = bk_ / max(float(bk_[~dead].mean()) if (~dead).any() else 1.0, 1e-9)
                ev_p[:, BL_S] *= bk_[:, None]
            if ML_ON:   # and the mind's, less with resilience
                mk_ = np.minimum(np.exp(MP_["risk_k"] * (0.75 - mind_v)), 3.0) * (1 - md_res)
                if P["risk_norm"]:
                    mk_ = mk_ / max(float(mk_[~dead].mean()) if (~dead).any() else 1.0, 1e-9)
                ev_p[:, ML_S] *= mk_[:, None]
            if DTH_ON and (dl_at > NEVER // 2).any():   # F2: in a last decline nothing new begins
                ev_p = ev_p * np.where((dl_at > NEVER // 2)[:, None], 1 - SH_NEW[None], 1.0)
            fire = rng.random(ev_p.shape) < ev_p
            if WON:
                fire |= frc_
            if dead.any():
                fire &= ~dead[:, None]
            had_ev = fire.any(1)
            s_ev = np.argmax(np.where(fire, rng.random(ev_p.shape) + (2.0 * frc_ + 1.0 * fdd_ if WON else 0.0), -1.0), 1)
            if WON:   # a death in the cast brings its moment (first among the world's moments); if none is open, it waits up
                # to eight weeks for one, and only then grieves without it
                for n, r_, si_ in dfr_:
                    if si_ >= 0 and had_ev[n] and s_ev[n] == si_ and not dead[n]:
                        dq_[n, r_] = False
                        continue
                    if not dq_[n, r_]:
                        dq_[n, r_] = True; dq_t[n, r_] = t
                    if not dead[n] and t - dq_t[n, r_] < 8:
                        continue
                    dq_[n, r_] = False
                    need[n, NIDX["belonging"]] -= KILL_HIT[r_, 0]; stress[n] += KILL_HIT[r_, 1]
                    hz_mem[n] += P["hz_remind"] * HZ_ROLE[r_]; ago["death"][n] = t; ago["loss"][n] = t
                    if r_ == ROLES.index("partner") and held[n, PAR]:
                        widowed[n] = True; end([n], [PAR], "widowed", t)
                    if n in events:
                        events[n].append(dict(death=dict(age=round(age, 2), role=ROLES[r_], left=int(WL.PP.alive[n, r_]))))
            ev_last[had_ev, s_ev[had_ev]] = t
            if WFX_ON:   # a life event the world brought (its event) or made likelier or rarer (its rate), when it comes
                for n in np.nonzero(had_ev & ~dead)[0]:
                    si_ = int(s_ev[n])
                    if frc_[n, si_]:
                        e_ = WL.fire_why.get(si_)
                        if e_ is not None and not fdd_[n, si_] and WL.pending.get(int(n), (0, 0, -1))[2] != si_:
                            wfx_add(n, e_.get("kind"), "moment", 1.0, age, moment=L["names"][si_],
                                    cause=dict(domain=e_.get("domain"), kind=e_.get("kind"), key=e_.get("key"), age=round(age, 2)))
                    elif WL.rk[si_] >= 0 and WLM.RK[WL.rk[si_]] != "birth" and abs(rf_w[n, si_] - 1) >= 0.1:
                        rk_ = WLM.RK[WL.rk[si_]]; m_ = float(rf_w[n, si_])
                        wfx_add(n, "unemployment" if rk_ == "jobloss" else rk_, WFX_RISK[rk_], m_ - 1, age,
                                moment=L["names"][si_], share=round(max(0.0, 1 - 1 / m_), 3))
            if P["ev_gap"]:   # a child version and its original are one event: the pause covers both
                for n in np.nonzero(had_ev & HASFAM_[s_ev])[0]:
                    ev_last[n, ROOT == ROOT[s_ev[n]]] = t
            for n in np.nonzero(had_ev)[0]:
                lev_log.append((int(n), t, int(s_ev[n])))
            aff_d = aff * EVERYDAY[None]; near_e = None
            if BAT:   # a person whose rite of passage is late (a 20-year-old still juvenile) lives the everyday of their age:
                # when few ordinary moments are open in their stage and age (title and joining moments do not count, or
                # a choir member would meet the choir every week), the neighbouring stages' open moments join in. A
                # moment only resting (gap:) still counts as open; what joins keeps its own pause and the engine's reading
                rowz = ((aff_open * EVERYDAY[None] > 0) & REG_[None]).sum(1) < P["everyday_min"]
                if rowz.any():
                    near = L["STG"][:, np.minimum(stage[rowz] + 1, NS - 1)].T | L["STG"][:, np.maximum(stage[rowz] - 1, 0)].T
                    near &= ~L["STG"][:, stage[rowz]].T          # the stage's own moments are counted already
                    add_ = np.exp(2.0 * (nic[rowz] @ L["ALPHA"].T)) * (near & gate[rowz] & REG_[None]) * RATE[None] * cond_fac[rowz]
                    if WON:   # the world's gates hold here too: the spheres' (haunt, rung, sphere event) always, the rest
                        add_ = add_ * np.where(WL.new_gates[None] | P["near_gate"], mf_[rowz], 1.0)   # with near_gate
                    aff_d[rowz] += add_ * gapw_[rowz] if GAPXON_ else add_
                    near_e = np.zeros_like(aff_d); near_e[rowz] = add_   # open before their pauses (gap_keep)
            # never a life event as an ordinary week: if every everyday moment is resting, the least rested of the open
            # ones (their weight before the pause); only if none is open at all, anything open (Library 23:20)
            aff_e = aff_open * EVERYDAY[None]
            if BAT and P["gap_keep"] and GAPXON_:   # another moment's pause never raises a moment's own weekly chance: each
                # moment that is not ordinary routine (a door, a holder's moment, an inner one) keeps its share of everything
                # open before the pauses (its rate on the everyday scale); the ordinary routine fills the weeks the pauses free
                open_e = aff_e if near_e is None else aff_e + near_e
                tot_ = open_e.sum(1)
                reg_ = aff_d * ROUT_[None]; oth_ = (aff_d - reg_) / np.maximum(tot_, 1e-12)[:, None]
                oth_ = oth_ / np.maximum(oth_.sum(1, keepdims=True), 1.0)
                gx_ = np.ones(sit_last.shape, bool)   # speed pass: tested on the gapped moments' columns only
                gx_[:, GAPX_I] = (t - sit_last[:, GAPX_I]) / 52 >= GAPXLO_[:, GAPX_I]
                re_ = open_e * ROUT_[None] * gx_   # never inside its gap's lo
                rs_ = reg_.sum(1, keepdims=True); rse_ = re_.sum(1, keepdims=True)
                gf_ = P["gap_fill"]   # the freed weeks spread over the routine by its weight before (gf) and after its own pauses
                fw_ = gf_ * re_ / np.maximum(rse_, 1e-300) + (1 - gf_) * np.where(rs_ > 0, reg_ / np.maximum(rs_, 1e-300), re_ / np.maximum(rse_, 1e-300))
                fill_ = fw_ / np.maximum(fw_.sum(1, keepdims=True), 1e-300)
                kp_ = ((rs_ + rse_) > 0)[:, 0] & (tot_ > 0)
                aff_d[kp_] = oth_[kp_] + (1 - oth_[kp_].sum(1, keepdims=True)) * fill_[kp_]
            aff = np.where(aff_d.sum(1, keepdims=True) > 0, aff_d, np.where(aff_e.sum(1, keepdims=True) > 0, aff_e, aff))
        aff /= aff.sum(1, keepdims=True)
        s = (aff.cumsum(1) > rng.random((N, 1))).argmax(1)
        if pausing:
            s = yield Pause("situation", t, locals(), s)
        if P["base_rates"]:
            s = np.where(had_ev, s_ev, s)
        if BAT and P["base_rates"] and len(ECH):   # a due echo comes back in a week without a life event
            pe_ = (echo_ready & avail0[:, ECH_S] & ~once_done[:, ROOT[ECH_S]] & ~had_ev[:, None] & ~dead[:, None]) \
                * np.minimum(1, P["echo_w"] * echo_fac)                    # once: on an echo is honoured too
            fe_ = rng.random(pe_.shape) < pe_
            has_e = fe_.any(1)
            if has_e.any():
                e_pick = np.argmax(np.where(fe_, rng.random(fe_.shape), -1.0), 1)
                ie_ = np.nonzero(has_e)[0]
                s[ie_] = ECH_S[e_pick[ie_]]
                echo_anchor[ie_, e_pick[ie_]] = NEVER; echo_ready[ie_, e_pick[ie_]] = False
        sea_tr = np.zeros(N, bool)
        if SEA_AGE_ON:   # a stage's season not yet opened by its rite comes at its age (waiting for a running season to end)
            for k_ in SEA_KS:
                last_ = SEA_HI[k_] - SEA_LEN_Y
                due_ = ~sea_had[:, k_] & ~dead & (age >= sea_age[:, k_]) & (age <= last_ + 1 / 52) & ((sea_k < 0) | (age >= last_))
                if k_ == ELD_ and RET_SEA:   # later life opens with retiring; someone still at work by its last week opens it then
                    due_ &= (ret_pend < 0) & (~held[:, CAR] | (age >= last_))
                for n in np.nonzero(due_)[0]:
                    sea_open(n, k_)
        if SEA_ON and (sea_k >= 0).any():   # threshold season: the due step's moment in place of an ordinary week
            for n in np.nonzero(sea_k >= 0)[0]:
                dt_ = t - sea_t0[n]
                if dt_ > P["season_len"]:
                    sea_k[n] = -1; continue
                B[n] = max(B[n], P["season_open"])            # open through the season
                if had_ev[n] if P["base_rates"] else False:
                    continue                                   # a big life event this week: the step waits
                due_ = np.nonzero(~sea_done[n] & (dt_ >= SW_))[0]
                if not len(due_):
                    continue
                st_ = int(due_[np.argmin(SW_[due_])]); sea_done[n, :st_ + 1 if st_ < 3 else 0] = True; sea_done[n, st_] = True
                if st_ == 3:   # the transforming chance's own week: the season's transform: moment (any step)
                    c_ = np.nonzero((TH_K == sea_k[n]) & TH_TR & gate_sea[n])[0]
                else:          # a step: its plain moments first; its transform: moment only when no plain one is open
                    c_ = np.nonzero((TH_K == sea_k[n]) & (TH_STEP == st_ + 1) & gate_sea[n])[0]
                    if (~TH_TR[c_]).any():
                        c_ = c_[~TH_TR[c_]]
                    elif len(c_):
                        sea_done[n, 3] = True
                if ret_pend[n] >= 0 and st_ == 0:             # retiring: the season opens on the last day at work
                    cr_ = c_[RETIRES_[c_]]
                    if len(cr_):
                        c_ = cr_
                    elif held[n, CAR]:
                        end([n], [CAR], "retired", t); ret_pend[n] = -1
                if len(c_) and P["season_excl"]:    # K6: one draw for the step; each moment at its own share, tilted by
                    tl_ = np.exp(2.0 * (nic[n] @ L["ALPHA"][c_].T))   # the person's colours (share-weighted mean tilt 1)
                    pp_ = TH_P[c_] * tl_ * TH_P[c_].sum() / max((TH_P[c_] * tl_).sum(), 1e-12)
                    pp_ = pp_ / max(1.0, pp_.sum()); k_ = int(np.searchsorted(np.cumsum(pp_), sea_rng.random(), side="right"))
                    c_ = c_[k_:k_ + 1]                # past the sum: the step passes as an ordinary week
                elif len(c_) and P["season_share"]:   # each step moment comes to its share of lives (Library next3 §4): a
                    c_ = c_[sea_rng.random(len(c_)) < TH_P[c_]]   # step none of whose moments comes passes as an ordinary week
                if len(c_):
                    wt_ = np.exp(2.0 * (nic[n] @ L["ALPHA"][c_].T)) * RATE[c_]
                    s[n] = c_[rng.choice(len(c_), p=wt_ / wt_.sum())]
                    sea_tr[n] = TH_TR[s[n]]
                if sea_done[n].all():
                    sea_k[n] = -1
        # a commitment that no longer fits what the person wants, and keeps disappointing, comes up for reconsideration
        a_now = softmax(y)
        misfit = _uclip(1 - 5 * (prof * a_now[:, None, :]).sum(-1), 0, 1)   # wanting what it stands for less than an even share
        p_re = held * P["recon_p"] * (1 - sat) * (1 + 3 * misfit) * (stage >= 2)[:, None]   # children cannot walk away
        mf_ = np.where(held, misfit, -1.0) if P["recon_held"] else misfit   # (the game's family check: a partner left twice)
        p_re = np.where(force_re[:, None] & (mf_ > P["clash_off"]) & (mf_ >= mf_.max(1, keepdims=True)), 1.0, p_re)
        force_re[:] = False
        hit = rng.random((N, NK)) < p_re
        rk = np.where(hit.any(1), np.argmax(np.where(hit, p_re, -1.0), 1), -1)
        recon = rk >= 0
        s = np.where(recon, L["RECON"], s)
        sit_n[np.arange(N), s] += 1                              # how often each situation came up in each life
        m = L["M"][s]; e = Eeff[s]; e0 = L["E"][s]; diff = L["DIFF"][s]; mask = L["MASK"][s]
        stakes = L["STAKES"][s]; alpha = L["ALPHA"][s]; oid = L["OID"][s]
        ri = np.nonzero(recon)[0]; rkk = rk[ri]
        if len(ri):
            pk = prof[ri, rkk]
            m[ri, 0] = pk; m[ri, 1] = 0.5 * pk + 0.5 * a_now[ri]; m[ri, 2] = EXIT
            e[ri, :3] = 0.7 * m[ri, :3]
        do_nothing = (m.std(-1) < 1e-9)
        closed_s = L["CLOSED"][s] if BAT else None
        pbump = 0.0; earn = 0.0; lackf = 1.0
        if RON:   # an act that needs a title or perk the person lacks: impossible (acting as what one is not), or closed by
            rq_ = GR["A_REQ"][s]                                  # law, approval or means (the act's without:, else the kind's)
            unmet = (rq_ >= 0) & ~r_has[ar[:, None], np.maximum(rq_, 0)]
            if unmet.any():
                wk_ = np.where(GR["A_WITHOUT"][s] >= 0, GR["A_WITHOUT"][s], GR["without_default"][np.maximum(rq_, 0)])
                mask = mask & ~(unmet & (wk_ == 3))
                closed_s = np.where(unmet & (wk_ < 3) & (closed_s < 0), wk_, closed_s)
                if LACK_ON:
                    lackf = np.where(unmet, A_LACK[s], 1.0)
            # skills and standing make acts in their ways likelier to work (a lapsed skill counts at its fading level)
            hp_ = r_has[:, NT_:]                                 # the best perk in each color counts fully, the rest a little
            cb_ = (np.where(MEM_K, np.maximum(hp_, p_lev), hp_) * ODD4)[:, :, None] * INDP[None]      # N,perks,C (logit units)
            mx_ = cb_.max(1); PB = np.minimum(mx_ + P["perk_breadth"] * (cb_.sum(1) - mx_), P["perk_cap"])
            pbump = np.einsum("nkc,nc->nk", m, PB)
            gr_ = A_GR1[s]; gi_ = np.maximum(gr_, 0)             # regaining a lapsed licence or skill is easier while it lasts
            pbump = pbump + np.where((gr_ >= 0) & ~r_has[ar[:, None], gi_], p_lev[ar[:, None], np.maximum(gi_ - NT_, 0)], 0.0)
            at_ = missed_at(GR["A_EARN"][s], s) if EARN_ON else None   # N,K: the title (else perk) each option's act earns for
            if AMS_ON:   # {missed}: the budget's cut on the title missed (the written chance carries it for the others)
                pbump = pbump + np.where(AMS_[s] & (missed_t[:, None] >= 0), TZM_[np.maximum(missed_t, 0)][:, None], 0.0)
            if EARN_ON and (at_ >= 0).any():   # prepared for the title the act gives (HELPS), and the right time (WINDOWS)
                rw_ = np.nonzero((at_ >= 0).any(1))[0]; ai_ = np.maximum(at_[rw_], 0)
                hw_ = r_has[rw_].astype(np.float32)
                if P["rung_years"] > 0:   # a rung counts by the years on it (Emren 09:18; packs 09:21)
                    yk_ = black_k()[rw_, None] if RP_ON and P["black_edge"] else 1.0   # black_edge: Black climbs faster
                    hw_[:, :NT_] *= np.minimum(np.maximum(t - r_since[rw_, :NT_], 0) * yk_ / (52.0 * P["rung_years"]), 1.0)
                prep_ = (np.einsum("ni,nki->nk", hw_, GR["HELP"][ai_])
                         + np.einsum("nm,nkm->nk", (mark_n[rw_] > 0).astype(np.float32), GR["HELP_MK"][ai_][:, :, :NM])) \
                    / np.maximum(GR["HELP_N"][ai_], 1)
                er_ = P["help_lift"] * np.minimum(prep_, 1.0) \
                    + P["try_lift"] * np.minimum(tries_ct[rw_[:, None], ai_], P["try_max"])   # earlier tries at it
                if P["base_rates"]:   # the context that opens this moment's window (driver words), good times or bad
                    wr_ = L["WINDOW_REF"][s[rw_]]
                    er_ = er_ + P["window_lift"] * _uclip((X[rw_] * L["WINDOW"][s[rw_]]).sum(1) / np.maximum(wr_, 1e-9), -1, 1)[:, None]
                earn = np.zeros((N, L["K"])); earn[rw_] = er_ * (at_[rw_] >= 0) * GR["LIFT"][ai_]
        if AQ_ON:   # v7: an act that needs a state the person is not in (wealthy, fit): not offered, or closed by means
            aq_ = L["ADJ_REQ"][s]
            un_ = (aq_ >= 0) & ~adj[ar[:, None], np.maximum(aq_, 0)]
            if un_.any():
                wk_ = np.where(L["ADJ_WOUT"][s] >= 0, L["ADJ_WOUT"][s], ADJ_WITHOUT[np.maximum(aq_, 0)])
                mask = mask & ~(un_ & (wk_ == 3))
                closed_s = np.where(un_ & (wk_ < 3) & (closed_s < 0), wk_, closed_s)
                if LACK_ON:
                    lackf = lackf * np.where(un_, A_LACK[s], 1.0)
        if BAT and CLU_ON:
            clu_ = (closed_s >= 0).astype(float)
        if BAT and IDC_ON:   # N1b: crossing the role the world expects, or naming one's own gender, is closed by approval as
            # strongly as the world frowns on it (in units of a written closed: approval; where one is written, the larger)
            rs_w, at_w, ex_w = role_view()
            ra_ = ROLE_ACT[s]; rc_ = _uclip(ra_, 0, 1)
            cw_ = np.where(ra_ == 3, 1.0, np.where(ra_ < 2, np.take_along_axis(ex_w, 1 - rc_, 1), 0.0)) * (ra_ >= 0)
            u_ = P["role_k"] * rs_w[:, None] * cw_ * np.where(~female & (age < 13), P["role_boys"], 1.0)[:, None]
            u_ = np.maximum(u_, (TRANS_OPT[s] | (OPENMK_[s] & named_g[:, None])) * 2.0 * (1 - at_w)[:, None])
            clu_ = np.where(closed_s >= 0, np.maximum(1.0, u_), u_)
            closed_s = np.where((closed_s < 0) & (u_ > 0), 1, closed_s)
        if BAT and WON:   # the world's law, norms and technology (world-fields.md): a written closed: law opens where the law
            # allows it; an option with law: is closed by the law where it is (banned 1 unit, restricted half); norm: costs
            # 2 x (1 - acceptance) units of approval; tech: is not offered without the technology, and closed by means as
            # far as the person's class lacks it
            ul_, lo_, ua_, um_, gone_ = WL.closures(s, partner_same if ID2 else np.zeros(N, bool), age)
            if WFX_ON:
                wco_.update(s=s.copy(), ul=ul_, lo=lo_, ua=ua_, um=um_, gone=gone_, closed0=closed_s.copy(),
                            role=u_.copy() if IDC_ON else None)
            op_ = lo_ & (closed_s == 0)
            clu_ = np.where(op_, 0.0, clu_); closed_s = np.where(op_, -1, closed_s)
            for kd_, u2_ in ((0, ul_), (1, ua_), (2, um_)):
                closed_s = np.where((closed_s < 0) & (u2_ > 0), kd_, closed_s)
                clu_ = np.maximum(clu_, u2_)
            mask = mask & ~gone_
            diff = diff + WL.odds(s)   # finding work by local unemployment, education by places, treatment by hospitals
            if SV_ON:   # phase 5, service as a chapter: 5 years after the guard or the host, hiring is easier in prot and
                # rule work and a little harder elsewhere; 10 years after prison, harder by the record's weight (Pager 2003)
                jo_ = WL.job_o[s]
                if jo_.any():
                    se_ = r_end[:, SVC_T].max(1) if len(SVC_T) else np.full(N, NEVER)
                    vet_ = (se_ > NEVER) & (t - se_ < 52 * SVS_["after_guard_or_host"]["years"])
                    if len(SVC_T):
                        vet_ &= ~r_has[:, SVC_T].any(1)
                    rec_ = (pris_out > NEVER) & (pris_out <= t) & (t - pris_out < 52 * SVS_["after_prison"]["years"])
                    pr_ = PR_T[np.where(GR["A_TITLE"][s] >= 0, GR["A_TITLE"][s], NT_)]
                    diff = diff + jo_ * (vet_[:, None] * np.where(pr_, SV_D[0], SV_D[1]) + rec_[:, None] * SV_D[2])
                    br_ = (brec > NEVER) & (t - brec < 7 * YR_)   # a bank's record: hiring a little harder
                    diff = diff + jo_ * (br_[:, None] * DB_D)
        if BAT and CLU_ON:
            diff = diff + P["closed_diff"] * clu_
        elif BAT:   # closed by law, approval or means: still pickable, but harder
            diff = diff + P["closed_diff"] * (closed_s >= 0)

        if t == 6 * 52:                                      # raised in a faith: the family's, not a choice
            shu_ = rng.random(N); inh = shu_ < P["faith_inherit"]
            if STH_ON:   # v22.5, F12: raised in the family's own faith (the world's), in none when the family holds none;
                # a start that promises a faith or none keeps it (faith_inherit 1 or 0; the birth was drawn to fit)
                shfi_ = P["faith_inherit"]; shpf_ = np.asarray(WL.PP.pfaith, np.int64)
                inh = np.full(N, shfi_ >= 1) if (shfi_ <= 0 or shfi_ >= 1) else (shpf_ >= 0) & (shu_ < P["faith_fam_p"])
            held[inh, FAI] = True; I[inh, FAI] = 0.3; since[inh, FAI] = t; sat[inh, FAI] = 0.7; faith_given[inh] = True
            prof[inh, FAI] = rng.dirichlet(np.full(C, P["faith_conc"]), inh.sum())     # families hold many kinds of faith
            if STH_ON and inh.any():   # the family's faith's own ways
                shfp_ = np.asarray(WL.W.faith_profile, float); shfp_ = shfp_ / shfp_.sum(1, keepdims=True)
                shk_ = inh & (shpf_ >= 0)
                prof[shk_, FAI] = shfp_[np.minimum(shpf_[shk_], len(shfp_) - 1)]
            for n in np.nonzero(inh)[0]:
                commit_log.append((int(n), t, FAI, "inherited", prof[n, FAI].round(2).tolist(), 0.3))
                if n in events:
                    events[n].append(dict(commitment=dict(age=6.0, kind="faith", what="inherited", profile=prof[n, FAI].round(2).tolist())))

        # ---- v7: how far each option of this week's situation serves each goal (fit with its ways, or a step into its domain)
        if GON:
            cf = _uclip((5 * np.einsum("nkc,ngc->ngk", m, gm) - 1) / 2, 0, 1)
            dstep = (gd[:, :, None] >= 0) & (L["COMMIT"][s][:, None, :] == gd[:, :, None])
            rel = np.where(((gk == 2) & (gd >= 0))[:, :, None], np.maximum(dstep * (0.5 + 0.5 * cf), 0.5 * cf), cf)
            rel = rel * (mask & ~do_nothing)[:, None, :] * (gk >= 0)[:, :, None]
            wR = gs * np.select([gk == 0, gk == 1, gk == 2], [P["g_dream"], P["g_pass"], P["g_plan"]], 0.0)
            wI = gs * np.select([gk == 1, gk == 2], [P["g_pass_auto"] * (1.5 - ga), P["g_plan_auto"]], 0.0)
            gU_R = np.einsum("ng,ngk->nk", wR, rel); gU_I = np.einsum("ng,ngk->nk", wI, rel)
            gN = P["g_notice"] * np.einsum("ng,ngk->nk", gs * (gk >= 0), rel)
            # what a person's weeks usually offer: ways strongly in each color, steps into each domain (for felt odds)
            rk_ = mask & ~do_nothing
            pres_c = pres_c * (1 - 1 / 104) + (np.where(rk_[..., None], m, 0).max(1) >= 0.5) / 104
            pres_d = pres_d * (1 - 1 / 104) + HAS_STEP[s] / 104
            pres_n = pres_n * (1 - 1 / 104) + 1 / 104
        else:
            gU_R = gU_I = gN = 0.0

        # ---- 2. choice
        if DOM_ON:   # in an area of life the colors that weigh the options are the core plus that area's offset
            area_ = L["AREA"][s]; inA_ = area_ >= 0
            zA_ = z + np.where(inA_[:, None], Dz[ar, np.maximum(area_, 0)], 0.0)
            w_hat = softmax(zA_ + P["act"] * alpha)
        else:
            w_hat = softmax(z + P["act"] * alpha)
        a_hat = softmax(y + P["act"] * alpha)
        V = np.einsum("nc,nkc->nk", w_hat, e)            # what current motives value
        VA = np.einsum("nc,nkc->nk", a_hat, e)           # what the person wants to value
        # reading the moment (Emren 09:25, point 8): with experience a person senses part of what the moment calls for and
        # how the world around them pushes, so felt odds spread like the true ones (the rest stays a misread)
        read_ = P["read_moment"][0] + P["read_moment"][1] * M / (M + P["M0"])
        mom_ = np.einsum("nkc,nc->nk", m, f_tot) + P["fit"] * np.einsum("nkc,nc->nk", m, alpha - alpha.mean(1, keepdims=True))
        readk_ = read_[:, None]   # per option; read_skill: expertise reads the moment, skill in its ways fills part of the rest
        if P["read_skill"]:
            readk_ = readk_ + P["read_skill"] * _uclip(np.einsum("nkc,nc->nk", m, sig - 0.3) / 0.7, 0, 1) * (1 - readk_)
        # v10 interpretation: threat focus follows where the deep core sits on security vs freedom, hard times and reactivity
        thr += (1 / (1 + np.exp(-(P["thr0"] + P["thr_axis"] * 5 * (softmax(k) @ AXSEC) + P["thr_hist"] * (wound + 0.5 * trouble)
                                  + P["thr_react"] * (react - 1)))) - thr) / (52 * P["thr_lag"])
        if MIS_ON:   # how the person misreads the odds (felt odds only): focus, memories, scars, mood, status; expertise shrinks it
            mis_ = (P["mis_focus"] * (0.5 - thr) + P["mis_mood"] * mood + P["mis_status"] * hub_)[:, None] \
                + np.einsum("nkc,nc->nk", m, P["mis_mem"] * mem_rel() - P["mis_scar"] * scar)
            if P["mis_expert"]:
                mis_ = mis_ / (1 + P["mis_expert"] * np.minimum(np.einsum("nkc,nc->nk", m, xp_), 3))
        else:
            mis_ = 0.0
        p_hat = 1 / (1 + np.exp(-earned(P["gain"] * (np.einsum("nkc,nc->nk", m, sig + fb) + readk_ * mom_ - diff)
                                        + TON * P["o_bias"] * (outlook - P["o_ref"])[:, None] + pbump + mis_, earn)))   # outlook: optimism or pessimism
        p_hat = np.where(do_nothing, 0.5, p_hat * lackf)   # lacking: the felt odds see it too
        if SEEN_ON:   # S6: a path or colour way seen walked feels more possible, one seen failing less (felt odds only)
            p_hat = WL.seen_felt(p_hat, s, m, ~do_nothing, mask)
        H = np.einsum("nkc,nc->nk", m, habit)             # habit is a pull toward familiar ways of acting
        lack = nimp * np.maximum(0, P["need_set"] - need) / P["need_set"] + P["duty_w"] * np.minimum(1, (held * I) @ DUTY)   # N,J
        serves = np.einsum("njc,nkc->nkj", NMP, np.maximum(e, 0)) if NM_ON else \
            np.einsum("jc,nkc->nkj", NMAP, np.maximum(e, 0))            # needs each option meets
        relief = np.einsum("nj,nkj->nk", lack, serves) * p_hat
        # gate 1, the world: is the option open to this person at all?
        acc = _uclip(P["access_base"] + P["access_k"] * (np.einsum("nkc,nc->nk", m, nic) - 0.2), 0.05, 1.0)
        if BAT and CLU_ON:
            acc = acc * P["closed_acc"] ** clu_
        elif BAT:
            acc = np.where(closed_s >= 0, acc * P["closed_acc"], acc)
        if OWN_ON:   # v22.5, F12: the culture's own acts are always around them (the means gate below still holds)
            acc = np.where(L["OWN"][s], 1.0, acc)
        req = L["REQ"][s]                                    # what each option needs: money, time, health, ties, freedom
        rg = np.where(req > 0, 1 / (1 + np.exp(-P["req_g"] * (res[:, None, :] - req))), 1.0).prod(-1)
        open_n = rng.random(mask.shape) < acc; open_r = rng.random(mask.shape) < rg
        open_ = mask & ((open_n & open_r) | do_nothing)
        # gate 2, the mindset: is an open option even considered? (fit with the deep core)
        kw = softmax(k)
        # v6 (Fredrickson 2001): a good mood widens what a person considers, a bad one narrows it to their usual ways
        ng = P["notice_g"] * (1 - P["broaden"] * _uclip(2 * (content - 0.5) + mood, -1, 1))
        see = 1 / (1 + np.exp(-(P["notice_b"] + ng[:, None] * (5 * np.einsum("nkc,nc->nk", m, kw) - 1) + gN)))   # v7: goals draw the eye
        seen = open_ & ((rng.random(mask.shape) < see) | do_nothing)
        # gate 3, wanting versus pull: reflective (aspiration, odds) vs automatic (motives, habit)
        step = 5 * np.einsum("nkc,nc->nk", m, softmax(y) - w)   # acting the way you want to become
        tryf = 1 + TON * P["o_try"] * (outlook - P["o_ref"])            # a sense of control makes people try to change
        U_R = (P["beta_V"] * VA + P["beta_A"] * tryf[:, None] * step + P["beta_P"] * (p_hat - 0.5) * stakes[:, None]
               + P["beta_N"] * relief)
        U_I = P["beta_V"] * V + P["beta_H"] * (1 + stress[:, None]) * H + P["beta_N"] * relief
        # roles: each held commitment expects its own ways of acting, felt as duty and as routine
        DW = (L["DOM"][s] + P["role_base"]) * held * I
        role = np.einsum("nk,nko->no", DW, 5 * np.einsum("nkc,noc->nko", prof, m) - 1)
        U_R = U_R + P["beta_role"] * role; U_I = U_I + P["beta_role"] * role
        U_R = U_R + gU_R; U_I = U_I + gU_I                   # v7: dreams, passions and plans
        if P["scar_pull"]:                                   # v10: never again, in the ways of a scar
            scU = P["scar_pull"] * np.einsum("nkc,nc->nk", m, scar); U_R = U_R - scU; U_I = U_I - scU
        if P["hz_k"]:                                        # v7: with time felt short, closeness, care and the familiar weigh more
            hzU = P["hz_k"] * fhz[:, None] * np.einsum("nkc,c->nk", 0.5 * (m + e), HZT)   # in its ways and for its ends
            U_R = U_R + hzU; U_I = U_I + hzU
        if len(ri):                                          # walking away costs what was invested; wanting out helps
            built = 5 * (prof[ri, rkk] * softmax(k[ri])).sum(1)      # how much of the deep self was built on it (1 = neutral)
            xc = P["beta_exit"] * EXITW[rkk] * I[ri, rkk] * (0.5 + 0.5 * built)   # sunk cost: leaving betrays that self
            U_R[ri, 2] += -xc + P["beta_A"] * 3 * misfit[ri, rkk]
            U_I[ri, 2] += -xc
        if WON:   # the world: felt reach makes voice and organising at institutions and the state feel worth it (spec 7 §6)
            rU_ = WL.reach_pull(s); U_R = U_R + rU_; U_I = U_I + rU_
            if P.get("sph_fair"):   # spheres phase 4: felt fairness tilts exit, neglect and subvert against voice and loyalty
                fU_ = WL.fair_pull(s) * (P["tau0"] * (1 + 0.5 * stress))[:, None]   # log odds x the choice's tau
                U_R = U_R + fU_; U_I = U_I + fU_
            if ODD_ON_:   # S4: an unplayed life holds on more where its colour is strong and its rung high (log odds x tau)
                oU_ = WL.eyes_pull(s) * (P["tau0"] * (1 + 0.5 * stress))[:, None]
                U_R = U_R + oU_; U_I = U_I + oU_
        if SHON:   # overuse ("when all you have is a hammer"): the shadow pulls toward its colour's ways, fitting or not
            shU_ = P["sh_over"] * np.einsum("nkc,nc->nk", m, shA); U_R = U_R + shU_; U_I = U_I + shU_
        ctrl = np.minimum(1, CTRL[stage] * dsc * _uclip(1 - P["ctrl_stress"] * stress, 0.05, 1)
                          * _uclip(1 + P["peace_ctrl"] * (peace - 0.55), 0.5, 1.3))     # a calm mind steers better
        U = ctrl[:, None] * U_R + (1 - ctrl[:, None]) * U_I
        if DC_ON:   # F17: an option that leaves a deed leans by that deed's canon colours (log odds x the choice's tau)
            U = U + P["deed_canon"] * np.einsum("nkc,nc->nk", DC_L[s], 5 * w - 1) * (P["tau0"] * (1 + 0.5 * stress))[:, None]
        U = np.where(do_nothing, -0.3 + 0.3 * stress[:, None], U)
        tau = P["tau0"] * (1 + 0.5 * stress)
        pr = pr0 = softmax(np.where(seen, U / tau[:, None], -np.inf))
        if P["steer"] is not None:   # the player's steer (P3): it bends the character's own pick, then it is spent
            mix_ = np.asarray(P["steer"], float); mix_ = mix_ / np.maximum(mix_.sum(-1, keepdims=True), 1e-9)
            sU_ = np.where(do_nothing, 0.0, P["steer_k"] * (5 * np.einsum("nkc,nc->nk", m, np.broadcast_to(np.atleast_2d(mix_), (N, C))) - 1))
            pr = softmax(np.where(seen, (U + sU_) / tau[:, None], -np.inf))
            P["steer"] = None
        if SAC_ON_ and WL.sac_pend:   # S5: at an offer on a held line the character's own pick holds it at .9 (and more
            pr = WL.sacred_tilt(s, pr.copy(), mask)   # for a bigger offer, .7 with a gesture); at a tragic one, a, b or torn
        a = (pr.cumsum(1) > rng.random((N, 1))).argmax(1)
        if SHON:   # U indecisive: while they weigh it, the chance passes (the act becomes doing nothing, where there is one)
            lap_ = (rng.random(N) < P["sh_lapse"] * shA[:, 1]) & ~do_nothing[ar, a] & do_nothing.any(1)
            if lap_.any():
                a = np.where(lap_, do_nothing.argmax(1), a)
        if pausing:
            steer_moved = pr[ar, a] - pr0[ar, a]   # how much the steer raised (or lowered) the drawn option's odds
            a_self = a.copy()                      # the character's own pick (a counter-pick lowers its shadow)
            a = yield Pause("choose", t, locals(), a)
        # bookkeeping: where does the option the person most wants get lost?
        UR_ = np.where(mask & ~do_nothing, U_R, -np.inf)
        best = UR_.argmax(1); has = np.isfinite(UR_.max(1))
        lost_open = has & ~open_[ar, best]; lost_seen = has & open_[ar, best] & ~seen[ar, best]
        pulled = has & seen[ar, best] & (a != best); tried = has & (a == best)
        pull_best = np.where(seen & ~do_nothing, U_I, -np.inf).argmax(1)
        conflict = has & seen[ar, best] & (pull_best != best)
        big_gap = 0.5 * np.abs(softmax(y) - w).sum(1) > 0.1; hi_s = stress > 1
        ma = m[ar, a]; ea = e[ar, a]; ea0 = e0[ar, a]; da = diff[ar, a]; ph = p_hat[ar, a]
        idle = do_nothing[ar, a] | dead                 # a life that has ended does nothing
        if BAT and IDC_ON:   # N1b: how far this week's act crossed the role expected of them (role_fit, the game's frown)
            act_cw = cw_[ar, a] * ~idle
        blocked += has & lost_open

        # ---- 3. outcome vs expectation
        fit = P["fit"] * (ma * (alpha - alpha.mean(1, keepdims=True))).sum(1)
        shc_ = P["sh_fail"] * (ma * shA).sum(1) if SHON else 0.0   # shadows: over-reliance on a ruling colour costs
        p_true = 1 / (1 + np.exp(-earned(P["gain"] * ((ma * (sig + f_tot)).sum(1) + fit - da) + (pbump[ar, a] if RON else 0.0) - shc_,
                                         earn[ar, a] if np.ndim(earn) else 0.0)))
        if np.ndim(lackf):
            p_true = p_true * lackf[ar, a]
        if BAT:   # for the Library's chance (batch.CHANCE_REF): skill, world and perks of those who meet each moment, and the
            # true odds of every option for them (calib_v7/chance_check.py)
            rf_ = sig + f_tot + (PB / P["gain"] if RON else 0.0)
            np.add.at(ref_sum, s, rf_); np.add.at(ref_cnt, s, 1.0)
            fk_ = P["fit"] * np.einsum("nkc,nc->nk", m, alpha - alpha.mean(1, keepdims=True))
            pk_ = 1 / (1 + np.exp(-earned(P["gain"] * (np.einsum("nkc,nc->nk", m, sig + f_tot) + fk_ - diff) + pbump
                                          - (P["sh_fail"] * np.einsum("nkc,nc->nk", m, shA) if SHON else 0.0), earn)))
            pk_ = pk_ * lackf                                  # as the engine draws them: earned odds and lacking: included
            if np.ndim(earn):   # the mean earned lift on the options that give a title, for the reference (CHANCE_REF's 6th)
                tk_ = GR["A_EARN"][s] >= 0
                np.add.at(earn_sum, s, (earn * tk_).sum(1) / np.maximum(tk_.sum(1), 1)); np.add.at(earn_cnt, s, tk_.any(1).astype(float))
            np.add.at(pk_sum, s, np.where(mask, pk_, 0.0)); np.add.at(pk_cnt, s, mask.astype(float))   # open to them
        if pausing:
            p_true = yield Pause("odds", t, locals(), p_true)
        succ = rng.random(N) < p_true
        if SHON:   # a shadow shows: an act in the ruling colour's own ways fails while its shadow is strong (check 5)
            shw_ = (ma * shA)
            for n in np.nonzero(~succ & ~idle & (shw_.max(1) > 0.3))[0]:
                c_ = int(shw_[n].argmax()); sh_n[n, c_] += 1
                sh_log.append((int(n), t, c_, int(s[n]), int(a[n])))
                if n in events:
                    events[n].append(dict(shadow=dict(age=round(age, 2), state=SH_STATES[c_], strength=round(float(shA[n, c_]), 2),
                                                      through=L["labels"][s[n]][a[n]])))
        long_miss = (~succ & ~idle & ~recon & (p_true < P["long_shot"]) & (LONGT_[s, a] | (missed_at(GR["A_TITLE"][s, a], s, a) >= 0))
                     ) if RON else np.zeros(N, bool)
        if RON:   # a failed try at a title (else a perk with its own helps) is remembered for the next (try_lift)
            ae_ = missed_at(GR["A_EARN"][s, a], s, a)
            ft_ = np.nonzero(~succ & ~idle & ~recon & (ae_ >= 0))[0]
            if len(ft_):
                ti_ = ae_[ft_]; tries_ct[ft_, ti_] = np.minimum(tries_ct[ft_, ti_] + 1, 100)
        tries += tried; wins += tried & succ
        np.add.at(gates, stage, np.stack([has, lost_open, lost_seen, pulled, tried, tried & succ, conflict, conflict & (a == best),
                                     conflict & big_gap, conflict & big_gap & (a == best), conflict & hi_s, conflict & hi_s & (a == best),
                                     has & ~open_r[ar, best], has & open_r[ar, best] & ~open_n[ar, best]], 1).astype(float))
        r = np.where(succ, 1.0, -P["loss"]) * stakes
        delta = np.where(idle, 0.0, r - (ph - (1 - ph) * P["loss"]) * stakes)
        if pausing:
            delta = yield Pause("learn", t, locals(), delta)
        appf_ = 1 + P["app_k"] * (2 * thr - 1)              # v10 appraisal: a loss weighs appf_, a gain 2 - appf_
        fdelta = delta * np.where(delta < 0, appf_, 2 - appf_) if P["app_k"] else delta   # as felt (mood, stress, wounds)
        if P["app_vigil"] and P["app_k"]:   # app_vigil: threat focus learns more from gains and losses alike (vigilance), so
            ldelta = delta * (1 + P["app_learn"] * (appf_ - 1))   # the colours that bring it (W U, AXSEC) do not teach a life out of themselves
        else:
            ldelta = delta + P["app_learn"] * (fdelta - delta) if P["app_learn"] else delta   # as learned (which ways to keep)
        act_ = (~idle)[:, None]
        fb += 0.05 * ((succ.astype(float) - ph)[:, None] * ma) * act_
        sig += P["skill_gain"] * ma * (1 - sig) * act_            # skill grows with practice in a color's ways
        if CU_ON:   # C2: understanding keeps into later life (Blue skill fades more slowly from cu_age); C3 reads its growth
            sg0_ = sig[:, 1].copy()
            sig -= P["skill_fade"] * (sig - 0.3) * (1 - ma) * np.where((np.arange(C) == 1)[None] & (age >= P["cu_age"]),
                                                                       1 - P["cu_keep"], 1.0)
        else:
            sig -= P["skill_fade"] * (sig - 0.3) * (1 - ma)           # and fades back toward a beginner's level without it
        if RP_ON:   # role_practice: the ways of what one holds, at most one act's worth a week
            rw_ = np.einsum("nk,nkc->nc", held * I, prof); rs_ = rw_.sum(1, keepdims=True)
            rw_ = rw_ / np.maximum(rs_, 1.0) * ~dead[:, None]
            sig += P["role_skill"] * P["skill_gain"] * rw_ * (1 - sig) * (black_k()[:, None] if P["black_edge"] else 1.0)
        SE += 0.05 * ma * (succ[:, None] - SE) * act_
        habit = 0.99 * habit + 0.01 * ma * act_
        # v10 memory: how acts in each color's ways went, weighted by stakes; bad memories fade faster than good ones
        mem_s = mem_s * DMS_ + (stakes * succ)[:, None] * ma * act_
        mem_f = mem_f * DMF_ + (stakes * ~succ)[:, None] * ma * act_
        if P["scar_k"]:   # a failure at high stakes can leave a never-again scar in its ways; support heals it faster
            sc_ = ~succ & ~idle & (stakes >= P["scar_min"])
            scar += P["scar_k"] * (stakes * sc_)[:, None] * ma * (1 - scar)
            scar *= 0.5 ** ((1 + support)[:, None] / (52 * P["scar_half"]))

        held_wk = held.copy()
        # ---- 3b. resources and commitments (v4)
        res += act_ * (L["PAY"][s, a] + np.where(succ[:, None], L["WIN"][s, a], L["LOSE"][s, a]))
        ck = L["COMMIT"][s, a]
        if OR_ON and BORN_S_ >= 0:   # F7: the moment a child is born is the birth, however the act goes (a birth named once)
            bn_ = (s == BORN_S_) & ~recon & ~dead
            ck = np.where(bn_, KID, ck)
        cp_ = CP[np.maximum(ck, 0)]
        if BA_ON:   # late births: a choice to have a child of one's own starts one as fertility at that age allows
            cp_ = np.where(BIRTH_O[s, a], cp_ * np.where(female, fert(age, FERT_F), fert(age, FERT_M)), cp_)
        if BAT:   # a batch life event that starts a commitment is the match itself (falling in love, a child is born)
            cp_ = np.where((L["TIER"][s] == 1) & ((ck == CAR) | (ck == PAR) | (ck == KID) | (ck == COM)), 1.0, cp_)
        if CRS_ON:   # F16: any other act that would start one (a faith joined, a partner met in an everyday week) leans too
            cj_ = np.select([ck == PAR, ck == KID, ck == FAI], [0, 1, 2], -1)
            gate_ = (cj_ >= 0) & (CRS_EV[s] < 0)
            if gate_.any():
                cp_ = np.where(gate_, cp_ * np.minimum(1.0, course_q()[ar, np.maximum(cj_, 0)]), cp_)
        if PA_ON:   # F9: a first home together comes with adulthood
            cp_ = np.where(ck == PAR, cp_ * np.interp(age, PA_A, PA_F), cp_)
        ok_ = succ & ~idle
        if OR_ON and BORN_S_ >= 0:
            ok_ = ok_ | bn_
        fi = np.nonzero((ck >= 0) & ok_ & ~recon & (rng.random(N) < cp_))[0]
        fk = ck[fi]; new = ~held[fi, fk]
        if BAT:   # R15: a later child born (or taken in) while there are children already is one more living child
            kb_ = (ck == KID) & ok_ & ~recon & (L["TIER"][s] == 1) & kid_on
            alive[kb_, 5] += 1; kid_last[kb_] = t
            birth_log.extend((int(n), t, L["names"][s[n]], L["labels"][s[n]][a[n]]) for n in np.nonzero(kb_)[0])
        fi, fk = fi[new], fk[new]
        birth_log.extend((int(n), t, L["names"][s[n]], L["labels"][s[n]][a[n]]) for n in fi[fk == KID])
        held[fi, fk] = True; I[fi, fk] = 0.2; sat[fi, fk] = 0.6; since[fi, fk] = t
        if RE_ON:   # F8: going back to work, by their own pick, ends the retirement (one work status)
            retired[fi[fk == CAR]] = False
        # what a commitment expects of you: partly the way you entered it, partly who you were then, partly the
        # people and place it belongs to (a job or a partner brings their own ways)
        pm = P["commit_mix"]; prof[fi, fk] = pm[0] * ma[fi] + pm[1] * w[fi] + pm[2] * nic[fi]
        for n, kk in zip(fi, fk):
            commit_log.append((int(n), t, int(kk), "start", prof[n, kk].round(2).tolist(), 0.2))
            if n in events:
                events[n].append(dict(commitment=dict(age=round(age, 2), kind=KNAMES[kk], what="start",
                                                      through=L["labels"][s[n]][a[n]], profile=prof[n, kk].round(2).tolist())))
        # living a commitment: its own situations shape satisfaction and strength; holding it is an investment
        upd = (L["DOM"][s] >= 0.7) & held & (~idle)[:, None] & ~recon[:, None]
        sat = np.where(upd, sat + 0.05 * (succ[:, None] - sat), sat)
        I = np.where(upd, _uclip(I + np.where(succ[:, None], 0.02, -0.02), 0.05, 1), I)
        grow_ = held.copy()
        if age < P["faith_own_age"]:
            grow_[:, FAI] &= ~faith_given                   # the family's faith, not yet one's own
        I = np.where(grow_, I + P["invest"] * (1 - I), I)
        if len(ri):
            ch, ok = a[ri], succ[ri]
            sel = ch == 0                                    # recommit, and talk yourself back into it
            rs = ri[sel & ok]
            dy_ = P["rationalise"] * (centre(np.log(prof[rs, rkk[sel & ok]] + 0.02)) - y[rs])
            y[rs] += dy_; asrc[rs, 5] += dy_
            I[ri[sel], rkk[sel]] = _uclip(I[ri[sel], rkk[sel]] + np.where(ok[sel], 0.15, -0.05), 0.05, 1)
            sat[ri[sel & ok], rkk[sel & ok]] = 0.7
            sel = (ch == 1) & ok                             # reshape it toward the want
            prof[ri[sel], rkk[sel]] = 0.6 * prof[ri[sel], rkk[sel]] + 0.4 * m[ri[sel], 1]; sat[ri[sel], rkk[sel]] = 0.6
            clash_by[ri, rkk] = np.where(ch < 3, ch, clash_by[ri, rkk])
            sel = (ch == 2) & ok                             # walk away
            end(ri[sel], rkk[sel], "left", t)
            stress[ri[(ch == 2) & ~ok]] += 0.2
        # endings nobody chooses: retirement, widowhood (inside a bereavement), job loss (inside a betrayal)
        if P["retire_hz"] is None:                           # the old rule: from pension age, about two years on average
            ret = held[:, CAR] & (age >= P["retire_age"]) & (rng.random(N) < 0.01)
        else:                                                # early or late: health, means and fit decide who goes when
            ra_, rh_ = np.asarray(P["retire_hz"], float).T
            mx_ = P["retire_means"] * (1.0 if age < P["retire_age"] else 1 / 3)
            h_ = (np.interp(age, ra_, rh_) * np.exp(P["retire_health"] * (0.7 - res[:, HEA]))
                  * _uclip(res[:, MON] / 0.2, 0.25, 4.0) ** mx_ * (1 + P["retire_misfit"] * misfit[:, CAR]))
            ret = held[:, CAR] & (rng.random(N) < h_ / 52)
        if RE_ON:   # F8: a job just taken (back from retirement, or any) is not retired from in its first weeks
            ret = ret & (t - since[:, CAR] >= P["retire_back"])
        if RET_SEA:   # retiring opens the later-life season, whose first step is the last day at work
            ret = ret & (ret_pend < 0)
            for n in np.nonzero(ret & ~sea_had[:, ELD_])[0]:
                if sea_fits(ELD_, age):
                    sea_open(n, ELD_); ret_pend[n] = t; ret[n] = False
            ret_pend[(ret_pend >= 0) & ~held[:, CAR]] = -1
            late_ = (ret_pend >= 0) & (t - ret_pend > 8)          # the day never came as a moment: retired all the same
            ret = ret | late_; ret_pend[late_] = -1
        end(np.nonzero(ret)[0], [CAR] * int(ret.sum()), "retired", t)
        if P["faith_drift"] is not None and age >= P["faith_own_age"]:   # a faith or cause that quietly stops mattering
            fa_, fh_ = np.asarray(P["faith_drift"], float).T
            hf_ = (np.interp(age, fa_, fh_) * np.exp(P["faith_tilt_k"] * ((w - 1 / C) @ np.asarray(P["faith_tilt"], float)))
                   * _uclip(1.2 - I[:, FAI], 0.1, 1.2))
            dr_ = held[:, FAI] & ~recon & (rng.random(N) < hf_ / 52)
            drift_now[:] = dr_
            end(np.nonzero(dr_)[0], [FAI] * int(dr_.sum()), "left", t)
            drift_now[:] = False
        wid = WID_ON & held[:, PAR] & (rng.random(N) < 0.005 * np.exp((age - 55) / 10) / 52)   # partner dies (yearly risk 0.5% at 55, 6% at 80)
        widowed |= wid; hz_mem[wid] += P["hz_remind"] * HZ_ROLE[-1]
        need[wid, NIDX["belonging"]] -= 0.4; stress[wid] += 0.5
        end(np.nonzero(wid)[0], [PAR] * int(wid.sum()), "widowed", t)
        # resources drift toward what a life's commitments and age provide
        mt = P["money_base"] + 0.45 * held[:, CAR] * (0.4 + 0.6 * I[:, CAR]) + P["pension_k"] * pension - P["kid_cost"] * kids
        if P["pension_base"] and age >= P["retire_age"]:   # F9: the state pension
            mt = mt + P["pension_base"]
        if LP_ON:   # F9.38: a new job's pay, drawn once (a change of employer draws again, rho of it the last job's)
            nj_ = np.nonzero(held[:, CAR] & (ago["job"] != lp_at))[0]
            if len(nj_):
                r_ = np.where(lp_at[nj_] == NEVER, 0.0, lp_rho)
                lp_z[nj_] = r_ * lp_z[nj_] * lp_d[nj_] + np.sqrt(1 - r_ ** 2) * lp_rng.standard_normal(len(nj_))
                lp_d[nj_] = 1.0; lp_at[nj_] = ago["job"][nj_]
                if PC_ is not None:   # F9.40: the colours lean the new job's pay and its spread
                    lc_ = 5 * w[nj_] - 1
                    lp_mu[nj_] = lc_ @ PC_[0]; lp_sc[nj_] = np.exp(lc_ @ PC_[1])
            sd_ = lp_sd * lp_sc * lp_d
            mt = mt + 0.45 * held[:, CAR] * (0.4 + 0.6 * I[:, CAR]) * (np.exp(lp_mu + sd_ * lp_z - sd_ ** 2 / 2) - 1)
            lp_d *= 0.5 ** (1 / (52 * lp_half))
        if PRP_ON and age >= 18:   # F9.38: a couple that lives together shares its money: a working partner's pay
            tog_ = r_has[:, CO_T_].any(1) if len(CO_T_) else held[:, PAR]
            if WON:   # the partner in the cast, at work
                ps_ = np.asarray(WL.PP.pslot); tog_ = tog_ & (ps_ >= 0) & np.asarray(WL.PP.emp)[np.arange(N), np.maximum(ps_, 0)]
            mt = mt + P["pair_pay"] * (tog_ & held[:, PAR])
        tt = 0.15 + 0.3 * held[:, PAR] + 0.15 * held[:, KID] + 0.25 * held[:, COM] + 0.1 * held[:, CAR]
        if HH_ON or TP_ON:   # F3: the household's money until they live on their own; ties are the people around them
            own_, away_ = home_share(age)
            if HH_ON:
                hh_lv_, hh_fl_ = household(age)
                mt = (1 - own_) * hh_lv_ + own_ * mt
            if TP_ON:
                tt = np.asarray(WL.PP.ties, float) if WON else ties_off(age, away_)
                if WON and P["tie_k"] != 1.0:   # F9: the people's closeness as ties, read on a scale (k = 20 / the T used)
                    tt = 1 - (1 - tt) ** (P["tie_k"] * (np.exp((5 * w - 1) @ TC_) if TC_ is not None else 1.0))
                if WON and P["kid_tie"] is not None and age < 15:   # F9.39: a child's ties are first its family's
                    tt = np.maximum(tt, P["kid_tie"])
        ht = _uclip(1 - 0.012 * max(0.0, age - 35), 0.2, 1)
        if MK_ON:   # spheres phase 2, the mark of the work: hard work ages the body (years beyond its own)
            ht = _uclip(ht - 0.012 * np.asarray(WL.PP.mark_wear, float), 0.2, 1)
        ft = FREE_STAGE[stage] - 0.1 * kids - 0.05 * held[:, PAR]
        if RON:   # a title's own resources: a nurse's pay, the freedom a record takes
            tr_ = (r_has[:, :NT_] * np.where(TK_ < NK, 0.4 + 0.6 * I[:, np.minimum(TK_, NK - 1)], 1.0)) @ GR["meets_res"]
            mt = mt + tr_[:, MON]; tt = tt + tr_[:, TIE]; ht = ht + tr_[:, HEA]; ft = ft + tr_[:, FRE]
        if WON:   # the world: rents, prices, the welfare floor, rights (package §5, Resources)
            wm_, wf_ = WL.resources(held[:, CAR]); mt = mt + wm_; ft = ft + wf_
            if WFX_ON:   # the money and freedom a life drifts to, by the world's cause
                rp_ = WL.resources_parts(held[:, CAR])
                wfx_track("money", {k_: rp_[k_] for k_ in ("housing", "prices", "welfare")}, age, dead)
                wfx_track("freedom", {"rights": rp_["rights"]}, age, dead)
            if WL2_ON:   # WL2: the small effects, each charged once (spheres-implementation.md "One cost, one place")
                w2_ = WL.wl2_parts(held[:, CAR])
                mt = mt + w2_["prices_work"] + w2_["recession"] + w2_["disaster"]
                ft = ft + w2_["rec_hours"] + w2_["disaster_time"]; tt = tt + w2_["pandemic"]
                if WFX_ON:
                    wfx_track("money", {k_: w2_[k_] for k_ in ("prices_work", "recession", "disaster")}, age, dead)
                    wfx_track("freedom", {k_: w2_[k_] for k_ in ("rec_hours", "disaster_time")}, age, dead)
                    wfx_track("ties", {"pandemic": w2_["pandemic"]}, age, dead)
        if DB_ON:   # phase 5: holdings yield, a home saves the rent, debts' payments take their share of income
            d_inc[:] = np.maximum(mt, 0.02)
            hm_ = (hk == 0).any(1)
            # a home of their own: .05, plus the rent a renter of that household would pay (world_link's "housing" read as
            # if own_home were false; for a life the world already charges, that charge ends), less the loan's payment
            rent_ = -0.05 * float(_uclip(WL.W.housing, -1, 1))
            mt = mt - rent_ * hm_ + 0.05 * hm_ + np.where(hk >= 0, H_YV[np.maximum(hk, 0)], 0.0).sum(1) * d_inc
            ds_ = np.where(dk >= 0, dsz / dterm + drate * dbal / 12, 0.0).sum(1)
            mt = mt * (1 - np.minimum(ds_, 0.9))
            pd_ = (WL.deaths()[:, 0] > 0) & (np.asarray(WL.PP.alive)[:, 0] == 0) & ~dead
            if H_OK[0] and age >= 16 and pd_.any():
                for n in np.nonzero(pd_)[0]:
                    db_inherit(n)
        if HH_ON:   # F3 D2: the family is a floor in hard times, by its class and how close a living parent is
            mt = np.maximum(mt, P["hh_floor"] * hh_fl_)
        tie_r = 0.01
        if LON_ON and age >= LA_[0]:   # F9.39: a spell of loneliness starts or ends; while it lasts the ties fall away
            rk_ = (LO_["single"] * ~held[:, PAR] + LO_["work"] * (~held[:, CAR] & ~retired & (ago["job"] != NEVER)) * (age < P["retire_age"])
                   + LO_["low"] * (md_end[:, 0] > t) + LO_["ill"] * (bd_cw.sum(1) > 0))
            u_ = lon_rng.random(N)
            on_ = ~lone & ~dead & (u_ < float(np.interp(age, LA_, LF_)) * np.exp(rk_) / 52)
            lone = (lone | on_) & ~(lone & (u_ < LO_["out"] * np.exp(-0.5 * rk_) / 52))
            tt = np.where(lone, LO_["keep"] * tt, tt); tie_r = np.where(lone, LO_["rate"], 0.01)
        mon_r = P["mon_drift"]
        if P["job_gap"] is not None and age >= 18 and age < P["retire_age"]:   # F9.38: a lost wage stops at once
            gp_ = (~held[:, CAR] & ~retired & (ago["job"] != NEVER) & (end_t[:, CAR] > NEVER // 2)
                   & (t - end_t[:, CAR] < 52 * P["job_gap"][2]))
            mt = mt - P["job_gap"][0] * gp_
            mon_r = np.where(gp_ & (mt < res[:, MON]), P["job_gap"][1], P["mon_drift"])
        res[:, MON] += mon_r * (mt - res[:, MON]); res[:, TIE] += tie_r * (tt - res[:, TIE])
        if DB_ON and t % 4 == 0 and age >= 18:
            db_month()
        if HM_ON:   # v22.5 F1: the body and the mind make health (ht's age part is the body's own curve there)
            body_week(ht, _uclip(1 - 0.012 * max(0.0, age - 35), 0.2, 1))
        else:
            res[:, HEA] += 0.01 * (ht - res[:, HEA])
        res[:, FRE] += 0.02 * (ft - res[:, FRE])
        res[:, HEA] -= 0.08 * ((stakes >= 1.3) & ~succ & ~idle)       # disasters that go wrong hurt the body
        if SHON:   # shadows: rigid and ruthless lose people, reckless burns bridges and the body pays, rigid strains on duty
            res[:, TIE] -= 0.01 * P["sh_tie"] * (shA[:, 0] + shA[:, 2] + 0.5 * shA[:, 3])
            res[:, HEA] -= 0.01 * P["sh_body"] * shA[:, 3]
            stress += P["sh_strain"] * shA[:, 0]
            dsc -= P["sh_burn"] / 52 * shA[:, 3] * (dsc - P["disc_range"][0])
            # the four sources (shadows-mechanics.md §3), each 0 to 1
            a_w_ = softmax(y)
            sh_src[:, :, 0] = _uclip(2.5 * (hold - 0.2), 0, 1) * _uclip(5 * (w - a_w_), 0, 1) \
                * _uclip((t - sh_brk) / 52.0, 0, 1)[:, None]                 # holding on (a breakthrough lets go for a while)
            sh_src[:, :, 1] = _uclip((w - 0.30) / 0.30, 0, 1)                   # ruling
            en_max_ = np.where(ENEMY_B[None], w[:, None, :], 0.0).max(2)       # the stronger of its two enemies
            sh_src[:, :, 2] = _uclip((0.12 - en_max_) / 0.09, 0, 1)             # no counterweight
            sh_src[:, :, 3] = _uclip(stress / 1.5 + Q / 4, 0, 1)[:, None] * w / w.max(1, keepdims=True)   # strain
            sk_ = np.asarray(P["sh_src"], float)
            tgt_ = 1 - np.prod(1 - sk_[None, None] * sh_src, 2)
            if SHAR_ON and getattr(WL.PP, "sh_around", None) is not None:   # phase 5: the shadow around them (N5)
                sa_ = _uclip((np.asarray(WL.PP.sh_around, float)[:, np.argsort(WL.W.perm)] - 0.1) / 0.4, 0, 1)
                tgt_ = 1 - (1 - tgt_) * (1 - P["sh_around"] * sa_)
            if LW_ON:   # S7: years leading one way add to that colour's shadow part (People.lead_sh, 0 .. lead_par sh)
                tgt_ = 1 - (1 - tgt_) * (1 - np.asarray(WL.PP.lead_sh, float)[:, np.argsort(WL.W.perm)])
            sup_ = np.clip(0.5 * (need[:, NIDX["belonging"]] + res[:, TIE]), 0, 1)
            integ_ = np.where(ENEMY_B[None], J, 0.0).max(2)                    # an enemy pair held well
            tgt_ = tgt_ * (1 - P["sh_care"] * sup_)[:, None] * (1 - P["sh_integ"] * integ_) * (age >= P["sh_age"])
            tgt_ = np.clip(tgt_ * SHG_[None], 0, 1)
            up_ = tgt_ > shS                                                   # shadows come faster than they go
            shS += (tgt_ - shS) / (4.33 * np.where(up_, P["sh_grow"], P["sh_fade"]))
            if pausing and not recon.all():   # the Voice leads them out: the shadow pulled the character's own pick, the
                # player picked another way, and it worked
                ctr_ = (a != a_self) & succ & ~idle & ~recon
                for n in np.nonzero(ctr_)[0]:
                    pu_ = shA[n] * m[n, a_self[n]]
                    c_ = int(pu_.argmax())
                    if pu_[c_] > 0 and m[n, a[n], c_] < m[n, a_self[n], c_]:
                        shS[n, c_] = max(0.0, shS[n, c_] - P["sh_counter"])
            rf_ = SH_REFL[s]                                                   # a reflection moment met: they see it
            for n in np.nonzero((rf_ >= 0) & ~recon)[0]:
                c_ = int(rf_[n]); shS[n, c_] = max(0.0, shS[n, c_] - P["sh_seen"]); sh_seen[n, c_] = True; sh_rt[n, c_] = t
            shA = np.minimum(1.0, w * shS / P["sh_full"])
        res = _uclip(res, 0, 1)
        # clash: holding a commitment that no longer fits what you want. It costs stress until it is resolved
        mis = _uclip(1 - 5 * (prof * softmax(y)[:, None, :]).sum(-1), 0, 1)
        on = held & (clash0 < 0) & (mis > P["clash_on"])
        clash0[on] = t; clashI[on] = I[on]; clash_by[on] = -1
        cload = (held * (clash0 >= 0) * mis * I).sum(1)         # living against what you are supposed to be (ought conflict)
        stress += P["clash_stress"] * cload
        done = (clash0 >= 0) & (~held | (mis < P["clash_off"]))
        for n, kk in zip(*np.nonzero(done)):
            how = "left" if not held[n, kk] and clash_by[n, kk] == 2 else "ended otherwise" if not held[n, kk] else \
                  {0: "doubled down", 1: "reshaped it"}.get(int(clash_by[n, kk]), "made peace")
            clash_log.append((int(n), int(kk), int(clash0[n, kk]), t, how, round(float(clashI[n, kk]), 2), int(np.argmax(softmax(z[n])))))
            if n in events:
                events[n].append(dict(clash=dict(kind=KNAMES[kk], start=round(clash0[n, kk] / 52, 1), end=round(age, 1), how=how)))
        clash0[done] = -1

        # ---- 3c. v7 goals: steps taken, strength, meaningful success, plans reached
        if GON:
            ra = rel[ar, :, a]                                       # N,G: how far this week's act served each goal
            acted = (~idle)[:, None] & (gk >= 0) & (ra > 0)
            win_ = acted & succ[:, None]; fail_ = acted & ~succ[:, None]
            st_ = np.minimum(stakes, 1.2)[:, None]
            gs = np.where(win_, gs + np.where(gk == 0, P["g_up_dream"], P["g_up"]) * ra * st_ * (1 - gs), gs)
            gs = np.where(fail_, gs - P["g_down"] * ra * st_ * (1.5 - outlook)[:, None] * gs, gs)
            gpk = np.maximum(gpk, gs)
            glast = np.where(acted, t, glast)
            # tries that work and feel like one's own gather toward a passion (2A)
            own_g = 0.5 * (w + softmax(y))
            conc_a = _uclip(2 * (ma * own_g).sum(1) / own_g.max(1) - 1, -0.5, 1)
            # only real tries count: an act clearly in its ways, in a moment that mattered, that felt like one's own
            dv = win_ * (gk <= 1) * (ra >= 0.5) * ra * _uclip((stakes - 0.4) / 0.4, 0, 1)[:, None] * np.maximum(conc_a, 0)[:, None]
            gv = gv + dv
            # taken in freely or under pressure? Parents prizing it (childhood), needing it for one's worth, being only about
            # this one thing, against support and room to choose (Mageau et al. 2009): harmonious or obsessive passion
            lk_ = np.maximum(0, P["need_set"] - need) / P["need_set"]
            dp_ = (gk <= 1) * (gk >= 0) * gs; spec = dp_ / np.maximum(dp_.sum(1, keepdims=True), 1e-9)
            ctl = (P["ctl_fam"] * _uclip(5 * np.einsum("nc,ngc->ng", fam, gm) - 1, 0, 2) * (stage <= 1)[:, None]
                   + P["ctl_lack"] * 0.5 * (lk_[:, NIDX["competence"]] + lk_[:, NIDX["meaning"]])[:, None] + P["ctl_spec"] * spec
                   - P["ctl_sup"] * (support - 0.5)[:, None] - P["ctl_free"] * (res[:, FRE] - 0.5)[:, None]
                   + P["ctl_stress"] * (stress - 0.5)[:, None] + P["ctl_press"] * (0.5 * np.abs(nic - w).sum(1) - 0.15)[:, None]
                   + P["ctl_react"] * (react - 1)[:, None])
            auto_now = 1 / (1 + np.exp(-(P["ctl_mid"] - 4 * ctl)))   # stress and pressure to be someone else make it compulsive
            ga = np.where(dv > 0, ga + 0.5 * dv / (1 + gv) * (auto_now - ga), ga)   # set while it is taken in, then settles
            # a passion lived lifts the mood when harmonious, much less when obsessive (Vallerand et al. 2003)
            mood = mood + P["hp_mood"] * (((gk == 1) & win_) * gs * ra * (ga - 0.5 * (1 - ga))).sum(1)
            # plans: progress and what has been put in
            pln = gk == 2
            # a pursuit moves on deliberate steps: they take self-control and free time (busy, stressed weeks get less done)
            gp = np.where(pln & win_ & (gd < 0), gp + ra * st_ * (ctrl * (0.3 + 0.7 * res[:, TIM]))[:, None]
                          / np.asarray(P["g_size"], float)[ghz], gp)
            gp = np.where(pln & win_ & (gd >= 0), np.minimum(0.95, gp + 0.1 * ra), gp)
            gi = np.where(pln, gi + 0.005 * gs + 0.05 * acted * st_, gi)
            # what the person learns about their chances: how often one comes, and how a step looks to them
            chance = (rel >= 0.5).any(2)
            gch = np.where(pln, gch * (1 - 1 / 52) + chance / 52, gch)
            gph = np.where(pln & chance, 0.9 * gph + 0.1 * np.where(rel >= 0.5, p_hat[:, None, :], 0).max(2), gph)
            # reached: the steps add up, or the commitment the plan was for begins
            newk = held & ~held_wk
            got = pln & (gtt < 0) & (((gd < 0) & (gp >= 1)) | ((gd >= 0) & newk[ar[:, None], np.maximum(gd, 0)]))
            if RON:   # a plan aimed at a title is reached when the title is held
                got |= pln & (gtt >= 0) & r_has[ar[:, None], np.maximum(gtt, 0)]
            for n, j in zip(*np.nonzero(got)):
                cc = float(_uclip(2 * (gm[n, j] * own_g[n]).sum() / own_g[n].max() - 1, -0.5, 1))
                fit_ = 0.5 + 0.5 * max(cc, 0)    # reaching what fits who one is means more (Sheldon & Elliot 1999)
                need[n, NIDX["meaning"]] += 0.15 * gs[n, j] * fit_; need[n, NIDX["competence"]] += 0.1 * gs[n, j]
                mood[n] += 0.3 * gs[n, j] * fit_
                outlook[n] += 0.1 * (1 - outlook[n]) * TON; steady[n] += 0.05 * fit_ * TON
                if gpar[n, j] >= 0:
                    gs[n, gpar[n, j]] = min(1.0, gs[n, gpar[n, j]] + 0.1)
                gp[n, j] = 1.0
                end_goal(n, j, "achieved")

        # ---- 4. learning channels
        pos = delta > 0
        lens_ = w if not P["lens_want"] else (1 - P["lens_want"]) * w + P["lens_want"] * softmax(y)   # lens_want: and who one is becoming
        kap = ma * lens_ ** P["rho"]; kap /= kap.sum(1, keepdims=True) + 1e-12
        defend = P["defend_k"] * (ma * w).sum(1) / w.max(1) * (M / (M + P["M0"]))   # experienced people discount failures in what they hold
        # v6 (Library notes A5): a failure sends the person toward what the situation called for, the colors whose
        # argument it proved right, not evenly toward everything else they hold
        called = np.maximum(alpha - alpha.mean(1, keepdims=True), 0)
        called = np.where(called.sum(1, keepdims=True) > 1e-9, called / np.maximum(called.sum(1, keepdims=True), 1e-9), w)
        # Only big failures in one's own strongest ways do this (the flaw shows where life pushes back)
        ff = P["fail_fit"] * _uclip((stakes - 0.7) / 0.5, 0, 1) * _uclip((ma * w).sum(1) / w.max(1), 0, 1)
        away = (1 - ff[:, None]) * w + ff[:, None] * called
        dI = np.where(pos[:, None], P["eta"] * ldelta[:, None] * (kap - w),
                      P["eta"] * ldelta[:, None] * (1 - defend)[:, None] * (ma - away))
        if P["unusual_k"]:   # v6 (Bardi & Schwartz 2003): doing what everyone around you does says little about you
            typ = (ma * nic).sum(1) / (nic * nic).sum(1)
            dI *= _uclip(1 + P["unusual_k"] * (1 - typ), 0.5, 2.0)[:, None]
        dI[idle] = 0
        if P["own_k"] != 1.0:   # played lives: the game weighs the character's own weekly lesson
            dI = P["own_k"] * dI
        dD = np.where(pos[:, None], -ldelta[:, None] * ma, -ldelta[:, None] * defend[:, None] * ma) - P["slack"] * ma
        dD[idle] = 0
        D = np.maximum(0, D * (1 - P["D_decay"]) + dD)

        # needs: drain weekly; your niche supplies some; successful acts meet the needs
        # their ends serve; acting against a value's ends drains the needs it meets. Only the act's own ends
        # drain needs: a world that frames colors as opposed adds inner tension (peace), not deprivation (v4)
        if NM_ON:   # P4: through each person's own table
            need += -P["need_drain"] + P["need_drain"] * 0.7 * 5 * np.einsum("njc,nc->nj", NMP, nic)
            room = (1 - need) if P["satiate"] else 1.0
            need += 0.12 * np.maximum(stakes, P["need_floor"])[:, None] * np.where(succ[:, None], np.einsum("njc,nc->nj", NMP, np.maximum(ea, 0)), 0) * act_ * room
            need += 0.06 * np.einsum("njc,nc->nj", NMP, np.minimum(ea0, 0)) * act_
            # the table moves (§1): an act that worked feeds what lacked most, through its colours (one that failed, the
            # reverse, at half); habit ties the colours used to what lacks; held goals tie theirs to their domain's needs
            ep_ = np.maximum(ea, 0); sg_ = np.where(succ, 1.0, -0.5) * stakes * (~idle)
            dNM = P["nm_lr_moment"] * sg_[:, None, None] * (lack - lack.mean(1, keepdims=True))[:, :, None] * ep_[:, None, :]
            dNM += P["nm_lr_habit"] * lack[:, :, None] * (ma - 0.2)[:, None, :] * act_[:, :, None]
            gw_ = gs * (gd >= 0)
            if gw_.any():
                dNM += P["nm_lr_goal"] * np.einsum("ng,ngj,ngc->njc", gw_, KPAY[np.maximum(gd, 0)], gm - 0.2)
            NMP = NMP + dNM * (NMAP > 0)[None] + (NMAP[None] - NMP) * (np.log(2) / (52 * P["nm_back"]))
            NMP = np.clip(NMP, NM_LO[None], NM_HI[None])
            NMP = NMP * (NM_TOT / np.maximum(NMP.sum(1), 1e-9))[:, None, :]     # each colour's column keeps its total
        else:
            need += -P["need_drain"] + P["need_drain"] * 0.7 * 5 * (nic @ NMAP.T)
            room = (1 - need) if P["satiate"] else 1.0    # v6: a need that is nearly met gains less from each act (satiation)
            need += 0.12 * np.maximum(stakes, P["need_floor"])[:, None] * np.where(succ[:, None], np.maximum(ea, 0) @ NMAP.T, 0) * act_ * room   # v6: quiet weeks meet needs too
            need += 0.06 * (np.minimum(ea0, 0) @ NMAP.T) * act_
        if P["disc_win"]:   # v7 discipline: a hard thing done on purpose (the act the person meant, against the odds), most
            hw_ = tried & succ & (p_true < 0.4)          # formative in childhood as temperament is; slowly drifts back to even
            dsc[hw_] += P["disc_win"] * TST[stage[hw_]] / TST[2] * (P["disc_range"][1] - dsc[hw_])
            dsc += (1 - dsc) * (1 - 0.5 ** (1 / (52 * P["disc_back"])))
        if P["aut_self"]:   # v6: acting as oneself meets autonomy; acting against oneself drains it a little
            own_ = 0.5 * (w + softmax(y))
            concord = _uclip(2 * (ma * own_).sum(1) / own_.max(1) - 1, -0.5, 1)   # 1 = in one's strongest color, 0 = at half of it
            need[:, NIDX["autonomy"]] += P["aut_act"] * concord * (~idle) * np.where(concord > 0, room[:, NIDX["autonomy"]] if P["satiate"] else 1, 1)
            # competence: succeeding at what was hard for you, in any color; failing drains it a little
            need[:, NIDX["competence"]] += P["comp_act"] * np.where(succ, (0.5 + (1 - p_true)) * (room[:, NIDX["competence"]] if P["satiate"] else 1), -0.3 * appf_) * (~idle)
        if CU_ON:   # a curious, thinking life (item 7): its own goods
            ln_ = ma[:, 1] * (1 - sg0_) * (~idle)                        # C3: learning in Blue's ways, worked or not
            need[:, NIDX["meaning"]] += P["cu_learn"] * ln_; need[:, NIDX["autonomy"]] += 0.5 * P["cu_learn"] * ln_
            late_ = _uclip((age - 55) / 10, 0, 1) * np.maximum(sig[:, 1] - 0.3, 0)   # C2: understanding pays late
            need[:, NIDX["competence"]] += P["cu_late"] * late_; need[:, NIDX["meaning"]] += 0.5 * P["cu_late"] * late_
            ask_on_ = (age >= 35) & (sig[:, 1] > 0.55) & (w[:, 1] > 0.22)  # C4: the one people ask
            asked += P["cu_ask_rate"] * np.where(ask_on_, 1 - asked, -0.1 * asked)
            ak_ = P["cu_ask"] * asked * (age >= 50)
            need[:, NIDX["belonging"]] += ak_; need[:, NIDX["meaning"]] += ak_
        duty_ = np.minimum(1, (held * I) @ DUTY)                      # needs of those the person answers for
        served = ((np.maximum(ea, 0) @ NMAP.T) * duty_).sum(1)
        need[:, NIDX["meaning"]] += P["duty_mean"] * served * succ * (~idle) * (room[:, NIDX["meaning"]] if P["satiate"] else 1)
        # v6: tension rebounds both ways (Emren 22:46). An act that joins colors the world reads as opposed is a bet on
        # holding both: when it works the two fit together (integration, meaning, calm); when it fails the split hurts
        # (integration loosens, stress). The more the person holds both, the bigger the stakes
        span = np.einsum("ni,ij,nj->n", ma, FRpos, ma) * (~idle) * (1 + 4 * np.einsum("ni,nij,nj->n", w, FRpos[None] * (1 - J), w))
        if P["ten_good"] or P["ten_bad"]:
            need[:, NIDX["meaning"]] += P["ten_good"] * span * succ * (room[:, NIDX["meaning"]] if P["satiate"] else 1)
            stress += P["ten_bad"] * span * ~succ
        reb += np.stack([span * succ, span * ~succ], 1)
        # v6 (Library notes C1, A2): a big event that goes badly feeds later trouble and leaves the person open for months;
        # one that goes well feeds later fortune (Hobfoll's loss and gain spirals)
        big = had_ev & (s == s_ev) & ~idle if P["base_rates"] else np.zeros(N, bool)
        dec = np.exp(-1 / (52 * P["clust_years"]))
        trouble = trouble * dec + big * np.maximum(-fdelta, 0)
        fortune = fortune * dec + big * np.maximum(fdelta, 0)
        wound = wound * np.exp(-1 / (52 * P["wound_years"])) + big * np.maximum(-fdelta, 0)
        B += P["ev_open"] * big * np.abs(delta)   # v6 (Bardi et al. 2009): big events, good or bad, open a person to change
        if BAT:
            # ---- 3d. the Library's batch: what this week leaves in the person's history
            live_ = ~recon
            sit_last[ar[live_], s[live_]] = t
            fs_ = sit_first[ar[live_], s[live_]] <= NEVER // 2
            sit_first[ar[live_][fs_], s[live_][fs_]] = t
            on_ = ONCE[s] & live_
            once_done[ar[on_], ROOT[s[on_]]] = True       # a child version and its original are one event (variant_of)
            if RON:   # the act's titles and perks: becoming a nurse, a licence taken (on success; the _if_fails fields on failure)
                for n in np.nonzero(GR["A_HASFX"][s, a] & ~idle & live_)[0]:
                    for op_, j0_, yrs_ in GR["A_FX"][(int(s[n]), int(a[n]))]["ok" if succ[n] else "fail"]:
                        if j0_ == LONG_ and not succ[n]:
                            continue                           # [a long shot that missed]: only after a real long shot, below
                        for j_ in fx_targets(n, int(s[n]), j0_):
                            r_act(n, op_, j_, yrs_, "through " + L["labels"][s[n]][a[n]], ma[n])
                if C5F_ >= 0 and WL is not None:   # C5: "a following of your own" taken and working founds the movement in
                    # their town: its colours become the founder's own, its growth scales with their reach (ties .8 is 1)
                    for n in np.nonzero((GR["A_TITLE"][s, a] == C5F_) & succ & ~idle & live_)[0]:
                        WL.W.c5_found_by(np.asarray(w[n], float)[WL.W.perm], reach=float(res[n, TIE]) / 0.8)
                at_l = missed_at(GR["A_TITLE"][s, a], s, a)    # a failed try for a title at true odds under long_shot: a long shot
                for n in np.nonzero(long_miss)[0]:              # that missed, whatever the option names (election night with no
                    if at_l[n] >= 0:                          # nomination, the part of a lifetime for an unknown); packs 08:02
                        missed_t[n] = at_l[n]
                    if LONG_ >= 0:
                        r_gain(n, LONG_, "through " + L["labels"][s[n]][a[n]] + (" (missed: " + GR["names"][at_l[n]] + ")"
                                                                                 if at_l[n] >= 0 else ""), ma[n])
                for n in np.nonzero(GR["S_HASFX"][s] & live_)[0]:   # the moment itself gives it (going into foster care)
                    for op_, j0_, yrs_ in GR["S_FX"][int(s[n])]:
                        for j_ in fx_targets(n, int(s[n]), j0_):
                            r_act(n, op_, j_, yrs_, "through " + L["names"][s[n]], None)
                for n in np.nonzero(RETIRES_[s] & live_ & held[:, CAR])[0]:   # the last day at work: the career ends here
                    end([n], [CAR], "retired", t); ret_pend[n] = -1
                if AD_ON:   # a risky act that fails can end the life (never a child's own act); with self_death off it
                    # leaves the body badly hurt instead
                    # a failure that does not kill can still put the person in hospital: near_ratio times as often as death
                    # (non-fatal overdoses and crash injuries far outnumber deaths); with self_death off, deaths are near
                    # misses too
                    for n in np.nonzero((A_DEATH[s, a] > 0) & ~succ & ~idle & live_ & (age >= 13))[0]:
                        u_ = rid.random(); sh_ = A_DEATH[s[n], a[n]]
                        if u_ < sh_ and P["self_death"]:
                            die(n, "through " + L["labels"][s[n]][a[n]])
                        elif u_ < min(1.0, P["near_ratio"] * sh_):
                            res[n, HEA] = max(0.0, res[n, HEA] - 0.3); stress[n] += 0.5; ago["near_death"][n] = t
                            if n in events:
                                events[n].append(dict(near_death=dict(age=round(age, 2), through=L["labels"][s[n]][a[n]])))
                if AK_ON:   # taking a life (by choice, rarely; never a child's act, never a child): the person is gone,
                    # [has taken a life], and about half are caught: a record, the job lost, prison, then [ex-prisoner]
                    for n in np.nonzero((A_KILL[s, a] != -1) & succ & ~idle & live_ & (age >= 13))[0]:
                        r_ = int(A_KILL[s[n], a[n]])
                        if r_ >= 0 and ROLES[r_] == "partner":
                            if held[n, PAR]:
                                end([n], [PAR], "widowed", t)
                        elif r_ >= 0 and WON:   # the world's cast: that person is gone
                            WL.PP.kill(int(n), ROLES[r_]); alive[n, :5] = WL.PP.alive[n]
                        elif r_ >= 0:
                            alive[n, r_] = max(alive[n, r_] - 1, 0)
                        stress[n] += 1.0; ago["death"][n] = t; ago["loss"][n] = t
                        caught_ = bool(rid.random() < P["kill_caught"])
                        if "has taken a life" in GR["ID"]:
                            r_gain(n, GR["ID"]["has taken a life"], "took a life")
                        if caught_ and EYES_ON_:   # S3: a crime found out, read by their places in the act's colours
                            WL.PP.eyes_see([n], ma[n][None], [0.0], "crime")
                        if caught_:
                            if "someone with a record" in GR["ID"]:
                                r_gain(n, GR["ID"]["someone with a record"], "arrested")
                            if held[n, CAR]:
                                end([n], [CAR], "lost job", t)
                            pris_out[n] = t + int(52 * rid.uniform(*P["kill_prison"]))
                        if n in events:
                            events[n].append(dict(killed=dict(age=round(age, 2), role=ROLES[r_] if r_ >= 0 else "someone",
                                                              through=L["labels"][s[n]][a[n]], caught=caught_)))
                if AKF_ON:   # an act that fails costs someone their life (an overdose nobody stopped): grief, not a crime
                    for n in np.nonzero((A_KILLF[s, a] != -1) & ~succ & ~idle & live_ & (age >= 13))[0]:
                        if A_KILLFS[s[n], a[n]] < 1 and rid.random() >= A_KILLFS[s[n], a[n]]:
                            continue
                        r_ = int(A_KILLF[s[n], a[n]])
                        if r_ >= 0 and ROLES[r_] == "partner":
                            if held[n, PAR]:
                                end([n], [PAR], "widowed", t)
                        elif r_ >= 0 and WON:   # the world's cast: that person is gone
                            WL.PP.kill(int(n), ROLES[r_]); alive[n, :5] = WL.PP.alive[n]
                        elif r_ >= 0:
                            alive[n, r_] = max(alive[n, r_] - 1, 0)
                        stress[n] += 1.0; ago["death"][n] = t; ago["loss"][n] = t
                        if n in events:
                            events[n].append(dict(lost=dict(age=round(age, 2), role=ROLES[r_] if r_ >= 0 else "someone",
                                                            through=L["labels"][s[n]][a[n]])))
                if GON:   # aims: choosing it sets the person's heart on a title: a five-year plan aimed at it (pathways)
                    for n in np.nonzero((GR["A_AIM"][s, a] >= 0) & ~idle & live_)[0]:
                        x_ = int(GR["A_AIM"][s[n], a[n]])
                        if not r_has[n, x_] and not (gtt[n] == x_).any():
                            pf_ = PW_[x_, int(np.argmax(np.where(PMASK_[x_], PW_[x_] @ w[n], -np.inf)))]
                            new_goal(n, 2, pf_ if pf_.sum() > 0 else w[n].copy(), -1, GSRC["resolution"], hz=2, s0=0.6, target=x_)
            newk_ = held & ~held_wk
            for n, kk in zip(*np.nonzero(newk_)):        # a new commitment opens its once-per-commitment events again
                once_done[n, ONCE_K == kk] = False
            # deaths: someone close is gone (the partner's death also ends the partnership, below)
            for r_ in range(len(ROLES)):
                hit_ = np.nonzero((KILLS[s] == r_) & live_)[0]
                if not len(hit_):
                    continue
                hz_mem[hit_] += P["hz_remind"] * HZ_ROLE[r_]
                if ROLES[r_] == "partner":
                    widowed[hit_] = True
                elif not (WON and r_ < 5):   # with the world on, the cast counted it already (a child's is the engine's)
                    alive[hit_, r_] = np.maximum(alive[hit_, r_] - 1, 0)
                if WON and ROLES[r_] == "child":
                    for n in hit_:
                        WL.PP.kill(int(n), "child")
                if ROLES[r_] == "friend" and not WON:   # a new friend in two years (with the world on, the cast makes them)
                    friend_back[hit_] = t + int(2 * 52)
                need[hit_, NIDX["belonging"]] -= KILL_HIT[r_, 0]; stress[hit_] += KILL_HIT[r_, 1]
                ago["death"][hit_] = t; ago["loss"][hit_] = t
                for n in hit_:
                    if n in events:
                        events[n].append(dict(death=dict(age=round(age, 2), role=ROLES[r_], left=int(alive[n, r_]))))
            # endings the event brings: a breakup, a divorce, a death, a lost job
            en_ = np.nonzero((ENDS[s] >= 0) & live_ & held[ar, np.maximum(ENDS[s], 0)])[0]
            if PS_ON and len(en_):   # F9: a breakup moment ends a home together this share of the time (else a rough patch)
                en_ = en_[~(PS_SOFT[s[en_]] & (ps_rng.random(len(en_)) >= P["par_split"]))]
            for n in en_:
                kk = int(ENDS[s[n]])
                end([n], [kk], "widowed" if KILLS[s[n]] == ROLES.index("partner") else "lost job" if kk == CAR else "broke up", t)
            # marks: what the act leaves in the person's history (echoes read them years later)
            mk_ = L["MARK"][s, a]; hm_ = np.nonzero((mk_ >= 0) & ~idle & live_)[0]
            if DR_ON and len(hm_):   # F17: most acts of a rare deed pass; a share by their stakes leaves the mark
                rr_ = DR_M[mk_[hm_]]
                if rr_.any():
                    kp_ = dr_rng.random(len(hm_)) < np.minimum(1.0, P["deed_rare"] * stakes[hm_])
                    hm_ = hm_[~rr_ | kp_]
            if len(hm_):
                jj_ = mk_[hm_]; first_ = mark_n[hm_, jj_] == 0
                mark_first[hm_[first_], jj_[first_]] = t
                mark_last[hm_, jj_] = t; mark_ok[hm_, jj_] = succ[hm_]; mark_n[hm_, jj_] += 1
                heavy_risk[hm_] += (jj_ == MIDX["took a wild risk"]) & (L["BODY"][s[hm_], a[hm_]] >= 1)
                if ID2 and BAT:   # N1b: which trait a mark tells (came out in a moment about one trait tells that one)
                    for n, j_ in zip(hm_, jj_):
                        if j_ == NAMED_K or (j_ == COME_K and CO_SPLIT[s[n]] != 2):
                            if gender_self[n] > 0 and not named_g[n]:
                                named_g[n] = True
                                if j_ != NAMED_K:   # read as named their gender until the Library's marks land
                                    mark_first[n, NAMED_K] = t if mark_n[n, NAMED_K] == 0 else mark_first[n, NAMED_K]
                                    mark_last[n, NAMED_K] = t; mark_ok[n, NAMED_K] = succ[n]; mark_n[n, NAMED_K] += 1
                        if j_ == COME_K and CO_SPLIT[s[n]] != 1:
                            came_o[n] = True
                for n, j_ in zip(hm_, jj_):
                    mark_log.append((int(n), t, int(j_), bool(succ[n])))
                    if n in events:
                        events[n].append(dict(mark=dict(age=round(age, 2), mark=L["MARKS"][j_], worked=bool(succ[n]))))
            # moves: the family moves, or the person moves away or leaves home (and it works)
            mvk = (L["MOVES"][s] & live_) | (((mk_ == MIDX["moved away"]) | (mk_ == MIDX["left home"]) | (mk_ == MIDX.get("came home", -2))) & succ & ~idle & live_)
            mv_own_ = (((mk_ == MIDX["moved away"]) | A_MOVE[s, a]) & succ & ~idle & live_)   # their own move
            if P["far_share"] < 1 and mv_own_.any():   # E6: only some of one's own moves are to a new town (newcomer .93 vs .60)
                mv_own_ &= far_rng.random(N) < P["far_share"]
            mv_fam_ = L["MOVES"][s] & live_
            if P["move_near"] and mv_fam_.any():   # K2: the family's move is to a new town fam_far of the time
                mv_fam_ &= fam_rng.random(N) < MVF_[s]
            mv_far = mv_fam_ | mv_own_   # a new town (newcomer); without move_near the family's move always is one
            mvk = mvk | (A_MOVE[s, a] & succ & ~idle & live_)
            if mvk.any():
                ii_ = np.nonzero(mvk)[0]
                if P["move_near"]:   # K2: a move within the town keeps half the circle (new neighbours, the same friends)
                    kp_ = np.where(mv_far[ii_], 0.0, 0.5)[:, None]
                    circle[ii_] = kp_ * circle[ii_] + (1 - kp_) * random_messages(rng, len(ii_))
                    nic[ii_] = (0.5 + 0.5 * kp_) * nic[ii_] + (0.5 - 0.5 * kp_) * circle[ii_]
                    res[ii_, TIE] = np.maximum(0, res[ii_, TIE] - np.where(mv_far[ii_], 0.2, 0.1))
                else:
                    circle[ii_] = random_messages(rng, len(ii_)); nic[ii_] = 0.5 * nic[ii_] + 0.5 * circle[ii_]
                    res[ii_, TIE] = np.maximum(0, res[ii_, TIE] - 0.2)
                ago["move"][ii_] = t; n_moves[ii_] += 1
                if WON:   # the world: a new place (a far move: another locality; leaving or coming home: nearby)
                    for n in ii_:
                        why_ = "came home" if mk_[n] == MIDX.get("came home", -2) else "left home" if mk_[n] == MIDX.get("left home", -2) else None
                        WL.move(int(n), local=not bool(mv_far[n]), why=why_)
            if WON:   # the world: the close circle judges the act, rank in settings moves, a lever pushes (world-fields.md);
                # a want the moment answered is met or refused; what happened in each logged life's world goes in its events
                for r_ in WL.on_act(~idle & live_ & ~dead, s, a, ma, succ, L, closed_s[ar, a] >= 0 if closed_s is not None else np.zeros(N, bool)):
                    if isinstance(r_, dict) and r_.get("n") in events:
                        events[r_["n"]].append(dict(sphere_lever=r_) if r_.get("kind") == "sphere lever" else dict(world_push=r_))
                    if (DB_ON and isinstance(r_, dict) and r_.get("kind") == "sphere lever" and r_.get("lever") == "found"
                            and r_.get("sphere") in ("prod", "comm") and float(r_.get("went", 0)) >= 0.5):
                        n_ = int(r_["n"])   # a found act that went well founds a workshop or shop, worth a year's income
                        if res[n_, MON] >= DP_["found_lv"] and (hk[n_] < 0).any() and not (hk[n_] == 2).any():
                            hk[n_, int(np.argmax(hk[n_] < 0))] = 2
                            db_log(n_, kind="holding gained", holding=H_KIND[2], why="founded")
                for n in list(WL.pending):
                    ev_ = WL.resolve(n, s[n], a[n], succ[n], idle[n])
                    if SAC_ON_ and isinstance(ev_, dict) and ev_.get("kind") == "sacred":
                        sac_fx(n, ev_)
                        if n in events:
                            events[n].append(dict(sacred=ev_))
                        continue
                    if ev_ is not None and n in events:
                        events[n].append(dict(cast_want=ev_))
                if SAC_ON_:   # S5: offers decided off-screen this week (no moment for them)
                    for ev_ in WL.PP.sac_take():
                        n_ = int(ev_["n"])
                        if not dead[n_]:
                            sac_fx(n_, ev_)
                        if n_ in events:
                            events[n_].append(dict(sacred=ev_))
                world_cast(WL.drain())   # the act's own cast events (the world's events came at the week's start)
            # tags: habit pulls harder, a door opens the niche, identity teaches more, binds holds and costs autonomy
            tg_ = L["TAG"][s, a] & (~idle & live_)[:, None]
            habit += P["tag_habit"] * tg_[:, :1] * ma
            hedon_n = hedon_n * (1 - 1 / 52) + (tg_[:, 0] & L["HEDON"][s, a])
            bodyhab_n = bodyhab_n * 0.75 + (tg_[:, 0] & (L["BODY"][s, a] > 0))
            dr_ = tg_[:, 1] & succ
            nic[dr_] += P["tag_door"] * (ma[dr_] - nic[dr_])
            dI = dI * (1 + P["tag_identity"] * tg_[:, 2:3])
            bd_ = tg_[:, 3] & succ
            bind_m = bind_m * np.exp(-1 / 520) + bd_
            bind_c = np.where(bd_[:, None], 0.8 * bind_c + 0.2 * ma, bind_c)
            need[:, NIDX["autonomy"]] -= P["bind_aut"] * np.minimum(bind_m, 3)
            # v7 discipline: an act the Library flags self_control "+" builds it (half when it does not work out), "-" wears it
            sc_ = L["SC"][s, a] * (~idle & live_); stf_ = TST[stage] / TST[2]
            up_ = sc_ > 0; dn_ = sc_ < 0
            dsc[up_] += P["disc_tag"] * stf_[up_] * np.where(succ[up_], 1.0, 0.5) * (P["disc_range"][1] - dsc[up_])
            dsc[dn_] -= P["disc_tag"] * stf_[dn_] * (dsc[dn_] - P["disc_range"][0])
            # closed options that fail backfire by kind: law (freedom, ties, money), approval (belonging, ties), means (money)
            clk_ = closed_s[ar, a]; bf_ = (clk_ >= 0) & ~succ & ~idle & live_
            if bf_.any():
                law_, app_, mea_ = bf_ & (clk_ == 0), bf_ & (clk_ == 1), bf_ & (clk_ == 2)
                res[law_, FRE] -= 0.15; res[law_, TIE] -= 0.1; res[law_, MON] -= 0.05; stress[law_] += 0.3
                bk_ = np.minimum(clu_[ar, a], 1.0)[app_] if CLU_ON else 1.0   # N1b: a light frown backfires lightly
                need[app_, NIDX["belonging"]] -= 0.1 * bk_; res[app_, TIE] -= 0.08 * bk_; stress[app_] += 0.15 * bk_
                res[mea_, MON] -= 0.1; stress[mea_] += 0.15
            res[:, HEA] -= P["body_hurt"] * L["BODY"][s, a] * (~succ & ~idle & live_)
            if SAC_ON_:   # S5: the acts that cost something real (money, ties or stress from the act itself, over
                # sacred_par's thresholds) count toward a line in their colour's ways, and heal a wound in it (People.sac_act)
                sp_ = WL.PP.sac_par
                rd_ = L["PAY"][s, a] + np.where(succ[:, None], L["WIN"][s, a], L["LOSE"][s, a])
                dm_, dt_, ds_ = rd_[:, MON].copy(), rd_[:, TIE].copy(), np.zeros(N)
                if closed_s is not None:   # a closed option's backfire, as above
                    ck2_ = closed_s[ar, a]; b2_ = (ck2_ >= 0) & ~succ
                    bk2_ = np.minimum(clu_[ar, a], 1.0) if CLU_ON else 1.0
                    dm_ -= 0.05 * (b2_ & (ck2_ == 0)) + 0.1 * (b2_ & (ck2_ == 2))
                    dt_ -= 0.1 * (b2_ & (ck2_ == 0)) + 0.08 * bk2_ * (b2_ & (ck2_ == 1))
                    ds_ += 0.3 * (b2_ & (ck2_ == 0)) + 0.15 * bk2_ * (b2_ & (ck2_ == 1)) + 0.15 * (b2_ & (ck2_ == 2))
                cost_ = (dm_ <= -sp_["cost_money"]) | (dt_ <= -sp_["cost_ties"]) | (ds_ >= sp_["cost_stress"])
                lv2_ = ~idle & live_ & ~dead
                if sp_["cost_closed"] and closed_s is not None:   # any closed option's backfire counts (sacred_par)
                    cost_ = cost_ | b2_
                    WL.PP._sac_count("cost closed", b2_ & lv2_)
                for nm_, m_ in (("money", dm_ <= -sp_["cost_money"]), ("ties", dt_ <= -sp_["cost_ties"]),
                                ("stress", ds_ >= sp_["cost_stress"])):
                    WL.PP._sac_count(f"cost {nm_}", m_ & lv2_)   # (for the checks)
                for ev_ in WL.sacred_act(lv2_, ma, cost_):
                    sac_fx(int(ev_["n"]), ev_)
                    if int(ev_["n"]) in events:
                        events[int(ev_["n"])].append(dict(sacred=ev_))
            res = _uclip(res, 0, 1)
            # after a lost job, most people find work again within a year or two (quietly, when the batch has no event for it)
            rj_ = np.nonzero(REJOB_ON & ~held[:, CAR] & ~retired & (end_t[:, CAR] > NEVER // 2) & (age < P["retire_age"] - 1)
                             & (rng.random(N) < P["rejob"] / 52))[0]
            for n in rj_:
                held[n, CAR] = True; I[n, CAR] = 0.2; sat[n, CAR] = 0.6; since[n, CAR] = t
                prof[n, CAR] = P["commit_mix"][0] * nic[n] + P["commit_mix"][1] * w[n] + P["commit_mix"][2] * nic[n]
                commit_log.append((int(n), t, CAR, "start", prof[n, CAR].round(2).tolist(), 0.2))
                if n in events:
                    events[n].append(dict(commitment=dict(age=round(age, 2), kind="career", what="start", through="found new work",
                                                          profile=prof[n, CAR].round(2).tolist())))
            newk_[rj_, CAR] = True
            if JM_ON:   # F9.19: a change of employer; the career and its strength go on, the workplace is new
                jm_ = np.nonzero(held[:, CAR] & ~retired & ~dead & (t - since[:, CAR] >= 52) & (t - ago["job"] >= 52) & (age < P["retire_age"])
                                 & (jm_rng.random(N) < float(np.interp(age, JM_A, JM_F)) / 52))[0]
                for n in jm_:
                    commit_log.append((int(n), t, CAR, "moved", prof[n, CAR].round(2).tolist(), round(float(I[n, CAR]), 2)))
                    if n in events:
                        events[n].append(dict(commitment=dict(age=round(age, 2), kind="career", what="moved",
                                                              through="changed employer")))
                    if WON:
                        WL.PP.leave(int(n), "work", t, "changed employer")   # a new work setting is joined next
                ago["job"][jm_] = t
            # what happened lately, and how long things have been as they are
            if P["base_rates"]:
                ago["le"][had_ev] = t
            ago["commit"][newk_.any(1)] = t; ago["child"][newk_[:, KID]] = t; ago["job"][newk_[:, CAR]] = t
            ago["win"][succ & ~idle & (stakes >= 0.9)] = t
            ago["hard_win"][succ & ~idle & (p_true < 0.5)] = t
            ago["fail_big"][~succ & ~idle & (stakes >= 0.9)] = t
            ago["fail_body"][~succ & ~idle & ((L["BODY"][s, a] > 0) | ((A_DEATH[s, a] > 0) if BAT else False))] = t
            ago["fail_long"][long_miss] = t
            ago["hard"][stress > 1.5] = t
            fails13 = fails13 * (1 - 1 / 13) + (~succ & ~idle & (delta < -0.3))
            stress_slow = 0.9 * stress_slow + 0.1 * stress
            for nm_, c_ in (("quiet", ~((had_ev if P["base_rates"] else False) | newk_.any(1) | mvk)),
                            ("lo_meaning", need[:, NIDX["meaning"]] < 0.45), ("vlo_meaning", need[:, NIDX["meaning"]] < 0.3),
                            ("lo_belong", need[:, NIDX["belonging"]] < 0.35), ("lo_peace", peace < 0.45), ("hi_stress", stress > 1.5),
                            ("lo_time", res[:, TIM] < 0.15), ("lo_auto", need[:, NIDX["autonomy"]] < 0.35),
                            ("ok_needs", (need[:, [0, 1, 3]] >= 0.55).all(1)), ("ok_body", (res[:, HEA] > 0.75) & (stress < 0.6)),
                            ("easing", stress < stress_slow - 0.01),
                            ("flat_comp", np.abs(need[:, NIDX["competence"]] - comp_ref) < 0.03)):
                streak[nm_] = np.where(c_, streak[nm_] + 1, 0)
            comp_ref = np.where(streak["flat_comp"] > 0, comp_ref, need[:, NIDX["competence"]])
            hist_m = np.where(idle[:, None], hist_m, hist_m + (ma - hist_m) / 520)
            ep_ = np.maximum(ea, 0); ep_ = ep_ / np.maximum(ep_.sum(1, keepdims=True), 1e-9)
            hist_e = np.where(idle[:, None], hist_e, hist_e + (ep_ - hist_e) / 520)
        imp = rng.random(N) < P["impose_p"]
        if imp.any():
            which = rng.choice(nI, size=imp.sum(), p=pb)
            need[imp] += 0.5 * L["IMP"][which]
            stress[imp] += 0.15
            res[imp, FRE] = _uclip(res[imp, FRE] + 0.5 * IMP_FREE[which], 0, 1)
            ii = np.nonzero(imp)[0]
            lost = ii[(which == 1) & held[ii, CAR] & JOBLOSS_ON & (rng.random(len(ii)) < 0.25)]    # an institution betrays its promise
            end(lost, [CAR] * len(lost), "lost job", t)
        if RON:   # titles follow commitments: a new one takes its first title; an ended one loses its titles, maybe leaving a status
            tk_ = (r_has[:, :NT_] @ KT_) > 0
            ent_ = held & ~tk_ & ((since == t) | (t % 4 == 0))
            ns_ = cond_ns(t, age, w) if (ent_.any() or t % 4 == 0) else None
            if ent_.any():
                for n, kk in zip(*np.nonzero(ent_)):
                    r_entry(n, kk, ma[n] if since[n, kk] == t and not idle[n] else w[n], ns_)
            for n, kk in zip(*np.nonzero(tk_ & ~held)):
                tl_ = np.nonzero(r_has[n, :NT_] & (TK_ == kk))[0]
                why_ = WHY[end_why[n, kk]] if end_why[n, kk] >= 0 else "it ended"
                nm_ = {GR["names"][i_] for i_ in tl_}
                for i_ in tl_:
                    r_lose(n, i_, why_)
                wed_ = nm_ & {"wife or husband", "married again", "partner of many years", "living together"}
                if why_ == "widowed" and wed_:
                    r_give(n, "widowed", "the partner died")
                elif kk == PAR and why_ in ("broke up", "left") and nm_ & {"wife or husband", "married again", "partner of many years"}:
                    r_give(n, "divorced", "the marriage ended")
                elif why_ == "retired":
                    r_give(n, "retiree", "retired")
                if kk == FAI and why_ == "left" and (left_given[n] or P["faith_drift"] is None):   # the faith they grew up in
                    r_give(n, "left the faith", "drifted away" if faith_drifted[n] else "walked away")
            if "out of work" in RID:
                for n in np.nonzero(r_has[:, RID["out of work"]] & held[:, CAR])[0]:
                    r_lose(n, RID["out of work"], "found work")
            for n in np.nonzero(mv_far)[0]:
                r_give(n, "newcomer", "moved")
            if t % 4 == 0:   # ---- each month: suspensions end, statuses run out, the engine's rules give and take
                # a title's profile follows the person: after about a year in which another of its profiles fits clearly
                # better, they hold it that way (a lab technician who came for the routine stays for the living material)
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & (PN_[:NT_] > 1)[None])):
                    f_ = np.where(PMASK_[i_], PW_[i_] @ w[n], -np.inf); b_ = int(np.argmax(f_))
                    r_drift[n, i_] = r_drift[n, i_] + 1 if (b_ != r_prof[n, i_] and f_[b_] - f_[r_prof[n, i_]] > P["profile_margin"]) else 0
                    if r_drift[n, i_] >= 12:
                        if TK_[i_] < NK and held[n, TK_[i_]]:   # the commitment leans the new way (and stays a mix of colors)
                            kk_ = TK_[i_]
                            pr_ = np.maximum(prof[n, kk_] + 0.25 * (PW_[i_, b_] - PW_[i_, r_prof[n, i_]]), 0.0)
                            prof[n, kk_] = pr_ / pr_.sum() if pr_.sum() > 1e-9 else PW_[i_, b_]
                        r_prof[n, i_] = b_; r_drift[n, i_] = 0
                        r_note(n, i_, "reshaped", GR["pwords"][i_][b_] or "in other ways")
                for n, p_ in zip(*np.nonzero((p_sus > NEVER // 2) & (p_sus <= t))):
                    p_sus[n, p_] = NEVER; r_has[n, NT_ + p_] = True; r_note(n, NT_ + p_, "restored", "the suspension ended")
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & ((t - r_since[:, :NT_]) / 52 >= GR["lasts"]))):
                    if i_ == OW_ and not held[n, CAR]:
                        continue                                   # out of work lasts while there is no work
                    r_lose(n, i_, "time passed")
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & (age > GR["ages"][:NT_, 1]))):   # outgrown: a scout at nineteen
                    r_lose(n, i_, "outgrew it")
                    if not (TK_[i_] == CAR and age < P["retire_age"]):   # an apprentice at thirty, a soldier at fifty-five:
                        r_close(n, i_, "retired" if TK_[i_] == CAR else "outgrew it")   # the work goes on under another title
                    if i_ == OW_:
                        r_give(n, "retiree", "reached pension age")
                for n, p_ in zip(*np.nonzero(p_acc & ((age >= GR["retires"]) | (age > GR["ages"][NT_:, 1]))[None])):
                    r_lose(n, NT_ + p_, "retired")                 # the skill stays as memory
                # what slips away on its own: an unused skill, standing, a bond (more when alone), an asset (more when poor);
                # what a rule says how it is lost (good credit, a car, a dog) goes only that way
                pk_ = GR["pkind"]
                use_ = 5 * (hist_m @ INDP.T) / np.maximum(INDP.sum(1), 1)[None]
                mult_ = np.where(pk_[None] == 0, 2 * _uclip(1.5 - use_, 0, 1.5), 1.0)
                mult_ = np.where(pk_[None] == 3, 1 + 2 * (res[:, TIE] < 0.3)[:, None], mult_)
                mult_ = np.where(pk_[None] == 4, 1 + 4 * (res[:, MON] < 0.15)[:, None], mult_)
                base_ = np.select([pk_ == 0, pk_ == 2, pk_ == 3, pk_ == 4], list(P["perk_loss"]), 0.0)
                for n, p_ in zip(*np.nonzero(r_has[:, NT_:] & ~RULE_LOSS[None] & (rng.random((N, NP_)) < 1 - np.exp(-base_[None] * mult_ / 13)))):
                    r_lose(n, NT_ + p_, "slipped away")
                fade_ = MEM_K[None] & ~p_acc & (p_lev > 0)        # a skill without access fades by its half-life
                p_lev *= np.where(fade_, 0.5 ** (1 / (13 * np.maximum(GR["half"], 1e-9)))[None], 1.0)
                if "out of work" in RID:   # still without work half a year after losing a job
                    ow_ = (~held[:, CAR] & ~retired & (end_why[:, CAR] == WHY.index("lost job")) & (t - end_t[:, CAR] >= P["ow_weeks"])
                           & (t - end_t[:, CAR] < P["ow_weeks"] + 4) & (age < P["retire_age"]))
                    for n in np.nonzero(ow_)[0]:
                        r_give(n, "out of work", "no work for half a year" if P["ow_weeks"] < 52 else "no work for a year")
                # a new job inside the career: now and then, to one the person now qualifies for (a graduate becomes a teacher)
                mv_ = held[:, CAR] & (rng.random(N) < P["title_move"] / 13)
                for n in np.nonzero(mv_)[0]:
                    r_entry(n, CAR, w[n], ns_, move=True)
                for i_ in LZ_:   # every item with a rule for losing it, whether or not a background rule gives it
                    ru_ = GR["rule"][i_]
                    hold_ = r_has[:, i_] | (p_acc[:, i_ - NT_] if i_ >= NT_ else False)
                    if np.count_nonzero(hold_):
                        pz_ = hold_ & (rng.random(N) < 1 - (1 - min(ru_["lrate"], 1.0)) ** (1 / 13))
                        for code_, why_ in ru_["lose"]:                  # each way of losing it, in its own words
                            lz_ = pz_ & ev_cond(code_, ns_); pz_ = pz_ & ~lz_
                            for n in np.nonzero(lz_)[0]:
                                r_lose(n, i_, why_)
                                if not (i_ < NT_ and TK_[i_] == CAR and age < P["retire_age"]):   # a physician whose
                                    r_close(n, i_, ru_["lend"])  # registration lapses works on under another title;
                                    # lend: how the commitment ends with it (an engagement broken off: "broke up")
                for i_ in BG:
                    ru_ = GR["rule"][i_]
                    lo_, hi_ = AGES_T[i_]
                    if not (lo_ <= age <= hi_) or (i_ >= NT_ and age >= GR["retires"][i_ - NT_]):
                        continue
                    cand_ = ~r_has[:, i_]
                    if i_ >= NT_:
                        cand_ = cand_ & ~p_acc[:, i_ - NT_]
                    kk_ = TK_[i_] if i_ < NT_ else NK
                    if ru_["after"]:                          # grows from another title (a cook becomes head chef), held
                        cand_ = cand_ & (r_has[:, ru_["after"]] & (t - r_since[:, ru_["after"]] >= 52 * P["rung_min"])).any(1)
                    elif kk_ < NK and not ru_["starts"]:      # a role inside a commitment already held
                        cand_ = cand_ & held[:, kk_]
                    elif kk_ < NK:                            # a role that starts its commitment: not for those whose kind is full
                        cand_ = cand_ & (~held[:, kk_] | ((r_has[:, :NT_] & (TK_ == kk_)).sum(1) < CAP_K[kk_]))
                        if RE_ON and kk_ == CAR:              # F8: no job comes to the retired on its own (only by their act)
                            cand_ = cand_ & ~(retired & ~held[:, CAR])
                    if not np.count_nonzero(cand_):
                        continue
                    base_ = cand_
                    cand_ = cand_ & ev_cond(ru_["req"], ns_)
                    if ru_["more"]:   # a pack's own way into this rule (EXTEND_<PACK>), at its own yearly rate
                        rt_ = r_rate(i_)
                        pr_ = (np.ones(N) if rt_ >= 1 else 1 - np.exp(-rt_ * ru_.get("hz", ru_["norm"]) * r_weight(i_) / 13)) * cand_
                        for code_, rx_ in ru_["more"]:
                            px_ = (base_ & ev_cond(code_, ns_)) * (1 - np.exp(-rx_ / 13))
                            pr_ = 1 - (1 - pr_) * (1 - px_); cand_ = cand_ | (px_ > 0)
                    if not np.count_nonzero(cand_):
                        continue
                    if not ru_["more"]:
                        rt_ = r_rate(i_)
                        pr_ = np.ones(N) if rt_ >= 1 else 1 - np.exp(-rt_ * ru_.get("hz", ru_["norm"]) * r_weight(i_) / 13)
                    for n in np.nonzero(cand_ & (rng.random(N) < pr_))[0]:
                        fr_ = [j_ for j_ in ru_["after"] if r_has[n, j_] and t - r_since[n, j_] >= 52 * P["rung_min"]]
                        for j_ in fr_:
                            r_lose(n, j_, "became " + GR["names"][i_], succ=i_)
                        r_gain(n, i_, ("grew from " + GR["names"][fr_[0]]) if fr_ else "in time")
                if f_pend:   # a facet an act gave in the week before its title came (newlywed at the wedding): now, or never
                    keep_ = []
                    for (n, i_, how_, mix_, t0_) in f_pend:
                        if (REFM_[i_] & r_has[n, :NT_]).any():
                            r_gain(n, i_, how_, mix_)
                        elif t - t0_ < 8:
                            keep_.append((n, i_, how_, mix_, t0_))
                    f_pend[:] = keep_
        # ---- 4b. the outside world. An era begins: everyone gets its message at once
        if t in era_at:
            key, inten, kind = era_at[t]
            msg = np.tile(COMBO_MIX[key], (N, 1)); ex = era_expo(ERA_KINDS.index(kind)); ac = accept(ar, msg, 1.0)
            if WON:   # close first (Emren 10:39; spec 1 §4): with the world on the era reaches a life mostly through its people
                # (their niche carries the times), so its own message is half as strong, and weighs most at 15 to 25
                ex = ex * 0.5 * float(np.interp(age, [10, 15, 25, 40], [0.3, 1.0, 1.0, 0.5]))
            take_in(ar, msg, P["era_shock"] * inten * ex * ac, 8)
            stress += 0.2 * inten
            for n in events:
                events[n].append(dict(era=dict(age=round(age, 2), combo=key, name=IDEAS[key][0], idea=IDEAS[key][1], kind=kind,
                                               intensity=round(inten, 2), took=round(float(ac[n]), 2))))
        # personal events: peers, institutions, daily life, nature, the supernatural
        if P["events_on"]:
            rates = EV["rate"] * P["ev_scale"] * EV_KEEP; tot = rates.sum()
            ii = np.nonzero(rng.random(N) < tot)[0]
            if len(ii):
                j = rng.choice(len(rates), size=len(ii), p=rates / tot); kind = EV["kind"][j]
                msg = np.zeros((len(ii), C))
                sel = kind == "fixed"; msg[sel] = EV["mix"][j[sel]]
                sel = kind == "random"; msg[sel] = random_messages(rng, int(sel.sum()))
                sel = kind == "niche"; msg[sel] = nic[ii[sel]] / nic[ii[sel]].sum(1, keepdims=True)
                sel = kind == "faith"; mf = random_messages(rng, int(sel.sum())); hf = held[ii[sel], FAI]
                mf[hf] = prof[ii[sel][hf], FAI]; msg[sel] = mf
                src = EV["src"][j]
                expo = np.select([src == 0, src == 1, src == 2, src == 3, src == 4],
                                 [0.5 + res[ii, TIE] + 0.5 * held[ii, COM] * I[ii, COM], inst_expo()[ii], np.ones(len(ii)),
                                  0.5 + (1 - res[ii, MON]), 0.4 + held[ii, FAI] * (0.6 + I[ii, FAI])])
                ac = np.zeros(len(ii)); hm = kind != "none"
                if hm.any():
                    ac[hm] = accept(ii[hm], msg[hm], (src[hm] <= 1).astype(float))
                    take_in(ii[hm], msg[hm], EV["s"][j[hm]] * expo[hm] * ac[hm], 7)
                need[ii] += EV["need"][j]; res[ii] = _uclip(res[ii] + EV["res"][j], 0, 1)
                stress[ii] += 0.3 * EV["s"][j] * (EV["need"][j].sum(1) < 0)
                mv = EV["move"][j]; nic[ii[mv]] = 0.5 * nic[ii[mv]] + 0.5 * msg[mv]; res[ii[mv], TIE] = np.maximum(0, res[ii[mv], TIE] - 0.2)
                dr = EV["door"][j]; nic[ii[dr]] += 0.15 * EV["s"][j[dr], None] * (msg[dr] - nic[ii[dr]])
                for q_, n in enumerate(ii):
                    ev_log.append((int(n), t, int(j[q_]), float(ac[q_])))
                    if n in events:
                        events[n].append(dict(outside=dict(age=round(age, 2), name=EV["names"][j[q_]], source=SOURCES[src[q_]],
                                                           message=msg[q_].round(2).tolist() if hm[q_] else None,
                                                           took=round(float(ac[q_]), 2) if hm[q_] else None)))
        if BAT and len(EVR) and t % 4 == 0:   # outside events from the batch, each read through the person's own colors
            dis_src_ = {}   # life -> (hazard, "home" or "near"): the world's disaster that brings its outside event (WL6)
            if WON and DIS_J_:   # a disaster's outside event comes when the world's disaster strikes one's own town or a
                # close person's (spec 5 §2: the history dial reaches the life through it), not on its own clock
                own_, near_ = WL.disasters()
                hit_ = ((own_ > 0) & (rng.random(N) < 0.4 + 0.5 * own_)) | (near_ & (rng.random(N) < WLM.DIS_NEAR))
                for j_ in DIS_J_:
                    evr_next[:, j_] = np.where(hit_ & (t >= evr_ok[:, j_]), t, T + 1)
                if events or WFX_ON:   # the story names the hazard that struck (WL6), so its scene can fit it
                    dis_src_ = {int(n): ((WL.dis_haz_now[n], "home") if own_[n] > 0 else (WL.dis_nhaz_now[n], "near"))
                                for n in np.nonzero(hit_)[0] if n in events or WFX_ON}
                if P["dis_match"]:   # WL6: only the events of the hazard that struck their own town
                    for n in np.nonzero(hit_ & (own_ > 0))[0]:
                        ok_ = DIS_FOR_.get(WL.dis_haz_now[n], DIS_J_)
                        for j_ in DIS_J_:
                            if j_ not in ok_:
                                evr_next[n, j_] = T + 1
                if WFX_ON:
                    for n in np.nonzero(((own_ > 0) | near_) & ~dead)[0]:
                        rc_ = WL.dis_rec_now[n] if own_[n] > 0 else None
                        wfx_add(n, "disaster", "home" if own_[n] > 0 else "close person", own_[n] if own_[n] > 0 else 1.0, age,
                                cause=None if rc_ is None else dict(domain=rc_.get("domain"), kind=rc_.get("kind"),
                                                                    key=rc_.get("key"), age=round(age, 2)),
                                hazard=WL.dis_haz_now[n] if own_[n] > 0 else None)
            due_ = evr_next <= t
            if due_.any():
                ns = cond_ns(t, age, w)
                lens_ = 0.5 * softmax(k) + 0.5 * w
                for j_ in np.nonzero(due_.any(0))[0]:
                    e_ = EVR[j_]; ii_ = np.nonzero(due_[:, j_])[0]
                    evr_next[ii_, j_] = t + rng.uniform(e_["gap"][0], e_["gap"][1], len(ii_)) * 52
                    if not (e_["window"][0] <= age <= e_["window"][1]):
                        continue
                    p_ = _uclip(P["read_p"] * factor(e_, ns)[ii_], 0, 1) * ev_cond(e_["req"], ns)[ii_]
                    ii_ = ii_[rng.random(len(ii_)) < p_]
                    if not len(ii_):
                        continue
                    if WON:
                        evr_ok[ii_, j_] = t + e_["gap"][0] * 52
                    pr_ = softmax(P["read_beta"] * 5 * lens_[ii_] @ e_["lens"].T)
                    rd_ = (pr_.cumsum(1) > rng.random((len(ii_), 1))).argmax(1)
                    imp_ = e_["impact"][rd_]
                    an_ = np.array([e_["also"][r_][0] for r_ in rd_]); ar_ = np.array([e_["also"][r_][1] for r_ in rd_])
                    thr_ = np.maximum(-np.asarray(e_["base_need"], float), 0)   # P4 §4: the needs it threatens
                    ev_by_ = (P["ev_need_k"] or P["ev_state_k"] or P["ev_reach_k"]) and thr_.sum() > 0
                    if ev_by_:
                        thr_ = thr_ / thr_.sum()
                        calm_ = _uclip(peace[ii_] + content[ii_] - 0.5, 0, 1)   # at peace and content: 1; strained: 0
                        if P["ev_need_k"]:   # it lands harder on a need already lacking
                            imp_ = imp_ * _uclip(1 + P["ev_need_k"] * (lack[ii_] @ thr_ - 0.3), 0.5, 2.0)
                    need[ii_] += P["read_k"] * imp_[:, None] * e_["base_need"][None] + an_
                    r0_ = res[ii_].copy() if WFX_ON and j_ in DIS_J_ else None
                    res[ii_] = _uclip(res[ii_] + imp_[:, None] * e_["base_res"][None] + ar_, 0, 1)
                    if r0_ is not None:   # what a disaster cost them: money, time, health, ties, freedom
                        for q_, n in enumerate(ii_):
                            for ri_ in np.nonzero(np.abs(res[n] - r0_[q_]) >= P["wfx_step"])[0]:
                                wfx_add(n, "disaster", RESOURCES[ri_], res[n, ri_] - r0_[q_, ri_], age, moment=e_["name"],
                                        hazard=dis_src_.get(int(n), (None, None))[0])
                    good_ = e_["base_need"].sum() + e_["base_res"].sum() >= 0
                    if good_:
                        mood[ii_] += 0.1 * imp_
                    else:
                        stress[ii_] += 0.3 * imp_ * ((1 + P["ev_state_k"] * (1 - 2 * calm_)) if ev_by_ and P["ev_state_k"] else 1.0)
                        mood[ii_] -= 0.1 * imp_
                    msg_ = np.eye(C)[e_["want"][rd_]]
                    take_in(ii_, msg_, P["read_want"] * imp_, 7)
                    if ev_by_ and P["ev_reach_k"] and not good_:   # they reach for what their own table ties to safety
                        tb_ = NMP[ii_] if NM_ON else np.repeat(NMAP[None], len(ii_), 0)   # (strained) or belonging (calm)
                        rch_ = (1 - calm_)[:, None] * tb_[:, NIDX["safety"]] + calm_[:, None] * tb_[:, NIDX["belonging"]]
                        take_in(ii_, rch_ / np.maximum(rch_.sum(1, keepdims=True), 1e-9), P["ev_reach_k"] * imp_, 7)
                    for q_, n in enumerate(ii_):
                        read_log.append((int(n), t, int(j_), int(rd_[q_])))
                        if n in events:
                            rdd_ = dict(age=round(age, 2), name=e_["name"], reading=e_["labels"][rd_[q_]],
                                        say=e_["say"][rd_[q_]], impact=float(imp_[q_]))
                            if int(n) in dis_src_ and WON and j_ in DIS_J_:   # WL6: the hazard that struck, and where
                                rdd_.update(hazard=dis_src_[int(n)][0], where=dis_src_[int(n)][1])
                            events[n].append(dict(read=rdd_))
        # resources and commitments feed needs: safety (money, health), belonging (ties), autonomy (freedom, time)
        supply = np.stack([0.5 * res[:, MON] + 0.5 * res[:, HEA], res[:, TIE], 0.6 * res[:, FRE] + 0.4 * res[:, TIM]], 1)
        if WON:   # the world: safety from crime, war and disaster where one lives; belonging from one's settings and people
            supply[:, 0] += WL.safety(); supply[:, 1] += 0.5 * (np.asarray(WL.PP.belong, float) - WLM.BELONG_REF)
            if WFX_ON:   # what the place gives to feeling safe, by the world's cause
                wfx_track("safety", WL.safety_parts(), age, dead)
        need[:, :3] += P["res_need"] * (supply - 0.5)
        need += P["commit_need"] * ((held * I) @ KPAY) * ((1 - need) if P["satiate"] else 1)
        if MK_ON:   # the mark of the work: a trade with say and skill meets autonomy and competence more (Jahoda 1982)
            mz_ = np.asarray(WL.PP.mark_z, float) * (held[:, CAR] * I[:, CAR])[:, None]
            need[:, NIDX["autonomy"]] += 0.1 * P["commit_need"] * mz_[:, 0]; need[:, NIDX["competence"]] += 0.1 * P["commit_need"] * mz_[:, 1]
        if RON:   # a title's own needs on top of its kind's, scaled the same way (statuses at full strength)
            tn_ = (r_has[:, :NT_] * np.where(TK_ < NK, I[:, np.minimum(TK_, NK - 1)], 1.0)) @ GR["meets_need"]
            need += P["commit_need"] * P["title_need"] * tn_ * np.where(tn_ > 0, (1 - need) if P["satiate"] else 1, 1)
        stress += 0.01 * np.maximum(0, 0.5 - res[:, HEA])
        if DEEP_ON and getattr(WL.PP, "care_load", None) is not None:   # phase 5: the care load wears on the carer
            stress += P["care_stress"] / 4.33 * np.asarray(WL.PP.care_load, float) / 10
        # a family looks after its children: safety and belonging are mostly provided before adolescence
        care = P["family_care"] * np.where(stage == 0, 1.0, np.where(stage == 1, 0.5, 0.0))
        need[:, :2] += care[:, None] * (0.85 - need[:, :2])
        need[:, 3:] += 0.5 * care[:, None] * (0.7 - need[:, 3:])     # and school and play give some competence and meaning (v5)
        need = _uclip(need, 0, 1)
        lack_raw = np.maximum(0, P["need_set"] - need) / P["need_set"]
        if P["flex"]:      # v6: needs that stay unmet lose importance, slowly, and faster with age; met ones regain it
            # driven by experience, not age (Emren 2026-10-04: favor comes from preference, mindset and experience):
            # the more wanted things a person has seen fail or close, the more readily they let go of what stays unmet
            fa = _uclip((tries - wins + blocked - P["flex_exp"][0]) / P["flex_exp"][1], 0, 1)[:, None]
            nimp += P["flex_rate"] * fa * ((1 - P["flex_depth"] * lack_raw) - nimp) + P["flex_rate"] * 0.2 * (1 - nimp)
        lack = nimp * lack_raw + P["duty_w"] * P["duty_asp"] * np.minimum(1, (held * I) @ DUTY)
        felt = np.einsum("nj,njc->nc", lack, NMP) if NM_ON else lack @ NMAP   # how much each color's ends could meet what is lacking
        dV = P["zeta"] * (w / w.max(1, keepdims=True)) * felt * (SE - P["eps0"])   # v2 direct channel (zeta=0 in v3)
        stress += 0.02 * (nimp * lack_raw).sum(1)

        conf = P["chi"] * (w[:, 0] + w[:, 4] - w[:, 3] - w[:, 2])
        obs = softmax(3 * f_tot)
        dS = conf[:, None] * (nic - w) + P["xi"] * (obs - w)
        if P["social_child"]:   # v6: children take on the ways of the family around them, whatever their own lean
            dS += P["social_child"] * np.where(stage == 0, 1.0, np.where(stage == 1, 0.5, 0.0))[:, None] * (nic - w)
        if P["react_k"]:   # v6 (Library notes A6; Brehm): strong pressure on a steady person pushes them the other way
            s_n = np.tanh(steady / P["steady_cap"])
            press = 0.5 * np.abs(nic - w).sum(1)
            rs = _uclip((s_n - 0.5) / 0.5, 0, 1) * _uclip((press - P["react_press"]) / P["react_press"], 0, 1)
            dS -= P["react_k"] * P["chi"] * rs[:, None] * (nic - w)

        # aspiration: what the person wants to be. Needs, norms and role models act here
        a_ = softmax(y)
        conf_a = P["chi_a"] / P["chi"] * conf if P["chi"] else 0 * conf
        aligned = _uclip(5 * (ma * (a_ - w)).sum(1), 0, 1) * (~idle)       # how far this act was a step toward the want
        # the times: an era's norms, taken or pushed back according to the person (exposure x acceptance)
        times = np.zeros((N, C))
        if e_i > 0:
            ep = np.tile(e_p, (N, 1)); times = P["era_norm"] * e_i * (era_expo(era_k[t]) * accept(ar, ep, 1.0))[:, None] * (ep - a_)
        # feedback from the meta variables: discontent wants what is missing (unmet needs) and what seems to work
        # for others; contentment settles the want on who one is; restlessness wants out of inner color tension
        fs = felt.sum(1, keepdims=True); felt_n = np.where(fs > 1e-9, felt / np.maximum(fs, 1e-9), obs)
        disc = np.maximum(0, 0.5 - content)[:, None] * (0.5 * felt_n + 0.5 * obs - a_)
        settle_ = np.maximum(0, content - 0.6)[:, None] * (w - a_)
        tgrad = np.einsum("nij,nj->ni", np.maximum(FR, 0)[None] * (1 - J), w)
        restless = np.maximum(0, 0.5 - peace)[:, None] * -2 * centre(tgrad)
        dAs = np.stack([P["zeta_a"] * felt * (SE - P["eps0"]), conf_a[:, None] * (nic - a_) * np.ones((N, 1)),
                        P["xi_a"] * (obs - a_), P["eps_v"] * (z - y) * (1 + P["tw_want"] * np.minimum(B + TWo, 2.0))[:, None]
                        + P["resign"] * np.maximum(0, -delta)[:, None] * aligned[:, None] * (z - y),
                        times, P["fb_disc"] * disc, P["fb_acc"] * settle_, P["fb_peace"] * restless,
                        P["g_want"] * np.einsum("ng,ngc->nc", gs * np.select([gk == 0, gk == 1, gk == 2], [1.0, 0.7, 0.5], 0.0),
                                                gm - a_[:, None, :]) if GON else np.zeros((N, C)),   # v7: dreams and plans shape the want
                        P["hz_want"] * fhz[:, None] * (HZW - a_)], 1)                  # v7: time felt short shifts what one wants
        dA = dAs.sum(1)
        gap = 0.5 * np.abs(a_ - w).sum(1)
        gap_r = gap
        stress += P["gap_stress"] * gap
        # pent-up demand: each time the wanted option is blocked (closed, unnoticed, out-pulled) or fails,
        # the gap between wanted and actual adds pressure. Inertia, the strength with which the person holds
        # the colors the want would take from them, sets how much pressure it takes to break through.
        # satisfaction (meta variable, Emren 2026-10-04): needs met, compared with what the person has got used to,
        # recent luck, and the distance from the person they want to be (ideal-self gap: dejection, Higgins 1987)
        f_need = (nimp * need).sum(1) / nimp.sum(1)                # v6: needs weighted by how much they matter now
        react_eff = 1 + TON * (react - 1)
        mood = mood * 0.9 + 0.1 * react_eff * np.where(idle, 0.0, fdelta)
        smid = smid + (SMID[stage] - smid) / (52 * P["mid_years"]) if P["mid_years"] > 0 else SMID[stage]
        # v7 unmet hope (point 9): the young count on more than life gives them now and raise their hopes with what it
        # gives; as time starts to feel short, what has not come weighs on them and they let it go. The weight peaks in
        # midlife and fades as hopes are let go (Schwandt 2016; Heckhausen et al. 2010)
        hzf = np.minimum(1.0, (fhz / P["hope_hz"]) ** 2)
        hope += P["hope_up"] / 52 * (1 - hzf) * np.maximum(0, lvl + P["hope_young"] - hope)
        hope -= P["hope_let"] / 52 * hzf * np.maximum(0, hope - lvl)
        unmet = np.maximum(-1.0, (hope - lvl) / P["hope_young"])      # share of a young person's extra hope still unmet;
                                                                        # below 0, life gives more than is now hoped for
        gap_c = gap
        if P["gap_move"]:   # gap_move: a gap one is acting to close weighs less (progress toward a goal, not only its distance)
            dir_ = np.maximum(a_ - w, 0); ds_ = dir_.sum(1)
            al_ = np.where(ds_ > 1e-9, (hist_m * dir_).sum(1) / np.maximum(ds_, 1e-9), 0.2)   # recent acts toward the want
            gap_c = gap * (1 - P["gap_move"] * _uclip((al_ - 0.2) / 0.3, 0, 1))
        c_now = 1 / (1 + np.exp(-(P["sat_need"] * (f_need - smid) + P["sat_adapt"] * (f_need - lvl)
                                  + P["sat_mood"] * mood - P["sat_gap"] * (gap_c - P["sat_gap_ref"])
                                  + TON * P["sat_base"] * (base_mood - P["base_ref"])      # a person's own usual mood
                                  - P["regret_k"] * regret                                  # v7: lost dreams that still fit
                                  - (P["sat_hope"] * hzf * unmet if P["sat_hope"] else 0.0)
                                  + (float(np.interp(age, MU_A, MU_F)) if P["mind_u"] is not None else 0.0))))   # F19: the midlife dip, the later rise
        content += (c_now - content) / P["meta_weeks"]            # felt over the last months, not this week
        lvl += (f_need - lvl) / P["adapt_weeks"]                  # hedonic adaptation, incomplete by design
        # pent-up demand (discontent): wanting that is blocked (closed, unnoticed, out-pulled) or fails, while the
        # gap is beyond what people tolerate and they are not content, builds pressure (crystallisation of discontent)
        base_now = SP_[stage] * np.where(stage == 0, min(1.0, age / 8), 1.0)
        frus = has & (lost_open | lost_seen | pulled | (tried & ~succ))
        # pressure piles up faster when ordinary change is slow (low plasticity): youth mostly just changes
        stuck = 1 - base_now / SP_.max()
        Q = Q * (1 - P["q_decay"]) + np.maximum(0, gap - P["q_tol"]) * frus * (1.5 - content) * stuck
        rsh = np.einsum("nk,nkc->nc", held * I, prof)
        if BAT:   # vows, debts and promises hold their colors as a role does
            rsh = rsh + P["bind_hold"] * np.minimum(bind_m, 1)[:, None] * bind_c
        rs_ = rsh.sum(1, keepdims=True)
        hold = 0.4 * kw + 0.3 * habit / np.maximum(habit.sum(1, keepdims=True), 1e-9) + \
            0.3 * np.where(rs_ > 0, rsh / np.maximum(rs_, 1e-9), 0.2)
        if GON:   # v7: a passion holds its colors, as a role does
            pas = np.einsum("ng,ngc->nc", gs * (gk == 1), gm); ps_ = pas.sum(1, keepdims=True)
            hp_ = P["pass_hold"] * np.minimum(1, ps_)
            hold = (1 - hp_) * hold + hp_ * np.where(ps_ > 0, pas / np.maximum(ps_, 1e-9), 0.2)
        give = np.maximum(0, w - a_); give /= np.maximum(give.sum(1, keepdims=True), 1e-9)
        hold_against = 5 * (give * hold).sum(1)            # 1 = holds them as much as an even share

        # ---- 4b2. v7 felt horizon: years a person feels are left (age, health), shortened by reminders of mortality
        if P["hz_k"] or P["hz_want"]:
            hea_ = res[:, HEA]
            hz_mem += P["hz_remind"] * _uclip((hea_last - hea_ - 0.05) / 0.2, 0, 1) * (hea_last >= 0)   # a health shock
            hea_last = hea_.copy()
            hz_mem *= 0.5 ** (1 / (52 * P["hz_mem_half"]))
            yl_ = np.maximum(P["hz_life"] - age, 1.0) * _uclip(hea_ / P["hz_health"], 0.2, 1.0)
            ltd_ = _uclip(1 - yl_ / P["hz_span"] + hz_mem, 0, 1)
            fhz += (ltd_ - fhz) / (52 * P["hz_lag"])

        # ---- 4c. temperament (v5): four slow traits learned from the life lived, fastest in childhood
        if TON:
            lrT = P["T_rate"] * TST[stage]
            # reactivity follows how harsh (stress), unpredictable (surprise) and supportive (safety, belonging) life has been
            sup = need[:, :2].mean(1)
            r_now = _uclip(1 + P["r_harsh"] * (stress - RR[0]) + P["r_unpred"] * np.where(idle, 0.0, np.abs(delta) / stakes - RR[1])
                            - P["r_support"] * (sup - RR[2]), 0.3, 2.5)
            react += (lrT if RST is None else P["T_rate"] * RST[stage]) * (r_now - react)
            # steadiness: succeeding in what one holds confirms who one is; failing in it shakes that; roles and being
            # who one wants to be steady a person; everything fades slowly
            own = np.maximum(0, 5 * (ma * hold).sum(1) - 1) * (~idle)
            steady += (stakes * own * np.where(succ, P["s_conf"], -P["s_hit"]) + P["s_role"] * (held * I).sum(1)
                       + P["s_fit"] * np.maximum(0, 0.15 - gap) - P["s_decay"] * steady)
            steady = np.maximum(steady, 0)
            # baseline mood: a slow average of how content life has been
            base_mood += lrT * (content - base_mood)
            # outlook: did trying work? Blocked or failed wanting teaches helplessness, success teaches control
            ev_o = has & (tried | lost_open)
            outlook += np.where(ev_o, 4 * lrT * stakes * (np.where(tried & succ, 1.0, 0.0) - outlook), 0.0)
            outlook = _uclip(outlook, 0, 1)

        # ---- 4d. v7 dreams, passions and plans: new ones, fading, letting go, deadlines, regret
        if GON:
            a_now_ = softmax(y); own_g = 0.5 * (w + a_now_)
            # sparks (1A): someone or something the person admires (a parent at work, a teacher, a book, a film, a parade)
            # starts a dream when what it shows speaks to who they are and want to be
            for n in np.nonzero(rng.random(N) < np.asarray(P["dream_rate"])[stage] / 52 * (age >= 4))[0]:
                st = stage[n]
                ex_src = np.array([0.5 + res[n, TIE], 0.5 + 0.5 * turn_pm[n], 0.3 + 0.5 * res[n, MON] + 0.5 * res[n, FRE],
                                   0.5 + 0.5 * held[n, COM] + e_i, 0.5 + 0.5 * turn_pm[n]])
                wt = TRIG_W[:, st] * ex_src[TRIG_SRC]
                if DG_ON:   # F6: a spark comes only at the ages its telling fits (a school visit, the elders' teaching)
                    wt = wt * ((TRIG_AGE[:, 0] <= age) & (age <= TRIG_AGE[:, 1]))
                if wt.sum() <= 0:
                    continue
                tr = int(rng.choice(len(wt), p=wt / wt.sum())); sc = TRIG_SRC[tr]
                wp_ = np.asarray(P["world_profile"], float)
                culture = 0.5 * wp_ / wp_.sum() + 0.5 * (e_p if e_i > 0 else np.full(C, 0.2))
                if sc == 0:
                    msg = rng.dirichlet(20 * fam[n] + 0.1)
                elif sc == 1:
                    msg = rng.dirichlet(20 * circle[n] + 0.1)
                elif sc == 2:
                    msg = random_messages(rng, 1)[0] if rng.random() < 0.6 else rng.dirichlet(20 * culture)
                elif sc == 3:
                    msg = rng.dirichlet(20 * culture) if rng.random() < 0.6 else random_messages(rng, 1)[0]
                else:
                    msg = random_messages(rng, 1)[0]
                if TRIG_TILT[tr].sum() > 0:
                    msg = 0.5 * msg + 0.5 * TRIG_TILT[tr] / TRIG_TILT[tr].sum()
                lens = 0.5 * softmax(k[n]) + 0.5 * a_now_[n]
                adm = 1 / (1 + np.exp(-(P["d_adm0"] + P["d_fit"] * (5 * (lens * msg).sum() - 1) + P["d_open"] * min(B[n], 2) / 2)))
                if rng.random() >= adm:
                    continue
                g_ = np.maximum(msg * (1 + P["d_read"] * (5 * lens - 1)), 0)      # read through their own colors
                g_ = 0.8 * g_ / max(g_.sum(), 1e-9) + 0.2 * lens
                subj_ = -1
                if DG_ON and TRIG_SUBJ[tr]:   # F6: the spark keeps its subject: of the dreams it shows, the one nearest their
                    dgc_ = [i_ for i_ in TRIG_SUBJ[tr] if DRM_FROM[i_] <= age and DRM_S[i_, st]   # colours that they are old
                           and not (st >= 2 and DRM_D[i_] >= 0 and held[n, DRM_D[i_]])]           # enough for and do not hold
                    if not dgc_:
                        continue                                                 # too young for any of them: no dream yet
                    subj_ = dgc_[int(np.argmax(DRM_M[dgc_] @ (g_ - 1 / C)))]
                    g_ = (1 - P["dream_subj"]) * g_ + P["dream_subj"] * DRM_X[subj_]   # its ways, partly the subject's
                dw = np.asarray(P["d_dom"], float).copy()
                fitd = KPAY @ (NMAP @ g_); dw[:NK] *= fitd / fitd.mean()        # what the dream is about follows what its ways serve
                if st >= 2:
                    dw[:NK] *= ~held[n]
                if SEEN_ON and SD_AGES_[0] <= age <= SD_AGES_[1]:   # S6: from 8 to 20 a dream is about a path they have seen
                    dw[:NK] *= 1 + SD_DREAM_ * WL.PP.seen_dom(n)    # more often (the sparks' rate as it was)
                if DG_ON and subj_ < 0:   # F6: only what a dream of their age can be about
                    dgf_ = (DRM_FROM <= age) & DRM_S[:, st]
                    dgh_ = np.array([(dgf_ & (DRM_D == d_)).any() for d_ in range(NK)] + [(dgf_ & (DRM_D < 0)).any()])
                    if (dw * dgh_).sum() > 0:
                        dw = dw * dgh_
                if subj_ >= 0:
                    dom = int(DRM_D[subj_])
                else:
                    dom = int(rng.choice(NK + 1, p=dw / dw.sum())); dom = dom if dom < NK else -1
                new_goal(n, 0, g_, dom, sc, trig=tr, s0=0.2 + 0.4 * adm, name=subj_)
                if SEEN_ON and n in events and SD_AGES_[0] <= age <= SD_AGES_[1]:   # S6: a dream seeded from a seen path
                    sd_ = WL.PP.seen_dream(n, dom)                                    # and its model (the Library's "dream")
                    if sd_:
                        events[n].append(dict(seen=dict(sd_, age=round(age, 2))))
            # fading: an unfed dream fades (fast in childhood); a passion only when unpractised for a year; a plan that
            # does not fit who one is loses its pull (self-concordance: Sheldon & Elliot 1999)
            fd_ = np.exp(-np.log(2) / (52 * np.asarray(P["d_half"], float)[stage]))[:, None]
            if DG_ON:   # F6: a young child's play dream is short-lived (children of 4 to 8 change them often)
                fd_ = np.where(gplay, np.exp(-np.log(2) / (52 * P["dream_play_half"])), fd_)
            gs = np.where(gk == 0, gs * fd_, gs); gv = np.where(gk == 0, gv * fd_, gv)
            gs = np.where((gk == 1) & (t - glast > 52), gs * np.exp(-np.log(2) / (52 * P["pass_half"])), gs)
            conc_g = _uclip(2 * np.einsum("ngc,nc->ng", gm, own_g) / own_g.max(1)[:, None] - 1, -0.5, 1)
            gs = np.where((gk == 2) & (gby == 0), gs - P["g_decay"] * (1 - np.maximum(conc_g, 0)) * gs, gs)
            # an obsessive passion gnaws when the person is kept from it (rumination)
            stress = stress + P["op_rum"] * (((gk == 1) & (t - glast > P["op_away"])) * gs * (1 - ga)).sum(1)
            # a turning point seals a dream as a rite does: a big life event met in the dream's ways, and it worked
            if P["base_rates"]:
                for n in np.nonzero(big & succ)[0]:
                    seal(n, "a turning point", only=set(np.nonzero((gk[n] == 0) & (ra[n] >= 0.5))[0].tolist()))
            for n, j in zip(*np.nonzero((gk >= 0) & (gs < 0.08) & (gby == 0))):
                end_goal(n, j, ("faded", "faded", "drifted away")[gk[n, j]])
            # new plans (adults; a plan is not a commitment): a resolution at a birthday, a passion that wants room,
            # an unmet need, an old dream that returns
            npl = (gk == 2).sum(1); room_ = (npl < P["max_plans"]) & (stage >= 2)
            if t % 52 == 0:   # fresh start (Dai, Milkman & Riis 2014): birthdays invite resolutions
                gap_now = 0.5 * np.abs(a_now_ - w).sum(1)
                for n in np.nonzero(room_ & (rng.random(N) < P["res_p"] * _uclip(gap_now / 0.15, 0, 2)))[0]:
                    pos_ = np.maximum(a_now_[n] - w[n], 0)
                    if new_goal(n, 2, 0.5 * a_now_[n] + 0.5 * pos_ / max(pos_.sum(), 1e-9), -1, GSRC["resolution"], hz=1, s0=0.35) >= 0:
                        npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            kid_ = np.zeros((N, NGS), bool)
            for j in range(NGS):
                kid_[:, j] = ((gpar == j) & (gk == 2)).any(1)
            cand = (gk == 1) & ~kid_ & room_[:, None] & (rng.random((N, NGS)) < P["pass_plan"] / 52 * gs)
            for n, j in zip(*np.nonzero(cand)):
                if npl[n] >= P["max_plans"]:
                    continue
                d_ = gd[n, j]
                if d_ >= 0 and (held[n, d_] or (d_ == CAR and (retired[n] or age > 60)) or (d_ == KID and age > 45)):
                    d_ = -1
                hz = 3 if (d_ < 0 and rng.random() < 0.3) else 2
                if new_goal(n, 2, gm[n, j].copy(), d_, GSRC["passion"], hz=hz, par=j, s0=0.3 + 0.4 * gs[n, j]) >= 0:
                    npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            desire = (nimp * np.maximum(0, P["need_set"] - need) / P["need_set"]) @ KPAY.T            # N,NK
            elig = ~held & room_[:, None]
            elig[:, CAR] &= ~retired & (age < 60); elig[:, KID] &= (age < 45)
            for d_ in range(NK):
                elig[:, d_] &= ~((gk == 2) & (gd == d_)).any(1)
            pdom = P["dom_plan"] / 52 * desire * elig * np.where(np.arange(NK) == KID, 0.3 + 0.7 * held[:, PAR][:, None], 1.0)
            hit_d = rng.random((N, NK)) < pdom
            for n in np.nonzero(hit_d.any(1))[0]:
                d_ = int(np.argmax(np.where(hit_d[n], pdom[n], -1)))
                if new_goal(n, 2, 0.5 * a_now_[n] + 0.5 * w[n], d_, GSRC["need"], hz=2, s0=0.3 + 0.4 * min(1.0, desire[n, d_])) >= 0:
                    npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            fit_l = _uclip(5 * (lost_m * a_now_[:, None, :]).sum(2) - 1, 0, 2) / 2
            p_rv = (P["revive"] / 52 * fit_l * lost_s * lost_on * room_[:, None]
                    * (res[:, FRE] * (0.5 + res[:, TIM]) * (1 + 2 * regret))[:, None])
            for n, q_ in zip(*np.nonzero(rng.random((N, 3)) < p_rv)):
                if npl[n] >= P["max_plans"]:
                    continue
                d_ = lost_d[n, q_]
                if d_ >= 0 and (held[n, d_] or (d_ == CAR and (retired[n] or age > 60)) or (d_ == KID and age > 45)):
                    d_ = -1
                if new_goal(n, 2, lost_m[n, q_].copy(), d_, GSRC["old dream"], hz=2, s0=0.4, name=lost_nm[n, q_]) >= 0:
                    lost_on[n, q_] = False; npl[n] += 1
            # felt odds, letting go and deadlines
            pln = gk == 2
            if pln.any():
                wl = np.minimum(gh - t, max(52.0, (P["life_end"] - age) * 52))
                steps = np.ceil((1 - gp) * np.asarray(P["g_size"], float)[ghz] / STEP_INC).astype(int)
                fo_ = np.nonzero(pln)   # speed pass: the felt odds of the plans alone (each plan's odds is its own; the rest went unused)
                gfelt = gfelt.copy(); gfelt[fo_] = felt_odds(gch[fo_], gph[fo_], wl[fo_], steps[fo_], gd[fo_],
                                                             np.broadcast_to(outlook[:, None], pln.shape)[fo_], P)
                # clinging to a plan that seems hopeless is stressful (Wrosch et al. 2003)
                stress = stress + P["g_ruminate"] * (pln * gs * _uclip((0.3 - gfelt) / 0.3, 0, 1)).sum(1)
                fa_ = _uclip((tries - wins + blocked - P["flex_exp"][0]) / P["flex_exp"][1], 0, 1)
                letgo = 0.3 + 0.7 * fa_               # having seen wanted things fail makes letting go easier
                sunk = 1 - np.exp(-gi)                 # what has been put in holds people to a plan
                drop = (pln & (gby == 0) & (gfelt < P["g_drop"]) & (rng.random((N, NGS)) < 1 / 13)
                        & (rng.random((N, NGS)) < letgo[:, None] * (1 - sunk)))
                for n, j in zip(*np.nonzero(drop)):
                    quit_(n, j, "let go", letgo[n])
                for n, j in zip(*np.nonzero((gk == 2) & (t >= gh))):
                    hw = HORIZON_W[ghz[n, j]]
                    if hw is not None and hw > 1 and gx[n, j] < 2 and gby[n, j] == 0:
                        felt2 = float(felt_odds(gch[n, j], gph[n, j], hw, steps[n, j], gd[n, j], outlook[n], P))
                        p_ext = 1 / (1 + np.exp(-(3 * (felt2 - 0.35) + 1.5 * sunk[n, j] + (gsrc[n, j] == GSRC["passion"]) - 1.5 * letgo[n])))
                        if rng.random() < p_ext:   # more time, the same plan (sunk cost, and the planning fallacy again)
                            gh[n, j] = t + hw; gx[n, j] += 1; glog(n, j, "extended")
                            continue
                    quit_(n, j, "not reached in time", letgo[n])
            if t % 52 == 0:   # regret of what was let go grows over a decade when it still fits (Gilovich & Medvec 1995)
                yrs_ = _uclip((age - lost_t) / 10, 0, 1)
                regret = (lost_on * lost_s * _uclip(5 * (lost_m * a_now_[:, None, :]).sum(2) - 1, 0, 1) * yrs_).sum(1) / 3

        # coherence under the world's framing, softened by what this person has integrated
        Tm = np.maximum(FR, 0)[None] * (1 - J) + np.minimum(FR, 0)[None]
        G = np.einsum("nij,nj->ni", Tm, w)
        tension = np.einsum("ni,nij,nj->n", w, np.maximum(FR, 0)[None] * (1 - J), w)   # opposed colors held at once
        # peace (meta variable): the absence of agitation. Stress, ought conflict with commitments, inner tension
        # between colors the world frames as opposed, and blocked wanting all disturb it
        q_thr = P["q_theta"] * np.maximum(hold_against, 0.2) ** P["q_hold"]
        q_rel = Q / q_thr
        p_now = 1 / (1 + np.exp(-(P["pc_mid"] - P["pc_stress"] * stress - P["pc_clash"] * cload
                                  - P["pc_tension"] * tension - P["pc_pent"] * q_rel)))
        peace += (p_now - peace) / P["meta_weeks"]
        if P["adjectives"] and t % 4 == 0:   # v7 adjectives: each month, with a margin so a state does not flicker
            src_ = dict(content=content, peace=peace, mood=mood, stress=stress, wound=wound, discipline=dsc, gap=gap_r,
                        unmet_hope=hzf * np.maximum(unmet, 0), **{"shadow_" + c_: shA[:, i_] for i_, c_ in enumerate(COLORS)})
            src_.update({nm_: need[:, i_] for i_, nm_ in enumerate(NEEDS)}); src_.update({nm_: res[:, i_] for i_, nm_ in enumerate(RESOURCES)})
            av_ = np.stack([np.broadcast_to(src_[a_[2]], (N,)) for a_ in ADJ_ALL], 1) * ADJ_SIDE
            adj_v = av_ if adj_v is None else adj_v + P["adj_smooth"] * (av_ - adj_v)    # the last few months
            old_ = adj
            adj = ((adj_v >= ADJ_ON * ADJ_SIDE) | (adj & (adj_v >= ADJ_OFF * ADJ_SIDE))) & (age >= ADJ_AGE)
            for n, a_ in zip(*np.nonzero(adj != old_)):
                what_ = "gained" if adj[n, a_] else "lost"
                adj_log.append((int(n), t, int(a_), what_))
                if adj[n, a_]:
                    adj_since[n, a_] = t
                if n in events:
                    events[n].append(dict(adj=dict(age=round(age, 2), name=ADJ_NAMES[a_], say=ADJ_SAY[a_], what=what_)))
        dC = -MU_ * w * (G - (w * G).sum(1, keepdims=True))
        J += P["iota"] * np.maximum(delta, 0)[:, None, None] * \
            np.einsum("ni,nj->nij", ma, ma) * 4 * (1 - J) * (1 - np.eye(C))[None]
        if P["ten_bad"]:   # v6: a failed attempt to hold both loosens what had been integrated
            J -= P["iota"] * P["ten_split"] * np.maximum(-delta, 0)[:, None, None] * np.einsum("ni,nj->nij", ma, ma) * 4 * J * (1 - np.eye(C))[None]

        # upkeep: a concentrated identity decays toward balance unless constantly fed
        conc = ((w ** 2).sum(1) - 0.2) / 0.8
        # shadows replace the flat upkeep: an active shadow pulls its own color back (its costs teach), the rest share it
        if not SHON:
            dU = -P["upkeep"] * conc[:, None] * z
        elif P["sh_form"] == "balance":   # back toward what the person lacks, as strongly as their strongest shadow
            dU = -P["sh_pull"] * shA.max(1)[:, None] * z
        else:                             # "own": the shadowed color itself gives way
            dU = -P["sh_pull"] * shA * np.maximum(z, 0)
            if P["sh_will"]:   # sh_will: less on a colour wanted beyond what is held
                dU = dU * (1 - P["sh_will"] * _uclip(5 * (softmax(y) - w), 0, 1))

        # ---- 4e. identity and the character's own death (point 11)
        if t % 52 == 0 and age >= 25 and P["attr_drift"]:   # a woman's attraction can shift a step in adult life
            dr_ = female & (attr != 2) & ((idr_ if ID2 else rid).random(N) < P["attr_drift"])
            attr[dr_] += np.where(attr[dr_] < 2, 1, -1)
        if ID2 and BAT:   # N1b (chroma-identity/for-the-engine.md)
            newp_ = held[:, PAR] & ~par_prev                 # a new partner: of the same sex or not, by attraction (Pew 2013)
            for n in np.nonzero(newp_)[0]:
                partner_same[n] = ps_u[n, min(ps_n[n], ps_u.shape[1] - 1)] < PSP_[attr[n]]; ps_n[n] += 1
            partner_same &= held[:, PAR]; par_prev = held[:, PAR].copy()
            if IDF_ON:   # found: the first week a moment about a trait the person has comes (the game shows it from then)
                hv_ = np.stack([gender_self > 0, attr >= 1, ace, intersex], 1)
                fd_ = IDG[s] & hv_ & (found_id <= NEVER // 2) & ~dead[:, None]
                if fd_.any():
                    found_id[fd_] = t
                    for n in set(np.nonzero(fd_.any(1))[0].tolist()) & set(events):
                        for k_ in np.nonzero(fd_[n])[0]:
                            events[n].append(dict(found=dict(age=round(age, 2), trait=("gender", "attraction", "ace", "intersex")[k_])))
            rs_w, at_w, ex_w = role_view()
            cwt_ = np.zeros(N)
            if TROLE_ON:   # a title the world reserves for the other sex, as they are expected: a small weekly strain
                th_ = r_has[:, :NT_] & (TROLE_ >= 0)[None]
                if th_.any():
                    cwt_ = np.where(th_, ex_w[:, 1 - _uclip(TROLE_, 0, 1)], 0.0).max(1)
                    stress += P["role_title_stress"] * rs_w * cwt_ * ~dead
            cross_title = cwt_ >= 0.5
            hidg_ = (gender_self > 0) & ~named_g & (age >= P["aware_age"])
            x_ = np.maximum(np.maximum(act_cw, cwt_), hidg_.astype(float))
            rfit_avg += (1 - 0.5 ** (1 / (52 * P["role_fit_hl"]))) * (x_ - rfit_avg)
        if BAT and P["hide_stress"] and age >= P["aware_age"] and ID2:   # hiding each trait weighs on them until they tell it;
            # gender more where it is less accepted; after telling, a share stays where the world is hostile (Meyer 2003)
            clim_ = P["climate"] + (clim_w if WON else 0.5 * faith_given * I[:, FAI])   # the world: local norm and the right
            o_ = (attr >= 2) & ~dead; g_ = (gender_self > 0) & ~dead
            ho_ = (1 + clim_) * np.where(came_o, P["out_stress"] * clim_, 1.0) * o_
            hg_ = (1 + clim_) * (1.5 - at_w) * np.where(named_g, P["out_stress"] * (1 - at_w), 1.0) * g_
            stress += P["hide_stress"] * (ho_ + hg_)
        elif BAT and P["hide_stress"] and age >= P["aware_age"]:   # hiding who they are weighs on them until they come out
            came_ = mark_n[:, MIDX["came out"]] > 0 if "came out" in MIDX else np.zeros(N, bool)
            hid_ = ((attr >= 2) | unease) & ~came_ & ~dead
            if hid_.any():
                stress += P["hide_stress"] * hid_ * (1 + P["climate"] + (clim_w if WON else 0.5 * faith_given * I[:, FAI]))
        if P["self_death"] and DTH_ON:   # v22.5 F2: death from the life
            death_week()
        elif P["self_death"]:   # the life table, likelier in poor health
            sm_ = P["self_mort"]
            q_ = np.minimum(1, (sm_[0] + sm_[1] * np.exp(sm_[2] * age)) * np.exp(P["self_health"] * (0.6 - res[:, HEA])))
            for n in np.nonzero(~dead & (rid.random(N) < q_ / 52))[0]:
                die(n, "illness" if age < 75 else "old age")
        if RON and (pris_out == t).any():   # out of prison
            for n in np.nonzero(pris_out == t)[0]:
                if "ex-prisoner" in GR["ID"]:
                    r_gain(n, GR["ID"]["ex-prisoner"], "released")

        # ---- 5. integrate. Plasticity belongs to the life stage
        if P["tw_trans"]:   # a turning point this week opens a window (see tw_trans)
            if tw_held is None:
                tw_held = held.copy(); tw_has = r_has[:, :NT_].copy() if RON else None
            tr_ = (held != tw_held).sum(1) + ((r_has[:, :NT_] != tw_has).sum(1) if RON else 0)
            if P["tw_sep"]:
                TWo += P["tw_trans"] * np.minimum(tr_, 2) * (stage >= 1)
            else:
                B += P["tw_trans"] * np.minimum(tr_, 2) * (stage >= 1)
            tw_held = held.copy()
            if RON: tw_has = r_has[:, :NT_].copy()
        base = SP_[stage] * np.where(stage == 0, min(1.0, age / 8), 1.0)
        settle = np.log1p(M / P["M0"]) if P["settle_log"] else M / P["M0"]   # experience settles a person, with diminishing effect
        s_eff = P["steady_cap"] * np.tanh(steady / P["steady_cap"])          # steadiness slows change, up to a ceiling
        plast = base / (1 + settle) * (1 + B) / (1 + TON * P["steady_k"] * s_eff)   # a steady person changes more slowly
        if SET_ON:   # F14: colours settle with age; a big event (openness) still lets them move as a younger person's
            sf_ = float(np.interp(age, SET_A, SET_F))
            settle_f = sf_ + (1 - sf_) * _uclip((B - set_bu) / P["set_big"], 0, 1)
            set_bu += (B - set_bu) / (52 * P["set_usual"])
            plast = plast * settle_f
        F = np.stack([centre(dI), centre(dV), centre(dS), centre(dC), centre(dU)], 1)
        noise = centre(rng.normal(0, P["noise"], (N, C)))
        if P["drift_k"] != 1.0:   # played lives: the game weighs the random drift
            noise = P["drift_k"] * noise
        if CUR_ON:   # item 12: the current takes over part of the random drift
            noise = (1 - P["cur_cut"]) * noise
        support =0.5 * (need[:, NIDX["belonging"]] + res[:, TIE])          # being cared for: belonging and ties
        if WON:   # and what the cast and the settings give in hard weeks
            support = support + np.asarray(WL.PP.support, float)
        open_ = np.minimum(wound, 2.0)
        kap_e = P["kappa_e"] * (1 + P["care_k"] * support + P["heal_k"] * open_ * support)   # cared for, people come back
        if P["tw_pull"]:   # while a window is open, the old self pulls back less
            kap_e = kap_e / (1 + P["tw_pull"] * np.minimum(B + TWo, 2.0))
        drift = plast[:, None] * noise + P["mom"] * v - kap_e[:, None] * (z - k)
        if P["hz_self"]:   # next version: limited time felt changes who one is as it changes what one wants
            drift = drift + P["hz_self"] * fhz[:, None] * centre(HZW[None] - w)
        stepF = plast[:, None, None] * F
        if P["tw_force"] and P["tw_sep"]:   # an open window: what happens now moves the colors more
            stepF = stepF * (1 + P["tw_force"] * np.minimum(TWo, 2.0))[:, None, None]
        if SEA_ON and sea_tr.any():   # the season's transforming chance moves the colors further
            stepF = stepF * np.where(sea_tr, P["season_amp"], 1.0)[:, None, None]
        chan[:, :5] += stepF; chan[:, 6] += drift
        dz_ = stepF.sum(1)
        if UPL_ON and P["up_self"]:   # F15: the start's lean on who they are (booked as social)
            udz_ = (P["up_self"] * up_short(w) * plast)[:, None] * centre(5 * (UPM_[None] - w))
            if age >= P["up_from"]:
                udz_ = udz_ - UP_DEC * up_oz
            up_oz += udz_
            dz_ = dz_ + udz_; chan[:, 2] += udz_
        if DOM_ON:   # a share of what a moment in an area teaches stays in that area; offsets fade back toward the core
            srf_ = P["dom_share"] * dz_ * (inA_ & ~idle)[:, None]
            Dz[ar, np.maximum(area_, 0)] += srf_; dz_ = dz_ - srf_
            hl_ = np.array([held[:, CAR] | (stage <= 2), np.ones(N, bool), np.ones(N, bool), held[:, FAI]]).T   # school is work
            Dz *= (1 - np.log(2) / (52 * np.where(hl_, P["dom_half"], P["dom_end_half"])))[:, :, None]
            Dz = np.clip(Dz - Dz.mean(2, keepdims=True), -P["dom_cap"], P["dom_cap"])
        if WON and t % 4 == 0:   # S2 (read only, for the game): the colour shares of what surrounds them, once a month
            around = WL.PP.around()
        if CUR_ON and t % 4 == 0 and age >= 3:   # item 12: the times as a steady current, once a month
            if WON:
                cl_, st_, tm_ = (np.asarray(x_, float) for x_ in WL.PP.cur_parts)
            else:   # no outer world: the niche stands for people and places (the circle's turnover is random)
                cl_, st_ = nic, nic
                wp_ = WP_ if UPL_ON and P["up_ease"] else np.asarray(P["world_profile"], float); tm_ = wp_ + 0.5 * e_i * (np.asarray(e_p, float) - wp_)
                tm_ = np.broadcast_to(tm_ / tm_.sum(), (N, C))
            cm_ = P["cur_mix"]
            cur_ = (cm_[0] * cl_ + cm_[1] * st_ + cm_[2] * tm_) / sum(cm_)
            cur_m = cur_.copy() if cur_m is None else cur_m + (cur_ - cur_m) / (12 * P["cur_mem"])   # what has reached them lately
            cur_ = cur_m
            b0_, pk_, at_, wd_ = P["cur_age"]
            if WON and P["cur_rel"]:   # against the society (people), the town's average places, the times with cur_era of the era
                V_ = np.asarray(WL.W.V, float)[None, :]
                pr_ = WL.PP.places_ref if getattr(WL.PP, "places_ref", None) is not None else V_
                ref_ = (cm_[0] * V_ + cm_[1] * pr_ + cm_[2] * (P["cur_era"] * V_ + (1 - P["cur_era"]) * tm_)) / sum(cm_)
                lr_ = np.log(np.maximum(cur_m, 1e-4)) - np.log(ref_) - P["cur_bal"] * np.log(np.maximum(w, 1e-4))
                cdz_ = (P["cur_rel_k"] * (b0_ + pk_ * np.exp(-((age - at_) / wd_) ** 2)) * plast)[:, None] * centre(lr_)
            else:
                cdz_ = (P["cur_k"] * (1.0 if WON else P["cur_off"]) * (b0_ + pk_ * np.exp(-((age - at_) / wd_) ** 2)) * plast)[:, None] * centre(5 * (cur_ - w))
            if P["era_push_k"] != 1.0:   # played lives: the game weighs the times' push as it weighs an era's
                cdz_ = P["era_push_k"] * cdz_
            if P["cur_will"]:   # cur_will: on a colour wanted beyond what is held, the current pulls it down up to this share less
                cdz_ = centre(np.where(cdz_ < 0, cdz_ * (1 - P["cur_will"] * _uclip(5 * (softmax(y) - w), 0, 1)), cdz_))
            dz_ = dz_ + cdz_; chan[:, 8] += cdz_; cur_sum += np.abs(cdz_).sum(1)
        if ODD_ON_ and t % 4 == 0:   # S4: blending in at a place steps the colours toward it (booked with the current)
            edw_ = WL.PP.eyes_dw
            if edw_.any():
                edz_ = centre(5 * edw_); WL.PP.eyes_dw = np.zeros_like(edw_)
                if SET_ON: edz_ = settle_f[:, None] * edz_   # F14
                dz_ = dz_ + edz_; chan[:, 8] += edz_
        if MK_ON and t % 4 == 0:   # spheres phase 2: the mark of the work, a year's step once it is drawn (booked with the current)
            mdw_ = WL.PP.mark_dw
            if mdw_.any():
                mdz_ = centre(5 * mdw_); WL.PP.mark_dw = np.zeros_like(mdw_)
                if P["era_push_k"] != 1.0:   # played lives: weighed as the other outside pushes
                    mdz_ = P["era_push_k"] * mdz_
                if SET_ON: mdz_ = settle_f[:, None] * mdz_   # F14
                dz_ = dz_ + mdz_; chan[:, 8] += mdz_
            hu_ = WL.PP.mark_hurt & ~dead
            if hu_.any():   # a serious injury at work
                res[hu_, HEA] -= 0.15; WL.PP.mark_hurt = np.zeros(N, bool)
            for n_ in np.nonzero(WL.PP.mark_die & ~dead)[0] if P["self_death"] else ():   # (deaths only where lives can die)
                die(int(n_), "an accident at work")
            WL.PP.mark_die = np.zeros(N, bool)
        z_new = centre(z + dz_ + drift)
        v = 0.7 * v + 0.3 * (z_new - z)
        if P["tw_pen"]:    # a big life event reaches the deep core directly, in proportion to how hard it hit
            k = k + (P["tw_pen"] * big * np.minimum(np.abs(delta) / np.maximum(stakes, 1e-9), 1.0))[:, None] * (z_new - z)
        z = z_new
        eps_w = eps_k * (1 + P["tw_core"] * np.minimum(B + TWo, 2.0)) if P["tw_core"] else eps_k   # open: the core follows faster
        k = k + (eps_w * (1 + P["harden_k"] * open_ * (1 - support)))[:, None] * (z - k)   # alone, the shift hardens into the core
        if SEA_ON and sea_tr.any():   # and what the person became in it settles into the deep core
            k = k + (P["season_imprint"] * sea_tr)[:, None] * (z - k)
        if P["core_walk"]:   # v6: the deep core itself drifts a little, unnoticed, so people grow apart over decades (12-year
            cw_ = ((stage >= 2) * settle_f)[:, None] if SET_ON else (stage >= 2)[:, None]   # (F14: settling with age)
            k += P["drift_k"] * P["core_walk"] * centre(rng.normal(0, 1, (N, C))) * cw_   # value stability ~.5: Leijen 2022)
        ystep = P["asp_rate"] * (SP_[stage] * (1 + B) / (1 + TON * P["steady_want"] * P["steady_k"] * s_eff))[:, None, None]
        if SET_ON:   # F14: what they want settles with age as who they are does
            ystep = ystep * settle_f[:, None, None]
        asrc[:, AS_WEEKLY] += ystep * (dAs - dAs.mean(-1, keepdims=True))
        y = centre(y + ystep[:, 0] * centre(dA))
        M += 0.1 * np.abs(delta) * stakes
        re_ = react_eff * (1 - P["hz_calm"] * np.minimum(fhz, 1)) if P["hz_calm"] else react_eff   # v7: calmer as time feels short
        if P["mind_kid"] is not None:   # F19: a child carries less of what adds stress in a week than an adult
            re_ = re_ * float(np.interp(age, MK_A, MK_F))
        stress = _uclip((stress0 + re_ * (stress - stress0)) * 0.93 + re_ * 0.08 * np.maximum(0, -fdelta), 0, 3)
        B *= decay_B; TWo *= decay_B
        nic += P["nu_niche"] * (np.where(idle[:, None], nic, ma) - nic) + 0.002 * ((WP_ if UPL_ON and P["up_ease"] else P["world_profile"]) - nic) + P["era_niche"] * e_i * (e_p - nic)
        if RP_ON and P["role_niche"]:   # role_practice: the people of one's commitments, in their ways
            rsum_ = rw_.sum(1, keepdims=True)
            nic += P["role_niche"] * P["nu_niche"] * rsum_ * (rw_ / np.maximum(rsum_, 1e-9) - nic)
        if P["turnover"]:   # v6: the people around you change: new colleagues, friends, neighbours bring their own ways
            new_ = rng.random(N) < 1 / (52 * P["turn_years"])
            moved = new_.astype(float)
            if new_.any():
                circle[new_] = random_messages(rng, int(new_.sum()))
            nic += P["turnover"] * turn_pm[:, None] * np.asarray(P["turn_stage"])[stage][:, None] / 52 * (circle - nic)
        if WON:   # the world: the niche is what the settings and the close circle bring, with the times through them
            nic = np.array(WL.PP.niche, float)
            if STH_SOC is not None:   # v22.5, F12: and the start's society
                nic = (1 - P["start_soc"]) * nic + P["start_soc"] * STH_SOC

        for i in log_lives:
            if not idle[i]:
                more_ = dict(threat=round(float(thr[i]), 2))
                if ID2 and act_cw[i] > 0:
                    more_["cross"] = round(float(act_cw[i]), 2)   # N1b: the act crossed the role expected of them (people frowned)
                if MIS_ON:
                    more_["misread"] = round(float(mis_[i, a[i]]), 2)   # logit the felt odds were bent by (+ hopeful, - fearful)
                if WON and W_WHO_[s[i]]:   # who is in the moment: the cast member with the want first, else by role
                    more_["who"] = WL.who(i, int(s[i]))
                if WON and EYES_ON_ and EYEW_[s[i]]:   # S3, S4: the places of a caught-between or odd-one-out moment
                    ei_ = WL.eyes_info(i, int(s[i]))
                    if ei_:
                        more_["eyes"] = ei_
                if WON and LEADS_ON_ and LEADS_[s[i]] and getattr(WL, "lw", False):   # S7: the post the moment is about
                    li_ = WL.lead_info(i, int(s[i]))                                     # (its {place}, way, legitimacy)
                    if li_:
                        more_["lead"] = li_
                if SAC_ON_ and SACS_[s[i]]:   # S5: the line, the offer ({offer}), its round, size and refusal odds
                    si_ = WL.sacred_info(i, int(s[i]))
                    if si_:
                        more_["sacred"] = si_
                if WON and FARS_ON_ and FARS_[s[i]]:   # far_ties: the tie's town and what happened there
                    fi_ = WL.far_info(i, int(s[i]))
                    if fi_:
                        more_["far"] = fi_
                if SEEN_ON:   # S6: per option, the Library's word and the strongest model on its path, else its way
                    sn_ = WL.seen_info(i, int(s[i]))
                    if sn_:
                        more_["seen"] = sn_
                if WON:   # the world on the options (hooks §2.6, §2.8): each option's lever and where it lands; a move names towns
                    lv_ = WL.option_levers(int(s[i]))
                    if lv_:
                        more_["levers"] = lv_
                    if WL.move_s[s[i]] and hasattr(WL.PP, "move_options"):
                        more_["places"] = WL.PP.move_options(i)
                best_, bm_ = None, P["epi_recall"]
                mc_ = ma[i] - ma[i].mean(); nm_ = float(np.linalg.norm(mc_)) + 1e-9   # the act's lean among the colors
                for ep_ in epi[i]:
                    if t - ep_["last"] < 26:
                        continue
                    hl_ = P["mem_pos"] if ep_["success"] else P["mem_neg"]   # fading affect bias (a scar's pull is its own state)
                    st_ = ep_["w"] * 0.5 ** ((t - ep_["t"]) / (52 * hl_))
                    cs_ = 1.0 if ep_["situation"] == L["names"][s[i]] else float(mc_ @ ep_["mix"]) / (nm_ * ep_["nm"])
                    mt_ = st_ * cs_ if cs_ >= 0.7 else 0.0   # the same moment again, or an act leaning the same way
                    if mt_ > bm_:
                        best_, bm_ = ep_, mt_
                if best_ is not None:
                    best_["last"] = t
                    more_["recall"] = dict(age=best_["age"], situation=best_["situation"], choice=best_["choice"],
                                           success=best_["success"], scar=best_["scar"], strength=round(bm_, 2))
                events[i].append(dict(age=round(age, 2), stage=STAGE_NAMES[stage[i]],
                                      situation=L["names"][s[i]], choice=L["labels"][s[i]][a[i]],
                                      success=bool(succ[i]), delta=round(float(delta[i]), 3),
                                      push={ch: stepF[i, j].round(4).tolist() for j, ch in enumerate(CHANNELS[:5])},
                                      w=softmax(z[i]).round(3).tolist(), want=softmax(y[i]).round(3).tolist(),
                                      wanted=L["labels"][s[i]][best[i]], res=res[i].round(2).tolist(),
                                      gate=(("lacked the means" if not open_r[i, best[i]] else "not offered") if lost_open[i] else "unnoticed" if lost_seen[i]
                                                                               else "pulled away" if pulled[i] else "chosen"),
                                      ctrl=round(float(ctrl[i]), 2), **more_))
                if abs(delta[i]) >= P["epi_min"]:   # an act that hit hard becomes an episode the person may recall later
                    epi[i].append(dict(t=t, last=t, age=round(age, 2), situation=L["names"][s[i]], choice=L["labels"][s[i]][a[i]],
                                       success=bool(succ[i]), scar=bool(P["scar_k"] and not succ[i] and stakes[i] >= P["scar_min"]),
                                       w=float(abs(delta[i])), mix=mc_.copy(), nm=nm_))
                    if len(epi[i]) > 60:
                        epi[i].sort(key=lambda e_: e_["w"] * 0.5 ** ((t - e_["t"]) / (52 * P["mem_neg"])))
                        del epi[i][0]

        # ---- 6. rites of passage: an impactful event inside the next stage's window
        nxt = np.minimum(stage + 1, NS - 1)
        lo, hi = STAGE_LO[nxt], STAGE_HI[nxt]
        progress = _uclip((age - lo) / np.maximum(hi - lo, 1e-9), 0, 1)
        impact = np.abs(delta) / stakes * L["RIT"][s, nxt]   # only situations that can mark this passage count
        # a big surprise in a fitting situation may mark the passage; readiness grows across the window
        p_rite = 1 - np.exp(-P["rite_h"] * impact ** 2 * (1 + P["rite_ready"] * progress ** 2))
        rite = (stage < NS - 1) & (age >= lo) & ((rng.random(N) < p_rite) | (age >= hi))
        for n in np.nonzero(rite)[0]:
            quiet = bool(age >= hi[n] and impact[n] < P["rite_thr"] * 0.2)
            k[n] += P["rite_imprint"] * (z[n] - k[n])     # who you are now becomes your anchor
            B[n] += P["rite_boost"]; eps_k[n] *= P["stiffen"]
            stage[n] += 1
            if sea_fits(int(stage[n]), age):
                sea_open(n, int(stage[n]))                # the threshold season of the stage just entered
            rec = dict(life=int(n), age=round(age, 2), to=STAGE_NAMES[stage[n]], quiet=quiet,
                       event=None if quiet else f"{L['names'][s[n]]}: {L['labels'][s[n]][a[n]]} ({'success' if succ[n] else 'failure'})",
                       w=softmax(z[n]).round(3).tolist())
            rite_log.append(rec)
            if n in events:
                events[n].append(dict(rite=rec))
            if GON:   # v7 (2A): a rite seals dreams that have proved themselves into passions
                seal(n, "a rite of passage")
                if stage[n] == 2:   # coming of age: a strong dream that is not yet a passion becomes a plan (Emren 21:39)
                    for j in np.nonzero(gk[n] == 0)[0]:
                        if (gk[n] == 2).sum() < P["max_plans"] and rng.random() < P["dream_plan"] * gs[n, j]:
                            to_plan(n, j)

        # ---- 7. conversion: dissonance past threshold
        w = softmax(z)
        openness = np.sqrt(base / 0.9)
        theta = P["theta0"] * (1 + 2 * w) / np.maximum(openness, 1e-3)[:, None]
        D = np.minimum(D, 1.5 * theta)
        over = D >= theta
        if over.any():
            for n, c in zip(*np.nonzero(over)):
                acc = _uclip(1 - 0.4 * FR[c], 0.2, 1.4); acc[c] = 0   # framing shapes where you can go
                q = obs[n] * SE[n] * acc; q = q / q.sum()
                dz = centre(P["Lam"] * (q - np.eye(C)[c]) * min(2.0, D[n, c] / theta[n, c]))
                z[n] += dz; k[n] += 0.5 * dz; chan[n, 5] += dz
                y[n] = centre(y[n] + 2 * dz)          # a turning point is first a change in what you want
                asrc[n, 4] += 2 * dz
                B[n] += P["crisis"]; D[n] = 0
                steady[n] *= 1 - 0.5 * TON                    # a crisis shakes who one is
                conv_log.append((int(n), t, int(c), q))
                if n in events:
                    events[n].append(dict(conversion=dict(age=round(age, 2), disowned=COLORS[c],
                                                          toward=q.round(2).tolist(), w=softmax(z[n]).round(3).tolist())))

        # ---- 8. breakthrough: pent-up demand overcomes inertia (stick, then slip)
        q_thr = P["q_theta"] * np.maximum(hold_against, 0.2) ** P["q_hold"]
        # v6 (fresh-start effect: Dai, Milkman & Riis 2014; Alter & Hershfield 2014): a birthday, an age ending in 9, or a
        # change of surroundings lowers the bar for a change that has been building
        lm = float(t % 52 == 0) + 0.3 * float(int(age) % 10 == 9) + moved
        q_thr = q_thr * (1 - P["landmark"] * _uclip(lm, 0, 1))
        brk = (Q >= q_thr) & (gap > P["q_min_gap"]) & (stage >= 2)
        for n in np.nonzero(brk)[0]:
            dz = centre(P["q_step"] * (y[n] - z[n]))
            w0 = softmax(z[n])
            z[n] += dz; k[n] += 0.5 * dz; chan[n, 7] += dz
            B[n] += P["q_open"]; Q[n] = 0.0; sh_brk[n] = t
            steady[n] *= 1 - 0.3 * TON
            nic[n] += P["q_niche"] * (softmax(y[n]) - nic[n])
            force_re[n] = True                              # the commitment that fits worst comes up for decision
            rec = dict(age=round(age, 2), gap=round(float(gap[n]), 2), hold=round(float(hold_against[n]), 2),
                       before=w0.round(3).tolist(), w=softmax(z[n]).round(3).tolist(), want=softmax(y[n]).round(3).tolist())
            brk_log.append((int(n), t, rec))
            if n in events:
                events[n].append(dict(breakthrough=rec))
        if pausing:
            _ = yield Pause("end", t, locals(), None)
    z = bound_logratios(z, P["min_color"], P["max_color"]); y = bound_logratios(y, P["min_color"], P["max_color"])
    W_hist.append(softmax(z)); M_hist.append(M.copy()); S_hist.append(stage.copy()); A_hist.append(softmax(y))
    R_hist.append(res.copy()); K_hist.append(held * np.maximum(I, 1e-3))
    wout = WL.output(log_lives) if WON else None           # the outer world for the game (world-build.md, "Game data")
    return dict(world=wout, w=softmax(z), z=z, k=k, y=y, a=softmax(y), gates=gates, M=M, J=J, sig=sig, need=need, chan=chan, conv=conv_log,
                rites=rite_log, W_hist=np.array(W_hist), M_hist=np.array(M_hist), S_hist=np.array(S_hist),
                events=events, nic=nic, D=D, stage=stage, A_hist=np.array(A_hist),
                R_hist=np.array(R_hist), K_hist=np.array(K_hist), commits=commit_log, **({"births": birth_log} if (P["birth_free"] or P["birth_par"] is not None) else {}),
                V_hist={k_: np.array(v_) for k_, v_ in V_hist.items()}, A_src=np.array(A_src), breaks=brk_log, Q=Q, history=hist, outside=ev_log,
                clashes=clash_log + [(int(n), int(kk), int(clash0[n, kk]), T, "still living with it", round(float(clashI[n, kk]), 2), int(np.argmax(softmax(z[n]))))
                                     for n, kk in zip(*np.nonzero(clash0 >= 0))], held=held, I=I, prof=prof, res=res, tries=tries, wins=wins, blocked=blocked,
                sit_n=sit_n, sit_names=L["names"], life_events=lev_log, rebounds=reb,
                goals=goal_log, goal_state=dict(kind=gk, mix=gm, domain=gd, strength=gs, progress=gp, valued=gv, harmonious=ga,
                                                invested=gi, born=gb, due=gh, horizon=ghz, source=gsrc, trigger=gtrig, felt=gfelt,
                                                chance=gch, p_step=gph, by_player=gby, id=gid, aims=gtt,
                                                lost=dict(mix=lost_m, domain=lost_d, strength=lost_s, age=lost_t, on=lost_on, id=lost_id)),
                regret=regret, marks=dict(names=L["MARKS"], n=mark_n, last=mark_last, ok=mark_ok, log=mark_log), alive=alive,
                read_log=read_log, read_names=[e_["name"] for e_ in EVR], widowed=widowed, seasons=sea_log,
                identity=dict(female=female, attr=attr, unease=unease, gender_self=gender_self, intersex=intersex, ace=ace,
                              **(dict(named=named_g, came_out=came_o, partner_same=partner_same, role_fit=1 - rfit_avg,
                                      cross_title=cross_title, role_strict=RS0, accept_trans=AT0,
                                      found={k_: found_id[:, i_] for i_, k_ in enumerate(("gender", "attraction", "ace", "intersex"))})
                                 if ID2 else {})), died=died,
                cond_hold=cond_hold.sum(0) / max(cond_n.sum(), 1), drv_mean=drv_sum / np.maximum(drv_cnt, 1),
                chance_ref=dict(ref=ref_sum / np.maximum(ref_cnt, 1)[:, None], n=ref_cnt, earn=earn_sum / np.maximum(earn_cnt, 1),
                                earn_n=earn_cnt, p_option=pk_sum / np.maximum(pk_cnt, 1), n_option=pk_cnt),
                roles=(dict(names=GR["names"], kinds=GR["kindname"], NT=NT_, has=r_has, ever=r_ever, since=r_since, end=r_end,
                            access=p_acc, level=p_lev, log=role_log, profile=r_prof, pwords=GR["pwords"], refines=GR["refines"])
                       if RON else None),
                adjectives=dict(names=ADJ_NAMES[:NA_OUT], say=ADJ_SAY[:NA_OUT], has=adj[:, :NA_OUT], since=adj_since[:, :NA_OUT],
                                log=adj_log),   # with shadows off, without the shadow states (never held then)
                **(dict(asked=asked) if CU_ON else {}),
                **(dict(current=cur_sum) if CUR_ON else {}),
                **(dict(body=dict(body=body_v, mind=mind_v, conditions=dict(weight=bd_cw, kind=bd_ck, age=bd_ca, kinds=COND_KINDS),
                                  serious=dict(kind=bd_sk, since=bd_s0, until=bd_s1, kinds=SER_KINDS), kept=bd_keep,
                                  constitution=bd_con, resilience=md_res, threats=md_end, decline=dict(at=dl_at, since=dl_t0, cause=list(dl_cause))))
                   if HM_ON or DTH_ON else {}),
                **(dict(need_map=dict(person=NMP, shared=NMAP, needs=list(NEEDS))) if NM_ON else {}),
                **(dict(shadows=dict(states=SH_STATES, part=shS, force=shA, sources=sh_src, seen=sh_seen, last_seen=sh_rt,
                                     shown=sh_n, log=sh_log)) if SHON else {}),
                **(dict(areas=dict(names=AREAS, offsets=Dz, hist=D_hist,   # each area's colors are softmax(core z + offset)
                                   colors=softmax(z[:, None, :] + Dz, -1))) if DOM_ON else {}))


# ---------- pause points (backend plan item 2, 2026-10-08): the game's own way into the weekly loop
PAUSES = ("week", "situation", "choose", "odds", "learn", "end")
Pause = namedtuple("Pause", "kind t state value")   # what run_steps() yields; a plain 4-tuple to code that unpacks it

# The run's own variables the game, explain.py and foresee.py read at a pause: each is in the state at every pause from
# the first week the person is 3 (younger, a week has only its "week" pause). A name of this week's moment holds last
# week's value until this week sets it. Arrays are per person (N rows). tools/t_steps.py checks every name is there.
STATE = (
    # the run: settings, Library, week, age, switches, the outer world's link
    "P", "L", "t", "age", "RON", "AQ_ON", "SEA_ON", "TH_K", "TH_STEP", "TH_TR", "AT0", "RS0", "WL",
    # who the person is: colours (z, w), wants (y), core (k), maturity (M), skill and belief, habits, means, needs
    "z", "w", "y", "k", "M", "sig", "SE", "fb", "habit", "hold", "nic", "res", "need", "doors", "f_tot", "B", "X",
    # temperament and how life feels
    "mood", "content", "peace", "stress", "react", "steady", "base_mood", "outlook", "plast", "ctrl", "dsc", "support",
    "wound", "trouble", "fortune", "Q", "q_thr", "TWo", "fhz", "hzf", "gap_r", "regret", "earned",
    # commitments, people, body and identity, marks, seasons, tries
    "held", "I", "prof", "sat", "since", "stage", "alive", "dead", "died", "widowed", "female", "intersex", "found_id",
    "faith_given", "faith_drifted", "clash0", "act_cw", "rfit_avg", "adj", "adj_since", "adj_v", "mark_n", "had_ev",
    "missed_t", "events", "tries", "wins", "blocked", "sit_n", "sea_k", "sea_t0", "sea_done",
    # dreams, passions and plans (goal slots) and the helpers that change them
    "gk", "gm", "gd", "gs", "gp", "gh", "ghz", "gsrc", "gby", "gid", "gname", "gfelt", "gfelt0", "gplay",
    "new_goal", "end_goal", "quit_", "plan_odds", "dream_phrase",
    # this week's moment: situation, options, what pulls, the choice, the odds, the outcome, what it teaches
    "s", "s_ev", "rk", "recon", "m", "e", "e0", "diff", "mask", "closed_s", "stakes", "alpha", "do_nothing", "lack",
    "lackf", "earn", "pbump", "serves", "relief", "rel", "wR", "gU_R", "gU_I", "w_hat", "a_hat", "V", "VA", "H", "hzU",
    "step", "tryf", "U_R", "U_I", "U", "read_", "readk_", "open_r", "open_", "seen", "pr", "p_hat", "a", "ma", "ea", "ph", "idle",
    "p_true", "succ", "delta", "span", "stepF", "role",
    # the player's steer (P["steer"]): the pick's odds without it, and how much it moved the drawn option's odds
    "pr0", "steer_moved",
    # light and shadow (stage 2, item 2): each colour's shadow part, its force, the four sources (holding on, ruling, no
    # counterweight, strain), seen, and the character's own pick before the player's ("a_self" at the choose pause and after)
    "shS", "shA", "sh_src", "sh_seen", "SHON",
    # a curious, thinking life (stage 2, item 7 C4): how much others come to them for answers, 0 to 1
    "asked", "CU_ON",
    # each person's own colour-to-need table (stage 2, P4): needs x colours, from the shared table
    "NMP", "NM_ON",
    # the times as a steady current (item 12): how much it has moved each life's colours so far
    "cur_sum", "cur_m", "CUR_ON",
    # v22.5 F1 and F2: the body and the mind (health's two halves, 0 to 1), the end week of each threat (a low season,
    # anxiety, numbing; NEVER or past: none), a last decline's end and start weeks (NEVER: none) and cause, the long-term
    # conditions (weight, COND_KINDS index, -1 none) and a serious illness now (SER_KINDS index, -1 none), and the switches
    "body_v", "mind_v", "md_end", "dl_at", "dl_t0", "dl_cause", "bd_cw", "bd_ck", "bd_sk", "HM_ON", "DTH_ON",
    # colours settle with age (v22.5, F14): this week's factor on plasticity, 1 with set_age off (the game's lean_self can
    # follow it, so steering an older life is harder too)
    "settle_f",
    # the times: this week's era strength and its colour mix (the era's pull, e_i * (e_p - 0.2) in the world's rewards)
    "e_i", "e_p",
    # the world in their life: this week's effects on each life (lists of dicts) and the causes behind each option
    "wfx", "option_causes",
    # the run's logs
    "ev_log", "goal_log", "brk_log", "conv_log", "rite_log", "commit_log", "clash_log", "role_log", "adj_log",
    "mark_log", "read_log",
)
# names there only when a switch in the state is on: titles (the packs' roles), name -> switch
STATE_IF = dict.fromkeys(("r_has", "r_ever", "r_since", "r_prof", "p_acc", "p_lev", "p_sus"), "RON")


def run(N=1000, years=80, seed=0, P=None, record_every=52, intervention=None, lib=None, log_lives=()):
    """Run N lives for `years` years and return everything the run kept (see the end of _run)."""
    g = _run(N, years, seed, P, record_every, intervention, lib, log_lives, False)
    try:
        next(g)
    except StopIteration as done:
        return done.value
    raise RuntimeError("engine.run() paused, which it never should (pausing is off)")


def run_steps(N=1000, years=80, seed=0, P=None, record_every=52, intervention=None, lib=None, log_lives=()):
    """The same run as run(), as a generator that pauses six times a week (the game drives one life with it).

    Each pause yields Pause(kind, t, state, value): kind is one of PAUSES, t the week, state the run's own variables
    at that moment (a dict; STATE names the ones the game, explain.py and foresee.py may read) and value the one
    thing the caller may change. Send the value back, changed or not (None for "week" and "end"):
      "week"       start of the week, after the outside-world intervention    value None
      "situation"  after the week's situation is drawn                        value s, the situation per person
      "choose"     right after the person picks an option                     value a, the option per person
      "odds"       just before the outcome is drawn                           value p_true, the true chance
      "learn"      right after the surprise of the outcome is worked out      value delta, the prediction error
      "end"        end of the week                                            value None
    Before the person is 3 a week has only its "week" pause; from then on every week has all six, in this order.
    Sending every value back unchanged gives exactly the life run() gives. When the life ends the generator returns
    run()'s result (StopIteration.value)."""
    return _run(N, years, seed, P, record_every, intervention, lib, log_lives, True)


# ---------- the four color vectors of a person at a given year (Emren, 2026-10-04): a reading of the state
def color_vectors(o, i, yr):
    """Per color, for person i at age yr (whole years):
    position     where the person is: motive weights (sum to 1)
    demand       where they want to move: aspiration minus position (sums to 0); demand_sources says what moved
                 the want over the last five years (log-ratio units), pressure is the discontent built up by blocked
                 wanting and threshold the pressure their inertia can hold back
    accelerator  how fast they can move toward each color now: readiness (plasticity x self-control, opened up by
                 crises) x belief they can act that way x doors (the world and their means let them)
    inertia      how strongly they hold on to each color, above (+) or below (-) an even share: deep core 40%,
                 habit 30%, the roles of their commitments 30%. Holding is what stops a want from becoming change
    velocity     how they actually moved over the last year"""
    V = o["V_hist"]; w = o["W_hist"][yr][i]; a = o["A_hist"][yr][i]
    role = V["role"][yr][i]; role = role / role.sum() if role.sum() > 0 else np.full(C, 0.2)
    core, habit = V["core"][yr][i], V["habit"][yr][i]
    hold = 0.4 * core + 0.3 * habit + 0.3 * role
    ready = V["plast"][yr][i] * V["ctrl"][yr][i]
    belief = V["SE"][yr][i] / 0.5; doors = V["doors"][yr][i]
    give = np.maximum(0, w - a); give = give / give.sum() if give.sum() > 0 else np.full(C, 0.2)
    hold_against = 5 * (give * hold).sum()
    src = o["A_src"][yr][i] - o["A_src"][max(yr - 5, 0)][i]
    return dict(position=w, demand=a - w, demand_strength=0.5 * np.abs(a - w).sum(),
                demand_sources={nm: src[j] for j, nm in enumerate(ASOURCES)},
                pressure=float(V["Q"][yr][i]), threshold=float(DEFAULT["q_theta"] * max(hold_against, 0.2) ** DEFAULT["q_hold"]),
                accelerator=ready * belief * doors, readiness=float(ready), belief=belief, doors=doors,
                inertia=hold - 0.2, inertia_parts=dict(core=core - 0.2, habit=habit - 0.2, roles=role - 0.2),
                velocity=w - o["W_hist"][max(yr - 1, 0)][i])


def meta(o, i, yr):
    """Emren's four meta variables (2026-10-04) for person i at age yr.
    satisfaction  how content they are (0..1): needs met, versus what they got used to, recent luck, ideal-self gap
    peace         how tranquil they are (0..1): low stress, no ought conflict, no inner color tension, no pent-up demand
    mindset       how they perceive: lens = deep core shares (decides what they notice), belief = self-efficacy per color
    skillset      how they can shape reality: skill per color (decides how often acting that way works)"""
    V = o["V_hist"]
    return dict(satisfaction=float(V["content"][yr][i]), peace=float(V["peace"][yr][i]),
                mindset=dict(lens=V["core"][yr][i], belief=V["SE"][yr][i]), skillset=V["skill"][yr][i],
                parts=dict(needs_met=float(V["fneed"][yr][i]), mood=float(V["mood"][yr][i]), stress=float(V["stress"][yr][i]),
                           ought_conflict=float(V["cload"][yr][i]), color_tension=float(V["tension"][yr][i]),
                           pressure=float(V["Q"][yr][i])))


def temperament(o, i, yr):
    """Temperament (v5, Emren 2026-10-04): never preset; learned from the life lived, fastest in childhood.
    reactivity    how hard events hit (1 = average): a harsh or unpredictable life raises it, safety and belonging lower it
    steadiness    how firmly the person holds who they are (0 = not at all): succeeding in what they hold, keeping
                  commitments and being who they want to be build it; crises, breakthroughs and leaving shake it
    baseline_mood their own usual satisfaction (0..1), a slow average of how life has gone
    outlook       sense of control (0..1): the share of wanted attempts that worked out, weighted by stakes"""
    V = o["V_hist"]
    return dict(reactivity=float(V["react"][yr][i]), steadiness=float(V["steady"][yr][i]),
                baseline_mood=float(V["base_mood"][yr][i]), outlook=float(V["outlook"][yr][i]))


# ---------- identity labels (display convention; not a force in the engine)
GUILD = {"W": "mono-White", "U": "mono-Blue", "B": "mono-Black", "R": "mono-Red", "G": "mono-Green",
         "WU": "Azorius", "UB": "Dimir", "BR": "Rakdos", "RG": "Gruul", "WG": "Selesnya",
         "WB": "Orzhov", "UR": "Izzet", "BG": "Golgari", "WR": "Boros", "UG": "Simic",
         "WUG": "Bant", "WUB": "Esper", "UBR": "Grixis", "BRG": "Jund", "WRG": "Naya",
         "WBG": "Abzan", "WUR": "Jeskai", "UBG": "Sultai", "WBR": "Mardu", "URG": "Temur",
         "WUBR": "Artifice (no G)", "UBRG": "Chaos (no W)", "WBRG": "Aggression (no U)",
         "WURG": "Altruism (no B)", "WUBG": "Growth (no R)", "WUBRG": "Five-color",
         "": "Colorless (unformed)"}


def identity(w, M, prev="", M_formed=6.0, enter=0.22, leave=0.18):
    """A color is part of the identity when it holds more than an even share (0.2; Emren, 2026-10-04).
    A +-0.02 buffer stops colors hovering at 0.2 from flickering: a color joins above 0.22 and leaves
    below 0.18. Without a previous label, nothing above 0.22 means nothing stands out: five-color."""
    if M < M_formed:
        return ""
    keep = (w > enter) | ((w > leave) & np.array([c in prev for c in COLORS]))
    return "".join(c for c, k in zip(COLORS, keep) if k) or COLORS


def identity_path(W, Mh):
    """Labels year by year for one life (W: years x 5), carrying the buffer forward."""
    out, prev = [], ""
    for w, M in zip(W, Mh):
        prev = identity(w, M, prev); out.append(prev)
    return out


def shape(label):
    n = len(label)
    if n == 0: return "unformed"
    if n == 1: return "mono"
    if n == 2:
        return "ally pair" if A[IDX[label[0]], IDX[label[1]]] > 0 else "enemy pair"
    if n == 3:
        idx = [IDX[c] for c in label]
        allies = sum(A[a, b] > 0 for a in idx for b in idx if a < b)
        return "shard (ally triad)" if allies == 2 else "wedge (enemy triad)"
    if n == 4: return "four-color"
    return "five-color"
