# Chroma content pack: Stage and Screen. Earned odds: what prepares a person for each title. Pathways and packs thread,
# 2026-10-06, after Emren's answer (21:03): "give more chance than real odds, but keep it consistent and achievable, if
# player and character create a good strategy, and they are at right place at right time." The rule is in
# chroma-packs/PROPOSAL.md, section 2 ("Earned odds"); the per-step figures are in PACK.md. Plain data for the engine;
# nothing runs.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>; the engine reads the first title of the field). The more of them the person holds, the
# more that act's chance rises above the real base chance (engine: up to +1.0 logit when the list is complete, never
# above 90%). The same list works for every life, played or simulated; ordinary lives seldom hold many of them, so the
# simulated shares stay close to the real ones. Each list mixes colors, so a Red or Green road to a part is as well
# prepared as a Blue or White one: the company player's reliability, the craft actor's training, the networker's agent,
# the raw talent's fringe, the local player's company. Names in [brackets] in the catalogues are written here plainly;
# marks are prefixed "mark:".

HELPS_STAGE = {
    # careers: the actor's road
    "professional actor": ["acting", "drama school diploma", "auditioning", "casting directory listing", "a showreel",
                           "an agent who believes in you", "a year group from drama school",
                           "a company that feels like family", "improvisation", "a lead role to remember"],
    "voice actor": ["accents and voices", "acting", "a showreel", "studio of one's own", "community-radio presenter",
                    "singing", "telling a story aloud", "an agent who believes in you"],
    "lead actor or actress": ["acting", "learning lines", "good notices", "a director who keeps casting you",
                              "an agent who believes in you", "a known face", "understudy", "a lead role to remember",
                              "a company that feels like family", "accents and voices", "a producer who backs you",
                              "mark:kept your word"],
    "director": ["directing actors", "acting", "stagecraft", "community theatre director", "a company of your own",
                 "good notices", "a producer who backs you", "writing scripts", "mentor",
                 "a company that feels like family"],
    "artistic director": ["director", "a company of your own", "good notices", "a producer who backs you",
                          "organising people", "patron", "contact in the trade", "telling a story aloud",
                          "mark:kept your word"],
    "playwright or screenwriter": ["writing scripts", "writing stories", "a fringe slot", "book in print", "editing",
                                   "a company of your own", "a producer who backs you", "improvisation", "mentor"],
    "producer": ["striking a deal", "organising people", "savings", "contact in the trade", "a company of your own",
                 "a casting eye", "patron", "bookkeeping", "a company that feels like family"],
    # careers: side roads
    "stage manager": ["stagecraft", "calling the show", "organising people", "first-aid certificate",
                      "reliable record", "stage technician", "drama school diploma", "learning lines",
                      "mark:kept your word"],
    "casting director": ["a casting eye", "contact in the trade", "talent agent", "acting", "directing actors",
                         "organising people", "a company that feels like family", "mark:made a friend"],
    "talent agent": ["striking a deal", "selling", "a casting eye", "contact in the trade", "friend in power",
                     "casting directory listing", "professional actor", "mark:made a friend"],
    "drama teacher": ["acting", "teaching", "teacher", "cleared to work with children", "directing actors",
                      "drama school diploma", "telling a story aloud", "improvisation", "a lead role to remember"],
    # community and statuses
    "background artist": ["casting directory listing", "acting", "reliable record", "screen acting"],
    "amateur actor": ["acting", "youth theatre member", "a lead role to remember", "singing", "dancing",
                      "learning lines", "mark:made a friend"],
    "youth theatre member": [],
    "community theatre director": ["directing actors", "amateur actor", "a lead role to remember", "organising people",
                                   "stagecraft", "good name in town", "a company that feels like family",
                                   "name on the local scene"],
    "drama school student": ["acting", "youth theatre member", "a lead role to remember", "auditioning",
                             "improvisation", "singing", "dancing", "scholarship", "mentor", "amateur actor"],
    "understudy": ["learning lines", "acting", "a director who keeps casting you", "reliable record", "union card",
                   "mark:kept your word"],
}

# An ask, not read by the engine today (a perk key in HELPS raises an error, since HELPS keys are titles): the amateur,
# child and fringe lead is the standing perk [a lead role to remember], given by grants: on options in
# 'casting night at the local players', 'the summer show casts its lead', 'a casting call for children' and 'opening
# night at the fringe'. Emren's lead must be reachable, with earned odds, on those roads too, so the pack asks the engine
# to read HELPS for an act that grants a standing perk as it does for title: (PACK.md, "What the engine needs", 6).
HELPS_PERK_STAGE = {
    "a lead role to remember": ["acting", "learning lines", "youth theatre member", "amateur actor", "singing",
                                "dancing", "improvisation", "a company that feels like family",
                                "stagecraft"],   # not mark:learned a skill, which most adults hold (engine, 03:11)
}

# Windows ("right place at right time"): the doors and crossings come when an opening exists, and their rate follows
# the outside context (drivers, as on any life event). A second, smaller lift on the act's chance when the context is
# favourable (engine: up to +0.4 logit), in the same driver words. prosper: good years fill theatres and fund new shows;
# era: new ways of making and showing drama (a boom in series, new channels) open parts and posts at once; fortune:
# the person's own luck (the lead falls ill on the night the producer is in); community: a town with a live amateur
# scene; ties: the people who know your work; family: the parent who drives a child to the audition.
WINDOWS_STAGE = {
    "drama school auditions": "prosper+.2 money+.2",        # fees and the trains to the auditions
    "an open audition in the city": "prosper+.3",
    "the showcase for agents": "prosper+.3",
    "cast as understudy to the lead": "prosper+.2",          # long runs need understudies
    "the understudy goes on": "fortune+.4",
    "the part of a lifetime is cast": "era+.2 fortune+.3",
    "a screen test": "era+.3 prosper+.2",                    # a boom in series casts the most new faces
    "the leading player leaves the company": "fortune+.3",
    "opening night at the fringe": "fortune+.3 prosper+.1",
    "the lead voice in a series": "era+.3",
    "the director calls again": "ties+.3",
    "casting night at the local players": "community+.3 ties+.2",
    "the summer show casts its lead": "community+.3",
    "a casting call for children": "family+.3",
    "a voice for the cartoon": "era+.2 prosper+.2",
    "the stage management team is a person short": "prosper+.2",
    "a director is needed for the autumn play": "community+.3",
    "the script competition": "era+.2",
    "the theatre needs an artistic director": "era+.3",
    # Round 5, 2026-10-07: the two new step moments (checklist P3, P16) in the same driver words as their own drivers:
    "the city wants the town's show": "community+.2 prosper+.2",   # a town proud of its show, theatres with gaps
    "the school needs someone to take drama": "era+.1",            # schools that keep the arts on the timetable
}

# The lead stays a long shot that preparation only softens (PACK.md, "Earned odds"): Emren's lead gets half the
# preparation and timing lifts, as Politics' party leader does. The engine reads it as a multiplier on both lifts.
LIFT_STAGE = {"lead actor or actress": .5}
