# Chroma content pack: The Five Callings. The engine's reading of how each title and perk comes and goes, proposed in
# earth_rules.ROLES syntax (chroma-engine/v22-speedpass/earth_rules.py, "ROLES = {"). Plain data for the Engine, which
# owns the rules and refits every rate (ROLE_NORM, and the tier lift for careers and summits). Condition words are the
# engine's own (batch.COND_VOCAB): has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark'), age, money, time,
# yrs_career. A name with an apostrophe is written in double quotes inside the condition.
#
# As in Art and Writing (../art/roles.py), most steps are taken by the player's own act at a door or a crossing
# (title: on an option in the pack's moments), so the background rates are low and every req is narrow: the road's own
# earlier title, or years on it, never a perk alone (Emren 10-06 09:18, "never from nothing"). Every career and summit
# lists its rungs below in rungs=, so the was() roads (the soldier who left and came back through the academy) stay
# open. Rules are checked every four weeks, so odds belong in rate, never in a chance() inside req.
#
# SWITCHED OFF: nothing reads this file until the Engine adds `callings` to batch.PACKS.

ROLES_CALLINGS = {
    # ------------------------------------------------ W: the faith leader
    "senior cleric": dict(req="(age >= 35) & has('scripture') & ((yrs_has('ordained religious minister') >= 8) | "
                              "(yrs_has('member of a monastic community') >= 10))",
                          rungs=["ordained religious minister", "member of a monastic community"],
                          rate=0.003, entry=True, weight="colors",
                          lose="yrs_has('senior cleric') >= 6", lrate=0.03,
                          lwhy="stepped back to a smaller congregation"),
    "head of a faith order": dict(refines="senior cleric; member of a monastic community",
                                  rungs=["senior cleric", "member of a monastic community"],
                                  req="(age >= 45) & ((yrs_has('senior cleric') >= 8) | "
                                      "(yrs_has('member of a monastic community') >= 20)) & "
                                      "(has('a flock that follows you') | has('known across the country') | "
                                      "has('a degree in theology'))",
                                  rate=0.003, weight="colors",
                                  lose="age >= 82", lrate=0.15, lwhy="stepped down in old age"),
    # ------------------------------------------------ U: the inventor
    "inventor": dict(req="(has('prototyping') | has('fixing things')) & ((yrs_has('software developer') >= 3) | "
                         "(yrs_has('civil engineer') >= 3) | (yrs_has('machinist') >= 3) | "
                         "(yrs_has('electrician') >= 3) | (yrs_has('founder of a firm') >= 2) | "
                         "(has('workshop') & (yrs_has('apprentice') >= 2)))",
                     rungs=["software developer", "civil engineer", "machinist", "electrician", "founder of a firm",
                            "apprentice"],
                     rate=0.002, entry=True, weight="colors",
                     lose="yrs_has('inventor') >= 3", lrate=0.08,
                     lwhy="the inventions stopped selling, and a steady job took over"),
    "celebrated inventor": dict(refines="inventor", rungs=["inventor"],
                                req="has('inventor') & (yrs_has('inventor') >= 5) & "
                                    "(has('a patent of your own') | has('an invention in everyday use'))",
                                rate=0.003, weight="colors", grants=["an invention in everyday use"]),
    # ------------------------------------------------ B: the magnate
    "chief executive": dict(req="(age >= 28) & ((yrs_has('founder of a firm') >= 3) | (yrs_has('shop owner') >= 5) | "
                                "(yrs_has('café or bar owner') >= 5) | (yrs_has('shift manager') >= 8)) & "
                                "(has('striking a deal') | has('bookkeeping') | has('investors who back you'))",
                            rungs=["founder of a firm", "shop owner", "café or bar owner", "shift manager"],
                            rate=0.002, entry=True, weight="colors",
                            lose="yrs_has('chief executive') >= 4", lrate=0.08, lwhy="the board voted them out"),
    "magnate": dict(refines="chief executive; founder of a firm", rungs=["chief executive", "founder of a firm"],
                    req="((yrs_has('chief executive') >= 5) | (yrs_has('founder of a firm') >= 10)) & "
                        "(has('investors who back you') | has('shares') | has('a seat on boards')) & (money > .3)",
                    rate=0.002, weight="colors", grants=["a business empire"],
                    lose="money < .05", lrate=0.3, lwhy="the empire fell, and the creditors took what was left"),
    # ------------------------------------------------ R: the commander
    "army officer": dict(req="(age >= 20) & (age <= 45) & ~has('someone with a record') & "
                             "((yrs_has('soldier') >= 3) | (has('graduate') & (has('keeping fit') | was('soldier') | "
                             "has('national service done'))))",
                         rungs=["soldier", "graduate", "national service done"],
                         rate=0.003, entry=True, weight="colors", grants=["an officer's commission"],
                         lose="yrs_has('army officer') >= 8", lrate=0.06,
                         lwhy="the commission ended, and civilian life began"),
    "general": dict(refines="army officer", rungs=["army officer"],
                    req="has('army officer') & (yrs_has('army officer') >= 15) & has('rank') & "
                        "(has('mentioned in dispatches') | has('award for bravery') | has('leading soldiers'))",
                    rate=0.002, weight="colors",
                    lose="age >= 62", lrate=0.3, lwhy="retired from the army"),
    # ------------------------------------------------ G: the healer
    "senior nurse or midwife": dict(req="((yrs_has('nurse') >= 5) | (yrs_has('midwife') >= 5)) & "
                                        "has('professional registration')",
                                    rungs=["nurse", "midwife"], rate=0.01, entry=True, weight="colors",
                                    lose="yrs_has('senior nurse or midwife') >= 5", lrate=0.03,
                                    lwhy="stepped back to the wards, or into teaching"),
    "renowned healer": dict(refines="senior nurse or midwife; nurse; midwife; physician; complementary therapist",
                            rungs=["senior nurse or midwife", "midwife", "nurse", "physician"],
                            req="(has('senior nurse or midwife') | has('nurse') | has('midwife') | has('physician') | "
                                "has('complementary therapist')) & (yrs_career >= 10) & "
                                "(has('families who send for you') | has('a clinic of your own') | "
                                "has('name in the field'))",
                            rate=0.003, weight="colors"),
    # ------------------------------------------------ skills (rates per year while the rung is held)
    "leading soldiers": dict(req="has('army officer') | (yrs_has('soldier') >= 3)", rate=0.1, weight="practice"),
    "preaching": dict(req="has('ordained religious minister') | has('senior cleric') | has('street preacher') | "
                          "has('independent preacher') | (has('lay religious teacher') & has('scripture'))",
                      rate=0.08, weight="practice"),
    "prototyping": dict(req="(has('fixing things') | has('machining') | has('writing code')) & (has('workshop') | "
                            "has('software developer') | has('civil engineer') | has('machinist') | "
                            "has('electrician') | has('inventor') | has('repair-cafe volunteer'))",
                        rate=0.03, weight="practice"),
    # ------------------------------------------------ credentials
    "a degree in theology": dict(req="(was('ordained religious minister') | has('lay religious teacher') | "
                                     "was('member of a monastic community')) & (has('graduate') | "
                                     "(yrs_has('ordained religious minister') >= 2))", rate=0.2),
    "an officer's commission": dict(req="has('army officer')", rate=0.9,
                                    lose="~has('army officer') & (yrs_has(\"an officer's commission\") >= 1)",
                                    lrate=0.5, lwhy="the commission was resigned with the post"),
    "licence to prescribe": dict(req="((yrs_has('nurse') >= 3) | (yrs_has('midwife') >= 3) | "
                                     "has('senior nurse or midwife') | has('physician')) & "
                                     "has('professional registration')", rate=0.05),
    # ------------------------------------------------ standing
    "an invention in everyday use": dict(req="has('celebrated inventor') | (has('inventor') & "
                                             "has('a patent of your own') & (yrs_has('inventor') >= 3))",
                                         rate=0.04, weight="colors"),
    "a seat on boards": dict(req="(yrs_has('chief executive') >= 2) | has('magnate') | "
                                 "(yrs_has('founder of a firm') >= 8)", rate=0.06, weight="colors"),
    "mentioned in dispatches": dict(req="has('army officer') | (yrs_has('soldier') >= 2)", rate=0.01),
    # ------------------------------------------------ bonds
    "families who send for you": dict(req="(yrs_has('nurse') >= 4) | (yrs_has('midwife') >= 3) | "
                                          "(yrs_has('physician') >= 4) | has('senior nurse or midwife') | "
                                          "(yrs_has('care worker') >= 6)", rate=0.04),
    "a flock that follows you": dict(req="(yrs_has('ordained religious minister') >= 4) | has('senior cleric') | "
                                         "(yrs_has('street preacher') >= 4)", rate=0.04, weight="colors"),
    "investors who back you": dict(req="(yrs_has('founder of a firm') >= 2) | has('chief executive') | "
                                       "(yrs_has('shop owner') >= 5)", rate=0.03, weight="colors"),
    # ------------------------------------------------ assets
    "a business empire": dict(req="has('magnate')", rate=0.5),
    "a patent of your own": dict(req="has('prototyping') & (has('inventor') | has('founder of a firm') | "
                                     "(has('workshop') & (money > .2)))", rate=0.03,
                                 lose="yrs_has('a patent of your own') >= 20", lrate=0.5,
                                 lwhy="the patent ran out after twenty years"),
    "a clinic of your own": dict(req="(has('senior nurse or midwife') | has('physician') | has('renowned healer')) & "
                                     "(has('savings') | has('families who send for you')) & (yrs_career >= 8)",
                                 rate=0.01),
}

# More ways into rules the pack does not own (or-ed onto the base rule, at the rule's own rate).
EXTEND_CALLINGS = {
    # every summit is national news, as the other packs' summits are
    "known across the country": "has('head of a faith order') | has('celebrated inventor') | has('magnate') | "
                                "has('general') | has('renowned healer')",
    "rank": "has('army officer')",
    "name in the field": "has('inventor') & has('a patent of your own')",
    "good name in town": "(yrs_has('senior cleric') >= 2) | (yrs_has('senior nurse or midwife') >= 3)",
    "shares": "has('magnate') | (has('chief executive') & (money > .3))",
    "workshop": "has('inventor') & (money > .15)",
}

# Fit targets (batch._targets; Emren's one budget for all packs): a tier word per title, as TARGET_ART. The engine fits
# one lift per tier, so the loaded packs together give about 1 life in 3 a career and about 1 in 20 a summit
# (earth_rules.BUDGET); with the floors on (batch.FLOORS) each pack career reaches 1.5 lives in 100 and each summit 1 in
# 100 (BUDGET_FLOORS). A fifth pack takes its share of that one budget: the Engine refits the tier lifts with
# `callings` loaded. The two faith titles carry the career and summit words too: a calling of faith is the faith road's
# career, though the catalogue keeps it of the faith kind. Perks keep a multiple (ROLE_NORM): 10x for the perks of the
# Known rungs and summits, 4x for the skills and credentials of the rungs below.
TARGET_CALLINGS = {
    # the Known rungs
    "senior cleric": "career", "inventor": "career", "chief executive": "career", "army officer": "career",
    "senior nurse or midwife": "career",
    # summits
    "head of a faith order": "summit", "celebrated inventor": "summit", "magnate": "summit", "general": "summit",
    "renowned healer": "summit",
    # perks of the Known rungs and summits
    "an officer's commission": 10, "an invention in everyday use": 10, "a seat on boards": 10,
    "mentioned in dispatches": 10, "families who send for you": 10, "a flock that follows you": 10,
    "investors who back you": 10, "a business empire": 10, "a patent of your own": 10, "a clinic of your own": 10,
    # skills and credentials of the rungs below
    "leading soldiers": 4, "preaching": 4, "prototyping": 4, "a degree in theology": 4, "licence to prescribe": 4,
}
