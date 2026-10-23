# Chroma content pack: Politics. The pack's five aims as fields, for aims version 2 (Emren's v25 decision #9, "Every
# held aim, shared capacity and worthwhile development"). Pathways and packs thread, 2026-10-23, to the writers' brief
# (chroma-ideas/v25-prep/packs/fields/BRIEF.md).
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and the pack is in batch.PACKS, so it changes
# no life. The format is the Engine's frozen aims shape (chroma-engine/notes/v25/aims-shape.md, sections 3 and 8: the
# chess entry, key for key, with the keys section 3 adds: demand, window, upkeep, prep and meets);
# chroma-packs/tools/check_fields.py checks it. FIELDS_POLITICS = {aim: field}, one field for each aim of aims.py (v1),
# under the same name. Each keeps v1's face, sphere, domain, tribal and magic, and v1's steps in order as its rungs
# (say, any, req and height unchanged); its dreams are v1's, then the aim's dreams from core/dreams.py (AIM_DREAMS).
# Shapes: the seat and the back room are careers ("to lead the country", "to be the one who makes things happen");
# the argument, the movement and the town are causes. Every shape here has 5 rungs, as every aim has 5 steps, so no
# skip.
#
# How the clocks were set. `years` is (median, 10th, 90th percentile) of steady effort from the rung below, read from
# the catalogue's sources (House of Commons, LGIU, Institute for Government), the years roles.py and the long shots'
# gates ask of a title (yrs_has), the earned odds in PACK.md, the years past heads of government sat in the house
# first, and LEGACY_POLITICS in aims.py (the Historic rung asks age 40 and 8 to 15 years at the top); the rest is
# estimate, and the comment above each field says which. `share` is, of those who keep at it, the share who reach the
# rung; the shares multiply down the ladder, and the products were held against the catalogue's share= (a member of
# parliament is about 1 life in 10,000, a mayor 1 in 500, a head of government 1 in two million): about 3 in 100 of
# those who keep at "to lead the country" reach a seat and about 1 in 2,000 the head of the government. `start` is
# when interest in politics usually comes (the youth wings and school debates from 12 to 14, most members by their
# twenties); the odds fall after late_from but never shut.
#
# `demand` is at steady intensity: hours a week of free time (a council seat sits next to a day job, so its hours
# count; a paid post counts only the extra evenings), money a year and a one-time entry cost as shares of a year's free
# money (party dues .02, a campaign for parliament with its deposit and time off work .15), and how tiring it is.
# `window` marks the real elections and selections only: a council selection about every 2 years (most councils elect
# every 2 to 4 years, some by thirds, with by-elections between), a general election or a mayor's election about
# every 4, each open for the weeks of the selection and the campaign. `upkeep` only where a benefit really fades:
# allies, donors, a following and the people who read a paper drift away after a few years out of the work (access);
# a seat won, a reform passed or a name made stays.

FIELDS_POLITICS = {
    # Clock: House of Commons (650 seats, about 70 new members a year); PACK.md's earned odds (a winnable seat's
    # selection about 12 in 100 per vacancy, the seat then about 1 in 2 on a party ticket; parliament about 1 in 12
    # for a life that pushes at every step); most members held local office first; the last eight UK prime ministers
    # sat 7 to 24 years in the house first (median about 13). The years to a first office and to the party's trust:
    # estimate.
    "to lead the country": dict(
        shape="career", face="W B", sphere="rule", domain="career", calling=True,
        dreams=["the country's leader", "the speaker for all the bands", "to sit at the head of the council"],
        thing="politics", doing="working for the party", contest="an election",
        places=["rule.voice", "rule.counsel", "gather.hall"], prep=["public speaking", "organising", "leading people"],
        meets=["meaning", "competence"],
        people=dict(coach="an old councillor who knows every rule of the chamber",
                    rival="a member who wants the same nomination", peer="the branch's regulars",
                    patron="a senior figure in the party who takes them up"),
        round=["a seat the party cannot win, fought to learn the trade", "a post at the party's head office",
               "the party conference, every year"],
        below="{N} stands for class rep every year, and has a speech ready before anyone else has thought of one",
        tribal="to speak for all the bands at the great gathering", magic="to sit at the head of the realm's council",
        rungs=[
            dict(say="a voice in the party", any=["party member", "campaign volunteer", "local party officer",
                                                  "union rep"],
                 years=(1, 0.3, 3), share=0.9, start=(14, 25, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.01, energy=0.3), window=None, upkeep=None),
            dict(say="a first office", any=["party official", "local councillor", "council candidate",
                                            "parliamentary candidate", "party nomination"],
                 years=(3, 1, 8), share=0.55, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.04, entry=0.05, energy=0.5),
                 window=dict(every=2, open_weeks=8), upkeep=None),
            dict(say="a name the party trusts", any=["allies in the party", "knowing the rules of the house",
                                                     "the party whip", "voice at the town hall"], height="Known",
                 years=(4, 2, 9), share=0.45, contests_y=2, forks=["go_on"],
                 demand=dict(hours=12, money=0.03, entry=0, energy=0.55), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["party work", "office"])),
            dict(say="a seat in parliament", any=["member of parliament", "minister"], height="Notable",
                 years=(8, 3, 16), share=0.12, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=15, money=0.08, entry=0.15, energy=0.75),
                 window=dict(every=4, open_weeks=8), upkeep=None),
            dict(say="leading the country", any=["head of government"], height="Historic",
                 years=(12, 6, 25), share=0.02, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0.1, energy=0.85),
                 window=dict(every=4, open_weeks=6), upkeep=None),
        ]),
    # Clock: a first degree of 3 to 4 years, then a first post at a think tank or in an office (roles.py: an analyst
    # after 2 years in policy, data or reporting; an adviser after a year as organiser, caseworker, analyst or party
    # official); LEGACY_POLITICS asks a reform and 15 years as analyst or adviser, or 8 in the house. Think tanks about
    # 2,200 in the US and 500 in the UK (Penn TTCSP, in the catalogue). Shares: estimate.
    "to change the argument": dict(
        shape="cause", face="U R", sphere="rule", domain="career", calling=True,
        dreams=["to change how the country thinks", "the voice the gathering heeds",
                "the voice that turns the council"],
        thing="the argument", doing="making the case", contest="a public debate",
        places=["rule.voice", "learn.keeping", "gather.talk"], prep=["writing", "public speaking", "research"],
        meets=["meaning", "competence"],
        people=dict(coach="an old speechwriter who still marks up every draft",
                    rival="a writer on the other side who always answers back", peer="the others in the policy team",
                    patron="a minister who reads every paper they send"),
        round=["a column in the local paper", "a think tank's open call for papers",
               "the debating society's meeting, every week"],
        below="{N} argues the other side of every question at the dinner table, just to see whether it holds",
        tribal="to be the voice that turns the gathering's mind", magic="to be the voice that turns the council's mind",
        rungs=[
            dict(say="words that carry", any=["debating", "writing speeches", "reading the polls",
                                               "campaign volunteer"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 22, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.01, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="a desk behind the speeches", any=["speechwriter", "policy analyst", "pollster",
                                                        "political adviser"],
                 years=(3, 1, 7), share=0.35, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.15, entry=0.2, energy=0.5), window=None, upkeep=None),
            dict(say="people read what you write", any=["drafting policy", "a parliamentary pass", "name in the field",
                                                        "a name for straight talk"], height="Known",
                 years=(4, 2, 9), share=0.45, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "writing"])),
            dict(say="the argument is yours", any=["a reform with your name on it", "member of parliament"],
                 height="Notable",
                 years=(8, 3, 18), share=0.12, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=8, money=0.03, entry=0.05, energy=0.65), window=None, upkeep=None),
            dict(say="a change that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(10, 4, 25), share=0.15, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),
    # Clock: roles.py (an adviser after a year as organiser, caseworker, analyst or party official, or 3 as a
    # journalist; a lobbyist from those posts); OpenSecrets (about 12,000 to 13,000 registered US federal lobbyists a
    # year, in the catalogue); the seat as in "to lead the country"; LEGACY_POLITICS asks a reform and 15 years as an
    # adviser or 8 in the house. The years to a name as a fixer: estimate.
    "to be the one who makes things happen": dict(
        shape="career", face="B U", sphere="rule", domain="career", calling=True,
        dreams=["a spy", "a spymaster of the court", "a scout who knows every clan's business"],
        thing="the back room", doing="working the back room", contest="a close vote",
        places=["rule.counsel", "rule.voice", "gather.night"], prep=["organising", "leading people"],
        meets=["competence", "autonomy"],
        people=dict(coach="an old fixer who has seen five leaders come and go",
                    rival="another adviser who wants the same ear", peer="the other staff along the corridor",
                    patron="a minister who trusts their judgement"),
        round=["a lobbying firm that takes on former staff", "a donor's dinner across town",
               "the drinks after the committee, every week"],
        below="{N} always knows who has fallen out with whom in the playground, and quietly sorts it out before the "
              "teacher hears",
        tribal="to be the one every leader listens to before deciding", magic="to be the hand behind the throne",
        rungs=[
            dict(say="knowing the right people", any=["party member", "old school network", "handling the press",
                                                      "fundraising"],
                 years=(1.5, 0.5, 4), share=0.9, start=(16, 25, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="a seat in the back room", any=["political adviser", "lobbyist", "registered lobbyist"],
                 years=(4, 2, 9), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0.1, energy=0.5), window=None, upkeep=None),
            dict(say="the fixer people call", any=["a name as a fixer", "friend in power", "donors"], height="Known",
                 years=(5, 2, 10), share=0.45, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.5), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "party work"])),
            dict(say="power at the top", any=["minister", "member of parliament", "known across the country"],
                 req="was('political adviser') | was('lobbyist')", height="Notable",
                 years=(8, 3, 18), share=0.12, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=12, money=0.08, entry=0.15, energy=0.75),
                 window=dict(every=4, open_weeks=8), upkeep=None),
            dict(say="the hand behind the country", any=["a work that outlives you"], height="Historic",
                 years=(10, 4, 25), share=0.12, contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
    # Clock: ANES (about 3 to 4 US adults in 100 work for a party or candidate in an election year, in the catalogue);
    # roles.py (an organiser from a volunteer or branch officer; a following in the party after 3 years in the cause);
    # a movement that reaches the country commonly takes one to several decades; LEGACY_POLITICS asks a movement founded
    # and still behind its founder, at 40 or more. Shares: estimate.
    "to build a movement": dict(
        shape="cause", face="R G", sphere="rule", domain="faith", calling=True,
        dreams=["to fight for a cause", "to found a movement of one's own"],
        thing="the movement", doing="campaigning", contest="a day of action",
        places=["rule.voice", "gather.great", "gather.hall"], prep=["organising", "public speaking", "leading people"],
        meets=["belonging", "meaning"],
        people=dict(coach="an old organiser who has run a hundred campaigns",
                    rival="a rival group after the same supporters", peer="the volunteers who turn up every weekend",
                    patron="a union that backs the cause"),
        round=["a group in the next town that needs organisers", "a petition passed round online",
               "the open meeting in the community hall, every month"],
        below="{N} talks the whole class into a sponsored walk for the animal shelter, and walks at the front of it",
        tribal="to rouse the bands behind a new way", magic="to raise the commons behind a cause",
        rungs=[
            dict(say="joining the cause", any=["activist in a cause", "campaign volunteer", "canvassing"],
                 years=(0.5, 0.2, 2), share=0.9, start=(14, 25, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.01, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="people behind you", any=["campaign organiser", "a loyal campaign team", "a list of supporters",
                                               "rousing a crowd"],
                 years=(3, 1, 7), share=0.45, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0.02, energy=0.6), window=None, upkeep=None),
            dict(say="a movement behind you", any=["a movement behind you", "a following in the party", "local hero"],
                 height="Known",
                 years=(5, 2, 12), share=0.35, contests_y=2, forks=["go_on"],
                 demand=dict(hours=12, money=0.04, entry=0.02, energy=0.65), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["campaigning", "organising"])),
            dict(say="the movement reaches the country", any=["party leader", "member of parliament",
                                                              "known across the country"],
                 req="was('campaign organiser') | was('activist in a cause') | has('a movement behind you')",
                 height="Notable",
                 years=(8, 3, 20), share=0.1, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=14, money=0.06, entry=0.1, energy=0.8), window=None, upkeep=None),
            dict(say="a movement that outlives you", any=["founder of a movement", "a work that outlives you"],
                 height="Historic",
                 years=(10, 4, 25), share=0.15, contests_y=1, forks=["go_on"],
                 demand=dict(hours=10, money=0.04, entry=0.05, energy=0.7), window=None, upkeep=None),
        ]),
    # Clock: LGIU and NALC (about 17,000 principal and about 100,000 parish and town councillors in England, in the
    # catalogue); councillors mostly first elected in their forties or fifties after years on committees; roles.py (a
    # mayor from a councillor of 3 years, about 1 councillor in 5 over 25 years on the council); LEGACY_POLITICS asks 12
    # years as mayor. The years to a ward post: estimate.
    "to look after the town": dict(
        shape="cause", face="G W", sphere="rule", domain="community", calling=True,
        dreams=["to run the town", "to make one's town a green and fair place to live",
                "an elder whose counsel the clans seek", "a seat on the city council"],
        thing="the town", doing="looking after the town", contest="a ward election",
        places=["rule.counsel", "gather.hall", "rule.voice"], prep=["care", "organising", "public speaking"],
        meets=["belonging", "meaning"],
        people=dict(coach="a councillor who has held the ward for twenty years",
                    rival="a neighbour who stands for the same seat", peer="the residents' committee",
                    patron="the leader of the council, who notices who turns up"),
        round=["the empty seat on the village council", "the caseworker's job in the member's office",
               "the councillor's advice evening at the library, every month"],
        below="{N} knows the name of every dog on the street, and which neighbour needs the shopping carried in",
        tribal="to be the elder the band turns to", magic="to be the town's lord mayor",
        rungs=[
            dict(say="one of the town's helpers", any=["polling-station volunteer", "neighbourhood volunteer",
                                                       "residents' committee member", "knowing every street"],
                 years=(1, 0.3, 3), share=0.9, start=(12, 30, 55), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.01, entry=0, energy=0.25), window=None, upkeep=None),
            dict(say="working for the ward", any=["constituency caseworker", "local party officer", "council candidate",
                                                  "constituency casework"],
                 years=(3, 1, 8), share=0.5, contests_y=1, forks=["take"],
                 demand=dict(hours=7, money=0.02, entry=0.02, energy=0.45), window=None, upkeep=None),
            dict(say="the town knows your name", any=["local councillor", "voice at the town hall",
                                                      "good name in town"], height="Known",
                 years=(4, 2, 10), share=0.5, contests_y=1, forks=["take"],
                 demand=dict(hours=10, money=0.02, entry=0.02, energy=0.5), window=None, upkeep=None),
            dict(say="the town's own", any=["mayor", "member of parliament"],
                 req="was('constituency caseworker') | was('local councillor') | was('local party officer')",
                 height="Notable",
                 years=(7, 3, 15), share=0.2, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=12, money=0.04, entry=0.05, energy=0.65),
                 window=dict(every=4, open_weeks=8), upkeep=None),
            dict(say="a town that remembers you", any=["a work that outlives you"], height="Historic",
                 years=(12, 6, 25), share=0.2, contests_y=1, forks=["go_on"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
}
