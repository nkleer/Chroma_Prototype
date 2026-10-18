"""The outer world's per-character tables and helpers: everything world_people.py held before class People,
moved out verbatim. world_people.py and People's mixins import from here."""
import sys
import numpy as np
try:   # speed pass: np.clip's own ufunc, called without its Python wrapper (the same numbers)
    from numpy._core.umath import clip as _uclip
except ImportError:
    from numpy.core.umath import clip as _uclip
from library import COLORS, COMMITMENTS, RESOURCES
from world_keys import (WHO_SLOTS, CAST_WANTS, GROUP_KINDS, LEVERS, DOMAINS, RINGS, NORM_KEYS, INST_KINDS, SECTORS,
                        FEATURES)
from world_keys import SPHERES, GROUP_SPHERE, SECTOR_SPHERE, HAUNT_KINDS, TIME_ROWS, LADDER, TOUCHES
from world_keys import CAUGHT_TAGS as WK_CAUGHT, ODD_TAGS as WK_ODD
from world_keys import LEAD_WAYS
from world_keys import OWN_WANTS, SACRED_KINDS, OFFER_KINDS, OFFER_ROUNDS, HEAL_TAGS
from world_keys import INST_SPHERE

C = len(COLORS)
KN = [c_[0] for c_ in COMMITMENTS]
CAR, PAR, KID, COM, FAI = (KN.index(k_) for k_ in ("career", "partner", "children", "community", "faith"))
MON, TIM, HEA = (RESOURCES.index(r_) for r_ in ("money", "time", "health"))
ENGINE_ROLES = ["parent", "sibling", "friend", "grandparent", "partner"]   # the engine's ROLES: the columns of alive
_NW = WHO_SLOTS.index("keeper") if "keeper" in WHO_SLOTS else len(WHO_SLOTS)   # slots appended later go after the own
ROLE = list(WHO_SLOTS[:_NW]) + ["kin", "grandchild", "inlaw", "classmate", "member", "acquaintance"] + list(WHO_SLOTS[_NW:])
R = {r_: i_ for i_, r_ in enumerate(ROLE)}
BIT = {r_: 1 << i_ for i_, r_ in enumerate(ROLE)}
GROUP_SPH = np.array([-1 if GROUP_SPHERE[k_] is None else SPHERES.index(GROUP_SPHERE[k_]) for k_ in GROUP_KINDS])
SECTOR_SPH = np.array([SPHERES.index(SECTOR_SPHERE[k_]) for k_ in SECTORS])   # spheres (item 15): world.py's maps
# each setting kind's subsector (its place, sphere_data.PLACE_BY_EPOCH); work by its employer's sector (item 15, phase 1d)
SET_SUB = {"household": "care.hearth", "class": "learn.schooling", "congregation": "faith.congregation",
           "club": "gather.circle", "scene": "gather.night", "online": "gather.talk", "neighbours": "gather.house",
           "gang": "prot.hire", "unit": "prot.host", "ward": "care.houses", "movement": "rule.voice"}
# phase 2 (N1, N2): the haunt kinds' spheres; which kinds a club or a scene setting is held at; the youngest age for
# each kind (others from 4; the yearly great gathering is the whole town's, never picked); what a kind costs (0 to 1)
HAUNT_SPH = np.array([SPHERES.index(k_.split(".")[0]) for k_ in HAUNT_KINDS], np.int64)
SCENE_HAUNTS = {"gather.night", "arts.stage", "arts.song"}
SET_HAUNTS = {"club": [i_ for i_, k_ in enumerate(HAUNT_KINDS) if k_ not in SCENE_HAUNTS and k_.split(".")[0] in ("gather", "arts", "learn", "prod", "prot", "care", "rule") and k_ not in ("gather.great", "learn.higher")],
              "scene": [i_ for i_, k_ in enumerate(HAUNT_KINDS) if k_ in SCENE_HAUNTS],
              "congregation": [i_ for i_, k_ in enumerate(HAUNT_KINDS) if k_.startswith("faith.")]}
HAUNT_AGE = np.array([dict(**{"gather.house": 16, "gather.night": 16, "gather.great": 999, "comm.credit": 18, "rule.voice": 16,
                              "rule.counsel": 30, "prot.watch": 18, "prot.host": 18, "prot.rescue": 18, "care.houses": 14,
                              "learn.higher": 18, "faith.orders": 18, "comm.shop": 12, "comm.market": 8}).get(k_, 4)
                      for k_ in HAUNT_KINDS], float)
HAUNT_COST = np.array([dict(**{"gather.house": .5, "gather.night": .6, "gather.hall": .4, "arts.stage": .4, "arts.screen": .3,
                               "comm.shop": .3, "comm.credit": .3, "gather.games": .2, "arts.craft": .2}).get(k_, 0.0)
                       for k_ in HAUNT_KINDS], float)
WORK_SUB = {"farm": "prod.land", "industry": "prod.works", "services": "comm.shop", "knowledge": "learn.finding",
            "public": "rule.office"}
G = {g_: i_ for i_, g_ in enumerate(GROUP_KINDS)}
NG = len(GROUP_KINDS)
WI = {w_: i_ for i_, w_ in enumerate(CAST_WANTS)}
NW = min([CAST_WANTS.index(w_) for w_ in OWN_WANTS if w_ in CAST_WANTS] + [len(CAST_WANTS)])   # the cast's wants (the
# life's own, S5's, go last and never arise in the cast)
LI = {l_: i_ for i_, l_ in enumerate(LEVERS)}
DI = {d_: i_ for i_, d_ in enumerate(DOMAINS)}
NNORM = len(NORM_KEYS)
GATES = ["open", "invitation", "test", "birth", "admission"]
RING_OF = np.array([0 if d_ == "close" else 1 if d_ in ("group", "place") else 2 if d_ == "institution" else 3
                    for d_ in DOMAINS])
REACH = np.array([[3, 1, 0, 0], [3, 2, 1, 0], [3, 2, 2, 1], [3, 2, 3, 2]], float)   # spec 7 §2: standing level x ring
RUNG_MULT = np.array([0.125, 0.5, 1.0, 1.5, 2.0])   # spheres phase 4: a lever's pull by rung, newcomer .. leader (N2)
NEVER = -10 ** 7
STATUS = ["citizen", "migrant", "resident"]   # a life's status in the society it lives in (spec 5 §5)
# display priority when someone holds several roles toward the character
ROLE_ORDER = ["partner", "ex", "parent", "child", "sibling", "grandparent", "grandchild", "inlaw", "kin", "boss",
              "teacher", "mentor", "rival", "friend", "prospect", "colleague", "classmate", "neighbour", "elder",
              "member", "acquaintance"]
KIN_ROLES = ["parent", "sibling", "child", "grandparent", "grandchild", "inlaw", "kin"]
KINMASK = sum(BIT[r_] for r_ in KIN_ROLES)
CORE = BIT["partner"] | BIT["parent"] | BIT["child"] | BIT["sibling"]

PP_DEFAULT = dict(
    K=200,               # cast slots per life: Dunbar's 5/15/50/150 plus room for the dead, the remembered and faces
    M=8,                 # setting slots per life
    KC=24,               # close index: the slots updated weekly (layers 1 and 2 hold about 15)
    conc=0.7,            # a new person's pie: Dirichlet concentration per color around their expected mix (estimate)
    pw_loc=0.55, pw_coh=0.45,   # that expected mix: the locality's residents and the person's generation (spec 2 §6)
    layer_c=(0.55, 0.33, 0.15, 0.02),   # closeness from which a person is in layer 1, 2, 3, 4 (fitted to 5/15/50/150)
    f_half=16.0,         # contacts a year that bring closeness to half its ceiling: with the ceiling about 0.85,
                         # weekly contact holds layer 1, monthly layer 2, quarterly layer 3, yearly layer 4 (Dunbar's
                         # contact frequencies by layer; Sutcliffe et al. 2012)
    tau_up=0.35,         # years for a tie to grow toward what contact supports (new friendships form in months)
    tau_dn=1.0, tau_dn_kin=4.0,   # years to fade: friends within one to two years without contact, kin far slower
                         # (Roberts and Dunbar 2011)
    D0=350.0,            # deliberate contacts a year (calls, visits) an adult spends outside shared settings (estimate)
    soc_spread=(0.2, 2.0),   # each life's own sociability: x on that budget and on chance meetings, log-uniform
    soc_set=0.75,         # ... and (sociability / its geometric mean)^soc_set on the contact in shared settings
                         # (like the engine's turn_spread; gives the share of adults with no close friend)
    alloc_pow=2.5,       # deliberate contact goes to the closest first (x closeness^pow): the layers emerge from it
    dist_far=0.4,        # share of a deliberate contact that reaches someone in another locality without remote tools;
                         # W.comm (phones, video calls) adds up to 0.5 (spec 3 §2.6, spec 5)
    cap_like=0.5,        # ease: closeness's ceiling is 1 - cap_like x (1 - likeness); alike people keep ties for less
    mingle=(0.35, 1.3),  # within a setting people seek out the alike: attention a + b x likeness^2 ...
    att_c0=0.15, att_pow=0.3,  # ... and the already close: x (closeness + c0)^pow; shared out so the members' mean
                         # is the setting's contact (a team of twenty holds a few friends, not twenty; Feld 1981)
    mingle_age=(5.0, 0.2, 0.25),  # ... and those near their own age (kin aside): x f + (1 - f) / (1 + (gap / w)^2) with
                         # w = a + b x age (age is among the strongest likenesses friends share; McPherson,
                         # Smith-Lovin and Cook 2001): close non-kin about 8 years apart, acquaintances about 16
    kin_f=dict(parent=(30, 8), child=(30, 8), sibling=(12, 3), grandparent=(6, 2), grandchild=(10, 3),
               inlaw=(5, 1.5), kin=(2, 0.6)),   # family gatherings and calls: contacts a year (same locality, elsewhere)
    meet=(0.5, 1.2),     # new people a quarter: brought by a friend (x friends / 3, up to 6), by chance (x sociability)
    trust_k=0.06,        # quarterly pull of trust toward what likeness and shared marks support
    break_p=0.012,       # yearly chance a close non-kin tie breaks in a fight (x (1.5 - likeness)); kin a third of it
    mort=(0.0006, 3.5e-5, 0.09),   # yearly death chance c + a exp(b x) (the engine's self_mort, Gompertz-Makeham)
    mort_cls=(1.3, 1.0, 0.8),      # x by class: lower, middle, upper (estimate)
    ill_p=(0.015, 0.0012),         # yearly chance of a serious illness: a + b x max(0, age - 30)^1.5 / 10 (estimate)
    jobloss=0.03,        # yearly chance an employed cast member loses their job (x W.rate_mult("jobloss") by sector)
    rehire=2.0,          # yearly chance an unemployed one finds work at the natural rate
    couple_p=0.12, divorce_p=0.012, kid_p=0.10,   # their own partnering, divorce and births a year (estimate)
    far_share=0.35,      # share of moves that leave the locality (the rest change neighbourhood) (estimate)
    move_age=((0, 0.12), (5, 0.085), (18, 0.12), (20, 0.16), (22, 0.21), (25, 0.20), (30, 0.14), (35, 0.09), (45, 0.06),
              (55, 0.045), (65, 0.035), (75, 0.03)),   # yearly moving rate from each age (US Census CPS: about 8.5% overall;
                                                       # 18-19 about 13%, 20-24 about 20%, 25-29 about 18%)
    sib_p=(0.2, 0.4, 0.25, 0.15),  # number of siblings 0-3 (the engine's draw, so alive counts agree)
    p_sep=0.10, sep_p=0.012,       # parents living apart at the birth; yearly separation while the child is under 18
    p_biz=0.08,          # a parent runs a family business or craft (successor wants; about 1 in 10 self-employed)
    p_uni=(0.30, 0.45, 0.65),      # tertiary study by family class (estimate)
    leave_home=0.2,      # yearly chance from 18 of leaving the parents' household (sooner with a partner)
    vol_join=dict(club=0.04, scene=0.04, online=0.06), vol_leave=0.2,   # adults' yearly joining and leaving of groups
    care_home=0.08,      # yearly chance from 75 with poor health of moving into a care home (a ward)
    same_sex=(0.0, 0.03, 0.16, 0.8, 1.0),    # chance a partner is of the same sex by the engine's attraction 0-4 (Pew
                                             # 2013; the engine's partner_same_p); S["partner_same"] overrides it
    stand_p=(0.93, 0.055, 0.013, 0.002),     # a cast member's standing 0-3 (local, inside power, national) (estimate)
    p_inherit=0.75,      # a child keeps a parent's faith and party (Jennings, Stoker and Bowers 2009: strongest)
    pie_inherit=0.35,    # weight of the parents' mix in a child's expected pie (values pass on moderately)
    times_w=(0.04, 0.16, 20.0, 7.0),   # the times' share of the niche: base + peak x exp(-((age - at) / width)^2)
                         # (Close first, Emren 10:39: peaks at 15 to 25)
    close_w=0.15,        # weight of the close circle's colors in the niche against the settings' norms (the settings
                         # are the main weekly push, spec 3 §1.4; the close circle about a third of it)
    msg_ref=1.75,       # raw push strength of a typical adult's circle (msg_w = raw / msg_ref, so 1 is today's niche)
    belong_k=(1.6, 0.35),          # belonging met: settings (ts x cohesion x acceptance) and close people (closeness^2)
    comm_ref=0.6, comm_k=0.8,     # community driver: comm_k x (settings' cohesion x acceptance - comm_ref), -0.5..0.5
    ties_T=20.0,         # ties = 1 - exp(-(sum of closeness in layers 1-3) / ties_T): about 0.55 for a typical adult
    help_H=6.0, help_ref=0.67, sup_k=0.35,   # support: sup_k x (help - help_ref) x (1 + hard week); help in 0..1
    rank_k=0.006,        # weekly rank change in a group per visible act: x how much better (worse) it fits the group's
                         # ways than its members' own do, x how well it went when it fits better
    rank_rev=0.02, rank_base=0.4,   # monthly pull of rank back to the middle (rank is relative: few can lead)
    wide_net=250,        # people in the active network that make a wide network (standing 1 in groups and place)
    strict_age=0.015,    # a cast member's strictness on norm keys rises with their age (older cohorts lag)
    obj_half=3.0,        # half-life in years of a close person's strong disapproval of an act of the character's
    circle_w=0.5,        # most the close circle weighs in the acceptance a character feels (against their groups')
    fr_k=0.8,            # felt reach: reach + fr_k x (outlook - 0.45) x (1 + reach) + a personal bias (spec 7 §6)
    fr_bias=0.15,        # spread of that personal bias
    push_unit=(1.0, 1.0, 0.02, 0.01),   # a push of size 1 by ring, in the target's units (outer rings: W.push amount)
    crowd=1e-6,          # an ordinary vote or voice in the state, economy or culture: one among millions
    backfire=dict(exit=0.1, voice=0.3, loyalty=0.05, neglect=0.1, subvert=0.4),   # chance a failed push backfires
    lever_sign=dict(exit=-1, voice=1, loyalty=1, neglect=-1, subvert=1),
    forgive=(0.25, 13),  # a kin member's wish to make peace after a break with the character: quarterly hazard weight,
                         # from this many weeks after it, while still apart (once per break; about a quarter of adults
                         # are estranged from a relative, most reconcile once at most: Pillemer 2020)
    contagion=(0.25, 0.15),        # extra chance of divorce and of quitting after a close person's (small; McDermott,
                                   # Fowler and Christakis 2013, debated)
    lang0=0.15,          # a migrant's skill in the new society's language on arrival (0-1; native 1)
    lang_k=((0, 1.0), (6, 1.6), (12, 1.3), (18, 0.6), (30, 0.25), (60, 0.12)),   # yearly learning rate by age at
                         # full exposure: lang -> 1 - (1 - lang) exp(-k x exposure x years) (children learn fastest;
                         # exposure: the time spent in settings outside the home)
    mig_gate=(0.2, 3.0), # joining a setting or institution as a migrant at first: openness to migrants x (g0 + (1 - g0)
                         # x language), easing toward always over tau years (spec 5 §5; Bertrand and Mullainathan 2004)
    auto_move=False,     # True: PP moves people itself at move_wish's rate (checks); False: the engine's moving moments
    color_perm=None,     # None: the World's own (W.perm); the equivariance test relabels colors through it
    watch=None,          # lives whose events are built (None: all)
)

# settings by kind: contact a year with each member, depth (how much of it builds closeness), time share (adult, young),
# cast members met, statistical size, yearly member turnover, base cohesion, monthly norm drift, weights of members,
# anchor (institution, faith or founding ways) and the culture in the norms' target, gate, exit cost, leader role
KT = dict(
    household=(200, 1.00, 0.35, 0.55, 0, 4, 0.00, 0.70, 0.020, 1.0, 0.0, 0.02, "birth", 0.6, None),
    **{"class": (40, 0.20, 0.27, 0.27, 22, 26, 0.02, 0.45, 0.030, 0.4, 0.4, 0.20, "admission", 0.2, "teacher")},
    work=(45, 0.15, 0.36, 0.36, 22, 40, 0.15, 0.45, 0.015, 0.4, 0.5, 0.10, "admission", 0.4, "boss"),
    congregation=(15, 0.35, 0.03, 0.04, 14, 150, 0.06, 0.65, 0.005, 0.25, 0.7, 0.05, "open", 0.5, "elder"),
    club=(25, 0.30, 0.04, 0.06, 12, 30, 0.15, 0.50, 0.020, 0.6, 0.3, 0.10, "test", 0.2, "member"),
    scene=(15, 0.30, 0.05, 0.06, 9, 80, 0.20, 0.45, 0.030, 0.6, 0.3, 0.20, "invitation", 0.3, None),
    online=(30, 0.10, 0.05, 0.06, 6, 800, 0.30, 0.25, 0.080, 0.7, 0.2, 0.20, "open", 0.05, None),
    neighbours=(12, 0.30, 0.02, 0.02, 24, 300, 0.08, 0.40, 0.010, 0.5, 0.5, 0.05, "open", 0.1, None),
    gang=(60, 0.40, 0.15, 0.15, 6, 12, 0.20, 0.70, 0.030, 0.6, 0.3, 0.05, "test", 0.8, "member"),
    unit=(80, 0.35, 0.70, 0.70, 12, 30, 0.20, 0.75, 0.020, 0.3, 0.7, 0.05, "admission", 0.9, "boss"),
    ward=(40, 0.25, 0.80, 0.80, 5, 30, 0.30, 0.30, 0.020, 0.4, 0.6, 0.02, "admission", 0.5, "member"),
    movement=(15, 0.30, 0.05, 0.05, 7, 3000, 0.20, 0.55, 0.030, 0.4, 0.6, 0.10, "open", 0.3, "member"),
)
KTA = np.array([[float(v_) if not isinstance(v_, str) and v_ is not None else 0.0 for v_ in KT[g_][:12]]
                for g_ in GROUP_KINDS])
(K_F, K_DEPTH, K_TS, K_TSY, K_NCAST, K_SIZE, K_CHURN, K_COH, K_DRIFT, K_WM, K_WA, K_WV) = range(12)
K_GATE = np.array([GATES.index(KT[g_][12]) for g_ in GROUP_KINDS])
K_XC = np.array([KT[g_][13] for g_ in GROUP_KINDS], float)
K_LEAD = [KT[g_][14] for g_ in GROUP_KINDS]
LEAD_BIT = np.array([BIT[K_LEAD[g_]] if K_LEAD[g_] else 0 for g_ in range(len(GROUP_KINDS))], np.int32)
LEAD_ROLE = np.array([R[K_LEAD[g_]] if K_LEAD[g_] else -1 for g_ in range(len(GROUP_KINDS))], np.int8)
MEMBER_ROLE = dict(household="kin", work="colleague", unit="colleague", neighbours="neighbour", **{"class": "classmate"})
MEMBER_ROLE_OF = np.array([R[MEMBER_ROLE.get(g_, "member")] for g_ in GROUP_KINDS])
VOLUNTARY = np.array([G[g_] for g_ in ("congregation", "club", "scene", "movement")])
LOCAL_KINDS = np.array([G[g_] for g_ in ("class", "work", "congregation", "club", "scene", "neighbours", "gang")])
INST_OF = dict(work="employer", unit="army", ward="hospital", **{"class": "school"})
COMM_W = np.array([dict(household=0.2, work=0.3, congregation=1.0, club=1.0, scene=0.8, online=0.4, neighbours=0.5,
                        gang=0.6, unit=0.8, ward=0.3, movement=1.0, **{"class": 0.3})[g_] for g_ in GROUP_KINDS])
WANT_RATE = np.array([dict(money=2.0, care=2.0, successor=0.5, grandchild=0.7, love=1.0, rival=1.0, forgiveness=0.5,
                           home=0.7, stop=1.5, secret=1.0, far_hard=26.0, far_good=26.0, far_mixed=26.0,
                           caught=0.0, odd=0.0, sacred=0.0, tragic=0.0, amends=0.0,
                           lead_take=26.0, lead_crisis=26.0, lead_fall=26.0, lead_routine=26.0, lead_hand=26.0).get(w_, 0.0)
                      for w_ in CAST_WANTS])   # ripening a year (a far tie's call: within weeks; S3, S4's never ripen)
NW_ARISE = WI.get("caught", NW)   # S3, S4: the wants from "caught" on never arise as a cast member's wish (the place
                                  # reading fires them, sph_eyes and sph_odd; S5's come with a line, S7's lead_* with a post)
# resolving a want: (closeness, trust) if accepted, (closeness, trust) if refused, mark if accepted, mark if refused
# (marks are words of engine.py's MARK_BASE)
WANT_FX = dict(money=((0.05, 0.10), (-0.08, -0.10), "helped someone in need", "refused someone in need"),
               care=((0.10, 0.10), (-0.15, -0.15), "helped someone in need", "refused someone in need"),
               successor=((0.10, 0.05), (-0.10, -0.05), "kept your word", "turned down a chance"),
               grandchild=((0.05, 0.05), (-0.05, -0.05), None, None),
               love=((0.20, 0.10), (-0.20, -0.05), None, None),
               rival=((-0.05, -0.05), (0.02, 0.02), "made an enemy", None),
               forgiveness=((0.25, 0.20), (-0.05, 0.0), "made a friend", None),
               home=((0.15, 0.10), (-0.10, -0.05), "stayed home", "moved away"),
               stop=((0.10, 0.10), (-0.15, -0.10), "kept your word", None),
               secret=((0.10, 0.10), (-0.05, -0.05), "kept your word", None),
               far_hard=((0.10, 0.10), (-0.10, -0.10), "helped someone in need", "refused someone in need"),
               far_good=((0.05, 0.05), (-0.05, -0.05), None, None),
               far_mixed=((0.08, 0.08), (-0.08, -0.05), None, None),
               caught=((0.0, 0.0), (0.0, 0.0), None, None), odd=((0.0, 0.0), (0.0, 0.0), None, None))
FAIR_PART_NAMES = ["rules", "reasons", "due", "respect", "goodwill"]   # S1: the parts of fairness, W U B R G (Library)
# body_trust (the spheres' finishing pack, part 3; chroma-world/spheres/finish-pack-draft.md): the sphere of each body kind
# (world_keys.INST_SPHERE; an employer has none, so a job at a firm is not work in a sphere's bodies), and the titles of the
# force that serve in a body without naming one (the guard, the host)
BT_INST_J = np.array([SPHERES.index(INST_SPHERE[k_]) if INST_SPHERE.get(k_) else -1 for k_ in INST_KINDS], np.int64)
BT_FORCE = {"police officer": "police", "soldier": "army"}
BT_FIRST = (0.5, 0.3)   # the start of a first life: .5 + .3 x (the town sphere's fairness - .5) (finish-pack-draft.md part 3)


def bt_title_kind(name, inst):
    """body_trust: the body kind (INST_KINDS index) a title is held at, where that body has a sphere: its institution's
    (the catalogue's institution=), else the force's by name; -1 none."""
    if inst is not None and int(inst) >= 0 and BT_INST_J[int(inst)] >= 0:
        return int(inst)
    return INST_KINDS.index(BT_FORCE[name]) if name in BT_FORCE else -1


FR_HABIT = 3.0   # S1: the half-life, in years, of how often each part of fairness was heard of lately (habituation)
FARW = np.array([w_.startswith("far_") for w_ in CAST_WANTS])
# far_ties (item 18, chroma-ideas/far-off-events.md): start values, estimates refit in v22.3's one refit. hard, good: the
# sides' shares x these; call_*: the chance a touched tie among the ~15 closest, living in another town, calls; take:
# the share of the cast's random job loss, rehire and illness the towns' events take over (jobloss, rehire, illness);
# stay: weeks a tie taken in lives in the household; lapse: weeks an unanswered call waits; cause: weeks a later want
# carries the event that started it
FAR_DEFAULT = dict(hard=1.0, good=1.0, call_hard=0.75, call_good=0.5, call_mixed=0.75, take=(0.3, 0.3, 0.1), stay=52,
                   lapse=8, cause=104)
# sacred lines (S5, chroma-ideas/social-mechanics.md): start values, estimates refit in v22.3's one refit
SAC_DEFAULT = dict(
    lead=5.0,          # years a colour has led the life's colours (the engine's w) before a line can form in it
    paid=2,            # ... and acts in its ways that cost something real (engine.py, the act's own steps: money at or
    cost_money=0.1,    # below -.1, a tenth of the money scale (an option's own price, the means backfire); ties at or below
    cost_ties=0.1,     # -.1 (the law backfire); stress of .3 or more (the law backfire): the price of an act the law or
    cost_stress=0.3,   # the world closed, or of one that costs real money), counted from age 12
    cost_closed=True,  # ... and any closed option that failed, whatever closed it (law, approval or means): its backfire is
                       # a real cost even where it stays under those thresholds (a frowned-on act's: ties -.08, stress .15),
                       # so each colour's ways count as costly as the world closes them (v22.4 fix: White's costs are
                       # mostly frowned-on acts, and without it White formed lines at .37 of its share of lead years)
    age=16.0,          # lines form from this age (and offers reach them)
    lines=2,           # at most two lines a life
    reach=0.25,        # the share of those in the event's town an offer fits (who:) and touches a line of that it reaches
                       # (an offer event comes about 1.7 times a town-year, so a line meets one every 10 to 20 years)
    known=2,           # a line answered this many times (held or crossed) is known around them: no more offers
                       # come for it (v22.4 fix: offers follow the town's events, the who: they fit and how long the line
                       # lasts, so without it Black and Green lines met up to twice the offers of White and Blue ones)
    c3_reach=0.5,      # C3's institution events: the share of its staff it reaches (as the C hooks' moments, .3 to .7)
    refuse=0.9, gesture=0.7, doubling=0.05, cap=0.98,   # the character's own pick holds at .9 (.7 when the offer carries
                       # a symbolic gesture), + .05 per doubling of the offer's size, at most .98 (Ginges et al. 2007)
    size_max=4.0,      # a refused offer comes back doubled (round raised), up to four times the first (.98 there)
    raised=(4, 12),    # weeks after a first refusal before the raised offer comes
    lapse=8,           # weeks an offer or amends waits for its moment
    quiet=True,        # an offer with no moment for it (or whose moment never came) is decided off-screen by the same odds
    hold=dict(money=(0.05, 0.0), post=(0.05, 0.03), favour=(0.05, 0.05)),   # holding: the money and ties not had, by the
                       # offer's kind, x its size: every offer's price is money not had (a post its pay, a favour what
                       # it was worth), a post and a favour also cost ties (v22.4 fix: a favour cost no money, and White's
                       # promise lines meet mostly favours)
    wound=0.5,         # crossing: stress, a moral injury (Litz et al. 2009), as a widowing's
    seed=0.15,         # ... a seed in the line colour's shadow part (with shadows; a reflection moment takes off as much)
    piv=0.15, piv_far=1.0, piv_core=0.3,   # ... and a turning point's lesson (the game's item 4, its full "toward" kind)
    heal=0.25,         # healing (amends or reflection): stress eased
    amends=(26, 104),  # an amends moment comes this many weeks after the wound, again a year after one left for later,
    amends_again=52, amends_max=3,   # at most three
    tragic=0.1,        # the share of lives with two lines that may meet a tragic trade-off (once): at most 1 life in 10
    tragic_w=(0.45, 0.45, 0.1),   # the character's own pick at one: a, b, torn
)
SAC_WHO = ("any", "in_work", "out_of_work", "owner", "renter", "poor", "comfortable", "young", "old", "ill", "parent")
FAR_WHO = ("any", "in_work", "out_of_work", "owner", "renter", "poor", "comfortable", "young", "old", "ill", "parent")
FAR_OFF = 10 ** 9   # far_in: not taken in
# S3 "Their places' eyes" and S4 "The odd one out" (chroma-ideas/social-mechanics.md; the reading itself, its outcome step,
# half-life, rung speeds, talk weight and caught gap are dynamics.json place_reading, copied as sphere_data.PLACE_READ).
# Start values here are the Engine's estimates where the spec names no number, all for v22.4's refit: act_w, the share
# of a place's reading one act adds to the name there (rep -1..1); step, how far a caught-between pick moves a name (the
# outcome's size); fair, felt fairness lost in the sphere of the side not taken; back, the drift of stepping back; strain,
# belonging a kept-apart pair costs while both places last; door, the job-finding difficulty a name moves through a
# place's go-betweens (DIFF units, x the mean name); cool, weeks between two caught-between moments; wait, weeks a
# moment waits to be met; ev_opp, how opposed two sphere events' asks must read (place reading of one by the other);
# buf_haunt, the exit cost of a haunt (a club's); buf_half, the half-life in weeks of the belonging a leaving costs;
# odd_*: S4's odd_z, how far under what they are used to their lead colour's share at a place must sit, in spreads (1;
# what they are used to: each colour's mean log share at their places a year or more theirs, and its spread among them, a
# running mean with odd_mem of each year's places, .25; in proportion, so half the share is as odd for a rare colour as a
# common one; the spread with odd_vmem when set, v22.5 .05: how far apart their places sit is learnt over a life, so two
# places do not put the lower one exactly one spread under; None: odd_mem), visibility x1.5, pressure x1.3, contrast .05 x the rung factor,
# blend step .02, years held (3), the place's lean by rung a year (regular .005, known .02, leader .04; pillar between),
# the regulars' .002 a year, hardening .01; hold_k, the log-odds an unplayed life's own colour strength and rung add to
# holding on; pair_k, the power of the two places' mean share that scales each colour's gap when the caught-between pair
# is read (.5: the root, as a chi-square reads two mixes; higher reads a rarer colour's gap larger); pair_norm, when above 0,
# reads each pair's gap against how far apart that pair's colours usually sit in the reads so far (a running mean, this
# much of each read), so the pair named is the split that stands out, not the one that is wide everywhere (0: as before)
EYES_DEFAULT = dict(act_w=0.1, step=0.3, fair=0.1, back=0.1, strain=0.02, door=0.1, cool=52, wait=13, ev_opp=-0.2,
                    buf_haunt=0.2, buf_half=26.0, odd_z=1.0, odd_mem=0.25, odd_vmem=None, odd_vis=1.5, odd_press=1.3, odd_contrast=0.05,
                    odd_rung=(1.0, 0.75, 0.5, 0.25, 0.0), odd_blend=0.02, odd_hold=3,
                    odd_lean=(0.0, 0.005, 0.02, 0.03, 0.04), odd_regular=0.002, odd_harden=0.01, hold_k=0.5, pair_k=0.5, pair_norm=0.0)
EYES_G = [G[k_] for k_ in ("work", "congregation", "unit")]   # S3: the settings that are places of their own
EYES_ENEMY = ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))   # S3: the Canon's enemy pairs WB WR UR UG BG, as W U B R G indices
EYES_LEAVE = ("left job", "left partner", "left faith", "title lost")   # acts read as walking away from their colours
# lead_ways (S7 "Ways to lead", chroma-ideas/social-mechanics.md, with "The leader's time in post" and "The falls in
# numbers"): start values for v22.3's one refit, estimates where the spec gives none. The time in post itself (term,
# renewal, consecutive terms, yearly end chance, age out, by post kind and epoch) and the fast-change line are the Outer
# world's (dynamics.json lead_posts, sphere_data.LEAD_POSTS). take: a quarter's chance that a pillar (rank .85 or more) of
# a setting with a leader takes the lead; take_age: from this age; rival: a quarter's chance that the setting's most
# standing member challenges (a rival of higher rung takes over); fall: legitimacy under this is a fall; step: the size of
# every fall's step in legitimacy, one for all five ways (v22.4 fix round: with the spec's .3, .3, .4, .05 and custom's
# .05, posts by rules, knowing and favours fell at their first step and inspiring and custom ones never fell, so time in
# post leaned on the way; .15: from the typical legitimacy, about .43, a second failure is the fall); crisis: the chance
# that a crisis (a sphere event in the sphere led) breaks a way: a rules leader rule-bound, a knowing one shown wrong, an
# inspiring one not carrying it (the spec's roads gave rules and knowing almost no falls, and inspiring almost no
# success; fitted at the even base, about four steps in ten years in post for each way); fair_line: the led's felt
# fairness under this is a fairness scandal; frail: health under this ends a post; sh, sh_years: the shadow target one
# way held sh_years adds to its colour (item 2, with shadows); fight: a fall fought and won leaves legitimacy here, once
# a post (its next fall ends it; v22.4 fix round: fighting is a rules and an inspiring leader's own answer in the fall
# moments, and fights won again and again kept White's posts longest); again: weeks after standing down before the
# take chance doubles there; wait: weeks a post's moment waits to come; routine: yearly fades in a row after which the
# inspiring leader's turn to routine is offered in place of the crisis; ruler_end: the yearly end chance of a national
# office where there are no elections (held at the ruler's pleasure); fav_drop: favours owed also run out when, at the
# yearly check, the leader's money is under this share of its best since they began leading by favours (a patron with
# less to give than the clients came for; Scott 1972), read against the life's own money so it holds whatever money
# the society runs at (v22.5: with real money few leaders sit under the need line, and favours fell .7 a ten post-years
# against 3.4 to 3.7 for the other ways); 0: the need line alone, as before; fast_gap: weeks after a custom step before
# fast change can step the post again (custom reads the town's change over four quarters, so one stretch of change stayed
# in the window and stepped the post in back-to-back quarters: 96% of a custom post's later steps came the next quarter,
# against none to a third for the other ways, and its second step was the fall; 52: once a year, as favours and
# inspiring are read), fast_k: the fast line x this (with fast_gap, the line that keeps custom's falls with the other
# ways'); 0 and 1: every quarter, at the Outer world's line, as before; owner_kind: a title that owns what it leads
# (LEAD_OWNED: a founder of a firm) holds it as an owner does (place_owned, as a shop or café owner: about .07 a year to
# step down and an age out at 70), not as an appointed manager (setting_work: .15 and 67); False: as before (the v22.5
# refit's values: engine.V225 lead_par)
LEAD_DEFAULT = dict(take=0.05, take_age=18, rival=0.02, fall=0.2, step=0.15, crisis=0.25, fair_line=0.35, frail=0.35,
                    sh=0.2, sh_years=10.0, fight=0.3, again=52, wait=8, routine=2, ruler_end=0.1, fav_drop=0.0,
                    fast_gap=0, fast_k=1.0, owner_kind=False)
# the engine's titles that lead (each held title is a post; the catalogue's own leaders, since a setting's rank seldom
# reaches a pillar's .85): its post kind in lead_posts (national: the world's own government term and elections), its
# sphere, and the group kind of the setting it leads (the led place is that setting's ways, or its named place, when the
# life is in one; else the town sphere's faces)
LEAD_TITLES = {"head of government": ("national", "rule", None), "minister": ("national", "rule", None),
               "party leader": ("national", "rule", None), "member of parliament": ("national", "rule", None),
               "mayor": ("office_local", "rule", None), "local councillor": ("office_seat", "rule", None),
               "lay judge": ("office_judge", "rule", None), "research group leader": ("office_head", "learn", None),
               "community centre manager": ("office_head", "gather", None), "artistic director": ("office_head", "arts", None),
               "shift manager": ("setting_work", "comm", "work"), "head chef": ("setting_work", "comm", "work"),
               "founder of a firm": ("setting_work", "prod", "work"), "union rep": ("setting_member_led", "prod", "work"),
               "shop owner": ("place_owned", "comm", None), "café or bar owner": ("place_owned", "gather", None),
               "community theatre director": ("place_chosen", "arts", None),
               "deacon or elder": ("setting_congregation", "faith", "congregation"),
               "team captain": ("setting_member_led", "gather", "club"),
               "community-garden coordinator": ("setting_member_led", "prod", "club"),
               "parent-association organiser": ("setting_member_led", "learn", "club"),
               "book-club organiser": ("setting_member_led", "arts", "club"),
               "board-game club organiser": ("setting_member_led", "gather", "club"),
               "neighbourhood-watch coordinator": ("setting_member_led", "prot", "club"),
               "festival organiser": ("setting_member_led", "gather", "club"),
               "volunteer research organiser": ("setting_member_led", "learn", "club"),
               "disability-rights organiser": ("setting_member_led", "rule", "movement"),
               "campaign organiser": ("setting_member_led", "rule", "movement"),
               "founder of a movement": ("setting_member_led", "rule", "movement")}
LEAD_OWNED = {"founder of a firm": "place_owned"}   # titles that own what they lead: their post kind with owner_kind
LEAD_KINDS = ("work", "congregation", "club", "gang", "unit", "movement")   # settings a life can come to lead
# seen_done (S6, chroma-ideas/social-mechanics.md "Seen it done"): start values, estimates refit in v22.3's joint refit
# (the Outer world files none in dynamics.json). close, regular, figure: an exposure's weight by who walked the path
# (close people, layers 1 and 2; regulars at the life's haunts; public figures); win, fail: a success seen counts +win,
# a failure seen -fail; far: x for a model far above (far_rungs or more rungs higher, or far_years or more older);
# lift: felt odds per unit of exposure, up to cap units; fail_lift: felt odds lost per failure seen, up to fail_cap
# (the Engine's cap, so a long life of losses seen cannot take the felt odds to nothing); dream: at dream_ages a new
# dream's domain leans by 1 + dream x the share of cap its best seen path has reached; from_age: the age from which a
# life takes in what it sees; mix: a regular of another class counts through a gather haunt only, by mix x the town's
# gather.mixing (up to 1: the middle of the scale lets them in fully)
SEEN_DEFAULT = dict(close=1.0, regular=0.3, figure=0.05, win=1.0, fail=0.5, far=0.3, far_rungs=3, far_years=25,
                    lift=0.03, cap=3.0, fail_lift=0.02, fail_cap=3.0, dream=1.0, dream_ages=(8, 20), from_age=4, mix=2.0)
SEEN_WORDS = ("seen", "wrong", "far", "none", "dream")   # the Library's words (earth_spheres.SEEN): the strongest model
# on an option's path or way succeeded (seen), was seen failing (wrong), counts as far above (far); nobody (none); a dream
# seeded from a seen path (dream, an event at the dream's birth)
SEEN_KINDS = ("career", "partner", "children")   # the paths a cast member walks: work (sector, standing), partner, children
# the public figures' roles (world.FIG_ROLES) and the catalogue title each walks, where the catalogue has it
SEEN_FIG = {"head of government": "head of government", "opposition leader": "party leader",
            "star": "lead actor or actress", "athlete": "professional athlete", "preacher": "ordained religious minister",
            "scientist": "research scientist", "magnate": "founder of a firm", "activist": "activist in a cause"}


def _isin_small(a, vals):
    """Speed pass: np.isin against a few whole numbers, as equalities (the same answer, without isin's sorting)."""
    a = np.asarray(a); r = np.zeros(a.shape, bool)
    for v_ in vals:
        r |= a == v_
    return r


def _csum(x):
    """Sum over the colors (the last axis), in float64 in a fixed order: fast for the (N, K, C) arrays, and exact
    enough that relabelling the colors changes nothing (the equivariance test)."""
    s_ = x[..., 0].astype(np.float64)
    for i_ in range(1, x.shape[-1]):
        s_ += x[..., i_]
    return s_


def _norm(x):
    """Rows to shares (a pie); an empty row becomes even."""
    x = np.maximum(x, 0.0); s_ = _csum(x)[..., None]
    return np.where(s_ > 1e-12, x / np.maximum(s_, 1e-12), 1.0 / C)


def overlap(p, q):
    """Fit between two pies: overlap, the same for every pair of colors."""
    return _csum(p * q)


def fit(p, q):
    """Centred overlap: 0 when either pie is even, up to C - 1 for one shared color."""
    return C * _csum(p * q) - 1.0


def likeness(p, q):
    """1 - half the L1 distance (the shared part, sum of min(p, q), for pies): 1 for the same pie, 0 for pies with
    no color in common. (Color by color: no (N, K, C) temporary; the same sum in the same order as _csum.)"""
    s_ = np.minimum(p[..., 0], q[..., 0]).astype(np.float64)
    for i_ in range(1, np.shape(p)[-1]):
        s_ += np.minimum(p[..., i_], q[..., i_])
    return s_


_LUT = np.unpackbits(np.arange(256, dtype=np.uint8)[:, None], axis=1, bitorder="little").astype(np.float32)
_LOWBIT = np.array([(b_ & -b_).bit_length() - 1 for b_ in range(256)], np.int64)   # lowest set bit (-1: none)
# a fixed personal view per person and norm key (-1.7..1.7), looked up by name index (deterministic, no draws)
_EPS = ((lambda e_: (e_ - np.floor(e_) - 0.5) * 3.4)(np.sin(np.arange(4096)[:, None] * 12.9898
                                                             + np.arange(len(NORM_KEYS)) * 78.233) * 43758.5453))


_NKI = {k_: i_ for i_, k_ in enumerate(NORM_KEYS)}
_EPS6 = (0.6 * _EPS).astype(np.float32)


def _ix(x):
    """Indices and counts as np.intp for numpy calls that cast them 'safe' (take, put, repeat, bincount, ufunc.at):
    int64 does not cast safely to a 32-bit intp (Pyodide, wasm32); a no-op on 64-bit CPython."""
    return np.asarray(x).astype(np.intp, copy=False)


def _nz2(m):
    """np.nonzero for a 2-D mask, faster (flat indices split into rows and columns)."""
    fl = np.flatnonzero(m)
    return fl // m.shape[1], fl % m.shape[1]


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def _logit(p):
    p = _uclip(p, 0.02, 0.98)
    return np.log(p / (1 - p))
