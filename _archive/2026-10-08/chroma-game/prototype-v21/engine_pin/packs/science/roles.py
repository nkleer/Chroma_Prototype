# Chroma content pack: Science, Research and Discovery. The engine's reading of how each title and perk comes and goes,
# proposed in earth_rules.ROLES syntax (chroma-engine/prototype/earth_rules.py, "ROLES = {"). Plain data for the engine
# thread, which owns the rules and refits every rate to the catalogue's shares (ROLE_NORM). Condition words are the ones
# the engine has today: has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark') >= n, had(['situation'], years), age,
# money, health, held_career, yrs_career, and the like.
#
# In this pack most first steps are taken by the player's own act at a door (title: on an option in the pack's
# moments), so the background rates below are low: they stand for the ordinary lives that drift into research without
# a door moment, and the engine fits them so the simulated shares match the catalogue.

ROLES_SCIENCE = {
    # careers: entries
    "research assistant": dict(req="((has('graduate') & (has('lab work') | has('finding things out') | "
                                   "has('working with data'))) | (yrs_has('citizen scientist') >= 2) | "
                                   "(yrs_has('community observer') >= 2)) & (age <= 33)",   # a science degree, or years
                               after=["citizen scientist", "community observer"], rungs=["graduate"],   # the degree is a
                               rate=0.01, entry=True),                 # rung kept on the step (engine rungs=, 11:30)
    # careers: rungs
    "research scientist": dict(req="has('doctoral graduate') | (has('graduate') & (was('research assistant') | "
                                   "was('laboratory technician')) & (mkn('learned a skill') >= 4))",
                               after=["research assistant", "laboratory technician", "research data steward",
                                      "research software engineer"], rate=0.09, entry=True),
    "research project lead": dict(after=["research scientist", "research software engineer", "research data steward",
                                         "evidence synthesis specialist", "participatory research coordinator"],
                                  req="(yrs_career >= 3) & (has('research grant') | has('a research project under way'))",
                                  rate=0.6),
    "research group leader": dict(after=["research project lead", "research scientist"],
                                  req="(yrs_career >= 6) & has('research grant') & (has('published research') | "
                                      "has('name in the field'))", rate=0.05,
                                  grants=["supervising researchers"]),
    "research facility lead": dict(after=["laboratory technician", "research scientist", "research software engineer"],
                                   req="(yrs_career >= 8) & has('instrument troubleshooting')", rate=0.03),
    "independent investigator": dict(after=["research scientist", "research project lead", "research group leader",
                                            "research data steward"],
                                     req="(has('published research') | has('a finding that held up')) & "
                                         "(has('research grant') | has('savings') | (money > .45))", rate=0.002),
    # careers: side roads
    "research software engineer": dict(req="has('writing code') & ((yrs_has('software developer') >= 2) | "
                                           "(yrs_has('data analyst') >= 2) | was('research assistant') | "
                                           "was('research scientist'))", after=["research assistant", "software developer",
                                                                         "data analyst"], rate=0.03, entry=True),
    "research data steward": dict(req="(has('working with data') | has('archive research')) & (was('research assistant') | "
                                      "was('research scientist') | was('laboratory technician') | "
                                      "(yrs_has('data analyst') >= 2) | (yrs_has('archivist') >= 2))",
                                  after=["research assistant", "archivist", "data analyst"], rate=0.02, entry=True),
    "evidence synthesis specialist": dict(req="has('graduate') & (has('evidence synthesis') | has('finding things out'))",
                                          after=["research scientist", "research assistant"], rate=0.02),
    "science communication specialist": dict(req="has('graduate') & (has('explaining science') | "
                                                 "((has('public speaking') | has('reporting')) & "
                                                 "(was('research scientist') | was('research assistant') | "
                                                 "has('finding things out'))))",
                                             after=["research scientist", "research assistant", "journalist", "teacher"],
                                             rate=0.015, entry=True),
    "participatory research coordinator": dict(req="has('community listening') | was('volunteer research organiser')",
                                               after=["research assistant", "research scientist"], rate=0.03),
    # community
    "citizen scientist": dict(req="(age >= 12) & (time > .4) & (has('finding things out') | has('knowing the woods'))",
                              rate=0.0001, starts=True, weight="colors",
                              lose="yrs_has('citizen scientist') >= 2", lrate=0.3, lwhy="the season over, and no next one"),
    "community observer": dict(req="(age >= 12) & (was('citizen scientist') | has('knowing the woods'))",
                               rate=0.007, starts=True, weight="practice"),
    "volunteer research organiser": dict(req="(was('citizen scientist') | was('community observer')) & "
                                             "(has('organising people') | mk('helped someone in need'))", rate=0.003),
    # facets (colorless appointments)
    "postdoctoral researcher": dict(refines="research scientist",
                                    req="has('research scientist') & was('doctoral graduate') & "
                                        "(yrs_has('research scientist') <= 3)", rate=0.6,
                                    lose="yrs_has('postdoctoral researcher') >= 5", lrate=0.5,
                                    lwhy="the fixed-term years over"),
    "professor": dict(refines="research scientist; research group leader",
                      req="(has('research group leader') | (has('research scientist') & was('research project lead'))) & "   # a rung below (09:18)
                          "(yrs_career >= 10) & "
                          "(has('name in the field') | has('published research'))", rate=0.12),
    # skills: learned on the job (rates per year while the job is held)
    "experimental design": dict(req="has('research scientist') | has('research assistant') | has('research project lead')",
                                rate=0.15, weight="practice"),
    "statistical judgment": dict(req="has('working with data') & (has('research scientist') | has('data analyst') | "
                                     "has('research data steward'))", rate=0.25, weight="practice"),
    "instrument troubleshooting": dict(req="has('lab work') & (has('laboratory technician') | has('research scientist') | "
                                           "has('research facility lead'))", rate=0.25, weight="practice"),
    "fieldwork": dict(req="has('research scientist') | has('community observer') | has('archaeologist') | "
                          "has('participatory research coordinator')", rate=0.03, weight="practice"),
    "qualitative interpretation": dict(req="has('research scientist') | has('participatory research coordinator')",
                                       rate=0.05, weight="practice"),
    "reproducible workflow": dict(req="has('research software engineer') | has('research data steward') | "
                                      "(has('research scientist') & has('writing code'))", rate=0.12, weight="practice"),
    "evidence synthesis": dict(req="has('evidence synthesis specialist') | (has('research scientist') & (yrs_career >= 5))",
                               rate=0.03, weight="practice"),
    "supervising researchers": dict(req="(has('research scientist') & (yrs_career >= 5)) | has('research facility lead') | "
                                        "has('research project lead')", rate=0.08, weight="practice"),
    "credit negotiation": dict(req="has('research assistant') | has('research scientist') | has('research project lead')",
                               rate=0.02, weight="colors"),
    "community listening": dict(req="has('community observer') | has('volunteer research organiser') | "
                                    "has('participatory research coordinator')", rate=0.05, weight="practice"),
    "grant writing": dict(req="has('research scientist') & (yrs_career >= 2)", rate=0.1, weight="practice"),
    "project triage": dict(req="has('research project lead') | has('research group leader')", rate=0.08),
    "explaining science": dict(req="has('science communication specialist') | ((has('research scientist') | "
                                   "has('citizen scientist')) & has('public speaking'))", rate=0.04, weight="practice"),
    "research integrity": dict(req="(has('research scientist') | has('research assistant')) & mk('owned up') & "
                                   "~mk('hid a wrong')", rate=0.05),
    "automating analysis": dict(req="has('writing code') & (has('research software engineer') | has('research scientist'))",
                                rate=0.1, weight="practice"),
    "a nose for the odd result": dict(req="has('fieldwork') | has('lab work') | has('citizen scientist')", rate=0.002,
                                      weight="colors"),
    # access
    "institutional affiliation": dict(req="has('research assistant') | has('research scientist') | "
                                          "has('research project lead') | has('research group leader') | "
                                          "has('research facility lead') | has('research software engineer') | "
                                          "has('research data steward') | has('laboratory technician')", rate=1.0,
                                      lose="~held_career", lrate=1.0, lwhy="the post ended"),
    "ethics approval": dict(req="has('institutional affiliation') & has('a research project under way')", rate=0.5,
                            lose="~has('a research project under way')", lrate=1.0, lwhy="the study over"),
    "field permit": dict(req="has('a research project under way') & has('fieldwork')", rate=0.5,
                         lose="~has('a research project under way')", lrate=1.0, lwhy="the season over"),
    "instrument time": dict(req="has('institutional affiliation') & has('a research project under way') & has('lab work')",
                            rate=0.4, lose="yrs_has('instrument time') >= 1", lrate=0.8, lwhy="the booking over"),
    "a research project under way": dict(req="has('research grant') | has('research project lead') | "
                                             "has('independent investigator') | has('volunteer research organiser')",
                                         rate=0.3, lose="yrs_has('a research project under way') >= 3", lrate=0.6,
                                         lwhy="the project closed"),
    # standing and bonds
    "a dataset others use": dict(req="has('reproducible workflow') & (yrs_career >= 5)", rate=0.02),
    "a finding that held up": dict(req="has('published research') & has('research integrity')", rate=0.01),
    "a method others use": dict(req="has('experimental design') | has('automating analysis') | "
                                    "has('instrument troubleshooting')", rate=0.004),
    "research collaborators": dict(req="has('research scientist') | has('research project lead')", rate=0.05,
                                   weight="ties"),
    "former students": dict(req="has('supervising researchers') & (yrs_has('supervising researchers') >= 5)", rate=0.05),
    "community partners": dict(req="has('community listening') & (has('participatory research coordinator') | "
                                   "has('volunteer research organiser'))", rate=0.15, weight="ties"),
    "a loyal research team": dict(req="(has('research group leader') | has('research project lead')) & (yrs_career >= 4)",
                                  rate=0.05, weight="ties"),
}

# Shared core (chroma-packs/core/reach.py)
ROLES_REACH = {
    "known across the country": dict(req="has('name in the field') | has('following online') | has('good name in town')",
                                     rate=0.003, weight="colors"),
    "a household name": dict(req="yrs_has('known across the country') >= 3", rate=0.0003),
}

# Additions to rules the pack does not own (as EXTEND_POLITICS in politics/roles.py): a string is or-ed into the rule's
# req at that rule's own rate; a dict is a separate route at its own yearly rate, which the engine's rate fit (ROLE_NORM)
# leaves as written. The base [research grant] (earth_rules.ROLES: age 23 or more and a doctorate, or a museum, archive
# or conservation post; rate .0025) can also come to a [research scientist] or a [postdoctoral researcher], since most
# simulated scientists hold no doctorate (calibration.md, engine issue 7). Round 2 (2026-10-06): the grant, [published
# research] and [lab work] come with the research jobs at their own rates, so the ladder's next steps (project lead,
# group leader, professor) open for those who hold the rung below.
EXTEND_SCIENCE = {
    "research grant": dict(req="has('research scientist') | has('postdoctoral researcher')", rate=0.18),
    "published research": dict(req="has('research scientist') | has('postdoctoral researcher') | "
                                     "has('research project lead') | has('research group leader') | "
                                     "has('independent investigator')", rate=0.3),
    "lab work": dict(req="has('research assistant') | has('research scientist')", rate=0.08),
    # the research road into Politics' [policy analyst] (packs thread, round 3: the Politics rule names only its own and
    # base titles, so it loads on its own); or-ed into that rule at its own rate, a graduate with two years in research
    "policy analyst": "has('graduate') & ((yrs_has('research assistant') >= 2) | (yrs_has('research scientist') >= 2))",
}

# Fit targets (round 2, 2026-10-06). Emren's budget (pack ideas thread, 08:11): across all packs together about 1 life
# in 3 holds a pack career at some point and about 1 in 20 reaches a summit. A tier word puts a title in that budget
# (the engine, batch._targets and earth_rules.BUDGET, 08:21): "career" titles share one multiplier, "summit" titles
# split the summit budget by the square root of their real share, "community" titles go to 10x their real share, at most
# .25 of lives. One fitted lift per tier (earth_rules.TIER_LIFT) moves a whole tier: under budget it raises the
# background rules of its careers and summits (their norm is exp(lift), not ROLE_NORM) and leaves the written chance as
# written; over budget it also lowers the odds of every act that gives one. The rates here keep the titles of a tier at
# a similar multiple of their real share, so one lift moves them together. Community titles and perks keep ROLE_NORM.
# The catalogue keeps the real shares. A number is a perk's own multiplier, given only where a pathway needs the perk to
# follow its holders: [community listening] opens the participatory coordinator's door, and the reach ladder
# (core/reach.py) opens the top of politics.
TARGET_SCIENCE = {
    "research assistant": "career", "research scientist": "career", "research project lead": "career",
    "research software engineer": "career", "research data steward": "career", "evidence synthesis specialist": "career",
    "science communication specialist": "career", "participatory research coordinator": "career",
    "postdoctoral researcher": "career",
    "research group leader": "summit", "research facility lead": "summit", "professor": "summit",
    "independent investigator": "summit",
    "citizen scientist": "community", "community observer": "community", "volunteer research organiser": "community",
    "community listening": 5, "known across the country": 6, "a household name": 6,
}
