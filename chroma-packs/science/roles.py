# Chroma content pack: Science, Research and Discovery. The engine's reading of how each title and perk comes and goes,
# proposed in earth_rules.ROLES syntax (chroma-engine/prototype/earth_rules.py, "ROLES = {"). Plain data for the engine
# thread, which owns the rules and refits every rate to the catalogue's shares (ROLE_NORM). Condition words are the ones
# the engine has today: has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark') >= n, had(['situation'], years), age,
# money, health, held_career, yrs_career, and the like.
#
# In this pack most first steps are taken by the player's own act at a door (title: on an option in the pack's
# moments), so the background rates below are low: they stand for the ordinary lives that drift into research without
# a door moment, and the engine fits them so the simulated shares match the catalogue.

# Round 5, 2026-10-07 (release round, checklist rows P1, P2, P4, P5, P7, P12): every career and summit rule names in its
# req only titles in its after= or rungs= (or the title it refines), so the engine's "from nothing" check can verify each
# step (Emren 09:18); careers and summits lean to their colors in who takes the step (weight="colors": the title's ways
# and profiles in catalogue.py, the road per color of Emren's card 10:47); and the rates below are set where a road was
# out of reach (facility lead, postdoc, independent investigator) or over three times its target (science
# communication, project lead, evidence synthesis, research scientist, professor). Community titles stay open to anyone.
ROLES_SCIENCE = {
    # careers: entries
    "research assistant": dict(req="((has('graduate') & (has('lab work') | has('finding things out') | "
                                   "has('working with data'))) | (yrs_has('citizen scientist') >= 2) | "
                                   "(yrs_has('community observer') >= 2)) & (age <= 33)",   # a science degree, or years
                               after=["citizen scientist", "community observer"], rungs=["graduate"],   # the degree is a
                               rate=0.01, entry=True, weight="colors"),   # rung kept on the step (engine rungs=, 11:30)
    # careers: rungs
    # Round 5: the degrees its req names are rungs (kept on the step); .09 -> .06, since the doctorate route (EXTEND below)
    # opens it to more assistants and the scientist ran at 2 to 3.3 times its target (t_packs_fit_11b, 12b)
    "research scientist": dict(req="has('doctoral graduate') | (has('graduate') & (was('research assistant') | "
                                   "was('laboratory technician')) & (mkn('learned a skill') >= 4))",
                               after=["research assistant", "laboratory technician", "research data steward",
                                      "research software engineer"], rungs=["graduate", "doctoral graduate"],
                               rate=0.06, entry=True, weight="colors"),
    # Round 5: .6 -> .15 (3.6 times its target on seed 12, still 3.3 times in the round 5 smoke runs, which hold the
    # project lead at .6 of the scientists against about .4 in life; the funding call now comes at its times: rate, P10)
    "research project lead": dict(after=["research scientist", "research software engineer", "research data steward",
                                         "evidence synthesis specialist", "participatory research coordinator"],
                                  req="(yrs_career >= 3) & (has('research grant') | has('a research project under way'))",
                                  rate=0.15, weight="colors"),
    "research group leader": dict(after=["research project lead", "research scientist"],
                                  req="(yrs_career >= 6) & has('research grant') & (has('published research') | "
                                      "has('name in the field'))", rate=0.05, weight="colors",
                                  grants=["supervising researchers"]),
    # Round 5 (P1): the facility head was never reached (0 of 1,000 lives): [instrument troubleshooting] reached 6 lives in
    # 800 and research stints last a median 2.1 to 2.5 years, so eight years in the career with that one skill was almost
    # never met. Now four years in the career and the hands-on skill of the bench ([lab work]) or of the machines
    # ([instrument troubleshooting]); rate .03 -> .05 (the summit lift raises a rung's rate by at most e^1)
    # Round 5, merge (packs thread, 1,600 lives over four seeds): with [lab work] now common among scientists the rule
    # put the facility head at 9.6x its target (64 lives), 60 of them 'in time'; rate .05 -> .005
    "research facility lead": dict(after=["laboratory technician", "research scientist", "research software engineer"],
                                   req="(yrs_career >= 4) & (has('instrument troubleshooting') | has('lab work'))",
                                   rate=0.005, weight="colors"),
    # Round 5 (P4): .48 times its target with the summit lift at its cap; rate .002 -> .004. The long-shot skip of
    # 'a discovery nobody asked you for' starts from a research assistant post or years of volunteer research with a
    # publication (LONGSHOTS-BRIEF, one rung skipped): those rungs are named, so the step can be checked
    "independent investigator": dict(after=["research scientist", "research project lead", "research group leader",
                                            "research data steward"],
                                     rungs=["research assistant", "citizen scientist", "community observer",
                                            "volunteer research organiser"],
                                     req="(has('published research') | has('a finding that held up')) & "
                                         "(has('research grant') | has('savings') | (money > .45))", rate=0.004,
                                     weight="colors"),
    # careers: side roads
    # Round 5 (P7): its req names the research scientist, now a rung below as well
    "research software engineer": dict(req="has('writing code') & ((yrs_has('software developer') >= 2) | "
                                           "(yrs_has('data analyst') >= 2) | was('research assistant') | "
                                           "was('research scientist'))", after=["research assistant", "software developer",
                                                                         "data analyst", "research scientist"],
                                       rate=0.03, entry=True, weight="colors"),
    "research data steward": dict(req="(has('working with data') | has('archive research')) & (was('research assistant') | "
                                      "was('research scientist') | was('laboratory technician') | "
                                      "(yrs_has('data analyst') >= 2) | (yrs_has('archivist') >= 2))",
                                  # Round 5 (P7): the scientist and the technician its req names are rungs below too;
                                  # .02 -> .012 for the wider door
                                  after=["research assistant", "archivist", "data analyst", "research scientist",
                                         "laboratory technician"], rate=0.012, entry=True, weight="colors"),
    # Round 5: the degree is a rung (P7); .02 -> .01 (2.8 times its target over seeds 11 and 12)
    "evidence synthesis specialist": dict(req="has('graduate') & (has('evidence synthesis') | has('finding things out'))",
                                          after=["research scientist", "research assistant"], rungs=["graduate"],
                                          rate=0.01, weight="colors"),
    "science communication specialist": dict(req="has('graduate') & (has('explaining science') | "
                                                 "((has('public speaking') | has('reporting')) & "
                                                 "(was('research scientist') | was('research assistant') | "
                                                 "has('finding things out'))))",
                                             # Round 5 (P5): 21 times its real share in tier_fit4 (4.2 times its
                                             # target) and 4 times on seed 12: rate .015 -> .006; the degree is a rung
                                             after=["research scientist", "research assistant", "journalist", "teacher"],
                                             rungs=["graduate"], rate=0.006, entry=True, weight="colors"),
    # Round 5 (P5, P7): the organiser its req names is a rung kept on the step (rungs=, not after=): the step itself is
    # from a research post. With the organisers in after= (about 1 life in 25), most of them stepped up in time, and the
    # coordinator came to some 25 times its target in the smoke runs; the yearly lift cannot take that back (it moves a
    # rung's rate by e^.5 to e^1 only). A research assistant or scientist who organised volunteers, or who learned
    # [community listening], steps up; rate .03 -> .02
    "participatory research coordinator": dict(req="has('community listening') | was('volunteer research organiser') | "
                                                   "has('community partners') | was('community observer')",   # 10-09 floors (Emren: rare titles reachable): two more roads
                                               after=["research assistant", "research scientist"],
                                               rungs=["volunteer research organiser"], rate=0.02, weight="colors"),
    # community
    "citizen scientist": dict(req="(age >= 12) & (time > .4) & (has('finding things out') | has('knowing the woods'))",
                              rate=0.0001, starts=True, weight="colors",
                              lose="yrs_has('citizen scientist') >= 2", lrate=0.3, lwhy="the season over, and no next one"),
    # Round 5, 2026-10-07 (09:18 check): the community titles stay open to anyone; rungs= (non-gating) only names the
    # titles their req reads, so the engine's "from nothing" report can follow them
    "community observer": dict(req="(age >= 12) & (was('citizen scientist') | has('knowing the woods'))",
                               rungs=["citizen scientist"], rate=0.007, starts=True, weight="practice"),
    # Round 5 (P12): the organiser leans to its profiles (catalogue.py: W B, U R, G), on the Green road
    "volunteer research organiser": dict(rungs=["citizen scientist", "community observer"],
                                         req="(was('citizen scientist') | was('community observer')) & "
                                             "(has('organising people') | mk('helped someone in need'))", rate=0.003,
                                         weight="colors"),
    # facets (colorless appointments)
    # Round 5 (P7): the doctorate its req names is a rung (P2: the doctorate on the research road is EXTEND below)
    "postdoctoral researcher": dict(refines="research scientist", rungs=["doctoral graduate"],
                                    req="has('research scientist') & was('doctoral graduate') & "
                                        "(yrs_has('research scientist') <= 3)", rate=0.6,
                                    lose="yrs_has('postdoctoral researcher') >= 5", lrate=0.5,
                                    lwhy="the fixed-term years over"),
    # Round 5: the project lead its req names is a rung (P7); rate .12 -> .06 (3.1 times its target on seed 12, all of it
    # "in time"); the chair is now also offered by the moments of the rung below (P16) and has a long shot (P9)
    "professor": dict(refines="research scientist; research group leader", rungs=["research project lead"],
                      req="(has('research group leader') | (has('research scientist') & was('research project lead'))) & "   # a rung below (09:18)
                          "(yrs_career >= 10) & "
                          "(has('name in the field') | has('published research'))", rate=0.06),
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
    "field permit": dict(req="has('fieldwork')", rate=0.5,   # 10-09 floors (Emren: rare titles reachable): fieldwork alone, no project asked
                         lose="yrs_has('field permit') >= 1", lrate=1.0, lwhy="the season over"),
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
# Round 5, 2026-10-07 (P2): the research road's own doctorate. Doctorates were rare (9 lives in 800, 6 of them research
# scientists), so the postdoc facet, which needs one within the first three years as a scientist, came to 0.1 of its
# target. A doctorate taken while employed on a project: a graduate with two years or more as a research assistant, or
# in the first three years as a research scientist, completes one at about 1 in 5 a year (doctorates take three to
# five years, and in much of Europe the doctoral candidate is the project's employed researcher). A route of its own,
# which ROLE_NORM leaves as written; [doctoral graduate] has its own number in TARGET_SCIENCE below, so the fit does not
# crush the base route to make room for it. The grant .18 -> .1: the funding call now comes at its times: rate (P10).
EXTEND_SCIENCE = {
    "doctoral graduate": dict(req="has('graduate') & (age <= 45) & ((yrs_has('research assistant') >= 2) | "
                                  "((yrs_has('research scientist') >= 1) & (yrs_has('research scientist') <= 3)))",
                              rate=0.2),
    "research grant": dict(req="has('research scientist') | has('postdoctoral researcher')", rate=0.1),
    "published research": dict(req="has('research scientist') | has('postdoctoral researcher') | "
                                     "has('research project lead') | has('research group leader') | "
                                     "has('independent investigator')", rate=0.3),
    # Round 5 (P1): the technician's bench too, as the base catalogue says ([lab work] is gained "at a bench as a
    # [laboratory technician]"); the base rule is fitted near zero, so technicians never held it and the facility road,
    # which needs the hands-on skill, was closed to them
    "lab work": dict(req="has('research assistant') | has('research scientist') | has('laboratory technician')",
                     rate=0.08),
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
    # Round 5 (P2): the doctorate feeds the pack's careers (the scientist, the postdoc), as [parliamentary nomination] feeds
    # the seat in Politics: 4 times its real share (about .04 of lives: the base 1 in 100 and the research road's own,
    # with research scientists at their career multiple and about half of them holding one, as real postdocs do)
    "doctoral graduate": 4,
}
