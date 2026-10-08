# Chroma content pack: Politics, Elections and Public Office (modern Earth). Catalogue: titles and perks.
# Pathways and packs thread, 2026-10-05; live since 10-06 19:37 Emren's time (16:37 UTC). Emren's line: "Campaign
# volunteer, organizer, adviser, candidate, elected representative, minister. Constituencies, coalitions, campaigning,
# policy compromises and public accountability. Winning office changes your obligations and relationships rather than
# ending progression." Plain data in the fields of chroma-library/earth_perks_titles.py (its header defines every
# field); nothing is imported and nothing runs. Modern Earth terms, as the base catalogue (no worlds field); the forms
# of every title and perk in the tribal and magic worlds are in worlds.py next to this file.
#
# The pack only adds. It reuses the base catalogue's [party member], [local councillor], [activist in a cause],
# [union rep], [residents' committee member], [school-governance board member], [civil-liberties campaigner],
# [graduate], [journalist], [data analyst], [campaigning], [public speaking], [organising people], [striking a deal],
# [settling disputes], [handling red tape], [good name in town], [voice at the town hall], [friend in power],
# [mentor], [patron], [following online] and [inner circle at work] instead of repeating them. The reach ladder
# ([known across the country], [a household name]) is shared by every pathway pack: chroma-packs/core/reach.py.
#
# Choices, on purpose (PACK.md, "Departures"):
#   - [mayor] is a community title, held next to a day job, as most of the world's mayors run small places part-time
#     (France alone has 34,875 communes, each with a mayor). It grows out of the base [local councillor] (same kind).
#     A big-city mayor's season offers giving up the day job.
#   - [minister], [party leader] and [head of government] are facets held on top of [member of parliament] (the
#     engine's refines), each with its own ways and profiles: a seat is kept while in office, and losing it ends them.
#     [head of government] sits on [party leader]. Presidential systems are told through the same chain.
#   - Standing for office is a status that lasts a campaign: [council candidate], [parliamentary candidate],
#     [mayoral candidate] (a direct election for mayor, for someone who never sat on the council; round 3, 2026-10-06).
#     The campaign moments hold it. [former member of parliament] is a status for life.
#   - Perks carry ways (colors), balanced over the five colors, as in the Science pack.
#
# Shares: share of people in a modern rich country who ever hold it. Sources: House of Commons (650 seats; 335 new MPs
# in 2024 and about 70 a year since 2010; 4,515 candidates in 2024), ONS births (about 650,000 to 700,000 a year in the
# UK), Institute for Government (120 paid ministers, at most 95 in the Commons, 2026), LGIU (about 17,000 principal
# councillors in England), NALC (about 10,000 parish and town councils with about 100,000 councillors), NCSL (7,386 US
# state legislators), US Congress (535 members, about 60 to 80 new every two years, against about 3.6 million US
# births a year), Census of Governments (about 19,500 US municipalities; about 511,000 US elected officials in 1992),
# DGCL (34,875 French communes, 2025), Pew Research Center 2024 (about 774,000 US poll workers in 2020 and 644,000 in
# 2022), OpenSecrets (about 12,000 to 13,000 registered US federal lobbyists a year in the 2020s), ANES (about 3 to 4
# US adults in 100 work for a party or a candidate in an election year). Everything else is an estimate, and says so.

# Round 5, 2026-10-07: the outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector= on every career,
# institution= (an at: value) and standing= (0 an ordinary person, 1 local, 2 inside power, 3 national; chroma-world
# spec-7 section 2) on every career and summit.
TITLES = []
PERKS = []

# ---------------------------------------------------------------- careers: the road to parliament and office
TITLES += [
  dict(name="campaign organiser", kind="career", sector="services", institution="party", standing=0, ways="R W",
       profiles=[("R W", "Knocks on doors from dawn to dark for a cause worth winning, and makes the volunteers believe "
                         "it too."),
                 ("B", "Runs the target lists, the rota and the volunteers like a machine built to win."),
                 ("G U", "Builds the campaign street by street, knowing which families talk to which.")],
       meets="need:meaning+.08 need:belonging+.06 res:money+.03 res:time-.15 res:health-.03",
       ages=(18, 70), share=.002,   # estimate: paid field and campaign staff; US presidential and state campaigns hire
                                    # thousands each cycle, UK parties a few hundred; most stay a cycle or two
       say="a campaign organiser",
       gained="'a paid job on the campaign' after a season as a [campaign volunteer]; [campaigning] or [organising "
              "people] learned in a cause or a union",
       lost="the election over and no next campaign; a step up to [political adviser] or [party official]; 'burnout'",
       needs="[campaigning], [organising people] or a season as a [campaign volunteer]",
       turning="Forty volunteers, one weekend left, and the target lists say the ward is lost."),
  dict(name="constituency caseworker", kind="career", sector="public", institution="party", standing=0, ways="G W",
       profiles=[("G W", "Treats every resident as a neighbour, and sees each case through to the end."),
                 ("U", "Knows every form, deadline and office, and finds the rule that unlocks a case."),
                 ("B R", "Picks a fight with the housing office for whoever walks in, and keeps count of the wins.")],
       meets="need:meaning+.08 need:competence+.05 res:money+.04 res:time-.1",
       ages=(18, 75), share=.001,   # estimate: UK MPs employ about four staff each, two of them on casework (about
                                    # 1,300 posts); US district offices about 3,000; turnover every three to four years
       say="a caseworker for an elected member",
       gained="'a paid job on the campaign' that turns into a job in the office of the member; [handling red tape] "
              "learned the hard way",
       lost="the member losing the seat; a step up to [political adviser]; 'burnout'",
       needs="[handling red tape], [graduate] or a season as a [campaign volunteer]"),
  dict(name="political adviser", kind="career", sector="public", institution="ministry", standing=1, ways="U B",
       profiles=[("U B", "Shapes decisions from the room next door, with knowledge and discretion."),
                 ("W G", "Serves the office faithfully, and keeps the boss true to the people who sent them."),
                 ("R", "Burns for the cause inside the building, and tells the boss the hard thing to their face.")],
       meets="need:competence+.08 need:autonomy-.04 res:money+.08 res:time-.15 res:ties-.03",
       ages=(20, 75), share=.003,   # estimate: aides, staffers and special advisers; the US Congress employs about
                                    # 15,000 staff and the states about 30,000; the UK about 3,500 staff to MPs and
                                    # about 120 special advisers; high turnover
       say="a political adviser",
       gained="'a paid job on the campaign' with [graduate]; years as a [campaign organiser], [constituency "
              "caseworker], [policy analyst] or [journalist]",
       lost="the boss losing office; a move to [lobbyist] or [policy analyst] ('leaving politics for another life'); "
            "a step into a race of their own ('a seat falls vacant')",
       needs="[graduate] in most offices, or years of [campaigning]; a member or a minister who hires them",
       turning="The night before the big announcement, the adviser knows something the boss does not want to hear."),
  dict(name="member of parliament", kind="career", sector="public", institution="party", standing=2, ways="W U",
       profiles=[("W U", "Serves the law and the evidence, and reads every bill before voting on it."),
                 ("B R", "Fights to rise, loves the battle in the chamber, and makes a name."),
                 ("G", "Stands for the place they come from and the people who have always lived there.")],
       meets="need:meaning+.1 need:competence+.06 res:money+.1 res:time-.15 res:ties-.04 need:safety-.04",
       ages=(18, 95), share=.0001,   # House of Commons: 650 seats, about 70 new members a year since 2010, against
                                     # 650,000 to 700,000 UK births a year (ONS): about 1 life in 10,000. The US (535
                                     # in Congress for 340 million) is ten times lower; Sweden (349 seats for 10.5
                                     # million) three times higher. The say line can read parliament or congress
       say="a member of parliament",
       gained="'election night' won as a [parliamentary candidate]; a by-election after 'a seat falls vacant'",
       lost="'the night you lose the seat'; standing down; a scandal ('a scandal breaks'); leaving for another life",
       needs="[parliamentary candidate]; in most seats [parliamentary nomination]; age 18 or more",
       turning="The whips want the vote on a bill the constituency hates."),
]

# ---------------------------------------------------------------- facets: office on top of the seat (engine refines)
# Each is held on top of [member of parliament] (head of government on top of party leader), adds its ways and meets
# to the career, and ends when the seat ends. Shares are tiny, and the top stays reachable through the moments.
TITLES += [
  dict(name="minister", kind="career", sector="public", institution="ministry", standing=3, ways="W U", refines="member of parliament",
       profiles=[("W U", "Runs the department by the rules and the evidence, and answers to parliament for it."),
                 ("B", "Trades favours, builds a power base in cabinet, and gets what the department wants."),
                 ("R G", "Speaks for the angry and guards what the country has always been, whatever the officials "
                         "say.")],
       meets="need:autonomy+.06 need:competence+.06 res:money+.05 res:time-.12 res:health-.03",
       ages=(21, 95), share=.00003,   # Institute for Government: 120 paid ministers at a time (at most 95 in the
                                      # Commons); about 1 member in 3 ever holds office (estimate): 1 life in 30,000
       say="a minister",
       gained="'the phone call from the leader' after years as a [member of parliament]; a deal after 'the leadership "
              "falls vacant'",
       lost="'the reshuffle'; resigning over a vote or 'a scandal breaks'; the government falling; the seat lost",
       needs="[member of parliament] in most systems; a leader who asks; [allies in the party] help",
       turning="A policy the minister argued against in cabinet is now theirs to defend in the chamber."),
  dict(name="party leader", kind="career", sector="public", institution="party", standing=3, ways="R", refines="member of parliament",
       profiles=[("R", "Leads by conviction and voice, and the members follow the fire."),
                 ("W G", "Holds a broad church together, and keeps every wing of the party at the table."),
                 ("B U", "Holds the party through its machine and a long plan, three moves ahead of rivals.")],
       meets="need:autonomy+.08 need:meaning+.06 res:time-.15 res:ties-.05 need:safety-.05",
       ages=(25, 95), share=.000005,   # estimate: a rich country has five to ten parties in parliament, each changing
                                       # leader every four to six years: one or two new leaders a year, about 1 life
                                       # in 200,000 to 400,000
       say="the leader of the party",
       gained="'the leadership falls vacant' won by a [member of parliament] with [known across the country] or a "
              "[a following in the party]",
       lost="'the party turns on its leader'; a lost general election; resigning",
       needs="[member of parliament] for years; [known across the country] in most parties",
       turning="The party is at war with itself, and both sides want the leader to choose."),
  dict(name="head of government", kind="career", sector="public", institution="ministry", standing=3, ways="W", refines="party leader",
       profiles=[("W", "Governs for the whole country, through the constitution and its institutions."),
                 ("U B", "Governs by strategy and control, a step ahead of rivals and of events."),
                 ("R G", "Governs as the voice of the people and the guardian of the nation and its ways.")],
       meets="need:meaning+.1 need:autonomy+.08 res:money+.05 res:time-.15 res:health-.05 res:freedom-.1",
       ages=(30, 95), share=.0000005,   # estimate: a new head of government every three to five years in most
                                        # democracies (the UK: 17 prime ministers since 1945), about 1 life in two
                                        # to three million
       say="at the head of the government",
       gained="'the country goes to the polls' won as [party leader]; a coalition deal; a leader who falls in office",
       lost="a lost election; 'the party turns on its leader'; resigning; the term ending",
       needs="[party leader]; [known across the country]",
       turning="A call at three in the morning, and the decision cannot wait for cabinet."),
]

# ---------------------------------------------------------------- careers: side roads of the pathway
TITLES += [
  dict(name="party official", kind="career", sector="services", institution="party", standing=1, ways="W B",
       profiles=[("W B", "Keeps the rules, the lists and the money of the party in order, and holds the machine "
                         "together."),
                 ("G", "Holds the party family together through every leader and every defeat."),
                 ("U R", "Rebuilds the machinery of the party for a new age, trying what nobody has tried.")],
       meets="need:belonging+.08 need:meaning+.05 res:money+.05 res:time-.1",
       ages=(20, 75), share=.0005,   # estimate: paid staff of parties: regional organisers, agents, compliance,
                                     # general secretaries; a few hundred per party in the UK, more in the US
       say="a party official",
       gained="years as a [campaign organiser] or [local party officer]; a post at party headquarters",
       lost="a new leader who brings their own people; money running out after a defeat; 'burnout'",
       needs="[party member]; [organising people] or [campaigning]"),
  dict(name="lobbyist", kind="career", sector="services", institution="employer", standing=1, ways="B U",
       profiles=[("B U", "Sells access and argument to whoever pays, and knows exactly whom to call."),
                 ("W", "Makes the case of the client openly, within the register and its rules."),
                 ("R G", "Lobbies for a cause or a place they love: farmers, a charity, the factory of a town.")],
       meets="res:money+.12 need:competence+.06 res:ties+.05 res:time-.1 need:meaning-.03",
       ages=(22, 80), share=.002,   # OpenSecrets: about 12,000 to 13,000 registered US federal lobbyists a year in the
                                    # 2020s, plus state registers; the UK public affairs trade about 4,000; estimate
                                    # for ever
       say="a lobbyist",
       gained="'leaving politics for another life' as a [political adviser] or [former member of parliament]; years "
              "as a [salesperson] or [journalist] near government",
       lost="a client gone; a ban after 'a donor wants a favour' turns into a scandal; a return to office",
       needs="[graduate] or years in politics; [registered lobbyist] where the law asks for it",
       turning="An old colleague is now the one who decides, and the client wants a meeting by Friday."),
  dict(name="policy analyst", kind="career", sector="public", institution="ministry", standing=0, ways="U",
       profiles=[("U", "Follows the evidence to the policy, wherever it leads."),
                 ("W G", "Designs policy that protects the institutions and communities people rely on."),
                 ("B R", "Writes bold ideas that grab attention and move a party, and enjoys the fight.")],
       meets="need:competence+.08 need:meaning+.06 res:money+.05 res:time-.08",
       ages=(21, 85), share=.002,   # estimate: think tanks (about 2,200 in the US and 500 in the UK, Penn TTCSP
                                    # 2020), party research units and the policy teams of charities and unions
       say="a policy analyst",
       gained="[graduate] and a post at a think tank, a party or a charity; years as a [political adviser]",
       lost="the money of the funders moving on; a move into government as a [political adviser]",
       needs="[graduate]; [finding things out] or [working with data] help"),
  dict(name="speechwriter", kind="career", sector="public", institution="ministry", standing=0, ways="R U",
       profiles=[("R U", "Finds the words that make a hall rise, and polishes them until they ring."),
                 ("G", "Writes in the plain voice of the people back home."),
                 ("W B", "Writes words for power, so that every line can be defended and every promise kept.")],
       meets="need:competence+.08 need:meaning+.05 res:money+.06 res:time-.12 need:autonomy-.04",
       ages=(21, 80), share=.0002,   # estimate: a few hundred posts in a large country (leaders, ministers, mayors,
                                     # big firms)
       say="a speechwriter",
       gained="years as a [political adviser] or [journalist] with [writing stories] or [editing]",
       lost="the speaker losing office; a move to novels or journalism",
       needs="[writing speeches], [writing stories] or [editing]"),
  dict(name="pollster", kind="career", sector="knowledge", institution="employer", standing=0, ways="U",
       profiles=[("U", "Measures what a country thinks, and trusts the method over the hunch."),
                 ("W G", "Listens to people in focus groups and reports fairly what they really say."),
                 ("B R", "Sells the numbers that win, and lives for the night the exit poll lands.")],
       meets="need:competence+.08 res:money+.08 res:time-.1",
       ages=(21, 80), share=.0005,   # estimate: political polling and campaign data teams, a small corner of market
                                     # research
       say="a pollster",
       gained="years as a [data analyst] with [working with data]; a campaign data team after 'a paid job on the "
              "campaign'",
       lost="a famous miss on election night; a move back to market research",
       needs="[working with data] or [reading the polls]"),
]

# ---------------------------------------------------------------- community: democracy as a pastime, and the mayor
TITLES += [
  dict(name="campaign volunteer", kind="community", ways="R G",
       profiles=[("R G", "Gives evenings and weekends to a cause or a candidate they believe in."),
                 ("W", "Does the dull work of democracy: the leaflets, the lists, the phone calls."),
                 ("B U", "Volunteers to learn the trade and meet the people who matter.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.06",
       ages=(14, 100), share=.08,   # ANES: about 3 to 4 US adults in 100 work for a party or a candidate in an
                                    # election year; estimate for ever, over many elections
       say="a campaign volunteer",
       gained="'leaflets to deliver before Saturday'; 'the fight that made you want to stand'; a friend standing for "
              "the council",
       lost="the election over; no time any more; a quarrel with the candidate",
       needs="age 14 or more; a cause or a candidate"),
  dict(name="polling-station volunteer", kind="community", ways="G W",
       profiles=[("G W", "Opens the village hall for every election, as it has always been done."),
                 ("B", "Takes the fee for the day and a front-row seat at how power is counted."),
                 ("U R", "Loves the long day and the late count, and notices every odd thing.")],
       meets="need:belonging+.03 need:meaning+.03 res:money+.02 res:time-.02",
       ages=(16, 95), share=.03,   # Pew Research Center 2024: about 774,000 US poll workers in 2020 and 644,000 in
                                   # 2022; the UK staffs about 40,000 polling stations; estimate for ever
       say="works the polling station on election day",
       gained="'poll workers wanted for election day'",
       lost="no call for the next election; the body no longer up to a fifteen-hour day",
       needs="age 16 to 18 or more, by country; a short training"),
  dict(name="mayor", kind="community", institution="council", standing=2, ways="G W",
       profiles=[("G W", "Looks after the town as a whole: its streets, its old places and its people."),
                 ("B U", "Runs the budget and the patronage of the town hall with a long plan, and gets things built."),
                 ("R", "A big, warm personality who gets the town talking and the cranes up.")],
       meets="need:meaning+.08 need:competence+.05 res:ties+.05 res:time-.12 res:money+.03",
       ages=(21, 95), share=.002,   # estimate: France has a mayor for each of its 34,875 communes (DGCL 2025), the
                                    # US about 19,500 municipalities, England about 300 council leaders and 30
                                    # elected mayors: about 1 life in 250 in France, 1 in 1,000 in the US, far fewer
                                    # in the UK
       say="the mayor",
       gained="'the town needs a mayor' after years as a [local councillor]; 'polling day for mayor' won as a "
              "[mayoral candidate]; leading the council",
       lost="the term over; a lost vote; 'a scandal breaks'; standing down",
       needs="[local councillor] in most places, or a direct election as a [mayoral candidate]; [good name in town] "
             "helps",
       turning="A developer offers the town a stadium, and the price is the old park."),
]

# ---------------------------------------------------------------- faith (cause): the local party
TITLES += [
  dict(name="local party officer", kind="faith", ways="G W",
       profiles=[("G W", "Holds the branch together like a family, meeting after meeting, year after year."),
                 ("B", "Controls the branch: the membership list, the selection meeting and the votes."),
                 ("U R", "Wakes a sleepy branch up with new ideas and new people.")],
       meets="need:belonging+.06 need:meaning+.04 res:ties+.03 res:time-.06",
       ages=(16, 100), share=.01,   # estimate: chairs, secretaries and treasurers of local party branches
       say="an officer of the local party",
       gained="years as a [party member]; 'the ward needs a candidate', for one who would rather run the branch",
       lost="handing on at an annual meeting; a quarrel with the leadership; moving away",
       needs="[party member]; [organising people] helps"),
]

# ---------------------------------------------------------------- statuses: standing, and after
TITLES += [
  dict(name="council candidate", kind="status", ways="", lasts=1,
       meets="need:meaning+.04 need:safety-.03 res:time-.08 res:money-.02",
       ages=(18, 95), share=.03,   # estimate: about three candidates for each principal council seat in England, many
                                   # parish seats uncontested; the US elects about half a million local offices
       say="standing for the council",
       gained="'the ward needs a candidate'; 'the fight that made you want to stand'",
       lost="'polling day in the ward', won or lost",
       needs="age 18 or more; signatures and a deposit in some places; [party nomination] for a party ticket"),
  dict(name="parliamentary candidate", kind="status", ways="", lasts=2,
       meets="need:meaning+.05 need:safety-.05 res:time-.12 res:money-.04",
       ages=(18, 95), share=.001,   # House of Commons: 4,515 candidates for 650 seats in 2024, many standing more than
                                    # once; estimate for ever, about 1 life in 1,000; about 4 in 5 stand in a seat their
                                    # party cannot win (estimate)
       say="standing for parliament",
       gained="'a seat falls vacant' and a selection won; 'a seat the party cannot win', as a paper candidate; standing "
              "as an independent",
       lost="'election night', won or lost",
       needs="[parliamentary nomination] for a party ticket in a seat the party can win (a paper candidate stands "
             "without it); age 18 or more; a deposit"),
  dict(name="mayoral candidate", kind="status", ways="", lasts=2,
       meets="need:meaning+.05 need:safety-.04 res:time-.10 res:money-.03",
       ages=(21, 95), share=.002,   # estimate: where the mayor is elected directly, about two candidates stand for each
                                    # mayor's post, many of them more than once; France has a mayor for each of its
                                    # 34,875 communes (DGCL 2025), the US about 19,500 municipalities (Census of
                                    # Governments); most mayors are chosen from the council and never stand as a
                                    # candidate for mayor; estimate for ever, about 1 life in 500
       say="standing for mayor",
       gained="'a run for mayor from outside the council', after years of standing in the town",
       lost="'polling day for mayor', won or lost",
       needs="years of standing in the town outside the council (a branch office, a committee, a union post, a "
             "business, a good name); signatures and a deposit in some places; age 21 or more"),
  dict(name="former member of parliament", kind="status", ways="", lasts="life",
       meets="need:belonging-.03 res:ties+.03",
       ages=(20, 110), share=.0001,   # nearly every member leaves one day
       say="a former member of parliament",
       gained="'the night you lose the seat'; standing down; 'leaving politics for another life'",
       lost="nothing: the title stays for life (a return to the seat holds both)",
       needs="[member of parliament] once"),
]

# ---------------------------------------------------------------- perks: skills
PERKS += [
  dict(name="canvassing", kind="skill", ways="R W", odds=.04, skill_half=6, retires=None,
       ages=(14, 100), share=.04,   # estimate: campaign volunteers, organisers and candidates
       say="can work a street of doors",
       gained="evenings as a [campaign volunteer]; 'a door slammed in your face' and the next door knocked",
       lost="years off the doorstep", needs="nothing but nerve; [campaigning] helps"),
  dict(name="rousing a crowd", kind="skill", ways="R", odds=.05, skill_half=8, retires=None,
       ages=(16, 100), share=.01,   # estimate
       say="can lift a hall to its feet",
       gained="rallies as a candidate or an [activist in a cause]; 'a speech that goes everywhere'",
       lost="years without a crowd", needs="[public speaking] or [campaigning]"),
  dict(name="debating", kind="skill", ways="U R", odds=.05, skill_half=10, retires=None,
       ages=(12, 100), share=.02,   # estimate: school debaters, councillors, members and advocates
       say="can win an argument in the chamber",
       gained="'a debate or contest at school'; 'the hustings in the church hall'; years in a council chamber",
       lost="years without an opponent", needs="[public speaking] helps"),
  dict(name="fundraising", kind="skill", ways="B G", odds=.04, skill_half=6, retires=None,
       ages=(16, 100), share=.03,   # estimate: campaign and charity fundraisers, party treasurers
       say="can raise money for a cause",
       gained="'the money runs short three weeks out' met; years as a [party official] or [local party officer]",
       lost="years without asking", needs="[striking a deal] or [organising people] help"),
  dict(name="coalition building", kind="skill", ways="W G", odds=.05, skill_half=12, retires=None,
       ages=(18, 100), share=.005,   # estimate
       say="can bring rival groups to one table",
       gained="'a deal to get it through'; years as a [local councillor], [mayor] or [member of parliament] in a hung "
              "chamber",
       lost="years of going it alone", needs="[settling disputes] helps"),
  dict(name="handling the press", kind="skill", ways="U B", odds=.05, skill_half=5, retires=None,
       ages=(18, 100), share=.005,   # estimate: advisers, press officers and members
       say="knows how to handle the press",
       gained="years as a [political adviser] or [member of parliament]; 'a scandal breaks' and survived",
       lost="years out of the news", needs="[public speaking] or [reporting] help"),
  dict(name="constituency casework", kind="skill", ways="G W", odds=.05, skill_half=8, retires=None,
       ages=(18, 100), share=.002,   # estimate
       say="can take a case through the system",
       gained="years as a [constituency caseworker], [local councillor] or [member of parliament]; 'a family about to "
              "lose their home'",
       lost="years away from the casework", needs="[handling red tape] helps"),
  dict(name="drafting policy", kind="skill", ways="U W", odds=.05, skill_half=10, retires=None,
       ages=(20, 100), share=.005,   # estimate
       say="can turn an idea into a workable policy",
       gained="years as a [policy analyst] or [political adviser]; a [minister] with a department",
       lost="years away from the paper", needs="[graduate] or [finding things out]"),
  dict(name="knowing the rules of the house", kind="skill", ways="W B", odds=.04, skill_half=10, retires=None,
       ages=(18, 100), share=.002,   # estimate: members, councillors and the staff who serve them
       say="knows the rules of the house",
       gained="years in a chamber as a [local councillor] or [member of parliament]; 'the whip on the phone'",
       lost="years out of the chamber", needs="a seat or a post in a chamber"),
  dict(name="counting the votes", kind="skill", ways="B", odds=.04, skill_half=6, retires=None,
       ages=(18, 100), share=.001,   # estimate: whips, party managers and branch fixers
       say="knows how every vote will fall",
       gained="'two members want the same nomination' settled; years as a [party official] or a whip",
       lost="years out of the room", needs="[allies in the party] or [knowing the rules of the house]"),
  dict(name="reading the polls", kind="skill", ways="U", odds=.04, skill_half=5, retires=None,
       ages=(18, 100), share=.003,   # estimate
       say="can read what the polls really say",
       gained="years as a [pollster]; 'the poll that says your client is losing' read right",
       lost="the methods moving on", needs="[working with data]"),
  dict(name="writing speeches", kind="skill", ways="R U", odds=.04, skill_half=8, retires=None,
       ages=(18, 100), share=.002,   # estimate
       say="can write words others will say",
       gained="years as a [speechwriter]; 'the speech is due at midnight' met",
       lost="years without a speaker", needs="[writing stories] or [editing]"),
  dict(name="knowing every street", kind="skill", ways="G", odds=.04, skill_half=10, retires=None,
       ages=(16, 110), share=.01,   # estimate: long-serving volunteers, caseworkers and councillors
       say="knows every street and who lives on it",
       gained="years on the same doorsteps as a [campaign volunteer], [constituency caseworker] or [local "
              "councillor]",
       lost="moving away", needs="years in one place"),
]

# ---------------------------------------------------------------- perks: access (odds 0; they work through requires:)
PERKS += [
  dict(name="party nomination", kind="credential", ways="W B", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.025,   # estimate: most council candidates (.03) stand for a party; the nomination for
                                     # parliament is [parliamentary nomination]
       say="has the party's nomination for the council",
       gained="a ward selection won ('the ward needs a candidate'); standing for the council as a [party member]",
       lost="polling day over; deselection",
       needs="[party member] in most parties; a council seat to fight"),
  dict(name="parliamentary nomination", kind="credential", ways="W U B R G", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.0002,   # estimate: about 1 life in 10,000 becomes a [member of parliament] (.0001), and
                                      # about half of those nominated in a seat their party can win are elected
       say="has the party's nomination for a seat in parliament it can win",
       gained="a selection won for a winnable seat ('a seat falls vacant'); years of work for the party as a [local "
              "councillor], [political adviser], [party official], [mayor], [campaign organiser] or [union rep]",
       lost="'election night' lost; deselection; leaving parliament",
       needs="[party member] or [local party officer]; a seat the party can win"),
  dict(name="the party whip", kind="credential", ways="W G", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.0001,   # every member elected for a party
       say="sits with the party in parliament",
       gained="election as a [member of parliament] on [parliamentary nomination]",
       lost="'a vote against your conscience' that goes too far; 'a scandal breaks'; leaving parliament",
       needs="[member of parliament] and [parliamentary nomination]"),
  dict(name="registered lobbyist", kind="credential", ways="B U", odds=0, skill_half=None, retires=None,
       ages=(21, 100), share=.002,   # OpenSecrets and national registers; estimate for ever
       say="is on the register of lobbyists",
       gained="taking a job as a [lobbyist] where the law asks for registration",
       lost="leaving the trade; struck off after a breach",
       needs="[lobbyist]"),
  dict(name="a movement behind you", kind="credential", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.005,   # estimate: candidates backed by a union, a cause or a local movement
       say="has the backing of a movement",
       gained="a cause, a union or a local campaign that backs the candidate ('the fight that made you want to "
              "stand')",
       lost="the campaign over; a vote that betrays the movement",
       needs="a candidacy; [activist in a cause], [union rep] or [a following in the party] help"),
  dict(name="a parliamentary pass", kind="credential", ways="U R", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.003,   # estimate: the UK parliament issues passes to members, staff, lobbyists and
                                     # former members
       say="has a pass to parliament",
       gained="a post as a [political adviser], [constituency caseworker] or [lobbyist]; a seat; being a [former member "
              "of parliament]",
       lost="the post ending; a pass withdrawn after a breach",
       needs="a post in or near parliament"),
]

# ---------------------------------------------------------------- perks: standing
PERKS += [
  dict(name="a following in the party", kind="standing", ways="R G", odds=.05, skill_half=6, retires=None,
       ages=(18, 110), share=.002,   # estimate
       say="has a following among the members",
       gained="years as a [local party officer] or [member of parliament]; 'the speech at the party conference'; "
              "'a speech that goes everywhere'",
       lost="'the party turns on its leader'; a betrayal of the members", needs="[party member] for years"),
  dict(name="a safe seat", kind="standing", ways="G B", odds=.05, skill_half=4, retires=None,
       ages=(21, 110), share=.00005,   # estimate: about half the seats in a first-past-the-post parliament seldom
                                       # change hands
       say="holds a safe seat",
       gained="selection for a seat the party always wins; years as its [member of parliament]",
       lost="new boundaries; a landslide the other way ('the night you lose the seat')",
       needs="[member of parliament]"),
  dict(name="a reform with your name on it", kind="standing", ways="W U", odds=.05, skill_half=20, retires=None,
       ages=(21, 110), share=.002,   # estimate: a bylaw, a law or a policy that lasts and is known by its author
       say="made a reform that bears their name",
       gained="'a deal to get it through'; 'the decision that will carry your name'; years as a [mayor] or [minister]",
       lost="the reform repealed", needs="an office that makes rules"),
  dict(name="a name for straight talk", kind="standing", ways="R W", odds=.04, skill_half=8, retires=None,
       ages=(18, 110), share=.005,   # estimate
       say="has a name for straight talk",
       gained="'kept your word' in office many times; 'news the boss does not want to hear' told",
       lost="'broke your word' in public; 'hid a wrong' found out", needs="an office or a post people watch"),
  dict(name="a name as a fixer", kind="standing", ways="B U", odds=.05, skill_half=6, retires=None,
       ages=(20, 110), share=.003,   # estimate
       say="has a name as a fixer",
       gained="years as a [party official], [lobbyist] or [political adviser] with [striking a deal]",
       lost="a deal that blows up in public ('a scandal breaks')", needs="[striking a deal]"),
]

# ---------------------------------------------------------------- perks: bonds
PERKS += [
  dict(name="allies in the party", kind="bond", ways="W B", odds=.05, skill_half=5, retires=None,
       ages=(18, 110), share=.005,   # estimate
       say="has allies in the party",
       gained="favours given and returned over years as a [local councillor], [member of parliament] or [party "
              "official]",
       lost="'the reshuffle'; a betrayal; backing the losing side when 'the leadership falls vacant'",
       needs="[party member]"),
  dict(name="donors", kind="bond", ways="B R", odds=.05, skill_half=4, retires=None,
       ages=(21, 110), share=.002,   # estimate
       say="has donors who answer the phone",
       gained="[fundraising] for years; 'the money runs short three weeks out' met",
       lost="'a donor wants a favour' refused; a scandal", needs="[fundraising]"),
  dict(name="a loyal campaign team", kind="bond", ways="R G", odds=.05, skill_half=5, retires=None,
       ages=(18, 110), share=.002,   # estimate
       say="has a campaign team that would follow them anywhere",
       gained="a race won or lost together ('polling day in the ward', 'election night')",
       lost="the team scattered; a promise to them broken", needs="a campaign of their own"),
  dict(name="friends across the aisle", kind="bond", ways="G U", odds=.04, skill_half=8, retires=None,
       ages=(18, 110), share=.002,   # estimate
       say="has friends on the other side",
       gained="years in a chamber; 'a deal to get it through' with the other side",
       lost="a campaign that turns personal", needs="a seat or a post in a chamber; 'made a friend'"),
  dict(name="officials who trust you", kind="bond", ways="U W", odds=.05, skill_half=4, retires=None,
       ages=(21, 110), share=.003,   # estimate: civil servants and council officers who tell an office-holder the
                                     # truth
       say="has officials who trust them",
       gained="'the officials say it cannot be done' heard out; 'the department starts to trust you'; years as a "
              "[mayor]",
       lost="'the reshuffle'; blaming officials in public", needs="an office with officials under it"),
]

# ---------------------------------------------------------------- perks: assets
PERKS += [
  dict(name="a campaign war chest", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.003,   # estimate
       say="has money in the bank for the next campaign",
       gained="'the money runs short three weeks out' met; [donors]; [savings] put in",
       lost="spent on a campaign; returned after a breach of the spending rules",
       needs="a candidacy or a seat"),
  dict(name="a list of supporters", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 110), share=.005,   # estimate
       say="has a list of people who will turn out",
       gained="seasons of [canvassing]; a campaign of their own",
       lost="the list gone stale after years; taken by a rival",
       needs="[canvassing]"),
]
