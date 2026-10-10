"""world_people.py: the per-character side of the outer world (chroma-world specs 2, 3 and 7; the interface is
chroma-engine/world-build.md, "world_people.py: what it exposes").

Vectorised over the run's N lives, all born in one shared World W at the same world week t0. Per life:
- drawn birth: locality, neighbourhood, family class, parents, siblings, grandparents, aunts, uncles and cousins
  (spec 3 §2.5b), from the society's population shares;
- the named cast (spec 2): up to K people with their own pies, the character's reading of them, closeness (which sets
  the layer), trust, contact, marks and debts, a light life of their own (age, health, money, partner, job, mood:
  ruling R8, no reduced engine per person) and at most one want toward the character;
- settings (spec 3 §1): household, class, work, congregation, club, scene, online, neighbours, gang, unit, ward and
  movement, with norms, cohesion, the character's rank and time share, members, leader, gate and exit cost;
- what the engine reads each week: niche, msg_w, support, belong, alive, community, ties, approval, standing and
  felt reach (spec 7 §2, §6);
- levers and pushes (spec 7 §3; reach per domain), `who` slots, wants due, place and moving (with candidate
  localities), emigration to a neighbour society and return (spec 5 §5: society id, status, language, harder gates at
  first), views for the game (cast, place, settings, reach, public figures through the character's reading), save and
  load.

Rules kept (world-build.md): fit between two pies is overlap or distance only, the same for every pair of colors;
one random stream per (world seed, run seed); the world's history is only touched through W.push; no years, names or
brands (names are integer indices the game maps); numpy and stdlib only.

Cadence (t: the world week): week (cast layers 1-2: contact, closeness, deaths; partner and children follow the
engine; wants ripen; niche, msg_w, support, help, belong, felt reach, contagion, events), month when t % 4 == 0 (the
life course of settings, contact in settings, the close index, standing and reach, community, ties, the alive friend
column; the settings' slow drift of norms, cohesion and strictness every second month), quarter when t % 13 == 0
(cast layers 3-4, the reading, trust and breaks, members' turnover, new people, roles, wants arising, the full alive
counts, local norm and approval; the cast's own light lives every half year). `tick(t, S)` runs all three on their
weeks; each is safe to call twice in a week.
"""
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
from world_keys import LEAD_WAYS

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
NW = len(CAST_WANTS)
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
    dist_far=0.3,        # share of a deliberate contact that reaches someone in another locality without remote tools;
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
                           lead_take=26.0, lead_crisis=26.0, lead_fall=26.0, lead_routine=26.0, lead_hand=26.0)[w_]
                      for w_ in CAST_WANTS])   # ripening a year (a far tie's call: within weeks)
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
               far_mixed=((0.08, 0.08), (-0.08, -0.05), None, None))
FARW = np.array([w_.startswith("far_") for w_ in CAST_WANTS])
# far_ties (item 18, chroma-ideas/far-off-events.md): start values, estimates refit in v22.3's one refit. hard, good: the
# sides' shares x these; call_*: the chance a touched tie among the ~15 closest, living in another town, calls; take:
# the share of the cast's random job loss, rehire and illness the towns' events take over (jobloss, rehire, illness);
# stay: weeks a tie taken in lives in the household; lapse: weeks an unanswered call waits; cause: weeks a later want
# carries the event that started it
FAR_DEFAULT = dict(hard=1.0, good=1.0, call_hard=0.75, call_good=0.5, call_mixed=0.75, take=(0.3, 0.3, 0.1), stay=52,
                   lapse=8, cause=104)
FAR_WHO = ("any", "in_work", "out_of_work", "owner", "renter", "poor", "comfortable", "young", "old", "ill", "parent")
FAR_OFF = 10 ** 9   # far_in: not taken in
# lead_ways (S7 "Ways to lead", chroma-ideas/social-mechanics.md, with "The leader's time in post" and "The falls in
# numbers"): start values for v22.3's one refit, estimates where the spec gives none. The time in post itself (term,
# renewal, consecutive terms, yearly end chance, age out, by post kind and epoch) and the fast-change line are the Outer
# world's (dynamics.json lead_posts, sphere_data.LEAD_POSTS). take: a quarter's chance that a pillar (rank .85 or more) of
# a setting with a leader takes the lead; take_age: from this age; rival: a quarter's chance that the setting's most
# standing member challenges (a rival of higher rung takes over); fall: legitimacy under this is a fall; rules .. favours,
# inspiring: the falls in numbers (the spec's; custom's is lead_posts.fast_change.loss_q); fair_line: the led's felt
# fairness under this is a fairness scandal; frail: health under this ends a post; sh, sh_years: the shadow target one
# way held sh_years adds to its colour (item 2, with shadows); fight: a fall fought and won leaves legitimacy here; again:
# weeks after standing down before the take chance doubles there; wait: weeks a post's moment waits to come; routine:
# yearly fades in a row after which the inspiring leader's turn to routine is offered in place of the crisis; ruler_end:
# the yearly end chance of a national office where there are no elections (held at the ruler's pleasure)
LEAD_DEFAULT = dict(take=0.05, take_age=18, rival=0.02, fall=0.2, rules=0.3, knowing=0.3, favours=0.4, inspiring=0.05,
                    fair_line=0.35, frail=0.35, sh=0.2, sh_years=10.0, fight=0.3, again=52, wait=8, routine=2, ruler_end=0.1)
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
LEAD_KINDS = ("work", "congregation", "club", "gang", "unit", "movement")   # settings a life can come to lead


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


class People:
    """The cast, settings, place and reach of N characters in one World (see the module docstring)."""

    def __init__(self, W, N, run_seed=0, female=None, cfg=None):
        P = dict(PP_DEFAULT); P.update(cfg or {}); self.P = P
        self.W = W; self.N = N = int(N); self.K = K = int(P["K"]); self.M = M = int(P["M"])
        self.KC = min(int(P["KC"]), K)
        self.seed = int(getattr(W, "seed", getattr(W, "_seed", 0))); self.run_seed = int(run_seed)
        self.rng = np.random.default_rng([self.seed, 31, self.run_seed])
        # color-indexed draws are made in the world's canonical frame and relabelled like every color table, so a
        # World(color_perm=p) gives the same lives with their colors relabelled (the equivariance test)
        cp = P.get("color_perm")
        self.perm = np.asarray(getattr(W, "perm", np.arange(C)) if cp is None else cp, np.int64)
        self.iperm = np.argsort(self.perm)
        self.female = (np.zeros(N, bool) if female is None else
                       np.broadcast_to(np.asarray(female, bool), (N,)).copy())
        z = lambda dt, v: np.full((N, K), v, dt)
        # the cast: one row per life, one column per slot
        i32 = np.int32   # ids, name indices and weeks fit in 32 bits (half the memory traffic of int64)
        self.used = z(bool, False); self.lv = z(bool, False); self.uid = z(i32, -1)
        self.nm = z(i32, 0); self.line = z(i32, 0); self.kof = z(i32, -1)
        self.role = z(np.int8, -1); self.rmask = z(np.int32, 0); self.face = z(bool, False)
        self.born = z(i32, 0); self.fem = z(bool, False); self.since = z(i32, 0); self.died_t = z(i32, NEVER)
        self.pie = np.full((N, K, C), 1.0 / C, np.float32); self.read = np.full((N, K, C), 1.0 / C, np.float32)
        self.c = z(np.float32, 0.0); self.cmax = z(np.float32, 0.0); self.trust = z(np.float32, 0.5)
        self.last = z(i32, NEVER); self.fsh = z(np.float32, 0.0); self.fkin = z(np.float32, 0.0)
        self.fkin_far = z(np.float32, 0.0); self.mset = z(np.uint8 if M <= 8 else np.uint16, 0)
        self.debt = z(np.int8, 0); self.mgood = z(np.uint8, 0); self.mbad = z(np.uint8, 0)
        self.secret = z(bool, False); self.brk = z(i32, NEVER)
        self.health = z(np.float32, 1.0); self.money = z(np.float32, 0.5); self.mcls = z(np.int8, 1)
        self.emp = z(bool, False); self.sector = z(np.int8, -1); self.inst = z(i32, -1)
        self.mpart = z(bool, False); self.nkids = z(np.int8, 0); self.mood = z(np.float32, 0.6)
        self.want = z(np.int8, -1); self.wripe = z(np.float32, 0.0); self.wstate = z(np.int8, 0)
        self.wknown = z(bool, False); self.wdue = z(i32, NEVER); self.stand = z(np.int8, 0)
        self.mloc = z(i32, 0); self.faith = z(np.int16, -1); self.party = z(i32, -1)
        self.strict = z(np.float32, 0.0); self.fbiz = z(bool, False); self.inci = z(bool, False)
        self.unext = np.zeros(N, np.int64)
        # settings
        assert M <= 8, "settings are a byte of bits per cast member"
        self.skind = np.full((N, M), -1, np.int8); self.snorm = np.full((N, M, C), 1.0 / C, np.float32)
        self.sanch = np.full((N, M, C), 1.0 / C, np.float32)
        self.scoh = np.zeros((N, M), np.float32); self.srank = np.zeros((N, M), np.float32)
        self.sts = np.zeros((N, M), np.float32); self.ssize = np.zeros((N, M), np.int64)
        self.sncast = np.zeros((N, M), np.int64); self.sgate = np.zeros((N, M), np.int8)
        self.sxcost = np.zeros((N, M), np.float32); self.sform = np.zeros((N, M), np.int64)
        self.sjoin = np.zeros((N, M), np.int64); self.sref = np.full((N, M), -1, np.int64)
        self.slead = np.full((N, M), -1, np.int64)   # leader's slot, -1 none, -2 the character
        self.sstrict = np.zeros((N, M), np.float32); self._fitm = np.zeros((N, M), np.float32)
        self._sh = np.arange(M, dtype=self.mset.dtype)[None, :, None]
        # the person
        self.loc = np.zeros(N, np.int64); self.nb = np.zeros(N, np.int64); self.cls = np.ones(N, np.int64)
        self.pfaith = np.full(N, -1, np.int64); self.pparty = np.full(N, -1, np.int64); self.pline = np.zeros(N, np.int64)
        self.hhj = np.full(N, -1, np.int64); self.own_home = np.zeros(N, bool); self.pslot = np.full(N, -1, np.int64)
        self.psector = np.full(N, -1, np.int64); self.n_moves = np.zeros(N, np.int64); self.last_move = np.full(N, NEVER)
        self.par_change = np.full(N, NEVER); self.older_sib = np.zeros(N, np.int64); self.younger_sib = np.zeros(N, np.int64)
        self.family_mix = np.full((N, C), 1.0 / C); self.vol_tgt = np.zeros(N, np.int64); self.sociab = np.ones(N)
        self.fr_bias = np.zeros(N); self.objk = np.zeros((N, NNORM)); self.cont_t = np.full((N, 2), NEVER)
        self.lens = np.full((N, C), 1.0 / C); self.w = np.full((N, C), 1.0 / C); self.w32 = self.w.astype(np.float32)
        self._lkm = np.zeros((N, K), np.float32); self._Dn = np.zeros(N, np.float32)
        self._psq = np.full((N, K), 1.0 / C, np.float32)   # each cast member's sum of squared shares (their spread)
        self.held = np.zeros((N, len(KN)), bool); self.dead = np.zeros(N, bool); self._nch = np.zeros(N, np.int64)
        self._nchl = np.zeros(N, np.int64)   # the character's living children in the cast
        self.kids_eng = None                 # the engine's living children (S["children"]), when it sends them
        # what the engine reads
        self.niche = np.full((N, C), 1.0 / C); self.msg_w = np.ones(N); self.support = np.zeros(N); self.help = np.zeros(N)
        self.belong = np.zeros(N); self.alive = np.zeros((N, len(ENGINE_ROLES))); self.community = np.zeros(N)
        self.ties = np.zeros(N); self.approval = np.zeros((N, NNORM)); self.local_norm = np.full((N, NNORM), 0.5)
        self.standing = np.zeros((N, 4)); self.reach = np.tile(REACH[0], (N, 1)); self.felt_reach = self.reach.copy()
        self.dstanding = np.zeros((N, len(DOMAINS))); self.dreach = np.tile(REACH[0][RING_OF], (N, 1))
        self.died = np.zeros((N, len(ENGINE_ROLES)), np.int64)
        self.contagion = dict(divorce=np.ones(N), quit=np.ones(N))
        self.events = []; self._carry = []; self._due = []; self.pend = {}
        self._setmix = np.zeros((N, C)); self._setw = np.zeros(N); self._belong_set = np.zeros(N); self._comm = np.zeros(N)
        self._den = np.ones(N); self.ci = np.zeros((N, self.KC), np.int64)
        self._r_w = [np.float32(1 - np.exp(-1 / 52.0 / P[k_])) for k_ in ("tau_up", "tau_dn_kin", "tau_dn")]
        ma_ = P["move_age"]   # yearly moving rate by whole year of age (the table's line at mid-year)
        self._mr_tab = np.interp(np.arange(121) + 0.5, [a_ for a_, _ in ma_], [r_ for _, r_ in ma_]).astype(np.float32)
        self._last_m = self._last_q = self._last_w = self._last_appr = self._last_set = None; self._defer = None
        self._last_lives = 0
        self.t0 = 0; self.t = 0
        self.watch = np.ones(N, bool) if P["watch"] is None else np.isin(np.arange(N), np.asarray(P["watch"]))
        self.nh = []; self._coh_tab = None; self._coh_y0 = 0
        self._kf_near = np.array([P["kin_f"].get(r_, (0, 0))[0] for r_ in ROLE], np.float32)
        self._kf_far = np.array([P["kin_f"].get(r_, (0, 0))[1] for r_ in ROLE], np.float32)
        self.res = np.full((N, len(RESOURCES)), 0.5); self.stress = np.zeros(N); self.outlook = np.full(N, 0.45)
        self.attr = np.zeros(N, np.int64); self.risky = np.zeros(N); self.title_st = None; self.partner_same = None
        self.dom_st = None
        # the society each life lives in (spec 5 §5): its id (0 home; a neighbour its index + 1), the life's status
        # there, its language skill; per cast member, the society they live in (msoc)
        hs = self._wf("society_id", 0); hs = int(hs) if np.ndim(hs) == 0 else 0
        self.soc = np.full(N, hs, np.int64); self.soc_home = self.soc.copy()
        self.stat = np.zeros(N, np.int8); self.lang = np.ones(N); self.arr_t = np.full(N, NEVER)
        self.cls_home = np.ones(N, np.int64); self.loc_home = np.zeros(N, np.int64); self.par_apart = np.zeros(N, bool)
        self.msoc = z(np.int16, hs)
        self._xsoc = False   # True once a life has lived abroad: only then are societies compared (home lives unchanged)
        self._smem = {}      # (life, society id): (language, status) kept for a return
        self._Ws = {}        # N == 1: the Worlds left behind, by society id
        self._world_static()
        # the spheres of society, phase 2 (item 15): the world's switches decide; off, none of this exists
        wp_ = getattr(W, "p", None) or {}
        self.sph_h = bool(wp_.get("sph_haunts", False)); self.sph_hr = bool(wp_.get("sph_hours", False))
        self.sph_mk = bool(wp_.get("sph_marks", False))
        if self.sph_h or self.sph_hr or self.sph_mk:
            self._sph_init()
        # phase 4: the levers on places and town spheres, and felt fairness per sphere (each off: nothing of it exists)
        self.sph_lv = bool(wp_.get("sph_levers", False)); self.sph_fr = bool(wp_.get("sph_fair", False))
        if wp_.get("sph_deep", False):   # phase 5, service as a chapter: comrades met in a unit fade at half speed
            self.comrade = np.zeros((N, K), bool)
            self.roots = np.zeros(N, bool)       # debts and holdings: a life holding something moves half as readily
            self.care_buy = np.zeros(N, bool)    # a carer with money buys help (the engine sets it each month)
        self.far_on = bool(wp_.get("far_ties", False))
        if self.far_on:   # far_ties (item 18): the towns' events touch the people living there; a far tie calls
            self._far_init(run_seed)
        self.lw = bool(wp_.get("lead_ways", False)) and self.sph_lv   # S7: ways to lead, with phase 4's levers
        if self.lw:
            self._lead_init()
        if self.sph_lv or self.sph_fr:
            self.fair = np.full((N, 9), 0.5)    # felt fairness in each sphere, 0..1 (sph_fair)
            self.fair_log = []                  # [week, life, sphere, +1 went well / -1 badly]: voice and loyalty acts
            self._p4_yr = -1

    # ------------------------------------------------------------------ the world, read through world-build.md's names
    def _world_static(self):
        W = self.W
        ps = np.asarray(W.loc_pop_share, float); self.n_loc = len(ps); self.loc_p = ps / ps.sum()
        self.n_nb = len(np.asarray(W.nb_loc))
        fs = np.asarray(getattr(W, "faith_share", np.zeros(0)), float); self.n_faith = len(fs)
        sec = getattr(W, "secular", None)
        p_none = float(sec) if sec is not None and np.ndim(sec) == 0 else max(0.0, 1.0 - fs.sum())
        pf = np.concatenate([[p_none], fs * (1 - p_none) / max(fs.sum(), 1e-9)]) if len(fs) else np.ones(1)
        self.faith_p = pf / pf.sum()
        self._inst_refresh()

    def _inst_refresh(self):
        W = self.W
        ik = np.asarray(getattr(W, "inst_kind", []))
        if ik.dtype.kind in "US" or ik.dtype == object:
            ik = np.array([INST_KINDS.index(k_) if k_ in INST_KINDS else -1 for k_ in ik], np.int64)
        self.inst_kind = ik.astype(np.int64); self.inst_loc = np.asarray(getattr(W, "inst_loc", np.zeros(len(ik))), np.int64)
        self.parties = np.nonzero(self.inst_kind == INST_KINDS.index("party"))[0]
        isec = getattr(W, "inst_sector", None)
        self.inst_sector = None if isec is None else np.asarray(isec)

    def _wf(self, name, default):
        v = getattr(self.W, name, default)
        return default if v is None else v

    @property
    def status(self):
        """Each life's status in the society it lives in: "citizen", "migrant" or "resident"."""
        return np.array(STATUS)[self.stat]

    def _here(self, n, k):
        """Cast members (n, k) living in the character's locality (and society)."""
        h = self.mloc[n, k] == self.loc[n]
        return h & (self.msoc[n, k] == self.soc[n]) if self._xsoc else h

    def _unemp(self, name, default=0.05):
        """Unemployment as a share (world.py keeps it in percent)."""
        v = np.asarray(self._wf(name, default), float)
        return v / 100.0 if v.size and np.nanmax(v) > 1.0 else v

    def _rate(self, kind, locs=None):
        try:
            v = self.W.rate_mult(kind)
        except Exception:
            return 1.0
        v = np.asarray(v, float)
        if v.ndim == 0 or locs is None:
            return float(v) if v.ndim == 0 else v
        return v[_uclip(locs, 0, len(v) - 1)]

    def _cohort(self, born):
        """The generation's mix for each birth week (a table by birth year; a generation still under 26 is read
        again each quarter, since the world can still change it)."""
        yr = np.floor_divide(np.asarray(born, np.int64), 52)
        if yr.size == 0:   # nobody to draw (an only child has no siblings): an empty table of mixes
            return np.zeros(yr.shape + (C,))
        lo, hi = int(yr.min()), int(yr.max())
        tb = self._coh_tab
        if tb is None or lo < self._coh_y0 or hi >= self._coh_y0 + len(tb[0]):   # (re)grow the table
            y0 = min(lo, self._coh_y0 if tb is not None else lo) - 10
            y1 = max(hi, self._coh_y0 + len(tb[0]) - 1 if tb is not None else hi) + 10
            nt = (np.zeros((y1 - y0 + 1, C)), np.full(y1 - y0 + 1, -1, np.int64))
            if tb is not None:
                nt[0][self._coh_y0 - y0:self._coh_y0 - y0 + len(tb[0])] = tb[0]
                nt[1][self._coh_y0 - y0:self._coh_y0 - y0 + len(tb[0])] = tb[1]
            self._coh_tab = tb = nt; self._coh_y0 = y0
        q = self.t // 13
        row = yr - self._coh_y0
        uq = np.unique(row)
        need = uq[(tb[1][uq] < 0) | ((tb[1][uq] != q) & ((self.t - (uq + self._coh_y0) * 52) <= 26 * 52))]
        for r_ in need.tolist():
            try:
                v_ = np.asarray(self.W.cohort_mix(int((r_ + self._coh_y0) * 52 + 26)), float)
            except Exception:
                v_ = np.asarray(self.W.V, float)
            tb[0][r_] = _norm(v_); tb[1][r_] = q
        return tb[0][row]

    def _popmean(self, loc, born):
        lm = np.asarray(self.W.loc_mix, float)[loc]
        return _norm(self.P["pw_loc"] * _norm(lm) + self.P["pw_coh"] * self._cohort(born))

    def _dirichlet(self, m, conc=None):
        a_ = np.maximum(m, 0.002) * (self.P["conc"] if conc is None else conc) * C
        g_ = self.rng.standard_gamma(a_[..., self.iperm])[..., self.perm]
        return _norm(g_ + 1e-12)

    def _party_of(self, pie):
        if not len(self.parties):
            return np.full(len(pie), -1, np.int64)
        prof = _norm(np.asarray(self.W.inst_profile, float)[self.parties])
        sc = pie @ prof.T + 0.05 * self.rng.gumbel(size=(len(pie), len(self.parties)))
        out = self.parties[np.argmax(sc, 1)]
        return np.where(self.rng.random(len(pie)) < 0.35, -1, out)   # about a third hold no party

    def _faith_draw(self, E):
        return self.rng.choice(len(self.faith_p), E, p=self.faith_p) - 1

    def _class_draw(self, loc):
        cm = np.asarray(self.W.loc_class_mix, float)[loc]
        cm = np.cumsum(cm / cm.sum(1, keepdims=True), 1)
        return np.minimum((self.rng.random(len(loc))[:, None] > cm).sum(1), 2)

    def _q(self, age, health=None, mcls=None):
        """Yearly death chance by age, health and class (life table); float32 for float32 ages."""
        c_, a_, b_ = self.P["mort"]
        age = np.asarray(age)
        q_ = c_ + a_ * np.exp(b_ * age)
        if mcls is not None:
            q_ = q_ * np.take(np.asarray(self.P["mort_cls"], q_.dtype), _ix(mcls), mode="clip")
        if health is not None:
            q_ = q_ * (0.6 + 0.8 * (1 - health))
        return np.minimum(q_, 0.9)

    def _rate_at(self, kind, locs):
        """W.rate_mult(kind) at each location in locs (float32; a scalar when the world gives one)."""
        v = self._rate(kind)
        if np.ndim(v) == 0:
            return np.float32(v)
        return np.take(np.asarray(v, np.float32), _ix(locs), mode="clip")

    def _surv(self, a1, a2):
        c_, a_, b_ = self.P["mort"]
        H_ = lambda x: c_ * x + a_ / b_ * (np.exp(b_ * x) - 1)
        return np.exp(-(H_(np.asarray(a2, float)) - H_(np.asarray(a1, float))))

    def _age(self, t=None):
        return ((self.t if t is None else t) - self.t0) / 52.0

    def _mage(self, t=None):
        return ((self.t if t is None else t) - self.born) / 52.0

    # ------------------------------------------------------------------ adding and dropping people
    def _gen(self, n, born, t, loc=None, ctx=None, sel=0.0, mcls=None, p_same_cls=0.0):
        """Fields for len(n) new people met by lives n, born in weeks born; ctx: a mix they share (a setting's norms,
        a family's ways) with weight sel."""
        rng = self.rng; E = len(n); P = self.P
        n = np.asarray(n, np.int64); born = np.asarray(born, np.int64)
        loc = self.loc[n] if loc is None else np.asarray(loc, np.int64)
        if ctx is not None and sel >= 1:
            m_ = _norm(np.asarray(ctx, float))
        else:
            m_ = self._popmean(loc, born)
            if ctx is not None:
                m_ = _norm((1 - sel) * m_ + sel * np.asarray(ctx, float))
        pie = self._dirichlet(m_)
        age = (t - born) / 52.0
        cl = self._class_draw(loc)
        if mcls is not None:
            cl = np.where(rng.random(E) < p_same_cls, mcls, cl)
        adult = age >= 18
        emp = adult & (age < 65) & (rng.random(E) < 0.78)
        ls = np.asarray(self._wf("loc_sectors", np.full((self.n_loc, len(SECTORS)), 0.2)), float)[loc]
        ls = np.cumsum(ls / np.maximum(ls.sum(1, keepdims=True), 1e-9), 1)
        sec = np.minimum((rng.random(E)[:, None] > ls).sum(1), len(SECTORS) - 1)
        sec = np.where(age >= 16, sec, -1)
        pp_ = np.interp(age, [18, 25, 32, 45, 65, 80], [0.05, 0.35, 0.6, 0.68, 0.65, 0.45])
        mpart = adult & (rng.random(E) < pp_)
        nk = np.where(age > 24, rng.poisson(_uclip((age - 24) / 10, 0, 1.8)), 0)
        hb = _uclip(1 - 0.012 * np.maximum(0, age - 35), 0.2, 1)
        health = _uclip(hb - 0.1 * rng.random(E), 0.05, 1)
        money = _uclip(np.array([0.3, 0.5, 0.75])[cl] + 0.1 * emp - 0.15 * (adult & (age < 65) & ~emp)
                        + 0.08 * rng.standard_normal(E), 0.02, 1)
        stand = np.where(adult, rng.choice(4, E, p=P["stand_p"]), 0)
        return dict(n=n, born=born, pie=pie, fem=rng.random(E) < 0.5, mloc=loc, mcls=cl, emp=emp, sector=sec,
                    mpart=mpart, nkids=np.minimum(nk, 6), health=health, money=money, stand=stand,
                    faith=self._faith_draw(E), party=self._party_of(pie),
                    strict=rng.standard_normal(E) + P["strict_age"] * (age - 40),
                    nm=rng.integers(0, 2 ** 31 - 1, E), line=rng.integers(0, 2 ** 31 - 1, E))

    def _add(self, F, t, role, c0=0.05, trust0=0.5, setbit=None, ctx_read=None, acc0=0.1, face=False,
             alive=True, kof=None, quiet=False, via=None):
        """Put the people in F (from _gen, optionally edited) into free slots of their lives; returns the slots."""
        n = np.asarray(F["n"], np.int64); E = len(n)
        if E == 0:
            return np.zeros(0, np.int64)
        P = self.P; rng = self.rng
        order = np.argsort(n, kind="stable"); n_s = n[order]
        first = np.searchsorted(n_s, n_s); rank_s = np.arange(E) - first
        rank = np.empty(E, np.int64); rank[order] = rank_s
        un, cnt = np.unique(n, return_counts=True)
        nfree = (~self.used[un]).sum(1)
        if (nfree < cnt).any():
            self._evict(un[nfree < cnt], (cnt - nfree)[nfree < cnt], t)
        free = ~self.used[un]                                 # the free slots of each life, in order
        nfree = free.sum(1); fl = np.flatnonzero(free)
        start = np.concatenate([[0], np.cumsum(nfree)[:-1]])
        inv = np.searchsorted(un, n)
        ok = rank < nfree[inv]
        slot = fl[start[inv[ok]] + rank[ok]] % self.K
        n = n[ok]
        sl = lambda a_: (np.asarray(a_)[ok] if np.ndim(a_) else np.full(len(n), a_))
        role = sl(role); rm = (1 << role.astype(np.int64)).astype(np.int32)
        self.used[n, slot] = True; self.lv[n, slot] = sl(alive)
        self.uid[n, slot] = self.unext[n] + rank[ok]
        np.add.at(self.unext, _ix(un), cnt)
        self.role[n, slot] = role; self.rmask[n, slot] = rm; self.face[n, slot] = face
        for k_ in ("born", "fem", "mloc", "mcls", "emp", "sector", "mpart", "nkids", "health", "money", "stand", "faith",
                   "party", "strict", "nm", "line"):
            getattr(self, k_)[n, slot] = sl(F[k_])
        self.pie[n, slot] = sl(F["pie"]) if np.ndim(F["pie"]) == 2 else F["pie"]
        self._psq[n, slot] = _csum(self.pie[n, slot] ** 2)
        self.fbiz[n, slot] = sl(F.get("fbiz", False))
        self.kof[n, slot] = -1 if kof is None else sl(kof)
        self.since[n, slot] = t; self.died_t[n, slot] = np.where(sl(alive), NEVER, t)
        c0 = _uclip(sl(c0), 0, 1); self.c[n, slot] = c0; self.cmax[n, slot] = c0
        self.trust[n, slot] = sl(trust0); self.last[n, slot] = t
        self.debt[n, slot] = 0; self.mgood[n, slot] = 0; self.mbad[n, slot] = 0; self.secret[n, slot] = False
        if getattr(self, "comrade", None) is not None:
            self.comrade[n, slot] = False
        if self.far_on:
            self.far_ev[n, slot] = -1; self.far_t[n, slot] = NEVER; self.far_sg[n, slot] = 0; self.far_sd[n, slot] = -1
            self.far_in[n, slot] = FAR_OFF; self.far_from[n, slot] = -1
        self.brk[n, slot] = NEVER; self.mood[n, slot] = 0.6; self.want[n, slot] = -1; self.wripe[n, slot] = 0
        self.wstate[n, slot] = 0; self.wknown[n, slot] = False; self.wdue[n, slot] = NEVER; self.inci[n, slot] = False
        self.inst[n, slot] = sl(F.get("inst", -1))
        self.msoc[n, slot] = sl(F["msoc"]) if "msoc" in F else self.soc[n]
        self.mset[n, slot] = 0
        if setbit is not None:
            sb = sl(setbit)
            self.mset[n, slot] = np.where(sb >= 0, 1 << np.maximum(sb, 0), 0).astype(self.mset.dtype)
        self.fkin[n, slot] = self._kf_near[role]; self.fkin_far[n, slot] = self._kf_far[role]
        # the character's first reading: the context they met in, the character's own lens, and noise; a little truth
        lmx = np.asarray(self.W.loc_mix, float)
        ctx = (lmx[np.minimum(self.mloc[n, slot], len(lmx) - 1)] if ctx_read is None
               else sl(ctx_read) if np.ndim(ctx_read) == 2 else np.tile(np.asarray(ctx_read, float), (len(n), 1)))
        prior = _norm(0.35 * _norm(ctx) + 0.35 * self.lens[n] + 0.3 * self._dirichlet(np.full((len(n), C), 1.0 / C), 1.0))
        a0 = sl(acc0)[:, None]
        self.read[n, slot] = (1 - a0) * prior + a0 * self.pie[n, slot]
        self._lkm[n, slot] = likeness(self.pie[n, slot], self.w32[n])
        if np.ndim(quiet):   # one flag per person: the events of those met openly
            q_ = sl(quiet)
            if not q_.all():
                self._ev_join(n[~q_], slot[~q_], t, via)
        elif not quiet:
            self._ev_join(n, slot, t, via)
        full = np.full(E, -1, np.int64); full[ok] = slot
        return full

    def _ev_join(self, n, slot, t, via):
        wn = self.watch[n]
        if not wn.any():
            return
        if via is not None:   # a group of people met at once: one event per life
            for n_ in np.unique(n[wn]):
                ss = slot[n == n_]
                self.events.append(dict(n=int(n_), t=int(t), kind="joined", via=via, cids=[int(x_) for x_ in self.uid[n_, ss]]))
            return
        for n_, s_ in zip(n[wn], slot[wn]):
            self.events.append(dict(n=int(n_), t=int(t), kind="joined", cid=int(self.uid[n_, s_]), role=self._rname(n_, s_)))

    def _evict(self, ns, need, t):
        """Make room in lives ns for need[i] people: the least tied go back to the statistics (faces, the long dead,
        faded acquaintances first; kin, the core and the partner last or never)."""
        ns = np.asarray(ns, np.int64); need = np.asarray(need, np.int64)
        rm = self.rmask[ns]
        sc = (self.c[ns] + 2.0 * ((rm & KINMASK) != 0) + 3.0 * ((rm & CORE) != 0)
              + 0.3 * ((self.mgood[ns] > 0) | (self.mbad[ns] > 0)) + 0.5 * (self.mset[ns] > 0) + 1.0 * self.inci[ns]
              - 1.0 * self.face[ns] - 1.5 * (~self.lv[ns] & ((t - self.died_t[ns]) > 5 * 52)))
        sc = np.where(self.used[ns], sc, np.inf)
        ps = self.pslot[ns]; hp = ps >= 0
        sc[np.nonzero(hp)[0], ps[hp]] = np.inf
        order = np.argsort(sc, 1, kind="stable")
        r_, p_ = np.nonzero(np.arange(self.K)[None, :] < need[:, None])
        k_ = order[r_, p_]
        ok = np.isfinite(sc[r_, k_])
        self._drop(ns[r_[ok]], k_[ok], t, quiet=True)

    def _drop(self, n, k, t, quiet=False):
        n = np.asarray(n, np.int64); k = np.asarray(k, np.int64)
        if not len(n):
            return
        if not quiet:
            sel = self.watch[n] & (self.cmax[n, k] >= self.P["layer_c"][2]) & self.lv[n, k]
            for n_, k_ in zip(n[sel], k[sel]):
                self.events.append(dict(n=int(n_), t=int(t), kind="left", cid=int(self.uid[n_, k_]), role=self._rname(n_, k_)))
        self.used[n, k] = False; self.lv[n, k] = False; self.mset[n, k] = 0; self.want[n, k] = -1; self.uid[n, k] = -1
        self.wstate[n, k] = 0; self.inci[n, k] = False; self.c[n, k] = 0; self.rmask[n, k] = 0; self.role[n, k] = -1
        for j_ in range(self.M):
            hit = self.slead[n, j_] == k
            self.slead[n[hit], j_] = -1
        hit = self.pslot[n] == k
        self.pslot[n[hit]] = -1

    def _rnames(self, n, k):
        """_rname for many (n, k) at once."""
        rm = self.rmask[n, k]; out = np.full(len(rm), -1)
        for i_ in range(len(ROLE_ORDER) - 1, -1, -1):
            out = np.where((rm & BIT[ROLE_ORDER[i_]]) != 0, i_, out)
        ro = self.role[n, k]
        return [ROLE_ORDER[i_] if i_ >= 0 else ROLE[r_] if r_ >= 0 else "acquaintance" for i_, r_ in zip(out.tolist(), ro.tolist())]

    def _evs(self, n, k, t, kind, **kw):
        """Events of one kind about cast members (n, k) of watched lives."""
        w_ = self.watch[n]; n, k = n[w_], k[w_]
        if len(n):
            self.events.extend(dict(n=n_, t=int(t), kind=kind, cid=u_, role=r_, **kw)
                               for n_, u_, r_ in zip(n.tolist(), self.uid[n, k].tolist(), self._rnames(n, k)))

    def _rname(self, n, k):
        m_ = int(self.rmask[n, k])
        for r_ in ROLE_ORDER:
            if m_ & BIT[r_]:
                return r_
        return ROLE[int(self.role[n, k])] if self.role[n, k] >= 0 else "acquaintance"

    def _slot(self, n, cid):
        hit = np.nonzero(self.used[n] & (self.uid[n] == cid))[0]
        return int(hit[0]) if len(hit) else -1

    # ------------------------------------------------------------------ birth (spec 3 §2.5b)
    def birth(self, t0, legacy=None):
        """Locality, neighbourhood, class, parents and the born-into cast, drawn from the society's population shares.
        legacy: a dict from save() (or one per life): the birth is placed in that family line."""
        self.t0 = t0 = int(t0); self.t = t0; self._last_lives = t0
        N = self.N; P = self.P; rng = self.rng; W = self.W
        self.loc = rng.choice(self.n_loc, N, p=self.loc_p)
        self.cls = self._class_draw(self.loc)
        self._pick_nb(np.arange(N))
        self.fr_bias = P["fr_bias"] * rng.standard_normal(N)
        lo_, hi_ = P["soc_spread"]
        self.sociab = np.exp(rng.uniform(np.log(lo_), np.log(hi_), N))
        self.vol_tgt = rng.choice(3, N, p=[0.25, 0.5, 0.25])
        allN = np.arange(N)
        # parents: the mother first, then a partner chosen alike (assortative: the best of five)
        am = _uclip(rng.normal(30.5, 5.2, N), 17, 46); af = _uclip(am + rng.normal(2.5, 4.0, N), 18, 62)
        Fm = self._gen(allN, t0 - (am * 52).astype(np.int64), t0); Fm["fem"][:] = True
        Ff = self._gen(allN, t0 - (af * 52).astype(np.int64), t0, mcls=self.cls, p_same_cls=0.8); Ff["fem"][:] = False
        cands = np.stack([self._dirichlet(self._popmean(self.loc, Ff["born"])) for _ in range(5)], 1)
        Ff["pie"] = cands[allN, np.argmax(overlap(cands, Fm["pie"][:, None, :]), 1)]
        for F_ in (Fm, Ff):
            F_["mcls"][:] = self.cls; F_["mpart"][:] = True; F_["mloc"][:] = self.loc
        fam_f = self._faith_draw(N)
        Fm["faith"] = fam_f; Ff["faith"] = np.where(rng.random(N) < 0.8, fam_f, self._faith_draw(N))
        Ff["party"] = np.where(rng.random(N) < 0.6, Fm["party"], Ff["party"])
        Fm["fbiz"] = rng.random(N) < P["p_biz"] / 2; Ff["fbiz"] = rng.random(N) < P["p_biz"] / 2
        sep = rng.random(N) < P["p_sep"]
        self.pfaith = fam_f.astype(np.int64); self.pparty = Fm["party"].astype(np.int64); self.pline = Ff["line"].copy()
        self.family_mix = _norm(0.5 * (Fm["pie"] + Ff["pie"]))
        Ff["line"] = self.pline
        sm = self._add(Fm, t0, R["parent"], c0=0.95, trust0=0.9, acc0=0.2, quiet=True)
        sf = self._add(Ff, t0, R["parent"], c0=np.where(sep, 0.45, 0.92), trust0=0.85, acc0=0.2, quiet=True)
        self.mloc[allN[sep], sf[sep]] = np.where(rng.random(sep.sum()) < 0.6, self.loc[sep],
                                                  rng.choice(self.n_loc, sep.sum(), p=self.loc_p))
        # siblings (the engine's distribution); older ones are here, younger ones are born later
        nsib = rng.choice(4, N, p=P["sib_p"])
        older = np.floor(rng.random(N) * (nsib + 1)).astype(np.int64)
        self.older_sib = older; self.younger_sib = nsib - older
        gaps = 1.5 + rng.gamma(2.0, 0.8, (N, 3))
        sib_n, sib_b = [], []
        for i_ in range(3):
            o_ = older > i_
            sib_n.append(allN[o_]); sib_b.append(t0 - (gaps[o_, :i_ + 1].sum(1) * 52).astype(np.int64))
        sib_n = np.concatenate(sib_n); sib_b = np.concatenate(sib_b)
        ok_ = (am[sib_n] - (t0 - sib_b) / 52) >= 16
        sib_n, sib_b = sib_n[ok_], sib_b[ok_]
        Fs = self._gen(sib_n, sib_b, t0, ctx=self.family_mix[sib_n], sel=P["pie_inherit"])
        Fs["mcls"][:] = self.cls[sib_n]; Fs["mloc"][:] = self.loc[sib_n]; Fs["line"][:] = self.pline[sib_n]
        self._inherit(Fs, self.pfaith[sib_n], self.pparty[sib_n])
        ss = self._add(Fs, t0, R["sibling"], c0=0.7, trust0=0.7, acc0=0.2, quiet=True)
        for i_ in range(3):
            y_ = self.younger_sib > i_
            for n_, b_ in zip(allN[y_], t0 + ((gaps[y_, :i_ + 1].sum(1)) * 52).astype(np.int64)):
                if am[n_] + (b_ - t0) / 52 <= 44:
                    self.pend.setdefault(int(b_), []).append((int(n_), "sibling"))
        # grandparents: alive now if they lived through the years since the parent was born
        gp_n, gp_b, gp_f, gp_s, gp_l, gp_fa, gp_pa = [], [], [], [], [], [], []
        for par_age, par_pie, par_line, F_ in ((am, Fm["pie"], Fm["line"], Fm), (af, Ff["pie"], self.pline, Ff)):
            ga = par_age + _uclip(rng.normal(28, 5, N), 17, 45)
            for fem_, gage in ((True, ga), (False, ga + rng.normal(2.5, 3.5, N))):
                live = rng.random(N) < self._surv(gage - par_age, gage)
                gp_n.append(allN[live]); gp_b.append(t0 - (gage[live] * 52).astype(np.int64)); gp_f.append(np.full(live.sum(), fem_))
                gp_s.append(par_pie[live]); gp_l.append(par_line[live]); gp_fa.append(F_["faith"][live]); gp_pa.append(F_["party"][live])
        gp_n = np.concatenate(gp_n)
        Fg = self._gen(gp_n, np.concatenate(gp_b), t0, ctx=np.concatenate(gp_s), sel=P["pie_inherit"])
        Fg["fem"] = np.concatenate(gp_f); Fg["line"] = np.concatenate(gp_l)
        self._inherit(Fg, np.concatenate(gp_fa), np.concatenate(gp_pa))
        far = rng.random(len(gp_n)) < 0.4
        Fg["mloc"] = np.where(far, rng.choice(self.n_loc, len(gp_n), p=self.loc_p), self.loc[gp_n])
        Fg["mpart"][:] = True
        self._add(Fg, t0, R["grandparent"], c0=np.where(far, 0.2, 0.35), trust0=0.7, acc0=0.15, quiet=True)
        # aunts and uncles (the parents' siblings, some with partners) and their children, the cousins
        au_n, au_b, au_s, au_l, au_k, au_f, au_p = [], [], [], [], [], [], []
        for par_age, F_, par_line, par_slot in ((am, Fm, Fm["line"], sm), (af, Ff, self.pline, sf)):
            k_ = rng.choice(4, N, p=P["sib_p"])
            for i_ in range(3):
                h_ = k_ > i_
                au_n.append(allN[h_]); au_b.append(t0 - ((par_age[h_] + rng.normal(0, 4, h_.sum())) * 52).astype(np.int64))
                au_s.append(F_["pie"][h_]); au_l.append(par_line[h_]); au_k.append(self.uid[allN[h_], par_slot[h_]])
                au_f.append(F_["faith"][h_]); au_p.append(F_["party"][h_])
        au_n = np.concatenate(au_n); au_b = np.concatenate(au_b)
        Fa = self._gen(au_n, au_b, t0, ctx=np.concatenate(au_s), sel=P["pie_inherit"])
        Fa["line"] = np.concatenate(au_l)
        self._inherit(Fa, np.concatenate(au_f), np.concatenate(au_p))
        livea = rng.random(len(au_n)) < self._surv(20, (t0 - au_b) / 52)
        far = rng.random(len(au_n)) < 0.4
        Fa["mloc"] = np.where(far, rng.choice(self.n_loc, len(au_n), p=self.loc_p), self.loc[au_n])
        Fa = {k2: (v2[livea] if np.ndim(v2) else v2) for k2, v2 in Fa.items()}
        sa = self._add(Fa, t0, R["kin"], c0=np.where(far[livea], 0.06, 0.12), trust0=0.6, kof=np.concatenate(au_k)[livea], quiet=True)
        an = Fa["n"]
        sp_ = rng.random(len(an)) < 0.6
        Fp = self._gen(an[sp_], Fa["born"][sp_] + (rng.normal(0, 3, sp_.sum()) * 52).astype(np.int64), t0)
        Fp["mloc"] = Fa["mloc"][sp_]; Fp["mpart"][:] = True; Fp["fem"] = ~Fa["fem"][sp_]
        self._add(Fp, t0, R["kin"], c0=0.05, trust0=0.5, kof=self.uid[an[sp_], sa[sp_]], quiet=True)
        nco = rng.choice(4, len(an), p=[0.25, 0.3, 0.3, 0.15])
        nco = _ix(nco); co_n = np.repeat(an, nco); co_src = np.repeat(np.arange(len(an)), nco)
        co_b = np.minimum(t0 + (rng.normal(-1, 5, len(co_n)) * 52).astype(np.int64), t0)
        Fc = self._gen(co_n, co_b, t0, ctx=Fa["pie"][co_src], sel=P["pie_inherit"])
        Fc["mloc"] = Fa["mloc"][co_src]; Fc["line"] = Fa["line"][co_src]
        self._inherit(Fc, Fa["faith"][co_src], Fa["party"][co_src])
        self._add(Fc, t0, R["kin"], c0=np.where(Fc["mloc"] == self.loc[co_n], 0.08, 0.04), trust0=0.55,
                  kof=self.uid[co_n, sa[co_src]], quiet=True)
        # the household: the parents (unless apart) and the older siblings
        for n_ in range(N):
            j_ = self._new_setting(n_, "household", t0)
            self.hhj[n_] = j_
        bit = np.uint8(1) if self.mset.dtype == np.uint8 else np.uint16(1)
        hj = self.hhj
        self.mset[allN, sm] |= (bit << hj).astype(self.mset.dtype)
        self.mset[allN[~sep], sf[~sep]] |= (bit << hj[~sep]).astype(self.mset.dtype)
        self.mset[sib_n, ss] |= (bit << hj[sib_n]).astype(self.mset.dtype)
        self.snorm[allN, hj] = self.family_mix; self.sanch[allN, hj] = self.family_mix
        if legacy is not None:
            for n_ in range(N):
                lg = legacy[n_] if isinstance(legacy, (list, tuple)) else legacy
                if lg:
                    self._legacy(n_, lg, t0)
        self._fsh(); self._close_index(); self._alive_counts(np.arange(N)); self._outputs_settings(); self._approval(t0)
        # the drawn birth is delivered with the first week's events (the engine takes events after a week; held back
        # here so that it arrives exactly once, whoever reads PP.events)
        self._carry = [dict(n=int(n_), t=t0, kind="born", loc=int(self.loc[n_]), nb=int(self.nb[n_]), cls=int(self.cls[n_]))
                       for n_ in range(N) if self.watch[n_]]
        self.events = []
        self.cls_home = np.asarray(self.cls, np.int64).copy(); self.loc_home = np.asarray(self.loc, np.int64).copy()
        self.par_apart = np.asarray(sep, bool).copy()

    def _pick_nb(self, ns):
        nbl = np.asarray(self.W.nb_loc, np.int64); nbc = np.asarray(self._wf("nb_class", np.ones(len(nbl))), np.int64)
        for n_ in ns:
            cand = np.nonzero(nbl == self.loc[n_])[0]
            if not len(cand):
                self.nb[n_] = -1; continue
            wt = np.where(nbc[cand] == self.cls[n_], 4.0, 1.0)
            self.nb[n_] = int(self.rng.choice(cand, p=wt / wt.sum()))

    def _legacy(self, n, lg, t):
        """A legacy line: one of the ancestor's grown children becomes a parent; the ancestor and their partner are
        grandparents; the ancestor's other children are aunts and uncles; their children are cousins."""
        cast = lg.get("cast", [])
        kids = [m_ for m_ in cast if "child" in m_.get("roles", []) and m_.get("alive") and 18 <= (t - m_["born"]) / 52 <= 46]
        if not kids:
            self.loc[n] = int(_uclip(lg.get("loc", self.loc[n]), 0, self.n_loc - 1)); return
        par = kids[int(self.rng.integers(len(kids)))]
        self.loc[n] = int(_uclip(par.get("mloc", lg.get("loc", self.loc[n])), 0, self.n_loc - 1))
        self.cls[n] = int(lg.get("cls", self.cls[n]))
        self._pick_nb([n])
        keep = self.used[n] & ((self.rmask[n] & (BIT["parent"] | BIT["sibling"])) != 0)
        drop = np.nonzero(self.used[n] & ~keep)[0]
        self._drop(np.full(len(drop), n), drop, t, quiet=True)
        ps = np.nonzero(self.used[n] & ((self.rmask[n] & BIT["parent"]) != 0))[0]
        same = [p_ for p_ in ps if bool(self.fem[n, p_]) == bool(par.get("fem"))]
        if same:   # the inherited child takes the place of the drawn parent of the same sex
            p_ = same[0]
            for k_ in ("born", "fem", "nm", "line", "mcls", "faith", "party"):
                if k_ in par:
                    getattr(self, k_)[n, p_] = par[k_]
            self.pie[n, p_] = par["pie"]; self.mloc[n, p_] = self.loc[n]; self._psq[n, p_] = _csum(self.pie[n, p_] ** 2)
            self.family_mix[n] = _norm(self.pie[n, ps].mean(0)); self.pline[n] = int(par.get("line", 0))
        anc = lg.get("self", {})
        add = []
        if anc.get("alive", False) and anc.get("pie") is not None:
            add.append((dict(anc, roles=["grandparent"]), R["grandparent"], 0.35))
        for m_ in cast:
            if not m_.get("alive"):
                continue
            rl = m_.get("roles", [])
            if "partner" in rl:
                add.append((m_, R["grandparent"], 0.35))
            elif "child" in rl and m_ is not par:
                add.append((m_, R["kin"], 0.12))
            elif "grandchild" in rl:
                add.append((m_, R["kin"], 0.08))
        for m_, r_, c_ in add:
            F = self._gen(np.array([n]), np.array([int(m_["born"])]), t)
            F["pie"] = np.asarray(m_["pie"], float)[None]
            for k_ in ("fem", "nm", "line", "mcls", "faith", "party", "mloc"):
                if k_ in m_:
                    F[k_] = np.array([m_[k_]])
            self._add(F, t, r_, c0=c_, trust0=0.6, acc0=0.15, quiet=True)

    # ------------------------------------------------------------------ settings (spec 3 §1)
    def _new_setting(self, n, kind, t, ref=-1):
        """A free setting slot for life n, filled with a setting of this kind (no members yet); returns its index."""
        g = G[kind]; P = self.P; rng = self.rng
        free = np.nonzero(self.skind[n] < 0)[0]
        if not len(free):
            vol = [j_ for j_ in range(self.M) if self.skind[n, j_] in VOLUNTARY or self.skind[n, j_] == G["online"]]
            if not vol:
                return -1
            self._leave(n, min(vol, key=lambda j_: self.sts[n, j_]), t, "full")
            free = np.nonzero(self.skind[n] < 0)[0]
        j = int(free[0]); a = self._age(t)
        self.skind[n, j] = g; self.scoh[n, j] = _uclip(KTA[g, K_COH] + 0.08 * rng.standard_normal(), 0.05, 0.95)
        self.srank[n, j] = 0.5 if kind in ("household", "class") else 0.25
        self.sts[n, j] = KTA[g, K_TSY] if a < 18 else KTA[g, K_TS]
        self.ssize[n, j] = max(1, int(KTA[g, K_SIZE] * rng.lognormal(0, 0.4)))
        self.sgate[n, j] = K_GATE[g]; self.sxcost[n, j] = K_XC[g]
        self.sform[n, j] = t if kind in ("household", "class") else t - int(52 * rng.exponential(12))
        self.sjoin[n, j] = t; self.sref[n, j] = ref; self.slead[n, j] = -1; self.sncast[n, j] = 0
        self.mset[n] &= ~self._bit(j)
        if self.sph_h:
            self.shnt[n, j] = -1
        return j

    def _inst_pick(self, n, ikind, sector=-1):
        cand = np.nonzero(self.inst_kind == INST_KINDS.index(ikind))[0]
        if not len(cand):
            return -1
        here = cand[self.inst_loc[cand] == self.loc[n]]
        pool = here if len(here) else cand
        if sector >= 0 and self.inst_sector is not None:
            s_ = pool[np.asarray(self.inst_sector)[pool] == sector]
            pool = s_ if len(s_) else pool
        return int(self.rng.choice(pool))

    def join(self, n, kind, t=None, ref=-1, cause=None, quiet=False):
        """The character joins a group of this kind (life course, a moment, or a lever): members are drawn from the
        place's population (most cast members are met this way). cause: a movement's mix. Returns the setting index."""
        js = self._join_many(np.array([n]), kind, t, refs=None if ref < 0 else np.array([ref]), cause=cause, quiet=quiet)
        return int(js[0]) if len(js) else -1

    def _join_many(self, ns, kind, t=None, refs=None, cause=None, quiet=False, gate=True):
        """join() for many lives at once (vectorised members); returns their setting indices (-1: no room)."""
        t = self.t if t is None else t; rng = self.rng; W = self.W
        ns = np.asarray(ns, np.int64)
        if not len(ns):
            return np.zeros(0, np.int64)
        g = G[kind]; a = self._age(t)
        refs = np.full(len(ns), -1, np.int64) if refs is None else np.asarray(refs, np.int64).copy()
        for i_, n_ in enumerate(ns):
            if refs[i_] >= 0:
                continue
            if kind in INST_OF:
                refs[i_] = self._inst_pick(n_, "university" if (kind == "class" and a >= 17.5) else INST_OF[kind],
                                           self.psector[n_] if kind == "work" else -1)
            elif kind == "congregation":
                refs[i_] = int(self.pfaith[n_]) if self.pfaith[n_] >= 0 else self._faith_for(n_)
        gk = self._mig_gate(ns, kind, refs, t, a) if self._xsoc and gate else None
        if gk is not None and not gk.all():   # turned away this time (a migrant, at first): no setting
            out = np.full(len(ns), -1, np.int64)
            if gk.any():
                out[gk] = self._join_many(ns[gk], kind, t, refs[gk], cause, quiet, gate=False)
            return out
        js = np.array([self._new_setting(int(n_), kind, t, int(r_)) for n_, r_ in zip(ns, refs)], np.int64)
        ok = js >= 0
        ns, js, refs = ns[ok], js[ok], refs[ok]
        E = len(ns)
        if not E:
            return js
        lm = _norm(np.asarray(W.loc_mix, float)[self.loc[ns]])
        if kind in INST_OF:
            prof = _norm(np.asarray(W.inst_profile, float))
            anch = np.where((refs >= 0)[:, None], prof[np.maximum(refs, 0)], lm)
        elif kind == "congregation" and self.n_faith:
            fp = _norm(np.asarray(W.faith_profile, float))
            anch = np.where((refs >= 0)[:, None], fp[_uclip(refs, 0, len(fp) - 1)], lm)
            fp_ = getattr(self, "_force_place", None) if self.sph_h else None
            if fp_ is not None and fp_[0] in ns:   # the player's pick of a faith's place: the congregation meets there
                self.shnt[ns[ns == fp_[0]], js[ns == fp_[0]]] = fp_[1]
        elif kind == "movement" and cause is not None:
            anch = np.tile(_norm(np.asarray(cause, float)), (E, 1))
        elif self.sph_h and kind in ("club", "scene"):
            # spheres phase 2 (N1): the setting meets at a named place, one of their haunts (or the town's best fitting
            # place of such a kind, which becomes one), in place of the best of three random ways; the player's pick first
            fp_ = getattr(self, "_force_place", None)
            pl_ = np.array([fp_[1] if fp_ is not None and fp_[0] == n_ else self._haunt_for(int(n_), kind) for n_ in ns], np.int64)
            self.shnt[ns, js] = pl_
            anch = np.where((pl_ >= 0)[:, None], W.hp_s.reshape(-1, C)[np.maximum(pl_, 0)], lm)
        elif kind in ("club", "scene", "online", "gang", "movement"):
            # people choose the group that fits them (children: the parents choose): the best of three nearby ways
            base = lm if kind in ("club", "gang") else np.full((E, C), 1.0 / C)
            cands = self._dirichlet(np.repeat(base, 3, 0), 1.2).reshape(E, 3, C)
            who = self.w[ns] if a >= 10 else self.family_mix[ns]
            anch = cands[np.arange(E), np.argmax(overlap(cands, who[:, None, :]), 1)]
        elif kind == "household":
            anch = self.w[ns]
        else:
            anch = lm
        self.sanch[ns, js] = anch
        self.snorm[ns, js] = anch if kind == "household" else _norm(0.6 * anch + 0.4 * lm)
        if kind == "neighbours":
            eff = np.asarray(self._wf("nb_efficacy", np.full(max(self.n_nb, 1), 0.5)), float)[np.maximum(self.nb[ns], 0)]
            self.scoh[ns, js] = _uclip(0.2 + 0.5 * eff, 0.05, 0.95)
        cnt = np.round(KTA[g, K_NCAST] * rng.lognormal(0, 0.25, E)).astype(np.int64)
        self.sncast[ns, js] = cnt + (K_LEAD[g] is not None)
        if self._defer is not None:   # the month's joins get their members in one batch (_fill_members)
            self._defer.append((ns, js, cnt, g, quiet))
        else:
            self._fill_members([(ns, js, cnt, g, quiet)], t)
        if not quiet:
            for n_, j_, r_ in zip(ns, js, refs):
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="group_joined", group=kind, j=int(j_), ref=int(r_)))
        out = np.full(len(ok), -1, np.int64); out[ok] = js
        return out

    def _mig_gate(self, ns, kind, refs, t, a):
        """Who of lives ns gets in (spec 5 §5: gates are harder at first for a migrant): a citizen always; a migrant
        or resident with chance openness to migrants (the institution's, else the society's mean) x (g0 + (1 - g0) x
        language), easing toward 1 over the years since arrival (a resident halfway there). The home, the
        neighbours, online groups, care and a child's school are not gated. Draws only when a non-citizen asks."""
        ok = np.ones(len(ns), bool)
        if kind in ("household", "online", "neighbours", "ward") or (kind == "class" and a < 18):
            return ok
        st = self.stat[ns]; nc = st != 0
        if not nc.any():
            return ok
        om = np.atleast_1d(np.asarray(self._wf("inst_open_mig", 0.7), float))
        op = np.full(len(ns), float(om.mean()))
        if kind in INST_OF:
            hr = refs >= 0
            op[hr] = om[_uclip(refs[hr], 0, len(om) - 1)]
        g0, tau = self.P["mig_gate"]
        base = _uclip(op, 0, 1) * (g0 + (1 - g0) * self.lang[ns])
        yrs = np.maximum(t - self.arr_t[ns], 0) / 52.0
        p_ = base + (1 - base) * (1 - np.exp(-yrs / tau))
        p_ = np.where(st == STATUS.index("resident"), 0.5 + 0.5 * p_, p_)
        return ~nc | (self.rng.random(len(ns)) < p_)

    def _fill_members(self, batch, t):
        """Members and leaders for new settings [(lives, setting indices, member counts, kind, quiet)], in one go."""
        batch = [(ns[ok], js[ok], cnt[ok], g, q) for ns, js, cnt, g, q in batch
                 for ok in [(self.skind[ns, js] == g) & (self.sjoin[ns, js] == t)] if ok.any()]
        if not batch:
            return
        parts = []   # (lives, settings, leader?, quiet?): the members, then a leader where the kind has one
        for ns, js, cnt, g, q in batch:
            parts.append((np.repeat(ns, _ix(cnt)), np.repeat(js, _ix(cnt)), False, bool(q)))
            if K_LEAD[g] is not None:
                parts.append((ns, js, True, True))
        nn = np.concatenate([x_[0] for x_ in parts]); jj = np.concatenate([x_[1] for x_ in parts])
        ld = np.concatenate([np.full(len(x_[0]), x_[2]) for x_ in parts])
        qu = np.concatenate([np.full(len(x_[0]), x_[3]) for x_ in parts])
        sl_ = self._members(nn, jj, t, leader=ld, quiet=qu)
        ok = ld & (sl_ >= 0)
        if ok.any():
            ln, lj, sl_ = nn[ok], jj[ok], sl_[ok]
            gk = self.skind[ln, lj].astype(np.int64)
            self.slead[ln, lj] = sl_
            nc = gk != G["club"]
            self.stand[ln[nc], sl_[nc]] = np.maximum(1, self.stand[ln[nc], sl_[nc]])
            self.rmask[ln, sl_] |= LEAD_BIT[gk]; self.role[ln, sl_] = LEAD_ROLE[gk]

    def _faith_for(self, n):
        if not self.n_faith:
            return -1
        fp = _norm(np.asarray(self.W.faith_profile, float))
        sc = fp @ self.w[n]
        if len(sc) > 3 and hasattr(self.W, "faith_open"):   # C5: a movement slot only while it lives and holds join_share
            sc = np.where(self.W.faith_open(), sc, -np.inf)
        return int(np.argmax(sc))

    def _members(self, n, j, t, leader=False, quiet=False):
        """New cast members for settings (n, j), vectorised: ages, pies near the setting's norms, roles by kind.
        leader, quiet: one flag for all, or one per row (a leader is drawn older and takes the kind's leader role)."""
        n = np.asarray(n, np.int64); j = np.asarray(j, np.int64); E = len(n)
        if not E:
            return np.zeros(0, np.int64)
        rng = self.rng; a = self._age(t); g = self.skind[n, j].astype(np.int64)
        ld = np.broadcast_to(np.asarray(leader, bool), (E,))
        kinds = np.array(GROUP_KINDS)[g]
        ages = np.empty(E)
        for kd in np.unique(kinds):
            h = kinds == kd; m_ = h.sum(); lh = ld[h]
            if kd == "class":
                ag = (a + rng.normal(0, 0.35, m_)) if a < 17.5 else a + np.abs(rng.normal(0, 2.0, m_))
                ag = np.where(lh, rng.uniform(26, 62, m_), ag) if lh.any() else ag
            elif kd in ("work", "unit"):
                ag = np.where(lh, rng.uniform(35, 62, m_), rng.uniform(19, 64, m_)) if lh.any() else rng.uniform(19, 64, m_)
            elif kd == "congregation":
                ag = np.where(lh, rng.uniform(45, 75, m_), rng.uniform(5, 88, m_)) if lh.any() else rng.uniform(5, 88, m_)
            elif kd in ("scene", "gang"):
                ag = np.maximum(12, a + rng.normal(0, 4, m_))
            elif kd == "ward":
                ag = np.maximum(a, 60) + rng.normal(0, 8, m_)
            elif kd == "neighbours":
                ag = rng.uniform(1, 88, m_)
            else:
                ag = np.maximum(5, a + rng.normal(0, 10 if a >= 18 else 3, m_))
            ages[h] = _uclip(ag, 0, 99)
        born = t - (ages * 52).astype(np.int64)
        sel = np.where(np.isin(g, VOLUNTARY) | np.isin(g, [G["online"], G["gang"]]), 0.5, 0.25)[:, None]
        F = self._gen(n, born, t, ctx=self.snorm[n, j], sel=1.0, mcls=self.cls[n], p_same_cls=0.4)
        F["pie"] = _norm((1 - sel) * self._dirichlet(self._popmean(self.loc[n], born)) + sel * F["pie"])
        cong = g == G["congregation"]
        F["faith"] = np.where(cong, self.sref[n, j], F["faith"])
        wk = g == G["work"]
        F["emp"] = np.where(wk, True, F["emp"]); F["sector"] = np.where(wk & (self.psector[n] >= 0), self.psector[n], F["sector"])
        F["inst"] = np.where(wk | (g == G["class"]) | (g == G["unit"]), self.sref[n, j], -1)
        rn = np.where(ld, LEAD_ROLE[g], MEMBER_ROLE_OF[g]).astype(np.int64)
        c0 = _uclip(0.04 + 0.08 * rng.random(E), 0.03, 0.2)
        sl = self._add(F, t, rn, c0=c0, trust0=0.5, setbit=j, ctx_read=self.snorm[n, j], acc0=0.05,
                       quiet=np.broadcast_to(np.asarray(quiet, bool), (E,)) | ld, via="group")
        return sl

    def _leave(self, n, j, t, why="left"):
        if j < 0 or self.skind[n, j] < 0:
            return
        kind = GROUP_KINDS[int(self.skind[n, j])]
        bit = self._bit(j)
        self.mset[n] &= ~bit
        self.skind[n, j] = -1; self.sts[n, j] = 0; self.slead[n, j] = -1; self.sncast[n, j] = 0
        if self.sph_h:
            self.shnt[n, j] = -1
        if self.hhj[n] == j:
            self.hhj[n] = -1
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="group_left", group=kind, j=int(j), why=why))

    def leave(self, n, kind, t=None, why="left"):
        """The character leaves their group of this kind (the newest one), paying its exit cost in belonging."""
        js = np.nonzero(self.skind[n] == G[kind])[0]
        if len(js):
            self._leave(n, int(js[np.argmax(self.sjoin[n, js])]), self.t if t is None else t, why)

    def _bit(self, j):
        return (np.ones(1, self.mset.dtype) << np.asarray(j, self.mset.dtype))[0] if np.ndim(j) == 0 else \
            (np.ones(1, self.mset.dtype) << np.asarray(j).astype(self.mset.dtype))

    def _bits(self):
        """(N, K, M) membership of the living in each setting (float32)."""
        return np.take(_LUT[:, :self.M], np.where(self.lv, self.mset, 0).astype(np.uint8), axis=0)

    def _count(self, B):
        """(N, M) living members of each setting."""
        return np.matmul(np.ones((self.N, 1, self.K), np.float32), B)[:, 0, :]

    def _fsh(self, B=None):
        """Contact a year with each cast member through shared settings: the setting's contact x depth, shared out by
        attention (the alike and the already close get more; the members' mean keeps the setting's contact)."""
        B = self._bits() if B is None else B; P = self.P; f32 = np.float32
        g = np.maximum(self.skind, 0)
        fd = np.where(self.skind >= 0, KTA[g, K_F] * KTA[g, K_DEPTH], 0).astype(f32)
        if self._xsoc and (self.lang < 1).any():   # a language still being learned thins contact outside the home
            fd = np.where(g == G["household"], fd, fd * (0.4 + 0.6 * self.lang).astype(f32)[:, None])
        lk = self._lkm = likeness(self.pie, self.w32[:, None, :]).astype(f32)
        att = (f32(P["mingle"][0]) + f32(P["mingle"][1]) * lk * lk) * (self.c + f32(P["att_c0"])) ** f32(P["att_pow"])
        ma_ = P["mingle_age"]
        if ma_ is not None and ma_[0] > 0:   # near in age (every character of the run has the same age)
            f0 = ma_[2] if len(ma_) > 2 else 0.0
            dg = (self.born - self.t0).astype(f32); dg *= f32(1 / (52.0 * (ma_[0] + ma_[1] * self._age())))
            dg *= dg; dg += f32(1); np.reciprocal(dg, out=dg); dg *= f32(1 - f0); dg += f32(f0)
            dg[(self.rmask & KINMASK) != 0] = 1
            att *= dg
        A2 = np.empty((self.N, 2, self.K), f32); A2[:, 0] = att; A2[:, 1] = 1.0
        dc = np.matmul(A2, B)                                    # (N, 2, M): attention summed, members counted
        den = dc[:, 0] / np.maximum(dc[:, 1], 1.0)
        sw = ((self.sociab / np.sqrt(np.prod(P["soc_spread"]))) ** P["soc_set"]).astype(f32)[:, None]
        self.fsh = np.matmul(B, (fd / np.maximum(den, 1e-6))[..., None])[..., 0] * att * sw

    def _settings_month(self, t, S, B, dm=1.0):
        """Norms drift toward members (by standing), the character (by rank), the leader, the anchor (institution,
        faith, founding ways) and the culture (faster for the young); cohesion follows the members' spread; splits.
        dm: months since the last step (the monthly rates are scaled to it)."""
        N, M = self.N, self.M; P = self.P; W = self.W; a = self._age(t); f32 = np.float32
        act = self.skind >= 0
        if not act.any():
            return
        g = np.maximum(self.skind, 0)
        # sums over members, weighted by standing: their pies; their spread (sum of squares), strictness and weight
        wt = (1.0 + self.stand).astype(f32)
        msum = np.matmul(B.transpose(0, 2, 1), self.pie * wt[..., None])   # (N, M, C)
        Xs = np.empty((N, 4, self.K), f32)
        np.multiply(self._psq, wt, out=Xs[:, 0]); np.multiply(self.strict, wt, out=Xs[:, 1]); Xs[:, 2] = wt; Xs[:, 3] = 1.0
        Rw = np.matmul(Xs, B)                                    # (N, 4, M)
        mw = Rw[:, 2]; cnt = Rw[:, 3]
        memmix = np.where(mw[..., None] > 0, msum / np.maximum(mw[..., None], 1e-9), self.snorm)
        self._fitm = (C * _csum(memmix * self.snorm) - 1).astype(f32)   # how well members fit the ways
        self.srank += (act * (1 - (1 - P["rank_rev"]) ** dm) * (P["rank_base"] - self.srank)).astype(f32)
        ls = np.clip(self.slead, 0, None)
        lp = self.pie[np.arange(N)[:, None], ls]
        haslead = (self.slead >= 0) & self.lv[np.arange(N)[:, None], ls]
        lp = np.where((self.slead == -2)[..., None], self.w[:, None, :], lp)
        haslead = haslead | (self.slead == -2)
        inst_k = act & np.isin(g, [G["class"], G["work"], G["unit"], G["ward"]]) & (self.sref >= 0)
        if inst_k.any():
            prof = _norm(np.asarray(W.inst_profile, float))
            self.sanch[inst_k] = prof[_uclip(self.sref[inst_k], 0, len(prof) - 1)]
        V = _norm(np.asarray(W.V, float))
        young = 1.5 if a < 25 else 1.0
        tgt = (KTA[g, K_WM][..., None] * memmix + 0.15 * self.srank[..., None] * self.w[:, None, :]
               + 0.2 * haslead[..., None] * lp + KTA[g, K_WA][..., None] * self.sanch
               + young * KTA[g, K_WV][..., None] * V)
        hh = (g == G["household"]) & act
        if hh.any():   # a household's ways are its adults' ways
            hn, hj = np.nonzero(hh)
            al = (self.born <= t - 18 * 52) & self.lv          # the adults living in it (one household per life at most)
            if len(hn) == N:
                ba = (((self.mset >> hj[:, None].astype(self.mset.dtype)) & 1) * al).astype(f32); hp_ = self.pie
            else:
                ba = (((self.mset[hn] >> hj[:, None].astype(self.mset.dtype)) & 1) * al[hn]).astype(f32); hp_ = self.pie[hn]
            hsum = np.matmul(ba[:, None, :], hp_)[:, 0] + (a >= 18) * self.w[hn]
            hcnt = ba.sum(1) + (a >= 18)
            hmix = np.where(hcnt[:, None] > 0, hsum / np.maximum(hcnt[:, None], 1e-9), self.snorm[hn, hj])
            tgt[hn, hj] = hmix + 0.02 * V
        tgt = _norm(tgt)
        age_y = (t - self.sform) / 52.0
        rate = np.minimum(dm * KTA[g, K_DRIFT] * (1 - 0.5 * self.scoh) / (1 + np.maximum(age_y, 0) / 20), 1) * act
        self.snorm += (rate[..., None] * (tgt - self.snorm)).astype(f32)
        # cohesion: members pulling apart lower it; old ritual groups and outside threat keep it
        disp = np.sqrt(np.maximum(Rw[:, 0] / np.maximum(mw, 1e-9) - _csum(memmix * memmix), 0)) * (mw > 0)
        thr = 0.1 * ((g == G["unit"]) & (int(self._wf("war", 0)) > 0))
        tc = KTA[g, K_COH] - 0.8 * (disp - 0.35) + thr
        self.scoh += (act * ((1 - 0.96 ** dm) * (tc - self.scoh) + 0.015 * np.sqrt(dm) * self.rng.standard_normal((N, M)))).astype(f32)
        self.scoh = _uclip(self.scoh, 0.02, 0.98).astype(f32)
        # members' strictness on norm keys (for the local norms)
        self.sstrict = np.where(mw > 0, Rw[:, 1] / np.maximum(mw, 1e-9), 0).astype(f32)
        # splits: low cohesion and members pulling apart; the character goes with the side that fits them
        sp = act & ~hh & (self.scoh < 0.18) & (cnt >= 4) & (self.rng.random((N, M)) < 1 - 0.97 ** dm)
        for n_, j_ in zip(*np.nonzero(sp)):
            mem = np.nonzero(B[n_, :, j_] > 0)[0]
            lk = likeness(self.pie[n_, mem], self.w[n_])
            go = mem[lk < np.median(lk)]
            self.mset[n_, go] &= ~self._bit(j_)
            stay = mem[lk >= np.median(lk)]
            self.snorm[n_, j_] = _norm(0.5 * self.snorm[n_, j_] + 0.5 * self.pie[n_, stay].mean(0))
            self.scoh[n_, j_] = 0.55; self.sncast[n_, j_] = len(stay)
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="split", group=GROUP_KINDS[int(self.skind[n_, j_])],
                                        j=int(j_), left=[int(x_) for x_ in self.uid[n_, go]]))

    @property
    def set_sphere(self):
        """Each setting's sphere (N x M, index into SPHERES; -1 an empty slot): a work setting by its employer's
        sector (none known: commerce). Read only (item 15, Replace)."""
        g = self.skind.astype(np.int64); sph = GROUP_SPH[np.maximum(g, 0)]
        serv = SECTORS.index("services"); isec = self.inst_sector
        if isec is not None and len(isec):
            isec = np.asarray(isec, np.int64); sec = isec[np.clip(self.sref, 0, len(isec) - 1)]
            wsec = np.where((self.sref >= 0) & (sec >= 0), sec, serv)
        else:
            wsec = np.full(g.shape, serv)
        out = np.where(g < 0, -1, np.where(sph >= 0, sph, SECTOR_SPH[wsec]))
        if self.sph_h and getattr(self.W, "hp_s", None) is not None:   # phase 2: a setting at a place is in that place's sphere
            P_ = self.W.hp_s.shape[2]
            out = np.where(self.shnt >= 0, HAUNT_SPH[(np.maximum(self.shnt, 0) // P_) % len(HAUNT_KINDS)], out)
        return out

    def setting_places(self, n):
        """Life n's settings as places (item 15, phase 1d; read only, no dice): slot, kind, sphere, subsector, the
        place's name in the world's epoch, and the nearest face (the colour the setting's ways lean to most, with its
        name). A class at a university is learn.higher."""
        import sphere_data as SD
        ep = getattr(self.W, "sph_epoch", "modern"); ss = self.set_sphere[n]; out = []
        isec = self.inst_sector; ikind = self.inst_kind
        for j in np.nonzero(self.skind[n] >= 0)[0]:
            kind = GROUP_KINDS[int(self.skind[n, j])]; ref = int(self.sref[n, j])
            if kind == "work":
                sec = int(isec[ref]) if isec is not None and 0 <= ref < len(isec) and isec[ref] >= 0 else SECTORS.index("services")
                sub = WORK_SUB[SECTORS[sec]]
            elif kind == "class" and 0 <= ref < len(ikind) and ikind[ref] == INST_KINDS.index("university"):
                sub = "learn.higher"
            else:
                sub = SET_SUB[kind]
            sph = SPHERES[int(ss[j])]
            if not sub.startswith(sph + "."):        # the subsector follows the sphere the layer reads
                sub = sph + "." + SD.SUBSECTORS[sph][0]
            c = int(np.argmax(self.snorm[n, j])); fk = f"{sph}.{COLORS[c]}"
            out.append(dict(slot=int(j), kind=kind, sphere=sph, subsector=sub,
                            place=SD.PLACE_BY_EPOCH.get(sub, {}).get(ep), face=fk, face_name=SD.FACE_NAMES[fk]))
        return out

    # ------------------------------------------------------------------ the spheres of society (item 15): phase 2
    def _sph_init(self):
        import sphere_data as SD
        N, M = self.N, self.M; pm = self.perm
        self.hnt = np.full((N, 3), -1, np.int64)     # N1: each life's haunts, flat place ids (World.place_info), best first
        self.shnt = np.full((N, M), -1, np.int64)    # the place a club, scene or congregation setting is held at
        self.rung = np.zeros((N, 9))                 # N2: standing in each sphere, 0 newcomer .. 4 leader (LADDER)
        self.ryrs = np.zeros((N, 9))                 # years present in each sphere's places
        self.hrs = np.zeros((N, len(TIME_ROWS)))     # hours a week by row (TIME_ROWS), this month
        self.hpick = -1                              # the year of age of the last yearly pick
        self.places_mix = None                       # the places part of item 12's current (sph_hours)
        self._hrng = np.random.default_rng([self.seed, 47, self.run_seed])   # haunt picks draw only here
        T = np.asarray(SD.TEACH, float)              # sphere x face x colour (W U B R G), into this world's frame
        self._teach = T[:, pm][:, :, pm]
        ep = getattr(self.W, "sph_epoch", "modern")
        self._tgrp = SD.TIME_GROUPS.index({"bands": "early", "villages": "early", "machine": "machine", "modern": "modern"}.get(ep, "middle"))
        self._time = SD.TIME; self._tages = SD.TIME_AGES; self._depth = np.array([SD.DEPTH[r_] for r_ in TIME_ROWS])
        self.mark = np.zeros((N, C))                 # the mark of the work drawn in so far (pie units, this world's frame)
        self.mark_dw = np.zeros((N, C))              # this year's step of it, for the engine to apply (then cleared)
        self._mark_yr = -1
        self._mark_tau = float(SD.MARK_TAU)
        hs_ = np.array([SD.HAUNT_SHARES[k_] for k_ in HAUNT_KINDS])   # how common each haunt kind is (modern shares)
        self._hprior = np.log(hs_ / hs_.mean())
        self._mark_pull = {k_: np.asarray(v_["pull"], float)[pm] for k_, v_ in SD.MARKS.items()}
        mz_ = {d_: (np.mean([v_[d_] for v_ in SD.MARKS.values()]), np.std([v_[d_] for v_ in SD.MARKS.values()]))
               for d_ in ("say", "skill")}
        self._mark_dim = {k_: (v_["danger"], v_["wear"], (v_["say"] - mz_["say"][0]) / mz_["say"][1],
                               (v_["skill"] - mz_["skill"][0]) / mz_["skill"][1]) for k_, v_ in SD.MARKS.items()}
        self.mark_wear = np.zeros(N)                 # years the body has aged beyond its own in hard work (.15 x wear a year)
        self.mark_hurt = np.zeros(N, bool)           # a serious injury at work this year, for the engine (then cleared)
        self.mark_die = np.zeros(N, bool)            # a death at work this year, for the engine (then cleared)
        self.mark_z = np.zeros((N, 2))               # the trade's say and skill (centred over the 60), while in it

    def _marks_year(self, t):
        """sph_marks, once a year: a worker's colours are drawn toward their trade's mark (marks.json, at its colour
        reading) with a drawing-in time of MARK_TAU years; the trade is the work setting's subsector (the employer's
        sector, as setting_places reads it). The step goes to the engine as mark_dw (pie units)."""
        a = self._age(t); yr = int(a)
        if yr == self._mark_yr:
            return
        self._mark_yr = yr
        wk = (self.skind == G["work"]); has = wk.any(1) & ~self.dead
        isec = self.inst_sector; serv = SECTORS.index("services")
        tgt = np.zeros((self.N, C)); dw_ = np.zeros((self.N, 2)); self.mark_z = np.zeros((self.N, 2))
        for n_ in np.nonzero(has)[0]:
            ref = int(self.sref[n_, int(np.argmax(wk[n_]))])
            sec = int(isec[ref]) if isec is not None and 0 <= ref < len(isec) and isec[ref] >= 0 else serv
            sub_ = WORK_SUB[SECTORS[sec]]
            tgt[n_] = self._mark_pull[sub_]
            dg_, wr_, sz_, kz_ = self._mark_dim[sub_]
            dw_[n_] = dg_, wr_; self.mark_z[n_] = sz_, kz_
        step = np.where(has[:, None], (tgt - self.mark) / self._mark_tau, 0.0)
        self.mark += step; self.mark_dw = self.mark_dw + step
        # the body (marks.json size.body): a serious injury at .03 x danger a work-year, a death at .0005 x danger; the
        # body ages .15 x wear years a year worked (the haunt stream draws, so every other stream draws as before)
        u_ = self._hrng.random((self.N, 2))
        self.mark_hurt |= has & (u_[:, 0] < 0.03 * dw_[:, 0])
        self.mark_die |= has & (u_[:, 1] < 0.0005 * dw_[:, 0])
        self.mark_wear += 0.15 * dw_[:, 1] * has

    def _tstage(self, a):
        for st_, (lo_, hi_) in self._tages.items():
            if lo_ <= a < hi_ + 1:
                return st_
        return "old"

    def _haunt_hours(self, a):
        """Each life's free hours a week for haunts (the stage's mean, by sociability) and how many haunts that holds."""
        h = self._time[self._tstage(a)]["haunts"][self._tgrp] * np.sqrt(np.maximum(self.sociab, 0.05))
        n = np.where(h < 4, 1, np.where(h <= 10, 2, 3)) * (a >= 4)
        return h, n

    def _haunt_util(self, ns, a, kinds=None):
        """Utility of each place in each life's town (len(ns) x 31 kinds x N_PLACES): how common the kind is (the log of
        its share, HAUNT_SHARES), fit of the place's ways with the
        life's (a child's: the family's), money against what the kind costs, the age a kind asks, and a faith's places
        for those who keep one; plus a Gumbel draw from the haunt stream (who goes where is partly chance)."""
        W = self.W; hp = W.hp_s[self.loc[ns]]                                     # n x 31 x P x 5
        who = self.w[ns] if a >= 10 else self.family_mix[ns]
        fit_ = likeness(hp, who[:, None, None, :])
        mon = self.res[ns, MON] if self.res.shape[1] > MON else np.full(len(ns), 0.5)
        u = 12.0 * fit_ - 1.5 * HAUNT_COST[None, :, None] * (1 - mon)[:, None, None] + self._hprior[None, :, None]
        ok = (HAUNT_AGE <= a)[None, :]
        fk = np.array([k_.startswith("faith.") and k_ != "faith.seeking" for k_ in HAUNT_KINDS])
        ok = ok & ~(fk[None, :] & (self.pfaith[ns] < 0)[:, None])
        if kinds is not None:
            ok = ok & np.isin(np.arange(len(HAUNT_KINDS)), kinds)[None, :]
        u = u + self._hrng.gumbel(0, 1, u.shape)
        return np.where(ok[:, :, None], u, -np.inf)

    def _haunts_year(self, t, ns=None):
        """N1: once a year (and on a move) each life picks its haunts by fit: one under 4 haunt hours a week, two at 4
        to 10, three above; a place they already go to, and one a setting of theirs meets at, is kept more often.
        A setting whose place is no longer theirs is left ("stopped going")."""
        a = self._age(t); live = ~self.dead
        ns = np.nonzero(live)[0] if ns is None else np.asarray(ns, np.int64)
        if not len(ns):
            return
        _, nh = self._haunt_hours(a); nh = nh[ns]
        u = self._haunt_util(ns, a)                                              # n x 31 x P
        H, P_ = u.shape[1], u.shape[2]
        base = self.loc[ns][:, None] * (H * P_)
        flat = u.reshape(len(ns), -1)
        held = self.hnt[ns]; linked = self.shnt[ns]
        for q_ in range(3):   # a haunt kept is easier to keep; one a setting meets at, easier still
            ok_ = (held[:, q_] >= 0) & (held[:, q_] // (H * P_) == self.loc[ns])
            ii_ = np.nonzero(ok_)[0]
            flat[ii_, held[ii_, q_] - base[ii_, 0]] += 1.0
        for j_ in range(self.M):
            ok_ = (linked[:, j_] >= 0) & (linked[:, j_] // (H * P_) == self.loc[ns])
            ii_ = np.nonzero(ok_)[0]
            flat[ii_, linked[ii_, j_] - base[ii_, 0]] += 2.0
        u = flat.reshape(u.shape)
        bp = u.argmax(2); bu = np.take_along_axis(u, bp[..., None], 2)[..., 0]  # each kind's best place
        order = np.argsort(-bu, 1, kind="stable")[:, :3]
        new = np.full((len(ns), 3), -1, np.int64)
        for q_ in range(3):
            k_ = order[:, q_]; ok_ = (q_ < nh) & np.isfinite(bu[np.arange(len(ns)), k_])
            new[ok_, q_] = base[ok_, 0] + k_[ok_] * P_ + bp[np.arange(len(ns)), k_][ok_]
        self.hnt[ns] = new
        for i_, n_ in enumerate(ns):   # settings held at a place that is no longer theirs
            for j_ in np.nonzero(self.shnt[n_] >= 0)[0]:
                if self.shnt[n_, j_] not in new[i_]:
                    self._leave(int(n_), int(j_), t, "stopped going")

    def _haunt_for(self, n, kind):
        """The place a new setting of this kind is held at: the life's best haunt of a fitting kind that no setting of
        theirs meets at yet, else the town's best fitting place of such a kind, which becomes a haunt. -1: none."""
        H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]; a = self._age()
        ks = SET_HAUNTS.get(kind)
        if not ks:
            return -1
        for p_ in self.hnt[n]:
            if p_ >= 0 and (p_ // P_) % H in ks and p_ not in self.shnt[n] and p_ // (H * P_) == self.loc[n]:
                return int(p_)
        u = self._haunt_util(np.array([n]), a, kinds=ks)[0]
        if not np.isfinite(u).any():
            return -1
        k_, i_ = np.unravel_index(int(np.argmax(u)), u.shape)
        p_ = int(self.loc[n] * H * P_ + k_ * P_ + i_)
        self._haunt_add(n, p_)
        return p_

    def _haunt_add(self, n, p_, first=False):
        """Place p_ becomes one of life n's haunts: first (the player's pick) or in a free slot, else in the last one."""
        h_ = [x_ for x_ in self.hnt[n] if x_ >= 0 and x_ != p_]
        h_ = [p_] + h_ if first else h_ + [p_]
        if len(h_) > 3:
            h_ = h_[:2] + [p_] if not first else h_[:3]
        self.hnt[n] = (h_ + [-1, -1, -1])[:3]

    def pick_haunt(self, n, sphere, colour, t=None):
        """The player's (or the life's own) haunt choice (N1; the haunt choice moments): the town's place in that sphere
        whose ways lean most to that face becomes their first haunt, and they go: a setting meets there (a congregation
        for a faith's place, a scene or a club for the rest). colour: W U B R G (the face's letter); returns the place."""
        t = self.t if t is None else t; n = int(n)
        if not self.sph_h:
            return -1
        H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]; a = self._age(t)
        j = SPHERES.index(sphere) if isinstance(sphere, str) else int(sphere)
        c = int(self.iperm[COLORS.index(colour) if isinstance(colour, str) else int(colour)])
        ks = [k_ for k_ in range(H) if HAUNT_SPH[k_] == j and HAUNT_AGE[k_] <= a]
        if not ks:
            return -1
        hp = self.W.hp_s[self.loc[n]][ks]                                         # kinds x P x 5
        k_, i_ = np.unravel_index(int(np.argmax(hp[..., c])), hp.shape[:2])
        p_ = int(self.loc[n] * H * P_ + ks[k_] * P_ + i_)
        self._haunt_add(n, p_, first=True)
        if p_ not in self.shnt[n]:
            kn_ = HAUNT_KINDS[ks[k_]]
            kind = "congregation" if kn_.startswith("faith.") else "scene" if kn_ in SCENE_HAUNTS else "club"
            if kind == "congregation" and self.pfaith[n] < 0:
                self.pfaith[n] = self._faith_for(n)
            self._force_place = (n, p_)
            try:
                self.join(n, kind, t)
            finally:
                self._force_place = None
        return p_

    def _haunts_month(self, t):
        """Monthly: a setting held at a place takes the place's ways as its anchor (the town's spheres reach the life
        through its haunts); the setting's leader is the keeper, its members regulars, and keepers and leaders of any
        setting can be go-betweens (N4)."""
        on = self.shnt >= 0
        if on.any():
            n_, j_ = np.nonzero(on)
            H = len(HAUNT_KINDS); P_ = self.W.hp_s.shape[2]
            p_ = self.shnt[n_, j_]
            self.sanch[n_, j_] = self.W.hp_s.reshape(-1, C)[p_]
            ld_ = self.slead[n_, j_]; ok_ = ld_ >= 0
            self.rmask[n_[ok_], ld_[ok_]] |= BIT["keeper"] | BIT["go-between"]
            B = self._bits()
            mem = (B[n_, :, j_] > 0)                                              # rows x K
            rr, kk = np.nonzero(mem)
            self.rmask[n_[rr], kk] |= BIT["regular"]
        ld = self.slead >= 0
        if ld.any():
            n_, j_ = np.nonzero(ld)
            self.rmask[n_, self.slead[n_, j_]] |= BIT["go-between"]

    def _sph_hours(self, t):
        """Monthly (sph_hours): hours a week in each of the eight rows (dynamics.json exposure, this epoch's column, by
        the life's settings), the places part of item 12's current (each row's mix x hours x depth x (1 + .25 x rung))
        and, yearly, the rungs (N2): years present in a sphere's places make a regular (1) and a known face (5); rank .85
        or more in a setting there makes a pillar, leading one a leader; absence fades a rung a step a year."""
        W = self.W; N = self.N; a = self._age(t); T = self._time[self._tstage(a)]; g = self._tgrp
        sph = getattr(W, "sph_s", None)
        if sph is None:
            return
        town = sph[self.loc]                                                      # N x 9 x 5
        ph_ = getattr(W, "sph_ph", None) if W.p.get("sph_pairs", False) else None
        tm = W.sph_teach_mix((town, None if ph_ is None else ph_[self.loc]), self._teach)   # each town sphere's teaching mix
        has = lambda k_: (self.skind == G[k_])
        def set_mix(k_):
            h_ = has(k_); any_ = h_.any(1); j_ = h_.argmax(1)
            return any_, self.snorm[np.arange(N), j_].astype(float)
        S_ = SPHERES.index
        hrs = np.zeros((N, 8)); mix = np.zeros((N, 8, C)); rs = np.zeros((N, 8), np.int64)
        wk_, wm_ = set_mix("work"); ws_ = self.set_sphere[np.arange(N), has("work").argmax(1)]
        hrs[:, 0] = T["work"][g] * wk_; mix[:, 0] = np.where(wk_[:, None], wm_, tm[:, S_("comm")]); rs[:, 0] = np.where(wk_, ws_, S_("comm"))
        cl_, cm_ = set_mix("class")
        hrs[:, 1] = np.where(cl_, max(T["learn"][g], 12.0 if a >= 5 else 0.0), T["learn"][g] * (a >= 18))
        mix[:, 1] = np.where(cl_[:, None], cm_, tm[:, S_("learn")]); rs[:, 1] = S_("learn")
        hh, _ = self._haunt_hours(a)
        if self.sph_h:
            ok_ = self.hnt >= 0; nk_ = ok_.sum(1)
            hs_ = HAUNT_SPH[(np.maximum(self.hnt, 0) // W.hp_s.shape[2]) % len(HAUNT_KINDS)]   # N x 3
            hm_ = np.einsum("nqf,nqfc->nqc", W.hp_s.reshape(-1, C)[np.maximum(self.hnt, 0)], self._teach[hs_])
            hm_ = (hm_ * ok_[..., None]).sum(1) / np.maximum(nk_, 1)[:, None]
            hsph = hs_[:, 0]
            hrs[:, 2] = hh * (nk_ > 0); mix[:, 2] = np.where((nk_ > 0)[:, None], hm_, tm[:, S_("gather")]); rs[:, 2] = hsph
        else:
            hrs[:, 2] = hh * (a >= 4); mix[:, 2] = tm[:, S_("gather")]; rs[:, 2] = S_("gather")
        fa_, fm_ = set_mix("congregation")
        hrs[:, 3] = T["faith"][g] * np.where(fa_, 1.6, 0.25)   # the row is the mean: members about 1.6 times it (most belong); mix[:, 3] = np.where(fa_[:, None], fm_, tm[:, S_("faith")]); rs[:, 3] = S_("faith")
        isch = (self.rmask & BIT["child"]) != 0
        small = (isch & self.used & self.lv & ((t - self.born) < 6 * 52)).any(1)
        hrs[:, 4] = T["care_given"][g] * np.where(small, 2.5, 1.0); mix[:, 4] = tm[:, S_("care")]; rs[:, 4] = S_("care")
        un_, um_ = set_mix("unit")
        hrs[:, 5] = np.where(un_, 40.0, T["service"][g]); mix[:, 5] = np.where(un_[:, None], um_, tm[:, S_("prot")]); rs[:, 5] = S_("prot")
        rr_ = np.floor(self.rung[:, S_("rule")])
        hrs[:, 6] = T["civic"][g] * np.where(rr_ >= 4, 6.0, np.where(rr_ >= 3, 3.0, 1.0)); mix[:, 6] = tm[:, S_("rule")]; rs[:, 6] = S_("rule")
        hrs[:, 7] = T["market"][g]; mix[:, 7] = tm[:, S_("comm")]; rs[:, 7] = S_("comm")
        if W.p.get("sph_deep", False):   # phase 5: the care load (who carries whom) adds care hours and costs work hours
            self.care_load = self._care_load(t)
            if getattr(self, "care_buy", None) is not None:   # bought help: care hours x .7 (phase5c-answers.md)
                self.care_load = self.care_load * np.where(self.care_buy, getattr(self, "care_buy_x", 0.7), 1.0)
            hrs[:, 4] += self.care_load; hrs[:, 0] = np.maximum(0.0, hrs[:, 0] - 0.1 * self.care_load)   # 1 work hour per 10
        if W.p.get("sph_seasons", False):                                         # N7: the year's rhythm in each row's sphere
            hrs = hrs * W._sph_tables()["seas_h"][rs, W.season]
        self.hrs = hrs
        if W.p.get("sph_shadow", False):   # N5: the shadow around them, the hours-weighted shadow share of their rows' spheres
            rsh = np.take_along_axis(W._sph_sh()[self.loc], rs[:, :, None], 1)  # N x 8 x 5
            self.sh_around = (hrs[..., None] * rsh).sum(1) / np.maximum(hrs.sum(1), 1e-9)[:, None]
        wt = hrs * self._depth[None] * (1 + 0.25 * np.floor(np.take_along_axis(self.rung, rs, 1)))
        tot = wt.sum(1)
        self.places_mix = np.where(tot[:, None] > 1e-9, (wt[..., None] * mix).sum(1) / np.maximum(tot, 1e-9)[:, None], self.w)
        yr = int(a)
        if yr != getattr(self, "_rung_yr", -1):   # the rungs, once a year
            self._rung_yr = yr
            # present where a community meets them: the work, the class, each haunt, the congregation, the unit (not the
            # shops, the town's council or the care given at home, which make no one known)
            pres = np.zeros((N, 9)); ar_ = np.arange(N)
            np.add.at(pres, (ar_, rs[:, 0]), hrs[:, 0]); np.add.at(pres, (ar_, rs[:, 1]), hrs[:, 1] * cl_)
            np.add.at(pres, (ar_, rs[:, 3]), hrs[:, 3] * fa_); np.add.at(pres, (ar_, rs[:, 5]), hrs[:, 5] * un_)
            if self.sph_h:
                for q_ in range(3):
                    ok_ = self.hnt[:, q_] >= 0
                    np.add.at(pres, (ar_[ok_], hs_[ok_, q_]), (hrs[:, 2] / np.maximum(nk_, 1))[ok_])
            here = pres >= 2.0
            self.ryrs = np.where(here, self.ryrs + 1, self.ryrs * 0.8)
            tg = np.where(self.ryrs >= 5, 2, np.where(self.ryrs >= 1, 1, 0)).astype(float)   # years make a regular, then a known face
            ss = self.set_sphere; act = self.skind >= 0
            for j_ in range(self.M):   # standing earned in a setting: a pillar there (rank .85 or more), its leader a leader
                sj = ss[:, j_]; ok_ = act[:, j_] & (sj >= 0)
                ii_ = np.nonzero(ok_)[0]
                tg[ii_, sj[ii_]] = np.maximum(tg[ii_, sj[ii_]], np.where(self.slead[ii_, j_] == -2, 4, np.where(self.srank[ii_, j_] >= 0.85, 3, 0)))
            self.rung = np.where(tg >= self.rung, np.minimum(tg, self.rung + 1), np.maximum(tg, self.rung - 1))

    def _care_load(self, t):
        """Phase 5 (sph_deep), "who carries whom": hours a week of care each life gives (N; deep_state.care_load). A close
        partner, parent, parent-in-law or grandparent (closeness layer 2 or nearer) in poor health (under .35) or 82 or
        older needs care: partner 20, parent 12, parent-in-law 8, grandparent 4 hours, x 1.5 under health .2. A partner's
        lands on the life; a parent's or grandparent's is shared with the close siblings still living, and a
        parent-in-law's with the partner, each weighted 1 + .5 x the world's role strictness (1 - acceptance of role
        crossing) toward the expected carer (a daughter; a daughter-in-law); x (1 - .5 x the town's care.reach). At
        most 60. Not yet: money buying hours."""
        import sphere_data as SD
        D = SD.DEEP; H = D["care_hours"]
        L2 = self.P["layer_c"][1]; rm = self.rmask
        live = self.used & self.lv & (self.c >= L2)
        has = lambda r_: (rm & BIT[r_]) != 0
        age = (t - self.born) / 52.0; mine = (t - self.t0) / 52.0
        need = live & ((self.health < 0.35) | (age >= 82))
        fx = np.where(self.health < D["care_frail"], D["care_frail_x"], 1.0)
        rs = 1.0 - float(self.W.norm("role crossing"))
        wt = lambda fem_: 1.0 + D["care_role"] * rs * fem_                      # toward the expected carer
        own = wt(self.female.astype(float))
        sib = (live & has("sibling")) * wt(self.fem.astype(float))
        share = own / (own + sib.sum(1))                                         # of a parent's or grandparent's care
        pil = need & has("inlaw") & (age >= mine + 15)                          # the partner's parents
        ps_ = (self.used & self.lv & has("partner"))
        p_fem = (ps_ & self.fem).any(1).astype(float)
        share_il = np.where(ps_.any(1), own / (own + wt(p_fem)), 1.0)
        h = ((need & has("partner")) * H["partner"] * fx).sum(1) \
            + ((need & has("parent")) * H["parent"] * fx).sum(1) * share \
            + ((need & has("grandparent")) * H["grandparent"] * fx).sum(1) * share \
            + (pil * H["parent_in_law"] * fx).sum(1) * share_il
        W = self.W; E = W._sph_ev_tables()
        st = getattr(W, "sph_st", None)
        if st is not None and "care.reach" in E["own"]:
            k_ = E["own"].index("care.reach"); rch = np.clip(st[:, k_] + W.sph_st_soc[k_] - 0.5, 0, 1)[self.loc]
        else:
            rch = np.full(self.N, 0.5)
        return np.where(self.dead, 0.0, np.minimum(60.0, h * (1 - D["care_public"] * rch)))

    def haunts_info(self, n):
        """Life n's haunts (N1), best first, as World.place_info gives them, each with whether a setting of theirs meets
        there, and their rung in each sphere (N2): {sphere: rung word}. For the game's "your places"."""
        if not self.sph_h:
            return dict(haunts=[], rungs={})
        out = [dict(self.W.place_info(int(p_)), setting=bool(p_ in self.shnt[n])) for p_ in self.hnt[n] if p_ >= 0]
        return dict(haunts=out, rungs={s_: LADDER[int(self.rung[n, j_])] for j_, s_ in enumerate(SPHERES)})

    def _outputs_settings(self):
        """Cached monthly: the settings' part of the niche, of belonging and of the community driver."""
        act = self.skind >= 0; g = np.maximum(self.skind, 0); a = self._age()
        agew = np.where((g == G["class"]) & (12 <= a < 19), 1.5, 1.0)
        sw = self.sts * (0.5 + self.scoh) * agew * act
        self._setw = sw.sum(1); self._setmix = (sw[..., None] * self.snorm).sum(1)
        fitj = _uclip(likeness(self.snorm, self.w[:, None, :]), 0, 1)
        accj = 0.5 * fitj + 0.5 * self.srank
        self._belong_set = (self.sts * self.scoh * accj * act).sum(1)
        self._comm = (COMM_W[g] * self.scoh * accj * act).sum(1)
        self.community = _uclip(self.P["comm_k"] * (self._comm - self.P["comm_ref"]), -0.5, 0.5)

    # ------------------------------------------------------------------ the weekly, monthly and quarterly ticks
    def _read_S(self, t, S):
        S = S or {}
        N = self.N
        g_ = lambda k_, d_: d_ if S.get(k_) is None else S.get(k_)
        self.w = _norm(np.asarray(g_("w", self.w), float).reshape(N, C)); self.w32 = self.w.astype(np.float32)
        self.held = np.asarray(g_("held", self.held), bool).reshape(N, -1)
        self.res = np.asarray(g_("res", np.full((N, len(RESOURCES)), 0.5)), float).reshape(N, -1)
        self.stress = np.broadcast_to(np.asarray(g_("stress", 0.0), float), (N,))
        self.outlook = np.broadcast_to(np.asarray(g_("outlook", 0.45), float), (N,))
        self.attr = np.broadcast_to(np.asarray(g_("attr", 0), np.int64), (N,))
        self.risky = np.broadcast_to(np.asarray(g_("risky", 0.0), float), (N,))
        self.dead = np.broadcast_to(np.asarray(g_("dead", False), bool), (N,)).copy()
        if S.get("lens") is not None:
            self.lens = _norm(np.asarray(S["lens"], float).reshape(N, C))
        if S.get("sector") is not None:
            self.psector = np.broadcast_to(np.asarray(S["sector"], np.int64), (N,)).copy()
        ps_ = S.get("partner_same")   # the engine's own draw: the partner it holds is of the character's sex
        self.partner_same = None if ps_ is None else np.broadcast_to(np.asarray(ps_, bool), (N,)).copy()
        ts_ = S.get("title_standing")
        self.title_st = None if ts_ is None else np.asarray(ts_, float)
        ds_ = S.get("domain_standing")   # (N, len(DOMAINS)) 0-3: a title's standing in its own domain
        self.dom_st = None if ds_ is None else np.asarray(ds_, float)
        if getattr(self, "lw", False) and S.get("lead_has") is not None:   # S7: the leading titles held (LEAD_TITLES)
            self.lw_has = np.asarray(S["lead_has"], bool).reshape(N, -1)
        kc_ = S.get("children")          # the engine's living children (its alive[:, 5]; or S["alive"] with 6 columns)
        if kc_ is None and S.get("alive") is not None and np.ndim(S["alive"]) == 2 and np.shape(S["alive"])[1] > 5:
            kc_ = np.asarray(S["alive"])[:, 5]
        if kc_ is not None:
            self.kids_eng = np.broadcast_to(np.round(np.asarray(kc_, float)).astype(np.int64), (N,)).copy()

    def tick(self, t, S):
        """One week of the cast, plus the month's settings and the quarter's outer layers on their weeks."""
        self.week(t, S)
        if t % 4 == 0:
            self.month(t, S)
        if t % 13 == 0:
            self.quarter(t, S)

    def week(self, t, S):
        """Cast layers 1-2 (contact, closeness, deaths), the partner and children the engine holds, wants ripening,
        and everything the engine reads this week. S: the engine's person state (see the module's notes)."""
        if self._last_w == t:
            return
        self._last_w = t; self.t = t
        self.events = self._carry; self._carry = []; self.died[:] = 0
        self._read_S(t, S)
        for n_, kind_ in self.pend.pop(t, []):
            self._born_kin(n_, kind_, t)
        self._sync(t)
        self._close_step(t, 1)
        if self.P["auto_move"]:
            mv = np.nonzero(~self.dead & (self.rng.random(self.N) < self.move_wish(t)))[0]
            for n_ in mv:
                self.move(int(n_), t=t)
        if self.far_on:
            self._far_week(t)
        self._wants_week(t)
        self._outputs(t)

    def month(self, t, S):
        if self._last_m == t:
            return
        self._last_m = t; self.t = t
        if self._last_w != t:
            self._read_S(t, S)
        if self.sph_h:   # spheres phase 2: a life that has moved picks its haunts in the new town
            H_ = len(HAUNT_KINDS) * self.W.hp_s.shape[2] if getattr(self.W, "hp_s", None) is not None else 0
            if H_:
                mv_ = np.nonzero(~self.dead & (self.hnt[:, 0] >= 0) & (self.hnt[:, 0] // H_ != self.loc))[0]
                if len(mv_) or self.hpick < 0 or int(self._age(t)) != self.hpick:
                    if self.hpick < 0 or int(self._age(t)) != self.hpick:
                        self.hpick = int(self._age(t)); self._haunts_year(t)
                    else:
                        self._haunts_year(t, mv_)
        self._lifecourse(t)
        if self.far_on:
            self._far_month(t)
        if self._xsoc:
            self._lang_step(t)
        if self.sph_h and getattr(self.W, "hp_s", None) is not None:
            self._haunts_month(t)
        if self.sph_hr:
            self._sph_hours(t)
        if self.sph_mk:
            self._marks_year(t)
        if getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False):
            self._sph_year4(t)
        B = self._bits()
        if getattr(self, "comrade", None) is not None:   # phase 5: whoever shares a unit with them is a comrade from now on
            un_ = (self.skind == G["unit"])
            if un_.any():
                self.comrade |= (B * un_[:, None, :]).any(2)
        if self._last_set is None or t - self._last_set >= 8:   # the settings' slow drift: every second month
            self._settings_month(t, S, B, 1.0 if self._last_set is None else (t - self._last_set) / 4.0)
            self._last_set = t
        self._fsh(B)
        self._close_index()
        self._standing(t)
        self._outputs_settings()
        self._ties()

    def quarter(self, t, S):
        if self._last_q == t:
            return
        self._last_q = t; self.t = t
        if self._last_w != t:
            self._read_S(t, S)
        self._inst_refresh()
        self._norm_hist(t)
        self._outer_step(t)
        if t - self._last_lives >= 26:   # the cast's own light lives: every half year
            self._lives(t, (t - self._last_lives) / 52.0); self._last_lives = t
        self._ties()
        self._membership(t)
        self._new_people(t)
        self._roles(t)
        self._wants_arise(t)
        self._cleanup(t)
        self._alive_counts(np.arange(self.N))
        self._approval(t)   # felt acceptance per norm key: once a quarter (views move slowly)
        if self.lw:          # S7: the posts' quarter (after the settings' leaders are replaced)
            self._lead_q(t)

    # ------------------------------------------------------------------ ties: contact and closeness (spec 2 §3)
    def _tie_target(self, n2=None, k2=None):
        """What contact supports for slots (n2, k2) (index arrays of one shape; None: every slot, as (N, K)):
        contacts a year, the closeness they hold (ceiling x f / (f + f_half)), likeness to the character, ceiling.
        Likeness and the deliberate budget per unit of closeness^alloc_pow are the month's (_fsh, _close_index)."""
        P = self.P; f32 = np.float32
        if n2 is None:
            g = lambda A_: A_
            pp = lambda v_: v_[:, None]
        else:
            fi = _ix(np.asarray(n2, np.int64) * self.K + k2)
            g = lambda A_: np.take(A_, fi)
            pp = lambda v_: v_[n2]
        lk = g(self._lkm)
        near = g(self.mloc) == pp(self.loc.astype(self.mloc.dtype))
        if self._xsoc:   # someone in another society is far wherever they live
            near &= g(self.msoc) == pp(self.soc.astype(self.msoc.dtype))
        comm = float(self._wf("comm", 0.5))
        dist = np.where(near, f32(1.0), f32(P["dist_far"] + 0.5 * comm))
        hj = pp(self.hhj)
        hh = (((g(self.mset) >> np.maximum(hj, 0).astype(self.mset.dtype)) & 1) > 0) & (hj >= 0)
        core = np.where((g(self.rmask) & CORE) != 0, f32(1.3), f32(1.0))
        c = g(self.c)
        fdel = pp(self._Dn) * self._cpow(c) * core * dist * dist * ~hh
        f = g(self.fsh) + np.where(near, g(self.fkin), g(self.fkin_far) * f32(0.5 + comm)) + fdel
        cap = (f32(1 - P["cap_like"]) + f32(P["cap_like"]) * lk) * (f32(0.75) + f32(0.25) * g(self.trust))
        return f, cap * f / (f + f32(P["f_half"])), lk, cap

    def _cpow(self, c):
        """closeness^alloc_pow (2.5 by default: c^2 sqrt(c), cheaper than a power)."""
        ap = self.P["alloc_pow"]
        return c * c * np.sqrt(c) if ap == 2.5 else c ** np.float32(ap)

    def _close_step(self, t, dt_w):
        """Layers 1-2 weekly: closeness, contact and deaths of the close index (slow terms cached monthly)."""
        P = self.P; fi = self._fi
        ok = (np.take(self.uid, fi) == self._cuid) & np.take(self.lv, fi) & ~self.dead[:, None]   # dropped: id -1
        c = np.take(self.c, fi)
        f = self._cf0 + self._cdf * self._cpow(c)
        e = self._ccap * f / (f + np.float32(P["f_half"]))
        r_up, r_dk, r_dn = self._r_w if dt_w == 1 else [np.float32(1 - np.exp(-dt_w / 52.0 / P[k_]))
                                                         for k_ in ("tau_up", "tau_dn_kin", "tau_dn")]
        rdn = self._crdn if dt_w == 1 else np.where(self._ckin, r_dk, r_dn)
        if dt_w != 1 and getattr(self, "comrade", None) is not None:
            rdn = np.where(self._ccom, rdn * np.float32(0.5), rdn)
        rr = np.where(e > c, r_up, rdn)
        c2 = np.where(ok, c + (e - c) * rr, c).astype(np.float32)
        np.put(self.c, fi, c2)
        self._cok = ok; self._cc = c2   # for this week's on_act
        U = self.rng.random((2,) + f.shape, dtype=np.float32)
        met = ok & (U[0] < f * np.float32(dt_w / 52.0))
        np.put(self.last, fi[met], t)
        dies = ok & (U[1] < self._cq * np.float32(dt_w))
        if self.kids_eng is not None:   # the character's children die only by the engine's moment (R15, kill())
            dies &= (self._crm & BIT["child"]) == 0
        if dies.any():
            self._die(self._n2[dies], self.ci[dies], t)

    def _outer_step(self, t):
        """Quarterly: layers 3-4 (everyone outside the close index): closeness, contact, deaths; for all the living:
        the reading sharpens, trust drifts, a few ties break. Whole (N, K) arrays, masked, float32."""
        P = self.P; f32 = np.float32
        live = self.used & self.lv & ~self.dead[:, None]
        if not live.any():
            return
        f, e, lk, _ = self._tie_target()
        self._lk = lk
        out = live & ~self.inci
        c = self.c
        kin = (self.rmask & KINMASK) != 0
        r_up, r_dk, r_dn = (f32(1 - np.exp(-13 / 52.0 / P[k_])) for k_ in ("tau_up", "tau_dn_kin", "tau_dn"))
        c2 = np.where(out, c + (e - c) * np.where(e > c, r_up, np.where(kin, r_dk, r_dn)), c).astype(f32)
        self.c = c2; np.maximum(self.cmax, c2, out=self.cmax)
        U = self.rng.random((3,) + c.shape, dtype=f32)
        self.last[out & (U[0] < -np.expm1(f * f32(-0.25)))] = t
        age = self._qage = (t - self.born).astype(f32) * f32(1 / 52.0); self._qage_t = t
        q = np.minimum(self._q(age, self.health, self.mcls)
                       * np.where(age >= 65, self._rate_at("old_death", self.mloc), self._rate_at("illness", self.mloc)), f32(0.95))
        dies = out & (U[1] < -np.expm1(f32(0.25) * np.log1p(-q)))
        if self.kids_eng is not None:
            dies &= (self.rmask & BIT["child"]) == 0
        # the reading sharpens with shared time (contacts) and is bent by the character's lens
        # (in one pass: read += lam (pie - read), then read += m (lens - read), with m = 0.01 for the living)
        lam = np.where(live, -np.expm1(f * f32(-0.0025)), f32(0)); m_ = f32(0.01) * live
        a_ = (f32(1) - m_) * lam
        rd = self.read; tmp = self.pie * a_[..., None]; tmp += m_[..., None] * self.lens.astype(f32)[:, None, :]
        rd *= (f32(1) - a_ - m_)[..., None]; rd += tmp
        # trust drifts toward what likeness and shared history support
        tb = _uclip(f32(0.45) + f32(0.35) * lk + f32(0.05) * self.mgood - f32(0.1) * self.mbad, f32(0.02), f32(0.98))
        self.trust += live * f32(P["trust_k"]) * (tb - self.trust)
        # breaks: a fight or a betrayal (rarer among the alike; kin rarely)
        rm = self.rmask
        bp = f32(P["break_p"] * 0.25) * (f32(1.5) - lk) * np.where((rm & KINMASK) == 0, f32(1.0), f32(0.33))
        brk = live & (c2 >= P["layer_c"][2]) & ((rm & BIT["partner"]) == 0) & (U[2] < bp)
        for n_, k_ in zip(*_nz2(brk)):
            self._break(n_, k_, t)
        if dies.any():
            nn, kk = _nz2(dies)
            self._die(nn, kk, t)

    def _break(self, n, k, t, why="fight"):
        self.c[n, k] *= 0.3; self.trust[n, k] *= 0.6; self.brk[n, k] = t; self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="break", cid=int(self.uid[n, k]), role=self._rname(n, k), why=why))

    def _die(self, n, k, t, count=True):
        n = np.asarray(n, np.int64); k = np.asarray(k, np.int64)
        P = self.P
        hit = self.lv[n, k]
        n, k = n[hit], k[hit]
        if not len(n):
            return
        rm = self.rmask[n, k]
        if count:
            L2 = P["layer_c"][1]
            was_friend = ((rm & BIT["friend"]) != 0) & ((rm & KINMASK) == 0) & (self.c[n, k] >= L2)
            if was_friend.any():   # the engine's friend column is the closest friend (0/1): only their death counts
                fn, fk = n[was_friend], k[was_friend]
                un = np.unique(fn); rmu = self.rmask[un]; cu = self.c[un]
                cand = (self.used[un] & self.lv[un] & ((rmu & BIT["friend"]) != 0) & ((rmu & KINMASK) == 0) & (cu >= L2))
                best = np.argmax(np.where(cand, cu, -1), 1)
                was_friend[was_friend] = fk == best[np.searchsorted(un, fn)]
            for i_, r_ in enumerate(ENGINE_ROLES):
                h_ = was_friend if r_ == "friend" else (rm & BIT[r_]) != 0
                if h_.any():
                    self.died[:, i_] += np.bincount(_ix(n[h_]), minlength=self.N)
        self.lv[n, k] = False; self.died_t[n, k] = t; self.mset[n, k] = 0
        self.want[n, k] = -1; self.wstate[n, k] = 0
        ev = self.watch[n] & ((self.cmax[n, k] >= P["layer_c"][3]) | ((rm & KINMASK) != 0))
        ne, ke = n[ev], k[ev]
        if len(ne):
            self.events.extend(dict(n=n_, t=int(t), kind="died", cid=u_, role=r_, age=a_) for n_, u_, r_, a_ in
                               zip(ne.tolist(), self.uid[ne, ke].tolist(), self._rnames(ne, ke),
                                   ((t - self.born[ne, ke]) // 52).tolist()))
        self._alive_counts(np.unique(n))

    def kill(self, n, role, t=None):
        """An engine moment kills someone of this engine role (parent, sibling, friend, grandparent, partner): the
        member is chosen by the life table's odds; returns their cast id (or -1 when no one fits)."""
        t = self.t if t is None else t
        cand = np.nonzero(self._has_role(n, role) & self.lv[n])[0]
        if not len(cand):
            return -1
        q = self._q((t - self.born[n, cand]) / 52.0, self.health[n, cand]) + 1e-6
        k = int(self.rng.choice(cand, p=q / q.sum()))
        self._die([n], [k], t, count=False)
        return int(self.uid[n, k])

    def _has_role(self, n, role):
        u = self.used[n]
        if role == "friend":
            return u & ((self.rmask[n] & BIT["friend"]) != 0) & ((self.rmask[n] & KINMASK) == 0)
        if role == "partner":
            m_ = np.zeros(self.K, bool)
            if self.pslot[n] >= 0:
                m_[self.pslot[n]] = True
            return m_
        return u & ((self.rmask[n] & BIT[role]) != 0)

    def _close_index(self):
        """Monthly: the KC closest living people of each life (updated weekly), the denominator of deliberate
        contact, and the slow terms of their weekly update (contact from settings and kin, ceilings, death odds)."""
        P = self.P; N = self.N; f32 = np.float32
        np.maximum(self.cmax, self.c, out=self.cmax)
        ul = self.used & self.lv
        sc = np.where(ul, self.c, f32(-1))
        ci = np.argpartition(-sc, self.KC - 1, axis=1)[:, :self.KC]
        self.ci = ci; n2 = self._n2 = np.repeat(np.arange(N)[:, None], self.KC, 1)
        fi = self._fi = _ix(n2 * self.K + ci)   # flat (N, KC) indices into (N, K) arrays
        self.inci[:] = False
        np.put(self.inci, fi, np.take(sc, fi) >= 0)
        comm = float(self._wf("comm", 0.5))
        here = self.mloc == self.loc.astype(self.mloc.dtype)[:, None]
        if self._xsoc:
            here &= self.msoc == self.soc.astype(self.msoc.dtype)[:, None]
        dist = np.where(here, f32(1.0), f32(P["dist_far"] + 0.5 * comm))
        hh = (((self.mset >> np.maximum(self.hhj, 0).astype(self.mset.dtype)[:, None]) & 1) > 0) & (self.hhj[:, None] >= 0)
        core = np.where((self.rmask & CORE) != 0, f32(1.3), f32(1.0))
        self._den = (self._cpow(self.c) * core * dist * (ul & ~hh)).sum(1, dtype=np.float64) + 0.05
        a = self._age()
        dstage = 0.3 if a < 12 else 0.8 if a >= 70 else 1.0
        self._Dn = (P["D0"] * dstage * self.sociab * (0.5 + self.res[:, TIM]) / self._den).astype(f32)
        # cached for the weekly step: f = cf0 + cdf x c^alloc_pow, e = ccap x f / (f + f_half)
        f0, e0, lk, cap = self._tie_target(n2, ci)
        d2 = np.take(dist, fi)
        tk = lambda A_: np.take(A_, fi)
        self._cdf = (self._Dn[:, None] * tk(core) * d2 * d2 * ~tk(hh)).astype(f32)
        self._cf0 = np.maximum(f0 - self._cdf * self._cpow(tk(self.c)), 0).astype(f32)
        self._ccap = cap.astype(f32)
        self._crm = tk(self.rmask)
        self._ckin = (self._crm & KINMASK) != 0
        self._crdn = np.where(self._ckin, self._r_w[1], self._r_w[2])   # the weekly fading rate (kin fade slower)
        if getattr(self, "comrade", None) is not None:   # phase 5: comrades from a unit fade at half speed
            self._ccom = tk(self.comrade)
            self._crdn = np.where(self._ccom, self._crdn * np.float32(0.5), self._crdn)
        self._cuid = tk(self.uid)
        self._cpie = np.take(self.pie.reshape(-1, C), fi, axis=0).astype(np.float64)   # float64: exact weekly sums
        self._cpage = (self.t - tk(self.born)) / 52.0
        age = self._cpage; lc = tk(self.mloc)
        q = self._q(age, tk(self.health), tk(self.mcls)) * np.where(age >= 65, self._rate("old_death", lc), self._rate("illness", lc))
        self._cq = (np.minimum(q, 0.95) / 52.0).astype(f32)
        self._cav = (tk(self.health) * (0.5 + 0.5 * tk(self.money)) * (tk(self.mood) >= 0.35)).astype(f32)
        # the weight of each close person's colors in the niche, by the character's age and their role (monthly)
        a = self._age(); rm = self._crm
        if a < 12:
            self._caw = np.where((rm & BIT["parent"]) != 0, f32(3.0), np.where((rm & BIT["sibling"]) != 0, f32(1.5), f32(0.5)))
        elif a < 18:
            peer = ~self._ckin & (np.abs(self._cpage - a) <= 3)
            self._caw = np.where((rm & BIT["parent"]) != 0, f32(0.8), np.where(peer, f32(2.0), f32(1.0)))
        else:
            self._caw = np.where((rm & BIT["partner"]) != 0, f32(1.5), f32(1.0))
        # the engine's friend column (a close non-kin friend, layers 1-2: all in the close index); the other columns
        # change with births, deaths and partners, which recount them, and once a quarter in full
        self.alive[:, 2] = (((self._crm & BIT["friend"]) != 0) & ~self._ckin & (tk(self.c) >= P["layer_c"][1])
                            & tk(self.used) & tk(self.lv)).any(1)

    def _alive_counts(self, ns=None):
        """The engine's alive columns, counted from the cast: living parents, siblings (born), a closest friend (0/1),
        grandparents, partner (0/1)."""
        ns = np.arange(self.N) if ns is None else np.unique(np.atleast_1d(np.asarray(ns, np.int64)))
        if not len(ns):
            return
        L2 = self.P["layer_c"][1]
        u = self.used[ns] & self.lv[ns]; rm = self.rmask[ns]
        hasr = lambda r_: ((rm & BIT[r_]) != 0) & u
        ps = self.pslot[ns]
        pl = (ps >= 0) & self.lv[ns, np.maximum(ps, 0)]
        self._nch[ns] = (((rm & BIT["child"]) != 0) & self.used[ns]).sum(1)   # children, living or not
        self._nchl[ns] = (((rm & BIT["child"]) != 0) & u).sum(1)              # living children
        self.alive[ns] = np.stack([hasr("parent").sum(1), (hasr("sibling") & (self.born[ns] <= self.t)).sum(1),
                                   (hasr("friend") & ((rm & KINMASK) == 0) & (self.c[ns] >= L2)).any(1),
                                   hasr("grandparent").sum(1), pl], 1)

    # ------------------------------------------------------------------ the engine's commitments in the cast
    def _born_kin(self, n, kind, t):
        """A younger sibling, or the character's own child, is born."""
        if self.dead[n] and kind == "child":
            return
        P = self.P; rng = self.rng
        if kind == "sibling":
            pr = np.nonzero(self._has_role(n, "parent") & self.lv[n])[0]
            ctx = _norm(self.pie[n, pr].mean(0)) if len(pr) else self.family_mix[n]
            F = self._gen(np.array([n]), np.array([t]), t, ctx=ctx[None], sel=P["pie_inherit"])
            F["mcls"][:] = self.cls[n]; F["line"][:] = self.pline[n]; F["mloc"][:] = self.mloc[n, pr[0]] if len(pr) else self.loc[n]
            F["msoc"] = np.full(1, self.msoc[n, pr[0]] if len(pr) else self.soc[n])
            F["faith"] = np.where(rng.random(1) < P["p_inherit"], self.pfaith[n], F["faith"])
            F["party"] = np.where(rng.random(1) < P["p_inherit"], self.pparty[n], F["party"])
            home = (not self.own_home[n]) and self.hhj[n] >= 0
            sl = self._add(F, t, R["sibling"], c0=0.5 if home else 0.15, trust0=0.6, acc0=0.2,
                           setbit=self.hhj[n] if home else -1, quiet=True)
        else:
            self._born_kids(np.array([n]), t)
            return
        if self.watch[n] and len(sl):
            self.events.append(dict(n=int(n), t=int(t), kind="born", cid=int(self.uid[n, sl[0]]), role=kind))
        self._alive_counts([n])

    def _born_kids(self, ns, t):
        """The characters ns each have a child: the two parents' ways pass on moderately; faith and party most
        strongly (p_inherit); the child joins the household."""
        ns = np.asarray(ns, np.int64); ns = ns[~self.dead[ns]]
        if not len(ns):
            return
        P = self.P; rng = self.rng; E = len(ns)
        ps = self.pslot[ns]; hp = ps >= 0; pk = np.maximum(ps, 0)
        ctx = np.where(hp[:, None], 0.5 * (self.w[ns] + self.pie[ns, pk]), self.w[ns])
        F = self._gen(ns, np.full(E, t), t, ctx=ctx, sel=P["pie_inherit"])
        F["mcls"][:] = self.cls[ns]; F["line"][:] = self.pline[ns]; F["mloc"][:] = self.loc[ns]
        myf = np.where(self.held[ns, FAI], self.pfaith[ns], -1) if self.held.shape[1] > FAI else np.full(E, -1)
        F["faith"] = np.where(rng.random(E) < P["p_inherit"], myf, F["faith"])
        pp_ = np.where(hp, self.party[ns, pk], self.pparty[ns])
        F["party"] = np.where(rng.random(E) < P["p_inherit"], pp_, F["party"])
        for n_ in ns[self.hhj[ns] < 0]:
            self.hhj[n_] = self._new_setting(int(n_), "household", t); self.own_home[n_] = True
        sl = self._add(F, t, R["child"], c0=0.85, trust0=0.8, acc0=0.3, setbit=self.hhj[ns], quiet=True)
        ok = sl >= 0
        self.kof[ns[ok & hp], sl[ok & hp]] = self.uid[ns[ok & hp], ps[ok & hp]]
        for n_, s_ in zip(ns[ok], sl[ok]):
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="born", cid=int(self.uid[n_, s_]), role="child"))
        self._alive_counts(ns)

    def _sync(self, t):
        """The partner and the children follow the engine's commitments."""
        held = self.held; P = self.P; rng = self.rng; a = self._age(t)
        ps = self.pslot
        has = (ps >= 0)
        hasliving = has.copy(); hasliving[has] = self.lv[np.nonzero(has)[0], ps[has]]
        if held.shape[1] <= PAR:
            return
        for n_ in np.nonzero(held[:, PAR] & ~hasliving & ~self.dead)[0]:
            self._new_partner(int(n_), t)
        for n_ in np.nonzero(~held[:, PAR] & hasliving)[0]:
            k_ = int(ps[n_])
            self.rmask[n_, k_] = (self.rmask[n_, k_] & ~BIT["partner"]) | BIT["ex"]; self.role[n_, k_] = R["ex"]
            if self.hhj[n_] >= 0:
                self.mset[n_, k_] &= ~self._bit(self.hhj[n_])
            self.c[n_, k_] *= 0.35; self.trust[n_, k_] *= 0.6; self.brk[n_, k_] = t; self.pslot[n_] = -1
            self.par_change[n_] = t
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="ex", cid=int(self.uid[n_, k_])))
            self._alive_counts([n_])
        dead_p = has & ~hasliving
        self.pslot[dead_p] = -1
        if self.partner_same is not None:   # the cast partner's sex follows the engine's partner_same
            hp = np.nonzero(self.pslot >= 0)[0]
            self.fem[hp, self.pslot[hp]] = self.female[hp] == self.partner_same[hp]
        if self.kids_eng is not None:   # the engine's count: each child it adds joins the cast, born now (deaths: kill())
            need = np.where(self.dead, 0, self.kids_eng - self._nchl)
            for r_ in range(int(need.max()) if len(need) else 0):
                self._born_kids(np.nonzero(need > r_)[0], t)
        elif held.shape[1] > KID:   # no count from the engine: the first child when it holds children
            self._born_kids(np.nonzero(held[:, KID] & (self._nch == 0) & ~self.dead)[0], t)

    def _new_partner(self, n, t):
        """The engine's partner commitment begins: a prospect from the cast, or someone new chosen alike (spouses
        start alike: the best of six); their family and friends join through them."""
        P = self.P; rng = self.rng; a = self._age(t)
        same = rng.random() < P["same_sex"][int(_uclip(self.attr[n], 0, 4))]
        if self.partner_same is not None:
            same = bool(self.partner_same[n])
        want_fem = bool(self.female[n]) == bool(same)
        cand = np.nonzero(self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["prospect"] | BIT["friend"])) != 0)
                          & ((self.rmask[n] & KINMASK) == 0) & (self.fem[n] == want_fem) & ~self.mpart[n]
                          & (np.abs((t - self.born[n]) / 52.0 - a) <= 8))[0]
        if len(cand) and rng.random() < 0.6:
            sc = likeness(self.pie[n, cand], self.w[n]) * self.c[n, cand] + 0.5 * (self.want[n, cand] == WI["love"])
            k = int(cand[np.argmax(sc)])
        else:
            born = t - ((a + rng.normal(1.5 if not want_fem else -1.0, 3.5, 6)) * 52).astype(np.int64)
            F = self._gen(np.full(6, n), born, t)
            best = int(np.argmax(likeness(F["pie"], self.w[n])))
            F = {k2: (v2[best:best + 1] if np.ndim(v2) else v2) for k2, v2 in F.items()}
            F["fem"] = np.array([want_fem]); F["mpart"] = np.array([False]); F["nkids"] = np.array([0])
            k = int(self._add(F, t, R["partner"], c0=0.5, trust0=0.7, acc0=0.15, quiet=True)[0])
            # the partner's family and friends come through them (spec 2 §1 "through others")
            pa = (t - self.born[n, k]) / 52.0
            fam_b = []
            for d_ in (rng.normal(30, 5), rng.normal(32, 5)):
                if rng.random() < self._surv(pa, pa + d_):
                    fam_b.append(t - int((pa + d_) * 52))
            nsb = rng.choice(4, p=P["sib_p"])
            fam_b += [t - int((pa + rng.normal(0, 4)) * 52) for _ in range(nsb)]
            if fam_b:
                Fi = self._gen(np.full(len(fam_b), n), np.array(fam_b), t, ctx=np.tile(self.pie[n, k], (len(fam_b), 1)),
                               sel=P["pie_inherit"])
                Fi["mloc"][:] = self.mloc[n, k]; Fi["line"][:] = self.line[n, k]; Fi["msoc"] = np.full(len(fam_b), self.msoc[n, k])
                self._add(Fi, t, R["inlaw"], c0=0.1, trust0=0.5, kof=np.full(len(fam_b), self.uid[n, k]), quiet=True)
            nf = int(rng.integers(3, 6))
            Ff = self._gen(np.full(nf, n), t - ((pa + rng.normal(0, 4, nf)) * 52).astype(np.int64), t,
                           ctx=np.tile(self.pie[n, k], (nf, 1)), sel=0.4)
            self._add(Ff, t, R["acquaintance"], c0=0.06, trust0=0.5, kof=np.full(nf, self.uid[n, k]), quiet=True)
        self.rmask[n, k] = (self.rmask[n, k] & ~BIT["prospect"]) | BIT["partner"]; self.role[n, k] = R["partner"]
        self.c[n, k] = max(float(self.c[n, k]), 0.85); self.trust[n, k] = max(float(self.trust[n, k]), 0.75)
        self.mloc[n, k] = self.loc[n]; self.msoc[n, k] = self.soc[n]; self.pslot[n] = k; self.par_change[n] = t
        if self.want[n, k] == WI["love"]:
            self.want[n, k] = -1; self.wstate[n, k] = 0
        if a >= 17 and not self.own_home[n]:
            self._leave_home(n, t)
        if self.hhj[n] < 0:
            self.hhj[n] = self._new_setting(n, "household", t); self.own_home[n] = True
        self.mset[n, k] |= self._bit(self.hhj[n])
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="partner", cid=int(self.uid[n, k])))
        self._alive_counts([n])

    def _leave_home(self, n, t):
        """The character leaves the parents' household for one of their own (the partner and children come along)."""
        old = self.hhj[n]
        if old >= 0:
            self._leave(n, int(old), t, "left home")
        j = self._new_setting(n, "household", t)
        self.hhj[n] = j; self.own_home[n] = True
        if j >= 0:
            self.sanch[n, j] = self.w[n]; self.snorm[n, j] = self.w[n]
            mates = np.nonzero(self.used[n] & self.lv[n] & (((self.rmask[n] & BIT["partner"]) != 0)
                                                            | (((self.rmask[n] & BIT["child"]) != 0) & ((t - self.born[n]) < 18 * 52))))[0]
            self.mset[n, mates] |= self._bit(j)

    # ------------------------------------------------------------------ the life course of settings (spec 3 §1.6)
    def _lifecourse(self, t):
        """Monthly: the groups a life holds by age and by the engine's commitments (spec 3 §1.6)."""
        self._defer = []
        try:
            self._lifecourse_(t)
        finally:
            batch, self._defer = self._defer, None
            self._fill_members(batch, t)

    def _lifecourse_(self, t):
        a = self._age(t); P = self.P; rng = self.rng; N = self.N; held = self.held
        live = ~self.dead
        has = lambda g_: (self.skind == G[g_]).any(1)
        nz = lambda m_: np.nonzero(m_)[0]
        mo = 1 / 12.0
        if a >= 4:
            self._join_many(nz(live & ~has("neighbours")), "neighbours", t)
        # school: a class from 5, a new one at 11, study after 18 for some
        cj = np.where(self.skind == G["class"], self.sjoin, -1).max(1)
        if 5 <= a < 18:
            need = live & ((cj < 0) | ((a >= 11) & (cj < self.t0 + 11 * 52)))
            for n_ in nz(need & (cj >= 0)):
                self.leave(int(n_), "class", t, "school changed")
            self._join_many(nz(need), "class", t)
        if a >= 18:
            sec = live & (cj >= 0) & (cj < self.t0 + int(17.5 * 52))
            leaving = sec | (live & (cj >= 0) & (t - cj > int(3.5 * 52)))
            for n_ in nz(leaving):
                self.leave(int(n_), "class", t, "finished")
            if a < 19:
                pu = np.asarray(P["p_uni"])[_uclip(self.cls, 0, 2)]
                self._join_many(nz(sec & (rng.random(N) < pu)), "class", t)
        nvol = _isin_small(self.skind, VOLUNTARY).sum(1)
        if 6 <= a < 18:   # children's and teenagers' activities; a scene or an online community for some teens
            self._join_many(nz(live & (nvol < self.vol_tgt) & (rng.random(N) < 0.1)), "club", t)
            if a >= 13:
                self._join_many(nz(live & ~has("scene") & (rng.random(N) < 0.3 / 60)), "scene", t)
                if self._tech("internet"):
                    self._join_many(nz(live & ~has("online") & (rng.random(N) < 0.5 / 60)), "online", t)
        if a >= 18:
            vj = P["vol_join"]
            self._join_many(nz(live & (nvol < 3) & (rng.random(N) < vj["club"] * mo)), "club", t)
            if a < 40:
                self._join_many(nz(live & ~has("scene") & (rng.random(N) < vj["scene"] * mo)), "scene", t)
            if a < 70 and self._tech("internet"):
                self._join_many(nz(live & ~has("online") & (rng.random(N) < vj["online"] * mo)), "online", t)
        # leaving groups: a steady rate, faster in old age (settings thin out)
        lv = P["vol_leave"] * (1 + max(0.0, a - 70) / 10) * (0.6 if a < 18 else 1.0) * mo
        vol_or_on = _isin_small(self.skind, np.concatenate([VOLUNTARY[VOLUNTARY != G["congregation"]], [G["online"]]]))
        for n_, j_ in zip(*np.nonzero(vol_or_on & (rng.random(self.skind.shape) < lv) & live[:, None])):
            if self.skind[n_, j_] == G["movement"] and self.srank[n_, j_] > 0.6:
                continue
            self._leave(int(n_), int(j_), t, "drifted away")
        # work, faith and community follow the engine's commitments
        if held.shape[1] > FAI and a >= 14:
            self._join_many(nz(live & held[:, CAR] & ~has("work")), "work", t)
            for n_ in nz(live & ~held[:, CAR] & has("work")):
                self.leave(int(n_), "work", t, "job ended")
            nf = nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith < 0))
            for n_ in nf:
                self.pfaith[n_] = self._faith_for(int(n_))
            self._join_many(nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith >= 0)), "congregation", t)
            if a >= 16:
                for n_ in nz(live & ~held[:, FAI] & has("congregation")):
                    self.leave(int(n_), "congregation", t, "left the faith")
            nvol = _isin_small(self.skind, VOLUNTARY).sum(1)
            self._join_many(nz(live & held[:, COM] & (nvol == 0)), "club", t)
        elif held.shape[1] > FAI and a < 14:   # a child goes to the congregation with a practising family
            self._join_many(nz(live & held[:, FAI] & ~has("congregation") & (self.pfaith >= 0)), "congregation", t)
        # leaving home; care homes in old age
        if a >= 17.5:
            for n_ in nz(live & ~self.own_home & (rng.random(N) < P["leave_home"] * mo)):
                self._leave_home(int(n_), t)
        if a >= 75:
            hl = self.res[:, HEA] if self.res.shape[1] > HEA else np.full(N, 0.5)
            self._join_many(nz(live & (hl < 0.35) & ~has("ward") & (rng.random(N) < P["care_home"] * mo)), "ward", t)
        # parents separate while the child is young
        if a < 18:
            for n_ in nz(live & ~self.own_home & (rng.random(N) < P["sep_p"] * mo)):
                if self.hhj[n_] < 0:
                    continue
                pa = self._has_role(n_, "parent") & self.lv[n_]
                ps = np.nonzero(pa & ~self.fem[n_] & (((self.mset[n_] >> self.hhj[n_]) & 1) > 0))[0]
                if len(ps) and pa.sum() == 2:
                    self.mset[n_, ps] &= ~self._bit(self.hhj[n_]); self.par_apart[n_] = True
                    if self.watch[n_]:
                        self.events.append(dict(n=int(n_), t=int(t), kind="parents_apart", cid=int(self.uid[n_, ps[0]])))
        # the character's children leave home at 18 to 24; more children while the engine holds children
        isch = (self.rmask & BIT["child"]) != 0
        if a >= 30:   # (a child of the character's is 18 only from about 34)
            hb = (((self.mset >> np.maximum(self.hhj, 0).astype(self.mset.dtype)[:, None]) & 1) > 0) & (self.hhj >= 0)[:, None]
            cn, ck = _nz2(isch & self.used & self.lv & hb)
            go = ((t - self.born[cn, ck]) >= 18 * 52) & (rng.random(len(cn)) < 0.25 * mo)
            for n_, k_ in zip(cn[go], ck[go]):
                self.mset[n_, k_] &= ~self._bit(self.hhj[n_])
        if held.shape[1] > KID and a < 44 and self.kids_eng is None:   # (when the engine counts them, its count rules)
            nk = isch.sum(1)
            more = live & held[:, KID] & (self.pslot >= 0) & (nk >= 1) & (nk < 4)
            p_ = np.where(nk == 1, 0.15, 0.07) * mo
            self._born_kids(nz(more & (rng.random(N) < p_)), t)

    def _tech(self, key):
        try:
            return bool(self.W.tech_has(key))
        except Exception:
            return True

    # ------------------------------------------------------------------ the cast's own lives (light; ruling R8)
    def _lives(self, t, dy=0.5):
        """Every half year (dy: years since the last step): health and illness, jobs, partners, children, moves, mood
        and colors of every cast member (light lives, ruling R8); whole (N, K) arrays, masked to the living, float32."""
        P = self.P; rng = self.rng; N = self.N; f32 = np.float32; nq = dy / 0.25   # quarters
        live = self.used & self.lv & ~self.dead[:, None]
        if not live.any():
            return
        U = rng.random((6,) + live.shape, dtype=f32)
        age = self._qage if getattr(self, "_qage_t", None) == t else (t - self.born).astype(f32) * f32(1 / 52.0)
        rm = self.rmask; part = (rm & BIT["partner"]) != 0
        # health: the age curve, serious illness (season, pandemic and medicine through W.rate_mult)
        hb = _uclip(f32(1) - f32(0.012) * np.maximum(age - 35, f32(0)), f32(0.2), f32(1))
        x_ = np.maximum(age - 30, f32(0))
        tk_ = self.far_par["take"] if self.far_on else None   # far_ties: the towns' events take over a share
        ill = live & (U[0] < (f32(P["ill_p"][0]) + f32(P["ill_p"][1] / 10) * x_ * np.sqrt(x_))
                      * f32(dy if tk_ is None else dy * (1 - tk_[2])) * self._rate_at("illness", self.mloc))
        h = self.health
        self.health = _uclip(h + f32(1 - 0.85 ** nq) * (hb - h) - f32(0.35) * ill, f32(0.02), f32(1))   # (the dead's drift is unread)
        # jobs: loss by the economy and sector, finding work by unemployment, retirement
        jm = np.asarray(self._rate("jobloss"), float)
        sec = self.sector
        jl = np.take(jm.astype(f32), _ix(sec), mode="clip") if jm.ndim == 1 and len(jm) > 1 else f32(jm)
        emp = self.emp
        lose = live & emp & (U[1] < f32(P["jobloss"] * dy if tk_ is None else P["jobloss"] * dy * (1 - tk_[0])) * jl)
        un = float(self._unemp("unemp")); nat = float(self._unemp("natural"))
        wa = (age >= 18) & (age < 64) & (sec >= 0)
        find = live & ~emp & wa & (U[2] < np.where(age < 19, f32(1 - 0.5 ** nq),
                                                   f32(min(1.0, P["rehire"] * _uclip(1 - 4 * (un - nat), 0.3, 1.5) * dy
                                                           * (1 if tk_ is None else 1 - tk_[1])))))
        emp2 = ((emp & ~lose) | find) & (age < 65)
        self.emp = emp2
        tm = (np.take(np.array([0.3, 0.5, 0.75], f32), _ix(self.mcls), mode="clip") + f32(0.12) * emp2
              - f32(0.15) * (~emp2 & (age >= 18) & (age < 65)))
        self.money = _uclip(self.money + f32(1 - 0.8 ** nq) * (tm - self.money), f32(0.02), f32(1))
        # partners, divorces, children (the character's own partner follows the engine)
        mp = self.mpart
        cpl = live & ~mp & (age >= 20) & (age < 70) & (U[3] < P["couple_p"] * dy)
        div = live & mp & (age < 75) & ~part & (U[3] < P["divorce_p"] * dy)
        self.mpart = (mp | cpl) & ~div
        kid = live & self.mpart & ~part & (age >= 22) & (age < 42) & (self.nkids < 4) & (U[4] < P["kid_p"] * dy)
        self.nkids = (self.nkids + kid).astype(np.int8)
        # moves away (a share of all moves leave the locality); the household does not move without the character
        hj = self.hhj[:, None]
        inhh = (hj >= 0) & (((self.mset >> np.maximum(hj, 0).astype(self.mset.dtype)) & 1) > 0)
        mr = np.take(self._mr_tab, age.astype(np.intp), mode="clip")
        mv = live & (age >= 18) & ~inhh & (U[5] < mr * f32(P["far_share"] * dy))
        if mv.any():
            mn, mk = _nz2(mv)
            nl_ = rng.choice(self.n_loc, len(mn), p=self.loc_p)
            if self._xsoc:   # people living in another society move there (their places are not modelled here)
                nl_ = np.where(self.msoc[mn, mk] == self.soc[mn], nl_, self.mloc[mn, mk])
            self.mloc[mn, mk] = nl_
            loc_bits = np.zeros(len(mn), self.mset.dtype)
            for j_ in range(self.M):
                loc_bits |= np.where(np.isin(self.skind[mn, j_], LOCAL_KINDS), self._bit(j_), 0).astype(self.mset.dtype)
            self.mset[mn, mk] &= ~loc_bits
        # mood: events knock it down, it comes back
        bad = ill | lose | div
        self.mood = _uclip(self.mood + f32(1 - 0.8 ** nq) * (f32(0.6) - self.mood) - f32(0.3) * bad, f32(0), f32(1))
        # colors: a slow drift toward their surroundings, faster when young; the character's children toward the
        # household (upbringing); partners barely converge (Caspi, Herbener and Ozer 1992); a step after a big event
        dn, dk = _nz2(live & ((age < 25) | (self.c >= P["layer_c"][2]) | part))
        da, dp = age[dn, dk], part[dn, dk]
        rate = f32(nq) * np.where(dp, f32(0.0015), np.interp(da, [0, 12, 18, 25, 40, 60], [0.04, 0.04, 0.03, 0.01, 0.004, 0.002]).astype(f32))
        jf = _LOWBIT[self.mset[dn, dk]]   # the context: the first group they share with the character, else the place
        lm = _norm(np.asarray(self.W.loc_mix, float)).astype(f32)
        ctx = np.take(lm, _ix(self.mloc[dn, dk]), axis=0, mode="clip")
        hj_ = jf >= 0
        ctx[hj_] = self.snorm[dn[hj_], jf[hj_]]
        ctx[dp] = self.w32[dn[dp]]
        chm = ((self.rmask[dn, dk] & BIT["child"]) != 0) & (da < 18) & (self.hhj[dn] >= 0)
        if chm.any():   # the character's children are brought up in the household
            ctx[chm] = self.snorm[dn[chm], self.hhj[dn[chm]]]
        pi = self.pie[dn, dk]
        pi += rate[:, None] * (ctx - pi)
        bd = bad[dn, dk]
        if bd.any():
            st_ = (0.05 * (1 - _uclip(da[bd], 0, 90) / 100))[:, None]
            pi[bd] += st_ * (self._dirichlet(np.full((int(bd.sum()), C), 1.0 / C), 1.0) - pi[bd])
        self.pie[dn, dk] = pi = _norm(pi)
        self._psq[dn, dk] = _csum(pi * pi)
        # what reaches the character: their crises sharpen the reading; events of the close
        close = live & (self.c >= P["layer_c"][2])
        cr = close & bad
        rv_ = None
        if cr.any():
            cn, ck = np.nonzero(cr)
            r_old = self.read[cn, ck]
            err0 = 0.5 * np.abs(r_old - self.pie[cn, ck]).sum(-1)
            self.read[cn, ck] = r_old + 0.3 * (self.pie[cn, ck] - r_old)
            rv_ = (err0 >= 0.45) & self.watch[cn]   # (cn, ck) in row order: the order _nz2 gives
        L2 = P["layer_c"][1]
        wn = self.watch[:, None] & close
        for kind_, m_ in (("ill", ill), ("lost_job", lose), ("divorce", div), ("moved_away", mv)):
            self._evs(*_nz2(m_ & wn), t, kind_)
        if rv_ is not None and rv_.any():   # a crisis shows who they are: the reading before and after
            rn, rk = cn[rv_], ck[rv_]
            self.events.extend(dict(n=n_, t=int(t), kind="reveal", cid=u_, role=r_, old=[round(float(x_), 3) for x_ in o_],
                                    new=[round(float(x_), 3) for x_ in w_])
                               for n_, u_, r_, o_, w_ in zip(rn.tolist(), self.uid[rn, rk].tolist(), self._rnames(rn, rk),
                                                             r_old[rv_], self.read[rn, rk]))
        c2 = self.c >= L2
        self.cont_t[(div & c2).any(1), 0] = t; self.cont_t[(lose & c2).any(1), 1] = t
        # the character's children's children; siblings' children
        gk = kid & ((rm & (BIT["child"] | BIT["sibling"])) != 0)
        if gk.any():
            gn, gkk = _nz2(gk)
            F = self._gen(gn, np.full(len(gn), t), t, ctx=self.pie[gn, gkk], sel=P["pie_inherit"])
            F["mloc"] = self.mloc[gn, gkk]; F["line"] = self.line[gn, gkk]; F["msoc"] = self.msoc[gn, gkk]
            self._inherit(F, self.faith[gn, gkk], self.party[gn, gkk])
            isch = (self.rmask[gn, gkk] & BIT["child"]) != 0
            sl = self._add(F, t, np.where(isch, R["grandchild"], R["kin"]), c0=np.where(isch, 0.35, 0.12), trust0=0.6,
                           kof=self.uid[gn, gkk], quiet=True)
            for n_, s_, ok_ in zip(gn, sl, isch):
                if self.watch[n_] and ok_ and s_ >= 0:
                    self.events.append(dict(n=int(n_), t=int(t), kind="born", cid=int(self.uid[n_, s_]), role="grandchild"))

    def _inherit(self, F, faith, party):
        """Faith and party pass from a parent most strongly (p_inherit)."""
        E = len(F["n"]); pi = self.P["p_inherit"]
        F["faith"] = np.where(self.rng.random(E) < pi, faith, F["faith"])
        F["party"] = np.where(self.rng.random(E) < pi, party, F["party"])
        return F

    def _membership(self, t):
        """Settings keep their size: members leave (turnover, moves, deaths) and new ones are met."""
        P = self.P; rng = self.rng; N, M = self.N, self.M
        act = (self.skind >= 0) & (self.skind != G["household"])
        churn = np.where(act, KTA[np.maximum(self.skind, 0), K_CHURN] * 0.25, 0).astype(np.float32)
        keep = np.zeros((N, self.K), bool)
        ls = self.slead
        keep[np.nonzero(ls >= 0)[0], ls[ls >= 0]] = True
        mn, mk = _nz2((self.mset > 0) & ~keep)   # members leave each of their groups at its turnover
        if len(mn):
            u_ = rng.random(len(mn), dtype=np.float32)
            gone = ((u_[:, None] < churn[mn]) * (1 << np.arange(M))).sum(1).astype(self.mset.dtype)
            self.mset[mn, mk] &= ~gone
        B = self._bits()
        cnt = self._count(B)
        deficit = np.where(act, np.maximum(self.sncast - cnt.astype(np.int64), 0), 0)
        if deficit.any():
            nn, jj = np.nonzero(deficit)
            rep = deficit[nn, jj]
            self._members(np.repeat(nn, _ix(rep)), np.repeat(jj, _ix(rep)), t, quiet=True)
        # a leader who left or died is replaced by the most standing member
        for n_, j_ in zip(*np.nonzero(act & (self.slead == -1) & np.isin(self.skind, [G[g_] for g_ in GROUP_KINDS if K_LEAD[G[g_]]]))):
            mem = np.nonzero(B[n_, :, j_] > 0)[0]
            if len(mem):
                k_ = int(mem[np.argmax(self.stand[n_, mem] + 0.1 * rng.random(len(mem)))])
                if self.lw and self._lead_vacant(n_, j_, k_, t):   # S7: the character stands higher and takes the lead
                    continue
                self.slead[n_, j_] = k_
                lr = K_LEAD[int(self.skind[n_, j_])]
                self.rmask[n_, k_] |= BIT[lr]

    def _new_people(self, t):
        """By chance and through others: strangers who stay, friends of friends (quarterly)."""
        rng = self.rng; N = self.N; a = self._age(t); P = self.P
        live = ~self.dead
        if a < 3:
            return
        L2 = P["layer_c"][1]
        nfr = (((self.rmask & BIT["friend"]) != 0) & (self.c >= L2) & self.lv).sum(1)
        lam_ff = P["meet"][0] * np.minimum(nfr, 6) / 3 * (a >= 12) * self.sociab
        lam_ch = P["meet"][1] * (a >= 14) * self.sociab
        k_ff = rng.poisson(lam_ff) * live; k_ch = rng.poisson(lam_ch) * live
        nn = np.repeat(np.arange(N), _ix(k_ff))
        if len(nn):   # someone a friend brings along: alike the friend
            frm = ((self.rmask[nn] & BIT["friend"]) != 0) & (self.c[nn] >= L2) & self.lv[nn]
            pick = np.argmax(np.where(frm, rng.random(frm.shape, dtype=np.float32), -1), 1)
            ctx = np.where(frm.any(1)[:, None], self.pie[nn, pick], self.w[nn])
            ages = np.maximum(5, a + rng.normal(0, 5, len(nn)))
            F = self._gen(nn, t - (ages * 52).astype(np.int64), t, ctx=ctx, sel=0.4)
            self._add(F, t, R["acquaintance"], c0=0.08, trust0=0.5, ctx_read=ctx, quiet=True)
        nn = np.repeat(np.arange(N), _ix(k_ch))
        if len(nn):   # by chance: travel, online, a stranger who stays
            ages = np.maximum(5, a + rng.normal(0, 10, len(nn)))
            far = rng.random(len(nn)) < 0.4
            loc = np.where(far, rng.choice(self.n_loc, len(nn), p=self.loc_p), self.loc[nn])
            F = self._gen(nn, t - (ages * 52).astype(np.int64), t, loc=loc)
            self._add(F, t, R["acquaintance"], c0=0.06, trust0=0.45, quiet=True)

    def _roles(self, t):
        """Roles that emerge: friend (a close non-kin tie), mentor, rival, prospect, elder (quarterly)."""
        P = self.P; rng = self.rng; a = self._age(t); L1, L2, L3, L4 = P["layer_c"]
        rm = self.rmask
        age = self._qage if getattr(self, "_qage_t", None) == t else (t - self.born).astype(np.float32) / np.float32(52)
        un = self.used & self.lv & ((rm & (KINMASK | BIT["partner"] | BIT["ex"])) == 0)   # living non-kin
        newf = un & (self.c >= L2) & ((rm & BIT["friend"]) == 0) & (a >= 3)
        self.rmask[newf] |= BIT["friend"]
        for n_, k_ in zip(*_nz2(newf & self.watch[:, None] & (a >= 12))):
            self.events.append(dict(n=int(n_), t=int(t), kind="friend", cid=int(self.uid[n_, k_])))
        rm = self.rmask
        lk = self._lk if getattr(self, "_lk", None) is not None else likeness(self.pie, self.w[:, None, :])

        def nz(m_, p_):   # the candidates in m_, each taken with chance p_ this quarter
            nn_, kk_ = _nz2(m_)
            h_ = rng.random(len(nn_)) < p_
            return nn_[h_], kk_[h_]
        new = {}
        if a >= 14:
            new["mentor"] = nz(un & (self.stand >= 1) & (age >= a + 10) & (self.trust >= 0.6) & (self.c >= L3)
                               & ((rm & BIT["mentor"]) == 0), 0.15 * 0.25)
        if a >= 10:
            new["rival"] = nz(un & ((rm & (BIT["colleague"] | BIT["classmate"])) != 0) & (np.abs(age - a) <= 8) & (lk < 0.45)
                              & ((rm & BIT["rival"]) == 0), 0.04 * 0.25)
        if a >= 15:   # someone of the sex the character is drawn to, single, near in age, close enough and alike
            pn, pk = _nz2(un & (self.pslot < 0)[:, None] & (np.abs(age - a) <= 6) & ~self.mpart & (self.c >= L3)
                                & (lk >= 0.5) & ((rm & BIT["prospect"]) == 0))
            at = self.attr[pn]; r_ = rng.random((2, len(pn)))
            comp = np.where(self.fem[pn, pk] != self.female[pn], (at <= 2) | ((at == 3) & (r_[0] < 0.15)),
                            (at >= 2) | ((at == 1) & (r_[0] < 0.15)))
            h_ = comp & (r_[1] < 0.3 * 0.25)
            new["prospect"] = (pn[h_], pk[h_])
        new["elder"] = _nz2(un & (age >= 65) & (self.stand >= 1) & ((rm & BIT["elder"]) == 0))
        for r_, (nn_, kk_) in new.items():
            self.rmask[nn_, kk_] |= BIT[r_]
        # partnered: prospects fade back to friends or acquaintances
        hp = np.nonzero(self.pslot >= 0)[0]
        self.rmask[hp] &= ~BIT["prospect"]
        for kind_ in ("mentor", "rival", "prospect"):
            for n_, k_ in zip(*new.get(kind_, ((), ()))):
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="role", role=kind_, cid=int(self.uid[n_, k_])))

    def _cleanup(self, t):
        """Faces with no tie and the faded with no role or mark go back to the statistics; the long dead are let go."""
        P = self.P; L4 = P["layer_c"][3]
        u = self.used
        role_keep = (self.rmask & (KINMASK | BIT["partner"] | BIT["ex"] | BIT["rival"] | BIT["mentor"])) != 0
        marks = (self.mgood + self.mbad > 0) | (self.debt != 0) | self.secret
        faded = u & self.lv & (self.c < L4 * 0.67) & (self.mset == 0) & ~role_keep & ~marks & ((t - self.since) > 13)
        faded |= u & self.face & self.lv & (self.c < 0.1) & ((t - self.since) > 26)
        gone = u & ~self.lv & ((t - self.died_t) > 10 * 52) & ((self.rmask & CORE) == 0)
        nn, kk = _nz2(faded | gone)
        if len(nn):
            self._drop(nn, kk, t, quiet=True)

    # ------------------------------------------------------------------ wants (spec 2 §5)
    def _wants_arise(self, t):
        P = self.P; rng = self.rng; a = self._age(t); L1, L2, L3, L4 = P["layer_c"]
        if a < 14:
            return
        cand = self.used & self.lv & (self.want < 0) & ~self.dead[:, None] & ((self.c >= L3) | (self.brk > NEVER // 2))
        nn, kk = _nz2(cand)
        if not len(nn):
            return
        age = (t - self.born[nn, kk]) / 52.0; c = self.c[nn, kk]; rm = self.rmask[nn, kk]
        has = lambda r_: (rm & BIT[r_]) != 0
        par = has("parent"); gp = has("grandparent")
        H = np.zeros((len(nn), NW))
        held = self.held
        hk = lambda i_: held[nn, i_] if held.shape[1] > i_ else np.zeros(len(nn), bool)
        H[:, WI["money"]] = 0.12 * c * (c >= L2) * (((~self.emp[nn, kk]) & (age >= 18) & (age < 65)) | (self.money[nn, kk] < 0.2))
        H[:, WI["care"]] = 0.6 * (par | gp | has("partner")) * ((self.health[nn, kk] < 0.35) | (age >= 82))
        H[:, WI["successor"]] = 0.15 * par * self.fbiz[nn, kk] * (18 <= a <= 40) * (age >= 50)
        H[:, WI["grandchild"]] = 0.25 * par * (age >= 58) * ~hk(KID) * (25 <= a <= 45)
        comp = np.where(self.fem[nn, kk] != self.female[nn], self.attr[nn] <= 2, self.attr[nn] >= 2)
        lk = self._lk[nn, kk] if getattr(self, "_lk", None) is not None else likeness(self.pie[nn, kk], self.w[nn])
        H[:, WI["love"]] = (0.08 * lk * comp * ~hk(PAR) * (a >= 16) * (np.abs(age - a) <= 8) * ~self.mpart[nn, kk]
                            * ((rm & (KINMASK | BIT["ex"])) == 0) * (c >= 0.3))
        H[:, WI["rival"]] = (0.4 * has("rival") + 0.06 * has("colleague") * (lk < 0.5)) * (a >= 16)
        fg0, fgw = P["forgive"]
        H[:, WI["forgiveness"]] = (fg0 * ((t - self.brk[nn, kk]) >= fgw) * (self.brk[nn, kk] > NEVER // 2)
                                   * (c < 0.6 * self.cmax[nn, kk]) * (self.cmax[nn, kk] >= L2) * ((rm & KINMASK) != 0))
        H[:, WI["home"]] = 0.15 * (par | gp) * ~self._here(nn, kk) * (a >= 18)
        H[:, WI["stop"]] = 0.25 * self.risky[nn] * (c >= L1)
        H[:, WI["secret"]] = 0.03 * (self.trust[nn, kk] >= 0.75) * (c >= L1) * ~has("partner")
        tot = H @ np.ones(NW)
        occ = rng.random(len(nn)) < 1 - np.exp(-0.25 * tot)
        if not occ.any():
            return
        cum = np.cumsum(H[occ], 1) / tot[occ, None]
        key = (rng.random(occ.sum())[:, None] > cum).sum(1)
        n2, k2 = nn[occ], kk[occ]
        self.want[n2, k2] = key; self.wripe[n2, k2] = 0; self.wstate[n2, k2] = 1; self.wknown[n2, k2] = False
        fg = key == WI["forgiveness"]   # a break brings one wish to make peace at most (answered or not, it is spent)
        self.brk[n2[fg], k2[fg]] = NEVER
        for n_, k_, w_ in zip(n2, k2, key):
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="begins", key=CAST_WANTS[int(w_)],
                                        cid=int(self.uid[n_, k_]), known=False, **self._far_cause(n_, k_, t)))

    def _wants_week(self, t):
        """Wants ripen; ripe ones fall due; wants that no longer hold are met or lapse (unanswered: after two years)."""
        P = self.P; L2 = P["layer_c"][1]
        nn, kk = _nz2(self.wstate > 0)
        if not len(nn):
            return
        st = self.wstate[nn, kk]; wk = self.want[nn, kk].astype(np.int64); c = self.c[nn, kk]
        g = st == 1
        wr = self.wripe[nn, kk] + g * WANT_RATE[np.maximum(wk, 0)] * (0.5 + c) / 52.0
        self.wripe[nn, kk] = wr
        self.wknown[nn[g & (c >= L2) & (wr >= 0.5)], kk[g & (c >= L2) & (wr >= 0.5)]] = True
        due = g & (wr >= 1)
        for n_, k_ in zip(nn[due], kk[due]):
            self.wstate[n_, k_] = 2; self.wdue[n_, k_] = t; self.wknown[n_, k_] = True
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="due", key=CAST_WANTS[int(self.want[n_, k_])],
                                        cid=int(self.uid[n_, k_]), known=True, **self._far_cause(n_, k_, t)))
        d = st == 2
        hk = self.held[nn, KID] if self.held.shape[1] > KID else np.zeros(len(nn), bool)
        met = ((wk == WI["grandchild"]) & hk) | ((wk == WI["home"]) & self._here(nn, kk))
        lapse = ((wk == WI["love"]) & ((self.pslot[nn] >= 0) | self.mpart[nn, kk])) | (d & ((t - self.wdue[nn, kk]) > 104))
        lapse |= ~self.lv[nn, kk]
        if self.far_on:   # far_ties: an unanswered call lapses within weeks; work an event found meets a wish for money
            lapse |= FARW[np.maximum(wk, 0)] & d & ((t - self.wdue[nn, kk]) > self.far_par["lapse"])
            met |= ((wk == WI["money"]) & self.emp[nn, kk] & ((t - self.far_t[nn, kk]) <= 26)
                    & ((self.far_sg[nn, kk] & 1) > 0)) & ~lapse
        for n_, k_, m_, d_ in zip(nn[met | lapse], kk[met | lapse], met[met | lapse], d[met | lapse]):
            if not m_ and d_:
                self.trust[n_, k_] = max(0.0, float(self.trust[n_, k_]) - 0.05)
            if self.watch[n_] and self.lv[n_, k_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="want", state="met" if m_ else "lapsed",
                                        key=CAST_WANTS[int(self.want[n_, k_])], cid=int(self.uid[n_, k_])))
            self.want[n_, k_] = -1; self.wstate[n_, k_] = 0

    def want_due(self, t=None):
        """Wants ripe this week, and those still unanswered every half year after: [(n, cast id, want key)]. The
        engine offers the matching moment with that person in its first who: slot."""
        t = self.t if t is None else t
        nn, kk = _nz2(self.wstate == 2)
        if not len(nn):
            return []
        wd = self.wdue[nn, kk]
        d = ((wd == t) | (((t - wd) % 26 == 0) & (t > wd))) & ~self.dead[nn]
        return [(int(n_), int(self.uid[n_, k_]), CAST_WANTS[int(self.want[n_, k_])]) for n_, k_ in zip(nn[d], kk[d])]

    def resolve_want(self, n, cid, key, accepted, succ=True, t=None):
        """The moment that answered a want: trust and closeness move, a mark is left, a loan becomes a debt."""
        t = self.t if t is None else t
        k = self._slot(n, cid)
        if k < 0:
            return None
        (dc_a, dt_a), (dc_r, dt_r), mk_a, mk_r = WANT_FX[key]
        h = 1.0 if succ else 0.5
        dc, dtr, mk = (dc_a * h, dt_a * h, mk_a) if accepted else (dc_r, dt_r, mk_r)
        if key == "rival" and accepted:   # competing for the place: winning makes an enemy, losing costs trust
            dc, dtr, mk = ((-0.1, -0.1, "made an enemy") if succ else (-0.03, -0.05, None))
            self.rmask[n, k] |= BIT["rival"]
        self.c[n, k] = _uclip(self.c[n, k] + dc, 0, 1); self.trust[n, k] = _uclip(self.trust[n, k] + dtr, 0, 1)
        if mk:
            bad = mk in ("refused someone in need", "made an enemy", "broke your word")
            if bad:
                self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
            else:
                self.mgood[n, k] = min(255, int(self.mgood[n, k]) + 1)
        if accepted and key == "money":
            self.debt[n, k] = min(100, int(self.debt[n, k]) + 1)   # they owe the character
        if accepted and key == "secret":
            self.secret[n, k] = True
        if accepted and key == "forgiveness":
            self.brk[n, k] = NEVER; self.mbad[n, k] = max(0, int(self.mbad[n, k]) - 1)
        if accepted and key == "love":
            self.rmask[n, k] |= BIT["prospect"]
        if accepted and key == "successor":
            self.rmask[n, k] |= BIT["mentor"]
        self.want[n, k] = -1; self.wstate[n, k] = 0; self.wknown[n, k] = False
        ev = dict(n=int(n), t=int(t), kind="want", state="met" if accepted else "refused", key=key, cid=int(cid),
                  worked=bool(succ), mark=mk)
        if self.watch[n]:
            self.events.append(ev)
        return ev

    # ------------------------------------------------------------------ far_ties (item 18): the towns' events and the ties
    def _far_init(self, run_seed):
        """far_ties (chroma-ideas/far-off-events.md): the sides of each town event (sphere_data.FAR, Outer world's
        far_sides.json), the per-slot record of the last event that touched a cast member, and its own random stream."""
        import sphere_data as SD
        N, K = self.N, self.K
        self.far_par = {**FAR_DEFAULT, **dict((getattr(self.W, "p", None) or {}).get("far_par") or {})}
        self.far_ev = np.full((N, K), -1, np.int16)      # the last event that touched them (index into sphere_data.EV)
        self.far_t = np.full((N, K), NEVER, np.int64)    # its week
        self.far_sg = np.zeros((N, K), np.int8)          # its sides that touched them: 1 good, 2 hard, 3 both (mixed)
        self.far_sd = np.full((N, K, 2), -1, np.int16)   # the good and the hard side (index into _far_sides)
        self.far_in = np.full((N, K), FAR_OFF, np.int64)  # taken in (F4): the week their year in the household ends
        self.far_from = np.full((N, K), -1, np.int64)    # ... and the town they came from
        self._far_rng = np.random.default_rng([self.seed, 84, self.run_seed])
        self._far_i = len(getattr(self.W, "sph_ev_log", ()))   # the world's town events already read
        self.far_n = {}                                   # counts for the checks (not saved)
        ek = {f"{e['sphere']}.{e['key']}": i for i, e in enumerate(SD.EV)}
        self._far_sides = []; self._far_tab = {}
        for k, v in SD.FAR.items():
            if k not in ek:
                continue
            ids = []
            for x in v["sides"]:
                bad = [w_ for w_ in x["who"] if w_ not in FAR_WHO and not (w_.startswith("sector:") and w_[7:] in SECTORS)]
                if bad or x["touch"] not in TOUCHES:
                    raise ValueError(f"far side of {k}: unknown who {bad} or touch {x['touch']!r}")
                ids.append(len(self._far_sides))
                self._far_sides.append(dict(x, event=k, far_event=v["far_event"]))
            self._far_tab[ek[k]] = ids

    def _far_count(self, key, m=1):
        self.far_n[key] = self.far_n.get(key, 0) + int(np.sum(m))

    def _far_fit(self, nn, kk, who, age):
        """The cast members (nn, kk) a side reaches: every word of its who list fits their own state (16 and over)."""
        m = age >= 16
        own = self.fbiz[nn, kk] | (self.mcls[nn, kk] >= 2)
        for w_ in who:
            if w_ == "in_work":
                m = m & self.emp[nn, kk]
            elif w_ == "out_of_work":
                m = m & ~self.emp[nn, kk] & (age >= 18) & (age < 65)
            elif w_.startswith("sector:"):
                m = m & self.emp[nn, kk] & (self.sector[nn, kk] == SECTORS.index(w_[7:]))
            elif w_ == "owner":
                m = m & own
            elif w_ == "renter":
                m = m & ~own
            elif w_ == "poor":
                m = m & (self.money[nn, kk] < 0.15)
            elif w_ == "comfortable":
                m = m & (self.money[nn, kk] >= 0.4)
            elif w_ == "young":
                m = m & (age < 30)
            elif w_ == "old":
                m = m & (age >= 65)
            elif w_ == "ill":
                m = m & (self.health[nn, kk] < 0.5)
            elif w_ == "parent":
                m = m & (self.nkids[nn, kk] >= 1)
        return m

    def _far_touch(self, nn, kk, x, good, age):
        """A side's touch on the cast members it reached (far_sides.json touch_effects): work found or lost, money,
        home, health, safety (mood) and standing, up or down."""
        tch = x["touch"]; sg = 1.0 if good else -1.0
        self._far_count(f"{tch} {'good' if good else 'hard'}", len(nn))
        if tch == "work":
            e_ = self.emp[nn, kk]
            if good:
                wa = ~e_ & (age >= 18) & (age < 65)
                a_, b_ = nn[wa], kk[wa]
                sec_ = [w_[7:] for w_ in x["who"] if w_.startswith("sector:")]
                s0_ = SECTORS.index(sec_[0]) if sec_ else SECTORS.index("services")
                self.sector[a_, b_] = np.where(self.sector[a_, b_] < 0, s0_, self.sector[a_, b_])
                self.emp[a_, b_] = True
                self._far_count("found work", wa)
                self.money[nn[e_], kk[e_]] = np.minimum(self.money[nn[e_], kk[e_]] + 0.05, 1)   # better work
            else:
                self.emp[nn[e_], kk[e_]] = False
                self._far_count("lost work", e_)
        elif tch == "money":
            self.money[nn, kk] = np.clip(self.money[nn, kk] + 0.15 * sg, 0.02, 1)
        elif tch == "home":
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.1 * sg, 0, 1)
            if not good:
                self.money[nn, kk] = np.clip(self.money[nn, kk] - 0.1, 0.02, 1)
        elif tch == "health":
            self.health[nn, kk] = np.clip(self.health[nn, kk] + 0.15 * sg, 0.02, 1)
        elif tch == "safety":
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.1 * sg, 0, 1)
        elif tch == "standing":
            self.stand[nn, kk] = np.clip(self.stand[nn, kk].astype(np.int64) + int(sg), 0, 3)
            self.mood[nn, kk] = np.clip(self.mood[nn, kk] + 0.05 * sg, 0, 1)

    def _far_week(self, t):
        """F1 and F2: each town event fired since last week (local ones only; the whole society's reach everyone the
        same way) touches the cast members living in that town by its sides; a touched tie among the ~15 closest living
        in another town calls (a far want, due within weeks, in the want's first who: slot)."""
        log = getattr(self.W, "sph_ev_log", None)
        if log is None or len(log) <= self._far_i:
            return
        rows = np.asarray(log[self._far_i:]).tolist(); self._far_i = len(log)
        fp = self.far_par; L2, L3 = self.P["layer_c"][1], self.P["layer_c"][2]; rng = self._far_rng
        live = self.used & self.lv & ~self.dead[:, None]
        if self._xsoc:
            live &= self.msoc == self.soc.astype(self.msoc.dtype)[:, None]
        for _, i_, l_ in rows:
            ids = self._far_tab.get(int(i_))
            if l_ < 0 or not ids:
                continue
            nn, kk = np.nonzero(live & (self.mloc == l_))
            if not len(nn):
                continue
            age = (t - self.born[nn, kk]) / 52.0
            hit = np.zeros((len(nn), 2), bool); sd = np.full((len(nn), 2), -1)
            for j in ids:
                x = self._far_sides[j]; g = x["sign"] == "good"
                h = self._far_fit(nn, kk, x["who"], age) & (rng.random(len(nn)) < x["share"] * fp["good" if g else "hard"])
                if h.any():
                    self._far_touch(nn[h], kk[h], x, g, age[h])
                    hit[h, 1 - g] = True; sd[h, 1 - g] = j
            a_ = hit.any(1)
            if not a_.any():
                continue
            n2, k2, h2, s2, ag2 = nn[a_], kk[a_], hit[a_], sd[a_], age[a_]
            self.far_ev[n2, k2] = i_; self.far_t[n2, k2] = t
            self.far_sg[n2, k2] = h2[:, 0] + 2 * h2[:, 1]; self.far_sd[n2, k2] = s2
            away = self.mloc[n2, k2] != self.loc[n2]
            mixed = h2.all(1)
            key = np.where(mixed, WI["far_mixed"], np.where(h2[:, 1], WI["far_hard"], WI["far_good"]))
            pc = np.where(mixed, fp["call_mixed"], np.where(h2[:, 1], fp["call_hard"], fp["call_good"]))
            call = (away & (self.c[n2, k2] >= L2) & (self.want[n2, k2] < 0) & (ag2 >= 16) & (rng.random(len(n2)) < pc)
                    & (self._age(t) >= 14))   # (as every want: from the character's 14th year)
            for n_, k_, w_ in zip(n2[call], k2[call], key[call]):
                self.want[n_, k_] = w_; self.wripe[n_, k_] = 0; self.wstate[n_, k_] = 1; self.wknown[n_, k_] = False
                self._far_count(f"call {CAST_WANTS[int(w_)]}")
                if self.watch[n_]:
                    self.events.append(dict(n=int(n_), t=int(t), kind="want", state="begins", key=CAST_WANTS[int(w_)],
                                            cid=int(self.uid[n_, k_]), known=False, **self._far_cause(n_, k_, t)))
            for j_ in np.nonzero(self.watch[n2] & (self.c[n2, k2] >= L3))[0]:   # a close tie's news reaches the story
                n_, k_ = int(n2[j_]), int(k2[j_])
                self.events.append(dict(n=n_, t=int(t), kind="far", cid=int(self.uid[n_, k_]), here=not bool(away[j_]),
                                        **self._far_cause(n_, k_, t)))

    def _far_cause(self, n, k, t):
        """F5: the event that touched cast member (n, k) within far_par cause weeks, for a want or a story line: {} if
        none (and always with far_ties off)."""
        if not self.far_on or t - int(self.far_t[n, k]) > self.far_par["cause"]:
            return {}
        sg = int(self.far_sg[n, k]); sides = [self._far_sides[j] for j in self.far_sd[n, k] if j >= 0]
        return dict(cause=dict(event=sides[0]["event"], far_event=sides[0]["far_event"], town=int(self.mloc[n, k])
                               if self.far_in[n, k] == FAR_OFF else int(self.far_from[n, k]),
                               sign="mixed" if sg == 3 else "good" if sg == 1 else "hard", week=int(self.far_t[n, k]),
                               touch=[x["touch"] for x in sides], line=[x["line"] for x in sides]))

    def far_info(self, n, cid, t=None):
        """What the game names in a far moment: the tie's town (their_town), the event (far_event), what happened to
        them (line) and the touch; None if the cast member has no far event on record."""
        k = self._slot(n, cid)
        if k < 0 or not self.far_on:
            return None
        c_ = self._far_cause(n, k, self.t if t is None else t).get("cause")
        if c_ is None:
            return None
        return dict(c_, their_town=self._loc_info(c_["town"]))

    def far_rel(self, n, k):
        """The who: slots cast member k of life n fits by their relation (far_ties picks the moment by its first)."""
        rm = int(self.rmask[n, k])
        out = [s_ for s_ in WHO_SLOTS if s_ in BIT and s_ != "friend" and (rm & BIT[s_])]
        if (rm & BIT["friend"]) and not (rm & KINMASK):
            out.append("friend")
        if self.pslot[n] == k:
            out.append("partner")
        return out

    def take_in(self, n, cid, t=None):
        """F4, "took them in": the tie moves into the character's town and household for far_par stay weeks; then they
        stay in town or go back, even odds."""
        t = self.t if t is None else t
        k = self._slot(n, cid)
        if k < 0 or not self.far_on or self.far_in[n, k] != FAR_OFF:
            return None
        self.far_from[n, k] = self.mloc[n, k]; self.far_in[n, k] = t + int(self.far_par["stay"])
        self.mloc[n, k] = self.loc[n]; self.msoc[n, k] = self.soc[n]
        if self.hhj[n] >= 0:
            self.mset[n, k] |= self._bit(int(self.hhj[n]))
        self._far_count("taken in")
        ev = dict(n=int(n), t=int(t), kind="taken in", cid=int(cid), until=int(self.far_in[n, k]))
        if self.watch[n]:
            self.events.append(ev)
        return ev

    def _far_month(self, t):
        """F4: a year in the household over, a tie taken in finds a place in town or goes back home."""
        nn, kk = np.nonzero(self.far_in <= t)
        for n_, k_ in zip(nn, kk):
            if self.hhj[n_] >= 0:
                self.mset[n_, k_] &= ~self._bit(int(self.hhj[n_]))
            back = self._far_rng.random() < 0.5 and self.far_from[n_, k_] >= 0
            if back and self.used[n_, k_] and self.lv[n_, k_]:
                self.mloc[n_, k_] = self.far_from[n_, k_]
                for j_ in range(self.M):
                    if np.isin(self.skind[n_, j_], LOCAL_KINDS):
                        self.mset[n_, k_] &= ~self._bit(j_)
            self._far_count("went back" if back else "stayed in town")
            if self.watch[n_] and self.used[n_, k_] and self.lv[n_, k_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="taken in", state="went back" if back else "stayed",
                                        cid=int(self.uid[n_, k_])))
            self.far_in[n_, k_] = FAR_OFF

    # ------------------------------------------------------------------ approval, standing, reach (spec 2 §3, spec 7)
    def _norm_hist(self, t):
        v = np.zeros(NNORM)
        for i_, k_ in enumerate(NORM_KEYS):
            try:
                v[i_] = float(self.W.norm(k_))
            except Exception:
                v[i_] = 0.5
        self.nh.append(v)

    def _approval(self, t):
        """Acceptance per norm key as the character feels it, minus the society's: PP.approval, so that
        W.norm(key) + PP.approval is the acceptance where the character lives and among their own people. The local
        norm is the members' acceptance in the character's groups by time share (older and stricter members lag);
        the close circle (layers 1-2, by closeness^2) weighs in up to circle_w; a close person's strong disapproval of
        an act of the character's (objk) comes off it and fades."""
        P = self.P; N = self.N; L2 = P["layer_c"][1]
        if not self.nh:
            self._norm_hist(t)
        nh = np.array(self.nh); lnh = _logit(nh)
        now = lnh[-1]
        tsw = self.sts * (self.skind >= 0)
        accs = _sig(now[None, None, :] - 1.2 * self.sstrict[..., None])
        tt = tsw.sum(1, keepdims=True)
        self.local_norm = np.where(tt > 0, (tsw[..., None] * accs).sum(1) / np.maximum(tt, 1e-9), nh[-1][None, :])
        fi = self._fi; f32 = np.float32
        cc = np.take(self.c, fi)
        ok = np.take(self.used, fi) & np.take(self.lv, fi) & (cc >= L2)
        qf = _uclip((np.take(self.born, fi).astype(np.int64) + 20 * 52 - self.t0) // 13, 0, len(nh) - 1)
        # each close person's acceptance (N, KC, NNORM; float32, the whole close index, weighted 0 where not close):
        # half the norms now, half those when they were 20, less their strictness, plus a fixed personal view
        z = (0.5 * lnh).astype(f32)[qf]; z += (0.5 * now).astype(f32); z -= f32(1.2) * np.take(self.strict, fi)[..., None]
        z += _EPS6[np.take(self.nm, fi) % len(_EPS6)]
        acc = _sig(z)
        wc = np.where(ok, cc * cc, f32(0)).astype(f32); sw = wc.sum(1)
        circle = np.where(sw[:, None] > 0, np.einsum("nk,nkj->nj", wc, acc) / np.maximum(sw, 1e-9)[:, None], self.local_norm)
        wcl = (P["circle_w"] * sw / (sw + 1.0))[:, None]
        dt = (t - self._last_appr) / 52.0 if self._last_appr is not None else 0.0
        self.objk *= 0.5 ** (dt / P["obj_half"]); self._last_appr = t
        self.approval = _uclip((1 - wcl) * self.local_norm + wcl * circle - self.objk, 0, 1) - nh[-1][None, :]

    def _standing(self, t):
        """Standing per domain and per ring (spec 7 §2: a famous actor has national standing in culture and ordinary
        standing in the economy): money, the standing of the innermost circle (one level below theirs), a wide
        network, rank in groups and movements hold for every domain of their ring; titles count in their own domain
        (S["domain_standing"], one level 0-3 per domain) or, when the engine sends only S["title_standing"], in
        every outer ring (one level, or one per ring). A ring's standing is its best domain's; reach from the table,
        per ring (self.reach) and per domain (self.dreach, what a push uses)."""
        P = self.P; N = self.N; L1 = P["layer_c"][0]
        st = np.zeros((N, 4))
        mon = self.res[:, MON] if self.res.shape[1] > MON else np.full(N, 0.5)
        st[:, 1] = np.maximum(st[:, 1], (mon >= 0.85) + (mon >= 0.95))
        st[:, 3] = np.maximum(st[:, 3], 1.0 * (mon >= 0.95))
        tk = lambda A_: np.take(A_, self._fi)   # the close index (layer 1 is inside it)
        lend = np.where(tk(self.used) & tk(self.lv) & (tk(self.c) >= L1), tk(self.stand).astype(np.int64) - 1, 0).max(1)
        st[:, 1:3] = np.maximum(st[:, 1:3], lend[:, None])
        act = (self.used & self.lv & (self.c >= P["layer_c"][3])).sum(1)
        st[:, 1] = np.maximum(st[:, 1], 1.0 * (act >= P["wide_net"]))
        hi = (self.srank >= 0.8) & (self.scoh >= 0.3) & (self.skind >= 0) & (self.skind != G["household"])
        st[:, 1] = np.maximum(st[:, 1], 1.0 * hi.any(1))
        wk = ((self.skind == G["work"]) & (self.srank >= 0.85)).any(1)
        st[:, 2] = np.maximum(st[:, 2], 1.0 * wk)
        mv = self.skind == G["movement"]
        st[:, 3] = np.maximum(st[:, 3], np.where((mv & (self.srank >= 0.85)).any(1), 2, np.where((mv & (self.srank >= 0.6)).any(1), 1, 0)))
        st[:, 2] = np.maximum(st[:, 2], np.where((mv & (self.srank >= 0.85)).any(1), 2, 0))
        st = _uclip(np.round(st), 0, 3)
        sd = st[:, RING_OF]   # (N, domains): what holds across a whole ring
        ds = getattr(self, "dom_st", None); ts = getattr(self, "title_st", None)
        if ds is not None:
            sd = np.maximum(sd, _uclip(np.round(np.asarray(ds, float).reshape(N, len(DOMAINS))), 0, 3))
        elif ts is not None:
            ts = np.asarray(ts, float); tr = np.zeros((N, 4))
            if ts.ndim == 1:
                tr[:, 1:] = ts[:, None]
            else:
                tr = ts.reshape(N, 4)
            sd = np.maximum(sd, _uclip(np.round(tr), 0, 3)[:, RING_OF])
        for r_ in range(1, 4):
            st[:, r_] = sd[:, RING_OF == r_].max(1)
        st[:, 0] = st[:, 1:].max(1)
        sd[:, RING_OF == 0] = st[:, :1]
        self.standing = st; self.dstanding = sd
        lv = st.astype(np.int64)
        self.reach = np.stack([REACH[lv[:, r_], r_] for r_ in range(4)], 1)
        self.dreach = REACH[sd.astype(np.int64), RING_OF[None, :]]

    def _ties(self):
        lay3 = self.used & self.lv & (self.c >= self.P["layer_c"][2])
        self.ties = 1 - np.exp(-(self.c * lay3).sum(1) / self.P["ties_T"])

    def _felt(self):
        o = self.outlook
        self.felt_reach = _uclip(self.reach + self.P["fr_k"] * (o - 0.45)[:, None] * (1 + self.reach) + self.fr_bias[:, None], 0, 3)

    # ------------------------------------------------------------------ what the engine reads each week
    def _outputs(self, t):
        P = self.P; N = self.N; a = self._age(t)
        if getattr(self, "_cok", None) is not None and self._last_w == t:   # this week's close step
            c = self._cc * self._cok
        else:
            fi = self._fi
            c = np.take(self.c, fi) * (np.take(self.used, fi) & np.take(self.lv, fi) & (np.take(self.uid, fi) == self._cuid))
        c2 = c * c
        wg = c2 * self._caw                                       # the close circle's weight: closeness^2 x role by age
        csum = np.matmul(wg.astype(np.float64)[:, None, :], self._cpie)[:, 0, :]; cw = wg.sum(1)
        tot = self._setw + P["close_w"] * cw
        msc = (self._setmix + P["close_w"] * csum) / np.maximum(tot, 1e-9)[:, None]
        msc = np.where(tot[:, None] > 1e-9, msc, self.w)
        V = _norm(np.asarray(self.W.V, float)); ei = float(self._wf("era_i", 0.0))
        ep = _norm(np.asarray(self._wf("era_p", V), float))
        times = _norm(V + 0.5 * ei * (ep - V))
        b0, pk, at, wd = P["times_w"]
        tw = b0 + pk * np.exp(-((a - at) / wd) ** 2)
        self.niche = _norm((1 - tw) * msc + tw * times[None, :])
        # item 12, the steady current's parts (read only): close people, the places they are inside, the times
        pl_ = (self.places_mix if self.sph_hr and getattr(self, "places_mix", None) is not None else   # phase 2: the
               np.where(self._setw[:, None] > 1e-9, self._setmix / np.maximum(self._setw, 1e-9)[:, None], self.w))   # hours
        self.cur_parts = (np.where(cw[:, None] > 1e-9, csum / np.maximum(cw, 1e-9)[:, None], self.w), pl_,
                          np.broadcast_to(times, (N, C)))
        self._msg_raw = tot
        self.msg_w = _uclip(tot / P["msg_ref"], 0.25, 2.5)
        bs, bc = P["belong_k"]
        self.belong = 1 - np.exp(-(bs * self._belong_set + bc * c2.sum(1)))
        self.help = 1 - np.exp(-(c * self._cav).sum(1) / P["help_H"])
        hard = _uclip(self.stress - 0.5, 0, 1)
        self.support = _uclip(P["sup_k"] * (self.help - P["help_ref"]) * (1 + hard), -0.3, 0.3)
        self._felt()
        ct = P["contagion"]
        self.contagion = dict(divorce=1 + ct[0] * np.exp(-(t - self.cont_t[:, 0]) / 104.0),
                              quit=1 + ct[1] * np.exp(-(t - self.cont_t[:, 1]) / 104.0))

    # ------------------------------------------------------------------ acts, levers and pushes (spec 2 §3, spec 7 §3)
    def on_act(self, idx, ma, succ, visibility=None, lever=None, pushes=None, base=None, target=None, norm=None,
               var=None, t=None, sphere=None, office=None):
        """The character's act this week (vectorised over idx): the close circle judges it (overlap of the act's mix
        with their pies), rank in groups moves, and acts with a lever push (size = base x reach x how well it went;
        a failed push can backfire). Returns dict(approval=(n,), results=[push results])."""
        t = self.t if t is None else t; P = self.P; rng = self.rng; L1, L2, L3, L4 = P["layer_c"]
        idx = np.atleast_1d(np.asarray(idx, np.int64)); E = len(idx)
        if not E:
            return dict(approval=np.zeros(0), results=[])
        ma = _norm(np.asarray(ma, float).reshape(E, C))
        q = _uclip(np.broadcast_to(np.asarray(succ, float), (E,)), 0, 1)
        vis = np.broadcast_to(np.asarray(0.5 if visibility is None else visibility, float), (E,))
        def as_idx(v_, tab):
            if v_ is None:
                return np.full(E, -1, np.int64)
            if isinstance(v_, np.ndarray) and v_.dtype.kind in "iu":
                return np.broadcast_to(v_.astype(np.int64), (E,))
            return np.array([(-1 if x_ is None else tab[x_] if isinstance(x_, str) else int(x_))
                             for x_ in np.broadcast_to(np.asarray(v_, dtype=object), (E,))], np.int64)
        lev = as_idx(lever, LI); dom = as_idx(pushes, DI); nk = as_idx(norm, _NKI)
        bas = np.broadcast_to(np.asarray(1.0 if base is None else base, float), (E,))
        tg = np.broadcast_to(np.asarray(-1 if target is None else target, dtype=object), (E,))
        # 1. the close circle judges what it sees
        ix = slice(None) if E == self.N and (idx == np.arange(E)).all() else idx   # (views when every life acts)
        fi = self._fi[ix]
        if getattr(self, "_cok", None) is not None and self._last_w == t:
            ok = self._cok[ix]; c = self._cc[ix]
        else:
            ok = np.take(self.used, fi) & np.take(self.lv, fi) & (np.take(self.uid, fi) == self._cuid[ix]); c = np.take(self.c, fi)
        f32 = np.float32
        off = np.where(c >= L1, f32(0.0), np.where(c >= L2, f32(0.3), f32(1.0)))
        obs = np.minimum(np.maximum((2 * vis[:, None]).astype(f32) - off, f32(0)), f32(1)) * ok
        ft = C * np.matmul(self._cpie[ix], ma[:, :, None])[..., 0] - 1.0
        wt = obs * c
        appr = (wt * ft).sum(1) / np.maximum(wt.sum(1), 1e-9)
        tr = np.take(self.trust, fi); tr += f32(0.01) * obs * np.minimum(np.maximum(ft, -1.0), 1.0).astype(f32)
        np.minimum(np.maximum(tr, f32(0), out=tr), f32(1), out=tr); np.put(self.trust, fi, tr)
        strong = (ft < -0.6) & (obs > 0) & (c >= L2)
        hasn = nk >= 0
        if hasn.any():
            add = (strong * c ** 2 * 0.5).sum(1)
            np.add.at(self.objk, (_ix(idx[hasn]), _ix(nk[hasn])), add[hasn])
            np.clip(self.objk, 0, 1, out=self.objk)
        # 2. rank in groups: acts that fit the group's ways better than its members do (and work) raise it
        sk = self.skind[ix] >= 0
        fs = C * np.matmul(self.snorm[ix], ma[:, :, None])[..., 0] - 1.0
        vs = _uclip(2 * vis, 0, 1)[:, None] * sk * np.minimum(1, self.sts[ix] * 4)
        d_ = fs - self._fitm[ix]
        dr = P["rank_k"] * vs * np.where(d_ > 0, q[:, None] * d_, d_)
        self.srank[ix] = _uclip(self.srank[ix] + dr, 0, 1)
        # 3. levers
        res = []
        for e_ in np.nonzero((lev >= 0) & (dom >= 0) & ~self.dead[idx])[0]:
            res.append(self._push(int(idx[e_]), ma[e_], float(q[e_]), int(lev[e_]), int(dom[e_]), float(bas[e_]),
                                  tg[e_], None if var is None else (var[e_] if isinstance(var, (list, tuple, np.ndarray)) else var), t))
        # 4. spheres phase 4: the lever on the person's place or town sphere (sph_levers), the act kept for felt fairness
        if (getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False)) and sphere is not None:
            js = np.broadcast_to(np.asarray(sphere, np.int64), (E,))
            ok_ = np.broadcast_to(np.asarray(2 if office is None else office, np.int64), (E,))
            for e_ in np.nonzero((lev >= 0) & (js >= 0) & ~self.dead[idx])[0]:
                r_ = self._sph_lever(int(idx[e_]), int(js[e_]), int(lev[e_]), ma[e_], float(q[e_]), int(ok_[e_]), int(dom[e_]), t)
                if r_ is not None:
                    res.append(r_)
        return dict(approval=appr, results=res)

    def _sph_lever(self, n, j, lev, ma, q, office, dom, t):
        """Phase 4: life n's lever lev in sphere j (Outer world's phase 4 answers). size = the reach for the act's ring
        (dreach, 0 to 3) / 3 x the rung's multiplier (newcomer .125 .. leader 2) x how well it went. It lands on their
        haunt in that sphere; else, working in that sphere (no named work place), on the town sphere at half the size;
        else on the town sphere at a quarter. A voice or loyalty act is kept for felt fairness (+1 went well, -1 not)."""
        lv = LEVERS[lev]
        if self.sph_fr and lv in ("voice", "loyalty"):
            self.fair_log.append([int(t), int(n), int(j), 1 if q >= 0.5 else -1])
        if not self.sph_lv:
            return None
        W = self.W
        rg = int(np.floor(self.rung[n, j])) if hasattr(self, "rung") else 0
        place = -1
        if getattr(self, "sph_h", False) and getattr(W, "hp_s", None) is not None:
            P_ = W.hp_s.shape[2]
            for p_ in self.hnt[n]:
                if p_ >= 0 and HAUNT_SPH[(p_ // P_) % len(HAUNT_KINDS)] == j:
                    place = int(p_); break
        # the reach: on their own place, the settings' ring (a place is a setting's ring, 1); on the town's sphere, the
        # ring of the act's own domain (an institution's, without one)
        reach = float(self.dreach[n, DI["group"] if place >= 0 else (dom if dom >= 0 else DI["institution"])])
        size = reach / 3.0 * float(RUNG_MULT[min(max(rg, 0), 4)]) * q
        if place < 0:
            ss_ = self.set_sphere[n]
            size *= 0.5 if ((self.skind[n] == G["work"]) & (ss_ == j)).any() else 0.25
        span = None
        if self.lw:   # S7: a leader's act in the sphere they lead: the lead lever's size x (.5 + legitimacy), a fund act
            p_ = self._lead_post(n, j)   # lasts what is left of the post (not phase 4's fixed 80 quarters), and the act
            if p_ is not None:            # counts for the way's falls (a failed one, a favour, a success)
                if lv == "lead":
                    size *= 0.5 + p_["legit"]
                if rg >= 4:
                    span = self._lead_left(p_, t)
                self._lead_act(p_, lv, q, t)
        what = W.sph_lever(int(self.loc[n]), j, place, lv, ma, size, rg, self.rng, office=("ban", "licence", "budget")[office],
                           span=span)
        return dict(kind="sphere lever", n=int(n), t=int(t), lever=lv, sphere=SPHERES[j], place=place, size=round(size, 4), reach=reach, went=q,
                    rung=LADDER[min(max(rg, 0), 4)], moved=what)

    def _sph_year4(self, t):
        """Yearly (phase 4): the lives leading a sphere in their town (rung leader) join its leaders' mix (sph_levers;
        World.sph_plead, town x sphere x (colour sums, count)); each life's felt fairness moves .1 of the way toward
        its town's target (World.sph_fair_target) + .1 per voice or loyalty act there in the last 3 years that went
        well, - .1 per one that did not, + .05 x rung (sph_fair)."""
        a = int(self._age(t))
        if a == self._p4_yr:
            return
        self._p4_yr = a; W = self.W; N = self.N
        live = ~self.dead
        if self.sph_lv and hasattr(self, "rung") and not self.lw:   # (lead_ways: the posts join it, each quarter)
            pl = np.zeros((self.n_loc, 9, C + 1))
            n_, j_ = np.nonzero((np.floor(self.rung) >= 4) & live[:, None])
            np.add.at(pl, (self.loc[n_], j_), np.concatenate([self.w[n_], np.ones((len(n_), 1))], 1))
            W.sph_plead = pl if len(n_) else None
        if self.sph_fr and getattr(W, "sph_s", None) is not None:
            self.fair_log = [r_ for r_ in self.fair_log if t - r_[0] <= 3 * 52]
            acts = np.zeros((N, 9))
            for _, n_, j_, v_ in self.fair_log:
                acts[n_, j_] += v_
            rg = np.floor(self.rung) if hasattr(self, "rung") else 0.0
            tgt = _uclip(W.sph_fair_target()[self.loc] + 0.1 * acts + 0.05 * rg, 0, 1)
            self.fair = np.where(live[:, None], self.fair + 0.1 * (tgt - self.fair), self.fair)

    def _push(self, n, ma, q, lev, dom, base, target, var, t):
        P = self.P; rng = self.rng; W = self.W
        lv = LEVERS[lev]; ring = int(RING_OF[dom]); reach = float(self.dreach[n, dom])   # the domain's own reach
        if lv not in P["backfire"]:   # the spheres' levers (found, fund, lead, office) act from phase 4 (item 15)
            return dict(kind="push", n=int(n), t=int(t), lever=lv, domain=DOMAINS[dom], target=None, size="none",
                        backfire=False)
        size = base * reach * q
        bfp = P["backfire"][lv]
        if lv == "voice":
            rights = np.asarray(self._wf("rights", np.ones(5)), float)
            bfp *= 1 + (1 - float(rights[0]))
        elif lv == "subvert":
            bfp *= 1 + float(self._wf("watch", 0.3))
        back = (q < 0.5) and rng.random() < bfp
        tgt_out = None
        if ring == 0:   # the close circle: closeness, trust, their colors
            k = self._slot(n, int(target)) if target is not None and not isinstance(target, str) and int(target) >= 0 else -1
            if k < 0 and isinstance(target, str) and target in BIT:
                cand = np.nonzero(self._has_role(n, target) & self.lv[n])[0]
                k = int(cand[np.argmax(self.c[n, cand])]) if len(cand) else -1
            if k < 0:
                cand = np.nonzero(self.used[n] & self.lv[n])[0]
                k = int(cand[np.argmax(self.c[n, cand])]) if len(cand) else -1
            if k >= 0:
                tgt_out = int(self.uid[n, k]); s_ = size / 3.0
                if lv == "voice":
                    self.trust[n, k] = min(1, self.trust[n, k] + 0.05 * s_)
                    self.pie[n, k] = _norm(self.pie[n, k] + 0.02 * s_ * (ma - self.pie[n, k]))
                    self._psq[n, k] = _csum(self.pie[n, k] ** 2)
                    self.read[n, k] += 0.1 * s_ * (self.pie[n, k] - self.read[n, k])
                elif lv == "loyalty":
                    self.c[n, k] = min(1, self.c[n, k] + 0.05 * s_); self.trust[n, k] = min(1, self.trust[n, k] + 0.05 * s_)
                elif lv == "exit":
                    self.c[n, k] *= (1 - 0.25 * size); self.brk[n, k] = t
                elif lv == "neglect":
                    self.c[n, k] = max(0, self.c[n, k] - 0.03 * size)
                elif lv == "subvert" and q >= 0.5:
                    self.debt[n, k] = min(100, int(self.debt[n, k]) + 1)
                if back:
                    self.trust[n, k] *= 0.85; self.c[n, k] *= 0.9; self.mbad[n, k] = min(255, int(self.mbad[n, k]) + 1)
        elif ring == 1:   # a group (or the neighbourhood): norms, cohesion, rank
            if DOMAINS[dom] == "place":
                js = np.nonzero(self.skind[n] == G["neighbours"])[0]
            elif isinstance(target, str) and target in G:
                js = np.nonzero(self.skind[n] == G[target])[0]
            else:
                js = np.nonzero((self.skind[n] >= 0) & (self.skind[n] != G["household"]))[0]
                js = js[np.argsort(-self.sts[n, js])]
            if len(js):
                j = int(js[0]); tgt_out = GROUP_KINDS[int(self.skind[n, j])]; s_ = size / 3.0
                if lv == "voice":
                    self.snorm[n, j] = _norm(self.snorm[n, j] + 0.03 * s_ * (1 - self.scoh[n, j] / 2) * (ma - self.snorm[n, j]))
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.02 * s_)
                elif lv == "loyalty":
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.03 * s_); self.scoh[n, j] = min(0.98, self.scoh[n, j] + 0.02 * s_)
                elif lv == "exit" and q >= 0.5:
                    self._leave(n, j, t, "exit")
                elif lv == "neglect":
                    self.srank[n, j] = max(0, self.srank[n, j] - 0.03 * size)
                elif lv == "subvert" and q >= 0.5:
                    self.srank[n, j] = min(1, self.srank[n, j] + 0.04 * s_)
                if back:
                    self.srank[n, j] = max(0, self.srank[n, j] - 0.15)
        else:   # institutions and the outer rings: queued in the world (lands next quarter)
            amt = size if reach > 0 else base * q * P["crowd"]   # W.push takes reach units; the world scales them
            tgt_out = DOMAINS[dom] if target is None or isinstance(target, (int, np.integer)) else f"{DOMAINS[dom]} {target}"
            if amt > 0:
                W.push(DOMAINS[dom], self._push_var(n, dom, ma, var), float(amt), int(P["lever_sign"][lv]))
            if back:   # a backfire in an institution or the state: rank at work falls; the engine may add the rest
                js = np.nonzero(self.skind[n] == G["work"])[0]
                if len(js):
                    self.srank[n, js[0]] = max(0, self.srank[n, js[0]] - 0.15)
        seen = 0.0 if back else size
        word = "none" if seen <= 0 or (ring >= 2 and reach <= 0) else "small" if seen < 0.75 else "clear" if seen < 2 else "strong"
        if ring >= 2 and not back:   # institutions and the outer rings: nothing visible yet when it is queued (spec 7 §3);
            word = "unseen"          # what it changes reaches the story later through the world's own record
        # returned only: the engine logs it once, as world_push (not also as a cast event)
        return dict(kind="push", n=int(n), t=int(t), lever=lv, domain=DOMAINS[dom], target=tgt_out, size=word,
                    backfire=bool(back))

    def _push_var(self, n, dom, ma, var):
        """The world variable a push moves when the engine names none: a color-valued domain takes the act's own
        leading color as its direction (spec 7 §4); others their main lever point."""
        if var is not None:
            return str(var)
        d = DOMAINS[dom]
        if d in ("state", "culture"):
            return COLORS[int(np.argmax(ma))]
        if d == "institution":
            js = np.nonzero((self.skind[n] >= 0) & (self.sref[n] >= 0) & np.isin(self.skind[n], [G["work"], G["class"], G["unit"], G["ward"]]))[0]
            return f"legitimacy:{int(self.sref[n, js[0]])}" if len(js) else "legitimacy:0"
        if d == "place":
            return f"efficacy:{int(self.nb[n])}" if self.nb[n] >= 0 else f"crime:{int(self.loc[n])}"
        if d == "belief":
            return f"faith:{int(self.pfaith[n])}" if self.pfaith[n] >= 0 else "secular"
        return dict(economy="inequality", tech="invent", nature="warming", abroad="relation:0").get(d, d)

    # ------------------------------------------------------------------ S7, ways to lead (lead_ways)
    # chroma-ideas/social-mechanics.md S7, "The leader's time in post" first: a post per leading role a life holds (it
    # leads one of its settings, kind "setting", or one held at a named place, "place", or holds an office title,
    # LEAD_TITLES, kind "office"). Each post keeps its start, its way (rules W, knowing best U, favours owed B, inspiring R, custom G)
    # and its legitimacy (the fit of the way's colour to the led place's faces through the place reading, scaled 0..1,
    # less the falls' steps). Its time in post is the Outer world's (dynamics.json lead_posts, by post kind and epoch: a
    # term renewed with chance min(.95, renew x (.5 + legitimacy)) up to max_terms, a yearly end chance, an age out;
    # health under .35 ends it; national offices keep the world's own elections). It also ends at a move, when a rival
    # of higher rung takes over, or by a fall (legitimacy under .2), each told as an event and, where the Library has
    # them, a moment (cast_want lead_take, lead_crisis, lead_fall, lead_routine, lead_hand; fired with no holder, cid -1).
    def _lead_init(self):
        import sphere_data as SD
        wp_ = getattr(self.W, "p", None) or {}
        self.lw_par = {**LEAD_DEFAULT, **dict(wp_.get("lead_par") or {})}
        tb = SD.PLACE_READING
        T = np.array([[float(tb[COLORS[f_]][COLORS[c_]]) for c_ in range(C)] for f_ in range(C)])   # face x act colour
        self._lw_T = T[self.perm][:, self.perm]          # in this world's frame
        LP = SD.LEAD_POSTS
        self._lw_kinds = LP["kinds"]
        self._lw_hk = {h_: k_ for k_, v_ in LP["kinds"].items() for h_ in v_["haunts"]}   # a place's post kind by haunt kind
        self._lw_gk = {g_: k_ for k_, v_ in LP["kinds"].items() for g_ in v_["groups"]}   # a setting's by group kind
        self._lw_fast = np.array([LP["fast_line"][sp_] for sp_ in SPHERES]); self._lw_floss = float(LP["fast_loss"])
        self._lw_hist = []        # the town spheres' face mixes the last five quarters (custom's fast change: 4 quarters)
        self._lw_need = float(SD.DEEP["money"]["need_line"])   # favours: money under the need line
        self.lw_posts = []        # the posts held now: dicts (see _lead_new)
        self.lw_ended = []        # the posts that ended, oldest first
        self.lw_due = []          # [life, moment key, post id, week queued]: a post's moment waiting to come
        self.lw_lost = []         # [life, office index, why]: an office title the engine takes away (a fall, a term)
        self.lw_keys = set()      # the lead moment keys the batch has (WorldLink sets it); none: no moment is waited for
        self.lw_tnames = list(LEAD_TITLES)
        self.lw_has = np.zeros((self.N, len(LEAD_TITLES)), bool)    # the leading titles held (the engine's, each week)
        self.lead_sh = np.zeros((self.N, C))                       # the shadow target years in one way add (with shadows)
        self._lw_next = 0; self._lw_q = -1; self._lw_back = {}
        self._lw_rng = np.random.default_rng([self.seed, 97, self.run_seed])   # the posts' own dice

    def _lead_cell(self, pk):
        """The time in post of post kind pk in this world's epoch (form, term_q, renew, max_terms, end_y, age_out), None
        where the kind has no post then. A national office keeps the world's own elections (no term, no end chance of
        S7's); where there are none, it is held at the ruler's pleasure (end_y .1)."""
        if pk == "national":
            el_ = float(getattr(self.W, "regime", 0.0)) >= 0
            return dict(form="chosen" if el_ else "appointed", term_q=None, renew=None, max_terms=None,
                        end_y=0.0 if el_ else self.lw_par["ruler_end"], age_out=None)
        return self._lw_kinds[pk]["by"].get(getattr(self.W, "sph_epoch", "modern"))

    def _lead_kind(self, n, kind, slot, place):
        """The post kind (lead_posts) of a setting led (by the haunt kind of its place, else its group kind) or an office."""
        if kind == "office":
            return LEAD_TITLES[self.lw_tnames[slot]][0]
        if kind == "place":
            return self._lw_hk.get(HAUNT_KINDS[(int(place) // self.W.hp_s.shape[2]) % len(HAUNT_KINDS)])
        return self._lw_gk.get(GROUP_KINDS[int(self.skind[n, slot])])

    def _lead_left(self, p, t):
        """Quarters left in post (phase 4's fund span for a leader): the term's rest, else the next vote for a national
        office, else the expected time to its yearly end chance; never past the age out; at least 1."""
        c_ = self._lead_cell(p["pk"]) or {}
        if c_.get("term_q"):
            q_ = c_["term_q"] - (t - p["term_t0"]) // 13
        elif p["pk"] == "national" and float(getattr(self.W, "regime", 0.0)) >= 0:
            q_ = int(getattr(self.W, "next_vote", 16))
        else:
            q_ = 4.0 / c_["end_y"] if c_.get("end_y") else 80
        if c_.get("age_out"):
            q_ = min(q_, 4 * (c_["age_out"] - self._age(t)))
        return max(1, int(q_))

    def _lead_renew(self, p, t):
        """A term's end: handed over after max_terms in a row, else renewed with chance min(.95, renew x (.5 +
        legitimacy)), else it ends."""
        c_ = self._lead_cell(p["pk"]) or {}
        p["terms"] += 1
        if c_.get("max_terms") and p["terms"] >= c_["max_terms"]:
            self._lead_end(p, t, "term limit")
        elif self._lw_rng.random() < min(0.95, float(c_.get("renew") or 0.0) * (0.5 + p["legit"])):
            p["term_t0"] = int(t)
            self._lead_ev(p, t, "renewed", terms=p["terms"])
        else:
            self._lead_end(p, t, "term")

    def _lead_faces(self, p):
        """The led place's faces (this world's frame): the named place, the setting's ways, or the town's sphere."""
        W = self.W; n = p["n"]
        if p["kind"] == "office" and p.get("gslot", -1) >= 0:   # a leading title over a setting the life is still in
            g_ = p["gslot"]
            if self.skind[n, g_] >= 0 and int(self.sjoin[n, g_]) == p["gjoin"]:
                if p["place"] >= 0 and getattr(W, "hp_s", None) is not None and int(self.shnt[n, g_]) == p["place"]:
                    return np.asarray(W.hp_s.reshape(-1, C)[p["place"]], float)
                return np.asarray(self.snorm[n, g_], float)
        if p["kind"] == "place" and getattr(W, "hp_s", None) is not None:
            return np.asarray(W.hp_s.reshape(-1, C)[p["place"]], float)
        if p["kind"] in ("place", "setting"):
            return np.asarray(self.snorm[n, p["slot"]], float)
        if getattr(W, "sph_s", None) is not None:
            return np.asarray(W.sph_s[p["loc"], p["sphere"]], float)
        return np.full(C, 1.0 / C)

    def _lead_fit(self, p):
        """The fit of the post's way to the led place: the place's reading of the way's colour (own +1, ally +.4,
        enemy -.4, dynamics.json place_reading), from -.4..1 to 0..1."""
        r = float(self._lead_faces(p) @ self._lw_T[:, int(self.iperm[p["way"]])])
        return (r + 0.4) / 1.4

    def _lead_legit(self, p):
        p["legit"] = float(min(max(self._lead_fit(p) + p["dent"], 0.0), 1.0))
        return p["legit"]

    def _lead_post(self, n, j):
        """Life n's post in sphere j (the most legitimate, when several), else None."""
        best = None
        for p in self.lw_posts:
            if p["n"] == n and p["sphere"] == j and (best is None or p["legit"] > best["legit"]):
                best = p
        return best

    def _lead_ev(self, p, t, state, **kw):
        if self.watch[p["n"]]:
            self.events.append(dict(n=int(p["n"]), t=int(t), kind="lead", state=state, post=p["kind"],
                                    sphere=SPHERES[p["sphere"]], way=LEAD_WAYS[p["way"]], legit=round(p["legit"], 3), **kw))

    def _lead_queue(self, p, key, t):
        """A post's moment waits to come (only when the batch has moments of that key)."""
        if key in self.lw_keys and not any(d_[2] == p["id"] and d_[1] == key for d_ in self.lw_due):
            self.lw_due.append([int(p["n"]), key, int(p["id"]), int(t)])
            return True
        return False

    def _lead_new(self, n, kind, j, slot, place, t, gslot=-1):
        """A post begins: the character picks the way of its lead colour (a lead_take moment can change it). gslot: the
        setting a leading title leads (-1 none)."""
        pk = self._lead_kind(n, kind, slot, place)
        if pk is None or self._lead_cell(pk) is None:   # no such post in this epoch
            return None
        c = int(self.perm[int(np.argmax(self.w[n]))])
        p = dict(id=self._lw_next, n=int(n), kind=kind, pk=pk, terms=0, sphere=int(j), slot=int(slot), place=int(place),
                 loc=int(self.loc[n]), t0=int(t), term_t0=int(t), way=c, col=c, way_t=int(t), succ_t=int(t), fade_t=int(t),
                 fades=0, dent=0.0, legit=0.0, join=int(self.sjoin[n, slot]) if kind != "office" else -1, fair_lo=False,
                 money_yr=-1, falls=[], end_t=None, why=None, gslot=int(gslot),
                 gjoin=int(self.sjoin[n, gslot]) if gslot >= 0 else -1)
        self._lw_next += 1
        self._lead_legit(p)
        self.lw_posts.append(p)
        self._lead_ev(p, t, "took", title=self.lw_tnames[slot] if kind == "office" else None)
        self._lead_queue(p, "lead_take", t)
        return p

    def _lead_end(self, p, t, why):
        """A post ends: a setting's lead goes to its most standing member; an office S7 ended (a fall, a term, a
        hand-over, a move...) is taken from the engine's titles, and a favours leader's other posts lose what the office
        paid for."""
        if p not in self.lw_posts:
            return
        self.lw_posts.remove(p)
        p["end_t"] = int(t); p["why"] = why
        self.lw_ended.append(p)
        self.lw_due = [d_ for d_ in self.lw_due if d_[2] != p["id"]]
        n = p["n"]
        if p["kind"] != "office" and self.slead[n, p["slot"]] == -2 and why != "rival":
            self.slead[n, p["slot"]] = -1   # handed to the most standing member (no dice), else left for the members' turn
            if self.skind[n, p["slot"]] >= 0:
                mem = np.nonzero((self._bits()[n, :, p["slot"]] > 0) & self.lv[n])[0]
                if len(mem):
                    k = int(mem[np.argmax(self.stand[n, mem])])
                    self.slead[n, p["slot"]] = k; self.rmask[n, k] |= LEAD_BIT[int(self.skind[n, p["slot"]])]
        if p["kind"] == "office":
            if why not in ("died", "office ended"):   # S7 ended it: the engine takes the title (a fall, a term, a move)
                self.lw_lost.append([int(n), int(p["slot"]), why])
            if why != "died":   # favours owed: the office that paid them has ended
                for q_ in [q_ for q_ in self.lw_posts if q_["n"] == n and q_["way"] == 2]:
                    self._lead_step(q_, t, "favours", self.lw_par["favours"], why="the office ended")
        self._lead_ev(p, t, "ended", why=why, years=round((t - p["t0"]) / 52.0, 2))

    def _lead_step(self, p, t, key, size, why=None):
        """A fall's step in legitimacy (the falls in numbers); the crisis of the way waits to come (lead_crisis), or the
        turn to routine for a fading inspiring leader; under the fall line, the fall."""
        if p not in self.lw_posts:
            return
        p["dent"] -= size; p["falls"].append([int(t), int(p["way"]), key])
        self._lead_legit(p)
        self._lead_ev(p, t, "step", key=key, why=why, size=size)
        if p["legit"] < self.lw_par["fall"]:
            self._lead_fall(p, t)
        elif key == "inspiring" and p["fades"] >= self.lw_par["routine"] and "lead_routine" in self.lw_keys:
            self._lead_queue(p, "lead_routine", t)
        else:
            self._lead_queue(p, "lead_crisis", t)

    def _lead_fall(self, p, t):
        """Legitimacy under the fall line: the fall moment (go, fight, again), else the post ends."""
        if any(d_[2] == p["id"] and d_[1] == "lead_fall" for d_ in self.lw_due):
            return
        self.lw_due = [d_ for d_ in self.lw_due if d_[2] != p["id"]]   # the fall comes before any crisis
        self._lead_ev(p, t, "falling")
        if not self._lead_queue(p, "lead_fall", t):
            self._lead_end(p, t, "fell")

    def _lead_act(self, p, lv, q, t):
        """A leader's lever act in the sphere they lead (phase 4's levers): a success keeps an inspiring leader's spark
        (no fade for a year); a visible failure is knowing best's mistake; a favour (subvert) touching the leader is a
        rules leader's scandal."""
        if q >= 0.5:
            p["succ_t"] = int(t); p["fades"] = 0
        if p["way"] == 1 and q < 0.5:
            self._lead_step(p, t, "knowing", self.lw_par["knowing"], why="a failed lead act")
        elif p["way"] == 0 and lv == "subvert":
            self._lead_step(p, t, "rules", self.lw_par["rules"], why="a favour")

    def _lead_vacant(self, n, j, k, t):
        """A setting's leader left or died (the members' most standing one, k, would follow): with lead_ways the
        character takes the lead instead when the setting's kind can be led (LEAD_KINDS), they are of age, and they
        stand higher: their rung in the setting's sphere (a regular 1, a known face 2, a pillar 3) above k's (1 +
        standing). True when they took it."""
        if (GROUP_KINDS[int(self.skind[n, j])] not in LEAD_KINDS or self.dead[n] or self._age(t) < self.lw_par["take_age"]
                or not hasattr(self, "rung")):
            return False
        sj = int(self.set_sphere[n, j])
        if sj < 0 or int(np.floor(self.rung[n, sj])) <= 1 + int(self.stand[n, k]):
            return False
        pl_ = int(self.shnt[n, j]) if getattr(self.W, "hp_s", None) is not None else -1
        if self._lead_new(int(n), "place" if pl_ >= 0 else "setting", sj, int(j), pl_, t) is None:
            return False
        self.slead[n, j] = -2
        return True

    def _lead_q(self, t):
        """Each quarter: posts end (death, the office or setting gone, a move, frailty, the age out, the yearly end
        chance, a rival of higher rung, the term's end unrenewed), the legitimacy of the rest and the falls of each way,
        new posts (a pillar takes the lead; an office title), the leaders' mix of each town sphere (World.sph_plead, each
        post x (.5 + legitimacy)) and the shadow target."""
        if self._lw_q == t:
            return
        self._lw_q = t; W = self.W; par = self.lw_par; a = self._age(t)
        if getattr(W, "sph_s", None) is not None:
            self._lw_hist = (self._lw_hist + [np.array(W.sph_s, float)])[-5:]
        # 1. ends
        for p in list(self.lw_posts):
            n = p["n"]; why = None; c_ = self._lead_cell(p["pk"])
            if self.dead[n]:
                why = "died"
            elif p["kind"] == "office" and not self.lw_has[n, p["slot"]]:
                why = "office ended"
            elif p["kind"] != "office" and (self.skind[n, p["slot"]] < 0 or int(self.sjoin[n, p["slot"]]) != p["join"]):
                why = "left"
            elif int(self.loc[n]) != p["loc"]:
                why = "moved"
            elif c_ is None:
                why = "no such post"
            elif float(self.res[n, HEA]) < par["frail"]:
                why = "frail"
            elif c_.get("age_out") and a >= c_["age_out"]:
                why = "retired"
            elif c_.get("end_y") and self._lw_rng.random() < 1 - (1 - c_["end_y"]) ** 0.25:
                why = "stepped down"
            if why:
                self._lead_end(p, t, why)
        # 2. a rival of higher rung: the setting's most standing member (rung 1 + standing) above 4 x legitimacy
        B = None
        for p in [p_ for p_ in self.lw_posts if p_["kind"] != "office"]:
            if self._lw_rng.random() >= par["rival"]:
                continue
            B = self._bits() if B is None else B
            n = p["n"]; mem = np.nonzero((B[n, :, p["slot"]] > 0) & self.lv[n])[0]
            if not len(mem):
                continue
            k = int(mem[np.argmax(self.stand[n, mem])])
            if 1 + int(self.stand[n, k]) > 4 * p["legit"]:
                self._lead_end(p, t, "rival")
                self.slead[n, p["slot"]] = k
                self.rmask[n, k] |= LEAD_BIT[int(self.skind[n, p["slot"]])]
        # 3. legitimacy and the falls of each way
        fair_ = W.sph_fair_target() if self.lw_posts else None
        tv_ = (0.5 * np.abs(self._lw_hist[-1] - self._lw_hist[0]).sum(-1)) if len(self._lw_hist) == 5 else None
        for p in list(self.lw_posts):
            if p not in self.lw_posts:
                continue
            n = p["n"]; l_, j_ = p["loc"], p["sphere"]
            self._lead_legit(p)
            if p["way"] == 0:   # rules: a fairness scandal among the led (their felt fairness falls under the line)
                lo_ = bool(fair_[l_, j_] < par["fair_line"])
                if lo_ and not p["fair_lo"]:
                    self._lead_step(p, t, "rules", par["rules"], why="a fairness scandal")
                p["fair_lo"] = lo_
            elif p["way"] == 2:   # favours: once a year, money under the need line
                if int(a) != p["money_yr"]:
                    p["money_yr"] = int(a)
                    if float(self.res[n, MON]) < self._lw_need and t > p["t0"]:
                        self._lead_step(p, t, "favours", par["favours"], why="money under need")
            elif p["way"] == 3:   # inspiring: a year without a new success fades the spark
                if t - p["succ_t"] >= 52 and t - p["fade_t"] >= 52:
                    p["fade_t"] = int(t); p["fades"] += 1
                    self._lead_step(p, t, "inspiring", par["inspiring"], why="no new success")
            elif p["way"] == 4 and tv_ is not None:   # custom: the town sphere changed fast over the last four quarters
                if tv_[l_, j_] > self._lw_fast[j_]:
                    self._lead_step(p, t, "custom", self._lw_floss, why="fast change")
        # 4. a term's end: handing the post on (lead_hand: chosen, open or stay), else renewed or not
        for p in list(self.lw_posts):
            c_ = self._lead_cell(p["pk"]) or {}
            if p in self.lw_posts and c_.get("term_q") and t - p["term_t0"] >= 13 * c_["term_q"]:
                if not any(d_[2] == p["id"] and d_[1] in ("lead_hand", "lead_fall") for d_ in self.lw_due):
                    if not self._lead_queue(p, "lead_hand", t):
                        self._lead_renew(p, t)
        # 5. new posts: a pillar of a setting with a leader takes the lead (when they stand at least as high as its
        # leader: rung 3 against the leader's 1 + standing), and every office title held is a post
        if a >= par["take_age"]:
            held = {(p["n"], p["kind"] == "office", p["slot"]) for p in self.lw_posts}
            kinds = np.array([G[k_] for k_ in LEAD_KINDS])
            cand = (~self.dead[:, None] & np.isin(self.skind, kinds) & (self.srank >= 0.85) & (self.slead != -2))
            nn, jj = np.nonzero(cand)
            u = self._lw_rng.random(len(nn))
            for n, j_, u_ in zip(nn, jj, u):
                n, j_ = int(n), int(j_)
                if (n, False, j_) in held:
                    continue
                k = int(self.slead[n, j_])
                if k >= 0 and 1 + int(self.stand[n, k]) > 3:
                    continue
                if u_ >= par["take"] * (2.0 if self._lw_back.get((n, j_), NEVER) <= t else 1.0):
                    continue
                pl_ = int(self.shnt[n, j_]) if getattr(self, "shnt", None) is not None and getattr(W, "hp_s", None) is not None else -1
                p = self._lead_new(n, "place" if pl_ >= 0 else "setting", int(self.set_sphere[n, j_]), j_, pl_, t)
                if p is None:
                    continue
                if k >= 0:   # the leader they replace is a member again (unless they lead another of the life's settings)
                    others = (self.slead[n] == k); others[j_] = False
                    if not others.any():
                        self.rmask[n, k] &= ~LEAD_BIT[int(self.skind[n, j_])]
                self.slead[n, j_] = -2
        for n, i_ in zip(*np.nonzero(self.lw_has & ~self.dead[:, None])):
            if (int(n), True, int(i_)) not in {(p["n"], p["kind"] == "office", p["slot"]) for p in self.lw_posts}:
                pk_, sp_, gk_ = LEAD_TITLES[self.lw_tnames[i_]]
                gs_ = np.nonzero(self.skind[n] == G[gk_])[0] if gk_ else []   # the setting it leads, when the life is in one
                j_ = SPHERES.index(sp_); pl_ = -1
                if len(gs_):
                    gs_ = int(gs_[0]); j_ = int(self.set_sphere[n, gs_])
                    if getattr(self, "shnt", None) is not None and getattr(W, "hp_s", None) is not None:
                        pl_ = int(self.shnt[n, gs_])
                self._lead_new(int(n), "office", j_, int(i_), pl_, t, gslot=gs_ if isinstance(gs_, int) else -1)
        # 6. the leaders' mix of each town sphere (the lead lever's size x (.5 + legitimacy)), and the shadow target
        pl = np.zeros((self.n_loc, 9, C + 1))
        self.lead_sh = np.zeros((self.N, C))
        for p in self.lw_posts:
            if self.dead[p["n"]]:
                continue
            wt_ = 0.5 + p["legit"]
            pl[p["loc"], p["sphere"], :C] += wt_ * self.w[p["n"]]; pl[p["loc"], p["sphere"], C] += wt_
            c_ = int(self.iperm[p["way"]])
            self.lead_sh[p["n"], c_] = max(self.lead_sh[p["n"], c_],
                                           par["sh"] * min((t - p["way_t"]) / 52.0 / par["sh_years"], 1.0))
        W.sph_plead = pl if pl[..., C].any() else None

    def lead_due(self, t=None):
        """The posts' moments waiting this week [(life, key, post id)]; those waited for too long lapse (a fall's: the
        post ends, "fell"; a hand-over's: it ends at its term)."""
        t = self.t if t is None else t
        out = []
        for d_ in list(self.lw_due):
            n, key, pid, t0_ = d_
            p = next((p_ for p_ in self.lw_posts if p_["id"] == pid), None)
            if p is None or self.dead[n]:
                self.lw_due.remove(d_); continue
            if t - t0_ > self.lw_par["wait"]:
                self.lw_due.remove(d_)
                if key == "lead_fall":
                    self._lead_end(p, t, "fell")
                elif key == "lead_hand":   # unanswered: they stay on, as the term's renewal decides
                    self._lead_renew(p, t)
                continue
            out.append((int(n), key, int(pid), p["way"]))
        return out

    def lead_resolve(self, n, pid, key, way, fall, hand, succ, idle, t=None):
        """The post's moment came and the character acted: way (an option's lead:, -1 none), fall (go 0, fight 1,
        again 2), hand (chosen 0, open 1, stay 2). take: the post takes the option's way; crisis: an option of the post's
        way holds it, another way shifts the post to it; routine: a rules option moves the inspiring post to rules;
        fall: go ends it, fight keeps it when the act works (legitimacy back to .3) and ends it when not, again stands
        down (the take chance there doubles after a year); hand: chosen or open hands it on, stay leaves it to the
        term's renewal (lead_posts: renew x (.5 + legitimacy), max_terms).
        Returns the event."""
        t = self.t if t is None else t
        p = next((p_ for p_ in self.lw_posts if p_["id"] == int(pid)), None)
        self.lw_due = [d_ for d_ in self.lw_due if not (d_[2] == int(pid) and d_[1] == key)]
        if p is None:
            return None
        way = -1 if idle else int(way); fall = -1 if idle else int(fall); hand = -1 if idle else int(hand)
        ans = None
        def set_way(c_):
            if c_ != p["way"]:
                p["way"] = int(c_); p["way_t"] = int(t); p["succ_t"] = int(t); p["fade_t"] = int(t); p["fades"] = 0
                p["fair_lo"] = False
                self._lead_legit(p)
        if key in ("lead_take", "lead_crisis") and way >= 0:
            ans = "held" if way == p["way"] else "shifted"
            set_way(way)
        elif key == "lead_routine":
            ans = "routine" if way == 0 else "kept"
            if way == 0:
                set_way(0)
        elif key == "lead_fall":
            if fall == 1 and succ:
                ans = "fought"; p["dent"] = self.lw_par["fight"] - self._lead_fit(p); self._lead_legit(p)
            elif fall == 2:
                ans = "stood down"; self._lw_back[(int(n), int(p["slot"]))] = int(t) + int(self.lw_par["again"])
                self._lead_end(p, t, "stood down")
            else:
                ans = "fell"; self._lead_end(p, t, "fell")
        elif key == "lead_hand":
            if hand in (0, 1):
                ans = "handed on"; self._lead_end(p, t, "handed on")
            else:   # stay (or no answer): the term's renewal decides (renewed, a term limit or the term's end)
                ans = "stayed"; self._lead_renew(p, t)
        ev = dict(n=int(n), t=int(t), kind="lead", state="answered", key=key, answer=ans, post=p["kind"],
                  sphere=SPHERES[p["sphere"]], way=LEAD_WAYS[p["way"]], legit=round(p["legit"], 3), worked=bool(succ))
        if self.watch[n]:
            self.events.append(ev)
        return ev

    def lead_info(self, n):
        """Life n's posts for the game: each with its kind, sphere, the led place (its name in the world's epoch, or the
        setting kind or the office), the way (rules .. custom), legitimacy, start and end (age), the end's reason and
        its falls; the posts held now first, then the ended ones."""
        out = []
        for p in [p_ for p_ in self.lw_posts if p_["n"] == n] + [p_ for p_ in self.lw_ended if p_["n"] == n]:
            if p["place"] >= 0 and getattr(self.W, "place_info", None) is not None:   # a named place: its name and kind
                where = dict(self.W.place_info(int(p["place"])))
            else:
                where = {}
            if p["kind"] == "office":
                where["title"] = self.lw_tnames[p["slot"]]
            sl_ = p["slot"] if p["kind"] != "office" else p.get("gslot", -1)
            if sl_ >= 0 and self.skind[n, sl_] >= 0:
                where["setting"] = GROUP_KINDS[int(self.skind[n, sl_])]
            if not where:
                where["sphere"] = SPHERES[p["sphere"]]   # the town's sphere
            out.append(dict(id=p["id"], kind=p["kind"], sphere=SPHERES[p["sphere"]], place=where, way=LEAD_WAYS[p["way"]],
                            colour=COLORS[p["col"]], legit=round(p["legit"], 3), start=round((p["t0"] - self.t0) / 52.0, 2),
                            end=None if p["end_t"] is None else round((p["end_t"] - self.t0) / 52.0, 2), why=p["why"],
                            post_kind=p["pk"], terms=p["terms"],
                            falls=[dict(age=round((f_[0] - self.t0) / 52.0, 2), way=LEAD_WAYS[f_[1]], key=f_[2]) for f_ in p["falls"]]))
        return out

    # ------------------------------------------------------------------ who: slots (world-fields.md)
    def fill(self, n, slots, at=None, t=None):
        """{slot: cast id} for a moment's who: slots, from the cast by role and closeness, else a new face (never
        blocks). at: an institution kind for the slot "at" (the person who stands for it there)."""
        t = self.t if t is None else t; rng = self.rng; a = self._age(t)
        taken = set(); out = {}
        u = self.used[n] & self.lv[n]
        age = (t - self.born[n]) / 52.0
        for s_ in ([slots] if isinstance(slots, str) else list(slots)) + (["at"] if at is not None else []):
            if s_ == "dead":
                cand = np.nonzero(self.used[n] & ~self.lv[n] & (self.cmax[n] >= self.P["layer_c"][3]))[0]
                score = self.cmax[n, cand] - (t - self.died_t[n, cand]) / 5200.0
            elif s_ == "partner":
                cand = np.array([self.pslot[n]]) if self.pslot[n] >= 0 and self.lv[n, self.pslot[n]] else np.zeros(0, np.int64)
                score = np.ones(len(cand))
            elif s_ == "elder":
                cand = np.nonzero(u & (((self.rmask[n] & BIT["elder"]) != 0) | ((age >= 60) & (age >= a + 20))))[0]
                score = self.c[n, cand] + 0.5 * ((self.rmask[n, cand] & BIT["elder"]) != 0)
            elif s_ == "friend":
                cand = np.nonzero(u & ((self.rmask[n] & BIT["friend"]) != 0) & ((self.rmask[n] & KINMASK) == 0))[0]
                score = self.c[n, cand]
            elif s_ == "at":
                cand = np.zeros(0, np.int64); score = cand
            elif s_ in BIT:
                cand = np.nonzero(u & ((self.rmask[n] & BIT[s_]) != 0))[0]
                score = self.c[n, cand] + 0.3 * self.inci[n, cand]
                if s_ in ("boss", "colleague", "teacher"):
                    j_ = np.nonzero(self.skind[n] == G["work" if s_ != "teacher" else "class"])[0]
                    if len(j_):
                        score = score + 1.0 * (((self.mset[n, cand] >> j_[0]) & 1) > 0)
            else:
                cand = np.zeros(0, np.int64); score = cand
            keep = np.array([k_ not in taken for k_ in cand], bool) if len(cand) else np.zeros(0, bool)
            cand, score = cand[keep], np.asarray(score)[keep]
            if len(cand):
                k = int(cand[np.argmax(score)])
            else:
                k = self._face(n, s_, t, at)
            if k >= 0:
                taken.add(k); out[s_] = int(self.uid[n, k])
        return out

    def _face(self, n, slot, t, at=None):
        """A new person for a slot no cast member fits: drawn from the locality, layer 4, dropped unless a tie forms."""
        rng = self.rng; a = self._age(t)
        off = dict(parent=28, grandparent=55, elder=40, child=-28, teacher=20, boss=15, mentor=15).get(slot, 0)
        ag = max(1.0, a + off + rng.normal(0, 5))
        F = self._gen(np.array([n]), np.array([t - int(ag * 52)]), t)
        # a face never takes a core or family role: a partner slot gets a date, a family slot a distant relative
        role = (R["prospect"] if slot == "partner" else R["kin"] if slot in ("parent", "child", "sibling", "grandparent")
                else R[slot] if slot in R and slot not in ("dead", "at") else R["acquaintance"])
        if slot == "prospect":
            same = rng.random() < self.P["same_sex"][int(_uclip(self.attr[n], 0, 4))]
            F["fem"] = np.array([bool(self.female[n]) == bool(same)])
        if slot in ("boss", "teacher", "mentor", "elder", "at"):
            F["stand"] = np.array([1])
        sl = self._add(F, t, role, c0=0.05, trust0=0.45, face=True, alive=slot != "dead", quiet=True)
        if not len(sl):
            return -1
        k = int(sl[0])
        if slot == "at" and at is not None:
            self.inst[n, k] = self._inst_pick(n, at) if at in INST_KINDS else -1
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="face", cid=int(self.uid[n, k]), role=slot))
        return k

    # ------------------------------------------------------------------ place and moving (spec 3 §2.6)
    def move_wish(self, t=None, S=None):
        """Weekly chance of moving (all moves, local and away): by age, peaking in the twenties (about 8-9% a year
        overall, US Census), higher after a partnership starts or ends. The engine scales its moving moments by it."""
        t = self.t if t is None else t; a = self._age(t); P = self.P
        r = np.interp(a, [a_ for a_, _ in P["move_age"]], [r_ for _, r_ in P["move_age"]])
        pc = np.exp(-(t - self.par_change) / 26.0)
        un = float(self._unemp("unemp"))
        ul = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, un)), float)[self.loc]
        r = r * (1 + 1.5 * pc) * _uclip(1 + 3 * (ul - un), 0.7, 1.5)
        r = np.full(self.N, r / 52.0) if np.ndim(r) == 0 else r / 52.0
        if getattr(self, "roots", None) is not None:   # phase 5: roots, the move wish x .5 while a holding is held
            r = r * np.where(self.roots, 0.5, 1.0)
        return r

    def kin_let_down(self, n, by, t):
        """Phase 5, a kin debt broken: trust falls by `by` with the closest living parent or sibling, who remembers."""
        u = self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["parent"] | BIT["sibling"])) != 0)
        if u.any():
            k = int(np.argmax(np.where(u, self.c[n], -1)))
            self.trust[n, k] = max(0.0, float(self.trust[n, k]) - by)

    def move(self, n, loc=None, why=None, t=None, local=None):
        """The household moves: to loc (another locality), or within the locality (a new neighbourhood). Distant
        ties fade faster (W.comm slows that); the local groups, their rank and the neighbourhood circle are lost.
        why: 'left home' (a home of one's own), 'came home' (back to the parents' place), or None."""
        t = self.t if t is None else t; rng = self.rng; P = self.P; a = self._age(t)
        if why == "left home" and not self.own_home[n]:
            self._leave_home(n, t)
        if why == "came home":
            ps = np.nonzero(self._has_role(n, "parent") & self.lv[n] & (self.msoc[n] == self.soc[n]))[0]
            loc = int(min(self.mloc[n, ps[0]], self.n_loc - 1)) if len(ps) else loc
        if local is None:
            local = loc is None and rng.random() >= P["far_share"] * (1.3 if 18 <= a < 30 else 1.0)
        old = int(self.loc[n])
        if not local:
            if loc is None:
                wt = self._move_wt(n, a)
                loc = int(rng.choice(self.n_loc, p=wt / wt.sum())) if wt.sum() > 0 else old
            self.loc[n] = int(loc)
            for j_ in range(self.M):   # local groups are lost (online ones stay; the household moves)
                if self.skind[n, j_] in LOCAL_KINDS:
                    self._leave(n, j_, t, "moved")
            hh = self.hhj[n]
            if hh >= 0:   # the household moves along: the partner, the children at home (a child: parents, siblings)
                mates = np.nonzero(((self.mset[n] >> hh) & 1) > 0)[0]
                self.mloc[n, mates] = loc; self.msoc[n, mates] = self.soc[n]
        else:
            js = np.nonzero(self.skind[n] == G["neighbours"])[0]
            for j_ in js:
                self._leave(n, int(j_), t, "moved")
        self._pick_nb([n])
        self.n_moves[n] += 1; self.last_move[n] = t
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="moved", loc=int(self.loc[n]), nb=int(self.nb[n]),
                                    away=not local, why=why))

    def _move_wt(self, n, a):
        """Weights of the other localities for a move away: population, young adults toward cities, universities
        and the capital, work (lower unemployment), the old toward their children and parents."""
        wt = self.loc_p.copy()
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        if feat.shape[1] == len(FEATURES) and 18 <= a < 30:
            wt = wt * (1 + 1.0 * feat[:, [FEATURES.index("capital"), FEATURES.index("university"), FEATURES.index("city")]].any(1))
        un = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, 0.05)), float)
        wt = wt * np.exp(-8 * (un - un.mean()))
        kin_l = self.mloc[n, self.used[n] & self.lv[n] & ((self.rmask[n] & (BIT["child"] | BIT["parent"])) != 0)
                          & (self.msoc[n] == self.soc[n])]
        kin_l = kin_l[kin_l < self.n_loc]
        if a >= 60 and len(kin_l):
            wt[kin_l] *= 3
        wt[int(self.loc[n])] = 0
        return wt

    def move_options(self, n, k=3, t=None):
        """Up to k candidate localities for a move away, drawn by the weights move() uses (a stream of their own, so
        asking changes nothing): [dict(loc, kind, size, features)], size 0-3 (village, town, city, metropolis)."""
        t = self.t if t is None else int(t); n = int(n)
        wt = self._move_wt(n, self._age(t))
        cand = np.nonzero(wt > 0)[0]
        if not len(cand):
            return []
        r_ = np.random.default_rng([self.seed, 37, self.run_seed, n, max(int(t), 0)])
        key = np.log(wt[cand]) + r_.gumbel(size=len(cand))   # weighted draws without replacement (Gumbel top-k)
        return [self._loc_info(int(l_)) for l_ in cand[np.argsort(-key, kind="stable")[:int(k)]]]

    def _loc_info(self, l):
        kk = self._wf("loc_kind_key", None)
        kind = kk[l] if kk is not None else np.asarray(self._wf("loc_kind", np.zeros(self.n_loc)))[l]
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        fl = [FEATURES[i_] for i_ in np.nonzero(feat[l])[0]] if feat.shape[1] == len(FEATURES) else []
        sz = np.asarray(self._wf("loc_size", np.zeros(self.n_loc, np.int64)))
        return dict(loc=int(l), kind=kind.item() if hasattr(kind, "item") else kind,
                    size=int(sz[l]) if len(sz) > l else 0, features=fl)

    # ------------------------------------------------------------------ other societies: emigration (spec 5 §5)
    def emigrate(self, n, W_new=None, society_id=None, t=None, with_partner=True):
        """Life n emigrates to another society (spec 5 §5; Emren 10:30 "Yes, fully"); returns the new locality.

        With one life (N == 1) the People switch their world to W_new, the neighbour at full detail
        (World.spawn_neighbour(k)), and keep the old World to go back to. With several lives sharing one World
        (N > 1) there is no second world to switch to: only the bookkeeping is done (society id, status, language,
        far ties, the settings left, the class), and the life stays on the shared World's places, rates and
        institutions, which stand in for the new country.

        The life arrives as a migrant: a locality drawn toward cities and work, the family's class one step lower at
        first, a new neighbourhood; every setting is left but online groups (and the household when the partner and
        children come along, with_partner; a child's whole household comes); a few people from the old country are
        met there; a language to learn (lang, from lang0); joining settings and institutions is harder at first
        (openness to migrants, _mig_gate). Everyone left behind stays in the cast as a far contact and fades by the
        distance rules. The engine changes the status (set_status) and adds to the language (lang_boost)."""
        t = self.t if t is None else int(t); P = self.P; rng = self.rng; n = int(n); a = self._age(t)
        sid = society_id if society_id is not None else getattr(W_new, "society_id", None)
        old = int(self.soc[n])
        sid = old + 1 if sid is None else int(sid)
        if sid == old:
            return int(self.loc[n])
        if sid == int(self.soc_home[n]):
            return self.return_home(n, W_new, t, with_partner)
        self._xsoc = True
        self._smem[(n, old)] = (float(self.lang[n]), int(self.stat[n]))
        if old == int(self.soc_home[n]):
            self.loc_home[n] = self.loc[n]; self.cls_home[n] = self.cls[n]
        mates, hh = self._coming(n, a, t, with_partner)
        self._leave_all(n, hh, t, "emigrated")
        # people from the old country met there (drawn from the old society, before the switch)
        nd = int(rng.integers(2, 6))
        ages = _uclip(max(a, 25.0) + rng.normal(0, 8, nd), 1, 90)
        Fd = self._gen(np.full(nd, n), t - (ages * 52).astype(np.int64), t, ctx=np.tile(self.w[n], (nd, 1)), sel=0.2)
        if self.N == 1 and W_new is not None and W_new is not self.W:   # the neighbour at full detail
            self._Ws[old] = self.W
            self._switch(W_new)
        loc = self._arrival_loc()
        self.soc[n] = sid; self.loc[n] = loc; self.arr_t[n] = t
        self.lang[n], self.stat[n] = self._smem.get((n, sid), (float(P["lang0"]), STATUS.index("migrant")))
        self.cls[n] = max(0, int(self.cls_home[n]) - 1)
        self._pick_nb([n])
        self._settle(n, mates, hh, t, a)
        Fd["mloc"] = np.full(nd, loc); Fd["msoc"] = np.full(nd, sid)
        self._add(Fd, t, R["acquaintance"], c0=0.08 + 0.06 * rng.random(nd), trust0=0.55, quiet=True)
        self._arrived(n, t, "emigrated")
        return loc

    def return_home(self, n, W_home=None, t=None, with_partner=True):
        """Life n goes back to the society it was born in (spec 5 §5: return is possible), undoing emigrate(): the
        home World again (N == 1: W_home, or the one kept when leaving), near the parents if they live there, else
        the old locality; citizen, native language, the family's class at least; settings left as on leaving (online
        groups stay; the household comes when the partner and children do); the people at home are near again.
        With N > 1, as for emigrate(), only the bookkeeping. Returns the locality."""
        t = self.t if t is None else int(t); n = int(n); a = self._age(t)
        home = int(self.soc_home[n]); cur = int(self.soc[n])
        if cur == home:
            return int(self.loc[n])
        self._smem[(n, cur)] = (float(self.lang[n]), int(self.stat[n]))
        mates, hh = self._coming(n, a, t, with_partner)
        self._leave_all(n, hh, t, "returned")
        if self.N == 1:
            Wh = W_home if W_home is not None else self._Ws.get(home)
            if Wh is not None and Wh is not self.W:
                self._Ws[cur] = self.W
                self._switch(Wh)
        ps = np.nonzero(self._has_role(n, "parent") & self.lv[n] & (self.msoc[n] == home))[0]
        loc = int(self.mloc[n, ps[0]]) if len(ps) else int(self.loc_home[n])
        loc = int(_uclip(loc, 0, self.n_loc - 1))
        self.soc[n] = home; self.loc[n] = loc; self.arr_t[n] = t
        self.lang[n] = 1.0; self.stat[n] = STATUS.index("citizen")
        self.cls[n] = max(int(self.cls[n]), int(self.cls_home[n]))
        self._pick_nb([n])
        self._settle(n, mates, hh, t, a)
        self._arrived(n, t, "returned")
        return loc

    def set_status(self, n, status):
        """The engine sets life n's status in the society it lives in: "citizen", "migrant" or "resident"."""
        self.stat[int(n)] = STATUS.index(status) if isinstance(status, str) else int(status)

    def lang_boost(self, n, x):
        """The engine adds to life n's language skill (a course, a partner from there): x of what is left to learn."""
        n = int(n); l_ = float(self.lang[n]); l_ += float(_uclip(x, 0, 1)) * (1 - l_)
        self.lang[n] = 1.0 if l_ > 0.995 else l_

    def _lang_step(self, t):
        """Monthly, for lives abroad: language skill grows by exposure (time in settings outside the home), fastest
        in childhood (lang_k); the family's class comes back once the language is good (0.8) and four years have
        passed since arrival. No draws."""
        P = self.P
        ab = np.nonzero(self.lang < 1)[0]
        if len(ab):
            k = float(np.interp(self._age(t), [x_ for x_, _ in P["lang_k"]], [y_ for _, y_ in P["lang_k"]]))
            sk = self.skind[ab]
            es = (self.sts[ab] * ((sk >= 0) & (sk != G["household"]) & (sk != G["online"]))).sum(1)
            ex = 0.3 + 0.7 * np.minimum(1.0, es / 0.35)
            l2 = 1 - (1 - self.lang[ab]) * np.exp(-k * ex * 4 / 52.0)
            self.lang[ab] = np.where(l2 > 0.995, 1.0, l2)
        back = (self.soc != self.soc_home) & (self.cls < self.cls_home) & (self.lang >= 0.8) & (t - self.arr_t >= 4 * 52)
        self.cls[back] = self.cls_home[back]

    def _coming(self, n, a, t, with_partner):
        """Who moves country with life n: a child's whole household; an adult's household when it is their own and
        the partner comes; else the partner and the children under 18 (with_partner). Returns (slots, household kept
        or -1)."""
        hh = int(self.hhj[n])
        if hh >= 0 and (a < 18 or (self.own_home[n] and with_partner)):
            return np.nonzero(self.used[n] & self.lv[n] & (((self.mset[n] >> hh) & 1) > 0))[0], hh
        ks = []
        if with_partner:
            ps = int(self.pslot[n])
            if ps >= 0 and self.lv[n, ps]:
                ks.append(ps)
            ks += np.nonzero(self.used[n] & self.lv[n] & ((self.rmask[n] & BIT["child"]) != 0)
                             & ((t - self.born[n]) < 18 * 52))[0].tolist()
        return np.array(sorted(set(ks)), np.int64), -1

    def _leave_all(self, n, keep, t, why):
        for j_ in range(self.M):
            if self.skind[n, j_] >= 0 and self.skind[n, j_] != G["online"] and j_ != keep:
                self._leave(n, j_, t, why)

    def _switch(self, W):
        """N == 1: the People now live in World W (its places, rates, institutions, generations)."""
        self.W = W; self._coh_tab = None
        self._world_static()

    def _arrival_loc(self):
        """A migrant's first locality: population, cities and the capital (where migrants mostly settle), work."""
        wt = self.loc_p.copy()
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        if feat.shape[1] == len(FEATURES):
            wt = wt * (1 + 2.0 * feat[:, [FEATURES.index("capital"), FEATURES.index("city")]].any(1))
        un = np.asarray(self._unemp("unemp_loc", np.full(self.n_loc, 0.05)), float)
        wt = wt * np.exp(-8 * (un - un.mean()))
        return int(self.rng.choice(self.n_loc, p=wt / wt.sum()))

    def _settle(self, n, mates, hh, t, a):
        """Those who came along live where life n lives now; a household of their own when the old one was left."""
        self.mloc[n, mates] = self.loc[n]; self.msoc[n, mates] = self.soc[n]
        if hh < 0 and self.hhj[n] < 0 and (a >= 18 or len(mates)):
            j = self._new_setting(n, "household", t)
            self.hhj[n] = j; self.own_home[n] = a >= 18
            if j >= 0:
                self.sanch[n, j] = self.w[n]; self.snorm[n, j] = self.w[n]
                self.mset[n, mates] |= self._bit(j)

    def _arrived(self, n, t, why):
        self.n_moves[n] += 1; self.last_move[n] = t
        if self.watch[n]:
            self.events.append(dict(n=int(n), t=int(t), kind="moved", loc=int(self.loc[n]), nb=int(self.nb[n]),
                                    away=True, why=why, society=int(self.soc[n])))
        self._fsh(); self._close_index(); self._alive_counts([n]); self._outputs_settings()

    # ------------------------------------------------------------------ views for the game
    def _kin_links(self, n):
        """Partners and children among life n's cast, by slot: ({slot: partner's cast id or "you"}, {slot: [children's
        cast ids, "you" for the character]}), from the roles, family lines and kof links."""
        u = np.nonzero(self.used[n])[0]
        uid = self.uid[n]; rm = self.rmask[n]; kof = self.kof[n]; born = self.born[n]
        by = {int(uid[k]): int(k) for k in u}
        has = lambda k, r_: bool(int(rm[k]) & BIT[r_])
        par = [int(k) for k in u if has(k, "parent")]
        sib = [int(k) for k in u if has(k, "sibling")]
        kids = [int(k) for k in u if has(k, "child")]
        gps = [int(k) for k in u if has(k, "grandparent")]
        pa, ch = {}, {}
        ps = int(self.pslot[n])
        if ps >= 0 and self.used[n, ps]:
            pa[ps] = "you"
            ch[ps] = [int(uid[k]) for k in kids if int(kof[k]) == int(uid[ps])]
        if len(par) == 2 and not self.par_apart[n]:
            pa[par[0]] = int(uid[par[1]]); pa[par[1]] = int(uid[par[0]])
        for k in par:
            ch[k] = [int(uid[s_]) for s_ in sib] + ["you"]
        for i_, k in enumerate(gps):
            for k2 in gps[i_ + 1:]:
                if self.line[n, k] == self.line[n, k2] and self.fem[n, k] != self.fem[n, k2]:
                    pa.setdefault(k, int(uid[k2])); pa.setdefault(k2, int(uid[k]))
            mine = [p_ for p_ in par if self.line[n, p_] == self.line[n, k]]
            ch[k] = [int(uid[p_]) for p_ in mine] + [int(uid[m_]) for m_ in u if has(m_, "kin") and
                                                       any(int(kof[m_]) == int(uid[p_]) for p_ in mine)]
        # the rest through kof (kin of): someone 15 to 60 years younger is their child; kin about their age, their
        # partner (the partner's own family and friends are kin of the partner, not counted here)
        for m_ in u:
            x_ = by.get(int(kof[m_]))
            if x_ is None or x_ == ps or x_ in par:
                continue
            gap = (int(born[m_]) - int(born[x_])) / 52.0
            if 15 <= gap <= 60:
                ch.setdefault(x_, []).append(int(uid[m_]))
            elif abs(gap) < 15 and has(m_, "kin") and has(x_, "kin"):
                pa.setdefault(int(m_), int(uid[x_])); pa.setdefault(x_, int(uid[m_]))
        return pa, ch

    def cast_view(self, n, t=None, layers=(1, 2, 3, 4), dead=False):
        """The people around life n, closest first: their reading (never the true pie), closeness and trust (the game
        writes the words), their want when the character knows it, weeks since they last met (last_contact, None if
        never), where they live (loc, society), their partner's and children's cast ids ("you" for the character;
        None or [] when not in the cast)."""
        t = self.t if t is None else t; L = self.P["layer_c"]
        out = []
        pa, ch = self._kin_links(n)
        idx = np.nonzero(self.used[n] & (self.lv[n] | dead))[0]
        for k in idx[np.argsort(-self.c[n, idx])]:
            c = float(self.c[n, k])
            layer = 1 if c >= L[0] else 2 if c >= L[1] else 3 if c >= L[2] else 4 if c >= L[3] else 0
            if layer not in layers and not (dead and not self.lv[n, k]):
                continue
            rm = int(self.rmask[n, k])
            out.append(dict(id=int(self.uid[n, k]), name_idx=int(self.nm[n, k]), line=int(self.line[n, k]),
                            sex="female" if self.fem[n, k] else "male",
                            age=int(((t if self.lv[n, k] else self.died_t[n, k]) - self.born[n, k]) // 52),
                            alive=bool(self.lv[n, k]), role=self._rname(n, k), roles=[r_ for r_ in ROLE_ORDER if rm & BIT[r_]],
                            layer=layer, closeness=round(c, 2), trust=round(float(self.trust[n, k]), 2),
                            read=[round(float(x_), 3) for x_ in self.read[n, k]],
                            want=CAST_WANTS[int(self.want[n, k])] if self.want[n, k] >= 0 and self.wknown[n, k] else None,
                            standing=int(self.stand[n, k]), here=bool(self._here(n, k)),
                            owes=int(self.debt[n, k]), face=bool(self.face[n, k]),
                            last_contact=None if self.last[n, k] <= NEVER // 2 else int(t - self.last[n, k]),
                            loc=int(self.mloc[n, k]), society=int(self.msoc[n, k]),
                            partner=pa.get(int(k)), children=list(ch.get(int(k), []))))
        return out

    def place_view(self, n):
        W = self.W; l = int(self.loc[n])
        kk = self._wf("loc_kind_key", None)
        kind = kk[l] if kk is not None else np.asarray(self._wf("loc_kind", np.zeros(self.n_loc)))[l]
        feat = np.asarray(self._wf("loc_feat", np.zeros((self.n_loc, len(FEATURES)), bool)), bool)
        fl = [FEATURES[i_] for i_ in np.nonzero(feat[l])[0]] if feat.shape[1] == len(FEATURES) else []
        return dict(loc=l, nb=int(self.nb[n]), kind=kind.item() if hasattr(kind, "item") else kind, features=fl,
                    cls=int(self.cls[n]), own_home=bool(self.own_home[n]), moves=int(self.n_moves[n]),
                    society=int(self.soc[n]), home_society=int(self.soc_home[n]), status=STATUS[int(self.stat[n])],
                    lang=round(float(self.lang[n]), 2))

    def figure_view(self, n, W=None):
        """The public figures in role (World W, default the People's): id, role (index; role_name when the world
        names them), party, standing, and their colors as life n reads them (spec 5 §6: only the character's reading,
        never the true pie): half what they show, the character's lens and a fixed personal slant."""
        W = self.W if W is None else W
        try:
            role = np.asarray(W.fig_role, np.int64); pie = np.asarray(W.fig_pie, float).reshape(-1, C)
            stn = np.asarray(W.fig_standing, float); alive = np.asarray(W.fig_alive, bool)
        except AttributeError:
            return []
        act = np.asarray(getattr(W, "fig_active", alive), bool)
        party = getattr(W, "fig_party", None); party = None if party is None else np.asarray(party, np.int64)
        names = getattr(sys.modules.get(type(W).__module__), "FIG_ROLES", None)
        out = []
        for f_ in np.nonzero(alive & act)[0].tolist():
            x_ = np.sin((f_ + 1) * 12.9898 + np.arange(C) * 78.233 + n * 0.618034 + self.run_seed * 0.414214) * 43758.5453
            sl_ = _norm((x_ - np.floor(x_) + 0.2)[self.perm])   # drawn in the canonical color frame, then relabelled
            rd = _norm(0.5 * pie[f_] + 0.3 * self.lens[n] + 0.2 * sl_)
            out.append(dict(id=int(f_), role=int(role[f_]),
                            role_name=names[int(role[f_])] if names is not None and 0 <= role[f_] < len(names) else None,
                            party=int(party[f_]) if party is not None and f_ < len(party) else -1,
                            standing=round(float(stn[f_]), 2), read=[round(float(v_), 3) for v_ in rd]))
        return out

    def settings_view(self, n):
        """The character's groups: kind, time share, cohesion, rank, members and leader, and their ways as the
        character reads them (the members' reading blended with what the group openly praises)."""
        out = []
        for j in np.nonzero(self.skind[n] >= 0)[0]:
            mem = np.nonzero(((self.mset[n] >> j) & 1).astype(bool) & self.used[n] & self.lv[n])[0]
            seen = _norm(0.5 * self.snorm[n, j] + 0.5 * (self.read[n, mem].mean(0) if len(mem) else self.snorm[n, j]))
            ld = int(self.slead[n, j])
            out.append(dict(j=int(j), kind=GROUP_KINDS[int(self.skind[n, j])], time_share=round(float(self.sts[n, j]), 3),
                            cohesion=round(float(self.scoh[n, j]), 2), rank=round(float(self.srank[n, j]), 2),
                            members=[int(x_) for x_ in self.uid[n, mem]], size=int(self.ssize[n, j]),
                            leader="you" if ld == -2 else (int(self.uid[n, ld]) if ld >= 0 and self.used[n, ld] else None),
                            gate=GATES[int(self.sgate[n, j])], exit_cost=round(float(self.sxcost[n, j]), 2),
                            years=int((self.t - self.sform[n, j]) // 52), ways=[round(float(x_), 3) for x_ in seen]))
        return out

    def reach_view(self, n):
        # felt and hint are 0 to 1 (reach level / 3): felt is the character's sense; hint is reality only as a rough
        # step (spec 7 §6): three steps, 0 (none), .5 (some: reach 1 or 2), 1 (full)
        return dict(rings=list(RINGS), standing=[int(x_) for x_ in self.standing[n]],
                    felt=[round(float(x_) / 3, 2) for x_ in self.felt_reach[n]],
                    hint=[round(round(float(x_) / 3 * 2) / 2, 2) for x_ in self.reach[n]],
                    domains=list(DOMAINS), domain_standing=[int(x_) for x_ in self.dstanding[n]],
                    domain_hint=[round(round(float(x_) / 3 * 2) / 2, 2) for x_ in self.dreach[n]])

    # ------------------------------------------------------------------ save and load
    _CAST_F = ("uid", "nm", "line", "kof", "role", "rmask", "face", "born", "fem", "since", "died_t", "c", "cmax", "trust",
               "last", "debt", "mgood", "mbad", "secret", "brk", "health", "money", "mcls", "emp", "sector", "inst", "mpart",
               "nkids", "mood", "want", "wripe", "wstate", "wknown", "wdue", "stand", "mloc", "faith", "party", "strict",
               "fbiz", "fkin", "fkin_far", "mset", "lv", "msoc")
    _SET_F = ("skind", "scoh", "srank", "sts", "ssize", "sncast", "sgate", "sxcost", "sform", "sjoin", "sref", "slead")
    _PER_F = ("loc", "nb", "cls", "pfaith", "pparty", "pline", "hhj", "own_home", "pslot", "psector", "n_moves", "last_move",
              "par_change", "older_sib", "younger_sib", "vol_tgt", "fr_bias", "sociab", "unext", "female", "soc", "soc_home",
              "stat", "lang", "arr_t", "cls_home", "loc_home", "par_apart")

    def save(self, n, w=None, alive=True):
        """One life's cast, settings and place as a JSON-safe dict (w: the character's own pie, for a legacy line)."""
        py = lambda v_: v_.item() if hasattr(v_, "item") else v_
        ks = np.nonzero(self.used[n])[0]
        cast = []
        for k in ks:
            d = {f_: py(getattr(self, f_)[n, k]) for f_ in self._CAST_F}
            d["slot"] = int(k); d["pie"] = [float(x_) for x_ in self.pie[n, k]]; d["read"] = [float(x_) for x_ in self.read[n, k]]
            d["roles"] = [r_ for r_ in ROLE if int(self.rmask[n, k]) & BIT[r_]]; d["alive"] = bool(self.lv[n, k])
            cast.append(d)
        sets = []
        for j in range(self.M):
            d = {f_: py(getattr(self, f_)[n, j]) for f_ in self._SET_F}
            d["snorm"] = [float(x_) for x_ in self.snorm[n, j]]; d["sanch"] = [float(x_) for x_ in self.sanch[n, j]]
            sets.append(d)
        per = {f_: py(getattr(self, f_)[n]) for f_ in self._PER_F}
        per["family_mix"] = [float(x_) for x_ in self.family_mix[n]]; per["objk"] = [float(x_) for x_ in self.objk[n]]
        per["smem"] = [[int(s_), float(l_), int(st_)] for (n_, s_), (l_, st_) in sorted(self._smem.items()) if n_ == n]
        out = dict(version=2, world_seed=self.seed, run_seed=self.run_seed, t=int(self.t), t0=int(self.t0), K=self.K, M=self.M,
                   loc=int(self.loc[n]), cls=int(self.cls[n]), cast=cast, settings=sets, person=per,
                   self=dict(born=int(self.t0), fem=bool(self.female[n]), alive=bool(alive),
                             pie=None if w is None else [float(x_) for x_ in np.asarray(w, float)], nm=0, line=int(self.pline[n]),
                             mloc=int(self.loc[n]), mcls=int(self.cls[n]), faith=int(self.pfaith[n])),
                   nh=[[float(x_) for x_ in v_] for v_ in self.nh])
        if self.N == 1:
            out["rng"] = self.rng.bit_generator.state
        if self.sph_h or self.sph_hr or self.sph_mk:   # spheres phase 2 (only when on: off, a life saves as v22.2 saved it)
            out["spheres"] = dict(mark=[float(x_) for x_ in self.mark[n]], mark_yr=int(self._mark_yr),
                                  mark_wear=float(self.mark_wear[n]), mark_z=[float(x_) for x_ in self.mark_z[n]], hnt=[int(x_) for x_ in self.hnt[n]], shnt=[int(x_) for x_ in self.shnt[n]],
                                  rung=[float(x_) for x_ in self.rung[n]], ryrs=[float(x_) for x_ in self.ryrs[n]],
                                  hpick=int(self.hpick), rung_yr=int(getattr(self, "_rung_yr", -1)),
                                  hrng=self._hrng.bit_generator.state if self.N == 1 else None)
        if getattr(self, "sph_lv", False) or getattr(self, "sph_fr", False):   # phase 4 (only when on)
            out["spheres4"] = dict(fair=[float(x_) for x_ in self.fair[n]], p4_yr=int(self._p4_yr),
                                   fair_log=[[int(r_[0]), int(r_[2]), int(r_[3])] for r_ in self.fair_log if r_[1] == n])
        ca_, sa_ = getattr(self, "care_load", None), getattr(self, "sh_around", None)
        cm_ = getattr(self, "comrade", None)
        if ca_ is not None or sa_ is not None or cm_ is not None:   # phase 5 (only once on): this month's care load and
            out["spheres5"] = dict(care_load=None if ca_ is None else float(ca_[n]),   # shadow around them, the comrades
                                   sh_around=None if sa_ is None else [float(x_) for x_ in sa_[n]],
                                   comrade=None if cm_ is None else [int(k_) for k_ in np.nonzero(cm_[n])[0]],
                                   roots=None if getattr(self, "roots", None) is None else bool(self.roots[n]),
                                   care_buy=None if getattr(self, "care_buy", None) is None else bool(self.care_buy[n]))
        if self.far_on:   # far_ties (only when on): the town events read, and each slot's last far event and stay
            ks_ = np.nonzero(self.far_t[n] != NEVER)[0]
            out["far"] = dict(i=int(self._far_i), k=[int(k_) for k_ in ks_], ev=[int(x_) for x_ in self.far_ev[n, ks_]],
                              t=[int(x_) for x_ in self.far_t[n, ks_]], sg=[int(x_) for x_ in self.far_sg[n, ks_]],
                              sd=[[int(y_) for y_ in x_] for x_ in self.far_sd[n, ks_]],
                              inn=[int(x_) for x_ in self.far_in[n, ks_]], frm=[int(x_) for x_ in self.far_from[n, ks_]],
                              rng=self._far_rng.bit_generator.state if self.N == 1 else None)
        if getattr(self, "lw", False):   # S7 lead_ways (only when on): the life's posts, held and ended, and their moments
            out["lead"] = dict(posts=[dict(p_) for p_ in self.lw_posts if p_["n"] == n],   # (plain numbers already)
                               ended=[dict(p_) for p_ in self.lw_ended if p_["n"] == n],
                               due=[list(d_) for d_ in self.lw_due if d_[0] == n], q=int(self._lw_q),
                               back=[[int(k_[1]), int(v_)] for k_, v_ in self._lw_back.items() if k_[0] == n],
                               has=[bool(x_) for x_ in self.lw_has[n]],
                               rng=self._lw_rng.bit_generator.state if self.N == 1 else None)
        return out

    @classmethod
    def load(cls, W, saved, run_seed=None, cfg=None):
        """Lives saved by save() continue in World W (one dict, or a list of them: one per life)."""
        saved = [saved] if isinstance(saved, dict) else list(saved)
        d0 = saved[0]
        cfg = dict(cfg or {}); cfg.setdefault("K", d0["K"]); cfg.setdefault("M", d0["M"])
        pp = cls(W, len(saved), d0["run_seed"] if run_seed is None else run_seed,
                 female=[d_["person"]["female"] for d_ in saved], cfg=cfg)
        pp.t0 = int(d0["t0"]); pp.t = int(d0["t"]); pp._last_lives = pp.t
        for n, d in enumerate(saved):
            per = dict(d["person"])
            if int(d.get("version", 1)) < 2 and "sociab" not in per:   # version 1 kept sociability as "soc"
                per["sociab"] = per.pop("soc", 1.0)
            for f_ in cls._PER_F:
                if f_ in per:   # (fields added since a save keep their defaults)
                    getattr(pp, f_)[n] = per[f_]
            if "cls_home" not in per:
                pp.cls_home[n] = pp.cls[n]; pp.loc_home[n] = pp.loc[n]
            for s_, l_, st_ in per.get("smem", []):
                pp._smem[(n, int(s_))] = (float(l_), int(st_))
            pp.family_mix[n] = per["family_mix"]; pp.objk[n] = per["objk"]
            for m_ in d["cast"]:
                k = m_["slot"]; pp.used[n, k] = True
                for f_ in cls._CAST_F:
                    if f_ in m_:
                        getattr(pp, f_)[n, k] = m_[f_]
                pp.pie[n, k] = m_["pie"]; pp.read[n, k] = m_["read"]
            for j, s_ in enumerate(d["settings"]):
                for f_ in cls._SET_F:
                    getattr(pp, f_)[n, j] = s_[f_]
                pp.snorm[n, j] = s_["snorm"]; pp.sanch[n, j] = s_["sanch"]
        pp.nh = [np.asarray(v_, float) for v_ in d0.get("nh", [])]
        pp._psq = _csum(pp.pie * pp.pie).astype(np.float32)
        pp._xsoc = bool((pp.soc != pp.soc_home).any() or ((pp.msoc != pp.soc[:, None]) & pp.used).any())
        if len(saved) == 1 and "rng" in d0:
            pp.rng.bit_generator.state = d0["rng"]
        if pp.sph_h or pp.sph_hr or pp.sph_mk:
            for n, d in enumerate(saved):
                sp_ = d.get("spheres")
                if sp_:
                    pp.mark[n] = sp_.get("mark", [0.0] * C); pp._mark_yr = int(sp_.get("mark_yr", -1))
                    pp.mark_wear[n] = sp_.get("mark_wear", 0.0); pp.mark_z[n] = sp_.get("mark_z", [0.0, 0.0])
                    pp.hnt[n] = sp_["hnt"]; pp.shnt[n] = sp_["shnt"]; pp.rung[n] = sp_["rung"]; pp.ryrs[n] = sp_["ryrs"]
                    pp.hpick = int(sp_["hpick"]); pp._rung_yr = int(sp_["rung_yr"])
                    if len(saved) == 1 and sp_.get("hrng"):
                        pp._hrng.bit_generator.state = sp_["hrng"]
        if getattr(pp, "sph_lv", False) or getattr(pp, "sph_fr", False):
            for n, d in enumerate(saved):
                s4_ = d.get("spheres4")
                if s4_:
                    pp.fair[n] = s4_["fair"]; pp._p4_yr = int(s4_["p4_yr"])
                    pp.fair_log += [[t_, n, j_, v_] for t_, j_, v_ in s4_["fair_log"]]
        if any(d.get("spheres5") for d in saved):
            for n, d in enumerate(saved):
                s5_ = d.get("spheres5") or {}
                if s5_.get("care_load") is not None:
                    if getattr(pp, "care_load", None) is None:
                        pp.care_load = np.zeros(pp.N)
                    pp.care_load[n] = s5_["care_load"]
                if s5_.get("sh_around") is not None:
                    if getattr(pp, "sh_around", None) is None:
                        pp.sh_around = np.zeros((pp.N, C))
                    pp.sh_around[n] = s5_["sh_around"]
                if s5_.get("comrade") is not None and getattr(pp, "comrade", None) is not None:
                    pp.comrade[n, s5_["comrade"]] = True
                if s5_.get("roots") is not None and getattr(pp, "roots", None) is not None:
                    pp.roots[n] = bool(s5_["roots"])
                if s5_.get("care_buy") is not None and getattr(pp, "care_buy", None) is not None:
                    pp.care_buy[n] = bool(s5_["care_buy"])
        if pp.far_on:
            for n, d in enumerate(saved):
                f_ = d.get("far")
                if f_:
                    pp._far_i = int(f_["i"]); ks_ = np.asarray(f_["k"], np.int64)
                    if len(ks_):
                        pp.far_ev[n, ks_] = f_["ev"]; pp.far_t[n, ks_] = f_["t"]; pp.far_sg[n, ks_] = f_["sg"]
                        pp.far_sd[n, ks_] = f_["sd"]; pp.far_in[n, ks_] = f_["inn"]; pp.far_from[n, ks_] = f_["frm"]
                    if f_.get("rng") is not None and pp.N == 1:
                        pp._far_rng.bit_generator.state = f_["rng"]
        if getattr(pp, "lw", False):
            for n, d in enumerate(saved):
                l_ = d.get("lead")
                if l_:
                    ids_ = {}   # each life's posts take new ids (lives saved apart may share them)
                    for p_ in l_["posts"] + l_["ended"]:
                        ids_[p_["id"]] = pp._lw_next
                        p_ = dict(p_, n=n, id=pp._lw_next); pp._lw_next += 1
                        (pp.lw_posts if p_.get("end_t") is None else pp.lw_ended).append(p_)
                    pp.lw_due += [[n, d_[1], ids_.get(d_[2], -1), d_[3]] for d_ in l_["due"]]
                    pp._lw_q = int(l_["q"]); pp.lw_has[n] = l_["has"]
                    pp._lw_back.update({(n, int(k_)): int(v_) for k_, v_ in l_["back"]})
                    if l_.get("rng") is not None and pp.N == 1:
                        pp._lw_rng.bit_generator.state = l_["rng"]
        pp._fsh(); pp._close_index(); pp._alive_counts(np.arange(pp.N)); pp._outputs_settings()
        return pp
