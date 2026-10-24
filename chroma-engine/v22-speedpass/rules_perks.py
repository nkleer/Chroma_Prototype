# rules_perks.py: part 4 of 11 of earth_rules.py, the engine's reading of the Library's words.
# ROLES_P2, TITLE_LINKS, budgets, tier lifts, ROLES_WHEN, the sphere titles.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# ---- perks volume 2 (Emren 15:46; the Library's drafts/perks2/roles-perks2.py of 16:40, as written): ROLES_P2, 85 perk
# rules, and TITLE_LINKS, an overlay on 34 title rules (req, lose and lrate replace the title's own; grants add; why is a
# comment). Like volume 2's titles, a catalogue without these perks still loads (ROLES_OPTIONAL).
ROLES_P2 = {
    # ---------------- p1_access
    # ---------------- credentials
    # transport: the job's licence, its medical and its record
    "airline pilot licence": dict(req="has('commercial pilot') & (health >= .5) & ~has('someone with a record')",
                                  rate=1.0, lrate=0.5,
                                  lose=[("health < .5", "failed the medical"),
                                        ("has('someone with a record')", "a conviction"),
                                        ("~has('commercial pilot')", "let it lapse after leaving the airline")]),
    "train driving licence": dict(req="has('train driver') & (health >= .45) & ~has('someone with a record')",
                                  rate=1.0, lrate=0.5,
                                  lose=[("health < .45", "failed the medical"),
                                        ("has('someone with a record')", "a conviction"),
                                        ("~has('train driver')", "lapsed after leaving the cab")]),
    # the sea: the seafarer's own papers, and the survival course every boat asks for
    "seafarer's papers": dict(req="(has('merchant seafarer') | ((age >= 18) & (age <= 35) & has('swimming') & "
                                  "had(['a trip far from home', 'the itch to be somewhere else'], 2))) & (health >= .45)",
                              rate=0.0029, lrate=0.3,
                              lose=[("health < .45", "failed the seafarer medical"),
                                    ("~has('merchant seafarer') & (yrs_has('seafarer\\'s papers') >= 2)",
                                     "let them lapse ashore")]),
    "sea survival certificate": dict(req="has('commercial fisher') | has('lifeboat volunteer') | has('merchant seafarer') | "
                                         "((has('welder') | has('rigging ticket') | has('trade ticket')) & (age <= 55))",
                                     rate=0.0038, lrate=0.5,
                                     lose="~has('commercial fisher') & ~has('lifeboat volunteer') & "
                                          "~has('merchant seafarer') & (yrs_has('sea survival certificate') >= 4)",
                                     lwhy="lapsed without a refresher"),
    "fishing licence": dict(req="has('hunting and fishing') | has('commercial fisher') | "
                                "((age >= 12) & had(['a day at the beach', 'a weekend hike'], 1))", rate=0.011),
    # trades: tickets that come after the apprenticeship, and lapse when the trade is left
    "gas safety registration": dict(req="(has('plumber') & (yrs_career >= 2)) | (has('trade ticket') & (age >= 21) & chance(.1))",
                                    rate=0.032, lose="~has('plumber') & ~has('trade ticket')", lrate=0.5,
                                    lwhy="lapsed after leaving the trade"),
    "welding certificate": dict(req="has('welder') | ((has('apprentice') | has('machinist') | has('builder')) & "
                                    "(mkn('learned a skill') >= 2))",
                                rate=0.002, lose="~has('welder') & ~has('machinist') & ~has('builder')", lrate=0.3,
                                lwhy="lapsed out of use"),
    "site safety card": dict(req="(age >= 16) & (has('builder') | has('carpenter') | has('welder') | has('plumber') | "
                                 "has('electrician') | has('civil engineer') | has('land surveyor') | "
                                 "(has('apprentice') & has('building trade')))",
                             rate=0.22, lrate=0.5,
                             lose="~has('builder') & ~has('carpenter') & ~has('welder') & ~has('plumber') & "
                                  "~has('electrician') & ~has('civil engineer') & ~has('land surveyor') & "
                                  "~has('apprentice') & (yrs_has('site safety card') >= 5)",
                             lwhy="ran out after years off the sites"),
    "rigging ticket": dict(req="(has('stage technician') & (yrs_career >= 1)) | "
                               "((has('builder') | has('welder')) & (yrs_career >= 2) & chance(.2))", rate=0.043),
    "chainsaw ticket": dict(req="(age >= 16) & (has('forester') | has('farmer') | "
                                "((has('plot of land') | has('hunting and fishing') | has('fixing things')) & chance(.1)))",
                            rate=0.018),
    "chartered status": dict(req="(has('civil engineer') | has('land surveyor') | has('architect') | has('urban planner')) & "
                                 "(yrs_career >= 4)", rate=0.086),
    # food and care: the commonest papers, kept while the work lasts
    "food hygiene certificate": dict(req="has('cook') | has('head chef') | has('baker') | has('community-kitchen volunteer') | "
                                         "has('care worker') | has('shop owner') | "
                                         "((has('waiter or bartender') | has('shop assistant')) & chance(.5))",
                                     rate=0.027, lrate=0.3,
                                     lose="~has('cook') & ~has('head chef') & ~has('baker') & "
                                          "~has('community-kitchen volunteer') & ~has('care worker') & ~has('shop owner') & "
                                          "~has('waiter or bartender') & ~has('shop assistant') & "
                                          "(yrs_has('food hygiene certificate') >= 3)",
                                     lwhy="out of date after years away from food work"),
    "cleared to work with children": dict(req="(age >= 16) & ~has('someone with a record') & (has('teacher') | "
                                              "has('youth coach') | has('foster parent') | has('adoptive parent') | "
                                              "has('school-governance board member') | has('lay religious teacher') | "
                                              "has('parent-association organiser') | has('guardian of an unrelated child') | "
                                              "has('nurse') | has('paramedic') | has('physician') | has('midwife') | "
                                              "(kids_home & chance(.1)) | (held_community & chance(.05)))",
                                          rate=0.045, lrate=0.5,
                                          lose="has('someone with a record') & (yrs_has('someone with a record') < 1)",
                                          lwhy="a new conviction showed on the check"),
    "lifeguard qualification": dict(req="has('swimming') & (age >= 16) & (age <= 30) & (health > .6)", rate=0.0033,
                                    weight="colors", grants=["first-aid certificate"], lrate=0.4,
                                    lose="(age >= 26) & (yrs_has('lifeguard qualification') >= 2) & ~has('lifeboat volunteer')",
                                    lwhy="let it lapse"),
    # words, ceremonies and care of the mind: approvals that come with the work, and go with a conviction
    "tattoo licence": dict(req="has('tattoo artist')", rate=1.0, lose="~has('tattoo artist')", lrate=0.5,
                           lwhy="lapsed after leaving the trade"),
    "celebrant authorisation": dict(req="(has('civil celebrant') | has('ordained religious minister') | "
                                        "(has('public speaking') & had(['dancing at a wedding'], 1) & chance(.2))) & "
                                        "~has('someone with a record')",
                                    rate=0.4, lose="has('someone with a record')", lrate=0.5,
                                    lwhy="struck from the register"),
    "court interpreter accreditation": dict(req="(has('court interpreter') | (has('translator') & (yrs_career >= 3))) & "
                                                "~has('someone with a record') & (age >= 23)",
                                            rate=0.00017, lrate=1.0,
                                            lose=[("has('someone with a record')", "a conviction"),
                                                  ("~has('court interpreter') & ~has('translator')",
                                                   "lapsed after leaving the work")]),
    "press card": dict(req="has('journalist') & (yrs_career >= 1)", rate=0.11, lose="~has('journalist')", lrate=0.5,
                       lwhy="handed back after leaving journalism"),
    "therapy accreditation": dict(req="(has('psychotherapist') | ((has('nurse') | has('teacher') | has('care worker')) & "
                                      "has('calming people down') & (age >= 25) & chance(.1))) & ~has('someone with a record')",
                                  rate=0.8, lose="has('someone with a record')", lrate=0.5,
                                  lwhy="struck off the register"),
    "mediation accreditation": dict(req="(age >= 21) & (has('community-mediation volunteer') | "
                                        "has('restorative-justice advocate') | "
                                        "(has('calming people down') & held_career & (yrs_career >= 5) & chance(.1)))",
                                    rate=0.0062),
    # learning, travel and settling
    "diving certificate": dict(req="has('swimming') & (age >= 10) & (health > .5) & "
                                   "had(['a long-planned trip', 'a trip far from home', 'a day at the beach'], 1)",
                               rate=0.018, weight="colors"),
    "reader's ticket": dict(req="(age >= 16) & (has('finding things out') | has('graduate') | "
                                "had(['a parent dies', 'a grandparent dies', 'losing a grandparent', "
                                "'a long-lost relative finds you'], 3))", rate=0.0007, weight="colors"),
    "permanent residence": dict(req="((has('immigrant') & (yrs_has('immigrant') >= 3)) | "
                                    "(has('refugee') & (yrs_has('refugee') >= 3))) & "
                                    "~has('citizenship') & ~has('returned migrant')",
                                rate=0.13, lrate=1.0,
                                lose=[("has('citizenship')", "replaced by citizenship"),
                                      ("has('returned migrant')", "given up on going home")]),

    # ---------------- assets
    "hives of one's own": dict(req="(age >= 14) & (has('plot of land') | has('farmer') | has('growing food') | "
                                   "had(['a new hobby you cannot put down', 'tending an allotment'], 2))",
                               rate=0.00017, weight="colors", lrate=0.5,
                               lose=[("had(['a third of the hives dead after winter'], 1) & chance(.3)",
                                      "the colonies died out"),
                                     ("ago_move < 1", "nowhere to keep them after a move"),
                                     ("(age >= 80) | (health < .35)", "the boxes grew too heavy")]),
    "boat of one's own": dict(req="(age >= 16) & (money > .3) & (has('swimming') | has('hunting and fishing'))",
                              rate=0.015, weight="money"),
    "share in a fishing boat": dict(req="has('commercial fisher') & (yrs_career >= 3) & "
                                        "(has('savings') | has('family business') | has('inheritance'))",
                                    rate=1.0, lrate=0.4,
                                    lose=[("had(['financial ruin'], 1)", "sold to pay debts"),
                                          ("~has('commercial fisher')", "sold on leaving the sea")]),
    "studio of one's own": dict(req="(age >= 18) & (money > .2) & (has('tattoo artist') | has('sound engineer') | "
                                    "((has('drawing and painting') | has('musical instrument')) & chance(.1)))",
                                rate=0.033, weight="money"),
    "premises of one's own": dict(req="has('shop owner') | ((has('founder of a firm') | has('baker') | "
                                      "has('funeral director') | has('pharmacist') | has('veterinarian') | "
                                      "has('physician') | has('carpenter') | has('tattoo artist') | "
                                      "has('psychotherapist') | has('head chef')) & (money > .25) & chance(.2))",
                                  rate=0.23, weight="money", lrate=0.5,
                                  lose=[("had(['financial ruin'], 1)", "financial ruin"),
                                        ("~held_career", "the lease given up")]),
    "horse of one's own": dict(req="(age >= 6) & (money > .3) & (has('plot of land') | has('farmer') | "
                                   "has('handling animals') | had(['a pet of your own'], 10))", rate=0.02, weight="money"),
    "good telescope": dict(req="(age >= 10) & (has('amateur astronomer in a club') | ((has('finding things out') | "
                               "had(['more stars than anyone could count', 'the sun goes dark at noon', 'awe'], 2)) & "
                               "chance(.1)))", rate=0.008, weight="colors"),
    "period kit": dict(req="has('historical reenactment member')", rate=0.67),
    "stake in the firm": dict(req="held_career & (yrs_career >= 8) & (has('physician') | has('pharmacist') | "
                                  "has('veterinarian') | has('architect') | has('accountant') | has('civil engineer') | "
                                  "has('land surveyor') | has('funeral director') | has('founder of a firm') | "
                                  "has('inner circle at work') | has('family business'))",
                              rate=0.023, weight="money", lrate=0.5,
                              lose=[("~held_career", "bought out on leaving"),
                                    ("had(['financial ruin'], 1)", "the firm went under")]),
    "research grant": dict(req="(age >= 23) & (has('doctoral graduate') | has('archaeologist') | has('museum curator') | "
                               "has('professional conservator') | has('archivist') | "
                               "(has('graduate') & (mkn('learned a skill') >= 5) & chance(.1)))",
                           rate=0.0025, weight="practice", lrate=0.6,
                           lose=[("had(['the grant runs out in June'], 1)", "the grant ran out"),
                                 ("yrs_has('research grant') >= 3", "the money was spent")]),
    "collection of one's own": dict(req="(age >= 12) & (has('finding things out') | has('museum curator') | "
                                        "had(['a curiosity that will not let go', 'a new hobby you cannot put down', "
                                        "'an unexpected legacy'], 3))", rate=0.0027, weight="colors"),
    "tools of one's own": dict(req="(age >= 16) & (has('carpenter') | has('welder') | has('plumber') | has('electrician') | "
                                   "has('builder') | has('machinist') | has('building trade') | has('car mechanics'))",
                               rate=0.03, weight="money"),
    "camper van": dict(req="(age >= 21) & has('driving licence') & (money > .35) & "
                           "(has('parent of independent adult children') | has('retiree') | "
                           "had(['the itch to be somewhere else', 'a late chance to see the world', 'a long-planned trip'], 3))",
                       rate=0.024, weight="money", lrate=0.5,
                       lose=[("had(['the doctor says to stop driving'], 1)", "the doctor says to stop driving"),
                             ("had(['financial ruin'], 1)", "financial ruin"),
                             ("(money < .05) & (yrs_adj('poor') >= 1)", "sold in hard times")]),
    "secure tenancy": dict(req="(age >= 18) & (ago_move >= 1) & ~has('homeowner') & (((money < .2) & (ago_move >= 2)) | "
                               "has('homeless') | "
                               "has('housing-cooperative member') | has('displaced by a disaster') | "
                               "had(['losing the home'], 2))",
                           rate=0.0061, lrate=0.5,
                           lose=[("has('homeowner')", "bought a home of their own"),
                                 ("(ago_move < 1) & ~has('housing-cooperative member')", "given up on moving away"),
                                 ("(money < .01) & (yrs_adj('poor') >= 1) & chance(.2)", "evicted after months of arrears")]),
    # ---------------- p2_skills
    # ---------------- skills
    # trades and making
    "welding": dict(req="has('welder') | has('machinist') | has('car mechanics') | has('building trade') | has('farmer')",
                    rate=0.00099),
    "machining": dict(req="has('machinist') | (was('apprentice') & (mkn('learned a skill') >= 2)) | "
                          "(has('factory worker') & has('fixing things'))", rate=0.00026),
    "baking": dict(req="has('baker') | has('cook') | has('cooking for a crowd') | "
                       "had(['learning to cook for yourself', 'a holiday meal with the whole family'], 3)", rate=0.0029),
    "restoring old things": dict(req="has('professional conservator') | has('museum curator') | has('repair-cafe volunteer') | "
                                     "((has('fixing things') | has('sewing and mending')) & (age >= 25))", rate=0.00028),
    # sea, land and living things
    "navigation": dict(req="has('commercial pilot') | has('merchant seafarer') | has('search-and-rescue volunteer') | "
                           "has('lifeboat volunteer') | has('soldier') | has('scout or guide') | "
                           "had(['a weekend hike', 'a long walk alone'], 3)", rate=0.0025),
    "boat handling": dict(req="has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | "
                              "has('hunting and fishing') | (has('swimming') & had(['a day at the beach', 'summer camp'], 2))",
                          rate=0.004),
    # sea legs come within weeks at sea and go within a year or two ashore
    "sea legs": dict(req="has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | has('boat handling')",
                     rate=0.06,
                     lose="~(has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | "
                          "has('boat handling'))", lrate=0.5, lwhy="years ashore"),
    "knowing the woods": dict(req="has('forester') | has('hunting and fishing') | has('scout or guide') | has('farmer') | "
                                  "had(['a weekend hike', 'a long walk alone'], 3)", rate=0.0013),
    "handling animals": dict(req="has('veterinarian') | has('farmer') | has('animal-shelter campaigner') | "
                                 "has('dog of one\\'s own') | has('cat of one\\'s own')", rate=0.002),
    "beekeeping": dict(req="has('professional beekeeper') | has('farmer') | has('hives of one\\'s own') | "
                           "((age >= 14) & had(['a new hobby you cannot put down', 'tending an allotment'], 3))", rate=0.00029),
    # words and records
    "interpreting": dict(req="has('court interpreter') | has('translator') | (has('second language') & "
                             "(has('immigrant') | has('refugee') | has('parent raising a child across languages')))", rate=0.00096),
    "editing": dict(req="has('book editor') | has('journalist') | has('doctoral graduate') | "
                        "(has('graduate') & (mkn('learned a skill') >= 3))", rate=0.00048),
    "reporting": dict(req="has('journalist') | has('community-radio presenter') | has('digital-rights advocate') | "
                          "(has('finding things out') & has('writing stories'))", rate=0.0013),
    "writing stories": dict(req="has('novelist') | (had(['inspiration strikes', 'the urge to make something', "
                                "'the notebooks come together'], 3) & (mkn('learned a skill') >= 2))", rate=0.00067),
    "archive research": dict(req="has('archivist') | has('museum curator') | has('archaeologist') | has('doctoral graduate') | "
                                 "(has('finding things out') & (age >= 40))", rate=0.00036),   # family historians start late
    # science and systems
    "lab work": dict(req="has('laboratory technician') | has('pharmacist') | has('physician') | has('veterinarian') | "
                         "has('doctoral graduate') | (has('graduate') & (age <= 30) & (mkn('learned a skill') >= 3))", rate=0.0051),
    "working with data": dict(req="has('data analyst') | has('accountant') | has('software developer') | "
                                  "has('cybersecurity analyst') | has('doctoral graduate') | "
                                  "(has('office clerk') & has('bookkeeping')) | (has('graduate') & (mkn('learned a skill') >= 3))",
                              rate=0.0025),
    "keeping systems secure": dict(req="has('cybersecurity analyst') | has('digital-rights advocate') | "
                                       "(has('writing code') & (mkn('learned a skill') >= 3))", rate=0.00029),
    # stage and sound
    "sound mixing": dict(req="has('sound engineer') | has('community-radio presenter') | has('amateur band member') | "
                             "has('congregation musician') | has('stage technician')", rate=0.002),
    "stagecraft": dict(req="has('stage technician') | has('festival organiser') | has('amateur band member') | "
                           "(had(['the school play'], 5) & has('fixing things') & (age <= 25))", rate=0.0031),
    "singing": dict(req="has('choir member') | has('congregation musician') | has('amateur band member') | "
                        "has('regular worshipper') | (age <= 14)", rate=0.0051),
    # people
    "counselling": dict(req="has('psychotherapist') | has('ordained religious minister') | has('prison visitor') | "
                            "(has('calming people down') & (mkn('helped someone in need') >= 3))", rate=0.00041),
    "leading a ceremony": dict(req="has('civil celebrant') | has('ordained religious minister') | has('funeral director') | "
                                   "has('lay religious teacher') | has('deacon or elder') | "
                                   "(has('public speaking') & had(['a memorial service for a friend'], 2))", rate=0.00074),
    "settling disputes": dict(req="has('community-mediation volunteer') | has('restorative-justice advocate') | has('union rep') | "
                                  "has('shift manager') | (has('calming people down') & (mkn('helped someone in need') >= 3))",
                              rate=0.0014),
    "organising people": dict(req="(held_community & (yrs_community >= 2)) | has('shift manager') | has('founder of a firm')",
                              rate=0.0022),
    "campaigning": dict(req="has('civil-liberties campaigner') | has('disability-rights organiser') | "
                            "has('digital-rights advocate') | has('animal-shelter campaigner') | has('activist in a cause') | "
                            "has('union rep') | has('party member') | "
                            "had(['a protest in your city', 'a protest to save the local hospital'], 3)", rate=0.00049),
    "handling red tape": dict(req="has('parent coordinating complex support needs') | has('carer for a parent') | "
                                  "has('caregiving partner') | has('immigrant') | has('asylum applicant') | "
                                  "has('founder of a firm') | has('shop owner') | had(['your first tax form and a stack of bills', "
                                  "'sorting out your will', 'a dispute over an inheritance'], 2)", rate=0.0022),
    # the body
    "emergency care": dict(req="has('paramedic') | has('firefighter') | has('search-and-rescue volunteer') | "
                               "has('lifeboat volunteer') | has('nurse') | has('physician') | has('midwife') | "
                               "has('police officer') | has('soldier') | (has('first-aid certificate') & mk('helped someone in need'))",
                           rate=0.00058),
    "strong stomach": dict(req="has('paramedic') | has('physician') | has('nurse') | has('midwife') | has('funeral director') | "
                               "has('sanitation worker') | has('firefighter') | has('veterinarian') | has('farmer') | "
                               "has('care worker') | has('soldier')", rate=0.069),
    # the body adjusts within a year of nights and readjusts within a year of days; tolerance falls after sixty
    "used to night shifts": dict(req="has('nurse') | has('paramedic') | has('emergency dispatcher') | has('police officer') | "
                                     "has('firefighter') | has('physician') | has('midwife') | has('care worker') | "
                                     "has('factory worker') | has('baker') | has('train driver') | has('merchant seafarer') | "
                                     "has('waiter or bartender') | has('cleaner') | has('postal worker')", rate=0.013,
                                 lose=[("~held_career", "nights given up"), ("age >= 60", "the nights grew harder with age")],
                                 lrate=0.3),
    "head for heights": dict(req="has('firefighter') | has('stage technician') | has('builder') | has('building trade') | "
                                 "has('electrician') | has('search-and-rescue volunteer') | "
                                 "(has('keeping fit') & mk('took a wild risk'))", rate=0.0018),
    "keeping fit": dict(req="has('on the team') | has('professional athlete') | has('firefighter') | has('soldier') | "
                            "has('police officer') | has('search-and-rescue volunteer') | has('boxing or martial arts') | "
                            "had(['a weekend hike', 'a band or a sport that takes over your life', 'a warning from the doctor'], 2)",
                        rate=0.009),

    # ---------------- standing
    "book in print": dict(req="has('novelist') | has('journalist') | has('doctoral graduate') | has('name in the field') | "
                              "(has('writing stories') & (age >= 25))", rate=0.0021, weight="practice"),
    "published research": dict(req="has('doctoral graduate') | has('physician') | has('archaeologist') | "
                                   "has('laboratory technician') | has('museum curator') | has('professional conservator') | "
                                   "has('veterinarian') | has('pharmacist')", rate=0.045, weight="practice"),
    # regulars follow the person, not the shop: lost with the work or a move
    "loyal clientele": dict(req="(has('tattoo artist') | has('baker') | has('plumber') | has('carpenter') | has('electrician') | "
                                "has('builder') | has('translator') | has('civil celebrant') | has('sound engineer') | "
                                "has('psychotherapist') | has('shop owner') | has('cleaner') | has('funeral director') | "
                                "has('accountant') | has('salesperson') | has('estate agent')) & (yrs_career >= 3)",
                            rate=0.02, weight="practice",
                            lose=[("~held_career", "the work given up"), ("ago_move < 1", "a move away from the clients")],
                            lrate=0.6),
    # an award is kept for life; only a scandal undoes it
    "award for bravery": dict(req="(has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                  "has('paramedic') | has('police officer') | has('soldier') | has('local hero')) & "
                                  "mk('took a wild risk', 2) & mk('helped someone in need', 2)", rate=0.011,
                              lose="had(['a public scandal'], 1)", lrate=0.5, lwhy="a public scandal"),
    "voice at the town hall": dict(req="has('local councillor') | has('school-governance board member') | has('urban planner') | "
                                       "has('residents\\' committee member') | has('neighbourhood-watch coordinator') | "
                                       "has('civil-liberties campaigner') | has('disability-rights organiser') | "
                                       "(has('good name in town') & (yrs_community >= 3))", rate=0.0029, weight="colors",
                                   lose=[("ago_move < 1", "a move away"),
                                         ("had(['a public scandal', 'a bitter election'], 1)", "a scandal or a bitter election")],
                                   lrate=0.6),
    "name on the local scene": dict(req="has('amateur band member') | has('festival organiser') | has('community-radio presenter') | "
                                        "has('tattoo artist') | has('sound engineer') | has('head chef') | "
                                        "has('board-game club organiser')", rate=0.0073, weight="colors",
                                    lose=[("ago_move < 1", "a move to a new town"),
                                          ("~held_community & ~held_career", "out of the scene")], lrate=0.5),
    "trusted with the keys": dict(req="(age >= 18) & (has('reliable record') | has('cleaner') | has('postal worker') | "
                                      "has('club treasurer') | has('deacon or elder') | has('lay religious teacher') | "
                                      "has('neighbourhood-watch coordinator') | has('housing-cooperative member'))",
                                  rate=0.008, weight="colors",
                                  lose=[("mk('broke your word', 1) | mk('hid a wrong', 1)", "trust broken"),
                                        ("ago_move < 1", "a move away")], lrate=0.5),
    "trophies won": dict(req="(has('on the team') & (yrs_has('on the team') >= 2)) | has('team captain') | "
                             "has('professional athlete') | has('boxing or martial arts')", rate=0.0021, weight="practice"),

    # ---------------- bonds
    # the crew of the job held now; once the job is left, what remains is old comrades
    "crew that has your back": dict(req="has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                        "has('merchant seafarer') | has('commercial fisher') | has('stage technician') | "
                                        "has('paramedic') | has('police officer') | has('soldier') | has('head chef') | "
                                        "has('cook') | has('sanitation worker') | has('builder')", rate=0.05, weight="ties",
                                    lose="~(has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                         "has('merchant seafarer') | has('commercial fisher') | has('stage technician') | "
                                         "has('paramedic') | has('police officer') | has('soldier') | has('head chef') | "
                                         "has('cook') | has('sanitation worker') | has('builder'))",
                                    lrate=0.5, lwhy="the crew left behind"),
    # an apprenticeship runs three or four years; then the apprentice goes
    "apprentice of one's own": dict(req="(age >= 25) & (yrs_career >= 5) & (has('machinist') | has('welder') | has('plumber') | "
                                        "has('carpenter') | has('electrician') | has('builder') | has('baker') | has('head chef') | "
                                        "has('tattoo artist') | has('farmer') | has('professional beekeeper'))",
                                    rate=0.035, weight="practice",
                                    lose="yrs_has('apprentice of one\\'s own') >= 4", lrate=0.5,
                                    lwhy="the apprentice qualified and went their own way"),
    "carers' group": dict(req="has('carer for a parent') | has('caregiving partner') | "
                              "has('parent coordinating complex support needs') | has('grandparent raising a grandchild')",
                          rate=0.0046, weight="ties",
                          lose="~(has('carer for a parent') | has('caregiving partner') | "
                               "has('parent coordinating complex support needs') | has('grandparent raising a grandchild'))",
                          lrate=0.3, lwhy="the caring years over"),
    "source who trusts you": dict(req="has('journalist') | has('digital-rights advocate') | has('civil-liberties campaigner')",
                                  rate=0.0085, weight="ties",
                                  lose=[("mk('broke your word', 1)", "a confidence broken"),
                                        ("~(has('journalist') | has('digital-rights advocate') | has('civil-liberties campaigner'))",
                                         "out of the work")], lrate=0.5),
    "business partner": dict(req="(age >= 18) & (has('founder of a firm') | has('shop owner') | has('plumber') | has('carpenter') | "
                                 "has('tattoo artist') | has('architect') | has('accountant') | has('psychotherapist') | "
                                 "has('estate agent') | has('farmer'))", rate=0.061, weight="money",
                             lose=[("had(['betrayed by a friend or a business partner', 'financial ruin'], 1)", "a betrayal or a ruin"),
                                   ("~held_career", "the business wound up")], lrate=0.6),
    "godchild": dict(req="(age >= 16) & (mkn('made a friend') >= 2) & (has('friend for life') | has('regular worshipper') | "
                         "has('believer on the big days'))", rate=0.0031, weight="ties"),
    "cat of one's own": dict(req="had(['a pet of your own'], 1) | (age >= 18)", rate=0.01,
                             lose="had(['your pet dies'], 1)", lrate=1.0, lwhy="the cat died"),
    "people from home": dict(req="has('immigrant') | has('refugee') | has('asylum applicant') | "
                                 "((ago_move < 3) & (mkn('moved away') >= 1))", rate=0.0063, weight="ties"),
}

TITLE_LINKS = {
    'train driver': dict(grants=['train driving licence'], lrate=1.0, lose=[("~has('train driving licence')", 'lost the train driving licence')], why="the operator's training gives the licence; a failed medical or a conviction ends the licence, and the cab goes with it"),
    'commercial pilot': dict(grants=['airline pilot licence', 'navigation'], lrate=1.0, lose=[("~has('airline pilot licence') & (age < 65)", 'lost the licence')], why='the licence comes with the first commercial post; a failed medical ends the licence, and at 65 the title ends by age as before; years of flight training come before a first commercial post'),
    'merchant seafarer': dict(grants=["seafarer's papers", 'sea survival certificate'], lrate=1.0, lose=[("~has('seafarer\\'s papers')", "lost the seafarer's papers")], why='the cadetship gives the papers and the survival course; a failed seafarer medical ends the papers and the sea career'),
    'court interpreter': dict(grants=['court interpreter accreditation', 'interpreting'], lrate=1.0, lose=[("~has('court interpreter accreditation')", 'lost accreditation')], why="accreditation comes with the first court list; a conviction ends it (as the title's old lose did) and the court work with it; an interpreting qualification comes before accreditation"),
    'civil celebrant': dict(req="(age >= 25) & has('public speaking') & ~has('someone with a record')", grants=['celebrant authorisation', 'leading a ceremony'], lrate=1.0, lose=[("~has('celebrant authorisation')", 'lost authorisation')], why='registration asks for a fit and proper person; struck from the register, the celebrant stops; a celebrant course comes before the first booking'),
    'psychotherapist': dict(req="has('graduate') & (age >= 25) & ~has('someone with a record')", grants=['therapy accreditation', 'counselling'], lrate=1.0, lose=[("~has('therapy accreditation')", 'lost accreditation')], why='the training ends in accreditation; struck off, the therapist closes the practice; a long training with supervised clients comes before a caseload'),
    'professional beekeeper': dict(req="(age >= 20) & (mkn('learned a skill') >= 3) & has('hives of one\\'s own')", lrate=1.0, lose=[("~has('hives of one\\'s own')", 'the hives were lost or sold')], why="the business grows from a few hives of one's own; without hives it ends; years of beekeeping practice come before hundreds of hives", grants=['beekeeping']),
    'amateur astronomer in a club': dict(req="(age >= 10) & (had(['more stars than anyone could count', 'the sun goes dark at noon', 'awe'], 10) | has('finding things out') | has('good telescope'))", why='an owner of a good telescope often looks for a club to share the sky with; the telescope is one way in, never required'),
    'commercial fisher': dict(grants=['sea survival certificate', 'fishing licence'], why='sea safety training and a licence come with the first berth'),
    'lifeboat volunteer': dict(grants=['sea survival certificate'], why='sea survival is part of crew training'),
    'welder': dict(grants=['welding certificate', 'welding'], why='the coded test is how a welder is taken on; coded tests are passed before the first job'),
    'tattoo artist': dict(grants=['tattoo licence'], why='the council registers the artist with the studio'),
    'forester': dict(grants=['chainsaw ticket', 'knowing the woods'], why='forestry training includes the chainsaw ticket; a forestry degree or apprenticeship comes first'),
    'community-mediation volunteer': dict(grants=['mediation accreditation', 'settling disputes'], why="the service's training course ends in accreditation; a training course comes before supervised mediation"),
    'ordained religious minister': dict(grants=['celebrant authorisation', 'leading a ceremony'], why='in most traditions ordination lets a minister conduct weddings; years of training come before ordination'),
    'baker': dict(grants=['food hygiene certificate', 'baking'], why='no bakery opens its ovens to the untrained; early shifts as a bakery assistant come before responsibility for the bake'),
    'cook': dict(grants=['food hygiene certificate'], why='every commercial kitchen trains its staff in food hygiene'),
    'community-kitchen volunteer': dict(grants=['food hygiene certificate'], why='the induction includes food-safety training'),
    'laboratory technician': dict(grants=['lab work'], why='a technical course or a science degree, and safety training, come first'),
    'paramedic': dict(grants=['emergency care'], why='a paramedic degree with supervised ambulance placements comes first'),
    'veterinarian': dict(grants=['handling animals'], why='five or six years of veterinary school come first'),
    'firefighter': dict(grants=['keeping fit'], why='fitness tests are passed before a place on a watch'),
    'journalist': dict(grants=['reporting'], why='a journalism course or a student paper comes before a first commission'),
    'book editor': dict(grants=['editing'], why="years as an editorial assistant come before a list of one's own"),
    'archivist': dict(grants=['archive research'], why='archival training or proven competence comes first'),
    'data analyst': dict(grants=['working with data'], why='the workplace takes them on to turn records into answers'),
    'cybersecurity analyst': dict(grants=['keeping systems secure'], why='certifications come before a post on a security team'),
    'machinist': dict(grants=['machining'], why="machine training comes before jobs of one's own on the lathes and mills"),
    'sound engineer': dict(grants=['sound mixing'], why='audio skill comes before paid sessions'),
    'stage technician': dict(grants=['stagecraft'], why='a venue or a crew takes on someone who already knows the work'),
    'professional athlete': dict(grants=['keeping fit'], why='years of academies and tryouts come before a contract'),
    'novelist': dict(grants=['writing stories'], why='a long writing practice comes before the first published book'),
    'professional conservator': dict(grants=['restoring old things'], why='a conservation degree and internships come first'),
    'search-and-rescue volunteer': dict(grants=['navigation'], why='a probationary year of training comes before a place on the team'),
}

ROLES.update(ROLES_V2)
ROLES.update(ROLES_P2)
for t_, r_ in TITLE_LINKS.items():
    d_ = dict(ROLES.get(t_) or {})
    for k_, v_ in r_.items():
        if k_ == "grants":
            d_["grants"] = list(d_.get("grants", [])) + [g_ for g_ in v_ if g_ not in d_.get("grants", [])]
        elif k_ != "why":
            d_[k_] = v_
    ROLES[t_] = d_
# only ever through an act (the packs, 07:21): a failed long shot (grants_if_fails), so every holder has a real scene behind
# it for the Book, the peace reading and the echoes; rate 0 means no draw "in time", and the rate fit leaves it out
ROLES_ACTS_ONLY = {"a long shot that missed": dict(rate=0),
                   # v25 A2: founding a movement only through its founding moment ('a following of your own', C5), never
                   # drawn "in time" with no cause (the catalogue: "a new movement founded in their lifetime, by them").
                   # Drawn in time it was every Historic life left alone (v24's refit doubled its norm, 1.109 to 2.021)
                   "founder of a movement": dict(rate=0)}
ROLES_ACTS_V25 = ("founder of a movement",)   # made acts-only by v25: with founder_moment off, the rule each had before
# One budget for big lives across all the packs on (Emren, pack ideas thread, relayed 08:14): about 1 life in 3 holds a big
# career and about 1 in 20 reaches a summit; community titles at 10x their real share, capped at 1 in 4 (batch.TARGET_CAP).
# Pack titles join a tier through the tier words in TARGET_<PACK> (batch._targets).
BUDGET = dict(career=1 / 3, summit=1 / 20, community=10.0, summit_floor=0.001,   # each summit in 1 life in 1,000 or more
              rung_cap=1.0,   # the lift raises a rung's yearly rate by at most e^1 (steps keep their pace)
              act_cap=0.7)    # and the odds of an act that gives one by at most e^.7, about double (Emren 14:41)
# The floors (item 16; Emren 10-09: "0.1% is not playable. Rare titles must be more reachable"): every summit in 1 life
# in 100 or more (the summit budget from 1 in 20 to about 1 in 7 to hold ten to twelve of them), every career above 1 in
# 100 (1.5%), and every other title of one's own doing and every perk in 1 life in 100 or more. Statuses keep their real
# shares: what befalls a life (refugee, widowed) is not a prize to make reachable. Off until the v22.3 refit: they apply
# when batch.FLOORS is True, over BUDGET (tools/tier_fit.py: FLOORS=1).
BUDGET_FLOORS = dict(summit=0.15, summit_floor=0.01, career_floor=0.015, title_floor=0.01, perk_floor=0.01)
# The fitted logit lift per tier, on the odds of the acts that give a pack career or summit and on their background rates,
# per set of packs on (",".join(sorted(packs))); "split": the extra lift per summit that brings each to its share of the
# summit budget (the square root of its real share). calib_v8/tier_fit.py writes it.
TIER_LIFT = {
    'art,callings,politics,science,stage': {"career": 2.51, "split": {"army officer": -2.7731, "art teacher": -3.0, "artistic director": 0.1233, "campaign organiser": -3.0, "casting director": 3.0, "celebrated author": 3.0, "celebrated inventor": 3.0, "chief executive": -2.489, "constituency caseworker": -3.0, "director": -3.0, "drama teacher": -0.9514, "evidence synthesis specialist": 3.0, "gallery owner": 2.147, "general": -0.447, "head of a faith order": 2.913, "head of government": 3.0, "illustrator for hire": -3.0, "independent investigator": -0.0878, "inventor": -0.7876, "lead actor or actress": -3.0, "lobbyist": -2.1687, "magnate": -0.8343, "master craftsperson": 2.7329, "mayor": -3.0, "member of parliament": -3.0, "minister": 3.0, "painter or sculptor": -3.0, "participatory research coordinator": 3.0, "party leader": 3.0, "party official": -0.4396, "playwright or screenwriter": 2.5074, "policy analyst": 2.4288, "political adviser": -2.893, "pollster": 3.0, "postdoctoral researcher": 3.0, "producer": 3.0, "professional actor": -3.0, "professor": 1.5285, "renowned artist": -3.0, "renowned healer": 0.2758, "research assistant": -2.833, "research data steward": 3.0, "research facility lead": -3.0, "research group leader": -2.4946, "research project lead": 2.0541, "research scientist": -1.9883, "research software engineer": 3.0, "science communication specialist": 1.4586, "senior cleric": 0.5325, "senior nurse or midwife": 2.1083, "speechwriter": 3.0, "stage manager": -0.7367, "street artist": -3.0, "talent agent": 3.0, "voice actor": 3.0}, "summit": 6.0},
    'art,politics,science,stage': {"career": 2.5666, "split": {"art teacher": -3.0, "artistic director": 0.7475, "campaign organiser": -1.4809, "casting director": 3.0, "celebrated author": 2.8124, "constituency caseworker": -1.842, "director": -3.0, "drama teacher": -0.0495, "evidence synthesis specialist": 3.0, "gallery owner": 3.0, "head of government": 3.0, "illustrator for hire": -3.0, "independent investigator": 0.9553, "lead actor or actress": -3.0, "lobbyist": -1.5035, "master craftsperson": 3.0, "mayor": -3.0, "member of parliament": -3.0, "minister": 3.0, "painter or sculptor": -3.0, "participatory research coordinator": 3.0, "party leader": 3.0, "party official": 0.9266, "playwright or screenwriter": 1.0832, "policy analyst": 0.9457, "political adviser": -2.3503, "pollster": 3.0, "postdoctoral researcher": 3.0, "producer": 2.6491, "professional actor": -2.602, "professor": 2.6301, "renowned artist": -3.0, "research assistant": -2.9139, "research data steward": 0.9608, "research facility lead": -3.0, "research group leader": -0.653, "research project lead": 0.6647, "research scientist": -2.3137, "research software engineer": 2.3706, "science communication specialist": 0.4028, "speechwriter": 3.0, "stage manager": -0.5815, "street artist": -3.0, "talent agent": 3.0, "voice actor": 3.0}, "summit": 6.0},
    'politics,science,stage': {"career": 4.5471, "split": {"artistic director": 2.0773, "campaign organiser": -2.4654, "casting director": 1.5328, "constituency caseworker": -2.3997, "director": -0.4846, "drama teacher": -0.6021, "evidence synthesis specialist": -1.5554, "head of government": 3.0, "independent investigator": -2.0594, "lead actor or actress": -3.0, "lobbyist": -1.6391, "mayor": -2.6445, "member of parliament": 1.0946, "minister": 3.0, "participatory research coordinator": 3.0, "party leader": 3.0, "party official": -0.9879, "playwright or screenwriter": -1.2509, "policy analyst": 1.362, "political adviser": 1.6598, "pollster": 3.0, "postdoctoral researcher": 3.0, "producer": -0.5221, "professional actor": -0.6582, "professor": -0.8054, "research assistant": -0.5191, "research data steward": 3.0, "research facility lead": -1.6856, "research group leader": -2.0694, "research project lead": -3.0, "research scientist": -2.2876, "research software engineer": 3.0, "science communication specialist": -1.3945, "speechwriter": 0.5772, "stage manager": -0.5504, "talent agent": 2.749, "voice actor": 3.0}, "summit": 3.8206},
}
ROLES.update(ROLES_ACTS_ONLY)
ROLES_OPTIONAL = set(ROLES_V2) | set(ROLES_P2) | set(ROLES_ACTS_ONLY)   # chroma-packs/core/longshot.py: only with packs on
ROLES = {k_: v_ for k_, v_ in ROLES.items() if v_ is not None and k_ == k_.strip()}
# v22.4, three green entry careers (chroma-packs/notes/v22.4-green-entries-for-library.md; the Library's catalogue
# entries) and two roads that name them. Read only with the switch green_jobs on (batch._roles compiles them beside the
# rules, as the sphere titles): off, a catalogue with the three titles gives them no rule of their own and every other
# title its rule above, as the v22.3 engine does. Each entry: (the titles it needs in the catalogue, the rule); a road
# for a sphere title (park ranger) stands in for its SPH_TITLE_ROLES rule
ROLES_WHEN = {
    # plain first jobs like [shop assistant], drawn by share and fit
    "gardener or groundskeeper": (["gardener or groundskeeper"], dict()),
    "farm hand": (["farm hand"], dict()),
    "animal care worker": (["animal care worker"],
                           dict(req="has('handling animals') | was('animal-shelter campaigner') | (age >= 18)")),
    # a farm hand of five years with savings can take on a farm (the packs' proposal)
    "farmer": (["farm hand"], dict(req="has('plot of land') | has('family business') | "
                                       "((yrs_has('farm hand') >= 5) & has('savings'))")),
    # three years on the grounds is a road to the ranger's post too
    "park ranger": (["gardener or groundskeeper"],
                    dict(after=["forester", "gardener or groundskeeper"],
                         req="(age >= 20) & (age <= 60) & (health > .5) & (was('scout or guide') | "
                             "was('search-and-rescue volunteer') | has('knowing the woods') | was('forester') | "
                             "(yrs_has('gardener or groundskeeper') >= 3))", entry=True)),
}
# E2 (cause_fit; "Every change has a cause", chroma-ideas/gameplay-2026-10-17/every-change-has-a-cause.md): the
# Library's cause audit (chroma-library/notes/cause-audit.md, tier A) tightens the rules whose cause line would read
# false, in place of the rule's req (its rate, after and lose kept), read only with cause_fit on. Kept as they are: the
# readings the engine does not have yet (the audit's NEW: stepparent, a family-arranged marriage, a first-generation
# student, residential care); the cat (with no dog from 'a pet of your own', the pet is the cat). The first two are the
# audit's precedence bugs
ROLES_FIT = {
    "boxing or martial arts": dict(req="(mkn('learned a skill') >= 2) & (age <= 40) & "
                                       "had(['a fight after school', 'someone starts mocking you online'], 3)"),
    "home nursing": dict(req="has('carer for a parent') | ((mkn('helped someone in need') >= 2) & "
                             "had(['flu, alone in a rented room', 'your child falls seriously ill', "
                             "'your partner falls seriously ill'], 3))"),
    "parent of three or more": dict(req="has('mother or father') & (alive_child >= 3) & had(['a child is born'], 1)"),
    "foster parent": dict(req="(age >= 25) & (money > .4) & (mk('took them in', 2) | "
                              "had(['you take in a child who needs a home'], 1))"),
    "adoptive parent": dict(req="(age >= 25) & ~held_children & (mk('took them in', 2) | "
                                "had(['you take in a child who needs a home'], 1))"),
    "grandparent": dict(req="has('mother or father') & had(['your first grandchild', \"a grandchild's visit\", "
                          "'teaching a grandchild to fish', \"a call from the grandchild's parent\"], 1)"),
    "convert": dict(req="held_faith & (was('seeker') | had(['welcomed into a community', 'a friend takes another faith', "
                        "'a new faith comes to town'], 2))"),
    "graduate": dict(req="has('school-leaving certificate') & (age >= 20) & "
                         "(had(['you win a scholarship or a place'], 12) | was('first-generation university student') | "
                         "had(['the first in the family to graduate', 'pens down on the last exam', 'the degree show', "
                         "'a degree and a job at the till'], 2))"),
    "has killed in war": dict(req="has('soldier') & had(['war comes', 'the unit comes home one short', "
                                "'home from the posting, and not the same'], 3)"),
    "immigrant": dict(req="had(['the first months in a new country', 'work and a room abroad, if you go this month'], 1)"),
    "someone with a record": dict(req="mk('broke the law', 2)"),
    "ex-prisoner": dict(req="has('someone with a record') & ((yrs_out < 1) | had(['the first night in a cell'], 6))"),
    "cancer survivor": dict(req="had(['a frightening diagnosis'], 3) & (health > .4)"),
    "citizenship": dict(req="(has('immigrant') & (yrs_has('immigrant') >= 5)) | had(['the oath of citizenship'], 1)"),
    "drinks licence": dict(req="~has('someone with a record') & (age >= 18) & (has('shop owner') | has('waiter or bartender'))"),
    "local hero": dict(req="had(['a stranger saves you, or you save one'], 1) & mk('helped someone in need', 1)"),
    "friend for life": dict(req="had(['a friend for life', 'a best friend of your own'], 2)"),
    "dog of one's own": dict(req="had(['a stray dog follows you home'], 1)"),
    "inheritance": dict(req="had(['a parent dies', 'a grandparent dies', 'losing a grandparent', 'an unexpected legacy'], 1)"),
    "scholarship": dict(req="had(['you win a scholarship or a place'], 1)"),
    "parent of an only child": dict(req="has('mother or father') & (yrs_children >= 4) & (kid_young >= yrs_children - .1) & "
                                        "~was('parent of an only child')"),
    "guardian of an unrelated child": dict(req="(age >= 21) & had(['you take in a child who needs a home'], 1) & "
                                               "mk('took them in')"),
    "former foster child": dict(req="had(['going into foster care'], 110)"),
    "asylum applicant": dict(req="(ago_move < 1) & had(['war comes'], 3) & ~was('asylum applicant')"),
    "displaced by a disaster": dict(req="had(['the flood wall gives way'], 1) | (had(['losing the home'], 1) & "
                                      "had(['war comes', 'the street pulls together after the storm', "
                                      "'the flood in the community centre'], 2))"),
    "award for bravery": dict(req="(has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                  "has('paramedic') | has('police officer') | has('soldier') | has('local hero')) & "
                                  "had(['a stranger saves you, or you save one'], 1)"),
    "business partner": dict(req="(age >= 18) & (has('founder of a firm') | has('shop owner') | "
                                 "had(['a friend wants to start a project with you', 'a chance to start a business of your "
                                 "own'], 2)) & mk('made a friend', 5)"),
    "godchild": dict(req="had(['asked to stand for a child at the naming'], 1) | ((age >= 16) & (has('friend for life') | "
                         "(alive_sibling > 0)) & (mkn('made a friend') >= 2) & chance(.1))"),
}
SPH_TITLE_ROLES = {
    # rule
    "lay judge": dict(req="(age >= 25) & (age <= 70) & ~has('someone with a record') & "
                          "(was('court clerk') | was('community-mediation volunteer') | has('good name in town'))",
                      rate=0.004, starts=True, weight="colors"),
    "paralegal": dict(req="has('school-leaving certificate') & (age >= 18)"),
    "lawyer": dict(after=["paralegal"], req="has('graduate') & has('professional registration') & (age >= 23)",
                   entry=True),
    "mediator": dict(req="(age >= 25) & (has('mediation accreditation') | (yrs_has('community-mediation volunteer') >= 3))"),
    # gather
    "community centre manager": dict(req="(age >= 21) & ((yrs_has('community-kitchen volunteer') >= 2) | "
                                         "(yrs_has('neighbourhood volunteer') >= 3) | was('club treasurer'))"),
    "events promoter": dict(after=["waiter or bartender"], req="(age >= 18) & (was('club treasurer') | "
                            "was('festival organiser') | has('waiter or bartender') | has('organising people'))", entry=True),
    "DJ": dict(after=["waiter or bartender"], req="(age >= 16) & (has('musical instrument') | has('sound mixing') | "
               "was('amateur band member'))", entry=True),
    "café or bar owner": dict(after=["waiter or bartender", "cook", "head chef"],
                              req="(age >= 21) & (has('savings') | has('family business'))", entry=True),
    # arts
    "music teacher": dict(after=["session player"], req="(age >= 18) & has('musical instrument')", entry=True),
    "touring musician": dict(after=["session player"], req="(age >= 17) & has('musical instrument') & "
                             "(was('amateur band member') | was('session player'))", entry=True),
    "folk musician": dict(req="(age >= 12) & (has('musical instrument') | has('singing'))", rate=0.0015, starts=True,
                          weight="colors"),
    "craft maker": dict(after=["apprentice", "carpenter"], req="(age >= 18) & (has('workshop') | (mkn('learned a skill') >= 2))",
                        entry=True),
    # faith
    "independent preacher": dict(after=["regular worshipper", "convert", "street preacher"],
                                 req="(yrs_faith >= 3) & (age >= 21) & (has('public speaking') | has('scripture'))",
                                 rate=0.0004, weight="colors"),
    # care
    "complementary therapist": dict(req="age >= 18"),
    "physiotherapist": dict(req="has('graduate') & has('professional registration') & (age >= 22)"),
    "hospice volunteer": dict(req="(age >= 16) & ((mkn('helped someone in need') >= 1) | was('carer for a parent') | "
                                  "had(['your partner dies', 'a parent dies'], 10))", rate=0.0003, starts=True, weight="colors"),
    # learn
    "teaching assistant": dict(req="(age >= 17) & ~has('someone with a record')"),
    "consultant": dict(after=["accountant", "data analyst", "teacher", "private tutor"], req="has('graduate') & (age >= 23)",
                       entry=True),
    "mechanic": dict(after=["apprentice"], req="(age >= 16) & (has('car mechanics') | was('apprentice') | "
                     "was('repair-cafe volunteer'))", entry=True),
    "community language teacher": dict(req="(age >= 15) & has('second language')", rate=0.0006, starts=True, weight="colors"),
    "outdoor instructor": dict(req="(age >= 18) & (age <= 60) & (health > .6) & (was('scout or guide') | was('youth coach') | "
                               "was('search-and-rescue volunteer') | has('knowing the woods'))"),
    # prod
    "quality inspector": dict(after=["factory worker"], req="(age >= 17) & (has('school-leaving certificate') | "
                              "(yrs_career >= 2))", entry=True),
    # comm
    "standards inspector": dict(after=["market porter", "office clerk", "shop assistant"],
                                req="(age >= 21) & ~has('someone with a record') & has('school-leaving certificate')", entry=True),
    "market trader": dict(after=["shop assistant", "salesperson", "market porter"], req="age >= 16", entry=True),
    "savings-circle member": dict(req="(age >= 16) & (money < .6)", rate=0.0008, starts=True, weight="colors"),
    # prot
    "detective": dict(after=["police officer"], req="(yrs_career >= 3) & (age >= 23) & ~has('someone with a record')"),
    "private investigator": dict(after=["police officer", "security guard", "door staff", "journalist"],
                                 req="(age >= 21) & ~has('someone with a record')", entry=True),
    "park ranger": dict(after=["forester"], req="(age >= 20) & (age <= 60) & (health > .5) & (was('scout or guide') | "
                        "was('search-and-rescue volunteer') | has('knowing the woods') | was('forester'))", entry=True),
}
