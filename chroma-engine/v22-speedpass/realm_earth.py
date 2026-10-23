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
# 2006); Green in kin, land and its place in the whole (Howell et al. 2013). Columns still sum to .6; the note's rows
# (meaning 1.1, safety and belonging .95) became meaning .95 and safety 1.1 at the v24 refit (below)
NEED_MAP_V7 = [
  #  W     U     B     R     G
  [0.23, 0.28, 0.28, 0.13, 0.18],   # safety
  [0.20, 0.10, 0.10, 0.30, 0.25],   # belonging
  [0.00, 0.00, 0.00, 0.00, 0.00],   # autonomy (the engine: acting as oneself)
  [0.00, 0.00, 0.00, 0.00, 0.00],   # competence (the engine: succeeding at what is hard for you)
  [0.17, 0.22, 0.22, 0.17, 0.17],   # meaning
]
# (the v24 refit moved .03 of each colour's meaning to its safety, each column still .6: with the note's .20 to .25,
# meaning at 60 to 79 sat at .955, over the realism ceiling of .95, and safety .02 to .035 under v23.2's; now meaning
# .944 and safety at or above v23.2's, seeds 41 and 42, 100 lives)
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
# what each setback's cause is called (need_why's nw_imp_cause indexes this list; the core picks the cause from the life's
# age, its work, partner and health and, with the world on, its place's crime, disasters and war and the state's law and
# rights; needs-research.md section 5, "each setback should name its cause from these world facts"). In order: family,
# school, work, a partner, friends, crime where they live, a disaster, war, the state, the law failing, health, old
# age, word going round, a stranger. A realm names its own (a lord's decree, a curse, a raid from the hills)
IMP_CAUSES = ("family", "school", "work", "a partner", "friends", "crime nearby", "a disaster", "war", "the authorities",
              "the law failing", "failing health", "old age", "word going round", "a stranger")

# ---- v25 N3, setbacks that fit the world (switch imp_world; Outer world's chroma-world/spheres/world-fit-v1.md section 1
# and data/world_fit.json "setbacks", which wins). For each setback (IMPOSITIONS order) the world facts it follows, as
# {fact: elasticity e}: its weight g = prod (fact / ref) ** e, clipped to IMP_WORLD_CLIP. Facts about the life (crime
# where it lives, harm, the land, frailty, age) are normalised over the living people each year, so the kind's count
# holds and only who gets it moves; facts about the world (weak law, repression) are read against IMP_WORLD_REF, Earth's
# modern start, so a harsher world has more. Evidence: lawlessness follows the area's crime (Sampson et al. 1997);
# institutional trust and corruption track each other (Rothstein and Uslaner 2005); the rest are estimates
IMP_WORLD = (
    {"repress": 1.0},                    # a rule is imposed on you
    {"weak": 1.0, "crime": 0.3},         # an institution betrays its promise
    {},                                  # you are lied to and misled
    {},                                  # someone takes what you earned
    {"harm": 1.0, "land": 1.0},          # your community or habitat is damaged (harm: 1 + IMP_HARM_K x harm; land: x IMP_LAND_X)
    {},                                  # you are forbidden to see someone you love
    {},                                  # evidence you trusted is overturned
    {"frail": 1.5, "age": 1.0},          # you are made dependent on others (age by IMP_AGE_X)
    {"repress": 1.0},                    # your traditions are mocked or banned
    {"crime": 1.0, "weak": 0.5},         # lawlessness spreads around you
)
# refs: crime the population-weighted mean of the localities' crime (.05 to .30); weak = 1 - law_rule and repress = 1 -
# the mean of the rights in Earth's burned-in modern world (law_rule .856, rights .835 after the 80-year burn-in;
# Outer world 10-23: fixed Earth refs, not read at each run's start); frail = 1 - health (an estimate; Release's split
# was at .22)
IMP_WORLD_REF = dict(crime=0.206, weak=0.144, repress=0.165, frail=0.25)
IMP_WORLD_CLIP = (0.2, 4.0)
IMP_HARM_K = 5.0                      # harm (struck by a disaster or recovering from one, or at war): 1 + 5 x harm
IMP_LAND_X = 2.0                      # the land: x2 while a stretch the life loves is lost (only with wa_land)
IMP_AGE_X = ((70, 1.5), (80, 2.5))    # age: x1.5 from 70, x2.5 from 80 (estimates)
IMP_CAUSE = {   # what the panel names, by the fact that weighed most ({disaster_kind}, {stretch}: filled by the engine)
    "crime": "the crime around you", "weak": "the law growing weak", "repress": "the state tightening its grip",
    "harm": "the {disaster_kind} or the war", "land": "{stretch} lost", "frail": "your failing health", "age": "your age",
}
IMP_CAUSE_BETRAY_WEAK = "corruption in the institutions"   # the betrayal's own word for weak law

# ---- v25 #10, what a world rewards (switch tilt_world; Outer world's chroma-world/spheres/world-fit-v2.md section 2 and
# data/world_fit.json "tilt.engine", which wins; Engine contracts.md section 8). No global colour bonus (Emren's decision
# #10): Earth states, by place kind, community, institution and period, three things kept apart as dimensions on 0 to 1
# (.5 Earth's average and the neutral world), each (mean, sd): values (the people's own; read only through the existing
# start), practices (what places and bodies do) and incentives (what is recognised and rewarded). Only incentives reach
# the one tilt site, the years that make a regular and a known face: r[c] = (1 + MIX_K x (mix[c] / .2 - 1)) x (1 +
# PROFILE_K x sum_d (x[d] - .5) x DIM_COLOURS[d][c]), clipped to PROFILE_CLIP and renormalised to a mean of 1 per sphere
# (the sphere's mix read at half strength, Outer world 10-23, so r stays a tendency); x = the place's draw + a
# community's + the body's own (sd .10, seeded by its id) + the period's. Sources: Schwartz 2006; Gelfand et al. 2011;
# Harrington and Gelfand 2014; Fischer and Schwartz 2011; House et al. 2004 (GLOBE); Inglehart and Welzel 2005
# (directions). The sizes, k and the spreads are design estimates, tuned against the Known floor (decision #5).
PROFILE_DIMS = ('autonomy', 'belonging', 'norm_strength', 'hierarchy', 'egalitarian', 'mastery', 'harmony')
DIM_COLOURS = {   # many-to-many, interpretive: a design reading, not an empirical law (W U B R G; sums need not be 1)
    'autonomy': dict(W=0.0, U=0.638, B=0.434, R=0.862, G=0.066),
    'belonging': dict(W=0.443, U=0.0, B=0.13, R=0.0, G=0.427),
    'norm_strength': dict(W=0.406, U=0.155, B=0.178, R=0.0, G=0.261),
    'hierarchy': dict(W=0.315, U=0.27, B=0.415, R=0.0, G=0.0),
    'egalitarian': dict(W=0.257, U=0.0, B=0.0, R=0.413, G=0.33),
    'mastery': dict(W=0.0, U=0.231, B=0.444, R=0.325, G=0.0),
    'harmony': dict(W=0.178, U=0.306, B=0.0, R=0.0, G=0.516),
}
PROFILES = {   # kind -> name -> values, practices, incentives (dim: (mean, sd)), period, source, note
    'place': {
        'capital': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.537, 0.04), belonging=(0.444, 0.04), norm_strength=(0.456, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.518, 0.04), mastery=(0.518, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.537, 0.04), belonging=(0.444, 0.04), norm_strength=(0.456, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.518, 0.04), mastery=(0.518, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'second city': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.507, 0.04), belonging=(0.474, 0.04), norm_strength=(0.476, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.498, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.507, 0.04), belonging=(0.474, 0.04), norm_strength=(0.476, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.498, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'university city': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.527, 0.04), belonging=(0.454, 0.04), norm_strength=(0.466, 0.04), hierarchy=(0.458, 0.04), egalitarian=(0.538, 0.04), mastery=(0.478, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.527, 0.04), belonging=(0.454, 0.04), norm_strength=(0.466, 0.04), hierarchy=(0.458, 0.04), egalitarian=(0.538, 0.04), mastery=(0.478, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'port city': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.512, 0.04), belonging=(0.484, 0.04), norm_strength=(0.446, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.508, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.512, 0.04), belonging=(0.484, 0.04), norm_strength=(0.446, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.508, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'declining industrial town': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.462, 0.04), belonging=(0.564, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.528, 0.04), mastery=(0.428, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.462, 0.04), belonging=(0.564, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.528, 0.04), mastery=(0.428, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'industrial town': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.477, 0.04), belonging=(0.544, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.528, 0.04), egalitarian=(0.508, 0.04), mastery=(0.478, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.477, 0.04), belonging=(0.544, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.528, 0.04), egalitarian=(0.508, 0.04), mastery=(0.478, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'market town': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.462, 0.04), belonging=(0.564, 0.04), norm_strength=(0.556, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.521, 0.04)),
            incentives=dict(autonomy=(0.462, 0.04), belonging=(0.564, 0.04), norm_strength=(0.556, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.521, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'commuter suburb': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.477, 0.04), belonging=(0.504, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.518, 0.04), egalitarian=(0.468, 0.04), mastery=(0.528, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.477, 0.04), belonging=(0.504, 0.04), norm_strength=(0.536, 0.04), hierarchy=(0.518, 0.04), egalitarian=(0.468, 0.04), mastery=(0.528, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'coastal resort': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.507, 0.04), belonging=(0.504, 0.04), norm_strength=(0.476, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.521, 0.04)),
            incentives=dict(autonomy=(0.507, 0.04), belonging=(0.504, 0.04), norm_strength=(0.476, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.521, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'farming village': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.437, 0.04), belonging=(0.594, 0.04), norm_strength=(0.586, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.541, 0.04)),
            incentives=dict(autonomy=(0.437, 0.04), belonging=(0.594, 0.04), norm_strength=(0.586, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.541, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'fishing village': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.477, 0.04), belonging=(0.594, 0.04), norm_strength=(0.576, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.518, 0.04), mastery=(0.478, 0.04), harmony=(0.531, 0.04)),
            incentives=dict(autonomy=(0.477, 0.04), belonging=(0.594, 0.04), norm_strength=(0.576, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.518, 0.04), mastery=(0.478, 0.04), harmony=(0.531, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'mountain village': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.467, 0.04), belonging=(0.584, 0.04), norm_strength=(0.576, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.571, 0.04)),
            incentives=dict(autonomy=(0.467, 0.04), belonging=(0.584, 0.04), norm_strength=(0.576, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.571, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'river village': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.477, 0.04), belonging=(0.584, 0.04), norm_strength=(0.566, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.541, 0.04)),
            incentives=dict(autonomy=(0.477, 0.04), belonging=(0.584, 0.04), norm_strength=(0.566, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.478, 0.04), harmony=(0.541, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'remote area': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.477, 0.04), belonging=(0.584, 0.04), norm_strength=(0.556, 0.04), hierarchy=(0.468, 0.04), egalitarian=(0.518, 0.04), mastery=(0.478, 0.04), harmony=(0.561, 0.04)),
            incentives=dict(autonomy=(0.477, 0.04), belonging=(0.584, 0.04), norm_strength=(0.556, 0.04), hierarchy=(0.468, 0.04), egalitarian=(0.518, 0.04), mastery=(0.478, 0.04), harmony=(0.561, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'tech boom town': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.537, 0.04), belonging=(0.434, 0.04), norm_strength=(0.456, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.558, 0.04), harmony=(0.491, 0.04)),
            incentives=dict(autonomy=(0.537, 0.04), belonging=(0.434, 0.04), norm_strength=(0.456, 0.04), hierarchy=(0.498, 0.04), egalitarian=(0.488, 0.04), mastery=(0.558, 0.04), harmony=(0.491, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
        'energy boom town': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.497, 0.04), belonging=(0.474, 0.04), norm_strength=(0.506, 0.04), hierarchy=(0.538, 0.04), egalitarian=(0.488, 0.04), mastery=(0.548, 0.04), harmony=(0.431, 0.04)),
            incentives=dict(autonomy=(0.497, 0.04), belonging=(0.474, 0.04), norm_strength=(0.506, 0.04), hierarchy=(0.538, 0.04), egalitarian=(0.488, 0.04), mastery=(0.548, 0.04), harmony=(0.431, 0.04)),
            period='modern', source='Schwartz 2006; Gelfand 2011; Harrington and Gelfand 2014; Inglehart and Welzel 2005 (directions); sizes are design estimates',
            note="values at the middle: Earth's people keep the existing start's lean (no new lean, lives unchanged); practices and incentives share the place's deviation, which feeds the faces and the tilt site respectively"),
    },
    'community': {
        'faith congregation': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.5, 0.05), belonging=(0.56, 0.05), norm_strength=(0.56, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.5, 0.05), harmony=(0.52, 0.05)),
            incentives=dict(autonomy=(0.5, 0.05), belonging=(0.56, 0.05), norm_strength=(0.56, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.5, 0.05), harmony=(0.52, 0.05)),
            period='modern', source='Gelfand 2011 (religiosity and tightness); size a design estimate',
            note="a deviation added to the place's for members' settings"),
        'sports or hobby club': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.5, 0.05), belonging=(0.54, 0.05), norm_strength=(0.5, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.53, 0.05), harmony=(0.5, 0.05)),
            incentives=dict(autonomy=(0.5, 0.05), belonging=(0.54, 0.05), norm_strength=(0.5, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.53, 0.05), harmony=(0.5, 0.05)),
            period='modern', source='design estimate',
            note="a deviation added to the place's for members' settings"),
        'neighbourhood': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.5, 0.05), belonging=(0.5, 0.05), norm_strength=(0.5, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.5, 0.05), harmony=(0.5, 0.05)),
            incentives=dict(autonomy=(0.5, 0.05), belonging=(0.5, 0.05), norm_strength=(0.5, 0.05), hierarchy=(0.5, 0.05), egalitarian=(0.5, 0.05), mastery=(0.5, 0.05), harmony=(0.5, 0.05)),
            period='modern', source="the place's own profile; no deviation of its own",
            note="a deviation added to the place's for members' settings"),
    },
    'institution': {
        'any body': dict(
            values=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            practices=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            incentives=dict(autonomy=(0.5, 0.1), belonging=(0.5, 0.1), norm_strength=(0.5, 0.1), hierarchy=(0.5, 0.1), egalitarian=(0.5, 0.1), mastery=(0.5, 0.1), harmony=(0.5, 0.1)),
            period='modern', source='House et al. 2004 (GLOBE: organisations differ within one society); sd a design estimate',
            note="a deviation drawn around its place (sd .10), seeded by the body's id, kept, drifting .1 a year toward its leaders' practice; no sphere-typical mean, because the sphere's character is already in its colour mix"),
    },
    'period': {
        'modern': dict(
            values=dict(autonomy=(0.5, 0.0), belonging=(0.5, 0.0), norm_strength=(0.5, 0.0), hierarchy=(0.5, 0.0), egalitarian=(0.5, 0.0), mastery=(0.5, 0.0), harmony=(0.5, 0.0)),
            practices=dict(autonomy=(0.5, 0.0), belonging=(0.5, 0.0), norm_strength=(0.5, 0.0), hierarchy=(0.5, 0.0), egalitarian=(0.5, 0.0), mastery=(0.5, 0.0), harmony=(0.5, 0.0)),
            incentives=dict(autonomy=(0.5, 0.0), belonging=(0.5, 0.0), norm_strength=(0.5, 0.0), hierarchy=(0.5, 0.0), egalitarian=(0.5, 0.0), mastery=(0.5, 0.0), harmony=(0.5, 0.0)),
            period='modern', source='the reference epoch',
            note='other epochs and realms state their own'),
    },
}
PROFILE_K = 1.5
MIX_K = 0.5   # the share of the sphere's own mix that reaches r (1: r = mix / .2)
PROFILE_CLIP = (0.67, 1.5)
# which group kinds (world_keys.GROUP_KINDS) are which community of PROFILES["community"]; a setting of another kind has
# only its body's own draw (the neighbourhood's profile is the place's own)
COMMUNITY_GROUPS = {"congregation": "faith congregation", "club": "sports or hobby club", "neighbours": "neighbourhood"}
# other-shapes.md section 1's formal layer: r[s][c] += TILT_LAYER[c] x (s in TILT_FORMAL) x (law_rule / TILT_LAW_REF). Earth's
# is 0 in every colour (decision #10: a predetermined global White-Blue lift is ruled out; a layer can come back only
# as a property of particular institutions, places or periods, with its spread and source, through PROFILES)
TILT_FORMAL = ("rule", "prot", "learn", "care", "prod")   # the spheres whose formal bodies the layer may apply to
TILT_LAYER = (0.0, 0.0, 0.0, 0.0, 0.0)                   # W U B R G, sums to 0
TILT_LAW_REF = 0.73                                      # the layer is at full strength at this law_rule
TILT_LAND = (1.0, 1.0, 1.0, 1.0, 1.0)   # read by lane D: the land rewards every colour alike on Earth (decision #2)

# ---- v25 lane D, the land (wa_land; chroma-world/spheres/land-v1.md, values in sphere_data.LAND). Earth's land is
# physical (decision #2): nothing below reads a colour. What LAND leaves to the engine, each an estimate unless a source
# is named. sd: one standard deviation of each felt state, the unit LAND's sizes (small .1, clear .25, strong .5, very
# strong 1) are written in (estimates from the engine's own spread among adult lives)
LAND_ENGINE = dict(
    sd=dict(need=0.12, money=0.15, health=0.10, mood=0.25, stress=0.20),
    # a strike's households (for_all_lives disaster_hit): the share of a struck town's households hit is .05 + .25 x
    # severity (flood, fire, quake, storm; heat hits no home); over displaced_sev they also leave home (one size step more)
    hit_share=(0.05, 0.25), displaced_sev=0.7, hit_kinds=("flood", "fire", "quake", "storm"),
    disrupted=0.2,              # disaster_near: of the rest of the town, 1 in 5 cut off or out of work (safety - clear)
    # the hit person's year (after_disaster shapes, Bonanno 2024): weeks at full depth, then weeks to fade out; delayed:
    # fine at first (delayed_dip: weeks at a depth), low from a year to two years. Chronic lasts until helped: each week
    # after its first two years ends it with chronic_end (x 3 with close bonds)
    course=dict(resilient=(8, 8), recovery=(26, 52), chronic=(104, 0), delayed=(52, 52)), delayed_dip=(8, 0.3),
    chronic_end=0.005,
    shape_bonds=1.0, shape_money=1.0,   # close bonds (ties) raise the odds of resilient; isolation and money lost, chronic
    course_safety=0.3, course_stress=0.02,   # each week at full depth: the safety need's supply and stress
    trust_weeks=52, trust_belong=0.1,   # after_help: the town's trust clearly up for a year, then fading by .5 a quarter
    heat_old=75, heat_frail=0.4,        # heat_summer: the old and the frail (health under this) lose health clearly
    # nature time (dose): minutes a week outdoors on the town's land (walks) = walk_min x the town's nature access x a
    # lognormal of sd walk_sd for each person, plus the hours in nature haunts and in the land ways held
    walk_min=200.0, walk_sd=0.8, nature_haunts=("prod.wild", "prod.land"),
    worry_share=0.6, worry_ages=(16, 25), worry_rise=0.05,   # climate_worry (Hickman 2021): while extremes rise this much
    attach_age=12, lost=0.2, haunt_years=10,   # sick_land: lost .2 since 12; clear after 10 years of haunting
    per_year=1.0, gap_weeks=13,         # the moments' budget: about one a year, never two in a quarter
    alone=(0.3, 0.1),                   # company: alone about .3 of the time for adults, .1 for the young
    stranger_tie=0.25,                  # a stranger becomes an acquaintance 1 in 4
    tie_small=0.02, tie_clear=0.05,     # a tie closer a little, clearly
    max_ways=3, way_time=1 / 112.0,     # ways: at most three held; each hour a week is this share of the week's waking
                                        # hours (as world_answers' price)
    way_k=0.1,                          # a held way's yearly effect, in sd units per unit of its effect (keenness 1)
    everyday=0.002, everyday_step=0.0005,   # reach.everyday: at most .002 a year on a stretch; a moment's use moves it this
    tend_per10=0.002, tend_cap=0.02,    # uses.tend: a group tending a stretch, per 10 members a year, at most
    # the moments the land brings when its state holds (a moment's `when`), the chance it comes in that week or year
    force=dict(flood_home=1.0, storm_damage=1.0, neighbours_dig_out=0.3, smoke_days=0.3, heatwave=0.3, drought=0.2,
               dry_well=0.2, sick_river=0.3, wood_cleared=0.3, protest_at_the_wood=0.2, river_clean_again=1.0,
               planted_tree_grown=1.0, remembrance_tree=0.3, first_date_outdoors=0.3, climate_worry=0.3,
               outdoor_injury=0.05),
)
# which stretch a Known land decision moves (its moment's land: key; the decisions open no way to read it from)
LAND_DECIDE = dict(save_the_wood="wood", drain_the_marsh="water", open_a_quarry="field", plant_trees="wood",
                   water_rule="water", flood_defence="water")

# ---- v25 lane D, national standing (wa_nat_climb; chroma-engine/notes/v25/other-shapes.md section 5, world-fit-v2.md
# section 3, sphere_data.WORLD_FIT national). The climb: a life at a route's wider step (rung_years at rung 4, or a summit
# title held, or a movement or firm past its town) reaches each kind (recognition, influence, authority) with base a
# year, x aim_x with an aim for that route; authority only to a free seat (no town-size factor, decision #11). The
# movement road (a movement holding movement_share of the country) and the money road (money and work rank) reach
# national influence, not authority. country_people: the model country's people a movement's members are counted
# against (estimate). Authority holds while the seat is held and hold_after_years after; recognition fades over
# recognition_fade_years without new work; influence holds while its asset (rung 4, the movement, the money) holds
NATIONAL_CLIMB = dict(rung_years=5, base=0.02, aim_x=1.5, movement_share=0.01, money=0.99, work_rank=0.85,
                      hold_after_years=2, recognition_fade_years=10, country_people=1_000_000, influence_y=(4, 8),
                      # a seat's term in years (drawn when taken), its fall or scandal a year, the age it ends by, and a
                      # movement's members or a firm's people past its town (estimates)
                      seat_years=(4, 10), seat_fall=0.05, seat_age=75, past_town=dict(movement=1000, work=200))



# ---- The heights of a life (aims v1, plan.md section 5, behind aims and heights): Earth's names for each height. The
# core reads leading a sphere (rung 4; Emren 10-19, not pillar) as Known and a summit title (TIER 2) as Notable in every realm; what a
# realm names here is its own. Read as Release reads them (chroma-release/out/heights/heights_judge.py, 10-19): Known,
# a good name in town or a master's mark (no master's perk exists; the craft's top title and hallmark stand in);
# Notable, reach across the country; Historic, head of a state (head of government stands in), of a movement, or a
# work that outlives them (chroma-packs/core/legacy.py)
HEIGHT_NAMES = dict(
    Known=["good name in town", "master craftsperson", "a maker's hallmark"],
    Notable=["known across the country", "a household name"],
    Historic=["head of government", "founder of a movement", "a work that outlives you"],
)

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
# v25 aims v2 (lane B, aims_v2; aims-shape.md section 5): Earth's week for the one resource account, hours a week.
# Waking hours after sleep (about 8.8 h a day), the essentials (eating, personal care, about 2 h a day) and household
# work (about 2 h a day), a partner's own time, and the free hours of a life with nothing held (world off: res time 1).
# Rounded from the American Time Use Survey 2019 averages (sleep 8.8 h, eating and personal care 1.9 h, household 1.9 h,
# leisure and sport 5.2 h a day); provisional, as every aims_v2 number.
AIM_WEEK = dict(wake=116.0, essentials=14.0, household=13.0, partner=7.0, free_open=36.0)
# integrated assets (aims-shape.md section 5, "Gains"): a rare asset a life earns once when an integrate outcome shows two
# of its fields used together. Key: (field, field) by name (either order), or (shape, shape); value dict(name (the
# asset's words), title ("" or a catalogue title or perk it grants), opens (words: what it opens), rungs (the least rung
# reached in each, default (1, 1))). The Library writes Earth's; empty, nobody earns one (the mechanism stays).
AIM_ASSETS = {}
