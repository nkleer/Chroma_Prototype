# Chroma content pack: Politics. The public callings' ladders, for aims version 1 (chroma-ideas/next-table-2026-10-19/
# plan.md, section 5: "Packs. The ladders for the public callings: politics, science, stage, art"; Emren 10-19 11:38 UTC,
# "can we create more 'aim' for player"). Pathways and packs thread, 2026-10-19.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims switch is on (batch.py reads catalogue.py, roles.py and
# helps.py only), so it changes no life. The format is set out in chroma-packs/tools/check_aims.py, which checks it.
# In short, AIMS_<PACK> = {aim, as the character would say it: dict(face, domain, sphere, dreams, tribal, magic, steps)}:
#   face    the colour face, one colour or a pair (the fifteen faces); the pack's five faces together are colour-even
#   domain  the goal domain (career, partner, children, community, faith; "" for a pursuit), as the engine's goal slots
#   sphere  the sphere whose rung 4 or 5 also counts as the ladder's Known step (sphere_data.SPHERES codes)
#   dreams  the Library's dreams (chroma-library/dreams.py) that can grow into this aim, in any world
#   tribal, magic  the aim in the game's other worlds; each step's titles carry their own forms (worlds.py)
#   steps   3 to 5 rungs. A step is reached when one of its `any` titles or perks is held or was held (and its `req`,
#           if any, holds then). `height` is the height the step stands for: Known, Notable or Historic.
# LEGACY_<PACK>: who in this pack can earn [a work that outlives you] (core/legacy.py), the Historic marker.
#
# One calling per road (PACK.md, "Roads per color"), each road's lead colour with a second colour from its titles, so
# the five faces make a ring (W B, B U, U R, R G, G W) and every colour stands in two of them. Across the four packs
# every colour pair has two callings (check_aims.py prints the table).

AIMS_POLITICS = {
    # W, party and office: the statesperson
    "to lead the country": dict(
        face="W B", domain="career", sphere="rule",
        dreams=[],
        tribal="to speak for all the bands at the great gathering", magic="to sit at the head of the realm's council",
        steps=[
            dict(say="a voice in the party", any=["party member", "campaign volunteer", "local party officer",
                                                  "union rep"]),
            dict(say="a first office", any=["party official", "local councillor", "council candidate",
                                            "parliamentary candidate", "party nomination"]),
            dict(say="a name the party trusts", any=["allies in the party", "knowing the rules of the house",
                                                     "the party whip", "voice at the town hall"], height="Known"),
            dict(say="a seat in parliament", any=["member of parliament", "minister"], height="Notable"),
            dict(say="leading the country", any=["head of government"], height="Historic"),
        ]),
    # U, policy and polling: the one who changes the argument
    "to change the argument": dict(
        face="U R", domain="career", sphere="rule",
        dreams=[],
        tribal="to be the voice that turns the gathering's mind", magic="to be the voice that turns the council's mind",
        steps=[
            dict(say="words that carry", any=["debating", "writing speeches", "reading the polls",
                                               "campaign volunteer"]),
            dict(say="a desk behind the speeches", any=["speechwriter", "policy analyst", "pollster",
                                                        "political adviser"]),
            dict(say="people read what you write", any=["drafting policy", "a parliamentary pass", "name in the field",
                                                        "a name for straight talk"], height="Known"),
            dict(say="the argument is yours", any=["a reform with your name on it", "member of parliament"],
                 height="Notable"),
            dict(say="a change that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # B, lobbying and the back room: the one who makes things happen
    "to be the one who makes things happen": dict(
        face="B U", domain="career", sphere="rule",
        dreams=["a spy", "a spymaster of the court", "a scout who knows every clan's business"],
        tribal="to be the one every leader listens to before deciding", magic="to be the hand behind the throne",
        steps=[
            dict(say="knowing the right people", any=["party member", "old school network", "handling the press",
                                                      "fundraising"]),
            dict(say="a seat in the back room", any=["political adviser", "lobbyist", "registered lobbyist"]),
            dict(say="the fixer people call", any=["a name as a fixer", "friend in power", "donors"], height="Known"),
            dict(say="power at the top", any=["minister", "member of parliament", "known across the country"],
                 req="was('political adviser') | was('lobbyist')", height="Notable"),
            dict(say="the hand behind the country", any=["a work that outlives you"], height="Historic"),
        ]),
    # R, campaigning and the bold bid: the one who builds a movement (a cause: the faith domain, as the dreams have it)
    "to build a movement": dict(
        face="R G", domain="faith", sphere="rule",
        dreams=["to fight for a cause", "to found a movement of one's own"],
        tribal="to rouse the bands behind a new way", magic="to raise the commons behind a cause",
        steps=[
            dict(say="joining the cause", any=["activist in a cause", "campaign volunteer", "canvassing"]),
            dict(say="people behind you", any=["campaign organiser", "a loyal campaign team", "a list of supporters",
                                               "rousing a crowd"]),
            dict(say="a movement behind you", any=["a movement behind you", "a following in the party", "local hero"],
                 height="Known"),
            dict(say="the movement reaches the country", any=["party leader", "member of parliament",
                                                              "known across the country"],
                 req="was('campaign organiser') | was('activist in a cause') | has('a movement behind you')",
                 height="Notable"),
            dict(say="a movement that outlives you", any=["founder of a movement", "a work that outlives you"],
                 height="Historic"),
        ]),
    # G, the ward, the caseworker and the town: the one who looks after the town
    "to look after the town": dict(
        face="G W", domain="community", sphere="rule",
        dreams=["to run the town", "to make one's town a green and fair place to live",
                "an elder whose counsel the clans seek", "a seat on the city council"],
        tribal="to be the elder the band turns to", magic="to be the town's lord mayor",
        steps=[
            dict(say="one of the town's helpers", any=["polling-station volunteer", "neighbourhood volunteer",
                                                       "residents' committee member", "knowing every street"]),
            dict(say="working for the ward", any=["constituency caseworker", "local party officer", "council candidate",
                                                  "constituency casework"]),
            dict(say="the town knows your name", any=["local councillor", "voice at the town hall",
                                                      "good name in town"], height="Known"),
            dict(say="the town's own", any=["mayor", "member of parliament"],
                 req="was('constituency caseworker') | was('local councillor') | was('local party officer')",
                 height="Notable"),
            dict(say="a town that remembers you", any=["a work that outlives you"], height="Historic"),
        ]),
}

# Who in politics can earn [a work that outlives you] (core/legacy.py): a government led, a party led for years, a reform
# with one's name on it after long years in the house or behind it, a town led for a generation, a movement founded.
LEGACY_POLITICS = ("(age >= 40) & ((yrs_has('head of government') >= 2) | (yrs_has('party leader') >= 5) | "
                   "(has('a reform with your name on it') & ((yrs_has('member of parliament') >= 8) | "
                   "(yrs_has('policy analyst') >= 15) | (yrs_has('political adviser') >= 15))) | "
                   "(yrs_has('mayor') >= 12) | (was('founder of a movement') & has('a movement behind you')))")
