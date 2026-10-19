# Chroma content pack: The Five Callings. Earned odds: what prepares a person for each title. Pathways and packs
# thread, 2026-10-19, in the shape of ../art/helps.py, after Emren's answer (10-05 21:03): "give more chance than real
# odds, but keep it consistent and achievable, if player and character create a good strategy, and they are at right
# place at right time." Plain data for the engine; nothing runs. SWITCHED OFF until `callings` is in batch.PACKS.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>; the engine reads the first title of the field). The more of them the person holds, the
# more that act's chance rises above the real base chance (engine: up to +1.0 logit when the list is complete, never
# above 90%). Each list mixes colours, so every colour's road to a title is as well prepared as another's: White's
# degree, rule and kept word, Blue's skill and method, Black's backers and name, Red's courage and risk, Green's
# people, place and patience. Marks are prefixed "mark:".

HELPS_CALLINGS = {
    # W: the faith leader
    "senior cleric": ["scripture", "leading a ceremony", "preaching", "a degree in theology", "a flock that follows you",
                      "known face at worship", "good name in town", "mentor", "mark:kept your word"],
    "head of a faith order": ["a flock that follows you", "a degree in theology", "preaching", "known across the country",
                              "good name in town", "friend in power", "organising people", "settling disputes",
                              "mark:helped someone in need"],
    # U: the inventor
    "inventor": ["prototyping", "fixing things", "machining", "writing code", "workshop", "tools of one's own",
                 "a patent of your own", "savings", "mark:learned a skill", "mark:took a wild risk"],
    "celebrated inventor": ["a patent of your own", "an invention in everyday use", "name in the field", "prototyping",
                            "investors who back you", "workshop", "known across the country", "apprentice of one's own"],
    # B: the magnate
    "chief executive": ["striking a deal", "bookkeeping", "selling", "investors who back you", "a seat on boards",
                        "organising people", "good credit", "contact in the trade", "mark:took a wild risk"],
    "magnate": ["investors who back you", "a seat on boards", "shares", "friend in power", "striking a deal",
                "good credit", "inner circle at work", "known across the country", "old family name"],
    # R: the commander
    "army officer": ["leading soldiers", "keeping fit", "graduate", "rank", "old comrades", "award for bravery",
                     "mentioned in dispatches", "first-aid certificate", "navigation", "mark:defied an authority"],
    "general": ["leading soldiers", "rank", "mentioned in dispatches", "award for bravery", "old comrades",
                "friend in power", "organising people", "known across the country"],
    # G: the healer
    "senior nurse or midwife": ["professional registration", "home nursing", "emergency care", "licence to prescribe",
                                "families who send for you", "calming people down", "used to night shifts",
                                "strong stomach", "mark:helped someone in need"],
    "renowned healer": ["families who send for you", "a clinic of your own", "licence to prescribe", "name in the field",
                        "home nursing", "calming people down", "good name in town", "known across the country",
                        "apprentice of one's own"],
}

# Windows ("right place at right time"): the steps come when an opening exists, and their rate follows the outside
# context (drivers, as on any life event). A second, smaller lift on the act's chance when the context is favourable
# (engine: up to +0.4 logit), in the same driver words. prosper: good years fund firms, wards and new buildings; era:
# new machines and new ways of working open posts and markets at once; fortune: the person's own luck; community: a
# congregation, a district or a town that wants someone of its own; money: fees, loans and backers.
WINDOWS_CALLINGS = {
    "the congregation needs a senior minister": "community+.3",
    "the order chooses its head": "community+.2 fortune+.2",
    "the prototype works": "era+.3 fortune+.2",
    "an invention in every home": "era+.3 prosper+.2",
    "the board needs a chief executive": "prosper+.3 money+.2",
    "a rival firm is for sale": "prosper+.2 money+.3",
    "officer selection": "era+.1",
    "the army needs a new general": "era+.2 fortune+.2",
    "the ward needs someone in charge": "prosper+.1 community+.2",
    "patients come from far away": "community+.3 fortune+.2",
    # long shots
    "a sermon that goes round the country": "era+.2 fortune+.3",
    "the garage invention": "era+.3 fortune+.3",
    "the market stall that became a chain": "prosper+.3 fortune+.2",
    "the field commission": "fortune+.3",
    "the remedy that worked": "community+.2 fortune+.3",
}

# The summits stay long shots that preparation only softens, as the other packs' summits: half the preparation and
# timing lifts. The engine reads it as a multiplier on both lifts.
LIFT_CALLINGS = {"head of a faith order": .5, "celebrated inventor": .5, "magnate": .5, "general": .5,
                 "renowned healer": .5}
