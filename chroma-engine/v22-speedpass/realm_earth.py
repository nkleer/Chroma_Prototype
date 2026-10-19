"""Earth's realm: the constants that are modern Earth's, not the core's (realm-ready, the next stage's standing rule;
chroma-ideas/next-table-2026-10-19/plan.md section 2). The core (colours, needs, means, people, places, powers) stays in
the engine; a realm gives it its face as data: here the setbacks and the needs they hit, the needs table and what
commitments meet, births, the body, the mind and death, the settings' norms, and the keys of law and technology.

Moved verbatim from library.py, engine.py and world_keys.py, which import every name back, so every life is the same
byte for byte. A later realm (the Spires first) is a file like this one. Nothing here may import the engine.
"""
import re

# ---- Setbacks: unchosen impositions and the needs they hit (from library.py)
# Unchosen impositions: things that happen TO the person. They hit human needs
# directly (needs are shared across colors), and raise stress. sampled with
# probability impose_p per week.
IMPOSITIONS = [
  ("a rule is imposed on you", "autonomy-.6"),
  ("an institution betrays its promise", "safety-.4 meaning-.3"),
  ("you are lied to and misled", "competence-.3 safety-.3"),
  ("someone takes what you earned", "autonomy-.3 competence-.3"),
  ("your community or habitat is damaged", "belonging-.4 safety-.3"),
  ("you are forbidden to see someone you love", "belonging-.6"),
  ("evidence you trusted is overturned", "competence-.4 meaning-.2"),
  ("you are made dependent on others", "autonomy-.5"),
  ("your traditions are mocked or banned", "meaning-.4 belonging-.3"),
  ("lawlessness spreads around you", "safety-.6"),
]


# ---- The needs table: how far each colour's ends meet each need (from library.py)
NEED_MAP = [
  #  W     U     B     R     G
  [0.35, 0.15, 0.20, 0.00, 0.30],   # safety: order, foresight, self-protection, rootedness
  [0.25, 0.00, 0.00, 0.35, 0.40],   # belonging: duty, love and passion, community
  [0.00, 0.25, 0.45, 0.30, 0.00],   # autonomy: mastery of self, power, freedom
  [0.15, 0.45, 0.25, 0.10, 0.05],   # competence: skill, knowledge, results
  [0.25, 0.15, 0.10, 0.25, 0.25],   # meaning: duty, understanding, passion, place in the whole
]
# v6: autonomy and competence are met by HOW one acts, in any color (self-determination theory, Ryan & Deci 2000):
# autonomy by acting as oneself (self-concordance, Sheldon & Elliot 1999) plus free time and freedom; competence by
# succeeding at what is hard for you (effectance). The engine supplies both. Colors' ends meet the three needs that
# depend on WHAT one serves: safety, belonging and meaning, and every color meets the same total (columns sum to 0.6).
# In v5 Black and Blue met most of autonomy and competence, so the scarcest needs made Black-, Blue- and White-leaners
# the most satisfied and Red-leaners the least, while surveys find values barely predict life satisfaction.
NEED_MAP_V6 = [
  #  W     U     B     R     G
  [0.25, 0.20, 0.20, 0.15, 0.20],   # safety: order, foresight, self-protection and means, standing up for one's own, home and roots
  [0.15, 0.10, 0.15, 0.30, 0.30],   # belonging: duty, kinship of minds, alliances, love and passion, community
  [0.00, 0.00, 0.00, 0.00, 0.00],   # autonomy: acting as oneself (engine), free time and freedom
  [0.00, 0.00, 0.00, 0.00, 0.00],   # competence: succeeding at what is hard for you (engine), in any color
  [0.20, 0.30, 0.25, 0.15, 0.10],   # meaning: duty and faith, understanding, ambition and legacy, passion, place in the whole
]


# ---- Commitments: their weekly time and the needs they meet, and the duties they bring (from library.py)
# v4: commitments: (name, weekly time load, needs it meets while held, scaled by its strength)
COMMITMENTS = [
  ("career",    0.40, "competence.6 meaning.3 safety.1"),
  ("partner",   0.15, "belonging.7 safety.3"),
  ("children",  0.30, "meaning.6 belonging.4"),
  ("community", 0.10, "belonging.5 meaning.5"),
  ("faith",     0.05, "meaning.6 belonging.3 safety.1"),   # a religion, ideology or cause; often inherited in childhood
]
# v6: duties. A held commitment makes the needs of the people it serves felt as one's own (a parent feels the child's
# need for safety; a job asks for competence and provision). This is why roles move values (social investment).
DUTIES = {
  "career":    "competence.5 safety.5",
  "partner":   "belonging.6 safety.4",
  "children":  "safety.6 belonging.4",
  "community": "belonging.5 safety.5",
  "faith":     "meaning.6 belonging.4",
}
# ---- Needs that fit life (the next stage's workstream 4, behind need_tab="v7" and imp_age; read from today's tables
# unless set). chroma-ideas/next-table-2026-10-19/needs-research.md, one source per cell (section 7):
# each colour's ends: White's order and duty also make belonging (McMillan & Chavis 1986); Blue's foresight is safety
# (Aspinwall & Taylor 1997) and its meaning is curiosity's (Kashdan & Steger 2007); Black's means are safety (Kasser
# et al. 1995) and cost belonging (Dittmar et al. 2014); Red finds meaning in passion and the people loved (King et al.
# 2006); Green in kin, land and its place in the whole (Howell et al. 2013). Columns still sum to .6; meaning's row
# rises from 1.0 to 1.1, safety and belonging fall to .95 each
NEED_MAP_V7 = [
  #  W     U     B     R     G
  [0.20, 0.25, 0.25, 0.10, 0.15],   # safety
  [0.20, 0.10, 0.10, 0.30, 0.25],   # belonging
  [0.00, 0.00, 0.00, 0.00, 0.00],   # autonomy (the engine: acting as oneself)
  [0.00, 0.00, 0.00, 0.00, 0.00],   # competence (the engine: succeeding at what is hard for you)
  [0.20, 0.25, 0.25, 0.20, 0.20],   # meaning
]
# what each commitment meets while held (each row still 1.0): a partner gives meaning (Gold et al. 2024), work gives
# contact and less meaning than a calling (Paul & Batinic 2010, Wrzesniewski et al. 1997), a community gives safety
# (Sampson et al. 1997), a faith's belonging is its congregation (Lim & Putnam 2010)
COMMIT_MEETS_V7 = {
  "career":    "competence.55 meaning.2 safety.15 belonging.1",
  "partner":   "belonging.55 safety.25 meaning.2",
  "children":  "meaning.65 belonging.35",
  "community": "belonging.5 meaning.35 safety.15",
  "faith":     "meaning.5 belonging.35 safety.15",
}
# the youngest age each setback (IMPOSITIONS, in order) can happen at (imp_age): a rule imposed from 10 (Smetana et al.
# 2006), an institution's betrayal from 12, being lied to from 5 (Heyman et al. 2009), what you earned taken from 4
# (Kanngiesser & Warneken 2012), the community damaged at any age (Masten & Osofsky 2010), kept from someone loved from
# 1 (Ainsworth et al. 1978), trusted evidence overturned from 14 (Kuhn et al. 2000), made dependent from 16 (Baltes
# 1996), traditions mocked from 7 (Brown & Bigler 2005), lawlessness at any age (Fowler et al. 2009)
IMP_AGE = (10, 12, 5, 4, 0, 1, 14, 16, 7, 0)


# ---- Births by the parent's age, and a home together (from engine.py)
# births by the parent's age (birth_age): births a year per 1,000 women and per 1,000 men at each age (US NCHS natality,
# mothers 2019 and fathers' age-specific rates), read as a share of the peak; own births only
FERT_F = ((15, 0.0), (17, 17), (22, 66), (27, 93), (32, 98), (37, 52), (42, 12), (47, 1), (51, 0.0))
FERT_M = ((15, 0.0), (17, 8), (22, 60), (27, 95), (32, 100), (37, 60), (42, 25), (47, 9), (52, 3), (57, 1), (62, 0.0))
BIRTH_OWN = ("a child is born", "a baby on the way, planned or not")   # the moments of a life's own births
BIRTH_NOT = re.compile(r"adopt|foster|take (?:them )?in|surrogate|clinic|donor", re.I)   # other ways to a child
HOME_TOGETHER = ("living together", "wife or husband", "married again", "partner of many years",
                 "spouse in a family-arranged marriage")   # the titles of a home together (birth_with)


# ---- The body, the mind and death: life tables, illnesses, conditions (from engine.py)
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
    dip_level=False,         # v22.5 F9.37: what an illness or injury takes (its dip, a condition's weight, the mark it leaves) is a
                             # share of what the body has at its age (x its level for the age over its best), less at 90 than at 30
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
    frail_late=None,         # v22.5 F9.33: (age, slope): from this age the body's own failing rises at this slope instead (its
                             # last reserves go), so almost no one lives past 105. None: one slope
    ser_fatal=dict(cancer=0.4, **{"heart disease": 0.15, "a stroke": 0.2, "lung disease": 0.4}),   # a serious
                             # illness's course ends in death this often (at 60, with the body at its age's level)
    ser_age=0.02, ser_age_lim=(0.4, 2.0),   # x (1 + this x (age - 60)), within these: the young come through more often
    cond_k=0.005,            # a condition's complications: its weight x this x e^(.06 (age - 50)) a year
    decline=dict(old=(12, 52), serious=(4, 20), condition=(8, 30)),   # weeks of the last decline, by what ends the life
    decline_k=1.0,           # v22.5 F9.37: the decline deepens as (the share of its weeks gone) ** this; 2: slowly at first and
                             # steeply at the end, as a last decline does (most of its weeks are not yet the lowest)
)


# ---- Settings: role strictness and acceptance by setting (from engine.py)
ROLE_BY_SETTING = dict(earth=0.3, tribal=0.7, magic=0.5)     # role_strict when None (estimates; ISSP 2012, WVS 7)
ACCEPT_BY_SETTING = dict(earth=0.5, tribal=0.3, magic=0.5)   # accept_trans when None (estimates)


# ---- Laws and norms: the keys an option's law: and norm: may name (from world_keys.py)
LAW_KEYS = ["drugs", "divorce", "abortion", "same-sex marriage", "conscription", "guns", "gambling", "alcohol", "sex work",
            "euthanasia", "home schooling", "death penalty", "adoption"]
# v23: a key written with a leading minus closes the option the other way round (law: -conscription, evading a call-up
# where conscription is in force; norm: -same-sex marriage, snubbing a same-sex partner where it is accepted)
NORM_KEYS = LAW_KEYS + ["cohabiting", "tattoos", "single parenthood", "faith in public", "leaving a faith", "coming out",
                        "role crossing", "transition", "mixed marriage"]
# W38b (the Library's held-back law keys): options may name them in law: and norm:. The world does not model them yet:
# they read at their modern state (world.py LAW_MOD, NORM_MOD) until the world's switch for them is built (v22.3 refit).
LAW_V23 = ["tobacco", "knives", "drink-driving", "prescription medicines", "childminding", "gender on papers"]
LAW_KEYS_ALL = LAW_KEYS + LAW_V23           # what an option's law: may name
NORM_KEYS_ALL = NORM_KEYS + LAW_V23         # what an option's norm: may name
# "role crossing": acceptance of living across the expected role for one's sex (was "women at work"); options use role:
# "transition": acceptance of living as one's own gender (chroma-identity/for-the-engine.md)


# ---- Technology: the keys an option's tech: may name (from world_keys.py)
TECH_KEYS = ["phone", "computer", "internet", "video calls", "online dating", "remote work", "ai helper", "modern medicine",
             "car", "plane"]
