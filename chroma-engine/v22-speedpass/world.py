"""Chroma's shared outer world: one society per world seed, shared by every life in a run (chroma-world package, agreed
by Emren 2026-10-06 10:51; build plan chroma-engine/world-build.md; keys chroma-engine/world-fields.md and world_keys.py).

    W = World(seed, cfg=None)       cfg: pace, tech_level, climate, setting, preset, legacy (see CFG_DEFAULT)
    W.burn_in(80)                   the world alone before the birth (spec 5 §4); the log keeps it
    W.tick(week)                    every week with the world clock (W.t0 + the life's week), or W.tick() for one week
    W.spawn_neighbour(k)            a full World for neighbour k, its clock equal to this one's (emigration, spec 5 §5);
                                    W.society_id is 0 at home, k + 1 in a spawned neighbour
    W.disaster_now, W.disaster_kind per locality: severity (0..1) and HAZARDS index of a disaster striking this week,
                                    else 0 and -1 (cleared the next week)

Ticks follow package.md §4: the season every week; every 13 weeks the quarter in order nature, other societies,
economy, state, institutions, places, culture, society and eras, public figures, history log; every 52 weeks the year
(technology, belief, the generations turning 15 to 25, the population). Pushes queued by the lives land at the next
quarter tick.

Rules kept (world-build.md "Rules every part keeps"):
- No color rule. Nothing here reads or defines a relation between colors on the wheel. Fit between two pies is overlap
  or distance, the same for every pair. Every color-indexed table is a module-level array below; World(color_perm=p)
  permutes all of them (and every color-indexed random draw) at construction, so a permuted world is the same world
  with its colors relabelled (the equivariance test in calib_v10/world_check.py).
- One world per seed: own streams np.random.default_rng([seed + 104729, k]), one k per domain (a spawned neighbour
  adds its society id: [seed + 104729, k, society]). The world never sees N.
- Timeless: keys and ids only, never a year, a brand, a real place, person or event.
- pace (0.5 to 2) multiplies only the world's hazards (recession start, crises, war, pandemic, disasters) and how fast
  society's pressure builds.
- numpy and the standard library only; no file input or output; safe in Pyodide.
"""
import numpy as np
try:   # speed pass: np.clip's own ufunc, called without its Python wrapper (the same numbers)
    from numpy._core.umath import clip as _uclip
except ImportError:
    from numpy.core.umath import clip as _uclip
from library import COLORS, NEEDS, NEED_MAP_V6, ERA_KINDS
from combos import IDEAS, ERA_COMBOS
from world_keys import (TIME_OF_YEAR, HOLY_KEYS, WHO_SLOTS, CAST_WANTS, GROUP_KINDS, FEATURES, INST_KINDS, LAW_KEYS,
                        NORM_KEYS, LAW_STATES, TECH_KEYS, LEVERS, DOMAINS, RECORD_DOMAINS, SECTORS, RINGS)
from world_keys import SPHERES, GROUP_SPHERE, INST_SPHERE, SECTOR_SPHERE, STATE_SPHERE, HAUNT_KINDS

C = 5
SEASONS = TIME_OF_YEAR                                   # 0 winter, 1 spring, 2 summer, 3 autumn (northern)
WEEK_SEASON = np.array([0] * 9 + [1] * 13 + [2] * 13 + [3] * 13 + [0] * 4)     # week of year -> season
CLASSES = ["lower", "middle", "upper"]
PLACE_CLASSES = ["city", "town", "rural"]                # the coarse place of a population group (spec 2 §6)
AGE_BANDS = [(0, 15), (15, 25), (25, 35), (35, 45), (45, 55), (55, 65), (65, 75), (75, 100)]
MIGRANT = ["native", "migrant"]
OPEN_GROUPS = [f"{c} {m}" for c in CLASSES for m in MIGRANT]   # institution openness: class and migrant status (R9)
PHASES = ["expansion", "recession"]
SEVERITY = ["mild", "severe", "crisis"]
WAR_STATES = ["peace", "abroad", "home"]
PANDEMIC = ["none", "rising", "peak", "waning"]
HAZARDS = ["flood", "fire", "quake", "storm", "heat"]
SERVICES = ["schools", "health", "transport"]
RIGHTS = ["speech", "faith", "movement", "sexuality", "women"]   # sexuality is read as sexuality and gender identity
RELATIONS = ["allied", "neutral", "rival", "hostile"]
BREAKTHROUGHS = ["reform", "revolution", "revival", "restoration"]
TECH_LEVELS = ["behind", "modern", "ahead"]
NEW_TECH = ["new treatment", "new medium", "new way to meet", "new kind of job", "new machine", "new energy", "new watch"]
FIG_ROLES = ["head of government", "opposition leader", "star", "athlete", "preacher", "scientist", "magnate", "activist"]
TRENDS = ["declining", "steady", "growing"]
SIZES = ["village", "town", "city", "metropolis"]
COSMOLOGY = {"earth": "believed", "tribal": "felt", "magic": "real"}   # spec 5 §3, a setting value only
VALUES = ["self-direction", "stimulation", "hedonism", "achievement", "power",
          "security", "conformity", "tradition", "benevolence", "universalism"]          # schwartz.VALUES
NI = {k: i for i, k in enumerate(NORM_KEYS)}
LI = {k: i for i, k in enumerate(LAW_KEYS)}

# The spheres of society (item 15), Replace: every group kind, institution kind and part of the state has a home sphere
# (world_keys). The arrays stay where they are, with the same values, update order and draws; World.inst_sphere,
# World.sphere_insts, World.state_parts and People.set_sphere read them by sphere. -1: by the employer's sector.
SPH = {s_: i_ for i_, s_ in enumerate(SPHERES)}
INST_SPH = np.array([-1 if INST_SPHERE[k_] is None else SPH[INST_SPHERE[k_]] for k_ in INST_KINDS], np.int64)
GROUP_SPH = np.array([-1 if GROUP_SPHERE[k_] is None else SPH[GROUP_SPHERE[k_]] for k_ in GROUP_KINDS], np.int64)
SECTOR_SPH = np.array([SPH[SECTOR_SPHERE[k_]] for k_ in SECTORS], np.int64)
HAUNT_SPH = np.array([SPH[k_.split(".")[0]] for k_ in HAUNT_KINDS], np.int64)   # each haunt kind's sphere (phase 2)
SPH_PAIRS = ["WU", "UB", "BR", "RG", "GW", "WB", "UR", "BG", "RW", "GU"]   # the ten pair faces of each sphere (phase 3)
N_PLACES = 3            # named places per town and haunt kind (phase 2, N1: "a few named places per haunt kind")
LEAD_W = 0.25           # phase 4: a life leading a sphere in town weighs a quarter of the town's bodies in its leaders' mix
K_PAT = 0.005           # phase 4: a patron's pull a quarter, x size (dynamics.json levers.fund, kPat)
FUND_SPAN = [0, 4, 16, 40, 80]   # quarters a fund act's pull lasts by rung (levers.fund.span; a leader's tenure: 20 years)
STATE_PARTS = {"say": ("G", "regime", "support", "gov_party", "Dem"), "law_book": ("laws",), "rights": ("rights",),
               "purse": ("welfare", "welfare_pub"), "war": ("war", "ext_war", "war_with"), "force": ()}   # force: police, army
NN, NL, NT = len(NORM_KEYS), len(LAW_KEYS), len(TECH_KEYS)

# ---------------------------------------------------------------------------------------------- color-indexed tables
# Every table in this block is indexed by color (last axis W U B R G) and is permuted by World(color_perm=...).


def _mix(s):
    """'W.6 U.4' -> 5 shares."""
    v = np.zeros(C)
    for tok in s.split():
        v[COLORS.index(tok[0])] += float(tok[1:])
    return v / v.sum()


COMBO_KEYS = list(ERA_COMBOS)                                       # combos.IDEAS keys: 5 singles, 10 pairs, 10 triads
COMBO_MIX = np.array([[1.0 / len(k) if c in k else 0.0 for c in COLORS] for k in COMBO_KEYS])   # engine.COMBO_MIX as rows
_cd = COMBO_MIX - 0.2
COMBO_DIR = _cd / np.linalg.norm(_cd, axis=1, keepdims=True)        # the set is closed under any color permutation

# The engine's Schwartz map: schwartz.LOAD (10 values x 5 colors). schwartz.py imports the engine, so the numbers are
# copied here; world_check.py checks them against schwartz.LOAD.
LOAD = np.array([[-3.0, 0.5, 3.5, 1.5, -2.5], [-2.5, -2.0, 1.5, 2.5, 0.5], [-2.5, -1.5, 1.5, 2.5, 0.0],
                 [-1.0, 2.0, 2.5, -0.5, -3.0], [-1.5, 0.5, 1.5, 1.0, -1.5], [1.5, 1.5, -1.0, -1.5, -0.5],
                 [3.0, 2.0, -2.0, -3.0, 0.0], [2.5, -1.5, -3.5, -0.5, 3.0], [1.0, 0.0, -1.0, -1.0, 1.0],
                 [0.5, -1.0, -1.0, 0.0, 1.5]])
NEED_MAP = np.array(NEED_MAP_V6, float)                             # needs x colors (library.NEED_MAP_V6)

# What each law and norm serves (5 shares), one line of reason each. Every key is the acceptance of an act; the law
# entry is whether the act is legal. "conscription" and "death penalty" are acts of the state: legal = in force.
# Acceptance norms are mostly freedoms, so Red and Black serve more of them than White (column sums 3.6 to 5.3 over
# 22 keys; world_check prints them). Only the profiles' deviations from even enter the dynamics.
NORM_PROF_SRC = {
    "drugs":             ("R.4 B.3 U.3", "pleasure and altered experience, rule over one's own body, curiosity about the mind"),
    "divorce":           ("R.3 B.3 U.4", "leaving a bond for one's own happiness, self-interest, choosing by reason over vows"),
    "abortion":          ("B.4 U.4 R.2", "control over one's own life, planning and foresight, freedom from an imposed duty"),
    "same-sex marriage": ("R.3 W.4 G.3", "love as one feels it, equal standing under the law, family and belonging"),
    "conscription":      ("W.6 G.2 R.2", "the duty owed to the group, defending the home ground, courage in the fight"),
    "guns":              ("R.3 G.3 B.3 W.1", "freedom and self-defence, self-reliance and the hunt, power, lawful order of owners"),
    "gambling":          ("B.5 R.3 U.2", "chasing gain, the thrill, calculating the odds"),
    "alcohol":           ("R.4 G.4 B.2", "pleasure and celebration, custom and conviviality, indulgence"),
    "sex work":          ("B.6 R.3 W.1", "trading for gain, sexual freedom, a trade under rules"),
    "euthanasia":        ("U.5 B.3 W.2", "reasoned control over death, self-determination, mercy through due process"),
    "home schooling":    ("G.5 W.3 U.2", "the family's own ways and roots, moral or faith teaching, self-directed learning"),
    "death penalty":     ("W.6 B.4", "retribution through the state's order, power over life"),
    "adoption":          ("W.4 G.4 U.2", "a child given a family through due process, care and kinship, planning the child's future"),
    "cohabiting":        ("R.4 G.3 U.3", "love without vows, a natural partnership, a considered trial before commitment"),
    "tattoos":           ("R.5 G.3 B.2", "self-expression, tribe and ritual, self-display"),
    "single parenthood": ("G.4 B.3 R.2 U.1", "family in any form, self-reliance, independence, a planned choice"),
    "faith in public":   ("W.6 G.4", "a shared moral order, tradition"),
    "leaving a faith":   ("U.5 B.3 R.2", "reason over doctrine, self-determination, freedom"),
    "coming out":        ("R.4 G.3 U.3", "living as one feels, being what one is, self-knowledge"),
    "role crossing":     ("B.3 U.3 R.2 W.2", "choosing one's path over the expected role, skill over custom, living as one feels, equal rules"),
    "transition":        ("R.4 U.3 G.2 B.1", "living as one truly is, self-understanding and medicine, being true to one's nature, self-determination"),
    "mixed marriage":    ("R.3 G.3 U.3 W.1", "love across lines, family, an open mind, equal standing"),
    # W38b (the Library's held-back keys; estimates): read at their modern state, not modelled yet (world_keys.LAW_V23)
    "tobacco":           ("R.4 B.3 G.3", "pleasure and habit, rule over one's own body, custom and company"),
    "knives":            ("B.4 R.3 G.3", "self-defence and power, readiness for a fight, a tool of the outdoors"),
    "drink-driving":     ("R.6 B.4", "the night out and the thrill, one's own convenience first"),
    "prescription medicines": ("B.4 U.3 R.3", "rule over one's own body, knowing better than the rules, relief now"),
    "childminding":      ("G.5 W.3 B.2", "care among kin and neighbours, mutual help, earning on the side"),
    "gender on papers":  ("R.4 U.3 W.3", "being recognised as one is, self-understanding, equal standing under the law"),
}
WELFARE_PROF_SRC = ("W.5 G.4 U.1", "care organised by the state, mutual support, planned provision")
NORM_PROF = np.array([_mix(NORM_PROF_SRC[k][0]) for k in NORM_KEYS])
WELFARE_PROF = _mix(WELFARE_PROF_SRC[0])

# Native institution profiles from Ravnica's guilds (spec 4 §2): 0.6 of the guild's colors plus 0.4 spread evenly.
GUILDS = dict(azorius="WU", dimir="UB", rakdos="BR", gruul="RG", selesnya="WG", orzhov="WB", izzet="UR", golgari="BG",
              boros="WR", simic="UG")
GUILD_MIX = {g: np.array([1.0 / len(k) if c in k else 0.0 for c in COLORS]) for g, k in GUILDS.items()}
NATIVE_SRC = {                              # kind -> list of profile sources; a firm draws one from its sector's list
    "school": ["W.6 U.4"],                  # "Schools start White with Blue"
    "university": ["simic izzet"],          # research and engineering
    "bank": ["orzhov"], "hospital": ["simic"], "police": ["boros"], "court": ["azorius"], "prison": ["boros"],
    "army": ["boros"], "media": ["rakdos", "dimir"], "union": ["gruul selesnya"], "charity": ["selesnya"],
    "council": ["azorius"], "ministry": ["azorius"], "party": [], "faith body": [], "employer": [],
}
SECTOR_GUILDS = [["golgari", "selesnya"], ["izzet", "orzhov"], ["rakdos", "selesnya", "orzhov", "golgari"],
                 ["izzet", "simic", "dimir"], ["azorius", "selesnya", "simic"]]   # farm, industry, services, knowledge, public
ROUTINE = _mix("W1")       # spec 4 §3: founders' zeal hardens into rules, the profile drifts toward White with age
OLIGARCHY = _mix("B1")     # spec 4 §3: leaders entrench and serve themselves, the profile drifts toward Black

# Faiths: invented ids, profiles chosen so the set sums evenly over the colors (0.6 each).
FAITH_PROF = np.array([[.34, .12, .10, .12, .32],      # 0: duty and tradition (the culture's old majority faith)
                       [.12, .34, .30, .12, .12],      # 1: learning and striving
                       [.14, .14, .20, .36, .16]])     # 2: passion and devotion (most migrants' faith)
NF = len(FAITH_PROF)

# First society, "typical rich": the value climate fitted so its Schwartz profile through LOAD matches the average
# centred ESS profile of rich democracies. Centred means are estimates read from the ESS rounds 1-9 country means of
# Western and Northern European members and Schwartz and Bardi's (2001) pan-cultural baseline (benevolence,
# universalism, self-direction and security high; stimulation and power low). LOAD spans 4 of the 10 dimensions, so
# the fit is a shape match (world_check prints r); the lean is set to 0.04 (estimate: a society is far less uneven
# than a person).
ESS_RICH = np.array([.50, -.60, -.10, -.35, -1.05, .45, -.05, -.20, .80, .60])        # VALUES order (estimate)


def fit_values(target, lean=0.04):
    """A 5-share mix whose centred Schwartz profile through LOAD best matches target (least squares on the zero-sum
    plane), scaled so its largest deviation from even is lean."""
    M = LOAD - LOAD.mean(0)
    B = np.linalg.svd(np.ones((1, C)))[2][1:].T
    d = B @ np.linalg.lstsq(M @ B, target - target.mean(), rcond=None)[0]
    return 0.2 + d / np.abs(d).max() * lean


V_RICH = fit_values(ESS_RICH)

# ------------------------------------------------------------------------------------------------- other content
# Localities of the first society (spec 3 §2.1). kind key, features, size (0 village .. 3 metropolis), density,
# population share, class mix (lower middle upper), sectors (farm industry services knowledge public), unemployment
# factor (regional spread, OECD: a factor of 2 to 3; estimate), rent index, crime (0..1), hazards (flood fire quake
# storm heat), nature access, place class (city, town, rural).
LOC_TABLE = [
    ("capital", "city capital university", 3, .95, .20, (.27, .47, .26), (.01, .12, .50, .22, .15), .85, 1.6, .30, (.2, .05, .15, .15, .5), .25, 0),
    ("second city", "city industry", 2, .80, .11, (.33, .49, .18), (.02, .26, .44, .13, .15), 1.0, 1.15, .28, (.3, .05, .15, .1, .4), .3, 0),
    ("university city", "city university", 2, .70, .06, (.28, .50, .22), (.02, .12, .40, .21, .25), .9, 1.25, .20, (.25, .05, .15, .1, .3), .45, 0),
    ("port city", "city port coast industry", 2, .75, .07, (.38, .47, .15), (.02, .30, .46, .08, .14), 1.15, 1.0, .30, (.4, .05, .15, .5, .3), .45, 0),
    ("declining industrial town", "town industry mining", 1, .50, .045, (.48, .44, .08), (.04, .44, .34, .04, .14), 1.7, .6, .27, (.3, .1, .15, .1, .25), .5, 1),
    ("industrial town", "town industry", 1, .50, .05, (.40, .49, .11), (.04, .40, .36, .06, .14), 1.2, .75, .20, (.25, .1, .15, .1, .25), .5, 1),
    ("market town", "town farming", 1, .40, .05, (.33, .53, .14), (.11, .18, .46, .07, .18), .95, .85, .14, (.3, .15, .15, .1, .25), .65, 1),
    ("commuter suburb", "suburb town", 1, .55, .10, (.15, .55, .30), (.02, .14, .48, .21, .15), .7, 1.3, .10, (.15, .15, .15, .1, .3), .5, 1),
    ("coastal resort", "town coast resort", 1, .45, .03, (.36, .50, .14), (.03, .07, .67, .05, .18), 1.25, 1.05, .18, (.25, .1, .15, .6, .3), .8, 1),
    ("farming village", "village farming", 0, .10, .04, (.33, .55, .12), (.35, .14, .31, .03, .17), .9, .55, .06, (.3, .35, .15, .15, .3), .9, 2),
    ("fishing village", "village coast fishing", 0, .12, .02, (.38, .52, .10), (.30, .15, .38, .02, .15), 1.1, .6, .07, (.3, .05, .15, .7, .15), .9, 2),
    ("mountain village", "village mountain", 0, .08, .02, (.33, .55, .12), (.22, .12, .48, .03, .15), .95, .65, .05, (.25, .4, .5, .25, .1), .95, 2),
    ("river village", "village farming", 0, .10, .03, (.35, .54, .11), (.30, .20, .32, .03, .15), 1.0, .55, .06, (.7, .1, .15, .15, .25), .85, 2),
    ("remote area", "remote farming", 0, .03, .02, (.40, .52, .08), (.40, .12, .30, .02, .16), 1.4, .45, .05, (.2, .5, .3, .3, .2), 1.0, 2),
    ("tech boom town", "town boom", 1, .50, .03, (.25, .50, .25), (.01, .10, .35, .42, .12), .6, 1.2, .15, (.15, .3, .3, .1, .4), .5, 1),
]
BOOM_ENERGY = ("energy boom town", "town boom mining industry", (.05, .45, .32, .06, .12))   # the other boom town
LOC_KINDS = [r[0] for r in LOC_TABLE] + [BOOM_ENERGY[0]]
# Tribal and magic worlds run the same machinery; only the kind words differ (the game writes the names).
LOC_KIND_ALIASES = {
    "tribal": dict(zip(LOC_KINDS, ["great camp", "second camp", "elders' camp", "harbour camp", "worn quarry camp",
                                   "smithing camp", "trading ground", "outer camp", "shore camp", "planting camp",
                                   "fishing camp", "mountain camp", "river camp", "far range", "new ground",
                                   "ore ground"])),
    "magic": dict(zip(LOC_KINDS, ["tower city", "guild city", "academy town", "harbour city", "spent forge town",
                                  "forge town", "market ward", "outer ward", "tide town", "farming hamlet",
                                  "fishing hamlet", "mountain hamlet", "river hamlet", "wildlands", "rift town",
                                  "ore rift town"])),
}
UNIVERSITY_LOCS = (0, 1, 2)       # capital, second city, university city
COURT_LOCS = (1, 3, 6)            # regional courts (the high court sits in the capital)
PRISON_LOCS = (4, 13)
RMEDIA_LOCS = (1, 2, 3)

# Holy calendars (weeks of the year) per faith; faith 1 keeps a lunar year and moves about 1.5 weeks earlier each year.
HOLY_BASE = [dict(feast=[0, 14, 51], fast=[9, 10, 11, 12, 13], pilgrimage=[30], mourning=[44]),
             dict(feast=[20, 21, 31], fast=[16, 17, 18, 19], pilgrimage=[31, 32], mourning=[40]),
             dict(feast=[22, 38], fast=[35, 36], pilgrimage=[26, 27], mourning=[4])]
HOLY_LUNAR = [0.0, -1.5, 0.0]

# Modern kit adoption ceilings by technology level (spec 5 §1; estimates: rich-country household and individual
# adoption). 0 = the kind does not exist yet in that world (it can arrive later as a new kind).
TECH_CEIL = {"behind": [.80, .45, .45, 0, 0, 0, 0, .75, .70, .30],
             "modern": [.95, .85, .92, .75, .45, .35, .45, .95, .85, .60],
             "ahead":  [.98, .93, .97, .90, .60, .50, .75, .98, .80, .70]}

# Norms of the first society: acceptance at the birth (modern) and about 80 years earlier (start of the burn-in), so
# the generations alive at the birth lived through the S-curves. Modern values: averages over rich democracies'
# surveys (ESS, World Values Survey, Gallup, Pew; estimates). The start values are estimates.
NORM_MOD = {"drugs": .30, "divorce": .85, "abortion": .65, "same-sex marriage": .70, "conscription": .45, "guns": .35,
            "gambling": .60, "alcohol": .90, "sex work": .40, "euthanasia": .55, "home schooling": .45,
            "death penalty": .30, "adoption": .85, "cohabiting": .85, "tattoos": .60, "single parenthood": .70,
            "faith in public": .55, "leaving a faith": .80, "coming out": .70, "role crossing": .70, "transition": .45,
            "mixed marriage": .90, "tobacco": .55, "knives": .25, "drink-driving": .08, "prescription medicines": .30,
            "childminding": .70, "gender on papers": .45}   # v23 keys: estimates
NORM_START = {"drugs": .12, "divorce": .45, "abortion": .35, "same-sex marriage": .08, "conscription": .70, "guns": .45,
              "gambling": .40, "alcohol": .85, "sex work": .20, "euthanasia": .30, "home schooling": .40,
              "death penalty": .65, "adoption": .80, "cohabiting": .25, "tattoos": .15, "single parenthood": .25,
              "faith in public": .80, "leaving a faith": .40, "coming out": .08, "role crossing": .35,
              "transition": .05, "mixed marriage": .25,
              "tobacco": .80, "knives": .45, "drink-driving": .50, "prescription medicines": .40, "childminding": .85,
              "gender on papers": .03}   # v23 keys: estimates
# Law book about 80 years before the birth (0 legal, 1 restricted, 2 banned).
LAW_START = {"drugs": 2, "divorce": 1, "abortion": 2, "same-sex marriage": 2, "conscription": 0, "guns": 1,
             "gambling": 1, "alcohol": 0, "sex work": 2, "euthanasia": 2, "home schooling": 1, "death penalty": 0,
             "adoption": 0, "tobacco": 0, "knives": 0, "drink-driving": 0, "prescription medicines": 0, "childminding": 0,
             "gender on papers": 2}
# The law book at the birth, typical rich (averaged over rich democracies; estimates): the state the modern norms point to.
LAW_MOD = {"drugs": 2, "divorce": 0, "abortion": 0, "same-sex marriage": 0, "conscription": 1, "guns": 1,
           "gambling": 0, "alcohol": 0, "sex work": 1, "euthanasia": 1, "home schooling": 1, "death penalty": 2,
           "adoption": 0, "tobacco": 1, "knives": 1, "drink-driving": 2, "prescription medicines": 1, "childminding": 1,
           "gender on papers": 1}
NORM_RIGHT = {"role crossing": 4, "transition": 3}   # norms without a law entry whose law push is a right
RIGHT_MOD = {"role crossing": 0.85, "transition": 0.75}

CFG_DEFAULT = dict(pace=1.0, tech_level="modern", climate="middle", setting="earth", preset="typical rich", legacy=None,
                   trace=False)

W_DEFAULT = dict(
    # ---- economy (spec 1 §2). NBER post-war US: expansions about 64 months, recessions about 11.
    h0=0.012,          # quarterly hazard that an expansion ends, at its start (estimate, fitted to ~5 y)
    h_age=0.006,       # added hazard per year of expansion (duration dependence; estimate)
    h_imb=0.06,        # added hazard per unit of housing gap above 0 (booms end in busts)
    h_trade=0.08,      # added hazard per unit of trade with a neighbour that fell into recession 1-3 quarters ago
    h_world=0.03,      # added hazard during a world recession
    h_shock=0.02,      # added hazard per 5 points of energy price shock
    sev_p=(0.70, 0.25, 0.05),   # severity mild/severe/crisis at a recession's start (spec 1 §2)
    crisis_boom=11.0,  # crisis odds multiply by 1 + this x the housing boom of the last 3 years (Reinhart-Rogoff)
    rec_len=(3.0, 4.2, 7.0),    # mean recession length in quarters by severity (overall ~11 months; crises longer)
    gap_floor=(-0.45, -0.7, -1.0),   # output gap in the trough (prosper: -0.5 in a recession, -1 in a crisis)
    gap_boom=0.3, gap_tau=3.0,  # boom ceiling (prosper +0.3) and years to approach it
    gap_rec=(0.30, 0.18, 0.07), # quarterly recovery speed of the gap after a mild, severe, crisis recession
    u_nat=5.0,         # natural unemployment, percent (setting; spec 1 §2)
    u_rise=(1.5, 3.0, 5.0),     # unemployment rise by severity, points (spec 1 §2)
    u_half=(8.0, 8.0, 12.0),    # half-life of the rise in quarters (about 2 years; slower after crises)
    infl0=2.0,         # inflation baseline, percent
    infl_gap=1.5,      # inflation points per unit of output gap (demand pressure)
    e_haz=0.013,       # quarterly hazard of an energy price shock (estimate; tuned to a big inflation every ~20-25 y)
    e_size=(3.0, 9.0), # energy shock, inflation points at onset (uniform range)
    e_decay=0.85,      # quarterly persistence of an energy shock
    f_haz=0.004,       # quarterly hazard of a food price shock (harvest failure; heat and drought raise it)
    f_size=(1.0, 3.0), f_decay=0.75,
    ineq0=0.32,        # inequality (Gini-like) of a typical rich democracy (OECD average about 0.32)
    pay_pos=1.0,       # payoff: in a boom the order's winners win more, in a bust they lose (zero mean over the cycle)
    pay_ent=0.12,      # payoff: booms reward enterprise, busts caution, read through LOAD (zero mean over the cycle)
    # ---- state (spec 1 §3)
    regime0=9.0,       # +9: a modern rich democracy (Polity-like scale)
    rule_cost=0.02,    # support lost per year in office (Paldam 1986)
    ev_gap=0.10,       # support per unit change of the output gap (economic vote)
    ev_u=0.012,        # support lost per point rise in unemployment
    ev_infl=0.004,     # support lost per point of inflation above 4, per quarter
    th_sup=0.10,       # support lost per unit of distance between government and demand (thermostat)
    s_noise=0.010,     # quarterly noise in support
    s_win=0.69,        # support of a new government (wins its first re-election a little more often than not)
    e_noise=0.04,      # noise of the election result
    break_keep=0.15,   # a reform wave stays with the governing party unless another fits the new order this much better
    ref_g=0.5,         # share of the way a reform moves the government's colors toward the target (with the
                       # institutions' step, Pos moves about a quarter of the way: spec 6 §5)
    q_vote=0.5,        # pressure kept when an election changes the government (the rest is released; estimate)
    mandate_q=16,      # quarters in which a new government's distance from demand counts as its mandate (a term;
                       # without it a reform undid most electoral swings within a year: estimate)
    k_thermo=0.6,      # G_new = Dem + k (Dem - G_old): the next government swings past demand (spec 1 §3)
    g_noise=0.40,      # spread of a new government's colors around that (log shares; coalitions, leaders)
    th_dem=0.25,       # demand leans away from where government pushes beyond it (Wlezien 1995)
    law_h=0.025,       # quarterly chance a law moves one step toward what its support points to (laws trail norms)
    law_cut=(0.33, 0.52),   # support below the first bans, above the second makes legal (majority support ~50%)
    law_fit=1.0,       # support added per unit of the government's fit with the law's colors above even (more lets
                       # governments legalise ahead of majority support)
    law_open=3.0,      # law changes come this many times easier in a breakthrough's open years
    welfare0=0.6,      # welfare level of a typical rich democracy (estimate)
    # ---- culture (spec 1 §4)
    norm_r=0.05,       # yearly speed of a norm in logit units, before the young-share and communication factors
                       # (~1.4x today): from 27% toward a far target it reaches 70% in about 23 years (US same-sex
                       # marriage 27% to 70% in 25 y; world_check measures it)
    norm_v=10.0,       # target shift (logit) per unit change of the value climate's fit with the norm's colors
    norm_era=8.0,      # target shift per unit of the era's fit with the norm's colors, times intensity (period effect)
    norm_law=0.4,      # target shift when the act is legal (+) or banned (-) (Aksoy et al. 2020)
    norm_back=4.0,     # backlash per unit of fast change (logit per year above 0.08) times the older share
    trust0=0.45,       # social trust of a typical rich democracy (ESS about 5 of 10)
    fear0=0.30,        # media fear in normal times
    # ---- generations and value climate (spec 1 §4)
    coh_era=0.05,      # a formative year's pull toward the era's colors, times intensity (higher runs away: era ->
                       # cohorts -> values -> demand -> era drove an even start 0.2 -> 0.39 in one color in 200 y)
    coh_sec=0.12,      # a formative year's shift along the secure/insecure direction (through LOAD)
    coh_anchor=0.15,   # pull of each new generation back toward the society's long-run values (estimate)
    coh_noise=0.012,   # spread of a generation's mix (log shares)
    tilt_class=0.025,  # class tilt along the secure direction (through LOAD; estimate)
    tilt_place=0.020,  # city/rural tilt along openness vs conservation (through LOAD; estimate)
    tilt_faith=0.30,   # the faithful lean this far toward their faith's profile
    tilt_mig=0.5,      # migrants lean this far toward their origin's value climate
    # ---- society and eras (spec 6)
    w_pos=(0.35, 0.35, 0.15, 0.15),   # Pos weights: state and law, institutions, economy payoff, belief (spec 6 §2)
    w_gov=0.7,         # inside the state term: government colors against the law book
    zeta=0.25,         # unmet needs make the colors that could meet them wanted (engine zeta_a = 0.2)
    mobil=1.5,         # groups weigh in pressure by 1 + this x their unmet needs (the left-out mobilise)
    q_tol=0.010,       # distance between order and demand that people live with
    q_hab=0.75,        # ... plus this share of the distance they have lived with for decades (habituation)
    q_hab_r=0.01,      # quarterly speed of that habituation (a memory of about 25 years)
    q_k=1.6,           # pressure built per quarter per unit of distance beyond tolerance
    q_decay=0.03,      # quarterly fading of pressure (people get used to things)
    q_theta=0.11,      # pressure needed for a breakthrough at hold 1 (tuned: reform waves every 8-12 y)
    q_hold=2.0,        # threshold = q_theta x hold ** q_hold (as for a person)
    q_step=(0.25, 0.6, 0.25, 0.3),    # step toward the target: reform, revolution, revival, restoration
    q_open=(4.0, 6.0, 4.0, 3.0),      # open years after each kind
    era_on=0.012,      # lean (half L1 distance of Pos from its reference) that starts an era (tuned: gaps near 8-12 y)
    era_off=0.007,     # lean below which an era ends
    era_hi=0.030,      # lean at full intensity
    era_ref=1.0,       # reference for the lean: 0 = even, 1 = the society's own slow normal (see World._era)
    era_mem=0.016,     # quarterly speed of that slow normal (half-life about 11 years)
    era_smooth=0.06,   # quarterly speed of the order as the era reads it (half-life about 2.8 years)
    era_switch=14,      # quarters the order must point elsewhere before the era turns
    era_keep=0.5,      # an era holds while the order's lean still points this much its way (cosine)
    mixed_acc=1.0,     # mixed regimes (-5 to 6, as the snapshot) are the least stable (Hegre et al. 2001): more pressure ...
    mixed_hold=0.25,   # ... less hold (closed regimes keep their extra hold) ...
    mixed_hab=0.85,    # ... and people there get used to the gap less (times q_hab) (spec 6 §8; estimates)
    # ---- institutions (spec 4)
    inst_lead=0.03,    # quarterly pull of a profile toward its leader's pie
    inst_mission=0.006,   # pull back toward the native mission
    inst_routine=0.0015,  # drift toward ROUTINE, times age/50
    inst_olig=0.010,   # drift toward OLIGARCHY, times corruption
    tenure_q=24.0,     # mean leader tenure in quarters (about 6 years; estimate)
    firm_exit=0.020,   # quarterly exit hazard of a local firm at normal finances (about 9% a year)
    pub_exit=0.004,    # quarterly closure or merger of a public employer at a normal budget (about 1.6% a year; estimate)
    firm_big=0.25,     # national firms and banks exit at this fraction of that
    scandal0=0.0015,   # quarterly scandal hazard at zero corruption
    scandal_c=0.03,    # added per unit of corruption times media scrutiny
    # ---- outer ring (spec 5)
    new_tech=1 / 20.0, # yearly chance a new kind of technology appears (one every 15-25 y; estimate)
    tech_r=0.24,       # yearly logit speed of a new kind (smartphones 35% to 85% in 10 y: ~0.235)
    pand_haz=0.02,     # yearly chance of a pandemic as severe as COVID-19 (Marani et al. 2021)
    dis_base=(0.035, 0.025, 0.01, 0.025, 0.02), # yearly disaster chance per unit of hazard (flood fire quake storm heat;
                                                # about 1 in 25 years for a typical locality at today's warming, estimate)
    dis_active=1.0,    # rate_mult("disaster") is this much higher while a locality recovers from a strike (estimate)
    war_rel=(0.0, 0.0002, 0.0012, 0.004),       # quarterly war hazard with a neighbour by relation
    war_dem=0.1,       # two democracies fight this much less (Russett and Oneal 2001)
    war_abroad=0.003,  # quarterly chance of sending troops abroad in an outside war (estimate; R7: rare, abroad)
    war_home_p=0.25,   # share of wars with a hostile closed neighbour fought at home
    mig0=0.009,        # yearly migrant inflow, share of population (OECD; stock about 1 in 7)
    mig_out=0.045,     # yearly return or onward migration of the migrant stock
    secularise=0.10,   # share of the faithful young who leave at coming of age in normal secure times
    leave_p=0.0065,    # yearly chance an adult leaves their faith, times an age weight peaking at 15-25 (Pew 2015:
                       # about 1 in 3 over a lifetime, most by their late twenties)
    join_p=0.004,      # yearly chance a secular adult joins a faith
    switch_p=0.002,    # yearly chance of changing faith
    # ---- stage 3 of the v22 update (chroma-world/model/stage3-rules.md §2, §3, §8). Each switch is a rule; off, the
    # world runs exactly as v22.1 (engine UPD_OFF; a world saved before stage 3 loads with them off). Off by default:
    # stage 1 goes live alone as v22.2 (Emren 10-09 19:15 UTC), these come on with stages 2 to 4 (v22.3). Values: the
    # refit of 10-09 (Emren chose "Settle" 20:32 UTC), fitted on 8 worlds x 300 years and checked on 24 (stage3-rules.md §7)
    cult_schools=False, cult_scenes=False, cult_adults=False, cult_anchor=False, cult_pushback=False, cult_shake=False,
    cult_no_dice=False, hist_party_gov=False, hist_pressure=False, hist_grievance=False, hist_chance_only=False,
    coh_inst=0.0023,   # LW1 1b: the young take in what schools, universities and media stand for (I -> K)
    coh_scene=0.032,   # LW1 1c: the mobilised groups' want (and a revival's faith) reaches the young (G -> K)
    coh_adult=0.27,    # LW1 1d: generations past 25 move with the times at this share of the young's pace (Danigelis 2007)
    coh_home=0.59,     # LW1 1e (reworked): the young's pull toward the starting values moved by the era
    era_home_k=0.34,   # LW1 1e: how far an era moves that target (times its intensity and colours, era_p - .2)
    era_fade_y=4.7,    # LW1 1e: an era's hold on the young fades with its age (years, e-folding)
    coh_back=0.059,    # LW1 1f: groups left behind brake the culture's change of the last decade (Norris and Inglehart 2019)
    acc_calm=1.61,     # LW1 1g: the shake index acc in a calm year (median of calm years, tools/world_alone.py, 10-09)
    k_sh=3.43,         # LW1 1g: m_sh = clip(1 + k_sh (acc - acc_calm), 1, 3): about 1 decade in 5 shaken
    gov_voter=0.14,    # LW2 2a: a new government moves this far from its party's colours toward what voters want
    lead_k=0.26,       # LW2 2a: the head of government's own touch
    party_k=0.01,      # LW2 2a': quarterly pull of a party toward its voters (Adams, Clark, Ezrow and Glasgow 2004)
    loser_k=0.058,     # LW2 2a': ... and of a party that lost office toward the median, for four quarters
    q_theta_s3=0.11, q_k_s3=0.43, q_hab_s3=0.48, era_on_s3=0.0042, era_off_s3=0.0015,   # LW2 2c: pressure, habit, eras (refit)
    q_tol_s3=0.0116, q_decay_s3=0.0070,   # LW2 2c: the gap people live with and the fading of pressure (refit)
    th_dem_s3=0.33,    # LW2 2b: the public leans against whoever governs (th_dem), refit with 2a's governments
    coh_gain=2.91,     # LW1: the era's and the times' security pull on the young (coh_era, coh_sec), refit with the rest
    lose_k=18.2,       # LW2 2d: grievance built per unit of a group's loss at a breakthrough or an era's start
    grv_fade=1 / 15.0, # LW2 2d: yearly fading of a grievance
    lead_spread_s3=0.15,  # LW2 2e: spread of an institution leader's colours around the government's or society's
    # ---- the spheres of society (item 15, v22.3 stage 2; chroma-engine/notes/spheres-plan.md). Off, nothing of them is
    # computed or saved and the world runs as v22.2
    sph_town=False,    # phase 1c: each town's nine spheres, their sizes and five face shares, updated each quarter (read only)
    sph_par=None,      # {name: value} over sphere_data.PARAMS (tuning; None: the design values)
    sph_haunts=False,  # phase 2, N1: named places per town and haunt kind, each with its own face mix; lives pick haunts
    sph_hours=False,   # phase 2: hours in all nine spheres and the rungs (N2), the places part of item 12's current
    sph_marks=False,   # phase 2: the mark of the work (reserved: waits for the Outer world's table of trades)
    sph_events=False,  # phase 3: the 195 sphere events (hazards, effect rows on the faces, chains); rates from the data
    sph_ev_base=None,  # phase 3 tuning and checks: one quarterly base chance for every event, in place of the data's
    sph_seasons=False, # phase 3, N7: the year's rhythm (dynamics.json seasons) on each sphere's event hazards and hours
    sph_joins=False,   # phase 3, N6: an event's shift spills to joined spheres at J x (1 - separation) (epochs.json)
    sph_pairs=False,   # phase 3: the ten pair faces per town sphere (dynamics.json pair_faces), a layer over two faces
    sph_links=False,   # phase 3: the 72 sphere-to-sphere links (links.json, through their via states) and their colour
                       # readings (colour.by_colour); with sph_events (the states are the events')
    sph_memory=False,  # phase 3: the four memories that make history (credit, plague, land, command; events_run.memories)
    pair_calm=False,   # phase 3: a held pair face calms its pair's quarrel events in its sphere, a broken one makes them
                       # flare (events_run.pair_quarrels); with sph_pairs
    sph_cascades=False,  # phase 3: the 14 cascades (links.json colour.cascades): a running cascade raises its next step
    sph_levers=False,  # phase 4: the nine levers on a place or a town's sphere, by reach and rung (dynamics.json levers;
                       # Outer world's answers in chroma-world/spheres/phase4-answers.md)
    sph_fair=False,    # phase 4: felt fairness per life and sphere (dynamics.json felt_fairness), read by the options
    sph_shadow=False,  # phase 5, N5: each face's shadow share per town and sphere (event rows' shadow turns, subvert,
                       # the fairness gap), the spheres' grey shares, and the shadow around a life (notes/spheres-phase5-asks.md)
    sph_deep=False,    # phase 5: the deep state of a life (the care load first; service, debts, holdings to come)
    far_ties=False,    # item 18: a town's events touch the named people living there; a close tie in another town calls
                       # (chroma-ideas/far-off-events.md; sides in sphere_data.FAR); with sph_events
    far_par=None,      # far_ties tuning: {name: value} over world_people.FAR_DEFAULT (None: the start values)
    sacred=False,      # S5, sacred lines (chroma-ideas/social-mechanics.md): a life grows up to two lines it will not sell;
                       # sphere and C3 events offer a price for them (sphere_data.OFFER); with sph_events (and c3_inst)
    sacred_par=None,   # sacred tuning: {name: value} over world_people.SAC_DEFAULT (None: the start values)
    inst_even=False,   # phase 3: bodies drift toward their own past and their leaders' colours, not toward W with age
                       # or B with corruption (Emren's "Colour-even", spheres-implementation.md question 6)
    # ---- the C hooks of item 10 (chroma-world/model/stage3-rules.md section 5), built by the Outer world. Off, nothing of
    # them is drawn, computed or saved and the world runs as before
    c3_inst=False,     # C3: institution events (sold, merged, nationalised, a leak, a cover-up)
    c4_nature=False,   # C4: nature's own year (bad air, bad water, a poisoned river, drought, a glorious spring, recovery)
    c5_faith=False,    # C5: three new faith movement slots on the faith axis (founding, growth, fading, claims, tension)
    c_par=None,        # {name: value} over C_DEFAULT (tuning; None: the start values)
)
# the switches above (stage3-rules.md §8)
S3_RULES = ("cult_schools", "cult_scenes", "cult_adults", "cult_anchor", "cult_pushback", "cult_shake", "cult_no_dice",
            "hist_party_gov", "hist_pressure", "hist_grievance", "hist_chance_only")
SPH_RULES = ("sph_town", "sph_par", "sph_haunts", "sph_hours", "sph_marks", "sph_events", "sph_ev_base", "sph_seasons",
             "sph_joins", "sph_pairs", "inst_even", "sph_links", "sph_memory", "pair_calm", "sph_cascades",
             "sph_levers", "sph_fair", "sph_shadow", "sph_deep", "far_ties", "far_par",
             "sacred", "sacred_par")   # the spheres' switches and tuning (item 15); off, saved without them, as v22.2 saved
C_RULES = ("c3_inst", "c4_nature", "c5_faith", "c_par")   # the C hooks' switches and tuning (item 10); off, saved without them
# the C hooks' start values (stage3-rules.md section 5; estimates, refit at the stage's end). Yearly rates per place
C_DEFAULT = dict(
    sold=0.02, sold_poor=2.0, sold_pull=0.3,   # C3 sold: private firms and banks, twice as often with finances under .3;
                                     # the profile moves this far toward the sector's biggest firm
    merged=0.01, merge_jl=3.0, merge_share=0.25,   # C3 merged: a firm with a rival of its sector in its place; a quarter
                                     # of the moved staff face three times the job-loss rate for a quarter
    nat_share=0.5, nat_cap=0.5,      # C3 nationalised: half of big firms' and banks' closures in a deep recession, where
                                     # the state's capacity is .5 or more
    leak=0.02, leak_legit=0.05, leak_trust=0.001,   # C3 a leak: times (.5 + internet adoption) x (1.5 - capacity)
    cover=0.005, cover_c=0.03, cover_y0=1.0, cover_y1=5.0, cover_sc=3.0,   # C3 a cover-up: .5% + 3% x corruption, hidden
                                     # 1 to 5 years, the scandal rate x3 meanwhile; an insider's voice breaks it
    air=0.30, air_heat=0.5,          # C4 bad air: cities and industrial places; heat extremes against the birth's raise it
    water=0.02, river=0.005,         # C4 bad water and a poisoned river: industrial and mining places
    drought=0.08,                    # C4 drought: farming and hotter places, times drought extremes against the birth's
    spring=0.15,                     # C4 a glorious spring: everywhere, drawn in spring
    air_ill=1.2, water_ill=1.1, river_ill=1.15,   # C4 illness rate in the place, for a quarter (a river: two)
    water_serv=0.05, drought_serv=0.03,           # C4 the place's services lost
    drought_food=0.5, drought_fhaz=2.0,           # C4 a drought lifts food prices and doubles the food shock's chance
    rec_cost=0.03,                   # C4 recovery: the council's capacity spent rebuilding
    found=0.01, found_mean=3.0, found_speed=2.0,  # C5 founding, per society a year: 1% x (1 + 3 x unmet meaning above its
                                     # mean) x (1 + 2 x norm_speed), with a free slot
    succeed=0.1, ceil_lo=0.02, ceil_hi=0.08,      # C5 about 1 in 10 grows to 2 to 8% of the people (Stark 1996)
    fail_lo=0.002, fail_hi=0.008, fade_y0=5.0, fade_y1=15.0, fade=0.25,   # C5 the rest peak under 1% and fade from 5 to
                                     # 15 years on, a quarter of their members a year
    grow=0.35, seed_share=0.0005,    # C5 logistic growth a year toward the ceiling, from the founding's first members
    free_share=0.001, free_y=5.0, fail_y=20.0,    # C5 a slot frees under .1% after 5 years, or a failed movement at 20
    join_share=0.01,                 # C5 the cast take up a movement as their faith only once it holds 1% of the people
    claims=0.5,                      # C5 claims spread: a year's chance while a movement grows
    tension_share=0.05, tension_tv=0.25, tension_trust=0.41, tension_p=0.5,   # C5 faith tension: two faiths over 5%, far
                                     # apart, trust under .41 (the lowest tenth of years in a typical world); a tense year
                                     # shows in a town with this chance
    found_open=52,                   # C5 the founding gate stays open this many weeks in the founding's town
)
NM = 3   # C5: the faith axis's movement slots (faith index NF + k), only with c5_faith on
# their parameters; a world with every rule off saves without these keys, exactly as v22.1 saved it
S3_PARAMS = ("coh_inst", "coh_scene", "coh_adult", "coh_home", "era_home_k", "era_fade_y", "coh_back", "acc_calm", "k_sh", "gov_voter",
             "lead_k", "party_k", "loser_k", "q_theta_s3", "q_k_s3", "q_hab_s3", "era_on_s3", "era_off_s3", "coh_gain",
             "lose_k", "grv_fade", "lead_spread_s3", "q_tol_s3", "q_decay_s3", "th_dem_s3")

# ------------------------------------------------------------------------------------------------- small helpers


def _norm(x, lo=0.005):
    x = np.maximum(x, lo)
    return x / x.sum(-1, keepdims=True)


def _cl(x, lo, hi):
    """Clip a scalar (faster than np.clip on one number)."""
    x = float(x)
    return lo if x < lo else hi if x > hi else x


def _logit(p):
    p = _uclip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def _tv(a, b):
    """Half the L1 distance between two pies (0 same .. 1 disjoint)."""
    return 0.5 * np.abs(a - b).sum(-1)


def _jsafe(v):
    if isinstance(v, (np.floating, float)):
        return float(v)
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, np.ndarray):
        return [_jsafe(x) for x in v.tolist()] if v.dtype == object else v.tolist()
    if isinstance(v, dict):
        return {str(k): _jsafe(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsafe(x) for x in v]
    return v


class World:
    """The shared outer world. See the module docstring and world-build.md for what it exposes."""

    _STREAMS = dict(setup=0, nature=1, abroad=2, economy=3, state=4, institution=5, place=6, culture=7, society=8,
                    figure=9, tech=10, belief=11, group=12)
    _CONST = ("p", "cfg", "perm", "NEEDM", "LOADP", "NPROF", "WPROF", "GMIX", "FPROF", "ROUT", "OLIG", "VPRE",
              "DSEC", "DOPEN", "DENT", "R", "pace", "gidx", "gadult", "_seed", "trace")

    # ------------------------------------------------------------------------------------------------ construction
    def __init__(self, seed, cfg=None, color_perm=None, params=None, society=0, start_t=0):
        """society > 0 and start_t are for spawn_neighbour: the neighbour's own streams, and its clock at setup."""
        cfg = dict(CFG_DEFAULT, **(cfg or {}))
        self.cfg = cfg
        self.p = dict(W_DEFAULT, **(params or cfg.get("params") or {}))
        self._seed = int(seed)
        self.perm = np.arange(C) if color_perm is None else np.asarray(color_perm, int)
        self.pace = float(cfg["pace"])
        self._tables()
        self.society_id = int(society)                     # 0 = home; a spawned neighbour is its index + 1 (spec 5 §5)
        self.R = [np.random.default_rng([self._seed + 104729, k] + ([self.society_id] if self.society_id else []))
                  for k in range(len(self._STREAMS))]
        self.log, self.record, self.push_log = [], [], []
        self._queue = []
        self._setup(int(start_t))

    def _s3(self, k):
        """Whether a stage 3 rule of the v22 update is on (stage3-rules.md §8)."""
        return bool(self.p.get(k, False))

    def _tables(self):
        """Every color-indexed table, permuted once (color_perm)."""
        P = self.perm
        self.NEEDM = NEED_MAP[:, P]
        self.LOADP = LOAD[:, P]
        self.NPROF = NORM_PROF[:, P]
        self.WPROF = WELFARE_PROF[P]
        self.GMIX = {g: m[P] for g, m in GUILD_MIX.items()}
        self.FPROF = FAITH_PROF[:, P]
        if self.p.get("c5_faith"):                         # C5: the slots' colours (even until a movement is founded)
            self.FPROF = np.vstack([self.FPROF, getattr(self, "c5_prof", np.full((NM, C), 0.2))])
        self.ROUT, self.OLIG = ROUTINE[P], OLIGARCHY[P]
        pre = self.cfg["preset"]
        if isinstance(pre, (list, tuple, np.ndarray)):       # a value climate in the canonical frame (spawn_neighbour)
            self.VPRE = _norm(np.asarray(pre, float))[P]
        else:
            self.VPRE = (V_RICH if pre == "typical rich" else np.full(C, 0.2))[P]
        L = self.LOADP
        V_ = {v: i for i, v in enumerate(VALUES)}
        def d(plus, minus):
            x = L[[V_[v] for v in plus]].sum(0) - L[[V_[v] for v in minus]].sum(0)
            return x / np.abs(x).max()                       # zero-sum (LOAD rows sum to 0), largest share 1
        self.DSEC = d(["self-direction", "universalism"], ["security", "tradition"])      # secure vs insecure youth
        self.DOPEN = d(["self-direction", "stimulation", "universalism"], ["tradition", "conformity", "security"])
        self.DENT = d(["achievement", "stimulation"], ["security", "conformity"])          # enterprise vs caution

    def _profile_src(self, src):
        if src in self.GMIX or " " in src and all(t in self.GMIX for t in src.split()):
            return 0.6 * np.mean([self.GMIX[t] for t in src.split()], 0) + 0.08
        return 0.6 * _mix(src)[self.perm] + 0.08

    def _cn(self, r, *shape):
        """Color-indexed normal noise, drawn in the canonical frame and permuted like every color table."""
        return r.normal(size=shape + (C,))[..., self.perm]

    def _setup(self, start_t=0):
        p, r = self.p, self.R[0]
        cfg = self.cfg
        # clock
        self.t = self.t0 = int(start_t)
        self.week_of_year = self.t % 52
        self.season = int(WEEK_SEASON[self.week_of_year])
        self.clim_t0 = None                                # the climate scenario's anchor (the first birth), set once
        self.rich = 1.0                                    # how rich against home (a spawned neighbour: its ext_rich)
        # ---- economy
        self.phase, self.severity, self.exp_q, self.rec_q, self.rec_len, self.last_sev = 0, 0, int(r.integers(0, 16)), 0, 0, 0
        self.gap, self.gap_prev, self.gap_ema, self.housing, self.house_m = 0.05, 0.05, 0.0, 0.0, 0.0
        self.house_hist = np.zeros(12)
        self.natural = float(p["u_nat"])
        self.u_rise, self.u_rise_tgt, self.u_noise = 0.0, 0.0, 0.0
        self.unemp, self.unemp_prev = self.natural, self.natural
        self.infl, self.infl_e = p["infl0"], 0.0
        self.energy, self.food = 0.0, 0.0
        self.ineq = p["ineq0"]
        self.sector_tilt = np.zeros(5)
        self.payoff = np.full(C, 0.2)
        self.rec_declared, self.rec_start_t, self.rec_end_t = False, -1, -1
        self.n_rec = 0
        # ---- technology (setup level)
        lvl = cfg["tech_level"]
        self.tech_ceil = np.array(TECH_CEIL[lvl], float)
        self.tech_keys = list(TECH_KEYS)
        self.tech_adopt_v = self.tech_ceil.copy()
        self.tech_exists = self.tech_ceil > 0
        self.tech_kind = [-1] * NT                         # NEW_TECH index for kinds that arrived later
        self.tech_born = [0] * NT
        self.automation = np.array([.10, .25, .15, .10, .03]) * (0.7 if lvl == "behind" else 1.3 if lvl == "ahead" else 1.0)
        self.medical0 = {"behind": .55, "modern": .70, "ahead": .80}[lvl]
        self.medical = self.medical0
        self.comm = float(0.5 * self.tech_ceil[0] + 0.5 * self.tech_ceil[2])
        self.watch = {"behind": .25, "modern": .40, "ahead": .55}[lvl]
        # ---- nature
        self.climate = cfg["climate"]
        self.warming = self._warming(0)
        self.extremes = self._extremes(self.warming)
        self.pandemic, self.pand_q = 0, 0
        self.pand_n = 0
        # ---- localities (spec 3 §2)
        boom_energy = r.random() < 0.5
        rows = [list(x) for x in LOC_TABLE]
        if boom_energy:
            rows[-1][0], rows[-1][1], rows[-1][6] = BOOM_ENERGY
        nl = len(rows)
        self.n_loc = nl
        self.loc_kind = np.array([LOC_KINDS.index(x[0]) for x in rows])
        self.loc_kind_key = [x[0] if cfg["setting"] == "earth" else LOC_KIND_ALIASES[cfg["setting"]][x[0]] for x in rows]
        self.loc_feat = np.array([[f in x[1].split() for f in FEATURES] for x in rows])
        self.loc_size = np.array([x[2] for x in rows])
        self.loc_density = np.array([x[3] for x in rows], float)
        self.loc_pop0 = np.array([x[4] for x in rows], float); self.loc_pop0 /= self.loc_pop0.sum()
        self.loc_pop_share = self.loc_pop0.copy()
        self.loc_class_mix = np.array([x[5] for x in rows], float)
        self.loc_sector_base = np.array([x[6] for x in rows], float)
        self.loc_sectors = self.loc_sector_base.copy()
        self.loc_ufac = np.array([x[7] for x in rows], float)
        self.loc_rent0 = np.array([x[8] for x in rows], float)
        self.loc_rent = self.loc_rent0.copy()
        self.loc_crime0 = np.array([x[9] for x in rows], float)
        self.loc_crime = self.loc_crime0.copy()
        hz = np.array([x[10] for x in rows], float)
        hz[:, 2] *= r.uniform(0.0, 2.0)                    # how seismic this world's land is
        self.loc_hazards = _uclip(hz * np.exp(0.2 * r.normal(size=hz.shape)), 0, 1)
        self.loc_nature = np.array([x[11] for x in rows], float)
        self.loc_place = np.array([x[12] for x in rows])
        self.loc_services = _uclip(np.array([[.6, .55, .4], [.7, .65, .55], [.8, .75, .7], [.85, .85, .85]])[self.loc_size]
                                    + 0.05 * r.normal(size=(nl, 3)), 0.1, 1)
        self.loc_unemp = np.full(nl, self.natural)
        self.loc_trend = np.ones(nl, int)
        self.loc_growth = np.zeros(nl)
        self.loc_disaster = np.zeros(nl)                   # years of recovery left after a disaster
        self.disaster_now = np.zeros(nl)                   # severity of a disaster striking this week (0 none)
        self.disaster_kind = np.full(nl, -1)               # its HAZARDS index (-1 none)
        self.dis_pending, self.dis_on = [], False          # [week, loc, hazard, severity] drawn for the coming quarter
        self.loc_next_vote = r.integers(1, 20, nl)
        self.loc_crime_ma = self.loc_crime.copy()
        ref_mult = self._extremes(self._warming_now())
        self.haz_ref = float((self.loc_pop0 * (self.loc_hazards * np.array(p["dis_base"]) * ref_mult).sum(1)).sum())
        self.crime_ref = float((self.loc_pop0 * self.loc_crime0).sum())
        # neighbourhoods
        nbn = np.array([1, 3, 4, 5])[self.loc_size]
        self.nb_loc = np.repeat(np.arange(nl), np.asarray(nbn).astype(np.intp))   # intp: the browser's numpy is 32-bit
        q = np.concatenate([(np.arange(k) + 0.5) / k for k in nbn])
        cum = np.cumsum(self.loc_class_mix, 1)[self.nb_loc]
        self.nb_class = (q[:, None] > cum[:, :2]).sum(1)
        self.n_nb = len(self.nb_loc)
        self.nb_efficacy = _uclip(np.array([.45, .58, .70])[self.nb_class] + 0.06 * r.normal(size=self.n_nb), .1, .95)
        self.nb_crime = self.loc_crime[self.nb_loc].copy()
        # ---- population groups (spec 2 §6): age band x class x place x faith (0 secular, 1.. faiths) x migrant
        self.pop = self._init_pop(r)
        g = np.indices(self.pop.shape).reshape(5, -1)
        self.gidx = g
        self.gadult = g[0] >= 1
        # ---- culture, generations
        self.Y0 = 110                                      # cohort array row of birth year 0 (oldest born -110 y)
        y0 = self.t // 52                                  # 0 at home; a spawned neighbour starts later
        ncoh = self.Y0 + max(400, y0 + 130)
        nz_ = self._cn(r, ncoh)
        if self._s3("cult_no_dice"):                       # LW1 1h: no dice in the culture
            nz_ = 0.0 * nz_
        self.coh = np.tile(self.VPRE, (ncoh, 1)) * np.exp(p["coh_noise"] * nz_)
        self.coh /= self.coh.sum(1, keepdims=True)
        self.coh_fixed = np.zeros(len(self.coh), bool); self.coh_fixed[:self.Y0 + y0 - 14] = True
        self.coh_n = np.zeros(len(self.coh)); self.coh_n[:self.Y0 + y0 - 14] = 11
        self.V_anchor = self.VPRE.copy()
        self.mig_tilt = np.zeros(C)
        self.norm_x = _logit(np.array([NORM_START[k] for k in NORM_KEYS]))
        self.norm_x += 0.25 * r.normal(size=NN)
        self.norm_x0 = _logit(np.array([NORM_MOD[k] for k in NORM_KEYS]))      # modern acceptance under the modern law
        self.lawsign0 = np.zeros(NN)
        self.lawsign0[:NL] = 1.0 - np.array([LAW_MOD[k] for k in LAW_KEYS])
        for kk, v in RIGHT_MOD.items():
            self.lawsign0[NI[kk]] = 2 * v - 1
        self.norm_hist = np.tile(self.norm_x, (21, 1))      # last 5 years, quarterly
        self.norm_push = np.zeros(NN)
        self.norm_pub = _sig(self.norm_x).round(2)
        self.trust, self.fear, self.polar = p["trust0"], p["fear0"], 0.1
        self.spiritual, self.conspiracy = 0.15, 0.10
        # ---- belief
        self.cosmology = COSMOLOGY.get(cfg["setting"], "believed")
        self.holy_shift = np.zeros(self._nf())
        # ---- state
        self.regime = p["regime0"] if cfg["preset"] in ("typical rich", "even") else float(cfg.get("regime", p["regime0"]))
        self._regime_derived()
        self.laws = np.array([LAW_START[k] for k in LAW_KEYS], int)
        self.law_push = np.zeros(NL)
        self.law_since = np.zeros(NL)
        self.welfare, self.welfare_pub = 0.45, 0.45
        self.rights = np.array([.85, .85, .9, .2, .45])
        self.unrest, self.war, self.war_with, self.war_q, self.lost_war_q = 0.05, 0, -1, 0, 0
        self.lockdown = 0.0
        # ---- belief shares, value climate and demand need the population
        self._group_mix()
        self.V = self._V()
        self.Vc_hist = [self.V.tolist()]
        Dem0 = self.V.copy()
        self.Dem, self.Dem_q = Dem0.copy(), Dem0.copy()
        self.G = _norm(Dem0 * np.exp(p["g_noise"] * self._cn(r)))
        self.support, self.gov_q, self.next_vote = p["s_win"], 0, int(r.integers(4, 20))
        self.gov_party, self.opp_party = 0, 1
        self.u_at_office = self.natural
        # ---- other societies (spec 5 §5)
        self._init_ext(r)
        # ---- institutions (spec 4) and public figures (spec 5 §6)
        self._init_inst(r)
        self._init_figs(r)
        if self._s3("hist_chance_only"):                   # LW2 2e: the first government is its party's (drawn as before)
            self.G = self.inst_profile[self.party_ids[self.gov_party]].copy()
        # ---- society (spec 6)
        self.Q, self.open_q, self.since_break, self.gap_now = 0.0, 0, 40, 0.0
        self.Pos = self._pos()
        self.Pos_slow = self.Pos.copy() if p["era_ref"] > 0 else np.full(C, 0.2)
        self.Pos_era = self.Pos.copy()
        self.pos_hist = np.tile(self.Pos, (41, 1))         # last 10 years, quarterly
        self.gap_slow = _tv(self.Pos, self.Dem_q)
        self.need_base = np.zeros(5)
        self.unmet_mean = np.zeros(5)
        self.era_i, self.era_k, self.era_key, self.era_p = 0.0, 0, None, np.zeros(C)
        self.era_since, self.era_lead, self.era_lead_q, self.n_era = -1, -1, 0, 0
        self.era_at = []                                   # [t, key, intensity, kind] at each era start
        self.harsh_loc = np.zeros(nl)
        self.loc_mix = np.tile(self.V, (nl, 1))
        self.loc_gov = _norm(self.loc_mix * np.exp(0.25 * self._cn(r, nl)))
        self.prosper = self.gap
        self.unemp_sector = np.full(5, self.natural)
        self.unemp_loc = self.loc_unemp
        self._derive_econ()
        self.revival = (0, 0)
        self.norm_speed = 0.0
        self.cycles = []          # hidden: [start t, end t, severity] of each recession (tests; never published)
        self.trace = [] if cfg.get("trace") else None

    def _init_pop(self, r):
        """Age x class x place x faith x migrant shares of a typical rich democracy (estimates: OECD age structure,
        about 4 in 5 urban, migrant stock rising toward 1 in 7, faith of the older society at the burn-in's start)."""
        age = np.array([.16, .12, .13, .13, .13, .13, .11, .09])
        place = np.array([(self.loc_pop0 * (self.loc_place == k)).sum() for k in range(3)])
        cls = np.array([[.28, .48, .24], [.33, .52, .15], [.35, .53, .12]])           # by place
        sec = np.array([.16, .16, .14, .12, .10, .08, .07, .06])                        # secular share by age
        fsh = np.array([.86, .08, .06])                                                  # among the faithful, natives
        mig_f = np.array([.25, .30, .15, .30])                                           # migrants: secular, faiths
        mig_age = np.array([.05, .18, .25, .20, .14, .09, .06, .03])
        mig = 0.08
        pop = np.zeros((8, 3, 3, NF + 1, 2))
        for a in range(8):
            fn = np.concatenate([[sec[a]], (1 - sec[a]) * fsh])
            for pl in range(3):
                pop[a, :, pl, :, 0] = (1 - mig) * age[a] * place[pl] * cls[pl][:, None] * fn[None, :]
                pop[a, :, pl, :, 1] = mig * mig_age[a] * place[pl] * np.array([.45, .45, .10])[:, None] * mig_f[None, :]
        if self.p.get("c5_faith"):                         # C5: the movement slots, empty at the start
            pop = np.concatenate([pop, np.zeros((8, 3, 3, NM, 2))], axis=3)
        return pop / pop.sum()

    def _nf(self):
        """The faiths on the faith axis: NF, and C5's NM movement slots when it is on."""
        return NF + (NM if self.p.get("c5_faith") else 0)

    def _regime_derived(self):
        demo = _cl((self.regime + 10) / 20, 0, 1)
        self.demo = demo
        self.law_rule = 0.3 + 0.6 * demo ** 1.5
        self.capacity = 0.45 + 0.4 * demo
        self.rights_base = demo ** 1.5

    def _init_ext(self, r):
        n = int(r.integers(3, 6))
        self.n_ext = n
        reg = np.where(np.arange(n) < 2, r.uniform(7, 10, n), 0.0)
        for j in range(2, n):
            u_ = r.random()
            reg[j] = r.uniform(7, 10) if u_ < 0.45 else r.uniform(-5, 5) if u_ < 0.8 else r.uniform(-10, -6)
        self.ext_regime = reg
        self.ext_V = _norm(np.tile(self.VPRE, (n, 1)) * np.exp(0.15 * self._cn(r, n)))
        self.ext_anchor = np.tile(self.VPRE, (n, 1))       # where each neighbour's value climate drifts back to
        self.ext_society = np.arange(n) + 1                # each neighbour's society id (spawn_neighbour)
        self.ext_G = _norm(self.ext_V * np.exp(0.3 * self._cn(r, n)))
        self.ext_rich = np.where(reg >= 6, r.uniform(0.7, 1.1, n), r.uniform(0.2, 0.6, n))
        rel = np.where(reg >= 6, np.where(r.random(n) < 0.6, 0, 1), np.where(r.random(n) < 0.5, 1, 2))
        self.ext_relation = rel.astype(int)
        self.ext_trade = r.uniform(0.05, 0.3, n) * np.where(reg >= 6, 1.0, 0.5)
        self.ext_phase = np.zeros(n, int)
        self.ext_rec_q = np.full(n, 99)                     # quarters since a recession started
        self.ext_exp_q = r.integers(0, 16, n)
        self.ext_war = np.zeros(n, int)                     # at war (with anyone) 0/1
        self.ext_migration = np.zeros(n)
        self.ext_next_gov = r.integers(8, 40, n)
        self.world_rec, self.world_q = 0, 0
        self.trade_hit = 0.0
        self.mig_in = self.p["mig0"]

    def _init_inst(self, r):
        rows = []                                           # kind, level, loc, native, sector, public
        def add(kind, level, loc, native, sector=-1, public=True):
            rows.append((INST_KINDS.index(kind), level, loc, native, sector, public))
        for l in range(self.n_loc):
            s = self.loc_size[l]
            for _ in range([1, 2, 3, 4][s]): add("school", 0, l, self._profile_src(NATIVE_SRC["school"][0]))
            if s >= 1:
                for _ in range(2 if s == 3 else 1): add("hospital", 0, l, self._profile_src("simic"))
            add("police", 0, l, self._profile_src("boros"))
            add("council", 0, l, self._profile_src("azorius"))
            for _ in range([1, 2, 3, 4][s]):
                sec = int(r.choice(5, p=self.loc_sector_base[l]))
                add("employer", 0, l, self._profile_src(SECTOR_GUILDS[sec][int(r.integers(len(SECTOR_GUILDS[sec])))]), sec, sec == 4)
        for l in UNIVERSITY_LOCS: add("university", 1, l, self._profile_src("simic izzet"))
        for l in COURT_LOCS: add("court", 1, l, self._profile_src("azorius"))
        for l in PRISON_LOCS: add("prison", 1, l, self._profile_src("boros"))
        for l in RMEDIA_LOCS: add("media", 1, l, self._profile_src(NATIVE_SRC["media"][int(r.integers(2))]), -1, False)
        add("court", 2, 0, self._profile_src("azorius"))
        for _ in range(3): add("ministry", 2, 0, self._profile_src("azorius"))
        add("army", 2, 0, self._profile_src("boros"))
        add("media", 2, 0, self._profile_src("rakdos"), -1, False); add("media", 2, 0, self._profile_src("dimir"), -1, False)
        for _ in range(3): add("bank", 2, 0, self._profile_src("orzhov"), 3, False)
        for sec in (1, 2, 3, 3):
            add("employer", 2, 0, self._profile_src(SECTOR_GUILDS[sec][int(r.integers(len(SECTOR_GUILDS[sec])))]), sec, False)
        for _ in range(2): add("union", 2, 0, self._profile_src("gruul selesnya"), -1, False)
        for _ in range(2): add("charity", 2, 0, self._profile_src("selesnya"), -1, False)
        for f in range(NF): add("faith body", 2, 0, self.FPROF[f].copy(), -1, False)
        self.party_ids = []
        for j in range(4):
            prof = _norm(self.V * np.exp(0.35 * self._cn(r)))
            self.party_ids.append(len(rows)); add("party", 2, 0, prof, -1, False)
        n = len(rows)
        self.n_inst = n
        self.inst_kind = np.array([x[0] for x in rows]); self.inst_level = np.array([x[1] for x in rows])
        self.inst_loc = np.array([x[2] for x in rows]); self.inst_native = np.array([x[3] for x in rows])
        self.inst_sector = np.array([x[4] for x in rows]); self.inst_public = np.array([x[5] for x in rows])
        self.inst_profile = self.inst_native.copy()
        self.inst_faith = np.full(n, -1); fb = np.nonzero(self.inst_kind == INST_KINDS.index("faith body"))[0]
        self.inst_faith[fb] = np.arange(NF)
        self.party_ids = np.array(self.party_ids)
        k = self.inst_kind
        K = {x: INST_KINDS.index(x) for x in INST_KINDS}
        self.inst_firm = ((k == K["employer"]) & ~self.inst_public) | (k == K["bank"])     # market firms
        self.inst_pubemp = (k == K["employer"]) & self.inst_public                         # public employers
        reach = np.array([{"school": .4, "university": 1.5, "employer": 1.0, "bank": 2.0, "hospital": .8, "police": .6,
                           "court": .8, "prison": .3, "army": 1.5, "faith body": 0.0, "media": 1.0, "party": 0.0,
                           "union": 1.5, "charity": .8, "council": .4, "ministry": 2.0}[INST_KINDS[x]] for x in k])
        reach *= np.where(self.inst_level == 2, 2.5, 1.0)
        self.inst_reach = reach                            # faith bodies get their faith's share, yearly
        base = {"school": .65, "university": .65, "employer": .50, "bank": .45, "hospital": .70, "police": .60,
                "court": .52, "prison": .40, "army": .65, "faith body": .48, "media": .46, "party": .25, "union": .45,
                "charity": .60, "council": .45, "ministry": .40}   # OECD Trust Survey 2023 where measured (media set
                                                                         # higher so its lower capacity lands it near 0.4); others estimates
        self.inst_legit0 = np.array([base[INST_KINDS[x]] for x in k])
        self.inst_legitimacy = _uclip(self.inst_legit0 + 0.05 * r.normal(size=n), .05, .95)
        self.inst_capacity = _uclip(0.7 + 0.08 * r.normal(size=n), .2, 1)
        self.inst_corruption = _uclip(0.12 + 0.05 * r.normal(size=n), .01, .6)
        self.inst_age = r.uniform(5, 80, n)
        self.inst_age[self.inst_firm & (self.inst_level == 0)] = r.uniform(0, 30, (self.inst_firm & (self.inst_level == 0)).sum())
        self.inst_finances = _uclip(0.5 + 0.15 * r.normal(size=n), 0, 1)
        self.inst_leader_fig = np.full(n, -1)
        self.inst_leader_pie = _norm(np.where(self.inst_public[:, None], self.G, self.V) * np.exp(0.3 * self._cn(r, n)))
        self.inst_leader_q = r.integers(0, 24, n).astype(float)
        self.inst_gen = np.zeros(n, int)                    # bumps when a firm closes and a new one takes its place
        oc = np.array([.78, .92, 1.0])
        self.inst_open_cls = _uclip(oc + 0.04 * r.normal(size=(n, 3)), .3, 1)
        self.inst_open_mig = _uclip(0.70 + 0.05 * r.normal(size=n), .3, 1)    # Bertrand and Mullainathan 2004: ~2/3
        self._openness()
        self._state_corruption()

    def _state_corruption(self):
        """state.corruption (package registry): the public bodies' corruption weighted by their reach."""
        w = self.inst_public * self.inst_reach
        self.corruption = float(w @ self.inst_corruption / max(float(w.sum()), 1e-9))

    def _openness(self):
        self.inst_openness = (self.inst_open_cls[:, :, None] * np.stack([np.ones(self.n_inst), self.inst_open_mig], 1)[:, None, :]).reshape(self.n_inst, 6)

    def _init_figs(self, r):
        self.F_role, self.F_pie, self.F_standing, self.F_alive, self.F_party = [], [], [], [], []
        self.F_born, self.F_female, self.F_mom, self.F_active, self.F_inst = [], [], [], [], []
        self.fig_role_now = {}
        self.fig = -1
        for role in range(len(FIG_ROLES)):
            self._new_fig(r, role, quiet=True)

    # public figures as arrays (world-build.md: W.fig_* role, pie, standing, alive, party)
    fig_role = property(lambda self: np.array(self.F_role, int))
    fig_pie = property(lambda self: np.array(self.F_pie, float).reshape(-1, C))
    fig_standing = property(lambda self: np.array(self.F_standing, float))
    fig_alive = property(lambda self: np.array(self.F_alive, bool))
    fig_party = property(lambda self: np.array(self.F_party, int))
    fig_born = property(lambda self: np.array(self.F_born, int))
    fig_female = property(lambda self: np.array(self.F_female, bool))
    fig_active = property(lambda self: np.array(self.F_active, bool))
    fig_inst = property(lambda self: np.array(self.F_inst, int))

    def _set_role(self, role, fid):
        old = self.fig_role_now.get(role)
        if old is not None and old != fid:
            self.F_active[old] = False
        self.fig_role_now[role] = fid
        self.F_role[fid] = role; self.F_active[fid] = True
        inst = self.F_inst[fid]
        if role in (0, 1):
            inst = int(self.party_ids[self.F_party[fid]]); self.F_inst[fid] = inst
        if inst >= 0:
            self.inst_leader_fig[inst] = fid; self.inst_leader_pie[inst] = np.asarray(self.F_pie[fid]); self.inst_leader_q[inst] = 0
        self.fig = self.fig_role_now.get(0, -1)

    def _new_fig(self, r, role, quiet=False, party=None):
        """A new public figure rises into a role (spec 5 §6). Pies come from what the role stands in (party, faith,
        firm, the society), never from a rule about the role's colors."""
        x = r.random(4); nz = self._cn(r)
        rn = FIG_ROLES[role]
        inst = -1
        if role in (0, 1):
            party = (self.gov_party if role == 0 else self.opp_party) if party is None else party
            inst = int(self.party_ids[party]); base = self.inst_profile[inst]
        elif rn == "preacher":
            inst = int(np.nonzero(self.inst_faith == int(np.argmax(self.faith_share[:NF])))[0][0]); base = self.FPROF[self.inst_faith[inst]]
        elif rn == "scientist":
            inst = int(np.nonzero(self.inst_kind == INST_KINDS.index("university"))[0][0]); base = self.inst_profile[inst]
        elif rn == "magnate":
            cand = np.nonzero(self.inst_firm & (self.inst_level == 2))[0]; inst = int(cand[int(x[3] * len(cand))]); base = self.inst_profile[inst]
        elif rn == "activist":
            base = self.Dem_q
        else:
            base = self.V
        pie = _norm(base * np.exp((0.35 if rn in ("star", "athlete") else 0.25) * nz))
        fid = len(self.F_role)
        age = {"athlete": 22, "star": 26}.get(rn, 40) + 12 * x[0]
        self.F_role.append(role); self.F_pie.append(pie.tolist()); self.F_standing.append(float(0.35 + 0.3 * x[1]))
        self.F_alive.append(True); self.F_party.append(-1 if party is None else int(party))
        self.F_born.append(int(self.t - age * 52)); self.F_female.append(bool(x[2] < 0.5)); self.F_mom.append(0.05)
        self.F_active.append(True); self.F_inst.append(inst)
        self._set_role(role, fid)
        if not quiet:
            self._event("figure", "rises", rn, dict(fig=fid, party=self.F_party[fid]), big=role == 0)
        return fid

    # ------------------------------------------------------------------------------------------------ clock
    def burn_in(self, years=80):
        """The world alone before the birth (spec 5 §4). Ends with t0 = the birth's world week. The climate scenario is
        anchored at the first birth only: a saved world run on before a later birth keeps its warming."""
        self.t0 = self.t + int(round(years * 52))
        if self.clim_t0 is None:
            self.clim_t0 = self.t0
        while self.t < self.t0:
            self._week()
        return self

    def tick(self, week=None):
        """Run the world up to the given world week (every week in between), or one week when week is None."""
        target = self.t + 1 if week is None else int(week)
        while self.t < target:
            self._week()

    # ------------------------------------------------------------------------------------------------ emigration (spec 5 §5)
    def spawn_neighbour(self, k, years=60):
        """A full World for neighbour k, for a character who emigrates there (spec 5 §5).

        Built from the neighbour's light state here: its value climate (the preset), regime, richness (tech level),
        government colors, economy phase and relation, with its own streams from (seed, society id = k + 1). It runs
        alone for `years` before this world's clock (from 0 when this world is younger), so its t equals this world's
        t, and shares t0 and the climate anchor. In it this world is neighbour 0, its relation mirrored, and this
        world's other neighbours follow; ext_society gives each neighbour's society id. Nothing here touches this
        world's state or streams, so the home world ticks on exactly as before. Entry k of a spawned world whose
        ext_society is 0 is the home world itself: keep using that World (ValueError here)."""
        k = int(k)
        soc = np.asarray(getattr(self, "ext_society", np.arange(self.n_ext) + 1))
        sid = int(soc[k])
        if sid == 0:
            raise ValueError("neighbour %d is the home world; go back to that World" % k)
        rich = float(self.ext_rich[k])
        cfg = {a: b for a, b in self.cfg.items() if a != "legacy"}
        cfg.update(preset=[float(v) for v in self.ext_V[k][np.argsort(self.perm)]], regime=float(self.ext_regime[k]),
                   tech_level=self.cfg["tech_level"] if rich >= 0.65 else "behind", trace=False)
        start = max(self.t - int(round(years * 52)), 0)
        N = World(self._seed, cfg=cfg, color_perm=self.perm.tolist(), params=dict(self.p), society=sid, start_t=start)
        N.rich = rich
        N.t0 = int(self.t0)
        N.clim_t0 = int(self.clim_t0 if self.clim_t0 is not None else self.t0)
        N._ext_from(self, k)
        N.tick(self.t)
        N.regime = float(self.ext_regime[k]); N._regime_derived()      # the light state at arrival
        N.G = self.ext_G[k].copy()
        N._force_phase(int(self.ext_phase[k]), int(self.ext_rec_q[k]))
        N._ext_from(self, k)
        if self.war and self.war_with == k:              # at war with each other: the front is mirrored
            N.war, N.war_with, N.war_q = 3 - int(self.war), 0, int(self.war_q)
        elif self.ext_war[k]:                            # at war elsewhere (the war that sends refugees)
            if not N.war:
                N.war, N.war_with, N.war_q = 2, -1, 0
        else:
            N.war, N.war_with = 0, -1
        N._derive_econ()
        return N

    def _ext_from(self, home, k):
        """Neighbours seen from a spawned neighbour: home (entry 0, the relation mirrored), then home's others."""
        others = [j for j in range(home.n_ext) if j != k]
        n = 1 + len(others)
        hsoc = np.asarray(getattr(home, "ext_society", np.arange(home.n_ext) + 1))
        self.n_ext = n
        self.ext_society = np.array([home.society_id] + [int(hsoc[j]) for j in others])
        self.ext_regime = np.array([float(home.regime)] + [float(home.ext_regime[j]) for j in others])
        self.ext_V = np.vstack([home.V] + [home.ext_V[j] for j in others])
        self.ext_anchor = np.vstack([home.VPRE] + [home.ext_anchor[j] for j in others])
        self.ext_G = np.vstack([home.G] + [home.ext_G[j] for j in others])
        self.ext_rich = np.array([float(getattr(home, "rich", 1.0))] + [float(home.ext_rich[j]) for j in others])
        reg = self.ext_regime
        rel = np.where((reg >= 6) & (self.regime >= 6), 0, np.where((reg < 0) | (self.regime < 0), 2, 1))
        rel[0] = home.ext_relation[k]
        self.ext_relation = rel.astype(int)
        self.ext_trade = np.array([float(home.ext_trade[k])] + [float(home.ext_trade[j]) for j in others])
        self.ext_phase = np.array([int(home.phase)] + [int(home.ext_phase[j]) for j in others])
        self.ext_rec_q = np.array([int(home.rec_q) if home.phase == 1 else 99] + [int(home.ext_rec_q[j]) for j in others])
        self.ext_exp_q = np.array([int(home.exp_q)] + [int(home.ext_exp_q[j]) for j in others])
        self.ext_war = np.array([int(home.war > 0)] + [int(home.ext_war[j]) for j in others])
        self.ext_next_gov = np.array([max(int(home.next_vote), 1) if home.regime >= 0 else 28]
                                     + [int(home.ext_next_gov[j]) for j in others])
        self.ext_migration = _uclip(0.2 * (1 - self.ext_rich) + 0.6 * self.ext_war + 0.2 * (self.ext_phase == 1), 0, 1)
        self.world_rec, self.world_q = int(home.world_rec), int(home.world_q)
        if self.war_with >= n:
            self.war_with = -1

    def _force_phase(self, ph, rec_q=0):
        """Set the economy's phase to a spawned neighbour's light state (a mild recession starts or the one running ends)."""
        if ph == 1 and self.phase == 0:
            self.phase, self.severity, self.rec_q = 1, 0, int(min(max(rec_q, 0), 3))
            self.rec_len = max(self.rec_q + 2, 3)
            self.u_rise_tgt = self.u_rise + self.p["u_rise"][0]
            self.rec_start_t = int(self.t - 13 * self.rec_q); self.n_rec += 1
            self.cycles.append([self.rec_start_t, -1, 0])
        elif ph == 0 and self.phase == 1:
            self.phase, self.exp_q, self.last_sev = 0, 0, self.severity
            self.rec_end_t = self.t
            self.cycles[-1][1] = int(self.t)
        self._derive_econ()

    def _week(self):
        self.t += 1
        self.week_of_year = self.t % 52
        self.season = int(WEEK_SEASON[self.week_of_year])
        if self.dis_on:                                    # last week's strikes are over
            self.disaster_now[:] = 0; self.disaster_kind[:] = -1; self.dis_on = False
        if self.dis_pending:
            self._strike()
        if self.t % 13 == 0:
            self._quarter()
        if self.t % 52 == 0:
            self._year()

    def _quarter(self):
        self._apply_pushes()
        self._nature_q()
        self._ext_q()
        self._econ_q()
        self._state_q()
        self._inst_q()
        self._place_q()
        self._culture_q()
        self._society_q()
        if (self.p.get("sph_town", False) or self.p.get("sph_haunts", False) or self.p.get("sph_hours", False)
                or self.p.get("sph_events", False) or self.p.get("sph_pairs", False)):
            self._sphere_q()   # (phase 2's haunts and hours read the town spheres, so either switch computes them)
            if self.p.get("sph_haunts", False):
                self._sph_places_q()
        self._figures_q()
        self._history_q()
        if self.trace is not None:
            self._trace()

    def _year(self):
        self._tech_y()
        self._belief_y()
        if self.p.get("c5_faith"):
            self._c5_y()
        self._generations_y()
        self._pop_y()

    # ------------------------------------------------------------------------------------------------ nature (spec 5 §2)
    def _warming_now(self):
        return {"low": 1.1, "middle": 1.2, "high": 1.3}.get(self.climate, 1.2)

    def _warming(self, t):
        """Degrees above pre-industrial. The scenario is anchored at the birth (t0): about 1.2 then, rising ~0.22 a
        decade and slowing as policy bites (middle path, IPCC AR6; Forster et al. 2023); before the birth it rises
        toward that value."""
        w0 = self._warming_now()
        r0, tau = {"low": (0.015, 35.0), "middle": (0.022, 70.0), "high": (0.03, 400.0)}.get(self.climate, (0.022, 70.0))
        y = (t - (self.clim_t0 if self.clim_t0 is not None else self.t0)) / 52.0
        if y >= 0:
            return w0 + r0 * tau * (1 - np.exp(-y / tau))
        return w0 * np.exp(y * r0 / w0)

    @staticmethod
    def _extremes(w):
        """How often extremes come against pre-industrial (flood fire quake storm heat). Hot extremes 2.8x at 1 degree,
        5.6x at 2 (IPCC AR6, 10-year events); heavy rain 1.3x and 1.7x; drought (fire) 1.7x and 2.4x; storms a little
        more; quakes unchanged."""
        return np.array([1 + .25 * w + .05 * w * w, 1 + .6 * w + .05 * w * w, 1.0, 1 + .15 * w + .05 * w * w,
                         1 + 1.3 * w + .5 * w * w])

    def _nature_q(self):
        p, r = self.p, self.R[1]
        x = r.random(8)
        self.warming = float(self._warming(self.t))
        self.extremes = self._extremes(self.warming)
        q_season = WEEK_SEASON[(self.t + 7) % 52]          # season in the middle of the coming quarter
        sf = np.array([[1.2, 1.2, .6, 1.0], [.2, .8, 2.2, .8], [1, 1, 1, 1], [1.5, .6, .6, 1.3], [0, .5, 3.3, .2]])[:, q_season]
        rate = self.loc_hazards * np.array(p["dis_base"]) * self.extremes * sf / 4 * self.pace
        draw = r.random(rate.shape)
        sev = r.random(rate.shape)
        when = r.random(rate.shape)
        hit = draw < rate
        self.loc_disaster = np.maximum(self.loc_disaster - 0.25, 0)
        for l, h in zip(*np.nonzero(hit)):                 # the coming quarter's disasters, each on its own week
            self.dis_pending.append([int(self.t + 1 + int(13 * when[l, h])), int(l), int(h), float(sev[l, h])])
        # price shocks (energy: war and new energy; food: heat and drought)
        eh = p["e_haz"] * (1 + 1.5 * (self.war == 1) + 4 * (self.war == 2) + 1.0 * self.ext_war.any()) * (0.7 if self._has_new("new energy") else 1.0)
        self.energy *= p["e_decay"]; self.food *= p["f_decay"]
        if x[0] < eh:
            self.energy += p["e_size"][0] + (p["e_size"][1] - p["e_size"][0]) * x[1]
            self._event("nature", "price shock", "energy", round(float(self.energy), 1), big=self.energy > 5)
        fh_ = self._c_par("drought_fhaz") if p.get("c4_nature") and getattr(self, "c4_dry", 0) > 0 else 1.0   # C4
        if x[2] < p["f_haz"] * (0.5 + 0.5 * self.extremes[4] / 2.8) * fh_:
            self.food += p["f_size"][0] + (p["f_size"][1] - p["f_size"][0]) * x[3]
            self._event("nature", "price shock", "food", round(float(self.food), 1), big=False)
        # pandemic: none, rising, peak, waning (about 2% a year for a severe one; Marani et al. 2021)
        ph = self.pandemic
        self.pand_q += 1
        if ph == 0 and x[4] < 1 - np.exp(-p["pand_haz"] / 4 * self.pace):
            self.pandemic, self.pand_q = 1, 0; self.pand_n += 1
        elif ph == 1 and self.pand_q >= 1 + (x[5] < 0.5):
            self.pandemic, self.pand_q = 2, 0
        elif ph == 2 and self.pand_q >= 2 + int(x[5] * 3):
            self.pandemic, self.pand_q = 3, 0
        elif ph == 3 and self.pand_q >= 2 + int(x[6] * 3):
            self.pandemic, self.pand_q = 0, 0
        if self.pandemic != ph:
            self._event("nature", "pandemic", PANDEMIC[self.pandemic], None, big=self.pandemic in (1, 2) or ph == 3)
        self.lockdown = 0.35 if self.pandemic == 2 else 0.15 if self.pandemic in (1, 3) else 0.0
        scar = (max(self.energy, 0) + max(self.food, 0)) / 6.0
        lh = np.log(np.maximum((self.loc_hazards * np.array(p["dis_base"]) * self.extremes).sum(1), 1e-4) / self.haz_ref)
        self.harsh_loc = _uclip(0.5 * lh, -1, 1.5) + 0.5 * np.minimum(self.loc_disaster, 1) + np.minimum(scar, 1.5)
        if p.get("c4_nature"):
            self._c4_nature_q(int(q_season))

    # ------------------------------------------------------------------ the C hooks (item 10), built by the Outer world
    # stage3-rules.md section 5. Each is off unless its switch is on; off, it draws nothing and adds nothing to the save.
    def _c_par(self, k):
        return (self.p.get("c_par") or {}).get(k, C_DEFAULT[k])

    def _c_rng(self, k):
        """A fresh generator for this quarter's draws of C hook k: keyed on the seed, the hook and the week, so it keeps
        no state to save and moves no other stream (the hooks' events are chance, so their dice stay: LW2 2e)."""
        return np.random.default_rng([self._seed + 104729, 7000 + int(k), int(self.t)] + ([self.society_id] if self.society_id else []))

    def _c4_nature_q(self, q_season):
        """C4, nature's own year: per place each quarter, a season of bad air (cities, industry), bad water or a poisoned
        river (industry, mining), a dry year (farming and hotter places, drawn in summer), a glorious spring (everywhere,
        drawn in spring) and the recovery after a disaster. Rates are yearly, at the birth's climate, times the pace."""
        nl, t, c = self.n_loc, int(self.t), self._c_par
        if getattr(self, "c4_ill", None) is None:          # made on the first quarter the hook runs, so a world with it off
            self.c4_ill = np.ones(nl)                      # saves nothing of it
            self.c4_ill_to = np.zeros(nl, np.int64)
            self.c4_air_t = np.full(nl, -9999, np.int64)
            self.c4_dis = self.loc_disaster >= 1
            self.c4_dry = 0
        self.c4_dry = max(int(self.c4_dry) - 1, 0)
        x = self._c_rng(4).random((nl, 5))
        ft = lambda f: self.loc_feat[:, FEATURES.index(f)]
        ref = self._extremes(self._warming_now())          # the birth's extremes: the start rates hold there
        hz = self.loc_hazards[:, HAZARDS.index("heat")]
        hot = hz > hz.mean()
        pace = self.pace

        def ill(l, k, weeks):
            on = self.c4_ill_to[l] > t
            self.c4_ill[l] = max(self.c4_ill[l], k) if on else k
            self.c4_ill_to[l] = max(self.c4_ill_to[l], t + weeks)

        heat = 1 + c("air_heat") * (self.extremes[4] / ref[4] - 1)
        air = (ft("city") | ft("industry")) & (t - self.c4_air_t >= 52) & (x[:, 0] < c("air") / 4 * max(heat, 0) * pace)
        for l in np.nonzero(air)[0]:
            self.c4_air_t[l] = t
            ill(l, c("air_ill"), 13)
            self._event("nature", "bad air", None, dict(loc=int(l)), big=False)
        dirty = ft("industry") | ft("mining")
        for l in np.nonzero(dirty)[0]:
            if x[l, 1] < c("river") / 4 * pace:
                kind, k_, w_ = "poisoned river", c("river_ill"), 26
            elif x[l, 1] < (c("river") + c("water")) / 4 * pace:
                kind, k_, w_ = "bad water", c("water_ill"), 13
            else:
                continue
            self.loc_services[l] = np.maximum(self.loc_services[l] - c("water_serv"), 0.05)   # each class's
            ill(l, k_, w_)
            self._event("nature", kind, None, dict(loc=int(l)), big=False)
        if q_season == 2:                                  # the dry year shows in summer
            dry = (ft("farming") | hot) & (x[:, 2] < c("drought") * self.extremes[1] / ref[1] * pace)
            if dry.any():
                share = float(self.loc_pop_share[dry].sum())
                self.food += self.p["f_size"][0] * c("drought_food") * min(1.0, 3 * share)
                self.c4_dry = 2                            # the food shock's chance doubles for this quarter and the next
            for l in np.nonzero(dry)[0]:
                self.loc_services[l] = np.maximum(self.loc_services[l] - c("drought_serv"), 0.05)
                self._event("nature", "drought", None, dict(loc=int(l), farming=bool(ft("farming")[l])), big=False)
        if q_season == 1:                                  # a glorious spring
            for l in np.nonzero(x[:, 3] < c("spring") * pace)[0]:
                self._event("nature", "glorious spring", None, dict(loc=int(l), farming=bool(ft("farming")[l])), big=False)
        hit = self.loc_disaster >= 1                       # a disaster's active years end: the town builds itself back
        for l in np.nonzero(self.c4_dis & ~hit)[0]:
            cn = (self.inst_kind == INST_KINDS.index("council")) & (self.inst_loc == l)
            self.inst_capacity[cn] = np.maximum(self.inst_capacity[cn] - c("rec_cost"), 0.05)
            self._event("nature", "recovery", None, dict(loc=int(l)), big=False)
        self.c4_dis = hit

    def _c5_state(self):
        """C5's own state, made the first year the hook runs (a world with it off saves none of it)."""
        if getattr(self, "c5_prof", None) is None:
            self.c5_prof = np.full((NM, C), 0.2)            # each slot's colours, fixed for the movement's life
            self.c5_on = np.zeros(NM, bool)                 # a living movement holds the slot
            self.c5_born = np.zeros(NM, np.int64)           # the founding week
            self.c5_ceil = np.zeros(NM)                     # the share its growth heads for
            self.c5_fade = np.zeros(NM)                     # years from the founding until a failing one fades (0: it lasts)
            self.c5_parent = np.full(NM, -1, np.int64)      # the tradition it came from (-1: spiritual but secular)
            self.c5_loc = np.full(NM, -1, np.int64)         # the town it was founded in
            self.c5_fig = np.full(NM, -1, np.int64)         # its founder, a public figure
            self.c5_reach = np.ones(NM)                     # its growth scale (a founder's reach, c5_found_by)
            self.c5_tense = np.zeros((NF + NM, NF + NM), bool)   # pairs of faiths in a tense stretch
            self.c5_found_t, self.c5_found_l = -9999, -1    # the last founding: week and town (the founding gate)

    def faith_open(self, min_share=None):
        """Faiths a person can take up: the traditions, and C5's living movements holding min_share of the people
        (default join_share)."""
        nf = self._nf()
        ok = np.arange(nf) < NF
        if nf > NF and getattr(self, "c5_on", None) is not None:
            ms = self._c_par("join_share") if min_share is None else min_share
            ok[NF:] = self.c5_on & (np.asarray(self.faith_share)[NF:] >= ms)
        return ok

    def living_faiths(self):
        """C5's movement slots as the Faith sphere's "living faiths" (read only): each living movement's slot, faith
        index, share of the people, colours (W U B R G), founding week and town, parent tradition and founder."""
        if getattr(self, "c5_prof", None) is None:
            return []
        inv = np.argsort(self.perm)
        return [dict(slot=int(k), faith=NF + int(k), share=round(float(self.faith_share[NF + k]), 4),
                     colours=[round(float(v), 3) for v in self.c5_prof[k][inv]], born=int(self.c5_born[k]),
                     town=int(self.c5_loc[k]), parent=int(self.c5_parent[k]), founder=int(self.c5_fig[k]),
                     lasting=bool(self.c5_fade[k] == 0))
                for k in np.nonzero(self.c5_on)[0]]

    def c5_founding(self, loc):
        """C5's founding gate per person (earth_rules INNER "a following of your own"): a movement founded in the
        person's town within found_open weeks (the founding took a free slot)."""
        loc = np.asarray(loc)
        if getattr(self, "c5_prof", None) is None or self.t - int(self.c5_found_t) >= self._c_par("found_open"):
            return np.zeros(loc.shape, bool)
        return loc == int(self.c5_found_l)

    def c5_found_by(self, pie, reach=1.0):
        """C5: the person founds the movement founded in their town (the option of "a following of your own"): its
        colours become the founder's own and its growth scales with their reach (1 typical). For the Engine to call."""
        if getattr(self, "c5_prof", None) is None or self.t - int(self.c5_found_t) >= self._c_par("found_open"):
            return -1
        k = int(np.argmax(np.where(self.c5_on, self.c5_born, -1)))
        self.c5_prof[k] = _norm(np.asarray(pie, float)); self.c5_reach[k] = float(max(reach, 0.1))
        self.FPROF[NF + k] = self.c5_prof[k]
        return k

    def _c5_move(self, src, dst, amount):
        """Move a share of all the people from faith column src to dst (0 secular, 1.. faiths), group by group in
        proportion to src's own groups; returns the share moved."""
        m = self.pop[..., src, :]
        tot = float(m.sum())
        a = min(float(amount), tot)
        if a <= 0:
            return 0.0
        mv = m * (a / tot)
        self.pop[..., src, :] -= mv; self.pop[..., dst, :] += mv
        return a

    def _c5_y(self):
        """C5, new faith movements (stage3-rules.md section 5): founding, growth, fading, claims and tension, once a
        year after the belief year. Invented movements only; conflict is told indirectly."""
        self._c5_state()
        c, t = self._c_par, int(self.t)
        x = self._c_rng(5).random(16 + 2 * (NF + NM) ** 2)   # 0-7 founding, 8.. claims, 16.. tension
        fs = self.pop.sum((0, 1, 2, 4))                     # 0 secular, 1.. faiths
        # founding
        U = getattr(self, "group_unmet", None)
        free = np.nonzero(~self.c5_on)[0]
        if U is not None and len(free):
            exc = max(float(self.unmet_mean[4] - self.need_base[4]), 0.0)
            pf = c("found") * (1 + c("found_mean") * exc) * (1 + c("found_speed") * float(getattr(self, "norm_speed", 0.0))) * self.pace
            if x[0] < pf:
                k = int(free[0])
                par = int(np.argmax(fs[1:])) if fs[1:].max() >= fs[0] else -1
                pp = self.FPROF[par] if par >= 0 else self.V
                size = self.pop.reshape(-1) * self.gadult
                want = _norm(self.gmix + self.p["zeta"] * (U @ self.NEEDM))
                wm = size * U[:, 4] ** 3
                prof = _norm(0.5 * (wm[:, None] * want).sum(0) / max(wm.sum(), 1e-12) + 0.5 * pp)
                ok = x[2] < c("succeed")
                l = int(min(np.searchsorted(np.cumsum(self.loc_pop_share) / self.loc_pop_share.sum(), x[1]), self.n_loc - 1))
                self.c5_prof[k], self.c5_on[k], self.c5_born[k] = prof, True, t
                self.c5_ceil[k] = (c("ceil_lo") + (c("ceil_hi") - c("ceil_lo")) * x[3]) if ok else (c("fail_lo") + (c("fail_hi") - c("fail_lo")) * x[3])
                self.c5_fade[k] = 0.0 if ok else c("fade_y0") + (c("fade_y1") - c("fade_y0")) * x[4]
                self.c5_parent[k], self.c5_loc[k], self.c5_reach[k] = par, l, 1.0
                self.c5_found_t, self.c5_found_l = t, l
                self.FPROF[NF + k] = prof
                self._c5_move(par + 1, NF + 1 + k, 0.5 * c("seed_share"))
                self._c5_move(0, NF + 1 + k, 0.5 * c("seed_share"))
                # its founder, a public figure outside the roles (no seat to fill; the figure lives on in the record)
                fid = len(self.F_role)
                self.F_role.append(FIG_ROLES.index("preacher")); self.F_pie.append(_norm(prof * np.exp(0.25 * self._cn(self._c_rng(6)))).tolist())
                self.F_standing.append(float(0.1 + 0.1 * x[5])); self.F_alive.append(True); self.F_party.append(-1)
                self.F_born.append(int(t - (30 + 20 * x[6]) * 52)); self.F_female.append(bool(x[7] < 0.5)); self.F_mom.append(0.05)
                self.F_active.append(True); self.F_inst.append(-1)
                self.c5_fig[k] = fid
                self._event("belief", "new movement", None, dict(slot=k, loc=l, parent=par, fig=fid), big=False)
                self.fire_sphere_event("new_teaching", l)  # its sphere event (world-fired: faith.new_teaching)
        # growth, fading, claims, freeing
        fs = self.pop.sum((0, 1, 2, 4))
        for k in np.nonzero(self.c5_on)[0]:
            col, par = NF + 1 + int(k), int(self.c5_parent[k]) + 1
            s_ = float(fs[col]); age = (t - int(self.c5_born[k])) / 52.0
            failing = self.c5_fade[k] > 0
            if failing and age >= self.c5_fade[k]:
                ds = -c("fade") * s_
            else:
                ds = c("grow") * self.c5_reach[k] * s_ * (1 - s_ / self.c5_ceil[k]) * self.pace
            if ds > 0:
                got = self._c5_move(par, col, 0.5 * ds) if par > 0 else 0.0
                self._c5_move(0, col, ds - got)
                if x[8 + k] < c("claims") and age > 0 and s_ < 0.9 * self.c5_ceil[k]:   # while it still grows
                    self._event("belief", "claims spread", None, dict(slot=int(k), loc=int(self.c5_loc[k])), big=False)
            elif ds < 0:
                self._c5_move(col, par, -0.5 * ds); self._c5_move(col, 0, -0.5 * ds)
            s_ = float(self.pop[..., col, :].sum())
            if (s_ < c("free_share") and age >= c("free_y")) or (failing and age >= c("fail_y")):
                self._c5_move(col, par, 0.5 * s_); self._c5_move(col, 0, s_)
                self.pop[..., col, :] = 0.0
                self._event("belief", "movement fades", None, dict(slot=int(k), years=round(age, 1)), big=False)
                self.c5_on[k] = False; self.c5_prof[k] = 0.2; self.FPROF[NF + k] = 0.2
                self.c5_tense[NF + k, :] = False; self.c5_tense[:, NF + k] = False
        self.faith_share = self.pop.sum((0, 1, 2, 4))[1:].copy()
        # tension between two faiths: both over 5%, far apart, trust low; told indirectly, in a town
        sh = self.faith_share
        alive = self.faith_open(0.0)
        big_ = alive & (sh > c("tension_share"))
        cum = np.cumsum(self.loc_pop_share) / self.loc_pop_share.sum()
        nn = (NF + NM) ** 2
        for i in range(NF + NM):
            for j in range(i + 1, NF + NM):
                xr, xl = x[16 + i * (NF + NM) + j], x[16 + nn + i * (NF + NM) + j]
                on = bool(big_[i] and big_[j] and _tv(self.FPROF[i], self.FPROF[j]) > c("tension_tv") and self.trust < c("tension_trust"))
                start = on and not self.c5_tense[i, j]
                self.c5_tense[i, j] = on
                if start or (on and xr < c("tension_p")):
                    l = int(min(np.searchsorted(cum, xl), self.n_loc - 1))
                    self._event("belief", "faith tension", None, dict(faiths=[i, j], loc=l, start=start), big=False)

    # C3's sphere events (spheres-phase3-answers.md section 1; the relay of 10-10 01:00 UTC): a closure averted by the
    # state is the sphere's closure, a leak its exposure; sold and merged are words only. Ordinary closures and scandals
    # are mapped in _sph_wf_key, so only these new events call fire_sphere_event. big as for the world event: a town
    # body's leak stays in its town, a national one's acts for the whole society (fire-big, Engine #78)
    C3_SPH = {"nationalised": {"prod": "works_close", "comm": "lender_fails"},
              "leak": {"rule": "favour_exposed", "care": "neglect_scandal", "faith": "scandal"}}

    def _c3_sph(self, i, kind, big):
        key = self.C3_SPH.get(kind, {}).get(SPHERES[int(self.inst_sphere[i])])
        if key is not None:
            self.fire_sphere_event(key, int(self.inst_loc[i]), big=big)

    def _c3_state(self):
        """C3's own state, made the first quarter the hook runs (a world with it off saves none of it)."""
        if getattr(self, "c3_cover", None) is None:
            self.c3_cover = np.zeros(self.n_inst, np.int64)   # the week a hidden cover-up would surface by itself
            self.c3_break = np.zeros(self.n_inst, bool)       # an insider spoke up this quarter

    def _c3_nationalise(self, close):
        """C3 nationalised: a big firm or bank about to close in a deep recession becomes a public body (half of them,
        where the state's capacity is .5 or more); it then drifts toward the government as public bodies do."""
        self._c3_state()
        c = self._c_par
        deep = self.phase == 1 and self.severity >= 1 and self.capacity >= c("nat_cap")
        if not deep:
            return close
        x = self._c_rng(30).random(self.n_inst)
        nat = close & self.inst_firm & (self.inst_level == 2) & (x < c("nat_share"))
        K_ = {k_: INST_KINDS.index(k_) for k_ in ("employer", "bank")}
        for i in np.nonzero(nat)[0]:
            self.inst_public[i] = True; self.inst_firm[i] = False
            self.inst_pubemp[i] = self.inst_kind[i] == K_["employer"]
            self.inst_finances[i] = 0.5
            self._inst_event(i, "nationalised", big=True)
            self._c3_sph(i, "nationalised", big=True)
        return close & ~nat

    def _c3_inst_q(self, close):
        """C3, institution events (stage3-rules.md section 5): sold, merged, a leak and a cover-up, each quarter at a
        quarter of the yearly start rates. Each is recorded with _inst_event; scandals and closures stay as built, and
        the spheres read them as their own events (spheres-phase3-answers.md, world-fired)."""
        self._c3_state()
        n, t, c = self.n_inst, int(self.t), self._c_par
        r = self._c_rng(3); x = r.random((n, 6)); nz = r.normal(size=(n, C))
        k = self.inst_kind; K_ = {k_: INST_KINDS.index(k_) for k_ in INST_KINDS}
        free = ~close
        ls_ = self.p["lead_spread_s3"] if self._s3("hist_chance_only") else 0.3
        size = self.inst_level * 2.0 + self.inst_capacity                 # who is the bigger of two firms
        # sold: a private firm or bank changes hands; new owners bring their own leader and the sector's big ways
        sold = free & self.inst_firm & (x[:, 0] < c("sold") / 4 * np.where(self.inst_finances < 0.3, c("sold_poor"), 1.0))
        for i in np.nonzero(sold)[0]:
            peers = np.nonzero(self.inst_firm & (self.inst_sector == self.inst_sector[i]) & (np.arange(n) != i))[0]
            if len(peers):
                j = peers[int(np.argmax(size[peers]))]
                self.inst_profile[i] = _norm(self.inst_profile[i] + c("sold_pull") * (self.inst_profile[j] - self.inst_profile[i]))
            if self.inst_leader_fig[i] < 0:
                self.inst_leader_q[i] = 0; self.inst_leader_pie[i] = _norm(self.V * np.exp(ls_ * nz[i]))
            self._inst_event(i, "sold", big=bool(self.inst_level[i] == 2))
        # merged: the smaller of two firms of one sector in one place is folded into the bigger; its slot is a new firm
        emp = free & ~sold & self.inst_firm & (k == K_["employer"])
        done = np.zeros(n, bool)
        for i in np.nonzero(emp & (x[:, 1] < c("merged") / 4))[0]:
            if done[i]:
                continue
            rivals = np.nonzero(emp & ~done & (self.inst_sector == self.inst_sector[i]) & (self.inst_loc == self.inst_loc[i])
                                & (np.arange(n) != i))[0]
            if not len(rivals):
                continue
            j = rivals[int(np.argmax(size[rivals]))]
            small, big = (i, j) if size[i] <= size[j] else (j, i)
            done[[small, big]] = True
            self._event("institution", "merged", INST_KINDS[k[small]], dict(inst=int(small), into=int(big),
                        loc=int(self.inst_loc[small]), gen=int(self.inst_gen[small])), big=False)
            sec = int(self.inst_sector[small]) if self.inst_sector[small] >= 0 else 2
            g = SECTOR_GUILDS[sec][int(x[small, 5] * len(SECTOR_GUILDS[sec]))]
            self.inst_native[small] = self._profile_src(g); self.inst_profile[small] = self.inst_native[small].copy()
            self.inst_finances[small], self.inst_age[small], self.inst_gen[small] = 0.5, 0.0, self.inst_gen[small] + 1
            self.inst_corruption[small], self.inst_legitimacy[small], self.inst_leader_q[small] = 0.1, self.inst_legit0[small], 0
            self.inst_leader_pie[small] = _norm(self.V * np.exp(ls_ * nz[small]))
            self._inst_event(small, "new firm", big=False)
        # a leak: private files get out, more where nearly everyone is online and the body is weak
        net = float(self.tech_adopt("internet")) if "internet" in self.tech_keys else 0.0
        lk_k = np.isin(k, [K_[k_] for k_ in ("hospital", "council", "ministry")]) | self.inst_firm
        leak = free & lk_k & (x[:, 2] < c("leak") / 4 * (0.5 + net) * np.maximum(1.5 - self.inst_capacity, 0))
        for i in np.nonzero(leak)[0]:
            self.inst_legitimacy[i] = max(self.inst_legitimacy[i] - c("leak_legit"), 0.02)
            self.trust = max(self.trust - c("leak_trust"), 0.02)
            big = bool(self.inst_level[i] == 2)
            self._inst_event(i, "leak", big=big)
            self._c3_sph(i, "leak", big=big)
        # a cover-up: money, safety checks, records or negligence (never harm to children or sexual violence); hidden,
        # it is not on the record; its staff know
        cv_k = np.isin(k, [K_[k_] for k_ in ("hospital", "bank", "council", "police", "faith body")])
        cov = free & cv_k & (self.c3_cover <= t) & (x[:, 3] < (c("cover") + c("cover_c") * self.inst_corruption) / 4)
        for i in np.nonzero(cov)[0]:
            yrs = c("cover_y0") + (c("cover_y1") - c("cover_y0")) * x[i, 4]
            self.c3_cover[i] = t + int(52 * yrs)
            subj = ("money", "safety checks", "records", "negligence")[int(x[i, 5] * 4) % 4]
            self._event("institution", "cover-up", INST_KINDS[k[i]], dict(inst=int(i), loc=int(self.inst_loc[i]),
                        gen=int(self.inst_gen[i]), subject=subj), big=False, public=False)

    def c4_illness(self):
        """C4: each place's multiplier on illness (bad air, bad water, a poisoned river), or None with the hook off."""
        if getattr(self, "c4_ill", None) is None:
            return None
        return np.where(self.c4_ill_to > self.t, self.c4_ill, 1.0)

    def _strike(self):
        """Disasters drawn for this week strike: the locality's recovery, its services, the record, disaster_now."""
        due = [d for d in self.dis_pending if d[0] <= self.t]
        if not due:
            return
        self.dis_pending = [d for d in self.dis_pending if d[0] > self.t]
        for _, l, h, sv in due:
            self.loc_disaster[l] = max(self.loc_disaster[l], 1.0 + 2.0 * sv)
            self.loc_services[l] *= 1 - 0.1 * sv
            if max(sv, 0.01) > self.disaster_now[l]:
                self.disaster_now[l], self.disaster_kind[l] = max(sv, 0.01), h
            self._event("nature", "disaster", HAZARDS[h], dict(loc=int(l), severity=round(float(sv), 2)), big=bool(sv > 0.9))
        self.dis_on = True

    # ------------------------------------------------------------------------------------------------ abroad (spec 5 §5)
    def _ext_q(self):
        p, r = self.p, self.R[2]
        n = self.n_ext
        x = r.random((n, 10)); xw = r.random(6); nz = self._cn(r, n)
        # world cycle: a global recession about once a decade, lasting about 3 quarters (estimate)
        if self.world_rec:
            self.world_q += 1
            if xw[0] < 0.35: self.world_rec = 0
        elif xw[0] < 0.025 * self.pace:
            self.world_rec, self.world_q = 1, 0
            self._event("abroad", "world recession", None, None, big=False)
        # neighbours' cycles: own hazard, the world, contagion from home along trade
        home_hit = float(self.phase == 1 and self.rec_q <= 2)
        haz = (0.02 + 0.004 * self.ext_exp_q / 4 + 0.08 * self.world_rec + 0.3 * self.ext_trade * home_hit) * self.pace
        rec = self.ext_phase == 1
        start = ~rec & (x[:, 0] < haz)
        end = rec & (x[:, 1] < 1 / 3.5) & (self.ext_rec_q >= 2)
        self.ext_phase = np.where(start, 1, np.where(end, 0, self.ext_phase))
        self.ext_rec_q = np.where(start, 0, self.ext_rec_q + 1)
        self.ext_exp_q = np.where(self.ext_phase == 0, self.ext_exp_q + 1, 0)
        lag = (self.ext_rec_q >= 1) & (self.ext_rec_q <= 3)
        self.trade_hit = float((self.ext_trade * lag).sum())
        # governments and value climates
        ch = self.ext_next_gov <= 0
        self.ext_G = np.where(ch[:, None], _norm(self.ext_V * np.exp(0.3 * nz)), self.ext_G)
        self.ext_next_gov = np.where(ch, 28 + (x[:, 2] * 16).astype(int), self.ext_next_gov - 1)
        self.ext_V = _norm(self.ext_V + 0.02 * (self.ext_anchor - self.ext_V) + 0.002 * nz)
        # regimes: mixed regimes are the least stable (Hegre et al. 2001)
        mixed = np.abs(self.ext_regime) < 6
        flip = mixed & (x[:, 3] < 0.01)
        self.ext_regime = np.where(flip, np.where(x[:, 4] < 0.5, x[:, 5] * 4 + 6, -6 - x[:, 5] * 4), self.ext_regime)
        # relations drift toward what the regimes and crises make likely (estimate)
        dem = (self.ext_regime >= 6) & (self.regime >= 6)
        closed = (self.ext_regime < 0) | (self.regime < 0)
        tgt = np.where(dem, 0, np.where(closed, 2 + (self.ext_phase == 1), 1))
        mv = x[:, 6] < 0.03
        self.ext_relation = _uclip(self.ext_relation + np.where(mv, np.sign(tgt - self.ext_relation), 0), 0, 3).astype(int)
        # neighbours' own wars (refugees)
        ew = self.ext_war == 1
        self.ext_war = np.where(ew, (x[:, 7] > 0.08).astype(int), (x[:, 7] < 0.0015 * (1 + 3 * (self.ext_regime < 6)) * self.pace).astype(int))
        for j in np.nonzero((self.ext_war == 1) & ~ew)[0]:
            self._event("abroad", "war abroad", None, dict(society=int(j)), big=False)
        # home's war (spec 1 §3; R7: rare and abroad by default in a rich democracy)
        if self.war == 0:
            dp = np.where((self.ext_regime >= 6) & (self.regime >= 6), p["war_dem"], 1.0)
            cf = 1 + (self.phase == 1) * (self.severity + 1) * 0.5 + (self.ext_phase == 1) + 2 * (self.since_break < 8) * (self.regime < 6)
            hz = np.array(p["war_rel"])[self.ext_relation] * dp * cf * self.pace
            hit = np.nonzero(x[:, 8] < hz)[0]
            if len(hit):
                j = int(hit[0])
                home = (self.ext_relation[j] == 3) and (self.ext_regime[j] < 6) and xw[1] < p["war_home_p"]
                self.war, self.war_with, self.war_q = (2 if home else 1), j, 0
            elif xw[2] < p["war_abroad"] * self.pace * (1 + self.ext_war.any()):
                self.war, self.war_with, self.war_q = 1, -1, 0
            if self.war and self.war_with >= 0:
                self.ext_relation[self.war_with] = 3
            if self.war:
                self._event("abroad", "war begins", WAR_STATES[self.war], dict(society=self.war_with), big=True)
        else:
            self.war_q += 1
            if xw[3] < (0.05 if self.war == 1 else 0.08):
                lost = bool(xw[4] < 0.4)
                self._event("abroad", "war ends", WAR_STATES[self.war], dict(society=self.war_with, lost=lost), big=True)
                if lost: self.lost_war_q = 8
                self.war, self.war_with = 0, -1
            elif self.war == 1 and self.war_with >= 0 and xw[5] < 0.01:
                self.war = 2
                self._event("abroad", "war comes home", None, dict(society=self.war_with), big=True)
        self.lost_war_q = max(self.lost_war_q - 1, 0)
        # migration push: neighbours at war or poor, the home economy pulling
        self.ext_migration = _uclip(0.2 * (1 - self.ext_rich) + 0.6 * self.ext_war + 0.2 * (self.ext_phase == 1), 0, 1)

    # ------------------------------------------------------------------------------------------------ economy (spec 1 §2)
    def _econ_q(self):
        p, r = self.p, self.R[3]
        x = r.random(8)
        self.gap_prev, self.unemp_prev = self.gap, self.unemp
        self.house_hist = np.roll(self.house_hist, 1); self.house_hist[0] = self.housing
        if self.phase == 0:
            self.exp_q += 1
            yrs = self.exp_q / 4
            h = (p["h0"] + p["h_age"] * yrs + p["h_imb"] * max(self.housing, 0) + p["h_trade"] * self.trade_hit
                 + p["h_world"] * self.world_rec + p["h_shock"] * max(self.energy, 0) / 5
                 + 0.4 * (self.pandemic == 2) + 0.15 * (self.war == 2))
            if x[0] < 1 - np.exp(-h * self.pace):
                boom = _cl(self.house_hist.max(), 0, 1)
                pr = np.array(p["sev_p"], float)
                pr[2] *= (1 + p["crisis_boom"] * boom) * self.pace
                if self.pandemic == 2 or self.war == 2: pr[0] *= 0.2
                pr /= pr.sum()
                sev = int((x[1] > np.cumsum(pr)).sum())
                self.phase, self.severity, self.rec_q = 1, min(sev, 2), 0
                self.rec_len = 2 + int(-np.log(max(x[2], 1e-9)) * (p["rec_len"][self.severity] - 2))
                self.u_rise_tgt = self.u_rise + p["u_rise"][self.severity] * (0.7 + 0.6 * x[3])
                self.rec_start_t = self.t; self.n_rec += 1
                self.cycles.append([int(self.t), -1, int(self.severity)])
        else:
            self.rec_q += 1
            if self.rec_q >= self.rec_len:
                self.phase, self.exp_q, self.last_sev = 0, 0, self.severity
                self.rec_end_t = self.t
                self.cycles[-1][1] = int(self.t)
        # output gap
        if self.phase == 1:
            self.gap += 0.5 * (p["gap_floor"][self.severity] - self.gap)
        else:
            tgt = p["gap_boom"] * (1 - np.exp(-self.exp_q / 4 / p["gap_tau"]))
            self.gap += p["gap_rec"][self.last_sev] * (tgt - self.gap)
        self.gap += 0.02 * r.normal() - 0.05 * max(self.energy, 0) / 5
        self.gap = _cl(self.gap, -1, 1)
        self.gap_ema += 0.01 * (self.gap - self.gap_ema)
        # unemployment: natural + a rise that decays with a half-life of about 2 years (spec 1 §2)
        if self.phase == 1:
            self.u_rise += 0.45 * (self.u_rise_tgt - self.u_rise)
        else:
            self.u_rise *= 0.5 ** (1 / p["u_half"][self.last_sev])
        self.u_noise = 0.6 * self.u_noise + 0.12 * r.normal()
        auto = float((self.automation * self._sectors()).sum())
        self.unemp = _cl(self.natural + self.u_rise + self.u_noise + 4 * max(auto - 0.15, 0) + 3 * (self.war == 2), 1.5, 30)
        # inflation: 2% baseline, demand, price shocks, war and pandemic (spec 1 §2)
        self.infl_e = 0.7 * self.infl_e + 0.3 * r.normal()
        self.infl = _cl(p["infl0"] + p["infl_gap"] * self.gap + self.energy + self.food + 2.5 * (self.war == 2)
                                  + 0.8 * (self.pandemic == 3) + 1.2 * max(self.housing, 0) + self.infl_e, -2, 15)
        # housing: momentum with mean reversion; recessions knock it down, crises hard
        self.house_m = 0.85 * self.house_m - 0.03 * self.housing + 0.02 * self.gap + 0.022 * r.normal()
        if self.phase == 1: self.house_m -= (0.01, 0.03, 0.08)[self.severity]
        self.housing = _cl(self.housing + self.house_m, -1, 1)
        # inequality drifts with automation, welfare and crises
        self.ineq = _cl(self.ineq + 0.01 * (p["ineq0"] - self.ineq) + 0.002 * (auto - 0.15) * 10
                                  - 0.002 * (self.welfare - p["welfare0"]) * 10 + 0.003 * (self.phase == 1) * (self.severity == 2)
                                  + 0.002 * r.normal(), 0.15, 0.6)
        # what pays off (spec 1 §2, spec 6 §2): centred on the cycle so it favours no color over time
        s = self.gap - self.gap_ema
        pos = getattr(self, "Pos", np.full(C, 0.2))
        self.payoff = _norm(0.2 + p["pay_pos"] * s * (pos - 0.2) + p["pay_ent"] * s * self.DENT * 0.2)
        self._derive_econ()

    def _sectors(self):
        """National sector shares (farm industry services knowledge public): population-weighted localities."""
        return (self.loc_pop_share[:, None] * self.loc_sectors).sum(0)

    def _derive_econ(self):
        p = self.p
        sh = self._sectors()
        cyc = np.array([0.9, 1.5, 1.0, 0.6, 0.3])           # how far each sector rides the cycle (estimate)
        stru = np.array([1.2, 1.1, 1.0, 0.65, 0.6])          # structural unemployment by sector (estimate)
        u_s = self.natural * stru / (sh * stru).sum() + (self.unemp - self.natural) * cyc / (sh * cyc).sum() \
            + 6 * np.maximum(self.automation - 0.15, 0)
        u_s *= self.unemp / max((sh * u_s).sum(), 1e-6)
        self.unemp_sector = _uclip(u_s, 0.5, 40)
        self.nat_sector = self.natural * stru / (sh * stru).sum()
        lu = (self.loc_sectors * self.unemp_sector).sum(1) * self.loc_ufac
        lu *= self.unemp / max((self.loc_pop_share * lu).sum(), 1e-6)
        self.loc_unemp = self.unemp_loc = _uclip(lu, 0.5, 45)
        self.prosper = self.gap
        self.phase_key = PHASES[self.phase]

    # ------------------------------------------------------------------------------------------------ state (spec 1 §3)
    def _state_q(self):
        p, r = self.p, self.R[4]
        x = r.random(8); xl = r.random(NL); nz = self._cn(r)
        d = _tv(self.G, self.Dem)
        sn_ = r.normal()
        if self._s3("hist_chance_only"):                   # LW2 2e: support follows the record, not dice
            sn_ = 0.0
        self.support += (-p["rule_cost"] / 4 + p["ev_gap"] * (self.gap - self.gap_prev) - p["ev_u"] * (self.unemp - self.unemp_prev)
                         - p["ev_infl"] * max(self.infl - 4, 0) - p["th_sup"] * 0.25 * max(d - 0.05, 0)
                         + 0.03 * (0.5 - self.support) * 0.25 + p["s_noise"] * sn_)
        self.support = _cl(self.support, 0.05, 0.95)
        self.gov_q += 1
        self.next_vote -= 1
        if self.next_vote <= 0 and self.regime >= 0:
            self._election(x, nz)
        elif self.regime < 0 and (self.Q > 0.5 * getattr(self, "q_thr", 1e9) if self._s3("hist_chance_only") else x[5] < 0.01):
            self.G = _norm(self.G + 0.1 * (self.Dem - self.G))   # closed regimes reshuffle rarely (2e: when pressure builds)
        # the law book (spec 1 §3): the support a law has (the norm, the government's fit with the law's colors, pushes
        # that count for more where the norms agree) points to a state; the law moves one step toward it with a small
        # chance each quarter, so laws trail norms by years
        n = _sig(self.norm_x[:NL])
        fit = (self.G - 0.2) @ self.NPROF[:NL].T
        neff = n + p["law_fit"] * fit + 0.12 * self.law_push * (n / 0.5) ** 2
        neff[LI["conscription"]] += 0.5 * (self.war == 2) + 0.15 * (self.war == 1)
        tgt = np.where(neff > p["law_cut"][1], 0, np.where(neff > p["law_cut"][0], 1, 2))
        margin = np.where(tgt < self.laws, neff - np.where(self.laws == 2, p["law_cut"][0], p["law_cut"][1]),
                          np.where(self.laws == 0, p["law_cut"][1], p["law_cut"][0]) - neff)
        hz = p["law_h"] * (1 + 10 * np.maximum(margin, 0)) * (p["law_open"] if self.open_q > 0 else 1.0) + 0.3 * (self.law_push > 0.5)
        mv = (tgt != self.laws) & (xl < hz)
        self.law_push *= 0.5
        self.law_since += 0.25
        for k in np.nonzero(mv)[0]:
            self._set_law(k, self.laws[k] + int(np.sign(tgt[k] - self.laws[k])))
        # welfare: a law-book entry that moves with government and with unmet safety (spec 1 §3)
        wt = p["welfare0"] + 3.0 * float((self.G - 0.2) @ self.WPROF) + 0.5 * (self.unmet_mean[0] - self.need_base[0] if hasattr(self, "unmet_mean") else 0)
        self.welfare = _cl(self.welfare + 0.02 * (wt - self.welfare) * (2 if self.open_q > 0 else 1), 0.05, 0.95)
        if abs(self.welfare - self.welfare_pub) >= 0.05:
            self._event("state", "welfare raised" if self.welfare > self.welfare_pub else "welfare cut", "welfare", round(self.welfare, 2), big=False)
            self.welfare_pub = round(self.welfare, 2)
        # rights (spec 1 §3): from the regime, the matching norms and laws, lockdowns
        nr = _sig(self.norm_x)
        tgt = self.rights_base * np.array([1.0, 0.85 + 0.15 * nr[NI["faith in public"]], 1.0 - self.lockdown,
                                           0.25 + 0.75 * np.mean([nr[NI["coming out"]], nr[NI["transition"]], (2 - self.laws[LI["same-sex marriage"]]) / 2]),
                                           0.35 + 0.65 * nr[NI["role crossing"]]])
        old = self.rights.copy()
        self.rights = _uclip(self.rights + 0.06 * (tgt - self.rights), 0, 1)
        self.rights[2] = min(self.rights[2], 1.0 - self.lockdown)
        for k in np.nonzero(np.floor(self.rights * 10) != np.floor(old * 10))[0]:
            self._event("state", "right gained" if self.rights[k] > old[k] else "right lost", RIGHTS[k], round(float(self.rights[k]), 1), big=False)
        # unrest (spec 1 §3): unemployment above natural, inequality, the gap between government and demand, repression
        rep = (1 - self.rights.mean()) * (self.regime < 6)
        ut = (0.25 * max(self.unemp - self.natural, 0) / 5 + 0.6 * max(self.ineq - 0.3, 0) + 1.5 * max(d - 0.08, 0)
              + 0.3 * rep + 0.4 * (self.war == 2) + 0.1 * (self.pandemic == 2) + 0.2 * (self.severity == 2) * (self.phase == 1)
              + 0.3 * self.lost_war_q / 8 + 0.15 * max(self.infl - 6, 0) / 6)
        self.unrest = _cl(self.unrest + 0.3 * (ut - self.unrest) + 0.01 * r.normal(), 0, 1)
        self._regime_derived()

    def _election(self, x, nz):
        p = self.p
        res = self.support + p["e_noise"] * (2 * x[0] - 1) * 1.7
        turnout = _cl(0.66 - 0.15 * (self.polar - 0.1) * 0 + 0.1 * (self.trust - 0.45) + 0.03 * (2 * x[1] - 1), 0.3, 0.9)
        if res < 0.5 and self._s3("hist_party_gov"):    # LW2 2a: the party closest to demand governs in its own colours,
            d = np.array([_tv(self.inst_profile[i], self.Dem) for i in self.party_ids])   # moved toward its voters, with
            d[self.gov_party] = 9                                                         # its leader's touch
            old = self.gov_party
            self._change_gov(int(np.argmin(d)), x[3])
            Pw = self.inst_profile[self.party_ids[self.gov_party]]
            fid = self.fig_role_now.get(0)
            L = np.asarray(self.F_pie[fid], float) if fid is not None and fid >= 0 else Pw
            self.G = _norm(Pw + p["gov_voter"] * (self.Dem - Pw) + p["lead_k"] * (L - Pw))
            self.s3_loser = (int(old), 4)
        elif res < 0.5:
            Gn = _norm(self.Dem + p["k_thermo"] * (self.Dem - self.G))
            self.G = _norm(Gn * np.exp(p["g_noise"] * nz))
            d = np.array([_tv(self.inst_profile[i], self.G) for i in self.party_ids])
            d[self.gov_party] = 9
            old = self.gov_party
            self._change_gov(int(np.argmin(d)), x[3])
            pid = self.party_ids[self.gov_party]
            self.inst_profile[pid] = 0.5 * self.inst_profile[pid] + 0.5 * self.G
        if res < 0.5:
            self.support = p["s_win"] + 0.02 * (2 * x[2] - 1)
            self._event("state", "election", "change", dict(party=self.gov_party, leader=self.fig, colors=self.G.round(2).tolist(),
                                                              support=round(float(res), 2), turnout=round(turnout, 2)), big=True)
        else:
            self.G = _norm(self.G + 0.2 * (self.Dem - self.G))
            self.support = float(0.5 + 0.5 * (res - 0.5) + 0.04)
            self._event("state", "election", "held", dict(party=self.gov_party, leader=self.fig, colors=self.G.round(2).tolist(),
                                                            support=round(float(res), 2), turnout=round(turnout, 2)), big=False)
        self.next_vote = 16 + int(x[3] * 5)

    def _change_gov(self, new, xv):
        """The governing party changes: the opposition leader of the new party becomes head of government, the old
        head leads the opposition; a new term starts."""
        old = self.gov_party
        self.gov_party, self.opp_party = new, old
        self.gov_q, self.u_at_office = 0, self.unemp
        self.n_gov_change = getattr(self, "n_gov_change", 0) + 1
        head_old, opp_old = self.fig_role_now.get(0), self.fig_role_now.get(1)
        if opp_old is not None and self.F_alive[opp_old] and self.F_party[opp_old] == new:
            self.F_standing[opp_old] = min(1.0, self.F_standing[opp_old] + 0.2)
            self.fig_role_now.pop(1, None)
            self._set_role(0, opp_old)
        else:
            self._new_fig(self.R[9], 0, quiet=True, party=new)
        if head_old is not None and self.F_alive[head_old]:
            self.F_party[head_old] = old
            self._set_role(1, head_old)
        else:
            self._new_fig(self.R[9], 1, quiet=True, party=old)
        self.next_vote = 16 + int(xv * 5)
        self.Q *= self.p["q_vote"]                         # the change people voted for releases pressure, and the new
        self.mandate_q = int(self.p["mandate_q"])          # order's distance from demand is its mandate for a while
        self._event("state", "government falls", None, dict(party=old), big=True)

    def _set_law(self, k, s):
        s = int(_uclip(s, 0, 2))
        if s == self.laws[k]:
            return
        old = self.laws[k]
        self.laws[k] = s
        self.law_since[k] = 0
        self._event("state", "law changed", LAW_KEYS[k], dict(state=LAW_STATES[s], was=LAW_STATES[old]), big=s != 1)

    # ------------------------------------------------------------------------------------------------ institutions (spec 4)
    def _inst_q(self):
        p, r = self.p, self.R[5]
        n = self.n_inst
        x = r.random((n, 8)); nz = self._cn(r, n)
        k = self.inst_kind
        pub = self.inst_public
        self.inst_age += 0.25
        # leaders: tenure about 6 years; public bodies' leaders are appointed by the government
        self.inst_leader_q += 1
        newl = (x[:, 0] < 1 / p["tenure_q"]) & (self.inst_leader_fig < 0)
        self.tenure_sum = getattr(self, "tenure_sum", 0.0) + float(self.inst_leader_q[newl].sum())   # hidden, for tests
        self.tenure_n = getattr(self, "tenure_n", 0) + int(newl.sum())
        base = np.where(pub[:, None], self.G, self.V)
        ls_ = p["lead_spread_s3"] if self._s3("hist_chance_only") else 0.3   # LW2 2e: who leads is chance, their colours
        self.inst_leader_pie = np.where(newl[:, None], _norm(base * np.exp(ls_ * nz)), self.inst_leader_pie)   # less so
        self.inst_leader_q = np.where(newl, 0, self.inst_leader_q)
        for i in np.nonzero(newl & (self.inst_level == 2))[0]:          # local routine changes stay off the record
            self._inst_event(i, "new leader")
        # profile drift: leader, mission, routine (toward White), oligarchy (toward Black), spec 4 §3
        prof = self.inst_profile
        party = k == INST_KINDS.index("party")
        if p.get("inst_even", False):    # colour-even: routine keeps the body's own past, oligarchy its leaders' colours
            if getattr(self, "inst_H", None) is None:   # the body's own past: a 25-year memory of its profile (H_mem)
                self.inst_H = prof.copy()
            rout_, olig_ = self.inst_H, self.inst_leader_pie
        else:
            rout_, olig_ = self.ROUT, self.OLIG
        dp = (p["inst_lead"] * (self.inst_leader_pie - prof) + p["inst_mission"] * (self.inst_native - prof)
              + p["inst_routine"] * np.minimum(self.inst_age, 100)[:, None] / 50 * (rout_ - prof)
              + p["inst_olig"] * self.inst_corruption[:, None] * (olig_ - prof))
        fb = self.inst_faith >= 0
        dp[fb] = 0.02 * (self.FPROF[self.inst_faith[fb]] - prof[fb])
        dp[party] = 0
        self.inst_profile = _norm(prof + dp)
        if p.get("inst_even", False):
            self.inst_H += self._sph_tables()["pr"]["H_mem"] * (self.inst_profile - self.inst_H)
        # capacity follows funding: the state budget, the market, members (spec 4 §3)
        budget = 0.6 + 0.4 * (self.welfare - self.p["welfare0"]) + 0.15 * self.gap
        ct = np.where(pub, self.capacity * (0.75 + 0.4 * budget), 0.45 + 0.45 * self.inst_finances)
        ct = np.where(fb, 0.4 + 0.8 * self.faith_share[np.maximum(self.inst_faith, 0)], ct)
        self.inst_capacity = _uclip(self.inst_capacity + 0.05 * (ct - self.inst_capacity) + 0.01 * r.normal(size=n), .05, 1)
        # corruption rises where oversight is weak and leaders entrench; falls with reform
        cterm = 0.12 * (1.9 - self.law_rule) / 1.0 * (1 + 0.3 * np.minimum(self.inst_leader_q / 24, 2))
        self.inst_corruption = _uclip(self.inst_corruption + 0.02 * (cterm * 0.85 - self.inst_corruption) + 0.006 * r.normal(size=n), .01, .9)
        self._state_corruption()
        # legitimacy follows performance, scandals, the media's mood and trust (OECD trust targets by kind)
        lt = self.inst_legit0 * (1 + 0.6 * (self.inst_capacity - 0.84)) * (1 - 0.8 * (self.inst_corruption - 0.14)) \
            * (0.45 + 0.55 * self.trust / self.p["trust0"] - 0.3 * (self.fear - self.p["fear0"]))
        gov = (k == INST_KINDS.index("ministry"))
        lt = np.where(gov, lt * (0.55 + 0.8 * (self.support - 0.5) + 0.45), lt)
        self.inst_legitimacy = _uclip(self.inst_legitimacy + 0.06 * (lt - self.inst_legitimacy), .02, .98)
        # openness by class and migrant status (R9): corruption favours insiders, trust and rights open doors
        oc = np.array([.78, .92, 1.0]) - np.array([.6, .2, 0.0])[None, :] * (self.inst_corruption[:, None] - 0.12) \
            - np.array([.4, .1, 0])[None, :] * (self.ineq - 0.32)
        self.inst_open_cls += 0.05 * (_uclip(oc, .2, 1) - self.inst_open_cls)
        om = 0.70 + 0.25 * (self.trust - 0.45) + 0.2 * (self.rights[0] - 0.85) - 0.3 * max(self.mig_in - 0.01, 0) * 20
        self.inst_open_mig += 0.05 * (_uclip(om, .3, 1) - self.inst_open_mig)
        self._openness()
        # firms live and die with the economy (business demography: 8-10% exit a year); public employers follow the
        # state's budget (welfare level and the public share), not the cycle (spec 1 §2)
        firm, pube = self.inst_firm, self.inst_pubemp
        cyc = np.array([0.9, 1.5, 1.0, 0.6, 0.3])[np.maximum(self.inst_sector, 0)]
        ftgt = np.where(pube, 0.5 + 1.2 * (self.welfare - p["welfare0"]), 0.5 + 0.5 * cyc * self.gap)
        self.inst_finances = _uclip(self.inst_finances + 0.15 * (ftgt - self.inst_finances)
                                     - 0.05 * self.automation[np.maximum(self.inst_sector, 0)] * firm + 0.05 * r.normal(size=n), -0.5, 1)
        ex = p["firm_exit"] * np.exp(-3 * (self.inst_finances - 0.5)) * np.where(self.inst_level == 2, p["firm_big"], 1.0)
        ex = np.where(pube, p["pub_exit"] * np.exp(-3 * (self.inst_finances - 0.5)), ex)
        close = (firm | pube) & (x[:, 1] < ex)
        # events: scandal, new leader, strike, budget cut, ruling, reform, closure (spec 4 §4)
        media_cap = self.inst_capacity[k == INST_KINDS.index("media")].mean()
        sc_ = p["scandal0"] + p["scandal_c"] * self.inst_corruption * media_cap * (0.5 + self.watch)
        if p.get("c3_inst") and getattr(self, "c3_cover", None) is not None:   # C3: a cover-up hides it, so it breaks
            hid_ = self.c3_cover > self.t                                      # three times as often, and at once
            sc_ = np.where(hid_, sc_ * self._c_par("cover_sc"), sc_)           # when an insider speaks up
            sc = ((x[:, 2] < sc_) | (hid_ & self.c3_break)) & ~party
            self.c3_cover = np.where(sc, 0, self.c3_cover); self.c3_break[:] = False
        else:
            sc = (x[:, 2] < sc_) & ~party
        for i in np.nonzero(sc)[0]:
            self.inst_legitimacy[i] -= 0.12; self.trust -= 0.002
            big = self.inst_level[i] == 2
            self._inst_event(i, "scandal", big=bool(big))
            if x[i, 3] < 0.5 and self.inst_leader_fig[i] < 0:
                self.inst_leader_q[i] = 0; self.inst_leader_pie[i] = _norm(base[i] * np.exp(ls_ * nz[i]))
                self._inst_event(i, "new leader")
            if self.inst_leader_fig[i] >= 0:
                self._fig_scandal(self.inst_leader_fig[i])
        ref = (self.inst_legitimacy < 0.22) & (x[:, 4] < 0.08)
        for i in np.nonzero(ref)[0]:
            self._reform_inst(i, self.inst_native[i])
        union = k == INST_KINDS.index("union")
        st = union & (x[:, 5] < 0.012 + 0.05 * max(self.infl - 3, 0) / 5 + 0.03 * (self.welfare < self.welfare_pub - 0.02))
        for i in np.nonzero(st)[0]:
            self._inst_event(i, "strike", big=self.infl > 6)
        if self.phase == 1 and self.rec_q == 3 and x[0, 6] < 0.6:
            cut = pub & (x[:, 6] < 0.25)
            self.inst_capacity[cut] *= 0.93
            self._event("institution", "budget cut", None, dict(n=int(cut.sum())), big=False)
        court = k == INST_KINDS.index("court")
        for i in np.nonzero(court & (x[:, 6] > 0.985))[0]:
            j = int(x[i, 0] * NL) % NL
            if _sig(self.norm_x[j]) > 0.55 and self.laws[j] > 0:
                self.law_push[j] += 0.6
            self._inst_event(i, "ruling", big=self.inst_level[i] == 2)
        if p.get("c3_inst"):                               # C3: some big closures in a deep recession are nationalised
            close = self._c3_nationalise(close)
        for i in np.nonzero(close)[0]:
            self._inst_event(i, "closure", big=self.inst_level[i] == 2)
            sec = int(self.inst_sector[i]) if self.inst_sector[i] >= 0 else 2
            g = SECTOR_GUILDS[sec][int(x[i, 7] * len(SECTOR_GUILDS[sec]))]
            self.inst_native[i] = self._profile_src(g); self.inst_profile[i] = self.inst_native[i].copy()
            if getattr(self, "inst_H", None) is not None:   # inst_even: a new body has no past but its founding
                self.inst_H[i] = self.inst_native[i].copy()
            self.inst_finances[i], self.inst_age[i], self.inst_gen[i] = 0.5, 0.0, self.inst_gen[i] + 1
            self.inst_corruption[i], self.inst_legitimacy[i], self.inst_leader_q[i] = 0.1, self.inst_legit0[i], 0
            self.inst_leader_pie[i] = _norm(self.V * np.exp(ls_ * nz[i]))
            self._inst_event(i, "new firm", big=False)
        self.n_closures = getattr(self, "n_closures", 0) + int(close.sum())
        if p.get("c3_inst"):
            self._c3_inst_q(close)

    def _inst_event(self, i, kind, big=False):
        self._event("institution", kind, INST_KINDS[self.inst_kind[i]], dict(inst=int(i), loc=int(self.inst_loc[i]),
                                                                          gen=int(self.inst_gen[i])), big=big)

    def _reform_inst(self, i, toward, step=0.4):
        self.inst_corruption[i] *= 0.5
        self.inst_profile[i] = _norm(self.inst_profile[i] + step * (toward - self.inst_profile[i]))
        self.inst_legitimacy[i] = min(0.95, self.inst_legitimacy[i] + 0.1)
        self._inst_event(i, "reform")

    # ------------------------------------------------------------------------------------------------ places (spec 3 §2)
    def _place_q(self):
        p, r = self.p, self.R[6]
        nl = self.n_loc
        x = r.random((nl, 3)); nz = self._cn(r, nl)
        self._derive_econ()
        # crime follows local unemployment, inequality and efficacy, with a lag (Sampson et al. 1997)
        nbl = self.nb_loc.astype(np.intp, copy=False)
        eff = np.bincount(nbl, self.nb_efficacy, nl) / np.bincount(nbl, None, nl)
        ct = self.loc_crime0 * (1 + 0.08 * (self.loc_unemp - self.natural * self.loc_ufac)) * (1 + 2.0 * (self.ineq - 0.32)) \
            * (1.35 - 0.6 * eff) / (1.35 - 0.6 * 0.57) * (1 + 0.3 * (self.war == 2))
        self.loc_crime = _uclip(self.loc_crime + 0.1 * (ct - self.loc_crime) + 0.01 * r.normal(size=nl), 0.01, 1)
        wave = (self.loc_crime > 1.3 * self.loc_crime_ma) & (x[:, 0] < 0.5)
        for l in np.nonzero(wave)[0]:
            self._event("place", "crime wave", None, dict(loc=int(l)), big=False)
            self.loc_crime_ma[l] = self.loc_crime[l]
        self.loc_crime_ma += 0.05 * (self.loc_crime - self.loc_crime_ma)
        nbf = np.array([1.6, 0.9, 0.5])[self.nb_class] * (1.4 - 0.8 * self.nb_efficacy) / (1.4 - 0.8 * 0.57)
        self.nb_crime = _uclip(self.loc_crime[self.nb_loc] * nbf, 0.005, 1)
        et = np.array([.45, .58, .70])[self.nb_class] + 0.3 * (self.trust - 0.45) - 0.2 * (self.loc_unemp[self.nb_loc] - 5) / 10
        self.nb_efficacy = _uclip(self.nb_efficacy + 0.03 * (et - self.nb_efficacy) + 0.01 * r.normal(size=self.n_nb), .05, .98)
        # rent follows the housing gap and local growth; services follow the state budget
        self.loc_rent = _uclip(self.loc_rent + 0.05 * (self.loc_rent0 * (1 + 0.5 * self.housing) * (1 + 3 * self.loc_growth) - self.loc_rent), 0.2, 4)
        st = np.array([[.6, .55, .4], [.7, .65, .55], [.8, .75, .7], [.85, .85, .85]])[self.loc_size] \
            * (0.8 + 0.4 * self.capacity) * (0.85 + 0.5 * (self.welfare - self.p["welfare0"]) + 0.1 * self.gap)
        self.loc_services = _uclip(self.loc_services + 0.04 * (st - self.loc_services), 0.05, 1)
        # local politics: own cycle, same thermostat
        self.loc_next_vote -= 1
        for l in np.nonzero(self.loc_next_vote <= 0)[0]:
            if x[l, 1] < 0.5:
                self.loc_gov[l] = _norm(_norm(self.loc_mix[l] + p["k_thermo"] * (self.loc_mix[l] - self.loc_gov[l])) * np.exp(0.25 * nz[l]))
                self._event("place", "local election", "change", dict(loc=int(l)), big=False)
            else:
                self._event("place", "local election", "held", dict(loc=int(l)), big=False)
            self.loc_next_vote[l] = 16 + int(x[l, 2] * 5)

    # ------------------------------------------------------------------------------------------------ culture (spec 1 §4)
    def _culture_q(self):
        p, r = self.p, self.R[7]
        nz = r.normal(size=NN)
        # norms: logit S-curves toward a target set by the modern baseline, the value climate, the era and the law
        fitV = (self.V - self.V_anchor) @ self.NPROF.T
        fitE = self.era_i * ((self.era_p - 0.2) @ self.NPROF.T) if self.era_key is not None else 0.0
        lawsign = np.zeros(NN); lawsign[:NL] = 1.0 - self.laws
        for kk, ri in NORM_RIGHT.items():
            lawsign[NI[kk]] = 2 * self.rights[ri] - 1
        speed = (self.norm_x - self.norm_hist[0]) / 5.0                # logit per year over the last 5 years
        old = self._share_old()
        back = p["norm_back"] * np.sign(speed) * np.maximum(np.abs(speed) - 0.08, 0) * old
        tgt = self.norm_x0 + p["norm_v"] * fitV + p["norm_era"] * fitE + p["norm_law"] * (lawsign - self.lawsign0) - back
        young = self._share_young()
        rr = p["norm_r"] / 4 * (1 + 2.0 * (young - 0.2)) * (1 + 0.5 * self.comm)
        if self._s3("cult_no_dice"):                       # LW1 1h: no dice in the culture
            nz = 0.0 * nz
        self.norm_x = self.norm_x + rr * _uclip(tgt - self.norm_x, -1, 1) + 0.25 * self.norm_push + 0.012 * nz
        self.norm_push *= 0.5
        self.norm_hist = np.roll(self.norm_hist, -1, 0); self.norm_hist[-1] = self.norm_x
        self.norm_speed = float(np.abs(speed).mean())
        # trust falls with scandals and polarisation, recovers slowly; media fear rises with crime and crises
        tt = p["trust0"] + 0.04 - 0.5 * max(self.polar - 0.12, 0) - 0.08 * (self.phase == 1) * self.severity - 0.1 * (self.unrest - 0.12)
        self.trust = _cl(self.trust + 0.03 * (tt - self.trust), 0.05, 0.9)
        ft = p["fear0"] + 0.6 * ((self.loc_pop_share * self.loc_crime).sum() / self.crime_ref - 1) + 0.15 * (self.phase == 1) \
            + 0.3 * (self.war > 0) + 0.2 * (self.pandemic in (1, 2)) + 0.1 * (self.loc_disaster > 0).mean()
        self.fear = _cl(self.fear + 0.2 * (ft - self.fear), 0.02, 1)

    def _share_old(self):
        return self.old_share

    def _share_young(self):
        return self.young_share

    def _place_w(self):
        """(3, n_loc) population weights of the localities in each place class."""
        m = (self.loc_place[None, :] == np.arange(3)[:, None]) * self.loc_pop_share[None, :]
        return m / m.sum(1, keepdims=True)

    # ------------------------------------------------------------------------------------------------ society (spec 6)
    def _pos(self):
        """What the order rewards (spec 6 §2): state and law, institutions by reach and capacity, the economy's payoff,
        the established faiths by share."""
        p = self.p
        lawmix = _norm(0.2 + 0.25 * ((1.0 - self.laws)[:, None] * (self.NPROF[:NL] - 0.2)).mean(0)
                       + 0.5 * (self.welfare - p["welfare0"]) * (self.WPROF - 0.2))
        S = p["w_gov"] * self.G + (1 - p["w_gov"]) * lawmix
        w = self.inst_reach * self.inst_capacity
        w = np.where(self.inst_faith >= 0, 0.0, w)
        I = (w[:, None] * self.inst_profile).sum(0) / w.sum()
        B = self.faith_share @ self.FPROF + self.secular * 0.2
        ws = p["w_pos"]
        self.pos_parts = np.array([S, I, self.payoff, B])
        return _norm(ws[0] * S + ws[1] * I + ws[2] * self.payoff + ws[3] * B)

    def _needs(self):
        """Unmet needs per population group (safety, belonging, autonomy, competence, meaning), 0 met .. 1 unmet, from
        the economy, the state, war, welfare, place, faith and how far the order rewards the group's ways."""
        a, c, pl, f, m = self.gidx
        PW = self._place_w()
        pu, pc, pdis = PW @ self.loc_unemp, PW @ self.loc_crime, PW @ np.minimum(self.loc_disaster, 1)
        u_g = pu[pl] * np.array([1.6, 0.9, 0.5])[c] * np.array([0, 1.8, 1.2, 1.0, 0.9, 1.0, 0.3, 0])[a] * np.where(m == 1, 1.5, 1.0)
        rel = (f > 0).astype(float)
        old = (a >= 6).astype(float)
        lower = (c == 0).astype(float)
        mis = np.maximum(_tv(self.gmix, self.Pos) - 0.08, 0)
        lawc = (self.gmix @ self.NPROF[:NL].T) @ (self.laws / 2.0) / NL      # how far the law book closes the group's ways
        speed = getattr(self, "norm_speed", 0.0)
        fastmig = max(self.mig_in - 0.008, 0) * 60
        safety = (0.10 + 0.04 * np.maximum(u_g - 4, 0) + 0.35 * (self.war == 2) + 0.06 * (self.war == 1) + 0.4 * pc[pl]
                  + 0.04 * max(self.infl - 3, 0) * (1 + lower) + 0.2 * (self.pandemic == 2) * (1 + old) + 0.3 * pdis[pl]
                  - 0.2 * (self.welfare - self.p["welfare0"]) * (1 + lower))
        belong = (0.25 - 0.10 * rel + 0.15 * m * (1 - self.inst_open_mig.mean()) * 2 + 0.10 * (a == 7) + 0.05 * (pl == 0)
                  + 2.0 * speed * (a >= 5) + 0.3 * fastmig * (m == 0) * (a >= 4) + 0.15 * (0.45 - self.trust))
        auton = 0.15 + 0.6 * (1 - self.rights.mean()) + 1.2 * lawc + 0.8 * mis + 0.3 * self.lockdown
        compet = 0.15 + 0.04 * np.maximum(u_g - 4, 0) + 0.3 * (self.automation.mean()) * lower + 0.8 * mis
        mean_ = 0.20 - 0.12 * rel + 0.08 * (1 - rel) * (self.phase == 1) + 0.8 * mis + 1.0 * speed
        U = _uclip(np.stack([safety, belong, auton, compet, mean_], 1), 0, 1)
        return U

    def _society_q(self):
        p, r = self.p, self.R[8]
        x = r.random(6); nz = self._cn(r)
        self.Pos = self._pos()
        # demand: the groups' wanted colors (their mix plus what their unmet needs ask for, NEED_MAP_V6), by size and
        # voice for elections, by size and mobilisation for pressure (spec 6 §3)
        U = self._needs()
        want = _norm(self.gmix + p["zeta"] * (U @ self.NEEDM))
        size = self.pop.reshape(-1) * self.gadult
        voice = np.where(self.gidx[4] == 1, 0.3, 1.0) * (0.15 + 0.85 * self.demo) * np.where(self.gidx[0] == 1, 0.7, 1.0)
        voice = np.where(self.gidx[1] == 2, np.maximum(voice, 0.5), voice)
        wv = size * voice
        wq = size * (1 + p["mobil"] * U.sum(1))
        if self._s3("hist_grievance") and getattr(self, "s3_grv", None) is not None:   # LW2 2d: those the last change
            wq = wq * (1 + self.s3_grv)                                                # left behind push harder
        D0 = (wv[:, None] * want).sum(0) / wv.sum()
        Dq0 = (wq[:, None] * want).sum(0) / wq.sum()
        self.D0 = D0                                       # demand before the thermostat (hidden; tests)
        th_ = p["th_dem_s3" if self._s3("hist_party_gov") else "th_dem"]   # LW2 2b: the thermostat, refit with 2a
        self.Dem = _norm(D0 - th_ * (self.G - D0))
        self.Dem_q = _norm(Dq0 - th_ * (self.G - Dq0) + getattr(self, "dem_push", np.zeros(C)))
        self.dem_push = getattr(self, "dem_push", np.zeros(C)) * 0.8
        self.polar = float((size * _tv(want, D0)).sum() / size.sum())
        um = (size[:, None] * U).sum(0) / size.sum()
        self.unmet_mean = um
        self.need_base += 0.02 * (um - self.need_base)
        self.group_unmet = U
        # pressure, accelerators, inertia (spec 6 §4)
        gap = _tv(self.Pos, self.Dem_q)
        rec = (self.phase == 1) * (1 + self.severity) / 3
        tn = np.array(self.tech_kind) >= 0                 # new kinds spreading fast
        tech = float((self.tech_adopt_v[tn] * (1 - self.tech_adopt_v[tn])).mean() * 4) if tn.any() else 0.0
        mixed = -5 <= self.regime < 6                      # half open, half closed: the least stable (Hegre et al. 2001)
        acc = (1 + 1.0 * rec + 1.5 * self.unrest + 2.0 * (self._share_young() - 0.25) + 0.3 * tech
               + 0.5 * (self.ext_trade.sum() + 10 * self.mig_in) * 0.3 + 0.5 * max(p["trust0"] - self.trust, 0) * 4
               + 0.8 * (self.lost_war_q > 0) + p["mixed_acc"] * mixed)
        self.gap_slow += p["q_hab_r"] * (gap - self.gap_slow)        # people get used to a gap they have long lived with
        if getattr(self, "mandate_q", 0) > 0:                         # ... and give a new government its mandate
            self.gap_slow = max(self.gap_slow, gap)
            self.mandate_q -= 1
        self.gap_now = gap
        hp_ = self._s3("hist_pressure")
        exc = max(gap - p["q_tol_s3" if hp_ else "q_tol"]
                  - p["q_hab_s3" if hp_ else "q_hab"] * (p["mixed_hab"] if mixed else 1.0) * self.gap_slow, 0)
        self.Q = self.Q * (1 - p["q_decay_s3" if hp_ else "q_decay"]) + self.pace * p["q_k_s3" if hp_ else "q_k"] * exc * max(acc, 0.2)
        self._s3_society(U, want, size, wv, wq, D0, acc)
        age_i = float(np.minimum(self.inst_age, 120) @ self.inst_reach) / (float(self.inst_reach.sum()) + 1e-9) / 60
        rigid = float((self.law_since > 20).sum()) / NL
        hold = (0.55 + 0.15 * age_i + 0.2 * self.capacity + 0.15 * rigid + 1.0 * (self._share_old() - 0.25)
                + 0.4 * (self.regime < -5) * (1 - self.demo) - p["mixed_hold"] * mixed)
        self.hold = hold
        self.q_thr = p["q_theta_s3" if hp_ else "q_theta"] * max(hold, 0.2) ** p["q_hold"]
        self.open_q = max(self.open_q - 1, 0)
        self.since_break += 0.25
        if self.Q > self.q_thr:
            self._breakthrough(U, want, size, x, nz)       # (it recomputes Pos)
        self.pos_hist = np.roll(self.pos_hist, -1, 0); self.pos_hist[-1] = self.Pos
        self._era()

    def _breakthrough(self, U, want, size, x, nz):
        """Reform, revolution, revival or restoration (spec 6 §5); then pressure resets and the society stays open."""
        p = self.p
        pos_before = self.Pos.copy()
        exc = self.unmet_mean - self.need_base
        change = _tv(self.Pos, self.pos_hist[0])
        if self.regime < 6 and (self.unrest > 0.3 or (self.phase == 1 and self.severity == 2) or self.war == 2 or self.lost_war_q > 0):
            kind = 1
        elif exc[4] > 0.02 and exc[4] >= exc.max() - 1e-12:
            kind = 2
        elif change > 0.05 and (exc[1] > 0.01 or self.norm_speed > 0.06):
            kind = 3
        else:
            kind = 0
        step = p["q_step"][kind]
        if kind == 1:                                        # toward the most mobilised groups, not the majority
            w = size * U.sum(1) ** 3
            T = _norm((w[:, None] * want).sum(0) / w.sum())
        elif kind == 3:                                      # toward the losers of the last change
            loss = np.maximum(_tv(self.gmix, self.Pos) - _tv(self.gmix, self.pos_hist[0]), 0)
            w = size * (loss + 1e-6)
            T = _norm(0.5 * (w[:, None] * want).sum(0) / w.sum() + 0.5 * self.pos_hist[0])
        else:
            T = self.Dem_q
        self._event("era", "breakthrough", BREAKTHROUGHS[kind], dict(regime=round(float(self.regime), 1)), big=True)
        self.last_break = BREAKTHROUGHS[kind]
        self.n_break = getattr(self, "n_break", 0) + 1
        if kind == 2:                                        # revival: belief and norms first (spec 6 §5)
            fit_ = self.FPROF @ ((U[:, 4] * size)[:, None] * want).sum(0)
            if len(fit_) > NF:                             # C5: only a living movement can be revived
                fit_[NF:] = np.where(self.faith_open(0.0)[NF:], fit_[NF:], -np.inf)
            f = int(np.argmax(fit_))                       # the faith that fits the unmet
            self.revival = (f, 8)
            self.norm_x += 0.6 * ((self.FPROF[f] - 0.2) @ self.NPROF.T) * 5
            self.G = _norm(self.G + step * (T - self.G))
            self._event("belief", "revival", None, dict(faith=f), big=True)
        else:                                                # a landslide or a wave of reforms: the order is formed anew
            Gt = T if self._s3("hist_pressure") else _norm(T * np.exp(0.5 * p["g_noise"] * nz))   # 2c: no spread
            self.G = Gt if kind != 0 else _norm(self.G + p["ref_g"] * (Gt - self.G))   # a reform goes part of the way
            old = self.gov_party
            d = np.array([_tv(self.inst_profile[i], self.G) for i in self.party_ids])
            if kind != 0:
                d[old] = 9                                   # a revolution or restoration removes the governing party
            else:
                d[old] -= p["break_keep"]                    # a reform wave the governing party can lead itself
            if int(np.argmin(d)) != old:                     # a landslide: the party that fits it best, a new term
                self._change_gov(int(np.argmin(d)), x[1])
                self.support = p["s_win"] + 0.05
            else:
                self.support = min(0.95, self.support + 0.05)
            pid = self.party_ids[self.gov_party]
            if not self._s3("hist_party_gov"):               # 2a: a party keeps its own colours; they move with its voters
                self.inst_profile[pid] = 0.5 * self.inst_profile[pid] + 0.5 * self.G
        # laws: a burst of landmark laws toward the target; institutions reorganised toward it
        fit = (T - 0.2) @ self.NPROF[:NL].T
        n = _sig(self.norm_x[:NL])
        for k_ in range(NL):
            if fit[k_] > 0.02 and n[k_] > 0.5 and self.laws[k_] > 0 and x[2] < step * 2:      # laws trail norms
                self._set_law(k_, self.laws[k_] - 1)
            elif fit[k_] < -0.02 and n[k_] < 0.5 and self.laws[k_] < 2 and x[3] < step * 2:
                self._set_law(k_, self.laws[k_] + 1)
        pub = np.nonzero(self.inst_public | (self.inst_kind == INST_KINDS.index("media")))[0]
        self.inst_profile[pub] = _norm(self.inst_profile[pub] + step * (T - self.inst_profile[pub]))
        self.inst_corruption[pub] *= 1 - 0.5 * step
        if kind == 1:                                        # the regime falls: toward the mobilised groups' voice
            self.regime = _cl(self.regime + (8 if x[4] < 0.6 else -6) * (0.5 + x[5]), -10, 10)
            self.unrest = min(1.0, self.unrest + 0.3)
            self._event("state", "regime changes", None, dict(regime=round(self.regime, 1)), big=True)
            self._regime_derived()
        self.Q = 0.0
        self.Pos = self._pos()
        if self._s3("hist_grievance"):                     # LW2 2d: who lost by this change keeps it in mind
            self._grieve(want, pos_before, self.Pos)
        self.gap_slow = _tv(self.Pos, self.Dem_q)          # the new order becomes what people measure against
        self.open_q = int(p["q_open"][kind] * 4)
        self.since_break = 0.0
        self.break_kind = kind
        self.break_t = self.t

    # ---- stage 3 of the v22 update (chroma-world/model/stage3-rules.md §2 and §3)
    def _m_sh(self):
        """LW1 1g: how shaken the last year was, 1 (calm) to 3, from the year's mean of the accelerators."""
        p = self.p
        a = getattr(self, "s3_acc", None)
        acc = float(np.mean(a)) if a else p["acc_calm"]
        return float(_cl(1 + p["k_sh"] * (acc - p["acc_calm"]), 1, 3))

    def _s3_young_pull(self):
        """LW1 1b and 1c: what schools and media stand for, and the movements of the time, pulling the young."""
        p, out = self.p, np.zeros(C)
        if self._s3("cult_schools"):
            k = self.inst_kind
            sm = np.isin(k, [INST_KINDS.index("school"), INST_KINDS.index("university"), INST_KINDS.index("media")])
            w = self.inst_capacity[sm] * self.inst_reach[sm]
            if w.sum() > 0:
                out += p["coh_inst"] * ((w[:, None] * self.inst_profile[sm]).sum(0) / w.sum() - self.Vc)
        if self._s3("cult_scenes") and getattr(self, "s3_mw", None) is not None:
            out += p["coh_scene"] * self.s3_mob * (self.s3_mw - self.Vc)
        return out

    def _grieve(self, want, before, after):
        """LW2 2d: each group's loss from a change of the order becomes a grievance that fades over years."""
        loss = np.maximum(_tv(want, after) - _tv(want, before), 0)
        g = getattr(self, "s3_grv", None)
        self.s3_grv = (np.zeros(len(loss)) if g is None else g) + self.p["lose_k"] * loss

    def _s3_society(self, U, want, size, wv, wq, D0, acc):
        """The stage 3 rules that read society's quarter: the shake (1g), movements (1c), parties (2a'), grievances."""
        p = self.p
        if not any(self._s3(k) for k in S3_RULES):
            return
        self.s3_want, self.s3_size = want, size
        if self._s3("cult_shake"):                         # 1g, plus fast growth: the gap a deviation above its mean
            gm = getattr(self, "s3_gap_m", None)
            if gm is None:
                gm, gv = float(self.gap), 0.0
            else:
                gv = self.s3_gap_v
            gm += 0.01 * (self.gap - gm); gv += 0.01 * ((self.gap - gm) ** 2 - gv)
            self.s3_gap_m, self.s3_gap_v = gm, gv
            self.s3_boom_q = (getattr(self, "s3_boom_q", 0) + 1) if self.gap - gm > np.sqrt(max(gv, 1e-12)) else 0
            self.acc = float(acc + 0.5 * (self.s3_boom_q >= 4))
            self.s3_acc = (getattr(self, "s3_acc", []) + [self.acc])[-4:]
        if self._s3("cult_scenes"):                        # 1c: the movements of the time (and a revival's faith)
            u = 1 + p["mobil"] * U.sum(1)
            ub = float((size * u).sum() / size.sum())
            w = size * np.maximum(u - ub, 0)
            mw = (w[:, None] * want).sum(0) / w.sum() if w.sum() > 0 else self.Vc.copy()
            m0 = getattr(self, "s3_mob_m", None)
            m0 = ub if m0 is None else m0 + (ub - m0) / 200
            self.s3_mob_m = m0
            mob = float(_cl(ub / m0 - 1, 0, 1))
            rv = getattr(self, "revival", (0, 0))
            if rv[1] > 0:
                mw, mob = 0.5 * mw + 0.5 * self.FPROF[rv[0]], max(mob, 0.5)
            self.s3_mw, self.s3_mob = _norm(mw), mob
        if self._s3("hist_party_gov"):                     # 2a': parties move slowly with their voters
            ids = self.party_ids
            prof = self.inst_profile[ids]
            close = np.argmin(0.5 * np.abs(want[:, None, :] - prof[None]).sum(-1), 1)
            lam = _cl((self._m_sh() - 1) / 2, 0, 1) if self._s3("cult_shake") else 0.0
            w = (1 - lam) * wv + lam * wq
            ls = getattr(self, "s3_loser", (-1, 0))
            for j in range(len(ids)):
                sel = close == j
                if w[sel].sum() > 0:
                    B = (w[sel][:, None] * want[sel]).sum(0) / w[sel].sum()
                    prof[j] = prof[j] + p["party_k"] * (B - prof[j])
                if j == ls[0] and ls[1] > 0:
                    prof[j] = prof[j] + p["loser_k"] * (D0 - prof[j])
            self.inst_profile[ids] = _norm(prof)
            if ls[1] > 0:
                self.s3_loser = (ls[0], ls[1] - 1)
        if self._s3("hist_grievance") and getattr(self, "s3_grv", None) is not None:
            if len(self.s3_grv) != len(want):
                self.s3_grv = np.zeros(len(want))
            self.s3_grv = self.s3_grv * (1 - p["grv_fade"] / 4)

    def _era(self):
        """Name what emerges (spec 6 §6): an era while Pos leans clearly toward one combination.

        The lean is read from the society's own slow normal (era_ref = 1), not from even: a typical rich society leans
        the same way from even all the time, which would name one endless era. Intensity is that lean, scaled. An era
        ends when the lean fades (era_off) or when the order has pointed elsewhere for era_switch quarters (at once
        after a breakthrough that turns it), and the next can begin at once. Swing is not a rule here: it comes from
        the thermostat in Dem and from the normal following the order."""
        p = self.p
        lam = p["era_ref"]
        self.Pos_era += p["era_smooth"] * (self.Pos - self.Pos_era)     # a stretch of years, not one quarter
        self.Pos_slow += p["era_mem"] * (self.Pos_era - self.Pos_slow)
        ref = (1 - lam) * 0.2 + lam * self.Pos_slow
        d = self.Pos_era - ref
        lean = 0.5 * np.abs(d).sum()
        nd = np.linalg.norm(d)
        best = int(np.argmax(COMBO_DIR @ d)) if nd > 0 else -1
        self.lean = lean
        e_on, e_off = self._era_th()
        just = getattr(self, "break_t", -1) == self.t
        if just and getattr(self, "break_kind", 0) == 2 and best >= 0 and not (self.era_key is not None and self.era_k == 2):
            if self.era_key is not None:                      # a revival is a cosmology era (spec 6 §5-6): it ends the
                self._era_end()                               # running one and names its own, even on a faint lean
            self._era_begin(best, max(lean, e_on))
            return
        if self.era_key is None:
            if lean > e_on and best >= 0:
                self._era_begin(best, lean)
            return
        cur = COMBO_KEYS.index(self.era_key)
        if lean < e_off:
            self._era_end()
            return
        cos = float(COMBO_DIR[cur] @ d / nd)
        if cos < p["era_keep"] and best != cur:              # the order has turned elsewhere
            self.era_lead_q += 1
            if self.era_lead_q >= p["era_switch"] or (just and cos < 0):
                self._era_end()
                if lean > e_on:
                    self._era_begin(best, lean)
                return
        else:
            self.era_lead_q = 0
        self.era_i = float(0.8 * self.era_i + 0.2 * self._inten(lean))

    def _inten(self, lean):
        p = self.p
        e_on = self._era_th()[0]
        return _cl(0.3 + 0.7 * (lean - e_on) / (p["era_hi"] - e_on), 0.3, 1.0)

    def _era_th(self):
        """The era's start and end leans (LW2 2c refits them when pressure alone makes the eras)."""
        p = self.p
        return (p["era_on_s3"], p["era_off_s3"]) if self._s3("hist_pressure") else (p["era_on"], p["era_off"])

    def _era_begin(self, best, lean):
        key = COMBO_KEYS[best]
        if getattr(self, "break_t", -10 ** 9) >= self.t - 8 * 13 and getattr(self, "break_kind", 0) == 2:   # 2 years
            kind = 2
        else:
            u = COMBO_DIR[best]
            c = np.array([(self.p["w_pos"][0] * (self.pos_parts[0] - 0.2)) @ u,
                          (self.p["w_pos"][1] * (self.pos_parts[1] - 0.2) + self.p["w_pos"][2] * (self.pos_parts[2] - 0.2)) @ u,
                          (self.p["w_pos"][3] * (self.pos_parts[3] - 0.2)) @ u])
            kind = int(np.argmax(c - c.mean()))
        self.era_key, self.era_k, self.era_i = key, kind, self._inten(lean)
        self.era_p = COMBO_MIX[best].copy()
        self.era_since, self.era_lead, self.era_lead_q = self.t, -1, 0
        self.n_era += 1
        by_break = getattr(self, "break_t", -10 ** 9) >= self.t - 8 * 13
        self.era_at.append([self.t, key, round(self.era_i, 3), ERA_KINDS[kind]])
        if self._s3("hist_grievance") and getattr(self, "s3_want", None) is not None:   # LW2 2d
            if getattr(self, "s3_grv", None) is None or len(self.s3_grv) != len(self.s3_want):
                self.s3_grv = np.zeros(len(self.s3_want))
            w_ = self.s3_size * self.s3_grv
            if w_.sum() > 0:                               # what the last change's losers want, as this era starts (tests)
                self.s3_era_ans = getattr(self, "s3_era_ans", []) + [(int(self.t), ((w_[:, None] * self.s3_want).sum(0)
                                                                                     / w_.sum()).tolist(), key)]
            self._grieve(self.s3_want, self.Pos_slow, self.Pos_era)
        self._event("era", "era begins", key, dict(kind=ERA_KINDS[kind], idea=IDEAS[key][0], intensity=round(self.era_i, 2),
                                                    breakthrough=bool(by_break)), big=True)

    def _era_end(self):
        self._event("era", "era ends", self.era_key, dict(years=round((self.t - self.era_since) / 52, 1)), big=True)
        self.era_key, self.era_i, self.era_k, self.era_p = None, 0.0, 0, np.zeros(C)

    # ------------------------------------------------------------------------------------------------ public figures
    def _figures_q(self):
        r = self.R[9]
        x = r.random((len(FIG_ROLES), 4))
        for role, fid in list(self.fig_role_now.items()):
            if not self.F_alive[fid]:
                continue
            xr = x[role]
            age = (self.t - self.F_born[fid]) / 52
            self.F_mom[fid] = 0.8 * self.F_mom[fid] + 0.03 * (xr[0] - 0.5)
            self.F_standing[fid] = _cl(self.F_standing[fid] + self.F_mom[fid] * 0.3, 0.02, 1)
            if role == 0:
                self.F_standing[fid] = float(0.5 * self.F_standing[fid] + 0.5 * (0.3 + self.support))
            mort = 0.0005 * np.exp(0.085 * (age - 30)) / 4         # Gompertz, rich-country life table (estimate)
            if xr[1] < mort:
                self.F_alive[fid] = False; self.F_active[fid] = False
                self._event("figure", "death", FIG_ROLES[self.F_role[fid]], dict(fig=fid), big=self.F_standing[fid] > 0.4)
                self._replace_fig(role)
                continue
            if xr[2] < 0.008 * (1 + self.watch):
                self._fig_scandal(fid)
            retire = (FIG_ROLES[role] == "athlete" and age > 34) or (role >= 2 and age > 70) or self.F_standing[fid] < 0.05
            if retire and role >= 2 and xr[3] < 0.3:
                self.F_active[fid] = False
                self._event("figure", "falls", FIG_ROLES[role], dict(fig=fid), big=False)
                self._replace_fig(role)

    def _fig_scandal(self, fid):
        self.F_standing[fid] = max(0.02, self.F_standing[fid] - 0.25)
        self.F_mom[fid] -= 0.05
        self._event("figure", "scandal", FIG_ROLES[self.F_role[fid]], dict(fig=int(fid)), big=self.F_standing[fid] > 0.3)
        if self.F_role[fid] == 0:
            self.support -= 0.04

    def _replace_fig(self, role):
        if role == 0:                                         # a death in office: the party picks a new leader
            self._new_fig(self.R[9], 0, party=self.gov_party)
        else:
            self._new_fig(self.R[9], role, party=self.opp_party if role == 1 else None)

    # ------------------------------------------------------------------------------------------------ history (spec 5 §4)
    def _entry(self, domain, kind, key, value, big=False):
        # world-build.md "Game data": dict(t, age, era, domain, kind, key, value, who); age and who are the
        # character's, so the world writes None and the engine fills them; big marks headline events
        return dict(t=int(self.t), age=None, era=self.era_key, domain=domain, kind=kind, key=key,
                    value=_jsafe(value), who=None, big=bool(big))

    def _event(self, domain, kind, key, value, big=False, public=True):
        e = self._entry(domain, kind, key, value, big)
        if self.p.get("sph_events", False):   # spheres phase 3: the world-fired sphere events, fired at the next quarter
            v_ = value if isinstance(value, dict) else {}
            if domain == "state" and kind == "regime changes":   # which way, against the regime the last quarter saw
                was_ = getattr(self, "sph_reg_seen", None)
                v_ = dict(v_, state=None if was_ is None or float(self.regime) == was_ else ("up" if float(self.regime) > was_ else "down"))
            if not hasattr(self, "sph_wq") or self.sph_wq is None:
                self.sph_wq = []
            self.sph_wq.append([domain, kind, None if key is None else str(key), int(v_.get("loc", -1)), int(v_.get("inst", -1)),
                                None if v_.get("state") is None else str(v_["state"]), bool(big)])
        self.log.append(e)
        if public:
            self.record.append(e)

    def _history_q(self):
        # published figures lag a quarter; recessions are declared after the fact (two quarters in), as is the end
        self.record.append(self._entry("economy", "published", "unemployment", round(self.unemp_prev, 1)))
        self.record.append(self._entry("economy", "published", "inflation", round(self.infl, 1)))
        self.record.append(self._entry("state", "poll", "support", round(self.support, 2)))
        if self.phase == 1 and not self.rec_declared and self.rec_q >= 2:
            self.rec_declared = True
            self._event("economy", "recession declared", SEVERITY[self.severity], None, big=self.severity >= 1)
        if self.phase == 0 and self.rec_declared and self.t - self.rec_end_t >= 26:
            self.rec_declared = False
            self._event("economy", "recession over", None, None, big=False)
        if self.t % 104 == 0:
            self.norm_pub = _sig(self.norm_x).round(2)
            self.record.append(self._entry("culture", "poll", "norms", {k: float(v) for k, v in zip(NORM_KEYS, self.norm_pub)}))

    def _trace(self):
        """Hidden per-quarter state for the world-alone tests (cfg trace=True); never part of the game data."""
        K = self.inst_kind
        leg = [float(self.inst_legitimacy[K == INST_KINDS.index(x)].mean()) for x in ("ministry", "police", "court", "media")]
        self.trace.append(dict(t=self.t, phase=self.phase, sev=self.severity, unemp=self.unemp, infl=self.infl, gap=self.gap,
                               support=self.support, party=self.gov_party, G=self.G.copy(), Dem=self.Dem.copy(),
                               Pos=self.Pos.copy(), V=self.V.copy(), era=self.era_key, era_i=self.era_i, lean=self.lean,
                               Q=self.Q, thr=self.q_thr, unrest=self.unrest, trust=self.trust, legit=leg, war=self.war,
                               pandemic=self.pandemic, laws=self.laws.copy(), norms=_sig(self.norm_x), welfare=self.welfare,
                               mig=self.migrant_share, secular=self.secular, housing=self.housing, ineq=self.ineq,
                               loc_unemp=self.loc_unemp.copy(), payoff=self.payoff.copy(), polar=self.polar,
                               regime=self.regime, gov_q=self.gov_q, natural=self.natural, D0=self.D0.copy(),
                               tech=(self.tech_adopt_v / np.maximum(self.tech_ceil, 1e-3)).copy(), tech_born=list(self.tech_born),
                               temp=float(self._warming(self.t)), jobloss=float(self.rate_mult("jobloss").mean()),
                               birth=self.rate_mult("birth"), parts=self.pos_parts.copy(), Pos_era=self.Pos_era.copy(),
                               Pos_slow=self.Pos_slow.copy()))

    def events_since(self, t):
        """Log entries after world week t (the week's world events for the engine's events list)."""
        out = []
        for e in reversed(self.log):
            if e["t"] <= t:
                break
            out.append(e)
        return out[::-1]

    # ------------------------------------------------------------------------------------------------ yearly
    def _has_new(self, kind):
        return any(self.tech_kind[i] == NEW_TECH.index(kind) and self.tech_adopt_v[i] > 0.3 for i in range(len(self.tech_keys)))

    def _tech_y(self):
        """Technology (spec 5 §1): a generic modern kit at its level; a few new generic kinds arrive and spread."""
        p, r = self.p, self.R[10]
        x = r.random(4)
        lvl = self.cfg["tech_level"]
        rate = p["new_tech"] * {"behind": 0.6, "modern": 1.0, "ahead": 1.5}[lvl]
        if x[0] < rate:
            missing = [i for i in range(NT) if not self.tech_exists[i]]
            if missing:
                i = missing[int(x[1] * len(missing))]
                self.tech_exists[i] = True; self.tech_adopt_v[i] = 0.03; self.tech_ceil[i] = TECH_CEIL["modern"][i]
                self.tech_kind[i] = -2; self.tech_born[i] = int(self.t)
                self._event("tech", "arrives", TECH_KEYS[i], None, big=False)
            else:
                kind = int(x[1] * len(NEW_TECH))
                n_same = sum(1 for k_ in self.tech_kind if k_ == kind)
                key = f"{NEW_TECH[kind]} {n_same + 1}"
                self.tech_keys.append(key); self.tech_kind.append(kind); self.tech_born.append(int(self.t))
                self.tech_adopt_v = np.append(self.tech_adopt_v, 0.03); self.tech_ceil = np.append(self.tech_ceil, 0.6 + 0.35 * x[2])
                self.tech_exists = np.append(self.tech_exists, True)
                self._event("tech", "arrives", key, None, big=False)
        openness = float(self.V @ self.DOPEN) * 5
        sp = p["tech_r"] * (1 + 0.5 * self.gap) * (1 + 0.3 * openness)
        a = _uclip(self.tech_adopt_v, 1e-4, 1 - 1e-4)
        c = np.maximum(self.tech_ceil, 1e-3)
        frac = _uclip(a / c, 1e-4, 1 - 1e-4)
        before = self.tech_adopt_v.copy()
        self.tech_adopt_v = np.where(self.tech_exists, c * _sig(_logit(frac) + sp), 0.0)
        for i in np.nonzero((before < 0.5 * c) & (self.tech_adopt_v >= 0.5 * c) & (np.array(self.tech_born) > 0))[0]:
            self._event("tech", "spreads", self.tech_keys[i], round(float(self.tech_adopt_v[i]), 2), big=False)
        # effects of the new kinds
        kinds = np.array(self.tech_kind)
        def adopt_of(kind):
            m = kinds == NEW_TECH.index(kind)
            return float(self.tech_adopt_v[m].sum()) if m.any() else 0.0
        self.medical = _cl(self.medical + 0.05 * (self.medical0 + 0.08 * adopt_of("new treatment") - self.medical), 0, 0.98)
        self.comm = _cl(0.4 * self.tech_adopt_v[0] + 0.4 * self.tech_adopt_v[2] + 0.1 * adopt_of("new medium") + 0.1 * adopt_of("new way to meet"), 0, 1)
        wt = {"behind": .25, "modern": .40, "ahead": .55}[lvl] + 0.2 * (self.regime < 0) + 0.1 * adopt_of("new watch")
        self.watch = _cl(self.watch + 0.1 * (wt - self.watch), 0, 1)
        newm = adopt_of("new machine") + 0.5 * self.tech_adopt_v[TECH_KEYS.index("ai helper")]
        base = np.array([.10, .25, .15, .10, .03]) * (0.7 if lvl == "behind" else 1.3 if lvl == "ahead" else 1.0)
        spread = np.array([max(self.tech_adopt_v[i] - before[i], 0) for i in range(len(self.tech_keys))])
        mach = float(sum(spread[i] for i in range(len(self.tech_keys)) if kinds[i] == NEW_TECH.index("new machine")))
        self.automation = _uclip(self.automation + 0.15 * (base - self.automation) + mach * np.array([.3, 1.0, .6, .3, .1]), 0, 1)
        # sectors: automation shrinks the exposed sectors, new kinds of jobs grow knowledge, welfare moves the public sector
        jobs = adopt_of("new kind of job")
        tilt = np.array([-.4, -.6, -.1, .2, 0]) * (self.automation - base) * 2 + np.array([0, 0, 0, .15, 0]) * jobs \
            + np.array([0, 0, 0, 0, 0.8]) * (self.welfare - p["welfare0"])
        self.sector_tilt += 0.2 * (tilt - self.sector_tilt)
        self.loc_sectors = _norm(self.loc_sector_base * np.exp(self.sector_tilt))

    def _belief_y(self):
        """Belief (spec 5 §3): switching at real rates, insecurity raises religiosity, revivals, the calendar."""
        p, r = self.p, self.R[11]
        x = r.random(4)
        pop = self.pop
        insecure = _cl((self.phase == 1) * (self.severity + 1) / 3 + 0.6 * (self.war == 2) + 0.3 * (self.pandemic in (1, 2))
                                 + 0.3 * (self.loc_disaster > 0).mean(), 0, 1)
        adult = pop[1:]
        rel = adult[:, :, :, 1:, :]
        sec = adult[:, :, :, :1, :]
        dis = self._place_w() @ np.minimum(self.loc_disaster, 1)
        # leaving comes mostly in early adulthood (Pew 2015), joining a little more with age (both by adult age band)
        a_lv = np.array([2.5, 1.5, 0.7, 0.5, 0.4, 0.3, 0.3])[:, None, None, None, None]
        a_jn = np.array([0.6, 0.8, 1.0, 1.0, 1.2, 1.4, 1.4])[:, None, None, None, None]
        lv = p["leave_p"] * (1 - 0.6 * insecure) * a_lv
        jn = p["join_p"] * (1 + 2.0 * insecure) * (1 + 3 * dis)[None, None, :, None, None] * a_jn   # Bentzen 2019: disasters
        rv = getattr(self, "revival", None)
        fshare = rel.sum((0, 1, 2, 4)); fshare = fshare / max(fshare.sum(), 1e-9)
        attract = fshare.copy()
        if rv is not None and rv[1] > 0:
            attract[rv[0]] += 1.0; jn = jn * 3
            self.revival = (rv[0], rv[1] - 1)
        attract /= attract.sum()
        leave = rel * lv
        join = sec * jn
        sw = rel * p["switch_p"]
        moved = sw.sum(3, keepdims=True)
        new_rel = rel - leave - sw + join * attract[None, None, None, :, None] + moved * attract[None, None, None, :, None]
        new_sec = sec + leave.sum(3, keepdims=True) - join
        self.pop[1:, :, :, 1:, :] = np.maximum(new_rel, 0)
        self.pop[1:, :, :, :1, :] = np.maximum(new_sec, 0)
        self.switched = float(p["leave_p"] * (1 - 0.6 * insecure) + p["switch_p"])
        self.spiritual = _cl(self.spiritual + 0.05 * (0.1 + 0.3 * self.secular - self.spiritual), 0, 1)
        self.conspiracy = _cl(self.conspiracy + 0.1 * (0.08 + 0.3 * (0.45 - self.trust) + 0.2 * self.fear - self.conspiracy), 0, 1)
        self.holy_shift = (self.holy_shift + np.array(HOLY_LUNAR + [0.0] * (self._nf() - NF))) % 52

    def _generations_y(self):
        """Each generation's mix is set while it is 15 to 25 (spec 1 §4): from the society's values, the era and how
        secure the times are, read through the engine's Schwartz map (secure youth lean to self-direction and
        universalism, insecure youth to security and tradition), never a color rule."""
        p, r = self.p, self.R[12]
        y = self.t // 52
        nz = self._cn(r)
        sec = self.security()
        self.sec_hist = getattr(self, "sec_hist", []) + [round(sec, 4)]
        ca_ = p["coh_anchor"]
        base = _norm((1 - ca_) * self.Vc + ca_ * self.V_anchor)
        era = self.era_i * (self.era_p - 0.2) if self.era_key is not None else np.zeros(C)
        if self._s3("cult_anchor"):                        # LW1 1e as reworked (Emren 10-09): the young are drawn toward
            if getattr(self, "V_start", None) is None:     # the society's starting values moved by the era, whose hold
                self.V_start = np.asarray(self.Vc, float).copy()   # fades with its age: a bounded target, never a push
            if self.era_key is not None:                            # that lasts (which ran away)
                era = era * np.exp(-(self.t - self.era_since) / (52.0 * p["era_fade_y"]))
            tgt_ = np.maximum(self.V_start + p["era_home_k"] * era, 0.005)
            base = _norm((1 - p["coh_home"]) * self.Vc + p["coh_home"] * tgt_ / tgt_.sum())
            era = np.zeros(C)
        open_ = 1.5 if self.open_q > 0 else 1.0
        m_ = self._m_sh() if self._s3("cult_shake") else 1.0                          # LW1 1g: shaken times move faster
        if self._s3("cult_no_dice"):                                                  # LW1 1h: no dice in the culture
            nz = 0.0 * nz
        if m_ == 1.0 and not (self._s3("cult_schools") or self._s3("cult_scenes")):
            imp = _norm(base + p["coh_era"] * open_ * era + p["coh_sec"] * (sec - SEC_REF) * self.DSEC * 0.2) * np.exp(p["coh_noise"] * nz)
        else:
            imp = _norm(base + m_ * p["coh_gain"] * (p["coh_era"] * open_ * era + p["coh_sec"] * (sec - SEC_REF) * self.DSEC * 0.2)
                        + m_ * self._s3_young_pull()) * np.exp(p["coh_noise"] * nz)
        imp /= imp.sum()
        self._ensure_coh(y)
        for age in range(15, 26):
            b = self.Y0 + y - age
            if b < 0 or self.coh_fixed[b]:
                continue
            self.coh_n[b] += 1
            self.coh[b] += (imp - self.coh[b]) / self.coh_n[b]
            if age == 25:
                self.coh_fixed[b] = True
        for b in range(max(self.Y0 + y - 14, 0), self.Y0 + y + 1):       # the unformed young follow the society
            if not self.coh_fixed[b] and self.coh_n[b] == 0:
                self.coh[b] = base
        if self._s3("cult_adults"):                        # LW1 1d: generations past 25 move with the times, a fifth as fast
            bs = np.arange(max(self.Y0 + y - 100, 0), max(self.Y0 + y - 25, 0))
            bs = bs[self.coh_fixed[bs]]
            if len(bs):
                self.coh[bs] += p["coh_adult"] / 11 * m_ * (imp - self.coh[bs])
                self.coh[bs] /= self.coh[bs].sum(1, keepdims=True)

    def security(self):
        """How secure the times are for the young (0..1): work, war, pandemic, prices, welfare (estimate)."""
        return _cl(1 - 0.06 * max(self.unemp - self.natural, 0) - 0.12 * (self.phase == 1) * (1 + self.severity)
                             - 0.45 * (self.war == 2) - 0.1 * (self.war == 1) - 0.15 * (self.pandemic == 2)
                             - 0.03 * max(self.infl - 5, 0) + 0.2 * (self.welfare - self.p["welfare0"]) - 0.15 * self.unrest, 0, 1)

    def _ensure_coh(self, y):
        need = self.Y0 + y + 30
        if need > len(self.coh):
            extra = need - len(self.coh) + 100
            self.coh = np.concatenate([self.coh, np.tile(self.coh[-1], (extra, 1))])
            self.coh_fixed = np.concatenate([self.coh_fixed, np.zeros(extra, bool)])
            self.coh_n = np.concatenate([self.coh_n, np.zeros(extra)])

    def _pop_y(self):
        """Population (spec 2 §6): deaths, ageing, births, coming of age, migrants, class mobility; places."""
        p, r = self.p, self.R[12]
        x = r.random(4)
        pop = self.pop
        mort = np.array([.0003, .0005, .0008, .0015, .0035, .008, .02, .08])           # rich-country life tables (estimate)
        mult = 1 + 0.3 * (self.pandemic == 2) * np.array([0, 0, 0, 0, .2, .5, 1, 1.5]) + 0.01 * (self.war == 2)
        pop *= (1 - mort * mult)[:, None, None, None, None]
        width = np.array([15, 10, 10, 10, 10, 10, 10, 1e9])
        flow = pop / width[:, None, None, None, None]
        flow[-1] = 0
        # coming of age: in secure times some of the faithful young leave (secularisation by generation)
        sec = self.security()
        psi = _cl(p["secularise"] * (1 + 3.0 * (sec - SEC_REF)) * (0.3 if getattr(self, "revival", (0, 0))[1] > 0 else 1), 0, 0.5)
        f0 = flow[0].copy()
        lv = f0[:, :, 1:, :] * psi
        f0[:, :, 1:, :] -= lv; f0[:, :, :1, :] += lv.sum(2, keepdims=True)
        flow[0] = f0
        pop -= flow
        pop[1:] += flow[:-1]
        # births (Sobotka et al. 2011: put off in downturns), into the parents' class, place and faith, native-born
        parents = pop[2:4].sum(0).sum(-1)
        pop[0, ..., 0] += 0.042 * self.rate_mult("birth") * parents
        # migrants (UN DESA; OECD: about 1 in 7 foreign-born): inflow pulled by the economy, pushed by neighbours
        push = float((self.ext_migration * (0.5 + self.ext_trade)).sum())
        self.mig_in = float(p["mig0"] * (1 + 0.8 * self.gap) * (0.7 + 0.6 * push) * (0.5 + 0.5 * self.demo))
        if push > 0.8 and x[0] < 0.5 and self.ext_war.any():
            self._event("abroad", "refugees arrive", None, dict(share=round(self.mig_in, 4)), big=False)
        tot = pop.sum()
        newm = self.mig_in * tot
        ma = np.array([0, .4, .45, .1, .05, 0, 0, 0]); mc = np.array([.45, .45, .10]); mp = np.array([.7, .25, .05])
        mf = np.array([.25, .30, .15, .30] + [0.0] * (self._nf() - NF))   # C5: no migrant arrives in a movement
        pop[..., 1] += newm * ma[:, None, None, None] * mc[None, :, None, None] * mp[None, None, :, None] * mf[None, None, None, :]
        pop[..., 1] *= 1 - p["mig_out"]
        # class mobility (small, downward in recessions)
        down = 0.004 + 0.004 * (self.phase == 1)
        up = 0.006 * (1 + self.gap)
        lo, mi, hi = pop[:, 0].copy(), pop[:, 1].copy(), pop[:, 2].copy()
        pop[:, 0] += down * mi - up * lo; pop[:, 1] += up * lo - down * mi + 0.004 * hi - 0.003 * mi
        pop[:, 2] += 0.003 * mi - 0.004 * hi
        # places: growth follows the local economy; declining places lose people (spec 3 §2.3)
        g = (0.004 * self.loc_trend_base() - 0.003 * (self.loc_unemp - self.unemp) / max(self.unemp, 1)
             + 0.02 * (self.loc_pop0 - self.loc_pop_share) / self.loc_pop0)
        self.loc_growth = 0.7 * self.loc_growth + 0.3 * g
        old_tr = self.loc_trend.copy()
        self.loc_trend = np.where(self.loc_growth > 0.002, 2, np.where(self.loc_growth < -0.002, 0, 1))
        self.loc_pop_share = self.loc_pop_share * (1 + g); self.loc_pop_share /= self.loc_pop_share.sum()
        place = np.array([(self.loc_pop_share * (self.loc_place == k)).sum() for k in range(3)])
        cur = pop.sum((0, 1, 3, 4))
        pop *= (place / np.maximum(cur / cur.sum(), 1e-9))[None, None, :, None, None]
        self.pop = pop / pop.sum()
        # faith shares, migrants, value climate
        self._group_mix()
        self.V = self._V()
        self.Vc_hist.append(self.V.tolist())
        w = self.pop.reshape(-1) * self.gadult
        pl = self.gidx[2]
        lm = np.array([(w[pl == k][:, None] * self.gmix[pl == k]).sum(0) / max(w[pl == k].sum(), 1e-9) for k in range(3)])
        self.loc_mix = _norm(lm[self.loc_place] + 0.15 * (self.loc_class_mix[:, 2:3] - 0.15) * self.DSEC * 0.2)

    def loc_trend_base(self):
        k = [LOC_KINDS[i] for i in self.loc_kind]
        return np.array([{"capital": .8, "tech boom town": 2.0, "energy boom town": 1.5, "declining industrial town": -2.0,
                          "commuter suburb": .8, "remote area": -1.0, "fishing village": -.8, "mountain village": -.6,
                          "university city": .5}.get(x, 0.0) for x in k])

    def _group_mix(self):
        """Each group's mix: its generations' mixes plus class, place, faith and migrant tilts (the class and place
        tilts run along the secure and openness directions of the Schwartz map)."""
        p = self.p
        y = self.t // 52
        self._ensure_coh(y)
        cb = np.zeros((8, C))
        for a, (lo, hi) in enumerate(AGE_BANDS):
            bs = np.arange(self.Y0 + y - min(hi, 100) + 1, self.Y0 + y - lo + 1)
            bs = bs[bs >= 0]
            cb[a] = self.coh[bs].mean(0)
        self.coh_band = cb
        w = self.pop.sum((1, 2, 3, 4))
        self.Vc = _norm((w[1:, None] * cb[1:]).sum(0) / w[1:].sum())
        tc = p["tilt_class"] * np.array([-1, 0, 1])[:, None] * self.DSEC * 0.2 * 5
        tp = p["tilt_place"] * np.array([1, 0, -1])[:, None] * self.DOPEN * 0.2 * 5
        tf = np.vstack([np.zeros(C), p["tilt_faith"] * (self.FPROF - 0.2)])
        if hasattr(self, "ext_V"):
            ev = (self.ext_V * (self.ext_migration + 0.1)[:, None]).sum(0) / (self.ext_migration + 0.1).sum()
            self.mig_tilt = p["tilt_mig"] * (ev - self.Vc)
        tm = np.vstack([np.zeros(C), self.mig_tilt])
        a, c, pl, f, m = self.gidx
        if self._s3("cult_pushback") and getattr(self, "group_unmet", None) is not None and len(self.Vc_hist) > 10:
            dV = self.V - np.asarray(self.Vc_hist[-11])  # LW1 1f: the last decade's change, braked by those it leaves behind
            u_ = self.group_unmet.sum(1); u_ = _uclip(u_ / max(u_.mean(), 1e-9) - 1, 0, 2)
            lb = (u_ * np.where(a >= 4, 1.0, np.where(a >= 3, 0.5, 0.2)) * np.array([0.7, 1.0, 1.3])[pl]
                  * np.array([1.3, 1.0, 0.7])[c])
            self.gmix = _norm(cb[a] + tc[c] + tp[pl] + tf[f] + tm[m] - p["coh_back"] * lb[:, None] * dV, 0.01)
        else:
            self.gmix = _norm(cb[a] + tc[c] + tp[pl] + tf[f] + tm[m], 0.01)
        a_ = self.pop.sum((1, 2, 3, 4))
        self.old_share, self.young_share = float(a_[5:].sum() / a_[1:].sum()), float(a_[1:3].sum() / a_[1:].sum())
        fs = self.pop.sum((0, 1, 2, 4))
        self.secular = float(fs[0])
        self.faith_share = fs[1:].copy()
        self.migrant_share = float(self.pop[..., 1].sum())

    def _V(self):
        w = self.pop.reshape(-1) * self.gadult
        return _norm((w[:, None] * self.gmix).sum(0) / w.sum())

    # ------------------------------------------------------------------------------------------------ pushes (spec 7 §3)
    def push(self, domain, var, amount, sign):
        """Queue a push from a life; it lands at the next quarter tick, scaled into the domain's own dynamics.
        amount is the push's size in reach units (0 one of the crowd .. 3 strongly: base x reach x how well it went);
        sign is +1 or -1. Variables by domain (an id follows a colon, e.g. "legitimacy:12"):
          state: "support"; a law key (a minister passes what the norms support, fails more often against them);
                 "welfare"; "pressure" (a movement's push on the society's pressure); a color letter (its direction)
          culture: a norm key (moves acceptance a little, with a lag); "trust"; a color letter
          economy: "inequality", "housing"; place: "crime:<loc>", "efficacy:<nb>", "unemp:<loc>"
          institution: "legitimacy:<id>", "corruption:<id>", "capacity:<id>", "reform:<id>"
          tech: "adopt:<key>", "medical", "invent"; belief: "faith:<f>", "secular"; abroad: "relation:<society>"
          nature: "warming" (tiny)."""
        self._queue.append([str(domain), str(var), float(amount), 1.0 if sign >= 0 else -1.0])

    def _apply_pushes(self):
        CROWD = 1e-6                                          # an ordinary voice is one of millions
        for dom, var, amt, sg in self._queue:
            a = max(amt, CROWD) * sg
            key, _, idx = var.partition(":")
            done = None
            try:
                if dom == "state" and key == "support":
                    self.support = _cl(self.support + 0.01 * a, 0.02, 0.98); done = 0.01 * a
                elif dom == "state" and key in LI:
                    self.law_push[LI[key]] += 0.6 * a; done = 0.6 * a     # a minister (3) passes it if norms agree
                elif dom == "state" and key == "welfare":
                    self.welfare = _cl(self.welfare + 0.01 * a, 0.05, 0.95); done = 0.01 * a
                elif dom == "state" and key == "pressure":
                    self.Q = max(0.0, self.Q + 0.05 * a * getattr(self, "q_thr", self.p["q_theta"])); done = 0.05 * a
                elif dom in ("state", "culture") and key in COLORS:
                    dv = np.zeros(C); dv[COLORS.index(key)] = 0.005 * a; dv -= dv.mean()
                    self.dem_push = getattr(self, "dem_push", np.zeros(C)) + dv; done = 0.005 * a
                elif dom == "culture" and key in NI:
                    self.norm_push[NI[key]] += 0.05 * a; done = 0.05 * a
                elif dom == "culture" and key == "trust":
                    self.trust = _cl(self.trust + 0.005 * a, 0.02, 0.95); done = 0.005 * a
                elif dom == "economy" and key == "inequality":
                    self.ineq = _cl(self.ineq + 0.002 * a, 0.15, 0.6); done = 0.002 * a
                elif dom == "economy" and key == "housing":
                    self.housing = _cl(self.housing + 0.01 * a, -1, 1); done = 0.01 * a
                elif dom == "place" and key == "crime":
                    self.loc_crime[int(idx)] = _uclip(self.loc_crime[int(idx)] + 0.02 * a, 0.01, 1); done = 0.02 * a
                elif dom == "place" and key == "efficacy":
                    self.nb_efficacy[int(idx)] = _uclip(self.nb_efficacy[int(idx)] + 0.03 * a, 0.05, 0.98); done = 0.03 * a
                elif dom == "place" and key == "unemp":
                    self.loc_ufac[int(idx)] = max(0.3, self.loc_ufac[int(idx)] + 0.02 * a); done = 0.02 * a
                elif dom == "institution" and key in ("legitimacy", "corruption", "capacity"):
                    arr = getattr(self, "inst_" + key); i = int(idx)
                    arr[i] = _uclip(arr[i] + 0.03 * a, 0.01, 0.99); done = 0.03 * a
                    if a < 0 and getattr(self, "c3_cover", None) is not None and self.c3_cover[i] > self.t:
                        self.c3_break[i] = True                    # C3: an insider speaks up; the scandal breaks
                elif dom == "institution" and key == "reform" and a > 0:
                    i = int(idx)
                    if a >= 1.5: self._reform_inst(i, self.inst_native[i], step=0.2 * a)
                    done = a
                elif dom == "tech" and key == "adopt" and idx in self.tech_keys:
                    i = self.tech_keys.index(idx)
                    self.tech_adopt_v[i] = _uclip(self.tech_adopt_v[i] + 0.002 * a, 0, self.tech_ceil[i]); done = 0.002 * a
                elif dom == "tech" and key == "medical":
                    self.medical0 = _cl(self.medical0 + 0.005 * a, 0, 0.95); done = 0.005 * a
                elif dom == "tech" and key == "invent" and a >= 2.0:
                    self.medical0 = _cl(self.medical0 + 0.01, 0, 0.95); done = 0.01
                elif dom == "belief" and key == "faith":
                    f = int(idx); d = 0.002 * a * self.pop[1:, :, :, 0, :]
                    self.pop[1:, :, :, 0, :] -= d; self.pop[1:, :, :, 1 + f, :] += d; done = 0.002 * a
                elif dom == "belief" and key == "secular":
                    d = 0.002 * a * self.pop[1:, :, :, 1:, :]
                    self.pop[1:, :, :, 1:, :] -= d; self.pop[1:, :, :, :1, :] += d.sum(3, keepdims=True); done = 0.002 * a
                elif dom == "abroad" and key == "relation" and abs(a) >= 1:
                    j = int(idx); self.ext_relation[j] = int(_uclip(self.ext_relation[j] - np.sign(a), 0, 3)); done = -np.sign(a)
                elif dom == "nature" and key == "warming":
                    done = 0.0
            except (ValueError, IndexError):
                done = None
            self.push_log.append(dict(t=int(self.t), domain=dom, var=var, amount=amt, sign=sg,
                                      applied=None if done is None else float(done)))
        self._queue = []
        if len(self.push_log) > 400:
            self.push_log = self.push_log[-400:]

    # ------------------------------------------------------------------------------------------------ what the engine reads
    def law_state(self, key):
        return int(self.laws[LI[key]]) if key in LI else int(LAW_MOD[key])   # W38b keys: the modern law book

    def norm(self, key):
        return float(_sig(self.norm_x[NI[key]])) if key in NI else float(NORM_MOD[key])   # W38b keys: modern acceptance

    def tech_has(self, key):
        return key in self.tech_keys and bool(self.tech_exists[self.tech_keys.index(key)])

    def tech_adopt(self, key, cls=None, age=None, place=None):
        """Adoption 0..1, nationally or for a group: the young, the rich and the urban first (spec 5 §1)."""
        if not self.tech_has(key):
            return 0.0
        a = float(self.tech_adopt_v[self.tech_keys.index(key)])
        if cls is None and age is None and place is None:
            return a
        off = 0.0
        if cls is not None: off += (-0.8, 0.0, 0.7)[int(cls)]
        if place is not None: off += (0.3, 0.0, -0.6)[int(place)]
        if age is not None: off += _cl((35 - age) / 25, -2.0, 0.8)
        return float(_sig(_logit(a) + off))

    def holy_weeks(self, faith=None):
        """{holy key: set of weeks of the year} for a faith (default: the culture's main faith) this year."""
        f = int(np.argmax(self.faith_share)) if faith is None or faith < 0 else int(faith)
        sh = int(round(self.holy_shift[f]))
        return {k: set(int((w + sh) % 52) for w in HOLY_BASE[f][k]) for k in HOLY_KEYS}

    def cohort_mix(self, birth_week):
        """A generation's mix: fixed when it is 15 to 25; the current base while it is younger."""
        b = int(self.Y0 + np.floor(birth_week / 52))
        self._ensure_coh(self.t // 52)
        b = int(_uclip(b, 0, len(self.coh) - 1))
        return self.coh[b].copy()

    def rate_mult(self, kind):
        """Multipliers on the Library's per_year rates (world-build.md). Season, pandemic and medicine for illness and
        old-age deaths (scalar); locality arrays for disaster and crime (crime_nb per neighbourhood); a sector array for
        job loss; scalars for war, pandemic moments and births. Health effects stay rate multipliers only (R5)."""
        s = self.season
        if kind == "illness":
            return float((1.3, 1.0, 0.75, 0.95)[s] * (1, 1.3, 2.0, 1.3)[self.pandemic] * (1 - 0.5 * (self.medical - self.medical0)))
        if kind == "old_death":
            return float((1.12, 0.99, 0.92, 0.97)[s] * (1, 1.2, 1.6, 1.15)[self.pandemic] * (1 - 0.5 * (self.medical - self.medical0)))
        if kind == "disaster":                             # pace, and the recovery years after a strike (loc_disaster);
            hz = (self.loc_hazards * np.array(self.p["dis_base"]) * self.extremes).sum(1) / self.haz_ref   # the strike
            return self.pace * hz * (1 + self.p["dis_active"] * np.minimum(self.loc_disaster, 1))          # itself: disaster_now
        if kind == "crime":
            return self.loc_crime / self.crime_ref
        if kind == "crime_nb":
            return self.nb_crime / self.crime_ref
        if kind == "war":
            return float((0.3, 4.0, 15.0)[self.war])
        if kind == "pandemic":
            return float((0.2, 2.0, 4.0, 1.5)[self.pandemic])
        if kind == "jobloss":
            return self.unemp_sector / self.nat_sector
        if kind == "birth":
            return _cl(1 - 0.015 * (self.unemp - self.natural) - 0.15 * (self.war == 2) - 0.08 * (self.pandemic == 2)
                                 + 0.03 * max(self.gap, 0), 0.6, 1.1)
        raise KeyError(kind)

    @property
    def faith_profile(self):
        return self.FPROF

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 1c
    # Each town's nine spheres: a size (its share of the town's waking hours) and five face shares (one per colour),
    # updated each quarter after _society_q (needs and demand are fresh) and before _figures_q. Read only: nothing in a
    # life reads it yet, and it draws no dice. Rules: chroma-world/spheres/data/dynamics.json (face_mix, size, drivers),
    # proposal chroma-ideas/spheres-implementation.md section 3, phase 1; the tables: sphere_data.py.
    SPH_EPOCH = {"earth": "modern", "tribal": "bands", "magic": "magic"}
    SPH_DRV_K = None

    def _sph_tables(self):
        """The sphere tables in this world's colour frame (permuted like _tables), made once (not saved)."""
        c_ = getattr(self, "_cache_sph", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        P_ = self.perm; pr = dict(SD.PARAMS, **(self.p.get("sph_par") or {})); ep = self.SPH_EPOCH.get(self.cfg.get("setting", "earth"), "modern")
        M0 = np.asarray(SD.M0[ep], float)[:, P_]
        D = np.array([SD.D[d] for d in SD.DRIVERS], float)[:, :, P_]            # 8 drivers x 9 spheres x 5 colours
        D = D - D.mean(1, keepdims=True)                                          # each colour's mean over the spheres out
        kd = dict(pr["k_drivers"], insecurity=pr["kQ"], plenty=pr["kO"])
        MEET = np.asarray(SD.MEETS, float)[:, P_, :]                              # 9 x 5 x (safety, belonging, meaning)
        sp = SD.SPHERES; ix = {s_: i_ for i_, s_ in enumerate(sp)}
        vec = lambda d_, dflt=0.0: np.array([float(d_.get(s_, dflt)) for s_ in sp])
        phi = np.zeros((9, 3))                                                    # under 15, 15 to 29, 65 and over
        for k_, v_ in pr["phi"].items():
            s_, a_ = (k_.split("<")[0], 0) if "<" in k_ else (k_[:-3], 2) if k_.endswith("65+") else (k_[:-5], 1)
            phi[ix[s_], a_] = v_
        alpha = np.zeros(9); alpha[ix["prod"]] = pr["alpha_prod"]
        c_ = dict(ep=ep, M0=M0, D=D, kd=np.array([kd[d] for d in SD.DRIVERS]), MEET=MEET,
                  MEETc=MEET - MEET.mean(1, keepdims=True), rho=vec(pr["rho"]), eps=vec(pr["eps"], 1.0),
                  beta=vec(pr["beta"]), zeta=vec(pr["zeta"]), alpha=alpha, phi=phi,
                  base=np.asarray(pr["base_share"][ep], float), mem=np.array([pr["drv_mem"]["war" if d == "war" else "others"]
                                                                         for d in SD.DRIVERS]),
                  war=(ix["prot"], ix["rule"]), plague=(ix["care"], ix["gather"]), pr=pr, n_drv=len(SD.DRIVERS))
        # phase 3: the joins' spill (N6), the year's rhythm (N7) and the pair faces, in this world's colour frame
        inv = np.argsort(P_); ci = {c_k: inv["WUBRG".index(c_k)] for c_k in "WUBRG"}
        pA = np.zeros((len(SPH_PAIRS), C)); pT = np.full((len(SPH_PAIRS), C), 0.2 / 3)
        for k_, pp in enumerate(SPH_PAIRS):
            pA[k_, [ci[pp[0]], ci[pp[1]]]] = 1.0; pT[k_, [ci[pp[0]], ci[pp[1]]]] = 0.4
        c_.update(Jsp=np.asarray(SD.J[ep], float) * (1 - float(SD.SEPARATION[ep])),
                  seas_h=np.array([SD.SEASONS["hours"][s_] for s_ in sp]), seas_z=np.array([SD.SEASONS["hazards"][s_] for s_ in sp]),
                  pairA=pA, pairT=pT, pair_i=np.array([[ci[pp[0]], ci[pp[1]]] for pp in SPH_PAIRS]))
        self._cache_sph = c_
        return c_


    def _sph_town_needs(self):
        """Each town's unmet needs (n_loc x 5), from the population groups of its place class (_society_q's
        group_unmet), with its own crime and disasters in place of its class's mean."""
        U = self.group_unmet; pl = self.gidx[2]; w = self.pop.reshape(-1)
        Uc = np.stack([(w[pl == k][:, None] * U[pl == k]).sum(0) / max(w[pl == k].sum(), 1e-12) for k in range(3)])
        PW = self._place_w(); lp = self.loc_place
        pc, pdis = PW @ self.loc_crime, PW @ np.minimum(self.loc_disaster, 1)
        Ut = Uc[lp].copy()
        Ut[:, 0] += 0.4 * (self.loc_crime - pc[lp]) + 0.3 * (np.minimum(self.loc_disaster, 1) - pdis[lp])
        return _uclip(Ut, 0, 1)

    def _sph_ages(self):
        """Each town's shares under 15, 15 to 29 and 65 and over (n_loc x 3), from its place class's groups."""
        pop = self.pop.sum(axis=(1, 3, 4))                                        # age band x place class
        pop = pop / np.maximum(pop.sum(0, keepdims=True), 1e-12)
        a3 = np.stack([pop[0], pop[1] + 0.5 * pop[2], pop[6] + pop[7]], 1)        # place class x 3
        return a3[self.loc_place]

    def _sph_drivers(self):
        """The eight drivers' levels in each town (n_loc x 8; dynamics.json drivers)."""
        nl = self.n_loc
        sec = self.security() - 0.4 * self.loc_crime - 0.3 * np.minimum(self.loc_disaster, 1) - 0.2 * (self.fear - self.p["fear0"])
        y = self.gap + (self.natural - self.loc_unemp) / 10 - (self.food + self.energy) / 6
        war = 0.5 * (self.war == 1) + 1.0 * (self.war == 2) + 0.2 * bool(np.any(self.ext_war))
        crowd = 100 * self.loc_growth + 50 * self.mig_in
        ineq = 5 * self.ineq
        school = self.loc_sectors[:, SECTORS.index("knowledge")]                 # proxy until the literate share is built
        media = self.inst_kind == INST_KINDS.index("media")
        expo = self.watch * (float(self.inst_capacity[media].mean()) if media.any() else 0.0)
        tv = np.asarray(self.tech_adopt_v, float); au = float(np.mean(self.automation)); tr = float(np.sum(self.ext_trade))
        last = getattr(self, "sph_chg_last", None)
        n_ = 0 if last is None else min(len(tv), len(last[0]))            # a new kind counts from its second quarter
        chg = 0.0 if last is None else (float(np.maximum(tv[:n_] - last[0][:n_], 0).sum()) + (au - last[1]) + (tr - last[2]))
        self.sph_chg_last = (tv.copy(), au, tr)
        chg += float(getattr(self, "norm_speed", 0.0))
        b = lambda x_: np.broadcast_to(np.asarray(x_, float), (nl,))
        return np.stack([-b(sec), b(y), b(war), b(crowd), b(ineq), b(school), b(expo), b(chg)], 1)   # insecurity: -sec

    def _sph_leaders(self):
        """Per town and sphere: the leaders' colour mix, their corruption and the bodies' age (capacity- and reach-
        weighted over the sphere's institutions in town, else the whole country's); has: whether the sphere has any."""
        nl = self.n_loc
        # a body with no reach beyond itself (a faith body, a party) still leads its own sphere: reach counts from .2
        A = (self.inst_sphere[:, None] == np.arange(9)[None]) * (self.inst_capacity * np.maximum(self.inst_reach, 0.2) + 1e-9)[:, None]
        B = (np.asarray(self.inst_loc)[:, None] == np.arange(nl)[None]).astype(float)        # institution x town
        X = np.concatenate([self.inst_leader_pie, self.inst_corruption[:, None], self.inst_age[:, None],
                            np.ones((len(A), 1))], 1)                                         # what is averaged, and 1
        loc = np.einsum("il,ij,ik->ljk", B, A, X)                                            # town x sphere x (5 + 3)
        nat = np.einsum("ij,ik->jk", A, X)[None]                                             # the whole country's
        has_l = loc[..., -1] > 1e-6
        tot = np.where(has_l[..., None], loc, nat)
        has = tot[..., -1] > 1e-6
        m = tot[..., :-1] / np.maximum(tot[..., -1:], 1e-12)
        Ld = np.where(has[..., None], m[..., :C], 0.2); corr = np.where(has, m[..., C], 0.0)
        age = np.where(has, m[..., C + 1], 50.0)
        return Ld, corr, age, has

    def _sphere_q(self):
        T = self._sph_tables(); pr = T["pr"]; nl = self.n_loc
        U = self._sph_town_needs(); un = U[:, [0, 1, 4]]                          # safety, belonging, meaning
        x_lvl = self._sph_drivers(); ages = self._sph_ages()
        tech = float(self.tech_adopt_v[self.tech_keys.index("internet")]) if "internet" in self.tech_keys else 0.0
        auto = float(np.mean(self.automation[[SECTORS.index("farm"), SECTORS.index("industry")]]))
        if getattr(self, "sph_s", None) is None:                                  # the first quarter: home ways, at rest
            self.sph_s = np.tile(T["M0"], (nl, 1, 1)); self.sph_ds = np.zeros((nl, 9, C)); self.sph_H = self.sph_s.copy()
            self.sph_Z = np.tile(T["base"], (nl, 1)); self.sph_need = un.copy(); self.sph_drv = x_lvl.copy()
            self.sph_ref = dict(ages=ages.copy(), tech=tech, auto=auto); self.sph_rat = np.ones(9)
        s, Z = self.sph_s, self.sph_Z
        # needs (N): gaps from the town's slow baseline, plus the pushback of what the town's spheres leave unmet
        e = un - self.sph_need
        sup = np.einsum("lj,ljc,jcn->ln", Z, s, T["MEET"]); sup0 = np.einsum("lj,jcn->ln", Z, 0.2 * T["MEET"])
        e = e + pr["kS"] * (sup0 - sup)
        self.sph_need += pr["need_mem"] * (un - self.sph_need)
        Nt = pr["kN"] * np.einsum("ln,jcn->ljc", e, T["MEETc"])
        # drivers (Q, O, T): each level against the town's memory of it, by the sphere's own projected weights
        x = _uclip(x_lvl - self.sph_drv, -1, 1)
        self.sph_drv += T["mem"] * (x_lvl - self.sph_drv); self.sph_x = x
        Tt = np.einsum("d,ld,djc->ljc", T["kd"], x, T["D"])
        Kt = pr["kK"] * (np.asarray(self.loc_mix, float) - 0.2)[:, None, :]     # the culture's lean in town
        Xt = self._sph_events_q(e) if self.p.get("sph_events", False) else 0.0   # phase 3: the events' fading shifts
        if self.p.get("sph_joins", False) and self.p.get("sph_events", False):   # N6: a shift spills to joined spheres
            Xt = Xt + np.einsum("jk,ljc->lkc", T["Jsp"], Xt)
        if self.p.get("sph_links", False) and self.p.get("sph_events", False):   # the links between spheres
            Xt = Xt + self._sph_links_q()
        Dm = T["M0"][None] * np.exp(Nt + Tt + Kt + Xt)
        Dm = Dm / Dm.sum(-1, keepdims=True)
        Ld, corr, age, has = self._sph_leaders()
        if self.p.get("sph_levers", False) and getattr(self, "sph_plead", None) is not None:   # lead: the lives leading
            pn = self.sph_plead[..., C]                                                       # a sphere in town join its
            Ld = np.where(pn[..., None] > 0, (Ld * has[..., None] + LEAD_W * self.sph_plead[..., :C])   # leaders' mix
                          / np.maximum(has[..., None] + LEAD_W * pn[..., None], 1e-9), Ld)
            has = has | (pn > 0)
        Lg = 1 - np.exp(-s / pr["sL"])
        ds = (T["rho"][None, :, None] * Lg * (Dm - s) + pr["mu"] * self.sph_ds
              + pr["aH"] * np.minimum(age, 100)[..., None] / 50 * (self.sph_H - s)
              + has[..., None] * pr["aL"] * (1 + pr["kOl"] * corr)[..., None] * (Ld - s)
              + pr["aA"] * U[:, 2][:, None, None] * (0.2 - s))
        s_new = np.maximum(s + ds, pr["s_min"]); s_new /= s_new.sum(-1, keepdims=True)
        self.sph_ds = s_new - s; self.sph_s = s_new
        if self.p.get("sph_levers", False) and getattr(self, "sph_fund", None):          # a patron's pull on the sphere
            self._sph_fund_q(place=False)
        if self.p.get("sph_shadow", False):
            self._sph_shadow_q()
        self.sph_H += pr["H_mem"] * (s_new - self.sph_H)
        if self.p.get("sph_pairs", False):
            self._sph_pairs_q(T, s_new)
        # sizes: hours by epoch base, income, budget, the town's ages and technology; war and plague jump, a war's
        # rise partly kept
        Yr = _uclip(1 + 0.01 * self.gap - 0.01 * (self.loc_unemp - self.natural), 0.5, 2.0)
        lz = (T["eps"][None] * np.log(Yr)[:, None] + T["beta"][None] * (self.welfare - self.p["welfare0"])
              + (ages - self.sph_ref["ages"]) @ T["phi"].T - T["alpha"][None] * (auto - self.sph_ref["auto"])
              + T["zeta"][None] * (tech - self.sph_ref["tech"]))
        jump = np.ones(9); wj = pr["war_jump"]; pj = pr["plague_jump"]
        if self.war == 2:
            jump[T["war"][0]], jump[T["war"][1]] = wj["prot"], wj["rule"]
        if self.pandemic == 2:
            jump[T["plague"][0]], jump[T["plague"][1]] = pj["care"], pj["gather"]
        if self.war == 2:
            kept = 1 + wj["ratchet_kept"] * (jump - 1)
            self.sph_rat = np.maximum(self.sph_rat, np.where(np.arange(9) == T["war"][0], kept, np.where(np.arange(9) == T["war"][1], kept, 1.0)))
        mult = np.maximum(jump, self.sph_rat)
        Zs = T["base"][None] * mult[None] * np.exp(lz); Zs /= Zs.sum(1, keepdims=True)
        kz = np.where(jump > 1.0001, 0.25, pr["kZ"])                              # a war or plague moves hours within a year
        self.sph_Z = Z + kz[None] * (Zs - Z)

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 2
    def _sph_rng(self):
        """The spheres' own dice stream ("sphere", after the world's other streams; world-fields.md), made the first
        time a sphere rule draws, so every other stream draws as before and a world with the rules off saves as before."""
        k = len(self._STREAMS)
        if len(self.R) == k:
            self.R.append(np.random.default_rng([self._seed + 104729, k] + ([self.society_id] if self.society_id else [])))
        return self.R[k]

    def _sph_places_q(self):
        """N1: each town's named places, N_PLACES per haunt kind (31), each with a face mix that follows its sphere's mix
        in town at the sphere's own speed (rho), leaning its own lasting way (hp_off, drawn once: a place is like itself,
        never like every place of its kind). hp_nm: a name number the Library's place names are read by."""
        T = self._sph_tables(); nl = self.n_loc; H = len(HAUNT_KINDS)
        base = self.sph_s[:, HAUNT_SPH][:, :, None, :]                            # town x kind x 1 x 5
        if getattr(self, "hp_off", None) is None:
            r = self._sph_rng(); sd = float(T["pr"].get("place_sd", 0.6))
            self.hp_off = r.normal(0, sd, (nl, H, N_PLACES, C))[..., self.perm]   # drawn in W U B R G, held in this frame
            self.hp_nm = r.integers(0, 1000, (nl, H, N_PLACES))
            self.hp_s = base * np.exp(self.hp_off); self.hp_s /= self.hp_s.sum(-1, keepdims=True)
        tgt = base * np.exp(self.hp_off); tgt /= tgt.sum(-1, keepdims=True)
        rho = T["rho"][HAUNT_SPH][None, :, None, None]
        if self.p.get("sph_levers", False) and getattr(self, "hp_hold", None) is not None:   # loyalty slows a place
            q = int(self.t // 13)
            rho = rho * np.where(self.hp_hold[..., 0] >= q, self.hp_hold[..., 1], 1.0)[..., None]
        self.hp_s += rho * (tgt - self.hp_s)
        if self.p.get("sph_levers", False) and getattr(self, "sph_fund", None):          # a patron's pull on a place
            self._sph_fund_q(place=True)

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 4
    def _sph_nudge(self, mix, toward, k):
        """A face mix moved k of the way toward toward (0..1 shares), kept over the floor and summing to 1."""
        m = np.maximum(mix + k * (toward - mix), 0.005)
        return m / m.sum()

    def _sph_place_set(self, l, h, i, new):
        """A place's face mix set to new, its lasting lean (hp_off) moved with it, so the change stays."""
        old = self.hp_s[l, h, i]
        self.hp_off[l, h, i] += np.log(np.maximum(new, 1e-9)) - np.log(np.maximum(old, 1e-9))
        self.hp_s[l, h, i] = new

    def sph_lever(self, loc, j, place, lever, ma, size, rung, rng, office="budget"):
        """Phase 4 (sph_levers): a life's lever lands on its place (a flat place id, World.place_info) or, with place -1,
        on its town's sphere j (the caller passes the smaller size there). ma: the act's colours in this world's frame;
        size: reach / 3 x the rung's multiplier x how well it went; rung: 0 newcomer .. 4 leader. Returns what moved (a
        word) for the record. dynamics.json levers' on_the_mix, as Outer world's answers read them."""
        if size <= 0 or getattr(self, "sph_s", None) is None:
            return "none"
        loc = int(loc); j = int(j); q = int(self.t // 13); ma = np.asarray(ma, float)
        hp_ok = place >= 0 and getattr(self, "hp_s", None) is not None
        if hp_ok:
            l, h, i = (int(x) for x in np.unravel_index(int(place), self.hp_s.shape[:3]))
        nP = int((HAUNT_SPH == j).sum()) * N_PLACES                            # places of the sphere in town
        town = self.sph_s[loc, j]
        def on_place(k_, toward):
            if hp_ok:
                new = self._sph_nudge(self.hp_s[l, h, i], toward, k_)
                d_ = new - self.hp_s[l, h, i]; self._sph_place_set(l, h, i, new)
                self.sph_s[loc, j] = self._sph_nudge(town, town + d_, 1.0 / max(nP, 1))
            else:
                self.sph_s[loc, j] = self._sph_nudge(town, toward, k_)
        away = np.maximum(2 * (self.hp_s[l, h, i] if hp_ok else town) - ma, 0.0)
        away = away / max(away.sum(), 1e-9)
        if lever == "voice":
            on_place(0.03 * size, ma)
        elif lever == "subvert":
            if self.p.get("sph_shadow", False):                                   # N5: feeds its shadow side
                sh_ = self._sph_sh(); c_ = int(np.argmax(ma))
                sh_[loc, j, c_] = min(1.0, sh_[loc, j, c_] + self._sh_par()["subvert"] * size)
            if rng.random() < 0.4:                                               # backfires 4 in 10
                on_place(0.02 * size, away); return "backfired"
            on_place(0.03 * size, ma)
        elif lever == "neglect":
            on_place(0.02 * size, town)
        elif lever == "exit":
            on_place(0.01 * size, away)
            if rung >= 2 and hp_ok:                                               # a known face's leaving is felt
                lead_ = np.eye(C)[int(np.argmax(self.hp_s[l, h, i]))]
                self._sph_place_set(l, h, i, self._sph_nudge(self.hp_s[l, h, i], self.hp_s[l, h, i] - 0.02 * lead_ + 0.02 * town, 1.0))
        elif lever == "loyalty":
            if hp_ok:
                if getattr(self, "hp_hold", None) is None:
                    self.hp_hold = np.zeros(self.hp_s.shape[:3] + (2,)); self.hp_hold[..., 0] = -1
                self.hp_hold[l, h, i] = [q + 4, max(0.0, 1 - 0.1 * size)]
            else:
                return "none"
        elif lever == "found":
            top = np.argsort(-ma)[:2]
            face = np.zeros(C); face[top[0]] = 1.0
            if ma[top[1]] >= 0.26:                                                # a pair face: two colours of .26 or more
                face[top] = 0.5
            new = _norm(0.75 * face + 0.25 * town)
            hs_ = np.nonzero(HAUNT_SPH == j)[0]
            if getattr(self, "hp_s", None) is not None and len(hs_):
                if hp_ok and HAUNT_SPH[h] == j:
                    hs_ = np.array([h])
                cand = self.hp_s[loc, hs_].reshape(-1, C)                         # the place furthest from the founder
                k_ = int(np.argmax(np.abs(cand - new).sum(1)))
                h2, i2 = int(hs_[k_ // N_PLACES]), k_ % N_PLACES
                self._sph_place_set(loc, h2, i2, new)
            self.sph_s[loc, j] = self._sph_nudge(town, new, 1.0 / (nP + 1))
        elif lever == "fund":
            span = FUND_SPAN[min(int(rung), 4)]
            if span <= 0:
                return "none"
            if not hasattr(self, "sph_fund") or self.sph_fund is None:
                self.sph_fund = []
            onp = hp_ok and rung < 3                                              # a pillar's endowment: the town sphere
            self.sph_fund.append([loc, j, int(place) if onp else -1, [float(x) for x in ma], float(size), q + span])
        elif lever == "office":
            return self._sph_office(loc, j, office, size, rng)
        else:
            return "none"
        return "moved"

    def _sh_par(self):
        """N5's numbers (dynamics.json shadow_state.share: start, relax, event_row, subvert, fairness_gap, comm_grey)."""
        import sphere_data as SD
        return SD.SHADOW["share"]

    def _sph_sh(self):
        """N5's shadow shares (town x sphere x colour, 0..1; made at the start value the first time they are needed)."""
        if getattr(self, "sph_sh", None) is None:
            self.sph_sh = np.full((self.n_loc, 9, C), self._sh_par()["start"])
        return self.sph_sh

    def _sph_shadow_q(self):
        """Phase 5, N5 (sph_shadow), each quarter: every shadow share relaxes .02 of the gap toward .1 and moves .01 x
        (.5 - the town's felt-fairness target in that sphere): a sphere that fails people grows its shadow, fair
        enforcement and trust shrink it; comm's also move .01 x (comm.grey - .5) (shadow_state.share)."""
        sh = self._sph_sh(); pr = self._sh_par()
        d = pr["relax"] * (pr["start"] - sh) + pr["fairness_gap"] * (0.5 - self.sph_fair_target())[..., None]
        E = self._sph_ev_tables()
        if getattr(self, "sph_st", None) is not None and "comm.grey" in E["own"]:
            k_ = E["own"].index("comm.grey")
            g_ = np.clip(self.sph_st[:, k_] + self.sph_st_soc[k_] - 0.5, 0, 1)
            d[:, SPH["comm"]] += pr["comm_grey"] * (g_ - 0.5)[:, None]
        self.sph_sh = np.clip(sh + d, 0, 1)

    def sph_grey(self):
        """N5's grey share of each town's spheres (town x sphere): the face-weighted shadow share, no dice."""
        sh = self._sph_sh() if self.p.get("sph_shadow", False) else np.full((self.n_loc, 9, C), self._sh_par()["start"])
        return (self.sph_s * sh).sum(-1)

    def sph_state(self, key):
        """One sphere state for each town (n_loc,): the town's plus the society's for its own states, the world's for the
        16 world states; .5 where the sphere events are off (phase 5's debts read comm.credit and prot.order)."""
        import sphere_data as SD
        E = self._sph_ev_tables(); st = getattr(self, "sph_st", None)
        if key in E["own"]:
            if st is None:
                return np.full(self.n_loc, 0.5)
            k = E["own"].index(key)
            return _uclip(st[:, k] + self.sph_st_soc[k] - 0.5, 0, 1)
        return self._sph_world_states(E)[:, list(SD.STATE_WORLD).index(key)]

    def sph_fair_target(self):
        """Phase 4 (sph_fair): where each town's felt fairness in each sphere settles (n_loc x 9), before a life's own acts
        and rung: .5 + .3 x (the sphere's fair-hearing states - .5) - .3 x (its against states - .5); a sphere with no
        against state of its own reads rule.favour at .15 (dynamics.json felt_fairness; Tyler 1990). States are the town's
        plus the society's (own) or the world's (the 16 world states); without the sphere events, own states read .5."""
        import sphere_data as SD
        E = self._sph_ev_tables(); nl = self.n_loc
        st = getattr(self, "sph_st", None)
        own = _uclip(st + self.sph_st_soc[None] - 0.5, 0, 1) if st is not None else np.full((nl, len(E["own"])), 0.5)
        ws = self._sph_world_states(E)
        def val(k):
            if k in E["own"]:
                return own[:, E["own"].index(k)]
            return ws[:, list(SD.STATE_WORLD).index(k)]
        out = np.full((nl, len(SPHERES)), 0.5)
        for j, sp in enumerate(SPHERES):
            d = SD.FAIR["states"].get(sp, {})
            fr = [val(k) for k in d.get("fair", [])]
            ag = d.get("against") or []
            if fr:
                out[:, j] += 0.3 * (np.mean(fr, 0) - 0.5)
            out[:, j] -= (0.3 if ag else 0.15) * (np.mean([val(k) for k in (ag or ["rule.favour"])], 0) - 0.5)
        return out

    def _sph_fund_q(self, place):
        """The patrons' pulls this quarter (kPat .005 x size toward their colours), on places or on town spheres; a pull
        ends after its span."""
        q = int(self.t // 13)
        self.sph_fund = [f for f in self.sph_fund if f[5] >= q]
        for loc, j, p_, ma, size, _ in self.sph_fund:
            if place and p_ >= 0 and getattr(self, "hp_s", None) is not None:
                l, h, i = np.unravel_index(int(p_), self.hp_s.shape[:3])
                self._sph_place_set(l, h, i, self._sph_nudge(self.hp_s[l, h, i], np.asarray(ma), K_PAT * size))
            elif not place and p_ < 0:
                self.sph_s[loc, j] = self._sph_nudge(self.sph_s[loc, j], np.asarray(ma), K_PAT * size)

    def _sph_office(self, loc, j, kind, size, rng):
        """An office act on sphere j (kind ban, licence or budget; levers.office.events): with chance min(1, size) it
        fires that sphere's event for it in the town (its own rows; next quarter), or, where the sphere has none, moves
        the state by by x .05 x size."""
        import sphere_data as SD
        ent = SD.LEVER_OFFICE.get(SPHERES[j], {}).get(kind)
        if ent is None or rng.random() >= min(1.0, size):
            return "none"
        if "event" in ent:
            if not self.p.get("sph_events", False):
                return "none"
            self.fire_sphere_event(ent["event"], loc, big=False)
            return "fired " + ent["event"]
        E = self._sph_ev_tables()
        if ent["state"] in E["own"] and getattr(self, "sph_st", None) is not None:
            k_ = E["own"].index(ent["state"])
            self.sph_st[loc, k_] = min(1.0, max(0.0, self.sph_st[loc, k_] + ent["by"] * 0.05 * size))
            return "moved " + ent["state"]
        return "none"

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 3
    SPH_LAG = {"quarters": (1, 4), "a year": (3, 6), "years": (4, 20)}   # a chain's window, in quarters after its event

    def _sph_ev_tables(self):
        """The sphere events as arrays (made once, not saved): every event of sphere_data.EV, in its order (the Library's
        sphere_event: names an index here); its base chance a quarter (0 outside this world's epoch and for the
        world-fired events; else sph_ev_base for every event, the sph_par ev_base, or the fitted sphere_ev_base.BASE);
        hazard weights over the readers (the eight drivers, the hazard variables, the 74 sphere states; a bare state key
        is the event's own sphere's, else the one sphere that has it); the effect rows (a sphere's faces in this world's
        colour frame, and their steps on the sphere's own states); the chains; the world-fired events."""
        c_ = getattr(self, "_cache_sphev", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        try:
            from sphere_ev_base import BASE as FIT
        except ImportError:
            FIT = {}
        T = self._sph_tables(); pr = T["pr"]; ep = T["ep"]; EV = SD.EV; n = len(EV)
        key = {e["key"]: i for i, e in enumerate(EV)}
        cols = list(SD.DRIVERS) + list(SD.HAZARD_VARS) + list(SD.STATES); ci = {k: j for j, k in enumerate(cols)}
        def res(e, k):
            if k in ci:
                return k
            if f"{e['sphere']}.{k}" in ci:
                return f"{e['sphere']}.{k}"
            m_ = [s_ for s_ in SD.STATES if s_.split(".")[1] == k]
            return m_[0] if len(m_) == 1 else None
        b_ = self.p.get("sph_ev_base")
        tab = pr.get("ev_base") if isinstance(pr.get("ev_base"), dict) else {}
        fired = np.array([e.get("fired") is not None for e in EV])
        base = np.array([(float(b_) if b_ is not None else float(tab.get(e["key"], tab.get(e["family"], FIT.get(e["key"], 0.0)))))
                         * (ep in e["epochs"]) for e in EV]) * ~fired
        Hm = np.zeros((n, len(cols))); unread = []
        for i, e in enumerate(EV):
            for k, v in e["hazard"].items():
                r_ = res(e, k)
                if r_ is None:
                    unread.append((e["key"], k))
                else:
                    Hm[i, ci[r_]] += v
        own = [s_ for s_ in SD.STATES if s_ not in SD.STATE_WORLD or s_ == "rule.pressure"]   # (pressure: the world's Q only
        oi = {s_: j for j, s_ in enumerate(own)}                                                # with hist_pressure)
        rows = []
        for i, e in enumerate(EV):
            for r in e["rows"]:
                if r["target"] not in SPH:
                    continue                                   # a model domain's row: words only (answers item 3)
                f = np.zeros(C) if r["faces"] is None else np.asarray(r["faces"], float)[self.perm]
                st = [(oi[f"{r['target']}.{k}"], u) for k, u in r["state"].items() if f"{r['target']}.{k}" in oi]
                if f.any() or st:
                    rows.append((i, SPH[r["target"]], f, r["scope"] == "big", r["tau"], st))
        big = np.array([any(r["scope"] == "big" for r in e["rows"]) for e in EV])
        shrows = [(i, SPH[r["target"]], np.array([float(c_ in r["shadow"]) for c_ in COLORS])[self.perm], r["scope"] == "big")
                  for i, e in enumerate(EV) for r in e["rows"] if r.get("shadow") and r["target"] in SPH]   # N5's turns
        shsph = np.zeros((n, 9))
        for i_, j_, _, _ in shrows:
            shsph[i_, j_] = 1.0
        chains = [(i, key[k], *self.SPH_LAG.get(lag, self.SPH_LAG["years"])) for i, e in enumerate(EV)
                  for k, lag in e["chains"] if k in key]
        c_ = dict(n=n, key=key, names=[e["key"] for e in EV], base=base, cols=cols, Hm=Hm, unread=unread, dice=np.array([e["dice"] for e in EV]), big=big,
                  rows=rows, chains=chains, shrows=shrows, shsph=shsph / np.maximum(shsph.sum(1, keepdims=True), 1), sig=(float(pr.get("sig_local", 0.2)), float(pr.get("sig_big", 0.4))),
                  sph=np.array([SPH[e["sphere"]] for e in EV], np.int64), fired=fired, own=own,
                  wsi=[ci[s_] for s_ in SD.STATE_WORLD], osi=[ci[s_] for s_ in own], sr=dict(SD.STATE_RULE),
                  fam={(e["sphere"], e["family"]): [j for j, x in enumerate(EV) if (x["sphere"], x["family"]) == (e["sphere"], e["family"])]
                       for e in EV})
        self._cache_sphev = c_
        return c_

    def _sph_world_states(self, E):
        """The 16 sphere states that are world.py variables (dynamics.json events_run states.world_vars), per town, 0..1,
        in sphere_data.STATE_WORLD's order."""
        import sphere_data as SD
        nl = self.n_loc; p = self.p; b = lambda x_: np.broadcast_to(np.asarray(x_, float), (nl,))
        q_ = (float(self.Q) / max(2 * float(self.q_thr), 1e-9) if self._s3("hist_pressure") else None)
        ew = np.asarray(self.ext_war)
        rv = self.revival[1] > 0 if isinstance(self.revival, (tuple, list)) else False
        v = {"rule.trust": b(self.trust), "rule.purse": b(self.welfare), "rule.faction_heat": b(self.polar),
             "rule.favour": b(getattr(self, "corruption", 0.1)), "rule.say": b((self.regime + 10) / 20),
             "rule.pressure": None if q_ is None else b(q_), "prot.war": b(self.war / 2),
             "prot.order": 1 - np.asarray(self.loc_crime, float), "prot.threat": b(float((ew[1:] > 0).mean()) if len(ew) > 1 else 0.0),
             "comm.prices": b(0.5 + 0.05 * (self.infl - p["infl0"])), "care.outbreak": b(float(self.pandemic in (1, 2, 3))),
             "care.skill": b(self.medical), "prod.hands": 0.5 + (self.natural - np.asarray(self.loc_unemp, float)) / 20,
             "prod.stores": b(0.5 - self.food / 10), "faith.devotion": b(self.spiritual), "faith.fervour": b(0.5 + 0.3 * rv)}
        j_ = E["own"].index("rule.pressure")
        own = (self.sph_st[:, j_] + self.sph_st_soc[j_] - 0.5 if getattr(self, "sph_st", None) is not None
               else np.full(nl, 0.5))                                     # (phase 4's felt fairness reads without events)
        out = [own if (k == "rule.pressure" and v[k] is None) else v[k] for k in SD.STATE_WORLD]
        return _uclip(np.stack(out, 1), 0, 1)

    def _sph_hazard_x(self, E, e_need):
        """Each town's reading of every hazard reader (n_loc x len(cols)), clipped to -1..1: the drivers against the town's
        memory (as T), the hazard variables (drivers.vocabulary), the sphere states' level against their memory (own
        states: the town's plus the society's)."""
        import sphere_data as SD
        nl = self.n_loc; X = np.zeros((nl, len(E["cols"])))
        wl = (0.5 if self.war == 1 else 1.0 if self.war == 2 else 0.0) + 0.2 * float(np.any(np.asarray(self.ext_war) > 0))
        ob = float(self.pandemic in (1, 2, 3))
        hist = getattr(self, "sph_war4", None)
        hist = np.full((2, 4), [[wl], [ob]]) if hist is None or np.ndim(hist) == 1 else np.concatenate([hist[:, 1:], [[wl], [ob]]], 1)
        self.sph_war4 = hist
        nd = len(SD.DRIVERS); X[:, :nd] = self.sph_x
        hv = dict(war_drop=max(0.0, hist[0, 0] - wl), outbreak_drop=max(0.0, hist[1, 0] - ob),
                  disaster_now=np.minimum(np.asarray(self.loc_disaster, float), 1), meaning_gap=e_need[:, 2],
                  welfare=float(self.welfare) - float(self.p["welfare0"]),
                  old_share=self._sph_ages()[:, 2] - np.asarray(self.sph_ref["ages"], float)[:, 2])
        for j, k in enumerate(SD.HAZARD_VARS):
            X[:, nd + j] = hv.get(k, 0.0)
        lv = np.zeros((nl, len(SD.STATES)))
        k0 = nd + len(SD.HAZARD_VARS)
        lv[:, np.asarray(E["osi"]) - k0] = _uclip(self.sph_st + self.sph_st_soc[None] - 0.5, 0, 1)
        lv[:, np.asarray(E["wsi"]) - k0] = self._sph_world_states(E)
        if getattr(self, "sph_st_m", None) is None:
            self.sph_st_m = lv.copy()
        X[:, k0:] = lv - self.sph_st_m
        self.sph_st_m += E["sr"]["mem"] * (lv - self.sph_st_m)
        return _uclip(X, -1, 1)

    def fire_sphere_event(self, key, loc=-1, big=True):
        """A world rule fires sphere event key (bare, or "sphere.key") at the next quarter, in town loc (-1: where its
        hazard is highest; a big event acts for the whole society). big=False with a town keeps the event in that town,
        as for a world event that was not big. Nothing while sph_events is off."""
        if self.p.get("sph_events", False):
            if not hasattr(self, "sph_wq") or self.sph_wq is None:
                self.sph_wq = []
            self.sph_wq.append(["sphere", str(key).split(".")[-1], None, int(loc), -1, None, bool(big)])

    def _sph_wf_key(self, domain, kind, key, value):
        """The sphere event a world event fires (dynamics.json events_run world_fired; one key, one event), or None."""
        v = value if isinstance(value, dict) else {}
        if domain == "institution" and kind in ("closure", "scandal") and v.get("inst", -1) >= 0:
            i = int(v["inst"]); k_ = INST_KINDS[int(self.inst_kind[i])]; sp = int(self.inst_sphere[i])
            sec = int(self.inst_sector[i]) if self.inst_sector[i] >= 0 else -1
            if kind == "closure":
                if k_ == "bank":
                    return "lender_fails"
                if k_ == "employer" and sec in (SECTORS.index("farm"), SECTORS.index("industry")):
                    return "works_close"
                return (SPHERES[sp], "a_house_closes", v.get("loc", -1))
            if SPHERES[sp] == "rule":
                return "favour_exposed"
            if k_ == "faith body":
                return "scandal"
            if k_ in ("hospital", "charity"):
                return "neglect_scandal"
            if k_ == "bank" or (k_ == "employer" and sec == SECTORS.index("services")):
                return "swindle"
            return (SPHERES[sp], "trust_broken", v.get("loc", -1))
        if domain == "era" and kind == "breakthrough":
            return {"reform": "reform_wave", "revolution": "rising", "restoration": "restoration"}.get(key)
        if domain == "state" and kind == "law changed":
            return "drink_banned" if key == "alcohol" and v.get("state") == "banned" else None
        if domain == "tech" and kind == "arrives":
            return "new_medium" if key in ("phone", "internet", "video calls") else "new_tool"
        if domain == "nature" and kind == "pandemic":
            return "plague_wave" if key == "rising" else None
        if domain == "nature" and kind == "price shock":
            return "dearth" if key == "food" else None
        # the say and its rights (events_run world_fired, Outer world 10-10): speech or women's rights gained, or the
        # regime moving up, widen the say; a right lost in speech, faith, sexuality or women's rights, or the regime moving
        # down, narrows it, and only the fall seizes power (a lockdown's lost movement is neither)
        if domain == "state" and kind == "right gained":
            return "say_widened" if key in ("speech", "women") else None
        if domain == "state" and kind == "right lost":
            return "rights_narrowed" if key in ("speech", "faith", "sexuality", "women") else None
        if domain == "state" and kind == "regime changes":
            return {"up": "say_widened", "down": ["power_seized", "rights_narrowed"]}.get(v.get("state"))
        if domain == "nature" and kind == "drought":        # C4 (c4_nature)
            return "lean_year"
        if domain == "nature" and kind == "glorious spring":   # C4: in farming places
            l_ = int(v.get("loc", -1))
            ok_ = 0 <= l_ < self.n_loc and "farming" in FEATURES and bool(self.loc_feat[l_, FEATURES.index("farming")])
            return "rich_season" if ok_ else None
        if domain == "figure" and kind == "falls":
            return "star_falls" if key in ("star", "athlete") else None
        return {("belief", "revival"): "faith_revival", ("place", "crime wave"): "crime_wave",
                ("nature", "disaster"): "disaster_strikes", ("abroad", "war begins"): "call_up",
                ("abroad", "war ends"): "peace_made",
                ("institution", "budget cut"): "hands_short"}.get((domain, kind))

    def _sph_events_q(self, e_need):
        """Phase 3 (sph_events): this quarter's sphere events and the fading demand shifts of all that fired
        (dynamics.json face_mix "Events (X)": sig x faces x exp(-quarters / tau)). Each event's chance a quarter is its
        base x exp(hazard . readings) x 3 inside a chain's window (x the season's hazard with sph_seasons); a big event
        is one draw for the society. Dice only for events with dice (a hashed draw by world seed and quarter, so no
        stream moves); the rest add their chance each quarter and fire when the sum reaches 1, which goes back to 0
        (item 14: the same start, the same history). The world-fired events fire with the world's own (queued by _event
        since the last quarter). The sphere states relax toward .5. Returns X (n_loc x 9 x 5)."""
        E = self._sph_ev_tables(); nl = self.n_loc; n = E["n"]; q = int(self.t // 13); sr = E["sr"]
        if getattr(self, "sph_ev_last", None) is None:
            self.sph_ev_last = np.full((nl, n), -10 ** 6, np.int64)   # the week each event last fired in each town
            self.sph_ev_acc = np.zeros((nl, n)); self.sph_ev_win = np.zeros((nl, n, 2), np.int64)
            self.sph_ev_rows = np.zeros((0, 4 + C))                     # town, sphere, start quarter, tau, then sig x faces
            self.sph_ev_log = np.zeros((0, 3), np.int64)                # week, event, town (-1: the whole society)
            self.sph_st = np.full((nl, len(E["own"])), sr["start"]); self.sph_st_soc = np.full(len(E["own"]), sr["start"])
        xv = self._sph_hazard_x(E, e_need)
        p = E["base"][None] * np.exp(xv @ E["Hm"].T)
        w_ = self.sph_ev_win; p = p * np.where((w_[..., 0] <= q) & (q <= w_[..., 1]), 3.0, 1.0)
        if self.p.get("sph_seasons", False):   # N7: the season in the middle of the coming quarter
            p = p * self._sph_tables()["seas_z"][E["sph"], WEEK_SEASON[(self.t + 7) % 52]][None]
        if self.p.get("sph_memory", False) or self.p.get("pair_calm", False) or self.p.get("sph_cascades", False):
            p = p * self._sph_p3_factor(E, q, w_)
        if self.p.get("sph_shadow", False) and getattr(self, "sph_sh", None) is not None:   # N5: a grey sphere's shadow events
            p = p * np.exp(self.sph_grey() @ E["shsph"].T - self._sh_par()["start"] * (E["shsph"].sum(1) > 0)[None])
        self._cache_evh = np.exp(xv @ E["Hm"].T)                                         # for where a big event's local
        on = E["base"] > 0                                                               # rows act (not saved)
        if on.any():
            p = np.where(E["big"][None], p.mean(0, keepdims=True), p)                       # one chance for the society
            r = np.random.default_rng([self._seed + 7919, q]).random((nl, n))
            r[:, E["big"]] = r[:1, E["big"]]
            self.sph_ev_acc += np.where(E["dice"][None], 0.0, p)
            fire = on[None] & np.where(E["dice"][None], r < p, self.sph_ev_acc >= 1.0)
            self.sph_ev_acc = np.where(fire & ~E["dice"][None], 0.0, self.sph_ev_acc)
            fire[1:, E["big"]] = False                                                       # a big event fires once
            for l, i in zip(*np.nonzero(fire)):
                self._sph_fire(int(l), int(i), q, E)
        for dom, kind, k_, lc_, in_, st_, *bg_ in (getattr(self, "sph_wq", None) or []):   # the world-fired events
            ek = kind if dom == "sphere" else self._sph_wf_key(dom, kind, k_, dict(inst=in_, loc=lc_, state=st_) if in_ >= 0 else dict(loc=lc_, state=st_))
            if isinstance(ek, tuple):                                    # a house closes, trust broken: the sphere's own
                cand = E["fam"].get((ek[0], ek[1]), [])                  # event of that family with the highest hazard
                l_ = ek[2] if 0 <= ek[2] < nl else None
                h_ = self._cache_evh[l_ if l_ is not None else slice(None)]
                ek = E["names"][cand[int(np.argmax(np.atleast_2d(h_)[:, cand].mean(0)))]] if cand else None
            for ek in (ek if isinstance(ek, list) else [ek]):
                if ek is None or ek not in E["key"]:
                    continue
                i = E["key"][ek]; l = int(lc_) if 0 <= lc_ < nl else int(np.argmax(self._cache_evh[:, i]))
                here_ = 0 <= lc_ < nl
                self._sph_fire(l, i, q, E, here=here_, local=here_ and not (bg_[0] if bg_ else True))   # a town's own news

        self.sph_wq = []; self.sph_reg_seen = float(self.regime)
        if self.p.get("sph_memory", False):
            self.sph_mem = np.maximum(self._sph_mem() - self._sph_p3_tables()["fade"], 0.0)
        self.sph_st += sr["relax"] * (sr["start"] - self.sph_st); self.sph_st_soc += sr["relax"] * (sr["start"] - self.sph_st_soc)
        # the fading shifts of every row still acting
        R_ = self.sph_ev_rows; X = np.zeros((nl, 9, C))
        if len(R_):
            age = q - R_[:, 2]; k = np.exp(-age / R_[:, 3])
            keep = k >= 0.01; R_ = self.sph_ev_rows = R_[keep]; k = k[keep]
            np.add.at(X, (R_[:, 0].astype(np.intp), R_[:, 1].astype(np.intp)), R_[:, 4:] * k[:, None])
        return X

    SPH_LINK_LAG = {"weeks": 1, "months": 1, "quarters": 2, "years": 8, "decades": 40}   # a link's lag, in quarters

    def _sph_link_tables(self):
        """The 72 sphere-to-sphere links as arrays (made once, not saved): A (link x the 74 states) averages each link's
        from-states, signed; B (link x own state) is each to-state's step per unit, signed, x strength / 3 (to-states
        that are world.py variables are left alone: words only, as the events' domain rows); rate, 1 / the lag in
        quarters; F (link x sphere x face), the colour readings: + feeds, - starves on the link's low side, x strength / 3,
        in this world's colour frame."""
        c_ = getattr(self, "_cache_sphlk", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        E = self._sph_ev_tables(); si = {k: j for j, k in enumerate(SD.STATES)}; oi = {k: j for j, k in enumerate(E["own"])}
        nL = len(SD.LINKS); A = np.zeros((nL, len(SD.STATES))); B = np.zeros((nL, len(E["own"]))); F = np.zeros((nL, 9, C))
        lid = {l["id"]: j for j, l in enumerate(SD.LINKS)}
        for j, l in enumerate(SD.LINKS):
            for k, sg in l["src"]:
                A[j, si[k]] += sg / len(l["src"])
            for k, sg in l["dst"]:
                if k in oi:
                    B[j, oi[k]] += sg * l["strength"] / 3
        for r in SD.LINK_COLOUR:
            f = np.array([(c in r["feeds"]) - (c in r["starves"]) for c in COLORS], float)[self.perm]
            F[lid[r["link"]], SPH[r["faces_in"]]] += (1 if r["side"] == "low" else -1) * r["strength"] / 3 * f
        rate = np.array([1.0 / self.SPH_LINK_LAG.get(l["lag"], 8) for l in SD.LINKS])
        c_ = self._cache_sphlk = dict(A=A, B=B, F=F, rate=rate, osi=[si[k] for k in E["own"]], wsi=[si[k] for k in SD.STATE_WORLD])
        return c_

    def _sph_links_q(self):
        """Phase 3 (sph_links): each link's input is the mean of its from-states' levels minus .5 (signed, "(down)"
        turned), lagged (it moves 1 / lag of the way a quarter, from 0); each to-state of the sphere's own steps
        link_k x strength / 3 x the lagged input a quarter (link_k .01: the links' loop gain, .0138 at most, stays under
        the states' relax of .02); the colour readings shift demand by link_c x strength / 3 x the lagged input, the low
        side feeding the row's feeds and starving its starves (the high side the other way round). Returns the X shift
        (n_loc x 9 x 5)."""
        E = self._sph_ev_tables(); Lk = self._sph_link_tables(); pr = self._sph_tables()["pr"]; nl = self.n_loc
        lv = np.zeros((nl, Lk["A"].shape[1]))
        lv[:, Lk["osi"]] = _uclip(self.sph_st + self.sph_st_soc[None] - 0.5, 0, 1)
        lv[:, Lk["wsi"]] = self._sph_world_states(E)
        x = (lv - 0.5) @ Lk["A"].T
        if getattr(self, "sph_lk", None) is None:
            self.sph_lk = np.zeros_like(x)
        self.sph_lk += Lk["rate"][None] * (x - self.sph_lk)
        self.sph_st = np.clip(self.sph_st + float(pr.get("link_k", 0.01)) * (self.sph_lk @ Lk["B"]), 0, 1)   # as events do
        return -float(pr.get("link_c", 0.3)) * np.einsum("ln,njc->ljc", self.sph_lk, Lk["F"])

    CAS_LAG = {"quarters": (1, 4), "a year or two": (4, 8), "years": (4, 20), "decades": (20, 60)}   # a cascade step's
    # window after the step before, in quarters ("a year or two": about 6 quarters, Outer world's answer 5)

    def _sph_p3_tables(self):
        """The memories, the pairs' quarrels and the cascades as arrays (made once, not saved): MF (event x memory) what
        each firing adds, MR (memory x event) each memory's pull on each hazard, fade; PQ (pair x event) the quarrel
        events of each pair (a pair face calms its own sphere's: every event is its own sphere's); the cascades with
        their steps as event indices (a step whose event cannot happen in this world's epoch passes time, as a step with
        no event does)."""
        c_ = getattr(self, "_cache_sphp3", None)
        if c_ is not None:
            return c_
        import sphere_data as SD
        E = self._sph_ev_tables(); n = E["n"]; key = E["key"]; ep = self._sph_tables()["ep"]
        mems = list(SD.MEMORIES); MF = np.zeros((n, len(mems))); MR = np.zeros((len(mems), n))
        for m_, nm in enumerate(mems):
            for k, a in SD.MEMORIES[nm]["feeds"].items():
                MF[key[k], m_] += a
            for k, a in SD.MEMORIES[nm]["raises"].items():
                MR[m_, key[k]] += a
        PQ = np.zeros((len(SPH_PAIRS), n), bool)
        for j, pr_ in enumerate(SPH_PAIRS):
            for k in SD.PAIR_QUARRELS.get(pr_, []):
                PQ[j, key[k]] = True
        runs = (E["base"] > 0) | E["fired"]
        cas = []
        for c in SD.CASCADES:
            if ep not in c["epochs"]:
                continue
            st = [(key[k] if k is not None and runs[key[k]] else -1, lag) for k, lag in c["steps"]]
            if st and st[0][0] >= 0:
                cas.append(st)
        c_ = self._cache_sphp3 = dict(MF=MF, MR=MR, fade=float(SD.MEM_FADE), PQ=PQ, cas=cas,
                                      cas_first={st[0][0]: k for k, st in enumerate(cas)})
        return c_

    def _sph_mem(self):
        if getattr(self, "sph_mem", None) is None:
            self.sph_mem = np.zeros((self.n_loc, self._sph_p3_tables()["MF"].shape[1]))
        return self.sph_mem

    def _sph_p3_factor(self, E, q, w_):
        """This quarter's hazard factor per town and event (n_loc x n) from the memories (sph_memory: exp(memory . size)),
        the pair faces' calm (pair_calm: while a pair face holds over .1, x (1 - 2 x held), at least .5, on its sphere's
        quarrel events; a pair face that broke, x 1.5 for 8 quarters) and the running cascades (sph_cascades: x 3 on the
        next step's event inside its window, not on top of a chain's own x 3)."""
        P3 = self._sph_p3_tables(); nl = self.n_loc; f = np.ones((nl, E["n"]))
        if self.p.get("sph_memory", False):
            f = f * np.exp(self._sph_mem() @ P3["MR"])
        if self.p.get("pair_calm", False) and self.p.get("sph_pairs", False) and getattr(self, "sph_ph", None) is not None:
            h = self.sph_ph[:, E["sph"], :]                                        # town x event x pair: its sphere's
            calm = np.where(h > 0.1, np.maximum(1 - 2 * h, 0.5), 1.0)
            brk = getattr(self, "sph_pbrk", None)
            if brk is not None:
                calm = calm * np.where(brk[:, E["sph"], :] >= q, 1.5, 1.0)
            f = f * np.prod(np.where(P3["PQ"].T[None], calm, 1.0), axis=2)
        if self.p.get("sph_cascades", False) and getattr(self, "sph_cas", None):
            inch = (w_[..., 0] <= q) & (q <= w_[..., 1])                          # already x 3 by a chain
            for c, loc, k, lo, hi in self.sph_cas:
                i = P3["cas"][c][k][0]
                if lo <= q <= hi:
                    rows = slice(None) if loc < 0 else loc
                    f[rows, i] = np.where(inch[rows, i], f[rows, i], f[rows, i] * 3.0)
            self.sph_cas = [x for x in self.sph_cas if q <= x[4]]                  # a window passed: it ends
        return f

    def _sph_p3_fired(self, l, i, q, E, loc):
        """Event i fired (in town loc; -1 the whole society): it feeds or drains the memories (sph_memory; a society's
        event in every town), moves on the cascades waiting for it, and starts the cascade it begins (sph_cascades; one
        of each per town or society at a time)."""
        P3 = self._sph_p3_tables()
        if self.p.get("sph_memory", False) and P3["MF"][i].any():
            m = self._sph_mem(); rows = slice(None) if loc < 0 else loc
            m[rows] = np.clip(m[rows] + P3["MF"][i], 0, 1)
        if self.p.get("sph_cascades", False):
            cas = getattr(self, "sph_cas", None) or []
            out = []
            for c, lc, k, lo, hi in cas:
                st = P3["cas"][c]
                if st[k][0] == i and lo <= q <= hi and (lc < 0 or loc < 0 or lc == loc):
                    nxt = self._sph_cas_next(st, k + 1, q)
                    if nxt is not None:
                        out.append([c, lc, *nxt])
                else:
                    out.append([c, lc, k, lo, hi])
            c0 = P3["cas_first"].get(i)
            if c0 is not None and not any(x[0] == c0 and x[1] == loc for x in out):
                nxt = self._sph_cas_next(P3["cas"][c0], 1, q)
                if nxt is not None:
                    out.append([c0, int(loc), *nxt])
            self.sph_cas = out

    def _sph_cas_next(self, st, k, q):
        """The cascade's next step with an event from step k, and its window [lo, hi] in quarters (a step with no event,
        or one that cannot happen here, passes its own lag), or None at the end."""
        lo, hi = q, q
        while k < len(st):
            a, b = self.CAS_LAG.get(st[k][1], self.CAS_LAG["years"])
            lo, hi = lo + a, hi + b
            if st[k][0] >= 0:
                return [k, lo, hi]
            k += 1
        return None

    def _sph_pairs_q(self, T, s):
        """Phase 3 (sph_pairs): the ten pair faces of each town sphere (dynamics.json pair_faces). A pair's strength pi
        rises pair_rise a quarter while both its faces have held pair_share of the sphere for pair_quarters running, or
        while a body leading the sphere in town has a leader holding both colours at pair_person or more (then at once
        to .5 at least); it falls pair_decay a quarter otherwise. The pair holds pi x min(s1, s2), taken equally from
        both faces (the five shares stay; sph_ph is the layer people's teaching reads). The same thresholds for all ten
        pairs, ally and enemy alike (Canon rule 4). Later: the quarrel calm (pair_calm), its entry into the memory H after
        five strong years, and the faster fade after its founder leaves."""
        pr = T["pr"]; nl = self.n_loc; i1, i2 = T["pair_i"][:, 0], T["pair_i"][:, 1]
        if getattr(self, "sph_pi", None) is None:
            self.sph_pi = np.zeros((nl, 9, len(SPH_PAIRS))); self.sph_pq = np.zeros((nl, 9, len(SPH_PAIRS)), np.int64)
        s1, s2 = s[..., i1], s[..., i2]                                            # town x sphere x pair
        ok = (s1 >= pr["pair_share"]) & (s2 >= pr["pair_share"])
        self.sph_pq = np.where(ok, self.sph_pq + 1, 0)
        lp = self.inst_leader_pie                                                 # a two-coloured leader of a body here
        two = (lp[:, i1] >= pr["pair_person"]) & (lp[:, i2] >= pr["pair_person"])   # institution x pair
        il = np.asarray(self.inst_loc); isp = self.inst_sphere; on_ = (il >= 0) & (il < nl) & (isp >= 0)
        lead = np.zeros((nl, 9, len(SPH_PAIRS)), bool)
        np.logical_or.at(lead, (il[on_], isp[on_]), two[on_])
        cond = (self.sph_pq >= pr["pair_quarters"]) | lead
        pi = np.clip(np.where(cond, self.sph_pi + pr["pair_rise"], self.sph_pi - pr["pair_decay"]), 0, 1)
        self.sph_pi = np.where(lead, np.maximum(pi, 0.5), pi)
        if self.p.get("pair_calm", False):   # a pair face that held .5 or more and fell under .2 broke (8 quarters' flare)
            if getattr(self, "sph_ppk", None) is None:
                self.sph_ppk = np.zeros_like(self.sph_pi); self.sph_pbrk = np.full(self.sph_pi.shape, -1, np.int64)
            broke = (self.sph_pi < 0.2) & (self.sph_ppk >= 0.5)
            self.sph_pbrk = np.where(broke, int(self.t // 13) + 8, self.sph_pbrk)
            self.sph_ppk = np.where(self.sph_pi < 0.2, 0.0, np.maximum(self.sph_ppk, self.sph_pi))
        h = self.sph_pi * np.minimum(s1, s2)
        take = np.einsum("ljp,pc->ljc", h, T["pairA"])                            # what each face gives to its pairs
        f = np.minimum(1.0, s / np.maximum(take, 1e-12))                          # never more than the face holds
        self.sph_ph = h * np.minimum(f[..., i1], f[..., i2])

    def sph_teach_mix(self, town, teach):
        """The teaching mix of town spheres (n x 9 x 5 face shares, read through the per-sphere teach matrices), with the
        pair faces' layer when sph_pairs is on: what a pair holds leaves its two faces and teaches .4 of each of its two
        colours and .2 spread over the other three (dynamics.json pair_faces "does")."""
        tm = np.einsum("njf,jfc->njc", town[0], teach)
        if town[1] is None:
            return tm
        T = self._sph_tables(); ph = town[1]
        adj = town[0] - np.einsum("njp,pc->njc", ph, T["pairA"])
        return np.einsum("njf,jfc->njc", adj, teach) + 2 * np.einsum("njp,pc->njc", ph, T["pairT"])

    def _sph_fire(self, l, i, q, E, here=False, local=False):
        """Event i fires in town l (a big event: for the whole society): its rows start acting and step the sphere's own
        states (a big row on the society's, in every town; a local row on the town's: town l, or for an event with a big
        row the top third of towns by its hazard, at least one), its chains open their windows, the log and the
        last-fired table take it. here: a world-fired event with a town of its own (its local rows act there); local: the
        world's event was not big (every row acts in that town only, and only that town's moments open)."""
        nl = self.n_loc; sr = E["sr"]
        if self.p.get("sph_memory", False) or self.p.get("sph_cascades", False):
            self._sph_p3_fired(l, i, q, E, l if (local or not E["big"][i]) else -1)
        if local:                 # a world event that stays in its town (a local body's closure or scandal, a town's
            loc_t = every = np.array([l])                     # crime wave): every row acts there, as a local row
        elif E["big"][i]:
            k_ = max(1, int(np.ceil(nl / 3)))
            loc_t = np.array([l]) if here else np.argsort(-self._cache_evh[:, i], kind="stable")[:k_]
            every = np.arange(nl)
        else:
            loc_t = every = np.array([l])
        add = []
        for (ei, j, f, bg, tau, st) in E["rows"]:
            if ei != i:
                continue
            bg = bg and not local
            towns = every if bg else loc_t
            if f.any():
                add += [np.concatenate([[t_, j, q, tau], (E["sig"][1] if bg else E["sig"][0]) * f]) for t_ in towns]
            for s_, u_ in st:
                if bg:
                    self.sph_st_soc[s_] = min(1.0, max(0.0, self.sph_st_soc[s_] + sr["step"] * u_))
                else:
                    self.sph_st[towns, s_] = np.clip(self.sph_st[towns, s_] + sr["step"] * u_, 0, 1)
        if add:
            self.sph_ev_rows = np.vstack([self.sph_ev_rows, np.array(add)])
        if self.p.get("sph_shadow", False):   # N5: the row's shadow colours turn toward their shadow side there
            sh_ = self._sph_sh(); k_ = self._sh_par()["event_row"]
            for (ei, j, v, bg) in E["shrows"]:
                if ei == i:
                    tw_ = every if (bg and not local) else loc_t
                    sh_[tw_, j] = np.minimum(1.0, sh_[tw_, j] + k_ * v)
        for (a, b, lo, hi) in E["chains"]:
            if a == i:
                self.sph_ev_win[every, b, 0] = q + lo; self.sph_ev_win[every, b, 1] = q + hi
        self.sph_ev_last[every, i] = int(self.t)
        self.sph_ev_log = np.vstack([self.sph_ev_log, [[int(self.t), i, -1 if E["big"][i] and not local else l]]])

    def place_info(self, p):
        """A named place (flat index town x kind x N_PLACES, as People.hnt holds it): its town, kind, sphere, name number,
        five face shares (W U B R G) and leading face. Public, as the town portrait is."""
        import sphere_data as SD
        l, h, i = np.unravel_index(int(p), (self.n_loc, len(HAUNT_KINDS), N_PLACES))
        f = self.hp_s[l, h, i][np.argsort(self.perm)]; c = int(np.argmax(f)); sp = SPHERES[HAUNT_SPH[h]]
        return dict(place=int(p), town=int(l), kind=HAUNT_KINDS[h], sphere=sp, name=int(self.hp_nm[l, h, i]),
                    faces=[round(float(x), 3) for x in f], leads=f"{sp}.{COLORS[c]}", leads_name=SD.FACE_NAMES[f"{sp}.{COLORS[c]}"])

    # ------------------------------------------------------------------ the spheres of society (item 15): Replace
    @property
    def inst_sphere(self):
        """Each institution's sphere (index into SPHERES); an employer by its sector (no sector: commerce)."""
        sph = INST_SPH[self.inst_kind]
        sec = np.asarray(self.inst_sector)
        return np.where(sph >= 0, sph, SECTOR_SPH[np.where(sec >= 0, sec, SECTORS.index("services"))])

    @property
    def sph_epoch(self):
        """The spheres' epoch for this world's setting (modern days for Earth)."""
        return self.SPH_EPOCH.get(self.cfg.get("setting", "earth"), "modern")

    EV_SPHERE = {("belief", None): "faith", ("era", None): "rule", ("place", "crime wave"): "prot",
                 ("place", None): "rule", ("nature", "pandemic"): "care", ("nature", "disaster"): "prot",
                 ("nature", None): "comm", ("abroad", "refugees arrive"): "gather", ("abroad", "world recession"): "comm",
                 ("abroad", None): "prot", ("state", None): "rule", ("economy", None): "comm", ("tech", None): "prod",
                 ("figure", None): "rule", ("culture", None): "gather"}

    def event_sphere(self, e):
        """The sphere a world event belongs to (item 15, phase 1d; spheres-implementation.md section 5, "Sphere events
        onto the world's events"): an institution's by its sphere, a law on drink in gathering, else by its domain and
        kind. Read only: the event itself is not changed. None for a domain with no sphere."""
        d, k = e.get("domain"), e.get("kind")
        if d == "institution":
            i = (e.get("value") or {}).get("inst") if isinstance(e.get("value"), dict) else None
            return SPHERES[int(self.inst_sphere[i])] if i is not None and 0 <= i < len(self.inst_kind) else None
        if d == "state" and k == "law changed" and e.get("key") == "alcohol":
            return "gather"
        return self.EV_SPHERE.get((d, k), self.EV_SPHERE.get((d, None)))

    def sphere_insts(self, sphere):
        """The institutions of one sphere (a name or an index), in their stored order."""
        return np.nonzero(self.inst_sphere == (SPH[sphere] if isinstance(sphere, str) else int(sphere)))[0]

    def state_parts(self, sphere=None):
        """The state by part ({part: {field: value}}), all parts or one sphere's; the force is that sphere's police
        and army, read with sphere_insts."""
        return {k_: {f_: getattr(self, f_) for f_ in STATE_PARTS[k_]} for k_, s_ in STATE_SPHERE.items()
                if sphere is None or s_ == sphere}

    # the arrays world-build.md names, as views of the state
    def snapshot(self):
        """The public state for the world panel: never pressure, hazards or odds (Emren 10:09)."""
        figs = [dict(id=i, female=bool(self.F_female[i]), born_t=int(self.F_born[i]), role=FIG_ROLES[self.F_role[i]],
                     party=int(self.F_party[i]), standing=round(float(self.F_standing[i]), 2), alive=bool(self.F_alive[i]))
                for i in sorted(set(self.fig_role_now.values()))]
        last = {}
        for e in reversed(self.record):
            if e["kind"] == "published" and e["key"] not in last:
                last[e["key"]] = e["value"]
            if len(last) == 2:
                break
        return dict(t=int(self.t), week_of_year=int(self.week_of_year), season=SEASONS[self.season],
                    era=None if self.era_key is None else dict(key=self.era_key, kind=ERA_KINDS[self.era_k],
                                                              idea=IDEAS[self.era_key][0], since_t=int(self.era_since)),
                    econ=dict(phase_published="recession" if self.rec_declared else "expansion",
                              unemp=last.get("unemployment"), infl=last.get("inflation"), housing=round(float(self.housing), 1)),
                    gov=dict(colors=[round(float(v), 2) for v in self.G], leader=int(self.fig), party=int(self.gov_party),
                             support=round(float(self.support), 2), next_election_t=int(self.t + 13 * self.next_vote)),
                    laws={k: LAW_STATES[int(s)] for k, s in zip(LAW_KEYS, self.laws)}, welfare=round(float(self.welfare_pub), 2),
                    rights={k: round(float(v), 1) for k, v in zip(RIGHTS, self.rights)}, war=WAR_STATES[self.war],
                    pandemic=PANDEMIC[self.pandemic], norms={k: float(v) for k, v in zip(NORM_KEYS, self.norm_pub)},
                    faiths=[round(float(v), 2) for v in self.faith_share], secular=round(float(self.secular), 2),
                    tech={k: round(float(a), 2) for k, a, e in zip(self.tech_keys, self.tech_adopt_v, self.tech_exists) if e},
                    figures=figs, regime="democracy" if self.regime >= 6 else "autocracy" if self.regime < -5 else "mixed",
                    **({"spheres": self._sph_portrait()} if getattr(self, "sph_s", None) is not None else {}))

    def _sph_portrait(self):
        """The town portrait (item 15, N3), public: per town each sphere's share of the hours and its five face shares
        (W U B R G, the canonical order), with the leading face. Never the pressures, drivers or hazards behind them."""
        import sphere_data as SD
        inv = np.argsort(self.perm); out = []
        for l in range(self.n_loc):
            sp = {}
            for j, s_ in enumerate(SPHERES):
                f = self.sph_s[l, j][inv]; c = int(np.argmax(f))
                sp[s_] = dict(hours=round(float(self.sph_Z[l, j]), 3), faces=[round(float(x), 3) for x in f],
                              leads=f"{s_}.{COLORS[c]}", leads_name=SD.FACE_NAMES[f"{s_}.{COLORS[c]}"])
            out.append(dict(town=int(l), spheres=sp))
        return out

    # ------------------------------------------------------------------------------------------------ save and load
    def save(self):
        """JSON-safe dict of the whole state (lists, floats, ints, strings); World.load(d) continues identically."""
        st = {}
        for k, v in self.__dict__.items():
            if k in self._CONST or k.startswith("_cache"):
                continue
            if isinstance(v, np.ndarray):
                st[k] = {"__nd__": str(v.dtype), "shape": list(v.shape), "data": v.reshape(-1).tolist()}
            elif isinstance(v, (np.floating, np.integer, np.bool_)):
                st[k] = v.item()
            elif isinstance(v, dict) and k == "fig_role_now":
                st[k] = {"__intkeys__": [[int(a), int(b)] for a, b in v.items()]}
            elif isinstance(v, tuple):
                st[k] = {"__tuple__": _jsafe(list(v))}
            elif isinstance(v, list) and v and isinstance(v[0], np.ndarray):
                st[k] = {"__ndlist__": [x.tolist() for x in v]}
            else:
                st[k] = _jsafe(v)
        rng = []
        for g in self.R:
            s = g.bit_generator.state
            rng.append(dict(bit_generator=s["bit_generator"], state={a: str(b) for a, b in s["state"].items()},
                            has_uint32=int(s["has_uint32"]), uinteger=str(s["uinteger"])))
        cfg, par = {k: v for k, v in self.cfg.items() if k != "legacy"}, dict(self.p)
        if not any(self.p.get(k, False) for k in SPH_RULES):   # spheres off: saved as v22.2 saved it
            par = {k: v for k, v in par.items() if k not in SPH_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in SPH_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self.p.get(k) for k in C_RULES):        # the C hooks off: saved without them
            par = {k: v for k, v in par.items() if k not in C_RULES}
            if "params" in cfg:
                cfg = dict(cfg, params={k: v for k, v in cfg["params"].items() if k not in C_RULES})
                if not cfg["params"]:
                    cfg.pop("params")
        if not any(self._s3(k) for k in S3_RULES):        # stage 3 off: saved as v22.1 saved it (load restores them)
            par = {k: v for k, v in par.items() if k not in S3_RULES + S3_PARAMS}
            cp_ = {k: v for k, v in (cfg.get("params") or {}).items() if k not in S3_RULES + S3_PARAMS}
            cfg = {k: v for k, v in cfg.items() if k != "params"}
            if cp_:
                cfg["params"] = cp_
        return dict(version=1, seed=self._seed, society=int(self.society_id), cfg=_jsafe(cfg),
                    params=_jsafe(par), perm=self.perm.tolist(), rng=rng, state=st)

    @classmethod
    def load(cls, d):
        params = dict(d["params"])
        for k in S3_RULES + SPH_RULES:                     # saved before stage 3 or the spheres: their rules stay off
            params.setdefault(k, False)
        for k in C_RULES:                                  # saved before the C hooks: they stay off
            params.setdefault(k, None if k == "c_par" else False)
        W = cls(d["seed"], cfg=d["cfg"], color_perm=d["perm"], params=params, society=d.get("society", 0))
        for k, v in d["state"].items():
            if isinstance(v, dict) and "__nd__" in v:
                v = np.array(v["data"], dtype=v["__nd__"]).reshape(v["shape"])
            elif isinstance(v, dict) and "__intkeys__" in v:
                v = {int(a): int(b) for a, b in v["__intkeys__"]}
            elif isinstance(v, dict) and "__tuple__" in v:
                v = tuple(v["__tuple__"])
            elif isinstance(v, dict) and "__ndlist__" in v:
                v = [np.array(x) for x in v["__ndlist__"]]
            setattr(W, k, v)
        if len(d["rng"]) > len(W.R):                       # the spheres' stream, once a sphere rule has drawn
            W._sph_rng()
        for g, s in zip(W.R, d["rng"]):
            g.bit_generator.state = dict(bit_generator=s["bit_generator"], state={a: int(b) for a, b in s["state"].items()},
                                         has_uint32=s["has_uint32"], uinteger=int(s["uinteger"]))
        if getattr(W, "c5_prof", None) is not None:      # C5: the movements' colours (FPROF is rebuilt, not saved)
            W.FPROF[NF:] = W.c5_prof
        if "clim_t0" not in d["state"] and W.t > 0:        # saved before the climate anchor was kept: freeze it
            W.clim_t0 = int(W.t0)
        return W


SEC_REF = 0.86   # the typical security of the young in a rich democracy (the long-run mean of World.security(); estimate)
