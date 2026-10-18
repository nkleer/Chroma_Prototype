"""The outer world's tables, defaults and helpers: everything world.py held outside class World, moved out
verbatim. world.py and World's mixins import from here."""
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
    prison_ties=False,  # spheres finishing pack, part 4: former inmates as ties in a life's People (read by world_people
                        # only: the world itself is the same with it on or off)
    far_ties=False,    # item 18: a town's events touch the named people living there; a close tie in another town calls
                       # (chroma-ideas/far-off-events.md; sides in sphere_data.FAR); with sph_events
    far_par=None,      # far_ties tuning: {name: value} over world_people.FAR_DEFAULT (None: the start values)
    fair_read=False,   # S1, fairness read five ways: each life reads its spheres' fairness through its colours' parts, and
                       # a tagged sphere event moves it (chroma-ideas/social-mechanics.md S1); with sph_fair
    sph_eyes=False,    # S3 "Their places' eyes" (chroma-ideas/social-mechanics.md): each place a life belongs to reads its
                       # acts by its faces (sphere_data.PLACE_READ); a name per place moves rungs and doors, talk travels
                       # through go-betweens, places that read an act apart catch the life between them; with sph_haunts
    sph_odd=False,     # S4 "The odd one out": a life whose lead colour is rare at a place (well under its share at their
                       # other places) is seen more, pressed to blend in, and can move the place by holding on; with sph_eyes
    eyes_par=None,     # sph_eyes, sph_odd tuning: {name: value} over world_people.EYES_DEFAULT (None: the start values)
    lead_ways=False,   # S7 "Ways to lead" (chroma-ideas/social-mechanics.md): a modelled post per leading role (start,
                       # way, legitimacy, end) in place of phase 4's fixed leader's tenure; with sph_levers (and sph_eyes)
    lead_par=None,     # lead_ways tuning: {name: value} over world_people.LEAD_DEFAULT (None: the start values)
    sacred=False,      # S5, sacred lines (chroma-ideas/social-mechanics.md): a life grows up to two lines it will not sell;
                       # sphere and C3 events offer a price for them (sphere_data.OFFER); with sph_events (and c3_inst)
    sacred_par=None,   # sacred tuning: {name: value} over world_people.SAC_DEFAULT (None: the start values)
    seen_done=False,   # S6 "Seen it done" (chroma-ideas/social-mechanics.md): the paths and colour ways each life has
                       # seen close people, regulars and public figures walk bend its felt odds and its dreams
    seen_par=None,     # seen_done tuning: {name: value} over world_people.SEEN_DEFAULT (None: the start values)
    place_turnover=False,   # spheres finishing pack, part 2 (chroma-world/spheres/finish-pack-draft.md): the named places
                            # close (a quarterly hazard, and three town events) and a new place opens in the empty slot 2 to
                            # 6 quarters later (sphere_data.TURNOVER); with sph_haunts
    inst_even=False,   # phase 3: bodies drift toward their own past and their leaders' colours, not toward W with age
                       # or B with corruption (Emren's "Colour-even", spheres-implementation.md question 6)
    # ---- the C hooks of item 10 (chroma-world/model/stage3-rules.md section 5), built by the Outer world. Off, nothing of
    # them is drawn, computed or saved and the world runs as before
    c3_inst=False,     # C3: institution events (sold, merged, nationalised, a leak, a cover-up)
    c4_nature=False,   # C4: nature's own year (bad air, bad water, a poisoned river, drought, a glorious spring, recovery)
    c5_faith=False,    # C5: three new faith movement slots on the faith axis (founding, growth, fading, claims, tension)
    c_par=None,        # {name: value} over C_DEFAULT (tuning; None: the start values)
    c2_groups=False,   # C2 rest (Engine): a group moment's options judged half by society's norm, half by the group's;
                       # the strike vote on the world's strike, the congregation's split on a revival, a new movement or
                       # a drift from its faith body (world_link.C2_MOMENTS); c2_par: its tuning (world_link.C2_DEFAULT)
    c2_par=None,
    # ---- the spheres' finishing pack (chroma-world/spheres/finish-pack-draft.md). Off, nothing of it is computed or saved
    body_trust=False,  # part 3, trust in a sphere's bodies: each life's btrust per sphere (sphere_data.TRUST; world_people);
                       # with sph_fair
)
# the switches above (stage3-rules.md §8)
S3_RULES = ("cult_schools", "cult_scenes", "cult_adults", "cult_anchor", "cult_pushback", "cult_shake", "cult_no_dice",
            "hist_party_gov", "hist_pressure", "hist_grievance", "hist_chance_only")
SPH_RULES = ("sph_town", "sph_par", "sph_haunts", "sph_hours", "sph_marks", "sph_events", "sph_ev_base", "sph_seasons",
             "sph_joins", "sph_pairs", "inst_even", "sph_links", "sph_memory", "pair_calm", "sph_cascades",
             "sph_levers", "sph_fair", "sph_shadow", "sph_deep", "far_ties", "far_par", "fair_read",
             "sph_eyes", "sph_odd", "eyes_par", "lead_ways", "lead_par",
             "sacred", "sacred_par", "seen_done", "seen_par", "place_turnover")   # the spheres' switches and tuning (item 15); off, saved without them, as v22.2 saved
# v22.4's world switches (S3 their places' eyes, S4 the odd one out, S5 sacred lines, S6 seen it done, S7 ways to lead):
# saved only when on, so a save with them off, spheres on, is v22.3's
V224_RULES = ("sph_eyes", "sph_odd", "eyes_par")
V224_RULES += ("sacred", "sacred_par")   # S5 sacred lines
V224_RULES += ("seen_done", "seen_par")   # S6 seen it done
V224_RULES += ("lead_ways", "lead_par")   # S7 ways to lead
# the spheres finishing pack's switches (finish-pack-draft.md): saved only when on, so a save with them off is v22.5's
FIN_RULES = ("place_turnover",)   # part 2, places close and open
FIN_RULES += ("body_trust",)   # part 3, trust in a sphere's bodies
FIN_RULES += ("prison_ties",)   # part 4, former inmates as ties
C_RULES = ("c3_inst", "c4_nature", "c5_faith", "c_par", "c2_groups", "c2_par")   # the C hooks' switches and tuning (item 10); off, saved without them
# S1 (fair_read): the part or parts of fairness each felt_fairness state reads (W the same rules for all, U the truth and
# the reasons, B their due, R respect and a say, G people who mean well by us). Provisional (the Engine's reading of
# social-mechanics.md S1) until the Outer world's tags (sphere_data.FAIR["parts"]) take their place
FAIR_PARTS_PROV = {"rule.fair_hearing": "WR", "rule.favour": "W", "gather.mixing": "G", "arts.makers": "B",
                   "arts.licence": "R", "faith.trust": "G", "faith.doubt_free": "U", "care.reach": "B", "care.trust": "G",
                   "learn.openness": "U", "prod.terms": "B", "prod.holding": "B", "comm.openness": "U", "comm.trust": "G",
                   "comm.concentration": "WB", "prot.trust": "G", "prot.harshness": "R"}
_FAIR_TAGS = None


def fair_tags():
    """S1 (fair_read): {"parts": {state: parts}, "events": {event index: [(sphere index, parts, side +1 fair / -1
    unfair)]}}: the Outer world's tags (sphere_data.FAIR "parts" and "events", from dynamics.json felt_fairness.five_parts;
    each of an event's tags moves its own sphere). Without them, the provisional parts, and each event reads the
    fairness states its rows move (a fair state up or an against state down is the fair side), on the sphere moved."""
    global _FAIR_TAGS
    if _FAIR_TAGS is None:
        import sphere_data as SD
        parts = dict(SD.FAIR.get("parts") or FAIR_PARTS_PROV)
        evs = {}; given = SD.FAIR.get("events")
        for i, e in enumerate(SD.EV):
            if given is not None:
                g = given.get(f"{e['sphere']}.{e['key']}")
                if g:
                    evs[i] = [(SPH[e["sphere"]], str(p_), int(sd_)) for p_, sd_ in g]
                continue
            for r in e.get("rows", []):
                sp = r.get("target")
                if sp not in SPH:
                    continue
                d = SD.FAIR["states"].get(sp, {})
                for k, v in (r.get("state") or {}).items():
                    key = f"{sp}.{k}"; sd = 1 if key in d.get("fair", []) else -1 if key in (d.get("against") or []) else 0
                    if sd and v:
                        evs.setdefault(i, []).append((SPH[sp], parts.get(key, "WUBRG"), sd * (1 if v > 0 else -1)))
        _FAIR_TAGS = dict(parts=parts, events=evs)
    return _FAIR_TAGS
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


SEC_REF = 0.86   # the typical security of the young in a rich democracy (the long-run mean of World.security(); estimate)
