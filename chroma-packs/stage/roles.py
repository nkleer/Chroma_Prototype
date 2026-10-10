# Chroma content pack: Stage and Screen. The engine's reading of how each title and perk comes and goes, proposed in
# earth_rules.ROLES syntax (chroma-engine/prototype/earth_rules.py, "ROLES = {"). Plain data for the engine thread, which
# owns the rules and refits every rate to the catalogue's shares (ROLE_NORM). Condition words are the ones the engine
# has today (batch.COND_VOCAB): has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark'), had(['situation'], years),
# age, money, time, yrs_career, ago_move, retired.
#
# Most steps in this pack are taken by the player's own act at a door or a crossing (title: on an option in the pack's
# moments), so the background rates below are low: they stand for the ordinary lives that drift onto the stage without
# a door moment, and the engine fits them so the simulated shares match the catalogue. Every req is narrow, as the
# calibration of Science and Politics taught (../calibration.md, issue 3): the pathway's own earlier title, a skill or a
# history mark, never a bare age or [graduate]. Parts are won in the moments ('the understudy goes on', 'the part of a
# lifetime is cast', 'a screen test'), whose option chances carry the real odds; the background rule for the lead stands
# for the same casting in a life that never meets the moment. Rules are checked every four weeks, so odds belong in
# rate, never in chance() inside req (engine, 22:12).

ROLES_STAGE = {
    # Every career and summit names the rung below it (Emren 09:18): a title of the rung below, or years on the rung
    # below that, never a perk alone.
    # Round 5, 2026-10-07 (checklist P8): every career and summit lists its rungs below in rungs= (or refines), so the
    # engine's "from nothing" check can read them, and every title its req names is among them. rungs=, not after=:
    # after= would let the rule come only to someone who still holds the rung (a year or more) and drop it on the step,
    # which shuts the was() roads (the actor who left, the drama school that ended) and the community director's
    # society kept beside the job; a career title replaces the one held anyway (one career at a time). The lists also
    # name the rungs the moments use: [voice actor] where 'leaving acting for another life' comes to voice actors,
    # [professional actor] for stage management (the actor who moves to the prompt desk).
    # Round 5 (P5): the careers at 3x their target or more (pooled 11b and 12b: voice actor 4.4, casting director 4.0,
    # stage manager 3.8, playwright or screenwriter 3.75, drama teacher 3.2, talent agent 3.0, the lead 3.05) mostly
    # came "in time", by these rules, where the engine's split lift had already reached -3: their rates are lowered
    # title by title (the old rate in each comment) and the moments carry more of the road (shown, not given).
    # careers: the actor's road
    "professional actor": dict(req="(was('drama school student') & ~has('drama school student')) | was('understudy') | "
                                   "(has('acting') & ((yrs_has('amateur actor') >= 2) | "
                                   "(yrs_has('background artist') >= 2)) & (has('union card') | "
                                   "has('casting directory listing') | has('a fringe slot')))",
                               rungs=["drama school student", "understudy", "amateur actor", "background artist"],
                               rate=0.003, starts=True, entry=True, weight="colors",
                               lose="yrs_has('professional actor') >= 2", lrate=0.15,
                               lwhy="the work dried up, and the day job took over"),
    # round 5: rate .002 to .0007 (P5, 4.4x)
    "voice actor": dict(req="has('accents and voices') & (was('professional actor') | (yrs_has('amateur actor') >= 2) | "
                            "(yrs_has('community-radio presenter') >= 2))",
                        rungs=["professional actor", "amateur actor", "community-radio presenter"],
                        rate=0.0007, entry=True, weight="colors"),
    # the lead: a facet on the actor's title, for a run or a series (the background twin of the casting moments)
    # round 5: rungs= names the understudy its req reads and the amateur of five years with a lead behind them (the
    # one-rung skip of 'the lead from the open queue' and 'the part of a lifetime is cast'); rate .02 to .015 (P5, 3.05x)
    "lead actor or actress": dict(refines="professional actor; voice actor", rungs=["understudy", "amateur actor"],
                                  req="(has('professional actor') | has('voice actor')) & (yrs_career >= 2) & "
                                      "(has('good notices') | has('an agent who believes in you') | "
                                      "has('a director who keeps casting you') | was('understudy') | has('a known face'))",
                                  rate=0.015, weight="colors", grants=["a lead role to remember"],
                                  lose="yrs_has('lead actor or actress') >= 1", lrate=0.4,
                                  lwhy="the run ended, and the next part was a smaller one"),
    "director": dict(req="has('directing actors') & ((yrs_has('community theatre director') >= 3) | "
                         "(yrs_has('stage manager') >= 3) | (yrs_has('professional actor') >= 3))",
                     rungs=["community theatre director", "stage manager", "professional actor"],
                     rate=0.05, entry=True, weight="colors"),
    # round 5 (P3): director stints in the engine last about 1 to 4.5 years (its general job turnover), so five years
    # on the rung was met by almost nobody: three years now, at rate .05 (was .02); rungs= adds the community director's
    # one-rung skip ('the old theatre needs someone to save it' gives the facet with its title)
    "artistic director": dict(refines="director", rungs=["community theatre director"],
                              req="has('director') & (yrs_has('director') >= 3) & (has('good notices') | "
                                  "has('a company of your own') | has('a producer who backs you'))",
                              rate=0.05, weight="ties", lose="yrs_has('artistic director') >= 6", lrate=0.15,
                              lwhy="the board chose a new artistic director"),
    "playwright or screenwriter": dict(req="has('writing scripts') & (was('novelist') | was('journalist') | "
                                           "((yrs_has('writing scripts') >= 2) & (was('professional actor') | "
                                           "was('drama school student') | was('amateur actor') | "
                                           "was('community theatre director'))))",
                                       rungs=["novelist", "journalist", "professional actor", "drama school student",
                                              "amateur actor", "community theatre director"],
                                       rate=0.004, entry=True, weight="colors"),   # round 5: .015 to .004 (P5, 3.75x)
    # round 5: a company of one's own is the rung kept on the step (rungs=); rate .05 to .012, all its first gains came
    # "in time" (P5, P16: 'the city wants the town's show' and the old theatre carry the road now); weight "colors" (was
    # "money"): its single-color profile is Black, the road it leads (P12)
    "producer": dict(req="(has('striking a deal') | has('organising people')) & (was('stage manager') | "
                         "has('a company of your own') | was('director') | "
                         "(yrs_has('community theatre director') >= 3))",
                     rungs=["stage manager", "director", "community theatre director", "a company of your own"],
                     rate=0.012, entry=True, weight="colors"),
    # careers: side roads (no after: a career title replaces the one held, and after would shut out every other road in)
    # round 5: rate .003 to .0005 (P5, 3.8x)
    "stage manager": dict(req="has('stagecraft') & (was('stage technician') | was('drama school student') | "
                              "(yrs_has('amateur actor') >= 2) | (yrs_has('community theatre director') >= 2))",
                          rungs=["stage technician", "drama school student", "amateur actor", "community theatre director",
                                 "professional actor", "voice actor"],
                          rate=0.0005, entry=True, weight="colors"),
    # round 5: rate .01 to .0025, all its first gains came "in time" (P5, 4.0x); weight "colors" (was "ties"): its
    # single-color profile is White, the road it leads (P12)
    "casting director": dict(req="(has('a casting eye') & (was('professional actor') | was('talent agent') | "
                                 "was('stage manager') | was('producer') | was('director'))) | "
                                 "(was('drama teacher') & (yrs_career >= 5))",   # 10-09 floors (Emren: rare titles reachable): a drama teacher's road
                             rungs=["professional actor", "talent agent", "stage manager", "producer", "director",
                                    "voice actor"],
                             rate=0.0025, entry=True, weight="colors"),
    # round 5: the casting eye alone no longer stands in for a rung (it named no title); rate .012 to .004, all its
    # first gains came "in time" (P5, 3.0x); weight "colors" (was "ties"): its single-color profile is Black (P12)
    "talent agent": dict(req="(has('striking a deal') | has('selling')) & (was('professional actor') | "
                             "was('casting director') | was('producer'))",
                         rungs=["professional actor", "casting director", "producer", "voice actor"],
                         rate=0.004, entry=True, weight="colors"),
    # related to the base teacher: a teacher with acting moves into it ("a new job inside the career"), and so does an
    # actor who teaches; no after, which would end the road for the actor who never held [teacher]
    # round 5: the teacher's way in needs two years of teaching and the local players behind them (a youth theatre in
    # childhood, a quarter of all lives, was far too wide); rate .02 to .005, nearly all its first gains came "in time"
    # (P5, 3.2x); 'the school needs someone to take drama' carries the teacher's road now (P16)
    "drama teacher": dict(req="has('acting') & (was('drama school student') | was('professional actor') | "
                              "(has('teacher') & (yrs_has('teacher') >= 2) & (was('amateur actor') | "
                              "was('community theatre director'))))",
                          rungs=["drama school student", "professional actor", "teacher", "amateur actor",
                                 "community theatre director", "voice actor"],
                          rate=0.005, entry=True, weight="colors"),
    # community
    "background artist": dict(req="(age >= 16) & (has('amateur actor') | has('casting directory listing') | "
                                  "(was('youth theatre member') & has('acting')))",
                              rate=0.0003, starts=True, weight="colors",
                              lose="yrs_has('background artist') >= 1", lrate=0.3, lwhy="the calls stopped coming"),
    "amateur actor": dict(req="(age >= 14) & (was('youth theatre member') | has('acting') | "
                              "has('a lead role to remember'))",
                          rate=0.003, starts=True, weight="colors",
                          lose="yrs_has('amateur actor') >= 3", lrate=0.12, lwhy="no time for rehearsals any more"),
    "youth theatre member": dict(req="(age <= 17) & (had(['the school play'], 3) | has('acting'))",
                                 rate=0.001, starts=True, weight="colors",
                                 lose="yrs_has('youth theatre member') >= 2", lrate=0.3,
                                 lwhy="dropped it for exams and friends"),
    "community theatre director": dict(req="(has('amateur actor') & (yrs_has('amateur actor') >= 4)) | "
                                           "(has('directing actors') & (has('amateur actor') | has('drama teacher')))",
                                       rate=0.0005, starts=True, weight="colors",
                                       lose="yrs_has('community theatre director') >= 5", lrate=0.2,
                                       lwhy="handed the society on"),
    # statuses (they fade by their lasts: three years at drama school, one run as understudy)
    "drama school student": dict(req="(age >= 17) & (age <= 30) & has('acting') & (was('youth theatre member') | "
                                     "has('a lead role to remember') | was('amateur actor'))",
                                 rate=0.003, weight="colors"),
    "understudy": dict(req="has('professional actor') & has('learning lines') & ~has('lead actor or actress')",
                       rate=0.05, weight="colors"),
    # skills: learned on the job (rates per year while the job is held)
    "acting": dict(req="has('youth theatre member') | has('amateur actor') | has('drama school student') | "
                       "has('professional actor') | has('drama teacher') | has('background artist')",
                   rate=0.1, weight="practice"),
    "screen acting": dict(req="(has('professional actor') | has('background artist')) & has('acting')", rate=0.06,
                          weight="practice"),
    "improvisation": dict(req="has('youth theatre member') | has('amateur actor') | has('drama school student') | "
                              "has('a fringe slot')", rate=0.02, weight="practice"),
    "stage combat": dict(req="has('drama school student') | (has('professional actor') & has('boxing or martial arts'))",
                         rate=0.1, weight="practice"),
    "accents and voices": dict(req="has('drama school student') | has('voice actor') | (has('professional actor') & "
                                   "has('second language')) | (yrs_has('community-radio presenter') >= 1) | "
                                   "(yrs_has('amateur actor') >= 3)", rate=0.06, weight="practice"),
    "learning lines": dict(req="has('amateur actor') | has('professional actor') | has('drama school student') | "
                               "has('understudy')", rate=0.04, weight="practice"),
    "auditioning": dict(req="has('professional actor') | has('drama school student') | has('background artist') | "
                            "has('casting directory listing')", rate=0.05, weight="practice"),
    "telling a story aloud": dict(req="has('drama teacher') | has('community theatre director') | "
                                      "has('community-radio presenter') | (has('grandparent') & has('acting'))",
                                  rate=0.04, weight="practice"),
    # round 5 (P3): also the stage manager of three years and the actor of five, who watch directors at work every day,
    # so the director's road from the stage management and acting rungs is open, not only from the community director's
    "directing actors": dict(req="has('director') | has('community theatre director') | has('drama teacher') | "
                                 "(has('amateur actor') & (yrs_has('amateur actor') >= 8)) | "
                                 "(yrs_has('stage manager') >= 3) | (yrs_has('professional actor') >= 5)", rate=0.05,
                             weight="practice"),
    "a casting eye": dict(req="has('casting director') | has('talent agent') | has('director') | has('producer')",
                          rate=0.05, weight="practice"),
    "writing scripts": dict(req="has('playwright or screenwriter') | ((has('writing stories') | has('improvisation')) & "
                                "(has('amateur actor') | has('professional actor') | has('a fringe slot') | "
                                "has('drama teacher')))",
                            rate=0.05, weight="practice"),
    "calling the show": dict(req="has('stage manager') | (has('stagecraft') & has('amateur actor'))", rate=0.1,
                             weight="practice"),
    # access
    "union card": dict(req="has('professional actor') | has('stage manager') | has('voice actor') | "
                           "(has('background artist') & (yrs_has('background artist') >= 2))", rate=0.3,
                       lose="~has('professional actor') & ~has('stage manager') & ~has('voice actor') & "
                            "~has('director') & (yrs_has('union card') >= 3)", lrate=0.1,
                       lwhy="let the membership lapse"),
    # the course ends with the diploma (a few leave early; the moments that end it early carry drops:)
    "drama school diploma": dict(req="was('drama school student') & ~has('drama school student')", rate=0.9),
    "child performance licence": dict(req="(age <= 15) & has('youth theatre member') & has('acting')", rate=0.3,
                                      lose="yrs_has('child performance licence') >= 1", lrate=0.5,
                                      lwhy="the production over"),
    "casting directory listing": dict(req="has('professional actor') | has('drama school diploma') | "
                                          "has('background artist') | has('voice actor')", rate=0.15, weight="money",
                                      lose="~has('professional actor') & ~has('background artist') & ~has('voice actor')",
                                      lrate=0.3, lwhy="stopped paying for the listing"),
    "a fringe slot": dict(req="(has('writing scripts') | has('a company of your own') | has('improvisation')) & "
                              "(has('amateur actor') | has('drama school student') | has('professional actor'))",
                          rate=0.08, weight="money", lose="yrs_has('a fringe slot') >= 0.5", lrate=1.0,
                          lwhy="the festival ended"),
    # standing
    "a lead role to remember": dict(req="has('youth theatre member') | has('amateur actor')", rate=0.015,
                                    weight="colors"),
    "good notices": dict(req="(has('professional actor') | has('director') | has('playwright or screenwriter')) & "
                             "(yrs_career >= 2)", rate=0.08, weight="colors"),
    "a known face": dict(req="has('screen acting') & (has('professional actor') | has('lead actor or actress')) & "
                             "(yrs_has('screen acting') >= 2)", rate=0.02),
    "an award for acting": dict(req="has('lead actor or actress') | (has('professional actor') & has('good notices')) | "
                                    "(has('amateur actor') & has('a lead role to remember'))", rate=0.008),
    "a cult following": dict(req="(was('a fringe slot') | has('voice actor') | has('lead actor or actress')) & "
                                 "(has('following online') | has('a known face'))", rate=0.01),
    # bonds
    "an agent who believes in you": dict(req="(has('professional actor') | has('voice actor') | "
                                             "has('playwright or screenwriter') | has('director')) & "
                                             "(has('good notices') | has('a showreel') | has('drama school diploma'))",
                                         rate=0.1, weight="ties"),
    "a director who keeps casting you": dict(req="has('professional actor') & (yrs_has('professional actor') >= 2) & "
                                                 "mk('kept your word', 5)", rate=0.02, weight="ties"),
    "a company that feels like family": dict(req="(has('amateur actor') & (yrs_has('amateur actor') >= 2)) | "
                                                 "(has('youth theatre member') & (yrs_has('youth theatre member') >= 2)) | "
                                                 "(has('professional actor') & mk('made a friend', 2))",
                                             rate=0.03, weight="ties"),
    "a year group from drama school": dict(req="has('drama school student') & (yrs_has('drama school student') >= 1)",
                                           rate=0.3, weight="ties"),
    "a producer who backs you": dict(req="(has('lead actor or actress') | has('director') | "
                                         "has('playwright or screenwriter')) & (has('good notices') | "
                                         "has('an award for acting'))", rate=0.02, weight="ties"),
    # assets
    "a showreel": dict(req="(has('professional actor') & (has('screen acting') | has('casting directory listing'))) | "
                           "has('voice actor')", rate=0.2,
                       weight="money", lose="yrs_has('a showreel') >= 6", lrate=0.3, lwhy="the reel went out of date"),
    "repeat fees": dict(req="has('screen acting') & (has('a known face') | has('lead actor or actress') | "
                            "has('voice actor'))", rate=0.1, weight="money",
                        lose="yrs_has('repeat fees') >= 5", lrate=0.2, lwhy="the series went off the air"),
    "a company of your own": dict(req="(has('writing scripts') | has('directing actors') | has('producer')) & "
                                      "(was('a fringe slot') | has('amateur actor') | has('professional actor') | "
                                      "has('community theatre director'))", rate=0.03, weight="money",
                                  lose="money < .1", lrate=0.3, lwhy="the money ran out"),
}

# Additions to rules the pack does not own (the pack never rewrites a base or core rule; these widen who can gain
# them). A string is or-ed into the rule's req at that rule's own rate (batch._roles, EXTEND):
#   - the core [known across the country] (science/roles.py, ROLES_REACH) can also come to a lead with a face, an award
#     or a series that keeps airing: the background twin of 'the show is a hit';
#   - the base [stagecraft] also comes to stage managers and to the people who run the local players;
#   - the base [name on the local scene] also comes to the amateur who played the lead the town remembers, and to the
#     one who directs the town's plays;
#   - the base [cleared to work with children] also comes to drama teachers and community theatre directors, with the
#     base rule's own record check;
#   - the base studio of one's own also comes to a voice actor who builds a booth at home.
EXTEND_STAGE = {
    "known across the country": "has('lead actor or actress') & (has('a known face') | has('an award for acting') | "
                                "has('repeat fees'))",
    "stagecraft": "has('stage manager') | has('community theatre director')",
    "name on the local scene": "(has('amateur actor') & has('a lead role to remember')) | "
                               "has('community theatre director')",
    "cleared to work with children": "(age >= 16) & ~has('someone with a record') & (has('drama teacher') | "
                                     "has('community theatre director'))",
    "studio of one's own": "has('voice actor') & (money > .2)",
}

# Fit targets (batch._targets, engine 08:21; Emren's one budget for all packs, 08:11): a tier word per title. The engine
# fits one lift per tier on the acts that give its titles and on their background rates, so the loaded packs together
# give about 1 life in 3 a career and about 1 in 20 a summit (earth_rules.BUDGET); the summit budget is split by the
# square root of each summit's real share. Community, status and entry titles get BUDGET["community"] times their real
# share, capped at .25 (youth theatre member and amateur actor reach the cap). The catalogue keeps the real shares.
# Perks keep a multiple (ROLE_NORM), since an item without a target is fitted back to its real share: perks follow
# their holders, 10x for the craft, credential, standing, bond and asset perks of the careers, 3x to 5x for the perks of
# youth theatre and amateur acting, and 4x, where it stands, for [a director who keeps casting you], which opens 'the
# director calls again', the crossing that already wins most often.
TARGET_STAGE = {
    # careers
    "professional actor": "career", "voice actor": "career", "playwright or screenwriter": "career",
    "producer": "career", "stage manager": "career", "casting director": "career", "talent agent": "career",
    "drama teacher": "career",
    # summits
    "lead actor or actress": "summit", "director": "summit", "artistic director": "summit",
    # community, status and entry titles
    "background artist": "community", "amateur actor": "community", "youth theatre member": "community",
    "community theatre director": "community", "drama school student": "community", "understudy": "community",
    # perks of the careers
    "screen acting": 10, "stage combat": 10, "accents and voices": 10, "auditioning": 10, "directing actors": 10,
    "a casting eye": 10, "writing scripts": 10, "calling the show": 10, "union card": 10, "drama school diploma": 10,
    "casting directory listing": 10, "a fringe slot": 10, "good notices": 10, "a known face": 10,
    "an award for acting": 10, "a cult following": 10, "an agent who believes in you": 10,
    "a director who keeps casting you": 4, "a year group from drama school": 10, "a producer who backs you": 10,
    "a showreel": 10, "repeat fees": 10, "a company of your own": 10,
    # perks of youth theatre and amateur acting
    "acting": 4, "improvisation": 4, "learning lines": 5, "telling a story aloud": 3, "child performance licence": 3,
    "a lead role to remember": 4, "a company that feels like family": 4,
}
