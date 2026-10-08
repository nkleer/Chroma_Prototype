# Chroma content pack: Politics, Elections and Public Office. Earned odds: what prepares a person for each title.
# Pathways and packs thread, 2026-10-05, after Emren's answer (21:03): "give more chance than real odds, but keep it
# consistent and achievable, if player and character create a good strategy, and they are at right place at right time."
# The rule is in chroma-packs/PROPOSAL.md, section 2 ("Earned odds"); the per-step figures are in PACK.md. Plain data
# for the engine; nothing runs.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>). The more of them the person holds, the more that act's chance rises above the real base
# chance (proposed: up to about +1.0 logit when the list is complete, never above 90%). The same list works for every
# life, played or simulated; ordinary lives seldom hold many of them, so the simulated shares stay close to the real
# ones. Each list mixes colors, so a Red or Green road to a rung is as well prepared as a Black or Blue one.
# Names in [brackets] in the catalogues are written here plainly; marks are prefixed "mark:".

HELPS_POLITICS = {
    # careers: the road to parliament and office
    "campaign organiser": ["campaign volunteer", "canvassing", "campaigning", "organising people", "knowing every street",
                           "a list of supporters", "mark:kept your word"],
    "constituency caseworker": ["handling red tape", "constituency casework", "calming people down", "graduate",
                                "knowing every street", "mark:helped someone in need"],
    "political adviser": ["graduate", "drafting policy", "handling the press", "campaign organiser", "mentor",
                          "friend in power", "allies in the party", "a parliamentary pass"],
    "member of parliament": ["parliamentary nomination", "local councillor", "canvassing", "debating", "a list of supporters",
                             "a loyal campaign team", "a campaign war chest", "a movement behind you",
                             "good name in town", "public speaking"],
    "minister": ["drafting policy", "knowing the rules of the house", "allies in the party", "handling the press",
                 "a safe seat", "friend in power", "known across the country", "mark:kept your word"],
    "party leader": ["known across the country", "a following in the party", "allies in the party",
                     "rousing a crowd", "counting the votes", "donors", "minister"],
    "head of government": ["known across the country", "a following in the party", "coalition building", "donors",
                           "a loyal campaign team", "handling the press", "minister"],
    # careers: side roads
    "party official": ["party member", "local party officer", "organising people", "fundraising", "counting the votes",
                       "campaign organiser"],
    "lobbyist": ["former member of parliament", "political adviser", "striking a deal", "friend in power",
                 "a parliamentary pass", "a name as a fixer", "friends across the aisle"],
    "policy analyst": ["graduate", "finding things out", "working with data", "drafting policy", "mentor",
                       "published research"],
    "speechwriter": ["writing stories", "editing", "writing speeches", "political adviser", "journalist",
                     "public speaking"],
    "pollster": ["working with data", "reading the polls", "data analyst", "graduate", "knowing every street"],
    # community, faith and statuses
    "campaign volunteer": [],
    "polling-station volunteer": ["reliable record", "good name in town"],
    "mayor": ["local councillor", "good name in town", "voice at the town hall", "coalition building",
              "officials who trust you", "a loyal campaign team", "knowing every street", "mark:kept your word"],
    "local party officer": ["party member", "organising people", "bookkeeping", "mark:kept your word"],
    "council candidate": ["party member", "good name in town", "canvassing", "campaign volunteer", "activist in a cause",
                          "residents' committee member", "public speaking"],
    "parliamentary candidate": ["parliamentary nomination", "local councillor", "political adviser", "allies in the party",
                                "a following in the party", "union rep", "mayor", "campaign organiser"],
    # round 3: the candidacy for a direct election for mayor, from years of standing outside the council
    "mayoral candidate": ["voice at the town hall", "good name in town", "local party officer",
                          "residents' committee member", "a list of supporters", "canvassing", "organising people"],
    "former member of parliament": [],
}

# Windows ("right place at right time"): the doors and crossings come when an opening exists, and their rate follows
# the outside context (drivers, as on any life event). Proposed as a second, smaller lift on the act's chance when the
# context is favourable (up to about +0.4 logit), in the same driver words; the engine decides whether to build it.
# era: new laws and new leaders arrive (a change of government opens seats, posts and ministries); unrest: anger
# that favours challengers and new faces; prosper: good years that favour the people already in office.
WINDOWS_POLITICS = {
    "the ward needs a candidate": "era+.2 unrest+.2",
    "a paid job on the campaign": "era+.3 unrest+.2",       # big, open elections hire the most staff
    "the fight that made you want to stand": "unrest+.3",
    "polling day in the ward": "unrest+.2",                  # an angry year unseats incumbents
    "a seat falls vacant": "era+.3 unrest+.2",
    "election night": "unrest+.2 era+.2",
    "the town needs a mayor": "era+.2",
    "polling day for mayor": "unrest+.2 era+.1",            # round 3: an angry year favours a newcomer to the town hall
    "the phone call from the leader": "era+.4",              # a new government fills every post at once
    "the leadership falls vacant": "unrest+.3 prosper-.2",
    "the country goes to the polls": "unrest+.3 prosper-.2", # hard times favour the opposition's leader
    # Round 5, 2026-10-07 (P9): the long shot for the campaign's own posts; an early or angry election leaves the gaps
    "the campaign loses its organiser": "era+.2 unrest+.1",
}

# The summit stays a long shot (PACK.md, "Earned odds"): the top two rungs get half the preparation and timing lifts.
# The engine reads it as a multiplier on both lifts (engine, 22:12).
LIFT_POLITICS = {"party leader": .5, "head of government": .5}
