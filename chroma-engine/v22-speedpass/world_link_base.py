"""world_link.py's tables, helpers and the burned-in world's cache: everything world_link.py held before class WorldLink,
moved out verbatim. world_link.py and WorldLink's mixins import from here."""
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

TOY_SEASON = {k_: i_ for i_, k_ in enumerate(WK.TIME_OF_YEAR)}   # winter, spring, summer, autumn = the world's season
# moments the world brings on its own events (Library W39 and the specs): (domain, kind, key or None, moment, share of
# those the moment's gates admit who meet it that week). With the world on, these moments have no background rate.
WORLD_MOMENTS = [
    ("state", "election", None, "election day", 0.6),
    ("state", "election", "change", "a landslide on election night", 0.35),
    ("era", "breakthrough", "revolution", "the old order falls", 0.8),
    ("state", "regime changes", None, "the old order falls", 0.8),
    ("belief", "revival", None, "a revival fills the square", 0.25),
    ("tech", "arrives", "new treatment", "a cure is found at last", 0.3),
    ("tech", "arrives", "new medium", "everyone is suddenly on the new medium", 0.5),
    ("tech", "arrives", "new machine", "the machines come for the work", 0.3),
    ("tech", "arrives", "new kind of job", "the machines come for the work", 0.3),
    ("nature", "price shock", "energy", "the power and the networks go down", 0.4),
    ("economy", "recession declared", "crisis", "a crash takes the savings", 0.5),
    ("economy", "recession declared", "severe", "a crash takes the savings", 0.3),
    ("abroad", "war comes home", None, "war comes", 0.7),
    ("abroad", "war begins", None, "the call to serve", 0.15),
    # the C hooks (stage3-rules.md section 5; Library earth-world-seasons.lib and earth-world-institutions.lib): a sixth
    # field names who can meet it, "place" for the people living in the event's place (value["loc"]), "staff" for those
    # who work at its institution (value["inst"]); without one, everyone the gates admit
    ("institution", "sold", None, "new owners take over the firm", 0.6, "staff"),
    ("institution", "merged", None, "folded into a bigger firm", 0.7, "staff"),
    ("institution", "nationalised", None, "the state takes over the failing firm", 0.7, "staff"),
    ("institution", "leak", None, "the private files get out", 0.5, "staff"),
    ("institution", "cover-up", None, "the thing the bosses are hiding", 0.3, "staff"),
    ("nature", "bad air", None, "a season of bad air", 0.3, "place"),
    ("nature", "bad water", None, "the river runs foul", 0.4, "place"),
    ("nature", "poisoned river", None, "the river runs foul", 0.4, "place"),
    ("nature", "drought", None, "a dry year on the land", 0.5, "place"),
    ("nature", "glorious spring", None, "a glorious spring", 0.15, "place"),
    ("nature", "recovery", None, "the town builds itself back", 0.4, "place"),
    ("belief", "new movement", None, "a new faith comes to town", 0.3, "place"),
    ("belief", "faith tension", None, "the hall on the corner is shut", 0.4, "place"),
]
# C2 (c2_groups; stage3-rules.md section 5, Library earth-world-civic.lib and earth-world-wants.lib): group moments the
# world brings, for the members only. "place_group": the members of that group kind living in the event's place;
# "faith_group": the members of a congregation of the reviving faith. The strike vote then comes only on a strike (no
# everyday draw); the split keeps its own yearly rate among members and comes on these too (C2_KEEP). Shares are start
# values for the refit
C2_MOMENTS = [
    ("institution", "strike", "union", "a strike vote at work", 0.5, "place_group"),
    ("belief", "revival", None, "the congregation splits in two", 0.1, "faith_group"),
    ("belief", "new movement", None, "the congregation splits in two", 0.2, "place_group"),
]
C2_KEEP = {"the congregation splits in two"}
C2_DEFAULT = dict(drift_tv=0.10, drift_share=0.5, group_half=0.5)   # a congregation drifted this far from its faith body
CRIME_W = re.compile(r"\b(robbed|burgl|mugg|attacked|break-in|broken into|stolen|pickpocket)", re.I)
DISASTER_W = re.compile(r"\b(flood|fire|storm|earthquake|quake|drought|heatwave|hurricane|landslide)\b", re.I)
PANDEMIC_W = re.compile(r"\b(pandemic|epidemic|outbreak|lockdown)\b", re.I)
RK = ["illness", "old_death", "disaster", "crime", "war", "pandemic", "jobloss", "birth"]
# outside events (read events) the world's own disasters bring: with the world on they come when a disaster strikes the
# person's town or a close person's (spec 5 §2), not on their own clock
DIS_EVR = re.compile(r"\b(disaster|flood|wildfire|earthquake|hurricane)\b", re.I)
# the lever an option pulls when the Library writes none (world-fields.md, "lever:"): by its mark; drops: or moves: is
# an exit, and an act closed by law at an institution is subvert
LEVER_MARK = {"left home": "exit", "moved away": "exit",
              "defied an authority": "subvert", "broke the law": "subvert", "hid a wrong": "subvert",
              "came out": "voice", "named their gender": "voice", "owned up": "voice", "made an enemy": "voice",
              "kept your word": "loyalty", "helped someone in need": "loyalty", "stayed home": "loyalty",
              "made a friend": "loyalty", "came home": "loyalty",
              "refused someone in need": "neglect", "broke your word": "neglect"}
NORM_MARK = {"came out": "coming out", "named their gender": "transition"}   # the norm such an act is judged by
# where an option's push lands when the Library writes no pushes: (world-fields.md): the moment's at:, group: or who:,
# else the commitment the option or moment is about
PUSH_COMMIT = {"career": ("institution", "employer"), "community": ("group", None), "faith": ("belief", None),
               "partner": ("close", "partner"), "children": ("close", "child")}
LOCAL_SEEN = ("disaster", "crime wave", "local election",   # local public events a person living there lives through
              "bad air", "bad water", "poisoned river", "drought", "glorious spring", "recovery",   # (C4's with its hook on)
              "new movement", "faith tension")                                                       # (C5's)
# the typical world after the 80-year burn-in (seeds 1-6 or 1-8, modern Earth): every channel below is neutral there
CLIM_REF = 0.51     # acceptance of coming out (.70) x the sexuality right (.73)
U_REF = 6.5         # local unemployment, percent
CAP_REF, OPEN_REF = 0.83, 0.91   # hospitals' and universities' capacity; universities' openness, mean over the classes
INFL_REF, WELF_REF, RIGHTS_REF = 3.0, 0.63, 0.82
REACH_K = 0.5       # utility of voice and subvert at the outer rings per unit of felt reach (0 to 1)
CRIME_REF = 0.17    # local crime
BELONG_REF = 0.85   # belonging met by settings and close people (People.belong): the mean week from age 20 (seed 3, 40 lives)
# WL2's sizes (values for the v22.3 refit): workers feel this share of the price squeeze the jobless feel (real wages
# lag prices); a recession takes about 3% of a wage's money (hours and raises; Great Recession hours -3%, BLS) and gives
# a little time back; a disaster in town costs money and time while its damage lasts; a lockdown at its peak (.35)
# takes about .1 off the ties a life drifts to
WL2_PAR = dict(price_work=0.5, rec_money=0.02, rec_free=0.01, dis_money=0.05, dis_free=0.03, pand_tie=0.3)
DIS_NEAR = 0.35     # share of disasters in a close person's town that become the life's own outside event
# the world's own record entries behind each kind of effect on a life (domain, kind), for its cause on hover (stage 1, WL1)
CAUSE_REC = {"housing": (("economy", "recession declared"), ("economy", "recession over")),
             "prices": (("nature", "price shock"), ("economy", "recession declared"), ("abroad", "world recession"),
                        ("abroad", "war comes home")),
             "welfare": (("state", "welfare raised"), ("institution", "budget cut"), ("state", "government falls")),
             "rights": (("state", "right gained"), ("state", "law changed"), ("state", "regime changes")),
             "law": (("state", "law changed"), ("state", "right gained"), ("state", "regime changes")),
             "crime": (("place", "crime wave"),), "war": (("abroad", "war comes home"), ("abroad", "war begins"), ("abroad", "war ends")),
             "disaster": (("nature", "disaster"),), "illness": (("nature", "pandemic"),), "pandemic": (("nature", "pandemic"),),
             "unemployment": (("economy", "recession declared"), ("abroad", "world recession"), ("tech", "arrives", "new machine"),
                              ("tech", "arrives", "new kind of job")),
             "university places": (("institution", "budget cut"),), "hospital places": (("institution", "budget cut"),),
             "technology": (("tech", "arrives"), ("tech", "spreads")), "norm": (("era", "era begins"),)}   # (domain, kind[, key's start])
CAUSE_REC.update(prices_work=CAUSE_REC["prices"], disaster_time=CAUSE_REC["disaster"],   # WL2's effects
                 recession=(("economy", "recession declared"), ("abroad", "world recession")))
CAUSE_REC["rec_hours"] = CAUSE_REC["recession"]
# a disaster's outside events by the world's hazard (world.HAZARDS), for P["dis_match"] (WL6): words in the event's name
HAZ_EVR = {"flood": r"\bflood", "fire": r"\b(wild)?fire", "quake": r"\b(earth)?quake", "storm": r"\b(storm|hurricane)",
           "heat": r"\b(heat|drought)"}
TIME_REF = 0.015   # time the groups no commitment counts take in the typical life (group_time): mean life-week from age 3 (seeds 3, 4, 40 lives x 80 years: .017, .013)
# the domain a title's standing counts in (spec 7 §2: a famous actor stands high in culture, not in the economy): by its
# institution (W40 institution=), else its sector; the packs' stage and screen titles sit at an employer in services
TITLE_DOM = {"party": "state", "ministry": "state", "council": "place", "university": "tech", "media": "culture",
             "faith body": "belief", "charity": "group", "union": "group"}
TITLE_DOM_NAME = {"lobbyist": "state", "pollster": "state"}


def title_domain(name, inst, sector):
    if name in TITLE_DOM_NAME:
        return TITLE_DOM_NAME[name]
    if inst == "charity" and sector == "knowledge":
        return "tech"
    if inst in TITLE_DOM:
        return TITLE_DOM[inst]
    if inst == "employer":
        return "culture" if sector == "services" else "tech" if sector == "knowledge" else "economy"
    if inst is not None:
        return "institution"
    return {"public": "institution", "knowledge": "tech"}.get(sector, "economy")


MIGRATE_T = {"immigrant", "refugee", "asylum applicant"}   # the catalogue's titles that take a life to another society
CITIZEN_T = {"naturalised citizen", "citizenship"}


def _isin_small(a, vals):
    """Speed pass: np.isin against a few whole numbers, as equalities (the same answer, without isin's sorting)."""
    a = np.asarray(a); r = np.zeros(a.shape, bool)
    for v_ in vals:
        r |= a == v_
    return r


# v22.5, F12 (the world and the start hold; chroma-ideas/realism/v22.5-realism-list.md): the localities a start's place
# word promises (the game's presets: "town", "a traditional village", "a city of learning", "hard streets"), by kind
START_PLACES = {
    "town": ("market town", "industrial town", "declining industrial town", "commuter suburb", "coastal resort",
             "tech boom town", "energy boom town"),
    "village": ("farming village", "fishing village", "mountain village", "river village"),
    "city": ("capital", "second city", "university city"),
    "neighbourhood": ("capital", "second city", "port city"),
}
START_TRIES = 400        # births drawn again at most (the last is kept when none fits)
START_HARD_CRIME = 0.2   # hard streets: a lower-class neighbourhood in a place with at least this much crime (cities, mill towns)


def start_classes(wealth):
    """The classes (0 lower, 1 middle, 2 upper) a start's wealth (the game's res0 money) stands for."""
    if wealth is None:
        return (0, 1, 2)
    return (0,) if wealth <= 0.1 else ((0, 1) if wealth < 0.4 else (1, 2))


def start_fits(PP, W, start):
    """v22.5, F12: whether each life's birth keeps the start's promise (world_cfg["start"]): the place kind its word
    names (START_PLACES; another word: any), the class its wealth stands for, the family's faith ("none": a family
    without one, "held": a family in one) and, for hard streets, a lower-class neighbourhood in a place with crime."""
    kinds = START_PLACES.get(str(start.get("place", "")))
    lk = np.asarray([W.loc_kind_key[l_] for l_ in PP.loc]) if kinds else None
    ok = np.ones(PP.N, bool) if kinds is None else np.isin(lk, kinds)
    ok &= np.isin(PP.cls, start_classes(start.get("wealth")))
    fa = start.get("faith")
    if fa == "none":
        ok &= np.asarray(PP.pfaith) < 0
    elif fa == "held":
        ok &= np.asarray(PP.pfaith) >= 0
    if start.get("hard"):
        nb_ = np.asarray(PP.nb); nbc = np.asarray(W.nb_class)
        ok &= (PP.cls == 0) & (nb_ >= 0) & (nbc[np.maximum(nb_, 0)] == 0) & (np.asarray(W.loc_crime)[PP.loc] >= START_HARD_CRIME)
    return ok


# The world's burn-in (its 80 years before the birth) is the same for the same seed, settings and code, so a run keeps the
# burned-in World and each run of that world starts from a deep copy of it, which goes on exactly as a fresh one does.
# BURN_KEEP worlds are kept in memory (a new life with the same seed and setup, a check that runs a life twice); with
# CHROMA_WORLD_CACHE set to a folder they are also kept there as pickles (named by the seed, settings and the md5 of the
# code that builds them), so every check run on that folder skips them. BURN_HITS counts the runs that used one.
BURN_KEEP = 2
BURN = {}
BURN_HITS = [0]
BURN_MODS = ("world",) + WM._PARTS + ("world_keys", "library", "combos", "sphere_data", "sphere_ev_base", "realm_earth")


def _code_md5():
    """The md5 of the code a burn-in runs (the files of BURN_MODS as loaded), with Python's and numpy's versions."""
    h = hashlib.md5(("%d.%d %s" % (sys.version_info[0], sys.version_info[1], np.__version__)).encode())
    for nm in BURN_MODS:
        f = getattr(sys.modules.get(nm), "__file__", None)
        h.update(nm.encode())
        if f and os.path.isfile(f):
            with open(f, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


def burned_world(seed, cfg, burn):
    """World(seed, cfg) after burn_in(burn), from the cache when the same world was burned in before (a deep copy)."""
    key = json.dumps([int(seed), cfg, float(burn)], sort_keys=True, default=repr)
    W0 = BURN.get(key)
    path = None
    if W0 is None and os.environ.get("CHROMA_WORLD_CACHE"):
        import world_keys, library, combos  # noqa: F401  (loaded already: the md5 reads their files)
        d_ = os.environ["CHROMA_WORLD_CACHE"]
        path = os.path.join(d_, "world_%s.pkl" % hashlib.md5((key + _code_md5()).encode()).hexdigest())
        if os.path.isfile(path):
            try:
                with open(path, "rb") as fh:
                    W0 = pickle.load(fh)
                path = None
            except Exception:   # a broken file: burn it again
                W0 = None
    if W0 is None:
        W0 = WM.World(int(seed), cfg=copy.deepcopy(cfg))
        W0.burn_in(burn)
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp_ = "%s.%d.tmp" % (path, os.getpid())
            with open(tmp_, "wb") as fh:
                pickle.dump(W0, fh, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp_, path)
    else:
        BURN_HITS[0] += 1
    BURN.pop(key, None)
    BURN[key] = W0
    while len(BURN) > BURN_KEEP:
        BURN.pop(next(iter(BURN)))
    return copy.deepcopy(W0)
