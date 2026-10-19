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
import ast
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
from realm_earth import NEED_MAP_V7, COMMIT_MEETS_V7, IMP_AGE   # needs that fit life (need_tab "v7", imp_age): Earth's
NMAP_V7 = np.array(NEED_MAP_V7, float)
from realm_earth import HEIGHT_NAMES   # aims v1: Earth's names of the three heights
AIM_HEIGHTS = ["Known", "Notable", "Historic"]   # a step's height: 0 none, 1 Known, 2 Notable, 3 Historic
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
TIERS = ["everyday", "life event", "inner", "echo", "engine", "return"]
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
    soc_own=0.0,         # G19w (v22.5): with the world on, the share of the people who shape them (the social pull and the
                         # current's close people) that is the company they pick by what they do, following their acts as the
                         # niche does with the world off; the world's settings and circle are the rest (people pick friends
                         # like themselves and become more alike: Kandel 1978; McPherson, Smith-Lovin and Cook 2001). 0: the
                         # world's alone, so a life's choices never reached the people around it
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
    cause_fit=True,     # E2 (every-change-has-a-cause.md): the Library's cause audit's tightened title and perk rules
                         # (earth_rules.ROLES_FIT) in place of the loose ones, so a gain's cause reads true
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
    # picks come back (chroma-ideas/gameplay-2026-10-17/picks-come-back.md): set only by the game for a played life. A pick
    # the player was asked (echo_asked, set by the game at its checkpoint and spent here) whose way leaves a mark: or names
    # back: plants a seed: its kind, week, moment, way and whether it went well. A share p of seeds fall due after delay
    # years; a due seed comes back at w a week (weeks with no life event, at least gap years after the last return, until keep
    # years past due) as one moment of its kind and side never met (else not met for again years): a return moment (tier: return, of:, side:) or a mark echo
    # anchored on that kind (whose own clock it then clears). An ordinary echo of a kind with a waiting seed is that seed's return.
    # Tuned 10-17 with the Library's back: tags and RETURNS (#271): about 8 returns in a played life of about 85 asks
    echo_play=False, echo_asked=False,
    # every change has a cause (E1): for a played life only (events), each title or perk gained "in time" records the clause
    # of its rule that held and the history behind it (the mark and its moment, the moment met, the title or perk built on,
    # money, age), and each lost as time passed or slipped away how long it was held and unused; read-only (no draw), so
    # every life plays the same with it on or off. The game's causes switch turns it on
    role_why=False,
    # need_why (WS1, "because of you, and meanwhile"; chroma-ideas/next-table-2026-10-19/plan.md section 1): a record of
    # why each need moved this week, by source (NSOURCES): nw, N x NSOURCES x needs, from the start of the week (before
    # the "week" pause) to the "end" pause, summing exactly to the week's change (what the clip to 0..1 takes off goes
    # back to the week's moves of its sign, pro rata), and nw_imp, the week's silent setback (IMPOSITIONS index, -1
    # none). Read-only (no draw): every life plays the same with it on or off. Changes the caller makes at the "end"
    # pause fall in no week's record
    need_why=False,
    # needs that fit life (the next stage's workstream 4; chroma-ideas/next-table-2026-10-19/needs-research.md), each off
    # until the joint refit: need_tab "v7" reads the colour-to-needs table and what commitments meet from realm_earth
    # (NEED_MAP_V7, COMMIT_MEETS_V7: a partner gives meaning, each colour a meaning of its own); shared_hist, the most of
    # an act's belonging gain that also feeds meaning (shared history: shared_hist_par's share with no close bond,
    # rising to shared_hist as the longest held partnership, children or community lasts, halfway in its years); imp_age,
    # setbacks only from the age each can happen at (realm_earth.IMP_AGE)
    need_tab="v7", shared_hist=0.2, shared_hist_par=(0.10, 5.0), imp_age=True,   # on at the v24 refit
    # aims v1 (the next stage's workstream 5; plan.md section 5), off until the joint refit; needs the batch's aims
    # (batch.AIMS or load_batch(aims=True)). An aim is a ladder of steps (titles or perks held or once held) toward what a
    # person wants to become, in up to aims_par slots: one grows from below out of a dream, passion or plan whose
    # concrete dream it names or whose domain and colours it fits (fit, the lean's cosine), or the player sets one (it
    # stays "set by you", pulling at reluctant, the spark moment sought at spark_seek, until a try at its spark moment
    # works and a rite or the moment's own seal makes it theirs). It raises the odds of moments with a way into its next
    # step (seek, by its strength) and each step reached meets meaning (meet, by the step's height: none, Known,
    # Notable, Historic). With no goal behind it an aim fades (half, in years; half_set for one not yet their own) and
    # goes below drop. A calling: an aim of their own that leads to a height, held as a passion for call_yrs
    aims=True,   # on at the v24 refit
    aims_par=dict(slots=3, fit=0.3, seek=1.0, reluctant=0.5, spark_seek=2.0, meet=(0.03, 0.06, 0.09, 0.12), half=4.0,
                  half_set=2.0, drop=0.05, call_yrs=3.0, set_s=0.5, spark_up=0.15),
    # the heights of a life (plan.md section 5), read-only: the week each height (Known, Notable, Historic) was first
    # reached (realm_earth.HEIGHT_NAMES, leading a sphere (rung 4), a summit title, leading a movement); on with aims
    heights=True,
    # the world answers v1 (the next stage's workstream 6; chroma-world/spheres/world-answers-v1.md, values in
    # sphere_data.WORLD_ANSWERS), off until the joint refit; with the world. The forest and the tree: no life moves
    # nothing. Its parts each have a sub-switch, read only with world_answers on: wa_groups (A: a member's presence leans
    # their settings' ways, kept beside the norm; a good voice, found or lead act grows the setting), wa_places (B: a
    # regular leans their haunts a little each year; a place they lead closes less often), wa_ledger (D: record only,
    # what each life moved by unit, told when a unit passes a step: the run's wa_ledger, events' wa_ledger), wa_notice
    # (E: the world notices the goal pursued: the people met, the haunt pick, the sphere's asks with the batch's world
    # answers moments, its events and offers; no moment odds of its own). wa_phase2 (F, off on its own): a Known life
    # (aims v1's heights: Known reached, its standing still held) decides for others in the sphere it stands in, 4 to 8
    # times a year (8 to 12 at national standing), with rivals, allies and a successor, at a price in hours and stress
    world_answers=True, wa_groups=True, wa_places=True, wa_ledger=True, wa_notice=True, wa_phase2=True,   # on at v24
    # footprints (the next stage's workstream 3; plan.md section 3), off until the joint refit; needs the batch's FOOT
    # (batch.FOOT or load_batch(foot=True)). Each picked option's footprints get real state (run_03_moments.py, the
    # footprints): a person in the cast (off-world, ties by foot_par ties), a haunt, a means, a mark or door (one only a
    # return reads shuts after foot_par door_yrs), a lesson told
    foot_on=True, foot_par=dict(ties=0.05, door_yrs=5.0),   # on at the v24 refit
    echo_play_par=dict(p=0.6, w=0.3, delay=(1.0, 8.0), keep=10.0, gap=0.5, again=12.0),
    # bold ways (chroma-ideas/gameplay-2026-10-17/bold-ways.md): set only by the game for a played life, with the batch's
    # BOLD_MOMENTS. In a week the game asks (bold_ask, set at the situation pause and spent at the choice; "all": every
    # week), a moment with the Library's bold ways (<world>_play.BOLD) has up to two bold slots beside their base ways:
    # the base way's gates and pull, its odds moved by the written chances' logit gap, plus likelier_if: points, between
    # .1 and .9 (bold_now's p_act at the choose pause; its p, the card's, also counts the chance F16 keeps a win that
    # starts a partnership, children or a faith not held, which r_gain still draws). The character's own pick re-picks with the week's own draw over the ways
    # and the slots (a slot weighs its base way's share x exp of the utility its odds change); the game may take a slot
    # (bold_take, the slot, with a = its base way; -1: an ordinary way). A bold pick is its base way drawn at the bold
    # odds, with the row's act fields and mark in place of the base way's. With echo_play on it plants a seed of kind
    # bold:<moment>/<colour> due inside its links' delay: (ep_rng), at most bold_cap a life, none in a link's own week (one
    # link deep); a seed with no link of its own open takes a shared link of its kind of change and side (of_change:)
    bold_play=False, bold_ask=False, bold_take=None, bold_cap=6,
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
    grey_gate=True,    # finishing pack, part 5 (Emren's "Parts 1 to 5", 10-17): a moment with shadow: (a sphere, or town)
                        # comes only while that sphere's grey share in their town is at least .25 (sphere_data.SHADOW;
                        # the Library's Crime pack moments join with batch.SHADOW_MOMENTS); grey_y reads the shares yearly
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
    place_turnover=True,   # spheres finishing pack, part 2 (chroma-world/spheres/finish-pack-draft.md): the named places
                            # close (a hazard and three town events) and new ones open; their regulars lose the haunt, a
                            # rung and half the ties made there, a keeper the post (world switch, with sph_haunts; the
                            # moments cast_want place_closed, place_opened come only with it, batch.TURNOVER_MOMENTS)
    body_trust=True,   # the spheres' finishing pack, part 3: trust in a sphere's bodies per life and sphere (btrust; world
                         # switch, with sph_fair; chroma-world/spheres/finish-pack-draft.md, sphere_data.TRUST): it tilts the
                         # levers, care seeking and the felt odds of pursuits in those bodies, and gates trust: moments
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
    # spheres finishing pack, part 4 (chroma-world/spheres/finish-pack-draft.md): former inmates as ties
    # (sphere_data.DEEP service.after_prison.tie_values). Off by default; world on only (the ties are People's; world off
    # the switch does nothing). prison_par: years_unknown, the years inside when [ex-prisoner] comes by its rule with no
    # term known; cap, the most ties one release makes; active, the closeness at or above which a tie is still active
    # (layer 4's line, .02: still among the 150 they know); pull, the re-offending pull (None: the data's 1.2); shadow,
    # the lead colour's shadow part over which their way leans to its shadow side (the pull back's gate); test, (age,
    # years): every life starts a term at that age (checks only; None: never)
    prison_ties=True,
    prison_par=dict(years_unknown=2.0, cap=6, active=0.02, pull=None, shadow=0.3, test=None),   # shadow .3: v22.6 refit (.5 never fired)
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
    skill_room=None,     # G19w (v22.5): practice is shared: the acts in a skill's ways keep up this much of the skills held in
                         # those ways (each held skill counts by the share of its ways it shares: two skills in the same two
                         # ways count 1), and a skill among more is used as much less, so it can slip away (skills fade
                         # without practice: Arthur, Bennett, Stanush and McNelly 1998). None: each skill kept up alone
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
    up_fam=0.0,          # where the start is a culture (world off: the clan, the towers) its lean comes through the family: each
                         # household's own ways are drawn around the society (Dirichlet, concentration up_conc a colour, its own
                         # random stream) and are the family a child first admires (fam); the life leans toward this share of
                         # them and the rest of the start's colours, so households differ as values differ more within a
                         # culture than between cultures (Fischer & Schwartz 2011). With the world on the upbringing is the family's
                         # own already (its world people), so Earth lives are untouched
    up_conc=0.3,         # up_fam: how alike the households of one culture are (lower = households differ more)
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
    ev_gapfit=None,      # F9.13: {life event: (lo, hi) years}, the gap before it comes again where the Library gives none (as
                         # ev_gap: none before lo years, fully likely by hi); a home is bought, then moved up or down years later
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
    pay_col2=((0.0, 0.18, 0.04, 0.0, 0.0), (0.0, 0.4, 0.1, 0.0, 0.0)),   # v22.6 refit: pay_col in its place (Blue's
                         # pay lean .08 to .18: with the spheres pack on, Blue's money at 30 to 70 fell under the others',
                         # F9.40); None: pay_col as v22.5 set it
    tie_col=None,        # F9.40 (world on): the colours lean ties: tie_k x exp(tie_col . (5 w - 1)) (five weights). None: even
    work_die=None,       # F9.29 (world on): a death at work, a work-year at this x the job's danger (None: .0005, about
                         # seven times the real rate of deaths at work, about 3 in 100,000 workers a year)
    low_net=None,        # F9.38: (years, level, help): after that many years with the money (over about a season) at 5% or less,
                         # help comes (benefits, family, a way out found) for help years: the money is at least level while it
                         # lasts, then the life's own means take over again; None: as before
    pen_pay=None,        # F9.38 (with low_pay): a career's pension x exp(lp_mu + s z - s^2 / 2), s = pen_pay x the job's pay
                         # spread, z the last job's pay draw (its rank, not faded with the years in it); None: as before
    low_pay=None,        # F9.38 low pay: (sd, rho, half): each job's pay x exp(sd z d - (sd d)^2 / 2), mean 1, z drawn at each
                         # job start or change of employer (rho of it the last job's: pay follows a life), d halving every half
                         # years in the job (low pay is mostly a first step: pay rises with experience); own stream. None: as before
    age_free=None,       # F9: [life event, ...] that come by their age window at their highest stage rate, not by the life stage
                         # reached (a stage can begin years after its window opens); "your first full-time job" for F9.38
    age_rate=None,       # F9.24: [life event, ...] whose rate rises with age, read between the stages' per_year, each at the
                         # end of its window (where lives begin that stage), not stepping up only when the next stage begins
                         # (stages mostly begin at their window's end, elder at 80: a 70-year-old fell ill at the midlife rate)
    age_pts=None,        # F9.23 (with age_rate): {life event: ((age, per_year), ...)}, its own rate points by age in place of the
                         # stages' per_year and ev_fit (a child version counts as one); flat beyond the last point. None: as before
    birth_par=None,      # F9.3 (with birth_age): a life's own births x this factor by the children it has living (0, 1, 2, ...;
                         # the last for more): fewer go on to a third or fourth child. None: as before
    ti_fit=None,         # F9: {title: factor} on its yearly rate (the Library's or the packs' rule), fitted to Release's rows
                         # (records/v22.5/scope.md); "living together" for F9.6. None: as written
    loan_end=False,      # F9.15: a home loan whose term ends is paid off (its payments came out of the income all along); off:
                         # it breaks, and the home goes with it, if the money is under .1 that month
    home_sale=1.0,       # F9.15: in a hard year under the need line, the home itself is sold in this share of cases (other
                         # holdings still go first); otherwise the household gets by, cutting back and borrowing. 1.0: always
    birth_free=False,    # F9.2 to F9.4 (with birth_age): a life's own births come by its age (the moment's age window, at
                         # its highest per_year), not by the life stage it has reached; birth_age's taper then shapes them
    birth_with=None,     # F9.2: a life's own births x these factors by its partnership: (no partner, a partner not living
                         # together, a home together, the years a partnership, or a home together, takes to reach its full
                         # rate, from 0), so most first births follow setting up home by a few years. None: as before
    nest=None,           # F9.5: the children leave home when the youngest is grown: (the youngest's age in years, the yearly
                         # rate from then, by age not the life stage). None: 16 years after the first child, at the stage's rate
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
    # S7 (lead_ways) with v22.5's money, the yearly custom read and a founder leading as an owner
    # (world_people.LEAD_DEFAULT): seeds 41-52, 300 x 80, falls per way and time in post per lead colour back within
    # 1.5x and 1.2x
    lead_par=dict(fav_drop=0.88, fast_gap=52, fast_k=0.86, owner_kind=True, crisis=0.30),   # crisis (round 3e, S7): a crisis breaks
                         # a rules, knowing or inspiring leader's way a little more often (.25: White's work posts led longest)
    dream_grow=True,
    own_open=True,
    start_hold=True,
    set_age=((30, 1.0), (50, 0.12), (70, 0.02)),
    up_lean=0.006,
    up_self=0.05,
    up_ease=1.0,
    up_fam=1.0,
    up_conc=0.2,
    up_half=4.0,
    up_l0=0.4,           # v23 (K14 F15): with the v22.6 content start 2's (W.6 G.4) lean at 35 stayed near .70 of its lean
                         # at 15 on 120 seeds (target .35 to .65; v22.5 .61); .35 still read .71, as the pull acts only below
                         # up_l0 and the lean at 15 sat at .35. At .40 (120 seeds): starts 2, 3, 4 read .589, .402, .486
    course=True,
    deed_canon=2.0,
    deed_rare=0.15,
    mind_kid=((10, 0.5), (18, 1.0)),
    mind_u=((45, 0.0), (50, -0.15), (58, 0.0), (68, 0.45), (80, 0.6)),
    death_par=dict(frail=(1.25e-07, 0.15), frail_k=1.5, ser_age=0.016, frail_c=0.00015, frail_late=(92, 0.25), decline_k=2.0,
                   acc=((0, 5e-5), (15, 2e-4), (20, 3.5e-4), (30, 2.8e-4), (70, 3e-4), (85, 1.2e-3), (100, 3e-3))),
    # round 3e (F9.35, F9.28): fewer young deaths of a failing heart (frail_c .00025), a few more young accidents
    body_par=dict(dip_level=True),
    course_mu=(-0.55, -0.2, -3.5),
    pension_k=0.55,
    pension_base=0.15,
    drv_self=True,
    risk_norm=True,
    par_age=((16, 0.0), (19, 0.35), (24, 1.0)),
    tie_k=1.75,
    par_split=0.05,
    ill_real=True,
    kid_cost=0.15,
    hh_cls=(0.12, 0.3, 0.55),
    ev_fit={'losing your job': 0.45,
            'a serious accident or illness': (1, 1, 0.25, 0.25, 1.6, 4.5),
            'a long dark season': 0.65,
            'an addiction takes hold': 0.63,
            'living with a chronic illness': 0.75,   # its rate by age is age_pts below
            'your first full-time job': 1.5,
            'a new job at last': 0.35,
            'buying a home': (1, 1, 1.8, 1.0, 0.7, 0.07),
            'divorce after twenty years': 0.2,
            'a child is born': 0.4,
            'a baby on the way, planned or not': 0.1},
    ev_gapfit={'buying a home': (3, 8)},   # F9.13 (round 3): a home is bought again only 3 to 8 years on, not a year later
    set_big=6.0,
    cond_once=True,
    job_move=((18, 0.22), (25, 0.14), (35, 0.08), (45, 0.05), (55, 0.03), (64, 0)),
    birth_free=True,
    home_sale=0.065,
    loan_end=True,
    ti_fit={'living together': 4.5},
    birth_par=(3.0, 0.3, 0.16, 0.1, 0.06, 0.03),
    birth_with=(0.02, 0.8, 3.0, 5.0),
    nest=(18, 0.3),
    age_free=('your first full-time job',),
    age_rate=('a frightening diagnosis', 'a serious accident or illness', 'buying a home', 'living with a chronic illness'),
    # F9.14, F9.23 (round 3c): a home and a lasting illness by age between the stages' rates (most 60-79s are still 'mature')
    # F9.23 (round 3d): a lasting illness by its own points: lower to 40, rising through 60-77, back to the old elder rate after 80
    # (past 80 new ones only widened the old-age health spread, F9.37); a year's rate before the drivers
    age_pts={'living with a chronic illness': ((0, 0.0045), (12, 0.003), (25, 0.004), (36, 0.0052), (45, 0.0125), (60, 0.021),
                                               (70, 0.046), (77, 0.06), (82, 0.03))},
    mon_drift=0.015,
    lone=dict(age=((13, 0.03), (16, 0.014), (18, 0.003), (25, 0.009), (30, 0.012), (35, 0.014), (50, 0.014), (60, 0.012),
                   (70, 0.008), (80, 0.004), (95, 0.003)), single=0.7, work=0.5, low=1.0, ill=0.4, out=0.35, keep=0.05, rate=0.05),
    low_pay=(1.6, 0.3, 3.0),
    pen_pay=0.9,
    low_net=(3.0, 0.1, 1.0),
    pay_col=((0.0, 0.08, 0.04, 0.0, 0.0), (0.0, 0.4, 0.1, 0.0, 0.0)),
    tie_col=(0.3, 0.0, 0.0, 0.0, 0.05),
    kid_tie=0.6,
    job_gap=(0.35, 0.1, 2.5),
    pair_pay=0.12,
    work_die=0.00007,
    retire_hz=((50, 0.0), (54, 0.0), (56, 0.045), (58, 0.05), (60, 0.035), (61.9, 0.035), (62, 0.11), (65, 0.12), (67, 0.15),
               (70, 0.18), (80, 0.24)),   # F9.22: poorer old age kept more at work past 70
    c_par=dict(sold=0.03, merged=0.015),
    eyes_par=dict(odd_vmem=0.05, pair_norm=0.01),   # S4: the spread of their places' shares learnt over about twenty years
                         # (world_people); pair_norm (round 3e, S3): the caught-between pair is the split that stands out against
                         # each pair's usual gap (UR was met least, 1.55x)
    soc_own=0.2,
    skill_room=1.0,
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
# body_trust (finish-pack-draft.md part 3; dynamics.json body_trust effects, not among sphere_data.TRUST's numbers): care
# seeking for an illness x (.7 + .6 x btrust[care])
BT_CARE = (0.7, 0.6)


def bt_care(lean_c, bc):
    """body_trust: care seeking (1 + the early-care lean) x (.7 + .6 x btrust[care]), read back as the lean; a life whose
    trust has not started (NaN) keeps its lean. tools/t_steps.py reads its direction."""
    return _uclip((1 + _uclip(lean_c, -1, 1)) * np.where(np.isnan(bc), 1.0, BT_CARE[0] + BT_CARE[1] * bc) - 1, -1, 1)


def pt_pull_of(act, shadow, thr, partner, steady):
    """prison_ties, the pull back: on while a former-inmate tie is active and the lead colour's shadow part is over thr,
    and the life holds neither a partner nor steady work (Sampson and Laub 1993). tools/t_steps.py reads it."""
    return act & (shadow > thr) & ~partner & ~steady


def pt_pull_u(U, pull, bl, tau, f):
    """prison_ties, the pull back on the choice: the options that break the law (bl) at odds x f for the lives pulled
    (log odds x the choice's tau)."""
    return U + np.log(f) * (pull[:, None] & bl) * tau[:, None]
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
from realm_earth import FERT_F, FERT_M, BIRTH_OWN, BIRTH_NOT, HOME_TOGETHER   # Earth's (realm_earth.py)


def toward(lv, m):
    """v22.5 F1: a level lv (0 to 1) moved by m: one for one going down (to .01), with diminishing returns going up, so a
    strong body or a steady mind nears 1 without passing it."""
    return np.where(m < 0, np.maximum(lv + m, 0.01), lv + (1 - lv) * (1 - np.exp(-np.maximum(m, 0) / (1 - lv))))


def fert(age, table):
    """A year's chance of a birth at this age as a share of the peak age's (FERT_F, FERT_M)."""
    xs, ys = zip(*table)
    return np.interp(age, xs, ys) / max(ys)


from realm_earth import (BODY_PAR, BODY_MOMENTS, MIND_MOMENTS, CO_TITLES, SPLIT_SOFT, COND_KINDS, COND_P, COND_LETHAL,   # Earth's
                         COND_DEATH, SER_KINDS, MIND_PAR, DEATH_PAR)                                                    # (realm_earth.py)


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
               sph_shadow=False, grey_gate=False, sph_deep=False, far_ties=False, sph_titles=False, fair_read=False, lead_ways=False, lead_par=None,
               # spheres finishing pack, part 4: former inmates as ties
               prison_ties=False, prison_par=dict(years_unknown=2.0, cap=6, active=0.02, pull=None, shadow=0.5, test=None),
               sph_eyes=False, sph_odd=False, sacred=False, seen_done=False,
               # the spheres finishing pack (finish-pack-draft.md): part 2, places close and open
               place_turnover=False,
               # the spheres' finishing pack: trust in a sphere's bodies (part 3)
               body_trust=False,
               # item 11, the world in their life: WL2's small effects
               wl2=False, near_gate=False,
               # late births: a life's own births by real fertility for its age and sex
               birth_age=False,
               # what one holds is practice too
               role_practice=False, read_skill=0.0, lens_want=0.0, app_vigil=False, sh_will=0.0, cur_will=0.0, gap_move=0.0,
               # v22.4: a refused first job or job move re-draws to the next-best fit
               acc_redraw=False, green_jobs=False, cause_fit=False,
               # item 10, the C hooks (chroma-world/model/stage3-rules.md section 5)
               c3_inst=False, c4_nature=False, c5_faith=False, c2_groups=False,
               # the K limits' rule fixes (b-package.md K2 newcomer, K6 season steps)
               move_near=False, season_excl=False,
               # v22.5 F1 a body and a mind, F2 death from the life
               body=False, mind=False, death_life=False,
               # values the v22.5 refit changed (V225)
               death_par=None, body_par=None, course_mu=(-1.2, -0.3, -3.5), pension_k=0.3, pension_base=0.0, tie_k=1.0,
               kid_cost=0.12, hh_cls=(0.12, 0.30, 0.55), set_big=1.0, eyes_par=None,
               # v22.5, the many-lives fixes (F14 to F17, F19)
               set_age=None, up_lean=0.0, up_self=0.0, up_ease=0.0, up_fam=0.0, up_conc=0.3, up_half=20.0, course=False, par_age=None, par_split=None, job_move=None, birth_free=False, home_sale=1.0, loan_end=False,
               retire_hz=((50, 0.0), (54, 0.0), (56, 0.045), (58, 0.05), (60, 0.035), (61.9, 0.035), (62, 0.11), (65, 0.12), (67, 0.12), (70, 0.14), (80, 0.2)),
               ti_fit=None, birth_par=None, age_free=None, age_rate=None, age_pts=None, mon_drift=0.01, lone=None, low_pay=None, pay_col=None, pay_col2=None, tie_col=None, kid_tie=None, c_par=None, job_gap=None, pair_pay=None, pen_pay=None, low_net=None, work_die=None, birth_with=None, nest=None, ev_fit=None, ev_gapfit=None, ill_real=False, cond_once=False, risk_norm=False, drv_self=False, deed_canon=0.0, deed_rare=0.0,
               mind_kid=None, mind_u=None,
               # v22.5 realism (chroma-ideas/realism/v22.5-realism-list.md): F6 dreams that grow up, F12 the world and
               # the start hold
               dream_grow=False, own_open=False, start_hold=False,
               # v22.5 G19w: the company a life picks (world on)
               soc_own=0.0, skill_room=None,
               # v22.5 realism F3: a household and real people
               hh_money=False, ties_people=False,
               # v22.5 realism F8 and F10: retirement ends work; a world moment only on the world's event
               retire_ends=False, world_only=False,
               # v22.5 realism F7: one roll of the living
               one_roll=False,
               # picks come back: the game's played-life hook
               echo_play=False,
               # bold ways: the game's played-life hook
               bold_play=False,
               # every change has a cause: the played life's role causes (read-only)
               role_why=False,
               # because of you, and meanwhile: why each need moved (read-only)
               need_why=False,
               # needs that fit life (workstream 4)
               need_tab=None, shared_hist=0.0, imp_age=False,
               # aims v1 and the heights reading (workstream 5)
               aims=False, heights=False,
               # the world answers v1 (workstream 6) and its second phase
               world_answers=False, wa_phase2=False,
               # footprints (workstream 3)
               foot_on=False,
    # the v22.3 refit's satisfaction level (the new mechanics lift satisfaction; the set point moved .80 -> .86)
    sat_mid=0.8)
# the v24 refit's switches off (Release's K4 PNEW, with batch CHROMA_BATCH_OFF=FOOT,AIMS,WORLD_ANSWERS and v23.2's packs in
# CHROMA_PACKS): the lives of v23.2
V24_OFF = dict(need_tab=None, shared_hist=0.0, imp_age=False, aims=False, heights=False, world_answers=False,
               wa_phase2=False, foot_on=False, cause_fit=False)
# everything since the go-live off, for the identity check (C-E14): lives then equal engine_v9_golive.py
GOLIVE = {**V10_OFF, **ID_OFF, **FIX_OFF, **UPD_OFF, "world": False}
from realm_earth import ROLE_BY_SETTING, ACCEPT_BY_SETTING   # Earth's (realm_earth.py)
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
# need_why (WS1, "because of you, and meanwhile"): what moved each need this week, by source. act: the week's act (its
# ends met or drained, acting as oneself, succeeding at what was hard, learning, serving those one answers for, holding
# opposed colours, a binding act, a closed option that backfired); fade: the weekly drain, net of what one's niche gives;
# setback: an unchosen imposition (its kind in nw_imp); outside: a personal event from outside; reading: a batch event
# read through one's own colours; loss: a close person died; means: money, health, ties, freedom and time (and the
# place, with the world on); commitments: what held commitments meet, the mark of the work, leaving one; titles: what
# titles and statuses meet; care: a family looking after its child; goals: a goal reached or given up; people: being
# the one people ask; age: understanding that pays late; player: what the caller changed at a pause
NSOURCES = ["act", "fade", "setback", "outside", "reading", "loss", "means", "commitments", "titles", "care", "goals",
            "people", "age", "player"]

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


# ---------- the life loop. _run, the whole simulation (run() and run_steps() below call it), lives in the files of
# RUN_PARTS, one stretch of its lines each, unchanged and at their own indent (map: chroma-engine/notes/
# by-function-2026-10-18.md). parts.join puts them back in order and they are compiled here as the one function
# they are, so every life is what it was when _run stood here. A traceback in _run names "engine.py+parts";
# parts.where(<line>) gives the part and its line.
RUN_PARTS = ('run_01_start', 'run_02_goals', 'run_03_moments', 'run_04_titles', 'run_05_conditions', 'run_06_world',
             'run_07_body', 'run_08_fixes', 'run_09_week', 'run_10_situation', 'run_11_choice', 'run_12_commitments',
             'run_13_learning', 'run_14_marks', 'run_15_titles', 'run_16_world', 'run_17_inner', 'run_18_integrate')
exec(compile(*__import__("parts").join(RUN_PARTS, __file__), "exec"), globals())   # no module-level name: see parts.py


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
# names also read where they are there (not checked by tools/t_steps.py): the game's (the family's ways, each goal slot's
# steps per situation and the helper that fills them, the places' around with the world on) and Release's check_roll's
# (F8, F10: retired, this week's commitment kind, its success, the world's forced moments, the titles' once-a-life lists)
# and tools/t_steps.py's (this week's drift, at drift_k 0) and the game's picks come back (echo_play: the seeds, and the
# seed whose return is this week's moment, -1 for none)
STATE_MORE = ("fam", "gsr", "goal_rel_S", "around", "retired", "ck", "ok_", "frc_", "ONCE_HOLD_", "noise", "ep_seeds", "ep_now",
              "bold_now", "bold_pick",   # bold ways: per life this week's bold slots (a list of dicts: row, slot, base, label,
              # chance, p (the card's: p_act x the chance its win is kept), p_act, seen; None when not asked) and the slot taken (-1 none), from the choose pause on
              "asrc", "asrc_c",   # every change has a cause: what moved the want so far, by source (asrc: N x ASOURCES x
              # colours; asrc_c: the first logged life's, ASOURCES x colours; the game takes the year's movers between two pauses)
              "J", "FRpos", "clu_", "CLU_ON",   # foresee.arrows: how far each pair of colours is held together, the
              # world's opposed pairs and this week's closures in units (with CLU_ON)
              "nw", "nw_imp",   # need_why: this week's need moves by source (N x NSOURCES x needs) and silent setback
              # (IMPOSITIONS index, -1 none), from the start of the week; None off. The game takes the pick's from the choose pause on
              "AIM_ON", "HT_ON", "AIM", "ak", "astr", "astep", "aown", "aby", "atest", "acall", "abirth", "aim_best", "gal",
              "ht_t", "aim_take", "aim_end", "aim_fit", "aim_of_goal",   # aims v1 (foresee's aims track, set_aim, drop_aim)
              # and the heights reached (ht_t, weeks, -1 never); None off
              "WA_ON", "WA2_ON", "wa_book", "wa_lines", "wa_known",   # the world answers: on, its second phase on, each
              # life's ledger of rings 1 and out ((unit, key) -> record), its told lines, who is Known (the phase); None off
              "mark_last",   # foresee.marks_toward: the week each mark was last left (NEVER never)
              "FOOT_ON", "foot_log",   # footprints: on, and every pick's footprints so far (foot_log, a list of dicts)
              "foot", "foot_open",     # per life (None off): the last act's footprints (kind, value, who); doors (kind, since)
              "btrust")   # body_trust (finishing pack part 3): each life's trust per sphere (N x 9, NaN before 15); None off
STATE_MISSED = set()   # names read at a pause that are not handed over (STATE, STATE_IF, STATE_MORE): t_steps wants none


class PauseState(dict):
    """The state a run hands over at its pauses: one dict for the whole run, refreshed at each pause with the handed-over
    variables as they are there (a name not yet set is left out), as locals() is under Python 3.11 and 3.12 (Pyodide):
    a reference kept from an earlier pause reads the latest pause, and a key the caller set itself stays. While the run
    waits at a pause, a name not handed over is still read from the run (and noted in STATE_MISSED)."""
    __slots__ = ("_fr",)

    def __missing__(self, k):
        fr = getattr(self, "_fr", None)
        if fr is not None and k in fr.f_locals:
            STATE_MISSED.add(k)
            return fr.f_locals[k]
        raise KeyError(k)

    def __contains__(self, k):
        if dict.__contains__(self, k):
            return True
        fr = getattr(self, "_fr", None)
        if fr is not None and k in fr.f_locals:
            STATE_MISSED.add(k)
            return True
        return False

    def get(self, k, d=None):
        return self[k] if k in self else d


def _pause_state(st, cells, fr):
    """Refresh the run's pause state from its cells of the handed-over names and open it to the paused frame."""
    for nm, c in cells:
        try:
            st[nm] = c.cell_contents
        except ValueError:   # not set yet (or deleted): out, as locals() leaves it
            st.pop(nm, None)
    st._fr = fr
    return st


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
