# rules_titles.py: part 3 of 11 of earth_rules.py, the engine's reading of the Library's words.
# ROLES and ROLES_V2: titles and perks, how they come and go.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# ---------------------------------------------------------------- titles and perks (chroma-engine/perks-titles-format.md)
# The engine's reading of the Library's plain words (gained, lost, needs) in chroma-library/<world>_perks_titles.py.
# Each entry: req (who can gain it, in the condition vocabulary plus has('name'), was('name'), yrs_has('name')), rate
# (a yearly chance while req holds; left out: the share spread over the age window), after (titles of the same kind it
# grows out of, and replaces), entry (a commitment's first title when the commitment starts; default: no after),
# starts (a background gain also starts its commitment), lose / lrate (a yearly chance of losing it while lose holds),
# weight (practice | colors | money | ties: who is likelier among those who qualify), grants (perks that come with it),
# lwhy (the words for a loss through lose), refines (held on top of another title, as the catalogue's refines: the
# rules set it where the nesting is the engine's reading). A perk with a lose rule is lost only that way (and through
# acts), never slipping away at random. Money gates follow the engine's money among adults 25 to 65 (calib_v7/
# churn_check.py, 2026-10-05): .003 is the poorest tenth, .02 the 15th percentile, .08 the 30th, .2 the median, .25
# the 58th, .45 the 90th.
# Engine-granted, outside these rules: widowed, divorced, retiree, out of work, newcomer, veteran, left the faith.
# Every act field (title:, grants:, takes:, suspends:, requires:) works on top of these, and replaces a background rule
# once the Library has put it on the acts.
SKILLED = "mkn('learned a skill') >= 2"
ROLES = {
    # careers: the first title when a career starts, chosen by fit with the act that started it; a few grow from others
    "shop assistant": dict(), "waiter or bartender": dict(), "care worker": dict(), "factory worker": dict(),
    "office clerk": dict(req="has('school-leaving certificate')"),
    "nurse": dict(req="has('professional registration')"),
    "teacher": dict(req="has('graduate') & has('professional registration')"),
    "electrician": dict(req="has('trade ticket')", after=["apprentice"], rate=0.25, grants=["building trade"]),
    "builder": dict(after=["apprentice"], rate=0.15, entry=True),
    "shop owner": dict(req="has('savings') | has('family business')"),
    "soldier": dict(req="(age <= 30) & ~has('someone with a record')"),
    "farmer": dict(req="has('plot of land') | has('family business')"),
    "software developer": dict(req="has('writing code')"),
    "shift manager": dict(after=["shop assistant", "waiter or bartender", "care worker", "factory worker", "office clerk",
                                 "cook", "delivery driver", "salesperson"], req="(yrs_career >= 1) & has('reliable record')", rate=0.08),
    "police officer": dict(req="(age <= 40) & ~has('someone with a record')"),
    "cook": dict(), "salesperson": dict(), "builder ": None,
    "delivery driver": dict(req="has('driving licence')"),
    "accountant": dict(req="has('bookkeeping')"),
    "estate agent": dict(req="has('driving licence')"),
    "founder of a firm": dict(req="(has('savings') | (money > .6)) & mk('took a wild risk')"),
    "head chef": dict(after=["cook"], req="yrs_career >= 4", rate=0.08),
    "apprentice": dict(req="age <= 30"),
    # partners: a first love, then moving in, engagement, marriage, many years
    "girlfriend or boyfriend": dict(),
    "living together": dict(after=["girlfriend or boyfriend"], req="(yrs_partner >= 1) & (age >= 18)", rate=0.35),
    "engaged": dict(after=["girlfriend or boyfriend", "living together"], req="(yrs_partner >= 1.5) & (age >= 19)", rate=0.12,
                    # game play-test 16:19 (engaged for 17 years): most engaged couples marry within two years (LIFE: getting
                    # married is much likelier while engaged); one still engaged after three years mostly breaks it off
                    lose=[("yrs_has('engaged') >= 3", "the engagement broken off")], lrate=0.35, lend="broke up"),
    "married again": dict(after=["girlfriend or boyfriend", "living together", "engaged"], req="married & (was('divorced') | was('widowed'))", rate=1.0),
    "wife or husband": dict(after=["girlfriend or boyfriend", "living together", "engaged"], req="married & ~was('divorced') & ~was('widowed')", rate=1.0),
    "partner of many years": dict(after=["wife or husband", "living together", "married again"], req="yrs_partner >= 20", rate=0.5),
    # children
    # a parent stays one: three or more, single parent and grandparent are held on top of mother or father (2026-10-05:
    # as successions they took it away and gave it back, and its facets with it)
    "mother or father": dict(entry=True),
    "parent of three or more": dict(refines="mother or father", req="has('mother or father') & (yrs_children >= 3) & (yrs_children <= 15) & held_partner", rate=0.03),
    "single parent": dict(refines="mother or father", req="has('mother or father') & kids_home & ~held_partner & (ago_end_partner >= 1)", rate=0.5,
                          lose="(held_partner & (yrs_partner >= 1)) | ~kids_home", lrate=1.0, lwhy="a partner at home, or the children grown"),
    "stepparent": dict(req="held_partner & (yrs_partner < 3) & ~held_children & (age >= 22)", rate=0.04, starts=True, entry=False),
    "foster parent": dict(req="(age >= 25) & (money > .4) & mk('helped someone in need')", rate=0.0015, starts=True),
    "adoptive parent": dict(req="(age >= 25) & held_partner & ~held_children & (yrs_partner >= 3)", rate=0.003, starts=True),
    "grandparent": dict(refines="mother or father", req="has('mother or father') & (yrs_children >= 22)", rate=0.12),
    # community: up to three at once; children's teams and troops start the commitment on their own
    "on the team": dict(req="(age <= 40) & ((hR + hG + hB) > .55)", rate=0.06, starts=True, weight="colors"),
    "scout or guide": dict(req="age <= 14", rate=0.03, starts=True),
    "prefect": dict(req="has('teachers\\' favourite') & (age >= 13)", rate=0.1, starts=True),
    "team captain": dict(after=["on the team"], req="yrs_has('on the team') >= 2", rate=0.08),
    "neighbourhood volunteer": dict(req="mk('helped someone in need')", rate=0.02, starts=True, weight="colors"),
    "union rep": dict(req="held_career & (yrs_career >= 3) & mk('defied an authority')", rate=0.02),
    "local councillor": dict(req="has('good name in town') & (age >= 25)", rate=0.004),
    "youth coach": dict(req="was('on the team') & (age >= 25) & held_children", rate=0.02),
    "residents' committee member": dict(req="has('homeowner')", rate=0.004),
    "club treasurer": dict(req="has('bookkeeping') & has('reliable record')", rate=0.01),
    "in a street gang": dict(req="(age <= 25) & ((money < .3) | mk('made an enemy'))", rate=0.004, starts=True, lose="age > 25", lrate=0.3),
    # faith, ideology or cause
    "regular worshipper": dict(),
    "deacon or elder": dict(after=["regular worshipper"], req="(yrs_faith >= 10) & has('known face at worship')", rate=0.01),
    "activist in a cause": dict(req="had(['a sense of injustice', 'a protest in your city'], 2)", rate=0.04, weight="colors", starts=True),
    "party member": dict(req="age >= 18", rate=0.004, weight="colors", starts=True, entry=True), "convert": dict(req="~was('regular worshipper') | was('left the faith')"),
    "seeker": dict(),
    # statuses
    "graduate": dict(req="has('school-leaving certificate') & (age >= 20) & (age <= 30)", rate=0.08, weight="colors"),
    "veteran": None, "widowed": None, "retiree": None, "newcomer": None, "divorced": None, "out of work": None,
    "has killed in war": dict(req="has('soldier') & (yrs_career >= 1)", rate=0.05),   # most who serve never do
    "homeowner": dict(req="(age >= 22) & ((money > .5) | has('savings') | has('inheritance'))", rate=0.12),
    "immigrant": dict(req="ago_move < 1", rate=0.2),
    "someone with a record": dict(req="mk('defied an authority', 1) | mk('hid a wrong', 1) | mk('took a wild risk', 1)", rate=0.03),
    "ex-prisoner": dict(req="has('someone with a record') & mk('defied an authority', 2)", rate=0.02),
    "in recovery": dict(req="had(['an addiction takes hold'], 5)", rate=0.25),
    "eldest child": dict(req="(age <= 6) & (older_siblings == 0) & (younger_siblings > 0)", rate=0.6),   # N4: first-born with a younger one
    # (rate .6 a year: most first-borns take it within a year or two of the first younger one; .12 reached .13 of lives
    # against a share of .35, Library next3 §1)
    "carer for a parent": dict(req="(alive_parent > 0) & (age >= 30)", rate=0.012),
    "homeless": dict(req="(money < .08) & (ties < .3)", rate=0.1),
    "cancer survivor": dict(req="had(['a frightening diagnosis'], 1) & (health > .4)", rate=0.4),
    "left the faith": None,
    # perks: skills come with practice in their ways (weight practice); credentials and assets with their prerequisites
    "swimming": dict(req="age <= 14", rate=0.12),
    "cooking for a crowd": dict(req="had(['learning to cook for yourself', 'a holiday meal with the whole family'], 3)", rate=0.05),
    "second language": dict(rate=0.02), "musical instrument": dict(req="has('instrument of one\\'s own')", rate=0.08),
    "building trade": dict(req="has('apprentice') | has('builder')", rate=0.3),
    "fixing things": dict(req="mk('learned a skill')", rate=0.025), "car mechanics": dict(req=SKILLED, rate=0.006),
    "growing food": dict(req="had(['tending an allotment'], 3) | (age <= 14)", rate=0.025),
    "sewing and mending": dict(req="mk('learned a skill')", rate=0.012),
    "public speaking": dict(req="mk('learned a skill') & mk('took a wild risk')", rate=0.012),
    "bookkeeping": dict(req="mk('learned a skill') & (age >= 16)", rate=0.015),
    "boxing or martial arts": dict(req=SKILLED + " & (age <= 40)", rate=0.005),
    "dancing": dict(rate=0.008), "writing code": dict(req=SKILLED, rate=0.005),
    "drawing and painting": dict(req="mk('learned a skill')", rate=0.006),
    "home nursing": dict(req="mkn('helped someone in need') >= 2 | has('carer for a parent')", rate=0.012),
    "hunting and fishing": dict(rate=0.004), "selling": dict(req="mk('made a friend') | mk('took a wild risk')", rate=0.008),
    "finding things out": dict(req="mk('learned a skill')", rate=0.012),
    "minding small children": dict(req="mk('helped someone in need') | held_children", rate=0.03),
    "calming people down": dict(req="mkn('helped someone in need') >= 2", rate=0.008),
    "striking a deal": dict(req="mk('took a wild risk') & (age >= 16)", rate=0.008), "scripture": dict(req="was('regular worshipper')", rate=0.05),
    "cards for money": dict(req="mk('took a wild risk')", rate=0.004), "teaching": dict(req="mk('learned a skill') & mk('helped someone in need')", rate=0.008),
    "driving licence": dict(req="(age >= 17) & ((age < 30) | chance(.15))", rate=0.1),   # most learn young (2026-10-05)
    "first-aid certificate": dict(rate=0.01), "passport": dict(rate=0.06),
    "school-leaving certificate": dict(req="(age >= 16) & (age <= 20)", rate=0.6, weight="practice"),
    "professional registration": dict(req="has('graduate') & (age <= 40)", rate=0.05),
    "lorry or bus licence": dict(req="has('driving licence') & held_career", rate=0.002),
    "trade ticket": dict(req="(has('apprentice') & (yrs_career >= 2)) | (has('building trade') & (age >= 20))", rate=0.15),
    "hunting licence": dict(req="has('hunting and fishing') & ~has('someone with a record')", rate=0.15),
    "motorbike licence": dict(rate=0.004), "citizenship": dict(req="has('immigrant')", rate=0.04),
    "drinks licence": dict(req="~has('someone with a record') & held_career", rate=0.001),
    "coaching badge": dict(req="was('on the team') & (age >= 18)", rate=0.004),
    "referee's badge": dict(req="was('on the team')", rate=0.002),
    "good name in town": dict(req="(mkn('kept your word') >= 3) & (mkn('helped someone in need') >= 3) & (ago_move > 3)", rate=0.04,
                              lose="mk('hid a wrong', 1) | (ago_move < 1)", lrate=0.5),
    "rank": dict(req="(yrs_career >= 5) & has('reliable record')", rate=0.025, lose="~held_career", lrate=1.0),
    "known face at worship": dict(req="has('regular worshipper') & (yrs_faith >= 3)", rate=0.1, lose="~held_faith | (ago_move < 1)", lrate=1.0),
    "reliable record": dict(req="mkn('kept your word') >= 3", rate=0.08, lose="mk('broke your word', 1)", lrate=0.4),
    "good credit": dict(req="(age >= 18) & (money >= .08)", rate=0.15, lrate=0.5,
                        lose=[("had(['financial ruin'], 1)", "financial ruin"), ("(money < .01) & (yrs_adj('poor') >= 1)", "missed payments")]),
    "the one everyone asks": dict(req="(age >= 25) & (mkn('learned a skill') >= 5)", rate=0.01),
    "following online": dict(req="had(['wanting to be noticed'], 2)", rate=0.04),
    "name in the field": dict(req="(yrs_career >= 10) & (mkn('learned a skill') >= 8)", rate=0.006),
    "not to be crossed": dict(req="mkn('made an enemy') >= 3", rate=0.01),
    "regular at the local": dict(req="(age >= 18) & mk('made a friend')", rate=0.015, lose="ago_move < 1", lrate=1.0),
    "local hero": dict(req="mk('helped someone in need', 1) & mk('took a wild risk', 1)", rate=0.01),
    "old family name": dict(req="age <= 4", rate=0.02, lose="ago_move < 1", lrate=0.5),
    "inner circle at work": dict(req="held_career & (yrs_career >= 5)", rate=0.008, lose="~held_career", lrate=1.0),
    "teachers' favourite": dict(req="age <= 16", rate=0.04, weight="practice"),
    "mentor": dict(req="mk('learned a skill') | mk('helped someone in need')", rate=0.03),
    "friend in power": dict(req="mkn('made a friend') >= 3", rate=0.003),
    "patron": dict(req="mk('took a wild risk') & (mkn('learned a skill') >= 4)", rate=0.002),
    "family who will always take you in": dict(req="age <= 4", rate=0.5),
    "friend for life": dict(req="mk('made a friend')", rate=0.03, lose="alive_friend < 1", lrate=1.0),
    "old school network": dict(req="has('graduate')", rate=0.08),
    "sponsor in recovery": dict(req="has('in recovery')", rate=0.5),
    "neighbour who has your back": dict(req="(age >= 18) & (mk('made a friend') | mk('helped someone in need'))", rate=0.03, lose="ago_move < 1", lrate=1.0),
    "contact in the trade": dict(req="held_career & (yrs_career >= 3)", rate=0.015),
    "family abroad": dict(req="(age <= 4) | has('immigrant')", rate=0.06),
    "old comrades": dict(req="(was('soldier') & (yrs_career >= 3)) | (yrs_has('on the team') >= 5)", rate=0.05),
    "godparent who looks out": dict(req="age <= 4", rate=0.15, lose="age >= 60", lrate=1.0),
    "dog of one's own": dict(req="had(['a pet of your own', 'a stray dog follows you home'], 1)", rate=0.5, lose="had(['your pet dies'], 1)", lrate=1.0),
    "in-laws who took you in": dict(req="has('wife or husband') | has('living together') | has('married again')", rate=0.15,
                                    lose="~held_partner", lrate=0.7),
    "savings": dict(req="(age >= 14) & (money >= .25)", rate=0.2, lrate=0.5,
                    lose=[("had(['financial ruin'], 1)", "financial ruin"), ("had(['losing your job'], 1) & (money < .1)", "spent while out of work"),
                          ("(money < .03) & (yrs_adj('poor') >= 1)", "spent in hard times")]),
    "paid-off home": dict(req="has('homeowner') & (yrs_has('homeowner') >= 20)", rate=0.1),
    "car": dict(req="has('driving licence') & (money > .02)", rate=0.3, lrate=0.5,
                lose=[("had(['financial ruin'], 1)", "financial ruin"), ("(money < .003) & (yrs_adj('poor') >= 2) & chance(.3)", "no money to keep it"),
                      ("(age >= 75) & (health < .35)", "the doctor says to stop driving")]),
    "family business": dict(req="age < 15", rate=0.07),          # a family business one can join at fourteen
    "inheritance": dict(req="ago_death < 1", rate=0.3),
    "workplace pension": dict(req="held_career & (yrs_career >= 2) & (age >= 22)", rate=0.12),
    "plot of land": dict(req="had(['tending an allotment'], 3) | has('farmer')", rate=0.05),
    "shares": dict(req="(has('savings') | has('workplace pension')) & (money > .45)", rate=0.04),
    "van and tools": dict(req="(has('trade ticket') | has('building trade')) & has('driving licence')", rate=0.1),
    "flat to rent out": dict(req="(has('savings') | has('inheritance')) & has('good credit') & (money > .55)", rate=0.01),
    "place by the sea": dict(req="(has('savings') | has('inheritance')) & (money > .55) & (age >= 40)", rate=0.006),
    "scholarship": dict(req="(age >= 11) & (age <= 20) & (mkn('learned a skill') >= 3)", rate=0.02),
    "workshop": dict(req="has('fixing things')", rate=0.02),
    "instrument of one's own": dict(req="age <= 30", rate=0.012),
}
# ---- volume 2: Emren's 100 more titles (12:05), the Library's rules proposal (chroma-library/drafts/titles2/roles-v2.py,
# taken in 2026-10-05 ~14:30; engine changes marked "engine"). A catalogue without these titles (the first draft)
# runs as before: their names are in ROLES_OPTIONAL.
ROLES_V2 = {
    # ---------------- careers (T2-001 to T2-045)
    # health and emergency services
    "laboratory technician": dict(req="has('school-leaving certificate')"),
    "paramedic": dict(req="has('professional registration') & has('driving licence') & (health > .5)",
                      lose="health < .4", lrate=0.3),
    "physician": dict(req="has('graduate') & has('professional registration') & (age >= 24)",
                      lose="~has('professional registration') & (age < 70)", lrate=1.0),
    "psychotherapist": dict(req="has('graduate') & (age >= 25)", after=["nurse", "teacher"], rate=0.003, entry=True),
    "pharmacist": dict(req="has('graduate') & has('professional registration')"),
    "veterinarian": dict(req="has('graduate') & has('professional registration')"),
    "midwife": dict(req="has('professional registration')", after=["nurse"], rate=0.01, entry=True,
                    lose="~has('professional registration') & (age < 70)", lrate=1.0),
    "firefighter": dict(req="(age >= 18) & (age <= 40) & ~has('someone with a record') & (health > .6)",
                        lose="health < .45", lrate=0.3),
    "emergency dispatcher": dict(req="(age >= 18) & ~has('someone with a record')",
                                 after=["paramedic", "firefighter", "police officer"], rate=0.01, entry=True),
    # words, records and heritage
    "translator": dict(req="has('second language') & (age >= 20)"),
    "journalist": dict(req="has('graduate') | has('finding things out')"),
    "book editor": dict(req="has('graduate')", after=["journalist"], rate=0.005, entry=True),
    "archivist": dict(req="has('graduate')"),
    "museum curator": dict(req="has('graduate')", after=["archivist", "archaeologist"], rate=0.02, entry=True),
    "archaeologist": dict(req="has('graduate')"),
    # land, buildings and systems
    "land surveyor": dict(req="(has('graduate') | was('apprentice')) & (age >= 18)"),
    "urban planner": dict(req="has('graduate')"),
    "architect": dict(req="has('graduate') & has('professional registration')"),
    "civil engineer": dict(req="has('graduate')"),
    "data analyst": dict(req="has('graduate') | has('writing code') | has('finding things out')",
                         after=["office clerk", "accountant"], rate=0.01, entry=True),
    "cybersecurity analyst": dict(req="has('writing code')", after=["software developer", "data analyst"], rate=0.02,
                                  entry=True),
    # trades and making
    "machinist": dict(req="was('apprentice') | (mkn('learned a skill') >= 2)", after=["apprentice", "factory worker"],
                      rate=0.05, entry=True),
    "welder": dict(req="was('apprentice') | has('building trade') | (mkn('learned a skill') >= 2)",
                   after=["apprentice", "factory worker", "builder"], rate=0.04, entry=True),
    "plumber": dict(req="has('trade ticket') | has('building trade')", after=["apprentice", "builder"], rate=0.1,
                    entry=True),
    "carpenter": dict(req="has('building trade') | has('trade ticket')", after=["apprentice", "builder"], rate=0.1,
                      entry=True),
    "baker": dict(req="age >= 16", after=["cook", "shop assistant"], rate=0.01, entry=True),
    # services that keep a place running
    "cleaner": dict(),
    "sanitation worker": dict(req="age >= 18"),
    "postal worker": dict(req="age >= 17"),
    "train driver": dict(req="(age >= 20) & (age <= 50) & ~has('someone with a record') & (health > .6)",
                         lose="(health < .45) | has('someone with a record')", lrate=0.5),
    "commercial pilot": dict(req="(age >= 19) & (age <= 40) & ~has('someone with a record') & (health > .6) & "
                                 "(has('savings') | has('graduate') | was('soldier'))",
                             after=["soldier"], rate=0.003, entry=True, lose="health < .5", lrate=0.5),
    # sea, land and living things
    "merchant seafarer": dict(req="(age >= 16) & (age <= 45) & (health > .6)"),
    "commercial fisher": dict(req="(age >= 16) & (health > .5) & (has('family business') | (age <= 35))"),
    "forester": dict(req="has('graduate') | was('apprentice')"),
    "professional beekeeper": dict(req="(age >= 20) & (mkn('learned a skill') >= 3)", after=["farmer"], rate=0.003,
                                   entry=True),
    # ceremonies, craft and performance
    "funeral director": dict(req="(age >= 20) & (has('family business') | (mkn('helped someone in need') >= 2))"),
    "civil celebrant": dict(req="(age >= 25) & has('public speaking')"),
    "tattoo artist": dict(req="(age >= 18) & has('drawing and painting')"),
    "sound engineer": dict(req="has('musical instrument') | (mkn('learned a skill') >= 2)"),
    "stage technician": dict(req="(age >= 17) & (has('fixing things') | (mkn('learned a skill') >= 2))"),
    "video-game developer": dict(req="has('writing code') | has('drawing and painting')", after=["software developer"],
                                 rate=0.01, entry=True),
    "professional athlete": dict(req="(age >= 16) & (age <= 30) & was('on the team') & (health > .7)",
                                 lose="health < .55", lrate=0.3),
    "novelist": dict(req="(age >= 20) & (mkn('learned a skill') >= 3)", after=["journalist", "book editor", "teacher"],
                     rate=0.002, entry=True),
    "court interpreter": dict(req="has('second language') & ~has('someone with a record') & (age >= 23)",
                              after=["translator"], rate=0.03, entry=True, lose="has('someone with a record')",
                              lrate=1.0),
    "professional conservator": dict(req="has('graduate')"),

    # ---------------- partner, children, community, faith and status (T2-046 to T2-100)
    # partners: four facets on wife or husband, one partnership of its own that starts the commitment
    "newlywed": dict(req="(has('wife or husband') & (yrs_has('wife or husband') < 1)) | (has('married again') & (yrs_has('married again') < 1))", rate=1.0, entry=False),   # Library 15:50
    # granted by an act (title: on a moment about a partner falling ill); the engine does not model a partner's health.
    # No rate, so it is no background rule: the lasts cap (10) and the refined title's end close it
    "caregiving partner": dict(req="held_partner", entry=False, lose="~held_partner", lrate=1.0),   # Library 15:50: any partner
    "nonromantic life partner": dict(req="(age >= 20) & ~held_partner & (mkn('made a friend') >= 2)", rate=0.0005,
                                     starts=True, entry=False, weight="ties"),
    "spouse in a family-arranged marriage": dict(req="has('wife or husband') & (yrs_has('wife or husband') < 1)",
                                                 rate=0.03, entry=False, weight="ties"),
    "partner in a multigenerational household": dict(req="has('wife or husband') & (alive_parent > 0) & (ago_move >= 1)",
                                                     rate=0.004, entry=False, weight="ties",
                                                     lose="(alive_parent < 1) | (ago_move < 1)", lrate=0.5),
    # children: six facets on mother or father, one on grandparent, and a guardianship that starts the commitment
    "parent of an only child": dict(req="has('mother or father') & (yrs_children >= 4) & ~was('parent of an only child') & "
                                        "~had(['a child is born', 'a baby on the way, planned or not'], 4)",   # engine: once
                                    rate=0.1, entry=False, lose="had(['a child is born'], 1)", lrate=1.0),
    "parent of independent adult children": dict(req="has('mother or father') & held_children & ~kids_home", rate=0.5,
                                                 entry=False),
    "parent with a child living abroad": dict(req="has('mother or father') & (yrs_children >= 18)", rate=0.004,
                                              entry=False, lose="yrs_has('parent with a child living abroad') >= 2",
                                              lrate=0.1),
    "home-educating parent": dict(req="has('mother or father') & kids_home & (yrs_children >= 4) & (yrs_children <= 16)",
                                  rate=0.003, entry=False, lose="yrs_has('home-educating parent') >= 1", lrate=0.2),
    "guardian of an unrelated child": dict(req="(age >= 21) & mk('helped someone in need')", rate=0.0003, starts=True,
                                           lose="yrs_has('guardian of an unrelated child') >= 5", lrate=0.2),
    "grandparent raising a grandchild": dict(req="has('grandparent') & (age <= 75)", rate=0.001, entry=False,
                                             lose="yrs_has('grandparent raising a grandchild') >= 3", lrate=0.1),
    "parent coordinating complex support needs": dict(req="has('mother or father') & kids_home & (yrs_children >= 1)",
                                                      rate=0.003, entry=False, lose="~kids_home", lrate=0.3),
    "parent raising a child across languages": dict(req="has('mother or father') & kids_home & "
                                                        "(has('second language') | has('immigrant') | has('family abroad'))",
                                                    rate=0.05, entry=False, lose="~kids_home", lrate=0.5),
    # community: each can start the community commitment (up to three titles at once) and is a possible first title
    "choir member": dict(req="age >= 8", rate=0.004, starts=True, weight="colors"),
    "community-garden coordinator": dict(req="(age >= 18) & (had(['tending an allotment'], 3) | has('growing food'))",
                                         rate=0.004, starts=True, weight="colors"),
    "repair-cafe volunteer": dict(req="(age >= 16) & (has('fixing things') | has('sewing and mending') | has('car mechanics'))",
                                  rate=0.003, starts=True, weight="colors"),
    "amateur astronomer in a club": dict(req="(age >= 10) & (had(['more stars than anyone could count', "
                                             "'the sun goes dark at noon', 'awe'], 10) | has('finding things out'))",
                                         rate=0.002, starts=True, weight="colors"),
    "historical reenactment member": dict(req="age >= 14", rate=0.0003, starts=True, weight="colors"),
    "community-radio presenter": dict(req="(age >= 16) & (has('public speaking') | mk('learned a skill'))", rate=0.0003,
                                      starts=True, weight="colors"),
    "community-mediation volunteer": dict(req="(age >= 21) & has('calming people down')", rate=0.002, starts=True,
                                          weight="colors"),
    "search-and-rescue volunteer": dict(req="(age >= 18) & (age <= 60) & has('first-aid certificate') & (health > .6)",
                                        rate=0.002, starts=True, lose="health < .4", lrate=0.5),
    "lifeboat volunteer": dict(req="(age >= 17) & (age <= 55) & has('swimming') & (health > .6)", rate=0.0002,
                               starts=True, lose="health < .4", lrate=0.5),
    "school-governance board member": dict(req="(age >= 21) & (kids_home | has('good name in town'))", rate=0.002,
                                           starts=True, lose="yrs_has('school-governance board member') >= 4", lrate=0.4),
    "parent-association organiser": dict(req="kids_home & (yrs_children >= 4) & (yrs_children <= 16)", rate=0.005,
                                         starts=True, lose="~kids_home | (yrs_has('parent-association organiser') >= 3)",
                                         lrate=0.4),
    "housing-cooperative member": dict(req="(age >= 18) & (ago_move >= 1)", rate=0.002, starts=True,
                                       lose="ago_move < 1", lrate=1.0),
    "sports referee": dict(req="has('referee\\'s badge')", rate=0.3, starts=True, lose="~has('referee\\'s badge')",
                           lrate=0.5),
    "festival organiser": dict(req="(age >= 16) & (mkn('made a friend') >= 2)", rate=0.0005, starts=True,
                               weight="colors", lose="had(['burnout'], 1)", lrate=0.5),
    "amateur band member": dict(req="(age >= 12) & has('musical instrument')", rate=0.05, starts=True, weight="colors"),
    "book-club organiser": dict(req="(age >= 16) & mk('made a friend')", rate=0.001, starts=True, weight="colors"),
    "community-kitchen volunteer": dict(req="(age >= 16) & mk('helped someone in need')", rate=0.002, starts=True,
                                        weight="colors"),
    "neighbourhood-watch coordinator": dict(req="(age >= 21) & (ago_move >= 1) & "
                                                "had(['break-ins on the street', 'robbed or attacked in the street'], 2)",
                                            rate=0.05, starts=True, lose="ago_move < 1", lrate=1.0),
    "prison visitor": dict(req="(age >= 21) & (mkn('helped someone in need') >= 2)", rate=0.0002, starts=True,
                           weight="colors"),
    "board-game club organiser": dict(req="(age >= 14) & mk('made a friend')", rate=0.0007, starts=True, weight="colors"),
    # faith and causes: religious roles grow from a faith already held (and replace its title); causes start the faith
    # commitment like [activist in a cause]
    "ordained religious minister": dict(after=["regular worshipper", "deacon or elder", "convert"],
                                        req="(yrs_faith >= 3) & (age >= 23) & has('scripture')", rate=0.002),
    "member of a monastic community": dict(after=["regular worshipper", "convert", "seeker"],
                                           req="(age >= 18) & ~held_partner & ~kids_home", rate=0.0005),
    "lay religious teacher": dict(after=["regular worshipper", "convert"],
                                  req="(yrs_faith >= 3) & (age >= 16) & (has('scripture') | has('teaching') | (yrs_faith >= 8))",
                                  rate=0.01),   # Library 13:55: no test life met scripture or teaching, so long practice counts too
    "congregation musician": dict(after=["regular worshipper", "believer on the big days", "convert"],
                                  req="(age >= 12) & has('musical instrument')", rate=0.02),
    "interfaith-dialogue participant": dict(after=["regular worshipper", "deacon or elder", "convert", "seeker"],
                                            req="(age >= 16) & (yrs_faith >= 2) & mk('made a friend')", rate=0.003),
    "animal-shelter campaigner": dict(req="(age >= 14) & (had(['a pet of your own', 'a stray dog follows you home', "
                                          "'your pet dies'], 10) | has('dog of one\\'s own'))",
                                      rate=0.003, starts=True, weight="colors"),
    "disability-rights organiser": dict(req="(age >= 16) & (had(['living with a chronic illness', "
                                            "'a serious accident or illness', 'a sense of injustice'], 3) | "
                                            "has('parent coordinating complex support needs') | has('carer for a parent'))",
                                        rate=0.002, starts=True, weight="colors"),
    "civil-liberties campaigner": dict(req="(age >= 16) & had(['a sense of injustice', 'a protest in your city', "
                                           "'a bitter election'], 2)", rate=0.003, starts=True, weight="colors"),
    "restorative-justice advocate": dict(req="(age >= 18) & (had(['a sense of injustice', "
                                             "'robbed or attacked in the street'], 3) | was('someone with a record'))",
                                         rate=0.002, starts=True, weight="colors"),
    "digital-rights advocate": dict(req="(age >= 16) & (has('writing code') | has('finding things out') | "
                                        "had(['someone starts mocking you online'], 3))",
                                    rate=0.002, starts=True, weight="colors"),
    # statuses: no colors; facts of a history (lasts life) or spells that end when what they need stops holding
    "doctoral graduate": dict(req="has('graduate') & (age >= 25) & (age <= 45) & (mkn('learned a skill') >= 3)",
                              rate=0.002),
    "first-generation university student": dict(req="has('school-leaving certificate') & (age >= 17) & (age <= 25) & "
                                                    "~has('graduate') & ~was('first-generation university student')",
                                                rate=0.05, lose="has('graduate')", lrate=1.0),
    "former foster child": dict(req="False"),   # Library 16:55: only through the child event 'going into foster care'
    "adopted person": dict(req="age < 3.05", rate=0.02),   # Library 16:55: a fact of the family story from the start (the
                                                           # engine's lives begin at 3, so: their first month)
    # a claim granted: the applicant becomes a refugee (after), settled as an immigrant (grants); citizenship ends the
    # refugee status, and naturalised citizen comes with it
    "refugee": dict(after=["asylum applicant"], req="yrs_has('asylum applicant') >= .5", rate=0.6, grants=["immigrant"],
                    lose="has('citizenship')", lrate=1.0),
    "asylum applicant": dict(req="(ago_move < 1) & (had(['war comes'], 3) | mk('moved away', 1)) & "
                                 "~was('asylum applicant')", rate=0.01,
                             lose="yrs_has('asylum applicant') >= 1", lrate=0.3),
    "naturalised citizen": dict(req="has('citizenship') & has('immigrant')", rate=1.0),   # gained with [citizenship]
    "bankruptcy or insolvency in their history": dict(req="had(['financial ruin'], 2)", rate=0.5),
    "on probation or community supervision": dict(req="(has('someone with a record') & "
                                                      "(yrs_has('someone with a record') < 1)) | "
                                                      "(has('ex-prisoner') & (yrs_has('ex-prisoner') < 1))",
                                                  rate=0.4, lose="yrs_has('on probation or community supervision') >= 1",
                                                  lrate=0.5),
    "living in residential care": dict(req="(had(['moving to a smaller home or into care'], 1) & (age >= 60)) | "
                                           "((age >= 80) & (health < .5))", rate=0.1, lose="health > .6", lrate=0.2),   # Library 13:55: health < .3 at 75 was
                                           # too rare in test lives (2 in 100 against the share's 15)
    "returned migrant": dict(req="(age >= 20) & mk('came home', 1) & (mkn('moved away') >= 1)", rate=0.3),
    "displaced by a disaster": dict(req="had(['losing the home', 'war comes'], 1)", rate=0.15,
                                    lose="~had(['losing the home', 'war comes'], 1)", lrate=0.5),
}
