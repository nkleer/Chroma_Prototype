# Chroma content pack: National standing. The engine's reading of how each seat and route asset comes and goes,
# proposed in earth_rules.ROLES syntax (chroma-engine/v22-speedpass/earth_rules.py, "ROLES = {"). Plain data for the
# Engine, which owns the rules and refits every rate. Condition words are the engine's own (batch.COND_VOCAB): has('x'),
# was('x'), yrs_has('x'), mk('mark'), age, money. Rules are checked every four weeks.
#
# SWITCHED OFF: nothing reads this file until the Engine adds `national` to batch.PACKS, with `callings` (DEPENDS in
# catalogue.py).
#
# The seats. Each req is the route's "wider" step (Outer world's world_fit.json "national", climb.who): years in the
# titles the seat refines, as roles.py's summits ask (five or more at the Known rung, fewer from a summit), and one of
# the route's ways of being known beyond the town: a good name in the field, the route's own asset, or the shared
# reach ladder ([known across the country]), never the reach alone. The background rate, .0015 a check (about .02 a
# year), is the Engine's NATIONAL_CLIMB base (other-shapes.md section 5): with `wa_nat_climb` on, the climb gives the
# same chance (times 1.5 with an aim for the route) and only to a free seat, so the Engine reads one of the two, never
# both. Most seats come by the player's act at a route's moments (the Library's encounters), whose option chances carry
# the real odds. Each seat ends as its catalogue lost= says: a term, a vote, a scandal (the mark [hid a wrong]) or age,
# and never after its catalogue ages (C-X4). A seat gives no recognition (decision #11: the three are kept apart), so
# there is no EXTEND onto [known across the country].
#
# The assets. Fifteen, one per route (catalogue.py). Five are the seats' own (odds 0: they come only by these rules);
# the standings and bonds also come by a moment's grant (odds .05). Each is kept while its obligation is kept: lose=
# names the broken obligation, or the years away from the work that carries it, at a slow rate where it fades.

ROLES_NATIONAL = {
    # ------------------------------------------------ the ten new seats (standing 3)
    # W, Common-Ground Maker
    "head of a national faith body": dict(refines="head of a faith order; senior cleric",
                                          rungs=["head of a faith order", "senior cleric"],
                                          req="(age >= 45) & ((yrs_has('head of a faith order') >= 3) | "
                                              "(yrs_has('senior cleric') >= 10)) & "
                                              "(has('standing with both sides') | has('a flock that follows you') | "
                                              "has('mediator') | has('known across the country'))",
                                          rate=0.0015, weight="colors",
                                          lose=[("yrs_has('head of a national faith body') >= 7", "the term ended"),
                                                ("mk('hid a wrong')", "a split in the faith, over what was hidden"),
                                                ("age >= 88", "stepped down in old age")],
                                          lrate=0.08),
    # U, Discoverer
    "chief scientist": dict(refines="professor; research group leader; research facility lead",
                            rungs=["professor", "research group leader", "research facility lead"],
                            req="(age >= 45) & ((yrs_has('professor') >= 5) | (yrs_has('research group leader') >= 5) | "
                                "(yrs_has('research facility lead') >= 5)) & "
                                "(has('name in the field') | has('a finding that held up') | "
                                "has('a finding and its method') | has('known across the country'))",
                            rate=0.0015, weight="colors",
                            lose=[("yrs_has('chief scientist') >= 5", "the appointment ended"),
                                  ("mk('hid a wrong')", "a quarrel with the government in public"),
                                  ("age >= 74", "retired")],
                            lrate=0.1),
    # U, Systems Inventor
    "director of a national laboratory": dict(refines="research facility lead; research group leader; celebrated inventor",
                                              rungs=["research facility lead", "research group leader",
                                                     "celebrated inventor"],
                                              req="(age >= 40) & ((yrs_has('research facility lead') >= 5) | "
                                                  "(yrs_has('research group leader') >= 8) | "
                                                  "(yrs_has('celebrated inventor') >= 3)) & "
                                                  "(has('name in the field') | has('an invention in everyday use') | "
                                                  "has('a working national system') | "
                                                  "has('known across the country'))",
                                              rate=0.0015, weight="colors",
                                              lose=[("yrs_has('director of a national laboratory') >= 8",
                                                     "the term ended"),
                                                    ("age >= 74", "retired")],
                                              lrate=0.08),
    # U, Truthfinder
    "editor of a national paper": dict(refines="journalist", rungs=["journalist"],
                                       req="(age >= 35) & (yrs_has('journalist') >= 10) & "
                                           "(has('source who trusts you') | has('name in the field') | "
                                           "has('a record and its sources') | has('known across the country'))",
                                       rate=0.0015, weight="colors",
                                       lose=[("yrs_has('editor of a national paper') >= 6", "the owners' displeasure"),
                                             ("mk('hid a wrong')", "a story that proved wrong"),
                                             ("age >= 74", "retired")],
                                       lrate=0.08),
    # B, Coalition Builder
    "head of a national industry body": dict(refines="chief executive; founder of a firm; celebrated inventor",
                                             rungs=["chief executive", "founder of a firm", "celebrated inventor"],
                                             req="(age >= 40) & ((yrs_has('chief executive') >= 5) | "
                                                 "(yrs_has('founder of a firm') >= 10) | "
                                                 "(yrs_has('celebrated inventor') >= 5)) & "
                                                 "(has('a seat on boards') | has('investors who back you') | "
                                                 "has('the voice of a whole industry') | "
                                                 "has('known across the country'))",
                                             rate=0.0015, weight="colors",
                                             lose=[("yrs_has('head of a national industry body') >= 6",
                                                    "the members' vote"),
                                                   ("age >= 79", "retired")],
                                             lrate=0.08),
    # B, Opportunity Patron
    "head of a national bank or exchange": dict(refines="chief executive; accountant",
                                                rungs=["chief executive", "accountant"],
                                                req="(age >= 40) & ((yrs_has('chief executive') >= 5) | "
                                                    "(yrs_has('accountant') >= 15)) & "
                                                    "(has('a seat on boards') | has('a portfolio of people backed'))",
                                                rate=0.0015, weight="colors",
                                                lose=[("yrs_has('head of a national bank or exchange') >= 7",
                                                       "a vote of the board or the government"),
                                                      ("age >= 79", "retired")],
                                                lrate=0.08),
    # R, National Virtuoso: held for life in name; it fades only when the work stops
    "celebrated star of stage or sport": dict(refines="lead actor or actress; professional athlete; touring musician",
                                              rungs=["lead actor or actress", "professional athlete",
                                                     "touring musician"],
                                              req="(age >= 18) & ((yrs_has('lead actor or actress') >= 5) | "
                                                  "(yrs_has('professional athlete') >= 4) | "
                                                  "(yrs_has('touring musician') >= 5)) & "
                                                  "(has('a lead role to remember') | has('known across the country') | "
                                                  "has('a household name'))",
                                              rate=0.0015, weight="colors",
                                              lose="~has('lead actor or actress') & ~has('professional athlete') & "
                                                   "~has('touring musician') & (age >= 40)",
                                              lrate=0.01, lwhy="the work stopped, and the fame faded"),
    # G, Living-Land Steward
    "head of the national parks": dict(refines="park ranger; forester", rungs=["park ranger", "forester"],
                                       req="(age >= 35) & ((yrs_has('park ranger') >= 10) | "
                                           "(yrs_has('forester') >= 10)) & "
                                           "(has('good name in town') | has('a stretch of land kept alive') | "
                                           "has('known across the country'))",
                                       rate=0.0015, weight="colors",
                                       lose=[("yrs_has('head of the national parks') >= 8", "the term ended"),
                                             ("age >= 74", "retired")],
                                       lrate=0.08),
    # G, Living-Heritage Keeper
    "keeper of the national heritage": dict(refines="museum curator; archivist; master craftsperson; folk musician",
                                            rungs=["museum curator", "archivist", "master craftsperson",
                                                   "folk musician"],
                                            req="(age >= 40) & ((yrs_has('museum curator') >= 10) | "
                                                "(yrs_has('archivist') >= 10) | "
                                                "(yrs_has('master craftsperson') >= 10) | "
                                                "(yrs_has('folk musician') >= 15)) & "
                                                "(has('name in the field') | has('a living tradition kept') | "
                                                "has('known across the country'))",
                                            rate=0.0015, weight="colors",
                                            lose=[("yrs_has('keeper of the national heritage') >= 10", "stepped down"),
                                                  ("age >= 88", "retired")],
                                            lrate=0.08),
    # G, Community Weaver
    "head of a national charity": dict(refines="community centre manager; community-garden coordinator; renowned healer",
                                       rungs=["community centre manager", "community-garden coordinator",
                                              "renowned healer"],
                                       req="(age >= 35) & ((yrs_has('community centre manager') >= 8) | "
                                           "(yrs_has('community-garden coordinator') >= 10) | "
                                           "(yrs_has('renowned healer') >= 3)) & "
                                           "(has('good name in town') | has('a web of groups that help each other') | "
                                           "has('known across the country'))",
                                       rate=0.0015, weight="colors",
                                       lose=[("yrs_has('head of a national charity') >= 8", "stepped down"),
                                             ("mk('hid a wrong')", "a scandal"),
                                             ("age >= 84", "retired")],
                                       lrate=0.08),
    # ------------------------------------------------ the fifteen assets (one per route)
    # W
    "a standing mandate": dict(req="has('head of government') | (has('party leader') & has('known across the country'))",
                               rate=0.03, weight="colors",
                               lose=[("mk('broke your word')", "the promise broken"),
                                     ("~has('head of government') & ~has('party leader')", "the years after office")],
                               lrate=0.01),
    "a working public service": dict(req="yrs_has('minister') >= 2", rate=0.02, weight="colors",
                                     lose="~has('minister')", lrate=0.004,
                                     lwhy="a later government closed it; the name stays"),
    "standing with both sides": dict(req="(yrs_has('mediator') >= 3) | (yrs_has('head of a faith order') >= 3) | "
                                         "has('head of a national faith body')",
                                     rate=0.01, weight="colors",
                                     lose="mk('hid a wrong')", lrate=0.2, lwhy="took one side in public"),
    # U
    "a finding and its method": dict(req="has('chief scientist') | (has('published research') & "
                                         "has('a finding that held up'))",
                                     rate=0.01, weight="colors",
                                     lose="mk('hid a wrong')", lrate=0.2,
                                     lwhy="a result found wrong and not corrected in public"),
    "a working national system": dict(req="(yrs_has('director of a national laboratory') >= 2) | "
                                          "(yrs_has('celebrated inventor') >= 3)",
                                      rate=0.01, weight="colors",
                                      lose="~has('director of a national laboratory') & ~has('celebrated inventor')",
                                      lrate=0.004, lwhy="a newer system replaced it"),
    "a record and its sources": dict(req="has('editor of a national paper') | ((yrs_has('journalist') >= 8) & "
                                         "has('source who trusts you'))",
                                     rate=0.01, weight="colors",
                                     lose=[("mk('hid a wrong')", "a story printed that was not true"),
                                           ("~has('journalist') & ~has('editor of a national paper')",
                                            "years away from the news")],
                                     lrate=0.02),
    # B
    "the voice of a whole industry": dict(req="yrs_has('head of a national industry body') >= 2", rate=0.03,
                                          weight="colors",
                                          lose="~has('head of a national industry body') & ~has('chief executive')",
                                          lrate=0.01, lwhy="years out of the industry"),
    "a firm and its people": dict(req="(yrs_has('magnate') >= 3) | (yrs_has('chief executive') >= 8)", rate=0.01,
                                  weight="colors",
                                  lose="~has('magnate') & ~has('chief executive')", lrate=0.01,
                                  lwhy="the firm broken up, or its people let go"),
    "a portfolio of people backed": dict(req="(yrs_has('head of a national bank or exchange') >= 2) | "
                                             "(has('investors who back you') & (money > .5))",
                                         rate=0.01, weight="colors",
                                         lose="money < .05", lrate=0.2, lwhy="a crash"),
    # R
    "a following that turns out": dict(req="(yrs_has('party leader') >= 2) | (has('a following in the party') & "
                                           "has('rousing a crowd'))",
                                       rate=0.01, weight="colors",
                                       lose="~has('party leader') & ~has('a following in the party')", lrate=0.01,
                                       lwhy="years out of the fight"),
    "a unit that trusts its leader": dict(req="(yrs_has('general') >= 2) | ((yrs_has('army officer') >= 8) & "
                                              "has('leading soldiers'))",
                                          rate=0.01, weight="colors",
                                          lose="~has('general') & ~has('army officer')", lrate=0.01,
                                          lwhy="years out of uniform"),
    "a signature work and its audience": dict(req="yrs_has('celebrated star of stage or sport') >= 1", rate=0.03,
                                              weight="colors",
                                              lose="~has('celebrated star of stage or sport')", lrate=0.004,
                                              lwhy="it faded from view when the work stopped; the work stays"),
    # G
    "a living tradition kept": dict(req="(yrs_has('keeper of the national heritage') >= 2) | "
                                        "(yrs_has('master craftsperson') >= 15) | (yrs_has('folk musician') >= 20)",
                                    rate=0.01, weight="colors",
                                    lose="~has('keeper of the national heritage') & ~has('master craftsperson') & "
                                         "~has('folk musician')",
                                    lrate=0.004, lwhy="no one learned the old ways from them"),
    "a web of groups that help each other": dict(req="(yrs_has('head of a national charity') >= 2) | "
                                                     "(yrs_has('community centre manager') >= 10)",
                                                 rate=0.01, weight="colors",
                                                 lose="~has('head of a national charity') & "
                                                      "~has('community centre manager')",
                                                 lrate=0.004, lwhy="the branches drifted apart"),
    "a stretch of land kept alive": dict(req="(yrs_has('head of the national parks') >= 2) | "
                                             "(yrs_has('park ranger') >= 12) | (yrs_has('forester') >= 12)",
                                         rate=0.01, weight="colors",
                                         lose="~has('head of the national parks') & ~has('park ranger') & "
                                              "~has('forester')",
                                         lrate=0.004, lwhy="the keepers gone"),
}

# More ways into rules the pack does not own: none. A seat gives no recognition (decision #11), and the reach ladder's
# own rules (core/reach.py, EXTEND in the other packs) already take a summit to [known across the country].
EXTEND_NATIONAL = {}

# Fit targets (batch._targets): the seats are summits, the only fitting tier word the engine reads for them today
# (batch.TIERS). Release's WA7 judges national standing of any kind (the fifteen seats, recognition and influence) at
# .01 to .03 of lives left alone (world_fit.json "national", targets), so the ten new seats belong under one lift of
# their own, not each at the summit floor (ten summits at 1 in 100 would put a tenth of lives in a national seat):
# a proposal for the Engine, a "national" tier fitted with the climb, which this table then names. The five seats that
# exist keep their own tiers. The seats' assets keep the 10x multiple of the perks of the Known rungs and summits
# (callings/roles.py, TARGET_CALLINGS).
TARGET_NATIONAL = {
    "head of a national faith body": "summit", "chief scientist": "summit",
    "director of a national laboratory": "summit", "editor of a national paper": "summit",
    "head of a national industry body": "summit", "head of a national bank or exchange": "summit",
    "celebrated star of stage or sport": "summit", "head of the national parks": "summit",
    "keeper of the national heritage": "summit", "head of a national charity": "summit",
    "a standing mandate": 10, "a working public service": 10, "standing with both sides": 10,
    "a finding and its method": 10, "a working national system": 10, "a record and its sources": 10,
    "the voice of a whole industry": 10, "a firm and its people": 10, "a portfolio of people backed": 10,
    "a following that turns out": 10, "a unit that trusts its leader": 10, "a signature work and its audience": 10,
    "a living tradition kept": 10, "a web of groups that help each other": 10, "a stretch of land kept alive": 10,
}
