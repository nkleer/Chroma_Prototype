# Chroma content pack: Art and Writing. Earned odds: what prepares a person for each title. Pathways and packs thread,
# 2026-10-10, in the shape of ../stage/helps.py, after Emren's answer (10-05 21:03): "give more chance than real odds,
# but keep it consistent and achievable, if player and character create a good strategy, and they are at right place
# at right time." Plain data for the engine; nothing runs.
#
# HELPS: for each title, the titles, perks and history marks that count as preparation for an act that takes it (any
# option with title: <name>; the engine reads the first title of the field). The more of them the person holds, the
# more that act's chance rises above the real base chance (engine: up to +1.0 logit when the list is complete, never
# above 90%). Each list mixes colours, so every colour's road to a title is as well prepared as another's: White's class
# kept and degree finished, Blue's method and technique, Black's dealer and name, Red's walls and open-mic nights,
# Green's circle, place and craft. Marks are prefixed "mark:".

HELPS_ART = {
    # community and status: the taste rung and the school
    "open-mic poet": ["writing poems", "writing stories", "public speaking", "a circle of artists",
                      "mark:took a wild risk"],
    "life-drawing regular": ["drawing and painting", "a circle of artists", "mark:learned a skill"],
    "art school student": ["drawing and painting", "life-drawing regular", "scholarship", "savings", "mentor",
                           "sculpting", "a circle of artists"],
    # careers: the practice rung
    "street artist": ["drawing and painting", "a mural the town loves", "a circle of artists", "life-drawing regular",
                      "following online", "name on the local scene", "mark:defied an authority"],
    "illustrator for hire": ["illustration", "drawing and painting", "art school degree", "following online",
                             "contact in the trade", "selling", "a circle of artists", "mark:kept your word"],
    # careers: the profession and the side roads
    "painter or sculptor": ["drawing and painting", "sculpting", "art school degree", "studio of one's own",
                            "a circle of artists", "a name in the art world", "a dealer who sells your work",
                            "patron", "mentor", "a mural the town loves"],
    "art teacher": ["art school degree", "teaching", "teacher", "graduate", "professional registration",
                    "cleared to work with children", "drawing and painting", "pupils who remember you"],
    "gallery owner": ["savings", "patron", "striking a deal", "selling", "contact in the trade",
                      "a name in the art world", "a circle of artists", "shop owner", "good name in town"],
    "master craftsperson": ["craft maker", "workshop", "tools of one's own", "a maker's hallmark", "sculpting",
                            "pupils who remember you", "selling", "mark:learned a skill"],
    # summits
    "renowned artist": ["a name in the art world", "a dealer who sells your work", "works in collectors' hands",
                        "patron", "a body of work", "a mural the town loves", "a maker's hallmark",
                        "known across the country", "studio of one's own"],
    "celebrated author": ["book in print", "a publishing contract", "a prize for writing", "royalties",
                          "following online", "writing stories", "writing poems", "known across the country",
                          "a body of work"],
    # the base writer's rung: the open-mic poet's collection ('a publisher reads the manuscript') and the long shot
    "novelist": ["writing stories", "writing poems", "book in print", "a publishing contract", "open-mic poet",
                 "a prize for writing", "a circle of artists"],
}

# Windows ("right place at right time"): the doors and steps come when an opening exists, and their rate follows the
# outside context (drivers, as on any life event). A second, smaller lift on the act's chance when the context is
# favourable (engine: up to +0.4 logit), in the same driver words. prosper: good years fill galleries and fund
# commissions; era: new ways of making and showing work (new media, a boom in illustrated books) open posts and walls at
# once; fortune: the person's own luck (the critic who happens by); community: a town that wants its walls painted and
# its makers kept; money: fees and a shop's rent.
WINDOWS_ART = {
    "art school applications": "prosper+.2 money+.2",
    "the degree show": "prosper+.3",
    "a wall that needs a mural": "community+.3 prosper+.1",
    "the first commission": "era+.2 prosper+.2",
    "the first show": "prosper+.3 fortune+.2",
    "the school needs an art teacher": "era+.1",
    "an empty shop on the corner": "prosper+.3 money+.2",
    "the guild judges your masterpiece": "community+.2",
    "a publisher reads the manuscript": "era+.2",
    "a work in the national collection": "era+.2 fortune+.3",
    "a national prize for writing": "era+.2 fortune+.2",
    "the sketch that went round the world": "era+.3 fortune+.3",
    "the open submission to the great summer show": "fortune+.3",
    "the late starter at the easel": "fortune+.2",
    "the judge stops at your table at the craft fair": "community+.2",
}

# The summits stay long shots that preparation only softens, as the Stage pack's lead and Politics' party leader:
# half the preparation and timing lifts. The engine reads it as a multiplier on both lifts.
LIFT_ART = {"renowned artist": .5, "celebrated author": .5}
