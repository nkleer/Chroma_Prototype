# Chroma content pack: Art and Writing. The engine's reading of how each title and perk comes and goes, proposed in
# earth_rules.ROLES syntax (chroma-engine/v22-speedpass/earth_rules.py, "ROLES = {"). Plain data for the Engine, which
# owns the rules and refits every rate (ROLE_NORM, and the tier lift for careers and summits). Condition words are the
# engine's own (batch.COND_VOCAB): has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark'), age, money, time,
# yrs_career. A name with an apostrophe is written in double quotes inside the condition.
#
# As in Stage and Screen (../stage/roles.py), most steps are taken by the player's own act at a door or a crossing
# (title: on an option in the pack's moments), so the background rates are low and every req is narrow: the pathway's
# own earlier title, or years on it, never a perk alone (Emren 10-06 09:18, "never from nothing"). Every career and
# summit lists its rungs below in rungs= (round 5's rule, P8): rungs=, not after=, so the was() roads (the student who
# graduated, the class given up) stay open. Rules are checked every four weeks, so odds belong in rate, never in a
# chance() inside req.

ROLES_ART = {
    # community: the taste rung, held beside a day job
    "open-mic poet": dict(req="(age >= 15) & (has('writing poems') | has('writing stories'))",
                          rate=0.002, starts=True, weight="colors",
                          lose="yrs_has('open-mic poet') >= 3", lrate=0.15,
                          lwhy="no time for the poetry nights any more"),
    "life-drawing regular": dict(req="(age >= 16) & has('drawing and painting')",
                                 rate=0.001, starts=True, weight="colors",
                                 lose="yrs_has('life-drawing regular') >= 3", lrate=0.12,
                                 lwhy="the class moved, and life got busy"),
    # status: three years at art school (lasts=3 in the catalogue)
    "art school student": dict(req="(age >= 17) & (age <= 30) & has('drawing and painting') & "
                                   "(was('life-drawing regular') | (age <= 19))",
                               rate=0.002, weight="colors"),
    # careers: the practice rung (entry careers, the red road's first paid work)
    "street artist": dict(req="(age >= 16) & has('drawing and painting') & (was('life-drawing regular') | "
                              "was('art school student'))",
                          rungs=["life-drawing regular", "art school student"],
                          rate=0.002, starts=True, entry=True, weight="colors",
                          lose="yrs_has('street artist') >= 3", lrate=0.15,
                          lwhy="the commissions dried up, and the day job took over"),
    "illustrator for hire": dict(req="(has('illustration') | has('drawing and painting')) & "
                                     "(was('art school student') | (yrs_has('life-drawing regular') >= 2))",
                                 rungs=["art school student", "life-drawing regular"],
                                 rate=0.003, starts=True, entry=True, weight="colors",
                                 lose="yrs_has('illustrator for hire') >= 3", lrate=0.08,
                                 lwhy="the work dried up, and a steady job took its place"),
    # careers: the profession and the side roads (one per colour; the catalogue's profiles)
    "painter or sculptor": dict(req="(has('drawing and painting') | has('sculpting')) & (was('art school student') | "
                                    "(yrs_has('life-drawing regular') >= 4) | (yrs_has('street artist') >= 2) | "
                                    "(yrs_has('illustrator for hire') >= 3))",
                                rungs=["art school student", "life-drawing regular", "street artist",
                                       "illustrator for hire"],
                                rate=0.002, starts=True, entry=True, weight="colors",
                                lose="yrs_has('painter or sculptor') >= 3", lrate=0.08,
                                lwhy="the work stopped selling, and another job took over"),
    "art teacher": dict(req="has('art school degree') | (has('teacher') & (yrs_has('teacher') >= 2) & "
                            "(has('drawing and painting') | was('life-drawing regular')))",
                        rungs=["art school student", "teacher", "life-drawing regular"],
                        rate=0.004, entry=True, weight="colors"),
    "gallery owner": dict(req="(has('savings') | has('patron')) & ((yrs_has('painter or sculptor') >= 3) | "
                              "(yrs_has('art teacher') >= 5) | (yrs_has('shop owner') >= 3) | "
                              "(yrs_has('museum curator') >= 3) | (yrs_has('illustrator for hire') >= 5))",
                          rungs=["painter or sculptor", "art teacher", "shop owner", "museum curator",
                                 "illustrator for hire"],
                          rate=0.002, entry=True, weight="colors",
                          lose="yrs_has('gallery owner') >= 3", lrate=0.08, lwhy="the rent rose and the sales did not"),
    "master craftsperson": dict(req="(yrs_has('craft maker') >= 5) | ((yrs_has('carpenter') >= 8) & "
                                    "has(\"a maker's hallmark\"))",
                                rungs=["craft maker", "carpenter"], rate=0.004, entry=True, weight="colors"),
    # summits: facets on the career held (as [lead actor or actress]); they stay once won
    "renowned artist": dict(refines="painter or sculptor; street artist; illustrator for hire; master craftsperson",
                            rungs=["life-drawing regular", "art school student"],
                            req="(has('painter or sculptor') | has('street artist') | has('illustrator for hire') | "
                                "has('master craftsperson')) & (yrs_career >= 5) & (has('a name in the art world') | "
                                "has('a dealer who sells your work') | has(\"works in collectors' hands\") | "
                                "has('a mural the town loves') | has('patron'))",
                            rate=0.004, weight="colors", grants=["works in collectors' hands"]),
    "celebrated author": dict(refines="novelist", rungs=["open-mic poet"],
                              req="has('novelist') & (yrs_has('novelist') >= 3) & has('book in print') & "
                                  "(has('a publishing contract') | has('a prize for writing') | has('following online'))",
                              rate=0.004, weight="colors", grants=["a prize for writing"]),
    # skills: learned on the rung (rates per year while it is held)
    "writing poems": dict(req="has('open-mic poet') | has('novelist') | (has('writing stories') & (age >= 12))",
                          rate=0.05, weight="practice"),
    "illustration": dict(req="has('illustrator for hire') | has('art school student')", rate=0.2, weight="practice"),
    "sculpting": dict(req="has('art school student') | has('painter or sculptor') | has('master craftsperson') | "
                          "(has('craft maker') & (yrs_has('craft maker') >= 2))", rate=0.08, weight="practice"),
    # credentials
    "art school degree": dict(req="was('art school student') & ~has('art school student')", rate=0.9),
    "a publishing contract": dict(req="has('novelist') | has('illustrator for hire') | "
                                      "(yrs_has('open-mic poet') >= 3)", rate=0.02,
                                  lose="~has('novelist') & ~has('illustrator for hire') & "
                                       "(yrs_has('a publishing contract') >= 3)", lrate=0.1,
                                  lwhy="the books stopped selling, and the publisher let the contract go"),
    "a maker's hallmark": dict(req="(yrs_has('craft maker') >= 4) | has('master craftsperson')", rate=0.05),
    # standing
    "a name in the art world": dict(req="has('painter or sculptor') | has('street artist') | has('renowned artist') | "
                                        "has('gallery owner')", rate=0.03, weight="colors"),
    "a prize for writing": dict(req="has('novelist') | (yrs_has('open-mic poet') >= 2) | has('celebrated author')",
                                rate=0.01),
    "a mural the town loves": dict(req="has('street artist') | (has('art teacher') & (yrs_has('art teacher') >= 2))",
                                   rate=0.04),
    # bonds
    "pupils who remember you": dict(req="(yrs_has('art teacher') >= 3) | (yrs_has('master craftsperson') >= 3)",
                                    rate=0.1),
    "a dealer who sells your work": dict(req="has('painter or sculptor') | has('renowned artist') | "
                                             "(has('master craftsperson') & has(\"a maker's hallmark\"))", rate=0.03),
    "a circle of artists": dict(req="has('life-drawing regular') | has('open-mic poet') | has('art school student') | "
                                    "has('street artist')", rate=0.08),
    # assets
    "a body of work": dict(req="(yrs_has('painter or sculptor') >= 8) | (yrs_has('illustrator for hire') >= 10) | "
                               "(yrs_has('master craftsperson') >= 8) | (yrs_has('novelist') >= 10)", rate=0.2),
    "works in collectors' hands": dict(req="has('a dealer who sells your work') | has('renowned artist') | "
                                           "(yrs_has('master craftsperson') >= 3)", rate=0.05),
    "royalties": dict(req="has('a publishing contract') | (yrs_has('illustrator for hire') >= 5)", rate=0.03),
}

# More ways into rules the pack does not own (or-ed onto the base rule, at the rule's own rate).
EXTEND_ART = {
    # a poet of three years with a book of poems in print is a writer of books: the base [novelist] stands for both
    "novelist": "(yrs_has('open-mic poet') >= 3) & has('writing poems') & has('book in print')",
    "book in print": "has('a publishing contract')",
    "studio of one's own": "(has('painter or sculptor') | has('renowned artist')) & (money > .2)",
    "known across the country": "has('renowned artist') | has('celebrated author')",
    "patron": "has('renowned artist') | (has('painter or sculptor') & has('a name in the art world'))",
    "teaching": "has('art teacher')",
    "cleared to work with children": "(age >= 18) & ~has('someone with a record') & has('art teacher')",
}

# Fit targets (batch._targets; Emren's one budget for all packs): a tier word per title, as TARGET_STAGE. The engine
# fits one lift per tier, so the loaded packs together give about 1 life in 3 a career and about 1 in 20 a summit
# (earth_rules.BUDGET); with the floors on (batch.FLOORS, v22.3) each pack career reaches 1.5 lives in 100 and each
# summit 1 in 100 (BUDGET_FLOORS). Perks keep a multiple (ROLE_NORM), as in the other packs: 10x for the perks of the
# careers, 3x to 4x for the taste rung's.
TARGET_ART = {
    # careers
    "street artist": "career", "illustrator for hire": "career", "painter or sculptor": "career",
    "art teacher": "career", "gallery owner": "career", "master craftsperson": "career",
    # The writing road's career rung is the base [novelist] (real share .0005), and [celebrated author] can only sit on
    # it. A tier word here would put [novelist] under the pack careers' lift on its broad base rule: a scratch run on
    # 10-10 (300 lives) gave it to 57 lives in 100. A multiple keeps it under ROLE_NORM at 60 times its share (about 3
    # lives in 100, the Engine's choice of 10-10), so about a third of novelists can reach the summit floor of 1 in 100.
    "novelist": 60,
    # summits
    "renowned artist": "summit", "celebrated author": "summit",
    # community and status
    "open-mic poet": "community", "life-drawing regular": "community", "art school student": "community",
    # perks of the careers
    "illustration": 10, "sculpting": 10, "a publishing contract": 10, "a maker's hallmark": 10,
    "a name in the art world": 10, "a prize for writing": 10, "a mural the town loves": 10,
    "pupils who remember you": 10, "a dealer who sells your work": 10, "a body of work": 10,
    "works in collectors' hands": 10, "royalties": 10,
    # perks of the taste rung and the school
    "writing poems": 3, "a circle of artists": 4, "art school degree": 4,
}
