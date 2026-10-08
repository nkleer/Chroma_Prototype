# Chroma content pack: Politics, Elections and Public Office. The engine's reading of how each title and perk comes
# and goes, proposed in earth_rules.ROLES syntax (chroma-engine/prototype/earth_rules.py, "ROLES = {"). Plain data for
# the engine thread, which owns the rules and refits every rate to the catalogue's shares (ROLE_NORM). Condition words
# are the ones the engine has today (batch.COND_VOCAB): has('x'), was('x'), yrs_has('x'), mk('mark'), mkn('mark'),
# had(['situation'], years), chance(p), age, money, held_career, yrs_career, yrs_faith, ago_move.
#
# Most steps in this pack are taken by the player's own act at a door or a crossing (title: on an option in the
# pack's moments), so the background rates below are low: they stand for the ordinary lives that drift into politics
# without a door moment, and the engine fits them so the simulated shares match the catalogue. Elections are won in
# the moments ('polling day in the ward', 'election night'), whose option chances carry the real odds; the background
# rule for a seat stands for the same race in a life that never meets the moment.

ROLES_POLITICS = {
    # Round 5, 2026-10-07 (release checklist P5, P7, P12): every name a req uses is in its after= or rungs= (or the title
    # it refines), so the engine can verify each step; each road leans to its colors (weight="colors" on its careers;
    # minister and mayor keep "ties", as office comes through allies and votes); and the careers that ran above three
    # times their target in the 10-06 fits (campaign organiser, party official, lobbyist, constituency caseworker,
    # speechwriter) have lower background rates, about half again to allow for the colors weight (about 2 on average).
    # Roads (PACK.md, "Roads per color"): W party and office (party official, polling-station volunteer, member of
    # parliament, minister, head of government); U policy and polling (policy analyst, pollster); B lobbying and the
    # back room (lobbyist, political adviser); R campaigning and the bold bid (campaign volunteer, campaign
    # organiser, speechwriter, party leader); G the ward, the caseworker and the town (constituency caseworker, local
    # party officer, mayor).
    # careers: the road to parliament and office
    # round 5: a volunteer or a branch officer now (has, not was), so a job move in later life no longer lands here from a
    # season of leaflets decades ago (11b: 4 in 10 organisers came by "changed jobs"); rate .01 to .004 with the colors
    # weight, and the organiser's post at 'a paid job on the campaign' is Red's alone (White's is the party's head office)
    "campaign organiser": dict(req="(has('campaign volunteer') | has('local party officer')) & (age <= 60)",
                               after=["campaign volunteer", "local party officer"], rate=0.004, entry=True,
                               weight="colors",
                               lose="yrs_has('campaign organiser') >= 2", lrate=0.4,
                               lwhy="the campaign over, and no next one"),
    # round 5: [party member], [graduate] and [handling red tape], named in req, are rungs; rate .02 to .008 with the
    # colors weight (12b: 3.6x)
    "constituency caseworker": dict(req="(has('graduate') | has('handling red tape')) & (was('campaign volunteer') | "
                                        "has('party member')) & (age <= 60)",
                                    after=["campaign organiser", "office clerk", "campaign volunteer",
                                           "local party officer"], rungs=["party member", "graduate", "handling red tape"],
                                    rate=0.008,
                                    entry=True, weight="colors"),
    # round 5: [graduate] and [campaigning] are rungs; rate .1 to .05 with the colors weight (about 1x its target in the
    # 10-06 fits)
    "political adviser": dict(req="(has('graduate') | has('campaigning')) & ((yrs_has('campaign organiser') >= 1) | "
                                  "(yrs_has('constituency caseworker') >= 1) | (yrs_has('policy analyst') >= 1) | "
                                  "(yrs_has('party official') >= 1) | (yrs_has('journalist') >= 3))",
                              after=["campaign organiser", "constituency caseworker", "policy analyst",
                                     "party official", "journalist"], rungs=["graduate", "campaigning"], rate=0.05,
                              entry=True,
                              weight="colors"),
    # the seat comes to a candidate on a winnable seat's nomination; a paper candidate or an independent wins only at
    # 'election night', at the written chance times its lacking: share
    # round 5: [parliamentary nomination] is a rung, since 'election night' also comes to a nominee (round 4) before the
    # candidacy rule has reached them
    "member of parliament": dict(req="has('parliamentary candidate') & has('parliamentary nomination')",
                                 after=["parliamentary candidate"], rungs=["parliamentary nomination"], rate=0.0005,
                                 starts=True, weight="colors",
                                 lose=[("(yrs_has('member of parliament') >= 1) & chance(.5)",
                                        "lost the seat at an election"),
                                       ("(age >= 60) & (yrs_has('member of parliament') >= 10)", "stood down")],
                                 lrate=0.12, lend="lost job"),
    # facets: office on top of the seat (refines; they end with it)
    # the engine reads rate as a yearly rate among members of two years or more (engine fit, 14:00): about 1 member in 3
    # ever holds office, so .05 a year (it was .0002, a population share, and no member ever became a minister)
    # Round 5, 2026-10-07 (P4, P10, P16): 'the phone call from the leader' is back at its times line (.06 a year; nine
    # options in ten take the post, at 40 to 88), which alone gives about .05 a year; members leave the seat at about
    # .13 a year here, so the call and this rule together (about .07 a year) make about 1 member in 4 to 1 in 3 a
    # minister, the real share. Rate .05 to .02, so the call carries the road and more members meet office (the call,
    # and 'the leadership falls vacant' after four years: about .095 a year) than hold it.
    "minister": dict(refines="member of parliament",
                     req="has('member of parliament') & (yrs_has('member of parliament') >= 2)", rate=0.02,
                     weight="ties", lose="yrs_has('minister') >= 1", lrate=0.3, lwhy="moved out at a reshuffle"),
    "party leader": dict(refines="member of parliament",
                         req="has('member of parliament') & (yrs_has('member of parliament') >= 4) & "
                             "(was('minister') | has('a following in the party') | has('known across the country'))",
                         rungs=["minister", "a following in the party", "known across the country"],
                         rate=0.02, weight="colors", grants=["known across the country"],   # round 4: as written, not
                         # fitted (TARGET below), so about 1 member in 10 ever leads a party
                         lose="yrs_has('party leader') >= 2", lrate=0.15, lwhy="replaced by the party"),
    "head of government": dict(refines="party leader",
                               req="has('party leader') & has('known across the country')",
                               rungs=["known across the country"], rate=0.05,   # round 4: about 1 leader in 3
                               grants=["a household name"], lose="yrs_has('head of government') >= 1", lrate=0.2,
                               lwhy="the government fell, or the term ran out"),
    # careers: side roads
    # round 5 (P5, P16): 11b 4.8x, 12b 2.4x, nearly all of it this rule (5 in 6 grew from local party officer), and the
    # post was barely met (.002 to .004 of lives). Rate .006 to .0012 with the colors weight; the post now has doors of
    # its own, each from the rung below: White's single at 'a paid job on the campaign' (a volunteer or branch officer
    # of a year), the White and Black pair at 'a seat the party cannot win' (a branch officer), and the letter. So
    # [campaign volunteer] and [party member] are rungs, with [member of parliament] (a post at headquarters after a lost
    # seat, 'the night you lose the seat').
    "party official": dict(req="(yrs_has('local party officer') >= 1) | (yrs_has('campaign organiser') >= 1)",
                           after=["local party officer", "campaign organiser"],
                           rungs=["campaign volunteer", "party member", "member of parliament"], rate=0.0012,
                           entry=True, weight="colors"),
    # round 5 (P5, P7): a former member was in req but not a rung, so a member who changed jobs into lobbying counted as
    # "from nothing" (12b); [member of parliament] is now a rung, with [mayor] and [campaign organiser], whom 'leaving
    # politics for another life' can also take to a lobbying firm. Rate .045 to .008 with the colors weight: in 11b over
    # half the lobbyists grew from salesperson by this rule alone (3x target)
    "lobbyist": dict(req="was('political adviser') | was('member of parliament') | was('party official') | "
                         "was('policy analyst') | ((has('journalist') | has('salesperson')) & has('friend in power'))",
                     after=["political adviser", "policy analyst", "party official", "journalist", "salesperson"],
                     rungs=["friend in power", "member of parliament", "mayor", "campaign organiser"], rate=0.008,
                     entry=True, weight="colors", grants=["registered lobbyist"]),
    # round 3: only politics and base names, so the pack loads on its own (batch.py refuses an after= it cannot find);
    # the research road (a research assistant or scientist of two years) belongs in the Science pack's EXTEND_SCIENCE
    # round 5 (P7): [drafting policy] and [reporting], named in req, are rungs (the research post at 'leaving politics for
    # another life' requires [drafting policy]); rate .02 to .01 with the colors weight
    "policy analyst": dict(req="has('graduate') & ((yrs_has('drafting policy') >= 2) | (yrs_has('reporting') >= 2) | "
                               "(yrs_has('political adviser') >= 2) | (yrs_has('journalist') >= 2) | "
                               "(yrs_has('data analyst') >= 2))",   # years in policy, data or reporting
                           after=["political adviser", "journalist", "data analyst"],
                           rungs=["graduate", "drafting policy", "reporting"], rate=0.01, entry=True,
                           weight="colors"),
    # round 4: an adviser of two years may move to the speeches (engine fit 14:44: never reached)
    "speechwriter": dict(req="has('writing speeches') | has('writing stories') | has('editing') | "
                             "(yrs_has('political adviser') >= 2)",
                         after=["political adviser", "journalist", "book editor", "novelist"],
                         rungs=["writing speeches", "writing stories", "editing"], rate=0.004,   # round 4 test: the
                         # adviser road at .1 made .009 of lives speechwriters against a .001 target; round 5 (P5): .015
                         # to .004 with the colors weight (tier fit 10-06 16:06: 3.0x)
                         weight="colors"),
    # a data analyst of two years qualifies on the years alone (engine fit, 14:00: [working with data] seldom comes to
    # data analysts, so nobody ever became a pollster); round 5: the colors weight (Blue's road), rate kept (under target)
    "pollster": dict(req="(yrs_has('data analyst') >= 2) | ((has('working with data') | has('reading the polls')) & "
                         "((yrs_has('reading the polls') >= 2) | was('campaign organiser') | "
                         "was('political adviser')))",   # survey or data work, or a campaign
                     after=["data analyst", "political adviser", "campaign organiser"],
                     rungs=["working with data", "reading the polls"], rate=0.008, entry=True, weight="colors"),
    # community
    "campaign volunteer": dict(req="(age >= 14) & (has('party member') | has('activist in a cause') | "
                                   "has('union rep'))", rate=0.005, starts=True, weight="colors",
                               lose="yrs_has('campaign volunteer') >= 1", lrate=0.5, lwhy="the election over"),
    "polling-station volunteer": dict(req="(age >= 18) & (has('party member') | was('campaign volunteer') | "
                                          "has('residents\\' committee member') | "
                                          "has('school-governance board member') | has('local party officer'))",
                                      rate=0.004, starts=True, weight="colors",
                                      lose="yrs_has('polling-station volunteer') >= 2", lrate=0.3,
                                      lwhy="no call for the next election"),
    # after: the background rule takes a councillor of three years to mayor (engine 22:12: after ends the old title);
    # a [mayoral candidate] wins the chain only by the act at 'polling day for mayor' (round 3)
    # Round 5, 2026-10-07 (P6): the rate was .0006, a population share, but the engine reads it as a yearly rate among
    # councillors of three years or more (the same mistake minister had), so almost no mayor came by it. Now .003 a year,
    # about 1 councillor in 13 over twenty-five years on the council; 'the town needs a mayor' is back at its times line
    # (2 to 4 in 100 a year, five ways in ten to stand at 30), about 1 in 7 to 1 in 5 over the same years, so together
    # about 1 councillor in 5 becomes mayor (catalogue times line; estimate)
    "mayor": dict(req="has('local councillor') & (yrs_has('local councillor') >= 3)",
                  after=["local councillor", "mayoral candidate"],
                  rate=0.003, weight="ties",
                  lose="yrs_has('mayor') >= 4", lrate=0.2, lwhy="the term over, or the vote lost"),
    # faith (cause); round 5: the colors weight (Green's road, the ward)
    "local party officer": dict(after=["party member"],
                                req="(yrs_faith >= 2) & (has('organising people') | mk('kept your word'))", rate=0.1,
                                weight="colors"),
    # statuses
    "council candidate": dict(req="(age >= 18) & (has('party member') | has('good name in town') | "
                                  "has('activist in a cause') | has('residents\\' committee member'))", rate=0.01,   # 2026-10-07: .025 to .01,
                              # standing comes mostly by choice at 'the ward needs a candidate', now open to every party member
                              weight="colors", lose="yrs_has('council candidate') >= 0.5", lrate=1.0,
                              lwhy="polling day came and went"),
    "parliamentary candidate": dict(req="has('parliamentary nomination') & ~has('member of parliament')", rate=0.008,
                                    lose="yrs_has('parliamentary candidate') >= 2.5", lrate=1.0,
                                    lwhy="the election came and went"),
    # round 3 (2026-10-06): the step of a direct election for mayor, from years of standing outside the council. No
    # background entry (rate 0): it comes only by the act at 'a run for mayor from outside the council', whose LIFE
    # gate holds the years; 'polling day for mayor' drops it, won or lost, and it lapses after two years in any case.
    # rungs: the standings that gate the run, kept on the step (engine rungs=, 11:30)
    "mayoral candidate": dict(req="~has('mayor') & ~has('local councillor')", rate=0.0,
                              rungs=["voice at the town hall", "good name in town", "local party officer",
                                     "residents' committee member", "school-governance board member", "union rep",
                                     "local hero", "founder of a firm", "family business",
                                     # round 5 (P4): the run's two new standings
                                     "party member", "activist in a cause"],
                              lose="yrs_has('mayoral candidate') >= 2", lrate=1.0,
                              lwhy="polling day came and went"),
    "former member of parliament": dict(req="was('member of parliament') & ~has('member of parliament')", rate=1.0),
    # skills: learned on the job (rates per year while the job is held)
    "canvassing": dict(req="has('campaign volunteer') | has('campaign organiser') | has('council candidate') | "
                           "has('parliamentary candidate')", rate=0.1, weight="practice"),
    "rousing a crowd": dict(req="(has('public speaking') | has('activist in a cause')) & (has('council candidate') | "
                                "has('parliamentary candidate') | has('member of parliament') | has('union rep'))",
                            rate=0.05, weight="colors"),
    "debating": dict(req="(has('public speaking') & (has('local councillor') | has('member of parliament') | "
                         "has('council candidate') | has('parliamentary candidate'))) | "
                         "had(['a debate or contest at school'], 3)", rate=0.004, weight="practice"),
    "fundraising": dict(req="has('campaign organiser') | has('party official') | has('parliamentary candidate') | "
                            "has('local party officer')", rate=0.25, weight="practice"),
    "coalition building": dict(req="has('local councillor') | has('mayor') | has('member of parliament') | "
                                   "has('party official')", rate=0.002, weight="practice"),
    "handling the press": dict(req="has('political adviser') | has('member of parliament') | has('mayor') | "
                                   "has('minister')", rate=0.04, weight="practice"),
    "constituency casework": dict(req="has('constituency caseworker') | has('local councillor') | "
                                      "has('member of parliament')", rate=0.0003, weight="practice"),
    "drafting policy": dict(req="has('policy analyst') | has('political adviser') | has('minister') | "
                                "(has('member of parliament') & (yrs_has('member of parliament') >= 3))", rate=0.06,
                            weight="practice"),
    "knowing the rules of the house": dict(req="(has('member of parliament') & (yrs_has('member of parliament') >= 1)) | "
                                               "(has('local councillor') & (yrs_has('local councillor') >= 2)) | "
                                               "(has('political adviser') & (yrs_career >= 2))", rate=0.0005,
                                           weight="practice"),
    "counting the votes": dict(req="(has('member of parliament') & has('allies in the party')) | has('party official') | "
                                   "has('local party officer')", rate=0.001, weight="colors"),
    "reading the polls": dict(req="has('pollster') | (has('campaign organiser') & has('working with data'))", rate=0.25,
                              weight="practice"),
    "writing speeches": dict(req="has('speechwriter') | (has('political adviser') & has('writing stories'))", rate=0.25,
                             weight="practice"),
    "knowing every street": dict(req="(was('campaign volunteer') | has('constituency caseworker') | "
                                     "has('local councillor')) & (ago_move > 5)", rate=0.005, weight="practice",
                                 lose="ago_move < 1", lrate=1.0, lwhy="moved away"),
    # access: [party nomination] is the council's, [parliamentary nomination] a winnable seat's in parliament
    "party nomination": dict(req="has('council candidate') & (has('party member') | has('local party officer'))",
                             rate=1.0, lose="~has('council candidate') & (yrs_has('party nomination') >= 1)", lrate=1.0,
                             lwhy="the election over"),
    "parliamentary nomination": dict(req="(has('party member') | has('local party officer')) & (has('local councillor') | "
                                         "has('political adviser') | has('party official') | has('mayor') | "
                                         "has('campaign organiser') | has('union rep') | has('known across the country'))",
                                     rate=0.0002, weight="ties",   # round 4: lapses at 2.5 years, as the candidacy
                                     lose="~has('parliamentary candidate') & ~has('member of parliament') & "
                                          "(yrs_has('parliamentary nomination') >= 2.5)", lrate=1.0,
                                     lwhy="the election over"),
    "the party whip": dict(req="has('member of parliament') & has('parliamentary nomination')",
                           rate=1.0, lose="~has('member of parliament')", lrate=1.0, lwhy="out of parliament"),
    "registered lobbyist": dict(req="has('lobbyist')", rate=1.0, lose="~has('lobbyist')", lrate=1.0,
                                lwhy="no longer lobbying"),
    "a movement behind you": dict(req="(has('council candidate') | has('parliamentary candidate')) & "
                                      "(has('activist in a cause') | has('union rep') | has('a following in the party'))",
                                  rate=0.4, lose="~has('council candidate') & ~has('parliamentary candidate') & "
                                                 "~has('member of parliament') & ~has('mayor')", lrate=1.0,
                                  lwhy="the campaign over"),
    "a parliamentary pass": dict(req="has('political adviser') | has('lobbyist') | has('member of parliament') | "
                                     "has('constituency caseworker')", rate=0.8,
                                 lose="~has('political adviser') & ~has('lobbyist') & ~has('member of parliament') & "
                                      "~has('constituency caseworker') & ~has('former member of parliament')",
                                 lrate=1.0, lwhy="the post ended"),
    # standing
    "a following in the party": dict(req="(has('local party officer') | has('member of parliament') | "
                                         "has('rousing a crowd')) & (yrs_faith >= 3)", rate=0.007, weight="colors"),
    "a safe seat": dict(req="has('member of parliament') & (yrs_has('member of parliament') >= 5)", rate=0.05,
                        lose="~has('member of parliament')", lrate=1.0, lwhy="out of parliament"),
    "a reform with your name on it": dict(req="has('minister') | (has('member of parliament') & "
                                              "(yrs_has('member of parliament') >= 5)) | (has('mayor') & "
                                              "(yrs_has('mayor') >= 2)) | (has('local councillor') & "
                                              "(yrs_has('local councillor') >= 6))", rate=0.002),
    "a name for straight talk": dict(req="(has('member of parliament') | has('local councillor') | has('mayor') | "
                                         "has('political adviser')) & (mkn('kept your word') >= 3) & "
                                         "~mk('hid a wrong', 5)", rate=0.005,
                                     lose="mk('broke your word', 1) | mk('hid a wrong', 1)", lrate=0.5,
                                     lwhy="a broken promise in public"),
    "a name as a fixer": dict(req="(has('party official') | has('lobbyist') | has('political adviser') | "
                                  "has('member of parliament')) & has('striking a deal')", rate=0.03),
    # bonds
    "allies in the party": dict(req="(has('party member') | has('local party officer')) & (has('local councillor') | "
                                    "has('member of parliament') | has('party official') | has('political adviser'))",
                                rate=0.02, weight="ties"),
    "donors": dict(req="has('fundraising') & (has('member of parliament') | has('mayor') | "
                       "has('parliamentary candidate') | has('party leader'))", rate=0.08, weight="money"),
    "a loyal campaign team": dict(req="(was('council candidate') | was('parliamentary candidate')) & "
                                      "(has('local councillor') | has('member of parliament') | has('mayor'))",
                                  rate=0.003, weight="ties"),
    "friends across the aisle": dict(req="(has('member of parliament') | has('local councillor') | has('mayor')) & "
                                         "mk('made a friend')", rate=0.002, weight="ties"),
    "officials who trust you": dict(req="(has('minister') | has('mayor') | (has('local councillor') & "
                                        "(yrs_has('local councillor') >= 4))) & mk('kept your word')", rate=0.01),
    # assets
    "a campaign war chest": dict(req="(has('council candidate') | has('parliamentary candidate') | "
                                     "has('member of parliament') | has('mayor')) & (has('fundraising') | "
                                     "has('donors') | has('savings'))", rate=0.1,
                                 lose="~has('council candidate') & ~has('parliamentary candidate') & "
                                      "~has('member of parliament') & ~has('mayor')", lrate=0.5,
                                 lwhy="spent on the campaign"),
    "a list of supporters": dict(req="has('canvassing') & (has('council candidate') | has('parliamentary candidate') | "
                                     "has('local councillor') | has('member of parliament') | "
                                     "has('campaign organiser') | has('local party officer'))", rate=0.03,
                                 lose="yrs_has('a list of supporters') >= 8", lrate=0.2, lwhy="the list went stale"),
}

# Additions to rules the pack does not own (the pack never rewrites a base or core rule; these widen who can gain
# them). A string is or-ed into the rule's req at that rule's own rate; a dict is a separate route with its own rate
# (engine, 22:12: rules are checked every four weeks, so odds belong in rate, never in chance() inside req):
#   - the base [local councillor] (earth_rules.ROLES: "has('good name in town') & (age >= 25)", rate .004) can also
#     come to a person standing for the council, the background twin of 'polling day in the ward': rate .03 a year
#     (calibrated 2026-10-06), so that with the moment about 35 in 100 candidates win, the real share (estimate);
#   - the core [known across the country] (science/roles.py, ROLES_REACH) can also come with high office, the
#     background twin of 'a speech that goes everywhere' and of a cabinet post.
EXTEND_POLITICS = {
    "local councillor": dict(req="has('council candidate')", rate=0.03),
    "known across the country": "has('minister') | has('party leader') | "
                                "(has('member of parliament') & (yrs_has('member of parliament') >= 10)) | "
                                "(has('mayor') & has('a following in the party'))",
}

# Fit targets (round 2, 2026-10-06). Emren's budget (pack ideas thread, 08:11): across all packs together about 1 life
# in 3 holds a pack career at some point and about 1 in 20 reaches a summit. A tier word puts a title in that budget
# (the engine, batch._targets and earth_rules.BUDGET, 08:21): "career" titles share one multiplier, "summit" titles
# split the summit budget by the square root of their real share, "community" titles (with the candidacies and the
# party's local posts) go to 10x their real share, at most .25 of lives. One fitted lift per tier
# (earth_rules.TIER_LIFT) moves a whole tier: under budget it raises the background rules of its careers and summits
# (their norm is exp(lift), not ROLE_NORM) and leaves the written chance as written; over budget it also lowers the odds
# of every act that gives one. The rates here keep the titles of a tier at a similar multiple of their real share, so
# one lift moves them together. Community titles and perks keep ROLE_NORM. The catalogue keeps the real shares. A number
# is a perk's own multiplier: [parliamentary nomination] is what makes a seat winnable at 'election night', so it
# follows the members of parliament it feeds rather than its real share. Every career here grows from the rung below it
# (after=, the holds: of its moments), as Emren asked at 09:18: big titles take consecutive steps.
TARGET_POLITICS = {
    "campaign organiser": "career", "constituency caseworker": "career", "political adviser": "career",
    "party official": "career", "lobbyist": "career", "policy analyst": "career", "speechwriter": "career",
    "pollster": "career",
    # round 4 (engine fit 14:44): the seat and office are summits; [party leader] and [head of government] ride on them
    # at their written step rates (not fitted), since four nested titles cannot each sit at the .001 summit floor while
    # parliament's own target is .0018 (Emren 14:41: "Keep odds higher than real, but not super unrealistically")
    "member of parliament": "summit", "minister": "summit",
    "mayor": "summit",
    "campaign volunteer": "community", "polling-station volunteer": "community",
    # Round 5, 2026-10-07: [local party officer] at 5x its real share (.05), not the community 10x (.1). Only party
    # members can take the post (after= party member), and members are about .057 of lives in play, so .1 cannot be
    # reached at any lift; .05 is about 9 members in 10 holding a branch post at some point, still high. Flagged for
    # the engine's fit.
    "local party officer": 5,
    # the council candidacy at 3x its real share, not the community 10x: at .25 of lives it made local councillors .077
    # (catalogue .010) and overfed mayor (engine fit, 14:00); 3x keeps the road to mayor near the mayor's own multiple.
    # Round 5, 2026-10-07: 3 to 1.5 (about .045 candidacies), since at 3x the councillors still ran 3.4 to 4.8x their
    # .010 (fits 11b, 12b); with about 35 in 100 candidates winning that is near .016 councillors
    "council candidate": 1.5, "parliamentary candidate": "community", "mayoral candidate": "community",
    "former member of parliament": "community",
    "parliamentary nomination": 20,   # round 4: 15 to 20, so members reach parliament's .0018
}
